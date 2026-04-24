# Cassette-CTRL-001 — Cassette BMS & Controls Specification — Rev 1.2

**Document ID:** Cassette-CTRL-001
**Revision:** 1.2
**Date:** 2026-04-22
**Classification:** CONFIDENTIAL
**Supersedes:** Rev 1.1 (2026-03-xx) — superseded in full
**Companion documents:** Cassette-INT-001 · Cassette-ECP-001 · Cassette-BOM-001 · Cassette-COOL-001 · Cassette-COOL2-001 · Cassette-ELEC-001
**Prepared by:** Scott Tomsu · CEO / Chief Engineer · scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana

---

## Revision log

| Rev | Date | Author | Summary |
|---|---|---|---|
| 1.0 | 2026-02-xx | Scott Tomsu | First issue. Jetson AGX Orin as BMS controller; preliminary I/O and alarm table. |
| 1.1 | 2026-03-xx | Scott Tomsu | Added OPC-UA tag tree outline; Modbus map to CDU skid placeholder. Superseded. |
| **1.2** | **2026-04-22** | **Scott Tomsu** | **Full rebuild against COOL-001 Rev 1.1 and COOL2-001 Rev 1.0. MIV command set finalized (MIV-S, MIV-R Belimo DN125 fail-closed). CDU skid Modbus register map locked as companion to COOL2-001 §9. TraceTek 4-zone mapping locked per BOM-001 §8.1. Alarm hierarchy finalized to four levels (INFO / WARN / ALARM / CRITICAL) with safe-state definition separated from ELEC-001 E-stop. Watchdog architecture locked — independent of Jetson, 5 s heartbeat timeout drives E-stop relay. Open items renumbered CL-xx to avoid collision with COOL-001 C-xx and COOL2-001 CX-xx.** |

---

## 1. Scope

This document specifies the Cassette BMS — the embedded control intelligence inside a single Cassette that monitors and commands all internal subsystems, interfaces with the external CDU skid PLC, interfaces with the platform SCADA / NOC, and executes safe-state and emergency responses.

**One BMS per Cassette.** The BMS is one NVIDIA Jetson AGX Orin 64 GB (BOM-001 §12.1) mounted in the ECP panel (ECP-001 §4), paired with an independent hardware watchdog (BOM-001 §12.2) and fed from the 24 VDC life-safety UPS bus per ELEC-001 §5.

**In scope:**

- Controller hardware, electrical, and enclosure
- Full I/O architecture — analog input (AI), digital input (DI), analog output (AO), digital output (DO)
- Communications to CDU skid (Modbus TCP), NOC / SCADA (OPC-UA), NVIDIA racks (IPMI/Redfish), networking gear (SNMP)
- Software architecture, configuration, logging, and OTA update strategy
- Alarm hierarchy, safe-state logic, and MIV closure logic
- CDU skid Modbus register map
- Compute-rack telemetry interface
- Factory and site commissioning steps for the BMS
- Open items

**Out of scope:**

- Mechanical cooling loop design (COOL-001)
- CDU skid mechanical, electrical, and PLC programming (COOL2-001)
- Novec 1230 fire suppression agent delivery logic (FIRE-001) — the BMS only sources the arm/release dry contact and receives the fire-triggered DI
- 480 V AC power distribution, shunt trip circuit, and ELEC ECP panel build (ELEC-001)
- NVIDIA workload dispatch and tenant scheduling (platform NOC scope)
- Cybersecurity hardening posture (CYBER-001, pending)

---

## 2. Controller hardware & electrical

### 2.1 Primary controller — NVIDIA Jetson AGX Orin 64 GB

| Parameter | Value | Source |
|---|---|---|
| Module | NVIDIA Jetson AGX Orin 64 GB | BOM-001 §12.1 |
| Developer kit carrier | NVIDIA P3737 reference carrier (Jetson AGX Orin DevKit) | BOM-001 §12.1 |
| CPU | 12-core Arm Cortex-A78AE @ 2.2 GHz | — |
| GPU | 2,048-core NVIDIA Ampere + 64 Tensor Cores | — |
| RAM | 64 GB LPDDR5 | — |
| Storage | 1 TB NVMe (primary) + 256 GB eMMC (boot / recovery) | BOM-001 §12.1 |
| Operating system | Ubuntu 22.04 LTS base, JetPack 6.x | — |
| Hardening posture | per CYBER-001 (pending — CL-07) | — |
| Input power | 9–20 VDC, 60 W typical, 90 W peak | NVIDIA datasheet |
| Network | 1 × 10 GbE (management), 1 × 1 GbE (service), 1 × CAN (watchdog link) | — |
| Rated ambient | 0–50 °C operating | — |
| Location | ECP panel, upper Din-rail bay | ECP-001 §4 |

The Jetson runs the BMS application (§5), the OPC-UA server (§4), the Modbus TCP client (§4, §8), and the I/O scanner (§3). It is the single point of command inside the Cassette.

### 2.2 Watchdog — independent hardware

| Parameter | Value | Source |
|---|---|---|
| Watchdog device | Din-rail hardware watchdog / safety relay | BOM-001 §12.2 |
| Heartbeat source | Jetson GPIO heartbeat pulse, 1 Hz expected | — |
| Timeout | **5 s** — no pulse received → watchdog asserts safe-state relay | — |
| Output | Normally-energized dry contact to safe-state relay coil (see §7.2) | — |
| Power | 24 VDC life-safety bus, separately fused from Jetson feed | ELEC-001 §5 |
| Behavior on own power loss | Opens safe-state relay (fail-safe) | — |

The watchdog is electrically and logically independent of the Jetson. If the Jetson crashes, hangs, loses OS, or is pulled from its socket, the watchdog opens the safe-state relay within 5 s, closing MIV-S / MIV-R and de-energizing the workload enable relay. The Jetson cannot inhibit the watchdog from software.

### 2.3 UPS — 24 VDC life-safety bus

| Parameter | Value | Source |
|---|---|---|
| UPS bus voltage | 24 VDC | ELEC-001 §5 |
| BMS hold-up time | ≥ 30 min after main 480 V AC loss | ELEC-001 §5 |
| Loads on UPS feed | Jetson, watchdog, MIV-S actuator, MIV-R actuator, sump floats, TraceTek controller, interior T/RH sensors, CO₂ sensor, fire-panel interface, BMS network switch, ECP panel lighting | §2.5 |
| UPS technology | per ELEC-001 — LiFePO₄ or equivalent, sized for total life-safety load | ELEC-001 §5 |

The UPS exists so the BMS can execute a controlled safe-state and publish final alarm records to the NOC after main AC is lost, and so MIV actuators have power to drive to their fail-closed position under command (MIVs are spring-return fail-closed — loss of UPS also closes them passively, but a commanded close while UPS is live is cleaner and logged).

