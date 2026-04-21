# Cassette — OPERATING MODES & SEQUENCES

**Document:** Cassette-MODES-001
**Revision:** 1.1
**Date:** 2026-04-20
**Classification:** CONFIDENTIAL
**Status:** Released

**Companion documents:** Cassette-CTRL-001 Rev 1.1 · Cassette-SIS-001 Rev 1.1 · Cassette-INT-001 Rev 3.0 · Cassette-ELEC-001 Rev 1.2 · Cassette-COOL-002 Rev 1.0 · Cassette-CDUSKID-001 Rev 1.0 · Cassette-FIRE-001 Rev 1.2

| Rev | Date       | Description                                                                             |
|-----|------------|-----------------------------------------------------------------------------------------|
| 1.0 | 2026-04-20 | Initial release. Ten operating modes: COLD_OFF, COLD_START, WARM_START, NORMAL, DEGRADED, HOT_STANDBY, SERVICE, PLANNED_SHUTDOWN, EMERGENCY_SHUTDOWN, BLACK_START. Full transition state machine, step-by-step sequences with elapsed-time budgets, per-mode interlock matrix, and failover procedures for genset, CDU pumps, and BMS. |
| **1.1** | **2026-04-20** | **Companion documents updated to Rev 3.0 baseline. External CDU skid (COOL-002/CDUSKID-001) now referenced explicitly in COLD_START sequence (skid primary pump start precedes rack energize), HOT_STANDBY (buffer tank pre-charge), and SERVICE modes (skid filter/strainer swap paths). EMERGENCY_SHUTDOWN updated to include skid isolation valve close command and QD dry-break isolation. Mode transition timings preserved; no changes to state machine structure.** |

**Prepared by:** Scott Tomsu · CEO / Chief Engineer
scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana

---

## TABLE OF CONTENTS

- §1  Scope & Concept of Operations
- §2  Mode State Machine — Overview
- §3  Mode 0 — COLD_OFF
- §4  Mode 1 — COLD_START
- §5  Mode 2 — WARM_START
- §6  Mode 3 — NORMAL
- §7  Mode 4 — DEGRADED
- §8  Mode 5 — HOT_STANDBY
- §9  Mode 6 — SERVICE
- §10 Mode 7 — PLANNED_SHUTDOWN
- §11 Mode 8 — EMERGENCY_SHUTDOWN
- §12 Mode 9 — BLACK_START
- §13 Failover Sequences
- §14 Mode-to-Mode Interlock Matrix
- §15 Timing Budgets
- §16 Open Items

---

## §1  SCOPE & CONCEPT OF OPERATIONS

### Scope

This document defines every operating mode of the Cassette edge AI compute node, the permitted transitions between them, and the detailed step-by-step sequences the site orchestrator (L3 Ignition SCADA) executes during each transition.

### Concept of Operations

The deployed unit is a six-subsystem coordinated machine:

1. **Gensets** — two Cat G3520K natural gas gensets, 2N redundant
2. **Switchgear** — 800 VDC main bus + 480 VAC auxiliary
3. **Absorption chiller** — produces chilled water from genset waste heat
4. **CDU skid** — primary PG25 loop to cassette, secondary CHW from chiller
5. **Munters skid** — interior humidity control via process air loop
6. **Cassette** — the sealed compute module (15 racks, 1.6–2.2 MW IT)

Each subsystem has its own local interlocks and local autonomous behavior, but none of them can safely start or stop in isolation. The orchestrator executes coordinated sequences that ensure dependencies are met at every step — for example, you cannot start the cassette before the CDU has established flow, and you cannot start the CDU until the chiller is producing CHW, and the chiller needs the gensets running. The coordination is what this document defines.

### Design Principles

1. **Every mode has a defined steady state.** Whatever mode is active, there is a single consistent configuration that is being maintained.
2. **Every transition has an acceptance test.** A mode change does not complete until the orchestrator verifies the expected state has been reached.
3. **Every transition has a reversal path.** If a step fails, there is a defined abort sequence that returns the system to a known safe state (typically the prior mode or HOT_STANDBY or EMERGENCY_SHUTDOWN).
4. **Operator intent is never assumed.** Mode changes require explicit operator command at the HMI (local, remote, or mobile) with privilege authentication.
5. **The SIS overrides everything.** Any safety trip (SIS-001) forces EMERGENCY_SHUTDOWN regardless of current mode. The orchestrator cannot suppress or defer this.

---

## §2  MODE STATE MACHINE — OVERVIEW

### Modes at a Glance

| Mode | Code | Description | Cassette IT | Gensets | CDU | Chiller | Munters |
|------|------|-------------|-------------|---------|-----|---------|---------|
| 0 | COLD_OFF | Fully powered down | OFF | OFF | OFF | OFF | OFF |
| 1 | COLD_START | Bringing gensets online | OFF | 1 starting | OFF | OFF | ON |
| 2 | WARM_START | Cooling established, racks powering | ramping | 1 running | flow est. | producing | ON |
| 3 | NORMAL | Full production | full | 1 at load | full flow | full CHW | ON |
| 4 | DEGRADED | Reduced-capacity operation | reduced | 1 only | N-only | N-only | ON |
| 5 | HOT_STANDBY | Everything running, workload paused | idle | 1 at low | flow held | idle | ON |
| 6 | SERVICE | One or more skids isolated for PM | varies | varies | varies | varies | varies |
| 7 | PLANNED_SHUTDOWN | Orderly shutdown | spinning down | spinning down | cooling down | off | ON |
| 8 | EMERGENCY_SHUTDOWN | Hard stop | tripped | tripped | off | off | off |
| 9 | BLACK_START | Recovery from uncontrolled stop | off | starting | off | off | starting |

