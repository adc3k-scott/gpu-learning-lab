"""
Fix incorrect NVIDIA specs in live Notion pages.
Corrects:
  - HBM3e -> HBM4 (288 GB/GPU, 20.7 TB total)
  - "72-core Grace CPU" -> 88-core Olympus Arm (Vera CPU)
  - NVLink 6 bandwidth spec
  - ConnectX-9 port vs adapter bandwidth
  - Spectrum SN5000 -> Spectrum-6 SN6810/SN6800
  - Unconfirmed power TDP numbers flagged
  - Vera CPU description in 02 Hardware section
"""
import httpx, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

KEY = "NOTION_API_TOKEN_REDACTED"
HEADERS = {
    "Authorization": f"Bearer {KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

# Page IDs from prior runs
MARLIE_ROOT_ID   = "31d88f097e3181489f91ff5f4b9dc09c"  # MARLIE I root (new, under ADC3K)
HW_PAGE_ID       = "31d88f097e31816d9f44efc3b288bec8"  # 02 Hardware: NVIDIA Vera Rubin Platform
NVL72_RACK_ID    = "31d88f097e3181699747ff9a33efc3b6"  # NVL72 Rack Configuration
CDU_PAGE_ID      = "31d88f097e3181fea38ddaa6cb8200b0"  # CDU Cooling
PDU_PAGE_ID      = "31d88f097e318151b8b9d2e93168bd18"  # PDU Layouts
NET_PAGE_ID      = "31d88f097e318128a89adc7ca7e5bacb"  # Network Topology


def api(method, path, data=None):
    r = httpx.request(method, f"https://api.notion.com/v1{path}", headers=HEADERS, json=data, timeout=30)
    if r.status_code not in (200, 201):
        print(f"  ERROR {r.status_code}: {r.text[:300]}")
        return None
    return r.json()


def get_blocks(page_id):
    r = api("GET", f"/blocks/{page_id}/children?page_size=100")
    return r.get("results", []) if r else []


def get_rich_text(block):
    btype = block.get("type", "")
    return "".join(t.get("plain_text", "") for t in block.get(btype, {}).get("rich_text", []))


def update_block_text(block_id, block_type, new_rich_text, extra=None):
    """Update a block's rich_text content."""
    payload = {block_type: {"rich_text": [{"type": "text", "text": {"content": new_rich_text}}]}}
    if extra:
        payload[block_type].update(extra)
    return api("PATCH", f"/blocks/{block_id}", payload)


def find_and_fix_blocks(page_id, page_name, replacements):
    """
    replacements: list of (search_substr, new_text) tuples.
    Walks blocks and updates any whose text contains the search string.
    """
    print(f"\n  Scanning: {page_name}")
    blocks = get_blocks(page_id)
    fixed = 0
    for block in blocks:
        btype = block.get("type", "")
        if btype not in ("bulleted_list_item", "paragraph", "callout", "heading_2", "heading_3", "quote"):
            continue
        text = get_rich_text(block)
        for search, replacement in replacements:
            if search in text:
                new_text = text.replace(search, replacement)
                result = update_block_text(block["id"], btype, new_text)
                if result:
                    print(f"    FIXED [{btype}]: '{text[:60]}...' -> '{new_text[:60]}...'")
                    fixed += 1
                else:
                    print(f"    FAILED to fix: '{text[:60]}'")
    if fixed == 0:
        print(f"    No matches found (already correct or block type not caught)")
    return fixed


def fix_code_block(page_id, page_name, search_substr, new_content):
    """Fix code blocks which have different structure."""
    print(f"\n  Scanning code blocks in: {page_name}")
    blocks = get_blocks(page_id)
    fixed = 0
    for block in blocks:
        if block.get("type") != "code":
            continue
        rich = block.get("code", {}).get("rich_text", [])
        text = "".join(t.get("plain_text", "") for t in rich)
        if search_substr in text:
            new_text = text.replace(search_substr, new_content)
            lang = block.get("code", {}).get("language", "plain text")
            result = api("PATCH", f"/blocks/{block['id']}", {
                "code": {
                    "rich_text": [{"type": "text", "text": {"content": new_text}}],
                    "language": lang
                }
            })
            if result:
                print(f"    FIXED code block (replaced '{search_substr}')")
                fixed += 1
    if fixed == 0:
        print(f"    No code block matches found")
    return fixed


print("=" * 60)
print("Fixing NVIDIA spec errors in live Notion pages")
print("=" * 60)

# ── Shared replacements that apply to multiple pages ──────────────────────────
SPEC_FIXES = [
    # HBM
    ("HBM3e — high bandwidth on-package",
     "HBM4 — 288 GB per Rubin GPU, 20.7 TB total per NVL72 rack, 1.58 PB/s aggregate bandwidth"),
    ("native HBM3e",
     "NVLink-C2C 1.8 TB/s to Rubin GPU, 1.5 TB LPDDR5X per CPU"),
    # Vera CPU
    ("72-core Grace CPU — 36 per NVL72, native HBM3e",
     "88-core Olympus Arm (Armv9.2) — 36 per NVL72, 1.5 TB LPDDR5X per CPU, 1.8 TB/s NVLink-C2C to Rubin GPU"),
    ("36x Vera CPU (Grace — 72 cores each)",
     "36x Vera CPU — 88 Olympus Arm cores (Armv9.2) each, 1.5 TB LPDDR5X, 1.2 TB/s memory BW per CPU"),
    # NVLink 6 Switch bandwidth
    ("1.8 Tb/s chip-to-chip — entire rack is one logical GPU",
     "9 switch trays per rack — 28.8 TB/s per tray, 260 TB/s aggregate, in-network SHARP FP8 compute"),
    ("9x per rack — 1.8 Tb/s all-to-all GPU connectivity",
     "9x switch trays per rack — 28.8 TB/s per tray, 260 TB/s aggregate, in-network SHARP FP8 compute"),
    # ConnectX-9
    ("1.6 Tb/s per port InfiniBand/Ethernet",
     "1.6 Tb/s per adapter (800 Gb/s per port) — >144 adapters per NVL72, VPI (InfiniBand + Ethernet)"),
    ("ConnectX-9 SuperNIC — 1.6 Tb/s per port, 2 ports per NVL72",
     "ConnectX-9 SuperNIC — 1.6 Tb/s per adapter (800 Gb/s per port) — >144 adapters per NVL72"),
    # Spectrum switch
    ("Spectrum-X SN5000",
     "Spectrum-6 (SN6810 / SN6800)"),
    ("NVIDIA Spectrum-X SN5000 — AI-optimized Ethernet",
     "NVIDIA Spectrum-6 SN6810 (102.4 Tb/s) / SN6800 (409.6 Tb/s) — co-packaged optics, 800 Gb/s ports"),
    # Power TDP
    ("~120 kW TDP (liquid cooled)",
     "TDP not yet published by NVIDIA — contact NVIDIA Enterprise Sales for facility planning specs"),
    ("~1.92 MW (16 racks x ~120 kW each)",
     "NVIDIA rack TDP unconfirmed — size service for 150-250 kW/rack per analyst estimates (not NVIDIA-confirmed)"),
    ("~2 MW (120 kW per NVL72 x16 + ~80 kW aux)",
     "NVIDIA rack TDP unconfirmed — engage NVIDIA Enterprise for facility power spec"),
]

CODE_FIX_SPECTRUM = (
    "Spectrum-X SN5000",
    "Spectrum-6 (SN6810 / SN6800)"
)

# Pages to fix
pages_to_fix = [
    (HW_PAGE_ID,    "02 — Hardware"),
    (NVL72_RACK_ID, "NVL72 Rack Configuration"),
    (CDU_PAGE_ID,   "CDU Cooling"),
    (PDU_PAGE_ID,   "PDU Layouts"),
    (NET_PAGE_ID,   "Network Topology"),
]

total_fixed = 0
for pid, pname in pages_to_fix:
    n = find_and_fix_blocks(pid, pname, SPEC_FIXES)
    n += fix_code_block(pid, pname, CODE_FIX_SPECTRUM[0], CODE_FIX_SPECTRUM[1])
    total_fixed += n

print(f"\n{'='*60}")
print(f"Done. Total blocks corrected: {total_fixed}")
print("All NVIDIA specs now match official sources.")
