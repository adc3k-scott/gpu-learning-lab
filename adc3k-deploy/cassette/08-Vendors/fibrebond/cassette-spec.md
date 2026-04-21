# ADC Pure DC AI Factory -- Cassette Specification
**For: Fibrebond (Eaton) Partnership Discussion**
Last updated: 2026-04-08
Status: DRAFT -- Pre-Visit Working Document

---

## Definition

One ADC Pure DC AI Cassette = one factory-built modular AI compute unit.
10 NVIDIA NVL72 racks. 2,300 kW IT load. 800V DC input. Liquid-first cooling. Factory-tested.

Site provides four connections: DC bus, cooling loop, fiber, concrete pad. The cassette is self-contained from those four points. Manufactured in Minden, Louisiana by Fibrebond, fully assembled and acceptance-tested before shipment.

---

## Enclosure

- **External form factor:** 40-ft High Cube ISO external dimensions (40' x 8' x 9'6") -- purpose-built steel enclosure to ISO dims, not a converted shipping container
- **ISO corner castings:** Required -- crane lift, standard flatbed/lowboy transport, 2-high stacking compatible
- **Layout:** Single row of 10 racks running the length of the enclosure. Mechanical bay at the left end. External connection panel at the right end. All utilities run overhead. Single-row layout places rack face toward one long wall with rear service access from the opposite side via access panels.
- **Access panels:** 8 hinged panels (4 per side), top-hinged -- NEC 110.26 DC clearance compliant. Side panels are the primary service access path; no internal walkable aisle required.
- **Penetrations (factory-installed at external connection end):**
  - DC bus entry (1500V rated, OCP Stage 1d compliant)
  - Cooling supply/return loops (Staubli UQD ports, capped at factory)
  - Fiber/network conduit (2x single-mode OS2)
  - Munters fresh air intake + exhaust
  - Fire suppression agent lines
  - Sensor/BMS conduit
- **Structural floor:** Rated for NVL72 rack point loads (OCP Open Rack V3 -- 1,360 kg per rack, concentrated on four leveling feet)
- **Thermal insulation:** Spray foam, R-19 minimum -- 95 deg F design day (ASHRAE 0.4% cooling design condition, Lafayette LA)
- **Ingress protection:** NEMA 3R minimum -- Louisiana ambient humidity (75-80% RH), rain, and wind-driven debris
- **Wind/seismic:** Anchored to concrete pad per ASCE 7-22 wind loads for Risk Category III, 150 mph basic wind speed (Louisiana Cat 4 hurricane zone). ISO corner casting anchor bolt pattern per Fibrebond structural engineering.
- **Stacking:** 2-high stacking permitted where pad is rated and stacking certification obtained -- doubles compute density per footprint
- **Transport:** Racks shipped empty from Minden. Server hardware installed on-site after cassette placement. Vibration/shock protection provisions for flatbed transport per Fibrebond spec.

---

## IT Load & Power Summary

| Parameter | Value |
|-----------|-------|
| Racks | 10 x NVIDIA NVL72 (OCP ORV3) -- Vera Rubin Max P |
| GPUs per rack | 72 x Vera Rubin (Rubin GPU + Vera CPU) |
| HBM per rack | 288 GB HBM4/GPU x 72 = 20.7 TB |
| IT load per rack | 230 kW |
| Total IT load | 2,300 kW (2.3 MW) |
| Target PUE | <= 1.05 |
| Total facility draw | ~2,415 kW (2,300 kW x 1.05 PUE) |
| Non-IT overhead | ~115 kW (CDU pumps, Munters, BMS, network, lighting) |
| DC bus input voltage | 800V DC (OCP Stage 1d, 1500V insulation rated) |
| DC bus input current | ~3,019A @ 800V (total facility draw / bus voltage) |
| Bus conductor sizing | ~3,774A nameplate (NEC 125% continuous load rule, NEC 210.19(A)(1)) |

---

## Power Distribution -- Eaton Stack

### DC Bus Entry and PDU
- DC bus enters at the external connection panel (right end of enclosure)
- **PDU cabinet** (Power Distribution Unit) located in mechanical bay at left end -- factory-installed, factory-wired
- Heavy DC cables run from PDU along the enclosure floor to the overhead busbar distribution system
- PDU provides: main disconnect, overcurrent protection (SSCB -- solid-state circuit breakers for microsecond DC fault response), metering, and distribution to ORV3 sidecars
- **Ground fault protection** per NEC 2023 Section 210.13(B) for disconnecting means rated >=1,000A

### 800V DC Overhead Copper Busbar
- Copper busbar rated 1500V insulation, sized for ~3,774A (NEC 125% continuous load)
- Runs overhead the full length of the rack row
- Factory-installed tap points at each rack bay + mechanical bay loads
- Vibration-isolated mounting from enclosure structure
- Grounding per OCP DCF LVDC v1.0 (TN-S or IT systems only -- no TN-C, no TT)
- Arc flash analysis required per NFPA 70E for DC systems -- labeling at all access points

### Eaton ORV3 Sidecar Power Distribution
- Three ORV3 sidecars per cassette (each rated 800 kW, total 2,400 kW capacity)
- Sidecar assignment: ORV3-A serves racks R1-R4 (920 kW), ORV3-B serves racks R5-R8 (920 kW), ORV3-C serves racks R9-R10 + mechanical loads (460 kW IT + ~115 kW mech = ~575 kW)
- **Capacity margin:** 2,400 kW sidecar capacity vs ~2,415 kW total facility draw. Net margin is <1%. Fibrebond to confirm whether mechanical loads (CDU pumps, Munters, BMS) are fed from ORV3 sidecars or from a separate branch off the main PDU. If sidecars feed IT only, margin is 100 kW (4.3%).
- ORV3 sidecar delivers +/-400V DC (bipolar) to each NVL72 rack
- NVIDIA Kyber power shelf steps down to 54V rack bus, then to point-of-load at GPU
- Supercapacitor fast-cycle backup integrated in sidecar (sub-millisecond GPU load spike buffering)
- Eaton co-designed with NVIDIA for DSX compliance

---

## Liquid Cooling -- Liquid-First Architecture

### Design Principle
Direct liquid cooling at GPU and HBM removes >80% of rack heat before air is involved. Residual heat (<20%) is managed through hot-aisle containment within the enclosure. PUE <= 1.05 is achievable only with liquid-first architecture -- air-cooled systems at 230 kW/rack cannot approach this.

### Overhead Cooling Distribution
- **Cold Coolant Supply Header** (blue) runs overhead the full length of the rack row -- factory-installed
- **Warm Coolant Return Header** (red/orange) runs overhead the full length -- factory-installed
- **Flexible drops** connect from overhead headers down to each rack via Staubli UQD quick-disconnects
- Flexible hose spec: rated for operating pressure + 2x safety factor, temperature rated to 70 deg C, bend radius per Staubli UQD routing requirements
- Overhead distribution eliminates under-floor infrastructure and simplifies rack replacement

### CDU (Cooling Distribution Unit) -- N+1 Pump Configuration
- **Unit:** Boyd CDU (2,000 kW liquid heat removal capacity)
- **Pump redundancy:** N+1 internal pump configuration -- either pump carries full cassette load
- **Required liquid capacity:** ~1,840 kW (230 kW x 10 racks x 80%)
- **CDU margin:** 2,000 kW capacity vs 1,840 kW required = 8.7% headroom
- **Pumps and heat exchanger** factory-mounted in mechanical bay (left end of enclosure)
- **Secondary loop:** CDU -> external dry cooler / BAC TrilliumSeries adiabatic cooler (site-provided)
- **Supply temp target:** <= 45 deg C to CDU primary side
- **Return temp:** ~55-60 deg C
- **Flow rate:** Sized for 10 racks at full load -- Fibrebond to confirm header diameter and pump capacity against NVL72 per-rack flow requirement (~130 LPM per rack, ~1,300 LPM total)

### Staubli UQD Quick-Disconnects
- Staubli UQD at every rack flexible drop -- drip-free disconnect for hot-swap without loop drainage
- Staubli UQD at cassette wall penetration (external connection panel) -- site loop connects here
- All Staubli connections factory-installed and pressure-tested before shipment

### Leak Detection
- TraceTek rope leak sensor cable runs full loop length per OCP Rope Leak Sensor Base Specification R1.0.0
- Zones: under CDU, under rack row, at all penetration points
- OCP spec defines: sensing conductor material, detection threshold, alarm output interface (dry contact to BMS), placement guidelines, fluid compatibility verification required for selected coolant

### Forward Path -- Two-Phase Dielectric Cooling
Current cassette uses single-phase water-glycol. Two-phase dielectric fluid (engineered fluorocarbons / HFOs per OCP Guidelines for Using Dielectric Heat Transfer Fluids in Two-Phase Cold Plate-Based Liquid-Cooled Racks) is the forward path for rack densities beyond 230 kW. Fibrebond to confirm: (a) overhead header dimensions and CDU bay can accommodate two-phase upgrade, and (b) fluid containment and recovery provisions to design in from day one.

---

## Environmental Control -- Munters

### Desiccant Dehumidification
- **Unit:** Munters HCD or MCD series desiccant wheel -- located in mechanical bay
- **Purpose:** Louisiana ambient RH 75-80% -- dehumidify before air contacts electronics
- **Process:** Incoming fresh air -> Munters desiccant wheel -> conditioned air -> rack row
- **Regeneration heat source:** Waste heat from cooling loop return (~55-60 deg C) -- no additional electrical draw for regeneration
- **Target RH inside cassette:** <= 50% (ASHRAE A1 recommended range: 20-80% non-condensing; <=50% target provides margin against condensation at 45 deg C supply water temp)

### Airflow
- Hot-aisle containment along the rack row -- hot exhaust directed to CDU return
- Positive pressure maintained via Munters supply -- prevents unfiltered outside air ingestion
- Side access panels sealed when closed -- panel gaskets maintain positive pressure envelope

---

## Fire Suppression

### Detection -- VESDA
- **Unit:** Honeywell VESDA-E VEU aspirating smoke detector
- **Air-sampling tubes:** Run overhead the full length of the enclosure
- **Coverage:** 4 sampling points per pipe, full cassette coverage per NFPA 76 Section 8.4 (Information Technology Equipment Rooms)
- **Response:** Pre-alarm at trace smoke levels -- detects thermal event before ignition
- **Integration:** BMS alert + suppression system trigger

### Suppression -- Clean Agent (Novec 1230)
- **Agent:** Ansul Sapphire Novec 1230 (FK-5-1-12)
- **Design:** Total flood -- sealed enclosure enables full agent concentration per NFPA 2001
- **Cylinder sizing:** Per NFPA 2001 design concentration calculation by licensed Fire Protection Engineer (FPE) based on enclosure net volume. Cylinders factory-mounted in mechanical bay, manifolded to overhead nozzle array.
- **Discharge time:** <= 10 seconds per NFPA 2001 Section 5.5
- **Hold time:** Minimum 10 minutes per NFPA 2001 Section 5.7
- **Enclosure integrity:** Door fan pressure test required at commissioning per NFPA 2001 Section 5.4.3 (AHJ sign-off)
- **Manual abort:** Pull station at each access panel

---

## Sensor Suite

| Sensor | Location | Qty |
|--------|----------|-----|
| RTD temperature | Rack inlet, rack outlet, CDU supply, CDU return, ambient | 10+ |
| Pressure transducer | Cooling loop supply + return, CDU | 4 |
| Flow meter | CDU primary loop | 2 |
| RH sensor | Cold aisle, hot aisle, outside air | 3 |
| Leak detection (TraceTek) | Under CDU, under rack row, at penetrations | 4 zones |
| Smoke (VESDA sampling) | Full cassette via overhead tubes | 4 points |
| Door contact | Each access panel | 8 |
| Power meter | DC bus input, per sidecar | 4 |

Signal conditioning for all sensors per OCP Signal Conditioner Standard Footprint Base Specification v1.0.0 -- standardized form factor and interface for BMS integration.

---

## BMS / Edge Controller

- **Unit:** NVIDIA Jetson AGX Orin (275 TOPS)
- **Function:** Real-time sensor aggregation, cooling PID control, CDU pump N+1 failover, alarm management, BMS dashboard
- **Connectivity:** Fiber to site NOC, local display port at external connection panel
- **Data:** All sensor telemetry logged and streamed to Mission Control (ADC site management)
- **Alerts:** Temperature, humidity, leak, smoke, power anomaly -- all auto-escalate to site NOC
- **Power:** 15-60W configurable -- fed from BMS branch, battery-backed for graceful shutdown telemetry

---

## Network Fabric

- **Rack-to-rack:** NVIDIA InfiniBand NDR (400 Gb/s per port, native to NVL72 compute fabric)
- **Spine switch:** NVIDIA QM9700 (NDR InfiniBand) -- factory-mounted in mechanical bay
- **Forward path:** Vera Rubin NVL72 ships with ConnectX-9 (NVLink 6, 800 Gb/s capable). Spine switch upgrade to Quantum-X800 XDR when cassette transitions to Vera Rubin hardware. QM9700 bay dimensions to accommodate XDR form factor.
- **Management:** 1 GbE management network, isolated VLAN
- **External:** 2x single-mode OS2 fiber at external connection panel (site provides run to NOC)
- **All cabling:** Factory-terminated and tested before shipment
- **DSX compliance:** Network bay layout and cable routing validated against NVIDIA DSX spec before shipment

---

## Enclosure Interior Layout

```
LEFT END                                                        RIGHT END
[MECHANICAL BAY         ] [====== SINGLE ROW -- 10 NVL72 RACKS ======] [EXT PANEL]

OVERHEAD: [800V DC BUSBAR =================================================>]
OVERHEAD: [COLD SUPPLY HEADER (blue) =====================================>]
OVERHEAD: [WARM RETURN HEADER (red)  =====================================>]
OVERHEAD: [VESDA SAMPLING TUBES + FIRE SUPPRESSION =======================>]

          [DROP][DROP][DROP][DROP][DROP][DROP][DROP][DROP][DROP][DROP]
           |     |     |     |     |     |     |     |     |     |
[CDU  ]   [R1]  [R2]  [R3]  [R4]  [R5]  [R6]  [R7]  [R8]  [R9] [R10]  [DC IN ]
[PUMPS]                                                                  [COOL IN]
[PDU  ]   [ORV3-A: 4 racks] [ORV3-B: 4 racks] [ORV3-C: 2 racks + mech] [FIBER  ]
[DEHU ]
[MUNTR]   [LEAK DETECT CABLE ============================================>]
[QM97 ]

[ACCESS PANELS x4 (LONG SIDE)]                [ACCESS PANELS x4 (LONG SIDE)]
```

- All site connections terminate at the external panel (right end) -- single-face connection
- Mechanical bay (left end): CDU, pumps/heat exchanger, PDU, Munters, QM9700 network switch
- Overhead utilities factory-installed: DC busbar, cooling headers, VESDA, fire suppression manifold
- Rack row services from overhead via flexible drops -- no under-floor infrastructure
- Heavy DC cables route from PDU along floor to overhead busbar tap points

---

## Site Interface Spec (What the Site Provides)

| Item | Spec |
|------|------|
| DC power | 800V DC bus, ~3,019A continuous (3,774A conductor nameplate), 1500V insulation rated |
| Cooling | Coolant supply <= 45 deg C, return capacity ~1,840 kW liquid + ~115 kW air-side, Staubli UQD at cassette wall |
| Fiber | 2x single-mode OS2, LC connectors, terminated to patch panel |
| Pad | Level concrete pad, load-rated for cassette + rack point loads, anchor bolt pattern per Fibrebond spec |
| Crane | 50-ton minimum for placement (Fibrebond to confirm loaded cassette weight -- see Open Items) |

**Four connections. Nothing else.** Cassette is self-contained from those four points.

---

## Power Source Architecture -- Fuel and Grid Agnostic

The cassette does not care what generates the 800V DC. The site interface spec is the only contract.

| Source | Path | Notes |
|--------|------|-------|
| Bloom SOFC | 800V DC native -> bus | Primary. 90-day delivery. No conversion. |
| FuelCell Energy MCFC | DC roadmap -> bus | Second platform. DC ship date TBD. |
| First Solar TR1 | 1500V DC strings -> DC-DC converter -> 800V bus | Offset. Louisiana-manufactured. |
| Natural gas | Bloom SOFC -> bus | Standard ADC site fuel. |
| MVAC grid | MV AC -> rectifier -> 800V DC -> bus | Grid-tied sites. Same cassette. |

Grid-optional operation eliminates the utility interconnect approval cycle -- a 12-18 month permitting path removed by design.

---

## Factory Acceptance Test Protocol

Every cassette runs the following before it leaves Minden:

| Test | Method | Pass Criteria |
|------|--------|--------------|
| Cooling loop pressure test | Hydrostatic at 1.5x operating pressure, 30-min hold | No leaks, no pressure drop >1% |
| DC bus insulation resistance | Megger test at 1500V DC per IEEE 43 | >= 1 MOhm per meter of busbar |
| Ground fault protection | Verify ground fault relay trips within rated time | Trip confirmed, reset verified |
| BMS sensor verification | All sensors powered, readings checked against calibration reference | All channels within +/-2% of reference |
| VESDA functional test | Introduce test aerosol at each sampling point | Pre-alarm triggers within 60 sec |
| Leak detection continuity | End-to-end continuity check all TraceTek zones | All zones pass, alarm output confirmed |
| Staubli UQD function | Connect/disconnect all quick-disconnects, flow test | No drips, no flow restriction |
| Fire suppression system check | Inspect cylinder pressure, nozzle clear, abort pull station | All checks pass (no agent discharge) |
| Door fan pressure test | NFPA 2001 enclosure integrity test | Hold time >= 10 min at design concentration |
| Door contact / access panel | All 8 panels cycled open/close, contact verified | All contacts switching, seal integrity confirmed |
| Network fabric | QM9700 powered, management VLAN verified, IB port test | All ports link up |
| Power meter calibration | Each power meter checked against NIST-traceable reference | Within +/-1% |

Signed factory acceptance test report ships with every cassette. ADC reserves right to witness first article factory test in person at Minden.

---

## Performance Summary

| Metric | Value | vs. Traditional |
|--------|-------|----------------|
| PUE | <= 1.05 | vs. 1.3-1.5 air-cooled |
| Liquid heat removal | >80% of rack heat via direct-to-chip | Air-cooled: 0% liquid path |
| Sustained GPU performance | Full TDP at Max P, no thermal throttle | Air-cooled: thermally limited above ~100 kW/rack |
| Time to compute | 30-60 days pad-ready to live | vs. 18-24 months traditional build |
| CDU redundancy | N+1 pumps, hot-swap capable | No planned cooling downtime |
| Power source | Any source meeting 800V DC interface spec | Fuel and grid agnostic |
| Manufacturing | Louisiana, factory-tested, signed FAT report | No field integration risk |

---

## Scale Model

| Scale | Cassettes | Racks | GPUs | IT Load |
|-------|-----------|-------|------|---------|
| MARLIE 1 (proof of concept) | 4 | 40 | 2,880 | 9.2 MW |
| Trappeys Phase 1 | 5 | 50 | 3,600 | 11.5 MW |
| Trappeys Full | 50 | 500 | 36,000 | 115 MW |
| New Iberia | 87 | 870 | 62,640 | 200 MW |

---

## MARLIE 1 -- Proof of Concept Path

1. ADC builds first cassette internally at MARLIE 1 -- manual assembly, live production load
2. Real customers, real revenue, real performance data
3. Engineering corrections documented in the field
4. Locked spec handed to Fibrebond for factory production
5. Fibrebond produces at scale in Minden -- 90 min from Lafayette
6. Every future site receives factory-tested cassettes -- no field assembly, no custom engineering per site

---

## Open Items for Fibrebond

1. Confirm buildable internal dimensions within 40-ft HC ISO external form factor for single-row 10-rack layout with mechanical bay. NVL72 rack depth is 1,068mm (~42 in). Single row leaves ~4.5 ft from rack rear to opposite wall -- confirm this meets NEC 110.26 working space for rear access on 800V DC equipment.
2. Boyd CDU (2,000 kW, N+1 pump config) -- confirm current product designation and lead time
3. Eaton ORV3 sidecar (800 kW rating) -- confirm rating and factory-mount feasibility. Clarify whether sidecars feed IT racks only, or IT + mechanical loads. If IT + mechanical, total draw (~2,415 kW) is within 1% of sidecar capacity (2,400 kW) -- margin insufficient.
4. Overhead cooling header material, pressure rating, diameter for ~1,300 LPM total flow, and factory installation method
5. Flexible drop hose spec (pressure, temp, bend radius) for overhead-to-rack cooling connections
6. Munters desiccant integration -- experience with waste-heat regeneration loop in modular builds? Regeneration requires ~55-60 deg C water -- confirm CDU return temp is sufficient.
7. 1500V DC insulation rating throughout -- current Fibrebond spec or requires engineering change?
8. Two-phase cooling readiness -- can enclosure accommodate future upgrade without structural retrofit?
9. Rope leak sensor (OCP R1.0.0) -- factory installation and pre-ship test protocol?
10. Novec 1230 cylinder sizing -- Fibrebond experience with total-flood clean agent in sealed enclosures of this volume? Cylinder storage in mechanical bay vs. external mount?
11. Production capacity -- cassettes per month at Minden once tooled? Lead time after spec lock?
12. 2-high stacking structural certification and wind load anchor spec for ASCE 7-22, 150 mph basic wind speed
13. Loaded cassette weight (enclosure + 10 empty racks + CDU + all mechanical) -- for crane spec and pad design
14. Single PO structure -- Eaton owns Boyd: can CDU + ORV3 sidecar + enclosure consolidate under one contract?

---

*This document is confidential -- ADC internal use and Fibrebond direct discussion only.*
*ADC contact: Scott Tomsu -- scott@adc3k.com -- (337) 780-1535*
