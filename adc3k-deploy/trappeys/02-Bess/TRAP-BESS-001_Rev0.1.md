# ST-TRAP-BESS-001 — BESS Architecture Basis — Rev 0.1

**Document:** Battery Energy Storage System Architecture Basis
**Project:** Trappey's AI Center, Lafayette, Louisiana
**Revision:** 0.1 — first issue; companion to ELEC-001 Rev 1.2 and BOD-001 Rev 0.4
**Date:** April 17, 2026
**Owner:** Scott Tomsu
**Status:** Working draft

---

## 1. Purpose

Defines the BESS architecture for Trappey's AI Center. Establishes the role, sizing basis, chemistry selection, DC coupling topology, vendor shortlist, and AMCL integration for the block-level battery system. Serves as the engineering anchor for the BESS RFQ package.

This document does not cover: solar DC-DC buck converter (ST-TRAP-SOLAR-001), in-row rack BBU and PCS (locked in ELEC-001 §7), or protection coordination across the AC-DC boundary (ST-TRAP-PROT-001).

## 2. Relationship to other documents

**Upstream (this document inherits from):**

- BOD-001 Rev 0.4 — ledger authority; E-10 through E-13 are the source entries
- ELEC-001 Rev 1.2 — BESS sizing, power rating, coupling topology, contingency scenarios (§8)
- ARCHDIAG-001 Rev 0.1 — Diagram 4 shows BESS on 800 VDC bus; Diagram 6 shows AMCL tiers

**Downstream (inherits from this document):**

- ST-TRAP-SLD-001 — formal single-line; BESS tie to 800 VDC bus with CT/PT designations
- ST-TRAP-PROT-001 — protection coordination at DC-DC converter output; SSCB settings
- ST-TRAP-BESS-RFQ-001 — vendor procurement package (not yet drafted)

---

## 3. Role and operating principle

**The BESS is the block-level system stabilizer, not backup.**

It is always active on the 800 VDC bus. It does not sit idle waiting for a fault — it runs continuously in charge/discharge dispatch under AMCL L1 (deterministic) and L3 (AI) control, absorbing and injecting power in real time.

Four operating functions, in priority order:

1. **Transient buffer.** Sub-second response to genset governor lag during load swings. The Cat CG260-16 governor requires finite time to settle after a step load change. The BESS bidirectional DC-DC converter — SiC-based, microsecond to millisecond response — closes the gap between governor command and mechanical settle. This is the primary justification for DC-coupling: AC-coupled BESS via an inverter at the MV side does not place the buffer on the same voltage rail as the GPU load.

2. **Contingency support.** Energy reserve for single-genset trip, partial gas curtailment, and full gas-loss graceful shutdown. See §6 for scenario sizing.

3. **Solar clip-recapture.** Absorbs First Solar overproduction that would otherwise require MPPT throttling. Releases during high-load periods under L3 dispatch.

4. **Load shifting.** Flattens genset loading within the 55–75% AI dispatch envelope. BESS absorbs overnight low-load excess and discharges into morning GPU ramp.

**What BESS is not:** It is not the primary voltage-forming source on the 800 VDC bus. Bus voltage is regulated by the in-row power rack rectifiers. The bidirectional DC-DC converter tracks bus voltage and dispatches accordingly. It is not a replacement for the in-row BBU + PCS storage, which handles sub-100 ms GPU load swings (ELEC-001 E-20). The two layers are complementary and run in parallel.

---

## 4. Per-block sizing basis

**Source:** BOD-001 E-10; ELEC-001 §8.

| Parameter | Value | Status |
|---|---|---|
| Facility total (Stage 1, 11 blocks) | 40 MWh | W |
| Per-block allocation | 3.6 MWh working midpoint | W |
| Per-block envelope | 3–5 MWh | W |
| Sizing anchor | Three contingency scenarios — see §6 | W |

