# ST-TRAP-MASTER-ENG-001 — Master Engineering Package — Rev 0.4

**Document:** Master Engineering Package — Trappey's AI Center
**Project:** Trappey's AI Center — 22-acre historic cannery site, Vermilion River, Lafayette, Louisiana
**Revision:** 0.4 — cassette architecture reconciled; 480 VAC block bus confirmed; IT load and thermal numbers rebased
**Date:** 2026-04-23
**Owner:** Scott Tomsu
**Status:** Working draft — internal use only
**Authority:** BOD-001 Rev 0.6 governs all locked values. This document consolidates the current state of downstream engineering documents; all value changes flow through BOD-001.

L = Locked · W = Working · O = Open

---

## Rev 0.4 Changelog

Rev 0.3 → Rev 0.4 changes (2026-04-23):

1. **Electrical — cassette architecture reconciled (§1, §3).** Cassette is AC-in: 480 VAC primary feed to each cassette. Five Delta 660 kW in-row power racks (R11–R15) inside each cassette rectify 480 VAC → 800 VDC on a cassette-internal busway. No shared block-level 800 VDC bus. §3.1 block steps rewritten; block-level DC busway removed; cassette 480 VAC primary feeds added. Source: Cassette-ELEC-001 Rev 1.3 / BOD-001 Rev 0.6.
2. **Electrical — IT load rebased (§1, §2, §3, §7).** 101.2 MW (44 × 2,300 kW) → **91.1 MW (44 × 2,070 kW)**. Cascade: 9 compute racks × 230 kW × 44 cassettes. GPU count: 31,680 → **28,512 Stage 1** (44 × 648); 63,360 → **57,024 Full Build**. Per-cassette facility load: 2,415 kW → **~2,295 kW**. Block cassette facility load: 9.66 MW → **~9.18 MW**. Source: BOD-001 Rev 0.6 C-11 / C-15.
3. **Electrical — load margin now positive (§3.7).** At 61.5% anchor, generation (108.24 MW) exceeds total site load (~104–106 MW) by **+2.3 to +4.3 MW**. Rev 0.3 showed negative margin; Rev 0.4 positive throughout the AI dispatch envelope. Source: ELEC-001 Rev 1.3 §11.
4. **Electrical — BESS AC-coupled (§4).** BESS LFP → Hitachi AMPS PCS SiC bidirectional inverter → 480 VAC block bus. No DC-DC converter at block level. Sub-100 ms GPU transients handled by Delta rack BBU + Power Capacitance Shelf inside each cassette. Source: BOD-001 Rev 0.6 E-11/E-12.
5. **Electrical — solar AC-coupled (§5).** 1,500 VDC strings → PV inverter → 480 VAC block bus. No DC-DC buck converter. Source: BOD-001 Rev 0.6 E-17.
6. **Thermal — CDU updated (§6, §7, §8).** Boyd CDU replaced with **CoolIT CHx2000 external CDU skid** per Cassette-COOL2-001 Rev 1.0. Source: BOD-001 Rev 0.6 C-03.
7. **Thermal — Munters updated (§6).** Munters HCD/MCD → **Munters DSS Pro**. T-12 regen basis flagged for DSS Pro reconciliation. Source: BOD-001 Rev 0.6 C-19.
8. **Thermal — secondary cooling rebased (§6, §7, §8).** Per-cassette GPU warm water: 1,840 kW → **~1,656 kW** (80% × 2,070 kW IT). Stage 1 tower duty: 80.96 MW → **~72.9 MW** (44 × ~1,656 kW). Full Build: 161.9 MW → **~145.7 MW**. Flow: 30,700 GPM → **~27,600 GPM**. Makeup: 830 GPM / 1.20 MGD → **~747 GPM / ~1.08 MGD**. Source: BOD-001 Rev 0.6 C-17.
9. **Document register updated (§10).** BOD-001 Rev 0.5 → Rev 0.6; ELEC-001 Rev 1.2 → Rev 1.3; MASTER-ENG Rev 0.3 → this document.

---

## Rev 0.3 Changelog

Rev 0.2 → Rev 0.3 changes (2026-04-22):

1. **Thermal — absorption chiller ELIMINATED (§6, §7, §8).** Decision locked 2026-04-22.
2. **Thermal — CHP exhaust: Munters slip-stream only (§7).** 5,500 kW (T-12 LOCKED). Remainder (~42,372 kW) to stack.
3. **Thermal — Boyd CDU path reversed (§6.5, §8).** GPU warm water routes facility headers → plate HX PHX-001 → cooling tower circuit.
4. **Thermal — cooling towers serve GPU warm water exclusively (§8).**
5. **Cancelled open items:** T-03, T-11, T-14, COND-WB, HRU-RFQ.
6. **Document register updated:** CHP-SCHEMATIC Rev 0.2 and COOLING-TOWER Rev 0.2 issued.

---

## 1. Executive Summary

Trappey's AI Center is a **91.1 MW IT load AI compute facility** on a 22-acre historic cannery site on the Vermilion River in Lafayette, Louisiana. The site hosts 12 nationally registered historic structures. Four principal buildings (B1–B4) are under active engineering; supporting infrastructure sits on a 42,000 sq ft rear slab and 28,000 sq ft infrastructure yard.

The facility is a **behind-the-meter permanent electrical island from day one** — no utility grid import or export in base-case operation, no LUS interconnect provisioning. Power is generated on-site by 44 × Cat CG260-16 natural gas gensets (4,000 ekW each) organized into 11 electrically independent blocks. Each block: 13.8 kV genset bus → step-down transformer → **480 VAC block switchboard** as the convergence point for all sources and loads. Each cassette takes a **480 VAC primary feed** from the block switchboard; five Delta 660 kW in-row power racks per cassette (R11–R15) rectify 480 VAC → 800 VDC on a **cassette-internal busway only**. No shared block-level 800 VDC bus. BESS (LFP, AC-coupled via Hitachi AMPS PCS bidirectional inverter) and solar (First Solar Series 7 CdTe, AC-coupled via PV inverter) connect to the **480 VAC block bus**. No anti-islanding. No sell-back to LUS modeled.

**Stage 1 / Full Build:**

| Parameter | Stage 1 | Full Build | Status |
|---|---|---|---|
| IT load | 91.1 MW (44 × 2,070 kW) | 182.2 MW (88 × 2,070 kW) | L |
| Cassettes | 44 | 88 | L |
| Gensets (Cat CG260-16) | 44 | 88 | L |
| Blocks | 11 | 22 | L |
| GPUs (NVIDIA Vera Rubin, 648/cassette) | 28,512 | 57,024 | W |
| Per-cassette IT | 2,070 kW | 2,070 kW | L |
| Per-cassette facility | ~2,295 kW | ~2,295 kW | W |

![Figure 1 — Stage 1 energy flow, Rev 0.4](diagrams/fig1_energy_sankey.svg)

**Thermal architecture** is a simplified two-path system. CHP genset exhaust drives Munters DSS Pro desiccant dehumidification per cassette (5,500 kW, T-12 LOCKED). No absorption chiller. No exhaust HRU. No CHW distribution. Exhaust remainder (~42,372 kW) and full jacket water (~58,212 kW) reject to atmosphere via stack and dedicated JW radiators respectively. CoolIT CHx2000 external CDU skid GPU warm water (~50–55°C return) routes through facility warm-water headers to plate HX PHX-001 (C1 open item), which is the thermal and hydraulic boundary between the closed CDU circuit and the open cooling tower circuit. Cooling towers reject **~72.9 MW GPU warm water** to atmosphere. No separate adiabatic dry cooler. Building-level cooling (NOC, offices, electrical rooms) served by per-building split DX — no central CHW plant.

