# ST-TRAP-BOD-001 — Basis of Design — Rev 0.4

**Document:** Basis of Design, Trappey's AI Center
**Project:** Trappey's AI Center — 22-acre historic cannery site, Lafayette, Louisiana
**Revision:** 0.4 — ledger extended with decisions from the electrical architectural diagram package
**Date:** April 17, 2026
**Owner:** Scott Tomsu
**Status:** Working draft — canonical source of design parameters for all downstream documents

## Rev 0.4 change summary

Ledger expanded with eight new Working entries captured during ST-TRAP-ARCHDIAG-001 Rev 0.1 development: primary in-row rack vendor (E-24), rack count per cassette (E-25), per-genset protection relay set (E-26), transformer protection (E-27), LV secondary grounding (E-28), 480 VAC feeder categorization (E-29), cassette internal topology below the umbilical (E-30), and the five-tier AMCL control architecture (A-09). Prior sections A–N retained as authoritative rationale; Rev 0.3 change summary moved to the revision log.

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
| P-03 | Stage 1 IT load | 101.2 MW (44 × 2,300 kW) | L | 2026-04-16 |
| P-04 | Stage 1 cassette count | 44 | L | 2026-04-14 |
| P-05 | Full Build IT load | 202.4 MW (88 × 2,300 kW) | L | 2026-04-16 |
| P-06 | Full Build cassette count | 88 | L | 2026-04-14 |
| P-07 | GPU target Stage 1 | 31,680 NVIDIA Vera Rubin (44 × 720) | W | 2026-04-16 |
| P-08 | GPU target Full Build | 63,360 (88 × 720) | W | 2026-04-16 |
| P-09 | Revenue model | Colocation only, base case | L | 2026-04-16 |
| P-10 | Sell-back to LUS | Excluded from base case; future optionality only | L | 2026-04-16 |

### Regulatory and incentive

| # | Parameter | Value | Status |
|---|---|---|---|
| R-01 | LDEQ thermal rise limit | 2.8°C (5°F) above ambient after mixing | L |
| R-02 | LDEQ absolute max water temp | 32.2°C (90°F); no additional heat above | L |
| R-03 | LPDES permit required | Yes — cooling tower blowdown + river loop | L |
| R-04 | Title V air permit | Yes — 44 gensets at CG260-16 scale triggers | W |
| R-05 | SHPO Part 1 | Prepared, not yet filed | O |
| R-06 | SHPO Part 2 | Scope TBD within HTC constraints | O |
| R-07 | HTC stack | 45% (Federal 20% + LA 25%) | L |
| R-08 | LA ITEP | To be filed before any construction | W |
| R-09 | Parish PILOT | Pursued in place of HB 827 (below $200M threshold) | L |
| R-10 | LA corporate tax rate (financial model) | 5.5% | L |

### Cassette platform (product IP) — per eng-pack-5MW Rev 3.1 §15

| # | Parameter | Value | Status |
|---|---|---|---|
| C-01 | Cassette architecture | Locked as IP core; vendor-neutral outside | L |
| C-02 | Cassette internal DC bus | 800 VDC overhead busbar | L |
| C-03 | CDU | Boyd 2,000 kW water-glycol, N+1 pumps | L |
| C-04 | CDU supply temperature | ≤45°C to rack | L |
| C-05 | Fire suppression | Novec 1230 + VESDA, NFPA 2001 | L |
| C-06 | Cassette BMS | NVIDIA Jetson AGX Orin, 148 sensor channels | L |
| C-07 | Container width constraint | 93" internal; 40 ft HC ISO external | L |
| C-08 | Enclosure | 40 ft HC ISO, NEMA 3R | L |
| C-09 | External dimensions | 40' × 8' × 9.5' | L |
| C-10 | GPU platform | NVIDIA Vera Rubin NVL72 | L |
| C-11 | Rack count per cassette | 10 × OCP ORV3 | L |
| C-12 | GPUs per rack | 72 (NVL72 tray) | L |
| C-13 | HBM4 memory | 288 GB/GPU, 20.7 TB/rack, 207 TB/cassette | L |
| C-14 | IT load per rack | 230 kW | L |
| C-15 | IT load per cassette | 2,300 kW | L |
| C-16 | Facility load per cassette | 2,415 kW | L |
| C-17 | Secondary cooling demand | 1,840 kW per cassette to site heat rejection | L |
| C-18 | Internal power distribution | 3 × Eaton ORV3 + NVIDIA Kyber PDUs | L |
| C-19 | Dehumidification | Munters HCD/MCD, exhaust-heat regen, ≤50% RH | L |
| C-20 | Munters regen heat draw | ~125 kW per cassette (exhaust slip-stream) | L |
| C-21 | Network | NVIDIA QM9700 InfiniBand | L |
| C-22 | Hot-swap disconnects | Staubli | L |
| C-23 | Cassette-level PUE | ≤1.05 | L |
| C-24 | External connections (single panel) | 800 VDC umbilical, CHW supply/return, fiber, BMS, exhaust regen | L |
| C-25 | Immersion fluid vendor (future rev) | Dual-track: GRC vs Submer | O |

