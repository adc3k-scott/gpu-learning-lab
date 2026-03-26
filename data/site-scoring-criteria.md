# ADC AI Factory Site Selection — Scoring Criteria Database
Version: 1.0 | Created: 2026-03-25 | Author: Mission Control

---

## SCORING SYSTEM OVERVIEW

Total possible: 100 base points + 24 bonus points = 124 maximum
Tier system based on BASE score (before bonus):
- **Tier S** (90-100): Exceptional — pursue immediately
- **Tier A** (80-89): Top Priority — strong candidate
- **Tier B** (60-79): Strong Candidate — investigate further
- **Tier C** (40-59): Marginal — requires significant mitigation
- **Tier D** (<40): Disqualified — pass

---

## 10 BASE SCORING VARIABLES (100 points max)

### 1. Natural Gas Pipeline Proximity (Weight: 15 pts)
**Why:** Gas is the backbone. Layer 2 power runs 24/7. Closer = cheaper interconnect, faster permitting.

| Distance | Score | Points | Notes |
|----------|-------|--------|-------|
| 0-5 mi | 10 | 15 | Pipeline on/adjacent to property — ideal |
| 5-15 mi | 7 | 10.5 | Short lateral. ~$500K-2M interconnect |
| 15-30 mi | 4 | 6 | Expensive lateral. $2-5M+ interconnect |
| >30 mi | 0 | 0 | Disqualifying for primary facilities |

Key pipelines in Louisiana:
- **Tennessee Gas** (TGP) — Evangeline to Allen parishes, crosses Atchafalaya
- **Southern Natural Gas** (SNG) — I-10 corridor, Iberia to Calcasieu
- **Gulf South Pipeline** — central/south Louisiana
- **Acadian Gas** — Acadiana region
- **Texas Eastern** (TETCO) — east Louisiana
- **Columbia Gulf Transmission** — Assumption/Lafourche corridor
- **Transco** (Williams) — Terrebonne/Lafourche, $91.8M expansion approved

### 2. Water Access for Cooling (Weight: 12 pts)
**Why:** River/bayou water is the cheapest heat rejection available. Eliminates cooling tower costs.

| Proximity | Score | Points | Notes |
|-----------|-------|--------|-------|
| River/bayou adjacent (<0.25 mi) | 10 | 12 | Direct intake — best case |
| Within 1 mi | 7 | 8.4 | Short pipe run feasible |
| Within 5 mi | 4 | 4.8 | Expensive pipe, may not justify |
| None / >5 mi | 0 | 0 | Dry coolers only — higher OpEx |

Louisiana cooling water sources (ranked):
- **Mississippi River** — 150,000+ CFS, unlimited capacity, permits complex (USACE)
- **Atchafalaya River** — 150,000+ CFS, same flow, fewer industrial conflicts
- **Bayou Teche** — navigable, lower flow, adequate for <50 MW
- **Vermilion River** — Lafayette area, adequate for <20 MW
- **Municipal water** — available everywhere, expensive at scale
- **Bayou Lafourche** — diverted Mississippi water, south Louisiana

### 3. Flood Zone Status (Weight: 10 pts)
**Why:** Insurance costs, foundation costs, permitting complexity. Zone AE is manageable with pilings; Zone VE is a hard pass.

| Zone | Score | Points | Notes |
|------|-------|--------|-------|
| Zone X (no flood) | 10 | 10 | Best case — slab on grade, cheap insurance |
| Zone X Shaded (0.2% annual) | 7 | 7 | Minimal risk, standard construction |
| Zone AE with mitigation (pilings) | 4 | 4 | Pilings add $50-200K but solvable |
| Zone V / VE (coastal) | 0 | 0 | Hard disqualifier — storm surge |

FEMA flood map access:
- **FEMA Flood Map Service Center**: msc.fema.gov
- **Louisiana DOTD Floodplain Management**: la-fpm.com
- Programmatic: FEMA NFHL WMS API (used by our scout agents)

### 4. Foundation Type Needed (Weight: 8 pts)
**Why:** Slab on grade is cheapest. Deep pilings in soft alluvial soil can add $500K+ to site prep.

