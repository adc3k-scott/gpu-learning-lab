# ST-TRAP-BESS-RFQ-001 — BESS Vendor RFQ Package — Rev 0.1

**Document:** Battery Energy Storage System — Vendor Request for Quotation
**Project:** Trappey's AI Center, Lafayette, Louisiana
**Revision:** 0.1 — first issue
**Date:** April 18, 2026
**Owner:** Scott Tomsu | scott@adc3k.com | (337) 780-1535
**Status:** Working draft — ready for vendor distribution
**Authority:** ST-TRAP-BESS-001 Rev 0.1 and BOD-001 Rev 0.4 govern all technical requirements. This document is the procurement instrument derived from that basis.

---

## 1. Project overview

**Trappey's AI Center** is a 101.2 MW IT load AI compute facility on a 22-acre historic cannery site in Lafayette, Louisiana. The facility operates as a **behind-the-meter permanent island** — no utility grid connection on day one. Power is generated on-site by 44 × Cat CG260-16 natural gas gensets (4,000 ekW each) arranged in 11 electrically independent blocks.

The electrical architecture is OCP Stage 1d compliant: 480 VAC from genset step-down transformer → in-row DC power racks → **800 VDC common busway** per block. There is no AC anywhere downstream of the in-row racks. Every load is DC. The BESS must be DC-coupled to this bus.

**Stage 1:** 11 blocks, 44 cassettes, 31,680 NVIDIA GPUs, 101.2 MW IT.
**Full Build:** 22 blocks, 88 cassettes, 202.4 MW IT (option pricing requested — see §8).

This RFQ covers the **block-level BESS** for Stage 1. The BESS is an always-active system stabilizer and contingency reserve — it is not backup power that sits idle.

---

## 2. BESS system requirements

### 2.1 Per-block requirements

| Parameter | Value | Notes |
|---|---|---|
| Energy capacity per block | 3.6 MWh working; quote 3.0, 4.0, and 5.0 MWh options | See §2.3 for sizing basis |
| Continuous power rating | 2 MW | Bidirectional charge and discharge |
| Peak power rating | 4 MW | 10-second minimum duration |
| Operating DC bus voltage | 800 VDC | Fixed — OCP Stage 1d architecture |
| Battery pack output voltage | 1,100–1,500 VDC acceptable | Must include bidirectional DC-DC to 800 V — see §4 |
| Chemistry | LFP (LiFePO4) only | NMC, NCA, NiMH excluded |
| Minimum cycle life | 3,000 cycles at 80% DOD | Daily dispatch cycling required |
| Operating temperature range | −20°C to +50°C ambient | Outdoor pad, Lafayette, Louisiana (summer peak 35°C dry-bulb) |
| BESS operating mode | Island / off-grid | Behind-the-meter permanent island — no utility grid. Vendor must confirm island-mode operation. |
| Depth of discharge (operating) | 10–100% SOC | 10% SOC floor is a hard limit enforced by BMS. See §7. |
| Aux power | ≤80 kW per container | Fed from dedicated 480 VAC feeder — HVAC, BMS compute, fire suppression controls |

### 2.2 Facility-level quantities

| Parameter | Value |
|---|---|
| Stage 1 blocks | 11 |
| Stage 1 BESS containers | 11 (1 per block, or 2 if split architecture — quote both) |
| Stage 1 total energy | ~39.6 MWh (11 × 3.6 MWh working) |
| Full Build blocks | 22 |
| Full Build total energy | ~79.2 MWh (option pricing — see §8) |

### 2.3 Sizing basis and contingency scenarios

The 3.6 MWh per-block working figure is bounded by three contingency scenarios. Vendor response should confirm which configurations cover each scenario and at what power and duration.

| Scenario | Trigger | Required energy per block | Required duration |
|---|---|---|---|
| Single genset trip | One of four CG260-16 gensets trips; remaining three ramp to carry load | ~1–2 MWh | Seconds to minutes — until governor settle |
| Partial gas curtailment | Gas supply pressure drop; block derate ordered by AI dispatch | ~2–3 MWh | Minutes — graceful IT load ramp-down |
| Full gas loss — graceful shutdown | Total gas supply interruption to block | ~3–4 MWh | 15–20 minutes — GPU checkpoint + cassette cooldown |