### Permitted Transitions

```
                    ┌──────── COLD_OFF ─────────┐
                    │             ↑             │
                    │             │             │
                    ▼             │             ▼
               COLD_START ──→ [abort] ──→ EMERGENCY_SHUTDOWN
                    │             ↑             ↑
                    ▼             │             │
               WARM_START ─────[fail]──────────┤
                    │             ↑             │
                    ▼             │             │
     ┌─────────→ NORMAL ←─────→ DEGRADED ──────┤
     │              │  ↓          │             │
     │              │  ↓          ↓             │
     │          HOT_STANDBY ←→  SERVICE         │
     │              │             │             │
     │              ▼             ▼             │
     └────── PLANNED_SHUTDOWN ────┘             │
                    │                           │
                    ▼                           │
                COLD_OFF                        │
                                                │
            BLACK_START ────────────────────────┘
                 │
                 ▼
           COLD_START (continue)
```

### Mode Transition Rules

| From | To | Trigger | Privilege | Typical duration |
|------|-----|---------|-----------|------------------|
| COLD_OFF | COLD_START | Operator command | Operator | — |
| COLD_START | WARM_START | Cooling established (see §4) | Automatic | 12–18 min |
| WARM_START | NORMAL | Rack power stable, IT load enabled | Automatic | 6–10 min |
| NORMAL | DEGRADED | Any permitted degradation trigger (§7) | Automatic | 30 s – 2 min |
| NORMAL | HOT_STANDBY | Operator command | Operator | 1–3 min |
| NORMAL | SERVICE | Operator command | Supervisor | 5–15 min |
| NORMAL | PLANNED_SHUTDOWN | Operator command | Supervisor | — |
| Any | EMERGENCY_SHUTDOWN | SIS trip, E-stop, or any critical alarm | Automatic | immediate |
| EMERGENCY_SHUTDOWN | BLACK_START | Manual reset after root-cause confirmed | Engineer + SIS key | — |
| BLACK_START | COLD_START | Power restored, breakers set | Automatic | 3–6 min |
| DEGRADED | NORMAL | Fault cleared, redundancy restored | Automatic | 30 s – 2 min |
| HOT_STANDBY | NORMAL | Operator command | Operator | 1–3 min |
| SERVICE | NORMAL | Service window closed, equipment re-commissioned | Supervisor | 5–15 min |
| PLANNED_SHUTDOWN | COLD_OFF | Residual heat bled down | Automatic | 20–40 min |

### Privilege Levels

| Level | Role | Mode transitions permitted |
|-------|------|----------------------------|
| Operator | Site operator / NOC technician | NORMAL ↔ HOT_STANDBY, NORMAL → DEGRADED ack |
| Supervisor | Shift supervisor, customer ops lead | NORMAL → SERVICE, NORMAL → PLANNED_SHUTDOWN |
| Engineer | ADC field engineer, integrator | COLD_OFF → COLD_START, BLACK_START initiation |
| SIS Key | Physical key + authenticated engineer | EMERGENCY_SHUTDOWN reset |

---

## §3  MODE 0 — COLD_OFF

### Steady State

| Subsystem | State |
|-----------|-------|
| Gensets | Shut down; fuel valves closed; coolant circulating at ambient |
| Switchgear | Main breaker open, locked out and tagged |
| Absorption chiller | Off; solution pump off; isolated |
| CDU skid | Off; pumps stopped; fluid at ambient temperature |
| Munters skid | Off; rotor parked |
| Cassette | Unpowered; Jetson BMS off; fire suppression armed on 24 VDC UPS |
| 24 VDC life-safety UPS | On; SIS and VESDA active; CO₂/dust monitoring active |

### Entry Conditions

- From PLANNED_SHUTDOWN §10 after residual heat bled below 35 °C on primary loop
- Initial installation after commissioning tests complete
- After BLACK_START → COLD_START → PLANNED_SHUTDOWN chain if commissioning fails

### What Happens in This Mode

Essentially nothing — the unit is dormant. The 24 VDC UPS keeps the SIS, VESDA, and basic BMS alive so that fire/gas/leak detection remains operational. The BMS reports COLD_OFF status to any reachable L3 / L4 endpoint at 1 minute intervals. Unit is safe to perform extended service (full overhauls, rebuilds).

### Exit Conditions

- Operator-initiated transition to COLD_START (§4)

---

## §4  MODE 1 — COLD_START

### Purpose

Sequenced startup of auxiliary and primary infrastructure to the point where the cassette can safely begin energizing racks.

### Pre-Start Checklist (automated verification)

The orchestrator verifies before any action:

