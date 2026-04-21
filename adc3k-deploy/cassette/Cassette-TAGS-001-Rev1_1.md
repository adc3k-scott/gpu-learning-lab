# Cassette — SITE TAG DICTIONARY & OPC UA NAMESPACE

**Document:** Cassette-TAGS-001
**Revision:** 1.1
**Date:** 2026-04-20
**Classification:** CONFIDENTIAL
**Status:** Released

**Companion documents:** Cassette-CTRL-001 Rev 1.1 · Cassette-MODES-001 Rev 1.1 · Cassette-SIS-001 Rev 1.1 · Cassette-CYBER-001 Rev 1.1 · Cassette-INT-001 Rev 3.0 · Cassette-ECP-001 Rev 3.0 · Cassette-ELEC-001 Rev 1.2 · Cassette-COOL-002 Rev 1.0 · Cassette-CDUSKID-001 Rev 1.0

| Rev | Date       | Description                                                                      |
|-----|------------|----------------------------------------------------------------------------------|
| 1.0 | 2026-04-20 | Initial release. Defines tag naming conventions, engineering-unit standards, data-type conventions, OPC UA namespace hierarchy (ISA-95 aligned), alarm-class conventions, archival policies, and Access Control Lists. Enumerates representative tag inventory across cassette + 4 skids. Full enumeration maintained in companion CSV artifact `cassette-tag-inventory-v1.0.csv` (~2,400 tags). |
| **1.1** | **2026-04-20** | **SKID-CDU namespace expanded per CDUSKID-001 Rev 1.0 equipment list and COOL-002 Rev 1.0 control interface. Tag inventory for skid PLC (Siemens S7-1500F) detailed at §14A. CASSETTE-CHW tags deprecated (no CHW inside cassette per ECP-001 Rev 3.0). CASSETTE-PG25-QD tags added for the two DN150 primary QDs at the CDU-end ECP. Deprecated tags flagged but retained for audit trail. Total active tag count ~2,440 (up from ~2,400 due to skid expansion).** |

**Prepared by:** Scott Tomsu · CEO / Chief Engineer
scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana

---

## TABLE OF CONTENTS

- §1  Scope & Purpose
- §2  Naming Convention
- §3  OPC UA Namespace Structure (ISA-95)
- §4  Engineering Units
- §5  Data Types & Signal Conventions
- §6  Tag Categories & Sampling Policy
- §7  Alarm Classes & Limits
- §8  Archival Policy
- §9  Access Control List (ACL) Conventions
- §10 Tag Inventory — Cassette Interior
- §11 Tag Inventory — CDU Skid
- §12 Tag Inventory — Munters Skid
- §13 Tag Inventory — Gensets
- §14 Tag Inventory — Absorption Chiller
- §15 Tag Inventory — Switchgear
- §16 Tag Inventory — Safety (SIS)
- §17 Calculated / Derived Tags
- §18 Governance & Version Control
- §19 Open Items

---

## §1  SCOPE & PURPOSE

### Scope

This document defines the complete tag namespace for a deployed Cassette edge AI compute node: every measurable and controllable quantity, its canonical OPC UA path, engineering unit, data type, range, alarm limits, archival retention, and access permissions.

The tag dictionary is **the contract** between the control systems integrator, the skid vendors, the historian platform, the HMI developer, the analytics team, and the customer. Every system that reads or writes data in the deployment must use these exact tag paths.

### Relationship to Other Documents

- **CTRL-001 §9.2** defines the OPC UA namespace structure at the template level. This document instantiates every tag under that structure.
- **MODES-001** references tags by path for interlock conditions and mode transition acceptance tests.
- **SIS-001** references tags by path for safety trip logic.
- **Companion CSV** `cassette-tag-inventory-v1.0.csv` is the machine-readable master. This Markdown document is the human-readable narrative framework and representative sampling. **When they disagree, the CSV is authoritative.**

### Volume

| Skid / Domain              | Approximate tag count |
|----------------------------|-----------------------|
| Cassette interior          | 860   |
| CDU skid                   | 280   |
| Munters skid               | 120   |
| Gensets (×2)               | 440   |
| Absorption chiller         | 180   |
| Switchgear                 | 230   |
| SIS                        | 90    |
| Calculated / derived       | 220   |
| **Total**                  | **~2,420** |

---

## §2  NAMING CONVENTION

### Principles

1. **Hierarchical** — path segments reflect physical and functional containment
2. **Human-readable** — any engineer reading a tag should understand what it measures without a lookup
3. **Unambiguous** — no two tags have the same path; no path collisions across vendors
4. **Stable** — tag paths do not change across revisions unless a major breaking-change is required (and then the old path is deprecated, not deleted, for 12 months)
5. **Vendor-agnostic** — the canonical tag path does not reflect the source protocol (OPC UA path = what it is, not how it arrived)

### Path Format

```
/Site/{site_id}/{Skid}/{Component}/{Instance}/{Measurement}
```

- `Site` — root for multi-site fleet (top of namespace)
- `{site_id}` — deployment identifier, uppercase, underscores (e.g., `LFT_WELLPAD_03`, `SHELL_GOM_FPS-17`)
- `{Skid}` — one of: `Cassette`, `CDU_Skid`, `Munters_Skid`, `Gensets`, `Chiller`, `Switchgear`, `Safety`, `Site` (site-level), `Calc` (calculated tags)
- `{Component}` — subsystem within skid (e.g., `Racks`, `Pumps`, `Heat_Recovery`)
- `{Instance}` — specific instance when multiple (e.g., `R1..R15`, `A/B`, `1..N`)
- `{Measurement}` — the quantity: PV (process variable), SP (setpoint), OUT (output), STS (status), ALM (alarm), CMD (command)

### Examples

```
/Site/LFT_WELLPAD_03/Cassette/Racks/R5/Supply_T
/Site/LFT_WELLPAD_03/CDU_Skid/Pumps/A/Speed_SP
/Site/LFT_WELLPAD_03/Gensets/A/Engine/RPM
/Site/LFT_WELLPAD_03/Switchgear/MainBreaker/Position_STS
/Site/LFT_WELLPAD_03/Safety/SIS/State
/Site/LFT_WELLPAD_03/Calc/CHP_Efficiency
```

### Suffix Glossary

