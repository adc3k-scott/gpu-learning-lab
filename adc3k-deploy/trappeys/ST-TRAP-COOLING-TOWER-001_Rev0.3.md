# ST-TRAP-COOLING-TOWER-001 — Cooling Tower Field Specification — Rev 0.3

**Document:** Cooling Tower Field — Vendor Specification Basis
**Project:** Trappey's AI Center, Lafayette, Louisiana
**Revision:** 0.3 — tower duty rebased to ~72.9 MW per BOD Rev 0.6 C-17; CDU updated to CoolIT CHx2000; flow and makeup scaled accordingly
**Date:** April 23, 2026
**Owner:** Scott Tomsu
**Status:** Working draft
**Authority:** TRAP-BOD-001 Rev 0.6 and ST-TRAP-THERMAL-BASIS Rev 0.6 govern all upstream values. This document governs cooling tower field sizing basis and vendor RFQ framework.

---

## Revision Log

| Rev | Date | Changes |
|---|---|---|
| 0.1 | 2026-04-18 | First issue — cooling towers sized for absorption chiller condenser + absorber rejection (~241 MW); GPU warm water routed to separate adiabatic dry cooler |
| **0.2** | **2026-04-22** | **Absorption chiller eliminated. Cooling towers now serve GPU warm water directly (80.96 MW Stage 1 / 161.9 MW Full Build). Plate HX added as facility boundary. All duty, flow, water consumption, footprint, and electrical estimates recalculated.** |
| **0.3** | **2026-04-23** | **Tower duty rebased to ~72.9 MW Stage 1 / ~145.7 MW Full Build per BOD Rev 0.6 (C-17: ~1,656 kW/cassette). CDU updated to CoolIT CHx2000 external skid per Cassette-COOL2-001 Rev 1.0. Flow: ~30,700 GPM → ~27,600 GPM. Makeup: ~830 GPM / ~1.20 MGD → ~747 GPM / ~1.08 MGD. Tower sizing: ~23,020 RT → ~20,720 RT. Cooling MCC: ~1,500 kW → ~1,400 kW.** |

---

## 1. Purpose

This document establishes the cooling tower field specification basis for the Trappey's AI Center. It defines:

- System boundary — what the cooling tower field serves and what it does not
- Thermal duty calculation — Stage 1 and Full Build heat rejection loads
- Design conditions — Lafayette climate, ASHRAE wet-bulb basis, CDU supply temperature constraints
- Plate HX interface — facility boundary between CDU warm water circuit and cooling tower circuit
- Tower type analysis — wet vs hybrid vs adiabatic, with recommendation basis
- Water consumption estimates — makeup and blowdown working figures
- Electrical and controls requirements — fan VFDs, pump sizing, AMCL integration
- Vendor shortlist and RFQ anchor conditions

Values marked **W** are working estimates. Values marked **L** are locked. Values marked **O** are open pending external input.

---

## 2. Relationship to other documents

**Upstream (this document inherits from):**

- TRAP-BOD-001 Rev 0.6 — locked site, IT load, and infrastructure parameters. BOD C-17 (~1,656 kW/cassette cassette secondary cooling load, W) is the primary sizing input.
- ST-TRAP-THERMAL-BASIS Rev 0.6 — CHP cascade disposition, GPU warm water path, Vermilion River elimination, design wet-bulb
- ST-TRAP-CHP-SCHEMATIC-001 Rev 0.3 — visual companion confirming cooling towers as sole GPU warm water rejection path

**Downstream (inherits from this document):**

- ST-TRAP-ELEC-001 Rev 1.3 — cooling MCC feeder sizing revision after T-08 closes (~1,400 kW campus, down from prior ~1,500 kW)
- ST-TRAP-ARCHDIAG-001 (update pending) — cooling tower siting annotation on campus diagram
- Cooling tower vendor RFQ — issued from this basis after T-05 and T-08 close

---

## 3. System boundary

