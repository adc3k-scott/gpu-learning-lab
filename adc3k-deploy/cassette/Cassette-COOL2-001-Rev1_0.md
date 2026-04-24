# Cassette — EXTERNAL CDU SKID SPECIFICATION

**Document:** Cassette-COOL2-001
**Revision:** 1.0
**Date:** 2026-04-22
**Classification:** CONFIDENTIAL
**Companion to:** Cassette-INT-001 · Cassette-ECP-001 · Cassette-BOM-001 · Cassette-COOL-001 · Cassette-ELEC-001

**Purpose:** Complete specification for the external Coolant Distribution Unit (CDU) skid that serves one Cassette. The CDU skid circulates the primary PG25 loop, rejects heat from the primary loop to a platform-provided intermediate loop via a liquid-to-liquid plate heat exchanger, and maintains loop pressure, flow, and makeup. Covers skid architecture, heat exchanger sizing, pump selection, expansion and makeup, flexible hose interconnect, intermediate loop interface, skid structure, controls, electrical, and commissioning. One skid is procured per Cassette.

The CDU skid is the hydraulic counterpart to the Cassette. It takes what the Cassette guarantees at the QBH-150 QD face (COOL-001) and delivers PG25 back into the Cassette at design supply temperature. The platform delivers intermediate cooling fluid (tower water, dry cooler loop, river water, or seawater) to the skid; the skid handles everything between those two interfaces.

**Prepared by:** Scott Tomsu · CEO / Chief Engineer
scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana

---

## TABLE OF CONTENTS

- §1  Scope
- §2  Skid Architecture & Process Flow Diagram
- §3  Heat Exchanger — Primary / Intermediate
- §4  Circulation Pumps — Primary PG25 Side
- §5  Expansion Tank & Makeup System
- §6  Flexible Hose Assemblies (Cassette ↔ Skid)
- §7  Intermediate Loop Interface (Platform Side)
- §8  Skid Frame, Drip Containment, Footprint
- §9  Controls & Instrumentation
- §10 Electrical Distribution
- §11 Commissioning — Skid Hydraulic + Thermal
- §12 Open Items

---

## §1  SCOPE

### What This Document Covers

- Plate heat exchanger (PG25 primary to intermediate loop)
- Circulation pumps on the primary PG25 side (duty + standby with VFDs)
- Expansion tank, pressurization, automatic makeup, and PG25 reservoir
- Flexible braided hose assemblies between Cassette QBH-150 QDs and skid DN150 inlets
- Skid-side primary PG25 piping, valves, strainers, and instrumentation
- Intermediate loop skid-side connection (flanged interface to platform fluid)
- Skid structural frame, drip containment, leveling feet / fork pockets
- Skid-local controls panel, HMI, VFD cabinet, BMS interface
- Skid primary electrical distribution (480 V AC 3-ph in, motor starters, control transformer, local disconnect)

### What This Document Does Not Cover

- Cassette primary PG25 internals — governed by **Cassette-COOL-001**
- Platform intermediate cooling plant (dry cooler banks, cooling tower, chilled water plant, river intake, seawater heat exchanger) — platform engineering responsibility, specified in site-specific installation package
- Platform-side intermediate loop pumps, piping, and instrumentation upstream of the skid flanged interface
- Cassette ELEC ECP 480 V AC primary — governed by **Cassette-ELEC-001**; skid electrical is a separate feed per ECP-001 §1
- Munters DSS Pro dehumidification skid — separate external skid, governed by INT-001 §15 and open item MO-03
- Site piping, conduit, trenching between skid and platform equipment — platform installation scope

### Interface Contract

The CDU skid is the partner half of two interfaces:

| Interface              | Document      | Skid Obligation                                                   | Cassette / Platform Obligation                                                |
|------------------------|---------------|-------------------------------------------------------------------|-------------------------------------------------------------------------------|
| Primary PG25           | COOL-001 §7   | Deliver 45 °C ±1 °C supply at 1,810 LPM (CPX) / 1,369 LPM (NVL72), ≥ 2.7 bar head above cassette return | Cassette accepts PG25 within its stated envelope (16 bar max, 25% glycol, chemistry per §9) |
| Intermediate loop      | §7 (this doc) | Accept intermediate fluid at flanged ANSI B16.5 Class 150 DN100 connections | Platform delivers intermediate fluid within stated temperature and flow envelope |

### Rule of Hydraulic Contract (Recap)

The CDU skid is **responsible for loop pressure, loop temperature, loop flow, and loop chemistry** at the QBH-150 QD face on the Cassette. The Cassette is a passive thermal load. The skid does not cross the QBH-150 QD face — everything upstream of that face is Cassette scope.

---

## §2  SKID ARCHITECTURE & PROCESS FLOW DIAGRAM

### Block Diagram

