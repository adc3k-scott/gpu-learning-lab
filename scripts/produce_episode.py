"""
AI Daily Omniverse — Full Episode Production Pipeline
Produces a complete news episode: script -> voice -> story images -> assembly

Usage:
  python scripts/produce_episode.py [--date 2026-03-24] [--stories 5]

Pipeline:
  1. Read daily briefing
  2. Generate anchor script from top stories
  3. ElevenLabs TTS -> anchor audio
  4. Generate story thumbnail images (FLUX Schnell)
  5. Generate lower third title cards (PIL)
  6. Assemble final video (FFmpeg): anchor segments + story images + titles + music
  7. Output: data/episodes/aido-YYYY-MM-DD-final.mp4

Requirements:
  pip install httpx pillow

Environment:
  ELEVENLABS_API_KEY — from .env
  HEYGEN_API_KEY — from HeyGen settings (for anchor video)
  RUNPOD_API_KEY — from .env (for Schnell thumbnails)
"""

import os
import sys
import json
import time
import datetime
import subprocess
import httpx

# Load env
from pathlib import Path
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
HEYGEN_API_KEY = os.environ.get("HEYGEN_API_KEY", "")
RUNPOD_API_KEY = os.environ.get("RUNPOD_API_KEY", "")

SHOW_NAME = "AI Daily Omniverse"
VOICE_ID = "XjLkpWUlnhS8i7gGz3lZ"  # David Castlemore - Newsreader
SCHNELL_ENDPOINT = "https://api.runpod.ai/v2/black-forest-labs-flux-1-schnell/runsync"

BASE_DIR = Path(__file__).parent.parent
EPISODES_DIR = BASE_DIR / "data" / "episodes"
EPISODES_DIR.mkdir(parents=True, exist_ok=True)


def read_briefing(date_str):
    """Read daily briefing markdown."""
    path = BASE_DIR / "data" / f"daily-briefing-{date_str}.md"
    if not path.exists():
        print(f"ERROR: No briefing for {date_str}. Run morning scan first.")
        return None
    return path.read_text(encoding="utf-8")


def parse_stories(briefing_text, max_stories=5):
    """Extract top stories from briefing."""
    stories = []
    current = None
    for line in briefing_text.split("\n"):
        if line.startswith("### ") and ". " in line:
            if current:
                stories.append(current)
            title = line.replace("### ", "").strip()
            if title[0].isdigit() and ". " in title:
                title = title.split(". ", 1)[1]
            current = {"title": title, "body": "", "relevance": ""}
        elif current and line.startswith("**ADC RELEVANCE:"):
            current["relevance"] = line.split("**")[2].strip().strip("-").strip()
        elif current and not line.startswith("**ACTION") and not line.startswith("**Source:"):
            if line.strip():
                current["body"] += line.strip() + " "
    if current:
        stories.append(current)
    return stories[:max_stories]


def generate_script(stories, date_str):
    """Generate newscast script."""
    date_obj = datetime.date.fromisoformat(date_str)
    date_spoken = date_obj.strftime("%A, %B %d, %Y")

    segments = []

    # Intro
    intro = (
        f"Good morning. This is {SHOW_NAME} for {date_spoken}. "
        f"I'm your host, and here are the top {len(stories)} stories "
        f"in AI infrastructure today."
    )
    segments.append({"type": "intro", "text": intro, "title": SHOW_NAME})

    # Stories
    for i, story in enumerate(stories):
        body = story["body"].strip()
        body = body.replace("**", "").replace("- ", "")
        sentences = [s.strip() for s in body.split(". ") if s.strip()]
        body = ". ".join(sentences[:4]) + "."

        if i == 0:
            text = f"Our top story. {story['title']}. {body}"
        elif i == len(stories) - 1:
            text = f"And finally. {story['title']}. {body}"
        else:
            text = f"Next. {story['title']}. {body}"

        segments.append({
            "type": "story",
            "index": i + 1,
            "text": text,
            "title": story["title"],
            "relevance": story.get("relevance", ""),
        })

    # Outro
    outro = (
        f"That's your {SHOW_NAME} briefing for {date_spoken}. "
        "Follow us for daily updates on AI infrastructure, energy, and technology. "
        "Visit louisiana ai dot net for more. "
        "This has been Ground Zero. See you tomorrow."
    )
    segments.append({"type": "outro", "text": outro, "title": "Ground Zero"})

    return segments


def generate_tts(text, output_path):
    """Generate speech audio via ElevenLabs."""
    if not ELEVENLABS_API_KEY:
        print("  WARNING: No ElevenLabs API key")
        return None

    resp = httpx.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
        headers={
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json",
        },
        json={
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.45,
                "similarity_boost": 0.75,
                "style": 0.35,
                "use_speaker_boost": True,
            },
        },
        timeout=120,
    )

    if resp.status_code == 200:
        Path(output_path).write_bytes(resp.content)
        return output_path
    else:
        print(f"  TTS error: {resp.status_code}")
        return None