### 2.4 Panel mounting — ECP panel

Controller, watchdog, 24 VDC power supply, terminal blocks, fuses, and I/O modules mount in the ECP panel per ECP-001 §4. Panel door contains the local HMI touchscreen (§5.3) and E-stop mushroom pushbutton (wired into ELEC-001 shunt trip — not a BMS input; BMS reads E-stop state via DI for logging only).

### 2.5 24 VDC distribution inside the ECP panel

Single 24 VDC bus fed from the UPS, distributed through individually fused terminal blocks:

```
UPS 24 VDC feed
  │
  ├── F1  Jetson AGX Orin (60 W typ / 90 W peak)
  ├── F2  Hardware watchdog (5 W)
  ├── F3  MIV-S actuator (Belimo DN125, 15 W drive, 5 W hold)
  ├── F4  MIV-R actuator (Belimo DN125, 15 W drive, 5 W hold)
  ├── F5  TraceTek TT-SIM-2 controller (10 W)
  ├── F6  Sump float input loop (2 W)
  ├── F7  Interior T/RH sensors — SHT45 × 2 (< 1 W)
  ├── F8  Interior CO₂ sensor (3 W)
  ├── F9  Munters DSS Pro interlock / status interface (2 W)
  ├── F10 Fire panel interface loop (2 W)
  ├── F11 BMS network switch (managed, 10 GbE uplink) (15 W)
  └── F12 ECP HMI touchscreen (12 W)
```

Total steady-state UPS draw: ~130 W. Peak (both MIVs driving): ~160 W. UPS sized per ELEC-001 §5 for ≥ 30 min hold-up at peak draw plus margin for the external TraceTek controller and miscellaneous interior sensors.

---

## 3. I/O architecture

### 3.1 Overview

The BMS I/O is split between (a) signals wired directly into the ECP panel I/O modules, and (b) signals that arrive over Modbus TCP from the CDU skid PLC (§8). Nothing on the CDU skid is wired directly to the BMS — that boundary is cleanly at the Modbus TCP interface.

```
                  ┌──────────────────────────────┐
                  │         Jetson AGX Orin      │
                  │                              │
                  │   BMS application (§5)       │
                  │   OPC-UA server → NOC        │
                  │   Modbus TCP client → CDU    │
                  │   I/O scanner → local panel  │
                  └──┬──────────────┬────────────┘
                     │              │
              10 GbE mgmt         CAN / GPIO heartbeat
                     │              │
     ┌───────────────┴──┐      ┌────┴────────┐
     │  BMS network     │      │  Watchdog   │── safe-state relay
     │  switch (mgmt)   │      │  (HW)       │
     └──┬──────────┬────┘      └─────────────┘
        │          │
        │          └── OPC-UA → Platform NOC / SCADA (§4.2)
        │          └── Modbus TCP → CDU skid PLC (§4.1, §8)
        │          └── IPMI/Redfish → NVIDIA BMCs (§4.3, §9)
        │          └── SNMP → QM9700 IB + mgmt switch (§4.4)
        │
        └── I/O module chain (DIN rail in ECP panel)
              ├── AI module(s) — T/RH, pressure, CO₂, RH, sump level analog
              ├── DI module(s) — valve position, ISV × 20, floats, fire-panel, E-stop
              ├── AO module(s) — (not used in Rev 1.2 — see §3.5)
              └── DO module(s) — MIV command (2), workload enable, fire arm, Munters run
```

### 3.2 Sensors owned by the Cassette BMS

Signals wired directly to the ECP panel (not routed via CDU skid PLC):

| Tag | Description | Sensor | Signal type | Location | Source |
|---|---|---|---|---|---|
| LT-S-01 | TraceTek Zone 1 — trench | TT-500 cable + TT-SIM-2 | DI wet/dry + analog resistance | Trench drip pan under supply/return headers | BOM-001 §8.1 |
| LT-S-02 | TraceTek Zone 2 — sump | TT-500 cable + TT-SIM-2 | DI wet/dry + analog resistance | Sump pit interior | BOM-001 §8.1 |
| LT-S-03 | TraceTek Zone 3 — ELEC end | TT-500 cable + TT-SIM-2 | DI wet/dry + analog resistance | ELEC ECP panel base | BOM-001 §8.1 |
| LT-S-04 | TraceTek Zone 4 — CDU end | TT-500 cable + TT-SIM-2 | DI wet/dry + analog resistance | Cassette-side CDU end (QBH-150 face, floor level) | BOM-001 §8.1 |
| LSL-01 | Sump low-level (normal operating) | Float switch, NO dry contact | DI | Sump pit | COOL-001 §9 |
| LSH-01 | Sump high-level (alarm) | Float switch, NO dry contact | DI | Sump pit | COOL-001 §9 |
| LSHH-01 | Sump high-high (critical) | Float switch, NO dry contact | DI | Sump pit | COOL-001 §9 |
| TT-INT-01 | Interior T/RH, rack mid-height, east | SHT45 | I²C via Modbus bridge | East rack row, mid-height | BOM-001 §11.1 |
| TT-INT-02 | Interior T/RH, rack mid-height, west | SHT45 | I²C via Modbus bridge | West rack row, mid-height | BOM-001 §11.1 |
| CO2-INT-01 | Interior CO₂ | NDIR, 0–5,000 ppm | 4–20 mA AI | Center of Cassette interior | BOM-001 §11.2 |
| PT-S-QBH | Supply QD pressure at QBH-150 face | 0–10 bar transmitter | 4–20 mA AI | Supply QBH-150 face | COOL-001 §8 |
| PT-R-QBH | Return QD pressure at QBH-150 face | 0–10 bar transmitter | 4–20 mA AI | Return QBH-150 face | COOL-001 §8 |
| TT-MUN-S | Munters supply air T | Integrated Munters sensor | Modbus RTU | Munters DSS Pro skid | INT-001 §15.2 |
| TT-MUN-R | Munters return air T | Integrated Munters sensor | Modbus RTU | Munters DSS Pro skid | INT-001 §15.2 |
| RH-MUN-OUT | Munters outlet RH | Integrated Munters sensor | Modbus RTU | Munters DSS Pro skid | INT-001 §15.2 |
| ZS-MIV-S-OPEN | MIV-S open limit | Belimo internal switch | DI | MIV-S actuator | COOL-001 §8 |
| ZS-MIV-S-CLOSED | MIV-S closed limit | Belimo internal switch | DI | MIV-S actuator | COOL-001 §8 |
| ZS-MIV-R-OPEN | MIV-R open limit | Belimo internal switch | DI | MIV-R actuator | COOL-001 §8 |
| ZS-MIV-R-CLOSED | MIV-R closed limit | Belimo internal switch | DI | MIV-R actuator | COOL-001 §8 |
| ZS-ISV-S-R1..R10 | Per-rack supply isolation valve position (10 valves) | NO dry contact limit | DI × 10 | Rack supply tees | COOL-001 §7 |
| ZS-ISV-R-R1..R10 | Per-rack return isolation valve position (10 valves) | NO dry contact limit | DI × 10 | Rack return tees | COOL-001 §7 |
| FIRE-DI | Fire panel status (triggered / armed / fault) | Dry contact, NC fail-safe | DI × 3 | Fire panel interface terminal | FIRE-001 |
| ESTOP-DI | E-stop panel button state | NC dry contact | DI | ECP panel door | ELEC-001 §6 |
| POWER-OK | 480 V AC main presence | NO dry contact via ELEC aux | DI | ELEC ECP | ELEC-001 §5 |

