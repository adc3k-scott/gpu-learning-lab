# Cassette-MODES-001 — Cassette Operating Modes Specification — Rev 1.2

**Document ID:** Cassette-MODES-001
**Revision:** 1.2
**Date:** 2026-04-22
**Classification:** CONFIDENTIAL
**Supersedes:** Rev 1.1 (deleted) — full clean rebuild
**Companion documents:** Cassette-CTRL-001 · Cassette-FIRE-001 · Cassette-ELEC-001 · Cassette-COOL-001 · Cassette-COOL2-001 · Cassette-BOM-001
**Prepared by:** Scott Tomsu · CEO / Chief Engineer · scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana

---

## Revision log

| Rev | Date | Author | Summary |
|---|---|---|---|
| 1.0 | 2026-01-xx | Scott Tomsu | First issue. Four-mode sketch (OFF / COOLING / RUNNING / FAULT). Superseded. |
| 1.1 | 2026-02-xx | Scott Tomsu | Withdrawn and deleted — mode definitions were inconsistent with CTRL-001 safe-state posture and predated the FIRE-001 hardwired Munters interlock decision. |
| **1.2** | **2026-04-22** | **Scott Tomsu** | **Full rebuild against CTRL-001 Rev 1.2 and FIRE-001 Rev 1.2. Seven-mode state machine locked (INIT, STANDBY, READY, PRODUCTION, DEGRADED, SAFE-STATE, E-STOP). MAINTENANCE locked as sub-state of STANDBY. Fire event locked as an entry path into SAFE-STATE with a `fire_event` flag, not a separate top-level mode. DEGRADED bounded. Recovery paths locked for all three recovery scenarios. Mode OPC-UA tag schema locked. Mode persistence across power cycles locked (cold start always INIT→STANDBY).** |

---

## 1. Scope

This document specifies the **operating mode state machine** for one ADC 3K Cassette. It defines the seven modes the Cassette can be in, the subsystem state for each mode, the transition conditions between modes, the recovery paths out of safety-related modes, the OPC-UA surface for mode publication and operator-initiated transitions, and the per-mode commissioning verification procedure.

**What MODES-001 owns:**

- The seven-mode state machine (§2–§4)
- Per-mode subsystem state tables — what CDU pumps, MIVs, workload-enable, Munters, fire panel arm state, 480 V AC, and BMS itself are doing in each mode
- INIT self-test sequence and failure handling (§5)
- STANDBY sub-states including maintenance and fire-recovery variants (§6)
- DEGRADED mode entry/exit logic and the workload-throttle-request severity mapping (§7)
- The distinction between fire-origin and non-fire-origin SAFE-STATE (§8)
- Recovery paths out of SAFE-STATE and E-STOP (§9)
- The `mode.current` and `mode.history` OPC-UA tags (§10)
- How the alarm hierarchy maps to mode effects (§11)
- Mode-transition commissioning verification (§12)
- Platform NOC interface for operator-initiated transitions (§13)
- Mode persistence across power cycles (§14)

**What MODES-001 defers:**

- The alarm table itself (what conditions raise INFO / WARN / ALARM / CRITICAL) → CTRL-001 §6.2. MODES-001 consumes alarm levels; it does not define them.
- The literal step-by-step execution of the seven-step safe-state sequence → CTRL-001 §6.3. MODES-001 states the resulting mode; CTRL-001 states the actions.
- The MIV closure trigger matrix → CTRL-001 §7.2
- The CDU skid Modbus register map → CTRL-001 §8
- Fire panel terminal wiring, fire panel release authority, the Ansul panel's internal countdown logic → FIRE-001
- 480 V AC shunt trip circuit and E-stop pushbutton wiring → ELEC-001 §6
- The hardwired Munters-off-on-fire interlock schematic → FIRE-001 §9.1

---

## 2. Mode definitions

Seven modes. Every Cassette, at every moment, is in exactly one of these. See §12 for priority resolution when multiple conditions would drive different modes.

Subsystem state table columns, used in every §2.x mode:

- **CDU pumps** — commanded state over Modbus to CDU skid PLC (RUN / STOP)
- **MIV-S** — supply isolation valve position (OPEN / CLOSED)
- **MIV-R** — return isolation valve position (OPEN / CLOSED)
- **Workload-enable** — the 24 VDC DO driving the platform-side workload-enable relay (ENERGIZED / DE-ENERGIZED)
- **Munters** — the DSS Pro dehumidification skid (RUN / STOP / HARDWARE-CONTROLLED)
- **Fire panel arm state** — the Ansul panel's arm/inhibit state as seen by the BMS via DO-FIRE-ARM (ARMED / INHIBITED / HARDWARE-CONTROLLED)
- **480 V AC** — the main Cassette AC feed (PRESENT / ABSENT)
- **BMS** — the BMS application itself (BOOTING / RUNNING / HELD)

"HARDWARE-CONTROLLED" means the state is not driven from BMS software in that mode — a separate physical interlock owns it.

### 2.1 INIT

**Purpose.** Power-on self-test. The BMS proves it is healthy before being allowed to command anything.

**Entry conditions.** Jetson power-on (either cold start from 480 V AC restoration, or planned BMS restart from a platform maintenance command).

**Exit conditions.**

- Success → STANDBY, within 120 s maximum on a healthy system (§5 defines the step checklist)
- Failure → INIT-FAULT latched in INIT; publish fault reason to HMI and OPC-UA; hold here until manual intervention

**Subsystem state during INIT.**

| Subsystem | State |
|---|---|
| CDU pumps | STOP (Modbus not yet up — skid continues whatever it was doing; skid defaults to its own standby) |
| MIV-S | CLOSED (DO de-energized at boot — actuators are spring-return fail-closed) |
| MIV-R | CLOSED (same) |
| Workload-enable | DE-ENERGIZED (DO defaults off at boot) |
| Munters | RUN (Munters is on its own starter, independent of BMS boot state; humidity control is continuous) |
| Fire panel arm state | ARMED (DO-FIRE-ARM de-energized at boot — fail-safe toward arming per FIRE-001 §8.5) |
| 480 V AC | PRESENT |
| BMS | BOOTING |

### 2.2 STANDBY

**Purpose.** BMS healthy, Cassette physically safe, no workload, no coolant circulating. The resting state the Cassette can occupy indefinitely with no operator intervention.

**Entry conditions.**

- INIT completes successfully
- SAFE-STATE (non-fire) reset per CTRL-001 §6.4 completes → directly to STANDBY
- SAFE-STATE (fire-origin) recovery completes all five gates (§9.2) → proceeds through STANDBY-FIRE-RECOVERY, then to STANDBY
- E-STOP recovery: 480 V AC restored and POWER-OK DI asserts → STANDBY
- Platform NOC commands a planned stop-cooling from PRODUCTION or READY → STANDBY

**Exit conditions.**

- Platform NOC issues `start-cooling` OPC-UA command → transition to READY
- Platform NOC issues `enter-maintenance-general` or `enter-maintenance-coolant` → transition to STANDBY-MAINT-* sub-state (see §6)
- Any CRITICAL alarm → SAFE-STATE (with `fire_event` flag set if source is FIRE-TRIGGERED)
- E-stop assertion → E-STOP
- Unexpected 480 V AC loss > 5 min → SAFE-STATE with POWER-LOSS-EXT trigger (CTRL-001 §6.2)

**Subsystem state during STANDBY.**

| Subsystem | State |
|---|---|
| CDU pumps | STOP (CMD-PUMP-ENABLE = 0 via Modbus, CTRL-001 §8.3) |
| MIV-S | CLOSED |
| MIV-R | CLOSED |
| Workload-enable | DE-ENERGIZED |
| Munters | RUN (humidity control continuous) |
| Fire panel arm state | ARMED (DO-FIRE-ARM de-energized) |
| 480 V AC | PRESENT |
| BMS | RUNNING |

### 2.3 READY

**Purpose.** Cooling is running and stable. Cassette is waiting for workload-enable authorization from platform NOC.

**Entry conditions.**

- STANDBY + `start-cooling` command received + BMS has issued MIV-open commands and CDU pump-enable

**Exit conditions.**

