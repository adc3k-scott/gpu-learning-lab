# Cassette — ELECTRICAL SINGLE-LINE DIAGRAM & DISTRIBUTION SPECIFICATION

**Document:** Cassette-ELEC-001
**Revision:** 1.0
**Date:** 2026-04-19
**Classification:** CONFIDENTIAL
**Companion to:** Cassette-INT-001 Rev 1.0 · Cassette-ECP-001 Rev 1.0 · Cassette-BOM-001 Rev 1.0

**Purpose:** Complete electrical engineering specification for one Cassette. Defines all power distribution circuits, conductor sizing, protective device ratings, grounding architecture, and auxiliary power systems. Serves as the fabricator-ready electrical specification and the basis for permit drawings.

| Rev | Date       | Description                                           |
|-----|------------|-------------------------------------------------------|
| 1.0 | 2026-04-19 | Initial release                                       |

**Prepared by:** Scott Tomsu · CEO / Chief Engineer
scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana

---

## TABLE OF CONTENTS

- §1  Electrical System Overview
- §2  One-Line Diagram — Primary 800 V DC
- §3  One-Line Diagram — 415 V AC Alternate Path
- §4  One-Line Diagram — 480 V AC Auxiliary Circuits
- §5  One-Line Diagram — 24 V DC Life-Safety Bus
- §6  Load Schedule
- §7  Conductor Sizing — Main DC Feed
- §8  Conductor Sizing — DC Branch Circuits (Per Rack)
- §9  Conductor Sizing — AC Alternate Path
- §10 Conductor Sizing — Auxiliary & Life-Safety
- §11 Voltage Drop Analysis
- §12 Protective Device Coordination
- §13 DC Busway Sizing & Upgrade Path
- §14 Fault Current Analysis
- §15 Grounding & Bonding Architecture
- §16 Ungrounded IT System (IMD) Architecture
- §17 BOM Discrepancies & Corrections
- §18 Open Items

---

## §1  ELECTRICAL SYSTEM OVERVIEW

### Four Independent Power Systems

The Cassette contains four electrically separate power systems. They share a common grounding reference but are otherwise independent.

| System | Voltage | Source | Loads | ECP Entry |
|--------|---------|--------|-------|-----------|
| Primary DC | 800 V DC, ungrounded | Platform (Bloom / Cat / grid-tie) | 15 compute racks (Delta shelves) | ELEC ECP — Stäubli CombiTac 2500 |
| AC Alternate | 415 V AC 3-ph | Platform (transformer secondary) | Same 15 racks (Delta shelf AC input) | ELEC ECP — Cam-Lok E1016 |
| Auxiliary AC | 480 V AC 3-ph | Platform | CDU + Munters HCD-600 | CDU ECP — IEC 60309 pin-and-sleeve |
| Life-Safety DC | 24 V DC | Internal UPS (LiFePO4 2 kWh) | BMS, fire panel, sensors, lighting | Self-contained (no ECP) |

**Only one of Primary DC or AC Alternate is active at any time.** Selection is made at commissioning. The unused ECP connectors are capped with rated weather covers. The Auxiliary AC and Life-Safety DC are always live when the Cassette is deployed.

### Key Electrical Parameters

| Parameter | Value | Basis |
|-----------|-------|-------|
| Primary input voltage | 800 V DC ± 5% (760–840 V DC) | ECP-001 §5 |
| System grounding | Ungrounded IT per IEC 61557-8 | INT-001 §8 / §16 |
| Design operating current (NVL72) | 1,981 A | 1,585 kW ÷ 800 V |
| Design operating current (NVL144 CPX) | 2,631 A | 2,105 kW ÷ 800 V |
| NEC 80% continuous busway rule (NVL72) | Minimum busway: 2,476 A | See §13 |
| NEC 80% continuous busway rule (NVL144 CPX) | Minimum busway: 3,289 A | See §13 — **drives busway upgrade** |
| Fault current withstand at ECP | 50 kA for 100 ms | ECP-001 §5 |
| Primary operating frequency | DC (no frequency) | — |
| Auxiliary AC voltage | 480 V AC 3-ph, 60 Hz | INT-001 §8 |
| Life-safety DC voltage | 24 V DC nominal | INT-001 §23 |

---

## §2  ONE-LINE DIAGRAM — PRIMARY 800 V DC

