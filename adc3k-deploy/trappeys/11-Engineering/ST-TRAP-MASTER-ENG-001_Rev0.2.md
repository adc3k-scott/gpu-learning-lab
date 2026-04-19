# ST-TRAP-MASTER-ENG-001 — Master Engineering Package — Rev 0.2

**Document:** Master Engineering Package — Trappey's AI Center
**Project:** Trappey's AI Center — 22-acre historic cannery site, Vermilion River, Lafayette, Louisiana
**Revision:** 0.2 — thermal load census correction; architecture pivot to Option A (dump)
**Date:** 2026-04-18
**Owner:** Scott Tomsu
**Status:** Working draft — internal use only
**Authority:** BOD-001 Rev 0.4 governs all locked values. This document consolidates the current state of downstream engineering documents; all value changes flow through BOD-001. Rev 0.2 changes flagged here trigger BOD-001 Rev 0.5.

L = Locked · W = Working · O = Open

---

## Rev 0.2 Changelog

Rev 0.1 → Rev 0.2 changes, all sourced from thermal load census (this document §6.8) and cross-system arithmetic verification:

1. **Thermal — absorption chiller load corrected (§6, §7, §8).** Rev 0.1 stated 107.3 MW absorption load (= IT + facility aux). This double-counted the 80.96 MW Boyd CDU GPU warm-water heat that is rejected via a separate adiabatic dry cooler. Census-corrected working value: **33 MW absorption load**. All downstream tower / water / capex numbers revised proportionally (tower duty 241 MW → 57 MW; water 2,476 GPM → 750 GPM; footprint 20,000 sq ft → 6,100 sq ft).
2. **Thermal — architecture pivoted to Option A (§6.2).** With 33 MW absorption load, CHP cascade has ~77 MW of orphaned drive heat. Working basis is now **Option A: minimum absorption sized for actual load + exhaust bypass + JW radiator for remainder**. Option B (absorb everything, eliminate dry cooler) and Option C (two absorption systems) retained as contingencies gating on CHP utilization incentive eligibility.
3. **Electrical — N-1 philosophy clarified (§3.2, §3.7).** At N-1, surviving 3 gensets carry 80.5% vs stated 55–75% dispatch envelope. Added "N-1 contingency envelope" spec of 55–85% to bracket the transient; flagged as confirmation item for Cat CSA.
4. **Electrical — CO emissions major-source flag added (§3.2, §9.1).** Title V major source designation nearly certain without CO oxidation catalyst. New C1 item E-31 "CO control strategy" added.
5. **Electrical — in-row rack loading flagged (§3.1, §3.3).** 16 racks/block = 91.5% steady-state loading on Delta 660 kW units. E-24/E-25 RFQ scope expanded to specify 5 racks/cassette (73% loading) as preferred, with 4 as fallback.
6. **Electrical — fuel rate label corrected (§3.2).** "2,200 Nm³/hr per block full load" was actually at 61.5% anchor. Full load = ~3,660 Nm³/hr/block; ~40,300 Nm³/hr campus. Gas supply Step 17 revised to contract firm pipeline capacity for full-load contingency.
7. **Electrical — block DC busway ampacity clarified (§3.1).** 12,075 A was cassette-only. Peak with simultaneous BESS injection 14,500–17,000 A. Busway specification updated.
8. **Electrical — transformer protection clarification (§3.4).** `87T primary + 87T secondary` replaced with single `87T overall differential` — standard protection practice for a two-winding transformer.
9. **Solar — Voc temp coefficient cited explicitly (§5.1, §5.2).** Updated cold-limit analysis to Louisiana record low (−12°C, 1989) with Voc coef −0.28%/°C. Margin still comfortable.
10. **Siting — SITING-001 elevated to C1 (§9.1).** Rear slab 42,000 sq ft and infrastructure yard 28,000 sq ft both undersized against standard packing. Revised 33 MW thermal load significantly relaxes the yard constraint; rear slab constraint remains.
11. **Water — WATER-SRC and BLOWDOWN elevated to C1 (§9.1).** 33 MW cooling reduces annual makeup to ~395 MG/year, which brings municipal supply back into viability. Permit pathway still material.

---

## 1. Executive Summary

Trappey's AI Center is a **101.2 MW IT load AI compute facility** on a 22-acre historic cannery site on the Vermilion River in Lafayette, Louisiana. The site hosts 12 nationally registered historic structures. Four principal buildings (B1–B4) are under active engineering; supporting infrastructure sits on a 42,000 sq ft rear slab and 28,000 sq ft infrastructure yard.

The facility is a **behind-the-meter permanent electrical island from day one** — no utility grid import or export in base-case operation, no LUS interconnect provisioning. Power is generated on-site by 44 × Cat CG260-16 natural gas gensets (4,000 ekW each) organized into 11 electrically independent blocks, each with a per-block 13.8 kV → 480 VAC step-down transformer feeding Delta 660 kW in-row power racks that rectify to a single 800 VDC common busway per block. BESS (LFP, DC-coupled) and solar (First Solar Series 7 CdTe, DC-coupled via buck) attach to the same 800 VDC bus. No AC anywhere downstream of the in-row racks. No anti-islanding. No sell-back to LUS modeled.

**Stage 1 / Full Build:**

| Parameter | Stage 1 | Full Build | Status |
|---|---|---|---|
| IT load | 101.2 MW | 202.4 MW | L |
| Cassettes | 44 | 88 | L |
| Gensets (Cat CG260-16) | 44 | 88 | L |
| Blocks | 11 | 22 | L |
| GPUs (NVIDIA Vera Rubin, 720/cassette) | 31,680 | 63,360 | W |
| Per-cassette IT | 2,300 kW | 2,300 kW | L |
| Per-cassette facility | 2,415 kW | 2,415 kW | L |

![Figure 1 — Stage 1 energy flow, Option A, 61.5% anchor](diagrams/fig1_energy_sankey.svg)

