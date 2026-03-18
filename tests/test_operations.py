"""Tests for operational upgrades: structured logging, agent capabilities, health probes."""

import asyncio
import json
import logging
import pytest

from core.logging import (
    configure_logging,
    set_log_context,
    clear_log_context,
    get_log_context,
    StructuredFormatter,
    ContextFormatter,
)
from core.event_bus import EventBus
from core.state_store import StateStore
from agents.base import BaseAgent, AgentState, AgentStatus
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
    capabilities = ["file_manager", "test_skill"]
    async def _setup(self):
        pass


class BareAgent(BaseAgent):
    role = "bare"
    async def _setup(self):
        pass


# ---------------------------------------------------------------------------
# Structured logging tests
# ---------------------------------------------------------------------------

class TestLogContext:
    def test_set_and_get_context(self):
        clear_log_context()
        set_log_context(agent_id="coder-1", job_id="j-123", step_id="s1")
        ctx = get_log_context()
        assert ctx["agent_id"] == "coder-1"
        assert ctx["job_id"] == "j-123"
        assert ctx["step_id"] == "s1"
        clear_log_context()

    def test_clear_context(self):
        set_log_context(agent_id="x", job_id="y")
        clear_log_context()
        ctx = get_log_context()
        assert ctx == {}

    def test_partial_context(self):
        clear_log_context()
        set_log_context(agent_id="a1")
        ctx = get_log_context()
        assert ctx == {"agent_id": "a1"}
        assert "job_id" not in ctx
        clear_log_context()

    def test_correlation_id(self):
        clear_log_context()
        set_log_context(correlation_id="corr-456")
        ctx = get_log_context()
        assert ctx["correlation_id"] == "corr-456"
        clear_log_context()

    def test_overwrite_context(self):
        clear_log_context()
        set_log_context(agent_id="old")
        set_log_context(agent_id="new")
        assert get_log_context()["agent_id"] == "new"
        clear_log_context()


class TestStructuredFormatter:
    def test_json_output(self):
        fmt = StructuredFormatter()
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="hello world", args=(), exc_info=None,
        )
        output = fmt.format(record)
        parsed = json.loads(output)
        assert parsed["level"] == "INFO"
        assert parsed["message"] == "hello world"
        assert "timestamp" in parsed

    def test_json_includes_context(self):
        clear_log_context()
        set_log_context(agent_id="coder-1", job_id="j-abc")
        fmt = StructuredFormatter()
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="processing", args=(), exc_info=None,
        )
        output = fmt.format(record)
        parsed = json.loads(output)
        assert parsed["agent_id"] == "coder-1"
        assert parsed["job_id"] == "j-abc"
        clear_log_context()

    def test_json_no_context_when_empty(self):
        clear_log_context()
        fmt = StructuredFormatter()
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="no context", args=(), exc_info=None,
        )
        output = fmt.format(record)
        parsed = json.loads(output)
        assert "agent_id" not in parsed


class TestContextFormatter:
    def test_text_output_with_context(self):
        clear_log_context()
        set_log_context(agent_id="a1")
        fmt = ContextFormatter()
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="hello", args=(), exc_info=None,
        )
        output = fmt.format(record)
        assert "hello" in output
        assert "[agent_id=a1]" in output
        clear_log_context()

    def test_text_output_without_context(self):
        clear_log_context()
        fmt = ContextFormatter()
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="plain", args=(), exc_info=None,
        )
        output = fmt.format(record)
        assert "plain" in output
        assert "[" not in output


class TestConfigureLogging:
    def test_configure_text(self):
        configure_logging(level="DEBUG", log_format="text")
        root = logging.getLogger()
        assert root.level == logging.DEBUG
        assert len(root.handlers) >= 1

    def test_configure_json(self):
        configure_logging(level="INFO", log_format="json")
        root = logging.getLogger()
        # Should have a StructuredFormatter
        has_structured = any(
            isinstance(h.formatter, StructuredFormatter)
            for h in root.handlers
        )
        assert has_structured

    def test_reconfigure_replaces_handlers(self):
        configure_logging(level="INFO", log_format="text")
        count1 = len(logging.getLogger().handlers)
        configure_logging(level="INFO", log_format="json")
        count2 = len(logging.getLogger().handlers)
        # Should not accumulate handlers
        assert count2 == count1


