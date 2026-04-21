# Cassette — COOLING HYDRAULIC MODEL

**Document:** Cassette-COOL-001
**Revision:** 1.2
**Date:** 2026-04-20
**Classification:** CONFIDENTIAL
**Status:** §7 SUPERSEDED by COOL-002 Rev 1.0 · §1–§6, §8–§11 remain current as primary-loop reference

**Companion documents:** Cassette-INT-001 Rev 3.0, Cassette-ECP-001 Rev 3.0, Cassette-BOM-001 Rev 3.0, Cassette-MASS-001 Rev 3.0, Cassette-COOL-002 Rev 1.0, Cassette-CDUSKID-001 Rev 1.0

| Rev | Date       | Description                                                                          |
|-----|------------|--------------------------------------------------------------------------------------|
| 1.0 | 2026-04-19 | Initial release. Primary loop hydraulics, CHx2000 verification, CHW secondary loop, UQD-16 analysis, four BOM/ECP corrections. |
| 1.1 | 2026-04-19 | §11 BOM / ECP corrections BOM-CO-01 through BOM-CO-04 adopted in BOM Rev 2.1 and ECP Rev 2.1. Analysis preserved as audit trail; resolution annotated inline. |
| **1.2** | **2026-04-20** | **§7 (CoolIT CHx2000 internal CDU verification) marked SUPERSEDED by Cassette-COOL-002 Rev 1.0 (external CDU skid architecture). §8 (CHW Secondary Loop at ECP) marked SUPERSEDED — CHW no longer at cassette ECP (see ECP-001 Rev 3.0 §7 for PG25 QD interface). Remaining content preserved as reference for primary loop hydraulics, which are unchanged inside the cassette per INT-001 Rev 3.0 §14. Companion doc references updated to Rev 3.0 baseline.** |

**Prepared by:** Scott Tomsu · CEO / Chief Engineer
scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana

---

## TABLE OF CONTENTS

- §1  Scope and References
- §2  Design Basis
- §3  Thermal Load Summary
- §4  Primary Loop — PG25 Glycol Circuit (CDU to Racks)
- §5  Primary Loop — Manifold Hydraulics
- §6  In-Rack Fluid Connection Analysis — Stäubli UQD-16
- §7  CDU Selection Verification — CoolIT CHx2000
- §8  CHW Secondary Loop at ECP
- §9  Cold Plate Supply Temperature Compliance
- §10 Air-Side Thermal Residual
- §11 BOM / ECP Corrections Identified
- §12 Open Items

---

## §1  SCOPE AND REFERENCES

### Scope

This document covers the complete hydraulic model for Cassette primary coolant distribution (CDU to cold plates) and the secondary chilled water interface (platform CHW to CDU). Scope is strictly within the Cassette boundary — from the ECP CDU fluid penetrations to the rack cold plate connections and back.

Out of scope: platform chilling plant sizing, cooling tower design, secondary water chemistry management, and offshore seawater or desalinated water loop design.

### References

| Document | Title | Rev |
|----------|-------|-----|
| Cassette-INT-001 | Interior Design Specification | 1.0 |
| Cassette-ECP-001 | External Connection Panel ICD | 1.0 |
| Cassette-BOM-001 | Bill of Materials | 1.0 |
| ASHRAE Datacom Series | Liquid Cooling Guidelines for Datacom Equipment | 2014 |
| NVIDIA NVL72 Vera Rubin | Cooling Interface Specification | TBD — pending vendor release |

---

## §2  DESIGN BASIS

### Key Design Parameters (from INT-001 and ECP-001)

| Parameter                     | NVL72 Tier   | CPX Tier     | Source        |
|-------------------------------|--------------|--------------|---------------|
| Cassette IT load                   | 1,585 kW     | 2,105 kW     | INT-001 §2    |
| Cassette facility load             | 1,677 kW     | 2,212 kW     | INT-001 §2    |
| Primary supply temperature    | 45 °C        | 45 °C        | INT-001 §8    |
| Primary return temperature    | 55–60 °C     | 55–60 °C     | INT-001 §8    |
| CHW supply temperature at ECP | 7–12 °C      | 7–12 °C      | ECP-001 §7    |
| CHW return temperature at ECP | ≤ 18 °C      | ≤ 18 °C      | ECP-001 §7    |
| Primary flow (INT-001 nominal)| 2,100 LPM    | see §4.2     | INT-001 §8    |
| Working fluid (primary)       | PG25 glycol  | PG25 glycol  | INT-001 §8    |
| CDU                           | CoolIT CHx2000, 2,000 kW rated | same | INT-001 §8 |

