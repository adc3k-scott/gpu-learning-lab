# Edge AI Upgrade — Part 4: Terminology Map, Site Strategy & Roadmap
*Notion backup — 2026-03-28*

> Status: DRAFT — March 2026. Covers official project terminology, site layout strategy, and phased deployment roadmap.
## PART A — TERMINOLOGY MAP
Official language for all ADC project documents, presentations, financing proposals, and investor materials. Use the right-column term in all new and revised documents. The left column is deprecated.
### Architecture & Product Language
- data center pods  ->  edge compute nodes
- container data center  ->  modular edge infrastructure
- GPU pod  ->  deployable AI compute module
- data center site  ->  edge infrastructure campus
- containerized data center  ->  modular edge compute node
- GPU cluster  ->  distributed AI compute array
- server rack  ->  compute payload (within the node context)
- data center build  ->  edge infrastructure deployment
- pod manufacturer  ->  edge infrastructure manufacturer
### NVIDIA Hardware Language
- Blackwell / GB200 / GB300 / B200 / B100  ->  RETIRED — do not reference
- Grace CPU / Grace Hopper  ->  Vera CPU (88 Olympus Arm cores, Armv9.2)
- HBM3e  ->  HBM4 (288 GB per Rubin GPU, 20.7 TB per NVL72 rack, 1.58 PB/s aggregate)
- NVLink 5  ->  NVLink 6 (3.6 TB/s per GPU bidirectional, 260 TB/s aggregate per rack)
- Spectrum-X SN5000  ->  Spectrum-6 (SN6810 / SN6800)
- ConnectX-8 / BlueField-3  ->  ConnectX-9 SuperNIC / BlueField-4 DPU
- Feynman / Kyber  ->  UNCONFIRMED — do not reference until officially announced
- Current platform reference  ->  NVIDIA Vera Rubin NVL72 (H2 2026, confirmed CES 2026)
### Performance & Compute Language
- 10x lower token cost vs Blackwell  ->  REMOVE — not NVIDIA-sourced
- 4x fewer GPUs  ->  REMOVE — not NVIDIA-sourced
- ~120 kW TDP per rack  ->  TDP not published by NVIDIA — contact NVIDIA Enterprise Sales
- 2.5x FP4 compute density vs GB200 NVL72  ->  USE THIS (3.6 vs 1.44 ExaFLOPS per rack, NVFP4)
- 260 TB/s connecting 14-rack cluster  ->  260 TB/s aggregate per NVL72 rack (intra-rack only via NVLink 6)
- Scale-out networking  ->  InfiniBand NDR (cross-rack) — not NVLink 6
### Financial & Business Language
- GPU rental business  ->  edge infrastructure hosting
- cloud GPU provider  ->  regional edge AI infrastructure operator
- data center investor  ->  edge infrastructure capital partner
- compute rental  ->  edge infrastructure services
- pod revenue  ->  edge compute hosting revenue
---
## PART B — SITE STRATEGY: 1201 SE EVANGELINE THRUWAY
Primary deployment site for MARLIE I — Lafayette AI Factory. Located in an established commercial/industrial corridor in Lafayette, Louisiana, with direct access to three-phase electrical service, LUS Fiber, natural gas, and municipal water and drainage.
### Site Overview
- Address: 1201 SE Evangeline Thruway, Lafayette, Louisiana
- Site area: Three adjacent parcels on Chag Street — approximately 0.60 acres Phase 1 footprint
- Existing asset: Borrower-owned commercial facility adjacent to site serves as operations base
- Current condition: Three blighted structures — removal included in Phase 1 scope
- Zoning: Commercial/industrial corridor — compatible with edge compute deployment
- Utility access: Three-phase electrical service, LUS Fiber, natural gas, municipal water and drainage
### Phase 1 Site Layout
- Four 20-foot ISO edge compute nodes — deployed in 2x2 grid with maintenance clearance
- Shared utility plant — central CDU (coolant distribution unit), switchgear, and MDF
- Bloom Energy fuel cell zone — reserved pad adjacent to utility plant, natural gas service pre-run
- Diesel generator backup — N+1 standby units, auto-start on grid failure
- Fiber entry point — LUS Fiber primary, diverse second carrier conduit pre-installed
- Security perimeter — fenced and monitored yard, camera coverage, access control
- Operations base — existing adjacent building handles NOC, storage, and staff functions
### Utility Infrastructure
- Power: Utility grid three-phase primary + Bloom Energy fuel cell supplemental + diesel emergency
- Cooling: Closed-loop liquid cooling plant — warm-water CDU serving all nodes, dry coolers on perimeter
- Connectivity: LUS Fiber primary (carrier-grade municipal network) + diverse carrier secondary
- Gas: Natural gas service for Bloom Energy fuel cells — Gulf Coast supply, existing infrastructure
- Water: Municipal water and drainage for cooling plant makeup water and fire suppression
### Expansion Capacity
- Phase 1 IT capacity: 520 kW across four nodes
- Phase 1 infrastructure ceiling: Designed to 800 kW per node — 3.2 MW total site capacity
- Phase 2 expansion: Additional node rows on same parcels — no new land acquisition required
- Phase 3 multi-site: Replicate site model to additional Gulf Coast locations using same manufactured nodes
- Power expansion path: Additional Bloom Energy server units stack in modular increments (300 kW each)
- Cooling expansion path: Additional CDU modules add in-line with node deployment — no plant redesign
---
## PART C — DEPLOYMENT ROADMAP
Phased deployment schedule from site preparation through regional multi-site buildout. All timelines are based on 12-week node manufacturing lead time and standard commercial construction sequencing.
### Phase 1 — MARLIE I Lafayette (2026)
1. Site prep and blight removal — Q1 2026
1. Financing close and infrastructure procurement — Q1/Q2 2026
1. Utility plant construction (CDU, switchgear, fiber, gas) — Q2 2026
1. First two node deliveries and commissioning — Q2/Q3 2026
1. NVIDIA Vera Rubin NVL72 compute payload installation — H2 2026 (per NVIDIA availability)
1. Nodes 3 and 4 deployment — Q3 2026
1. Bloom Energy Phase 1 fuel cell installation — Q3/Q4 2026
1. Full Phase 1 operational: 520 kW IT capacity, 4 nodes — Q4 2026
### Phase 2 — Capacity Expansion (2027)
1. Add nodes 5-8 on existing site — no new land required
1. Scale Bloom Energy fuel cell capacity to match expanded load
1. Upgrade fiber to additional carrier for redundancy
1. Target: 1.0 MW+ IT capacity on Lafayette site
1. Begin site evaluation for second Gulf Coast location
### Phase 3 — Gulf Coast Regional Deployment (2027-2028)
1. Deploy edge compute campus at second Gulf Coast location (New Orleans corridor or Lake Charles)
1. Leverage manufactured node inventory for rapid site-to-site replication
1. Establish regional fiber backbone between edge campuses
1. Target markets: energy sector clients, municipal contracts, enterprise AI hosting
1. Scale to 5+ regional edge campuses across Louisiana and Gulf Coast
### Manufacturing & Supply Chain Notes
- Node manufacturing lead time: 12 weeks factory-to-ship
- NVIDIA Vera Rubin NVL72 availability: H2 2026 (confirmed CES 2026 — full production)
- Bloom Energy server lead time: 6-12 months — order in parallel with site construction
- CDU and cooling plant: Standard commercial HVAC procurement — 8-12 weeks
- LUS Fiber service order: 60-90 day lead time for commercial service activation
- All Phase 1 components commercially available as of Q1 2026
---
## PART C — KLFT / SKYCOMMAND TERMINOLOGY
Use this language when referencing the KLFT drone operations project in any document.
- autonomous drone hub  ->  Gulf Coast Emergency Drone Deployment Hub
- drone operations center  ->  AI-Coordinated Drone Operations Hub
- KLFT drone project  ->  KLFT / SkyCommand — Gulf Coast Emergency Drone Deployment Hub
- commercial drones  ->  autonomous air systems (AAS) or unmanned aircraft systems (UAS)
- DJI  ->  REMOVED — do not reference. Platform: Skydio X10 + Skydio Dock only.
- drone AI compute  ->  Jetson Orin NX 16GB (edge, dock-side) | NVIDIA L40S (Phase 3, MARLIE I networked)
---
## PART D — DEPLOYMENT GEOGRAPHY STRATEGY
> ADC 3K pod deployment sites are selected based on natural gas pipeline accessibility. Louisiana's natural gas infrastructure is the deployment map.
- Primary deployment criterion: Active natural gas service at site (for Bloom Energy fuel cell integration)
- Secondary criteria: Three-phase electrical service, broadband fiber, industrial/commercial zoning, physical security
- Phase 1 hub: Lafayette — MARLIE I base station + Trappeys Cannery first pod site
- Expansion corridor: I-10 corridor — Baton Rouge (east), Lake Charles (west), New Orleans (southeast)
- Gulf Coast coverage target: Houma-Thibodaux (offshore energy support), Morgan City, Patterson (industrial)
- Renewable overlay: Sites near New Iberia solar distribution range prioritized for solar+fuel cell hybrid systems
- Airport hub: Lafayette Regional Airport (KLFT) — drone operations base, not a compute pod site
---
## PART E — ENERGY HIERARCHY (USE IN ALL DOCUMENTS)
- Now (2026): Natural gas + Bloom Energy fuel cells as primary supplemental generation
- Near-term: New Iberia solar arrays added to pod sites as daytime supplement
- Mid-term: Biogas and renewable natural gas (RNG) blended into fuel cell supply
- Long-term: Green hydrogen from Gulf Coast offshore wind — Bloom fuel cells are hydrogen-compatible
- Baseline: LUS grid primary + diesel N+1 emergency backup maintained throughout all phases