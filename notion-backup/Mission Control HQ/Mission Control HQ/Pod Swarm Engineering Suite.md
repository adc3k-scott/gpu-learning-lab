# Pod Swarm Engineering Suite
*Notion backup — 2026-04-03*

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
> NVL72 is 100% liquid cooled. No air cooling fallback. CDU units mount rear of each rack. Heat rejected to exterior dry coolers via closed glycol loop.
---
## System Overview
  - Type: Rear-door liquid cooling — CDU (Coolant Distribution Unit) per rack
  - Loop: Closed primary loop: rack CDU <-> exterior dry cooler
  - Coolant: Deionized water + glycol mix (40/60 for Louisiana climate)
  - Heat rejection: Exterior dry coolers — no chiller required at Phase 1 scale
  - Phase 1 total heat load: NVIDIA rack TDP unconfirmed — size service for 150-250 kW/rack per analyst estimates (not NVIDIA-confirmed)
---
## Loop Topology
### Primary Loop (High Temp)
  - Supply temp target: 45C supply to CDU inlet
  - Return temp target: 55-60C return from CDU outlet
  - Flow rate: Per NVIDIA CDU spec — typically 20-40 L/min per rack
  - Pump: Variable speed — pressure regulated
---
### Secondary Loop (Dry Cooler)
  - Location: Exterior — north wall or rooftop mount
  - Type: Adiabatic dry cooler — air-cooled finned coil, optional misting for peak days
  - Climate note: Lafayette avg high 93F summer — size dry cooler for 100F ambient
  - Glycol loop: Runs through exterior wall penetration (insulated sleeve)
  - Isolation valve: 1x ball valve per dry cooler — serviceable without rack downtime
---
## Pipe Routing Schematic — Phase 1
```plain text
Exterior wall (north)
  [Dry Cooler 1] [Dry Cooler 2] [Dry Cooler 3] [Dry Cooler 4]
       |               |               |               |
  ====[ Supply manifold — 4-inch insulated pipe along north wall ]====
       |               |               |               |
  [CDU A01-A04]  [CDU A05-A08]  [CDU B01-B04]  [CDU B05-B08]
  ====[ Return manifold — 4-inch insulated pipe along north wall ]====
       |               |               |               |
  [ Pump station — NW corner — 2x variable speed pumps, 1 redundant ]
```
---
## Key Components
  - CDU units: 16x — 1 per NVL72 rack (NVIDIA-supplied or approved vendor)
  - Dry coolers: 4x exterior — sized for 500 kW each (2 MW total capacity)
  - Pump station: 2x variable speed pumps — N+1 redundancy
  - Expansion tank: 1x — pressure relief, glycol makeup
  - Flow meters: 1x per CDU loop — monitored via BMS
  - Leak detection: Rope-style sensor along entire manifold run
  - Isolation valves: Ball valves at each CDU inlet/outlet — hot-swap capable
---
## Wall Penetration Detail
  - Penetration size: 6-inch core drill — north exterior wall
  - Sleeve: Insulated pipe sleeve — vapor barrier sealed
  - Fire stop: Intumescent firestop collar — maintain Type X fire rating
  - Contractor: Licensed mechanical contractor — permit required
---
## Monitoring
  - BMS: Building Management System — supply/return temps, flow rate, leak status
  - Alerts: High temp (>62C return), low flow, leak detection — SMS + Mission Control event
  - Integration: InfraManagerAgent monitors BMS via HTTP API or Modbus gateway
> SCOPE: This document applies to MARLIE I — the permanent AI Factory at 1201 SE Evangeline Thruway. NOT applicable to ADC 3K container pods, which use immersion cooling and a separate architecture.
---
## ADC 3K Container Pod Cooling — DIFFERENT ARCHITECTURE
> ADC 3K pods use immersion cooling, NOT rear-door CDU. Immersion eliminates HVAC requirements entirely — pods deploy into metal structures (e.g. Trappeys Cannery warehouse) with no air conditioning infrastructure needed. Separate engineering spec required for ADC 3K immersion loop, dielectric fluid selection, and heat rejection.
  - Heat rejection: Dry cooler or liquid-to-liquid HX — same exterior rejection strategy as MARLIE I but different primary loop
  - PUE target: 1.02-1.05 — immersion is more efficient than CDU at pod scale
  - Advantage: No HVAC, no raised floor, no hot aisle containment — drops into any structure with power + fiber
  - First deployment: Trappeys Cannery metal warehouse — immersion pods, no structural HVAC modifications required
