# ST-TRAP-SOLAR-001 — Solar Integration — Rev 0.2

**Document:** Solar Array Integration — Architecture and Specification Basis
**Project:** Trappey's AI Center, Lafayette, Louisiana
**Revision:** 0.2 — PV inverter rewrite; 480 VAC block bus interface replacing DC-DC buck to 800 VDC bus; companion to ELEC-001 Rev 1.3 and BOD-001 Rev 0.6
**Date:** April 23, 2026
**Owner:** Scott Tomsu
**Status:** Working draft
**Authority:** BOD-001 Rev 0.6 governs all locked values (E-14 through E-17). ELEC-001 Rev 1.3 §9 establishes the bus integration topology. This document provides the detailed specification basis and PV inverter RFQ anchor.

W = Working estimate · L = Locked per BOD-001 · O = Open

---

## Revision Log

| Rev | Date | Changes |
|---|---|---|
| 0.1 | 2026-04-18 | First issue — DC-DC buck converter (1,500 VDC → 800 VDC, MPPT) on block-level 800 VDC bus. |
| **0.2** | **2026-04-23** | **PV inverter rewrite per BOD-001 Rev 0.6 E-17. §6 DC-DC buck spec replaced with PV inverter spec (1,500 VDC → 480 VAC 3-phase 60 Hz, MPPT, grid-forming, island-mode). §7 bus interface rewritten for 480 VAC block switchboard — SSCB + blocking diode replaced with AC circuit breaker. §1 purpose updated. §2 upstream references updated. §5 key finding updated (string voltage vs PV inverter MPPT range). §12 open items and vendor shortlist updated.** |

---

## 1. Purpose

This document establishes the solar array integration basis for the Trappey's AI Center. It defines:

- Panel specification and array configuration
- String voltage and current analysis across Louisiana seasonal temperature range
- PV inverter specification (1,500 VDC → 480 VAC 3-phase 60 Hz, MPPT, grid-forming, island-mode)
- 480 VAC block bus interface topology
- AMCL MPPT and dispatch integration
- Energy production estimates and operating role
- ITC incentive basis and First Solar engagement path
- Open items and PV inverter vendor RFQ anchor (E-22)

---

## 2. Relationship to other documents

**Upstream (this document inherits from):**

- BOD-001 Rev 0.6 — E-14 through E-17 are the locked source entries
- ELEC-001 Rev 1.3 §9 — bus integration topology; PV inverter AC output on 480 VAC block bus
- TRAP-MASTER-ENG-001 Rev 0.4 — §5 solar PV inverter on 480 VAC block bus; anti-islanding DISABLED

**Downstream (inherits from this document):**

- ST-TRAP-SLD-001 — formal single-line; solar inverter AC breaker and conductor sizing
- ST-TRAP-PROT-001 — protection coordination at solar AC bus tie; LSIG trip settings
- PV inverter vendor RFQ (E-22, not yet issued)

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
| **Net 30-year advantage (Louisiana)** | **~+6% cumulative vs silicon** *(First Solar vendor data; +2% hot climate, +4% humid climate — approximately verified by independent field data)* |

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

The 5-panel string configuration delivers a string MPP voltage range of ~891V (summer) to ~1,013V (winter) across the Louisiana temperature envelope. This range sits comfortably within the 1,500 VDC maximum system voltage at Voc and within the MPPT input range of standard 1,500 VDC-rated PV inverters (~200–1,500 VDC). No string reconfiguration is required seasonally.

### 5.1 Voltage analysis

| Condition | Cell temp | String MPP voltage | String Voc | 1,500V limit |
|---|---|---|---|---|
| STC (reference) | 25°C | 5 × 190.4V = **952V** | 5 × 228.8V = **1,144V** | ✓ Within |
| Summer peak (Lafayette) | 45°C (cell) | 952V × (1 + (−0.32% × 20)) = **~891V** | < 952V | ✓ Within range |
| Winter cold | 5°C (cell) | 952V × (1 + (−0.32% × −20)) = **~1,013V** | 5 × 228.8V × (1 + (0.28%/°C × (25−5))) = **~1,208V** | ✓ Within |
| Extreme cold (record) | −5°C (cell) | 952V × (1 + (0.32% × 30)) = **~1,043V** | 5 × 228.8V × (1 + (0.28%/°C × 30)) = **~1,240V** | ✓ Within 1,500V |

**Temperature coefficients used:** MPP uses Pmax coef −0.32%/°C. Voc uses First Solar FS-7550A Voc coef −0.28%/°C (per datasheet; distinct from Pmax coef). MPP and Voc calculations must use their respective coefficients.

**Key finding:** String MPP voltage ranges ~891V (summer) to ~1,013V (winter). The PV inverter MPPT input range must cover this full span — a standard 1,500V-rated inverter MPPT window of ~200–1,500 VDC satisfies this requirement with margin. Voc peaks at ~1,240V under extreme cold — well within 1,500 VDC limit.