| Foundation | Score | Points | Notes |
|------------|-------|--------|-------|
| Slab on grade | 10 | 8 | Existing pad or firm ground — cheapest |
| Shallow piling (8-15 ft) | 7 | 5.6 | Moderate cost, typical for south LA |
| Deep piling (30+ ft) | 4 | 3.2 | Expensive — river batture, soft clay |
| Impossible (wetland/marsh) | 0 | 0 | Cannot build — pass |

Louisiana soil considerations:
- **Mississippi River corridor** — generally firm, former levee/industrial sites have compacted fill
- **Atchafalaya Basin** — alluvial, soft, pilings always needed near basin
- **Coastal parishes** — deep pilings, salt intrusion on steel
- **Prairie terrace (Lafayette/Opelousas)** — generally firm, slab on grade common
- Existing concrete pads (former industrial) = free foundation — massive advantage

### 5. Electrical Grid Proximity (Weight: 10 pts)
**Why:** Grid is backup/sell-back (Layer 3 or 4), but substation proximity matters for interconnect and redundancy.

| Distance to Substation | Score | Points | Notes |
|------------------------|-------|--------|-------|
| Within 1 mi | 10 | 10 | Short interconnect, cheap |
| Within 5 mi | 7 | 7 | Standard distribution run |
| Within 15 mi | 4 | 4 | Expensive, may need new line |
| >15 mi | 0 | 0 | Off-grid only — no backup |

Louisiana utility map:
- **Entergy Louisiana** — most of south LA outside Lafayette
- **LUS (Lafayette Utilities System)** — Lafayette Parish, municipal, fiber included
- **SLEMCO** — rural Acadiana co-op
- **CLECO** — central/north Louisiana
- **Demco** — Baton Rouge area co-op

### 6. Fiber Optic Proximity (Weight: 10 pts)
**Why:** AI factories need low-latency, high-bandwidth connectivity. Lit fiber is critical.

| Distance | Score | Points | Notes |
|----------|-------|--------|-------|
| Lit fiber within 0.5 mi | 10 | 10 | Connect in weeks |
| Within 2 mi | 7 | 7 | Short build, ~$50-100K |
| Within 10 mi | 4 | 4 | Expensive build, $200K+ |
| >10 mi | 0 | 0 | Satellite only — latency problem |

Louisiana fiber networks:
- **LUS Fiber** — Lafayette metro, municipal FTTH, lit building network
- **AT&T** — statewide backbone, metro areas
- **Lumen (CenturyLink)** — statewide, long-haul
- **Zayo** — major intercity fiber routes along I-10, I-20
- **EAT (Eatel)** — Ascension/Iberville parishes
- **Windstream** — rural Louisiana
- Industrial corridors (River Road) typically have fiber — petrochemical plants need it

### 7. Road Access (Weight: 8 pts)
**Why:** Heavy equipment delivery (transformers, gensets, racks), ongoing logistics.

| Access | Score | Points | Notes |
|--------|-------|--------|-------|
| Highway frontage (US/Interstate) | 10 | 8 | Best — direct truck access |
| Paved parish road | 7 | 5.6 | Adequate for most loads |
| Gravel/unpaved | 4 | 3.2 | Needs upgrade for heavy equipment |
| No road access | 0 | 0 | Pass |

### 8. Rail Access (Weight: 5 pts)
**Why:** Heavy equipment, fuel delivery at scale, future expansion.

| Access | Score | Points | Notes |
|--------|-------|--------|-------|
| On-site rail spur | 10 | 5 | Transformers, fuel, equipment by rail |
| Adjacent (within 0.25 mi) | 7 | 3.5 | Short spur buildable |
| Within 1 mi | 4 | 2 | Expensive spur, justify at >50 MW |
| No rail | 0 | 0 | Truck-only — fine for <20 MW |

Louisiana railroads:
- **CN (Canadian National)** — former IC, Mississippi River corridor
- **BNSF** — I-10 corridor, Lafayette to Lake Charles
- **UP (Union Pacific)** — I-10 corridor, Baton Rouge to New Orleans
- **KCS** — northeast Louisiana, Baton Rouge
- **Louisiana & Delta Railroad (LDRR)** — short line, New Iberia to Opelousas

### 9. Zoning (Weight: 12 pts)
**Why:** Industrial zoning = no rezoning needed. Agricultural can be rezoned but adds 3-6 months.

