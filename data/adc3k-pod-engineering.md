# ADC 3K Pod Engineering Layout
## 40-ft High Cube ISO Container — 10x NVL72 Rack Configuration

**Document**: ADC3K-ENG-001 Rev A
**Date**: 2026-03-24
**Author**: Mission Control Engineering
**Status**: PRELIMINARY DESIGN — Requires Physical Verification

---

## 1. VERIFIED EQUIPMENT SPECIFICATIONS

### 1.1 NVL72 Rack — Physical Dimensions (VERIFIED)

Sources: HPE QuickSpecs (a50009224enw), Supermicro SRS-GB200-NVL72-M1 datasheet

| Parameter | Metric | Imperial | Source |
|-----------|--------|----------|--------|
| **Width** | 600 mm | 23.6 in (1 ft 11.6 in) | HPE/Supermicro confirmed |
| **Depth** | 1,068 mm | 42.0 in (3 ft 6 in) | HPE/Supermicro confirmed |
| **Height** | 2,236 mm (Supermicro) / 2,495 mm (HPE) | 88 in / 98.2 in | Varies by OEM |
| **Rack Units** | 48U | 48U | OCP Open Rack V3 |
| **Form Factor** | OCP Open Rack V3 (NOT standard 19-in) | — | NVIDIA MGX |

**CRITICAL NOTE**: The NVL72 is NOT a standard 19-inch rack. It uses OCP Open Rack V3
at 600mm wide (vs 600mm/23.6in for OCP, compared to 482mm/19in for EIA-310).
Depth is 1,068mm (42 in), NOT the 48 in (1,200mm) used in standard deep racks.

**HEIGHT DISCREPANCY**: Supermicro lists 2,236mm (88 in / 7 ft 4 in). HPE lists
2,495mm (98.2 in / 8 ft 2 in). The HPE figure likely includes casters or overhead
cable management. Using Supermicro's 2,236mm (88 in) as the rack body height.

**Container clearance check**: Container internal height is 2,698mm (8 ft 10 in).
Rack height 2,236mm leaves 462mm (18.2 in) overhead for cable routing and lighting.
If HPE height (2,495mm) applies, only 203mm (8 in) overhead — TIGHT. MUST VERIFY.

### 1.2 NVL72 Rack — Weight (VERIFIED)

| Parameter | Value | Source |
|-----------|-------|--------|
| Rack fully loaded (Supermicro) | 1,360 kg / 3,000 lbs | Supermicro datasheet |
| Rack fully loaded (HPE, with PGW) | 1,472 kg / 3,245 lbs | HPE QuickSpecs |
| **Design weight per rack** | **1,500 kg / 3,300 lbs** | Conservative estimate |

Using 3,300 lbs per rack for engineering calculations (worst case + margin).

### 1.3 NVL72 Rack — Internal Configuration

Each NVL72 rack contains (single integrated 48U rack):
- 18x 1U compute trays (each: 2 Grace CPUs + 4 Blackwell GPUs)
- 9x 1U NVLink switch trays (mid-rack, connecting all 18 compute nodes)
- NVLink passive copper cable backplane (5,000+ internal copper cables)
- 8x 1U power shelves (33 kW each, N+N redundant)
- In-rack liquid cooling manifolds
- In-rack CDU option (Supermicro: 4U, 250 kW capacity) OR external CDU

**KEY**: Compute + NVLink switches are ALL in the same rack. The NVL72 is a single
rack system, not a two-rack split. Each rack is a self-contained NVLink domain.

### 1.4 NVL72 Rack — Power (VERIFIED)

| Parameter | Value | Source |
|-----------|-------|--------|
| Rack TDP (GB200 generation) | 120-132 kW | NVIDIA / TrendForce |
| Rack operating power | 125-135 kW | NVIDIA |
| Liquid-cooled portion | ~115 kW | NVIDIA DGX User Guide |
| Air-cooled portion (PSUs, fans) | ~17 kW | NVIDIA DGX User Guide |
| Power shelves | 8x 33 kW (N+N redundant) | Supermicro |

