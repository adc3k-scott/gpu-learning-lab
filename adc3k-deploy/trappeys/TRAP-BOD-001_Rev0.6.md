# ST-TRAP-BOD-001 — Basis of Design — Rev 0.6

**Document:** Basis of Design, Trappey's AI Center
**Project:** Trappey's AI Center — 22-acre historic cannery site, Lafayette, Louisiana
**Revision:** 0.6 — cassette architecture updated to Rev 1.3 (480 VAC primary, 9 compute racks, CoolIT CHx2000 external CDU); BESS and solar AC-coupled at block 480 VAC bus; Vermilion River supplemental removed; transformer protection corrected; IT load and GPU count cascaded.
**Date:** April 23, 2026
**Owner:** Scott Tomsu
**Status:** Working draft — canonical source of design parameters for all downstream documents

## Rev 0.6 change summary

Cassette primary input changed from 800 VDC umbilical to 480 VAC feed per Cassette-ELEC-001 Rev 1.3 §1. Five Delta 660 kW in-row power racks (R11–R15) now located inside Cassette boundary; perform 480 V AC → 800 V DC conversion internally. 800 V DC bus exists only inside each Cassette — not a shared block-level bus. Compute rack count per cassette corrected to 9 (R1–R9) + 1 control (R10) + 5 Delta (R11–R15) = 15 rack positions (C-11). IT load per cassette 2,300 → 2,070 kW (C-15). Stage 1 IT 101.2 → 91.1 MW (P-03). Full Build 202.4 → 182.2 MW (P-05). GPU targets revised: 28,512 Stage 1, 57,024 Full Build (P-07, P-08). CDU updated to CoolIT CHx2000 external skid per Cassette-COOL2-001 Rev 1.0 (C-03; was Boyd 2,000 kW internal). Secondary cooling per cassette 1,840 → ~1,656 kW (C-17); Stage 1 rejection ~72.9 MW (T-04, T-08). Munters updated HCD/MCD → DSS Pro (C-19). C-24 ECP connection updated: 800 VDC umbilical → 480 VAC primary feed. Block-level 800 VDC common busway eliminated (E-07, E-22 updated). BESS AC-coupled to block 480 VAC bus via Hitachi AMPS PCS (E-11, E-12). Solar AC-coupled to block 480 VAC bus via inverter (E-17). E-25 in-row rack count confirmed 5 per cassette inside Cassette. E-27 transformer protection corrected to 87T overall differential. E-29 feeder categories updated to 4 × cassette 480 VAC feeds. E-30 cassette internal topology updated. T-06 (Vermilion River supplemental) removed. R-03 updated to blowdown only. §F Vermilion River paragraph removed; cooling tower rejection numbers updated. §D PUE note updated. §B LPDES scope updated. §G water section updated. §N BESS vendor shortlist updated. Revision plan updated.

---

## Purpose

Single source of truth for every design parameter on the Trappey's AI Center. Downstream documents cite BOD-001 rather than restating values. When a working assumption becomes locked, only BOD-001 changes.

## How to use

Every parameter carries a status tag:

- **L (Locked)** — validated, cited externally, not changed without a BOD-001 revision
- **W (Working)** — committed enough for downstream engineering; may move based on vendor feedback or analysis
- **O (Open)** — decision not made; downstream must not cite a value

The Decision Ledger is the one-page scan. Sections A–N hold the rationale.

---

## Decision Ledger

### Project-level

| # | Parameter | Value | Status | Updated |
|---|---|---|---|---|
| P-01 | Site | 22-acre Trappey's Cannery site, Vermilion River, Lafayette, LA | L | 2026-04-14 |
| P-02 | Historic structures on site | 12 nationally registered | L | 2026-04-14 |
| P-03 | Stage 1 IT load | 91.1 MW (44 × 2,070 kW) | L | 2026-04-23 |
| P-04 | Stage 1 cassette count | 44 | L | 2026-04-14 |
| P-05 | Full Build IT load | 182.2 MW (88 × 2,070 kW) | L | 2026-04-23 |
| P-06 | Full Build cassette count | 88 | L | 2026-04-14 |
| P-07 | GPU target Stage 1 | 28,512 NVIDIA Vera Rubin (44 × 648) | W | 2026-04-23 |
| P-08 | GPU target Full Build | 57,024 (88 × 648) | W | 2026-04-23 |
| P-09 | Revenue model | Colocation only, base case | L | 2026-04-16 |
| P-10 | Sell-back to LUS | Excluded from base case; future optionality only | L | 2026-04-16 |

