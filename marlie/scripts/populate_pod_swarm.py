"""Populate Pod Swarm Engineering Suite with real technical content."""
import httpx, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

KEY = "NOTION_API_TOKEN_REDACTED"
HEADERS = {
    "Authorization": f"Bearer {KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}
POD_SWARM_ID = "31d88f097e31814c8a49ffea016555e4"


def api(method, path, data=None):
    r = httpx.request(method, f"https://api.notion.com/v1{path}", headers=HEADERS, json=data, timeout=30)
    if r.status_code not in (200, 201):
        print(f"ERROR {r.status_code}: {r.text[:300]}")
        sys.exit(1)
    return r.json()


def create_page(parent_id, title, icon="📄", children=None):
    payload = {
        "parent": {"page_id": parent_id},
        "icon": {"type": "emoji", "emoji": icon},
        "properties": {"title": {"title": [{"text": {"content": title}}]}},
    }
    if children:
        payload["children"] = children
    r = api("POST", "/pages", payload)
    return r["id"], r.get("url", "")


def add_blocks(page_id, blocks):
    for i in range(0, len(blocks), 95):
        api("PATCH", f"/blocks/{page_id}/children", {"children": blocks[i:i+95]})


def h2(t):
    return {"object": "block", "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": t}}]}}

def h3(t):
    return {"object": "block", "type": "heading_3",
            "heading_3": {"rich_text": [{"type": "text", "text": {"content": t}}]}}

def para(t):
    return {"object": "block", "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": t}}]}}

def bullet(label, val=None):
    if val:
        rich = [
            {"type": "text", "text": {"content": label + ": "},
             "annotations": {"bold": True, "italic": False, "strikethrough": False,
                             "underline": False, "code": False, "color": "default"}},
            {"type": "text", "text": {"content": val},
             "annotations": {"bold": False, "italic": False, "strikethrough": False,
                             "underline": False, "code": False, "color": "default"}},
        ]
    else:
        rich = [{"type": "text", "text": {"content": label}}]
    return {"object": "block", "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": rich}}

def callout(t, emoji="💡", color="gray_background"):
    return {"object": "block", "type": "callout",
            "callout": {"rich_text": [{"type": "text", "text": {"content": t}}],
                        "icon": {"type": "emoji", "emoji": emoji},
                        "color": color}}

def code(t, lang="plain text"):
    return {"object": "block", "type": "code",
            "code": {"rich_text": [{"type": "text", "text": {"content": t}}], "language": lang}}

def divider():
    return {"object": "block", "type": "divider", "divider": {}}


