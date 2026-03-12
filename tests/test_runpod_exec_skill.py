"""Tests for RunPodExecSkill — mocks SSH/SCP subprocess calls, no real pods needed."""

import asyncio
import pytest

from skills.builtin.runpod_exec import RunPodExecSkill
from skills.base import SkillContext
from core.event_bus import EventBus
from core.state_store import StateStore


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
async def ctx():
    bus = EventBus(); store = StateStore()
    await bus.connect(); await store.connect()
    return SkillContext(
        agent_id="test",
        state_store=store,
        event_bus=bus,
        metadata={"runpod_api_key": "test-key-123"},
    )


@pytest.fixture
def skill():
    return RunPodExecSkill()


def _mock_pod_ssh_info(monkeypatch, host="1.2.3.4", port=22222):
    """Patch _get_pod_ssh_info to return fake SSH connection details."""
    async def fake_info(pod_id, api_key):
        return {"host": host, "port": port, "pod_id": pod_id, "name": "test-pod", "status": "RUNNING"}
    monkeypatch.setattr("skills.builtin.runpod_exec._get_pod_ssh_info", fake_info)


def _mock_ssh_success(monkeypatch, stdout="ok\n", stderr="", rc=0):
    """Patch _run_ssh to return a canned successful result."""
    async def fake_run(args, timeout=300):
        return (stdout, stderr, rc)
    monkeypatch.setattr("skills.builtin.runpod_exec._run_ssh", fake_run)


def _mock_ssh_failure(monkeypatch, stderr="command not found", rc=127):
    """Patch _run_ssh to return a failed result."""
    async def fake_run(args, timeout=300):
        return ("", stderr, rc)
    monkeypatch.setattr("skills.builtin.runpod_exec._run_ssh", fake_run)


# ---------------------------------------------------------------------------
# Validation — no network / SSH needed
# ---------------------------------------------------------------------------

class TestRunPodExecValidation:
    async def test_missing_action(self, skill, ctx):
        r = await skill.execute(ctx, {"pod_id": "p1"})
        assert r.success is False
        assert "action" in r.error

    async def test_missing_pod_id(self, skill, ctx):
        r = await skill.execute(ctx, {"action": "execute"})
        assert r.success is False
        assert "pod_id" in r.error

    async def test_missing_api_key(self, skill):
        bus = EventBus(); store = StateStore()
        await bus.connect(); await store.connect()
        ctx_no_key = SkillContext(agent_id="test", state_store=store, event_bus=bus, metadata={})
        r = await skill.execute(ctx_no_key, {"action": "execute", "pod_id": "p1"})
        assert r.success is False
        assert "API key" in r.error

    async def test_unknown_action(self, skill, ctx, monkeypatch):
        _mock_pod_ssh_info(monkeypatch)
        r = await skill.execute(ctx, {"action": "nuke", "pod_id": "p1"})
        assert r.success is False
        assert "Unknown action" in r.error

    def test_skill_metadata(self, skill):
        assert skill.name == "runpod_exec"
        assert skill.description
        assert "RUNPOD_API_KEY" in skill.required_secrets

    def test_discovered_by_registry(self):
        from skills.registry import SkillRegistry
        reg = SkillRegistry()
        reg.discover()
        assert "runpod_exec" in reg

    async def test_pod_not_running(self, skill, ctx, monkeypatch):
        """When pod has no SSH info, should fail gracefully."""
        async def no_info(pod_id, api_key):
            return None
        monkeypatch.setattr("skills.builtin.runpod_exec._get_pod_ssh_info", no_info)
        r = await skill.execute(ctx, {"action": "execute", "pod_id": "p1", "command": "ls"})
        assert r.success is False
        assert "no SSH" in r.error or "RUNNING" in r.error


# ---------------------------------------------------------------------------
# Execute action
# ---------------------------------------------------------------------------

class TestRunPodExecExecute:
    async def test_execute_success(self, skill, ctx, monkeypatch):
        _mock_pod_ssh_info(monkeypatch)
        _mock_ssh_success(monkeypatch, stdout="GPU 0: A100\n")
        r = await skill.execute(ctx, {"action": "execute", "pod_id": "p1", "command": "nvidia-smi"})
        assert r.success is True
        assert "GPU 0" in r.output["stdout"]
        assert r.output["exit_code"] == 0

    async def test_execute_missing_command(self, skill, ctx, monkeypatch):
        _mock_pod_ssh_info(monkeypatch)
        r = await skill.execute(ctx, {"action": "execute", "pod_id": "p1"})
        assert r.success is False
        assert "command" in r.error

    async def test_execute_nonzero_exit(self, skill, ctx, monkeypatch):
        _mock_pod_ssh_info(monkeypatch)
        _mock_ssh_failure(monkeypatch, stderr="bad command", rc=1)
        r = await skill.execute(ctx, {"action": "execute", "pod_id": "p1", "command": "bad"})
        assert r.success is False
        assert r.output["exit_code"] == 1
        assert "bad command" in r.error