| Suffix | Meaning                                  |
|--------|------------------------------------------|
| (none) | Primary measurement (PV implied)         |
| `_PV`  | Process variable (measured)              |
| `_SP`  | Setpoint (operator / orchestrator target)|
| `_OUT` | Controller output (PID output to actuator)|
| `_CMD` | Command (discrete: START, STOP, RESET)   |
| `_STS` | Status (discrete state: RUNNING, FAULT)  |
| `_ALM` | Alarm flag (boolean)                     |
| `_FB`  | Feedback (actuator position feedback)    |
| `_QUAL`| Quality / confidence indicator           |
| `_HH`  | High-high alarm limit                    |
| `_H`   | High alarm limit                         |
| `_L`   | Low alarm limit                          |
| `_LL`  | Low-low alarm limit                      |
| `_AVG` | Time-windowed average (e.g., `_AVG_5M`)  |
| `_TOT` | Totalizer (e.g., kWh, m³)                |
| `_FOR` | Forecast (future-looking value)          |

### Tag Path Length

- Maximum tag path: 200 characters
- Maximum single segment: 32 characters
- Lowercase, uppercase, digits, and underscore only; no spaces, dots, or special characters

---

## §3  OPC UA NAMESPACE STRUCTURE (ISA-95)

### Hierarchy

The namespace follows ISA-95 equipment hierarchy:

```
Enterprise ──▶ Site ──▶ Area (skid) ──▶ Unit (component) ──▶ EquipmentModule (instance) ──▶ Tag
```

Mapped to OPC UA:

```
Root
└── Objects
    └── Site/{site_id}                      ← ISA-95 "Site" level
        ├── Cassette                        ← "Area"
        │   ├── Racks                       ← "Unit"
        │   │   ├── R1..R15                 ← "EquipmentModule"
        │   │   │   ├── Supply_T            ← "Tag"
        │   │   │   ├── Return_T
        │   │   │   ├── Flow
        │   │   │   ├── Current
        │   │   │   └── ...
        │   │   └── (Racks summary)
        │   ├── Environmental
        │   ├── Fire
        │   └── BMS
        ├── CDU_Skid
        ├── Munters_Skid
        ├── Gensets
        ├── Chiller
        ├── Switchgear
        ├── Safety
        └── Calc
```

### Standard Object Types

Custom OPC UA Object Types defined in the namespace:
- `CassetteRackType` — supply_t, return_t, flow, current, vibration, status, alarm
- `PumpType` — speed, current, vibration, status, alarm
- `GensetType` — rpm, load, fuel_rate, jacket_t, status, alarm
- `BreakerType` — position_sts, voltage, current, trip_count
- `HeatExchangerType` — primary_in_t, primary_out_t, secondary_in_t, secondary_out_t, flow

Object Types make HMI development and analytics templating far more efficient — one template per object type covers every instance.

---

## §4  ENGINEERING UNITS

All tags carry engineering units per OPC UA EUInformation (IEC 62541-8) referencing UNECE Common Codes.

### Unit Standards Adopted

| Quantity | Unit | UNECE code | Notes |
|----------|------|-----------|-------|
| Temperature | °C | CEL | Degrees Celsius |
| Pressure | bar | BAR | Gauge unless noted `_ABS` |
| Differential pressure | kPa | KPA | For filters, HXs |
| Flow (liquid) | LPM | L/MIN (proprietary) | Liters per minute |
| Flow (air) | SCFM | FT3/MIN | Standard cubic feet per minute (at 14.7 psia, 60 °F) |
| Electrical — voltage | V | VLT | Volts |
| Electrical — current | A | AMP | Amperes |
| Electrical — power | kW | KWT | Kilowatts real; `kVA` for apparent; `kVAR` for reactive |
| Electrical — energy | kWh | KWH | Kilowatt-hours |
| Rotational speed | rpm | RPM | Revolutions per minute |
| Gas concentration (combustible) | % LEL | P1 | Percent of lower explosive limit |
| Gas concentration (toxic) | ppm | 59 | Parts per million |
| Humidity | %RH | P1 | Percent relative humidity |
| Frequency | Hz | HTZ | Hertz |
| Resistance | MΩ | MOH | Megohms |
| Concentration (LiBr) | % | P1 | Percent by mass |
| Vibration | mm/s | 4H | Velocity RMS |
| Vibration (acceleration) | g | MGR | Gravitational acceleration |
| Level | % | P1 | Percent of tank height |
| Position | % | P1 | Percent of travel (0 = closed, 100 = open) |

### Units Forbidden (do not use)

- °F — all temperature in °C (convert at HMI for display if needed)
- psi — pressure in bar (gauge) or kPa (differential)
- GPM — flow in LPM
- BTU/hr — power in kW (multiply by 0.293)
- RT (refrigeration tons) — cooling capacity in kW (multiply by 3.517)

Consistent units across the fleet eliminate a common source of control errors.

---

## §5  DATA TYPES & SIGNAL CONVENTIONS

### OPC UA Data Types

| Tag type       | OPC UA type | Width | Use |
|----------------|-------------|-------|-----|
| Analog float   | `Float`     | 32-bit | Most PVs (temperature, pressure, flow) |
| Analog double  | `Double`    | 64-bit | High-precision (totalizers, GPS coordinates) |
| Integer count  | `Int32`     | 32-bit | Alarm counts, event counters |
| Unsigned count | `UInt32`    | 32-bit | Runtime hours, motor starts |
| Boolean        | `Boolean`   | 1-bit  | Status, alarm flags, commands |
| State enum     | `Int32` with named enumeration | 32-bit | Mode states, equipment states |
| Timestamp      | `DateTime`  | 64-bit | Event times, last-update |
| String         | `String`    | variable | Alarm messages, operator notes, fault codes |

### Status Conventions

Boolean status:
- `true` = "good / running / normal / closed (energized coil)"
- `false` = "bad / stopped / abnormal / tripped / open"

Exception: `_ALM` flags where `true` = alarm active (inverted convention). All `_ALM` tags have explicit documentation.

### State Machines

Mode states use named integer enumerations. Example — Cassette operating state per MODES-001:

```
0: COLD_OFF
1: COLD_START
2: WARM_START
3: NORMAL
4: DEGRADED
5: HOT_STANDBY
6: SERVICE
7: PLANNED_SHUTDOWN
8: EMERGENCY_SHUTDOWN
9: BLACK_START
```

