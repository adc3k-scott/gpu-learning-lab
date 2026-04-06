# 🏗️ ADC 3K — Project Command Center
*Notion backup — 2026-04-06*

| Gate | Description | Target | Status |
| P-1 | Provisional patent filed | Week 6 | 🟡 Disclosure ready — needs counsel |
| N-1 | NVIDIA Inception accepted | Week 6 | 🟡 Application package ready — SUBMIT NOW |
| C-1 | Cooling vendor RFI responses received | Week 8 | 🟡 Cover emails ready — SEND NOW |
| H-1 | Lab hardware ordered (D1 decision) | Week 3 | 🔴 BOM ready — no PO issued |
| L-1 | Site LOI executed | Week 12 | 🔴 Site package ready — no conversations started |
| S-1 | Pilot customer LOI signed | Week 12 | 🔴 LOI template ready — no conversations started |
---
> TWO-PRODUCT MODEL — READ FIRST

ADC has two distinct products. Do not conflate them.

MARLIE I = Permanent AI Factory building at 1201 SE Evangeline Thruway, Lafayette LA. CDU liquid cooling, NVL72 racks, Bloom Energy + LUS grid power. This is the HQ, NOC, and primary compute facility.

ADC 3K = Manufactured containerized AI compute pod. 40-ft ISO container. Immersion cooling (Engineered Fluids EC-110). Deployed to remote sites. No HVAC required. Networked back to MARLIE I. This is the PRODUCT that MARLIE I manufactures and deploys.

All engineering in this Command Center labeled 'MARLIE I scope' refers to the building. ADC 3K pods have their own separate cooling, power, and deployment spec.
> ADC 3K POD — ALL CONTENT
Live pages:  adc3k.com/adc3k-pod  +  adc3k.com/adc3k-pod-spec
Manufacturing strategy:  ADC Manufacturing -- Pod Factory Strategy
GTM / sales angle:  The ADC 3K Pod — Your Edge AI Node
Engineering specs:  Pod Swarm Engineering Suite
---
---
## 🚀 Monday Morning Priority List
1. Submit NVIDIA Inception — ADC3K_NVIDIA_Inception_Application_Package_Rev1.docx · Portal: nvidia.com/en-us/startups · 15 minutes
1. Send cooling vendor RFIs — ADC3K_Cooling_Vendor_RFI_Outreach_Pack_Rev1.docx · Attach ADC-3K-Cooling-Vendor-RFI.html to all 4 emails
1. Deliver patent disclosure to counsel — ADC3K_Patent_Disclosure_Rev1.docx · Attorney-Client Privileged · Target provisional filing Q2 2026
1. Send pitch deck to 2 investors — ADC3K_Investor_Pitch_Deck_Rev1.pptx + ADC3K_Financial_Model_Rev1.xlsx · Use ADC3K_Investor_Outreach_Email_Pack_Rev1.docx for targeting
1. Start site conversations — ADC3K_Phase1_Site_Assessment_Package_Rev1.docx · Call Port of Iberia + LEDA + one industrial park contact
1. File ITEP application BEFORE any construction — ADC3K_Louisiana_Incentive_Stack_Brief_Rev1.docx §3 · opportunitylouisiana.gov · Do this at site LOI execution
---
## ⚠️ Critical Flags for Next Session
- Financial model needs update: Louisiana corporate tax rate is now 5.5% (not ~25% blended). IRR is higher than currently modeled — update Assumptions tab before next investor meeting
- HB 827 threshold: ADC Phase 1 alone (~$19–30M) is below the $200M eligibility threshold. Pursue parish-level PILOT agreement as alternative. Brief investors honestly.
- ITEP timing: Must file BEFORE breaking ground. Non-negotiable. Tie to site LOI execution.
- NVIDIA Inception eligibility: ADC Inc. founded 2003 — frame ADC-3K as the AI infrastructure division launched 2025/2026 to satisfy the <10-year rule.
---
## 🌐 Website Build (V3 — March 1, 2026)
File: ADC-3K-Master-Website-V3.html (~728 KB, single-file SPA)
Status: Production-ready, 10-page site with embedded images
Branding: ADC-3K POD (global rename complete)
Contact: (337) 780-1535 / scott@adc3k.com / Data Center Design Professional
Full build log, edit history, and source image inventory:
*[Child: Master Task Tracker]*
*[Child: Pod Swarm Engineering Suite]*
> MARLIE I engineering specs — NVL72 racks, CDU liquid cooling, PDU layouts, network topology, RunPod API. All docs apply to the permanent building at 1201 SE Evangeline. ADC 3K pods use immersion cooling — separate spec required.
---
## Contents
  - NVL72 rack configurations and cable plans
  - CDU liquid cooling schematics
  - Power distribution unit layouts
  - Network topology diagrams
  - RunPod API integration notes
*[Child: NVL72 Rack Configuration & Cable Plans]*
> NVIDIA Vera Rubin NVL72 — 72 Rubin GPUs + 36 Vera CPUs per rack. 3.6 ExaFLOPS NVFP4. 100% liquid cooled. Full production H2 2026.
---
## Phase 1 Layout — 22 x 35 ft Floor (770 sq ft)
    - Total racks: 16 NVL72 units
    - Arrangement: Row A (8 racks) + Row B (8 racks) — hot aisle contained between rows
    - Walk-through: Cold aisle access front and rear — sealed hot aisle center
    - Aggregate compute: 57.6 ExaFLOPS NVFP4
    - Aggregate memory BW: 260 TB/s
---
## Per-Rack Specs (NVL72)
    - GPUs: 72x Rubin GPU — 36 per NVLink domain, 2 domains per rack
    - CPUs: 36x Vera CPU — 88 Olympus Arm cores (Armv9.2) each, 1.5 TB LPDDR5X, 1.2 TB/s memory BW per CPU
    - NVLink 6 Switches: 9x switch trays per rack — 28.8 TB/s per tray, 260 TB/s aggregate, in-network SHARP FP8 compute
    - Memory: HBM4 — 288 GB per Rubin GPU, 20.7 TB total per NVL72 rack, 1.58 PB/s aggregate bandwidth
    - Power per rack: TDP not yet published by NVIDIA — contact NVIDIA Enterprise Sales for facility planning specs
    - Cooling: Rear-door CDU manifold — 100% liquid, no air cooling
---
## Cable Plans
### NVLink Fabric (Intra-rack)
    - Topology: NVLink 6 Switch — full mesh within rack via 9-switch rail
    - Cable type: NVIDIA NVLink optical cables — pre-routed at factory
    - Field cabling required: None for NVLink intra-rack
---
### InfiniBand NDR (Inter-rack)
    - NIC: ConnectX-9 SuperNIC — 1.6 Tb/s per adapter (800 Gb/s per port) — >144 adapters per NVL72
    - Fabric: NDR400 InfiniBand — 400 Gb/s per port
    - Switch: NVIDIA Quantum-3 InfiniBand — top-of-rack or end-of-row
    - Cable type: NVIDIA Quantum HDR/NDR DAC or optical — 2m intra-row, 5m cross-row
    - Total uplinks: 16 racks x 2 ports = 32 uplinks to spine
---
### Ethernet Management (BlueField-4 DPU)
    - DPU: BlueField-4 — 1x per NVL72 — OOB management + storage offload
    - Uplink: 10GbE management — 1 cable per rack to management switch
    - Switch: Dedicated 24-port 10GbE management switch in network core
---
## Rack Numbering Convention
```plain text
Row A: A01 A02 A03 A04 A05 A06 A07 A08  (cold aisle front)
              [sealed hot aisle]
Row B: B01 B02 B03 B04 B05 B06 B07 B08  (cold aisle rear)

Network Core: NC01 (north end, near entry)
CDU Manifold: Runs along exterior north wall
```
---
## NVIDIA Field Resources
    - DGX-Ready colocation checklist: developer.nvidia.com/dgx-ready-data-center
    - NVL72 power + cooling specs: Contact NVIDIA Enterprise Sales
    - Field installation: NVIDIA-certified solution architect required