The full gas-loss scenario is the design anchor. 15–20 minutes is sufficient for GPU checkpointing and orderly shutdown. BESS is not sized for extended hold — gas supply continuity is the primary reliability path.

---

## 3. Scope of supply

Vendors are requested to quote the following. Indicate clearly in the response which items are included, which are separately priced, and which are not supplied.

| Item | Required | Notes |
|---|---|---|
| LFP battery enclosure(s) per block | Yes | With integrated BMS, thermal management, fire detection, contactor |
| Bidirectional DC-DC converter | Yes | SiC-based; input 1,100–1,500 VDC; output 800 VDC regulated. May be integrated with BESS enclosure or supplied as separate skid. See §4. |
| SSCB (solid-state circuit breaker) at 800 VDC bus tie | Yes | Sub-millisecond trip. May be supplied by vendor or specified as a third-party item |
| Container thermal management (HVAC) | Yes | Size for outdoor Louisiana ambient; aux power ≤80 kW per container |
| Integrated fire suppression | Quote option | Dry pipe + detection system within container |
| NFPA 855 compliance documentation | Yes | Required for AHJ submittal — see §5 |
| Remote monitoring and BMS interface | Yes | Modbus TCP or CANBUS to customer L1 block PLC. See §7. |
| Factory acceptance test (FAT) | Yes | Include in base quote |
| Site acceptance test (SAT) support | Yes | Include in base quote |
| Commissioning support | Yes | On-site; include in base quote |
| Training | Yes | Operator + maintenance. Include in base quote. |
| Spare parts package (3-year) | Quote option | Common failure parts; pricing separate |
| O&M service agreement | Quote option | Annual; pricing separate |

---

## 4. Bidirectional DC-DC converter requirements

The BESS battery pack does not output natively at 800 VDC. The bidirectional DC-DC converter is the interface between the battery pack and the 800 VDC bus. It is **the most critical single component** in the BESS system for this application.

**The vendor must supply or specify the DC-DC converter as part of this scope.** It may be integrated with the BESS enclosure or supplied as a standalone skid. Quote both options if available.

| Parameter | Requirement |
|---|---|
| Switching technology | SiC (silicon carbide) — required for microsecond-to-millisecond response |
| Input voltage range | 1,100–1,500 VDC (full BESS pack SOC range from 0–100%) |
| Output voltage | 800 VDC ±1% steady-state |
| Continuous power | 2 MW bidirectional (charge and discharge) |
| Peak power | 4 MW for ≥10 seconds |
| Efficiency | ≥97% at rated continuous power |
| Galvanic isolation | Required — battery pack negative and 800 VDC bus negative must be isolated |
| Response time | Sub-millisecond to power setpoint command |
| Derating curve | Vendor must provide power vs SOC curve across full 0–100% SOC range. Derating at low SOC is a disqualifying condition if power falls below 2 MW continuous at any SOC above the 10% floor. |
| Communications | Modbus TCP for dispatch setpoints; IEC 61850 GOOSE for fast protection signals to L1 block PLC |
| Protection | Internal overcurrent, overvoltage, thermal. Coordinates with BESS BMS contactor and bus-side SSCB. |

**Hitachi Energy AMPS note:** If the vendor's battery pack has been tested or validated with Hitachi Energy AMPS (Advanced Multiport Power Station), confirm this in the RFQ response and provide the pairing reference. Hitachi AMPS is under evaluation as the DC-DC layer if vendor-integrated options are not available.

---

## 5. Compliance and certification requirements