**Why this approach:** BTM permanent island removes the primary reliability dependency on LUS and eliminates interconnect schedule risk. 11-block replicated Marlie-pattern architecture contains blast radius to one block and enables phased construction with standardized procurement. CHP exhaust drives Munters desiccant (Louisiana 75–80% RH annual average makes desiccant dehumidification an architectural constraint). CoolIT CHx2000 CDU handles 100% of GPU heat on a dedicated liquid circuit, eliminating the mechanical chiller plant and centralizing atmospheric rejection through three cooling tower cells. 480 VAC block bus with cassette-internal 800 VDC rectification matches the Cassette-ELEC-001 Rev 1.3 architecture; BESS and solar are AC-coupled on the same 480 VAC bus for simplicity and protection. Zero utility dependency is the thesis.

---

## 2. Site & Project Basis

Source: BOD-001 Rev 0.6.

![Figure 4 — Site layout, 22-acre Trappey's cannery (SITING-001 C1 gate)](diagrams/fig4_site_layout.svg)

### 2.1 Locked project-level parameters

| # | Parameter | Value | Status |
|---|---|---|---|
| P-01 | Site | 22-acre Trappey's Cannery, Vermilion River, Lafayette, LA | L |
| P-02 | Historic structures | 12 nationally registered | L |
| P-03 | Stage 1 IT load | 91.1 MW (44 × 2,070 kW) | L |
| P-04 | Stage 1 cassette count | 44 | L |
| P-05 | Full Build IT load | 182.2 MW (88 × 2,070 kW) | L |
| P-06 | Full Build cassette count | 88 | L |
| P-07 | GPU target Stage 1 | 28,512 NVIDIA Vera Rubin | W |
| P-09 | Revenue model | Colocation only, base case | L |
| P-10 | Sell-back to LUS | Excluded from base case; future optionality only | L |
| E-01 | Operating mode | Behind-the-meter permanent island, day one | L |
| E-07 | Campus electrical topology | Replicated Marlie-pattern blocks; 480 VAC block bus; cassette-internal 800 VDC only; no MV ring | L |
| B-01/B-02 | Building 1/2 role | Historic restoration — NOC / partner hub / rooftop solar | L |
| B-03 | Building 3 role | Compute hall — 20 cassettes | L |
| B-04 | Building 4 role | Compute hall — 24 cassettes | L |
| B-05 | Rear slab | 42,000 sq ft — genset installation + BESS | L |
| B-06 | Infrastructure yard | 28,000 sq ft — cooling and SCR | L |

### 2.2 Decision Ledger — domain status summary

Per BOD-001 §E–N. L = Locked, W = Working, O = Open.

| Domain | Locked | Working | Open | Representative open item |
|---|---|---|---|---|
| **P — Project-level** | 9 | 1 | 0 | — |
| **R — Regulatory / incentive** | 6 | 2 | 2 | R-05 / R-06 SHPO Parts 1 & 2 |
| **C — Cassette platform** | 24 | 0 | 1 | C-25 Immersion fluid vendor (deferred) |
| **E — Electrical** | 10 | 13 | 1 | E-23 Inter-block tie topology |
| **T — Thermal** | 8 | 1 | 3 | T-05 tower type; T-08 heat balance; PHX-001 plate HX sizing |
| **B — Structural / buildings** | 6 | 0 | 1 | B-07 Structural assessments not commissioned |
| **A — Operations & AI control** | 5 | 1 | 3 | A-05 AI model; A-06 Human-in-loop; A-07 Cybersecurity framework |
| **S — Solar (E-14 through E-17)** | 4 | 0 | 0 | (E-22 PV inverter RFQ tracked under E) |
| **N — Naming / communication** | 3 | 0 | 0 | — |

---

## 3. Power Architecture

Source: ST-TRAP-ELEC-001 Rev 1.3.

### 3.1 Block structure (one block, top-down)

Each of the 11 Stage 1 blocks is structurally identical to a 5 MW Marlie block except for the prime mover. Within one block:

1. **4 × Cat CG260-16** gas gensets, 4,000 ekW each at 60 Hz / 900 rpm, paralleled on 13.8 kV block MV bus via Cat ECS isochronous sharing. 3-of-4 carry load; 4th is N+1.
2. **Block MV bus** — 13.8 kV arc-resistant switchgear, 87B bus differential, three-stage UFLS (59.5 / 59.2 / 58.9 Hz).
3. **Block step-down transformer** — 13.8 kV Δ → 480Y/277 V, ~15 MVA, Dyn11, dry-type / cast-resin, Z≈6%. One per block.
4. **480 VAC main switchboard** — solidly grounded wye secondary, 50G residual ground sensing, LSIG main trip unit. **This is the convergence point for all block sources and loads.**
5. **4 × cassette 480 VAC primary feeds** — 480 VAC from block switchboard → Eaton Magnum DS 6,000 A cassette main disconnect at cassette boundary → cassette interior. Each cassette draws ~2,295 kW (~2,416 kVA at 0.95 PF); 4 cassettes ~9.18 MW (~9.66 MVA) total. Inside each cassette, 5 × Delta 660 kW in-row power racks (R11–R15) rectify 480 VAC → 800 VDC on the cassette-internal busway.
6. **DER ties on 480 VAC bus** — BESS via Hitachi AMPS PCS SiC bidirectional inverter (2 MVA continuous / 4 MVA peak, AC-coupled); solar PV via AC inverter (~2.1 MVA). Both connect to the block 480 VAC switchboard via AC circuit breakers. **Bus sizing: ~12,100 A cassette-only load; +4,811 A BESS peak injection; 17,000 A minimum bus and main breaker rating.**
7. **Cassette-internal 800 VDC busway** — inside the cassette envelope only. Not accessible at block level. 5 × Delta racks feed the internal busway → 9 NVL72/CPX compute racks (R1–R9) + 1 control rack (R10).

11 electrically independent blocks. No inter-block MV ring. No inter-block 800 VDC tie. No shared block-level 800 VDC bus. Shared services (gas header, water plant, NOC, security, AMCL) span the campus but do not carry power between blocks.

![Figure 2 — Single Stage 1 block electrical topology (Rev 0.4)](diagrams/fig2_block_electrical.svg)

### 3.2 Genset specification — Cat CG260-16

| Parameter | Value | Status |
|---|---|---|
| Rated output | 4,000 ekW continuous, 60 Hz, 900 rpm | L |
| Electrical efficiency | 43.8% (LHV, at 100% load — part-load derate pending Cat CSA) | L |
| Thermal efficiency | 42.4% (LHV to 120°C) | L |
| Total efficiency | 86.2% | L |
| Design anchor loading | 61.5% (2,460 ekW per genset) | W — pending Cat CSA |
| AI dispatch envelope (steady-state) | 55–75%; 63–65% expected average | W |
| **N-1 contingency envelope** | **55–85% — surviving 3 gensets per block carry 80.5% during single-genset trip** | W — Cat CSA to confirm |
| MV voltage | 13.8 kV | W — Cat CSA to confirm |
| Fuel — at 61.5% anchor loading | ~2,200 Nm³/hr per block (~24,200 Nm³/hr Stage 1 campus). Note: this is 61.5% anchor load, **not** full load. | W |
| **Fuel — at 100% load contingency** | **~3,660 Nm³/hr per block; ~40,300 Nm³/hr Stage 1 campus** | W — firm pipeline capacity basis |
| Emissions — NOx | <250 mg/Nm³ at 5% O₂ | L |
| **Emissions — CO** | Uncontrolled CO ~500–650 mg/Nm³ typical; **Title V Major Source threshold (100 tpy) likely exceeded even with 90% oxidation catalyst. CO control strategy required — see E-31.** | W |
| Hydrogen blending | 25% blend capable at same continuous rating | L (future optionality) |

**Prime mover rule:** CG260-16 for Trappey's and 100+ MW deployments; Cat G3520K for Marlie 1 and ≤10 MW platforms. Not substitutable.

### 3.3 Five feeder categories (E-29, per block)

| Feeder | Load | Notes |
|---|---|---|
| 4 × cassette 480 VAC primary feeds | ~9.18 MW (~9.66 MVA) | Dominant feeder — 480 VAC to each cassette; 5 Delta racks inside each cassette do AC-DC conversion |
| Cooling plant MCC | ~122 kW | VFD-driven (per-block average; campus cooling MCC ~1,400 kW total — see §8.6) |
| BESS auxiliary | ~80 kW | Battery HVAC, BMS, fire system |
| Solar PV inverter auxiliary | ~10 kW | Controls, HVAC |
| Facility ancillary | ~200 kW | SCADA, NOC, site lighting, fire/life safety |

### 3.4 Protection (island-only)

- **Per-genset (E-26):** 87G differential, 32 reverse power, 40 loss of field, 46 negative sequence, 47 phase sequence, 59/27 over/under-voltage, 64G stator ground, 78 out-of-step, 51V voltage-restrained overcurrent.
- **Block bus:** 87B bus differential, 51N neutral ground.
- **Transformer (E-27):** 87T overall differential (single two-winding transformer, one differential zone), 49T thermal (RTD), 63 pressure/gas, 51 time overcurrent on both primary and secondary, 50/51G ground overcurrent on secondary.
- **LV secondary (E-28):** solidly grounded wye, 52M with LSIG, 50G residual ground sensing.
- **Cassette 480 VAC primary:** Eaton Magnum DS 6,000 A draw-out disconnect at cassette boundary.
- **DER AC ties:** AC circuit breaker (draw-out LV, LSIG) at each BESS PCS output and each solar PV inverter output on the block 480 VAC switchboard.
- **Cassette-internal DC:** SSCB at each Delta rack output, SSCB at each compute/control rack feed, per Cassette-ELEC-001 Rev 1.3.
- **UFLS:** three-stage at block MV inlet — 59.5 / 59.2 / 58.9 Hz.

No anti-islanding. No external sync. No reverse-power coordination with utility.

### 3.5 Cassette internal topology (E-30, Locked)

Eaton Magnum DS 6,000 A 480 VAC cassette main disconnect → 5 × Delta 660 kW in-row power racks (R11–R15, AC-DC, 98% efficiency) → cassette 800 VDC internal busway → two branches:

- **Main DC distribution:** Eaton ORV3 PDUs + NVIDIA Kyber PDUs → 9 × OCP ORV3 compute racks (R1–R9) with NVL72/CPX trays → 648 Vera Rubin GPUs per cassette, 230 kW/rack, 2,070 kW cassette IT; 1 × control rack (R10).
- **Auxiliary:** CoolIT CHx2000 external CDU skid pumps (N+1), Munters DSS Pro blowers, Jetson AGX Orin BMS (148 sensor channels).

### 3.6 AMCL five-tier control (A-09, Working)

| Tier | Role |
|---|---|
| L0 field devices | Cat ECS governors, protection IEDs, VFDs, Jetson Orin BMS, RTDs, CTs/PTs |
| L1 block PLC | Paralleling, UFLS, BESS PCS setpoints, MPPT (solar), trip schemes, safety interlocks. Deterministic; cannot be overridden from higher tiers |
| L2 plant SCADA | Historian, OPC-UA backbone, cassette BMS aggregation (148 × 44 → 6,500 cassette points) |
| L3 AMCL dispatch (AI) | Cross-block optimization, gas/load/thermal coupling, BESS orchestration, solar recapture |
| L4 HMI + operator override | IEC 62443 segmentation, OT/IT isolation, incident response |

**AI failure mode:** last-known-good deterministic control. Gensets hold setpoint, BESS PCS holds mode, VFDs hold speed. Governors and protection autonomous. Operators take manual dispatch until AI restored.

### 3.7 Full Build vs Stage 1

| Parameter | Stage 1 (11 blocks) | Full Build (22 blocks) | Status |
|---|---|---|---|
| Cassette IT | 91.1 MW (44 × 2,070 kW) | 182.2 MW (88 × 2,070 kW) | L |
| Cassette facility | ~101.0 MW (44 × ~2,295 kW) | ~201.9 MW | W |
| Generation at 61.5% design anchor | 108.24 MW (9,840 kW/block × 11) | 216.5 MW | W |
| Generation at 63–65% operational | ~110.9–114.4 MW | ~221.8–228.8 MW | W |
| Block cassette facility load | ~9.18 MW (4 × ~2,295 kW) | ~9.18 MW | W |
| Non-cassette ancillary (cooling MCC + BESS aux + facility) | ~3–4 MW | ~6–8 MW | W |
| **Load margin at 61.5% anchor (Rev 0.4)** | **+2.3 to +4.3 MW positive** | — | W |
| Total Stage 1 site load | ~104–106 MW | — | W |

**Rev 0.4 note:** At 61.5% anchor, generation (108.24 MW) exceeds total site load (~104–106 MW) by +2.3 to +4.3 MW. Rev 0.3 showed negative margin at the old 2,300 kW/cassette basis; Rev 0.4 positive throughout the AI dispatch envelope. At 63–65% operational average: +5 to +7 MW additional margin.

**N-1 genset contingency:** At N-1 per block, the 3 surviving gensets carry ~9.18 MW / 12,000 kW = 76.5%. Below the 80.5% in the old basis (lower due to reduced cassette load). Cat CSA to confirm acceptable duration at this loading.

### 3.8 Single biggest technical risk

CG260-16 governor response in island-mode 24/7 at variable loading under AI dispatch, paired with block-level AC-coupled BESS via Hitachi AMPS PCS SiC bidirectional inverter. Cat CSA engagement is the most important external validation. If governor data returns unfavorable: add 5th genset per block (5:4 instead of 4:4) or oversize BESS.

---

## 4. BESS Architecture

Source: TRAP-BESS-001 Rev 0.1 (superseded — Rev 0.2 in progress) / BOD-001 Rev 0.6 E-10 through E-13.

**Note:** TRAP-BESS-001 Rev 0.1 described DC-coupled 800 VDC architecture. That revision is superseded. This section reflects BOD-001 Rev 0.6 (AC-coupled) as the current basis. Rev 0.2 of BESS-001 is in progress.

### 4.1 Role — stabilizer, not backup

BESS is **always active on the 480 VAC block bus** via Hitachi AMPS PCS bidirectional inverter, running continuously in charge/discharge under AMCL L1 (deterministic) and L3 (AI) control. Four operating functions, priority order:

1. **Transient buffer** — sub-cycle response to genset governor lag via SiC AC PCS (ms-scale response). Sub-100 ms GPU-level transients are handled by Delta rack BBU + Power Capacitance Shelf inside each cassette; block-level BESS handles sub-cycle to multi-minute transients.
2. **Contingency support** — single-genset trip, partial gas curtailment, full gas-loss graceful shutdown.
3. **Solar clip-recapture** — absorbs First Solar overproduction that would otherwise require PV inverter throttling.
4. **Load shifting** — flattens genset loading within 55–75% AI dispatch envelope.

BESS is **not** the primary voltage-forming source on the 480 VAC bus (gensets + transformer regulate bus voltage). Not a replacement for cassette-internal in-row BBU + PCS (which handles sub-100 ms GPU swings). Two storage layers run in parallel.

### 4.2 Sizing and power rating

| Parameter | Per block | Stage 1 facility (11 blocks) | Full Build (22 blocks) | Status |
|---|---|---|---|---|
| Energy — working midpoint | 3.6 MWh | ~39.6 MWh | ~79.2 MWh | W |
| Energy — envelope | 3.0–5.0 MWh | 33–55 MWh | 66–110 MWh | W |
| Continuous power | ~2 MVA | ~22 MVA | ~44 MVA | W |
| Peak power (10 s min) | ~4 MVA | ~44 MVA | ~88 MVA | W |

### 4.3 Contingency scenarios (per block)

| Scenario | Trigger | Energy | Duration |
|---|---|---|---|
| Single genset trip | 1 of 4 CG260-16 trips; remaining 3 ramp | ~1–2 MWh | Seconds to minutes |
| Partial gas curtailment | Gas supply pressure drop; L3 orders derate | ~2–3 MWh | Minutes — graceful ramp-down |
| Full gas-loss graceful shutdown | Total gas interruption to block | ~3–4 MWh | 15–20 min GPU checkpoint + cassette cooldown |

Full gas-loss scenario sets the 3 MWh floor. BESS is not sized for extended hold — gas supply continuity is the primary reliability path.

### 4.4 Chemistry and coupling

- **LFP (LiFePO4)** — lowest thermal runaway risk, 3,000–6,000 cycles at 80% DOD, wider temperature tolerance, cleaner NFPA 855 AHJ path. NMC / NCA eliminated.
- **AC-coupled** — battery pack output 1,100–1,500 VDC → Hitachi AMPS PCS SiC bidirectional inverter → AC circuit breaker → 480 VAC block bus.
- **PCS inverter spec:** SiC switching, 1,100–1,500 VDC DC input, 480 VAC ±1% 3-phase 60 Hz AC output, 2 MVA continuous / 4 MVA 10-second peak, ≥97% efficiency at rated, galvanic isolation required, grid-forming (island-mode) capable, Modbus TCP (dispatch) + IEC 61850 GOOSE (fast protection) to L1 block PLC.
- **Why AC-coupled at 480 VAC:** Storage is on the same voltage rail as the cassette primary feed. SiC PCS response (<1 cycle) is adequate because rack-level BBU+PCS handles sub-100 ms. Eliminates block-wide 800 VDC bus. Standard LV protection gear applies. Open vendor field — most commercial BESS PCS products ship 480 VAC native.

### 4.5 Vendor shortlist (BOD Rev 0.6 §N)

Engagement order:

1. **Fluence Energy — preferred.** Gridstack Pro 4.9–5.6 MWh per 20-ft, AESC HC-L530A LFP cell, up to 1,500 VDC with integrated AC PCS. Island / off-grid operation confirmed. UL 9540A confirmed. Arlington VA, +1 703 682 2700. Portfolio framing required (~100+ containers across ADC Louisiana sites).
2. **LG Energy Solution Vertech** — JF2 AC LINK (AC-coupled variant), 5.11 MWh, UL 9540A confirmed. Holland, Michigan — strongest domestic content for ITC. Confirm 23-ft width pad logistics before selection.
3. **Saft (TotalEnergies)** — Intensium Flex + AC PCS, 3.4 / 4.3 / 5.1 MWh, 20-ft ISO. DC-version UL 9540A listing — verify AC PCS variant before AHJ submittal. Saft US Cockeysville MD.
4. **Hitachi Energy AMPS PCS** — engaged in parallel on PCS layer regardless of BESS container selection. SiC AC inverter. Ask for battery partner list.
5. **Sungrow PowerTitan 2.0** — AC-coupled, LFP, 5 MWh. Evaluate.

**Hold — CATL:** EnerC+ 4.07 MWh / TENER 6.25 MWh. Hold pending Section 301 tariff + ITC domestic content clarity.

**Eliminated:** POWIN (bankrupt May 2025), Wärtsilä Quantum3 (unsuitable product line for this application), Samsung SDI SBB 1.5 (NCA chemistry).

### 4.6 Island-mode requirement

Behind-the-meter permanent island operation is a **disqualifying condition** in the RFQ — explicit written vendor confirmation of island / off-grid operation is required.

### 4.7 Key open items

| Ref | Item | Priority |
|---|---|---|
| E-10 | Per-block sizing validation against CG260-16 governor ramp data | C1 — pending Cat CSA |
| E-12 | PCS inverter vendor selection (integrated with BESS or standalone Hitachi AMPS PCS) | C1 — pending BESS RFQ |
| E-13 | BESS container vendor selection (Fluence / LG / Saft) | C1 — pending BESS RFQ |
| NFPA 855 AHJ | Lafayette Parish NFPA 855 (2026) interpretation | C1 — AHJ pre-application |
| PHYS | Rear slab NFPA 855 setback study | C2 |
| ITC | Domestic content per vendor | C2 |

---

## 5. Solar Integration

Source: ST-TRAP-SOLAR-001 Rev 0.1 (§1–§5 valid; §6–§7 superseded — Rev 0.2 in progress).

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
| String configuration | 5 panels in series | L |
| Complete strings | 746 | W |

### 5.2 String voltage analysis — confirms MPPT range across Louisiana temperature range

| Condition | Cell temp | String MPP | String Voc | 1,500V limit |
|---|---|---|---|---|
| STC reference | 25°C | 952V | 1,144V | ✓ |
| Summer peak | 45°C | **~891V** | <952V | ✓ |
| Winter cold | 5°C | **~1,013V** | ~1,208V | ✓ within |
| Extreme cold (design) | −5°C | ~1,074V | ~1,240V | ✓ within |
| Lafayette record low (1989) | −12°C | ~1,095V | ~1,263V | ✓ 237V margin |

String MPP stays above 600V (commercial PV inverter MPPT floor) across the full Louisiana temperature range.

### 5.3 PV Inverter Specification (E-22, Open — replaces DC-DC buck per Rev 0.4)

Interface between 1,500 VDC string field and 480 VAC block bus. Performs MPPT, grid-forming, and bus interface simultaneously.

| Parameter | Requirement |
|---|---|
| Input voltage range (MPPT) | 600–1,500 VDC (covers 891V summer to 1,095V record-low MPP) |
| Input voltage absolute max | 1,500 VDC |
| Output voltage | 480 VAC 3-phase 60 Hz, ±1% |
| Rated power | 2.05 MW DC / ~2.1 MVA AC |
| Efficiency (CEC weighted) | ≥98% |
| Island-mode / grid-forming | Required — no utility grid; must form voltage and frequency |
| Anti-islanding | DISABLED — no utility tie |
| Reactive power | ±0.9 PF capability minimum |
| Configuration | 4-unit preferred — one per roof section, ~512 kVA each, independent MPPT per section |
| Communications | Modbus TCP to L1 block PLC |

**Vendor shortlist (E-22, rebuilt):**
- SMA Solar Technology — Sunny Central UP series (grid-forming capable)
- Sungrow — SG3125HV series
- Power Electronics — FS3920K
- Fluence / Hitachi Energy — combined PV+BESS PCS (worth evaluating if same vendor for both)

### 5.4 Bus interface

Strings → combiner boxes + DC disconnects → PV inverter (1,500 VDC → 480 VAC, MPPT, grid-forming) → AC circuit breaker → 480 VAC block bus.

Solar physically ties to blocks nearest B1/B2. Inter-block solar distribution via 480 VAC feeder is an option under AC coupling — routing decision deferred to SLD-001.

### 5.5 Energy production and operating role

| Parameter | Value | Basis |
|---|---|---|
| Louisiana specific yield | ~1,750 kWh/kWp | W — industry average |
| Estimated annual production | ~3,588 MWh/year | W |
| Campus annual generation at 108.24 MW × 8,760 h × CF 0.90 | ~853,000 MWh | W |
| Solar offset fraction (annual) | ~0.42% | W |
| Peak midday production | ~1.85 MW | W |

Solar is **subordinate and supplemental**. Displaces genset fuel burn at margin. Never shuts down gensets for solar — gensets hold minimum loading for frequency stability.

### 5.6 ITC basis

| Item | Value | Notes |
|---|---|---|
| Federal Solar ITC base | 30% | IRC §48E |
| Domestic content adder | +10% → 40% total | First Solar US-manufactured Perrysburg OH + New Iberia LA |
| Estimated total solar CapEx | $2.5M–$3.5M | Modules + inverter + mounting + wiring + structural |
| ITC at 40% (domestic content) | $1.0M–$1.4M | |

### 5.7 Key open items

| Ref | Item | Priority |
|---|---|---|
| E-22 | PV inverter vendor RFQ (SMA preferred as starting point, 4-unit) | C1 |
| B-07 | Structural assessment B1/B2 — rooftop loading ~143,700–148,100 kg | C2 |
| YIELD | Bankable energy yield study (P50/P90) | C2 |
| ITC-DC | Domestic content determination | C2 |

---

## 6. Thermal Architecture

Source: ST-TRAP-THERMAL-BASIS Rev 0.5 (Rev 0.6 rebase in progress per cascade fix plan).

### 6.1 Architecture summary

**Absorption chiller ELIMINATED 2026-04-22.** CHP genset exhaust routes to Munters DSS Pro desiccant dehumidification (5,500 kW, T-12 LOCKED) and stack only. Full jacket water (~58,212 kW) rejected via dedicated JW radiators (JW-RAD, C1). CoolIT CHx2000 external CDU skid GPU warm water (~50–55°C return from cassettes) routes through facility warm-water headers to plate HX PHX-001 (C1 open item). PHX-001 is the thermal and hydraulic boundary between the closed CDU circuit and the open cooling tower circuit. Cooling towers reject **~72.9 MW GPU warm water** to atmosphere. No separate adiabatic dry cooler. Building-level cooling served by per-building split DX.

### 6.2 Decision basis

Absorption chiller eliminated because:
- CoolIT CHx2000 CDU handles 100% of GPU liquid cooling in a closed loop (~1,656 kW/cassette, W C-17). No IT-side chilled-water requirement.
- Remaining facility sensible loads are small (<5 MW total campus) and served by distributed split DX.
- Eliminating the chiller removes the exhaust HRU, CHW distribution headers, condenser water pumps — reducing capital cost.
- Cooling towers now serve only the GPU warm-water loop, simplifying control and sizing.

### 6.3 Munters desiccant deduction (T-12, Locked — T-12a open for DSS Pro reconciliation)

Each cassette houses one Munters DSS Pro unit drawing 125 kW exhaust slip-stream for desiccant regeneration. Louisiana 75–80% RH makes desiccant dehumidification an architectural constraint.

| Parameter | Value | Status |
|---|---|---|
| Munters per cassette | 125 kW | L (T-12) — T-12a open for DSS Pro datasheet reconciliation |
| Stage 1 deduction (44 cassettes) | 5,500 kW | L |
| Full Build deduction (88 cassettes) | 11,000 kW | L (T-13) |

**T-12a open item:** 125 kW/cassette regen draw was derived from HCD/MCD datasheet. DSS Pro is specified at C-19. Re-derive from DSS Pro datasheet and cassette moisture load before THERMAL-BASIS Rev 0.6 sign-off. Expected range ±30%; thermal balance not sensitive at campus level (<2% shift in residual stack heat).

### 6.4 Cooling tower role — primary atmospheric rejection for GPU warm water

Cooling towers serve **CoolIT CHx2000 CDU GPU warm water exclusively via plate HX PHX-001**. **~72.9 MW Stage 1** (44 × ~1,656 kW, W C-17). Continuous full-load duty.

**Vermilion River is eliminated as heat sink.** Two disqualifying conditions: (1) tidal influence — bidirectional flow at Lafayette; (2) ambient water temperature — Gulf Coast surface water peaks 30–33°C in summer.

**Water tower:** the historic water tower on site is currently inoperable and under consideration for restoration as a site landmark. It has **no role in the thermal system.**

### 6.5 CoolIT CHx2000 external CDU skid GPU warm water loop

| Parameter | Value | Status |
|---|---|---|
| Supply to GPU | ≤45°C | L (BOD C-04) |
| Return from GPU | ~50–55°C | W |
| Heat rejection path | Facility warm-water headers → plate HX PHX-001 → cooling tower circuit | L (Rev 0.3) |
| Per-cassette heat | ~1,656 kW | W (C-17) |
| Stage 1 total | ~72,864 kW | W |
| Full Build total | ~145,728 kW | W |

### 6.6 Plate HX — PHX-001

PHX-001 is the thermal and hydraulic boundary between the closed CoolIT CDU warm-water circuit and the open cooling tower circuit.

| Parameter | Value | Status |
|---|---|---|
| Hot-side inlet (CDU warm return) | ~50–55°C | W |
| Hot-side outlet (CDU supply back to cassettes) | ≤45°C | L (C-04) |
| Cold-side inlet (tower supply) | ~31–34°C | W |
| Cold-side outlet (tower return) | ~41–43°C | W |
| Temperature approach | ~14°C | W — comfortable for commercial gasketed plate HX |
| Duty Stage 1 | ~72,864 kW | W |
| Duty Full Build | ~145,728 kW | W |
| Open items | Vendor RFQ, number of units, material spec, maintenance access | O (C1) |

### 6.7 Key open items

| Ref | Item | Priority |
|---|---|---|
| **PHX-001** | Plate HX sizing + vendor RFQ (Alfa Laval / GEA / API) — ~72.9 MW Stage 1 | C1 |
| T-05 | Cooling tower type selection | C1 |
| T-08 | CHP heat balance final — Munters + stack + JW radiator paths | C1 |
| T-09 | Makeup water source — ~747 GPM / ~1.08 MGD | C1 |
| T-12a | Munters DSS Pro regen reconciliation (125 kW/cassette basis from HCD/MCD — re-derive) | C2 |
| Cat CSA | CG260-16 exhaust mass flow at 61.5%; JW temp + flow; N-1 governor response | C1 |
| JW-RAD | JW radiator vendor + sizing RFQ (~58,212 kW JW rejection at 61.5%) | C1 |

### 6.8 Thermal Load Census — Stage 1, 61.5% anchor (Rev 0.4 rebased)

| Heat source | kW | Temp grade | Rejection circuit |
|---|---:|---|---|
| GPU liquid cooling (CoolIT CHx2000 CDU skid × 44) | ~72,864 | Med (45–55°C) | PHX-001 → cooling towers |
| Cassette air-side / enclosure residual (~20% of IT, × 44) | ~18,216 | Low (room air) | Per-cassette/building split DX |
| Cassette aux — Munters DSS Pro blowers + CDU pumps (× 44) | ~5,060 | Low | Per-cassette/building split DX |
| Delta in-row rack losses (220 racks Stage 1, ~2% × 660 kW) | ~2,904 | Low | Per-building split DX |
| Munters process-air sensible (after desiccant) | 2,000 | Low | Per-cassette ventilation / split DX |
| Block step-down transformers (11 × 15 MVA) | 1,540 | Low | Forced-air room ventilation |
| NOC + offices + partner hub (B1/B2) HVAC | 1,500 | Low | Per-building split DX |
| BESS PCS losses + enclosure HVAC | 660 | Low | Self-contained packaged DX |
| MV switchgear + LV switchboard | 550 | Low | Room ventilation |
| Electrical room envelope gain (Louisiana summer) | 110 | Low | Per-room split DX |
| Solar PV inverter losses (peak) | ~61 | Low | Self-contained packaged DX |
| **TOTAL** | **~105,465** | | W — rebase from 94,841 kW (Rev 0.3) |

**Rolls up to:**

| Rejection circuit | Load | Equipment |
|---|---:|---|
| **PHX-001 → cooling towers** | **~72,864 kW** | **Plate HX + cooling tower field (§8)** |
| Per-building / per-cassette split DX | ~29,776 kW | Distributed packaged units |
| Self-contained packaged DX | ~721 kW | BESS enclosures, solar PV inverter |
| **Total campus cooling** | **~103,361 kW** | W |

---

## 7. CHP Cascade

Source: ST-TRAP-CHP-SCHEMATIC-001 Rev 0.2 (Rev 0.3 pending to rebase IT load and CDU).

![Figure 3 — Thermal cascade, Rev 0.4](diagrams/fig3_thermal_cascade.svg)

### 7.1 End-to-end chain — Rev 0.4 (no absorption chiller)

```
44 × Cat CG260-16 (61.5% loading)
  · Electrical output: 108,240 kW (W)
  · Waste heat total: ~106,084 kW (W) — pending Cat CSA part-load derate
  · Exhaust: ~47,872 kW at 372–420°C est. (W)
  · Jacket water: ~58,212 kW at ≤99°C outlet (W)
    ↓
Exhaust header splits (two ways):
  · → Munters DSS Pro slip-stream (5,500 kW, L T-12) → desiccant regen → cassettes ≤50% RH
  · → STACK (~42,372 kW) → atmosphere
    ↓
Jacket water:
  · → JW RADIATORS (~58,212 kW, JW-RAD, C1) → atmosphere

PARALLEL CIRCUITS:
  · CoolIT CHx2000 external CDU skid × 44 → facility warm-water headers
      → plate HX PHX-001 (facility boundary; CDU ≤45°C L C-04)
      → cooling tower circuit (supply ~31–34°C at 28°C WB, 3°C approach)
      → CT cells (~20,720 RT, ~72.9 MW, W C-17)
      → atmosphere
      → tower supply loops back to PHX cold-side inlet
  · Per-building split DX for NOC / offices / electrical rooms (~30 MW distributed)
  · Self-contained packaged DX on BESS / solar PV inverter enclosures (~720 kW)
```

### 7.2 Heat Balance Summary — Stage 1 Campus, Rev 0.4, 61.5% Load

| Stream | kW | Status | Disposition |
|---|---|---|---|
| Electrical generation (44 gensets) | 108,240 | W | IT + facility + aux |
| IT load (44 cassettes) | 91,080 | L | GPU compute |
| Facility aux (NOC, offices, controls) | ~6,100 | W | Facility load |
| Load margin at 61.5% | **+2,300 to +4,300 kW positive** | W | — |
| **Total waste heat — exhaust + JW** | **~106,084** | **W** | — see split below |
| Munters DSS Pro slip-stream (T-12 LOCKED) | 5,500 | L | → desiccant regen |
| **Stack exhaust (after Munters)** | **~42,372** | **W** | **→ atmosphere via stack** |
| **Jacket water to JW radiators** | **~58,212** | **W** | **→ atmosphere via dedicated radiators** |
| GPU warm water (CoolIT CHx2000 CDU) | ~72,864 | W (C-17) | → PHX-001 → cooling towers → atmosphere |
| Cooling tower makeup water | ~747 GPM | W | → evaporation + blowdown |

**No CHW produced. No absorption cooling. No condenser water circuit.**

**Note on CHP framing:** ~5,500 kW of genset exhaust heat is recovered for Munters desiccant regen (T-12 LOCKED), representing ~11.5% exhaust recovery. **External-facing materials should not describe this facility as a "CHP" or cogeneration facility.** Correct framing: "gas genset plant with exhaust heat recovery for on-site dehumidification."

### 7.3 Component status (Rev 0.4)

| Component | Status | Notes |
|---|---|---|
| Cat CG260-16 genset | L (count, rating); W (61.5% loading, voltage) | Cat CSA pending |
| Munters DSS Pro slip-stream 5.5 MW | L (T-12) | T-12a open for DSS Pro reconciliation |
| Stack (exhaust bypass — full) | W | No HRU |
| **JW radiators (~58 MW, JW-RAD)** | **O (vendor, sizing)** | C1 |
| **Plate HX PHX-001** | **O (vendor, sizing)** | C1 |
| Cooling tower field (~72.9 MW Stage 1) | W (type, T-05 open) | GPU warm water rejection |
| CoolIT CHx2000 external CDU skid | L (per C-03, C-04, C-17) | Cassette-level; 44 units Stage 1 |

---

## 8. Cooling Tower Field

Source: ST-TRAP-COOLING-TOWER-001 Rev 0.2 (Rev 0.3 pending to rebase to ~72.9 MW).

### 8.1 System boundary

The cooling tower field serves **one circuit exclusively**: CoolIT CHx2000 CDU GPU warm water, routed through plate HX PHX-001. **Continuous full-load duty.**

### 8.2 Thermal duty

| Parameter | Value | Status |
|---|---|---|
| Stage 1 duty (44 cassettes × ~1,656 kW) | **~72,864 kW / ~72.9 MW / ~20,720 RT** | W (C-17) |
| Full Build duty (88 cassettes) | ~145,728 kW / ~145.7 MW / ~41,440 RT | W |
| Operating profile | Continuous full-load; no seasonal swing | L |

### 8.3 Design conditions

| Parameter | Value | Status |
|---|---|---|
| CDU warm-water to PHX (hot-side in) | ~50–55°C | W |
| CDU supply from PHX (hot-side out) | ≤45°C | L (C-04) |
| Tower supply to PHX (cold-side in) | ~31–34°C | W |
| Tower return from PHX (cold-side out) | ~41–43°C | W |
| Tower ΔT | ~9–12°C | W |
| PHX approach temperature | ~14°C | W |
| Design wet-bulb | 28°C (ASHRAE 0.4%, Lafayette) | L |
| Tower approach to WB | 3°C → ~31°C cold supply | W |

### 8.4 Circulating flow — Stage 1

| Parameter | Value | Status |
|---|---|---|
| Heat duty Stage 1 | ~72,864 kW | W |
| ΔT tower circuit | ~10°C (midpoint of 9–12°C range) | W |
| Volumetric flow | ~1,740 L/s = **~27,600 GPM** | W |
| Circulating pumps | VFD-driven, N+1 | W |

### 8.5 Water consumption (Stage 1, continuous)

| Parameter | Value | Basis |
|---|---|---|
| Evaporation rate | ~498 GPM | ~1.44% of circulation at 10°C ΔT |
| Cycles of concentration (design) | 3.0 | Industry standard |
| Blowdown rate | ~249 GPM | Evaporation / (COC − 1) |
| Drift loss | <0.5 GPM | 0.001% with eliminators |
| **Total makeup — Stage 1** | **~747 GPM (~1.08 MGD)** | Sum |
| **Annual makeup** | **~1.55 billion gallons/year** | Continuous duty |

### 8.6 Electrical — cooling tower MCC

| Item | Working Value |
|---|---|
| Tower fan motors | ~730–1,095 kW (est. 1–1.5% of ~72.9 MW rejected) |
| Circulating pumps (~27,600 GPM, ~12 m head, 75% eff) | ~340–460 kW |
| Makeup, blowdown, chemical dosing, sump | ~55 kW |
| PHX auxiliary (valves, controls) | ~40 kW |
| **Total cooling tower MCC (campus)** | **~1,400 kW** |

### 8.7 Tower cells — Stage 1

| Parameter | Value | Status |
|---|---|---|
| Total duty | ~20,720 RT | W (C-17) |
| Configuration | 3 cells (2 duty + 1 spare) | W |
| Per-cell duty (design) | ~10,360 RT | W |
| **Estimated field footprint** | **~6,000 sq ft** | W |
| Infrastructure yard available | 28,000 sq ft | L |
| Remaining yard after towers | ~22,000 sq ft | W |

**Yard packing closes comfortably.** 3 cells fit within the 28,000 sq ft infrastructure yard; ~22,000 sq ft remaining for SCR, transformers, MV switchgear, service access.

### 8.8 Tower type (T-05 open)

| Option | Fit | Assessment |
|---|---|---|
| **Wet mechanical draft** | **Recommended basis** | Lowest capex; best approach to wet-bulb; ~747 GPM makeup manageable |
| Hybrid dry/wet | Contingency | 1.5–2× wet capex; 30–50% annual water reduction |
| Adiabatic | Not recommended | Peak-day limited by dry-bulb, not wet-bulb |
| Full dry | Rejected | Cannot maintain ≤34°C at 35°C design dry-bulb |

### 8.9 Vendor shortlist

SPX / Marley · BAC (Baltimore Aircoil) · Evapco. All US-manufactured. RFQ anchor pending T-05 decision. Updated basis: ~20,720 RT Stage 1 / ~41,440 RT Full Build; tower supply ≤34°C at 28°C WB; flow ~27,600 GPM Stage 1.

---

## 9. Open Engineering Items — Master List

C1 = must close, critical path · C2 = desirable, not blocking construction.

### 9.1 Items blocking RFQ / procurement

| ID | Description | Blocking What | Priority |
|---|---|---|---|
| **PHX-001** | Plate HX sizing + vendor RFQ (Alfa Laval / GEA / API) — ~72.9 MW Stage 1, approach ~14°C, CDU ≤45°C L C-04 | PHX vendor award; tower inlet/outlet temp confirmation | C1 |
| **E-31** | CO control strategy — oxidation catalyst; Title V Major Source acknowledgment | LDEQ Title V pre-app | C1 |
| **JW-RAD** | JW radiator sizing + vendor RFQ (~58,212 kW JW rejection at 61.5%) | CHP cascade JW path | C1 |
| Cat CSA | CG260-16 exhaust mass flow + temp at 61.5%; JW temp + flow; N-1 governor response; CO emissions | T-08 heat balance; JW-RAD sizing; E-31 baseline | C1 |
| T-05 | Cooling tower type selection (wet / hybrid / adiabatic) — ~72.9 MW GPU warm water basis | Tower RFQ | C1 |
| T-08 | CHP heat balance final — Munters (5.5 MW) + stack (~42 MW) + JW radiator (~58 MW) | JW-RAD sizing; ELEC-001 cooling MCC feeder | C1 |
| T-09 | Makeup water source — ~747 GPM / ~1.08 MGD; municipal vs well | LPDES pre-app; water permit | C1 |
| E-10 | Per-block BESS sizing validation vs CG260-16 governor ramp data | BESS RFQ vendor award | C1 |
| E-12 | PCS inverter vendor selection (Hitachi AMPS PCS / integrated with BESS) | BESS RFQ | C1 |
| E-13 | BESS container vendor selection (Fluence / LG / Saft) | BESS RFQ close | C1 |
| NFPA 855 AHJ | Lafayette Parish NFPA 855 (2026) interpretation | BESS AHJ submittal | C1 |
| E-24 / E-25 | Delta 660 kW rack RFQ; 5 per cassette preferred (73% loading, N-1 tolerance) | In-row rack procurement | C1 |
| E-8 | Block step-down transformer (13.8 kV → 480 V, ~15 MVA) RFQ | Transformer procurement | C1 |
| E-11 | Block MV switchgear vendor RFQ | MV switchgear procurement | C1 |
| E-22 | Solar PV inverter vendor RFQ (SMA / Sungrow / Power Electronics, 4-unit) | Solar procurement | C1 |
| **SITING-001** | Rear slab + infrastructure yard packing study — 42,000 sq ft rear slab undersized for 44 gensets + BESS | Genset + BESS layout | C1 |
| **WATER-SRC** | Makeup water source decision — ~747 GPM / ~1.08 MGD (Stage 1) | LPDES pre-app | C1 |
| **BLOWDOWN** | Blowdown disposal — ~249 GPM | LPDES pre-app | C1 |

### 9.2 Items blocking construction / downstream documents

| ID | Description | Priority |
|---|---|---|
| SLD-001 | Formal single-line diagram | C1 |
| PROT-001 | Protection coordination study | C1 |
| E-14 | Bus interconnect topology (E-23 — 11 independent vs tied) | C1 |
| SHPO R-05 / R-06 | Historic Tax Credit Part 1 / Part 2 filing | C1 |
| LDEQ LPDES | Pre-application (cooling tower blowdown only) | C1 |
| LDEQ Title V | Air permit pre-application — 44 gensets | C1 |
| LA ITEP | Filing before any construction | C1 |
| Gas supply lock | Pipeline interconnect, metering, contingency storage | C1 |
| NVIDIA allocation | Vera Rubin GPU allocation | C1 |

### 9.3 C2 items

| ID | Description | Priority |
|---|---|---|
| BOD-UPD | BOD T-04, T-06, R-03 update — river eliminated; confirmed Rev 0.6 | C2 |
| T-12a | Munters DSS Pro regen reconciliation | C2 |
| NOISE-VIS | Tower height, plume drift, fan noise — parish + SHPO | C2 |
| B-07 | Structural assessments B1–B4 | C2 |
| LAYOUT | Solar rooftop layout design | C2 |
| YIELD | Bankable energy yield study | C2 |
| ITC-DC | First Solar domestic content vs IRS requirements | C2 |
| MPPT | Multi-MPPT configuration per roof | C2 |
| ITC (BESS) | Domestic content verification | C2 |
| LG 23-ft | LG ES Vertech JF2 23-ft width logistics | C2 |
| A-05 / A-06 / A-07 | AI model vendor; human-in-loop policy; cybersecurity framework | C2 |
| C-25 | Immersion fluid vendor (GRC vs Submer — deferred) | C3 |
| Parish PILOT | Negotiation (below $200M threshold) | C2 |
| CATL | Section 301 tariff + ITC eligibility | C3 |

---

## 10. Document Register

### 10.1 Issued documents (current revisions)

| Doc # | File | Rev | Date | Status | Supersedes |
|---|---|---|---|---|---|
| ST-TRAP-BOD-001 | TRAP-BOD-001_Rev0.6.md | **0.6** | **2026-04-23** | Working draft — canonical | Rev 0.5 |
| ST-TRAP-THERMAL-BASIS | ST-TRAP-THERMAL-BASIS_Rev0.5.md | 0.5 | 2026-04-22 | Working draft — Rev 0.6 rebase in progress | Rev 0.4 |
| ST-TRAP-ELEC-001 | Trap-ELEC-001_Rev1.3.md | **1.3** | **2026-04-23** | Working draft — 480 VAC block bus architecture | Rev 1.2 |
| ST-TRAP-ARCHDIAG-001 (MD) | 03-Architecture/ST-TRAP-ARCHDIAG-001_Rev0.1.md | 0.1 | 2026-04-17 | Working draft — superseded architecture; rebuild pending | — |
| ST-TRAP-BESS-001 | TRAP-BESS-001_Rev0.1.md | ~~0.1~~ | 2026-04-17 | **Superseded by BOD Rev 0.6** — Rev 0.2 in progress | — |
| ST-TRAP-BESS-ARCHDIAG-001 | TRAP-BESS-ARCHDIAG-001_Rev0.1.md | ~~0.1~~ | 2026-04-17 | **Superseded by BOD Rev 0.6** — Rev 0.2 in progress | — |
| ST-TRAP-BESS-RFQ-001 | ST-TRAP-BESS-RFQ-001_Rev0.1.md | ~~0.1~~ | 2026-04-18 | **DO NOT DISTRIBUTE** — superseded architecture | — |
| ST-TRAP-CHP-SCHEMATIC-001 | 07-Thermal/ST-TRAP-CHP-SCHEMATIC-001_Rev0.2.md | **0.2** | **2026-04-22** | Working draft — Rev 0.3 rebase in progress | Rev 0.1 |
| ST-TRAP-COOLING-TOWER-001 | 07-Thermal/ST-TRAP-COOLING-TOWER-001_Rev0.2.md | **0.2** | **2026-04-22** | Working draft — Rev 0.3 rebase in progress | Rev 0.1 |
| ST-TRAP-SOLAR-001 | ST-TRAP-SOLAR-001_Rev0.1.md | ~~0.1~~ | 2026-04-18 | §1–§5 valid; **§6–§7 superseded** — Rev 0.2 in progress | — |
| ST-TRAP-MASTER-ENG-001 | TRAP-MASTER-ENG-001_Rev0.4.md (this doc) | **0.4** | **2026-04-23** | Working draft — cassette architecture reconciled | Rev 0.3 |

### 10.2 Pending / blocked documents

| Doc # | Description | Gate Conditions |
|---|---|---|
| ST-TRAP-SLD-001 | Formal single-line diagram | ELEC-001 Rev 1.3 current; Cat CSA, BESS vendor lock, solar PV inverter lock, E-14 inter-block tie decision |
| ST-TRAP-PROT-001 | Protection coordination study | SLD-001 draft; CT ratios, pickup settings, AC-DC boundary coordination |

### 10.3 Cancelled documents

| Doc # | Reason |
|---|---|
| ST-TRAP-RIVER-001 | Cancelled. Vermilion River eliminated as heat sink. |

---

## 11. Critical Path to Construction Package

Construction package gate: **SLD-001 + PROT-001**. Sequence unchanged from Rev 0.3 except solar step updated for PV inverter RFQ.

| # | Milestone | Depends On | Unblocks | Target |
|---|---|---|---|---|
| 1 | **Cat CSA engagement** — CG260-16 exhaust mass flow + temp at 61.5%, JW temp + flow, N-1 governor response, CO emissions | None | JW-RAD sizing; T-08; E-31 baseline | Scott / Cat |
| 2 | **PHX-001 plate HX sizing** — Alfa Laval / GEA / API RFQ; ~72.9 MW Stage 1 | C-04 L; C-17 W | PHX vendor award; tower inlet/outlet temp; tower RFQ | Scott |
| 3 | **JW radiator vendor RFQ + award** — ~58,212 kW JW rejection at 61.5% | Cat CSA JW data (Step 1) | JW rejection path lock | Scott |
| 4 | **T-05 cooling tower type decision** — wet / hybrid / adiabatic; ~72.9 MW basis | PHX-001 outlet temp (Step 2) | Tower RFQ (Step 5) | Scott |
| 5 | **Cooling tower vendor RFQ + award** — ~20,720 RT Stage 1 / ~41,440 RT Full Build; supply ≤34°C at 28°C WB; ~27,600 GPM Stage 1 | T-05 (Step 4); PHX sizing (Step 2) | Tower field procurement | Scott |
| 6 | **BESS vendor engagement + RFQ award** — Fluence preferred; Hitachi AMPS PCS in parallel on PCS layer | BOD Rev 0.6 AC-coupled basis; Cat governor data (Step 1 subset) | BESS container selection; PCS selection; BESS-001 Rev 0.2 | Scott |
| 7 | **Solar PV inverter RFQ (E-22)** — SMA / Sungrow / Power Electronics; 4-unit; 480 VAC output; grid-forming; First Solar engagement | SOLAR-001 Rev 0.2 | PV inverter vendor lock; SOLAR-001 Rev 0.2 | Scott / First Solar |
| 8 | **Delta in-row rack RFQ (E-24 / E-25)** — 5 racks/cassette preferred; N-1 tolerance | None | In-row rack procurement | Scott / Delta |
| 9 | **Block MV switchgear + step-down transformer RFQs (E-8, E-11)** | ELEC-001 Rev 1.3 (Cat voltage confirmed — Step 1) | MV switchgear + transformer procurement | Scott |
| 10 | **CO oxidation catalyst vendor RFQ (E-31)** — 44 CG260-16 gensets; >90% CO destruction | Cat CSA emissions data (Step 1) | Title V air permit path | Scott |
| 11 | **BOD-001 Rev 0.7 trigger** — Cat CSA preliminary data applied; T-08 close | T-08; Cat CSA preliminary (Step 1) | Downstream documents re-cite BOD Rev 0.7 | Scott |
| 12 | **SHPO Part 1 filing (R-05)** | — | Historic review initiated; HTC 45% stack preserved | Scott / SHPO |
| 13 | **LDEQ LPDES pre-application** — cooling tower blowdown only (~249 GPM) | T-05 (Step 4); BLOWDOWN decision | Water / thermal design lock | Scott / LDEQ |
| 14 | **LDEQ Title V pre-application** — 44-genset air emissions; CO catalyst included | Cat CSA data (Step 1); CO catalyst RFQ (Step 10) | Air emissions design lock | Scott / LDEQ |
| 15 | **LA ITEP filing** — before any construction | BOD Rev 0.6+ | Construction kickoff | Scott / LED |
| 16 | **Gas supply lock** — firm pipeline capacity for 100% contingency (~40,300 Nm³/hr campus) | Gas utility engagement | Block 1 energization | Scott / gas utility |
| 17 | **NFPA 855 AHJ pre-application** | BESS vendor compliance docs (Step 6); SITING-001 | BESS setback study; layout lock | Scott / AHJ |
| 18 | **SITING-001 packing study** — rear slab 42,000 sq ft; infrastructure yard ~6,000 sq ft for CT cells | — | Construction sequencing; BESS NFPA 855 setbacks | Scott / layout engineer |
| 19 | **Structural assessments B1–B4 (B-07)** | — | Rooftop solar loading lock; HTC Part 2 inputs | Scott / structural |
| 20 | **E-14 inter-block tie decision** | Contingency analysis; BESS sizing (Step 6) | ELEC-001 Rev 1.4 advance; SLD-001 routing | Scott |
| 21 | **SLD-001 draft** — formal single-line inheriting ELEC-001 Rev 1.3 | Steps 1, 6, 7, 8, 9, 20 closed | PROT-001 input | Scott |
| 22 | **PROT-001 draft** — protection coordination study | SLD-001 (Step 21) | **Construction package gate** | Scott / protection engineer |

### 11.1 BOD-001 revision trigger summary

| BOD Rev | Trigger | Sequence step |
|---|---|---|
| 0.6 (issued 2026-04-23) | Cassette architecture reconciled; 480 VAC block bus; 91.1 MW IT load; AC-coupled BESS/solar | Complete |
| 0.7 | Cat CSA validation complete; CO emissions locked; T-08 heat balance final | After Steps 1 + 11 |
| 0.8 | LDEQ LPDES pre-application returns | After Step 13 |
| 0.9 | SHPO Part 1 filing | After Step 12 |
| 1.0 | All C1 external dependencies locked | After Steps 1–22 closed |

### 11.2 Construction package gate

SLD-001 Rev 1.0 + PROT-001 Rev 1.0 paired with THERMAL-BASIS Rev 1.0, COOLING-TOWER-001 Rev 1.0, BESS-001 Rev 1.0, SOLAR-001 Rev 1.0, CHP-SCHEMATIC-001 Rev 1.0, and BOD-001 Rev 1.0. All C1 items per §9.1 and §9.2 closed.

---

**End of ST-TRAP-MASTER-ENG-001 Rev 0.4.**
