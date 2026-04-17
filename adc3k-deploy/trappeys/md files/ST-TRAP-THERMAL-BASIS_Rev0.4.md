# ST-TRAP-THERMAL-BASIS — Rev 0.4

**Document:** Thermal Architecture Basis of Design
**Project:** Trappey's AI Center, Lafayette, Louisiana
**Revision:** 0.4 — Option A single-stage chiller eliminated from design baseline; Boyd CDU T-11 action clarified as independent of Cat CSA; BOD-001 T-03 updated to B/C path
**Date:** April 17, 2026
**Prepared by:** Scott Tomsu
**Supersedes:** ST-TRAP-THERMAL-BASIS Rev 0.3
**Status:** Working draft — Option A eliminated; architecture proceeds on Options B or C pending chiller RFQ (TB-5)

---

## 1. Purpose

This document establishes the thermal architecture of the Trappey's AI Center cold sink. Rev 0.4 adds three updates to Rev 0.3:

- **Option A single-stage chiller eliminated from design baseline.** Heat balance at conservative supply scenario (1.05 ratio) yields only +1.4% drive margin — insufficient for 24/7 duty. Option A remains in the ledger for reference but is not the design path. Architecture proceeds on Options B (double-effect hot-water) or C (multi-energy/exhaust-driven) pending chiller RFQ (TB-5). BOD-001 T-03 updated accordingly.
- **Boyd CDU T-11 action is not blocked on Cat CSA.** Chiller delivery side is confirmed (BROAD rated 7°C, within 7–12°C Boyd-compatible range). Remaining action is a direct call to Boyd applications engineering to confirm CDU acceptance of CHW supply in that range. This can be closed independently of Cat CSA engagement.
- **Prior Rev 0.3 content retained:** CG260-16 continuous rating anchored to Cat Power Ratings Guide (4,000 ekW, 60 Hz / 900 rpm NG); three chiller options scoped with full heat balance arithmetic; Munters 5.5 MW slip-stream deduction in supply side; LDEQ/LPDES regulatory framework unchanged.

## 2. Scope

Covers the cold sink architecture and CHP cascade thermal framework serving Stage 1 (101.2 MW IT, 44 cassettes) and Full Build (202.4 MW IT, 88 cassettes).

Does not cover:

- Cassette-level cooling loop design — inside the cassette IP envelope
- Cooling tower field vendor specification — deferred to ST-TRAP-COOLING-TOWER-001
- Absorption chiller vendor selection — decision deferred per §5.7 and §6.5
- Vermilion River loop detailed engineering — deferred to ST-TRAP-RIVER-001
- LPDES application content — deferred to permitting workstream
- CG260-16 part-load exhaust temperature and mass-flow curves — pending Cat CSA engagement (remains P-0 despite published continuous rating now being in hand)

## 3. Controlling Regulatory Framework

Unchanged from Rev 0.2.

### 3.1 LAC 33:IX.1113.C.4.b.i — Freshwater temperature criteria

For streams and rivers in fresh water:

- Temperature differential: maximum 2.8°C (5°F) rise above ambient after mixing
- Absolute maximum: 32.2°C (90°F), except where otherwise tabulated

### 3.2 LAC 33:IX.1113.C.4.b — Process heat cutoff

Whenever ambient water temperature reaches the maximum, no additional process heat may be added except under natural conditions such as unusually hot or dry weather.

Operational implication: Whenever Vermilion River temperature at the site reaches 32.2°C (90°F), thermal discharge from the facility must stop. This is not a controllable variable.

### 3.3 LAC 33:IX.1113 — General criteria

Aesthetics, toxicity, solids, and other general water quality criteria apply at all times. Dilution and flow augmentation to achieve effluent concentration limits are prohibited.

### 3.4 LPDES permitting authority

New point-source thermal discharges to the Vermilion River require an LPDES permit covering both cooling tower blowdown and (if used) supplemental river-loop discharge. Pre-application engagement with LDEQ Water Permits Division is required before any design lock.

## 4. Controlling Site Hydrology

Unchanged from Rev 0.2.

### 4.1 Vermilion River is tidal at Lafayette

The Vermilion at the Trappey's site is not a free-flowing freshwater river. It is:

- Tidally influenced by Vermilion Bay; flow direction reverses during slack and rising tide
- Augmented by the Teche-Vermilion Freshwater Project (TVFWD); pump station capacity is 1,040 cfs but only a fraction (~10% via Bayou Fuselier plus additional downstream via Ruth Canal) reaches the Vermilion. Net Vermilion augmentation must be quantified (T-1c).
- Subject to extreme flow variability; historical record includes −11,300 cfs during August 2016 floods; TVFWD can shut down as in 2015

Thermal plume recirculation risk at intake during slack tides, rising tides, and TVFWD outages requires intake/discharge separation with reverse-flow margin.

### 4.2 Summer temperature ceiling

Louisiana summer surface water temperatures on the Vermilion routinely reach 85–92°F. When ambient is at or above 90°F, §3.2 prohibits any additional process heat input.

### 4.3 Political and permitting context

The Vermilion's 1970s reputation and 40+ years of TVFWD-led water-quality recovery mean a new industrial thermal discharge permit on this river will face heightened scrutiny regardless of engineering merit.

## 5. Architecture Decision — CHP Cascade

### 5.1 CHP cascade (locked per BOD-001 T-01)

```
Natural gas
   │
   ▼
44 × Cat CG260-16, 60 Hz, 900 rpm, 4,000 ekW continuous NG rating per genset (Cat published)
   │  Loading 61.5% nominal (AI-varied), ~2,460 kW electrical per genset
   │
   ├──── Electrical ─────────────────► cassettes, BESS, ancillary
   │
   ├──── Exhaust (high-grade) ──┐
   │                             │
   └──── Jacket water ───────────┤
                                  │
                  ┌───────────────┤
                  ▼               │
         Munters regen slip       │
         5.5 MW Stage 1           │
                                  ▼
                       Unified CHP hot water header
                       (and/or direct exhaust path, per §5.7)
                                  │
                                  ▼
                       Absorption chillers (architecture per §5.7)
                                  │
                     ┌────────────┴────────────┐
                     ▼                         ▼
                Chilled water              Condenser rejection
                 44°F rated                      │
                 (BROAD)                         ▼
                     │                  Cooling towers (primary)
                     ▼                         │
                Cassette Boyd CDUs             │ Supplemental:
                (≤45°C supply req.              │ Vermilion loop (§5.3)
                 per Rev 3.1)                   │ Water tower deferred (§5.6)
                     │                         │
                     ▼                         ▼
                Return CHW
```

### 5.2 Primary cold sink — Cooling towers (chiller condenser rejection)

Unchanged in architectural role; numerical tower load now depends on which chiller architecture is selected (§6.5).

Evaporative cooling towers carry the absorption chiller condenser load unconditionally. Tower field is sized to the highest-load chiller option (single-stage) so that any higher-COP option becomes pure margin.

Wet vs. hybrid vs. adiabatic decision stays in BOD-001 F.2 — driven by water consumption vs. capex tradeoff and LDEQ permitting posture.

### 5.3 Supplemental offset — Vermilion River

Unchanged.

Winter/shoulder favorable: 30–60 MW offset achievable. Louisiana summer ambient ≥ 90°F: 0 MW (LAC 33:IX.1113.C.4.b). TVFWD pump outage: 0 MW. Annual contribution 20–40% time-averaged, effectively 0% during peak weeks.

### 5.4 Munters regen slip-stream

Unchanged from Rev 0.2. Per cassette ~125 kW regen heat drawn from genset exhaust before absorption chiller drive. Stage 1 total 5.5 MW, Full Build 11.0 MW. Must appear in heat balance as deduction.

### 5.5 Chiller-cassette CHW compatibility — narrowed

**Delivery side (chiller):** BROAD XII catalog confirms rated CHW outlet/inlet 44°F/56.7°F; lowest permitted chilled water outlet 41°F; adjustable chilled water flow rate 50–120%. The BROAD chiller family can deliver chilled water within the 7–12°C (44.6–53.6°F) range Rev 3.1 identifies as Boyd-compatible. **Chiller delivery side is no longer a compatibility blocker.**

**Receiving side (Boyd CDU):** Rev 3.1 action E-8 asks specifically about Boyd CDU compatibility with chiller CHW supply. The range Rev 3.1 considers (7–12°C) is well inside BROAD's delivery envelope. What remains Open is direct confirmation from Boyd that their CDU accepts supply in this range at the required flow rates, approach temperatures, and control stability.

**Status:** Open but narrowed. BOD-001 T-11 remains Open. This is an informational call to Boyd, not a chiller-vendor call.

### 5.6 Deferred — Historic water tower

