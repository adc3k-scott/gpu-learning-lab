# Cassette — INTERIOR DESIGN SPECIFICATION

**Document:** Cassette-INT-001
**Revision:** 1.3
**Date:** 2026-04-22
**Classification:** CONFIDENTIAL
**Status:** Released

**40 ft HC ISO AI Compute Cassette — Sealed, Unmanned, Stackable, Autonomous, No Air Conditioning, No Internal CDU**
3,300 kW Installed · 9 Compute Racks + 1 Control Rack + 5 Delta In-Row Power Racks · 648 GPUs
Onshore (Lafayette) + Offshore (Marine) Variants

**Prepared by:** Scott Tomsu · CEO / Chief Engineer
scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana

---

## TABLE OF CONTENTS

- §1  Design Philosophy — Sealed PG25 Appliance
- §2  Cassette Nameplate
- §3  Container Shell — 40 ft HC ISO Baseline
- §4  Onshore vs Offshore Variants — Delta Summary
- §5  Interior Geometry & Rack Layout
- §6  Rack Specification — Vera Rubin NVL72
- §7  Power Architecture — 480 V AC In, 800 V DC Internal
- §8  End Zones — ELEC and Service
- §9  Access Panel System — 12 Panels
- §10 External Connection Panel (ECP) Summary
- §11 Floor Routing — Primary Manifold and Power Tray
- §12 Overhead Routing — Sensors, Lighting, Fire
- §13 Primary PG25 Manifold Design
- §14 Leak Detection — TraceTek + Drip Management
- §15 Munters External Skid — DSS Pro
- §16 Fire Suppression — Ansul Novec 1230 + VESDA-E
- §17 Grounding, Bonding & EMI Shielding
- §18 Sensor Instrumentation — Full Schedule
- §19 Autonomous Run System — Jetson AGX Orin
- §20 Networking — InfiniBand + OOB + Starlink
- §21 Terminal & Junction Box Schedule
- §22 Maintenance UPS & Life-Safety Power
- §23 Structural & Seismic Anchoring
- §24 Marinization — Offshore Variant Deltas
- §25 Acoustic & Thermal Envelope
- §26 Commissioning & Sealed Pressure-Vessel Procedure
- §27 Service Access Choreography
- §28 Bill of Materials (by Class)
- §29 Open Items & Risks

---

## §1  DESIGN PHILOSOPHY — SEALED PG25 APPLIANCE

The Cassette is a sealed, unmanned, stackable AI compute module. It accepts defined inputs at a single External Connection Panel (ECP), delivers compute capacity internally, and rejects heat via a sealed primary PG25 coolant loop across that same ECP. There is no interior aisle. There is no HVAC for personnel. Not designed for human ingress. The pod is serviced exclusively via bolt-sealed access panels on the long sides and is designed to be stacked two high on marine deck or purpose-built onshore racking.

### The Three Rules

**Rule 1 — The ECP is the contract.** Nothing outside the Cassette reaches past the ECP. Nothing inside the Cassette makes assumptions about upstream equipment. The ECP schedule in §10 is the sole interface document. The ECP carries electrical + data at the ELEC end, PG25 coolant + Munters ducts at the opposite end. No chilled water inside the Cassette.

**Rule 2 — Everything inside is redundant, hot-swappable, or bolted-for-life.** There is no middle category. Hot-swap means manifold valves, UQDs, and sensor modules only. All rotating equipment — pumps, compressors, fans beyond rack — is external. This makes the Cassette a sealed pressure vessel.

**Rule 3 — Diagnosis before dispatch.** The on-pod BMS (NVIDIA Jetson AGX Orin, N+1 redundant, Service End Zone at P-6) is authoritative for Cassette state. External systems receive telemetry and issue high-level workload dispatch. The BMS executes protection and safety actions locally with zero network dependency.

### What the Cassette Is Not

- Not a data center in a box. There is no cold aisle, no hot aisle, no CRAC.
- Not human-occupiable. There is no safe method to work inside while energized.
- Not grid-dependent. The pod accepts 480 V AC 3-phase at the ELEC ECP; Delta in-row racks (R11–R15) convert to 800 V DC internally. The cassette has no utility-side awareness and is optimized for natural gas gensets or DC-native generation upstream of the external switchgear.
- Not a CDU. Heat rejection requires the external CDU skid per Cassette-CDUSKID-001. The cassette is a primary-coolant endpoint only.
- Not a rack enclosure. It is a platform for 9 Vera Rubin NVL72 compute racks, 1 control rack, and 5 Delta in-row power racks that operate as a single InfiniBand-scaled cluster.

### Sealed Pressure-Vessel Posture

