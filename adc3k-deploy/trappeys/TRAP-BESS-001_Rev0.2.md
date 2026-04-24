# ST-TRAP-BESS-001 — BESS Architecture Basis — Rev 0.2

**Document:** Battery Energy Storage System Architecture Basis
**Project:** Trappey's AI Center, Lafayette, Louisiana
**Revision:** 0.2 — AC coupling rewrite; 480 VAC block bus topology replacing DC coupling; companion to ELEC-001 Rev 1.3 and BOD-001 Rev 0.6
**Date:** April 23, 2026
**Owner:** Scott Tomsu
**Status:** Working draft

---

## Revision Log

| Rev | Date | Changes |
|---|---|---|
| 0.1 | 2026-04-17 | First issue — DC-coupled BESS on block-level 800 VDC bus. Companion to ELEC-001 Rev 1.2 and BOD-001 Rev 0.5. |
| **0.2** | **2026-04-23** | **AC coupling rewrite per BOD-001 Rev 0.6 E-11/E-12. Block-level 800 VDC bus eliminated. BESS connects to 480 VAC block bus via Hitachi AMPS PCS SiC bidirectional inverter. §3 role updated. §8 DC coupling section replaced with AC coupling section. §9.4 Hitachi AMPS updated to PCS function. §12 protection hierarchy rewritten for AC topology. Wärtsilä Quantum3 elimination reason updated. Open items and revision plan updated.** |

---

## 1. Purpose

Defines the BESS architecture for Trappey's AI Center. Establishes the role, sizing basis, chemistry selection, AC coupling topology, vendor shortlist, and AMCL integration for the block-level battery system. Serves as the engineering anchor for the BESS RFQ package.

This document does not cover: solar PV inverter interface to 480 VAC block bus (ST-TRAP-SOLAR-001), in-row rack BBU and PCS inside cassette on the cassette 800 VDC internal bus (locked in ELEC-001 §7 and Cassette-ELEC-001), or protection coordination across the AC-DC boundary (ST-TRAP-PROT-001).

## 2. Relationship to other documents

**Upstream (this document inherits from):**

- BOD-001 Rev 0.6 — ledger authority; E-10 through E-13 are the source entries
- ELEC-001 Rev 1.3 — BESS sizing, power rating, coupling topology, contingency scenarios (§8)
- TRAP-MASTER-ENG-001 Rev 0.4 — block 480 VAC bus structure; §4 BESS AC-coupled section

**Downstream (inherits from this document):**

- ST-TRAP-SLD-001 — formal single-line; BESS PCS tie to 480 VAC switchboard with CT/PT designations
- ST-TRAP-PROT-001 — protection coordination at PCS AC output breaker; LSIG trip settings
- ST-TRAP-BESS-RFQ-001 Rev 0.2 — pending; Rev 0.1 superseded (DO NOT DISTRIBUTE)
- ST-TRAP-BESS-ARCHDIAG-001 Rev 0.2 — visual companion to this document

---

## 3. Role and operating principle

**The BESS is the block-level system stabilizer, not backup.**

It is always active on the 480 VAC block bus. It does not sit idle waiting for a fault — it runs continuously in charge/discharge dispatch under AMCL L1 (deterministic) and L3 (AI) control, absorbing and injecting power in real time.

Four operating functions, in priority order:

1. **Transient buffer.** Sub-cycle response to genset governor lag during load swings at the block 480 VAC bus. The Cat CG260-16 governor requires finite time to settle after a step load change. Sub-100 ms GPU load swings are absorbed inside the cassette by the Delta rack internal BBU and PCS on the cassette 800 VDC internal bus — this layer is always present and does not involve the block BESS. The block-level BESS via Hitachi AMPS PCS handles sub-cycle to multi-minute events at the 480 VAC block bus, bridging the cassette primary feed voltage between governor command and mechanical settle.

2. **Contingency support.** Energy reserve for single-genset trip, partial gas curtailment, and full gas-loss graceful shutdown. See §6 for scenario sizing.

3. **Solar clip-recapture.** Absorbs First Solar overproduction that would otherwise require MPPT throttling. Releases during high-load periods under L3 dispatch.

4. **Load shifting.** Flattens genset loading within the 55–75% AI dispatch envelope. BESS absorbs overnight low-load excess and discharges into morning GPU ramp.

