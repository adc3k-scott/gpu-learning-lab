# ST-TRAP-THERMAL-BASIS — Thermal Architecture Basis — Rev 0.4

**Document:** Thermal Architecture Basis
**Project:** Trappey's AI Center, Lafayette, Louisiana
**Revision:** 0.4 — first issue
**Date:** April 18, 2026
**Owner:** Scott Tomsu
**Status:** Working draft
**Authority:** BOD-001 Rev 0.4 governs all locked values. This document governs T-section (thermal) of the Decision Ledger.

---

## 1. Purpose

This document establishes the thermal architecture basis for the Trappey's AI Center. It defines:

- The cold-sink architecture — how GPU heat is rejected to atmosphere and the Vermilion River
- The CHP cascade framework — how genset waste heat drives absorption cooling and desiccant dehumidification
- The chiller option analysis — the basis for choosing Option B (double-effect hot-water LiBr) or Option C (multi-energy / exhaust-direct) pending vendor RFQ (open item TB-5)
- The Munters desiccant slip-stream accounting (Locked, T-12)
- The regulatory framework — LDEQ / LPDES constraints governing Vermilion River thermal discharge

This document is a working draft. Values marked **W** are working estimates derived from manufacturer datasheets and first-principles scaling. Values marked **L** are locked per BOD-001 §T. Values marked **O** are open pending external input. Downstream documents inherit from this basis; all value changes flow through BOD-001 before appearing here.

---

## 2. Relationship to other documents

**Upstream (this document inherits from):**

- BOD-001 Rev 0.4 — ledger authority for all T-section values
- CHP Cascade White Paper Rev 2.0 (04-CHP/) — first-principles 10 MW platform engineering basis
- Cat CG260-16 datasheets (08-Vendors/Cat-gensets/) — genset heat rejection data (direct) and G3520K CHP sheet (proxy)
- Broad XII Catalog 2018-12 (08-Vendors/Broad/) — absorption chiller rated parameters, drive temperatures, COP

**Downstream (inherits from this document):**

- ST-TRAP-COOLING-TOWER-001 — cooling tower field vendor specification (pending)
- ST-TRAP-RIVER-001 — Vermilion River loop detailed engineering (pending)
- ST-TRAP-ELEC-001 Rev 1.2 §6 — cooling plant MCC feeder sizing (gated by T-08 close)
- ST-TRAP-ARCHDIAG-001 — Diagram 3 cooling MCC feeder annotation (gated on T-08)

---

## 3. Site thermal context

**Location:** 22-acre Trappey's Cannery, Vermilion River, Lafayette, Louisiana
**Latitude:** 30.214°N — Gulf Coast climate. ASHRAE 0.4% design dry-bulb: 35°C (95°F), wet-bulb: 28°C (82°F).
**Humidity:** Annual average RH 75–80%. Peak summer 85–90%. Desiccant dehumidification is mandatory for cassette enclosure integrity and GPU reliability — this is an architectural constraint, not a feature option.
**Vermilion River:** Surface water adjacent to the eastern site boundary. Available as a low-grade heat sink subject to LDEQ / LPDES permit (see §8).

---

## 4. Stage 1 thermal load baseline

| Parameter | Value | Status |
|---|---|---|
| IT load (Stage 1) | 101,200 kW (44 cassettes × 2,300 kW) | L |
| Cassette count | 44 (11 blocks × 4 cassettes/block) | L |
| Genset count | 44 × Cat CG260-16 (4 per block, N+1 per block) | L |
| Genset rated output | 4,000 ekW continuous @ 60 Hz | L |
| Genset operating loading | 61.5% (2,460 ekW continuous) | W — pending Cat CSA |
| Target PUE | 1.06 | W |
| Non-IT facility overhead | ~6,100 kW (6% of IT) | W |
| Total heat to reject | ~107,300 kW campus | W |

---

## 5. Genset heat rejection characterization

### 5.1 Source data

The CG260-16 is rated at 4,000 ekW continuous, 43.8% electrical efficiency, 42.4% thermal efficiency (LHV basis, heat rejection to jacket water and exhaust to 120°C), 86.2% total (Cat data sheet LEHE21128-00). No Cat-supplied CHP heat balance sheet specific to the CG260-16 is on file; the G3520K CHP specification (LEHE22853-03-1) is used as a proxy engine because the two machines share near-identical thermal efficiency (G3520K: 42.9% vs CG260-16: 42.4%) and the same Cat lean-burn architecture.

