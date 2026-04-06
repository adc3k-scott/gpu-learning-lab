# Site Evaluation Framework & Scoring
*Notion backup — 2026-04-06*

> Use this framework on every site visit and property evaluation. Produces a TYPE classification and Priority Score. Run before any LOI or acquisition conversation.
---
## Step 1 — Classify the Site
- TYPE A (Full AI Factory): Large lot OR existing large building. CDU rack cooling. NVL72 racks. NOC build-out.
- TYPE B (ADC 3K Pod Site): Any metal structure OR cleared slab. Full EC-110 immersion. Container drop-in.
- TYPE C (Mixed Hub): Enough land/building for BOTH Type A facility AND Type B pod farm.
- TYPE D (EV/Drone Only): Location too small or wrong zoning for compute, but valid for EV charging + KLFT relay.
---
## Step 2 — Score the Location (1-5 each)
- Power access: 5=3-phase on property, 4=3-phase at road, 3=upgrade needed, 2=residential only, 1=none
- Gas access: 5=line on property, 4=within 1 mile, 3=1-5 miles, 2=5+ miles, 1=none
- Fiber access: 5=LUS Fiber lit, 4=conduit in road, 3=wireless backhaul viable, 2=long haul needed, 1=none
- Owner situation: 5=known 30 years/motivated seller, 4=known contact, 3=cold approach, 2=complicated title, 1=unavailable
- Flood risk: 5=Zone X high ground, 4=Zone X, 3=Zone AE with mitigation, 2=Zone AE, 1=Zone VE/flood plain
- Customer proximity: 5=anchor tenant identified, 4=multiple industries adjacent, 3=commercial corridor, 2=residential, 1=isolated
- Zoning: 5=industrial/heavy, 4=commercial, 3=mixed use (variance possible), 2=residential (hard rezone), 1=protected
---
## Step 3 — Determine Infrastructure Stack
Based on type and score, assign the standard infrastructure stack:
- Compute: NVL72 racks (CDU) for Type A | EC-110 immersion pods for Type B | Both for Type C
- Power: LUS/CLECO grid primary + Bloom Energy fuel cell + nat gas generator + diesel N+1
- Energy supplement: New Iberia Solar PPA where feasible (south Acadiana sites)
- Network: LUS Fiber primary + diverse second carrier + MARLIE I NOC backhaul
- EV: DC fast charge + Level 2 at every site, utility aesthetic
- Drone: KLFT relay node at every site — Skydio Dock if primary hub, relay antenna if secondary
---
## Scoring Thresholds
- Score 28-35: PRIORITY 1 — move immediately, LOI within 30 days
- Score 21-27: PRIORITY 2 — active engagement, 90-day target
- Score 14-20: PRIORITY 3 — monitor, re-evaluate when capital available
- Score below 14: HOLD — document but do not pursue until fundamentals improve
---
## Scoring System v2 — 10 Base + 6 Bonus Variables (2026-03-25)
> v2 replaces the original 7-variable system. 10 base variables (100 pts max) + 6 bonus variables (24 pts max) = 124 total possible. Scoring engine: agents/site_scout/scorer_v2.py
---
### Base Variables (10 x 10 pts = 100 pts max)
1. Power Access (0-10): Grid capacity, voltage, distance to substation
1. Natural Gas (0-10): Pipeline proximity, Henry Hub pricing zone, ATMOS service
1. Fiber/Network (0-10): LUS Fiber, LONI backbone, dark fiber availability
1. Water/Cooling (0-10): Water source for cooling, discharge permits, adiabatic viability
1. Flood Risk (0-10): FEMA zone, elevation, historical flooding
1. Zoning/Permits (0-10): Current zoning, variance difficulty, environmental review
1. Building/Land (0-10): Existing structure quality, sq footage, clear span, ceiling height
1. Road/Logistics (0-10): Interstate access, truck routes, equipment delivery path
1. Workforce (0-10): Proximity to labor pool, university pipeline, training programs
1. Acquisition Cost (0-10): Price per sq ft, seller motivation, deal complexity
---
### Bonus Variables (6 x 4 pts = 24 pts max)
1. University Partnership (0-4): Anchor tenant, research collaboration, grant eligibility
1. Solar Potential (0-4): Rooftop area, orientation, First Solar proximity
1. Historical/Tax Credits (0-4): Historic designation, Brownfield, Opportunity Zone
1. Community Impact (0-4): Job creation narrative, revitalization story, political support
1. Multi-Site Synergy (0-4): Proximity to other ADC sites, shared infrastructure
1. Strategic Value (0-4): Unique capabilities (river access, airport, rail)
---
### Tier Classification
- Tier S (100+): Exceptional — move immediately, flagship site
- Tier A (85-99): Excellent — priority development, strong fundamentals
- Tier B (70-84): Good — viable with targeted investment
- Tier C (55-69): Marginal — significant gaps, monitor only
- Tier D (<55): Not viable — pass
---
### Current Site Scores (v2)
> Trappeys Cannery: 84 base + 21 bonus = 105 (Tier S)
Willow Glen Terminal: 94 base + 11 bonus = 105 (Tier S)
MARLIE I Command Center: 89 base + 8 bonus = 97 (Tier A/S)
KLFT 1.1 Drone Hub: 74 base + 11 bonus = 85 (Tier B/A)
---
### Trappeys Cannery — 105 (Tier S)
- Base: 84/100 — Strong power (ATMOS gas, LUS grid), LUS Fiber lit, 112,500 sq ft across 4 buildings, I-10 access, UL Lafayette 2 miles
- Bonus: 21/24 — UL Lafayette partnership (+4), 2.05 MW solar rooftop (+4), Historic tax credits 45-55% (+4), Riverwalk/revitalization narrative (+4), Half mile from MARLIE I (+4), Near KLFT (+1)
- Key advantage: Highest bonus score of any site. University + solar + historic credits stack.
---
### Willow Glen Terminal — 105 (Tier S)
- Base: 94/100 — Former 2,200 MW Entergy station, existing heavy industrial infrastructure, river cooling (Mississippi), massive land parcel, transmission-grade power
- Bonus: 11/24 — LSU partnership potential (+4), River access strategic value (+4), Multi-site synergy with Baton Rouge (+3)
- Key advantage: Highest base score. Raw infrastructure is unmatched. 100+ MW scale potential.
---
### MARLIE I Command Center — 97 (Tier A/S)
- Base: 89/100 — Scott's existing location, LUS Fiber lit, ATMOS gas on property, I-49 access, Lafayette workforce
- Bonus: 8/24 — Multi-site synergy with Trappeys (+4), Strategic NOC/war room value (+4)
- Key advantage: Operational NOW. Backup NOC, R&D staging, Scott's war room. Zero acquisition cost.
---
### KLFT 1.1 — 85 (Tier B/A)
- Base: 74/100 — Airport infrastructure, FAA Part 108 BVLOS pending, limited compute space, specialized zoning
- Bonus: 11/24 — Strategic drone hub value (+4), NVIDIA Smart City convergence (+4), Proximity to Trappeys <1 mi (+3)
- Key advantage: Autonomous airspace ops. Not a compute site — it's a drone/AI-RAN command node.
---
Scoring engine source: agents/site_scout/scorer_v2.py — run programmatically against any new site prospect.