```
═══════════════════════════════════════════════════════════════════════
  ELEC ECP (CASSETTE BOUNDARY — PLATFORM SIDE LEFT, POD SIDE RIGHT)
═══════════════════════════════════════════════════════════════════════

  PLATFORM SIDE                        POD SIDE
  ─────────────                        ─────────
  800 V DC +  ──[STÄUBLI COMBICTAC 2500]──────────────────────────────
  800 V DC −  ──[STÄUBLI COMBICTAC 2500]──────────────────────────────
                   2,500 A blind-mate,                │         │
                   IP67, polarity keyed               │         │
                                                      │         │
                          [COPPER BUS STUB — 100×10 mm laminated, 600 mm]
                                                      │         │
                          ┌───────────────────────────┘         │
                          │  [SPD — Phoenix Contact Type 1       │
                          │         200 kA, shunt connected]     │
                          │                                      │
                 ┌────────┴─────────────────────────────────────┤
                 │  BENDER iso-PV1685 IMD                        │
                 │  Ungrounded IT monitoring                     │
                 │  Alarm: < 5 kΩ insulation resistance         │
                 └────────┬─────────────────────────────────────┘
                          │         │
                 ┌────────┴─────────┴────────────┐
                 │  REVENUE METER                 │
                 │  ANSI C12.20, 0.5% class       │
                 │  800 V DC rated                │
                 └────────┬──────────────────────-┘
                          │         │
                 ┌────────┴─────────┴────────────┐
                 │  800 V DC MAIN DISCONNECT      │
                 │  2,500 A, motor-operated       │
                 │  UL 98 listed, padlockable     │
                 │  Trip coil: E-stop hardwired   │
                 └────────┬──────────────────────-┘
                          │         │
                          │         │
         ┌────────────────┴─────────┴─────────────────────────────┐
         │        800 V DC BUSWAY — 2,500 A* — ~15 m run           │
         │        *See §13: recommend upgrade to 4,000 A           │
         └───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┘
             │   │   │   │   │   │   │   │   │   │   │   │   │   │   │
            B01 B02 B03 B04 B05 B06 B07 B08 B09 B10 B11 B12 B13 B14 B15
         250A/200A trip MCCB (×15) — 800 V DC rated — See §12
             │   │   │   │   │   │   │   │   │   │   │   │   │   │   │
            R1  R2  R3  R4  R5  R6  R7  R8  R9 R10 R11 R12 R13 R14 R15
         2×70mm² branch cable, ~2 m each (see §8)
         │                                                             │
         ▼                                                             ▼
    ┌──────────┐                                               ┌──────────┐
    │ COMPUTE  │  ×13 (R1–R13)                                 │ IB/MGMT  │ (R14/R15)
    │ NVL72    │                                               │ ~25 kW   │
    │ 120 kW   │                                               │ each     │
    │ per rack │                                               └──────────┘
    ├──────────┤
    │ Delta    │ 110 kW Power Shelf (4U) — rectifies 800 V DC → internal bus
    │ Delta    │ 800V→50V DC/DC Shelf (2U) — final conversion
    │ Delta    │ 33 kW Redundant Shelf (2U) — N+1
    └──────────┘

═══════════════════════════════════════════════════════════════════════
  GROUNDING: Single-point ground bar at ELEC end, bonded to container
  frame. NOT connected to 800 V DC bus (IT system). Bond cable from
  ECP ground stud (#9) to platform SPG via 50 mm² conductor at ECP.
═══════════════════════════════════════════════════════════════════════
```

---

## §3  ONE-LINE DIAGRAM — 415 V AC ALTERNATE PATH

**This path is present at the ELEC ECP on every Cassette. It is activated only when the platform cannot supply 800 V DC.** The DC and AC paths are mutually exclusive — never energize both simultaneously. The 800 V DC Stäubli connectors are capped when the AC path is active.

```
═══════════════════════════════════════════════════════════════════════
  ELEC ECP — 415 V AC ALTERNATE INPUT
═══════════════════════════════════════════════════════════════════════

  PLATFORM SIDE                        POD SIDE
  ─────────────                        ─────────
  L1  ──[CAM-LOK E1016 L1]────────────────────────────────────────────
  L2  ──[CAM-LOK E1016 L2]────────────────────────────────────────────
  L3  ──[CAM-LOK E1016 L3]────────────────────────────────────────────
  N   ──[CAM-LOK E1016 N ]────────────────────────────────────────────
  G   ──[CAM-LOK E1016 G ]────────────────────────────────────────────
           400 A, IP67                      │  │  │  │  │
                                            │  │  │  │  │
                               ┌────────────┴──┴──┴──┴──┴──────────┐
                               │  AC MAIN DISCONNECT — E-01         │
                               │  415 V AC 3-ph, 3,200 A            │
                               │  E-01 NOT IN CURRENT BOM — ADD     │
                               └────────────┬──┬──┬────────────────-┘
                                            │  │  │
                               ┌────────────┴──┴──┴──────────────────┐
                               │  415 V AC BUSWAY OR HOME-RUN CABLES  │
                               │  3-ph, 3,200 A minimum               │
                               │  NOT IN CURRENT BOM — ADD            │
                               └────┬───┬───┬───┬───┬───┬────────────┘
                                    │   │   │   │   │   │   ...×15
                                  [ACB1–ACB15: per-rack AC breakers]
                                    │   │   │   │   │   │
                                   R1  R2  R3  ...         R15
                               ┌──────────────────────────────────────┐
                               │ Delta 110 kW shelf — AC INPUT MODE   │
                               │ 415 V AC 3-ph → internal DC bus      │
                               └──────────────────────────────────────┘

```