**Note on CG260-16 exhaust reference temperature:** The Cat summary sheet (LEHE21128-00) footnote states that for CG260 series operating on biogas, the exhaust reference temperature for thermal efficiency is 180°C rather than the standard 120°C used for other Cat gas engine series. For natural gas operation at Trappeys, 120°C is the operative reference. This distinction matters for exhaust heat recovery calculations — heat content between exhaust-out and 120°C is what the 42.4% thermal efficiency figure captures.

### 5.2 G3520K heat rejection data (proxy for CG260-16)

From LEHE22853-03-1, G3520K CHP specification at rated 2,552 ekW (High Efficiency Package, JW outlet 99°C):

| Stream | Recoverable kW | Source |
|---|---|---|
| Jacket water + oil cooler + aftercooler 1 (JW circuit) | 1,372 kW | Cat LEHE22853-03-1 |
| Exhaust gas (LHV to 120°C) | 1,128 kW | Cat LEHE22853-03-1 |
| **Total recoverable thermal** | **2,500 kW** | |
| Electrical output | 2,552 ekW | |
| JW max outlet temperature | 99°C | |

High Response Package (10.5 CR, higher exhaust temp 397°C): exhaust heat 1,171 kW, JW circuit 1,411 kW.
High Efficiency Package (11.0 CR, exhaust 372°C): exhaust heat 1,054 kW, JW circuit 1,480 kW.

G3520 Oil & Gas spec (LEHW20286-03, 2,600 ekW): exhaust 456°C; JW+AC1+OC 1,355 kW; exhaust (LHV to 120°C) 1,654 kW. Noted for reference — O&G variant has higher exhaust temps due to different compression ratio.

### 5.3 CG260-16 heat rejection estimates (working, pending Cat CSA)

Scale factor: 4,000 ekW / 2,552 ekW = 1.568. Applied to G3520K High Efficiency values:

| Stream | Per Genset (100% load) | Per Genset (61.5% load, linear) | 44-Genset Campus |
|---|---|---|---|
| JW circuit recoverable | ~2,151 kW | ~1,323 kW | ~58,212 kW |
| Exhaust recoverable (to 120°C) | ~1,769 kW | ~1,088 kW | ~47,872 kW |
| **Total recoverable thermal** | **~3,920 kW** | **~2,411 kW** | **~106,084 kW** |

**Status: W — working estimates.** Linear part-load scaling introduces ±5–8% error because exhaust enthalpy drops faster at part load than jacket water heat. The CHP Cascade White Paper Rev 2.0 documents a +0.6% deviation from linear at 79.2% loading on G3520H (exhaust shortfall offset by JW surplus). The error band is acceptable for architecture-phase sizing but must be replaced with Cat CSA quadratic curve-fit data before chiller RFQ.

**Exhaust temperature (estimated):** The CG260-16 exhaust outlet temperature is not confirmed by Cat CSA. Based on the G3520K at similar compression ratio, working estimate is 372–420°C. This estimate is critical for Option B vs Option C selection (§7).

---

## 6. Munters desiccant dehumidification — thermal accounting

### 6.1 Munters slip-stream deduction (Locked, T-12)

Each cassette houses one Munters HCD/MCD desiccant dehumidification unit. The Munters unit draws thermal energy from the genset exhaust slip-stream for desiccant regeneration — this is the thermal load that is deducted from the heat available to drive the absorption chillers.

| Parameter | Value | Status |
|---|---|---|
| Munters thermal demand per cassette | 125 kW (exhaust slip-stream) | L (T-12) |
| Cassette count | 44 | L |
| **Total Munters deduction** | **5,500 kW (5.5 MW)** | **L (T-12)** |

### 6.2 Net thermal available for absorption cooling

| Parameter | Value | Status |
|---|---|---|
| Campus total recoverable thermal (44 gensets at 61.5%) | ~106,084 kW | W |
| Munters deduction | 5,500 kW | L |
| **Net available for absorption chillers** | **~100,584 kW** | **W** |

---

## 7. Absorption chiller option analysis

### 7.1 Option A — single-stage direct-fired chiller

**Eliminated.** Option A (Broad BZ series direct-fired absorption chiller, gas-to-cold) wastes the CHP thermodynamic advantage entirely by burning additional natural gas to drive the chiller rather than recovering genset waste heat. Rated COP 1.42. This option is architecturally incompatible with the CHP cascade framework.

### 7.2 Option B — double-effect hot-water chiller

