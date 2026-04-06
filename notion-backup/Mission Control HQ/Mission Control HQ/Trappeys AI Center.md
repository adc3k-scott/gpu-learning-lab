# Trappeys AI Center
*Notion backup — 2026-04-06*

> THE CORE PROJECT. Solar AI factory at former Trappeys Cannery, Lafayette LA. 112,500 sq ft across 4 buildings. 2.05 MW First Solar rooftop. Water tower cooling. Site walked 2026-03-21 -- all buildings structurally sound.
GPS: 30.21356N, 92.00163W  |  Acquisition: ~$1M  |  Half mile from MARLIE I  |  30 mi from First Solar
---
# Live Pages (adc3k.com)
- /trappeys -- Landing page
- /trappeys-campus -- Photo tour (4 buildings)
- /trappeys-technology -- DSX stack + NVIDIA architecture
- /trappeys-university -- UL Lafayette partnership
- /trappeys-responders -- First responder drone ops
- /trappeys-investors -- Investment case
- /trappeys-plan -- Master plan (buildings, solar, phasing)
- /trappeys-dsx-prep -- DSX Air input package (copy-paste ready)
- /trappeys-presentation -- Pitch deck (28 slides)
- /trappeys-gallery -- 56 numbered site photos for reference
---
# Buildings -- 112,500 sq ft Total Rooftop
## Rear High Ground -- 37,500 sq ft
150 x 250 ft. Tallest building. Connects via walkway to brick building (roof torn off but walls + metal repairable). ~1,276 solar panels = 676 kW.
## Middle High -- 22,500 sq ft
75 x 300 ft. Same height as Rear High. Wooden beams, roof good. Ready for solar panels. ~765 panels = 406 kW.
## Middle Low -- 30,000 sq ft
100 x 300 ft. ~2 ft lower than Middle High. Roof good, metal good. Extensive gas piping + fire suppression piping already installed. Gas heaters, huge trunk line. Could be primary compute space with elevated floors. ~1,020 panels = 541 kW.
## Front Lower -- 22,500 sq ft (on the water)
75 x 300 ft. Has vat holes in concrete floor -- perfect for cable risers and cooling plumbing. River views, park visible across bayou. Some roof sections off. NOT compute space -- this is the showcase, partner hub, tour stop, investor wow moment. ~765 panels = 406 kW.
---
# Solar -- 2.05 MW First Solar Rooftop
3,827 First Solar Series 7 TR1 panels across all 4 rooftops. Panels manufactured 30 miles away in New Iberia. 550W each, 19.7% efficiency, 0.3%/year degradation (industry best). 30-year warranty. Superior in humidity (+4% vs silicon) -- perfect for Lafayette.
- 30% federal solar ITC + state credits -- government pays for most of it
- 800V DC solar-direct to DSX bus possible (97% efficiency vs 92% AC path)
- Plan: seal roofs > build platform/racking > mount panels
---
# Power -- 4-Layer Hierarchy
> Gas is PRIMARY. Solar is offset. Grid is sell-back only. We don't need the grid. We don't scare anybody.
1. Solar -- primary offset, rooftop arrays, First Solar panels
1. Natural Gas -- BACKBONE, carries main load 24/7, Henry Hub pricing
1. Diesel Gensets -- emergency, on-site fuel, pipeline-independent
1. Grid (LUS) -- SELL-BACK ONLY, excess goes back to grid, NOT a source
Gas confirmed on-site: trunk lines, city hub up the road, heaters throughout Middle Low.
---
# Water Tower -- Branding + Cooling
### Branding
THE landmark. First thing to paint. Dark navy blue. NVIDIA, ADC, First Solar, UL Lafayette, City of Lafayette logos. Visible from Evangeline Thruway/US 90. DO FIRST.
### Cooling (engineering innovation)
Repurpose as thermal buffer tank in liquid cooling loop. 15,000+ gallon elevated steel tank. Hot water from NVL72 racks pumps up, gravity-feeds cold water back down to CDUs (no pump needed on return). Tower is a giant radiator. Thermal mass = cooling UPS -- if pumps trip, gravity-feeds racks for 10-15 minutes.
100-year-old water tower repurposed as AI factory cooling infrastructure = magazine cover, NVIDIA case study material.
---
# Infrastructure Yard -- Concrete Pad
~28,000 sq ft heavy-duty concrete slab. NOT solar -- this is where the power plant goes.
- Natural gas gensets (backbone, 24/7)
- Transformer/switchgear yard (Eaton Beam Rubin DSX)
- Dry coolers (backup to water tower)
- Battery storage (future)
- Diesel emergency genset
- Visible from US 90 -- make it look professional, it's marketing
---
# Adjacent Infrastructure -- Already There
- LUS Pin Hook Substation (Curtis Rodemacher) -- right next door, established
- Public Works -- next door, city uses area for vehicle parking. Infrastructure zone, NOT residential.
- Gas infrastructure -- confirmed on site. Trunk line, city hub up the road.
- ATMOS Energy -- gas utility hub visible from Pinhook
- Water department -- across street on US 90
- City sewer -- across street, permitted discharge path
- KLFT airport -- control tower visible from site
- Park across the river -- visible from Front Lower
---
# Front Building -- Partner Hub
Restore brick facade. Convert loading bays to entrance/lobby. This is the FRONT DOOR.
- ADC -- operations, reception, visitor intake
- NVIDIA -- regional presence, certification lab
- UL Lafayette -- research liaison, student workspace
- First Solar -- O&M monitoring for rooftop arrays
- City of Lafayette -- smart city coordination
- Shared conference room -- partner meetings, investor tours
---
# Phased Buildout
- Phase 3 (start): 4 racks, 288 GPUs, 520 kW IT. Solar + 1 MW gas genset.
- Phase 4: 8 racks, 576 GPUs, 1 MW IT. Solar + 1.5 MW gas.
- Phase 5: 20 racks, 1,440 GPUs, 2.6 MW IT. Solar + 3 MW gas.
- Phase 6: 36 racks, 2,592 GPUs, 4.7 MW IT. Solar + 6 MW gas.
- Phase 7: 50+ racks, 3,600+ GPUs, 6.5+ MW IT. Full power yard.
---
# Incentive Stack
- 45% historic tax credits (federal 20% + state 25%) on rehab costs
- 30% federal solar ITC on panels
- 10-year property tax abatement (ITEP -- must file BEFORE groundbreaking)
- 20-year Act 730 sales tax exemption ($200M+, 50 jobs)
- NSF/DOE grants through UL Lafayette partnership ($28-55M+ potential)
- LED FastStart -- FREE customized workforce training
---
# Business Documents (in repo)
- business-model/vendor-procurement-matrix.md -- full US vendor matrix, primary + backup, Phase 1 budget ($1.1-1.7M)
- business-model/trappeys-electrical-architecture.md -- 800V DC electrical design
- business-model/token-economics.md -- raw cost $0.004/M, ADC pricing $0.20-$150/M, 95%+ margins
- business-model/power-economics.md -- Phase 1 $0.058-0.068/kWh
- business-model/capex-model.md -- capital expenditure model
---
# Vendor Strategy (in Notion)
Full vendor tiers under Vendor & Partner Strategy:
- Tier 1 -- must-have hardware (NVIDIA, Atmos, LUS, Cat, Bloom, Vertiv/CoolIT)
- Tier 2 -- operational partners & professional services (PE, FPE, structural, EPC, GC, legal, insurance)
- Tier 3 -- government & institutional (LED, City, UL Lafayette, DOE, EDA)
---
# Action Items
- [ ] Site LOI -- secure the property (~$1M)
- [ ] ITEP filing -- call LED (Kristin Johnson, 225-342-2083). Must file BEFORE groundbreaking.
- [ ] NPN registration -- 5-minute web form
- [ ] First Solar outreach -- modulesales@firstsolar.com / 419-662-6899
- [ ] UL Lafayette intro -- Dr. Ramesh Kolluru via LEDA warm intro
- [ ] Structural engineer -- roof load analysis before solar
- [ ] Environmental consultant -- Phase I ESA before closing
- [ ] City council presentation -- schedule meeting
- [ ] Water tower rendering -- Kontext edit of real photo
- [ ] DSX Air trial -- inputs ready at /trappeys-dsx-prep
---
Last updated: 2026-03-21. Full details in memory/projects/trappeys.md (24 KB).
*[Child: 01 -- Investment Thesis]*
> THE CORE PROJECT. Solar AI factory at former Trappeys Cannery, Lafayette LA. Proof of concept for the Louisiana AI network.
Content source: Main page above + memory/projects/trappeys.md
## Key Points
  - 112,500 sq ft across 4 buildings -- existing industrial structures
  - 2.05 MW First Solar rooftop array (3,827 panels, manufactured 30 mi away)
  - Acquisition ~$1M -- historic cannery, half mile from MARLIE I
  - 45-55% historic tax credits on rehab costs (federal 20% + state 25-35%)
  - Proof of concept: earn NVIDIA certification, validate vendor stack, then scale to Willow Glen
  - UL Lafayette anchor tenant -- workforce, grants, credibility