### Regulatory and incentive

| # | Parameter | Value | Status |
|---|---|---|---|
| R-01 | LDEQ thermal rise limit | 2.8°C (5°F) above ambient after mixing | L |
| R-02 | LDEQ absolute max water temp | 32.2°C (90°F); no additional heat above | L |
| R-03 | LPDES permit required | Yes — cooling tower blowdown only | L |
| R-04 | Title V air permit | Yes — 44 gensets at CG260-16 scale triggers | W |
| R-05 | SHPO Part 1 | Prepared, not yet filed | O |
| R-06 | SHPO Part 2 | Scope TBD within HTC constraints | O |
| R-07 | HTC stack | 45% (Federal 20% + LA 25%) | L |
| R-08 | LA ITEP | To be filed before any construction | W |
| R-09 | Parish PILOT | Pursued in place of HB 827 (below $200M threshold) | L |
| R-10 | LA corporate tax rate (financial model) | 5.5% | L |

### Cassette platform (product IP) — per Cassette-ELEC-001 Rev 1.3

| # | Parameter | Value | Status |
|---|---|---|---|
| C-01 | Cassette architecture | Locked as IP core; vendor-neutral outside | L |
| C-02 | Cassette internal DC bus | 800 VDC bus — internal to Cassette only; not present at cassette ECP boundary | L |
| C-03 | CDU | CoolIT CHx2000; external CDU skid per Cassette-COOL2-001 Rev 1.0 | L |
| C-04 | CDU supply temperature | ≤45°C to rack | L |
| C-05 | Fire suppression | Novec 1230 + VESDA, NFPA 2001 | L |
| C-06 | Cassette BMS | NVIDIA Jetson AGX Orin, 148 sensor channels | L |
| C-07 | Container width constraint | 93" internal; 40 ft HC ISO external | L |
| C-08 | Enclosure | 40 ft HC ISO, NEMA 3R | L |
| C-09 | External dimensions | 40' × 8' × 9.5' | L |
| C-10 | GPU platform | NVIDIA Vera Rubin NVL72 | L |
| C-11 | Rack positions per cassette | 9 NVL72/CPX compute (R1–R9) + 1 control (R10) + 5 Delta 660 kW in-row (R11–R15) = 15 total | L |
| C-12 | GPUs per compute rack | 72 (NVL72 tray) | L |
| C-13 | HBM4 memory | 288 GB/GPU, 20.7 TB/rack, 186.3 TB/cassette (9 racks × 20.7 TB) | L |
| C-14 | IT load per rack | 230 kW | L |
| C-15 | IT load per cassette | 2,070 kW (9 × 230 kW) | L |
| C-16 | Facility load per cassette | ~2,295 kW | W |
| C-17 | Secondary cooling demand | ~1,656 kW per cassette to site heat rejection (80% × 2,070 kW IT) | W |
| C-18 | Internal power distribution | 5 × Delta 660 kW in-row racks (AC-DC, R11–R15); 800 V DC internal busway to compute and control racks | L |
| C-19 | Dehumidification | Munters DSS Pro, ≤50% RH | L |
| C-20 | Munters regen heat draw | ~125 kW per cassette (exhaust slip-stream) | L |
| C-21 | Network | NVIDIA QM9700 InfiniBand | L |
| C-22 | Hot-swap disconnects | Staubli (internal cassette connections) | L |
| C-23 | Cassette-level PUE | ≤1.15 design day; target ≤1.11 average | W |
| C-24 | External connections (single panel) | 480 VAC primary feed, CHW supply/return (CDU skid ECP boundary), fiber, BMS, exhaust regen | L |
| C-25 | Immersion fluid vendor (future rev) | Dual-track: GRC vs Submer | O |