### Electrical architecture

| # | Parameter | Value | Status |
|---|---|---|---|
| E-01 | Operating mode | Behind-the-meter permanent island, day one | L |
| E-02 | LUS Pinhook interconnect | Optional future feature at LUS cost/schedule | L |
| E-03 | Prime mover | Cat CG260-16 gas genset | L |
| E-04 | Genset count | 44 (11 blocks × 4) | L |
| E-05 | Nominal loading per genset | 61.5% (AI-varied in operation) | W |
| E-06 | Genset MV voltage | 13.8 kV working | W |
| E-07 | Campus electrical topology | Replicated Marlie-pattern blocks; 800 VDC bus per block; no MV ring | L |
| E-08 | Block step-down | Per-block MV→LV transformer (13.8 kV → 480 V, ~15 MVA) | W |
| E-09 | Cassette-side rectification | 800 VDC in-row power racks at cassette | L |
| E-10 | BESS size | 40 MWh working; 30–50 MWh envelope | W |
| E-11 | BESS coupling | DC-coupled to 800 VDC bus via bidirectional DC-DC | L |
| E-12 | BESS converter | Bidirectional DC-DC on 800 VDC bus; sub-second transient response | L |
| E-13 | BESS chemistry | LiFePO4 (Eaton xStorage working spec) | W |
| E-14 | Solar array | First Solar Series 7 rooftop | L |
| E-15 | Solar DC bus voltage | 1500 VDC string | L |
| E-16 | Solar capacity | 2.05 MW | L |
| E-17 | Solar coupling | DC-coupled: 1500 VDC → buck → 800 VDC bus | L |
| E-18 | Protection philosophy | Island-only; DC-dominated (SSCB + blocking diodes); no anti-islanding | L |
| E-19 | UFLS stages | Three: 59.5 / 59.2 / 58.9 Hz at block MV inlet | L |
| E-20 | In-row rack integrated storage | BBU + supercap sized for sub-100 ms GPU swings | L |
| E-21 | 800 VDC connector interface | Touch-safe mechanical interlock, EV-heritage per NVIDIA MGX | L |
| E-22 | Block-internal 800 VDC busway | Copper busway, scalable | W |
| E-23 | Inter-block tie (N+1 posture) | Open: 11 independent vs tied at aux point | O |
| **E-24** | **Primary in-row rack vendor** | **Delta 660 kW In-Row Power Rack — scored 4.75/5 vs Eaton 3.80, Schneider 3.15; procurement-ready today** | **W** |
| **E-25** | **In-row rack count per cassette** | **4 base (2,640 kW, 9.3% headroom) or 5 for rack-level N+1 (36.6% headroom)** | **W** |
| **E-26** | **Generator protection relay set** | **Per genset: 87G differential, 32 reverse power, 40 loss of excitation, 46 negative sequence, 47 phase sequence, 59/27 over/under-voltage, 64G stator ground, 78 out-of-step. Block bus: 87B differential.** | **W** |
| **E-27** | **Transformer protection** | **87T primary + secondary differential, 49T thermal (RTD), 63 pressure/gas (cast-resin equivalent)** | **W** |
| **E-28** | **LV secondary grounding** | **Solidly grounded wye at 480 VAC main with 50G residual ground sensing and LSIG trip unit on main** | **W** |
| **E-29** | **480 VAC feeder categorization** | **16× in-row racks (~10.6 MVA) + cooling MCC (~600 kW, VFD-driven) + BESS aux (~80 kW) + solar buck aux (~10 kW) + facility ancillary (~200 kW, SCADA/NOC/life safety)** | **W** |
| **E-30** | **Cassette internal electrical topology** | **800 VDC overhead busbar → main DC distribution (3× Eaton ORV3 + Kyber PDUs to 10 × ORV3 racks) + auxiliary DC-DC (Boyd CDU pumps, Munters blowers, Jetson Orin BMS)** | **L** |

