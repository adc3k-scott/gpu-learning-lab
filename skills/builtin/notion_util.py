"""
notion_util.py — Reusable Notion API utility module for Mission Control

Drop-in helpers for all Notion scripting. Import this instead of rewriting
auth, pagination, and block manipulation boilerplate every session.

Usage (in temp scripts):
    import sys; sys.path.insert(0, '.')
    from skills.builtin.notion_util import NotionClient, print_tree

Or standalone:
    from notion_util import NotionClient

All methods are synchronous (requests-based) for use in temp scripts.
For async skill use, see the async client in marlie_notion.py.

KNOWN API LIMITATIONS:
- Workspace root moves: PATCH {"parent": {"type": "workspace"}} is silently rejected.
  Pages can only be moved to workspace root via Notion UI (right-click → Move To).
- Always verify page ID after create_page(): call nc.get_page(id) to confirm.
  Build script stdout can truncate IDs (Windows cp1252 encoding), causing 404s later.
- Always use encode="utf-8" in print_tree() on Windows: print_tree(encode="utf-8")
"""

from __future__ import annotations

import os
import sys
from typing import Any

import requests

# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

def get_token() -> str:
    """Load NOTION_API_KEY from env or .env / .venv/.env files."""
    token = os.environ.get("NOTION_API_KEY")
    if token:
        return token
    for path in [".env", ".venv/.env"]:
        if os.path.exists(path):
            for line in open(path):
                if line.startswith("NOTION_API_KEY="):
                    return line.strip().split("=", 1)[1]
    raise RuntimeError("NOTION_API_KEY not found in environment or .env files")


# ---------------------------------------------------------------------------
# Core client
# ---------------------------------------------------------------------------

