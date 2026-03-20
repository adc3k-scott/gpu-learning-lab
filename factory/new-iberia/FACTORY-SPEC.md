# NEW IBERIA MODULE FACTORY — ENGINEERING SPECIFICATION

**Project:** ADC Manufacturing — Step 2 (AI-Automated Factory)
**Location:** 14th Street & Highway 90, New Iberia, LA
**Owner:** Advantage Design & Construction (ADC)
**Document:** Master Engineering Specification v2.0 (DSX PIVOT)
**Date:** 2026-03-20 (Updated from v1.0 2026-03-11)

---

## DSX PIVOT (March 2026)

**This spec has been updated post-GTC 2026.** Product pivoted from immersion-cooled GPU pods to **DSX-compliant facility modules** receiving NVIDIA standard liquid-cooled racks.

### Key Station Changes
- **S4 (Electrical)**: Now includes 800 VDC power distribution — adds complexity but is the industry standard for AI factories
- **S5 (Cooling)**: Renamed "Facility Water Loop." No immersion tanks or EC-110 coolant. Standard facility water plumbing for NVIDIA rack-level 45°C liquid cooling.
- **S6 (Compute)**: Renamed "Rack Receiving Bay + Network." No GPU sled insertion. Prepares mounting positions, power, water, and network connections for NVIDIA racks that install at customer site.
- **S7 (Test)**: Infrastructure validation only. No GPU burn-in. Validates power (800 VDC), water loop (flow, pressure, thermal), and network (throughput).

### Economic Impact
- Faster cycle time (37-43 hrs vs 41 hrs) — water loop simpler than immersion
- Lower material cost (~$3-6K/module savings from EC-110 elimination, partially offset by 800 VDC components)
- Higher throughput: 10-14 modules/month (up from 8-12)
- Selling price unchanged ($180K avg) — value is in DSX compliance, not cooling method

---

## 1. SITE

| Item | Detail |
|------|--------|
| Address | 14th Street & Highway 90, New Iberia, LA |
| GPS | Pending (site survey required) |
| Access | Direct Hwy 90 frontage — truck route to I-10 |
| Gas Pipeline | ON PROPERTY — existing pipeline corridor along Hwy 90 |
| Zoning | Industrial (verify M-1/M-2 with Iberia Parish) |
| Utilities | Entergy/CLECO grid, municipal water/sewer |

### Site Advantages
- Gas pipeline on-property eliminates fuel transport cost
- Highway 90 provides direct truck access to I-10 (east to Baton Rouge/New Orleans, west to Lafayette/Houston)
- Large footprint allows future expansion
- Industrial zoning — no residential buffer issues
- Iberia Parish has existing industrial workforce (oil & gas, manufacturing)

---

## 2. BUILDING

| Item | Detail |
|------|--------|
| Type | Pre-engineered metal building (PEMB), clear span |
| Footprint | 52,800 SF (240 ft × 220 ft) |
| Production Hall | 40,000 SF (200 ft × 200 ft), 32 ft clear height |
| Test Cell | 2,400 SF (isolated, soundproofed) |
| Control Room | 1,800 SF (overlooks production floor, glass wall) |
| Power Plant | 1,800 SF (gensets, switchgear, ATS) |
| Battery Room | 1,400 SF (battery storage, solar inverters) |
| Material Storage | 2,600 SF (climate-controlled) |
| Office/Break | 1,800 SF |
| Truck Docks | 3 receiving bays (north), 2 shipping bays (south) |
| Roof | Standing seam metal + solar array (750 kW) |
| Foundation | 8" reinforced concrete slab, 5,000 PSI, 32"×32" footings for robot bases |
| Fire Suppression | Wet sprinkler (production), Novec 1230 (battery room, control room) |
| HVAC | Factory: 10× rooftop units + exhaust fans. Office: mini-split. Control room: precision cooling. |
| Crane | 10-ton overhead bridge crane, full production hall coverage |