| Requirement | Standard | Notes |
|---|---|---|
| Cell/module-level listing | UL 9540A | Required. Provide test report with response. |
| System-level listing | UL 9540 | Required. Provide certificate with response. |
| Outdoor container fire safety | NFPA 855 (2026 edition) | Required. Compliance documentation required for Lafayette Parish AHJ submittal. |
| Additional fire safety | FM Global FM 5-33 | Preferred — FM Global preferred insurer for this facility. Confirm FM 5-33 compliance or equivalent status. |
| Hazardous gas detection | NFPA 69 | Required if applicable to product design. |
| Electrical safety | UL 508A (control panels) | Required for control panels and DC-DC skid. |
| Seismic | IEEE 693 or IBC Seismic Design Category C | Lafayette, Louisiana — confirm applicable seismic category per ASCE 7-22. |
| Thermal runaway notification | NFPA 855 §12 | Automated thermal runaway detection and notification integrated with BMS. Required. |
| Louisiana environmental | LDEQ — no hazardous waste streams from normal operation | Confirm no regulated discharge from normal BESS operation. |

---

## 6. Physical and mechanical requirements

| Parameter | Requirement | Notes |
|---|---|---|
| Container footprint | 20-ft standard ISO preferred | LG ES Vertech JF2 DC LINK 23-ft width flagged — confirm pad logistics before selection |
| Container type | Outdoor-rated; NEMA 3R minimum | Installed on concrete rear slab, Lafayette, Louisiana |
| Weight (loaded) | Provide gross weight | Rear slab structural loading to be confirmed |
| Connections panel | Single service-side access panel minimum | DC power output, aux AC power input, communications, fire suppression water |
| DC cable interface | Vendor to specify cable type, lug size, and bend radius at DC-DC output | Run to customer-supplied 800 VDC SSCB panel — ~10–30 ft run |
| Aux AC input | 480 VAC, 3-phase, customer-supplied feeder | Vendor to specify ampere draw |
| Cooling | Self-contained within container; no customer-supplied CHW | Outdoor air-cooled |
| Access | Minimum two-side access for maintenance | Confirm door locations and swing clearances |

---

## 7. Communications and controls interface

The BESS is integrated into the AMCL (AI Mission Control Layer) five-tier control architecture. The vendor must support the following interface points. Confirm each in the RFQ response.

| Interface | Protocol | Direction | Purpose |
|---|---|---|---|
| BMS → L1 block PLC | Modbus TCP or CANBUS (confirm) | Battery to customer | SOC, cell voltages, temperatures, fault codes, state of health |
| DC-DC converter → L1 block PLC | IEC 61850 GOOSE | DC-DC to customer | Fast protection signals — trip, fault, mode state |
| DC-DC converter → L1 block PLC | Modbus TCP | Bidirectional | Dispatch setpoints (charge/discharge power command), mode selection, status |
| BMS → L2 SCADA | OPC-UA (via L1 aggregation) | Via L1 | Historian data — ~50 points per block minimum |
| Remote monitoring | Vendor web portal or API (optional) | Vendor to customer | Parallel to customer SCADA — for vendor warranty monitoring |

**Critical control interface requirement:** The L1 block PLC enforces the 10% SOC floor hard limit and all temperature/voltage safety interlocks. The DC-DC converter **must accept and execute L1 dispatch commands** (power setpoints, mode changes) within the BMS safety envelope. The vendor BMS contactor may override L1 on a cell-level safety trip — this is expected and required. Document the priority hierarchy clearly in the response.

---

## 8. Quantities and schedule

### 8.1 Stage 1 — base quote

| Item | Quantity |
|---|---|
| BESS containers (LFP, 3.0 MWh option) | 11 |
| BESS containers (LFP, 3.6 MWh / 4.0 MWh option) | 11 |
| BESS containers (LFP, 5.0 MWh option) | 11 |
| Bidirectional DC-DC converter skids (if separate from container) | 11 |
| Commissioning support (days on-site per container) | Vendor to propose |

Quote each energy tier as a separate line. Provide pricing per container and total.

### 8.2 Full Build option — price as an option, not a commitment

| Item | Quantity (option) |
|---|---|
| Additional BESS containers for Full Build (Stage 2, same spec) | 11 |
| Total Full Build BESS containers | 22 |