The Cassette operates under sealed pressure-vessel discipline. All PG25 plumbing is factory-welded, X-ray inspected at critical joints, vacuum decay leak-tested, nitrogen-blanketed until commissioning fill, and then sealed for field life. Field commissioning is 48 hours, not 6–12 weeks. This is the submarine / ROV / satellite methodology applied to AI compute infrastructure.

---

## §2  CASSETTE NAMEPLATE

| Parameter                            | Value                                    |
|--------------------------------------|------------------------------------------|
| Enclosure                            | 40 ft HC ISO, CSC-plated                 |
| External dimensions                  | 12,192 × 2,438 × 2,896 mm (40' × 8' × 9'6") |
| Internal dimensions                  | 12,032 × 2,352 × 2,698 mm (39'5" × 7'8" × 8'10") |
| Rack positions                       | 15 (9 compute + 1 control + 5 Delta in-row power) |
| Compute racks                        | 9 (R1–R9, Vera Rubin NVL72, Oberon MGX 3rd gen) |
| Control rack                         | 1 (R10 — Quantum-X800 IB + storage + mgmt + Jetson) |
| Delta in-row power racks             | 5 (R11–R15, 660 kW each, 480V AC in, 800V DC out) |
| Installed power capacity             | 3,300 kW (5 × 660 kW, all active, parallel load-sharing) |
| Embedded BBU                         | 2,400 kW (5 × 480 kW, no separate compute UPS) |
| GPUs (compute racks only)            | 648 Rubin GPUs (1,296 dies, NVL72 tier) |
| Cassette IT load — NVL72 tier        | 1,080 kW (9 × 120 kW — compute racks R1–R9 only) |
| Cassette IT load — NVL144 CPX tier   | 1,440 kW (9 × 160 kW — compute racks R1–R9 only) |
| Control rack load (R10)              | ~25 kW (IB switches, NVMe, DPUs, mgmt, Jetson) — control overhead, not included in IT load |
| Cassette facility load — NVL72       | ~1,145 kW (IT + R10 control overhead + auxiliary/BMS + 2% Delta conversion loss) |
| Cassette facility load — NVL144 CPX  | ~1,526 kW (IT + R10 control overhead + auxiliary/BMS + 2% Delta conversion loss) |
| Cassette cooling demand (primary)    | ~1.0–1.4 MW (PG25)                      |
| Primary input                        | 480 V AC 3-phase at ELEC ECP; 800 V DC internal bus |
| AC primary current                   | 4,179 A/phase at installed capacity (3,300 kW) |
| DC internal bus                      | 800 V DC, 6,000 A rated busway           |
| Cold plate supply/return             | 45 °C / 55–60 °C (PG25)                 |
| Primary PG25 interface               | 2× Stäubli QBH-150 QDs at CDU-end ECP   |
| External CDU skid requirement        | Yes — per Cassette-CDUSKID-001           |
| PUE (cassette level)                 | ≤ 1.06 (PUE including external skid ~1.10–1.12) |
| Operating weight                     | 29,085 kg (preliminary — C-01 open)      |
| ISO 40-ft HC gross limit             | 30,480 kg                                |
| Mass margin to ISO limit             | 1,395 kg                                 |
| Access panels                        | 12 (6 per long side)                     |
| Interior occupancy                   | None — unmanned                          |
| Fire suppression                     | Novec 1230, 5.85% design concentration   |
| BMS                                  | NVIDIA Jetson AGX Orin (N+1 redundant), R10 control rack / Service End Zone |

---

## §3  CONTAINER SHELL — 40 FT HC ISO BASELINE

| Dimension                     | mm      | Notes            |
|-------------------------------|---------|------------------|
| Interior length               | 12,032  | 39'-5"           |
| Interior width                | 2,352   | 7'-8"            |
| Interior height               | 2,698   | 8'-10"           |
| Total interior volume         | 76.4 m³ |                  |
| Corner casting rating         | 4 × ISO (CSC) | Stackable 8-high empty |

Both variants start from a new-build 40-ft HC ISO container to CSC standard. Structural frame, corner castings, floor tie-downs, and lifting provisions are to standard.

Enclosure integrity requirement: container shell and all penetrations must pass pressure-decay integrity test at commissioning per ECP-001 §19 (100 Pa decay in 5 min onshore / 50 Pa offshore). Fire suppression enclosure integrity test per NFPA 2001 required before Novec 1230 charge. Final seal is a condition of pod release. (IEC 60529 IP54 is a dust/splash rating, not a gas-tightness criterion — it does not apply here.)

---

## §4  ONSHORE VS OFFSHORE VARIANTS — DELTA SUMMARY

| Parameter              | Onshore (Lafayette)        | Offshore (Marine)           |
|------------------------|----------------------------|-----------------------------|
| Painting               | 2-coat polyurethane        | 3-coat marine epoxy         |
| Hardware               | 304 SS (majority)          | 316L SS throughout          |
| Seals                  | EPDM                       | FKM (fuel-resistant)        |
| Panel fasteners        | Dzus quarter-turn          | 316L SS bolts + captive washers |
| Ambient rating         | −5 to +45 °C, 95% RH        | −10 to +45 °C, 100% RH salt spray |
| Shock rating           | Land transport (Class 2)    | Marine (Class 4) with lashing points |
| Ventilation seals      | Gasketed                   | IP67-gasketed + pressure test |

Offshore variant adds ~300 kg; operating weight becomes 29,385 kg. Still 1,095 kg margin to ISO limit.

---

## §5  INTERIOR GEOMETRY & RACK LAYOUT

### Zone Allocation

Interior 12,032 mm length is divided into four zones:

| Zone | Length (mm) | Purpose |
|------|-------------|---------|
| ELEC End Zone | 1,200 | 480 V AC landing, AC main disconnect, 5 feeder breakers, BMS network switch |
| Rack Zone | 9,332 | 15 rack positions (R1–R15) + manifolds |
| Service End Zone | 1,200 | BMS (in R10) + manifold termination + sensor concentration + PG25 QDs to ECP + Munters duct termination |
| Short-end wall allowances | 300 | 150 mm each short end for ECP housing depth |
| **Total** | **12,032 mm** | |

### Rack Zone Detail

Rack zone dimensions permit:

- **Manifold slack** — tapered manifold reducers fit the 9,332 mm run without compression
- **Service aisle width** — 300 mm working length at R1 end for maintenance access from Service End Zone

Rack spacing: 600 mm rack pitch, 9 compute (R1–R9) + 1 control (R10) + 5 Delta in-row power (R11–R15).

### Service End Zone

The Service End Zone contains:

| Item                              | Position                       | Notes |
|-----------------------------------|--------------------------------|-------|
| BMS (Jetson Orin N+1)             | R10 control rack, upper zone   | Accessible via Panel P-6 |
| Primary manifold termination header | Centerline, floor trench     | Final header expansion chamber before QD |
| PG25 supply QD plate              | Aft wall, centerline           | Stäubli QBH-150 supply QD (wetted surface inside, connector face at ECP) |
| PG25 return QD plate              | Aft wall, centerline (adjacent) | Same, return QD |
| Munters duct termination          | Aft wall, port side            | HVAC duct flange to ECP |
| TraceTek leak sensor concentrator | Starboard wall                 | Sensor cable terminations converge |
| Pressure & temperature gauges     | Below R10 rack                 | Local gauge panel for site tech |
| Service light (24 VDC)            | Overhead                       | For IR camera & maintenance use |
| Ceiling sensor cluster            | Centerline                     | VESDA sampling port, CO detector, smoke witness |

No rotating equipment, no air conditioning, no fluid pumps inside the Service End Zone. The zone exists to concentrate passive instrumentation and terminate manifolds.

---

## §6  RACK SPECIFICATION — VERA RUBIN NVL72

| Parameter                  | Value                                    |
|----------------------------|------------------------------------------|
| Rack standard              | NVIDIA MGX 3rd gen, Oberon 19"            |
| Height                     | 48U (2,200 mm overall frame)             |
| Width                      | 600 mm                                   |
| Depth                      | 1,200 mm                                 |
| NVL72 load (compute)       | 120 kW per rack                          |
| NVL144 CPX load            | 160 kW per rack                          |
| Primary coolant            | PG25 glycol, 45 °C supply                |
| Rack-level connection      | Stäubli UQD-25 (3 per side, supply + return) |
| DC primary input           | 800 V DC from internal busway (branch circuit per ELEC-001 §10) |
| Network                    | Quantum-X800 InfiniBand at R10 (control rack) |
| Storage + BMS              | DPU + NVMe servers + Jetson Orin at R10  |

See COOL-002 §4 for heat load derivation; see ELEC-001 for rack power architecture.

---

## §7  POWER ARCHITECTURE — 480 V AC IN, 800 V DC INTERNAL

480 V AC 3-phase enters the Cassette at the ELEC-end ECP (bus duct coupling, 4,179 A/phase at 3,300 kW installed capacity — open item E-01).

Inside the ELEC End Zone:
- 6,000 A AC main disconnect (motor-operated, NEC 125% of 4,179 A = 5,224 A minimum)
- Revenue meter (480 V AC, ANSI C12.20)
- 5× 1,200 A AC feeder breakers, one per Delta in-row power rack

Each feeder runs to one of 5 Delta 660 kW In-Row Power Racks (R11–R15):
- 6× 110 kW hot-swappable AC-DC shelves per rack
- Input: 480 V AC 3-phase (836 A/phase per rack)
- Output: 800 V DC
- Embedded BBU: 480 kW per rack (80 kW × 6 shelves), 2,400 kW total cassette

Delta rack 800 V DC outputs feed the internal DC busway (6,000 A rated, NEC 80% = 5,156 A minimum). The busway distributes to:
- R1–R9 compute racks via 200 A branch breakers (150 A per rack at NVL72 load)
- R10 control rack via branch breaker

800 V → 50 V DC/DC shelves installed in each compute rack (R1–R9) convert from busway voltage to GPU operating voltage. All 5 Delta in-row racks run simultaneously at parallel load-sharing. At 1,440 kW operating load, each rack runs at ~44% utilization. If one fails, remaining 4 carry the load at 55% — no service interruption.

Bender iso-PV1685 IMD monitors the internal 800 V DC ungrounded IT system continuously.

See ELEC-001 for full one-line diagram and sizing calculations.

---

## §8  END ZONES — ELEC AND SERVICE

### ELEC End Zone

| Parameter                | Value                                 |
|--------------------------|---------------------------------------|
| Length                   | 1,200 mm                               |
| Function                 | AC electrical landing, metering, distribution, E-stop |
| Contents                 | 480 V AC main disconnect (6,000 A) + 5× 1,200 A feeder breakers + revenue meter + SPD + network switch + E-stop + Starlink/5G junction |

### Service End Zone

| Parameter                | Value                                 |
|--------------------------|---------------------------------------|
| Length                   | 1,200 mm                              |
| Primary function         | Manifold termination + passive instrumentation (BMS in R10) |
| Heavy equipment          | None — all rotating equipment is external |
| Service interval         | None — no consumables inside          |
| Personnel access         | Not required during field life        |
| ECP connections          | 2× DN150 PG25 QD (Stäubli QBH-150 — IN-01 closed) |

### Panel Access to Service End Zone

Panel P-6 opens to Service End Zone and R10 control rack for BMS module access (hot-swap of Jetson modules). Access frequency expected: <2×/year for BMS maintenance. Not required for cooling system service — that happens at the external skid.

---

## §9  ACCESS PANEL SYSTEM — 12 PANELS

12 bolt-sealed access panels (6 per long side).

| Panel | Side | Zone              | Purpose                          |
|-------|------|-------------------|----------------------------------|
| P-1   | Port | ELEC End          | AC main disconnect + feeder breakers |
| P-2   | Stbd | ELEC End          | Network / Starlink               |
| P-3   | Port | Rack Zone fwd     | R1–R4 maintenance                |
| P-4   | Stbd | Rack Zone fwd     | R1–R4 mirror + Munters duct      |
| P-5   | Port | Rack Zone mid     | R5–R10 maintenance               |
| P-6   | Stbd | Service End       | R10 control rack / BMS access    |
| P-7   | Port | Rack Zone aft     | R11–R15 Delta rack maintenance   |
| P-8   | Stbd | Rack Zone aft     | R11–R15 Delta rack mirror        |
| P-9   | Port | Service End       | Manifold / leak detect           |
| P-10  | Stbd | Service End       | Munters duct access              |
| P-11  | Port | ELEC End          | E-stop + BMS aux                 |
| P-12  | Stbd | ELEC End          | Life-safety UPS / Starlink aux   |

### Fastener Schedule (Onshore / Offshore)

- Onshore: 12 Dzus quarter-turn latches per panel
- Offshore: 12 stainless 316L M10 bolts with captive washers per panel
- Seal: EPDM (onshore) / FKM (offshore), ≥6 years design life

### Safety Interlock

P-1 (AC main disconnect) has mechanical interlock with 480 V AC disconnect. Cannot open without breaker trip. All panels subject to electrical lockout-tagout when accessed.

---

## §10  EXTERNAL CONNECTION PANEL (ECP) SUMMARY

See Cassette-ECP-001 for detailed schedule. Summary for reference:

### ELEC End ECP

- 480 V AC 3-phase primary input (bus duct coupling, 4,179 A/phase — per open item E-01)
- BMS uplink (fiber × 4)
- E-stop (dual-contact 24 VDC)
- Starlink / 5G antenna pass-through
- Low-current Cam-Lok service taps (maintenance access only, not primary feed)

### CDU End ECP

| Penetration             | Spec                                  |
|-------------------------|---------------------------------------|
| Primary fluid #1        | PG25 supply — Stäubli QBH-150 QD      |
| Primary fluid #2        | PG25 return — Stäubli QBH-150 QD      |
| Munters supply duct     | 400 × 250 mm flange                   |
| Munters return duct     | 400 × 250 mm flange                   |
| InfiniBand pass-through | 3× MPO-24 bulkheads (uplink + downlink + redundant), 72 fibers total |
| Condensate drain        | DN40 with air gap                     |
| Test / vent port        | DN20 ball valve                       |

---

## §11  FLOOR ROUTING — PRIMARY MANIFOLD AND POWER TRAY

### Primary PG25 Manifold Trench

| Parameter              | Value                                    |
|------------------------|------------------------------------------|
| Trench location        | Side B (starboard), floor-integrated     |
| Trench dimensions      | 250 mm wide × 200 mm deep × 9,332 mm long |
| Cover                  | Removable floor grate, 4 × 25 mm bars   |
| Contents               | Primary supply manifold (DN125) + primary return manifold (DN125) + TraceTek leak cable |

Manifold headers tie to the termination headers in the Service End Zone which then connect through the PG25 QDs at the CDU-end ECP. See §13 for hydraulics.

### DC Power Tray (Internal)

| Parameter              | Value                           |
|------------------------|--------------------------------|
| Location               | Side A (port), overhead (2.4 m) |
| Type                   | Ladder tray, 600 × 150 mm      |
| Load                   | 800 V DC busway, 6,000 A rated  |

### AC Feeder Tray (ELEC End Zone to R11–R15)

| Parameter              | Value                           |
|------------------------|--------------------------------|
| Location               | ELEC End Zone floor-to-rack runs |
| Cable                  | 5× feeders, 2× 300 mm² per phase + 95 mm² G |
| Length                 | ~5 m per feeder                 |

---

## §12  OVERHEAD ROUTING — SENSORS, LIGHTING, FIRE

- Overhead cable tray (separate from power tray): BMS sensors, fire detection, lighting
- Linear LED lighting: service-only, manually switched from outside panel
- Novec 1230 distribution piping: 5× nozzles along centerline
- VESDA sampling ports: 8 ports distributed
- IR camera: single unit at Service End for health monitoring

---

## §13  PRIMARY PG25 MANIFOLD DESIGN

### Scope

This section covers the primary PG25 manifold system entirely inside the Cassette, from the rack branches through the trenched headers to the PG25 QDs at the CDU-end ECP. The intermediate loop, skid HX, and secondary water circuit are all external — see COOL-002.

### Primary Supply and Return Headers

| Parameter              | Value                                    |
|------------------------|------------------------------------------|
| Material               | 304L SS (onshore) / 316L SS (offshore)   |
| Diameter               | DN125 (125 mm bore)                       |
| Schedule               | Schedule 40                               |
| Design pressure        | 10 bar working, 15 bar hydrostatic        |
| Design temperature     | 5–70 °C                                   |
| Length                 | 9,000 mm (rack zone) + 1,000 mm (Service End Zone termination) |
| Joints                 | All-welded inside cassette (no serviceable joints) |
| Insulation             | 25 mm Aeroflex EPDM with aluminum jacket |

### Branch Laterals

Per compute rack (R1–R9):

| Parameter              | Value                                    |
|------------------------|------------------------------------------|
| Material               | Matched to headers (304L or 316L SS)     |
| Diameter               | DN40                                      |
| Connection to header   | Welded tee with full-port isolation valve |
| Connection to rack     | Stäubli UQD-25 (3 per side per rack)    |
| Design flow            | 159 LPM (NVL72) / 179 LPM (CPX)          |

Per control rack (R10):

| Parameter              | Value                                    |
|------------------------|------------------------------------------|
| Material               | 304L/316L SS                              |
| Diameter               | DN25                                      |
| Flow                   | ~20 LPM (R10 — IB switches + mgmt)       |

### QD Termination Plate (Service End Zone)

The two DN150 PG25 QDs at the CDU-end ECP are mounted on a single-piece 316L stainless plate, 300 × 600 × 20 mm, bolted to the Cassette aft interior wall and sealed with FKM gaskets. Penetration through the wall is TIG-welded and pressure-tested.

QDs pass through to the ECP outer recess where the flexible hoses from the skid mate. Connector model per §5 detail.

### Hydraulics

See COOL-001 §4–§5 for pressure drop budget, flow allocation per rack, and velocity analysis. This section only captures what's inside the Cassette; everything from the QD outward is in COOL-002.

---

## §14  LEAK DETECTION — TRACETEK + DRIP MANAGEMENT

- TraceTek cable in manifold trench (full 9,332 mm length)
- TraceTek cable in Service End Zone under QD termination plate (1,000 mm loop)
- TraceTek cable along branch laterals (aggregated to TTDM-128 in Service End Zone)
- TraceTek cable on ceiling drip tray (safety layer; expected never wet in normal operation)

Total TraceTek coverage: ~14 m wet-sensitive cable + 3 m bleed-sensitive cable.

The cassette carries a single-fluid PG25 system. TraceTek monitors for PG25 leaks only, which simplifies BMS sensor logic.

---

## §15  MUNTERS EXTERNAL SKID — DSS PRO

Munters DSS Pro desiccant dehumidifier — spec TBD pending vendor call. Product class confirmed correct for cassette duty (~70,000 m³/h range). Full spec to be filled in upon receipt of Munters selection report.

- Airflow capacity: TBD (DSS Pro class)
- Process air supply/return via 200 mm flanged ducts at CDU-end ECP
- Regen heat source: G3520K jacket water (CHP thermal path — interface TBD)
- Controls: Modbus TCP to cassette BMS
- Power feed: 480 V AC 3-ph at CDU ECP, ~25 kW running (spec TBD)

**Interior humidity design target: 10–38% RH** (per OCP Next-Generation ML Infrastructure Design Principles v0.5.0, Feb 2026 — applicable to both 2026 and 2028+ facility tiers). The Munters skid must be sized and controlled to maintain this range at maximum Cassette IT load. BMS setpoint and alarm thresholds must be set accordingly (see ECP-001 §9).

Open item MO-03: confirm DSS Pro model, airflow, FW coil ΔP, CHP regen interface, and moisture removal capacity required to maintain 10–38% RH interior at rated cassette load.

---

## §16  FIRE SUPPRESSION — ANSUL NOVEC 1230 + VESDA-E

Reference FIRE-001.

- Novec 1230 at 5.85% design concentration
- VESDA-E aspirating smoke detection with 8 sampling ports
- Release interlocked with BMS + operator dual-action
- Panel P-3 or P-5 preserves emergency access

---

## §17  GROUNDING, BONDING & EMI SHIELDING

Reference ELEC-001.

- Equipotential bonding throughout Cassette
- Single ground reference at ELEC End ECP
- EMI shielding at all cable tray crossings
- Bender iso-PV1685 IMD monitors ungrounded 800 V DC internal bus continuously

---

## §18  SENSOR INSTRUMENTATION — FULL SCHEDULE

### Sensor Summary (Per Cassette)

| Category                                | Count |
|-----------------------------------------|-------|
| Per-rack temperature (supply/return)    | 20    |
| Per-rack flow                           | 10    |
| Per-rack DC current                     | 10    |
| Per-rack vibration                      | 15    |
| Per-rack leak (integrated)              | 15    |
| Environmental (T/RH, pressure)          | 6     |
| Tilt / shock                            | 4     |
| Fire: VESDA sampling ports              | 8     |
| Electrical: bus V/I, IMD               | 6     |
| Breaker status (24 VDC)                 | 8     |
| UPS SoC                                 | 2     |
| Fluid: sump levels                      | 2     |
| Fluid: manifold pressure + temp         | 4     |
| PG25 QD pressure + temp at QD plate    | 4     |
| **Total per-cassette sensors**          | **114** |

Notes:
- Temperature, flow, and DC current sensors cover R1–R10 (9 compute + 1 control — cooled racks only).
- Vibration and leak sensors cover all 15 rack positions including Delta in-row power racks.

### Wiring

All sensors terminate at Advantech ADAM-6000 I/O modules in the Service End Zone / R10, networked via Ethernet to the BMS (Jetson Orin).

---

## §19  AUTONOMOUS RUN SYSTEM — JETSON AGX ORIN

### BMS Rack

| Parameter                       | Value                                    |
|---------------------------------|------------------------------------------|
| Location                        | R10 control rack, Service End Zone       |
| Rack size                       | 19" × 12U, within R10                   |
| BMS nodes                       | 2× NVIDIA Jetson AGX Orin 64 GB (N+1)    |
| Failover                        | Keepalived, <200 ms                       |
| Power                           | 24 VDC from life-safety UPS              |
| Cooling                         | None required (Orin low TDP, passive heatsink) |
| Network                         | 4× 1 Gbps Ethernet (redundant)           |
| OS                              | Ubuntu 22.04 LTS                          |
| Software stack                  | Telegraf → InfluxDB → MQTT → Kafka, TensorRT for inference |
| Uplink                          | Fiber to ELEC End ECP                    |

### Autonomous Functions

- Leak detection and isolation
- Thermal runaway protection
- Fire detection and suppression command
- Power quality alarm
- Panel-open interlock monitoring
- Predictive maintenance inference
- Workload-aware feedforward (per CTRL-001)

### Non-Autonomous (Supervisor Responsibility)

- Workload scheduling and dispatch
- Firmware updates (signed only)
- Operating mode transitions (initiated by orchestrator)

---

## §20  NETWORKING — INFINIBAND + OOB + STARLINK

- 3× MPO-24 bulkheads (uplink + downlink + redundant) at CDU-end ECP — 72 fibers total, originating at R10 Quantum-X800 switch
- Out-of-band management: dedicated Ethernet VLAN, separate from InfiniBand
- Starlink + 5G backup at ELEC End ECP
- BMS network isolated from data plane (OT/IT segmentation per CYBER-001)

---

## §21  TERMINAL & JUNCTION BOX SCHEDULE

- J-Box 01 (Service End Zone / R10): BMS power + sensor aggregation
- Total junction boxes: 15
- All boxes rated IP54 (onshore) / IP67 (offshore)

---

## §22  MAINTENANCE UPS & LIFE-SAFETY POWER

24 VDC maintenance UPS for BMS, leak detection, fire panel, emergency lighting. Runtime ≥ 5.6 hours from full charge (2 kWh LiFePO4 at 356 W peak load — see ELEC-001 §5 for full calculation). Compute racks have no separate UPS — covered by 2,400 kW embedded BBU in 5 Delta in-row power racks.

---

## §23  STRUCTURAL & SEISMIC ANCHORING

ISO 40-ft HC frame is the primary structure. All 15 rack positions bolted to floor rail inserts (M16 × 4 per rack = 60 anchor bolts total). No structural re-analysis triggered by current mass budget (1,395 kg margin to ISO limit).

**OCP facility floor requirements (deployment site responsibility):** OCP Next-Generation ML Infrastructure Design Principles v0.5.0 specifies ≥ 350 psf live load floor capacity and ≤ 6,000 lbs (2,722 kg) max rolling load per rack for large-scale ML facilities. Cassette rack rolling weight is estimated at 1,500 kg (3,307 lbs) per rack — within the 6,000 lb OCP rolling limit. The platform or facility deploying Cassette pods must provide ≥ 350 psf structural floor capacity. Confirm floor rating at each deployment site before rollout.

---

## §24  MARINIZATION — OFFSHORE VARIANT DELTAS

Offshore variant deltas per §4. Additional notes:

- Stäubli QBH-150 QDs specified with FKM seals for offshore
- PG25 QD plate 316L stainless
- Flexible hose to skid: Tema DryBreak alternative for subsea-rated deployments

---

## §25  ACOUSTIC & THERMAL ENVELOPE

| Parameter                                       | Value                             |
|-------------------------------------------------|-----------------------------------|
| Interior noise at BMS position (R10)            | ~55 dBA                           |
| Exterior noise at 1 m (cassette only)           | ~50 dBA                           |
| Combined noise (cassette + skid at 1 m)         | ~75 dBA (skid dominant)           |

Internal thermal envelope: no AC, no personnel occupancy, no forced air inside cassette.

---

## §26  COMMISSIONING & SEALED PRESSURE-VESSEL PROCEDURE

### Factory Commissioning

1. **Weld fabrication complete.** All primary PG25 piping, headers, branches, QD plate welds, and manifold joints finished.
2. **NDT inspection.** 100% visual inspection of all welds; 10% radiographic inspection of critical joints (manifold tees, QD plate, header terminations). Acceptance per ASME B31.3.
3. **Pneumatic proof test.** Pressurize primary loop (with QDs capped) to 15 bar air for 30 minutes. Soap test all welds. Zero leaks.
4. **Vacuum decay test.** Evacuate loop to 50 Pa absolute. Allow 5 minute stabilization. Monitor pressure rise. Acceptance: ≤ 50 Pa decay in 5 min.
5. **Nitrogen purge.** Vent vacuum with dry N₂ to 1.5 bar positive. Nitrogen blanket maintained through rack installation.
6. **Rack installation.** 9 compute racks + 1 control rack (R1–R10): UQDs mated at per-rack laterals. Each rack connection individually hydrostat-tested (local to branch) to 12 bar. 5 Delta in-row power racks (R11–R15): installed and AC feeders connected.
7. **Sensor and electrical commissioning.** Cable all sensors to ADAM modules. Energize BMS. Boot checkout.
8. **Initial PG25 fill.** Via dedicated fill port on QD plate. PG25 quality verified (pH 8.5–9.5, conductivity <500 µS/cm, visual clarity). Loop filled to ~180 L (Cassette interior only — skid portion filled at skid).
9. **Final seal.** Fill port sealed with blind cap, witnessed and inspected.
10. **QD caps installed.** Dust/moisture caps on exposed QD faces for shipping.
11. **Ship.** Cassette is a sealed unit from this point until site commissioning.

### Site Commissioning (48 Hour Target)

1. **Arrival inspection.** TraceTek integrity, QD cap integrity, no shipping damage.
2. **Connect to CDU skid.** Remove QD caps, mate to pre-filled flexible hoses. Hoses pressurized to 10 bar for 2 hours, confirm seal.
3. **Top-off PG25.** Minor top-off from skid expansion tank (accounts for hose fill).
4. **Connect Munters skid.** Mate ducts, confirm flow.
5. **Connect ELEC ECP.** 480 V AC 3-phase, network, E-stop.
6. **BMS + orchestrator handshake.** Confirm telemetry, mode commands.
7. **Workload dispatch test.** Dry run workloads at low compute to verify thermal envelope.
8. **Full rated test.** 75% load for 4 hours, confirm thermal steady-state.
9. **Release to service.**

Target: 48 hours arrival-to-production vs. 6–12 weeks industry standard for traditional container-based data center deployments.

---

## §27  SERVICE ACCESS CHOREOGRAPHY

| Service Event                       | Frequency   | Access Required                    | Duration     |
|-------------------------------------|-------------|------------------------------------|--------------|
| BMS module swap (failover verified) | <2×/year    | Panel P-6                          | 45 minutes   |
| VESDA filter                        | Annual      | Any panel                          | 30 minutes   |
| Sensor calibration (PG25 QD gauges) | Annual      | Panel P-9 or P-10                  | 60 minutes   |
| TraceTek cable health check         | Annual      | Panel P-9                          | 30 minutes   |
| Rack hot-swap (per-rack)            | As needed   | Panel P-3 through P-8 (per rack)   | 60 min/rack  |
| Delta shelf hot-swap (per shelf)    | As needed   | Panel P-7 or P-8                   | 30 min/shelf |
| InfiniBand fiber swap               | As needed   | CDU-end ECP external               | 15 minutes   |

Total service person-hours per Cassette per year (steady-state): <10 hours.

---

## §28  BILL OF MATERIALS (BY CLASS)

See Cassette-BOM-001 for per-line detail.

### Mass Budget Summary

| Class                                | Mass (kg) |
|--------------------------------------|-----------|
| Container shell (40' HC ISO)         | 4,800     |
| Racks (15 positions: 9 NVL72 compute + 1 control + 5 Delta in-row power) | 11,200 (preliminary — C-01 open) |
| Manifolds, piping, valves (interior) | 365       |
| Fire suppression (Novec + VESDA)     | 180       |
| Munters DSS Pro interface            | 60        |
| Cable tray, lighting, sensors        | 220       |
| Access panels and hardware           | 120       |
| QD plate + PG25 QDs                  | 35        |
| Miscellaneous / allowances           | 500       |
| Operator allowance (sensors, documentation, small fittings) | 380 |
| Initial PG25 charge (interior only, ~180 L) | 180  |
| **Total onshore operating**          | **29,085 (preliminary)** |

Margin to ISO 30,480 kg limit: **1,395 kg**

Margin allocation:
- 300 kg structural reinforcement (seismic / offshore)
- 500 kg extra racks or reinforcement (future CPX-Next)
- 595 kg reserve

---

## §29  OPEN ITEMS & RISKS

| ID    | Priority | Description                                                                 | Owner  |
|-------|----------|-----------------------------------------------------------------------------|--------|
| E-01  | ~~P-1~~ → P-0 → **CLOSED 2026-04-22** | ECP AC connector — down-selected: Eaton Pow-R-Way III wall entry fitting, 6,000 A, 600 V AC, UL 857. See ELEC-001 §18, ECP-001 §5. | ADC engineering |
| E-02  | ~~P-1~~ → P-0 → **CLOSED 2026-04-22** | 480 V AC main disconnect — down-selected: Eaton Magnum DS, 6,000 A, UL 1066, motor-operated, shunt trip 24 V DC. See ELEC-001 §18, BOM-001 §9. | ADC engineering |
| IN-01 | P-1 → **CLOSED 2026-04-22** | PG25 QD selection — Stäubli QBH-150 DN150 confirmed primary. Parker Snap-tite 75 removed as qualified alternate (poppet valve — not dry-break). See ECP-001 §7, BOM-001 §5.2. | ADC engineering |
| IN-02 | P-1      | Service End Zone detailed layout drawings — R10 control rack, QD plate, manifold termination | ADC engineering |
| IN-03 | P-1      | Panel P-6 access frequency <2×/year operationally acceptable — confirm with operations | ADC operations |
| IN-04 | P-1      | Sealed pressure-vessel commissioning workflow — qualify welders, X-ray vendor, vacuum decay test equipment | ADC engineering |
| IN-05 | P-2      | Mass budget re-verification with 5 Delta in-row power rack weights confirmed (C-01) | ADC engineering |
| IN-06 | P-2      | PG25 initial charge logistics — fill port, factory-to-site PG25 supply chain | ADC operations |
| IN-07 | P-2      | Internal noise reduction opportunity — possible to reduce rack acoustic damping | ADC engineering |
| IN-08 | P-3      | Acoustic measurements for marketing/customer documentation | ADC marketing |
| MO-03 | P-1      | Munters DSS Pro model, airflow, FW coil ΔP, and CHP regen interface confirmation | ADC engineering |

---

**Cassette-INT-001 — Interior Design Specification · Rev 1.2 · 2026-04-22**
**Scott Tomsu · scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana**
**CONFIDENTIAL**
