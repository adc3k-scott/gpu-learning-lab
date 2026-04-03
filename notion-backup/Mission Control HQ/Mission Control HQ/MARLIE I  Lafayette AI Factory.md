# MARLIE I — Lafayette AI Factory
*Notion backup — 2026-04-03*

> Louisiana's first next-generation AI factory — 1201 SE Evangeline Thruway, Lafayette LA 70501 — ADC3K / Scott Tomsu — CONFIDENTIAL INVESTOR DECK
---
## Project Status
- Phase: Pre-deployment — investor & partner outreach active
- Hardware: NVIDIA Vera Rubin NVL72 — Full Production — H2 2026 availability
- Site: Owner-built, debt-free — $15K total property debt
- Permits: Louisiana GC License active — build-ready
- Certifications: 7 NVIDIA + FAA Private Pilot + Part 107 UAS
---
## Workbook Sections
- 01 — Investment Thesis
- 02 — Hardware: NVIDIA Vera Rubin Platform
- 03 — Site & Building Specs
- 04 — Government Funding Stack
- 05 — Infrastructure Partners
- 06 — ADC3K Credentials
- 07 — Multi-Site Vision: Louisiana AI Network
- 08 — Contact & CTA
- 09 — Financial Architecture & ROI
*[Child: 01 — Investment Thesis]*
> The market is building for Blackwell. Marlie I is built for Rubin. That gap is the investment.
---
## Thesis 01 — Skip Blackwell. Deploy Rubin.
  - 10x lower token cost vs Blackwell
  - 4x fewer GPUs for equivalent training runs
  - 22 TB/s memory bandwidth per GPU (HBM4)
  - 3.6 ExaFLOPS NVFP4 inference per NVL72 rack
  - H2 2026 — full production — Texas factories 4 hours from Marlie I
---
## Thesis 02 — Infrastructure Already Exists
  - Property debt: $15,000 total — owner-built, 20 years standing
  - LUS Fiber: ~0.8 miles — 214 Jefferson St
  - Atmos Energy (natural gas): ~3 miles — 1818 Eraste Landry Rd
  - Henry Hub gas benchmark: ~40 miles — Erath, LA
  - Lafayette Regional Airport (LFT): adjacent — Part 107 UAS
  - NVIDIA TX Manufacturing: ~4 hours — Foxconn Houston / Wistron Fort Worth
---
## Thesis 03 — Federal & State Money Is Already Flowing
  - Stargate AI Program ($500B) + One Big Beautiful Bill Act (OBBBA): federal domestic AI infrastructure push — FEOC-clean mandate, Gulf OCS revenue, BEAD broadband funding
  - Louisiana Act 730: 20-year state/local sales & use tax rebate on AI factory equipment
  - BEAD Broadband Program: federal backhaul expansion — LUS Fiber path
  - Gulf OCS Revenue: $650M/year to Louisiana through 2034
  - Marlie I: 100% FEOC-clean, Texas-manufactured hardware, Louisiana GC — qualifies for all programs
---
## Key Stats
  - 10x — Lower token cost vs Blackwell
  - 6 months — Estimated deploy timeline
  - $15K — Total property debt
  - 20 years — Louisiana tax exemption on equipment
  - #1 — Louisiana industrial power rates in USA
*[Child: 02 — Hardware: NVIDIA Vera Rubin Platform]*
> Jensen Huang: "Rubin arrives at exactly the right moment... Rubin takes a giant leap toward the next frontier of AI."
> Sam Altman: "Intelligence scales with compute... The NVIDIA Rubin platform helps us keep scaling this progress."
---
## NVL72 Rack System
  - 72 Rubin GPUs per rack
  - 36 Vera CPUs per rack
  - 3.6 ExaFLOPS NVFP4 inference per rack
  - 100% liquid cooled — zero air cooling
  - NVLink 6 switch fabric — 3.6 TB/s GPU-to-GPU per rack
  - 260 TB/s NVLink bandwidth across 14-rack DGX SuperPOD
  - 50.4 ExaFLOPS per 14-rack SuperPOD
  - Ships fully integrated from Texas factory — 5-minute install (18x faster than prior gen)