**Architecture:** Genset exhaust → heat recovery unit (HRU, plate-fin, counter-flow) → hot water circuit at 180°C / 165°C (356°F / 329°F inlet / outlet) → Broad BH two-stage hot water absorption chiller → chilled water at 6.7°C (44°F) → facility cold distribution.

**Source data (Broad XII Catalog 2018-12, page 14, BH series):**

| Parameter | Value |
|---|---|
| Chiller type | Two-stage (double-effect) LiBr absorption |
| Drive medium | Hot water |
| Rated hot water inlet temperature | 180°C (356°F) |
| Rated hot water outlet temperature | 165°C (329°F) |
| Rated chilled water outlet / inlet | 6.7°C / 13.7°C (44°F / 56.7°F) |
| Rated cooling water outlet / inlet | 37°C / 29°C (97.5°F / 85°F) |
| Rated cooling COP | ~1.50 (implied from BEY exhaust-driven equivalent) |
| Capacity range (catalog) | 66–3,307 RT (233–11,630 kW) |
| Designed lifespan | 60 years (titanium tubes) |

**Thermal feasibility:** CG260-16 exhaust at 372–420°C (estimated) is well above 180°C. An exhaust-to-hot-water HRU (plate-fin heat exchanger, vendor RFQ required — Cain Industries / E-Tech as candidates per CHP Cascade White Paper §7) can extract heat down to 120°C exhaust leaving temperature and produce 180°C hot water. Thermal feasibility is confirmed in principle; sizing confirmation requires Cat CSA exhaust mass flow and temperature curves.

**Exhaust backpressure constraint:** Per Cat G3520H application guide (applicable to CG260-16 by family), maximum exhaust backpressure is 6.7 kPa (27 inH₂O). The HRU must be RFQ'd with backpressure as a binding constraint. Based on the CHP Cascade White Paper §7, a plate-fin HRU contributes 2.0–2.5 kPa. Combined with oxidation catalyst (0.5–0.8 kPa), Munters tee (0.2–0.3 kPa), and stack (0.3–0.5 kPa), total exhaust pressure drop is 3.5–4.9 kPa with 1.8–3.2 kPa margin (27–48%) to the 6.7 kPa limit. Achievable with coordinated HRU + catalyst RFQ.

**COP working estimate at campus scale (Option B):**

| Parameter | Working Value | Basis |
|---|---|---|
| Available thermal to absorption (after Munters) | 100,584 kW | W |
| Operating COP (double-effect, part-load) | 1.40 | Conservative: rated 1.50 derated to 1.40 at part-load |
| Absorption cooling delivered | 140,818 kW | W |
| Total campus cooling demand (IT + overhead) | ~107,300 kW | W |
| Absorption coverage | >100% — chiller capacity exceeds demand | W |
| Excess capacity margin | ~33 MW absorbed cooling | W |
| Disposition of excess margin | Trim cooler, partial-load chiller staging, or Vermilion River | O |

Note: The high thermal-to-cooling ratio (>100% at COP 1.40) is characteristic of double-effect architecture at this scale. Chiller staging (individual block chillers running at part load rather than fewer chillers at full load) manages this; the excess is an advantage, not a problem.

**Option B status:** Architecturally preferred. HRU adds one more component in the exhaust path requiring coordinated RFQ. Primary risk is exhaust temperature variability — if the Cat CSA confirms CG260-16 exhaust substantially below 372°C at 61.5% load, the HRU hot water output temperature may drop and reduce the effective drive temperature. This risk is mitigated by specifying the HRU for 99°C jacket water supplementation of the hot water circuit.

### 7.3 Option C — exhaust-direct (multi-energy / two-stage exhaust chiller)

**Architecture:** Genset exhaust ducted directly to Broad BE two-stage exhaust absorption chiller. No intermediate HRU or hot-water loop.

**Source data (Broad XII Catalog 2018-12, page 14, BE series):**

| Parameter | Value |
|---|---|
| Chiller type | Two-stage (double-effect) LiBr absorption |
| Drive medium | Exhaust gas direct |
| Rated exhaust inlet temperature | 500°C (932°F) |
| Rated exhaust outlet temperature | 160°C (320°F) |
| Rated chilled water outlet / inlet | 6.7°C / 13.7°C (44°F / 56.7°F) |
| Rated cooling water outlet / inlet | 37°C / 29°C (97.5°F / 85°F) |
| Rated cooling COP | 1.50 |
| Capacity range (catalog) | 66–3,307 RT (233–11,630 kW) |

