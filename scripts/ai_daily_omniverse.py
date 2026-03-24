"""
AI Daily Omniverse — Automated News Show Pipeline
Produces a daily AI news video with AI anchor at a news desk.

Pipeline:
1. Read daily briefing (data/daily-briefing-YYYY-MM-DD.md)
2. Generate news script from top stories
3. ElevenLabs TTS → audio file
4. HeyGen API → AI anchor video with audio
5. Download finished video
6. (Future) FFmpeg post-processing + YouTube upload

Requirements:
  pip install httpx elevenlabs

Environment variables:
  HEYGEN_API_KEY — from heygen.com API settings
  ELEVENLABS_API_KEY — from elevenlabs.io
  ELEVENLABS_VOICE_ID — newscast voice ID
"""

import os
import json
import time
import datetime
import httpx

# Config
HEYGEN_API_KEY = os.environ.get("HEYGEN_API_KEY", "")
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID", "")

SHOW_NAME = "AI Daily Omniverse"
ANCHOR_NAME = "Ground Zero News"


def read_daily_briefing(date_str=None):
    """Read today's briefing file."""
    if not date_str:
        date_str = datetime.date.today().isoformat()
    path = os.path.join(os.path.dirname(__file__), "..", "data", f"daily-briefing-{date_str}.md")
    if not os.path.exists(path):
        print(f"No briefing found for {date_str}")
        return None
    with open(path, "r") as f:
        return f.read()


def generate_news_script(briefing_text, num_stories=5):
    """Generate a news anchor script from the briefing.

    This produces a script that sounds like a real news anchor —
    not a robot reading bullet points.
    """
    # Parse stories from briefing
    stories = []
    current_story = None
    for line in briefing_text.split("\n"):
        if line.startswith("### ") and ". " in line:
            if current_story:
                stories.append(current_story)
            title = line.replace("### ", "").strip()
            # Remove number prefix
            if title[0].isdigit() and ". " in title:
                title = title.split(". ", 1)[1]
            current_story = {"title": title, "body": ""}
        elif current_story and line.startswith("**Source:**"):
            pass  # skip source lines
        elif current_story and not line.startswith("**ADC RELEVANCE") and not line.startswith("**ACTION"):
            current_story["body"] += line + " "
    if current_story:
        stories.append(current_story)

    # Take top N stories
    stories = stories[:num_stories]

    # Build script
    date_spoken = datetime.date.today().strftime("%A, %B %d, %Y")

    script = f"Good morning. This is {SHOW_NAME} for {date_spoken}. "
    script += f"I'm your host, and here are the top {len(stories)} stories in AI infrastructure today. "
    script += "\n\n"

    for i, story in enumerate(stories):
        body = story["body"].strip()
        # Clean up markdown artifacts
        body = body.replace("**", "").replace("- ", "").replace("  ", " ")
        # Trim to reasonable length for voice
        sentences = body.split(". ")
        body = ". ".join(sentences[:4]) + "."

        if i == 0:
            script += f"Our top story: {story['title']}. {body} "
        elif i == len(stories) - 1:
            script += f"And finally: {story['title']}. {body} "
        else:
            script += f"Next: {story['title']}. {body} "
        script += "\n\n"

    script += f"That's your {SHOW_NAME} briefing for {date_spoken}. "
    script += "Follow us for daily updates on AI infrastructure, energy, and technology. "
    script += "Visit louisiana ai dot net for more information. "
    script += "This has been Ground Zero. See you tomorrow."

    return script


def generate_tts(script, output_path):
    """Generate speech audio via ElevenLabs API."""
    if not ELEVENLABS_API_KEY:
        print("WARNING: No ElevenLabs API key. Saving script as text only.")
        with open(output_path.replace(".mp3", ".txt"), "w") as f:
            f.write(script)
        return None

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
    }
    data = {
        "text": script,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.32,
            "similarity_boost": 0.75,
            "style": 0.55,
            "use_speaker_boost": True,
        },
    }

    resp = httpx.post(url, json=data, headers=headers, timeout=120)
    if resp.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(resp.content)
        print(f"TTS audio saved: {output_path} ({len(resp.content):,} bytes)")
        return output_path
    else:
        print(f"TTS error: {resp.status_code} {resp.text[:200]}")
        return None


