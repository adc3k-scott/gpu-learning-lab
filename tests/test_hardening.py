"""Tests for production hardening: skill timeouts, graceful shutdown, circuit breakers."""

import asyncio
import time
import pytest

from core.circuit_breaker import CircuitBreaker, CircuitOpenError, CircuitState
from core.event_bus import EventBus
from core.state_store import StateStore
from agents.base import BaseAgent, AgentStatus
from agents.orchestrator.agent import OrchestratorAgent
from agents.orchestrator.job import Job, JobStatus, Step, StepStatus
from skills.base import BaseSkill, RetryPolicy, SkillContext, SkillResult
from skills.registry import SkillRegistry


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
async def infra():
    bus = EventBus(); store = StateStore()
    await bus.connect(); await store.connect()
    reg = SkillRegistry(); reg.discover()
    yield bus, store, reg
    await bus.disconnect()


class StubAgent(BaseAgent):
    role = "stub"
    async def _setup(self):
        pass


# ---------------------------------------------------------------------------
# Skill timeout tests
# ---------------------------------------------------------------------------

class _SlowSkill(BaseSkill):
    """Skill that sleeps longer than its timeout."""
    name = "slow_skill"
    description = "takes too long"
    retry_policy = RetryPolicy(max_attempts=1, timeout=0.1)

    async def execute(self, ctx: SkillContext, params: dict) -> SkillResult:
        await asyncio.sleep(5.0)  # way longer than 0.1s timeout
        return SkillResult.ok({"done": True})


class _FastSkill(BaseSkill):
    """Skill that completes well within timeout."""
    name = "fast_skill"
    description = "quick"
    retry_policy = RetryPolicy(max_attempts=1, timeout=10.0)

    async def execute(self, ctx: SkillContext, params: dict) -> SkillResult:
        return SkillResult.ok({"fast": True})


class _NoTimeoutSkill(BaseSkill):
    """Skill with timeout disabled (0)."""
    name = "no_timeout_skill"
    description = "no timeout"
    retry_policy = RetryPolicy(max_attempts=1, timeout=0)

    async def execute(self, ctx: SkillContext, params: dict) -> SkillResult:
        return SkillResult.ok({"ok": True})


class TestSkillTimeout:
    async def test_slow_skill_times_out(self, infra):
        """Skill exceeding timeout should return failure."""
        bus, store, reg = infra
        reg._skills["slow_skill"] = _SlowSkill()

        agent = StubAgent(bus=bus, store=store, registry=reg)
        await agent.start()

        result = await agent.run_skill("slow_skill", {})
        assert result.success is False
        assert "timed out" in result.error

        await agent.stop()

    async def test_fast_skill_succeeds_within_timeout(self, infra):
        """Skill completing within timeout should succeed normally."""
        bus, store, reg = infra
        reg._skills["fast_skill"] = _FastSkill()

        agent = StubAgent(bus=bus, store=store, registry=reg)
        await agent.start()

        result = await agent.run_skill("fast_skill", {})
        assert result.success is True
        assert result.output["fast"] is True

        await agent.stop()

    async def test_zero_timeout_means_no_limit(self, infra):
        """Timeout of 0 should disable timeout enforcement."""
        bus, store, reg = infra
        reg._skills["no_timeout_skill"] = _NoTimeoutSkill()

        agent = StubAgent(bus=bus, store=store, registry=reg)
        await agent.start()

        result = await agent.run_skill("no_timeout_skill", {})
        assert result.success is True

        await agent.stop()

    async def test_timeout_with_retry(self, infra):
        """Timeout on first attempt should allow retry if configured."""
        bus, store, reg = infra

        class _SlowThenFast(BaseSkill):
            name = "slow_then_fast"
            description = "slow first, fast second"
            retry_policy = RetryPolicy(max_attempts=2, backoff_base=0.01, timeout=0.1)

            def __init__(self):
                self._calls = 0

            async def execute(self, ctx, params):
                self._calls += 1
                if self._calls == 1:
                    await asyncio.sleep(5.0)  # timeout
                return SkillResult.ok({"attempt": self._calls})

        skill = _SlowThenFast()
        reg._skills[skill.name] = skill

        agent = StubAgent(bus=bus, store=store, registry=reg)
        await agent.start()

        result = await agent.run_skill("slow_then_fast", {})
        assert result.success is True
        assert skill._calls == 2

        await agent.stop()


# ---------------------------------------------------------------------------
# Graceful shutdown / job persistence tests
# ---------------------------------------------------------------------------

