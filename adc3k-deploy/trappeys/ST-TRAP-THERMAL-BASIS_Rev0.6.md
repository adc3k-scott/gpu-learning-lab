# ST-TRAP-THERMAL-BASIS — Thermal Architecture Basis — Rev 0.6

**Document:** Thermal Architecture Basis
**Project:** Trappey's AI Center, Lafayette, Louisiana
**Revision:** 0.6 — Stage 1 IT load rebased to 91.1 MW per BOD Rev 0.6; secondary cooling to towers rebased to ~72.9 MW; CDU updated to CoolIT CHx2000; Munters updated to DSS Pro; T-12 regen basis flagged for DSS Pro reconciliation
**Date:** April 23, 2026
**Owner:** Scott Tomsu
**Status:** Working draft
**Authority:** BOD-001 Rev 0.6 governs all locked values. This document governs T-section (thermal) of the Decision Ledger.

---

## 1. Purpose

This document establishes the thermal architecture basis for the Trappey's AI Center. It defines:

- The cold-sink architecture — how GPU heat is rejected to atmosphere via cooling towers (primary and only rejection path)
- The genset thermal characterization — CG260-16 heat rejection data (working, pending Cat CSA); retained as reference for Munters exhaust sizing
- The Munters desiccant slip-stream accounting (Locked, T-12) — the sole CHP heat recovery application
- The regulatory framework — LDEQ / LPDES constraints (no Vermilion River thermal discharge; cooling tower blowdown only)

**Rev 0.6 change summary:** IT load rebased from 101,200 kW (44 × 2,300 kW) to **91,080 kW (44 × 2,070 kW)** per BOD-001 Rev 0.6 C-15 (9 compute racks × 230 kW). Cassette secondary cooling rebased from 1,840 kW to **~1,656 kW** per cassette (C-17 W). Stage 1 tower duty rebased from 80.96 MW to **~72.9 MW** (44 × ~1,656 kW). CDU updated from Boyd CDU to **CoolIT CHx2000 external CDU skid** per Cassette-COOL2-001 Rev 1.0 (C-03). Munters updated from HCD/MCD to **DSS Pro** per C-19; T-12 regen basis (125 kW/cassette) flagged as T-12a open item pending DSS Pro reconciliation. Load margin at 61.5% is now **+2.3 to +4.3 MW positive** (was negative in Rev 0.5 at old IT load). BOD authority updated to Rev 0.6.

This document is a working draft. Values marked **W** are working estimates. Values marked **L** are locked per BOD-001 §T. Values marked **O** are open pending external input.

---

## 2. Relationship to other documents

**Upstream (this document inherits from):**

- BOD-001 Rev 0.6 — ledger authority for all T-section values
- CHP Cascade White Paper Rev 2.0 (04-CHP/) — first-principles 10 MW platform engineering basis; genset thermal characterization retained as reference
- Cat CG260-16 datasheets (08-Vendors/Cat-gensets/) — genset heat rejection data (direct) and G3520K CHP sheet (proxy)

**Downstream (inherits from this document):**

- ST-TRAP-COOLING-TOWER-001 Rev 0.3 — cooling tower field vendor specification
- ST-TRAP-ELEC-001 Rev 1.3 §6 — cooling plant MCC feeder sizing (gated by T-08 close)
- ST-TRAP-ARCHDIAG-001 — Diagram 3 cooling MCC feeder annotation (gated on T-08)

---

## 3. Site thermal context

**Location:** 22-acre Trappey's Cannery, Vermilion River, Lafayette, Louisiana
**Latitude:** 30.214°N — Gulf Coast climate. ASHRAE 0.4% design dry-bulb: 35°C (95°F), wet-bulb: 28°C (82°F).
**Humidity:** Annual average RH 75–80%. Peak summer 85–90%. Desiccant dehumidification is mandatory for cassette enclosure integrity and GPU reliability — this is an architectural constraint, not a feature option.
**Vermilion River:** Adjacent to the eastern site boundary. Eliminated as a heat sink (see §9.1). Not part of any thermal rejection circuit.

---

## 4. Stage 1 thermal load baseline

| Parameter | Value | Status |
|---|---|---|
| IT load (Stage 1) | 91,080 kW (44 cassettes × 2,070 kW) | L |
| Cassette count | 44 (11 blocks × 4 cassettes/block) | L |
| Genset count | 44 × Cat CG260-16 (4 per block, N+1 per block) | L |
| Genset rated output | 4,000 ekW continuous @ 60 Hz | L |
| Genset operating loading | 61.5% (2,460 ekW continuous) | W — pending Cat CSA |
| Target PUE | ~1.11 (facility ~101.0 MW / IT 91.1 MW) | W |
| Non-IT facility overhead | ~6,100 kW (6.7% of IT) | W |
| Total heat to reject | ~97,180 kW campus | W |