*[Child: 02 -- Hardware: NVIDIA Vera Rubin Platform]*
> NVIDIA technology stack for Trappeys -- same as Willow Glen, smaller initial scale.
## Platform
  - Vera Rubin NVL72 (72 GPUs/rack, 130 kW, liquid cooled)
  - Quantum InfiniBand (400 Gb/s per GPU)
  - Dynamo 1.0 (7x performance on same hardware)
  - Groq 3 LPX decode (5-10x revenue per MW)
  - Eaton Beam Rubin DSX (800V DC, co-designed with NVIDIA)
## Phased Rack Count
  - Phase 3 (start): 4 racks, 288 GPUs, 520 kW IT
  - Phase 5: 20 racks, 1,440 GPUs, 2.6 MW IT
  - Phase 7: 50+ racks, 3,600+ GPUs, 6.5+ MW IT
*[Child: 03 -- Site & Building Specs]*
> Trappeys Cannery -- Lafayette, LA. 4 buildings on the Vermilion River.
GPS: 30.21356N, 92.00163W | Acquisition: ~$1M | Half mile from MARLIE I
## Buildings -- 112,500 sq ft Total
  - Rear High Ground: 37,500 sq ft (150x250). Tallest building. ~1,275 panels.
  - Middle High: 22,500 sq ft (75x300). Wooden beams, roof good. ~765 panels.
  - Middle Low: 30,000 sq ft (100x300). Gas piping + fire suppression already in place. ~1,020 panels.
  - Front Lower: 22,500 sq ft (75x300). Vat holes = cable risers. River views. ~765 panels.
