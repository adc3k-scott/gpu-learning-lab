# Cassette — ELECTRICAL SINGLE-LINE DIAGRAM & DISTRIBUTION SPECIFICATION

**Document:** Cassette-ELEC-001
**Revision:** 1.2
**Date:** 2026-04-22
**Classification:** CONFIDENTIAL
**Companion to:** Cassette-INT-001 · Cassette-ECP-001 · Cassette-BOM-001 · Cassette-MASS-001 · Cassette-COOL-001

**Purpose:** Complete electrical engineering specification for one Cassette. Defines all power distribution circuits, conductor sizing, protective device ratings, grounding architecture, and auxiliary power systems. Serves as the fabricator-ready electrical specification and the basis for permit drawings.

**Prepared by:** Scott Tomsu · CEO / Chief Engineer
scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana

---

## TABLE OF CONTENTS

- §1  Electrical System Overview
- §2  One-Line Diagram — 480 V AC Primary Input
- §3  One-Line Diagram — 800 V DC Internal Distribution
- §4  One-Line Diagram — 480 V AC Auxiliary Circuits
- §5  One-Line Diagram — 24 V DC Life-Safety Bus
- §6  Load Schedule
- §7  Conductor Sizing — AC Main Feed
- §8  Conductor Sizing — Per Delta Rack AC Feeder
- §9  Conductor Sizing — 800 V DC Internal Bus
- §10 Conductor Sizing — DC Branch Circuits (Per Rack)
- §11 Conductor Sizing — Auxiliary & Life-Safety
- §12 Voltage Drop Analysis
- §13 Protective Device Coordination
- §14 DC Busway Sizing
- §15 Fault Current Analysis
- §16 Grounding & Bonding Architecture
- §17 Ungrounded IT System (IMD) Architecture
- §18 Engineering Analysis Notes
- §19 Open Items

---

## §1  ELECTRICAL SYSTEM OVERVIEW

### Four Independent Power Systems

The Cassette contains four electrically separate power systems. They share a common grounding reference but are otherwise independent.

| System | Voltage | Source | Function | ECP Entry |
|--------|---------|--------|----------|-----------|
| Primary AC | 480 V AC 3-ph | Platform | Feeds 5 × Delta 660 kW in-row racks | ELEC ECP — high-current AC (see §19 E-01) |
| 800 V DC Internal | 800 V DC, ungrounded | Delta rack outputs | Distributes DC to compute racks via internal busway | No ECP — internal only |
| Auxiliary AC | 480 V AC 3-ph | Platform | Munters DSS Pro dehumidification | CDU ECP — IEC 60309 pin-and-sleeve |
| Life-Safety DC | 24 V DC | Internal UPS (LiFePO4 2 kWh) | BMS, fire panel, sensors, lighting | Self-contained (no ECP) |

**The 480 V AC primary enters the Cassette at the ELEC ECP, feeds all five Delta 660 kW in-row power racks, and is converted to 800 V DC inside the Cassette. The 800 V DC bus does not appear at any ECP — it is entirely internal.**

### Key Electrical Parameters

| Parameter | Value | Basis |
|-----------|-------|-------|
| Installed capacity | **3,300 kW** | 5 × Delta 660 kW in-row power racks |
| Embedded battery backup | **2,400 kW** | 480 kW BBU per Delta rack × 5 (no separate UPS required for compute) |
| Primary AC input voltage | 480 V AC 3-ph, 60 Hz | Delta rack input spec: 400–480 VAC |
| AC primary input current (PF = 0.95) | **4,179 A per phase** | 3,300,000 ÷ (√3 × 480 × 0.95) |
| NEC 125% continuous factor (AC main) | **5,224 A** | 4,179 × 1.25 |
| AC main disconnect rating | **6,000 A** | Next standard above 5,224 A |
| Internal 800 V DC bus current (installed basis) | **4,125 A** | 3,300,000 ÷ 800 V |
| NEC 80% continuous busway rule | Minimum busway: **5,156 A** | 4,125 ÷ 0.80 |
| Specified DC internal busway | **6,000 A** | Next standard above 5,156 A |
| System grounding (DC bus) | Ungrounded IT per IEC 61557-8 | INT-001 §17 / §16 |
| Fault current withstand at ECP | 50 kA for 100 ms | ECP-001 §5 |
| Auxiliary AC voltage | 480 V AC 3-ph, 60 Hz | INT-001 §8 |
| Life-safety DC voltage | 24 V DC nominal | INT-001 §22 |

**All infrastructure ratings are based on 3,300 kW installed capacity — the nameplate output of the five Delta racks operating simultaneously. Actual GPU utilization does not govern equipment sizing.**

---

## §2  ONE-LINE DIAGRAM — 480 V AC PRIMARY INPUT