Full Build option pricing will be used for budget purposes. No commitment implied.

### 8.3 Multi-site portfolio context

ADC operates multiple AI factory sites in Louisiana at similar scale. The following table is provided for vendor context in pricing the per-unit cost. No commitment is made to any site beyond Trappeys Stage 1 at this time.

| Site | Approximate BESS scope |
|---|---|
| Trappeys AI Center (this RFQ) | 11 containers Stage 1; 22 Full Build |
| MARLIE I, Lafayette LA | 5 blocks, similar spec |
| Willow Glen, St. Gabriel LA | Up to 50+ blocks at Full Build |
| New Iberia AI Factory | Up to 40+ blocks at Full Build |
| **Portfolio estimate** | **~100+ containers across active sites** |

Vendors accustomed to 100 MWh+ engagements are encouraged to price accordingly.

### 8.4 Target schedule

| Milestone | Target |
|---|---|
| RFQ response deadline | [TBD — 4 weeks from issue] |
| Vendor clarification calls | [TBD — 2 weeks from issue] |
| Vendor selection | [TBD — 6 weeks from issue] |
| Contract execution | [TBD] |
| Lead time to first delivery (Block 1) | Vendor to state |
| Full Stage 1 delivery complete | Vendor to state |

---

## 9. Submittal requirements

Vendor RFQ response must include the following. Responses missing required items will be scored accordingly.

**Required:**

1. Technical compliance matrix — confirm or take exception to each requirement in §2 through §7. Use the section numbers.
2. Product data sheets — battery enclosure, bidirectional DC-DC converter (or BESS-integrated equivalent).
3. UL 9540A test report(s).
4. UL 9540 certificate(s).
5. NFPA 855 (2026) compliance documentation or compliance roadmap with expected date.
6. FM Global FM 5-33 status (compliant, in process, or not applicable — explain).
7. Island / off-grid operation confirmation letter or datasheet callout. Statement must be explicit — not implied.
8. Power vs SOC derating curve for the bidirectional DC-DC converter (continuous and peak power across 0–100% SOC).
9. Communications interface document — register map for Modbus TCP, IEC 61850 data model for GOOSE signals.
10. Container dimensional drawing (footprint, height, service clearances, door locations, weight).
11. Pricing per §8.1 (Stage 1 base quote, three energy tiers) and §8.2 (Full Build option).
12. Lead time — time from purchase order to first delivery, and full Stage 1 delivery schedule.
13. References — minimum two AI factory or data center BESS deployments in island / behind-the-meter configuration.

**Optional (evaluated positively):**

- Hitachi AMPS compatibility documentation
- FM Global FM 5-33 test report
- ITC domestic content eligibility analysis
- NFPA 855 AHJ letter from a comparable US jurisdiction
- Manufacturer plant location(s) and US domestic content percentage

---

## 10. Evaluation criteria

Responses will be scored on the following criteria. Weights are internal guidance — not published to vendors.

| Criterion | Weight | Key factors |
|---|---|---|
| Island / off-grid confirmation | 25% | Explicit written confirmation that the system operates without grid connection. Demonstrated deployments preferred. |
| Technical compliance | 20% | Compliance matrix completeness; no exceptions to SiC DC-DC, LFP chemistry, 800 VDC bus, power derating |
| UL 9540A + NFPA 855 documentation | 15% | Completeness and currency of compliance documentation. Ready for AHJ submittal now. |
| DC-DC converter quality | 15% | SiC confirmed, efficiency ≥97%, derating curve provided, IEC 61850 GOOSE supported |
| Delivery schedule | 10% | Lead time to first block; ability to deliver all 11 containers on Stage 1 schedule |
| Price (Stage 1 + Full Build option) | 10% | All-in per-container price including FAT, SAT support, commissioning, training |
| References | 5% | Comparable AI factory / data center island deployments |