### Working Fluid Properties — PG25 at 50 °C Average

Propylene glycol 25% v/v (PG25) has materially different properties from pure water. All primary loop calculations use PG25 properties at the 50 °C average loop temperature.

| Property                       | PG25 at 50 °C | Pure water at 50 °C |
|--------------------------------|---------------|---------------------|
| Density ρ (kg/m³)              | 1,023         | 988                 |
| Specific heat Cp (J/kg·K)      | 3,930         | 4,182               |
| Dynamic viscosity μ (mPa·s)    | 1.50          | 0.547               |
| Thermal conductivity k (W/m·K) | 0.42          | 0.644               |
| Freeze protection              | −13 °C        | 0 °C                |

**Design implication:** PG25 has 6% lower Cp than water (more flow required for same heat transport) and 2.7× higher viscosity (higher pipe friction losses). Both must be carried into sizing.

---

## §3  THERMAL LOAD SUMMARY

All heat generated inside the sealed Cassette must be rejected to the platform CHW via the CDU. The pod is sealed; there is no external air path. Every watt of facility input becomes a watt of heat the CDU must reject.

### NVL72 Tier

| Subsystem                         | Count    | Load (kW) | Notes                          |
|-----------------------------------|----------|-----------|--------------------------------|
| Compute racks (Vera Rubin NVL72)  | 13       | 1,560     | 120 kW/rack                    |
| InfiniBand rack (Quantum-X800)    | 1        | 15        | switches + cabling             |
| Storage / management rack         | 1        | 10        | DPUs + NVMe + mgmt servers     |
| **Total IT load**                 |          | **1,585** |                                |
| Delta shelf conversion losses (~5%)| 13 racks | 82       | (1,560/0.95) × 0.05            |
| Busway / cable I²R                | —        | 10        | at 1,585 kW, 800 V DC          |
| **Total facility load**           |          | **1,677** | matches INT-001 §2             |

### CPX Tier

| Subsystem                             | Load (kW) | Notes                     |
|---------------------------------------|-----------|---------------------------|
| Compute racks (NVL144 CPX, 160 kW ea) | 2,080     | 13 racks × 160 kW         |
| IB + storage/mgmt                     | 25        | unchanged                 |
| **Total IT load**                     | **2,105** |                           |
| Delta shelf losses (~5%)              | 110       |                           |
| Busway / cable I²R                    | 17        | proportional              |
| **Total facility load**               | **2,212** | matches INT-001 §2        |

### Thermal Path

```
  Compute heat + Delta conversion losses
              │
              ▼
    Primary loop — PG25 glycol (45 °C supply / 55–60 °C return)
              │
              ▼
    CoolIT CHx2000 liquid-to-liquid heat exchanger
              │
              ▼
    CHW secondary — platform chilled water (7–12 °C in / ≤18 °C out)
              │
              ▼
    Platform cooling plant  [out of scope]
```

Air inside the sealed Cassette is not a heat sink. Any heat rejected to interior air by components without direct cold plate contact must be captured by an air-to-liquid heat exchanger connected to the primary loop. See §10.

---

## §4  PRIMARY LOOP — PG25 GLYCOL CIRCUIT (CDU TO RACKS)

### §4.1  NVL72 Flow Verification

INT-001 §8 establishes 2,100 LPM as the nominal primary loop design flow. Does this hold return within the 55–60 °C specification?

```
V̇  = 2,100 LPM = 0.03500 m³/s
ṁ  = V̇ × ρ = 0.03500 × 1,023 = 35.81 kg/s

ΔT = Q / (ṁ × Cp) = 1,677,000 / (35.81 × 3,930) = 1,677,000 / 140,733 = 11.92 °C

Return temperature = 45 + 11.92 = 56.9 °C    within 55–60 °C spec  ✓
Margin to 60 °C limit: 3.1 °C
```

**2,100 LPM is correctly sized for NVL72 tier. 5 °C margin to the absolute cold plate return limit.**

### §4.2  CPX Flow Requirement

Does 2,100 LPM hold return within spec at CPX facility load of 2,212 kW?

```
ΔT = 2,212,000 / (35.81 × 3,930) = 2,212,000 / 140,733 = 15.72 °C

Return temperature = 45 + 15.72 = 60.7 °C    exceeds 60 °C limit by 0.7 °C  ✗
```

**Key Finding: At 2,100 LPM, CPX tier return temperature breaches the NVIDIA 60 °C cold plate return spec.**

Minimum flow to hold return exactly at 60 °C (ΔT = 15 °C, zero margin):

