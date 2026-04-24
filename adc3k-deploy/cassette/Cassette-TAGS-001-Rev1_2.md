# Cassette-TAGS-001 — Master Instrument and Tag Register — Rev 1.2

**Document ID:** Cassette-TAGS-001
**Revision:** 1.2
**Date:** 2026-04-22
**Classification:** CONFIDENTIAL
**Supersedes:** Rev 1.1 (deleted) — full clean rebuild
**Companion documents:** Cassette-CTRL-001 · Cassette-FIRE-001 · Cassette-ELEC-001 · Cassette-COOL-001 · Cassette-COOL2-001 · Cassette-MODES-001 · Cassette-BOM-001
**Prepared by:** Scott Tomsu · CEO / Chief Engineer · scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana

---

## Revision log

| Rev | Date | Author | Summary |
|---|---|---|---|
| 1.0 | 2026-01-xx | Scott Tomsu | First issue. Partial tag list, inconsistent naming. Superseded. |
| 1.1 | 2026-02-xx | Scott Tomsu | Withdrawn and deleted — mismatched CTRL-001 alarm naming and missing fire panel interface. |
| **1.2** | **2026-04-22** | **Scott Tomsu** | **Full rebuild as single master register. Tag naming convention locked (T1). Type vocabulary locked (T2). Fire panel interface per FIRE-001 §8. CDU skid Modbus tags per CTRL-001 §8 / COOL2-001 §9. MIV tags per COOL-001. Workload-enable per MODES-001. BMS virtual and OPC-UA tags per MODES-001 §10. Alarm setpoint cross-reference to CTRL-001 §6.2. Authority Doc column on every tag.** |

---

## 1. Scope

Cassette-TAGS-001 is the single master register of every instrument and tag on one ADC 3K Cassette. It assigns each tag a canonical ID, type, I/O location, engineering units and range, normal value or state, alarm-setpoint cross-reference, OPC-UA path, scan rate, and the companion document that owns its definition.

**What TAGS-001 owns:**

- The tag naming convention (§2.1) and type vocabulary (§2.2)
- The I/O module layout and card-slot assignment basis (§3)
- The canonical register rows for every physical and virtual tag (§4–§12)
- The consolidated master tag register table (Appendix A)
- The alarm setpoint cross-reference table (§13), pulled from CTRL-001 §6.2
- The open items affecting tag definition (§14)

**What TAGS-001 defers:**

- Alarm logic (level assignment, TTA, deadband, response) — CTRL-001 §6.2
- Mode transition conditions — MODES-001
- Physical wiring diagrams, terminal blocks, conductor sizing — ELEC-001
- Hydraulic and piping detail — COOL-001
- CDU skid internal PLC program — COOL2-001
- Fire panel internal release logic — FIRE-001
- Cybersecurity controls on OPC-UA surfaces — CYBER-001

**Rule of use.** A tag that appears in any companion document must appear in this register. If it does not appear here, the companion document reference is in error and must be reconciled. TAGS-001 is the authority on tag existence and identity; companion docs are the authority on what the tag does.

Any conflict between TAGS-001 values (alarm setpoints in §13, scan rates in §2.3, normal ranges in §4–§12) and the companion document they reference is an error; the companion document wins. TAGS-001 restates values for readability and must be corrected if drift is detected.

---

## 2. Tag naming convention and type definitions

### 2.1 Tag naming convention (T1)

Format:

```
<InstrumentCode>-<Location/Function>-<Sequence>
```

**Instrument codes:**

| Code | Meaning |
|---|---|
| TT | Temperature transmitter |
| FT | Flow transmitter |
| PT | Pressure transmitter |
| LT | Level transmitter / float switch |
| AT | Analytical transmitter (CO2, RH) |
| ZS | Position / limit switch |
| DI | Discrete input (field wired, generic) |
| DO | Discrete output (field wired, generic) |
| AI | Analog input (generic, when the instrument type is encompassed by a parent tag) |
| AO | Analog output (generic) |
| VT | BMS virtual tag — computed, not a physical I/O point |
| OT | OPC-UA-only tag — published by BMS, no backing physical I/O |
| CMD | BMS command register written over Modbus (not a measurement) |
| STS | Status register read over Modbus (not a measurement) |
| SP | Setpoint register (read/write over Modbus) |

**Location codes used on this Cassette:**

| Code | Scope |
|---|---|
| CDU | CDU skid interface (Modbus TCP tags and the PHX-boundary-crossing measurements it hosts) |
| MIV | Manifold Isolation Valve — the two Belimo DN125 isolation valves (S = supply, R = return) |
| FIRE | Fire panel interface (Ansul panel handshake) |
| ELEC | Electrical / power infrastructure (24 VDC UPS, 480 VAC presence, E-stop) |
| INT | Interior environment (air-side T, RH, CO2) |
| SUMP | Sump pit instrumentation |
| TK | TraceTek leak-detection zone (ZA, ZB) |
| WL | Workload enable subsystem |
| MODE | BMS operating mode (OPC-UA surface) |

**Shortened forms and canonical form rule.** Where a companion document uses a shortened form without a location code (for example `FT-102`, `TT-103`, `TT-104`, `PT-101`), the shortened form is the canonical form and TAGS-001 records it as-is. Where a location code is needed to disambiguate between two similar instruments on different subsystems (for example `TT-INT` vs `TT-CDU-103`), the long form is canonical. Both styles are consistent with T1.

**Examples:**

| Example | Meaning |
|---|---|
| TT-103 | CDU secondary supply temperature (short form — unambiguous on this Cassette) |
| ZS-MIV-S-OPEN | Supply MIV open limit switch |
| DO-FIRE-ARM | Fire panel arm/inhibit relay output |
| AT-INT-RH | Interior relative humidity analytical transmitter |
| TK-ZA-WET | TraceTek Zone A wet alarm discrete input |
| OT-MODE-CURRENT | BMS current mode OPC-UA tag |

### 2.2 Type vocabulary (T2)

| Type | Meaning | Physical path |
|---|---|---|
| DI | 24 VDC discrete input, field wired to a DI card on the DIN-rail I/O bus | Sensor → terminal block → DI card input |
| DO | 24 VDC discrete output, field wired to a DO card (sourcing or interposing relay per ELEC-001) | DO card output → terminal block → relay coil or actuator |
| AI | 4–20 mA analog input to an AI card (or 0–10 VDC where noted on the row) | Transmitter two-wire loop → terminal block → AI card |
| AO | 4–20 mA analog output from an AO card | AO card → terminal block → receiving device |
| MB-C | Modbus TCP coil (1-bit, read-write) on CDU skid PLC | BMS Modbus master → CDU skid PLC coil address |
| MB-HR | Modbus TCP holding register (16-bit, read-write) on CDU skid PLC | BMS Modbus master → CDU skid PLC holding-register address |
| MB-IR | Modbus TCP input register (16-bit, read-only) on CDU skid PLC | BMS Modbus master → CDU skid PLC input-register address |
| OT | OPC-UA tag published by BMS; no backing physical I/O | BMS application → OPC-UA server → platform SCADA client |
| VT | BMS virtual tag; computed from other tags, published on OPC-UA | BMS application logic → OPC-UA server |

Modbus tags reference the CDU skid PLC at the IP address configured in `/etc/adc-bms/config.yaml` per CTRL-001 §8. The Modbus unit ID and register addresses populate columns in the Modbus register rows (§5). Where the CDU skid vendor has not yet confirmed a specific register address, TAGS-01 or TAGS-02 (§14) records the placeholder and blocks the gap.

### 2.3 Scan rate vocabulary (T12)

| Class | Tags in class | Scan / publish rate |
|---|---|---|
| Safety-critical DI | FIRE-DI-1, FIRE-DI-2, FIRE-DI-3, DI-ESTOP, DI-POWER-OK, TK-ZA-WET, TK-ZB-WET, LT-SUMP-HIHI, ZS-MIV-S-OPEN, ZS-MIV-S-CLOSED, ZS-MIV-R-OPEN, ZS-MIV-R-CLOSED | ≥ 1 Hz scan (≤ 1 s cycle) |
| Process measurement | FT-102, TT-103, TT-104, PT-101, PT-102, AT-INT-RH, TT-INT | ≥ 1 Hz scan for alarm evaluation; historian 5 s base, 1 s when alarm active |
| Slow / environmental | AT-CO2, LT-SUMP-HI, TK-ZA-FAULT, TK-ZB-FAULT, DI-UPS-OK, DI-TAMPER | 10 s scan |
| BMS virtual / OPC-UA | OT-MODE-CURRENT, OT-MODE-FIRE-EVENT, OT-MODE-HISTORY, VT-WL-THROTTLE-REQ, OT-ALARM-ACTIVE | Publish on change + 10 s heartbeat |

Scan rates are a property of the BMS I/O scanner loop and the Modbus poll cadence. They are independent of the historian downsample strategy (CTRL-001 §11).

---

## 3. I/O module layout

The BMS I/O lives on a DIN-rail bus inside the ECP panel (CTRL-001 §2 and ECP-001 §4). Card assignment is consolidated here so every tag in §4–§12 has a known slot context.

### 3.1 DIN-rail slot assignments