```
═══════════════════════════════════════════════════════════════════════
  ELEC ECP (CASSETTE BOUNDARY — PLATFORM SIDE LEFT, POD SIDE RIGHT)
═══════════════════════════════════════════════════════════════════════

  PLATFORM SIDE                        POD SIDE
  ─────────────                        ─────────
  L1 ──[HIGH-CURRENT AC CONNECTOR — E-01]────────────────────────────
  L2 ──[HIGH-CURRENT AC CONNECTOR — E-01]────────────────────────────
  L3 ──[HIGH-CURRENT AC CONNECTOR — E-01]────────────────────────────
  N  ──[HIGH-CURRENT AC CONNECTOR — E-01]────────────────────────────
  G  ──[HIGH-CURRENT AC CONNECTOR — E-01]────────────────────────────
       480 V AC 3-ph, 4,179 A per phase
       Connector type: see §19 E-01             │  │  │  │  │
                                                │  │  │  │  │
                             ┌──────────────────┴──┴──┴──┴──┴──────┐
                             │  AC MAIN DISCONNECT                   │
                             │  480 V AC 3-ph, 6,000 A               │
                             │  Motor-operated, padlockable          │
                             │  Trip coil: E-stop hardwired         │
                             └──────────────┬──┬──┬────────────────-┘
                                            │  │  │
                             ┌──────────────┴──┴──┴────────────────-┐
                             │  REVENUE METER                        │
                             │  ANSI C12.20, 0.5% class              │
                             │  480 V AC 3-ph rated                  │
                             └──────────────┬──┬──┬────────────────-┘
                                            │  │  │
                        ┌───────────────────┴──┴──┴─────────────────────────┐
                        │  480 V AC DISTRIBUTION — ~12 m run                  │
                        │  5 feeders @ ~1,200 A per rack (see §8)             │
                        └──┬──────┬──────┬──────┬──────┬──────────────────┘
                           │      │      │      │      │
                        FEEDER FEEDER FEEDER FEEDER FEEDER
                          F1    F2    F3    F4    F5
                        1,200A 1,200A 1,200A 1,200A 1,200A
                        breaker each — 480 V AC 3-ph rated
                           │      │      │      │      │
                           ▼      ▼      ▼      ▼      ▼
                        ┌──────────────────────────────────────────┐
                        │  DELTA 660 kW IN-ROW POWER RACK (×5)     │
                        │  Input:  480 V AC 3-ph                   │
                        │  Output: 800 V DC                        │
                        │  Conversion: 6 × 110 kW AC/DC shelves    │
                        │  Embedded BBU: 480 kW per rack            │
                        │  Efficiency: up to 98%                   │
                        └──────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════
  GROUNDING: Single-point ground bar at ELEC end. AC neutral and
  equipment ground bonded at SPG. 800 V DC bus is FLOATING — not
  bonded to SPG or neutral. See §16.
═══════════════════════════════════════════════════════════════════════
```

---

## §3  ONE-LINE DIAGRAM — 800 V DC INTERNAL DISTRIBUTION

The 800 V DC bus is entirely internal to the Cassette. It does not appear at any ECP. All five Delta in-row racks output 800 V DC to a common busway. The busway distributes to compute racks via branch breakers.

```
═══════════════════════════════════════════════════════════════════════
  800 V DC INTERNAL BUS — SOURCE: 5 × DELTA 660 kW RACKS
═══════════════════════════════════════════════════════════════════════

  DELTA RACK OUTPUTS (×5 — each 660 kW / 825 A at 800 V DC)
           │        │        │        │        │
        DR1      DR2      DR3      DR4      DR5
        825A     825A     825A     825A     825A
           │        │        │        │        │
  ┌────────┴────────┴────────┴────────┴────────┴────────────────────┐
  │          800 V DC MAIN BUS — 6,000 A RATED — ~12 m run          │
  └───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬────────────────────────┘
      │   │   │   │   │   │   │   │   │   │
     B01 B02 B03 B04 B05 B06 B07 B08 B09 B10
   250A/250A trip MCCB (R1–R9) / 250A/200A trip (R10) — 800 V DC rated — See §13
      │   │   │   │   │   │   │   │   │   │
     R1  R2  R3  R4  R5  R6  R7  R8  R9  R10
   2×95mm² branch cable (R1–R9) / 2×70mm² (R10), ~2 m each (see §10)
      │                                   │
      ▼                                   ▼
  ┌─────────┐                       ┌──────────┐
  │ COMPUTE │  ×9 (R1–R9)           │ CONTROL  │ R10
  │ NVL72   │                       │ IB + mgmt│
  │ 120 kW  │                       │ ~25 kW   │
  │ per rack│                       └──────────┘
  ├─────────┤
  │ Delta   │ 800V→50V DC/DC Shelf — final conversion for GPU bus
  └─────────┘

  NOTE: Compute rack positions R1–R9 and control R10 are shown.
  Delta in-row power racks occupy 5 of the 15 rack positions (R11–R15
  or interspersed — physical layout per INT-001).
  Total rack positions: 9 compute + 1 control + 5 Delta power = 15.

═══════════════════════════════════════════════════════════════════════
  Bender iso-PV1685 IMD: monitors 800 V DC bus — floating (ungrounded IT).
  Alarm < 5 kΩ insulation. Trip < 1 kΩ. See §17.
═══════════════════════════════════════════════════════════════════════
```

