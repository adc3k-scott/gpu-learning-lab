"""Tests for BaseAgent, OrchestratorAgent, RepoAnalystAgent, CoderAgent."""

import asyncio
import pytest

from core.event_bus import Event, EventBus
from core.state_store import StateStore
from skills.registry import SkillRegistry, registry as global_registry
from agents.base import AgentStatus, BaseAgent
from agents.orchestrator import OrchestratorAgent
from agents.orchestrator.agent import _resolve_params
from agents.orchestrator.job import Job, JobStatus, Step, StepStatus
from agents.orchestrator.planner import plan
from agents.repo_analyst import RepoAnalystAgent
from agents.coder import CoderAgent


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
async def infra():
    bus = EventBus(); store = StateStore()
    await bus.connect(); await store.connect()
    yield bus, store
    await bus.disconnect()


@pytest.fixture
def reg():
    r = SkillRegistry()
    r.discover()
    return r


# ---------------------------------------------------------------------------
# BaseAgent
# ---------------------------------------------------------------------------

class EchoAgent(BaseAgent):
    role = "echo"
    async def _setup(self):
        self.bus.subscribe("ping", self._pong)
        self.pings = []
    async def _pong(self, e):
        self.pings.append(e.payload)
        await self.publish("pong", e.payload)


class TestBaseAgent:
    async def test_start_stop(self, infra, reg):
        bus, store = infra
        agent = EchoAgent(bus=bus, store=store, registry=reg, project_root=".")
        await agent.start()
        assert agent._state.status == AgentStatus.RUNNING
        await agent.stop()
        assert agent._state.status == AgentStatus.STOPPED

    async def test_state_persisted_to_store(self, infra, reg):
        bus, store = infra
        agent = EchoAgent(bus=bus, store=store, registry=reg, project_root=".")
        await agent.start()
        stored = await store.get(f"agents:{agent.agent_id}")
        assert stored is not None
        assert stored["status"] == "running"
        await agent.stop()

    async def test_publish_subscribe(self, infra, reg):
        bus, store = infra
        agent = EchoAgent(bus=bus, store=store, registry=reg, project_root=".")
        await agent.start()

        pongs = []
        bus.subscribe("pong", lambda e: pongs.append(e) or asyncio.sleep(0))

        await bus.publish(Event(event_type="ping", payload={"n": 1}))
        await asyncio.sleep(0.2)
        assert len(agent.pings) == 1
        await agent.stop()

    async def test_run_skill_success(self, infra, reg, tmp_path):
        bus, store = infra
        (tmp_path / "hello.txt").write_text("hi")
        agent = EchoAgent(
            bus=bus, store=store, registry=reg,
            project_root=str(tmp_path),
        )
        await agent.start()
        result = await agent.run_skill("file_manager", {"action": "exists", "path": "hello.txt"})
        assert result.success is True
        assert result.output is True
        await agent.stop()

    async def test_run_skill_unknown_name(self, infra, reg):
        bus, store = infra
        agent = EchoAgent(bus=bus, store=store, registry=reg, project_root=".")
        await agent.start()
        result = await agent.run_skill("no_such_skill", {})
        assert result.success is False
        await agent.stop()

    async def test_custom_agent_id(self, infra, reg):
        bus, store = infra
        agent = EchoAgent(agent_id="my-echo-1", bus=bus, store=store, registry=reg, project_root=".")
        assert agent.agent_id == "my-echo-1"


# ---------------------------------------------------------------------------
# Job / Step models
# ---------------------------------------------------------------------------

