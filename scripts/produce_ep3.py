"""
AI Daily Omniverse — Episode 3 Production (2026-03-26)
Generates TTS audio + HeyGen avatar videos from segment-plan.json.
Real source photos already downloaded — no AI image generation.
"""

import os
import sys
import json
import time
import httpx
from pathlib import Path

# Load env
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
HEYGEN_API_KEY = os.environ.get("HEYGEN_API_KEY", "")

# Voice IDs
ARMANDO_VOICE = "XjLkpWUlnhS8i7gGz3lZ"  # David Castlemore - Newsreader (male)
ADRIANA_VOICE = "EXAVITQu4vr4xnSDxMaL"  # Sarah - Mature Reassuring Confident (female)

EPISODE_DIR = Path(__file__).parent.parent / "data" / "episodes" / "2026-03-26"


def generate_tts(text, output_path, voice_id):
    """Generate speech audio via ElevenLabs."""
    if not ELEVENLABS_API_KEY:
        print(f"  WARNING: No ElevenLabs API key — skipping {output_path}")
        return None

    resp = httpx.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
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
        size_kb = len(resp.content) / 1024
        print(f"  Audio saved: {Path(output_path).name} ({size_kb:.0f} KB)")
        return output_path
    else:
        print(f"  TTS error {resp.status_code}: {resp.text[:200]}")
        return None


def upload_audio_heygen(audio_path):
    """Upload audio to HeyGen (raw binary, NOT multipart)."""
    if not HEYGEN_API_KEY:
        return None

    audio_data = Path(audio_path).read_bytes()
    resp = httpx.post(
        "https://upload.heygen.com/v1/asset",
        headers={
            "X-Api-Key": HEYGEN_API_KEY,
            "Content-Type": "audio/mpeg",
        },
        content=audio_data,
        timeout=60,
    )

    if resp.status_code == 200:
        data = resp.json()
        # HeyGen returns id in data dict
        asset_id = data.get("data", {}).get("id") or data.get("data", {}).get("asset_id") or data.get("asset_id")
        print(f"  Audio uploaded: {asset_id}")
        return asset_id
    else:
        print(f"  Upload error {resp.status_code}: {resp.text[:200]}")
        return None


def create_heygen_video(avatar_id, audio_asset_id):
    """Create HeyGen video with avatar + uploaded audio."""
    if not HEYGEN_API_KEY:
        return None

    video_data = {
        "video_inputs": [
            {
                "character": {
                    "type": "avatar",
                    "avatar_id": avatar_id,
                    "avatar_style": "normal",
                },
                "voice": {
                    "type": "audio",
                    "audio_asset_id": audio_asset_id,
                },
                "background": {
                    "type": "color",
                    "value": "#0a0a1a",
                },
            }
        ],
        "dimension": {"width": 1920, "height": 1080},
    }

    resp = httpx.post(
        "https://api.heygen.com/v2/video/generate",
        headers={
            "X-Api-Key": HEYGEN_API_KEY,
            "Content-Type": "application/json",
        },
        json=video_data,
        timeout=60,
    )

    if resp.status_code == 200:
        video_id = resp.json().get("data", {}).get("video_id")
        print(f"  Video generating: {video_id}")
        return video_id
    else:
        print(f"  Video create error {resp.status_code}: {resp.text[:300]}")
        return None