Unchanged. Zero load-bearing role. Structural assessment (T-5) not commissioned. Any future use contingent on assessment outcome.

### 5.7 Chiller architecture — three vendor-neutral options

BROAD's XII catalog confirms a vendor-class product exists for each path. This is architecturally significant: it means no architecture is blocked on "vendor doesn't make it." The choice is engineering and commercial.

**Option A — Single-stage hot-water-driven absorption chiller**
- Product class: BROAD BDH family (single-stage hot water), rated COP 0.76
- Drive source: hot water at ~208°F inlet / 190°F outlet (per BROAD rated conditions)
- Integration: unified CHP hot-water header from genset exhaust HRUs + jacket water plate HX
- Precedent: lowest-complexity path; matches Rev 3.1 baseline philosophy

**Option B — Double-effect hot-water-driven absorption chiller**
- Product class: BROAD BH family (double-effect hot-water), rated COP 1.50
- Drive source: hot water at ~356°F inlet / 329°F outlet (higher-grade than Option A)
- Integration: requires exhaust-derived high-grade hot water (jacket water alone cannot reach 356°F); HRU is the constraint
- Precedent: mainstream industrial absorption architecture

**Option C — Multi-energy (exhaust + hot water ± gas)**
- Product class: BROAD BZHE or BE family (exhaust-driven or multi-energy), rated COP 1.50 (exhaust-side) up to ~1.85 for condensing heat recovery configurations
- Drive source: direct exhaust at up to 932°F rated inlet (CG260-16 exhaust is well below this — derating curve needed from BROAD application engineering)
- Integration: direct exhaust to chiller HTG without HRU/hot-water intermediate stage; tighter thermal coupling to genset operating profile
- Precedent: Rev 3.1 Option 2 framework; BROAD's highest-performance architecture

All three options are retained. The chiller RFQ (new action item TB-5 in §8) selects among them based on written capacity/COP curves, capex, footprint, integration complexity, and vendor lead time.

## 6. Heat Balance Framework

### 6.1 Symbols

- Q_elec = genset electrical output
- Q_recov = recoverable thermal (exhaust above 120°C + jacket water)
- Q_munters = Munters regen slip-stream draw
- Q_drive = absorption chiller drive heat input
- Q_cool = chilled water cooling delivered to cassettes
- Q_tower = cooling tower condenser rejection
- COP = absorption chiller coefficient of performance

### 6.2 Conservation identity at chiller

```
Q_tower = Q_cool × (1 + 1/COP)
Q_drive = Q_cool / COP
```

### 6.3 Supply side — Stage 1

**Genset electrical (from Cat Power Ratings Guide):**

- CG260-16 continuous rating: 4,000 ekW per genset at 60 Hz / 900 rpm on NG
- Nominal loading: 61.5%
- Per-genset electrical at nominal: 2,460 kW
- 44 gensets at nominal: **108.24 MW electrical**

This is the confirmed electrical side. Site electrical load (Stage 1) per BOD-001: 106.3 MW from cassettes + ancillary (NOC, office, lighting, security, non-IT HVAC, BESS recharge, auxiliaries, controls). At 108.24 MW generated, ancillary headroom is approximately 2 MW at strict 61.5% loading. AI dispatch will vary loading in operation; the 61.5% figure is a design anchor, not a runtime constraint.

**Recoverable thermal estimate:**

Recoverable thermal ÷ electrical ratio at part-load for lean-burn gas gensets typically falls in 1.05–1.25 depending on engine family, part-load efficiency curve, and HRU effectiveness. The Rev 3.1 G3520K reference data shows ~1.155 at Mode A 64%. In the absence of CG260-16-specific part-load data from Cat CSA, a working range is used:

| Scenario | Ratio | Total recoverable (Stage 1) |
|---|---|---|
| Conservative | 1.05 | 113.6 MW |
| Central estimate | 1.15 | 124.5 MW |
| Optimistic | 1.25 | 135.3 MW |

**Less Munters regen deduction (§5.4): −5.5 MW**

| Scenario | Available for chiller drive |
|---|---|
| Conservative | 108.1 MW |
| Central | 119.0 MW |
| Optimistic | 129.8 MW |

**This range is the single biggest remaining thermal uncertainty.** Cat CSA engagement (T-08) resolves it. Until then, the conservative scenario (108.1 MW available for drive) should be used for sizing and margin decisions.

### 6.4 Demand side — Stage 1

Unchanged from Rev 0.2.

