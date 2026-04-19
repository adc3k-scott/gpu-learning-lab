# ST-TRAP-COOLING-TOWER-001 — Cooling Tower Field Specification — Rev 0.1

**Document:** Cooling Tower Field — Vendor Specification Basis
**Project:** Trappey's AI Center, Lafayette, Louisiana
**Revision:** 0.1 — first issue
**Date:** April 18, 2026
**Owner:** Scott Tomsu
**Status:** Working draft
**Authority:** BOD-001 Rev 0.4 and ST-TRAP-THERMAL-BASIS Rev 0.4 govern all upstream values. This document governs cooling tower field sizing basis and vendor RFQ framework.

---

## 1. Purpose

This document establishes the cooling tower field specification basis for the Trappey's AI Center. It defines:

- System boundary — what the cooling tower field serves and what it does not
- Thermal duty calculation — maximum and nominal operating heat rejection loads
- Design conditions — Lafayette climate, ASHRAE wet-bulb basis, condenser water temperature constraints
- Tower type analysis — wet vs hybrid vs adiabatic, with recommendation basis
- Water consumption estimates — makeup and blowdown working figures
- Electrical and controls requirements — fan VFDs, pump sizing, AMCL integration
- Vendor shortlist and RFQ anchor conditions

Values marked **W** are working estimates derived from THERMAL-BASIS Rev 0.4 and BOD-001 Rev 0.4. Values marked **L** are locked. Values marked **O** are open pending external input. Until TB-5 closes (chiller type selection), condenser water temperatures and flow rate carry W status.

---

## 2. Relationship to other documents

**Upstream (this document inherits from):**

- BOD-001 Rev 0.4 — locked site, IT load, and infrastructure parameters
- ST-TRAP-THERMAL-BASIS Rev 0.4 — CHP cascade heat balance, genset heat rejection, absorption chiller options, Vermilion River elimination, design wet-bulb

**Downstream (inherits from this document):**

- ST-TRAP-ELEC-001 (update pending) — cooling MCC feeder sizing revision after T-08 close
- ST-TRAP-ARCHDIAG-001 (update pending) — cooling tower siting annotation on campus diagram
- Cooling tower vendor RFQ package — issued from this basis after T-05 and COND-WB close

**Note on stale BOD entries:** BOD T-04 describes cooling towers as "residual rejection" and T-06 lists "Vermilion River supplemental" as a Locked supplemental cold sink. THERMAL-BASIS §9.1 eliminated the Vermilion River as a heat sink due to tidal reversal and Gulf Coast summer ambient temperatures (30–33°C exceeding the 29°C Broad chiller condenser rated inlet). The cooling towers are therefore the **sole and primary** heat rejection path — not residual. BOD T-04, T-06, and R-03 require update at the next BOD revision to reflect this. Until then, THERMAL-BASIS §9.1 governs.

---

## 3. System boundary

### 3.1 What the cooling tower field serves

The cooling tower field serves **one circuit exclusively**: the absorption chiller condenser + absorber cooling water loop. This is the CHP cascade's primary continuous heat rejection path to atmosphere.

```
Genset exhaust + jacket water
  ↓
[Option B] Exhaust HRU → 180°C hot water
  ↓
Broad BH two-stage absorption chiller
  ├── Chilled water side (6.7°C supply / 13.7°C return) → facility cold distribution
  └── Condenser + absorber side (37°C return from chiller)
        ↓
  COOLING TOWERS → atmospheric heat rejection → ≤29°C (≤31°C derating) supply to chiller
```

This is a continuous, full-load duty circuit, not a peak-day supplement or trim path.

### 3.2 What the cooling tower field does NOT serve

**Boyd CDU GPU warm water loop** is a separate circuit on separate equipment.

- Boyd CDU returns GPU warm water at ~50–55°C from the rack cold plates
- This loop rejects to a **dedicated adiabatic dry cooler**, not to the cooling towers
- Thermal cross-contamination between the 50°C warm water loop and the 29–37°C absorption chiller condenser circuit must be prevented — separate circuits, separate equipment, no shared basin or header

| Circuit | Campus Duty | Rejection Path |
|---|---|---|
| Absorption chiller condenser + absorber | ~184–241 MW (see §5) | Cooling towers (this document) |
| Boyd CDU GPU warm water | ~81 MW (BOD C-17 × 44 cassettes) | Adiabatic dry cooler (separate scope) |

---

## 4. Design conditions