```
ṁ_min = 2,212,000 / (3,930 × 15) = 37.52 kg/s
V̇_min = 37.52 / 1,023 = 36.68 L/s = 2,201 LPM  [no margin — not a design point]
```

Recommended CPX design point (ΔT = 14 °C, return = 59 °C, 1 °C margin):

```
ṁ = 2,212,000 / (3,930 × 14) = 40.20 kg/s
V̇ = 40.20 / 1,023 = 39.30 L/s = 2,358 LPM  →  use 2,350 LPM design flow
```

**For CPX upgrade, primary flow must be increased from 2,100 LPM to 2,350 LPM. CDU pump curve must confirm deliverability. Open item CO-01.**

### §4.3  Per-Rack Branch Flow Allocation

Primary flow is allocated proportionally to each rack's IT load fraction.

**NVL72 tier (2,100 LPM total):**

| Rack             | IT Load (kW) | Fraction | Flow (LPM) |
|------------------|--------------|----------|------------|
| R1–R13 (compute) | 120 each     | 0.0757   | **159**    |
| R14 InfiniBand   | 15           | 0.00947  | 20         |
| R15 Storage/mgmt | 10           | 0.00631  | 13         |
| **Total**        | **1,585**    |          | **2,100**  |

*Check: 13 × 159 + 20 + 13 = 2,067 + 33 = 2,100 LPM* ✓

**CPX tier (2,350 LPM total):**

| Rack             | IT Load (kW) | Fraction | Flow (LPM) |
|------------------|--------------|----------|------------|
| R1–R13 (CPX)     | 160 each     | 0.0760   | **179**    |
| R14 InfiniBand   | 15           | 0.00712  | 17         |
| R15 Storage/mgmt | 10           | 0.00475  | 11         |
| **Total**        | **2,105**    |          | **2,350**  |

*Check: 13 × 179 + 17 + 11 = 2,327 + 28 = 2,355 LPM* ≈ 2,350 LPM ✓ (rounding)

### §4.4  Return Temperature Summary

| Condition                   | Flow/rack | ΔT_rack  | Return     | Status |
|-----------------------------|-----------|----------|------------|--------|
| NVL72, 2,100 LPM total      | 159 LPM   | 11.9 °C  | 56.9 °C    | ✓      |
| CPX at NVL72 flow (2,100)   | 159 LPM   | 15.7 °C  | 60.7 °C    | ✗      |
| CPX at uprated flow (2,350) | 179 LPM   | 14.0 °C  | 59.0 °C    | ✓      |

---

## §5  PRIMARY LOOP — MANIFOLD HYDRAULICS

### §5.1  Architecture

Supply and return manifolds run along the manifold trench on Side B (INT-001 §11), full length of the rack zone (9,000 mm), from the CDU end to R1. Each rack taps off via a branch lateral.

```
CDU → [header] → tap R15 → tap R14 → ... → tap R2 → tap R1
      |←————————— 9,000 mm rack zone ————————————→|
```

### §5.2  Manifold Header Sizing

Target velocity: 1.5–3.0 m/s (PG25 design practice — higher viscosity penalizes friction at high velocity).

At full entry flow (2,100 LPM NVL72 / 2,350 LPM CPX):

| Header  | Bore   | Area (m²)   | v at 2,100 LPM | v at 2,350 LPM |
|---------|--------|-------------|----------------|----------------|
| DN 80   | 80 mm  | 5.03×10⁻³   | 6.97 m/s ✗     | 7.80 m/s ✗     |
| DN 100  | 100 mm | 7.854×10⁻³  | 4.46 m/s ⚠     | 4.99 m/s ✗     |
| DN 125  | 125 mm | 1.227×10⁻²  | 2.85 m/s ✓     | 3.19 m/s ⚠     |
| DN 150  | 150 mm | 1.767×10⁻²  | 1.98 m/s ✓     | 2.22 m/s ✓     |

**DN 100 manifold (BOM current spec) is too fast for CPX uprate and is marginal for NVL72. DN 125 is minimum for NVL72 and acceptable for CPX at 3.2 m/s entry (velocity drops rapidly as flow is distributed to racks). DN 150 covers both tiers with margin.**

**Recommendation: fabricate manifold headers as DN 125 304L stainless from first build. This avoids manifold replacement at CPX upgrade. BOM correction BOM-CO-02.**

Note: velocity in the manifold header decreases along its length as flow is tapped off. Entry velocity is the worst case; at the midpoint (after 7–8 racks tapped), velocity is approximately half the entry value.