| Slot | Card type | Channels | Primary tags served |
|---|---|---|---|
| S01 | CPU / bus coupler (gateway to Jetson over EtherCAT or Modbus RTU, per CTRL-001 §2.2) | — | Bus master |
| S02 | DI 16-channel, 24 VDC | 16 | FIRE-DI-1, FIRE-DI-2, FIRE-DI-3, DI-POWER-OK, DI-ESTOP, DI-UPS-OK, DI-TAMPER, TK-ZA-WET, TK-ZA-FAULT, TK-ZB-WET, TK-ZB-FAULT, LT-SUMP-HI, LT-SUMP-HIHI, + 3 spare |
| S03 | DI 16-channel, 24 VDC | 16 | ZS-MIV-S-OPEN, ZS-MIV-S-CLOSED, ZS-MIV-R-OPEN, ZS-MIV-R-CLOSED, STS-PUMP-RUN-DI (hardwired fallback from CDU skid if Modbus down), STS-FIRE-DISCHARGED-DI (hardwired fallback from fire panel discharge output) + 10 spare |
| S04 | DO 8-channel, 24 VDC (relay-output) | 8 | DO-FIRE-ARM, DO-FIRE-RELEASE, DO-MIV-S-OPEN, DO-MIV-R-OPEN, DO-WL-ENABLE, DO-HW-SAFE-STATE-LATCH (hardwired fallback to CDU skid safe-state) + 2 spare |
| S05 | AI 8-channel, 4–20 mA / 0–10 VDC selectable | 8 | AT-INT-RH, TT-INT, AT-CO2, PT-CDU-LOCAL (local supply pressure sense if plumbed) + 4 spare |
| S06 | AO 4-channel, 4–20 mA | 4 | Reserved for future CDU setpoint writes via 4–20 mA (alternative path to SP-FLOW Modbus write); 4 spare |
| S07 | Modbus TCP Ethernet port (on CPU) | — | CDU skid PLC Modbus master |
| S08 | OPC-UA Ethernet port (on Jetson via BMS switch VLAN) | — | Platform NOC publish/subscribe |

**I/O count summary.**

| Dimension | Count |
|---|---|
| DI total channels available | 32 |
| DI channels used at Rev 1.2 | 18 (13 on S02 + 5 on S03 + 1 hardwired-fallback pair) |
| DI channels spare | 14 — supports TAGS-06 (Munters run-status DI) and future expansion |
| DO total channels available | 8 |
| DO channels used at Rev 1.2 | 6 |
| DO channels spare | 2 |
| AI total channels available | 8 |
| AI channels used at Rev 1.2 | 4 |
| AI channels spare | 4 — supports rack-temp sensor expansion (TAGS-04) |
| AO channels used | 0 — reserved |
| Modbus TCP connections | 1 (CDU skid PLC) |
| OPC-UA server | 1 (BMS-hosted, consumed by platform NOC) |

**Card-slot verification is part of MODES-02 / CTRL-001 §14 commissioning.** Exact card part numbers are in BOM-001 §12.

### 3.2 Hardwired-fallback inputs

The BMS retains two hardwired DI fallbacks that are read in parallel with their Modbus or network counterparts:

- **STS-PUMP-RUN-DI** — a hardwired dry contact from the CDU skid's pump-running aux contact, in case the Modbus link is down and the BMS still needs to know whether pumps are physically turning. Not listed in the main tag register as a separate row; described here for S03 slot context. Covered by TAGS-03 if it is promoted to a first-class tag.
- **STS-FIRE-DISCHARGED-DI** — optional, future (FIRE-001 FIRE-07). Reserved DI channel on S03 for a future second fire-panel DI that would separate "confirmed alarm" (FIRE-DI-1) from "actual discharge." Not used in Rev 1.2.

These are infrastructure considerations rather than first-class tags; the S03 slot reservation is recorded here so the slot count does not drift.

---

## 4. Fire panel interface tags

Per T3 and FIRE-001 §8. Authority on purpose, wiring, and behavior is FIRE-001; TAGS-001 records the register row.

### 4.1 FIRE-DI-1 — fire panel confirmed alarm

| Field | Value |
|---|---|
| Tag ID | FIRE-DI-1 |
| Description | Fire panel confirmed alarm contact. Asserts at CONFIRMED ALARM state (cross-zone satisfied or manual release activated) — the start of the Ansul panel's 30 s pre-discharge countdown. |
| Type | DI |
| I/O Card Slot | S02 |
| Modbus Reg | — |
| OPC-UA Path | adc.cassette.<serial>.fire.fire_di_1 |
| Engineering Units | — (Boolean) |
| Range | 0 / 1 |
| Normal Value / State | CLOSED (loop current flowing, logical 0 = no alarm). Cable cut or panel power failure opens loop — BMS sees asserted — fail-safe toward alarm. |
| Alarm Setpoints (ref) | FIRE-TRIGGERED CRITICAL — TTA 0 s — CTRL-001 §6.2 |
| Scan Rate | ≥ 1 Hz (safety-critical) |
| Authority Doc | FIRE-001 §8.2 |

### 4.2 FIRE-DI-2 — fire panel arm / inhibit feedback

| Field | Value |
|---|---|
| Tag ID | FIRE-DI-2 |
| Description | Fire panel system-armed feedback contact. Reflects panel INHIBIT vs ARMED state. Used by BMS for round-trip verification of DO-FIRE-ARM (within 1 s of commanded change). |
| Type | DI |
| I/O Card Slot | S02 |
| Modbus Reg | — |
| OPC-UA Path | adc.cassette.<serial>.fire.fire_di_2 |
| Engineering Units | — (Boolean) |
| Range | 0 / 1 |
| Normal Value / State | CLOSED (panel armed, loop current flowing, BMS sees logical 0). Open = panel inhibited. |
| Alarm Setpoints (ref) | If INHIBITED state persists > 24 h outside a scheduled maintenance window — WARN (STANDBY-MAINT-TIMEOUT-W per CTRL-001 §6.2) |
| Scan Rate | ≥ 1 Hz (safety-critical) |
| Authority Doc | FIRE-001 §8.3 |

### 4.3 FIRE-DI-3 — fire panel fault / trouble

| Field | Value |
|---|---|
| Tag ID | FIRE-DI-3 |
| Description | Fire panel trouble / supervisory fault contact. Open on any panel fault: detector trouble, cylinder low pressure, battery low, AC loss beyond battery threshold, communication fault, ground fault. |
| Type | DI |
| I/O Card Slot | S02 |
| Modbus Reg | — |
| OPC-UA Path | adc.cassette.<serial>.fire.fire_di_3 |
| Engineering Units | — (Boolean) |
| Range | 0 / 1 |
| Normal Value / State | CLOSED (no fault). Loop cut also fails to open — fail-safe toward ALARM notification. |
| Alarm Setpoints (ref) | FIRE-FAULT ALARM — TTA 0 s — CTRL-001 §6.2 |
| Scan Rate | ≥ 1 Hz (safety-critical) |
| Authority Doc | FIRE-001 §8.4 |

### 4.4 DO-FIRE-ARM — fire panel maintenance-inhibit relay

| Field | Value |
|---|---|
| Tag ID | DO-FIRE-ARM |
| Description | BMS output to the fire panel remote-inhibit terminal pair. De-energized = inhibit removed, panel armed and ready to discharge. Energized = inhibit active, panel will not discharge. De-energized at BMS boot and on every SAFE-STATE entry regardless of prior state. Power loss to BMS — de-energized (panel armed by default) — fail-safe toward arming. |
| Type | DO |
| I/O Card Slot | S04 |
| Modbus Reg | — |
| OPC-UA Path | adc.cassette.<serial>.fire.do_fire_arm |
| Engineering Units | — (Boolean) |
| Range | 0 / 1 |
| Normal Value / State | DE-ENERGIZED (panel armed) in INIT, STANDBY-IDLE, READY, PRODUCTION, DEGRADED, SAFE-STATE, E-STOP. ENERGIZED only in STANDBY-MAINT-GENERAL and STANDBY-MAINT-COOLANT. |
| Alarm Setpoints (ref) | Commanded change not acknowledged by FIRE-DI-2 within 10 s — MIV-MISMATCH-style WARN (FIRE-ARM-MISMATCH-W per CTRL-001 §6.2) |
| Scan Rate | Command on change; feedback round-trip verified within 1 s |
| Authority Doc | FIRE-001 §8.5 |

### 4.5 DO-FIRE-RELEASE — remote fire suppression release

| Field | Value |
|---|---|
| Tag ID | DO-FIRE-RELEASE |
| Description | BMS momentary release command to the fire panel's remote-manual-release input pair. De-energized = release not requested (normal). Momentarily energized (≥ 500 ms pulse) = release requested. The BMS may assert only when all four FIRE-001 §8.6 gates are simultaneously satisfied: (1) FIRE-DI-1 asserted > 60 s, (2) FIRE-DI-3 NOT asserted, (3) authenticated NOC OPC-UA `fire-remote-release-request` command received, (4) DO-FIRE-ARM de-energized. |
| Type | DO |
| I/O Card Slot | S04 |
| Modbus Reg | — |
| OPC-UA Path | adc.cassette.<serial>.fire.do_fire_release |
| Engineering Units | — (Boolean) |
| Range | 0 / 1 |
| Normal Value / State | DE-ENERGIZED always, until all four gates met. |
| Alarm Setpoints (ref) | Every assertion logged at CRITICAL to alarms.jsonl per FIRE-001 §8.6; no self-triggered alarm on de-energized state |
| Scan Rate | Command on gate-satisfaction + operator request; pulse duration ≥ 500 ms |
| Authority Doc | FIRE-001 §8.6 |

---

## 5. CDU skid Modbus interface tags

Per T4 and CTRL-001 §8 / COOL2-001 §9. The BMS is Modbus master; the CDU skid PLC is slave. IP address and unit ID are placeholders in this register — the concrete address lives in `/etc/adc-bms/config.yaml` per CTRL-001 §8 and is confirmed at commissioning.

**Modbus unit ID:** 1 (CDU skid PLC default; confirm at commissioning — **TAGS-01**)
**Poll cadence:** 1 s for all read tags; write-on-change for commands and setpoints (CTRL-001 §4.1).
**Heartbeat:** bidirectional pair at Modbus HR 30020 (skid → BMS) and HR 40005 (BMS → skid) per CTRL-001 §8.4. Not listed as standalone tag rows; they are infrastructure on the Modbus link, exercised by the Modbus master worker in `adc-bms`.