---
## Six-Chip Architecture
### 1. Rubin GPU
288 GB HBM4 — 22 TB/s memory bandwidth — 72 per rack
### 2. Vera CPU
88 custom Olympus cores — replaces x86 for AI workload orchestration — 36 per rack
### 3. NVLink 6 Switch
3.6 TB/s GPU-to-GPU fabric per rack — 260 TB/s at SuperPOD scale
### 4. ConnectX-9 SuperNIC
1.6 Tb/s aggregate per GPU — AI traffic with zero CPU involvement
### 5. BlueField-4 DPU
Rack-scale confidential computing — unlocks healthcare, finance, government workloads. Encryption, firewall, storage I/O offloaded — GPU cycles reserved for inference.
### 6. Spectrum-X Ethernet
800G per port — co-packaged optics — AI east-west traffic at rack scale
---
## 5 Investor Facts
  - Fact 01: First rack-scale confidential computing — new market segments unlocked
  - Fact 02: 18x faster deployment — 5 min install vs 1.5 hours prior gen
  - Fact 03: 50.4 ExaFLOPS from 14 racks (DGX SuperPOD)
  - Fact 04: 260 TB/s NVLink bandwidth across full SuperPOD cluster
  - Fact 05: Full production H2 2026 — 4 hours from Marlie I (Foxconn Houston / Wistron Fort Worth)
---
## MARLIE I + 3 Pod Compute Allocation
> 40 NVL72 racks total — 2,880 GPUs — 5,200 kW IT load — 10 MW Bloom SOFC generation
### Building — Downstairs (Compute)
  - 10 NVL72 racks — single row along 37 ft usable length
  - Same single-row layout as ADC 3K pod — 24 ft width provides full cold aisle + CDU equipment space
  - 720 GPUs — 1,300 kW IT load
  - 10 Bloom SOFC units — 2,500 kW generation
  - 1 CDU pair — NVIDIA-integrated liquid cooling, 45C hot water, exterior dry coolers
### Building — Upstairs (NOC)
  - Mission Control operations center — no compute racks
  - Network core, fiber MDA, monitoring, command ops
  - Backup NOC for Willow Glen (60 mi, dedicated fiber, management traffic only)
### Pod 1
  - 10 NVL72 racks — single row, 40 ft container
  - 720 GPUs — 1,300 kW IT load
  - 10 Bloom SOFC units — 2,500 kW generation
### Pod 2
  - 10 NVL72 racks — single row, 40 ft container
  - 720 GPUs — 1,300 kW IT load
  - 10 Bloom SOFC units — 2,500 kW generation
### Pod 3
  - 10 NVL72 racks — single row, 40 ft container
  - 720 GPUs — 1,300 kW IT load
  - 10 Bloom SOFC units — 2,500 kW generation
---
### Total MARLIE I Footprint
  - 40 NVL72 racks
  - 2,880 Rubin GPUs
  - 5,200 kW IT load
  - 40 Bloom SOFC units x 250 kW = 10,000 kW (10 MW) generation
  - Facility draw at PUE 1.10: ~5,720 kW — Bloom headroom: ~4,280 kW
  - 800V DC native via Eaton Beam Rubin DSX
*[Child: 03 — Site & Building Specs]*
> Scott Tomsu designed and built this building himself, 20 years ago. Multiple direct Gulf hurricane impacts — zero structural damage.
---
## Address
1201 SE Evangeline Thruway, Lafayette, LA 70501 — ADC3K HQ
---
## Building Dimensions
  - Exterior footprint: 24 ft x 40 ft
  - Downstairs (compute): 24 ft wide x 37 ft usable — staircase takes 3 ft
  - Upstairs (NOC): full second floor — operations center, no compute racks
  - Adjacent Chag Street: 3 parcels, ~0.60 acres — owned, targeted for pod deployment
---
## Ceiling & Structure
  - Plate height: 7 ft 11 in to bottom of ceiling assembly (measured)
  - Framing: 2x12
  - Ceiling assembly: two layers 5/8 Type X sheetrock + insulation + full floor above
  - Fire rating: UL-rated assembly — built-in from day one
  - Insulation: heavy throughout — complete thermal shell — optimal for liquid cooling stability
  - Foundation: reinforced concrete slab
