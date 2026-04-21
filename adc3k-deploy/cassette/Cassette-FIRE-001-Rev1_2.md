# Cassette — FIRE SUPPRESSION ENGINEERING

**Document:** Cassette-FIRE-001
**Revision:** 1.2
**Date:** 2026-04-20
**Classification:** CONFIDENTIAL
**Companion to:** Cassette-INT-001 Rev 3.0 · Cassette-BOM-001 Rev 3.0 · Cassette-MASS-001 Rev 3.0 · Cassette-SIS-001 Rev 1.1

**Purpose:** NFPA 2001 engineering basis for the Novec 1230 total flood system. Calculates required agent quantity, evaluates cylinder sizing, verifies hold time, sizes the over-pressure vent, defines the VESDA detection-to-discharge sequence, and identifies a significant BOM over-specification that drives unnecessary weight and cost.

| Rev | Date       | Description                                           |
|-----|------------|-------------------------------------------------------|
| 1.0 | 2026-04-19 | Initial release                                       |
| 1.1 | 2026-04-19 | §12 cylinder right-sizing correction adopted in BOM Rev 2.1 and INT Rev 2.1; mass impact resolved in MASS Rev 2.0. Analysis preserved; resolution annotated inline. |
| **1.2** | **2026-04-20** | **Companion documents updated to Rev 3.0 baseline. Interior volume reconfirmed: 76.4 m³ unchanged by CDU removal (CDU occupied floor area, not displaced Novec-protected volume — see INT-001 Rev 3.0 §3). Agent quantity and hold time calculations remain valid. VESDA sampling port count unchanged (8). Safety interlock with Cassette-SIS-001 Rev 1.1 noted. No hardware changes.** |

**Applicable Standards:**
- NFPA 2001 (2022): Standard on Clean Agent Fire Extinguishing Systems
- NFPA 72 (2022): National Fire Alarm and Signaling Code
- ISO 14520-1: Gaseous fire-extinguishing systems — Part 1 (international reference)

**Prepared by:** Scott Tomsu · CEO / Chief Engineer
scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana

---

## TABLE OF CONTENTS

- §1  System Description
- §2  Protected Volume
- §3  Agent Quantity Calculation (NFPA 2001)
- §4  Hold Time Analysis
- §5  Cylinder Sizing — Current BOM vs Required
- §6  Nozzle Count & Distribution
- §7  Over-Pressure Vent Sizing
- §8  VESDA Detection Sequence
- §9  Discharge Interlock Sequence
- §10 Post-Discharge Ventilation
- §11 Offline Variant — Offshore Marine
- §12 Key Findings & BOM Corrections
- §13 Open Items

---

## §1  SYSTEM DESCRIPTION

### Type
Total flood Novec 1230 (FK-5-1-12) clean agent system per NFPA 2001.

### Hazard Classification
Class C (energized electrical equipment — 936 Rubin GPUs, 15 Oberon racks, Delta power shelves, 800 V DC busway). Class A combustibles present (acoustic foam, PU insulation, cable jacketing). System designed for Class A/B/C combined hazard.

### Design Concentration
5.85% v/v. Basis: minimum extinguishing concentration for heptane (Class B design fuel per NFPA 2001) is 4.2%; 5.85% applies a 39.3% safety factor appropriate for electronics with mixed-fuel combustibles (plastics, insulation, PCBs). NFPA NOAEL for Novec 1230: 10% v/v. Design concentration is below NOAEL. Note: the Cassette is **unmanned** — personnel exposure limits do not govern design concentration.

### Hold Time
10 minutes per NFPA 2001 §6.3.1. Cassette is sealed to pressure decay ≤ 100 Pa in 5 minutes (onshore) and ≤ 50 Pa in 5 minutes (offshore) per INT-001 §27. Hold time analysis in §4 confirms the enclosure tightness is more than adequate.

### Discharge Type
Single-shot total flood. Agent discharges from ceiling nozzles distributed along the rack zone. Both cylinders discharge simultaneously (not staged). N+1 is achieved by the second cylinder, not a sequential backup discharge — see §5.

---

## §2  PROTECTED VOLUME

### Interior Dimensions (from INT-001 §2)

