"""
AIDO TTS Generation — ElevenLabs
Generates per-segment MP3 audio from manifest narration text.

Usage:
    python -m aido.tts_generate --episode EP001 --out-dir output/EP001
    python -m aido.tts_generate --manifest path/to/manifest.json --out-dir output/EP001

Requires:
    ELEVENLABS_API_KEY in environment or .env
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path

import httpx
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("aido.tts")
logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")

_ELEVENLABS_BASE = "https://api.elevenlabs.io/v1"
_DEFAULT_MODEL = "eleven_turbo_v2_5"
_DEFAULT_VOICE_SETTINGS = {
    "stability": 0.55,
    "similarity_boost": 0.80,
    "style": 0.30,
    "use_speaker_boost": True,
}


def generate_segment_audio(
    text: str,
    voice_id: str,
    api_key: str,
    out_path: Path,
    model: str = _DEFAULT_MODEL,
    retries: int = 3,
) -> Path:
    """Call ElevenLabs TTS and write MP3 to out_path. Returns the path."""
    url = f"{_ELEVENLABS_BASE}/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }
    body = {
        "text": text,
        "model_id": model,
        "voice_settings": _DEFAULT_VOICE_SETTINGS,
    }

    for attempt in range(1, retries + 1):
        try:
            with httpx.Client(timeout=60.0) as client:
                resp = client.post(url, json=body, headers=headers)
            if resp.status_code == 200:
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_bytes(resp.content)
                logger.info("  saved %s  (%d bytes)", out_path.name, len(resp.content))
                return out_path
            elif resp.status_code == 429:
                wait = 10 * attempt
                logger.warning("  rate limited — waiting %ds (attempt %d/%d)", wait, attempt, retries)
                time.sleep(wait)
            else:
                logger.error("  ElevenLabs %d: %s", resp.status_code, resp.text[:200])
                raise RuntimeError(f"ElevenLabs HTTP {resp.status_code}")
        except httpx.TimeoutException:
            logger.warning("  timeout on attempt %d/%d", attempt, retries)
            if attempt == retries:
                raise

    raise RuntimeError(f"TTS failed after {retries} attempts for: {text[:60]}")


def run(episode_id: str | None, manifest_path: str | None, out_dir: str) -> None:
    api_key = os.environ.get("ELEVENLABS_API_KEY", "")
    if not api_key:
        logger.error("ELEVENLABS_API_KEY not set. Add it to .env")
        sys.exit(1)

    # Load manifest
    if manifest_path:
        with open(manifest_path, encoding="utf-8") as f:
            manifest_data = json.load(f)
        from aido.manifest_schema import EpisodeManifest
        manifest = EpisodeManifest.from_dict(manifest_data)
    elif episode_id:
        from aido import manifest_schema as ms
        manifest = getattr(ms, episode_id, None)
        if manifest is None:
            logger.error("Unknown episode %s. Available: EP001", episode_id)
            sys.exit(1)
    else:
        logger.error("Provide --episode or --manifest")
        sys.exit(1)

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    logger.info("Generating TTS for %s — %d segments", manifest.episode_id, len(manifest.segments))
    logger.info("Voice: %s", manifest.voice_id)

    for seg in manifest.segments:
        filename = f"{seg.id}.mp3"
        out_path = out / "audio" / filename
        if out_path.exists():
            logger.info("  [skip] %s already exists", filename)
            seg.audio_path = str(out_path)
            continue

        logger.info("  [TTS] %s", seg.id)
        generate_segment_audio(
            text=seg.narration,
            voice_id=manifest.voice_id,
            api_key=api_key,
            out_path=out_path,
        )
        seg.audio_path = str(out_path)
        time.sleep(1.0)   # polite gap between requests

    # Write updated manifest with audio paths
    manifest_out = out / "manifest.json"
    with open(manifest_out, "w", encoding="utf-8") as f:
        json.dump(manifest.to_dict(), f, indent=2)
    logger.info("Manifest written: %s", manifest_out)
    logger.info("TTS generation complete.")


def main() -> None:
    p = argparse.ArgumentParser(description="AIDO TTS generation")
    p.add_argument("--episode", help="Episode ID (e.g. EP001)")
    p.add_argument("--manifest", help="Path to manifest JSON")
    p.add_argument("--out-dir", default="output/EP001", help="Output directory")
    args = p.parse_args()
    run(args.episode, args.manifest, args.out_dir)


if __name__ == "__main__":
    main()
