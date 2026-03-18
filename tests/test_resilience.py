"""Tests for production resilience: job cleanup, skill retry, event sequence + replay."""

import asyncio
import time
import pytest

from core.event_bus import Event, EventBus
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
# Job cleanup tests
# ---------------------------------------------------------------------------

class TestJobCleanup:
    def _make_orchestrator(self, bus, store, reg):
        return OrchestratorAgent(
            agent_id="orch-cleanup", bus=bus, store=store, registry=reg
        )

    async def test_expired_jobs_removed(self, infra):
        """Jobs older than 1 hour in terminal state should be purged."""
        bus, store, reg = infra
        orch = self._make_orchestrator(bus, store, reg)
        await orch.start()

        # Create a completed job that looks 2 hours old
        job = Job(title="old-job", description="test")
        job.status = JobStatus.COMPLETED
        job.created_at = time.time() - 7200
        job.finished_at = time.time() - 7200
        orch._jobs[job.job_id] = job

        assert job.job_id in orch._jobs
        await orch._cleanup_jobs()
        assert job.job_id not in orch._jobs

        await orch.stop()

    async def test_recent_completed_jobs_kept(self, infra):
        """Completed jobs younger than 1 hour should NOT be purged."""
        bus, store, reg = infra
        orch = self._make_orchestrator(bus, store, reg)
        await orch.start()

        job = Job(title="recent-job", description="test")
        job.status = JobStatus.COMPLETED
        job.finished_at = time.time() - 60  # 1 minute ago

        orch._jobs[job.job_id] = job
        await orch._cleanup_jobs()
        assert job.job_id in orch._jobs

        await orch.stop()

    async def test_running_jobs_never_cleaned(self, infra):
        """Running jobs should never be cleaned, regardless of age."""
        bus, store, reg = infra
        orch = self._make_orchestrator(bus, store, reg)
        await orch.start()

        job = Job(title="active-job", description="test")
        job.status = JobStatus.RUNNING
        job.created_at = time.time() - 7200  # 2 hours old but still running

        orch._jobs[job.job_id] = job
        await orch._cleanup_jobs()
        assert job.job_id in orch._jobs

        await orch.stop()

    async def test_failed_jobs_cleaned(self, infra):
        """Failed jobs older than 1 hour should also be purged."""
        bus, store, reg = infra
        orch = self._make_orchestrator(bus, store, reg)
        await orch.start()

        job = Job(title="failed-old", description="test")
        job.status = JobStatus.FAILED
        job.created_at = time.time() - 7200
        job.finished_at = time.time() - 7200

        orch._jobs[job.job_id] = job
        await orch._cleanup_jobs()
        assert job.job_id not in orch._jobs

        await orch.stop()

    async def test_cleanup_also_removes_waiters(self, infra):
        """Job waiters should be cleaned up along with the job."""
        bus, store, reg = infra
        orch = self._make_orchestrator(bus, store, reg)
        await orch.start()

        job = Job(title="waiter-job", description="test")
        job.status = JobStatus.COMPLETED
        job.created_at = time.time() - 7200
        job.finished_at = time.time() - 7200

        orch._jobs[job.job_id] = job
        orch._job_waiters[job.job_id] = [asyncio.Queue()]

        await orch._cleanup_jobs()
        assert job.job_id not in orch._jobs
        assert job.job_id not in orch._job_waiters

        await orch.stop()


# ---------------------------------------------------------------------------
# Skill retry tests
# ---------------------------------------------------------------------------

class _FlakeySkill(BaseSkill):
    """Skill that fails N times then succeeds."""
    name = "flakey"
    description = "test skill"
    retry_policy = RetryPolicy(max_attempts=3, backoff_base=0.01)

    def __init__(self, fail_count: int = 2):
        self._fail_count = fail_count
        self._attempts = 0

    async def execute(self, ctx: SkillContext, params: dict) -> SkillResult:
        self._attempts += 1
        if self._attempts <= self._fail_count:
            return SkillResult.fail(f"attempt {self._attempts} failed")
        return SkillResult.ok({"value": "recovered"})


class _AlwaysFailSkill(BaseSkill):
    """Skill that always fails."""
    name = "always_fail"
    description = "always fails"
    retry_policy = RetryPolicy(max_attempts=3, backoff_base=0.01)

    async def execute(self, ctx: SkillContext, params: dict) -> SkillResult:
        return SkillResult.fail("permanent failure")


class _ExceptionSkill(BaseSkill):
    """Skill that raises exceptions."""
    name = "exploder"
    description = "raises"
    retry_policy = RetryPolicy(max_attempts=2, backoff_base=0.01)

    def __init__(self):
        self._attempts = 0

    async def execute(self, ctx: SkillContext, params: dict) -> SkillResult:
        self._attempts += 1
        if self._attempts == 1:
            raise RuntimeError("boom")
        return SkillResult.ok({"recovered": True})


