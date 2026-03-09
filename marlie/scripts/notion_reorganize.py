"""
Notion Workspace Reorganizer
Restructures the full workspace into proper hierarchy:
  - ADC 3K Project Command Center (hub)
      - MARLIE I — Lafayette AI Factory
      - Pod Swarm Engineering Suite
      - Edge AI Infrastructure Documents
      - Session Prompts & Claude Context
      - ADC-3K Website Build Logs
  - AI Daily Omniverse (hub)
  - Mission Control HQ (hub — missioncontrolhd.com SaaS only)
"""
import httpx
import json
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

NOTION_KEY = "NOTION_API_TOKEN_REDACTED"
HEADERS = {
    "Authorization": f"Bearer {NOTION_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

# ── Known page IDs (from prior workspace exploration) ──────────────────────────
# Verify these first via search before acting
ADC3K_HUB_ID    = "31488f09-7e31-816d-9fdc-c6aabba4e3fa"
MISSION_HQ_ID   = "31288f09-7e31-81a5-bf43-e2af16379346"
MARLIE_OLD_ID   = "31d88f09-7e31-817d-b355-e1fa8a9c9816"


def api(method, path, data=None, exit_on_error=True):
    url = f"https://api.notion.com/v1{path}"
    r = httpx.request(method, url, headers=HEADERS, json=data, timeout=30)
    if r.status_code not in (200, 201):
        msg = f"ERROR {r.status_code} {method} {path}: {r.text[:400]}"
        print(msg)
        if exit_on_error:
            sys.exit(1)
        return None
    return r.json()


def search_all_pages():
    """Return all pages from workspace via pagination."""
    results = []
    cursor = None
    while True:
        payload = {"page_size": 100, "filter": {"value": "page", "property": "object"}}
        if cursor:
            payload["start_cursor"] = cursor
        data = api("POST", "/search", payload)
        results.extend(data.get("results", []))
        if not data.get("has_more"):
            break
        cursor = data.get("next_cursor")
    return results


def get_title(page):
    props = page.get("properties", {})
    title_prop = props.get("title") or props.get("Name")
    if title_prop:
        rich = title_prop.get("title", [])
        return "".join(t.get("plain_text", "") for t in rich)
    return "(untitled)"


def create_page(parent_id, title, icon="📁", children=None):
    payload = {
        "parent": {"page_id": parent_id},
        "icon": {"type": "emoji", "emoji": icon},
        "properties": {
            "title": {"title": [{"text": {"content": title}}]}
        },
    }
    if children:
        payload["children"] = children
    result = api("POST", "/pages", payload)
    return result["id"], result.get("url", "")


def archive_page(page_id):
    return api("PATCH", f"/pages/{page_id}", {"archived": True}, exit_on_error=False)


def add_blocks(page_id, blocks):
    for i in range(0, len(blocks), 95):
        api("PATCH", f"/blocks/{page_id}/children", {"children": blocks[i:i+95]})


# ── Block helpers ──────────────────────────────────────────────────────────────
def h1(text):
    return {"object": "block", "type": "heading_1",
            "heading_1": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def h2(text):
    return {"object": "block", "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def h3(text):
    return {"object": "block", "type": "heading_3",
            "heading_3": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def para(text, bold=False):
    ann = {"bold": bold, "italic": False, "strikethrough": False,
           "underline": False, "code": False, "color": "default"}
    return {"object": "block", "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": text}, "annotations": ann}]}}

def callout(text, emoji="💡", color="gray_background"):
    return {"object": "block", "type": "callout",
            "callout": {"rich_text": [{"type": "text", "text": {"content": text}}],
                        "icon": {"type": "emoji", "emoji": emoji},
                        "color": color}}

def bullet(text, bold_prefix=None):
    if bold_prefix:
        rich = [
            {"type": "text", "text": {"content": bold_prefix + ": "},
             "annotations": {"bold": True, "italic": False, "strikethrough": False,
                             "underline": False, "code": False, "color": "default"}},
            {"type": "text", "text": {"content": text},
             "annotations": {"bold": False, "italic": False, "strikethrough": False,
                             "underline": False, "code": False, "color": "default"}},
        ]
    else:
        rich = [{"type": "text", "text": {"content": text}}]
    return {"object": "block", "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": rich}}