- 44 cassettes × 1,840 kW secondary loop demand = **81.0 MW chilled water demand** (locked per BOD-001 C-17)

### 6.5 Three-option heat balance

Each option is evaluated at all three supply scenarios. Tower load is computed from §6.2 conservation identity.

**Option A — Single-stage hot-water (BDH class, COP 0.76)**

| Supply scenario | Available drive | Drive required | Margin | Tower load |
|---|---|---|---|---|
| Conservative (1.05) | 108.1 MW | 106.6 MW | **+1.4%** (tight) | 187.6 MW |
| Central (1.15) | 119.0 MW | 106.6 MW | +11.6% | 187.6 MW |
| Optimistic (1.25) | 129.8 MW | 106.6 MW | +21.8% | 187.6 MW |

Drive required = 81.0 / 0.76 = 106.6 MW. Tower load = 81 × (1 + 1/0.76) = 187.6 MW.

**Assessment: Option A is eliminated from the design baseline.** +1.4% margin at conservative supply (1.05 ratio) is insufficient for 24/7 duty — any measurement error, fouling factor, or part-load deviation erases it. Option A would only be viable if Cat CSA confirms a heat recovery ratio solidly above 1.15; that confirmation is not in hand and cannot be assumed. Architecture proceeds on Options B or C. Option A remains in this ledger for reference only.

**Option B — Double-effect hot-water (BH class, COP 1.50)**

| Supply scenario | Available drive | Drive required | Margin | Tower load |
|---|---|---|---|---|
| Conservative (1.05) | 108.1 MW | 54.0 MW | +100% | 135.0 MW |
| Central (1.15) | 119.0 MW | 54.0 MW | +120% | 135.0 MW |
| Optimistic (1.25) | 129.8 MW | 54.0 MW | +140% | 135.0 MW |

Drive required = 81.0 / 1.50 = 54.0 MW. Tower load = 81 × (1 + 1/1.50) = 135.0 MW.

**Assessment:** Very large margin across all supply scenarios. Tower load drops by 52.6 MW vs. Option A. The integration constraint is getting hot water to ~356°F — this requires exhaust-driven HRU generating high-pressure hot water, not a simple jacket-water + exhaust merged header at ~200°F. HRU design becomes more intricate and Cat exhaust backpressure compatibility (from Rev 3.1 action E-3 on G3520K, analogous here) must be validated for CG260-16.

**Option C — Multi-energy or exhaust-driven (BZHE / BE class, effective COP 1.50, up to 1.85 condensing)**

| Supply scenario | Available drive | Drive required | Margin | Tower load |
|---|---|---|---|---|
| Conservative (1.05) | 108.1 MW | 54.0 MW | +100% | 135.0 MW |
| Central (1.15) | 119.0 MW | 54.0 MW | +120% | 135.0 MW |
| Optimistic (1.25) | 129.8 MW | 54.0 MW | +140% | 135.0 MW |

Using COP 1.50 (exhaust-side rated) as a conservative point. If condensing heat recovery configuration is selected (BROAD rated COP 1.85), drive required drops to 43.8 MW and tower load to 124.8 MW.

**Assessment:** Similar numerical outcome to Option B, but the integration path is different — direct exhaust to chiller HTG eliminates the HRU + hot water intermediate stage. Tighter thermal coupling to genset operating profile (load changes propagate faster into chiller state). Cat CG260-16 exhaust temperature is well below BROAD's 932°F rated inlet, so derating curves from BROAD are required — this is Rev 3.1 action E-2G carried to Trappey's.

### 6.6 Selection criteria (deferred to RFQ)

Option A is eliminated. Chiller RFQ (TB-5) decides between Option B and Option C. Criteria:

1. **Written COP/capacity curves at CG260-16 exhaust conditions** — no scaling from adjacent engine datasheets
2. **Written HRU and hot-water system requirements** (Option B) or direct-exhaust derating curves (Option C)
3. **Integration complexity** — number of intermediate stages, control coupling, failure modes under variable AI dispatch loading
4. **Capex** — chiller + HRU or direct-exhaust tie + interconnecting piping
5. **Footprint** — fit in 28,000 sq ft infrastructure yard
6. **Lead time** — 2026–2027 delivery window required
7. **Service and parts availability in US / Louisiana** — BROAD USA Inc. confirmed; service radius confirmation needed
8. **Margin on conservative supply scenario (1.05 ratio)** — both B and C pass comfortably (+100% minimum)