**Design gaps — AC path (not defined in INT-001 or BOM):**
- AC main disconnect not specified
- AC busway or home-run cable specification not defined
- Per-rack AC branch breaker ratings not specified
- See §17 (BOM Discrepancies) and §18 (Open Items — E-01, E-02)

---

## §4  ONE-LINE DIAGRAM — 480 V AC AUXILIARY CIRCUITS

Two separate auxiliary AC feeds enter the Cassette at the **CDU ECP** (not ELEC ECP). These are independent of the primary compute power.

```
═══════════════════════════════════════════════════════════════════════
  CDU ECP — 480 V AC AUXILIARY INPUTS
═══════════════════════════════════════════════════════════════════════

  PLATFORM SIDE                     POD SIDE
  ─────────────                     ─────────

  CIRCUIT AUX-1 — CDU POWER
  480 V AC 3-ph ──[IEC 60309, 60 A]──────────────────────────────────
                    Pin-and-sleeve,
                    IP67                       │
                                    ┌──────────┴───────────────────┐
                                    │  CDU POWER SUBPANEL           │
                                    │  480 V AC 3-ph, 60 A          │
                                    │  Eaton / Siemens              │
                                    │  Location: CDU end zone       │
                                    └──────────┬───────────────────-┘
                                               │
                                    ┌──────────┴───────────────────┐
                                    │  CoolIT CHx2000 CDU          │
                                    │  480 V AC 3-ph               │
                                    │  ~40–55 kW (pumps + controls) │
                                    └──────────────────────────────-┘

  CIRCUIT AUX-2 — MUNTERS POWER
  480 V AC 3-ph ──[IEC 60309, 80 A]──────────────────────────────────
                    Pin-and-sleeve,
                    IP67                       │
                                    ┌──────────┴───────────────────┐
                                    │  MUNTERS HCD-600 POWER FEED   │
                                    │  480 V AC 3-ph, 80 A          │
                                    │  Direct to external skid      │
                                    │  via CDU ECP M12 connector    │
                                    └──────────┬───────────────────-┘
                                               │
                                    ┌──────────┴───────────────────┐
                                    │  Munters HCD-600 (external)   │
                                    │  480 V AC, ~30 kW running     │
                                    └──────────────────────────────-┘

═══════════════════════════════════════════════════════════════════════
  NOTE: AUX-1 and AUX-2 are platform responsibility up to CDU ECP.
  Pod side terminates at subpanel (AUX-1) or skid connector (AUX-2).
═══════════════════════════════════════════════════════════════════════
```

---

## §5  ONE-LINE DIAGRAM — 24 V DC LIFE-SAFETY BUS

Self-contained. No ECP penetration. Charges from the 800 V DC primary (via integral charger in UPS). Maintains life-safety loads for ≥ 2 hours on loss of primary.

```
═══════════════════════════════════════════════════════════════════════
  24 V DC LIFE-SAFETY BUS — INTERNAL ONLY
═══════════════════════════════════════════════════════════════════════

             [800 V DC PRIMARY BUS]
                       │
              ┌────────┴────────────────────┐
              │  MAINTENANCE UPS             │
              │  24 V DC / 2 kWh LiFePO4    │
              │  Integral charger            │
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
═══════════════════════════════════════════════════════════════════════
```

---

## §6  LOAD SCHEDULE

### Primary 800 V DC Load Schedule (NVL72 Tier)

