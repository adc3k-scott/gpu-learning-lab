"""Tests for core infrastructure: EventBus and StateStore."""

import asyncio
import pytest

from core.event_bus import Event, EventBus
from core.state_store import StateStore


# ---------------------------------------------------------------------------
# StateStore
# ---------------------------------------------------------------------------

class TestStateStore:
    @pytest.fixture
    async def store(self):
        s = StateStore()
        await s.connect()
        yield s

    async def test_set_get_roundtrip(self, store):
        await store.set("k1", {"hello": "world"})
        val = await store.get("k1")
        assert val == {"hello": "world"}

    async def test_missing_key_returns_none(self, store):
        assert await store.get("nonexistent") is None

    async def test_delete(self, store):
        await store.set("del_key", 42)
        await store.delete("del_key")
        assert await store.get("del_key") is None

    async def test_exists(self, store):
        await store.set("ex_key", True)
        assert await store.exists("ex_key") is True
        assert await store.exists("no_such") is False

    async def test_ttl_expiry(self, store):
        await store.set("ttl_key", "expires", ttl=1)
        assert await store.get("ttl_key") == "expires"
        await asyncio.sleep(1.05)
        assert await store.get("ttl_key") is None

    async def test_keys_pattern(self, store):
        await store.set("ns:a", 1)
        await store.set("ns:b", 2)
        await store.set("other:c", 3)
        keys = await store.keys("ns:*")
        assert set(keys) == {"ns:a", "ns:b"}

    async def test_get_all(self, store):
        await store.set("grp:x", 10)
        await store.set("grp:y", 20)
        result = await store.get_all("grp:*")
        assert result == {"grp:x": 10, "grp:y": 20}

    async def test_overwrite(self, store):
        await store.set("ow", "first")
        await store.set("ow", "second")
        assert await store.get("ow") == "second"

    async def test_json_types(self, store):
        for val in [42, 3.14, True, None, [1, 2, 3], {"nested": {"deep": True}}]:
            await store.set("jtype", val)
            assert await store.get("jtype") == val

    async def test_mode_is_memory(self, store):
        assert store.mode == "memory"


# ---------------------------------------------------------------------------
# EventBus
# ---------------------------------------------------------------------------

class TestEventBus:
    @pytest.fixture
    async def bus(self):
        b = EventBus()
        await b.connect()
        yield b
        await b.disconnect()

    async def test_publish_subscribe(self, bus):
        received = []
        async def handler(e): received.append(e)
        bus.subscribe("test.event", handler)
        await bus.publish(Event(event_type="test.event", payload={"x": 1}))
        await asyncio.sleep(0.2)
        assert len(received) == 1
        assert received[0].payload == {"x": 1}

    async def test_wildcard_subscription(self, bus):
        received = []
        async def handler(e): received.append(e.event_type)
        bus.subscribe("job.*", handler)
        await bus.publish(Event(event_type="job.created"))
        await bus.publish(Event(event_type="job.completed"))
        await bus.publish(Event(event_type="step.done"))   # should NOT match
        await asyncio.sleep(0.2)
        assert received == ["job.created", "job.completed"]

    async def test_star_catches_all(self, bus):
        received = []
        async def handler(e): received.append(e.event_type)
        bus.subscribe("*", handler)
        for et in ["a.b", "c.d.e", "xyz"]:
            await bus.publish(Event(event_type=et))
        await asyncio.sleep(0.2)
        assert len(received) == 3

    async def test_multiple_handlers_same_pattern(self, bus):
        calls = []
        async def h1(e): calls.append("h1")
        async def h2(e): calls.append("h2")
        bus.subscribe("multi", h1)
        bus.subscribe("multi", h2)
        await bus.publish(Event(event_type="multi"))
        await asyncio.sleep(0.2)
        assert "h1" in calls and "h2" in calls

    async def test_unsubscribe(self, bus):
        received = []
        async def handler(e): received.append(e)
        bus.subscribe("unsub", handler)
        bus.unsubscribe("unsub", handler)
        await bus.publish(Event(event_type="unsub"))
        await asyncio.sleep(0.2)
        assert len(received) == 0

    async def test_event_fields(self, bus):
        captured = []
        async def handler(e): captured.append(e)
        bus.subscribe("fields", handler)
        await bus.publish(Event(
            event_type="fields",
            payload={"key": "val"},
            source="tester",
            correlation_id="corr-123",
        ))
        await asyncio.sleep(0.2)
        e = captured[0]
        assert e.payload == {"key": "val"}
        assert e.source == "tester"
        assert e.correlation_id == "corr-123"
        assert e.event_id         # auto-generated UUID
        assert e.timestamp        # auto-generated ISO timestamp

    async def test_handler_exception_does_not_crash_bus(self, bus):
        good = []
        async def bad(e):  raise RuntimeError("boom")
        async def good_fn(e): good.append(True)
        bus.subscribe("err_test", bad)
        bus.subscribe("err_test", good_fn)
        await bus.publish(Event(event_type="err_test"))
        await asyncio.sleep(0.2)
        assert good   # good handler still ran

    async def test_mode_is_memory(self, bus):
        assert bus.mode == "memory"
