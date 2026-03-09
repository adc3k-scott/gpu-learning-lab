"""
Move loose Notion pages into their correct group folders.
Uses PATCH /pages/{id} to reparent without recreating.
"""
import httpx, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

KEY = "NOTION_API_TOKEN_REDACTED"
HEADERS = {
    "Authorization": f"Bearer {KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

# ── Target folders ─────────────────────────────────────────────────────────────
EDGE_AI_FOLDER    = "31d88f09-7e31-8136-a572-e7e1b0008ad2"  # Edge AI Infrastructure Documents
POD_SWARM_FOLDER  = "31d88f09-7e31-814c-8a49-ffea016555e4"  # Pod Swarm Engineering Suite
SESSION_FOLDER    = "31d88f09-7e31-81bf-949f-d10e58ca4040"  # Session Prompts & Claude Context
WEBSITE_FOLDER    = "31d88f09-7e31-8189-9e98-d9d118cdda50"  # ADC-3K Website Build Logs

# ── Pages to move: (page_id, target_folder, title) ───────────────────────────
MOVES = [
    # Edge AI group
    ("31588f09-7e31-81b9-88bb-fcd241ce1282", EDGE_AI_FOLDER,   "Edge AI Upgrade — Part 1: Executive Summary Rewrites"),
    ("31588f09-7e31-81bb-9a03-e062421de5f6", EDGE_AI_FOLDER,   "Edge AI Upgrade — Part 2: Edge Infrastructure Positioning"),
    ("31588f09-7e31-81ca-a956-c735ccd1a3a3", EDGE_AI_FOLDER,   "Edge AI Upgrade — Part 3: Bloom Energy Power Architecture"),
    ("31588f09-7e31-81e7-b5eb-f9a81fc000fc", EDGE_AI_FOLDER,   "Edge AI Upgrade — Part 4: Terminology Map, Site Strategy & Roadmap"),
    ("31588f09-7e31-815a-a20f-daaf4ac86ace", EDGE_AI_FOLDER,   "Edge AI Infrastructure Upgrade — Master Prompt"),

    # Pod Swarm group
    ("31688f09-7e31-81c8-81f0-dbad001f2e36", POD_SWARM_FOLDER, "Pod Swarm Architecture — Document Index"),

    # Session Prompts group
    ("31988f09-7e31-8178-9d94-fa66c4b39690", SESSION_FOLDER,   "March 4 2026 — Engineering Package Backup & Status"),
    ("31588f09-7e31-8154-995a-dbff852cd3df", SESSION_FOLDER,   "ADC 3K — Master Session Prompt"),

    # Website group
    ("31688f09-7e31-81a2-abd4-c5a75652d460", WEBSITE_FOLDER,   "ADC-3K POD — Website Build Log (V3)"),
]


def move_page(page_id, new_parent_id, title):
    r = httpx.patch(
        f"https://api.notion.com/v1/pages/{page_id}",
        headers=HEADERS,
        json={"parent": {"page_id": new_parent_id}},
        timeout=30,
    )
    if r.status_code in (200, 201):
        print(f"  MOVED: {title}")
    else:
        print(f"  FAILED [{r.status_code}]: {title} — {r.text[:200]}")


print("Filing loose Notion pages into group folders...")
print("=" * 60)

print("\nEdge AI Infrastructure Documents:")
for pid, folder, title in MOVES:
    if folder == EDGE_AI_FOLDER:
        move_page(pid, folder, title)

print("\nPod Swarm Engineering Suite:")
for pid, folder, title in MOVES:
    if folder == POD_SWARM_FOLDER:
        move_page(pid, folder, title)

print("\nSession Prompts & Claude Context:")
for pid, folder, title in MOVES:
    if folder == SESSION_FOLDER:
        move_page(pid, folder, title)

print("\nADC-3K Website Build Logs:")
for pid, folder, title in MOVES:
    if folder == WEBSITE_FOLDER:
        move_page(pid, folder, title)

print("\n" + "=" * 60)
print("Done. Final structure:")
print()
print("ADC 3K — Project Command Center")
print("  MARLIE I — Lafayette AI Factory")
print("    01-08 sections")
print("  Pod Swarm Engineering Suite")
print("    NVL72 Rack Configuration & Cable Plans")
print("    CDU Liquid Cooling Schematics")
print("    Power Distribution Unit Layouts")
print("    Network Topology Diagrams")
print("    RunPod API Integration Notes")
print("    Pod Swarm Architecture — Document Index")
print("  Edge AI Infrastructure Documents")
print("    Edge AI Upgrade — Parts 1-4")
print("    Edge AI Infrastructure Upgrade — Master Prompt")
print("  Session Prompts & Claude Context")
print("    March 4 2026 — Engineering Package Backup")
print("    ADC 3K — Master Session Prompt")
print("  ADC-3K Website Build Logs")
print("    ADC-3K POD — Website Build Log (V3)")