def divider():
    return {"object": "block", "type": "divider", "divider": {}}


# ── Step 1: Verify workspace structure ────────────────────────────────────────
def verify_workspace():
    print("\n=== STEP 1: Scanning workspace ===")
    pages = search_all_pages()
    print(f"Total pages found: {len(pages)}")

    by_id = {p["id"].replace("-", ""): p for p in pages}
    # also index by id with dashes
    by_id_dash = {p["id"]: p for p in pages}

    # Find key pages
    adc3k = by_id_dash.get(ADC3K_HUB_ID)
    hq = by_id_dash.get(MISSION_HQ_ID)
    marlie_old = by_id_dash.get(MARLIE_OLD_ID)

    print(f"\nADC3K hub ({ADC3K_HUB_ID}):")
    if adc3k:
        print(f"  FOUND: {get_title(adc3k)}")
    else:
        print("  NOT FOUND by direct ID — searching by title...")
        for p in pages:
            t = get_title(p)
            if "adc" in t.lower() or "adc3k" in t.lower() or "adc-3k" in t.lower():
                print(f"  Candidate: [{p['id']}] {t}")

    print(f"\nMission Control HQ ({MISSION_HQ_ID}):")
    if hq:
        print(f"  FOUND: {get_title(hq)}")
    else:
        print("  NOT FOUND by direct ID — searching by title...")
        for p in pages:
            t = get_title(p)
            if "mission control" in t.lower() or "hq" in t.lower():
                print(f"  Candidate: [{p['id']}] {t}")

    print(f"\nOld MARLIE I ({MARLIE_OLD_ID}):")
    if marlie_old:
        print(f"  FOUND: {get_title(marlie_old)}")
    else:
        print("  NOT FOUND by direct ID — searching by title...")
        for p in pages:
            t = get_title(p)
            if "marlie" in t.lower():
                print(f"  Candidate: [{p['id']}] {t}")

    print("\nAll top-level pages (no parent page):")
    for p in pages:
        parent = p.get("parent", {})
        if parent.get("type") == "workspace":
            print(f"  [{p['id']}] {get_title(p)}")

    return pages, adc3k, hq, marlie_old