> SCOPE: This document applies to MARLIE I — the permanent AI Factory at 1201 SE Evangeline Thruway. NOT applicable to ADC 3K container pods, which use immersion cooling and a separate architecture.
---
> UPDATED 2026-03-23 -- POST-GTC REWRITE
## NVL72 Rack -- Vera Rubin Platform (December 2026 availability via HPE)
### Per Rack:
    - 72 NVIDIA Rubin GPUs
    - 36 NVIDIA Vera CPUs
    - 9 NVLink 6 switches (6th generation)
    - ConnectX-9 SuperNIC (1.6 Tb/s)
    - BlueField-4 DPUs
    - HBM4: 288 GB per GPU
    - Power: 130 kW per rack
    - Cooling: Direct-to-chip liquid, 45C hot water
    - Power input: 800V DC (Eaton Beam Rubin DSX)
    - Internal conversion: 64:1 LLC (800V -> 12V, 98% efficient, built-in)
### Rack Counts by Site:
Willow Glen: Phase 1 = 10 racks (8 VR + 2 Groq), Max = 2,000+, IT Power = 260 MW
MARLIE I: Phase 1 = 8 racks (4 per floor), Max = 8, IT Power = 1.04 MW
Trappeys: Phase 1 = 4 racks, Max = 225, IT Power = 29 MW
ADC 3K Pod: 1-2 per container, Max = 2, IT Power = 130-260 kW
### Cable Plan (per rack):
    - NVLink 6: Factory-integrated (intra-rack, do not touch)
    - InfiniBand: Quantum-X800 switches, 800 Gb/s per port
    - Ethernet: Spectrum-X, BlueField-4 DPU per node
    - Management: 10GbE OOB to NOC
    - Power: Single 800V DC feed from Eaton bus
### Multi-Vendor Future:
    - Primary: NVIDIA Vera Rubin NVL72
    - Future: Tesla Terafab chips (when available)
    - Future: AMD Instinct (if competitive)
Pod architecture is chip-agnostic at the facility level -- 800V DC and liquid cooling work for any vendor.
---
> WARNING (2026-03-24): Pre-GTC content above says 16 racks and InfiniBand NDR/Quantum-3. CORRECT specs are in the POST-GTC section: 8 racks per floor at MARLIE I, Quantum-X800 (800 Gb/s), 130 kW per rack.
*[Child: CDU Liquid Cooling Schematics]*
> UPDATED 2026-03-23 -- POST-GTC REWRITE
## Cooling Architecture -- Post-GTC 2026
NVIDIA now ships complete liquid-cooled NVL72 racks. 45C hot water direct-to-chip. ADC does NOT engineer custom immersion cooling. EC-110 dielectric immersion is DEPRIORITIZED.
### What ADC Builds (cooling):
    - Facility water loop (supply/return piping)
    - Exterior heat rejection (dry coolers or river cooling depending on site)
    - CDU connections to NVIDIA rack manifolds
### Per-Site Cooling:
Willow Glen: Mississippi River (once-through, unlimited) -- 260 MW ceiling
MARLIE I: Dry coolers on concrete pad -- 1.2 MW
Trappeys: Water tower + dry coolers -- 29 MW max
ADC 3K Pod: Integrated dry cooler per container -- 130-260 kW per pod
### ADC 3K Pod Cooling:
    - 40-ft container with 1-2 NVL72 racks
    - Integrated dry cooler mounted on container exterior
    - 45C supply / 55-60C return glycol loop
    - Self-contained -- no external water infrastructure needed
    - Designed for field deployment (oil fields, remote sites)
### Temperature Specs:
    - GPU junction: <83C
    - Coolant supply: 45C
    - Coolant return: 55-60C
    - Ambient operating range: -20C to 50C (dry cooler rated)
---
*[Child: Power Distribution Unit Layouts]*
> UPDATED 2026-03-23 -- POST-GTC REWRITE
## Power Architecture -- 800V DC Native (ALL Sites)
### 4-Layer Power Hierarchy (LOCKED):
Layer 1: Solar (First Solar TR1) -- Primary offset
Layer 2: Natural Gas (Henry Hub) -- Backbone 24/7
Layer 3: Diesel Gensets -- Emergency backup
Layer 4: Grid -- SELL-BACK ONLY (Willow Glen: Entergy, Lafayette: LUS)
> Grid is NEVER for consumption. Gas is ALWAYS running. Bloom Energy is NOT in the power stack. REMOVED post-GTC.
### Power Chain:
Gas/Solar -> Generator/Panels -> Eaton Beam Rubin DSX Rectifier (AC->800V DC) -> 800V DC Bus -> Eaton Busway -> Rack PDU (Eaton HDX G4) -> 64:1 LLC Converter (built into NVIDIA rack) -> 12V DC -> GPU
### Per-Site Power:
Willow Glen: 2x Cat CG260-16 (2.8 MW, H2-ready), 400+ acres ground mount solar, Sell-back to Entergy, Phase 1 IT = 1.3 MW (10 racks)
MARLIE I: 2x Cat G3520C (1.5 MW), 300 kW rooftop + ground solar, LUS backup, Phase 1 IT = 1.04 MW (8 racks)
Trappeys: 2x Cat G3520C (1.5 MW), 2.05 MW rooftop (3,731 panels), LUS sell-back, Phase 1 IT = 520 kW (4 racks)
ADC 3K Pod: 1x portable genset (250-500 kW), Optional roof panels, Optional grid tie, Phase 1 IT = 130-260 kW (1-2 racks)
### ADC 3K Pod Power:
    - Self-contained 800V DC system in 40-ft container
    - Portable natural gas generator (field gas available at oil field sites)
    - Eaton Beam Rubin DSX rectifier (containerized)
    - Optional solar panels on container roof
    - Optional grid tie for urban deployments
    - 4-layer hierarchy applies to EVERY deployment
---
*[Child: Network Topology Diagrams]*
> UPDATED 2026-03-23 -- POST-GTC REWRITE
## Network Architecture -- Hub and Spoke
### Fabric 1: NVLink 6 (Intra-Rack)
    - 6th generation NVLink
    - 260 TB/s aggregate bandwidth per rack
    - Factory-integrated -- DO NOT modify
### Fabric 2: InfiniBand (Inter-Rack, Intra-Site)
    - NVIDIA Quantum-X800 switches
    - 144 ports x 800 Gb/s per switch
    - Willow Glen: Full fat-tree topology (PRIMARY compute fabric)
    - MARLIE I: Single spine switch (8 racks)
    - ADC 3K Pod: No InfiniBand (single rack = NVLink only)
### Fabric 3: Ethernet (Services + WAN)
    - NVIDIA Spectrum-X (Spectrum-6 switches)
    - BlueField-4 DPU per node
    - Site-to-site: Dedicated fiber (Willow Glen <-> MARLIE I, 60 mi)
    - Remote pods: Starlink or cellular backhaul
    - LUS Fiber: 100GbE municipal fiber for MARLIE I/Trappeys (0.8 mi)
### Fabric 4: Management (OOB)
    - 10GbE out-of-band management
    - WireGuard/Tailscale mesh VPN across all sites
    - Mission Control dashboard at Willow Glen NOC
    - Backup NOC at MARLIE I
### Fleet Orchestration:
    - NVIDIA Run:AI for workload scheduling across all nodes
    - NVIDIA Dynamo 1.0 for inference optimization (7x performance)
    - Mission Control AI (ADC-built) for autonomous operations
    - NVIDIA Base Command Manager for cluster management
