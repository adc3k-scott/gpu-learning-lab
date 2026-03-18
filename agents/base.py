"""
BaseAgent — abstract base class for all Mission Control agents.

Every agent:
  • Has a unique ID and role name
  • Connects to the shared EventBus and StateStore
  • Can subscribe to events, publish events, and execute skills
  • Has a structured lifecycle: start() → handle work → stop()
  • Persists its own status to the StateStore under "agents:<id>"

Usage:
    class MyAgent(BaseAgent):
        role = "my_agent"

        async def _setup(self) -> None:
            self.bus.subscribe("job.*", self._on_job)

        async def _on_job(self, event: Event) -> None:
            result = await self.run_skill("file_manager", {"action": "read", "path": "README.md"})
            await self.publish("job.done", {"result": result.output})

    agent = MyAgent(agent_id="my-1", bus=bus, store=store, registry=registry)
    await agent.start()
"""

from __future__ import annotations

import asyncio
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from uuid import uuid4

from core.circuit_breaker import CircuitBreaker, CircuitOpenError
from core.event_bus import Event, EventBus
from core.logging import set_log_context, clear_log_context
from core.metrics import metrics
from core.state_store import StateStore
from skills.base import SkillContext, SkillResult
from skills.registry import SkillRegistry

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Agent status
# ---------------------------------------------------------------------------


class AgentStatus(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    BUSY = "busy"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"


@dataclass
class AgentState:
    agent_id: str
    role: str
    status: AgentStatus = AgentStatus.IDLE
    current_job: str | None = None
    started_at: float = field(default_factory=time.time)
    last_heartbeat: float = field(default_factory=time.time)
    error: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    capabilities: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "role": self.role,
            "status": self.status.value,
            "current_job": self.current_job,
            "started_at": self.started_at,
            "last_heartbeat": self.last_heartbeat,
            "error": self.error,
            "metadata": self.metadata,
            "capabilities": self.capabilities,
        }


# ---------------------------------------------------------------------------
# Base class
# ---------------------------------------------------------------------------


