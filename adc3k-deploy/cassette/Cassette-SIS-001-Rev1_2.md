# Cassette-SIS-001 — Safety Instrumented System Specification — Rev 1.2

**Document ID:** Cassette-SIS-001
**Revision:** 1.2
**Date:** 2026-04-22
**Classification:** CONFIDENTIAL
**Supersedes:** Rev 1.1 (deleted) — tag IDs inconsistent with pre-TAGS-001 register; full rebuild
**Companion documents:** Cassette-CTRL-001 · Cassette-FIRE-001 · Cassette-ELEC-001 · Cassette-COOL-001 · Cassette-MODES-001 · Cassette-TAGS-001 · Cassette-CYBER-001 · Cassette-ECP-001
**Prepared by:** Scott Tomsu · CEO / Chief Engineer · scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana

---

## Revision log

| Rev | Date | Author | Summary |
|---|---|---|---|
| 1.0 | 2026-01-xx | Scott Tomsu | First issue. General SIS posture and draft SIF list. Superseded. |
| 1.1 | 2026-02-xx | Scott Tomsu | Withdrawn and deleted — tag IDs in SIF register inconsistent with the TAGS-001 rebuild that locked the canonical naming convention. Also preceded FIRE-001 §8.6 four-gate remote-release lock and MODES-001 §6 STANDBY sub-state formalization. |
| **1.2** | **2026-04-22** | **Scott Tomsu** | **Full rebuild as the single authoritative SIS specification. All tag IDs reconciled with Cassette-TAGS-001 Rev 1.2; all alarm IDs reconciled with Cassette-CTRL-001 §6.2. 14 SIFs defined (SIF-01 through SIF-14). IEC 61511-1:2016 locked as governing framework. Logic solver identity locked: BMS is the software logic solver for SIF-01 through SIF-13; hardware watchdog is an independent second layer for SIF-14; Ansul panel is the NFPA 72 certified logic solver for fire detection and release. SIL 1 interim for BMS-software SIFs pending LOPA (SIS-01). SIL 2 by architecture for SIF-11 (hardwired E-stop) and SIF-14 (relay-only watchdog). Proof-test intervals and procedure format locked. Bypass rules locked (one at a time, 4 h max, workload must be off). Eight C1–C3 open items registered.** |

---

## 1. Scope

Cassette-SIS-001 is the Safety Instrumented System specification for one ADC 3K Cassette. It defines the set of Safety Instrumented Functions (SIFs) that automatically drive the Cassette to its safe state on a hazardous condition; assigns each SIF a SIL target, a process safety time (PST), a proof-test interval; specifies the initiator tags and final-element tags for each SIF; documents the logic solver architecture and independence; establishes bypass and inhibit rules; identifies common-cause failure scenarios; and specifies proof-test procedures.

**What SIS-001 owns:**

- The SIF register (§4) — the authoritative list of safety instrumented functions for this Cassette
- SIL assignment rationale and interim SIL targets (§4)
- Process safety times for each SIF (§4, per position SIS-05)
- Logic solver identity and independence claims (§5, per position SIS-02)
- Safe-state definition as it relates to SIF demand (§4.x, per position SIS-03)
- Proof-test procedures PT-SIF-01 through PT-SIF-14 (§6)
- Bypass and inhibit rules including OPC-UA method surface (§7, per position SIS-08)
- Common-cause failure register (§8, per position SIS-09)
- Diagnostic coverage and demand-mode classification (§9, §10)
- Commissioning verification of SIS functionality (§11)
- SIS modification control (§13)

**What SIS-001 defers:**

- Alarm logic — which condition raises INFO/WARN/ALARM/CRITICAL, TTA values, deadbands, response text — Cassette-CTRL-001 §6.2. SIS-001 consumes alarm IDs from CTRL-001; it does not redefine them.
- Mode state machine transitions, mode entry/exit conditions, recovery paths — Cassette-MODES-001. SIS-001 cites SAFE-STATE as the safe-state target and consumes the mode definition.
- Canonical tag IDs, engineering units, OPC-UA paths, Modbus register addresses — Cassette-TAGS-001. Every tag in this document exists in TAGS-001; any mismatch is an error in SIS-001 that must be corrected.
- Fire panel internal release logic, the 30-second Ansul countdown, agent delivery, cylinder supervisory — Cassette-FIRE-001. SIS-001 treats the Ansul panel as an independent logic solver and does not duplicate its internal logic.
- 480 V AC distribution, E-stop pushbutton wiring, shunt-trip breaker selection, UPS sizing — Cassette-ELEC-001.
- Cybersecurity controls on the OPC-UA `sis-bypass-request` method (authentication, role gating, logging) — Cassette-CYBER-001.

**Rule of use.** Every SIF that causes automatic entry to MODES-001 SAFE-STATE mode must appear in §4. A CRITICAL alarm in CTRL-001 §6.2 that drives SAFE-STATE must correspond to exactly one SIF row here. SIS-001 and CTRL-001 §6.2 together form a closed set — every CRITICAL alarm maps to a SIF; every SIF trigger is a CTRL-001 §6.2 CRITICAL (or, for SIF-11 and SIF-14, a hardware condition that bypasses the alarm engine).

Rev 1.2 is the **design-basis** document for the SIS. A formal Functional Safety Assessment (FSA) per IEC 61511-1 §5.6 has not been performed. FSA is gated on the C1 open items in §14; Rev 1.3 will be issued after those close.

---

## 2. Standards and regulatory basis

Per position SIS-01.

| Standard | Scope of application in this document |
|---|---|
| **IEC 61511-1:2016** — Functional safety — Safety instrumented systems for the process industry sector | Governing framework. Defines SIF, SIL, PST, proof-test interval, logic-solver independence, safe-state, demand mode, bypass management, FSA procedure. Every §4 SIF specification is written in IEC 61511 terms. Compliance claim: Rev 1.2 establishes the SIS design basis against IEC 61511; Rev 1.2 does **not** claim third-party IEC 61511 certification. An FSA per §5.6 is a Rev 1.3 prerequisite. |
| **IEC 61508** (parts 1–7) | Underlying functional safety standard for electrical / electronic / programmable electronic safety-related systems. Applied as the qualification layer for the logic solvers — the hardware watchdog relay (SIF-14 final element) must carry an IEC 61508 SIL 2 datasheet (SIS-04). The BMS software logic-solver qualification under IEC 61511 §11.5 is SIS-02. |
| **NFPA 72** — National Fire Alarm and Signaling Code | Governs the fire detection and alarm system — the Ansul clean-agent panel, its detectors, notification appliances, and manual stations. SIF-01 (fire detection) is implemented in compliance with NFPA 72; the Ansul panel is the certified NFPA 72 logic solver for the detection and release path. SIS-001 references but does not duplicate NFPA 72 design content — that sits in Cassette-FIRE-001. |
| **NFPA 2001** — Standard on Clean Agent Fire Extinguishing Systems | Governs the Novec 1230 clean-agent system, design concentration, agent quantity, discharge time, enclosure integrity, occupant safety, and proof-testing of the suppression system itself. SIS-001 relies on NFPA 2001 compliance being established in Cassette-FIRE-001; this document's proof-test procedures do not discharge agent. |
| **NEC 70** (NFPA 70, National Electrical Code) | Governs electrical installation of the fire panel, BMS ECP panel, I/O modules, interface loops, and the hardwired E-stop / shunt-trip circuit. SIS-001 assumes NEC-compliant installation per Cassette-ELEC-001. |
| **OSHA 29 CFR 1910.147** — The Control of Hazardous Energy (Lockout/Tagout) | Governs the procedural safety of the proof-test activities in §6. Every proof-test that touches a final element in a way that could release stored energy (coolant loop pressure, 480 V AC) is subject to LOTO. §6 proof-tests are written to be executable in MODES-001 STANDBY-MAINT-GENERAL or STANDBY-MAINT-COOLANT where energy sources are already isolated. LOTO alignment is open item SIS-06. |

These standards are additive. None supersedes IEC 61511 for the SIF definitions in §4. Where NFPA 72/2001 have stricter requirements for fire suppression elements, NFPA governs those elements; where IEC 61511 has stricter requirements for the SIS as a whole (independence, proof-test cadence, FSA), IEC 61511 governs.

---

## 3. Hazard identification summary

This is a qualitative hazard register that drives the §4 SIF list. Initiating-event frequency is a qualitative estimate (low / medium / high) based on engineering judgement and does not claim LOPA rigor. Quantitative confirmation is SIS-01.

| Hazard | Consequence | Initiating event frequency | SIF that addresses it | Companion doc source |
|---|---|:-:|---|---|
| Fire inside the Cassette envelope — electrical fault, Li-ion runaway, insulation ignition | Structural and equipment damage; personnel injury if occupied; downstream tenant outage | Low | SIF-01 | Cassette-FIRE-001 §3.3, Cassette-CTRL-001 §6.2 FIRE-TRIGGERED |
| Loss of coolant flow under workload — pump trip, blockage, pipe failure upstream | GPU thermal runaway, hotspot failure, permanent silicon damage, tenant data loss | Medium | SIF-02, SIF-09 | Cassette-COOL-001, Cassette-CTRL-001 §6.2 FLOW-LO-C, CDU-PUMP-ALL-OFF |
| Supply temperature high-high — CDU skid heat rejection failure | GPU over-temperature damage if sustained | Low | SIF-03 | Cassette-CTRL-001 §6.2 SUPPLY-T-HI-C |
| Return temperature high-high — PHX degradation, downstream boundary condition | Heat not rejected; second-order GPU damage | Low | SIF-04 | Cassette-CTRL-001 §6.2 RETURN-T-HI-C |
| Supply pressure high-high — hydraulic transient, valve mis-operation | PHX overload, pipe fitting failure, leak | Low | SIF-05 | Cassette-CTRL-001 §6.2 LOOP-P-HI-C |
| Supply pressure low-low — pump cavitation, PHX dry-run, loop integrity loss | Pump damage within seconds; GPU starvation | Low | SIF-06 | Cassette-CTRL-001 §6.2 LOOP-P-LO-C |
| Dual-zone coolant leak — two independent TraceTek zones wet | Electrical short on live 480 V AC bus; fluid pooling on energized equipment; escalation to fire | Low | SIF-07 | Cassette-CTRL-001 §6.2 TRACETEK-DUAL-WET-C |
| Sump high-high level — leak exceeding primary containment | Fluid breach of Cassette containment; environmental and electrical hazard | Low | SIF-08 | Cassette-CTRL-001 §6.2 SUMP-HIHI-C |
| All CDU pumps off while workload active — immediate coolant starvation | GPU thermal runaway in seconds | Low | SIF-09 | Cassette-CTRL-001 §6.2 CDU-PUMP-ALL-OFF |
| Extended 480 V AC loss while workload-enable active | UPS depletion risk; uncontrolled workload shutdown; loss of BMS observability | Medium | SIF-10 | Cassette-CTRL-001 §6.2 POWER-LOSS-EXT, Cassette-ELEC-001 §5 |
| Emergency stop demanded by operator (physical button or platform command) | Controlled de-energization of the Cassette | Low | SIF-11 | Cassette-ELEC-001 §6, Cassette-CTRL-001 §6.2 ESTOP-ACTIVE |
| MIV dual-fail — both isolation valves fail to close on command | Inability to isolate the Cassette coolant loop after a leak or contamination event | Very low | SIF-12 | Cassette-CTRL-001 §6.2 MIV-DUAL-FAIL |
| Single-zone coolant leak — one TraceTek zone wet | Early indicator of developing leak; protective, not safety-instrumented | Medium | SIF-13 (protective function; not SIL-rated) | Cassette-CTRL-001 §6.2 TRACETEK-ZA-WET-A, TRACETEK-ZB-WET-A |
| Logic solver failure — Jetson crash, BMS application hang, watchdog-detectable fault | BMS cannot evaluate or respond to SIFs | Low | SIF-14 | Cassette-CTRL-001 §2.2, §6.2 WATCHDOG-TRIPPED |

