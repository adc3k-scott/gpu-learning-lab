# Delta Electronics -- Complete 800V DC Product Line for AI Factories
Last updated: 2026-03-25

## Company Overview
- **HQ**: Taipei, Taiwan (founded 1971 by Bruce Cheng)
- **Market Cap**: ~$30B+ (TPE:2308)
- **2025 Revenue**: 554.89B TWD (~$17B USD), 31.76% YoY growth
- **TTM Revenue (Mar 2026)**: ~$14.86B USD
- **US HQ**: Fremont, California
- **US Manufacturing**: Plano, Texas -- 435,000 sq ft existing facility at 601 Data Dr
  - Phase 2: +477,000 sq ft mfg + 90,000 sq ft office (complete by 2028)
  - Phase 3: +477,000 sq ft (complete by 2031)
  - Total campus: ~1.5 million sq ft, 1,500+ employees
  - Focus: AI/cloud data center power, 5G, EV charging, energy infra
  - Markets as "Made in the USA" solutions
  - Committed to RE100 (100% renewable by 2030)
- **IMPORTANT -- What's Made Where**:
  - Plano TX: Power racks, power shelves, DC/DC converters, PSUs = AMERICAN MADE
  - Croatia: Xubus Node / Powertrain modular data centers = EMEA ONLY, not available in US
  - CDUs/cooling: Manufacturing location unclear (likely Asia)
  - SST: Prototype stage, location unclear
  - SOFC: Licensed from Ceres Power (UK), production location unclear
  - **For ADC: Delta power components are American. Complete modular solutions are NOT.**
  - **Pair Delta power (Plano) + American container (GTI/Cajun) + American cooling (BAC/CoolIT)**
- **Data Center Division**: Infrastructure Business (IFB), led by EVP Johnson Lee
- **Americas Sales**: Dave Morse, VP Sales & Product; Alex Lee, VP Channel Business
- **R&D**: Ralf Pieper, R&D Director Custom Design BU (ORV3, DC/DC converters)

---

## 1. 800V DC POWER PRODUCTS

### 1A. 660 kW In-Row Power Rack
- **Configuration**: 6x 110 kW hot-swappable AC-DC power shelves
- **Battery Backup**: 80 kW BBU per shelf = 480 kW total embedded backup (eliminates separate UPS)
- **PSU**: 18.5 kW AC/DC power supply units with aluminum capacitors for energy storage
- **Input**: 3-phase 400-480 VAC
- **Output**: 800 VDC
- **Efficiency**: Up to 98% AC-DC
- **Form Factor**: Standard 19-inch rack
- **Features**: LCD touch panel, lockable door (tool safety), seismic-rated with anchor kits
- **Designed for**: GPU workload behavior and high-frequency dynamic distortion
- **Status**: SHIPPING -- shown at OCP 2025, COMPUTEX 2025, GTC 2026
- **Est. Pricing**: $80K-150K per rack (unconfirmed)
- **Product image**: https://filecenter.deltaww.com/products/images/2509/202509241130369816001.png
- **Product page**: https://www.deltaww.com/en-US/products/dc-power-systems/800-vdc-in-row-power

### 1B. 1.1 MW In-Row Power System
- **Configuration**: Multiple 106 kW HVDC power shelves
- **Input**: 400-480 VAC
- **Output**: 800 VDC
- **Total Capacity**: Up to 1.1 MW in-row power delivery
- **Efficiency**: Up to 98%
- **Form Factor**: Standard 19-inch rack footprint
- **Purpose**: Bridges legacy infrastructure with next-gen rack designs
- **Features**: LCD touch panel, lockable door, seismic-rated

### 1C. AC-DC Server Power Shelves
- **180 kW (2OU)**: Converts 3-phase 415-480VAC to 800VDC, up to 98% efficiency
- **72 kW (1OU)**: Same conversion, 98% efficiency, compact form factor
- **55 kW**: For containerized data center deployments

### 1D. DC-DC Power Shelves
- **90 kW (1RU)**: Converts 800VDC to 50VDC, up to 98.5% efficiency, 180% transient response
- Designed for NVIDIA MGX architecture
- Includes management switch in rack configuration

### 1E. HVDC/DC Power Distribution Board
- **Output**: 800V to 12V
- **Maximum Efficiency**: 98.5%