- All four gates satisfied (§M7) and `workload-enable-request` received → PRODUCTION
- Any four-gate check fails within 120 s of the start-cooling command → hold in READY, raise WARN; operator decision
- Platform NOC issues `stop-cooling` → STANDBY (MIVs close, pumps stop)
- Any ALARM condition → remain in READY, publish alarm to NOC (no mode change for ALARM while workload is not yet asserted)
- Any CRITICAL alarm → SAFE-STATE
- E-stop → E-STOP

**Four gates for READY → PRODUCTION transition** (per M7):

1. MIV-S limit switch = OPEN **and** MIV-R limit switch = OPEN (ZS-MIV-S-OPEN, ZS-MIV-R-OPEN both asserted)
2. CDU secondary flow FT-102 ≥ 80 % of commissioned setpoint
3. CDU secondary supply temperature TT-103 ≤ 45 °C
4. No ALARM-level or CRITICAL-level alarms currently active

All four gates must be continuously satisfied for ≥ 10 s to prevent mode-chatter on marginal readings.

**Subsystem state during READY.**

| Subsystem | State |
|---|---|
| CDU pumps | RUN (CMD-PUMP-ENABLE = 1 via Modbus) |
| MIV-S | OPEN |
| MIV-R | OPEN |
| Workload-enable | DE-ENERGIZED (workload not yet asserted) |
| Munters | RUN |
| Fire panel arm state | ARMED |
| 480 V AC | PRESENT |
| BMS | RUNNING |

### 2.4 PRODUCTION

**Purpose.** Workload running at nominal. This is the steady-state operational mode of the Cassette.

**Entry conditions.**

- READY + all four gates continuously satisfied + `workload-enable-request` from platform NOC → BMS asserts workload-enable DO → PRODUCTION

**Exit conditions.**

- Any ALARM condition raised → DEGRADED (workload continues, throttle-request published)
- Any CRITICAL condition raised → SAFE-STATE (or E-STOP if source is E-stop)
- Platform NOC issues `stop-workload` → READY (workload-enable drops, cooling remains)
- Platform NOC issues `stop-cooling` or `enter-maintenance-*` → BMS first transitions to READY by dropping workload, then to STANDBY or STANDBY-MAINT-* per the operator request
- E-stop → E-STOP

**Subsystem state during PRODUCTION.**

| Subsystem | State |
|---|---|
| CDU pumps | RUN |
| MIV-S | OPEN |
| MIV-R | OPEN |
| Workload-enable | ENERGIZED |
| Munters | RUN |
| Fire panel arm state | ARMED |
| 480 V AC | PRESENT |
| BMS | RUNNING |

### 2.5 DEGRADED

**Purpose.** Workload continues but an ALARM-level condition is active; the BMS is asking the platform to reduce load and is watching for the condition to either clear or escalate to CRITICAL.

**Entry conditions.**

- PRODUCTION + any ALARM-level alarm active past its TTA and deadband

**Exit conditions.**

- All ALARM conditions clear past their deadbands → PRODUCTION
- Any CRITICAL alarm → SAFE-STATE
- Platform NOC issues `stop-workload` → READY (workload drops; cooling remains; BMS continues to work the alarm condition until clear)
- E-stop → E-STOP

**Workload-throttle-request severity mapping** — see §7 for the full mapping; in summary, thermal ALARMs (SUPPLY-T-HI-A, RETURN-T-HI-A, RACK-TEMP-HI escalated) map to severity 2 (hard reduce); humidity / pressure / flow ALARMs map to severity 1 (soft reduce); sump / TraceTek-drift / CDU-COMMS-LOST ALARMs map to severity 2 (proximate to CRITICAL escalation).

**Subsystem state during DEGRADED.** Identical to PRODUCTION by subsystem — the difference is the published mode tag, the active alarm set, and the workload-throttle-request severity:

| Subsystem | State |
|---|---|
| CDU pumps | RUN |
| MIV-S | OPEN |
| MIV-R | OPEN |
| Workload-enable | ENERGIZED |
| Munters | RUN |
| Fire panel arm state | ARMED |
| 480 V AC | PRESENT |
| BMS | RUNNING |

### 2.6 SAFE-STATE

**Purpose.** A CRITICAL event has occurred (or is suspected). The Cassette is physically held in a safe posture: no coolant circulating, no workload, fire suppression armed. 480 V AC remains present (that is the distinction from E-STOP per M1).

**Entry conditions.** Any active mode (STANDBY, READY, PRODUCTION, DEGRADED) + any CRITICAL alarm per CTRL-001 §6.2, or watchdog trip, or platform `maintenance-isolation` command. On entry, the BMS sets `fire_event = true` if the originating CRITICAL is FIRE-TRIGGERED (§8); otherwise `fire_event = false`.

**Exit conditions.**

- Non-fire-origin: CTRL-001 §6.4 reset sequence completes (all contributing CRITICALs cleared at source; 60 s all-tags-in-band verification; two-hand HMI or authenticated platform NOC reset) → STANDBY
- Fire-origin: all five recovery gates satisfied (§9.2) → STANDBY-FIRE-RECOVERY → STANDBY
- E-stop asserted while in SAFE-STATE → E-STOP
- 480 V AC lost while in SAFE-STATE → E-STOP (BMS remains live on UPS, mode transitions to E-STOP)

**Subsystem state during SAFE-STATE — non-fire-origin (`fire_event = false`).**

| Subsystem | State |
|---|---|
| CDU pumps | STOP (via Modbus CMD-PUMP-ENABLE = 0, plus hardwired safe-state relay fallback per CTRL-001 §8.4) |
| MIV-S | CLOSED (DO de-energized; Belimo spring-returns) |
| MIV-R | CLOSED |
| Workload-enable | DE-ENERGIZED |
| Munters | RUN (BMS keeps Munters running to hold humidity during cool-down — CTRL-001 §6.3 step 5) |
| Fire panel arm state | ARMED (DO-FIRE-ARM de-energized per CTRL-001 §6.3 step 6) |
| 480 V AC | PRESENT |
| BMS | RUNNING |

**Subsystem state during SAFE-STATE — fire-origin (`fire_event = true`).**

| Subsystem | State |
|---|---|
| CDU pumps | STOP |
| MIV-S | CLOSED |
| MIV-R | CLOSED |
| Workload-enable | DE-ENERGIZED |
| Munters | HARDWARE-CONTROLLED (stopped by fire panel NC interlock per FIRE-001 §9.1; BMS does not command this stop — the hardwired series contact in the Munters run circuit opens regardless of BMS state) |
| Fire panel arm state | ARMED (DO-FIRE-ARM de-energized — panel is free to proceed through its own countdown/discharge logic) |
| 480 V AC | PRESENT (fire does not shunt-trip 480 V AC in Rev 1.2 per FIRE-001 §9.5) |
| BMS | RUNNING |

The only cell that differs between the two variants is Munters. That difference is structural — in a fire event Munters airflow would dilute Novec 1230 and must be stopped before or during discharge; the hardwired NC contact in FIRE-001 §9.1 handles it without BMS mediation.

### 2.7 E-STOP

**Purpose.** The physical E-stop button has been pressed, or platform NOC has issued an E-stop-request, or 480 V AC has been tripped by ELEC-001 for any other reason. Every actuator is passively in its fail-safe state because power has been removed.

**Entry conditions.**

- ESTOP-DI asserted (panel E-stop pushbutton pressed — wired directly to ELEC-001 shunt-trip, not a BMS-logic path)
- Platform NOC issues authenticated `e-stop-request` over OPC-UA → BMS forwards the trip command to ELEC-001 via a DO (or via the hardwired safe-state relay path if configured)
- POWER-OK DI deasserts for ≥ 3 s without a corresponding `planned-shutdown` flag (unplanned 480 V AC loss — treated as E-STOP because the facility cannot operate at all without AC)

**Exit conditions.**

- 480 V AC restored externally (ELEC-001 breaker reset by field engineer) + POWER-OK DI asserts + ESTOP-DI clear + platform NOC acknowledgement of the E-stop event → STANDBY

The BMS cannot restore 480 V AC by software. Recovery is a physical action. Per M10.

**Subsystem state during E-STOP.**