### Thermal architecture

| # | Parameter | Value | Status |
|---|---|---|---|
| T-01 | Architecture | CHP cascade: genset waste heat → LiBr absorption chiller → process loop; cooling towers for residual | L |
| T-02 | Absorption chiller type | LiBr (lithium bromide) | L |
| T-03 | Chiller drive source | Options B or C (double-effect or multi-energy). Option A single-stage effectively eliminated — THERMAL-BASIS Rev 0.4 §6.5 shows only +1.4% margin at conservative supply (1.05 ratio); insufficient to design around. Decision between B and C deferred to chiller RFQ (TB-5). | W |
| T-04 | Primary cold sink | Evaporative cooling towers (residual rejection) | L |
| T-05 | Cooling tower type | TBD (wet vs hybrid vs adiabatic) | O |
| T-06 | Supplemental cold sink | Vermilion River, conditional | L |
| T-07 | Water tower (historic) | Deferred — no load-bearing role | L |
| T-08 | Stage 1 condenser rejection to towers | Pending CHP heat balance | O |
| T-09 | Tower makeup water (Stage 1 peak) | Pending CHP heat balance | O |
| T-10 | Cassette cooling fluid | Direct-to-chip water-glycol | W |
| T-11 | Cassette CHW compatibility | Chiller 7–12°C output vs Boyd CDU requirement | O |
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
| A-03 | Thermal dispatch | AI-controlled pumps, chillers, tower fans, VFD-driven | L |
| A-04 | BESS dispatch | AI-orchestrated frequency support, thermal shifting, solar recapture | L |
| A-05 | AI model / vendor | Open — scope not defined | O |
| A-06 | Human-in-loop policy | Open — to be defined | O |
| A-07 | Cybersecurity framework | Open — NIST CSF / IEC 62443 candidates | O |
| A-08 | Staffing | "Substantial" construction, "high-wage technical" operations (no specific numbers external) | L |
| **A-09** | **AMCL control architecture** | **Five-tier: L0 field devices (governors, IEDs, VFDs, Jetson Orin) · L1 block PLC (paralleling, UFLS, DC-DC setpoints) · L2 plant SCADA (historian, OPC-UA) · L3 AMCL AI dispatch · L4 HMI + operator override + IEC 62443 cybersecurity** | **W** |

### Naming and communication

| # | Parameter | Value | Status |
|---|---|---|---|
| N-01 | Project / company name in external docs | "Scott Tomsu" | L |
| N-02 | "Pinhook" spelling | One word | L |
| N-03 | FM Bank / Farmers Merchants Bank / Mark Sibley | Excluded from all project materials | L |

---

## A. Project identity and scope

22-acre Trappey's Cannery historic site on the Vermilion River. Adaptive reuse of twelve nationally registered historic structures. Four principal buildings (B1–B4) under active engineering. Supporting infrastructure on rear 42,000 sq ft slab and 28,000 sq ft infrastructure yard.

**Staging:** Stage 1 at 101.2 MW IT (44 cassettes × 2,300 kW, 31,680 GPU target); Full Build at 202.4 MW IT (88 cassettes, 63,360 GPU target). Per-cassette facility load 2,415 kW. Stage 1 cassette total: 106.3 MW. NVIDIA allocation is the gating variable and remains Open.

**Out of scope:** LUS sell-back revenue (base case), water tower as load-bearing element, residential repositioning, grid-parallel in any external-boundary sense.

## B. Regulatory framework

- **LDEQ water:** 5°F rise limit, 90°F absolute max, LPDES for cooling tower blowdown and supplemental river discharge
- **LDEQ air:** Title V for 44 gensets; SCR in infrastructure yard for NOx; CO threshold carryover from ADC workstream
- **Historic preservation:** SHPO Part 1 prepared not filed; Part 2 scope TBD; do not claim completion externally
- **Incentives:** HTC 45% + LA ITEP (before construction) + Parish PILOT + LED engagement