# ── 1. NVL72 Rack Configuration ───────────────────────────────────────────────
print("Creating NVL72 Rack Configuration...")
rid, rurl = create_page(POD_SWARM_ID, "NVL72 Rack Configuration & Cable Plans", icon="🗄️")
add_blocks(rid, [
    callout("NVIDIA Vera Rubin NVL72 — 72 Rubin GPUs + 36 Vera CPUs per rack. 3.6 ExaFLOPS NVFP4. 100% liquid cooled. Full production H2 2026.", emoji="🗄️", color="blue_background"),
    divider(),
    h2("Phase 1 Layout — 22 x 35 ft Floor (770 sq ft)"),
    bullet("Total racks", "16 NVL72 units"),
    bullet("Arrangement", "Row A (8 racks) + Row B (8 racks) — hot aisle contained between rows"),
    bullet("Walk-through", "Cold aisle access front and rear — sealed hot aisle center"),
    bullet("Aggregate compute", "57.6 ExaFLOPS NVFP4"),
    bullet("Aggregate memory BW", "260 TB/s"),
    divider(),
    h2("Per-Rack Specs (NVL72)"),
    bullet("GPUs", "72x Rubin GPU — 36 per NVLink domain, 2 domains per rack"),
    bullet("CPUs", "36x Vera CPU — 88 Olympus Arm cores (Armv9.2) each, 1.5 TB LPDDR5X, 1.2 TB/s memory BW per CPU"),
    bullet("NVLink 6 Switches", "9x switch trays per rack — 28.8 TB/s per tray, 260 TB/s aggregate, in-network SHARP FP8 compute"),
    bullet("Memory", "HBM4 — 288 GB per Rubin GPU, 20.7 TB total per NVL72 rack, 1.58 PB/s aggregate bandwidth"),
    bullet("Power per rack", "TDP not yet published by NVIDIA — contact NVIDIA Enterprise Sales for facility planning specs"),
    bullet("Cooling", "Rear-door CDU manifold — 100% liquid, no air cooling"),
    divider(),
    h2("Cable Plans"),
    h3("NVLink Fabric (Intra-rack)"),
    bullet("Topology", "NVLink 6 Switch — full mesh within rack via 9-switch rail"),
    bullet("Cable type", "NVIDIA NVLink optical cables — pre-routed at factory"),
    bullet("Field cabling required", "None for NVLink intra-rack"),
    divider(),
    h3("InfiniBand NDR (Inter-rack)"),
    bullet("NIC", "ConnectX-9 SuperNIC — 1.6 Tb/s per adapter, 800 Gb/s per port — >144 adapters per NVL72"),
    bullet("Fabric", "NDR400 InfiniBand — 400 Gb/s per port"),
    bullet("Switch", "NVIDIA Quantum-3 InfiniBand — top-of-rack or end-of-row"),
    bullet("Cable type", "NVIDIA Quantum HDR/NDR DAC or optical — 2m intra-row, 5m cross-row"),
    bullet("Total uplinks", "16 racks x 2 ports = 32 uplinks to spine"),
    divider(),
    h3("Ethernet Management (BlueField-4 DPU)"),
    bullet("DPU", "BlueField-4 — 1x per NVL72 — OOB management + storage offload"),
    bullet("Uplink", "10GbE management — 1 cable per rack to management switch"),
    bullet("Switch", "Dedicated 24-port 10GbE management switch in network core"),
    divider(),
    h2("Rack Numbering Convention"),
    code(
        "Row A: A01 A02 A03 A04 A05 A06 A07 A08  (cold aisle front)\n"
        "              [sealed hot aisle]\n"
        "Row B: B01 B02 B03 B04 B05 B06 B07 B08  (cold aisle rear)\n\n"
        "Network Core: NC01 (north end, near entry)\n"
        "CDU Manifold: Runs along exterior north wall"
    ),
    divider(),
    h2("NVIDIA Field Resources"),
    bullet("DGX-Ready colocation checklist", "developer.nvidia.com/dgx-ready-data-center"),
    bullet("NVL72 power + cooling specs", "Contact NVIDIA Enterprise Sales"),
    bullet("Field installation", "NVIDIA-certified solution architect required"),
])
print(f"  OK: {rurl}")