**Allocation math:** 40 MWh ÷ 11 blocks = 3.636 MWh/block → rounded to 3.6 MWh working. This is uniform math; actual per-block assignment may shift based on contingency analysis results (contingency analysis will refine — E-10 gated).

**Envelope logic:** 3 MWh is the floor set by the full gas-loss graceful shutdown scenario. 5 MWh provides headroom if the Cat CSA governor data shows slower-than-expected transient response, or if contingency analysis extends the graceful shutdown window beyond 20 minutes.

---

## 5. Power rating

**Source:** ELEC-001 §8.

| Parameter | Per block | Facility (11 blocks) |
|---|---|---|
| Continuous | ~2 MW | ~22 MW |
| Peak (short duration) | ~4 MW | ~44 MW |

Continuous rating covers solar clip-recapture and load shifting. Peak rating covers single-genset trip transient — the largest expected power excursion during normal operation.

**Vendor filter:** Bidirectional DC-DC converter must confirm rated continuous and peak throughput at 800 VDC bus voltage across the full operating SOC range of the BESS pack. Derating at low SOC is a common failure mode — require power vs SOC curve in RFQ response.

---

## 6. Contingency scenarios

**Source:** ELEC-001 §8. These scenarios bound the 3–5 MWh per-block envelope.

| Scenario | Trigger | Per-block energy | Duration |
|---|---|---|---|
| Single genset trip inside block | One of four CG260-16 trips; remaining 3 ramp to carry load | ~1–2 MWh | Seconds to minutes — until governor settle and UFLS coordination |
| Block partial gas curtailment | Gas supply pressure drop; block derate ordered by L3 dispatch | ~2–3 MWh | Minutes — graceful IT load ramp-down |
| Full gas loss — graceful shutdown | Total gas supply interruption to block | ~3–4 MWh | 15–20 min orderly cassette cooldown and checkpoint |

**Design anchor:** The full gas-loss scenario sets the 3 MWh floor. The 3.6 MWh working midpoint provides margin without reaching the 5 MWh ceiling. Contingency analysis (E-10) will validate these numbers against CG260-16 governor ramp rates when Cat CSA data is available.

**BESS is not sized for extended outage.** 15–20 minutes is sufficient to complete GPU checkpointing and orderly shutdown. Extended hold on BESS alone is not the design intent — the block is island-operated; gas supply continuity is the primary reliability path.

---

## 7. Chemistry

**LiFePO4 (LFP).** Source: BOD-001 E-13.

| Criterion | LFP position |
|---|---|
| Thermal runaway risk | Lowest of commercial lithium chemistries. No O₂ release on failure. |
| Cycle life | 3,000–6,000 cycles at 80% DOD — essential for daily AI dispatch cycling |
| Temperature tolerance | Wider charge/discharge range than NMC — suitable for Louisiana outdoor pad with thermal management |
| NFPA 855 compliance path | Cleaner AHJ submission than NMC or NCA; FM Global rating precedent exists for LFP outdoor containers |
| ITC domestic content eligibility | Depends on manufacturing location — see vendor table §8 |

**Eliminated chemistries:** NCA (Samsung SDI SBB 1.5) — thermal runaway risk not compatible with outdoor AI factory pad adjacent to compute buildings. NMC — higher energy density not needed; cycle life and temperature trade-offs not justified.

---

## 8. DC coupling architecture

**Source:** ELEC-001 §7–8; BOD-001 E-11, E-12.

```
BESS battery enclosure (1,100–1,500 VDC output)
    │
    ▼
Bidirectional DC-DC converter (SiC-based)
  ├─ Continuous: ~2 MW
  ├─ Peak: ~4 MW
  ├─ Response: microsecond–millisecond (SiC switching)
  └─ Regulates to 800 VDC bus voltage
    │
    ▼
SSCB (solid-state circuit breaker)
    │
    ▼
Blocking diode (prevents backfeed from bus to BESS DC-DC on fault)
    │
    ▼
800 VDC common busway (one per block)
```