### §5.3  Manifold Friction Loss — Darcy-Weisbach

PG25 at 50 °C in DN 125 304L stainless (ε = 0.05 mm):

```
Entry conditions (NVL72, 2,100 LPM):
  v = 2.85 m/s,  D = 0.125 m,  ρ = 1,023 kg/m³,  μ = 1.50×10⁻³ Pa·s

  Re = ρ v D / μ = 1,023 × 2.85 × 0.125 / 1.50×10⁻³ = 243,218  →  turbulent
  ε/D = 0.05/125 = 4.0×10⁻⁴
  Moody friction factor (Colebrook): f ≈ 0.018

  ΔP/m = f × (ρ v²/2) / D = 0.018 × (1,023 × 2.85²/2) / 0.125
        = 0.018 × 4,158 / 0.125 = 599 Pa/m = 0.006 bar/m

Over 9 m manifold, with average velocity ~1.4 m/s (entry tapering to ~0.3 m/s at R1 end):
  ΔP_manifold ≈ 0.006 × 9 × 0.50 [taper factor] ≈ 0.027 bar
```

**Manifold friction is negligible (~0.03 bar). System resistance is dominated by cold plate circuit and in-rack coupling losses. Detailed budget in §7.3.**

### §5.4  Branch Lateral Sizing

Per compute rack branch at 159 LPM (0.00265 m³/s):

| Lateral | Bore   | Area (m²)  | Velocity (m/s) | Assessment |
|---------|--------|------------|----------------|------------|
| DN 25   | 25 mm  | 4.91×10⁻⁴  | 5.40           | ✗ excessive with PG25 |
| DN 32   | 32 mm  | 8.04×10⁻⁴  | 3.30           | ✓ acceptable |
| DN 40   | 40 mm  | 1.257×10⁻³ | 2.11           | ✓ preferred |

**Branch laterals: minimum DN 32 stainless for compute rack connections. DN 40 preferred.** DN 25 branch laterals are undersized for PG25 at this flow rate.

---

## §6  IN-RACK FLUID CONNECTION ANALYSIS — STÄUBLI UQD-16

ECP-001 §17 specifies "Stäubli UQD-16" as the in-rack fluid quick-disconnect. This section evaluates whether DN 16 bore couplings are adequate for per-rack flows.

### §6.1  UQD-16 Hydraulic Capacity

| Parameter              | UQD-16 Value           |
|------------------------|------------------------|
| Nominal bore (DN)      | 16 mm                  |
| Flow area              | 2.011×10⁻⁴ m²          |
| Recommended max velocity (PG25) | 2.0–2.5 m/s  |

Maximum flow per single UQD-16 at 2.0 m/s:

```
V̇_max = A × v = 2.011×10⁻⁴ × 2.0 = 4.02×10⁻⁴ m³/s = 24.1 LPM per coupling
```

### §6.2  Couplings Required per Compute Rack

Design flow per compute rack: 159 LPM.

```
N = 159 / 24.1 = 6.6  →  minimum 7 UQD-16 couplings in parallel per side

7 supply + 7 return = 14 UQD-16 couplings per compute rack
```

Cassette-wide count:

| Rack group              | Flow (LPM) | Couplings/side | Total per rack | Qty | Subtotal |
|-------------------------|------------|----------------|----------------|-----|----------|
| R1–R13 compute          | 159        | 7              | 14             | 13  | 182      |
| R14 InfiniBand          | 20         | 1              | 2              | 1   | 2        |
| R15 Storage/mgmt        | 13         | 1              | 2              | 1   | 2        |
| **Total UQD-16**        |            |                |                |     | **186**  |

### §6.3  Finding and Recommendation

186 quick-disconnect couplings across 15 racks is technically workable but creates substantial part count, high potential leak surface (each coupling a failure point), and complex per-rack manifold header fabrication requiring 7-port manifolds.

**Alternative: upgrade to Stäubli UQD-25 or DN 25 equivalent:**

```
Area_DN25 = π/4 × 0.025² = 4.909×10⁻⁴ m²
V̇_max at 2.0 m/s = 4.909×10⁻⁴ × 2.0 × 60,000 = 58.9 LPM per coupling

Per compute rack:  159 / 58.9 = 2.7  →  3 couplings per side
                   3 supply + 3 return = 6 per rack
```

Cassette-wide at DN 25: 13 × 6 + 2 + 2 = 82 + 4 = **86 total** — 54% fewer couplings than UQD-16.