## Infrastructure Yard
~28,000 sq ft heavy-duty concrete slab. Gas gensets, transformer/switchgear, dry coolers, battery storage.
## Water Tower
15,000+ gallon elevated steel tank. Repurpose as thermal buffer in liquid cooling loop. Branding landmark.
*[Child: 04 -- Government Funding Stack]*
> Incentive stack for Trappeys -- historic tax credits are the differentiator.
## Programs
  - 45% historic tax credits (federal 20% + state 25%) on rehab costs
  - 30% federal solar ITC on panels
  - 10-year property tax abatement (ITEP -- must file BEFORE groundbreaking)
  - 20-year Act 730 sales tax exemption ($200M+, 50 jobs)
  - NSF/DOE grants through UL Lafayette partnership ($28-55M+ potential)
  - LED FastStart -- FREE customized workforce training
*[Child: 05 -- Infrastructure Partners]*
> Vendor stack for Trappeys. Prove them here, scale them to Willow Glen.
## Partners
  - First Solar -- TR1 panels, rooftop mount. Factory 30 mi away in New Iberia.
  - Louisiana Cat -- gensets, switchgear. New Iberia.
  - Eaton -- Beam Rubin DSX 800V DC distribution
  - ATMOS Energy -- gas supply confirmed on-site
  - LUS -- sell-back only grid connection. Pin Hook substation next door.
  - UL Lafayette -- research liaison, student workspace, grant co-applicant
  - City of Lafayette -- smart city coordination
*[Child: 06 -- ADC3K Credentials]*
> ADC qualifications and track record.
Same credentials as MARLIE I and Willow Glen sections. See adc3k.com.
## Key Credentials
  - Scott Tomsu -- 25+ year ROV Superintendent, deepwater robotics worldwide
  - FAA Private Pilot, IMCA ROV Supervisor, Electronic Technician, Commercial Diver
  - FuelTech engine management certified
  - NVIDIA Partner Network registered
  - ADC3K.com live with full project portfolio
*[Child: 07 -- Louisiana AI Network: Multi-Site Vision]*
> Trappeys is the proof of concept. Willow Glen is the flagship.
## Network Role
  - Trappeys = UL Lafayette anchor | 29 MW ceiling | Proof of concept
  - Willow Glen = LSU anchor | 260 MW ceiling | Flagship
  - MARLIE I = Backup NOC, R&D, edge compute (half mile from Trappeys)
  - KLFT 1.1 = Autonomous airspace ops hub (control tower visible from site)
Every vendor who helps on Trappeys earns their place on Willow Glen.
*[Child: 08 -- Contact & Next Steps]*
> Action items for Trappeys acquisition and buildout.
## Immediate Actions
  - Site LOI -- secure the property (~$1M)
  - ITEP filing -- call LED (Kristin Johnson, 225-342-2083). Must file BEFORE groundbreaking.
  - NPN registration -- 5-minute web form
  - First Solar outreach -- modulesales@firstsolar.com / 419-662-6899
  - UL Lafayette intro -- Dr. Ramesh Kolluru via LEDA warm intro
  - Structural engineer -- roof load analysis before solar
  - Environmental consultant -- Phase I ESA before closing
  - City council presentation -- schedule meeting
## Contact
Scott Tomsu -- scott@adc3k.com -- adc3k.com
*[Child: 09 -- Financial Architecture & ROI]*
> Trappeys financial model. Smaller scale than Willow Glen, faster to revenue.
## Phased Revenue
  - Phase 3 (start): 4 racks | 520 kW IT | Solar + 1 MW gas
  - Phase 5: 20 racks | 2.6 MW IT | Solar + 3 MW gas
  - Phase 7: 50+ racks | 6.5+ MW IT | Full power yard
---
## Trappeys vs Willow Glen
  - Trappeys: $4.5M start | $82M Y5 | 225 racks | 29 MW | $47M net 5yr
  - Willow Glen: $8M start | $360M Y5 | 1,000 racks | 130 MW | $128M net 5yr
  - COMBINED: $12.5M start | $442M Y5 | 1,225 racks | 159 MW | $175M net 5yr