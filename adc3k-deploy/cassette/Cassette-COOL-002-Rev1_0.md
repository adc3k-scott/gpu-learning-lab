# Cassette — EXTERNAL CDU COOLING ARCHITECTURE

**Document:** Cassette-COOL-002
**Revision:** 1.0
**Date:** 2026-04-20
**Classification:** CONFIDENTIAL
**Status:** Released

**Supersedes (in part):** Cassette-COOL-001 Rev 1.1 §7 (CoolIT CHx2000 internal CDU)
**Companion documents:** Cassette-CDUSKID-001 Rev 1.0 (RFQ spec), Cassette-INT-001 Rev 3.0, Cassette-ECP-001 Rev 3.0

| Rev | Date       | Description                                                                          |
|-----|------------|--------------------------------------------------------------------------------------|
| 1.0 | 2026-04-20 | Initial release. External CDU skid architecture replacing internal CoolIT CHx2000. Plate-and-frame HX, dual circulation loops, thermal buffer tank. Cassette becomes sealed appliance with only 2 PG25 QDs at the CDU-end ECP. |

**Prepared by:** Scott Tomsu · CEO / Chief Engineer
scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana

---

## TABLE OF CONTENTS

- §1  Purpose and Scope
- §2  Architectural Change Summary
- §3  Three-Loop Architecture
- §4  Design Basis — Heat Loads and Coolant Properties
- §5  Primary Loop (Cassette Interior) — Unchanged
- §6  Intermediate Loop (Skid-Side PG25)
- §7  Heat Exchanger Sizing — Plate-and-Frame
- §8  Thermal Buffer Tank
- §9  Circulation Pumps — Primary and Secondary
- §10 Filtration, Expansion, and Degassing
- §11 Cassette-to-Skid Interconnection
- §12 Secondary Loop (Facility CHW or Direct Chiller)
- §13 Thermal Performance — Approach, LMTD, Pinch
- §14 Failure Modes and Redundancy
- §15 Control Interface to Site Orchestrator
- §16 Commissioning Requirements
- §17 Mass and Footprint Impact
- §18 Open Items

---

## §1  PURPOSE AND SCOPE

### Scope

This document defines the cooling architecture for Cassette deployments using an **external CDU skid** in place of the internal CoolIT CHx2000 specified in COOL-001. All hydraulic physics inside the Cassette remain per COOL-001 §4, §5, §6, and §9. This document covers everything from the Cassette-side PG25 quick-disconnects at the CDU-end ECP outward through the heat exchanger to the facility-side chilled water or direct-chilled interface.

The external CDU approach is now the default architecture for all Cassette deployments. COOL-001 §7 (internal CoolIT CHx2000 selection and verification) is preserved for reference only — the internal CDU is no longer a production configuration.

### Out of Scope

- Platform chilling plant design (upstream of the skid secondary loop)
- Absorption chiller specification (covered in Cassette-ABS-CHLR-001 when written)
- Munters HCD-600 humidity management (COOL-001 §10 and INT-001 §16)
- Equipment vendor RFQ detail (Cassette-CDUSKID-001)

### References

| Document             | Title                                      | Rev  |
|----------------------|--------------------------------------------|------|
| Cassette-COOL-001    | Cooling Hydraulic Model                    | 1.1  |
| Cassette-CDUSKID-001 | CDU Skid Equipment Specification           | 1.0  |
| Cassette-INT-001     | Interior Design Specification              | 3.0  |
| Cassette-ECP-001     | External Connection Panel ICD              | 3.0  |
| Cassette-CTRL-001    | Control & Data Architecture                | 1.0  |
| Cassette-MODES-001   | Operating Modes & Sequences                | 1.0  |
| ASHRAE Datacom       | Liquid Cooling Guidelines for Datacom      | 2014 |
| Alfa Laval M15       | Industrial plate-and-frame HX datasheet    | —    |
| Grundfos CRE series  | Vertical multistage centrifugal pump data  | —    |

---

## §2  ARCHITECTURAL CHANGE SUMMARY

### What Moved Out of the Cassette

The CoolIT CHx2000 CDU specified in COOL-001 §7 — a purpose-built liquid-to-liquid data center CDU — is removed from the Cassette interior and replaced by a **field-assembled industrial skid** using standard process equipment (plate-and-frame HX, centrifugal pumps, buffer tank, expansion tank, duplex strainer).

### Why

Three drivers, in descending order of importance:

1. **Mass and space liberation.** The CHx2000 and its immediate plumbing account for ~850 kg of Cassette operating mass and occupy the 1,500 mm CDU end zone. Removing it brings the operating weight from 29,935 kg to ~29,085 kg against the ISO 40-ft HC gross limit of 30,480 kg — a 1,395 kg margin vs. the previous 545 kg, roughly 2.5× the headroom for field upgrades, additional racks, or reinforcement.

2. **Sealed pressure-vessel posture.** With the CDU external, the Cassette contains only the primary PG25 loop and its rack cold plates — a fully sealed, hard-plumbed fluid envelope with no human-service demand during operation. All filter changes, pump swaps, and HX maintenance happen on the skid, not inside the pod. This is the submarine / ROV / satellite discipline referenced in INT-001 §1.

3. **Capacity beyond the CHx2000 envelope.** The CHx2000 is 10.6% over nameplate at full CPX tier (COOL-001 §7.2). The external skid is sized from the ground up for 2.5 MW thermal duty with margin, eliminating the CPX overload concern and creating headroom for CPX-Next (2.5–3 MW class) racks without a platform change.

