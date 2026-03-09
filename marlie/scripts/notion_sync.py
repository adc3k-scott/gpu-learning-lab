"""
MARLIE I — Notion Workbook Builder
Creates the full MARLIE I workbook under Mission Control HQ
"""
import httpx
import json
import sys

NOTION_KEY = "NOTION_API_TOKEN_REDACTED"
HQ_PAGE_ID = "31288f09-7e31-81a5-bf43-e2af16379346"

HEADERS = {
    "Authorization": f"Bearer {NOTION_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

def api(method, path, data=None):
    url = f"https://api.notion.com/v1{path}"
    r = httpx.request(method, url, headers=HEADERS, json=data, timeout=30)
    if r.status_code not in (200, 201):
        print(f"ERROR {r.status_code}: {r.text[:400]}")
        sys.exit(1)
    return r.json()

def create_page(parent_id, title, children=None, icon="⚡"):
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
    return result["id"], result["url"]

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

def quote(text):
    return {"object": "block", "type": "quote",
            "quote": {"rich_text": [{"type": "text", "text": {"content": text},
                                     "annotations": {"italic": True, "bold": False,
                                                     "strikethrough": False, "underline": False,
                                                     "code": False, "color": "default"}}]}}

def add_blocks(page_id, blocks):
    # Notion limits 100 blocks per request
    for i in range(0, len(blocks), 95):
        chunk = blocks[i:i+95]
        api("PATCH", f"/blocks/{page_id}/children", {"children": chunk})

def build_workbook():
    print("Creating MARLIE I root page...")
    root_id, root_url = create_page(
        HQ_PAGE_ID,
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
    print(f"  Root: {root_url}")

    # ── 01 INVESTMENT THESIS ──────────────────────────────────────────
    print("Creating 01 — Investment Thesis...")
    t_id, t_url = create_page(root_id, "01 — Investment Thesis", icon="💡")
    add_blocks(t_id, [
        callout("The market is building for Blackwell. Marlie I is built for Rubin. That gap is the investment.", emoji="💡", color="yellow_background"),
        divider(),
        h2("Thesis 01 — Skip Blackwell. Deploy Rubin."),
        para("The market is building data centers around Blackwell — last generation's answer. Marlie I is designed from the ground up for NVIDIA Vera Rubin, shipping H2 2026."),
        bullet("10x lower token cost vs Blackwell"),
        bullet("4x fewer GPUs for equivalent training runs"),
        bullet("22 TB/s memory bandwidth per GPU (HBM4)"),
        bullet("3.6 ExaFLOPS NVFP4 inference per NVL72 rack"),
        bullet("Investors who move now own the next generation — not a commodity rack of yesterday's hardware"),
        divider(),
        h2("Thesis 02 — Infrastructure Already Exists"),
        para("1201 SE Evangeline Thruway is not a greenfield project. ADC3K owns the building. The property carries only $15K in total debt."),
        bullet("LUS Fiber: ~0.8 miles"),
        bullet("LUS Power Substation: ~1 mile"),
        bullet("Atmos Energy (natural gas): ~3 miles"),
        bullet("Henry Hub gas benchmark: ~40 miles — world's most liquid gas price"),
        bullet("Lafayette Regional Airport (LFT): adjacent — Part 107 UAS"),
        bullet("NVIDIA TX Manufacturing (Foxconn Houston / Wistron Fort Worth): ~4 hours"),
        divider(),
        h2("Thesis 03 — Money Is Already Flowing"),
        bullet("One Big Beautiful Bill Act (OBBBA): $500B toward domestic AI infrastructure"),
        bullet("Louisiana Act 730: 20-year state/local sales & use tax rebate on qualifying AI factory equipment"),
        bullet("BEAD Broadband Program: federal funding for infrastructure expansion"),
        bullet("Gulf OCS Revenue: $650M/year to Louisiana through 2034"),
        bullet("Stargate public-private AI program: FEOC-clean projects like Marlie I qualify"),
        divider(),
        h2("Key Stats"),
        bullet("10x — Lower token cost vs Blackwell"),
        bullet("6 months — Estimated deploy timeline"),
        bullet("$15K — Total property debt"),
        bullet("20 years — Louisiana tax exemption on equipment"),
        bullet("#1 — Louisiana industrial power rates in USA"),
    ])
    print(f"  {t_url}")

    # ── 02 HARDWARE ───────────────────────────────────────────────────
    print("Creating 02 — Hardware: NVIDIA Vera Rubin...")
    h_id, h_url = create_page(root_id, "02 — Hardware: NVIDIA Vera Rubin Platform", icon="🤖")
    add_blocks(h_id, [
        callout("Jensen Huang: \"Rubin arrives at exactly the right moment... Rubin takes a giant leap toward the next frontier of AI.\"", emoji="🤖", color="blue_background"),
        callout("Sam Altman: \"Intelligence scales with compute... The NVIDIA Rubin platform helps us keep scaling this progress.\"", emoji="💬", color="gray_background"),
        divider(),
        h2("NVL72 Rack System"),
        bullet("72 Rubin GPUs per rack"),
        bullet("36 Vera CPUs per rack"),
        bullet("3.6 ExaFLOPS NVFP4 inference per rack"),
        bullet("100% liquid cooled — zero air cooling"),
        bullet("NVLink 6 switch fabric — 3.6 TB/s GPU-to-GPU"),
        bullet("Ships fully integrated from Texas factory — install in 5 minutes (18x faster than prior gen)"),
        bullet("4-hour drive from Foxconn Houston / Wistron Fort Worth to Marlie I"),
        divider(),
        h2("Six-Chip Architecture"),
        h3("1. Rubin GPU"),
        bullet("288 GB HBM4 memory"),
        bullet("22 TB/s memory bandwidth"),
        bullet("The inference engine — 72 per NVL72 rack"),
        h3("2. Vera CPU"),
        bullet("88 custom Olympus cores"),
        bullet("Replaces x86 entirely for AI workload orchestration"),
        bullet("36 per rack, paired with Rubin GPUs"),
        h3("3. NVLink 6 Switch"),
        bullet("3.6 TB/s GPU-to-GPU fabric per rack"),
        bullet("260 TB/s across 14-rack DGX SuperPOD"),
        bullet("Eliminates PCIe as the bottleneck"),
        h3("4. ConnectX-9 SuperNIC"),
        bullet("1.6 Tb/s aggregate networking per GPU"),
        bullet("AI traffic between nodes, racks, and storage — zero CPU involvement"),
        h3("5. BlueField-4 DPU"),
        bullet("Security and infrastructure offload at line rate"),
        bullet("Encryption, firewall, storage I/O — GPU cycles reserved for inference only"),
        bullet("First rack-scale confidential computing — unlocks healthcare, finance, government workloads"),
        h3("6. Spectrum-X Ethernet"),
        bullet("800G per port — co-packaged optics"),
        bullet("Scale-out factory fabric for AI east-west traffic at rack scale"),
        divider(),
        h2("Performance vs Prior Generation"),
        bullet("Token cost reduction: 10x lower"),
        bullet("GPUs to train same model: 4x fewer"),
        bullet("GPU-to-GPU NVLink bandwidth: 3.6 TB/s per rack"),
        bullet("NVLink cluster bandwidth (14-rack SuperPOD): 260 TB/s"),
        bullet("Memory per GPU: 288 GB HBM4"),
        bullet("Memory bandwidth per GPU: 22 TB/s"),
        bullet("Inference compute per rack (NVFP4): 3.6 ExaFLOPS"),
        bullet("SuperPOD compute (14 racks): 50.4 ExaFLOPS"),
        bullet("Cooling architecture: 100% liquid — zero air cooling"),
        bullet("Rack deployment time: 5 minutes (18x faster than prior gen)"),
        bullet("Production status: FULL PRODUCTION"),
        bullet("Availability: H2 2026"),
        bullet("TX factory distance to Marlie I: ~4 hours"),
        divider(),
        h2("5 Investor Facts"),
        bullet("First rack-scale confidential computing", "Fact 01"),
        bullet("18x faster deployment — 5 min install vs 1.5 hours prior gen", "Fact 02"),
        bullet("50.4 ExaFLOPS from 14 racks (DGX SuperPOD)", "Fact 03"),
        bullet("260 TB/s NVLink bandwidth across full SuperPOD cluster", "Fact 04"),
        bullet("Full production H2 2026 — Texas factories 4 hours from Marlie I", "Fact 05"),
    ])
    print(f"  {h_url}")

    # ── 03 SITE & BUILDING ────────────────────────────────────────────
    print("Creating 03 — Site & Building Specs...")
    s_id, s_url = create_page(root_id, "03 — Site & Building Specs", icon="🏗️")
    add_blocks(s_id, [
        callout("Scott Tomsu designed and built this building himself, 20 years ago. It has survived multiple direct Gulf hurricane impacts with zero structural damage.", emoji="🏗️", color="green_background"),
        divider(),
        h2("Address"),
        para("1201 SE Evangeline Thruway, Lafayette, LA 70501 — ADC3K HQ"),
        divider(),
        h2("Building Dimensions"),
        bullet("Exterior footprint: 24 ft × 40 ft"),
        bullet("Interior Phase 1 floor: 22 ft × 35 ft — 770 sq ft"),
        bullet("Second floor: available — Phase 2 vertical expansion"),
        bullet("Adjacent property: owned — horizontal expansion ready"),
        divider(),
        h2("Ceiling & Structure"),
        bullet("Plate height: 7 ft 11 in to bottom of ceiling assembly (measured)"),
        bullet("Framing: 2×12"),
        bullet("Ceiling assembly: two layers 5/8\" Type X sheetrock + insulation + full floor above"),
        bullet("Fire rating: UL-rated fire assembly — built-in from day one (original motorcycle shop build)"),
        bullet("Insulation: heavy throughout — complete thermal shell, ideal for cooling stability"),
        bullet("Foundation: reinforced concrete slab"),
        divider(),
        h2("Site Specs"),
        bullet("FEMA Zone: Zone X — Minimal Flood Hazard"),
        bullet("Ground elevation: high ground — above regional base flood elevation"),
        bullet("Zoning: Industrial — heavy use permitted"),
        bullet("Property debt: $15,000 total"),
        bullet("Storm history: multiple hurricanes — zero structural damage"),
        bullet("Roof: solar + skylight ready"),
        bullet("Cooling: 100% liquid cooling design — CDU heat rejection to exterior"),
        bullet("Security: Phase 1 scope — 24/7 monitoring"),
        divider(),
        h2("Phase 1 Floor Plan — Rack Layout"),
        para("Hot aisle / cold aisle containment configuration. Compute equipment only inside the thermal envelope. All mechanical (generators, dry coolers, UPS batteries) located exterior."),
        bullet("Row A: 8× NVL72 racks"),
        bullet("Sealed hot aisle between rows with CDU units at each end"),
        bullet("Row B: 8× NVL72 racks"),
        bullet("Cold supply plenums above and below rack rows"),
        bullet("Network core / fiber MDA / CDU control — compact zone near entry"),
        bullet("CDU liquid loops: cold supply lines in, hot return lines to exterior dry coolers"),
        bullet("Building insulation provides thermal stability — reduces cooling load, optimizes liquid loop efficiency"),
        divider(),
        h2("Scalability — Three Expansion Vectors"),
        bullet("Phase 1: 22×35 ft first floor — up to 16 NVL72 racks, 57.6 ExaFLOPS"),
        bullet("Phase 2: Second floor — full vertical expansion, same footprint"),
        bullet("Phase 3: Adjacent owned property — horizontal campus buildout"),
        para("No land acquisition needed to triple capacity."),
        divider(),
        h2("Infrastructure Proximity"),
        bullet("LUS Fiber: ~0.8 mi — 214 Jefferson St"),
        bullet("LUS Power / Utilities: ~1 mi — 1314 Walker Rd"),
        bullet("Atmos Energy (natural gas): ~3 mi — 1818 Eraste Landry Rd"),
        bullet("SLEMCO Electric: 2727 SE Evangeline Thruway"),
        bullet("Lafayette Regional Airport (LFT): adjacent — GPS 30.20529, -91.98760"),
        bullet("Henry Hub (world gas price benchmark): ~40 mi — Erath, LA"),
        bullet("First Solar 3.5 GW factory: ~20 mi — Iberia Parish"),
        bullet("NVIDIA TX Manufacturing (Foxconn Houston / Wistron Fort Worth): ~4 hours"),
    ])
    print(f"  {s_url}")

    # ── 04 FUNDING STACK ─────────────────────────────────────────────
    print("Creating 04 — Government Funding Stack...")
    f_id, f_url = create_page(root_id, "04 — Government Funding Stack", icon="🏛️")
    add_blocks(f_id, [
        callout("Marlie I does not merely hope to qualify for federal and state incentives — it was designed around them.", emoji="🏛️", color="blue_background"),
        divider(),
        h2("Federal: One Big Beautiful Bill Act (OBBBA)"),
        para("Signed July 4, 2025. Most favorable federal policy environment for domestic AI infrastructure in US history."),
        bullet("FEOC restrictions: Chinese, Russian, Iranian, North Korean supply chain = disqualified from federal credits/grants"),
        bullet("Marlie I: NVIDIA hardware manufactured in Texas (Foxconn Houston, Wistron Fort Worth), 100% US ownership, Louisiana-licensed GC — fully FEOC compliant"),
        bullet("$500M added to BEAD broadband program"),
        bullet("Gulf OCS revenue sharing raised to $650M/year through 2034"),
        bullet("$500B Stargate public-private AI program — Marlie I's FEOC-clean structure qualifies"),
        divider(),
        h2("Federal: BEAD Broadband Program"),
        bullet("Distributes federal funding to expand broadband in underserved areas"),
        bullet("LUS Fiber runs 0.8 miles from the site"),
        bullet("Direct fiber connection to Marlie I accelerates BEAD eligibility for City of Lafayette"),
        bullet("Solves Marlie I connectivity requirements simultaneously"),
        divider(),
        h2("Federal: Gulf OCS Revenue"),
        bullet("OBBBA raised Louisiana's OCS revenue cap from $500M to $650M/year through 2034 — 30% increase"),
        bullet("Louisiana's share ~$200M/year at cap — funds Coastal Master Plan"),
        bullet("Henry Hub, 40 miles from Marlie I — fuel costs benchmarked to most competitive gas price on earth"),
        divider(),
        h2("State: Louisiana Act 730"),
        para("Effective July 1, 2024."),
        bullet("20-year state and local sales and use tax rebate on qualifying AI factory equipment, software, construction materials, installation"),
        bullet("10-year renewal option (30 years total)"),
        bullet("Qualification: $200M+ capital investment + 50+ new permanent jobs"),
        bullet("Direct Payment Number — eliminates tax liability on GPU hardware"),
        bullet("Stackable with Quality Jobs Program (6% payroll rebate, 10 years)"),
        bullet("Stackable with LED FastStart (free customized workforce training)"),
        bullet("Combined with Louisiana #1-ranked industrial electricity rates — unbeatable per-token economics"),
        divider(),
        h2("ADC3K Compliance Position"),
        callout("100% US ownership. Texas-manufactured NVIDIA hardware. Louisiana-licensed GC. Zero foreign entity involvement. Marlie I is not just eligible — it is the ideal OBBBA candidate.", emoji="✅", color="green_background"),
    ])
    print(f"  {f_url}")

    # ── 05 INFRASTRUCTURE PARTNERS ────────────────────────────────────
    print("Creating 05 — Infrastructure Partners...")
    i_id, i_url = create_page(root_id, "05 — Infrastructure Partners", icon="🔗")
    add_blocks(i_id, [
        callout("Every infrastructure partner at the table is not a vendor. They are a node in the same network.", emoji="🔗", color="yellow_background"),
        divider(),
        h2("LUS Fiber"),
        bullet("Address: 214 Jefferson St, Lafayette, LA 70501"),
        bullet("Distance from Marlie I: ~0.8 miles"),
        bullet("Type: Municipal gigabit network — city-owned and operated"),
        bullet("What LUS Fiber gains: anchor industrial fiber customer, justification for BEAD-funded backhaul expansion along SE Evangeline corridor"),
        bullet("No incumbent telco gatekeeping — competitive pricing, natural public-private partnership pathway"),
        divider(),
        h2("LUS Power / Utilities"),
        bullet("Address: 1314 Walker Rd, Lafayette, LA 70506"),
        bullet("Distance from Marlie I: ~1 mile"),
        bullet("Note: Marlie I is off-grid by design — natural gas primary power. LUS Power = backup/grid feed relationship"),
        bullet("Excess generation capacity feeds back to LUS grid — revenue stream + city utility relationship"),
        divider(),
        h2("Atmos Energy — Natural Gas"),
        bullet("Address: 1818 Eraste Landry Rd, Lafayette, LA 70506"),
        bullet("Distance from Marlie I: ~3 miles"),
        bullet("What Atmos gains: long-term industrial gas supply contract, high-volume predictable load"),
        bullet("Henry Hub benchmark (Erath, LA) — 40 miles — locks Marlie I fuel costs to most competitive gas price on earth"),
        divider(),
        h2("SLEMCO Electric"),
        bullet("Address: 2727 SE Evangeline Thruway, Lafayette, LA 70508"),
        bullet("Note: Secondary electric relationship — Marlie I primary power is on-site natural gas generation"),
        divider(),
        h2("Lafayette Regional Airport (LFT)"),
        bullet("GPS: 30.20529, -91.98760"),
        bullet("Distance: adjacent to Marlie I site"),
        bullet("ADC3K holds FAA Private Pilot Certificate + Part 107 Remote Pilot Certificate"),
        bullet("Commercial UAS operations from site — inspection, survey, last-mile logistics"),
        bullet("What LFT gains: active commercial Part 107 operator adjacent to controlled airspace"),
        divider(),
        h2("City of Lafayette / Louisiana Economic Development"),
        bullet("Act 730 qualified — 20-year equipment tax exemption"),
        bullet("OBBBA compliant — FEOC-clean, Texas-manufactured hardware, Louisiana GC"),
        bullet("50+ permanent jobs required for Act 730 certification"),
        bullet("Lafayette becomes home to Louisiana's first Rubin-class AI factory"),
        bullet("Hub of the ADC3K Louisiana AI Network — three sites planned"),
    ])
    print(f"  {i_url}")

    # ── 06 ADC3K CREDENTIALS ──────────────────────────────────────────
    print("Creating 06 — ADC3K Credentials...")
    c_id, c_url = create_page(root_id, "06 — ADC3K Credentials", icon="🎓")
    add_blocks(c_id, [
        callout("Scott Tomsu — Owner/Operator — ADC3K (Advantage Design Construction)", emoji="🎓", color="gray_background"),
        divider(),
        h2("Certifications"),
        bullet("Louisiana General Contractor License — active — eliminates 10-15% GC markup, single point of accountability"),
        bullet("7 NVIDIA Certifications — AI infrastructure design, GPU compute deployment, NVIDIA partner program"),
        bullet("FAA Private Pilot Certificate"),
        bullet("FAA Part 107 Remote Pilot Certificate (commercial UAS)"),
        bullet("CompTIA A+ — earned late 1990s"),
        bullet("CompTIA Network+ — earned late 1990s"),
        divider(),
        h2("Background"),
        bullet("20 years underwater robotics / ROV work — Gulf of Mexico oil and gas industry"),
        bullet("Systems operating at depth, under pressure, in hostile environments — zero tolerance for failure"),
        bullet("AI factory operations demand the same discipline: continuous uptime, redundant systems, immediate fault response"),
        bullet("Built 1201 SE Evangeline Thruway himself — 20 years standing, hurricane-proven"),
        divider(),
        h2("Why This Matters for Investors"),
        bullet("No third-party GC — Scott pulls permits, hires trades, executes buildout directly"),
        bullet("No third-party integrator for NVIDIA hardware — 7 certifications enable direct rack-and-power"),
        bullet("Revenue from day one — no markup, no delay, no middlemen"),
        bullet("GC license + building + certifications = one team, one point of accountability"),
        bullet("Field-hardened systems thinking — not finance background, not software background — infrastructure operations"),
    ])
    print(f"  {c_url}")

    # ── 07 MULTI-SITE VISION ──────────────────────────────────────────
    print("Creating 07 — Louisiana AI Network Vision...")
    v_id, v_url = create_page(root_id, "07 — Louisiana AI Network: Multi-Site Vision", icon="🌐")
    add_blocks(v_id, [
        callout("We are not building a data center. We are building a network.", emoji="🌐", color="yellow_background"),
        divider(),
        h2("Phase 1 — MARLIE I (Active)"),
        para("Home base. ADC3K's owned property — $15K total debt. The proving ground. First Rubin-class AI factory in Louisiana."),
        bullet("Location: 1201 SE Evangeline Thruway, Lafayette, LA 70501"),
        bullet("Target: H2 2026 operational"),
        bullet("Floor: 22×35 ft Phase 1 + second floor + adjacent property"),
        bullet("Establishes: cash flow, operational credibility, infrastructure partnerships, and the playbook"),
        callout("Activation: Now — investor and infrastructure partner outreach active", emoji="🟢", color="green_background"),
        divider(),
        h2("Phase 2 — Site Two (In Development)"),
        para("Funded by Marlie I cash flow. Playbook already written. Infrastructure relationships already established."),
        bullet("Location: TBD — ADC3K Louisiana Network"),
        bullet("ADC3K replicates the model with speed and precision no outside operator can match"),
        callout("Activation Trigger: Marlie I reaches operational revenue threshold → Site Two capital deploy begins. No external fundraising required at that stage.", emoji="🟡", color="yellow_background"),
        divider(),
        h2("Phase 3 — Site Three (In Development)"),
        para("Third node completes the Louisiana hub-and-spoke architecture. Statewide inference capacity at enterprise-grade scale."),
        bullet("Location: TBD — ADC3K Louisiana Network"),
        bullet("Combined: three ADC3K sites → statewide AI inference network → enterprise + government + city infrastructure at scale"),
        bullet("Three sites. One network. One operator."),
        callout("Activation Trigger: Site Two operational → Site Three capital deploy begins.", emoji="⚫", color="gray_background"),
        divider(),
        h2("What Each Infrastructure Partner Gains Across the Network"),
        bullet("LUS Fiber: anchor customer + justification for BEAD backhaul expansion along SE Evangeline corridor", "LUS FIBER"),
        bullet("Long-term industrial gas supply contract — high-volume predictable load, rate stability across distribution network", "ATMOS GAS"),
        bullet("Active Part 107 commercial UAS operator adjacent to controlled airspace — inspection, logistics, survey", "LFT AIRPORT"),
        bullet("Louisiana's first Rubin-class AI factory — Act 730 qualified, OBBBA compliant, 50+ permanent jobs, Lafayette on national AI map", "CITY / LED"),
        divider(),
        quote("ADC3K is not asking the city for a favor. ADC3K is inviting Lafayette's infrastructure partners to build the city's next chapter with us. Every site we add is another node in Lafayette's economic future."),
    ])
    print(f"  {v_url}")

    # ── 08 CONTACT ────────────────────────────────────────────────────
    print("Creating 08 — Contact & CTA...")
    ct_id, ct_url = create_page(root_id, "08 — Contact & Next Steps", icon="📞")
    add_blocks(ct_id, [
        h2("ADC3K — Advantage Design Construction"),
        bullet("Owner/Operator: Scott Tomsu"),
        bullet("Address: 1201 SE Evangeline Thruway, Lafayette, LA 70501"),
        bullet("Email: SCOTT@ADC3K.COM"),
        bullet("Phone: 337-780-1535"),
        bullet("Web: www.adc3k.com"),
        divider(),
        h2("Investor Pitch Page"),
        para("Full interactive pitch page (HTML): marlie/index.html in gpu-learning-lab repo"),
        divider(),
        h2("Next Steps"),
        bullet("Schedule infrastructure partner meetings: LUS Fiber, Atmos Energy, LUS Power, LFT Airport"),
        bullet("Louisiana Economic Development — Act 730 pre-qualification"),
        bullet("NVIDIA partner program — NVL72 procurement pipeline"),
        bullet("Investor term sheet discussions"),
        bullet("Phase 1 buildout kickoff — 6 month deploy timeline"),
        divider(),
        callout("Marlie I is named for Marlie — a reminder that what we build outlasts the spreadsheet. The federal money is flowing. The hardware is in production. The site is ready. The only question is who is at the table when Marlie I goes live.", emoji="⚡", color="yellow_background"),
    ])
    print(f"  {ct_url}")

    print("\n✓ MARLIE I Notion workbook complete.")
    print(f"\nRoot page: {root_url}")
    return root_url

if __name__ == "__main__":
    build_workbook()
