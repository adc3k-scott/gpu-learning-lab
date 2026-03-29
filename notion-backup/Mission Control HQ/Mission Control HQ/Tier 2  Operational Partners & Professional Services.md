# Tier 2 — Operational Partners & Professional Services
*Notion backup — 2026-03-28*

> Tier 2 partners BUILD, INSTALL, CONNECT, and MAINTAIN the facility. Without them, Tier 1 hardware sits in crates.
Tier 1 = Hardware you can't run without (NVIDIA, Cat, Eaton, First Solar)
Tier 2 = People who build, install, and operate it (THIS PAGE)
Tier 3 = Government & institutional (LED, DOE, UL Lafayette, City Council)
---
# Engineering Services
These are the licensed professionals who stamp drawings, certify systems, and get permits approved. Without them, nothing gets energized.
## Licensed Electrical PE — 800V DC System Design
Scope: Design and stamp the 800V DC power distribution system. Solar string layout, genset interconnect, Beam Rubin DSX integration, arc flash study, short circuit analysis, NEC compliance.
- Must have DC power experience — 800V DC is not standard commercial electrical. Most PEs do 480V AC. Find one who has done utility-scale solar or EV charging infrastructure.
- Louisiana PE license required — stamps must be valid in-state
- Eaton may provide design assist — Beam Rubin DSX comes with application engineering. PE still needed to stamp and take liability.
- [ ] Contact Eaton rep — ask if they have preferred PE firms for DSX projects in Louisiana
- [ ] Search Louisiana PE board for firms with DC power / renewable energy experience
- [ ] Budget: $50,000-80,000 for full electrical engineering package
## Fire Protection Engineer (FPE) — Suppression & Detection Design
Scope: Design VESDA-E aspirating detection + Novec 1230/FM-200 clean agent suppression for compute area. Room integrity testing. AHJ coordination. Insurance carrier approval.
- Must understand lithium battery fire risks — NVL72 racks have UPS batteries. Clean agent alone may not be sufficient. FPE must address thermal runaway scenarios.
- Fike and Xtralis (Honeywell) both offer design services — but independent FPE stamps the drawings
- [ ] Identify FPE firms in Louisiana with compute facility / clean agent experience
- [ ] Budget: $25,000-40,000 for fire protection engineering package
## Structural Engineer — Roof Load Analysis
Scope: Verify all 4 Trappeys buildings can support rooftop solar. Phase 1 = Building #3 (63,300 lbs). Full campus = 316,500 lbs across 4 buildings. Seismic and wind load calcs (hurricane zone).
- First Solar TR1 panels are heavier than silicon — CdTe glass-glass construction. ~85 lbs per panel. 746 panels = 63,410 lbs on Building #3 alone.
- Historic buildings may have load restrictions — Trappeys is pre-1950s construction. Structural assessment is FIRST before any solar goes up.
- [ ] Get structural engineering firm — Lafayette area, commercial/industrial roof experience
- [ ] Budget: $15,000-25,000 for roof load analysis (all 4 buildings)
## Environmental Consultant — Permitting & Thermal Modeling
Scope: LDEQ LPDES permit application. Thermal discharge modeling (liquid cooling heat rejection). Brownfield assessment (former cannery — potential soil contamination). Noise study for gas gensets.
- Brownfield advantage — former industrial site means zoning is already M2. But brownfield also means potential remediation costs. Environmental Phase I/II assessment tells you what is in the ground.
- [ ] Engage environmental firm — Phase I ESA before closing on property
- [ ] Budget: $20,000-40,000 (Phase I: $5K, Phase II if needed: $15-35K)
---
# Construction & Installation
## Solar EPC Contractor — Panel Installation
Scope: Engineer, procure (mounting hardware), and construct the rooftop solar array. Phase 1: 746 panels on Building #3. Full build: 3,731 panels across 4 buildings. Includes racking, wiring, combiners, commissioning.
- First Solar may have preferred EPC partners — ask modulesales@firstsolar.com for Louisiana commercial installers with CdTe experience
- Must be licensed in Louisiana (LLR contractor license, electrical license)
- Look for NABCEP-certified installers — industry gold standard
- [ ] Ask First Solar for Louisiana EPC referrals
- [ ] Get 3 bids for Phase 1 installation (746 panels, Building #3)
## General Contractor — Building Modifications
Scope: Building penetrations (cable runs, cooling piping, exhaust). Concrete pad for genset + switchgear yard. Door modifications. Interior buildout for compute area (vapor barrier, insulation, flooring). Loading dock prep.
- Historic building considerations — if pursuing 45% historic tax credits, all exterior modifications must comply with NPS Standards. GC must understand Secretary of Interior guidelines.
- Lafayette-based preferred — local knowledge, relationships with inspectors, fast response
- [ ] Identify 3 commercial GCs in Lafayette with industrial/warehouse renovation experience
## Licensed Electrical Contractor — Installation
Scope: Install everything the Electrical PE designs. Conduit runs, wire pulls, switchgear installation, PDU mounting, genset connection, utility interconnect, grounding grid. Separate from solar EPC (different skill set).
- 800V DC experience is rare — most commercial electricians work 480V AC. Need a shop that has done industrial DC, mining, or EV charging infrastructure.
- Budget from procurement matrix: $100,000-150,000 for Phase 1 electrical labor
- [ ] Find electrical contractors with DC power experience in Louisiana
---
# Connectivity & Networking
## Dark Fiber / Backbone Provider
Scope: Dedicated fiber connecting Trappeys to MARLIE I (0.5 mi), and long-haul backbone to Willow Glen (60 mi). LUS Fiber handles last-mile metro. Need dark fiber or lit services for inter-site fabric and internet transit.
- LUS Fiber — municipal fiber, 0.8 mi from site. Metro connectivity + sell-back grid interconnect. Part of Tier 1 (city relationship).
- Zayo / Lumen / AT&T — long-haul dark fiber for Trappeys to Willow Glen backbone. Zayo has Louisiana fiber presence.
- Starlink Business — backup/redundant internet. Not for compute fabric, but for management plane failover.
- [ ] Check Zayo fiber map for Lafayette coverage
- [ ] Get LUS Fiber commercial service quote for Trappeys address
---
# Security & Compliance
## Physical Security Integrator
Scope: Access control (badge readers, biometric), CCTV (AI-powered analytics), perimeter fencing, vehicle barriers. Required for NVIDIA NCP certification — physical security is an audit item.
- NVIDIA Metropolis compatible cameras preferred — runs on Jetson edge compute. Same stack as KLFT. One vendor, one platform.
- [ ] Identify security integrators in Acadiana — must support IP-based access control + AI video analytics
## Cybersecurity / SOC Provider
Scope: SOC-2 Type II compliance (required for enterprise customers). Network security monitoring. Penetration testing. Incident response plan. Required for NCP certification path.
- Can start with managed SOC service — do not need in-house team for Phase 1
- NVIDIA BlueField DPUs handle infrastructure-level security — but still need compliance framework and monitoring
- [ ] Research managed SOC providers with compute facility experience
---
# Financial & Legal Services
## Equipment Financing / Leasing
Scope: Finance major equipment (gensets, switchgear, UPS) to preserve cash for site acquisition and NVIDIA hardware allocation. Explore vendor financing programs.
- Cat Financial — built-in financing for all Caterpillar equipment. Lease or loan. Louisiana Cat handles everything.
- Eaton Capital — Eaton offers equipment financing for power infrastructure. Ask during Beam Rubin engagement.
- SBA 504 loan — up to $5.5M for equipment + real estate. 10% down, 25-year term. Perfect for site acquisition + Phase 1 buildout.
- [ ] Ask Louisiana Cat about Cat Financial terms for prime-rated gas genset
- [ ] Research SBA 504 lenders in Lafayette (LEDA may have contacts)
## Insurance & Bonding
Scope: Builder's risk (during construction), general liability, professional liability (E&O), property insurance, equipment breakdown, cyber liability. Required before any construction begins and before any customer workloads.
- Compute facility insurance is specialized — standard commercial property will not cover $2M+ of GPU hardware. Need a broker who understands technology infrastructure.
- NVIDIA may require minimum coverage levels for NCP certification
- [ ] Find insurance broker with AI compute / technology infrastructure experience
## Legal Counsel
Scope: Entity structure (LLC vs C-Corp for investor readiness), vendor contracts, lease/purchase agreement for Trappeys, Act 730 application, ITEP filing, historic tax credit NPS applications, customer MSAs, IP protection.
- Need two types: (1) Louisiana real estate/tax attorney for property + incentives, (2) technology/IP attorney for customer contracts + NVIDIA agreements
- [ ] Identify Louisiana attorneys with LED incentive program experience (Act 730, ITEP)
---
# Workforce — First Hires
From ADC 3K Master Task Tracker — these are the first three hires before go-live.
## Site Manager / Ops Lead
- First hire. Owns facility operations, vendor relationships on-site, safety, scheduling.
- ROV industry background ideal — Lafayette has hundreds of experienced remote operations supervisors. Same skillset: complex equipment, safety-critical, 24/7 ops.
## 2x AI Compute Technicians
- Rack, cable, monitor, troubleshoot GPU servers. Liquid cooling maintenance. Network fabric.
- UL Lafayette pipeline — CS/EE students, LED FastStart training program (FREE customized training). This is why the university partnership matters.
- [ ] Write job descriptions for all 3 roles
- [ ] Contact LED FastStart for customized training program design
---
# Tier 2 Action Summary
23 action items above. Priority order:
1. Structural engineer — nothing happens until roof loads are verified
1. Environmental consultant — Phase I ESA before closing on property
1. Electrical PE — 800V DC design is longest engineering lead time
1. Legal counsel — entity structure + incentive applications need to start in parallel
1. Insurance broker — builder's risk needed before construction begins
1. Everything else — sequences after engineering designs are done

Estimated Tier 2 budget (engineering + services, NOT equipment): $300,000-500,000
This is on top of the $1.1-1.7M Phase 1 equipment budget in the procurement matrix.
---
> POST-GTC 2026 UPDATE (2026-03-23) -- Key Tier 2 changes driven by NVIDIA shipping complete racks and Eaton as 800V DC partner.
## Tier 2 Updates Post-GTC 2026
- Electrical PE scope updated: Eaton Beam Rubin DSX provides application engineering + design assist. PE still needed to stamp drawings, but engineering workload reduced. Budget may decrease 20-30%.
- CDU procurement REMOVED from Tier 2: NVIDIA ships liquid-cooled NVL72 racks complete with CDU. No separate Vertiv/CoolIT procurement for main racks.
- Louisiana Cat Financial available for genset financing -- reduces upfront capital needs for Layer 2 power. Ask Spencer Landry (985-498-9336).
- Eaton Capital available for power infrastructure financing -- reduces upfront capital for 800V DC distribution. Ask during Beam Rubin engagement.
- SBA 504 loan still the best path for site acquisition + Phase 1 buildout (.5M, 10% down, 25-year term).
- Workforce note: LED FastStart is FREE customized training. UL Lafayette pipeline stronger than ever -- Dr. Ramesh Kolluru (new Interim President) is a CS PhD and R1 builder. No GPU infra at UL means they NEED this partnership.
- Multi-site scope: Tier 2 vendors now cover Trappeys + MARLIE I + Willow Glen. Same engineering firms, larger scope, better pricing.