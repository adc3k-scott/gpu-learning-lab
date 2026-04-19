# ST-TRAP-MASTER-ENG-001 — Master Engineering Package — Rev 0.1

**Document:** Master Engineering Package — Trappey's AI Center
**Project:** Trappey's AI Center — 22-acre historic cannery site, Vermilion River, Lafayette, Louisiana
**Revision:** 0.1 — first issue, consolidated summary of current engineering state
**Date:** 2026-04-18
**Owner:** Scott Tomsu
**Status:** Working draft — internal use only
**Authority:** BOD-001 Rev 0.4 governs all locked values. This document consolidates the current state of downstream engineering documents; all value changes flow through BOD-001.

L = Locked · W = Working · O = Open

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

**Thermal architecture** is a CHP cascade: genset exhaust + jacket water drives Broad BH double-effect LiBr absorption chillers (Option B working basis; Option C exhaust-direct retained as contingency pending Cat CSA). Munters HCD/MCD desiccant dehumidification per cassette draws 125 kW exhaust slip-stream per cassette (5.5 MW Stage 1, Locked T-12). **Cooling towers are the sole and primary heat rejection path** — not residual. Vermilion River is eliminated as heat sink (tidal reversal + summer Gulf Coast ambient 30–33°C exceeding Broad's 29°C rated condenser inlet). Boyd CDU GPU warm water is an isolated loop rejecting to a separate adiabatic dry cooler.

**Why this approach:** BTM permanent island removes the primary reliability dependency on LUS and eliminates interconnect schedule risk. 11-block replicated Marlie-pattern architecture contains blast radius to one block and enables phased construction with standardized procurement. CHP cascade converts genset waste heat into cooling (COP ~1.40 operating, coverage >100% of campus demand), eliminating auxiliary chiller capex and fuel burn. DC-coupled BESS + DC-coupled solar + DC rectification on one 800 VDC bus per block matches OCP Stage 1d / NVIDIA DSX reference architecture. Zero utility dependency is the thesis.

---

## 2. Site & Project Basis

Source: BOD-001 Rev 0.4.

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
5. **16 × Delta 660 kW in-row power racks** (4 per cassette base spec) — AC-DC conversion, BBU + PCS, 98% efficiency, touch-safe 800 VDC output.
6. **Block 800 VDC common busway** — copper, ~12,075 A at 9.66 MW full block load. Single DC bus per block carries rack outputs + BESS + solar + 4 cassette umbilicals.
7. **4 cassette umbilicals** — load-break contactor + SSCB → 800 VDC cable → Staubli hot-swap disconnect at cassette (~3,000 A at 2,415 kW).

11 electrically independent blocks. No inter-block MV ring. No inter-block 800 VDC tie (E-23 deferred). Shared services (gas header, water plant, NOC, security, AMCL) span the campus but do not carry power between blocks.

### 3.2 Genset specification — Cat CG260-16

| Parameter | Value | Status |
|---|---|---|
| Rated output | 4,000 ekW continuous, 60 Hz, 900 rpm | L |
| Electrical efficiency | 43.8% (LHV) | L |
| Thermal efficiency | 42.4% (LHV to 120°C) | L |
| Total efficiency | 86.2% | L |
| NOx | <250 mg/Nm³ at 5% O₂ | L |
| Hydrogen blending | 25% blend capable at same continuous rating | L (future optionality) |
| Design anchor loading | 61.5% (2,460 ekW per genset) | W — pending Cat CSA |
| AI dispatch envelope | 55–75%; 63–65% expected average | W |
| MV voltage | 13.8 kV | W — Cat CSA to confirm |
| Fuel | ~2,200 Nm³/hr per block full load; ~24,000 Nm³/hr Stage 1 campus | W |

**Prime mover rule:** CG260-16 for Trappey's and 100+ MW deployments; Cat G3520K for Marlie 1 and ≤10 MW platforms. Not substitutable.

### 3.3 Five feeder categories (E-29, per block)

| Feeder | Load | Notes |
|---|---|---|
| 16 × Delta 660 kW in-row power racks | ~10.6 MVA | Dominant feeder — 4 racks × 4 cassettes |
| Cooling plant MCC | ~600 kW | VFD-driven (per-block estimate; actual campus cooling MCC ~4,800 kW likely centralized — see §8.5) |
| BESS auxiliary | ~80 kW | Battery HVAC, BMS, fire system |
| Solar DC-DC buck auxiliary | ~10 kW | Controls, HVAC |
| Facility ancillary | ~200 kW | SCADA, NOC, site lighting, fire/life safety |

### 3.4 Protection (island-only, DC-dominated)

- **Per-genset (E-26):** 87G differential, 32 reverse power, 40 loss of field, 46 negative sequence, 47 phase sequence, 59/27 over/under-voltage, 64G stator ground, 78 out-of-step, 51V voltage-restrained overcurrent.
- **Block bus:** 87B bus differential, 51N neutral ground.
- **Transformer (E-27):** 87T primary + 87T secondary, 49T thermal (RTD), 63 pressure/gas.
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
| Generation at 63–65% operational | ~122.8 MW | ~245.6 MW | W |
| Block cassette facility load | 9.66 MW | 9.66 MW | L |
| Non-cassette ancillary | ~3–5 MW | ~6–10 MW | W |
| **Total Stage 1 site load** | **109.3–111.3 MW** | — | W |

Stage 1 design-anchor margin vs cassette facility load is −1 to −3 MW; operational loading at 63–65% closes this comfortably. Design anchor 61.5% is retained for Cat longevity discussions.

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
| Extreme cold record | −5°C | ~1,074V | ~1,280V | ✓ within |

String MPP stays above 800V across the full Louisiana temperature range; string Voc stays below 1,500V in all conditions. No seasonal reconfiguration required. Total array current at MPP = 2,155 A at ~952V.

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

Source: ST-TRAP-THERMAL-BASIS Rev 0.4.

### 6.1 Architecture summary

**CHP cascade (Locked, T-01):** genset waste heat (exhaust + jacket water) drives LiBr absorption chillers. Chillers produce chilled water for facility cold distribution (Munters cooling side, NOC, offices, electrical rooms). Absorption chiller condenser + absorber circuit rejects through cooling tower field. Boyd CDU GPU warm water loop is a physically and thermally separated circuit rejecting through a dedicated adiabatic dry cooler.

### 6.2 Option B (working basis) vs Option C (contingency)

| Option | Architecture | Status |
|---|---|---|
| **Option A — single-stage direct-fired** | Gas-to-cold; wastes CHP advantage. Rated COP 1.42. **Eliminated** — architecturally incompatible with CHP cascade. | Eliminated |
| **Option B — double-effect hot-water (Broad BH via HRU)** | Exhaust → plate-fin HRU (Cain / E-Tech / Rentech TBD) → 180°C hot water → Broad BH two-stage LiBr → 6.7°C chilled water. COP rated 1.50; operating estimate 1.40. Full drive temp match from any exhaust ≥200°C. | **Working basis** |
| **Option C — exhaust-direct (Broad BE / BZE multi-energy)** | Direct exhaust duct to Broad BE two-stage LiBr. Rated exhaust inlet 500°C; CG260-16 estimated 372–420°C → **80–128°C gap**. COP and capacity derating TBD via Broad app eng. BZE supplements with direct-fired gas burner to bridge gap. | Contingency |

**TB-5 resolution:** gates on (1) Cat CSA confirming CG260-16 exhaust temperature and mass flow at 61.5% load and (2) Broad / Thermax application engineering confirming derating curve for Option C. If Cat CSA confirms exhaust ≥450°C, Option C becomes more attractive. If 372–380°C, Option B is thermally superior because the HRU can efficiently extract to 120°C leaving temperature regardless of the 500°C rated threshold.

Until Cat CSA is received, **Option B is the working architecture for all downstream sizing**.

### 6.3 Munters desiccant deduction (T-12, Locked)

Each cassette houses one Munters HCD/MCD unit drawing 125 kW exhaust slip-stream for desiccant regeneration. Louisiana wet-bulb (28°C ASHRAE 0.4%) and 75–80% RH annual average make desiccant dehumidification **an architectural constraint, not a feature option**.

| Parameter | Value | Status |
|---|---|---|
| Munters per cassette | 125 kW | L (T-12) |
| Stage 1 deduction (44 cassettes) | 5,500 kW | L |
| Full Build deduction (88 cassettes) | 11,000 kW | L (T-13) |

### 6.4 Cooling tower = primary heat rejection (not residual)

**Vermilion River is eliminated as heat sink.** Two disqualifying conditions:

1. **Tidal influence** — bidirectional flow at Lafayette; during reversal events effective mixing volume for regulated thermal discharge drops to near-zero or reverses.
2. **Ambient water temperature** — Gulf Coast surface water peaks at 30–33°C (86–91°F) in summer, exceeding Broad's 29°C rated condenser water inlet. River cannot provide meaningful ΔT for heat rejection during peak cooling demand months.

**Consequence:** ST-TRAP-RIVER-001 cancelled. LPDES thermal discharge permit not required. BOD T-04 ("residual rejection"), T-06 ("Vermilion River supplemental"), and R-03 require update at next BOD revision.

**Water tower nomenclature clarification:** the historic water tower on site (pressurized storage tank from original cannery operation) is currently inoperable and under consideration for restoration as a site landmark. It has **no role in the thermal system**. The cooling towers referenced throughout are purpose-built new mechanical-draft evaporative heat rejection units. No relation.

### 6.5 Boyd CDU GPU warm water loop — isolated

| Parameter | Value | Status |
|---|---|---|
| Supply to GPU | ≤45°C | L (BOD C-03) |
| Return from GPU | ~50–55°C | W |
| Heat rejection path | Separate adiabatic dry cooler (not cooling towers) | L |
| Per-cassette heat | 1,840 kW (C-17) | L |
| Stage 1 total | ~80,960 kW | L |
| Thermal isolation | No shared basin, header, or piping with absorption chiller condenser circuit | L |

### 6.6 CHW compatibility (T-11 open)

T-11 confirms whether any Boyd CDU sub-loop requires 7–12°C chilled water input. If Boyd CDU supply is a closed warm-water loop with no tie to the 7°C chiller, T-11 resolves by separation. Priority C1 — gates cooling loop mechanical design. Resolution path: Boyd CDU application engineering call.

### 6.7 Key open items

| Ref | Item | Priority |
|---|---|---|
| TB-5 | Absorption chiller type (Option B / C) | C1 |
| T-03 | Chiller type selection in BOD ledger | C1 |
| T-08 | CHP heat balance final values | C1 |
| T-11 | Boyd CDU CHW supply compatibility | C1 |
| Cat CSA | CG260-16 exhaust temperature, mass flow, part-load curves | C1 |
| HRU-RFQ | Exhaust HRU vendor RFQ (Cain / E-Tech / Rentech) — backpressure binding | C1 |
| COND-WB | Broad chiller app eng confirmation at 30–31°C condenser water inlet | C1 |

---

## 7. CHP Cascade

Source: ST-TRAP-CHP-SCHEMATIC-001 Rev 0.1. Working basis Option B.

### 7.1 End-to-end chain (with key numbers at each node)

```
44 × Cat CG260-16 (61.5% loading)
  · Electrical output: 108,240 kW (W)
  · Waste heat total: ~106,084 kW (W)
  · Exhaust: ~47,872 kW at 372–420°C est. (W)
  · Jacket water: ~58,212 kW at ≤99°C outlet (W)
    ↓
Exhaust header splits:
  · → Munters slip-stream (5,500 kW, L T-12) → desiccant regen → cassettes ≤50% RH
  · → Exhaust HRU (plate-fin; ~42,372 kW, W; Option B)
       └→ stack ~120°C leaving → atmosphere
       └→ 180°C / 165°C hot water
            ↓
JW recovery (detail TBD) → JW supplement to hot water header (robust across block genset trip)
    ↓
Absorption drive header ~100,584 kW net (W; after Munters deduction)
    ↓
Broad BH two-stage LiBr double-effect chiller
  · Rated COP 1.50; operating COP 1.40 (W, part-load derate)
  · Chilled water 6.7°C supply / 13.7°C return → facility cold distribution (Munters cooling side, NOC, offices, electrical rooms)
  · Absorption cooling produced: ~140,818 kW (W)
  · Campus cooling demand: ~107,300 kW (W)
  · Coverage: >100% — chiller staging required (fewer units at higher load, not all at minimum)
  · Condenser + absorber out: 37°C
    ↓
Condenser water circuit (~114,400 GPM max, VFD pumps N+1)
    ↓
Cooling tower field (wet mechanical draft, T-05 open; SPX/Marley · BAC · Evapco)
  · Design WB 28°C ASHRAE 0.4% (L)
  · Maximum duty 241,402 kW (241.4 MW) / 68,640 RT (W)
  · Nominal staged duty ~183,943 kW (183.9 MW) / 52,310 RT (W)
  · Supply ≤31°C at 28°C WB, 3°C approach (W; COND-WB open)
    ↓
Atmosphere (evaporation + sensible)
```

### 7.2 Heat Balance Summary — Stage 1 Campus, Option B, 61.5% Load (verbatim from CHP-SCHEMATIC-001)

| Stream | kW | Status | Disposition |
|---|---|---|---|
| Electrical generation (44 gensets) | 108,240 | W | IT + facility + aux |
| IT load (44 cassettes) | 101,200 | L | GPU compute |
| Facility aux (NOC, offices, controls) | ~6,100 | W | Facility load |
| **Total waste heat — exhaust + JW** | **~106,084** | **W** | → recovery cascade |
| Munters slip-stream (T-12 LOCKED) | 5,500 | L | → desiccant regen |
| Net to absorption chiller | ~100,584 | W | → Broad BH drive |
| Absorption COP (Option B, operating) | 1.40 | W | — |
| Absorption cooling produced (max) | ~140,818 | W | > campus demand |
| Campus cooling demand (IT + overhead) | ~107,300 | W | Staged chiller output |
| **Condenser + absorber rejection — nominal** | **~183,943** | **W** | → cooling towers |
| **Condenser + absorber rejection — maximum** | **~241,402** | **W** | → cooling towers (design sizing) |
| GPU warm water (Boyd CDU) | ~80,960 | L (C-17) | → adiabatic dry cooler (separate) |
| Stack exhaust (after HRU extraction) | TBD | O | → atmosphere via stack |
| Cooling tower makeup water | ~2,476 GPM | W | → evaporation + blowdown |

**Key finding:** all campus cooling demand met by absorption cooling alone under Option B at 61.5% genset load. No grid, no river, no auxiliary chiller required.

### 7.3 Option B vs C branch (TB-5)

Everything downstream of the chiller is identical under both options. TB-5 is the only structural topology decision in the CHP cascade. Decision gates:

| Trigger | Action |
|---|---|
| Cat CSA confirms exhaust ≥450°C at 61.5% load | Option C (Broad BE direct) becomes viable; re-evaluate |
| Cat CSA confirms exhaust 372–380°C | Option B locks (HRU produces 180°C hot water regardless of Broad BE's 500°C rated threshold) |
| Backpressure budget (Cat limit 6.7 kPa) | Option B HRU adds 2.0–2.5 kPa; with oxidation catalyst + Munters tee + stack, total 3.5–4.9 kPa with 1.8–3.2 kPa margin (27–48%) |

### 7.4 Component status

| Component | Status | Notes |
|---|---|---|
| Cat CG260-16 genset | L (count, rating); W (61.5% loading, voltage option) | Cat CSA pending |
| Munters slip-stream 5.5 MW | L (T-12) | Locked per BOD |
| Exhaust HRU (Option B) | O (vendor) | Cain / E-Tech / Rentech — RFQ required |
| JW integration detail | O | Direct header supplement vs separate PHE cascade vs separate single-effect stage |
| Broad BH double-effect chiller | W (Option B working) | TB-5 open |
| Condenser water circuit | W | Flow, temps, COND-WB pending |
| Cooling tower field | W (type, T-05 open) | Wet mechanical draft recommended basis |
| Boyd CDU + adiabatic dry cooler | L (Boyd CDU per C-03); O (dry cooler vendor) | Isolated from absorption circuit |

---

## 8. Cooling Tower Field

Source: ST-TRAP-COOLING-TOWER-001 Rev 0.1.

### 8.1 System boundary

The cooling tower field serves **one circuit exclusively**: the absorption chiller condenser + absorber cooling water loop. **Continuous full-load duty**, not peak-day supplement.

**Not served:** Boyd CDU GPU warm water (separate adiabatic dry cooler; ~81 MW from 44 × 1,840 kW). Thermal cross-contamination prevented — separate circuits, separate equipment, no shared basin or header.

### 8.2 Thermal duty

| Parameter | Value | Status |
|---|---|---|
| **Maximum duty (design sizing basis)** | **241,402 kW / 241.4 MW / 68,640 RT** | W |
| **Nominal staged duty** | **~183,943 kW / 183.9 MW / 52,310 RT** | W |
| Turndown ratio (nominal / maximum) | 76.2% | W |

Maximum duty = all absorption chillers operating at max capacity against full available drive heat (100,584 kW × COP 1.40 = 140,818 kW cooling produced; condenser + absorber rejection = 241,402 kW). Nominal = chillers staged to match actual campus cooling demand (107,300 kW).

**Excess drive heat at nominal:** ~23,941 kW (100,584 available − 76,643 consumed) managed through chiller staging (fewer units at higher loading) or trim heat exchanger (piping design item).

### 8.3 Condenser water circuit

| Parameter | Value | Status |
|---|---|---|
| Supply (tower outlet → chiller inlet) | ≤29°C rated; **≤31°C derating case** | W |
| Return (chiller outlet → tower inlet) | 37°C | W |
| Temperature range (ΔT) | 8°C (14.4°F) | W |
| Circulating flow — maximum duty | ~7,220 L/s / ~114,400 GPM | W |
| Circulating flow — nominal duty | ~5,500 L/s / ~87,200 GPM | W |

### 8.4 Approach temperature gap — COND-WB open

At ASHRAE 0.4% Lafayette wet-bulb (28°C):
- Broad BH rated condenser inlet: **29°C** → required tower approach 1°C (not achievable economically with commercial mechanical-draft towers)
- Standard 3°C approach: **31°C** condenser water supply → **2°C above Broad rated inlet**
- Standard 5°C approach: 33°C → 4°C above rated

**Not a project-stopper.** Absorption chillers operate above rated CW temperature with predictable capacity / COP derating (expected 3–5% at 2°C above rated). Existing >100% absorption coverage margin absorbs derating without impact to campus cooling reliability.

**COND-WB resolution:**
1. Broad / Thermax application engineering confirms operating envelope at 30–31°C CW inlet.
2. RFQ specifies supply ≤31°C at 28°C WB, 3°C approach as binding performance point.
3. Broad confirmation is pre-award condition on chiller RFQ (TB-5).
4. If Broad imposes stricter CW limit: re-evaluate for ≤2°C approach (larger tower, higher capex) vs alternative chiller vendor with higher rated CW tolerance.

### 8.5 Water consumption (wet tower, maximum duty)

| Parameter | Value | Basis |
|---|---|---|
| Evaporation rate | ~1,650 GPM | ~1.44% of circulation at 14.4°F range |
| Cycles of concentration (design) | 3.0 | Industry standard municipal water |
| Blowdown rate | ~825 GPM | Evaporation / (COC − 1) |
| Drift loss | ~1 GPM | 0.001% with eliminators |
| **Total makeup — maximum duty** | **~2,476 GPM (~3.57 MGD)** | Sum |
| Total makeup — nominal | ~1,888 GPM (~2.72 MGD) | Scaled 76.2% |

Makeup water source open (municipal / on-site well / Vermilion River intake). Vermilion intake for makeup is a **separate permit path** from the cancelled RIVER-001 thermal discharge (LDEQ intake permit if volume significant).

### 8.6 Electrical — cooling plant MCC

| Item | Working Value |
|---|---|
| Tower fan motors (all cells) | ~3,000 kW (1–1.5% of 241 MW rejected) |
| Condenser water pumps | ~1,400–1,900 kW (7,220 L/s, ~15–20 m head, 75% eff) |
| Makeup, blowdown, chemical dosing, sump | ~200 kW |
| **Total cooling tower MCC (campus)** | **~4,800 kW** |

**Note on BOD E-29:** E-29 allocates ~600 kW per block × 11 = 6,600 kW campus. The ~4,800 kW estimate above is consistent as an order-of-magnitude check. E-29 was written before absorption chiller condenser load was fully sized. Cooling tower MCC likely a single centralized campus switchboard fed from the Power Hall, not distributed per-block — architectural decision open for SLD-001.

### 8.7 Tower type (T-05 open)

| Option | Fit | Assessment |
|---|---|---|
| **Wet mechanical draft (W)** | **Recommended basis** | Lowest capex; best approach to wet-bulb; highest water (~2,476 GPM makeup); LPDES blowdown required; standard Legionella management |
| Hybrid dry/wet (H) | Contingency | 1.5–2× wet capex; 30–50% annual water reduction; Lafayette wet-bulb rarely below 24°C limits dry-mode hours Nov–Feb only; candidate if LPDES blowdown or municipal water cost becomes binding |
| Adiabatic (A) | Not recommended | Highest capex; peak-day limited by 35°C dry-bulb (not wet-bulb); cannot maintain ≤31°C CW on peak without extreme oversizing |
| Full dry | Rejected | Cannot maintain ≤31°C CW at 35°C design dry-bulb at economic scale |

### 8.8 Siting — 28,000 sq ft yard flag

Reference tower sizing: SPX/Marley NC or BAC Series 3000 counterflow at 10,000–12,000 RT occupies ~60 × 30 ft. For 68,640 RT total:
- 6–7 units + N+1 spare
- Estimated field footprint ~200 × 100 ft
- Infrastructure yard (28,000 sq ft ≈ 167 × 168 ft) **at or below the lower limit** for cooling tower field alone, before transformers and switchgear

**Rear slab (42,000 sq ft) may need to provide overflow tower positions.** SITING-001 is a C2 deliverable required before tower RFQ.

### 8.9 Vendor shortlist

| Vendor | Key Products | Notes |
|---|---|---|
| SPX / Marley | NC counterflow, FXV fluid cooler, Ultracool hybrid | Widest RT range; US-manufactured |
| BAC (Baltimore Aircoil) | Series 3000 counterflow, ICC, Hybrid Cooler | Strong CHP + industrial experience |
| Evapco | AT, UT; hybrid AMC; LSTA low-profile | US-manufactured; DOE pump efficiency compliant |
| Brentwood Industries | PVC fill media — component supplier | Not a packaged tower vendor |

RFQ anchor conditions pending T-05 decision and COND-WB close.

---

## 9. Open Engineering Items — Master List

Consolidated across all documents. Priority: **C1 = must close, critical path** (blocks construction package or procurement); **C2 = desirable, not blocking construction**.

### 9.1 Items blocking RFQ / procurement (must close before vendor award)

| ID | Description | Blocking What | Source Doc | Priority |
|---|---|---|---|---|
| TB-5 | Absorption chiller RFQ — Option B or C selection | THERMAL-BASIS → architecture lock; gates HRU and chiller specs | THERMAL-BASIS §7; CHP-SCHEMATIC §OpenItems | C1 |
| Cat CSA | CG260-16 exhaust temp, mass flow, part-load heat rejection curves at 61.5% load | TB-5; T-08 heat balance; E-5/E-6 voltage and governor confirmation | THERMAL-BASIS §11; ELEC-001 §15; BOD-001 §M | C1 |
| HRU-RFQ | Exhaust HRU vendor RFQ (Cain / E-Tech / Rentech) — backpressure binding | Option B cascade lock | THERMAL-BASIS §11 | C1 |
| COND-WB | Broad chiller app eng confirmation — condenser water inlet at 30–31°C | Cooling tower CW supply spec; chiller RFQ pre-award | COOLING-TOWER-001 §6; THERMAL-BASIS §11 | C1 |
| T-05 | Cooling tower type selection (wet / hybrid / adiabatic) | Tower RFQ | COOLING-TOWER-001 §7; BOD-001 T-05 | C1 |
| T-08 | CHP heat balance final values — JW + exhaust recovery, Munters applied | Cooling tower sizing lock; ELEC-001 §6 cooling MCC feeder | THERMAL-BASIS §11 | C1 |
| T-11 | Boyd CDU CHW supply 7–12°C compatibility | Cooling loop mechanical design | THERMAL-BASIS §8; BOD-001 T-11 | C1 |
| E-10 | Per-block BESS sizing validation (3.6 MWh working, 3–5 MWh envelope) | BESS RFQ vendor award | BESS-001 §13; ELEC-001 §15 | C1 |
| E-12 | Bidirectional DC-DC converter vendor selection | BESS RFQ | BESS-001 §13 | C1 |
| E-13 | BESS container vendor selection (Fluence / LG / Saft) | BESS RFQ close | BESS-001 §13 | C1 |
| NFPA 855 AHJ | Lafayette Parish AHJ NFPA 855 (2026) interpretation | BESS AHJ submittal; setback lock | BESS-001 §13; BESS-RFQ-001 §13 | C1 |
| E-24 / E-25 | Delta 660 kW rack RFQ; 4 vs 5 per cassette; lead times at 10 and 100+ quantities | In-row rack procurement | ELEC-001 §15 | C1 |
| E-8 | Block step-down transformer (13.8 kV → 480 V, ~15 MVA) RFQ | Transformer procurement | ELEC-001 §15 | C1 |
| E-11 | Block MV switchgear vendor RFQ | MV switchgear procurement | ELEC-001 §15 | C1 |
| E-22 | Solar DC-DC buck converter vendor RFQ (Delta preferred, 4-unit) | Solar procurement | SOLAR-001 §12 | C1 |

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
| SITING-001 | Cooling tower field siting study — 28,000 sq ft yard vs full field footprint | Tower vendor RFQ layout | COOLING-TOWER-001 §11 | C2 |
| WATER-SRC | Makeup water source (municipal / well / Vermilion intake) | LPDES pre-app | COOLING-TOWER-001 §11 | C2 |
| BLOWDOWN | Blowdown disposal (POTW / Vermilion intake / evaporation pond) | LPDES pre-app | COOLING-TOWER-001 §11 | C2 |
| CRYST-MIN | Minimum CW supply temp to chiller (LiBr crystallization floor) | Tower control constraint | COOLING-TOWER-001 §11 | C2 |
| NOISE-VIS | Tower height, plume drift, fan noise — parish + SHPO | Tower submittal | COOLING-TOWER-001 §11 | C2 |
| B-07 | Structural assessments B1–B4 | Rooftop solar loading; interior retrofit | BOD-001 B-07; SOLAR-001 §4 | C2 |
| LAYOUT | Solar rooftop layout design — panel placement, walkways, HVAC clearances | Solar installation | SOLAR-001 §12 | C2 |
| YIELD | Bankable energy yield study (P50/P90) | Solar financial model | SOLAR-001 §12 | C2 |
| ITC-DC | First Solar domestic content vs IRS requirements | Solar ITC basis confirmation | SOLAR-001 §12 | C2 |
| MPPT | Multi-MPPT configuration — independent zones per roof | Solar DC-DC design | SOLAR-001 §12 | C2 |
| ITC (BESS) | Domestic content verification — Saft (France) vs LG (Holland MI) | BESS ITC basis | BESS-001 §13 | C2 |
| HITACHI | Hitachi AMPS compatibility with shortlisted BESS packs | DC-DC vendor selection | BESS-001 §13 | C2 |
| PHYS (BESS) | Rear slab NFPA 855 setback study | BESS container positions | BESS-001 §13; BESS-RFQ-001 §13 | C2 |
| LG 23-ft | LG ES Vertech JF2 23-ft width logistics | LG selection feasibility | BESS-RFQ-001 §13 | C2 |
| A-05 / A-06 / A-07 | AI model vendor; human-in-loop policy; cybersecurity framework (NIST CSF / IEC 62443) | Ops design | BOD-001 §I | C2 |
| C-25 | Immersion fluid vendor (GRC vs Submer — deferred, future rev) | Cassette future revision | BOD-001 C-25 | C3 |
| Parish PILOT | Negotiation (below $200M threshold, pursued vs HB 827) | Tax structure | BOD-001 §M | C2 |
| CATL | Section 301 tariff + ITC eligibility | CATL re-entry consideration | BESS-001 §13 | C3 |

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
| ST-TRAP-MASTER-ENG-001 | ST-TRAP-MASTER-ENG-001_Rev0.1.md (this doc) | 0.1 | 2026-04-18 | Working draft — internal use only | — |

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

The construction package gate is **SLD-001 + PROT-001**. The following milestone sequence is required to reach that gate.

| # | Milestone | Depends On | Unblocks | Target Owner |
|---|---|---|---|---|
| 1 | **Cat CSA engagement** — CG260-16 exhaust temp, mass flow, part-load heat rejection curves at 61.5%, voltage option confirmation, governor characterization | None (engagement in hand) | TB-5 (Option B/C lock); T-08 heat balance final; E-5/E-6 voltage and governor; THERMAL-BASIS Rev 0.5; ELEC-001 Rev 1.3 | Scott / Cat |
| 2 | **Broad / Thermax app eng — COND-WB** | Preliminary Cat exhaust data (sufficient for derating analysis) | Condenser water inlet envelope at 30–31°C; cooling tower RFQ binding spec lock; TB-5 Option B viability confirmation | Scott / Broad / Thermax |
| 3 | **TB-5 resolution** — absorption chiller Option B or C selection | Cat CSA (Step 1) + Broad app eng (Step 2) | CHP-SCHEMATIC-001 Rev 0.2 (contingency branch removed); THERMAL-BASIS Rev 0.5; chiller RFQ issue | Scott |
| 4 | **T-05 cooling tower type decision** — wet / hybrid / adiabatic | Water cost analysis + LPDES blowdown disposal review | Cooling tower RFQ issue to SPX/Marley / BAC / Evapco; COOLING-TOWER-001 Rev 0.2 | Scott |
| 5 | **HRU vendor RFQ + award (Option B path)** — Cain / E-Tech / Rentech; backpressure binding ≤6.7 kPa Cat | TB-5 (Step 3) closing on Option B; Cat exhaust mass flow confirmed | Exhaust cascade lock; CHP-SCHEMATIC-001 Rev 0.3 | Scott |
| 6 | **Absorption chiller vendor RFQ + award** — Broad BH (Option B) or BE/BZE (Option C) | TB-5 (Step 3); HRU award (Step 5 if Option B); COND-WB confirmation | Chiller selection lock; THERMAL-BASIS Rev 0.6 | Scott |
| 7 | **Cooling tower vendor RFQ + award** | T-05 (Step 4); T-08 heat balance; COND-WB confirmation (Step 2); SITING-001 study | Tower field procurement; COOLING-TOWER-001 Rev 1.0 | Scott |
| 8 | **BESS vendor engagement + RFQ award** — Fluence (preferred) → LG ES Vertech → Saft; Hitachi AMPS in parallel on DC-DC layer | BESS-RFQ-001 Rev 0.1 distribution (done); Cat governor preliminary data (Step 1 subset) | BESS container selection (E-13); DC-DC converter selection (E-12); per-block sizing lock (E-10); BESS-001 Rev 0.3 | Scott |
| 9 | **First Solar engagement + DC-DC buck RFQ (E-22)** — Delta preferred, 4-unit configuration; First Solar pricing via New Iberia factory proximity | SOLAR-001 Rev 0.1 (done); multi-year offtake portfolio framing | DC-DC vendor lock; SOLAR-001 Rev 0.2; solar module purchase order | Scott / First Solar / Delta |
| 10 | **Delta in-row rack RFQ (E-24 / E-25)** — 4 vs 5 per cassette; 10-unit and 100+ unit lead times | None (procurement-ready today) | In-row rack procurement; ELEC-001 Rev 1.4 | Scott / Delta |
| 11 | **Block MV switchgear + step-down transformer RFQs (E-8, E-11)** | ELEC-001 Rev 1.3 (Cat voltage confirmed — Step 1) | MV switchgear + transformer procurement | Scott |
| 12 | **BOD-001 Rev 0.5 trigger** — CHP heat balance with Munters slip-stream + Cat CSA data applied; updates T-03, T-08, F-section | T-08 close (Step 3 supporting); Cat CSA data (Step 1) | Downstream documents re-cite BOD Rev 0.5 | Scott |
| 13 | **SHPO Part 1 filing (R-05)** | — | Historic review initiated; HTC 45% stack preserved | Scott / SHPO |
| 14 | **LDEQ LPDES pre-application** — cooling tower blowdown only (river discharge cancelled) | T-05 (Step 4); BLOWDOWN path decision; WATER-SRC decision | Water / thermal design lock; BOD-001 Rev 0.7 | Scott / LDEQ |
| 15 | **LDEQ Title V pre-application** — 44-genset air emissions | Cat CSA emissions data (Step 1) | Air emissions design lock | Scott / LDEQ |
| 16 | **LA ITEP filing** — before any construction | BOD Rev 0.5+ | Construction kickoff | Scott / LED |
| 17 | **Gas supply lock** — pipeline interconnect, metering, contingency storage | Gas utility engagement | Block 1 energization | Scott / gas utility |
| 18 | **NFPA 855 AHJ pre-application (Lafayette Parish)** | BESS vendor compliance docs (Step 8); rear slab layout | BESS setback study; PHYS layout lock | Scott / AHJ |
| 19 | **Structural assessments B1–B4 (B-07)** | — | Rooftop solar loading lock; interior retrofit scope; HTC Part 2 inputs | Scott / structural engineer |
| 20 | **E-14 inter-block tie decision** (11 independent vs tied at aux point) | Contingency analysis; BESS sizing (Step 8) | ELEC-001 §9 advance; SLD-001 routing | Scott |
| 21 | **SLD-001 draft** — formal single-line inheriting ARCHDIAG-001 + ELEC-001 | Steps 1, 8, 9, 10, 11, 20 closed | PROT-001 input | Scott |
| 22 | **PROT-001 draft** — protection coordination study with CT ratios, pickup settings, coord intervals, AC-DC boundary coordination | SLD-001 (Step 21) | **Construction package gate** | Scott / protection engineer |

### 11.1 BOD-001 revision trigger summary

| BOD Rev | Trigger | Approximate sequence step |
|---|---|---|
| 0.4 (current) | E-24 through E-30, A-09 added from ARCHDIAG-001 | — |
| 0.5 | CHP heat balance with Munters slip-stream; updates T-03, T-08, F-section | After Step 3 (TB-5) + Step 1 (Cat CSA) |
| 0.6 | Cat CSA validation complete; updates E-05, E-06, E-08 | After Step 1, 11 |
| 0.7 | LDEQ LPDES pre-application returns; updates B-section and G-section | After Step 14 |
| 0.8 | SHPO Part 1 filing; updates R-05 and HTC constraints | After Step 13 |
| 1.0 | All C1 external dependencies locked; ready for circulation | After Steps 1–22 closed |

### 11.2 Construction package gate

SLD-001 Rev 1.0 + PROT-001 Rev 1.0 paired with THERMAL-BASIS Rev 1.0, COOLING-TOWER-001 Rev 1.0, BESS-001 Rev 1.0, SOLAR-001 Rev 1.0, CHP-SCHEMATIC-001 Rev 1.0, and BOD-001 Rev 1.0. All C1 items per §9.1 and §9.2 closed.

---

**End of ST-TRAP-MASTER-ENG-001 Rev 0.1.**