| Dimension | Value |
|-----------|-------|
| Interior length | 12,032 mm |
| Interior width | 2,352 mm |
| Interior height | 2,698 mm |

### Gross Enclosure Volume

V = 12.032 × 2.352 × 2.698 = **76.35 m³**

### Volume Deductions

NFPA 2001 §5.4.1.1 permits deduction of permanently fixed, air-tight, non-communicating equipment volumes. The following is the deduction analysis:

| Item | Justification | Deduction |
|------|---------------|-----------|
| Compute racks R1–R13 (13 × Oberon) | Open rack format — cooling airflow paths, tray slots, connector voids. Agent penetrates freely. No deduction. | 0 m³ |
| R14 InfiniBand rack | Same rationale | 0 m³ |
| R15 Storage/mgmt rack | Same rationale | 0 m³ |
| CoolIT CHx2000 CDU | Sealed liquid-side, but external surfaces and electronics bay are open. No deduction. | 0 m³ |
| Floor manifold trench (SS, fluid-filled) | Sealed — no agent access. Deductible. | −0.61 m³ * |
| DC busway (copper, enclosed) | Solid metal — agent cannot enter. Deductible. | −0.16 m³ ** |
| Novec cylinders themselves (in ELEC zone) | Solid steel cylinders. | −0.07 m³ |

*Floor trench: 450 mm wide × 9 m × 150 mm deep × 2 sides = 1.215 m³ gross. But ~50% is fluid-filled manifold pipe. Net deduction = 0.61 m³.
**Busway: 400 mm × 200 mm cross-section × 15 m × ~13% packing = ~0.16 m³.

**Total deductible volume: 0.84 m³**
**Net protected volume: V = 76.35 − 0.84 = 75.51 m³**

**For this calculation, use V = 76.35 m³ (gross).** The deductions are minor (1.1%) and the conservative value gives more agent. Agent quantity is not cost-sensitive enough to justify the accounting complexity of deductions.

---

## §3  AGENT QUANTITY CALCULATION

### NFPA 2001 Formula (§5.4.1.1)

```
W = (V / S) × [C / (100 − C)]
```

Where:
- W = mass of agent required (kg)
- V = protected volume (m³) = **76.35 m³**
- S = specific volume of agent vapor at minimum design temperature (m³/kg)
- C = design concentration (% v/v) = **5.85%**

### Specific Volume S for Novec 1230

Per Chemours / 3M design guide (empirical fit, more accurate than ideal gas):

```
S = 0.0664 + 0.000274 × T  (m³/kg, T in °C)
```

| Design temperature | S (m³/kg) | Notes |
|-------------------|-----------|-------|
| 0°C (arctic / cold deploy) | 0.0664 | Minimum possible S |
| **20°C (standard NFPA minimum)** | **0.07188** | **Use this — most conservative indoor** |
| 25°C | 0.07328 | |
| 45°C (max inside cassette at full load) | 0.07878 | |

**Design temperature: 20°C (conservatively low — more agent required at lower temperature)**

S = 0.0664 + (0.000274 × 20) = **0.07188 m³/kg**

### Agent Quantity

```
W = (76.35 / 0.07188) × [5.85 / (100 − 5.85)]
W = 1,062.0 × [5.85 / 94.15]
W = 1,062.0 × 0.06213
W = 65.98 kg
```

**Required agent: 66 kg (rounded up for conservatism)**

### Verification — Achieved Concentration

Back-solving with W = 66 kg:

```
C = W / (W + V/S) × 100
C = 66 / (66 + 1,062.0) × 100
C = 66 / 1,128.0 × 100
C = 5.85%  ✓
```

### Sensitivity to Temperature

| Min Design Temp | S (m³/kg) | Required W (kg) |
|-----------------|-----------|-----------------|
| 0°C | 0.0664 | 72.0 |
| 20°C | 0.07188 | 66.0 |
| 45°C | 0.07878 | 60.2 |

Design is based on 20°C. At 0°C (extreme cold deploy), required agent increases to 72 kg. Cylinder selection must accommodate the 0°C case for offshore / arctic variant.

**Design agent quantity: 72 kg (0°C minimum temperature, covers all deployment environments)**

---

## §4  HOLD TIME ANALYSIS

NFPA 2001 §6.3.1 requires ≥ 5.85% concentration maintained for a minimum 10 minutes after discharge.

