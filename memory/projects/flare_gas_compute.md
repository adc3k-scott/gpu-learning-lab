# Flare Gas to Compute — Louisiana Opportunity

## Executive Summary

Louisiana flares and vents ~2-5 billion cubic feet (BCF) of natural gas annually. Oil operators burn this gas because pipeline infrastructure is too far, volumes are too small, or connection costs exceed the gas value. ADC can deploy containerized AI compute at flare sites, converting waste gas into GPU-hours. The pitch: "You're burning money. We take the gas, run AI compute, you stop paying penalties. Zero cost to you."

This is Crusoe Energy's playbook — they scaled from zero to $10B valuation doing exactly this. ADC adapts it for Louisiana with three advantages: proximity to ADC facilities (Trappeys, MARLIE 1, Willow Glen), bayou/river water for cooling, and existing relationships with Louisiana oil operators.

---

## Louisiana Flaring Data (EIA Annual, Million Cubic Feet)

Source: [EIA Louisiana Natural Gas Vented and Flared](https://www.eia.gov/dnav/ng/hist/n9040la2a.htm)

| Year | Vented & Flared (MMCF) |
|------|----------------------|
| 2018 | 5,966 |
| 2019 | 5,101 |
| 2020 | 4,491 |
| 2021 | 3,499 |
| 2022 | 3,816 |
| 2023 | 1,990 |
| 2024 | 1,847 |

**Trend**: Declining from ~6 BCF (2018) to ~1.8 BCF (2024). The 2019 EDF/Synapse study found 27 BCF total wasted (including leaks) — worth $82 million. Flaring alone was 19% of that waste (~5.1 BCF, ~$15.6M).

**Context**: Louisiana is NOT a top-flaring state (Texas and North Dakota dominate). But 1.8 BCF/year is still significant — enough to generate ~180,000 MWh of electricity, which could power ~20-25 MW of continuous compute.

### What 1.8 BCF Means in Compute Terms
- 1 BCF of natural gas = ~100,000 MWh of electricity (at ~35% generator efficiency)
- 1.8 BCF = ~180,000 MWh
- A 1 MW compute container runs 8,760 MWh/year
- **1.8 BCF supports ~20 MW of continuous compute across the state**
- At GPU cloud rates ($2-3/GPU-hr for H100s), even 5 MW = substantial revenue

---

## Where Gas Is Flared in Louisiana

### Top Oil-Producing Parishes (Where Flaring Occurs)

**Coastal/South Louisiana (PRIMARY TARGET ZONE for ADC)**:
1. **Plaquemines Parish** — #1 oil producer, 12.74% of state production (189.6k BBL/month). Major operators: numerous offshore/onshore.
2. **Lafourche Parish** — #10 state BOE. Historically oil-dominant. Golden Meadow area.
3. **Terrebonne Parish** — #12 state BOE. Major offshore staging area.
4. **Vermilion Parish** — #14 state BOE. Adjacent to Lafayette/Acadiana. NEAR ADC SITES.
5. **Cameron Parish** — Coastal oil & gas, remote locations. Cheniere LNG nearby.
6. **St. Martin Parish** — Atchafalaya Basin wells. NEAR ADC SITES (30 min from Trappeys).
7. **Iberia Parish** — Oil production near New Iberia. ADJACENT to ADC territory.
8. **Acadia Parish** — Historic (Jennings oilfield, 1901). Still producing.
9. **St. Mary Parish** — Atchafalaya delta, offshore staging.

**North Louisiana (Haynesville Shale)**:
10. **Caddo Parish** — Haynesville gas production.
11. **DeSoto Parish** — Core Haynesville. Apex, Comstock, Tellurian operating.
12. **Bossier Parish** — Haynesville producing.
13. **Red River Parish** — Active drilling.
14. **Bienville Parish** — Haynesville activity.

### Why South Louisiana Parishes Matter for ADC
- **Vermilion, Iberia, St. Martin, Acadia** — all within 30-60 miles of Trappeys and MARLIE 1
- **Lafourche, Terrebonne** — within 90 miles of Willow Glen
- **Plaquemines** — near Willow Glen corridor
- Every site has bayou/river water access for cooling
- Existing oil field roads and infrastructure

### Satellite Flare Detection
- **SkyTruth Flaring Map**: [flaring.skytruth.org](https://flaring.skytruth.org/) — daily VIIRS satellite updates showing every active flare globally. Use to identify specific Louisiana flare sites.
- **VIIRS Nightfire**: [eogdata.mines.edu](https://eogdata.mines.edu/products/vnf/global_gas_flare.html) — raw data, temperature/size of each detection. Version 4.0 (July 2025) from three satellites.
- **EPA FLIGHT**: [ghgdata.epa.gov](https://ghgdata.epa.gov/ghgp/main.do) — facility-level greenhouse gas data for Louisiana, searchable by facility.

### State Data Systems
- **SONRIS**: [sonris.com](https://www.sonris.com/) — Louisiana's official oil & gas database. Well permits, production, operator data. Permit forms now require gas management plan (Jan 2024 amendment).
- **SONRIS GIS**: [Interactive map](https://sonris-gis.dnr.la.gov/gis/agsweb/IE/JSViewer/index.html?TemplateID=181) — map every well in Louisiana.

---

## Major Louisiana Oil & Gas Operators (Targets)

### Majors
- **ExxonMobil** — massive Louisiana presence (Baton Rouge refinery, offshore)
- **Chevron** — Gulf operations, onshore Louisiana
- **Shell** — offshore GoM, Louisiana onshore
- **BP** — Gulf operations

### Large Independents
- **Cantium LLC** (Covington, LA) — Bay Marchand, Main Pass, 193,000+ acres
- **LLOG Exploration** (Golden Meadow, LA) — deepwater GoM, private
- **PetroQuest Energy** (Lafayette, LA) — exploration/production in TX and LA
- **Comstock Resources** — Haynesville Shale (DeSoto, Red River, Bossier, etc.)
- **Apex Energy** — 9 rigs in NW Louisiana (Haynesville)
- **Tellurian** — 20,000+ acres in DeSoto, Bossier, Red River, Webster

### Key Insight for ADC
The **independents and smaller operators** are the real targets. Majors have the capital to build pipeline connections. Small/mid operators with 1-10 wells in remote locations are the ones who flare because they can't justify pipeline economics. These are the operators Crusoe targets.

---

## Why Operators Flare

1. **No pipeline access** — well is too far from gathering system, or volume too small to justify connection cost ($500K-$2M per connection)
2. **Pipeline constraints** — existing gathering system is at capacity, no takeaway
3. **Pressure management** — gas must be disposed to prevent equipment over-pressurization
4. **Economics** — gas price too low relative to capture/transport cost
5. **Temporary production** — well may only produce for 1-3 years; pipeline investment doesn't pencil
6. **Permitting delays** — gas sales infrastructure takes months/years to permit and build

**Louisiana-specific**: Many south Louisiana wells are in wetlands, marshes, and coastal areas where pipeline construction is especially expensive and environmentally restricted. The Atchafalaya Basin, coastal Vermilion, Cameron, and Terrebonne are particularly pipeline-constrained.

---

## Louisiana Regulatory Framework

### State Rules: La. Admin. Code tit. 43, Section XIX-3507

**Venting**: PROHIBITED except where flaring is not economical or safe.

**Routine Flaring**:
- Wells with GOR > 2000:1 — flaring PROHIBITED unless Office of Conservation grants hardship exemption
- Horizontal wells with GOR < 2001:1 — flaring PROHIBITED unless approved by Office of Conservation
- Hardship exemption DENIED if "current market value of the gas proposed to be flared exceeds the cost involved in making such gas available to a market"

**Application Requirements**:
- Statement of need
- Economic justification
- Evaluation of alternative beneficial uses (THIS IS WHERE ADC FITS)
- Rate information
- Duration specification

**Reporting**: Monthly reporting of all flaring/venting volumes on OGP and R5D forms.

**Safety**: Flares must be placed at safe distance from wells, tanks, and structures.

**January 2024 Amendment**: Permit to Drill forms modified to require gas management plan selection. Operators must now declare how they will handle associated gas BEFORE drilling.

### Federal Rules: EPA Waste Emissions Charge (Inflation Reduction Act)

- **$900/metric ton** of wasteful methane emissions (2024)
- **$1,200/metric ton** (2025)
- **$1,500/metric ton** (2026+)
- Applies to facilities emitting >25,000 mt CO2e/year
- **Status (2025-2026)**: EPA removed implementing regulations per Congressional resolution, BUT the underlying IRA fee requirement remains until Congress repeals it. Operators face legal uncertainty — the fee obligation may still apply.

### ADC's Regulatory Angle
"We provide an alternative beneficial use for your stranded gas. Instead of applying for a flaring hardship exemption (which the Office of Conservation can deny), partner with us. We consume your gas on-site, you report zero flaring, and you avoid both state scrutiny and potential federal methane fees."

---

## The Crusoe Model — What They Did and How ADC Adapts

### Crusoe's Playbook (2018-2025)

| Element | Crusoe | ADC Adaptation |
|---------|--------|----------------|
| **Founded** | 2018, Denver CO | — |
| **Technology** | Digital Flare Mitigation (DFM) — patented | ADC builds similar but DSX-compliant |
| **Generator** | INNIO Waukesha engines (1-1.5 MW each) | Same or Caterpillar/Cummins gas gensets |
| **Compute container** | Custom modular (Crusoe Spark), GPU racks, HVAC, fire suppression | ADC 3K pod + gas genset skid |
| **Gas agreement** | 1-5 year gas purchase agreements; Crusoe PAYS for the gas | ADC pays $0 or nominal — gas has zero/negative value at flare site |
| **Combustion efficiency** | 99.89% (vs 93% for open flares) | Generator engines achieve similar |
| **CO2 reduction** | 63% less CO2e vs flaring | Same physics |
| **Deployment time** | ~3 months per site | ADC targets similar |
| **Site duration** | 1-3 years per well site | Same — modular/mobile |
| **Revenue 2024** | $276M | — |
| **Revenue 2025** | $998M projected | — |
| **Revenue 2026** | $2B projected | — |
| **Valuation** | $10B+ (Series E, Oct 2025) | — |
| **Gas captured** | 39 BCF total, 10 BCF in 2024 alone | — |
| **Units deployed** | 400+ Spark units, 250+ MW | — |
| **Pivot** | Sold DFM/Bitcoin division to NYDIG (March 2025), now pure AI infrastructure | ADC starts with AI from day one |

### Crusoe's Pitch to Operators
1. "We'll pay you for gas you're currently burning"
2. "We handle all equipment, installation, and operations"
3. "Your flaring compliance improves immediately"
4. "Contracts are 1-5 years — aligned with well life"
5. "We can relocate when the well declines"

### How ADC's Pitch Is BETTER Than Crusoe's
1. **Louisiana-based** — Crusoe operates mainly in North Dakota, Wyoming, Colorado, Texas. NO Louisiana presence.
2. **Local relationships** — Scott knows Louisiana oil & gas operators. Crusoe is a Colorado company cold-calling.
3. **Water cooling advantage** — Louisiana bayous and rivers everywhere. Crusoe's dry-state deployments need air cooling.
4. **Backhaul to AI factory** — flare-site pods connect back to Trappeys/MARLIE 1/Willow Glen via fiber or wireless. Crusoe has standalone cloud; ADC has an integrated network.
5. **DSX-compliant** — ADC builds to NVIDIA spec from day one. Crusoe started with Bitcoin miners.
6. **State incentives** — Louisiana ITEP, Act 730, LED FastStart all apply to ADC's operations. Crusoe doesn't benefit from Louisiana programs.
7. **Regulatory alignment** — January 2024 rule requires "alternative beneficial uses" evaluation. ADC IS the alternative beneficial use.

---

## Competitors in Flare Gas Compute

| Company | Model | Status |
|---------|-------|--------|
| **Crusoe Energy** | DFM + AI cloud. Sold Bitcoin/DFM division (March 2025), now pure AI infra. $10B valuation. | Focused on hyperscale (Abilene/Stargate). NOT in Louisiana. |
| **Giga Energy** | Shipping container Bitcoin miners at well sites. Texas-focused. | Smaller scale, Bitcoin only. |
| **MARA Holdings** | 25 MW micro data centers on wellheads (Texas, North Dakota). Partnership with NGON. | Bitcoin mining. 99% combustion efficiency. Lowest energy cost in their fleet. |
| **EZ Blockchain** | SmartGrid containers at oil/gas sites. | Smaller player, Bitcoin focused. |
| **Genesis Digital Assets** | Flare gas mining operations. | Bitcoin focused. |

**Key insight**: Crusoe pivoted AWAY from flare-site deployments toward hyperscale. MARA and Giga are Bitcoin-only. **Nobody is doing flare-gas AI compute at small/medium scale in Louisiana.** The field is WIDE OPEN.

---

## ADC Flare Gas Deployment Model

### Unit Configuration
- **Gas genset**: INNIO Waukesha VHP (1-1.5 MW) or Caterpillar G3520H (2 MW). Burns wellsite gas.
- **Compute container**: ADC 3K pod with NVIDIA liquid-cooled GPU racks
- **Cooling**: Liquid cooling loop + bayou/river water heat rejection (massive Louisiana advantage)
- **Network**: Starlink for initial connectivity, fiber buildout for high-bandwidth sites
- **Footprint**: ~40x60 ft pad (genset + container + cooling)
- **Deployment**: 2-3 months from agreement to operation

### Revenue Model
- **GPU cloud revenue**: $2-3/GPU-hr for H100/B200 inference
- **Carbon credits**: 63% CO2e reduction vs flaring = sellable credits
- **Gas cost**: $0 or near-$0 (gas has negative value — operator pays penalties to flare it)
- **Electricity cost**: $0.01-0.02/kWh (fuel is free; only cost is genset maintenance)
- **Margin**: 80%+ (free fuel + high GPU rates)

### Phase 1: Proof of Concept (1-2 Sites)
1. Identify 2-3 flare sites within 30 miles of Trappeys/MARLIE 1 (Vermilion, Iberia, St. Martin parishes)
2. Deploy 1 MW genset + 1 ADC 3K pod at each site
3. Backhaul to MARLIE 1 over wireless/fiber
4. Run inference workloads from Trappeys/MARLIE 1 overflow
5. Document emissions reduction for regulatory credit

### Phase 2: Regional Scale (5-10 Sites)
1. Expand to Lafourche, Terrebonne, Cameron, Acadia parishes
2. Deploy standardized genset+pod packages
3. Manage fleet from MARLIE 1 as backup NOC
4. Begin carbon credit sales

### Phase 3: State Scale (20+ Sites)
1. Cover all major producing parishes
2. Network all sites back to Willow Glen primary hub
3. Position as Louisiana's flare mitigation compute provider
4. Pitch to LOGA (Louisiana Oil and Gas Association) as industry solution

---

## The Pitch to Oil Operators

### Version 1: Cold Approach
"You're burning money. We'll take that gas, generate electricity, run AI compute, and you stop paying flaring penalties. Zero cost to you. We bring the container, we bring the generator, we bring the compute. You provide the gas that you're currently setting on fire."

### Version 2: Regulatory Angle
"The January 2024 venting and flaring rule requires you to evaluate alternative beneficial uses before you can get a flaring permit. We ARE the alternative beneficial use. Partner with us and your permit application shows zero routine flaring."

### Version 3: Revenue Share
"We'll pay you for gas you're currently burning AND give you a revenue share on the compute. Your waste stream becomes a profit center. One phone call, we handle everything."

### Version 4: Environmental/ESG
"Every ton of methane you flare is a liability — regulatory, reputational, and soon financial (federal methane fee). We eliminate 63% of your flaring CO2e immediately. That's not just compliance — that's a competitive advantage in ESG-conscious markets."

---

## Key Data Sources for Site Identification

| Source | URL | What It Shows |
|--------|-----|---------------|
| SkyTruth Flaring Map | flaring.skytruth.org | Satellite-detected active flares, updated daily |
| VIIRS Nightfire | eogdata.mines.edu/products/vnf/ | Raw flare detection data with temperature/size |
| EPA FLIGHT | ghgdata.epa.gov | Facility-level GHG emissions for large reporters |
| SONRIS | sonris.com | Louisiana well permits, production, operators |
| SONRIS GIS Map | sonris-gis.dnr.la.gov | Interactive map of all Louisiana wells |
| EIA Vented/Flared | eia.gov/dnav/ng/hist/n9040la2a.htm | Annual state-level flaring volumes |
| DrillingEdge | drillingedge.com/louisiana | Parish-level production, operators, wells |
| MineralAnswers | mineralanswers.com/louisiana | Parish-level activity and producer data |
| ShalExp | shalexp.com/louisiana | Company and production data by parish |

---

## Proximity Analysis — Flare Sites to ADC Facilities

| ADC Facility | GPS | Nearby Oil-Producing Parishes | Distance |
|-------------|-----|-------------------------------|----------|
| **Trappeys** | 30.21356N, 92.00163W | Vermilion, Iberia, St. Martin, Acadia, Lafayette | 10-40 mi |
| **MARLIE 1** | 30.21975N, 92.00645W | Same as Trappeys (half mile away) | 10-40 mi |
| **Willow Glen** | 30.24700N, 91.09850W | Iberville, Ascension, St. James, Plaquemines (via river) | 20-80 mi |

**Water cooling assets nearby**:
- Vermilion River (at Trappeys)
- Bayou Teche (St. Martin, Iberia)
- Atchafalaya Basin (St. Martin, Iberia, St. Mary)
- Mississippi River (at Willow Glen)
- Bayou Lafourche (Lafourche Parish)
- Every south Louisiana flare site is within 5 miles of a waterway

---

## Next Steps

1. **Pull SkyTruth flare map** for south Louisiana — screenshot active flares in Vermilion, Iberia, St. Martin, Acadia, Cameron parishes
2. **Query SONRIS** for active wells with flaring permits in ADC-proximate parishes
3. **Identify 5-10 target operators** with active flares within 30 miles of Trappeys
4. **Spec the genset package** — get quotes from Waukesha/INNIO dealer and Caterpillar (Louisiana has multiple CAT dealers)
5. **Draft operator outreach letter** — tailored to Louisiana regulatory language
6. **Contact LOGA** (Louisiana Oil and Gas Association) — present ADC as flare mitigation solution provider
7. **Model unit economics** — gas volume required per MW, GPU revenue per site, carbon credit value
8. **Crusoe gap analysis** — Crusoe sold their DFM division. Their former customers may need a new provider. Research if any Crusoe DFM sites existed in Louisiana.

---

## Key Numbers for Pitch Decks

- **$82M** of gas wasted annually in Louisiana (2019 EDF study, includes leaks)
- **27 BCF** total gas wasted annually (flaring + venting + leaks)
- **~1.8 BCF** flared/vented in 2024 (EIA)
- **$2.5M** in lost tax/royalty revenue to the state per year
- **31,000** active wells in Louisiana
- **93%** combustion efficiency of open flares (7% methane escapes)
- **99.9%** combustion efficiency of gas engines (Crusoe/MARA proven)
- **63%** CO2-equivalent reduction vs flaring
- **$900-$1,500/ton** federal methane waste emissions charge (2024-2026, if enforced)
- **$10B** Crusoe's valuation — proving the model works
- **$0** cost to the oil operator
- **0** Louisiana competitors doing flare-gas AI compute