| Item | Check |
|------|-------|
| 24 VDC UPS | State of charge ≥ 80% |
| SIS | Armed, no active trips, no bypassed safety functions |
| VESDA | No pre-alarm states, sampling flow normal |
| Gas detect (all 13 points) | All within normal range, no faults |
| Gas inlet | Pressure ≥ 35 psi, composition within spec (if analyzer present) |
| Cassette seal | Last pressure decay test within 12 months |
| CDU skid fluid | PG25 level in expansion tank 60–80%, no leak detection alarms |
| Munters | Filter ΔP within range |
| Network | L2 Gateway reachable, L3 orchestrator command path verified |
| Time sync | PTP grandmaster locked to GPS |

### Sequence Steps

**Elapsed time from operator command to end of COLD_START: target 12–18 minutes**

| Step | Elapsed (mm:ss) | Action | Acceptance |
|------|-----------------|--------|------------|
| 1.0  | 00:00           | Operator commands COLD_START at L2 HMI | Privilege verified |
| 1.1  | 00:15           | Orchestrator executes pre-start checklist | All items pass |
| 1.2  | 00:30           | Start Munters skid (needs to dry interior air before fluid circulation starts) | Rotor at speed, reactivation heater at 50% |
| 1.3  | 01:00           | Command Genset A start sequence via EMCP 4.4 | Engine cranking |
| 1.4  | 01:30           | Genset A at rated speed (1,800 rpm), alternator building voltage | Voltage 800 V DC ± 2% |
| 1.5  | 02:00           | Close Genset A output breaker to the bus | Bus energized |
| 1.6  | 02:15           | Bender IMD self-test, insulation resistance > 5 MΩ | Pass |
| 1.7  | 02:30           | Auxiliary 480 VAC energized (for CDU, Munters, chiller) | Aux bus live |
| 1.8  | 03:00           | Start CDU primary circulation pumps at 20% speed (low flow circulation) | Flow detected, no leak alarms |
| 1.9  | 03:30           | Bleed air from CDU primary loop via automatic air vents | No air-lock alarm |
| 1.10 | 04:30           | Ramp CDU primary pumps to 40% (establish nominal low flow) | 900 LPM flow achieved |
| 1.11 | 05:00           | Start absorption chiller heat input (genset waste heat routing valve opens) | Heat recovery exchanger flowing |
| 1.12 | 06:00           | Chiller solution pump starts, LiBr begins circulation | Solution pump status OK |
| 1.13 | 08:00           | Chiller generator T reaches setpoint, evaporator begins cooling | CHW supply T trending toward 12 °C |
| 1.14 | 10:00           | CHW supply T reaches 12 °C | ≤ 12 °C for 60 s |
| 1.15 | 10:30           | CDU secondary (CHW) flow established | 2,180 LPM CHW |
| 1.16 | 11:00           | CDU primary loop temperature check: return at 45 °C within 2 °C | ≤ 47 °C primary return with no load |
| 1.17 | 12:00           | Start Genset B in standby hot mode (spinning, synchronized, breaker open) | Genset B synchronized, ready to close |
| 1.18 | 12:30           | Arm 800 VDC bus for rack energization | Bus ready signal to Cassette BMS |
| 1.19 | 13:00           | Orchestrator transitions to WARM_START | — |

### Abort Conditions

Any of the following aborts COLD_START and transitions to COLD_OFF (if genset not yet synced) or PLANNED_SHUTDOWN (if genset already on the bus):

- Genset A fails to start within 90 s of start command
- Gas detection alarm (any LEL, H₂S, CO over threshold)
- Insulation resistance fail at step 1.6
- CDU leak detection alarm at any step
- CHW supply T does not reach 12 °C within 12 minutes
- Any SIS trip (immediate EMERGENCY_SHUTDOWN, not abort)

---

## §5  MODE 2 — WARM_START

### Purpose

Bring the cassette racks online in an orderly sequence, verifying each rack is thermally and electrically healthy before enabling GPU workload.

### Pre-Conditions (inherited from COLD_START)

- 800 VDC bus energized and stable
- CDU primary flow at 40% (900 LPM), return T ≤ 47 °C
- CHW supply at ≤ 12 °C
- Munters dry air circulation established
- All L1 PLCs reporting healthy

### Sequence Steps

**Elapsed time from WARM_START entry to NORMAL transition: target 6–10 minutes**

| Step | Elapsed (mm:ss) | Action | Acceptance |
|------|-----------------|--------|------------|
| 2.0  | 00:00           | Close R15 (storage + mgmt) rack DC breaker | Jetson primary and secondary boot |
| 2.1  | 01:00           | Jetson BMS acknowledges bus voltage, publishes ready | BMS state = READY |
| 2.2  | 01:30           | Close R14 (InfiniBand) rack DC breaker | QM9700 switches boot |
| 2.3  | 02:30           | Close compute rack breakers R1–R3 (first group of three) | All Delta shelves report OK |
| 2.4  | 03:00           | Ramp CDU primary pumps to 60% (1,300 LPM) | Flow increase confirmed |
| 2.5  | 03:30           | Close compute rack breakers R4–R6 | Delta shelves OK |
| 2.6  | 04:00           | Ramp CDU primary pumps to 75% (1,600 LPM) | Flow OK |
| 2.7  | 04:30           | Close compute rack breakers R7–R9 | Delta shelves OK |
| 2.8  | 05:00           | Close compute rack breakers R10–R13 | Delta shelves OK |
| 2.9  | 05:30           | Ramp CDU primary pumps to 100% (2,100 LPM NVL72 nominal) | Flow at setpoint |
| 2.10 | 06:00           | Verify per-rack cold plate supply T ≤ 45 °C, return T ≤ 50 °C (no load yet) | All racks pass |
| 2.11 | 06:30           | BMS verifies all rack internal diagnostics (NVIDIA rack self-test) | All racks healthy |
| 2.12 | 07:00           | Enable InfiniBand fabric and external uplink | Links up, fabric discovery complete |
| 2.13 | 07:30           | Signal to site orchestrator: IT_READY | State published |
| 2.14 | 08:00           | Orchestrator transitions to NORMAL; workload scheduler enabled | — |