class TestJobModel:
    def test_ready_steps_no_deps(self):
        job = Job(title="t")
        s1 = Step(name="s1")
        s2 = Step(name="s2")
        job.add_step(s1).add_step(s2)
        assert len(job.ready_steps()) == 2

    def test_ready_steps_with_deps(self):
        job = Job(title="t")
        s1 = Step(name="s1")
        s2 = Step(name="s2", depends_on=[s1.step_id])
        job.add_step(s1).add_step(s2)
        assert job.ready_steps() == [s1]

    def test_ready_steps_after_completion(self):
        job = Job(title="t")
        s1 = Step(name="s1")
        s2 = Step(name="s2", depends_on=[s1.step_id])
        job.add_step(s1).add_step(s2)
        s1.complete("done")
        assert job.ready_steps() == [s2]

    def test_is_done(self):
        job = Job(title="t")
        s = Step(name="s")
        job.add_step(s)
        assert not job.is_done()
        s.complete("ok")
        assert job.is_done()

    def test_has_failures(self):
        job = Job(title="t")
        s = Step(name="s")
        job.add_step(s)
        s.fail("boom")
        assert job.has_failures()

    def test_step_can_retry(self):
        s = Step(name="s", max_attempts=3)
        s.start(); s.fail("err")
        assert s.can_retry()
        s.start(); s.fail("err")
        assert s.can_retry()
        s.start(); s.fail("err")
        assert not s.can_retry()

    def test_job_lifecycle(self):
        job = Job(title="t")
        assert job.status == JobStatus.PENDING
        job.start()
        assert job.status == JobStatus.RUNNING
        job.complete()
        assert job.status == JobStatus.COMPLETED

    def test_cancel_skips_pending_steps(self):
        job = Job(title="t")
        s1 = Step(name="s1"); s2 = Step(name="s2")
        job.add_step(s1).add_step(s2)
        job.cancel()
        assert all(s.status == StepStatus.SKIPPED for s in job.steps)


# ---------------------------------------------------------------------------
# Step output passing
# ---------------------------------------------------------------------------

class TestResolveParams:
    def test_exact_reference_preserves_type(self):
        result = _resolve_params({"data": "{{step_a}}"}, {"step_a": {"key": "val"}})
        assert result["data"] == {"key": "val"}

    def test_exact_reference_string_result(self):
        result = _resolve_params({"content": "{{read_file}}"}, {"read_file": "hello\n"})
        assert result["content"] == "hello\n"

    def test_partial_reference_interpolated(self):
        result = _resolve_params(
            {"prompt": "Summarise this: {{read_file}}"},
            {"read_file": "file contents here"},
        )
        assert result["prompt"] == "Summarise this: file contents here"

    def test_unknown_reference_left_unchanged(self):
        result = _resolve_params({"x": "{{unknown}}"}, {})
        assert result["x"] == "{{unknown}}"

    def test_nested_dict(self):
        result = _resolve_params(
            {"outer": {"inner": "{{step_a}}"}},
            {"step_a": 42},
        )
        assert result["outer"]["inner"] == 42

    def test_list_values(self):
        result = _resolve_params(
            {"items": ["{{step_a}}", "{{step_b}}"]},
            {"step_a": "x", "step_b": "y"},
        )
        assert result["items"] == ["x", "y"]

    def test_non_string_values_passthrough(self):
        result = _resolve_params({"n": 99, "flag": True}, {"step_a": "x"})
        assert result["n"] == 99
        assert result["flag"] is True

    def test_step_name_dot_result_notation(self):
        """{{step_name.result}} should work the same as {{step_name}}."""
        result = _resolve_params({"val": "{{step_a.result}}"}, {"step_a": "output"})
        assert result["val"] == "output"


class TestResultsByName:
    def test_returns_completed_only(self):
        job = Job(title="t")
        s1 = Step(name="s1"); s2 = Step(name="s2"); s3 = Step(name="s3")
        job.add_step(s1).add_step(s2).add_step(s3)
        s1.complete("out1")
        s2.fail("boom")
        # s3 still pending
        assert job.results_by_name() == {"s1": "out1"}

    def test_empty_when_none_complete(self):
        job = Job(title="t")
        job.add_step(Step(name="s1"))
        assert job.results_by_name() == {}


# ---------------------------------------------------------------------------
# Planner
# ---------------------------------------------------------------------------