---
## Downstairs Layout — Single Row, 10 NVL72 Racks
> Same design as ADC 3K pod. 10 racks in a single row along the 37 ft length. 24 ft width gives full cold aisle + CDU space — no second row needed.
  - Single row of 10 NVL72 racks running 37 ft length
  - 24 ft width: cold aisle on front face, hot aisle + CDU equipment space at rear
  - CDU pair at row ends — liquid heat rejection to exterior dry coolers on concrete pad
  - Network core / fiber MDA / CDU controls — compact zone near entry
  - ALL mechanical exterior: dry coolers, UPS batteries, Bloom units, security, fuel systems
The extra width vs a container (24 ft vs ~8 ft interior) provides full maintenance access and CDU equipment space without requiring a second rack row. Building and pods share the same thermal architecture and power design — different enclosures, same playbook.
---
## Upstairs — NOC
  - Mission Control operations center
  - Network monitoring, telemetry, command ops
  - Backup NOC for Willow Glen (60 mi, dedicated fiber, management traffic only)
  - No compute racks — no IT load
---
## Site Specs
  - FEMA Zone: Zone X — Minimal Flood Hazard
  - Ground elevation: high ground — above regional base flood elevation
  - Zoning: Industrial — heavy use permitted
  - Property debt: $15,000 total
  - Storm history: multiple direct hurricanes — zero structural damage
  - GC Permits: Louisiana GC License — active
  - NVIDIA Certs: 7 active certifications
  - FAA Certs: Private Pilot + Part 107 UAS
---
## Infrastructure Proximity
  - LUS Fiber: ~0.8 mi — 214 Jefferson St
  - LUS Power / Utilities: ~1 mi — 1314 Walker Rd
  - Atmos Energy: ~3 mi — 1818 Eraste Landry Rd
  - SLEMCO Electric: 2727 SE Evangeline Thruway
  - LFT Airport: adjacent — GPS 30.20529, -91.98760
  - Henry Hub: ~40 mi — Erath, LA
  - NVIDIA TX Manufacturing: ~4 hrs — Foxconn Houston / Wistron Fort Worth
  - Trappeys Cannery: 0.5 mi
  - Willow Glen: 60 mi — dedicated fiber (management traffic only, NOT InfiniBand)
---
## Cooling Architecture — Building
  - NVIDIA integrated cold plate CDU — direct-to-chip liquid cooling
  - 45C hot water output — liquid heat rejection to exterior dry coolers on concrete pad
  - 1 CDU pair — covers 10-rack single row
  - PUE target: 1.10
  - No CRAC units, no chiller plant, no raised floor
---
## Adjacent Parcels — Chag Street
  - 3 adjacent parcels, approx 0.60 acres total
  - 3 blighted structures targeted for Phase 1 demolition
  - Ground-mount First Solar TR1 panels + exterior cooling infrastructure on cleared parcels
  - Pod deployment zone: 3 ADC 3K pods side by side adjacent to building
---
## GPS & References
  - GPS: 30.21975N, 92.00645W
  - Land debt: $5,000. Effectively debt-free.
  - Role: Backup NOC for Willow Glen, edge compute, R&D staging, Scott HQ
  - Half mile from Trappeys. 60 miles from Willow Glen.
  - Blueprints: 6-sheet set at adc3k.com/blueprints-marlie
  - Sheets: E-001 (electrical SLD), C-001 (cooling), S-001 (site plan), A-001 (floor plan), P-001 (power dist), L-001 (solar layout)
*[Child: 04 — Government Funding Stack]*
> Marlie I was designed around the incentives — not retrofitted to qualify.
---
## Federal: One Big Beautiful Bill Act (OBBBA)
  - Signed July 4, 2025
  - FEOC restrictions: Chinese/Russian/Iranian/North Korean supply chain = disqualified
  - Marlie I: Texas-manufactured NVIDIA hardware, 100% US ownership, Louisiana GC — fully compliant
  - $500M added to BEAD broadband program
  - Gulf OCS revenue raised to $650M/year through 2034
  - $500B Stargate AI program — Marlie I FEOC-clean structure qualifies