| Zoning | Score | Points | Notes |
|--------|-------|--------|-------|
| Industrial (I-1, I-2, M2) | 10 | 12 | Ready to build — no process |
| Commercial (C-1, C-2) | 7 | 8.4 | May need special use permit |
| Agricultural (A-1, A-2) | 4 | 4.8 | Rezoning needed — 3-6 months |
| Residential | 0 | 0 | Hard pass — political nightmare |

### 10. Acquisition Cost (Weight: 10 pts)
**Why:** Capital efficiency. Lower land cost = more budget for infrastructure.

| Cost per Acre | Score | Points | Notes |
|---------------|-------|--------|-------|
| < $10,000/acre | 10 | 10 | Rural/ag land — maximum leverage |
| $10,000-50,000/acre | 7 | 7 | Industrial/commercial — standard |
| $50,000-100,000/acre | 4 | 4 | Urban/premium — needs strong justification |
| >$100,000/acre | 0 | 0 | Too expensive — pass |

---

## 6 BONUS VARIABLES (24 points max)

### B1. Historic Tax Credit Eligible (+5 pts)
National Register property: 20% federal + 25% Louisiana state = **45% of rehab costs returned**.
Qualifies if: listed on/eligible for National Register of Historic Places, contributing structure.

### B2. Brownfield / EPA Eligible (+5 pts)
EPA Brownfields grants: up to $2M for assessment, $5M for cleanup.
Louisiana DEQ Voluntary Remediation Program: liability protection + tax credits.
Former industrial sites (refineries, fabrication yards, terminals) often qualify.

### B3. University Within 5 Miles (+5 pts)
Research compute anchor tenant, grant pipeline (NSF, DOE, EPSCoR), workforce pipeline.
Louisiana tier-1 targets:
- **UL Lafayette** — Trappeys (<1 mi), MARLIE I (<2 mi)
- **LSU** — Willow Glen (~15 mi), Port Allen sites (~5 mi)
- **McNeese** — Lake Charles sites
- **Nicholls State** — Thibodaux/Gray sites
- **Southern University** — Baton Rouge corridor

### B4. Existing Structure (+3 pts)
Warehouse, fabrication building, or any enclosed structure reduces CapEx.
Existing concrete pad = free foundation. Existing 3-phase power = months saved.

### B5. LUS / Municipal Utility vs. Entergy (+3 pts)
Municipal utilities (LUS, CLECO) = lower rates, faster interconnect, fiber bundled.
LUS Fiber specifically: municipal broadband, competitive pricing, no carrier gatekeeping.
Entergy = regulated monopoly, slower interconnect process, higher rates.

### B6. Port / Dock Access (+3 pts)
Barge delivery for heavy equipment (transformers, large gensets).
River cooling water infrastructure already permitted at dock sites.
Relevant for >50 MW facilities where equipment exceeds road weight limits.

---

## EXISTING SITE SCORECARDS

### 1. Trappeys Cannery — Lafayette, LA
**GPS:** 30.21356N, 92.00163W | **Status:** THE CORE PROJECT

| Variable | Detail | Score | Weight | Points |
|----------|--------|-------|--------|--------|
| Gas pipeline | Trunk line ON SITE, city hub up the road | 10 | 15 | 15 |
| Water access | Vermilion River adjacent (riverfront property) | 10 | 12 | 12 |
| Flood zone | Zone X Shaded (river adjacent but elevated) | 7 | 10 | 7 |
| Foundation | Existing concrete pads + floors (100 yr old, solid) | 10 | 8 | 8 |
| Grid proximity | LUS Pin Hook Substation visible from site | 10 | 10 | 10 |
| Fiber proximity | LUS Fiber conduit path confirmed | 10 | 10 | 10 |
| Road access | US 90 / SE Evangeline Thruway frontage | 10 | 8 | 8 |
| Rail access | LDRR within ~1 mi (Ambassador Caffery area) | 4 | 5 | 2 |
| Zoning | Industrial corridor (adjacent to Public Works) | 10 | 12 | 12 |
| Acquisition cost | ~$1M for 8 acres = ~$125K/acre (high, but structures included) | 0 | 10 | 0 |
| **BASE TOTAL** | | | | **84** |

