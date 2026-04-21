# Cassette — SAFETY INSTRUMENTED SYSTEM

**Document:** Cassette-SIS-001
**Revision:** 1.1
**Date:** 2026-04-20
**Classification:** CONFIDENTIAL
**Status:** Released

**Companion documents:** Cassette-CTRL-001 Rev 1.1 · Cassette-MODES-001 Rev 1.1 · Cassette-FIRE-001 Rev 1.2 · Cassette-INT-001 Rev 3.0 · Cassette-ECP-001 Rev 3.0 · Cassette-ELEC-001 Rev 1.2 · Cassette-COOL-002 Rev 1.0 · Cassette-CDUSKID-001 Rev 1.0

| Rev | Date       | Description                                                                         |
|-----|------------|-------------------------------------------------------------------------------------|
| 1.0 | 2026-04-20 | Initial release. Applies IEC 61511 / IEC 61508 functional safety framework to the cassette + 4-skid deployment unit. Identifies eight Safety Instrumented Functions (SIFs), assigns SIL targets, specifies sensors and final elements, defines proof-test intervals, and maps compliance with NFPA 87, API RP 14C, and IEC 62443. |
| **1.1** | **2026-04-20** | **Companion documents updated to Rev 3.0 baseline. SIF-04 (coolant leak detection) updated to reflect sealed-PG25 Cassette architecture per INT-001 Rev 3.0 §15 — single-fluid leak detection only (no CHW inside Cassette). Skid-side leak detection (external to Cassette) moved to CDUSKID-001 scope. SIF-05 (genset overspeed), SIF-06 (switchgear protection) references to separate GENSET-001 / SWGR-001 docs noted as pending. No changes to SIL targets or SIF logic.** |

**Prepared by:** Scott Tomsu · CEO / Chief Engineer
scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana

---

## TABLE OF CONTENTS

- §1  Scope & Standards
- §2  Hazard Identification (HAZID Summary)
- §3  Layer of Protection Analysis (LOPA)
- §4  Safety Instrumented Functions (SIFs)
- §5  SIF-01 — Gas Leak Detection & Isolation
- §6  SIF-02 — Fire Detection & Suppression
- §7  SIF-03 — Arc Flash Protection
- §8  SIF-04 — Coolant Leak Isolation
- §9  SIF-05 — Genset Overspeed / Protective Shutdown
- §10 SIF-06 — Switchgear Fault Protection
- §11 SIF-07 — Loss of Cooling Protection
- §12 SIF-08 — Emergency Stop (E-stop)
- §13 Safety System Architecture
- §14 Separation from BPCS
- §15 Proof-Test & Maintenance
- §16 Functional Safety Assessment & Sign-off
- §17 Open Items

---

## §1  SCOPE & STANDARDS

### Scope

This document specifies the Safety Instrumented System (SIS) for the one-cassette edge AI compute deployment unit. The SIS is physically and logically separate from the Basic Process Control System (BPCS) defined in CAS-CTRL-001, and its sole function is to bring the process to a safe state when the BPCS is insufficient to prevent a hazard.

### Applicable Standards

| Standard | Title | Relevance |
|----------|-------|-----------|
| IEC 61511-1:2016 | Functional safety — Safety instrumented systems for the process industry sector | Primary framework |
| IEC 61508:2010 | Functional safety of electrical/electronic/programmable electronic safety-related systems | Device-level SIL certification |
| NFPA 87:2021 | Standard for Fluid Heaters | Applies to genset enclosure hazards |
| NFPA 2001:2022 | Standard on Clean Agent Fire Extinguishing Systems | Novec 1230 (cassette interior) |
| NFPA 30:2024 | Flammable and Combustible Liquids Code | Fuel storage / genset fuel handling |
| NFPA 70:2023 | National Electrical Code, Article 517/518/708 | Hazardous-area classification |
| NFPA 110:2022 | Standard for Emergency and Standby Power Systems | Genset installation |
| API RP 14C:2017 | Analysis, Design, Installation, and Testing of Basic Surface Safety Systems for Offshore Production Platforms | Offshore / upstream oil & gas |
| API RP 500 / 505 | Classification of locations for electrical installations at petroleum facilities | Hazardous-area classification |
| IEC 60079 series | Explosive atmospheres | Zone classification (IEC system) |
| ISA-84.00.01 | Functional Safety: SIS for the Process Industry | US adoption of IEC 61511 |