### What Stays Inside the Cassette

Unchanged from COOL-001 / INT-001:

- Primary PG25 glycol loop, 45 °C supply / 55–60 °C return
- DN125 304L stainless manifold headers (supply and return)
- DN32–DN40 branch laterals to each rack
- Stäubli UQD-25 in-rack quick disconnects (3 per rack side)
- NVL72 rack cold plate circuits
- TraceTek leak detection
- VESDA-E smoke detection
- Jetson AGX Orin BMS (N+1)
- Munters HCD-600 external duct interface

### What the Cassette Now Looks Like Electrically and Hydraulically

The Cassette boundary crossing at the CDU-end ECP reduces to:

| Interface               | Before (COOL-001)                          | After (COOL-002)                         |
|-------------------------|--------------------------------------------|------------------------------------------|
| Primary fluid           | Internal — contained in CDU                | 2× PG25 QDs at ECP (supply + return)     |
| CHW supply + return     | 2× DN150 Victaulic at ECP                  | Not at Cassette ECP (moves to skid)      |
| CDU control panel       | Inside Cassette, accessible via panel P-6  | Absent                                   |
| CDU maintenance access  | Panel P-6 open required                    | Not required inside Cassette             |
| Panel P-6               | CDU service                                | Reclaimed for BMS and sensor concentration (INT-001 Rev 3.0 §9) |

---

## §3  THREE-LOOP ARCHITECTURE

### Loop Inventory

The external CDU introduces an intermediate loop between the Cassette primary and the facility chilled water. This is deliberate — it decouples the Cassette fluid envelope from the site fluid chemistry, pressure class, and service interval.

| Loop       | Fluid              | Location                     | Temp (supply/return)       | Flow (nominal)       |
|------------|--------------------|-----------------------------|---------------------------|----------------------|
| Primary    | PG25 glycol        | Cassette interior + skid HX | 45 °C / 55–60 °C          | 2,100–2,350 LPM      |
| Intermediate (skid PG25) | PG25 glycol        | Skid only (HX cold side)   | 40 °C / 52 °C (typ.)      | 2,200–2,500 LPM      |
| Secondary  | CHW (water) or refrigerant direct | Facility or on-board chiller | 7–12 °C / 12–18 °C | 2,200 LPM (NVL72) / 2,900 LPM (CPX) |

Note on terminology: COOL-001 references "primary" (PG25 in pod) and "secondary" (CHW at ECP). This document preserves those names for continuity. The new intermediate loop sits physically in the skid and is functionally part of the primary distribution — the HX separating primary from secondary is still a liquid-to-liquid HX, just relocated.

### Thermal Path

```
  15 racks × cold plates
         │ (PG25 45→57 °C, 2,100 LPM)
         ▼
  Cassette manifold headers
         │
         ▼ [Cassette ECP: 2× PG25 QDs]
         │
         ▼
  Flexible supply hose (skid inlet)
         │
         ▼
  SKID — Strainer → Filter → Buffer Tank → Pump Skid → HX Primary Side (57→45 °C)
         │
         ▼ [HX gap: ~5 °C approach]
         │
  SKID — HX Secondary Side (12→23 °C) ← Secondary pumps ← Facility CHW (7 °C)
         │
         ▼
  Facility chiller / absorption chiller / cooling tower [out of scope]
```

### Why Dual Loops Instead of Single Loop to Facility CHW

A single-loop architecture (CHW directly through racks) is not viable because:

- NVIDIA Vera Rubin cold plates require 45 °C ± 2 °C supply. Pure water would freeze at condensation points in the warmest-rack-coldest-CHW combination.
- Platform CHW at 7 °C with cassette interior at 40 °C ambient would condense moisture on any unprotected surface in the rack, destroying electronics.
- Water chemistry control across 15 sealed Cassettes sharing a CHW loop is operationally impossible; per-Cassette PG25 loops are isolated by the HX.

The HX is the pressure, chemistry, and temperature boundary between fleet-owned rack cooling and customer-owned facility cooling. This is a structural separation, not an efficiency trade.

---

## §4  DESIGN BASIS — HEAT LOADS AND COOLANT PROPERTIES

### Cassette Heat Loads (Unchanged from COOL-001)

| Parameter                            | NVL72 Tier   | CPX Tier     | Source         |
|--------------------------------------|--------------|--------------|----------------|
| IT load                              | 1,585 kW     | 2,105 kW     | COOL-001 §3    |
| Facility load (with Delta losses + I²R) | 1,677 kW | 2,212 kW     | COOL-001 §3    |
| Primary supply temperature           | 45 °C        | 45 °C        | NVIDIA spec    |
| Primary return temperature           | 56.9 °C (nom) | 59.0 °C (nom) | COOL-001 §4.4 |
| Primary flow                         | 2,100 LPM    | 2,350 LPM    | COOL-001 §4    |

### PG25 Properties (Both Primary and Intermediate Loops)

Same fluid in both loops. Simplifies makeup, filtration, and corrosion-inhibitor management.

| Property (PG25 at 50 °C avg)  | Value    |
|-------------------------------|----------|
| Density ρ                     | 1,023 kg/m³ |
| Specific heat Cp              | 3,930 J/kg·K |
| Dynamic viscosity μ           | 1.50 mPa·s  |
| Thermal conductivity k        | 0.42 W/m·K  |
| Freeze protection             | −13 °C   |