---

## §4  ONE-LINE DIAGRAM — 480 V AC AUXILIARY CIRCUITS

One auxiliary AC feed enters the Cassette at the **CDU ECP** (not ELEC ECP). Independent of the primary compute power. The external CDU skid has its own dedicated 480 V AC service furnished directly by the platform — not routed through the cassette.

```
═══════════════════════════════════════════════════════════════════════
  CDU ECP — 480 V AC AUXILIARY INPUTS
═══════════════════════════════════════════════════════════════════════

  PLATFORM SIDE                     POD SIDE
  ─────────────                     ─────────

  CIRCUIT AUX-1 — MUNTERS POWER
  480 V AC 3-ph ──[IEC 60309, 80 A]──────────────────────────────────
                    Pin-and-sleeve,
                    IP67                       │
                                    ┌──────────┴───────────────────┐
                                    │  MUNTERS DSS PRO POWER FEED   │
                                    │  480 V AC 3-ph, 80 A          │
                                    │  Direct to external skid      │
                                    │  via CDU ECP M12 connector    │
                                    └──────────┬───────────────────-┘
                                               │
                                    ┌──────────┴───────────────────┐
                                    │  Munters DSS Pro (external)   │
                                    │  480 V AC, ~25 kW running     │
                                    └──────────────────────────────-┘

═══════════════════════════════════════════════════════════════════════
  AUX-1 is platform responsibility up to CDU ECP.
  CDU skid has its own dedicated 480 V AC service.
═══════════════════════════════════════════════════════════════════════
```

---

## §5  ONE-LINE DIAGRAM — 24 V DC LIFE-SAFETY BUS

Self-contained. No ECP penetration. Maintenance UPS charges from the internal 800 V DC bus (via integral DC/DC charger). Maintains life-safety loads for ≥ 2 hours on loss of primary power.

```
═══════════════════════════════════════════════════════════════════════
  24 V DC LIFE-SAFETY BUS — INTERNAL ONLY
═══════════════════════════════════════════════════════════════════════

             [INTERNAL 800 V DC BUS — Delta rack outputs]
                       │
              ┌────────┴────────────────────┐
              │  MAINTENANCE UPS             │
              │  24 V DC / 2 kWh LiFePO4    │
              │  Integral DC/DC charger      │
              │  Runtime @ 270 W: ≥ 7 hours  │
              │  Location: ELEC end zone     │
              └────────┬────────────────────-┘
                       │
              ┌────────┴────────────────────┐
              │  LIFE-SAFETY DC PANEL       │
              │  24 V DC distribution       │
              │  Blue Sea Systems           │
              └──┬──┬──┬──┬──┬──┬──┬──┬───-┘
                 │  │  │  │  │  │  │  │
                 │  │  │  │  │  │  │  │
           LS-1  │  │  │  │  │  │  │  │  LS-8
        VESDA-E  │  │  │  │  │  │  │  │  Interior LED work lights
         35 W    │  │  │  │  │  │  │  │  50 W (panel-open only)
                 │  │  │  │  │  │  │  │
           LS-2  │  │  │  │  │  │  │  LS-7
         Novec   │  │  │  │  │  │  │  Exterior emergency
         control │  │  │  │  │  │  │  strobes (×2) — 40 W
         panel   │  │  │  │  │  │  │
         25 W    │  │  │  │  │  │  │
                 │  │  │  │  │  │  │
           LS-3  │  │  │  │  │  │  LS-6
      Jetson AGX │  │  │  │  │  │  Sump pump
      Orin BMS   │  │  │  │  │  │  + solenoid
      primary    │  │  │  │  │  │  valves — 20 W
      40 W       │  │  │  │  │  │
                 │  │  │  │  │  │
           LS-4  │  │  │  │  │  LS-5
      Jetson AGX │  │  │  │  │  ADAM I/O
      Orin BMS   │  │  │  │  │  modules
      standby    │  │  │  │  │  + sensors
      40 W       │  │  │  │  │  30 W
                 │  │  │  │
           [Starlink modem — 75 W]
                 │  │
           [Panel reed switches — 1 W]

═══════════════════════════════════════════════════════════════════════
  TOTAL CONTINUOUS LIFE-SAFETY LOAD: ~306 W
  PEAK (panel open event): ~356 W
  2 kWh capacity at 356 W: 5.6 hours — exceeds 2-hour design target ✓
  NOTE: Compute load UPS function is provided by Delta rack embedded
  BBU (2,400 kW total). No separate compute UPS is required.
═══════════════════════════════════════════════════════════════════════
```

---

## §6  LOAD SCHEDULE

### Installed Capacity Basis