### Structural Notes
- Robot base plates require 32"×32" isolated concrete footings, 5,000 PSI, with J-bolt anchors
- CNC plasma table requires 10'×6' isolated slab section to prevent vibration transfer
- Test cell has 6" acoustic wall separation from production hall
- Overhead crane rated for full container weight (empty 20ft container = ~5,000 lbs)
- All floor drains in water loop station (S5) tied to water recovery system, NOT sewer

---

## 3. PRODUCTION FLOW

### U-Flow Layout

Containers enter from the north (receiving dock) and travel through 7 stations in a U-pattern:

```
                RECEIVING DOCK (3 bays)
                ┌─────────────────────────────────────────┐
                │                                         │
    ┌───────────┤  S1: RECEIVING     S2: CNC/FAB    S3: INSULATION  │
    │           │  & CONTAINER PREP  & WELDING       SPRAY FOAM     │
    │           │                                         │
    │  GAS      │─────────→──────────→──────────→─────────│
    │  PIPELINE │                                    │    │
    │           │                                    ▼    │
    │           │                                         │
    │           │  S6: COMPUTE       S5: COOLING     S4: ELECTRICAL  │
    │           │  INSTALL           SYSTEM          PANELS/WIRING   │
    │           │                                         │
    │           │←─────────←──────────←──────────←────────│
    │           │  │                                      │
    │           │  ▼                                      │
    │           │  ┌─────────────┐  ┌──────────┐  ┌─────────────┐
    │           │  │ S7: TEST    │  │ CONTROL  │  │ POWER PLANT │
    │           │  │ CELL        │  │ ROOM     │  │ 2× G3516    │
    │           │  └─────────────┘  └──────────┘  └─────────────┘
    │           │  ┌─────────────┐  ┌──────────┐  ┌─────────────┐
    │           │  │ BATTERY +   │  │ OFFICE   │  │ MATERIAL    │
    │           │  │ SOLAR INV   │  │ & BREAK  │  │ STORAGE     │
    │           │  └─────────────┘  └──────────┘  └─────────────┘
    │           │                                         │
    │           └─────────────────────────────────────────┘
    │                               SHIPPING DOCK (2 bays)
    └── 2" service line from Hwy 90 pipeline corridor
```

### Material Flow
- **Overhead conveyor system** moves pods between stations on guided rails
- **10-ton bridge crane** handles initial container lift from truck to Station 1
- **AGVs** (Automated Guided Vehicles) move sub-assemblies and materials from storage to stations
- **Finished pod** exits via south shipping dock onto flatbed truck

### Cycle Time Per Station

| Station | Operation | Cycle Time | Limiting Factor |
|---------|-----------|-----------|-----------------|
| S1 | Container prep + CNC cut | 4 hours | Plasma cut time |
| S2 | Fabrication + welding | 6 hours | Weld cycle count |
| S3 | Insulation + cure | 3 hours | Foam cure time |
| S4 | Electrical + 800 VDC | 8 hours | Connection count + DC distribution (bottleneck) |
| S5 | Facility water loop | 5 hours | Pressure test hold |
| S6 | Rack receiving bay + network | 5 hours | Cable routing precision |
| S7 | Infrastructure test | 5 hours | 2hr thermal water test |
| **Total** | **End-to-end** | **36 hours (~4.5 shifts)** | **S4 is the bottleneck** |