def generate_thumbnail(prompt, output_path):
    """Generate story thumbnail via FLUX Schnell."""
    if not RUNPOD_API_KEY:
        print("  WARNING: No RunPod API key for thumbnails")
        return None

    resp = httpx.post(
        SCHNELL_ENDPOINT,
        headers={"Authorization": f"Bearer {RUNPOD_API_KEY}"},
        json={"input": {"prompt": prompt, "width": 1920, "height": 1080, "num_outputs": 1}},
        timeout=120,
    )

    if resp.status_code == 200:
        data = resp.json()
        image_url = None
        output = data.get("output", {})
        if isinstance(output, dict):
            image_url = output.get("image_url") or output.get("images", [None])[0]
        elif isinstance(output, list) and output:
            image_url = output[0].get("image") if isinstance(output[0], dict) else output[0]

        if image_url:
            img_resp = httpx.get(image_url, timeout=30)
            if img_resp.status_code == 200:
                Path(output_path).write_bytes(img_resp.content)
                return output_path

    print(f"  Thumbnail generation failed")
    return None


def generate_title_card(title, subtitle, output_path, width=1920, height=1080):
    """Generate a lower-third title card image."""
    try:
        from PIL import Image, ImageDraw, ImageFont

        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Lower third bar
        bar_y = height - 200
        draw.rectangle([(0, bar_y), (width, bar_y + 80)], fill=(10, 10, 30, 220))
        draw.rectangle([(0, bar_y + 80), (width, bar_y + 120)], fill=(59, 130, 246, 200))

        # Text
        try:
            font_title = ImageFont.truetype("arial.ttf", 36)
            font_sub = ImageFont.truetype("arial.ttf", 24)
        except:
            font_title = ImageFont.load_default()
            font_sub = ImageFont.load_default()

        draw.text((40, bar_y + 18), title, fill=(255, 255, 255), font=font_title)
        draw.text((40, bar_y + 85), subtitle, fill=(255, 255, 255), font=font_sub)

        # Show logo area
        draw.text((width - 300, bar_y + 18), SHOW_NAME, fill=(59, 130, 246), font=font_sub)

        img.save(output_path)
        return output_path
    except Exception as e:
        print(f"  Title card error: {e}")
        return None


def assemble_video(date_str, segments, episode_dir):
    """Assemble final video using FFmpeg."""
    # Check for FFmpeg
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("WARNING: FFmpeg not found. Skipping video assembly.")
        print("Install FFmpeg and re-run, or assemble manually.")
        return None

    # Build concat file
    concat_entries = []
    for seg in segments:
        audio_path = episode_dir / f"seg-{seg.get('index', seg['type'])}-audio.mp3"
        thumb_path = episode_dir / f"seg-{seg.get('index', seg['type'])}-thumb.jpg"

        if not audio_path.exists():
            continue

        # Get audio duration
        probe = subprocess.run(
            ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)],
            capture_output=True, text=True
        )
        try:
            duration = float(probe.stdout.strip())
        except:
            duration = 10.0

        # Create video from image + audio
        seg_video = episode_dir / f"seg-{seg.get('index', seg['type'])}-video.mp4"

        if thumb_path.exists():
            img_input = str(thumb_path)
        else:
            # Create solid color frame
            img_input = f"color=c=0x0a0a1a:s=1920x1080:d={duration}"

        subprocess.run([
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(thumb_path) if thumb_path.exists() else "color=black",
            "-i", str(audio_path),
            "-c:v", "libx264", "-tune", "stillimage",
            "-c:a", "aac", "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-shortest",
            str(seg_video)
        ], capture_output=True)

        if seg_video.exists():
            concat_entries.append(f"file '{seg_video}'")

    if not concat_entries:
        print("No segments to assemble")
        return None

    # Write concat file
    concat_file = episode_dir / "concat.txt"
    concat_file.write_text("\n".join(concat_entries))

    # Concatenate
    output = episode_dir / f"aido-{date_str}-final.mp4"
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
        "-c", "copy",
        str(output)
    ], capture_output=True)

    if output.exists():
        size_mb = output.stat().st_size / (1024 * 1024)
        print(f"Final video: {output} ({size_mb:.1f} MB)")
        return output
    return None