### Electrical architecture

| # | Parameter | Value | Status |
|---|---|---|---|
| E-01 | Operating mode | Behind-the-meter permanent island, day one | L |
| E-02 | LUS Pinhook interconnect | Optional future feature at LUS cost/schedule | L |
| E-03 | Prime mover | Cat CG260-16 gas genset | L |
| E-04 | Genset count | 44 (11 blocks × 4) | L |
| E-05 | Nominal loading per genset | 63–65% steady-state AI dispatch; 61.5% Cat longevity reference / light-load floor | W |
| E-06 | Genset MV voltage | 13.8 kV working | W |
| E-07 | Campus electrical topology | Replicated Marlie-pattern blocks; 480 VAC distribution to cassettes; BESS and solar AC-coupled at block 480 VAC bus; no MV ring | L |
| E-08 | Block step-down | Per-block MV→LV transformer (13.8 kV → 480 V, ~15 MVA) | W |
| E-09 | Cassette-side rectification | 480 V AC → 800 V DC inside Cassette via 5 × Delta 660 kW in-row racks (R11–R15) | L |
| E-10 | BESS size | 39.6 MWh working (11 blocks × 3.6 MWh); 30–50 MWh envelope | W |
| E-11 | BESS coupling | AC-coupled to block 480 VAC bus via Hitachi AMPS PCS bidirectional inverter | L |
| E-12 | BESS converter | Hitachi AMPS PCS bidirectional inverter on block 480 VAC bus; sub-second transient response | W |
| E-13 | BESS chemistry | LiFePO4 | W |
| E-14 | Solar array | First Solar Series 7 rooftop | L |
| E-15 | Solar DC bus voltage | 1500 VDC string | L |
| E-16 | Solar capacity | 2.05 MW | L |
| E-17 | Solar coupling | AC-coupled: 1500 VDC strings → inverter → block 480 VAC bus | L |
| E-18 | Protection philosophy | Island-only; no anti-islanding | L |
| E-19 | UFLS stages | Three: 59.5 / 59.2 / 58.9 Hz at block MV inlet | L |
| E-20 | In-row rack integrated storage | BBU + supercap sized for sub-100 ms GPU swings (inside Cassette) | L |
| E-21 | 800 VDC connector interface | Touch-safe mechanical interlock, EV-heritage per NVIDIA MGX — cassette-internal only | L |
| E-22 | Cassette-internal 800 VDC busway | Copper busway inside Cassette; not a shared block-level bus | L |
| E-23 | Inter-block tie (N+1 posture) | Open: 11 independent vs tied at aux point | O |
| **E-24** | **Primary in-row rack vendor** | **Delta 660 kW In-Row Power Rack — scored 4.75/5 vs Eaton 3.80, Schneider 3.15; procurement-ready today** | **W** |
| **E-25** | **In-row rack count per cassette** | **5 per cassette — confirmed inside Cassette (R11–R15) per Cassette-ELEC-001 Rev 1.3; 3,300 kW, 59.4% headroom vs 2,070 kW IT** | **L** |
| **E-26** | **Generator protection relay set** | **Per genset: 87G differential, 32 reverse power, 40 loss of excitation, 46 negative sequence, 47 phase sequence, 59/27 over/under-voltage, 64G stator ground, 78 out-of-step. Block bus: 87B differential.** | **W** |
| **E-27** | **Transformer protection** | **87T overall differential (single two-winding transformer), 49T thermal (RTDs), 63 pressure/gas (cast-resin equivalent)** | **W** |
| **E-28** | **LV secondary grounding** | **Solidly grounded wye at 480 VAC main with 50G residual ground sensing and LSIG trip unit on main** | **W** |
| **E-29** | **480 VAC feeder categorization** | **4 × cassette 480 VAC primary feeds (~9.2 MVA total) + BESS inverter (~2.1 MVA) + solar inverter (~2.1 MVA) + cooling tower MCC (~136 kW/block) + facility ancillary (~200 kW, SCADA/NOC/life safety)** | **W** |
| **E-30** | **Cassette internal electrical topology** | **480 VAC → 5 × Delta 660 kW in-row racks (R11–R15) → 800 VDC cassette-internal busway → 9 × NVL72/CPX compute racks + 1 control rack; auxiliary: Munters DSS Pro blowers, Jetson AGX Orin BMS (148 sensor channels)** | **L** |

