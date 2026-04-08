# Crusoe Energy Playbook — Flare Gas to $10B+ AI Infrastructure Company

**Compiled**: 2026-03-24
**Purpose**: Reverse-engineer Crusoe's model for ADC strategic positioning

---

## 1. FOUNDING STORY & TIMELINE

- **Founded**: 2018, Denver, Colorado
- **Founders**: Chase Lochmiller (CEO, MIT/Stanford ML, ex-quant/HFT, crypto hedge fund) + Cully Cavness (COO, Middlebury College geology, oil & gas family)
- **Origin**: Hiking Colorado 14ers in 2017, discussing waste flaring. Cavness embarrassed by industry waste, Lochmiller saw compute opportunity
- **Original name concept**: "Island Clouds" — archipelago of isolated data centers
- **Company name**: After Robinson Crusoe (resourcefulness in isolation)
- **Initial product**: Crypto mining powered by flare gas (Digital Flare Mitigation)
- **Key pivot**: Sold Bitcoin mining division to NYDIG (March 2025, ~135 employees transferred) to go 100% AI cloud

### Funding History
| Round | Date | Amount | Lead | Valuation |
|-------|------|--------|------|-----------|
| Series B | April 2021 | $128M | — | — |
| Series C | 2024 | $600M | Founders Fund (Peter Thiel) | $2.8B |
| Series E | October 2025 | $1.38B | Valor Equity Partners, Mubadala | $10B+ |
| **Total raised** | — | **$3.9B+ (debt + equity)** | — | — |
| Credit facilities | Various | $750M (Brookfield) + $225M (Upper90) + $175M (Victory Park) | — | — |
| Stargate-specific | 2025 | $11.6B (debt/equity, Blue Owl Capital) | — | — |

### Revenue Trajectory
| Year | Revenue | Growth |
|------|---------|--------|
| 2023 | $152M | — |
| 2024 | $276M | +82% YoY |
| 2025 (projected) | $998M | +262% YoY |
| 2026 (projected) | ~$2B | +100% YoY |

**2024 Revenue split**: AI Cloud $124M (45%), Crypto Mining $152M (55%). Cloud projected to reach 70-80% by end of 2025.

---

## 2. THE DFM (DIGITAL FLARE MITIGATION) MODEL — HOW IT WORKS

### The Problem
When oil is extracted, associated natural gas comes up as a byproduct. In remote areas without pipeline infrastructure, it is cheaper to flare (burn) this gas than to capture and transport it. The US flared ~0.5 Bcf/day in 2023. North Dakota alone flared 5.1% of gross withdrawals.

### The Solution
Crusoe deploys mobile, modular data centers directly at wellheads. Instead of flaring the gas, reciprocating engines burn it more efficiently to generate electricity, which powers containerized GPU clusters.

### Environmental Value Proposition
- **98% reduction** in methane emissions vs open-air flaring
- **63% reduction** in CO2-equivalent emissions (engines combust more completely than open flares)
- **4.4 metric tons CO2e avoided** per DFM-powered GPU per year
- Cumulative through 2025: **21+ billion cubic feet captured**, **2.5 TWh electricity generated**, **2.7 million metric tons CO2 avoided**
- 2024 alone: 10 BCF gas consumed, 1.3 TWh power generated

### How They Pitch Oil Operators
1. **"Free flare mitigation"** — Crusoe takes the gas at no cost to the operator (or pays a small amount)
2. **Regulatory compliance** — EPA methane rules tightening; operators face fines for flaring. Crusoe solves this overnight
3. **ESG reporting** — Operators get verifiable emissions reduction metrics
4. **Zero capex for operator** — Crusoe owns and deploys all equipment
5. **Original pitch tool**: "A video of a gas flare getting smaller as a Bitcoin wallet grew in size"
6. **Key operator clients**: Equinor, Kraken Oil & Gas, EnerPlus, Devon Energy, Exxon

