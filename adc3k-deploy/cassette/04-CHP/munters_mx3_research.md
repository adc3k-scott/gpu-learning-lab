# Munters MX3 & MX3 PLUS — Research Dossier

**Compiled:** April 21, 2026
**Subject:** Munters MX3 Series (MX3 standalone dehumidifier + MX3 PLUS air treatment system)
**Launch announcement:** March 3, 2026

---

## 1. Executive Summary

Munters Group AB (Nasdaq Stockholm-listed, headquartered in Kista, Sweden) announced the **MX3 Series** on March 3, 2026 as the successor to the long-running MX² / MX² Plus platform. The series is a ground-up refresh of Munters' mid-capacity industrial desiccant dehumidification line — the first major redesign of this airflow class in roughly a decade.

The series consists of two distinct SKUs built around the same technology core:

- **Munters MX3** — standalone desiccant dehumidifier, seven model sizes, 3,000–9,500 m³/h airflow range
- **Munters MX3 PLUS** — complete air treatment system built around the MX3 core with configurable pre- and/or post-treatment modules. System-level airflow range: **1,000–14,750 m³/h**

Headline claims:

- **15–20% lower energy consumption** vs. previous models
- **Up to 15% CO₂ emissions reduction**
- **Up to 15% dehumidification improvement**
- Advanced purge technology (descended from patented PowerPurge™)
- AirPro casing (inherited from DSS Pro platform)
- AirC800 controller with Modbus / BACnet / LON
- Optional AirC Connect for remote monitoring

Availability at launch was limited to "selected markets."

Spokesperson: **Camilla Engbrink**, VP R&D and Offer Management, AirTech at Munters.

---

## 2. Product Architecture

### 2.1 Two SKUs, one core

The MX3 is the desiccant dehumidifier module itself. The MX3 PLUS is the MX3 packaged inside a larger air handling system that adds configurable pre- and post-treatment modules (filtering, heating, cooling, humidification, pre-cooling coils, etc.). This mirrors the MX² / MX² Plus relationship that preceded it.

Why this matters: when Munters marketing says "MX3 PLUS airflow 1,000–14,750 m³/h" but the press release says "3,000–9,500 m³/h," both are correct. The narrow range describes the MX3 core's seven standalone models. The wider range describes what the PLUS system can handle across its full module ecosystem.

### 2.2 Target applications (explicit from Munters)

Primary applications called out by Munters marketing:

- **Pharmaceutical manufacturing** — protects active pharmaceutical ingredients (API), ensures product quality and GMP/FDA compliance, avoids unexpected downtime
- **Food processing** — controls production climate, preserves product quality, saves energy, mitigates microbial safety issues
- **Storage and preservation** — maintains year-round RH regardless of outdoor conditions; protects documents, collections, and stored materials

Broader "related industries" listed on the MX3 product page:

- Military bases
- Defense and aerospace
- Construction and infrastructure
- Museums and galleries
- Storage, archives, and museums
- Wastewater treatment
- Public buildings and offices
- Pulp, paper, and printing
- Classic cars
- Steel and cement

---

## 3. MX3 Standalone — Model Matrix

All seven standalone MX3 models, pulled directly from the Munters product page:

| Model | Width (mm) | Length (mm) | Height (mm) | Weight (kg) |
|-------|-----------:|------------:|------------:|------------:|
| MX3 30 | 1,896 | 810 | 1,872 | 407 |
| MX3 35 | 1,903 | 1,091 | 1,909 | 472 |
| MX3 40 | 1,903 | 1,091 | 1,909 | 537 |
| MX3 55 | 1,903 | 1,091 | 1,909 | 479 |
| MX3 60 | 2,240 | 1,307 | 2,214 | 704 |
| MX3 80 | 2,240 | 1,307 | 2,214 | 712 |
| MX3 95 | 2,240 | 1,307 | 2,214 | 656 |

### Chassis observations