def produce_episode(date_str=None, max_stories=5):
    """Full production pipeline."""
    if not date_str:
        date_str = datetime.date.today().isoformat()

    episode_dir = EPISODES_DIR / date_str
    episode_dir.mkdir(exist_ok=True)

    print(f"{'='*60}")
    print(f"  {SHOW_NAME} — Episode Production")
    print(f"  Date: {date_str}")
    print(f"{'='*60}")
    print()

    # Step 1: Read briefing
    print("STEP 1: Reading daily briefing...")
    briefing = read_briefing(date_str)
    if not briefing:
        return

    # Step 2: Parse stories
    print("STEP 2: Parsing top stories...")
    stories = parse_stories(briefing, max_stories)
    print(f"  Found {len(stories)} stories")
    for s in stories:
        print(f"    - {s['title'][:60]}")

    # Step 3: Generate script segments
    print("STEP 3: Generating script segments...")
    segments = generate_script(stories, date_str)
    print(f"  Generated {len(segments)} segments")

    # Save full script
    full_script = "\n\n".join(seg["text"] for seg in segments)
    script_path = episode_dir / "script.txt"
    script_path.write_text(full_script)
    print(f"  Script: {len(full_script)} chars, ~{len(full_script.split())} words")

    # Step 4: Generate TTS for each segment
    print("STEP 4: Generating TTS audio segments...")
    for seg in segments:
        seg_id = seg.get("index", seg["type"])
        audio_path = episode_dir / f"seg-{seg_id}-audio.mp3"
        print(f"  Segment {seg_id}: {seg['title'][:40]}...")
        result = generate_tts(seg["text"], str(audio_path))
        if result:
            size_kb = audio_path.stat().st_size / 1024
            print(f"    Audio: {size_kb:.0f} KB")
        seg["audio_path"] = str(audio_path) if result else None

    # Step 5: Generate story thumbnails
    print("STEP 5: Generating story thumbnails...")
    thumbnail_prompts = {
        "LaGuardia": "Airport runway at night with emergency lights and fire truck, dramatic news photo style",
        "Jensen": "NVIDIA CEO on stage at technology conference, green lighting, keynote presentation",
        "Hut 8": "Large industrial construction site in Louisiana, aerial view, AI data center being built",
        "Louisiana": "Louisiana state map with technology overlay showing data center locations, modern infographic",
        "Skydio": "Military drone flying over a field, small tactical quadcopter, US Army, professional photography",
    }

    for seg in segments:
        if seg["type"] != "story":
            continue
        seg_id = seg["index"]
        thumb_path = episode_dir / f"seg-{seg_id}-thumb.jpg"

        # Find matching prompt
        prompt = "Professional news broadcast background with blue and dark tones"
        for key, p in thumbnail_prompts.items():
            if key.lower() in seg["title"].lower():
                prompt = p
                break

        print(f"  Story {seg_id}: generating thumbnail...")
        try:
            generate_thumbnail(prompt, str(thumb_path))
        except Exception as e:
            print(f"    Thumbnail skipped: {e}")

    # Step 6: Generate title cards
    print("STEP 6: Generating title cards...")
    for seg in segments:
        seg_id = seg.get("index", seg["type"])
        title_path = episode_dir / f"seg-{seg_id}-title.png"
        subtitle = f"{SHOW_NAME} — {date_str}"
        if seg["type"] == "story":
            subtitle = f"Story {seg['index']} of {len(stories)}"
        generate_title_card(seg["title"][:80], subtitle, str(title_path))

    # Step 7: Generate combined audio (all segments)
    print("STEP 7: Generating combined audio...")
    combined_audio = episode_dir / f"aido-{date_str}-full-audio.mp3"
    generate_tts(full_script, str(combined_audio))
    if combined_audio.exists():
        size_kb = combined_audio.stat().st_size / 1024
        print(f"  Combined audio: {size_kb:.0f} KB")

    # Step 8: Assemble video
    print("STEP 8: Assembling video...")
    final = assemble_video(date_str, segments, episode_dir)

    # Summary
    print()
    print(f"{'='*60}")
    print(f"  PRODUCTION COMPLETE")
    print(f"{'='*60}")
    print(f"  Episode dir: {episode_dir}")
    print(f"  Script: {script_path}")
    print(f"  Audio: {combined_audio}")
    if final:
        print(f"  Video: {final}")
    else:
        print(f"  Video: Pending HeyGen anchor + FFmpeg assembly")
    print()
    print(f"  Next steps:")
    print(f"  1. Upload audio to HeyGen -> get anchor video")
    print(f"  2. FFmpeg combine anchor video + story thumbnails")
    print(f"  3. Upload to YouTube @ScottTomsu")
    print(f"{'='*60}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=f"{SHOW_NAME} Episode Producer")
    parser.add_argument("--date", default=datetime.date.today().isoformat())
    parser.add_argument("--stories", type=int, default=5)
    args = parser.parse_args()
    produce_episode(args.date, args.stories)
