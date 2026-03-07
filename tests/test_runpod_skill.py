"""Tests for RunPodSkill — uses httpx mock transport so no real API calls."""

import pytest
import httpx

from skills.builtin.runpod import RunPodSkill
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
    return RunPodSkill()


# ---------------------------------------------------------------------------
# Validation — no network needed
# ---------------------------------------------------------------------------

class TestRunPodSkillValidation:
    async def test_missing_action(self, skill, ctx):
        r = await skill.execute(ctx, {})
        assert r.success is False
        assert "action" in r.error

    async def test_missing_api_key(self, skill):
        bus = EventBus(); store = StateStore()
        await bus.connect(); await store.connect()
        ctx_no_key = SkillContext(
            agent_id="test",
            state_store=store,
            event_bus=bus,
            metadata={},   # no runpod_api_key
        )
        r = await skill.execute(ctx_no_key, {"action": "list_pods"})
        assert r.success is False
        assert "API key" in r.error

    async def test_pod_action_missing_pod_id(self, skill, ctx):
        for action in ("pod_status", "start_pod", "stop_pod", "terminate_pod"):
            r = await skill.execute(ctx, {"action": action})
            assert r.success is False
            assert "pod_id" in r.error

    async def test_unknown_action(self, skill, ctx):
        r = await skill.execute(ctx, {"action": "nuke_everything", "pod_id": "p1"})
        assert r.success is False
        assert "Unknown action" in r.error

    def test_skill_metadata(self, skill):
        assert skill.name == "runpod"
        assert skill.description
        assert "RUNPOD_API_KEY" in skill.required_secrets

    def test_discovered_by_registry(self):
        from skills.registry import SkillRegistry
        reg = SkillRegistry()
        reg.discover()
        assert "runpod" in reg


# ---------------------------------------------------------------------------
# HTTP-level tests using httpx MockTransport
# ---------------------------------------------------------------------------

def _make_ctx_with_mock(mock_transport):
    """Return a SkillContext whose skill can use a patched httpx client."""
    # We patch at the module level via monkeypatch in each test instead.
    pass


class TestRunPodSkillHTTP:
    """Patch httpx.AsyncClient to return canned responses."""

    async def test_list_pods_success(self, skill, ctx, monkeypatch):
        payload = {"data": {"myself": {"pods": [
            {"id": "pod1", "name": "my-pod", "desiredStatus": "RUNNING",
             "runtime": {"uptimeInSeconds": 3600}},
        ]}}}

        class MockResp:
            status_code = 200
            is_success = True
            def json(self): return payload

        class MockClient:
            async def __aenter__(self): return self
            async def __aexit__(self, *_): pass
            async def post(self, *a, **kw): return MockResp()

        monkeypatch.setattr("skills.builtin.runpod.httpx.AsyncClient", lambda **_: MockClient())

        r = await skill.execute(ctx, {"action": "list_pods"})
        assert r.success is True
        pods = r.output["myself"]["pods"]
        assert pods[0]["id"] == "pod1"

    async def test_pod_status_success(self, skill, ctx, monkeypatch):
        payload = {"data": {"pod": {
            "id": "pod1", "name": "my-pod", "desiredStatus": "RUNNING",
            "runtime": {"uptimeInSeconds": 100, "gpus": [{"id": "g0", "memoryInGb": 24}]},
        }}}

        class MockResp:
            status_code = 200
            is_success = True
            def json(self): return payload

        class MockClient:
            async def __aenter__(self): return self
            async def __aexit__(self, *_): pass
            async def post(self, *a, **kw): return MockResp()

        monkeypatch.setattr("skills.builtin.runpod.httpx.AsyncClient", lambda **_: MockClient())

        r = await skill.execute(ctx, {"action": "pod_status", "pod_id": "pod1"})
        assert r.success is True
        assert r.output["pod"]["id"] == "pod1"
        assert r.output["pod"]["runtime"]["gpus"][0]["memoryInGb"] == 24

    async def test_api_http_error(self, skill, ctx, monkeypatch):
        class MockResp:
            status_code = 401
            is_success = False
            text = "Unauthorized"

        class MockClient:
            async def __aenter__(self): return self
            async def __aexit__(self, *_): pass
            async def post(self, *a, **kw): return MockResp()

        monkeypatch.setattr("skills.builtin.runpod.httpx.AsyncClient", lambda **_: MockClient())

        r = await skill.execute(ctx, {"action": "list_pods"})
        assert r.success is False
        assert "401" in r.error

    async def test_graphql_error_response(self, skill, ctx, monkeypatch):
        payload = {"errors": [{"message": "Pod not found"}]}

        class MockResp:
            status_code = 200
            is_success = True
            def json(self): return payload

        class MockClient:
            async def __aenter__(self): return self
            async def __aexit__(self, *_): pass
            async def post(self, *a, **kw): return MockResp()

        monkeypatch.setattr("skills.builtin.runpod.httpx.AsyncClient", lambda **_: MockClient())

        r = await skill.execute(ctx, {"action": "pod_status", "pod_id": "bad-id"})
        assert r.success is False
        assert "Pod not found" in r.error

    async def test_start_pod(self, skill, ctx, monkeypatch):
        payload = {"data": {"podResume": {"id": "pod1", "desiredStatus": "RUNNING"}}}

        class MockResp:
            status_code = 200
            is_success = True
            def json(self): return payload

        class MockClient:
            async def __aenter__(self): return self
            async def __aexit__(self, *_): pass
            async def post(self, *a, **kw): return MockResp()

        monkeypatch.setattr("skills.builtin.runpod.httpx.AsyncClient", lambda **_: MockClient())

        r = await skill.execute(ctx, {"action": "start_pod", "pod_id": "pod1"})
        assert r.success is True
        assert r.output["podResume"]["desiredStatus"] == "RUNNING"

    async def test_stop_pod(self, skill, ctx, monkeypatch):
        payload = {"data": {"podStop": {"id": "pod1", "desiredStatus": "EXITED"}}}

        class MockResp:
            status_code = 200
            is_success = True
            def json(self): return payload

        class MockClient:
            async def __aenter__(self): return self
            async def __aexit__(self, *_): pass
            async def post(self, *a, **kw): return MockResp()

        monkeypatch.setattr("skills.builtin.runpod.httpx.AsyncClient", lambda **_: MockClient())

        r = await skill.execute(ctx, {"action": "stop_pod", "pod_id": "pod1"})
        assert r.success is True
        assert r.output["podStop"]["desiredStatus"] == "EXITED"