# ── 2. CDU Liquid Cooling Schematics ──────────────────────────────────────────
print("Creating CDU Liquid Cooling Schematics...")
cid, curl = create_page(POD_SWARM_ID, "CDU Liquid Cooling Schematics", icon="💧")
add_blocks(cid, [
    callout("NVL72 is 100% liquid cooled. No air cooling fallback. CDU units mount rear of each rack. Heat rejected to exterior dry coolers via closed glycol loop.", emoji="💧", color="blue_background"),
    divider(),
    h2("System Overview"),
    bullet("Type", "Rear-door liquid cooling — CDU (Coolant Distribution Unit) per rack"),
    bullet("Loop", "Closed primary loop: rack CDU <-> exterior dry cooler"),
    bullet("Coolant", "Deionized water + glycol mix (40/60 for Louisiana climate)"),
    bullet("Heat rejection", "Exterior dry coolers — no chiller required at Phase 1 scale"),
    bullet("Phase 1 heat load", "NVIDIA has not published rack TDP — facility sizing requires NVIDIA Enterprise engagement; plan for 150-250 kW/rack range per industry analyst estimates (unconfirmed)"),
    divider(),
    h2("Loop Topology"),
    h3("Primary Loop (High Temp)"),
    bullet("Supply temp target", "45C supply to CDU inlet"),
    bullet("Return temp target", "55-60C return from CDU outlet"),
    bullet("Flow rate", "Per NVIDIA CDU spec — typically 20-40 L/min per rack"),
    bullet("Pump", "Variable speed — pressure regulated"),
    divider(),
    h3("Secondary Loop (Dry Cooler)"),
    bullet("Location", "Exterior — north wall or rooftop mount"),
    bullet("Type", "Adiabatic dry cooler — air-cooled finned coil, optional misting for peak days"),
    bullet("Climate note", "Lafayette avg high 93F summer — size dry cooler for 100F ambient"),
    bullet("Glycol loop", "Runs through exterior wall penetration (insulated sleeve)"),
    bullet("Isolation valve", "1x ball valve per dry cooler — serviceable without rack downtime"),
    divider(),
    h2("Pipe Routing Schematic — Phase 1"),
    code(
        "Exterior wall (north)\n"
        "  [Dry Cooler 1] [Dry Cooler 2] [Dry Cooler 3] [Dry Cooler 4]\n"
        "       |               |               |               |\n"
        "  ====[ Supply manifold — 4-inch insulated pipe along north wall ]====\n"
        "       |               |               |               |\n"
        "  [CDU A01-A04]  [CDU A05-A08]  [CDU B01-B04]  [CDU B05-B08]\n"
        "  ====[ Return manifold — 4-inch insulated pipe along north wall ]====\n"
        "       |               |               |               |\n"
        "  [ Pump station — NW corner — 2x variable speed pumps, 1 redundant ]"
    ),
    divider(),
    h2("Key Components"),
    bullet("CDU units", "16x — 1 per NVL72 rack (NVIDIA-supplied or approved vendor)"),
    bullet("Dry coolers", "4x exterior — sized for 500 kW each (2 MW total capacity)"),
    bullet("Pump station", "2x variable speed pumps — N+1 redundancy"),
    bullet("Expansion tank", "1x — pressure relief, glycol makeup"),
    bullet("Flow meters", "1x per CDU loop — monitored via BMS"),
    bullet("Leak detection", "Rope-style sensor along entire manifold run"),
    bullet("Isolation valves", "Ball valves at each CDU inlet/outlet — hot-swap capable"),
    divider(),
    h2("Wall Penetration Detail"),
    bullet("Penetration size", "6-inch core drill — north exterior wall"),
    bullet("Sleeve", "Insulated pipe sleeve — vapor barrier sealed"),
    bullet("Fire stop", "Intumescent firestop collar — maintain Type X fire rating"),
    bullet("Contractor", "Licensed mechanical contractor — permit required"),
    divider(),
    h2("Monitoring"),
    bullet("BMS", "Building Management System — supply/return temps, flow rate, leak status"),
    bullet("Alerts", "High temp (>62C return), low flow, leak detection — SMS + Mission Control event"),
    bullet("Integration", "InfraManagerAgent monitors BMS via HTTP API or Modbus gateway"),
])
print(f"  OK: {curl}")