---
## Federal: BEAD Broadband Program
  - LUS Fiber ~0.8 miles from site
  - Marlie I connection accelerates BEAD eligibility for City of Lafayette
---
## State: Louisiana Act 730
  - Effective July 1, 2024
  - 20-year state/local sales & use tax rebate on qualifying AI factory equipment
  - 10-year renewal option (30 years total)
  - Qualification: $200M+ capital investment + 50+ permanent jobs
  - Direct Payment Number eliminates tax liability on GPU hardware
  - Stackable: Quality Jobs Program (6% payroll rebate, 10yr) + LED FastStart (free workforce training)
> 100% US ownership. Texas-manufactured NVIDIA hardware. Louisiana-licensed GC. Zero foreign entity involvement. Marlie I is not just eligible — it is the ideal candidate.
*[Child: 05 — Infrastructure Partners]*
> Every infrastructure partner is not a vendor. They are a node in the same network.
---
## LUS Fiber
  - 214 Jefferson St, Lafayette, LA 70501 — ~0.8 miles from Marlie I
  - Municipal gigabit network — city-owned, no incumbent telco gatekeeping
  - What LUS Fiber gains: anchor industrial fiber customer + BEAD backhaul justification for SE Evangeline corridor
---
## LUS Power / Utilities
  - 1314 Walker Rd, Lafayette, LA 70506 — ~1 mile
  - MARLIE I is off-grid by design (Bloom SOFC primary). LUS Power = emergency backup only.
  - Grid not used for consumption. No sell-back at MARLIE I.
---
## Atmos Energy — Natural Gas
  - 1818 Eraste Landry Rd, Lafayette, LA 70506 — ~3 miles
  - Fuel supply for Bloom SOFC primary generation — 40 units, 10 MW installed
  - Henry Hub benchmark (Erath, LA, ~40 mi) — fuel costs locked to most competitive gas price on earth
  - What Atmos gains: long-term industrial contract, high-volume predictable load, rate stability
---
## SLEMCO Electric
  - 2727 SE Evangeline Thruway — same corridor as Marlie I
  - Emergency backup only
---
## Lafayette Regional Airport (LFT)
  - GPS: 30.20529, -91.98760 — adjacent to Marlie I site
  - ADC3K: FAA Private Pilot Certificate + Part 107 Remote Pilot Certificate
  - Commercial UAS operations: inspection, survey, logistics from day one
  - What LFT gains: active commercial Part 107 operator on the doorstep
---
## City of Lafayette / Louisiana Economic Development (LED)
  - Act 730 qualified — 20-year equipment tax exemption
  - OBBBA compliant — FEOC-clean, Texas-manufactured, Louisiana GC
  - 50+ permanent jobs required for Act 730 certification
  - Lafayette becomes home to Louisiana's first Rubin-class AI factory
  - Hub of ADC3K Louisiana AI Network — three sites planned
---
## Bloom Energy — Primary Power Generation
> 40 Bloom SOFC units. 10 MW installed capacity. Natural gas to 800V DC — no inverter, no rectifier. PRIMARY power for MARLIE I building and all 3 pods.
  - Building downstairs: 10 units — 2,500 kW generation
  - Pod 1: 10 units — 2,500 kW generation
  - Pod 2: 10 units — 2,500 kW generation
  - Pod 3: 10 units — 2,500 kW generation
  - Total: 40 units x 250 kW = 10,000 kW (10 MW)
  - 54% electrical efficiency — best-in-class for on-site generation
  - 800V DC direct output — native to DSX power bus, no conversion loss
  - No battery array required for steady-state — Bloom provides continuous base load
  - 90-day delivery window — no grid interconnect required to operate
---
## Eaton — Power Distribution
  - Eaton Beam Rubin DSX: 800V DC native power distribution
  - Eaton xStorage: 600 kWh LFP battery — ride-through bridge, ATS, millisecond switchover
  - Contact made post-GTC 2026