**Recommendation: upgrade in-rack fluid connection spec from UQD-16 to UQD-25 (or DN 25 ball-check equivalent). Must be confirmed against NVIDIA NVL72 rack cold plate inlet/outlet fitting specification before BOM update. Open item CO-03.**

---

## §7  CDU SELECTION VERIFICATION — COOLIT CHx2000

> **⚠ SUPERSEDED in Rev 1.2.** The internal CoolIT CHx2000 architecture analyzed in this section is no longer the production configuration. Refer to Cassette-COOL-002 Rev 1.0 for the external CDU skid architecture (Alfa Laval M15 plate-and-frame HX + Grundfos pumps + 5 m³ buffer tank on a dedicated skid). Content below is preserved as engineering audit trail for the original CHx2000 analysis and for the CPX overload finding that motivated the architectural change.


### §7.1  NVL72 Tier Capacity

```
Facility load:     1,677 kW
CHx2000 rated:     2,000 kW
Utilization:       1,677 / 2,000 = 83.9%
Margin:            323 kW  (+16.1%)
```

**CHx2000 is correctly sized for NVL72. 16% headroom. INT-001 §8 claim of "~85% utilization" confirmed.** ✓

### §7.2  CPX Tier Capacity

```
Facility load:     2,212 kW
CHx2000 rated:     2,000 kW
Utilization:       2,212 / 2,000 = 110.6%
Overload:          +212 kW  (+10.6%)
```

**Key Finding: CoolIT CHx2000 is 10.6% over nameplate at full CPX tier.** INT-001 §8 claims "CHx2000 sits comfortably with margin" for CPX — this is incorrect based on the nameplate comparison.

CPX upgrade resolution paths:

| Path | Action | Heat Handled | Status |
|------|--------|-------------|--------|
| A | CoolIT confirms 2,212 kW deliverable (short-term overload clause) | 2,212 kW | Requires CoolIT written confirmation — CO-04 |
| B | Add supplemental CDU (CHx300–CHx500) for delta 212 kW | 2,000 + 212 kW | Increases CDU zone footprint; impacts ECP |
| C | Derate CPX to 11 compute racks | 13 × 160 – 2 × 160 + 25 + losses = ~1,874 kW (93.7%) | Reduces compute count |
| D | Accept risk at annual peak; derate if CDU alarm threshold hit | 2,212 kW | Operationally managed |

**Path A is preferred if CoolIT can provide a written 10% overload allowance (common on CDU datasheets). CO-04 must be resolved before CPX upgrade commitment.**

### §7.3  Pump Head Budget

Without the CHx2000 published pump curve (CO-05), the pressure drop budget uses estimated values. This establishes the minimum pump head requirement and gates the open item.

| Loss Element                                     | ΔP (bar) | Basis                                    |
|--------------------------------------------------|----------|------------------------------------------|
| CDU internal HX + piping + flow controls         | 1.00     | typical 2 MW L2L CDU                     |
| Supply manifold (DN 125, 9 m, tapered flow)      | 0.03     | §5.3 D-W                                 |
| Return manifold (DN 125, 9 m, symmetric)         | 0.03     | symmetric                                |
| Branch lateral (DN 32, ~2 m each side)           | 0.15     | D-W at 159 LPM, PG25                     |
| In-rack manifold header and distribution valves  | 0.10     | estimated                                |
| Rack cold plate circuit (NVIDIA spec TBD)        | 0.80–1.50 | CO-02 — dominant uncertainty            |
| In-rack quick-disconnect couplings (3× DN 25)    | 0.25–0.40 | estimated at design flow                |
| **Total estimated system resistance**            | **2.36–3.21 bar** |                                 |
| Engineering margin (15%)                         | 0.35–0.48 |                                          |
| **Minimum pump head required**                   | **2.71–3.69 bar** |                                 |

**CHx2000 pump head must be confirmed ≥ 3.7 bar at 2,100 LPM (NVL72) and ≥ 3.7 bar at 2,350 LPM (CPX). Open item CO-05.**

Note: INT-001 §8 states "Secondary flow (CHW): 1,800 LPM nominal at 40 psi [2.76 bar] external ΔP." This refers to the pressure differential the platform CHW system must supply at the ECP connectors — a platform-side requirement, not CDU pump head.

---

## §8  CHW SECONDARY LOOP AT ECP

> **⚠ SUPERSEDED in Rev 1.2.** Chilled water no longer enters the Cassette. The CHW interface has moved entirely to the external CDU skid per Cassette-COOL-002 Rev 1.0. The cassette ECP now carries only primary PG25 coolant at the CDU-end ECP via Stäubli QBH-150 QDs per Cassette-ECP-001 Rev 3.0 §7. Content below is preserved as audit trail for the CHW sizing corrections adopted in ECP-001 Rev 2.0 (BOM-CO-03, BOM-CO-04) which informed the skid-side secondary loop sizing in CDUSKID-001.