Totals — BMS-owned physical I/O:

| Signal type | Count | Notes |
|---|---:|---|
| AI (4–20 mA) | 3 | CO2-INT-01, PT-S-QBH, PT-R-QBH |
| AI (resistance / analog from TT-SIM-2) | 4 | LT-S-01..04 analog resistance channel |
| DI (dry contact) | ~47 | 4 × TraceTek wet, 3 × sump float, 4 × MIV limit, 20 × ISV limit, 3 × fire, 1 × E-stop, 1 × POWER-OK, + spares |
| Modbus RTU (I²C bridge + Munters) | 4 devices | SHT45 ×2, Munters RTU, TT-SIM-2 (if serial) |
| AO | 0 | none required in Rev 1.2 — §3.5 |
| DO | 6 | MIV-S cmd, MIV-R cmd, workload enable, fire arm, fire release, Munters run/stop |

**The above is the Rev 1.2 working count.** Final exact count is a commissioning deliverable and is flagged as **CL-01** (§11) — sized here with +25 % spare on each module to cover the final sensor schedule.

### 3.3 Signals received via CDU skid Modbus TCP (not wired to BMS)

Per COOL2-001 §9, the CDU skid PLC owns the following and publishes them over Modbus TCP. The BMS reads them; they do not consume BMS physical I/O:

| Tag | Description | Notes |
|---|---|---|
| TT-101 | CDU primary supply T | From CDU skid |
| TT-102 | CDU primary return T | From CDU skid |
| TT-103 | CDU secondary supply T (to Cassette) | From CDU skid |
| TT-104 | CDU secondary return T (from Cassette) | From CDU skid |
| PT-101 | CDU primary loop P | From CDU skid |
| PT-102 | CDU secondary supply P | From CDU skid |
| PT-103 | CDU secondary return P | From CDU skid |
| FT-101 | CDU primary flow | From CDU skid |
| FT-102 | CDU secondary flow | From CDU skid |
| Pump run / fault status | Per-pump | From CDU skid |
| HX Δp | Derived | From CDU skid |

See §8 for the full Modbus register map.

### 3.4 Panel wiring approach

- Signal wiring terminated at numbered terminal blocks (TB-xx) in the ECP panel with a terminal schedule generated at As-Built.
- 4–20 mA loops two-wire, loop-powered from the AI module; shielded twisted pair (STP), shield grounded single-point at the panel.
- Dry contacts wired with 24 VDC loop interrogation current ≥ 4 mA for positive detection.
- TraceTek TT-500 cable grounded per Raychem/TE installation manual; TT-SIM-2 controller on BMS network switch via Modbus TCP gateway.
- MIV actuator cables: 2-conductor + shield for command, 3-conductor for feedback limits, all in separate conduit from 480 V AC feeders.
- All I/O cables labeled at both ends with the tag from §3.2.

### 3.5 No AO in Rev 1.2

No 4–20 mA AO is required in Rev 1.2 because:

- MIV command is binary open/close (Belimo DN125 is 2-position, not modulating — COOL-001 §8)
- CDU supply setpoint is sent over Modbus TCP (§8), not as a 4–20 mA signal
- Munters setpoint is sent over Modbus RTU (INT-001 §15)
- Fire panel arm/release is DO (dry contact)

If a future revision adds modulating valves or analog setpoints, an AO module is added on the DIN rail bus with no other architectural change. Flagged as a forward-compatibility note, not a Rev 1.2 open item.

---

## 4. Communications

### 4.1 Modbus TCP — BMS ↔ CDU skid PLC

| Parameter | Value | Source |
|---|---|---|
| Role | BMS is master; CDU skid PLC is slave | COOL2-001 §9 |
| Transport | Modbus TCP over Ethernet, port 502 | — |
| Physical link | 1 GbE, dedicated VLAN on BMS network switch | — |
| Poll rate | 1 s for telemetry; write-on-change for setpoints | — |
| Timeout | 3 missed polls → CDU_COMMS_LOST alarm (§6) | §8.4 |
| Register map | Full map per §8 | — |

### 4.2 OPC-UA — BMS ↔ Platform NOC / SCADA

| Parameter | Value |
|---|---|
| Role | BMS is OPC-UA server; platform SCADA is client |
| Transport | OPC-UA binary over TCP, port 4840 (default) |
| Physical link | 10 GbE, management VLAN |
| Security | OPC-UA message signing + encryption, Basic256Sha256 minimum; user authentication per CYBER-001 (CL-07) |
| Publish rate | 1 s default; subscribable per tag |
| Tag tree | One node per signal, namespace `adc.cassette.<serial>.<subsystem>.<tag>` |
| Commands subscribable from SCADA | Platform-E-stop-request (triggers §7 safe-state); workload-throttle-request (sets DO WORKLOAD-ENABLE) |
| Historian | Platform-side; BMS holds 30-day local ring buffer (§5.4) |

### 4.3 IPMI / Redfish — BMS ↔ NVIDIA rack BMCs

| Parameter | Value |
|---|---|
| Role | BMS is client (read-only) |
| Targets | 10 compute racks in the Cassette (per INT-001) |
| Transport | IPMI 2.0 over LAN (UDP 623) and/or Redfish (HTTPS port 443) |
| Physical link | Out-of-band management VLAN via BMS network switch |
| Poll rate | 5 s for temp / power; on-demand for throttle state |
| Read tags | CPU/GPU temps, ambient intake T, power draw, fan state, throttle state, SEL events |
| Commands | **None — BMS does not command racks.** Workload dispatch authority sits at platform NOC. |

### 4.4 SNMP — BMS ↔ networking gear

| Parameter | Value |
|---|---|
| Role | BMS is SNMP manager (read-only) |
| Targets | NVIDIA QM9700 InfiniBand switches + ECP management switch |
| Transport | SNMPv3 (AuthPriv), UDP 161 |
| Physical link | Out-of-band management VLAN |
| Poll rate | 30 s for port state, link state, temp; trap receiver enabled |
| Commands | None — BMS does not command network switches |