**What BESS is not:** It is not the primary voltage-forming source at the cassette 800 VDC internal bus — that bus is regulated by the Delta in-row rectifiers inside the cassette. The Hitachi AMPS PCS regulates 480 VAC bus voltage and dispatches charge/discharge from the block bus side. It is not a replacement for the in-row BBU + PCS storage inside each cassette (ELEC-001 E-20); those handle sub-100 ms GPU transients on the cassette-internal 800 VDC bus. The two layers are complementary and run in parallel.

---

## 4. Per-block sizing basis

**Source:** BOD-001 E-10; ELEC-001 §8.

| Parameter | Value | Status |
|---|---|---|
| Facility total (Stage 1, 11 blocks) | ~39.6 MWh as-procured (11 × 3.6 MWh/block); BOD E-10 carries 40 MWh as the round working target | W |
| Per-block allocation | 3.6 MWh working midpoint | W |
| Per-block envelope | 3–5 MWh | W |
| Sizing anchor | Three contingency scenarios — see §6 | W |

**Allocation math:** 40 MWh ÷ 11 blocks = 3.636 MWh/block → rounded to 3.6 MWh working. Installed capacity at 3.6 MWh/block × 11 = 39.6 MWh; difference from BOD 40 MWh target is 400 kWh (<1%), within the 30–50 MWh envelope. Use 39.6 MWh for vendor RFQ line items; use 40 MWh for round-number financial modeling. Actual per-block assignment may shift based on contingency analysis results (E-10 gated).

**Envelope logic:** 3 MWh is the floor set by the full gas-loss graceful shutdown scenario. 5 MWh provides headroom if the Cat CSA governor data shows slower-than-expected transient response, or if contingency analysis extends the graceful shutdown window beyond 20 minutes.

---

## 5. Power rating

**Source:** ELEC-001 §8.

| Parameter | Per block | Facility (11 blocks) |
|---|---|---|
| Continuous | ~2 MVA | ~22 MVA |
| Peak (short duration) | ~4 MVA (10 s) | ~44 MVA |

Continuous rating covers solar clip-recapture and load shifting. Peak rating covers single-genset trip transient — the largest expected power excursion during normal operation.

**Vendor filter:** PCS (bidirectional inverter) must confirm rated continuous and peak throughput at 480 VAC output across the full operating SOC range of the BESS pack. Derating at low SOC is a common failure mode — require power vs SOC curve in RFQ response.

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
| ITC domestic content eligibility | Depends on manufacturing location — see vendor table §9 |

**Eliminated chemistries:** NMC — higher energy density not needed at this application; lower cycle life and temperature tolerance vs LFP not justified for continuous outdoor dispatch duty. NCA — thermal runaway risk not compatible with outdoor AI factory pad adjacent to compute buildings.

---

## 8. AC coupling architecture

**Source:** BOD-001 E-11, E-12; ELEC-001 §7–8; TRAP-MASTER-ENG-001 Rev 0.4 §4.

```
BESS battery enclosure (1,100–1,500 VDC output)
    │
    ▼
Hitachi AMPS PCS — SiC bidirectional inverter
  ├─ Continuous: ~2 MVA
  ├─ Peak: ~4 MVA (10 s)
  ├─ Response: sub-cycle (ms)
  ├─ Input: 1,100–1,500 VDC from BESS pack
  └─ Output: 480 VAC 3-phase 60 Hz · ±1% voltage regulation
    │
    ▼
AC circuit breaker (standard draw-out LV breaker · LSIG trip)
    │
    ▼
Block 480 VAC main switchboard
    │
    ├──► Cassette primary feed 1 (Eaton Magnum DS · 6,000 A)
    ├──► Cassette primary feed 2
    ├──► Cassette primary feed 3
    └──► Cassette primary feed 4
```

**Why AC-coupled at 480 VAC block bus:** BESS output lands on the same voltage rail as the cassette primary feed. All block sources (gensets via transformer, BESS via PCS, solar via PV inverter) and all block loads (cassette 480 VAC feeds) converge at a single 480 VAC switchboard — one bus, standard LV protection gear, open vendor competition for both battery pack and PCS. No block-level DC bus required.