### Hazardous-Area Assumption

Deployments at upstream oil & gas sites will typically be classified per API RP 500 as:
- Class I, Division 2 around gas-containing equipment (gensets, fuel train, chiller)
- Unclassified inside the cassette (sealed, no hydrocarbons)
- Unclassified in the control cabinets (if inside a purged enclosure or outside hazardous radius)

The SIS design assumes Class I Div 2 for the outdoor equipment; Class I Div 1 upgrades are possible but significantly more expensive.

---

## §2  HAZARD IDENTIFICATION (HAZID SUMMARY)

### Scope of Hazard Identification

Systematic review of all credible hazards associated with the deployment unit. Conducted as a structured HAZID workshop (to be formalized as HAZID-001 during detailed engineering). This section summarizes the findings that drive SIF selection.

### Identified Hazards

| H-ID | Hazard | Cause | Potential consequence | Severity |
|------|--------|-------|----------------------|----------|
| H-01 | Natural gas leak at fuel train | Line / fitting / valve failure | Flash fire, explosion, asphyxiation | Catastrophic |
| H-02 | Genset exhaust CO buildup | Exhaust leak inside enclosure | Personnel CO poisoning, ignition source | Severe |
| H-03 | H₂S from sour gas | Inlet gas composition off-spec | Personnel fatality, equipment corrosion | Catastrophic |
| H-04 | Fire inside cassette | Electrical fault, thermal runaway | GPU / rack damage, toxic smoke | Severe |
| H-05 | Fire inside genset enclosure | Hot surface + fuel leak | Genset destruction, cassette damage | Severe |
| H-06 | Arc flash at switchgear | Breaker failure, insulation breakdown | Personnel fatality, equipment damage | Catastrophic |
| H-07 | 800 VDC shock | Insulation failure + personnel contact | Personnel fatality | Catastrophic |
| H-08 | Primary coolant leak | Manifold / UQD / cold plate failure | Rack damage, slip hazard, glycol release | Moderate |
| H-09 | Chiller LiBr release | Solution tube failure | Corrosive spill, environmental | Moderate |
| H-10 | Overspeed genset | Governor failure | Catastrophic mechanical failure, fire | Catastrophic |
| H-11 | Loss of cooling under full IT load | CDU or chiller failure | GPU thermal damage ($10M+ loss) | Severe |
| H-12 | Loss of ventilation in genset enclosure | Fan failure + gas leak | Gas accumulation, explosion | Catastrophic |
| H-13 | Lightning strike | Weather event | Equipment damage, fire ignition | Moderate |
| H-14 | Vehicle impact | Site access incident | Equipment damage, fluid release | Moderate |
| H-15 | Seismic / marine motion (offshore) | Earthquake, vessel roll | Structural / fluid / electrical | Severe |

### Severity Scale

| Level | Personnel | Environmental | Financial |
|-------|-----------|---------------|-----------|
| Catastrophic | Fatality | > $10M cleanup | > $20M loss |
| Severe | Lost-time injury | $1–10M cleanup | $5–20M loss |
| Moderate | First-aid | $100K–1M cleanup | $0.5–5M loss |
| Minor | No injury | < $100K | < $0.5M loss |

---

## §3  LAYER OF PROTECTION ANALYSIS (LOPA)

### Method

Standard LOPA per CCPS methodology. For each initiating cause, independent protection layers (IPLs) are credited with reducing the event frequency until the Target Mitigated Event Likelihood (TMEL) is met. If credited IPLs are insufficient, a new Safety Instrumented Function (SIF) with an assigned SIL is required.

### Summary by Hazard Category