### 3.1 What the cooling tower field serves

The cooling tower field serves **one circuit exclusively**: the GPU warm water loop via a plate heat exchanger (PHX) at the facility boundary. This is the primary continuous heat rejection path for all cassette secondary cooling.

```
NVIDIA Vera Rubin GPU cold plates
  ↓ ~50–55°C warm water return (W)
CoolIT CHx2000 external CDU skid (44 units · N+1 pumps) (L C-03)
  ↓ warm water facility header
Plate HX PHX-001 — facility boundary
  ↓ CDU warm water cools to ≤45°C supply (L C-04)
  ↕ [heat transfer: ~72.9 MW Stage 1]
Cooling tower circuit
  ↓ ~41–43°C return to tower (W)
COOLING TOWERS — atmospheric rejection
  ↓ ~31–34°C supply back to PHX cold side (W)
```

This is a continuous, full-load duty circuit. The plate HX maintains thermal and pressure isolation between the CDU warm water circuit and the cooling tower open circuit.

### 3.2 What the cooling tower field does not serve

**CHP exhaust and jacket water heat** are not routed to the cooling towers.

- CHP exhaust: 5,500 kW routes to Munters DSS Pro desiccant regen (T-12 LOCKED). Remaining ~42,372 kW rejects via exhaust stack.
- CHP jacket water: ~58,212 kW rejects via air-cooled radiators to atmosphere.
- No HRU, no absorption chiller, no chilled water distribution from CHP.

| Circuit | Campus Duty | Rejection Path |
|---|---|---|
| GPU warm water (CoolIT CHx2000 CDU secondary) | ~72.9 MW Stage 1 / ~145.7 MW Full Build (W C-17) | Cooling towers — plate HX PHX-001 boundary (this document) |
| CHP exhaust — Munters load | 5,500 kW (L T-12) | Munters DSS Pro desiccant regen in cassette enclosures |
| CHP exhaust — remainder | ~42,372 kW (W) | Stack to atmosphere |
| CHP jacket water | ~58,212 kW (W) | Air-cooled radiators to atmosphere |

---

## 4. Design conditions

| Parameter | Value | Status | Source |
|---|---|---|---|
| Site | 22-acre Trappey's Cannery, Lafayette, LA, 30.214°N | L | BOD P-01 |
| Climate classification | Gulf Coast, humid subtropical, ASHRAE zone 2A | L | Site |
| ASHRAE 0.4% design wet-bulb | 28°C (82°F) | L | ASHRAE HOF, Lafayette |
| ASHRAE 0.4% design dry-bulb | 35°C (95°F) | L | ASHRAE HOF, Lafayette |
| Annual average RH | 75–80% | L | THERMAL-BASIS §3 |
| CDU warm water supply to PHX (hot side in) | ~50–55°C | W | THERMAL-BASIS §9 |
| CDU supply from PHX (hot side out) | ≤45°C | L | BOD C-04 |
| Cooling tower supply to PHX (cold side in) | ~31–34°C | W | 3–6°C approach at 28°C WB |
| Cooling tower return from PHX (cold side out, tower inlet) | ~41–43°C | W | Pending PHX sizing |
| Cooling tower temperature range | ~9–12°C | W | |
| PHX approach temperature — design day | ~14°C (CDU ≤45°C supply vs. tower ~31°C cold side in) | W | Well within commercial PHX capability |

---

## 5. Thermal duty

### 5.1 GPU warm water load — sizing basis

The cooling tower field is sized to reject the full cassette secondary cooling load as defined in BOD-001 C-17.

| Stage | Cassettes | Unit Load (kW) | Total Duty | Status |
|---|---|---|---|---|
| Stage 1 | 44 | ~1,656 | **~72,864 kW (~72.9 MW)** | **W (C-17)** |
| Full Build | 88 | ~1,656 | ~145,728 kW (~145.7 MW) | W |