**Why NOT DC-coupled at cassette 800 VDC internal bus:** The cassette 800 VDC bus is inside the cassette enclosure, downstream of the Eaton Magnum DS disconnect and the Delta in-row rectifiers. Routing BESS 800 VDC cables into cassette interiors would violate the cassette IP boundary, require cassette-by-cassette cable penetrations, and place the BESS on the wrong side of the Eaton disconnect. Sub-100 ms GPU transients at the cassette 800 VDC level are handled by the Delta rack BBU+PCS already inside each cassette — block BESS does not belong on that bus.

**Hitachi AMPS PCS spec (working):**
- SiC switching devices — required for sub-cycle response
- Bidirectional — charges BESS from bus (solar recapture, load-shifting) and discharges to bus (contingency, transient)
- Operating input voltage range: 1,100–1,500 VDC (matches BESS pack output across full SOC)
- Output: 480 VAC 3-phase 60 Hz, ±1% voltage regulation
- Power rating: 2 MVA continuous, 4 MVA 10-second peak
- Efficiency: ≥97% at rated power (SiC target)
- Grid-forming capable: island-mode operation without upstream grid — required for permanent behind-the-meter island
- Anti-islanding: DISABLED (behind-the-meter island; no grid connection to protect)
- Communication: Modbus TCP / IEC 61850 GOOSE to L1 block PLC

**AC circuit breaker at bus tie:** Standard draw-out LV power circuit breaker with LSIG trip unit. Interrupts PCS output from 480 VAC switchboard on AC fault. No blocking diode. No SSCB. Standard protection coordination with other feeder breakers on the switchboard.

---

## 9. Vendor evaluation

### 9.1 Shortlisted — three viable (battery pack)

#### Saft (TotalEnergies) — Intensium Flex

| Parameter | Detail |
|---|---|
| Chemistry | LFP |
| Capacity | 3.4 / 4.3 / 5.1 MWh — three configurations per 20-ft container |
| Architecture | DC block — no integrated PCS/inverter; requires external bidirectional PCS (Hitachi AMPS or equivalent) |
| Output voltage | Up to 1,500 VDC |
| Container | 20-ft standard ISO |
| UL 9540A | Designed to NFPA 855; DC-version UL 9540A listing not yet confirmed (DC production started late 2025). Verify with Saft before AHJ submittal. |
| US contact | Saft US, Cockeysville MD, +1 410 771 3200 |
| RFQ angle | TotalEnergies parent — energy company that understands natural gas, fuel cells, behind-the-meter. Opens a different conversation than a pure battery company. |
| Status | Viable. Engage after BESS-RFQ-001 Rev 0.2 is drafted. |

#### LG Energy Solution Vertech — JF2 DC LINK

| Parameter | Detail |
|---|---|
| Chemistry | LFP — manufactured in Holland, Michigan |
| Capacity | 5.11 MWh |
| Architecture | DC block — no integrated inverter; requires external PCS |
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
| RFQ angle | Strongest compliance documentation. Grid-forming / islanded confirmation is the single most important spec for behind-the-meter permanent island. Frame conversation around total multi-site volume (10 sites × 40 MWh = 400 MWh) to get traction. |
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
| Wärtsilä Quantum3 | Integrated inverter + battery in single container. Does not support independent PCS vendor selection or battery pack decoupling. Not compatible with Hitachi AMPS PCS architecture where pack and PCS are separate procurements. |
| Samsung SDI SBB 1.5 | NMC chemistry. SBB 2.0 LFP not in production. Eliminated on chemistry grounds — NMC cycle life and temperature tolerance not justified vs LFP for this application. |
| Rittal | Enclosure company only. No battery product. |
| Eaton xStorage | Working vendor in eng-pack-5MW Rev 3.0 §24 (Marlie 5 MW block context). Requires re-evaluation at CG260-16 / Trappey's scale — Eaton's AC-coupled PCS confirmation at the ~2 MVA continuous / 4 MVA peak rating required for the 480 VAC block bus topology. Do not carry forward from Marlie spec without RFQ validation. |

### 9.4 PCS layer — Hitachi AMPS PCS

**Hitachi AMPS PCS (Advanced Multiport Power Station — PCS function)**

The SiC bidirectional PCS inverter between the BESS battery pack and the 480 VAC block bus. Hitachi AMPS PCS is the confirmed architecture candidate per BOD-001 E-11/E-12.