def generate_video(audio_path, output_dir):
    """Generate AI anchor video via HeyGen API."""
    if not HEYGEN_API_KEY:
        print("WARNING: No HeyGen API key. Skipping video generation.")
        return None

    # Step 1: Upload audio to HeyGen
    print("Uploading audio to HeyGen...")
    with open(audio_path, "rb") as f:
        upload_resp = httpx.post(
            "https://api.heygen.com/v1/asset",
            headers={"X-Api-Key": HEYGEN_API_KEY},
            files={"file": ("narration.mp3", f, "audio/mpeg")},
            timeout=60,
        )

    if upload_resp.status_code != 200:
        print(f"Upload error: {upload_resp.status_code} {upload_resp.text[:200]}")
        return None

    asset_id = upload_resp.json().get("data", {}).get("asset_id")
    print(f"Audio uploaded: {asset_id}")

    # Step 2: Create video with avatar
    print("Creating video...")
    video_data = {
        "video_inputs": [
            {
                "character": {
                    "type": "avatar",
                    "avatar_id": "default",  # Will need to be updated with custom avatar
                    "avatar_style": "normal",
                },
                "voice": {
                    "type": "audio",
                    "audio_asset_id": asset_id,
                },
                "background": {
                    "type": "color",
                    "value": "#0a0a1a",  # Dark news desk background
                },
            }
        ],
        "dimension": {"width": 1920, "height": 1080},
    }

    create_resp = httpx.post(
        "https://api.heygen.com/v2/video/generate",
        headers={
            "X-Api-Key": HEYGEN_API_KEY,
            "Content-Type": "application/json",
        },
        json=video_data,
        timeout=60,
    )

    if create_resp.status_code != 200:
        print(f"Video create error: {create_resp.status_code} {create_resp.text[:200]}")
        return None

    video_id = create_resp.json().get("data", {}).get("video_id")
    print(f"Video generating: {video_id}")

    # Step 3: Poll for completion
    for i in range(60):  # 10 minutes max
        time.sleep(10)
        status_resp = httpx.get(
            f"https://api.heygen.com/v1/video_status.get?video_id={video_id}",
            headers={"X-Api-Key": HEYGEN_API_KEY},
            timeout=30,
        )
        status = status_resp.json().get("data", {}).get("status")
        print(f"  Status: {status} ({(i+1)*10}s)")

        if status == "completed":
            video_url = status_resp.json()["data"]["video_url"]
            # Download
            date_str = datetime.date.today().isoformat()
            output_path = os.path.join(output_dir, f"aido-{date_str}.mp4")
            video_data = httpx.get(video_url, timeout=120)
            with open(output_path, "wb") as f:
                f.write(video_data.content)
            print(f"Video saved: {output_path} ({len(video_data.content):,} bytes)")
            return output_path
        elif status == "failed":
            error = status_resp.json().get("data", {}).get("error")
            print(f"Video failed: {error}")
            return None

    print("Video generation timed out")
    return None


if __name__ == "__main__":
    today = datetime.date.today().isoformat()
    output_dir = os.path.join(os.path.dirname(__file__), "..", "data", "episodes")
    os.makedirs(output_dir, exist_ok=True)

    print(f"=== {SHOW_NAME} — {today} ===")
    print()

    # Step 1: Read briefing
    print("Step 1: Reading daily briefing...")
    briefing = read_daily_briefing()
    if not briefing:
        print("No briefing available. Run the morning scan first.")
        exit(1)

    # Step 2: Generate script
    print("Step 2: Generating news script...")
    script = generate_news_script(briefing)
    script_path = os.path.join(output_dir, f"aido-{today}-script.txt")
    with open(script_path, "w") as f:
        f.write(script)
    print(f"Script saved: {script_path}")
    print(f"Script length: {len(script)} chars (~{len(script.split())} words)")
    print()
    print("--- SCRIPT PREVIEW ---")
    print(script[:500])
    print("--- END PREVIEW ---")
    print()

    # Step 3: Generate TTS
    print("Step 3: Generating TTS audio...")
    audio_path = os.path.join(output_dir, f"aido-{today}-audio.mp3")
    audio = generate_tts(script, audio_path)

    # Step 4: Generate video
    if audio:
        print("Step 4: Generating AI anchor video...")
        video = generate_video(audio_path, output_dir)
        if video:
            print(f"\n=== EPISODE COMPLETE: {video} ===")
        else:
            print("\nVideo generation skipped or failed. Audio + script are ready for manual production.")
    else:
        print("\nTTS skipped (no API key). Script saved for manual recording.")

    print(f"\nAll outputs in: {output_dir}/")