### Abort Conditions

- Any rack fails to power up (self-check failure): skip that rack, continue with remaining; if > 2 racks fail, abort to PLANNED_SHUTDOWN
- Cold plate supply T > 45 °C at any step: halt step, reduce flow setpoint, re-verify; if unresolved in 2 min, abort
- Any leak detection alarm: trip affected rack only, continue others if possible
- Any SIS trip: EMERGENCY_SHUTDOWN

---

## §6  MODE 3 — NORMAL

### Purpose

Full production operation. This is the intended steady state for >95% of operating hours.

### Steady State

| Subsystem | State |
|-----------|-------|
| Genset A | Running at load, ~45-85% loaded depending on workload |
| Genset B | Hot standby (spinning at rated speed, breaker open, ready for <5 s failover) |
| Switchgear | Main breaker closed, all feeders live |
| Absorption chiller | Producing CHW at 7–12 °C, flow 2,180 LPM |
| CDU skid | Primary 2,100–2,350 LPM @ 45 °C supply, pumps N+1, buffer tank 5 °C stratified |
| Munters skid | Interior RH 30–45% |
| Cassette | All 15 racks operational, workload scheduler dispatching |

### Ongoing Activities

- **Feedforward control** (CTRL-001 §11) actively modulating CDU flow, buffer tank, chiller heat demand based on workload forecast
- **Predictive maintenance models** (CTRL-001 §12) evaluating every asset at 1 Hz
- **Historian** logging at 1 Hz fast, 1 min trend
- **Alarms** processed per ISA-18.2
- **SIS** armed and watching

### Expected Performance

| Metric | Target | Trip threshold |
|--------|--------|----------------|
| Cassette IT load | 1.6–2.2 MW sustainable | — |
| Gas consumption | ~40 Mscf/day at full load | — |
| Primary loop return T | ≤ 59 °C (NVL72) / ≤ 60 °C (CPX) | > 60 °C → DEGRADED |
| CHW return T | ≤ 18 °C | > 20 °C → DEGRADED |
| Interior humidity | 30–50% RH | > 60% sustained → alarm |
| PUE (site level) | ≤ 1.12 | — |
| CHP efficiency | ≥ 80% | — |

### Transition Triggers Out of NORMAL

| Trigger | To mode |
|---------|---------|
| Genset A fault | DEGRADED (Genset B takes over, then Genset A becomes standby when restored) |
| CDU primary pump A or B fault | DEGRADED (N+1 remaining pump holds) |
| Chiller fault | DEGRADED (see §7.3 — cooling path varies) |
| Munters fault | DEGRADED (interior RH trends higher; bounded) |
| Operator command | HOT_STANDBY, SERVICE, or PLANNED_SHUTDOWN |
| SIS trip | EMERGENCY_SHUTDOWN |

---

## §7  MODE 4 — DEGRADED

### Purpose

Continue production at reduced capacity when any subsystem has failed or been isolated but the remaining system can still run.

### Degradation Scenarios

**§7.1 Single Genset (Genset A fault, Genset B active)**

Automatic response:
1. Genset A protective trip at L1 (EMCP)
2. Switchgear 27/81 undervoltage/frequency triggers on sensing the fault
3. Genset B breaker closes within 2–5 s (Genset B was already spinning in hot standby)
4. Bus ride-through provided by Delta in-rack BBUs (10 s capacity)
5. Cassette BMS confirms bus stable
6. Orchestrator enters DEGRADED, alerts operator
7. Work order generated for Genset A repair

Operational impact: none immediate. 2N becomes N (loss of electrical redundancy). Cassette continues at full load. If second genset fails before first is repaired, EMERGENCY_SHUTDOWN.

**§7.2 Single CDU Pump (Pump A fault, Pump B active)**

Automatic response:
1. Pump A low-flow protective trip
2. Pump B ramps to 100% within 3 s (was at 0% standby)
3. Flow re-established within 5 s
4. Cassette BMS confirms flow, no rack thermal excursion
5. Orchestrator enters DEGRADED, alerts operator
6. Work order generated for Pump A repair

Operational impact: loss of pump redundancy (N+1 → N). Continue at full load. If second pump fails, cassette must be taken to PLANNED_SHUTDOWN quickly.

**§7.3 Chiller Fault**

Absorption chiller has the fewest options:
- If site-provided backup CHW available (facility cooling tower loop): switch CHW source, continue at full load
- If no backup CHW: cassette must derate to IT load that can be cooled by thermal buffer tank reserves (~30–90 min of full load) then transition to PLANNED_SHUTDOWN
- Alternative: if absorption chiller failed but gensets are running, waste heat still needs to go somewhere — heat rejection to atmosphere via emergency radiator (if fitted) or genset must throttle

