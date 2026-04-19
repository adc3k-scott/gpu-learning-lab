# ST-TRAP-SOLAR-001 — Solar Integration — Rev 0.1

**Document:** Solar Array Integration — Architecture and Specification Basis
**Project:** Trappey's AI Center, Lafayette, Louisiana
**Revision:** 0.1 — first issue
**Date:** April 18, 2026
**Owner:** Scott Tomsu
**Status:** Working draft
**Authority:** BOD-001 Rev 0.4 governs all locked values (E-14 through E-17). ELEC-001 Rev 1.2 §9 establishes the bus integration topology. This document provides the detailed specification basis and DC-DC buck converter RFQ anchor.

W = Working estimate · L = Locked per BOD-001 · O = Open

---

## 1. Purpose

This document establishes the solar array integration basis for the Trappey's AI Center. It defines:

- Panel specification and array configuration
- String voltage and current analysis across Louisiana seasonal temperature range
- DC-DC buck converter specification (1,500 VDC → 800 VDC, MPPT)
- 800 VDC bus interface topology
- AMCL MPPT and dispatch integration
- Energy production estimates and operating role
- ITC incentive basis and First Solar engagement path
- Open items and DC-DC buck vendor RFQ anchor (E-22)

---

## 2. Relationship to other documents

**Upstream (this document inherits from):**

- BOD-001 Rev 0.4 — E-14 through E-17 are the locked source entries
- ELEC-001 Rev 1.2 §9 — bus integration topology; DC-DC buck position on 800 VDC bus
- ARCHDIAG-001 Rev 0.1 — Diagram 3 shows solar DC-DC tie on 800 VDC bus

**Downstream (inherits from this document):**

- ST-TRAP-SLD-001 — formal single-line; solar SSCB and DC-DC conductor sizing
- ST-TRAP-PROT-001 — protection coordination at solar bus tie; SSCB settings
- DC-DC buck converter RFQ (E-22, not yet issued)

---

## 3. Panel specification — First Solar Series 7 TR1

### 3.1 Module data (High Bin)

| Parameter | Value | Status |
|---|---|---|
| Model | FS-7550A-TR1 | L |
| Technology | CdTe thin-film | L |
| STC power (High Bin) | 550 W | L |
| Module efficiency | 19.7% | L |
| Cell efficiency | 20.6% | L |
| Vmp (MPP voltage) | 190.4 V | L |
| Imp (MPP current) | 2.89 A | L |
| Voc (open circuit) | 228.8 V | L |
| Isc (short circuit) | 3.08 A | L |
| Dimensions | 2,300 × 1,216 mm | L |
| Module area | 2.80 m² | L |
| Weight | 38.47–39.7 kg (84.8–87.5 lbs) | L |
| Temperature coefficient (Pmax) | −0.32%/°C | L |
| Max system voltage | 1,500 VDC | L |
| Connector | TE Connectivity PV4-S | L |
| Orientation | Portrait only | L |

### 3.2 Warranted performance

| Parameter | Value |
|---|---|
| Product warranty | 12 years |
| Linear performance warranty | 30 years — 98% Year 1; 0.3%/year degradation; >89% Year 30 |
| Cell cracking warranty | Yes — only manufacturer with this warranty |
| LID / LeTID | None — CdTe is immune |
| Salt air certification | IEC 61701 — suitable for Gulf Coast coastal environment |

### 3.3 Louisiana climate advantage — CdTe over silicon

| Factor | CdTe Series 7 vs standard silicon |
|---|---|
| Temperature coefficient | −0.32%/°C vs silicon −0.35 to −0.45%/°C — better hot-weather performance |
| Hot climate annual bonus | ~+2% annual energy production |
| Humid climate annual bonus | ~+4% annual energy production |
| Hurricane zone | Immune to cell cracking — silicon cell cracking warranty void in high-wind events |
| LID first-year loss | Zero — no light-induced degradation |
| **Net 30-year advantage (Louisiana)** | **~+6% cumulative vs silicon** |

---

## 4. Array specification

| Parameter | Value | Status |
|---|---|---|
| Total panel count | 3,731 | L |
| Total DC capacity | 2.05 MW | L |
| Rooftop locations | Buildings B1 and B2 (BOD B-01, B-02) | L |
| String configuration | 5 panels in series | L |
| Complete strings | 746 (3,730 panels) | W |
| Remaining panel | 1 (spare / partial string) | W |
| Total strings | 746 | W |
| String combiner boxes | TBD — one per roof section (E-22 scope) | O |

**Panel count check:** 746 strings × 5 panels = 3,730 panels × 550 W = 2,051.5 kW ≈ 2.05 MW. ✓