### 5.1 CMD-PUMP-ENABLE — CDU pump run command

| Field | Value |
|---|---|
| Tag ID | CMD-PUMP-ENABLE |
| Description | Primary pump run/stop command from BMS to CDU skid. 0 = pumps commanded OFF, 1 = pumps commanded ON. |
| Type | MB-C |
| I/O Card Slot | S07 (Modbus TCP) |
| Modbus Reg | Coil 40002 (per CTRL-001 §8.3 register map) |
| OPC-UA Path | adc.cassette.<serial>.cdu.cmd_pump_enable |
| Engineering Units | — (Boolean) |
| Range | 0 / 1 |
| Normal Value / State | 1 in READY, PRODUCTION, DEGRADED; 0 in all other modes |
| Alarm Setpoints (ref) | No self-triggered alarm; mismatch with STS-PUMP-RUN detected by CDU-COMMS / PUMP-STATE logic per CTRL-001 §6.2 |
| Scan Rate | Write on change |
| Authority Doc | CTRL-001 §8.3 · COOL2-001 §9 |

### 5.2 STS-PUMP-RUN — CDU pump running feedback

| Field | Value |
|---|---|
| Tag ID | STS-PUMP-RUN |
| Description | CDU skid PLC report of pump-running status. 1 = at least one primary pump running; 0 = all pumps stopped. |
| Type | MB-IR (or MB-C per CDU skid PLC map — TAGS-01 confirms) |
| I/O Card Slot | S07 |
| Modbus Reg | IR 30012 (per CTRL-001 §8.2 — PUMP-1-STATE, enum 0/1/2) |
| OPC-UA Path | adc.cassette.<serial>.cdu.sts_pump_run |
| Engineering Units | enum (0 = off, 1 = on, 2 = fault) |
| Range | 0 / 1 / 2 |
| Normal Value / State | 1 when CMD-PUMP-ENABLE = 1 and skid healthy; 0 when pumps commanded off |
| Alarm Setpoints (ref) | CDU-PUMP-ALL-OFF CRITICAL at 10 s when workload-enable active and all pump states = 0 — CTRL-001 §6.2 |
| Scan Rate | 1 s (Modbus poll) |
| Authority Doc | CTRL-001 §8.2 · COOL2-001 §9 |

### 5.3 STS-PUMP-FAULT — CDU pump fault status

| Field | Value |
|---|---|
| Tag ID | STS-PUMP-FAULT |
| Description | CDU skid PLC report of pump fault. 1 = any pump reports fault; 0 = no fault. Derived from the pump-state enum (state = 2) or from the SKID-ALARM-WORD-1 bitfield per CTRL-001 §8.2. |
| Type | MB-IR |
| I/O Card Slot | S07 |
| Modbus Reg | IR 30018 (SKID-ALARM-WORD-1 bitfield per CTRL-001 §8.2) |
| OPC-UA Path | adc.cassette.<serial>.cdu.sts_pump_fault |
| Engineering Units | — (Boolean) |
| Range | 0 / 1 |
| Normal Value / State | 0 |
| Alarm Setpoints (ref) | CDU-PUMP-FAULT ALARM — TTA 0 s — CTRL-001 §6.2 |
| Scan Rate | 1 s |
| Authority Doc | CTRL-001 §8.2 · COOL2-001 §9 |

### 5.4 FT-102 — CDU secondary flow

| Field | Value |
|---|---|
| Tag ID | FT-102 |
| Description | CDU secondary-circuit flow rate (flow into Cassette, through coolant loop, back to CDU). |
| Type | MB-IR (32-bit across 30010–30011 per CTRL-001 §8.2) |
| I/O Card Slot | S07 |
| Modbus Reg | IR 30010–30011 |
| OPC-UA Path | adc.cassette.<serial>.cdu.ft_102 |
| Engineering Units | L/min |
| Range | 0–2,500 L/min |
| Normal Value / State | 1,600–2,000 L/min (design flow ~1,810 LPM per COOL-001 Rev 1.2) |
| Alarm Setpoints (ref) | FLOW-LO-A ALARM at < 80 % of commissioned setpoint — TTA 30 s — CTRL-001 §6.2; FLOW-LO-C CRITICAL at < 50 % of commissioned setpoint — CTRL-001 §6.2 |
| Scan Rate | 1 Hz (process measurement) |
| Authority Doc | CTRL-001 §8.2 · COOL-001 · COOL2-001 §9 |

### 5.5 TT-103 — CDU secondary supply temperature

| Field | Value |
|---|---|
| Tag ID | TT-103 |
| Description | CDU secondary-circuit supply temperature (coolant flowing into the Cassette from the CDU skid). |
| Type | MB-IR (INT16 ×0.1 scaling per CTRL-001 §8.2) |
| I/O Card Slot | S07 |
| Modbus Reg | IR 30003 |
| OPC-UA Path | adc.cassette.<serial>.cdu.tt_103 |
| Engineering Units | °C |
| Range | 18–45 °C operational; transmitter range 0–80 °C |
| Normal Value / State | 30–42 °C at design load (per COOL-001 / COOL2-001) |
| Alarm Setpoints (ref) | SUPPLY-T-HI-W WARN at > 45 °C — TTA 60 s; SUPPLY-T-HI-A ALARM at > 48 °C — TTA 180 s; SUPPLY-T-HI-C CRITICAL at > 60 °C — TTA 0 s — CTRL-001 §6.2 |
| Scan Rate | 1 Hz |
| Authority Doc | CTRL-001 §8.2 · COOL2-001 §9 |

### 5.6 TT-104 — CDU secondary return temperature

| Field | Value |
|---|---|
| Tag ID | TT-104 |
| Description | CDU secondary-circuit return temperature (coolant flowing out of the Cassette back to the CDU skid). |
| Type | MB-IR (INT16 ×0.1) |
| I/O Card Slot | S07 |
| Modbus Reg | IR 30004 |
| OPC-UA Path | adc.cassette.<serial>.cdu.tt_104 |
| Engineering Units | °C |
| Range | 40–62 °C operational; transmitter range 0–80 °C |
| Normal Value / State | 45–55 °C at design load |
| Alarm Setpoints (ref) | RETURN-T-HI-W WARN at > 55 °C — TTA 60 s; RETURN-T-HI-A ALARM at > 58 °C — TTA 180 s; RETURN-T-HI-C CRITICAL at > 62 °C — TTA 0 s — CTRL-001 §6.2 |
| Scan Rate | 1 Hz |
| Authority Doc | CTRL-001 §8.2 · COOL2-001 §9 |

### 5.7 PT-101 — CDU secondary supply pressure

| Field | Value |
|---|---|
| Tag ID | PT-101 |
| Description | CDU secondary-circuit supply pressure. Note: CTRL-001 §8.2 uses PT-101 for primary-loop P and PT-102 for secondary-supply P; TAGS-001 uses the shorter PT-101 / PT-102 naming without the primary/secondary disambiguation because in the Cassette boundary the secondary supply is the pressure the Cassette cares about. The alarm table in CTRL-001 §6.2 refers to LOOP-P-* with PT-102 as the source register. This row reflects the Cassette-side pressure; the register address is per CTRL-001 §8.2. |
| Type | MB-IR (UINT16 ×0.01) |
| I/O Card Slot | S07 |
| Modbus Reg | IR 30006 (PT-102 in CTRL-001 §8.2 = secondary supply P) |
| OPC-UA Path | adc.cassette.<serial>.cdu.pt_101 |
| Engineering Units | bar(g) |
| Range | 0–8 bar operational; transmitter 0–10 bar |
| Normal Value / State | 3.0–5.5 bar |
| Alarm Setpoints (ref) | LOOP-P-LO-W WARN at < 3.0 bar — TTA 30 s; LOOP-P-LO-A ALARM at < 2.5 bar — TTA 30 s; LOOP-P-LO-C CRITICAL at < 1.5 bar — TTA 0 s; LOOP-P-HI-W WARN at > 5.5 bar; LOOP-P-HI-A ALARM at > 6.0 bar; LOOP-P-HI-C CRITICAL at > 6.5 bar — CTRL-001 §6.2 |
| Scan Rate | 1 Hz |
| Authority Doc | CTRL-001 §8.2 · COOL2-001 §9 |

### 5.8 PT-102 — CDU secondary return pressure

| Field | Value |
|---|---|
| Tag ID | PT-102 |
| Description | CDU secondary-circuit return pressure. Used with PT-101 to compute loop Δp as a diagnostic for HX fouling or coolant distribution health. Rev 1.2 status: the CDU skid PLC register map at Rev 0.x does **not** expose a discrete return pressure register — PT-102 availability is pending CDU skid vendor confirmation (TAGS-02). Until confirmed, PT-102 is populated from the CDU skid's HX-DP register (IR 30015 per CTRL-001 §8.2) as a computed Δp, not an absolute return pressure. |
| Type | MB-IR (UINT16 ×0.01 when Δp; ×0.01 bar(g) when absolute) |
| I/O Card Slot | S07 |
| Modbus Reg | IR 30015 (HX-DP at Rev 1.2; pending discrete return-P register at TAGS-02) |
| OPC-UA Path | adc.cassette.<serial>.cdu.pt_102 |
| Engineering Units | bar(g) (absolute) or bar (Δp) depending on source register |
| Range | Δp: 0–3 bar; absolute: 0–8 bar |
| Normal Value / State | Δp: 0.5–1.5 bar at design flow; absolute return: 2.5–4.5 bar |
| Alarm Setpoints (ref) | HX-dP-HI WARN at > baseline + 25 % — CTRL-001 §6.2 |
| Scan Rate | 1 Hz |
| Authority Doc | CTRL-001 §8.2 · COOL2-001 §9 |

### 5.9 SP-FLOW — CDU secondary flow setpoint write