---

## 4. SIF register and individual SIF specifications

### 4.1 SIF register — summary

Per position SIS-06. Every tag ID in this register matches Cassette-TAGS-001 Rev 1.2 exactly; every alarm ID matches Cassette-CTRL-001 §6.2 exactly.

| SIF ID | Hazard | Initiating tags | Logic solver | Final element tags | Safe state outcome | PST | SIL target | Proof-test interval |
|---|---|---|---|---|---|:-:|:-:|:-:|
| SIF-01 | Fire — thermal damage / personnel injury from suppression delay | FIRE-DI-1 (Ansul panel confirmed alarm DI) | BMS (CTRL-001 §2) + Ansul panel (FIRE-001) as independent peer | DO-WL-ENABLE, CMD-PUMP-ENABLE, DO-MIV-S-OPEN, DO-MIV-R-OPEN, DO-FIRE-ARM | MODES-001 SAFE-STATE with OT-MODE-FIRE-EVENT = true | 30 s | SIL 1 (interim) | 6-month |
| SIF-02 | Coolant flow loss — GPU thermal runaway | FT-102 | BMS | DO-WL-ENABLE, CMD-PUMP-ENABLE, DO-MIV-S-OPEN, DO-MIV-R-OPEN | MODES-001 SAFE-STATE | 60 s | SIL 1 (interim) | 12-month |
| SIF-03 | Supply temperature high-high — GPU over-temperature | TT-103 | BMS | DO-WL-ENABLE, CMD-PUMP-ENABLE, DO-MIV-S-OPEN, DO-MIV-R-OPEN | MODES-001 SAFE-STATE | 60 s | SIL 1 (interim) | 12-month |
| SIF-04 | Return temperature high-high — PHX / GPU downstream over-temperature | TT-104 | BMS | DO-WL-ENABLE, CMD-PUMP-ENABLE, DO-MIV-S-OPEN, DO-MIV-R-OPEN | MODES-001 SAFE-STATE | 60 s | SIL 1 (interim) | 12-month |
| SIF-05 | Supply pressure high-high — PHX overload | PT-101 | BMS | DO-WL-ENABLE, CMD-PUMP-ENABLE, DO-MIV-S-OPEN, DO-MIV-R-OPEN | MODES-001 SAFE-STATE | 15 s | SIL 1 (interim) | 12-month |
| SIF-06 | Supply pressure low-low — pump cavitation, PHX dry-run | PT-101 | BMS | DO-WL-ENABLE, CMD-PUMP-ENABLE, DO-MIV-S-OPEN, DO-MIV-R-OPEN | MODES-001 SAFE-STATE | 10 s | SIL 1 (interim) | 12-month |
| SIF-07 | Dual-zone leak — electrical short, fluid on live bus | TK-ZA-WET AND TK-ZB-WET | BMS | DO-WL-ENABLE, CMD-PUMP-ENABLE, DO-MIV-S-OPEN, DO-MIV-R-OPEN | MODES-001 SAFE-STATE | 300 s | SIL 1 (interim) | 12-month |
| SIF-08 | Sump high-high — active leak beyond containment | LT-SUMP-HIHI | BMS | DO-WL-ENABLE, CMD-PUMP-ENABLE, DO-MIV-S-OPEN, DO-MIV-R-OPEN | MODES-001 SAFE-STATE | 60 s | SIL 1 (interim) | 12-month |
| SIF-09 | CDU pumps all-off while workload active | STS-PUMP-RUN (all pumps = 0) evaluated against DO-WL-ENABLE = 1 | BMS | DO-WL-ENABLE, CMD-PUMP-ENABLE, DO-MIV-S-OPEN, DO-MIV-R-OPEN | MODES-001 SAFE-STATE | 10 s | SIL 1 (interim) | 12-month |
| SIF-10 | Extended power loss — UPS depletion risk | DI-POWER-OK (deasserted for ≥ 300 s while DO-WL-ENABLE = 1) | BMS (on UPS) | DO-WL-ENABLE, CMD-PUMP-ENABLE (Modbus may already be unavailable), DO-MIV-S-OPEN, DO-MIV-R-OPEN | MODES-001 SAFE-STATE | 300 s | SIL 1 (interim) | 12-month |
| SIF-11 | E-stop — emergency manual de-energization | DI-ESTOP (hardwired also to ELEC-001 shunt-trip, independent of BMS software) | ELEC-001 shunt-trip circuit (hardware) | 480 V AC bus (de-energized via shunt-trip); BMS publishes E-STOP mode on UPS power | MODES-001 E-STOP; 480 V AC absent | 0 s (hardware) | SIL 2 (architecture) | 6-month |
| SIF-12 | MIV dual-fail — both valves fail to close on command | ZS-MIV-S-CLOSED AND ZS-MIV-R-CLOSED (neither asserted within 30 s of commanded close) | BMS | DO-WL-ENABLE (already 0 in the triggering safe-state); SCADA dispatch for manual intervention | MODES-001 SAFE-STATE + manual dispatch | 30 s | SIL 1 (interim) | 12-month |
| SIF-13 | Single-zone leak — protective function (not SIL-rated) | TK-ZA-WET OR TK-ZB-WET (single) | BMS (alarm engine) | DO-WL-ENABLE via workload-throttle-request to platform; not final-element forced | MODES-001 DEGRADED (PRODUCTION → DEGRADED with severity 2 throttle-request) | N/A (not SIL-rated) | N/A | Covered in CTRL-001 alarm-engine test; no separate proof-test |
| SIF-14 | Hardware watchdog — Jetson heartbeat loss | Heartbeat pulse on dedicated discrete output from Jetson (≤ 1 Hz) | Hardware watchdog relay — independent of BMS software and I/O bus power | DO-HW-SAFE-STATE-LATCH (dry contact to CDU skid safe-state input); 24 VDC removed from S04 DO card power rail (de-energizes DO-MIV-S-OPEN, DO-MIV-R-OPEN, DO-WL-ENABLE, DO-FIRE-RELEASE); DO-FIRE-ARM remains de-energized on its own rail (panel armed) | Cassette driven to SAFE-STATE by de-energization of S04 DOs; CDU skid goes to its own safe state via the hardwired dry contact | 5 s | SIL 2 (architecture — pending SIS-04 datasheet) | 6-month |

### 4.2 SIF-01 — Fire detection and response

**Hazard.** Fire inside the Cassette envelope — Class A (insulation, PCB substrate) or Class C (energized-equipment) ignition, with or without Li-ion BBU thermal runaway contribution. Suppression delay results in structural and equipment damage and risk to personnel if occupied.

**Initiator logic.** `FIRE-DI-1` (Cassette-TAGS-001 §4.1) asserts when the Ansul clean-agent panel enters its CONFIRMED ALARM state (cross-zone 2-of-N satisfied, or manual release station activated). The BMS reads this DI on ≥ 1 Hz scan (Cassette-TAGS-001 §2.3). The triggering alarm ID is `FIRE-TRIGGERED` CRITICAL, TTA 0 s, per Cassette-CTRL-001 §6.2.

**Logic solver.** BMS (CTRL-001 §2) is the software logic solver for the BMS response. The Ansul panel (Cassette-FIRE-001) is an independent peer logic solver for the detection and release path per NFPA 72; the two layers act in parallel on the same event.

**Final element actions.** On `FIRE-TRIGGERED`:

- `DO-WL-ENABLE` → 0 (de-energized; workload inhibited)
- `CMD-PUMP-ENABLE` → 0 (Modbus write to CDU skid, Coil 40002)
- `DO-MIV-S-OPEN` → 0 (supply MIV spring-returns closed)
- `DO-MIV-R-OPEN` → 0 (return MIV spring-returns closed)
- `DO-FIRE-ARM` → 0 (fire panel armed, inhibit removed — per Cassette-FIRE-001 §8.5 safe-state rule)
- `fire_event.flag` written to `/var/bms/state/fire_event.flag`
- `OT-MODE-CURRENT` → "SAFE-STATE"; `OT-MODE-FIRE-EVENT` → true

Per position SIS-11: the BMS must complete all four safe-state actions (workload, pumps, MIVs, mode) within 5 s of `FIRE-DI-1` assertion — well inside the 30 s PST.

**Safe state outcome.** MODES-001 SAFE-STATE with `fire_event = true`. Munters is hardware-controlled OFF via the FIRE-001 §9.1 hardwired NC interlock (not mediated by BMS — the BMS has no authority over Munters stop during fire).

**PST.** 30 s — bounded by the Ansul panel's pre-discharge countdown. The BMS must reach safe state before the panel commands agent discharge. 5 s BMS target leaves 25 s contingency.

**SIL target.** SIL 1 (interim). The independent Ansul panel layer supports a higher overall layer-of-protection assessment but that is resolved in LOPA (SIS-01).

**Proof-test interval.** 6-month (per position SIS-07). Fire panel proof-testing per Cassette-FIRE-001 §13 is a separate NFPA 72 cadence; SIS-001 proof-tests the BMS-side of the handshake.

**Failure-mode notes.** Loss of 24 VDC loop power on the FIRE-DI-1 cable opens the NC contact, which is interpreted as FIRE-TRIGGERED — fail-safe toward alarm. If `FIRE-DI-3` (panel fault) is also asserted concurrently, the BMS still enters SAFE-STATE on FIRE-DI-1; the four-gate condition for DO-FIRE-RELEASE (Cassette-FIRE-001 §8.6) is not met (gate 2 requires FIRE-DI-3 clear), so the BMS does not send a remote release; the panel acts autonomously per its own internal logic.

### 4.3 SIF-02 — Coolant flow loss

**Hazard.** Loss of coolant circulation through the Cassette secondary loop under active GPU workload.

**Initiator logic.** `FT-102` < 50 % of commissioned setpoint for 0 s (TTA 0 s for CRITICAL per CTRL-001 §6.2). Triggering alarm ID: `FLOW-LO-C` CRITICAL. FT-102 read from CDU skid PLC IR 30010–11 over Modbus TCP at 1 Hz (Cassette-TAGS-001 §5.4).