## C. Cassette platform (IP core)

The cassette is the product. Everything outside the cassette is vendor-neutral and selected on price, lead time, availability. This framing has permitting and financing consequences.

All cassette values locked per eng-pack-5MW Rev 3.1 §15. Trappey's cassette is identical to the Rev 3.1 cassette; no changes inside the envelope at 44-cassette scale.

**Cassette-to-facility interface (single panel, 5 connections):** 800 VDC umbilical, CHW supply/return, fiber (data + control), BMS sensor aggregation, exhaust regen slip-stream.

**Open items at cassette interface:** Immersion fluid vendor (GRC vs Submer, deferred). CHW temperature compatibility between LiBr chiller (7–12°C) and Boyd CDU — C1 open item (T-11), gates all facility chiller selection.

## D. Load and performance

Stage 1 IT: 101.2 MW (44 × 2,300 kW). Full Build IT: 202.4 MW. Per-cassette total facility: 2,415 kW. Per-rack: 230 kW. Ancillary (NOC, office, lighting, security, non-IT HVAC, controls): working 3–5% of IT load.

Diversity factor working 0.95. AI control may flatten further.

**PUE (honest seasonal envelope):** Winter/shoulder target high-1.0s to low-1.1s with river loop active. Louisiana summer design day 1.2–1.3 with tower field carrying full residual after CHP cascade. Single-number PUE below 1.15 not claimed externally without qualifier.

## E. Electrical architecture

**Behind-the-meter permanent island from day one.** No LUS provisioning day one — spatial allocation only. If LUS engages later, at their cost and schedule.

**Replicated block architecture.** Trappey's = N replicated Marlie-pattern blocks. Each block structurally identical to a 5 MW Marlie block except for the prime mover. 4 × Cat CG260-16 per block paralleled at 13.8 kV, one step-down transformer per block (13.8 kV → 480 V, ~15 MVA), in-row power racks rectify to 800 VDC, single 800 VDC common bus per block carries rack outputs + BESS + solar + 4 cassette umbilicals. 11 independent blocks (base case) — no campus MV ring.

**What's different from Marlie:** CG260-16 generates at 13.8 kV not 480 V; per-block step-down transformer inserted. Everything downstream (in-row racks, 800 VDC bus, BESS/solar coupling, cassette distribution) identical.

**Protection philosophy is DC-dominated.** Island-only. Per-genset relay set per E-26; transformer protection per E-27; block bus 87B; UFLS three-stage at block inlet. DC side: SSCB + blocking diodes at every source tie (rack output, BESS tie, solar tie). Load-break contactors at each cassette umbilical. Cross-domain trip schemes defined in PROT-001.

**In-row power rack selection (E-24, E-25):** Delta 660 kW In-Row Power Rack wins the vendor comparison 4.75/5. 4 racks per cassette is the base spec (2,640 kW, 9.3% headroom); 5 racks preferred for rack-level N+1 (3,300 kW, 36.6% headroom). Per-rack: 6 × 110 kW PSU shelves, 80 kW BBU per shelf (480 kW aggregate BBU), Power Capacitance Shelf with aluminum caps + supercaps for sub-100 ms swings, EVA variant for peak shaping, 98% AC-DC at full load, touch-safe 800 VDC output.

**Single biggest technical risk:** CG260-16 governor response in island-mode 24/7 at variable loading under AI dispatch, with block-level DC-coupled BESS as first-line transient buffer. Cat CSA engagement is the most important external validation. If governor data comes back unfavorable: add 5th genset per block or oversize BESS — both engineerable.

## F. Thermal architecture

**CHP cascade (locked):** Genset waste heat (exhaust + jacket water) drives LiBr absorption chillers. Chillers pre-cool facility process loop. Cooling towers carry residual rejection only.

**Consequences:** Genset operating profile couples with chiller effectiveness. Jacket water temperatures must stay in absorption envelope. AI dispatch respects this constraint alongside electrical dispatch. Single-stage (~0.7 COP, jacket-driven) vs double-stage (~1.2, exhaust-driven) vs cascade decision open per T-03.

**Cooling tower field (primary residual sink, locked).** Type — wet / hybrid / adiabatic — open per T-05. Wet lowest capex, highest water; hybrid cuts summer water 30–50%; adiabatic uses evaporative only at peak but limited by Louisiana wet-bulb. Full dry excluded at this scale. Scott decides after CHP heat balance closes.