**Why DC-coupled:** The BESS does not output natively at 800 VDC. All viable LFP containerized battery packs output 1,100–1,500 VDC from the battery enclosure. The bidirectional DC-DC converter sits between the battery and the bus — it is the interface, the regulator, and the protection boundary. This is not a compromise; it is the standard topology for DC-coupled BESS at this voltage level.

**Why not AC-coupled at MV:** Placing an inverter at the 13.8 kV bus would require: inverter → step-up transformer → MV tie breaker → block MV bus. Response time measured in cycles, not microseconds. Does not place the storage resource on the same rail as the GPU load. Increases hardware count and failure modes. Not compatible with OCP Stage 1d / NVIDIA DSX 800 VDC architecture.

**Bidirectional DC-DC converter spec (working):**
- SiC switching devices — required for microsecond response
- Bidirectional — charges BESS from bus (solar recapture, load-shifting) and discharges to bus (contingency, transient)
- Operating input voltage range: 1,100–1,500 VDC (matches BESS pack output across full SOC)
- Output voltage: 800 VDC regulated (tight regulation, <1% steady-state deviation)
- Power rating: 2 MW continuous, 4 MW 10-second peak
- Efficiency: ≥97% at rated power (SiC target)
- Isolation: galvanic isolation required — battery pack negative and bus negative must be isolated to maintain fault discrimination
- Communication: Modbus TCP / CANBUS to L1 block PLC; IEC 61850 GOOSE for fast protection signals

**SSCB at bus tie:** Solid-state circuit breaker at the bus connection point. Sub-millisecond trip. Coordinates with blocking diode to prevent fault propagation from 800 VDC bus into the DC-DC converter or BESS pack.

---

## 9. Vendor evaluation

### 9.1 Shortlisted — three viable

#### Saft (TotalEnergies) — Intensium Flex

| Parameter | Detail |
|---|---|
| Chemistry | LFP |
| Capacity | 3.4 / 4.3 / 5.1 MWh — three configurations per 20-ft container |
| Architecture | DC block — no integrated PCS/inverter; requires external bidirectional DC-DC |
| Output voltage | Up to 1,500 VDC |
| Container | 20-ft standard ISO |
| UL 9540A | Designed to NFPA 855; DC-version UL 9540A listing not yet confirmed (DC production started late 2025). Verify with Saft before AHJ submittal. |
| US contact | Saft US, Cockeysville MD, +1 410 771 3200 |
| RFQ angle | TotalEnergies parent — energy company that understands natural gas, fuel cells, behind-the-meter. Opens a different conversation than a pure battery company. |
| Status | Viable. Engage after BESS-RFQ-001 is drafted. |

#### LG Energy Solution Vertech — JF2 DC LINK

| Parameter | Detail |
|---|---|
| Chemistry | LFP — manufactured in Holland, Michigan |
| Capacity | 5.11 MWh |
| Architecture | DC block — no integrated inverter |
| Output voltage | 1,134–1,499 VDC (confirmed published datasheet) |
| Container | 23 ft wide — NOT standard ISO. Requires flatbed transport. Confirm pad logistics and crane requirements before ordering. |
| UL 9540A | Confirmed. NFPA 855, NFPA 69, UL 9540 all confirmed. |
| US manufacturing | Holland, Michigan. Best domestic content story for ITC purposes. |
| RFQ angle | Cleanest domestic manufacturing narrative. ITC domestic content eligibility strongest of shortlist. |
| Status | Viable. Flag 23-ft width at pad planning stage before committing. |

#### Fluence (Siemens + AES JV) — Gridstack Pro

