# Cassette — CONTROL & DATA ARCHITECTURE

**Document:** Cassette-CTRL-001
**Revision:** 1.1
**Date:** 2026-04-20
**Classification:** CONFIDENTIAL
**Status:** Released

**Companion documents:** Cassette-INT-001 Rev 3.0 · Cassette-ECP-001 Rev 3.0 · Cassette-ELEC-001 Rev 1.2 · Cassette-COOL-002 Rev 1.0 · Cassette-CDUSKID-001 Rev 1.0 · Cassette-FIRE-001 Rev 1.2 · Cassette-MODES-001 Rev 1.1 · Cassette-SIS-001 Rev 1.1 · Cassette-CYBER-001 Rev 1.1 · Cassette-TAGS-001 Rev 1.1

| Rev | Date       | Description                                                                           |
|-----|------------|---------------------------------------------------------------------------------------|
| 1.0 | 2026-04-20 | Initial release. Five-layer Purdue-style control architecture for cassette + external CDU skid + Munters skid + 2× Cat G3520K gensets + absorption chiller + switchgear. Defines site orchestrator, protocol gateway, time synchronization, workload-aware control, predictive maintenance model catalog, HMI architecture, network segmentation. |
| **1.1** | **2026-04-20** | **Companion documents updated to Rev 3.0 baseline (INT, ECP) and Rev 1.2 (ELEC, FIRE). External CDU architecture references updated from COOL-001 (superseded) to COOL-002 + CDUSKID-001. CDU skid L1 PLC spec (Siemens S7-1500F) confirmed against CDUSKID-001 §17. No changes to Purdue model, protocol gateway, time sync, or PM model catalog.** |

**Prepared by:** Scott Tomsu · CEO / Chief Engineer
scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana

---

## TABLE OF CONTENTS

- §1  Purpose, Scope & References
- §2  Architecture Overview — Five-Layer Model
- §3  Layer 0 — Field Devices
- §4  Layer 1 — Skid-Level PLCs
- §5  Layer 2 — Supervisory Control
- §6  Layer 3 — Site Operations
- §7  Layer 4 — Enterprise / Fleet
- §8  Data Flow Specifications
- §9  Protocol Translation & OPC UA Namespace
- §10 Time Synchronization
- §11 Workload-Aware Control Loop
- §12 Predictive Maintenance Models
- §13 HMI Architecture — Three Tiers
- §14 Redundancy, Failure Modes & Graceful Degradation
- §15 Network Architecture & Segmentation
- §16 Bill of Materials Summary
- §17 Open Items

---

## §1  PURPOSE, SCOPE & REFERENCES

### Purpose

This document defines the complete control and data architecture for a deployed Cassette edge AI compute node. It is the top-level control systems specification and serves as the contract between the hardware design (defined in INT-001, ECP-001, ELEC-001, COOL-001) and the site systems integrator who will commission the deployment.

### Scope

The architecture spans five hierarchical layers with defined responsibilities, protocol interfaces, and failure-mode expectations at each layer. The deployed unit comprises:

| Unit                     | Function                               | Control domain                  |
|--------------------------|----------------------------------------|---------------------------------|
| 1× Cassette              | 15 Vera Rubin NVL72 racks, sealed     | Cassette BMS (Jetson Orin N+1)  |
| 1× External CDU skid     | Plate HX, pumps, filters, buffer tank | CDU skid PLC (new)              |
| 1× Munters HCD-600 skid  | Dehumidification                      | Munters PLC (existing, Siemens) |
| 2× Cat G3520K gensets    | Natural gas, 2N electrical redundancy | Cat EMCP 4.4 per genset         |
| 1× Heat recovery + LiBr  | Waste-heat absorption chiller         | Chiller controller (vendor)     |
| 1× 800 VDC switchgear    | Primary protection + distribution     | Protective relays (IEC 61850)   |

### What This Document Is Not

- Not a safety system specification — see CAS-SIS-001
- Not a cybersecurity architecture — see CAS-CYBER-001
- Not the complete tag dictionary — see CAS-TAGS-001 (this document defines the namespace structure; TAGS-001 enumerates every tag)
- Not a physical equipment specification — see INT-001, CDUSKID-001 (forthcoming)
- Not a cloud platform selection (AWS vs Azure vs GCP is a procurement decision made at commercialization)

### References

| Document | Title | Rev |
|----------|-------|-----|
| Cassette-INT-001  | Interior Design Specification            | 2.2 |
| Cassette-ECP-001  | External Connection Panel ICD            | 2.2 |
| Cassette-ELEC-001 | Electrical Single-Line & Distribution    | 1.1 |
| Cassette-COOL-001 | Cooling Hydraulic Model                  | 1.1 |
| Cassette-FIRE-001 | Fire Suppression Engineering             | 1.1 |
| Cassette-MODES-001| Operating Modes & Sequences              | 1.0 |
| Cassette-SIS-001  | Safety Instrumented System               | 1.0 |
| ISA-95            | Enterprise–Control System Integration    | 2018 |
| ISA-18.2          | Management of Alarm Systems              | 2016 |
| IEC 62443         | Industrial Automation Cybersecurity      | 2018 |
| IEC 62541         | OPC Unified Architecture                 | 2020 |
| IEEE 1588         | Precision Time Protocol                  | 2019 |
| NVIDIA Redfish    | Delta shelf + NVL72 management API       | current |

---

## §2  ARCHITECTURE OVERVIEW — FIVE-LAYER MODEL

### Layer Summary

| Layer | Role                                            | Typical scan / publish rate | End-to-end latency SLA |
|-------|-------------------------------------------------|-----------------------------|------------------------|
| L4    | Enterprise — fleet analytics, business systems  | minutes to days             | — (batch)              |
| L3    | Site — orchestration, historian, twin, workload | 100 ms – 10 s               | < 2 s                  |
| L2    | Supervisory — BMS, gateway, safety coordination | 10 – 100 ms                 | < 500 ms               |
| L1    | Direct control — skid PLCs, protective logic    | 1 – 10 ms                   | < 50 ms                |
| L0    | Field I/O — sensors and actuators               | ≤ 1 ms                      | < 10 ms                |

### Design Principles

1. **Each layer is independently certifiable.** A failure or upgrade at a higher layer does not prevent continued safe operation at lower layers. The cassette can run in local-autonomous mode with only L0–L2 operating if the cloud and site-level systems are offline.

2. **The safety system is separate.** The Safety Instrumented System (SIS) is a parallel control path with its own sensors, controller, and final elements. It is not subordinate to any layer in this hierarchy. See CAS-SIS-001.

3. **Data flows up, commands flow down.** Telemetry aggregates from L0 upward through lossy summarization at each layer. Commands originate at L3 (or operator-initiated at L2/L4) and flow downward with acknowledgment. No layer bypasses its immediate neighbors for normal operation.

4. **Vendor diversity is expected and translated.** Every skid vendor ships its own controller and protocol. The architecture does not attempt to standardize vendor controllers — it translates them at the L2 protocol gateway into a single canonical namespace.