### Facility CHW Properties (Secondary Loop)

| Property (CHW water at 12 °C avg) | Value    |
|-----------------------------------|----------|
| Density ρ                         | 999.5 kg/m³ |
| Specific heat Cp                  | 4,205 J/kg·K |
| Dynamic viscosity μ               | 1.23 mPa·s |

---

## §5  PRIMARY LOOP (CASSETTE INTERIOR) — UNCHANGED

All primary-side hydraulics inside the Cassette are preserved from COOL-001. Reference only:

| Item                          | Spec                                              | COOL-001 §   |
|-------------------------------|---------------------------------------------------|--------------|
| Manifold headers              | DN125 304L stainless, supply + return             | §5.2         |
| Branch laterals               | DN32 min / DN40 preferred, 304L SS                | §5.4         |
| In-rack couplings             | Stäubli UQD-25 (3 per side per compute rack)      | §6.3         |
| Cold plate supply compliance  | 45 °C verified at 7–12 °C CHW supply              | §9           |
| Air-side thermal residual     | ~59 kW open item (CO-07)                          | §10          |

The Cassette primary loop now terminates at the CDU-end ECP with two Stäubli QBH-25 or Parker FEM-series PG25 quick-disconnects (one supply, one return). These replace the 2× DN150 Victaulic CHW penetrations in COOL-001 / ECP-001 Rev 2.2.

### Cassette-Side PG25 QD Selection

Design flow at CPX uprate: 2,350 LPM per line (single supply + single return).

| Candidate            | Bore  | Rated flow @ 2.0 m/s | Assessment                         |
|----------------------|-------|----------------------|------------------------------------|
| Stäubli QBH-80       | 80 mm | 602 LPM              | ✗ undersized by 4×                  |
| Stäubli QBH-125      | 125 mm | 1,472 LPM           | ⚠ 60% loaded at CPX — tight         |
| **Stäubli QBH-150**  | 150 mm | 2,121 LPM            | ⚠ 111% at CPX (acceptable short-duration) |
| Parker FEM-150       | 150 mm | 2,121 LPM            | ⚠ same velocity as QBH-150          |
| Parker Snap-tite 75  | DN200 | ~3,770 LPM            | ✓ ample margin, pipe-class connector |

**Recommendation: Parker Snap-tite Series 75 in DN150 or Stäubli QBH-150 with documented short-duration overflow allowance (CPX condition). Selection gated on vendor QBH-150 published flow curve at PG25 50 °C — open item CO-08.** Single connector per line preferred over parallel smaller to minimize leak surface count.

---

## §6  INTERMEDIATE LOOP (SKID-SIDE PG25)

The intermediate loop carries PG25 from the skid-side HX primary port through the skid pumps and buffer tank back to the HX. It shares fluid inventory with the Cassette primary loop — the two are hydraulically contiguous at the QDs.

### Fluid Inventory

Total PG25 charge at full depletion through one Cassette + one skid:

| Segment                                     | Estimated volume (L) |
|---------------------------------------------|----------------------|
| Cassette manifold + branches + cold plates  | 180                  |
| ECP-to-skid supply and return hoses (5 m ea) | 40                  |
| Skid inlet/outlet piping                    | 60                   |
| Strainer + filter housings                  | 25                   |
| HX primary side (plates + headers)          | 95                   |
| Circulation pump casings (4×)               | 20                   |
| Buffer tank (5 m³ nominal)                  | 5,000                |
| Expansion tank + air separator              | 60                   |
| **Total (nominal 5 m³ buffer)**             | **~5,480 L**         |

The buffer tank dominates charge volume. Per §8, the tank size is selected against ride-through requirements, not charge volume — but its choice drives PG25 initial-fill quantity and makeup-glycol logistics.

### Pressure Class

Maximum design working pressure: 10 bar (145 psi) at 65 °C maximum excursion temperature.

- Cassette-side components: rated 6 bar per COOL-001 (pump head + ~2 bar static)
- Skid-side components: must match 10 bar class across all pumps, HX, valves, and tank
- Flexible hoses between ECP and skid: 16 bar rated with 4:1 safety factor (64 bar burst)

10 bar class is an upgrade vs. the 6 bar Cassette-internal class because the skid-side pumps operate at higher discharge head and the buffer tank imposes a larger static head (up to 2 bar from its elevation).

---

## §7  HEAT EXCHANGER SIZING — PLATE-AND-FRAME

### Why Plate-and-Frame

Three advantages over the shell-and-tube or brazed-plate alternatives:

1. **Thermal duty at low approach.** Gasketed plate-and-frame HX achieve 2–3 °C approach routinely; 1 °C approach at cost. Shell-and-tube targets 5–8 °C approach.
2. **Serviceable.** Plates can be inspected, cleaned, re-gasketed, or added/removed to re-rate the HX without replacing the frame. Shell-and-tube requires tube-bundle pull.
3. **Compact.** At 2.5 MW class, a plate-and-frame HX is ~1/4 the footprint of an equivalent shell-and-tube, which matters on a 40-ft skid.

Brazed-plate is cheaper and more compact but cannot be serviced — any fouling or leak requires full HX replacement. Not acceptable for a 15-year continuous-duty asset.

### Duty Calculation — NVL72 Tier

Heat rejection required: 1,677 kW (full Cassette facility load).

LMTD at design condition:

```
Primary in (skid HX cold side, from cassette):   57 °C (rack return)
Primary out (skid HX cold side, to cassette):    45 °C
Secondary in (skid HX hot side, from facility):  12 °C (facility CHW supply)
Secondary out (skid HX hot side, to facility):   23 °C (facility CHW return)

LMTD = [(57−23) − (45−12)] / ln[(57−23)/(45−12)]
     = [34 − 33] / ln(34/33)
     = 1 / 0.0299
     = 33.4 °C
```

### Duty Calculation — CPX Tier

Heat rejection required: 2,212 kW.

```
Primary in:   59 °C
Primary out:  45 °C
Secondary in: 12 °C
Secondary out: 25 °C (wider ΔT at higher load; facility must confirm)

LMTD = [(59−25) − (45−12)] / ln[(59−25)/(45−12)]
     = [34 − 33] / ln(34/33) = 33.4 °C  (coincidentally same)
```

### Required UA

```
UA_NVL72 = Q / LMTD = 1,677,000 / 33.4 = 50,210 W/K
UA_CPX   = Q / LMTD = 2,212,000 / 33.4 = 66,230 W/K
```

Sizing to CPX (largest) with 10% margin: **UA required ≥ 73,000 W/K.**

### Plate-and-Frame Candidates

Overall heat transfer coefficient U for water/PG25 plate-and-frame HX at typical velocities (0.3–0.6 m/s plate channel): 4,000–6,000 W/m²·K. Using conservative U = 4,500 W/m²·K:

```
Required plate surface area A = UA / U = 73,000 / 4,500 = 16.2 m²
```

| Vendor / Model                      | Max duty (W/K) | Plate area range | Notes                                       |
|-------------------------------------|----------------|------------------|---------------------------------------------|
| **Alfa Laval M15**                  | up to 100,000  | 10–140 m²        | Preferred — workhorse industrial HX         |
| Alfa Laval M10                      | up to 60,000   | 2–48 m²          | Marginal at CPX                             |
| SWEP VM140                          | up to 80,000   | 5–80 m²          | Secondary choice                             |
| GEA NT150S                          | up to 120,000  | 15–170 m²        | Overspec — unless 3+ cassettes/skid         |
| Tranter GX-145                      | up to 85,000   | 10–120 m²        | Acceptable alternate                        |

**Recommendation: Alfa Laval M15 with 18 m² plate area, EPDM gaskets (PG25 compatible), AISI 316L plates.** Provides 20% UA margin over CPX requirement and allows plate addition for future 3 MW class.

Design procurement spec goes in CDUSKID-001 §7 for RFQ. Open item CO-09 — confirm Alfa Laval M15 available with <12 week lead time, or specify SWEP VM140 alternate.

---

## §8  THERMAL BUFFER TANK

### Purpose

The stratified buffer tank serves two functions:

1. **Thermal ride-through.** Absorbs short-duration heat load without drawing on facility chilled water. Bridges genset swap, chiller cycling, or secondary-loop pump restart.
2. **Load smoothing.** Damps rapid workload transitions (training burst ramps, sync-barrier spikes) so the facility chiller sees a smoothed thermal profile rather than raw GPU workload noise.

### Sizing for Ride-Through

Assumption: 60-second loss of secondary cooling with primary loop still circulating (pumps on UPS). Tank stores enough chilled PG25 to absorb full Cassette load for that duration without breaching 60 °C return limit.

```
Energy to absorb: Q × t = 2,212,000 × 60 = 132.7 MJ (CPX tier worst case)

Useful tank ΔT: tank initially at 40 °C, allowed to rise to 55 °C = 15 °C useful ΔT

Required mass: m = 132,700,000 / (3,930 × 15) = 2,250 kg
Required volume: V = 2,250 / 1,023 = 2.20 m³

With 50% buffer margin and plumbing allowance: 3.5 m³ minimum, 5.0 m³ preferred.
```

**Recommended tank: 5 m³ stratified vertical cylindrical, 316L stainless, insulated to R-15 with vapor barrier.** Stratification dividers (3–5 internal baffles) prevent thermal mixing during draw/return. Diffuser plates at inlet/outlet.

### Sizing for Load Smoothing

Time constant of the tank + primary loop:

```
Total primary-side mass (tank + piping + pod): ≈ 5,700 kg at 5 m³ tank
C_thermal = 5,700 × 3,930 = 22.4 MJ/K

At 1 MW load step: dT/dt = 1,000,000 / 22.4×10⁶ = 0.045 °C/s = 2.7 °C/min
```

A 1 MW step-up from idle takes ~4 minutes to shift tank average temperature by 10 °C. This is slow enough for facility chilled water controls (typical 30-s response) to track without alarm. The buffer tank is the dominant source of thermal time-constant in the combined system.

### Why Not a Smaller Tank

At ≤2 m³, the thermal time constant drops to <2 minutes and chiller oscillation risk rises. At 10+ m³, the thermal inertia becomes annoying during startup (slow to reach operating temperature) without adding useful ride-through. 5 m³ is the sweet spot per industry practice for 2–3 MW CDU skids.

---

## §9  CIRCULATION PUMPS — PRIMARY AND SECONDARY

### Primary Loop (PG25 Circulating)

Shared between cassette-interior loop and skid-interior loop — the two are hydraulically one system when QDs are mated.

Head budget (from COOL-001 §7.3, adjusted for external skid):