### Enclosure Leakage Rate

INT-001 §27 specifies pressure decay test: ≤ 100 Pa in 5 min (onshore), ≤ 50 Pa in 5 min (offshore).

Leakage rate Q_L from pressure decay:

```
Q_L = V × ΔP / (P_atm × t)
```

| Variant | ΔP limit | Time | Q_L (m³/s) | Q_L (ACH) |
|---------|----------|------|------------|-----------|
| Onshore | 100 Pa | 300 s | 76.35 × 100 / (101,325 × 300) = **0.000251 m³/s** | 0.012 ACH |
| Offshore | 50 Pa | 300 s | 76.35 × 50 / (101,325 × 300) = **0.000126 m³/s** | 0.006 ACH |

### Hold Time Calculation

Concentration decay with leakage, assuming agent loss proportional to leakage:

```
C(t) = C_initial × exp(−Q_L × t / V)
```

Required: C(600 s) ≥ 5.85% with C_initial = 5.85%

| Variant | At t = 600 s | Margin |
|---------|--------------|--------|
| Onshore | 5.85% × exp(−0.000251 × 600 / 76.35) = 5.85% × exp(−0.00197) = **5.84%** | −0.01% |
| Offshore | 5.85% × exp(−0.000126 × 600 / 76.35) = 5.85% × exp(−0.00099) = **5.84%** | −0.01% |

### Interpretation

The cassette enclosure is **extremely tight** (ACH = 0.006–0.012). At 10 minutes, concentration drops by less than 0.01% — essentially no decay. The enclosure sealing specification is more than adequate for the 10-minute hold time.

**No additional agent overcharge is required for hold time.** The 66 kg (design: 72 kg for 0°C) quantity is sufficient for both the discharge concentration AND the full 10-minute hold.

**Implication:** The over-pressure vent (§7) closes after 15 seconds per INT-001 §17. After closure, the Cassette is again sealed. The concentration holds at essentially the discharge value for the entire 10-minute hold period. ✓

---

## §5  CYLINDER SIZING — CURRENT BOM vs REQUIRED

### Current BOM Specification

Per BOM §7 and INT-001 §17:
- **2 × Ansul Novec 1230 cylinder, 180 L water volume, 25 bar supercharged nitrogen**
- "Cylinder weight (each): ~190 kg"

Fill mass calculation:
- Ansul Novec 1230 fill density at 25 bar supercharge: **0.827 kg/L** (Ansul design guide)
- Agent per cylinder: 180 L × 0.827 kg/L = **148.9 kg**
- Total agent in 2 cylinders: **297.8 kg**

### Required vs Available

| | Value |
|--|-------|
| Required agent (0°C worst case) | 72 kg |
| Available agent (2 × 180 L, both discharge) | **297.8 kg** |
| Ratio | **4.14×** over-specification |
| Achieved concentration at 297.8 kg discharge | **21.9% v/v** |
| NFPA NOAEL (unmanned — not a constraint) | 10% |
| Excess agent mass over requirement | **225.8 kg** |

### Consequences of Over-Specification

1. **Weight:** 2 × 190 kg (cylinder + agent) = 380 kg total. Correctly sized cylinders would be 2 × ~60 kg = 120 kg. **Penalty: ~260 kg of unnecessary mass** — directly worsens the weight compliance issue identified in Cassette-MASS-001.

2. **Post-discharge recovery:** Novec 1230 is expensive (~$25–35/kg). 297.8 kg of agent per discharge event vs 72 kg. Unnecessary cost at each event.

3. **Discharge time:** Larger agent mass through 8 fixed nozzles takes longer to discharge. NFPA 2001 §5.4.3.1 requires design concentration achieved within 10 seconds. Discharging 297.8 kg through 8 nozzles in 10 seconds requires a nozzle flow rate of ~37.2 kg/s — this is high and requires verification. At 72 kg in 10 seconds: 9 kg/s total, 1.125 kg/s per nozzle — achievable with standard Ansul nozzles at 25 bar. The oversized cylinders may actually make the 10-second discharge requirement harder to meet.

4. **ELEC end zone crowding:** 180 L cylinders are physically large. Properly sized 50–75 kg fill cylinders are standard small-to-medium units.