| Parameter | Detail |
|---|---|
| Chemistry | LFP — AESC HC-L530A cell |
| Capacity | 4.9–5.6 MWh per 20-ft enclosure |
| Architecture | DC block — no integrated inverter; requires external PCS |
| Output voltage | Up to 1,500 VDC |
| Container | 20-ft enclosure (ships in 40-ft for logistics — not ISO corner-cast) |
| UL 9540A | Confirmed. Large-scale fire tests completed June 2025, observed by CSA Group at Safe Laboratories NC. Exceeded current UL 9540A requirements. NFPA 855 (2026) compliance documentation in preparation. |
| Grid-forming / islanded | Confirmed — "can be used partially or fully off-grid." Only vendor on shortlist that explicitly confirmed off-grid island operation. |
| US contact | Fluence Energy (NASDAQ: FLNC), Arlington VA, +1 703 682 2700 |
| RFQ angle | Strongest compliance documentation. Grid-forming / islanded confirmation is the single most important spec for behind-the-meter permanent island. Frame conversation around total multi-site volume (10 sites × 40 MWh = 400 MWh) to get traction — typical Fluence engagements are 100 MWh+. |
| Status | Preferred based on island-mode confirmation. Engage first. |

### 9.2 Hold — CATL

| Parameter | Detail |
|---|---|
| Products | EnerC+ (4.07 MWh / 20-ft), TENER (6.25 MWh / 20-ft) |
| Chemistry | LFP |
| Architecture | DC block |
| UL 9540A | Confirmed for EnerC+. TENER (2025) — not yet confirmed. |
| Hold reason | Chinese manufacturer. Section 301 tariffs create material cost uncertainty. ITC domestic content eligibility blocked. |
| Status | Hold pending tariff clarity. Best product-to-price ratio on the market but tariff exposure is a real cost risk. |

### 9.3 Eliminated

| Vendor | Reason |
|---|---|
| POWIN | Bankrupt May 2025. Acquired by FlexGen. Not evaluated. |
| Wärtsilä Quantum3 | AC block — integrated inverter inside container. Adding a rectifier downstream to reach 800 VDC bus defeats efficiency advantage. Eliminated. |
| Samsung SDI SBB 1.5 | NCA chemistry. SBB 2.0 LFP not in production. Eliminated on chemistry grounds. |
| Rittal | Enclosure company only. No battery product. |
| Eaton xStorage | Working vendor in eng-pack-5MW Rev 3.0 §24 (Marlie 5 MW block context). Requires re-evaluation at CG260-16 / Trappey's scale — Eaton's 800 VDC DC-coupling confirmation at the ~2 MW continuous / 4 MW peak rating required. Do not carry forward from Marlie spec without RFQ validation. |

**Note on Eaton xStorage:** eng-pack-5MW carried Eaton as the working BESS vendor for the Marlie block (G3520K, 480 VAC, ≤10 MW). Trappey's is a different scale — CG260-16, 13.8 kV, 11 blocks, 40 MWh facility. Eaton is not eliminated; it is returned to open competition. If Eaton can confirm DC-coupled bidirectional operation at the required ratings, it re-enters shortlist consideration.

### 9.4 PCS layer — Hitachi Energy AMPS

**Hitachi Energy AMPS (Advanced Multiport Power Station)**

The bidirectional DC-DC converter between the BESS battery pack and the 800 VDC bus may be supplied by the BESS vendor as an integrated system or sourced separately. Hitachi Energy AMPS is the confirmed architecture candidate for the PCS function.

| Parameter | Detail |
|---|---|
| Function | Accepts multiple DC input voltages simultaneously (1,500 V solar, 800V+ genset-rectifier, BESS pack output) |
| Bus regulation | Regulates and stabilizes 800 VDC output |
| BESS management | Manages BESS charge/discharge per L1/L3 dispatch commands |
| Input range | Validated at 1,550 VDC — covers full BESS pack output range |
| Architecture | DC-coupled throughout — no AC conversion |
| Integration | No public validated pairing with Saft / LG ES Vertech / Fluence documented. Ask Hitachi directly for battery partner list — commercial, not technical. Voltage ranges are compatible. |
| Contact | hitachienergy.com/products-and-solutions/power-conversion/advanced-multiport-power-stations-amps |
| Status | Confirmed architecture candidate. Engage alongside shortlisted BESS vendors — ask each BESS vendor whether their pack has been validated with Hitachi AMPS, or whether they supply their own bidirectional DC-DC. |

