"""
UIAgent — maintains live dashboard state for the Mission Control web interface.

Subscribes to every event on the bus, keeps an in-memory snapshot of:
  • All agent statuses
  • Recent jobs (last 50)
  • Infrastructure health
  • Recent event log (last 100 events)

The FastAPI SSE endpoint reads from UIAgent.snapshot() to push updates
to connected browsers without polling.

Event contract
--------------
Listens on:  *   (all events)
Emits:       ui.snapshot  (debounced, ~500 ms after last change)
"""

from __future__ import annotations

import asyncio
import logging
import time
from collections import deque
from typing import Any

from agents.base import BaseAgent
from core.event_bus import Event

logger = logging.getLogger(__name__)

_MAX_JOBS   = 50
_MAX_EVENTS = 100
_DEBOUNCE_S = 0.4   # merge rapid bursts before emitting ui.snapshot


class UIAgent(BaseAgent):
    role = "ui"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._agents:  dict[str, dict] = {}
        self._jobs:    dict[str, dict] = {}
        self._infra:   dict[str, Any]  = {}
        self._log:     deque[dict]     = deque(maxlen=_MAX_EVENTS)
        self._dirty    = False
        self._debounce_task: asyncio.Task | None = None
        # SSE subscribers: list of asyncio.Queue, one per open browser tab
        self._sse_queues: list[asyncio.Queue] = []

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def _setup(self) -> None:
        self.bus.subscribe("*", self._on_any_event)
        # Bootstrap: pull existing agent + job state from the store
        await self._bootstrap()
        logger.info("[%s] UIAgent ready — listening to all events", self.agent_id)

    async def _bootstrap(self) -> None:
        """Load pre-existing agents and jobs from the state store on startup."""
        agent_entries = await self.store.get_all("agents:*")
        for data in agent_entries.values():
            role = data.get("role", "")
            if role:
                self._agents[role] = data

        job_entries = await self.store.get_all("jobs:*")
        for data in job_entries.values():
            job_id = data.get("job_id", "")
            if job_id:
                self._jobs[job_id] = {
                    "job_id":     job_id,
                    "title":      data.get("title", ""),
                    "status":     data.get("status", ""),
                    "updated_at": data.get("finished_at") or data.get("started_at") or "",
                    "steps":      data.get("steps", []),
                }

        cached_infra = await self.store.get("infra:health")
        if cached_infra:
            self._infra = cached_infra

    async def _teardown(self) -> None:
        if self._debounce_task:
            self._debounce_task.cancel()

    # ------------------------------------------------------------------
    # Event handler — catches everything
    # ------------------------------------------------------------------

    async def _on_any_event(self, event: Event) -> None:
        t = event.event_type

        # Update structured state based on event type
        if t == "agent.started" or t == "agent.stopped":
            role = event.payload.get("role", event.source)
            self._agents[role] = {
                "role": role,
                "agent_id": event.source,
                "status": "running" if t == "agent.started" else "stopped",
                "last_seen": event.timestamp,
            }

        elif t.startswith("job."):
            job_id = event.payload.get("job_id", "")
            if job_id:
                if job_id not in self._jobs:
                    self._jobs[job_id] = {"job_id": job_id}
                self._jobs[job_id].update({
                    "status": t.split(".")[-1],   # created/started/completed/failed
                    "title": event.payload.get("title", self._jobs[job_id].get("title", "")),
                    "updated_at": event.timestamp,
                })
                if t == "job.completed":
                    self._jobs[job_id]["results"] = event.payload.get("results", {})
                if t == "job.failed":
                    self._jobs[job_id]["error"] = event.payload.get("error", "")
                # Trim to last N jobs
                if len(self._jobs) > _MAX_JOBS:
                    oldest = sorted(self._jobs.values(), key=lambda j: j.get("updated_at", ""))[0]
                    self._jobs.pop(oldest["job_id"], None)

        elif t == "infra.report":
            self._infra = event.payload

        # Always append to event log
        self._log.append({
            "event_type": t,
            "source": event.source,
            "timestamp": event.timestamp,
            "preview": str(event.payload)[:120],
        })

        self._schedule_snapshot()

    # ------------------------------------------------------------------
    # Snapshot
    # ------------------------------------------------------------------

    def snapshot(self) -> dict[str, Any]:
        """Return the current dashboard state dict."""
        return {
            "timestamp": time.time(),
            "agents": list(self._agents.values()),
            "jobs": sorted(
                self._jobs.values(),
                key=lambda j: j.get("updated_at", ""),
                reverse=True,
            )[:_MAX_JOBS],
            "infra": self._infra,
            "events": list(self._log),
        }

    # ------------------------------------------------------------------
    # SSE subscriber management
    # ------------------------------------------------------------------

    def add_sse_subscriber(self) -> asyncio.Queue:
        q: asyncio.Queue = asyncio.Queue(maxsize=20)
        self._sse_queues.append(q)
        return q

    def remove_sse_subscriber(self, q: asyncio.Queue) -> None:
        try:
            self._sse_queues.remove(q)
        except ValueError:
            pass

    # ------------------------------------------------------------------
    # Debounced snapshot push
    # ------------------------------------------------------------------

    def _schedule_snapshot(self) -> None:
        if self._debounce_task and not self._debounce_task.done():
            self._debounce_task.cancel()
        self._debounce_task = asyncio.create_task(self._emit_snapshot())

    async def _emit_snapshot(self) -> None:
        try:
            await asyncio.sleep(_DEBOUNCE_S)
            snap = self.snapshot()
            await self.publish("ui.snapshot", snap)
            # Push to all SSE queues (drop if full — browser will catch up on next event)
            import json
            data = json.dumps(snap)
            for q in list(self._sse_queues):
                try:
                    q.put_nowait(data)
                except asyncio.QueueFull:
                    pass
        except asyncio.CancelledError:
            pass