**Structural note:** BOD B-07 (structural assessment status) is Open — no structural assessment has been commissioned for B1 or B2. Rooftop solar loading must be confirmed by structural engineer before installation. Panel weight: 38.5–39.7 kg per panel × 3,731 panels = ~143,700–148,100 kg (317,000–326,000 lbs) array weight, before mounting hardware and ballast. Structural assessment is a C2 dependency gating final rooftop layout.

---

## 5. String voltage and current analysis

The 5-panel string is designed specifically for the 800 VDC bus. The string voltage must remain above 800V at MPP across the full operating temperature range, and below 1,500V at Voc under the coldest expected conditions.

### 5.1 Voltage analysis

| Condition | Cell temp | String MPP voltage | String Voc | 1,500V limit |
|---|---|---|---|---|
| STC (reference) | 25°C | 5 × 190.4V = **952V** | 5 × 228.8V = **1,144V** | ✓ Within |
| Summer peak (Lafayette) | 45°C (cell) | 952V × (1 + (−0.32% × 20)) = **~891V** | < 952V | ✓ Above 800V |
| Winter cold | 5°C (cell) | 952V × (1 + (−0.32% × −20)) = **~1,013V** | 5 × 228.8V × (1 − (−0.32%/°C × (5−25))) = **~1,208V** | ✓ Within |
| Extreme cold (record) | −5°C (cell) | ~1,074V MPP | ~1,280V Voc | ✓ Within 1,500V |

**Key finding:** String MPP voltage stays above 800V across the full Louisiana temperature range. The DC-DC buck converter must track MPPT from ~891V (summer MPP) to ~1,013V (winter MPP). No string reconfiguration required seasonally.

### 5.2 Current analysis

| Parameter | Value |
|---|---|
| String current at MPP (Imp) | 2.89 A per string |
| String current at Isc | 3.08 A per string |
| Total array current at MPP (746 strings) | 746 × 2.89A = **2,155 A** at ~952V |
| Total power at MPP (STC) | 2,155A × 952V = 2,052 kW ✓ |

---

## 6. DC-DC buck converter specification

The DC-DC buck converter is the interface between the 1,500 VDC solar string field and the 800 VDC common busway. It performs three functions simultaneously: voltage step-down (1,500→800V), MPPT (maximizing array output), and bus interface (regulating output to 800 VDC bus voltage).

**This is open item E-22.** Delta Electronics is the preferred vendor (aligned with in-row power rack selection E-24). Vendor RFQ to be issued from this specification.

### 6.1 Electrical requirements

| Parameter | Requirement | Notes |
|---|---|---|
| Input voltage range (MPPT) | 800–1,500 VDC | Must track MPP from ~891V (summer) to ~1,013V (winter) |
| Input voltage range (operating) | 800–1,500 VDC | Same range as MPPT |
| Input voltage absolute maximum | 1,500 VDC | IEC 62109-2 rated |
| Output voltage | 800 VDC ±1% | Regulated — must not deviate to maintain bus stability |
| Maximum input current | ~2,200 A total array | Distribute across multiple converter units |
| Total rated power | 2.05 MW | See §6.2 for preferred multi-unit configuration |
| Efficiency | ≥97% at rated power | SiC switching preferred |
| MPPT algorithm | Required — single or multi-MPPT depending on unit configuration | Must handle partial shading per roof section independently |
| Galvanic isolation | Required or confirm ground-fault detection if non-isolated | Solar array negative must be isolated from 800 VDC bus negative |
| Output regulation | Must hold 800 VDC against bus voltage transients (BESS and load swings) | |
| Protection | Input overvoltage, output overvoltage, overcurrent, arc-fault detection, GFDI | |
| Communications | Modbus TCP to L1 block PLC — power output, MPPT point, fault status, string current per combiner | |

### 6.2 Preferred multi-unit configuration

One large 2 MW converter carries a single point of failure for the entire array. Distributed architecture is preferred:

| Option | Configuration | Units | Per-unit power | Advantage |
|---|---|---|---|---|
| **A (preferred)** | One unit per roof section | 4 | ~512 kW | Independent MPPT per section; partial shading isolated; N partial redundancy |
| B | Two units | 2 | ~1,025 kW | Simpler wiring; 50% production loss on one unit failure |
| C | One unit | 1 | 2,050 kW | Simplest; full production loss on failure |

**Option A preferred.** Four roof sections on B1 and B2, one converter per section, each with independent MPPT. Partial shading from HVAC equipment, antennas, or adjacent structures on one section does not derate other sections. Each unit output connects to 800 VDC bus via dedicated SSCB + blocking diode.

### 6.3 Vendor shortlist (E-22, open)