**Logic solver.** BMS.

**Final element actions.** `DO-WL-ENABLE` → 0, `CMD-PUMP-ENABLE` → 0, `DO-MIV-S-OPEN` → 0, `DO-MIV-R-OPEN` → 0. CDU pumps commanded off because the flow-loss root cause is often skid-side (pump fault, filter block); commanding pumps off prevents continued dry-run.

**Safe state outcome.** MODES-001 SAFE-STATE, `fire_event = false`.

**PST.** 60 s — based on GPU thermal mass at maximum load; confirmation by thermal model is SIS-05.

**SIL target.** SIL 1 (interim).

**Proof-test interval.** 12-month.

**Failure-mode notes.** FT-102 stuck-at-value is a dangerous failure mode (flow reads nominal while actual is zero). Partial mitigation: TT-103 and TT-104 temperature escalation (SIF-03, SIF-04) catches the consequence. CDU-COMMS-LOST ALARM provides diagnostic coverage if Modbus link itself fails.

### 4.4 SIF-03 — Supply temperature high-high

**Hazard.** CDU skid or PHX failing to reject heat; supply water exceeding safe GPU inlet temperature.

**Initiator logic.** `TT-103` > 60 °C, TTA 0 s. Alarm ID: `SUPPLY-T-HI-C` CRITICAL (CTRL-001 §6.2).

**Logic solver.** BMS.

**Final element actions.** Same as SIF-02.

**Safe state outcome.** MODES-001 SAFE-STATE.

**PST.** 60 s (SIS-05).

**SIL target.** SIL 1 (interim).

**Proof-test interval.** 12-month.

**Failure-mode notes.** TT-103 stuck-high is a spurious trip (safe, conservative). TT-103 stuck-low is dangerous; partial mitigation is TT-INT interior temperature escalation and independent rack-BMC inlet temperatures (CTRL-001 §9 IPMI telemetry, not a SIS input).

### 4.5 SIF-04 — Return temperature high-high

**Hazard.** PHX degradation or GPU over-duty pushing return temperature beyond safe envelope; indicates heat not being rejected downstream.

**Initiator logic.** `TT-104` > 62 °C, TTA 0 s. Alarm ID: `RETURN-T-HI-C` CRITICAL.

**Logic solver.** BMS.

**Final element actions.** Same as SIF-02.

**Safe state outcome.** MODES-001 SAFE-STATE.

**PST.** 60 s.

**SIL target.** SIL 1 (interim).

**Proof-test interval.** 12-month.

**Failure-mode notes.** Correlation with TT-103: if both rise together, indicates CDU skid heat rejection failing; if TT-104 rises while TT-103 holds, indicates internal Cassette over-duty. BMS does not distinguish — both paths land in SAFE-STATE.

### 4.6 SIF-05 — Supply pressure high-high

**Hazard.** Hydraulic transient, pump VFD runaway, valve mis-operation; risk of PHX overload or fitting failure and subsequent leak.

**Initiator logic.** `PT-101` > 6.5 bar(g), TTA 0 s. Alarm ID: `LOOP-P-HI-C` CRITICAL.

**Logic solver.** BMS.

**Final element actions.** Same as SIF-02. Note: commanding pumps off is the primary mitigation for high-pressure events because the pump is the pressure source.

**Safe state outcome.** MODES-001 SAFE-STATE.

**PST.** 15 s — hydraulic transient; longer than SIF-06 because pressure relief exists upstream at the CDU skid (COOL2-001).

**SIL target.** SIL 1 (interim).

**Proof-test interval.** 12-month.

**Failure-mode notes.** Mechanical pressure relief at the CDU skid is a separate protection layer (not within this SIS scope); its failure is a LOPA input for overall risk assessment.

### 4.7 SIF-06 — Supply pressure low-low

**Hazard.** Pump cavitation, dry-run, loss of loop integrity from a large leak upstream. Pump damage within seconds of dry-run at speed.

**Initiator logic.** `PT-101` < 1.5 bar(g), TTA 0 s. Alarm ID: `LOOP-P-LO-C` CRITICAL.

**Logic solver.** BMS.

**Final element actions.** Same as SIF-02.

**Safe state outcome.** MODES-001 SAFE-STATE.

**PST.** 10 s — pump damage mechanism is fast.

**SIL target.** SIL 1 (interim).

**Proof-test interval.** 12-month.

**Failure-mode notes.** Often co-triggers with TK-ZA-WET or TK-ZB-WET (if the low pressure is caused by a leak). BMS processes both independently; co-trigger does not change the safe-state response.

### 4.8 SIF-07 — Dual-zone leak

**Hazard.** Two independent TraceTek zones report wet — evidence of a substantive leak that has spread beyond a single containment area. Risk of electrical short on live 480 V AC bus, fluid on energized equipment, fire escalation.

**Initiator logic.** `TK-ZA-WET` AND `TK-ZB-WET` both asserted. TTA 0 s. Alarm ID: `TRACETEK-DUAL-WET-C` CRITICAL.

**Logic solver.** BMS. A single-zone wet event is SIF-13 (protective function, DEGRADED). The escalation from single-zone ALARM to dual-zone CRITICAL is handled by the BMS alarm engine — SIS-07 open item verifies the escalation path correctness.

**Final element actions.** Same as SIF-02.

**Safe state outcome.** MODES-001 SAFE-STATE.

**PST.** 300 s — a dual-zone wet event is the result of an accumulating leak; the 300 s envelope represents the total window from first-zone wet to second-zone wet during which DEGRADED operations are acceptable. Once the second zone asserts, the BMS reaches SAFE-STATE within its normal < 5 s scan-to-response loop.

**SIL target.** SIL 1 (interim).

**Proof-test interval.** 12-month.

**Failure-mode notes.** TraceTek FAULT on a zone (TK-ZA-FAULT or TK-ZB-FAULT) is a supervisory WARN and does not mask the corresponding WET channel — the two are separate DIs (Cassette-TAGS-001 §10). Dual FAULT on both zones, however, is a CCF concern (§8, CCF-4) and the combination is not automatically detected as a SIF demand — it requires proof-test detection.

### 4.9 SIF-08 — Sump high-high

**Hazard.** Active leak exceeding the primary containment sump's first float set-point; fluid reaching the higher float indicates escalation toward Cassette envelope breach.

**Initiator logic.** `LT-SUMP-HIHI` asserted. TTA 0 s. Alarm ID: `SUMP-HIHI-C` CRITICAL.

**Logic solver.** BMS.

**Final element actions.** Same as SIF-02.

**Safe state outcome.** MODES-001 SAFE-STATE.

**PST.** 60 s — sump HIHI represents fluid volume already accumulated; immediate response is required to prevent the leak source from continuing to fill beyond the sump's design volume.

**SIL target.** SIL 1 (interim).

**Proof-test interval.** 12-month.

**Failure-mode notes.** LT-SUMP-HI (first float) generates ALARM → DEGRADED (not a SIF); if the leak is being actively managed while in DEGRADED, SIF-08 is the escalation path if the leak is not resolved in time.

### 4.10 SIF-09 — CDU pumps all-off during workload

**Hazard.** Complete loss of CDU circulation while GPU workload is active — immediate coolant starvation.

**Initiator logic.** All reported `STS-PUMP-RUN` states = 0 (i.e., every pump reports not-running) while `DO-WL-ENABLE` = 1. TTA 10 s per CTRL-001 §6.2 `CDU-PUMP-ALL-OFF` CRITICAL.

**Logic solver.** BMS. This SIF differs from SIF-02 in the initiator: SIF-02 is flow-based (FT-102 directly reads flow), SIF-09 is pump-state-based (combination of three pump status enums). Both are present because a single-point failure (flow meter fault) should not defeat detection — the two SIFs are independent detectors of overlapping hazards.

**Final element actions.** Same as SIF-02.

**Safe state outcome.** MODES-001 SAFE-STATE.

**PST.** 10 s.

**SIL target.** SIL 1 (interim).

**Proof-test interval.** 12-month.

**Failure-mode notes.** CDU skid Modbus link failure (CDU-COMMS-LOST ALARM) is a diagnostic for this SIF — if the BMS cannot read pump states, it cannot detect the all-off condition via SIF-09. Partial mitigation: hardwired STS-PUMP-RUN-DI fallback on S03 (CCF-3, SIS-001 §8) and FT-102 diagnostic path on the same link (if one Modbus tag fails, likely all fail — so the mitigation is the S03 fallback, which is hardwired, not Modbus).

### 4.11 SIF-10 — Extended power loss during workload

**Hazard.** 480 V AC absence extended beyond a threshold where UPS depletion is a credible risk and workload-enabled state is no longer supportable.

**Initiator logic.** `DI-POWER-OK` deasserted (0) continuously for ≥ 300 s while `DO-WL-ENABLE` = 1. TTA 300 s per CTRL-001 §6.2 `POWER-LOSS-EXT` CRITICAL.

**Logic solver.** BMS, on UPS power.

**Final element actions.** `DO-WL-ENABLE` → 0; `CMD-PUMP-ENABLE` → 0 (Modbus may already be unavailable — CDU skid has likely lost 480 V AC too — write is attempted; if link is down the skid is already stopped physically); `DO-MIV-S-OPEN` → 0, `DO-MIV-R-OPEN` → 0 (MIV actuators on 24 VDC UPS still drive to closed under command).

**Safe state outcome.** MODES-001 SAFE-STATE.

**PST.** 300 s.

**SIL target.** SIL 1 (interim).

**Proof-test interval.** 12-month.

**Failure-mode notes.** If UPS itself fails during the 300 s window (DI-UPS-OK deasserts), BMS transitions to E-STOP by the E-stop path — all DOs de-energize by loss of power, which is the same outcome. If AC is restored inside 300 s without a `planned-shutdown` flag, no SAFE-STATE; POWER-LOSS ALARM logs the excursion.

### 4.12 SIF-11 — Emergency stop

**Hazard.** Any condition requiring immediate manual de-energization of the Cassette. Initiating events include: operator-observed hazard not otherwise detected, platform NOC command in response to external emergency, any condition the operator judges requires a superset of SAFE-STATE.

**Initiator logic.** `DI-ESTOP` asserted (NC contact opens). E-stop pushbutton wiring is hardwired directly to ELEC-001 shunt-trip coil, independent of BMS software — pressing the button trips the 480 V AC main breaker in hardware. Alarm ID: `ESTOP-ACTIVE` CRITICAL (for log/record purposes; the alarm does not drive the trip because the trip is already mechanically committed).

**Logic solver.** ELEC-001 shunt-trip circuit — pure hardware, no BMS software in the trip path. Per position SIS-02, this is a separate logic solver from the BMS software layer.