**Rev 0.6 note:** At 61.5% anchor, total electrical generation (108,240 kW) exceeds total site load (~104,000–106,000 kW) by **+2,300 to +4,300 kW positive margin**. Rev 0.5 had negative margin at the old 2,300 kW/cassette IT basis; Rev 0.6 is positive throughout the AI dispatch envelope.

---

## 5. Genset heat rejection characterization

### 5.1 Source data

The CG260-16 is rated at 4,000 ekW continuous, 43.8% electrical efficiency, 42.4% thermal efficiency (LHV basis, heat rejection to jacket water and exhaust to 120°C), 86.2% total (Cat data sheet LEHE21128-00). No Cat-supplied CHP heat balance sheet specific to the CG260-16 is on file; the G3520K CHP specification (LEHE22853-03-1) is used as a proxy engine because the two machines share near-identical thermal efficiency (G3520K: 42.9% vs CG260-16: 42.4%) and the same Cat lean-burn architecture.

**Note on CG260-16 exhaust reference temperature:** The Cat summary sheet (LEHE21128-00) footnote states that for CG260 series operating on biogas, the exhaust reference temperature for thermal efficiency is 180°C rather than the standard 120°C used for other Cat gas engine series. For natural gas operation at Trappeys, 120°C is the operative reference.

### 5.2 G3520K heat rejection data (proxy for CG260-16)

From LEHE22853-03-1, G3520K CHP specification at rated 2,552 ekW (High Efficiency Package, JW outlet 99°C):

| Stream | Recoverable kW | Source |
|---|---|---|
| Jacket water + oil cooler + aftercooler 1 (JW circuit) | 1,372 kW | Cat LEHE22853-03-1 |
| Exhaust gas (LHV to 120°C) | 1,128 kW | Cat LEHE22853-03-1 |
| **Total recoverable thermal** | **2,500 kW** | |
| Electrical output | 2,552 ekW | |
| JW max outlet temperature | 99°C | |

High Response Package (10.5 CR, exhaust 397°C): exhaust heat 1,171 kW, JW circuit 1,411 kW.
High Efficiency Package (11.0 CR, exhaust 372°C): exhaust heat 1,054 kW, JW circuit 1,480 kW.

### 5.3 CG260-16 heat rejection estimates (working, pending Cat CSA)

Scale factor: 4,000 ekW / 2,552 ekW = 1.568. Applied to G3520K High Efficiency values:

| Stream | Per Genset (100% load) | Per Genset (61.5% load, linear) | 44-Genset Campus |
|---|---|---|---|
| JW circuit recoverable | ~2,151 kW | ~1,323 kW | ~58,212 kW |
| Exhaust recoverable (to 120°C) | ~1,769 kW | ~1,088 kW | ~47,872 kW |
| **Total recoverable thermal** | **~3,920 kW** | **~2,411 kW** | **~106,084 kW** |

**Status: W — working estimates.** Linear part-load scaling introduces ±5–8% error. The error band is acceptable for confirming Munters exhaust sizing (5.5 MW draw at Stage 1) but must be replaced with Cat CSA quadratic curve-fit data before final Munters HX sizing.

**Rev 0.6 load margin footnote:** Total electrical output at 61.5% (108,240 kW) now exceeds cassette facility load (~101,000 kW) plus ancillary (3–5 MW) by +2,300 to +4,300 kW. Rev 0.5 had negative margin; Rev 0.6 has positive margin throughout the AI dispatch envelope due to the cassette IT load correction (2,300 kW → 2,070 kW per cassette).

---

## 6. Munters desiccant dehumidification — thermal accounting

### 6.1 Munters slip-stream deduction (Locked, T-12 — T-12a open for DSS Pro reconciliation)

Each cassette houses one **Munters DSS Pro** desiccant dehumidification unit per BOD-001 Rev 0.6 C-19. The Munters unit draws thermal energy from the genset exhaust slip-stream for desiccant regeneration — this is the sole CHP heat recovery load.

| Parameter | Value | Status |
|---|---|---|
| Munters thermal demand per cassette | 125 kW (exhaust slip-stream) | L (T-12) — T-12a open |
| Cassette count | 44 | L |
| **Total Munters deduction** | **5,500 kW (5.5 MW)** | **L (T-12)** |

**T-12a open item:** The 125 kW/cassette regen draw was derived from the HCD/MCD datasheet. BOD-001 Rev 0.6 C-19 specifies Munters DSS Pro. Re-derive regen heat demand from the DSS Pro datasheet and cassette moisture load at Lafayette design-day humidity before this document is locked. Expected range ±30% vs HCD/MCD basis; thermal balance is not sensitive at the campus level — a ±30% shift on Munters moves residual stack heat <2%.