---
## ADC 3K Pod — Immersion Cooling (Remote Deployments)
> ADC 3K pods use immersion cooling — NOT CDU/liquid cooling. CDU applies to MARLIE I (building racks). These are two separate products.
### Dielectric Fluid — Committed Specification
> COMMITTED: Engineered Fluids EC-110 (single-phase immersion). 3M Novec is DISCONTINUED — do not reference in investor materials or engineering specs.
  - Fluid: Engineered Fluids EC-110 — single-phase dielectric, non-flammable, non-toxic, commercially available
  - Cooling method: Single-phase immersion (servers submerged in fluid bath inside 40-ft ISO container)
  - Heat rejection: Exterior dry cooler (primary) or liquid-to-liquid HX — no HVAC required at deployment site
  - PUE target: 1.02–1.05 (immersion eliminates almost all cooling overhead)
  - Vendor: Engineered Fluids — RFI package prepared, not yet submitted
  - GPU platform: NVIDIA Vera Rubin NVL72 — TDP not yet published by NVIDIA. Final tank sizing pending TDP confirmation.
### Remote Site Power Spec (Per Pod)
  - Input: 480V 3-phase, utility feed to pod junction box
  - Backup: N+1 diesel generator, exterior pad mount, auto-start <15 sec
  - Fiber: Site must have fiber connectivity — pod networks back to MARLIE I NOC
  - Remote monitoring: MARLIE I NOC manages all deployed pods centrally — no on-site staff required at remote locations
---
> SCOPE OF THIS DOCUMENT: Cold plate CDU cooling schematics are for MARLIE I (1201 SE Evangeline Thruway ONLY). ADC 3K pods at Trappeys, KLFT, New Iberia, and all other remote sites use FULL IMMERSION (EC-110). Do NOT apply CDU schematics to ADC 3K pod deployments.
## Cooling Architecture — Two Systems, Same GPU Platform
  - MARLIE I: Cold plate CDU — NVL72 racks in sealed hot aisle, CDU at each end, dry coolers exterior
  - ADC 3K pods: EC-110 full immersion — NVL72 GPUs submerged in dielectric bath inside 40-ft ISO container
  - Both systems: achieve PUE 1.02-1.10, zero rack-level air cooling, 100% direct liquid heat removal
  - Why CDU for MARLIE I: permanent building, code compliance, public-facing, hot aisle containment standard
  - Why immersion for ADC 3K: field deployment, variable ambient (Louisiana heat/humidity), no HVAC permitting
  - NVL72 GPU compatibility: same hardware in both — different fluid delivery path, same thermal outcome
---
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
> CRITICAL WARNING (2026-03-24): This page has 4 CONFLICTING cooling architectures. ONLY the "POST-GTC REWRITE" section is correct. The 3 sections above it pushing EC-110 immersion are WRONG -- NVIDIA ships complete liquid-cooled racks, immersion is deprioritized. Ignore all immersion content.
*[Child: Power Distribution Unit Layouts]*
> Phase 1 target: ~2 MW total load (16 NVL72 racks + cooling + network). Natural gas generators and UPS batteries stay outside the thermal envelope.
---
## Power Architecture
  - Source A: LUS Power utility feed — primary
  - Source B: Natural gas generators (exterior) — automatic transfer switch (ATS)
  - UPS: Exterior battery cabinet — bridges utility-to-generator gap (~10-15 sec)
  - Distribution: 480V 3-phase to main panel — step-down to rack PDUs
  - Phase 1 load estimate: NVIDIA rack TDP unconfirmed — engage NVIDIA Enterprise for facility power spec
