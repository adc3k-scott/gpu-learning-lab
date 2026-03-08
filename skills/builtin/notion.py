"""
Built-in skill: notion

Interact with the Notion API to read and write workspace content.

Supported actions:
  get_page        — fetch a page's properties and metadata (requires page_id)
  get_page_blocks — fetch all block children of a page (requires page_id)
  create_page     — create a new page in a database or as a child page
                    (requires parent_id, title; optionally properties, blocks)
  update_page     — update page properties (requires page_id, properties)
  append_blocks   — append block children to a page (requires page_id, blocks)
  query_database  — query a Notion database with optional filter/sort
                    (requires database_id; optionally filter, sorts, page_size)
  search          — full-text search across the workspace (requires query)

Credentials:
  The skill reads the API key from ctx.metadata["notion_api_key"] first,
  then falls back to the NOTION_API_KEY environment variable.

Block format (for create_page / append_blocks):
  Blocks are Notion API block objects. The simplest form:
    {"type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "Hello"}}]}}
  The _make_paragraph() helper generates these from plain strings.
"""

from __future__ import annotations

import logging
import os
from typing import Any

import httpx

from skills.base import BaseSkill, SkillContext, SkillResult

logger = logging.getLogger(__name__)

_NOTION_BASE = "https://api.notion.com/v1"
_NOTION_VERSION = "2022-06-28"
_TIMEOUT = 15.0
_MAX_RESULTS = 100    # cap for query_database page_size


class NotionSkill(BaseSkill):
    name = "notion"
    description = (
        "Read and write Notion workspace content — pages, databases, and blocks. "
        "Create pages, query databases, search, and append content."
    )
    version = "0.1.0"
    required_secrets = ["NOTION_API_KEY"]

    async def execute(self, ctx: SkillContext, params: dict[str, Any]) -> SkillResult:
        action = params.get("action", "")
        if not action:
            return SkillResult.fail("Missing required parameter: action")

        api_key = (
            ctx.metadata.get("notion_api_key")
            or os.environ.get("NOTION_API_KEY", "")
        )
        if not api_key:
            return SkillResult.fail(
                "Notion API key not configured. "
                "Set NOTION_API_KEY in .env or pass notion_api_key in skill metadata."
            )

        try:
            result = await self._dispatch(action, params, api_key)
            return SkillResult.ok(output=result)
        except _NotionError as exc:
            return SkillResult.fail(str(exc))
        except Exception as exc:
            logger.exception("notion skill error: %s", exc)
            return SkillResult.fail(str(exc))

    # ------------------------------------------------------------------
    # Dispatch
    # ------------------------------------------------------------------

    async def _dispatch(self, action: str, params: dict[str, Any], api_key: str) -> Any:
        client = _NotionClient(api_key)

        if action == "get_page":
            return await client.get(f"pages/{_require(params, 'page_id')}")

        if action == "get_page_blocks":
            return await client.get(f"blocks/{_require(params, 'page_id')}/children")

        if action == "create_page":
            body = _build_create_page(params)
            return await client.post("pages", body)

        if action == "update_page":
            page_id = _require(params, "page_id")
            body = {"properties": params.get("properties", {})}
            if "archived" in params:
                body["archived"] = params["archived"]
            return await client.patch(f"pages/{page_id}", body)

        if action == "append_blocks":
            page_id = _require(params, "page_id")
            raw_blocks = params.get("blocks", [])
            blocks = _coerce_blocks(raw_blocks)
            return await client.patch(f"blocks/{page_id}/children", {"children": blocks})

        if action == "query_database":
            db_id = _require(params, "database_id")
            body: dict[str, Any] = {}
            if params.get("filter"):
                body["filter"] = params["filter"]
            if params.get("sorts"):
                body["sorts"] = params["sorts"]
            body["page_size"] = min(int(params.get("page_size", 50)), _MAX_RESULTS)
            if params.get("start_cursor"):
                body["start_cursor"] = params["start_cursor"]
            return await client.post(f"databases/{db_id}/query", body)

        if action == "search":
            q = params.get("query", "")
            body = {"query": q}
            if params.get("filter"):
                body["filter"] = params["filter"]
            if params.get("sort"):
                body["sort"] = params["sort"]
            return await client.post("search", body)

        valid = "get_page, get_page_blocks, create_page, update_page, append_blocks, query_database, search"
        raise _NotionError(f"Unknown action {action!r}. Choose: {valid}")


# ---------------------------------------------------------------------------
# HTTP client wrapper
# ---------------------------------------------------------------------------

class _NotionClient:
    def __init__(self, api_key: str) -> None:
        self._headers = {
            "Authorization": f"Bearer {api_key}",
            "Notion-Version": _NOTION_VERSION,
            "Content-Type": "application/json",
        }

    async def get(self, path: str) -> Any:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            resp = await client.get(f"{_NOTION_BASE}/{path}", headers=self._headers)
        return _handle(resp)

    async def post(self, path: str, body: dict) -> Any:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            resp = await client.post(f"{_NOTION_BASE}/{path}", json=body, headers=self._headers)
        return _handle(resp)

    async def patch(self, path: str, body: dict) -> Any:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            resp = await client.patch(f"{_NOTION_BASE}/{path}", json=body, headers=self._headers)
        return _handle(resp)


def _handle(resp: httpx.Response) -> Any:
    if not resp.is_success:
        try:
            detail = resp.json().get("message", resp.text[:300])
        except Exception:
            detail = resp.text[:300]
        raise _NotionError(f"Notion API HTTP {resp.status_code}: {detail}")
    return resp.json()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

class _NotionError(RuntimeError):
    pass


def _require(params: dict, key: str) -> str:
    val = params.get(key, "")
    if not val:
        raise _NotionError(f"Missing required parameter: {key}")
    return str(val)


def _build_create_page(params: dict[str, Any]) -> dict[str, Any]:
    parent_id = _require(params, "parent_id")
    parent_type = params.get("parent_type", "database_id")  # "database_id" or "page_id"

    title = params.get("title", "Untitled")
    properties: dict[str, Any] = params.get("properties") or {}

    # Ensure the title property is set if not already in properties
    if "title" not in {k.lower() for k in properties}:
        properties["title"] = {
            "title": [{"text": {"content": title}}]
        }

    body: dict[str, Any] = {
        "parent": {parent_type: parent_id},
        "properties": properties,
    }

    raw_blocks = params.get("blocks", [])
    if raw_blocks:
        body["children"] = _coerce_blocks(raw_blocks)

    return body


def _coerce_blocks(blocks: list) -> list[dict]:
    """
    Accept either proper Notion block dicts or plain strings.
    Plain strings become paragraph blocks.
    """
    result = []
    for b in blocks:
        if isinstance(b, str):
            result.append(_make_paragraph(b))
        elif isinstance(b, dict):
            result.append(b)
    return result


def _make_paragraph(text: str) -> dict:
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": text}}]
        },
    }