### 6.2 Munters is the sole CHP heat recovery path

| Parameter | Value | Status |
|---|---|---|
| Campus total recoverable thermal (44 gensets at 61.5%) | ~106,084 kW | W |
| Munters deduction (sole CHP recovery, T-12) | 5,500 kW | L |
| **Remaining genset heat (JW + excess exhaust)** | **~100,584 kW** | **W — rejected via JW radiators / exhaust stack** |

---

## 7. Absorption chiller option analysis — Eliminated (Rev 0.5)

The absorption chiller was eliminated from the design in BOD-001 Rev 0.5 (2026-04-22). CHP waste heat no longer drives an LiBr absorption chiller. Options B and C are both withdrawn. Open items TB-5, T-03, HRU-RFQ, and COND-WB are all cancelled. The exhaust backpressure budget analysis (6.7 kPa limit) remains applicable to the exhaust path serving the Munters DSS Pro slip-stream.

---

## 8. Cooling loop topology (Rev 0.6)

The absorption chiller has been eliminated. A single cassette secondary cooling path serves all GPU thermal rejection.

**Loop — Cassette secondary cooling (GPU warm water → cooling towers):**
- **CoolIT CHx2000 external CDU skid** (per Cassette-COOL2-001 Rev 1.0) provides direct-to-chip water-glycol cooling for Vera Rubin NVL72/CPX GPUs
- Supply to GPU: ≤45°C (BOD C-04, Locked)
- Return from GPU: ~50–55°C (working estimate)
- Heat rejection path: CoolIT CHx2000 CDU warm water → cassette ECP warm water supply/return connection → facility cooling water header → plate HX PHX-001 → cooling tower circuit → cooling towers → atmosphere
- Per-cassette secondary cooling load: **~1,656 kW** (W, C-17; rebased from 1,840 kW)

---

## 9. Heat rejection — Vermilion River eliminated; cooling tower is the design basis

### 9.1 Vermilion River — disqualified as heat sink

The Vermilion River is **not available** as a thermal heat sink for this project. Two site-specific conditions eliminate it:

1. **Tidal influence.** The Vermilion River at Lafayette is tidally influenced. Tidal reversal produces bidirectional flow conditions that make it unsuitable as a continuous thermal heat sink.

2. **Ambient water temperature.** Gulf Coast surface water temperatures at Lafayette peak at 30–33°C (86–91°F) in summer months, providing insufficient ΔT for meaningful heat rejection during the months of peak cooling demand.

**Decision:** The Vermilion River is removed from all heat rejection calculations. ST-TRAP-RIVER-001 is cancelled.

### 9.2 Nomenclature clarification — water tower vs cooling towers

**The Trappey's site contains a historic water tower** — a pressurized storage tank structure used in the original cannery operation. It is currently inoperable and is under consideration for restoration as a site landmark. It has no role in the thermal system.

**Cooling towers** referenced throughout this document are purpose-built evaporative heat rejection units — new equipment to be installed as part of the facility build-out.

### 9.3 Cooling towers — primary full-load heat rejection (Rev 0.6)

Cooling towers carry the **full cassette secondary cooling load** — **~72.9 MW at Stage 1** (44 × ~1,656 kW per BOD C-17 W), **~145.7 MW at Full Build**. Towers serve the GPU warm water rejection path directly via plate HX PHX-001.

**Thermodynamic chain (current architecture):**

```
GPU cold plate warm water return (~50–55°C)
        ↓
CoolIT CHx2000 external CDU skid (per Cassette-COOL2-001 Rev 1.0)
  N+1 pumps · 44 units · ~1,656 kW/cassette secondary load (W)
        ↓
Facility warm water header (cassette ECP CHW supply/return connection)
        ↓
Plate heat exchanger PHX-001 (facility/cassette boundary)
        ↓
Cooling tower condenser water circuit
        ↓
Cooling towers (~20,720 RT Stage 1) → reject heat to atmosphere
```

**Governing design condition:** ASHRAE 0.4% wet-bulb 28°C (82°F), Lafayette, Louisiana. At 28°C WB with a 3°C approach, cooling tower supply ~31°C. CDU supply requirement ≤45°C (BOD C-04) — compatible with margin. PHX approach ~14°C.

Sizing the cooling tower field for **~72.9 MW continuous duty** at 28°C WB is the primary thermal design deliverable (T-08, open).

### 9.4 LDEQ / LPDES status