---
## First Solar — Renewable Energy
  - First Solar Series 7 TR1 panels — $1.1B factory in New Iberia, LA (~30 mi)
  - 300 kW: pod roofs + ground mount on cleared Chag Street parcels
  - Note: No solar on main building roof — tree coverage
  - LOCKED American-made partner. FEOC-clean.
---
## Power Stack — MARLIE I (Locked)
> Bloom SOFC is PRIMARY. Grid is NEVER used for consumption at MARLIE I.
  - Layer 1 (Offset):   Solar — 300 kW — First Solar TR1 — pod roofs + Chag Street ground mount
  - Layer 2 (Primary):  Bloom SOFC — 40 units — 10 MW — 800V DC direct — gas in, DC out
  - Layer 3 (Bridge):   LFP Battery — 600 kWh Eaton xStorage — millisecond ATS — ride-through
  - Layer 4 (Emergency): Diesel genset — hurricane insurance — on-site fuel reserve
  - Layer 5 (Never):    Grid — emergency backup only — not used for consumption — no sell-back
*[Child: 06 — ADC3K Credentials]*
> Scott Tomsu — Owner/Operator — ADC3K (Advantage Design Construction) — Lafayette, LA
---
## Certifications
  - Louisiana General Contractor License — active — eliminates 10-15% GC markup, single accountability
  - 7 NVIDIA Certifications — AI infrastructure design, GPU compute deployment, NVIDIA partner program
  - FAA Private Pilot Certificate
  - FAA Part 107 Remote Pilot Certificate (commercial UAS)
  - CompTIA A+ — earned late 1990s
  - CompTIA Network+ — earned late 1990s
---
## Background
  - 20 years underwater robotics / ROV — Gulf of Mexico oil and gas industry
  - Systems at depth, under pressure, hostile environments — zero tolerance for failure
  - AI factory ops demand the same: continuous uptime, redundant systems, immediate fault response
  - Built 1201 SE Evangeline Thruway himself — 20 years standing, hurricane-proven
---
## Why This Matters
  - No third-party GC — Scott pulls permits, hires trades, executes buildout directly
  - No third-party NVIDIA integrator — 7 certifications = receive, rack, power on
  - Revenue from day one — no markup, no delay, no middlemen
  - Field-hardened systems thinking — not finance, not software — infrastructure operations
*[Child: 07 — Louisiana AI Network: Multi-Site Vision]*
> We are not building an AI factory. We are building a network.
---
## Phase 1 — MARLIE I (Active)
  - Location: 1201 SE Evangeline Thruway, Lafayette, LA 70501
  - Target: H2 2026 operational
  - Building: 24 x 40 ft, 2 floors — downstairs compute (10 racks, single row), upstairs NOC
  - 3 ADC 3K pods on adjacent Chag Street parcels (cleared, prepped)
  - Total: 40 NVL72 racks, 2,880 Rubin GPUs, 40 Bloom SOFC units, 10 MW generation
  - Purpose: home base — cash flow, credibility, playbook for Phases 2 and 3
  - Activation: NOW — investor and infrastructure partner outreach active
---
## Phase 2 — Site Two (In Development)
  - Location: TBD — ADC3K Louisiana Network
  - Funded by Marlie I cash flow — no external fundraising required
  - Playbook: written. Infrastructure relationships: established. Hardware: understood.
  - Activation trigger: Marlie I reaches revenue threshold -> Site Two deploys
---
## Phase 3 — Site Three (In Development)
  - Location: TBD — ADC3K Louisiana Network
  - Completes hub-and-spoke Louisiana AI architecture
  - Combined: enterprise + government + city infrastructure at statewide scale
  - Three sites. One network. One operator.
  - Activation trigger: Site Two operational -> Site Three deploys
---
## Partner Gains Across the Full Network
  - LUS FIBER: Anchor industrial fiber customer + BEAD backhaul justification
  - ATMOS GAS: Long-term industrial gas contract — high-volume predictable load for Bloom fuel supply
  - LFT AIRPORT: Active Part 107 commercial UAS on the doorstep
  - CITY / LED: Louisiana's first Rubin-class AI factory — Act 730, OBBBA, 50+ jobs, Lafayette on national map