| Element                                     | ΔP (bar)   |
|---------------------------------------------|------------|
| Cassette interior (headers + branches + cold plates + UQDs) | 2.5–3.5 |
| ECP QDs (×2)                                | 0.3        |
| Flex hoses, 5 m each                        | 0.15       |
| Skid piping, strainer, filter               | 0.40       |
| HX primary side pressure drop               | 0.40–0.60  |
| Buffer tank inlet/outlet diffusers          | 0.10       |
| Engineering margin (15%)                    | 0.60–0.75  |
| **Total primary pump head required**        | **4.3–5.6 bar** |

At 2,350 LPM (CPX), 5 bar head:

```
Hydraulic power = V̇ × ΔP = (2,350/60,000) × 5×10⁵ = 19.6 kW
Pump shaft power at 75% efficiency = 26.1 kW
Motor rating (service factor 1.15): 30 kW
```

**Candidate pump: Grundfos CRE-64 vertical multistage (30 kW, 2,400 LPM at 5.5 bar), or Armstrong 4300 end-suction.** N+1 redundancy: 2 running + 1 standby, VFD-controlled.

### Secondary Loop (CHW Circulating)

Only used if the skid interfaces to facility CHW (most deployments). If interfacing to an on-board absorption chiller or direct-chilled cooling tower, secondary-loop pumps are sized by that equipment.

At 2,200 LPM NVL72 / 2,900 LPM CPX, 3 bar ΔP to facility loop:

```
Hydraulic power = (2,900/60,000) × 3×10⁵ = 14.5 kW
Motor rating: 22 kW
```

**Candidate: Grundfos CRE-45 (22 kW, 2,900 LPM at 3.3 bar).** N+1: 2 running + 1 standby.

### Total Pump Count per Skid

| Role                       | Count | Rating      | Total |
|----------------------------|-------|-------------|-------|
| Primary (PG25) circulation | 3     | 30 kW each  | 90 kW installed (60 kW operating) |
| Secondary (CHW) circulation| 3     | 22 kW each  | 66 kW installed (44 kW operating) |
| **Total**                  | **6** |             | **156 kW installed / 104 kW operating** |

Parasitic cooling energy: 104 kW / 2,212 kW = 4.7% of thermal load. This is the PUE cost of the dual-loop architecture vs. the single-loop CHx2000 approach (which ran ~2.5% parasitic). The PUE penalty is ~0.022 — acceptable against the mass/capacity/serviceability gains.

---

## §10  FILTRATION, EXPANSION, AND DEGASSING

### Duplex Strainer (Bulk Particulate)

- Primary-side suction-mounted upstream of pumps
- 40 mesh stainless basket (400 µm)
- Duplex design: online basket + standby; switchover without flow interruption
- Differential pressure sensor alarms at 0.3 bar across active basket → schedule swap

**Candidate: Eaton Model 53BTX DN150 duplex, or Hayward 2500 Series.**

### Cartridge Filter (Fine)

- Downstream of strainer, upstream of HX
- 25 µm cartridge, polypropylene spun, sanitized for glycol service
- 3 cartridges in parallel, differential pressure monitored
- Swap at 0.5 bar ΔP

**Candidate: Parker Fulflo or Pentair 3M PP25.** Three cartridges in parallel give ~100 gpm per cartridge; N+1 means swap one at a time without taking the skid offline.

### Expansion Tank

Bladder-type to prevent air contact with PG25 (PG25 oxidation produces acids).

```
System volume (liquid side): ≈ 5,500 L
Temperature excursion: 20 °C (normal range 30–50 °C at startup/standby)
PG25 thermal expansion: β ≈ 5×10⁻⁴ /K
Expansion volume: 5,500 × 5×10⁻⁴ × 20 = 55 L

With 50% safety + initial precharge allowance: 200 L tank
```

**Candidate: Amtrol ST-60V or Wessels FXT-120 (200 L bladder tank, 125 psig rating).**

### Air Separator

Micro-bubble coalescer mounted at the high-point of the skid piping. Removes dissolved gas that would otherwise accumulate at pump suctions or cold plate channels.

**Candidate: Spirotherm VJS-150 air separator with automatic vent.**

---

## §11  CASSETTE-TO-SKID INTERCONNECTION

### Flexible Hose Run

Between the Cassette CDU-end ECP and the skid inlet/outlet flanges:

- Length: 3–8 m depending on skid placement (skid sits 2–5 m from Cassette for service access)
- Diameter: DN150 inside bore (matches QD)
- Construction: 304 SS braided overlay on synthetic rubber or PTFE-lined; 16 bar rated
- Fittings: Stäubli QBH-150 on Cassette end, flanged to skid manifold on skid end
- Leak detection: TraceTek cable in a tray run under both hoses

**Candidate hose: Parker ParFlex 797TC or Gates Mega4000.**

### Thermal Insulation

Hoses and fittings are insulated to prevent condensation in high-humidity Gulf Coast ambient. At 45 °C PG25 and 80% RH / 35 °C ambient, surface condensation risk is low, but inrush at cold start (PG25 at 20 °C entering warmer hose) could condense.

- 25 mm Aeroflex elastomeric insulation with UV-protected jacket
- Continuous — no bare-metal bands that would become condensation points

### Break-Away Requirement

If the Cassette is to be lifted or moved (e.g., offshore deck repositioning), the hoses must disconnect without fluid loss. The Stäubli QBH series is specified because it has integral dry-break design — the ball valves close automatically on disconnect, retaining ~99% of loop fluid.