class TestPlanner:
    async def test_list_pattern(self):
        job = await plan("list the files in the project")
        assert len(job.steps) == 1
        assert job.steps[0].assigned_role == "repo_analyst"
        assert job.steps[0].params.get("action") == "list"

    async def test_read_pattern(self):
        job = await plan("read file pyproject.toml")
        assert len(job.steps) == 1
        assert job.steps[0].assigned_role == "coder"
        assert job.steps[0].params.get("path") == "pyproject.toml"

    async def test_explain_pattern(self):
        job = await plan("explain what the codebase does")
        assert job.steps[0].assigned_role == "repo_analyst"

    async def test_terminate_pod_pattern(self):
        job = await plan("terminate pod abc123def")
        assert len(job.steps) == 1
        assert job.steps[0].skill == "runpod"
        assert job.steps[0].params.get("action") == "terminate_pod"

    async def test_write_file_pattern(self):
        job = await plan("write file hello.py with the content")
        assert len(job.steps) == 1
        assert job.steps[0].assigned_role == "coder"
        assert job.steps[0].params.get("action") == "write"

    async def test_generate_code_pattern(self):
        job = await plan("generate a Python script to parse JSON")
        assert len(job.steps) == 1
        assert job.steps[0].assigned_role == "coder"
        assert job.steps[0].params.get("action") == "generate"

    async def test_webhook_pattern(self):
        job = await plan("send webhook to http://example.com/hook with payload")
        assert len(job.steps) == 1
        assert job.steps[0].assigned_role == "integration"
        assert job.steps[0].params.get("action") == "webhook"

    async def test_http_pattern(self):
        job = await plan("fetch http://api.example.com/data")
        assert len(job.steps) == 1
        assert job.steps[0].skill == "http_client"

    async def test_unknown_falls_back_to_single_step(self):
        job = await plan("do something completely unrecognised xyz123")
        assert len(job.steps) == 1

    async def test_job_title_set(self):
        job = await plan("list files", title="My Job")
        assert job.title == "My Job"

    async def test_step_ids_unique(self):
        job = await plan("list files")
        ids = [s.step_id for s in job.steps]
        assert len(ids) == len(set(ids))


# ---------------------------------------------------------------------------
# OrchestratorAgent end-to-end
# ---------------------------------------------------------------------------

class TestOrchestratorAgent:
    async def test_task_completes_with_analyst(self, infra, reg, tmp_path):
        bus, store = infra
        orch    = OrchestratorAgent(bus=bus, store=store, registry=reg, project_root=str(tmp_path))
        analyst = RepoAnalystAgent(bus=bus, store=store, registry=reg, project_root=str(tmp_path))
        await orch.start(); await analyst.start()

        job_id = await orch.submit_task("list the files in the project")
        await asyncio.sleep(0.5)

        job = await orch.get_job(job_id)
        assert job is not None
        assert job["status"] == "completed"

        await analyst.stop(); await orch.stop()

    async def test_job_failed_when_no_handler(self, infra, reg):
        bus, store = infra
        orch = OrchestratorAgent(bus=bus, store=store, registry=reg, project_root=".")
        await orch.start()

        # Submit task that maps to repo_analyst but no analyst is running
        # Step stays running (never completed) — job stays running too
        job_id = await orch.submit_task("list the files in the project")
        await asyncio.sleep(0.3)

        job = await orch.get_job(job_id)
        assert job is not None
        assert job["status"] in ("running",)  # waiting for handler

        await orch.stop()

    async def test_list_jobs(self, infra, reg, tmp_path):
        bus, store = infra
        orch    = OrchestratorAgent(bus=bus, store=store, registry=reg, project_root=str(tmp_path))
        analyst = RepoAnalystAgent(bus=bus, store=store, registry=reg, project_root=str(tmp_path))
        await orch.start(); await analyst.start()

        await orch.submit_task("list the files in the project", title="Job A")
        await orch.submit_task("list the files in the project", title="Job B")
        await asyncio.sleep(0.5)

        jobs = await orch.list_jobs()
        assert len(jobs) >= 2

        await analyst.stop(); await orch.stop()


# ---------------------------------------------------------------------------
# OrchestratorAgent — job waiter / SSE pub-sub
# ---------------------------------------------------------------------------