```
═══════════════════════════════════════════════════════════════════════════
  CDU SKID — PROCESS FLOW (ONE SKID PER CASSETTE)
═══════════════════════════════════════════════════════════════════════════

  CASSETTE SIDE                                       PLATFORM SIDE
  (via QBH-150 hoses)                                 (intermediate loop)
  ──────────────────                                  ────────────────────

  [QD-R] PG25 return  ──────[HOSE-R]──────► ┌─────────────────────────┐
  57 °C, 1,810 LPM                           │   SUCTION STRAINER       │
                                             │   (Y-type, 40 mesh)      │
                                             └────────────┬────────────┘
                                                          │
                                             ┌────────────┴────────────┐
                                             │   PUMP P1 (duty)         │
                                             │   15 kW VFD, 1,810 LPM   │
                                             │   @ 27 m head            │
                                             └────────────┬────────────┘
                                                          │
                                             ┌────────────┴────────────┐  ◄──┐
                                             │   PUMP P2 (standby)      │    │
                                             │   Same spec, auto-failover│    │
                                             └────────────┬────────────┘    │
                                                          │                 │
                                             ┌────────────┴────────────┐    │  parallel
                                             │   FLOW METER             │    │  isolation
                                             │   (mag / Coriolis)       │    │  valves
                                             └────────────┬────────────┘    │
                                                          │                 │
                     ┌────────────────────────────────────┤  ◄──────────────┘
                     │                                    │
               ┌─────┴─────┐                   ┌──────────┴────────────┐
               │ EXPANSION │                   │  PLATE HEAT EXCHANGER │◄── INT RETURN
               │ TANK      │                   │  PG25 side (primary)  │    42 °C
               │ 100 L     │                   │  1,465 kW duty        │    to platform
               │ 2.5 bar   │                   │  24 m² plate area     │    ~3,010 LPM (water)
               │ pre-charge│                   │  Alfa Laval M20 or eq │
               └─────┬─────┘                   │  Intermediate side    │◄── INT SUPPLY
                     │                         └──────────┬────────────┘    35 °C
                     │  (pressurization tap)              │                 from platform
                     │                                    │
                     │                         ┌──────────┴────────────┐
                     │                         │  PRIMARY SUPPLY T ctrl│
                     │                         │  RTD + VFD setpoint   │
                     │                         └──────────┬────────────┘
                     │                                    │
                     └────────────────────────────────────┤
                                                          │
                                                          ▼
  [QD-S] PG25 supply ◄─────[HOSE-S]────────────────────────
  45 °C, 1,810 LPM                                         
                                                          
           ┌─────────────┐
           │ MAKEUP SYS  │
           │ 200 L PG25  │
           │ storage     │───► (tees into loop low-pressure side)
           │ auto-fill   │
           │ pump        │
           └─────────────┘

═══════════════════════════════════════════════════════════════════════════
  SKID CONTROLS: PLC + VFD + HMI — commands pumps P1/P2, reads all T/P/F
  sensors, controls supply temperature to 45 °C ±1 °C by modulating
  pump speed and (optionally) intermediate loop bypass valve.
═══════════════════════════════════════════════════════════════════════════
```

### Flow Direction Convention

- **PG25 return (hot, 57 °C)** exits the Cassette at QBH-R and enters the skid
- Skid pumps draw hot PG25 through strainer and flow meter
- Pumps discharge into the HX primary-side inlet
- HX primary-side outlet returns PG25 at 45 °C
- Supply PG25 exits skid and enters Cassette at QBH-S
- Expansion tank tees into the low-pressure side (pump suction) for stable pressure reference
- Makeup system tees into the same low-pressure leg on loss-of-pressure signal

### Why Pump on Return (Hot) Side

- Pump draws suction from cassette return (hot) and discharges into HX
- Keeps the high-pressure side (discharge, 2.7 bar gauge) confined between pump discharge and HX inlet — shorter high-pressure run
- Pump seal sees 57 °C maximum, which is well within mechanical seal limits (150 °C typical)
- Pump NPSH available is maximized at suction to the cassette return (coolest point on return flow is the cassette exit; cavitation margin is preserved)

Alternative architecture (pump on cold side): rejected — puts the high-pressure discharge across the hoses and QBH-150 QDs, which would lift QBH-150 seat load at the face and push available working pressure closer to the 16 bar QD rating under transients.

---

## §3  HEAT EXCHANGER — PRIMARY / INTERMEDIATE

### Duty & Design Point

| Parameter                | CPX (sizing basis)   | NVL72 (nominal op)   | Units            |
|--------------------------|----------------------|----------------------|------------------|
| Heat duty                | 1,465                | 1,105                | kW               |
| Primary (PG25) inlet T   | 57                   | 55                   | °C               |
| Primary (PG25) outlet T  | 45                   | 45                   | °C               |
| Primary ΔT               | 12                   | 10                   | K                |
| Primary flow             | 1,810                | 1,369                | LPM              |
| Intermediate inlet T     | 35                   | 32                   | °C (baseline: dry cooler) |
| Intermediate outlet T    | 42                   | 38                   | °C               |
| Intermediate ΔT          | 7                    | 6                    | K                |
| Intermediate flow (water)| 3,010                | 2,635                | LPM              |
| LMTD (counter-flow)      | 12.3                 | 11.5                 | K                |
| Required UA              | 119                  | 96                   | kW/K             |

**Sizing basis:** plate HX sized for **CPX duty at 12.3 K LMTD, 119 kW/K UA.**

### Plate HX Specification

| Parameter                      | Value                                                |
|--------------------------------|------------------------------------------------------|
| HX type                        | Gasketed plate heat exchanger, single-pass counter-flow |
| Plate material                 | 316L stainless (0.5 mm thickness standard)           |
| Gasket material                | EPDM peroxide-cured (onshore) / FKM (offshore)       |
| Frame material                 | Carbon steel, painted (onshore) / 316L SS (offshore) |
| Port connections — primary     | DN150 flanged (ANSI B16.5 Class 150 RF)              |
| Port connections — intermediate| DN150 flanged (ANSI B16.5 Class 150 RF)              |
| Design pressure                | 16 bar both sides                                    |
| Design temperature             | 90 °C both sides                                     |
| Plate area (per CPX sizing)    | ~24 m² total plate area (U ≈ 5,000 W/m²·K baseline)  |
| Estimated plate count          | 80–100 plates (depends on vendor plate pattern)      |
| Primary-side Δp at design flow | 0.80 bar (target; vendor quote to confirm)           |
| Intermediate-side Δp at design flow | 0.50 bar (target)                               |
| Primary-side fouling allowance | 0.0001 m²·K/W (closed-loop PG25, low fouling)        |
| Intermediate-side fouling allowance | Depends on variant (see §7); water: 0.0002; tower water: 0.0004; river/sea: 0.0006 |
| Approach temperature           | 10 K cold end (design), 15 K hot end                 |

### Vendor Shortlist

| Vendor           | Model family      | Notes                                                    |
|------------------|-------------------|----------------------------------------------------------|
| Alfa Laval       | M20-BFG / MK15    | Industry standard for data-center warm-water duty        |
| Kelvion          | NT350M / NT500S   | Competitive; common in North America                     |
| Sondex           | S100 / S110       | Danfoss-owned; strong marine offerings                   |
| Tranter          | GX-91 / GC-109    | US-fabricated; shorter lead time                         |
| SWEP             | GL-series         | Brazed alternative; not recommended — no gasket service  |

