"""
AI Daily Omniverse — Newscast Assembly
Composites anchor video (side) + story graphic (main screen) into broadcast layout.

Layout:
  +------------------------------------------+
  |                                          |
  |         STORY GRAPHIC / IMAGE            |
  |              (70% width)                 |
  |                                          |
  |                              +---------+ |
  |                              | ANCHOR  | |
  |                              | (30%)   | |
  +------------------------------------------+
  |  LOWER THIRD: Story Title                |
  +------------------------------------------+

The anchor is overlaid in the bottom-right corner over the story graphic.
"""

import subprocess
import json
import os
import sys
from pathlib import Path


def composite_segment(anchor_video, story_image, title_text, output_path,
                      anchor_scale=0.35, anchor_x="W-w-30", anchor_y="H-h-80"):
    """
    Composite an anchor video over a story image background with lower third.

    anchor_video: path to the HeyGen avatar MP4
    story_image: path to the story thumbnail JPG (or None for plain background)
    title_text: text for the lower third bar
    output_path: where to save the composited MP4
    """

    if story_image and os.path.exists(story_image):
        # Story image as background, anchor overlaid bottom-right
        # 1. Scale story image to 1920x1080
        # 2. Scale anchor video down to 35%
        # 3. Overlay anchor on bottom-right
        # 4. Add lower third text bar

        filter_complex = (
            f"[1:v]scale=1920:1080[bg];"
            f"[0:v]scale=iw*{anchor_scale}:ih*{anchor_scale}[anchor];"
            f"[bg][anchor]overlay={anchor_x}:{anchor_y}[composed];"
            # Lower third dark bar
            f"[composed]drawbox=x=0:y=ih-90:w=iw:h=90:color=black@0.7:t=fill[bar];"
            # Title text
            f"[bar]drawtext=text='{title_text}':fontsize=32:fontcolor=white:x=30:y=h-70:fontfile=/Windows/Fonts/arial.ttf[out]"
        )

        cmd = [
            "ffmpeg", "-y",
            "-i", anchor_video,        # input 0: anchor video
            "-loop", "1", "-i", story_image,  # input 1: story image
            "-filter_complex", filter_complex,
            "-map", "[out]",
            "-map", "0:a",              # keep anchor audio
            "-c:v", "libx264", "-preset", "fast",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            "-pix_fmt", "yuv420p",
            output_path
        ]
    else:
        # No story image — just the anchor with lower third
        filter_complex = (
            f"drawbox=x=0:y=ih-90:w=iw:h=90:color=black@0.7:t=fill,"
            f"drawtext=text='{title_text}':fontsize=32:fontcolor=white:x=30:y=h-70:fontfile=/Windows/Fonts/arial.ttf"
        )

        cmd = [
            "ffmpeg", "-y",
            "-i", anchor_video,
            "-vf", filter_complex,
            "-c:v", "libx264", "-preset", "fast",
            "-c:a", "aac", "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            output_path
        ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"FFmpeg error: {result.stderr[-300:]}")
        return False
    return True


def assemble_episode(date_str):
    """Assemble full episode from composited segments."""
    episode_dir = Path(f"data/episodes/{date_str}")
    segments = json.loads((episode_dir / "segment-plan.json").read_text())

    composited = []

    for seg in segments:
        seg_id = seg['id']

        # Use v3 video for field reporter (female voice), v2 for anchor
        if seg['role'] == 'field' and (episode_dir / f"v3-{seg_id}-video.mp4").exists():
            anchor_video = str(episode_dir / f"v3-{seg_id}-video.mp4")
        else:
            anchor_video = str(episode_dir / f"v2-{seg_id}-video.mp4")

        if not os.path.exists(anchor_video):
            print(f"  {seg_id}: video not found, skipping")
            continue

        # Story thumbnail — use the filename from segment plan
        thumb_name = seg.get('thumbnail')
        if thumb_name and (episode_dir / thumb_name).exists():
            story_image = str(episode_dir / thumb_name)
        else:
            # Fallback to old naming convention
            story_image = str(episode_dir / f"v2-{seg_id}-thumb.jpg")
            if not os.path.exists(story_image):
                story_image = None

        # Title
        title = seg.get('title', seg_id.upper())
        # Escape special chars for FFmpeg drawtext
        title = title.replace("'", "").replace(":", " -").replace("$", "USD ")

        output = str(episode_dir / f"v3-{seg_id}-composited.mp4")

        print(f"  {seg_id}: compositing {'with graphic' if story_image else 'plain'}...")
        success = composite_segment(anchor_video, story_image, title, output)

        if success and os.path.exists(output):
            composited.append(output)
            size_mb = os.path.getsize(output) / (1024*1024)
            print(f"    saved: {size_mb:.1f} MB")
        else:
            # Fallback to raw video
            composited.append(anchor_video)
            print(f"    composite failed, using raw video")

    # Concatenate all composited segments
    concat_file = episode_dir / "v3-concat.txt"
    with open(concat_file, "w") as f:
        for path in composited:
            # Need relative paths for concat
            rel = os.path.basename(path)
            f.write(f"file '{rel}'\n")

    final = str(episode_dir / f"v3-final-episode.mp4")

    # Re-encode for consistent format (composited segments may have different encodings)
    print(f"\n  Assembling {len(composited)} segments...")

    # Build input list for FFmpeg concat with re-encode
    inputs = []
    for p in composited:
        inputs.extend(["-i", p])

    # Use filter_complex to concat with re-encode
    filter_parts = []
    for i in range(len(composited)):
        filter_parts.append(f"[{i}:v:0][{i}:a:0]")
    filter_str = "".join(filter_parts) + f"concat=n={len(composited)}:v=1:a=1[outv][outa]"

    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", filter_str,
        "-map", "[outv]", "-map", "[outa]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        final
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0 and os.path.exists(final):
        size_mb = os.path.getsize(final) / (1024*1024)
        print(f"\n  FINAL EPISODE: {final} ({size_mb:.1f} MB)")
    else:
        print(f"\n  Assembly failed: {result.stderr[-300:]}")


if __name__ == "__main__":
    date_str = sys.argv[1] if len(sys.argv) > 1 else "2026-03-24"
    print(f"=== Assembling AI Daily Omniverse — {date_str} ===\n")
    assemble_episode(date_str)