| Subsystem | State |
|---|---|
| CDU pumps | STOP (CDU skid loses 480 V AC — pumps physically dead; BMS Modbus link to skid may also be down) |
| MIV-S | CLOSED (actuator 24 VDC loop is on UPS for ≥ 30 min; DO de-energized drives valve closed; if UPS itself drops, spring-return still closes the valve passively) |
| MIV-R | CLOSED (same) |
| Workload-enable | DE-ENERGIZED |
| Munters | STOP (Munters runs on 480 V AC — it dies with the feed) |
| Fire panel arm state | ARMED (fire panel has its own 24 h battery; remains armed) |
| 480 V AC | ABSENT |
| BMS | RUNNING (on UPS, ≥ 30 min hold-up per CTRL-001 §2.3; after UPS depletion BMS goes HELD) |

If UPS depletion occurs during an extended E-STOP (> 30 min), the BMS itself shuts down cleanly. On power restoration, the Jetson cold-boots and re-enters INIT.

---

## 3. Mode state machine — directed graph

```
                           ┌─────────────────────────────────────────┐
                           │                                         │
                    [cold boot]                                       │
                           │                                          │
                           ▼                                          │
                     ┌──────────┐                                     │
                     │   INIT   │                                     │
                     └────┬─────┘                                     │
                          │  [self-test pass, ≤120s]                  │
                          │                                           │
                          ▼                                           │
                    ┌───────────┐                                     │
                    │  STANDBY  │◄────────────────────────┐           │
                    └───┬───────┘                          │           │
                        │  ▲   ▲                           │           │
                        │  │   │                           │           │
           [start-cool] │  │   │ [reset §6.4 complete,     │           │
                        │  │   │  non-fire-origin]         │           │
                        │  │   │                           │           │
                        │  │   │  ┌──────────────────────┐ │           │
                        │  │   └──┤  STANDBY-FIRE-       │ │           │
                        │  │      │  RECOVERY (§6)       │ │           │
                        │  │      │  [all 5 gates §9.2]  │ │           │
                        │  │      └──────────────▲───────┘ │           │
                        │  │                     │         │           │
                        │  │ [stop-cool]         │[gate5]  │           │
                        ▼  │                     │         │           │
                     ┌──────────┐           ┌────┴─────────┴─┐         │
                     │  READY   │           │   SAFE-STATE    │         │
                     └───┬──────┘           │  (fire/non-fire)│         │
                         │  ▲               └──▲──▲──▲──▲────┘         │
                         │  │                  │  │  │  │              │
          [wl-enable +   │  │                  │  │  │  │              │
           all 4 gates]  │  │[stop-wl]         │  │  │  │              │
                         │  │                  │  │  │  │              │
                         ▼  │                  │  │  │  │              │
                     ┌──────────┐  [ALARM]     │  │  │  │              │
                     │PRODUCTION├────────────┐ │  │  │  │              │
                     └───┬──────┘            │ │  │  │  │              │
                         │                   ▼ │  │  │  │              │
                         │              ┌──────────┐                   │
                         │              │ DEGRADED │                   │
                         │              └────┬─────┘                   │
                         │                   │                         │
                         │                   │[all ALARMs clear]       │
                         │                   │                         │
                         │         [CRITICAL]▼    ▲                    │
                         │             (CRITICAL) │[PROD→DEG via ALARM]│
                         │                        │                    │
                         └────────────[CRITICAL]──┘                    │
                                                                        │
                     ┌────────┐                                         │
                     │ E-STOP │◄───────[E-stop DI, platform e-stop,     │
                     └───┬────┘         unplanned 480VAC loss]          │
                         │                                              │
                         │  [480VAC restored + POWER-OK + NOC ack]      │
                         └──────────────────────────────────────────────┘

   Simultaneous triggers resolved by priority (§12 alarm→mode mapping):
     E-STOP > SAFE-STATE > DEGRADED > MAINTENANCE-STANDBY > READY > PRODUCTION > STANDBY > INIT
```

(STANDBY sub-states STANDBY-MAINT-GENERAL and STANDBY-MAINT-COOLANT are treated as STANDBY for the top-level diagram; their branch within STANDBY is shown in §6.)

---

## 4. Transition table

Every arc in §3 is listed here, with the trigger condition, any prerequisite, and the BMS actions executed on transition.

| From | To | Trigger | Prerequisite | BMS action on transition |
|---|---|---|---|---|
| *(cold boot)* | INIT | Jetson power-on | 480 V AC present; UPS healthy | Begin self-test sequence (§5); mode.current = "INIT" |
| INIT | STANDBY | All self-test steps pass within 120 s | No INIT-FAULT | Open OPC-UA server; start publishing mode.current = "STANDBY"; begin normal I/O scan |
| INIT | *(held in INIT)* | Any self-test step fails after 3 retries | — | Publish INIT-FAULT; display fault reason on local HMI; hold mode = "INIT-FAULT" |
| STANDBY | STANDBY-MAINT-GENERAL | Authenticated `enter-maintenance-general` from platform NOC | No active alarms above WARN | Energize DO-FIRE-ARM (panel inhibit); verify FIRE-DI-2 opens round-trip; mode = "STANDBY-MAINT-GENERAL" |
| STANDBY | STANDBY-MAINT-COOLANT | Authenticated `enter-maintenance-coolant` from platform NOC | No active alarms above WARN; MIVs already closed | Energize DO-FIRE-ARM; verify FIRE-DI-2 opens; confirm MIV-S/MIV-R closed limits; mode = "STANDBY-MAINT-COOLANT" |
| STANDBY-MAINT-* | STANDBY | Authenticated `exit-maintenance` from platform NOC | All maintenance work signed off | De-energize DO-FIRE-ARM; verify FIRE-DI-2 closes round-trip; mode = "STANDBY" |
| STANDBY | READY | Authenticated `start-cooling` from platform NOC | No active ALARM or CRITICAL | Energize MIV-S DO; energize MIV-R DO; write CMD-PUMP-ENABLE=1 over Modbus; mode = "READY" |
| READY | PRODUCTION | Authenticated `workload-enable-request` from platform NOC | All four gates satisfied continuously ≥ 10 s | Energize workload-enable DO; mode = "PRODUCTION" |
| READY | STANDBY | Authenticated `stop-cooling` from platform NOC | — | Write CMD-PUMP-ENABLE=0; de-energize MIV DOs; verify closed limits; mode = "STANDBY" |
| READY | *(held in READY)* | Any of four gates fails within 120 s of start-cooling | — | Raise WARN; hold in READY; platform operator decides whether to retry or drop to STANDBY |
| PRODUCTION | DEGRADED | Any ALARM-level alarm active past TTA and deadband | No CRITICAL alarm | Publish workload-throttle-request with severity per §7 mapping; mode = "DEGRADED" |
| PRODUCTION | READY | Authenticated `stop-workload` from platform NOC | — | De-energize workload-enable DO; mode = "READY" |
| PRODUCTION | SAFE-STATE | Any CRITICAL alarm | — | Execute CTRL-001 §6.3 safe-state sequence; set `fire_event` flag per CRITICAL source; mode = "SAFE-STATE" |
| DEGRADED | PRODUCTION | All ALARM conditions clear past deadbands continuously ≥ 30 s | — | Clear workload-throttle-request; mode = "PRODUCTION" |
| DEGRADED | SAFE-STATE | Any CRITICAL alarm | — | Execute §6.3 safe-state sequence; set `fire_event`; mode = "SAFE-STATE" |
| DEGRADED | READY | Authenticated `stop-workload` from NOC | — | De-energize workload-enable DO; alarm conditions remain monitored; mode = "READY" |
| Any non-E-STOP | SAFE-STATE | Any CRITICAL alarm; watchdog trip; platform `maintenance-isolation` | — | Execute §6.3; set `fire_event` = true iff CRITICAL source is FIRE-TRIGGERED; mode = "SAFE-STATE" |
| Any mode | E-STOP | ESTOP-DI asserts; platform `e-stop-request`; POWER-OK deasserts ≥ 3 s without `planned-shutdown` | — | ELEC-001 shunt-trip executes; BMS publishes e-stop event; mode = "E-STOP" |
| SAFE-STATE | STANDBY | CTRL-001 §6.4 reset; `fire_event = false` | All contributing CRITICALs cleared; 60 s all-tags-in-band; two-hand HMI or authenticated NOC reset | Open MIVs; enable pumps; clear workload-enable latch; mode = "STANDBY" (per M8 — does NOT auto-progress to PRODUCTION) |
| SAFE-STATE | STANDBY-FIRE-RECOVERY | `fire_event = true` and CRITICAL fire condition has cleared at panel level | Fire panel reset, cylinder status confirmed (steps 1 & 2 of §9.2) | Remain in safe-state posture; mode = "STANDBY-FIRE-RECOVERY"; await remaining 3 gates |
| STANDBY-FIRE-RECOVERY | STANDBY | All five gates in §9.2 logged complete in recovery-gates.json | — | Clear `fire_event` flag; mode = "STANDBY" |
| E-STOP | STANDBY | POWER-OK DI asserts + ESTOP-DI clear + authenticated `e-stop-acknowledge` from NOC | Jetson has not cold-booted (if UPS depleted, path is E-STOP → cold boot → INIT → STANDBY) | Log E-stop duration; publish recovery event; mode = "STANDBY" |