| Hazard | Initiating event freq (yr⁻¹) | Existing IPLs | Gap | SIF assigned | Required SIL |
|--------|-------------------------------|---------------|------|---------------|--------------|
| H-01 Gas leak → explosion | 1 × 10⁻² | Design, inspection, vent | 10⁻³ | SIF-01 | **SIL 2** |
| H-02 CO accumulation | 5 × 10⁻² | Natural ventilation | 10⁻² | SIF-01 (CO subset) | **SIL 1** |
| H-03 H₂S exposure | 1 × 10⁻² (sour gas sites) | Supplier-provided H₂S scavenger | 10⁻³ | SIF-01 (H₂S subset) | **SIL 2** |
| H-04 Cassette fire | 1 × 10⁻² | Delta shelf protection, VESDA | — | SIF-02 | **SIL 2** |
| H-05 Genset enclosure fire | 1 × 10⁻² | Genset fuel/oil level switches | 10⁻² | SIF-02 (genset subset) | **SIL 1** |
| H-06 Arc flash | 1 × 10⁻³ | Protective relay coordination | 10⁻² | SIF-03 | **SIL 2** |
| H-07 DC shock | 1 × 10⁻² | IMD insulation monitor | 10⁻² | (existing IMD sufficient) | — |
| H-08 Coolant leak | 5 × 10⁻² | TraceTek detection, drip trays | 10⁻¹ | SIF-04 | **SIL 1** |
| H-09 LiBr release | 1 × 10⁻² | Chiller-integral level switches | — | (chiller OEM safety sufficient) | — |
| H-10 Overspeed genset | 1 × 10⁻² | Governor, EMCP protection | — | SIF-05 | **SIL 2** |
| H-11 Loss of cooling | 1 × 10⁻¹ | CDU redundancy, buffer tank | 10⁻¹ | SIF-07 | **SIL 1** |
| H-12 Loss of genset ventilation + gas | 1 × 10⁻³ | Ventilation flow switch | 10⁻² | SIF-01 (linked) | SIL 2 (covered) |

### SIL Assignment Summary

| SIF | Function | Assigned SIL |
|-----|----------|--------------|
| SIF-01 | Gas leak detection & isolation | SIL 2 |
| SIF-02 | Fire detection & suppression | SIL 2 |
| SIF-03 | Arc flash protection | SIL 2 |
| SIF-04 | Coolant leak isolation | SIL 1 |
| SIF-05 | Genset overspeed / protective shutdown | SIL 2 |
| SIF-06 | Switchgear fault protection | SIL 2 (electrical-protective-device heritage) |
| SIF-07 | Loss of cooling protection | SIL 1 |
| SIF-08 | Emergency stop (E-stop) | SIL 2 |

---

## §4  SAFETY INSTRUMENTED FUNCTIONS (SIFs)

### SIF Summary Table

| SIF ID | Description | Sensor(s) | Logic Solver | Final Element(s) | SIL | Response time |
|--------|-------------|-----------|--------------|------------------|-----|---------------|
| SIF-01 | Gas leak → isolate fuel, stop ignition sources | LEL ×6, H₂S ×4, CO ×3 | SIS PLC | Fuel SOV, genset ESD, main DC trip, enclosure vent fan | 2 | < 2 s |
| SIF-02 | Fire → suppress + isolate | VESDA + heat + flame detectors | Dedicated Novec panel + SIS PLC | Novec release, fuel SOV, main trip, fluid isolation | 2 | < 10 s (post 30 s pre-discharge) |
| SIF-03 | Arc flash → isolate breaker | Optical light sensor + current | SEL-751 relay + SIS PLC | Upstream breaker trip | 2 | < 20 ms |
| SIF-04 | Coolant leak → isolate rack | TraceTek + sump conductivity | Cassette BMS + SIS PLC | Rack UQD isolation, cassette power-off | 1 | < 30 s |
| SIF-05 | Genset overspeed | EMCP speed input + redundant sensor | Cat EMCP + SIS PLC | Fuel SOV, genset ESD | 2 | < 500 ms |
| SIF-06 | Switchgear fault (87/50/51) | Protective relay | SEL relay | Breaker trip | 2 | < 100 ms |
| SIF-07 | Loss of cooling → trip cassette | Flow + temperature + pressure | SIS PLC | Rack DC breakers, alarm | 1 | < 30 s |
| SIF-08 | E-stop assertion | 4× hardwired stations | SIS PLC | All ESD functions | 2 | < 5 s |

### SIL Definitions (IEC 61511)

| SIL | Probability of Failure on Demand (PFD) | Risk Reduction Factor (RRF) |
|-----|----------------------------------------|------------------------------|
| 1   | 10⁻¹ to 10⁻²                           | 10 to 100                    |
| 2   | 10⁻² to 10⁻³                           | 100 to 1,000                 |
| 3   | 10⁻³ to 10⁻⁴                           | 1,000 to 10,000              |
| 4   | 10⁻⁴ to 10⁻⁵                           | 10,000 to 100,000            |

---

## §5  SIF-01 — GAS LEAK DETECTION & ISOLATION

### Hazard