| Parameter | Value | Status | Source |
|---|---|---|---|
| Site | 22-acre Trappey's Cannery, Lafayette, LA, 30.214°N | L | BOD P-01 |
| Climate classification | Gulf Coast, humid subtropical, ASHRAE zone 2A | L | Site |
| ASHRAE 0.4% design wet-bulb | 28°C (82°F) | L | ASHRAE HOF, Lafayette |
| ASHRAE 0.4% design dry-bulb | 35°C (95°F) | L | ASHRAE HOF, Lafayette |
| Annual average RH | 75–80% | L | THERMAL-BASIS §3 |
| Summer peak RH | 85–90% | L | THERMAL-BASIS §3 |
| Condenser water supply to chiller (tower outlet) | ≤29°C rated; ≤31°C derating case | W | Broad BH catalog; COND-WB open |
| Condenser water return from chiller (tower inlet) | 37°C | W | Broad XII catalog, BH and BE series |
| Condenser water temperature range | 8°C (14.4°F) | W | Broad rated |
| Tower approach temperature at 28°C WB design day | 1°C to reach 29°C; 3°C practical (31°C supply) | W | See §6 — COND-WB open |

---

## 5. Thermal duty

### 5.1 Absorption chiller energy balance

For a LiBr absorption chiller, the energy balance is:

**Q_condenser+absorber = Q_drive + Q_evaporator**

The cooling tower rejects the combined condenser and absorber load. Pump work is negligible against the process heat and is excluded.

### 5.2 Maximum duty case — design sizing basis

This is the sizing basis for the cooling tower field. It represents all absorption chillers operating at maximum capacity against the full available drive heat.

| Parameter | Value | Status |
|---|---|---|
| Net thermal drive (after Munters 5,500 kW deduction) | 100,584 kW | W |
| Absorption COP (Option B, double-effect, part-load derate) | 1.40 | W |
| Absorption cooling produced — Q_evaporator | 140,818 kW | W |
| **Cooling tower duty — Q_condenser+absorber (maximum)** | **241,402 kW (241.4 MW)** | **W** |
| Equivalent in cooling tons | 68,640 RT | W |

### 5.3 Nominal operating duty — chiller staged to campus demand

This is the expected continuous operating point. Chillers are staged to match actual campus cooling demand.

| Parameter | Value | Status |
|---|---|---|
| Campus cooling demand (IT + facility overhead) | ~107,300 kW | W |
| Drive consumed at nominal demand (Q_demand / COP) | ~76,643 kW | W |
| **Cooling tower duty — nominal staged operation** | **~183,943 kW (183.9 MW)** | **W** |
| Equivalent in cooling tons | 52,310 RT | W |
| Turndown ratio (nominal / maximum) | 76.2% | W |

### 5.4 Excess drive heat disposition

At nominal staged operation, ~23,941 kW of drive heat remains after satisfying cooling demand (100,584 kW available − 76,643 kW consumed). This excess must be managed:

- **Chiller staging:** Operate fewer chiller units at higher individual loading rather than all units at minimum load. Reduces excess drive heat and keeps individual chillers in efficient operating range.
- **Trim heat exchanger (contingency):** Bypass path to reject residual drive heat without producing additional chilled water. Piping design item — not scoped in this document; flagged for mechanical design package.
- **Tower sizing implication:** The cooling tower field is sized for the **maximum duty case** (§5.2). VFD-driven fans provide turndown to nominal operating point.

---

## 6. Condenser water circuit and approach temperature

### 6.1 Circuit parameters

| Parameter | Value | Status |
|---|---|---|
| Condenser water supply temperature (tower outlet → chiller inlet) | ≤29°C rated; ≤31°C derating | W |
| Condenser water return temperature (chiller outlet → tower inlet) | 37°C | W |
| Temperature range (ΔT) | 8°C (14.4°F) | W |
| Circulating flow — maximum duty | ~7,220 L/s (~114,400 GPM) | W |
| Circulating flow — nominal duty | ~5,500 L/s (~87,200 GPM) | W |

Flow rate basis: Q = P / (ρ · Cp · ΔT) = 241,402 kW / (1.0 kg/L × 4.18 kJ/kg·K × 8°C) = 7,220 kg/s at maximum duty. Nominal duty scales proportionally.

### 6.2 Approach temperature constraint — COND-WB open item

**The approach temperature required to meet Broad's rated 29°C condenser inlet at the Lafayette design wet-bulb is critically tight.**

At 28°C wet-bulb (ASHRAE 0.4% Lafayette):

| Parameter | Value |
|---|---|
| Broad BH rated condenser water inlet | 29°C |
| Required tower approach (to achieve rated CW supply) | 29 − 28 = **1°C** |
| Standard commercial tower approach (3°C) | 28 + 3 = **31°C** — 2°C above rated |
| Standard commercial tower approach (5°C) | 28 + 5 = **33°C** — 4°C above rated |

