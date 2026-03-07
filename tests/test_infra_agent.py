"""Tests for InfraManagerAgent health checks."""

import pytest

from core.event_bus import Event, EventBus
from core.state_store import StateStore
from skills.registry import SkillRegistry
from agents.infra_manager import InfraManagerAgent


@pytest.fixture
async def agent(tmp_path):
    bus = EventBus(); store = StateStore()
    await bus.connect(); await store.connect()
    a = InfraManagerAgent(
        bus=bus, store=store,
        registry=SkillRegistry(),
        project_root=str(tmp_path),
        check_interval=999,   # disable auto-loop
    )
    await a.start()
    yield a
    await a.stop()
    await bus.disconnect()


class TestInfraManagerAgent:
    async def test_health_returns_dict(self, agent):
        h = await agent._health()
        assert isinstance(h, dict)
        assert "gpu" in h
        assert "system" in h
        assert "docker" in h
        assert "redis" in h
        assert "processes" in h

    async def test_gpu_check_graceful(self, agent):
        result = await agent._gpu_status()
        assert "available" in result

    async def test_system_check(self, agent):
        result = await agent._system_resources()
        assert "platform" in result

    async def test_docker_check_graceful(self, agent):
        result = await agent._docker_status()
        assert "available" in result

    async def test_redis_check_memory_mode(self, agent):
        result = await agent._redis_status()
        assert result["mode"] == "memory"

    async def test_step_dispatch_redis(self, agent):
        """Use the fast 'redis' action to verify step dispatch round-trip."""
        completed = []
        async def on_complete(e): completed.append(e.payload)
        agent.bus.subscribe("step.completed", on_complete)

        await agent.bus.publish(Event(
            event_type="step.dispatched",
            payload={
                "job_id": "j1", "step_id": "s1",
                "assigned_role": "infra_manager",
                "skill": "", "description": "",
                "params": {"action": "redis"},
            }
        ))
        import asyncio; await asyncio.sleep(0.5)
        assert len(completed) == 1
        assert completed[0]["result"]["mode"] == "memory"

    async def test_step_dispatch_ignored_for_other_roles(self, agent):
        completed = []
        async def on_complete(e): completed.append(e)
        agent.bus.subscribe("step.completed", on_complete)

        await agent.bus.publish(Event(
            event_type="step.dispatched",
            payload={
                "job_id": "j1", "step_id": "s1",
                "assigned_role": "coder",       # not infra_manager
                "skill": "", "description": "",
                "params": {"action": "health"},
            }
        ))
        import asyncio; await asyncio.sleep(0.2)
        assert len(completed) == 0