| Field | Value |
|---|---|
| Tag ID | SP-FLOW |
| Description | CDU secondary flow setpoint write. Allows BMS to request VFD speed change on CDU skid pumps in response to DEGRADED workload-throttle-request (CTRL-001 §9.2 / MODES-001 §7). Active write is **OPEN** at Rev 1.2 — SP-FLOW is registered and the Modbus holding-register address is reserved, but the BMS Modbus master does not write to it until TAGS-03 closes (confirms CDU skid PLC accepts external flow setpoint writes). Read access for supply-setpoint verification uses IR 30017 per CTRL-001 §8.2. |
| Type | MB-HR |
| I/O Card Slot | S07 |
| Modbus Reg | HR 40001 (CMD-SUPPLY-SETPOINT in CTRL-001 §8.3 — currently used for temperature setpoint write, not flow). Reserved HR for flow: see TAGS-03. |
| OPC-UA Path | adc.cassette.<serial>.cdu.sp_flow |
| Engineering Units | L/min |
| Range | 800–2,500 L/min |
| Normal Value / State | Commissioned setpoint (nominally 1,810 L/min) |
| Alarm Setpoints (ref) | Out-of-range write attempt rejected by BMS with log entry per CTRL-001 §8.5; no self-triggered alarm |
| Scan Rate | Write on change (disabled at Rev 1.2 pending TAGS-03) |
| Authority Doc | CTRL-001 §8.3 · COOL2-001 §9 |