---
## Exterior Equipment (Outside Thermal Envelope)
  - Generators: 2x natural gas gensets — N+1 — exterior south pad mount
  - ATS: Automatic Transfer Switch — exterior weatherproof enclosure
  - UPS batteries: Battery cabinet — exterior weatherproof, climate controlled
  - Main disconnect: Main breaker panel — exterior accessible
---
## Interior Distribution
### Main Distribution Panel
  - Feed: 480V 3-phase from exterior ATS through conduit penetration
  - Breakers: 1x 400A 3-phase breaker per 2-rack PDU zone (8 breakers total)
  - Location: Network core — north end of room
---
### Per-Rack PDU
  - Qty: 8x dual-feed PDUs — each serves 2 NVL72 racks
  - Type: Metered, switched — remote outlet control via SNMP/REST
  - Input: 480V 3-phase / 200A per PDU
  - Monitoring: Per-outlet current metering — feeds InfraManagerAgent
---
## Generator Spec (Preliminary)
  - Fuel: Natural gas — Atmos Energy supply line
  - Size: 2x 1.25 MW continuous — N+1 for 2 MW load
  - Startup: Auto-start on utility fail — <15 sec to full load
  - Enclosure: Sound-attenuated weatherproof — exterior pad mount
  - Fuel line: Atmos Energy commercial service — 2-inch minimum supply
---
## PUE Target
```plain text
PUE = Total Facility Power / IT Equipment Power
    = (1.92 MW compute + 0.06 MW cooling aux + 0.02 MW misc) / 1.92 MW
    = ~1.04  (liquid cooled, no CRAC units, no hot aisle air handling)

Industry best practice: <1.2
Hyperscale liquid-cooled target: <1.1
MARLIE I target: <1.05
```
---
## Monitoring
  - Mission Control: InfraManagerAgent — real-time kW per rack, PUE, phase balance
  - Alerts: Over-current, phase imbalance, generator ATS transfer events, UPS state
> CORRECTED POWER HIERARCHY (March 8, 2026): LUS grid = primary. Bloom Energy fuel cell = continuous supplemental generation (baseload, not backup). Diesel gensets = emergency backup only (N+1). Do not describe Bloom as primary or as backup — it is continuous supplemental.
---
> SCOPE: This document applies to MARLIE I — the permanent AI Factory at 1201 SE Evangeline Thruway. NOT applicable to ADC 3K container pods, which use immersion cooling and a separate architecture.
---
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
> CRITICAL WARNING (2026-03-24): This page has 3 CONFLICTING power hierarchies. ONLY the POST-GTC section is correct: 800V DC native, Eaton Beam Rubin DSX, 4-layer hierarchy (Solar > Gas > Diesel > Grid sell-back). Bloom Energy is REMOVED. LUS grid is backup only at MARLIE I. 480V 3-phase content is WRONG.
*[Child: Network Topology Diagrams]*
> Three separate fabrics: NVLink 6 (intra-rack GPU), InfiniBand NDR (inter-rack compute), Spectrum-X Ethernet (external/storage). Management on isolated 10GbE.
---
## Fabric 1 — NVLink 6 (Intra-Rack GPU Fabric)
  - Scope: Within each NVL72 rack only
  - Bandwidth: 3.6 TB/s per GPU bidirectional (NVLink 6) — 260 TB/s aggregate across rack
  - Topology: Rail-optimized via 9x NVLink 6 Switch per rack
  - Cabling: Factory-integrated — no field assembly
  - Latency: Sub-microsecond GPU-to-GPU within rack
---
## Fabric 2 — InfiniBand NDR (Inter-Rack Compute Fabric)
```plain text
                 [ IB Spine Switch (64-port NDR400) ]
                /              |              \
       [IB Leaf 1]        [IB Leaf 2]        [IB Leaf 3]
       (32-port NDR)      (32-port NDR)      (32-port NDR)
      / | | | | \        / | | | | \        / | | | | \
    A01 A02 A03 A04   A05 A06 A07 A08   B01 B02 B03 B04
                                         B05 B06 B07 B08

Each rack: 2x ConnectX-9 SuperNIC (1.6 Tb/s each)
Each leaf: 16 downlinks (rack) + 8 uplinks (spine)
Total bisection BW: ~25.6 Tb/s
Oversubscription: 2:1 leaf-to-spine
```
  - Switch vendor: NVIDIA Quantum-3 InfiniBand
  - Per-port BW: 400 Gb/s NDR