A 1°C approach is not achievable with commercial mechanical-draft cooling towers at economic sizing. The standard 3°C approach delivers 31°C condenser water to the Broad chiller on peak design days — 2°C above the rated 29°C inlet.

**This is not a project-stopper.** Absorption chillers operate above rated condenser water temperature with a predictable capacity and COP derating. The existing >100% absorption coverage margin (§5.2) provides headroom to absorb this derating without impact to campus cooling reliability.

**COND-WB resolution path:**

1. Broad / Thermax application engineering confirms the operating envelope at 30–31°C condenser water inlet. Expected finding: 3–5% capacity and COP derating at 2°C above rated.
2. RFQ to cooling tower vendors specifies: supply ≤31°C at 28°C wet-bulb with 3°C approach as the binding performance point.
3. Broad confirmation of acceptable CW inlet envelope is a pre-award condition on the chiller RFQ (TB-5).
4. If Broad imposes a stricter CW inlet limit: re-evaluate tower sizing for ≤2°C approach (larger tower, higher capex) vs alternative chiller vendor with higher rated CW inlet tolerance.

Until COND-WB closes, condenser water supply to chiller is specified at ≤31°C at 28°C WB (3°C approach).

---

## 7. Tower type analysis

BOD T-05 (cooling tower type) is Open. This section provides the basis for Scott's decision.

### 7.1 Option W — wet mechanical draft (evaporative)

| Factor | Assessment |
|---|---|
| Capital cost | Lowest of all options |
| Approach to wet-bulb | Best — closest approach, best peak-day performance |
| Water consumption | Highest — ~2,450 GPM makeup at design day (§8) |
| Annual water/treatment cost | Highest — biocide, scale, corrosion inhibition, blowdown disposal |
| Louisiana wet-bulb profile | Best fit — tower sized directly for 28°C WB |
| LPDES blowdown | Required — cooling tower blowdown is a permitted discharge |
| Legionella management | Standard water treatment program required |

### 7.2 Option H — hybrid dry/wet (fluid cooler)

| Factor | Assessment |
|---|---|
| Capital cost | 1.5–2× wet tower |
| Water consumption reduction | 30–50% at annual average |
| Dry-mode hours (Lafayette) | Limited — wet-bulb rarely below 24°C; dry mode useful November–February only |
| Peak-day performance | Wet section active; same peak capacity as Option W |
| Louisiana climate fit | Marginal — Gulf Coast minimizes dry-mode hours; higher capex with limited payback |

Candidate if LPDES blowdown disposal or municipal water cost becomes a binding constraint.

### 7.3 Option A — adiabatic pre-cooler

| Factor | Assessment |
|---|---|
| Capital cost | Highest |
| Water consumption | Substantially lower |
| Peak-day performance | Limited by dry-bulb (35°C), not wet-bulb — cannot maintain ≤31°C CW supply on peak design days without extreme oversizing |
| Louisiana fit | Poor — summer dry-bulb 35°C eliminates the adiabatic advantage when it matters most |

Not recommended as primary tower type for this site.

### 7.4 Full dry cooling (rejected)

Full dry air-cooled heat rejection cannot maintain ≤31°C condenser water supply at 35°C design dry-bulb. Excluded at any economic scale for this duty.

### 7.5 Recommendation basis

**Option W (wet mechanical draft) is the recommended basis** pending Scott's review of water cost and blowdown disposal options. Option H is the contingency if treatment complexity or LPDES blowdown discharge becomes a cost or permitting driver. Tower type selection closes T-05.

---

## 8. Water consumption estimates — wet tower, maximum duty

All values are working estimates. Actual values depend on tower type, cycles of concentration, and monthly wet-bulb variability.

| Parameter | Value | Basis |
|---|---|---|
| Circulating flow rate | ~114,400 GPM | §6.1 |
| Cooling range | 8°C (14.4°F) | Broad condenser water ΔT |
| Evaporation rate | ~1,650 GPM | ~1.44% of circulation at 14.4°F range |
| Cycles of concentration (design) | 3.0 | Industry standard for municipal water |
| Blowdown rate | ~825 GPM | Evaporation / (COC − 1) |
| Drift loss | ~1 GPM | 0.001% with drift eliminators |
| **Total makeup water — maximum duty** | **~2,476 GPM (~3.57 MGD)** | Sum |
| Total makeup water — nominal operating | ~1,888 GPM (~2.72 MGD) | Scaled 76.2% |