**Exhaust temperature gap (critical finding):**

| Parameter | Value | Status |
|---|---|---|
| Broad BE rated exhaust inlet | 500°C (932°F) | L (catalog) |
| CG260-16 estimated exhaust outlet | 372–420°C | W — pending Cat CSA |
| Temperature gap | 80–128°C below rated drive temp | W |
| Effect | Chiller operates below rated capacity; actual COP and cooling output derated | W |

The estimated 372–420°C CG260-16 exhaust is 80–128°C below the Broad BE rated drive temperature. While Broad chillers can operate below rated drive temperature with reduced output, the capacity and COP derating must be quantified via Broad application engineering before this option can be sized. The Broad multi-energy chiller (BZE series) — which combines exhaust + direct-fired gas supplementation — could bridge this gap by topping up the exhaust energy with burner heat to reach effective drive temperature.

**Broad BZE multi-energy option:** The BZE series (Broad XII, page 17) combines exhaust (932°F rated) and direct-fired natural gas as hybrid energy sources. For Trappeys, this means: low-temperature exhaust provides primary heat, direct-fired gas burner compensates for the temperature shortfall. COP not explicitly stated for BZE but is lower than exhaust-only operation because additional gas input reduces the effective waste-heat fraction.

**Option C status:** Feasible in principle but carries a material temperature-gap risk pending Cat CSA exhaust characterization. If the Cat CSA confirms exhaust ≥450°C at 61.5% load, the gap narrows and Option C becomes more attractive. If exhaust is confirmed at 372–380°C, Option B (with HRU producing 180°C hot water) is thermally superior because the HRU can efficiently extract to 120°C leaving temperature regardless of the 500°C rated threshold.

### 7.4 Option B vs Option C summary and recommendation

| Factor | Option B (Double-effect hot water via HRU) | Option C (Exhaust-direct BE / BZE) |
|---|---|---|
| Chiller drive temp match | Full match — HRU produces 180°C water from any exhaust ≥200°C | Gap risk — rated 500°C; CG260-16 exhaust 372–420°C (estimated) |
| Chiller COP (rated) | ~1.50 | 1.50 (at full drive temp) |
| Chiller COP (operating) | ~1.40 (estimated part-load derate) | Unknown pending Cat CSA + Broad app eng |
| HRU requirement | Yes — plate-fin, coordinated RFQ | No (direct duct connection) |
| Exhaust backpressure | HRU adds 2.0–2.5 kPa; manageable within 6.7 kPa budget | Chiller shell direct: lower backpressure |
| Jacket water integration | JW can supplement HRU hot water header (robust) | JW integration requires separate PHE cascade |
| N+1 thermal resilience | JW header pools across block; robust during genset trip | Exhaust-direct: one genset trip cuts one chiller entirely |
| Chiller vendor footprint | Standard product (BH series) | Larger shell required for direct exhaust duct |
| **Current recommendation** | **Preferred architecture** | **Contingency if Cat CSA confirms high exhaust temp** |

**TB-5 resolution path:** Option B vs C selection gates on (1) Cat CSA returning confirmed exhaust temperature and mass flow at 61.5% load, and (2) Broad / Thermax application engineering confirming derating curve for Option C at the confirmed exhaust temperature. Until Cat CSA is received, Option B is the working architecture for all downstream sizing.

---

## 8. CHW temperature compatibility — Boyd CDU (Open Item T-11)

### 8.1 Loop topology (working)

The facility cooling architecture operates two physically separated water loops:

**Loop 1 — GPU liquid cooling (warm water):**
- Boyd CDU provides direct-to-chip water-glycol cooling for Vera Rubin NVL72 GPUs
- Supply to GPU: ≤45°C (BOD C-03, Locked)
- Return from GPU: ~50–55°C (working estimate)
- Heat rejection path: Boyd CDU → facility warm water header → adiabatic dry cooler (separate from absorption chiller condenser tower) → ≤45°C supply return
- Absorption chiller is not in the primary GPU heat rejection path

**Loop 2 — Facility cold distribution:**
- Absorption chiller produces 6.7°C (44°F) chilled water
- Chilled water serves: Munters HCD/MCD cooling-side air stream, facility space conditioning, NOC/office, electrical room cooling
- Return to chiller: ~13.7°C (56.7°F)

### 8.2 T-11 open item

