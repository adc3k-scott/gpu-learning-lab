# Heat Reuse — Waste Heat Recovery for Willow Glen AI Factory

## Site Context
- **Location**: Willow Glen Terminal, St. Gabriel, Louisiana (30.24700N, 91.09850W)
- **Climate**: Hot humid — 90F+ summers, 75-80% humidity, 8 months/year
- **Waste heat sources**: 40-45 MW total
  - Gas generators: exhaust at 450-650C, jacket coolant at 80-100C
  - GPU liquid cooling (NVL72 racks): coolant inlet 45C, outlet 65C (20C delta, 130 LPM/rack)
- **Key advantage**: 3,500 ft Mississippi River deepwater frontage with 43-ft dock
- **River water**: ~25-28C summer surface temperature — ideal cold sink for ORC condensers

---

## 1. ORC (ORGANIC RANKINE CYCLE) — BEST OPTION FOR ELECTRICITY GENERATION

### How It Works
Uses organic fluid (pentane, toluene, refrigerants) with low boiling point instead of water. Waste heat vaporizes fluid, drives turbine, generates electricity. Works on low-to-medium temperature heat sources (80-400C).

### Two Separate ORC Systems for Willow Glen

**System A: HIGH-TEMP ORC on Gas Engine Exhaust (450-650C)**
- Efficiency: 20-28% thermal efficiency (best case)
- From 40 MW gas engine exhaust heat: **~8-11 MW additional electricity**
- Working fluid: toluene or silicone oil
- This is proven, mature technology — hundreds of installations worldwide

**System B: LOW-TEMP ORC on GPU Cooling Water (45-65C)**
- Efficiency: 2-5% thermal efficiency (low temperature delta)
- From ~30 MW GPU waste heat: **~0.6-1.5 MW additional electricity**
- CRITICAL: Efficiency is LOW because GPU coolant is only 65C
- Rice University 2025 breakthrough: solar thermal boost (flat-plate solar collectors) pre-heats coolant before ORC, recovering 60-80% more electricity
- At Willow Glen: 2.05 MW solar array on Trappeys could boost GPU coolant temps during daylight
- Working fluid: R245fa, R134a, or ammonia

**CRITICAL INSIGHT: Use Mississippi River water as ORC cold sink**
- River water at ~25-28C in summer vs ambient air at 35C+
- Water-cooled ORC condenser is 15-25% more efficient than air-cooled in Louisiana summer
- The 43-ft deepwater dock is a massive advantage — most ORC plants are stuck with air cooling
- Once-through river cooling or closed-loop cooling tower both viable
- Regulatory note: Clean Water Act Section 316(b) applies; thermal discharge permits needed from LDEQ

### Total ORC Electricity Recovery: ~9-12 MW from 40-45 MW waste heat

### ORC Manufacturers (US-focused)
| Company | HQ | Capacity Range | Notes |
|---------|-----|---------------|-------|
| **Ormat Technologies** | Reno, NV | 1-30 MW per unit | World leader (63% market share). 900+ MW installed globally. 24 plants on US gas pipelines (3-8 MW each). AMERICAN COMPANY. |
| **Turboden** (Mitsubishi) | Brescia, Italy / US offices | 200 kW - 40 MW | 13.4% global share. Owned by MHI. Strong in industrial waste heat. |
| **Infinity Turbine** | US | 10 kW - 1 MW | Supercritical CO2 + ORC hybrid. IT250 = 250 kW at $999K. IT1000 = 1 MW. Specifically targeting data centers. |
| **ElectraTherm** | Reno, NV | 35-110 kW | Small-scale, low-temp specialist. AMERICAN. |
| **Exergy (Enertime)** | Italy | 100 kW - 50 MW | 11.1% global share. Radial outflow turbine design. |

### ORC Cost Estimates (2024-2025)
- CAPEX: **$1.8M - $3.2M per MWe installed**
- For 10 MW ORC system: **$18M - $32M total installed cost**
- Payback: 3-7 years depending on electricity price offset
- O&M: Low — closed-loop system, no combustion, minimal moving parts

### Recommendation
**Ormat Technologies is the obvious first call.** American company, Reno NV, dominant market position, already does gas pipeline waste heat recovery across the US. They can spec a system for both the high-temp exhaust and low-temp coolant streams.

---

## 2. ABSORPTION CHILLERS — BEST OPTION FOR COOLING (Use Heat to MAKE Cold)