H-01 (natural gas leak → explosion), H-02 (CO accumulation), H-03 (H₂S exposure), H-12 (loss of ventilation + gas).

### Protected Zones

- Gas fuel train (from ECP gas inlet to each genset)
- Genset enclosures (inside each of 2 enclosures)
- Chiller enclosure (LiBr concentration ≠ gas, but if natural-gas-fired backup available)

### Sensors

| Tag | Type | Location | Range | Voting |
|-----|------|----------|-------|--------|
| GD-LEL-01/02 | Catalytic bead or IR, LEL 0–100% | Gas regulator station | 0–100% LEL | 1oo2 |
| GD-LEL-03/04 | IR methane | Genset A enclosure (inlet + interior) | 0–100% LEL | 1oo2 |
| GD-LEL-05/06 | IR methane | Genset B enclosure | 0–100% LEL | 1oo2 |
| GD-H2S-01/02 | Electrochemical | Gas regulator station | 0–100 ppm | 1oo2 |
| GD-H2S-03/04 | Electrochemical | Inside each genset enclosure | 0–100 ppm | 1oo2 |
| GD-CO-01 | Electrochemical | Genset A enclosure | 0–500 ppm | 1oo1 |
| GD-CO-02 | Electrochemical | Genset B enclosure | 0–500 ppm | 1oo1 |
| GD-CO-03 | Electrochemical | Chiller enclosure (if gas-fired backup) | 0–500 ppm | 1oo1 |
| FV-01/02 | Ventilation flow switch | Genset enclosure exhaust fan | ON/OFF | 1oo1 |

Recommended products:
- LEL / methane: MSA Ultima XIR or Dräger Polytron 8700 IR
- H₂S / CO: Dräger Polytron 8200 electrochemical

### Trip Logic

| Condition | Action | Delay |
|-----------|--------|-------|
| 1oo2 LEL > 20% LEL (1/5 of explosive limit) | Pre-alarm: warn, increase ventilation | 0 s |
| 1oo2 LEL > 40% | SIF-01 trip: close fuel SOV, stop gensets, vent | 0 s |
| 1oo2 H₂S > 10 ppm (IDLH threshold) | SIF-01 trip | 0 s |
| 1oo1 CO > 100 ppm | SIF-01 trip for that genset | 30 s |
| Ventilation fan fails while gas alarm present | SIF-01 trip | 0 s |

### Final Elements

| Tag | Description | Fail-state |
|-----|-------------|-----------|
| FV-SOV-01 | Fuel shutoff valve, main inlet (double-block) | Fail-closed |
| FV-SOV-02 | Fuel shutoff valve, genset A inlet | Fail-closed |
| FV-SOV-03 | Fuel shutoff valve, genset B inlet | Fail-closed |
| ESD-GEN-A | Cat EMCP ESD input | Fail-stop |
| ESD-GEN-B | Cat EMCP ESD input | Fail-stop |
| DC-MAIN-TRIP | 800 VDC main breaker trip coil | Fail-open (energize to trip) |
| VENT-FORCE | Force enclosure fan to high speed | Fail-high |

### SIL Calculation (Example)

For SIF-01 (gas leak → fuel isolation), SIL 2 target:

- Sensor subsystem: 1oo2D catalytic bead, λ_DU = 2 × 10⁻⁷/hr, MTTR = 24 hr, proof test = 6 mo → PFD_s ≈ 4 × 10⁻⁴
- Logic solver: Siemens S7-1500F, SIL 3 certified → PFD_l ≈ 5 × 10⁻⁵
- Final element: solenoid valve + actuator, λ_DU = 3 × 10⁻⁶/hr, proof test = 6 mo → PFD_v ≈ 7 × 10⁻³

Total PFD = 4 × 10⁻⁴ + 5 × 10⁻⁵ + 7 × 10⁻³ ≈ **7.5 × 10⁻³**

SIL 2 range is 10⁻² to 10⁻³. The valve proof test interval may need to be reduced to 3 months to achieve solid SIL 2 margin. Open item S-01.

### Response Time

- Gas detection cycle: < 200 ms
- Logic solver: < 100 ms
- Valve actuation: < 1 s (typical pneumatic solenoid)
- **Total: < 2 s** to full isolation

---

## §6  SIF-02 — FIRE DETECTION & SUPPRESSION

### Hazard

H-04 (cassette fire), H-05 (genset enclosure fire).

### Existing Coverage (FIRE-001)