No river discharge. No LPDES thermal discharge permit required. Air emission permitting (LDEQ Minor Source, 40 CFR Part 60 Subpart JJJJ) remains required for genset exhaust stacks. RIVER-001 and LPDES items are struck from the open items ledger.

---

## 10. Thermal balance — Stage 1 campus (working, Rev 0.6)

| Parameter | Value | Status |
|---|---|---|
| IT load | 91,080 kW (44 × 2,070 kW) | L |
| Gensets operating | 44 × CG260-16 at 61.5% (2,460 ekW each) | W |
| Total electrical generation | 108,240 kW | W |
| Load margin at 61.5% | +2,300 to +4,300 kW positive | W |
| JW thermal available (44 gensets at 61.5%) | ~58,212 kW | W |
| Exhaust thermal available (44 gensets, to 120°C) | ~47,872 kW | W |
| Total genset waste heat | ~106,084 kW | W |
| Munters DSS Pro exhaust slip-stream (T-12, sole CHP recovery) | 5,500 kW | L |
| Remaining genset heat (JW + excess exhaust) | ~100,584 kW | W — rejected via JW radiators / exhaust stack |
| **Cassette secondary cooling load (to towers)** | **~72,864 kW (44 × ~1,656 kW, BOD C-17)** | **W** |
| Cooling tower duty (Stage 1) | ~72,864 kW primary | W — pending tower field sizing (T-08) |
| Cooling tower sizing basis | Full cassette secondary load at ASHRAE 0.4% WB 28°C | W |

**Note:** Total genset waste heat (~106 MW) is greater than the cassette secondary cooling demand (~72.9 MW) because genset heat rejection is additional to the IT thermal load. Cooling towers are sized only for the cassette secondary cooling path.

---

## 11. Open items ledger

| Ref | Item | Blocked on | Priority |
|---|---|---|---|
| T-08 | Tower field sizing — **~72.9 MW Stage 1** rejection duty; confirm with COOL-TWR-001 | COOL-TWR-001 | C1 |
| T-09 | Tower makeup water at design day (~747 GPM / ~1.08 MGD) | T-08 close | C1 |
| T-05 | Cooling tower type selection (wet / hybrid / adiabatic) | T-08 heat balance | C1 |
| T-12a | Munters DSS Pro regen reconciliation — re-derive 125 kW/cassette from DSS Pro datasheet | DSS Pro datasheet | C2 |
| Cat CSA | CG260-16 exhaust temperature and mass flow at 61.5% loading — confirms Munters HX sizing and exhaust backpressure budget | Cat application engineering | C1 |
| COOL-TWR-001 | Cooling tower field vendor specification — **~72.9 MW duty**, 28°C WB, plate HX boundary spec | T-08 duty confirmation | C1 |

**Cancelled items (Rev 0.5):** TB-5, T-03, T-11, HRU-RFQ, COND-WB — all eliminated with the absorption chiller.

---

## 12. Revision plan

- **Rev 0.4 (2026-04-18)** — first issue. Working estimates from Cat datasheets, Broad XII catalog, CHP Cascade White Paper Rev 2.0. Vermilion River eliminated as heat sink.
- **Rev 0.5 (2026-04-22)** — absorption chiller eliminated per BOD-001 Rev 0.5. Cooling towers promoted to primary full-load rejection for 80.96 MW Stage 1 cassette secondary cooling load. Open items TB-5, T-03, T-11, HRU-RFQ, COND-WB cancelled.
- **Rev 0.6 (2026-04-23, current)** — IT load rebased to 91,080 kW (44 × 2,070 kW) per BOD Rev 0.6. CDU updated to CoolIT CHx2000 external skid. Munters updated to DSS Pro; T-12a open item added for DSS Pro regen reconciliation. Secondary cooling rebased to ~1,656 kW/cassette; tower duty rebased to ~72.9 MW. Load margin now +2.3 to +4.3 MW positive at 61.5% anchor.
- **Rev 0.7** — after Cat CSA confirms exhaust mass flow and temperature at 61.5% load; updates §5.3 with curve-fit values; T-12a resolved; confirms Munters HX sizing and exhaust backpressure budget.
- **Rev 0.8** — after cooling tower field siting study and tower RFQ; updates §9.3 and §10 with confirmed tower specs and makeup water at design day.
- **Rev 1.0** — all C1 items closed. Paired with ST-TRAP-COOLING-TOWER-001 Rev 1.0.

---

## 13. Approval

Rev 0.6 does not carry external circulation approval. Sign-off inherits from BOD-001 Rev 0.6 approval status. External distribution waits for Rev 1.0, gated on all C1 thermal dependencies closing per BOD-001 §M.

---

**End of ST-TRAP-THERMAL-BASIS Rev 0.6.**