Three distinct physical frame sizes carry the seven models:

- **Compact frame** — MX3 30 only (1,896 × 810 × 1,872 mm)
- **Mid-size frame** — MX3 35, 40, 55 (1,903 × 1,091 × 1,909 mm)
- **Large frame** — MX3 60, 80, 95 (2,240 × 1,307 × 2,214 mm)

Model numbers roughly track airflow/capacity, not physical size. The MX3 55 is lighter than the MX3 40 despite identical dimensions — likely reflects different rotor/motor/purge configurations rather than cabinet variants.

### Product sheet PDF references (Munters Digizuite paths)

- `32829-en-mx3-30-ps-en-202602.pdf` — MX3 30
- `32830-en-mx3-35-to-95-ps-en-202602.pdf` — MX3 35 through 95 (combined sheet)
- `32831-en-mx3-plus-ps-en-202602.pdf` — MX3 PLUS

These PDFs are hosted on `www.munters.com/globalassets/digizuite/` and contain the detailed moisture-removal performance curves, dew point data, and power draw figures that are not exposed on the product web pages.

---

## 4. MX3 PLUS — System Product

### 4.1 Published specification

- **Rated airflow range:** 1,000–14,750 m³/h
- **Configuration:** Pre-configured modular components built around MX3 dehumidifier core
- **Casing:** AirPro (tested for strength, insulation, leakage reduction)
- **Compliance:** Meets European CE and UKCA requirements
- **Install readiness:** Modular design and pre-wired controls for rapid setup and commissioning

### 4.2 Module options

Pre- and/or post-treatment options that can be integrated into an MX3 PLUS system:

- Air filtration (filter module)
- Heating
- Cooling
- Humidification
- Pre-cooling coil module
- System bypass
- Process fans
- Panel mount

### 4.3 Configuration spectrum

Per Munters marketing, configurations span:

- Compact standalone (MX3 30) for small applications
- Highly configurable MX3 PLUS with full pre/post-treatment for demanding industrial processes
- Heating options: electric, steam, or gas
- Pre- and/or post-treatment arrangement to match specific application

---

## 5. Technology Stack

### 5.1 AirPro casing

