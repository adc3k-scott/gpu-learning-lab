"""
AIDO Local Renderer — Pexels B-roll + ffmpeg news template

Produces a broadcast-style news video without GPU/Omniverse.
For each segment: downloads a Pexels stock video clip matching the topic,
overlays Ground Zero lower-third branding, syncs to the segment audio.
All clips are then concatenated into the final episode MP4.

Usage:
    python -m aido.render_local --manifest output/EP001/manifest.json --out-dir output/EP001

Requires:
    PEXELS_API_KEY in .env  (free: https://www.pexels.com/api/)
    ffmpeg on PATH (or WinGet installed)
"""

from __future__ import annotations

import glob
import json
import logging
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import httpx
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("aido.render_local")
logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")

_PEXELS_VIDEO_SEARCH = "https://api.pexels.com/videos/search"
_BRAND_COLOR = "0xFF2020"          # Ground Zero red
_BAR_COLOR = "black@0.85"
_BAR_HEIGHT = 90                   # news lower-third height (px)
_WIDTH = 1920
_HEIGHT = 1080

# Fallback keywords if b_roll_tags is empty for a segment type
_TYPE_KEYWORDS = {
    "cold_open": "technology city night",
    "ai_headline": "artificial intelligence computer",
    "tech_breakthrough": "server room data center",
    "global_map": "world globe satellite",
    "infrastructure_watch": "industrial network sensors",
    "future_watch": "robot automation future",
}


def _require_ffmpeg() -> str:
    ff = shutil.which("ffmpeg")
    if not ff:
        patterns = [
            r"C:\Users\*\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg*\ffmpeg-*\bin\ffmpeg.exe",
            r"C:\ProgramData\chocolatey\bin\ffmpeg.exe",
            r"C:\ffmpeg\bin\ffmpeg.exe",
        ]
        for pattern in patterns:
            matches = glob.glob(pattern, recursive=False)
            if matches:
                ff = matches[0]
                logger.info("Found ffmpeg at: %s", ff)
                break
    if not ff:
        logger.error("ffmpeg not found. Install it: https://ffmpeg.org/download.html")
        sys.exit(1)
    return ff


def _require_ffprobe() -> str | None:
    fp = shutil.which("ffprobe")
    if not fp:
        # Try same directory as ffmpeg
        ff = shutil.which("ffmpeg")
        if ff:
            fp_candidate = str(Path(ff).parent / "ffprobe.exe")
            if Path(fp_candidate).exists():
                return fp_candidate
        # WinGet
        patterns = [
            r"C:\Users\*\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg*\ffmpeg-*\bin\ffprobe.exe",
        ]
        for pattern in patterns:
            matches = glob.glob(pattern, recursive=False)
            if matches:
                return matches[0]
    return fp


def _get_audio_duration(ffprobe: str, audio_path: str) -> float:
    result = subprocess.run(
        [ffprobe, "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", audio_path],
        capture_output=True, text=True,
    )
    try:
        return float(result.stdout.strip())
    except (ValueError, AttributeError):
        return 30.0


def _search_pexels_video(query: str, api_key: str) -> str | None:
    """Search Pexels for a video clip. Returns the best MP4 download URL or None."""
    try:
        with httpx.Client(timeout=15.0) as client:
            resp = client.get(
                _PEXELS_VIDEO_SEARCH,
                headers={"Authorization": api_key},
                params={"query": query, "per_page": 5, "size": "medium", "orientation": "landscape"},
            )
        if resp.status_code != 200:
            logger.warning("  Pexels search failed (%d) for: %s", resp.status_code, query)
            return None
        videos = resp.json().get("videos", [])
        if not videos:
            logger.warning("  No Pexels results for: %s", query)
            return None
        # Pick first video, prefer HD (1280+) MP4
        for video in videos:
            files = video.get("video_files", [])
            # Sort by width descending, pick best that's ≤ 1920
            mp4_files = [f for f in files if f.get("file_type") == "video/mp4" and f.get("width", 0) >= 1280]
            if not mp4_files:
                mp4_files = [f for f in files if f.get("file_type") == "video/mp4"]
            if mp4_files:
                mp4_files.sort(key=lambda x: x.get("width", 0), reverse=True)
                return mp4_files[0]["link"]
        return None
    except Exception as e:
        logger.warning("  Pexels search error: %s", e)
        return None


