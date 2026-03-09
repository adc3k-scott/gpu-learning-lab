"""
Move remaining loose pages into their correct folders via copy + archive.
"""
import httpx, sys, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

KEY = "NOTION_API_TOKEN_REDACTED"
HEADERS = {
    "Authorization": f"Bearer {KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

POD_SWARM_FOLDER = "31d88f09-7e31-814c-8a49-ffea016555e4"  # Pod Swarm Engineering Suite
SESSION_FOLDER   = "31d88f09-7e31-81bf-949f-d10e58ca4040"  # Session Prompts & Claude Context
WEBSITE_FOLDER   = "31d88f09-7e31-8189-9e98-d9d118cdda50"  # ADC-3K Website Build Logs

MOVES = [
    ("31688f09-7e31-81c8-81f0-dbad001f2e36", POD_SWARM_FOLDER, "Pod Swarm Architecture — Document Index"),
    ("31988f09-7e31-8178-9d94-fa66c4b39690", SESSION_FOLDER,   "March 4 2026 — Engineering Package Backup & Status"),
    ("31588f09-7e31-8154-995a-dbff852cd3df", SESSION_FOLDER,   "ADC 3K — Master Session Prompt"),
    ("31688f09-7e31-81a2-abd4-c5a75652d460", WEBSITE_FOLDER,   "ADC-3K POD — Website Build Log (V3)"),
]


def api(method, path, data=None):
    r = httpx.request(method, f"https://api.notion.com/v1{path}", headers=HEADERS, json=data, timeout=30)
    if r.status_code not in (200, 201):
        print(f"    API ERROR {r.status_code}: {r.text[:150]}")
        return None
    return r.json()


def get_all_blocks(page_id):
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


def get_child_pages(page_id):
    """Return child page blocks (sub-pages to recurse into)."""
    blocks = get_all_blocks(page_id)
    return [(b["id"], b["child_page"]["title"]) for b in blocks if b.get("type") == "child_page"]


def clean_block(block):
    btype = block.get("type")
    if not btype or btype == "child_page":
        return None
    content = dict(block.get(btype, {}))
    content.pop("is_toggleable", None)
    return {"object": "block", "type": btype, btype: content}


def create_page(parent_id, title, icon=None):
    payload = {
        "parent": {"page_id": parent_id},
        "properties": {"title": {"title": [{"text": {"content": title}}]}},
    }
    if icon:
        payload["icon"] = icon
    r = api("POST", "/pages", payload)
    return r["id"] if r else None


def copy_blocks(src_id, dst_id):
    blocks = get_all_blocks(src_id)
    clean = [c for b in blocks for c in [clean_block(b)] if c]
    for i in range(0, len(clean), 95):
        api("PATCH", f"/blocks/{dst_id}/children", {"children": clean[i:i+95]})
        time.sleep(0.2)
    return len(clean)


def copy_page_recursive(src_id, src_title, dst_parent_id, depth=0):
    indent = "  " * depth
    src_data = api("GET", f"/pages/{src_id}")
    icon = src_data.get("icon") if src_data else None

    new_id = create_page(dst_parent_id, src_title, icon=icon)
    if not new_id:
        print(f"{indent}  FAILED: could not create {src_title}")
        return

    count = copy_blocks(src_id, new_id)
    print(f"{indent}  Created '{src_title}' — {count} blocks copied")

    # Recurse into child pages
    child_pages = get_child_pages(src_id)
    for child_id, child_title in child_pages:
        copy_page_recursive(child_id, child_title, new_id, depth + 1)
        api("PATCH", f"/pages/{child_id}", {"archived": True})

    return new_id


def archive_page(page_id):
    api("PATCH", f"/pages/{page_id}", {"archived": True})


print("Moving remaining loose pages into group folders")
print("=" * 60)

folder_names = {
    POD_SWARM_FOLDER: "Pod Swarm Engineering Suite",
    SESSION_FOLDER:   "Session Prompts & Claude Context",
    WEBSITE_FOLDER:   "ADC-3K Website Build Logs",
}

for src_id, target_folder, title in MOVES:
    print(f"\n-> {title}")
    print(f"   Destination: {folder_names[target_folder]}")
    copy_page_recursive(src_id, title, target_folder)
    archive_page(src_id)
    print(f"   Original archived.")

print("\n" + "=" * 60)
print("Complete. Final ADC3K structure:")
print()
print("ADC 3K — Project Command Center")
print("  MARLIE I — Lafayette AI Factory  [8 sections]")
print("  Pod Swarm Engineering Suite")
print("    5 technical docs + Pod Swarm Architecture — Document Index")
print("  Edge AI Infrastructure Documents")
print("    Master Prompt + Parts 1-4")
print("  Session Prompts & Claude Context")
print("    March 4 2026 Engineering Package")
print("    ADC 3K — Master Session Prompt")
print("  ADC-3K Website Build Logs")
print("    ADC-3K POD — Website Build Log (V3)")