---
## Fabric 3 — Spectrum-X Ethernet (External / Storage)
```plain text
[ LUS Fiber Uplink -- 100GbE (upgrade path: 400GbE) ]
        |
  [ Spectrum-6 (SN6810 / SN6800) Top-of-Row Switch ]
   /    |    |    |    |    |    |    \
 A01  A02  ...  B08  [NAS] [Object Store] [Customer VPN]

Each NVL72: 1x 400GbE to Spectrum-X via BlueField-4 DPU
Purpose: external customer traffic, storage, internet uplink
```
  - LUS Fiber uplink: 100GbE day 1 — upgrade path to 400GbE / dark fiber
  - BlueField-4 DPU: Offloads networking/storage from Vera CPU — 1 per rack
  - Switch: NVIDIA Spectrum-6 SN6810 (102.4 Tb/s) / SN6800 (409.6 Tb/s) — co-packaged optics, 800 Gb/s ports
---
## Fabric 4 — Management Network (OOB)
```plain text
[ Management Switch -- 24-port 10GbE ]
  |  |  |  |  ...  |  |  |  |
 A01 A02 ... B08  [MC Server] [BMS GW] [KVM/IPMI]

Purpose: out-of-band management, independent of compute fabrics
Access: BMC/IPMI per rack + BlueField-4 DPU management port
Remote: WireGuard / Tailscale VPN
```
---
## WAN / Uplink
  - Provider: LUS Fiber — city-owned, direct negotiation, no Big Telecom premium
  - Day 1: 100GbE dedicated
  - Upgrade path: 400GbE or dark fiber as customer demand grows
  - Redundancy: SLEMCO or secondary carrier as failover
  - BGP: Own AS number + IP block for sovereign routing — Phase 2 target
---
## IP Plan (Draft)
```plain text
Management:    10.0.0.0/24    -- BMC, switches, BMS
Compute IB:    10.1.0.0/16    -- InfiniBand fabric
Storage/Eth:   10.2.0.0/16    -- Spectrum-X tenant fabric
Customer VMs:  10.100.0.0/16  -- NAT to LUS uplink
Mission Ctrl:  10.0.0.1
DNS/NTP:       10.0.0.2
```
> SCOPE: This document applies to MARLIE I — the permanent AI Factory at 1201 SE Evangeline Thruway. NOT applicable to ADC 3K container pods, which use immersion cooling and a separate architecture.
---
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
> WARNING (2026-03-24): Pre-GTC fabric specs above reference Quantum-3 NDR 400 Gb/s. CORRECT: Quantum-X800 at 800 Gb/s. Hub-and-spoke architecture in POST-GTC section is authoritative.
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
    - Cooling: Immersion (dielectric fluid). No CDU, no HVAC, no raised floor. PUE target: 1.02-1.05
    - Power: 480V 3-phase + Bloom Energy supplemental + diesel N+1
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
    - 1-2 NVIDIA Vera Rubin NVL72 racks (liquid cooled, shipped complete)
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
    - 4-Layer Hierarchy: Solar -> Gas -> Diesel -> Grid (sell-back)
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
    1. NPN registration (5-min form -- DO TODAY)
    1. NemoClaw 403 bug fix (NVIDIA GitHub Issues #314, #336)
    1. Container vendor selection (40-ft HC ISO)
    1. Portable genset spec for field deployment
    1. Starlink business account for remote pods
    1. Run:AI licensing and setup
    1. First Solar panel mounting spec for container roof
---
> DANGER (2026-03-24): The "COPY FROM HERE" section at the top has WRONG pre-GTC specs. DO NOT COPY IT. Use CLAUDE.md in the git repo as the session startup source. It is current and authoritative. This Notion page is ARCHIVED -- do not use for session prompts.
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