### 1F. Energy Variance Appliance (EVA) Rack
- **Purpose**: Foundation of 800VDC architecture -- stabilizes and protects GPU infrastructure
- **Efficiency**: Up to 97% at full load
- **Function**: Maintains limited peak-to-average AC input current ratio
- **Key Feature**: Uses energy storage to smooth GPU peak load profiles (eliminates overshoots/undershoots)

### 1G. Power Capacitance Shelf (PCS)
- **Type**: Built-in supercapacitors
- **Backup**: 20 kW for 15 seconds during outages
- **Function**: Smooths AC-side load fluctuations, provides second-level backup

### 1H. e-Fuse Module
- **Technology**: SiC (Silicon Carbide) switch
- **Fault Cutoff**: < 3 microseconds
- **Purpose**: Arc-flash prevention, minimizes downtime

---

## 2. 800V DC DISTRIBUTION

### 2A. HVDC Air-Cooled Busbar
- **Rating**: 800VDC / 1000A
- **Type**: Overhead distribution

### 2B. Core-Shell Liquid-Cooled Busbar
- **Rating**: 50VDC / 8000A
- **Type**: Board-level distribution to compute nodes

### 2C. Busway Systems
- **BR Series**: 250-2000A, epoxy cast resin, modular
- **BL Series**: 400-6400A, vacuum cast epoxy
- **Standards**: IEC, CNS, GB compliant
- **Features**: Waterproof, dustproof, fireproof, shock-proof, corrosion-proof
- **Design**: Modular -- easy disassembly, reconstruction, expansion

---

## 3. SOLID-STATE TRANSFORMER (SST)

- **Function**: Medium-voltage AC (10-33 kV grid) direct to 800 VDC -- single-stage conversion
- **Efficiency**: Up to 98.5%
- **Technology**: SiC power modules, high-frequency transformers (tens to hundreds of kHz)
- **Architecture**: Modular cabinet design -- scalable and customizable
- **Features**:
  - Bidirectional AC/DC power conversion
  - Harmonics control and voltage regulation under varying loads
  - Rapid response to grid condition changes
  - Reduced core losses through high-frequency operation
- **Advantage**: Eliminates traditional transformer + rectifier chain
- **Status**: Prototype / early production. Co-development with NVIDIA.
- **Datasheet PDF**: https://filecenter.deltaww.com/Products/download/21/2117/Products-202410081337215817.pdf
- **Product page**: https://landing.deltaww.com/en-US/products/solid-state-transformer/ALL/

---

## 4. LIQUID COOLING PRODUCTS

### 4A. 3 MW Liquid-to-Liquid CDU
- **Cooling Capacity**: Up to 3,000 kW
- **Hydraulic Performance**: 1.5 LPM/kW at 50 psi
- **Scalability**: Up to 8 units operating as a group (24 MW cooling)
- **Purpose**: Row-level cooling for high-density AI deployments

### 4B. 2.4 MW Liquid-to-Liquid CDU (800 VDC native)
- **Cooling Capacity**: 2,400 kW
- **Approach Temperature**: As low as 4 deg C
- **Pumps**: Self-contained 800 VDC electrical pumps with N+1 redundancy
- **Dimensions**: 1,500mm W x 1,200mm D x 2,286mm H
- **Purpose**: Engineered specifically for 800 VDC AI factory architectures
- **Status**: Shown at GTC 2026

### 4C. 1.5 MW Liquid-to-Liquid CDU (GoCool-1500)
- **Cooling Capacity**: 1,500 kW
- **Features**: Stainless steel plumbing, coolant filtration, precise flow/pressure/temp control
- **Product page**: https://www.deltapowersolutions.com/en/mcis/liquid-to-liquid-coolant-distribution-unit-1500kw.php

### 4D. 140 kW In-Rack CDU (4RU) -- for NVIDIA GB300 NVL72
- **Form Factor**: 4RU
- **Cooling Capacity**: 140 kW
- **Type**: Plate-type heat exchanger (secondary server loop to primary facility water)
- **Certification**: NVIDIA GB200 NVL72 certified, GB300 NVL72 compatible
- **Status**: CERTIFIED and SHIPPING

### 4E. 200 kW In-Rack CDU (6RU)
- **Form Factor**: 6RU
- **Cooling Capacity**: 200 kW
- **Type**: Liquid-to-Liquid