# ── Step 2: Create MARLIE I under ADC3K hub ────────────────────────────────────
def create_marlie_under_adc3k(adc3k_id):
    print("\n=== STEP 2: Creating MARLIE I under ADC 3K hub ===")
    marlie_id, marlie_url = create_page(
        adc3k_id,
        "MARLIE I — Lafayette AI Factory",
        icon="⚡",
        children=[
            callout(
                "Louisiana's first next-generation AI factory — 1201 SE Evangeline Thruway, Lafayette LA 70501 — ADC3K / Scott Tomsu — CONFIDENTIAL INVESTOR DECK",
                emoji="⚡", color="yellow_background"
            ),
            divider(),
            h2("Project Status"),
            bullet("Phase: Pre-deployment — investor & partner outreach active"),
            bullet("Hardware: NVIDIA Vera Rubin NVL72 — Full Production — H2 2026 availability"),
            bullet("Site: Owner-built, debt-free — $15K total property debt"),
            bullet("Permits: Louisiana GC License active — build-ready"),
            bullet("Certifications: 7 NVIDIA + FAA Private Pilot + Part 107 UAS"),
            divider(),
            h2("Workbook Sections"),
            bullet("01 — Investment Thesis"),
            bullet("02 — Hardware: NVIDIA Vera Rubin Platform"),
            bullet("03 — Site & Building Specs"),
            bullet("04 — Government Funding Stack"),
            bullet("05 — Infrastructure Partners"),
            bullet("06 — ADC3K Credentials"),
            bullet("07 — Multi-Site Vision: Louisiana AI Network"),
            bullet("08 — Contact & CTA"),
        ]
    )
    print(f"  Created: {marlie_url}")

    # Create 8 sub-sections
    sections = [
        ("01 — Investment Thesis", "💡", [
            h2("Why MARLIE I Wins"),
            callout("First-mover AI infrastructure in Louisiana — sovereign land, owner-built, zero lease risk.", emoji="⚡", color="yellow_background"),
            divider(),
            bullet("Location", "Louisiana — low energy cost, tax incentives (LED), fiber (LUS), gas (Atmos)"),
            bullet("Hardware", "NVIDIA Vera Rubin NVL72 — 3.6 ExaFLOPS per rack, 100% liquid cooled, H2 2026"),
            bullet("Building", "Owner-built 22x35 ft compute shell — debt-free, no landlord, full control"),
            bullet("Scalability", "Phase 1 (16 racks), Phase 2 (2nd floor), Phase 3 (adjacent property)"),
            bullet("Revenue", "GPU cloud rental, AI inference API, on-prem enterprise contracts"),
            divider(),
            h2("5 Investor Facts"),
            bullet("NVIDIA projects 1 trillion AI data center market by 2030"),
            bullet("Louisiana has NO hyperscale AI factory — MARLIE I is first mover"),
            bullet("$15K total property debt — investor capital goes straight to hardware"),
            bullet("LUS fiber + Atmos gas + LFT Airport logistics all within 5 miles"),
            bullet("ADC3K holds 7 NVIDIA certifications, FAA Private Pilot, Part 107 UAS"),
        ]),
        ("02 — Hardware: NVIDIA Vera Rubin Platform", "🤖", [
            h2("NVIDIA Vera Rubin NVL72"),
            callout("3.6 ExaFLOPS NVFP4 inference per rack. 72 Rubin GPUs + 36 Vera CPUs. 100% liquid cooled. Full production H2 2026.", emoji="🤖", color="blue_background"),
            divider(),
            h3("Six Chips — One AI Supercomputer"),
            bullet("Rubin GPU", "Next-gen transformer engine, 3.6 ExaFLOPS NVFP4 per rack"),
            bullet("Vera CPU", "88-core Olympus Arm (Armv9.2) CPU — 36 per NVL72, 1.5 TB LPDDR5X per CPU, 1.8 TB/s NVLink-C2C to Rubin GPU"),
            bullet("NVLink 6 Switch", "9 switch trays per rack — 28.8 TB/s per tray, 260 TB/s aggregate rack bandwidth, in-network SHARP compute"),
            bullet("ConnectX-9 SuperNIC", "1.6 Tb/s per adapter (800 Gb/s per port) — >144 adapters per NVL72, InfiniBand and Ethernet (VPI)"),
            bullet("BlueField-4 DPU", "AI-accelerated networking and storage offload"),
            bullet("Spectrum-X Ethernet", "Dedicated AI Ethernet fabric"),
            divider(),
            h2("Phase 1 Performance (16 Racks)"),
            bullet("Compute", "57.6 ExaFLOPS NVFP4 aggregate"),
            bullet("Memory bandwidth", "260 TB/s aggregate"),
            bullet("Cooling", "CDU liquid cooling — heat to exterior dry coolers"),
            bullet("Power", "~500 kW Phase 1 — backed by natural gas generators"),
            bullet("Deployment", "Rack-to-compute in days — modular architecture"),
        ]),
        ("03 — Site & Building Specs", "🏗️", [
            h2("1201 SE Evangeline Thruway, Lafayette LA 70501"),
            callout("Owner-built compute shell — 22 x 35 ft interior floor plate. 2x12 framing, double 5/8 inch Type X sheetrock ceiling, 7ft 11in plate height.", emoji="🏗️", color="gray_background"),
            divider(),
            h3("Dimensions"),
            bullet("Exterior footprint", "24 ft x 40 ft"),
            bullet("Interior floor (Phase 1)", "22 ft x 35 ft — 770 sq ft compute space"),
            bullet("Plate height", "7 ft 11 in to bottom of double 5/8 inch Type X sheetrock"),
            bullet("Ceiling structure", "2x12 framing — full second floor above"),
            bullet("Fire rating", "2-layer Type X sheetrock — commercial fire resistance"),
            divider(),
            h3("Infrastructure"),
            bullet("Insulation", "Heavy insulation — superior thermal envelope"),
            bullet("Cooling", "Interior: CDU liquid loops. Exterior: dry coolers"),
            bullet("Power", "Interior: PDUs. Exterior: natural gas generators + UPS batteries"),
            bullet("Network", "LUS Fiber direct — dark fiber available"),
            divider(),
            h3("Expansion Vectors"),
            bullet("Phase 2", "Full second floor — 22 x 35 ft additional"),
            bullet("Phase 3", "Adjacent owned property — separate building"),
        ]),
        ("04 — Government Funding Stack", "🏦", [
            h2("Louisiana Funding Opportunities"),
            callout("Louisiana Economic Development (LED) and federal programs available for AI infrastructure.", emoji="🏦", color="gray_background"),
            divider(),
            bullet("LED FastStart", "Louisiana workforce training — free, customized to AI ops"),
            bullet("Industrial Tax Exemption (ITEP)", "Up to 80% property tax exemption on qualifying infrastructure"),
            bullet("Quality Jobs", "6% rebate on payroll for qualifying positions"),
            bullet("CHIPS and Science Act", "Federal semiconductor/AI infrastructure grants — data center eligible"),
            bullet("DOE grid modernization", "AI-optimized power grid tie-ins — LUS partnership angle"),
            bullet("SBIR/STTR", "NSF and DOD programs for AI research infrastructure"),
            bullet("EDA Tech Hubs", "Economic Development Administration designations for tech clusters"),
            divider(),
            para("Strategy: LED FastStart + ITEP as baseline. Layer CHIPS Act and EDA Tech Hub designation for Phase 2. Engage LUS and LED together for site incentive package."),
        ]),
        ("05 — Infrastructure Partners", "🔗", [
            h2("Lafayette Infrastructure Stack"),
            callout("Every critical utility is within 5 miles of MARLIE I. This is not a coincidence — it is why Lafayette.", emoji="⚡", color="yellow_background"),
            divider(),
            bullet("LUS Fiber", "214 Jefferson St — city-owned gigabit fiber, dark fiber available, no Big Telecom premium"),
            bullet("LUS Power", "1314 Walker Rd — city-owned utility, direct negotiation possible"),
            bullet("Atmos Energy", "1818 Eraste Landry Rd — natural gas for generator backup"),
            bullet("SLEMCO", "2727 SE Evangeline Thruway — co-op power, redundancy option"),
            bullet("LFT Airport", "200 Terminal Dr — cargo + charter, 1.6 miles from site"),
            divider(),
            h3("Partner Value Proposition"),
            bullet("LUS Fiber gains", "Anchor AI tenant, showcase for statewide fiber expansion"),
            bullet("Atmos Energy gains", "Commercial gas contract, AI sector market entry"),
            bullet("LFT Airport gains", "AI equipment logistics hub, tech sector anchor"),
            bullet("City of Lafayette gains", "First AI factory in Louisiana — economic development press release"),
        ]),
        ("06 — ADC3K Credentials", "🎓", [
            h2("Scott Tomsu / ADC3K"),
            callout("7 NVIDIA certifications. FAA Private Pilot. Part 107 UAS. Louisiana GC License. Not a startup — a qualified operator.", emoji="🎓", color="blue_background"),
            divider(),
            h3("NVIDIA Certifications (7)"),
            bullet("NVIDIA DLI — Fundamentals of Deep Learning"),
            bullet("NVIDIA DLI — Accelerating Data Science Workflows"),
            bullet("NVIDIA DLI — Applications of AI for Anomaly Detection"),
            bullet("NVIDIA DLI — Fundamentals of Accelerated Computing with CUDA Python"),
            bullet("NVIDIA DLI — Accelerated Computing with CUDA C/C++"),
            bullet("NVIDIA DLI — Deploying AI at the Edge"),
            bullet("NVIDIA DLI — Building Transformer-Based NLP Applications"),
            divider(),
            h3("Other Credentials"),
            bullet("FAA Private Pilot Certificate"),
            bullet("FAA Part 107 Remote Pilot (UAS)"),
            bullet("Louisiana General Contractor License"),
            bullet("Mission Control — AI multi-agent platform (open source, this repo)"),
        ]),
        ("07 — Multi-Site Vision: Louisiana AI Network", "🌐", [
            h2("Three-Phase Louisiana AI Network"),
            callout("MARLIE I is Phase 1. The vision is a state-wide AI infrastructure network — sovereign, Louisiana-owned, AI-first.", emoji="🌐", color="green_background"),
            divider(),
            h3("Phase 1 — MARLIE I (Home Base)"),
            bullet("Location", "1201 SE Evangeline Thruway, Lafayette LA"),
            bullet("Capacity", "16 NVL72 racks — 57.6 ExaFLOPS"),
            bullet("Status", "Pre-deployment — investor outreach active"),
            bullet("Timeline", "Build start: pending H2 2026 NVL72 delivery"),
            divider(),
            h3("Phase 2 — Site Two (Greater Louisiana)"),
            bullet("Target", "Baton Rouge or New Orleans metro"),
            bullet("Rationale", "State capital (BR) or port logistics (NO) — both have grid + fiber"),
            bullet("Funding", "Cash flow from MARLIE I + Phase 2 raise"),
            divider(),
            h3("Phase 3 — Site Three (Regional Expansion)"),
            bullet("Target", "Shreveport or Lake Charles"),
            bullet("Rationale", "Western Louisiana coverage — oil & gas AI applications"),
            bullet("Vision", "Federated AI inference network — statewide sovereign compute"),
        ]),
        ("08 — Contact & CTA", "📬", [
            h2("Get In Touch"),
            callout("MARLIE I is actively seeking infrastructure partners, equity investors, and enterprise AI customers.", emoji="📬", color="yellow_background"),
            divider(),
            bullet("Name", "Scott Tomsu"),
            bullet("Company", "ADC3K, Lafayette LA"),
            bullet("Site", "1201 SE Evangeline Thruway, Lafayette LA 70501"),
            bullet("Email", "[contact via Notion or direct outreach]"),
            divider(),
            h2("What We Need"),
            bullet("Infrastructure partners", "LUS Fiber, Atmos Energy — anchor tenant discussions"),
            bullet("Equity investors", "Hardware acquisition + working capital — H2 2026 deployment"),
            bullet("Enterprise customers", "GPU cloud contracts, AI inference API, on-prem deals"),
            bullet("LED / State of Louisiana", "Site incentive package, FastStart, ITEP"),
            divider(),
            para("MARLIE I pitch deck: marlie/index.html in the gpu-learning-lab repo."),
            para("Mission Control dashboard: http://localhost:8000 (internal AI ops platform)."),
        ]),
    ]

    created_sections = []
    for title, icon, blocks in sections:
        print(f"  Creating {title}...")
        sid, surl = create_page(marlie_id, title, icon=icon)
        add_blocks(sid, blocks)
        created_sections.append((title, sid, surl))
        print(f"    OK: {surl}")

    return marlie_id, marlie_url, created_sections