This scenario is why Cat G3520K gensets may be fitted with both jacket water heat exchangers (primary for heat recovery) and emergency radiators (backup heat rejection). Specify at procurement — open item MO-01.

**§7.4 Munters Skid Fault**

Interior humidity rises toward ambient. Bounded at 55–60% RH for Gulf Coast (Lafayette) ambient. No immediate thermal risk at cold plates (dew point well below cold-plate surface T of ~45 °C). Cassette continues at full load. Munters scheduled for maintenance within 72 hours.

**§7.5 Partial Rack Failure**

One or more compute racks offline (Delta shelf fault, internal rack self-test fail). Orchestrator isolates affected rack (close rack breaker, close UQD isolation valves), logs work order, continues operation on remaining racks. If > 3 racks fail, consider PLANNED_SHUTDOWN.

### Exit from DEGRADED

Fault cleared + redundancy restored → Orchestrator performs re-commissioning verification → transition back to NORMAL.

---

## §8  MODE 5 — HOT_STANDBY

### Purpose

Keep the site fully powered and thermally conditioned, but pause GPU workload. Used during workload gaps, scheduled operator attention, or pre-PLANNED_SHUTDOWN cooldown.

### Steady State

| Subsystem | State |
|-----------|-------|
| Genset A | Running at minimum load (~5% for heat) |
| Genset B | Hot standby |
| CDU skid | Primary at 40% flow (low circulation to prevent stagnation) |
| Chiller | At minimum heat input, producing light cooling |
| Cassette | Racks powered (DC breakers closed), GPUs idle, no workload dispatched |

### Transition into HOT_STANDBY (from NORMAL)

Target duration: 1–3 min

| Step | Action |
|------|--------|
| 5.1 | Workload scheduler pause requested; current batch completes within bounded time (cooperative) |
| 5.2 | New workload dispatching disabled |
| 5.3 | When all jobs drain, signal GPUs to idle state |
| 5.4 | CDU primary flow ramps from 100% to 40% over 30 s |
| 5.5 | Chiller heat demand reduced to minimum |
| 5.6 | Genset A throttles to ~5–10% load |
| 5.7 | Orchestrator state = HOT_STANDBY |

### Return from HOT_STANDBY (to NORMAL)

Ramp-up mirrors the above in reverse. Workload dispatching enabled only after CDU flow reaches 100% and system is verified thermally ready.

---

## §9  MODE 6 — SERVICE

### Purpose

Isolate one or more subsystems for scheduled maintenance while the remainder of the unit continues operating at reduced capability.

### Service Sub-Modes

| Sub-mode | Isolated skid(s) | Impact |
|----------|------------------|--------|
| SERVICE_GENSET_A | Genset A | Genset B carries full load; 2N → N temporarily |
| SERVICE_GENSET_B | Genset B | Genset A carries full load; 2N → N |
| SERVICE_CDU_FILTER | Duplex filter swap | Switch to standby filter, swap service filter, no IT impact |
| SERVICE_MUNTERS | Munters skid | Interior humidity rises; 24-hour service window |
| SERVICE_CHILLER | Absorption chiller | Requires backup CHW or cassette derate |
| SERVICE_CASSETTE | Full cassette isolation | Cassette in COLD_OFF; rest of plant in HOT_STANDBY for rapid restart |

### Entry Procedure

1. Supervisor requests SERVICE mode at L2 HMI, specifies sub-mode
2. Orchestrator verifies prerequisites:
   - For genset service: second genset healthy, 72 hr since last SERVICE of same asset
   - For CDU filter swap: standby filter ΔP < 15 kPa (not loaded)
   - For Munters / chiller: cassette operating state tolerant of reduced capability
3. Orchestrator issues isolation commands:
   - Genset: open breaker, close fuel valve, set manual/off selector
   - CDU filter: sequence valves for standby-only flow, bleed service filter
   - Munters: close dampers, spin rotor to park position, isolate power
   - Chiller: divert heat to alternate path (emergency radiator or secondary CHW)
4. Lockout/tagout (LOTO) engaged — service key switch activates, logged in BMS
5. Orchestrator state = SERVICE, technician cleared to work

### Exit Procedure

1. Technician signals service complete at field HMI + removes LOTO
2. Orchestrator runs re-commissioning test suite on the serviced subsystem
3. If pass: re-integrate subsystem (close breaker / open valves / start equipment)
4. Verify stable operation for ≥ 5 minutes
5. Orchestrator returns to NORMAL or DEGRADED based on other system state

---

## §10  MODE 7 — PLANNED_SHUTDOWN

### Purpose

Orderly controlled shutdown of the entire unit, preserving equipment health and allowing residual heat to bleed down safely.

### Entry Triggers

- Supervisor command at L2 HMI
- Long-duration fault that cannot be corrected in DEGRADED mode
- Scheduled site maintenance / relocation / customer request

### Sequence Steps

**Target duration: 20–40 min**

