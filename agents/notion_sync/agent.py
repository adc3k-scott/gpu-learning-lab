"""
NotionSyncAgent — syncs completed Mission Control jobs to a Notion work folder.

Every time a job completes, this agent creates a Notion page in the configured
work database. The page records the job title, status, and step-by-step results,
giving you a persistent audit trail in your Notion workspace.

Configuration (checked in order):
  1. StateStore key  "config:notion_work_db_id"  — set at runtime via /config API
  2. StateStore key  "config:notion_api_key"      — set at runtime via /config API
  3. Environment variables NOTION_WORK_DB_ID / NOTION_API_KEY — from .env

If neither a database ID nor an API key is configured, the agent silently skips
sync (it does not fail the originating job).

Event contract
--------------
Listens on:
  job.completed   payload: {job_id, results}
  job.failed      payload: {job_id, error}
  config.updated  payload: {key, value}          (re-reads config on the fly)

Emits:
  notion.page.created  payload: {job_id, page_id, url}
  notion.sync.skipped  payload: {job_id, reason}
  notion.sync.error    payload: {job_id, error}
"""

from __future__ import annotations

import json
import logging
import os
import time
from typing import Any

from agents.base import BaseAgent
from core.event_bus import Event

logger = logging.getLogger(__name__)

_CONFIG_DB_KEY  = "config:notion_work_db_id"
_CONFIG_KEY_KEY = "config:notion_api_key"


class NotionSyncAgent(BaseAgent):
    role = "notion_sync"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Cached config — refreshed on config.updated events
        self._db_id:  str = ""
        self._api_key: str = ""

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def _setup(self) -> None:
        await self._reload_config()
        self.bus.subscribe("job.completed", self._on_job_done)
        self.bus.subscribe("job.failed",    self._on_job_done)
        self.bus.subscribe("config.updated", self._on_config_updated)
        logger.info(
            "[%s] NotionSyncAgent ready — work db: %s",
            self.agent_id,
            self._db_id or "(not configured)",
        )

    # ------------------------------------------------------------------
    # Config helpers
    # ------------------------------------------------------------------

    async def _reload_config(self) -> None:
        stored_db  = await self.store.get(_CONFIG_DB_KEY)
        stored_key = await self.store.get(_CONFIG_KEY_KEY)
        self._db_id   = stored_db  or os.environ.get("NOTION_WORK_DB_ID", "")
        self._api_key = stored_key or os.environ.get("NOTION_API_KEY", "")

    async def _on_config_updated(self, event: Event) -> None:
        key = event.payload.get("key", "")
        if key in (_CONFIG_DB_KEY, _CONFIG_KEY_KEY):
            await self._reload_config()
            logger.info("[%s] Config reloaded — work db: %s", self.agent_id, self._db_id or "(none)")

    # ------------------------------------------------------------------
    # Event handler
    # ------------------------------------------------------------------

    async def _on_job_done(self, event: Event) -> None:
        job_id = event.payload.get("job_id", "")
        if not job_id:
            return

        if not self._db_id:
            await self.publish("notion.sync.skipped", {
                "job_id": job_id,
                "reason": "NOTION_WORK_DB_ID not configured",
            })
            return

        if not self._api_key:
            await self.publish("notion.sync.skipped", {
                "job_id": job_id,
                "reason": "NOTION_API_KEY not configured",
            })
            return

        # Fetch full job dict from state store
        job = await self.store.get(f"jobs:{job_id}")
        if not job:
            logger.warning("[%s] Could not fetch job %s from store — skipping Notion sync", self.agent_id, job_id)
            await self.publish("notion.sync.skipped", {
                "job_id": job_id,
                "reason": "Job not found in state store",
            })
            return

        try:
            page_id, url = await self._sync_job(job)
            await self.publish("notion.page.created", {
                "job_id": job_id,
                "page_id": page_id,
                "url": url,
            })
            logger.info("[%s] Synced job %s → Notion page %s", self.agent_id, job_id, page_id)
        except Exception as exc:
            logger.warning("[%s] Notion sync failed for job %s: %s", self.agent_id, job_id, exc)
            await self.publish("notion.sync.error", {
                "job_id": job_id,
                "error": str(exc),
            })

    # ------------------------------------------------------------------
    # Notion page construction
    # ------------------------------------------------------------------

    async def _sync_job(self, job: dict[str, Any]) -> tuple[str, str]:
        """Create a Notion page for the completed job. Returns (page_id, url)."""
        title   = job.get("title") or job.get("job_id", "Untitled job")
        status  = job.get("status", "unknown")
        job_id  = job.get("job_id", "")
        steps   = job.get("steps", [])
        error   = job.get("error", "")

        blocks = _build_blocks(job_id, status, steps, error)

        result = await self.run_skill("notion", {
            "action":      "create_page",
            "parent_id":   self._db_id,
            "parent_type": "database_id",
            "title":       title,
            "blocks":      blocks,
        }, extra_metadata={"notion_api_key": self._api_key})

        if not result.success:
            raise RuntimeError(result.error)

        page_id = result.output.get("id", "")
        url     = result.output.get("url", "")
        return page_id, url

    # ------------------------------------------------------------------
    # Public API — for /config and tests
    # ------------------------------------------------------------------

    def set_config(self, db_id: str = "", api_key: str = "") -> None:
        """Update in-memory config directly (used by /config endpoint)."""
        if db_id:
            self._db_id = db_id
        if api_key:
            self._api_key = api_key

    def get_config(self) -> dict[str, str]:
        return {
            "notion_work_db_id": self._db_id,
            "notion_api_key_set": "yes" if self._api_key else "no",
        }