### Hub-Spoke Connectivity:
Willow Glen <-> MARLIE I: Dedicated fiber, 100 Gbps (Management only, NOT InfiniBand)
Willow Glen <-> Trappeys: Dedicated fiber, 100 Gbps (Via Lafayette fiber)
Willow Glen <-> Remote Pods: Starlink/VSAT, 100-500 Mbps (Inference results only)
MARLIE I <-> Trappeys: LUS Fiber, 10 Gbps (0.5 mi)
---
*[Child: RunPod API Integration Notes]*
> Mission Control manages RunPod cloud GPU pods via GraphQL API. IntegrationAgent dispatches via runpod skill. When MARLIE I goes live, on-prem racks replace RunPod cloud as primary.
---
## Current Setup — RunPod Cloud
    - Endpoint: https://api.runpod.io/graphql
    - Auth: Bearer token — RUNPOD_API_KEY in .venv/.env
    - Skill: skills/builtin/runpod.py — list / start / stop / terminate
    - Planner patterns: list pods | pod status | start pod | stop pod | terminate pod
---
## GraphQL Operations
### List Pods
```graphql
query {
  myself {
    pods {
      id name status
      runtime { uptimeInSeconds gpus { id gpuUtilPercent } }
      machine { gpuDisplayName }
    }
  }
}
```
### Start Pod
```graphql
mutation {
  podResume(input: { podId: "POD_ID", gpuCount: 1 }) {
    id status
  }
}
```
### Stop Pod
```graphql
mutation {
  podStop(input: { podId: "POD_ID" }) {
    id status
  }
}
```
---
## Mission Control Flow
    - Chat trigger: "list pods" / "start pod XYZ" / "stop pod XYZ"
    - Planner: Regex fast-path -> IntegrationAgent -> runpod skill
    - SSE stream: /tasks/{id}/stream — live step events during pod ops
    - Dashboard: Mission Control HQ at http://localhost:8000
---
## MARLIE I Transition Plan (H2 2026)
> When NVL72 racks go live, on-prem becomes primary. RunPod cloud is overflow. Mission Control routes by cost/latency/availability.
    - Phase 1 (now): RunPod cloud — dev/test workloads
    - Phase 2 (H2 2026): MARLIE I on-prem — production inference + training
    - Phase 3: Hybrid routing — Mission Control schedules across on-prem + cloud
---
## On-Prem API Design (Future)
    - Protocol: OpenAI-compatible REST — drop-in for cloud providers
    - Auth: API key per customer — managed by Mission Control
    - Billing: Per-GPU-hour metering via PDU current sensors
    - Scheduler: OrchestratorAgent — job queue, priority, multi-tenant isolation
```plain text
POST /v1/chat/completions    -- inference
POST /v1/embeddings         -- embeddings
GET  /v1/models             -- available models
GET  /v1/pods               -- active compute pods (internal)
POST /v1/jobs               -- batch job submission
```
---
> UPDATED 2026-03-23 -- POST-GTC REWRITE
RunPod remains the cloud GPU provider for Phase 0 (pre-facility). The existing GraphQL integration and Mission Control planner patterns are still valid.
### Current Status:
    - RunPod balance: ~$184
    - Network volume: aido-workspace (250GB, US-TX-3)
    - Active pod: ml4cl3icn37ys1 (L40S, EXITED)
    - Image gen endpoints: FLUX Schnell + Kontext (live on RunPod Hub)
### Transition Plan (unchanged):
    - Phase 0: RunPod cloud (NOW)
    - Phase 1: On-prem at MARLIE I (H2 2026 when Vera Rubin ships Dec 2026)
    - Phase 2: Hybrid (Willow Glen primary + RunPod overflow)
    - Phase 3: Full on-prem fleet (Willow Glen + MARLIE I + pods)
### Fleet Management Stack:
    - NVIDIA Run:AI -- workload orchestration across all on-prem nodes
    - NVIDIA Dynamo 1.0 -- inference optimization (7x performance boost)
    - NVIDIA Base Command Manager -- cluster lifecycle management
    - Mission Control AI (ADC-built) -- autonomous operations, monitoring, SSE dashboard
    - NVIDIA Mission Control (HPE offering) -- available 2026, evaluate for integration
*[Child: Pod Swarm Architecture — Document Index]*
*[Child: 🎯 Pod Swarm — Next Session Command Prompt]*
> ADC 3K session startup prompt. Copy/paste at the start of any new Claude session on ADC 3K pod engineering or deployment.
## COPY FROM HERE
You are the lead infrastructure engineer for ADC 3K — Advantage Design Construction containerized AI compute pod product line. Owner: Scott Tomsu, Lafayette, Louisiana.
### ADC 3K Product
      - 40-ft High Cube ISO container — manufactured AI compute pod, deployed to remote sites
      - Cooling: Direct-to-chip liquid cooling (NVIDIA reference). External dry cooler. No immersion, no HVAC. PUE target: 1.03
      - Power: 800V DC native. Bloom SOFC primary. Dual Bloom + CNG backup per site. No diesel — network redundancy via distributed sites.
      - Networked back to MARLIE I HQ at 1201 SE Evangeline Thruway
### First Deployment — Trappeys Cannery
      - Metal warehouse structure. Pods drop into bays, no structural modifications needed.
      - Status: Planning. No hardware ordered, no LOI signed.
### GPU Platform
      - NVIDIA Vera Rubin NVL72 — H2 2026. TDP NOT confirmed — all sizing from analyst estimates.
      - Blackwell/GB200/GB300 RETIRED. Do not reference.
### Open Investor Items (5 open)
      - 1. Customer LOI  2. NVIDIA TDP confirmation  3. HB 827 PILOT  4. CapEx reconciliation  5. Tax rate fix (5.5% not 25%)
### Notion
      - Command Center: 31488f09-7e31-816d-9fdc-c6aabba4e3fa
      - Master Task Tracker: 41 P0/P1/P2 tasks from container order to GO-LIVE
---
> UPDATED 2026-03-23 -- POST-GTC REWRITE
## ADC 3K Pod -- Current Spec (Post-GTC 2026)
### Hardware:
      - 40-ft High Cube ISO container (NOT 20-ft)
      - 10 NVIDIA Vera Rubin NVL72 racks (8 compute + 1 network + 1 storage) — C1 SuperPOD, 576 GPUs, 1.3 MW IT load
      - Eaton Beam Rubin DSX (800V DC rectifier + bus + PDUs)
      - Integrated dry cooler (exterior mount)
      - Portable natural gas generator OR site power tie-in
      - Optional: First Solar rooftop panels, LFP battery
### Software:
      - NVIDIA Dynamo 1.0 (inference OS)
      - NVIDIA Run:AI (fleet orchestration)
      - NVIDIA Base Command Manager (cluster management)
      - Mission Control AI (ADC autonomous ops)
      - NemoClaw (secure agent sandbox -- waiting for 403 bug fix)
### Power: 800V DC Native
      - Power hierarchy: Solar/First Solar 1500V DC -> Bloom SOFC 800V DC (primary) -> LFP BESS (bridge/ATS) -> Grid (sell-back only). No diesel — network redundancy via distributed sites.
      - Eaton Beam Rubin DSX throughout
      - Henry Hub natural gas pricing
### Deployment Targets:
      1. Oil fields (natural gas on-site)
      1. University campuses
      1. Municipal/emergency response
      1. 6G/AI-RAN base stations
      1. Remote/offshore (Starlink backhaul)
### Network Home:
      - All pods connect back to Willow Glen (PRIMARY NOC) via fiber or Starlink
      - MARLIE I = backup NOC (60 mi from Willow Glen)
      - Mission Control dashboard shows all nodes live
### Multi-Vendor:
      - NVIDIA Vera Rubin = primary (Dec 2026)
      - Tesla Terafab = future option (monitor availability)
      - AMD Instinct = future option