All electrical infrastructure is sized to the **installed capacity of the five Delta 660 kW in-row power racks.** Actual GPU utilization does not govern equipment sizing.

| Parameter | Value |
|-----------|-------|
| Delta in-row racks | 5 units |
| Capacity per rack | 660 kW |
| **Total installed capacity** | **3,300 kW** |
| Internal 800 V DC bus current | 4,125 A |
| AC primary input current (PF = 0.95) | 4,179 A per phase |
| Embedded BBU (compute) | 2,400 kW (480 kW × 5) |

### 800 V DC Internal Distribution — Per Rack

| Circuit | Rack | Load Type | IT Load (kW) | Current (A) | Breaker | Conductor |
|---------|------|-----------|--------------|-------------|---------|-----------|
| B-01 | R1 | Compute NVL72 / CPX | 120–160 | 150–200 | 250A/250A | 2× 95 mm² |
| B-02 | R2 | Compute NVL72 / CPX | 120–160 | 150–200 | 250A/250A | 2× 95 mm² |
| B-03 | R3 | Compute NVL72 / CPX | 120–160 | 150–200 | 250A/250A | 2× 95 mm² |
| B-04 | R4 | Compute NVL72 / CPX | 120–160 | 150–200 | 250A/250A | 2× 95 mm² |
| B-05 | R5 | Compute NVL72 / CPX | 120–160 | 150–200 | 250A/250A | 2× 95 mm² |
| B-06 | R6 | Compute NVL72 / CPX | 120–160 | 150–200 | 250A/250A | 2× 95 mm² |
| B-07 | R7 | Compute NVL72 / CPX | 120–160 | 150–200 | 250A/250A | 2× 95 mm² |
| B-08 | R8 | Compute NVL72 / CPX | 120–160 | 150–200 | 250A/250A | 2× 95 mm² |
| B-09 | R9 | Compute NVL72 / CPX | 120–160 | 150–200 | 250A/250A | 2× 95 mm² |
| B-10 | R10 | Control / IB / mgmt | 25 | 31 | 250A/200A | 2× 70 mm² |
| **TOTAL** | | | **1,105–1,440** | **1,381–1,831** | Main: 6,000A DC bus | Internal busway |

**DC branch circuit totals span NVL72 tier (1,105 kW / 1,381 A) to NVL144 CPX tier (1,440 kW / 1,800 A). Busway and all upstream equipment are sized to 3,300 kW installed capacity. Branch conductors (2× 95 mm² per polarity, R1–R9) are sized to accommodate CPX tier maximum (200 A) without rewiring.**

### Auxiliary Load Schedule

| Circuit | Voltage | Load | Continuous (kW) | Peak (kW) |
|---------|---------|------|-----------------|-----------|
| AUX-1 | 480 V AC 3-ph | Munters DSS Pro (external) | 25 | 35 |
| Life-safety | 24 V DC | See §5 | 0.31 | 0.36 |

---

## §7  CONDUCTOR SIZING — AC MAIN FEED

### ECP to AC Main Disconnect

At 3,300 kW installed capacity, the AC main feed operates at high current levels requiring bus duct or parallel cable runs. Individual conductor selection per phase:

| Parameter | Value | Calculation |
|-----------|-------|-------------|
| Installed capacity | 3,300 kW | 5 × 660 kW |
| AC efficiency factor (98%) | AC draw: ~3,367 kW | 3,300 ÷ 0.98 |
| Operating current per phase (PF = 0.95) | **4,179 A** | 3,367,000 ÷ (√3 × 480 × 0.95) |
| NEC 125% continuous factor | **5,224 A** | 4,179 × 1.25 |
| AC main disconnect required | **6,000 A** | Next standard above 5,224 A |
| Main feed conductor | Bus duct rated 6,000 A, or parallel cable banks | See §19 E-01 for ECP connector selection |

**Note:** At 4,179 A per phase, the ECP AC connection requires bus duct or a multi-connector parallel bank. Standard Cam-Lok E1016 connectors (400 A each) would require 11 per phase — impractical. ECP high-current AC connector selection is open item E-01.

---

## §8  CONDUCTOR SIZING — PER DELTA RACK AC FEEDER

Each Delta 660 kW in-row rack receives an individual 480 V AC 3-phase feeder from the AC main disconnect.