### Per-Site DFM Economics
- **Typical DFM site**: 1-10+ modules per site, modular and scalable
- **Power per module**: ~250 kW per compute module (Spark spec)
- **Gas consumption**: ~10 million cubic feet/day across entire fleet (86 modules, 30 sites)
- **Implied per-module**: ~100-120 MCF/day per module (rough estimate)
- **Total DFM fleet (peak)**: 250+ MW across 7 US states + Argentina
- **86 mobile data centers across 30 sites** in major US oil fields

### What Operators Get
- Compliance with EPA methane rules (EPA's Quad Oa/OOOOb/OOOOc)
- Reduced flaring on permits (important in North Dakota, Wyoming, Montana)
- Revenue share or gas purchase payments
- ESG/sustainability metrics for reporting

---

## 3. GENERATOR SPECIFICATIONS

### DFM Wellsite Generators (Phase 1 — Flare Gas)
- **Brand**: INNIO Waukesha
- **Model**: VHP9504GSI Series Five gensets
- **Type**: Rich-burn, natural gas reciprocating engines
- **Key capability**: Can run on wellhead gas DIRECTLY without complex fuel treatment
- **Emissions**: Three-way catalyst for low emissions
- **Deployment**: "Large portion of Crusoe's fleet" powered by Waukesha engines
- **Robustness**: Built on same platform as compression engines (oil & gas grade)

### Large-Scale AI Factory Generators (Phase 2 — Abilene/Stargate)
- **Brand**: GE Vernova
- **Model**: LM2500XPRESS aeroderivative gas turbines
- **Power output**: 35 MW per unit
- **Order**: 29 units = ~1 GW combined
- **Fuel**: Dual-fuel (natural gas + future hydrogen blend capability)
- **Assembly**: 95% factory-assembled
- **Installation**: As little as 2 weeks per unit
- **Startup**: 5-minute start capability
- **Emissions**: SCR (Selective Catalytic Reduction) — 90% lower emissions than reciprocating engines, near-zero methane slip
- **Use case**: Backup power for Abilene data halls (primary = ERCOT grid/wind)

### ADC COMPARISON NOTE
ADC's approach with Siemens recip engines at Trappeys and CCGT at Willow Glen aligns with Crusoe's evolution — they started with recip engines at wellheads and graduated to turbines for large-scale facilities.

---

## 4. GAS QUALITY HANDLING

- Waukesha VHP9504GSI runs on **wellhead gas directly** — no complex treatment needed
- This was a KEY differentiator: most generators require cleaned/dried gas
- Wellhead gas is variable in composition, temperature, flow rate, and may contain:
  - Wet gas (natural gas liquids, condensate)
  - Trace H2S (sour gas)
  - Variable BTU content
  - Fluctuating pressure and flow
- For more challenging gas quality, third-party fuel gas conditioning (e.g., GTUIT) provides modular treatment at the wellhead
- Rich-burn engines are more tolerant of gas quality variation than lean-burn alternatives

---

## 5. CONTAINER/MODULE DESIGN

### Original DFM Modules
- Shipping container-sized modular units
- Contain: power generation + compute racks + cooling + telecommunications
- Designed for rapid mobilization and demobilization
- Can relocate as well production declines (critical for decline curve economics)

### Crusoe Spark (Current Generation — 2025/2026)
- **Form factor**: Shipping container-sized, portable
- **Integrated systems**: Power, cooling, GPU racks, remote monitoring, fire suppression, power distribution, security access, dust-proof vestibules
- **Rack density**: 12.5 kW to 25 kW per rack, 250 kW per module
- **Scalability**: Hundreds of kW to hundreds of MW (modules group into clusters)
- **Cooling (current)**: Air-cooled with redundant HVAC
- **Cooling (H2 2026)**: Liquid-cooled version for next-gen GPU density
- **Deployment speed**: As little as 3 months from order
- **Units deployed**: 400+ globally as of June 2025
- **Manufacturing**: Spark Factory, Brighton, CO — 352,000 sq ft, 200+ jobs, $200M+ investment
- **First factory-produced units**: Q3 2026
- **Power source flexibility**: Solar + EV batteries, grid, natural gas, SMRs (small modular nuclear)

### Crusoe Edge Zones (Announced 2026)
- Spark-powered, geographically distributed AI inference clusters
- **Performance**: 9.9x faster time-to-first-token, 5x higher throughput vs standard configs
- **Technology**: MemoryAlloy — cluster-wide KV cache fabric (proprietary)
- **Targets**: Low-latency inference, data sovereignty, regulated industries, government

---

## 6. COOLING SYSTEMS

### DFM Wellsite (Early)
- Air-cooled, containerized HVAC
- Designed for harsh conditions (North Dakota winters, Montana remote sites)
- Redundant systems

### Abilene Flagship (Current)
- **Direct-to-chip liquid cooling**
- **Zero-water evaporation** closed-loop system
- Initial fill: 1 million gallons per building
- Annual maintenance: ~12,625 gallons per building per year
- Water continuously recirculated — zero consumption during heat rejection
- Carbon steel and copper piping
- Air-cooled chillers for heat rejection

### Spark Modules
- Air-cooled (current generation)
- Liquid-cooled (H2 2026) for ultra-high-density next-gen GPU clusters

---

## 7. REMOTE SITE OPERATIONS

- **Monitoring**: 24/7 support across 4 time zones
- **Response time**: <6 minutes average
- **Resolution time**: 24 hours
- **SLA**: 99.5% uptime guarantee
- **Remote monitoring**: Built into every Spark module
- **Connectivity**: Not publicly detailed, but DFM sites in remote oil fields used satellite (Starlink/VSAT inferred) + cellular where available
- **Security**: Steel structures, access controls, dust-proof vestibules

---

## 8. REVENUE MODEL & ECONOMICS

### Revenue Streams
1. **Crusoe Cloud** — GPU-as-a-Service (IaaS), on-demand and spot instances
2. **Hyperscale infrastructure leasing** — Long-term contracts (e.g., Oracle/OpenAI Stargate)
3. **Crusoe Industries** — Manufacturing (switchgear, modular units, electrical components)

### Pricing (On-Demand)
| GPU | Crusoe $/hr | AWS $/hr | Savings |
|-----|------------|----------|---------|
| A100 80GB | $1.95 | $4.10 | ~52% |
| A100 80GB (spot) | $1.30 | — | — |
| MI300X | $3.45 | — | — |

### Cost Advantages
- **Energy cost**: 30-50% lower than traditional hyperscalers
- **Stranded gas**: Electricity at ~1/13th standard grid cost (early DFM model)
- **Energy = 60%+ of AI data center opex** — so cheaper power = structural margin advantage
- **Vertical integration**: Built own switchgear factory when lead times hit 100 weeks (cut to 22 weeks)

### Unit Economics (Abilene)
- **Capital deployed**: $3.4B for West Texas campus
- **Payback period**: 2-3 years
- **Projected IRR**: 45%
- **Base ROI**: 5x
- **Leveraged ROI**: 8.7x
- **Revenue projection**: $250M for 2026 from Abilene alone (25x original $10M projection)
- **Economic impact**: $1B+ local over 20 years
- **Interest expense**: ~$300M annually by end of 2025

---

## 9. SCALE & INFRASTRUCTURE (Current)

### Compute Fleet
- **Total footprint**: 9.8 million sq ft
- **GPU capacity**: Up to 946,000 GPUs
- **Power available**: 3.4 GW electricity
- **Power pipeline**: 45+ GW (4x growth in 2025)
- **Team**: 1,000+ FTEs, 5,000+ contractors (Abilene alone)

### Major Sites
| Site | Location | Power | Status |
|------|----------|-------|--------|
| Abilene Campus | Texas | 1.2 GW (expanding) | Phase 1 live (200+ MW), Phase 2 mid-2026 |
| Wyoming Campus | Wyoming | 1.8 GW | Announced |
| Energy Vault | Snyder, TX | 25 MW (scaling) | Deploying 2026 |
| Redwood Materials | — | 12 MW microgrid | Live, expanding 7x |
| Iceland | — | — | Liquid cooling + Blackwell |
| DFM fleet | 7 US states + Argentina | 250+ MW | Operating |

### Energy Supply
- **4.5 GW natural gas** secured (GE Vernova turbines + other sources)
- **Wind/solar**: Abilene = one of windiest locations in Texas
- **Batteries**: Form Energy iron-air (12 GWh order), Redwood Materials repurposed EV batteries
- **Future**: SMR nuclear compatibility designed into Spark modules

---

## 10. PATENTS & IP

### Issued Patents
- **5 issued patents** (as of public record)
- US Patent 10,862,307 and 10,862,309 — core DFM technology
- Priority date: August 1, 2018
- Named inventors: Charles Cavness, Chase Lochmiller, Kenneth Parker
- Primary category: "Generation; Conversion Or Distribution Of Electric Power"
- **Digital Flare Mitigation** is a registered trademark

### IP Strategy
- Cross-licensing agreement with **Lancium** (another energy-first compute company)
- **Patent litigation**: Upstream Data (Canadian flare gas miner) sued Crusoe for infringement — claims Crusoe's tech infringes on founder Stephen Barbour's patent
- **Proprietary tech**: MemoryAlloy (cluster-wide KV cache fabric for inference)

---

## 11. CHALLENGES, PROBLEMS & LESSONS LEARNED

### What Went Wrong / What Was Hard

1. **Oil well decline curves** — Wells produce less gas over time. If your data center is powered by a declining well, you lose power. SOLUTION: Made everything mobile/modular so they can pick up and move to next site.

2. **Short-term gas agreements** — Oil operators don't guarantee long-term gas supply. Creates revenue uncertainty. SOLUTION: Diversified beyond flare gas to grid, wind, solar, batteries.

3. **Pipeline infrastructure gaps** — No midstream infrastructure near producing wells, delayed pipeline arrival, pipeline capacity challenges, extended gas plant downtime. SOLUTION: Turned the bug into a feature (co-locate at the well, bypass pipelines entirely).

4. **Supply chain bottlenecks** — Low voltage switchgear quotes hit 100-week lead times. SOLUTION: Built their own factory. Cut lead times to 22 weeks. This became Crusoe Industries revenue stream.

5. **Crypto volatility** — Bitcoin mining revenue fluctuates wildly with crypto prices. SOLUTION: Pivoted to AI cloud (more predictable revenue, higher margins, better for capital markets).

6. **Scaling beyond wellpads** — DFM maxes out at wellpad scale (single-digit MW per site). AI training needs 100+ MW clusters. SOLUTION: Built Abilene (grid-connected, 1.2 GW) while keeping DFM for edge/distributed use.

7. **Gas quality variation** — Wellhead gas composition varies site to site. SOLUTION: Chose Waukesha engines specifically because they run on raw wellhead gas without treatment.

8. **Remote operations** — Sites in middle of nowhere (Montana, North Dakota badlands). SOLUTION: Built robust remote monitoring, satellite connectivity, <6-minute response time SLA.

9. **Capital intensity** — Asset-heavy model requires massive upfront investment. SOLUTION: Raised $3.9B+, leveraged project finance (Blue Owl for Stargate), credit facilities.

10. **Interest expense** — $300M/year by end 2025. High leverage = high risk if revenue projections miss.

### Key Strategic Lessons

- **Energy-first, compute-second** — The moat is power, not GPUs. Anyone can buy GPUs. Cheap, reliable power at scale is the real competitive advantage.
- **Vertical integration** — When supply chain fails, build it yourself. Crusoe Industries now makes switchgear, modular units, electrical components.
- **Modularity = survivability** — If you can't move your data center, you're stuck when conditions change (well decline, regulation, power source shift).
- **Start small, scale up** — DFM wellpads (250 kW) taught them operations before building Abilene (1.2 GW).
- **Follow the bigger market** — Crypto mining was the wedge, AI cloud is the endgame. Don't be precious about your original business.

---

## 12. SPARK FACTORY — MODULAR AI FACTORY PRODUCT

### Facility
- **Location**: Brighton, Colorado
- **Size**: 352,000 sq ft
- **Investment**: $200M+
- **Jobs**: 200+ local + supply chain
- **First units**: Q3 2026

### Product (Crusoe Spark)
- Factory-manufactured, standardized AI compute modules
- 3-month delivery from order
- Air-cooled (now), liquid-cooled (H2 2026)
- Scalable: individual units (250 kW) to clustered campuses (100+ MW)
- Compatible with: solar, EV batteries, grid, natural gas, SMR nuclear
- Integrated: power, cooling, monitoring, fire suppression, security, GPU racks
- 400+ units deployed globally as of mid-2025

### Why This Matters for ADC
Crusoe is treating AI infrastructure as a **manufactured product** — same playbook ADC is developing with the ADC 3K pod concept. Key difference: ADC builds to NVIDIA DSX reference design; Crusoe builds proprietary. ADC's advantage: NVIDIA certification path (NCP), university partnerships, Louisiana incentives.

---

## 13. LOUISIANA FLARE GAS OPPORTUNITY — THE MATH

### Louisiana Flaring Data (EIA)
| Year | Vented & Flared (MMCF) |
|------|----------------------|
| 2020 | 4,491 |
| 2021 | 3,499 |
| 2022 | 3,816 |
| 2023 | 1,990 |
| 2024 | 1,847 |

Louisiana flares ~1.8-4.5 BCF/year (declining trend). This is SMALL compared to:
- **Texas**: ~73 BCF/year (0.2 Bcf/d x 365)
- **North Dakota**: ~5.1% of ~3 Bcf/d = ~56 BCF/year

### Energy Conversion Calculation
```
Louisiana flared gas (2024):         1,847 MMCF = 1.847 BCF/year
Average BTU content:                 ~1,020 BTU/CF (associated gas)
Total energy:                        1.847B CF x 1,020 BTU/CF = 1.884 trillion BTU/year
Convert to kWh:                      1.884T BTU / 3,412 BTU/kWh = 552 million kWh/year
At 35% gen efficiency:               193 million kWh/year usable electricity
Continuous MW equivalent:            193M kWh / 8,760 hrs = ~22 MW continuous

At Crusoe's ~250 kW per module:     ~88 Spark modules could be powered
At 8 GPUs per module (estimate):     ~704 GPUs
```

### The Honest Assessment
**Louisiana's flare gas alone is NOT a major compute opportunity** (~22 MW). It's a rounding error compared to Crusoe's 4.5 GW pipeline.

### BUT — Louisiana's REAL Opportunity is NOT Flare Gas

Louisiana's advantage is DIFFERENT from Crusoe's origin story:

| Factor | Crusoe (Flare Gas Origin) | ADC (Louisiana) |
|--------|--------------------------|-----------------|
| Power source | Stranded wellhead gas | Henry Hub natural gas ($2-3/MMBtu) + 2.05 MW solar + grid sell-back |
| Power cost | ~1/13th grid (but small scale) | $0.04-0.068/kWh at scale (competitive with any US market) |
| Scale potential | Started at kW, now GW via grid | 100+ MW from day one (Willow Glen = former 2,200 MW station) |
| Cooling | Closed-loop liquid (built from scratch) | Mississippi River water (Willow Glen) + water tower (Trappeys) — FREE cooling |
| Workforce | Imported to remote sites | 25 years of ROV/offshore tech workforce IN STATE |
| University | None (built own training) | UL Lafayette (anchor tenant, R1 research, grants) + LSU |
| Incentives | Colorado/Texas standard | ITEP ($8-16M), Act 730 (20-year sales tax exemption, $200M+), Historic Tax Credits (45-55%), LED FastStart (free training) |
| Manufacturing | Built Spark Factory (352K sq ft, $200M) | First Solar factory 30 mi away (panels), Baton Rouge + New Iberia cassette factory |
| Certification | Proprietary (no NVIDIA cert) | NVIDIA DSX reference design, NCP certification path |
| Grid advantage | Abilene = ERCOT (wind) | Willow Glen = sell BACK to grid (Layer 4), not dependent on it |

### What ADC Should Take From Crusoe

1. **"Energy-first" branding works** — Investors respond to "we solved the power problem." ADC has this with the 4-layer hierarchy.
2. **Modular manufacturing is the future** — ADC 3K pods = same thesis as Spark Factory. Get factory running ASAP.
3. **Vertical integration wins** — Crusoe built switchgear factory when supply chain failed. ADC should control pod manufacturing end-to-end.
4. **Start with the wedge, scale to the platform** — Crusoe: flare gas crypto -> AI cloud. ADC: Trappeys proof of concept -> Willow Glen at scale.
5. **University partnerships are a gap Crusoe never filled** — ADC + UL Lafayette + LSU = workforce pipeline, research grants, credibility that Crusoe lacks.
6. **Cooling is ADC's secret weapon** — Mississippi River + water tower cooling costs nearly nothing. Crusoe spent massively on closed-loop liquid cooling systems. ADC gets this for free.
7. **Louisiana incentive stack is unmatched** — ITEP + Act 730 + Historic Tax Credits + LED FastStart = $200M+ in savings Crusoe doesn't get in Colorado/Texas.

---

## 14. COMPETITIVE POSITIONING — ADC vs CRUSOE

### Where Crusoe Wins
- First mover (8 years of operations)
- $3.9B+ raised, $10B+ valuation
- 1,000+ employees, proven at GW scale
- Stargate/OpenAI partnership
- 45+ GW power pipeline
- Global brand recognition
- MemoryAlloy inference technology

### Where ADC Wins
1. **NVIDIA-native** — DSX reference design, NCP certification path. Crusoe is proprietary.
2. **Louisiana power economics** — Henry Hub pricing ($2-3/MMBtu) at the source. Gas doesn't need to be transported.
3. **Free cooling** — Mississippi River (Willow Glen) and water tower (Trappeys) vs Crusoe's engineered cooling systems.
4. **Brownfield advantage** — Willow Glen (former 2,200 MW station) and Trappeys (existing buildings) = faster permitting, existing infrastructure.
5. **University partnerships** — UL Lafayette, LSU = workforce, research, grants ($28-55M+ potential). Crusoe has none.
6. **Incentive stack** — $200M+ in Louisiana tax incentives Crusoe can't access.
7. **American manufacturing** — First Solar 30 mi away, cassette factory in-state. Crusoe's supply chain is distributed.
8. **Workforce** — 25 years of ROV/offshore/deepwater expertise already in Louisiana. Crusoe imports workers to remote sites.
9. **Sell-back grid model** — Layer 4 power hierarchy sells excess to grid. Crusoe buys FROM grid at Abilene.
10. **Newer hardware** — ADC deploys NVIDIA liquid-cooled NVL72 racks (latest gen). No legacy fleet to manage.

### The Pitch
"Crusoe proved the energy-first AI infrastructure model works — $152M to $2B in 3 years. ADC is building the Louisiana version with three advantages Crusoe will never have: Mississippi River cooling, a 15-program state incentive stack worth $200M+, and NVIDIA DSX certification. Crusoe started at oil wells in North Dakota. We're starting at a former 2,200 MW power station with river water cooling and a flagship university partnership."

---

## SOURCES

- [Contrary Research — Crusoe Business Breakdown](https://research.contrary.com/company/crusoe)
- [Sacra — Crusoe at $276M Revenue](https://sacra.com/research/crusoe-at-276m-revenue/)
- [Crusoe — Spark Factory Announcement](https://www.crusoe.ai/resources/newsroom/crusoe-announces-new-manufacturing-facility-to-produce-modular-ai-factories)
- [Crusoe — Edge Zones](https://www.crusoe.ai/resources/newsroom/crusoe-unveils-crusoe-edge-zones)
- [GE Vernova — LM2500XPRESS for Crusoe](https://www.gevernova.com/gas-power/resources/case-studies/crusoe-ai-data-centers-lm2500xpress)
- [Crusoe — Abilene Data Center Inside Look](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center)
- [INNIO Waukesha — Crusoe DFM Deployments](https://www.innio.com/en/news-media/press-releases/innio-waukesha-brings-electrical-power-to-remote-stranded-gas-locations-powers-innovative-crusoe-digital-flare-mitigation-deployments/)
- [Crusoe — Series E Announcement ($10B+ Valuation)](https://www.crusoe.ai/resources/newsroom/crusoe-announces-series-e-funding)
- [CNBC — Crusoe Sells Bitcoin Mining to NYDIG](https://www.cnbc.com/2025/03/25/crusoe-energy-sells-bitcoin-mining-unit-to-nydig-to-focus-on-ai.html)
- [EIA — US Natural Gas Vented and Flared](https://www.eia.gov/todayinenergy/detail.php?id=62383)
- [EIA — Louisiana Natural Gas Vented and Flared](https://www.eia.gov/dnav/ng/hist/n9040la2a.htm)
- [DCD — Crusoe Pivots to AI Data Centers](https://www.datacenterdynamics.com/en/news/crusoe-pivots-to-building-data-centers-plans-100mw-facility/)
- [Crusoe — Redwood Materials Partnership](https://www.crusoe.ai/resources/newsroom/crusoe-and-redwood-materials-expand-strategic-partnership-scaling-to-7x-the-original-ai-infrastructure-density)
- [Crusoe — GE Vernova 29-Unit Turbine Deal](https://www.crusoe.ai/resources/newsroom/ge-vernova-and-crusoe-announce-major-29-unit-gas-turbine-deal)
- [Crusoe — Energy Vault Partnership](https://www.businesswire.com/news/home/20260211881549/en/Energy-Vault-and-Crusoe-Announce-Strategic-Framework-Agreement-for-Deployment-of-Crusoe-Spark-Modular-AI-Factory-Units-to-Deliver-Crusoe-Cloud)
- [Crusoe Cloud Pricing](https://www.crusoe.ai/cloud/pricing)
- [Upstream Data v. Crusoe Patent Lawsuit](https://www.coindesk.com/policy/2023/05/23/upstream-data-sues-crusoe-energy-over-waste-gas-mining-patent)
- [Lancium + Crusoe Cross-Licensing](https://www.crusoe.ai/resources/newsroom/lancium-and-crusoe-cross-licensing-intellectural-property)
- [Bain Capital — Crusoe's Climb](https://baincapitalventures.com/insight/crusoe-climb-betting-on-power-before-ai-was-cool/)
- [Denver Post — Spark Factory in Brighton](https://www.denverpost.com/2026/03/18/crusoe-ai-data-center-factory/)
- [EDF — Louisiana Natural Gas Waste](https://www.edf.org/media/new-analysis-quantifies-natural-gas-waste-and-pollution-louisiana)
- [North Dakota Legislature — Crusoe DFM Testimony (Dale Patten)](https://ndlegis.gov/assembly/67-2021/testimony/SFINTAX-2137-20210112-1174-N-PATTEN_DALE.pdf)
- [Crusoe — Understanding the Problem](https://www.crusoe.ai/resources/blog/understanding-the-problem-crusoe-solves)