---

## 5. INIT sequence

Per M5: ≤ 120 s total on a healthy system; each step retries up to 3 times on failure; any step failing all 3 retries raises INIT-FAULT CRITICAL and the BMS freezes in INIT until manual intervention.

| # | Step | Pass criterion | On failure |
|---|---|---|---|
| I-01 | OS boot check | `/` mounted RW; kernel version matches gold-image digest | Publish "OS_BOOT_FAIL" reason; hold in INIT |
| I-02 | Application supervisor check | `systemd` reports `adc-bms.service` active (running) within 30 s of OS ready | Publish "APP_SUPERVISOR_FAIL"; hold |
| I-03 | Watchdog handshake verification | Hardware watchdog confirms receipt of 1 Hz heartbeat for ≥ 5 consecutive seconds | Publish "WATCHDOG_HANDSHAKE_FAIL"; hold |
| I-04 | I/O module scan | All configured I/O modules on the DIN-rail bus respond to scan command | Publish "IO_MODULE_<addr>_MISSING"; hold (CTRL-001 §3 tag list is the authority on expected modules) |
| I-05 | Sensor baseline check | Every configured sensor reports a value within its sensible range on first read | Publish "SENSOR_<tag>_OUT_OF_RANGE"; hold |
| I-06 | Modbus TCP CDU skid reachability | BMS Modbus master successfully reads 3 consecutive polls from CDU skid PLC (§CTRL-001 §8) | Publish "CDU_COMMS_FAIL_AT_INIT"; hold — INIT does not let the Cassette enter STANDBY without a working CDU skid connection |
| I-07 | OPC-UA server bind | Server binds to configured port (4840) on platform-mgmt VLAN interface and passes a local self-subscription test | Publish "OPCUA_BIND_FAIL"; hold |
| I-08 | Configuration schema validation | YAML config in `/etc/adc-bms/config.yaml` validates against schema (`adc-bms --check-config` exits 0) | Publish "CONFIG_SCHEMA_INVALID"; hold |
| I-09 | Alarm table load | Alarm table from config loaded into alarm-engine; smoke-test a synthetic alarm injection clears within 1 s | Publish "ALARM_ENGINE_FAIL"; hold |
| I-10 | Fire panel DI sanity | FIRE-DI-1, FIRE-DI-2, FIRE-DI-3 all read as expected for a powered, armed, non-alarm panel (DI-1 = closed/no-alarm, DI-2 = closed/armed, DI-3 = closed/no-fault) | Publish "FIRE_PANEL_STATE_UNEXPECTED"; hold — BMS will not enter STANDBY if the fire panel is already in alarm or fault at boot |
| I-11 | Time sync acquired | PTP lock within 100 ms of platform reference, or NTP fallback active | Publish "TIME_SYNC_FAIL"; hold |
| I-12 | Certificate validity check | OPC-UA device cert, OTA client cert both within validity period and chain-verify against pinned CA (per CYBER-001 §7) | Publish "CERT_<svc>_INVALID"; hold |
| I-13 | Mode transition | All of the above pass → publish mode.current = "STANDBY"; log INIT_COMPLETE event with elapsed time | — |

On INIT-FAULT: the BMS holds in mode "INIT-FAULT", displays the failed step reason on local HMI, publishes to OPC-UA (if I-07 succeeded, otherwise local-HMI-only), and requires a manual `clear-init-fault` command or BMS restart. The watchdog continues to run; if the Jetson also stops heartbeating, the watchdog drops the safe-state relay independently.

---

## 6. STANDBY sub-states

STANDBY has four sub-states. The top-level mode tag always shows "STANDBY" or its specific sub-state variant; the platform SCADA distinguishes by the sub-state string.

### 6.1 STANDBY-IDLE

Default STANDBY. Per §2.2 exactly. This is the one the Cassette enters out of INIT, out of recovery paths, out of `stop-cooling` from READY.

### 6.2 STANDBY-MAINT-GENERAL

**Purpose.** A maintenance window where the coolant loop is not being worked on. Example: rack swap, cable termination, non-coolant sensor replacement, HMI touchscreen service.

**Entry.** STANDBY + authenticated `enter-maintenance-general` from platform NOC.

**Key difference from STANDBY-IDLE:**

- DO-FIRE-ARM is ENERGIZED (panel is INHIBITED — safe for personnel to be inside the Cassette). BMS verifies round-trip: FIRE-DI-2 must transition from closed to open within 1 s of energizing the DO.
- MIVs remain CLOSED (no coolant in the loop beyond what is already captured; it does not need to be there to do general work).
- Tamper DI is expected to change state (ECP panel or outer door opened); this generates an INFO event during a maintenance window, a WARN otherwise.

**Subsystem state.**

| Subsystem | State |
|---|---|
| CDU pumps | STOP |
| MIV-S | CLOSED |
| MIV-R | CLOSED |
| Workload-enable | DE-ENERGIZED |
| Munters | RUN |
| Fire panel arm state | INHIBITED (DO-FIRE-ARM energized, FIRE-DI-2 open) |
| 480 V AC | PRESENT |
| BMS | RUNNING |

**Exit.** Authenticated `exit-maintenance` from NOC → de-energize DO-FIRE-ARM → verify FIRE-DI-2 closes (round-trip < 1 s) → STANDBY-IDLE.

### 6.3 STANDBY-MAINT-COOLANT

**Purpose.** Maintenance on the coolant loop itself. Example: MIV actuator replacement, sensor-in-loop calibration, leak repair at QBH-150, CDU skid QD swap.

**Entry.** STANDBY + authenticated `enter-maintenance-coolant` from platform NOC.

**Key difference from STANDBY-MAINT-GENERAL.** None at the mode-tag level — the Cassette reports both as sub-states of STANDBY with the maintenance flag. The operational difference is that the platform NOC knows coolant work is being done and holds a maintenance record accordingly. BMS does not physically enforce a different posture — MIVs are already closed in both maintenance sub-states.

**Why distinguish them.** Audit and safety paperwork. Coolant work carries additional hazard considerations (propylene glycol handling, hot coolant if work is performed soon after PRODUCTION exit). The mode tag drives platform-side procedure templates.

**Subsystem state.** Identical to STANDBY-MAINT-GENERAL by subsystem; different sub-state label.

**Exit.** Same as STANDBY-MAINT-GENERAL.

### 6.4 STANDBY-FIRE-RECOVERY

**Purpose.** Post-fire recovery staging. The Cassette has been through a fire-origin SAFE-STATE and the operator has begun the five-gate recovery checklist. BMS enforces gate completion before allowing transition to STANDBY-IDLE.

**Entry.** SAFE-STATE (fire-origin) + gates 1 and 2 of §9.2 complete (fire panel manually reset by Ansul technician with service key AND cylinder replaced or confirmed recharged). The BMS cannot autonomously detect these — they are logged as authenticated platform NOC events and written to `recovery-gates.json`.

**Subsystem state.**

| Subsystem | State |
|---|---|
| CDU pumps | STOP |
| MIV-S | CLOSED |
| MIV-R | CLOSED |
| Workload-enable | DE-ENERGIZED |
| Munters | HARDWARE-CONTROLLED (still interlocked off until fire panel is fully reset and Munters starter is manually re-armed — same posture as fire-origin SAFE-STATE); transitions to RUN once the hardwired interlock NC contact closes again after panel reset |
| Fire panel arm state | ARMED (post-reset — DO-FIRE-ARM de-energized; FIRE-DI-2 closed; FIRE-DI-3 clear — these are in fact gate 4 of §9.2) |
| 480 V AC | PRESENT |
| BMS | RUNNING |

**Exit.** All five gates in `recovery-gates.json` logged complete → clear `fire_event` flag → STANDBY-IDLE.

