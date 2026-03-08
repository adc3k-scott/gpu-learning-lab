"""Tests for NotionSyncAgent."""

from __future__ import annotations

import asyncio
import pytest

from core.event_bus import Event, EventBus
from core.state_store import StateStore
from skills.registry import SkillRegistry
from agents.notion_sync import NotionSyncAgent
from agents.notion_sync.agent import _build_blocks


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
async def infra():
    bus = EventBus()
    store = StateStore()
    await bus.connect()
    await store.connect()
    yield bus, store
    await bus.disconnect()


@pytest.fixture
def reg():
    r = SkillRegistry()
    r.discover()
    return r


# ---------------------------------------------------------------------------
# Config management
# ---------------------------------------------------------------------------

class TestNotionSyncConfig:
    async def test_starts_unconfigured_by_default(self, infra, reg):
        bus, store = infra
        agent = NotionSyncAgent(bus=bus, store=store, registry=reg, project_root=".")
        await agent.start()
        cfg = agent.get_config()
        assert cfg["notion_work_db_id"] == ""
        assert cfg["notion_api_key_set"] == "no"
        await agent.stop()

    async def test_set_config_updates_db_id(self, infra, reg):
        bus, store = infra
        agent = NotionSyncAgent(bus=bus, store=store, registry=reg, project_root=".")
        await agent.start()
        agent.set_config(db_id="my-db-uuid")
        assert agent.get_config()["notion_work_db_id"] == "my-db-uuid"
        await agent.stop()

    async def test_set_config_updates_api_key(self, infra, reg):
        bus, store = infra
        agent = NotionSyncAgent(bus=bus, store=store, registry=reg, project_root=".")
        await agent.start()
        agent.set_config(api_key="secret_abc")
        assert agent.get_config()["notion_api_key_set"] == "yes"
        await agent.stop()

    async def test_reloads_config_from_store(self, infra, reg):
        bus, store = infra
        await store.set("config:notion_work_db_id", "store-db-id")
        await store.set("config:notion_api_key", "store-key")
        agent = NotionSyncAgent(bus=bus, store=store, registry=reg, project_root=".")
        await agent.start()
        assert agent._db_id == "store-db-id"
        assert agent._api_key == "store-key"
        await agent.stop()

    async def test_config_updated_event_reloads(self, infra, reg):
        bus, store = infra
        agent = NotionSyncAgent(bus=bus, store=store, registry=reg, project_root=".")
        await agent.start()

        # Store new value then fire config.updated
        await store.set("config:notion_work_db_id", "new-db-id")
        await bus.publish(Event(
            event_type="config.updated",
            payload={"key": "config:notion_work_db_id", "value": "new-db-id"},
        ))
        await asyncio.sleep(0.1)
        assert agent._db_id == "new-db-id"
        await agent.stop()


# ---------------------------------------------------------------------------
# Skip behaviour when unconfigured
# ---------------------------------------------------------------------------

class TestNotionSyncSkip:
    async def test_skips_when_no_db_id(self, infra, reg):
        bus, store = infra
        agent = NotionSyncAgent(bus=bus, store=store, registry=reg, project_root=".")
        agent.set_config(api_key="secret_key")  # key set, but no db id
        await agent.start()

        skipped = []
        bus.subscribe("notion.sync.skipped", lambda e: skipped.append(e.payload))

        # Persist a fake job so the agent can fetch it
        job_id = "job-skip-1"
        await store.set(f"jobs:{job_id}", {"job_id": job_id, "title": "Test", "status": "completed", "steps": []})
        await bus.publish(Event(event_type="job.completed", payload={"job_id": job_id}))
        await asyncio.sleep(0.2)

        assert any(s.get("job_id") == job_id for s in skipped)
        assert "NOTION_WORK_DB_ID" in skipped[0]["reason"]
        await agent.stop()

    async def test_skips_when_no_api_key(self, infra, reg):
        bus, store = infra
        agent = NotionSyncAgent(bus=bus, store=store, registry=reg, project_root=".")
        agent.set_config(db_id="db-uuid")  # db set, but no API key
        await agent.start()

        skipped = []
        bus.subscribe("notion.sync.skipped", lambda e: skipped.append(e.payload))

        job_id = "job-skip-2"
        await store.set(f"jobs:{job_id}", {"job_id": job_id, "title": "Test", "status": "completed", "steps": []})
        await bus.publish(Event(event_type="job.completed", payload={"job_id": job_id}))
        await asyncio.sleep(0.2)

        assert any(s.get("job_id") == job_id for s in skipped)
        await agent.stop()

    async def test_ignores_event_with_no_job_id(self, infra, reg):
        bus, store = infra
        agent = NotionSyncAgent(bus=bus, store=store, registry=reg, project_root=".")
        agent.set_config(db_id="db-uuid", api_key="secret_key")
        await agent.start()

        # Should not raise or publish anything
        await bus.publish(Event(event_type="job.completed", payload={}))
        await asyncio.sleep(0.1)
        await agent.stop()


# ---------------------------------------------------------------------------
# Sync via skill
# ---------------------------------------------------------------------------