### 4F. 24 kW In-Rack CDU (20RU)
- **Form Factor**: 20RU
- **Cooling Capacity**: 24 kW
- **Type**: Liquid-to-Air (L2A)

### 4G. 3D Vapor Chamber (4RU)
- **Cooling Capacity**: 1,000 W per chip
- **Purpose**: Direct chip-level cooling

### 4H. Micro Channel Cold Plates
- **Technology**: Novel bonding process for reduced flow resistance
- **Purpose**: GPU/CPU direct contact cooling

---

## 5. MICROGRID & ENERGY SOLUTIONS

### 5A. Microgrid Controller
- **Function**: Total site power control -- integrates solar, battery, gensets, hydrogen fuel cells, grid
- **Response**: 100% step-load changes at millisecond scale
- **Voltage Regulation**: Tight regulation during transients
- **Modeling**: Plant-grade simulation to optimize power flows
- **Applications**: AI data centers, telecom, oil/gas, mining, military, remote sites

### 5B. Solid Oxide Fuel Cell (SOFC)
- **Technology**: Licensed from Ceres Power (UK) -- solid oxide hydrogen technology
- **Efficiency**: >60% electrochemical conversion
- **System Efficiency**: Up to 85% with heat recovery (CHP)
- **Heat Recovery**: 25% via absorption chillers or CHP
- **Fuels**: Hydrogen, natural gas, ammonia
- **Carbon**: <360g/kWh (25% reduction vs traditional), <50g/kWh with CCUS, net-zero on H2/ammonia
- **Operation**: 24/7 continuous, stable generation
- **Integration**: Compatible with Delta PCS, ESS, UPS, BBU
- **Applications**: Microgrid, AI data center, semiconductor, hospital
- **Advantage**: Reduces "time-to-power" from years to months (vs grid interconnection)
- **Status**: First production-ready units launching 2026
- **Product page**: https://www.deltaww.com/en-US/products/hydrogen-fuel-cell-solutions/solid-oxide-fuel-cell

### 5C. Energy Storage Systems

**C Series (Commercial & Industrial)**
- Power: 125 kW per cabinet
- Energy: 261 kWh per cabinet
- Cooling: Fully liquid-cooled
- Integration: PCS, battery modules, controllers in one cabinet
- Variants: C-type (pairs with DH60C hybrid PV inverter), C+-type (DC-coupled PV arrays)

**U Series (Utility-Scale)**
- Capacity: 2.5 MW / 5 MWh
- Form Factor: Two 20-foot containers
- Features: Integrated liquid cooling and fire protection
- Purpose: Rapid site construction and commissioning

### 5D. Solid-State Transformer (SST) as Microgrid Core
- Acts as DC-coupling core for entire microgrid
- 98.5% efficiency
- Streamlines AC-to-DC conversion, reducing stages and losses
- Aligns with 800V DC bus architecture for AI factories

### 5E. Solar Inverters
- Full product line at https://www.deltaww.com/en-US/products/Photovoltaic-Inverter
- DH60C hybrid PV inverter pairs with C Series ESS

---

## 6. UPS & BATTERY (800V DC NATIVE)

Delta's approach is UNIQUE: they embed battery backup directly into the 800V DC power rack rather than using a separate centralized UPS.

- **In-Rack BBU**: 80 kW per shelf x 6 = 480 kW per 660 kW rack
- **Power Capacitance Shelf**: 20 kW for 15 seconds (supercapacitor-based bridge)
- **EVA Rack**: Energy storage smooths GPU load spikes
- **No separate DC UPS needed** -- backup is distributed at the rack level
- **Traditional UPS line** also available: https://www.deltapowersolutions.com/en/mcis/ups.php

---

## 7. CONTAINERIZED DATA CENTER

- **Form Factor**: 20-foot container
- **Integrated**: Power (55 kW shelf), cooling (80 kW liquid), IT, BBU, networking
- **Networking**: 800G/1.6T switches with NVIDIA-accelerated servers
- **Monitoring**: AI-powered cloud surveillance, 24/7
- **Deployment**: Weeks vs months for traditional builds
- **Shown at**: COMPUTEX 2025

---

## 8. NVIDIA PARTNERSHIP