### 4.5 Internal 10 GbE management switch

| Parameter | Value |
|---|---|
| Device | Managed L2/L3 10 GbE switch, ECP-panel-mounted | BOM-001 §12.3 |
| Uplinks | 2 × 10 GbE to platform NOC (active/standby) |
| Downlinks | Jetson mgmt, CDU skid PLC VLAN, NVIDIA BMC VLAN, QM9700 mgmt VLAN, TT-SIM-2 VLAN, HMI, spare × 4 |
| VLAN scheme | See CYBER-001 (CL-07) — working: platform mgmt, CDU, BMC, IB-mgmt, safety, maintenance |
| Power | 24 VDC UPS feed |

### 4.6 Communication matrix (summary)

| Interface | Protocol | BMS role | Peer | Direction |
|---|---|---|---|---|
| CDU skid | Modbus TCP | Master | CDU skid PLC | R/W |
| Platform NOC | OPC-UA | Server | Platform SCADA | R/W (commands in) |
| NVIDIA racks | IPMI / Redfish | Client | Rack BMCs | R only |
| Networking | SNMPv3 | Manager | QM9700 + mgmt sw | R only |
| Fire panel | Hardwired DI/DO | — | FIRE-001 panel | DI in + DO out |
| E-stop | Hardwired DI | — | ELEC-001 panel | DI in only |

---

## 5. Software architecture

### 5.1 Operating system

- Ubuntu 22.04 LTS base, JetPack 6.x (NVIDIA Linux for Tegra)
- Hardened baseline per CYBER-001 (pending — **CL-07**). Working posture: disable unused services, enforce SSH key-only, firewall default-deny with explicit allow per §4 protocols, automatic security patching on maintenance windows only
- Time sync: PTP (IEEE 1588) preferred from platform NOC; NTP fallback
- Filesystem: `/` on eMMC (boot + recovery), `/var/bms` and `/var/log/bms` on NVMe with ext4 + periodic fstrim

### 5.2 BMS application framework

The BMS runs a single long-lived Python 3.11 application (`adc-bms`) supervised by `systemd`. The application loads a YAML configuration file describing the I/O tag schedule, alarm table, Modbus register map, and OPC-UA tag tree, and spawns worker tasks for each subsystem:

| Worker | Function | Source of truth |
|---|---|---|
| `io-scanner` | Polls local I/O modules; publishes to in-process bus | §3.2 |
| `modbus-cdu` | Modbus TCP master to CDU skid; R/W per §8 | §8 |
| `opcua-server` | OPC-UA server; publishes tag tree; accepts platform commands | §4.2 |
| `rack-telemetry` | IPMI / Redfish polling; publishes to in-process bus | §9 |
| `snmp-manager` | SNMP polling and trap receiver | §4.4 |
| `alarm-engine` | Evaluates §6 alarm table against live tag values; sets alarm state; dispatches safe-state on CRITICAL | §6 |
| `miv-controller` | Implements §7 closure trigger matrix and command sequencing | §7 |
| `heartbeat` | 1 Hz pulse to hardware watchdog GPIO | §2.2 |
| `logger` | Structured JSON logs → local ring buffer + platform historian forwarder | §5.4 |
| `hmi-server` | Local touchscreen web UI over loopback | §5.3 |

Each worker runs in its own asyncio task with a supervisor that restarts crashed workers within 1 s and logs a WARN-level event. Loss of the `heartbeat` worker is specifically detected by the hardware watchdog (§2.2) and causes safe-state within 5 s regardless of whether the supervisor restarts it.

### 5.3 Local HMI