### §8.1  Required CHW Flow Calculation

**What CHW flow is needed to reject 1,677 kW with supply at 7 °C and return ≤ 18 °C?**

```
Design condition: CHW supply 7 °C, max return 18 °C  →  ΔT_max = 11 °C
Fluid properties at 12 °C average: ρ = 999.5 kg/m³, Cp = 4,205 J/(kg·K)

ṁ = Q / (Cp × ΔT) = 1,677,000 / (4,205 × 11) = 36.27 kg/s
V̇ = 36.27 / 999.5 = 36.29 L/s = **2,177 LPM  ≈  2,180 LPM**
```

### §8.2  ECP-001 CHW Spec Inconsistency — Key Finding

ECP-001 §7 specifies:
- CHW flow design: **1,800 LPM**
- ΔT design: **5 °C**

Neither is consistent with the facility heat load:

```
At 1,800 LPM, CHW supply 7 °C:
  ṁ = (1,800/60/1,000) × 999.5 = 29.99 kg/s
  ΔT = 1,677,000 / (29.99 × 4,205) = 1,677,000 / 126,130 = 13.30 °C
  Return = 7 + 13.30 = 20.30 °C    exceeds 18 °C limit by 2.3 °C  ✗

At 1,800 LPM, CHW supply 12 °C (worst case supply temperature):
  Return = 12 + 13.30 = 25.30 °C    far exceeds limit  ✗
```

At 1,800 LPM with a 5 °C ΔT: Q = 29.99 × 4,205 × 5 = 630 kW — only 38% of the 1,677 kW facility load. The "5 °C" ΔT figure cannot represent the CHW temperature rise at any valid operating point; it appears to be a transcription of the CDU approach temperature parameter from INT-001 §8 applied incorrectly to the CHW fluid ΔT.

**Required CHW flow vs. ECP-001 spec:**

| Tier      | Required CHW Flow (7 °C supply, ≤18 °C return) | ECP-001 Spec | Deficit     |
|-----------|-----------------------------------------------|--------------|-------------|
| NVL72     | 2,180 LPM                                     | 1,800 LPM    | −380 LPM    |
| CPX       | 2,880 LPM                                     | 1,800 LPM    | −1,080 LPM  |

*CPX: ṁ = 2,212,000 / (4,205 × 11) = 47.83 kg/s = 2,870 LPM*

**ECP-001 §7 CHW flow spec must be corrected to 2,200 LPM (NVL72 design) with a note that CPX upgrade requires platform CHW capacity of 2,900 LPM. The "5 °C ΔT" entry must be corrected to "11 °C." BOM correction BOM-CO-03.**

### §8.3  ECP CDU Connector Velocity Check — DN100 Victaulic

ECP-001 §4 specifies 4" (DN100) Victaulic Style 77 for both CHW supply and return penetrations.

```
At corrected NVL72 CHW flow (2,180 LPM = 0.03633 m³/s):
  A_DN100 = π/4 × 0.10² = 7.854×10⁻³ m²
  v = 0.03633 / 7.854×10⁻³ = 4.62 m/s
```

**4.62 m/s exceeds the ASHRAE-recommended 3.0 m/s maximum for chilled water distribution piping. This drives elevated pipe erosion and acoustic noise.**

For ≤ 3.0 m/s at NVL72 corrected flow:

```
A_min = 0.03633 / 3.0 = 1.211×10⁻² m²
D_min = √(4 × 1.211×10⁻² / π) = 0.1242 m  →  DN 125 minimum
```

Options:

| Option | Description                              | Velocity at 2,180 LPM |
|--------|------------------------------------------|-----------------------|
| A      | 6" (DN 150) Victaulic Style 77 (single)  | 2.06 m/s ✓ preferred  |
| B      | 2× 4" (DN 100) Victaulic in parallel     | 2.31 m/s ✓            |
| C      | 5" (DN 125) Victaulic Style 77 (single)  | 2.98 m/s ✓ marginal   |

**Recommendation: upgrade ECP CDU fluid penetrations to 6" (DN 150) Victaulic Style 77. Single connector per line is simpler to couple, lower ΔP, and fully covers CPX CHW flow (2,880 LPM = 2.74 m/s in DN150). BOM correction BOM-CO-04.**

---