### 6.7 Full Build scaling

All Stage 1 numbers scale linearly (44 → 88 cassettes):

| Parameter | Stage 1 | Full Build |
|---|---|---|
| Chilled water demand | 81.0 MW | 162.0 MW |
| Munters deduction | 5.5 MW | 11.0 MW |
| Electrical at 61.5% | 108.2 MW | 216.5 MW |
| Recoverable (central) | 124.5 MW | 249.0 MW |
| Available drive (central) | 119.0 MW | 238.0 MW |
| Option A drive required | 106.6 MW | 213.2 MW |
| Option A tower load | 187.6 MW | 375.2 MW |
| Option B/C drive required | 54.0 MW | 108.0 MW |
| Option B/C tower load | 135.0 MW | 270.0 MW |

Same caveats apply at Full Build scale.

### 6.8 Tower sizing recommendation

Size the cooling tower field for **Option A at Stage 1 conservative supply: 187.6 MW**. Extend to **375.2 MW at Full Build** with staged buildout.

Rationale: sizing for the highest-load option means any decision to select Options B or C later produces pure margin rather than forcing tower rework. Marginal capex on the larger tower field is small relative to the cost of undersizing and rebuilding.

## 7. Downstream Consequences

### 7.1 Into ST-TRAP-SCALE-001 Rev 0.4

- Adopt CHP cascade as described in §5.1 with three chiller options retained vendor-neutral
- Tower field sized to 187.6 MW Stage 1 / 375.2 MW Full Build (Option A conservative supply)
- Remove all "river as primary cold sink" language
- Remove "zero evaporative loss" — replaced with honest seasonal envelope (see BOD-001 G.4)
- Cat CG260-16 at 4,000 ekW continuous per genset (Cat Power Ratings Guide, public reference)
- Site electrical total 108.24 MW at 61.5% nominal — ancillary headroom ~2 MW at Stage 1

### 7.2 Into ST-TRAP-STATE-001 Rev 1.2

- CHP cascade is a real, defensible technical story — describe as such
- Do not commit to chiller type externally before RFQ closes
- Soften river-cooling language per BOD-001 §C.6 directive
- Acknowledge water consumption honestly; frame tower hybridization as active trade space

### 7.3 Into LPDES pre-application (T-2)

- Intake/discharge separation with reverse-flow allowance
- TVFWD dependency acknowledgment
- Seasonal discharge schedule per §3.2 cutoff
- Thermal modeling at 7Q10 low flow and summer ambient ceiling
- Tower blowdown volume/quality — depends on tower type decision (hybrid vs. wet vs. adiabatic)

### 7.4 Into ST-TRAP-COOLING-TOWER-001

- Tower field carries 100% of chiller condenser rejection at design-day conditions
- Size to Option A conservative (187.6 MW Stage 1); lower load chiller selection → pure margin
- No river or solar credit in primary sizing
- Water consumption is a design output, not a design input
- Wet/hybrid/adiabatic decision per BOD-001 F.2

### 7.5 Into chiller RFQ (new, TB-5)

RFQ sent to BROAD, Thermax, Carrier/Sanyo, and other absorption-chiller vendors. Request:

- COP and capacity curves at actual CG260-16 exhaust temperature and mass flow (request Cat CSA data first so RFQ carries real operating conditions)
- Written response on Options A, B, C applicability for the vendor's product line
- HRU and hot-water system requirements for Options A and B
- Direct-exhaust derating curves for Option C
- Capex, footprint, lead time for each option
- Service radius from Louisiana
- OSHPD or equivalent seismic certification (not critical for Louisiana but a quality proxy)

### 7.6 Into Cat CSA engagement (E-6, BOD-001)

The Cat Power Ratings Guide gives continuous rating but not part-load heat split. Still required:

- Part-load exhaust temperature curve across 40–100% loading
- Part-load exhaust mass flow curve
- Jacket water heat rate vs. load
- Governor response in island-mode, 24/7 duty, at variable loading under AI dispatch
- Maximum exhaust backpressure (gates HRU design)
- Part-load BSFC curve (gates fuel consumption / emissions)

This datasheet request is the second gating question (after chiller RFQ, or in parallel). Rev 3.1 actions E-4A/E-4B/E-3 are the analog actions on G3520K; the same data in CG260-16 form is required.

## 8. Data Gaps and Open Items

Updated from Rev 0.2.