5. **Time is a first-class signal.** All timestamps across all layers are synchronized to IEEE 1588 PTP grandmaster discipline. Event ordering across controllers must be reconstructable to 1 ms granularity.

### Architecture Diagram Reference

See `Cassette Control & Data Architecture — five-layer model` diagram (generated inline in design reviews). Layer-by-layer specification follows in §3–§7.

---

## §3  LAYER 0 — FIELD DEVICES

### Scope

L0 comprises every sensor and actuator in the deployment: approximately 200+ sensor points and 40+ actuator points distributed across the cassette interior, the CDU skid, the Munters skid, the two genset enclosures, the absorption chiller, and the switchgear lineup.

### Signal Inventory by Zone

| Zone                 | Sensors                                                                                      | Actuators                              | Count (sens/act) |
|----------------------|----------------------------------------------------------------------------------------------|----------------------------------------|------------------|
| Cassette interior    | Per-rack supply/return T, flow, current, vibration, leak; interior T/RH ×6, pressure, tilt, shock | Rack UQD isolation, panel indicators   | 110 / 18         |
| ECP                  | External T/RH/baro, leak, reed switches                                                      | CHW / PG25 isolation valves, purge     | 20 / 6           |
| CDU skid             | Supply/return T, flow, pressure, filter ΔP, pump vib & current, buffer tank T strat, expansion level | Pump VFDs ×2, filter switchover, bypass valve | 24 / 6    |
| Munters skid         | Process air T/RH/flow, reactivation heater T, rotor position, filter ΔP                      | Heater relay, damper, rotor speed      | 8 / 3            |
| Gensets (×2)         | Per-genset: jacket T, oil P/T, exhaust T, fuel rate, RPM, voltages, currents, vib, knock     | Start/stop relay, fuel valve, load ref | 36 / 6           |
| Absorption chiller   | LiBr concentration, generator T, condenser T, evaporator T, pump status, solution level      | Heat source valve, solution pump       | 12 / 3           |
| Switchgear           | Bus V, I per feeder, breaker status, CT secondaries, arc-flash light sensors                 | Breaker trip/close, SPD status         | 24 / 10          |
| Gas detection (SIS)  | LEL at 6 points, H₂S at 4, CO at 3                                                           | ESD valve interfaces                   | 13 / 3           |
| **Total**            |                                                                                              |                                        | **~247 / ~55**   |

### Signal Standards

| Signal type            | Wiring                              | Interface               |
|------------------------|-------------------------------------|-------------------------|
| RTD (Pt100 / Pt1000)   | 3-wire or 4-wire shielded twisted pair | Direct to PLC AI card or via ADAM-6015 |
| Thermocouple (K, J)    | Compensated extension wire          | Isolated AI, cold-junction compensation |
| 4–20 mA loop           | 2-wire shielded twisted pair, loop-powered | Standard AI card        |
| Ultrasonic flow        | Ethernet / Modbus TCP               | Via L1 PLC              |
| MEMS accelerometer     | I²C or SPI                          | Via dedicated vibration monitor (IFM VSE100) |
| Digital discrete       | 24 V DC dry contact                 | Standard DI card        |
| Analog output (VFD ref)| 4–20 mA                             | Standard AO card        |
| Valve position feedback| 4–20 mA position + 24 V DC limit switches | AI + DI              |
| Leak detect (TraceTek) | Proprietary 2-wire                  | TTDM-128 alarm panel → Modbus TCP |
| Arc-flash light sensor | Fiber-coupled                       | Dedicated arc-flash relay (SEL-751 or equivalent) |

### Wiring Conventions

- All field signal cables routed in separate cable tray from power cables (minimum 300 mm separation per IEEE 518).
- Shields grounded at single point at the PLC cabinet end only.
- Cable designations follow ISA S5.1 tag numbering, integrated with the site tag dictionary (CAS-TAGS-001).
- All field cables include ≥ 2 spare conductors for future expansion (15% spare per cable minimum).

---

## §4  LAYER 1 — SKID-LEVEL PLCs

### Controller Domains

The deployment has six L1 controller domains, each with defined responsibilities and a defined interface to L2:

| Domain | Controller | Primary responsibilities | Existing/new |
|--------|-----------|--------------------------|--------------|
| 4.1 Cassette I/O | Jetson AGX Orin (primary) + Advantech ADAM-6000 series I/O | Per-rack telemetry aggregation, leak isolation, rack DC breaker control, fire interlocks | **Existing (INT §20)** |
| 4.2 CDU skid | Siemens S7-1500 | Pump VFD control, filter switchover, flow setpoint, bypass valve, interlocks to cassette | **New** |
| 4.3 Munters skid | Siemens S7-1200 | Rotor speed, reactivation heater, process damper, filter monitoring | **Existing (INT §16)** |
| 4.4 Gensets | Cat EMCP 4.4 (one per genset) | Start/stop, load sharing, protective functions, CHP mode selection | **Existing (Cat OEM)** |
| 4.5 Absorption chiller | Vendor-integrated PLC (Yazaki, Thermax, Carrier-type) | LiBr concentration control, heat input modulation, generator T control | **Vendor OEM**, requires integration spec |
| 4.6 Switchgear protective relays | SEL-751 / SEL-787 or ABB REF615 | 87, 51, 50, 27, 59, 81 functions; IEC 61850 GOOSE inter-trip | **New** |

### §4.1  Cassette I/O Aggregation

The cassette uses the existing architecture from INT §20:
- Jetson AGX Orin 64 GB industrial (2× for N+1 redundancy) in R15
- Advantech ADAM-6017 (×4), ADAM-6060 (×2), ADAM-6050 (×1) as field I/O
- TraceTek TTDM-128 as dedicated leak detection subsystem (Modbus TCP to Jetson)
- Xtralis VESDA-E VEU-A00 aspirating smoke detector (VESDAnet + Modbus TCP)
- CoolIT CDU (existing internal; deprecated in external-CDU architecture) or external CDU skid PLC
- Delta power shelves (Redfish via OOB Ethernet)

The Jetson also serves as the L2 Cassette BMS (see §5). Its dual role — L1 I/O aggregation plus L2 supervisory — is intentional and leverages the Orin's compute headroom. A dedicated L1-only controller is not required inside the sealed cassette.

### §4.2  CDU Skid PLC

Controller: **Siemens S7-1500 CPU 1515F-2 PN** (or equivalent Rockwell ControlLogix 5580)

I/O count:
- 16× AI (4–20 mA and RTD) for temperatures, pressures, levels
- 8× DI (24 VDC) for limit switches, breaker aux contacts
- 6× AO (4–20 mA) for pump speed references, valve positioners
- 8× DO (24 VDC) for relay outputs

Protective logic:
- Low suction pressure → trip pump (protects seal)
- High discharge pressure → modulate pump speed down (protects piping)
- Filter ΔP > threshold → auto-switchover to standby filter, alarm
- Loss of primary flow > 5 s at non-zero pump command → trip cassette (via L2 coordinated signal)
- Expansion tank level low → alarm, then trip at low-low
- Buffer tank high temperature → force bypass to HX

