"""
Populate Part 4: Terminology Map, Site Strategy & Roadmap
"""
import httpx, sys, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

KEY = "NOTION_API_TOKEN_REDACTED"
HEADERS = {
    "Authorization": f"Bearer {KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

PAGE_ID = "31d88f09-7e31-8108-9179-ce8c055d074f"


def p(text):
    return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def h2(text):
    return {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def h3(text):
    return {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def b(text):
    return {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def n(text):
    return {"object": "block", "type": "numbered_list_item", "numbered_list_item": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def q(text):
    return {"object": "block", "type": "quote", "quote": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def divider():
    return {"object": "block", "type": "divider", "divider": {}}


blocks = [
    q("Status: DRAFT — March 2026. Covers official project terminology, site layout strategy, and phased deployment roadmap."),

    h2("PART A — TERMINOLOGY MAP"),
    p("Official language for all ADC project documents, presentations, financing proposals, and investor materials. Use the right-column term in all new and revised documents. The left column is deprecated."),

    h3("Architecture & Product Language"),
    b("data center pods  ->  edge compute nodes"),
    b("container data center  ->  modular edge infrastructure"),
    b("GPU pod  ->  deployable AI compute module"),
    b("data center site  ->  edge infrastructure campus"),
    b("containerized data center  ->  modular edge compute node"),
    b("GPU cluster  ->  distributed AI compute array"),
    b("server rack  ->  compute payload (within the node context)"),
    b("data center build  ->  edge infrastructure deployment"),
    b("pod manufacturer  ->  edge infrastructure manufacturer"),

    h3("NVIDIA Hardware Language"),
    b("Blackwell / GB200 / GB300 / B200 / B100  ->  RETIRED — do not reference"),
    b("Grace CPU / Grace Hopper  ->  Vera CPU (88 Olympus Arm cores, Armv9.2)"),
    b("HBM3e  ->  HBM4 (288 GB per Rubin GPU, 20.7 TB per NVL72 rack, 1.58 PB/s aggregate)"),
    b("NVLink 5  ->  NVLink 6 (3.6 TB/s per GPU bidirectional, 260 TB/s aggregate per rack)"),
    b("Spectrum-X SN5000  ->  Spectrum-6 (SN6810 / SN6800)"),
    b("ConnectX-8 / BlueField-3  ->  ConnectX-9 SuperNIC / BlueField-4 DPU"),
    b("Feynman / Kyber  ->  UNCONFIRMED — do not reference until officially announced"),
    b("Current platform reference  ->  NVIDIA Vera Rubin NVL72 (H2 2026, confirmed CES 2026)"),

    h3("Performance & Compute Language"),
    b("10x lower token cost vs Blackwell  ->  REMOVE — not NVIDIA-sourced"),
    b("4x fewer GPUs  ->  REMOVE — not NVIDIA-sourced"),
    b("~120 kW TDP per rack  ->  TDP not published by NVIDIA — contact NVIDIA Enterprise Sales"),
    b("2.5x FP4 compute density vs GB200 NVL72  ->  USE THIS (3.6 vs 1.44 ExaFLOPS per rack, NVFP4)"),
    b("260 TB/s connecting 14-rack cluster  ->  260 TB/s aggregate per NVL72 rack (intra-rack only via NVLink 6)"),
    b("Scale-out networking  ->  InfiniBand NDR (cross-rack) — not NVLink 6"),

    h3("Financial & Business Language"),
    b("GPU rental business  ->  edge infrastructure hosting"),
    b("cloud GPU provider  ->  regional edge AI infrastructure operator"),
    b("data center investor  ->  edge infrastructure capital partner"),
    b("compute rental  ->  edge infrastructure services"),
    b("pod revenue  ->  edge compute hosting revenue"),

    divider(),
    h2("PART B — SITE STRATEGY: 1201 SE EVANGELINE THRUWAY"),
    p("Primary deployment site for MARLIE I — Lafayette AI Factory. Located in an established commercial/industrial corridor in Lafayette, Louisiana, with direct access to three-phase electrical service, LUS Fiber, natural gas, and municipal water and drainage."),

    h3("Site Overview"),
    b("Address: 1201 SE Evangeline Thruway, Lafayette, Louisiana"),
    b("Site area: Three adjacent parcels on Chag Street — approximately 0.60 acres Phase 1 footprint"),
    b("Existing asset: Borrower-owned commercial facility adjacent to site serves as operations base"),
    b("Current condition: Three blighted structures — removal included in Phase 1 scope"),
    b("Zoning: Commercial/industrial corridor — compatible with edge compute deployment"),
    b("Utility access: Three-phase electrical service, LUS Fiber, natural gas, municipal water and drainage"),

    h3("Phase 1 Site Layout"),
    b("Four 20-foot ISO edge compute nodes — deployed in 2x2 grid with maintenance clearance"),
    b("Shared utility plant — central CDU (coolant distribution unit), switchgear, and MDF"),
    b("Bloom Energy fuel cell zone — reserved pad adjacent to utility plant, natural gas service pre-run"),
    b("Diesel generator backup — N+1 standby units, auto-start on grid failure"),
    b("Fiber entry point — LUS Fiber primary, diverse second carrier conduit pre-installed"),
    b("Security perimeter — fenced and monitored yard, camera coverage, access control"),
    b("Operations base — existing adjacent building handles NOC, storage, and staff functions"),

    h3("Utility Infrastructure"),
    b("Power: Utility grid three-phase primary + Bloom Energy fuel cell supplemental + diesel emergency"),
    b("Cooling: Closed-loop liquid cooling plant — warm-water CDU serving all nodes, dry coolers on perimeter"),
    b("Connectivity: LUS Fiber primary (carrier-grade municipal network) + diverse carrier secondary"),
    b("Gas: Natural gas service for Bloom Energy fuel cells — Gulf Coast supply, existing infrastructure"),
    b("Water: Municipal water and drainage for cooling plant makeup water and fire suppression"),

    h3("Expansion Capacity"),
    b("Phase 1 IT capacity: 520 kW across four nodes"),
    b("Phase 1 infrastructure ceiling: Designed to 800 kW per node — 3.2 MW total site capacity"),
    b("Phase 2 expansion: Additional node rows on same parcels — no new land acquisition required"),
    b("Phase 3 multi-site: Replicate site model to additional Gulf Coast locations using same manufactured nodes"),
    b("Power expansion path: Additional Bloom Energy server units stack in modular increments (300 kW each)"),
    b("Cooling expansion path: Additional CDU modules add in-line with node deployment — no plant redesign"),

    divider(),
    h2("PART C — DEPLOYMENT ROADMAP"),
    p("Phased deployment schedule from site preparation through regional multi-site buildout. All timelines are based on 12-week node manufacturing lead time and standard commercial construction sequencing."),

    h3("Phase 1 — MARLIE I Lafayette (2026)"),
    n("Site prep and blight removal — Q1 2026"),
    n("Financing close and infrastructure procurement — Q1/Q2 2026"),
    n("Utility plant construction (CDU, switchgear, fiber, gas) — Q2 2026"),
    n("First two node deliveries and commissioning — Q2/Q3 2026"),
    n("NVIDIA Vera Rubin NVL72 compute payload installation — H2 2026 (per NVIDIA availability)"),
    n("Nodes 3 and 4 deployment — Q3 2026"),
    n("Bloom Energy Phase 1 fuel cell installation — Q3/Q4 2026"),
    n("Full Phase 1 operational: 520 kW IT capacity, 4 nodes — Q4 2026"),

    h3("Phase 2 — Capacity Expansion (2027)"),
    n("Add nodes 5-8 on existing site — no new land required"),
    n("Scale Bloom Energy fuel cell capacity to match expanded load"),
    n("Upgrade fiber to additional carrier for redundancy"),
    n("Target: 1.0 MW+ IT capacity on Lafayette site"),
    n("Begin site evaluation for second Gulf Coast location"),

    h3("Phase 3 — Gulf Coast Regional Deployment (2027-2028)"),
    n("Deploy edge compute campus at second Gulf Coast location (New Orleans corridor or Lake Charles)"),
    n("Leverage manufactured node inventory for rapid site-to-site replication"),
    n("Establish regional fiber backbone between edge campuses"),
    n("Target markets: energy sector clients, municipal contracts, enterprise AI hosting"),
    n("Scale to 5+ regional edge campuses across Louisiana and Gulf Coast"),

    h3("Manufacturing & Supply Chain Notes"),
    b("Node manufacturing lead time: 12 weeks factory-to-ship"),
    b("NVIDIA Vera Rubin NVL72 availability: H2 2026 (confirmed CES 2026 — full production)"),
    b("Bloom Energy server lead time: 6-12 months — order in parallel with site construction"),
    b("CDU and cooling plant: Standard commercial HVAC procurement — 8-12 weeks"),
    b("LUS Fiber service order: 60-90 day lead time for commercial service activation"),
    b("All Phase 1 components commercially available as of Q1 2026"),
]

print(f"Total blocks: {len(blocks)}")
for i in range(0, len(blocks), 95):
    chunk = blocks[i:i+95]
    r = httpx.patch(
        f"https://api.notion.com/v1/blocks/{PAGE_ID}/children",
        headers=HEADERS,
        json={"children": chunk},
        timeout=30
    )
    print(f"Batch {i//95 + 1}: {r.status_code} ({len(chunk)} blocks)")
    if r.status_code not in (200, 201):
        print(f"  Error: {r.text[:200]}")
    time.sleep(0.3)

print("Done.")