### Thermal architecture

| # | Parameter | Value | Status |
|---|---|---|---|
| T-01 | Architecture | Genset exhaust heat → Munters dehumidification regen only. Cooling towers are primary heat rejection for cassette secondary cooling loop. No absorption chiller. | W |
| T-04 | Primary cold sink | Evaporative cooling towers — primary heat rejection for full cassette secondary cooling load (~72.9 MW Stage 1 / ~145.7 MW Full Build) | L |
| T-05 | Cooling tower type | TBD (wet vs hybrid vs adiabatic) | O |
| T-07 | Water tower (historic) | Deferred — no load-bearing role | L |
| T-08 | Stage 1 rejection to cooling towers | ~72.9 MW nominal (44 × ~1,656 kW cassette secondary); pending tower field sizing confirmation | O |
| T-09 | Tower makeup water (Stage 1 peak) | Pending tower field sizing with ~72.9 MW rejection duty | O |
| T-10 | Cassette cooling fluid | Direct-to-chip water-glycol | W |
| T-12 | Munters regen heat draw (Stage 1) | 5.5 MW deducted from exhaust (44 × 125 kW) | L |
| T-13 | Munters regen heat draw (Full Build) | 11.0 MW deducted (88 × 125 kW) | L |

### Structural / buildings

| # | Parameter | Value | Status |
|---|---|---|---|
| B-01 | Building 1 role | Historic restoration — NOC / partner hub / rooftop solar | L |
| B-02 | Building 2 role | Historic restoration — NOC / partner hub / rooftop solar | L |
| B-03 | Building 3 role | Compute hall — 20 cassettes | L |
| B-04 | Building 4 role | Compute hall — 24 cassettes | L |
| B-05 | Rear slab | 42,000 sq ft — genset installation + BESS | L |
| B-06 | Infrastructure yard | 28,000 sq ft — cooling and SCR | L |
| B-07 | Structural assessment status | Not commissioned for any building | O |

### Operations and AI control

| # | Parameter | Value | Status |
|---|---|---|---|
| A-01 | Operating philosophy | AI-controlled autonomous dispatch | L |
| A-02 | Genset dispatch | AI-optimized loading across 11 blocks; 61.5% nominal | L |
| A-03 | Thermal dispatch | AI-controlled pumps, tower fans, VFD-driven | L |
| A-04 | BESS dispatch | AI-orchestrated frequency support, thermal shifting, solar recapture | L |
| A-05 | AI model / vendor | Open — scope not defined | O |
| A-06 | Human-in-loop policy | Open — to be defined | O |
| A-07 | Cybersecurity framework | Open — NIST CSF / IEC 62443 candidates | O |
| A-08 | Staffing | "Substantial" construction, "high-wage technical" operations | L |
| **A-09** | **AMCL control architecture** | **Five-tier: L0 field devices · L1 block PLC · L2 plant SCADA · L3 AMCL AI dispatch · L4 HMI + operator override + IEC 62443 cybersecurity** | **W** |

### Naming and communication

| # | Parameter | Value | Status |
|---|---|---|---|
| N-01 | Project / company name in external docs | "Scott Tomsu" | L |
| N-02 | "Pinhook" spelling | One word | L |
| N-03 | FM Bank / Farmers Merchants Bank / Mark Sibley | Excluded from all project materials | L |

---

## A. Project identity and scope

22-acre Trappey's Cannery historic site on the Vermilion River. Adaptive reuse of twelve nationally registered historic structures. Four principal buildings (B1–B4) under active engineering. Supporting infrastructure on rear 42,000 sq ft slab and 28,000 sq ft infrastructure yard.