def poll_heygen_video(video_id, output_path, max_wait=600):
    """Poll HeyGen for video completion and download."""
    if not HEYGEN_API_KEY or not video_id:
        return None

    for i in range(max_wait // 10):
        time.sleep(10)
        resp = httpx.get(
            f"https://api.heygen.com/v1/video_status.get?video_id={video_id}",
            headers={"X-Api-Key": HEYGEN_API_KEY},
            timeout=30,
        )
        data = resp.json().get("data", {})
        status = data.get("status")
        print(f"    Status: {status} ({(i+1)*10}s)")

        if status == "completed":
            video_url = data.get("video_url")
            if video_url:
                vid_resp = httpx.get(video_url, timeout=120)
                Path(output_path).write_bytes(vid_resp.content)
                size_mb = len(vid_resp.content) / (1024 * 1024)
                print(f"  Video saved: {Path(output_path).name} ({size_mb:.1f} MB)")
                return output_path
        elif status == "failed":
            error = data.get("error", "unknown")
            print(f"  Video FAILED: {error}")
            return None

    print(f"  Video timed out after {max_wait}s")
    return None


def main():
    print("=" * 60)
    print("  AI Daily Omniverse -- Episode 3 Production")
    print("  Date: 2026-03-26")
    print("  Real source photos: 6 downloaded")
    print("  NO AI-generated thumbnails")
    print("=" * 60)
    print()

    # Load segment plan
    plan = json.loads((EPISODE_DIR / "segment-plan.json").read_text())
    print(f"Loaded {len(plan)} segments")
    print()

    # ---- STEP 1: TTS Audio ----
    print("STEP 1: Generating TTS audio...")
    audio_paths = {}
    for seg in plan:
        seg_id = seg["id"]
        # Pick voice based on role
        if seg["role"] == "field":
            voice_id = ADRIANA_VOICE
        else:
            voice_id = ARMANDO_VOICE

        audio_path = EPISODE_DIR / f"v2-{seg_id}-audio.mp3"
        print(f"  [{seg_id}] voice={'Adriana' if seg['role']=='field' else 'Armando'}...")
        result = generate_tts(seg["text"], str(audio_path), voice_id)
        if result:
            audio_paths[seg_id] = str(audio_path)
    print(f"\nTTS complete: {len(audio_paths)}/{len(plan)} segments")
    print()

    if not audio_paths:
        print("ERROR: No audio generated. Check API key.")
        return

    # ---- STEP 2: Upload audio + create HeyGen videos ----
    print("STEP 2: Uploading audio and creating HeyGen videos...")
    video_ids = {}
    for seg in plan:
        seg_id = seg["id"]
        audio_path = audio_paths.get(seg_id)
        if not audio_path:
            continue

        print(f"  [{seg_id}] uploading audio...")
        asset_id = upload_audio_heygen(audio_path)
        if not asset_id:
            continue

        print(f"  [{seg_id}] creating video with {seg['avatar']}...")
        video_id = create_heygen_video(seg["avatar"], asset_id)
        if video_id:
            video_ids[seg_id] = video_id

    # Save video IDs for recovery
    ids_path = EPISODE_DIR / "v2-video-ids.json"
    ids_path.write_text(json.dumps(video_ids, indent=2))
    print(f"\nSubmitted {len(video_ids)} videos to HeyGen")
    print(f"Video IDs saved: {ids_path}")
    print()

    if not video_ids:
        print("ERROR: No videos submitted. Check HeyGen API key.")
        return

    # ---- STEP 3: Poll and download videos ----
    print("STEP 3: Polling for video completion...")
    for seg_id, vid_id in video_ids.items():
        print(f"  [{seg_id}] waiting for {vid_id}...")
        output_path = EPISODE_DIR / f"v2-{seg_id}-video.mp4"
        poll_heygen_video(vid_id, str(output_path))

    # ---- Summary ----
    print()
    print("=" * 60)
    print("  PRODUCTION STATUS")
    print("=" * 60)
    for seg in plan:
        seg_id = seg["id"]
        audio_ok = (EPISODE_DIR / f"v2-{seg_id}-audio.mp3").exists()
        video_ok = (EPISODE_DIR / f"v2-{seg_id}-video.mp4").exists()
        thumb = seg.get("thumbnail", "n/a")
        print(f"  {seg_id:10s} audio={'OK' if audio_ok else 'MISSING':7s} video={'OK' if video_ok else 'MISSING':7s} thumb={thumb}")

    print()
    print("Next: python scripts/assemble_newscast.py 2026-03-26")
    print("=" * 60)


if __name__ == "__main__":
    main()
