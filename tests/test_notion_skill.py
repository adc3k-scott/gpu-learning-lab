"""Tests for the notion built-in skill."""

from __future__ import annotations

import json
import pytest
import httpx

from skills.base import SkillContext, SkillResult
from skills.builtin.notion import NotionSkill, _make_paragraph, _coerce_blocks
from skills.registry import SkillRegistry


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_ctx(api_key: str = "secret_test_key") -> SkillContext:
    return SkillContext(
        agent_id="test",
        job_id="j1",
        metadata={"notion_api_key": api_key},
    )


def notion_response(data: dict, status_code: int = 200) -> httpx.Response:
    return httpx.Response(
        status_code=status_code,
        content=json.dumps(data).encode(),
        headers={"content-type": "application/json"},
    )


def error_response(message: str, status_code: int = 400) -> httpx.Response:
    return httpx.Response(
        status_code=status_code,
        content=json.dumps({"object": "error", "message": message}).encode(),
        headers={"content-type": "application/json"},
    )


# ---------------------------------------------------------------------------
# Skill metadata
# ---------------------------------------------------------------------------

class TestNotionSkillMeta:
    def test_name(self):
        assert NotionSkill.name == "notion"

    def test_description_not_empty(self):
        assert len(NotionSkill.description) > 10

    def test_required_secrets(self):
        assert "NOTION_API_KEY" in NotionSkill.required_secrets

    def test_registry_discovers_skill(self):
        reg = SkillRegistry()
        reg.discover()
        assert reg.get("notion") is not None


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

class TestNotionSkillValidation:
    async def test_missing_action_fails(self):
        skill = NotionSkill()
        result = await skill.execute(make_ctx(), {})
        assert result.success is False
        assert "action" in result.error.lower()

    async def test_missing_api_key_fails(self):
        skill = NotionSkill()
        ctx = SkillContext(agent_id="test", job_id="j1")  # no key in metadata or env
        result = await skill.execute(ctx, {"action": "search", "query": "hello"})
        assert result.success is False
        assert "notion api key" in result.error.lower()

    async def test_unknown_action_fails(self, monkeypatch):
        skill = NotionSkill()
        result = await skill.execute(make_ctx(), {"action": "delete_everything"})
        assert result.success is False
        assert "unknown action" in result.error.lower()

    async def test_get_page_requires_page_id(self, monkeypatch):
        skill = NotionSkill()
        result = await skill.execute(make_ctx(), {"action": "get_page"})
        assert result.success is False
        assert "page_id" in result.error.lower()

    async def test_query_database_requires_database_id(self, monkeypatch):
        skill = NotionSkill()
        result = await skill.execute(make_ctx(), {"action": "query_database"})
        assert result.success is False
        assert "database_id" in result.error.lower()

    async def test_create_page_requires_parent_id(self, monkeypatch):
        skill = NotionSkill()
        result = await skill.execute(make_ctx(), {"action": "create_page", "title": "Test"})
        assert result.success is False
        assert "parent_id" in result.error.lower()


# ---------------------------------------------------------------------------
# get_page
# ---------------------------------------------------------------------------

class TestNotionGetPage:
    async def test_get_page_success(self, monkeypatch):
        skill = NotionSkill()
        page_data = {"object": "page", "id": "abc123", "properties": {}}

        async def mock_get(self_client, url, **kwargs):
            assert "pages/abc123" in url
            return notion_response(page_data)

        monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)
        result = await skill.execute(make_ctx(), {"action": "get_page", "page_id": "abc123"})
        assert result.success is True
        assert result.output["id"] == "abc123"

    async def test_get_page_sends_auth_header(self, monkeypatch):
        skill = NotionSkill()
        captured_headers = {}

        async def mock_get(self_client, url, **kwargs):
            captured_headers.update(kwargs.get("headers", {}))
            return notion_response({"object": "page", "id": "p1"})

        monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)
        await skill.execute(make_ctx("secret_mykey"), {"action": "get_page", "page_id": "p1"})
        assert captured_headers.get("Authorization") == "Bearer secret_mykey"
        assert captured_headers.get("Notion-Version") == "2022-06-28"

    async def test_get_page_api_error_fails(self, monkeypatch):
        skill = NotionSkill()

        async def mock_get(self_client, url, **kwargs):
            return error_response("object_not_found", 404)

        monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)
        result = await skill.execute(make_ctx(), {"action": "get_page", "page_id": "missing"})
        assert result.success is False
        assert "404" in result.error


# ---------------------------------------------------------------------------
# search
# ---------------------------------------------------------------------------

class TestNotionSearch:
    async def test_search_sends_query(self, monkeypatch):
        skill = NotionSkill()
        captured_body = {}
        search_data = {"object": "list", "results": []}

        async def mock_post(self_client, url, **kwargs):
            captured_body.update(kwargs.get("json", {}))
            return notion_response(search_data)

        monkeypatch.setattr(httpx.AsyncClient, "post", mock_post)
        result = await skill.execute(make_ctx(), {"action": "search", "query": "meeting notes"})
        assert result.success is True
        assert captured_body.get("query") == "meeting notes"

    async def test_search_with_filter(self, monkeypatch):
        skill = NotionSkill()
        captured_body = {}

        async def mock_post(self_client, url, **kwargs):
            captured_body.update(kwargs.get("json", {}))
            return notion_response({"object": "list", "results": []})

        monkeypatch.setattr(httpx.AsyncClient, "post", mock_post)
        await skill.execute(make_ctx(), {
            "action": "search",
            "query": "standup",
            "filter": {"value": "page", "property": "object"},
        })
        assert captured_body.get("filter") == {"value": "page", "property": "object"}