# ---------------------------------------------------------------------------
# Agent capability tests
# ---------------------------------------------------------------------------

class TestAgentCapabilities:
    async def test_capabilities_in_state(self, infra):
        """Agent capabilities should be persisted in state."""
        bus, store, reg = infra
        agent = StubAgent(bus=bus, store=store, registry=reg)
        await agent.start()

        state = await agent.get_state()
        assert "file_manager" in state.capabilities
        assert "test_skill" in state.capabilities

        await agent.stop()

    async def test_capabilities_in_to_dict(self, infra):
        """capabilities should appear in to_dict output."""
        bus, store, reg = infra
        agent = StubAgent(bus=bus, store=store, registry=reg)
        await agent.start()

        state = await agent.get_state()
        d = state.to_dict()
        assert "capabilities" in d
        assert "file_manager" in d["capabilities"]

        await agent.stop()

    async def test_empty_capabilities_default(self, infra):
        """Agent with no declared capabilities should have empty list."""
        bus, store, reg = infra
        agent = BareAgent(bus=bus, store=store, registry=reg)
        await agent.start()

        state = await agent.get_state()
        assert state.capabilities == []

        await agent.stop()

    async def test_capabilities_in_started_event(self, infra):
        """agent.started event should include capabilities."""
        bus, store, reg = infra
        events = []

        async def _collect(e):
            if e.event_type == "agent.started":
                events.append(e)

        bus.subscribe("agent.started", _collect)

        agent = StubAgent(agent_id="cap-test", bus=bus, store=store, registry=reg)
        await agent.start()
        await asyncio.sleep(0.2)

        assert len(events) >= 1
        payload = events[-1].payload
        assert "capabilities" in payload
        assert "file_manager" in payload["capabilities"]

        await agent.stop()

    def test_agent_state_capabilities_field(self):
        """AgentState should accept capabilities in constructor."""
        state = AgentState(
            agent_id="test", role="coder",
            capabilities=["file_manager", "editor"],
        )
        assert state.capabilities == ["file_manager", "editor"]
        d = state.to_dict()
        assert d["capabilities"] == ["file_manager", "editor"]


# ---------------------------------------------------------------------------
# Health/readiness endpoint unit tests (no HTTP, just logic)
# ---------------------------------------------------------------------------

class TestHealthLogic:
    async def test_agent_state_reflects_status(self, infra):
        """Agent state should correctly reflect running/stopped status."""
        bus, store, reg = infra
        agent = StubAgent(bus=bus, store=store, registry=reg)
        await agent.start()

        state = await agent.get_state()
        assert state.status == AgentStatus.RUNNING

        await agent.stop()
        state = await agent.get_state()
        assert state.status == AgentStatus.STOPPED

    async def test_error_agent_detectable(self, infra):
        """Agent in error state should be detectable."""
        bus, store, reg = infra

        class FailSetupAgent(BaseAgent):
            role = "fail_setup"
            async def _setup(self):
                raise RuntimeError("setup boom")

        agent = FailSetupAgent(bus=bus, store=store, registry=reg)
        await agent.start()

        state = await agent.get_state()
        assert state.status == AgentStatus.ERROR
        assert "setup boom" in state.error

    async def test_store_mode_readable(self, infra):
        """StateStore mode should be queryable for readiness checks."""
        bus, store, reg = infra
        assert store.mode in ("memory", "redis")

    async def test_bus_mode_readable(self, infra):
        """EventBus mode should be queryable for readiness checks."""
        bus, store, reg = infra
        assert bus.mode in ("memory", "redis")