### 5.2 Current analysis

| Parameter | Value |
|---|---|
| String current at MPP (Imp) | 2.89 A per string |
| String current at Isc | 3.08 A per string |
| Total array current at MPP (746 strings) | 746 × 2.89A = **2,155 A** at ~952V |
| Total power at MPP (STC) | 2,155A × 952V = 2,052 kW ✓ |

---

## 6. PV inverter specification

The PV inverter is the interface between the 1,500 VDC solar string field and the 480 VAC block switchboard. It performs three functions simultaneously: DC-to-AC conversion (1,500 VDC strings → 480 VAC 3-phase 60 Hz), MPPT (maximizing array output), and grid-forming island-mode operation (voltage and frequency regulation on the 480 VAC block bus without a utility grid reference).

**This is open item E-22.** Vendor RFQ to be issued from this specification.

### 6.1 Electrical requirements

| Parameter | Requirement | Notes |
|---|---|---|
| Input voltage range (MPPT) | 200–1,500 VDC minimum | Must track MPP from ~891V (summer) to ~1,013V (winter) across Louisiana temperature range |
| Input voltage absolute maximum | 1,500 VDC | IEC 62109-2 / UL 1741 rated |
| Output voltage | 480 VAC 3-phase 60 Hz, ±1% steady-state regulation | Block bus interface |
| Total rated power | 2.05 MW AC | See §6.2 for preferred multi-unit configuration |
| Power factor | ≥0.99 at rated power | Inductive and capacitive reactive compensation preferred |
| Efficiency | ≥97% at rated power (SiC preferred) | CEC weighted efficiency acceptable for comparison |
| MPPT algorithm | Multi-MPPT — one independent MPPT per roof section minimum | Handles partial shading per section independently |
| Grid-forming / island-mode | Required — inverter must regulate 480 VAC bus voltage and 60 Hz frequency without grid reference | Behind-the-meter permanent island; no utility grid connection |
| Anti-islanding | DISABLED — not applicable | Island is the operating mode, not a fault condition. Inverter must not disconnect on island detection. |
| Protection | Input overvoltage, output overvoltage, overcurrent, arc-fault detection (AFCI), GFDI | Per UL 1741 / NEC Article 690 |
| Communications | Modbus TCP to L1 block PLC — power output, MPPT point, fault status, string current per combiner | |

### 6.2 Preferred multi-unit configuration

One large 2 MW inverter carries a single point of failure for the entire array. Distributed architecture is preferred:

| Option | Configuration | Units | Per-unit power | Advantage |
|---|---|---|---|---|
| **A (preferred)** | One unit per roof section | 4 | ~512 kW | Independent MPPT per section; partial shading isolated; N partial redundancy |
| B | Two units | 2 | ~1,025 kW | Simpler wiring; 50% production loss on one unit failure |
| C | One unit | 1 | 2,050 kW | Simplest; full production loss on failure |

**Option A preferred.** Four roof sections on B1 and B2, one inverter per section, each with independent MPPT. Partial shading from HVAC equipment, antennas, or adjacent structures on one section does not derate other sections. Each unit AC output connects to 480 VAC block switchboard via dedicated AC circuit breaker (LSIG trip).

### 6.3 Vendor shortlist (E-22, open)

| Vendor | Products | Notes |
|---|---|---|
| **SMA Solar Technology** | Sunny Highpower PEAK3, Tripower Core1 | Strong multi-MPPT history; confirm 480 VAC 3-phase output configuration and island-mode at this power level |
| **ABB (Fimer)** | PVS-100/120 series | Broad power range; confirm island-mode / grid-forming capability; confirm 480 VAC |
| **Power Electronics** | SC500CP, SC630CP | Industrial-grade PV inverter; island-mode track record in remote/off-grid applications |
| **Sungrow** | SG250HX, SG350HX | High-efficiency string inverters; confirm island-mode and AFCI at this voltage/power |
| **Delta Electronics** | M250HV, M500HV | Delta still relevant — confirm AC island-mode PV inverter product at 480 VAC; in-row rack relationship may support integration |

---

## 7. 480 VAC block bus interface

### 7.1 Connection topology

```
First Solar Series 7 strings (1,500 VDC)
  ↓ string combiner boxes + DC disconnects
  ↓ PV inverter (1,500 VDC → 480 VAC 3-phase 60 Hz, MPPT, island-mode)
  ↓ AC circuit breaker (standard draw-out LV breaker · LSIG trip)
  ↓ Block 480 VAC main switchboard
```

**AC circuit breaker at bus tie:** Standard draw-out LV power circuit breaker with LSIG trip unit. Interrupts PV inverter AC output from 480 VAC switchboard on AC fault. No SSCB. No blocking diode. Standard protection coordination with other feeder breakers on the switchboard (genset transformer, BESS PCS).