def _download_clip(url: str, out_path: Path) -> bool:
    """Download a video clip from URL to out_path. Returns True on success."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with httpx.Client(timeout=60.0, follow_redirects=True) as client:
            with client.stream("GET", url) as resp:
                resp.raise_for_status()
                with open(out_path, "wb") as f:
                    for chunk in resp.iter_bytes(chunk_size=65536):
                        f.write(chunk)
        logger.info("  downloaded %s (%.1f MB)", out_path.name, out_path.stat().st_size / 1e6)
        return True
    except Exception as e:
        logger.warning("  clip download failed: %s", e)
        return False


def _stage_fonts(out_dir: Path) -> dict[str, str]:
    """
    Copy Windows system fonts to out_dir/fonts/ and return name → relative path map.
    Relative paths have no drive letter colon, so ffmpeg filter_complex can use them safely.
    """
    font_dir = Path("C:/Windows/Fonts")
    fonts_out = out_dir / "fonts"
    fonts_out.mkdir(parents=True, exist_ok=True)
    wanted = {
        "bold": ["ariblk.ttf", "arialbd.ttf"],
        "regular": ["arial.ttf", "Arial.ttf"],
    }
    result: dict[str, str] = {}
    for key, candidates in wanted.items():
        for name in candidates:
            src = font_dir / name
            if src.exists():
                dst = fonts_out / name
                if not dst.exists():
                    shutil.copy2(src, dst)
                # Return as forward-slash relative path from cwd (no colon)
                result[key] = str(dst).replace("\\", "/")
                break
    return result  # keys: "bold", "regular"


def _render_segment_clip(
    ffmpeg: str,
    clip_path: Path | None,
    audio_path: Path,
    out_path: Path,
    title: str,
    segment_type: str,
    duration: float,
    date_str: str,
    fonts: dict[str, str] | None = None,
) -> bool:
    """
    Render one segment: background clip (or color fallback) + news lower third + audio.
    Returns True on success.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fonts = fonts or {}
    font_bold = fonts.get("bold", "")
    font_reg = fonts.get("regular", "")

    # Escape title for ffmpeg drawtext (colons and special chars need escaping)
    def esc(s: str) -> str:
        return s.replace("'", "\\'").replace(":", "\\:").replace(",", "\\,")

    title_esc = esc(title)
    brand_esc = esc("GROUND ZERO")
    sub_esc = esc("AI DAILY")
    date_esc = esc(date_str)

    bar_y = _HEIGHT - _BAR_HEIGHT

    # Build drawtext filter args — use font paths if available
    def dt(text: str, fontfile: str, color: str, size: int, x: str, y: str, extra: str = "") -> str:
        ff = f":fontfile={fontfile}" if fontfile else ""
        return f"drawtext=text='{text}'{ff}:fontcolor={color}:fontsize={size}:x={x}:y={y}{(':' + extra) if extra else ''}"

    # Layout: bar_y = bottom 90px
    # Two rows: brand/title on row1, sub-label/date on row2
    # All fonts at ~50% of previous size to prevent overlap
    row1_y = bar_y + 12
    row2_y = bar_y + 56

    filters = [
        f"scale={_WIDTH}:{_HEIGHT}:force_original_aspect_ratio=decrease",
        f"pad={_WIDTH}:{_HEIGHT}:(ow-iw)/2:(oh-ih)/2:color=black",
        # dark bar
        f"drawbox=x=0:y={bar_y}:w=iw:h={_BAR_HEIGHT}:color={_BAR_COLOR}:t=fill",
        # red accent line above bar (3px)
        f"drawbox=x=0:y={bar_y}:w=iw:h=3:color=0xFF2020:t=fill",
        # GROUND ZERO brand — 50% smaller (22 → 11)
        dt(brand_esc, font_bold, "0xFF2020", 11, "24", str(row1_y)),
        # AI DAILY sub-label — 50% smaller (14 → 9 min readable)
        dt(sub_esc, font_reg, "white@0.55", 9, "24", str(row2_y)),
        # vertical divider — moved inward to match smaller brand width
        f"drawbox=x=110:y={bar_y + 8}:w=2:h={_BAR_HEIGHT - 16}:color=white@0.20:t=fill",
        # segment title — 50% smaller (28 → 14), starts after divider
        dt(title_esc, font_bold, "white", 14, "122", str(row1_y)),
        # date bottom right — 50% smaller (14 → 9)
        dt(date_esc, font_reg, "white@0.45", 9, f"{_WIDTH - 160}", str(row2_y)),
    ]
    vf = ",".join(filters)

    if clip_path and clip_path.exists():
        cmd = [
            ffmpeg, "-y",
            "-stream_loop", "-1",       # loop clip if shorter than audio
            "-i", str(clip_path),
            "-i", str(audio_path),
            "-filter_complex", f"[0:v]{vf}[vout]",
            "-map", "[vout]",
            "-map", "1:a",
            "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            "-t", str(duration),
            str(out_path),
        ]
    else:
        # Dark background with subtle temporal noise — renders fast, gives texture/motion
        # noise allf=t means noise pattern changes each frame (temporal motion)
        logger.info("  using dark noise background (no Pexels key)")
        cmd = [
            ffmpeg, "-y",
            "-f", "lavfi",
            "-i", f"color=c=0x080810:size={_WIDTH}x{_HEIGHT}:rate=24",
            "-i", str(audio_path),
            "-filter_complex", f"[0:v]noise=c0s=18:c0f=t,{vf}[v]",
            "-map", "[v]",
            "-map", "1:a",
            "-c:v", "libx264", "-preset", "fast", "-crf", "22", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            "-t", str(duration),
            str(out_path),
        ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        logger.error("  ffmpeg segment render failed:\n%s", result.stderr[-600:])
        return False
    return True


def _concat_clips(ffmpeg: str, clip_paths: list[Path], out_path: Path) -> bool:
    """Concatenate rendered segment MP4s into the final episode MP4."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    list_file = out_path.parent / "clips_concat.txt"
    with open(list_file, "w", encoding="utf-8") as f:
        for cp in clip_paths:
            f.write(f"file '{cp.resolve()}'\n")
    cmd = [
        ffmpeg, "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(list_file),
        "-c", "copy",
        str(out_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        logger.error("ffmpeg concat failed:\n%s", result.stderr[-600:])
        return False
    logger.info("  final → %s  (%.1f MB)", out_path.name, out_path.stat().st_size / 1e6)
    return True


def run(manifest_path: str, out_dir: str) -> str:
    """
    Main entry: render all segments, concat into final MP4.
    Returns path to final MP4.
    """
    ffmpeg = _require_ffmpeg()
    ffprobe = _require_ffprobe()
    pexels_key = os.environ.get("PEXELS_API_KEY", "")
    if not pexels_key:
        logger.warning("PEXELS_API_KEY not set — using color background fallback for all segments")

    with open(manifest_path, encoding="utf-8") as f:
        d = json.load(f)
    from aido.manifest_schema import EpisodeManifest
    manifest = EpisodeManifest.from_dict(d)

    out = Path(out_dir)
    clips_dir = out / "clips"
    clips_dir.mkdir(parents=True, exist_ok=True)
    raw_dir = out / "clips" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    # Stage fonts to local directory (avoids Windows drive-letter colon in ffmpeg filter paths)
    fonts = _stage_fonts(out)
    if fonts:
        logger.info("Staged fonts: %s", list(fonts.keys()))
    else:
        logger.info("No system fonts found — using ffmpeg default font")

    # Date string for lower third
    from datetime import datetime
    date_str = datetime.now().strftime("%B %d, %Y").upper()

    rendered_clips: list[Path] = []

    for i, seg in enumerate(manifest.segments, 1):
        logger.info("[%d/%d] Rendering segment: %s", i, len(manifest.segments), seg.id)

        audio_path = Path(seg.audio_path) if seg.audio_path else None
        if not audio_path or not audio_path.exists():
            logger.error("  Audio not found for %s — run TTS first", seg.id)
            sys.exit(1)

        # Get audio duration
        duration = seg.duration_hint
        if ffprobe:
            duration = _get_audio_duration(ffprobe, str(audio_path))
            logger.info("  audio duration: %.1fs", duration)

        # Search and download Pexels clip
        clip_path: Path | None = None
        if pexels_key:
            # Use first b_roll_tag or fall back to type keyword
            tags = seg.b_roll_tags if seg.b_roll_tags else []
            query = tags[0] if tags else _TYPE_KEYWORDS.get(seg.type, "technology")
            logger.info("  searching Pexels: %s", query)
            video_url = _search_pexels_video(query, pexels_key)
            if video_url:
                raw_clip = raw_dir / f"{seg.id}_raw.mp4"
                if raw_clip.exists():
                    logger.info("  clip already cached: %s", raw_clip.name)
                    clip_path = raw_clip
                else:
                    if _download_clip(video_url, raw_clip):
                        clip_path = raw_clip
            time.sleep(0.5)  # polite gap for Pexels API

        # Render segment clip
        out_clip = clips_dir / f"{seg.id}.mp4"
        success = _render_segment_clip(
            ffmpeg=ffmpeg,
            clip_path=clip_path,
            audio_path=audio_path,
            out_path=out_clip,
            title=seg.title,
            segment_type=seg.type,
            duration=duration,
            date_str=date_str,
            fonts=fonts,
        )
        if not success:
            logger.error("  Segment render failed: %s", seg.id)
            sys.exit(1)

        logger.info("  segment done → %s", out_clip.name)
        rendered_clips.append(out_clip)

    # Concatenate all segments
    final_mp4 = out / f"{manifest.episode_id}_final.mp4"
    logger.info("Concatenating %d segments into final MP4...", len(rendered_clips))
    if not _concat_clips(ffmpeg, rendered_clips, final_mp4):
        sys.exit(1)

    # Update manifest
    manifest.final_mp4 = str(final_mp4.resolve())
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest.to_dict(), f, indent=2)

    logger.info("Local render complete: %s", final_mp4)
    return str(final_mp4)


def main() -> None:
    import argparse
    p = argparse.ArgumentParser(description="AIDO local renderer (Pexels + ffmpeg)")
    p.add_argument("--manifest", required=True, help="Path to manifest.json")
    p.add_argument("--out-dir", default="output/EP001")
    args = p.parse_args()
    run(args.manifest, args.out_dir)


if __name__ == "__main__":
    main()