### How It Works
Uses waste heat to drive a refrigeration cycle (lithium bromide + water). Heat IN = cold OUT. Counterintuitive but proven for 60+ years. PERFECT for hot climates because you need cooling anyway and have waste heat to burn.

### Why This Is a Home Run for Willow Glen
- Louisiana = 8 months of cooling demand
- AI factory generates massive waste heat AND needs massive cooling
- Absorption chiller converts waste heat into cooling capacity
- Reduces or eliminates need for electric chillers (which consume 30-40% of total facility power in hot climates)
- COP (Coefficient of Performance): 0.7-1.4 depending on single/double effect

### Capacity Calculation
- Single-effect hot water absorption chiller (from GPU 65C coolant): COP ~0.7
- Double-effect steam absorption chiller (from gas exhaust): COP ~1.2-1.4
- From 40 MW waste heat at COP 1.0: **~40 MW (11,400 tons) of cooling capacity**
- This could potentially cover ALL facility cooling needs from waste heat alone

### Absorption Chiller Manufacturers
| Company | HQ | Capacity | Notes |
|---------|-----|----------|-------|
| **YORK (Johnson Controls)** | Milwaukee, WI | 100-2,000 tons | Pioneer since 1960. AMERICAN. Full YORK absorption line. |
| **Trane (Trane Technologies)** | Davidson, NC | 200-2,000 tons | Horizon Series. Hot water or steam driven. AMERICAN. |
| **Carrier** | Palm Beach Gardens, FL | 100-7,000 kW | 16TJ (single-effect), 16NK (double-effect). AMERICAN. |
| **BROAD USA** | Hackensack, NJ | 150-2,000 tons | Chinese parent company, US operations. 35,000+ units in 80 countries. COP up to 6.5 claimed. |
| **Thermax** | India / US offices | Up to 5,000 TR | Large industrial absorption chillers. |

### Cost Estimates
- CAPEX: ~$600/kW-th (~$2,100/ton)
- Operating cost: 6-7 cents/ton-hour (vs 15-20 cents for electric chillers)
- Payback: **2-5 years** (Villanova study showed 4-5 MONTH payback at 10 MW data center scale)
- 3x capital cost vs electric chillers BUT dramatically lower operating cost

### The Trigeneration Play (CCHP)
Gas engines produce electricity + exhaust heat + jacket heat.
- Exhaust heat (high temp) → double-effect absorption chiller OR high-temp ORC
- Jacket heat (low temp) → single-effect absorption chiller
- GPU waste heat (45-65C) → single-effect absorption chiller or low-temp ORC
- Overall system efficiency: **80-95%** (vs 35-40% for power-only)

### Recommendation
**YORK (Johnson Controls) or Trane for absorption chillers.** Both American, both proven at scale, both have hot-water and steam-driven models. Get quotes for a trigeneration setup where gas engine waste heat drives absorption chillers that cool the GPU racks.

---

## 3. THERMAL ENERGY STORAGE (TES)

### Why It Matters for Willow Glen
- Solar produces power during daytime only
- AI factory runs 24/7
- Store excess thermal energy during day, use at night
- Can also store "cold" during off-peak for peak shaving

### Technologies

**Ice/Cold Storage (IceBricks)**
- Nostromo IceBrick 360: specifically designed for data centers
- DOE loan guarantee: $305.5M to deploy across California data centers
- Make ice at night (cheap power), use for cooling during day (expensive power)
- Reduces peak cooling electricity demand by 20-40%

**Phase Change Materials (PCM)**
- Store heat at specific temperature using material phase transition
- Can reshape thermal profile — "Thermal Time Shifting"
- Commercial products available for data center temperature ranges

**Molten Salt (High Temp)**
- 33x cheaper than lithium-ion batteries for thermal storage
- Better suited for high-temp industrial applications
- Could store gas engine exhaust heat for continuous ORC operation

### Recommendation
**Ice storage for peak-shaving cooling loads.** Nostromo IceBrick is purpose-built for data centers. Make ice at night with cheap power, deploy cold during peak afternoon hours. Secondary: investigate molten salt for storing gas engine heat if engines cycle on/off.

---

## 4. SUPERCRITICAL CO2 POWER CYCLES

### Status: EMERGING — Not Yet Commercially Mature at Scale

- 10 MWe STEP Demo pilot in San Antonio, TX: completed Phase 1, generated 4 MWe at 500C
- Infinity Turbine (US): selling sCO2 systems up to 1 MW, specifically targeting data centers
- Advantages over ORC: more compact, no flammability concerns, potentially higher efficiency
- Disadvantages: less proven, fewer commercial installations, higher capital cost

