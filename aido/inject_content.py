"""
AIDO Content Injector — USD Scene Overrides
Reads a manifest and patches the base .usda scene with episode-specific
text, timing, and camera data via USDA sublayer overrides.

This does NOT require Omniverse to be installed locally — it writes
plain-text .usda overlay files that the headless Kit render reads.

Usage:
    python -m aido.inject_content --manifest output/EP001/manifest.json
    python -m aido.inject_content --episode EP001 --out-dir output/EP001
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

logger = logging.getLogger("aido.inject")
logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")


# ---------------------------------------------------------------------------
# USD text helpers (plain USDA — no Python USD bindings required)
# ---------------------------------------------------------------------------

def _usda_string(val: str) -> str:
    """Escape a Python string for inline USDA."""
    return val.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def _write_title_card_overlay(
    out_path: Path,
    episode_id: str,
    title: str,
    subtitle: str,
) -> None:
    """Write a USDA sublayer that overrides title card text prims."""
    content = f'''\
#usda 1.0
(
    doc = "AIDO {episode_id} title card overlay — auto-generated"
    subLayers = []
)

over "World" {{
    over "TitleCard" {{
        over "EpisodeLabel" {{
            string primvars:displayText = "{_usda_string(episode_id)}"
        }}
        over "TitleText" {{
            string primvars:displayText = "{_usda_string(title)}"
        }}
        over "SubtitleText" {{
            string primvars:displayText = "{_usda_string(subtitle)}"
        }}
    }}
}}
'''
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")
    logger.info("  wrote %s", out_path.name)


def _write_segment_overlay(
    out_path: Path,
    seg_id: str,
    seg_type: str,
    title: str,
    duration: float,
    extra: dict,
) -> None:
    """Write a per-segment USDA overlay for lower-thirds and timing."""
    extras_usda = ""
    for k, v in extra.items():
        if isinstance(v, str):
            extras_usda += f'            string primvars:{k} = "{_usda_string(v)}"\n'
        elif isinstance(v, (int, float)):
            extras_usda += f'            double primvars:{k} = {v}\n'

    content = f'''\
#usda 1.0
(
    doc = "AIDO segment overlay: {seg_id}"
)

over "World" {{
    over "SegmentOverlay" {{
        string primvars:segmentId = "{_usda_string(seg_id)}"
        string primvars:segmentType = "{_usda_string(seg_type)}"
        string primvars:segmentTitle = "{_usda_string(title)}"
        double primvars:durationHint = {duration}
{extras_usda}    }}
}}
'''
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")
    logger.info("  wrote %s", out_path.name)


def _write_master_overlay(
    out_path: Path,
    base_scene: str,
    segment_overlays: list[str],
    title_card_overlay: str,
) -> None:
    """Write a master .usda that references base scene + all overlays as sublayers."""
    layers = [base_scene, title_card_overlay] + segment_overlays
    layers_str = "\n    ".join(f'@{p}@,' for p in layers)
    content = f'''\
#usda 1.0
(
    doc = "AIDO episode master — auto-generated"
    subLayers = [
    {layers_str}
    ]
)
'''
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")
    logger.info("  wrote master: %s", out_path.name)


# ---------------------------------------------------------------------------
# Main injection logic
# ---------------------------------------------------------------------------

def run(episode_id: str | None, manifest_path: str | None, out_dir: str) -> None:
    if manifest_path:
        with open(manifest_path, encoding="utf-8") as f:
            d = json.load(f)
        from aido.manifest_schema import EpisodeManifest
        manifest = EpisodeManifest.from_dict(d)
    elif episode_id:
        import aido.manifest_schema as ms
        manifest = getattr(ms, episode_id, None)
        if manifest is None:
            logger.error("Unknown episode: %s", episode_id)
            sys.exit(1)
    else:
        logger.error("Provide --episode or --manifest")
        sys.exit(1)

    out = Path(out_dir)
    usd_out = out / "usd"

    logger.info("Injecting content for %s into USD overlays", manifest.episode_id)

    # Title card
    title_overlay = usd_out / "title_card.usda"
    _write_title_card_overlay(
        title_overlay,
        manifest.episode_id,
        manifest.title,
        manifest.subtitle,
    )

    # Per-segment overlays
    seg_overlay_paths: list[str] = []
    for seg in manifest.segments:
        seg_overlay = usd_out / f"{seg.id}_overlay.usda"
        _write_segment_overlay(
            seg_overlay,
            seg.id,
            seg.type,
            seg.title,
            seg.duration_hint,
            seg.usd_overrides,
        )
        seg_overlay_paths.append(str(seg_overlay.resolve()))

    # Master scene
    master = usd_out / f"{manifest.episode_id}_master.usda"
    _write_master_overlay(
        master,
        base_scene=str(Path(manifest.scene_usd).resolve()),
        segment_overlays=seg_overlay_paths,
        title_card_overlay=str(title_overlay.resolve()),
    )

    # Update manifest with USD paths
    manifest.output_dir = str(out.resolve())
    manifest_out = out / "manifest.json"
    with open(manifest_out, "w", encoding="utf-8") as f:
        json.dump(manifest.to_dict(), f, indent=2)
    logger.info("Manifest updated: %s", manifest_out)
    logger.info("USD injection complete. Master scene: %s", master)

    return str(master)


def main() -> None:
    p = argparse.ArgumentParser(description="AIDO USD content injector")
    p.add_argument("--episode", help="Episode ID (e.g. EP001)")
    p.add_argument("--manifest", help="Path to manifest JSON")
    p.add_argument("--out-dir", default="output/EP001")
    args = p.parse_args()
    run(args.episode, args.manifest, args.out_dir)


if __name__ == "__main__":
    main()