**SPOC Grid (secondary note):** Trussville AL. Oil and gas VFD company entering 800 VDC data center architecture. OCP ESS whitepaper contributor. Not a replacement for Hitachi AMPS — no proven data center deployments. Monitor; may be relevant for Haynesville/Permian Basin deployments given oil and gas background.

---

## 10. AMCL integration

**Source:** BOD-001 A-04, A-09; ELEC-001 §12.

The BESS is dispatched at two control tiers:

**L1 — Block PLC (deterministic, local):**
- Receives real-time bus voltage, DC-DC converter state, BESS SOC and temperature
- Executes frequency-based BESS dispatch: detects Hz drop at UFLS thresholds, triggers DC-DC inject mode before UFLS trips loads
- Executes contingency dispatch: single-genset trip signal → DC-DC to peak inject mode within milliseconds
- Safety interlocks: SOC floor (do not discharge below 10% except gas-loss graceful shutdown), temperature limits, cell voltage limits — cannot be overridden from L3
- Cannot be overridden by L3 dispatch on safety parameters

**L3 — AMCL AI dispatch (optimization layer):**
- Sets DC-DC charge/discharge setpoints within L1 safety envelope
- Orchestrates BESS across four operating functions: transient buffer (always enabled), contingency reserve (SOC floor maintenance), solar recapture (charge when PV overproduces), load shifting (charge off-peak, discharge peak)
- Cross-block BESS SOC coordination — ensures no block enters contingency scenarios without adequate SOC reserve
- Gas supply awareness: if pipeline pressure drops, L3 pre-charges all blocks to SOC ceiling before expected curtailment

**BESS communication path:**
- Battery BMS → L1 block PLC: SOC, cell voltages, temperatures, alarms — Modbus TCP or CANBUS (vendor-dependent)
- DC-DC converter → L1 block PLC: power setpoint, mode, fault status — IEC 61850 GOOSE for protection; Modbus TCP for dispatch
- L1 block PLC → L2 SCADA: BESS historian points (~50 per block: SOC, power, voltage, temperature, fault codes)
- L2 SCADA → L3 AMCL: aggregated BESS state across all 11 blocks; OPC-UA publish

---

## 11. Physical installation

**Location:** Rear slab (42,000 sq ft), behind Building 3/4 compute halls. Shared with genset installation area. BOD-001 B-05.

**Container layout:** 11 blocks × 1–2 BESS containers per block (depending on final MWh selection). Saft 4.3 MWh or LG ES Vertech 5.11 MWh = 1 container per block at 3.6 MWh working. Fluence Gridstack Pro 4.9–5.6 MWh = 1 container per block.

**Setback:** NFPA 855 (2026 edition) governs minimum separation between BESS containers, between BESS and buildings, and between BESS and fuel storage/gas lines. AHJ (Lafayette Parish) submittal requires NFPA 855 compliance documentation. Fluence has NFPA 855 (2026) documentation in preparation — strongest AHJ path.

**Fire protection:** Integrated thermal runaway detection in battery BMS. Site-level fire suppression for BESS yard per BOD-001 §J. FM Global preferred for insurance rating — FM 5-33 (large-scale energy storage) governs outdoor LFP containers.

**Utility connections per BESS container:**
- DC power: cable run from BESS container to bidirectional DC-DC converter skid, then to 800 VDC bus SSCB panel
- Aux AC power: ~80 kW per block for BESS HVAC, BMS compute, fire suppression controls — fed from 480 VAC BESS aux feeder per ELEC-001 §4 (E-29)
- Communications: fiber to L1 block PLC rack
- Fire suppression water demand: sized per NFPA 855 and AHJ requirement

---

## 12. Protection and safety

**Source:** BOD-001 E-11, E-12; ELEC-001 §7.