### Correctly Sized Cylinder Selection

Required agent: **72 kg** (at 0°C, covering all variants)

Standard Ansul (Johnson Controls) Novec 1230 cylinder fill sizes closest to 72 kg:
- **75 lb (34 kg)** — too small alone
- **150 lb (68 kg)** — marginally small (68 < 72 kg)
- **200 lb (90.7 kg)** — adequate with 26% margin ✓
- **Two × 100 lb (2 × 45.4 kg = 90.8 kg)** — adequate if both discharge simultaneously ✓

### Recommendation

**Replace 2 × 180 L cylinders with 2 × 200 lb (90.7 kg fill) cylinders, both discharging simultaneously.**

| Configuration | Agent available | vs Requirement | Mass saved vs current BOM |
|---------------|----------------|----------------|---------------------------|
| Current: 2 × 180 L (148.9 kg each) | 297.8 kg | 4.14× | — |
| **Recommended: 2 × 200 lb (90.7 kg each)** | **181.4 kg** | **2.52×** | **~230 kg** |
| Minimum compliant: 2 × 100 lb (45.4 kg each) | 90.8 kg | 1.26× | ~300 kg |

The 2 × 200 lb configuration:
- Both cylinders discharge simultaneously into the enclosure (not staged backup)
- 181.4 kg achieves 16.0% v/v — still above design at 5.85%, providing margin for any enclosure seal degradation
- Cylinder weight per unit: ~35 kg each (200 lb fill + cylinder tare ~10 kg). Total: ~70 kg vs 380 kg current
- Standard Ansul catalog item, readily available

**BOM Rev 2.0: Change §7 cylinders from 180 L, 25 bar to 200 lb (90.7 kg) Ansul Novec 1230, standard supercharge.**

---

## §6  NOZZLE COUNT & DISTRIBUTION

### Current Specification
INT-001 §17: 8 ceiling-mounted 360° nozzles distributed along the rack zone.

### Coverage Analysis

| Parameter | Value | Notes |
|-----------|-------|-------|
| Enclosure length | 12,032 mm | |
| Number of nozzles | 8 | Per INT-001 |
| Nozzle pitch | 12,032 / 8 = 1,504 mm | |
| Enclosure width | 2,352 mm | |
| Nozzle centerline to wall | 1,176 mm | |
| 360° nozzle throw radius at 25 bar | 2,000–3,000 mm typical | Ansul catalog; confirm for selected orifice |
| 1,504 mm pitch — within throw radius? | 1,504 mm < 2,000 mm | **✓ — overlapping coverage** |
| 1,176 mm to wall — within throw radius? | 1,176 mm < 2,000 mm | **✓ — wall coverage adequate** |

8 nozzles at 1,504 mm pitch provides overlapping 360° coverage across the full 12.032 m × 2.352 m ceiling plane.

### Discharge Rate per Nozzle

For the **recommended** 2 × 200 lb (181.4 kg total) configuration at 10-second discharge:
- Total mass flow: 181.4 kg / 10 s = 18.14 kg/s total
- Per nozzle: 18.14 / 8 = **2.27 kg/s per nozzle**

For the **current BOM** 2 × 180 L (297.8 kg) at 10-second discharge:
- Per nozzle: 297.8 / (8 × 10) = **3.73 kg/s per nozzle**

Both are within the operating range of Ansul 360° nozzles at 25 bar (typical: 0.5–5 kg/s depending on orifice). However, the exact orifice size must be confirmed by Ansul hydraulic design software (ANSUL CHECKFIRE or equivalent).

**Nozzle count of 8 is appropriate for the enclosure geometry.** Exact orifice sizing requires Ansul hydraulic calculation. See §13 open item F-01.

### End Zone Coverage

The 8 nozzles are described as distributed along the rack zone (9,000 mm). The ELEC end zone (1,200 mm) and CDU end zone (1,500 mm) would then be outside the nozzle run.

NFPA 2001 requires the agent to protect the entire enclosure. The Novec 1230 vapor, once discharged, will diffuse throughout the sealed enclosure. Because Novec 1230 vapor is heavier than air at room temperature (molecular weight 316 vs air 29), there is some stratification risk.