| Parameter | Detail |
|---|---|
| Function | SiC bidirectional inverter — converts 1,100–1,500 VDC from BESS pack to 480 VAC 3-phase 60 Hz output on block bus |
| Charge path | Accepts 480 VAC from block bus, rectifies to charge BESS pack (solar recapture, load-shifting) |
| Discharge path | Inverts BESS pack DC to 480 VAC for block bus injection (contingency, transient, load-shifting) |
| Bus regulation | Regulates 480 VAC output voltage; grid-forming island-mode capable |
| BESS management | Manages BESS charge/discharge per L1/L3 dispatch commands |
| Input range | 1,100–1,500 VDC — covers full BESS pack output range across SOC |
| Output | 480 VAC 3-phase 60 Hz, ±1% voltage regulation |
| Communication | Modbus TCP / IEC 61850 GOOSE to L1 block PLC |
| Status | Confirmed architecture candidate per BOD-001 Rev 0.6. Engage alongside shortlisted BESS vendors — ask each BESS vendor whether their pack has been validated with Hitachi AMPS PCS, or whether they supply their own bidirectional inverter. |

**Alternative PCS candidates (open competition):**
- Fluence Gridstack Pro with integrated power conversion module
- Sungrow PowerTitan 2.0 — integrated AC-coupled system; confirm island-mode
- Power Electronics FreeStor — modular PCS architecture; confirm 480 VAC 3-phase rating
- LG ES Vertech JF2 paired with Hitachi AMPS PCS — requires compatibility confirmation

---

## 10. AMCL integration

**Source:** BOD-001 A-04, A-09; ELEC-001 §12.

The BESS is dispatched at two control tiers:

**L1 — Block PLC (deterministic, local):**
- Receives real-time 480 VAC bus voltage, PCS inverter state, BESS SOC and temperature
- Executes frequency-based BESS dispatch: detects Hz drop at UFLS thresholds, triggers PCS discharge mode before UFLS trips loads
- Executes contingency dispatch: single-genset trip signal → PCS to peak discharge mode within milliseconds
- Safety interlocks: SOC floor (do not discharge below 10% except gas-loss graceful shutdown), temperature limits, cell voltage limits — cannot be overridden from L3
- Cannot be overridden by L3 dispatch on safety parameters

**L3 — AMCL AI dispatch (optimization layer):**
- Sets PCS charge/discharge setpoints within L1 safety envelope
- Orchestrates BESS across four operating functions: transient buffer (always enabled), contingency reserve (SOC floor maintenance), solar recapture (charge when PV overproduces), load shifting (charge off-peak, discharge peak)
- Cross-block BESS SOC coordination — ensures no block enters contingency scenarios without adequate SOC reserve
- Gas supply awareness: if pipeline pressure drops, L3 pre-charges all blocks to SOC ceiling before expected curtailment

**BESS communication path:**
- Battery BMS → L1 block PLC: SOC, cell voltages, temperatures, alarms — Modbus TCP or CANBUS (vendor-dependent)
- PCS inverter → L1 block PLC: power setpoint, mode, fault status — IEC 61850 GOOSE for protection; Modbus TCP for dispatch
- L1 block PLC → L2 SCADA: BESS historian points (~50 per block: SOC, power, voltage, temperature, fault codes)
- L2 SCADA → L3 AMCL: aggregated BESS state across all 11 blocks; OPC-UA publish

---

## 11. Physical installation

**Location:** Rear slab (42,000 sq ft), behind Building 3/4 compute halls. Shared with genset installation area. BOD-001 B-05.

**Container layout:** 11 blocks × 1–2 BESS containers per block (depending on final MWh selection). Saft 4.3 MWh oversizes the 3.6 MWh working target by ~19%; LG ES Vertech 5.11 MWh oversizes by ~42%; Fluence Gridstack Pro 4.9–5.6 MWh oversizes by ~36–56%. In all three cases, 1 container per block delivers capacity above the 3.6 MWh working target — installed capacity is the container nameplate, not 3.6 MWh.

**Setback:** NFPA 855 (2026 edition) governs minimum separation between BESS containers, between BESS and buildings, and between BESS and fuel storage/gas lines. AHJ (Lafayette Parish) submittal requires NFPA 855 compliance documentation. Fluence has NFPA 855 (2026) documentation in preparation — strongest AHJ path.

**Fire protection:** Integrated thermal runaway detection in battery BMS. Site-level fire suppression for BESS yard per BOD-001 §J. FM Global preferred for insurance rating — FM 5-33 (large-scale energy storage) governs outdoor LFP containers.