Interfaces to L2:
- OPC UA server on the S7-1500 (integrated with firmware V2.8+)
- Modbus TCP slave as fallback
- Hardwired 24 VDC dry-contact emergency trip from cassette BMS (two-pole redundant)

### §4.3  Munters Skid PLC (existing)

Per INT §16:
- Siemens S7-1200 CPU with KTP400 HMI
- Modbus RTU to cassette BMS
- Siemens native protocol for local diagnostics

Upgrade required for this architecture: add **CM 1241 RS-485 and CP 1242-7 GPRS/Ethernet** module to enable OPC UA publication (S7-1200 supports OPC UA server in firmware V4.4+). This is a firmware and hardware add-on, not a controller replacement.

### §4.4  Cat EMCP 4.4 Genset Controllers

One Cat EMCP 4.4 per genset, factory-installed, provides:
- ECM engine control (CAN/J1939 to the engine)
- Protective functions per NFPA 110 Level 1 / ISO 8528-4
- Load sharing via Cat Communications Network (CCN) between EMCPs
- Remote start/stop, manual/auto selector
- Native J1939 and Modbus TCP exposure

Interface to L2:
- **J1939 via Cat NTE Gateway** → Ethernet/Modbus TCP translation
- Modbus TCP map per Cat Application Note LEBE0006
- Hardwired ESD input (SIS-driven, see CAS-SIS-001)

CHP-specific data points that must be exposed:
- Jacket water supply T (°C)
- Jacket water return T (°C)
- Exhaust temperature pre-turbo (°C)
- Exhaust temperature post-turbo (°C)
- Heat recovery flow rate (if metered)
- Current fuel LHV correction factor

### §4.5  Absorption Chiller Controller

Product selection: Yazaki WFC-SC20 (20 RT equivalent, double-effect) or Thermax Cogenie series sized at ~800 RT (~2.8 MW cooling) to match Cat G3520K CHP output.

Chiller controllers vary by manufacturer. Integration requirement:
- BACnet/IP or Modbus TCP exposed at a single Ethernet drop
- Minimum tag list:
  - Chilled water supply T (°C)
  - Chilled water return T (°C)
  - Chilled water flow (LPM or m³/h)
  - Heat input rate (kW)
  - Generator temperature (°C)
  - Condenser water T (if cooling-tower-coupled)
  - LiBr solution concentration (%)
  - Solution pump status
  - Fault/alarm bitmap

Vendor selection gates open item CT-01: confirm protocol and tag availability before contract.

### §4.6  Switchgear Protective Relays

Microprocessor-based protective relays per feeder:
- Main 800 VDC breaker: SEL-751 (motor protection class repurposed for DC, requires SEL FAE engagement) or ABB REX615 DC-rated
- 480 VAC auxiliary (CDU, Munters, controls): SEL-751 standard
- Per-rack DC feeders (15× 250 A): no dedicated relay; protection at the DC main

Communications:
- IEC 61850 GOOSE between relays on a dedicated process bus (separate Ethernet ring from the control network)
- IEC 61850 MMS to the L2 protocol gateway for telemetry and event records
- DNP3 fallback to site SCADA if a customer requires it

---

## §5  LAYER 2 — SUPERVISORY CONTROL

### §5.1  Cassette BMS (Jetson AGX Orin) — Existing

Per INT §20, the Jetson Orin hosts:
- **OS:** Ubuntu 22.04 LTS (JetPack 6.x)
- **Data collection:** Telegraf (Modbus, SNMP, Redfish input plugins)
- **Time-series:** InfluxDB local, 30-day retention
- **Dashboard:** Grafana (local + remote access)
- **Control logic:** Custom Python + MQTT bridge
- **ML inference:** TensorRT on Orin GPU (see §12)
- **External telemetry:** MQTT to platform SCADA + cloud
- **Backhaul:** Starlink / 4G/5G fallback

New additions for the 5-skid architecture:
- **OPC UA client subscription** to the L2 Protocol Gateway (see §5.2) for non-cassette skid telemetry
- **Published OPC UA server** on the Jetson exposing cassette-internal tags (rack temperatures, flows, currents) to the Gateway
- **Workload scheduler integration** (see §11) — subscription to SLURM / Kubernetes GPU queue
- **Predictive maintenance inference runtime** — TensorRT-optimized models executed at 1 Hz (see §12)

Redundancy: 2× Jetson Orin in active/standby. Failover managed by Keepalived with <200 ms takeover. State synchronization via InfluxDB replication (streaming replication mode).

### §5.2  Protocol Gateway — New

Purpose: translate every L1 controller protocol into a single canonical OPC UA namespace and publish summary telemetry via MQTT Sparkplug B to L3.

**Recommended product: Ignition Edge** (Inductive Automation) running on a ruggedized Linux edge server.

Alternative: **PTC Kepware KEPServerEX** with MQTT advanced plugin. Kepware is a pure protocol translator; Ignition bundles translation, SCADA, historian, and MQTT into one platform and is generally a better fit for this scale.

Hardware: 1U industrial server, dual power supply, 16 GB RAM, 512 GB SSD, redundant Ethernet. Example: **Advantech MIC-770 V3** or **Siemens IPC847E**.

Southbound protocols supported:
- J1939 (Cat gensets via NTE gateway)
- Modbus TCP / Modbus RTU (Munters, CDU PLC, chiller, TraceTek, VESDA)
- IEC 61850 (switchgear relays)
- Redfish (Delta shelves, NVL72 management)
- BACnet/IP (chiller, possibly)
- OPC UA client (Siemens S7-1500, Cassette BMS)

Northbound:
- OPC UA server (IEC 62541 compliant) — canonical namespace
- MQTT Sparkplug B publisher (ISA-95 tag hierarchy)
- REST API for ad-hoc queries and engineering access

Redundancy: 1+1 hot-standby with 250 ms failover. Primary and secondary Gateway instances share the same canonical namespace and hot-sync via Ignition Gateway Network.

### §5.3  Safety System (SIS) Integration Point

The SIS runs in parallel (see CAS-SIS-001) but has defined interfaces to the BPCS at L2:
- SIS publishes its state (armed/tripped/bypassed) to the BMS via hardwired dry contacts and via Modbus TCP (read-only from BPCS perspective)
- BMS requests from SIS are advisory only — the SIS executes based on its own sensor inputs
- Any SIS trip is mirrored at L2 for logging and alarm propagation
- L2 cannot reset an SIS trip — reset is manual at the SIS HMI only

---

## §6  LAYER 3 — SITE OPERATIONS

### §6.1  Site Orchestrator

Purpose: coordinate all skids, execute operating mode sequences, optimize CHP performance, manage startup / shutdown / failover / maintenance windows. This is the "brain" that sees the whole unit.

**Platform: Ignition SCADA full license** on the same server hosting the L2 Protocol Gateway, or on a dedicated L3 server for larger fleets. Single-site deployment can co-host; fleet deployment (>3 sites) separates them.

