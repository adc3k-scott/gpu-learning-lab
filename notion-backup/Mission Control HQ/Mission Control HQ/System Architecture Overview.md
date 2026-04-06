# System Architecture Overview
*Notion backup — 2026-04-06*

> This is the master cross-reference document for all ADC infrastructure projects. Read this first to understand how MARLIE I, ADC 3K pods, KLFT/SkyCommand, New Iberia Solar, and the City of Lafayette connect as one ecosystem.
---
# ADC Infrastructure Ecosystem — How It All Connects
Advantage Design Construction operates an integrated AI infrastructure ecosystem across South Louisiana. Every project is designed to interconnect. MARLIE I is the permanent command center. ADC 3K pods are the deployable field units. KLFT/SkyCommand is the autonomous operations arm. New Iberia Solar is the renewable energy partner. The City of Lafayette — its power grid, fiber network, and airport — is the foundation that makes all of it possible.
---
## MARLIE I — Lafayette AI Factory (Base Station)
> MARLIE I is the permanent headquarters and primary compute facility. It is NOT a pod — it is a building-based AI factory at 1201 SE Evangeline Thruway, Lafayette LA.
- Location: 1201 SE Evangeline Thruway, Lafayette, Louisiana
- Role: HQ + NOC + primary AI compute + customer operations center
- Hardware: NVIDIA Vera Rubin NVL72 racks (H2 2026 deployment target)
- Cooling: Cold plate liquid cooling (CDU) with fan-assisted thermal management — direct-to-chip liquid, no immersion
- Power: LUS grid (primary) + Bloom Energy fuel cells (supplemental) + diesel N+1 (emergency backup)
- Connectivity: LUS Fiber — carrier-grade municipal fiber, already in place
- NOC function: Remotely monitors and manages all ADC 3K pod deployments across Louisiana — no on-site staff at remote sites
MARLIE I cooling note: Cold plate CDU with fans represents the current state-of-the-art public-facing approach — proven, code-compliant, and well-understood by inspectors and lenders.
---
## ADC 3K — Deployable Edge Compute Pods
> ADC 3K pods are the manufactured containerized product line. Each pod is a self-contained, site-agnostic AI compute module deployed to remote Louisiana sites. All pods are managed remotely from MARLIE I NOC.
- Form factor: 20-ft ISO shipping container — fully integrated, ships complete
- Cooling: FULL IMMERSION (Engineered Fluids EC-110, single-phase) — no HVAC, no fans, no external cooling towers
- Why immersion for Louisiana: Ambient temperatures regularly exceed 95°F with 90%+ humidity. Traditional air and even cold plate systems struggle with Louisiana climate. Immersion eliminates ambient air from the cooling equation entirely — GPU thermal performance is identical whether deployed in New Orleans in August or Shreveport in January.
- Power: 480V AC active + 800V DC pre-wired. Bloom Energy fuel cell integration port standard on all units.
- Deployment trigger: Natural gas pipeline accessibility. Pod sites are selected where Gulf Coast natural gas infrastructure provides reliable, low-cost fuel for on-site Bloom Energy generation.
- Remote management: All pods networked back to MARLIE I NOC. No permanent on-site staff required.
- First deployment: Trappeys Cannery — 1201 SE Evangeline Thruway. Metal warehouse structure. Pods drop in.
- Dielectric fluid: Engineered Fluids EC-110. NEVER reference 3M Novec — discontinued.
---
## Louisiana Deployment Geography
ADC 3K pods follow the natural gas pipeline map. Louisiana has one of the densest natural gas distribution networks in the nation — the same infrastructure that powers the petrochemical industry also powers ADC pod sites. This gives ADC a cost and supply advantage that no out-of-state operator can match.
- Primary hub: Lafayette (MARLIE I + Trappeys — Phase 1)
- Expansion priority: Sites with existing natural gas service and industrial zoning along the I-10 corridor
- Gulf Coast coverage: Baton Rouge, Lake Charles, New Orleans, Houma-Thibodaux corridor
- Each pod site requires: natural gas service, three-phase electrical, broadband fiber, and basic security infrastructure
---
## KLFT / SkyCommand — Gulf Coast Emergency Drone Deployment Hub
> KLFT is not just an autonomous drone operations project. It is a Gulf Coast Emergency Drone Deployment Hub — AI-coordinated drone response for disasters, search and rescue, infrastructure inspection, and public safety operations across the Gulf Coast region, based at Lafayette Regional Airport.
- Location: Lafayette Regional Airport (KLFT) — Lafayette, Louisiana
- Platform: Skydio X10 + Skydio Dock (committed). DJI removed — Countering CCP Drones Act regulatory compliance.
- Primary mission: Gulf Coast emergency response — hurricanes, flooding, industrial incidents, search and rescue
- Secondary missions: Infrastructure inspection (pipelines, towers, bridges), precision agriculture, commercial logistics
- AI compute: Jetson Orin NX 16GB at dock (edge inference). NVIDIA L40S (Phase 3 inference node, networked to MARLIE I).
- Integration: MARLIE I NOC provides remote fleet management. SkyCommand platform scales to multi-site, multi-vehicle ops.
- Lafayette connection: KLFT is a city asset. This project keeps AI drone infrastructure locally owned and operated — not contracted to out-of-state platforms.
---
## New Iberia Solar — Renewable Energy Partner
> A new solar manufacturing facility has been built in New Iberia, Louisiana (Iberia Parish, ~30 miles from Lafayette). ADC is committed to supporting this local industry as the renewable energy transition accelerates.
- New Iberia, Louisiana — Iberia Parish, approximately 30 miles southwest of Lafayette
- Significance: Local solar manufacturing capability means ADC can source panels regionally — shorter supply chain, economic development impact, alignment with Louisiana energy transition goals
- Integration path: ADC 3K pod sites with roof or ground space can incorporate solar arrays sourced from New Iberia as supplemental generation — reducing natural gas consumption and qualifying for renewable energy credits
- MARLIE I application: Rooftop or adjacent ground-mount solar at 1201 SE Evangeline Thruway — supplements Bloom Energy + LUS grid
- Narrative value: Every investor deck and financing proposal should reference New Iberia solar as evidence of Louisiana-first supply chain commitment
---
## City of Lafayette — Infrastructure Foundation
Every ADC project is designed around Lafayette's existing infrastructure advantages. This is not incidental — it is strategic. Lafayette has built public infrastructure that most cities its size do not have, and ADC is purpose-built to leverage it.
- LUS (Lafayette Utilities System): Municipal electric and fiber — low-cost power, carrier-grade fiber, local control
- LUS Fiber: Direct fiber connectivity already in place at MARLIE I site — no construction required
- Lafayette Regional Airport (KLFT): Municipal airport = city asset. KLFT/SkyCommand keeps drone AI infrastructure locally controlled
- University of Louisiana Lafayette: AI research pipeline, workforce development, potential compute tenant
- Economic incentives: ITEP, Quality Jobs, Enterprise Zone, LED FastStart — all available to ADC projects
- Goal: Lafayette becomes the regional hub for Gulf Coast AI infrastructure — not a branch office of a Dallas or Atlanta firm
---
## How the Projects Reinforce Each Other
- MARLIE I NOC manages all ADC 3K pod sites — more pods = more NOC revenue per fixed overhead
- MARLIE I NOC manages KLFT drone fleet — same NOC, multiple revenue streams
- ADC 3K pods at natural gas sites serve energy sector customers — same customers who benefit from KLFT pipeline inspection drones
- New Iberia solar panels on pod sites reduce energy cost across entire fleet
- Lafayette city partnerships create regulatory goodwill and preferred access to public infrastructure contracts
- Every project creates local jobs, local tax revenue, local infrastructure — reinforcing the city partnership narrative