ADC3K is not asking the city for a favor. ADC3K is inviting Lafayette's infrastructure partners to build the city's next chapter with us. Every site we add is another node in Lafayette's economic future.
---
## KLFT 1.1 — First Operational Remote Node
  - KLFT 1.1 (Gulf Coast Emergency Drone Deployment Hub) — first remote edge node managed from Marlie I NOC
  - KLFT site: Lafayette Regional Airport adjacent — Part 107 UAS operations hub
  - Command: SkyCommand fleet management, mission dispatch, live video feed
  - Drone platform: Skydio X10 + Skydio Dock (autonomous launch, charge, relay)
  - Edge compute: ADC 3K pod at KLFT site — on-site inference, video processing
  - NOC link: Marlie I aggregates KLFT telemetry, archives incidents, coordinates multi-site missions
  - Revenue model: government/emergency services SaaS + per-mission fees
---
## ADC 3K Pod Deployment Geography — Natural Gas Pipeline Map
ADC 3K pods deploy along Louisiana's natural gas pipeline corridor. Each pod connects to Marlie I via fiber or cellular backhaul. Bloom SOFC in every pod: gas in, tokens out — no grid required.
  - Henry Hub corridor (~40 mi): Erath, LA — Vermilion Parish gas hub — high-density pipeline node
  - Gulf Coast industrial corridor: refineries, LNG terminals, petrochemical plants — captive ADC pod customers
  - New Iberia (Site 2 candidate): solar factory + industrial port + pipeline access
  - Lake Charles / Cameron Parish: LNG export terminals — security/monitoring pod deployment
  - Morgan City: offshore supply base, pipeline terminus — SAR + industrial ADC pod
---
## Ground Zero — Media Arm of the Louisiana AI Network
Ground Zero (@GroundZero-ai) is the YouTube documentary arm that translates ADC ecosystem operations into public-facing content.
  - Audience 1 — General public: AI infrastructure explained at civilian level
  - Audience 2 — Technical/industry: GPU specs, deployment architecture, ROI models
  - Audience 3 — Investor/government: live proof-of-concept — Marlie I, ADC 3K pods, KLFT operations
  - ADC Insider Series: 8 planned episodes documenting MARLIE I buildout, ADC 3K pod deploy, KLFT launch
  - Monetization: YouTube revenue + sponsorships + investor lead generation + NVIDIA partner content
  - Status: EP001 live (private), EP002 in pipeline. Channel: @GroundZero-ai
Ground Zero turns every infrastructure milestone into investor-grade content. The construction of Marlie I IS the content strategy.
---
## MARLIE I Key Specs — Reference
  - 40 NVL72 racks (10 building downstairs + 10 per pod x 3 pods), 2,880 GPUs
  - Building: 24 x 40 ft, single-row 10-rack layout downstairs, NOC upstairs
  - 3 ADC 3K pods: single-row 10-rack layout, 40 ft containers, Chag Street parcels adjacent
  - Power: 40 Bloom SOFC units, 10 MW primary generation, 800V DC native
  - Fiber: LUS (0.8 mi) + dedicated to Willow Glen (60 mi, management only)
  - 0.5 mi from Trappeys. 60 mi from Willow Glen.
*[Child: 08 — Contact & Next Steps]*
## ADC3K — Advantage Design Construction
  - Owner/Operator: Scott Tomsu
  - Address: 1201 SE Evangeline Thruway, Lafayette, LA 70501
  - Email: SCOTT@ADC3K.COM
  - Phone: 337-780-1535
  - Web: www.adc3k.com
---
## Next Steps
  - Infrastructure partner meetings: LUS Fiber, Atmos Energy, LUS Power, LFT Airport
  - Louisiana Economic Development — Act 730 pre-qualification
  - NVIDIA partner program — NVL72 procurement pipeline
  - Investor term sheet discussions
  - Phase 1 buildout kickoff — 6 month deploy timeline