class NotionClient:
    """Synchronous Notion API client with pagination and block helpers."""

    BASE = "https://api.notion.com/v1"
    VERSION = "2022-06-28"

    def __init__(self, token: str | None = None):
        tok = token or get_token()
        self.headers = {
            "Authorization": f"Bearer {tok}",
            "Notion-Version": self.VERSION,
            "Content-Type": "application/json",
        }

    # -----------------------------------------------------------------------
    # Low-level
    # -----------------------------------------------------------------------

    def get(self, path: str, params: dict | None = None) -> dict:
        r = requests.get(f"{self.BASE}{path}", headers=self.headers, params=params)
        r.raise_for_status()
        return r.json()

    def post(self, path: str, body: dict) -> dict:
        r = requests.post(f"{self.BASE}{path}", headers=self.headers, json=body)
        r.raise_for_status()
        return r.json()

    def patch(self, path: str, body: dict) -> dict:
        r = requests.patch(f"{self.BASE}{path}", headers=self.headers, json=body)
        r.raise_for_status()
        return r.json()

    def delete(self, path: str) -> dict:
        r = requests.delete(f"{self.BASE}{path}", headers=self.headers)
        r.raise_for_status()
        return r.json()

    # -----------------------------------------------------------------------
    # Pages
    # -----------------------------------------------------------------------

    def get_page(self, page_id: str) -> dict:
        return self.get(f"/pages/{page_id}")

    def create_page(self, parent_id: str, title: str, icon: str = "📄",
                    children: list | None = None) -> dict:
        payload: dict[str, Any] = {
            "parent": {"page_id": parent_id},
            "icon": {"type": "emoji", "emoji": icon},
            "properties": {"title": {"title": [{"text": {"content": title}}]}},
        }
        if children:
            payload["children"] = children[:100]
        return self.post("/pages", payload)

    # -----------------------------------------------------------------------
    # Blocks
    # -----------------------------------------------------------------------

    def get_blocks(self, block_id: str) -> list[dict]:
        """Fetch all children of a block/page (handles pagination)."""
        results = []
        cursor = None
        while True:
            params = {"page_size": 100}
            if cursor:
                params["start_cursor"] = cursor
            data = self.get(f"/blocks/{block_id}/children", params=params)
            results.extend(data.get("results", []))
            if not data.get("has_more"):
                break
            cursor = data.get("next_cursor")
        return results

    def append_blocks(self, block_id: str, blocks: list[dict],
                      after: str | None = None) -> dict:
        """Append blocks to a page. Use after= to insert after a specific block."""
        body: dict = {"children": blocks}
        if after:
            body["after"] = after
        return self.patch(f"/blocks/{block_id}/children", body)

    def update_block(self, block_id: str, block_type: str, payload: dict) -> dict:
        """Update a block's content. payload is the type-specific dict."""
        return self.patch(f"/blocks/{block_id}", {block_type: payload})

    def update_text_block(self, block_id: str, block_type: str, text: str,
                          annotations: dict | None = None) -> dict:
        """Convenience: update any text block (paragraph, heading, callout, etc.)."""
        rich = [{"type": "text", "text": {"content": text}}]
        if annotations:
            rich[0]["annotations"] = annotations
        payload: dict = {"rich_text": rich}
        return self.patch(f"/blocks/{block_id}", {block_type: payload})

    def delete_block(self, block_id: str) -> dict:
        return self.delete(f"/blocks/{block_id}")

    def block_text(self, block: dict) -> str:
        """Extract plain text from any block."""
        btype = block.get("type", "")
        if btype not in block:
            return ""
        return "".join(
            r.get("plain_text", "")
            for r in block[btype].get("rich_text", [])
        )

    # -----------------------------------------------------------------------
    # Tables
    # -----------------------------------------------------------------------

    def get_table_rows(self, table_id: str) -> list[dict]:
        """Get all rows of a table block."""
        return [
            b for b in self.get_blocks(table_id)
            if b.get("type") == "table_row"
        ]

    def get_table_row_texts(self, table_id: str) -> list[list[str]]:
        """Return table as list of rows, each row as list of cell strings."""
        rows = []
        for row in self.get_table_rows(table_id):
            cells = row.get("table_row", {}).get("cells", [])
            rows.append(["".join(t.get("plain_text", "") for t in cell) for cell in cells])
        return rows

    def update_table_row(self, row_id: str, cell_texts: list[str]) -> dict:
        """Update a table row with plain-text cell values."""
        cells = [[{"type": "text", "text": {"content": t}}] for t in cell_texts]
        return self.patch(f"/blocks/{row_id}", {"table_row": {"cells": cells}})

    def find_table_rows_with(self, table_id: str, keyword: str) -> list[dict]:
        """Return table_row blocks whose text contains keyword (case-insensitive)."""
        kw = keyword.lower()
        results = []
        for row in self.get_table_rows(table_id):
            cells = row.get("table_row", {}).get("cells", [])
            row_text = " ".join("".join(t.get("plain_text", "") for t in cell) for cell in cells)
            if kw in row_text.lower():
                results.append(row)
        return results

    # -----------------------------------------------------------------------
    # Search
    # -----------------------------------------------------------------------

    def search_all(self, obj_type: str = "page") -> list[dict]:
        """Fetch ALL pages or databases from the workspace (paginated)."""
        results = []
        cursor = None
        while True:
            body: dict = {
                "page_size": 100,
                "filter": {"value": obj_type, "property": "object"},
            }
            if cursor:
                body["start_cursor"] = cursor
            data = self.post("/search", body)
            results.extend(data.get("results", []))
            if not data.get("has_more"):
                break
            cursor = data.get("next_cursor")
        return results

    def search(self, query: str, obj_type: str = "page") -> list[dict]:
        """Search by title query."""
        body = {
            "query": query,
            "page_size": 20,
            "filter": {"value": obj_type, "property": "object"},
        }
        return self.post("/search", body).get("results", [])

    def find_page(self, title: str) -> dict | None:
        """Find the first page matching a title substring."""
        for p in self.search(title):
            if title.lower() in get_title(p).lower():
                return p
        return None

    # -----------------------------------------------------------------------
    # Workspace tree
    # -----------------------------------------------------------------------

    def full_tree(self) -> dict[str, list[str]]:
        """
        Build the full workspace object map.
        Returns {parent_id: [child_id, ...]} and {id: obj} lookup.
        """
        all_objs = self.search_all("page") + self.search_all("database")
        by_id: dict[str, dict] = {o["id"].replace("-", ""): o for o in all_objs}
        children: dict[str, list[str]] = {}
        roots: list[str] = []

        for obj in all_objs:
            oid = obj["id"].replace("-", "")
            p = obj.get("parent", {})
            pt = p.get("type", "")
            pid = None
            if pt == "page_id":
                pid = p["page_id"].replace("-", "")
            elif pt == "database_id":
                pid = p["database_id"].replace("-", "")

            if pid and pid in by_id:
                children.setdefault(pid, []).append(oid)
            else:
                roots.append(oid)

        return {"by_id": by_id, "children": children, "roots": roots}