**Improvement vs old spec:** 5 hours faster per module. Water loop simpler than immersion. No GPU burn-in (NVIDIA's responsibility). Rack bay prep simpler than GPU sled insertion.

**Throughput at 2 shifts/day, 4 days/week:**
- 1 module every 2–2.5 working days
- 10–14 modules/month depending on configuration complexity

---

## 4. STATION SPECIFICATIONS

### Station 1 — Receiving & Container Prep

**Purpose:** Receive shipping containers, inspect, position on assembly jig, CNC cut all penetration ports.

| Equipment | Model | Spec |
|-----------|-------|------|
| Robot #1 | Fanuc M-710iC/50 | 50kg payload, 2050mm reach. Container positioning. |
| Robot #2 | Fanuc M-710iC/50 | Hold/stabilize during CNC operations. |
| CNC Plasma | Hypertherm XPR300 | 300A, cuts up to 3" steel. Gantry-mounted. |
| Crane | 10-ton overhead | Lifts container from truck to Station 1 jig. |
| Vision | 2× Metropolis cameras | Container inspection (damage/corrosion) + cut quality verification. |
| Jig | Custom welded steel | Hydraulic clamps, self-leveling, precision-located stops. |

**Process:**
1. Crane lifts container from receiving dock to jig
2. Robot #1 positions container, hydraulic clamps engage
3. Robot #2 stabilizes while Hypertherm cuts ports per Omniverse cut file
4. Metropolis verifies all cuts: position (±2mm), edge quality, no burrs
5. Deburring pass (automatic) on all cut edges
6. Container advances to Station 2

---

### Station 2 — CNC Cutting & Fabrication

**Purpose:** All custom metalwork — brackets, rack mounts, conduit runs, structural reinforcements. Robotic welding of all internal framing.

| Equipment | Model | Spec |
|-----------|-------|------|
| CNC Plasma Table | Hypertherm XPR300 | 5'×10' table. Cuts brackets and mounts from steel plate stock. |
| Welding Robot | Fanuc Arc Mate 120iD | 6-axis, 1437mm reach. MIG/TIG capable. |
| Wire Feed | Lincoln Power Wave R450 | Multi-process: MIG, pulse MIG, TIG. |
| Vision | 2× Metropolis cameras | Weld inspection (porosity, undercut, bead width) + cut tolerance. |
| Material | Steel plate stock | 10-ga to 1/2" plate. Pre-cut BOM from Omniverse. |

**Process:**
1. Omniverse generates cut file and weld sequence from pod model
2. CNC table cuts all parts from plate stock (nested for minimum waste)
3. Robot picks parts, positions inside container
4. Arc Mate welds per Isaac Sim-trained weld paths
5. Metropolis inspects every weld — X-ray quality visible-light analysis
6. Tolerance check: all dimensions within ±0.5mm (cut), ±1mm (weld)

---

### Station 3 — Insulation

**Purpose:** Closed-cell spray foam insulation on all interior surfaces. Vapor barrier application.

| Equipment | Model | Spec |
|-----------|-------|------|
| Spray Robot | ABB IRB 5500 | Hollow wrist (ideal for spray applications), 2.55m reach. |
| Barrier Robot | ABB IRB 2600 | 1.85m reach. Applies vapor barrier membrane sheets. |
| Foam System | Graco Reactor 2 E-XP2 | Heated proportioner, 2-component closed-cell SPF. |
| Vision | 2× Metropolis (visual + FLIR thermal) | Coverage verification + thermal uniformity scan. |

**Process:**
1. ABB IRB 5500 follows Omniverse-generated spray path
2. 3 passes for 3" total depth (R-21 insulation value)
3. 1-hour cure time (robot moves to next pod in pipeline)
4. ABB IRB 2600 applies vapor barrier membrane, heat-welds seams
5. Metropolis thermal camera scans entire interior — any cold spot >1°F delta flagged for re-spray
6. Coverage report generated and logged in Omniverse

---

### Station 4 — Electrical + 800 VDC Distribution (BOTTLENECK STATION)

**Purpose:** Main panels, 800 VDC power distribution, sub-panels, PDUs, bus bars, rack power connections. Human-robot collaborative station.

| Equipment | Model | Spec |
|-----------|-------|------|
| Cobot #1 | Universal Robots UR10e | 10kg payload, 1300mm reach. Panel mount + wire routing. |
| Cobot #2 | Universal Robots UR10e | Wire termination + torque application. |
| Human | Licensed Electrician | Code compliance oversight, 800 VDC safety, final sign-off. |
| Vision | 3× Metropolis cameras | Connection verification, wire color/gauge, torque values. |
| Panel | 400A main service + 800 VDC distribution | Sub-panels + PDUs + DC bus bars per module configuration. |

**This is the bottleneck station at 8 hours.** 800 VDC adds complexity — DC-rated components, arc flash analysis, NEC Article 712 compliance. The cobots handle repetitive routing while the electrician focuses on code-critical decisions and DC safety.

**Process:**
1. Cobot #1 mounts main panel, 800 VDC distribution, sub-panels, and PDUs per Omniverse layout
2. Cobot #2 routes wire through pre-installed conduit (from S2 framing)
3. Both cobots terminate wires — pre-programmed torque profiles per connector
4. 800 VDC bus bar assembly installed and torqued to spec
5. Electrician verifies all connections against NEC code (Article 712 for DC microgrids)
6. Metropolis photographs and logs every single connection (digital record)
7. Megger test on all circuits (AC and DC) before advancing

**Bottleneck Mitigation:**
- Future: Add 3rd cobot dedicated to 800 VDC bus bar assembly
- Future: Pre-fabricate wire harnesses at Station 2 (parallel path)
- Future: Pre-fabricate 800 VDC bus bar assemblies off-line
- Future: Automated wire labeling and heat-shrink station

---

### Station 5 — Facility Water Loop

**Purpose:** Plumb facility water supply/return for NVIDIA rack-level liquid cooling. CDU connection points. Heat rejection interface. Temperature and flow sensors.

| Equipment | Model | Spec |
|-----------|-------|------|
| Robot | Fanuc CRX-25iA | 25kg payload, 1889mm reach. Collaborative. CDU positioning + pipe handling. |
| Pipe System | Automated threading + fitting | Pre-measured pipe from Omniverse BOM. Robotic torque. |
| Sensors | Temperature + flow | Inline sensors for monitoring water loop performance. |
| Vision | 3× Metropolis cameras | Leak detection, fitting torque verification, sensor placement. |

**Process:**
1. CRX-25iA positions CDU connection manifolds at each rack receiving bay
2. Automated pipe system threads, cuts, and fits all water supply/return lines (45°C hot water)
3. Install isolation valves, flow meters, temperature sensors at each branch
4. All fittings torqued to spec by robotic wrench (logged)
5. System pressurized to 45 PSI, held 30 minutes
6. Metropolis monitors for any pressure drop >0.5 PSI (leak detection)
7. System flushed and filled with treated water

**Note:** Simpler than old immersion station — no EC-110 coolant, no immersion tanks, no dielectric fluid handling. Standard facility water plumbing with automated threading.

---

### Station 6 — Rack Receiving Bay + Network

**Purpose:** Install rack mounting positions, pre-route power/water/network to each bay. Prepare infrastructure for NVIDIA liquid-cooled racks that install at customer site.

| Equipment | Model | Spec |
|-----------|-------|------|
| Robot #1 | Fanuc CRX-25iA | Rack mount hardware placement on vibration-damped mounts. |
| Robot #2 | Fanuc CRX-25iA | 800 VDC power cable routing to each rack position. |
| Cobot | Universal Robots UR10e | Network cable management — route, bundle, terminate. |
| Vision | 3× Metropolis cameras | Mount alignment, cable routing, connector seating. |
| Network | InfiniBand or 400GbE | All cables pre-made to Omniverse-specified lengths. Customer spec. |

**Process:**
1. CRX-25iA #1 installs rack mounting hardware on damped floor mounts (±2mm tolerance)
2. CRX-25iA #2 routes 800 VDC power cables and water loop connections to each rack position
3. UR10e routes all network cables per Omniverse cable map (InfiniBand or 400GbE per customer spec)
4. UR10e terminates all connections with calibrated crimping tool
5. Metropolis verifies every connector is fully seated (vision data)
6. Metropolis checks cable bend radius — flags any below minimum spec
7. All rack positions labeled and connection points documented

**Note:** ADC does NOT install NVIDIA racks in the factory. The module ships with prepared infrastructure. NVIDIA liquid-cooled racks arrive at the customer site and drop into the prepared bays (2-hour install per rack).

---

### Station 7 — Infrastructure Test Cell

**Purpose:** Full infrastructure validation — power (AC + 800 VDC), water loop, network. Module-level QA. No GPU burn-in (NVIDIA validates their own racks at customer site).

| Equipment | Model | Spec |
|-----------|-------|------|
| Vision Array | Metropolis 8-cam thermal + 4 visible | AI-trained on known-good infrastructure thermal signatures. |
| Power | Facility power connection + 800 VDC test supply | Full module infrastructure load. |
| Water | Test rig (pump + heater) | Simulates NVIDIA rack heat load at 45°C. |
| Network | InfiniBand or 400GbE test connection | Throughput + latency validation per customer spec. |
| Monitoring | Omniverse real-time dashboard | Every sensor value displayed in digital twin. |

**Test Sequence (5 hours):**

| Phase | Duration | Test |
|-------|----------|------|
| 1. Power-On Self-Test | 15 min | All AC + 800 VDC circuits energize, no faults |
| 2. 800 VDC Load Test | 30 min | Full DC distribution under simulated rack load |
| 3. Network Validation | 30 min | All ports active, throughput verified, latency <1ms |
| 4. Water Loop Cold Test | 30 min | Flow rate, pressure, leak check at ambient temp |
| 5. Water Loop Thermal Test | 2 hours | Run water at 45°C, verify no leaks under thermal expansion, check all joints |
| 6. Sensor Validation | 15 min | All temperature sensors, flow meters, pressure gauges reading correctly |
| 7. Cooldown + Final Scan | 15 min | Thermal decay analysis, visual inspection |
| 8. QA Sign-Off | 45 min | Report generation, infrastructure certificate, ship prep |

**Pass Criteria:**
- All AC and 800 VDC circuits pass under load with no faults
- Water loop maintains pressure at 45°C for 2 hours with zero leaks
- Flow rate within ±5% of design spec at all rack positions
- All network ports pass throughput test
- All sensors reading within calibration range
- Zero electrical faults during entire sequence
- **Target: 98% first-pass yield**

---

## 5. ROBOT INVENTORY

| # | Model | Station | Task | Payload | Reach |
|---|-------|---------|------|---------|-------|
| 1 | Fanuc M-710iC/50 | S1 | Container positioning | 50 kg | 2050 mm |
| 2 | Fanuc M-710iC/50 | S1 | Container stabilization | 50 kg | 2050 mm |
| 3 | Hypertherm XPR300 (gantry) | S2 | CNC plasma cutting | — | 5'×10' table |
| 4 | Fanuc Arc Mate 120iD | S2 | Robotic welding | 25 kg | 1437 mm |
| 5 | ABB IRB 5500 | S3 | Spray foam application | 13 kg | 2550 mm |
| 6 | ABB IRB 2600 | S3 | Vapor barrier install | 12 kg | 1850 mm |
| 7 | Universal Robots UR10e | S4 | Panel mount + wire route | 10 kg | 1300 mm |
| 8 | Universal Robots UR10e | S4 | Wire termination | 10 kg | 1300 mm |
| 9 | Fanuc CRX-25iA | S5 | CDU positioning + pipe handling | 25 kg | 1889 mm |
| 10 | Auto Pipe System | S5 | Pipe thread + fit (water loop) | — | — |
| 11 | Fanuc CRX-25iA | S6 | Rack mount hardware placement | 25 kg | 1889 mm |
| 12 | Fanuc CRX-25iA | S6 | 800 VDC + water routing to rack positions | 25 kg | 1889 mm |
| 13 | Universal Robots UR10e | S6 | Network cable management | 10 kg | 1300 mm |
| 14 | Metropolis Vision Array | S7 | Automated infrastructure QA (12 cameras) | — | — |

**Total: 14 robotic systems across 7 stations**

### Robot Brands Selected (and Why)

- **Fanuc M-710iC** (S1, S2): Heavy-duty industrial. Proven in automotive. Handles container weight.
- **Fanuc Arc Mate 120iD** (S2): Purpose-built welding robot. Best-in-class path accuracy.
- **ABB IRB 5500** (S3): Hollow wrist designed specifically for spray painting/coating. Perfect for foam.
- **Universal Robots UR10e** (S4, S6): Collaborative — works beside humans safely. Ideal for electrical where an electrician must be present.
- **Fanuc CRX-25iA** (S5, S6): Collaborative + 25kg payload. Gentle enough for precision placement, strong enough for server racks.

---

## 6. NVIDIA TECHNOLOGY STACK

### Omniverse — Factory Digital Twin

The entire factory exists as a real-time digital twin in NVIDIA Omniverse before any physical construction begins.

**Design Phase:**
- Full building model (OpenUSD) with structural, mechanical, electrical
- Robot reach envelopes verified — no collisions, no dead zones
- Material flow simulation — find bottlenecks before they're built
- Solar roof angle optimization for New Iberia latitude (30.0°N)

**Build Phase:**
- Construction progress tracked against digital model
- Robot base plate locations verified by survey against Omniverse coordinates
- As-built deviations flagged in real-time

**Operate Phase:**
- Live sensor data from all 22 cameras + robot controllers fed into twin
- Real-time production status visible in control room
- Predictive maintenance — AI flags robot joints approaching wear limits
- Production optimization — AI adjusts scheduling to reduce bottleneck wait times

### Isaac Sim — Robot Programming

Every robot path is programmed and validated in Isaac Sim before running on physical hardware.

- **Weld paths** (S2): Simulated with thermal model to predict distortion
- **Spray paths** (S3): Simulated with fluid model to predict coverage and overspray
- **Pick-and-place** (S1, S5, S6): Collision-free path planning with obstacle avoidance
- **Cable routing** (S4, S6): Optimal route planning with bend radius constraints
- **New pod model?** Reprogram all robots in simulation, validate, push to production. Zero downtime.

### Metropolis — AI Vision Quality Control

22 cameras across all 7 stations running NVIDIA Metropolis inference at the edge.

| Station | Cameras | AI Models |
|---------|---------|-----------|
| S1 | 2 | Container damage detection, cut quality |
| S2 | 2 | Weld defect classification, dimensional tolerance |
| S3 | 2 | Foam coverage mapping, thermal uniformity |
| S4 | 3 | Wire color/gauge verification, connection seating, torque |
| S5 | 3 | Leak detection (pressure), fitting quality, sensor placement |
| S6 | 3 | Rack mount alignment, cable routing, connector seating |
| S7 | 4+8 thermal | Infrastructure thermal analysis, water loop thermal expansion |

**Edge Inference:**
- NVIDIA Jetson AGX Orin at each station (7 units)
- Local inference <50ms latency — real-time pass/fail during operation
- Models trained on production data, retrained monthly via AI Enterprise
- All inspection images stored — complete digital quality record for every pod ever built

### AI Enterprise — Production Intelligence

- **Scheduling optimizer**: Balances station cycle times, minimizes idle time
- **Predictive maintenance**: Tracks robot joint wear, coolant pump vibration, power consumption trends
- **Defect root cause**: Correlates quality issues across stations — e.g., "weld defect at S2 correlates with plate thickness variation"
- **Energy optimizer**: Shifts high-power operations (welding, CNC) to peak solar hours when possible
- **Inventory forecasting**: Predicts material consumption, triggers reorders based on production schedule

---

## 7. POWER SYSTEM

### Architecture

```
                    ┌──────────────────────────────┐
                    │     SOLAR ROOF (750 kW)       │
                    │   768 panels × 475W            │
                    │   16 strings × 48 panels       │
                    └──────────┬───────────────────┘
                               │ DC
                    ┌──────────▼───────────────────┐
                    │  4× STRING INVERTERS (200kW)  │
                    │  + MPPT Controllers            │
                    └──────────┬───────────────────┘
                               │ 480V AC
    ┌──────────────────────────┼──────────────────────────┐
    │                          │                          │
    │  ┌───────────────┐  ┌───▼───────────┐  ┌──────────────────┐
    │  │ NAT GAS       │  │ MAIN          │  │ GRID CONNECTION   │
    │  │ GENSET #1     │──│ SWITCHGEAR    │──│ ENTERGY/CLECO     │
    │  │ CAT G3516H    │  │ 4000A 480V    │  │ ATS Failover      │
    │  │ 1.4 MW        │  │ 3-Phase       │  │                   │
    │  └───────────────┘  └───┬───────────┘  └──────────────────┘
    │  ┌───────────────┐      │
    │  │ NAT GAS       │      │
    │  │ GENSET #2     │──────┘
    │  │ CAT G3516H    │
    │  │ 1.4 MW        │
    │  └───────┬───────┘      ┌──────────────────────┐
    │          │              │  BATTERY STORAGE       │
    │          └──── 2" ──────│  500 kWh / 250 kW     │
    │          GAS PIPE       │  LFP Chemistry         │
    │          FROM           │  Peak Shaving           │
    │          HWY 90         └──────────────────────┘
    │          PIPELINE
    └──────────────────────────────────────────────────┘
```

### Power Budget

| Load | Demand | Notes |
|------|--------|-------|
| Robot arms (14 units) | 350 kW | Average 25 kW each during operation |
| CNC plasma table | 150 kW | Peak during cutting |
| Welding system | 100 kW | Peak during multi-pass welds |
| Overhead crane | 50 kW | Intermittent |
| HVAC + exhaust | 200 kW | Constant |
| Lighting | 60 kW | LED high-bay |
| Control room + IT | 30 kW | Constant |
| Test cell (full pod load) | 800 kW | When testing — biggest single load |
| Coolant pumps + compressed air | 100 kW | Constant during production |
| Miscellaneous | 60 kW | Charging, tools, etc. |
| **Total Peak** | **~1,900 kW** | **When test cell + welding + CNC simultaneous** |

### Gas Pipeline Tie-In

- **Source:** Existing natural gas pipeline corridor along Highway 90
- **Service Line:** 2" steel, ~200 ft from pipeline to power plant room
- **Meter:** Commercial gas meter (coordinate with pipeline operator)
- **Pressure:** Pipeline delivery ~60 PSI, regulated to 2-5 PSI at gensets
- **Consumption:** ~12,000 CFH at full load (both gensets)
- **Cost:** Henry Hub spot (~$2.50/MMBtu) — approximately $0.03/kWh generated
- **Permits:** Louisiana Dept of Natural Resources pipeline tap permit, Iberia Parish mechanical permit

### Solar Roof

- **Array:** 768 panels × 475W = 750 kW DC (STC)
- **Panel:** LONGi Hi-MO 6 (or equivalent Tier-1)
- **Mounting:** Standing seam clamp system (no roof penetrations)
- **Inverters:** 4× SolarEdge 200kW string inverters
- **Annual Production:** ~1,050 MWh (New Iberia solar resource: 4.8 kWh/m²/day)
- **Offset:** ~25% of annual factory energy consumption
- **ROI:** 4.5 years with 30% ITC + Louisiana solar tax credit

---

## 8. STAFFING

| Role | Count | Shift | Notes |
|------|-------|-------|-------|
| Plant Manager | 1 | Day | Overall operations, P&L |
| Omniverse Engineer | 1 | Day | Digital twin, robot programming, AI models |
| Robot Operators | 4 | 2/shift | Monitor and intervene on robot stations |
| Licensed Electrician | 2 | 1/shift | Station 4 oversight + code compliance |
| QA Technician | 2 | 1/shift | Test cell operation + final sign-off |
| Pipe Fitter | 2 | 1/shift | Station 5 oversight + pressure test |
| Material Handler | 2 | 1/shift | Receiving, storage, station supply |
| Logistics Coordinator | 1 | Day | Shipping, scheduling, inventory |
| Maintenance Tech | 2 | 1/shift | Robot maintenance, facility upkeep |
| **Total** | **17** | | |

### Shift Schedule
- **2 shifts × 10 hours** (6:00–16:00, 16:00–02:00)
- **Monday through Thursday** (4 × 10)
- Friday available for maintenance, training, and overtime surge

---

## 9. ECONOMICS

| Item | Value |
|------|-------|
| **Capital Cost** | |
| Land + site prep | $500K–800K |
| Building (52,800 SF PEMB) | $2.1M–2.6M |
| Robots + tooling (14 systems) | $1.8M–2.4M |
| NVIDIA stack (Omniverse, workstations, Jetson) | $250K–400K |
| Solar roof (750 kW) | $1.1M–1.4M |
| Gas gensets + switchgear | $800K–1.0M |
| Battery storage (500 kWh) | $250K–350K |
| Crane + conveyor | $300K–400K |
| Commissioning + contingency | $400K–600K |
| **Total Capital** | **$7.5M–10.0M** |
| | |
| **Operating Cost (Monthly)** | |
| Staff (17 people) | $180K |
| Materials (containers, steel, wire, coolant) | $120K |
| Energy (gas + grid backup) | $25K |
| Maintenance + consumables | $15K |
| Insurance + overhead | $20K |
| **Total Monthly OpEx** | **$360K** |
| | |
| **Revenue (Monthly at Capacity)** | |
| 12 modules × $180K average selling price | $2,160K |
| **Gross Profit** | **$1,800K/month** |
| **Annual Gross Profit** | **$21.6M** |
| **Capital Payback** | **~5 months at full capacity** |

---

## 10. TIMELINE

| Phase | Duration | Milestone |
|-------|----------|-----------|
| Site survey + soil test | 2 weeks | GPS coordinates confirmed, geotech report |
| Architecture + Omniverse design | 8 weeks | Full digital twin complete |
| Permitting | 6–8 weeks (parallel) | Building, electrical, gas, environmental |
| Foundation + steel erection | 10 weeks | Building dried in |
| Solar roof install | 3 weeks (parallel with interior) | Array energized |
| Gas pipeline tap + genset install | 4 weeks | Power system operational |
| Robot installation + calibration | 6 weeks | All 14 systems operational |
| Metropolis camera install + AI training | 3 weeks (parallel) | Vision QA live |
| Omniverse integration + testing | 4 weeks | Digital twin synchronized |
| Trial production run (3 pods) | 3 weeks | First-article inspection |
| **Total** | **12–14 months** | **First production pod ships** |

---

## 11. PERMITS & COMPLIANCE

| Permit | Authority | Notes |
|--------|-----------|-------|
| Building permit | Iberia Parish | PEMB + foundation |
| Electrical permit | Iberia Parish | 4000A service, all station wiring |
| Mechanical/plumbing permit | Iberia Parish | Cooling systems, gas piping |
| Gas pipeline tap | LA Dept of Natural Resources | 2" service line from Hwy 90 corridor |
| Environmental (air) | LDEQ | Genset emissions — likely minor source permit |
| Fire marshal | State Fire Marshal | Sprinkler + Novec system review |
| ITEP application | Louisiana Economic Development | **FILE BEFORE GROUNDBREAKING** |
| Solar interconnect | Entergy/CLECO | Net metering or export agreement |
| OSHA compliance | Federal | Robot safety zones, lockout/tagout procedures |

**CRITICAL: ITEP (Industrial Tax Exemption Program) must be filed BEFORE any construction begins. 80% property tax abatement for 10 years on manufacturing equipment.**

---

## 12. FUTURE EXPANSION

### Phase 2 Additions (Year 2+)
- **3rd genset** — additional 1.4 MW for expanded test cell capacity
- **Automated wire harness station** — parallel to S4, pre-builds harnesses to break the bottleneck
- **2nd test cell** — doubles test throughput, enables 24/7 testing
- **Outdoor container staging yard** — 20-container buffer stock
- **Additional solar canopy** — parking lot solar, another 500 kW

### Phase 3 (Year 3+)
- **2nd production line** — mirror of Line 1, doubles output to 20+ pods/month
- **Battery lab** — in-house battery pack assembly for pods
- **R&D bay** — prototype new pod designs, test new cooling technologies

---

*This document is the engineering basis of design for the New Iberia Module Factory. All specifications subject to refinement during detailed engineering and Omniverse simulation.*

*ADC — Advantage Design & Construction*
*Mission Control — Document updated 2026-03-20 (DSX Pivot)*