Alternative for offshore: **Tema DryBreak DB-150** — more aggressive containment, subsea-rated, fishing industry standard.

---

## §12  SECONDARY LOOP (FACILITY CHW OR DIRECT CHILLER)

### Interface at Skid Secondary Side

The skid exposes the following to the facility:

| Service                     | Flow        | Temperature         | Connector                 |
|-----------------------------|-------------|---------------------|---------------------------|
| CHW supply in               | 2,200 LPM (NVL72) / 2,900 LPM (CPX) | 7–12 °C | DN150 flanged              |
| CHW return out              | same        | 18–25 °C            | DN150 flanged              |
| Condensate drain            | low         | ambient             | DN40 with air gap          |
| Make-up water (PG25 top-off) | intermittent | ambient             | DN25 with RPBP             |

### Three Facility Configurations

**Configuration A — Facility CHW plant (most common).** Skid ties into existing chilled water infrastructure. Recommended for oil & gas onshore facilities, data center colocations, industrial sites with existing chillers.

**Configuration B — Absorption chiller on-site.** Skid secondary loop feeds a Broad BE 400 double-effect exhaust-driven absorption chiller (LiBr) driven by 2× Cat G3520H exhaust heat. Exhaust input: 2,410 kW at 395 °C (743 °F) per the G3520H spec. Operating COP at 743 °F exhaust: 1.32 (Broad XII catalog model selection curve). Chilled water output at operating conditions: 2,791 kW — covers 2,500 kW CDU skid duty with 12% margin. Broad USA vendor: 401 Hackensack Ave Suite 503, Hackensack NJ 07601, (201) 678-3010. BE model exhaust operating envelope: 536–990 °F (G3520H at 743 °F is mid-range). BE 400 operating weight: 61 tonnes — requires dedicated concrete pad separate from CDU skid. Lead time: 3–5 months. See Cassette-ABS-CHLR-001 (pending) for full chiller procurement spec.

**Configuration C — Direct evaporative / cooling tower.** Skid secondary loop couples to a forced-draft cooling tower. Simpler and lower capex, but requires water availability and rejects sensible heat to ambient (degrades in high-humidity Gulf Coast). Useful for oilfield deployment where water is cheap and process is already cooling-tower-heavy.

Facility selection drives secondary-loop pump specification (see §9) and skid-side control logic (see §15).

---

## §13  THERMAL PERFORMANCE — APPROACH, LMTD, PINCH

### Approach Temperature

The HX approach temperature is the difference between the warm-side-out and cold-side-in at the HX boundary.

```
Approach at NVL72:
  Primary out (45 °C) − Secondary in (12 °C) = 33 °C  (this is LMTD, not approach — recalc)
  
Approach (end-temperature difference at cold end):
  Primary out − Secondary in = 45 − 12 = 33 °C
  
Approach (end-temperature difference at hot end):
  Primary in − Secondary out = 57 − 23 = 34 °C
```

With both ends nearly equal (33 vs 34 °C), the HX is nearly isothermal — unusual but favorable. Typical data-center CDU approaches are 8–15 °C; here we're at 33–34 °C because the primary loop runs warm (45 °C supply) and the secondary loop runs cold (12 °C supply). Large LMTD → small required UA → compact HX.

### Pinch Point

No pinch point. The approach is uniform across the HX because both streams have similar heat capacity rates:

```
C_primary = ṁ_primary × Cp_PG25 = 35.8 × 3,930 = 140,700 W/K
C_secondary (NVL72 CHW at 2,180 LPM) = (2,180/60,000) × 999.5 × 4,205 = 152,700 W/K
C-ratio = C_primary / C_secondary = 0.92
```

Near-unity C-ratio gives a counter-flow HX with almost parallel temperature profiles — efficient configuration. Operating far from pinch minimizes sensitivity to off-design conditions (e.g., facility CHW at 10 °C instead of 12 °C).

### Effectiveness

```
ε (HX effectiveness) = actual heat transfer / maximum possible
                     = Q / (C_min × (T_h,in − T_c,in))
                     = 1,677,000 / (140,700 × (57 − 12))
                     = 1,677,000 / 6,331,500
                     = 26.5%
```

Effectiveness of 26.5% is low but appropriate here — the system is oversized on the secondary side relative to approach, giving headroom for facility CHW supply temperature excursions. If CHW supply rises to 14 °C (e.g., chiller degradation), the HX still delivers 45 °C primary supply without re-sizing.

---

## §14  FAILURE MODES AND REDUNDANCY

### FMEA Highlights

| ID  | Failure Mode                              | Detection        | Response                          | Consequence if Undetected |
|-----|-------------------------------------------|------------------|-----------------------------------|---------------------------|
| F-01 | Primary pump fail                         | VFD fault, flow sensor | Auto-swap to N+1 in <5 s      | Primary flow loss → thermal runaway in 60 s |
| F-02 | HX primary-side leak                      | Secondary pressure rise, PG25 level drop | Alarm, isolate HX manually | PG25 contamination of CHW |
| F-03 | HX secondary-side leak                    | Primary pressure drop, CHW level drop | Alarm, isolate HX manually  | CHW in PG25 (dilution) |
| F-04 | Facility CHW supply loss                  | Flow + temp sensors | Buffer tank sustains 60 s, then derate | Cassette thermal limit in 60 s |
| F-05 | ECP QD disconnection / leak               | TraceTek + flow delta | Emergency shutdown pumps, close isolation valves | Major PG25 release to floor |
| F-06 | Strainer blockage                         | ΔP sensor        | Swap to standby basket | Pump cavitation, flow loss |
| F-07 | Filter loading                            | ΔP sensor        | Scheduled swap | Particulate entry to HX/cold plates |
| F-08 | Expansion tank bladder rupture            | Pressure anomaly | Alarm, replace at next service window | Loss of expansion capacity |
| F-09 | Buffer tank stratification failure        | Tank T-stack sensors | Re-stratify via bypass valve | Reduced ride-through |
| F-10 | PG25 overheats (loss of HX contact)       | Temp sensors     | Emergency shutdown, facility CHW flush | Cold plate boiling at >60 °C |