---
> The federal money is flowing. The hardware is in production. The site is ready. The only question is who is at the table when Marlie I goes live.
*[Child: 09 — Financial Architecture & ROI]*
> This is not an AI factory. This is a money machine. Every watt generates revenue. Every dollar goes to compute. The comparison is not close.
---
## Capital Stack
  - Infrastructure raise: ~$1.17M — covers facility buildout (electrical, cooling, fiber, power distribution, commissioning)
  - GPU hardware financed separately: equipment financing + NVIDIA Capital programs + SBA facilities
  - EBITDA figures below = facility-level operating cash flow
  - Full investor pro forma with hardware financing and debt service available upon request
---
## MARLIE I vs Legacy AI Factory — Key Comparison
  - PUE: Legacy 1.4-1.8 (40-80% wasted) vs MARLIE I 1.10 (liquid-cooled, best-in-class)
  - Energy cost: Legacy $0.10-0.18/kWh national avg vs MARLIE I $0.058-0.068/kWh (Bloom SOFC on Henry Hub gas)
  - Cooling: Legacy air (CRAC units, chillers) vs MARLIE I 100% direct-to-chip liquid
  - Revenue per rack per year: Legacy $200K-$500K (colo) vs MARLIE I $3M-$5M+ (AI compute)
  - Operations: Legacy 20-50 FTE manual ops vs MARLIE I 3-5 FTE Mission Control AI
  - On-site generation: Legacy none (grid dependent) vs MARLIE I 40 Bloom SOFC units, 10 MW
  - Domestic content: Legacy mixed overseas vs MARLIE I 100% USA — OBBBA compliant
---
## MARLIE I Configuration
> 40 NVL72 racks — 2,880 Rubin GPUs — 5,200 kW IT — 10 MW Bloom generation
  - Building downstairs: 10 racks, 720 GPUs, 1,300 kW IT — single-row layout, same as pod
  - Building upstairs: NOC only — no compute racks
  - Pod 1: 10 racks, 720 GPUs, 1,300 kW IT
  - Pod 2: 10 racks, 720 GPUs, 1,300 kW IT
  - Pod 3: 10 racks, 720 GPUs, 1,300 kW IT
---
## Revenue Model — AI Compute Rental (Conservative Basis)
Rate basis: $6/GPU/hr base case (H100 spot: $2.50-$3.50/hr; Rubin delivers 2.5x FP4 density and 22 TB/s HBM4 bandwidth — premium tier justified). At $8/GPU/hr mid estimate, Phase 3 gross reaches $151.6M.
### Phase 1 — Building Downstairs (720 GPUs, 10 Racks)
  - 720 GPUs online — building downstairs only
  - 40% utilization (ramp year): 720 x $6 x 8,760 x 0.40 = $15.2M gross
  - 65% utilization (stabilized): 720 x $6 x 8,760 x 0.65 = $24.7M gross
  - OPEX at 65%: ~$2.8M (Bloom fuel + staffing + maintenance)
  - EBITDA at 65%: ~$21.9M
### Phase 2 — Building + Pod 1 (1,440 GPUs, 20 Racks)
  - 1,440 GPUs online — building + Pod 1
  - 65% utilization: 1,440 x $6 x 8,760 x 0.65 = $49.3M gross
  - OPEX: ~$4.5M
  - EBITDA: ~$44.8M
### Phase 3 — Full Footprint (2,880 GPUs, 40 Racks)
  - 2,880 GPUs online — building + all 3 pods
  - 75% utilization at $6/hr: 2,880 x $6 x 8,760 x 0.75 = $113.7M gross
  - 75% utilization at $8/hr: 2,880 x $8 x 8,760 x 0.75 = $151.6M gross
  - OPEX: ~$7.0M
  - EBITDA at $6/hr: ~$106.7M
  - EBITDA at $8/hr: ~$144.6M
---
## Power Resilience — 5 Independent Layers
> Bloom SOFC is PRIMARY. The grid is never used for consumption at MARLIE I.
  1. Solar (Offset): 300 kW — First Solar TR1 — pod roofs + Chag Street ground mount
  1. Bloom SOFC (Primary): 40 units x 250 kW = 10 MW — 800V DC direct — gas in, DC out — 54% efficiency
  1. LFP Battery (Bridge): 600 kWh Eaton xStorage — millisecond ATS — ride-through
  1. Diesel Genset (Emergency): on-site fuel reserve — hurricane insurance — zero production dependency
  1. Grid (Never): LUS emergency backup only — not used for consumption — no sell-back at MARLIE I