| Bonus | Detail | Points |
|-------|--------|--------|
| Historic tax credit | National Register APPROVED — 45% credits | +5 |
| Brownfield/EPA | Former industrial (cannery) — likely eligible | +5 |
| University <5 mi | UL Lafayette ~1 mile | +5 |
| Existing structure | 112,500 sq ft across 4 buildings | +3 |
| Municipal utility | LUS (electric + fiber) | +3 |
| Port/dock access | Vermilion River — small craft only, not deep water | +0 |
| **BONUS TOTAL** | | **+21** |

**TOTAL: 84 base + 21 bonus = 105 | Tier A**

Notes: High price/acre offset by historic tax credits (45% of rehab), existing structures, existing infrastructure. Net effective cost is dramatically lower. Gas ON SITE. Every utility ON SITE or adjacent. Half mile from MARLIE I. 30 mi from First Solar. This is why it's THE site.

---

### 2. MARLIE I — Lafayette, LA
**GPS:** 30.21975N, 92.00645W | **Status:** Command Center

| Variable | Detail | Score | Weight | Points |
|----------|--------|-------|--------|--------|
| Gas pipeline | Natural gas confirmed, trunk line nearby | 10 | 15 | 15 |
| Water access | Vermilion River ~0.5 mi | 7 | 12 | 8.4 |
| Flood zone | Zone X (SE Evangeline Thruway corridor) | 10 | 10 | 10 |
| Foundation | Existing parcels, demolish blighted structures, slab | 7 | 8 | 5.6 |
| Grid proximity | LUS substation <1 mi (same as Trappeys area) | 10 | 10 | 10 |
| Fiber proximity | LUS Fiber conduit confirmed | 10 | 10 | 10 |
| Road access | SE Evangeline Thruway (US 90) frontage | 10 | 8 | 8 |
| Rail access | None on-site, LDRR ~1.5 mi | 0 | 5 | 0 |
| Zoning | Industrial corridor — no rezoning needed | 10 | 12 | 12 |
| Acquisition cost | $15K land debt — effectively free | 10 | 10 | 10 |
| **BASE TOTAL** | | | | **89** |

| Bonus | Detail | Points |
|-------|--------|--------|
| Historic tax credit | Blighted structures — possible rehab credits | +0 |
| Brownfield/EPA | Not brownfield | +0 |
| University <5 mi | UL Lafayette ~2 mi | +5 |
| Existing structure | Structures to demolish, building new 24x40 | +0 |
| Municipal utility | LUS (electric + fiber) | +3 |
| Port/dock access | No | +0 |
| **BONUS TOTAL** | | **+8** |

**TOTAL: 89 base + 8 bonus = 97 | Tier A**

Notes: Nearly perfect score driven by zero land cost, existing utilities, industrial zoning, and LUS fiber. Small site (0.6 acres) limits scale to 8 NVL72 racks / 576 GPUs — by design. This is the command center, not the big compute site. Highest base score of all 4 existing sites.

---

### 3. KLFT Airport Area — Lafayette, LA
**GPS:** 30.21256N, 91.99069W | **Status:** Drone Hub (Future AI Compute TBD)

| Variable | Detail | Score | Weight | Points |
|----------|--------|-------|--------|--------|
| Gas pipeline | Acadian Gas corridor through Lafayette | 7 | 15 | 10.5 |
| Water access | Vermilion River ~1.5 mi | 4 | 12 | 4.8 |
| Flood zone | Zone X (airport elevated) | 10 | 10 | 10 |
| Foundation | Airport land — engineered fill, slab ready | 10 | 8 | 8 |
| Grid proximity | LUS/SLEMCO substations within 2 mi | 7 | 10 | 7 |
| Fiber proximity | LUS Fiber metro coverage | 10 | 10 | 10 |
| Road access | Airport Road / Hwy 90 corridor | 10 | 8 | 8 |
| Rail access | None at airport | 0 | 5 | 0 |
| Zoning | Airport/commercial — special use likely needed | 7 | 12 | 8.4 |
| Acquisition cost | Airport land lease — cost TBD (public land) | 7 | 10 | 7 |
| **BASE TOTAL** | | | | **73.7** |

| Bonus | Detail | Points |
|-------|--------|--------|
| Historic tax credit | No | +0 |
| Brownfield/EPA | No | +0 |
| University <5 mi | UL Lafayette ~3 mi | +5 |
| Existing structure | Airport facilities available | +3 |
| Municipal utility | LUS available | +3 |
| Port/dock access | No | +0 |
| **BONUS TOTAL** | | **+11** |