class TestNotionSyncPageCreation:
    async def test_sync_creates_page_via_skill(self, infra, reg, monkeypatch):
        """When fully configured, job.completed should trigger notion create_page."""
        bus, store = infra

        # Patch the notion skill to avoid a real HTTP call
        created_pages = []

        from skills.builtin.notion import NotionSkill
        from skills.base import SkillResult

        async def mock_execute(self_skill, ctx, params):
            created_pages.append(params)
            return SkillResult.ok(output={"id": "page-abc", "url": "https://notion.so/page-abc"})

        monkeypatch.setattr(NotionSkill, "execute", mock_execute)

        agent = NotionSyncAgent(bus=bus, store=store, registry=reg, project_root=".")
        await agent.start()
        agent.set_config(db_id="work-db-id", api_key="secret_key")

        page_created = []
        bus.subscribe("notion.page.created", lambda e: page_created.append(e.payload))

        job_id = "job-sync-1"
        await store.set(f"jobs:{job_id}", {
            "job_id": job_id,
            "title": "List project files",
            "status": "completed",
            "steps": [
                {"name": "list_files", "status": "completed", "result": ["main.py", "CLAUDE.md"]},
            ],
        })
        await bus.publish(Event(event_type="job.completed", payload={"job_id": job_id}))
        await asyncio.sleep(0.3)

        assert len(created_pages) == 1
        assert created_pages[0]["action"] == "create_page"
        assert created_pages[0]["parent_id"] == "work-db-id"
        assert "List project files" in created_pages[0]["title"]

        assert len(page_created) == 1
        assert page_created[0]["job_id"] == job_id
        assert page_created[0]["page_id"] == "page-abc"

        await agent.stop()

    async def test_sync_error_emits_error_event(self, infra, reg, monkeypatch):
        bus, store = infra

        from skills.builtin.notion import NotionSkill
        from skills.base import SkillResult

        async def mock_execute(self_skill, ctx, params):
            return SkillResult.fail("Notion API error 500")

        monkeypatch.setattr(NotionSkill, "execute", mock_execute)

        agent = NotionSyncAgent(bus=bus, store=store, registry=reg, project_root=".")
        await agent.start()
        agent.set_config(db_id="db-uuid", api_key="secret_key")

        errors = []
        bus.subscribe("notion.sync.error", lambda e: errors.append(e.payload))

        job_id = "job-err-1"
        await store.set(f"jobs:{job_id}", {"job_id": job_id, "title": "Test", "status": "completed", "steps": []})
        await bus.publish(Event(event_type="job.completed", payload={"job_id": job_id}))
        await asyncio.sleep(0.3)

        assert len(errors) == 1
        assert errors[0]["job_id"] == job_id
        assert "Notion API error" in errors[0]["error"]

        await agent.stop()

    async def test_also_syncs_failed_jobs(self, infra, reg, monkeypatch):
        """Failed jobs should also be synced (as a failure record)."""
        bus, store = infra

        from skills.builtin.notion import NotionSkill
        from skills.base import SkillResult

        async def mock_execute(self_skill, ctx, params):
            return SkillResult.ok(output={"id": "page-fail", "url": "https://notion.so/fail"})

        monkeypatch.setattr(NotionSkill, "execute", mock_execute)

        agent = NotionSyncAgent(bus=bus, store=store, registry=reg, project_root=".")
        await agent.start()
        agent.set_config(db_id="db-uuid", api_key="secret_key")

        page_created = []
        bus.subscribe("notion.page.created", lambda e: page_created.append(e.payload))

        job_id = "job-fail-1"
        await store.set(f"jobs:{job_id}", {
            "job_id": job_id, "title": "Failed task", "status": "failed",
            "error": "Step timed out", "steps": [],
        })
        await bus.publish(Event(event_type="job.failed", payload={"job_id": job_id}))
        await asyncio.sleep(0.3)

        assert len(page_created) == 1
        await agent.stop()


# ---------------------------------------------------------------------------
# Block builder
# ---------------------------------------------------------------------------

class TestBuildBlocks:
    def test_builds_blocks_for_completed_job(self):
        steps = [
            {"name": "list_files", "status": "completed", "result": "main.py\ntest.py"},
            {"name": "read_file",  "status": "completed", "result": "# hello"},
        ]
        blocks = _build_blocks("job-123", "completed", steps, "")
        types = [b["type"] for b in blocks]
        assert "callout" in types
        assert "code" in types

    def test_error_message_included(self):
        blocks = _build_blocks("job-456", "failed", [], "Something went wrong")
        text = " ".join(
            rt["text"]["content"]
            for b in blocks if b["type"] == "paragraph"
            for rt in b.get("paragraph", {}).get("rich_text", [])
        )
        assert "Something went wrong" in text

    def test_long_result_split_into_chunks(self):
        long_result = "x" * 4000
        steps = [{"name": "big_step", "status": "completed", "result": long_result}]
        blocks = _build_blocks("job-789", "completed", steps, "")
        code_blocks = [b for b in blocks if b["type"] == "code"]
        # 4000 chars → 3 chunks of ≤1900
        assert len(code_blocks) >= 2
        for cb in code_blocks:
            content = cb["code"]["rich_text"][0]["text"]["content"]
            assert len(content) <= 1900

    def test_no_steps_still_returns_blocks(self):
        blocks = _build_blocks("job-000", "completed", [], "")
        assert len(blocks) > 0