class TestGracefulShutdown:
    def _make_orchestrator(self, bus, store, reg):
        return OrchestratorAgent(
            agent_id="orch-shutdown", bus=bus, store=store, registry=reg
        )

    async def test_persist_active_jobs(self, infra):
        """persist_active_jobs should save running jobs to the store."""
        bus, store, reg = infra
        orch = self._make_orchestrator(bus, store, reg)
        await orch.start()

        # Create a running job
        job = Job(title="active", description="in progress")
        job.status = JobStatus.RUNNING
        orch._jobs[job.job_id] = job

        count = await orch.persist_active_jobs()
        assert count == 1

        # Verify it's in the store
        stored = await store.get(f"jobs:{job.job_id}")
        assert stored is not None
        assert stored["status"] == "running"

        await orch.stop()

    async def test_persist_skips_completed_jobs(self, infra):
        """persist_active_jobs should not re-persist completed jobs."""
        bus, store, reg = infra
        orch = self._make_orchestrator(bus, store, reg)
        await orch.start()

        job = Job(title="done", description="finished")
        job.status = JobStatus.COMPLETED
        orch._jobs[job.job_id] = job

        count = await orch.persist_active_jobs()
        assert count == 0

        await orch.stop()

    async def test_recover_jobs_from_store(self, infra):
        """recover_jobs should reload incomplete jobs from the store."""
        bus, store, reg = infra
        orch = self._make_orchestrator(bus, store, reg)
        await orch.start()

        # Simulate a prior-session job in the store
        job_data = {
            "job_id": "recovered-123",
            "title": "prior session job",
            "description": "was running when server died",
            "status": "running",
            "created_at": time.time() - 60,
            "started_at": time.time() - 60,
            "finished_at": None,
            "requested_by": "user",
            "error": "",
            "steps": [
                {
                    "step_id": "s1",
                    "name": "step_one",
                    "description": "first step",
                    "assigned_role": "coder",
                    "skill": "file_manager",
                    "params": {},
                    "depends_on": [],
                    "status": "completed",
                    "result": "done",
                    "error": "",
                    "started_at": None,
                    "finished_at": None,
                    "attempts": 1,
                    "max_attempts": 2,
                },
            ],
            "metadata": {},
        }
        await store.set("jobs:recovered-123", job_data)

        count = await orch.recover_jobs()
        assert count == 1
        assert "recovered-123" in orch._jobs
        recovered = orch._jobs["recovered-123"]
        assert recovered.title == "prior session job"
        assert recovered.status == JobStatus.RUNNING
        assert len(recovered.steps) == 1

        await orch.stop()

    async def test_recover_skips_completed(self, infra):
        """recover_jobs should not reload completed jobs."""
        bus, store, reg = infra
        orch = self._make_orchestrator(bus, store, reg)
        await orch.start()

        await store.set("jobs:done-456", {
            "job_id": "done-456",
            "title": "old completed",
            "description": "finished",
            "status": "completed",
            "created_at": time.time(),
            "steps": [],
            "metadata": {},
        })

        count = await orch.recover_jobs()
        assert count == 0
        assert "done-456" not in orch._jobs

        await orch.stop()

    async def test_recover_skips_already_loaded(self, infra):
        """recover_jobs should not duplicate jobs already in memory."""
        bus, store, reg = infra
        orch = self._make_orchestrator(bus, store, reg)
        await orch.start()

        # Job already in memory
        job = Job(job_id="existing-789", title="already here", description="test")
        job.status = JobStatus.RUNNING
        orch._jobs[job.job_id] = job

        # Same job in store
        await store.set("jobs:existing-789", {
            "job_id": "existing-789", "title": "already here",
            "description": "test", "status": "running",
            "created_at": time.time(), "steps": [], "metadata": {},
        })

        count = await orch.recover_jobs()
        assert count == 0  # not duplicated

        await orch.stop()


# ---------------------------------------------------------------------------
# Job/Step from_dict round-trip tests
# ---------------------------------------------------------------------------

class TestFromDict:
    def test_step_round_trip(self):
        """Step.to_dict() → Step.from_dict() should preserve all fields."""
        step = Step(
            name="analyze", description="run analysis",
            assigned_role="repo_analyst", skill="file_manager",
            params={"action": "read", "path": "README.md"},
            depends_on=["abc123"],
        )
        step.start()
        step.complete({"lines": 42})

        restored = Step.from_dict(step.to_dict())
        assert restored.step_id == step.step_id
        assert restored.name == "analyze"
        assert restored.status == StepStatus.COMPLETED
        assert restored.result == {"lines": 42}
        assert restored.depends_on == ["abc123"]
        assert restored.attempts == 1

    def test_job_round_trip(self):
        """Job.to_dict() → Job.from_dict() should preserve all fields."""
        job = Job(title="test job", description="desc", requested_by="scott")
        job.add_step(Step(name="s1", assigned_role="coder", skill="file_manager"))
        job.start()

        restored = Job.from_dict(job.to_dict())
        assert restored.job_id == job.job_id
        assert restored.title == "test job"
        assert restored.status == JobStatus.RUNNING
        assert len(restored.steps) == 1
        assert restored.steps[0].name == "s1"

    def test_job_from_dict_with_empty_steps(self):
        """Job with no steps should round-trip cleanly."""
        job = Job(title="empty", description="no steps")
        restored = Job.from_dict(job.to_dict())
        assert restored.steps == []
        assert restored.status == JobStatus.PENDING