### Practical Assessment
- **NOT ready for 40 MW scale** — largest demo is 10 MWe
- **Could be viable in 3-5 years** as technology matures
- Infinity Turbine's smaller units (250 kW - 1 MW) could serve as pilot/proof of concept
- Keep watching Hanwha, GE, Southwest Research Institute for commercial scale-up

### Recommendation
**Not yet. Monitor.** Stick with ORC for near-term deployment. sCO2 may be the next-generation replacement. Infinity Turbine's IT250 ($999K) could be a pilot test unit.

---

## 5. THERMOELECTRIC GENERATORS (TEG)

### Status: NOT PRACTICAL AT THIS SCALE

- Commercial efficiency: ~5% (theoretical max with new materials: 15-20%)
- No moving parts, silent, decades of life
- Global market: $472M (2021), growing to $1.44B by 2030
- Good for: sensors, remote power, auxiliary systems
- Bad for: MW-scale power generation

### Practical Assessment
- At 5% efficiency on 40 MW: only 2 MW output
- Cost per watt is dramatically higher than ORC
- Material costs (bismuth telluride, etc.) don't scale economically
- TEGs make sense for niche applications (waste heat from individual server exhaust, remote sensors)

### Recommendation
**Skip for primary waste heat recovery.** Not cost-effective at MW scale. ORC beats TEG in every metric that matters for Willow Glen.

---

## 6. KALINA CYCLE

### How It Differs from ORC
Uses ammonia-water mixture as working fluid. Variable boiling point allows better heat recovery from some sources. Licensed technology (KALiNA Power, formerly Wasabi Energy).

### Performance
- Claims 50% more output than ORC in suitable applications
- Best at LOW temperature sources (which fits GPU coolant at 45-65C)
- 16 commercial plants worldwide
- Licensed through Siemens and Shanghai Shenge

### Practical Assessment
- Fewer installations than ORC (16 vs hundreds)
- Ammonia handling adds safety complexity
- Limited US manufacturer base
- Technology is proven but niche

### Recommendation
**Consider as alternative to low-temp ORC for GPU coolant stream.** Worth getting a quote from KALiNA Power to compare against Ormat's low-temp ORC offering. The ammonia-water mixture may extract more electricity from the 45-65C GPU coolant than ORC can.

---

## PRIORITY RANKING FOR WILLOW GLEN

| Priority | Technology | Expected Output | Est. Cost | Payback |
|----------|-----------|----------------|-----------|---------|
| **1** | **Absorption Chillers** | 11,000+ tons cooling (eliminates electric chillers) | $25-40M | 2-5 years |
| **2** | **High-Temp ORC** (gas exhaust) | 8-11 MW electricity | $18-32M | 3-7 years |
| **3** | **Thermal Storage** (ice) | Peak shaving, 20-40% cooling savings | $5-15M | 3-5 years |
| **4** | **Low-Temp ORC or Kalina** (GPU coolant) | 0.6-1.5 MW electricity | $3-8M | 5-10 years |
| **5** | **sCO2 pilot** (monitor) | 250 kW - 1 MW test | ~$1M | R&D |

### Combined Value
- **Total recovered electricity**: 9-12+ MW (worth $5-8M/year at $0.06/kWh)
- **Eliminated cooling electricity**: 10-15 MW equivalent (worth $5-10M/year)
- **Total annual value**: $10-18M/year from waste heat recovery
- **Total CAPEX**: $50-95M
- **System payback**: 3-6 years

---

## PREVIOUS NOTES (Cold Climate / Edge Deployment Concepts)

### Core Insight
Every watt into a GPU comes out as heat. 100%. A 270 kW pod is a 270 kW heater that also does math. Don't get rid of heat -- SELL it twice (compute + thermal energy).

### Cold Climate Heat Reuse Products (for edge deployments, NOT Willow Glen)
- **Residential/Apartment**: GPU pod in basement, oil-to-water heat exchanger, free heat for tenants
- **Commercial Building**: Immersion tank in server closet, hydronic heating
- **Small Business ("GPU Water Heater")**: One board in sealed box, heats domestic hot water
- **Restaurant/Food Service**: 24/7 operations, heat supplements griddle/fryer energy
- These concepts apply to NORTHERN deployments and edge nodes, not Louisiana facilities
