"""
AIDO YouTube Upload
Uploads the final MP4 to YouTube using the Data API v3.

Setup (one-time):
    1. Create a project in Google Cloud Console
    2. Enable YouTube Data API v3
    3. Create OAuth 2.0 credentials (Desktop app)
    4. Download credentials.json → project root
    5. Run: python -m aido.upload_youtube --auth-only
       (Browser opens, approve, token saved to youtube_token.json)

Usage:
    python -m aido.upload_youtube \
        --manifest output/EP001/manifest.json \
        --mp4 output/EP001/EP001_final.mp4

Requires:
    pip install google-auth-oauthlib google-api-python-client
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path

logger = logging.getLogger("aido.upload_youtube")
logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")

_SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
_CREDENTIALS_FILE = "credentials.json"
_TOKEN_FILE = "youtube_token.json"
_CHUNK_SIZE = 8 * 1024 * 1024   # 8 MB


def _get_youtube_client():
    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
    except ImportError:
        logger.error(
            "Missing Google libraries. Install:\n"
            "  pip install google-auth-oauthlib google-api-python-client"
        )
        sys.exit(1)

    creds = None
    token_path = Path(_TOKEN_FILE)
    creds_path = Path(_CREDENTIALS_FILE)

    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), _SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not creds_path.exists():
                logger.error(
                    "credentials.json not found. Download it from Google Cloud Console:\n"
                    "  APIs & Services → Credentials → OAuth 2.0 → Download JSON\n"
                    "  Save as: %s",
                    creds_path.resolve(),
                )
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), _SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_path, "w") as f:
            f.write(creds.to_json())
        logger.info("YouTube token saved to %s", token_path)

    return build("youtube", "v3", credentials=creds)


def upload_video(
    mp4_path: str,
    title: str,
    description: str,
    tags: list[str] | None = None,
    playlist_id: str = "",
    privacy: str = "private",
) -> str:
    """Upload video and return the YouTube video ID."""
    try:
        from googleapiclient.http import MediaFileUpload
    except ImportError:
        logger.error("pip install google-api-python-client")
        sys.exit(1)

    yt = _get_youtube_client()

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags or ["AI", "technology", "daily briefing", "AIDO"],
            "categoryId": "28",   # Science & Technology
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(mp4_path, chunksize=_CHUNK_SIZE, resumable=True)
    request = yt.videos().insert(part="snippet,status", body=body, media_body=media)

    logger.info("Uploading %s to YouTube (privacy: %s)...", Path(mp4_path).name, privacy)
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            pct = int(status.progress() * 100)
            logger.info("  upload progress: %d%%", pct)

    video_id = response.get("id", "")
    logger.info("Upload complete! Video ID: %s", video_id)
    logger.info("  URL: https://www.youtube.com/watch?v=%s", video_id)

    if playlist_id and video_id:
        _add_to_playlist(yt, video_id, playlist_id)

    return video_id


def _add_to_playlist(yt, video_id: str, playlist_id: str) -> None:
    try:
        yt.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {"kind": "youtube#video", "videoId": video_id},
                }
            },
        ).execute()
        logger.info("Added to playlist: %s", playlist_id)
    except Exception as exc:
        logger.warning("Could not add to playlist: %s", exc)


def run(manifest_path: str, mp4_path: str | None, privacy: str = "private") -> None:
    with open(manifest_path, encoding="utf-8") as f:
        d = json.load(f)
    from aido.manifest_schema import EpisodeManifest
    manifest = EpisodeManifest.from_dict(d)

    mp4 = mp4_path or manifest.final_mp4
    if not mp4 or not Path(mp4).exists():
        logger.error("MP4 not found: %s. Run assemble.py first.", mp4)
        sys.exit(1)

    description = (
        f"{manifest.title}\n\n"
        f"Published: {manifest.publish_date}\n\n"
        f"Daily AI & technology briefing powered by Mission Control.\n\n"
        f"Subscribe for daily updates on AI breakthroughs, infrastructure, and IoT.\n\n"
        f"#AI #Technology #DailyBriefing #ArtificialIntelligence #IoT"
    )

    video_id = upload_video(
        mp4_path=mp4,
        title=manifest.title,
        description=description,
        tags=["AI", "technology", "AIDO", "Omniverse", "daily briefing", "IoT", "Claude"],
        playlist_id=manifest.youtube_playlist_id,
        privacy=privacy,
    )

    # Save video ID back to manifest
    d["youtube_video_id"] = video_id
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2)
    logger.info("Manifest updated with YouTube video ID.")


def main() -> None:
    p = argparse.ArgumentParser(description="AIDO YouTube uploader")
    p.add_argument("--manifest", required=True)
    p.add_argument("--mp4", help="Override MP4 path from manifest")
    p.add_argument("--privacy", default="private", choices=["private", "unlisted", "public"])
    p.add_argument("--auth-only", action="store_true", help="Just authenticate, don't upload")
    args = p.parse_args()

    if args.auth_only:
        _get_youtube_client()
        logger.info("Authentication complete.")
        return

    run(args.manifest, args.mp4, args.privacy)


if __name__ == "__main__":
    main()