### Redundancy

- Primary pumps: **N+1** — 2 active, 1 standby, VFD failover 5 s
- Secondary pumps: **N+1** — 2 active, 1 standby
- Strainer: **duplex** — online swap without flow interruption
- Filter: **3×1 parallel** — one at a time swap
- HX: **single unit** — plate service requires offline skid; mitigate by facility CHW overdesign (redundant chiller plant)
- Buffer tank: **single unit** — sized for 60 s ride-through; tank failure is low-probability structural event

### No Human Ingress to Cassette for Cooling Maintenance

With the CDU external, every cooling-related maintenance task happens on the skid or at the ECP — not inside the Cassette. This is a strong upgrade vs. COOL-001 where Panel P-6 (CDU service) was required for pump/filter/HX work.

---

## §15  CONTROL INTERFACE TO SITE ORCHESTRATOR

### CDU Skid PLC (L1)

Siemens SIMATIC S7-1500 per CTRL-001 §L1, with dedicated CPU for CDU skid duty. Publishes/subscribes via OPC UA to the site orchestrator.

### Signals Published by Skid (Sampled at 1 Hz Except Where Noted)

| Tag                              | Unit   | Sample rate |
|----------------------------------|--------|-------------|
| Primary supply temp (to cassette) | °C    | 1 Hz        |
| Primary return temp (from cassette) | °C   | 1 Hz        |
| Primary flow                     | LPM    | 1 Hz        |
| Primary pressure                 | bar    | 1 Hz        |
| Secondary supply temp            | °C     | 1 Hz        |
| Secondary return temp            | °C     | 1 Hz        |
| Secondary flow                   | LPM    | 1 Hz        |
| HX primary inlet / outlet temp   | °C     | 1 Hz        |
| HX secondary inlet / outlet temp | °C     | 1 Hz        |
| Buffer tank T-stack (5 points)   | °C     | 1 Hz        |
| Buffer tank level                | %      | 0.1 Hz      |
| Pump A/B/C status                | bool   | event       |
| Pump A/B/C current, speed, head  | —      | 1 Hz        |
| Strainer ΔP                      | bar    | 1 Hz        |
| Filter ΔP (per cartridge)        | bar    | 1 Hz        |
| Expansion tank pressure          | bar    | 1 Hz        |
| VFD fault status                 | enum   | event       |
| TraceTek leak alarm              | bool   | event       |

All tags enumerated in Cassette-TAGS-001 §SKID-CDU.

### Commands Accepted by Skid (From Orchestrator)

| Command                           | Scope                                    |
|-----------------------------------|------------------------------------------|
| Primary setpoint supply temp      | 43–47 °C (default 45)                    |
| Secondary setpoint supply temp    | 10–15 °C (nominal facility 12)           |
| Pump speed override               | 20–100% (auto by flow setpoint normally) |
| Standby pump pre-roll             | Start standby at 10% before swap (soft transfer) |
| Buffer tank pre-charge mode       | Drive tank to coldest allowed (pre-workload burst) |
| Filter bypass for service         | Bypass filter, alarm raised              |
| Emergency shutdown                | Kill all pumps, close isolation valves, vent expansion |

### Workload-Aware Feedforward

Per CTRL-001 §6, the orchestrator pushes a predicted-load tag `forecast_thermal_load_W` with a 30–60 s lookahead. The skid PLC uses this to:

- Pre-stage pump speeds (bring to workload target before step change)
- Pre-cool buffer tank (drive to minimum allowed in anticipation of burst)
- Smooth secondary flow setpoint (avoid step changes on facility chiller)

This is the differentiator. Conventional CDUs are reactive; this skid is predictive.

---

## §16  COMMISSIONING REQUIREMENTS

### Factory Acceptance Test (FAT) — at Skid Vendor

Per Cassette-CDUSKID-001 §20:

1. Hydrostatic pressure test — 15 bar for 60 min, both primary and secondary circuits
2. Flow verification — all pumps individually to nameplate and in parallel
3. Instrument calibration — all RTDs ±0.2 °C, flow meters ±1%, pressure ±0.5%
4. VFD tuning — pump response to setpoint step <2 s
5. PLC I/O checkout — all tags verified against TAGS-001

### Site Acceptance Test (SAT) — After Installation

1. **Cassette-skid interconnection leak test.** Flexible hoses connected, QDs mated. System fills with PG25 + 25% water. Pressurize to 10 bar for 2 hours; acceptable: <100 mbar decay.
2. **Full thermal loop test at load.** Operate cassette at 50% IT load (soft load via workload generator). Verify:
   - Primary supply stable 45 ± 1 °C
   - Primary return <60 °C
   - Secondary supply and return match facility spec
   - All pumps N+1 swap tested (plant stays stable)