**Vermilion River supplemental.** Winter/shoulder 30–60 MW offset achievable. Louisiana summer ≥90°F: 0 MW (regulatory). Annual time-average 20–40% of rejection; effectively 0% peak weeks. Value: real for water conservation, near-zero for thermal reliability.

**Munters regen slip-stream:** 5.5 MW exhaust heat deducted at Stage 1 (T-12), 11.0 MW at Full Build (T-13). Changes arithmetic of absorption chiller sizing — T-08 heat balance not complete until Munters is in the math.

**Cassette CHW compatibility (T-11, C1 open):** LiBr chiller output 7–12°C vs Boyd CDU requirement. Until resolved, downstream chiller selection, CHW piping sizing, and thermal control loop design are gated.

## G. Water

**Makeup source open.** Candidates: municipal (simplest, most expensive), on-site well, Vermilion intake (integrates with supplemental loop). Decision driven by tower type and LPDES pre-application.

**Treatment not scoped.** Cooling tower chemistry, biocide, scale/corrosion inhibition, blowdown — sized after F.2 lock.

**Blowdown disposal:** tower sump evaporation, LPDES-permitted Vermilion discharge, or POTW. Affects LPDES scope.

**Consumption:** seasonal, summer peak substantially higher than winter. Real number pending CHP heat balance and tower type.

## H. Structural / civil

No building has been structurally assessed (gap, per STATE-001). Must be scoped and commissioned before any load placement on B1 or B2.

Civil scope (flood elevation, stormwater, drainage, historic district overlay) at parish level. HTC Part 2 governs interior and envelope modifications — do not commit to specific B1/B2 restoration scope externally.

## I. AI control and automation

**Operating principle:** Autonomous AI dispatch of gensets, chillers, pumps, tower fans, BESS, solar. Not a decorative overlay on a manually-operated plant — it is the operating model.

**AMCL control architecture (A-09, Working):** Five-tier stack.

- **L0 field devices.** Cat ECS governors, generator protection IEDs, VFDs on all thermal auxiliaries, Jetson AGX Orin cassette BMS with 148 sensor channels, RTDs, CTs/PTs, protection relaying on LV and DC sides.
- **L1 block controller (PLC).** Genset paralleling, UFLS, DC-DC converter setpoints (BESS + solar buck), MPPT coordination, protection trip schemes, safety interlocks, deterministic and local — cannot be overridden from higher tiers.
- **L2 plant SCADA / data layer.** Historian, alarming, OPC-UA backbone, cassette BMS aggregation (148 channels × 44 cassettes = ~6,500 cassette points plus facility points).
- **L3 AMCL dispatch (AI).** Cross-block optimization against IT load, thermal profile, BESS state, solar production, gas supply. Runs the 55–75% genset loading envelope. Orchestrates BESS across frequency support, thermal shifting, solar recapture, planned shutdown. Does not override protection.
- **L4 HMI + operator override + cybersecurity.** IEC 62443 segmentation. OT plane isolation from IT plane (colocation customers). Human-in-loop policy gates, incident response, admin plane hardening, supply chain integrity for control equipment and model weights.

**AI failure modes:** Last-known-good deterministic control. Gensets hold setpoint, BESS DC-DC converters hold mode, VFDs hold speed. Governors and protection autonomous. Operations takes manual dispatch until AI restored.

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
- **Redundancy:** 44 gensets in 11 blocks with N+1 at block; BESS sized for single-genset trip, block loss, graceful gas-loss shutdown; towers sized for full residual with no river or solar credit; no external utility dependency.
- **Gas supply (open):** pipeline interconnect, metering, contingency storage. Block 1 energization gated on locked gas supply.
- **Maintenance philosophy (open):** AI changes model — predictive from sensor data, reduced preventive cadence, planned outages coordinated with dispatch.

## L. Commercial

Single revenue stream: colocation capacity (P-09). Sell-back to LUS retained as future optionality (P-10). No "zero evaporative" water-conservation marketing (implies lower opex than real).

**Capex categories:** cassettes (IP core), site and buildings (historic restoration + compute halls + slab + yard), generation and electrical (gensets, BESS, solar, transformers, switchgear, rectifiers), thermal (absorption chillers, cooling towers, pumps, piping), controls (SCADA, BMS, AI), permitting and soft.

