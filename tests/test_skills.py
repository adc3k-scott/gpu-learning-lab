"""Tests for the skill plugin system: base classes, registry, file_manager."""

import pytest
from pathlib import Path

from skills.base import BaseSkill, RetryPolicy, SkillContext, SkillResult
from skills.registry import SkillRegistry
from skills.builtin.file_manager import FileManagerSkill
from core.event_bus import EventBus
from core.state_store import StateStore


# ---------------------------------------------------------------------------
# SkillResult helpers
# ---------------------------------------------------------------------------

class TestSkillResult:
    def test_ok(self):
        r = SkillResult.ok(output="hello", extra="data")
        assert r.success is True
        assert r.output == "hello"
        assert r.error == ""
        assert r.metadata["extra"] == "data"

    def test_fail(self):
        r = SkillResult.fail("something broke", code=42)
        assert r.success is False
        assert r.output is None
        assert r.error == "something broke"
        assert r.metadata["code"] == 42


# ---------------------------------------------------------------------------
# BaseSkill validate_params
# ---------------------------------------------------------------------------

class ConcreteSkill(BaseSkill):
    name = "concrete"
    description = "test skill"
    async def execute(self, ctx, params): return SkillResult.ok()

class TestBaseSkill:
    def test_validate_params_ok(self):
        s = ConcreteSkill()
        assert s.validate_params({"a": 1, "b": 2}, required=["a", "b"]) is None

    def test_validate_params_missing(self):
        s = ConcreteSkill()
        err = s.validate_params({"a": 1}, required=["a", "b"])
        assert err is not None
        assert "b" in err

    def test_repr(self):
        s = ConcreteSkill()
        assert "concrete" in repr(s)


# ---------------------------------------------------------------------------
# SkillRegistry
# ---------------------------------------------------------------------------

class TestSkillRegistry:
    def test_register_and_get(self):
        reg = SkillRegistry()
        reg.register(ConcreteSkill())
        skill = reg.get("concrete")
        assert skill.name == "concrete"

    def test_get_missing_raises(self):
        reg = SkillRegistry()
        with pytest.raises(KeyError, match="not found"):
            reg.get("nope")

    def test_list_all(self):
        reg = SkillRegistry()
        reg.register(ConcreteSkill())
        items = reg.list_all()
        assert any(i["name"] == "concrete" for i in items)

    def test_skip_duplicate(self):
        reg = SkillRegistry()
        reg.register(ConcreteSkill())
        reg.register(ConcreteSkill())   # should not error, just skip
        assert len(reg) == 1

    def test_overwrite(self):
        reg = SkillRegistry()
        reg.register(ConcreteSkill())
        reg.register(ConcreteSkill(), overwrite=True)
        assert len(reg) == 1

    def test_contains(self):
        reg = SkillRegistry()
        reg.register(ConcreteSkill())
        assert "concrete" in reg
        assert "missing" not in reg

    def test_unregister(self):
        reg = SkillRegistry()
        reg.register(ConcreteSkill())
        reg.unregister("concrete")
        assert "concrete" not in reg

    def test_validation_rejects_no_name(self):
        class NoName(BaseSkill):
            name = ""
            description = "x"
            async def execute(self, ctx, params): return SkillResult.ok()
        reg = SkillRegistry()
        reg.register(NoName())
        assert "no_name" not in reg   # not registered

    def test_validation_rejects_no_description(self):
        class NoDesc(BaseSkill):
            name = "nodesc"
            description = ""
            async def execute(self, ctx, params): return SkillResult.ok()
        reg = SkillRegistry()
        reg.register(NoDesc())
        assert "nodesc" not in reg

    def test_discover_finds_file_manager(self):
        reg = SkillRegistry()
        reg.discover()
        assert "file_manager" in reg


# ---------------------------------------------------------------------------
# FileManagerSkill
# ---------------------------------------------------------------------------

@pytest.fixture
async def ctx(tmp_path):
    bus = EventBus(); store = StateStore()
    await bus.connect(); await store.connect()
    return SkillContext(
        agent_id="test",
        state_store=store,
        event_bus=bus,
        metadata={"project_root": str(tmp_path)},
    )


class TestFileManagerSkill:
    @pytest.fixture
    def skill(self): return FileManagerSkill()

    async def test_write_and_read(self, skill, ctx, tmp_path):
        content = "hello mission control\n"
        wr = await skill.execute(ctx, {"action": "write", "path": "test.txt", "content": content})
        assert wr.success is True

        rd = await skill.execute(ctx, {"action": "read", "path": "test.txt"})
        assert rd.success is True
        assert rd.output == content

    async def test_list(self, skill, ctx, tmp_path):
        (tmp_path / "a.py").write_text("x")
        (tmp_path / "b.py").write_text("y")
        r = await skill.execute(ctx, {"action": "list", "path": "."})
        assert r.success is True
        names = [e["name"] for e in r.output]
        assert "a.py" in names and "b.py" in names

    async def test_exists_true(self, skill, ctx, tmp_path):
        (tmp_path / "exists.txt").write_text("x")
        r = await skill.execute(ctx, {"action": "exists", "path": "exists.txt"})
        assert r.success and r.output is True

    async def test_exists_false(self, skill, ctx):
        r = await skill.execute(ctx, {"action": "exists", "path": "nope.txt"})
        assert r.success and r.output is False

    async def test_delete(self, skill, ctx, tmp_path):
        p = tmp_path / "del.txt"
        p.write_text("bye")
        r = await skill.execute(ctx, {"action": "delete", "path": "del.txt"})
        assert r.success is True
        assert not p.exists()

    async def test_read_missing_file(self, skill, ctx):
        r = await skill.execute(ctx, {"action": "read", "path": "ghost.txt"})
        assert r.success is False
        assert "not found" in r.error.lower()

    async def test_path_traversal_blocked(self, skill, ctx):
        r = await skill.execute(ctx, {"action": "read", "path": "../../etc/passwd"})
        assert r.success is False
        assert "escapes" in r.error

    async def test_missing_action(self, skill, ctx):
        r = await skill.execute(ctx, {"path": "x.txt"})
        assert r.success is False

    async def test_missing_path(self, skill, ctx):
        r = await skill.execute(ctx, {"action": "read"})
        assert r.success is False

    async def test_unknown_action(self, skill, ctx):
        r = await skill.execute(ctx, {"action": "destroy", "path": "x.txt"})
        assert r.success is False