## §9  COLD PLATE SUPPLY TEMPERATURE COMPLIANCE

NVIDIA cold plate warm-water cooling specification: supply ≤ 45 °C.

The CDU controls primary supply at 45 °C setpoint. Supply temperature compliance depends on the CDU's ability to re-cool the return stream (55–60 °C) back to 45 °C using available CHW.

```
Worst-case thermal driving force (CHW supply at 12 °C maximum, NVL72 return at 57 °C):
  T_return − T_CHW_supply = 57 − 12 = 45 °C

This 45 °C driving force is more than sufficient for the CHx2000 heat exchanger
to achieve a 12 °C temperature drop on the primary side (57 → 45 °C).
```

**Cold plate supply temperature compliance: VERIFIED ✓ across the full CHW supply range of 7–12 °C and at both NVL72 and CPX IT load tiers.**

The 45 °C supply limit is not a risk driver for this architecture. The risk driver is the return temperature upper limit (60 °C), addressed in §4.2.

---

## §10  AIR-SIDE THERMAL RESIDUAL

### §10.1  Estimated Magnitude

Not all rack heat transfers directly to the PG25 primary loop through cold plates. Delta power shelves, rack control boards, SSD bays, and similar components reject heat to rack internal air, which then heats the Cassette interior.

| Source                                          | Estimated (kW) |
|-------------------------------------------------|----------------|
| Delta shelf losses (air-cooled portion, est. 50%) | 41           |
| Rack control boards, fan motors, misc           | 8              |
| 800 V DC busway / cable I²R to enclosure air    | 10             |
| **Estimated air-cooled residual**               | **~59 kW**     |

This estimate assumes the Delta shelf dissipates approximately half its conversion loss to air and half to PG25 via any integral heat spreaders. If Delta shelves are entirely air-cooled, the residual increases to ~100 kW.

### §10.2  Sealed Container Consequence

Without a closed air-side thermal path, this heat accumulates in the interior.

```
Container air volume (estimated): ~30 m³
Container steel mass: ~6,000 kg

Thermal mass:
  Air:   30 × 1.2 [ρ] × 1,005 [Cp] =   36,180 J/K
  Steel: 6,000 × 490 [Cp]           = 2,940,000 J/K
  Total:                             = 2,976,180 J/K

dT/dt = 59,000 W / 2,976,180 J/K = 0.020 °C/s

Time to reach 70 °C interior air (from 25 °C start) = 45 / 0.020 = 2,250 s ≈ 38 min
```

38 minutes to 70 °C interior air is incompatible with continuous operation. Elevated interior air temperature degrades Delta shelf inlet cooling effectiveness and accelerates non-cold-plate component aging.

### §10.3  Required Resolution

INT-001 §1 states "No Air Conditioning" but does not specify how steady-state air-cooled heat is rejected. Open item CO-07.

| Option | Description | Complexity |
|--------|-------------|------------|
| A | Confirm Delta shelves are fully liquid-cooled (no air-side heat) | Low — vendor confirmation only; eliminates ~41 kW |
| B | Install 2–3 compact air-to-liquid heat exchangers (AHLX), ceiling-mounted, connected to primary PG25 loop | Medium — ~59 kW requires ~0.5 m² HX area at 15 °C LMTD |
| C | Rear-door heat exchangers (RDHx) on each rack connected to primary loop | High — 15 additional HX units + 15 additional manifold drops |

**Resolve Option A first with Delta Electronics (CO-07). If Delta shelves have integral liquid cooling, the air-cooled residual drops to ~18 kW, which the steel thermal mass absorbs for typical non-continuous duty without an AHLX. If air-cooled, Option B is the minimum-complexity solution.**

---

## §11  BOM / ECP CORRECTIONS IDENTIFIED

**RESOLUTION (Rev 1.1):** All four corrections below have been adopted in BOM Rev 2.1 and ECP Rev 2.1. Table preserved as audit trail.