| Parameter | Value | Calculation |
|-----------|-------|-------------|
| Power per rack | 660 kW output | Delta nameplate |
| AC draw per rack (PF = 0.95, 98% eff) | ~673 kW | 660 ÷ 0.98 |
| Operating current per phase | **836 A** | 673,000 ÷ (√3 × 480 × 0.95) |
| NEC 125% factor (continuous) | **1,045 A** | 836 × 1.25 |
| Per-rack AC feeder breaker | **1,200 A** | Next standard above 1,045 A |
| Conductor (per phase) | 2× 300 mm² XHHW-2 in parallel | |
| Ampacity per 300 mm² @ 90°C, in tray | ~600 A | NEC Table 310.15(B)(16) |
| Parallel ampacity | 1,200 A | 2 × 600 A |
| NEC 80% on conductor | 960 A continuous allowed per conductor | |
| Utilization | 69.7% | 836 ÷ (2 × 600) |
| Status | **COMPLIANT ✓** | |
| Run length | ~3–6 m (AC main disconnect to rack position) | |
| Per-rack cable set | 2× 3-ph (3× 300 mm² per run) + G (1× 95 mm²) | 5 identical sets for 5 racks — 3-wire + ground, no neutral (Delta racks are 3-phase delta, no neutral required). 95 mm² EGC exceeds NEC 250.122 minimum for 1,200 A OCPD (3/0 AWG = 85 mm²). |

---

## §9  CONDUCTOR SIZING — 800 V DC INTERNAL BUS

### Delta Rack Output Connection to Busway

Each Delta rack connects its 800 V DC output to the internal DC busway via a laminated copper bus stub.

| Parameter | Value | Calculation |
|-----------|-------|-------------|
| DC output per rack | 660 kW / 825 A | 660,000 ÷ 800 V |
| NEC 125% (continuous) | **1,031 A** | 825 × 1.25 |
| Bus stub per rack | 100×10 mm laminated copper (99.9% Cu) per polarity | |
| Bus stub cross-section | 1,000 mm² | 100 × 10 |
| Ampacity (bare copper, ventilated) | ~3,200 A | Per IPC-2152 |
| Utilization per rack | 25.8% | 825 ÷ 3,200 |
| Status | **COMPLIANT ✓** | |

### Internal DC Busway (Aggregate)

| Parameter | Value | Calculation |
|-----------|-------|-------------|
| Total DC installed capacity | 3,300 kW | 5 × 660 kW |
| Total DC bus current (installed basis) | **4,125 A** | 3,300,000 ÷ 800 V |
| NEC 80% continuous busway rule | **5,156 A minimum** | 4,125 ÷ 0.80 |
| **Specified internal DC busway** | **6,000 A, 800 V DC rated** | Next standard above 5,156 A |
| Utilization | 68.75% | 4,125 ÷ 6,000 |
| Status | **COMPLIANT ✓** | |

---

## §10  CONDUCTOR SIZING — DC BRANCH CIRCUITS (PER RACK)

### Compute Racks R1–R9 (120 kW NVL72 / 160 kW NVL144 CPX — sized to CPX maximum)

| Parameter | Value | Calculation |
|-----------|-------|-------------|
| Rack IT load — NVL72 | 120 kW | NVIDIA published |
| Rack IT load — NVL144 CPX (sizing basis) | 160 kW | NVIDIA published — maximum rated |
| Operating current — NVL72 | 150 A | 120,000 ÷ 800 V |
| Operating current — CPX (sizing basis) | 200 A | 160,000 ÷ 800 V |
| NEC 125% factor (continuous, CPX basis) | 250 A | 200 × 1.25 |
| Selected conductor | 95 mm² (≈ 3/0 AWG) XHHW-2, 2 kV rated, one per polarity | |
| Conductor ampacity @ 90°C, in tray | 300 A | NEC Table 310.15(B)(16) |
| NEC 80% continuous on conductor | 240 A allowed | 300 × 0.80 |
| Utilization — NVL72 (150 A) | 50.0% | 150 ÷ 300 |
| Utilization — CPX (200 A) | 66.7% | 200 ÷ 300 |
| 250 A < 300 A | **COMPLIANT ✓** | |
| Branch breaker | 250 A frame / 250 A trip — 800 V DC rated | Full frame rating; accommodates NVL72 and CPX without conductor change |
| Run length | ~2 m (busway tap to rack DC/DC shelf) | |

### R10 Control Rack (IB / Mgmt — 25 kW)

| Parameter | R10 |
|-----------|-----|
| Operating current | 31 A |
| Conductor utilization | 11.7% |
| Breaker trip vs load | 6.5× margin |
| Status | Oversized but correct ✓ — simplifies spare inventory |

---

## §11  CONDUCTOR SIZING — AUXILIARY & LIFE-SAFETY

### AUX-1: Munters DSS Pro Power Feed (480 V AC 3-ph, 80 A)

| Parameter | Value |
|-----------|-------|
| Munters DSS Pro running draw | ~25 kW (spec TBD pending vendor call) |
| Operating current (25 kW, PF = 0.85) | 35.4 A |
| NEC 125% | 44 A |
| IEC 60309 connector at ECP | 80 A — adequate ✓ |
| Conductor (ECP to skid, ~10 m) | 4× 16 mm² |
| 16 mm² ampacity @ 90°C | 68 A — adequate for 44 A ✓ |

### Life-Safety 24 V DC Distribution