**CX-02 open:** vendor selection and exact plate count pending RFQ to Alfa Laval, Kelvion, and Sondex. RFQ package includes the §3 design point, fouling allowances, and 10-year gasket service expectation.

### Plate Pack Service & Future-Proofing

Gasketed plate HX plate count can be increased in the field by loosening the frame tie-bolts and adding plates. The skid frame sizing (§8) reserves **20% frame length margin** to allow adding ~20 plates without replacing the HX — supports future CPX-Next tier if rack heat load rises above 200 kW/rack.

### Approach Temperature Sensitivity

The 10 K cold-end approach (intermediate 35 °C → primary supply 45 °C) is the design driver. Tightening approach below 10 K increases plate area rapidly (approach halved → area ~doubles). Widening approach above 15 K cuts plate area but forces the intermediate loop to a lower temperature — expensive on the platform side (requires chilled water or evaporative cooling).

**The 10 K approach is the sweet spot for NVIDIA warm-water architectures.** Platforms providing intermediate fluid above 35 °C (e.g., ambient dry cooler at 40 °C on a hot Louisiana day) will not meet the 45 °C primary supply. In such cases the Cassette operates with elevated supply temperature — NVL72 tolerates up to 50 °C supply for limited duration; CPX tolerance TBD per C-01.

---

## §4  CIRCULATION PUMPS — PRIMARY PG25 SIDE

### Head Budget (Total Dynamic Head at Design Flow)

| Component                             | Δp (bar) | Notes                                              |
|---------------------------------------|----------|----------------------------------------------------|
| Cassette internal (QD-to-QD)          | 0.55     | COOL-001 §5, R1 worst-case path                    |
| Rack internal (NVIDIA cold-plate loop) | 0.65    | NVL72 Oberon typical; confirm via NVIDIA (C-01)    |
| Flex hose — supply (5 m DN150 braided)| 0.03     | f ≈ 0.030, includes routing bends                  |
| Flex hose — return (5 m DN150 braided)| 0.03     | Same                                                |
| HX primary-side Δp                    | 0.80     | Vendor target (CX-02 to confirm)                   |
| Skid primary piping + strainer + valves | 0.40   | DN150 × ~8 m total; strainer 0.10 bar clean       |
| Pump suction/discharge + expansion-tee | 0.05    | —                                                  |
| Safety margin                         | 0.20     | —                                                  |
| **Total dynamic head (TDH)**          | **2.70** | = **27.0 m PG25 column** at ρ = 1,017 kg/m³        |

### Pump Sizing

| Parameter                          | Value                                          |
|------------------------------------|------------------------------------------------|
| Design flow per pump               | 1,810 LPM (108.6 m³/hr, 478 GPM)               |
| Design TDH                         | 27.0 m (88.6 ft)                               |
| Pump power (hydraulic)             | P_hyd = ρgHQ = 1017 × 9.81 × 27 × 0.0302 = **8.1 kW** |
| Pump efficiency at BEP             | 0.72 (typical for end-suction at this operating point) |
| Shaft power                        | 8.1 / 0.72 = 11.3 kW                           |
| Motor efficiency (IE3)             | 0.93                                           |
| Motor input power                  | 11.3 / 0.93 = 12.1 kW                          |
| **Selected motor size**            | **15 kW (20 hp)** — next standard above 12.1 kW |
| Operating current (480 V AC 3-ph, PF 0.88) | 15,000 / (√3 × 480 × 0.88) = 20.5 A    |
| NEC 125% (continuous)              | 25.6 A                                         |
| Branch breaker per pump            | 30 A, 480 V AC 3-ph                            |

### Redundancy & Control

**N+1 configuration:** 2 pumps installed in parallel, each sized for 100% design flow. Duty (P1) + standby (P2), auto-failover on duty pump fault. Pumps alternate as duty every 2,000 hours to equalize wear.

**VFD control:** both pumps on individual variable frequency drives (VFDs). Primary control signal is supply-temperature setpoint feedback. If intermediate fluid temperature allows, pump speed drops to maintain 45 °C supply at reduced flow — this is the primary energy-saving mode at part-load (NVL72 operating below CPX rating).

**Minimum flow protection:** VFD holds minimum ~600 LPM (33% of rated) to prevent pump dead-head. Below 600 LPM, supply temperature control is handed off to intermediate-side bypass valve (CX-04 pending).

### Vendor Shortlist

| Vendor                       | Model family                | Notes                                     |
|------------------------------|-----------------------------|-------------------------------------------|
| Grundfos                     | NB / NBE end-suction        | Industry reference; good service network  |
| Xylem (Bell & Gossett)       | e-1510 / e-80               | North America standard; strong warranty   |
| Armstrong                    | 4380 / 4030                 | Energy-saver ECM motor option             |
| Wilo                         | IL / BL series              | European market; fewer US service points  |
| KSB                          | Etanorm / Etabloc           | Strong offshore/marine track record       |

**CX-03 open:** pump vendor selection pending head/flow curves, seal options (single vs double mechanical), and spare parts availability.

### Seal, Materials, Accessories

| Parameter                   | Onshore                           | Offshore                                    |
|-----------------------------|-----------------------------------|---------------------------------------------|
| Casing material             | Cast iron, painted                | Bronze or 316L SS                            |
| Impeller                    | Bronze                            | 316L SS                                      |
| Shaft                       | 316 SS                            | 316 SS                                       |
| Mechanical seal             | Single Buna-N / SiC / carbon     | Double cartridge seal, 316 SS / SiC / carbon, water-flush |
| Mounting                    | Close-coupled or long-coupled     | Long-coupled with seismic base              |
| Coupling guard              | OSHA-compliant steel              | 316 SS                                       |
| Vibration isolator          | Rubber-in-shear (Mason Industries) | Spring + snubber (Mason Industries)         |

---

## §5  EXPANSION TANK & MAKEUP SYSTEM

### Loop Volume

| Section                         | Volume (L)   |
|---------------------------------|--------------|
| Cassette interior (COOL-001 §5) | 180          |
| Skid primary piping + HX        | 50           |
| Supply flex hose (DN150, 5 m)   | 93           |
| Return flex hose (DN150, 5 m)   | 93           |
| **Total system volume**         | **416**      |