The AirPro enclosure is a Munters-wide platform technology, not MX3-specific. It was originally introduced on the **DSS Pro** (Munters' larger 3,000–140,000 m³/h system). Key characteristics:

- Improved durability vs. previous casings
- Reduced air leakage
- Lower energy consumption (leakage reduction is a meaningful contributor to the 15–20% energy savings claim)
- Suitable for indoor or outdoor installation
- CE and UKCA compliant
- Modular and corrosion-resistant

### 5.2 Purge technology — EEP and ERP

Munters' press release referenced "advanced purge technology" without naming the options. The MX3 product page lists two:

- **EEP — Energy Efficiency Purge**
- **ERP — Energy Recovery Purge**

Both descend from Munters' patented **PowerPurge™** technology, originally launched on the ICA line and granted a US patent in 2006. The underlying mechanism:

> Extra purge sectors flank the reactivation sector of the rotor. A closed-loop air stream cools the rotor material before it enters the process airstream, then pre-heats rotor material before it enters the reactivation sector. This recovers waste heat from the hottest part of the rotor and uses it to reduce the energy demand for reactivation.

PowerPurge historically claims up to 30% energy reduction on larger systems. The 15–20% figure on MX3 is consistent with a scaled-down refinement for this airflow class. A related variant, **Green PowerPurge™**, is deployed on the DSS Pro for the same effect.

### 5.3 Desiccant rotor

The core IP of every Munters dehumidifier. Key attributes:

- Honeycomb matrix manufactured from corrugated composite material
- Proprietary desiccant formulation (multiple rotor types available — DSS Pro has three, MX family typically offers application-specific optimizations)
- Manufactured in-house by Munters
- Independently tested by the Swedish Institute for Food and Biotechnology and found to have both **bactericidal and fungicidal properties** — meaningful for pharma and food applications
- Capable of dew points down to -60°C / -76°F on appropriate systems
- Rotor sectioning and rotation speed optimized per application

### 5.4 Fans

EC (electronically commutated) fan technology, explicitly called out as reducing noise compared to previous MX² generation.

### 5.5 Regeneration options

Three standard heating options for reactivation:

- Electric
- Gas
- Steam

Selection depends on site utilities, fuel cost, and emissions profile.

---

## 6. Controls and Connectivity

### 6.1 AirC800 controller

Standard on MX3 systems. Provides:

- Modulating humidity control
- Communication protocols: **Modbus, BACnet, LON**
- Building Management System (BMS) integration
- Full control of pre- and post-treatment functionalities (heating, cooling, humidification, filtration)

### 6.2 AirC Connect

Optional cloud-based remote monitoring and control layer. Enables off-site operators to view performance, receive alerts, and adjust setpoints.

### 6.3 AirC Wireless

Munters' mesh control system (32 nodes per network, up to 2 wired sensors per terminal, Modbus IP communication) — compatible with MX3 for distributed sensor deployments.

### 6.4 Climatix

Standalone MX3 offers Climatix as a control option. This is Munters' BAS-style integrated platform and is standard on larger Munters systems (used as the upgrade path for retrofitting older MX² units).

---

## 7. Full Options List

### MX3 standalone options

- Configurable pre- and post-treatment
- Connectivity (AirC Connect)
- Dewpoint sensor
- Coating: Munters Protect or stainless steel
- Energy Efficiency Purge (EEP)
- Energy Recovery Purge (ERP)
- Filters: M5, G4, or G4/F7 combination
- Process fans
- System bypass
- System controls
- Climatix control platform
- Regeneration: gas, electric, or steam

### MX3 PLUS system options (additional to the above)

- Pre-Cooling Coil Module
- Panel Mount
- All pre-/post-treatment modules (filter, heat, cool, humidify)

---

## 8. Energy and Emissions Claims

Headline numbers from the press release and campaign page:

| Claim | Value | Baseline |
|-------|-------|----------|
| Energy consumption reduction | 15–20% | vs. previous MX² models |
| Dehumidification improvement | Up to 15% | vs. previous MX² models |
| CO₂ emissions reduction | Up to 15% | vs. previous MX² models |

Energy savings come from a combination of:

1. Refined purge technology (EEP / ERP)
2. AirPro casing reducing air leakage
3. EC fan technology
4. Next-generation rotor

---

## 9. Predecessor Context — MX² / MX² Plus

The MX³ series replaces the **MX²** standalone and the **MX² Plus** dehumidification system. Munters has confirmed the MX² is being discontinued ("a few units remain, it will soon be discontinued") and their product pages now explicitly steer customers to MX3.

The MX² platform has served Munters customers since at least 2015 (based on MX² Plus operating manual publication date `TEN-MX2P-B1505`), which means MX3 is the first full platform refresh in approximately 11 years.

The older MX² Plus operating manual remains publicly available at:
`https://www.munters.com/globalassets/inriver/manual/mx2p-operatingmanual2.pdf`

---

## 10. Munters Group — Company Snapshot

| Attribute | Value |
|-----------|-------|
| Parent | Munters Group AB |
| HQ | Borgarfjordsgatan 16, 164 40 Kista, Sweden |
| Listing | Nasdaq Stockholm |
| Founded | 1955 |
| Employees | ~5,000 |
| Countries of operation | 25+ |
| 2025 annual net sales | ~SEK 15 billion |
| Core domain | Energy-efficient air treatment and climate solutions |

---

## 11. Press Contact

**Daniel Frykholm**, VP External Relations & Internal Communications
- Email: `daniel.frykholm@munters.com`
- Phone: +46 (0)70 206 7786

---

## 12. Key URLs

| Resource | URL |
|----------|-----|
| US press release | `https://www.munters.com/en-us/news-media/press-releases/2026/munters-launches-new-mx3-dehumidifier-series/` |
| Campaign page | `https://www.munters.com/en-gb/campaign-pages/mx3-series-engineered-for-climate-excellence/` |
| MX3 product page | `https://www.munters.com/en-gb/products-cms/dehumidifiers/mx3/` |
| MX3 PLUS product page | `https://www.munters.com/en-gb/products-cms/dehumidifiers/mx3-plus/` |
| MX3 PLUS product sheet PDF | `https://www.munters.com/globalassets/digizuite/32831-en-mx3-plus-ps-en-202602.pdf` |
| MX3 30 product sheet PDF | `https://www.munters.com/globalassets/digizuite/32829-en-mx3-30-ps-en-202602.pdf` |
| MX3 35–95 product sheet PDF | `https://www.munters.com/globalassets/digizuite/32830-en-mx3-35-to-95-ps-en-202602.pdf` |
| MX2 Plus legacy manual | `https://www.munters.com/globalassets/inriver/manual/mx2p-operatingmanual2.pdf` |

---

## 13. US-Based Competitors (Similar Systems)

For context on the domestic alternatives to the MX3/MX3 PLUS class:

### Direct competitors — rotor desiccant, same product category

| Company | HQ | Closest MX3 PLUS analogue | Notes |
|---------|----|--------------------------|-------|
| **Bry-Air, Inc.** | Sunbury, OH | EcoDry® Series (13 sizes) | Founded 1964; acquired desiccant line from Bryant. Also offers VFB™ (300–30,000 CFM, dew points to -80°F), MiniPAC®, Desiccant Cassettes. Strong lithium battery dry-room vertical since 2019. Lists IT/Data Centres as industry. Privately owned. |
| **Climate by Design International (CDI)** | Owatonna, MN | CDH Series | Founded 1991 (as Concepts & Designs). **Acquired by Modine (NYSE: MOD) July 2025.** 1,500–38,000 SCFM. Patented NoThruMetal® (NTM) double-wall casing. Explicitly markets as "Munters DDS replacement." 203,760 sq ft HQ. |
| **NovelAire Technologies** | Baton Rouge, LA | PrecisionDry | Part of Madison Industries. 25+ years. Wheel-first OEM (supplies desiccant wheels to many NA HVAC manufacturers). ISS heritage. Lists **data centers** as explicit application. DES/DX hybrid claimed ~40% operating cost savings. |
| **Innovative Air Technologies (IAT)** | Georgia | Rotor Series | Since 2001. Custom/one-off engineered focus. XP variants for hazardous/offshore. Aerospace dew point work. |

### Adjacent technology — liquid desiccant, competes for same applications

| Company | HQ | Technology | Notes |
|---------|----|-----------|-------|
| **Alfa Laval Kathabar** | US operations (formerly Niagara Blower / Kathabar NJ) | Liquid desiccant (Kathene / LiCl solution) | 75 years US heritage, now under Alfa Laval. 1,500–20,000 CFM. ±1% RH control. Microbiological decontamination is a differentiator. Targets pharma, confectionery, brewing, cold storage, meat processing. |

### Adjacent / partial overlap

- **Desert Aire** (Germantown, WI) — primarily refrigerant-based; industrial desiccant is a minor line. Focus: natatoriums, CEA/cannabis, ice rinks.
- **Aggreko** — rental fleet, not purchased-product competitor. 2,000–15,000 CFM per unit, scalable to 1.3M CFM project-wide.

---

## 14. Gaps — What Public Sources Do Not Reveal

The following are not disclosed on Munters' public product pages or the press release and would require vendor engagement (local Munters AirTech sales or Daniel Frykholm) to obtain:

1. **Moisture removal capacity per model** (kg/h) at specific reference conditions — published in the individual PDF product sheets but not on web pages
2. **Reactivation power draw by fuel type** (electric kW, gas BTU/h, steam lb/h)
3. **Process and reactivation air temperatures** — inlet and outlet limits
4. **Dew point capability per model** — Munters systems generally reach -60°C / -76°F but the MX3-specific floor is not public
5. **Pricing** — not published anywhere public
6. **Lead times** at launch (selected markets only)
7. **Whether the 1,000 m³/h bottom end on MX3 PLUS** is a unique small-system SKU or achieved by throttling the MX3 30
8. **AirC800 controller details** — processor, I/O count, HMI size
9. **Sound power/pressure levels** by model (only "reduced noise" is claimed)
10. **Filter pressure drop curves** for the M5, G4, G4/F7 options
11. **Integration notes for third-party BMS platforms** beyond protocol-level compatibility

---

## 15. Source Inventory

Information in this dossier is consolidated from the following publicly available sources (all accessed April 2026):

### Primary Munters sources

- Munters US press release (Mar 3, 2026) — `munters.com/en-us/news-media/press-releases/2026/`
- MX3 Campaign page (UK) — `munters.com/en-gb/campaign-pages/mx3-series-engineered-for-climate-excellence/`
- MX3 product page (UK) — `munters.com/en-gb/products-cms/dehumidifiers/mx3/`
- MX3 PLUS product page (UK) — `munters.com/en-gb/products-cms/dehumidifiers/mx3-plus/`
- Munters dehumidification landing page — `munters.com/en/solutions/dehumidification/`
- Munters PowerPurge campaign page — `munters.com/en/campaigns/airt-campaigns/powerpurge/`
- Munters rotor energy recovery page — `munters.com/en-us/munters-life-cycle-phases/retrofit--upgrade/purge-energy-recovery/`
- MX² Plus operating manual (2015) — `munters.com/globalassets/inriver/manual/mx2p-operatingmanual2.pdf`

### Third-party coverage

- Cooling Post (Mar 3, 2026) — industry trade coverage
- ACR News (Mar 5, 2026) — industry trade coverage
- SMAC Enterprises / Air Treatment South Africa (Mar 4, 2026) — Munters distributor republishing press release

### Historical / technology context

- DirectIndustry catalog entries for MX2700, MXT5000, MCD100, DSS Pro
- Munters Control Conversion / Retrofit pages
- AirC Wireless user manual (2022)
- Thomasnet archive: PowerPurge US patent announcement (2006)

---

## 16. Quick Reference — Is MX3 Right for an Application?

Use this table as a first-pass fit check:

| Need | MX3 fit |
|------|---------|
| Airflow 1,000–14,750 m³/h with pre/post treatment | **Yes** (MX3 PLUS) |
| Airflow 3,000–9,500 m³/h, dehumidification only | **Yes** (MX3 standalone) |
| Airflow < 1,000 m³/h | No — consider Munters M series, ML, ComDry NX |
| Airflow > 14,750 m³/h | No — consider Munters DSS Pro (up to 140,000 m³/h) |
| Need BMS integration (Modbus / BACnet / LON) | Yes — AirC800 standard |
| Remote monitoring required | Yes — AirC Connect optional |
| Pharmaceutical GMP / FDA compliance | Yes — explicit target application |
| Food processing, hygienic environment | Yes — rotor has bactericidal/fungicidal properties |
| Lithium battery dry room | Consider — Bry-Air and CDI have stronger positioning here |
| Data center humidity control | Possible but not explicitly marketed — NovelAire or Munters DSS Pro may be better-matched |
| Ultra-low dew point (< -60°C) | Verify per model — Munters rotors generally capable, but MX3 dew point floor not publicly stated |
| Outdoor installation | Yes — AirPro casing supports indoor or outdoor |
| Budget-constrained | Consider US alternatives (Bry-Air, CDI) for potentially lower capex and shorter US lead times |

---

*End of dossier.*