**Makeup water source:** Open (BOD §G). Candidates: municipal (simplest, highest cost), on-site well, Vermilion River surface intake. Note: a Vermilion River intake for makeup water supply (not heat rejection) is a separate permit path from the cancelled RIVER-001 thermal discharge. River intake for makeup requires a separate LDEQ intake permit if volume is significant. Water treatment program (biocide, scale, corrosion) is not scoped in this document.

---

## 9. Equipment layout and siting

### 9.1 Infrastructure yard

Primary cooling tower location: **infrastructure yard, 28,000 sq ft** (BOD B-06). This yard also hosts genset step-down transformers, 13.8 kV switchgear, and SCR/oxidation catalyst equipment.

**Siting constraints:**

- Exhaust plume must not recirculate to genset combustion air intakes. Minimum separation per tower vendor guidance (typically one to two tower heights upwind clearance).
- Condenser water piping run: absorption chiller plant placement determines header routing. Preferred chiller plant location is adjacent to or inside the rear high-ground building (Power Hall), which minimizes condenser water header length.
- Tower height and fan noise: mechanical-draft fans must comply with Lafayette parish noise ordinances. Tower visual profile requires SHPO review for impact on the historic site character.
- Blowdown: piped to sump; disposal path (POTW, Vermilion River makeup-path permit, or evaporation) confirmed with LPDES pre-application.

### 9.2 Field footprint check

Reference tower sizing: a SPX/Marley NC or BAC Series 3000 counterflow unit rated at 10,000–12,000 RT (35–42 MW rejection) occupies approximately 60 × 30 ft footprint.

For 68,640 RT total duty:
- Estimated unit count: 6–7 units at 10,000–12,000 RT each (plus at least one spare cell for N+1 posture)
- Estimated field footprint: **~200 × 100 ft** (rough working estimate before vendor layout)
- Infrastructure yard (28,000 sq ft ≈ 167 × 168 ft): **at or below the lower limit** for the cooling tower field alone, before transformers and switchgear

**Flag:** The 28,000 sq ft infrastructure yard may not accommodate the full cooling tower field plus all genset electrical equipment. The rear slab (42,000 sq ft, BOD B-05, primary genset footprint) may need to provide overflow tower positions. A siting study is a C2 deliverable required before tower RFQ is issued.

---

## 10. Electrical requirements

### 10.1 Fan motors and VFDs

All cooling tower fan motors must be VFD-driven. VFD speed reference originates from the L1 condenser water temperature control loop; L3 AMCL dispatch overrides for optimization. VFD turndown prevents overcooling (condenser water below 29°C reduces chiller efficiency and may cause crystallization risk in the LiBr solution — minimum CW supply temperature to the chiller to be confirmed with Broad app eng).

### 10.2 Fan power estimate

| Parameter | Value | Basis |
|---|---|---|
| Gross heat rejected (maximum duty) | 241,402 kW | §5.2 |
| Fan power (1–1.5% of heat rejected) | ~2,400–3,600 kW | Industry estimate |
| Fan power per tower cell (6–7 cells) | ~350–600 kW per cell | Derived |

### 10.3 Condenser water circulation pumps

| Parameter | Value | Basis |
|---|---|---|
| Maximum circulating flow | 7,220 L/s (114,400 GPM) | §6.1 |
| System head (tower → chiller → return, estimated) | ~15–20 m | Pending piping layout |
| Pump power (maximum duty, 75% efficiency) | ~1,400–1,900 kW | P = ρgQH/η |
| Pump arrangement | N+1 — two duty pumps plus one standby per header | AMCL flow modulation |

### 10.4 Total cooling plant MCC estimate

| Item | Working Value |
|---|---|
| Tower fan motors (all cells) | ~3,000 kW |
| Condenser water circulation pumps | ~1,600 kW |
| Makeup, blowdown, chemical dosing, sump | ~200 kW |
| **Total cooling tower MCC (campus)** | **~4,800 kW** |

**Note on BOD E-29:** BOD E-29 allocates "cooling MCC ~600 kW" per block (11 blocks × 600 kW = 6,600 kW campus). The ~4,800 kW estimate above is consistent as an order-of-magnitude check. E-29 was written before the absorption chiller condenser load was fully sized. The cooling tower MCC will likely be a single centralized campus switchboard fed from the Power Hall, not distributed per-block — this architectural decision is open and feeds the SLD-001 scope.

### 10.5 Controls integration

| AMCL Level | Cooling Tower Functions |
|---|---|
| L0 — field devices | VFD drives; supply/return temperature sensors (RTDs); flow meters; basin level; vibration monitors; chemical dosing controls |
| L1 — block PLC | Condenser water supply temperature control loop; fan speed cascade; low-temperature cutout (crystallization protection); pump duty/standby switching |
| L2 — plant SCADA | CW temperature historian; makeup/blowdown totalizer; treatment dosing interlocks; alarm management |
| L3 — AMCL dispatch | Cross-block chiller staging vs tower load optimization; peak-day derating compensation; thermal shifting for BESS coordination |