**Final element actions.** ELEC-001 shunt-trip opens 480 V AC main breaker. 480 V AC bus de-energizes. Consequences: CDU skid pumps stop (lose 480 V AC); Munters stops; Cassette compute racks lose 480 V AC through the ORV3 PDUs; BMS continues on 24 VDC UPS for at least 30 min.

**Safe state outcome.** MODES-001 E-STOP (distinct from SAFE-STATE because 480 V AC is absent). BMS publishes the mode transition within 3 s of DI-POWER-OK deasserting following E-stop button press.

**PST.** 0 s — hardware action; shunt-trip is substantially faster than any software PST. No software PST applies.

**SIL target.** SIL 2 (architecture). The claim is based on hardwired design with no software dependency in the trip path. Quantitative SIL confirmation requires selected shunt-trip breaker PFDavg data (SIS-08) and is part of the overall FSA (SIS-01).

**Proof-test interval.** 6-month.

**Failure-mode notes.** E-stop pushbutton dormant failure is the primary dangerous failure mode. Proof-test is executive (physical button press), so coverage is high. Platform `e-stop-request` over OPC-UA is a separate initiator path that reaches ELEC-001 shunt-trip through the BMS — see §10 demand-mode note — but the button path is the SIL 2 claim.

### 4.13 SIF-12 — MIV dual-fail

**Hazard.** Both isolation valves fail to close on command during a safe-state entry. Cassette coolant loop cannot be isolated; leak or contamination propagates to/from the CDU skid.

**Initiator logic.** `DO-MIV-S-OPEN` = 0 AND `DO-MIV-R-OPEN` = 0 commanded, AND `ZS-MIV-S-CLOSED` NOT asserted AND `ZS-MIV-R-CLOSED` NOT asserted, continuously for 30 s. TTA 30 s per CTRL-001 §6.2 `MIV-DUAL-FAIL` CRITICAL.

**Logic solver.** BMS.

**Final element actions.** `DO-WL-ENABLE` is already 0 (triggering safe-state caused SIF-12 as a secondary failure). BMS publishes CRITICAL to NOC for manual dispatch. No additional automated mitigation — if both MIVs cannot close, there is no further automatic action available inside the Cassette.

**Safe state outcome.** MODES-001 SAFE-STATE with manual-dispatch flag. Platform NOC dispatches on-site response; physical valve closure via handwheel or upstream CDU-skid-side isolation may be required.

**PST.** 30 s — the same 30 s window used to detect the closure failure. Note: SIF-12 is a degraded-mitigation SIF; the consequence of the triggering event (whatever drove the initial SAFE-STATE entry — say, a leak) continues unchecked until manual intervention. This is an accepted residual risk for the CASSETTE at SL 1; a LOPA outcome may require a third isolation valve or redundant actuator to reach SIL 2 if the consequence severity warrants (SIS-01).

**SIL target.** SIL 1 (interim).

**Proof-test interval.** 12-month.

**Failure-mode notes.** Single MIV failure is detected as MIV-S-MISMATCH-W or MIV-R-MISMATCH-W WARN (CTRL-001 §6.2), which is a DEGRADED-level awareness indicator only; the single-valve failure does not prevent isolation because the other valve still closes. Dual failure is the SIF case.

### 4.14 SIF-13 — Single-zone leak (protective function, not SIL-rated)

**Hazard.** Early indicator of a developing coolant leak — one TraceTek zone reports wet while the other remains dry.

**Initiator logic.** `TK-ZA-WET` OR `TK-ZB-WET` (exclusive of both asserted). Alarm IDs: `TRACETEK-ZA-WET-A` or `TRACETEK-ZB-WET-A` ALARM, TTA 0 s.

**Logic solver.** BMS alarm engine.

**Response.** PRODUCTION → DEGRADED transition per MODES-001 §7; `VT-WL-THROTTLE-REQ` published with severity 2; operator dispatched.

**Safe state outcome.** NOT applicable — SIF-13 is a protective function, not a safety instrumented function. The Cassette remains in DEGRADED under workload-throttle-request; SAFE-STATE is entered only if the single-zone wet escalates to dual-zone (SIF-07) or via another CRITICAL path.

**PST.** N/A (not SIL-rated).

**SIL target.** N/A.

**Proof-test interval.** Covered by CTRL-001 §14 alarm-engine testing; no separate proof-test under SIS-001. SIS-001 §6 PT-SIF-07 (dual-zone proof-test) exercises both TraceTek zones and by extension the single-zone path.

**Failure-mode notes.** This entry is included in the SIF list numerically for completeness; it is explicitly **not** a SIF under IEC 61511 because it does not take the process to safe state. It is documented here so that a later auditor does not ask why TK-ZA-WET and TK-ZB-WET appear as initiators in SIF-07 but single-zone wet is not separately listed.

### 4.15 SIF-14 — Hardware watchdog

**Hazard.** BMS software fault or Jetson OS crash prevents software logic solver from responding to any SIF demand.

**Initiator logic.** Heartbeat pulse on dedicated discrete output from the Jetson, expected ≤ 1 Hz. If the watchdog relay detects no pulse for ≥ 5 s, the watchdog trips.

**Logic solver.** Hardware watchdog relay — a DIN-rail safety relay on the ECP panel, electrically independent of the BMS I/O bus and the BMS I/O bus power supply. Per position SIS-10, the watchdog is a separate second logic solver layer and does not share fault paths with the BMS software.

**Final element actions.** When the watchdog trips (NC contact opens):

- `DO-HW-SAFE-STATE-LATCH` is hardwired to the CDU skid safe-state input per Cassette-TAGS-001 §3.2. CDU skid goes to its own safe state (pumps off, last setpoint held) regardless of Modbus status
- 24 VDC is removed from the S04 DO card power rail. This simultaneously de-energizes `DO-MIV-S-OPEN`, `DO-MIV-R-OPEN`, `DO-WL-ENABLE`, and `DO-FIRE-RELEASE` in a single action. MIVs spring-return to closed. Workload-enable relay opens. Remote-release cannot be commanded.
- `DO-FIRE-ARM` is on a separate circuit (not on the S04 rail — per Cassette-ECP-001 and Cassette-TAGS-001 §3.1) and remains in its pre-trip state; by MODES-001 rule, that is de-energized (panel armed).

**Safe state outcome.** Cassette reaches its physical safe state by hardware without any BMS software involvement. When the Jetson recovers, it cold-boots into MODES-001 INIT per MODES-001 §14 cold-start rule.

**PST.** 5 s.

**SIL target.** SIL 2 (architecture claim, pending SIS-04 datasheet).

**Proof-test interval.** 6-month.

**Failure-mode notes.** Dangerous failure modes of a well-specified safety relay are quantified in manufacturer datasheets; SIS-04 obtains the data for PFDavg calculation. The watchdog cannot be disabled from BMS software — the BMS has no command path to the watchdog other than the heartbeat (which only serves to keep the watchdog un-tripped). Cable/terminal damage to the heartbeat pair is fail-safe (heartbeat lost → watchdog trips).

---

## 5. Logic solver description

Per position SIS-02.

### 5.1 Layered logic solver architecture

Three independent logic solvers participate in safety response on this Cassette. They share the same physical enclosure (ECP panel) but are architecturally and power-wise independent.

| Layer | Logic solver | SIF coverage | Independence basis |
|---|---|---|---|
| 1 | **BMS software** — Jetson Orin NX running `adc-bms` application, DIN-rail I/O bus (S01–S08 per Cassette-TAGS-001 §3.1) | SIF-01 through SIF-13 (software-path SIFs) | Reads the initiator tags, evaluates alarm conditions per Cassette-CTRL-001 §6.2, commands final elements per this document |
| 2 | **Hardware watchdog relay** — DIN-rail safety relay on separately-fused 24 VDC branch | SIF-14 only | Receives heartbeat from Jetson GPIO; if heartbeat lost, opens NC contact that removes S04 DO card power; electrically independent of Jetson I/O bus and I/O bus power supply; cannot be disabled from software |
| 3 | **Ansul clean-agent control panel** — certified NFPA 72 logic solver | SIF-01 (fire release — the panel side of the handshake; the BMS side is Layer 1) | Independent detection, independent 24 h battery, independent release solenoid command; communicates with BMS via three DI contacts + two DO contacts (Cassette-TAGS-001 §4) but does not require the BMS to release |

### 5.2 BMS scan loop timing

The BMS achieves its ≤ 1 Hz DI scan rate through a dedicated `io-scanner` worker in the `adc-bms` application (Cassette-CTRL-001 §5.2). The loop reads all DI channels on S02 and S03, all AI channels on S05, and polls the CDU skid PLC Modbus registers, in a single loop iteration. Loop target period: 500 ms; loop budget: 1 s. Under normal load the loop is measured at 200–400 ms per iteration. Alarm evaluation occurs in the `alarm-engine` worker consuming tag values from the in-process bus; TTA and deadband logic lives there.

**DI transition to safe-state action latency:** for a safety-critical DI like `FIRE-DI-1` or `LT-SUMP-HIHI`, measured end-to-end latency from DI transition to S04 DO de-energized is target ≤ 2 s, budget 5 s. This is the figure that matters for the PST calculations in §4 — SIF-01 PST 30 s vs 5 s target means large contingency.

**Modbus write latency:** `CMD-PUMP-ENABLE` = 0 write is write-on-change, target ≤ 500 ms from alarm trigger to PLC acknowledgement. CDU skid PLC scan rate sets the actual physical response (pump run contactor drops), which is skid-side and not BMS-controllable; typical < 2 s per Cassette-COOL2-001 §9.

### 5.3 Independence claims and shared failure domains

**Genuine independences:**

- BMS software vs hardware watchdog — separately fused 24 VDC branches; watchdog relay does not depend on Jetson OS, BMS application, Modbus link, or OPC-UA server
- BMS software vs Ansul panel — Ansul panel has its own 120 V AC feed + 24 h battery; fire detection is entirely the panel's job; the BMS observes and does not command detection
- BMS software vs ELEC-001 shunt-trip — shunt-trip is hardwired from the E-stop pushbutton; BMS is an observer via DI-ESTOP

**Shared failure domains (addressed in §8 CCF register):**

- BMS and hardware watchdog share the ECP panel enclosure — a fire inside the ECP panel could compromise both. Mitigated by physical separation of watchdog relay on DIN rail with separate fuse; the Ansul panel is the protection for this scenario
- BMS and hardware watchdog share the 24 VDC UPS source at the branch-supply level (separate fuses, same UPS) — UPS failure de-energizes both, which is the fail-safe direction

---

## 6. Proof-test procedures

Per position SIS-07. Every proof-test in this section is executed in MODES-001 STANDBY-MAINT-GENERAL or STANDBY-MAINT-COOLANT (no proof-test may be initiated in PRODUCTION, READY, or DEGRADED). Every proof-test is logged to the proof-test record system (SIS-03) with: SIF ID, test date, operator identity, pass/fail, anomalies noted, as-left state. Mandatory LOTO per Cassette-ELEC-001 LOTO procedure where applicable (SIS-06).