**Auxiliary power:** PV inverter controls and cooling require ~10 kW per unit from a dedicated 480 VAC feeder (BOD E-29 solar aux line item: ~10 kW per inverter unit).

### 7.2 Block allocation

The solar array is physically located on B1 and B2 rooftops. The 480 VAC block bus is a per-block architecture with 11 independent blocks. PV inverter AC output connects to the switchboard of the block(s) whose distribution runs nearest to B1/B2.

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
| L0 — field devices | String current sensors per combiner; PV inverter power output meter; MPPT operating point; fault/alarm status |
| L1 — block PLC | MPPT coordination setpoint to PV inverter; solar AC breaker control; anti-islanding DISABLED (inverter operates in island-mode); zero-export enforcement (no excess to utility — no utility connection) |
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
3. **Narrative and incentive:** First Solar Series 7 made 30 miles away in New Iberia, LA. First solar-to-480V-AI-factory AC-coupled reference architecture. Solar ITC on total CapEx (see §10).
4. **Resiliency margin:** Solar production during daylight hours reduces genset loading, extending engine TBO intervals.

**What solar does not do:** It does not reduce the genset count. It does not reduce the BESS sizing. It does not feed the grid. It does not create a net-zero claim.

---

## 10. ITC and First Solar incentives

| Item | Value | Notes |
|---|---|---|
| Federal Solar ITC (base) | 30% | IRC §48E — investment tax credit on solar CapEx |
| Domestic content adder | +10% possible → 40% total | First Solar: US-manufactured in Perrysburg, Ohio + New Iberia, LA. Strong domestic content claim. Confirm with tax counsel. |
| Estimated module cost | $575K–$720K | First Solar market rate $0.28–0.35/W; multi-year offtake typical |
| Estimated total solar CapEx | $2.5M–$3.5M | Modules + PV inverters + mounting hardware + wiring + structural reinforcement |
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

**Engagement framing:** Lead with the reference architecture story — First Solar made in Louisiana powering Louisiana's anchor AI factory. AC-coupled 480V integration into a permanent behind-the-meter island. Solar ITC + domestic content adder. Documented and publishable. First Solar has been looking for an AI factory reference customer — this is it.

**Pricing lever:** Multi-year offtake agreements are typical. If Full Build uses 2.05 MW × 2 (Stage 1 + Stage 2) = 4.1 MW, plus potential replication across MARLIE I and other ADC sites, total pipeline is 10+ MW. Frame at portfolio scale.

---

## 12. Open items ledger

| Ref | Item | Blocked on | Priority |
|---|---|---|---|
| E-22 | PV inverter vendor RFQ — 4-unit island-mode configuration; confirm grid-forming at 480 VAC | This document — issue RFQ from §6 | C1 |
| B-07 | Structural assessment B1 and B2 — rooftop loading for 143,700+ kg array | Structural engineer commission | C2 |
| LAYOUT | Rooftop layout design — panel placement, walkways, HVAC clearances, mounting | Structural + solar design firm | C2 |
| YIELD | Bankable energy yield study — irradiance model, shading analysis, P50/P90 | Solar design firm | C2 |
| ITC-DC | Domestic content determination — First Solar domestic content percentage vs IRS requirements | Tax counsel + First Solar | C2 |
| MPPT | Multi-MPPT configuration — confirm number of independent MPPT zones per roof | Solar design firm + inverter vendor | C2 |
| E-23 | Inter-block solar distribution — if solar AC output extends to non-adjacent blocks | SLD-001 routing | C3 |

---

## 13. Revision plan

| Rev | Trigger | Change |
|---|---|---|
| 0.1 | First issue (superseded) | Array spec, string analysis, DC-DC buck spec, 800 VDC bus topology — superseded by Rev 0.2 |
| **0.2 (current)** | **AC coupling rewrite** | **PV inverter spec replacing DC-DC buck; 480 VAC block bus interface; companion to BOD-001 Rev 0.6 and ELEC-001 Rev 1.3** |
| 0.3 | PV inverter vendor RFQ responses | Update §6 with selected vendor, confirmed efficiency, island-mode confirmation, MPPT specification |
| 0.4 | Structural assessment B1/B2 complete | Update §4 rooftop layout, confirmed panel count per building, structural loading |
| 0.5 | Bankable yield study complete | Update §9 production estimates with P50/P90 yield model |
| 1.0 | All C1 items closed | Ready for external distribution. Paired with SLD-001 Rev 1.0. |

---

## 14. Approval

Rev 0.2 does not carry external circulation approval. Architecture inherits from BOD-001 Rev 0.6 and ELEC-001 Rev 1.3 approval status. External distribution waits for Rev 1.0, gated on all C1 items per §12.

---

**End of ST-TRAP-SOLAR-001 Rev 0.2.**