### Thermal Expansion

- Fill temperature (cold): 20 °C
- Operating temperature (warm-average): 50 °C
- PG25 volumetric expansion coefficient at 50 °C: β ≈ 0.00055 /K
- Expansion volume: ΔV = V × β × ΔT = 416 × 0.00055 × 30 = **6.9 L** (nominal)
- Peak excursion (50 °C fill → 65 °C transient upset): ΔT = 45 K, ΔV = 10.3 L

### Expansion Tank Sizing

| Parameter                     | Value                                                 |
|-------------------------------|-------------------------------------------------------|
| Type                          | Pre-charged bladder tank (EPDM bladder, 316 SS tank shell) |
| Nominal volume                | 100 L                                                 |
| Acceptance volume             | ≥ 25 L (covers 10.3 L peak excursion × 2.4× margin)   |
| Pre-charge pressure           | 2.5 bar at 20 °C                                      |
| Operating pressure at skid    | 3.0–3.5 bar at 50 °C (loop hot, bladder compressed)   |
| Maximum pressure              | 10 bar (tank rating; loop working 10 bar)             |
| Connection                    | DN50 flanged or 1½" NPT, 316 SS, to pump suction leg  |

### Vendor Shortlist

| Vendor              | Model                        | Notes                                |
|---------------------|------------------------------|--------------------------------------|
| Amtrol              | ST-42V / Extrol 100          | US market leader                     |
| Flexcon             | PL-100                       | Commercial HVAC standard             |
| Spirotech           | B100/10                      | European; cassette-compatible        |
| Armstrong           | AX series                    | Made in Canada; bundled with pumps   |

### Makeup System

Automatic makeup prevents slow loss of PG25 (from micro-leaks, sampling, evaporation during chemistry audit) from drawing the loop below minimum pressure. Not sized to handle active leaks — active leaks trigger MIV-S / MIV-R closure on the Cassette side per COOL-001 §8 and BMS alarm escalation.

| Component                     | Spec                                                 |
|-------------------------------|------------------------------------------------------|
| PG25 storage tank             | 200 L, polyethylene, UN-rated, vented with desiccant filter |
| Storage tank cap              | Gasketed with anti-siphon air break                  |
| Makeup pump                   | Positive-displacement metering pump, ~2 LPM capacity (Grundfos DDI or Seepex MD) |
| Makeup pump motor             | 0.5 kW, 120 V AC single-phase                        |
| Solenoid fill valve           | Normally closed, 24 V DC; opens on BMS command       |
| Pressure switch               | 2.0 bar low-low trigger for makeup command           |
| Makeup flow totalizer         | Tracks fill events; alarm if > 5 L added in 30 days (indicates slow leak) |
| Back-flow prevention          | Double check valve (per ASSE 1024)                   |
| Manual fill port              | 1" NPT with cap; for initial charging                |
| Level sensor (storage tank)   | Ultrasonic, reports level to BMS                     |

---

## §6  FLEXIBLE HOSE ASSEMBLIES (CASSETTE ↔ SKID)

### Hose Specification

Per BOM-001 §5.5, supplied with the Cassette and installed on site. Hydraulic detail here.