| Circuit | Rack | Load Type | IT Load (kW) | Current (A) | Breaker | Conductor |
|---------|------|-----------|--------------|-------------|---------|-----------|
| B-01 | R1 | Compute NVL72 | 120 | 150 | 250A/200A | 2× 70 mm² |
| B-02 | R2 | Compute NVL72 | 120 | 150 | 250A/200A | 2× 70 mm² |
| B-03 | R3 | Compute NVL72 | 120 | 150 | 250A/200A | 2× 70 mm² |
| B-04 | R4 | Compute NVL72 | 120 | 150 | 250A/200A | 2× 70 mm² |
| B-05 | R5 | Compute NVL72 | 120 | 150 | 250A/200A | 2× 70 mm² |
| B-06 | R6 | Compute NVL72 | 120 | 150 | 250A/200A | 2× 70 mm² |
| B-07 | R7 | Compute NVL72 | 120 | 150 | 250A/200A | 2× 70 mm² |
| B-08 | R8 | Compute NVL72 | 120 | 150 | 250A/200A | 2× 70 mm² |
| B-09 | R9 | Compute NVL72 | 120 | 150 | 250A/200A | 2× 70 mm² |
| B-10 | R10 | Compute NVL72 | 120 | 150 | 250A/200A | 2× 70 mm² |
| B-11 | R11 | Compute NVL72 | 120 | 150 | 250A/200A | 2× 70 mm² |
| B-12 | R12 | Compute NVL72 | 120 | 150 | 250A/200A | 2× 70 mm² |
| B-13 | R13 | Compute NVL72 | 120 | 150 | 250A/200A | 2× 70 mm² |
| B-14 | R14 | InfiniBand switches | 15 | 19 | 250A/200A | 2× 70 mm² |
| B-15 | R15 | Storage + mgmt | 10 | 13 | 250A/200A | 2× 70 mm² |
| **TOTAL** | | | **1,585** | **1,981** | Main: 2,500A disc | Bus stub |

**NVL144 CPX upgrade path** (field upgrade, no circuit changes except busway — see §13):

| Config | IT Load (kW) | Bus Current (A) | Busway at 80% NEC |
|--------|-------------|-----------------|-------------------|
| NVL72 tier (current) | 1,585 | 1,981 | Need ≥ 2,476 A busway |
| NVL144 CPX upgrade | 2,105 | 2,631 | Need ≥ 3,289 A busway |

### Auxiliary Load Schedule

| Circuit | Voltage | Load | Continuous (kW) | Peak (kW) |
|---------|---------|------|-----------------|-----------|
| AUX-1 | 480 V AC 3-ph | CoolIT CHx2000 CDU | 40 | 55 |
| AUX-2 | 480 V AC 3-ph | Munters HCD-600 (external) | 30 | 40 |
| Life-safety | 24 V DC | See §5 | 0.31 | 0.36 |

---

## §7  CONDUCTOR SIZING — MAIN DC FEED

### ECP Connection to Main Disconnect (~600 mm service loop)

The Stäubli CombiTac 2500 connector terminates into a **laminated copper bus bar assembly**, not an individual cable. Individual cable is inappropriate for this current level at this connection point.

| Parameter | Value | Calculation |
|-----------|-------|-------------|
| Operating current | 1,981 A | 1,585 kW ÷ 800 V |
| NEC 125% factor (continuous) | 2,476 A | 1,981 × 1.25 |
| Selected bus bar | 100 mm × 10 mm copper (99.9% Cu) per polarity | Standard laminated bus section |
| Bus bar cross-section | 1,000 mm² | 100 × 10 |
| Ampacity (bare copper, ventilated, 30°C ambient) | ~3,200 A | Per IPC-2152 / IEEE Std 738 |
| Utilization | 61.8% | 1,981 ÷ 3,200 |
| Voltage drop (600 mm, 90°C Cu) | 0.014 V | 1,981 × 0.0217/1,000 × 0.6 × 2 |
| Status | **COMPLIANT ✓** | |

**BOM Correction:** BOM §15 lists "800 V DC primary, 2× 70 mm² XHHW-2, ~10 m" for the main feed. 70 mm² is rated 265 A per conductor — completely insufficient for 1,981 A. The main ECP stub must be laminated copper bus bar as specified above. See §17.

---

## §8  CONDUCTOR SIZING — DC BRANCH CIRCUITS (PER RACK)

### Compute Racks R1–R13 (120 kW each)

| Parameter | Value | Calculation |
|-----------|-------|-------------|
| Rack IT load | 120 kW | NVIDIA published, Oberon NVL72 |
| Operating current | 150 A | 120,000 ÷ 800 V |
| NEC 125% factor (continuous) | 187.5 A | 150 × 1.25 |
| Selected conductor | 70 mm² (≈ 2/0 AWG) XHHW-2, 2 kV rated | One per polarity |
| Conductor ampacity @ 90°C, in tray | 265 A | NEC Table 310.15(B)(16) |
| Utilization | 56.6% | 150 ÷ 265 |
| NEC 80% continuous rule on conductor | 212 A allowed | 265 × 0.80 |
| 187.5 A < 212 A | **COMPLIANT ✓** | |
| Branch breaker | 250 A frame / 200 A trip | |
| 200 A ≥ 187.5 A (NEC 125% minimum) | **COMPLIANT ✓** | |
| Conductor 265 A > 200 A breaker | **COMPLIANT ✓** | Cable can handle breaker fault let-through |
| Run length | ~2 m (busway tap to rack Delta shelf) | |