**Thermal architecture** is a CHP cascade sized for **33 MW absorption cooling load** (census-corrected from Rev 0.1's 107 MW double-count — see §6.8). Genset exhaust drives Broad BH double-effect LiBr absorption chiller for chilled-water facility loads (Munters process air post-desiccant, NOC, offices, cassette air-side heat, electrical room HVAC). Munters HCD/MCD desiccant dehumidification per cassette draws 125 kW exhaust slip-stream (5.5 MW Stage 1, Locked T-12). **Working basis is Option A — minimum absorption sized for actual load; exhaust bypass + JW radiator reject the ~77 MW of orphaned waste heat.** Options B (absorb everything, eliminate dry cooler) and C (two-chiller) retained as contingencies gating on CHP incentive eligibility. Vermilion River remains eliminated as heat sink. Boyd CDU GPU warm water is an isolated loop rejecting to a separate adiabatic dry cooler (~81 MW).

**Why this approach:** BTM permanent island removes the primary reliability dependency on LUS and eliminates interconnect schedule risk. 11-block replicated Marlie-pattern architecture contains blast radius to one block and enables phased construction with standardized procurement. CHP cascade eliminates the mechanical-chiller plant for facility cooling (absorption driven by genset waste heat), and Boyd CDU handles GPU heat on a dedicated dry-cooler loop. DC-coupled BESS + DC-coupled solar + DC rectification on one 800 VDC bus per block matches OCP Stage 1d / NVIDIA DSX reference architecture. Zero utility dependency is the thesis.

---

## 2. Site & Project Basis

Source: BOD-001 Rev 0.4.

![Figure 4 — Site layout, 22-acre Trappey's cannery (SITING-001 C1 gate)](diagrams/fig4_site_layout.svg)

### 2.1 Locked project-level parameters

| # | Parameter | Value | Status |
|---|---|---|---|
| P-01 | Site | 22-acre Trappey's Cannery, Vermilion River, Lafayette, LA | L |
| P-02 | Historic structures | 12 nationally registered | L |
| P-03 | Stage 1 IT load | 101.2 MW (44 × 2,300 kW) | L |
| P-04 | Stage 1 cassette count | 44 | L |
| P-05 | Full Build IT load | 202.4 MW (88 × 2,300 kW) | L |
| P-06 | Full Build cassette count | 88 | L |
| P-07 | GPU target Stage 1 | 31,680 NVIDIA Vera Rubin | W |
| P-09 | Revenue model | Colocation only, base case | L |
| P-10 | Sell-back to LUS | Excluded from base case; future optionality only | L |
| E-01 | Operating mode | Behind-the-meter permanent island, day one | L |
| E-07 | Campus electrical topology | Replicated Marlie-pattern blocks; 800 VDC bus per block; no MV ring | L |
| B-01/B-02 | Building 1/2 role | Historic restoration — NOC / partner hub / rooftop solar | L |
| B-03 | Building 3 role | Compute hall — 20 cassettes | L |
| B-04 | Building 4 role | Compute hall — 24 cassettes | L |
| B-05 | Rear slab | 42,000 sq ft — genset installation + BESS | L |
| B-06 | Infrastructure yard | 28,000 sq ft — cooling and SCR | L |

### 2.2 Decision Ledger — domain status summary

Per BOD-001 §E–N. L = Locked, W = Working, O = Open. Total entries per domain and the representative open items gating each.

| Domain | Locked | Working | Open | Representative open item |
|---|---|---|---|---|
| **P — Project-level** | 9 | 1 | 0 | — |
| **R — Regulatory / incentive** | 6 | 2 | 2 | R-05 / R-06 SHPO Parts 1 & 2 |
| **C — Cassette platform** | 24 | 0 | 1 | C-25 Immersion fluid vendor (deferred) |
| **E — Electrical** | 10 | 13 | 1 | E-23 Inter-block tie topology |
| **T — Thermal** | 7 | 2 | 4 | T-03 Chiller type B/C; T-05 tower type; T-08 heat balance; T-11 Boyd CDU CHW compat |
| **B — Structural / buildings** | 6 | 0 | 1 | B-07 Structural assessments not commissioned |
| **A — Operations & AI control** | 5 | 1 | 3 | A-05 AI model; A-06 Human-in-loop; A-07 Cybersecurity framework |
| **S — Solar (E-14 through E-17)** | 4 | 0 | 0 | (E-22 DC-DC buck RFQ tracked under E) |
| **N — Naming / communication** | 3 | 0 | 0 | — |

Domain shorthand in BOD-001: P project, R regulatory, C cassette, E electrical, T thermal, B buildings, A AI/ops, N naming. The S domain is covered inside E (E-14 solar array L, E-15 1500 VDC string L, E-16 2.05 MW capacity L, E-17 DC-coupled path L).

---

## 3. Power Architecture

Source: ST-TRAP-ELEC-001 Rev 1.2.

### 3.1 Block structure (one block, top-down)

Each of the 11 Stage 1 blocks is structurally identical to a 5 MW Marlie block except for the prime mover. Within one block:

1. **4 × Cat CG260-16** gas gensets, 4,000 ekW each at 60 Hz / 900 rpm, paralleled on 13.8 kV block MV bus via Cat ECS isochronous sharing. 3-of-4 carry load; 4th is N+1.
2. **Block MV bus** — 13.8 kV arc-resistant switchgear, 87B bus differential, three-stage UFLS (59.5 / 59.2 / 58.9 Hz).
3. **Block step-down transformer** — 13.8 kV Δ → 480Y/277 V, ~15 MVA, Dyn11, dry-type / cast-resin, Z≈6%. One per block; only topological addition vs Marlie (which generates at 480 V directly).
4. **480 VAC main switchboard** — solidly grounded wye secondary, 50G residual ground sensing, LSIG main trip unit.
5. **16 × Delta 660 kW in-row power racks** (4 per cassette base spec) — AC-DC conversion, BBU + PCS, 98% efficiency, touch-safe 800 VDC output. **Steady-state loading 91.5% of rated at 2,415 kW cassette facility draw** — E-24/E-25 RFQ scope expanded (Rev 0.2) to specify 5 racks/cassette (73% loading, full rack N-1 tolerance) as preferred configuration, with 4 as fallback.
6. **Block 800 VDC common busway** — copper. **Cassette-only current ~12,075 A at 9.66 MW cassette draw; peak instantaneous including simultaneous BESS injection (2 MW continuous / 4 MW peak) 14,575–17,075 A. Busway and SSCB ampacity shall be sized to 17,000 A minimum.** Single DC bus per block carries rack outputs + BESS + solar + 4 cassette umbilicals.
7. **4 cassette umbilicals** — load-break contactor + SSCB → 800 VDC cable → Staubli hot-swap disconnect at cassette (~3,000 A at 2,415 kW).

11 electrically independent blocks. No inter-block MV ring. No inter-block 800 VDC tie (E-23 deferred). Shared services (gas header, water plant, NOC, security, AMCL) span the campus but do not carry power between blocks.

![Figure 2 — Single Stage 1 block electrical topology (Rev 0.2)](diagrams/fig2_block_electrical.svg)

### 3.2 Genset specification — Cat CG260-16

| Parameter | Value | Status |
|---|---|---|
| Rated output | 4,000 ekW continuous, 60 Hz, 900 rpm | L |
| Electrical efficiency | 43.8% (LHV, at 100% load — part-load derate pending Cat CSA) | L |
| Thermal efficiency | 42.4% (LHV to 120°C) | L |
| Total efficiency | 86.2% | L |
| Design anchor loading | 61.5% (2,460 ekW per genset) | W — pending Cat CSA |
| AI dispatch envelope (steady-state) | 55–75%; 63–65% expected average | W |
| **N-1 contingency envelope (Rev 0.2)** | **55–85% — surviving 3 gensets per block carry 80.5% during single-genset trip** | W — Cat CSA to confirm acceptable duration |
| MV voltage | 13.8 kV | W — Cat CSA to confirm |
| Fuel — at 61.5% anchor loading | ~2,200 Nm³/hr per block; ~24,000 Nm³/hr Stage 1 campus | W |
| **Fuel — at 100% load contingency (Rev 0.2)** | **~3,660 Nm³/hr per block; ~40,300 Nm³/hr Stage 1 campus** | W — firm pipeline capacity basis |
| Emissions — NOx | <250 mg/Nm³ at 5% O₂ | L |
| **Emissions — CO (Rev 0.2)** | Uncontrolled CO ~500–650 mg/Nm³ typical for CG260; **Title V Major Source threshold (100 tpy) likely exceeded even with 90% oxidation catalyst. CO control strategy required — see E-31.** | W |
| Hydrogen blending | 25% blend capable at same continuous rating | L (future optionality) |

**Prime mover rule:** CG260-16 for Trappey's and 100+ MW deployments; Cat G3520K for Marlie 1 and ≤10 MW platforms. Not substitutable.

### 3.3 Five feeder categories (E-29, per block)

| Feeder | Load | Notes |
|---|---|---|
| 16 × Delta 660 kW in-row power racks | ~10.6 MVA | Dominant feeder — 4 racks × 4 cassettes |
| Cooling plant MCC | ~135 kW | VFD-driven (per-block average; campus cooling MCC ~1,475 kW total under Rev 0.2 — likely centralized — see §8.6) |
| BESS auxiliary | ~80 kW | Battery HVAC, BMS, fire system |
| Solar DC-DC buck auxiliary | ~10 kW | Controls, HVAC |
| Facility ancillary | ~200 kW | SCADA, NOC, site lighting, fire/life safety |

### 3.4 Protection (island-only, DC-dominated)

- **Per-genset (E-26):** 87G differential, 32 reverse power, 40 loss of field, 46 negative sequence, 47 phase sequence, 59/27 over/under-voltage, 64G stator ground, 78 out-of-step, 51V voltage-restrained overcurrent.
- **Block bus:** 87B bus differential, 51N neutral ground.
- **Transformer (E-27):** 87T overall differential, 49T thermal (RTD), 63 pressure/gas, 51 time overcurrent on both primary and secondary, 50/51G ground overcurrent on secondary.
- **LV secondary (E-28):** solidly grounded wye, 52M with LSIG, 50G residual ground sensing.
- **UFLS:** three-stage at block MV inlet — 59.5 / 59.2 / 58.9 Hz.
- **DC side:** SSCB at every source tie (each in-row rack output, BESS tie, solar tie), blocking diodes to prevent reverse flow, load-break contactors at each cassette umbilical.

No anti-islanding. No external sync. No reverse-power coordination with utility.

### 3.5 Cassette internal topology (E-30, Locked)

Staubli hot-swap disconnect → cassette 800 VDC overhead busbar → two branches:
- **Main DC distribution:** 3 × Eaton ORV3 PDUs + NVIDIA Kyber PDUs → 10 × OCP ORV3 racks with NVL72 trays → 720 Vera Rubin GPUs per cassette, 230 kW/rack, 2,300 kW cassette IT.
- **Auxiliary DC-DC:** Boyd CDU pumps (2,000 kW water-glycol primary loop, N+1), Munters HCD/MCD blowers, Jetson AGX Orin BMS (148 sensor channels).

### 3.6 AMCL five-tier control (A-09, Working)

| Tier | Role |
|---|---|
| L0 field devices | Cat ECS governors, protection IEDs, VFDs, Jetson Orin BMS, RTDs, CTs/PTs |
| L1 block PLC | Paralleling, UFLS, DC-DC setpoints (BESS + solar buck), MPPT, trip schemes, safety interlocks. Deterministic; cannot be overridden from higher tiers |
| L2 plant SCADA | Historian, OPC-UA backbone, cassette BMS aggregation (148 × 44 ≈ 6,500 cassette points) |
| L3 AMCL dispatch (AI) | Cross-block optimization, gas/load/thermal coupling, BESS orchestration, solar recapture |
| L4 HMI + operator override | IEC 62443 segmentation, OT/IT isolation, incident response |

**AI failure mode:** last-known-good deterministic control. Gensets hold setpoint, BESS DC-DC holds mode, VFDs hold speed. Governors and protection autonomous. Operators take manual dispatch until AI restored.

### 3.7 Full Build vs Stage 1

| Parameter | Stage 1 (11 blocks) | Full Build (22 blocks) | Status |
|---|---|---|---|
| Cassette IT | 101.2 MW | 202.4 MW | L |
| Cassette facility | 106.3 MW (44 × 2,415 kW) | 212.5 MW | L |
| Generation at 61.5% design anchor | 108.24 MW (9,840 kW/block × 11) | 216.5 MW | W |
| Generation at 63–65% operational | ~110.9–114.4 MW | ~221.8–228.8 MW | W |
| Block cassette facility load | 9.66 MW | 9.66 MW | L |
| Non-cassette ancillary (Rev 0.2 revised) | ~3–4 MW | ~6–8 MW | W |
| **Total Stage 1 site load (Rev 0.2)** | **~109.3–110.3 MW** | — | W |

Rev 0.2 margin update: with cooling MCC reduced from ~4.8 MW to ~1.5 MW (§8.6), total site load drops by ~3.3 MW vs Rev 0.1 figure. 63% genset dispatch (110.9 MW) now closes the site load balance with ~0.6 MW net headroom; 65% dispatch (114.4 MW) provides ~4 MW comfortable operating margin. Design anchor 61.5% is retained for Cat longevity discussions but requires cooling MCC parasitic reduction (which Rev 0.2 delivers) to close.

**N-1 genset contingency (Rev 0.2 added):** At N-1 per block, the 3 surviving gensets carry 9,660 kW / 12,000 kW = 80.5%. This is above the 55–75% steady-state dispatch envelope but within the 55–85% N-1 contingency envelope. Cat CSA to confirm (a) acceptable duration at 80% loading before TBO impact, and (b) governor response envelope during the transient ramp from 61.5% to 80.5%. If Cat CSA returns unfavorable, fallback is 5-genset-per-block architecture (5:4) — capex impact ~$8M Stage 1 (11 × ~$750K per additional genset + aux). Decision gate is Step 1 Cat CSA.

### 3.8 Single biggest technical risk

CG260-16 governor response in island-mode 24/7 at variable loading under AI dispatch, paired with block-level DC-coupled BESS via bidirectional DC-DC converter. Cat CSA engagement is the most important external validation. If governor data returns unfavorable: add 5th genset per block (5:4 instead of 4:4) or oversize BESS. Both engineerable; neither preferred.

---

## 4. BESS Architecture

Source: ST-TRAP-BESS-001 Rev 0.1 + ST-TRAP-BESS-RFQ-001 Rev 0.1.

### 4.1 Role — stabilizer, not backup

BESS is **always active on the 800 VDC bus**, running continuously in charge/discharge under AMCL L1 (deterministic) and L3 (AI) control. Four operating functions, priority order:

1. **Transient buffer** — sub-second response to genset governor lag via SiC bidirectional DC-DC (µs–ms response).
2. **Contingency support** — single-genset trip, partial gas curtailment, full gas-loss graceful shutdown.
3. **Solar clip-recapture** — absorbs First Solar overproduction that would otherwise require MPPT throttling.
4. **Load shifting** — flattens genset loading within 55–75% AI dispatch envelope.

BESS is **not** the primary voltage-forming source on the 800 VDC bus (in-row power rack rectifiers regulate bus voltage). Not a replacement for in-row BBU + PCS (which handles sub-100 ms GPU swings). Two storage layers run in parallel.

### 4.2 Sizing and power rating

| Parameter | Per block | Stage 1 facility (11 blocks) | Full Build (22 blocks) | Status |
|---|---|---|---|---|
| Energy — working midpoint | 3.6 MWh | ~39.6 MWh | ~79.2 MWh | W |
| Energy — envelope | 3.0–5.0 MWh | 33–55 MWh | 66–110 MWh | W |
| Continuous power | ~2 MW | ~22 MW | ~44 MW | W |
| Peak power (10 s min) | ~4 MW | ~44 MW | ~88 MW | W |

**Allocation math:** 40 MWh ÷ 11 blocks = 3.636 MWh → 3.6 MWh working midpoint.

### 4.3 Contingency scenarios (per block)

| Scenario | Trigger | Energy | Duration |
|---|---|---|---|
| Single genset trip | 1 of 4 CG260-16 trips; remaining 3 ramp | ~1–2 MWh | Seconds to minutes |
| Partial gas curtailment | Gas supply pressure drop; L3 orders derate | ~2–3 MWh | Minutes — graceful ramp-down |
| Full gas-loss graceful shutdown | Total gas interruption to block | ~3–4 MWh | 15–20 min GPU checkpoint + cassette cooldown |

Full gas-loss scenario sets the 3 MWh floor. BESS is not sized for extended hold — gas supply continuity is the primary reliability path.

### 4.4 Chemistry and coupling

- **LFP (LiFePO4)** — lowest thermal runaway risk, 3,000–6,000 cycles at 80% DOD, wider temperature tolerance, cleaner NFPA 855 AHJ path. NMC / NCA eliminated.
- **DC-coupled** — battery pack output 1,100–1,500 VDC → SiC bidirectional DC-DC → SSCB → blocking diode → 800 VDC block bus.
- **DC-DC converter spec:** SiC switching, 1,100–1,500 VDC input, 800 VDC ±1% regulated output, 2 MW continuous / 4 MW 10-second peak, ≥97% efficiency, galvanic isolation required, Modbus TCP (dispatch) + IEC 61850 GOOSE (fast protection) to L1 block PLC.

### 4.5 Vendor shortlist (BESS-RFQ-001 §11)

Engagement order:

1. **Fluence Energy — preferred.** Gridstack Pro 4.9–5.6 MWh per 20-ft, AESC HC-L530A LFP cell, up to 1,500 VDC. **Only vendor on shortlist that explicitly confirmed island / off-grid operation.** UL 9540A confirmed June 2025 large-scale fire tests (CSA Group, Safe Laboratories NC); NFPA 855 (2026) documentation in preparation. Arlington VA, +1 703 682 2700. Portfolio framing required: typical Fluence engagement is 100 MWh+ — lead with ~100+ containers across ADC Louisiana sites (Trappeys + MARLIE I + Willow Glen + New Iberia).
2. **LG Energy Solution Vertech** — JF2 DC LINK, 5.11 MWh, 1,134–1,499 VDC, UL 9540A confirmed. Manufactured Holland, Michigan — **strongest domestic content story for ITC**. Flag: 23-ft width (non-standard ISO) — confirm pad logistics and crane requirements before selection.
3. **Saft (TotalEnergies)** — Intensium Flex 3.4 / 4.3 / 5.1 MWh, 20-ft ISO, up to 1,500 VDC. TotalEnergies parent understands natural gas BTM. DC-version UL 9540A listing started late 2025 — verify before AHJ submittal. Saft US Cockeysville MD, +1 410 771 3200.
4. **Hitachi Energy AMPS** — engaged in parallel on DC-DC layer regardless of BESS container selection. Input validated at 1,550 VDC. Ask for battery partner list. Fallback if no BESS vendor integrates compliant DC-DC natively.

**Hold — CATL:** EnerC+ 4.07 MWh / TENER 6.25 MWh, UL 9540A confirmed on EnerC+. Hold pending Section 301 tariff clarity and ITC domestic content implications.

**Eliminated:** POWIN (bankrupt May 2025), Wärtsilä Quantum3 (AC block — integrated inverter defeats 800 VDC architecture), Samsung SDI SBB 1.5 (NCA chemistry).

### 4.6 Island-mode requirement

Behind-the-meter permanent island operation is a **disqualifying condition** in the RFQ — explicit written vendor confirmation of island / off-grid operation is required. Implied confirmation is not sufficient. Fluence is the only shortlist vendor with this confirmation today.

### 4.7 Key open items

| Ref | Item | Priority |
|---|---|---|
| E-10 | Per-block sizing validation against CG260-16 governor ramp data | C1 — pending Cat CSA |
| E-12 | Bidirectional DC-DC converter vendor selection — integrated or separate | C1 — pending BESS RFQ |
| E-13 | BESS container vendor selection (Fluence / LG / Saft) | C1 — pending BESS RFQ |
| NFPA 855 AHJ | Lafayette Parish interpretation | C1 — AHJ pre-application |
| PHYS | Rear slab NFPA 855 setback study | C2 |
| ITC | Domestic content per vendor | C2 |

---

## 5. Solar Integration

Source: ST-TRAP-SOLAR-001 Rev 0.1.

### 5.1 Panel and array

| Parameter | Value | Status |
|---|---|---|
| Panel | First Solar FS-7550A-TR1 (CdTe thin-film) | L |
| Panel count | 3,731 | L |
| Total DC capacity | 2.05 MW | L |
| Location | Building B1 and B2 rooftops | L |
| STC power per panel | 550 W | L |
| Vmp / Imp | 190.4 V / 2.89 A | L |
| Voc / Isc | 228.8 V / 3.08 A | L |
| Temperature coefficient (Pmax) | −0.32%/°C | L |
| Max system voltage | 1,500 VDC | L |
| Product warranty / linear performance | 12 yr / 30 yr (98% Y1, 0.3%/yr degradation, >89% Y30) | L |
| String configuration | 5 panels in series | L |
| Complete strings | 746 | W |

**Panel count check:** 746 strings × 5 panels × 550 W = 2,051.5 kW ≈ 2.05 MW. ✓

**CdTe Louisiana advantage:** ~+2% hot climate, ~+4% humid climate, salt-air certified (IEC 61701), immune to LID / LeTID, immune to hurricane cell cracking. **~+6% cumulative 30-year advantage over silicon** in Louisiana.

### 5.2 String voltage analysis — confirms >800V MPP across Louisiana temperature range

| Condition | Cell temp | String MPP | String Voc | 1,500V limit |
|---|---|---|---|---|
| STC reference | 25°C | 952V | 1,144V | ✓ |
| Summer peak | 45°C | **~891V** | <952V | ✓ above 800V |
| Winter cold | 5°C | **~1,013V** | ~1,208V | ✓ within |
| Extreme cold (design) | −5°C | ~1,074V | ~1,240V | ✓ within |
| **Lafayette record low (1989 — Rev 0.2)** | −12°C | ~1,095V | ~1,263V | ✓ 237V margin (16%) |

**Voc temp coefficient (Rev 0.2):** Cold-limit analysis uses First Solar FS-7550A Voc temp coef of −0.28%/°C (per datasheet). Rev 0.1 implicitly used the Pmax coefficient (−0.32%/°C) which overstated Voc expansion. NEC 690.7 binding calc uses Voc coef × (T_min − 25°C) applied to STC Voc — at Lafayette record low −12°C, string Voc = 5 × 228.8 × (1 + 0.0028 × 37) = 1,263 V. 237 V margin to the 1,500 V system limit is comfortable. String MPP stays above 800V across the full Louisiana temperature range. Total array current at MPP = 2,155 A at ~952V.

### 5.3 DC-DC buck converter (E-22 open)

Interface between 1,500 VDC string field and 800 VDC bus. Performs voltage step-down, MPPT, and bus interface simultaneously.

| Parameter | Requirement |
|---|---|
| Input voltage range (MPPT) | 800–1,500 VDC |
| Output voltage | 800 VDC ±1% regulated |
| Total rated power | 2.05 MW |
| Efficiency | ≥97% at rated |
| Switching | SiC preferred |
| Configuration | **4-unit preferred** — one per roof section, independent MPPT per section, ~512 kW per unit |
| Isolation | Required, or confirm ground-fault detection if non-isolated |
| Protection | Input/output OV, OC, arc-fault, GFDI |
| Comms | Modbus TCP to L1 block PLC |

**Vendor shortlist (E-22):**
- **Delta Electronics — preferred** (single-vendor alignment with E-24 in-row power racks)
- SMA Solar Technology (Core1, Sunny Highpower)
- ABB (TRIO series DC-DC)
- Ampt (per-string optimizer alternative architecture)

### 5.4 Bus interface

Strings → combiner boxes + DC disconnects → DC-DC buck (1,500→800 V, MPPT) → SSCB → blocking diode → 800 VDC block bus.

Solar physically ties to blocks nearest B1/B2 (nominal ~186 kW per block on paper but actual allocation is routing-dependent; non-adjacent blocks carry zero solar in base case). Inter-block solar distribution is a SLD-001 decision (E-23 tie coupling).

### 5.5 Energy production and operating role

| Parameter | Value | Basis |
|---|---|---|
| Louisiana specific yield | ~1,750 kWh/kWp | W — industry average; yield study required |
| Estimated annual production | ~3,588 MWh/year | W |
| Year 30 production (>89%) | ~3,193 MWh | W |
| Campus annual generation at 108.24 MW × 8,760 h × CF 0.90 | ~853,000 MWh | W |
| Solar offset fraction (annual) | ~0.42% | W |
| Peak midday production (clear, 22°C) | ~1.85 MW | W |
| Peak instantaneous offset | ~1.7% | W |

Solar is **subordinate and supplemental**. Displaces genset fuel burn at margin; charges BESS during clip events; extends engine TBO intervals. **Does not reduce genset count, BESS sizing, or create net-zero claim.** Never shuts down gensets for solar — gensets hold minimum loading for frequency stability.

### 5.6 ITC basis

| Item | Value | Notes |
|---|---|---|
| Federal Solar ITC base | 30% | IRC §48E |
| Domestic content adder | +10% → 40% total | First Solar US-manufactured Perrysburg OH + New Iberia LA; confirm with tax counsel |
| Estimated module cost | $575K–$720K | $0.28–0.35/W market rate |
| Estimated total solar CapEx | $2.5M–$3.5M | Modules + DC-DC + mounting + wiring + structural |
| ITC at 30% | $750K–$1.05M | |
| ITC at 40% (domestic content) | $1.0M–$1.4M | |

New Iberia factory is 30 miles from site — expedited delivery potential. Reference-architecture narrative: first DC-direct 1,500V solar to 800V AI factory bus anywhere; First Solar made in Louisiana powering Louisiana's anchor AI factory.

### 5.7 Key open items

| Ref | Item | Priority |
|---|---|---|
| E-22 | DC-DC buck converter vendor RFQ (Delta preferred, 4-unit) | C1 |
| B-07 | Structural assessment B1/B2 — rooftop loading ~143,700–148,100 kg | C2 |
| YIELD | Bankable energy yield study (P50/P90) | C2 |
| ITC-DC | Domestic content determination vs IRS requirements | C2 |

---

## 6. Thermal Architecture

Source: ST-TRAP-THERMAL-BASIS Rev 0.4 (Rev 0.5 pending to absorb this correction).

### 6.1 Architecture summary

**CHP cascade (Locked, T-01):** genset exhaust drives a Broad BH double-effect LiBr absorption chiller sized for **33 MW actual campus absorption load** (see §6.8 census). Chiller produces chilled water for facility cold distribution (Munters process air post-desiccant, NOC, offices, cassette air-side heat, transformer/switchgear rooms). Absorption condenser + absorber circuit rejects through cooling tower field. Boyd CDU GPU warm water loop is a physically and thermally separated circuit rejecting through a dedicated adiabatic dry cooler. **Orphaned drive heat (~77 MW) is dumped via exhaust bypass on the HRU and a dedicated jacket water radiator** — Option A working basis.

### 6.2 Working basis: Option A (dump) — and retained contingencies

| Option | Description | Status |
|---|---|---|
| **Option A — minimum absorption, dump excess** | 33 MW double-effect absorption chiller driven by exhaust HRU sized for ~24 MW drive heat. Remaining exhaust bypassed around HRU. Full jacket water (~58 MW) rejected via dedicated radiator since JW is not needed for the smaller absorption array. | **Working basis** |
| Option B — absorb everything | Scale absorption to 114 MW (33 MW CHW + 81 MW Boyd replacement). Eliminates Boyd adiabatic dry cooler. Uses essentially all CHP drive heat (~82% utilization). Requires ~200 MW tower field. | Contingency — CHP utilization / incentive story |
| Option C — two absorption systems | Double-effect for 33 MW CHW load (exhaust-driven) + single-effect for 81 MW Boyd loop (JW-driven). Eliminates Boyd dry cooler. ~100% CHP utilization. Requires ~250 MW tower field. | Contingency — best CHP narrative |
| Option D — smaller HRU variant | Same as A but with even smaller HRU; more heat to stack. Economically similar to A; mechanically simpler. | Contingency — if HRU backpressure becomes binding |
| ~~Option B (Rev 0.1 meaning) — double-effect hot-water 107 MW~~ | Superseded — 107 MW load was incorrect (double-counted Boyd GPU heat). | Superseded |
| ~~Option A (Rev 0.1 meaning) — single-stage direct-fired~~ | Eliminated — architecturally incompatible with CHP cascade. | Eliminated |

**Architecture decision gating:** Option A is the working basis because 20-year total cost (capex + parasitic + water) is lowest by ~$48M vs Option B and ~$50M vs Option C. Options B/C re-enter consideration only if (a) a federal or state CHP utilization incentive makes the ~82–100% utilization story worth ~$48M, or (b) the Cat CSA returns exhaust parameters that make exhaust bypass mechanically awkward.

**TB-5 resolution (Rev 0.1 framing of Option B vs C):** superseded by the Option A pivot. The Cat CSA exhaust temperature question remains important but is no longer gating architecture — only HRU sizing and bypass design.

### 6.3 Munters desiccant deduction (T-12, Locked — unchanged)

Each cassette houses one Munters HCD/MCD unit drawing 125 kW exhaust slip-stream for desiccant regeneration. Louisiana wet-bulb (28°C ASHRAE 0.4%) and 75–80% RH annual average make desiccant dehumidification **an architectural constraint, not a feature option**.

| Parameter | Value | Status |
|---|---|---|
| Munters per cassette | 125 kW | L (T-12) |
| Stage 1 deduction (44 cassettes) | 5,500 kW | L |
| Full Build deduction (88 cassettes) | 11,000 kW | L (T-13) |

### 6.4 Cooling tower role — primary heat rejection for absorption chiller (reduced duty)

**Vermilion River is eliminated as heat sink.** Two disqualifying conditions unchanged from Rev 0.1:

1. **Tidal influence** — bidirectional flow at Lafayette; during reversal events effective mixing volume for regulated thermal discharge drops to near-zero or reverses.
2. **Ambient water temperature** — Gulf Coast surface water peaks at 30–33°C (86–91°F) in summer, exceeding Broad's 29°C rated condenser water inlet. River cannot provide meaningful ΔT for heat rejection during peak cooling demand months.

**Consequence unchanged:** ST-TRAP-RIVER-001 cancelled. LPDES thermal discharge permit not required. BOD T-04 ("residual rejection"), T-06 ("Vermilion River supplemental"), and R-03 require update at next BOD revision.

**Tower duty now much smaller:** Under Option A the tower field handles only absorption condenser + absorber rejection at ~57 MW nominal (vs 184 MW under Rev 0.1). See §8 for revised sizing.

**Water tower nomenclature clarification (unchanged):** the historic water tower on site (pressurized storage tank from original cannery operation) is currently inoperable and under consideration for restoration as a site landmark. It has **no role in the thermal system**.

### 6.5 Boyd CDU GPU warm water loop — isolated (unchanged)

| Parameter | Value | Status |
|---|---|---|
| Supply to GPU | ≤45°C | L (BOD C-03) |
| Return from GPU | ~50–55°C | W |
| Heat rejection path | Separate adiabatic dry cooler (not cooling towers) | L |
| Per-cassette heat | 1,840 kW (C-17) | L |
| Stage 1 total | ~80,960 kW | L |
| Thermal isolation | No shared basin, header, or piping with absorption chiller condenser circuit | L |

**Capture ratio confirmation — open (T-14, new):** Boyd locked 1,840 kW/cassette against 2,300 kW per-cassette IT implies 80% liquid capture. The remaining ~460 kW/cassette (20,240 kW Stage 1) is assumed to be air-side heat rejected via rear-door HX or room-level chilled water — this is the single largest line in the absorption load census (§6.8). Confirmation via Boyd application engineering call required. If Boyd actually captures 100% of cassette IT, absorption load drops from 33 MW to ~13 MW and Option A economics get more favorable.

### 6.6 CHW compatibility (T-11 open — unchanged)

T-11 confirms whether any Boyd CDU sub-loop requires 7–12°C chilled water input. If Boyd CDU supply is a closed warm-water loop with no tie to the 7°C chiller, T-11 resolves by separation. Priority C1 — gates cooling loop mechanical design. Resolution path: Boyd CDU application engineering call (combine with T-14).

### 6.7 Key open items

| Ref | Item | Priority |
|---|---|---|
| T-14 | Boyd capture ratio confirmation (80% vs 100% vs other) | C1 — new Rev 0.2 |
| T-03 | Chiller type selection in BOD ledger (locks on Option A double-effect) | C1 |
| T-08 | CHP heat balance — revised for Option A with dump paths sized | C1 |
| T-11 | Boyd CDU CHW supply compatibility | C1 |
| Cat CSA | CG260-16 exhaust temperature, mass flow, part-load curves | C1 |
| HRU-RFQ | Exhaust HRU vendor RFQ — now sized for ~24 MW drive heat (was ~42 MW) | C1 |
| COND-WB | Broad chiller app eng confirmation at 30–31°C condenser water inlet | C1 |
| JW-RAD | Jacket water radiator vendor + sizing RFQ (new under Option A) | C1 — new Rev 0.2 |

### 6.8 Thermal Load Census — Stage 1, 61.5% anchor (Rev 0.2, new)

Every identified heat source on the campus, classified by rejection circuit:

| Heat source | kW | Temp grade | Rejection circuit | Basis |
|---|---:|---|---|---|
| GPU liquid cooling (Boyd CDU × 44) | 80,960 | Med (45–55°C) | Dry cooler | L C-17 |
| Cassette air-side heat (20% of IT × 44) | 20,240 | Low (room) | Absorption CHW | Derived 1,840/2,300 — **T-14 gates** |
| Cassette aux — Munters blowers + CDU pumps (× 44) | 5,060 | Low | Absorption CHW | 115 kW/cassette aux |
| Delta in-row rack losses (704 racks) | 2,160 | Low | Absorption CHW | 2% of 106 MW facility |
| Munters process-air cooling (after desiccant) | 2,000 | Low (7°C) | Absorption CHW | Est 220,000 CFM sensible |
| Block step-down transformers (11 × 15 MVA) | 1,540 | Low | Absorption CHW | 1% FL losses |
| NOC + offices + partner hub (B1/B2) HVAC | 1,500 | Low (7°C) | Absorption CHW | Est |
| BESS converter losses + enclosure HVAC | 660 | Low | Packaged DX | 3% × 2 MW × 11 |
| MV switchgear + LV switchboard | 550 | Low | Absorption CHW | 50 kW/block × 11 |
| Electrical room envelope gain (Louisiana summer) | 110 | Low | Absorption CHW | 10 kW/block × 11 |
| Solar DC-DC buck losses (peak) | 61 | Low | Packaged DX | 3% of 2.05 MW |
| **TOTAL** | **94,841** | | | |

**Rolls up to:**

| Rejection circuit | Load | Equipment |
|---|---:|---|
| Boyd dry cooler | 80,960 kW | Adiabatic dry cooler (separate, existing architecture) |
| **Absorption CHW loop** | **33,160 kW** | **Broad BH double-effect, cooling tower condenser reject** |
| Packaged DX | 721 kW | Self-contained units in enclosures |
| **Total campus cooling** | **94,841 kW** | |

Rev 0.1 stated 107,300 kW absorption load. This figure was = IT (101,200 kW) + facility aux (~6,100 kW). The 80,960 kW of Boyd-captured GPU heat was double-counted: once as part of IT load driving absorption demand, and separately as dry cooler load. Since Boyd rejects independently to its own adiabatic dry cooler (§6.5, Locked C-17 architecture), it must not appear in absorption demand. Corrected value: **33 MW (3.2× overstatement factor in Rev 0.1).**

**Uncertainty band:**
- **13 MW (lower)** if Boyd captures 100% of cassette IT (T-14 returns 100% ratio)
- **33 MW (midpoint, working)** if Boyd captures 80% and air-side lands on CHW
- **45 MW (upper)** if Munters process-air and NOC loads are bigger than estimated

All three cases are well below the 107 MW Rev 0.1 figure. Option A architecture is robust across the band.

---

## 7. CHP Cascade

Source: ST-TRAP-CHP-SCHEMATIC-001 Rev 0.2 (pending — absorbs Rev 0.2 load census). Working basis **Option A**.

![Figure 3 — Thermal cascade, Option A working basis (Rev 0.2)](diagrams/fig3_thermal_cascade.svg)

### 7.1 End-to-end chain — Option A (revised for 33 MW absorption load)

```
44 × Cat CG260-16 (61.5% loading)
  · Electrical output: 108,240 kW (W)
  · Waste heat total: ~106,084 kW (W) — pending Cat CSA part-load derate
  · Exhaust: ~47,872 kW at 372–420°C est. (W)
  · Jacket water: ~58,212 kW at ≤99°C outlet (W)
    ↓
Exhaust header splits (three ways — Option A):
  · → Munters slip-stream (5,500 kW, L T-12) → desiccant regen → cassettes ≤50% RH
  · → Exhaust HRU (plate-fin; ~24,000 kW) → 180°C hot water → Broad BH chiller
  · → Exhaust BYPASS (~18,372 kW) → direct to stack
       (new under Option A — bypass valve on HRU inlet)
    ↓
Jacket water: primarily to dedicated RADIATOR (~58 MW)
  (new under Option A — not cascaded to absorption)
  Small JW side-stream available as contingency boost to hot water header
    ↓
Absorption drive header ~24,000 kW (W; HRU only, no JW)
    ↓
Broad BH two-stage LiBr double-effect chiller (sized for ~33 MW cooling)
  · Rated COP 1.50; operating COP 1.40 (part-load derate)
  · Chilled water 6.7°C supply / 13.7°C return → facility cold distribution
      (Munters process air, cassette air-side, NOC, offices, electrical rooms)
  · Absorption cooling produced: ~33,600 kW (matches census load within margin)
  · Condenser + absorber out: 37°C
    ↓
Condenser water circuit (~34,800 GPM max, VFD pumps N+1)
    ↓
Cooling tower field (wet mechanical draft, T-05 open; SPX/Marley · BAC · Evapco)
  · Design WB 28°C ASHRAE 0.4% (L)
  · Nominal duty 57,171 kW (57.2 MW) / 16,260 RT (W)
  · Design duty (30% margin) 74,300 kW (74.3 MW) / 21,130 RT (W)
  · Supply ≤31°C at 28°C WB, 3°C approach (W; COND-WB open)
    ↓
Atmosphere (evaporation + sensible)

PARALLEL CIRCUITS (unchanged):
  · Boyd CDU × 44 → adiabatic dry cooler (~81 MW, Locked C-17)
  · Packaged DX on BESS / solar DC-DC enclosures (~720 kW, trivial)
```

### 7.2 Heat Balance Summary — Stage 1 Campus, Option A, 61.5% Load (Rev 0.2)

| Stream | kW | Status | Disposition |
|---|---|---|---|
| Electrical generation (44 gensets) | 108,240 | W | IT + facility + aux |
| IT load (44 cassettes) | 101,200 | L | GPU compute |
| Facility aux (NOC, offices, controls) | ~6,100 | W | Facility load |
| **Total waste heat — exhaust + JW** | **~106,084** | **W** | → see split below |
| Munters slip-stream (T-12 LOCKED) | 5,500 | L | → desiccant regen (unchanged) |
| Exhaust HRU extraction (sized for 33 MW CHW) | ~24,000 | W | → Broad BH drive |
| **Exhaust BYPASS (direct to stack) — new** | **~18,372** | **W** | **→ stack, higher temp** |
| Jacket water to radiator — new | ~58,212 | W | → atmosphere via engine-style radiator |
| Absorption COP (Option A, operating) | 1.40 | W | — |
| Absorption cooling produced | ~33,600 | W | Matches campus CHW demand (§6.8) |
| Campus CHW demand (census) | ~33,160 | W | Per §6.8 |
| **Condenser + absorber rejection — nominal** | **~57,171** | **W** | → cooling towers (74% reduction vs Rev 0.1) |
| **Condenser + absorber rejection — design (30% margin)** | **~74,300** | **W** | → cooling towers (design sizing) |
| GPU warm water (Boyd CDU) | ~80,960 | L (C-17) | → adiabatic dry cooler (separate, unchanged) |
| Stack exhaust (after HRU extraction + bypass) | TBD | O | → atmosphere via stack |
| Cooling tower makeup water | ~750 GPM | W | → evaporation + blowdown |

**Key finding (Rev 0.2):** all campus CHW demand met by absorption cooling alone under Option A with ~24 MW exhaust drive. ~77 MW of waste heat (18.4 MW exhaust bypass + 58.2 MW JW radiator — minus any JW contingency flow to absorption) leaves via stack and dedicated radiator rather than cascading to absorption. **Effective CHP utilization under Option A: ~27%** (5.5 Munters + 24 HRU drive = 29.5 MW of 106 MW waste heat recovered). The remainder is dumped via standard genset cooling paths.

**CHP utilization framing:** this is lower than Rev 0.1's implied 86% but is the honest operating point. Option A eliminates the mechanical chiller plant entirely via absorption cooling on genset waste heat — still the correct CHP differentiation vs grid + electric chillers, but not a "fully utilized cascade" story.

### 7.3 Option A bypass design (new under Rev 0.2)

The HRU now has an exhaust bypass damper on the inlet (not present in Rev 0.1 architecture). Bypass design parameters:

| Parameter | Value | Notes |
|---|---|---|
| HRU duty (nominal) | ~24 MW exhaust heat extracted | Drives 33 MW absorption at COP 1.40 |
| HRU duty (turndown) | ~10 MW | Shoulder seasons, reduced IT load |
| Bypass damper sizing | ~50% of exhaust mass flow at full bypass | Total exhaust / HRU duty ratio |
| Bypass return | Manifold upstream of stack | Common stack serves HRU outlet + bypass |
| Controls | Absorption chiller discharge temperature feedback | Modulate bypass to maintain CHW supply |
| Backpressure budget (Cat limit 6.7 kPa) | HRU adds 2.0–2.5 kPa (reduced from Rev 0.1 because smaller HRU). With oxidation catalyst + Munters tee + stack + bypass damper: total 3.8–5.1 kPa with 1.6–2.9 kPa margin (24–43%) | W |

### 7.4 Component status (Rev 0.2)

| Component | Status | Notes |
|---|---|---|
| Cat CG260-16 genset | L (count, rating); W (61.5% loading, voltage option) | Cat CSA pending |
| Munters slip-stream 5.5 MW | L (T-12) | Locked per BOD — unchanged |
| Exhaust HRU (~24 MW — reduced from 42 MW) | O (vendor) | Cain / E-Tech / Rentech — RFQ required |
| **Exhaust bypass damper — new** | O | RFQ with HRU package |
| **Jacket water radiator — new** | O (vendor) | Engine-standard package; Cat preferred or aftermarket |
| Broad BH double-effect chiller (33 MW) | W | Size reduced ~75% from Rev 0.1 |
| Condenser water circuit (~34,800 GPM) | W | Flow, temps, COND-WB pending |
| Cooling tower field (57 MW nominal) | W (type, T-05 open) | Wet mechanical draft recommended basis |
| Boyd CDU + adiabatic dry cooler | L (Boyd CDU per C-03); O (dry cooler vendor) | Unchanged from Rev 0.1 |

---

## 8. Cooling Tower Field

Source: ST-TRAP-COOLING-TOWER-001 Rev 0.2 (pending — Rev 0.1 reflected 241 MW tower duty; Rev 0.2 reflects 57 MW nominal under Option A).

### 8.1 System boundary (unchanged)

The cooling tower field serves **one circuit exclusively**: the absorption chiller condenser + absorber cooling water loop. **Continuous full-load duty**, not peak-day supplement.

**Not served:** Boyd CDU GPU warm water (separate adiabatic dry cooler; ~81 MW from 44 × 1,840 kW). Thermal cross-contamination prevented — separate circuits, separate equipment, no shared basin or header.

### 8.2 Thermal duty — revised for Option A

| Parameter | Value | Status |
|---|---|---|
| **Nominal duty (33 MW absorption load)** | **~57,171 kW / 57.2 MW / 16,260 RT** | W |
| **Design duty (30% margin over nominal)** | **~74,300 kW / 74.3 MW / 21,130 RT** | W |
| Turndown ratio (min load / design) | ~25% | W |

Nominal duty = absorption chiller at census load with COP 1.40 (cooling 33 MW + drive heat 24 MW = 57 MW rejected). Design duty applies 30% margin for (a) T-14 uncertainty on Boyd capture ratio, (b) Cat CSA part-load derate surprises, and (c) redundancy / future expansion headroom.

**Compared to Rev 0.1 (241 MW max / 184 MW nominal): 69–76% reduction in tower sizing.** The 30% margin above nominal is generous and allows Option A to absorb partial shifts toward Option B without re-tenderring the tower field if incentive eligibility later favors higher CHP utilization.

### 8.3 Condenser water circuit (revised)

| Parameter | Value | Status |
|---|---|---|
| Supply (tower outlet → chiller inlet) | ≤29°C rated; ≤31°C derating case | W |
| Return (chiller outlet → tower inlet) | 37°C | W |
| Temperature range (ΔT) | 8°C (14.4°F) | W |
| Circulating flow — nominal duty (57 MW) | ~1,700 L/s / ~27,100 GPM | W |
| Circulating flow — design duty (74 MW) | ~2,220 L/s / ~35,200 GPM | W |

### 8.4 Approach temperature gap — COND-WB open (unchanged analysis)

At ASHRAE 0.4% Lafayette wet-bulb (28°C):
- Broad BH rated condenser inlet: **29°C** → required tower approach 1°C (not achievable economically with commercial mechanical-draft towers)
- Standard 3°C approach: **31°C** condenser water supply → **2°C above Broad rated inlet**
- Standard 5°C approach: 33°C → 4°C above rated

**Not a project-stopper.** Absorption chillers operate above rated CW temperature with predictable capacity / COP derating (expected 3–5% at 2°C above rated). The 30% design margin on tower duty absorbs the derating without impact to CHW reliability.

**COND-WB resolution (unchanged procedure):**
1. Broad / Thermax application engineering confirms operating envelope at 30–31°C CW inlet.
2. RFQ specifies supply ≤31°C at 28°C WB, 3°C approach as binding performance point.
3. Broad confirmation is pre-award condition on chiller RFQ.
4. If Broad imposes stricter CW limit: re-evaluate for ≤2°C approach (larger tower, higher capex) vs alternative chiller vendor with higher rated CW tolerance.

### 8.5 Water consumption (wet tower, design duty)

| Parameter | Value | Basis |
|---|---|---|
| Evaporation rate (design duty) | ~505 GPM | ~1.44% of circulation at 14.4°F range |
| Cycles of concentration (design) | 3.0 | Industry standard municipal water |
| Blowdown rate | ~250 GPM | Evaporation / (COC − 1) |
| Drift loss | <0.5 GPM | 0.001% with eliminators |
| **Total makeup — design duty** | **~755 GPM (~1.09 MGD)** | Sum |
| Total makeup — nominal duty | ~580 GPM (~0.84 MGD) | Scaled |
| **Annual makeup — nominal** | **~395 MG/year** | Continuous duty |

**Water story much cleaner under Option A:** annual makeup drops from ~1,300 MG/year (Rev 0.1) to ~395 MG/year. Municipal supply is now viable without straining Lafayette's system (<1% of municipal avg). LDEQ permit exposure on intake is lower threshold. WATER-SRC remains C1 but is no longer project-critical sizing risk.

### 8.6 Electrical — cooling plant MCC (revised)

| Item | Working Value |
|---|---|
| Tower fan motors (all cells) | ~915 kW (1–1.5% of 74 MW rejected) |
| Condenser water pumps | ~500 kW (2,220 L/s, ~15–20 m head, 75% eff) |
| Makeup, blowdown, chemical dosing, sump | ~60 kW |
| **Total cooling tower MCC (campus)** | **~1,475 kW** |

**Note on BOD E-29:** E-29 allocated ~600 kW per block × 11 = 6,600 kW campus for cooling plant. Rev 0.2 revised figure is ~1,475 kW — a 3,325 kW reduction. Per-block allocation: 134 kW/block average if distributed, or (more likely) single centralized campus switchboard at ~1,500 kW fed from the Power Hall. Architectural decision open for SLD-001.

**Consequence for electrical balance:** the 3.3 MW parasitic reduction meaningfully helps close the §3.7 margin problem where 61.5% anchor couldn't cover full site load including cooling MCC. Under Rev 0.2, 63% genset dispatch now covers total site load with ~3 MW net headroom vs −4 MW under Rev 0.1 sizing.

### 8.7 Tower type (T-05 open — unchanged framing, simpler decision)

| Option | Fit | Assessment |
|---|---|---|
| **Wet mechanical draft** | **Recommended basis** | Lowest capex; best approach to wet-bulb; ~755 GPM makeup easily sourced municipally; standard Legionella management |
| Hybrid dry/wet | Contingency | 1.5–2× wet capex; 30–50% annual water reduction; less compelling at reduced water draw |
| Adiabatic | Not recommended | Highest capex; peak-day limited by 35°C dry-bulb (not wet-bulb) |
| Full dry | Rejected | Cannot maintain ≤31°C CW at 35°C design dry-bulb at economic scale |

### 8.8 Siting — 28,000 sq ft yard no longer flagged

Reference tower sizing at 21,000 RT design duty: SPX/Marley NC or BAC Series 3000 counterflow at 10,000 RT occupies ~60 × 30 ft. For 21,130 RT total:
- 2 units + N+1 spare (3 cells total)
- **Estimated field footprint ~6,100 sq ft** (reduced from 20,000 sq ft in Rev 0.1)
- Infrastructure yard (28,000 sq ft) now has ~22,000 sq ft remaining for SCR + transformers + MV switchgear + service access

**Yard packing now closes comfortably.** The rear slab overflow flagged in Rev 0.1 is no longer required for tower positioning. Rear slab remains flagged for genset + BESS packing (see §9.1 SITING-001).

### 8.9 Vendor shortlist (unchanged)

| Vendor | Key Products | Notes |
|---|---|---|
| SPX / Marley | NC counterflow, FXV fluid cooler, Ultracool hybrid | Widest RT range; US-manufactured |
| BAC (Baltimore Aircoil) | Series 3000 counterflow, ICC, Hybrid Cooler | Strong CHP + industrial experience |
| Evapco | AT, UT; hybrid AMC; LSTA low-profile | US-manufactured; DOE pump efficiency compliant |
| Brentwood Industries | PVC fill media — component supplier | Not a packaged tower vendor |

RFQ anchor conditions pending T-05 decision and COND-WB close. Updated RT is a much more vendor-comfortable size.

---

## 9. Open Engineering Items — Master List

Consolidated across all documents. Priority: **C1 = must close, critical path** (blocks construction package or procurement); **C2 = desirable, not blocking construction**.

### 9.1 Items blocking RFQ / procurement (must close before vendor award)

| ID | Description | Blocking What | Source Doc | Priority |
|---|---|---|---|---|
| ~~TB-5~~ | ~~Absorption chiller Option B vs C~~ | **Superseded by Rev 0.2 Option A pivot** | THERMAL-BASIS §7 | — |
| **T-14 (new Rev 0.2)** | **Boyd CDU capture ratio — 80% vs 100% — confirmation via Boyd app eng** | **Absorption chiller final sizing (13 MW vs 33 MW vs 45 MW band)** | THERMAL-BASIS §6.5, §6.8 | **C1** |
| **E-31 (new Rev 0.2)** | **CO control strategy — oxidation catalyst selection + expected emissions; Title V Major Source acknowledgment** | **LDEQ Title V pre-app; BOD Rev 0.5 locks** | ELEC-001 §3.2; LDEQ Title V | **C1** |
| **JW-RAD (new Rev 0.2)** | **Jacket water radiator sizing + vendor RFQ (Option A requires ~58 MW JW radiator — new scope vs Rev 0.1)** | **CHP cascade mechanical design; ELEC-001 aux feeders** | CHP-SCHEMATIC §7.1 | **C1** |
| Cat CSA | CG260-16 exhaust temp, mass flow, part-load heat rejection curves at 61.5% load; N-1 governor response envelope; CO emissions at anchor loading | T-08 heat balance; E-5/E-6 voltage and governor confirmation; E-31 CO | THERMAL-BASIS §11; ELEC-001 §15; BOD-001 §M | C1 |
| HRU-RFQ | Exhaust HRU vendor RFQ (Cain / E-Tech / Rentech) — **resized to ~24 MW drive (Rev 0.2) with bypass damper** | Option A exhaust cascade lock | THERMAL-BASIS §11 | C1 |
| COND-WB | Broad chiller app eng confirmation — condenser water inlet at 30–31°C | Cooling tower CW supply spec; chiller RFQ pre-award | COOLING-TOWER-001 §8.4; THERMAL-BASIS §11 | C1 |
| T-05 | Cooling tower type selection (wet / hybrid / adiabatic) | Tower RFQ | COOLING-TOWER-001 §8.7; BOD-001 T-05 | C1 |
| T-08 | CHP heat balance final values — **revised for Option A with dump paths (exhaust bypass + JW radiator)** | Cooling tower sizing lock; ELEC-001 cooling MCC feeder | THERMAL-BASIS §11 | C1 |
| T-11 | Boyd CDU CHW supply 7–12°C compatibility | Cooling loop mechanical design | THERMAL-BASIS §8; BOD-001 T-11 | C1 |
| E-10 | Per-block BESS sizing validation (3.6 MWh working, 3–5 MWh envelope) | BESS RFQ vendor award | BESS-001 §13; ELEC-001 §15 | C1 |
| E-12 | Bidirectional DC-DC converter vendor selection | BESS RFQ | BESS-001 §13 | C1 |
| E-13 | BESS container vendor selection (Fluence / LG / Saft) | BESS RFQ close | BESS-001 §13 | C1 |
| NFPA 855 AHJ | Lafayette Parish AHJ NFPA 855 (2026) interpretation | BESS AHJ submittal; setback lock | BESS-001 §13; BESS-RFQ-001 §13 | C1 |
| E-24 / E-25 | Delta 660 kW rack RFQ; **4 vs 5 per cassette (5 now preferred per Rev 0.2 — 73% loading, rack N-1 tolerance)**; lead times at 10 and 100+ quantities | In-row rack procurement | ELEC-001 §15 | C1 |
| E-8 | Block step-down transformer (13.8 kV → 480 V, ~15 MVA) RFQ | Transformer procurement | ELEC-001 §15 | C1 |
| E-11 | Block MV switchgear vendor RFQ | MV switchgear procurement | ELEC-001 §15 | C1 |
| E-22 | Solar DC-DC buck converter vendor RFQ (Delta preferred, 4-unit) | Solar procurement | SOLAR-001 §12 | C1 |
| **SITING-001 (elevated Rev 0.2)** | **Rear slab + infrastructure yard packing study — 42,000 sq ft rear slab undersized for 44 gensets + BESS at standard spacing; yard now OK under reduced tower footprint** | **Genset + BESS layout; construction sequence** | COOLING-TOWER-001 §8.8 | **C1 (was C2)** |
| **WATER-SRC (elevated Rev 0.2)** | **Makeup water source decision — municipal vs well vs Vermilion intake (easier at 395 MG/year vs 1,300 MG/year Rev 0.1)** | **LPDES pre-app; water permit pathway** | COOLING-TOWER-001 §8.5 | **C1 (was C2)** |
| **BLOWDOWN (elevated Rev 0.2)** | **Blowdown disposal (POTW / Vermilion intake / evaporation pond)** | **LPDES pre-app** | COOLING-TOWER-001 §8.5 | **C1 (was C2)** |

### 9.2 Items blocking construction / downstream documents

| ID | Description | Blocking What | Source Doc | Priority |
|---|---|---|---|---|
| SLD-001 | Formal single-line diagram | Construction package gate | README; ELEC-001 §15 | C1 |
| PROT-001 | Protection coordination study | Construction package gate; CT ratios, pickup settings, coord intervals | README; ELEC-001 §15; BESS-001 §13 | C1 |
| E-9 | Protection coord across AC-DC boundary per block | PROT-001 | ELEC-001 §15 | C1 |
| E-14 | Bus interconnect topology between blocks (E-23 tied vs independent) | ELEC-001 §9 advance; SLD-001 routing | README; ELEC-001 §15 | C1 |
| SHPO R-05 / R-06 | Historic Tax Credit Part 1 / Part 2 filing | HTC financing (45% stack) | README; BOD-001 §M | C1 |
| LDEQ LPDES | Pre-application (cooling tower blowdown only; river discharge cancelled) | Thermal/water design lock | BOD-001 §M | C1 |
| LDEQ Title V | Air permit pre-application for 44 gensets | Air emissions design lock | BOD-001 §M | C1 |
| LA ITEP | Filing before any construction | Construction kickoff | BOD-001 §M | C1 |
| Gas supply lock | Pipeline interconnect, metering, contingency storage | Block 1 energization | BOD-001 §M | C1 |
| NVIDIA allocation | Vera Rubin GPU allocation | Stage 1 GPU count P-07 lock | BOD-001 §M | C1 |

### 9.3 C2 items (desirable, not blocking construction award)

| ID | Description | Blocking What | Source Doc | Priority |
|---|---|---|---|---|
| BOD-UPD | BOD T-04, T-06, R-03 update — river eliminated; towers primary | BOD next revision | COOLING-TOWER-001 §2 | C2 |
| CRYST-MIN | Minimum CW supply temp to chiller (LiBr crystallization floor) | Tower control constraint | COOLING-TOWER-001 §11 | C2 |
| NOISE-VIS | Tower height, plume drift, fan noise — parish + SHPO | Tower submittal | COOLING-TOWER-001 §11 | C2 |
| B-07 | Structural assessments B1–B4 | Rooftop solar loading; interior retrofit | BOD-001 B-07; SOLAR-001 §4 | C2 |
| LAYOUT | Solar rooftop layout design — panel placement, walkways, HVAC clearances | Solar installation | SOLAR-001 §12 | C2 |
| YIELD | Bankable energy yield study (P50/P90) | Solar financial model | SOLAR-001 §12 | C2 |
| ITC-DC | First Solar domestic content vs IRS requirements | Solar ITC basis confirmation | SOLAR-001 §12 | C2 |
| MPPT | Multi-MPPT configuration — independent zones per roof | Solar DC-DC design | SOLAR-001 §12 | C2 |
| ITC (BESS) | Domestic content verification — Saft (France) vs LG (Holland MI) | BESS ITC basis | BESS-001 §13 | C2 |
| HITACHI | Hitachi AMPS compatibility with shortlisted BESS packs | DC-DC vendor selection | BESS-001 §13 | C2 |
| PHYS (BESS) | Rear slab NFPA 855 setback study (now subsumed under SITING-001 C1) | BESS container positions | BESS-001 §13; BESS-RFQ-001 §13 | C2 |
| LG 23-ft | LG ES Vertech JF2 23-ft width logistics | LG selection feasibility | BESS-RFQ-001 §13 | C2 |
| A-05 / A-06 / A-07 | AI model vendor; human-in-loop policy; cybersecurity framework (NIST CSF / IEC 62443) | Ops design | BOD-001 §I | C2 |
| C-25 | Immersion fluid vendor (GRC vs Submer — deferred, future rev) | Cassette future revision | BOD-001 C-25 | C3 |
| Parish PILOT | Negotiation (below $200M threshold, pursued vs HB 827) | Tax structure | BOD-001 §M | C2 |
| CATL | Section 301 tariff + ITC eligibility | CATL re-entry consideration | BESS-001 §13 | C3 |

**Rev 0.2 elevations to C1 (see §9.1):** SITING-001, WATER-SRC, BLOWDOWN.

---

## 10. Document Register

### 10.1 Issued documents (current revisions)

| Doc # | File | Rev | Date | Status | Supersedes |
|---|---|---|---|---|---|
| ST-TRAP-BOD-001 | 00-Basis/TRAP-BOD-001_Rev0.4.md | 0.4 | 2026-04-17 | Working draft — canonical | Rev 0.3 (MV-ring architecture removed) |
| ST-TRAP-THERMAL-BASIS | 00-Basis/ST-TRAP-THERMAL-BASIS_Rev0.4.md | 0.4 | 2026-04-18 | Working draft — first issue | — |
| ST-TRAP-ELEC-001 | 01-Electrical/Trap-ELEC-001_Rev1.2.md | 1.2 | 2026-04-17 | Working draft | Rev 1.1 (ARCHDIAG refinements rolled in) |
| ST-TRAP-ARCHDIAG-001 (MD) | 03-Architecture/ST-TRAP-ARCHDIAG-001_Rev0.1.md | 0.1 | 2026-04-17 | Working draft — six-diagram SLD | — |
| ST-TRAP-ARCHDIAG-001 (PDF) | 03-Architecture/ST-TRAP-ARCHDIAG-001_Rev0.1-1.pdf | 0.1 | 2026-04-17 | Working draft | — |
| ST-TRAP-ARCHDIAG-001 (DOCX) | 03-Architecture/ST-TRAP-ARCHDIAG-001_Rev0.1(1).docx | 0.1 | 2026-04-17 | Working draft | — |
| ST-TRAP-BESS-001 | 02-Bess/TRAP-BESS-001_Rev0.1.md | 0.1 | 2026-04-17 | Working draft — first issue | — |
| ST-TRAP-BESS-ARCHDIAG-001 | 02-Bess/ST-TRAP-BESS-ARCHDIAG-001_Rev0.1.md | 0.1 | 2026-04-17 | Working draft — five Mermaid diagrams | — |
| ST-TRAP-BESS-RFQ-001 | 02-Bess/ST-TRAP-BESS-RFQ-001_Rev0.1.md | 0.1 | 2026-04-18 | Working draft — ready for vendor distribution | — |
| ST-TRAP-CHP-SCHEMATIC-001 | 07-Thermal/ST-TRAP-CHP-SCHEMATIC-001_Rev0.1.md | 0.1 | 2026-04-18 | Working draft — visual companion | — |
| ST-TRAP-COOLING-TOWER-001 | 07-Thermal/ST-TRAP-COOLING-TOWER-001_Rev0.1.md | 0.1 | 2026-04-18 | Working draft — first issue | — |
| ST-TRAP-SOLAR-001 | 09-Solar/ST-TRAP-SOLAR-001_Rev0.1.md | 0.1 | 2026-04-18 | Working draft — first issue | — |
| ST-TRAP-MASTER-ENG-001 | ST-TRAP-MASTER-ENG-001_Rev0.2.md (this doc) | 0.2 | 2026-04-18 | Working draft — thermal load census correction; Option A pivot | Rev 0.1 |

### 10.2 Pending / blocked documents

| Doc # | Description | Gate Conditions |
|---|---|---|
| ST-TRAP-SLD-001 | Formal single-line diagram (inherits ARCHDIAG-001 + ELEC-001) | ELEC-001 Rev 1.3+ (Cat CSA close), E-14 inter-block tie decision, BESS vendor lock, solar DC-DC lock |
| ST-TRAP-PROT-001 | Protection coordination study | SLD-001 draft; CT ratios, pickup settings, coord intervals; BESS DC-side coordination settings |

### 10.3 Cancelled documents

| Doc # | Reason |
|---|---|
| ST-TRAP-RIVER-001 | Cancelled. Vermilion River eliminated as heat sink per THERMAL-BASIS §9.1 (tidal reversal + Gulf Coast summer ambient 30–33°C > Broad 29°C rated CW inlet). LPDES thermal discharge item removed. |

---

## 11. Critical Path to Construction Package

The construction package gate is **SLD-001 + PROT-001**. The following milestone sequence is required to reach that gate. **Rev 0.2 pivoted thermal architecture from TB-5 (Option B vs C) to Option A (working basis) — critical path sequence rewritten accordingly.**

| # | Milestone | Depends On | Unblocks | Target Owner |
|---|---|---|---|---|
| 1 | **Cat CSA engagement** — CG260-16 exhaust temp, mass flow, part-load heat rejection curves at 61.5%, N-1 governor response at 80.5%, voltage option confirmation, CO emissions at anchor loading | None (engagement in hand) | HRU sizing refinement; T-08 heat balance final; E-5/E-6 voltage + governor; E-31 CO baseline; THERMAL-BASIS Rev 0.5; ELEC-001 Rev 1.3 | Scott / Cat |
| 2 | **Boyd app eng call — T-14** (Rev 0.2 new) — confirm capture ratio (80% vs 100% vs other); resolve T-11 CHW compatibility in same call | None (engagement-ready) | Absorption chiller final sizing (13 / 33 / 45 MW band); T-11 resolution; chiller RFQ scope lock | Scott / Boyd |
| 3 | **Broad / Thermax app eng — COND-WB** | Preliminary Cat exhaust data (Step 1); T-14 sizing confirmation (Step 2) | Condenser water inlet envelope at 30–31°C; cooling tower RFQ binding spec lock; chiller RFQ pre-award | Scott / Broad / Thermax |
| 4 | **T-05 cooling tower type decision** — wet / hybrid / adiabatic (simpler decision under reduced 57 MW duty) | Water cost analysis + LPDES blowdown disposal review | Cooling tower RFQ issue to SPX/Marley / BAC / Evapco; COOLING-TOWER-001 Rev 0.3 | Scott |
| 5 | **HRU vendor RFQ + award (Rev 0.2 — Option A sizing)** — Cain / E-Tech / Rentech; **~24 MW duty with exhaust bypass damper**; backpressure binding ≤6.7 kPa Cat | T-14 (Step 2) closing sizing; Cat exhaust mass flow confirmed (Step 1) | Exhaust cascade lock; CHP-SCHEMATIC-001 Rev 0.3 | Scott |
| 5B | **JW radiator vendor RFQ + award (Rev 0.2 new)** — ~58 MW jacket water radiator; Cat-preferred aftermarket or engine-standard package | Cat CSA JW temp + flow (Step 1); Option A confirmed | JW rejection path lock; CHP-SCHEMATIC-001 Rev 0.3 | Scott |
| 6 | **Absorption chiller vendor RFQ + award** — Broad BH double-effect, sized for 13 / 33 / 45 MW per T-14 band (Rev 0.2: scope defaults to 33 MW midpoint with design margin) | T-14 (Step 2); HRU award (Step 5); COND-WB confirmation (Step 3) | Chiller selection lock; THERMAL-BASIS Rev 0.6 | Scott |
| 7 | **Cooling tower vendor RFQ + award** — ~21,000 RT design duty (reduced from 68,000 RT Rev 0.1) | T-05 (Step 4); T-08 heat balance; COND-WB confirmation (Step 3); SITING-001 study | Tower field procurement; COOLING-TOWER-001 Rev 1.0 | Scott |
| 8 | **BESS vendor engagement + RFQ award** — Fluence (preferred) → LG ES Vertech → Saft; Hitachi AMPS in parallel on DC-DC layer | BESS-RFQ-001 Rev 0.1 distribution (done); Cat governor preliminary data (Step 1 subset) | BESS container selection (E-13); DC-DC converter selection (E-12); per-block sizing lock (E-10); BESS-001 Rev 0.3 | Scott |
| 9 | **First Solar engagement + DC-DC buck RFQ (E-22)** — Delta preferred, 4-unit configuration; First Solar pricing via New Iberia factory proximity | SOLAR-001 Rev 0.1 (done); multi-year offtake portfolio framing | DC-DC vendor lock; SOLAR-001 Rev 0.2; solar module purchase order | Scott / First Solar / Delta |
| 10 | **Delta in-row rack RFQ (E-24 / E-25)** — Rev 0.2 preferred config: **5 racks/cassette (20/block)** with N-1 tolerance; 4 racks/cassette as fallback; 10-unit and 100+ unit lead times | None (procurement-ready today) | In-row rack procurement; ELEC-001 Rev 1.4 | Scott / Delta |
| 11 | **Block MV switchgear + step-down transformer RFQs (E-8, E-11)** | ELEC-001 Rev 1.3 (Cat voltage confirmed — Step 1) | MV switchgear + transformer procurement | Scott |
| 12 | **CO oxidation catalyst vendor RFQ (E-31 — Rev 0.2 new)** — size for 44 CG260-16 gensets; >90% CO destruction; NOx-compatible (non-SCR) or co-deployed with SCR | Cat CSA emissions data (Step 1) | Title V air permit path; BOD Rev 0.6 | Scott / catalyst vendor |
| 13 | **BOD-001 Rev 0.5 trigger** — Rev 0.2 thermal architecture (Option A) + Munters slip-stream + Cat CSA data applied; updates T-03, T-04, T-06, T-08, R-03, F-section | T-14 (Step 2); T-08 close; Cat CSA data (Step 1) | Downstream documents re-cite BOD Rev 0.5 | Scott |
| 14 | **SHPO Part 1 filing (R-05)** | — | Historic review initiated; HTC 45% stack preserved | Scott / SHPO |
| 15 | **LDEQ LPDES pre-application** — cooling tower blowdown only; reduced volume (~395 MG/year vs 1,300 MG/year Rev 0.1) | T-05 (Step 4); BLOWDOWN path decision; WATER-SRC decision | Water / thermal design lock; BOD-001 Rev 0.7 | Scott / LDEQ |
| 16 | **LDEQ Title V pre-application** — 44-genset air emissions, **CO control strategy included (Rev 0.2)** | Cat CSA emissions data (Step 1); CO catalyst RFQ (Step 12) | Air emissions design lock | Scott / LDEQ |
| 17 | **LA ITEP filing** — before any construction | BOD Rev 0.5+ | Construction kickoff | Scott / LED |
| 18 | **Gas supply lock** — pipeline interconnect, metering, contingency storage; **contracted capacity sized for 100% load contingency (~40,300 Nm³/hr campus, Rev 0.2)** | Gas utility engagement | Block 1 energization | Scott / gas utility |
| 19 | **NFPA 855 AHJ pre-application (Lafayette Parish)** | BESS vendor compliance docs (Step 8); rear slab layout (SITING-001) | BESS setback study; PHYS layout lock | Scott / AHJ |
| 20 | **SITING-001 packing study (Rev 0.2 — elevated to C1)** — rear slab 42,000 sq ft genset + BESS packing; infrastructure yard 28,000 sq ft verification (now relaxed under reduced tower footprint) | — | Construction sequencing; genset + BESS layout locked; BESS NFPA 855 setbacks (Step 19) | Scott / layout engineer |
| 21 | **Structural assessments B1–B4 (B-07)** | — | Rooftop solar loading lock; interior retrofit scope; HTC Part 2 inputs | Scott / structural engineer |
| 22 | **E-14 inter-block tie decision** (11 independent vs tied at aux point) | Contingency analysis; BESS sizing (Step 8) | ELEC-001 §9 advance; SLD-001 routing | Scott |
| 23 | **SLD-001 draft** — formal single-line inheriting ARCHDIAG-001 + ELEC-001 | Steps 1, 8, 9, 10, 11, 22 closed | PROT-001 input | Scott |
| 24 | **PROT-001 draft** — protection coordination study with CT ratios, pickup settings, coord intervals, AC-DC boundary coordination | SLD-001 (Step 23) | **Construction package gate** | Scott / protection engineer |

### 11.1 BOD-001 revision trigger summary (Rev 0.2 updated)

| BOD Rev | Trigger | Approximate sequence step |
|---|---|---|
| 0.4 (current) | E-24 through E-30, A-09 added from ARCHDIAG-001 | — |
| **0.5 (Rev 0.2 target)** | **Thermal architecture Option A lock; thermal load census; T-04/T-06/R-03 updates; CHP heat balance; Munters slip-stream; Cat CSA preliminary data; CO strategy line-item** | **After Step 1 (Cat CSA) + Step 2 (T-14 Boyd) + Step 12 (CO catalyst RFQ issued)** |
| 0.6 | Cat CSA validation complete; updates E-05, E-06, E-08; CO emissions locked | After Step 1 fully closed + Step 11 + Step 12 |
| 0.7 | LDEQ LPDES pre-application returns; updates B-section and G-section | After Step 15 |
| 0.8 | SHPO Part 1 filing; updates R-05 and HTC constraints | After Step 14 |
| 1.0 | All C1 external dependencies locked; ready for circulation | After Steps 1–24 closed |

### 11.2 Construction package gate

SLD-001 Rev 1.0 + PROT-001 Rev 1.0 paired with THERMAL-BASIS Rev 1.0, COOLING-TOWER-001 Rev 1.0, BESS-001 Rev 1.0, SOLAR-001 Rev 1.0, CHP-SCHEMATIC-001 Rev 1.0, and BOD-001 Rev 1.0. All C1 items per §9.1 and §9.2 closed.

### 11.3 Rev 0.2 pivot summary

The thermal architecture pivot from Rev 0.1 (Option B, 107 MW absorption load, 241 MW tower duty) to Rev 0.2 (Option A, 33 MW absorption load, 74 MW tower duty) removes three items from the critical path and adds two:

**Removed from critical path:**
- TB-5 Option B vs C decision (superseded — Option A is working basis)
- Large HRU (~42 MW) RFQ scope
- Large cooling tower RFQ scope (68,640 RT)

**Added to critical path:**
- T-14 Boyd capture ratio confirmation (Step 2 — gates absorption sizing)
- JW radiator vendor RFQ (Step 5B — new rejection path under Option A)

**Retained but resized:**
- HRU RFQ (~24 MW, down from ~42 MW)
- Cooling tower RFQ (~21,130 RT, down from 68,640 RT)
- Absorption chiller RFQ (33 MW, down from 107 MW equivalent)

Net effect: schedule compression (fewer architectural decisions gated on Cat CSA) and capex reduction (~$48M over 20 years vs Option B per §6.2). The trade-off is lower stated CHP utilization (~27% vs ~86%) — narrative and incentive implications covered in §6.2 contingency framing.

---

**End of ST-TRAP-MASTER-ENG-001 Rev 0.2.**