Container architecture is chip-agnostic -- 800V DC + liquid cooling works for any vendor.
### Open Items:
      1. NemoClaw 403 bug fix (NVIDIA GitHub Issues #314, #336)
      1. Container vendor selection (40-ft HC ISO)
      1. Portable genset spec for field deployment
      1. Starlink business account for remote pods
      1. Run:AI licensing and setup
      1. First Solar panel mounting spec for container roof
---
---
## Session Closeout — 2026-04-03
Notion fixes already pushed this session (do not redo): cooling corrected to direct-to-chip liquid throughout; rack count corrected to 10 NVL72 racks (C1 SuperPOD, 576 GPUs, 1.3 MW IT); email corrected to scott@adc3k.com; Bloom SOFC confirmed as PRIMARY; First Solar 1500V DC layer + grid sell-back only; deleted NPN 5-min form block, DANGER callout, duplicate cooling bullets, March 8 Bloom demotion.
### 10 MW Canonical Site Layout — LOCKED
      - 4 pods x 10 NVL72 racks per pad = one 10 MW site (40 racks, 2,880 GPUs)
      - Dual Bloom A + Bloom B — N+1 at generation level. Either covers full load solo.
      - One Atmos gas tap, manifold splits to both Bloom units
      - BESS vendor slot OPEN — do not lock supplier. Architecture = DC-coupled containerized BESS.
      - First Solar panels on pod rooftops. 1500V DC forward design. Operating at 800V today.
      - Two utility connections only per site: Atmos gas tap + LUS fiber drop. No grid. No water.
### Two-Bus Architecture — LOCKED
      - Bus 1 — COMPUTE (sacred): AI racks, liquid cooling, Mission Control. Hitachi AMPS + BESS. Zero interruptions. Nothing else on this bus.
      - Bus 2 — AUXILIARY (separate): site lighting, LED screen, EV/e-bike/scooter/phone/laptop DC charging, drone dock, security cameras. Separate smaller BESS.
      - Split happens after Bloom output. A fault on Bus 2 NEVER touches Bus 1. Both buses can be fed by either Bloom unit.
### Public-Facing Auxiliary Layer — LOCKED
      - LED screen on container exterior — advertising revenue + AI education content at night
      - DC charging hub: CCS fast charge EVs, e-bikes, scooters, phones, laptops. All DC-native — no AC conversion loss.
      - Scooter/bike docking — Lime, Bird, VeoRide partnership angle. Drop off, charge, pick up.
      - Site lighting: ADC owns its perimeter. Full LED flood + pathway. No city lighting dependence.
      - Drone security dock at every site. Autonomous patrol tied to Mission Control / SkyCommand. Mini KLFT node.
### City Neural Network Concept — INTERNAL ONLY
      - Lafayette pod network physically resembles a neural network. Each pod cluster = node, LUS fiber = axons, Bloom = synapse fuel.
      - Framing: We are not building a data center. We are building a brain for the city.
      - Map visualization: Lafayette street map, nodes lit at each site, edges showing fiber. MUST BUILD before investor meetings. NOT on website yet.
      - Scale target: 300-500 MW city-wide distributed. Do NOT publish a number. Frame as city-scale only.
      - Inference runs at nearest edge node. Training routes to Trappeys/Willow Glen. Network self-balances.
### Deployment Zones — Inner-City Infrastructure Corridors
      - Target: areas that cannot be traditionally developed (by water, gas infra, old neighborhoods) — already have Atmos gas + LUS fiber.
      - Only two utility connections needed: Atmos commercial gas tap + LUS fiber drop. No grid. No city plumbing. No building permits for occupied structures.
### OPEN ITEMS — Must Resolve Before Renders
      - OPEN: Cooling aesthetics — dry cooler is industrial-looking. Options: (1) louvered screen enclosure, (2) roof-mount low-profile, (3) visible design feature. Pick one. Must share design language with pod + LED screen + charging canopy + drone dock.
      - OPEN: Pad top-down site drawing — concrete pad, fenced perimeter, setback, Bloom A/B, BESS, AMPS PCS, 4 pods, cooler, charging canopy, drone dock. Lock this before renders.
### Next Actions
      1. Lock cooling aesthetics decision (choose one option)
      1. Produce pad top-down site drawing (concrete, perimeter, all equipment positions)
      1. Once pad is locked, begin renders — single design language, reusable across all sites
      1. Build city neural network map visualization (internal, before investor meetings)
New memory files: memory/projects/adc3k_city_network.md | memory/projects/adc3k_site_design.md | adc3k_pod_power_architecture.md updated with two-bus section at top.
---
> ARCHIVED (2026-03-24): This page is empty and vestigial. No content. Use the Pod Swarm Engineering Suite parent page instead.
---
> UPDATED 2026-03-23 -- POST-GTC REWRITE. All pre-GTC references to EC-110 immersion, Bloom Energy, 20-ft containers, and LUS-as-primary are SUPERSEDED by content below.
## ADC 3K Pod -- Post-GTC 2026 Architecture
The ADC 3K Pod is a 40-ft ISO container housing NVIDIA liquid-cooled racks (NOT immersion). DSX-compliant. 800V DC native power via Eaton Beam Rubin DSX. Self-powered on natural gas + solar. Managed remotely from Willow Glen (primary NOC) or MARLIE I (backup NOC).
### Key Changes Post-GTC:
  - 40-ft containers (NOT 20-ft -- too small for NVL72 racks)
  - NVIDIA ships complete liquid-cooled racks -- no custom immersion engineering needed
  - EC-110 immersion DEPRIORITIZED for main deployments
  - 800V DC native power distribution (Eaton Beam Rubin DSX)
  - 4-Layer Power Hierarchy: Solar -> Natural Gas -> Diesel -> Grid (sell-back only)
  - Bloom Energy SOFC = PRIMARY power source (800V DC direct, 3 units in series, ~750 kW/cell, no inverter needed)
  - Willow Glen = PRIMARY HUB, MARLIE I = backup NOC + edge
  - Multi-vendor chip ready (NVIDIA primary, Terafab/AMD future-proofed)
  - NVIDIA Run:AI for fleet orchestration across all pods
  - 6G/AI-RAN deployment capability via Nokia partnership
### Hub-and-Spoke Architecture:
  - HUB: Willow Glen Terminal (700 acres, 500kV/230kV, Mississippi River)
  - SPOKE 1: MARLIE I (Lafayette, backup NOC, 8 NVL72 racks)
  - SPOKE 2: Trappeys Cannery (Lafayette, UL Lafayette, 4 buildings)
  - SPOKE 3+: ADC 3K Pods (oil fields, remote sites, edge deployments)
  - All spokes connect back to Willow Glen via fiber (terrestrial) or Starlink (remote)
  - Mission Control AI manages all nodes from single dashboard
### Deployment Use Cases:
  1. Oil field edge compute (natural gas on-site, zero grid dependency)
  1. University research nodes (campus deployments)
  1. Municipal AI services (smart city, emergency response)
  1. 6G/AI-RAN base stations (NVIDIA + Nokia)
  1. Remote/offshore inference (Starlink backhaul)
  1. Disaster response mobile compute
---
> IMPORTANT (2026-03-24): This page has been audited. The ONLY current content is in the "POST-GTC REWRITE" section below. Everything ABOVE that section is pre-GTC (March 2026) and contains wrong specs: EC-110 immersion (deprioritized), Bloom Energy (removed), 480V AC (now 800V DC), MARLIE I as primary NOC (now Willow Glen). DO NOT use pre-GTC content for any purpose.
*[Child: Session Prompts & Claude Context]*
> Saved Claude session prompts and AI context documents for ADC 3K mission continuity. Contains the master session startup prompt and engineering package backup.
---
## Contents
  - ADC 3K master session startup prompt (copy/paste to begin any new session)
  - March 4, 2026 engineering package backup and document inventory
*[Child: March 4 2026 — Engineering Package Backup & Status]*
> Engineering package produced Feb 28 - Mar 4, 2026. Complete ADC 3K document set as of that date.
## Document Inventory (March 4, 2026)
### Engineering
    1. ADC-3K-Engineering-Lock-Package.docx — thermal model, CFD, 107 sensors, derate playbook (~99 pages)
    1. ADC-3K-Hard-Confirmation-Pack-RFI.docx — 80+ vendor questions, 5 sections
    1. ADC-3K-Single-Line-Diagram.html — interactive power distribution, PUE 1.083
    1. ADC-3K-Liquid-Loop-PID.html — dual-loop piping, valves, 64 sensors
    1. ADC-3K-Floor-Plan.html — plan view, cross section, dimensions + weight
    1. ADC-3K-Closed-Loop-Air-Strategy-v1.1a.docx — Section 6 insert
### Financial
    1. ADC-3K-Financial-Model.xlsx — 5-tab, 180 formulas, $33.2M CapEx, $9.4M EBITDA Y3 (NOTE: tax rate error, use 5.5% not 25%)
    1. ADC-3K-Investor-Pitch-Deck.pptx — 9-slide deck
    1. ADC-3K-Vendor-Parts-List.xlsx — 59 line items, $29.5M BOM, lead times
    1. ADC-3K-Session-Handoff-Final.md — full inventory and cross-reference map
### Outreach
    1. ADC3K_NVIDIA_Inception_Application_Package_Rev1.docx — ready to submit
    1. ADC3K_Cooling_Vendor_RFI_Outreach_Pack_Rev1.docx — 4 emails ready to send
    1. ADC3K_Patent_Disclosure_Rev1.docx — deliver to counsel, Q2 2026 provisional
    1. ADC3K_Investor_Pitch_Deck_Rev1.pptx + ADC3K_Financial_Model_Rev1.xlsx
### Website
    1. ADC-3K-Master-Website-V3.html — 728 KB SPA, 10 pages, production-ready
> ARCHITECTURE NOTE (March 8, 2026): ADC 3K cooling changed from CDU to immersion. These docs reflect older spec. Review before sending to vendors or investors.
*[Child: ADC 3K — Master Session Prompt]*
Last Updated: February 28, 2026 — Original engineering brief. Updated architecture below (March 8, 2026).
Use this prompt to start any new Claude session working on ADC project documents.
Copy everything below the line and paste it as your first message.
## START COPYING HERE
You are the lead infrastructure architect, financial strategist, and technical writer for Advantage Design Construction Inc.'s ADC 3K program.
## PROJECT CONTEXT
ADC (Advantage Design Construction Inc.) is a Louisiana-licensed general contractor (est. 2003) based in Lafayette, LA. Owner: Scott. ADC is developing the ADC 3K — a 3 Megawatt-class liquid-cooled AI compute pod built inside a standard 40-ft High Cube ISO container. 1,008 NVIDIA Rubin GPUs across 14 NVL72 racks (72 GPUs/rack). Direct-to-chip liquid cooling via 3x Vertiv XDU450 CDUs (N+1 redundant).
The project has evolved from: site-specific Trappey's concept → 20-ft 800 kW (V1-V4) → 40-ft 2,400 kW Model 2400X (V5) → ADC 3K (refined engineering, confirmed thermal model, complete documentation package).
## COMPLETE ADC 3K DOCUMENT SET
All produced February 28, 2026:
    1. ADC-3K-Engineering-Lock-Package.docx — Thermal model, CFD plan, 107 sensors, controls, derate playbook (~99 pages)
    1. ADC-3K-Hard-Confirmation-Pack-RFI.docx — 80+ vendor questions, 5 sections, email template
    1. ADC-3K-Single-Line-Diagram.html — Interactive: power distribution, breaker schedule, PUE 1.083
    1. ADC-3K-Liquid-Loop-PID.html — Interactive: dual-loop piping, valves, 64 liquid-loop sensors
    1. ADC-3K-Financial-Model.xlsx — 5-tab, 180 formulas: $33.2M CapEx, $9.4M EBITDA Y3
    1. ADC-3K-Investor-Pitch-Deck.pptx — 9-slide deck with charts and financial summary
    1. ADC-3K-Floor-Plan.html — Interactive: plan view, cross section, dimensions + weight
    1. ADC-3K-Vendor-Parts-List.xlsx — 59 line items, $29.5M BOM, lead times, vendor contacts
    1. ADC-3K-Session-Handoff-Final.md — Complete inventory, priorities, cross-reference map
    1. ADC-3K-Closed-Loop-Air-Strategy-v1.1a.docx — Section 6 insert: closed-loop air environment, capacity-based DOAS gating, dew point margin framework, Protect Mode, commissioning protocol, 29+ air-side sensors, 22 RFIs (AIR-01–A22)
## THREE CRITICAL ENGINEERING FLAGS
    1. CDU Capacity Short at 4°C ATD: 1,359 kW < 1,680 kW. Must operate ≥5.4°C ATD. Target 6–7°C.
    1. Flow Rate (GATING): At 10 deg C dT = 636 GPM (FAIL). At 20 deg C dT = 318 GPM (OK). MUST confirm Vera Rubin GPU dT >= 20 deg C (RFI S-01) — contact NVIDIA Enterprise for thermal spec.
    1. Busway Fit: 4,000A Starline T5 must fit 18" ceiling space. Derating at 45–55°C ambient (RFI B-01, B-02).
## TECHNICAL SPECS — ADC 3K
    - Container: 40-ft High Cube ISO, 93" internal width (TIGHT), 106" internal height
    - GPU: 1,008x NVIDIA Rubin GPU in 14x NVL72 racks (72 GPUs/rack)
    - IT Load: 2,100 kW peak (150 kW/rack), 1,848 kW typical (132 kW/rack)
    - PUE: 1.083 → 2,274 kW total facility load
    - Cooling: 3× Vertiv XDU450 CDU, manifolded N+1. 30% PG / 70% DI water. 318 GPM @ 20°C ΔT server-side. 1,680 kW liquid (80%), 420 kW air (20%).
    - Electrical: 480V / 4,000A Starline T5 busway. 14 tap-off boxes (250AF/200AT each). Active Power CLEANSOURCE flywheel UPS (external).
    - Controls: 107 sensors (48 temp, 4 flow, 6 pressure/ΔP, 1 RH, 4 leak, 3 vibration, 16 ambient, 14 rack power, 11 misc). 10-state MPC controller. Safety PLC with <100ms hardwired shutdown.
    - Container Zones: A (Power/2.5 ft), B (Cooling/3.5 ft), C (Compute/28 ft), D (Controls/3 ft), E (Access/2.4 ft)
    - Weight: ~60,000 lb estimated. Floor loading ~194 PSF.
    - Cost: $33.2M CapEx per pod ($25M GPU + $8.2M infrastructure)
    - Revenue: $11.6M/yr at 92% utilization (Year 3). EBITDA margin 80.8%. Payback ~3.5 years.
## VENDOR RFI STATUS (as of Feb 28, 2026)
All RFIs written and ready to send:
    - Supermicro/NVIDIA: 24 questions (S-01 through S-24). S-01 (ΔT) is GATING.
    - Vertiv: 21 questions (V-01 through V-21). V-01 (ATD curve) is CRITICAL.
    - Starline: 14 questions (B-01 through B-14). B-01 (profile dims) is CRITICAL.
    - Heat Rejection: 3 options with questions (dry cooler, wet tower, river HX).
    - Controls/BMS/PLC: 15 questions (C-01 through C-15).
## FINANCIAL MODEL KEY NUMBERS
    - CapEx: $33.2M (75% GPU, 8% racks, 6% cooling/power/container, 10% integration/engineering, 1% contingency)
    - Revenue (Y3): $11.6M (GPUaaS: $1.75/hr reserved, $2.50/hr spot, 70/30 mix, 92% utilization)
    - OpEx (Y3): $2.2M (power $982K, maintenance $1.0M, network $127K, staff $64K)
    - EBITDA (Y3): $9.4M (80.8% margin)
    - 5-Year Cum FCF: $39.4M
    - 10-pod deployment: $292M adjusted CapEx (12% volume discount), ~28% IRR
## TONE
Institutional, credible, engineering-first. Professional language suitable for PE-stamped documents, bank loan packages, and investor presentations. Not hype.
## INSTRUCTIONS FOR THIS SESSION
[EDIT THIS SECTION EACH SESSION — tell Claude what to work on]
Examples:
    - "Finalize thermal model with Supermicro's confirmed ΔT value"
    - "Update CDU operating point after Vertiv provides ATD curve"
    - "Create arc flash study after LUS provides fault current"
    - "Build container mechanical detail drawings (penetrations, structural)"
    - "Update financial model with actual vendor quotes"
## END COPYING HERE
---
> UPDATED BRIEF — March 8, 2026. Use this section for new sessions. Original Feb 28 brief above is preserved for document reference.
## COPY FROM HERE FOR NEW SESSIONS
You are the lead infrastructure architect and technical strategist for Advantage Design Construction Inc. (ADC). Owner: Scott Tomsu. Lafayette, Louisiana.
### TWO PRODUCTS — Never conflate them
    - MARLIE I = permanent AI Factory at 1201 SE Evangeline Thruway. Building-based. NVL72 racks inside existing structure. HQ + NOC + primary compute. CDU liquid cooling + Bloom Energy (continuous supplemental) + LUS grid (primary) + diesel N+1.
    - ADC 3K = manufactured containerized pod product line. 40-ft ISO containers deployed to remote sites as units. Immersion cooling (no HVAC, no CDU — works inside any metal structure). First deployment: Trappeys Cannery warehouse.
### Current Hardware Platform (both products)
    - NVIDIA Vera Rubin NVL72 — confirmed CES 2026, H2 2026 full production
    - 72 Rubin GPUs + 36 Vera CPUs per rack | HBM4 288 GB/GPU | NVLink 6 | 3.6 ExaFLOPS NVFP4
    - TDP NOT published by NVIDIA — all power/cooling sizing based on analyst estimates. Engage NVIDIA Enterprise Sales.
    - Blackwell / GB200 / GB300 / NVLink 5 / HBM3e — all RETIRED. Do not reference.
### Open Investor Action Items (must resolve before raise)
    1. Customer LOI — zero signed anchor tenants. Fatal for institutional investors.
    1. NVIDIA TDP — facility design unfinished without it.
    1. HB 827 — Phase 1 below 00M threshold. Develop parish-level PILOT.
    1. CapEx — 3.2M stated vs analyst -10M/rack × 14 racks. Reconcile.
    1. Financial model tax rate — 5.5% not ~25%. Fix Assumptions tab.
### Notion Workspace IDs
    - HQ: 31288f09-7e31-81a5-bf43-e2af16379346
    - MARLIE I: 31e88f09-7e31-8121-b4d2-d96b0084cc50
    - ADC 3K Command Center: 31488f09-7e31-816d-9fdc-c6aabba4e3fa
    - Trappeys AI Center: 31288f09-7e31-80a2-8712-ef09878afd53
### Louisiana Incentives
    - ITEP: file BEFORE breaking ground — non-negotiable
    - LA corporate tax: 5.5% | Henry Hub proximity: 40 miles — lowest natural gas cost in US
    - Historic Tax Credits: 45% combined | NVIDIA Inception: application ready, not submitted
---
> MARCH 21, 2026 UPDATE -- Post-GTC Strategic Pivot + Trappeys Core Project
This section supersedes conflicting info above. The Feb 28 and March 8 briefs are preserved for reference but the strategic direction has fundamentally shifted after GTC 2026 (March 17-21).
## Strategic Pivot: ADC Is a Neocloud
    - ADC is a NEOCLOUD -- GPU-first cloud provider, not a colocation facility. Energy-first model (Crusoe's playbook). Full NVIDIA stack. Sell tokens, not GPU hours.
    - Token Factory model -- managed inference via Dynamo 1.0 + Groq LPU decode. 7x performance on same Blackwell hardware. GPU prefill + Groq decode = 35x tokens/watt. Higher margin than bare metal GPU rental.
    - DSX Reference Design -- NVIDIA's complete AI factory blueprint. ADC builds to spec. 800V DC power (Eaton Beam Rubin). Direct-to-chip liquid cooling. InfiniBand fabric.
    - EC-110 immersion DEPRIORITIZED -- NVIDIA ships complete liquid-cooled racks (45 deg C hot water, 2-hr install). Immersion may still apply to edge/remote only.
## Trappeys = THE Core Project
    - Trappeys Cannery -- 112,500 sq ft across 4 buildings. Former cannery, Lafayette LA. ~$1M acquisition. Brownfield (M2 zoning). Half mile from MARLIE I. 30 mi from First Solar New Iberia factory.
    - 2.05 MW solar -- 3,731 First Solar TR1 panels across 4 rooftops. 800V DC solar-direct to DSX bus (97% efficiency vs 92% AC path).
    - 4-layer power hierarchy -- Solar (primary offset) > Natural Gas (backbone 24/7) > Diesel (emergency) > Grid (sell-back ONLY, not a source).
    - 9-page mini-site LIVE -- adc3k.com/trappeys + campus + technology + university + responders + investors + plan + dsx-prep + presentation
    - Phase 1 budget: $1.1-1.7M (equipment) + $300-500K (engineering/services). Full procurement matrix with primary + backup US vendors for every component.
## Certification Ladder
    - NPN (register NOW, 5-min form)  > DGX-Ready (Willow Glen)  > NCP (NVIDIA Cloud Partner)  > Reference Platform NCP
    - Inception is for software startups, NOT infrastructure. ADC goes through Partner Network.
## Key Contacts & Next Steps
    - UL Lafayette -- New president Dr. Ramesh Kolluru (CS PhD, R1 builder). No GPU infra. LEDA for warm intro. $28-55M+ grant potential.
    - ITEP -- NAICS code risk. Must pre-qualify with LED as 'emerging industry.' $8-16M savings. Contact: Kristin Johnson, 225-342-2083.
    - Act 730 -- Separate 20-year sales tax exemption ($200M+, 50 jobs).
    - First Solar -- LOCKED IN. Series 7 TR1. $1.1B New Iberia factory 30 mi away. modulesales@firstsolar.com / 419-662-6899.
    - Vendor tiers complete in Notion -- Tier 1 (hardware), Tier 2 (operational partners & professional services), Tier 3 (government & institutional). All under Vendor & Partner Strategy.
## Deployed Assets (adc3k.com)
    - 73+ HTML pages deployed to Vercel. Trappeys mini-site (9 pages + 40 photos). Omniverse DSX renders (v4 batch, 12 investor-grade). Investor page. Lafayette city pitch. Hub page links everything.
    - Business model docs in repo: token economics, power economics, capex model, revenue streams, vendor procurement matrix, ITEP filing, permits timeline, UL Lafayette approach, NPN registration checklist.
---
> ARCHIVED (2026-03-23): These session prompts are from early March 2026 (pre-GTC). The current session context is managed via CLAUDE.md in the git repo and memory files in .claude/projects/. These Notion pages are historical reference only.
*[Child: ADC-3K Website Build Logs]*
> Build logs, design decisions, and content for the ADC3K public website.
---
## Contents
  - Site architecture and page structure
  - Content drafts and copy
  - Design system and branding
  - Deployment notes
*[Child: ADC-3K POD — Website Build Log (V3)]*
> Build summary for ADC-3K-Master-Website-V3.html — production-ready SPA, March 1, 2026.
## V3 Build Summary
    - File: ADC-3K-Master-Website-V3.html | Size: ~728 KB single-file SPA with embedded images
    - Pages: 10 | Status: Production-ready as of March 1, 2026
    - Branding: ADC-3K POD — global rename complete
    - Contact: (337) 780-1535 / ADHSCOTT@yahoo.com
## Version History
    - V1-V4: 20-ft container, 800 kW, Trappeys site-specific
    - V5 (Model 2400X): 40-ft container, 2,400 kW
    - V3 Website: ADC-3K POD branding, 3 MW class
## Architecture Note (March 8, 2026)
> Website may reference CDU liquid cooling from original spec. Current ADC 3K architecture uses immersion cooling. Update copy before publishing.
## Deployment
    - Currently local file — not deployed to public URL
    - Target domain: adc3k.com | Hosting: Vercel, Cloudflare Pages, or ADC-hosted (TBD)
> ADC3K — Advanced Computing 3000, Lafayette LA. AI Factory + Edge AI + Infrastructure. Owner: Scott Tomsu.
---
## Active Projects
- MARLIE I — Lafayette AI Factory (pre-deployment, investor outreach active)
---
## Engineering Groups
- Pod Swarm Engineering Suite
- Edge AI Infrastructure Documents
- Session Prompts & Claude Context
- ADC-3K Website Build Logs
---
## Quick Links
- MARLIE I Pitch Deck: marlie/index.html in gpu-learning-lab repo
- Mission Control Dashboard: http://localhost:8000
- RunPod GPU Pods: via Mission Control > Integration Agent
---
> Everything AI, everything sovereign, everything Louisiana.
> Engineering & operations sub-workspace for ADC 3K infrastructure builds. Lives inside Mission Control HQ.
---
## Contents
- Pod Swarm Engineering Suite — NVL72 rack configs, CDU schematics, PDU layouts, network topology, RunPod API
- Session Prompts & Claude Context — AI session backups and master prompt archive
- ADC-3K Website Build Logs — V3 website build history
- Master Task Tracker — project task database
---
## Active Projects
- MARLIE I — Lafayette AI Factory: see Mission Control HQ → MARLIE I (Sections 01-09)
- Pod Swarm: NVL72 rack engineering package — see Pod Swarm Engineering Suite
---
> New root sections are being added to Mission Control HQ. This workspace handles engineering sub-documents.
---
> INVESTOR REVIEW — CRITICAL FIXES (March 8, 2026) | Items 6 & 7 RESOLVED. Items 1-5 require action.
## Issues That Will Kill the Deal in Diligence
### 1. No Customer — Fatal for Institutional Investors
- Zero signed LOIs or anchor tenant commitments documented anywhere
- All financial projections rest on assumed utilization with no demand validation
- ACTION: Secure at least one signed LOI before next investor meeting
### 2. TDP Not Confirmed by NVIDIA
- NVL72 Vera Rubin TDP not published — entire power, cooling, and electrical design built on analyst estimates (150-250 kW/rack)
- Cannot finalize CDU sizing, generator spec, or panel design without confirmed TDP
- ACTION: Engage NVIDIA Enterprise Sales — get written facility planning spec
### 3. HB 827 — Phase 1 Does Not Qualify
- HB 827 requires 00M minimum eligible investment. Phase 1 at 9-30M is below threshold
- This is listed as a named incentive in pitch materials — investors who know LA law will catch it
- ACTION: Fully develop parish-level PILOT agreement NOW as the replacement. Brief investors honestly.
### 4. CapEx Does Not Add Up
- 3.2M total CapEx stated. Analyst estimates for prior-gen GB200 NVL72 were -10M per rack.
- 14 Vera Rubin NVL72 racks at even half that = 6-70M hardware alone
- ACTION: Either reconcile CapEx with actual NVIDIA pricing OR reduce rack count to match 3.2M budget
### 5. Financial Model Tax Rate Error
- Model uses ~25% blended Louisiana corporate tax rate. Actual rate: 5.5%
- IRR is higher than currently shown — but model presented to investors is wrong
- ACTION: Update financial model Assumptions tab before next investor meeting
### 6. Bloom Energy Language — CORRECTED (2026-04-03)
- LOCKED: Bloom Energy SOFC = PRIMARY generation (800V DC direct, no inverter, Henry Hub gas). First Solar = 1500V DC layer. LUS grid = sell-back only. Diesel = emergency N+1 only.
- FIXED: Power Distribution page now has corrected hierarchy callout at top of page.
---
## What Institutional Investors Expect That Is Missing
- Signed LOI or anchor tenant term sheet
- Independent engineering validation — third-party thermal/electrical stamp
- 3-scenario financial model: bear (50% utilization), base (75%), bull (90%) with sensitivity tables
- Capital stack and waterfall — equity, debt, mezzanine structure with return hurdles
- Management team bios — LinkedIn-level detail on all team members with hyperscale or data center experience
- Written utility capacity confirmation from LUS or SLEMCO
- NVIDIA Enterprise relationship — Inception application submitted (listed as open task)
- Comparable transaction analysis — what did similar GPU campus deals trade at
- Exit strategy — 5-year path to liquidity: acquisition target, cash yield, or IPO path
---
## What Is Strong — Do Not Change
- Site ownership: 5K debt-free land, no lease risk — lead with this
- Henry Hub proximity — verifiable natural gas cost advantage
- Bloom Energy 3-layer power architecture — modern, ESG-aligned, differentiating
- ADC Inc. as GC (est. 2003) — construction risk internally managed, not outsourced
- Edge AI repositioning and terminology — polished, market-correct
- Louisiana incentive awareness — ITEP timing, parish PILOT — shows operational sophistication
---
> ARCHITECTURE CLARIFICATION — TWO SEPARATE PRODUCTS (March 8, 2026)
## Product 1: MARLIE I — Lafayette AI Factory (Fixed Facility)
- Location: 1201 SE Evangeline Thruway, Lafayette, Louisiana — owner-controlled, debt-free
- Type: Permanent building-based AI Factory — NVL72 racks inside existing structure
- Role: ADC HQ, primary compute facility, NOC, operations base
- Phase 1: 16 NVL72 racks on 22x35 ft floor — 57.6 ExaFLOPS NVFP4
- Cooling: Direct-to-chip CDU liquid cooling, exterior dry coolers. Power: Bloom SOFC primary + First Solar + LUS grid sell-back
## Product 2: ADC 3K — Containerized AI Pod (Manufactured Product Line)
- Type: Standardized containerized compute nodes — manufactured, sold, and deployed as units
- Role: Remote site deployments — edge AI distribution centers tied into the network
- Cooling: Direct-to-chip liquid cooling. External dry cooler. No HVAC required — enables deployment into metal structures without AC.
- First deployment site: Trappeys Cannery — metal warehouse structure, liquid-cooled pods
- Future sites: Industrial yards, commercial facilities, any site with power + fiber — no special building required
- Scale: Multiple pods per site, networked back to MARLIE I
> These are two different products serving different purposes. MARLIE I is the factory. ADC 3K pods are the distributed product deployed from it.
---
## Investor Review — Second Pass Gaps (March 8, 2026)
> These 7 gaps must be addressed before institutional investor meetings. Items marked [SCOTT ACTION] require work outside Notion.
### Gap 1 — Unit Economics Per Pod [SCOTT ACTION]
Missing: Revenue per pod, CapEx per pod, payback period per pod, gross margin per pod. Institutional investors need to evaluate the unit economics of the product — not just the aggregate financial model.
- Add to financial model: pod CapEx (container + hardware + liquid cooling system + install), monthly revenue per pod (colocation rate x GPU capacity), OpEx per pod (fluid maintenance, remote NOC, power), payback period per pod
- Target: 18–36 month payback per pod at base-case utilization
### Gap 2 — Remote Site Operations Model [SCOTT ACTION]
Missing: Who manages the pod at the remote site? What is the SLA? How is maintenance handled? This is a core differentiator — answer it explicitly.
- Model: MARLIE I NOC manages all pods remotely via Mission Control — no on-site staff at remote locations
- Maintenance: Fluid checks and GPU swap require on-site visit — contract with local HVAC/electrical firm per deployment site
- SLA target: 99.5% uptime — document in investor deck and customer contracts
- Site owner role: Provides power, fiber, and space — ADC 3K handles everything inside the container
### Gap 3 — Dielectric Fluid: RESOLVED (March 8, 2026)
> COMMITTED: Engineered Fluids EC-110 (single-phase). All 3M Novec references removed. Novec is discontinued — Engineered Fluids is the standard replacement.
### Gap 4 — Competitive Landscape [SCOTT ACTION]
No competitive analysis in investor materials. Institutional investors will ask: who else does this and why will you win?
- Direct competitors: CoreWeave (cloud GPU), Lambda Labs, Crusoe Energy (stranded gas), Lancium (remote compute)
- ADC 3K differentiators: (1) Site-agnostic liquid-cooled pod — deploy anywhere with power + fiber, (2) Louisiana incentive stack + Henry Hub gas proximity, (3) Owner-operator with captive manufacturing base (MARLIE I), (4) Small-footprint pod enables enterprise edge AI, not just hyperscale
- Add competitive landscape slide to investor deck — 1 slide, 4 quadrants or simple table
### Gap 5 — Exit Strategy [SCOTT ACTION]
- Option A: Acqui-hire / strategic acquisition — ADC 3K as manufactured AI infrastructure product is acquisition target for hyperscalers or REITs
- Option B: Build-to-sell — sell deployed pod swarms to data center operators or PE-backed infra funds
- Option C: REIT structure — pool pods into income-producing AI infrastructure fund (public or private)
- Add 1-slide exit strategy to investor deck — show realistic 5–7 year horizon
### Gap 6 — Management Team [SCOTT ACTION]
No team slide in investor materials. Investors bet on people as much as ideas. This gap can kill a raise regardless of how good the tech is.
- Add team slide: founder bio, relevant construction/real estate/AI experience, any advisors or anchor relationships
- Key hires to identify: CTO/engineering lead, CFO or fractional CFO for raise, NVIDIA/hyperscaler enterprise sales contact
### Gap 7 — 3-Scenario Financial Model [SCOTT ACTION]
- Bear case: GPU utilization 40%, GPU price correction -30%, deployment delays 12 months
- Base case: GPU utilization 70%, current market rates, H2 2026 Vera Rubin delivery on schedule
- Bull case: GPU utilization 90%, premium enterprise pricing, multi-site pod swarm at 10+ locations by Y3
- ALSO FIX: Tax rate in model is ~25% — Louisiana corporate tax is 5.5%. IRR is materially higher than currently modeled.
- ALSO FIX: CapEx $33.2M stated vs analyst estimate $8-10M/rack x 14 racks = $112-140M. Reconcile or explain.
- ALSO FIX: HB 827 threshold: Phase 1 is below $200M — replace HB 827 with parish-level PILOT and brief investors honestly
---
## ADC 3K Deployment Geography — Natural Gas Pipeline Map
ADC 3K liquid-cooled pods deploy along Louisiana natural gas pipeline corridor. This is not arbitrary. Gas pipeline infrastructure means: existing utility roads, 3-phase power stubs, industrial zoning, and co-location opportunity with captive industrial customers.
- Deployment logic: pods follow Atmos/CenterPoint gas pipeline map — industrial site co-location
- Henry Hub corridor: Erath, LA (~40 mi from MARLIE I) — Vermilion Parish gas distribution hub
- Gulf Coast industrial belt: refineries, LNG export terminals, petrochemical plants — captive ADC customers
- New Iberia (Site 2 candidate): solar factory + industrial port + pipeline access — ADC pod + energy partner
- Lake Charles / Cameron Parish: LNG export corridor — security, monitoring, AI inference pods
- Morgan City: offshore supply base, pipeline terminus — SAR + industrial AI
- Scaling rule: one ADC 3K pod per industrial customer — liquid-cooled pod drops into existing metal structure
---
## Ecosystem Network — How ADC 3K Connects to Everything
> ADC 3K is NOT a standalone product. It is the field arm of the ADC ecosystem. MARLIE I is the brain. ADC 3K pods are the muscle. KLFT is the showcase. Ground Zero tells the story.
- MARLIE I (HQ/NOC): all ADC 3K pods managed from 1201 SE Evangeline Thruway — Mission Control AI
- Trappeys Cannery (Site 1 planned): first remote pod deployment — metal warehouse, liquid cooling
- KLFT 1.1 (first live node): ADC 3K pod at Lafayette airport — SkyCommand compute, emergency drone ops
- New Iberia (Site 2): solar factory + ADC pod — renewable energy anchor + industrial AI customer
- Ground Zero: YouTube channel @GroundZero-ai — ADC ecosystem documentary, 8 planned ADC episodes
- SkyCommand SaaS: drone fleet management — runs on ADC 3K pod at KLFT, scales to multi-site
---
## Cooling Architecture (Updated Post-GTC 2026)
NVIDIA ships complete liquid-cooled racks (45 deg C hot water, 2-hour install). EC-110 immersion cooling DEPRIORITIZED for main facilities post-GTC 2026. The standard is now NVIDIA reference liquid cooling with direct-to-chip cold plates. Dry coolers for heat rejection. PUE target: 1.03. EC-110 may still apply to edge/remote deployments where standard rack cooling is impractical.
- Direct-to-chip liquid cooling: 45 deg C hot water loop. No massive AC systems. No loud fans. NVIDIA-standard for all Blackwell/Vera Rubin racks. Eaton Beam Rubin DSX handles 800V DC power delivery.
- Louisiana rationale: 95°F+ summers, 80%+ humidity — air cooling costs 40-80% of power budget
- No HVAC: zero air conditioning, zero CRAC, zero raised floor — pods deploy into raw warehouse space
- No fans: sealed fluid bath — silent, zero vibration, maximum GPU lifespan
- MARLIE I is DIFFERENT: cold plate CDU — building-based, code-compliant, public-facing state of the art
---
## New Iberia Solar Factory — Strategic Energy Partner
Local utility-scale solar production facility ~30 miles from MARLIE I in New Iberia, LA. New Iberia is simultaneously a candidate for ADC 3K Site 2 deployment and a renewable energy supplier.
- Energy role: solar PPA or wheeled credits through LUS grid — supplements Bloom + LUS + nat gas stack
- Site 2 role: ADC pod deployed at or near solar factory — captive AI compute for solar ops analytics
- Industrial port access: New Iberia has port and petrochemical industrial base — additional pod customers
- KLFT expansion: New Iberia is Site 2 candidate for KLFT Gulf Coast drone network expansion
- FEOC compliance: domestic renewable energy source — reinforces OBBBA clean-energy qualification
> MCHD ON HOLD: 18 tasks frozen as of 2026-03-23. Resume when Mission Control HD SaaS project restarts.
---
> MASTER TASK TRACKER — POST-GTC UPDATE (2026-03-23): The 35 tasks in this tracker reference 20-ft ISO containers and old specs. Post-GTC reality: 40-ft HC ISO containers, NVIDIA ships complete liquid-cooled racks (no custom immersion), 800V DC via Eaton Beam Rubin DSX. Tasks referencing 'Order 20-ft ISO container', CDU procurement, and immersion cooling are SUPERSEDED. Keep tasks for reference but specs must be updated when pod build restarts.
---
> CRITICAL UPDATE (2026-03-24): AUDIT RESULTS -- This page has severe stale content:
- "Two-Product Model" says MARLIE I is HQ -- WRONG. Willow Glen is PRIMARY.
- References NVIDIA Inception -- WRONG. ADC goes through Partner Network (NPN).
- Lists Bloom Energy as a strength -- REMOVED from power stack.
- Says 16 racks Phase 1 -- WRONG. MARLIE I is 8 racks per floor (16 total, 2 SuperPODs).
- Says immersion cooling for ADC 3K pods -- DEPRIORITIZED. NVIDIA ships liquid-cooled racks.
- Email shows ADHSCOTT@yahoo.com -- WRONG. Use scott@adc3k.com.
- All content below "POST-GTC" callouts is current. Everything above is pre-GTC and largely wrong.
- CLAUDE.md and memory files in .claude/projects/ are the authoritative source of truth.