**Disqualifying conditions (automatic exclusion):**
- Chemistry other than LFP
- No island / off-grid operation confirmation
- UL 9540A test report not available
- DC-DC converter does not achieve 2 MW continuous at any SOC above 10% SOC floor

---

## 11. Vendor engagement sequence

Engage in this order:

1. **Fluence Energy** — preferred first contact. Island-mode confirmed. Gridstack Pro 4.9–5.6 MWh per 20-ft enclosure. UL 9540A fire tests completed June 2025 (CSA Group, Safe Laboratories NC). NFPA 855 (2026) compliance documentation in preparation.
   - Contact: Fluence Energy (NASDAQ: FLNC), Arlington VA — +1 703 682 2700
   - Frame: total portfolio ~100+ containers across ADC Louisiana sites. Typical Fluence engagement threshold is 100 MWh+ — lead with portfolio, not single-site.

2. **LG Energy Solution Vertech** — strongest domestic content story (Holland MI manufacturing). JF2 DC LINK, 5.11 MWh, 1,134–1,499 VDC confirmed, UL 9540A confirmed.
   - Flag: JF2 is 23-ft wide (non-standard ISO). Confirm flatbed transport logistics and crane requirements at rear slab before selecting.
   - ITC domestic content eligibility strongest of shortlist.

3. **Saft (TotalEnergies)** — Intensium Flex, 3.4/4.3/5.1 MWh configurations, 20-ft ISO. TotalEnergies parent understands natural gas BTM — different conversation than a pure battery company.
   - US contact: Saft US, Cockeysville MD — +1 410 771 3200
   - Note: DC-version UL 9540A listing for production units started late 2025 — verify status before AHJ submittal.

4. **Hitachi Energy** — engage in parallel on AMPS DC-DC layer regardless of BESS container selection. Ask for battery partner list and validated BESS integrations. If no BESS vendor integrates a compliant DC-DC natively, Hitachi AMPS is the fallback.

---

## 12. Submission instructions

**Submit to:** Scott Tomsu, scott@adc3k.com  
**Phone:** (337) 780-1535  
**Response format:** PDF preferred. Include all required submittals as attachments or embedded.  
**Response deadline:** [TBD — insert date]  
**Clarification questions:** Submit by email no later than [TBD — 2 weeks from issue]. Responses issued in writing to all vendors.

Submissions will be treated as confidential. Do not distribute this RFQ externally without written permission from Scott Tomsu.

---

## 13. Open items and pending inputs

| Ref | Item | Impact on RFQ |
|---|---|---|
| E-10 | Per-block sizing validation — Cat CSA governor data pending | May shift 3.6 MWh working to a different point in the 3–5 MWh envelope. Vendors should quote all three tiers. |
| NFPA AHJ | Lafayette Parish AHJ NFPA 855 interpretation not yet confirmed | Vendor NFPA 855 documentation required for AHJ submittal after vendor selection. |
| PHYS | Rear slab BESS layout and NFPA 855 setback study not yet completed | Will confirm container positions and setback clearances before purchase order. |
| LG 23-ft | LG ES Vertech JF2 non-standard 23-ft width — logistics study required | Confirm crane and transport requirements with vendor during RFQ clarification call. |
| ITC | Domestic content analysis for ITC basis — per-vendor | Request documentation from each vendor. Tax counsel review after vendor selection. |

---

## 14. Revision plan

| Rev | Trigger | Change |
|---|---|---|
| **0.1 (current)** | First issue | Full RFQ package — requirements, scope, compliance, quantities, evaluation criteria, vendor sequence |
| 0.2 | Cat CSA data received | Update §2.3 contingency energy figures if sizing envelope shifts |
| 1.0 | Vendor selection | Update §11 with selected vendor; archive competing responses; move to contract package |

---

## 15. Approval

Rev 0.1 is ready for vendor distribution subject to Scott Tomsu review. No external engineering circulation approval required for RFQ phase. Vendor selection and contract execution require Scott Tomsu authorization.

---

**End of ST-TRAP-BESS-RFQ-001 Rev 0.1.**