| ID         | Document     | Location        | Current Spec                  | Corrected Spec                      | Basis  | Status |
|------------|--------------|-----------------|-------------------------------|-------------------------------------|--------|--------|
| BOM-CO-01  | BOM-001      | §14 per-rack coupling | Stäubli UQD-16            | **Stäubli UQD-25 or DN25 equiv.**   | §6 — UQD-16 needs 7 parallel per rack; UQD-25 needs 3 | ✓ Adopted BOM Rev 2.0/2.1 |
| BOM-CO-02  | BOM-001 / INT-001 §14 | Manifold headers | DN100 stainless       | **DN125 stainless (both supply & return)** | §5 — DN100 is undersized at CPX uprate flow | ✓ Adopted BOM Rev 2.0/2.1 |
| BOM-CO-03  | ECP-001      | §7 CHW flow spec | 1,800 LPM / 5 °C ΔT          | **2,200 LPM / 11 °C ΔT (NVL72 design point)** | §8 — 1,800 LPM causes 20.3 °C return, 2.3 °C over limit | ✓ Adopted ECP Rev 2.0/2.1 |
| BOM-CO-04  | ECP-001 / BOM-001 | §4 CDU fluid penetration | 4" DN100 Victaulic Style 77 | **6" DN150 Victaulic Style 77** | §8 — 4.6 m/s velocity exceeds ASHRAE 3.0 m/s limit at corrected flow | ✓ Adopted BOM/ECP Rev 2.0/2.1 |

---

## §12  OPEN ITEMS

| ID    | Priority | Description | Owner | Notes |
|-------|----------|-------------|-------|-------|
| CO-01 | P-1 | CoolIT CHx2000 pump curve: confirm pump delivers 2,350 LPM at estimated 3.7 bar system resistance for CPX upgrade path | ADC ↔ CoolIT | Without this, CPX hydraulics are unverified |
| CO-02 | P-1 | NVIDIA NVL72 rack cold plate hydraulic specification: pressure drop vs. flow curve at 45 °C supply with PG25 glycol | ADC ↔ NVIDIA | Dominant uncertainty in pressure drop budget; gates pump head selection |
| CO-03 | P-1 | NVIDIA NVL72 rack manifold coupling specification: confirm DN25 or UQD-25 compatibility with Vera Rubin rack cold plate inlet/outlet fittings | ADC ↔ NVIDIA | UQD-16→UQD-25 upgrade in BOM-CO-01 must be confirmed against NVIDIA rack spec before BOM is updated |
| CO-04 | P-1 | CoolIT CHx2000 CPX overload: confirm max continuous heat rejection above 2,000 kW nameplate | ADC ↔ CoolIT | CHx2000 is 110.6% loaded at full CPX; need written confirmation or select alternative CDU path |
| CO-05 | P-2 | CoolIT CHx2000 pump specification: head vs. flow curve (N+1 configuration) | ADC ↔ CoolIT | Required to close pressure drop budget in §7.3 |
| CO-06 | P-2 | Update ECP-001 §4 CDU fluid connector from DN100 to DN150 Victaulic Style 77 and update BOM-CO-04 accordingly | ADC engineering | Straightforward spec change; no structural impact |
| CO-07 | P-2 | Air-side thermal residual: confirm Delta shelf cooling method (liquid vs. air); specify AHLX units if required | ADC ↔ Delta | ~59 kW air-cooled residual reaches 70 °C interior air in 38 min without thermal path to CDU loop |

---

## SUMMARY OF KEY FINDINGS

| # | Finding | Immediate Action |
|---|---------|-----------------|
| 1 | **2,100 LPM primary flow is correct for NVL72 but insufficient for CPX** — return reaches 60.7 °C vs. 60 °C limit | CPX requires 2,350 LPM; confirm with CDU pump curve (CO-01) |
| 2 | **CHx2000 is 10.6% over nameplate at full CPX tier** | CoolIT overload confirmation or CPX derate (CO-04) |
| 3 | **UQD-16 requires 7 parallel couplings per compute rack (186 total)** | Upgrade to UQD-25 (3 per rack, 86 total) — confirm NVIDIA compatibility (CO-03) |
| 4 | **ECP-001 CHW flow spec (1,800 LPM / 5 °C ΔT) is internally inconsistent and undersized** — 1,800 LPM returns CHW at 20.3 °C, 2.3 °C over the 18 °C limit | Correct ECP-001 §7 to 2,200 LPM / 11 °C ΔT (BOM-CO-03) |
| 5 | **ECP DN100 Victaulic connector is undersized at corrected CHW flow (4.6 m/s)** | Upgrade to DN150 Victaulic (BOM-CO-04) |
| 6 | **Cold plate supply temperature (45 °C) compliance is not at risk** — CDU has 45 °C thermal driving force at worst-case CHW supply | No action required |
| 7 | **~59 kW air-cooled residual heats sealed container to 70 °C in 38 min without a thermal path** | Confirm Delta shelf cooling method first; specify AHLX if air-cooled (CO-07) |

---

**Cassette-COOL-001 — Cooling Hydraulic Model · Rev 1.2 · 2026-04-20**
**Scott Tomsu · scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana**
**CONFIDENTIAL**
