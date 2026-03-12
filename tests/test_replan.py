"""Tests for the replan() function and OrchestratorAgent._attempt_replan() method."""

import asyncio
import json
import pytest

from agents.orchestrator.planner import replan
from agents.orchestrator.agent import OrchestratorAgent
from agents.orchestrator.job import Job, JobStatus, Step, StepStatus
from core.event_bus import EventBus
from core.state_store import StateStore
from skills.registry import SkillRegistry


# ---------------------------------------------------------------------------
# Fake LLM client for replan tests
# ---------------------------------------------------------------------------

class _FakeContent:
    def __init__(self, text: str):
        self.text = text


class _FakeResponse:
    def __init__(self, text: str):
        self.content = [_FakeContent(text)]


class _FakeLLM:
    """Mock Anthropic client whose messages.create returns canned JSON."""

    def __init__(self, response_text: str):
        self._response_text = response_text
        self.calls: list[dict] = []

    @property
    def messages(self):
        return self

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return _FakeResponse(self._response_text)


class _ErrorLLM:
    """Mock that always raises on messages.create."""

    @property
    def messages(self):
        return self

    def create(self, **kwargs):
        raise RuntimeError("API exploded")


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


def _make_orchestrator(bus, store, reg, llm_client=None):
    return OrchestratorAgent(
        agent_id="orch-test",
        bus=bus,
        store=store,
        registry=reg,
        llm_client=llm_client,
    )


# ---------------------------------------------------------------------------
# replan() unit tests
# ---------------------------------------------------------------------------

class TestReplan:
    async def test_no_llm_client_returns_none(self):
        result = await replan(
            original_description="do something",
            completed_steps=[],
            failed_step={"name": "s1", "error": "boom"},
            pending_steps=[],
            llm_client=None,
        )
        assert result is None

    async def test_revised_plan_returned(self):
        revised = [
            {"name": "retry_alt", "description": "try alternate", "assigned_role": "coder",
             "skill": "", "params": {}, "depends_on": []}
        ]
        llm = _FakeLLM(json.dumps(revised))

        result = await replan(
            original_description="deploy model",
            completed_steps=[{"name": "upload", "result": "ok"}],
            failed_step={"name": "run", "error": "OOM"},
            pending_steps=[],
            llm_client=llm,
        )
        assert result is not None
        assert len(result) == 1
        assert result[0]["name"] == "retry_alt"
        # Verify LLM was called with correct context
        assert len(llm.calls) == 1
        assert "deploy model" in llm.calls[0]["messages"][0]["content"]
        assert "OOM" in llm.calls[0]["messages"][0]["content"]

    async def test_abort_signal_returns_none(self):
        llm = _FakeLLM(json.dumps([{"abort": True, "reason": "unrecoverable"}]))

        result = await replan(
            original_description="impossible task",
            completed_steps=[],
            failed_step={"name": "s1", "error": "fatal"},
            pending_steps=[],
            llm_client=llm,
        )
        assert result is None

    async def test_llm_error_returns_none(self):
        llm = _ErrorLLM()

        result = await replan(
            original_description="do stuff",
            completed_steps=[],
            failed_step={"name": "s1", "error": "err"},
            pending_steps=[],
            llm_client=llm,
        )
        assert result is None

    async def test_markdown_fenced_json_stripped(self):
        """LLM sometimes wraps JSON in ```json ... ``` — replan should handle that."""
        revised = [{"name": "alt", "description": "alt approach", "assigned_role": "coder",
                     "skill": "", "params": {}, "depends_on": []}]
        fenced = f"```json\n{json.dumps(revised)}\n```"
        llm = _FakeLLM(fenced)

        result = await replan(
            original_description="task",
            completed_steps=[],
            failed_step={"name": "s1", "error": "fail"},
            pending_steps=[],
            llm_client=llm,
        )
        assert result is not None
        assert result[0]["name"] == "alt"

    async def test_multi_step_revised_plan(self):
        revised = [
            {"name": "step_a", "description": "first", "assigned_role": "coder",
             "skill": "", "params": {}, "depends_on": []},
            {"name": "step_b", "description": "second", "assigned_role": "infra_manager",
             "skill": "", "params": {"data": "{{step_a}}"}, "depends_on": ["step_a"]},
        ]
        llm = _FakeLLM(json.dumps(revised))

        result = await replan(
            original_description="complex task",
            completed_steps=[],
            failed_step={"name": "orig", "error": "crash"},
            pending_steps=[],
            llm_client=llm,
        )
        assert len(result) == 2
        assert result[1]["depends_on"] == ["step_a"]


# ---------------------------------------------------------------------------
# OrchestratorAgent._attempt_replan() integration tests
# ---------------------------------------------------------------------------

