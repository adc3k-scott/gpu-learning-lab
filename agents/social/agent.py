"""
SocialAgent — Multi-platform content distribution.

Listens for completed episode assemblies and posts clips/descriptions
to TikTok, Instagram, X (Twitter), LinkedIn, and YouTube Shorts.

Platforms supported:
  youtube   — long-form via Data API v3 (handled by PublisherAgent/upload_youtube.py)
  twitter   — post tweet with clip link via Twitter API v2
  linkedin  — post to company page via LinkedIn API
  tiktok    — upload video via TikTok Content Posting API
  instagram — upload Reel via Meta Graph API

Event contract
--------------
Listens:
  publish.assemble.done   — {episode_id, mp4_path}  → post to all configured platforms
  social.post             — {platform, episode_id, mp4_path, caption}  → single platform

Emits:
  social.posted           — {episode_id, platform, url, post_id}
  social.failed           — {episode_id, platform, error}

Config (StateStore or .env):
  TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET
  LINKEDIN_ACCESS_TOKEN, LINKEDIN_PAGE_ID
  TIKTOK_ACCESS_TOKEN
  INSTAGRAM_ACCESS_TOKEN, INSTAGRAM_ACCOUNT_ID
  FACEBOOK_PAGE_ID, FACEBOOK_ACCESS_TOKEN
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
from pathlib import Path
from typing import Any

import httpx

from agents.base import BaseAgent
from core.event_bus import Event

logger = logging.getLogger(__name__)

_TIMEOUT = 60.0


class SocialAgent(BaseAgent):
    role = "social"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._creds: dict[str, str] = {}

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def _setup(self) -> None:
        self._load_creds()
        self.bus.subscribe("publish.assemble.done", self._on_assemble_done)
        self.bus.subscribe("social.post", self._on_social_post)
        self.bus.subscribe("config.updated", self._on_config_updated)
        logger.info("[%s] SocialAgent ready — platforms: %s", self.agent_id, self._active_platforms())

    def _load_creds(self) -> None:
        keys = [
            "TWITTER_API_KEY", "TWITTER_API_SECRET",
            "TWITTER_ACCESS_TOKEN", "TWITTER_ACCESS_SECRET",
            "LINKEDIN_ACCESS_TOKEN", "LINKEDIN_PAGE_ID",
            "TIKTOK_ACCESS_TOKEN",
            "INSTAGRAM_ACCESS_TOKEN", "INSTAGRAM_ACCOUNT_ID",
            "FACEBOOK_PAGE_ID", "FACEBOOK_ACCESS_TOKEN",
        ]
        self._creds = {k: os.environ.get(k, "") for k in keys}

    def _active_platforms(self) -> list[str]:
        active = []
        if self._creds.get("TWITTER_API_KEY"):
            active.append("twitter")
        if self._creds.get("LINKEDIN_ACCESS_TOKEN") and self._creds.get("LINKEDIN_PAGE_ID"):
            active.append("linkedin")
        if self._creds.get("TIKTOK_ACCESS_TOKEN"):
            active.append("tiktok")
        if self._creds.get("INSTAGRAM_ACCESS_TOKEN") and self._creds.get("INSTAGRAM_ACCOUNT_ID"):
            active.append("instagram")
        return active

    async def _on_config_updated(self, event: Event) -> None:
        self._load_creds()

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    async def _on_assemble_done(self, event: Event) -> None:
        episode_id = event.payload.get("episode_id", "")
        mp4_path   = event.payload.get("mp4_path", "")

        # Load manifest for caption/title
        manifest = await self._load_manifest(episode_id, mp4_path)
        caption = _build_caption(manifest)

        platforms = self._active_platforms()
        if not platforms:
            logger.info("[%s] No social platforms configured yet — skipping distribution", self.agent_id)
            return

        tasks = [
            self._post_to_platform(platform, episode_id, mp4_path, caption)
            for platform in platforms
        ]
        await asyncio.gather(*tasks, return_exceptions=True)

    async def _on_social_post(self, event: Event) -> None:
        platform   = event.payload.get("platform", "")
        episode_id = event.payload.get("episode_id", "")
        mp4_path   = event.payload.get("mp4_path", "")
        caption    = event.payload.get("caption", "")

        if not caption:
            manifest = await self._load_manifest(episode_id, mp4_path)
            caption = _build_caption(manifest)

        await self._post_to_platform(platform, episode_id, mp4_path, caption)

    # ------------------------------------------------------------------
    # Platform dispatch
    # ------------------------------------------------------------------

    async def _post_to_platform(self, platform: str, episode_id: str, mp4_path: str, caption: str) -> None:
        try:
            if platform == "twitter":
                result = await self._post_twitter(caption, mp4_path)
            elif platform == "linkedin":
                result = await self._post_linkedin(caption, mp4_path)
            elif platform == "tiktok":
                result = await self._post_tiktok(caption, mp4_path)
            elif platform == "instagram":
                result = await self._post_instagram(caption, mp4_path)
            else:
                logger.warning("[%s] Unknown platform: %s", self.agent_id, platform)
                return

            logger.info("[%s] Posted to %s: %s", self.agent_id, platform, result.get("url", ""))
            await self.publish("social.posted", {
                "episode_id": episode_id,
                "platform": platform,
                "url": result.get("url", ""),
                "post_id": result.get("post_id", ""),
            })
        except Exception as exc:
            logger.error("[%s] %s post failed: %s", self.agent_id, platform, exc)
            await self.publish("social.failed", {
                "episode_id": episode_id,
                "platform": platform,
                "error": str(exc),
            })

    # ------------------------------------------------------------------
    # Twitter / X
    # ------------------------------------------------------------------

    async def _post_twitter(self, caption: str, mp4_path: str) -> dict:
        """Post tweet with text. Video upload requires chunked media upload — text-only fallback for now."""
        import base64
        import hmac
        import hashlib
        import time
        import urllib.parse

        api_key    = self._creds["TWITTER_API_KEY"]
        api_secret = self._creds["TWITTER_API_SECRET"]
        token      = self._creds["TWITTER_ACCESS_TOKEN"]
        token_secret = self._creds["TWITTER_ACCESS_SECRET"]

        # Twitter API v2 tweet endpoint
        url = "https://api.twitter.com/2/tweets"
        tweet_text = caption[:280]

        # OAuth 1.0a signature
        oauth_params = {
            "oauth_consumer_key": api_key,
            "oauth_nonce": os.urandom(16).hex(),
            "oauth_signature_method": "HMAC-SHA1",
            "oauth_timestamp": str(int(time.time())),
            "oauth_token": token,
            "oauth_version": "1.0",
        }

        param_string = "&".join(
            f"{urllib.parse.quote(k, safe='')}={urllib.parse.quote(str(v), safe='')}"
            for k, v in sorted(oauth_params.items())
        )
        base_string = "&".join([
            "POST",
            urllib.parse.quote(url, safe=""),
            urllib.parse.quote(param_string, safe=""),
        ])
        signing_key = f"{urllib.parse.quote(api_secret, safe='')}&{urllib.parse.quote(token_secret, safe='')}"
        signature = base64.b64encode(
            hmac.new(signing_key.encode(), base_string.encode(), hashlib.sha1).digest()
        ).decode()
        oauth_params["oauth_signature"] = signature

        auth_header = "OAuth " + ", ".join(
            f'{urllib.parse.quote(k, safe="")}="{urllib.parse.quote(str(v), safe="")}"'
            for k, v in sorted(oauth_params.items())
        )

        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            resp = await client.post(
                url,
                json={"text": tweet_text},
                headers={
                    "Authorization": auth_header,
                    "Content-Type": "application/json",
                },
            )

        if not resp.is_success:
            raise RuntimeError(f"Twitter API {resp.status_code}: {resp.text[:300]}")

        data = resp.json()
        tweet_id = data.get("data", {}).get("id", "")
        return {"post_id": tweet_id, "url": f"https://twitter.com/i/web/status/{tweet_id}"}

    # ------------------------------------------------------------------
    # LinkedIn
    # ------------------------------------------------------------------

    async def _post_linkedin(self, caption: str, mp4_path: str) -> dict:
        token   = self._creds["LINKEDIN_ACCESS_TOKEN"]
        page_id = self._creds["LINKEDIN_PAGE_ID"]

        body = {
            "author": f"urn:li:organization:{page_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": caption[:3000]},
                    "shareMediaCategory": "NONE",
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
        }

        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            resp = await client.post(
                "https://api.linkedin.com/v2/ugcPosts",
                json=body,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                    "X-Restli-Protocol-Version": "2.0.0",
                },
            )

        if not resp.is_success:
            raise RuntimeError(f"LinkedIn API {resp.status_code}: {resp.text[:300]}")

        post_id = resp.headers.get("x-restli-id", "")
        return {"post_id": post_id, "url": f"https://www.linkedin.com/feed/update/{post_id}"}

    # ------------------------------------------------------------------
    # TikTok
    # ------------------------------------------------------------------

    async def _post_tiktok(self, caption: str, mp4_path: str) -> dict:
        """
        TikTok Content Posting API — uploads video directly.
        Requires TikTok for Developers app with video.publish scope.
        """
        token = self._creds["TIKTOK_ACCESS_TOKEN"]

        if not Path(mp4_path).exists():
            raise RuntimeError(f"MP4 not found for TikTok upload: {mp4_path}")

        # Step 1: Init upload
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            init_resp = await client.post(
                "https://open.tiktokapis.com/v2/post/publish/video/init/",
                json={
                    "post_info": {
                        "title": caption[:150],
                        "privacy_level": "SELF_ONLY",   # private until approved
                        "disable_duet": False,
                        "disable_comment": False,
                        "disable_stitch": False,
                        "video_cover_timestamp_ms": 1000,
                    },
                    "source_info": {
                        "source": "FILE_UPLOAD",
                        "video_size": Path(mp4_path).stat().st_size,
                        "chunk_size": Path(mp4_path).stat().st_size,
                        "total_chunk_count": 1,
                    },
                },
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json; charset=UTF-8",
                },
            )

        if not init_resp.is_success:
            raise RuntimeError(f"TikTok init {init_resp.status_code}: {init_resp.text[:300]}")

        data = init_resp.json().get("data", {})
        publish_id = data.get("publish_id", "")
        upload_url = data.get("upload_url", "")

        if not upload_url:
            raise RuntimeError("TikTok did not return upload_url")

        # Step 2: Upload video bytes
        video_bytes = Path(mp4_path).read_bytes()
        async with httpx.AsyncClient(timeout=300.0) as client:
            up_resp = await client.put(
                upload_url,
                content=video_bytes,
                headers={
                    "Content-Type": "video/mp4",
                    "Content-Length": str(len(video_bytes)),
                    "Content-Range": f"bytes 0-{len(video_bytes)-1}/{len(video_bytes)}",
                },
            )

        if not up_resp.is_success:
            raise RuntimeError(f"TikTok upload {up_resp.status_code}: {up_resp.text[:200]}")

        return {"post_id": publish_id, "url": "https://www.tiktok.com/@missioncontrol"}

    # ------------------------------------------------------------------
    # Instagram Reels
    # ------------------------------------------------------------------

    async def _post_instagram(self, caption: str, mp4_path: str) -> dict:
        """
        Meta Graph API — Instagram Reels posting.
        Requires publicly accessible video URL (S3/CDN) — local file not supported directly.
        """
        token      = self._creds["INSTAGRAM_ACCESS_TOKEN"]
        account_id = self._creds["INSTAGRAM_ACCOUNT_ID"]

        video_url = os.environ.get("INSTAGRAM_VIDEO_CDN_URL", "")
        if not video_url:
            logger.warning(
                "[%s] INSTAGRAM_VIDEO_CDN_URL not set — Instagram Reels require public video URL. "
                "Upload to S3/CDN first and set this env var.",
                self.agent_id,
            )
            return {"post_id": "", "url": "", "note": "CDN URL required"}

        base = f"https://graph.facebook.com/v19.0/{account_id}"

        # Step 1: Create media container
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            create_resp = await client.post(
                f"{base}/media",
                params={
                    "media_type": "REELS",
                    "video_url": video_url,
                    "caption": caption[:2200],
                    "access_token": token,
                },
            )

        if not create_resp.is_success:
            raise RuntimeError(f"Instagram create {create_resp.status_code}: {create_resp.text[:300]}")

        container_id = create_resp.json().get("id", "")

        # Step 2: Publish container
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            pub_resp = await client.post(
                f"{base}/media_publish",
                params={"creation_id": container_id, "access_token": token},
            )

        if not pub_resp.is_success:
            raise RuntimeError(f"Instagram publish {pub_resp.status_code}: {pub_resp.text[:300]}")

        post_id = pub_resp.json().get("id", "")
        return {"post_id": post_id, "url": f"https://www.instagram.com/reel/{post_id}"}

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    async def _load_manifest(self, episode_id: str, mp4_path: str) -> dict:
        # Try to find manifest.json next to the mp4
        if mp4_path:
            candidate = Path(mp4_path).parent / "manifest.json"
            if candidate.exists():
                with open(candidate, encoding="utf-8") as f:
                    return json.load(f)
        # Try StateStore
        cached = await self.store.get(f"publish:done:{episode_id}")
        return cached or {}


def _build_caption(manifest: dict) -> str:
    title    = manifest.get("title", "Mission Control Briefing")
    subtitle = manifest.get("subtitle", "")
    date     = manifest.get("publish_date", "")
    tags = "#AI #Technology #DailyBriefing #MissionControl #Innovation"
    parts = [title]
    if subtitle:
        parts.append(subtitle)
    if date:
        parts.append(date)
    parts.append("")
    parts.append("Daily intelligence briefing powered by Mission Control.")
    parts.append("Subscribe for AI, robotics, aviation, AUV, and motorcycle tech updates.")
    parts.append("")
    parts.append(tags)
    return "\n".join(parts)