# ---------------------------------------------------------------------------
# Deploy action
# ---------------------------------------------------------------------------

class TestRunPodExecDeploy:
    async def test_deploy_success(self, skill, ctx, monkeypatch, tmp_path):
        _mock_pod_ssh_info(monkeypatch)
        _mock_ssh_success(monkeypatch, stdout="sending file\n")
        test_file = tmp_path / "model.py"
        test_file.write_text("print('hello')")
        r = await skill.execute(ctx, {
            "action": "deploy", "pod_id": "p1",
            "local_path": str(test_file), "remote_path": "/workspace/",
        })
        assert r.success is True
        assert r.output["action"] == "deploy"

    async def test_deploy_missing_local_path(self, skill, ctx, monkeypatch):
        _mock_pod_ssh_info(monkeypatch)
        r = await skill.execute(ctx, {"action": "deploy", "pod_id": "p1"})
        assert r.success is False
        assert "local_path" in r.error

    async def test_deploy_nonexistent_file(self, skill, ctx, monkeypatch):
        _mock_pod_ssh_info(monkeypatch)
        r = await skill.execute(ctx, {
            "action": "deploy", "pod_id": "p1",
            "local_path": "/no/such/file.py",
        })
        assert r.success is False
        assert "does not exist" in r.error


# ---------------------------------------------------------------------------
# Pull action
# ---------------------------------------------------------------------------

class TestRunPodExecPull:
    async def test_pull_success(self, skill, ctx, monkeypatch, tmp_path):
        _mock_pod_ssh_info(monkeypatch)
        _mock_ssh_success(monkeypatch, stdout="receiving file\n")
        r = await skill.execute(ctx, {
            "action": "pull", "pod_id": "p1",
            "remote_path": "/workspace/output.tar.gz",
            "local_path": str(tmp_path / "output.tar.gz"),
        })
        assert r.success is True
        assert r.output["action"] == "pull"

    async def test_pull_missing_remote_path(self, skill, ctx, monkeypatch):
        _mock_pod_ssh_info(monkeypatch)
        r = await skill.execute(ctx, {
            "action": "pull", "pod_id": "p1", "local_path": "/tmp/out",
        })
        assert r.success is False
        assert "remote_path" in r.error

    async def test_pull_missing_local_path(self, skill, ctx, monkeypatch):
        _mock_pod_ssh_info(monkeypatch)
        r = await skill.execute(ctx, {
            "action": "pull", "pod_id": "p1", "remote_path": "/workspace/out",
        })
        assert r.success is False
        assert "local_path" in r.error


# ---------------------------------------------------------------------------
# Run script action
# ---------------------------------------------------------------------------

class TestRunPodExecRunScript:
    async def test_run_script_success(self, skill, ctx, monkeypatch, tmp_path):
        _mock_pod_ssh_info(monkeypatch)
        _mock_ssh_success(monkeypatch, stdout="training complete\n")
        script = tmp_path / "train.py"
        script.write_text("print('training')")
        r = await skill.execute(ctx, {
            "action": "run_script", "pod_id": "p1",
            "local_path": str(script),
        })
        assert r.success is True
        assert r.output["action"] == "run_script"
        assert r.output["script"] == "train.py"

    async def test_run_script_missing_path(self, skill, ctx, monkeypatch):
        _mock_pod_ssh_info(monkeypatch)
        r = await skill.execute(ctx, {"action": "run_script", "pod_id": "p1"})
        assert r.success is False
        assert "local_path" in r.error

    async def test_run_script_nonexistent(self, skill, ctx, monkeypatch):
        _mock_pod_ssh_info(monkeypatch)
        r = await skill.execute(ctx, {
            "action": "run_script", "pod_id": "p1",
            "local_path": "/no/such/script.py",
        })
        assert r.success is False
        assert "does not exist" in r.error

    async def test_run_script_failure_returns_output(self, skill, ctx, monkeypatch, tmp_path):
        _mock_pod_ssh_info(monkeypatch)
        # Deploy succeeds, but execution fails
        call_count = 0
        async def fake_run(args, timeout=300):
            nonlocal call_count
            call_count += 1
            if call_count == 1:  # scp (deploy)
                return ("", "", 0)
            else:  # ssh (execute)
                return ("partial output\n", "OOM killed", 137)
        monkeypatch.setattr("skills.builtin.runpod_exec._run_ssh", fake_run)

        script = tmp_path / "big_train.py"
        script.write_text("import torch")
        r = await skill.execute(ctx, {
            "action": "run_script", "pod_id": "p1",
            "local_path": str(script),
        })
        assert r.success is False
        assert r.output["exit_code"] == 137
        assert "OOM" in r.error