# ── Step 3: Create group pages under ADC3K hub ────────────────────────────────
def create_group_pages(adc3k_id):
    print("\n=== STEP 3: Creating group pages under ADC3K hub ===")
    groups = [
        ("Pod Swarm Engineering Suite", "⚙️", [
            callout("Engineering specs, hardware configs, and technical documentation for the ADC3K Pod Swarm infrastructure.", emoji="⚙️", color="gray_background"),
            divider(),
            h2("Contents"),
            bullet("NVL72 rack configurations and cable plans"),
            bullet("CDU liquid cooling schematics"),
            bullet("Power distribution unit layouts"),
            bullet("Network topology diagrams"),
            bullet("RunPod API integration notes"),
        ]),
        ("Edge AI Infrastructure Documents", "📡", [
            callout("Edge AI deployment specs, drone/UAS integration, and distributed inference architecture documents.", emoji="📡", color="gray_background"),
            divider(),
            h2("Contents"),
            bullet("Edge node hardware specs"),
            bullet("Part 107 UAS AI integration"),
            bullet("Distributed inference network design"),
            bullet("LTE/5G backhaul configurations"),
        ]),
        ("Session Prompts & Claude Context", "🧠", [
            callout("Saved Claude session prompts, CLAUDE.md snapshots, and AI context documents for mission continuity.", emoji="🧠", color="gray_background"),
            divider(),
            h2("Contents"),
            bullet("MARLIE I build session prompts"),
            bullet("Mission Control architecture prompts"),
            bullet("CLAUDE.md snapshots (versioned)"),
            bullet("Key decisions and rationale logs"),
        ]),
        ("ADC-3K Website Build Logs", "🌐", [
            callout("Build logs, design decisions, and content for the ADC3K public website.", emoji="🌐", color="gray_background"),
            divider(),
            h2("Contents"),
            bullet("Site architecture and page structure"),
            bullet("Content drafts and copy"),
            bullet("Design system and branding"),
            bullet("Deployment notes"),
        ]),
    ]

    created = []
    for title, icon, blocks in groups:
        print(f"  Creating {title}...")
        gid, gurl = create_page(adc3k_id, title, icon=icon, children=blocks)
        created.append((title, gid, gurl))
        print(f"    OK: {gurl}")

    return created