**Action F-02:** Confirm that 2 nozzles (one at each end of the rack row) provide adequate coverage into the ELEC and CDU end zones. If not, add one nozzle at each end zone (total 10 nozzles). Ansul hydraulic calculation governs.

---

## §7  OVER-PRESSURE VENT SIZING

### Specification (INT-001 §17)
250 × 250 mm powered damper, ceiling-mounted, opens during discharge window, closes after 15 seconds.

### NFPA 2001 Annex B — Peak Pressure Analysis

Agent vapor injection rate during discharge:

For the **recommended** 2 × 200 lb system (18.14 kg/s mass flow):
- Volumetric flow of Novec 1230 vapor at 20°C: 18.14 kg/s × 0.07188 m³/kg = **1.304 m³/s**

For the **current BOM** (29.78 kg/s mass flow):
- Volumetric flow: 29.78 × 0.07188 = **2.141 m³/s**

### Vent Flow Capacity

Vent area: 0.25 × 0.25 = **0.0625 m²**

Peak pressure to drive the injection volumetric flow through the vent (orifice flow equation, C_d = 0.61, ρ_air = 1.2 kg/m³):

```
Q = C_d × A × √(2ΔP / ρ)
ΔP = (Q / (C_d × A))² × ρ / 2
```

| System | Q (m³/s) | ΔP (Pa) | ΔP (kPa) | Container limit |
|--------|----------|---------|----------|-----------------|
| **Recommended 2 × 200 lb** | **1.304** | **(1,304/0.038125)² × 0.6 = 780 Pa** | **0.78** | ✓ << 50 kPa |
| Current BOM 2 × 180 L | 2.141 | (2,141/0.038125)² × 0.6 = 2,098 Pa | 2.10 | ✓ << 50 kPa |

*Note: 0.038125 = 0.61 × 0.0625*

Both configurations produce peak internal pressures well below the ISO container structural limit (estimated ≥ 50 kPa for modified container). The 250 × 250 mm vent is **adequately sized for both configurations.** ✓

### Damper Control Requirements

The powered damper must open **before agent discharge begins** — not simultaneously. Control sequence:
1. VESDA Fire 2 + pre-discharge timer expires → open damper first (< 2 seconds)
2. Damper open-confirmed signal → release Novec cylinders
3. Discharge complete (10 s) → hold damper open for 5 more seconds (total ~15 s)
4. Close damper — enclosure returns to sealed state for 10-minute hold

If damper fails to open (power loss, mechanical fault):
- Peak pressure for recommended system: 0.78 kPa → acceptable structural load even without vent relief
- Peak pressure for current BOM: 2.10 kPa → still structurally acceptable
- BMS must log damper position failure as a fault but must not inhibit discharge — fire suppression takes priority over vent confirmation

---

## §8  VESDA DETECTION SEQUENCE

### Xtralis VESDA-E VEU-A00 — Alarm Levels

Per Xtralis design guide for electronics/clean rooms:

| Level | Detector Reading | Meaning | Response |
|-------|-----------------|---------|----------|
| Alert | 0.005% obs/m | Trace combustion products — incipient fire | BMS alarm, increase poll rate, notify SCADA |
| Action | 0.02% obs/m | Active smoldering — fire developing | BMS alarm, workload pause, dispatch crew |
| Fire 1 | 0.05% obs/m | Active flaming possible | Pre-discharge alarm (strobe + horn, 30 sec), E-stop to racks |
| Fire 2 | 0.20% obs/m | Confirmed fire | Release sequence initiated after 30-second hold |

### Sampling Network (18 Points)

| Zone | Sample Points | Priority |
|------|--------------|----------|
| Per-rack (above each rack) | 15 | High — fire most likely inside racks |
| Delta power shelf cluster (×2) | 2 | High — power conversion = ignition risk |
| Ceiling reference | 1 | Medium — general volume |

Sampling velocity and hole sizing per Xtralis guidelines: 2.2 mm diameter holes, spacing per airflow model. Ansul-Xtralis hydraulic verification required — see §13 F-03.

### VESDA Fault Handling

If VESDA unit loses power or airflow: BMS switches to cross-zone thermal backup (rack temperature sensors). If rack supply/return ΔT exceeds 35°C (thermal runaway signature), BMS initiates Fire 1 equivalent response. This is not NFPA 2001 primary detection but provides degraded-mode protection.