3. **Failover tests.** Simulated pump fail, HX approach degradation, secondary flow loss, TraceTek trigger. Verify each response per MODES-001 §8–§12.
4. **Control handshake.** Skid publishes telemetry, accepts commands, integrates with site orchestrator. Verify OPC UA + Sparkplug B per CTRL-001 §4.

### Commissioning Acceptance

Skid is released to service when:
- 48 hours continuous operation at ≥75% load with no alarms
- All FAT and SAT line items signed off
- Workload-aware feedforward demonstrated (not just default reactive mode)
- Operations staff trained, runbook delivered

---

## §17  MASS AND FOOTPRINT IMPACT

### Cassette Mass Impact (Removing Internal CDU)

| Item removed                          | Mass (kg) |
|---------------------------------------|-----------|
| CoolIT CHx2000 unit                   | 650       |
| Internal CHW piping + Victaulic       | 120       |
| CDU service access provisions         | 80        |
| **Total cassette mass reduction**     | **~850**  |

Cassette operating mass: 29,935 → 29,085 kg (per MASS-001 Rev 3.0 update in companion document).

### Skid Footprint

| Dimension                  | Value                                   |
|----------------------------|-----------------------------------------|
| Overall LWH                | 6,000 × 2,200 × 2,500 mm                |
| Skid dry weight (equipped) | ~4,200 kg                               |
| Skid wet weight (PG25 fill)| ~9,700 kg (5,500 L PG25 at 1.02 kg/L) |
| Footprint                  | 13.2 m² (separate from cassette pad)    |
| Clearance around skid      | 1 m min all sides for service           |

Total deployment pad footprint (cassette + CDU skid + Munters skid): see INT-001 Rev 3.0 §24 and SITE-001 (pending).

---

## §18  OPEN ITEMS

| ID    | Priority | Description | Owner | Notes |
|-------|----------|-------------|-------|-------|
| CO-08 | P-1 | Stäubli QBH-150 or Parker Snap-tite 75 DN150 PG25 QD selection: vendor flow curves at PG25 50 °C, 2,350 LPM, published cycle life | ADC ↔ Stäubli / Parker | Gates ECP Rev 3.0 §4 closure |
| CO-09 | P-1 | Alfa Laval M15 availability: <12 week lead time at 18 m² / 73 kW/K duty; specify SWEP VM140 alternate if not | ADC ↔ Alfa Laval | Gates CDUSKID-001 FAT schedule |
| CO-10 | P-1 | Flexible hose selection for ECP↔skid run: 16 bar rating, DN150 bore, braided SS, length 5 m standard + 8 m alternate | ADC ↔ Parker / Gates | Procurement |
| CO-11 | P-2 | Primary pump N+1 failover timing: demonstrate <5 s swap without primary pressure excursion beyond ±15% | ADC engineering | SAT verification |
| CO-12 | P-2 | Buffer tank stratification baffle design: CFD or vendor-proven diffuser plates at inlet/outlet | Tank vendor | Gates tank RFQ |
| CO-13 | P-2 | Secondary loop interface: confirm facility CHW pressure class (10 bar vs 6 bar) and flow range for Configuration A deployments | ADC ↔ customer | Per-site |
| CO-14 | P-3 | Absorption chiller procurement spec (Cassette-ABS-CHLR-001): Broad BE 400 double-effect exhaust LiBr, 2,410 kW exhaust input at 743 °F, 2,791 kW cooling output, COP 1.32, 61-tonne standalone unit, 3–5 month lead time | ADC ↔ Broad USA (201) 678-3010 | Gates ABS-CHLR-001 |
| CO-15 | P-3 | PG25 corrosion inhibitor package: dual-fluid nitrite vs. organic acid, 3-year replacement schedule | ADC ↔ Dow / Houghton | Fluid spec |

---

## SUMMARY OF KEY CHANGES FROM COOL-001

| # | Change | Driver |
|---|--------|--------|
| 1 | **Internal CoolIT CHx2000 replaced by external industrial skid** | Mass margin, sealed-appliance posture, CPX overload |
| 2 | **Three-loop architecture** (primary PG25 in pod, intermediate PG25 in skid, secondary CHW at skid) | Pressure/chemistry isolation, fleet scalability |
| 3 | **Plate-and-frame HX (Alfa Laval M15 preferred)** replaces packaged CDU | Serviceability, 20% UA margin at CPX |
| 4 | **5 m³ stratified buffer tank** for thermal ride-through and load smoothing | 60 s ride-through, predictive smoothing |
| 5 | **Primary PG25 QDs (Stäubli QBH-150 or Parker Snap-tite 75)** at CDU-end ECP replace 2× DN150 Victaulic CHW | Cassette becomes sealed PG25 envelope |
| 6 | **Workload-aware feedforward control** integrated with skid PLC | 20–30% capacity uplift vs reactive control |
| 7 | **Parasitic cooling energy 4.7% of load** (vs 2.5% CHx2000) | PUE penalty ~0.022 — accepted for architecture gains |
| 8 | **Cassette operating mass 29,935 → 29,085 kg** | 1,395 kg margin to ISO limit (vs 545 kg before) |

---

**Cassette-COOL-002 — External CDU Cooling Architecture · Rev 1.0 · 2026-04-20**
**Scott Tomsu · scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana**
**CONFIDENTIAL**