**Staging:** Stage 1 at 91.1 MW IT (44 cassettes × 2,070 kW, 28,512 GPU target); Full Build at 182.2 MW IT (88 cassettes, 57,024 GPU target). Per-cassette facility load ~2,295 kW. Stage 1 cassette total: ~101.0 MW. NVIDIA allocation is the gating variable and remains Open.

**Out of scope:** LUS sell-back revenue (base case), water tower as load-bearing element, residential repositioning, grid-parallel in any external-boundary sense.

## B. Regulatory framework

- **LDEQ water:** 5°F rise limit, 90°F absolute max, LPDES for cooling tower blowdown
- **LDEQ air:** Title V for 44 gensets; SCR in infrastructure yard for NOx; CO threshold carryover from ADC workstream
- **Historic preservation:** SHPO Part 1 prepared not filed; Part 2 scope TBD; do not claim completion externally
- **Incentives:** HTC 45% + LA ITEP (before construction) + Parish PILOT + LED engagement

## C. Cassette platform (IP core)

The cassette is the product. Everything outside the cassette is vendor-neutral and selected on price, lead time, availability. This framing has permitting and financing consequences.

All cassette values locked per Cassette-ELEC-001 Rev 1.3 and Cassette-MASS-001 Rev 3.0. Trappey's cassette is identical to the Rev 1.3 cassette; no changes inside the envelope at 44-cassette scale.

**Cassette-to-facility interface (single panel, 5 connections):** 480 VAC primary feed, CHW supply/return (CDU skid at cassette ECP boundary), fiber (data + control), BMS sensor aggregation, exhaust regen slip-stream.

**Open items at cassette interface:** Immersion fluid vendor (GRC vs Submer, deferred).

## D. Load and performance

Stage 1 IT: 91.1 MW (44 × 2,070 kW). Full Build IT: 182.2 MW. Per-cassette total facility: ~2,295 kW. Per-rack: 230 kW. Ancillary (NOC, office, lighting, security, non-IT HVAC, controls): working 3–5% of IT load.

Diversity factor working 0.95. AI control may flatten further.

**PUE (honest seasonal envelope):** Louisiana summer design day 1.2–1.3 with cooling towers carrying full cassette secondary load. Single-number PUE below 1.15 not claimed externally without qualifier.

## E. Electrical architecture

**Behind-the-meter permanent island from day one.** No LUS provisioning day one — spatial allocation only. If LUS engages later, at their cost and schedule.

**Replicated block architecture.** Trappey's = N replicated Marlie-pattern blocks. Each block: 4 × Cat CG260-16 per block paralleled at 13.8 kV, one step-down transformer per block (13.8 kV → 480 V, ~15 MVA), 480 VAC block bus distributes to 4 cassette primary feeds, BESS inverter, and solar inverter. AC-DC rectification happens inside each Cassette (5 × Delta 660 kW in-row racks, R11–R15). The 800 VDC bus exists only inside each Cassette — not a shared block-level bus. 11 independent blocks (base case) — no campus MV ring.

**What's different from Marlie:** CG260-16 generates at 13.8 kV not 480 V; per-block step-down transformer inserted. Cassette architecture is identical to Rev 1.3 cassette — 480 VAC in, internal rectification, no DC umbilical.

**Protection philosophy is island-only.** Per-genset relay set per E-26; transformer protection per E-27 (87T overall differential); block bus 87B; UFLS three-stage at block MV inlet. Cassette-internal DC protection (SSCB, blocking diodes) per Cassette-ELEC-001 Rev 1.3. Load-break contactors at each cassette 480 VAC feed.

**In-row power rack selection (E-24, E-25):** Delta 660 kW In-Row Power Rack, 5 per cassette inside the Cassette boundary (confirmed). Per rack: 6 × 110 kW PSU shelves, 480 kW aggregate BBU, Power Capacitance Shelf for sub-100 ms swings, 98% AC-DC at full load, touch-safe 800 VDC internal output.

**Single biggest technical risk:** CG260-16 governor response in island-mode 24/7 at variable loading under AI dispatch, with block-level AC-coupled BESS (Hitachi AMPS PCS) as first-line transient buffer. Cat CSA engagement is the most important external validation.

