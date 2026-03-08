"""
PublisherAgent — End-to-end episode production coordinator.

Listens for approved episode manifests and drives the full render pipeline:
  TTS generation → USD injection → Omniverse render → FFmpeg assembly → platform upload

Supports two render modes:
  local   — runs pipeline steps in-process (TTS + assemble locally, no Omniverse)
  runpod  — SSH deploy to RunPod for full Omniverse render

Event contract
--------------
Listens:
  publish.episode       — {manifest_path|episode_id, out_dir, mode, skip_render, no_upload}
  news.stories.ready    — auto-draft + queue episode from news scout output
  publish.approve       — {episode_id} — approve a queued draft for production

Emits:
  publish.started       — {episode_id, out_dir}
  publish.tts.done      — {episode_id, audio_files}
  publish.render.done   — {episode_id, frames_dir}
  publish.assemble.done — {episode_id, mp4_path}
  publish.upload.done   — {episode_id, platforms, urls}
  publish.failed        — {episode_id, stage, error}
  publish.queued        — {episode_id, draft} — new draft waiting for approval

StateStore keys
---------------
  publish:queue         — list of pending episode drafts
  publish:active        — currently producing episode_id
  publish:done:{id}     — completed episode metadata
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import time
from pathlib import Path
from typing import Any

from agents.base import BaseAgent
from core.event_bus import Event

logger = logging.getLogger(__name__)


class PublisherAgent(BaseAgent):
    role = "publisher"

    def __init__(self, *, project_root: str = ".", **kwargs):
        super().__init__(project_root=project_root, **kwargs)
        self._output_base = Path(project_root) / "output"
        self._queue: list[dict] = []
        self._producing = False

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def _setup(self) -> None:
        self.bus.subscribe("publish.episode", self._on_publish_episode)
        self.bus.subscribe("publish.approve", self._on_publish_approve)
        self.bus.subscribe("news.stories.ready", self._on_news_ready)
        logger.info("[%s] PublisherAgent ready", self.agent_id)

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    async def _on_publish_episode(self, event: Event) -> None:
        """Directly trigger production of an episode."""
        p = event.payload
        episode_id   = p.get("episode_id", "EP001")
        manifest_path = p.get("manifest_path", "")
        out_dir      = p.get("out_dir", str(self._output_base / episode_id))
        mode         = p.get("mode", "local")          # "local" | "runpod"
        skip_render  = p.get("skip_render", True)
        no_upload    = p.get("no_upload", True)
        privacy      = p.get("privacy", "private")

        asyncio.create_task(
            self._produce(episode_id, manifest_path, out_dir, mode, skip_render, no_upload, privacy)
        )

    async def _on_publish_approve(self, event: Event) -> None:
        """Approve a queued draft episode for production."""
        episode_id = event.payload.get("episode_id", "")
        draft = next((d for d in self._queue if d.get("episode_id") == episode_id), None)
        if not draft:
            logger.warning("[%s] No queued draft for episode_id=%s", self.agent_id, episode_id)
            return
        self._queue.remove(draft)
        asyncio.create_task(
            self._produce(
                episode_id=draft["episode_id"],
                manifest_path=draft.get("manifest_path", ""),
                out_dir=draft.get("out_dir", str(self._output_base / episode_id)),
                mode=draft.get("mode", "local"),
                skip_render=draft.get("skip_render", True),
                no_upload=draft.get("no_upload", False),
                privacy=draft.get("privacy", "private"),
            )
        )

    async def _on_news_ready(self, event: Event) -> None:
        """Auto-queue a draft episode when NewsScoutAgent delivers stories."""
        vertical = event.payload.get("vertical", "ai")
        draft_data = event.payload.get("episode_draft", {})
        if not draft_data or not draft_data.get("segments"):
            return

        episode_id = f"DRAFT-{vertical.upper()}-{int(time.time())}"
        out_dir = str(self._output_base / episode_id)

        # Write manifest JSON for this draft
        Path(out_dir).mkdir(parents=True, exist_ok=True)
        manifest = _build_manifest_from_draft(episode_id, vertical, draft_data)
        manifest_path = Path(out_dir) / "manifest.json"
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        draft_entry = {
            "episode_id": episode_id,
            "vertical": vertical,
            "manifest_path": str(manifest_path),
            "out_dir": out_dir,
            "mode": "local",
            "skip_render": True,
            "no_upload": True,
            "privacy": "private",
            "created_at": time.time(),
            "draft": draft_data,
        }
        self._queue.append(draft_entry)
        await self.store.set("publish:queue", self._queue)

        logger.info("[%s] Queued draft: %s (%s)", self.agent_id, episode_id, vertical)
        await self.publish("publish.queued", {"episode_id": episode_id, "vertical": vertical, "draft": draft_data})

    # ------------------------------------------------------------------
    # Production pipeline
    # ------------------------------------------------------------------

    async def _produce(
        self,
        episode_id: str,
        manifest_path: str,
        out_dir: str,
        mode: str,
        skip_render: bool,
        no_upload: bool,
        privacy: str,
    ) -> None:
        if self._producing:
            logger.warning("[%s] Already producing — queuing %s", self.agent_id, episode_id)
            return

        self._producing = True
        await self.store.set("publish:active", episode_id)
        await self.publish("publish.started", {"episode_id": episode_id, "out_dir": out_dir})
        logger.info("[%s] Production started: %s (mode=%s)", self.agent_id, episode_id, mode)

        try:
            if mode == "runpod":
                await self._produce_runpod(episode_id, manifest_path, out_dir, privacy)
            else:
                await self._produce_local(episode_id, manifest_path, out_dir, skip_render, no_upload, privacy)
        except Exception as exc:
            logger.exception("[%s] Production failed: %s", self.agent_id, exc)
            await self.publish("publish.failed", {"episode_id": episode_id, "stage": "unknown", "error": str(exc)})
        finally:
            self._producing = False
            await self.store.set("publish:active", None)

    async def _produce_local(
        self,
        episode_id: str,
        manifest_path: str,
        out_dir: str,
        skip_render: bool,
        no_upload: bool,
        privacy: str,
    ) -> None:
        loop = asyncio.get_event_loop()

        # Stage 1: TTS
        logger.info("[%s] Stage: TTS", self.agent_id)
        try:
            from aido.tts_generate import run as tts_run
            await loop.run_in_executor(
                None, lambda: tts_run(
                    episode_id=episode_id if not manifest_path else None,
                    manifest_path=manifest_path or None,
                    out_dir=out_dir,
                )
            )
            await self.publish("publish.tts.done", {"episode_id": episode_id})
        except Exception as exc:
            await self.publish("publish.failed", {"episode_id": episode_id, "stage": "tts", "error": str(exc)})
            raise

        # Stage 2: USD injection
        logger.info("[%s] Stage: USD inject", self.agent_id)
        try:
            from aido.inject_content import run as inject_run
            mp = manifest_path or str(Path(out_dir) / "manifest.json")
            await loop.run_in_executor(
                None, lambda: inject_run(episode_id=None, manifest_path=mp, out_dir=out_dir)
            )
        except Exception as exc:
            logger.warning("[%s] USD inject error (non-fatal): %s", self.agent_id, exc)

        # Stage 3: Render (optional)
        if not skip_render:
            logger.info("[%s] Stage: Omniverse render", self.agent_id)
            try:
                from aido.render_episode import render_headless
                master_usd = str(Path(out_dir) / "usd" / f"{episode_id}_master.usda")
                rc = await loop.run_in_executor(
                    None, lambda: render_headless(
                        master_usd=master_usd,
                        out_dir=str(Path(out_dir) / "frames"),
                    )
                )
                if rc != 0:
                    raise RuntimeError(f"Render exited with code {rc}")
                await self.publish("publish.render.done", {"episode_id": episode_id})
            except Exception as exc:
                await self.publish("publish.failed", {"episode_id": episode_id, "stage": "render", "error": str(exc)})
                raise

        # Stage 4: Assemble
        logger.info("[%s] Stage: Assemble", self.agent_id)
        try:
            from aido.assemble import run as assemble_run
            mp = manifest_path or str(Path(out_dir) / "manifest.json")
            final_mp4 = await loop.run_in_executor(
                None, lambda: assemble_run(
                    manifest_path=mp,
                    frames_dir=str(Path(out_dir) / "frames"),
                    out_dir=out_dir,
                )
            )
            await self.publish("publish.assemble.done", {"episode_id": episode_id, "mp4_path": final_mp4})
        except Exception as exc:
            await self.publish("publish.failed", {"episode_id": episode_id, "stage": "assemble", "error": str(exc)})
            raise

        # Stage 5: Upload
        if not no_upload:
            logger.info("[%s] Stage: Upload", self.agent_id)
            try:
                from aido.upload_youtube import run as yt_run
                mp = manifest_path or str(Path(out_dir) / "manifest.json")
                await loop.run_in_executor(None, lambda: yt_run(mp, None, privacy))
                await self.publish("publish.upload.done", {
                    "episode_id": episode_id,
                    "platforms": ["youtube"],
                })
            except Exception as exc:
                await self.publish("publish.failed", {"episode_id": episode_id, "stage": "upload", "error": str(exc)})
                raise

        await self.store.set(f"publish:done:{episode_id}", {"episode_id": episode_id, "completed_at": time.time()})
        logger.info("[%s] Production complete: %s", self.agent_id, episode_id)

    async def _produce_runpod(self, episode_id: str, manifest_path: str, out_dir: str, privacy: str) -> None:
        """Trigger RunPod deploy script via shell."""
        pod_ip = os.environ.get("RUNPOD_POD_IP", "")
        if not pod_ip:
            raise RuntimeError("RUNPOD_POD_IP not set in .env — needed for RunPod mode")

        script = Path(self.project_root) / "aido" / "deploy_to_runpod.sh"
        loop = asyncio.get_event_loop()

        def _run_shell():
            import subprocess
            result = subprocess.run(
                ["bash", str(script), pod_ip, episode_id],
                capture_output=False,
                cwd=self.project_root,
            )
            return result.returncode

        rc = await loop.run_in_executor(None, _run_shell)
        if rc != 0:
            raise RuntimeError(f"RunPod deploy script exited with code {rc}")

        await self.publish("publish.assemble.done", {"episode_id": episode_id})


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _build_manifest_from_draft(episode_id: str, vertical: str, draft: dict) -> dict:
    """Convert a NewsScout draft into a pipeline-compatible manifest."""
    import time as _time
    from datetime import datetime
    segments = []
    for i, seg in enumerate(draft.get("segments", [])):
        segments.append({
            "id": seg.get("id", f"seg_{i+1:02d}"),
            "type": seg.get("type", "headline"),
            "title": seg.get("title", f"Segment {i+1}"),
            "narration": seg.get("narration", ""),
            "duration_hint": 30.0,
            "b_roll_tags": [],
            "usd_overrides": {},
            "audio_path": "",
            "render_path": "",
        })
    return {
        "version": "1.0",
        "episode_id": episode_id,
        "title": draft.get("title", f"Mission Control — {vertical.title()} Briefing"),
        "subtitle": vertical.title(),
        "publish_date": datetime.utcnow().strftime("%Y-%m-%d"),
        "voice_id": "XjLkpWUlnhS8i7gGz3lZ",
        "scene_usd": "workspace/scenes/AIDO_TestScene_v0.1.usda",
        "segments": segments,
        "notion_page_id": "",
        "youtube_playlist_id": "",
        "output_dir": "",
        "final_mp4": "",
    }