**Utility connections per BESS container:**
- AC power: cable run from BESS container to Hitachi AMPS PCS skid, then AC circuit breaker to 480 VAC block switchboard
- Aux AC power: ~80 kW per block for BESS HVAC, BMS compute, fire suppression controls — fed from 480 VAC BESS aux feeder
- Communications: fiber to L1 block PLC rack
- Fire suppression water demand: sized per NFPA 855 and AHJ requirement

---

## 12. Protection and safety

**Source:** BOD-001 E-11, E-12; ELEC-001 §7; TRAP-MASTER-ENG-001 Rev 0.4 §3.4.

**AC side protection hierarchy (BESS PCS to block bus):**

1. Battery BMS — cell-level over/undervoltage, over-temperature, overcurrent. Trips battery contactor inside pack. First line.
2. PCS inverter internal protection — overcurrent, overvoltage at PCS AC terminals. Shuts down inverter.
3. AC circuit breaker at bus tie — standard draw-out LV power circuit breaker, LSIG trip unit. Interrupts PCS AC output from 480 VAC switchboard. No blocking diode. No SSCB. Standard LV coordination with other feeder breakers.
4. Switchboard main breaker — upstream protection at block 480 VAC switchboard. Coordinates with all feeder breakers per standard LV protection study.

**No blocking diode. No SSCB at bus tie.** Those devices belong to DC bus topologies. The 480 VAC block bus uses standard AC protection gear throughout.

**Coordination note:** Pickup settings, coordination intervals, and CT designations for the PCS AC breaker and switchboard main breaker belong in ST-TRAP-PROT-001 (protection coordination study, not yet drafted).

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
| E-11 | Hitachi AMPS PCS vendor selection — integrated PCS with BESS pack or standalone | BESS RFQ | C1 |
| E-12 | PCS island-mode confirmation — 480 VAC grid-forming at block bus | BESS RFQ vendor response | C1 |
| E-13 | BESS container vendor selection (Saft / LG ES Vertech / Fluence) | BESS RFQ package (Rev 0.1 superseded — Rev 0.2 pending) | C1 |
| PROT | AC protection coordination — PCS breaker LSIG settings, coordination with switchboard main | ST-TRAP-PROT-001 | C1 |
| NFPA | NFPA 855 (2026) AHJ interpretation — Lafayette Parish | AHJ pre-application meeting | C1 |
| PHYS | Rear slab container layout — NFPA 855 setbacks vs genset placement | Physical layout study + AHJ | C2 |
| ITC | Domestic content verification for ITC basis — Saft (France) vs LG ES Vertech (Holland MI) | Tax counsel + vendor | C2 |
| HITACHI | Hitachi AMPS PCS compatibility with shortlisted BESS packs (battery partner list) | Hitachi Energy engagement | C2 |
| CATL | CATL tariff exposure and ITC eligibility — hold pending Section 301 clarity | Policy / tax counsel | C3 |

---

## 14. Revision plan

- **Rev 0.1** (superseded) — first issue. DC-coupled topology. Companion to ELEC-001 Rev 1.2 and BOD-001 Rev 0.5.
- **Rev 0.2 (current)** — AC coupling rewrite per BOD-001 Rev 0.6. Block 480 VAC bus topology. BESS via Hitachi AMPS PCS. §8 and §12 rewritten. Companion to ELEC-001 Rev 1.3 and BOD-001 Rev 0.6.
- **Rev 0.3** — after Cat CSA returns governor data. Updates contingency scenario sizing in §6; validates 3.6 MWh working or shifts envelope.
- **Rev 0.4** — after RFQ responses received from Saft, LG ES Vertech, Fluence. Updates §8 and §9 with scored vendor comparison. Locks BESS container vendor (E-13) and PCS vendor (E-11/E-12).
- **Rev 0.5** — after PROT-001 completes. Updates §12 with locked AC protection coordination settings.
- **Rev 1.0** — ready for external circulation. All C1 items closed. Paired with SLD-001 Rev 1.0 and PROT-001 Rev 1.0.

## 15. Approval

Rev 0.2 does not carry external circulation approval. Architecture inherits from ELEC-001 Rev 1.3 and BOD-001 Rev 0.6 approval status. External distribution waits for Rev 1.0, gated on all C1 items per §13.

---

**End of ST-TRAP-BESS-001 Rev 0.2.**