| Parameter                       | Value                                              |
|---------------------------------|----------------------------------------------------|
| Quantity                        | 2 (one supply, one return)                         |
| Length (each)                   | 5 m                                                |
| Nominal size                    | DN150 (6")                                         |
| Construction                    | 304 SS braid over EPDM or FEP inner tube           |
| Working pressure                | 16 bar                                             |
| Burst pressure                  | 64 bar (4× working)                                |
| Temperature range               | −20 °C to +120 °C                                  |
| End fitting — Cassette side     | QBH-150 male half (mates Cassette QBH-150 female QD plate) |
| End fitting — Skid side         | ANSI B16.5 Class 150 RF flange, 316L SS, matching skid inlet |
| Bend radius (minimum)           | 750 mm                                              |
| Insulation                      | 25 mm Aeroflex EPDM closed-cell foam, UV-jacketed  |
| Vendor                          | Parker ParFlex 797TC or Gates Mega4000             |

### Hose Δp Analysis

At 1,810 LPM (design flow, CPX basis):

| Parameter                   | Value                                          |
|-----------------------------|------------------------------------------------|
| Inside diameter (approx)    | 150 mm (matches DN150 nominal)                 |
| Flow area                   | 0.01767 m²                                     |
| Velocity                    | 1.71 m/s                                       |
| Reynolds number             | 275,000                                        |
| Friction factor (braided hose) | f ≈ 0.030 (higher than smooth pipe; braid-induced turbulence) |
| Friction Δp (5 m, per hose) | f × (L/D) × ρ × V²/2 = 0.030 × 33.3 × 1017 × 1.46 = **1,486 Pa = 0.015 bar** |
| Routing bend losses (2× 90°)| K = 0.8 total: 0.8 × 1017 × 1.46/2 = 744 Pa = 0.007 bar |
| End fitting Δp              | ≈ 0.005 bar                                    |
| **Per-hose Δp (total)**     | **0.027 bar**                                  |
| **Both hoses (supply + return)** | **0.054 bar ≈ 0.05 bar**                  |

### Installation & Service

- Hoses supported at midspan by overhead cable tray or dedicated hose bridle (no ground-lay permitted — foot traffic risk)
- Minimum 1 m straight run from QBH-150 face before any bend (to avoid face-loading the QD seat)
- Drip pan underneath the full hose run (100 mm deep SS trough) routed to the skid drip containment (§8)
- Visual inspection tag on each hose: installation date, last pressure test date, next service date (replace every 7 years or on inspection failure)
- IR thermography annual — confirm no hot spots indicating braid wear or inner-tube defect

### Offshore Additions

| Item                             | Onshore             | Offshore                                    |
|----------------------------------|---------------------|---------------------------------------------|
| Hose outer jacket                | 304 SS braid        | 316 SS braid or Monel braid                 |
| Hose inner tube                  | EPDM                | FEP (PTFE) for higher chemical resistance   |
| Flange bolts at skid end         | Stainless (18-8)    | Monel or Inconel, anti-galling compound     |
| Hose identification              | Printed tag         | Etched stainless tag, seawater-resistant    |

---

## §7  INTERMEDIATE LOOP INTERFACE (PLATFORM SIDE)

### Skid-Side Connection

| Parameter                        | Value                                                |
|----------------------------------|------------------------------------------------------|
| Connection type                  | ANSI B16.5 Class 150 RF flange, DN150                |
| Flange material                  | 304L SS (onshore) / 316L SS (offshore)               |
| Gasket                           | EPDM / spiral-wound graphite for higher temperature  |
| Location on skid                 | One inlet + one outlet, opposite face from Cassette-side hoses |
| Isolation                        | Manual butterfly valves, DN150, lever-operated, on both supply and return (skid side) |
| Strainer                         | Duplex Y-strainer on intermediate inlet (40 mesh stainless, blowdown-capable) |
| Test port                        | ½" NPT with cap, on each flange (for pressure/temperature survey) |

### Intermediate Fluid Variants

The skid HX plate material (316L SS baseline) is compatible with the below intermediate fluids without substitution. For aggressive fluids (seawater, brackish river water), plate upgrade is required (CX-01).

| Variant             | Fluid             | Supply T (°C) | Return T (°C) | Flow (LPM) | HX Plate Material | Notes                           |
|---------------------|-------------------|---------------|---------------|------------|-------------------|---------------------------------|
| A (baseline)        | 30% PG dry-cooler loop | 35        | 42            | 3,330      | 316L SS           | Most common; warm-water AI standard |
| B (tower water)     | Open condenser water | 30          | 35            | 4,220      | 316L SS (with biocide) | Cooling tower; higher flow, lower ΔT |
| C (once-through river) | Fresh river water | 15–25     | 25–35         | 2,100–3,500 | 316L SS with duplex plate option | Foulant control required (CX-01) |
| D (seawater, offshore) | Filtered seawater | 5–30       | 12–37         | 2,500–3,500 | Titanium Gr.1 (required) | Marine corrosion; plate upgrade mandatory |
| E (closed chilled water) | Facility CHW loop | 10    | 16            | 3,600      | 316L SS           | Not recommended — overdelivers cooling; wasteful |

**Baseline for Lafayette onshore Cassette deployment: Variant A (dry-cooler loop).** Matches the Gulf Coast climate profile: 35 °C intermediate supply is achievable year-round with a dry cooler bank sized to ASHRAE 2% summer design (Lafayette 2% dry-bulb ≈ 34 °C).

### Platform-Side Requirements

The platform must deliver the intermediate fluid at the specified temperature, flow, and chemistry at the skid flanged interface. Skid does not pump the intermediate fluid — intermediate circulation is platform scope.

| Platform Obligation                       | Specification                                       |
|-------------------------------------------|-----------------------------------------------------|
| Intermediate supply temperature           | 35 °C ±2 °C (Variant A) — or per variant table     |
| Intermediate flow                         | ≥ 3,330 LPM (Variant A) — or per variant table     |
| Intermediate Δp available at skid flange  | ≥ 0.8 bar (covers HX intermediate-side Δp plus skid piping) |
| Intermediate fluid chemistry              | Variant-dependent; per §7 table note below          |
| Backflow protection                       | Intermediate pumps to include NRV between skid and platform header |
| Isolation                                 | Platform provides lockable isolation valves on each branch |

**Intermediate fluid chemistry note:** for Variants A (30% PG closed loop) and B (tower water), platform is responsible for maintaining fluid chemistry per ASHRAE Guideline 3. The skid provides no chemistry treatment for the intermediate side. For Variants C/D, platform must provide pre-filtration and (for C) biological/chlorination control upstream of the skid strainer.

### Variant Selection Mechanism

Selection of intermediate variant drives:
- HX plate material (316L SS vs titanium)
- HX approach temperature and plate count
- Intermediate-side connection flange rating and materials
- Skid-side strainer mesh and maintenance frequency
- Commissioning test media

**CX-01 open:** variant selection per specific Cassette deployment; default to Variant A for the Lafayette onshore baseline. Offshore Cassette deployments default to Variant D (titanium HX, mandatory).

---

## §8  SKID FRAME, DRIP CONTAINMENT, FOOTPRINT

### Footprint

| Parameter                | Value                                                     |
|--------------------------|-----------------------------------------------------------|
| Overall length           | 3,500 mm                                                  |
| Overall width            | 2,000 mm                                                  |
| Overall height           | 2,200 mm (with expansion tank vertical; makeup tank at side) |
| Operating weight (wet)   | ~5,800 kg (with full PG25 and intermediate fluid in HX)   |
| Shipping weight (dry)    | ~4,400 kg                                                 |
| Total shipping volume    | ~15.4 m³                                                  |
| Frame reservation (§3 future-proof) | +400 mm length margin reserved for HX plate addition |

### Frame Construction

| Item                        | Onshore                             | Offshore                                         |
|-----------------------------|-------------------------------------|--------------------------------------------------|
| Main structural members     | HSS 6×6×¼" (150×150×6 mm) carbon steel, painted | HSS 6×6×¼" 316L SS or carbon steel with marine epoxy + GalvaZinc primer |
| Cross members               | HSS 4×4×¼" (100×100×6 mm)          | Same                                             |
| Deck plate                  | 3 mm steel chequered plate, painted | 3 mm 316L SS chequered plate                     |
| Leveling feet               | 4 × HD adjustable feet, 10,000 kg each | Same, with 316 SS adjusters                    |
| Fork pockets                | 200 × 100 mm × 1,500 mm deep, front + side approach | Same                                  |
| Lift points                 | 4 × M30 forged lifting eyes, 7,500 kg WLL each | Same, 316 SS                          |
| ISO corner compatibility    | Optional (for stackability on truck flatbed) | Required — must lash to deck per marine transport regs |
| Coatings                    | Zinc-rich primer + 2-pack epoxy + polyurethane topcoat (500 μm DFT) | Jotun SeaQuantum XP or Hempel marine system (800 μm DFT) |

### Drip Containment

| Item                        | Spec                                                      |
|-----------------------------|-----------------------------------------------------------|
| Drip pan                    | Welded 304L SS (onshore) / 316L SS (offshore), 3 mm thick |
| Drip pan depth              | 100 mm                                                    |
| Drip pan capacity           | 300 L (exceeds largest single PG25 leak scenario: 200 L storage tank rupture) |
| Pan drain                   | 2" NPT with manual ball valve and cap; routed per site plan to platform containment |
| Leak detection              | TraceTek TT1000-OHP cable mounted at pan bottom, 1 zone, routed to skid PLC |
| Pan slope                   | 2° toward drain point (corner)                            |

### Seismic / Marine Anchoring

**Onshore (Lafayette) — ICC-ES AC156 / ASCE 7-22 Ss = 0.15 g:**
- 4 anchor points at skid base corners
- M16 × 300 mm Hilti HIT-HY 200 epoxy anchor (or equivalent) into 150 mm minimum concrete slab
- Anchor seismic rating to match or exceed skid operating weight × 1.5× (8,700 kg rated)

**Offshore (North Sea / Gulf of Mexico marine):**
- 4 weld-on lashing cleats to skid base; ISO corner castings for deck securing
- Vibration isolators: spring isolators (Mason Industries AFS) under each pump foot, 50 mm natural deflection
- Skid-to-deck fasteners: Monel bolts with Inconel washers, anti-galling compound, loose inspection every 90 days

### Access & Maintenance Clearance

Required clearance around skid for service (documented on site plan):

- **Pump end (long side):** 1,200 mm (pump seal replacement, motor alignment)
- **HX end (long side):** 1,500 mm (plate pack removal; add-plates future expansion)
- **Controls panel side:** 800 mm (NFPA 70 Working Space, 480 V AC panel)
- **Expansion/makeup side:** 600 mm (tank inspection, makeup fill)

---

## §9  CONTROLS & INSTRUMENTATION

### Controller

| Parameter                | Value                                                    |
|--------------------------|----------------------------------------------------------|
| Platform                 | Siemens S7-1500 or Allen-Bradley CompactLogix 5380       |
| Redundancy               | Single controller (skid scope) — failover to Cassette Jetson Orin via Modbus TCP on skid PLC fault |
| I/O                      | 32 AI (RTD + 4–20 mA), 16 DI, 16 DO, 8 AO                |
| Communication            | Modbus TCP (to Cassette Jetson Orin BMS), OPC-UA (to platform SCADA), Ethernet/IP (to VFDs) |
| Control cabinet          | NEMA 4 (onshore) / NEMA 4X 316 SS (offshore), with HVAC cooling if skid interior heat-load exceeds 300 W |
| Power supply             | 480 V AC → 120 V AC control transformer, 10 kVA; 24 V DC logic supply with UPS backup (30 min) |
| HMI                      | 12" color touchscreen (Maple HMC, Siemens Basic Panel, or Red Lion Graphite) at skid face |

### Sensor Schedule

| Tag     | Service                      | Location                   | Sensor Type                    | Range          | Signal    |
|---------|------------------------------|----------------------------|--------------------------------|----------------|-----------|
| TT-101  | Primary supply T             | Skid supply outlet (to QBH-S) | Pt100 RTD, 3-wire           | 0–80 °C        | 4–20 mA   |
| TT-102  | Primary return T             | Skid return inlet (from QBH-R) | Pt100 RTD, 3-wire           | 0–80 °C        | 4–20 mA   |
| TT-103  | Intermediate supply T        | HX intermediate inlet      | Pt100 RTD, 3-wire              | 0–80 °C        | 4–20 mA   |
| TT-104  | Intermediate return T        | HX intermediate outlet     | Pt100 RTD, 3-wire              | 0–80 °C        | 4–20 mA   |
| PT-101  | Primary pump discharge P     | Pump discharge manifold    | Pressure transmitter           | 0–10 bar       | 4–20 mA   |
| PT-102  | Primary pump suction P       | Pump suction manifold      | Pressure transmitter           | 0–10 bar       | 4–20 mA   |
| PT-103  | Primary supply P (QD face)   | Skid supply outlet         | Pressure transmitter           | 0–10 bar       | 4–20 mA   |
| DPT-101 | HX primary-side Δp           | Across HX primary ports    | Δp transmitter                 | 0–2.0 bar      | 4–20 mA   |
| FT-101  | Primary flow                 | Pump discharge manifold    | Magnetic flow meter, DN150     | 0–3,000 LPM    | 4–20 mA + pulse |
| FT-102  | Intermediate flow            | Intermediate supply line   | Magnetic flow meter, DN150     | 0–5,000 LPM    | 4–20 mA   |
| LT-101  | Expansion tank pressure      | Tank air-side tap          | Pressure transmitter           | 0–6 bar        | 4–20 mA   |
| LT-102  | Makeup storage tank level    | Storage tank top           | Ultrasonic level               | 0–200 L        | 4–20 mA   |
| QT-101  | Makeup chemistry monitor     | Makeup fill line           | Conductivity probe             | 0–1,000 μS/cm  | 4–20 mA   |
| XE-101  | Primary side TraceTek        | Skid drip pan              | TraceTek TT1000-OHP (single zone) | On/off      | Alarm DI  |
| XE-102  | Intermediate side TraceTek   | HX intermediate return flange | TraceTek (single zone)      | On/off         | Alarm DI  |

### Control Loops

**CL-1 — Supply Temperature Control (primary).** Supply setpoint 45 °C. PID output modulates pump VFD speed; if pump speed is at minimum and supply T still too cold, opens intermediate-side bypass valve (CX-04) to reduce HX duty; if at maximum and too warm, escalates BMS alarm and requests platform increase intermediate flow.

**CL-2 — Loop Pressure Monitor.** PT-103 below 2.0 bar → open makeup solenoid valve, command makeup pump. Above 4.5 bar → alarm (indicates over-pressurization or thermal excursion).

**CL-3 — Pump Failover.** P1 duty, P2 standby. On P1 fault (VFD alarm, motor overload, no-flow after 10 s command): auto-start P2, log event, alert Cassette BMS. P1/P2 alternate every 2,000 operating hours at maintenance window.

**CL-4 — HX Δp Monitor.** DPT-101 rising over 30-day baseline indicates HX fouling. Warning alarm at +25% baseline; critical alarm at +50% (prompts HX cleaning).

**CL-5 — Leak Response.** XE-101 or XE-102 alarm → close MIV-S and MIV-R on Cassette side (Cassette BMS command via Modbus TCP), stop pumps, alert platform SCADA. Manual reset only.

### Alarm Hierarchy

| Level | Conditions (examples)                                              | Action                                         |
|-------|--------------------------------------------------------------------|-----------------------------------------------|
| WARN  | Pump runtime > alternation threshold; HX Δp +25% baseline         | Logged; scheduled maintenance ticket          |
| ALARM | Supply T > 48 °C > 5 min; makeup > 5 L in 30 days                 | SCADA alert; on-site response required         |
| CRITICAL | TraceTek wet; supply T > 55 °C; loop P < 2.0 bar after makeup   | Pump stop; MIV closure; E-stop handshake to Cassette |

---

## §10  ELECTRICAL DISTRIBUTION

### Skid Main Service

| Parameter                          | Value                                                    |
|------------------------------------|----------------------------------------------------------|
| Primary voltage                    | 480 V AC 3-phase, 60 Hz (50 Hz accepted with VFD/motor retuning) |
| Service entry                      | Platform-provided feeder, terminated at skid main disconnect |
| Skid main disconnect               | 60 A, 480 V AC 3-ph, motor-rated, lockable, shunt-trip   |
| Ground                             | Skid bonded to platform SPG via 25 mm² conductor (≤ 10 m run) |
| Surge protection                   | Type 2 SPD at skid main, 40 kA per phase                 |

**Skid service is separate from Cassette primary AC feed.** Per ECP-001 §1, Cassette 480 V AC primary enters at the ELEC ECP; CDU skid has its own dedicated 480 V AC service furnished directly by the platform — not routed through the cassette.

### Skid Load Schedule

| Load                           | Voltage      | Running (kW) | Peak (kW) | Breaker |
|--------------------------------|--------------|--------------|-----------|---------|
| Pump P1 (duty)                 | 480 V AC 3-ph | 15          | 17 (startup) | 30 A   |
| Pump P2 (standby, running ≤ 5% time) | 480 V AC 3-ph | 0 (0.3 avg) | 17       | 30 A   |
| HX intermediate-side bypass valve actuator | 120 V AC | 0.1     | 0.1       | 15 A   |
| Makeup metering pump           | 120 V AC     | 0.05         | 0.5       | 15 A   |
| Control cabinet + HMI          | 120 V AC     | 0.5          | 0.7       | 15 A   |
| VFDs (input) — 2 × PowerFlex 525 | 480 V AC 3-ph | (included in pump numbers) | — | — |
| Heat trace (offshore variant only) | 120 V AC  | 3.0 (seasonal) | 3.0     | 20 A   |
| Drip pan electric heater (offshore, freeze protect) | 120 V AC | 0.5 | 0.5 | 15 A   |
| **Running total (duty-only, onshore)** | — | **15.6 kW**  | **18.3 kW** | — |
| **Offshore running total**     | —            | **19.1 kW**  | **21.8 kW** | —    |

### Skid Electrical Panel

| Component                           | Spec                                                 |
|-------------------------------------|------------------------------------------------------|
| Main panel enclosure                | NEMA 4 (onshore) / NEMA 4X 316L SS (offshore), with window for HMI |
| Panel dimensions                    | 1,200 × 800 × 300 mm                                |
| Main disconnect                     | 60 A motor-rated, lockable                          |
| Branch circuit breakers             | 30 A (×2 for pumps), 20 A (×1 heat trace), 15 A (×3 accessories) |
| 480/120 V control transformer       | 10 kVA, NEMA 1 encapsulated, primary fused           |
| VFD location                        | In main panel if thermal budget allows; separate ventilated VFD cabinet if ambient > 40 °C |
| Ground bar                          | Copper, 25 mm² minimum; bonded to skid frame and platform SPG |
| Panel internal lighting             | LED 120 V AC, door-switch activated                  |
| Panel heater (offshore / cold climate) | 150 W with thermostat, prevents condensation     |

### Conductor Sizing — Skid Main

| Parameter                     | Value                                              |
|-------------------------------|----------------------------------------------------|
| Skid total running current    | 20.5 A (P1 duty) + 2 A (aux) = 22.5 A continuous  |
| Peak current (P1 startup + aux) | ~30 A (0.5 s inrush)                             |
| NEC 125% continuous + peak    | 30 A                                               |
| Skid main breaker             | 60 A (allows for future load growth, accommodates P2 startup overlap during failover) |
| Conductor from platform feeder | 4× 10 mm² (7 AWG) + 6 mm² (9 AWG) ground, XHHW-2 |
| Run length                    | Per site installation                              |

---

## §11  COMMISSIONING — SKID HYDRAULIC + THERMAL

### Factory Commissioning (Skid Vendor)

#### SK-1  Skid Hydrostatic Test

- Primary-side loop (pump → HX primary → expansion tank → return) pressure-tested to 15 bar for 60 min
- Intermediate-side loop (HX intermediate → flanged connections capped) pressure-tested to 15 bar for 60 min
- Acceptance: zero measurable pressure decay

#### SK-2  Dry Functional Test

- Energize 480 V AC input; verify phase rotation correct (A-B-C)
- Close main disconnect; verify control transformer outputs 120 V AC
- HMI boots, PLC runs, all I/O points show live values (zero for unsignaled analog, closed for normally-closed DI)
- Each VFD spins pump briefly (1–2 s) uncoupled from load to confirm motor rotation direction; recouple

#### SK-3  Wet Commissioning with Water

- Fill both primary and intermediate loops with clean water (no PG25 yet)
- Verify pump ramps to design flow; verify flow meter readings
- Verify pressure transmitters read correctly; dead-weight tester calibration within ±0.05 bar
- Verify temperature sensors track ±0.3 °C of calibrated reference
- Leak-check all joints, flanges, and seals over 4-hour hold
- Drain water; dry with warm-air purge

#### SK-4  Factory Acceptance Test (FAT)

- Witnessed by ADC representative
- Simulate P1 fault → P2 auto-start within 5 s verified
- Simulate TraceTek wet alarm → pumps stop, MIV-command output to Cassette interface verified
- Simulate loss of intermediate fluid flow → primary supply T rise detected → alarm to BMS
- Complete documentation: pressure test reports, electrical continuity, sensor cal certs, FAT sign-off

#### SK-5  Skid Ship with PG25 Stored Separately

- PG25 makeup storage tank (200 L, new) filled with inhibited pre-blended PG25 at factory
- Storage tank tethered to skid with anti-spill cap for transport
- Ship with skid per site plan

### Site Commissioning (≤ 12 hours, concurrent with Cassette S-stage commissioning per COOL-001 §10)

#### FS-1  Skid Arrival & Placement

- Inspect skid for shipping damage
- Place on pre-prepared foundation (or deck) per site anchoring spec
- Torque anchor bolts; verify with calibrated wrench

#### FS-2  Connect Platform Intermediate Loop

- Remove intermediate flange caps
- Connect platform-side supply and return to skid flanges
- Purge intermediate loop per platform commissioning procedure
- Pressurize and leak-check intermediate side

#### FS-3  Connect Cassette Hoses

- Remove QBH-150 shipping caps (skid-side flexible hose fittings)
- Mate QBH-150 male halves to Cassette QBH-150 female QD plate per COOL-001 §10 FS-2 (same protocol)
- Verify audible-click engagement and quarter-turn lock

#### FS-4  Electrical Connection

- Platform feeder connected to skid main disconnect
- Verify phase rotation
- Close main disconnect; boot PLC, HMI, VFDs

#### FS-5  Fill Primary Loop

- Skid makeup system primed with PG25 from storage tank
- Primary loop filled through skid makeup-bypass valve; air vented at Cassette VV-1…VV-8 (per COOL-001 §10 H-6)
- Loop pressurized to 3.5 bar at 25 °C ambient
- Leak-check at every joint, focusing on flexible hose fittings and QBH-150 mating faces

#### FS-6  Initial Pump Start

- Start P1 at 30% VFD speed
- Observe flow ramping on FT-101; verify incrementally to 100% over 10 min
- Check suction pressure (PT-102) remains above cavitation threshold
- Monitor vibration (IR thermography, acoustic) for 30 min; note any anomalies

#### FS-7  Thermal Commissioning

Concurrent with Cassette thermal commissioning (COOL-001 §10 S-4/S-5):

- Cassette dispatches compute at 50% CPX load
- Skid maintains 45 °C supply via CL-1 pump speed control
- Intermediate platform flow active
- Observe HX approach temperature, primary-side Δp, pump VFD output
- Ramp Cassette to 100% CPX load; verify steady-state at 45 °C supply, 57 °C return, 12 K ΔT
- Hold 4 hours at full load

#### FS-8  Failover Verification

- Manually trip P1 (open disconnect on P1 motor)
- Observe P2 auto-start within 5 s
- Verify supply T remains within ±1 °C of setpoint during transition
- Reset P1; return P2 to standby; log event

#### FS-9  Release to Service

- Sign-off per joint Cassette / skid acceptance matrix
- Transfer to platform operations

---

## §12  OPEN ITEMS

| ID    | Priority | Description                                                                                                   | Blocks                                                    |
|-------|----------|---------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------|
| CX-01 | P-0      | Intermediate loop variant selection per deployment — baseline onshore = Variant A (dry-cooler 30% PG), offshore = Variant D (titanium HX). Site-specific for river water or tower water sites. | HX plate material; flange/connection materials; chemistry provisions |
| CX-02 | P-0      | Plate HX vendor selection (Alfa Laval M20 / Kelvion NT series / Sondex S-series). Obtain thermal rating, plate count, primary-side Δp curve, and 10-year service TCO. Confirm 20% frame-length margin for CPX-Next plate addition. | Skid layout; pump head budget; procurement                |
| CX-03 | P-0      | Primary PG25 pump vendor selection (Grundfos NB / Xylem e-1510 / Armstrong 4380 / KSB Etanorm). Obtain head/flow curves at BEP, seal options (single vs double cartridge), spare parts kit. | Pump procurement; electrical load firming                 |
| CX-04 | P-1      | Intermediate-side bypass valve for part-load supply-T control — sizing, actuator (electric vs pneumatic), and control strategy. Affects CL-1 control loop at < 33% pump speed. | Low-load control stability; CL-1 tuning                   |
| CX-05 | P-1      | Skid MCC panel product selection (main disconnect brand, VFD platform, PLC platform) — coordinate with Cassette BMS Modbus TCP interface. | Controls fabrication                                       |
| CX-06 | P-1      | Flex hose 7-year replacement interval — confirm based on Parker or Gates service bulletins; adjust maintenance schedule in §6.       | Service documentation                                     |
| CX-07 | P-2      | Skid footprint vs Lafayette onshore site plan — confirm 3.5 × 2.0 m footprint fits allocated skid pad location; adjust frame if needed. | Civil works coordination                                  |
| CX-08 | P-2      | Offshore variant heat trace sizing — confirm 3.0 kW at worst-case ambient covers freeze protection; coordinate with platform heat-trace coverage. | Offshore procurement                                      |
| CX-09 | P-1      | Commissioning PG25 supply-chain — factory makeup storage tank fill logistics; pre-blended PG25 sourcing (Dowfrost HD or DynaCool per COOL-001 C-02). | Site commissioning logistics                              |
| CX-10 | P-2      | Intermediate loop fouling monitoring — implementation of HX Δp trending for intermediate-side plate fouling (separate from primary-side monitoring in CL-4). Required for open-loop tower water and river water variants. | Maintenance strategy — Variants B/C/D only                |

---

**Cassette — External CDU Skid Specification**
**Cassette-COOL2-001 · Rev 1.0 · 2026-04-22**
**Scott Tomsu · scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana**
**CONFIDENTIAL**