### R14 InfiniBand (15 kW) and R15 Storage/Mgmt (10 kW)

Both R14 and R15 are assigned the same 250A/200A breaker and 2× 70 mm² conductor as compute racks. This is conservative by ~8× for the actual load but simplifies spare inventory and commissioning. This is the correct engineering decision.

| Parameter | R14 | R15 |
|-----------|-----|-----|
| Operating current | 19 A | 13 A |
| Conductor utilization | 7.2% | 4.9% |
| Breaker trip vs load | 10.5× margin | 15× margin |
| Status | Oversized but correct ✓ | Oversized but correct ✓ |

---

## §9  CONDUCTOR SIZING — 415 V AC ALTERNATE PATH

The AC alternate path is architecturally incomplete. This section specifies what is required if the AC path is built out. See §18 open item E-01.

### Per-Rack AC Branch (415 V AC 3-phase)

| Parameter | Value | Calculation |
|-----------|-------|-------------|
| Rack IT load | 120 kW | Same rack, Delta shelf AC input mode |
| Operating current (3-phase balanced, PF = 0.95) | 175 A | 120,000 ÷ (√3 × 415 × 0.95) |
| NEC 125% factor (continuous) | 219 A | 175 × 1.25 |
| Required conductor ampacity | ≥ 219 A | |
| Selected conductor | 95 mm² (≈ 3/0 AWG) XHHW-2, per phase | |
| 95 mm² ampacity @ 90°C, in tray | 285 A | NEC Table 310.15(B)(16) |
| Utilization | 61.4% | 175 ÷ 285 |
| Status | **COMPLIANT ✓** | |

**BOM Correction:** BOM §4 lists "4× 35 mm² per-rack AC input cable." 35 mm² (≈ 2 AWG) is rated 130 A per conductor — insufficient for 175 A operating current and 219 A NEC-required ampacity. Correct cable is 3× 95 mm² + N (50 mm²) + G (25 mm²) per rack. See §17.

### AC Main Feed (ECP to AC Main Disconnect)

| Parameter | Value | Calculation |
|-----------|-------|-------------|
| Total 3-phase operating current (NVL72, all racks) | 2,276 A | 1,585,000 ÷ (√3 × 415 × 0.95) |
| NEC 125% | 2,845 A per phase | |
| AC main disconnect required | 3,200 A | Next standard size above 2,845 A |
| AC busway or parallel cables | 3,200 A 3-phase rated | Not currently in BOM |

---

## §10  CONDUCTOR SIZING — AUXILIARY & LIFE-SAFETY

### AUX-1: CDU Power Feed (480 V AC 3-ph, 60 A)

| Parameter | Value |
|-----------|-------|
| CoolIT CDU power draw | 40 kW continuous, 55 kW peak |
| Operating current (40 kW, PF = 0.90) | 53.7 A |
| NEC 125% | 67 A |
| IEC 60309 connector at ECP | 60 A — **undersized for NEC 125% requirement** |
| **Correction:** Use 80 A IEC 60309 connector | 80 A rated, same as Munters feed |
| Conductor (CDU ECP to CDU subpanel, ~3 m) | 3× 10 mm² + G (6 mm²) XHHW-2 |
| 10 mm² ampacity @ 90°C | 40 A per phase (in conduit) — insufficient |
| **Correction:** 3× 25 mm² + G (16 mm²) | 100 A ampacity ✓ |
| See §18 open item E-03 | Confirm CDU actual draw with CoolIT RFQ |

### AUX-2: Munters Power Feed (480 V AC 3-ph, 80 A)

| Parameter | Value |
|-----------|-------|
| Munters HCD-600 running draw | ~30 kW |
| Operating current (30 kW, PF = 0.85) | 42.5 A |
| NEC 125% | 53 A |
| IEC 60309 connector at ECP | 80 A — adequate ✓ |
| Conductor (ECP to skid, ~10 m per BOM) | 4× 16 mm² per BOM |
| 16 mm² ampacity @ 90°C | 68 A — adequate for 53 A ✓ |

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

## §11  VOLTAGE DROP ANALYSIS

### 800 V DC Branch Circuits (Most Critical: R1 — Farthest from ELEC end is R13)