## F. Thermal architecture

**CHP → Munters only.** Genset exhaust heat routes exclusively to the Munters dehumidification regen slip-stream inside each cassette (T-12, T-13). No absorption chiller. Jacket water heat is rejected directly. Genset operating profile no longer couples to chiller thermodynamics.

**Cooling tower field (primary heat rejection, locked).** Cooling towers carry the full cassette secondary cooling load — ~72.9 MW at Stage 1 (44 × ~1,656 kW), ~145.7 MW at Full Build. Not a residual sink. Type — wet / hybrid / adiabatic — open per T-05. Wet is lowest capex with highest water consumption; hybrid cuts summer water 30–50%; adiabatic is limited by Louisiana wet-bulb at peak. Full dry excluded at this scale. Tower type selection follows field siting study (T-05, SITING-001).

**Cassette secondary cooling path.** GPU cold-plate warm water → CoolIT CHx2000 CDU (external skid per Cassette-COOL2-001 Rev 1.0) → facility CHW supply/return connection at cassette ECP → cooling tower plate HX → cooling tower. CDU supply requirement ≤45°C (C-04) is compatible with cooling tower condenser water supply at ~31–34°C Louisiana summer design day — no low-temperature chilled water required.

**Munters regen slip-stream.** 5.5 MW exhaust heat at Stage 1 (T-12), 11.0 MW at Full Build (T-13). Deducted from genset exhaust enthalpy available for other use — in the current architecture this is the sole CHP heat recovery path.

**Open items:** T-05 (tower type), T-08 (~72.9 MW rejection duty confirmation), T-09 (makeup water at design day).

## G. Water

**Makeup source open.** Candidates: municipal (simplest, most expensive), on-site well, Vermilion River intake (for makeup only — no thermal loop; LPDES covers blowdown return).

**Treatment not scoped.** Cooling tower chemistry, biocide, scale/corrosion inhibition, blowdown — sized after tower type lock.

**Blowdown disposal:** tower sump evaporation, LPDES-permitted Vermilion River discharge, or POTW. Affects LPDES scope.

**Consumption:** seasonal, summer peak substantially higher than winter. Real number pending tower type selection and load confirmation.

## H. Structural / civil

No building has been structurally assessed (gap, per STATE-001). Must be scoped and commissioned before any load placement on B1 or B2.

Civil scope (flood elevation, stormwater, drainage, historic district overlay) at parish level. HTC Part 2 governs interior and envelope modifications — do not commit to specific B1/B2 restoration scope externally.

## I. AI control and automation

**Operating principle:** Autonomous AI dispatch of gensets, pumps, tower fans, BESS, solar. Not a decorative overlay on a manually-operated plant — it is the operating model.

**AMCL control architecture (A-09, Working):** Five-tier stack.

- **L0 field devices.** Cat ECS governors, generator protection IEDs, VFDs on all thermal auxiliaries, Jetson AGX Orin cassette BMS with 148 sensor channels, RTDs, CTs/PTs, protection relaying on LV and DC sides.
- **L1 block controller (PLC).** Genset paralleling, UFLS, BESS inverter setpoints, MPPT coordination, protection trip schemes, safety interlocks, deterministic and local — cannot be overridden from higher tiers.
- **L2 plant SCADA / data layer.** Historian, alarming, OPC-UA backbone, cassette BMS aggregation (148 channels × 44 cassettes = ~6,500 cassette points plus facility points).
- **L3 AMCL dispatch (AI).** Cross-block optimization against IT load, thermal profile, BESS state, solar production, gas supply. Runs the 55–75% genset loading envelope. Orchestrates BESS across frequency support, thermal shifting, solar recapture, planned shutdown. Does not override protection.
- **L4 HMI + operator override + cybersecurity.** IEC 62443 segmentation. OT plane isolation from IT plane (colocation customers). Human-in-loop policy gates, incident response, admin plane hardening, supply chain integrity for control equipment and model weights.

**AI failure modes:** Last-known-good deterministic control. Gensets hold setpoint, BESS inverters hold mode, VFDs hold speed. Governors and protection autonomous. Operations takes manual dispatch until AI restored.

