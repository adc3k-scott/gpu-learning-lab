"""Rebuild Trappeys AI Center Notion page with clean organized structure."""
import os, sys, json, urllib.request, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

token = None
for p in [".venv/.env", ".env"]:
    try:
        for line in open(os.path.join(r"c:/Users/adhsc/OneDrive/Documents/GitHub/gpu-learning-lab", p)):
            if line.startswith("NOTION_API_KEY"):
                token = line.split("=", 1)[1].strip()
    except:
        pass

def notion(method, path, body=None):
    req = urllib.request.Request(
        f"https://api.notion.com/v1{path}",
        data=json.dumps(body).encode() if body else None,
        headers={"Authorization": f"Bearer {token}", "Notion-Version": "2022-06-28", "Content-Type": "application/json"},
        method=method,
    )
    with urllib.request.urlopen(req) as r:
        return json.load(r)

TRAPPEYS_ID = "31288f09-7e31-80a2-8712-ef09878afd53"

def tx(t, bold=False, color="default"):
    return {"type": "text", "text": {"content": t}, "annotations": {"bold": bold, "italic": False, "strikethrough": False, "underline": False, "code": False, "color": color}}

def h1(t):      return {"object": "block", "type": "heading_1", "heading_1": {"rich_text": [tx(t)]}}
def h2(t):      return {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [tx(t)]}}
def h3(t):      return {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [tx(t)]}}
def para(*ts):  return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": list(ts)}}
def bullet(*ts):return {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": list(ts)}}
def num(*ts):   return {"object": "block", "type": "numbered_list_item", "numbered_list_item": {"rich_text": list(ts)}}
def divider():  return {"object": "block", "type": "divider", "divider": {}}

def callout(t, emoji="📁", color="gray_background"):
    return {"object": "block", "type": "callout", "callout": {
        "rich_text": [tx(t)], "icon": {"type": "emoji", "emoji": emoji}, "color": color}}

blocks = [
    callout("ARCHIVE — Predecessor project to MARLIE I. All active development is under ADC 3K -> MARLIE I.", "🗃️", "yellow_background"),
    divider(),
    h1("Trappeys AI Center — Project Archive"),
    para(tx("The original concept for deploying next-generation AI compute infrastructure at 1201 SE Evangeline Thruway, Lafayette, LA. Evolved through three major engineering iterations before rebranding as MARLIE I under ADC 3K in early 2026.")),
    divider(),

    h2("Status"),
    bullet(tx("Status: ", False), tx("ARCHIVED", True, "red"), tx(" — superseded by MARLIE I — Lafayette AI Factory")),
    bullet(tx("Site: 1201 SE Evangeline Thruway, Lafayette, LA — same site, rebranded and upgraded")),
    bullet(tx("Hardware: Evolved from Blackwell-era specs to NVIDIA Vera Rubin NVL72 (H2 2026)")),
    bullet(tx("Power strategy carried forward: Bloom Energy fuel cells + Cat natural gas prime power + Henry Hub advantage")),
    bullet(tx("Cooling architecture carried forward: CDU liquid-cooled, dry cooler heat rejection")),
    bullet(tx("Operations platform carried forward: Mission Control AI (built and operational under ADC 3K)")),
    bullet(tx("Active project: ", False), tx("ADC 3K -> MARLIE I — Lafayette AI Factory", True)),
    divider(),

    h2("Document Vault — 5 Uploaded Files"),
    para(tx("All original engineering and investor documents uploaded directly above this section. Click any file to open in Notion.", False, "gray")),
    para(),
    h3("Investor Materials"),
    bullet(tx("Trappeys-AI-Data-Center-Investor-Deck.pptx", True), tx(" — Original investor pitch deck. Superseded by MARLIE I deck. Historical reference for investment thesis evolution.")),
    para(),
    h3("V3 — Strategy & Operations (Latest Pre-MARLIE)"),
    bullet(tx("Containerized-AI-Compute-Pod-V3-Strategy-Operations.docx", True), tx(" — Final iteration before MARLIE I rebrand. Site layout, ops model, power strategy, Act 730 incentive capture, Bloom Energy, investor framework (Appendices J-Q).")),
    para(),
    h3("Engineering Package"),
    bullet(tx("Containerized-AI-Compute-Pod-Engineering-Package.docx", True), tx(" — Full site engineering package: floor plan, rack layout, CDU placement, power distribution, network topology.")),
    bullet(tx("Trappeys-Engineering-Diagrams.html", True), tx(" — Browser-viewable engineering diagrams. Open in browser for best viewing.")),
    para(),
    h3("V2 — Appendices"),
    bullet(tx("Containerized-AI-Compute-Pod-V2-Appendices.docx", True), tx(" — Supporting appendices from V2 phase: equipment specs, vendor contacts, piping details, electrical specs, risk register.")),
    divider(),

    h2("V3 Document Contents (Appendices J-Q)"),
    para(tx("The V3 Strategy & Operations doc contains the most complete pre-MARLIE engineering package:", False, "gray")),
    bullet(tx("Appendix J — Tax Incentive Capture: Act 730 rebate model, $200M qualifying threshold, combined incentive stack")),
    bullet(tx("Appendix K — NVIDIA Mission Control Software Integration: BMS integration, Schneider EcoStruxure, power optimization")),
    bullet(tx("Appendix L — Piping & Electrical Specifications: cooling piping, conductor sizing, grounding system")),
    bullet(tx("Appendix M — Workforce Plan & Staffing Model: staffing tiers, Louisiana talent pipeline, Act 730 job requirements")),
    bullet(tx("Appendix N — Investor Pitch Framework: investment thesis, market opportunity, financial summary")),
    bullet(tx("Appendix O — 30/60/90-Day Master Schedule: procurement, build, commission phases with Gantt summary")),
    bullet(tx("Appendix P — Risk Register")),
    bullet(tx("Appendix Q — Vendor Contact Directory")),
    divider(),

    h2("Project Evolution Timeline"),
    num(tx("V1 — Concept: Containerized GPU pods. Air-cooled. Ampere-era hardware. Proof-of-concept scale.")),
    num(tx("V2 — Engineering Package: Liquid cooling added. CDU architecture defined. Hopper-era hardware. Full engineering diagrams.")),
    num(tx("V3 — Strategy Pivot: Natural gas prime power formalized. Bloom Energy added. Blackwell-era hardware. Act 730 model built.")),
    num(tx("MARLIE I (Active): Full rebrand. Vera Rubin NVL72. Two-floor build (32 racks, 115.2 ExaFLOPS). OBBBA compliance. Lafayette Infrastructure Partnership.")),
    divider(),

    h2("What Carried Forward into MARLIE I"),
    bullet(tx("Site: 1201 SE Evangeline Thruway — owner-controlled, debt-free, FEMA Zone X")),
    bullet(tx("Power: Natural gas prime power + Bloom Energy fuel cells + Henry Hub proximity")),
    bullet(tx("Cooling: Closed-loop direct-to-chip liquid, CDU architecture, dry cooler heat rejection")),
    bullet(tx("Connectivity: LUS Fiber primary, 0.8 miles from site")),
    bullet(tx("Operations: AI-managed Mission Control platform — 3-5 FTE vs 20-50 legacy")),
    bullet(tx("Incentives: Act 730 qualification, OBBBA compliance path")),
    divider(),

    h2("Sub-Pages"),
    bullet(tx("Hardware Evolution Log", True), tx(" — GPU architecture progression: Ampere to Hopper to Blackwell to Vera Rubin with full specs")),
    bullet(tx("Site History — 1201 SE Evangeline Thruway", True), tx(" — Site selection rationale, pre-development condition, structural history, expansion capacity")),
    divider(),

    callout("Active MARLIE I documents, deck, and financials are in ADC 3K — Project Command Center -> MARLIE I — Lafayette AI Factory.", "🚀", "green_background"),
]

for i in range(0, len(blocks), 40):
    batch = blocks[i:i+40]
    notion("PATCH", f"/blocks/{TRAPPEYS_ID}/children", {"children": batch})
    time.sleep(0.3)
    print(f"  Pushed {i+1}-{min(i+40, len(blocks))}")

print(f"Done — {len(blocks)} blocks.")
