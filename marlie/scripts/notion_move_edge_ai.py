"""
Copy Edge AI pages into Edge AI Infrastructure Documents folder, then archive originals.
Notion API does not support reparenting via PATCH — must copy content + archive.
"""
import httpx, sys, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

KEY = "NOTION_API_TOKEN_REDACTED"
HEADERS = {
    "Authorization": f"Bearer {KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

EDGE_AI_FOLDER = "31d88f09-7e31-8136-a572-e7e1b0008ad2"

PAGES_TO_MOVE = [
    ("31588f09-7e31-815a-a20f-daaf4ac86ace", "Edge AI Infrastructure Upgrade — Master Prompt"),
    ("31588f09-7e31-81b9-88bb-fcd241ce1282", "Edge AI Upgrade — Part 1: Executive Summary Rewrites"),
    ("31588f09-7e31-81bb-9a03-e062421de5f6", "Edge AI Upgrade — Part 2: Edge Infrastructure Positioning"),
    ("31588f09-7e31-81ca-a956-c735ccd1a3a3", "Edge AI Upgrade — Part 3: Bloom Energy Power Architecture"),
    ("31588f09-7e31-81e7-b5eb-f9a81fc000fc", "Edge AI Upgrade — Part 4: Terminology Map, Site Strategy & Roadmap"),
]


def api(method, path, data=None):
    r = httpx.request(method, f"https://api.notion.com/v1{path}", headers=HEADERS, json=data, timeout=30)
    if r.status_code not in (200, 201):
        print(f"  API ERROR {r.status_code}: {r.text[:200]}")
        return None
    return r.json()


def get_all_blocks(page_id):
    """Fetch all top-level blocks, paginating if needed."""
    blocks = []
    cursor = None
    while True:
        path = f"/blocks/{page_id}/children?page_size=100"
        if cursor:
            path += f"&start_cursor={cursor}"
        data = api("GET", path)
        if not data:
            break
        blocks.extend(data.get("results", []))
        if not data.get("has_more"):
            break
        cursor = data.get("next_cursor")
    return blocks


def clean_block(block):
    """Strip read-only fields, keep only the content."""
    btype = block.get("type")
    if not btype:
        return None
    content = block.get(btype, {})

    # Remove read-only sub-fields
    content.pop("is_toggleable", None)
    content.pop("color", None) if btype not in ("callout", "quote") else None

    cleaned = {
        "object": "block",
        "type": btype,
        btype: content,
    }
    return cleaned


def get_page_title(page_id):
    data = api("GET", f"/pages/{page_id}")
    if not data:
        return "(unknown)"
    props = data.get("properties", {})
    tp = props.get("title") or props.get("Name")
    return "".join(t.get("plain_text", "") for t in tp.get("title", [])) if tp else "(untitled)"


def get_page_icon(page_id):
    data = api("GET", f"/pages/{page_id}")
    if not data:
        return None
    return data.get("icon")


def create_page(parent_id, title, icon=None):
    payload = {
        "parent": {"page_id": parent_id},
        "properties": {"title": {"title": [{"text": {"content": title}}]}},
    }
    if icon:
        payload["icon"] = icon
    r = api("POST", "/pages", payload)
    return r["id"] if r else None


def add_blocks_chunked(page_id, blocks):
    """Add blocks in chunks of 95 (Notion limit)."""
    for i in range(0, len(blocks), 95):
        chunk = blocks[i:i+95]
        api("PATCH", f"/blocks/{page_id}/children", {"children": chunk})
        time.sleep(0.3)


def archive_page(page_id):
    api("PATCH", f"/pages/{page_id}", {"archived": True})


print("Moving Edge AI pages into Edge AI Infrastructure Documents folder")
print("=" * 65)

for src_id, title in PAGES_TO_MOVE:
    print(f"\n  Processing: {title}")

    # 1. Get source blocks
    blocks = get_all_blocks(src_id)
    print(f"    Fetched {len(blocks)} blocks")

    # 2. Get icon
    src_data = api("GET", f"/pages/{src_id}")
    icon = src_data.get("icon") if src_data else None

    # 3. Create new page in target folder
    new_id = create_page(EDGE_AI_FOLDER, title, icon=icon)
    if not new_id:
        print(f"    FAILED to create new page")
        continue
    print(f"    Created new page: {new_id}")

    # 4. Clean and copy blocks
    clean_blocks = []
    for b in blocks:
        c = clean_block(b)
        if c:
            clean_blocks.append(c)

    if clean_blocks:
        add_blocks_chunked(new_id, clean_blocks)
        print(f"    Copied {len(clean_blocks)} blocks")

    # 5. Archive original
    archive_page(src_id)
    print(f"    Archived original")

print("\n" + "=" * 65)
print("Done. Edge AI Infrastructure Documents now contains:")
print("  - Edge AI Infrastructure Upgrade — Master Prompt")
print("  - Edge AI Upgrade — Part 1: Executive Summary Rewrites")
print("  - Edge AI Upgrade — Part 2: Edge Infrastructure Positioning")
print("  - Edge AI Upgrade — Part 3: Bloom Energy Power Architecture")
print("  - Edge AI Upgrade — Part 4: Terminology Map, Site Strategy & Roadmap")
