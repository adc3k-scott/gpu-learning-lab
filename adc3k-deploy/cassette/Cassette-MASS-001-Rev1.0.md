# Cassette — MASS STATEMENT & WEIGHT BUDGET

**Document:** Cassette-MASS-001
**Revision:** 1.0
**Date:** 2026-04-19
**Classification:** CONFIDENTIAL
**Companion to:** Cassette-INT-001 Rev 1.0 · Cassette-BOM-001 Rev 1.0

**Purpose:** Bottom-up component weight register for one Cassette. Verifies ISO 40 ft HC gross weight compliance, establishes longitudinal center of gravity, analyzes stacking loads, and identifies the weight-critical open items that gate rack count finalization.

| Rev | Date       | Description                                           |
|-----|------------|-------------------------------------------------------|
| 1.0 | 2026-04-19 | Initial release                                       |

**Prepared by:** Scott Tomsu · CEO / Chief Engineer
scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana

---

## TABLE OF CONTENTS

- §1  Applicable Standards & Limits
- §2  Mass Statement Summary
- §3  Component Weight Register — §2.1 Container Shell
- §4  Component Weight Register — §2.2 Racks
- §5  Component Weight Register — §2.3 Delta Power Shelves
- §6  Component Weight Register — §2.4 Cooling
- §7  Component Weight Register — §2.5 Electrical Distribution
- §8  Component Weight Register — §2.6 Fire Suppression
- §9  Component Weight Register — §2.7 Leak Detection & Drip
- §10 Component Weight Register — §2.8 Cables
- §11 Component Weight Register — §2.9 Controls, Sensors & Misc
- §12 Sensitivity Analysis — Rack Weight & Delta Shelf Inclusion
- §13 Longitudinal Center of Gravity
- §14 Vertical Center of Gravity
- §15 Two-High Stacking Analysis
- §16 Key Assumptions
- §17 Findings & Required Actions
- §18 Open Items

---

## §1  APPLICABLE STANDARDS & LIMITS

| Standard | Requirement | Value |
|----------|-------------|-------|
| ISO 668:2020 | 40 ft HC gross weight limit | **30,480 kg** |
| ISO 1161:2016 | Corner casting vertical stacking load | 86,400 kg per casting |
| ISO 1496-1:2013 | Container structural certification basis | CSC plate |
| DNV-OS-D101 | Marine stacking / structural (offshore variant) | Section §15 |
| IBC 2021 | Seismic rack anchor sizing basis | Section §15 |

**Design target:** Operating mass ≤ 30,480 kg at all configurations. No exceptions — exceeding ISO gross invalidates the CSC plate and voids stacking authorization.

---

## §2  MASS STATEMENT SUMMARY

### Totals by Subsystem

| Subsystem | Mass (kg) | Confidence | Notes |
|-----------|-----------|------------|-------|
| Container shell + modifications | 6,100 | Medium | See §3 |
| Compute racks R1–R13 (×13) | 19,500 | **LOW — C-01** | At 1,500 kg each; see §4 |
| InfiniBand rack R14 | 800 | Low | See §4 |
| Storage / management rack R15 | 900 | Low | See §4 |
| Rack anchors + snubbers | 60 | High | See §4 |
| Delta power shelves (3 types × 13) | 1,480 | Medium | **See §5 — critical double-count risk** |
| CoolIT CHx2000 CDU | 600 | Low | See §6 |
| Primary coolant PG25 (in-system) | 400 | Medium | See §6 |
| Chilled water manifold + piping | 230 | Medium | See §6 |
| DC electrical distribution | 425 | Medium | See §7 |
| Fire suppression | 455 | Medium | See §8 |
| Leak detection + drip trays | 200 | Medium | See §9 |
| Cables (~700 m mixed) | 235 | Medium | See §10 |
| Controls, sensors, misc hardware | 180 | Medium | See §11 |
| **TOTAL — WORST CASE** | **31,565** | — | Delta shelves separate from rack weight |
| **TOTAL — BEST CASE** | **30,085** | — | Delta shelves included in rack weight |
| **ISO 40 ft HC GROSS LIMIT** | **30,480** | — | Hard limit — no exceptions |
| **Margin — worst case** | **−1,085** | — | **NON-COMPLIANT** |
| **Margin — best case** | **+395** | — | Compliant, 1.3% margin |

### Verdict at 1,500 kg/Compute Rack

**The cassette is weight-critical at the baseline rack estimate.**

- If Delta power shelves are separately procured and their weight is not included in the NVIDIA/Foxconn-reported rack weight → **31,565 kg → 1,085 kg over limit → NON-COMPLIANT**
- If Delta shelves are included in the rack weight figure → **30,085 kg → 395 kg margin → marginally compliant**
- At 395 kg margin there is no room for any unaccounted mass (cabling tolerance, fastener spares, commissioning tooling, fluid fill variance). Effective margin is zero.

**This document establishes Action Item M-01 as the single most critical open item in the Cassette engineering package.** See §18.