The cassette interior is protected by:
- Xtralis VESDA-E VEU-A00 aspirating smoke detection (18 sample points)
- 3M Novec 1230 total flood, 5.85% v/v design concentration
- 10-minute hold time

This subsystem is the logic solver for the cassette-interior portion of SIF-02. It operates independent of the BPCS already (NFPA 2001 requirement) and is SIL 2 certified (Ansul / Xtralis Novec panel).

### New Coverage for External Skids

Genset enclosures require:
- Linear heat detection (kidde-type cable) or UV/IR flame detector inside each enclosure
- Automatic dry chemical extinguisher (ABC, DOT-approved) or FM-200 total flood within each genset enclosure

Chiller enclosure:
- Spot heat detector; extinguisher manual (not automated)

CDU skid:
- No active fire risk (no combustibles); passive only (smoke detector for alarm)

Munters skid:
- Rotor / belt fire possible but low-risk; smoke detector for alarm

### Trip Logic

| Condition | Action |
|-----------|--------|
| VESDA Fire 1 (cassette) | Pre-discharge alarm, 30 s countdown |
| VESDA Fire 2 (cassette) | Novec release, isolate rack DC, close ECP fluid valves |
| Genset heat detector activated | Trip that genset, isolate fuel, activate extinguisher |
| Any fire detector in control enclosure | Power-off that enclosure, alarm |

### Final Elements

Covered under SIF-01 (fuel isolation) + Novec suppression system + per-skid extinguishers.

---

## §7  SIF-03 — ARC FLASH PROTECTION

### Hazard

H-06 (arc flash at switchgear).

### Architecture

- Optical light sensors (fiber-coupled) at each breaker compartment
- Current detection via protective relay (already present per CTRL-001 §4.6)
- 2oo2 logic: light + current must both be present to declare arc event (reduces nuisance trip from camera flashes or door light)
- Action: trip upstream breaker within < 20 ms

### Recommended Products

- SEL-751 with AFD (arc-flash detection) option
- ABB REF615 with optical arc module

### Response Time

Arc flash incident energy curve says that shaving 50 ms off clearing time reduces incident energy by ~80%. Fast-tripping (< 20 ms) is the difference between a "hot flash" and an LTA event.

---

## §8  SIF-04 — COOLANT LEAK ISOLATION

### Hazard

H-08 (primary coolant leak).

### Sensors

Existing per INT-001 §15:
- TraceTek TT1000-OHP leak detection cable (~80 m, routed per INT §15)
- Sump level sensors (3-stage + overflow)
- Sump conductivity probe (distinguishes water / glycol / seawater)
- Per-rack drip trays with dedicated TraceTek tap

### Trip Logic

| Condition | Action | Delay |
|-----------|--------|-------|
| TraceTek alarm at any zone | Locate zone, isolate that rack, BMS alert | 30 s confirm |
| Sump level > mid | Start sump pump, escalate alarm | 0 |
| Sump level high-high | Isolate all rack UQDs, cassette power-off | 0 |
| Sump conductivity = seawater (offshore) | Close ECP valves, cassette power-off | 0 |

### Final Elements

- Belimo motorized ball valves at cassette ECP (close primary loop to skid)
- Per-rack UQD-25 isolation (BMS-commanded via rack-local solenoid actuator)
- Per-rack 250 A DC breaker (BMS-commanded open)

### SIL Target

SIL 1 — coolant leak consequences are generally moderate (equipment loss, slip hazard) not catastrophic unless volume is large. SIL 1 matches the ~30 s action time and existing detection coverage.

---

## §9  SIF-05 — GENSET OVERSPEED / PROTECTIVE SHUTDOWN

### Hazard

H-10 (overspeed → catastrophic mechanical failure, fire, debris).

### Architecture

- Primary: Cat EMCP 4.4 speed input (standard, engine-OEM)
- Redundant: independent magnetic pickup and redundant logic in the SIS PLC
- 2oo2 voting for trip decision: both EMCP and SIS must agree

### Trip Thresholds

- Governor setpoint: 1,800 rpm (60 Hz)
- Warning: 1,850 rpm
- Trip: 1,950 rpm (108% of rated) — **SIS-driven**, independent of EMCP
- EMCP also trips at 1,950 rpm via its own logic

### Final Elements

- Fuel rack shutoff (mechanical, governor-integral)
- Fuel SOV at genset inlet (electrical, SIS-driven)
- Starter lockout (prevents re-start until reset)