**DC side protection hierarchy (BESS to bus):**

1. Battery BMS — cell-level over/undervoltage, over-temperature, overcurrent. Trips battery contactor inside pack. First line.
2. DC-DC converter internal protection — overcurrent, overvoltage at DC-DC terminals. Shuts down converter.
3. SSCB at bus tie — solid-state breaker on 800 VDC bus. Sub-millisecond. Isolates converter output from bus on DC fault.
4. Blocking diode — prevents bus fault energy from flowing into DC-DC converter and BESS pack when SSCB trips.

**Coordination note:** The interaction between BESS battery contactor, DC-DC internal protection, SSCB, and blocking diode constitutes the DC protection scheme at the BESS bus tie. Detailed pickup settings, coordination intervals, and CT designations for the SSCB belong in ST-TRAP-PROT-001 (protection coordination study, not yet drafted).

**NFPA 855 requirements for outdoor LFP:**
- Thermal runaway detection and notification
- Automatic fire suppression if integrated (required for certain occupancy classifications)
- Minimum separation distances from property lines, buildings, and fuel storage
- Emergency responder access and hazard marking
- All of the above to be verified against Lafayette Parish AHJ interpretation

---

## 13. Open items ledger

| Ref | Item | Blocked on | Priority |
|---|---|---|---|
| E-10 | Per-block BESS sizing validation (3.6 MWh working, 3–5 MWh envelope) | Contingency analysis | C1 |
| E-10 | BESS contingency scenarios validated against CG260-16 governor ramp data | Cat CSA | C1 |
| E-12 | Bidirectional DC-DC converter vendor selection | BESS RFQ — vendor may supply integrated DC-DC or require Hitachi AMPS | C1 |
| E-13 | BESS container vendor selection (Saft / LG ES Vertech / Fluence) | BESS RFQ package (ST-TRAP-BESS-RFQ-001, not yet drafted) | C1 |
| PROT | DC protection coordination — SSCB pickup settings, blocking diode spec, coordination with BMS contactor | ST-TRAP-PROT-001 | C1 |
| NFPA | NFPA 855 (2026) AHJ interpretation — Lafayette Parish | AHJ pre-application meeting | C1 |
| PHYS | Rear slab container layout — NFPA 855 setbacks vs genset placement | Physical layout study + AHJ | C2 |
| ITC | Domestic content verification for ITC basis — Saft (France) vs LG ES Vertech (Holland MI) | Tax counsel + vendor | C2 |
| HITACHI | Hitachi AMPS compatibility with shortlisted BESS packs (battery partner list) | Hitachi Energy engagement | C2 |
| CATL | CATL tariff exposure and ITC eligibility — hold pending Section 301 clarity | Policy / tax counsel | C3 |

---

## 14. Revision plan

- **Rev 0.1 (current)** — first issue. Role, sizing, chemistry, topology, vendor shortlist, AMCL integration, protection framework. Companion to ELEC-001 Rev 1.2 and BOD-001 Rev 0.4.
- **Rev 0.2** — after Cat CSA returns governor data. Updates contingency scenario sizing in §6; validates 3.6 MWh working or shifts envelope.
- **Rev 0.3** — after RFQ responses received from Saft, LG ES Vertech, Fluence. Updates §8 with scored vendor comparison. Locks BESS container vendor (E-13) and DC-DC converter vendor (E-12).
- **Rev 0.4** — after PROT-001 completes. Updates §12 with locked DC protection coordination settings.
- **Rev 1.0** — ready for external circulation. All C1 items closed. Paired with SLD-001 Rev 1.0 and PROT-001 Rev 1.0.

## 15. Approval

Rev 0.1 does not carry external circulation approval. Architecture inherits from ELEC-001 Rev 1.2 and BOD-001 Rev 0.4 approval status. External distribution waits for Rev 1.0, gated on all C1 items per §13.

---

**End of ST-TRAP-BESS-001 Rev 0.1.**