# ---------------------------------------------------------------------------
# Block builders
# ---------------------------------------------------------------------------

def _build_blocks(job_id: str, status: str, steps: list[dict], error: str) -> list[dict]:
    """Return a list of Notion block dicts describing the job result."""
    blocks: list[dict] = []

    # --- Header callout ---
    emoji = "✅" if status == "completed" else "❌"
    blocks.append(_callout(f"{emoji} {status.upper()} — job {job_id[:8]}…"))

    # --- Metadata ---
    blocks.append(_paragraph(f"**Status:** {status}"))
    blocks.append(_paragraph(f"**Job ID:** `{job_id}`"))
    blocks.append(_paragraph(f"**Synced:** {_iso_now()}"))

    if error:
        blocks.append(_paragraph(f"**Error:** {error}"))

    # --- Step results ---
    if steps:
        blocks.append(_heading("Steps"))
        for step in steps:
            name   = step.get("name", "step")
            s_status = step.get("status", "")
            result = step.get("result")
            s_error  = step.get("error", "")

            icon = {"completed": "✅", "failed": "❌", "skipped": "⏭️"}.get(s_status, "⬜")
            blocks.append(_heading(f"{icon} {name}", level=3))

            if result is not None:
                body = result if isinstance(result, str) else json.dumps(result, indent=2)
                # Cap block text at 1900 chars (Notion limit is 2000)
                for chunk in _split(body, 1900):
                    blocks.append(_code(chunk))
            elif s_error:
                blocks.append(_paragraph(f"Error: {s_error}"))

    return blocks


def _callout(text: str) -> dict:
    return {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": [{"type": "text", "text": {"content": text}}],
            "icon": {"type": "emoji", "emoji": "🤖"},
        },
    }


def _paragraph(text: str) -> dict:
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": [{"type": "text", "text": {"content": text}}]},
    }


def _heading(text: str, level: int = 2) -> dict:
    t = f"heading_{level}"
    return {
        "object": "block",
        "type": t,
        t: {"rich_text": [{"type": "text", "text": {"content": text}}]},
    }


def _code(text: str) -> dict:
    return {
        "object": "block",
        "type": "code",
        "code": {
            "rich_text": [{"type": "text", "text": {"content": text}}],
            "language": "plain text",
        },
    }


def _split(text: str, size: int) -> list[str]:
    return [text[i: i + size] for i in range(0, len(text), size)] or [""]


def _iso_now() -> str:
    import datetime
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