The BMS does not skip gates. If gate 3 (enclosure re-inspection) is not logged, the BMS holds in STANDBY-FIRE-RECOVERY regardless of operator pressure to proceed. See §9.2 for the gate implementation.

---

## 7. DEGRADED mode logic

Per M4: DEGRADED is bounded. PRODUCTION + any ALARM ⇒ DEGRADED; DEGRADED → PRODUCTION when alarms clear; DEGRADED → SAFE-STATE on any CRITICAL.

### 7.1 Entry

PRODUCTION + any ALARM-level alarm active past its TTA and deadband per the CTRL-001 §6.2 alarm table. The ALARM must be genuinely active — transient conditions that clear within the TTA do not cause a mode transition.

### 7.2 Workload-throttle-request severity mapping

The BMS publishes a workload-throttle-request over OPC-UA on DEGRADED entry, updates on each alarm state change, and clears on DEGRADED exit. Severity is the maximum severity across all currently active ALARMs, per this mapping:

| Alarm ID (from CTRL-001 §6.2) | Severity | Suggested reduction fraction |
|---|:-:|:-:|
| SUPPLY-T-HI-A (CDU supply T > 48 °C > 3 min) | 2 (hard) | 0.40 |
| RETURN-T-HI-A (CDU return T > 58 °C > 3 min) | 2 | 0.40 |
| LOOP-P-LO-A (loop P < 2.5 bar) | 2 | 0.50 |
| LOOP-P-HI-A (loop P > 6.0 bar) | 2 | 0.30 |
| FLOW-LO-A (FT-102 < 80 % of setpoint) | 2 | 0.50 |
| INT-RH-HI-A (interior RH > 60 %) | 1 (soft) | 0.15 |
| INT-T-HI-A (interior T > 35 °C) | 2 | 0.30 |
| CO2-HI-A (CO₂ > 1,000 ppm) | 1 (soft) + personnel alert | 0.00 (personnel, not throttle) |
| SUMP-HI-A (sump high level) | 2 (proximate to CRITICAL) | 0.50 |
| CDU-COMMS-LOST | 2 | 0.50 |
| CDU-PUMP-FAULT | 2 | 0.30 |
| FIRE-FAULT | 1 (soft) | 0.00 (monitor; do not throttle on panel trouble alone) |
| POWER-LOSS (480 V AC absent, on UPS) | 2 | 0.80 |
| RACK-TEMP-HI (WARN-level by default) | — | not a DEGRADED trigger; raised to ALARM by rack escalation logic if persistent |

Multiple simultaneous ALARMs: maximum severity and maximum suggested reduction fraction.

### 7.3 Platform response

Per CTRL-001 §9.2, the BMS publishes workload-throttle-request; the platform NOC decides what to do. The BMS does **not** autonomously reduce workload. It maintains the DEGRADED mode tag so the platform dashboard shows the state.

If the platform NOC decides to reduce workload, it does so through its own scheduler — the BMS just observes the lower power draw and interior temperatures fall. The mode remains DEGRADED until the ALARM clears at the source.

If the platform chooses to ignore the throttle-request (rare but possible — e.g., a brief ALARM during a peak workload window that operations would rather ride out), the Cassette remains in DEGRADED. Continued DEGRADED with no clearing is an operational event, not a safety event. The BMS escalates to SAFE-STATE only on CRITICAL.

### 7.4 Exit

- All contributing ALARM conditions clear past their deadbands continuously for ≥ 30 s → PRODUCTION. The 30 s confirmation prevents mode flap when an ALARM borderline reading is oscillating around its threshold.
- Any CRITICAL alarm → SAFE-STATE (with `fire_event` flag if source is FIRE-TRIGGERED).
- `stop-workload` from NOC → READY, alarms remain monitored.

---

## 8. SAFE-STATE — fire-origin vs non-fire-origin

Per M2: fire event is not a separate top-level mode. It is an entry path into SAFE-STATE with `fire_event = true`.

### 8.1 The `fire_event` flag

Set on SAFE-STATE entry when the originating CRITICAL is FIRE-TRIGGERED (CTRL-001 §6.2, FIRE-001 §8.2). Cleared on successful exit from STANDBY-FIRE-RECOVERY to STANDBY-IDLE (see §9.2).

Stored at `/var/bms/state/fire_event.flag` (persisted to NVMe so it survives a BMS restart during recovery). Published as `adc.cassette.<serial>.mode.fire_event` over OPC-UA.

### 8.2 Difference between fire and non-fire SAFE-STATE