**Opex:** gas, water, maintenance, staffing, insurance, permits, capital reserves.

**Incentives:** HTC 45% + ITEP (before construction) + Parish PILOT + LED. HB 827 excluded.

**External capital:** no representations about committed capital in BOD-001 or any external doc.

## M. Schedule and dependencies

**C1 (must happen, critical path):**

- NVIDIA allocation (gates Stage 1 GPU count)
- Cat CSA validation: CG260-16 governor + voltage option (E-5, E-6)
- Cassette CHW compatibility: Boyd CDU vs LiBr chiller output (T-11)
- CHP heat balance including Munters slip-stream (T-08, T-12)
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
- **Vendors (categories, status):** gensets O (Cat CSA pending); BESS O (shortlist: Tesla, Fluence, Wärtsilä, Honeywell); cooling towers O (SPX/Marley, BAC, Evapco, Brentwood); absorption chillers O; transformers/switchgear/SCR/rectifiers O; AI/SCADA/BMS O
- **Customer:** NVIDIA allocation conversation + Inception program; LOI template exists (Pod Swarm Phase 0); no signed Trappey's customer LOIs

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
- **PCS** — Power Capacitance Shelf (Delta)
- **PILOT** — Payment In Lieu Of Taxes (parish-level industrial incentive)
- **SHPO** — State Historic Preservation Office
- **SSCB** — Solid-State Circuit Breaker
- **TVFWD** — Teche-Vermilion Fresh Water District
- **UFLS** — Under-Frequency Load Shedding

---

## Document control

**Revision plan:**

- **Rev 0.4 (current)** — E-24 through E-30, A-09 added from ARCHDIAG-001 development
- **Rev 0.5** — after CHP heat balance with Munters slip-stream; updates T-03, T-08, F-section
- **Rev 0.6** — after Cat CSA validation; updates E-05, E-06, E-08
- **Rev 0.7** — after LDEQ LPDES pre-application; updates B-section and G-section
- **Rev 0.8** — after SHPO Part 1 filing; updates R-05 and HTC constraints
- **Rev 1.0** — when all C1 external dependencies are locked; ready for circulation

**Revision log:**

- **Rev 0.1 (2026-04-16 AM):** Initial release. Established Decision Ledger, Sections A–N, Glossary.
- **Rev 0.2 (2026-04-16 PM):** Cassette §C rewritten against eng-pack-5MW Rev 3.1 §15. C-08 through C-25 added. Fire suppression locked (Novec 1230 + VESDA + NFPA 2001). CDU locked Boyd 2,000 kW. Dehumidification locked Munters. BMS locked Jetson AGX Orin. Network locked QM9700. PDUs locked 3× Eaton ORV3 + Kyber. Hot-swap Staubli. IT load 2,300 kW exact. Stage 1 IT 101.2 MW. Full Build 202.4 MW. §F.5 Munters regen added.
- **Rev 0.3 (2026-04-17):** Electrical architecture corrected — replicated Marlie block, DC-coupled BESS and solar, 800 VDC bus per block, in-row power racks. E-07, E-08, E-09, E-11, E-17 updated. E-20 through E-23 added. Rev 0.2 MV-ring architecture removed in entirety.
- **Rev 0.4 (2026-04-17):** Ledger extended with E-24 through E-30 (in-row rack vendor and count, generator and transformer protection, LV grounding, feeder categories, cassette internal topology) and A-09 (five-tier AMCL). Refinements originated in ST-TRAP-ARCHDIAG-001 Rev 0.1.

**BOD-001 is cited by:** ST-TRAP-ELEC-001 Rev 1.2, ST-TRAP-ARCHDIAG-001 Rev 0.1, ST-TRAP-THERMAL-BASIS (pending), ST-TRAP-STATE-001 Rev 1.2, ST-TRAP-RIVER-001, ST-TRAP-COOLING-TOWER-001, ST-TRAP-BESS-001, ST-TRAP-SOLAR-001, ST-TRAP-SCADA-001 / ST-TRAP-AICTRL-001, ST-TRAP-SLD-001, ST-TRAP-PROT-001, Pod Swarm financial model (Trappey's inputs).

---

**End of ST-TRAP-BOD-001 Rev 0.4.**