### Response Time

< 500 ms from overspeed detection to full fuel cutoff.

---

## §10  SIF-06 — SWITCHGEAR FAULT PROTECTION

### Hazard

H-06, H-07 (arc flash, DC shock from insulation failure).

### Architecture

Protective relays (SEL-751 DC variant, or equivalent) implement standard electrical protective functions:
- 87 (differential protection)
- 50/51 (overcurrent)
- 27 (undervoltage)
- 59 (overvoltage)
- 81 (frequency — AC only)
- Ground fault (50G/51G or insulation monitoring via Bender IMD)

### Function

Each protective element is a SIF unto itself from IEC 61511 perspective. The switchgear industry has used SIL 2 / SIL 3 certified relays for decades; this is inherited. SEL, ABB, Siemens, GE all produce SIL-certified protective relays.

### Integration with SIS

Protective relay trip outputs are hardwired to breaker trip coils (direct, fast). Relay event records are also sent to the SIS PLC via IEC 61850 MMS for logging and coordination.

---

## §11  SIF-07 — LOSS OF COOLING PROTECTION

### Hazard

H-11 (loss of cooling → GPU damage, $10M+ loss).

### Architecture

- Primary flow measurement (ultrasonic, per-rack)
- Primary temperature measurement (RTD, supply + return per rack)
- Pressure measurement at CDU supply / return

### Trip Logic

| Condition | Action |
|-----------|--------|
| Primary flow < 50% of nominal for > 30 s at non-zero pump demand | Trip all rack DC breakers, Cassette to HOT_STANDBY |
| Any rack return T > 62 °C for > 60 s | Trip that rack, alarm; if > 3 racks → trip all |
| Primary pressure < 0.5 bar (lost suction) | Trip pumps, alarm, Cassette to HOT_STANDBY |

### Final Elements

- Rack DC breakers (15 racks)
- CDU pump VFDs (fail-off)
- Cassette BMS state transition to HOT_STANDBY

### SIL Target

SIL 1 — driven more by economic consequence than safety; GPUs have thermal protection in firmware and will throttle before damage.

---

## §12  SIF-08 — EMERGENCY STOP

### Hazard

Operator-initiated emergency from any perceived hazard.

### Architecture

- 4× E-stop buttons located per INT §10: one at each ECP (ELEC-end and CDU-end), plus one at each genset and one at the switchgear
- Each station hardwired to SIS PLC with dual redundant channels (SIL 2)
- Press-to-activate, twist-to-reset, with key lockout available
- Latching — requires physical reset after actuation

### Action

Full EMERGENCY_SHUTDOWN sequence per CAS-MODES-001 §11. Equivalent to any SIS-driven trip — all final elements actuate in parallel within 5 s.

### Response Time

< 5 s to all ESD actions complete. Hardwired pathway bypasses any network latency.

---

## §13  SAFETY SYSTEM ARCHITECTURE

### Logic Solver

**Recommended: Siemens SIMATIC S7-1500F (fail-safe)**, TÜV-certified SIL 3 capable.

Alternative: HIMA H51q, Emerson DeltaV SIS, Honeywell Safety Manager, Triconex Tricon. HIMA is the purest-play safety PLC (their only product line is safety); Siemens 1500F is more common at this scale and integrates well with the non-safety S7-1500 PLCs already specified for the CDU skid.

### Redundancy

- **1oo2D architecture** for logic: dual processors, diverse voting
- **I/O**: SIL-rated input and output cards
- **Sensors**: 1oo2 voting where SIL 2 required; 1oo1 for SIL 1
- **Final elements**: single valve or breaker is generally acceptable if proof-tested regularly; dual valves (2oo2 to trip) considered for SIF-01 main fuel isolation

### Power

- Dedicated 24 VDC safety UPS (separate from the BPCS life-safety UPS)
- 8-hour runtime minimum (NFPA 110 Level 1 equivalent)
- Charger from 480 VAC aux (from switchgear) with battery disconnect

### Communications

- **Hardwired** connection to all final elements (no network dependency for safety actions)
- **Ethernet** connection to BPCS for status / event logging only (read-only from BPCS side)
- **PROFIsafe** (Siemens) or **CIP Safety** (Rockwell) for I/O over network if distance requires
- **No internet connectivity** — SIS is air-gapped from any WAN

### Time Synchronization