| Parameter | Value |
|-----------|-------|
| Continuous load | 306 W |
| Operating current at 24 V | 12.8 A |
| Selected conductor | 2.5 mm² for all life-safety drops |
| Ampacity 2.5 mm² | 27 A @ 60°C ✓ |
| Max run length (farthest load from UPS) | ~12 m (VESDA at far end) |
| Voltage drop at 12 m, 12.8 A, 2.5 mm² | 0.21 V (0.88%) — acceptable for 24 V system ✓ |

---

## §12  VOLTAGE DROP ANALYSIS

### 800 V DC Branch Circuits (Most Critical: R9 — Farthest Compute Rack)

Copper resistivity at 90°C: ρ = 0.0217 Ω·mm²/m

| Segment | Length | Conductor | Current | V-drop | % drop |
|---------|--------|-----------|---------|--------|--------|
| Delta rack stub to busway | 0.6 m | 1,000 mm² bus | 825 A | 0.013 V | 0.002% |
| Busway (DR1 output → B-09 tap) | ~10 m | 6,000 A busway | 1,381 A | ~0.73 V | 0.09% |
| Branch cable (B-09 → R9 DC/DC) | 2 m | 95 mm² | 150 A | 0.14 V | 0.017% |
| **Total — worst case (R9)** | | | | **0.88 V** | **0.11%** |

**0.11% voltage drop to the farthest compute rack is negligible.** Delta DC/DC shelves accept 800 V DC ± 5% (760–840 V). Actual delivery: 800 − 0.88 = 799.1 V — well within range ✓.

### 24 V DC Life-Safety (Most Critical: VESDA, ~12 m from UPS)

| Segment | Length | Conductor | Current | V-drop | % drop |
|---------|--------|-----------|---------|--------|--------|
| UPS → VESDA panel (~12 m) | 12 m | 2.5 mm² | 1.5 A | 0.31 V | 1.3% |
| **Result** | | | | 23.7 V at VESDA | Within VESDA range (18–30 V) ✓ |

---

## §13  PROTECTIVE DEVICE COORDINATION

### Hierarchy — Primary AC Input

```
TIER 1 (upstream, platform side):
  Platform main disconnect / generator or BESS protection
  Fault interrupt: per platform engineering
  Clearing time: < 50 ms

TIER 2 (AC main disconnect, ELEC end):
  480 V AC 3-ph main disconnect, 6,000 A, motor-operated
  Fault interrupt: per manufacturer rating
  Clearing time: < 100 ms on E-stop
```

### Hierarchy — 800 V DC Internal

```
TIER 1 (Delta rack output protection):
  Built-in electronic protection per Delta rack
  Each rack's internal e-fuse (SiC switch) — fault cutoff < 3 microseconds

TIER 2 (DC branch breakers B-01 through B-10):
  250 A frame / 250 A trip MCCB (R1–R9) / 200 A trip (R10), 800 V DC rated
  Fault interrupt: see §15
  Clearing time: < 20 ms on branch fault
```

**Selective coordination requirement:** Branch breaker B-xx must clear before any Delta rack internal protection operates for a fault limited to one rack. Delta SiC e-fuse response (< 3 µs) is upstream protection; branch MCCB clears branch faults before reaching the Delta rack output.

### Key Coordination Requirement — 800 V DC Breakers

**Standard molded-case circuit breakers (MCCBs) are commonly rated to 500–750 V DC.** Operation at 800 V DC requires specific DC-listed products. DC arc extinction is harder than AC (no current zero crossing), requiring longer contact gaps.

**Verified 800 V DC rated products for branch application (200 A):**
- ABB SACE Tmax XT4 — DC version: 800 V DC listed, available in 200 A. ICU at 800 V DC: 25 kA.
- Schneider Electric EasyPact CVS250B — requires DC kit; verify 800 V rating.
- Eaton Series C — confirm 800 V DC listing.

**Action E-04:** Obtain specific 800 V DC test certificates for selected branch breaker before procurement.

---

## §14  DC BUSWAY SIZING

### Installed Capacity Basis

NEC 384.15(B): continuous loads on a busway shall not exceed 80% of the busway ampere rating. All sizing is based on installed capacity — 3,300 kW, 5 × Delta 660 kW racks operating simultaneously.

| Parameter | Value | Calculation |
|-----------|-------|-------------|
| Installed DC capacity | 3,300 kW | 5 × 660 kW |
| DC bus current (installed basis) | 4,125 A | 3,300,000 ÷ 800 V |
| NEC 80% minimum busway rating | **5,156 A** | 4,125 ÷ 0.80 |
| **Specified busway** | **6,000 A, 800 V DC rated** | Next standard above 5,156 A |
| Utilization at installed capacity | 68.8% | 4,125 ÷ 6,000 |
| Status | **COMPLIANT ✓** | |

### Busway Selection

Starline Track Busway (6,000 A DC), Siemens SIVACON 8PS, or Schneider Canalis KS. Confirm 800 V DC listing and IP54 minimum on selected product. See BOM-001 §9.

---

## §15  FAULT CURRENT ANALYSIS

### DC Fault Characteristics