| Step | Elapsed (mm:ss) | Action | Acceptance |
|------|-----------------|--------|------------|
| 7.1  | 00:00           | Supervisor commands PLANNED_SHUTDOWN | Privilege verified |
| 7.2  | 00:30           | Workload scheduler pause: drain running jobs with 5 min grace period | Jobs completed or checkpointed |
| 7.3  | 05:30           | GPUs transition to idle | Load < 10 kW per rack |
| 7.4  | 06:00           | Ramp down racks in reverse order R13 → R1 | Rack-by-rack, verify each |
| 7.5  | 10:00           | Open rack DC breakers R1–R13 | Breakers open, no arc events |
| 7.6  | 10:30           | Open InfiniBand (R14) and management (R15) rack breakers | BMS remains powered via 24 VDC UPS |
| 7.7  | 11:00           | Reduce CDU primary flow to 30% (circulation only for heat bleed-off) | Flow at minimum |
| 7.8  | 12:00           | Reduce absorption chiller heat input to minimum | Chiller at idle |
| 7.9  | 15:00           | Throttle Genset A to minimum load | Engine at low load |
| 7.10 | 20:00           | Primary loop return T < 40 °C verified (heat bled) | Return ≤ 40 °C |
| 7.11 | 25:00           | Stop CDU primary pumps | Pumps stopped |
| 7.12 | 25:30           | Stop Munters | Rotor parked |
| 7.13 | 26:00           | Open 800 VDC main breaker | Bus de-energized |
| 7.14 | 26:30           | Open Genset A output breaker, initiate shutdown sequence | EMCP cooldown cycle (5 min idle before stop) |
| 7.15 | 32:00           | Genset A stopped, fuel valves closed | Gensets at rest |
| 7.16 | 33:00           | Primary loop residual check — no leaks, no alarms | Clean state |
| 7.17 | 35:00           | Orchestrator transitions to COLD_OFF | — |

### Abort

Operator can abort PLANNED_SHUTDOWN during steps 7.1–7.4 (returns to NORMAL). After step 7.5, abort only possible via BLACK_START sequence (full restart).

---

## §11  MODE 8 — EMERGENCY_SHUTDOWN

### Purpose

Immediate hard stop in response to a safety event. Protects personnel, equipment, and environment. Accepts that equipment may be stressed by the abrupt stop — this is the cost of safety.

### Triggers

| Source | Event | Automatic / Operator |
|--------|-------|----------------------|
| SIS | Gas leak (LEL, H₂S, CO) confirmed | Automatic |
| SIS | Fire detected (VESDA Fire 1 or 2) | Automatic |
| SIS | Arc flash detected | Automatic |
| SIS | Loss of essential services (fuel, coolant, power) | Automatic |
| Operator | E-stop pressed at any ECP (4 buttons) | Operator |
| Platform | Platform-wide E-stop asserted | Automatic |
| BMS | Cascade safety interlock (multiple simultaneous critical alarms) | Automatic |

### Sequence (all parallel — no sequential dependencies)

Target elapsed time to safe state: **< 5 seconds**

| Action | Mechanism | Time |
|--------|-----------|------|
| Trip main 800 VDC breaker | SIS-driven relay on trip coil | < 100 ms |
| Close fuel shutoff valves at gensets | SIS-driven solenoid (fail-closed) | < 500 ms |
| Stop Genset A and B (emergency stop) | EMCP emergency stop input | < 1 s |
| Stop CDU primary pumps | Loss of 480 VAC from aux bus + SIS-driven stop | < 500 ms |
| Close cassette ECP fluid isolation valves | Belimo motorized, SIS-driven | < 10 s |
| Stop Munters, parked rotor | SIS-driven stop | < 2 s |
| Energize strobes at all ECPs | 24 VDC UPS | < 100 ms |
| Discharge Novec 1230 (if fire) | Fire control panel, independent of BMS | < 10 s (after 30 s pre-discharge) |
| Open over-pressure vent damper | Novec discharge interlock | < 1 s |
| Notify platform SCADA | BMS publishes state | < 1 s |
| Notify cloud | L3 orchestrator publishes event | < 10 s |

### Post-EMERGENCY_SHUTDOWN State

| Subsystem | State |
|-----------|-------|
| Cassette | All breakers open, racks dark, cold plates static, ECPs isolated |
| Gensets | Stopped, fuel valves closed, blocked against restart |
| CDU | Pumps stopped, fluid static, no flow |
| Chiller | Off, solution pump stopped |
| Munters | Off, rotor parked |
| 24 VDC UPS | On; SIS, VESDA, BMS in monitoring mode, alarms latched |

### Reset Procedure

Resetting EMERGENCY_SHUTDOWN requires:

1. Root-cause investigation by authorized engineer
2. Physical inspection of all affected equipment
3. SIS key + dual authentication (engineer + supervisor)
4. SIS reset procedure per CAS-SIS-001 §11
5. Once SIS cleared, operator commands BLACK_START (§12)

An EMERGENCY_SHUTDOWN cannot be reset by operator alone. This is a deliberate gate — if the SIS tripped, something needed checking.

---

## §12  MODE 9 — BLACK_START

### Purpose

Recovery from EMERGENCY_SHUTDOWN or total power loss. Brings the unit from cold, de-energized state back to COLD_START entry conditions.

### Pre-Conditions

- SIS cleared and reset (CAS-SIS-001 §11)
- Physical inspection of all skids complete, no damage
- 24 VDC UPS state of charge ≥ 70%
- Gas supply pressure available

### Sequence Steps