Core responsibilities:
- **Mode state machine** execution (see CAS-MODES-001)
- **CHP optimization** — coordinate genset load setpoint, absorption chiller heat demand, and CDU cooling to maximize overall efficiency
- **Startup / shutdown sequences** — multi-minute scripted procedures that span multiple skids
- **Failover coordination** — genset A→B, CDU pump A→B, Jetson A→B
- **Maintenance mode** — isolate one skid for service while the rest runs
- **Alarm aggregation and rationalization** per ISA-18.2
- **Operator HMI** (see §13)
- **Work order generation** — integration with CMMS (Fiix, UpKeep, or manual CSV export)

Implementation environment:
- Ignition scripting language (Python 2.7 / Jython for SCADA compatibility)
- Ignition Vision or Perspective modules for HMI
- Built-in Ignition Historian for local store (parallel to the InfluxDB on the Jetson — redundant historian at two layers)

Redundancy: Ignition Gateway Network with warm-standby. RTO < 30 s for a full Gateway failover.

### §6.2  Historian + Digital Twin

**Historian** — persistent time-series store for all tags across all skids.

Architecture:
- Short-term: InfluxDB on Cassette BMS (existing, 30 days local)
- Medium-term: Ignition Tag Historian (separate time-series DB on the L2/L3 server, 1 year)
- Long-term: Cloud time-series store (TimescaleDB or InfluxDB Cloud, 7+ years for ESG / compliance)

Sampling strategy:
- Fast loops (per-rack T, pump speed, bus V/I): 1 Hz continuous
- Slow trends (ambient T/RH, total kWh, flow totalizers): 1 min
- Event-driven: alarms, state changes, operator actions, transients (full 1 kHz capture for 30 s around event)

**Digital Twin** — real-time physics model of the deployment.

Platform: **NVIDIA Omniverse** (existing work stream; see ADC-OMNIVERSE-GEN module) extended to a live-data-coupled twin.

Model scope:
- Thermal model of the cassette interior + cold plate circuits
- Hydraulic model of primary PG25 and secondary CHW loops
- Electrical model of 800 VDC bus and per-rack loads
- Thermodynamic model of the Cat genset (as mfg-supplied engine performance curves) and absorption chiller (LiBr phase diagram)

Use cases:
1. **Sensor validation** — compare measured vs modeled values; flag divergence
2. **Counterfactual replay** — "what if we had modulated genset load by 5% at 14:23?"
3. **Operator training** — desktop simulator for new site onboarding
4. **What-if planning** — estimate impact of proposed workload or maintenance changes

Data pipeline:
- InfluxDB → state extractor (Python) → Omniverse USD scene update at 1 Hz
- Model parameters (heat capacities, pipe roughness, pump curves) stored in a parameter file per deployment; tuned during commissioning from measured data

### §6.3  Workload Scheduler Integration

Purpose: close the loop between the GPU workload queue and the thermal/power system, enabling predictive rather than reactive control. See §11 for the control loop detail.

Integration hooks:
- **SLURM** — poll `squeue --json` API every 5 s, extract next-N-job estimated power draw from job metadata
- **Kubernetes** (NVIDIA GPU Operator) — subscribe to pod lifecycle events via k8s API
- **NVIDIA Base Command Platform** — native API for job submission and telemetry

Published to the orchestrator as MQTT topic `spBv1.0/site1/DDATA/workload/forecast` with payload:
```json
{
  "timestamp": "2026-04-20T14:23:17.420Z",
  "horizon_s": 60,
  "predicted_kw_mean": 2010,
  "predicted_kw_peak": 2380,
  "confidence": 0.87,
  "jobs_in_window": 3
}
```

### §6.4  CMMS Integration

Computerized Maintenance Management System — receives work orders generated by predictive maintenance models (§12) and schedules service.

Initial deployment: manual CSV export from orchestrator → customer's existing CMMS. Future: direct API integration with Fiix, UpKeep, or IBM Maximo.

Work order triggers:
- Predictive maintenance ML model flags likely failure > 7 days out
- Filter ΔP extrapolation predicts replacement need < 30 days out
- Genset 2,000 hr minor service approaching
- Calibration interval approaching on any class-1 sensor

---

## §7  LAYER 4 — ENTERPRISE / FLEET

### §7.1  Fleet Dashboard + Analytics

Platform: **Grafana Cloud** or **AWS Managed Grafana** for dashboards; **AWS Timestream** or **TimescaleDB on RDS** for long-term historian; **MLflow** for RL model lifecycle management.

Dashboards:
- **Operations view** — current state of all deployed units, active alarms, SLA compliance
- **Energy view** — gas consumption, electrical output, cooling output, CHP efficiency per unit
- **Maintenance view** — upcoming PM windows, open work orders, parts on order
- **Financial view** — revenue (GPU-hours sold), gas cost, maintenance cost, margin per unit
- **ESG view** — Scope 1 emissions per unit, flare-gas-offset credits, carbon intensity per GPU-hour

Cross-fleet analytics:
- **RL tuning** — reinforcement learning on control setpoints, trained on historical data from the fleet, deployed back to the orchestrators as tuned parameter sets. Candidate frameworks: Ray RLlib, Stable-Baselines3
- **Benchmarking** — unit-level comparison of efficiency, uptime, alarm rate
- **Anomaly pooling** — one-shot learning from a new failure mode observed at any unit propagates to all others

### §7.2  Customer + ESG Portal

Read-only, customer-facing dashboard per unit:
- SLA performance (uptime, availability, response time)
- Compute delivered (GPU-hours, TFLOPS-hours)
- Energy consumed and offset
- Carbon accounting per IPCC Scope 1/2/3 framework
- Maintenance history

Carbon credit framework for stranded-gas deployments:
- Flare gas captured vs baseline (customer-provided flare metering)
- Methane destruction factor per EPA 40 CFR 98 subpart W
- California LCFS or EU ETS offset eligibility documentation
- Auditable trail from field meter → orchestrator → portal → compliance filing

---

## §8  DATA FLOW SPECIFICATIONS

### §8.1  Upward Telemetry

| Class            | Examples                                           | Rate        | Destination              | Retention |
|------------------|----------------------------------------------------|-------------|--------------------------|-----------|
| Fast real-time   | Rack temperatures, pump speeds, bus V/I            | 1 Hz        | L2 BMS → L3 Historian   | 30 d raw, 1 y @ 1 min |
| Slow trend       | Ambient T, totalizers, filter hours                | 1 / min     | L3 Historian             | 7 y @ 1 min |
| Event-driven     | Alarms, state changes, operator actions            | as occurs   | L3 Orchestrator + L4     | 7 y |
| Forensic burst   | 1 kHz sampled ring buffer, flushed on trigger      | 30 s @ 1 kHz| L3 Orchestrator          | 90 d |
| High-speed trans | Electrical fault / arc-flash captures              | 4 kHz       | L2 local ring + dump     | 90 d |

### §8.2  Downward Commands