Unlike AC systems, DC short-circuit current does not naturally cross zero. DC circuit breakers and fuses must force current zero by creating a sufficient arc voltage. Delta in-row racks include SiC e-fuse modules (fault cutoff < 3 microseconds) as first-level protection on the DC bus.

### Available Fault Current at DC Busway

The Delta rack embedded BBU (480 kW per rack, 600 A per rack at 800 V DC) contributes to available fault current independently of AC input availability.

**Conservative bolted fault estimate at branch breaker input:**

- 5 Delta racks × 600 A BBU contribution = 3,000 A BBU source
- Delta rack internal impedance (estimated): ~0.05 Ω per rack
- Busway impedance: ~0.04 mΩ/m × 12 m = 0.48 mΩ

For stiff Delta rack source:
- Available fault current at busway: limited by Delta internal protection (SiC e-fuse cuts at < 3 µs)
- Prospective fault current before e-fuse: ~15–25 kA estimated
- ABB XT4 DC at 25 kA ICU is adequate; confirm with Delta actual source impedance documentation.

**Action E-07:** Obtain Delta 660 kW rack prospective fault current specification and e-fuse coordination data.

### Ungrounded IT System — First Fault Behavior

With the Bender IMD (iso-PV1685) monitoring the 800 V DC internal bus:
- **First ground fault:** Current path does not complete through ground. Fault current is near zero. IMD detects insulation resistance drop and alarms. System continues operating.
- **Second ground fault (different polarity):** Creates a full fault path. Branch or Delta rack protection must clear.
- **IMD response:** Trips system if insulation resistance < 1 kΩ. Prevents second fault from developing.

---

## §16  GROUNDING & BONDING ARCHITECTURE

### Single-Point Ground (SPG) — ELEC End

All grounding in the Cassette converges to **one** point: the single-point ground bar at the ELEC end (INT-001 §17).

```
  PLATFORM SPG ─── 50 mm² bond cable, ≤ 10 m ─── CASSETTE ECP GROUND STUD
                                                         │
                                              SPG BAR (Burndy, ELEC end)
                                                         │
              │
         25 mm² braid
         ×10 compute/control racks
              │
         RACK CHASSIS (frame bond)
              │
         DELTA RACK CHASSIS (frame bond — each of 5 power racks)
              │
         LOAD SPREADER PLATE ─── weld to container ─── CONTAINER FRAME
              │
         CABLE TRAY BONDS (at every section splice)
              │
         ACCESS PANEL BONDS (conductive EMI gasket + interior jumper)
              │
         ECP HOUSING BONDS (×2, one per ECP cover)
```

### AC System Neutral and Ground

The 480 V AC primary system neutral is bonded to the SPG bar at one point only (at the AC main disconnect). AC equipment grounds for the Delta racks bond to the SPG bar via rack chassis bond cables. **The AC neutral is not bonded downstream of the main disconnect.**

### What Is NOT Connected to the SPG

The 800 V DC bus is **floating** (ungrounded IT system). The + and − conductors of the 800 V DC bus have no intentional connection to the SPG bar. The Bender IMD measures impedance from each DC pole to ground and alarms if it falls below 5 kΩ.

**Never bond the 800 V DC bus + or − to the SPG bar, container frame, or AC neutral.** Doing so converts the IT system to a grounded system and eliminates first-fault current-limiting protection.

### Bond Resistance Target

Cassette frame to platform SPG: ≤ 1 Ω measured (ECP-001 §15). Verified at commissioning and annually.

### Offshore Bonding Additions

Per INT-001 §24 and §17: all bolted seams receive bonding jumpers for RFI suppression and cathodic protection coordination. Minimum 24 jumpers per Cassette.

---

## §17  UNGROUNDED IT SYSTEM (IMD) ARCHITECTURE

### Why Ungrounded DC

The 800 V DC internal bus operates as an **IT (Isolated Terra / Ungrounded) system** per IEC 61557-8 and OCP Stage 1d architecture:
- High-voltage DC at 800 V (above touch voltage limits)
- High-availability compute (first fault does not trip the system)
- Marine/offshore environments (no reference to sea ground potential)

### Bender iso-PV1685 IMD

| Parameter | Value |
|-----------|-------|
| Product | Bender iso-PV1685 |
| Application | Ungrounded DC up to 1,500 V |
| Measurement principle | AC injection method (frequency-selective) |
| Alarm threshold | Insulation resistance < 5 kΩ (configurable) |
| Trip threshold | Insulation resistance < 1 kΩ |
| Response time | < 30 seconds to alarm |
| Output | Modbus RTU → BMS (Jetson Orin) |
| Location | ELEC end zone, adjacent to DC busway |

### IMD Response Logic (BMS)

```
IMD reading > 50 kΩ         → Normal operation, log at 1 Hz
IMD reading 5–50 kΩ         → Warning: alert BMS, log at 10 Hz, notify SCADA
IMD reading < 5 kΩ          → Alarm: notify SCADA, dispatch technician
IMD reading < 1 kΩ          → Trip: isolate DC bus, E-stop platform
IMD: loss of measurement     → Fault: treat as alarm condition
```