Copper resistivity at 90°C: ρ = 0.0217 Ω·mm²/m

| Segment | Length | Conductor | Current | Resistance | V-drop | % drop |
|---------|--------|-----------|---------|------------|--------|--------|
| Bus stub (ECP → main disc) | 0.6 m | 1,000 mm² bus | 1,981 A | 0.000013 Ω | 0.026 V | 0.003% |
| Busway (main disc → B-13 tap) | 13.2 m | 2,500 A busway | 1,981 A | ~0.00053 Ω* | 1.05 V | 0.13% |
| Branch cable (B-13 → R13 shelf) | 2 m | 70 mm² | 150 A | 0.00124 Ω | 0.19 V | 0.023% |
| **Total — worst case (R13)** | | | | | **1.27 V** | **0.16%** |

*Busway resistance per manufacturer spec; ~0.04 mΩ/m for 2,500 A copper busway.

**0.16% voltage drop to the farthest rack is negligible.** Delta 110 kW shelves accept 800 V DC ± 5% (760–840 V). Actual delivery to R13 shelf at full load: 800 − 1.27 = 798.7 V → well within range ✓.

### 24 V DC Life-Safety (Most Critical: VESDA, ~12 m from UPS)

| Segment | Length | Conductor | Current | V-drop | % drop |
|---------|--------|-----------|---------|--------|--------|
| UPS → VESDA panel (~12 m) | 12 m | 2.5 mm² | 1.5 A | 0.31 V | 1.3% |
| **Result** | | | | 23.7 V at VESDA | Within VESDA operating range (18–30 V) ✓ |

---

## §12  PROTECTIVE DEVICE COORDINATION

### Hierarchy — Primary 800 V DC

```
TIER 1 (upstream, platform side):
  Platform main disconnect / BESS protection
  Fault interrupt: 50 kA
  Clearing time: < 50 ms (before pod main opens)

TIER 2 (pod main disconnect, ELEC end):
  800 V DC main disconnect, motor-operated, 2,500 A
  Fault interrupt: 50 kA for 100 ms (ECP-001 §5)
  Clearing time: < 100 ms on E-stop or IMD trip

TIER 3 (branch breakers B-01 through B-15):
  250 A frame / 200 A trip MCCB, 800 V DC rated
  Fault interrupt: see §14
  Clearing time: < 20 ms on branch fault
```

**Selective coordination requirement:** Branch breaker B-xx must clear before Tier 2 main opens, for any fault limited to one rack. This requires:
- Branch breaker interrupting time < main disconnect minimum clearing time
- Time-current curves must be verified for non-overlapping trip zones

### Key Coordination Requirement — 800 V DC Breakers

**Standard molded-case circuit breakers (MCCBs) are commonly rated to 500–750 V DC.** Operation at 800 V DC requires specific DC-listed products. DC arc extinction is harder than AC (no current zero crossing), requiring longer contact gaps.

**Verified 800 V DC rated products for branch application (200 A):**
- ABB SACE Tmax XT4 — DC version: 800 V DC listed, available in 200 A. ICU at 800 V DC: 25 kA. Confirm with ABB if 25 kA is adequate for fault current at busway tap (see §14).
- Schneider Electric EasyPact CVS250B — requires DC kit; verify 800 V rating.
- Eaton Series C — confirm 800 V DC listing.

**Action E-04:** Obtain specific 800 V DC test certificates for selected branch breaker before procurement. Do not assume standard AC breaker is DC-rated.

---

## §13  DC BUSWAY SIZING & UPGRADE PATH

### NEC 80% Continuous Load Rule

NEC 384.15(B): continuous loads on a busway shall not exceed 80% of the busway ampere rating.

| Tier | IT Load | Bus Current | Minimum Busway (÷ 0.80) | BOM Spec | Status |
|------|---------|-------------|------------------------|----------|--------|
| NVL72 | 1,585 kW | 1,981 A | **2,476 A** | 2,500 A | **Compliant — 24 A margin** |
| NVL144 CPX | 2,105 kW | 2,631 A | **3,289 A** | 2,500 A | **NON-COMPLIANT — 789 A short** |

### Finding: 2,500 A Busway Cannot Support CPX Upgrade

The BOM and INT-001 both state 2,500 A busway. This is just barely compliant for NVL72 tier (24 A margin — essentially zero). For the NVL144 CPX field upgrade path, the busway must be replaced.

Busway replacement inside a sealed, operational cassette is highly disruptive: the primary DC bus must be de-energized, all 15 branch breakers removed, the busway sections unbolted from the manifold floor trench, and new busway installed. This is a multi-day outage of the entire cassette.

### Recommendation: Install 4,000 A Busway from Build