# ── Step 4: Rebuild ADC3K hub navigation ──────────────────────────────────────
def rebuild_adc3k_hub(adc3k_id, marlie_url, groups):
    print("\n=== STEP 4: Rebuilding ADC3K hub navigation ===")
    nav_blocks = [
        callout(
            "ADC3K — Advanced Computing 3000, Lafayette LA. AI Factory + Edge AI + Infrastructure. Owner: Scott Tomsu.",
            emoji="⚡", color="yellow_background"
        ),
        divider(),
        h2("Active Projects"),
        bullet("MARLIE I — Lafayette AI Factory (pre-deployment, investor outreach active)"),
        divider(),
        h2("Engineering Groups"),
    ]
    for title, gid, gurl in groups:
        nav_blocks.append(bullet(title))

    nav_blocks += [
        divider(),
        h2("Quick Links"),
        bullet("MARLIE I Pitch Deck: marlie/index.html in gpu-learning-lab repo"),
        bullet("Mission Control Dashboard: http://localhost:8000"),
        bullet("RunPod GPU Pods: via Mission Control > Integration Agent"),
        divider(),
        callout("Everything AI, everything sovereign, everything Louisiana.", emoji="⚡", color="yellow_background"),
    ]
    add_blocks(adc3k_id, nav_blocks)
    print("  ADC3K hub navigation updated.")