**VERA RUBIN NOTE**: The Vera Rubin NVL72 (H2 2026, ADC's target) has TWO profiles:
- Max Q: ~190 kW per rack (1.8 kW per GPU)
- Max P: ~230 kW per rack (2.3 kW per GPU)
TDP is NOT yet final. Using 130 kW (GB200 baseline) for this document.
**If Vera Rubin ships at 190-230 kW, the power budget below DOUBLES. Redesign required.**

### 1.5 NVL72 Rack — Cooling (VERIFIED)

| Parameter | Value | Source |
|-----------|-------|--------|
| Cooling type | Direct-to-chip liquid | NVIDIA |
| Coolant supply temp | 45 deg C (113 deg F) | NVIDIA DSX / Vera Rubin spec |
| Coolant return temp | 55-65 deg C (131-149 deg F) | NVIDIA / Introl |
| Flow rate per rack | 80-130 LPM (21-34 GPM) | NVIDIA / OCP guidance |
| In-rack CDU capacity | 250 kW (Supermicro 4U) | Supermicro |
| Heat exchange | Liquid-to-liquid (secondary to facility loop) | NVIDIA |

### 1.6 Container — Internal Dimensions (STANDARD 40-FT HIGH CUBE)

| Parameter | Metric | Imperial |
|-----------|--------|----------|
| **Internal length** | 12,032 mm | 39 ft 5.4 in |
| **Internal width** | 2,352 mm | 7 ft 8.6 in |
| **Internal height** | 2,698 mm | 8 ft 10 in |
| Door opening width | 2,340 mm | 7 ft 8.1 in |
| Door opening height | 2,585 mm | 8 ft 5.8 in |
| Tare weight | 3,940 kg / 8,686 lbs | — |
| Max payload | 26,300 kg / 58,000 lbs | — |
| Max gross weight | 30,480 kg / 67,200 lbs | — |

---

## 2. LAYOUT GEOMETRY — CENTER-MOUNTED SINGLE ROW

### 2.1 Cross-Section Analysis (Width)

```
Container internal width:           2,352 mm (92.6 in)
NVL72 rack depth (front-to-back):   1,068 mm (42.0 in)
                                     ─────────────────
Remaining clearance (total):         1,284 mm (50.6 in)
Clearance per side:                    642 mm (25.3 in)
```

**25.3 inches per side** — This is TIGHT but workable for the following reasons:

1. **NEC 110.26 requires 30 inches** of working space in front of electrical equipment.
   The racks themselves are not panelboards, but the power shelves inside are.
   25.3 inches does NOT meet NEC 110.26 for live electrical work.

2. **SOLUTION: Removable access panels in container walls.**
   - Cut 36-in wide x 72-in tall access panels on BOTH long sides of container
   - One panel per rack position (10 panels per side, 20 total)
   - Hinged or bolt-on weatherproof panels (gasket-sealed for transport)
   - When open: technician stands OUTSIDE container, reaches into 25-in gap
   - Effective working space: unlimited (outdoor) + 25 in reach depth
   - This satisfies NEC intent: full-body access without entering confined space

3. **For transport**: All panels closed, sealed, and bolted. Container is weathertight.

4. **Alternative consideration**: Offset racks 3 inches toward one side to create
   28.3 in on one side (primary service) and 22.3 in on the other (cable side).
   Not recommended — keep centered for transport weight balance.

### 2.2 Longitudinal Layout (Length)

```
Container internal length: 12,032 mm (39 ft 5.4 in / 473.7 in)

LAYOUT — Door End to Closed End:

 [DOOR END]                                                    [CLOSED END]
 |                                                                        |
 | ELEC  |  R1   R2   R3   R4   R5   R6   R7   R8   R9   R10 |   CDU    |
 | PANEL |                                                     |   ZONE   |
 |       |                                                     |          |
 |<-36-->|<-- 10 racks x 24in = 240in + 9 gaps x 2in = 18in ->|<-- 48 ->|
 | 914mm |<-------------- 6,553 mm (258 in) ------------------>| 1,219mm |
 |       |                                                     |          |

 Total allocated: 914 + 6,553 + 1,219 = 8,686 mm (342 in / 28.5 ft)
 Remaining spare: 12,032 - 8,686 = 3,346 mm (131.7 in / 11.0 ft)
```

**11 feet of spare length.** This allows:

- Expanding CDU zone to 6 ft (1,829 mm) for larger external CDU manifold
- Adding a 3-ft (914 mm) network/patch panel zone between racks and CDU
- Increasing inter-rack gaps from 2 in to 4 in for better cable routing
- Buffer zone at door end for personnel entry/egress (NEC requires 24-in min)

### 2.3 Revised Layout with Spare Distributed

```
 [DOOR END]                                                          [CLOSED END]
 |                                                                              |
 | ENTRY | ELEC |  R1  R2  R3  R4  R5  R6  R7  R8  R9  R10 | PATCH | CDU     |
 | ZONE  | PANEL|                                             | PANEL | ZONE    |
 |       |      |                                             |       |         |
 |<-36-->|<-42->|<- 10x24in racks + 9x4in gaps = 276in ----->|<-36-->|<--72--->|
 |914 mm |1067mm|<------------ 7,010 mm (276 in) ----------->|914 mm |1,829 mm |

 Total: 914 + 1,067 + 7,010 + 914 + 1,829 = 11,734 mm (461.9 in / 38.5 ft)
 Remaining: 12,032 - 11,734 = 298 mm (11.7 in) — absorbed into tolerances
```

---

## 3. ENGINEERING DRAWINGS (ASCII)

### 3.1 TOP VIEW — Full Container Layout

```
                              39 ft 5 in (12,032 mm)
    |<-------------------------------------------------------------------->|
    |                                                                      |
    | ENTRY|ELEC |  R1    R2    R3    R4    R5    R6    R7    R8    R9   R10|PATCH| CDU  |
    | ZONE |PANEL|  ||    ||    ||    ||    ||    ||    ||    ||    ||    || |PANEL| ZONE |
    |      |     |  ||    ||    ||    ||    ||    ||    ||    ||    ||    || |     |      |
    |      |     |  ||    ||    ||    ||    ||    ||    ||    ||    ||    || |     |      |
    |      |     |  ||    ||    ||    ||    ||    ||    ||    ||    ||    || |     |      |
    |______|_____|__||____||____||____||____||____||____||____||____||____||_|_____|______|
                       7 ft 8.6 in (2,352 mm)

    ===  ACCESS PANELS (both long walls)  ===
    [AP1] [AP2] [AP3] [AP4] [AP5] [AP6] [AP7] [AP8] [AP9] [AP10]

    Each access panel: 36 in W x 72 in H, weatherproof, hinged/bolted
    Aligned with each rack position on BOTH sides of container
```

### 3.2 SIDE VIEW — Longitudinal Cross-Section (Looking from Access Panel Side)

```
    8 ft 10 in (2,698 mm) internal height
    _______________________________________________________________________________
    |  LED    CABLE TRAY (overhead)    LED    CABLE TRAY    LED    CABLE TRAY     |
    |  ___    _________________        ___    ___________   ___    ___________    |
    | |   |  | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |R10 |       |      |
    | | E |  |    |    |    |    |    |    |    |    |    |    |  P    |  CDU |
    | | L |  | 88"|    |    |    |    |    |    |    |    |    |  A    |      |
    | | E |  |    |    |    |    |    |    |    |    |    |    |  T    |      |
    | | C |  |    |    |    |    |    |    |    |    |    |    |  C    |      |
    | |   |  |____|____|____|____|____|____|____|____|____|____|  H    |______|
    | |___|                                                           |      |
    |  FLOOR (reinforced steel, no raised floor needed)                      |
    |________________________________________________________________________|

    ^         ^                                                   ^       ^
    36 in     42 in                276 in                         36 in   72 in
    entry     elec          10 racks + 9 gaps                     patch   CDU
```

### 3.3 END VIEW — Cross-Section (Looking from Door End Toward Racks)

```
                    7 ft 8.6 in (2,352 mm)
              |<--------------------------------->|
              |                                   |
     8 ft     |   ______  CABLE TRAY  ______      |
     10 in    |  |______|_____________|______|     |
              |         |             |            |
              |         |   NVL72     |            |
              |  25.3"  |    RACK     |  25.3"     |
              |  clear  |  (42 in /   |  clear     |
              |         | 1,068 mm    |            |
              |         |   deep)     |            |
              |         |             |            |
              |         |  23.6 in /  |            |
              |         |  600 mm wide|            |
              |_________|_____________|____________|

              |<------->|<---------->|<--------->|
                642 mm     1,068 mm     642 mm
                (25.3 in)  (42.0 in)   (25.3 in)

              [ACCESS]                  [ACCESS]
              [PANEL]                   [PANEL]
              (opens                    (opens
              outward)                  outward)
```

### 3.4 CABLE ROUTING — Overhead Drop-Down System

```
    CEILING (container roof, reinforced with Unistrut channel)
    |============================================================|
    |  [CABLE TRAY - 12in wide x 4in deep, perforated]          |
    |  ==========================================                 |
    |      |    |    |    |    |    |    |    |    |    |         |
    |      v    v    v    v    v    v    v    v    v    v         |
    |     R1   R2   R3   R4   R5   R6   R7   R8   R9  R10       |
    |                                                             |
    |  Cable types in tray:                                       |
    |  - Fiber optic (InfiniBand / Ethernet to patch panel)       |
    |  - 800V DC power bus from electrical panel                  |
    |  - Monitoring / management Ethernet (1GbE)                  |
    |  - Coolant sensor wiring (temp, flow, leak detection)       |
    |                                                             |
    |  SEPARATION: Power cables on LEFT side of tray              |
    |              Data cables on RIGHT side of tray              |
    |              Min 2-in separation per NEC 300.3              |
    |============================================================|
```

### 3.5 CDU ZONE — Closed End Detail

```
              CDU ZONE — 72 in (1,829 mm) deep
    |<------------------------------------------------------>|
    |                                                        |
    |  [PRIMARY CDU]          [SECONDARY CDU]                |
    |  Liquid-to-liquid       (N+1 redundancy)               |
    |  250 kW capacity        250 kW capacity                |
    |                                                        |
    |  Supply manifold (45C) ================================> to racks
    |  Return manifold (55-65C) <============================= from racks
    |                                                        |
    |  [QUICK-DISCONNECT BULKHEAD FITTINGS]                  |
    |  Through container end wall to external dry cooler     |
    |  - 2x supply (redundant)                               |
    |  - 2x return (redundant)                               |
    |  - Isolation valves on both sides                      |
    |                                                        |
    |  [LEAK DETECTION TRAY]                                 |
    |  Full-width drip tray with sensor rope                 |
    |                                                        |
    |  [EXPANSION TANK + FILL PORT]                          |
    |  Accessible from container end (external panel)        |
    |________________________________________________________|

    EXTERNAL (behind closed end wall):
    - Quick-disconnect to dry cooler / cooling tower
    - Facility water loop connection
    - Drain valve
```

### 3.6 ACCESS PANEL DETAIL

```
    CONTAINER WALL (Corten steel, 2mm)

    _________________________________
    |                               |
    |   REMOVABLE ACCESS PANEL      |
    |   36 in W x 72 in H          |
    |                               |
    |   - 14-gauge steel frame      |
    |   - EPDM gasket seal          |
    |   - 8x cam-lock fasteners     |
    |   - Hinge option (top-hung)   |
    |     for permanent install     |
    |   - Prop rod when open        |
    |                               |
    |   TRANSPORT: Bolted shut,     |
    |   gasket compressed,          |
    |   weathertight                |
    |                               |
    |   ON-SITE: Open for service   |
    |   access to rack sides        |
    |   Technician works from       |
    |   outside, reaching 25 in    |
    |   to rack face               |
    |_______________________________|

    10 panels per side x 2 sides = 20 panels total
```

---

## 4. WEIGHT ANALYSIS

### 4.1 Component Weight Budget

| Component | Qty | Unit Weight | Total Weight |
|-----------|-----|-------------|--------------|
| NVL72 racks (loaded) | 10 | 3,300 lbs | 33,000 lbs |
| CDU (primary) | 1 | 882 lbs (400 kg) | 882 lbs |
| CDU (secondary/redundant) | 1 | 882 lbs | 882 lbs |
| Electrical panel + bus bars | 1 | 800 lbs | 800 lbs |
| Cable trays + cables | — | — | 500 lbs |
| Coolant piping + manifolds | — | — | 400 lbs |
| Coolant fluid (in system) | — | — | 300 lbs |
| Structural reinforcement | — | — | 1,000 lbs |
| Access panels (20x) | 20 | 40 lbs | 800 lbs |
| Patch panel / network cab | 1 | 200 lbs | 200 lbs |
| LED lighting + sensors | — | — | 100 lbs |
| **TOTAL PAYLOAD** | | | **38,864 lbs** |

### 4.2 Payload Check

```
Container max payload:    58,000 lbs
Calculated payload:       38,864 lbs
Margin:                   19,136 lbs (33% under limit)   PASS
```

### 4.3 Floor Loading Analysis

```
Container floor area:     39.45 ft x 7.72 ft = 304.6 sq ft
Total weight on floor:    38,864 lbs
Average floor loading:    127.6 lbs/sq ft                 OK

POINT LOAD per rack:
  Rack footprint:         23.6 in x 42.0 in = 991 sq in = 6.88 sq ft
  Rack weight:            3,300 lbs
  Point load:             479.6 lbs/sq ft                 MANAGEABLE

  BUT: Rack has 4 leveling feet/casters
  Each foot carries:      ~825 lbs
  Foot area (est 4 sq in): 825 / 0.028 sq ft = 29,464 lbs/sq ft  CRITICAL

  SOLUTION: Steel spreader plates under each rack
  Plate size: 24 in x 44 in (1,056 sq in = 7.33 sq ft)
  Load per plate: 3,300 / 7.33 = 450 lbs/sq ft           OK
  Plate thickness: 1/2-inch A36 steel
  Plate weight: ~45 lbs each (included in structural budget)
```

### 4.4 Transport Weight Distribution

```
Container tare:           8,686 lbs
Payload:                  38,864 lbs
GROSS WEIGHT:             47,550 lbs (21.6 metric tons)

US highway limit (single axle): 80,000 lbs gross (truck + trailer + cargo)
Typical chassis:          ~15,000 lbs
Total on road:            ~62,550 lbs                     PASS

BALANCE: Racks are symmetric (5 front, 5 rear of center).
CDU zone (closed end) is heavier than entry zone (door end).
CDU ~1,764 lbs + coolant vs electrical panel ~800 lbs.
Net offset: ~1,264 lbs toward closed end.
Acceptable — well within transport stability limits.
Could add ballast plate at door end if needed.
```

---

## 5. POWER BUDGET

### 5.1 Rack Power (GB200 Baseline)

| Component | Power |
|-----------|-------|
| 10x NVL72 racks @ 130 kW each | 1,300 kW |
| CDU pumps (2x, redundant) | 15 kW |
| Container HVAC (ambient management) | 10 kW |
| Lighting + monitoring + network | 5 kW |
| **TOTAL CONTAINER POWER** | **1,330 kW (1.33 MW)** |

### 5.2 Vera Rubin Projection (IF 190 kW Max Q)

| Component | Power |
|-----------|-------|
| 10x NVL72 racks @ 190 kW each | 1,900 kW |
| CDU pumps + overhead | 30 kW |
| **TOTAL CONTAINER POWER** | **1,930 kW (1.93 MW)** |

### 5.3 Vera Rubin Projection (IF 230 kW Max P)

| Component | Power |
|-----------|-------|
| 10x NVL72 racks @ 230 kW each | 2,300 kW |
| CDU pumps + overhead | 40 kW |
| **TOTAL CONTAINER POWER** | **2,340 kW (2.34 MW)** |

### 5.4 Power Input Architecture

```
EXTERNAL POWER SOURCE
        |
        | 800V DC (Eaton Beam Rubin DSX platform)
        |     OR
        | 480V 3-phase AC (converted to DC at rack PSUs)
        |
        v
  [MAIN DISCONNECT / BREAKER PANEL]
        |
        | 800V DC bus bar (overhead, in cable tray)
        |
        +---> Rack 1 (8x 33kW power shelves)
        +---> Rack 2
        +---> ...
        +---> Rack 10
        +---> CDU power
        +---> Aux power (lighting, sensors, HVAC)

PREFERRED: 800V DC direct feed (Eaton Beam Rubin DSX)
  - Eliminates AC-DC conversion losses at each rack
  - 97% efficiency vs 92% through AC path
  - Reduces heat generated by power conversion
  - Fewer components, higher reliability

FALLBACK: 480V 3-phase AC
  - Standard industrial power input
  - Each rack's 8 power shelves convert AC to DC internally
  - Higher losses, more heat, but universally available
```

---

## 6. COOLING REQUIREMENTS

### 6.1 Heat Load Calculation

```
Total IT heat load:       1,300 kW (GB200 baseline)
Liquid-cooled portion:    ~87% = 1,131 kW
Air-cooled portion:       ~13% = 169 kW (PSU waste heat + fan exhaust)

Cooling requirement:      1,300 kW minimum rejection capacity
Design with 20% margin:  1,560 kW cooling capacity
```

### 6.2 Coolant Flow Rate

```
Heat to reject via liquid:    1,131 kW
Coolant delta T:              10 deg C (45C supply, 55C return — conservative)
                              20 deg C (45C supply, 65C return — max)

Flow rate at 10C delta T:
  Q = P / (Cp x dT)
  Q = 1,131,000 W / (4,186 J/kg-C x 10 C)
  Q = 27.0 kg/s = 1,621 LPM = 428 GPM

Flow rate at 20C delta T:
  Q = 1,131,000 / (4,186 x 20)
  Q = 13.5 kg/s = 810 LPM = 214 GPM

PER RACK (10C delta T):
  ~162 LPM (43 GPM) per rack
  NVIDIA spec: 80-130 LPM per rack
  DISCREPANCY: Our calc is higher than NVIDIA's range.
  Likely because NVIDIA spec assumes per-rack CDU with
  secondary loop; our calc is for the total facility loop.

DESIGN FLOW RATE: 130 LPM per rack x 10 racks = 1,300 LPM (343 GPM) total
  Using NVIDIA's upper spec as the design point.
```

### 6.3 External Heat Rejection

```
OPTION A: Dry Cooler (air-cooled radiator, external to container)
  - Size: ~200 kW per unit, need 7 units (with N+1)
  - Footprint: ~8 ft x 4 ft each, stacked or side-by-side
  - Location: Adjacent to container, connected via quick-disconnect
  - Pro: No water consumption, low maintenance
  - Con: Large footprint, ambient temperature dependent
  - Derate above 35C ambient (Louisiana summer: 95F / 35C)

OPTION B: Cooling Tower (evaporative)
  - Size: 1 unit, ~1,500 kW capacity
  - Water consumption: ~500 gal/hr at full load
  - Pro: Compact, effective in hot/humid climates
  - Con: Water consumption, chemical treatment, Legionella risk

OPTION C: Connection to Facility Cooling Loop
  - At Trappeys: water tower cooling system
  - At Willow Glen: Mississippi River cooling
  - Quick-disconnect bulkhead fittings on container end wall
  - Most efficient option when facility cooling exists

RECOMMENDED: Option C at fixed sites, Option A for remote/temporary deployment.
```

### 6.4 Ambient Air Management

```
Even with liquid cooling handling 87% of heat, 169 kW of air-cooled heat
enters the container interior from PSUs and power conversion.

169 kW in a 2,400 cu ft space = rapid temperature rise without ventilation.

SOLUTION:
  - 2x exhaust fans in container roof (thermostat-controlled)
  - Intake louvers near floor on both long walls (filtered)
  - Target: maintain ambient below 35C (95F) inside container
  - Air volume needed: ~5,000 CFM for 169 kW with 10C rise
  - Fan spec: 2x 2,500 CFM industrial exhaust fans (roof-mounted)
```

---

## 7. STRUCTURAL MODIFICATIONS

### 7.1 Container Reinforcement

| Modification | Purpose | Method |
|-------------|---------|--------|
| Floor reinforcement | Support 38,864 lbs distributed load | 1/4-in steel plate overlay, welded to floor corrugations |
| Spreader plates (10x) | Distribute rack point loads | 1/2-in A36 steel, 24x44 in, bolted to floor |
| Roof reinforcement | Support cable tray + 500 lbs cables | Unistrut channels welded to roof ribs (4 runs) |
| Access panel cutouts (20x) | Service access to rack sides | Plasma-cut openings, welded frames, gasket channels |
| CDU end wall penetrations | Coolant quick-disconnect | 4x 6-in bulkhead fittings (supply + return, redundant) |
| Electrical penetration | Power entry | 1x weatherproof junction box, bottom of door-end wall |
| Exhaust fan openings (2x) | Ambient heat removal | Roof-mounted, flanged, with rain caps |
| Intake louvers (4x) | Fresh air intake | Low on long walls, filtered, motorized dampers |
| Lifting/transport reinforcement | Maintain ISO lifting points | Corner casting reinforcement after panel cutouts |

### 7.2 Corrosion Protection

- All cut edges: prime + 2-coat marine epoxy
- Interior: anti-condensation paint on ceiling
- Exterior panels: powder-coated, gasket-sealed
- Floor: epoxy-coated after steel plate overlay
- Dissimilar metal isolation at all connections (galvanic corrosion prevention)

---

## 8. FIRE SUPPRESSION AND SAFETY

| System | Specification |
|--------|--------------|
| Suppression | Clean agent (Novec 1230 or FM-200), ceiling-mounted nozzles |
| Detection | VESDA (Very Early Smoke Detection Apparatus) — aspirating |
| Leak detection | Sensor rope under every rack, along coolant manifolds |
| Emergency disconnect | Big red button at door entry, kills all power |
| Egress | Door end is primary egress; emergency kick-out panel at CDU end |
| Grounding | Container bonded to ground rod, all racks bonded to container |
| Lightning | Container steel acts as Faraday cage; external ground rod required |

---

## 9. MONITORING AND CONTROLS

| System | Implementation |
|--------|---------------|
| Temperature | 40x sensors (4 per rack zone + ambient + coolant supply/return) |
| Humidity | 4x sensors (entry, mid, CDU, external) |
| Coolant flow | Inline flow meters on supply and return manifolds |
| Coolant leak | Sensor rope (full length of coolant path) + drip trays |
| Power monitoring | Per-rack metering at bus bar tap points |
| Door/panel status | Reed switches on all 20 access panels + both doors |
| Smoke/fire | VESDA system with 4 sampling points |
| Camera | 2x IR cameras (entry end, CDU end) |
| Vibration | Accelerometers on container frame (transport monitoring) |
| Connection | All sensors to local controller (Jetson Orin Nano) |
| Remote | 4G/5G + Starlink backup to MARLIE I NOC via Mission Control |

---

## 10. SUPERPOD CONFIGURATION

### 10.1 8+2 Rack Layout

```
RACK ASSIGNMENTS:

  R1  — COMPUTE (NVL72 #1)     \
  R2  — COMPUTE (NVL72 #2)      |
  R3  — COMPUTE (NVL72 #3)      |
  R4  — COMPUTE (NVL72 #4)      |— 8-rack DGX SuperPOD
  R5  — COMPUTE (NVL72 #5)      |  (8 NVLink domains)
  R6  — COMPUTE (NVL72 #6)      |
  R7  — COMPUTE (NVL72 #7)      |
  R8  — COMPUTE (NVL72 #8)     /
  R9  — NETWORKING (InfiniBand spine switches, Quantum NDR/XDR)
  R10 — STORAGE + MANAGEMENT (NVMe-oF storage, BMC management, monitoring)

SuperPOD inter-rack fabric: InfiniBand via R9 spine switches
Each compute rack's NVLink is INTERNAL (intra-rack GPU-GPU).
InfiniBand handles INTER-rack communication (job scheduling, collective ops).
```

### 10.2 Networking Rack (R9) Contents

| Component | Qty | Purpose |
|-----------|-----|---------|
| NVIDIA Quantum InfiniBand switches | 4-8 | Compute fabric spine |
| Ethernet ToR switches (25/100GbE) | 2 | Management network |
| Patch panels (fiber) | 4 | Inter-rack fiber termination |
| Out-of-band management switch | 1 | BMC/IPMI network |
| Firewall/router | 1 | External connectivity |

### 10.3 Storage Rack (R10) Contents

| Component | Qty | Purpose |
|-----------|-----|---------|
| NVMe-oF storage nodes | 4-8 | High-speed shared storage |
| NVIDIA Base Command Manager node | 1 | Cluster orchestration |
| Monitoring server (Prometheus/Grafana) | 1 | Metrics + alerting |
| Jetson Orin (edge controller) | 1 | Local AI + sensor processing |
| UPS (rack-mount, 10 kVA) | 1 | Graceful shutdown for management |

---

## 11. ITEMS REQUIRING PHYSICAL VERIFICATION

These items CANNOT be determined from documentation alone. They require hands-on
measurement, vendor consultation, or physical prototyping.

| # | Item | Why It Matters | How to Verify |
|---|------|---------------|---------------|
| 1 | **Vera Rubin NVL72 exact dimensions** | May differ from GB200 NVL72; Vera Rubin rack height unknown | Wait for NVIDIA spec sheet (H2 2026) or measure at GTC |
| 2 | **Vera Rubin NVL72 TDP** | 190-230 kW changes EVERYTHING — power, cooling, weight | NVIDIA Enterprise Sales engagement |
| 3 | **Rack height with overhead cable mgmt** | HPE shows 2,495mm vs Supermicro 2,236mm — 10-in difference | Measure physical unit; confirm if top cable mgmt is removable |
| 4 | **Container floor deflection under load** | 38,864 lbs on corrugated steel floor — how much flex? | Structural engineer FEA analysis; physical load test |
| 5 | **Access panel size vs structural integrity** | 20 cutouts weaken container walls significantly | Structural engineer review; may need external frame reinforcement |
| 6 | **Coolant manifold routing clearance** | 25.3 in side clearance must accommodate supply+return piping | Mock up with pipe + fittings in a container |
| 7 | **NEC compliance for 800V DC in container** | NEC 110.26 clearances, NFPA 75, local AHJ requirements | Licensed PE review; AHJ pre-consultation |
| 8 | **Vibration tolerance during transport** | NVL72 has 5,000+ internal copper cables, precision connectors | NVIDIA transport spec; vibration testing |
| 9 | **CDU physical fit in 72-in zone** | Two 250kW CDUs + manifolds + expansion tank in 6-ft depth | CDU vendor dimensions (CoolIT, Vertiv, Motivair) |
| 10 | **External dry cooler sizing** | 1,300 kW rejection at 95F (35C) Louisiana summer ambient | Thermal engineer calculation with local climate data |
| 11 | **Container ISO certification after mods** | 20 access panels + roof penetrations may void ISO rating | CSC (Container Safety Convention) re-certification |
| 12 | **Rack caster/leveling foot compatibility** | OCP Open Rack V3 base may not work on container floor | Confirm rack mounting interface; may need custom brackets |
| 13 | **InfiniBand cable bend radius** | Tight 25-in side clearance for fiber routing to spine rack | NVIDIA cable specs; physical routing test |
| 14 | **Weight with Vera Rubin** | If VR NVL72 weighs 4,000 lbs (per NVIDIA), 10 racks = 40,000 lbs + support = ~45,000 lbs | Re-run weight analysis when VR specs publish |
| 15 | **Insurance and code classification** | Containerized AI facility — what building code applies? | Consult with AHJ (Authority Having Jurisdiction) in target parish |

---

## 12. RISK REGISTER

| Risk | Severity | Mitigation |
|------|----------|-----------|
| Vera Rubin TDP exceeds 200 kW/rack | HIGH | Design power/cooling for 230 kW; if actual is lower, have margin |
| Container structural failure from cutouts | HIGH | PE-stamped structural analysis before fabrication |
| NEC non-compliance (800V DC, clearances) | HIGH | Licensed PE + AHJ pre-review before build |
| Coolant leak in transport | MEDIUM | Drain system before transport; ship dry, fill on-site |
| Overheating in Louisiana summer | MEDIUM | Size dry cooler for 105F (40.5C) ambient with 15% margin |
| Container exceeds road weight limits | LOW | 62,550 lbs total is well under 80,000 lb limit |
| Floor deflection under point loads | MEDIUM | Spreader plates + FEA before loading |
| Fire in enclosed space | HIGH | Clean agent suppression, VESDA, auto-disconnect |

---

## 13. BILL OF MATERIALS — MAJOR ITEMS

| Item | Qty | Est. Unit Cost | Est. Total |
|------|-----|---------------|------------|
| 40-ft High Cube container (new, one-trip) | 1 | $5,000 | $5,000 |
| NVL72 racks (Vera Rubin, fully loaded) | 10 | TBD ($2-3M est) | $20-30M |
| CDU 250kW (CoolIT, Vertiv, or Motivair) | 2 | $50,000 | $100,000 |
| Eaton Beam Rubin DSX power system | 1 | TBD | TBD |
| InfiniBand spine switches (Quantum) | 4-8 | $25,000 | $100-200K |
| NVMe-oF storage nodes | 4-8 | $15,000 | $60-120K |
| Steel floor reinforcement + spreader plates | 1 lot | $15,000 | $15,000 |
| Access panels (fabricated, 20x) | 20 | $500 | $10,000 |
| Cable tray + Unistrut + cables | 1 lot | $8,000 | $8,000 |
| Coolant piping + manifolds + fittings | 1 lot | $12,000 | $12,000 |
| Fire suppression (clean agent) | 1 | $15,000 | $15,000 |
| VESDA + sensors + monitoring | 1 lot | $10,000 | $10,000 |
| Exhaust fans + louvers + HVAC | 1 lot | $5,000 | $5,000 |
| LED lighting + electrical | 1 lot | $3,000 | $3,000 |
| Container modification labor | 1 lot | $25,000 | $25,000 |
| **CONTAINER FIT-OUT TOTAL (excl. racks)** | | | **~$370-530K** |
| **TOTAL WITH RACKS** | | | **$20-31M** |

---

## 14. KEY DIMENSIONS SUMMARY

```
QUICK REFERENCE — ALL VERIFIED DIMENSIONS

Container (40-ft HC internal):
  Length:  12,032 mm / 39 ft 5.4 in / 473.7 in
  Width:    2,352 mm /  7 ft 8.6 in /  92.6 in
  Height:   2,698 mm /  8 ft 10 in  / 106.2 in

NVL72 Rack (GB200 gen, Supermicro):
  Width:      600 mm /  1 ft 11.6 in / 23.6 in
  Depth:    1,068 mm /  3 ft 6.0 in  / 42.0 in
  Height:   2,236 mm /  7 ft 4.2 in  / 88.0 in
  Weight:   1,360-1,472 kg / 3,000-3,245 lbs

Side Clearance (each side):
  (2,352 - 1,068) / 2 = 642 mm / 25.3 in

Overhead Clearance:
  2,698 - 2,236 = 462 mm / 18.2 in (Supermicro height)
  2,698 - 2,495 = 203 mm /  8.0 in (HPE height)

Rack Row Length (10 racks + 9 gaps @ 4 in):
  (10 x 600) + (9 x 102) = 6,918 mm / 272.4 in / 22.7 ft

Total Allocated Length:
  Entry(914) + Elec(1067) + Racks(7010) + Patch(914) + CDU(1829) = 11,734 mm

Spare Length:
  12,032 - 11,734 = 298 mm / 11.7 in
```

---

## 15. COMPARISON: GB200 vs VERA RUBIN NVL72

| Parameter | GB200 NVL72 (VERIFIED) | Vera Rubin NVL72 (PROJECTED) |
|-----------|----------------------|---------------------------|
| GPUs per rack | 72 Blackwell B200 | 72 Rubin |
| CPUs per rack | 36 Grace | 36 Vera |
| Memory per GPU | 192 GB HBM3e | 288 GB HBM4 |
| Rack TDP | 120-132 kW | 190-230 kW (Max Q / Max P) |
| Rack weight | 3,000-3,245 lbs | ~4,000 lbs (per NVIDIA) |
| Rack dimensions | 600 x 1,068 x 2,236 mm | Same MGX form factor (ASSUMED) |
| Cooling | 45C liquid supply | 45C liquid supply |
| Power architecture | 48V bus bar | 800V DC (Eaton Beam Rubin) |
| Container power (10 racks) | 1.33 MW | 1.93-2.34 MW |
| Container weight (10 racks) | ~47,550 lbs gross | ~54,550-57,550 lbs gross |

**CRITICAL**: If Vera Rubin ships at 4,000 lbs/rack and 230 kW, the container hits
~57,550 lbs gross (under 67,200 lb limit) but cooling requirements nearly double.
The CDU zone may need to expand, and external dry cooler capacity roughly doubles.
The 800V DC bus from Eaton Beam Rubin becomes essential at these power densities.

---

## DOCUMENT HISTORY

| Rev | Date | Author | Changes |
|-----|------|--------|---------|
| A | 2026-03-24 | Mission Control | Initial release — preliminary design |

---

## SOURCES

- [NVIDIA GB200 NVL72](https://www.nvidia.com/en-us/data-center/gb200-nvl72/)
- [NVIDIA Vera Rubin NVL72](https://www.nvidia.com/en-us/data-center/vera-rubin-nvl72/)
- [HPE QuickSpecs — GB200 NVL72](https://www.hpe.com/psnow/doc/a50009224enw)
- [Supermicro GB200 NVL72 Datasheet](https://www.supermicro.com/datasheet/datasheet_SuperCluster_GB200_NVL72.pdf)
- [Supermicro GB200 NVL72 Product Page](https://www.supermicro.com/en/products/system/gpu/48u/srs-gb200-nvl72)
- [NVIDIA DGX GB Rack Systems User Guide](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html)
- [Sunbird — Is Your Data Center Ready for NVL72?](https://www.sunbirddcim.com/blog/your-data-center-ready-nvidia-gb200-nvl72)
- [Introl — GB200 NVL72 Deployment Guide](https://introl.com/blog/gb200-nvl72-deployment-72-gpu-liquid-cooled)
- [The Register — DGX GB200 NVL72 Rack System](https://www.theregister.com/2024/03/21/nvidia_dgx_gb200_nvk72/)
- [NVIDIA 800 VDC Architecture Blog](https://developer.nvidia.com/blog/nvidia-800-v-hvdc-architecture-will-power-the-next-generation-of-ai-factories/)
- [Eaton Beam Rubin DSX Announcement](https://www.eaton.com/us/en-us/company/news-insights/news-releases/2026/eaton-collaborates-with-nvidia-to-unveil-its-beam-rubin-dsx-platform.html)
- [NVIDIA DGX SuperPOD Reference Architecture — GB200](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-gb200/latest/dgx-superpod-components.html)
- [TrendForce — NVL72 TDP Data](https://x.com/trendforce/status/1900050272568926560)
- [NEC 110.26 Working Space Requirements](https://up.codes/s/spaces-about-electrical-equipment)
- [Introl — Vera Rubin 600kW Racks](https://introl.com/blog/nvidia-vera-rubin-gpu-600kw-racks-2027)

---

## 8. THERMAL ENGINEERING — LOUISIANA DEPLOYMENT

### 8.1 Design Philosophy
No air conditioning. No human occupancy. Control humidity, not temperature.
Solar roof for shade. Desiccant for moisture. Exhaust fan for convection.
100% AI-monitored — Mission Control manages thermals autonomously.

### 8.2 ASHRAE Equipment Classes (Verified)

| Class | Max Temp | Max Humidity | Application |
|-------|----------|-------------|-------------|
| A1 | 90°F (32°C) | 80% RH | Standard enterprise |
| A2 | 95°F (35°C) | 80% RH | Hardened equipment |
| A3 | 104°F (40°C) | 85% RH | Extreme environments |
| A4 | 113°F (45°C) | 90% RH | Purpose-built ruggedized |

### 8.3 Component Temperature Ratings

| Component | Cooling Method | Max Ambient Rating | Notes |
|-----------|---------------|-------------------|-------|
| GPUs/CPUs | Direct-to-chip liquid (45°C) | N/A — liquid cooled | Ambient doesn't matter |
| NVLink switches | Direct-to-chip liquid | N/A — liquid cooled | Same cooling loop |
| PSUs | Air-cooled (internal fans) | 40-50°C (104-122°F) | Tightest air-cooled spec |
| Network switches | Air-cooled | 40°C (104°F) | Tightest overall |
| SSDs/NVMe | Passive/conduction | 70°C (158°F) | No issue |
| Cables/connectors | Passive | 60-75°C (140-167°F) | No issue |
| Eaton 800V DC bus | Air-cooled | 40-50°C (104-122°F) | Rated for industrial |

### 8.4 Louisiana Thermal Analysis

| Condition | Outside Temp | Inside Unshaded | Inside With Solar Roof |
|-----------|-------------|-----------------|----------------------|
| Winter avg | 55°F (13°C) | 65°F (18°C) | 60°F (16°C) |
| Spring/Fall | 80°F (27°C) | 100°F (38°C) | 90°F (32°C) |
| Summer avg | 92°F (33°C) | 120°F (49°C) | 105°F (40°C) |
| Summer peak | 100°F (38°C) | 140°F (60°C) | 115°F (46°C) |
| Hurricane recovery | 85°F (29°C) | 105°F (40°C) | 95°F (35°C) |

Solar roof reduces internal temp by 10-15°F (15-25°F reduction from peak unshaded).

### 8.5 Design Target

**Container ambient: below 45°C (113°F) at all times.**

This is achievable with:
1. Solar roof (shade + power) — handles peak heat, generates power for support systems
2. Desiccant dehumidifier — strips humidity, no compressor, low power (~500W)
3. Exhaust fan at top — hot air rises, fan pulls it out (~200W)
4. Positive pressure from dehumidifier — dry air in at bottom, hot humid air out at top
5. Sealed container when panels closed — weathertight

### 8.6 What We Do NOT Need
- Air conditioning (no compressor, no refrigerant, no maintenance)
- Human-comfort HVAC (no occupancy, AI-monitored only)
- Raised floor plenum (top-drop cabling, not underfloor)
- Chilled water (liquid cooling loop is separate from ambient control)

### 8.7 AI Thermal Management
Mission Control monitors all thermal sensors autonomously:
- Container ambient temp (multiple sensors)
- Coolant supply/return temps
- Per-rack inlet/outlet temps
- Humidity level
- External ambient + solar irradiance
- Exhaust fan speed

AI adjusts: exhaust fan speed, dehumidifier power, cooling flow rate.
AI alerts: if ambient approaches 45°C, if humidity exceeds 60% RH, if any component over spec.
AI acts: can throttle GPU power to reduce heat generation as last resort.

No human needed. Ever. Unless something physically breaks.

---

## 9. SENSOR PACKAGE — AI MONITORING

### 9.1 Environmental Sensors
| Sensor | Quantity | Location | Purpose |
|--------|----------|----------|---------|
| Temperature (internal) | 4 | Each end + each side, mid-height | Ambient monitoring |
| Temperature (external) | 1 | Outside container, shaded | Ambient reference |
| Humidity (internal) | 2 | Intake + exhaust | Moisture control |
| Solar irradiance | 1 | Roof-mounted | Solar output tracking |

### 9.2 Per-Rack Sensors (x10 racks)
| Sensor | Per Rack | Total | Purpose |
|--------|----------|-------|---------|
| Coolant inlet temp | 1 | 10 | Cooling performance |
| Coolant outlet temp | 1 | 10 | Heat rejection monitoring |
| Coolant flow rate | 1 | 10 | Flow verification |
| Power draw | 1 (via Eaton PDU) | 10 | Per-rack power monitoring |

### 9.3 System Sensors
| Sensor | Quantity | Purpose |
|--------|----------|---------|
| CDU supply/return temp | 2 | Cooling loop health |
| CDU flow rate | 1 | System flow verification |
| Dehumidifier status | 1 | Humidity control |
| Exhaust fan RPM | 1-2 | Ventilation monitoring |
| 800V DC bus voltage | 1 | Power quality |
| Solar panel output (W) | 1 | Generation tracking |
| Generator status | 1 | External power monitoring |
| UPS/battery SOC | 1 | Backup power status |

### 9.4 Security Sensors
| Sensor | Quantity | Purpose |
|--------|----------|---------|
| Cameras (wide angle, IR) | 2 | Each end, interior monitoring |
| Access panel open sensors | 8 | Tamper/access detection |
| Door open sensor | 1 | Main entry |
| Vibration/tamper | 1 | Physical security |
| GPS | 1 | Location tracking (mobile deploy) |

### 9.5 Network Monitoring
| Metric | Method | Purpose |
|--------|--------|---------|
| Per-rack latency | Software | Performance monitoring |
| Bandwidth utilization | Software | Capacity planning |
| Mission Control heartbeat | Software | NOC connectivity |

### 9.6 Total Sensor Count: ~65 sensors per pod

### 9.7 AI Autonomous Responses
| Condition | AI Action |
|-----------|-----------|
| Night / low ambient | Fans to low, solar to battery, cooling reduced |
| Day / peak heat | Solar kicks in, fans ramp up, dehumidifier full |
| Temp approaching 45°C | Increase cooling flow, alert NOC |
| Temp exceeding 45°C | Throttle GPU power (last resort) |
| Humidity spike | Dehumidifier full power, positive pressure increase |
| Access panel opened | Camera alert, log event, notify NOC |
| Coolant leak (flow drop) | Isolate affected rack, alert immediately |
| Power loss | Battery bridge, graceful workload shutdown |
| Network loss to NOC | Continue autonomous operation, retry connection |

---

## 10. CABLE ROUTING — FLOOR LEVEL

### 10.1 Design Decision: Floor-Level, NOT Overhead
- No cable trays above racks (rack height may be 90-98 in, ceiling is 106 in)
- Nothing directly over racks — keep ceiling clear for rack removal
- All cabling runs on container floor along both sides
- Metal conduit or enclosed cable tray
- Optional grating over cables for foot access
- Everything visible and accessible through side access panels
- No humans in there regularly — AI monitored

### 10.2 Cable Routing Layout
```
[SIDE WALL — 4 access panels]
[Floor cable tray: power + network + cooling pipes]
[R1] [R2] [R3] [R4] [R5] [R6] [R7] [R8] [R9] [R10]
[Floor cable tray: power + network + cooling pipes]
[SIDE WALL — 4 access panels]
```

### 10.3 Cable Types on Floor
| Run | Type | Path | Notes |
|-----|------|------|-------|
| 800V DC power | Heavy gauge, metal conduit | Electrical end → each rack | Eaton busway or armored cable |
| InfiniBand | Copper, short runs | Rack to rack, rack to R9 (network) | Keep short for latency |
| Ethernet management | Cat6A | Each rack to R9 (network) | Standard patch cables |
| Cooling supply | Insulated pipe | CDU end → each rack manifold | 45°C supply |
| Cooling return | Insulated pipe | Each rack manifold → CDU end | 55-60°C return |
| Sensor wiring | Low voltage | Along floor to sensor controller | Can be wireless for some |

### 10.4 Why Floor-Level Works
- Nobody walks in there — AI managed, no human occupancy
- All service done from OUTSIDE through access panels
- Shorter cable runs than overhead (connections are at rack base/rear)
- Everything in line of sight through panels
- If someone needs to enter: grating provides walkway over cables
- Rack removal: nothing overhead blocking crane/forklift access

---

## 11. EXTREME CO-DESIGN — CONFIGURABLE RACK POSITIONS

### 11.1 Design Philosophy
The ADC 3K Pod is a configurable platform, not a fixed product. The container, power system (800V DC), cooling loop, access panels, solar roof, and AI monitoring are constant. The 10 rack positions are variable — configured per customer mission.

### 11.2 Standard Configurations

| Config | Name | Racks (Compute/Network/Storage/Other) | GPUs | Best For |
|--------|------|---------------------------------------|------|----------|
| C1 | Full SuperPOD | 8/1/1/0 | 576 | Training + inference (default) |
| C2 | Inference Heavy | 10/0/0/0 (network external) | 720 | Token factory, managed inference |
| C3 | Storage Heavy | 6/1/3/0 | 432 | Medical imaging, video, data lakes |
| C4 | CPU Heavy | 4 GPU + 4 CPU/1/1/0 | 288 GPU + HPC | Oil & gas, weather, molecular dynamics |
| C5 | Edge Inference | 2 GPU + 7 Groq/1/0/0 | 144 GPU + 7 LPU | Autonomous vehicles, robotics, real-time |
| C6 | Hybrid Vendor | 5 NVIDIA + 3 Terafab/1/1/0 | Mixed | Multi-vendor, future-proof |

### 11.3 What Stays Constant (All Configs)
- 40-ft HC ISO container
- 800V DC native power (Eaton Beam Rubin DSX)
- Liquid cooling loop (CDU + external dry cooler)
- 8 access panels (4 per side, top-hinged)
- Solar roof (shade + auxiliary power)
- Desiccant dehumidifier + exhaust fan
- 65 AI-monitored sensors
- Mission Control autonomous management
- Floor-level cable routing
- Fire suppression (Novec 1230 + VESDA)

### 11.4 What Changes Per Config
- Rack type in each of 10 positions
- Power budget (GPU racks: 130 kW each, CPU racks: ~30 kW, Groq LPU: ~TBD)
- Cooling load (proportional to power)
- Network topology (InfiniBand for GPU, Ethernet for CPU/storage)
- Software stack (Dynamo for inference, Base Command for training, Run:AI for orchestration)

### 11.5 Custom Configurations
Any combination of rack types in the 10 positions is possible. Customer specifies workload requirements, ADC engineers the optimal rack mix. The platform supports it — the racks are the variable.