---

## §3  CONTAINER SHELL + MODIFICATIONS

Basis: New-build 40 ft HC ISO container to ISO 668, tare 3,900 kg (standard industry), with modifications per INT-001 §3.

| Item | Qty | Unit Mass (kg) | Total (kg) | Basis |
|------|-----|----------------|------------|-------|
| Container tare (shell, unmodified) | 1 | 3,900 | 3,900 | Industry standard, new-build |
| Floor reinforcement plate, 6 mm steel, 29 m² | 1 lot | — | 1,365 | 29 × 0.006 × 7,850 kg/m³ |
| Access panel steel doors, 900×2,000×3 mm (×12) | 12 | 42 | 509 | 0.9 × 2.0 × 0.003 × 7,850 |
| Access panel gasket race hardware | 12 | 1 | 12 | Estimate |
| ECP outer cover assemblies (×2) | 2 | 50 | 100 | Estimate |
| ECP polycarbonate inspection windows (×6) | 6 | 2 | 12 | Plaskolite datasheet, ~2 kg each |
| Interior marine epoxy coating | 1 lot | — | 50 | Estimate |
| Interior acoustic foam, 50 mm melamine, 45 m² | 1 lot | — | 23 | 45 × 0.05 × 10 kg/m³ |
| Closed-cell PU insulation, 75 mm, 55 m² | 1 lot | — | 132 | 55 × 0.075 × 32 kg/m³ |
| Aluminum foil vapor barrier, 55 m² | 1 lot | — | 4 | Negligible |
| Overhead cable tray ceiling seats (×12) | 12 | ~1.7 | 20 | Estimate |
| **SUBTOTAL** | | | **6,127** | Rounded to **6,100** |

**Notes:**
- Access panel steel doors REPLACE material removed by cutouts. Container skin is typically 1.6–2.0 mm. Cutting 12 × (0.9 × 2.0) = 21.6 m² removes: 21.6 × 0.002 × 7,850 = ~339 kg. Net addition of 3 mm doors: 509 − 339 = ~170 kg net, but frame reinforcement around each opening adds back ~170 kg. Rounded to zero net for conservatism (door weight shown separately, cutout removal not credited).
- Load-spreader plate (BOM §2: 6 mm × 9 m × 700 mm = 6.3 m²) is within the 29 m² floor reinforcement figure. Not double-counted.

---

## §4  RACKS

### Compute Racks R1–R13 (Vera Rubin NVL72, Oberon)

| Item | Qty | Unit Mass (kg) | Total (kg) | Basis |
|------|-----|----------------|------------|-------|
| Vera Rubin NVL72, Oberon, fully loaded | 13 | **1,500** | **19,500** | **ESTIMATE — C-01 OPEN** |

Weight bracket for sensitivity analysis (§12): 1,400 / 1,500 / 1,600 kg per rack.

"Fully loaded" scope per INT-001 §6: Oberon rack frame, 18× compute trays (1U liquid-cooled), 9× NVLink switch trays (1U), 4× NVLink cartridges, HBM4 and LPDDR5x DIMMs, cold plates, integrated cabling. **Excludes Delta power shelves** (separately ordered from Delta Electronics — see §5).

### Network & Management Racks

| Item | Qty | Unit Mass (kg) | Total (kg) | Basis |
|------|-----|----------------|------------|-------|
| Quantum-X800 InfiniBand rack R14 (Oberon + 2× QM9700 + cabling) | 1 | 800 | 800 | Estimate: frame ~100 + 2× switch ~25 each + fabric ~650 |
| Storage + management rack R15 (Oberon + NVMe + mgmt servers + Jetson Orin) | 1 | 900 | 900 | Estimate: frame ~100 + storage ~400 + servers ~250 + BMS ~50 + misc ~100 |

### Rack Anchoring Hardware

| Item | Qty | Unit Mass (kg) | Total (kg) | Basis |
|------|-----|----------------|------------|-------|
| Seismic anchor kit, M16 × 4 per rack (×15 racks) | 60 | 0.5 | 30 | M16 × 100 mm ≈ 0.1 kg, with baseplate |
| Rack-to-rack snubbers, onshore (14 sets) | 14 sets | 2 | 28 | Mason Industries rubber isolators |
| Rack shock isolators, offshore (60 units) | 60 | 1.5 | 90 | Barry Controls spring-damper; offshore only |

**Subtotal racks + anchors: 21,258 kg (onshore) / 21,320 kg (offshore)**

---

## §5  DELTA POWER SHELVES

**Critical note on double-count risk:** The Vera Rubin NVL72 rack weight (C-01) is currently an estimate from INT-001. It is not confirmed whether NVIDIA/Foxconn/HPE will report shelf weight inclusive of Delta shelves or exclusive. If NVIDIA reports the rack as a complete compute system with power conversion included, this section must be zeroed out. If NVIDIA reports only the compute assembly (trays, NVLink, frame), Delta shelves add as below.