Enumerations published as OPC UA `EnumDefinition` structures; clients parse them automatically.

### Quality Codes

OPC UA StatusCode on every tag:
- `Good` — within calibrated range, sensor operational
- `Bad_OutOfService` — sensor offline for maintenance
- `Bad_NoCommunication` — PLC disconnected
- `Uncertain_SensorCalibration` — calibration overdue
- `Uncertain_LastUsableValue` — held at last value on communication loss

Quality flows with the tag. Analytics must check quality before trusting values.

---

## §6  TAG CATEGORIES & SAMPLING POLICY

### Category A — Fast Analog

Rack temperatures, pump speeds, bus voltages/currents, flow rates, vibration RMS.
- Sample rate: 1 Hz continuous
- Transport: OPC UA subscription with 1 Hz publish; MQTT Sparkplug B DDATA
- Historian: raw 1 Hz × 30 days local; 1 min average × 1 year; 1 hour average × 7 years

### Category B — Slow Analog

Ambient temperature/humidity, tank levels, totalizers, filter hours.
- Sample rate: 1/min
- Transport: OPC UA subscription with 60 s publish
- Historian: 1 min × 7 years

### Category C — Events / Discrete

Alarms, status changes, operator actions, mode transitions.
- Sample rate: event-driven
- Transport: MQTT Sparkplug B DDATA with timestamp; OPC UA Event notifications
- Historian: all events forever (compliance / forensics)

### Category D — Forensic Burst

High-speed ring buffer data captured during trip events.
- Sample rate: 1 kHz ring, flushed on trigger
- Transport: file upload post-trigger
- Historian: 30 s window × 90 days

### Category E — Electrical Protective

Breaker trip waveforms, protective-relay event records.
- Sample rate: 4 kHz during event
- Transport: IEC 61850 COMTRADE file via MMS
- Historian: 90 days

### Category F — Calculated / Derived

Efficiency metrics, rolling averages, forecast values, ML model outputs.
- Sample rate: 1/min (typical)
- Transport: published by orchestrator
- Historian: 1 min × 7 years

### Category G — Configuration / Setpoints

Operator-entered setpoints, control parameters.
- Sample rate: on-change
- Transport: OPC UA write-through from HMI
- Historian: all changes logged with operator ID

---

## §7  ALARM CLASSES & LIMITS

### Alarm Classification (ISA-18.2)

| Priority | Code | Max active (flood threshold) | Response time | Annunciation |
|----------|------|------------------------------|---------------|--------------|
| Urgent   | U    | 2 simultaneous               | < 1 min       | Audible + red flashing + SMS to on-call |
| High     | H    | 10                           | < 10 min      | Audible + orange + email to operator |
| Medium   | M    | 25                           | < 1 hr        | Yellow indicator + HMI queue |
| Low / Info | L  | unlimited                    | end of shift  | Log only, visible in HMI list |

### Limit Naming Convention

For any analog tag `X`, the following limit tags may exist:
- `X_HH` — high-high alarm (Urgent typical)
- `X_H`  — high alarm (High typical)
- `X_L`  — low alarm (High typical)
- `X_LL` — low-low alarm (Urgent typical)
- `X_DB` — deadband (hysteresis for return-to-normal)

Limits are read from OPC UA tags, not hardcoded in HMI or logic — enables field tuning by engineer with appropriate privilege.

### Example Alarm Tree

For `/Site/{id}/Cassette/Racks/R5/Supply_T`:

| Tag | Value | Class | Message |
|-----|-------|-------|---------|
| `Supply_T_H` | 48 | High | "R5 supply temperature high" |
| `Supply_T_HH` | 52 | Urgent | "R5 supply temperature critical — cooling impaired" |
| `Supply_T_L` | 35 | Medium | "R5 supply temperature low — possible overcooling" |
| `Supply_T_LL` | 30 | High | "R5 supply temperature very low — verify chiller/CDU" |
| `Supply_T_DB` | 1.0 °C | — | Deadband for return-to-normal |

Typical limits for cassette racks come from NVIDIA NVL72 vendor specifications; to be finalized per open item TG-01.

---

## §8  ARCHIVAL POLICY

| Tier | Storage | Retention | Compression | Use |
|------|---------|-----------|-------------|-----|
| Local fast (Jetson InfluxDB) | SSD on Jetson Orin | 30 days raw | None | Operator real-time trending, BMS internal |
| Site historian (Ignition Tag Historian) | L3 server SSD + 1 y snapshot | 1 year @ 1 min; raw 1 Hz × 90 days | Loss-less (gorilla/zstd) | Engineering analysis, PM model training |
| Cloud long-term (TimescaleDB / AWS Timestream) | Managed cloud | 7 years @ 1 min; 12 years @ 1 hour | Columnar compressed | Warranty, ESG reporting, fleet analytics |
| Event store | Same tiers | 7 years all events | — | Compliance, forensics |
| Forensic burst files | Object storage (S3) | 90 days | gzip | Post-trip analysis |

### Retention by Category

| Category | Local | Site | Cloud |
|----------|-------|------|-------|
| A Fast analog | 30 d @ 1 Hz | 90 d @ 1 Hz, 1 y @ 1 min | 7 y @ 1 min |
| B Slow analog | 30 d @ 1 min | 1 y @ 1 min | 7 y @ 1 min, 12 y @ 1 h |
| C Events | 30 d | 1 y | 7 y |
| D Forensic burst | 7 d | 90 d | (on-demand upload) |
| E Electrical protective | 30 d | 90 d | on-demand |
| F Calculated | 30 d @ 1 min | 1 y | 7 y |
| G Config / setpoints | forever | forever | forever |

---

## §9  ACCESS CONTROL LIST (ACL) CONVENTIONS

### Roles

| Role | Description |
|------|-------------|
| `Viewer` | Read any non-secure tag; no write |
| `Operator` | Read all; write operator-level setpoints (NORMAL ↔ HOT_STANDBY, ack alarms) |
| `Supervisor` | Operator + write supervisor setpoints (mode transitions to SERVICE, PLANNED_SHUTDOWN) |
| `Engineer` | Supervisor + write engineering parameters (PID gains, alarm limits, calibration) |
| `Integrator` | Engineer + write structural configuration (tag definitions, not during operations) |
| `SIS_Authorized` | Special — write to SIS bypass, reset. Requires physical key + authentication |
| `System` | Internal: orchestrator, BMS, gateway services |