| Aspect | Non-fire SAFE-STATE | Fire SAFE-STATE (`fire_event = true`) |
|---|---|---|
| Munters state | RUN (BMS keeps humidity control during cool-down, CTRL-001 §6.3 step 5) | HARDWARE-CONTROLLED — stopped by the fire panel NC interlock in series with the Munters run circuit (FIRE-001 §9.1). BMS is explicitly not the authority here. |
| Fire panel arm state | ARMED (DO-FIRE-ARM de-energized per CTRL-001 §6.3 step 6) | ARMED (same) |
| DO-FIRE-ARM | De-energized on entry | De-energized on entry (so the panel is free to run its own countdown/discharge sequence if it hasn't already) |
| DO-FIRE-RELEASE | De-energized, gate not met | De-energized by default; the four-condition gate per FIRE-001 §8.6 may be evaluated by the BMS if the platform NOC issues a `fire-remote-release-request` |
| Other subsystems (CDU pumps, MIVs, workload, 480 V AC) | Same as fire case | Same as non-fire case |
| Expected exit path | CTRL-001 §6.4 reset → STANDBY-IDLE | Five-gate recovery (§9.2) → STANDBY-FIRE-RECOVERY → STANDBY-IDLE |
| Expected duration | Minutes to hours (operator response + alarm source cleared) | Hours to days (Ansul service dispatch + cylinder replacement + AHJ clearance) |

The only runtime cell that differs between the two variants is Munters. Everything else is identical. The mode tag carries the flag; the recovery path is what diverges.

### 8.3 Multiple simultaneous CRITICALs

If more than one CRITICAL is active on entry (e.g., SUMP-HIHI-C and FIRE-TRIGGERED together), `fire_event` is set to `true` if FIRE-TRIGGERED is one of them. The recovery path is driven by the most restrictive case, which is fire.

---

## 9. Recovery paths

Three recovery scenarios — SAFE-STATE (non-fire), SAFE-STATE (fire), E-STOP.

### 9.1 SAFE-STATE (non-fire) → STANDBY → READY

Per M8.

1. Operator diagnoses and remediates the source of every active CRITICAL. Examples: TraceTek wet zone dried and cable reset; sump pumped down and high-high float cleared; CDU comms restored; supply-T overshoot resolved by CDU skid supply setpoint correction.
2. All contributing CRITICALs clear at the source. BMS alarm engine sees them transition out of CRITICAL; latched state remains.
3. Operator initiates reset. Per CTRL-001 §6.4: either a two-hand local HMI confirmation **or** an authenticated platform NOC command. Both paths require all alarms to be currently clear and to have been clear for ≥ 60 s.
4. BMS executes reset sequence (CTRL-001 §6.4): open MIVs, enable CDU pumps, verify flow > 50 % of setpoint within 60 s, re-energize workload-enable relay latch (but does not assert workload-enable DO).
5. **Mode.current transitions directly to STANDBY-IDLE**, not to PRODUCTION. Workload-enable DO remains de-energized. Per M8, reset never auto-asserts workload.
6. To return to productive operation, the operator then issues `start-cooling` (STANDBY → READY) and `workload-enable-request` (READY → PRODUCTION) in the normal path.

### 9.2 SAFE-STATE (fire-origin) → STANDBY-FIRE-RECOVERY → STANDBY → READY

Per M9. Five gates, enforced by the BMS via `/etc/adc-bms/recovery-gates.json`.

**The recovery-gates.json file.** A small JSON file owned by root, mode 0644, that the BMS reads on every mode-transition evaluation while `fire_event = true`. Schema:

```
{
  "cassette_serial": "<serial>",
  "fire_event_timestamp": "<ISO-8601>",
  "gates": {
    "panel_reset":         { "complete": false, "by": null, "at": null, "method": null },
    "cylinder_status":     { "complete": false, "by": null, "at": null, "method": null },
    "enclosure_inspection":{ "complete": false, "by": null, "at": null, "method": null },
    "bms_interface_check": { "complete": false, "by": null, "at": null, "method": null },
    "noc_signoff":         { "complete": false, "by": null, "at": null, "method": null }
  }
}
```

Each gate is a boolean with an audit trail (who set it complete, when, by what method — HMI vs OPC-UA). The BMS only reads this file; it does not write the gate booleans itself — they are set by authenticated writes triggered from OPC-UA calls (platform NOC role per CYBER-001 §6.3) or by physical HMI two-hand confirmation operations by an operator account authenticated at the local HMI.

**The five gates:**

1. **panel_reset** — Fire panel manually reset with service key by an Ansul-authorized technician. Evidence: photo of reset key sequence + panel annunciator returning to normal-ready; FIRE-DI-1, FIRE-DI-3 both clear at the BMS. The technician (or a platform NOC operator acting on technician's confirmation) logs this gate via authenticated call.
2. **cylinder_status** — Agent cylinder replaced or confirmed recharged per FIRE-001 §10.5. Evidence: supervisory pressure and supervisory weight both back to nominal; Ansul service record filed. Logged by platform NOC after Ansul paperwork received.
3. **enclosure_inspection** — Cassette interior re-inspected after any discharge: no residual moisture, no visible damage, MSDS signage posted and current, personnel-safety sign intact. Evidence: inspection checklist filed. Logged by platform NOC.
4. **bms_interface_check** — BMS fire-arm DI handshake re-verified: FIRE-DI-2 reading closed/armed; FIRE-DI-3 reading closed/no-fault; DO-FIRE-ARM energize/de-energize round-trip test executed and FIRE-DI-2 transitions correctly (identical to FIRE-001 §12.2 step SP-10 but done in the field). Logged by the BMS itself on successful round-trip, or by platform NOC if done out-of-band.
5. **noc_signoff** — Platform NOC lead sign-off. A final review that gates 1–4 are all genuinely complete (not rubber-stamped). This is a separate authenticated OPC-UA call distinct from gates 1–4.

**BMS enforcement.** On every mode-transition evaluation, if `fire_event = true` and mode is STANDBY-FIRE-RECOVERY, the BMS checks recovery-gates.json:

- If any gate is `complete: false`, mode stays STANDBY-FIRE-RECOVERY.
- When all five gates transition to `complete: true`, BMS logs a RECOVERY_COMPLETE event (with a summary of who/when/how for each gate), clears the `fire_event` flag (writes `/var/bms/state/fire_event.flag` to empty), deletes recovery-gates.json (so a future fire event starts from a fresh file), and transitions to STANDBY-IDLE.

This is a BMS-enforced checklist, not advisory text. Code review of the enforcement path is flagged at **MODES-03**.

### 9.3 E-STOP → STANDBY

Per M10.

1. 480 V AC has been removed — physically at the ELEC-001 breaker. BMS continues running on UPS; mode.current = "E-STOP".
2. Field engineer arrives on-site. Clears the E-stop pushbutton (if that was the cause) and resets the ELEC-001 shunt-trip breaker externally. Per ELEC-001 §6, neither can be reset by software.
3. POWER-OK DI asserts when 480 V AC returns to the Cassette. ESTOP-DI returns to normal if the panel button was the cause.
4. BMS detects POWER-OK asserted + ESTOP-DI clear; holds in E-STOP pending platform NOC acknowledgement.
5. Platform NOC issues authenticated `e-stop-acknowledge` OPC-UA command. This step exists so that an accidental AC restoration cannot auto-recover an E-stop that was deliberately engaged for operator safety. NOC confirms the field condition before ack.
6. BMS logs E-stop duration (from entry to acknowledge), publishes recovery event, transitions mode.current to "STANDBY-IDLE".
7. If UPS was depleted during the E-stop (> 30 min hold-up exhausted), the Jetson cold-boots on 480 V AC restoration. Path is E-STOP → cold boot → INIT → STANDBY. The BMS does not remember it was in E-STOP across a cold boot; it enters INIT fresh.

After STANDBY, the normal STANDBY → READY → PRODUCTION path applies.

---

## 10. Mode OPC-UA tag definition

Per M11. Mode is a first-class platform signal.

### 10.1 mode.current

| Field | Value |
|---|---|
| Tag path | `adc.cassette.<serial>.mode.current` |
| Data type | String (enum) |
| Enum values | `INIT`, `INIT-FAULT`, `STANDBY-IDLE`, `STANDBY-MAINT-GENERAL`, `STANDBY-MAINT-COOLANT`, `STANDBY-FIRE-RECOVERY`, `READY`, `PRODUCTION`, `DEGRADED`, `SAFE-STATE`, `E-STOP` |
| Fire event sidecar | `adc.cassette.<serial>.mode.fire_event` — Boolean — true iff current SAFE-STATE or STANDBY-FIRE-RECOVERY is fire-origin |
| Update rate | Published within 1 s of any mode transition; republished every 10 s steady-state for subscribers that may have missed a transition |
| Subscription model | All platform SCADA clients subscribed by default; historian records every transition |
| Access control | Read-only for all OPC-UA users; no client can write mode.current directly. Mode transitions happen through their specific transition commands (§13). |

### 10.2 mode.history

| Field | Value |
|---|---|
| Tag path | `adc.cassette.<serial>.mode.history` |
| Data type | Structured array — ring buffer of last 100 transitions |
| Per-record fields | `timestamp` (ISO-8601), `from_mode` (enum), `to_mode` (enum), `trigger` (string describing the condition, e.g., "CRITICAL:SUMP-HIHI-C", "NOC:start-cooling", "WATCHDOG-TRIPPED") |
| Update rate | Append-only on every transition |
| Local persistence | Last 100 records persisted in `/var/bms/state/mode_history.json`; survives BMS restart |
| Longer-term history | Platform historian holds the full record indefinitely |
| Subscription | Platform SCADA subscribes for real-time dashboard; incident response uses historian for past-event forensics |

### 10.3 Platform SCADA contract

The mode.current tag drives the Cassette tile color on the platform dashboard:

| Mode | Dashboard color |
|---|---|
| INIT | Amber (transient) |
| INIT-FAULT | Red flashing |
| STANDBY-IDLE | Grey (normal resting) |
| STANDBY-MAINT-* | Blue (planned) |
| STANDBY-FIRE-RECOVERY | Orange (post-event) |
| READY | Green-light (warming up) |
| PRODUCTION | Green (normal) |
| DEGRADED | Yellow |
| SAFE-STATE | Red |
| E-STOP | Red flashing |

The platform SCADA implementation is out of scope here, but the color mapping is published by the BMS as an enum so the platform does not need to reinvent it.

---

## 11. Interaction with the alarm hierarchy

CTRL-001 §6.2 is the authority on which condition raises INFO, WARN, ALARM, or CRITICAL. This section maps those levels to mode effects.

| Alarm level | Effect on mode |
|---|---|
| **INFO** | No mode change. Logged. Published as an OPC-UA event. |
| **WARN** | No mode change. Logged. SCADA banner on the Cassette tile. Persistent WARN during maintenance window is expected; during PRODUCTION is a data point for ops review. |
| **ALARM** (active past TTA and deadband) | **PRODUCTION → DEGRADED** (if currently PRODUCTION). No other mode transitions to DEGRADED. If in READY, alarms are logged and held; the mode stays READY. If in STANDBY, alarms are logged; the mode stays STANDBY. |
| **CRITICAL** | **Any mode → SAFE-STATE** if CRITICAL source is not E-stop-related. **Any mode → E-STOP** if source is ESTOP-DI, `e-stop-request`, or POWER-OK unplanned loss. Watchdog trip → SAFE-STATE. CRITICAL source FIRE-TRIGGERED → SAFE-STATE with `fire_event = true`. |

**A CRITICAL during a maintenance window** (STANDBY-MAINT-*) still causes SAFE-STATE. The BMS does not suppress safety responses during maintenance. However, the DO-FIRE-ARM state was ENERGIZED during maintenance (panel inhibited); on entry to SAFE-STATE, DO-FIRE-ARM is de-energized per CTRL-001 §6.3 step 6 regardless of prior state. The panel is armed in SAFE-STATE.

**A WARN during SAFE-STATE** does not cause a mode transition. The Cassette remains in SAFE-STATE. WARNs during SAFE-STATE are logged and help the operator diagnose the contributing CRITICAL.

**Alarm latching vs mode latching** are distinct. Alarms latch per CTRL-001 §6.2 and require acknowledgement (WARN, ALARM) or reset (CRITICAL). Modes change automatically when the underlying conditions change. Clearing an alarm does not immediately clear the mode — the BMS waits for the deadband and TTA criteria in §7.4 for DEGRADED → PRODUCTION and §9 for SAFE-STATE → STANDBY.

---

## 12. Per-mode commissioning verification

One verification step per mode transition, designed to exercise the real transition — not just synthetic alarm injection. Supplements CTRL-001 §10.2 site steps and FIRE-001 §12.2.

| # | Transition | Procedure | Pass criterion |
|---|---|---|---|
| M-V1 | (cold boot) → INIT → STANDBY | Power-cycle the Cassette from a clean 480 V AC restoration. Start a stopwatch at power-on. | INIT completes ≤ 120 s; mode.current transitions "INIT" → "STANDBY-IDLE"; all I-01 through I-13 pass criteria met; INIT_COMPLETE event with elapsed-time field appears in historian |
| M-V2 | STANDBY → READY | Platform NOC issues `start-cooling`. Operator watches the Cassette execute the transition. | MIV-S and MIV-R both reach OPEN limit within 15 s; CMD-PUMP-ENABLE written to 1; CDU skid reports pumps RUN; FT-102 ramps to ≥ 80 % of setpoint within 90 s; TT-103 holds ≤ 45 °C; mode.current = "READY" |
| M-V3 | READY → PRODUCTION | With the Cassette in READY and all four gates satisfied, platform NOC issues `workload-enable-request`. | Workload-enable DO energizes within 1 s; platform-side workload-enable relay closes; mode.current = "PRODUCTION"; no alarms raised by the transition itself |
| M-V4 | PRODUCTION → DEGRADED | Inject an ALARM-level condition — example: apply a temporary heat source near an interior T/RH sensor to push INT-T above 35 °C for > 300 s. | BMS raises INT-T-HI-A ALARM at t = 300 s; mode.current transitions "PRODUCTION" → "DEGRADED"; workload-throttle-request published at severity 2 with suggested reduction 0.30; platform NOC receives event. Remove heat source; verify mode returns to "PRODUCTION" 30 s after deadband clears. |
| M-V5 | DEGRADED → SAFE-STATE | From the DEGRADED state in M-V4 (still active), escalate by injecting a CRITICAL: simulated TraceTek Zone 2 wet via the TT-SIM-2 test mode. | mode.current transitions to "SAFE-STATE" within 1 s; `fire_event = false`; CTRL-001 §6.3 seven-step sequence executes and is logged; MIV-S and MIV-R reach CLOSED limit within 10 s; workload-enable DO de-energizes; Munters continues RUN; DO-FIRE-ARM de-energized (panel armed) |
| M-V6 | SAFE-STATE → STANDBY (non-fire) | Dry the TraceTek simulation, wait for all CRITICALs to clear + 60 s all-tags-in-band. Execute two-hand HMI reset. | CTRL-001 §6.4 reset sequence completes; MIVs re-open; pumps re-enable; FT-102 > 50 % within 60 s; mode.current = "STANDBY-IDLE"; workload-enable DO remains DE-ENERGIZED (M8 verified — no auto-progression to PRODUCTION) |
| M-V7 | SAFE-STATE (fire-origin) → STANDBY-FIRE-RECOVERY → STANDBY | At a scheduled fire-drill window, assert FIRE-DI-1 via the fire panel test mode (no actual agent discharge — use the panel's "alarm simulate" function). Verify BMS enters SAFE-STATE with `fire_event = true`. Then walk all five gates in §9.2 one at a time: (1) panel reset with service key; (2) verify cylinder supervisory (no real discharge, so gate 2 is a pressure/weight check only); (3) document enclosure inspection; (4) BMS interface round-trip; (5) NOC sign-off. | `fire_event = true` on SAFE-STATE entry; Munters hardware-controlled OFF verified; after each gate is logged, mode tag tracks progress; mode.current transitions STANDBY-FIRE-RECOVERY → STANDBY-IDLE only after all five gates show `complete: true`; `fire_event` clears |
| M-V8 | STANDBY → STANDBY-MAINT-GENERAL → STANDBY | Platform NOC issues `enter-maintenance-general`. Operator enters the Cassette interior with fire panel inhibited. After 5 min, NOC issues `exit-maintenance`. | DO-FIRE-ARM energizes; FIRE-DI-2 opens within 1 s (round-trip confirmed); mode.current = "STANDBY-MAINT-GENERAL"; ECP tamper DI fires during interior access (logged as INFO during maintenance window); on exit, DO-FIRE-ARM de-energizes; FIRE-DI-2 closes within 1 s; mode.current returns to "STANDBY-IDLE" |
| M-V9 | Any mode → E-STOP (panel button) | With the Cassette in PRODUCTION, an operator presses the ECP panel E-stop pushbutton. | ELEC-001 shunt-trips within the breaker's design time; POWER-OK clears within 3 s; 480 V AC drops; mode.current transitions to "E-STOP" within the Jetson's UPS-powered window; CDU pumps STOP (physical); MIVs reach CLOSED (fail-safe); Munters STOPS (loss of 480 VAC); workload-enable DE-ENERGIZED; fire panel on its own battery remains ARMED |
| M-V10 | E-STOP → STANDBY | Field engineer resets ELEC-001 breaker (physically). Platform NOC issues `e-stop-acknowledge`. | POWER-OK asserts; ESTOP-DI clear; BMS publishes e-stop duration; mode.current transitions "E-STOP" → "STANDBY-IDLE". If UPS depleted during E-stop, verify the alternative path: cold-boot → INIT → STANDBY, with the INIT-COMPLETE event noting cold-start cause. |

Signed by Ansul-authorized service provider (M-V7 at minimum) + Scott Tomsu + platform NOC lead. This completes the mode-machine commissioning record (**MODES-02**).

---

## 13. Platform NOC interface for mode management

Per M11 and M3. Not every mode transition is operator-initiated; some are BMS-autonomous on alarm or watchdog. This section lists what is which.

### 13.1 Platform-NOC-initiated transitions (authenticated OPC-UA methods)

| OPC-UA method | Drives transition | Required role (CYBER-001 §6.3) |
|---|---|---|
| `start-cooling()` | STANDBY → READY | `operator` or `platform` |
| `workload-enable-request()` | READY → PRODUCTION (after four gates) | `operator` or `platform` |
| `stop-workload()` | PRODUCTION → READY; DEGRADED → READY | `operator` or `platform` |
| `stop-cooling()` | READY → STANDBY; PRODUCTION → (stop-workload then stop-cooling) → STANDBY | `operator` or `platform` |
| `enter-maintenance-general()` | STANDBY → STANDBY-MAINT-GENERAL | `platform` |
| `enter-maintenance-coolant()` | STANDBY → STANDBY-MAINT-COOLANT | `platform` |
| `exit-maintenance()` | STANDBY-MAINT-* → STANDBY | `platform` |
| `e-stop-request()` | Any mode → E-STOP | `platform` |
| `e-stop-acknowledge()` | E-STOP → STANDBY (after physical restore) | `platform` |
| `safe-state-reset()` | SAFE-STATE → STANDBY (non-fire; CTRL-001 §6.4 path) | `platform` |
| `set-recovery-gate(gate_id)` | Updates recovery-gates.json entry (fire-recovery gates 1–5) | `platform` (gates 1, 2, 3, 5) or BMS-self (gate 4 on successful round-trip) |
| `fire-remote-release-request()` | Asserts DO-FIRE-RELEASE per FIRE-001 §8.6 four-condition gate | `platform` only; and all four conditions in FIRE-001 §8.6 must be satisfied |
| `maintenance-isolation()` | Any operating mode → SAFE-STATE (for cybersecurity or ops isolation per CYBER-001 §13) | `platform` |
| `clear-init-fault()` | INIT-FAULT → INIT (retry self-test); if still fails, back to INIT-FAULT | `platform` |

Method binding details (WSDL-equivalent definitions, request/response parameters, error codes) are **MODES-01**.

### 13.2 BMS-autonomous transitions (no NOC command required)

| Transition | Trigger |
|---|---|
| (cold boot) → INIT | Jetson power-on |
| INIT → STANDBY | All self-test steps pass |
| INIT → INIT-FAULT | Any self-test step fails after 3 retries |
| PRODUCTION → DEGRADED | ALARM-level alarm active past TTA and deadband |
| DEGRADED → PRODUCTION | All ALARMs clear past deadbands continuously ≥ 30 s |
| Any → SAFE-STATE | CRITICAL alarm per CTRL-001 §6.2 |
| Any → SAFE-STATE | Hardware watchdog trip (§2.2 of CTRL-001) |
| Any → E-STOP | ESTOP-DI asserts or POWER-OK unplanned loss ≥ 3 s |
| SAFE-STATE → STANDBY-FIRE-RECOVERY | `fire_event = true` and gates 1 & 2 of §9.2 first logged complete |
| STANDBY-FIRE-RECOVERY → STANDBY | All five gates complete in recovery-gates.json |
| READY → (held) | Any of four gates fails within 120 s of start-cooling |

Autonomous transitions are logged with the specific trigger; operator-initiated transitions are logged with the originating OPC-UA user identity.

### 13.3 Transitions that are a composition (autonomous + operator)

Some transitions are driven by an operator command but land the Cassette in a mode that also depends on ambient conditions. Example: `start-cooling` requests STANDBY → READY, but the Cassette actually reaches READY only when MIV open limits and CDU pump acknowledgement land. During the interval between `start-cooling` acceptance and four-gate satisfaction, the mode tag reports "READY" but the platform SCADA sees an additional "stabilizing" sub-status until all four gates latch.

---

## 14. Mode persistence across power cycles

Per M6 and M10 — cold start always goes to INIT → STANDBY regardless of prior mode.

### 14.1 Why

Two reasons.

1. **Safety.** If the Cassette lost 480 V AC while in PRODUCTION, restoring power should not auto-resume PRODUCTION. Workload, MIV state, and cooling flow all need operator confirmation.
2. **Simplicity.** The BMS cannot reliably know its pre-shutdown state across a cold boot — the prior state might have been part of the very event that caused the power loss. Treating every cold start identically removes an entire class of potential bugs.

### 14.2 Planned vs unplanned power-down

The BMS distinguishes these for logging and operator notification, but the mode outcome is the same (both go to INIT → STANDBY on power restoration):

| Scenario | Signature |
|---|---|
| **Planned shutdown** | Platform NOC issued `planned-shutdown` before AC drop; BMS logged a `GRACEFUL_SHUTDOWN` record to NVMe and shut down cleanly. `/var/bms/state/last_shutdown.json` has `kind: "planned"`. |
| **Unplanned power loss** | No `planned-shutdown` flag; last record in `/var/bms/state/last_shutdown.json` is either `kind: "unplanned"` (if the UPS held long enough for the BMS to detect AC loss and write the file) or the file is stale/missing (if UPS depleted or power was cut abruptly) |

Both paths end in Jetson cold-boot on 480 V AC restoration, INIT self-test, STANDBY. The difference appears only in the post-boot event log — the BMS publishes either `COLD_BOOT_AFTER_PLANNED_SHUTDOWN` or `COLD_BOOT_AFTER_UNPLANNED_LOSS` to OPC-UA after I-13 completes, so the platform SCADA can distinguish them on the dashboard.

### 14.3 Recovery-gates.json across power cycles

If the BMS goes through a cold boot while `fire_event = true` (i.e., during STANDBY-FIRE-RECOVERY), the flag at `/var/bms/state/fire_event.flag` and the file at `/etc/adc-bms/recovery-gates.json` both persist (NVMe). On cold boot:

1. INIT runs as normal.
2. Step I-13 transitions mode to STANDBY-IDLE by default.
3. Immediately after STANDBY entry, the BMS inspects `fire_event.flag`. If set, the BMS promotes mode to STANDBY-FIRE-RECOVERY and retains the in-flight gate state.

This means a power cycle during fire recovery does not reset gate progress. The operator picks up where they left off.

### 14.4 BMS reboot (planned, not a power cycle)

An in-place `systemd` restart of `adc-bms` (OTA update, config reload) is not a cold boot. Mode persistence across a BMS application restart is:

- `mode.current` is republished within 1 s of OPC-UA server re-bind based on current subsystem state at restart, not from memory.
- If the Cassette subsystems are in a PRODUCTION-consistent posture (MIVs open, pumps running, workload-enable energized, no alarms), the BMS re-publishes "PRODUCTION".
- If subsystems are in a STANDBY-consistent posture, "STANDBY-IDLE".
- If subsystems are in a SAFE-STATE posture, "SAFE-STATE" (with `fire_event` restored from flag file).

An application restart never autonomously changes subsystem state. The BMS observes the current physical state and reports it.

---

## 15. Open items

| ID | Priority | Description | Blocks |
|---|---|---|---|
| MODES-01 | C1 | Platform NOC OPC-UA method binding for every operator-initiated mode transition in §13.1 — concrete method signatures (request/response parameters, error codes, required role per CYBER-001 §6.3), published in platform API documentation; tested against an OPC-UA client fixture before first Cassette commissioning | Production deployment; M-V2 through M-V10 commissioning verification |
| MODES-02 | C1 | Commissioning verification walk per §12 — all ten transitions M-V1 through M-V10 executed on the first Cassette, signed by Ansul (for M-V7) + Scott Tomsu + platform NOC lead | First Cassette enters production |
| MODES-03 | C1 | BMS enforcement of fire-recovery five-gate checklist in `recovery-gates.json` — independent code review of the gate-enforcement path to confirm no bypass exists (no `skipGates` feature flag, no debug override, no upstream library dependency that could fail-open); review signed off by platform security | Production release of BMS with fire-recovery path |
| MODES-04 | C2 | DEGRADED workload-throttle-request severity tuning — review and adjust the §7.2 mapping after 30-day platform soak of the first production Cassette; refine based on actual platform scheduler response to each severity level | Operational optimization after first-Cassette soak |
| MODES-05 | C2 | INIT timeout tuning — 120 s is a working ceiling; measure actual Jetson boot time + self-test duration across the first 10 Cassette boots; adjust the ceiling downward if consistent headroom is observed, with a safety margin | Rev 1.3 close |
| MODES-06 | C2 | Mode transition alert delivery — platform pager and on-call notification rules for SAFE-STATE and E-STOP entries; alert throttling so that a chatty alarm does not page the team repeatedly | Platform operations readiness |
| MODES-07 | C2 | Mode dashboard visual spec — platform SCADA Cassette-tile color mapping (§10.3) finalized with platform UX team; color-blind-safe palette confirmed | Platform dashboard release |
| MODES-08 | C2 | Fire-drill procedure document — site-level procedure for executing M-V7 (fire-drill transition) on a production Cassette without disrupting neighboring Cassettes or tenant workload; coordinated with platform NOC and Ansul service | Periodic fire-drill capability |
| MODES-09 | C3 | Mode transition replay tool — offline tooling to replay mode history + alarm log for incident forensics; reads from platform historian + local mode_history.json; nice-to-have, not gating | Incident response tooling |

---

## Document control

**Cassette-MODES-001 — Rev 1.2 — CONFIDENTIAL**
**Prepared by:** Scott Tomsu · CEO / Chief Engineer · scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana
**Companion to:** Cassette-CTRL-001 · Cassette-FIRE-001 · Cassette-ELEC-001 · Cassette-COOL-001 · Cassette-COOL2-001 · Cassette-BOM-001
**Supersedes:** Cassette-MODES-001 Rev 1.1 (deleted)
**Authority scope:** the seven-mode state machine, per-mode subsystem states, mode transition conditions, INIT self-test, STANDBY sub-states, DEGRADED logic, fire-event variant of SAFE-STATE, recovery paths (non-fire, fire, E-STOP), mode.current and mode.history OPC-UA tags, alarm-level to mode-effect mapping, mode-transition commissioning verification, platform NOC interface for mode management, mode persistence across power cycles.

MODES-001 is the authority on mode. CTRL-001 §6.2 is the authority on what conditions raise which alarm level; CTRL-001 §6.3–§6.4 is the authority on the literal safe-state execution and reset sequences; FIRE-001 §8–§9 is the authority on the fire panel handshake and the Munters hardwired interlock. Any change to the seven-mode set, the transition table, or the recovery-gate enforcement in §9.2 requires a new revision of this document with coordinated updates to the companion specs.

**End of Cassette-MODES-001 Rev 1.2.**