| Busway | NVL72 Utilization | NVL144 CPX Utilization | Enables CPX Upgrade? | Relative Cost |
|--------|-------------------|------------------------|----------------------|---------------|
| 2,500 A (current BOM) | 79.2% (marginal) | Non-compliant | No | Baseline |
| 3,000 A | 66% | 87.7% (marginal) | No (marginal) | ~+20% |
| **4,000 A** | **49.5%** | **65.8%** | **Yes ✓** | **~+45%** |

**Recommendation: Replace BOM 2,500 A busway with 4,000 A busway.** The incremental cost of busway upgrade at build vs. a cassette outage for busway replacement in the field is not close. The upgrade path is a core design objective.

**Action E-05:** Update BOM §9 — change DC busway from 2,500 A to 4,000 A, 800 V DC rated. Vendors: Starline Track Busway (4000 A DC available), Siemens SIVACON 8PS, Schneider Canalis KS.

---

## §14  FAULT CURRENT ANALYSIS

### DC Fault Characteristics

Unlike AC systems, DC short-circuit current does not naturally cross zero. DC circuit breakers and fuses must force current zero by creating a sufficient arc voltage. This makes DC fault interruption harder at high voltages and high currents.

### Available Fault Current at ECP

Per ECP-001 §5: the Cassette main disconnect must withstand 50 kA for 100 ms. Platform-side fault current capacity determines available short-circuit current at the pod ECP. Platform engineering must provide the prospective short-circuit current (PSC) at the 800 V DC output.

**Pod-side calculation approach (conservative, bolted fault):**

At the DC busway tap points (branch breaker inputs), the available fault current is limited by:
1. Upstream source impedance (platform BESS or genset inverter — typically 5–15% internal impedance)
2. Busway impedance (~0.04 mΩ/m × 15 m = 0.6 mΩ)
3. Bus stub impedance (negligible, ~0.013 mΩ)

For a 800 V DC, 2 MW source with 10% internal impedance:
- Source impedance: 0.10 × (800²) / (2,000,000) = 0.032 Ω
- Bolted fault current: 800 / (0.032 + 0.0006) = **24.4 kA**

For a stiffer source with 5% impedance: 48.8 kA — approaching the 50 kA ECP rating.

**Conclusion:** The 50 kA rating on the main disconnect is appropriately sized for stiff DC sources. Branch breakers at busway taps see attenuated fault current due to busway impedance. ABB XT4 DC at 25 kA ICU is likely adequate, but must be confirmed against actual platform source impedance.

### Ungrounded IT System — First Fault Behavior

With the Bender IMD (iso-PV1685) monitoring the ungrounded DC bus:
- **First ground fault:** Current path does not complete through ground. Fault current is near zero. IMD detects insulation resistance drop and alarms. System continues operating.
- **Second ground fault (different polarity):** Creates a full fault path. Main disconnect must clear. This is the design scenario for the 50 kA withstand rating.
- **IMD response:** Trips main disconnect if insulation resistance < 5 kΩ on either pole. Prevents second fault from developing while first fault is present.

This is the safety advantage of the ungrounded IT system — single fault tolerance without system shutdown.

---

## §15  GROUNDING & BONDING ARCHITECTURE

### Single-Point Ground (SPG) — ELEC End

All grounding in the Cassette converges to **one** point: the single-point ground bar at the ELEC end (INT-001 §18). This prevents ground loops which generate ground potential differences across the rack cluster, corrupting high-speed I/O and causing DC offset in power supplies.

```
  PLATFORM SPG ─── 50 mm² bond cable, ≤ 10 m ─── CASSETTE ECP GROUND STUD
                                                         │
                                              SPG BAR (Burndy, ELEC end)
                                                         │
              ┌──────────────────────────────────────────┴──────────────────────────┐
              │                                                                       │
         25 mm² braid                                                          35 mm² cable
         ×15 racks                                                             CDU chassis
              │                                                                       │
         RACK CHASSIS                                                       COOLIT CHx2000
         (frame bond)                                                       CHASSIS BOND
              │
         LOAD SPREADER PLATE ─── weld to container ─── CONTAINER FRAME
              │
         CABLE TRAY BONDS (at every section splice)
              │
         ACCESS PANEL BONDS (conductiveEMI gasket + interior jumper per panel)
              │
         ECP HOUSING BONDS (×2, one per ECP cover)
```

### What Is NOT Connected to the SPG

The 800 V DC bus is **floating** (ungrounded IT system). The + and − conductors of the 800 V DC system have no intentional connection to the SPG bar. The Bender IMD measures the impedance from each DC pole to ground and alarms if it falls below 5 kΩ. This is the intended architecture.

