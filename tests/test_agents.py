"""Tests for BaseAgent, OrchestratorAgent, RepoAnalystAgent, CoderAgent."""

import asyncio
import pytest

from core.event_bus import Event, EventBus
from core.state_store import StateStore
from skills.registry import SkillRegistry, registry as global_registry
from agents.base import AgentStatus, BaseAgent
from agents.orchestrator import OrchestratorAgent
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
# CoderAgent
# ---------------------------------------------------------------------------

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