**Cybersecurity framework selection (A-07) open.** NIST CSF and IEC 62443 are baseline candidates.

## J. Fire and life safety

- **Cassette level:** Novec 1230 + VESDA + NFPA 2001 (C-05, locked)
- **Compute hall:** facility-level suppression independent of cassette; pre-action or clean agent candidates
- **Genset hall / rear slab:** CH4 detection, genset-specific suppression, vent/purge for gas leak response
- **BESS yard:** thermal runaway detection, fire-water demand, setback distances per NFPA 855; integrated with rear slab layout
- **Office / NOC:** standard commercial occupancy, integrated with historic envelope
- **Egress:** historic buildings may require code modernization for occupancy — scope flows from SHPO Part 2

## K. Operations

- **Staffing:** external messaging stays vague. Internal working assumption 40–70 permanent ops at Full Build; numbers do not appear externally.
- **Redundancy:** 44 gensets in 11 blocks with N+1 at block; BESS sized for single-genset trip, block loss, graceful gas-loss shutdown; towers sized for full cassette secondary cooling load with no solar credit; no external utility dependency.
- **Gas supply (open):** pipeline interconnect, metering, contingency storage. Block 1 energization gated on locked gas supply.
- **Maintenance philosophy (open):** AI changes model — predictive from sensor data, reduced preventive cadence, planned outages coordinated with dispatch.

## L. Commercial

Single revenue stream: colocation capacity (P-09). Sell-back to LUS retained as future optionality (P-10). No "zero evaporative" water-conservation marketing (implies lower opex than real).

**Capex categories:** cassettes (IP core), site and buildings (historic restoration + compute halls + slab + yard), generation and electrical (gensets, BESS, solar, transformers, switchgear), thermal (cooling towers, pumps, piping), controls (SCADA, BMS, AI), permitting and soft.

**Opex:** gas, water, maintenance, staffing, insurance, permits, capital reserves.

**Incentives:** HTC 45% + ITEP (before construction) + Parish PILOT + LED. HB 827 excluded.

**External capital:** no representations about committed capital in BOD-001 or any external doc.

## M. Schedule and dependencies

**C1 (must happen, critical path):**

- NVIDIA allocation (gates Stage 1 GPU count)
- Cat CSA validation: CG260-16 governor + voltage option (E-5, E-6)
- Tower field sizing: ~72.9 MW rejection duty confirmation (T-08, T-09)
- SHPO Part 1 filing (before any activity triggering historic review)
- LDEQ LPDES pre-application (before thermal/water design lock)
- LDEQ Title V pre-application (before air emissions design lock)
- LA ITEP filing (before any construction)
- Gas supply lock (before Block 1 energization)

**C2 (desirable, not blocking):** Structural assessments B1–B4; Parish PILOT negotiation.

**C3 (optional):** LUS Pinhook (at their cost/schedule); TVFWD informational.

## N. External dependencies and stakeholders