### ACL Conventions

Every tag has four ACL attributes:
- `read_min_role` — minimum role to read
- `write_min_role` — minimum role to write (null if read-only)
- `audit_write` — boolean; if true, every write is logged with who/when/old/new
- `encrypt_in_transit` — boolean; if true, OPC UA sessions must use Basic256Sha256 encryption

### Defaults by Category

| Category | Read | Write | Audit | Encrypt |
|----------|------|-------|-------|---------|
| Process variable (PV) | Viewer | — | — | false |
| Setpoint (SP) | Viewer | Operator (mostly) | true | true |
| Alarm limit | Viewer | Engineer | true | true |
| PID tuning | Engineer | Engineer | true | true |
| Safety-related | Viewer | SIS_Authorized | true | true |
| Calibration | Engineer | Engineer | true | true |
| Configuration | Integrator | Integrator | true | true |

### Privileged Operations Requiring Multi-factor

- SIS bypass engage
- SIS trip reset (requires hardware key + engineer credential)
- Mode transition to BLACK_START
- Firmware update approval
- Tag definition change (structural)

---

## §10  TAG INVENTORY — CASSETTE INTERIOR

### §10.1  Per-Rack Tags (×15 racks, R1..R15)

For racks R1 through R13 (compute racks NVL72) — 52 tags per rack:

| Tag (relative path under `.../R{n}/`) | Type | Unit | Range | Cat | Default alarm |
|----------------------------------------|------|------|-------|-----|---------------|
| `Supply_T` | Float | °C | 30–55 | A | H 48 / HH 52 |
| `Return_T` | Float | °C | 45–65 | A | H 58 / HH 62 |
| `DT` | Float | °C | 0–25 | A+F | — |
| `Flow` | Float | LPM | 100–200 | A | L 110 / LL 100 |
| `Flow_SP` | Float | LPM | 100–200 | G | — |
| `Current_Rack` | Float | A | 0–2,500 | A | H 2,400 |
| `Power_Rack` | Float | kW | 0–200 | A+F | H 190 |
| `Bus_V` | Float | V DC | 750–850 | A | L 760 / H 840 |
| `Vib_Pump_A` | Float | mm/s | 0–20 | A | H 12 / HH 15 |
| `Vib_Pump_B` | Float | mm/s | 0–20 | A | H 12 / HH 15 |
| `Leak_Detect` | Bool | — | 0/1 | C | Urgent on true |
| `Breaker_Sts` | Bool | — | 0/1 | C | — |
| `Breaker_Cmd` | Bool | — | 0/1 | G | — |
| `UQD_A_Valve_FB` | Float | % | 0–100 | A | — |
| `UQD_B_Valve_FB` | Float | % | 0–100 | A | — |
| `UQD_A_Cmd` | Float | % | 0–100 | G | — |
| `UQD_B_Cmd` | Float | % | 0–100 | G | — |
| `GPU_Count_Healthy` | Int32 | count | 0–72 | C | L 68 |
| `GPU_Max_T` | Float | °C | 30–90 | A | H 85 / HH 88 |
| `GPU_Mean_T` | Float | °C | 30–80 | A+F | — |
| `Shelf_A_Efficiency` | Float | % | 90–99 | A | L 94 |
| `Shelf_B_Efficiency` | Float | % | 90–99 | A | L 94 |
| ... (additional telemetry via Redfish) | | | | | |

For R14 (InfiniBand switches) — different tag set:
- QM9700 link status per port (×64 per switch)
- Port error counters
- Switch fan speeds
- Switch temperatures
- Switch power consumption

For R15 (management + storage) — different tag set:
- Jetson A/B state
- Jetson CPU, GPU, memory utilization
- Storage volume capacities
- Backup status

Per-rack count: ~52 tags × 13 compute + ~80 × 1 InfiniBand + ~50 × 1 management = ~807 rack-level tags.

### §10.2  Environmental

| Tag (under `Cassette/Environmental/`) | Type | Unit | Range | Cat |
|----------------------------------------|------|------|-------|-----|
| `Interior_T_{1..4}` | Float | °C | 15–45 | A |
| `Interior_RH_{1..2}` | Float | %RH | 20–80 | A |
| `Interior_Pressure_Diff` | Float | kPa | -0.5 to +1.0 | A |
| `Interior_Tilt_X` | Float | ° | -5 to +5 | A |
| `Interior_Tilt_Y` | Float | ° | -5 to +5 | A |
| `Shock_Peak` | Float | g | 0–10 | A |
| `Ambient_T` | Float | °C | -10 to 55 | B |
| `Ambient_RH` | Float | %RH | 0–100 | B |
| `Ambient_Pressure` | Float | kPa | 95–105 | B |
| `Wind_Speed` (if external met station) | Float | m/s | 0–50 | B |

### §10.3  Fire

| Tag (under `Cassette/Fire/`) | Type | Cat |
|-------------------------------|------|-----|
| `VESDA_Alarm_Level` | Int32 (0–4: none, aux, pre, F1, F2) | C |
| `VESDA_Sample_Flow_{1..2}` | Float %RH | B |
| `VESDA_Filter_Status` | Int32 | C |
| `Novec_Panel_Status` | Int32 | C |
| `Novec_Discharge_Cmd` | Bool | C |
| `Heat_Detect_{1..6}` | Bool | C |

### §10.4  BMS

| Tag (under `Cassette/BMS/`) | Type | Cat |
|------------------------------|------|-----|
| `State` | Int32 enum (10 states per MODES-001) | C |
| `Active_Alarms_Count` | Int32 | A |
| `Unack_Alarms_Count` | Int32 | A |
| `Primary_Jetson` | Int32 (A=1, B=2) | C |
| `Jetson_A_CPU_Util` | Float % | A |
| `Jetson_A_GPU_Util` | Float % | A |
| `Jetson_A_Memory_Used` | Float GB | A |
| `Jetson_B_*` (mirror of A) | ... | A |
| `Gateway_Heartbeat` | DateTime | C |
| `Last_Command_From` | String (operator ID) | C |
| `Last_Command_Time` | DateTime | C |

### §10.5  PG25 QD Plate (Rev 1.1 — New)