class TestSkillRetry:
    async def test_retry_recovers_on_third_attempt(self, infra):
        """Flakey skill should succeed after 2 failures with 3 max_attempts."""
        bus, store, reg = infra
        skill = _FlakeySkill(fail_count=2)
        reg._skills[skill.name] = skill

        agent = StubAgent(bus=bus, store=store, registry=reg)
        await agent.start()

        result = await agent.run_skill("flakey", {})
        assert result.success is True
        assert result.output["value"] == "recovered"
        assert skill._attempts == 3

        await agent.stop()

    async def test_retry_exhaustion_returns_failure(self, infra):
        """Skill that always fails should exhaust retries and return failure."""
        bus, store, reg = infra
        skill = _AlwaysFailSkill()
        reg._skills[skill.name] = skill

        agent = StubAgent(bus=bus, store=store, registry=reg)
        await agent.start()

        result = await agent.run_skill("always_fail", {})
        assert result.success is False
        assert "permanent failure" in result.error

        await agent.stop()

    async def test_exception_caught_and_retried(self, infra):
        """Skill that raises should be caught and retried."""
        bus, store, reg = infra
        skill = _ExceptionSkill()
        reg._skills[skill.name] = skill

        agent = StubAgent(bus=bus, store=store, registry=reg)
        await agent.start()

        result = await agent.run_skill("exploder", {})
        assert result.success is True
        assert skill._attempts == 2

        await agent.stop()

    async def test_no_retry_on_success(self, infra):
        """Skill that succeeds on first attempt should not retry."""
        bus, store, reg = infra
        skill = _FlakeySkill(fail_count=0)
        reg._skills[skill.name] = skill

        agent = StubAgent(bus=bus, store=store, registry=reg)
        await agent.start()

        result = await agent.run_skill("flakey", {})
        assert result.success is True
        assert skill._attempts == 1

        await agent.stop()

    async def test_agent_status_busy_during_skill(self, infra):
        """Agent should be BUSY during skill execution, RUNNING after."""
        bus, store, reg = infra
        agent = StubAgent(bus=bus, store=store, registry=reg)
        await agent.start()

        # After run_skill completes, agent should be back to RUNNING
        await agent.run_skill("file_manager", {"action": "exists", "path": "."})
        state = await agent.get_state()
        assert state.status == AgentStatus.RUNNING

        await agent.stop()


# ---------------------------------------------------------------------------
# Event sequence + replay buffer tests
# ---------------------------------------------------------------------------

class TestEventSequence:
    async def test_events_get_sequence_numbers(self):
        """Published events should receive monotonically increasing sequence numbers."""
        bus = EventBus()
        await bus.connect()

        e1 = Event(event_type="a")
        e2 = Event(event_type="b")
        e3 = Event(event_type="c")

        await bus.publish(e1)
        await bus.publish(e2)
        await bus.publish(e3)

        assert e1.sequence == 1
        assert e2.sequence == 2
        assert e3.sequence == 3

        await bus.disconnect()

    async def test_last_sequence_property(self):
        """last_sequence should track the highest assigned sequence."""
        bus = EventBus()
        await bus.connect()

        assert bus.last_sequence == 0
        await bus.publish(Event(event_type="x"))
        assert bus.last_sequence == 1
        await bus.publish(Event(event_type="y"))
        assert bus.last_sequence == 2

        await bus.disconnect()

    async def test_replay_since_returns_missed_events(self):
        """replay_since(N) should return events with sequence > N."""
        bus = EventBus()
        await bus.connect()

        for i in range(5):
            await bus.publish(Event(event_type=f"evt.{i}"))

        missed = bus.replay_since(3)
        assert len(missed) == 2
        assert missed[0].sequence == 4
        assert missed[1].sequence == 5
        assert missed[0].event_type == "evt.3"
        assert missed[1].event_type == "evt.4"

        await bus.disconnect()

    async def test_replay_since_zero_returns_all(self):
        """replay_since(0) should return all buffered events."""
        bus = EventBus()
        await bus.connect()

        for i in range(3):
            await bus.publish(Event(event_type=f"e.{i}"))

        missed = bus.replay_since(0)
        assert len(missed) == 3

        await bus.disconnect()

    async def test_replay_since_future_returns_empty(self):
        """replay_since with a sequence beyond current should return empty."""
        bus = EventBus()
        await bus.connect()

        await bus.publish(Event(event_type="x"))
        missed = bus.replay_since(999)
        assert missed == []

        await bus.disconnect()

    async def test_replay_buffer_bounded(self):
        """Buffer should not grow beyond _REPLAY_BUFFER_SIZE."""
        bus = EventBus()
        await bus.connect()

        for i in range(300):
            await bus.publish(Event(event_type=f"flood.{i}"))

        # Buffer is bounded to 200
        assert len(bus._replay_buffer) == bus._REPLAY_BUFFER_SIZE

        # replay_since(0) returns only what's in the buffer
        all_events = bus.replay_since(0)
        assert len(all_events) == bus._REPLAY_BUFFER_SIZE
        # Oldest buffered event should be sequence 101 (events 1-100 evicted)
        assert all_events[0].sequence == 101

        await bus.disconnect()

    async def test_sequence_survives_across_events(self):
        """Sequence numbers should be unique across different event types."""
        bus = EventBus()
        await bus.connect()

        await bus.publish(Event(event_type="job.created"))
        await bus.publish(Event(event_type="step.completed"))
        await bus.publish(Event(event_type="agent.started"))

        replay = bus.replay_since(0)
        sequences = [e.sequence for e in replay]
        assert sequences == [1, 2, 3]
        assert len(set(sequences)) == 3  # all unique

        await bus.disconnect()