# ---------------------------------------------------------------------------
# Circuit breaker tests
# ---------------------------------------------------------------------------

class TestCircuitBreaker:
    def test_starts_closed(self):
        cb = CircuitBreaker("test")
        assert cb.state == CircuitState.CLOSED
        assert cb.failure_count == 0

    def test_stays_closed_below_threshold(self):
        cb = CircuitBreaker("test", failure_threshold=5)
        for _ in range(4):
            cb.record_failure()
        assert cb.state == CircuitState.CLOSED

    def test_opens_at_threshold(self):
        cb = CircuitBreaker("test", failure_threshold=3)
        for _ in range(3):
            cb.record_failure()
        assert cb.state == CircuitState.OPEN

    def test_open_transitions_to_half_open_after_cooldown(self):
        cb = CircuitBreaker("test", failure_threshold=1, cooldown_seconds=0.1)
        cb.record_failure()
        assert cb.state == CircuitState.OPEN

        time.sleep(0.15)
        assert cb.state == CircuitState.HALF_OPEN

    def test_half_open_success_closes(self):
        cb = CircuitBreaker("test", failure_threshold=1, cooldown_seconds=0.01)
        cb.record_failure()
        time.sleep(0.02)
        assert cb.state == CircuitState.HALF_OPEN

        cb.record_success()
        assert cb.state == CircuitState.CLOSED
        assert cb.failure_count == 0

    def test_half_open_failure_reopens(self):
        cb = CircuitBreaker("test", failure_threshold=1, cooldown_seconds=0.01)
        cb.record_failure()
        time.sleep(0.02)
        assert cb.state == CircuitState.HALF_OPEN

        cb.record_failure()
        assert cb.state == CircuitState.OPEN

    def test_reset(self):
        cb = CircuitBreaker("test", failure_threshold=1)
        cb.record_failure()
        assert cb.state == CircuitState.OPEN
        cb.reset()
        assert cb.state == CircuitState.CLOSED

    async def test_call_success(self):
        cb = CircuitBreaker("test")

        async def ok():
            return 42

        result = await cb.call(ok())
        assert result == 42
        assert cb.state == CircuitState.CLOSED

    async def test_call_failure_increments(self):
        cb = CircuitBreaker("test", failure_threshold=3)

        async def fail():
            raise RuntimeError("boom")

        with pytest.raises(RuntimeError):
            await cb.call(fail())
        assert cb.failure_count == 1

    async def test_call_rejects_when_open(self):
        cb = CircuitBreaker("test", failure_threshold=1, cooldown_seconds=60)
        cb.record_failure()  # opens circuit

        async def noop():
            return "should not run"

        with pytest.raises(CircuitOpenError) as exc_info:
            await cb.call(noop())
        assert "OPEN" in str(exc_info.value)

    def test_to_dict(self):
        cb = CircuitBreaker("runpod", failure_threshold=5, cooldown_seconds=30)
        d = cb.to_dict()
        assert d["name"] == "runpod"
        assert d["state"] == "closed"
        assert d["failure_threshold"] == 5

    async def test_circuit_breaker_in_run_skill(self, infra):
        """run_skill should fail fast when circuit breaker is open."""
        bus, store, reg = infra
        agent = StubAgent(bus=bus, store=store, registry=reg)
        await agent.start()

        # Install a circuit breaker for file_manager and open it
        cb = CircuitBreaker("file_manager", failure_threshold=1, cooldown_seconds=60)
        cb.record_failure()  # opens it
        agent._circuit_breakers["file_manager"] = cb

        result = await agent.run_skill("file_manager", {"action": "exists", "path": "."})
        assert result.success is False
        assert "Circuit breaker OPEN" in result.error

        await agent.stop()

    async def test_run_skill_records_to_circuit_breaker(self, infra):
        """run_skill should record success/failure to circuit breaker."""
        bus, store, reg = infra
        agent = StubAgent(bus=bus, store=store, registry=reg)
        await agent.start()

        cb = CircuitBreaker("file_manager", failure_threshold=10)
        agent._circuit_breakers["file_manager"] = cb

        # Successful call
        await agent.run_skill("file_manager", {"action": "exists", "path": "."})
        assert cb.failure_count == 0  # success resets count

        # Failing call
        await agent.run_skill("file_manager", {"action": "read", "path": "nonexistent_xyz.txt"})
        assert cb.failure_count == 1

        await agent.stop()