**Target duration: 3–6 minutes to COLD_START handoff**

| Step | Elapsed (mm:ss) | Action |
|------|-----------------|--------|
| 9.1  | 00:00           | Engineer initiates BLACK_START at L2 HMI with SIS key |
| 9.2  | 00:30           | Orchestrator executes BLACK_START_CHECKLIST (same as COLD_START pre-check) |
| 9.3  | 01:00           | Genset A crank from 24 VDC starter battery |
| 9.4  | 01:30           | Genset A at rated speed, voltage building |
| 9.5  | 02:00           | Close Genset A breaker to energize aux 480 VAC bus |
| 9.6  | 02:30           | Aux bus live, IMD self-test |
| 9.7  | 03:00           | Hand off to COLD_START sequence §4 from step 1.7 |

BLACK_START is essentially a shortened COLD_START — it starts mid-sequence after the initial genset ignition, since pre-start checks have already been performed by the engineer.

### Failure Mode

If Genset A fails to start from black condition (e.g., starter battery depleted, fuel supply lost):
- Genset B is attempted
- If both fail, unit remains in EMERGENCY_SHUTDOWN until external utility power or a portable genset is connected for aux 480 VAC, then recommission per commissioning procedure

---

## §13  FAILOVER SEQUENCES

### §13.1  Genset A → Genset B Failover

**Trigger:** Genset A protective trip (any cause) while on the bus

| Step | Elapsed (ms) | Action |
|------|--------------|--------|
| F1.0 | 0            | Genset A protective trip (overspeed, underspeed, overload, oil P, jacket T, etc.) |
| F1.1 | +10          | Genset A output breaker opens |
| F1.2 | +50          | Switchgear 27/81 undervoltage relay picks up |
| F1.3 | +100         | Genset B (already spinning at 1,800 rpm, synchronized, breaker open) |
| F1.4 | +500         | Genset B breaker closes (synchrocheck verified) |
| F1.5 | +1,000       | Bus voltage stable at 800 V DC ± 2% |
| F1.6 | +2,000       | Cassette BMS confirms bus; Delta BBUs had been holding load, now recharge |
| F1.7 | +5,000       | Orchestrator enters DEGRADED, alerts operator |
| F1.8 | +30,000      | Automated diagnostic runs on Genset A to identify fault |
| F1.9 | varies       | Work order generated |

### §13.2  CDU Pump A → Pump B Failover

**Trigger:** Pump A protective trip or VFD fault

| Step | Elapsed (ms) | Action |
|------|--------------|--------|
| F2.0 | 0            | Pump A fault |
| F2.1 | +50          | CDU PLC detects fault via VFD fault bit + flow sensor |
| F2.2 | +100         | Pump B VFD ramp command (pump B was at 0% standby) |
| F2.3 | +3,000       | Pump B at full speed, flow restored |
| F2.4 | +4,000       | CDU PLC verifies flow in nominal range |
| F2.5 | +5,000       | Orchestrator enters DEGRADED, alerts operator |

Bridging during the 3-4 second flow dip: thermal buffer tank absorbs heat with no cold-plate T rise at the cassette.

### §13.3  Jetson BMS A → BMS B Failover

**Trigger:** Heartbeat loss from active Jetson

| Step | Elapsed (ms) | Action |
|------|--------------|--------|
| F3.0 | 0            | Heartbeat missed |
| F3.1 | +100         | Missed heartbeat threshold (2 consecutive at 50 ms interval) |
| F3.2 | +150         | Keepalived fails over VRRP virtual IP |
| F3.3 | +200         | BMS B takes primary role |
| F3.4 | +500         | OPC UA clients reconnect |
| F3.5 | +1,000       | Grafana dashboards update, all tags current |

State continuity: InfluxDB replication means <5 s of data loss across failover.

### §13.4  Orchestrator / Gateway Failover

**Trigger:** Ignition Gateway primary unresponsive

| Step | Elapsed | Action |
|------|---------|--------|
| F4.0 | 0       | Primary unresponsive |
| F4.1 | +5 s    | Standby Ignition Gateway detects via Gateway Network heartbeat loss |
| F4.2 | +10 s   | Standby promotes to primary, takes over OPC UA server role |
| F4.3 | +20 s   | Southbound L1 connections re-establish |
| F4.4 | +30 s   | HMI clients reconnect |

---

## §14  MODE-TO-MODE INTERLOCK MATRIX

For the orchestrator: a transition from any source mode to any target mode is permitted only if every interlock in the target mode is satisfied.

| Interlock | Checked in modes | Prerequisite |
|-----------|------------------|--------------|
| I-01 Gas supply OK | All except COLD_OFF, EMERGENCY_SHUTDOWN | Inlet pressure ≥ 35 psi, no gas alarms |
| I-02 24 VDC UPS healthy | All | SOC ≥ 70%, charger OK |
| I-03 SIS armed, no trips | All except COLD_OFF | SIS self-test pass, no bypasses |
| I-04 VESDA operating | All except COLD_OFF | Sample flow in range, no pre-alarm |
| I-05 Primary loop tight | NORMAL, WARM_START, DEGRADED | No leak detection alarms, expansion tank level OK |
| I-06 Genset A or B available | NORMAL, WARM_START, DEGRADED | Starter OK, fuel OK, no persistent faults |
| I-07 Chiller or alternate CHW | NORMAL | Chiller OK or backup loop connected |
| I-08 CHW supply T ≤ 12 °C | WARM_START entry, NORMAL | Measured supply T |
| I-09 Bus insulation > 5 MΩ | WARM_START, NORMAL | IMD reading |
| I-10 Cassette seal verified | All when sealed | Last decay test within 12 months |
| I-11 Munters operating | WARM_START, NORMAL, DEGRADED | Process flow > 500 SCFM |
| I-12 PTP locked | All | Grandmaster state |
| I-13 L2 Gateway reachable | All except COLD_OFF | Heartbeat received in last 10 s |
| I-14 No unacknowledged Urgent alarms | NORMAL | Alarm state |