# ---------------------------------------------------------------------------
# create_page
# ---------------------------------------------------------------------------

class TestNotionCreatePage:
    async def test_create_page_sets_title(self, monkeypatch):
        skill = NotionSkill()
        captured_body = {}
        page_data = {"object": "page", "id": "newpage123"}

        async def mock_post(self_client, url, **kwargs):
            captured_body.update(kwargs.get("json", {}))
            return notion_response(page_data)

        monkeypatch.setattr(httpx.AsyncClient, "post", mock_post)
        result = await skill.execute(make_ctx(), {
            "action": "create_page",
            "parent_id": "db-uuid-123",
            "parent_type": "database_id",
            "title": "My New Page",
        })
        assert result.success is True
        assert captured_body["parent"] == {"database_id": "db-uuid-123"}
        title_prop = captured_body["properties"].get("title", {})
        assert title_prop["title"][0]["text"]["content"] == "My New Page"

    async def test_create_page_with_blocks(self, monkeypatch):
        skill = NotionSkill()
        captured_body = {}

        async def mock_post(self_client, url, **kwargs):
            captured_body.update(kwargs.get("json", {}))
            return notion_response({"object": "page", "id": "p2"})

        monkeypatch.setattr(httpx.AsyncClient, "post", mock_post)
        await skill.execute(make_ctx(), {
            "action": "create_page",
            "parent_id": "page-uuid",
            "parent_type": "page_id",
            "title": "Notes",
            "blocks": ["First paragraph", "Second paragraph"],
        })
        children = captured_body.get("children", [])
        assert len(children) == 2
        assert children[0]["type"] == "paragraph"


# ---------------------------------------------------------------------------
# query_database
# ---------------------------------------------------------------------------

class TestNotionQueryDatabase:
    async def test_query_database_sends_db_id(self, monkeypatch):
        skill = NotionSkill()
        captured_url = []

        async def mock_post(self_client, url, **kwargs):
            captured_url.append(url)
            return notion_response({"object": "list", "results": []})

        monkeypatch.setattr(httpx.AsyncClient, "post", mock_post)
        result = await skill.execute(make_ctx(), {
            "action": "query_database",
            "database_id": "my-db-id",
        })
        assert result.success is True
        assert "my-db-id" in captured_url[0]

    async def test_query_database_caps_page_size(self, monkeypatch):
        skill = NotionSkill()
        captured_body = {}

        async def mock_post(self_client, url, **kwargs):
            captured_body.update(kwargs.get("json", {}))
            return notion_response({"object": "list", "results": []})

        monkeypatch.setattr(httpx.AsyncClient, "post", mock_post)
        await skill.execute(make_ctx(), {
            "action": "query_database",
            "database_id": "db1",
            "page_size": 9999,  # should be capped at 100
        })
        assert captured_body["page_size"] == 100


# ---------------------------------------------------------------------------
# append_blocks
# ---------------------------------------------------------------------------

class TestNotionAppendBlocks:
    async def test_append_plain_strings_as_paragraphs(self, monkeypatch):
        skill = NotionSkill()
        captured_body = {}

        async def mock_patch(self_client, url, **kwargs):
            captured_body.update(kwargs.get("json", {}))
            return notion_response({"object": "list", "results": []})

        monkeypatch.setattr(httpx.AsyncClient, "patch", mock_patch)
        result = await skill.execute(make_ctx(), {
            "action": "append_blocks",
            "page_id": "page-abc",
            "blocks": ["Hello world", "Second line"],
        })
        assert result.success is True
        children = captured_body.get("children", [])
        assert len(children) == 2
        assert children[0]["type"] == "paragraph"
        assert children[0]["paragraph"]["rich_text"][0]["text"]["content"] == "Hello world"


# ---------------------------------------------------------------------------
# Block helpers
# ---------------------------------------------------------------------------

class TestBlockHelpers:
    def test_make_paragraph(self):
        block = _make_paragraph("Test text")
        assert block["type"] == "paragraph"
        assert block["paragraph"]["rich_text"][0]["text"]["content"] == "Test text"

    def test_coerce_blocks_strings(self):
        blocks = _coerce_blocks(["line one", "line two"])
        assert len(blocks) == 2
        assert all(b["type"] == "paragraph" for b in blocks)

    def test_coerce_blocks_passthrough_dicts(self):
        raw = [{"type": "heading_1", "heading_1": {"rich_text": []}}]
        blocks = _coerce_blocks(raw)
        assert blocks[0]["type"] == "heading_1"

    def test_coerce_blocks_mixed(self):
        raw = ["plain text", {"type": "divider", "divider": {}}]
        blocks = _coerce_blocks(raw)
        assert blocks[0]["type"] == "paragraph"
        assert blocks[1]["type"] == "divider"
