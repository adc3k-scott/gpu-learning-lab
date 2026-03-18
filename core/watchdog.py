"""
Agent watchdog — detects stalled agents and emits alerts.

Runs as a background asyncio task, checking agent heartbeats against
a configurable staleness threshold. When an agent's heartbeat exceeds
the threshold, the watchdog:
  1. Emits an "agent.stalled" event on the event bus
  2. Increments a metric counter
  3. Logs a warning

Usage in main.py lifespan:
    from core.watchdog import AgentWatchdog
    watchdog = AgentWatchdog(bus=bus, store=store, agents=_ALL_AGENTS)
    await watchdog.start()
    ...
    await watchdog.stop()
"""

from __future__ import annotations

import asyncio
import logging
import time
from typing import TYPE_CHECKING

from core.event_bus import Event
from core.metrics import metrics

if TYPE_CHECKING:
    from agents.base import BaseAgent
    from core.event_bus import EventBus
    from core.state_store import StateStore

logger = logging.getLogger(__name__)

# Default: agent is "stalled" if no heartbeat for 90 seconds (3x the 30s default interval)
_DEFAULT_STALE_THRESHOLD = 90.0
_DEFAULT_CHECK_INTERVAL = 30.0


class AgentWatchdog:
    """Background task that monitors agent heartbeat freshness."""

    def __init__(
        self,
        *,
        bus: "EventBus",
        store: "StateStore",
        agents: list["BaseAgent"],
        stale_threshold: float = _DEFAULT_STALE_THRESHOLD,
        check_interval: float = _DEFAULT_CHECK_INTERVAL,
    ):
        self._bus = bus
        self._store = store
        self._agents = agents
        self._stale_threshold = stale_threshold
        self._check_interval = check_interval
        self._task: asyncio.Task | None = None
        self._running = False
        self._stalled_agents: set[str] = set()  # track which are currently stalled

    async def start(self) -> None:
        self._running = True
        self._task = asyncio.create_task(self._check_loop(), name="agent-watchdog")
        logger.info("AgentWatchdog started (threshold=%.0fs, interval=%.0fs)",
                     self._stale_threshold, self._check_interval)

    async def stop(self) -> None:
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("AgentWatchdog stopped")

    async def _check_loop(self) -> None:
        while self._running:
            try:
                await asyncio.sleep(self._check_interval)
                await self._check_agents()
            except asyncio.CancelledError:
                break
            except Exception as exc:
                logger.warning("Watchdog check error: %s", exc)

    async def _check_agents(self) -> None:
        now = time.time()
        running_count = 0
        stalled_count = 0

        for agent in self._agents:
            state = await agent.get_state()

            # Only check agents that should be running
            if state.status.value in ("stopped", "idle"):
                continue

            running_count += 1
            age = now - state.last_heartbeat

            if age > self._stale_threshold:
                stalled_count += 1

                # Only alert once per stall (not every check cycle)
                if agent.agent_id not in self._stalled_agents:
                    self._stalled_agents.add(agent.agent_id)
                    metrics.increment("agents.stalled")
                    logger.warning(
                        "Agent %s (%s) stalled — last heartbeat %.0fs ago",
                        agent.agent_id, agent.role, age,
                    )
                    await self._bus.publish(Event(
                        event_type="agent.stalled",
                        payload={
                            "agent_id": agent.agent_id,
                            "role": agent.role,
                            "last_heartbeat": state.last_heartbeat,
                            "stale_seconds": round(age, 1),
                        },
                        source="watchdog",
                    ))
            else:
                # Agent recovered — clear stall flag
                if agent.agent_id in self._stalled_agents:
                    self._stalled_agents.discard(agent.agent_id)
                    logger.info("Agent %s (%s) recovered from stall", agent.agent_id, agent.role)
                    metrics.increment("agents.recovered")

        metrics.gauge("agents.running", running_count)
        metrics.gauge("agents.stalled_current", stalled_count)

    @property
    def stalled_agents(self) -> set[str]:
        """Return IDs of currently stalled agents."""
        return set(self._stalled_agents)