class BaseAgent(ABC):
    """
    Abstract base class for Mission Control agents.

    Subclasses must implement _setup() and may override _teardown().
    All event handlers must be async coroutines.

    Class-level attributes:
        role            str        — logical role name, e.g. "coder", "repo_analyst"
        capabilities    list[str]  — skills/actions this agent can handle
    """

    role: str = "agent"
    capabilities: list[str] = []

    def __init__(
        self,
        *,
        agent_id: str | None = None,
        bus: EventBus,
        store: StateStore,
        registry: SkillRegistry,
        project_root: str = ".",
        heartbeat_interval: float = 30.0,
    ) -> None:
        self.agent_id = agent_id or f"{self.role}-{uuid4().hex[:8]}"
        self.bus = bus
        self.store = store
        self.registry = registry
        self.project_root = project_root
        self._heartbeat_interval = heartbeat_interval
        self._heartbeat_task: asyncio.Task | None = None
        self._state = AgentState(
            agent_id=self.agent_id, role=self.role,
            capabilities=list(self.capabilities),
        )
        self._running = False
        self._circuit_breakers: dict[str, CircuitBreaker] = {}

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def start(self) -> None:
        """Start the agent: run _setup(), begin heartbeat, update status."""
        logger.info("[%s] Starting agent (role=%s)", self.agent_id, self.role)
        self._running = True
        await self._set_status(AgentStatus.RUNNING)

        try:
            await self._setup()
        except Exception as exc:
            logger.exception("[%s] _setup() failed: %s", self.agent_id, exc)
            await self._set_status(AgentStatus.ERROR, error=str(exc))
            return

        self._heartbeat_task = asyncio.create_task(
            self._heartbeat_loop(), name=f"heartbeat-{self.agent_id}"
        )
        await self.publish("agent.started", {
            "role": self.role,
            "capabilities": self._state.capabilities,
        })
        logger.info("[%s] Agent started (capabilities=%s)", self.agent_id, self._state.capabilities)

    async def stop(self) -> None:
        """Gracefully stop the agent."""
        logger.info("[%s] Stopping agent", self.agent_id)
        self._running = False
        await self._set_status(AgentStatus.STOPPING)

        if self._heartbeat_task:
            self._heartbeat_task.cancel()
            try:
                await self._heartbeat_task
            except asyncio.CancelledError:
                pass

        try:
            await self._teardown()
        except Exception as exc:
            logger.warning("[%s] _teardown() error: %s", self.agent_id, exc)

        await self._set_status(AgentStatus.STOPPED)
        await self.publish("agent.stopped", {"role": self.role})
        logger.info("[%s] Agent stopped", self.agent_id)

    # ------------------------------------------------------------------
    # Abstract hooks
    # ------------------------------------------------------------------

    @abstractmethod
    async def _setup(self) -> None:
        """
        Called once during start().
        Subscribe to events and initialise resources here.
        """

    async def _teardown(self) -> None:
        """Called during stop(). Override to release resources."""

    # ------------------------------------------------------------------
    # Publishing helpers
    # ------------------------------------------------------------------

    async def publish(self, event_type: str, payload: dict[str, Any] | None = None) -> None:
        """Publish an event on the shared event bus."""
        await self.bus.publish(
            Event(
                event_type=event_type,
                payload=payload or {},
                source=self.agent_id,
            )
        )

    # ------------------------------------------------------------------
    # Skill execution
    # ------------------------------------------------------------------

    async def run_skill(
        self,
        skill_name: str,
        params: dict[str, Any],
        job_id: str = "",
        extra_metadata: dict[str, Any] | None = None,
    ) -> SkillResult:
        """
        Execute a registered skill and return its SkillResult.

        Automatically injects agent context (agent_id, job_id, project_root)
        into the SkillContext so skills have access to shared infrastructure.

        If the skill defines a retry_policy with max_attempts > 1, failed
        executions are retried with exponential backoff before giving up.
        """
        try:
            skill = self.registry.get(skill_name)
        except KeyError as exc:
            return SkillResult.fail(str(exc))

        # Circuit breaker check — fail fast if service is known-down
        cb = self._circuit_breakers.get(skill_name)
        if cb:
            try:
                # Just check state; don't wrap the call (retry loop needs control)
                if cb.state.value == "open":
                    retry_after = cb.cooldown_seconds - (time.time() - cb._opened_at)
                    metrics.increment(f"circuit.{skill_name}.rejected")
                    return SkillResult.fail(
                        f"Circuit breaker OPEN for '{skill_name}' — retry after {max(retry_after, 0):.0f}s"
                    )
            except Exception:
                pass  # circuit breaker should never block execution

        # Set logging correlation context for this skill execution
        set_log_context(agent_id=self.agent_id, job_id=job_id)

        ctx = SkillContext(
            agent_id=self.agent_id,
            job_id=job_id,
            state_store=self.store,
            event_bus=self.bus,
            metadata={"project_root": self.project_root, **(extra_metadata or {})},
        )

        policy = skill.retry_policy
        max_attempts = max(policy.max_attempts, 1)

        await self._set_status(AgentStatus.BUSY, job_id=job_id)
        metrics.increment("skills.executed")
        t0 = time.perf_counter()
        result = SkillResult.fail("skill did not execute")

        skill_timeout = policy.timeout if policy.timeout > 0 else None

        for attempt in range(1, max_attempts + 1):
            try:
                if skill_timeout:
                    result = await asyncio.wait_for(
                        skill.execute(ctx, params), timeout=skill_timeout
                    )
                else:
                    result = await skill.execute(ctx, params)
            except asyncio.TimeoutError:
                metrics.increment(f"skills.{skill_name}.timeout")
                logger.warning("[%s] Skill %r timed out after %.0fs (attempt %d/%d)",
                               self.agent_id, skill_name, skill_timeout, attempt, max_attempts)
                result = SkillResult.fail(
                    f"Skill '{skill_name}' timed out after {skill_timeout}s"
                )
            except Exception as exc:
                logger.exception("[%s] Skill %r raised (attempt %d/%d): %s",
                                 self.agent_id, skill_name, attempt, max_attempts, exc)
                result = SkillResult.fail(str(exc))

            if result.success or attempt == max_attempts:
                break

            # Retry eligible — exponential backoff
            if isinstance(result, SkillResult) and not result.success:
                delay = policy.backoff_base * (2 ** (attempt - 1))
                metrics.increment("skills.retried")
                logger.info("[%s] Retrying skill %r in %.1fs (attempt %d/%d)",
                            self.agent_id, skill_name, delay, attempt + 1, max_attempts)
                await asyncio.sleep(delay)

        elapsed_ms = (time.perf_counter() - t0) * 1000
        metrics.timing(f"skills.{skill_name}.duration_ms", elapsed_ms)
        metrics.timing("skills.all.duration_ms", elapsed_ms)

        # Update circuit breaker state
        if cb:
            if result.success:
                cb.record_success()
            else:
                cb.record_failure()

        if not result.success:
            metrics.increment("skills.failed")
            metrics.increment(f"skills.{skill_name}.failed")
        await self._set_status(AgentStatus.RUNNING)
        clear_log_context()

        return result

    # ------------------------------------------------------------------
    # State helpers
    # ------------------------------------------------------------------

    async def _set_status(
        self,
        status: AgentStatus,
        *,
        job_id: str | None = None,
        error: str = "",
    ) -> None:
        self._state.status = status
        if job_id is not None:
            self._state.current_job = job_id or None
        self._state.error = error
        self._state.last_heartbeat = time.time()
        await self.store.set(f"agents:{self.agent_id}", self._state.to_dict())

    async def get_state(self) -> AgentState:
        """Return a fresh copy of this agent's persisted state."""
        raw = await self.store.get(f"agents:{self.agent_id}")
        if raw:
            self._state.status = AgentStatus(raw.get("status", "idle"))
            self._state.current_job = raw.get("current_job")
            self._state.last_heartbeat = raw.get("last_heartbeat", time.time())
        return self._state

    # ------------------------------------------------------------------
    # Heartbeat
    # ------------------------------------------------------------------

    async def _heartbeat_loop(self) -> None:
        while self._running:
            try:
                await asyncio.sleep(self._heartbeat_interval)
                self._state.last_heartbeat = time.time()
                await self.store.set(f"agents:{self.agent_id}", self._state.to_dict())
                logger.debug("[%s] Heartbeat", self.agent_id)
            except asyncio.CancelledError:
                break
            except Exception as exc:
                logger.warning("[%s] Heartbeat error: %s", self.agent_id, exc)

    def __repr__(self) -> str:
        return f"<Agent {self.role!r} id={self.agent_id} status={self._state.status.value}>"