### PT-SIF-01 — Fire detection and BMS response

**SIF covered.** SIF-01.
**Test interval.** 6-month.
**Prerequisite mode.** STANDBY-MAINT-COOLANT. DO-FIRE-ARM energized (panel inhibit active) for the initial panel-side smoke injection; then the operator transitions to a staged test where DO-FIRE-ARM is de-energized for the BMS-response portion. Coordinated with Ansul-authorized service technician.

**Steps.**

1. Verify `OT-MODE-CURRENT` = "STANDBY-MAINT-COOLANT" and `FIRE-DI-2` = asserted-open (inhibited).
2. Ansul technician executes panel-side smoke-injection cross-zone test per Cassette-FIRE-001 §12 SP-05 — not part of this proof-test pass/fail but prerequisite for state setup.
3. Operator de-energizes DO-FIRE-ARM via authenticated NOC `exit-maintenance` command, returning panel to armed. Verify `FIRE-DI-2` closes within 1 s.
4. BMS technician asserts `FIRE-DI-1` via panel's test-mode "simulate confirmed alarm" function. Record timestamp t₀.
5. Verify within 5 s of t₀: `DO-WL-ENABLE` = 0, `CMD-PUMP-ENABLE` = 0 (confirmed by Modbus read-back of register 40002), `DO-MIV-S-OPEN` = 0, `DO-MIV-R-OPEN` = 0, `DO-FIRE-ARM` = 0.
6. Verify within 10 s of t₀: `ZS-MIV-S-CLOSED` and `ZS-MIV-R-CLOSED` both asserted.
7. Verify `OT-MODE-CURRENT` = "SAFE-STATE" and `OT-MODE-FIRE-EVENT` = true at OPC-UA path `adc.cassette.<serial>.mode.fire_event`.
8. Verify `/var/bms/state/fire_event.flag` exists and contains current timestamp.

**Pass/fail criteria.** All step 5 items reach stated values within 5 s (PST margin). Step 6 within 10 s. Step 7 within 10 s total. Any step failing is a PROOF-TEST-FAIL against SIF-01 and must be remediated before Cassette returns to PRODUCTION.

**Restoration.** Clear FIRE-DI-1 panel test (panel reset with service key). Operator runs full five-gate fire-recovery procedure per MODES-001 §9.2 even though no actual discharge occurred — this is consistent with the BMS enforcement of the recovery-gates.json path. Enter STANDBY-IDLE and confirm normal operation resumption.

### PT-SIF-02 — Coolant flow loss response

**SIF covered.** SIF-02.
**Test interval.** 12-month.
**Prerequisite mode.** STANDBY-MAINT-COOLANT. LOTO note: this test requires pumps to be running at low flow then commanded off — which in STANDBY-MAINT-COOLANT is only achievable by a temporary pump-on state that is not a normal maintenance state. Mark as SIS-06 open item for LOTO alignment. Interim procedure: execute test by overriding the FT-102 simulated value via Modbus write to a controlled-test register on the CDU skid PLC (requires TAGS-03 resolution for skid-side cooperation).

**Steps.**

1. Verify `OT-MODE-CURRENT` = "STANDBY-MAINT-COOLANT", `DO-WL-ENABLE` = 0.
2. Operator energizes `DO-MIV-S-OPEN` and `DO-MIV-R-OPEN` via maintenance override (permitted in MAINT-COOLANT with explicit NOC confirmation); verify open limits.
3. Command CDU skid pumps to low-speed run (via maintenance Modbus write). Verify FT-102 > 50 % of commissioned setpoint on the BMS.
4. Override FT-102 simulated value to < 50 % of commissioned setpoint by injection at the CDU skid PLC test register. Record timestamp t₀.
5. Verify within 60 s of t₀ (PST): `DO-WL-ENABLE` = 0 (already was), `CMD-PUMP-ENABLE` = 0 (Modbus write-back verified), `DO-MIV-S-OPEN` = 0, `DO-MIV-R-OPEN` = 0, MIVs reach closed limits within 10 s.
6. Verify `OT-MODE-CURRENT` = "SAFE-STATE" and `OT-MODE-FIRE-EVENT` = false.

**Pass/fail criteria.** Safe-state actions complete within 5 s of t₀; PST budget 60 s.

**Restoration.** Clear FT-102 override; execute MODES-001 §6.4 safe-state reset; return to STANDBY-MAINT-COOLANT.

### PT-SIF-03 — Supply temperature HI-HI response

**SIF covered.** SIF-03.
**Test interval.** 12-month.
**Prerequisite mode.** STANDBY-MAINT-COOLANT.

**Steps.**

1. Verify preconditions (MAINT-COOLANT mode).
2. Inject simulated TT-103 value via CDU skid PLC test register at 62 °C (> 60 °C threshold). Record t₀.
3. Verify within 60 s of t₀: safe-state actions per §4.4.
4. Verify `OT-MODE-CURRENT` = "SAFE-STATE".

**Pass/fail criteria.** Safe state reached within 5 s of t₀.

**Restoration.** Clear simulated TT-103 override; §6.4 reset.

### PT-SIF-04 — Return temperature HI-HI response

**SIF covered.** SIF-04.
**Test interval.** 12-month.
**Prerequisite mode.** STANDBY-MAINT-COOLANT.

**Steps.**

1. Verify preconditions.
2. Inject simulated TT-104 value at 63 °C (> 62 °C threshold). Record t₀.
3. Verify within 60 s: safe-state actions per §4.5.
4. Verify mode tag.

**Pass/fail criteria.** Safe state reached within 5 s of t₀.

**Restoration.** Clear override; §6.4 reset.

### PT-SIF-05 — Supply pressure HI-HI response

**SIF covered.** SIF-05.
**Test interval.** 12-month.
**Prerequisite mode.** STANDBY-MAINT-COOLANT.

**Steps.**

1. Verify preconditions.
2. Inject simulated PT-101 value at 7.0 bar(g) (> 6.5 bar threshold). Record t₀.
3. Verify within 15 s: safe-state actions per §4.6.
4. Verify mode tag.

**Pass/fail criteria.** Safe state reached within 5 s of t₀.

**Restoration.** Clear override; §6.4 reset.

### PT-SIF-06 — Supply pressure LO-LO response

**SIF covered.** SIF-06.
**Test interval.** 12-month.
**Prerequisite mode.** STANDBY-MAINT-COOLANT.

**Steps.**

1. Verify preconditions.
2. Inject simulated PT-101 value at 1.0 bar(g) (< 1.5 bar threshold). Record t₀.
3. Verify within 10 s: safe-state actions.
4. Verify mode tag.

**Pass/fail criteria.** Safe state reached within 5 s of t₀; pump stop Modbus write verified within 2 s.

**Restoration.** Clear override; §6.4 reset.

### PT-SIF-07 — Dual-zone leak response

**SIF covered.** SIF-07.
**Test interval.** 12-month.
**Prerequisite mode.** STANDBY-MAINT-GENERAL (no coolant loop work required; physical access to TraceTek cables required).

**Steps.**

1. Verify preconditions.
2. Apply moisture (damp cloth with deionized water) to TraceTek Zone A detector at a known location. Record t₀.
3. Verify TK-ZA-WET asserts within 10 s of t₀. Verify `TRACETEK-ZA-WET-A` ALARM raised and `OT-MODE-CURRENT` remains "STANDBY-MAINT-GENERAL" (no SAFE-STATE on single-zone in maintenance mode; alarm logged only).
4. Apply moisture to TraceTek Zone B detector. Record t₁.
5. Verify TK-ZB-WET asserts within 10 s of t₁. Verify `TRACETEK-DUAL-WET-C` CRITICAL raised.
6. Verify within 300 s of t₀ (PST): safe-state actions per §4.8.
7. Verify `OT-MODE-CURRENT` = "SAFE-STATE".

**Pass/fail criteria.** Dual-zone CRITICAL correctly escalates from single-zone ALARM state; safe-state reached within 5 s of the second-zone assertion (note: 300 s PST measures the window during which single-zone ALARM is tolerated while SAFE-STATE is not yet demanded; once the second zone asserts, response time is normal).

**Restoration.** Dry both TraceTek zones; wait for cables to confirm dry (TT-SIM-2 controller clears); §6.4 reset.

**Also exercises SIF-13** by satisfying the single-zone portion of this procedure.

### PT-SIF-08 — Sump HI-HI response

**SIF covered.** SIF-08.
**Test interval.** 12-month.
**Prerequisite mode.** STANDBY-MAINT-COOLANT.

**Steps.**

1. Verify preconditions.
2. Operator manually raises the LSHH-01 float switch to asserted position (using a ball on a string tool that raises the float without filling the sump). Alternatively: fill sump with controlled volume of water to reach second float.
3. Verify LT-SUMP-HIHI asserts within 10 s. Record t₀.
4. Verify within 60 s: safe-state actions per §4.9.
5. Verify mode tag.

**Pass/fail criteria.** Safe state reached within 5 s of t₀.

**Restoration.** Release float; pump sump dry; §6.4 reset.

### PT-SIF-09 — CDU pumps all-off during workload

**SIF covered.** SIF-09.
**Test interval.** 12-month.
**Prerequisite mode.** STANDBY-MAINT-COOLANT.

**Steps.**

1. Verify preconditions.
2. Establish simulated "workload active" by maintenance override (DO-WL-ENABLE = 1 for test purposes without actual workload on the compute racks; requires SIS-06 LOTO alignment to confirm safe execution).
3. Command CDU skid pumps to run at low speed via maintenance Modbus write.
4. Commence test: command all CDU skid pumps to stop (STS-PUMP-RUN = 0 for all) by maintenance Modbus write or by interrupting skid-side run-permit. Record t₀.
5. Verify within 10 s of t₀: `DO-WL-ENABLE` = 0 (BMS safe-state); MIVs closed; CMD-PUMP-ENABLE = 0 confirmed.
6. Verify mode tag = SAFE-STATE.

**Pass/fail criteria.** Safe state reached within 5 s of t₀; CDU-PUMP-ALL-OFF CRITICAL logged.

**Restoration.** Clear maintenance overrides; §6.4 reset.

### PT-SIF-10 — Extended power loss response

**SIF covered.** SIF-10.
**Test interval.** 12-month.
**Prerequisite mode.** STANDBY-MAINT-GENERAL. No actual 480 V AC loss is executed — simulated via DI-POWER-OK injection at the S02 DI card.

**Steps.**

1. Verify preconditions and that DI-UPS-OK = 1.
2. Establish simulated "workload active" (DO-WL-ENABLE = 1 by maintenance override). Record t₀.
3. At t₀, inject DI-POWER-OK = 0 at the S02 DI card (physical jumper removal on the maintenance test block, LOTO-controlled).
4. Verify POWER-LOSS ALARM raised at t₀ + 3 s.
5. Wait 305 s. At t₀ + 305 s, verify POWER-LOSS-EXT CRITICAL raised.
6. Verify within 5 s of CRITICAL: safe-state actions; mode tag = SAFE-STATE.