- **State:** LED (Secretary Bourgeois, Governor Landry's office), SHPO (HTC), LDEQ (water + air), LA Commerce (ITEP)
- **Federal:** Federal HTC via SHPO, EPA Region 6 via LDEQ, Army Corps if in-river work beyond LDEQ scope
- **Parish:** zoning, building permits, flood elevation, stormwater, PILOT, local historic overlay
- **Utility:** LUS (optional Pinhook future); gas utility (must lock before Block 1)
- **Vendors (categories, status):** gensets O (Cat CSA pending); BESS O (shortlist: Fluence, LG Energy Solution Vertech, Saft, Hitachi AMPS); cooling towers O (SPX/Marley, BAC, Evapco, Brentwood); transformers/switchgear/SCR O; AI/SCADA/BMS O

---

## Glossary (non-obvious terms only)

- **7Q10 flow** — minimum seven-consecutive-day average flow with a 10-year recurrence interval
- **AMCL** — AI Mission Control Layer (facility control architecture)
- **BESS** — Battery Energy Storage System
- **BOD** — Basis of Design
- **BTM** — Behind-the-Meter
- **CDU** — Coolant Distribution Unit
- **CHP** — Combined Heat and Power
- **CSA** — Cat Customer Support Agreement
- **HTC** — Historic Tax Credit (Federal 20% + LA 25%)
- **ITEP** — Industrial Tax Exemption Program (Louisiana)
- **LDEQ / LED / LPDES** — LA Dept of Environmental Quality / LA Economic Development / LA Pollutant Discharge Elimination System
- **NVL72** — NVIDIA rack-scale GPU reference architecture
- **PCS** — Power Conditioning System (Hitachi AMPS) or Power Capacitance Shelf (Delta) — context-dependent
- **PILOT** — Payment In Lieu Of Taxes (parish-level industrial incentive)
- **SHPO** — State Historic Preservation Office
- **SSCB** — Solid-State Circuit Breaker
- **TVFWD** — Teche-Vermilion Fresh Water District
- **UFLS** — Under-Frequency Load Shedding

---

## Document control

**Revision plan:**

- **Rev 0.6 (current)** — cassette architecture updated to Rev 1.3 (AC-in, 9 compute racks, 5 Delta in-row inside Cassette); IT/GPU numbers cascaded; CDU updated; BESS/solar re-coupled; river references removed; transformer protection corrected
- **Rev 0.7** — after Cat CSA validation; updates E-05, E-06, E-08
- **Rev 0.8** — after tower field siting study and sizing confirmation; updates T-05, T-08, T-09
- **Rev 0.9** — after LDEQ LPDES pre-application; updates B-section and G-section
- **Rev 1.0** — when all C1 external dependencies are locked; ready for circulation

**Revision log:**

- **Rev 0.1 (2026-04-16 AM):** Initial release. Established Decision Ledger, Sections A–N, Glossary.
- **Rev 0.2 (2026-04-16 PM):** Cassette §C rewritten. C-08 through C-25 added. Fire, CDU, dehumidification, BMS, network, PDUs, hot-swap, IT load locked. Stage 1 IT 101.2 MW. Full Build 202.4 MW.
- **Rev 0.3 (2026-04-17):** Electrical architecture corrected — replicated Marlie block, DC-coupled BESS and solar, 800 VDC bus per block, in-row power racks. E-07, E-08, E-09, E-11, E-17 updated. E-20 through E-23 added.
- **Rev 0.4 (2026-04-17):** Ledger extended with E-24 through E-30 and A-09. Delta vendor anchored. Protection details added.
- **Rev 0.5 (2026-04-22):** Absorption chiller eliminated. CHP exhaust to Munters only. Cooling towers promoted to primary rejection. T-01 rewritten; T-02, T-03, T-11 removed; T-04, T-08, T-09 updated. Section F rewritten. Chiller references removed campus-wide.
- **Rev 0.6 (2026-04-23):** Cassette architecture updated to Rev 1.3. AC-in (480 VAC primary). Five Delta 660 kW in-row racks inside Cassette (R11–R15). 9 compute racks per cassette. IT load 2,300 → 2,070 kW/cassette. Stage 1 IT 91.1 MW, Full Build 182.2 MW. GPU targets revised. CDU Boyd → CoolIT CHx2000 external. BESS and solar re-coupled to block 480 VAC bus. Block-level 800 VDC common bus eliminated. E-27 transformer protection corrected to 87T overall differential. Vermilion River supplemental removed (T-06 removed, §F paragraph removed, R-03 updated, §D updated). Secondary cooling per cassette 1,840 → ~1,656 kW; Stage 1 rejection ~72.9 MW.

**BOD-001 is cited by:** Trap-ELEC-001, ST-TRAP-ARCHDIAG-001, ST-TRAP-THERMAL-BASIS, ST-TRAP-COOLING-TOWER-001, ST-TRAP-BESS-001, ST-TRAP-SOLAR-001, ST-TRAP-SCADA-001, ST-TRAP-SLD-001, ST-TRAP-PROT-001, Pod Swarm financial model (Trappey's inputs).

---

**End of ST-TRAP-BOD-001 Rev 0.6.**