SIS has its own PTP slave, synchronized to the same grandmaster as the BPCS (IEEE 1588 Class A — better than 1 ms). Enables forensic reconstruction across SIS and BPCS events.

---

## §14  SEPARATION FROM BPCS

### Physical Separation

- Dedicated SIS enclosure, physically separate from BPCS / L2 Gateway cabinet
- Dedicated SIS power (separate UPS)
- Dedicated SIS network segment (Zone 0, see CTRL-001 §15)
- Dedicated field wiring: SIS sensors and final elements use separate cables from BPCS instrumentation

### Logical Separation

- SIS controller runs dedicated safety firmware (SIL-certified) — no BPCS logic shares CPU
- BPCS cannot write to SIS logic or bypass any safety function
- SIS can publish state to BPCS (read-only) for monitoring / logging
- Common-cause failure avoidance: SIS sensors use different technology from BPCS where practical (e.g., BPCS flow meter = ultrasonic; SIS low-flow switch = paddle)

### Management of Change (MOC)

Any change to SIS logic, sensors, or final elements requires:
1. Written MOC per procedure
2. Review by authorized functional safety engineer (with TÜV or CFSE credential)
3. Impact analysis on SIL calculations
4. Test proof after change
5. Signed approval by supervisor + engineer
6. Document update to this SIS-001

Changes to BPCS do **not** require MOC to the SIS unless they cross the interface. This is a deliberate design principle to keep the SIS stable while BPCS evolves.

---

## §15  PROOF-TEST & MAINTENANCE

### Proof Test Intervals

| SIF | Nominal Interval | Test method |
|-----|------------------|-------------|
| SIF-01 Gas detection | 3 months | Span gas calibration; simulate trip |
| SIF-02 Fire detection | 6 months | VESDA sampling flow test; Novec panel function test (no agent release) |
| SIF-03 Arc flash | 12 months | Light sensor injection test; relay trip test |
| SIF-04 Coolant leak | 6 months | Apply conductive fluid to TraceTek cable; verify alarm |
| SIF-05 Genset overspeed | 6 months | Speed signal injection via EMCP test mode |
| SIF-06 Switchgear | 12 months | Primary injection testing of relays |
| SIF-07 Loss of cooling | 6 months | Flow meter bypass test, reduce flow artificially |
| SIF-08 E-stop | 3 months | Press each station, verify trip |

Actual intervals may be reduced to achieve SIL targets (see §5 SIL calculation example). Final intervals set during commissioning and documented in the Safety Manual.

### Test Procedures

Each SIF has a formal proof-test procedure document (to be developed as CAS-SIS-PT-001 through CAS-SIS-PT-008). Procedures include:
- Pre-test safe-state verification
- Test steps
- Acceptance criteria (within performance spec)
- Pass/fail documentation
- Return to service steps
- Deviation handling

### Bypass Management

Under extraordinary circumstances a SIF may need to be bypassed (e.g., during commissioning test, deliberate proof test with output disabled). Requirements:
- Bypass requires two-key authentication (supervisor + engineer)
- Bypass engaged = visible annunciation at L2 HMI, constant
- Maximum bypass duration = 8 hours, auto-reset at end
- Bypass while in NORMAL or related modes = prohibited (interlock)
- Every bypass event is logged and reviewed weekly

### Maintenance Records

- Per-SIF maintenance log: every inspection, calibration, test, finding
- Cumulative PFD tracking: actual vs calculated
- Failure database: any device failure reported; root cause analyzed; replacement frequency tracked
- Annual functional safety audit per IEC 61511

---

## §16  FUNCTIONAL SAFETY ASSESSMENT & SIGN-OFF

### FSA Stages (per IEC 61511-1 clause 5.2)

| Stage | Description | Timing | Deliverable |
|-------|-------------|--------|-------------|
| FSA-1 | After H&RA and SRS complete | Pre-engineering | Hazard & Risk Analysis report, Safety Requirements Specification |
| FSA-2 | After SIS design complete | Pre-construction | Design review, SIL calculations verified |
| FSA-3 | After installation, pre-startup | Commissioning | Site acceptance test, all proof tests pass |
| FSA-4 | Periodic (typically annual) | Operation | Maintenance record review, SIS modifications reviewed |
| FSA-5 | After major change or retirement | As needed | Change impact assessment |

### Required Roles