**TOTAL: 74 base + 11 bonus = 85 | Tier B (base) / Tier A (with bonus)**

Notes: KLFT is primarily a drone operations hub, not an AI compute site. Score reflects land availability near the airport for potential edge compute co-location. Airport zoning adds complexity. Pipeline is close but not adjacent. Primary value is the NVIDIA Smart City convergence (Jetson + Metropolis + Omniverse), not raw compute.

---

### 4. Willow Glen Terminal — St. Gabriel, LA
**GPS:** 30.24700N, 91.09850W | **Status:** PRIMARY HUB (Big Daddy)

| Variable | Detail | Score | Weight | Points |
|----------|--------|-------|--------|--------|
| Gas pipeline | Pipeline corridor ON SITE, direct tap available | 10 | 15 | 15 |
| Water access | Mississippi River frontage, 3,500 ft, 43-ft dock | 10 | 12 | 12 |
| Flood zone | Zone X confirmed (minimal flood risk) | 10 | 10 | 10 |
| Foundation | Former 2,200 MW power station — engineered ground | 10 | 8 | 8 |
| Grid proximity | On-site Entergy substation (230kV + 138kV) | 10 | 10 | 10 |
| Fiber proximity | Industrial corridor fiber within 1 mi (EAT/AT&T) | 7 | 10 | 7 |
| Road access | LA-75 / I-10 access | 10 | 8 | 8 |
| Rail access | CN Railway ON SITE | 10 | 5 | 5 |
| Zoning | M2 Heavy Industrial | 10 | 12 | 12 |
| Acquisition cost | Price upon request — likely $50-100K/acre for lease | 7 | 10 | 7 |
| **BASE TOTAL** | | | | **94** |

| Bonus | Detail | Points |
|-------|--------|--------|
| Historic tax credit | Former power station — potential (need NPS review) | +0 |
| Brownfield/EPA | Former power station — likely Phase I ESA needed | +5 |
| University <5 mi | LSU ~15 mi (too far for bonus) | +0 |
| Existing structure | 20K SF warehouse, tank farm, dock infrastructure | +3 |
| Municipal utility | Entergy (not municipal) — no bonus | +0 |
| Port/dock access | 43-ft deepwater dock, 3,500 ft frontage | +3 |
| **BONUS TOTAL** | | **+11** |

**TOTAL: 94 base + 11 bonus = 105 | Tier S**

Notes: Highest base score possible for a Louisiana site. Every single infrastructure element is ON SITE or adjacent. The only weakness is fiber (not lit on property, but industrial corridor has fiber within 1 mile) and acquisition cost (price upon request, likely premium). The 230kV bidirectional substation alone is worth tens of millions — you cannot build that. Former river water cooling intake from power station era still exists. This is the endgame site. Hut 8 / River Bend campus ($10B) is 45 minutes north — validates the corridor.

---

## LAFAYETTE PARISH — EXPANSION OPPORTUNITIES

### SE Evangeline Thruway Corridor
The SE Evangeline Thruway (US 90) from downtown Lafayette south to the Vermilion River bridge is an industrial/commercial corridor. Key features:
- LUS utilities (electric + fiber) throughout
- Natural gas trunk lines along corridor
- Mix of light industrial, auto shops, warehouse, commercial
- Vermilion River parallel to the west
- Public Works facilities, water/sewer infrastructure

**Properties to investigate:**
- Parcels between Trappeys and MARLIE I (half-mile stretch)
- Former auto dealership/warehouse lots on Evangeline Thruway
- Underutilized commercial parcels south of Johnston Street
- City-owned surplus land near Public Works compound

**Assessor data access:**
- **Lafayette Parish Assessor**: lafayetteassessor.com
- **Online GIS**: Lafayette Parish GIS Portal (gis.lafayettela.gov)
- **Tax rolls**: searchable by owner, address, parcel ID
- **Sales data**: recent transactions available online

### Hwy 90 Corridor Near Airport
The Hwy 90 corridor from Lafayette south toward Broussard/Youngsville:
- SLEMCO electric (co-op, not municipal)
- Gas pipeline corridor (Acadian Gas, Gulf South)
- Growing commercial/industrial area (Safesource, oilfield services)
- I-10/US 90 interchange access
- Airport Road connects to KLFT

