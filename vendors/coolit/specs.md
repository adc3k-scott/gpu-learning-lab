# CoolIT Systems — Liquid Cooling for ADC
Last updated: 2026-03-30

## Company Overview
- **HQ:** Calgary, Alberta, Canada
- **Founded:** 2001 (Brydon Gierl + 3 colleagues)
- **Ownership:** KKR + Mubadala Capital (acquired May 2023)
- **CEO:** Jason Waxman
- **Founder:** Brydon Gierl (technical/R&D)
- **Phone:** +1 403-770-5766
- **Scale:** 5M+ coldplates shipped, 300+ AI compute facilities globally, 7 of top 10 supercomputers (including #1 El Capitan), 4 of 5 hyperscalers as clients, 4 of top 5 server OEMs
- **Production:** 100+ CDUs/month, 1,000+ rack manifolds/month, 10,000+ coldplate loops/month
- **Manufacturing:** Canada, China, Vietnam

---

## Business Model: TWO TRACKS
1. **OEM/ODM component supplier** — sells coldplates + loops to Dell, HPE, Supermicro, Lenovo who install in servers
2. **Direct turnkey deployer** — designs, prefabs, installs, and maintains complete DLC systems (TCS + CDUs + manifolds). Single rack = 1-3 days. Large secondary fluid network = weeks to months. Includes site survey, CDU sizing, piping design, thermal modeling, commissioning, 2-5 year maintenance SLAs.

---

## 1. CDU Product Line

### CHx2000 — THE AI CDU (Flagship, launched Oct 2024)
Built specifically for NVIDIA NVL72-class deployments.
- **Cooling Capacity:** 2,000 kW (2 MW) at 5°C approach temperature delta
- **Enhanced mode:** 2,550 LPM primary / 2,400 LPM secondary
- **Standard mode:** 1,800 LPM primary / 1,800 LPM secondary
- **Footprint:** Single-rack — 750mm W x 1,200mm D (compact)
- **Racks supported:** Up to **12 NVIDIA GB300 NVL72 racks** per unit
- **Enterprise density:** Up to 74 high-density enterprise racks
- **Piping:** Stainless steel, 4" Victaulic couplings
- **Pump:** Single pump: 12.24 kW at 1,500 LPM; dual pump mode available; hot-swappable
- **Controls:** 10" touchscreen; Redfish, TCP/IP, Modbus, BACnet
- **Serviceability:** Hot-swappable pumps, filters, sensors
- **Group control:** Up to 20 CHx2000 units coordinated
- **Production:** Hundreds of units/month at Starfield Mfg, Calgary
- **Status:** In production, deployed globally
- **URL:** https://www.coolitsystems.com/resources/news/chx2000-the-ai-cdu/

### AHx240 — Liquid-to-Air CDU (Flagship L-A)
- Industry's most powerful liquid-to-air CDU
- High-density air-side heat rejection

### AHx180 — Liquid-to-Air CDU
- Mid-density air-side rejection

### CHx200 — In-Rack CDU
- 200 kW, liquid-to-liquid
- Single rack or small cluster
- ASHRAE W+ warm water compatible
- URL: product page on coolitsystems.com

### CHx80 — Rack-Based CDU
- 80 kW, liquid-to-liquid
- HPC/enterprise rack-level

### Full CDU lineup: https://www.coolitsystems.com/products-services/data-center-products/cooling-distribution-units/

---

## 2. Coldplates

### Split-Flow Technology
- Primary coldplate design
- Divergent/convergent microchannel flow paths
- Low thermal resistance AND low pressure drop simultaneously (these normally trade off)
- Frontier: >4,000W per chip (4 kW coldplate) for AI accelerators

### OMNI Coldplate
- All-metal construction
- Aerospace-grade assembly process
- Unibody copper, full-metal seal

**NOTE:** Specific thermal resistance, flow rate, pressure drop specs are not published — shared under NDA/NPI engagement. Compatible with GB200 (Blackwell) confirmed from rack manifold imagery.

**URL:** https://www.coolitsystems.com/coldplate-technology/

---

## 3. Coldplate Loops (Server-Level)
- **Standard loops:** Pre-validated, configurable, off-the-shelf. Components: copper coldplates + TIMs + hoses + quick disconnects
- **Custom loops:** Fully engineered for specific system designs, capable of 100% heat capture
- Connect GPU/CPU coldplate back to rack manifold
- URL: https://www.coolitsystems.com/products-services/server-products/coldplate-loops/

---

## 4. Rack Manifolds

### EIA Rack Series
- 42U, 48U, 52U; top or bottom feed; single or dual-sided

### ORV3 Rack Series
- 44U OpenRack v3 format (hyperscaler standard)

### MGX Rack Series — KEY FOR NVIDIA DEPLOYMENTS
- NVIDIA MGX standard chassis
- Critical for Blackwell GB200/GB300 NVL72 deployments
- Color-coded QDs: red (hot return) / blue (cold supply)

**All manifolds:** Corrosion-resistant stainless steel, UL certified, engineered for low pressure drop and balanced flow
**URL:** https://www.coolitsystems.com/products-services/server-products/rack-manifolds/

---

## 5. TCS — Technology Cooling System
The facility-side distribution piping between CDUs and racks — the "plumbing backbone."

### Stainless Steel TCS
- Prefabricated modular components
- **Victaulic couplings** — grooved mechanical joints, no welding on-site
- CoolIT designs, prefabricates, and installs

### Polypropylene TCS
- Prefabricated **Aquatherm** polypropylene components
- Heat fusion welding on-site
- Alternative to stainless — lower cost, corrosion-proof

**Services:** CDU sizing, piping design, thermal modeling, layout optimization, pressure testing/flushing, commissioning
**URL:** https://www.coolitsystems.com/products-services/data-center-products/technology-cooling-system/

---

## 6. NVIDIA Relationship
- **NOT on NVIDIA's public RVL/AVL directly** — but inside deployments via OEM path (OEM gets certified, CoolIT's product is inside)
- **MGX rack manifold series** = building to NVIDIA's MGX hardware spec
- **CHx2000 engineered for NVL72** — 12 racks per unit at GB300 density
- **45°C inlet water capability** aligns with Jensen Huang's Vera Rubin/GB300 spec
- **4 of 5 hyperscalers** buying NVL72 clusters are CoolIT customers
- **Action item:** Call +1 403-770-5766 and ask specifically about DSX reference design compatibility and RVL/AVL status for GB300 NVL72