**Stage 1 (~72.9 MW) is the design sizing basis for the RFQ.** Full Build (~145.7 MW) establishes tower field expansion requirements; space and piping headers should accommodate phased addition of cells without system downtime.

### 5.2 No staging complexity

The CoolIT CHx2000 CDU skids operate at continuous duty matching IT load. Tower VFD fans provide turndown during partial IT load. No excess drive heat, no chiller staging, no bypass path needed.

---

## 6. Cooling tower circuit and plate HX interface

### 6.1 Circuit parameters — Stage 1

| Parameter | Value | Status |
|---|---|---|
| Circuit thermal duty | ~72,864 kW | W (C-17) |
| CDU warm water to PHX (hot side in) | ~50–55°C | W |
| CDU supply from PHX (hot side out) | ≤45°C | L (C-04) |
| Cooling tower supply to PHX (cold side in) | ~31–34°C | W |
| Cooling tower return from PHX (cold side out) | ~41–43°C | W |
| Temperature range across tower | ~9–12°C | W |
| Circulating flow — Stage 1 | **~1,742 L/s (~27,600 GPM)** | W |
| Circulating flow — Full Build | ~3,484 L/s (~55,200 GPM) | W |

Flow basis: Q = P / (ρ × Cp × ΔT) = 72,864 kW / (1.0 kg/L × 4.18 kJ/kg·K × 10°C) = ~1,742 kg/s ≈ ~27,600 GPM.

### 6.2 Plate HX — facility boundary

The plate HX thermally and hydraulically isolates the CDU warm water circuit (closed loop, facility headers) from the cooling tower circuit (open loop, chemical treatment, basin).

| PHX parameter | Value | Status |
|---|---|---|
| Hot side duty | ~72,864 kW | W |
| Hot side in | ~50–55°C | W |
| Hot side out | ≤45°C | L (C-04) |
| Cold side in | ~31–34°C | W |
| Cold side out | ~41–43°C | W |
| Approach temperature | ~14°C | W |
| Sizing reference | PHX-001 open item — T-08 dependent | O |

---

## 7. Tower type analysis

BOD T-05 (cooling tower type) is Open.

### 7.1 Option W — wet mechanical draft (evaporative)

| Factor | Assessment |
|---|---|
| Capital cost | Lowest of all options |
| Approach to wet-bulb | Best — closest approach, best peak-day performance |
| Water consumption | Highest — ~747 GPM makeup at design day (§8) |
| Louisiana wet-bulb profile | Best fit — tower sized directly for 28°C WB |
| LPDES blowdown | Required — cooling tower blowdown is a permitted discharge |

### 7.2 Option H — hybrid dry/wet (fluid cooler)

| Factor | Assessment |
|---|---|
| Capital cost | 1.5–2× wet tower |
| Water consumption reduction | 30–50% at annual average |
| Dry-mode hours (Lafayette) | Limited — wet-bulb rarely below 24°C; dry mode useful November–February only |
| Louisiana climate fit | Marginal — Gulf Coast minimizes dry-mode hours |

Candidate if LPDES blowdown disposal or municipal water cost becomes a binding constraint.

### 7.3 Option A — adiabatic pre-cooler

Not recommended. Cannot maintain ≤34°C tower supply on design days (35°C dry-bulb).

### 7.4 Full dry cooling (rejected)

Cannot maintain ≤34°C cooling tower supply at 35°C design dry-bulb.

### 7.5 Recommendation basis

**Option W (wet mechanical draft) is the recommended basis.** Option H is the contingency if treatment complexity or LPDES blowdown becomes a cost or permitting driver.

---

## 8. Water consumption estimates — wet tower, Stage 1 duty