Already in database: **Smede Hwy Industrial Tract** (46.49 acres, Zone X, $34K/acre, Score 74 Tier B)

### Known Lafayette Parish Brownfields
- **Trappeys Cannery** — already in database, cannery/industrial since 1920s
- **Former oil/gas service yards** along Evangeline Thruway
- **Downtown industrial properties** along the railroad tracks
- **City of Lafayette Brownfields Program**: contact LED (Louisiana Economic Development) for current inventory
- **EPA Brownfields search**: cleanups.epa.gov/enviro/query — search "Lafayette Parish, LA"

### FEMA Flood Maps — Lafayette Parish Access
- **FEMA Map Service Center**: msc.fema.gov — search by address
- **Lafayette Parish FIRM panels**: Community 220100 (Lafayette) and 220101 (unincorporated)
- Most of SE Evangeline Thruway corridor is **Zone X** (minimal flood)
- Vermilion River floodway is **Zone AE** — properties ON the river have AE designation
- Airport area is **Zone X** (elevated, engineered drainage)
- General rule: stay on the Evangeline Thruway ridge = Zone X; go toward bayous = Zone AE

---

## PIPELINE SCOUT DATABASE REVIEW (16 sites)

Current scoring uses the OLD system (pipeline_scout scorer.py — 6 variables, 100 pts).
Recommended updates to align with new 10-variable + bonus system:

| # | Site | Current Score | Issues / Updates Needed |
|---|------|---------------|------------------------|
| 1 | Leroy Road (Maurice) | 73 B | Add water, rail, foundation, cost scoring. Flood not verified. |
| 2 | Hulin Road (Erath) | 63 B | **STATUS: PASS** — Zone VE confirmed, hard disqualifier. Keep as-is. |
| 3 | Hwy 90 Industrial (New Iberia) | 67 B | Add water (Bayou Teche ~1 mi), rail (LDRR nearby). Good zoning. |
| 4 | Ratcliff Lane (Franklin) | 67 B | Add water (Bayou Teche <1 mi), flood not verified. |
| 5 | Kinder Industrial (Hwy 165) | 81 A | Strong. Add water scoring (Calcasieu River ~5 mi — marginal). |
| 6 | Riverside Road (Mamou Canal) | 67 B | Canal access = some water credit. Remote. |
| 7 | Bienville Road (Ville Platte) | 67 B | Remote, wooded, no water access. Likely downgrade. |
| 8 | Prudhomme Lane (Opelousas) | 51 C | Too small (2 acres), too expensive. Low priority. |
| 9 | **New Iberia I-1 (Hwy 90/14)** | **87 A** | **STRONG.** Gas ON property. Power ON property. Zone X. Add Bayou Teche ~1.5 mi. Update with new scoring — should stay Tier A. |
| 10 | Common St (Lake Charles) | 83 A | Pipeline corridor. Add Calcasieu River ~2 mi. Hurricane risk zone. |
| 11 | Franklin Ag (LA-87) | 72 B | Near SNG mainline. Add Bayou Teche proximity. |
| 12 | Iowa Industrial (Hwy 165/I-10) | 81 A | Good interstate access. Add water scoring (Calcasieu ~8 mi). |
| 13 | Smede Hwy (Broussard) | 74 B | Large (46 ac), Zone X, Hwy 90 frontage. Pipeline ~2 mi. No river. |
| 14 | Hwy 1011 (Napoleonville) | 57 C | Cheap but remote, poor power access. |
| 15 | Hwy 90 Energy Corridor (Gray) | 72 B | Huge (108 ac), no zoning restrictions. Transco pipeline nearby. |
| 16 | Hwy 3235 (Cut Off) | 59 C | Pipeline ~1.5 mi, no river direct access. Lafourche coastal risk. |

**Priority re-scores needed:** Sites #9 (New Iberia I-1) and #10 (Lake Charles) should be re-evaluated first — both are Tier A candidates that may strengthen further or weaken with the expanded criteria.

---

## RIVER SCOUT DATABASE REVIEW (15 sites)

River scout already uses 7-variable system (includes river). Updates needed for full 10-variable alignment:

| # | Site | Current Score | Issues / Updates Needed |
|---|------|---------------|------------------------|
| 1 | Krotz Springs Levee Tract 3 | 82 A | Add rail, foundation, cost. Flood AE expected — pilings OK. |
| 2 | Old Hwy 190 (721 acres) | 78 B | Massive. Add rail, foundation. Near Tier A with full scoring. |
| 3 | 9006 Hwy 182 (Morgan City) | 64 B | Waterfront industrial. Small (1.78 ac). Expensive. |
| 4 | New Iberia I-1 (Hwy 90/14) | 70 B | **DUPLICATE** of pipeline site #9. Merge records. |
| 5 | Former McDermott Yard (Morgan City) | 74 B | Brownfield (+5). Waterfront. Existing structures (+3). Should be Tier A with bonus. |
| 6 | Hwy 190 Port Allen | 82 A | Industrial, Zone X, near river. Opportunity Zone (+5 if applicable). |
| 7 | **Willow Glen Terminal** | **94 A** | **TOP SITE.** Already scored above. Now Tier S in new system. |
| 8 | Belle Grove (White Castle) | 80 A | LED Certified (+5 effective). 578 acres. Mississippi frontage. |
| 9 | Batture Land (Darrow) | 68 B | Batture = flood risk, pilings required. Small. |
| 10 | Tract B Hwy 190 (Port Allen) | 64 B | Commercial zoning (needs rezone). 1.5 mi from river. |
| 11 | Bayou Teche Frontage (Breaux Bridge) | 72 B | Direct bayou frontage. Unrestricted. Good for edge. |
| 12 | I-10 Exit 109 Industrial (Breaux Bridge) | 72 B | LED Certified. 42 acres. All utilities. Strong candidate. |
| 13 | Bayou Teche (Jeanerette/Sorrel) | 63 B | Small (4.65 ac). Cheap. Edge deployment only. |
| 14 | Bayou Teche (Centerville) | 67 B | Tiny (2.92 ac). Cheap. Edge only. |
| 15 | 24-Acre Ag (New Iberia) | 68 B | A1 zoning allows warehouse. Near Bayou Teche. |

**Priority re-scores needed:** Sites #5 (McDermott), #6 (Port Allen), #8 (Belle Grove) all likely move to Tier A with bonus scoring applied. Site #4 is a duplicate — merge with pipeline #9.

---

## NEXT STEPS

1. **Run updated scoring** — build `scripts/site_scorer_v2.py` that applies the 10+6 variable system to all 31 existing sites + 4 reference sites
2. **Lafayette Parish deep scan** — use assessor GIS + LandWatch + LoopNet to find additional parcels on SE Evangeline Thruway and Hwy 90 corridor
3. **Merge duplicates** — New Iberia I-1 appears in both pipeline and river databases
4. **Verify flood zones** — 18 of 31 sites have "No GPS — flood zone not checked"
5. **Add GPS coordinates** — 16 of 31 sites missing lat/lng
6. **Price research** — 4 sites have no price data (Willow Glen, Belle Grove, Breaux Bridge bayou, Breaux Bridge industrial)
7. **Brownfield inventory** — cross-reference EPA ACRES database for all 31 parishes represented

---

## DATA SOURCES REFERENCE

| Source | URL | What It Has |
|--------|-----|-------------|
| Lafayette Parish Assessor | lafayetteassessor.com | Tax rolls, sales, ownership |
| Lafayette GIS | gis.lafayettela.gov | Parcel maps, zoning, flood overlay |
| Iberville Parish Assessor | ibervilleassessor.com | Willow Glen area parcels |
| Iberia Parish Assessor | iberiaassessor.org / iberia.geosync.io | New Iberia parcels |
| FEMA Flood Maps | msc.fema.gov | FIRM panels, Zone X/AE/VE |
| LA DOTD Floodplain | la-fpm.com | State flood management |
| LED Site Selection | louisianasiteselection.com | Certified/mega sites |
| EPA Brownfields | cleanups.epa.gov | Contaminated site inventory |
| LA DEQ VRP | deq.louisiana.gov | Voluntary remediation |
| LoopNet | loopnet.com | Commercial/industrial listings |
| LandWatch | landwatch.com | Rural/agricultural listings |
| Land.com | land.com | All land types |
| Crexi | crexi.com | Commercial real estate |
| CBRE | cbre.com | Institutional listings (Willow Glen) |
| LA Pipeline Map | FERC eLibrary / NPMS | Pipeline locations |
| USGS National Map | viewer.nationalmap.gov | Topo, hydro, infrastructure |