- **Functional Safety Manager (FSM)** — CFSE or TÜV FS Engineer certified; employee of ADC or qualified integrator
- **Independent Assessor** — separate from engineering team; performs FSA
- **Operations / Maintenance SME** — represents operating organization

### Documentation

At each FSA stage, signed documents archived:
- H&RA (Hazard & Risk Analysis) report
- SRS (Safety Requirements Specification)
- SIS Design Document (this CAS-SIS-001 is the framework; detailed design follows)
- SIL calculation worksheets
- FAT report (factory acceptance test, at integrator's shop)
- SAT report (site acceptance test, at deployment site)
- Operations & Maintenance Manual
- Safety Lifecycle Audit report

---

## §17  OPEN ITEMS

| ID | Priority | Description | Owner | Notes |
|----|----------|-------------|-------|-------|
| S-01 | P-0 | Formal HAZID workshop — convene with integrator, FSM, operator, Cat, chiller vendor | ADC ↔ integrator | Formal deliverable HAZID-001; gates FSA-1 |
| S-02 | P-0 | SIS PLC selection — Siemens S7-1500F vs HIMA vs Emerson DeltaV SIS vs Rockwell GuardLogix | ADC engineering | Affects §13 |
| S-03 | P-0 | Gas detector vendor final selection — MSA Ultima XIR vs Dräger Polytron 8700 | ADC procurement | Affects §5 |
| S-04 | P-0 | Fuel SOV selection — double block-and-bleed valve per NFPA 87; vendor selection | ADC engineering | Affects SIF-01 final element |
| S-05 | P-1 | H₂S monitoring threshold — verify 10 ppm IDLH is the right trip vs 5 ppm (some operators) | ADC ↔ customer | Affects §5 |
| S-06 | P-1 | Proof-test interval optimization — may need 3-month interval for SIF-01 to achieve SIL 2 | ADC ↔ integrator | Affects §15 |
| S-07 | P-1 | Functional Safety Manager identification — ADC staff or consulting engagement | ADC | Gates FSA-1 |
| S-08 | P-1 | Independent Assessor selection — separate from integrator | ADC | Affects §16 |
| S-09 | P-2 | Offshore variant SIS adaptations — marine-specific hazards (heave, wave impact, saltwater) | ADC ↔ DNV | Affects offshore deployment |
| S-10 | P-2 | Cyber-physical attack modeling for SIS — how does compromised BPCS affect SIS? | ADC ↔ cybersecurity consultant | Interacts with CAS-CYBER-001 |
| S-11 | P-2 | Integration with customer's Emergency Response Plan (ERP) — who does SIS call, what's automated, what's manual | ADC ↔ customer BD | Affects deployment |
| S-12 | P-3 | Training curriculum for operator / technician on SIS | ADC engineering | Affects operational readiness |

---

## SUMMARY OF KEY DESIGN DECISIONS

| # | Decision | Rationale |
|---|----------|-----------|
| 1 | IEC 61511 / IEC 61508 framework | Industry-standard for process-industry SIS; recognized by oil & gas and regulatory bodies |
| 2 | Dedicated SIL-certified safety PLC (Siemens S7-1500F) | Pure safety hardware; TÜV-certified; common ground with CDU skid PLC (maintenance familiarity) |
| 3 | 1oo2D voting on sensors for SIL 2 | Reduces nuisance trip rate; standard practice per IEC 61511 |
| 4 | Physical and logical separation from BPCS | IEC 61511 mandatory; prevents common-cause failure with BPCS |
| 5 | Hardwired connections to all final elements | Eliminates network latency and cyber attack vector for safety actions |
| 6 | 8-hour dedicated safety UPS | Separate from BPCS UPS; eliminates common-cause power loss |
| 7 | IEEE 1588 PTP time sync shared with BPCS | Same grandmaster; enables forensic reconstruction |
| 8 | 3–12 month proof test intervals | Balances PFD target with operational burden |
| 9 | Formal FSA at 5 lifecycle stages | Ensures SIL assignments remain valid across lifecycle |
| 10 | LiBr chiller and UPS common-cause fire/ventilation risks mitigated by SIF-01 scope extension | Explicit, not inherited |
| 11 | Offshore deployment adds marine-specific SIFs (TBD) | Deferred to offshore variant design |

---

**Cassette-SIS-001 — Safety Instrumented System · Rev 1.1 · 2026-04-20**
**Scott Tomsu · scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana**
**CONFIDENTIAL**
