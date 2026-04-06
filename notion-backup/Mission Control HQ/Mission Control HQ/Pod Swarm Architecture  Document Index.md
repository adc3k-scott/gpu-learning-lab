# Pod Swarm Architecture — Document Index
*Notion backup — 2026-04-06*

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