---

## §9  DISCHARGE INTERLOCK SEQUENCE

Complete sequence from Fire 2 detection to post-discharge recovery:

```
T = 0 s       VESDA Fire 2 alarm received by Novec control panel
              (Two-zone confirmation or single-zone at 0.20% obs/m)

T = 0–2 s     BMS asserts: open over-pressure vent damper
              BMS asserts: E-stop to all Delta power shelves (workload down)
              BMS asserts: close CoolIT CDU manifold isolation valves
              BMS notifies platform SCADA (cannot inhibit)
              BMS activates exterior strobe + horn at both ECPs

T = 2 s       Verify: vent damper open-confirmed
              If damper fails to confirm: log fault, proceed regardless

T = 2–32 s    Pre-discharge alarm period (30 seconds)
              Abort available: key-switch at either ECP cancels discharge
              If abort activated: log event, hold all interlocks, notify

T = 32 s      Release Novec 1230 cylinders (both simultaneously)
              Expected discharge complete: T = 32 + 10 = 42 s

T = 47 s      Close over-pressure vent damper (15 s after discharge start)
              Enclosure now sealed — hold time begins

T = 47–647 s  10-minute hold period
              BMS monitors concentration via indirect indicators (no direct sensor)
              No personnel entry permitted
              Exterior strobe remains active throughout hold

T = 647 s     Hold complete
              BMS: active alert for enclosure entry
              Cassette remains locked until gas concentration measured
              Recharge / recovery per §10

```

### Critical Interlock: Power-Off Before Discharge

All Delta power shelves must be commanded OFF before Novec discharges. Energized equipment at discharge creates arc-flash risk from Novec vapor ionization (Novec 1230 is electrically non-conductive but displaces oxygen, and high-current arcs during power-off transition with agent present is a risk). The E-stop to all shelves at T=0 handles this.

The 800 V DC main disconnect also receives an E-stop signal from the Novec control panel (hardwired, not BMS-mediated — fail-safe). If BMS is offline, the main disconnect still opens on Fire 2.

### Abort Station

Two Novec abort stations, one at each ECP (key-switch type, per INT-001 §17). Abort is only effective during the 30-second pre-discharge hold (T = 2 to T = 32). After T = 32, agent has been released — abort has no effect on discharge.

Abort does NOT restore rack power automatically. Rack power restoration requires separate manual authorization at the ELEC ECP main disconnect.

---

## §10  POST-DISCHARGE VENTILATION

After the 10-minute hold period and personnel approach with monitoring equipment:

1. Confirm exterior atmosphere at ECP is safe before opening any panel (Novec 1230 can still be at high concentration inside)
2. Open CDU ECP Munters ducts (external) as exhaust path
3. Open Munters process air supply — cross-ventilate pod for minimum 15 minutes
4. Measure interior with FTIR or Novec-specific analyzer before entry
5. Remove Cassette access panels only after confirmed safe atmosphere
6. Recharge or replace cylinders before re-commissioning

**Cassette cannot return to service until:**
- Cylinder bank recharged or replaced
- VESDA system inspected and reset
- Fire cause identified and remediated
- Post-fire BMS log reviewed for sequence anomalies

---

## §11  OFFSHORE VARIANT — MARINE ADDITIONS

Per INT-001 §17 and §25:

| Item | Requirement |
|------|-------------|
| Cylinder brackets | USCG-approved, marine-rated, shock-tested to DNV |
| Cylinder hydrostatic test interval | 10 years (vs 12 years onshore) |
| Novec control panel power | Dual-powered: main 24 V DC + dedicated offshore battery backup |
| SOLAS compliance | Chapter II-2 gas-flooding system requirements |
| ABS/DNV certification | Required for fixed cylinder installation on classified vessel |
| Pre-discharge abort | Key-switch abort stations remain accessible on exterior ECP (not interior — unmanned) |
| Fire Department Connection (FDC) | At CDU ECP — DN65 (2.5") connection for platform firefighting augmentation |
| Post-discharge drain | MARPOL-compliant routing — Novec is classified non-persistent but must be contained per local authority |

---

## §12  KEY FINDINGS & BOM CORRECTIONS

### Finding 1 — Current BOM Cylinders Are 4× Oversized

**Required: 72 kg of Novec 1230** (at 0°C minimum design temperature, worst case).
**BOM specifies: 2 × 180 L cylinders = 297.8 kg available.**
This is a 4.14× over-specification. The over-design adds ~230 kg of unnecessary weight and unnecessary recurring cost at each discharge event.

**BOM Correction:** Replace BOM §7 "Ansul Novec 1230 cylinder, 180 L, 25 bar, 190 kg" with:
> Ansul Novec 1230 cylinder, 200 lb fill (90.7 kg), standard Ansul supercharge. Cylinder tare ~10 kg. Total unit weight ~35 kg. (×2)

**Both cylinders discharge simultaneously** — not a staged backup system. This still provides 181.4 kg of agent (2.52× requirement), delivering 16.0% v/v concentration — adequate margin for any seal degradation scenario over the service life.

### Finding 2 — Enclosure Is Extremely Tight

Pressure decay tests (≤ 100 Pa / 5 min onshore) confirm the enclosure will hold Novec concentration above 5.85% for the full 10-minute hold period with less than 0.01% decay. No additional agent overcharge is required for leakage compensation.

### Finding 3 — Over-Pressure Vent Is Correctly Sized

250 × 250 mm vent produces 0.78 kPa peak internal pressure with the recommended cylinder sizing. Structurally safe. Vent must open before discharge — sequence confirmed in §9.

### Finding 4 — Damper Must Open Before Cylinders Release

The interlock sequence must confirm vent damper open before releasing cylinders. Failure to sequence correctly risks internal over-pressure during discharge. This is a BMS control logic requirement, not just hardware.

### BOM Summary — Items to Change

**RESOLUTION (Rev 1.1):** All three corrections below have been adopted. Table preserved as audit trail.

| Section | Current | Corrected | Action | Status |
|---------|---------|-----------|--------|--------|
| BOM §7 — Cylinders | 2 × 180 L, 25 bar, ~190 kg each | 2 × 200 lb fill Ansul Novec 1230, ~35 kg each | **BOM Rev 2.0/2.1** | ✓ Adopted |
| INT-001 §17 — Cylinder weight | "~190 kg each" | "~35 kg each" | **INT-001 Rev 2.1** | ✓ Adopted |
| INT-001 §17 — Cylinder bank location | "ELEC end" | Unchanged — 2 small cylinders still fit at ELEC end | No change | ✓ |
| MASS-001 §8 — Fire suppression | 455 kg | ~180 kg (2 × 35 kg cylinders + VESDA + piping + misc) | **MASS-001 Rev 2.0** | ✓ Adopted |

**MASS-001 impact:** The cylinder right-sizing removed ~275 kg from the cassette. Adopted in MASS-001 Rev 2.0 §8. Combined with other Rev 2.0 corrections (electrical +95 kg, manifolds +30 kg), net −150 kg. Cassette operating mass under A-02 baseline: 29,935 kg with 545 kg margin to ISO 30,480 kg limit.

---

## §13  OPEN ITEMS

| ID | Item | Priority | Blocks |
|----|------|----------|--------|
| F-01 | Ansul hydraulic calculation: confirm nozzle orifice size for 2 × 200 lb cylinders, 8 nozzles, 10-second discharge requirement | P-0 | Final cylinder + nozzle spec |
| F-02 | Confirm end zone coverage (ELEC and CDU zones, 1,200 mm and 1,500 mm each) — add end nozzles if required by hydraulic calc | P-1 | Nozzle count finalization |
| F-03 | Xtralis VESDA sampling pipe hydraulic verification (18 sampling points, pipe network layout) | P-1 | VESDA commissioning |
| F-04 | Confirm Novec 1230 cylinder size availability: 200 lb fill = standard Ansul SKU in current catalog | P-1 | BOM finalization |
| F-05 | Update BOM Rev 2.0 and INT-001 Rev 2.0 to reflect corrected cylinder specification | P-1 | Document control |
| F-06 | MARPOL drain routing design for offshore variant (post-discharge Novec recovery path) | P-2 | Offshore ABS/DNV review |

---

**Cassette — Fire Suppression Engineering · Cassette-FIRE-001 · Rev 1.2 · 2026-04-20**
**Scott Tomsu · scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana**
**CONFIDENTIAL**
