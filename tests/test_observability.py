"""Tests for observability: MetricsCollector, AgentWatchdog, and instrumentation."""

import asyncio
import time
import pytest

from core.metrics import MetricsCollector
from core.watchdog import AgentWatchdog
from core.event_bus import EventBus, Event
from core.state_store import StateStore
from agents.base import AgentStatus, BaseAgent
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
# MetricsCollector tests
# ---------------------------------------------------------------------------

class TestMetricsCollector:
    def test_counter_increment(self):
        m = MetricsCollector()
        assert m.counter("test.count") == 0
        m.increment("test.count")
        assert m.counter("test.count") == 1
        m.increment("test.count", 5)
        assert m.counter("test.count") == 6

    def test_gauge_set_and_get(self):
        m = MetricsCollector()
        m.gauge("agents.running", 10)
        assert m.get_gauge("agents.running") == 10
        m.gauge("agents.running", 8)
        assert m.get_gauge("agents.running") == 8

    def test_gauge_default_zero(self):
        m = MetricsCollector()
        assert m.get_gauge("nonexistent") == 0.0

    def test_timing_records_stats(self):
        m = MetricsCollector()
        m.timing("skill.duration_ms", 10.0)
        m.timing("skill.duration_ms", 20.0)
        m.timing("skill.duration_ms", 30.0)
        snap = m.snapshot()
        h = snap["histograms"]["skill.duration_ms"]
        assert h["count"] == 3
        assert h["total"] == 60.0
        assert h["avg"] == 20.0
        assert h["min"] == 10.0
        assert h["max"] == 30.0

    def test_timing_p50_and_p95(self):
        m = MetricsCollector()
        for i in range(100):
            m.timing("latency", float(i))
        snap = m.snapshot()
        h = snap["histograms"]["latency"]
        assert h["p50"] == 50.0  # median of 0-99
        assert h["p95"] >= 94.0  # 95th percentile

    def test_timer_context_manager(self):
        m = MetricsCollector()
        with m.timer("test.block"):
            time.sleep(0.01)  # 10ms
        snap = m.snapshot()
        h = snap["histograms"]["test.block"]
        assert h["count"] == 1
        assert h["avg"] >= 5.0  # at least 5ms (conservative)

    async def test_async_timer(self):
        m = MetricsCollector()
        async with m.timer("async.block"):
            await asyncio.sleep(0.01)
        snap = m.snapshot()
        h = snap["histograms"]["async.block"]
        assert h["count"] == 1
        assert h["avg"] >= 5.0

    def test_snapshot_structure(self):
        m = MetricsCollector()
        m.increment("c1")
        m.gauge("g1", 42)
        m.timing("h1", 100)
        snap = m.snapshot()
        assert "uptime_seconds" in snap
        assert snap["counters"]["c1"] == 1
        assert snap["gauges"]["g1"] == 42
        assert "h1" in snap["histograms"]

    def test_reset(self):
        m = MetricsCollector()
        m.increment("x")
        m.gauge("y", 1)
        m.timing("z", 5)
        m.reset()
        snap = m.snapshot()
        assert snap["counters"] == {}
        assert snap["gauges"] == {}
        assert snap["histograms"] == {}

    def test_histogram_recent_bounded(self):
        """Recent samples should be bounded to 100."""
        m = MetricsCollector()
        for i in range(200):
            m.timing("bounded", float(i))
        snap = m.snapshot()
        # p50 should reflect recent values (100-199), not all 200
        assert snap["histograms"]["bounded"]["p50"] >= 100


# ---------------------------------------------------------------------------
# AgentWatchdog tests
# ---------------------------------------------------------------------------