# ── 3. Power Distribution Unit Layouts ────────────────────────────────────────
print("Creating PDU Layouts...")
pid, purl = create_page(POD_SWARM_ID, "Power Distribution Unit Layouts", icon="⚡")
add_blocks(pid, [
    callout("Phase 1 target: ~2 MW total load (16 NVL72 racks + cooling + network). Natural gas generators and UPS batteries stay outside the thermal envelope.", emoji="⚡", color="yellow_background"),
    divider(),
    h2("Power Architecture"),
    bullet("Source A", "LUS Power utility feed — primary"),
    bullet("Source B", "Natural gas generators (exterior) — automatic transfer switch (ATS)"),
    bullet("UPS", "Exterior battery cabinet — bridges utility-to-generator gap (~10-15 sec)"),
    bullet("Distribution", "480V 3-phase to main panel — step-down to rack PDUs"),
    bullet("Phase 1 load estimate", "NVIDIA rack TDP unconfirmed — size service for 150-250 kW/rack per analyst range; final spec requires NVIDIA Enterprise engagement"),
    divider(),
    h2("Exterior Equipment (Outside Thermal Envelope)"),
    bullet("Generators", "2x natural gas gensets — N+1 — exterior south pad mount"),
    bullet("ATS", "Automatic Transfer Switch — exterior weatherproof enclosure"),
    bullet("UPS batteries", "Battery cabinet — exterior weatherproof, climate controlled"),
    bullet("Main disconnect", "Main breaker panel — exterior accessible"),
    divider(),
    h2("Interior Distribution"),
    h3("Main Distribution Panel"),
    bullet("Feed", "480V 3-phase from exterior ATS through conduit penetration"),
    bullet("Breakers", "1x 400A 3-phase breaker per 2-rack PDU zone (8 breakers total)"),
    bullet("Location", "Network core — north end of room"),
    divider(),
    h3("Per-Rack PDU"),
    bullet("Qty", "8x dual-feed PDUs — each serves 2 NVL72 racks"),
    bullet("Type", "Metered, switched — remote outlet control via SNMP/REST"),
    bullet("Input", "480V 3-phase / 200A per PDU"),
    bullet("Monitoring", "Per-outlet current metering — feeds InfraManagerAgent"),
    divider(),
    h2("Generator Spec (Preliminary)"),
    bullet("Fuel", "Natural gas — Atmos Energy supply line"),
    bullet("Size", "2x 1.25 MW continuous — N+1 for 2 MW load"),
    bullet("Startup", "Auto-start on utility fail — <15 sec to full load"),
    bullet("Enclosure", "Sound-attenuated weatherproof — exterior pad mount"),
    bullet("Fuel line", "Atmos Energy commercial service — 2-inch minimum supply"),
    divider(),
    h2("PUE Target"),
    code(
        "PUE = Total Facility Power / IT Equipment Power\n"
        "    = (1.92 MW compute + 0.06 MW cooling aux + 0.02 MW misc) / 1.92 MW\n"
        "    = ~1.04  (liquid cooled, no CRAC units, no hot aisle air handling)\n\n"
        "Industry best practice: <1.2\n"
        "Hyperscale liquid-cooled target: <1.1\n"
        "MARLIE I target: <1.05"
    ),
    divider(),
    h2("Monitoring"),
    bullet("Mission Control", "InfraManagerAgent — real-time kW per rack, PUE, phase balance"),
    bullet("Alerts", "Over-current, phase imbalance, generator ATS transfer events, UPS state"),
])
print(f"  OK: {purl}")