**Never bond the 800 V DC bus + or − to the SPG bar or container frame.** Doing so converts the IT system to a grounded system and eliminates first-fault current-limiting protection.

### Bond Resistance Target

Cassette frame to platform SPG: ≤ 1 Ω measured (ECP-001 §15).
Verified at commissioning and annually. See ECP-001 §19.

### Offshore Bonding Additions

Per INT-001 §25 and §18: all bolted seams receive bonding jumpers for RFI suppression and cathodic protection coordination. Minimum 24 jumpers per Cassette (12 access panels + 2 ECP covers + 4 corner casting plates + structural seams).

---

## §16  UNGROUNDED IT SYSTEM (IMD) ARCHITECTURE

### Why Ungrounded DC

The 800 V DC bus operates as an **IT (Isolated Terra / Ungrounded) system** per IEC 61557-8 and OCP Stage 1d architecture. This is the correct architecture for:
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
| Trip threshold | Insulation resistance < 1 kΩ (trips main disconnect) |
| Response time | < 30 seconds to alarm |
| Output | Modbus RTU → BMS (Jetson Orin) |
| Location | ELEC end zone, adjacent to main disconnect |

### IMD Response Logic (BMS)

```
IMD reading > 50 kΩ         → Normal operation, log at 1 Hz
IMD reading 5–50 kΩ         → Warning: alert BMS, log at 10 Hz, notify SCADA
IMD reading < 5 kΩ          → Alarm: notify SCADA, dispatch technician
IMD reading < 1 kΩ          → Trip: open main disconnect, E-stop platform
IMD: loss of measurement     → Fault: treat as alarm condition
```

### Coordination with Platform IMD

If the platform also operates an IT system on the same 800 V DC bus, the platform and pod IMDs must be coordinated to avoid false alarms from injected test signals interfering with each other. IEC 61557-8 requires coordination when multiple IMDs monitor the same isolated system. This is a platform-pod integration task — see open item E-06.

---

## §17  BOM DISCREPANCIES & CORRECTIONS

The following items in BOM Rev 1.0 require correction based on this electrical analysis:

| Item | BOM Rev 1.0 | Corrected Spec | Impact |
|------|-------------|----------------|--------|
| DC busway (§9) | 2,500 A | **4,000 A, 800 V DC** | Enables CPX upgrade path |
| 800 V DC main cable (§15) | 2× 70 mm² XHHW-2 | **100×10 mm laminated copper bus bar per polarity** | 70 mm² is rated 265 A — cannot carry 1,981 A |
| Per-rack AC cable (§4, alternate) | 4× 35 mm² | **3× 95 mm² + N (50 mm²) + G (25 mm²)** | 35 mm² is insufficient for 175 A per phase |
| CDU power connector (§14 ECP) | IEC 60309, 60 A | **IEC 60309, 80 A** | CDU at 40 kW / 480V 3-ph requires up to 67 A — 60 A connector is undersized |
| CDU power feed cable (§15) | 4× 10 mm² | **3× 25 mm² + G (16 mm²)** | 10 mm² = 40 A; need 67 A |

**BOM Rev 2.0 required to incorporate above corrections.**

---

## §18  OPEN ITEMS

| ID | Item | Priority | Blocks |
|----|------|----------|--------|
| E-01 | Define AC main disconnect, AC busway, and per-rack AC breaker for 415 V AC alternate path — currently unspecified in INT-001 and BOM | P-1 | AC path fabrication |
| E-02 | Confirm Delta 110 kW shelf 800 V DC vs 415 V AC input selection at commissioning (C-02 from README) | P-0 | Input path selection |
| E-03 | Confirm CoolIT CHx2000 actual 480 V AC power draw (kW and A) with CoolIT RFQ | P-1 | AUX-1 connector sizing |
| E-04 | Obtain 800 V DC test certificates for selected branch breaker (250 A, ≥ 25 kA ICU at 800 V DC) | P-0 | Branch circuit compliance |
| E-05 | Update BOM §9: change DC busway from 2,500 A to 4,000 A | P-1 | CPX upgrade path |
| E-06 | IMD coordination with platform: confirm IT system boundary and IMD signal coordination per IEC 61557-8 | P-1 | Commissioning |
| E-07 | Obtain actual platform PSC (prospective short-circuit current) at 800 V DC ECP output | P-1 | Fault current analysis |

---

**Cassette — Electrical Single-Line Diagram & Distribution Specification**
**Cassette-ELEC-001 · Rev 1.0 · 2026-04-19**
**Scott Tomsu · scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana**
**CONFIDENTIAL**