class TestAgentWatchdog:
    async def test_watchdog_starts_and_stops(self, infra):
        bus, store, reg = infra
        agent = StubAgent(bus=bus, store=store, registry=reg)
        await agent.start()

        wd = AgentWatchdog(bus=bus, store=store, agents=[agent],
                           stale_threshold=5.0, check_interval=1.0)
        await wd.start()
        assert wd._running is True

        await wd.stop()
        assert wd._running is False

        await agent.stop()

    async def test_healthy_agent_not_flagged(self, infra):
        bus, store, reg = infra
        agent = StubAgent(bus=bus, store=store, registry=reg, heartbeat_interval=1.0)
        await agent.start()

        stall_events = []
        async def _collect(e): stall_events.append(e)
        bus.subscribe("agent.stalled", _collect)

        wd = AgentWatchdog(bus=bus, store=store, agents=[agent],
                           stale_threshold=10.0, check_interval=0.5)
        await wd.start()
        await asyncio.sleep(2.0)  # let watchdog check a few times

        assert len(stall_events) == 0
        assert len(wd.stalled_agents) == 0

        await wd.stop()
        await agent.stop()

    async def test_stalled_agent_detected(self, infra):
        bus, store, reg = infra
        agent = StubAgent(bus=bus, store=store, registry=reg, heartbeat_interval=999)
        await agent.start()

        # Manually set heartbeat to the past so it looks stalled
        agent._state.last_heartbeat = time.time() - 120
        await store.set(f"agents:{agent.agent_id}", agent._state.to_dict())

        stall_events = []
        async def _collect(e): stall_events.append(e)
        bus.subscribe("agent.stalled", _collect)

        wd = AgentWatchdog(bus=bus, store=store, agents=[agent],
                           stale_threshold=5.0, check_interval=0.5)
        await wd.start()
        await asyncio.sleep(2.0)

        assert len(stall_events) >= 1  # alert emitted
        assert agent.agent_id in wd.stalled_agents
        assert stall_events[0].payload["role"] == "stub"

        await wd.stop()
        await agent.stop()

    async def test_stall_alert_fires_once(self, infra):
        """Should not spam alerts for the same stalled agent."""
        bus, store, reg = infra
        agent = StubAgent(bus=bus, store=store, registry=reg, heartbeat_interval=999)
        await agent.start()

        agent._state.last_heartbeat = time.time() - 120
        await store.set(f"agents:{agent.agent_id}", agent._state.to_dict())

        stall_events = []
        async def _collect(e): stall_events.append(e)
        bus.subscribe("agent.stalled", _collect)

        wd = AgentWatchdog(bus=bus, store=store, agents=[agent],
                           stale_threshold=5.0, check_interval=0.5)
        await wd.start()
        await asyncio.sleep(3.0)  # multiple check cycles

        # Should fire exactly once, not every cycle
        assert len(stall_events) == 1

        await wd.stop()
        await agent.stop()

    async def test_recovery_clears_stall(self, infra):
        bus, store, reg = infra
        agent = StubAgent(bus=bus, store=store, registry=reg, heartbeat_interval=999)
        await agent.start()

        # Start stalled
        agent._state.last_heartbeat = time.time() - 120
        await store.set(f"agents:{agent.agent_id}", agent._state.to_dict())

        wd = AgentWatchdog(bus=bus, store=store, agents=[agent],
                           stale_threshold=5.0, check_interval=0.5)
        await wd.start()
        await asyncio.sleep(1.5)

        assert agent.agent_id in wd.stalled_agents

        # Simulate recovery — update heartbeat to now
        agent._state.last_heartbeat = time.time()
        await store.set(f"agents:{agent.agent_id}", agent._state.to_dict())

        await asyncio.sleep(1.5)

        assert agent.agent_id not in wd.stalled_agents

        await wd.stop()
        await agent.stop()

    async def test_stopped_agents_ignored(self, infra):
        bus, store, reg = infra
        agent = StubAgent(bus=bus, store=store, registry=reg)
        await agent.start()
        await agent.stop()  # stopped agent

        stall_events = []
        async def _collect(e): stall_events.append(e)
        bus.subscribe("agent.stalled", _collect)

        wd = AgentWatchdog(bus=bus, store=store, agents=[agent],
                           stale_threshold=1.0, check_interval=0.5)
        await wd.start()
        await asyncio.sleep(2.0)

        assert len(stall_events) == 0  # stopped agents should be skipped

        await wd.stop()


# ---------------------------------------------------------------------------
# Instrumentation integration tests
# ---------------------------------------------------------------------------

class TestInstrumentation:
    async def test_skill_execution_records_metrics(self, infra):
        """BaseAgent.run_skill should record timing and counters."""
        bus, store, reg = infra
        from core.metrics import metrics as global_metrics
        global_metrics.reset()

        agent = StubAgent(bus=bus, store=store, registry=reg)
        await agent.start()

        result = await agent.run_skill("file_manager", {"action": "read", "path": "nonexistent.txt"})

        snap = global_metrics.snapshot()
        assert snap["counters"]["skills.executed"] >= 1
        assert "skills.file_manager.duration_ms" in snap["histograms"]
        assert "skills.all.duration_ms" in snap["histograms"]

        await agent.stop()