Under `Cassette/PG25_QD/` — two DN150 primary quick-disconnects at the CDU-end ECP per INT-001 Rev 3.0 §14 and ECP-001 Rev 3.0 §7:

| Tag | Type | Unit | Range | Cat | Default alarm |
|-----|------|------|-------|-----|---------------|
| `Supply_QD_Pressure` | Float | bar | 0–10 | A | L 1.5 / H 7 |
| `Return_QD_Pressure` | Float | bar | 0–10 | A | L 1.5 / H 7 |
| `Supply_QD_Temperature` | Float | °C | 30–70 | A | H 50 / HH 53 |
| `Return_QD_Temperature` | Float | °C | 30–70 | A | H 62 / HH 65 |
| `Supply_QD_Seated` | Bool | — | 0/1 | C | Urgent on 0 |
| `Return_QD_Seated` | Bool | — | 0/1 | C | Urgent on 0 |
| `QD_Plate_Leak_Detect` | Bool | — | 0/1 | C | Urgent on true |
| `Fill_Port_Valve_Status` | Bool | — | 0/1 | C | Non-zero out of commissioning |

### §10.6  Deprecated Tags (Rev 1.1)

The following Rev 1.0 tags are deprecated in Rev 1.1 and return `null` + diagnostic code 0x1004 (`TAG_DEPRECATED_SEE_REV_1_1`). Consumers must migrate by 2027-04-20 (12-month window per §9 ACL conventions).

| Deprecated Tag | Reason | Replacement |
|----------------|--------|-------------|
| `Cassette/CHW_Supply/Flow` | No CHW inside Cassette (ECP-001 Rev 3.0) | `CDU_Skid/Secondary/Flow_Inlet` |
| `Cassette/CHW_Supply/T` | Same | `CDU_Skid/Secondary/T_Inlet` |
| `Cassette/CHW_Return/Flow` | Same | `CDU_Skid/Secondary/Flow_Outlet` |
| `Cassette/CHW_Return/T` | Same | `CDU_Skid/Secondary/T_Outlet` |
| `Cassette/CDU_Internal/*` (all) | No internal CDU (INT-001 Rev 3.0 §13 DELETED) | `CDU_Skid/*` (external) |
| `Cassette/ECP/CHW_Penetration_*` | Penetrations replaced by PG25 QDs | `Cassette/PG25_QD/*` |

---

## §11  TAG INVENTORY — CDU SKID

> **Rev 1.1 expansion note.** CDUSKID-001 Rev 1.0 specifies **3 primary pumps (N+1) + 3 secondary pumps (N+1)** for a total of 6 pumps. The §11.1 table below lists representative tags for one pump; replicate across all six pumps (`Pumps/P1A`, `P1B`, `P1C` for primary; `Pumps/P2A`, `P2B`, `P2C` for secondary). Additional Rev 1.1 tag groups added: §11.6 Strainer & Filtration, §11.7 Stratification Baffles & Diffusers, §11.8 Skid MCC & VFDs. Full enumeration in companion CSV `cassette-tag-inventory-v1.1.csv` (~2,440 tags).

### §11.1  Pumps (×2)

For each of pumps A and B, under `CDU_Skid/Pumps/{A,B}/`:

| Tag | Type | Unit | Cat | Default alarm |
|-----|------|------|-----|---------------|
| `Speed_PV` | Float | % | A | — |
| `Speed_SP` | Float | % | G | — |
| `Current_PV` | Float | A | A | H per nameplate |
| `Voltage_PV` | Float | V AC | A | — |
| `Power_PV` | Float | kW | A+F | — |
| `Vib_X` | Float | mm/s | A | H 10 / HH 15 |
| `Vib_Y` | Float | mm/s | A | H 10 / HH 15 |
| `Vib_Z` | Float | mm/s | A | H 10 / HH 15 |
| `Bearing_T_DE` | Float | °C | A | H 85 / HH 95 |
| `Bearing_T_NDE` | Float | °C | A | H 85 / HH 95 |
| `Suction_P` | Float | bar | A | L 0.5 / LL 0.3 |
| `Discharge_P` | Float | bar | A | H 6 / HH 7 |
| `DP` | Float | bar | A+F | — |
| `Status` | Int32 enum (STOPPED, STARTING, RUNNING, FAULT) | C | — |
| `Start_Cmd` | Bool | — | G | — |
| `Stop_Cmd` | Bool | — | G | — |
| `Fault_Code` | Int32 | C | — |
| `Run_Hours` | UInt32 | hr | B | — |
| `Start_Count` | UInt32 | count | B | — |

### §11.2  Heat Exchanger

Under `CDU_Skid/HX/`:

| Tag | Type | Unit | Cat |
|-----|------|------|-----|
| `Primary_Inlet_T` | Float | °C | A |
| `Primary_Outlet_T` | Float | °C | A |
| `Primary_Flow` | Float | LPM | A |
| `Secondary_Inlet_T` | Float | °C | A |
| `Secondary_Outlet_T` | Float | °C | A |
| `Secondary_Flow` | Float | LPM | A |
| `Approach_T` | Float | °C | A+F | Calculated as Secondary_Outlet_T − Primary_Outlet_T |
| `Heat_Duty` | Float | kW | A+F | Calculated |

### §11.3  Filters (Duplex)

Under `CDU_Skid/Filters/{A,B}/`:

| Tag | Type | Unit |
|-----|------|------|
| `DP` | Float | kPa |
| `InService` | Bool | — |
| `Change_Due` | Bool | — (derived from DP trend) |

### §11.4  Buffer Tank

Under `CDU_Skid/BufferTank/`:

| Tag | Type | Unit |
|-----|------|------|
| `Level` | Float | % |
| `T_Top` | Float | °C |
| `T_Mid` | Float | °C |
| `T_Bottom` | Float | °C |
| `Stratification_Index` | Float | °C (T_Top − T_Bottom) |
| `Thermal_Capacity_Remaining` | Float | kWh (derived) |

### §11.5  Expansion Tank & Misc

Under `CDU_Skid/Aux/`:

| Tag | Type | Unit |
|-----|------|------|
| `Expansion_Tank_Level` | Float | % |
| `Expansion_Tank_Pressure` | Float | bar |
| `Air_Separator_Status` | Bool | — |
| `Glycol_Concentration` | Float | % (from field meter if fitted; else manual entry) |
| `Loop_pH` | Float | — (if online analyzer) |
| `Loop_Conductivity` | Float | µS/cm |