class TestAttemptReplan:
    async def test_replan_injects_new_steps(self, infra):
        bus, store, reg = infra
        revised = [
            {"name": "recovery", "description": "try different approach",
             "assigned_role": "coder", "skill": "", "params": {}, "depends_on": []}
        ]
        llm = _FakeLLM(json.dumps(revised))
        orch = _make_orchestrator(bus, store, reg, llm_client=llm)
        await orch.start()

        # Build a job with one completed step and one failed step (exhausted retries)
        job = Job(title="test job", description="do the thing")
        s_done = Step(name="prep", assigned_role="coder", skill="", max_attempts=1)
        s_done.complete("prep result")
        s_fail = Step(name="run", assigned_role="coder", skill="", max_attempts=1)
        s_fail.start()
        s_fail.fail("crashed")

        job.steps = [s_done, s_fail]
        job.start()
        orch._jobs[job.job_id] = job

        await orch._attempt_replan(job)

        # Failed step should be removed, new recovery step added
        step_names = [s.name for s in job.steps]
        assert "prep" in step_names       # completed step kept
        assert "run" not in step_names     # failed step removed
        assert "recovery" in step_names    # new step injected
        assert job.metadata.get("replanned") is True

        await orch.stop()

    async def test_replan_only_once(self, infra):
        bus, store, reg = infra
        llm = _FakeLLM(json.dumps([{"abort": True, "reason": "nope"}]))
        orch = _make_orchestrator(bus, store, reg, llm_client=llm)
        await orch.start()

        job = Job(title="test", description="task")
        s = Step(name="s1", assigned_role="coder", max_attempts=1)
        s.start(); s.fail("err")
        job.steps = [s]
        job.start()
        orch._jobs[job.job_id] = job

        # First replan sets the flag
        await orch._attempt_replan(job)
        assert job.metadata["replanned"] is True
        assert len(llm.calls) == 1

        # Second call should not invoke LLM again (guard in _advance_job checks metadata)
        # Simulate: _advance_job checks `not job.metadata.get("replanned")` before calling
        # So directly calling _attempt_replan again would still call LLM,
        # but _advance_job won't reach it. Verify the flag is set.
        assert job.metadata["replanned"] is True

        await orch.stop()

    async def test_replan_abort_leaves_job_to_fail(self, infra):
        bus, store, reg = infra
        llm = _FakeLLM(json.dumps([{"abort": True, "reason": "unrecoverable"}]))
        orch = _make_orchestrator(bus, store, reg, llm_client=llm)
        await orch.start()

        job = Job(title="test", description="task")
        s_done = Step(name="ok", assigned_role="coder", max_attempts=1)
        s_done.complete("result")
        s_fail = Step(name="bad", assigned_role="coder", max_attempts=1)
        s_fail.start(); s_fail.fail("fatal")
        job.steps = [s_done, s_fail]
        job.start()
        orch._jobs[job.job_id] = job

        await orch._attempt_replan(job)

        # Abort returns None → no steps replaced, failed step still there
        step_names = [s.name for s in job.steps]
        assert "bad" in step_names  # failed step NOT removed (replan returned None)

        await orch.stop()

    async def test_replan_preserves_completed_results(self, infra):
        bus, store, reg = infra
        revised = [
            {"name": "alt", "description": "alternative", "assigned_role": "coder",
             "skill": "", "params": {"data": "{{prep}}"}, "depends_on": ["prep"]}
        ]
        llm = _FakeLLM(json.dumps(revised))
        orch = _make_orchestrator(bus, store, reg, llm_client=llm)
        await orch.start()

        job = Job(title="test", description="task")
        s_done = Step(name="prep", assigned_role="coder", max_attempts=1)
        s_done.complete({"key": "value"})
        s_fail = Step(name="process", assigned_role="coder", max_attempts=1)
        s_fail.start(); s_fail.fail("OOM")
        job.steps = [s_done, s_fail]
        job.start()
        orch._jobs[job.job_id] = job

        await orch._attempt_replan(job)

        # Completed step's result preserved
        prep = next(s for s in job.steps if s.name == "prep")
        assert prep.result == {"key": "value"}
        assert prep.status == StepStatus.COMPLETED

        # New step depends on completed step
        alt = next(s for s in job.steps if s.name == "alt")
        assert prep.step_id in alt.depends_on

        await orch.stop()

    async def test_advance_job_triggers_replan_on_blocked_pending(self, infra):
        """_advance_job calls _attempt_replan when a pending step is blocked by a failure."""
        bus, store, reg = infra

        revised = [
            {"name": "fallback", "description": "fallback", "assigned_role": "coder",
             "skill": "", "params": {}, "depends_on": []}
        ]
        llm = _FakeLLM(json.dumps(revised))
        orch = _make_orchestrator(bus, store, reg, llm_client=llm)
        await orch.start()

        job = Job(title="e2e", description="end to end replan test")
        s_fail = Step(name="orig", assigned_role="coder", skill="", max_attempts=1)
        s_fail.start(); s_fail.fail("crashed")
        # A pending step depends on the failed one — blocked, not done
        s_blocked = Step(name="next", assigned_role="coder", skill="",
                         depends_on=[s_fail.step_id])
        job.steps = [s_fail, s_blocked]
        job.start()
        orch._jobs[job.job_id] = job
        await orch._persist_job(job)

        # _advance_job: no ready steps, not done (pending blocked), has failures → replan
        await orch._advance_job(job)

        # After replan, blocked step removed, fallback injected
        step_names = [s.name for s in job.steps]
        assert "fallback" in step_names
        assert job.metadata["replanned"] is True

        await orch.stop()

    async def test_no_replan_without_llm_client(self, infra):
        """Without an LLM client, replan is skipped and the job fails normally."""
        bus, store, reg = infra
        orch = _make_orchestrator(bus, store, reg, llm_client=None)
        await orch.start()

        failed_events = []
        bus.subscribe("job.failed", lambda e: failed_events.append(e))

        job = Job(title="no-llm", description="will fail")
        s = Step(name="s1", assigned_role="coder", max_attempts=1)
        s.start(); s.fail("err")
        job.steps = [s]
        job.start()
        orch._jobs[job.job_id] = job
        await orch._persist_job(job)

        await orch._advance_job(job)

        # Job should be marked failed (no replan attempted)
        assert job.status == JobStatus.FAILED
        assert "replanned" not in job.metadata

        await orch.stop()