### What Was Shown at GTC 2026
- Booth #1221
- 800 VDC In-Row 660kW Power Racks with embedded BBU
- 2.4MW In-Row CDU (800 VDC native)
- 3MW L2L CDU
- Microgrid solution (SST + SOFC + ESS)
- NVIDIA Omniverse digital twins for building automation and smart manufacturing
- **Dedicated GTC session**: "800 VDC and Modular Data Center Solutions: Powering Next-Generation AI Infrastructure" (S82097, March 17, 2026, 5:00-5:40 PM)
- Speakers included Harry Petty (NVIDIA Sr. Technical Marketing Manager)

### Co-Development with NVIDIA
- 800 VDC power solutions enabling 1.1 MW-scale racks -- developed "in close collaboration with NVIDIA"
- 90 kW DC/DC Power Shelf designed for NVIDIA MGX architecture
- 140 kW In-Rack CDU -- NVIDIA GB200 NVL72 certified
- Omniverse digital twin integration for Delta's Thailand smart factory
- Delta is listed in NVIDIA's official 800V DC ecosystem as a "Power System Components" partner

### Position in NVIDIA Ecosystem
- **Category**: Power System Components (alongside Flex, LITEON, Megmeet, Bizlink, Lead Wealth)
- **NOT in the "Data Center Power Systems" tier** (that's ABB, Eaton, GE Vernova, Heron Power, Hitachi Energy, Mitsubishi Electric, Schneider Electric, Siemens, Vertiv)
- **Key distinction**: Delta supplies power MODULES and COMPONENTS that go INTO the racks. The "Data Center Power Systems" companies build the facility-level infrastructure.
- Co-authored China's first Data Center 800V DC Power Technology White Paper with Alibaba ("Panama" project)

### Videos & Content
- OCP Summit video: "Delta 800 VDC Power and Cooling Solutions for Data Centers" (speakers: Ralf Pieper, ChihChung Chen from Delta, Harry Petty from NVIDIA)
- LinkedIn collaboration post: https://www.linkedin.com/posts/delta-electronics-americas_introducing-next-gen-800-vdc-data-centers-activity-7383538918425546753-DrBH

---

## 9. COMPETITIVE COMPARISON: DELTA vs EATON vs SCHNEIDER vs VERTIV

### Delta Electronics
- **Strength**: Deepest 800V DC product stack -- rack power, SST, CDU, busway, e-fuse, BBU all in-house
- **Unique**: Only vendor with embedded 480 kW BBU in the power rack (no separate UPS)
- **Unique**: SST + SOFC + ESS microgrid -- complete behind-the-meter power plant
- **Unique**: 800 VDC-native CDU pumps (2.4 MW unit)
- **Weakness**: Classified as "component supplier" not "system integrator" in NVIDIA ecosystem
- **Weakness**: Less brand recognition in US enterprise data center market
- **Availability**: Products shipping NOW

### Eaton
- **Strength**: US-made (Fibrebond Minden LA for enclosures, Boyd Thermal for cooling)
- **Strength**: Medium-voltage SST under development -- will be heart of DC distribution
- **Strength**: Deep NVIDIA partnership -- grid-to-chip power management, reference architectures
- **Strength**: Strong brand recognition, established US channel
- **Weakness**: 800V DC products still maturing vs Delta's shipping lineup
- **Key contact**: JP Buzzell (met at CERAWeek)

### Schneider Electric
- **Strength**: EcoStruxure platform -- largest data center power market share
- **Strength**: EcoStruxure Pod Data Centre -- prefabricated, integrated liquid cooling
- **Strength**: Modular sidecar pods rated ~1.2 MW per row
- **Weakness**: Less focused on 800V DC specifically vs Delta/Eaton
- **Position**: Market leader by installed base, but not leading the 800V DC transition

### Vertiv
- **Strength**: Complete 800V DC ecosystem under development for NVIDIA Vera Rubin Ultra Kyber
- **Strength**: Launched 800V DC MGX reference architecture
- **Weakness**: 800V DC products NOT available until H2 2026 -- lagging Delta
- **Weakness**: Focused on next-gen platforms (Rubin Ultra 2027) -- not current Blackwell
- **Key quote**: Dion Harris (NVIDIA) specifically cited Vertiv partnership for "megawatt-scale AI factories"

### Summary Matrix
| Feature | Delta | Eaton | Schneider | Vertiv |
|---------|-------|-------|-----------|--------|
| 800V DC rack power | SHIPPING | In dev | Limited | H2 2026 |
| Solid-State Transformer | 98.5% eff, shipping | In development | No | No |
| In-rack CDU (NVL72) | 140kW certified | Via Boyd Thermal | Yes | Yes |
| Row-level CDU | 1.5/2.4/3 MW | Limited | Yes | Yes |
| Embedded BBU (no UPS) | 480 kW/rack | No | No | No |
| Microgrid (SST+SOFC+ESS) | Full stack | No | No | No |
| US Manufacturing | Plano TX 1.5M sqft | Minden LA + more | Multiple US | Multiple US |
| NVIDIA ecosystem tier | Component supplier | System integrator | System integrator | System integrator |
| Market share (DC power) | Growing | ~10% | ~15% (leader) | ~10% |

---

## 10. ADC RELEVANCE

### Why Delta Matters for ADC
1. **Most complete 800V DC product line available TODAY** -- not waiting for 2027
2. **SST eliminates traditional transformer** -- medium voltage grid direct to 800V DC bus
3. **Embedded BBU eliminates separate UPS room** -- massive space/cost savings
4. **SOFC on natural gas** -- perfect for Henry Hub / ATMOS gas infrastructure
5. **Microgrid controller** handles solar + gas + battery + grid sell-back (ADC's 4-layer power hierarchy)
6. **140 kW in-rack CDU certified for NVL72** -- drop-in compatible
7. **Plano TX manufacturing** -- US-made, short supply chain
8. **Containerized solution** -- aligns with ADC 3K pod concept

### Potential ADC Configuration
- Delta SST: 13.8 kV grid AC -> 800V DC bus (98.5% efficient)
- Delta 660 kW racks: Power + 480 kW BBU per rack
- Delta 140 kW in-rack CDU: One per NVL72 rack
- Delta 2.4 MW CDU: Row-level cooling (800 VDC pumps)
- Delta microgrid controller: Orchestrates solar + ATMOS gas gensets + ESS + grid sell-back
- Delta SOFC: Natural gas to electricity at >60% efficiency, 24/7, low emissions
- Delta C Series ESS: 125 kW / 261 kWh per cabinet for peak smoothing

### Open Questions for Delta Sales
1. ORV660 exact model number and datasheet -- "ORV660" not confirmed as official name
2. SST power rating in kVA/MVA -- not published yet
3. SST input voltage options (13.8 kV for US? or only 10-33 kV range?)
4. SOFC power output per module in kW -- not published
5. Pricing on SST, CDU, and SOFC
6. Lead times for all 800V DC products
7. Can Delta do a complete Trappeys power system (SST + racks + CDU + microgrid)?
8. NCP/DSX certification status -- are Delta products on the NVIDIA reference BOM?
9. Channel partner or direct sales for ADC-scale orders?
10. Integration with Eaton distribution (can Delta power rack + Eaton facility distribution coexist?)

---

## Key URLs
- Product page (800V In-Row): https://www.deltaww.com/en-US/products/dc-power-systems/800-vdc-in-row-power
- SST product page: https://landing.deltaww.com/en-US/products/solid-state-transformer/ALL/
- SOFC product page: https://www.deltaww.com/en-US/products/hydrogen-fuel-cell-solutions/solid-oxide-fuel-cell
- Cooling products: https://www.deltaww.com/en-US/products/data-center-cooling
- GoCool-1500 CDU: https://www.deltapowersolutions.com/en/mcis/liquid-to-liquid-coolant-distribution-unit-1500kw.php
- Microgrid solutions: https://www.delta-americas.com/en-US/solutions/Microgrid-Solutions/ALL/
- Energy storage: https://www.deltaww.com/en-US/products/Energy-Storage-Systems/ALL/
- Americas site: https://www.delta-americas.com/
- GTC 2026 PR: https://www.prnewswire.com/news-releases/deltas-power-cooling-and-microgrid-solutions-showcased-at-nvidia-gtc-to-bolster-the-800-vdc-architecture-of-next-gen-ai-factories-302714372.html
- OCP 2025 PR: https://www.delta-americas.com/en-us/news/deltas-groundbreaking-800-vdc-power-solutions-showcased-at-ocp-global-summit-2025-to-enable-sustainable-ai-factories
- NVIDIA 800V ecosystem blog: https://developer.nvidia.com/blog/building-the-800-vdc-ecosystem-for-efficient-scalable-ai-factories/
- SST datasheet PDF: https://filecenter.deltaww.com/Products/download/21/2117/Products-202410081337215817.pdf