### §11.6  Strainer & Filtration (Rev 1.1)

Under `CDU_Skid/Filtration/`:

| Tag | Type | Unit | Notes |
|-----|------|------|-------|
| `Duplex_Strainer_Basket_A_DP` | Float | bar | Alarm H 0.3 |
| `Duplex_Strainer_Basket_B_DP` | Float | bar | Alarm H 0.3 |
| `Duplex_Strainer_Active_Basket` | Int32 | — | A=1, B=2 |
| `Cart_Filter_1_DP` | Float | bar | Alarm H 0.5 |
| `Cart_Filter_2_DP` | Float | bar | Alarm H 0.5 |
| `Cart_Filter_3_DP` | Float | bar | Alarm H 0.5 |
| `Cart_Filter_{1,2,3}_InService` | Bool | — | Min 1 true at all times |
| `Cart_Filter_{1,2,3}_Bypass_Cmd` | Bool | — | Service operation |

### §11.7  Buffer Tank Stratification & Diffusers (Rev 1.1)

Under `CDU_Skid/BufferTank/Detail/`:

| Tag | Type | Unit |
|-----|------|------|
| `T_Stack_1_Top` | Float | °C |
| `T_Stack_2` | Float | °C |
| `T_Stack_3_Mid` | Float | °C |
| `T_Stack_4` | Float | °C |
| `T_Stack_5_Bot` | Float | °C |
| `Inlet_Diffuser_Flow` | Float | LPM |
| `Outlet_Diffuser_Flow` | Float | LPM |
| `Thermal_Ride_Through_Remaining` | Float | s (derived from stack T + flow) |

### §11.8  Skid MCC & VFDs (Rev 1.1)

Under `CDU_Skid/Electrical/`:

| Tag | Type | Unit |
|-----|------|------|
| `Main_Breaker_Status` | Bool | — |
| `Main_Breaker_Current` | Float | A |
| `VFD_{P1A..P2C}_Status` | Int32 enum | — |
| `VFD_{P1A..P2C}_Output_Hz` | Float | Hz |
| `VFD_{P1A..P2C}_Output_Current` | Float | A |
| `VFD_{P1A..P2C}_DC_Bus_V` | Float | V |
| `VFD_{P1A..P2C}_Motor_Torque` | Float | % |
| `VFD_{P1A..P2C}_Fault_Code` | Int32 | — |
| `Ground_Loop_Z` | Float | Ω |
| `Arc_Flash_Incident_E` | Float | cal/cm² (from static analysis, ref only) |

---

## §12  TAG INVENTORY — MUNTERS SKID

Under `Munters_Skid/`:

| Path | Tag | Unit | Cat |
|------|-----|------|-----|
| `Process_Air/` | `Supply_T` | °C | A |
|                | `Supply_RH` | %RH | A |
|                | `Supply_Flow` | SCFM | A |
|                | `Return_T` | °C | A |
|                | `Return_RH` | %RH | A |
| `Reactivation/`| `Heater_T_PV` | °C | A |
|                | `Heater_T_SP` | °C | G |
|                | `Heater_Status` | Int32 | C |
|                | `Exhaust_T` | °C | A |
| `Rotor/`       | `Speed_PV` | rpm | A |
|                | `Speed_SP` | rpm | G |
|                | `Position` | ° | A |
| `Filters/`     | `Pre_Filter_DP` | kPa | A |
|                | `HEPA_Filter_DP` | kPa | A |
| `Status/`      | `State` | Int32 | C |
|                | `Fault_Code` | Int32 | C |
|                | `Run_Hours` | UInt32 | B |

---

## §13  TAG INVENTORY — GENSETS (×2)

For each of gensets A and B, under `Gensets/{A,B}/`:

### §13.1  Engine

Under `Gensets/{A,B}/Engine/`:

| Tag | Type | Unit | Cat |
|-----|------|------|-----|
| `RPM` | Float | rpm | A |
| `Load_Pct` | Float | % | A |
| `Load_kW` | Float | kW | A |
| `Fuel_Rate` | Float | Nm³/h | A |
| `Fuel_Consumption_Tot` | Double | Nm³ | B |
| `Oil_P` | Float | bar | A |
| `Oil_T` | Float | °C | A |
| `Jacket_T_In` | Float | °C | A |
| `Jacket_T_Out` | Float | °C | A |
| `Intake_Air_T` | Float | °C | A |
| `Intake_Manifold_P` | Float | bar | A |
| `Knock_Level` | Float | — | A |
| `Hours_Run` | UInt32 | hr | B |
| `Start_Count` | UInt32 | count | B |
| `Start_Cmd` | Bool | — | G |
| `Stop_Cmd` | Bool | — | G |
| `State` | Int32 enum (OFF, STARTING, RUNNING, LOADED, COOLDOWN, FAULT) | C |

### §13.2  Exhaust & Heat Recovery

Under `Gensets/{A,B}/Exhaust/`:

| Tag | Type | Unit | Cat |
|-----|------|------|-----|
| `T_Pre_Turbo` | Float | °C | A |
| `T_Post_Turbo` | Float | °C | A |
| `T_Post_HX` | Float | °C | A |
| `Back_P` | Float | kPa | A |
| `HR_Jacket_Flow` | Float | LPM | A |
| `HR_Jacket_kW` | Float | kW | A+F |
| `HR_Exhaust_kW` | Float | kW | A+F |
| `HR_Total_kW` | Float | kW | A+F |

### §13.3  Alternator

Under `Gensets/{A,B}/Alternator/`:

| Tag | Type | Unit | Cat |
|-----|------|------|-----|
| `Voltage_L1`, `Voltage_L2`, `Voltage_L3` | Float | V AC | A |
| `Current_L1`, `Current_L2`, `Current_L3` | Float | A | A |
| `Frequency` | Float | Hz | A |
| `Power_Factor` | Float | — | A |
| `Real_Power` | Float | kW | A |
| `Reactive_Power` | Float | kVAR | A |
| `Winding_T` | Float | °C | A |
| `Bearing_T` | Float | °C | A |

### §13.4  Breaker

Under `Gensets/{A,B}/Breaker/`:

| Tag | Type | Cat |
|-----|------|-----|
| `Position_STS` | Bool | C |
| `Open_Cmd` | Bool | G |
| `Close_Cmd` | Bool | G |
| `Sync_Check_STS` | Bool | C |
| `Trip_Count` | UInt32 | B |
| `Last_Trip_Reason` | String | C |

---

## §14  TAG INVENTORY — ABSORPTION CHILLER

Under `Chiller/`:

| Tag | Type | Unit | Cat |
|-----|------|------|-----|
| `CHW_Supply_T` | Float | °C | A |
| `CHW_Return_T` | Float | °C | A |
| `CHW_Flow` | Float | LPM | A |
| `CHW_Cooling_kW` | Float | kW | A+F |
| `Heat_Input_kW` | Float | kW | A |
| `Generator_T` | Float | °C | A |
| `Condenser_T` | Float | °C | A |
| `Evaporator_T` | Float | °C | A |
| `Absorber_T` | Float | °C | A |
| `LiBr_Concentration` | Float | % | A |
| `Solution_Pump_Status` | Bool | C |
| `Solution_Level` | Float | % | A |
| `COP` | Float | — | F | Cooling_kW / Heat_Input_kW |
| `State` | Int32 enum | C |
| `Fault_Code` | Int32 | C |
| `Alarm_Codes` | Int32 bitmask | C |
| `Hours_Run` | UInt32 | B |

---

## §15  TAG INVENTORY — SWITCHGEAR

Under `Switchgear/`:

### §15.1  Main Breaker

Under `Switchgear/MainBreaker/`:

| Tag | Type | Cat |
|-----|------|-----|
| `Position_STS` | Bool | C |
| `Trip_Cmd` | Bool | G |
| `Close_Cmd` | Bool | G |
| `Racked_In_STS` | Bool | C |
| `Local_Remote_STS` | Bool | C |
| `Trip_Time_Last` | Float ms | C |
| `Trip_Count` | UInt32 | B |

### §15.2  Bus Metering

Under `Switchgear/Bus/`:

| Tag | Type | Unit | Cat |
|-----|------|------|-----|
| `Voltage_DC` | Float | V | A |
| `Current_Total` | Float | A | A |
| `Power_Total` | Float | kW | A |
| `Energy_Today_kWh` | Float | kWh | B |
| `Energy_Total_kWh` | Double | kWh | B |
| `Ripple_Voltage` | Float | V RMS | A |
| `Insulation_Resistance` | Float | MΩ | A |

### §15.3  Per-Feeder (×15)

Under `Switchgear/Feeders/R{1..15}/`:

| Tag | Type | Unit | Cat |
|-----|------|------|-----|
| `Current` | Float | A | A |
| `Power` | Float | kW | A |
| `Breaker_Sts` | Bool | — | C |
| `Breaker_Cmd_Open` | Bool | — | G |
| `Breaker_Cmd_Close` | Bool | — | G |
| `Fault_Code` | Int32 | — | C |

### §15.4  Protective Relays

Under `Switchgear/Relays/{SEL_xxx}/`:

| Tag | Type | Cat |
|-----|------|-----|
| `Relay_Healthy` | Bool | C |
| `Event_Count_24h` | Int32 | C |
| `Last_Event_Type` | String | C |
| `Last_Event_Time` | DateTime | C |
| `50_Pickup` | Bool | C |
| `51_Pickup` | Bool | C |
| `87_Pickup` | Bool | C |
| `27_Pickup` | Bool | C |
| `59_Pickup` | Bool | C |
| `AFD_Pickup` | Bool | C |

---

## §16  TAG INVENTORY — SAFETY (SIS)

Under `Safety/`, **read-only** from BPCS:

### §16.1  SIS State

Under `Safety/SIS/`:

| Tag | Type | Cat |
|-----|------|-----|
| `State` | Int32 enum (ARMED, TRIPPED, BYPASSED, SELFTEST, FAULT) | C |
| `Last_Trip_Reason` | String | C |
| `Last_Trip_Time` | DateTime | C |
| `Active_SIF_Trips` | Int32 bitmask (bit per SIF per SIS-001) | C |
| `Bypasses_Active` | Int32 bitmask | C |
| `Self_Test_OK` | Bool | C |
| `Next_Proof_Test_Due` | DateTime | B |

### §16.2  Gas Detection

Under `Safety/GasDetect/`:

| Tag | Type | Unit | Cat |
|-----|------|------|-----|
| `LEL_{01..06}` | Float | %LEL | A |
| `H2S_{01..04}` | Float | ppm | A |
| `CO_{01..03}` | Float | ppm | A |
| `{Any}_Pre_Alarm` | Bool | — | C |
| `{Any}_Alarm` | Bool | — | C |
| `{Any}_Fault` | Bool | — | C |

### §16.3  E-Stop

Under `Safety/ESD/`:

| Tag | Type |
|-----|------|
| `ESTOP_{01..04}_Pressed` | Bool |
| `ESTOP_Active` | Bool |
| `ESD_Reset_Required` | Bool |

---

## §17  CALCULATED / DERIVED TAGS

Under `Calc/`, computed by the site orchestrator at 1/min:

### §17.1  System Performance

| Tag | Formula | Unit |
|-----|---------|------|
| `Total_IT_Load` | Σ rack power R1..R13 | kW |
| `Total_Facility_Load` | Total IT + CDU + Munters + Aux | kW |
| `PUE` | Total_Facility_Load / Total_IT_Load | — |
| `Genset_Total_Power` | Genset_A.Load_kW + Genset_B.Load_kW | kW |
| `Gas_Consumption_Daily` | Σ of 24h Fuel_Rate | Nm³ |
| `Electrical_Efficiency` | Genset_Total_Power / (Fuel_Rate × LHV) | % |
| `Thermal_Efficiency` | (HR_Total + Chiller_Heat_Input) / (Fuel_Rate × LHV) | % |
| `CHP_Efficiency` | Electrical + Thermal | % |
| `COP_System` | Cassette_Cooling / Genset_Total | — |

### §17.2  Economic

| Tag | Formula | Unit |
|-----|---------|------|
| `GPU_Hours_Dispatched_Today` | From workload scheduler | hr |
| `Revenue_Today` | GPU_Hours × rate | USD |
| `Gas_Cost_Today` | Consumption × gas_price | USD |
| `Net_Margin_Today` | Revenue − Gas − Maintenance_Accrual | USD |