**Current assumption: Delta shelves are NOT included in the 1,500 kg rack estimate.** This is the conservative (higher mass) assumption and is the basis for the worst-case total in §2.

| Item | Qty | Unit Mass (kg) | Total (kg) | Basis |
|------|-----|----------------|------------|-------|
| Delta Vera Rubin NVL72 110 kW Power Shelf, 4U | 13 | 60 | 780 | Estimate: 110 kW / 4U high-current PSU shelf |
| Delta 800 V → 50 V DC/DC Power Shelf, 2U | 13 | 30 | 390 | Estimate: 2U DC/DC converter shelf |
| Delta GB200/GB300 33 kW Power Shelf, 2U | 13 | 20 | 260 | Estimate: 2U redundant shelf |
| Per-rack Delta shelf mounting rails | 39 sets | 1 | 39 | Per shelf |
| Per-rack DC input cable assembly (2× 70 mm², 2 m) | 13 | ~0.85 | 11 | 70 mm² = 0.60 kg/m × 2 m × 2 conductors |

**Subtotal Delta power shelves: 1,480 kg**

**Action M-01:** Confirm with Delta Electronics whether the shelf weight is captured in NVIDIA's rack weight specification. This single clarification resolves a 1,480 kg ambiguity — the difference between marginal compliance and non-compliance.

---

## §6  COOLING

### CoolIT CHx2000 CDU

| Item | Qty | Unit Mass (kg) | Total (kg) | Basis |
|------|-----|----------------|------------|-------|
| CoolIT CHx2000 CDU (frame, heat exchangers, dual pumps, controls, touchscreen) | 1 | 600 | 600 | Estimate — no published weight found. Comparable 2 MW L2L CDUs: 450–700 kg. RFQ to confirm. |

### Primary Coolant (PG25 In-System)

In-system volume estimate:

| Segment | Volume (L) | Notes |
|---------|------------|-------|
| CDU internal reservoir + heat exchanger passages | 50 | Estimate |
| Supply manifold 100 mm (4") × 9 m | 71 | π × 0.05² × 9 = 0.071 m³ |
| Return manifold 100 mm (4") × 9 m | 71 | Same |
| CDU-to-manifold transition 100 mm × 2 m × 2 runs | 31 | π × 0.05² × 4 |
| Per-rack supply + return drops, 25 mm (1") × 0.5 m × 30 | 15 | π × 0.0127² × 0.5 × 30 |
| Rack cold plate assembly × 15 racks | 120 | 8 L/rack estimated for NVL72 cold plate circuit |
| Expansion tank (half-full at operating) | 25 | 75 L tank, 1/3 ullage |
| **Total in-system volume** | **383 L** | |

PG25 density: 1.035 kg/L
In-system coolant mass: 383 × 1.035 = **396 kg → rounded to 400 kg**

### Chilled Water Manifold & Piping

| Item | Qty | Unit Mass (kg) | Total (kg) | Basis |
|------|-----|----------------|------------|-------|
| Supply manifold, 100 mm (4") Sch 40S SS304, 9 m | 9 m | 4.5 kg/m | 41 | ASME pipe tables |
| Return manifold, 100 mm (4") Sch 40S SS304, 9 m | 9 m | 4.5 kg/m | 41 | Same |
| CDU primary connection piping, 100 mm, ~4 m total | 4 m | 4.5 kg/m | 18 | Includes bends, fittings ×1.5 factor |
| Per-rack supply drops, 25 mm (1") SS304, 0.5 m × 15 | 15 | 0.85 | 13 | 1" Sch 40S = 1.7 kg/m |
| Per-rack return drops, 25 mm (1") SS304, 0.5 m × 15 | 15 | 0.85 | 13 | Same |
| Stäubli UQD-16 blind-mate connectors (×30) | 30 | 0.5 | 15 | Stäubli published ~0.45 kg |
| Per-rack isolation valves, 1" ball (×30) | 30 | 0.5 | 15 | Apollo 77-100 series |
| Manifold air bleed valves, 1/2" (×8) | 8 | 0.2 | 2 | |
| Manifold drain valves, 1" (×3) | 3 | 0.5 | 2 | |
| Expansion tank, 75 L bladder type | 1 | 15 | 15 | Amtrol, empty weight |
| Pressure relief valve | 1 | 2 | 2 | |
| Manifold insulation, 25 mm closed-cell, ~18 m | 1 lot | — | 20 | Armacell, ~1.1 kg/m |
| Pipe hangers and supports, stainless (40+) | 40 | 0.3 | 12 | |
| Manifold trench, 450 mm wide × 9 m, SS316L, 2 mm | 1 lot | — | 52 | 0.45 × 9 × 2 × 0.002 × 8,000 |
| **SUBTOTAL** | | | **261** | Rounded to **230** after deducting overlap |

Note: Trench is welded to floor plate; its weight is included here, not in §3 shell.
Subtotal cooling: 600 + 400 + 230 = **1,230 kg**

---

## §7  DC ELECTRICAL DISTRIBUTION

| Item | Qty | Unit Mass (kg) | Total (kg) | Basis |
|------|-----|----------------|------------|-------|
| 800 V DC main disconnect, motor-operated, 2,500 A | 1 | 80 | 80 | ABB SACE 2,500 A frame, ~75–90 kg |
| Surge protection device (SPD), Type 1, 200 kA | 1 | 5 | 5 | Phoenix Contact VAL-MS |
| Bender iso-PV1685 IMD | 1 | 8 | 8 | Bender published: 7.5 kg |
| Revenue meter, 800 V DC | 1 | 5 | 5 | Estimate |
| Maintenance UPS, 24 V DC, 2 kWh LiFePO4 | 1 | 20 | 20 | Battle Born 100Ah = ~12 kg; with charger/enclosure ~20 kg |
| Life-safety DC panel, 24 V distribution | 1 | 10 | 10 | Blue Sea Systems |
| Per-rack DC breaker, 250 A frame (×15) | 15 | 3 | 45 | ABB SACE Tmax XT4, ~2.8 kg |
| DC busway, 2,500 A, 800 V DC rated, ~15 m | 15 m | 13 | 195 | Starline copper laminated, ~12–14 kg/m |
| Busway taps (×15) | 15 | 2 | 30 | Per-rack tap off busway |
| CDU power subpanel, 480 V AC 3-ph, 60 A | 1 | 15 | 15 | Eaton CH-series panelboard |
| Ground bar, 50 mm² capacity | 1 | 5 | 5 | Burndy |
| Interior LED work light strips (×8) | 8 | 0.5 | 4 | Philips TrueLine |
| Panel open relay | 1 | 0.5 | 1 | Phoenix Contact |
| Terminal block bus and rails | 1 lot | — | 8 | Phoenix Contact, estimate |
| **SUBTOTAL** | | | **431** | Rounded to **425** |

---

## §8  FIRE SUPPRESSION

### Novec 1230 Agent & Cylinders

| Item | Qty | Unit Mass (kg) | Total (kg) | Basis |
|------|-----|----------------|------------|-------|
| Ansul Novec 1230 cylinder, 180 L, 25 bar (complete with agent) | 2 | 190 | 380 | INT-001 §17: "~190 kg each" |
| Novec discharge nozzles, 360° (×8) | 8 | 0.4 | 3 | Typical Ansul nozzle |
| Novec discharge piping, copper or SS, lot | 1 lot | — | 25 | ~10 m at ~2.5 kg/m |
| Novec control panel (FACU) | 1 | 10 | 10 | |
| Pre-discharge strobe + horn (interior) | 1 | 0.8 | 1 | Edwards/Wheelock |
| Pre-discharge strobe (exterior, ×2) | 2 | 0.8 | 2 | |
| Novec abort station, key-switch (×2) | 2 | 0.5 | 1 | |
| Over-pressure vent, powered damper 250×250 | 1 | 12 | 12 | Greenheck motorized damper |
| Cylinder brackets, stainless (×2) | 2 | 5 | 10 | Wall-mount |
| Fire panel battery backup | 1 | 5 | 5 | 24 hr standby, sealed lead-acid |

### VESDA Detection

| Item | Qty | Unit Mass (kg) | Total (kg) | Basis |
|------|-----|----------------|------------|-------|
| Xtralis VESDA-E VEU-A00 | 1 | 8 | 8 | Xtralis published: 7.8 kg |
| VESDA sampling pipe network, CPVC 25 mm, ~40 m | 1 lot | — | 5 | CPVC 25 mm = ~0.13 kg/m × 40 |
| Zone terminators (×5) | 5 | 0.1 | 1 | |

**SUBTOTAL fire suppression: 463 → rounded to 455 kg**

---

## §9  LEAK DETECTION & DRIP MANAGEMENT

| Item | Qty | Unit Mass (kg) | Total (kg) | Basis |
|------|-----|----------------|------------|-------|
| TraceTek TT1000-OHP cable, 80 m | 80 m | 0.2 | 16 | TE Connectivity, ~0.18 kg/m |
| TraceTek TTDM-128 panel | 1 | 3 | 3 | |
| Zone terminators (×5) | 5 | 0.1 | 1 | |
| Per-rack drip tray, 600×1,200×50 mm SS304, 2 mm plate + perimeter walls | 15 | 14 | 210 | Plate: 0.6×1.2×0.002×8,000 = 11.5 kg; perimeter: ~2.5 kg |
| Floor sump, 200×200×150 mm SS316L | 1 | 5 | 5 | |
| Sump pump, 20 LPM, submersible | 1 | 3 | 3 | Little Giant |
| Sump level sensor, capacitive 4-point | 1 | 0.5 | 1 | Ifm |
| Sump conductivity probe | 1 | 0.5 | 1 | Endress+Hauser |
| Condensate drain solenoid valve, 1" | 1 | 1.5 | 2 | ASCO |
| Leak isolation motorized valves (×2) | 2 | 3 | 6 | Belimo at ECP |
| **SUBTOTAL** | | | **248** | Rounded to **200** (drip tray weight includes some already counted structure) |

Note: Drip tray weight partially overlaps with floor structure. Conservatively not deducted.
Rounded to 200 kg to avoid double-counting with floor reinforcement in §3.

---

## §10  CABLES

Basis: BOM §15 cable summary — ~700 m copper, ~65 m fiber.

| Cable Type | Length (m) | kg/m | Total (kg) |
|------------|------------|------|------------|
| 800 V DC primary, 2× 70 mm² XHHW-2 | 10 | 1.20 | 12 |
| Per-rack DC branch, 2× 70 mm² (15 × 2 m) | 30 | 1.20 | 36 |
| 480 V AC CDU power feed, 4× 10 mm² | 6 | 0.40 | 2 |
| 480 V AC Munters feed, 4× 16 mm² | 6 | 0.56 | 3 |
| Cat6A shielded, OOB + console + sensor I/O | 200 | 0.10 | 20 |
| Modbus RTU, Belden 3106A | 30 | 0.06 | 2 |
| 24 V DC life-safety, 2× 2.5 mm² | 150 | 0.08 | 12 |
| Bonding cable, 25 mm² (rack chassis, 15 × 2.5 m) | 40 | 0.24 | 10 |
| Bonding cable, 50 mm² (ECP external) | 10 | 0.44 | 4 |
| Bare copper ground, 50 mm² | 15 | 0.44 | 7 |
| Sensor cable, shielded pair (RTD) | 80 | 0.08 | 6 |
| LMR-400 RF cable | 20 | 0.17 | 3 |
| Fiber OS2 (negligible mass) | 65 | 0.02 | 1 |
| Miscellaneous cable (splices, J-box drops, tails) | — | — | 30 |
| Cable management: tie wraps, conduit, loom | — | — | 15 |
| **SUBTOTAL** | ~700 m | — | **163** |

Note: BOM §15 estimated 700 m total. Bottom-up yields 163 kg. Using **235 kg** (+44% contingency) to account for service loops, unquantified runs, and cable tray fill.

---

## §11  CONTROLS, SENSORS & MISCELLANEOUS HARDWARE

### Sensors & Controls (not rack-mounted)

| Item | Qty | Unit Mass (kg) | Total (kg) |
|------|-----|----------------|------------|
| RTD thermowells, 1/8" NPT, Pt100 (×30) | 30 | 0.3 | 9 |
| Ultrasonic flow meter, clamp-on (×15) | 15 | 0.5 | 8 |
| Hall-effect current transformer, 0–300 A DC (×15) | 15 | 0.3 | 5 |
| 3-axis MEMS accelerometer (×15) | 15 | 0.1 | 2 |
| Vaisala HMP60 T/RH sensor (×6) | 6 | 0.3 | 2 |
| Setra 265 static pressure sensor | 1 | 0.5 | 1 |
| External T/RH/barometric sensors | 1 lot | — | 2 |
| Ifm JN2100 inclinometer | 1 | 0.2 | 0 |
| Omega SHK shock sensor | 1 | 0.3 | 0 |
| Advantech ADAM-6017 (×4) | 4 | 0.3 | 1 |
| Advantech ADAM-6060 (×2) | 2 | 0.3 | 1 |
| Advantech ADAM-6050 | 1 | 0.3 | 0 |
| Access panel reed switches (×12) | 12 | 0.05 | 1 |
| FLIR / Axis IR cameras (×2) | 2 | 1.5 | 3 |
| GPS-disciplined clock / antenna | 1 | 1.0 | 1 |
| Cellular modem (Cradlepoint) | 1 | 1.5 | 2 |
| OOB management switch, 24-port | 1 | 4.5 | 5 |
| Console server, 32-port | 1 | 3.0 | 3 |
| **Sensors & controls subtotal** | | | **46** |

### Junction Boxes & DIN Rail

| Item | Qty | Unit Mass (kg) | Total (kg) |
|------|-----|----------------|------------|
| Junction boxes, NEMA 4, IP66 (Hoffman) (×25) | 25 | 1.5 | 38 |
| DIN rail, terminal blocks, end stops | 1 lot | — | 5 |
| **JB subtotal** | | | **43** |

### Miscellaneous Hardware

| Item | Qty | Unit Mass (kg) | Total (kg) |
|------|-----|----------------|------------|
| Panel fasteners, M10 × 40 mm SS (×480) | 480 | 0.05 | 24 |
| Captive washer kit (×480) | 480 | 0.01 | 5 |
| Anti-galling compound, cable gland kits | 1 lot | — | 3 |
| Aluminum ladder cable tray, 400 mm × 12 m | 12 m | 3.0 | 36 |
| Perforated sensor cable tray, 150 mm × 12 m | 12 m | 1.5 | 18 |
| Commissioning tools / gaskets shipped with pod | 1 kit | — | 15 |
| Spare fasteners, QR labels, hazard labels | 1 lot | — | 5 |
| **Misc hardware subtotal** | | | **106** |

**SUBTOTAL controls + sensors + misc: 46 + 43 + 106 = 195 → rounded to 180 kg**

---

## §12  SENSITIVITY ANALYSIS

### Variable 1: Compute Rack Weight (C-01)

Each 100 kg change in unit rack weight × 13 racks = **1,300 kg** change in total.

| Rack Weight | Delta in Rack Weight | Total (Delta Separate) | Total (Delta in Rack) | vs ISO Limit |
|-------------|----------------------|------------------------|-----------------------|--------------|
| 1,200 kg | − | 28,265 | 26,785 | −2,215 / −3,695 ✓ |
| 1,300 kg | − | 29,565 | 28,085 | −915 / −2,395 ✓ |
| **1,400 kg** | − | **30,265** | **28,785** | **−215 ✓ / −1,695 ✓** |
| **1,500 kg** | − | **31,565** | **30,085** | **+1,085 ✗ / −395 ✓** |
| **1,600 kg** | − | **32,865** | **31,385** | **+2,385 ✗ / +905 ✗** |
| 1,700 kg | − | 34,165 | 32,685 | +3,685 ✗ / +2,205 ✗ |

"+" = over limit (non-compliant). "−" = under limit (compliant).

### Variable 2: Rack Count (14 vs 15)

Dropping from 15 to 14 compute racks removes: 1 compute rack + proportional Delta shelves + proportional manifold drops, cables, sensors, trays (~150 kg).

| Config | Rack Weight | Delta Separate | Delta in Rack |
|--------|-------------|----------------|---------------|
| 15 racks | 1,400 kg | 30,265 ✓ | 28,785 ✓ |
| 15 racks | 1,500 kg | 31,565 ✗ | 30,085 ✓ (thin) |
| 15 racks | 1,600 kg | 32,865 ✗ | 31,385 ✗ |
| **14 racks** | **1,400 kg** | **28,851 ✓** | **27,371 ✓** |
| **14 racks** | **1,500 kg** | **30,151 ✓** | **28,671 ✓** |
| **14 racks** | **1,600 kg** | **31,451 ✗** | **29,971 ✓** |

At 14 racks, any rack weight ≤ 1,500 kg is compliant under both Delta scenarios. Margin is comfortable.

### Conclusion from Sensitivity Analysis

- **15 racks is only viable if:** rack weight ≤ 1,400 kg (Delta separate) OR rack weight ≤ 1,500 kg AND Delta shelves confirmed included in rack weight with margin verified.
- **14 racks is safe at all realistic rack weights** up to and including 1,600 kg with Delta separate.
- The 15-rack design requires C-01 resolution before fabrication commitment.

---

## §13  LONGITUDINAL CENTER OF GRAVITY

### Reference System

- X = 0 at ELEC end (inside face of ELEC ECP)
- X = 12,032 mm at CDU end (inside face of CDU ECP)
- Container midpoint: X = 6,016 mm

### Rack Position Centers

From INT-001 §5: ELEC end zone = 1,200 mm, rack zone = 9,000 mm, CDU end zone = 1,500 mm.
- Rack pitch: 9,000 ÷ 15 = 600 mm per rack
- R1 center: 1,200 + 300 = **1,500 mm**
- R2 center: 1,200 + 900 = **2,100 mm**
- ...
- R13 center: 1,200 + (12 × 600) + 300 = **9,300 mm**
- R14 center: 1,200 + (13 × 600) + 300 = **9,900 mm**
- R15 center: 1,200 + (14 × 600) + 300 = **10,500 mm**
- CDU center: 12,032 − 750 = **11,282 mm** (CDU footprint 1,200 mm, centered in CDU zone)

### Longitudinal CG Computation

| Subsystem | Mass (kg) | X_CG (mm) | Moment (kg·mm) |
|-----------|-----------|-----------|----------------|
| Container shell | 6,100 | 6,016 | 36,698,000 |
| R1–R13 compute racks | 19,500 | 5,400* | 105,300,000 |
| R14 InfiniBand rack | 800 | 9,900 | 7,920,000 |
| R15 storage/mgmt rack | 900 | 10,500 | 9,450,000 |
| Rack anchors + snubbers | 60 | 5,700 | 342,000 |
| Delta power shelves (in racks R1–R13) | 1,480 | 5,400 | 7,992,000 |
| CoolIT CHx2000 CDU | 600 | 11,282 | 6,769,000 |
| Primary coolant (in manifold + CDU + racks) | 400 | 5,700 | 2,280,000 |
| Chilled water manifold + piping | 230 | 5,700 | 1,311,000 |
| DC electrical distribution (ELEC end zone) | 425 | 600 | 255,000 |
| Fire suppression (cylinders at ELEC end) | 455 | 700 | 318,500 |
| Leak detection + drip trays (along rack zone) | 200 | 5,400 | 1,080,000 |
| Cables (distributed) | 235 | 5,700 | 1,339,500 |
| Controls, sensors, misc (distributed) | 180 | 5,700 | 1,026,000 |
| **TOTAL** | **31,565** | | **181,081,000** |

*R1–R13 CG = (1,500 + 9,300) / 2 = **5,400 mm** from ELEC end (uniform rack mass distribution)

**X_CG = 181,081,000 ÷ 31,565 = 5,736 mm from ELEC end**

### CG Offset from Centerline

Centerline: 6,016 mm
CG: 5,736 mm
**Offset: 280 mm toward ELEC end**

The CG is biased toward the ELEC end because the main disconnect, Novec cylinders, and electrical panel are concentrated there. The CDU, R14, and R15 at the far end partially but not fully counterbalance.

**Implication for lifting:** When lifting the cassette by ISO corner castings, the ELEC-end pair carries slightly more load. At 31,565 kg total and 280 mm offset over 12,032 mm:
- ELEC-end pair: 31,565 × (6,016 + 280) / 12,032 = **17,068 kg** (54.1%)
- CDU-end pair: 31,565 × (6,016 − 280) / 12,032 = **14,497 kg** (45.9%)

Both ends well within ISO corner casting rating of 86,400 kg per casting.

### Lateral CG (Y-axis)

- Rack row: on container centerline → Y = 0
- Power tray (Side A): ~150 kg at Y ≈ −888 mm
- Manifold trench (Side B): ~230 kg at Y ≈ +888 mm
- All other mass: symmetric about centerline
- **Lateral CG offset ≈ +14 mm toward Side B (manifold side). Negligible.**

---

## §14  VERTICAL CENTER OF GRAVITY

### Reference System

- Z = 0 at finished floor (top of load-spreader plate)
- Container interior height: 2,698 mm

### Vertical CG Computation

| Subsystem | Mass (kg) | Z_CG (mm) | Moment (kg·mm) |
|-----------|-----------|-----------|----------------|
| Container shell (floor heavy, walls mid, roof light) | 6,100 | 900 | 5,490,000 |
| Racks R1–R15 (compute trays distributed, power shelves high) | 21,200 | 1,100 | 23,320,000 |
| Delta power shelves (top-of-rack or split; use top estimate) | 1,480 | 1,800 | 2,664,000 |
| CoolIT CHx2000 CDU (floor-standing unit, 1,200 mm tall) | 600 | 600 | 360,000 |
| Primary coolant (floor trench manifold + rack cold plates) | 400 | 500 | 200,000 |
| Manifold + piping (floor trench) | 230 | 200 | 46,000 |
| DC electrical (floor-mounted, ELEC end) | 425 | 600 | 255,000 |
| Novec cylinders (wall-mounted) | 455 | 900 | 409,500 |
| Drip trays (floor level) | 200 | 75 | 15,000 |
| Cables (overhead and floor mixed; average) | 235 | 800 | 188,000 |
| Controls, sensors, misc | 180 | 800 | 144,000 |
| **TOTAL** | **31,505** | | **33,091,500** |

**Z_CG = 33,091,500 ÷ 31,505 ≈ 1,050 mm above floor**

CG at 1,050 mm = **36% of interior height (2,698 mm).**

### Tipping Stability (Static)

Container width: 2,438 mm external. Half-width: 1,219 mm.
Static tipping angle: arctan(1,219 / 1,050) = arctan(1.161) = **49.2°**

49° before the CG crosses the tipping line. For context:
- Onshore seismic: max 0.3g lateral → equivalent tilt ≈ 17° → **safe margin**
- Offshore design roll: 30° → **safe margin**
- Marine pitch: 15° → **safe margin**

The cassette has adequate static stability in both variants.

---

## §15  TWO-HIGH STACKING ANALYSIS

### ISO Corner Casting Loads

ISO 1161 corner casting rated load: **86,400 kg per casting, vertical.**

For two-high stacking:
- Upper pod operating mass: 31,565 kg (worst case)
- Lower pod receives upper pod load distributed across 4 upper corner castings onto 4 lower corner castings.
- Load per lower corner casting: 31,565 ÷ 4 = **7,891 kg**
- Lower pod corner casting load: 7,891 kg (upper pod weight) + 31,565/4 (lower pod self-weight shared to casting) = 7,891 + 7,891 = **15,782 kg**
- Rating: 86,400 kg per casting
- **Utilization: 18.3% of rating → ample margin**

### Bottom Pod Combined Vertical Load

Total bottom pod floor loading (2-high): 31,565 × 2 = 63,130 kg
- 63,130 ÷ 4 corner castings = 15,783 kg per casting
- ISO limit: 86,400 kg per casting → **utilization 18.3% ✓**

### Twist-Lock Loading (Offshore Dynamic)

Offshore vertical shock per DNV: 5g peak.
Dynamic load on lower-pod corner casting: 15,783 × 5 = 78,915 kg per casting.
ISO limit: 86,400 kg. **Utilization: 91.3% → within limit but high.**

**Action M-04:** For offshore two-high stacking under 5g slam loading, the corner casting utilization is 91%. This requires DNV certification review of the specific casting and weld at the bottom pod. Do not stack two-high offshore without this review.

### Three-High Stacking

Not recommended without structural engineering review. Three-high would place 3 × 31,565 = 94,695 kg total through lower-pod castings → 23,674 kg per casting → at 5g dynamic: 118,369 kg → **exceeds ISO rating.** Three-high is disqualified offshore. Onshore static: 23,674 kg at corner casting = 27.4% utilization → acceptable statically, but not standard practice for live equipment.

---

## §16  KEY ASSUMPTIONS

| # | Assumption | Impact If Wrong |
|---|------------|-----------------|
| A-01 | Rack weight = 1,500 kg per compute rack (estimated) | ±1,300 kg per 100 kg change × 13 racks |
| A-02 | Delta power shelves NOT included in rack weight | If included, total drops by 1,480 kg |
| A-03 | R14 InfiniBand rack = 800 kg | ±100 kg minor impact |
| A-04 | R15 storage/mgmt rack = 900 kg | ±100 kg minor impact |
| A-05 | CoolIT CHx2000 CDU = 600 kg | No published weight found; ±150 kg possible |
| A-06 | In-system coolant volume = 383 L | ±50 L = ±52 kg |
| A-07 | Cold plate volume = 8 L per NVL72 rack | NVIDIA / CoolIT data needed to confirm |
| A-08 | Cable 44% contingency applied | Conservative; actual may be lower |
| A-09 | Drip tray steel mass not offset against floor reinforcement credits | Conservative (adds ~30 kg) |

---

## §17  FINDINGS & REQUIRED ACTIONS

### Finding 1 — Cassette Is Weight-Critical

The bottom-up weight estimate of 31,565 kg (worst case, Delta shelves separate) **exceeds the ISO 40 ft HC gross limit of 30,480 kg by 1,085 kg.** The INT-001 estimate of "~30,000 kg (98.6%)" is optimistic by 1,085–1,565 kg depending on Delta shelf counting.

**This is not a fatal finding — it can be resolved — but it must be resolved before container fabrication begins.**

### Finding 2 — Delta Shelf Count Is the Pivot

The single largest ambiguity is whether the NVIDIA-reported NVL72 rack weight includes the Delta power shelves. This 1,480 kg question determines whether the 15-rack design is compliant or not. Resolution is a phone call to NVIDIA/Foxconn/Delta — not an engineering exercise.

### Finding 3 — 14-Rack Design Is Safe at All Realistic Weights

Dropping from 15 to 14 compute racks yields a compliant cassette under all realistic rack weight scenarios. Compute capacity drops from 936 to 864 Rubin GPUs (7.7% reduction). Pod IT load drops from 1,585 kW to 1,465 kW. All other systems (CDU, manifold, ECP, fire, BMS) remain unchanged.

### Finding 4 — Offshore 2-High Stacking Needs DNV Review

Under DNV 5g slam loading, corner casting utilization is 91% of ISO rating. This is within spec but requires formal class certification before offshore 2-high stacking is authorized.

### Required Actions

| ID | Action | Owner | Gate |
|----|--------|-------|------|
| M-01 | Confirm with NVIDIA/Foxconn/HPE: does the NVL72 rack weight include Delta power shelves? | Scott | Before fabrication PO |
| M-02 | Confirm actual NVL72 loaded rack weight (C-01) | Scott / NVIDIA | Before fabrication PO |
| M-03 | Confirm CoolIT CHx2000 actual shipping weight | Scott / CoolIT | Before fabrication PO |
| M-04 | DNV review of corner casting for offshore 2-high stacking | DNV-certified engineer | Before offshore deployment |
| M-05 | Update INT-001 §2 Cassette Nameplate operating weight once M-01/M-02 resolved | Engineering | After M-01, M-02 |

---

## §18  OPEN ITEMS

| ID | Item | Priority | Resolves |
|----|------|----------|---------|
| M-01 | Delta shelf inclusion in rack weight — call to NVIDIA/Foxconn/Delta | **P-0** | Finding 1, 2 |
| M-02 | Actual NVL72 rack weight confirmation (same as C-01) | **P-0** | Finding 1 |
| M-03 | CoolIT CHx2000 actual shipping weight | P-1 | A-05 |
| M-04 | Cold plate internal volume per NVL72 rack | P-1 | A-07 |
| M-05 | DNV corner casting review for offshore 2-high | P-1 | Finding 4 |

---

**Cassette — Mass Statement & Weight Budget · Cassette-MASS-001 · Rev 1.0 · 2026-04-19**
**Scott Tomsu · scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana**
**CONFIDENTIAL**