### Coordination with Platform IMD

If the platform also monitors a DC IT system, IMD signals must be coordinated per IEC 61557-8. See open item E-06.

---

## §18  ENGINEERING ANALYSIS NOTES

Summary of key findings and decisions that drove the final specifications.

| Item | Initial | Final | Reason |
|------|---------|-------|--------|
| Primary cassette input | 800 V DC from platform | **480 V AC 3-ph from platform** | Delta 660 kW in-row racks take 480 V AC in, output 800 V DC internally. AC→DC conversion occurs inside the cassette, not at the platform. |
| DC busway | 4,000 A | **6,000 A, 800 V DC** | Installed capacity = 3,300 kW = 4,125 A at 800 V DC. NEC 80% requires 5,156 A minimum. 6,000 A is next standard. Infrastructure sized to installed capacity, not GPU operating load. |
| AC main disconnect | Not present (DC primary) | **6,000 A, 480 V AC 3-ph** | 3,300 kW at 480 V 3-ph = 4,179 A per phase. NEC 125% = 5,224 A. 6,000 A is next standard. |
| Per Delta rack feeder | Not present | **1,200 A, 480 V AC 3-ph** | 660 kW per rack = 836 A per phase (PF 0.95, 98% eff). NEC 125% = 1,045 A. 1,200 A breaker. |
| Per rack AC conductor | Not present | **2× 300 mm² per phase** | 836 A operating; single 300 mm² insufficient (600 A ampacity). 2 in parallel = 1,200 A capacity. |
| Compute UPS | Separate UPS required | **Eliminated — Delta BBU** | Each Delta rack has 480 kW embedded BBU (no inverter, no separate room). 5 racks = 2,400 kW total embedded backup. |
| Stäubli CombiTac 2500 DC connector | Specified at ELEC ECP | **Removed** | 800 V DC no longer enters at ECP. DC bus is internal only. ECP is now AC. |
| ECP primary connector | Stäubli CombiTac 2500 (DC) | **High-current AC — see E-01** | 4,179 A per phase at 480 V AC requires bus duct or custom connector bank. Standard Cam-Lok insufficient. |
| DC branch conductor (R1–R9) | 2× 70 mm² per polarity, 200 A trip | **2× 95 mm² per polarity, 250 A trip** | 2× 70 mm² at NVL72 (150 A) leaves only 6% margin at NVL144 CPX (200 A vs 212 A NEC 80% limit). Sealed unmanned pod cannot be rewired in field. Sized to CPX tier maximum to eliminate rewiring constraint. Consistent with installed-capacity sizing philosophy applied to all upstream equipment. |
| OCP row power compliance | Not assessed | **COMPLIANT ✓** | OCP Next-Generation ML Infrastructure Design Principles v0.5.0 requires ≥ 1 MW per row (2026 tier) and ≥ 2.4 MW per row (2028+ tier). Cassette facility load: 1,145 kW (NVL72) to 1,526 kW (CPX). A single Cassette meets the 2026 minimum. Multiple Cassettes per row (where applicable) scale proportionally. 2028+ 2.4 MW minimum requires two CPX-tier Cassettes per row or platform-level aggregation. |

---

## §19  OPEN ITEMS

| ID | Item | Priority | Blocks |
|----|------|----------|--------|
| E-01 | Specify ECP high-current 480 V AC 3-ph connector for 4,179 A per phase — evaluate bus duct coupling, Anderson SB series, or parallel Cam-Lok bank. Coordinate with platform distribution design. | P-0 | ECP fabrication, AC main feed |
| E-02 | Confirm AC main disconnect product: 6,000 A, 480 V AC 3-ph, motor-operated, UL listed. Evaluate Eaton Magnum DS, Siemens WL, ABB Emax2. | P-0 | AC main disconnect procurement |
| E-03 | *Withdrawn — see Rev 1.0 decision ledger.* | — | — |
| E-04 | Obtain 800 V DC test certificates for branch breakers (250 A frame / 250 A trip, ≥ 25 kA ICU at 800 V DC) before procurement. Confirm Delta fault current data per E-07 before releasing PO. | P-0 | Branch circuit compliance |
| E-05 | *Withdrawn — see Rev 1.0 decision ledger.* | — | — |
| E-06 | IMD coordination with platform: confirm IT system boundary and IMD signal coordination per IEC 61557-8. | P-1 | Commissioning |
| E-07 | Obtain Delta 660 kW rack prospective fault current specification and SiC e-fuse coordination data for branch breaker selection confirmation. | P-1 | Fault current analysis |

---

**Cassette — Electrical Single-Line Diagram & Distribution Specification**
**Cassette-ELEC-001 · Rev 1.2 · 2026-04-22**
**Scott Tomsu · scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana**
**CONFIDENTIAL**