---

## 7. Technology Position
CoolIT advocates single-phase direct liquid cooling (DLC) with water as most mature and widely deployed.
Positions AGAINST: immersion cooling (pressure/fluid/deployment challenges) and two-phase cooling.
**Rule of thumb published:** 1.5 LPM per kW of heat load.

---

## 8. Key Contacts
| Name | Title |
|---|---|
| Jason Waxman | CEO |
| Brydon Gierl | Founder |
| Scott Hudson | VP Quality |
- No VP Sales publicly listed — use contact form or call HQ directly
- **Contact:** https://www.coolitsystems.com/contact/
- **Phone:** +1 403-770-5766

---

## 9. ADC Stack Integration
- CoolIT = **thermal layer** (coldplates, manifolds, TCS piping, CDUs)
- Eaton = facility AC distribution to CDUs
- Delta = rack-level DC power to GPUs + in-rack 140 kW CDU
- CoolIT CDUs run on facility AC — no conflict with 800V DC compute bus
- **Recommended for ADC:** CHx2000 (2MW, 12 NVL72 racks) for Trappeys row-level cooling
- **Pairing:** CoolIT CHx2000 + Staubli quick-disconnects (existing vendor relationship confirmed)

## Key URLs
- Homepage: https://www.coolitsystems.com
- CDU lineup: https://www.coolitsystems.com/products-services/data-center-products/cooling-distribution-units/
- CHx2000: https://www.coolitsystems.com/resources/news/chx2000-the-ai-cdu/
- TCS: https://www.coolitsystems.com/products-services/data-center-products/technology-cooling-system/
- Coldplates: https://www.coolitsystems.com/coldplate-technology/
- Rack manifolds: https://www.coolitsystems.com/products-services/server-products/rack-manifolds/
- Professional services: https://www.coolitsystems.com/products-services/global-professional-services/