| Vendor | Products | Notes |
|---|---|---|
| **Delta Electronics** | DC-DC power conversion — 800 VDC product line | Preferred — already selected for in-row power racks (E-24). Single-vendor advantage for 800 VDC bus products. Confirm 1,500 VDC input solar MPPT buck at 500 kW scale. |
| SMA Solar Technology | Core1, Sunny Highpower series | Strong solar MPPT history; confirm DC-to-DC (no inverter) product at this voltage |
| ABB | TRIO series DC-DC | Broad power range; confirm 1,500V input to 800V regulated output |
| Ampt | String optimizer / central MPPT | Different architecture — per-string optimization feeding 800V rail; evaluate as alternative to section-level buck |

---

## 7. 800 VDC bus interface

### 7.1 Connection topology

```
First Solar Series 7 strings (1,500 VDC)
  ↓ string combiner boxes + DC disconnects
  ↓ DC-DC buck converter (1,500 → 800 VDC, MPPT)
  ↓ SSCB (solid-state circuit breaker)
  ↓ blocking diode (prevents bus backfeed into converter on bus fault)
  ↓ 800 VDC common busway
```

**SSCB at bus tie:** Sub-millisecond trip. Coordinates with blocking diode — on a bus fault, blocking diode prevents reverse current; SSCB isolates converter output from bus. On converter fault, SSCB trips and isolates. Ratings for SLD-001.

**Blocking diode:** Prevents bus fault energy from back-feeding into the DC-DC converter and potentially into the solar array. Required at every DC source tie per protection philosophy (ELEC-001 §10).

**Auxiliary power:** Solar DC-DC buck converter controls and cooling require ~10 kW per unit from a dedicated 480 VAC feeder (BOD E-29 solar buck aux line item: ~10 kW per block).

### 7.2 Block allocation

The solar array is physically located on B1 and B2 rooftops. The 800 VDC bus is a per-block architecture with 11 independent blocks. Solar DC output connects to the bus of the block(s) whose distribution runs nearest to B1/B2.

| Parameter | Value | Status |
|---|---|---|
| Solar allocation per block (nominal) | ~186 kW (2.05 MW / 11 blocks) | W — routing dependent |
| Actual allocation | Blocks physically nearest B1/B2 receive tie; others carry zero solar | W |
| AMCL dispatch implication | L3 dispatch models blocks with solar separately from blocks without | W |

**Note:** Solar does not power blocks on the far end of the campus from B1/B2 unless a dedicated solar distribution feeder is run — this is a design decision for SLD-001. The base case is local tie only.

---

## 8. AMCL integration

| AMCL Level | Solar Functions |
|---|---|
| L0 — field devices | String current sensors per combiner; DC-DC converter power output meter; MPPT operating point; fault/alarm status |
| L1 — block PLC | MPPT coordination setpoint to DC-DC converter; solar bus SSCB control; anti-islanding (N/A — no grid, no anti-islanding needed); zero-export enforcement (no excess to utility) |
| L2 — plant SCADA | Solar production historian; string-level fault logging; daily/monthly yield tracking |
| L3 — AMCL AI dispatch | Solar recapture coordination with BESS: when PV production exceeds instantaneous load minus minimum genset output, direct excess to BESS charge. Solar-aware genset dispatch: during peak solar, reduce genset loading toward 55% floor while maintaining frequency stability. Diurnal production forecast integration for BESS pre-charging. |

**Key L3 logic:** Solar is subordinate and supplemental. Gensets are never shut down for solar production — they hold minimum loading for frequency stability. Solar offsets gas consumption at the margin. BESS captures solar clip rather than MPPT throttling.

---

## 9. Energy production and operating role

### 9.1 Production estimates

| Parameter | Value | Basis |
|---|---|---|
| Array capacity | 2.05 MW DC | L |
| Louisiana annual irradiance (specific yield) | ~1,750 kWh/kWp | W — industry average for Lafayette; actual yield study required |
| Estimated annual production | ~3,588 MWh/year (~3.6 GWh/year) | W |
| CdTe climate bonus vs silicon | +6% cumulative over 30 years | L (First Solar data) |
| Year 1 production (no LID loss) | ~3,588 MWh | W |
| Year 30 production (>89% of rated) | ~3,193 MWh | W |
| Campus annual generation (108.24 MW × 8,760 h × capacity factor ~0.90) | ~853,000 MWh | W |
| Solar offset fraction | ~0.42% annual average | W |
| Peak midday production (clear day, 22°C ambient) | ~1.85 MW | W |
| Peak instantaneous offset vs campus load (108.2 MW) | ~1.7% | W |

### 9.2 Operating role

Solar is **subordinate and supplemental** to the genset-BESS base load. It does not affect any primary sizing decisions and is not credited in contingency calculations. Its value is:

1. **Gas displacement:** ~3,588 MWh/year of genset output replaced by solar → direct fuel cost reduction.
2. **BESS synergy:** Peak solar charges BESS when gensets are at minimum load floor → enables tighter genset dispatch optimization.
3. **Narrative and incentive:** First Solar Series 7 made 30 miles away in New Iberia, LA. First solar-to-800V-AI-factory direct DC coupling reference architecture. Solar ITC on total CapEx (see §10).
4. **Resiliency margin:** Solar production during daylight hours reduces genset loading, extending engine TBO intervals.

**What solar does not do:** It does not reduce the genset count. It does not reduce the BESS sizing. It does not feed the grid. It does not create a net-zero claim.

---

## 10. ITC and First Solar incentives

| Item | Value | Notes |
|---|---|---|
| Federal Solar ITC (base) | 30% | IRC §48E — investment tax credit on solar CapEx |
| Domestic content adder | +10% possible → 40% total | First Solar: US-manufactured in Perrysburg, Ohio + New Iberia, LA. Strong domestic content claim. Confirm with tax counsel. |
| Estimated module cost | $575K–$720K | First Solar market rate $0.28–0.35/W; multi-year offtake typical |
| Estimated total solar CapEx | $2.5M–$3.5M | Modules + DC-DC converters + mounting hardware + wiring + structural reinforcement |
| ITC at 30% | $750K–$1.05M | |
| ITC at 40% (domestic content) | $1.0M–$1.4M | |
| LA state incentives | Additive — confirm with LED | Act 730, ITEP may apply to solar equipment |
| Lead time | 6–12 months | New Iberia factory proximity may enable expedited delivery — engage First Solar directly |

---

## 11. First Solar engagement

| Contact | Details |
|---|---|
| Module Sales | modulesales@firstsolar.com |
| Technical Support | technicalsupport@firstsolar.com |
| General | Info@FirstSolar.com |
| Phone | 419-662-6899 |
| New Iberia factory | 1400 Corporate Drive, Iberia Parish, LA 70560 — 30 miles from Trappeys |

**Engagement framing:** Lead with the reference architecture story — first DC-direct 1,500V solar to 800V AI factory bus anywhere. First Solar made in Louisiana powering Louisiana's anchor AI factory. Documented and publishable. First Solar has been looking for an AI factory reference customer — this is it.

**Pricing lever:** Multi-year offtake agreements are typical. If Full Build uses 2.05 MW × 2 (Stage 1 + Stage 2) = 4.1 MW, plus potential replication across MARLIE I and other ADC sites, total pipeline is 10+ MW. Frame at portfolio scale.

---

## 12. Open items ledger

| Ref | Item | Blocked on | Priority |
|---|---|---|---|
| E-22 | DC-DC buck converter vendor RFQ — Delta preferred, 4-unit configuration | This document — issue RFQ from §6 | C1 |
| B-07 | Structural assessment B1 and B2 — rooftop loading for 143,700+ kg array | Structural engineer commission | C2 |
| LAYOUT | Rooftop layout design — panel placement, walkways, HVAC clearances, mounting | Structural + solar design firm | C2 |
| YIELD | Bankable energy yield study — irradiance model, shading analysis, P50/P90 | Solar design firm | C2 |
| ITC-DC | Domestic content determination — First Solar domestic content percentage vs IRS requirements | Tax counsel + First Solar | C2 |
| MPPT | Multi-MPPT configuration — confirm number of independent MPPT zones per roof | Solar design firm + DC-DC vendor | C2 |
| E-23 | Inter-block solar distribution — if solar DC output extends to non-adjacent blocks | SLD-001 routing | C3 |

---

## 13. Revision plan

| Rev | Trigger | Change |
|---|---|---|
| **0.1 (current)** | First issue | Array spec, string analysis, DC-DC spec, bus topology, AMCL integration, ITC basis, vendor contacts |
| 0.2 | DC-DC buck converter RFQ responses | Update §6 with selected vendor, confirmed efficiency, MPPT specification |
| 0.3 | Structural assessment B1/B2 complete | Update §4 rooftop layout, confirmed panel count per building, structural loading |
| 0.4 | Bankable yield study complete | Update §9 production estimates with P50/P90 yield model |
| 1.0 | All C1 items closed | Ready for external distribution. Paired with SLD-001 Rev 1.0. |

---

## 14. Approval

Rev 0.1 does not carry external circulation approval. Architecture inherits from BOD-001 Rev 0.4 and ELEC-001 Rev 1.2 approval status. External distribution waits for Rev 1.0, gated on all C1 items per §12.

---

**End of ST-TRAP-SOLAR-001 Rev 0.1.**