# ── 4. Network Topology Diagrams ──────────────────────────────────────────────
print("Creating Network Topology...")
nid, nurl = create_page(POD_SWARM_ID, "Network Topology Diagrams", icon="🌐")
add_blocks(nid, [
    callout("Three separate fabrics: NVLink 6 (intra-rack GPU), InfiniBand NDR (inter-rack compute), Spectrum-X Ethernet (external/storage). Management on isolated 10GbE.", emoji="🌐", color="blue_background"),
    divider(),
    h2("Fabric 1 — NVLink 6 (Intra-Rack GPU Fabric)"),
    bullet("Scope", "Within each NVL72 rack only"),
    bullet("Bandwidth", "1.8 Tb/s all-to-all between all 72 GPUs in rack"),
    bullet("Topology", "Rail-optimized via 9x NVLink 6 Switch per rack"),
    bullet("Cabling", "Factory-integrated — no field assembly"),
    bullet("Latency", "Sub-microsecond GPU-to-GPU within rack"),
    divider(),
    h2("Fabric 2 — InfiniBand NDR (Inter-Rack Compute Fabric)"),
    code(
        "                 [ IB Spine Switch (64-port NDR400) ]\n"
        "                /              |              \\\n"
        "       [IB Leaf 1]        [IB Leaf 2]        [IB Leaf 3]\n"
        "       (32-port NDR)      (32-port NDR)      (32-port NDR)\n"
        "      / | | | | \\        / | | | | \\        / | | | | \\\n"
        "    A01 A02 A03 A04   A05 A06 A07 A08   B01 B02 B03 B04\n"
        "                                         B05 B06 B07 B08\n\n"
        "Each rack: 2x ConnectX-9 SuperNIC (1.6 Tb/s each)\n"
        "Each leaf: 16 downlinks (rack) + 8 uplinks (spine)\n"
        "Total bisection BW: ~25.6 Tb/s\n"
        "Oversubscription: 2:1 leaf-to-spine"
    ),
    bullet("Switch vendor", "NVIDIA Quantum-3 InfiniBand"),
    bullet("Per-port BW", "400 Gb/s NDR"),
    divider(),
    h2("Fabric 3 — Spectrum-X Ethernet (External / Storage)"),
    code(
        "[ LUS Fiber Uplink -- 100GbE (upgrade path: 400GbE) ]\n"
        "        |\n"
        "  [ Spectrum-6 (SN6810 / SN6800) Top-of-Row Switch ]\n"
        "   /    |    |    |    |    |    |    \\\n"
        " A01  A02  ...  B08  [NAS] [Object Store] [Customer VPN]\n\n"
        "Each NVL72: 1x 400GbE to Spectrum-X via BlueField-4 DPU\n"
        "Purpose: external customer traffic, storage, internet uplink"
    ),
    bullet("LUS Fiber uplink", "100GbE day 1 — upgrade path to 400GbE / dark fiber"),
    bullet("BlueField-4 DPU", "Offloads networking/storage from Vera CPU — 1 per rack"),
    bullet("Switch", "NVIDIA Spectrum-6 (SN6810 — 102.4 Tb/s / SN6800 — 409.6 Tb/s) — co-packaged optics, 800 Gb/s ports"),
    divider(),
    h2("Fabric 4 — Management Network (OOB)"),
    code(
        "[ Management Switch -- 24-port 10GbE ]\n"
        "  |  |  |  |  ...  |  |  |  |\n"
        " A01 A02 ... B08  [MC Server] [BMS GW] [KVM/IPMI]\n\n"
        "Purpose: out-of-band management, independent of compute fabrics\n"
        "Access: BMC/IPMI per rack + BlueField-4 DPU management port\n"
        "Remote: WireGuard / Tailscale VPN"
    ),
    divider(),
    h2("WAN / Uplink"),
    bullet("Provider", "LUS Fiber — city-owned, direct negotiation, no Big Telecom premium"),
    bullet("Day 1", "100GbE dedicated"),
    bullet("Upgrade path", "400GbE or dark fiber as customer demand grows"),
    bullet("Redundancy", "SLEMCO or secondary carrier as failover"),
    bullet("BGP", "Own AS number + IP block for sovereign routing — Phase 2 target"),
    divider(),
    h2("IP Plan (Draft)"),
    code(
        "Management:    10.0.0.0/24    -- BMC, switches, BMS\n"
        "Compute IB:    10.1.0.0/16    -- InfiniBand fabric\n"
        "Storage/Eth:   10.2.0.0/16    -- Spectrum-X tenant fabric\n"
        "Customer VMs:  10.100.0.0/16  -- NAT to LUS uplink\n"
        "Mission Ctrl:  10.0.0.1\n"
        "DNS/NTP:       10.0.0.2"
    ),
])
print(f"  OK: {nurl}")