Zero single points of failure. 5 independent power layers. Bloom headroom: ~4,280 kW above full facility draw.
---
## Power Economics
  - Bloom SOFC effective cost: $0.058-0.068/kWh (fuel + maintenance, Henry Hub gas basis)
  - IT load: 5,200 kW — facility total at PUE 1.10: ~5,720 kW
  - Bloom generation: 10,000 kW — headroom buffer: ~4,280 kW
  - Annual power cost at Phase 3 / 75% utilization: ~$2.4M
---
## Investor Benefits
  - Reserved bandwidth: GPU compute access during off-peak hours proportional to investment tier. Estimated value: $50K-$500K/month compute credit.
  - Early mover rate lock: investors before first rack goes live receive locked GPU rental rates below market for 24 months
  - Single operator: Scott pulls GC permits, handles NVIDIA integration, runs Mission Control — no markup, no middlemen, revenue from day one
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/5a788f09-7e31-81eb-a3dc-00039a1662d6/9e682da1-85a0-44a9-94e4-61045a297666/Store_Front_Pic.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466Y5C6SC5I%2F20260403%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260403T212038Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEML%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJGMEQCIBs03fzMhOoHuRdOC9xLA8Rqu%2BfJYJw2uS%2FVXFW9r3bsAiAjiW7bW79APPc8S8lxzj8c66TTW4YnPyFmsOav18GauyqIBAiL%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIM3tJizb1r1nbaUNDQKtwDUuWkeLu0evkPEY%2B%2BU7ZCSbMerfKgS8AxF5YYx5QfApOfNZjSb7%2FfjfZ7TvWYXysTrmpNfy4znm0%2B99IFFjbiRCzAoyLJFMVBBYjOb2vm0bQTjGYLZizhe2g2t7aAUndSZBVRvON6iu%2FDUsFHstcfeu35jiA8B9sbK4k4VUkSrNhJj0KsNBiZHCV9L22bbxOtqKySvXs6boFY8iKJjYyszE29zwt7he%2Bd3bB%2BP0SDRtbhX5q0Q3qHwKFf3GiGwcEfGFcLSFlbKEbQg6ZWKYE7Z1%2B%2BPRcBlmIlmdNpltqHFdhn7L4SRVdMSGoZASkGtjsPaiZgN23JDGRrtZqjMe%2Bqdmj95Xubp7bcJ1DuKRsw1Xn1I4NmQL5vK86%2Bef%2Fh5923PY7JXVuE%2Bo33xgSLbrQsnMdxq4Rcf0sxe8bQkm39%2BN01cHbCJmk8X6LlDhS9%2FJAqn4r55PrxvvdeGAM5z7KVYTjJKoVemwp0AHzVeN7DKK0J%2FHyVf%2FFztwJd5yFx%2FB7RCoY4NJHu5DLzoezRN6t4mZlOhTtcBcXYJFqJmDZ8i%2FPqbA6gICYclz4LFwit3KVrUdMIoD91AhecHmG1%2BHbpo%2FSAkreZ1OFZY%2F0P%2F1bplgcV9x3k2rx8Q4qbKTwwm4TAzgY6pgG8AnmM0NyzyAUt4CbRL79JASKB3s%2BCeC2LsLqL3L7nftdWHFmeG3vNrcamhjj6jDwiUMrssXW%2Fadc34C5jbeP3kPk7aIdArqL9sAXXNGwioq%2Fk%2FfoO5wNsc64baho3D2xSP%2FBza7tV4PJRYx4iAthzHbqhYbGbSpwCyBYiG8VaFwp%2BMykDXy6ujI1N0EDhTQaaYo2XD03mQdQpXgxyqOnsGRKVgfz2&X-Amz-Signature=cbe2cac8ee5544fdae2048cad00ceee29e86b544f57df3115a30cbfd56f17797&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)