**T-11: Boyd CDU CHW supply 7–12°C compatibility.** This item is confirming whether any sub-loop of the Boyd CDU system (e.g., a pre-conditioning heat exchanger between the absorption chiller CHW and the Boyd supply manifold) requires 7–12°C input. If the Boyd CDU supply circuit is purely a closed warm-water loop (no tie to the 7°C chiller), T-11 resolves by separation — the two loops are isolated and temperature compatibility is not a constraint. If a direct-expansion or indirect PHE tie is specified between the 7°C chiller and the Boyd warm-water supply, the Boyd CDU operating range at ≤45°C supply is well above the 7°C floor and compatibility is confirmed.

**Resolution:** Boyd CDU application engineering call with confirmed supply temperature range and loop isolation confirmation. Priority C1 — gates cooling loop mechanical design.

---

## 9. Heat rejection — Vermilion River eliminated; cooling tower is the design basis

### 9.1 Vermilion River — disqualified as heat sink

The Vermilion River is **not available** as a thermal heat sink for this project. Two site-specific conditions eliminate it:

1. **Tidal influence.** The Vermilion River at Lafayette is tidally influenced. Tidal reversal produces bidirectional flow conditions that make it unsuitable as a continuous thermal heat sink. During tidal reversal events, the effective flow available for heat dilution can drop to near-zero or reverse direction, eliminating the mixing volume required for any regulated thermal discharge.

2. **Ambient water temperature.** Gulf Coast surface water temperatures at Lafayette peak at 30–33°C (86–91°F) in summer months. The Broad XII absorption chiller condenser/absorber cooling water requires inlet ≤29°C (85°F) at rated conditions. A river at ambient 30–33°C cannot serve as a condenser water source without a pre-cooler, which negates the economic and complexity advantage of a river loop. The river cannot provide meaningful ΔT for heat rejection during the months of peak cooling demand.

**Decision:** The Vermilion River is removed from all heat rejection calculations. ST-TRAP-RIVER-001 is cancelled. The pending documents list in the README will be updated accordingly.

### 9.2 Nomenclature clarification — water tower vs cooling towers

**The Trappey's site contains a historic water tower** — a pressurized storage tank structure used in the original cannery operation. It is currently inoperable and is under consideration for restoration as a site landmark. It has no role in the thermal system.

**Cooling towers** referenced throughout this document are purpose-built evaporative heat rejection units — mechanical draft towers that reject condenser/absorber heat from the absorption chillers to atmosphere. These are new equipment to be installed as part of the facility build-out. They are not related to the existing site water tower in any way.

### 9.3 Cooling towers in the CHP cascade — primary heat rejection

Cooling towers are **the primary heat rejection path** in the CHP cascade, not backup or trim. The complete thermodynamic chain is:

```
Genset exhaust + jacket water
        ↓
Absorption chiller (hot-water drive, Option B)
        ↓ produces chilled water (6.7°C / 44°F)
Facility cold distribution (Munters, space conditioning)
        ↓ condenser/absorber circuit
Cooling towers → reject heat to atmosphere
```

The cooling tower handles the condenser/absorber rejection for the absorption chillers — this is a continuous, full-load duty, not a peak-day supplement. Sizing the cooling tower correctly is therefore a primary design deliverable, not an ancillary one.

**Governing design condition:** ASHRAE 0.4% wet-bulb 28°C (82°F), Lafayette, Louisiana. Cooling tower must supply condenser water to the absorption chiller at ≤29°C (85°F) at or below this wet-bulb condition.

**Chiller condenser circuit limit:** Broad BH / BE series rated condenser cooling water inlet 29°C (85°F). At 28°C wet-bulb with a 2°C approach, tower supply reaches 30°C — 1°C above the Broad rated inlet. Broad application engineering must confirm acceptable operating envelope at 30°C condenser water inlet (expected to result in a 3–5% capacity derating at peak conditions, not a disqualification). This is an RFQ input item (COND-WB).

**GPU warm water loop:** The Boyd CDU warm water return (~50–55°C) is at temperatures far above wet-bulb and can be rejected via a separate adiabatic dry cooler or a dedicated circuit on the cooling tower, isolated from the absorption chiller condenser circuit to avoid thermal cross-contamination.

### 9.4 LDEQ / LPDES status

No river discharge. No LPDES thermal discharge permit required. Air emission permitting (LDEQ Minor Source, 40 CFR Part 60 Subpart JJJJ) remains required for the genset exhaust stacks. RIVER-001 and LPDES items are struck from the open items ledger.

---

## 10. CHP cascade heat balance — Stage 1 campus (working)

Summary table using Option B architecture at 61.5% genset loading:

| Parameter | Value | Status |
|---|---|---|
| IT load | 101,200 kW | L |
| Gensets operating | 44 × CG260-16 at 61.5% (2,460 ekW each) | W |
| Total electrical generation | 44 × 2,460 = 108,240 kW | W |
| JW thermal available (44 gensets) | ~58,212 kW | W |
| Exhaust thermal available (44 gensets, to 120°C) | ~47,872 kW | W |
| Total waste heat available | ~106,084 kW | W |
| Munters slip-stream deduction (T-12, Locked) | 5,500 kW | L |
| Net thermal to absorption chillers | ~100,584 kW | W |
| Absorption COP (Option B, double-effect, part-load) | 1.40 | W |
| Absorption cooling delivered | ~140,818 kW | W |
| Campus cooling demand (IT + overhead) | ~107,300 kW | W |
| Absorption coverage | >100% | W |
| Chiller staging required | Yes — operate chillers at part load, not all at full | W |
| Cooling tower duty | Primary continuous heat rejection for absorption chiller condenser circuit | L |
| Cooling tower sizing basis | Full campus condenser + absorber load at ASHRAE 0.4% wet-bulb 28°C | W |

**Note on coverage >100%:** The double-effect architecture at this scale delivers more absorption cooling capacity than demand at full genset thermal output. This headroom is intentional — it absorbs hot-day condenser water temperature increases, accommodates N+1 genset-trip partial-load operation, and allows chiller staging (running fewer units at higher load rather than all units at very low load). The cooling towers are sized for full continuous condenser duty, not for transient or trim use.

**Key uncertainty:** The COP 1.40 operating estimate must be validated by the chiller vendor application engineering as part of the RFQ (TB-5). The Broad XII catalog COP values are rated at standard conditions (29°C cooling water, 6.7°C chilled water). Gulf Coast wet-bulb conditions will affect condenser performance; hot-day derating is expected to be 5–10%.

---

## 11. Open items ledger

| Ref | Item | Blocked on | Priority |
|---|---|---|---|
| TB-5 | Absorption chiller RFQ — Option B or C selection | Cat CSA exhaust temp + Broad/Thermax app eng | C1 |
| T-03 | Chiller type selection (Option B vs C) — BOD Working entry | TB-5 close | C1 |
| T-08 | CHP heat balance final values — JW + exhaust recovery, 5.5 MW Munters deduction applied | Cat CSA part-load curves | C1 |
| T-11 | Boyd CDU CHW supply 7–12°C compatibility confirmation | Boyd CDU app eng call | C1 |
| HRU-RFQ | Exhaust HRU vendor RFQ (Option B) — Cain / E-Tech / Rentech; backpressure as binding spec | Cat CSA exhaust mass flow + temp | C1 |
| Cat CSA | CG260-16 exhaust temperature, mass flow, and part-load heat rejection curves at 61.5% loading | Cat application engineering | C1 |
| COOL-TWR-001 | Cooling tower field vendor specification — wet-bulb 28°C design, condenser water ≤29°C confirmation with Broad | T-08 heat balance final + TB-5 | C2 |
| COND-WB | Broad chiller app eng confirmation of condenser water inlet spec at 28–30°C wet-bulb conditions | Broad RFQ | C2 |

---

## 12. Revision plan

- **Rev 0.4 (current)** — first issue. Working estimates from Cat datasheets (CG260-16 rated + G3520K CHP proxy), Broad XII catalog, and CHP Cascade White Paper Rev 2.0. Option B vs C analysis complete; selection deferred to TB-5 RFQ close. Vermilion River eliminated as heat sink (tidal influence + summer ambient temp); dry cooling tower confirmed as design basis.
- **Rev 0.5** — after Cat CSA returns exhaust temperature and part-load curves. Updates §5.3 heat balance with curve-fit values; may resolve T-03 chiller option selection.
- **Rev 0.6** — after Broad / Thermax RFQ closes. Updates §7 with locked chiller model selection, rated capacity, and confirmed COP at project operating conditions.
- **Rev 1.0** — all C1 items closed. Paired with ST-TRAP-COOLING-TOWER-001 Rev 1.0.

---

## 13. Approval

Rev 0.4 does not carry external circulation approval. Sign-off inherits from BOD-001 Rev 0.4 approval status. External distribution waits for Rev 1.0, gated on all C1 thermal dependencies closing per BOD-001 §M.

---

**End of ST-TRAP-THERMAL-BASIS Rev 0.4.**