# ---------------------------------------------------------------------------
# Block constructors
# ---------------------------------------------------------------------------

def h1(text: str) -> dict:
    return {"object": "block", "type": "heading_1",
            "heading_1": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def h2(text: str) -> dict:
    return {"object": "block", "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def h3(text: str) -> dict:
    return {"object": "block", "type": "heading_3",
            "heading_3": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def para(text: str) -> dict:
    return {"object": "block", "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def bullet(text: str) -> dict:
    return {"object": "block", "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def numbered(text: str) -> dict:
    return {"object": "block", "type": "numbered_list_item",
            "numbered_list_item": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def callout(text: str, emoji: str = "💡", color: str = "gray_background") -> dict:
    return {"object": "block", "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {"content": text}}],
                "icon": {"type": "emoji", "emoji": emoji},
                "color": color,
            }}

def divider() -> dict:
    return {"object": "block", "type": "divider", "divider": {}}

def quote(text: str) -> dict:
    return {"object": "block", "type": "quote",
            "quote": {"rich_text": [{"type": "text", "text": {"content": text}}]}}


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def get_title(obj: dict) -> str:
    """Extract title from a page or database object."""
    if obj.get("object") == "database":
        title_arr = obj.get("title", [])
    else:
        props = obj.get("properties", {})
        title_arr = []
        for v in props.values():
            if isinstance(v, dict) and v.get("type") == "title":
                title_arr = v.get("title", [])
                break
    result = "".join(t.get("plain_text", "") for t in title_arr) or "(untitled)"
    try:
        result = result.encode('utf-16-le', 'surrogatepass').decode('utf-16-le')
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass
    return result


def print_tree(client: NotionClient | None = None, encode: str = "utf-8") -> None:
    """
    Print the full Notion workspace as an indented tree.
    Standard for 'show me files' requests.
    """
    sys.stdout.reconfigure(encoding=encode, errors="replace")  # type: ignore[attr-defined]
    nc = client or NotionClient()
    tree = nc.full_tree()
    by_id = tree["by_id"]
    children = tree["children"]
    roots = tree["roots"]

    total = len(by_id)
    print(f"Total objects: {total}\n")
    print("=== NOTION WORKSPACE TREE ===\n")

    def _print(oid: str, indent: int = 0) -> None:
        obj = by_id.get(oid)
        if not obj:
            return
        prefix = "  " * indent
        label = "[DB]" if obj.get("object") == "database" else "[PAGE]"
        title = get_title(obj)
        short_id = obj["id"][:8]
        print(f"{prefix}{label} {title}  ({short_id})")
        for child in sorted(children.get(oid, []), key=lambda x: get_title(by_id.get(x, {}))):
            _print(child, indent + 1)

    for rid in roots:
        _print(rid)
        print()


def find_blocks_with_text(blocks: list[dict], keyword: str,
                          block_types: list[str] | None = None) -> list[dict]:
    """Filter blocks containing keyword in their text content."""
    kw = keyword.lower()
    results = []
    for b in blocks:
        btype = b.get("type", "")
        if block_types and btype not in block_types:
            continue
        if btype in b:
            text = "".join(r.get("plain_text", "") for r in b[btype].get("rich_text", []))
            if kw in text.lower():
                results.append(b)
    return results


# ---------------------------------------------------------------------------
# Standalone: python notion_util.py  →  print workspace tree
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print_tree()