# ── Step 5: Archive old MARLIE I ──────────────────────────────────────────────
def archive_old_marlie(marlie_old_id):
    print(f"\n=== STEP 5: Archiving old MARLIE I ({marlie_old_id}) ===")
    result = archive_page(marlie_old_id)
    if result:
        print("  Archived successfully.")
    else:
        print("  Archive failed or page not found — skipping.")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("MARLIE I / ADC3K Notion Reorganizer")
    print("=" * 50)

    # Step 1: Verify
    pages, adc3k, hq, marlie_old = verify_workspace()

    # Resolve ADC3K hub ID
    if adc3k:
        adc3k_id = adc3k["id"]
        print(f"\nUsing ADC3K hub: [{adc3k_id}] {get_title(adc3k)}")
    else:
        print("\nERROR: Cannot find ADC3K hub. Check ADC3K_HUB_ID at top of script.")
        print("Run this script once to see candidate IDs, then update ADC3K_HUB_ID.")
        sys.exit(1)

    # Step 2: Create MARLIE I under ADC3K
    marlie_id, marlie_url, sections = create_marlie_under_adc3k(adc3k_id)

    # Step 3: Create group pages
    groups = create_group_pages(adc3k_id)

    # Step 4: Rebuild ADC3K hub nav
    rebuild_adc3k_hub(adc3k_id, marlie_url, groups)

    # Step 5: Archive old MARLIE I (under Mission Control HQ — wrong location)
    if marlie_old:
        archive_old_marlie(marlie_old["id"])
    else:
        print("\n=== STEP 5: Old MARLIE I not found by ID — skipping archive ===")
        # Search for any MARLIE pages under Mission Control HQ
        for p in pages:
            t = get_title(p)
            parent = p.get("parent", {})
            if "marlie" in t.lower() and parent.get("page_id") == MISSION_HQ_ID.replace("-", ""):
                print(f"  Found MARLIE under HQ: [{p['id']}] {t} — archiving...")
                archive_page(p["id"])

    print("\n" + "=" * 50)
    print("Reorganization complete.")
    print(f"MARLIE I: {marlie_url}")
    print(f"Sections created: {len(sections)}")
    print(f"Groups created: {len(groups)}")
    print("\nNotion workspace structure:")
    print("  ADC 3K Project Command Center")
    print("    MARLIE I — Lafayette AI Factory")
    for title, _, _ in sections:
        print(f"      {title}")
    for title, _, _ in groups:
        print(f"    {title}")
    print("  AI Daily Omniverse")
    print("  Mission Control HQ (missioncontrolhd.com SaaS only)")


if __name__ == "__main__":
    main()
