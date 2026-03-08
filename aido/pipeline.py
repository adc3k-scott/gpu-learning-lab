"""
AIDO Pipeline Orchestrator
Runs the full EP001 production pipeline end-to-end.

Stages:
  1. TTS Generation   — ElevenLabs → per-segment MP3s
  2. Content Injection — manifest → USD sublayer overlays
  3. Omniverse Render — Kit headless → PNG frames (runs on RunPod)
  4. FFmpeg Assembly  — frames + audio → EP001_final.mp4
  5. YouTube Upload   — final MP4 → YouTube (private by default)

Usage:
    # Full pipeline (TTS + USD + assemble with static bg, no Omniverse locally)
    python -m aido.pipeline --episode EP001 --skip-render

    # Full pipeline including Omniverse render (RunPod only)
    python -m aido.pipeline --episode EP001

    # Resume from a specific stage
    python -m aido.pipeline --episode EP001 --from-stage assemble

    # Skip YouTube upload
    python -m aido.pipeline --episode EP001 --skip-render --no-upload
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("aido.pipeline")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
    datefmt="%H:%M:%S",
)

STAGES = ("tts", "inject", "render", "assemble", "upload")
# render modes
_RENDER_OMNIVERSE = "omniverse"   # RunPod GPU — NVIDIA Omniverse Kit headless
_RENDER_LOCAL = "local"           # CPU — Pexels B-roll + ffmpeg news template
_RENDER_SKIP = "skip"             # Static dark background (original fallback)


def _banner(msg: str) -> None:
    bar = "=" * 60
    logger.info(bar)
    logger.info("  %s", msg)
    logger.info(bar)


def run_pipeline(
    episode_id: str,
    out_dir: str,
    skip_render: bool = False,
    no_upload: bool = False,
    from_stage: str = "tts",
    privacy: str = "private",
    fps: int = 24,
    render_mode: str = _RENDER_SKIP,
) -> None:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    manifest_path = out / "manifest.json"

    # Load or initialize manifest
    if manifest_path.exists() and from_stage != "tts":
        with open(manifest_path, encoding="utf-8") as f:
            d = json.load(f)
        from aido.manifest_schema import EpisodeManifest
        manifest = EpisodeManifest.from_dict(d)
        logger.info("Loaded existing manifest for %s", episode_id)
    else:
        import aido.manifest_schema as ms
        manifest = getattr(ms, episode_id, None)
        if manifest is None:
            logger.error("Unknown episode: %s", episode_id)
            sys.exit(1)
        manifest.output_dir = str(out.resolve())

    active_stages = STAGES[STAGES.index(from_stage):]
    t0 = time.time()

    # ------------------------------------------------------------------
    # Stage 1: TTS
    # ------------------------------------------------------------------
    if "tts" in active_stages:
        _banner("Stage 1/5 — TTS Generation")
        from aido.tts_generate import run as tts_run
        tts_run(episode_id=episode_id, manifest_path=None, out_dir=str(out))
        # Reload manifest (audio_paths updated)
        with open(manifest_path, encoding="utf-8") as f:
            d = json.load(f)
        from aido.manifest_schema import EpisodeManifest
        manifest = EpisodeManifest.from_dict(d)

    # ------------------------------------------------------------------
    # Stage 2: Content Injection (USD overlays)
    # ------------------------------------------------------------------
    if "inject" in active_stages:
        _banner("Stage 2/5 — USD Content Injection")
        from aido.inject_content import run as inject_run
        master_usd = inject_run(episode_id=None, manifest_path=str(manifest_path), out_dir=str(out))
        logger.info("Master USD: %s", master_usd)

    # ------------------------------------------------------------------
    # Stage 3: Render  (Omniverse / Local B-roll / Skip)
    # ------------------------------------------------------------------
    if "render" in active_stages:
        # Backward-compat: --skip-render forces skip mode
        effective_mode = _RENDER_SKIP if skip_render else render_mode

        if effective_mode == _RENDER_LOCAL:
            _banner("Stage 3/5 — Local Render (Pexels + ffmpeg)")
            from aido.render_local import run as local_render_run
            final_mp4 = local_render_run(
                manifest_path=str(manifest_path),
                out_dir=str(out),
            )
            logger.info("Final MP4: %s", final_mp4)
            # local render produces the final MP4 directly — skip assemble stage
            if "assemble" in active_stages:
                active_stages = [s for s in active_stages if s != "assemble"]

        elif effective_mode == _RENDER_OMNIVERSE:
            _banner("Stage 3/5 — Omniverse Render (RunPod)")
            master_usd_path = str(out / "usd" / f"{episode_id}_master.usda")
            frames_dir = str(out / "frames")
            from aido.render_episode import render_headless
            rc = render_headless(master_usd=master_usd_path, out_dir=frames_dir, fps=fps)
            if rc != 0:
                logger.error("Render failed with code %d — aborting.", rc)
                sys.exit(rc)

        else:  # skip
            _banner("Stage 3/5 — Omniverse Render [SKIPPED]")
            logger.info("Skipping render — will use static background in assemble step.")

    # ------------------------------------------------------------------
    # Stage 4: FFmpeg Assembly (skipped when local render already produced final MP4)
    # ------------------------------------------------------------------
    if "assemble" in active_stages:
        _banner("Stage 4/5 — FFmpeg Assembly")
        from aido.assemble import run as assemble_run
        final_mp4 = assemble_run(
            manifest_path=str(manifest_path),
            frames_dir=str(out / "frames"),
            out_dir=str(out),
            fps=fps,
        )
        logger.info("Final MP4: %s", final_mp4)

    # ------------------------------------------------------------------
    # Stage 5: YouTube Upload
    # ------------------------------------------------------------------
    if "upload" in active_stages:
        if no_upload:
            _banner("Stage 5/5 — YouTube Upload [SKIPPED]")
            logger.info("Pass --no-upload=false to enable YouTube upload.")
        else:
            _banner("Stage 5/5 — YouTube Upload")
            from aido.upload_youtube import run as upload_run
            upload_run(
                manifest_path=str(manifest_path),
                mp4_path=None,
                privacy=privacy,
            )

    elapsed = time.time() - t0
    _banner(f"Pipeline complete — {elapsed:.0f}s")
    logger.info("Output directory: %s", out.resolve())


def main() -> None:
    p = argparse.ArgumentParser(description="AIDO full render pipeline")
    p.add_argument("--episode", default="EP001", help="Episode ID")
    p.add_argument("--out-dir", default=None, help="Output directory (default: output/<episode_id>)")
    p.add_argument("--skip-render", action="store_true", help="Skip render entirely (static dark background)")
    p.add_argument("--local-render", action="store_true", help="Use local Pexels B-roll renderer (no GPU needed)")
    p.add_argument("--no-upload", action="store_true", help="Skip YouTube upload")
    p.add_argument("--from-stage", default="tts", choices=STAGES, help="Resume from stage")
    p.add_argument("--privacy", default="private", choices=["private", "unlisted", "public"])
    p.add_argument("--fps", type=int, default=24)
    args = p.parse_args()

    if args.local_render:
        render_mode = _RENDER_LOCAL
    elif args.skip_render:
        render_mode = _RENDER_SKIP
    else:
        render_mode = _RENDER_OMNIVERSE

    out_dir = args.out_dir or f"output/{args.episode}"
    run_pipeline(
        episode_id=args.episode,
        out_dir=out_dir,
        skip_render=args.skip_render,
        no_upload=args.no_upload,
        from_stage=args.from_stage,
        privacy=args.privacy,
        fps=args.fps,
        render_mode=render_mode,
    )


if __name__ == "__main__":
    main()
