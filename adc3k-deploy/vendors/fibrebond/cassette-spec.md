# ADC Pure DC AI Factory — Cassette Specification
**For: Fibrebond (Eaton) Partnership Discussion**
Last updated: 2026-04-08
Status: DRAFT — Pre-Visit Working Document

---

## What This Is

A self-contained, factory-built modular AI compute unit — a cassette.
One cassette = one ADC 3K cassette = 10 NVL72 racks = 1.3 MW IT load.

The cassette arrives on site with DC power, liquid cooling, fire suppression, environmental control, and monitoring pre-integrated and factory-tested. Site provides: DC bus connection, gas line (Bloom), and fiber. Nothing else.

This is a product, not a construction project.

---

## Enclosure

- **Footprint:** 40-ft High Cube ISO external dimensions (40' × 8' × 9'6")
- **Construction:** Steel, purpose-built (not a shipping container converted — built to ISO external dims with ISO corner castings for crane and flatbed transport)
- **ISO corner castings:** Required — crane lift, flatbed, and stacking compatible
- **Access panels:** 8 hinged panels (4 per side), top-hinged — NEC clearance compliant
- **Penetrations (factory-installed):**
  - DC bus entry (1500V rated, Stage 1d compliant)
  - Cooling supply/return loops (Staubli UQD ports, capped at factory)
  - Fiber/network conduit
  - Munters fresh air intake + exhaust
  - Fire suppression agent lines
  - Sensor/BMS conduit
- **Structural floor:** Rated for NVL72 rack point loads (OCP Open Rack V3 spec)
- **Thermal insulation:** Spray foam, R-19 minimum — Louisiana ambient (95°F+ design day)

---

## IT Load & Power Summary

| Parameter | Value |
|-----------|-------|
| Racks | 10 × NVIDIA NVL72 (OCP ORV3) |
| IT load per rack | 130 kW |
| Total IT load | 1,300 kW |
| Target PUE | ≤ 1.15 |
| Total facility draw | ~1,495 kW (~1.5 MW) |
| DC bus input voltage | 800V DC (OCP Stage 1d, 1500V rated) |
| DC bus input current | ~1,875A @ 800V |

---

## Power Distribution — Eaton Stack

### DC Bus Interface
- Input: 800V DC from site Bloom SOFC bus (N+1)
- Bus rated to OCP Stage 1d: operating 800V, rated 1500V
- No AC conversion inside the cassette. No inverters. No rectifiers.

### Eaton ORV3 Sidecar Power Distribution
- One ORV3 sidecar per rack row (800 kW per sidecar)
- Two sidecars for 10-rack cassette (5 racks per row)
- ORV3 sidecar delivers ±400V DC to each NVL72 rack
- NVIDIA Kyber 64:1 LLC inside NVL72 steps down to 12V at GPU
- Supercapacitor fast-cycle backup integrated in sidecar
- Eaton co-designed with NVIDIA for DSX compliance

### Busbar Distribution
- 1500V-rated DC busbar backbone runs the length of the cassette
- Sidecar tap points factory-installed at each rack bay
- Grounding per OCP and NEC DC requirements

---

## Liquid Cooling — Boyd / Eaton Stack

### CDU (Cooling Distribution Unit)
- **Unit:** Boyd CHx2000 CDU
- **Capacity:** 2,000 kW — covers all 10 racks with headroom
- **Redundancy:** N+1 pump configuration
- **Reliability:** Six 9s (99.9999% uptime)
- **Location:** Factory-mounted in cassette mechanical bay (end of enclosure)
- **Connections:** Staubli UQD quick-disconnect couplings (NVIDIA-approved, OCP-compliant, drip-free) at each rack

### Cooling Loop
- Facility-side: coolant supply/return ports (Staubli UQD) capped at cassette exterior
- Internal: primary loop CDU → rack manifold → each NVL72 rear-door heat exchanger
- Secondary loop: CDU → external dry cooler / BAC TrilliumSeries adiabatic cooler (site-provided)
- Supply temp target: ≤ 45°C
- Return temp: ~55-60°C
- Leak detection: TraceTek sensing cable runs full loop length

### Quick-Disconnects
- Staubli UQD at every rack — drip-free disconnect for hot-swap
- Staubli UQD at cassette wall penetration — site connects here, nothing spills

---

## Environmental Control — Munters

### Desiccant Dehumidification
- **Unit:** Munters HCD or MCD series desiccant wheel
- **Purpose:** Louisiana ambient RH 75-80% — must dehumidify before air contacts any electronics
- **Process:** Incoming fresh air → Munters desiccant wheel → conditioned air → cold aisle
- **Regeneration heat source:** Waste heat from cooling loop (closed loop, no energy penalty)
- **Target RH inside cassette:** ≤ 50% at all times

### Airflow
- Cold aisle / hot aisle containment inside cassette
- Racks face inward, hot exhaust contained and directed to CDU return
- No mixing of hot and cold air inside enclosure
- Positive pressure maintained via Munters supply — no unfiltered outside air ingestion

---

## Fire Suppression

### Detection — VESDA
- **Unit:** Honeywell VESDA-E VEU aspirating smoke detector
- **Coverage:** 4 sampling points per pipe, full cassette coverage
- **Response:** Pre-alarm at trace smoke levels — catches fire before it starts
- **Integration:** BMS alert + suppression system trigger

### Suppression — Clean Agent
- **Agent:** Ansul Sapphire Novec 1230 (FK-5-1-12)
- **Why:** Electronics-safe, zero residue, no GPU damage, no CO2 hazard to personnel
- **Design:** Total flood — sealed enclosure enables full agent concentration
- **Enclosure integrity:** Door fan test required at commissioning (AHJ sign-off)
- **Cylinders:** Factory-mounted in mechanical bay, manifolded to nozzle array above rack tops
- **Manual abort:** Pull station at each access panel

---

## Sensor Suite

| Sensor | Location | Qty |
|--------|----------|-----|
| RTD temperature | Rack inlet, rack outlet, CDU supply, CDU return, ambient | 8 |
| Pressure transducer | Cooling loop supply + return | 2 |
| Flow meter | CDU primary loop | 1 |
| RH sensor | Cold aisle, hot aisle, outside air | 3 |
| Leak detection (TraceTek) | Under CDU, under rack row, at penetrations | 3 zones |
| Smoke (VESDA sampling) | Full cassette | 4 points |
| Door contact | Each access panel | 8 |
| Power meter | DC bus input, per sidecar | 3 |

---

## BMS / Edge Controller

- **Unit:** NVIDIA Jetson AGX Orin (275 TOPS)
- **Function:** Real-time sensor aggregation, cooling PID control, alarm management, BMS dashboard
- **Connectivity:** Fiber to site NOC, local display port at cassette panel
- **Data:** All sensor telemetry logged, streamed to Mission Control HD
- **Alerts:** Temperature, humidity, leak, smoke, power anomaly — all auto-escalate

---

## Network Fabric

- **Rack-to-rack:** NVIDIA InfiniBand (NVL72 native — 400 Gb/s)
- **Spine switch:** NVIDIA QM9700 (NDR InfiniBand) — factory-mounted in network bay
- **Management:** 1 GbE management network, isolated VLAN
- **External:** 2× single-mode fiber penetrations at cassette wall (site provides fiber run)
- **All cabling:** Factory-terminated and tested before shipment

---

## Rack Layout — Interior

```
[ACCESS PANEL]  [ACCESS PANEL]  [ACCESS PANEL]  [ACCESS PANEL]
|                                                              |
|  RACK  RACK  RACK  RACK  RACK | RACK  RACK  RACK  RACK  RACK|
|  [1]   [2]   [3]   [4]   [5] | [6]   [7]   [8]   [9]  [10] |
|  ORV3 SIDECAR (5 racks)       | ORV3 SIDECAR (5 racks)      |
|                HOT AISLE CONTAINMENT                         |
|  CDU + MECHANICAL BAY    |    NETWORK BAY                    |
|                                                              |
[ACCESS PANEL]  [ACCESS PANEL]  [ACCESS PANEL]  [ACCESS PANEL]
```

- Racks in two rows of 5, facing each other (cold aisle center)
- Hot exhaust directed to CDU return plenum
- Mechanical bay: CDU, suppression cylinders, Munters unit, BMS controller
- Network bay: InfiniBand spine switch, fiber patch, management switch
- DC bus penetration: one end
- Cooling penetration: same end as DC bus (all site connections at one face)

---

## Site Interface Spec (What the Site Provides)

| Item | Spec |
|------|------|
| DC power | 800V DC bus, 1,875A continuous, 1500V insulation rated |
| Cooling | Coolant supply ≤ 45°C, return capacity 1,300 kW, Staubli UQD |
| Fiber | 2× single-mode OS2, LC connectors, terminated to patch panel |
| Pad | Level concrete pad, load-rated for cassette + rack point loads |
| Crane | 40-ton minimum for placement |

**That's it. Nothing else.** Cassette is self-contained from those four connections.

---

## Scale Model

| Scale | Cassettes | Racks | GPUs | IT Load |
|-------|-----------|-------|------|---------|
| MARLIE 1 (proof of concept) | 4 | 40 | 2,880 | 5.2 MW |
| Trappeys Phase 1 | 5 | 50 | 3,600 | 6.5 MW |
| Trappeys Full | 50 | 500 | 36,000 | 65 MW |
| New Iberia | 154 | 1,540 | 110,880 | 200 MW |

---

## MARLIE 1 — Proof of Concept Path

1. ADC builds first cassette internally at MARLIE 1 (40-ft HC from GTI Fabrication, manual assembly)
2. Live production load — real customers, real revenue, real performance data
3. Engineering corrections made in the field
4. Locked spec handed to Fibrebond (Eaton) for factory production
5. Fibrebond produces at scale in Minden, LA — 90 min from Lafayette
6. Every future site receives factory-tested cassettes — no field assembly

---

## Open Items for Fibrebond Discussion

1. Can Fibrebond build to ISO external dimensions with ISO corner castings (not standard shipping container)?
2. Boyd CDU — factory-integrated or field-installed? Eaton owns Boyd — single PO possible?
3. Eaton ORV3 sidecar — can it be factory-mounted and tested before shipment?
4. Munters integration — Fibrebond experience with desiccant units in modular builds?
5. 1500V DC insulation rating — current Fibrebond enclosure spec or requires engineering change?
6. Production capacity — how many cassettes per month at Minden once tooled up?
7. First article inspection — can ADC witness factory test before first shipment?
8. Lead time: first cassette after spec lock?

---

## Why Fibrebond / Why Now

- Only company in the country with enclosure + power distribution + liquid cooling under one roof (post-Boyd acquisition)
- Louisiana-based = Buy American, TAA compliant, no long-haul shipping
- Eaton DSX co-design with NVIDIA = cassette is already positioned for NVL72 from day one
- ADC is Fibrebond's first Pure DC AI Factory reference customer — that is on their wall forever
- Scale is real: if New Iberia builds 154 cassettes, that is a production contract, not a prototype

---

*This document is confidential — ADC internal use and Fibrebond direct discussion only.*