| Parameter | Value | Basis |
|---|---|---|
| Circulating flow rate | ~27,600 GPM | §6.1 |
| Cooling range | ~10°C (18°F) | §6.1 |
| Evaporation rate | ~498 GPM | ~1.44% per 14.4°F × (18/14.4) × 27,600 GPM |
| Cycles of concentration (design) | 3.0 | Industry standard for municipal water |
| Blowdown rate | ~249 GPM | Evaporation / (COC − 1) |
| Drift loss | ~0.3 GPM | 0.001% with drift eliminators |
| **Total makeup water — Stage 1 design day** | **~747 GPM (~1.08 MGD)** | Sum |
| Total makeup water — Full Build design day | ~1,494 GPM (~2.15 MGD) | Scaled ×2 |

**Makeup water source:** Open (BOD §G, T-09). Candidates: municipal (simplest, highest cost), on-site well, Vermilion River surface intake (separate makeup-water permit path — not the cancelled thermal discharge).

---

## 9. Equipment layout and siting

### 9.1 Infrastructure yard

Primary cooling tower location: **infrastructure yard, 28,000 sq ft** (BOD B-06). Exhaust plume must not recirculate to genset combustion air intakes. PHX placement preferred inside or adjacent to Power Hall to minimize warm water header length.

### 9.2 Field footprint check

For ~20,720 RT Stage 1 total duty:
- Estimated unit count: 2 cells at ~10,360 RT each, plus 1 spare cell for N+1 posture = **3 cells**
- Estimated field footprint: **~6,000 sq ft** Stage 1 (2 cells duty + 1 spare; ~200 × 30 ft)
- Full Build: additional 2 cells = 5 cells total; footprint ~330 × 30 ft (~10,000 sq ft)
- Infrastructure yard (28,000 sq ft): **tower field is well within available area**, leaving ample room for transformers and switchgear

---

## 10. Electrical requirements

### 10.1 Fan motors and VFDs

All cooling tower fan motors must be VFD-driven. VFD speed reference from L1 cooling tower supply temperature control loop; L3 AMCL dispatch overrides for optimization.

### 10.2 Fan power estimate

| Parameter | Value | Basis |
|---|---|---|
| Gross heat rejected (Stage 1) | ~72,864 kW | W (C-17) |
| Fan power (1–1.5% of heat rejected) | **~730–1,095 kW** | Industry estimate |
| Fan power per tower cell (3 cells) | ~243–365 kW per cell | Derived |

### 10.3 Cooling tower circuit pumps

| Parameter | Value | Basis |
|---|---|---|
| Stage 1 circulating flow | ~1,742 L/s (~27,600 GPM) | §6.1 |
| System head (tower → PHX → return, estimated) | ~15–20 m | Pending piping layout |
| Pump power (Stage 1, 75% efficiency) | **~340–460 kW** | P = ρgQH/η |
| Pump arrangement | N+1 — one duty plus one standby per header | |

### 10.4 Total cooling tower MCC estimate — Stage 1

| Item | Working Value |
|---|---|
| Tower fan motors (3 cells) | ~730–1,095 kW |
| Cooling tower circuit pumps | ~340–460 kW |
| Makeup, blowdown, chemical dosing, sump | ~90 kW |
| PHX auxiliary (valves, controls) | ~40 kW |
| **Total cooling tower MCC (Stage 1)** | **~1,400 kW** |

### 10.5 Controls integration

| AMCL Level | Cooling Tower Functions |
|---|---|
| L0 — field devices | VFD drives; supply/return RTDs; flow meters; basin level; vibration monitors; chemical dosing |
| L1 — block PLC | Cooling tower supply temperature control loop; fan speed cascade; pump duty/standby switching |
| L2 — plant SCADA | CT temperature historian; makeup/blowdown totalizer; alarm management |
| L3 — AMCL dispatch | Cross-system cooling optimization; peak-day anticipation; fan speed staging |

---

## 11. Open items ledger