| ID | Item | Owner | Status | Cross-ref |
|---|---|---|---|---|
| T-1a | USGS Gauge 07386880 (Surrey St.) 7Q10 low-flow analysis | Scott | Partial | — |
| T-1b | Vermilion summer temperature envelope ≥ 90°F | Scott | Pending | — |
| T-1c | TVFWD net contribution to Vermilion at Lafayette | Scott | Pending | — |
| T-1d | Tidal reversal frequency/duration at site | Scott | Pending | — |
| T-08 | CG260-16 part-load exhaust temp, mass flow, jacket water heat rate | Cat CSA | Continuous rating confirmed (4,000 ekW); part-load curves still needed | BOD-001 T-08 |
| T-11 | Cassette-CHW compatibility (Boyd CDU side) | Scott → Boyd | Narrowed — chiller delivery side confirmed (BROAD rated 7°C delivery, within 7–12°C range). **Not blocked on Cat CSA.** Action: contact Boyd applications engineering to confirm CDU acceptance of 7–12°C CHW supply at required flow rates and approach temperatures. | BOD-001 T-11, §5.5 |
| T-12 | Munters regen slip-stream routing, HX type, control | Scott + Munters | Architecture locked; vendor engagement pending | BOD-001 T-12 |
| TB-1 | Cooling tower make-up water estimate | Scott + vendor | Pending — depends on tower type and chiller selection | — |
| TB-2 | Tower field footprint fit in 28,000 sq ft yard | Scott | Sized for Option A — adequate; reconfirm at vendor engagement | — |
| TB-3 | Blowdown treatment and disposal path | Scott | Open — affects LPDES | — |
| TB-4 | Absorption chiller architecture (A vs. B vs. C) | Scott | Three options retained; decision deferred to RFQ (TB-5) | BOD-001 T-03, §5.7, §6.5 |
| **TB-5** | **Chiller RFQ to BROAD, Thermax, Carrier/Sanyo, others** | **Scott** | **Not sent; blocked by Cat CSA data (T-08) for accurate RFQ conditions** | **New this revision** |
| T-5 | Structural assessment of historic water tower | Scott | Not commissioned | — |
| T-2 | LPDES pre-application meeting | Scott | Not scheduled | — |

## 9. Revision Log

| Rev | Date | Notes |
|---|---|---|
| 0.1 | 2026-04-16 AM | Initial. Cooling-tower-primary / river-supplemental / water-tower-deferred. Four LDEQ constraints. No CHP explicit, no Munters, no CHW compatibility. |
| 0.2 | 2026-04-16 PM | CHP cascade explicit. Heat balance arithmetic added. 196.7 MW Stage 1 tower re-derived from first principles at COP 0.70. Munters slip-stream 5.5 MW deduction. CHW compatibility flagged as C1. COP sensitivity table added. Cat CG260-16 heat rates as key unknown. |
| 0.3 | 2026-04-16 PM | Cat CG260-16 continuous rating anchored to Cat Power Ratings Guide (4,000 ekW at 60 Hz / 900 rpm NG). Recoverable thermal presented as 1.05/1.15/1.25 ratio sensitivity (113.6 / 124.5 / 135.3 MW Stage 1). Three chiller architecture options (A single-stage, B double-effect, C multi-energy) scoped vendor-neutral against BROAD XII product family data, with margin analysis for each at all three supply scenarios. Option A exposed as tight (+1.4%) under conservative supply — no longer safe to commit to as baseline. Options B/C carry +100–140% margin. Tower sized for Option A worst case (187.6 MW Stage 1, 375.2 MW Full Build) to preserve optionality. CHW compatibility narrowed — BROAD rated 7°C delivery covers Rev 3.1 range; Boyd side is the remaining open. New action item TB-5 for chiller RFQ. |
| 0.4 | 2026-04-17 | Option A single-stage chiller eliminated from design baseline — +1.4% margin at conservative supply insufficient for 24/7 duty. §6.5 assessment upgraded from "too tight" to eliminated. §6.6 criteria rewritten to B vs. C decision only. BOD-001 T-03 updated to reflect B/C path. T-11 Boyd CDU action clarified as not blocked on Cat CSA — independent call to Boyd applications engineering. |

## 10. Approval

This document requires Scott's sign-off before SCALE-001 Rev 0.4 or any chiller RFQ is issued. Downstream documents citing Rev 0.1 or Rev 0.2 must be updated.

---

**End of ST-TRAP-THERMAL-BASIS Rev 0.4.**