**Additional CDU skid Modbus tags** — for completeness of the register, the BMS also consumes the following from CTRL-001 §8.2 but they are not promoted to first-class TAGS-001 rows with the same detail because their use is internal to the Modbus worker and historian (they feed other tags' alarm logic rather than standing as primary indicators):

- TT-101 (primary supply T, IR 30001), TT-102 (primary return T, IR 30002), PT-103 (secondary return P, IR 30007 — present in CTRL-001 §8.2 map; if populated, supersedes the PT-102 placeholder above — TAGS-02), FT-101 (primary flow, IR 30008–09), PUMP-2-STATE (IR 30013), PUMP-3-STATE (IR 30014), SKID-STATE (IR 30016), SKID-SETPOINT-ACTUAL (IR 30017), SKID-ALARM-WORD-2 (IR 30019), CMD-SAFE-STATE (HR 40003).

These are exposed over OPC-UA at `adc.cassette.<serial>.cdu.<register_name_lowercased>` on the same 1 s cadence. They are governed by CTRL-001 §8.

---

## 6. Manifold isolation valve tags

Per T5 and COOL-001 §8. Belimo DN125 spring-return fail-closed actuators; 24 VDC DO energized = drive open; DO de-energized = spring-return to closed. Limit switches confirm position.

### 6.1 DO-MIV-S-OPEN — supply MIV open command

| Field | Value |
|---|---|
| Tag ID | DO-MIV-S-OPEN |
| Description | BMS command to drive supply MIV to open position. De-energized = valve springs closed. Energized = valve drives open. |
| Type | DO |
| I/O Card Slot | S04 |
| Modbus Reg | — |
| OPC-UA Path | adc.cassette.<serial>.miv.do_miv_s_open |
| Engineering Units | — (Boolean) |
| Range | 0 / 1 |
| Normal Value / State | ENERGIZED in READY, PRODUCTION, DEGRADED; DE-ENERGIZED in INIT, STANDBY, SAFE-STATE, E-STOP |
| Alarm Setpoints (ref) | If ENERGIZED and ZS-MIV-S-OPEN not asserted within 15 s — VALVE-TRAVEL-FAULT WARN (MIV-S-MISMATCH-W per CTRL-001 §6.2); MIV-DUAL-FAIL CRITICAL if both MIVs commanded and neither reach limits within 30 s |
| Scan Rate | Command on change; feedback evaluated continuously |
| Authority Doc | COOL-001 §8 · CTRL-001 §7 |

### 6.2 DO-MIV-R-OPEN — return MIV open command

| Field | Value |
|---|---|
| Tag ID | DO-MIV-R-OPEN |
| Description | BMS command to drive return MIV to open position. Same logic as DO-MIV-S-OPEN. |
| Type | DO |
| I/O Card Slot | S04 |
| Modbus Reg | — |
| OPC-UA Path | adc.cassette.<serial>.miv.do_miv_r_open |
| Engineering Units | — (Boolean) |
| Range | 0 / 1 |
| Normal Value / State | ENERGIZED in READY, PRODUCTION, DEGRADED; DE-ENERGIZED elsewhere |
| Alarm Setpoints (ref) | MIV-R-MISMATCH-W WARN; MIV-DUAL-FAIL CRITICAL — CTRL-001 §6.2 |
| Scan Rate | Command on change |
| Authority Doc | COOL-001 §8 · CTRL-001 §7 |

### 6.3 ZS-MIV-S-OPEN — supply MIV open limit switch

| Field | Value |
|---|---|
| Tag ID | ZS-MIV-S-OPEN |
| Description | Supply MIV open-position limit switch. Asserted (closed circuit) when valve has reached full open. |
| Type | DI |
| I/O Card Slot | S03 |
| Modbus Reg | — |
| OPC-UA Path | adc.cassette.<serial>.miv.zs_miv_s_open |
| Engineering Units | — (Boolean) |
| Range | 0 / 1 |
| Normal Value / State | 1 (closed) when valve is open and MIV is commanded open; 0 otherwise |
| Alarm Setpoints (ref) | Conflict with ZS-MIV-S-CLOSED simultaneously asserted — VALVE-POSITION-CONFLICT CRITICAL (sensor fault) — CTRL-001 §6.2 |
| Scan Rate | ≥ 1 Hz |
| Authority Doc | COOL-001 §8 · CTRL-001 §7 |

### 6.4 ZS-MIV-S-CLOSED — supply MIV closed limit switch

| Field | Value |
|---|---|
| Tag ID | ZS-MIV-S-CLOSED |
| Description | Supply MIV closed-position limit switch. Asserted when valve has reached full closed. |
| Type | DI |
| I/O Card Slot | S03 |
| Modbus Reg | — |
| OPC-UA Path | adc.cassette.<serial>.miv.zs_miv_s_closed |
| Engineering Units | — (Boolean) |
| Range | 0 / 1 |
| Normal Value / State | 1 when valve is closed and commanded closed (INIT, STANDBY, SAFE-STATE, E-STOP) |
| Alarm Setpoints (ref) | VALVE-POSITION-CONFLICT CRITICAL if both open and closed asserted — CTRL-001 §6.2 |
| Scan Rate | ≥ 1 Hz |
| Authority Doc | COOL-001 §8 · CTRL-001 §7 |

### 6.5 ZS-MIV-R-OPEN — return MIV open limit switch

| Field | Value |
|---|---|
| Tag ID | ZS-MIV-R-OPEN |
| Description | Return MIV open-position limit switch. |
| Type | DI |
| I/O Card Slot | S03 |
| Modbus Reg | — |
| OPC-UA Path | adc.cassette.<serial>.miv.zs_miv_r_open |
| Engineering Units | — (Boolean) |
| Range | 0 / 1 |
| Normal Value / State | 1 when return valve open and commanded open |
| Alarm Setpoints (ref) | Conflict with ZS-MIV-R-CLOSED — CRITICAL — CTRL-001 §6.2 |
| Scan Rate | ≥ 1 Hz |
| Authority Doc | COOL-001 §8 · CTRL-001 §7 |

### 6.6 ZS-MIV-R-CLOSED — return MIV closed limit switch

| Field | Value |
|---|---|
| Tag ID | ZS-MIV-R-CLOSED |
| Description | Return MIV closed-position limit switch. |
| Type | DI |
| I/O Card Slot | S03 |
| Modbus Reg | — |
| OPC-UA Path | adc.cassette.<serial>.miv.zs_miv_r_closed |
| Engineering Units | — (Boolean) |
| Range | 0 / 1 |
| Normal Value / State | 1 when return valve closed |
| Alarm Setpoints (ref) | CRITICAL on conflict — CTRL-001 §6.2 |
| Scan Rate | ≥ 1 Hz |
| Authority Doc | COOL-001 §8 · CTRL-001 §7 |

---

## 7. Workload-enable tag

Per T6 and MODES-001 §2.3.

### 7.1 DO-WL-ENABLE

| Field | Value |
|---|---|
| Tag ID | DO-WL-ENABLE |
| Description | Platform workload-enable relay output. De-energized = workload inhibited (platform-side workload-enable relay open). Energized = workload permitted (relay closed). Asserted only after READY → PRODUCTION four-gate transition and authenticated NOC `workload-enable-request`. De-energized on any SAFE-STATE, E-STOP, or `stop-workload`. |
| Type | DO |
| I/O Card Slot | S04 |
| Modbus Reg | — |
| OPC-UA Path | adc.cassette.<serial>.workload.do_wl_enable |
| Engineering Units | — (Boolean) |
| Range | 0 / 1 |
| Normal Value / State | 1 in PRODUCTION and DEGRADED; 0 in all other modes |
| Alarm Setpoints (ref) | No self-triggered alarm; state-change events logged |
| Scan Rate | Command on change |
| Authority Doc | MODES-001 §2.3, §2.4 · CTRL-001 §6.3 |

---

## 8. Power and E-stop tags

Per T7 and ELEC-001.

### 8.1 DI-POWER-OK

| Field | Value |
|---|---|
| Tag ID | DI-POWER-OK |
| Description | 480 V AC main presence confirmation from ELEC-001 aux contact. Asserted = 480 V AC present and within tolerance. |
| Type | DI |
| I/O Card Slot | S02 |
| Modbus Reg | — |
| OPC-UA Path | adc.cassette.<serial>.elec.di_power_ok |
| Engineering Units | — (Boolean) |
| Range | 0 / 1 |
| Normal Value / State | 1 (asserted) |
| Alarm Setpoints (ref) | POWER-LOSS ALARM at 0 for ≥ 3 s; POWER-LOSS-EXT CRITICAL at 0 for ≥ 5 min while workload-enable active — CTRL-001 §6.2 |
| Scan Rate | ≥ 1 Hz (safety-critical) |
| Authority Doc | ELEC-001 §5 · CTRL-001 §6.2 |

### 8.2 DI-ESTOP

| Field | Value |
|---|---|
| Tag ID | DI-ESTOP |
| Description | E-stop pushbutton status. NC dry contact: closed = normal, open = E-stop pressed. E-stop is wired directly to ELEC-001 shunt-trip, independent of BMS; DI is for BMS event logging and mode publication. |
| Type | DI |
| I/O Card Slot | S02 |
| Modbus Reg | — |
| OPC-UA Path | adc.cassette.<serial>.elec.di_estop |
| Engineering Units | — (Boolean) |
| Range | 0 / 1 |
| Normal Value / State | 1 (closed, normal — BMS reads as no-E-stop) |
| Alarm Setpoints (ref) | ESTOP-ACTIVE CRITICAL — TTA 0 s (already in shunt-tripped state; alarm is for log/record) — CTRL-001 §6.2 |
| Scan Rate | ≥ 1 Hz (safety-critical) |
| Authority Doc | ELEC-001 §6 · CTRL-001 §6.2 · MODES-001 §2.7 |

### 8.3 DI-UPS-OK

| Field | Value |
|---|---|
| Tag ID | DI-UPS-OK |
| Description | 24 VDC life-safety UPS healthy status, read from UPS unit aux contact. Asserted = UPS on mains and charged. De-asserted = UPS on battery or in fault. |
| Type | DI |
| I/O Card Slot | S02 |
| Modbus Reg | — |
| OPC-UA Path | adc.cassette.<serial>.elec.di_ups_ok |
| Engineering Units | — (Boolean) |
| Range | 0 / 1 |
| Normal Value / State | 1 (asserted) |
| Alarm Setpoints (ref) | UPS-ON-BATTERY WARN at 0 (if 480 V AC still present); UPS-FAULT ALARM at 0 for > 60 s — CTRL-001 §6.2 |
| Scan Rate | 10 s |
| Authority Doc | ELEC-001 §5 |

### 8.4 DI-TAMPER

| Field | Value |
|---|---|
| Tag ID | DI-TAMPER |
| Description | Enclosure tamper DI — sums ECP panel tamper switch and outer door tamper switch. NC (door/panel closed). Opens when either door is opened. |
| Type | DI |
| I/O Card Slot | S02 |
| Modbus Reg | — |
| OPC-UA Path | adc.cassette.<serial>.elec.di_tamper |
| Engineering Units | — (Boolean) |
| Range | 0 / 1 |
| Normal Value / State | 1 (closed) |
| Alarm Setpoints (ref) | TAMPER-INFO INFO during STANDBY-MAINT-* modes; TAMPER-WARN WARN in any other mode — CTRL-001 §6.2 |
| Scan Rate | 10 s |
| Authority Doc | ELEC-001 · CYBER-001 §9.1 · CTRL-001 §6.2 |

---

## 9. Interior environment tags

Per T8.

### 9.1 AT-INT-RH

| Field | Value |
|---|---|
| Tag ID | AT-INT-RH |
| Description | Interior relative humidity. 4–20 mA analytical transmitter, ceiling-mounted in the ELEC-end of the Cassette interior. |
| Type | AI (4–20 mA) |
| I/O Card Slot | S05 |
| Modbus Reg | — |
| OPC-UA Path | adc.cassette.<serial>.int.at_int_rh |
| Engineering Units | %RH |
| Range | 0–100 %RH (transmitter); 20–55 %RH operational |
| Normal Value / State | 35–50 %RH (Munters-controlled) |
| Alarm Setpoints (ref) | INT-RH-HI-W WARN at > 55 %RH — TTA 300 s; INT-RH-HI-A ALARM at > 60 %RH — TTA 300 s; INT-RH-HI-C CRITICAL at > 75 %RH — TTA 0 s — CTRL-001 §6.2 |
| Scan Rate | 1 Hz |
| Authority Doc | CTRL-001 §6.2 |

### 9.2 TT-INT

| Field | Value |
|---|---|
| Tag ID | TT-INT |
| Description | Interior air temperature. 4–20 mA temperature transmitter, ceiling-mounted mid-Cassette. |
| Type | AI (4–20 mA) |
| I/O Card Slot | S05 |
| Modbus Reg | — |
| OPC-UA Path | adc.cassette.<serial>.int.tt_int |
| Engineering Units | °C |
| Range | 0–60 °C (transmitter); 18–35 °C operational |
| Normal Value / State | 22–30 °C |
| Alarm Setpoints (ref) | INT-T-HI-W WARN at > 30 °C — TTA 300 s; INT-T-HI-A ALARM at > 35 °C — TTA 300 s; INT-T-HI-C CRITICAL at > 45 °C — CTRL-001 §6.2 |
| Scan Rate | 1 Hz |
| Authority Doc | CTRL-001 §6.2 |

### 9.3 AT-CO2

| Field | Value |
|---|---|
| Tag ID | AT-CO2 |
| Description | Interior CO2 concentration. NDIR CO2 sensor, ceiling-mounted. Personnel-safety indicator for enclosed space occupancy; also an indirect combustion / decomposition marker post-fire-discharge. |
| Type | AI (4–20 mA) |
| I/O Card Slot | S05 |
| Modbus Reg | — |
| OPC-UA Path | adc.cassette.<serial>.int.at_co2 |
| Engineering Units | ppm |
| Range | 0–5,000 ppm (transmitter); 400–800 ppm operational |
| Normal Value / State | 450–700 ppm |
| Alarm Setpoints (ref) | CO2-HI-A ALARM at > 1,000 ppm — TTA 30 s (personnel alert, no throttle); CO2-HI-C CRITICAL at > 5,000 ppm — TTA 0 s — CTRL-001 §6.2 |
| Scan Rate | 10 s |
| Authority Doc | CTRL-001 §6.2 · FIRE-001 §11.2 |

---

## 10. Leak detection tags

Per T9. Two TraceTek zones (ZA = compute end, ZB = ELEC/control end), each with a WET and a FAULT DI.

### 10.1 TK-ZA-WET

| Field | Value |
|---|---|
| Tag ID | TK-ZA-WET |
| Description | TraceTek Zone A (compute end, under hot aisle) wet-detect output from TT-SIM-2 controller as dry contact. Asserted = liquid detected on Zone A cable. |
| Type | DI |
| I/O Card Slot | S02 |
| Modbus Reg | — |
| OPC-UA Path | adc.cassette.<serial>.leak.tk_za_wet |
| Engineering Units | — (Boolean) |
| Range | 0 / 1 |
| Normal Value / State | 0 (dry) |
| Alarm Setpoints (ref) | TRACETEK-ZA-WET-A ALARM — TTA 0 s (escalates to CRITICAL if TK-ZB-WET also asserts) — CTRL-001 §6.2 |
| Scan Rate | ≥ 1 Hz (safety-critical) |
| Authority Doc | CTRL-001 §6.2 |

### 10.2 TK-ZA-FAULT

| Field | Value |
|---|---|
| Tag ID | TK-ZA-FAULT |
| Description | TraceTek Zone A cable fault / open-circuit detection from TT-SIM-2 controller. Asserted = cable broken or terminator missing. |
| Type | DI |
| I/O Card Slot | S02 |
| Modbus Reg | — |
| OPC-UA Path | adc.cassette.<serial>.leak.tk_za_fault |
| Engineering Units | — (Boolean) |
| Range | 0 / 1 |
| Normal Value / State | 0 (healthy) |
| Alarm Setpoints (ref) | TRACETEK-ZA-FAULT-W WARN — TTA 60 s — CTRL-001 §6.2 |
| Scan Rate | 10 s |
| Authority Doc | CTRL-001 §6.2 |

### 10.3 TK-ZB-WET

| Field | Value |
|---|---|
| Tag ID | TK-ZB-WET |
| Description | TraceTek Zone B (ELEC and control end) wet-detect output. |
| Type | DI |
| I/O Card Slot | S02 |
| Modbus Reg | — |
| OPC-UA Path | adc.cassette.<serial>.leak.tk_zb_wet |
| Engineering Units | — (Boolean) |
| Range | 0 / 1 |
| Normal Value / State | 0 (dry) |
| Alarm Setpoints (ref) | TRACETEK-ZB-WET-A ALARM — TTA 0 s; TRACETEK-DUAL-WET-C CRITICAL when both TK-ZA-WET and TK-ZB-WET asserted — CTRL-001 §6.2 |
| Scan Rate | ≥ 1 Hz |
| Authority Doc | CTRL-001 §6.2 |

### 10.4 TK-ZB-FAULT

| Field | Value |
|---|---|
| Tag ID | TK-ZB-FAULT |
| Description | TraceTek Zone B cable fault / open-circuit detection. |
| Type | DI |
| I/O Card Slot | S02 |
| Modbus Reg | — |
| OPC-UA Path | adc.cassette.<serial>.leak.tk_zb_fault |
| Engineering Units | — (Boolean) |
| Range | 0 / 1 |
| Normal Value / State | 0 (healthy) |
| Alarm Setpoints (ref) | TRACETEK-ZB-FAULT-W WARN — TTA 60 s — CTRL-001 §6.2 |
| Scan Rate | 10 s |
| Authority Doc | CTRL-001 §6.2 |

---

## 11. Sump level tags

Per T10. Two float switches (hi and hi-hi); low-level is not instrumented because the sump is normally empty — its only role is to catch a leak.

### 11.1 LT-SUMP-HI

| Field | Value |
|---|---|
| Tag ID | LT-SUMP-HI |
| Description | Sump high-level float switch. Asserted when sump level reaches the first float set-point (indicates leak accumulation sufficient to require ALARM response and on-site investigation). |
| Type | DI |
| I/O Card Slot | S02 |
| Modbus Reg | — |
| OPC-UA Path | adc.cassette.<serial>.sump.lt_sump_hi |
| Engineering Units | — (Boolean) |
| Range | 0 / 1 |
| Normal Value / State | 0 (sump empty/low) |
| Alarm Setpoints (ref) | SUMP-HI-A ALARM — TTA 0 s — CTRL-001 §6.2 |
| Scan Rate | 10 s |
| Authority Doc | CTRL-001 §6.2 · COOL-001 |

### 11.2 LT-SUMP-HIHI

| Field | Value |
|---|---|
| Tag ID | LT-SUMP-HIHI |
| Description | Sump high-high-level float switch. Asserted when sump level reaches the second, higher float set-point (indicates leak is exceeding accumulation threshold — CRITICAL response required). |
| Type | DI |
| I/O Card Slot | S02 |
| Modbus Reg | — |
| OPC-UA Path | adc.cassette.<serial>.sump.lt_sump_hihi |
| Engineering Units | — (Boolean) |
| Range | 0 / 1 |
| Normal Value / State | 0 |
| Alarm Setpoints (ref) | SUMP-HIHI-C CRITICAL — TTA 0 s — CTRL-001 §6.2 |
| Scan Rate | ≥ 1 Hz (safety-critical) |
| Authority Doc | CTRL-001 §6.2 · COOL-001 |

---

## 12. BMS virtual and OPC-UA tags

Per T11 and MODES-001 §10. These have no backing physical I/O; they are computed or synthesized by the BMS application and published on the OPC-UA server.

### 12.1 OT-MODE-CURRENT

| Field | Value |
|---|---|
| Tag ID | OT-MODE-CURRENT |
| Description | BMS current operating mode. Published within 1 s of transition; republished every 10 s as heartbeat. Enum: INIT, INIT-FAULT, STANDBY-IDLE, STANDBY-MAINT-GENERAL, STANDBY-MAINT-COOLANT, STANDBY-FIRE-RECOVERY, READY, PRODUCTION, DEGRADED, SAFE-STATE, E-STOP. |
| Type | OT |
| I/O Card Slot | — |
| Modbus Reg | — |
| OPC-UA Path | adc.cassette.<serial>.mode.current |
| Engineering Units | — (String enum) |
| Range | 11 enum values |
| Normal Value / State | PRODUCTION at steady-state |
| Alarm Setpoints (ref) | No self-triggered alarm; mode transitions logged |
| Scan Rate | Publish on change + 10 s heartbeat |
| Authority Doc | MODES-001 §10.1 |

### 12.2 OT-MODE-FIRE-EVENT

| Field | Value |
|---|---|
| Tag ID | OT-MODE-FIRE-EVENT |
| Description | Sidecar Boolean flag to OT-MODE-CURRENT. True iff current mode is SAFE-STATE or STANDBY-FIRE-RECOVERY AND origin was FIRE-TRIGGERED. Persisted to NVMe at `/var/bms/state/fire_event.flag` so it survives BMS cold boot during fire-recovery. |
| Type | OT |
| I/O Card Slot | — |
| Modbus Reg | — |
| OPC-UA Path | adc.cassette.<serial>.mode.fire_event |
| Engineering Units | — (Boolean) |
| Range | true / false |
| Normal Value / State | false |
| Alarm Setpoints (ref) | No self-triggered alarm |
| Scan Rate | Publish on change + 10 s heartbeat |
| Authority Doc | MODES-001 §8, §10.1 |

### 12.3 OT-MODE-HISTORY

| Field | Value |
|---|---|
| Tag ID | OT-MODE-HISTORY |
| Description | Ring buffer of last 100 mode transitions, each record with timestamp (ISO-8601), from_mode, to_mode, trigger (string). Persisted locally at `/var/bms/state/mode_history.json`. |
| Type | OT |
| I/O Card Slot | — |
| Modbus Reg | — |
| OPC-UA Path | adc.cassette.<serial>.mode.history |
| Engineering Units | — (Structured array) |
| Range | Up to 100 records |
| Normal Value / State | Populated with planned transitions in normal ops |
| Alarm Setpoints (ref) | No self-triggered alarm |
| Scan Rate | Append on transition |
| Authority Doc | MODES-001 §10.2 |

### 12.4 VT-WL-THROTTLE-REQ

| Field | Value |
|---|---|
| Tag ID | VT-WL-THROTTLE-REQ |
| Description | Workload throttle request published during DEGRADED mode. Structure: severity (enum 0/1/2/3), suggested_reduction_fraction (0.0–1.0), triggering_alarms (array of alarm IDs), cassette_serial, timestamp. Cleared on DEGRADED → PRODUCTION exit. |
| Type | VT / OT |
| I/O Card Slot | — |
| Modbus Reg | — |
| OPC-UA Path | adc.cassette.<serial>.workload.throttle_request |
| Engineering Units | — (Structured) |
| Range | severity 0–3; fraction 0.0–1.0 |
| Normal Value / State | severity = 0, fraction = 0.0 (cleared) |
| Alarm Setpoints (ref) | Severity and fraction are set per MODES-001 §7.2 mapping, not per an alarm; the underlying ALARM per CTRL-001 §6.2 is what triggers the publish |
| Scan Rate | Publish on change |
| Authority Doc | MODES-001 §7.2 · CTRL-001 §9.2 |

### 12.5 OT-ALARM-ACTIVE

| Field | Value |
|---|---|
| Tag ID | OT-ALARM-ACTIVE |
| Description | Structured alarm-state array published by BMS alarm engine. Each entry carries alarm ID (from CTRL-001 §6.2), level (INFO/WARN/ALARM/CRITICAL), first_seen timestamp, last_state_change timestamp, tta_elapsed_seconds, acknowledged flag. |
| Type | OT |
| I/O Card Slot | — |
| Modbus Reg | — |
| OPC-UA Path | adc.cassette.<serial>.alarms.active |
| Engineering Units | — (Structured array) |
| Range | Variable; typically 0–20 entries |
| Normal Value / State | Empty array in steady-state PRODUCTION |
| Alarm Setpoints (ref) | No self-triggered alarm; this IS the alarm signal |
| Scan Rate | Publish on change + 10 s heartbeat |
| Authority Doc | CTRL-001 §6.2 · MODES-001 §11 |

---

## 13. Alarm setpoint cross-reference table

**Authority: CTRL-001 §6.2.** Every setpoint, TTA, deadband, and response mapping is cited exactly as CTRL-001 §6.2 defines it. This table is a readability convenience. If any value here drifts from CTRL-001 §6.2, CTRL-001 wins and TAGS-001 must be corrected at the next revision.

| Tag ID | Alarm ID (CTRL-001 §6.2) | Level | Setpoint | TTA | Deadband | Response mapping |
|---|---|:-:|---|:-:|:-:|---|
| TT-103 | SUPPLY-T-HI-W | WARN | > 45 °C | 60 s | 1 °C | Log + SCADA |
| TT-103 | SUPPLY-T-HI-A | ALARM | > 48 °C | 180 s | 1 °C | DEGRADED if PRODUCTION; severity 2 throttle |
| TT-103 | SUPPLY-T-HI-C | CRITICAL | > 60 °C | 0 s | — | SAFE-STATE |
| TT-104 | RETURN-T-HI-W | WARN | > 55 °C | 60 s | 1 °C | Log + SCADA |
| TT-104 | RETURN-T-HI-A | ALARM | > 58 °C | 180 s | 1 °C | DEGRADED; severity 2 |
| TT-104 | RETURN-T-HI-C | CRITICAL | > 62 °C | 0 s | — | SAFE-STATE |
| PT-101 | LOOP-P-LO-W | WARN | < 3.0 bar | 30 s | 0.1 bar | Log + SCADA |
| PT-101 | LOOP-P-LO-A | ALARM | < 2.5 bar | 30 s | 0.1 bar | DEGRADED; severity 2 |
| PT-101 | LOOP-P-LO-C | CRITICAL | < 1.5 bar | 0 s | — | SAFE-STATE |
| PT-101 | LOOP-P-HI-W | WARN | > 5.5 bar | 30 s | 0.1 bar | Log + SCADA |
| PT-101 | LOOP-P-HI-A | ALARM | > 6.0 bar | 30 s | 0.1 bar | DEGRADED; severity 2 |
| PT-101 | LOOP-P-HI-C | CRITICAL | > 6.5 bar | 0 s | — | SAFE-STATE |
| PT-102 | HX-dP-HI | WARN | > baseline + 25 % | 60 s | — | Log + SCADA (fouling indicator) |
| FT-102 | FLOW-LO-A | ALARM | < 80 % of commissioned setpoint | 30 s | — | DEGRADED; severity 2 |
| FT-102 | FLOW-LO-C | CRITICAL | < 50 % of commissioned setpoint | 0 s | — | SAFE-STATE |
| AT-INT-RH | INT-RH-HI-W | WARN | > 55 %RH | 300 s | 2 %RH | Log + SCADA |
| AT-INT-RH | INT-RH-HI-A | ALARM | > 60 %RH | 300 s | 2 %RH | DEGRADED; severity 1 |
| AT-INT-RH | INT-RH-HI-C | CRITICAL | > 75 %RH | 0 s | — | SAFE-STATE |
| TT-INT | INT-T-HI-W | WARN | > 30 °C | 300 s | 1 °C | Log + SCADA |
| TT-INT | INT-T-HI-A | ALARM | > 35 °C | 300 s | 1 °C | DEGRADED; severity 2 |
| TT-INT | INT-T-HI-C | CRITICAL | > 45 °C | 0 s | — | SAFE-STATE |
| AT-CO2 | CO2-HI-A | ALARM | > 1,000 ppm | 30 s | 100 ppm | DEGRADED; severity 1 + personnel alert (no throttle) |
| AT-CO2 | CO2-HI-C | CRITICAL | > 5,000 ppm | 0 s | — | SAFE-STATE (life safety) |
| TK-ZA-WET | TRACETEK-ZA-WET-A | ALARM | asserted | 0 s | — | DEGRADED; severity 2 (proximate to CRITICAL) |
| TK-ZB-WET | TRACETEK-ZB-WET-A | ALARM | asserted | 0 s | — | DEGRADED; severity 2 |
| TK-ZA-WET + TK-ZB-WET | TRACETEK-DUAL-WET-C | CRITICAL | both asserted | 0 s | — | SAFE-STATE |
| TK-ZA-FAULT | TRACETEK-ZA-FAULT-W | WARN | asserted | 60 s | — | Log + SCADA |
| TK-ZB-FAULT | TRACETEK-ZB-FAULT-W | WARN | asserted | 60 s | — | Log + SCADA |
| LT-SUMP-HI | SUMP-HI-A | ALARM | asserted | 0 s | — | DEGRADED; severity 2 |
| LT-SUMP-HIHI | SUMP-HIHI-C | CRITICAL | asserted | 0 s | — | SAFE-STATE |
| ZS-MIV-S-OPEN | MIV-S-MISMATCH-W | WARN | command/feedback disagree > 10 s | 10 s | — | Log + SCADA |
| ZS-MIV-R-OPEN | MIV-R-MISMATCH-W | WARN | command/feedback disagree > 10 s | 10 s | — | Log + SCADA |
| (ZS-MIV-*) | MIV-DUAL-FAIL | CRITICAL | both closed-cmd, neither reach closed in 30 s | 30 s | — | SAFE-STATE + manual dispatch |
| (ZS-MIV-*) | VALVE-POSITION-CONFLICT | CRITICAL | open + closed limits both asserted | 0 s | — | SAFE-STATE (sensor fault) |
| STS-PUMP-FAULT | CDU-PUMP-FAULT | ALARM | asserted | 0 s | — | DEGRADED; severity 2 |
| STS-PUMP-RUN | CDU-PUMP-ALL-OFF | CRITICAL | all pumps off while workload-enable active | 10 s | — | SAFE-STATE |
| (Modbus link) | CDU-COMMS-LOST | ALARM | 3 consecutive poll failures | 3 s | — | DEGRADED; severity 2 |
| FIRE-DI-1 | FIRE-TRIGGERED | CRITICAL | asserted | 0 s | — | SAFE-STATE + fire_event = true |
| FIRE-DI-2 | FIRE-ARM-MISMATCH-W | WARN | DO-FIRE-ARM round-trip > 10 s | 10 s | — | Log + SCADA |
| FIRE-DI-2 | STANDBY-MAINT-TIMEOUT-W | WARN | INHIBITED > 24 h outside maintenance window | — | — | Log + SCADA |
| FIRE-DI-3 | FIRE-FAULT | ALARM | asserted | 0 s | — | DEGRADED; severity 1 (panel trouble; no throttle) |
| DI-POWER-OK | POWER-LOSS | ALARM | 0 | 3 s | — | Log + SCADA; BMS on UPS |
| DI-POWER-OK | POWER-LOSS-EXT | CRITICAL | 0 for ≥ 5 min while workload active | 300 s | — | SAFE-STATE |
| DI-ESTOP | ESTOP-ACTIVE | CRITICAL | asserted (open) | 0 s | — | E-STOP mode (ELEC-001 shunt already tripped) |
| DI-UPS-OK | UPS-ON-BATTERY-W | WARN | 0 while 480 V AC present | 10 s | — | Log + SCADA |
| DI-UPS-OK | UPS-FAULT-A | ALARM | 0 for > 60 s | 60 s | — | SCADA alert |
| DI-TAMPER | TAMPER-INFO | INFO | asserted during STANDBY-MAINT-* | 0 s | — | Log |
| DI-TAMPER | TAMPER-WARN | WARN | asserted in any other mode | 0 s | — | Log + SCADA |
| (watchdog) | WATCHDOG-TRIPPED | CRITICAL | safe-state relay asserted | 0 s | — | SAFE-STATE (already executed by hardware) |
| (BMS app) | JETSON-HB-MISS | WARN | internal heartbeat missed > 2 s | 2 s | — | Log; watchdog trips at 5 s if continued |
| (BMS app) | OPCUA-CLIENT-LOST | WARN | platform SCADA subscription drops | 30 s | — | Log + local HMI banner |

Values that do not appear in CTRL-001 §6.2 at its Rev 1.2 (for example STANDBY-MAINT-TIMEOUT-W) are flagged at TAGS-05 — not for disagreement, but for verification that CTRL-001 §6.2 explicitly carries these rows; if it does not, the CTRL-001 §6.2 table is the one that must be updated, not TAGS-001.

---

## 14. Open items

| ID | Priority | Description | Blocks |
|---|---|---|---|
| TAGS-01 | C1 | Modbus register address confirmation from CDU skid PLC vendor — reconcile every MB-IR / MB-HR / MB-C address in §5 against the final CDU skid PLC program as delivered; confirm unit ID = 1; confirm word order, scaling, and bit positions in SKID-ALARM-WORD-1/2 | CDU skid integration; CTRL-001 §8 lock; commissioning CTRL-001 §10.2 step S-05 |
| TAGS-02 | C1 | Return pressure register availability — confirm whether CDU skid PLC exposes a discrete secondary return P register (per CTRL-001 §8.2 PT-103 at IR 30007). If yes, PT-102 register row is updated from HX-DP fallback to absolute return-P; if no, document PT-102 as a computed Δp only | Loop pressure diagnostics; HX fouling trend; CTRL-001 §6.2 HX-dP-HI alarm source |
| TAGS-03 | C1 | SP-FLOW active write implementation — confirm CDU skid PLC accepts external flow setpoint writes vs supply-temperature-only setpoint writes; assign a discrete HR if flow setpoint is a separate register from temperature setpoint; enable BMS Modbus master to write during DEGRADED throttle response | MODES-001 DEGRADED mode ergonomics; CTRL-001 §9.2 throttle implementation |
| TAGS-04 | C2 | Rack-level sensor tags — if NVIDIA GPU node inlet temperatures and power draw (read over IPMI/Redfish per CTRL-001 §9) are promoted from BMS-internal to first-class TAGS-001 rows, define per-rack tags RACK-R1-INLET-T through RACK-R9-INLET-T and RACK-R1-PWR through RACK-R9-PWR, with AI-card-equivalent virtual tag entries | Platform dashboard granularity; per-rack thermal trend |
| TAGS-05 | C2 | CTRL-001 §6.2 cross-check — verify that every alarm row in §13 exists in CTRL-001 §6.2 table at the same Rev (STANDBY-MAINT-TIMEOUT-W, TAMPER-INFO, TAMPER-WARN, VALVE-POSITION-CONFLICT are candidates that may need to be added to CTRL-001 §6.2 if not already present); reconcile and update whichever doc is behind | Alarm-table completeness; CTRL-001 / TAGS-001 consistency audit |
| TAGS-06 | C2 | Munters run-status DI — if the Munters DSS Pro starter exposes a dry-contact run-status output, add STS-MUNTERS-RUN DI on S03 slot. Current Rev 1.2 posture: BMS infers Munters run state from MODES-001 subsystem-state table; actual run-status feedback is not instrumented because the hardwired fire interlock is the authority (FIRE-001 §9.1) | Observability; post-event reconstruction; MODES-001 STANDBY-FIRE-RECOVERY gate 4 evidence |
| TAGS-07 | C2 | OTA and CYBER-001 tags — add VT / OT tags for certificate expiry warnings (per CYBER-001 §7.3 — auto-renewal trigger at 60 days), OTA pull status, CRL refresh timestamp, and firewall drop-rate counters. Feed platform SIEM rules in CYBER-001 §11.3 | Cybersecurity monitoring; SIEM rule completeness |
| TAGS-08 | C3 | Historian subsample strategy per tag — define which tags are "store-always" vs "store-on-change" vs "store-at-transition" for platform historian; CTRL-001 §11.2 sets the 30-day local ring buffer; the platform historian retention and subsample cadence is a platform-side decision informed by per-tag value here | Platform data governance; storage sizing |

---

## Appendix A — Consolidated master tag register

This is the single table that collects every tag from §4–§12 into one view.

| Tag ID | Description | Type | I/O Card Slot | Modbus Reg | OPC-UA Path | Eng Units | Range | Normal Value/State | Alarm Setpoints (ref) | Scan Rate | Authority Doc |
|---|---|---|---|---|---|---|---|---|---|---|---|
| FIRE-DI-1 | Fire panel confirmed alarm | DI | S02 | — | ...fire.fire_di_1 | — | 0/1 | CLOSED | FIRE-TRIGGERED CRITICAL | ≥1 Hz | FIRE-001 §8.2 |
| FIRE-DI-2 | Fire panel arm/inhibit feedback | DI | S02 | — | ...fire.fire_di_2 | — | 0/1 | CLOSED (armed) | STANDBY-MAINT-TIMEOUT-W | ≥1 Hz | FIRE-001 §8.3 |
| FIRE-DI-3 | Fire panel fault/trouble | DI | S02 | — | ...fire.fire_di_3 | — | 0/1 | CLOSED | FIRE-FAULT ALARM | ≥1 Hz | FIRE-001 §8.4 |
| DO-FIRE-ARM | Fire panel maintenance-inhibit relay | DO | S04 | — | ...fire.do_fire_arm | — | 0/1 | DE-ENERGIZED | FIRE-ARM-MISMATCH-W if round-trip > 10 s | on change | FIRE-001 §8.5 |
| DO-FIRE-RELEASE | Fire panel remote release | DO | S04 | — | ...fire.do_fire_release | — | 0/1 | DE-ENERGIZED | — (logged at CRITICAL on assertion) | on gate satisfaction | FIRE-001 §8.6 |
| CMD-PUMP-ENABLE | CDU pump run command | MB-C | S07 | C 40002 | ...cdu.cmd_pump_enable | — | 0/1 | 1 in READY/PROD/DEG | — | write on change | CTRL-001 §8.3 |
| STS-PUMP-RUN | CDU pump running feedback | MB-IR | S07 | IR 30012 | ...cdu.sts_pump_run | enum | 0/1/2 | 1 at steady-state | CDU-PUMP-ALL-OFF CRITICAL | 1 s | CTRL-001 §8.2 |
| STS-PUMP-FAULT | CDU pump fault | MB-IR | S07 | IR 30018 | ...cdu.sts_pump_fault | — | 0/1 | 0 | CDU-PUMP-FAULT ALARM | 1 s | CTRL-001 §8.2 |
| FT-102 | CDU secondary flow | MB-IR | S07 | IR 30010-11 | ...cdu.ft_102 | L/min | 0-2500 | 1,600-2,000 | FLOW-LO-A ALARM; FLOW-LO-C CRITICAL | 1 Hz | CTRL-001 §8.2 |
| TT-103 | CDU secondary supply T | MB-IR | S07 | IR 30003 | ...cdu.tt_103 | °C | 0-80 | 30-42 | SUPPLY-T-HI-W/A/C | 1 Hz | CTRL-001 §8.2 |
| TT-104 | CDU secondary return T | MB-IR | S07 | IR 30004 | ...cdu.tt_104 | °C | 0-80 | 45-55 | RETURN-T-HI-W/A/C | 1 Hz | CTRL-001 §8.2 |
| PT-101 | CDU secondary supply P | MB-IR | S07 | IR 30006 | ...cdu.pt_101 | bar(g) | 0-10 | 3.0-5.5 | LOOP-P-LO/HI W/A/C | 1 Hz | CTRL-001 §8.2 |
| PT-102 | CDU secondary return P / HX Δp | MB-IR | S07 | IR 30015 (or 30007 pending TAGS-02) | ...cdu.pt_102 | bar(g) or bar | 0-8 or 0-3 | 2.5-4.5 abs or 0.5-1.5 Δp | HX-dP-HI WARN | 1 Hz | CTRL-001 §8.2 |
| SP-FLOW | CDU flow setpoint (pending TAGS-03) | MB-HR | S07 | HR reserved | ...cdu.sp_flow | L/min | 800-2,500 | commissioned SP | — | write on change (disabled) | CTRL-001 §8.3 |
| DO-MIV-S-OPEN | Supply MIV open command | DO | S04 | — | ...miv.do_miv_s_open | — | 0/1 | ENERGIZED in READY/PROD/DEG | MIV-S-MISMATCH-W; MIV-DUAL-FAIL C | on change | COOL-001 §8 |
| DO-MIV-R-OPEN | Return MIV open command | DO | S04 | — | ...miv.do_miv_r_open | — | 0/1 | ENERGIZED in READY/PROD/DEG | MIV-R-MISMATCH-W; MIV-DUAL-FAIL C | on change | COOL-001 §8 |
| ZS-MIV-S-OPEN | Supply MIV open limit | DI | S03 | — | ...miv.zs_miv_s_open | — | 0/1 | 1 when open | VALVE-POSITION-CONFLICT C | ≥1 Hz | COOL-001 §8 |
| ZS-MIV-S-CLOSED | Supply MIV closed limit | DI | S03 | — | ...miv.zs_miv_s_closed | — | 0/1 | 1 when closed | VALVE-POSITION-CONFLICT C | ≥1 Hz | COOL-001 §8 |
| ZS-MIV-R-OPEN | Return MIV open limit | DI | S03 | — | ...miv.zs_miv_r_open | — | 0/1 | 1 when open | VALVE-POSITION-CONFLICT C | ≥1 Hz | COOL-001 §8 |
| ZS-MIV-R-CLOSED | Return MIV closed limit | DI | S03 | — | ...miv.zs_miv_r_closed | — | 0/1 | 1 when closed | VALVE-POSITION-CONFLICT C | ≥1 Hz | COOL-001 §8 |
| DO-WL-ENABLE | Workload-enable relay | DO | S04 | — | ...workload.do_wl_enable | — | 0/1 | 1 in PROD/DEG | — | on change | MODES-001 §2 |
| DI-POWER-OK | 480 V AC presence | DI | S02 | — | ...elec.di_power_ok | — | 0/1 | 1 | POWER-LOSS A; POWER-LOSS-EXT C | ≥1 Hz | ELEC-001 §5 |
| DI-ESTOP | E-stop pushbutton | DI | S02 | — | ...elec.di_estop | — | 0/1 | 1 (normal) | ESTOP-ACTIVE CRITICAL | ≥1 Hz | ELEC-001 §6 |
| DI-UPS-OK | UPS healthy | DI | S02 | — | ...elec.di_ups_ok | — | 0/1 | 1 | UPS-ON-BATTERY-W; UPS-FAULT-A | 10 s | ELEC-001 §5 |
| DI-TAMPER | Enclosure tamper | DI | S02 | — | ...elec.di_tamper | — | 0/1 | 1 (closed) | TAMPER-INFO / TAMPER-WARN | 10 s | ELEC-001 · CYBER-001 §9.1 |
| AT-INT-RH | Interior RH | AI | S05 | — | ...int.at_int_rh | %RH | 0-100 | 35-50 | INT-RH-HI-W/A/C | 1 Hz | CTRL-001 §6.2 |
| TT-INT | Interior T | AI | S05 | — | ...int.tt_int | °C | 0-60 | 22-30 | INT-T-HI-W/A/C | 1 Hz | CTRL-001 §6.2 |
| AT-CO2 | Interior CO2 | AI | S05 | — | ...int.at_co2 | ppm | 0-5,000 | 450-700 | CO2-HI-A; CO2-HI-C | 10 s | CTRL-001 §6.2 · FIRE-001 §11 |
| TK-ZA-WET | TraceTek Zone A wet | DI | S02 | — | ...leak.tk_za_wet | — | 0/1 | 0 | TRACETEK-ZA-WET-A; DUAL-WET-C | ≥1 Hz | CTRL-001 §6.2 |
| TK-ZA-FAULT | TraceTek Zone A fault | DI | S02 | — | ...leak.tk_za_fault | — | 0/1 | 0 | TRACETEK-ZA-FAULT-W | 10 s | CTRL-001 §6.2 |
| TK-ZB-WET | TraceTek Zone B wet | DI | S02 | — | ...leak.tk_zb_wet | — | 0/1 | 0 | TRACETEK-ZB-WET-A; DUAL-WET-C | ≥1 Hz | CTRL-001 §6.2 |
| TK-ZB-FAULT | TraceTek Zone B fault | DI | S02 | — | ...leak.tk_zb_fault | — | 0/1 | 0 | TRACETEK-ZB-FAULT-W | 10 s | CTRL-001 §6.2 |
| LT-SUMP-HI | Sump high level | DI | S02 | — | ...sump.lt_sump_hi | — | 0/1 | 0 | SUMP-HI-A | 10 s | CTRL-001 §6.2 |
| LT-SUMP-HIHI | Sump high-high | DI | S02 | — | ...sump.lt_sump_hihi | — | 0/1 | 0 | SUMP-HIHI-C | ≥1 Hz | CTRL-001 §6.2 |
| OT-MODE-CURRENT | BMS current mode | OT | — | — | ...mode.current | enum | 11 values | PRODUCTION | — | on change + 10 s | MODES-001 §10.1 |
| OT-MODE-FIRE-EVENT | Fire-event flag | OT | — | — | ...mode.fire_event | Boolean | 0/1 | false | — | on change + 10 s | MODES-001 §8 |
| OT-MODE-HISTORY | Mode transition ring buffer | OT | — | — | ...mode.history | array | 100 max | populated | — | on transition | MODES-001 §10.2 |
| VT-WL-THROTTLE-REQ | Workload throttle request | VT/OT | — | — | ...workload.throttle_request | struct | — | severity=0 | — | on change | MODES-001 §7.2 |
| OT-ALARM-ACTIVE | Active alarm array | OT | — | — | ...alarms.active | array | 0-20 | empty | — | on change + 10 s | CTRL-001 §6.2 |

OPC-UA path prefix `adc.cassette.<serial>.` is abbreviated as `...` in the Appendix A view for column width; the register rows in §4–§12 show the full path.

---

## Document control

**Cassette-TAGS-001 — Rev 1.2 — CONFIDENTIAL**
**Prepared by:** Scott Tomsu · CEO / Chief Engineer · scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana
**Companion to:** Cassette-CTRL-001 · Cassette-FIRE-001 · Cassette-ELEC-001 · Cassette-COOL-001 · Cassette-COOL2-001 · Cassette-MODES-001 · Cassette-BOM-001
**Supersedes:** Cassette-TAGS-001 Rev 1.1 (deleted)
**Authority scope:** the single master register of every instrument and tag on one Cassette — naming convention, type vocabulary, I/O slot assignment, Modbus register addresses, OPC-UA paths, engineering units and ranges, normal values, alarm-setpoint cross-reference (CTRL-001 §6.2 is authoritative on the values themselves), scan rates, and the Authority Doc column naming the governing companion document for each tag.

A tag that appears in any companion document must appear in this register. A conflict between values here and the companion document cited in the Authority Doc column is an error; the companion document wins and TAGS-001 is updated at the next revision.

**End of Cassette-TAGS-001 Rev 1.2.**