| Class            | Examples                                             | Path                                      |
|------------------|------------------------------------------------------|-------------------------------------------|
| Setpoint         | Primary flow target, chiller heat demand             | L3 Orchestrator → L2 Gateway → L1 PLC     |
| Mode change      | Transition from NORMAL to DEGRADED                   | L3 Orchestrator → L2 Gateway → L1 PLCs    |
| Manual override  | Operator-driven valve position, pump stop            | L2 HMI → L2 Gateway → L1 PLC              |
| Emergency stop   | E-stop from any source                               | Hardwired → SIS → all L1 PLCs (parallel)  |
| Firmware update  | Signed image to any controller                       | L4 → L3 → L2 → L1 (staged, acknowledged)  |

### §8.3  Alarm Propagation & Rationalization (ISA-18.2)

Alarm classification matrix:

| Priority | Response time | Consequence                              | Max count active |
|----------|---------------|------------------------------------------|------------------|
| Urgent   | < 1 min       | Imminent damage, safety, outage          | 2 simultaneous   |
| High     | < 10 min      | Production loss within the hour          | 10               |
| Medium   | < 1 hr        | Degradation, maintenance needed          | 25               |
| Low      | end of shift  | Information, trend deviation             | unlimited        |

Rationalization rules:
- Every alarm is **actionable** (if the operator can do nothing, it's a notification, not an alarm)
- Alarms are **correlated** — one root cause should not produce 30 downstream alarms; the orchestrator suppresses correlated children
- Alarm **floods** (> 10 new alarms in 60 s) trigger a flood-management dialog at the HMI
- All acknowledgments are **logged**, not silent

### §8.4  Forensic Capture

Purpose: when an unplanned event occurs, reconstruct the millisecond-by-millisecond sequence across controllers.

Mechanism:
- Every L1 controller maintains a 30-second ring buffer of all tags at native scan rate (typically 10–100 ms)
- Triggered by: any Urgent or High alarm, operator manual trigger, SIS activation
- Captured data flushed to L3 forensic store within 60 s of trigger
- Cross-controller event reconstruction at L3 using PTP timestamps (see §10)

---

## §9  PROTOCOL TRANSLATION & OPC UA NAMESPACE

### §9.1  Protocol Inventory

| Equipment                     | Native protocol(s)         | Translation target  |
|-------------------------------|----------------------------|---------------------|
| Cat G3520K gensets            | J1939, Modbus TCP (EMCP)   | OPC UA              |
| Switchgear relays             | IEC 61850 GOOSE + MMS      | OPC UA (MMS only)   |
| CDU skid PLC (Siemens)        | OPC UA native, Modbus TCP  | OPC UA pass-through |
| Munters (Siemens)             | Modbus RTU, OPC UA (V4.4+) | OPC UA              |
| Absorption chiller            | BACnet/IP or Modbus TCP    | OPC UA              |
| Delta power shelves           | Redfish (HTTPS)            | OPC UA              |
| CoolIT CDU (if retained)      | Redfish, Modbus TCP        | OPC UA              |
| TraceTek TTDM-128             | Modbus TCP                 | OPC UA              |
| VESDA-E                       | VESDAnet + Modbus TCP      | OPC UA              |
| Novec 1230 control panel      | Dry contacts + Modbus TCP  | OPC UA (digital)    |
| Jetson Orin BMS               | OPC UA native              | pass-through        |

### §9.2  OPC UA Namespace Structure (ISA-95 hierarchy)

```
/Site/{site_id}/
    /Cassette/
        /Racks/{R1...R15}/
            /Temperature/Supply
            /Temperature/Return
            /Flow
            /Current
            /Vibration
            /Status
        /Environmental/
            /Temperature/{1..4}
            /Humidity/{1..2}
            /Pressure
        /Fire/
            /VESDA/AlarmLevel
            /Novec/Status
        /BMS/
            /State
            /ActiveAlarms
    /CDU_Skid/
        /Pumps/{A,B}/
            /Speed
            /Current
            /Vibration
            /Status
        /HX/
            /Primary/Inlet_T, Outlet_T, Flow
            /Secondary/Inlet_T, Outlet_T, Flow
        /Filters/{A,B}/
            /DP
            /InService
        /BufferTank/
            /Level, Stratification_T{top,mid,bot}
    /Munters_Skid/
        /ProcessAir/Supply_T, Supply_RH, Flow
        /Reactivation/Heater_T, Status
        /Rotor/Speed, Position
    /Gensets/{A,B}/
        /Engine/RPM, Load, FuelRate, JacketT
        /Exhaust/Temperature{Pre,Post}_Turbo
        /Alternator/Voltage, Current, Frequency
        /CHP/JacketHeatRecovered, ExhaustHeatRecovered
        /Status, RunningHours
    /Chiller/
        /CHW/Supply_T, Return_T, Flow
        /Heat/InputRate
        /Solution/LiBrConcentration, GeneratorT
    /Switchgear/
        /MainBreaker/Status, Position
        /Bus/Voltage, Current
        /Feeders/{R1...R15}/Current, Status
    /Safety/
        /SIS/State (armed/tripped/bypassed)
        /GasDetect/{LEL, H2S, CO}
        /ESD/Status
```

### §9.3  MQTT Sparkplug B Topic Structure

```
spBv1.0/{group_id}/NBIRTH/{edge_node_id}        — node birth certificate
spBv1.0/{group_id}/NDATA/{edge_node_id}         — node data
spBv1.0/{group_id}/DBIRTH/{edge_node_id}/{dev}  — device birth
spBv1.0/{group_id}/DDATA/{edge_node_id}/{dev}   — device data
spBv1.0/{group_id}/NCMD/{edge_node_id}          — node command
spBv1.0/{group_id}/DCMD/{edge_node_id}/{dev}    — device command
spBv1.0/{group_id}/NDEATH/{edge_node_id}        — node death (last will)
```

Where:
- `group_id` = site identifier (e.g., `LFT_WELLPAD_03`)
- `edge_node_id` = Gateway instance identifier
- `dev` = skid or controller identifier (e.g., `CDU`, `GensetA`, `Cassette`)

### §9.4  Tag Dictionary Reference

The complete tag inventory — every physical and calculated tag, its OPC UA path, units, engineering range, alarm limits, archival policy, and access permissions — is maintained in CAS-TAGS-001 as a versioned CSV. This document (CTRL-001) defines only the namespace structure; TAGS-001 enumerates the instances.

---

## §10  TIME SYNCHRONIZATION

### Requirement

All timestamps across all controllers and all historian records must be synchronized to a common reference to support forensic reconstruction of multi-system events at 1 ms granularity.

### Architecture

- **Grandmaster clock:** GPS-disciplined PTP grandmaster (Meinberg LANTIME M1000 or Microchip SyncServer S650), installed at the L3 server cabinet with a rooftop GPS antenna.
- **Transparent switches:** All industrial Ethernet switches on the control LAN must be PTP-aware. Recommended: Hirschmann BOBCAT / RSP series or Cisco IE-4000 with PTP enabled.
- **Boundary clock:** The Ignition Gateway server acts as a PTP boundary clock, regenerating PTP on its downstream ports.
- **Endpoints:**
  - Siemens S7-1500: native PTP support via PROFINET IRT
  - Cat EMCP: no native PTP — Cat NTE Gateway translates and stamps at arrival time
  - Jetson Orin: Linux PTP daemon (ptp4l) with kernel hardware timestamping
  - Ignition Gateway: native PTP support (V8.1.24+)
  - Protective relays (SEL / ABB): native IEEE 1588 per IEC 61850-9-3
- **Fallback:** NTP to a local Stratum-1 NTP server for any device that cannot use PTP. Accuracy degraded to ~10 ms but acceptable for non-forensic functions.

### Time Quality Requirements

| Class | Accuracy to GPS | Examples |
|-------|----------------|----------|
| Class A | < 1 ms | Protective relays, SIS, electrical forensic recorders |
| Class B | < 10 ms | Most controllers, BMS, CDU PLC |
| Class C | < 100 ms | Munters, environmental sensors, trend data |
| Class D | < 1 s | Enterprise dashboards, reports |

All events in the historian are tagged with a quality indicator derived from the endpoint's time class.

---

## §11  WORKLOAD-AWARE CONTROL LOOP

### §11.1  Concept

Traditional data center cooling is **reactive**: measure temperature, adjust cooling. For Vera Rubin NVL72 under training workloads, thermal load pulses on second-scale timescales (forward/backward pass cycle), which outpaces the thermal time constant of the CDU and chiller. Reactive control chases these transients and either overshoots alarm limits or oversizes the cooling plant to stay conservative.

The workload scheduler knows what the GPUs are about to do 10–60 seconds ahead of load application. That horizon is long enough to:
- Pre-ramp CDU pump speed
- Pre-cool buffer tank strata
- Pre-position absorption chiller heat demand
- Pre-adjust genset load setpoint

This is **feedforward + feedback** control instead of pure feedback.

### §11.2  Control Loop Architecture

```
   Workload queue (SLURM / K8s / BCM)
           │
           ▼ job metadata (GPU count, estimated TDP, duration)
   Workload forecast service (on Cassette BMS)
           │
           ▼ MQTT topic: workload/forecast (payload in §6.3)
   Site Orchestrator feedforward controller
           │
           ├──▶ CDU pump speed preset (L1 CDU PLC)
           ├──▶ Buffer tank pre-cool command (L1 CDU PLC)
           ├──▶ Chiller heat demand preset (L1 Chiller PLC)
           └──▶ Genset load reference update (L1 Cat EMCP)
                       │
                       ▼ (system physically responds)
           Real-time sensors (L0)
                       │
                       ▼
           Feedback PID controllers (in L1 PLCs)
                       │
                       ▼ (trim feedforward)
```

### §11.3  Control Loop Parameters

Initial feedforward gains (tuned during commissioning):

| Actuator                  | Feedforward input            | Gain              | Rate limit |
|---------------------------|------------------------------|-------------------|------------|
| CDU pump speed            | Forecast kW_mean             | 1.0 Hz / MW       | 0.5 Hz/s   |
| Buffer tank pre-cool      | Forecast kW_peak − kW_mean   | 0.2 °C setpoint / MW | 0.05 °C/s |
| Chiller heat demand       | Forecast kW_mean             | 1.0 MW heat / MW cooling | 0.5 MW/min |
| Genset load reference     | Forecast kW_mean + aux       | 1.0 (direct)      | 50 kW/s    |

Feedback PIDs remain on every actuator, operating on measured error between setpoint and actual. Feedforward is additive to the feedback output.

### §11.4  Performance Target

Goal: reduce transient temperature excursions by 60% vs pure feedback control, allowing CDU to be operated at 85% of nameplate capacity continuously instead of 70%. This is a 20% increase in allowable compute load per CDU at the same hardware cost.

Performance measurement: log feedforward and feedback contributions separately; A/B test feedforward on vs off during commissioning week.

---

## §12  PREDICTIVE MAINTENANCE MODELS

### §12.1  Model Catalog

Deployed on the Cassette BMS (Jetson Orin) via TensorRT, with outputs published to the L3 orchestrator and escalated to CMMS work orders.

| Asset                      | Inputs                                          | Model class              | Target failure              | Lead time |
|----------------------------|-------------------------------------------------|--------------------------|-----------------------------|-----------|
| CDU pump bearings          | Vibration FFT, bearing T, motor current         | Autoencoder + threshold  | Bearing wear, misalignment  | 2–4 weeks |
| Cold plate fouling         | Per-rack ΔT vs flow at constant load            | Regression residual      | Scale buildup               | 4–8 weeks |
| Cartridge filter loading   | ΔP vs volumetric flow                           | Linear extrapolation     | Filter replacement timing   | exact     |
| Strainer basket            | Upstream ΔP + manual clean records              | Trending                 | Strainer clean needed       | 1–2 weeks |
| Genset efficiency decay    | Fuel rate (J1939) vs kW output vs T_ambient     | Baseline deviation       | Injector wear, top-end wear | 4–12 weeks|
| Absorption chiller COP     | Heat input vs cooling output, LiBr concentration| Thermodynamic residual  | Crystallization, leak       | 2–6 weeks |
| Switchgear contacts        | Trip time, aux contact chatter                  | Weibull trending         | Contact erosion             | months    |
| Power shelf failure        | Delta shelf fault codes + temperature           | Bayesian failure rate    | Early shelf replacement     | days–weeks|
| UQD leak-by                | Per-rack supply vs return T asymmetry           | Anomaly detection        | Seal leak                   | days      |

### §12.2  Model Lifecycle

- **Training:** offline on L4 cloud using pooled fleet data + unit-specific calibration
- **Deployment:** TensorRT engine file pushed to Jetson via signed firmware update
- **Inference:** 1 Hz, runs in parallel with other Jetson workloads (10% GPU allocation max)
- **Drift detection:** output distribution compared to training distribution; model retrained when Kullback-Leibler divergence > threshold
- **Rollback:** previous model version retained; automatic rollback if new model false-positive rate exceeds 2×

### §12.3  Output and Work Order Generation

Each model publishes to MQTT topic `spBv1.0/{site}/DDATA/PM/{asset}/{model}`:
```json
{
  "timestamp": "...",
  "asset": "CDU_Pump_A",
  "model": "bearing_autoencoder_v3",
  "anomaly_score": 0.73,
  "threshold": 0.80,
  "estimated_remaining_life_hr": 420,
  "confidence": 0.82,
  "recommended_action": "schedule bearing inspection within 2 weeks"
}
```

When `anomaly_score > threshold` or `estimated_remaining_life_hr < 7 × 24`, orchestrator auto-generates a CMMS work order (severity = low/medium/high mapped from confidence and remaining life).

---

## §13  HMI ARCHITECTURE — THREE TIERS

### §13.1  Tier 1 — Field HMI (at the unit)

Purpose: local operator interface at the deployment site. Hazardous-area-rated if site is Class I Div 2 (most oilfield edge deployments will be).

Hardware: **Pepperl+Fuchs VisuNet GXP** (Class I Div 2 rated) 15" panel mount, or **Beijer X2 Extreme 15"** for unclassified sites.

Screens (kept deliberately minimal):
1. **State dashboard** — current mode, active skids, top 5 alarms, emergency controls
2. **Manual mode screen** — skid-by-skid start/stop, local overrides (key-locked)
3. **Alarm log** — last 100 alarms, ack interface
4. **Trending** — last 2 hours of top 10 tags
5. **Maintenance mode entry** — controlled access with password + key switch

No deep diagnostics on the field HMI — that's the remote operator console's job. The field HMI is for "eyes-on, hands-on" actions only.

### §13.2  Tier 2 — Remote Operator Console

Purpose: full operational visibility and control for NOC staff or customer operations team.

Platform: **Ignition Perspective** (web-based HMI) served from the L3 Gateway. Accessed via VPN from authorized workstations.

Screen library:
- Full site overview (single pane of glass)
- Per-skid detail views (CDU, Munters, Gensets A & B, Chiller, Switchgear)
- Cassette internals (15-rack grid with per-rack T, flow, current, status)
- Alarm management (ISA-18.2 compliant view, filter, ack, shelving)
- Trending (any tag, any time range, up to 7 years from historian)
- Operating mode selector (privileged access)
- Maintenance scheduler
- Reports (daily, weekly, monthly operational summaries)
- Work orders (linked to CMMS)

### §13.3  Tier 3 — Mobile Field App

Purpose: service technician's interface. Replaces paper worklists and radio calls.

Platform: native mobile (iOS + Android) or PWA. Backend via REST API from the L3 orchestrator.

Core features:
- Assigned work orders with turn-by-turn navigation to the part/asset
- Barcode / QR scan on any skid or part to pull up live telemetry and service history
- **Natural-language diagnostic assistant** — technician asks "what failed on Unit 3 last night" and the app retrieves the relevant telemetry window and event log, summarized by an LLM call (Claude or GPT-4 API). This is a genuine differentiator and a natural extension of the Mission Control HD platform experience.
- Photo capture + annotation attached to work orders
- Consumable inventory tracking
- Offline-capable for sites without connectivity; syncs when back online

---

## §14  REDUNDANCY, FAILURE MODES & GRACEFUL DEGRADATION

### §14.1  Component Redundancy Summary

| Component                     | Redundancy   | Failover time  | Manual intervention needed? |
|-------------------------------|--------------|----------------|-----------------------------|
| Jetson Orin BMS               | 1+1 active/standby | < 200 ms   | No                          |
| CDU pumps                     | N+1          | < 5 s          | No (auto)                   |
| Cartridge filters             | Duplex       | < 30 s (manual switchover on rising ΔP) | Yes (technician) |
| Gensets                       | 2N (1 run, 1 standby) | < 30 s (black-start of standby) | No (auto) |
| Ignition Gateway (L2/L3)      | Hot-standby  | < 30 s         | No                          |
| MQTT broker                   | Clustered (3 nodes, quorum) | < 10 s | No                   |
| Historian (L3)                | Local (InfluxDB on Jetson) + Ignition + Cloud | rolling | No |
| PTP grandmaster               | 1+1 redundant + GPS holdover | < 1 s | No |
| Protocol Gateway              | 1+1 hot-standby | < 250 ms   | No                          |
| Switchgear relays             | Main relay + backup protection via thermal / fuse | immediate | No |

### §14.2  Graceful Degradation Matrix

What operation is maintained when each subsystem fails:

| Failure                                | Cassette keeps operating? | How                                    |
|----------------------------------------|---------------------------|----------------------------------------|
| Cloud connection lost                  | YES                       | L2/L3 continue autonomously up to 30 d |
| L3 Ignition Gateway (both) lost        | YES (limited)             | Cassette BMS runs in local-only mode; no cross-skid orchestration; preserved operating state |
| Protocol Gateway (both) lost           | YES (cassette only)       | Cassette isolates; skids hold last safe state per their local interlocks |
| L2 Cassette BMS (both) lost            | NO                        | SIS holds cassette in safe hot-standby; operator intervention required |
| SIS trip                               | NO                        | Cassette in EMERGENCY_SHUTDOWN; see CAS-SIS-001 |
| One genset                             | YES                       | Other genset carries full load (2N sizing) |
| Both gensets                           | NO                        | BLACK_START sequence attempted; until restored, cassette shut down |
| CDU pump A or B                        | YES                       | N+1 pumps, instant takeover            |
| Absorption chiller                     | YES (reduced)             | If available: backup electric chiller (option) or site-provided CHW; if not: cassette derates to power that can be cooled |
| Munters                                | YES (reduced)             | Interior humidity rises; BMS alarms at 55% RH; cassette continues while dew point remains above cold-plate surface T (well-bounded) |
| Network segment                        | YES (local)               | Skids revert to local-PLC autonomous operation |

### §14.3  Black-Start Provisions

If the site experiences a total power loss:
- **24 VDC UPS** (INT §23) maintains SIS, VESDA, Novec panel, BMS, lighting for ≥ 2 hr
- **Gensets** can black-start from 24 VDC starter batteries (Cat standard)
- **Site orchestrator** has a BLACK_START mode (see CAS-MODES-001 §10) that sequences restoration

---

## §15  NETWORK ARCHITECTURE & SEGMENTATION

### §15.1  Network Zones (Purdue Model)

| Zone | Function | Devices | External connectivity |
|------|----------|---------|------------------------|
| Zone 0 (Safety) | SIS, gas detectors, E-stop | SIS PLC, gas monitors, ESD relays | Isolated from everything |
| Zone 1 (Process) | L0 field I/O | ADAM modules, TraceTek, VESDA | Only to Zone 2 via L1 PLCs |
| Zone 2 (Basic control) | L1 PLCs | Siemens S7s, Cat EMCPs, SEL relays | To Zone 3 via L2 Gateway only |
| Zone 3 (Site operations) | L2 Gateway, L3 Orchestrator | Ignition Gateway servers, Historian | To Zone 4 via firewall + data diode |
| Zone 3.5 (DMZ) | Jump server, VPN endpoint | Privileged access management | Between Zone 3 and Zone 4 |
| Zone 4 (Enterprise) | Cloud, L4 dashboards | Grafana, Timestream, customer portal | Public internet |

### §15.2  Physical Network Layout

Three physically separate Ethernet networks at the site:

1. **Process Bus (Zone 0 + 1 + 2)** — industrial Ethernet ring, PTP-aware switches, redundant (RSTP or PRP), dedicated VLANs per skid. Runs IEC 61850 GOOSE at sub-ms latency for switchgear trip signals.

2. **Control LAN (Zone 3)** — SCADA, historian, HMI, orchestrator. Connected to Process Bus via a single firewalled interface on the L2 Gateway.

3. **Business LAN (Zone 4)** — cloud connectivity via Starlink / fiber. Completely separate from Control LAN, connected only via one-way data diode (Waterfall Security or Owl Cyber Defense) for outbound telemetry.

### §15.3  Data Diode Specification

One-way hardware-enforced data flow from OT to IT:
- Product: **Waterfall Unidirectional Security Gateway** or **Owl Cyber Defense DualDiode**
- Outbound: telemetry (OPC UA / MQTT Sparkplug B subscriber on OT side → publisher on IT side)
- Inbound: nothing — cyber-physically impossible
- Firmware updates flow in through a separate, audited path: engineering USB with signed firmware + dual-approval reset via SIS-approved procedure

This eliminates the remote cyber attack vector entirely. It is the gold standard for oil & gas upstream OT networks and is a prerequisite for IEC 62443 SL-3 compliance.

---

## §16  BILL OF MATERIALS SUMMARY

Hardware items added by this document (beyond what is in existing Cassette BOM-001 Rev 2.2):

| Item                                                    | Qty | Vendor candidates                         | Notes |
|---------------------------------------------------------|-----|-------------------------------------------|-------|
| Ignition Edge server (L2 Gateway)                       | 2   | Advantech MIC-770, Siemens IPC847E       | Redundant pair |
| Ignition SCADA server (L3 Orchestrator)                 | 2   | Dell PowerEdge R750 rackmount            | Redundant pair, co-located |
| PTP grandmaster clock                                   | 2   | Meinberg LANTIME M1000, Microchip SyncServer S650 | With rooftop GPS antenna |
| Managed industrial Ethernet switches (PTP-aware)        | 6   | Hirschmann BOBCAT, Cisco IE-4000         | Ring topology |
| Siemens S7-1500 PLC (CDU skid)                          | 1   | 1515F-2 PN with expansion I/O             | [LONG LEAD]   |
| Cat NTE Gateway (J1939 → Modbus TCP/OPC UA)             | 2   | Cat OEM                                   | One per genset |
| Protective relays (switchgear)                          | 3+  | SEL-751, ABB REX615                       | Per feeder per final design |
| Data diode (OT → IT, one-way)                           | 1   | Waterfall Unidirectional Security Gateway, Owl DualDiode | Hardware-enforced |
| VisuNet GXP HMI (Class I Div 2 site)                    | 1   | Pepperl+Fuchs VisuNet GXP 15"            | Hazardous-area rated |
| Beijer X2 Extreme (unclassified site alternative)       | 1   | Beijer X2 Extreme 15"                     | Outdoor rated |
| Gas detector array (LEL, H₂S, CO)                       | 13  | MSA Ultima XIR, Dräger Polytron 8000     | Per CAS-SIS-001 |
| SIS-rated safety PLC                                    | 1   | Siemens S7-1500F, HIMA H51q, Emerson DeltaV SIS | Per CAS-SIS-001 |
| Industrial edge server (PM model runtime, if separated) | 1   | NVIDIA Jetson AGX Orin Developer Kit     | Beyond the 2× already in R15 |
| Cloud platform (managed Grafana, Timestream)            | —   | AWS / Azure / GCP                         | Service, not hardware |

Software licenses:
- Ignition SCADA — standard bundle (Vision + Perspective + Historian + OPC UA + Alarm Notification + Mobile) — 2 instances
- Ignition Edge — 2 instances (L2 Gateway primary + standby)
- Kepware KEPServerEX (optional if Ignition does not cover all protocols) — 1 instance + protocol suites
- TensorRT runtime — included with JetPack
- MLflow (open source, self-hosted)

---

## §17  OPEN ITEMS

| ID | Priority | Description | Owner | Notes |
|----|----------|-------------|-------|-------|
| CT-01 | P-0 | Absorption chiller vendor selection: confirm protocol (BACnet/IP vs Modbus TCP) and tag availability before contract | ADC ↔ Yazaki/Thermax/Carrier | Gates §4.5 |
| CT-02 | P-0 | SCADA platform commitment: Ignition vs alternatives (AVEVA, WinCC). Recommendation is Ignition; needs executive sign-off before integrator RFQ | ADC engineering | Gates §5.2, §6.1 |
| CT-03 | P-0 | Site systems integrator RFQ — based on this document, MODES-001, SIS-001, TAGS-001 | ADC ↔ Optimation, Wood, Burns & McDonnell (candidates) | 12-16 week engagement |
| CT-04 | P-1 | Protective relay final selection on 800 VDC main — SEL-751 DC application has limitations; may require custom engineering | ADC ↔ SEL FAE | Affects §4.6 |
| CT-05 | P-1 | Cat NTE Gateway — confirm J1939 tag mapping includes all CHP data (jacket heat rate, exhaust heat rate) | ADC ↔ Cat | Gates §4.4 |
| CT-06 | P-1 | Data diode procurement — Waterfall vs Owl cost comparison and customer acceptance per industry | ADC engineering | Gates §15.3 |
| CT-07 | P-1 | PM model training data — need baseline operational data from commissioning + 90 days to train asset-specific models | ADC ↔ integrator | Gates §12.2 |
| CT-08 | P-2 | Hazardous-area classification by deployment site — varies by customer (Class I Div 2 typical for oilfield) | ADC BD | Affects HMI selection |
| CT-09 | P-2 | Workload scheduler API surface — confirm which NVIDIA platform (SLURM vs BCM vs K8s) customers will use; each has different integration | ADC ↔ customer | Gates §11.2 |
| CT-10 | P-2 | CMMS integration — which customer CMMS platforms are in scope (Fiix, UpKeep, Maximo, Infor) | ADC BD | Affects §6.4 |
| CT-11 | P-2 | Time sync budget verification — confirm that all controllers meet their stated PTP class after procurement | ADC ↔ integrator | Gates §10 |
| CT-12 | P-3 | Digital twin physics model — requires engine curve data from Cat and absorption cycle model from chiller vendor | ADC engineering | Affects §6.2 |

---

## SUMMARY OF KEY DECISIONS

| # | Decision | Rationale |
|---|----------|-----------|
| 1 | Five-layer Purdue hierarchy | Standard ISA-95 pattern; recognized by industrial integrators and oil & gas OT auditors |
| 2 | Ignition SCADA as L2+L3 platform | Best-in-class MQTT Sparkplug B, protocol breadth, mature industrial references, open scripting |
| 3 | OPC UA as canonical namespace | IEC standard, vendor-neutral, enforceable security, strong tooling |
| 4 | MQTT Sparkplug B as telemetry transport | Efficient, industry-standard for industrial IoT, preserves context and birth certificates |
| 5 | PTP (IEEE 1588) for time sync | Forensic reconstruction requires sub-ms accuracy; NTP is insufficient |
| 6 | Jetson Orin dual-role (L1 I/O + L2 BMS + ML inference) | Leverages existing hardware; Orin's compute is otherwise idle |
| 7 | Three-tier HMI (field / remote / mobile) | Matches operator role separation; allows class-rated hardware where needed |
| 8 | Hardware data diode at OT/IT boundary | Required for IEC 62443 SL-3 and oil & gas customer acceptance; eliminates remote attack vector |
| 9 | Workload-aware feedforward control | Differentiator; enables 20% more compute per same hardware; patentable |
| 10 | SIS physically separate from BPCS | Required by IEC 61511, non-negotiable for oil & gas deployment |

---

**Cassette-CTRL-001 — Control & Data Architecture · Rev 1.1 · 2026-04-20**
**Scott Tomsu · scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana**
**CONFIDENTIAL**