**Pass/fail criteria.** POWER-LOSS ALARM at 3 s; POWER-LOSS-EXT CRITICAL at 300 s; safe state reached within 5 s of CRITICAL.

**Restoration.** Clear DI-POWER-OK injection; §6.4 reset.

### PT-SIF-11 — E-stop hardware trip

**SIF covered.** SIF-11.
**Test interval.** 6-month.
**Prerequisite mode.** STANDBY-MAINT-GENERAL. Coordinated with ELEC-001 LOTO; the breaker is going to be tripped.

**Steps.**

1. Verify preconditions; notify platform NOC of planned E-stop test; confirm no adjacent Cassette workload dependency.
2. Physically press the ECP panel E-stop mushroom button. Record t₀.
3. Verify within 1 s of t₀: 480 V AC main breaker tripped (ELEC-001 feedback aux contact); DI-POWER-OK deasserts; BMS remains on UPS (DI-UPS-OK = 1); `OT-MODE-CURRENT` = "E-STOP" (published by BMS within 3 s).
4. Verify all DOs on S04 are de-energized (loss of 480 V AC on upstream rails); CDU skid pumps physically stopped (lost 480 V AC); Munters stopped (lost 480 V AC).
5. Verify BMS continues to publish OPC-UA tags on UPS power; verify at least 5 min of continued heartbeat.

**Pass/fail criteria.** 480 V AC bus de-energized within 1 s of button press; BMS transitions to E-STOP mode within 3 s; BMS continues on UPS for > 30 min expected (test to 5 min is sufficient for proof-test).

**Restoration.** Release E-stop button. Field engineer physically resets ELEC-001 shunt-trip breaker per ELEC-001 §6. Confirm DI-POWER-OK reasserts. Platform NOC issues `e-stop-acknowledge`. Verify mode transitions "E-STOP" → "STANDBY-IDLE". If UPS depleted during test, observe cold-boot path "E-STOP" → INIT → STANDBY-IDLE.

### PT-SIF-12 — MIV dual-fail detection

**SIF covered.** SIF-12.
**Test interval.** 12-month.
**Prerequisite mode.** STANDBY-MAINT-COOLANT.

**Steps.**

1. Verify preconditions.
2. Energize `DO-MIV-S-OPEN` and `DO-MIV-R-OPEN`; verify both valves at open limit.
3. Mechanically restrain both MIVs in the open position (physical blocking tool on the valve body; LOTO-controlled) so that they cannot spring-closed when DO is de-energized. This is the simulated dual-fail condition.
4. Command DO-MIV-S-OPEN = 0 and DO-MIV-R-OPEN = 0 via BMS maintenance override. Record t₀.
5. Verify ZS-MIV-S-CLOSED does not assert within 10 s (valve restrained); same for ZS-MIV-R-CLOSED.
6. Wait 30 s. Verify MIV-DUAL-FAIL CRITICAL raised at t₀ + 30 s.
7. Verify `OT-MODE-CURRENT` = "SAFE-STATE" with manual-dispatch flag.

**Pass/fail criteria.** CRITICAL raised at 30 s TTA; mode tag transitions to SAFE-STATE.

**Restoration.** Remove mechanical restraints; verify valves spring to closed (ZS-*-CLOSED asserted); §6.4 reset.

### PT-SIF-13 — Single-zone leak protective function

**SIF covered.** SIF-13 (not SIL-rated — protective, not SIS).
**Test interval.** Covered by PT-SIF-07 (dual-zone proof-test exercises the single-zone path at step 3).
**Note.** No separate procedure. Retained here for numbering completeness.

### PT-SIF-14 — Hardware watchdog trip

**SIF covered.** SIF-14.
**Test interval.** 6-month.
**Prerequisite mode.** STANDBY-MAINT-GENERAL. Mandatory coordination with platform NOC — the Jetson is going to appear to crash.

**Steps.**

1. Verify preconditions; notify platform NOC of planned watchdog test; confirm DO-WL-ENABLE = 0.
2. Stop the `adc-bms.service` heartbeat worker without stopping the rest of the application, so that the hardware watchdog heartbeat pulse ceases but the Jetson itself remains running and able to observe. (Alternative: simulate heartbeat loss by physical disconnection of the heartbeat wire pair at the terminal block — LOTO-controlled.) Record t₀.
3. Verify within 2 s of t₀: BMS raises JETSON-HB-MISS WARN (internal check at 2 s per CTRL-001 §6.2).
4. Verify within 5 s of t₀: hardware watchdog relay opens NC contact. Measurable results:
   - DO-HW-SAFE-STATE-LATCH contact opens at CDU skid safe-state input (confirmed at CDU skid diagnostics)
   - 24 VDC removed from S04 DO card; DO-MIV-S-OPEN, DO-MIV-R-OPEN, DO-WL-ENABLE, DO-FIRE-RELEASE all de-energized
   - MIVs spring-close within 15 s (ZS-MIV-*-CLOSED assert)
5. Verify `DO-FIRE-ARM` on its separate circuit is in the state it held prior (should be de-energized = armed, consistent with STANDBY-MAINT-GENERAL entry protocol for this test — MAINT-GENERAL normally energizes DO-FIRE-ARM, so the operator must de-energize it before starting the test per MODES-001 §6.2 safe posture).
6. Verify WATCHDOG-TRIPPED CRITICAL published (BMS may or may not publish this depending on whether the Jetson itself is still alive; for this test, Jetson is alive, so the mode publish occurs).

**Pass/fail criteria.** Watchdog trips at 5 s ± 0.5 s; S04 DO card power removed; CDU safe-state latch opens; MIVs close; fire-arm DO unchanged on its separate rail.

**Restoration.** Reset hardware watchdog relay per its manufacturer procedure (physical reset button on the DIN-rail unit, ECP panel access required). Restart `adc-bms.service` heartbeat worker. Verify heartbeat restored. Verify watchdog re-armed (NC contact closed). Jetson cold-boot path per MODES-001 §14 if the restart required full reboot — observe INIT → STANDBY-IDLE.

---

## 7. Bypass and inhibit management

Per position SIS-08.

### 7.1 Rules

1. **Authentication.** Every bypass requires an authenticated platform NOC OPC-UA operator command using method `sis-bypass-request` at OPC-UA path `adc.cassette.<serial>.sis.bypass-request`. Per Cassette-CYBER-001 §6.3, the authenticated role required is `platform`.
2. **Maximum duration.** A bypass window is maximum 4 h. The BMS records the granted duration and auto-restores the SIF at expiry without operator action.
3. **Logging.** WARN-level log entry at `/var/log/bms/alarms.jsonl` and platform historian, including: operator identity, SIF ID, requested duration, timestamp start, and (on restore) actual restore timestamp.
4. **One at a time.** Only one SIF may be bypassed in any overlapping window. A second `sis-bypass-request` while another is active is rejected with error code `SIS_BYPASS_CONFLICT`; the operator sees the currently bypassed SIF ID in the error response.
5. **Workload inactive prerequisite.** `DO-WL-ENABLE` must be 0 at the moment the bypass is requested. If workload is active, the request is rejected with error code `SIS_BYPASS_WORKLOAD_ACTIVE`; the operator must first stop workload before bypassing.

**Explicitly not a SIS bypass:** The `DO-FIRE-ARM` maintenance-inhibit relay that is energized during STANDBY-MAINT-GENERAL and STANDBY-MAINT-COOLANT per MODES-001 §6 is a mode-logic feature, not a SIS bypass. It does not count against the one-at-a-time limit; it is not recorded in the bypass log; it has its own round-trip verification path (FIRE-DI-2 handshake per FIRE-001 §8.5).

### 7.2 Bypass log schema

Every bypass event is recorded with the following fields:

| Field | Type | Notes |
|---|---|---|
| `sif_id` | string | One of `SIF-01` through `SIF-14` |
| `operator_id` | string | Authenticated platform OPC-UA user identity (CYBER-001 user cert subject CN) |
| `timestamp_start` | ISO-8601 | When bypass granted |
| `requested_duration_seconds` | integer | ≤ 14,400 (4 h) |
| `actual_restore_timestamp` | ISO-8601 | Set on auto-restore or manual revoke |
| `opc_ua_method` | string | Fixed: `adc.cassette.<serial>.sis.bypass-request` |
| `restore_reason` | enum | `expiry` (auto), `manual-revoke`, `workload-request-blocked` |

### 7.3 SIF-specific bypass notes

- **SIF-01 (fire)** — bypass is **not permitted** under any circumstance. The Ansul panel layer cannot be bypassed by this mechanism; DO-FIRE-ARM via maintenance mode is the only permitted fire-response modification, and it inhibits only the panel's discharge logic. The BMS-side response to FIRE-DI-1 assertion cannot be bypassed.
- **SIF-11 (E-stop hardware)** — cannot be bypassed from software; the shunt-trip path is hardwired and has no software disable.
- **SIF-14 (watchdog)** — cannot be bypassed from software; the heartbeat requirement is hardware-enforced.
- **SIF-02 through SIF-10, SIF-12** — bypass permitted per §7.1 rules for proof-test execution and controlled maintenance. Only one at a time.

---

## 8. Common cause failure analysis

Per position SIS-09.

| CCF Scenario | Affected SIFs | Mitigation | Residual risk statement |
|---|---|---|---|
| **CCF-1** — BMS software fault or Jetson OS crash | SIF-01 through SIF-13 | SIF-14 hardware watchdog independent of software; NFPA 72-certified Ansul panel covers SIF-01 detection and release autonomously | Accepted. If the watchdog itself is also dormantly failed, all software SIFs are undetected; watchdog proof-test every 6 months reduces dormant-failure window. |
| **CCF-2** — 24 VDC UPS failure | SIF-01 through SIF-14 (power to logic solvers and I/O bus) | BMS loses power; all DO outputs de-energize to safe state by fail-safe wiring design; DI-UPS-OK monitoring and UPS-FAULT-A alarm per CTRL-001 §6.2 | Accepted. UPS failure is a fail-safe failure mode because every final element is fail-closed or fail-de-energized. |
| **CCF-3** — Modbus TCP link failure to CDU skid | SIF-02 (FT-102), SIF-03 (TT-103), SIF-04 (TT-104), SIF-05/SIF-06 (PT-101), SIF-09 (STS-PUMP-RUN) | CDU-COMMS-LOST ALARM drives DEGRADED; hardwired STS-PUMP-RUN-DI fallback on S03 per TAGS-001 §3.2 provides alternate detection for SIF-09; TT-INT and AT-INT-RH on S05 provide coarse cassette-interior thermal trend independent of CDU | Significant. Modbus link failure blinds the BMS to primary process variables. Mitigation is the S03 fallback plus DEGRADED-level awareness. A prolonged outage with active workload is addressed by SIF-10 (power-loss-extended) only if AC loss is also present. SIS-01 LOPA should evaluate whether a persistent Modbus outage (without AC loss) warrants an additional SIF. |
| **CCF-4** — Single TraceTek zone fault masking a wet event | SIF-07, SIF-13 | TK-ZA-FAULT or TK-ZB-FAULT generates WARN per CTRL-001 §6.2; dual-zone independent physical routing ensures that a single cable fault does not affect the other zone; proof-test PT-SIF-07 exercises both zones individually | Accepted. A simultaneous wet event in a zone with an active FAULT is partially detected (the other zone still detects); dual FAULT concealing dual WET is a residual risk covered by periodic proof-test. |
| **CCF-5** — S04 DO card failure | SIF-01 through SIF-12 (final elements DO-WL-ENABLE, DO-MIV-S-OPEN, DO-MIV-R-OPEN, DO-FIRE-ARM, DO-FIRE-RELEASE) | S04 card failure de-energizes all card outputs simultaneously, which is the safe-state direction for every output (workload off, MIVs closed, fire panel armed, remote release not asserted) | Fail-safe failure mode, not a dangerous failure. No additional mitigation required. |
| **CCF-6** — Shared ECP panel enclosure for BMS and I/O | SIF-01 through SIF-14 | Fire inside the ECP panel could disable the logic solver; mitigated by (a) the hardware watchdog relay physically located on the DIN rail with a separate fuse, physically separated from the BMS I/O bus power (CTRL-001 §2.2), and (b) the Ansul panel operating independently with its own 120 V AC + 24 h battery outside the ECP panel | Accepted at SL 1. A fire that simultaneously destroys the BMS, the hardware watchdog, and the Ansul panel is beyond the design basis. The Ansul panel's location outside the ECP panel provides the primary independence. |