### §17.3  Environmental / ESG

| Tag | Formula | Unit |
|-----|---------|------|
| `CO2_Emissions_kg_Today` | Gas_Consumption × 2.02 kg/Nm³ CH₄ | kg |
| `CO2_Per_GPU_hour` | CO2_Emissions / GPU_Hours | kg/GPU-hr |
| `Methane_Destruction_Efficiency` | From flare baseline (if deployed on flare gas) | % |
| `LCFS_Credits_Earned` | Baseline offset method | credits |

### §17.4  Forecast / ML

| Tag | Source | Cat |
|-----|--------|-----|
| `Workload_Forecast_60s_kW` | Scheduler integration | A |
| `Workload_Forecast_Confidence` | Scheduler integration | A |
| `PM_Pump_A_Bearing_Score` | TensorRT autoencoder | B |
| `PM_Filter_Days_Remaining` | Linear extrapolation | B |
| `PM_Genset_A_Efficiency_Deviation` | Baseline deviation | B |

---

## §18  GOVERNANCE & VERSION CONTROL

### Source of Truth

The master tag dictionary is the CSV file `cassette-tag-inventory-v1.0.csv` maintained under version control (git repository). This Markdown document describes the framework and representative samples; the CSV is authoritative for exact contents.

CSV columns:

```
tag_path, opc_ua_node_id, data_type, unit, range_low, range_high,
alarm_hh, alarm_h, alarm_l, alarm_ll, deadband, category,
archival_policy, read_role, write_role, audit_write, encrypt,
source_protocol, source_address, description
```

### Change Control

| Change type | Approver | Notice period |
|-------------|----------|----------------|
| Add new tag | Engineer | none (additive) |
| Rename tag | Integrator + Engineer | 30 days (old path deprecated, not deleted) |
| Change data type | Integrator + Engineer + FSM if SIS-related | 60 days |
| Change range | Engineer | none (but notify operators) |
| Change alarm limits | Engineer | 7 days (operators review) |
| Remove tag | Integrator + Engineer | 90 days minimum |

Deprecated tags remain readable for 12 months after deprecation with a `_DEPRECATED` flag. Clients are expected to migrate within that window. Complete removal after 12 months.

### Revision History

Each tag dictionary CSV carries its own version. This MD document is the current descriptive specification. Migrations between major versions documented in a separate `MIGRATIONS.md`.

### Validation

Every commit to the CSV must pass:
- Schema validation (columns, types)
- No duplicate tag_paths
- All referenced source_protocols exist in the infrastructure
- All referenced alarm limits within range_low / range_high
- Roles in {Viewer, Operator, Supervisor, Engineer, Integrator, SIS_Authorized, System}
- Units in the approved list (§4)

Validation runs as a pre-merge CI check.

---

## §19  OPEN ITEMS

| ID | Priority | Description | Owner | Notes |
|----|----------|-------------|-------|-------|
| TG-01 | P-0 | Per-rack alarm limits for NVL72 (Supply_T, Return_T, Flow thresholds) — obtain from NVIDIA vendor specification | ADC ↔ NVIDIA | Affects §10.1 |
| TG-02 | P-0 | Cat J1939 → Modbus TCP tag map for gensets — confirm CHP-specific tags (HR_Jacket_kW, HR_Exhaust_kW) are exposed | ADC ↔ Cat | Affects §13 |
| TG-03 | P-0 | Chiller vendor tag list — varies by manufacturer; freeze after vendor selection | ADC ↔ Yazaki/Thermax | Affects §14 |
| TG-04 | P-1 | Initial commissioning — identify which tags need field-tuning of alarm limits vs ship defaults | ADC ↔ integrator | Affects §7 |
| TG-05 | P-1 | ML model output tags — finalize after §12 (CTRL-001) model selection | ADC engineering | Affects §17.4 |
| TG-06 | P-1 | Calculated tag computation location — orchestrator vs edge vs cloud? Affects real-time availability | ADC engineering | Affects §17 |
| TG-07 | P-1 | Revenue / economic tags — how real-time, who computes, where pricing comes from | ADC ↔ customer | Affects §17.2 |
| TG-08 | P-2 | Offshore-specific tags (heave, roll, pitch, saltwater detection) for marine variant | ADC ↔ DNV | Future revision |
| TG-09 | P-2 | Customer-specific tags — any deployment may need custom tags for customer's existing infrastructure integration | ADC ↔ customer | Deployment-specific |
| TG-10 | P-2 | Site tag aliases — if customer uses their own naming convention, maintain translation layer | ADC ↔ integrator | Scope question |
| TG-11 | P-3 | Automated CSV validation pipeline — CI setup for tag dictionary repository | ADC engineering | Affects §18 |
| TG-12 | P-3 | Tag discovery for clients — OPC UA browse vs static path list distribution | ADC ↔ integrator | Developer experience |

---

## SUMMARY OF KEY DESIGN DECISIONS

| # | Decision | Rationale |
|---|----------|-----------|
| 1 | ISA-95 equipment hierarchy as namespace | Industry-standard, recognized by integrators, aligns OT and IT naming |
| 2 | Machine-readable CSV as source of truth | Enables automated validation, client code generation, diff-tracking across revisions |
| 3 | Vendor-agnostic canonical paths | Allows vendor swaps without client-side rewrites |
| 4 | Strict unit standardization (SI + domain conventions) | Eliminates unit-conversion bugs across systems |
| 5 | Category-based archival retention | Balances storage cost with forensic / regulatory needs |
| 6 | ACL per tag, not per namespace branch | Fine-grained permission; write-audit automatic |
| 7 | Custom OPC UA Object Types | Enables template-based HMI and analytics |
| 8 | Read-only exposure of SIS to BPCS | IEC 61511 compliant; SIS independence preserved |
| 9 | Deprecation window (12 months) for renamed tags | Gives fleet clients time to migrate without breakage |
| 10 | Calculated tags published by orchestrator | Single computation point; consistent across consumers |

---

**Cassette-TAGS-001 — Site Tag Dictionary & OPC UA Namespace · Rev 1.1 · 2026-04-20**
**Scott Tomsu · scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana**
**CONFIDENTIAL**
