"""
notion_backup.py — Export Notion workspace to markdown files in notion-backup/

Walks the entire workspace tree, fetches block content for each page,
converts to markdown, saves to notion-backup/<Section>/<Page Title>.md

Run: python scripts/notion_backup.py
"""

import os, sys, re
from pathlib import Path
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from skills.builtin.notion_util import NotionClient, get_title

BACKUP_DIR = Path(__file__).parent.parent / "notion-backup"

# ---------------------------------------------------------------------------
# Block → Markdown converter
# ---------------------------------------------------------------------------

def block_to_md(block: dict, nc: NotionClient, depth: int = 0) -> str:
    btype = block.get("type", "")
    indent = "  " * depth

    def rich_text(arr):
        return "".join(r.get("plain_text", "") for r in arr)

    def get_rt(key):
        return rich_text(block.get(btype, {}).get("rich_text", []))

    lines = []

    if btype == "heading_1":
        lines.append(f"# {get_rt('heading_1')}")
    elif btype == "heading_2":
        lines.append(f"## {get_rt('heading_2')}")
    elif btype == "heading_3":
        lines.append(f"### {get_rt('heading_3')}")
    elif btype == "paragraph":
        text = get_rt("paragraph")
        lines.append(text if text else "")
    elif btype == "bulleted_list_item":
        lines.append(f"{indent}- {get_rt('bulleted_list_item')}")
    elif btype == "numbered_list_item":
        lines.append(f"{indent}1. {get_rt('numbered_list_item')}")
    elif btype == "to_do":
        checked = block.get("to_do", {}).get("checked", False)
        mark = "x" if checked else " "
        lines.append(f"{indent}- [{mark}] {get_rt('to_do')}")
    elif btype == "toggle":
        lines.append(f"{indent}> {get_rt('toggle')}")
    elif btype == "callout":
        lines.append(f"> {get_rt('callout')}")
    elif btype == "quote":
        lines.append(f"> {get_rt('quote')}")
    elif btype == "code":
        lang = block.get("code", {}).get("language", "")
        code = get_rt("code")
        lines.append(f"```{lang}\n{code}\n```")
    elif btype == "divider":
        lines.append("---")
    elif btype == "image":
        img = block.get("image", {})
        url = img.get("file", {}).get("url", "") or img.get("external", {}).get("url", "")
        caption = rich_text(img.get("caption", []))
        lines.append(f"![{caption}]({url})")
    elif btype == "table":
        # handled by children (table_row)
        pass
    elif btype == "table_row":
        cells = block.get("table_row", {}).get("cells", [])
        row = " | ".join(rich_text(cell) for cell in cells)
        lines.append(f"| {row} |")
    elif btype in ("child_page", "child_database"):
        title = block.get(btype, {}).get("title", "(child)")
        lines.append(f"*[Child: {title}]*")
    else:
        # fallback — try to get any text
        inner = block.get(btype, {})
        if isinstance(inner, dict):
            rt = rich_text(inner.get("rich_text", []))
            if rt:
                lines.append(rt)

    # Recurse into children if block has them
    if block.get("has_children"):
        try:
            children = nc.get_blocks(block["id"])
            for child in children:
                child_md = block_to_md(child, nc, depth + 1)
                if child_md:
                    lines.append(child_md)
        except Exception:
            pass

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Page exporter
# ---------------------------------------------------------------------------

def safe_filename(title: str) -> str:
    # Strip emoji and other non-ASCII characters
    title = re.sub(r'[^\x00-\x7F]', '', title).strip()
    # Strip Windows-illegal chars
    title = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '-', title)
    title = re.sub(r'-+', '-', title).strip('-').strip()
    return title[:60] or "untitled"


def export_page(page_id: str, title: str, folder: Path, nc: NotionClient) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    filepath = folder / f"{safe_filename(title)}.md"

    try:
        blocks = nc.get_blocks(page_id)
    except Exception as e:
        print(f"  SKIP (API error): {title} — {e}")
        return

    if not blocks:
        print(f"  EMPTY: {title}")
        return

    lines = [f"# {title}", f"*Notion backup — {datetime.now().strftime('%Y-%m-%d')}*", ""]
    for block in blocks:
        md = block_to_md(block, nc)
        if md:
            lines.append(md)

    filepath.write_text("\n".join(lines), encoding="utf-8")
    print(f"  OK: {filepath.relative_to(BACKUP_DIR.parent)}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(f"Notion Backup — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Output: {BACKUP_DIR}")
    print()

    nc = NotionClient()
    tree = nc.full_tree()
    by_id = tree["by_id"]
    children = tree["children"]
    roots = tree["roots"]

    # Clear and recreate backup dir
    import shutil
    if BACKUP_DIR.exists():
        shutil.rmtree(BACKUP_DIR)
    BACKUP_DIR.mkdir(parents=True)

    exported = 0
    skipped = 0

    def walk(oid: str, folder: Path, depth: int = 0) -> None:
        nonlocal exported, skipped
        obj = by_id.get(oid)
        if not obj:
            return

        title = get_title(obj)
        obj_type = obj.get("object", "page")

        if obj_type == "database":
            # Databases: recurse into child pages using same folder
            for child_id in children.get(oid, []):
                walk(child_id, folder, depth)
            return

        # It's a page — export it
        print(f"Exporting: {title}")
        export_page(oid, title, folder, nc)
        exported += 1

        # Recurse into children — max 1 subfolder level to avoid deep paths
        child_ids = children.get(oid, [])
        if child_ids:
            if depth < 1:
                subfolder = folder / safe_filename(title)
            else:
                subfolder = folder  # flatten beyond depth 1
            for child_id in child_ids:
                walk(child_id, subfolder, depth + 1)

    for rid in roots:
        obj = by_id.get(rid)
        if not obj:
            continue
        root_title = get_title(obj)
        root_folder = BACKUP_DIR / safe_filename(root_title)
        walk(rid, root_folder)

    print()
    print(f"Done. Exported: {exported} pages. Skipped: {skipped}.")
    print(f"Location: {BACKUP_DIR}")


if __name__ == "__main__":
    main()