# ── 5. RunPod API Integration Notes ───────────────────────────────────────────
print("Creating RunPod API Integration Notes...")
aid, aurl = create_page(POD_SWARM_ID, "RunPod API Integration Notes", icon="🤖")
add_blocks(aid, [
    callout("Mission Control manages RunPod cloud GPU pods via GraphQL API. IntegrationAgent dispatches via runpod skill. When MARLIE I goes live, on-prem racks replace RunPod cloud as primary.", emoji="🤖", color="gray_background"),
    divider(),
    h2("Current Setup — RunPod Cloud"),
    bullet("Endpoint", "https://api.runpod.io/graphql"),
    bullet("Auth", "Bearer token — RUNPOD_API_KEY in .venv/.env"),
    bullet("Skill", "skills/builtin/runpod.py — list / start / stop / terminate"),
    bullet("Planner patterns", "list pods | pod status | start pod | stop pod | terminate pod"),
    divider(),
    h2("GraphQL Operations"),
    h3("List Pods"),
    code(
        "query {\n"
        "  myself {\n"
        "    pods {\n"
        "      id name status\n"
        "      runtime { uptimeInSeconds gpus { id gpuUtilPercent } }\n"
        "      machine { gpuDisplayName }\n"
        "    }\n"
        "  }\n"
        "}",
        "graphql"
    ),
    h3("Start Pod"),
    code(
        "mutation {\n"
        "  podResume(input: { podId: \"POD_ID\", gpuCount: 1 }) {\n"
        "    id status\n"
        "  }\n"
        "}",
        "graphql"
    ),
    h3("Stop Pod"),
    code(
        "mutation {\n"
        "  podStop(input: { podId: \"POD_ID\" }) {\n"
        "    id status\n"
        "  }\n"
        "}",
        "graphql"
    ),
    divider(),
    h2("Mission Control Flow"),
    bullet("Chat trigger", '"list pods" / "start pod XYZ" / "stop pod XYZ"'),
    bullet("Planner", "Regex fast-path -> IntegrationAgent -> runpod skill"),
    bullet("SSE stream", "/tasks/{id}/stream — live step events during pod ops"),
    bullet("Dashboard", "Mission Control HQ at http://localhost:8000"),
    divider(),
    h2("MARLIE I Transition Plan (H2 2026)"),
    callout("When NVL72 racks go live, on-prem becomes primary. RunPod cloud is overflow. Mission Control routes by cost/latency/availability.", emoji="⚡", color="yellow_background"),
    bullet("Phase 1 (now)", "RunPod cloud — dev/test workloads"),
    bullet("Phase 2 (H2 2026)", "MARLIE I on-prem — production inference + training"),
    bullet("Phase 3", "Hybrid routing — Mission Control schedules across on-prem + cloud"),
    divider(),
    h2("On-Prem API Design (Future)"),
    bullet("Protocol", "OpenAI-compatible REST — drop-in for cloud providers"),
    bullet("Auth", "API key per customer — managed by Mission Control"),
    bullet("Billing", "Per-GPU-hour metering via PDU current sensors"),
    bullet("Scheduler", "OrchestratorAgent — job queue, priority, multi-tenant isolation"),
    code(
        "POST /v1/chat/completions    -- inference\n"
        "POST /v1/embeddings         -- embeddings\n"
        "GET  /v1/models             -- available models\n"
        "GET  /v1/pods               -- active compute pods (internal)\n"
        "POST /v1/jobs               -- batch job submission"
    ),
])
print(f"  OK: {aurl}")

print()
print("Pod Swarm Engineering Suite fully populated.")
print(f"  NVL72 Rack Config:   {rurl}")
print(f"  CDU Cooling:         {curl}")
print(f"  PDU Layouts:         {purl}")
print(f"  Network Topology:    {nurl}")
print(f"  RunPod Integration:  {aurl}")
