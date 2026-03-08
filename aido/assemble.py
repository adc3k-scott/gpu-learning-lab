"""
AIDO FFmpeg Assembly
Combines rendered frames + per-segment audio into the final episode MP4.

Pipeline per segment:
  1. Concat all segment audio → episode_audio.aac
  2. Concat all rendered frames → episode_video (image sequence)
  3. Mux audio + video → EP001_final.mp4

Requires ffmpeg on PATH.

Usage:
    python -m aido.assemble \
        --manifest output/EP001/manifest.json \
        --frames-dir output/EP001/frames \
        --out-dir output/EP001
"""

from __future__ import annotations

import argparse
import json
import logging
import shutil
import subprocess
import sys
from pathlib import Path

logger = logging.getLogger("aido.assemble")
logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")


def _require_ffmpeg() -> str:
    ff = shutil.which("ffmpeg")
    if not ff:
        logger.error("ffmpeg not found on PATH. Install it: https://ffmpeg.org/download.html")
        sys.exit(1)
    return ff


def _get_audio_duration(ffmpeg: str, audio_path: str) -> float:
    """Return duration in seconds using ffprobe."""
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        return 0.0
    result = subprocess.run(
        [
            ffprobe, "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            audio_path,
        ],
        capture_output=True, text=True,
    )
    try:
        return float(result.stdout.strip())
    except (ValueError, AttributeError):
        return 0.0


def concat_audio(ffmpeg: str, audio_files: list[str], out_path: Path) -> Path:
    """Concatenate multiple MP3/AAC files into one AAC file."""
    if not audio_files:
        logger.error("No audio files provided")
        sys.exit(1)

    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Write concat list
    list_file = out_path.parent / "audio_concat.txt"
    with open(list_file, "w", encoding="utf-8") as f:
        for af in audio_files:
            f.write(f"file '{Path(af).resolve()}'\n")

    cmd = [
        ffmpeg, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(list_file),
        "-c:a", "aac",
        "-b:a", "192k",
        str(out_path),
    ]
    logger.info("Concatenating %d audio segments...", len(audio_files))
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        logger.error("ffmpeg audio concat failed:\n%s", result.stderr[-500:])
        sys.exit(1)
    logger.info("  audio → %s", out_path)
    return out_path


def frames_to_video(
    ffmpeg: str,
    frames_dir: Path,
    audio_path: Path,
    out_path: Path,
    fps: int = 24,
    width: int = 1920,
    height: int = 1080,
) -> Path:
    """Convert image sequence + audio into final MP4."""
    out_path.parent.mkdir(parents=True, exist_ok=True)

    frames = sorted(frames_dir.glob("frame_*.png"))
    if not frames:
        logger.error("No frames found in %s", frames_dir)
        logger.error("If Omniverse render hasn't run yet, frames must be generated on RunPod first.")
        sys.exit(1)

    logger.info("Encoding %d frames @ %dfps → %s", len(frames), fps, out_path.name)

    cmd = [
        ffmpeg, "-y",
        "-framerate", str(fps),
        "-i", str(frames_dir / "frame_%06d.png"),
        "-i", str(audio_path),
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-vf", f"scale={width}:{height}",
        "-c:a", "copy",
        "-shortest",
        str(out_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        logger.error("ffmpeg encode failed:\n%s", result.stderr[-500:])
        sys.exit(1)
    logger.info("  video → %s  (%s MB)", out_path.name, out_path.stat().st_size // 1_000_000)
    return out_path


def audio_only_video(
    ffmpeg: str,
    audio_path: Path,
    out_path: Path,
    background_color: str = "0x1a1a2e",
    width: int = 1920,
    height: int = 1080,
) -> Path:
    """
    Fallback: if no frames exist, create a static-color video with the audio.
    Useful for testing the full pipeline before Omniverse is ready.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    logger.info("No frames found — creating static background video (fallback mode)")

    cmd = [
        ffmpeg, "-y",
        "-i", str(audio_path),
        "-f", "lavfi",
        "-i", f"color=c={background_color}:size={width}x{height}:rate=24",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(out_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        logger.error("ffmpeg static video failed:\n%s", result.stderr[-500:])
        sys.exit(1)
    logger.info("  fallback video → %s", out_path)
    return out_path


def run(manifest_path: str, frames_dir: str, out_dir: str, fps: int = 24) -> str:
    ffmpeg = _require_ffmpeg()

    with open(manifest_path, encoding="utf-8") as f:
        d = json.load(f)
    from aido.manifest_schema import EpisodeManifest
    manifest = EpisodeManifest.from_dict(d)

    out = Path(out_dir)

    # Collect audio files (skip segments with no audio)
    audio_files = [seg.audio_path for seg in manifest.segments if seg.audio_path and Path(seg.audio_path).exists()]
    if not audio_files:
        logger.error("No audio files found. Run tts_generate.py first.")
        sys.exit(1)

    # Step 1: concat audio
    episode_audio = out / "episode_audio.aac"
    concat_audio(ffmpeg, audio_files, episode_audio)

    # Step 2: video
    frames = Path(frames_dir)
    final_mp4 = out / f"{manifest.episode_id}_final.mp4"

    if frames.exists() and list(frames.glob("frame_*.png")):
        frames_to_video(ffmpeg, frames, episode_audio, final_mp4, fps=fps)
    else:
        audio_only_video(ffmpeg, episode_audio, final_mp4)

    # Step 3: update manifest
    manifest.final_mp4 = str(final_mp4.resolve())
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest.to_dict(), f, indent=2)

    logger.info("Assembly complete: %s", final_mp4)
    return str(final_mp4)


def main() -> None:
    p = argparse.ArgumentParser(description="AIDO FFmpeg assembly")
    p.add_argument("--manifest", required=True, help="Path to manifest.json")
    p.add_argument("--frames-dir", default="output/EP001/frames", help="Rendered frames directory")
    p.add_argument("--out-dir", default="output/EP001")
    p.add_argument("--fps", type=int, default=24)
    args = p.parse_args()
    run(args.manifest, args.frames_dir, args.out_dir, args.fps)


if __name__ == "__main__":
    main()
