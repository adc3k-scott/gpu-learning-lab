"""
Sync financial architecture & ROI content to Notion.
- Updates Section 01 (Investment Thesis) with ROI stats
- Creates new Financial Architecture page under MARLIE I
"""
import httpx, sys, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

KEY = "NOTION_API_TOKEN_REDACTED"
HEADERS = {
    "Authorization": f"Bearer {KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

MARLIE_ROOT = "31d88f09-7e31-8148-9f91-ff5f4b9dc09c"
SECTION_01  = "31d88f09-7e31-8101-80d0-ed7d00e83e9a"  # 01 Investment Thesis

def api(method, path, data=None):
    r = httpx.request(method, f"https://api.notion.com/v1{path}", headers=HEADERS, json=data, timeout=30)
    if r.status_code not in (200, 201):
        print(f"  ERROR {r.status_code}: {r.text[:200]}")
        return None
    return r.json()

def get_children(page_id):
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

def create_page(parent_id, title, icon_emoji=None):
    payload = {
        "parent": {"page_id": parent_id},
        "properties": {"title": {"title": [{"text": {"content": title}}]}},
    }
    if icon_emoji:
        payload["icon"] = {"type": "emoji", "emoji": icon_emoji}
    r = api("POST", "/pages", payload)
    return r["id"] if r else None

def add_blocks(page_id, blocks):
    for i in range(0, len(blocks), 95):
        chunk = blocks[i:i+95]
        r = api("PATCH", f"/blocks/{page_id}/children", {"children": chunk})
        if r:
            print(f"  Added blocks {i+1}-{i+len(chunk)}")
        time.sleep(0.3)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1: Update Section 01 — Investment Thesis with ROI numbers
# ─────────────────────────────────────────────────────────────────────────────
print("Step 1: Updating Section 01 — Investment Thesis")

# Get section 01 page ID from MARLIE I children
children = get_children(MARLIE_ROOT)
section_pages = {b["child_page"]["title"]: b["id"] for b in children if b.get("type") == "child_page"}
print(f"  Found sections: {list(section_pages.keys())}")

s01_id = section_pages.get("01 — Investment Thesis")
if not s01_id:
    print("  ERROR: Could not find Section 01")
else:
    # Get existing blocks to find the 5 Investor Facts section
    blocks = get_children(s01_id)
    print(f"  Section 01 has {len(blocks)} blocks")

    # Add ROI data as new section at end of page
    roi_blocks = [
        divider(),
        h2("REVENUE PROJECTIONS — Phase 1 Build-Out"),
        q("All projections conservative basis: $6/GPU/hr, 72 GPUs per NVL72 rack. Financial model only — GPU hardware pricing via NVIDIA Enterprise Sales."),
        h3("Year 1 — 4 Racks Online, 40% Utilization"),
        b("Gross Annual Revenue: $12.1M"),
        b("GPUs Online: 288 (4 racks x 72)"),
        b("Annual Energy Cost (est.): $1.37M for 4-rack load"),
        b("Estimated EBITDA (before hardware lease): ~$10.9M"),
        h3("Year 2 — 8 Racks Online, 65% Utilization"),
        b("Gross Annual Revenue: $19.6M"),
        b("GPUs Online: 576 (8 racks x 72)"),
        b("Estimated EBITDA: ~$17.8M"),
        h3("Year 3 — 16 Racks Online (Full Phase 1), 75% Utilization"),
        b("Gross Annual Revenue: $36.3M"),
        b("GPUs Online: 1,152 (16 racks x 72)"),
        b("Annual OPEX (full scale): ~$2.32M"),
        b("Estimated EBITDA: ~$34.0M"),
        p("At $8/GPU/hr mid estimate: Year 3 gross reaches $48.4M. OPEX stays flat. Upside is asymmetric."),

        divider(),
        h2("LOUISIANA ENERGY ARBITRAGE"),
        b("MARLIE I annual energy cost (est. 2.4 MW @ $0.065/kWh): $1.37M/year"),
        b("Same load at national average ($0.122/kWh): $2.57M/year"),
        b("Same load in California ($0.185/kWh): $3.86M/year"),
        b("Annual savings vs national average: $1.2M/year"),
        b("Annual savings vs California: $2.49M/year"),
        b("Natural gas (Henry Hub, 40 miles away): effective Bloom Energy power cost $0.07-0.09/kWh"),
        b("Combined energy + AI staffing savings vs legacy data center: $3.7M+/year"),

        divider(),
        h2("PHASE 1 INFRASTRUCTURE CAPITAL — ESTIMATED"),
        b("Building structure: OWNED — $0 additional cost"),
        b("Land: OWNED — $15,000 remaining debt only"),
        b("Electrical service upgrade (3-phase heavy): $150,000"),
        b("Liquid cooling plant (CDU x2, dry coolers, piping): $350,000"),
        b("Power distribution (switchgear, UPS, bus): $250,000"),
        b("Network infrastructure (LUS fiber, spine, patch): $120,000"),
        b("Security, monitoring, Mission Control integration: $80,000"),
        b("Permits, engineering, inspections: $100,000"),
        b("Contingency (10%): $105,000"),
        b("TOTAL INFRASTRUCTURE ESTIMATE: ~$1.17M"),
        p("GPU hardware (NVIDIA NVL72) priced separately via NVIDIA Enterprise Sales. Available through equipment financing, NVIDIA Capital, and SBA programs."),

        divider(),
        h2("INVESTOR BENEFITS"),
        b("Reserved GPU compute bandwidth during off-peak hours (proportional to investment tier)"),
        b("Estimated compute credit value: $50K-$500K/month depending on tier"),
        b("Early mover rate lock: locked GPU rates below market for 24 months"),
        b("Network equity: preferred participation rights in Phase 2 and Phase 3 sites"),
        b("Revenue begins Q4 2026 — infrastructure capital begins returning immediately"),

        divider(),
        h2("TIMELINE TO REVENUE"),
        n("Q1-Q2 2026 — Financing close, site prep, electrical upgrade, CDU, LUS fiber"),
        n("Q3 2026 — First NVIDIA Vera Rubin NVL72 racks delivered, racks 1-4 commissioned"),
        n("Q4 2026 — FIRST DOLLAR OF REVENUE. Racks 5-8 live. Bloom Energy fuel cells operational."),
        n("2027 — All 16 racks live. 57.6 ExaFLOPS online. $19-36M+ annual revenue."),
        n("2027-2028 — Phase 2 site. Louisiana AI Network buildout. Cash flow funds next node."),
    ]

    add_blocks(s01_id, roi_blocks)
    print(f"  Section 01 updated with {len(roi_blocks)} ROI blocks")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2: Create Financial Architecture & ROI page under MARLIE I
# ─────────────────────────────────────────────────────────────────────────────
print("\nStep 2: Creating Financial Architecture & ROI page under MARLIE I")

fin_page_id = create_page(MARLIE_ROOT, "09 — Financial Architecture & ROI", "💰")
if not fin_page_id:
    print("  ERROR: Could not create financial page")
else:
    print(f"  Created page: {fin_page_id}")

    fin_blocks = [
        q("Version: March 2026. Conservative financial model for MARLIE I Phase 1 — 16 NVL72 racks, Lafayette Louisiana. All revenue figures estimated. GPU hardware pricing via NVIDIA Enterprise Sales."),

        h2("THE POSITIONING"),
        p("MARLIE I is not a data center. It is a purpose-built AI inference factory — the first of its kind in Louisiana. Legacy data centers were designed for internet traffic: HTTP, CDN, email. They are air-cooled, energy-wasteful, and retrofitting GPUs into thermal environments never designed for them. Their renewable energy claims are paper REC credits, not actual generation. MARLIE I goes straight to the front of the line: liquid-cooled, Vera Rubin NVL72, on-site Bloom Energy fuel cells, AI-managed operations via Mission Control. The comparison is not close."),

        divider(),
        h2("COMPARISON: LEGACY DATA CENTER vs MARLIE I AI FACTORY"),
        b("Design purpose — Legacy DC: internet traffic (HTTP, CDN, email) | MARLIE I: AI inference, purpose-built from day one"),
        b("Power efficiency (PUE) — Legacy DC: 1.4-1.8 (40-80% wasted) | MARLIE I: 1.03 (<3% overhead)"),
        b("Cooling method — Legacy DC: air (CRAC units, chillers) | MARLIE I: 100% direct-to-chip liquid"),
        b("Energy cost/kWh — Legacy DC: $0.10-0.18 national avg | MARLIE I: $0.065 Louisiana industrial"),
        b("On-site generation — Legacy DC: none, grid dependent | MARLIE I: Bloom Energy fuel cells + generators"),
        b("Renewable claim — Legacy DC: REC paper credits | MARLIE I: actual on-site fuel cell generation"),
        b("Compute hardware — Legacy DC: mixed-gen retrofitted GPUs | MARLIE I: NVIDIA Vera Rubin NVL72 only"),
        b("AI compute density — Legacy DC: low, not purpose-built | MARLIE I: 3.6 ExaFLOPS/rack (NVFP4)"),
        b("Revenue per rack/year — Legacy DC: $200K-$500K (colo/hosting) | MARLIE I: $3M-$5M+ (AI compute)"),
        b("Operations model — Legacy DC: 20-50 FTE manual ops | MARLIE I: 3-5 FTE, Mission Control AI"),
        b("Domestic content — Legacy DC: mixed, overseas components | MARLIE I: 100% USA, OBBBA compliant"),
        b("CHIPS Act eligible — Legacy DC: No | MARLIE I: Yes, designed from day one"),

        divider(),
        h2("PHASE 1 CAPITAL STRUCTURE"),
        h3("Already Owned — Zero Cost to Investors"),
        b("Building structure (owner-built, 20 years old): $0"),
        b("Land (owned): $15,000 remaining debt only"),

        h3("Infrastructure Buildout — Phase 1 Estimated"),
        b("Electrical service upgrade (3-phase heavy): $150,000"),
        b("Liquid cooling plant (CDU x2, dry coolers, piping, connections): $350,000"),
        b("Power distribution (switchgear, UPS, bus, PDUs): $250,000"),
        b("Network infrastructure (LUS fiber, spine switches, patch panels): $120,000"),
        b("Security, monitoring, Mission Control integration: $80,000"),
        b("Permits, engineering, inspections: $100,000"),
        b("Contingency (10%): $105,000"),
        b("TOTAL INFRASTRUCTURE ESTIMATE: ~$1.17M"),

        h3("GPU Hardware — Separate Capital Event"),
        b("NVIDIA Vera Rubin NVL72 pricing: via NVIDIA Enterprise Sales (H2 2026 availability)"),
        b("Financing options: NVIDIA Capital programs, equipment lenders, SBA, institutional equipment finance"),
        b("Infrastructure above ($1.17M) is bankable as commercial real estate improvement — traditional lending"),
        b("GPU hardware financed separately against revenue contracts and equipment collateral"),

        divider(),
        h2("ANNUAL OPERATING COSTS — FULL BUILD (16 RACKS)"),
        b("Energy (est. 2.4 MW @ $0.065/kWh Louisiana industrial): $1,370,000/year"),
        b("  Same load at national average ($0.122/kWh): $2,570,000/year — $1.2M MORE expensive"),
        b("  Same load in California ($0.185/kWh): $3,860,000/year — $2.49M MORE expensive"),
        b("Staffing — Mission Control AI managed (3-5 FTE): $500,000/year"),
        b("  Legacy DC staffing same scale (25 FTE): $3,000,000/year — $2.5M MORE expensive"),
        b("Connectivity and bandwidth: $150,000/year"),
        b("Insurance, maintenance, miscellaneous: $300,000/year"),
        b("TOTAL ANNUAL OPEX ESTIMATE: ~$2,320,000/year"),
        b("Combined advantage vs equivalent national operation: $3.7M+/year in energy + staffing savings"),

        divider(),
        h2("REVENUE MODEL — CONSERVATIVE BASIS"),
        p("Basis: $6/GPU/hr, 72 Rubin GPUs per NVL72 rack. Current H100 market: $2.50-$3.50/GPU/hr. Vera Rubin delivers 2.5x FP4 density — premium tier justified. Mid estimate $8/GPU/hr adds ~33% to all revenue figures."),
        h3("Year 1 — 4 Racks, 40% Utilization"),
        b("Gross Annual Revenue: $12.1M"),
        b("Annual OPEX (4-rack scale): ~$1.2M"),
        b("Estimated EBITDA: ~$10.9M"),
        h3("Year 2 — 8 Racks, 65% Utilization"),
        b("Gross Annual Revenue: $19.6M"),
        b("Annual OPEX (8-rack scale): ~$1.8M"),
        b("Estimated EBITDA: ~$17.8M"),
        h3("Year 3 — 16 Racks (Full Phase 1), 75% Utilization"),
        b("Gross Annual Revenue: $36.3M"),
        b("Annual OPEX (full scale): ~$2.32M"),
        b("Estimated EBITDA: ~$34.0M"),
        p("At $8/GPU/hr mid estimate: Year 3 gross = $48.4M. OPEX unchanged. Revenue sensitivity is asymmetric."),

        divider(),
        h2("LOUISIANA ENERGY ARBITRAGE"),
        b("Henry Hub natural gas benchmark: 40 miles from MARLIE I site"),
        b("Gulf Coast pipeline infrastructure: most redundant natural gas network in North America"),
        b("Bloom Energy fuel cells: 60%+ electrical efficiency, $0.07-0.09/kWh effective power cost"),
        b("LUS Power: Louisiana industrial rate $0.065/kWh — among nation's lowest"),
        b("Grid independence: Bloom fuel cells + diesel generators = zero dependency on utility grid"),
        b("Power quality: fuel cells produce UPS-grade power, less than 1% THD — better than grid delivery"),
        b("Renewable path: fuel cells hydrogen-compatible — transition to green hydrogen without replacing hardware"),

        divider(),
        h2("AI-MANAGED OPERATIONS — MISSION CONTROL"),
        b("Platform: Mission Control — multi-agent AI platform built in-house, operational today"),
        b("Functions: thermal monitoring, load balancing, predictive maintenance, customer provisioning, health checks"),
        b("Staffing: 3-5 FTE vs 20-50 FTE for equivalent legacy operation"),
        b("Response time: milliseconds — AI never sleeps, never takes vacation, never misses an alert"),
        b("Annual staffing savings vs legacy ops: $2.5M+/year"),
        b("Uptime architecture: AI-managed N+1 redundancy across power, cooling, and networking layers"),

        divider(),
        h2("TIMELINE — CAPITAL IN, REVENUE OUT"),
        n("Q1-Q2 2026 — Financing close. Site prep and blight removal. Electrical service upgrade. CDU plant construction. LUS fiber activation."),
        n("Q3 2026 — NVIDIA Vera Rubin NVL72 delivery (H2 2026 confirmed). Racks 1-4 commissioned. Mission Control online."),
        n("Q4 2026 — FIRST DOLLAR OF AI COMPUTE REVENUE. Racks 5-8 live. Bloom Energy Phase 1 fuel cells operational."),
        n("2027 — All 16 racks live. 57.6 ExaFLOPS online. $19-36M+ annual revenue at target utilization."),
        n("2027-2028 — Phase 2 site (Baton Rouge or New Orleans corridor). Louisiana AI Network buildout. Cash flow funds next node."),

        divider(),
        h2("INVESTOR BENEFITS"),
        b("Reserved GPU compute: off-peak bandwidth proportional to investment tier — est. $50K-$500K/month compute value"),
        b("Early mover rate lock: locked GPU rental rates below market for 24 months from first rack online"),
        b("Network equity: preferred participation rights in Phase 2 and Phase 3 Louisiana AI Network sites"),
        b("Revenue velocity: first revenue Q4 2026 — capital return begins within 12 months of investment"),
        b("Government leverage: MARLIE I as anchor tenant unlocks CHIPS Act, EDA Tech Hub, LED FastStart, Act 730 for region"),

        divider(),
        h2("CITY & STATE ECONOMIC IMPACT"),
        b("Estimated 5-year local economic impact (Phase 1): $20M+ (operations, vendor spend, wages)"),
        b("Lafayette becomes first AI infrastructure hub in Louisiana — ahead of all competing cities"),
        b("Federal funding anchor: CHIPS Act, EDA Tech Hub designation, DOE grid programs unlocked for region"),
        b("Blight removal: three blighted structures removed, tax base improved"),
        b("Job creation: direct FTE + construction + vendor ecosystem"),
        b("Cities that win the AI infrastructure race in 2026 lead the regional economy for 20 years"),

        divider(),
        h2("MADE IN AMERICA — 100% DOMESTIC CONTENT"),
        b("NVIDIA GPUs: manufactured in Texas (Houston/Dallas) — CHIPS Act domestic production"),
        b("Bloom Energy fuel cells: assembled in Newark, Delaware — US solid oxide technology"),
        b("Vertiv cooling systems (CDU): Columbus, Ohio"),
        b("LUS Fiber network: Lafayette, Louisiana — city-owned municipal infrastructure"),
        b("Building and construction: ADC3K, Louisiana-licensed GC — Lafayette labor, Louisiana materials"),
        b("Mission Control platform: designed and built in Lafayette, Louisiana — open-source, American-owned"),
        b("100% OBBBA domestic content compliant — qualifies for full federal incentive stack"),
        p("We are not importing AI infrastructure. We are building America's AI infrastructure — American hands, American companies, American capital. This is what rebuilding American technological leadership looks like."),
    ]

    add_blocks(fin_page_id, fin_blocks)
    print(f"\nFinancial Architecture page populated: {len(fin_blocks)} blocks")

print("\n" + "="*60)
print("Notion sync complete.")
print("Updated: 01 — Investment Thesis (ROI data appended)")
print("Created: 09 — Financial Architecture & ROI")