---

## 9. Diagnostic coverage

| SIF ID | Automated diagnostic in BMS scan loop | Diagnostic coverage (qualitative) | Proof-test only | Notes |
|---|---|:-:|:-:|---|
| SIF-01 | FIRE-DI-1 loop supervision (loop open → fail-safe toward alarm); FIRE-DI-3 fault DI continuously monitored | High | Partial (full cross-zone verification in PT-SIF-01) | Loop supervision detects cable cuts; panel-side diagnostics are the Ansul panel's domain |
| SIF-02 | CDU-COMMS-LOST ALARM on Modbus timeout; FT-102 reading against expected range at known flow state | Medium | Partial | Sensor stuck-at-value is dangerous failure; partial mitigation from TT-103/TT-104 correlation |
| SIF-03 | Same as SIF-02 for Modbus link; TT-103 range check | Medium | Partial | Dangerous failure mode from sensor stuck-low not fully diagnosed; partial mitigation from TT-INT interior correlation |
| SIF-04 | Same as SIF-03 with TT-104 | Medium | Partial | Similar to SIF-03 |
| SIF-05 | Same Modbus diagnostic; PT-101 range check | Medium | Partial | Stuck-high is spurious-trip (safe); stuck-low is dangerous for SIF-05 |
| SIF-06 | Same as SIF-05 | Medium | Partial | Stuck-high is dangerous for SIF-06 (low-low detection) |
| SIF-07 | TK-ZA-FAULT and TK-ZB-FAULT DIs continuously monitored | Medium | Partial | Fault DI catches cable open; intermittent wet cable may not be caught until proof-test |
| SIF-08 | Float switch wiring continuity (loop supervision on S02 DI loop) | Medium | Partial | Stuck-float is a mechanical dormant failure detected by proof-test only |
| SIF-09 | CDU-COMMS-LOST; CDU-PUMP-FAULT ALARM from skid-side diagnostics | Medium | Partial | Hardwired STS-PUMP-RUN-DI on S03 is independent diagnostic |
| SIF-10 | DI-POWER-OK continuously monitored; DI-UPS-OK continuously monitored | High | Partial | UPS depletion prediction is not automated in Rev 1.2 — BMS waits for DI-UPS-OK to deassert |
| SIF-11 | DI-ESTOP continuously monitored; ELEC-001 shunt-trip aux contact continuously monitored | High | Partial | Button dormant failure (pressed but not tripping) is dangerous; proof-test coverage is executive (physical press) |
| SIF-12 | ZS-MIV-*-OPEN and ZS-MIV-*-CLOSED continuously monitored; command/feedback mismatch WARN at 10 s | High | Partial | Single-valve mismatch caught at 10 s WARN; dual-fail is the SIF condition at 30 s CRITICAL |
| SIF-13 | TK-ZA-WET and TK-ZB-WET continuously monitored | High | None | Protective function; single-zone wet is itself the diagnostic for developing dual-zone |
| SIF-14 | JETSON-HB-MISS WARN at 2 s (continuously monitored internally by BMS application supervisor) | High | Partial | Software-side diagnostic precedes hardware-side trip at 5 s; full hardware trip verified in PT-SIF-14 |

**Note on the JETSON-HB-MISS diagnostic.** Per CTRL-001 §6.2, the BMS application supervisor raises JETSON-HB-MISS WARN at 2 s if the heartbeat worker misses a pulse cycle. This is a software-side self-diagnostic that precedes the hardware watchdog's 5 s trip. The WARN is published to NOC for awareness; if the condition resolves within 3 s (before the 5 s hardware threshold), the watchdog does not trip and the system recovers. Persistent WARN for 3 s leads to WATCHDOG-TRIPPED CRITICAL when the hardware relay opens.

---

## 10. Demand mode vs continuous mode

Per IEC 61511-1 §9.2, SIFs are classified as low-demand (< 1 demand per year) or continuous/high-demand (≥ 1 demand per year).

| SIF ID | Mode | Basis |
|---|---|---|
| SIF-01 | Low-demand | Fire is a rare event; multiple Cassette-years of operation expected between demands |
| SIF-02 | Low-demand | Coolant flow loss during production is rare; design basis < 1 event per Cassette-year |
| SIF-03 | Low-demand | Supply T high-high requires a skid-side failure; rare |
| SIF-04 | Low-demand | Return T high-high; rare |
| SIF-05 | Low-demand | Pressure high-high; rare |
| SIF-06 | Low-demand | Pressure low-low; rare |
| SIF-07 | Low-demand | Dual-zone leak; rare |
| SIF-08 | Low-demand | Sump HIHI; rare |
| SIF-09 | Low-demand | Pumps all-off during active workload; rare |
| SIF-10 | Low-demand | Extended AC loss during workload; rare |
| **SIF-11** | **Continuous mode** | E-stop is available for demand at any moment; per IEC 61511, operator-demand safety functions are continuous mode because the demand rate is bounded only by operator decision |
| SIF-12 | Low-demand | MIV dual-fail only manifests on a safe-state entry; demand follows triggering SIF |
| SIF-13 | N/A | Not SIL-rated; protective function |
| **SIF-14** | **Continuous mode** | The watchdog is continuously evaluating the heartbeat; demand is every cycle |

**Implications:**

- **Low-demand SIFs** are characterized by PFDavg (Probability of Failure on Demand, average). Quantitative PFDavg calculation is open item SIS-08.
- **Continuous-mode SIFs (SIF-11, SIF-14)** are characterized by PFH (Probability of dangerous Failure per Hour). Quantitative PFH calculation is gated on SIS-04 (watchdog relay datasheet) and SIS-08 (general calculation framework).

The SIL 1 interim claim for low-demand SIFs corresponds to PFDavg in the range 10⁻² ≤ PFDavg < 10⁻¹ per IEC 61508 Table 2.

The SIL 2 interim claim for continuous SIF-11 and SIF-14 corresponds to PFH in the range 10⁻⁷ ≤ PFH < 10⁻⁶ per IEC 61508 Table 3. The SIL 2 architectural claim is conditional on SIS-04 datasheet confirming this range; if the selected watchdog relay cannot substantiate SIL 2, the SIL target reduces to SIL 1 and the claim is updated in Rev 1.3.

---

## 11. Commissioning verification

Per position SIS-07 and cross-referencing Cassette-CTRL-001 §14 commissioning.

| Test ID | SIF covered | Method | Cross-reference | Counts as first proof-test? |
|---|---|---|---|:-:|
| V-SIS-01 | SIF-01 | Execute PT-SIF-01 at commissioning | Cassette-CTRL-001 §14 item 22; Cassette-FIRE-001 §12.2 SP-10 | Yes |
| V-SIS-02 | SIF-02 | Execute PT-SIF-02 with CDU skid cooperation during wet commissioning | Cassette-CTRL-001 §14 item 12 | Yes |
| V-SIS-03 | SIF-03 | Execute PT-SIF-03 | Cassette-CTRL-001 §14 item 12 | Yes |
| V-SIS-04 | SIF-04 | Execute PT-SIF-04 | Cassette-CTRL-001 §14 item 12 | Yes |
| V-SIS-05 | SIF-05 | Execute PT-SIF-05 | Cassette-CTRL-001 §14 item 12 | Yes |
| V-SIS-06 | SIF-06 | Execute PT-SIF-06 | Cassette-CTRL-001 §14 item 12 | Yes |
| V-SIS-07 | SIF-07 | Execute PT-SIF-07 | Cassette-CTRL-001 §14 item 14 | Yes (also covers SIF-13) |
| V-SIS-08 | SIF-08 | Execute PT-SIF-08 | Cassette-CTRL-001 §14 item 14 | Yes |
| V-SIS-09 | SIF-09 | Execute PT-SIF-09 with CDU skid cooperation | Cassette-CTRL-001 §14 item 12 | Yes |
| V-SIS-10 | SIF-10 | Execute PT-SIF-10 | Cassette-CTRL-001 §14 item 19 | Yes |
| V-SIS-11 | SIF-11 | Execute PT-SIF-11; physical E-stop press coordinated with ELEC-001 | Cassette-CTRL-001 §14 item 19; Cassette-ELEC-001 §6 | Yes |
| V-SIS-12 | SIF-12 | Execute PT-SIF-12 with mechanical valve restraint | Cassette-CTRL-001 §14 item 13 | Yes |
| V-SIS-13 | SIF-13 | Covered by V-SIS-07 | Cassette-CTRL-001 §14 item 14 | N/A (protective function) |
| V-SIS-14 | SIF-14 | Execute PT-SIF-14 with controlled heartbeat interruption | Cassette-CTRL-001 §14 item 17 | Yes |

**First proof-test credit.** Per IEC 61511 common practice, if the commissioning test is executed against the same procedure as the periodic proof-test and all pass/fail criteria are met, it counts as the first proof-test cycle. The proof-test interval clock starts at the commissioning date; the next proof-test is due 6 months (SIF-01, SIF-11, SIF-14) or 12 months (all other SIFs) from that date.

**Proof-test record storage.** First-cycle records from commissioning are stored in the proof-test record system per SIS-03. The record format and storage path (`/var/bms/proof-test/<date>_<sif_id>.json` plus platform historian archival) is established before commissioning begins.

---

## 12. Integration with MODES-001

Per position SIS-03 and MODES-001 §11.