---

## §15  TIMING BUDGETS

### Startup to Production

| Transition | Nominal | Target SLA | Out of SLA |
|------------|---------|------------|------------|
| COLD_OFF → NORMAL | 22 min | 30 min | report |
| BLACK_START → NORMAL | 28 min | 40 min | report |
| HOT_STANDBY → NORMAL | 2 min | 5 min | report |
| SERVICE → NORMAL | 10 min | 20 min | report |

### Shutdown

| Transition | Nominal | Target SLA |
|------------|---------|------------|
| NORMAL → PLANNED_SHUTDOWN → COLD_OFF | 35 min | 45 min |
| Any → EMERGENCY_SHUTDOWN | < 5 s | < 10 s |

### Failover

| Event | Nominal | Target SLA |
|-------|---------|------------|
| Genset A fault → B | 5 s | 10 s |
| CDU pump fault → B | 3 s | 10 s |
| BMS fault → B | 200 ms | 1 s |
| Gateway fault → B | 20 s | 60 s |

---

## §16  OPEN ITEMS

| ID | Priority | Description | Owner | Notes |
|----|----------|-------------|-------|-------|
| MO-01 | P-0 | Cat G3520K emergency radiator option — required to allow operation during absorption chiller SERVICE window | ADC ↔ Cat | Affects §7.3, §9 |
| MO-02 | P-0 | Workload scheduler pause API — which NVIDIA platform (SLURM, BCM, K8s) and pause semantics | ADC ↔ customer | Affects §8, §10 |
| MO-03 | P-1 | Feedforward control loop gains — commissioning-tuned initial values | ADC engineering | Affects NORMAL mode performance |
| MO-04 | P-1 | Chiller backup CHW source — customer-side decision (cooling tower / dry cooler / air-cooled chiller alternative) | ADC BD ↔ customer | Affects §7.3, SERVICE mode |
| MO-05 | P-1 | Cold plate supply T threshold limit — vendor-specified; used in thermal interlocks | ADC ↔ NVIDIA | Gates I-08 |
| MO-06 | P-2 | Rack startup / shutdown order optimization — current sequence R1→R15 is arbitrary; may optimize for power distribution balance | ADC engineering | Affects WARM_START, PLANNED_SHUTDOWN |
| MO-07 | P-2 | BLACK_START battery sizing — confirm 24 VDC UPS has enough capacity to re-crank genset after extended COLD_OFF | ADC engineering | Gates §12 |
| MO-08 | P-2 | SERVICE mode LOTO electronic interface — integration with customer's electronic lockout system | ADC ↔ integrator | Affects §9 |
| MO-09 | P-3 | Mode transition FSM implementation in Ignition — Python script template vs visual sequence editor | ADC ↔ integrator | Affects development |
| MO-10 | P-3 | Operator training simulator — desktop replica for scenario practice before site deployment | ADC engineering | Affects §6.2 (CTRL-001) |

---

## SUMMARY OF KEY DESIGN DECISIONS

| # | Decision | Rationale |
|---|----------|-----------|
| 1 | Ten explicit modes with a formal state machine | Clarity for operators, integrators, auditors; eliminates ambiguous states |
| 2 | Genset-B-always-hot-spinning in NORMAL | Enables <5 s failover; N-1 electrical redundancy target |
| 3 | CDU pumps N+1 with standby at 0% | Cheaper than parallel operation; 3 s flow dip is within buffer tank coverage |
| 4 | Workload drain with 5 min grace period in PLANNED_SHUTDOWN | Respects cooperative job lifecycle; avoids compute loss |
| 5 | EMERGENCY_SHUTDOWN requires dual-authenticated reset | Forces root-cause investigation; prevents complacency reset |
| 6 | BLACK_START as distinct mode from COLD_START | Different pre-conditions (post-SIS reset vs initial); different failure modes |
| 7 | SERVICE mode per sub-mode rather than generic | Allows different skids to be isolated with scenario-specific interlocks |
| 8 | Predictive maintenance-driven SERVICE scheduling | Integrates with CMMS; operator has days-to-weeks notice, not minutes |
| 9 | 5-second EMERGENCY_SHUTDOWN SLA | Matches SIL-2 requirements for gas-detection-driven ESD |
| 10 | Mode state machine implemented in L3 orchestrator only | L1/L2 don't run sequences; they respond to coordinated commands — keeps complexity in one place |

---

**Cassette-MODES-001 — Operating Modes & Sequences · Rev 1.1 · 2026-04-20**
**Scott Tomsu · scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana**
**CONFIDENTIAL**