| Ref | Item | Blocked on | Priority |
|---|---|---|---|
| T-05 | Tower type selection (W / H / A) | Scott decision after water cost and LPDES review | C1 — gates RFQ |
| T-08 | Tower field sizing confirmation — **~72.9 MW Stage 1** | Cat CSA (genset load confirmation); PHX sizing | C1 |
| T-09 | Makeup water source (municipal / well / Vermilion intake) | BOD §G; LPDES pre-application | C2 |
| PHX-001 | Plate HX sizing — CDU warm water to cooling tower circuit | T-08 close; PHX vendor engagement | C1 |
| SITING-001 | Cooling tower field siting — PHX placement, header routing, N+1 expansion space | Tower vendor selection | C2 |
| BLOWDOWN | Blowdown disposal path (~249 GPM) | LPDES pre-application | C2 |
| NOISE-VIS | Tower height, plume drift, fan noise | Tower vendor submittal | C2 |

---

## 12. Vendor shortlist

From BOD-001 §N — no selection made; all open:

| Vendor | Key Products | Notes |
|---|---|---|
| SPX / Marley | NC counterflow, FXV fluid cooler, Ultracool hybrid | Widest RT range; US-manufactured |
| BAC (Baltimore Aircoil) | Series 3000 counterflow, Hybrid Cooler ICC | Strong industrial and data center experience |
| Evapco | AT, UT series; hybrid AMC; LSTA low-profile | US-manufactured; DOE pump efficiency compliant |

**RFQ anchor conditions (pending T-05, T-08, PHX-001):**

- Stage 1 rated duty: **~20,720 RT (~72.9 MW)** — size for this; provision header and pad for Full Build expansion to ~41,440 RT (~145.7 MW)
- Design wet-bulb: 28°C (82°F) ASHRAE 0.4%, Lafayette, Louisiana
- Cooling tower supply (tower outlet, PHX cold side in): ≤34°C at 28°C WB; target ≤31°C at 3°C approach
- Cooling tower return (tower inlet, PHX cold side out): ~41–43°C
- Temperature range: ~9–12°C
- Circulating flow: **~27,600 GPM Stage 1** (~55,200 GPM Full Build)
- Fan motors: VFD-driven; AMCL-compatible speed reference; IE3 motor minimum
- Arrangement: minimum 2 independent duty cells; 1 spare cell position for N+1 posture
- Drift eliminators: ≤0.001% of circulating flow
- Materials: coastal-environment compatible — 304 SS basin minimum, FRP or fiberglass structure, stainless hardware
- Noise: vendor to provide dBA at 50 ft; Lafayette parish compliance to be confirmed

---

## 13. Revision plan

| Rev | Date | Changes |
|---|---|---|
| 0.1 | 2026-04-18 | First issue — system boundary, duty calculation for absorption chiller condenser load (~241 MW) |
| 0.2 | 2026-04-22 | Absorption chiller eliminated. GPU warm water is sole tower load (80.96 MW Stage 1). Plate HX added. |
| **0.3 (current)** | **2026-04-23** | **Tower duty rebased to ~72.9 MW Stage 1 per BOD Rev 0.6 C-17 (~1,656 kW/cassette). CDU updated to CoolIT CHx2000. Flow: ~27,600 GPM. Makeup: ~747 GPM / ~1.08 MGD. Tower sizing: ~20,720 RT Stage 1. Cooling MCC: ~1,400 kW.** |
| 0.4 | T-08 close + PHX-001 | Update §5–§6 with confirmed heat balance; update §10 electrical with PHX pump sizing |
| 0.5 | T-05 decision | Update §7 with selected tower type; refine §8 water consumption; issue RFQ |
| 1.0 | Tower vendor selection + performance confirmation | All C1 items closed. Paired with THERMAL-BASIS Rev 1.0 and CHP-SCHEMATIC-001 Rev 1.0. |

---

## 14. Approval

Rev 0.3 is a working draft for internal engineering use. Not for external distribution. Sign-off follows BOD-001 Rev 0.6 approval path.

---

**End of ST-TRAP-COOLING-TOWER-001 Rev 0.3.**