### 12.1 SIF-demanded mode transitions

Every SIF demand results in a mode transition. Per MODES-001 §11:

- ALARM-level alarms (CTRL-001 §6.2) cause PRODUCTION → DEGRADED. These are **not** SIF demands. DEGRADED is a controlled workload-throttle response, not a safe state.
- CRITICAL-level alarms (CTRL-001 §6.2) from SIF initiators cause any operating mode → SAFE-STATE (or E-STOP for SIF-11). These **are** SIF demands.

| SIF demand | MODES-001 transition | Logged as SIF demand event |
|---|---|:-:|
| SIF-01 | Any → SAFE-STATE, fire_event = true | Yes |
| SIF-02 | Any → SAFE-STATE | Yes |
| SIF-03 | Any → SAFE-STATE | Yes |
| SIF-04 | Any → SAFE-STATE | Yes |
| SIF-05 | Any → SAFE-STATE | Yes |
| SIF-06 | Any → SAFE-STATE | Yes |
| SIF-07 | Any → SAFE-STATE | Yes |
| SIF-08 | Any → SAFE-STATE | Yes |
| SIF-09 | Any → SAFE-STATE | Yes |
| SIF-10 | Any → SAFE-STATE | Yes |
| SIF-11 | Any → E-STOP | Yes |
| SIF-12 | Any → SAFE-STATE (with manual-dispatch flag) | Yes |
| SIF-13 | PRODUCTION → DEGRADED | **No** — protective, not SIF |
| SIF-14 | Any → SAFE-STATE (via hardware) | Yes |

### 12.2 Operator-initiated transitions are not SIF demands

The following MODES-001 operator commands result in mode transitions that are **not** SIF demands:

- `start-cooling` (STANDBY → READY)
- `workload-enable-request` (READY → PRODUCTION)
- `stop-workload` (PRODUCTION → READY)
- `stop-cooling` (READY → STANDBY)
- `enter-maintenance-general` / `enter-maintenance-coolant` / `exit-maintenance`
- `safe-state-reset` (SAFE-STATE → STANDBY; this is the recovery from a SIF demand, not a new demand)
- `e-stop-acknowledge` (E-STOP → STANDBY; recovery)

These transitions are logged in `adc.cassette.<serial>.mode.history` with the triggering operator command. They do not consume proof-test credit and are not counted against SIS demand statistics.

### 12.3 Proof-test execution mode

Proof-tests may be executed in STANDBY-MAINT-GENERAL or STANDBY-MAINT-COOLANT only (per SIS-07). The mode must persist for the full duration of the test. If the Cassette exits the maintenance sub-state during a proof-test (for example, unexpected operator command or automatic exit on timeout), the proof-test is invalidated and must be restarted.

### 12.4 DEGRADED is not a SIS state

DEGRADED (MODES-001 §7) is a controlled response to ALARM-level conditions under active workload. It is achieved by publishing a workload-throttle-request to the platform NOC; the BMS does not autonomously reduce workload. DEGRADED is **explicitly not a SIF-demanded state** because:

- No final element is forced to its safe value (DO-WL-ENABLE remains 1, MIVs remain open, pumps continue running)
- The trip is advisory to the platform, not automatic
- Escalation from DEGRADED to SAFE-STATE on a subsequent CRITICAL is the SIF demand event, not the DEGRADED entry itself

This distinction matters for proof-test accounting — the DEGRADED response path is exercised by alarm-engine testing per CTRL-001 §14, not by SIS proof-tests.

---

## 13. Modification control

Per IEC 61511-1 §17.

### 13.1 Modification categories requiring SIF re-validation

Any modification falling into the following categories requires re-validation of the affected SIF(s) before the modification is placed into service:

| Category | Affected elements | Required re-validation |
|---|---|---|
| **Initiator wiring change** | Any change to the physical wiring of an initiator tag (FIRE-DI-*, FT-102, TT-103, TT-104, PT-101, STS-PUMP-RUN, TK-*, LT-SUMP-HIHI, DI-ESTOP, DI-POWER-OK) | Execute the corresponding PT-SIF-NN procedure after modification; update as-built terminal schedule |
| **Logic solver software change** | Any `adc-bms` release that touches alarm evaluation (`alarm-engine` worker), mode transition logic (`mode-controller` worker), or DO output logic (`io-scanner` worker, `miv-controller` worker); any change to `/etc/adc-bms/config.yaml` alarm table or SIF thresholds | Execute all PT-SIF-NN procedures for SIFs whose logic path touches the changed code; version-control record |
| **Final element wiring change** | Any change to DO-WL-ENABLE, DO-MIV-S-OPEN, DO-MIV-R-OPEN, CMD-PUMP-ENABLE (Modbus register address change), DO-FIRE-ARM, DO-FIRE-RELEASE, or the hardware watchdog relay wiring | Execute PT-SIF-NN for every SIF whose final-element list includes the changed output |
| **SIF bypass timeout change** | Change to the 4 h maximum bypass duration in §7.1 | Requires Rev 1.3+ issuance of this document; platform OPC-UA method signature update |
| **Proof-test interval change** | Change to 6-month or 12-month intervals in §6 | Requires Rev 1.3+ issuance; re-approval by FSA if FSA has been completed |
| **Tag addition/removal** | Any tag added to or removed from TAGS-001 that is a SIF initiator or final element | SIS-001 revision + corresponding PT-SIF-NN procedure update |

### 13.2 Change control process (summary)

For each modification:

1. Record the proposed change in a platform modification request ticket
2. Identify affected SIFs from the tables above
3. Author or update re-validation procedure if needed
4. Execute re-validation during a planned maintenance window in STANDBY-MAINT-*
5. Log re-validation results to proof-test record system (SIS-03)
6. If modification is a logic solver software change, platform code review per CYBER-001 §12.4 is also required
7. Sign-off by Scott Tomsu + platform safety lead before the modification is placed into service

### 13.3 Modifications during commissioning

Modifications made during the commissioning period (before the first proof-test cycle completes) require a revision of this document (e.g., Rev 1.2 → Rev 1.2.1) to reflect the as-built state before commissioning is closed and the Cassette enters production. No commissioning sign-off is issued against an out-of-date SIS-001.

---

## 14. Open items

| ID | Priority | Description | Blocks |
|---|---|---|---|
| SIS-01 | C1 | LOPA — perform layer of protection analysis for each SIF; confirm SIL 1 interim assignment or identify SIFs requiring SIL 2; consequence severity and initiating event frequency inputs from Cassette-CTRL-001 §6.2 alarm history post-commissioning; output feeds SIS-001 Rev 1.3 | FSA per IEC 61511-1 §5.6; SIS-001 Rev 1.3 |
| SIS-02 | C1 | Logic solver qualification — obtain or produce Cassette BMS (Jetson Orin NX + DIN-rail I/O hardware) IEC 61508 / IEC 61511 qualification documentation; if hardware is not IEC 61508 certified, document architectural constraints per IEC 61511-1 §11.5 and confirm SIL 1 capability | FSA; LOPA (SIS-01 uses logic solver SIL claim as a LOPA input) |
| SIS-03 | C1 | Proof-test record system — establish proof-test record format and storage (local NVMe at `/var/bms/proof-test/` + platform historian); define mandatory fields (SIF ID, test date, operator, pass/fail, anomalies, as-left state); first records from commissioning must be logged before SIS-001 Rev 1.3 | FSA; IEC 61511-1 §16 compliance (proof-test documentation) |
| SIS-04 | C1 | Hardware watchdog relay SIL datasheet and PFDavg — obtain IEC 61508 SIL 2 certification datasheet for the selected relay; calculate PFDavg at 6-month proof-test interval; confirm SIL 2 architectural claim for SIF-14 | SIF-14 SIL claim; §10 continuous-mode PFH calculation |
| SIS-05 | C2 | PST thermal confirmation — perform thermal model or controlled test at maximum GPU load to confirm PST ≥ 60 s for SIF-02, SIF-03, SIF-04; if actual PST < 60 s, reduce ALARM → SAFE-STATE TTA in Cassette-CTRL-001 §6.2 and revise this document | SIF-02/03/04 PST validity; Rev 1.3 |
| SIS-06 | C2 | LOTO alignment — align §6 proof-test procedures with Cassette-ELEC-001 LOTO procedure; confirm all proof-tests are executable in STANDBY-MAINT-* without live-load condition; identify any SIF requiring active coolant flow to proof-test (SIF-02 flow-loss test may require pump running at low flow to simulate FLOW-LO-C trigger); document any LOTO-exception requests | Proof-test executability; OSHA 29 CFR 1910.147 compliance |
| SIS-07 | C2 | Single-zone to dual-zone escalation verification — confirm BMS alarm engine correctly escalates TRACETEK-ZA-WET-A (ALARM, DEGRADED) to TRACETEK-DUAL-WET-C (CRITICAL, SAFE-STATE) within the PST of SIF-07 (300 s) when the second zone asserts; verify in software code review and in commissioning test V-SIS-07 | SIF-07 functional correctness; PT-SIF-07 pass criterion |
| SIS-08 | C3 | Quantitative PFDavg calculation — after LOPA (SIS-01) and logic solver qualification (SIS-02) complete, calculate PFDavg for each low-demand SIF and PFH for SIF-11 and SIF-14 using instrument failure-rate data from Cassette-TAGS-001 manufacturer datasheets; target PFDavg ≤ 0.1 for SIL 1 SIFs (10-year demand basis) | Quantitative SIL verification; Rev 1.3 FSA closure |

---

## Document control

**Cassette-SIS-001 — Rev 1.2 — CONFIDENTIAL**
**Prepared by:** Scott Tomsu · CEO / Chief Engineer · scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana
**Companion to:** Cassette-CTRL-001 · Cassette-FIRE-001 · Cassette-ELEC-001 · Cassette-COOL-001 · Cassette-MODES-001 · Cassette-TAGS-001 · Cassette-CYBER-001 · Cassette-ECP-001
**Supersedes:** Cassette-SIS-001 Rev 1.1 (deleted)
**Authority scope:** the Safety Instrumented System for one Cassette — the 14-row SIF register, SIL targets (SIL 1 interim for BMS-software SIFs; SIL 2 architectural for SIF-11 and SIF-14), process safety times, proof-test intervals and procedures, bypass and inhibit rules, common-cause failure analysis, diagnostic coverage, demand-mode classification, commissioning verification, and modification control.

Every tag ID in this document matches Cassette-TAGS-001 Rev 1.2 exactly. Every alarm ID matches Cassette-CTRL-001 §6.2 exactly. Every SIF that drives MODES-001 SAFE-STATE is listed here; every MODES-001 → SAFE-STATE transition corresponds to a SIF row in §4.

Rev 1.2 is the design-basis document. A full FSA per IEC 61511-1 §5.6 is gated on closure of SIS-01 through SIS-04 and will be documented in Rev 1.3.

**End of Cassette-SIS-001 Rev 1.2.**