VFDs hold last speed command on L3 loss. L1 protects against crystallization floor regardless of L3 command.

---

## 11. Open items ledger

| Ref | Item | Blocked on | Priority |
|---|---|---|---|
| T-05 | Tower type selection (W / H / A) | Scott decision after water cost and LPDES review | C1 — gates RFQ |
| TB-5 | Absorption chiller type (Option B / C) | Cat CSA exhaust temp + Broad app eng | C1 — affects condenser parameters |
| T-08 | CHP heat balance final values | Cat CSA part-load curves | C1 — updates §5 duty numbers |
| COND-WB | Broad condenser water inlet envelope at 30–31°C | Broad app eng / chiller RFQ | C1 — gates CW supply spec |
| BOD-UPD | BOD T-04, T-06, R-03 update — river eliminated; towers are primary, not residual | Next BOD revision | C2 |
| SITING-001 | Cooling tower field siting study — 28,000 sq ft yard check vs full field footprint | Tower vendor selection | C2 |
| WATER-SRC | Makeup water source selection (municipal / well / Vermilion intake) | BOD §G; LPDES pre-application | C2 |
| BLOWDOWN | Blowdown disposal path (POTW / Vermilion intake / evaporation pond) | LPDES pre-application | C2 |
| CRYST-MIN | Minimum condenser water supply temperature to chiller (crystallization floor) | Broad app eng | C2 — controls constraint |
| NOISE-VIS | Tower height, plume drift, fan noise — Lafayette parish and SHPO review | Tower vendor submittal | C2 |

---

## 12. Vendor shortlist

From BOD-001 §N — no selection made; all open:

| Vendor | Key Products | Notes |
|---|---|---|
| SPX / Marley | NC counterflow, FXV fluid cooler, Ultracool hybrid | Widest RT range; US-manufactured |
| BAC (Baltimore Aircoil) | Series 3000 counterflow, Cooling Tower ICC, Hybrid Cooler | Strong CHP + industrial application experience |
| Evapco | AT, UT series; hybrid AMC; LSTA for low-profile | US-manufactured; DOE pump efficiency compliant |
| Brentwood Industries | PVC fill media — component supplier; specified alongside tower OEM | Not a packaged tower vendor |

**RFQ anchor conditions (pending T-05 and COND-WB):**
- Maximum rated duty: 68,640 RT (241.4 MW) — size for this, not nominal operating
- Design wet-bulb: 28°C (82°F) ASHRAE 0.4%, Lafayette, Louisiana
- Condenser water supply (tower outlet): ≤31°C at 28°C WB, 3°C approach (Broad app eng confirmation attached)
- Condenser water return (tower inlet): 37°C
- Temperature range: 8°C
- Circulating flow: ~114,400 GPM at maximum duty
- Fan motors: VFD-driven; AMCL-compatible speed reference (0–10V or Modbus TCP); IE3 motor minimum
- Arrangement: minimum two independent cells; N+1 spare cell position reserved in layout
- Drift eliminators: ≤0.001% of circulating flow
- Materials: coastal-environment compatible — 304SS basin minimum, FRP or fiberglass structure, stainless hardware throughout
- Noise: vendor to provide dBA at 50 ft; Lafayette parish compliance to be confirmed

---

## 13. Revision plan

| Rev | Trigger | Changes |
|---|---|---|
| **0.1 (current)** | First issue | System boundary, duty calculation, tower type analysis, approach temperature gap documented, vendor shortlist, open items |
| 0.2 | T-05 decision | Updates §7 with selected tower type; refines §8 water consumption for type; issues RFQ |
| 0.3 | T-08 close (Cat CSA) | Updates §5 duty with confirmed heat balance; updates §10 electrical estimates |
| 0.4 | COND-WB (Broad app eng) | Updates §6 condenser water supply spec; confirms or revises approach temperature |
| 1.0 | Tower vendor selection + performance confirmation | All C1 items closed; issued for construction. Paired with THERMAL-BASIS Rev 1.0 |

---

## 14. Approval

Rev 0.1 does not carry external circulation approval. Sign-off inherits from BOD-001 Rev 0.4 approval status. External distribution waits for Rev 1.0, gated on all C1 cooling tower and thermal dependencies closing per BOD-001 §M.

---

**End of ST-TRAP-COOLING-TOWER-001 Rev 0.1.**