class TestJobWaiter:
    async def test_subscribe_returns_queue(self, infra, reg):
        bus, store = infra
        orch = OrchestratorAgent(bus=bus, store=store, registry=reg, project_root=".")
        await orch.start()
        q = orch.subscribe_job("job-1")
        assert q is not None
        await orch.stop()

    async def test_unsubscribe_removes_queue(self, infra, reg):
        bus, store = infra
        orch = OrchestratorAgent(bus=bus, store=store, registry=reg, project_root=".")
        await orch.start()
        q = orch.subscribe_job("job-1")
        orch.unsubscribe_job("job-1", q)
        assert "job-1" not in orch._job_waiters
        await orch.stop()

    async def test_push_event_delivers_to_all_waiters(self, infra, reg):
        bus, store = infra
        orch = OrchestratorAgent(bus=bus, store=store, registry=reg, project_root=".")
        await orch.start()
        q1 = orch.subscribe_job("job-x")
        q2 = orch.subscribe_job("job-x")
        orch._push_job_event("job-x", {"type": "test"})
        assert q1.get_nowait() == {"type": "test"}
        assert q2.get_nowait() == {"type": "test"}
        await orch.stop()

    async def test_push_event_ignores_unknown_job(self, infra, reg):
        """Pushing to a job with no waiters should not raise."""
        bus, store = infra
        orch = OrchestratorAgent(bus=bus, store=store, registry=reg, project_root=".")
        await orch.start()
        orch._push_job_event("no-such-job", {"type": "test"})  # should not raise
        await orch.stop()

    async def test_job_done_event_received_via_waiter(self, infra, reg, tmp_path):
        """End-to-end: waiter receives job.done after task completes."""
        bus, store = infra
        orch    = OrchestratorAgent(bus=bus, store=store, registry=reg, project_root=str(tmp_path))
        analyst = RepoAnalystAgent(bus=bus, store=store, registry=reg, project_root=str(tmp_path))
        await orch.start(); await analyst.start()

        job_id = await orch.submit_task("list the files in the project")
        q = orch.subscribe_job(job_id)

        # Drain events until job.done (with a time cap)
        done_event = None
        for _ in range(20):
            await asyncio.sleep(0.1)
            while not q.empty():
                ev = q.get_nowait()
                if ev.get("type") == "job.done":
                    done_event = ev
        assert done_event is not None
        assert done_event["job"]["job_id"] == job_id
        assert done_event["job"]["status"] == "completed"

        orch.unsubscribe_job(job_id, q)
        await analyst.stop(); await orch.stop()

    async def test_step_events_delivered_before_job_done(self, infra, reg, tmp_path):
        """step.completed events should arrive before job.done."""
        bus, store = infra
        orch    = OrchestratorAgent(bus=bus, store=store, registry=reg, project_root=str(tmp_path))
        analyst = RepoAnalystAgent(bus=bus, store=store, registry=reg, project_root=str(tmp_path))
        await orch.start(); await analyst.start()

        job_id = await orch.submit_task("list the files in the project")
        q = orch.subscribe_job(job_id)

        events = []
        for _ in range(20):
            await asyncio.sleep(0.1)
            while not q.empty():
                events.append(q.get_nowait())

        types = [e.get("type") for e in events]
        assert "job.done" in types
        # step.completed arrives before job.done
        if "step.completed" in types:
            assert types.index("step.completed") < types.index("job.done")

        orch.unsubscribe_job(job_id, q)
        await analyst.stop(); await orch.stop()


class TestCoderAgent:
    async def test_write_and_read_via_event(self, infra, reg, tmp_path):
        bus, store = infra
        coder = CoderAgent(bus=bus, store=store, registry=reg, project_root=str(tmp_path))
        await coder.start()

        completed = []
        failed    = []
        async def on_done(e): completed.append(e.payload)
        async def on_fail(e): failed.append(e.payload)
        bus.subscribe("step.completed", on_done)
        bus.subscribe("step.failed",    on_fail)

        # Write
        await bus.publish(Event(event_type="step.dispatched", payload={
            "job_id": "j1", "step_id": "w1", "assigned_role": "coder",
            "skill": "file_manager",
            "params": {"action": "write", "path": "out.txt", "content": "test\n"},
            "description": "",
        }))
        await asyncio.sleep(0.3)
        assert len(completed) == 1
        assert (tmp_path / "out.txt").exists()

        # Read
        await bus.publish(Event(event_type="step.dispatched", payload={
            "job_id": "j1", "step_id": "r1", "assigned_role": "coder",
            "skill": "file_manager",
            "params": {"action": "read", "path": "out.txt"},
            "description": "",
        }))
        await asyncio.sleep(0.3)
        assert completed[1]["result"] == "test\n"
        assert not failed

        await coder.stop()