Panel-door touchscreen (10" or similar, BOM-001 §12.4) renders a lightweight web UI served by `hmi-server` on loopback:

- Live values: MIV-S / MIV-R state, TraceTek zones, sump floats, interior T/RH, CO₂, CDU supply/return T, loop pressure
- Active alarms list with ack / silence (silence does not clear; CRITICAL cannot be silenced below ALARM level)
- Safe-state manual reset button (requires two-hand confirmation dialog; disabled while any CRITICAL alarm is active)
- Network / comms status to all peers (§4)
- Software version, last OTA timestamp, watchdog heartbeat rate

HMI is view + ack only. It does not allow changing setpoints or forcing outputs — that authority sits with the platform NOC over OPC-UA, with an override path through CYBER-001-defined credentials only.

### 5.4 Logging and local retention

- All events published as structured JSON to `/var/log/bms/bms.jsonl`, rotated daily, 30-day retention on NVMe
- Alarm events additionally published to a separate `/var/log/bms/alarms.jsonl` with indefinite retention until disk watermark, at which point oldest non-CRITICAL events are dropped
- Log forwarder pushes to platform historian over OPC-UA method call (`WriteHistoryEvents`) on 10 s batches; backlog cached locally if forwarder connection drops
- TraceTek zone resistance is logged as a time-series to support trending (§6 notes slow-developing seepage often appears as resistance drift before a full wet trigger)

### 5.5 Configuration management

- BMS configuration is a single YAML bundle (`/etc/adc-bms/config.yaml`) under version control (git) on the platform side; deployed via OTA
- Schema validation on load; refusal to start on invalid config with clear log message
- Includes: tag list, units, engineering-units conversion, alarm thresholds, Modbus register map, OPC-UA namespace, peer addresses, timeout constants
- One canonical config per Cassette serial; overrides per Cassette captured as a minimal diff file

### 5.6 OTA update strategy

- Application updates: pull a signed OCI-formatted container image via the platform OTA channel to `/opt/adc-bms/releases/<version>/`; atomic swap of the `current` symlink; systemd restart. Rollback to previous version on three consecutive crashes within 5 min.
- OS updates: attended only. Scheduled during a planned maintenance window with the Cassette in safe-state; on-site engineer present; dual-copy boot partition with known-good fallback.
- Watchdog firmware: field-upgradable only via attended maintenance; not accessible over the network.
- Signature verification: all update artifacts signed per CYBER-001 (CL-07); refusal to install unsigned or signature-mismatched artifacts.

---

## 6. Alarm hierarchy & safe-state logic

### 6.1 Levels

| Level | Meaning | Response |
|---|---|---|
| INFO | Routine operational event | Log only |
| WARN | Deviation from normal; no automatic action required | Log + SCADA alert; no automatic action |
| ALARM | Condition outside safe operating envelope but not immediately damaging | SCADA alert; on-site response required within 15 min |
| CRITICAL | Immediate risk of equipment damage, loss of coolant containment, or life-safety | Immediate safe-state (§6.3); manual reset required |

Latching: all ALARM and CRITICAL events latch until explicitly acknowledged (ALARM) or reset (CRITICAL). WARN clears when the underlying condition clears past the deadband.

### 6.2 Full alarm table

Deadbands are stated for thresholds that could chatter. Time-to-alarm (TTA) is the duration the condition must persist before the event is raised; this suppresses transient spikes.

| Alarm ID | Level | Trigger | Deadband | TTA | Response |
|---|---|---|---|---|---|
| SUPPLY-T-HI-W | WARN | CDU supply T (TT-103) > 45 °C | 1 °C | 60 s | Log + SCADA |
| SUPPLY-T-HI-A | ALARM | CDU supply T (TT-103) > 48 °C | 1 °C | 180 s | SCADA alert; on-site 15 min |
| SUPPLY-T-HI-C | CRITICAL | CDU supply T (TT-103) > 60 °C | — | 0 s | Safe-state |
| RETURN-T-HI-W | WARN | CDU return T (TT-104) > 55 °C | 1 °C | 60 s | Log + SCADA |
| RETURN-T-HI-A | ALARM | CDU return T (TT-104) > 58 °C | 1 °C | 180 s | SCADA alert |
| LOOP-P-LO-W | WARN | Loop P (PT-102) < 3.0 bar | 0.1 bar | 30 s | Log + SCADA |
| LOOP-P-LO-A | ALARM | Loop P (PT-102) < 2.5 bar | 0.1 bar | 30 s | SCADA alert |
| LOOP-P-LO-C | CRITICAL | Loop P (PT-102) < 1.5 bar | — | 0 s | Safe-state |
| LOOP-P-HI-W | WARN | Loop P (PT-102) > 5.5 bar | 0.1 bar | 30 s | Log + SCADA |
| LOOP-P-HI-A | ALARM | Loop P (PT-102) > 6.0 bar | 0.1 bar | 30 s | SCADA alert |
| QBH-dP-HI | WARN | \|PT-S-QBH − PT-R-QBH\| > baseline + 25 % | — | 60 s | Log + SCADA |
| HX-dP-HI | WARN | CDU HX Δp > baseline + 25 % | — | 60 s | Log + SCADA (fouling indicator) |
| FLOW-LO-A | ALARM | FT-102 < 80 % of setpoint | — | 30 s | SCADA alert |
| INT-RH-HI-W | WARN | Interior RH > 55 % | 2 % | 300 s | Log + SCADA |
| INT-RH-HI-A | ALARM | Interior RH > 60 % | 2 % | 300 s | SCADA alert |
| INT-T-HI-W | WARN | Interior T > 30 °C | 1 °C | 300 s | Log + SCADA |
| INT-T-HI-A | ALARM | Interior T > 35 °C | 1 °C | 300 s | SCADA alert |
| CO2-HI-A | ALARM | CO₂ > 1,000 ppm | 100 ppm | 30 s | SCADA alert; personnel safety |
| CO2-HI-C | CRITICAL | CO₂ > 5,000 ppm | — | 0 s | Safe-state (life safety) |
| TT-Z1-WET | CRITICAL | TraceTek Zone 1 (trench) wet | — | 0 s | Safe-state |
| TT-Z2-WET | CRITICAL | TraceTek Zone 2 (sump) wet | — | 0 s | Safe-state |
| TT-Z3-WET | CRITICAL | TraceTek Zone 3 (ELEC end) wet | — | 0 s | Safe-state |
| TT-Z4-WET | CRITICAL | TraceTek Zone 4 (CDU end) wet | — | 0 s | Safe-state |
| TT-Z-DRIFT | WARN | Any TraceTek zone resistance down > 20 % from 7-day rolling baseline | — | 600 s | Log + SCADA (pre-seepage) |
| SUMP-LO | INFO | LSL-01 low level (normal operating) | — | — | Log |
| SUMP-HI-A | ALARM | LSH-01 high level | — | 60 s | SCADA alert |
| SUMP-HIHI-C | CRITICAL | LSHH-01 high-high level | — | 0 s | Safe-state |
| MIV-S-MISMATCH | WARN | MIV-S command vs. limit switch feedback disagree > 10 s | — | 10 s | Log + SCADA |
| MIV-R-MISMATCH | WARN | MIV-R command vs. limit switch feedback disagree > 10 s | — | 10 s | Log + SCADA |
| MIV-DUAL-FAIL | CRITICAL | Both MIVs commanded closed, neither reaches closed limit in 30 s | — | 30 s | Safe-state + manual dispatch |
| ISV-POS-MISMATCH | WARN | Any per-rack ISV position contradicts commissioned baseline | — | 60 s | Log + SCADA |
| CDU-COMMS-LOST | ALARM | 3 consecutive Modbus poll failures (≥ 3 s without reply) | — | 3 s | SCADA alert; initiate §8.4 timeout behavior |
| CDU-PUMP-FAULT | ALARM | CDU skid reports any pump fault | — | 0 s | SCADA alert |
| CDU-PUMP-ALL-OFF | CRITICAL | All CDU skid pumps off while workload-enable is active | — | 10 s | Safe-state |
| FIRE-TRIGGERED | CRITICAL | Fire panel DI asserts | — | 0 s | Safe-state + workload enable off |
| FIRE-FAULT | ALARM | Fire panel reports fault state | — | 0 s | SCADA alert |
| WATCHDOG-TRIPPED | CRITICAL | Watchdog asserts safe-state relay (detected post-recovery via DI) | — | 0 s | Already in safe-state; manual reset |
| POWER-LOSS | ALARM | 480 V AC main absent (POWER-OK cleared) | — | 3 s | SCADA alert; BMS on UPS |
| POWER-LOSS-EXT | CRITICAL | Main AC loss > 5 min while workload-enable active | — | 300 s | Safe-state |
| ESTOP-ACTIVE | CRITICAL | ESTOP-DI asserted | — | 0 s | Already in safe-state (ELEC shunt-trip path); log |
| RACK-TEMP-HI | WARN | Any rack reports inlet T > INT-001 threshold via IPMI | — | 60 s | Log + SCADA |
| RACK-THROTTLE | INFO | Any rack reports throttle active | — | 0 s | Log; correlate with thermal trend |
| JETSON-HB-MISS | WARN | Jetson heartbeat missed internally > 2 s | — | 2 s | Log; watchdog takes over at 5 s if continued |
| OPCUA-CLIENT-LOST | WARN | Platform SCADA subscription drops | — | 30 s | Log + local HMI banner |

### 6.3 Safe-state — definition

When any CRITICAL alarm fires (or the watchdog asserts, or the platform sends an E-stop-request over OPC-UA), the BMS drives the Cassette to **safe-state**:

1. **Close MIV-S** (supply isolation) — DO de-energized; Belimo spring-return drives to closed
2. **Close MIV-R** (return isolation) — DO de-energized; Belimo spring-return drives to closed
3. **Command CDU skid pumps to stop** via Modbus TCP (write holding register per §8.3). If Modbus is unavailable, the watchdog safe-state relay also drops a hardwired dry contact back to the CDU skid (COOL2-001 §9 — skid PLC uses this as a loss-of-command stop)
4. **De-energize workload-enable DO** — the platform-side 24 VDC workload-enable relay drops; platform is responsible for acting on this (translating loss-of-enable into GPU workload drain), but the BMS does not wait
5. **Munters DSS Pro continues running** — needed for humidity control during cool-down; Munters is a separate interlocked subsystem and the BMS explicitly does **not** stop it on safe-state
6. **Arm fire suppression** if not already armed (DO to FIRE-001 panel); **do not** fire-release — release is only on a genuine fire trigger (FIRE-001 logic)
7. **BMS stays alive on UPS** — continues logging, publishing state, and holding safe-state outputs

Safe-state is **not** the same as E-stop. Safe-state keeps the Cassette electrically energized (480 V AC remains); it stops coolant flow and de-energizes workload. E-stop (from platform over OPC-UA or from the panel E-stop button) additionally triggers the ELEC-001 shunt trip, dropping 480 V AC feed at the upstream breaker. E-stop is a superset of safe-state.

### 6.4 Safe-state reset

- Manual reset only
- Requires all contributing CRITICAL alarms to have cleared at the source (sump dry, TraceTek zones dry, temperatures in band, etc.)
- Requires a physical local HMI two-hand reset or an authenticated platform NOC command (CYBER-001 credential)
- Reset sequence: acknowledge all alarms → verify all tags in normal band for 60 s → operator commands reset → BMS commands MIV open, sends CDU pump enable, re-energizes workload-enable relay, clears safe-state latch
- Re-entering safe-state requires a new trigger; it does not auto-arm on reset

---

## 7. MIV control logic

### 7.1 Normal operation

MIV-S and MIV-R are **normally open** during operation. They are commanded closed only under safe-state (§6.3) or under a maintenance-isolation command from the platform (authenticated OPC-UA call).

Belimo DN125 actuators are spring-return fail-closed (COOL-001 §8):

- DO energized → actuator drives open and holds open while power is present
- DO de-energized → spring returns actuator to closed position

This is a fail-safe design — loss of 24 VDC to the actuator (power fault, cable cut, watchdog trip, Jetson crash beyond the 5 s watchdog window) results in valve closure regardless of BMS state.

### 7.2 Closure trigger matrix

| Trigger | Source | Close MIV-S? | Close MIV-R? | Also… |
|---|---|---|---|---|
| Any CRITICAL alarm per §6.2 | BMS alarm engine | Yes | Yes | Per §6.3 |
| Watchdog timeout (> 5 s no heartbeat) | Hardware watchdog | Yes (DO drops via safe-state relay) | Yes | Workload enable off |
| Platform E-stop-request | Platform NOC via OPC-UA | Yes | Yes | Per §6.3 + ELEC shunt trip by platform |
| Panel E-stop button | Hardwired to ELEC shunt trip | Yes (via AC power loss → UPS → controlled close) | Yes | ELEC-001 removes 480 V AC |
| Fire panel triggered | Hardwired DI | Yes | Yes | Workload enable off; fire-release per FIRE-001 |
| Maintenance isolation command | Authenticated OPC-UA | Yes | Yes | Workload enable off; does not trip fire arm |
| Loss of 24 VDC to actuator (any cause) | Physical | Passive closure | Passive closure | Fail-safe behavior |

### 7.3 Closure sequence timing

On command:

1. **t = 0 s:** DO to MIV-S and MIV-R de-energized simultaneously
2. **t ≤ 10 s:** Actuators reach closed limit; ZS-MIV-S-CLOSED and ZS-MIV-R-CLOSED assert (Belimo DN125 nominal close time)
3. **If either limit not seen by t = 30 s:** MIV-DUAL-FAIL CRITICAL; SCADA alert; manual dispatch required

Note: Belimo DN125 close time is actuator-dependent; spec value ≤ 15 s worst case. The 30 s dual-fail threshold gives comfortable margin.

### 7.4 Reset conditions

MIVs reopen only on:

- Safe-state reset per §6.4, **and**
- Explicit operator command (not automatic after CRITICAL clears)

Reopen sequence: MIV-S DO energized → wait for ZS-MIV-S-OPEN → MIV-R DO energized → wait for ZS-MIV-R-OPEN → command CDU skid pump start over Modbus → verify flow FT-102 > 50 % of setpoint within 60 s → re-energize workload-enable relay.

If any step fails, revert to safe-state and alarm.

---

## 8. CDU skid interface (Modbus TCP)

### 8.1 Addressing and transport

| Parameter | Value |
|---|---|
| BMS IP | Fixed, per platform VLAN scheme |
| CDU skid PLC IP | Fixed, per platform VLAN scheme (COOL2-001 §9) |
| Port | TCP 502 |
| Unit ID | 1 |
| Function codes | 3 (Read Holding), 4 (Read Input), 6 (Write Single Register), 16 (Write Multiple Registers) |
| Word order | Big-endian per Modbus convention; 32-bit values in two consecutive registers, high word first |
| Scaling | See §8.2 column "Scaling" |

### 8.2 Read registers (BMS reads from CDU skid)

| Address | Tag | Description | Units | Scaling | Type | Source |
|---|---|---|---|---|---|---|
| 30001 | TT-101 | CDU primary supply T | °C | ×0.1 | INT16 | COOL2-001 §9 |
| 30002 | TT-102 | CDU primary return T | °C | ×0.1 | INT16 | COOL2-001 §9 |
| 30003 | TT-103 | CDU secondary supply T | °C | ×0.1 | INT16 | COOL2-001 §9 |
| 30004 | TT-104 | CDU secondary return T | °C | ×0.1 | INT16 | COOL2-001 §9 |
| 30005 | PT-101 | CDU primary loop P | bar | ×0.01 | UINT16 | COOL2-001 §9 |
| 30006 | PT-102 | CDU secondary supply P | bar | ×0.01 | UINT16 | COOL2-001 §9 |
| 30007 | PT-103 | CDU secondary return P | bar | ×0.01 | UINT16 | COOL2-001 §9 |
| 30008–09 | FT-101 | CDU primary flow | L/min | ×1 | UINT32 | COOL2-001 §9 |
| 30010–11 | FT-102 | CDU secondary flow | L/min | ×1 | UINT32 | COOL2-001 §9 |
| 30012 | PUMP-1-STATE | Pump 1 run/stop/fault | enum | 0=off, 1=on, 2=fault | UINT16 | COOL2-001 §9 |
| 30013 | PUMP-2-STATE | Pump 2 run/stop/fault | enum | same | UINT16 | COOL2-001 §9 |
| 30014 | PUMP-3-STATE | Pump 3 (N+1) run/stop/fault | enum | same | UINT16 | COOL2-001 §9 |
| 30015 | HX-DP | CDU HX differential pressure | bar | ×0.01 | UINT16 | COOL2-001 §9 |
| 30016 | SKID-STATE | Overall skid state | enum | 0=stopped, 1=running, 2=fault, 3=safe-state | UINT16 | COOL2-001 §9 |
| 30017 | SKID-SETPOINT-ACTUAL | Currently active supply setpoint | °C | ×0.1 | INT16 | COOL2-001 §9 |
| 30018 | SKID-ALARM-WORD-1 | Bitfield — pump fault, flow low, etc. | bits | — | UINT16 | COOL2-001 §9 |
| 30019 | SKID-ALARM-WORD-2 | Bitfield — HX Δp hi, loop P lo/hi, etc. | bits | — | UINT16 | COOL2-001 §9 |
| 30020 | SKID-HB-COUNTER | Skid-side heartbeat counter (increments 1 Hz) | — | — | UINT16 | §8.4 |

### 8.3 Write registers (BMS writes to CDU skid)

| Address | Tag | Description | Units | Scaling | Type | Notes |
|---|---|---|---|---|---|---|
| 40001 | CMD-SUPPLY-SETPOINT | CDU secondary supply setpoint | °C | ×0.1 | INT16 | 30–45 °C allowed range (COOL2-001 §9) |
| 40002 | CMD-PUMP-ENABLE | Pump run command | enum | 0=stop, 1=run | UINT16 | Write on reset / safe-state recovery |
| 40003 | CMD-SAFE-STATE | Safe-state request to skid | enum | 0=normal, 1=safe-state | UINT16 | Write 1 on §6.3 |
| 40004 | CMD-HX-BYPASS | Manual HX bypass (commissioning only) | enum | 0/1 | UINT16 | Locked disabled in normal config |
| 40005 | BMS-HB-COUNTER | BMS-side heartbeat counter (increments 1 Hz) | — | — | UINT16 | §8.4 |

### 8.4 Watchdog / timeout behavior

Both sides exchange heartbeat counters:

- BMS increments register 40005 once per second and writes it to the skid
- CDU skid increments register 30020 once per second; BMS reads it

**If BMS observes 30020 not incrementing for 3 consecutive polls (≥ 3 s):** raise CDU-COMMS-LOST (ALARM). If no recovery within 10 s, **escalate** — the BMS can no longer command the skid, so it drops the hardwired safe-state dry contact to the skid (the skid PLC interprets this as "lost command → stop pumps and go to skid safe-state" per COOL2-001 §9) and the BMS commands MIV closure locally (MIVs are BMS-owned, no skid dependency).

**If CDU skid observes 40005 not incrementing for 3 consecutive polls:** per COOL2-001 §9, the skid goes to its own safe-state (stops pumps, holds last known setpoint), which the BMS then detects via SKID-STATE=3 on the next successful read if/when comms recover, or via FT-102 falling to zero (FLOW-LO-A alarm) if reads also fail.

Both sides fail independently to a safe posture. Neither is dependent on the other staying alive.

### 8.5 Setpoint command rules

- Setpoint writes are debounced: minimum 10 s between setpoint changes
- Setpoint range enforced at BMS before write: 30 °C ≤ setpoint ≤ 45 °C (COOL2-001 §9 envelope); out-of-range writes rejected with log entry
- On reset from safe-state, default setpoint is the last-good value stored in BMS NVMe
- Platform NOC can override default setpoint via authenticated OPC-UA call; change logged to alarms.jsonl as INFO

---

## 9. Compute rack interface

### 9.1 Telemetry polling

The BMS polls each of the 10 compute racks (per INT-001) over the out-of-band management network for read-only telemetry:

| Read | Source | Rate |
|---|---|---|
| CPU die T, GPU die T, HBM T (per node) | IPMI sensors / Redfish `/redfish/v1/Systems/{id}/ProcessorCollection` | 5 s |
| Ambient intake T at rack | IPMI sensor | 5 s |
| Node power draw (W) | IPMI / Redfish PowerControl | 5 s |
| Rack PDU total draw (W) | Delta in-row PDU Modbus read (via ELEC-001) | 5 s |
| Fan tach | IPMI sensors | 30 s |
| Throttle state (on/off) | IPMI / Redfish processor throttle bit | 5 s |
| Recent SEL events | IPMI SEL | 60 s (delta only) |

### 9.2 BMS → platform workload throttle signal

The BMS does not command NVIDIA racks directly. If cooling margins degrade, the BMS publishes a **workload-throttle-request** over OPC-UA to the platform NOC with:

- Severity (0 = none, 1 = soft request to reduce workload, 2 = hard request, 3 = immediate)
- Suggested reduction fraction (0–1)
- Cassette serial
- Triggering alarm IDs

The platform NOC decides how to act (deschedule, migrate, or ignore). On CRITICAL cooling events, the BMS additionally drops the workload-enable DO (§6.3), which the platform is expected to act on as a hard drain signal. The BMS does not wait for the platform to acknowledge before going to safe-state.

### 9.3 Power draw trending

Per-rack and aggregate Cassette power draws are trended into the historian for:

- PUE contribution calculation
- Correlation with interior T/RH and supply/return loop T trends
- Early detection of degraded rack cooling (higher power at same workload → fan speed up → intake T creep)

No automatic action is taken on power trend — this is analytical output for platform operations.

---

## 10. Commissioning — BMS checkout

### 10.1 Factory acceptance (at ECP panel build)

Performed before the ECP panel is shipped to the Cassette integration site.

| Step | Description | Pass criterion |
|---|---|---|
| F-01 | Jetson boot + JetPack version check | JetPack 6.x version confirmed; `adc-bms` service active |
| F-02 | Watchdog GPIO pulse verified at 1 Hz | Scope capture at watchdog input; 5 s kill verified by pausing heartbeat |
| F-03 | 24 VDC distribution — every fused branch measured under load | All branches 23.5–25.0 V within tolerance; no over-fused branch |
| F-04 | Every AI channel injection-tested with calibrator | Reading within ±0.5 % of injected signal over 0–100 % span |
| F-05 | Every DI channel actuated with contact simulator | State transition logged within 1 s |
| F-06 | Every DO channel commanded on/off; relay chatter observed | Relay closes/opens as commanded; feedback via loop current |
| F-07 | MIV command → limit feedback loop test (with actuator on bench) | MIV drives to commanded state within 15 s; limit switches match |
| F-08 | Modbus TCP handshake against CDU skid PLC emulator | All registers in §8.2 / §8.3 read/write successfully |
| F-09 | OPC-UA server reachable from laptop client; tag tree published | All §3 and §8 tags visible; subscriptions work |
| F-10 | Alarm injection — force each §6.2 alarm via config override; verify level, response, latch | Every alarm in §6.2 exercised; safe-state sequence fires on CRITICAL injections |
| F-11 | Loss-of-UPS test — pull main feed, verify BMS holds ≥ 30 min on UPS | Measured hold time ≥ 30 min at peak load |
| F-12 | Watchdog trip test — inject heartbeat loss; confirm safe-state relay opens and MIVs drop | MIVs close within 10 s of relay drop |
| F-13 | Configuration bundle loaded; schema validation passes | `adc-bms --check-config` exits 0 |
| F-14 | Cybersecurity baseline verified per CYBER-001 (when available) | CL-07 dependency |

Factory acceptance test report (FAT report) signed off by Scott Tomsu before ECP ships.

### 10.2 Site integration (at Cassette integration + commissioning)

Performed after the Cassette is on-site and the CDU skid, MIVs, sensors, racks, and platform uplinks are terminated.

| Step | Description | Pass criterion |
|---|---|---|
| S-01 | Physical I/O continuity from each sensor to panel TB — end-to-end | Each tag from §3.2 reads the physical stimulus live |
| S-02 | MIV full-stroke test — command open/close, verify limits and close time | Close ≤ 15 s; open ≤ 15 s; limits match |
| S-03 | TraceTek per-zone wet test — apply moist cloth to each zone in turn | Correct zone fires within 10 s; others remain dry; resistance trend logged |
| S-04 | Sump float hierarchy test — fill sump to each level in turn | LSL-01, LSH-01, LSHH-01 fire in order; SUMP-HIHI-C triggers safe-state |
| S-05 | CDU skid Modbus integration — live read/write against commissioned skid PLC | Telemetry live; setpoint write acknowledged; heartbeat counters increment both ways |
| S-06 | Heartbeat loss test — disconnect BMS from skid LAN for 15 s | CDU-COMMS-LOST alarm fires at 3 s; skid goes to its safe-state; BMS commands MIV close at 10 s |
| S-07 | Platform OPC-UA integration — platform SCADA subscribes to tag tree | All tags visible at platform; platform can issue E-stop-request and it executes safe-state |
| S-08 | Fire panel interface test — assert FIRE-DI | FIRE-TRIGGERED CRITICAL; safe-state; workload enable off |
| S-09 | E-stop panel test — press E-stop | ELEC shunt trip drops 480 V AC; BMS on UPS; safe-state executes; ESTOP-ACTIVE logged |
| S-10 | Full alarm matrix verification — walk every row of §6.2 against real conditions or simulated injection | Every alarm exercised; response correct; latching behavior correct |
| S-11 | Workload throttle signal — publish severity-2 workload-throttle-request; confirm platform receipt | Platform NOC acknowledges receipt; operator log captures request |
| S-12 | Rack telemetry — IPMI poll succeeds against every rack BMC | All 10 racks report temps and power draw |
| S-13 | SNMP poll — QM9700 + mgmt switch reachable | Port state, link state readable |
| S-14 | Safe-state → reset full cycle | Trigger CRITICAL (e.g., simulated TT-Z2-WET), verify safe-state, clear source, perform two-hand reset, confirm return to normal |
| S-15 | Sign-off: 7-day soak at representative IT load with no unexplained alarms | Soak log reviewed and signed |

Site acceptance test report (SAT) signed off by Scott Tomsu and platform NOC lead before the Cassette is placed into production.

---

## 11. Open items

IDs use the **CL-xx** series to avoid collision with COOL-001 **C-xx** and COOL2-001 **CX-xx**.

| ID | Priority | Description | Blocks |
|---|---|---|---|
| CL-01 | C1 | Final I/O count verification — complete sensor schedule for as-built ECP panel, confirm AI/DI/DO module counts and spare capacity | ECP panel build release; factory acceptance F-04/F-05/F-06 detail |
| CL-02 | C1 | Modbus register map formal issue with CDU skid PLC vendor — reconcile §8.2 / §8.3 against final PLC program | CDU skid PLC FAT; COOL2-001 §9 cross-check |
| CL-03 | C1 | Alarm thresholds and deadbands — independent review by a second engineer; confirm against Boyd CDU max T, loop pressure relief setting, and INT-001 interior envelope | Safe-state testing F-10 / S-10 |
| CL-04 | C1 | OPC-UA tag namespace and data model — align with platform SCADA historian schema | Platform NOC integration S-07 |
| CL-05 | C2 | Baseline values for TT-Z-DRIFT (7-day rolling) and QBH-dP-HI — populate after 30-day soak | Normal-operation alarm quality |
| CL-06 | C2 | ECP HMI screen design — wireframes, navigation, operator usability review | HMI server deployment |
| CL-07 | C1 | CYBER-001 — full cybersecurity posture: hardening baseline, certificate management, user auth, OT/IT segmentation, OTA signing chain | Full production deployment; any external distribution of BMS config |
| CL-08 | C2 | OTA update infrastructure — platform-side release channel, signing CA, rollback automation | Attended-only fallback until this closes |
| CL-09 | C2 | Local HMI authentication — card reader / PIN / platform SSO tie-in | HMI operator access control |
| CL-10 | C2 | BMS failure-mode FMEA — independent review covering Jetson crash, watchdog failure, network partition, UPS depletion, actuator fault | Rev 1.3 close |
| CL-11 | C2 | Historian data retention policy — local 30-day default; confirm platform historian retention for audit/forensics | Platform data governance |
| CL-12 | C3 | AO module forward-compatibility — confirm DIN-rail bus module selection supports future AO addition without panel rebuild | Future revision only |
| CL-13 | C3 | Workload-throttle-request severity thresholds — tune against real thermal trend data once the first Cassette is in sustained production | Optimization, not gating |

---

## Document control

**Cassette-CTRL-001 — Rev 1.2 — CONFIDENTIAL**
**Prepared by:** Scott Tomsu · CEO / Chief Engineer · scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana
**Companion to:** Cassette-INT-001 · Cassette-ECP-001 · Cassette-BOM-001 · Cassette-COOL-001 · Cassette-COOL2-001 · Cassette-ELEC-001
**Supersedes:** Cassette-CTRL-001 Rev 1.1 in full

Every interface in this document is cross-referenced to its companion spec. Changes to any interface (MIV command set, CDU Modbus map, fire panel handshake, ELEC-001 24 VDC bus, OPC-UA tag tree) must be reflected in both this document and the companion before release.

**End of Cassette-CTRL-001 Rev 1.2.**
