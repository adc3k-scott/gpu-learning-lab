# Cassette — EXTERNAL CONNECTION PANEL (ECP) INTERFACE CONTROL DOCUMENT

**Document:** Cassette-ECP-001
**Revision:** 2.0
**Date:** 2026-04-19
**Classification:** CONFIDENTIAL
**Companion to:** 

**Purpose:** This document defines the sole physical and logical interface between the ADC-3K Pod and any upstream platform. Anyone integrating a pod — platform electrical, mechanical, controls, or operations — works from this document. No exceptions.

| Rev | Date       | Description                                                       |
|-----|------------|-------------------------------------------------------------------|
| 1.0 | 2026-04-19 | Initial release —                |
| 2.0 | 2026-04-19 | CHW interface corrected: 1,800→2,200 LPM, ΔT 5→11 °C, DN100→DN150 Victaulic at CDU ECP (Cassette-COOL-001 §8) |

**Prepared by:** Scott Tomsu · CEO / Chief Engineer
scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana

---

## TABLE OF CONTENTS

- §1  Purpose & Scope
- §2  ECP Zones — ELEC End and CDU End
- §3  ELEC ECP — Complete Penetration Schedule
- §4  CDU ECP — Complete Penetration Schedule
- §5  Electrical Interface — 800 V DC Primary
- §6  Electrical Interface — 415 V AC Alternative
- §7  Fluid Interface — Chilled Water
- §8  Fluid Interface — Condensate & Drains
- §9  Fluid Interface — Munters Ducts
- §10 Data Interface — InfiniBand Fabric
- §11 Data Interface — Out-of-Band Management
- §12 Data Interface — Starlink / Cellular Antennas
- §13 Safety Interface — Emergency Stop
- §14 Test & Commissioning Ports
- §15 Grounding & Bonding Interface
- §16 Environmental Ratings — Onshore vs Offshore
- §17 Connector Specifications (Referenced)
- §18 Cable Specifications (Referenced)
- §19 Acceptance Testing at ECP
- §20 Change Control

---

## §1  PURPOSE & SCOPE

### What This Document Is

The ECP Interface Control Document (ICD) is the contract between the Cassette and the platform. Every physical penetration through the Cassette shell, every cable, every pipe, every fiber that crosses the container boundary is specified here — no more, no less.

### What This Document Is Not

- Not a platform design document (Cassette makes no assumptions about upstream).


### Rule of Contract

If a service is not listed in §3 or §4, it does not exist at the ECP. If a service is listed but its detailed specification is ambiguous, the numbered specification section (§5–§15) is authoritative.

### Two-Zone Architecture

The pod has two ECP zones at opposite short ends:

- **ELEC ECP** (end opposite CDU): all electrical service, BMS uplink, E-stop
- **CDU ECP** (end with CoolIT CHx2000): all fluid service, InfiniBand, Munters ducts, test ports

This separation is deliberate — electrical and fluid services enter from opposite ends, eliminating the possibility of cable/pipe crossovers inside the pod and giving service crews orthogonal approach paths.

---

## §2  ECP ZONES — ELEC END AND CDU END

### ELEC ECP — Dimensions & Layout

Located at the short end of the Cassette opposite the CDU.

| Parameter                  | Value                              |
|----------------------------|------------------------------------|
| Zone footprint             | Entire short end face, 2,438 × 2,896 mm exterior |
| Usable penetration area    | 2,000 × 2,400 mm centered          |
| Recessed housing depth     | 300 mm (weather protection + service loop) |
| Access for service         | Hinged outer cover, 1,600 × 2,000 mm |
| Cover fastener             | 12 quarter-turn Dzus latches (onshore) or 12 stainless bolts (offshore) |
| Interior side              | Inside ELEC end zone (1,200 mm interior length) |

### CDU ECP — Dimensions & Layout

Located at the short end of the Cassette with the CoolIT CHx2000 CDU.

| Parameter                  | Value                              |
|----------------------------|------------------------------------|
| Zone footprint             | Entire short end face, 2,438 × 2,896 mm exterior |
| Usable penetration area    | 2,000 × 2,400 mm centered          |
| Recessed housing depth     | 400 mm (accommodates 4" Victaulic + Munters duct elbows) |
| Access for service         | Hinged outer cover, 1,600 × 2,000 mm |
| Cover fastener             | 12 quarter-turn Dzus latches (onshore) or 12 stainless bolts (offshore) |
| Interior side              | Inside CDU end zone (1,500 mm interior length) |

### ECP Cover Inspection Windows

Both ECP covers have three 200 × 150 mm polycarbonate inspection windows (2,000 J impact rating):
- Cable entry status (LED backlit, shows connection status)
- Primary disconnect position indicator (ELEC ECP) / CDU touchscreen (CDU ECP)
- Bond stud and grounding visual

---

## §3  ELEC ECP — COMPLETE PENETRATION SCHEDULE

All penetrations at the ELEC ECP, in physical order from top to bottom of the panel:

| # | Service                         | Connector / Interface                        | Rating            | Qty |
|---|----------------------------------|----------------------------------------------|-------------------|-----|
| 1 | GPS antenna (time sync)          | SMA connector, active antenna with DC pass   | IP66, surge-protected | 1   |
| 2 | Starlink antenna feed            | N-type connector, 50 Ω                       | IP66, marine rated| 1   |
| 3 | Cellular antenna feed            | N-type connector, 50 Ω                       | IP66, marine rated| 1   |
| 4 | BMS fiber uplink (primary)       | LC/APC duplex, single-mode OS2               | IP66 w/ EMI gland | 2 fibers |
| 5 | BMS fiber uplink (redundant)     | LC/APC duplex, single-mode OS2               | IP66 w/ EMI gland | 2 fibers |
| 6 | 800 V DC primary positive        | Stäubli CombiTac 2500 series, 2× 70 mm² cable | IP67, 2,500 A    | 1   |
| 7 | 800 V DC primary negative        | Stäubli CombiTac 2500 series, 2× 70 mm² cable | IP67, 2,500 A    | 1   |
| 8 | 415 V AC 3-ph alternate input    | Cam-Lok E1016 series (L1/L2/L3/N/G), optional | IP67, 400 A      | 5 (if used) |
| 9 | Chassis ground / bond            | 50 mm² bond stud, M12 stainless              | 10,000 A fault   | 1   |
|10 | Emergency stop (hardwire IN)     | MIL-DTL-5015 6-pin connector, 24 V DC dry    | IP67              | 1   |
|11 | Emergency stop (hardwire OUT)    | MIL-DTL-5015 6-pin connector, 24 V DC dry    | IP67              | 1   |
|12 | External strobe power            | Integral to ECP housing                      | —                 | 1   |

### Physical Arrangement (ELEC ECP)

```
+--------------------------------------------------+
|  [1]GPS   [2]Starlink   [3]Cell               +  |  ← Top (antennas)
|                                                  |
|  [4]BMS fiber primary   [5]BMS fiber redundant   |  ← Upper (data)
|                                                  |
|  [10]E-STOP IN          [11]E-STOP OUT           |  ← Mid (safety)
|                                                  |
|  [6] 800V DC (+)        [7] 800V DC (-)          |  ← Lower (power DC)
|                                                  |
|  [8] 415V AC L1 L2 L3 N G (5 connectors)         |  ← Bottom (power AC alt)
|                                                  |
|  [9] GND stud                            [12]     |  ← Bottom corners
+--------------------------------------------------+
     ELEC ECP outer cover removed
```

---

## §4  CDU ECP — COMPLETE PENETRATION SCHEDULE

All penetrations at the CDU ECP, in physical order:

| # | Service                         | Connector / Interface                     | Rating            | Qty |
|---|----------------------------------|-------------------------------------------|-------------------|-----|
| 1 | CHW supply inlet                 | 6" (DN150) Victaulic grooved, Style 77   | 250 psi, 120 °C  | 1   |
| 2 | CHW return outlet                | 6" (DN150) Victaulic grooved, Style 77   | 250 psi, 120 °C  | 1   |
| 3 | Munters process air supply (dry) | 200 mm insulated flanged duct, 4-bolt    | Sealed, vapor barrier | 1   |
| 4 | Munters process air return (wet) | 200 mm insulated flanged duct, 4-bolt    | Sealed           | 1   |
| 5 | InfiniBand compute uplink        | MPO-24 bulkhead, single-mode OS2         | IP54 (onshore) / IP66 (offshore) | 1 assembly |
| 6 | InfiniBand compute downlink      | MPO-24 bulkhead, single-mode OS2         | IP54 / IP66      | 1 assembly |
| 7 | InfiniBand compute redundant     | MPO-24 bulkhead, single-mode OS2         | IP54 / IP66      | 1 assembly |
| 8 | Out-of-band management A         | RJ-45 Cat6A shielded, Neutrik NE8FDX     | IP67             | 1   |
| 9 | Out-of-band management B         | RJ-45 Cat6A shielded, Neutrik NE8FDX     | IP67             | 1   |
|10 | CDU power feed (from platform)   | Pin-and-Sleeve IEC 60309, 60 A 3-ph      | IP67             | 1   |
|11 | Munters power feed (from platform)| Pin-and-Sleeve IEC 60309, 80 A 3-ph     | IP67             | 1   |
|12 | Munters Modbus RTU (RS-485)      | M12 A-coded, 5-pin                       | IP67             | 1   |
|13 | Condensate drain                 | 1" NPT female, with check valve + fume loop | Gravity         | 1   |
|14 | Leak-detection emergency drain   | 1" NPT female, solenoid-actuated         | Normally closed  | 1   |
|15 | N2 fill / purge port             | 1/2" NPT with check valve                | 250 psi          | 1   |
|16 | Annual pressure test port        | 1/4" NPT with cap                        | 500 psi          | 1   |
|17 | External IR camera port          | M12 A-coded, 4-pin (power + Ethernet)    | IP67             | 1   |

### Physical Arrangement (CDU ECP)

```
+--------------------------------------------------+
|  [3] Munters supply duct  [4] Munters return duct|  ← Top (air)
|  (200 mm insulated flanges)                      |
|                                                  |
|  [5]IB-UP   [6]IB-DN   [7]IB-RED (MPO-24 bulkhds)|  ← Upper (fiber)
|  [8]OOB-A   [9]OOB-B   [17]IR-CAM (small conn.)  |
|                                                  |
|  [10] CDU power   [11] Munters power   [12]MBUS  |  ← Mid (power/control)
|                                                  |
|  [1] CHW supply 4"  Victaulic                    |  ← Lower (fluid)
|  [2] CHW return 4"  Victaulic                    |
|                                                  |
|  [13]Cond.  [14]Leak  [15]N2  [16]Test (NPT x4)  |  ← Bottom (drains/test)
+--------------------------------------------------+
     CDU ECP outer cover removed
```

---

## §5  ELECTRICAL INTERFACE — 800 V DC PRIMARY

### Specification

| Parameter                        | Value                                    |
|----------------------------------|------------------------------------------|
| Nominal voltage                  | 800 V DC ±5%                             |
| Operating range                  | 760–840 V DC                             |
| Polarity                         | Ungrounded (IT system) per IEC 61557-8   |
| Pod peak current (NVL72 tier)    | 2,100 A (1.68 MW at 800 V)               |
| Pod peak current (NVL144 CPX)    | 2,800 A (2.24 MW at 800 V)               |
| Design current                   | 2,500 A continuous                       |
| NEC 125% rating                  | 3,125 A nameplate                        |
| Fault current withstand          | 50 kA for 100 ms                         |
| Ripple (allowable)               | ≤ 5 V peak-to-peak at 800 V nominal     |
| Connector                        | Stäubli CombiTac 2500 or equivalent blind-mate |
| Cable (pod-internal landing)     | 2× 70 mm² per polarity, 600 mm service loop |

### What the Cassette Guarantees

- Accepts inputs within the operating range without fault
- Trips its main disconnect within 100 ms on insulation resistance < 5 kΩ
- Reports bus voltage and current to BMS at 1 Hz minimum

### What the Cassette Requires From Platform

- Stable 800 V DC source with ripple ≤ 5 V p-p
- Ground-fault/insulation-monitoring coordinated with pod IMD (§5 of ADC-CAS-001 Rev 2.0)
- Isolation means upstream (platform-side disconnect) for pod service
- No back-feed permitted: pod is a sink, never a source

### Polarity Keying

Stäubli CombiTac connectors are mechanically keyed for polarity. Platform-side cable assemblies must be assembled with matching keying to prevent reverse-polarity connection. Verification required at commissioning per §19.

---

## §6  ELECTRICAL INTERFACE — 415 V AC ALTERNATIVE

### When This Applies

The Delta in-rack 110 kW power shelf supports both 800 V DC and 415 V AC 3-phase input. For platforms without 800 V DC infrastructure, 415 V AC can be delivered to the Cassette and rectified by the per-rack shelves.

### Specification

| Parameter                        | Value                                    |
|----------------------------------|------------------------------------------|
| Nominal voltage                  | 415 V AC line-to-line ±10%               |
| Frequency                        | 50 or 60 Hz ±3%                          |
| Phase imbalance (voltage)        | ≤ 2% steady-state                        |
| THDv at ECP                      | ≤ 5% per IEEE 519                        |
| Pod peak current (NVL72 tier)    | 2,330 A per phase (1.68 MW @ 415 V, 0.95 PF) |
| Pod peak current (NVL144 CPX)    | 3,115 A per phase (2.24 MW @ 415 V)      |
| Design current                   | 3,200 A per phase continuous             |
| Connector                        | Cam-Lok E1016 series, 5 connectors (L1/L2/L3/N/G) |
| Cable (pod-internal landing)     | 4× 120 mm² per phase + neutral           |

### What the Cassette Requires

- TN-S grounding system (solidly grounded neutral at source, separate protective earth)
- Source capable of sinking pod inrush current at rectifier startup (~3× nominal for 200 ms)
- Upstream overcurrent protection coordinated with pod main disconnect

### Selection

AC vs DC input is selected at commissioning (§19). Both sets of ECP connectors are physically present on every pod; only one is in service at a time. The unused set is capped with a weather-tight connector cover.

---

## §7  FLUID INTERFACE — CHILLED WATER

### Specification

| Parameter                    | Supply (to Pod)        | Return (from Pod)       |
|------------------------------|------------------------|-------------------------|
| Fluid                        | Treated water (platform-side)   | Treated water           |
| Supply temperature           | 7–12 °C (design 10 °C) | —                       |
| Return temperature           | —                      | 12–18 °C (design 15 °C) |
| ΔT design                    | 11 °C                  | —                       |
| ΔT operating range           | 8–14 °C                | —                       |
| Flow (design)                | 2,200 LPM              | 2,200 LPM               |
| Flow (operating range)       | 1,800–2,500 LPM        | matched                 |
| Pressure at ECP              | 150–350 kPa            | 150–350 kPa             |
| Max pressure                 | 600 kPa burst          | 600 kPa burst           |
| Connector                    | 6" (DN150) Victaulic Style 77 grooved | same   |
| Pipe material                | 304L or 316L stainless | same                    |

### Water Quality Requirements (Platform Responsibility)

| Parameter              | Limit                       |
|------------------------|-----------------------------|
| Total hardness         | < 60 mg/L as CaCO₃          |
| Chlorides              | < 50 mg/L (onshore) / < 25 mg/L (offshore) |
| Conductivity           | < 500 μS/cm                 |
| pH                     | 7.5–9.0                     |
| Total suspended solids | < 10 mg/L                   |
| Dissolved oxygen       | < 0.5 mg/L (corrosion control) |
| Biological load        | < 10⁴ CFU/mL (dosed)        |

### What the Cassette Guarantees

- Removes 1.6 MW minimum / 2.2 MW peak heat load into the return stream
- Return temperature stays within 12–18 °C when supply is within 7–12 °C
- No chemical addition to secondary water (pod-side is closed primary loop, chemistry isolated)
- No biological contamination introduced by pod
- Stops drawing flow (bypass mode) if supply exceeds 18 °C or pressure falls below 100 kPa

### What the Cassette Requires From Platform

- Supply water quality maintained per above table
- Flow control valve or pump modulation external to pod
- Expansion tank / makeup on platform side
- Annual water chemistry audit

### Fluid Isolation

Motorized isolation valves at both ECP fluid penetrations, pod-side. BMS can command closure on any fluid emergency (leak, sump overflow, seawater ingress). Platform-side should have matching manual valves for service isolation.

---

## §8  FLUID INTERFACE — CONDENSATE & DRAINS

### Condensate Drain

| Parameter                    | Value                                |
|------------------------------|--------------------------------------|
| Source                       | Interior condensation + CDU drip pan |
| Expected flow                | 0–2 L/hr normal, up to 20 L/hr peak  |
| Connector                    | 1" NPT female at ECP                 |
| Check valve                  | Integrated (prevents back-flow)      |
| Fume loop                    | 150 mm water seal                    |
| Platform side                | Routed to platform condensate collection or direct to environment per local permit |

### Leak-Detection Emergency Drain

| Parameter                    | Value                                |
|------------------------------|--------------------------------------|
| Source                       | Sump overflow path                   |
| Normally                     | Closed (solenoid)                    |
| BMS-actuated open            | On sump high-high alarm              |
| Connector                    | 1" NPT female at ECP                 |
| Platform side                | Emergency drain to approved disposal |

### Offshore-Specific

- Condensate drain to deck scupper or marine sump (MARPOL compliant)
- Emergency drain cannot discharge overboard without prior treatment; routes to platform collection tank
- Both drains include flame arrestor on offshore variant

---

## §9  FLUID INTERFACE — MUNTERS DUCTS

### Specification

| Parameter                        | Process Supply (Dry)   | Process Return (Wet)   |
|----------------------------------|------------------------|------------------------|
| Duct diameter                    | 200 mm internal        | 200 mm internal        |
| Insulation                       | 25 mm closed-cell foam | 25 mm closed-cell foam |
| Flange standard                  | 4-bolt, 225 mm BCD     | 4-bolt, 225 mm BCD     |
| Gasket                           | EPDM or silicone       | EPDM or silicone       |
| Flow                             | 600 SCFM (~1,020 m³/hr) | 600 SCFM              |
| Temperature                      | 5–30 °C dry            | 20–30 °C wet           |
| Relative humidity                | 5–30% (Munters output) | 30–100% (pod return)   |
| Material                         | 304 stainless or aluminum, weather-rated | same |

### Munters Skid Interface

The Munters HCD-600 sits on an external skid. Cassette provides the duct penetrations; platform provides the skid, its power, and the duct connections between skid and Cassette.

### What the Cassette Guarantees

- Maintains positive pressure at process return duct (slight over-pressure relative to ambient)
- Returns moist air to Munters within stated flow and temperature window
- Dampers at ECP close on fire suppression activation (prevents Novec escape + prevents duct draft-feeding fire)

### What the Cassette Requires From Platform

- Munters HCD-600 (or approved equivalent) on external skid
- 480 V AC 3-ph power to skid (separate from pod CDU power)
- Process air supply at 5–30% RH (Munters output spec)
- Skid control via Modbus RTU (§11)

### Duct Failure Mode

If Munters skid fails or is offline, Cassette continues to operate with elevated interior humidity (up to 50–60% RH). BMS alerts on humidity > 55% sustained. No automatic pod shutdown — pod tolerates elevated humidity as long as no dew-point-breach occurs at cold plates (well below operating range).

---

## §10 DATA INTERFACE — INFINIBAND FABRIC

### Specification

| Parameter                        | Value                                |
|----------------------------------|--------------------------------------|
| Fabric standard                  | NVIDIA Quantum-X800 InfiniBand NDR   |
| Line rate                        | 400 Gb/s per port                    |
| Fiber type                       | Single-mode OS2 (9/125 μm)           |
| Bulkhead connector               | MPO-24 female (12 fiber pairs each)  |
| Uplink bandwidth (per bulkhead)  | 24 × 400 Gb/s = 9.6 Tb/s             |
| Uplink bulkheads                 | 2 primary (uplink + downlink) + 1 redundant |
| Total pod bandwidth              | 28.8 Tb/s aggregate (primary + redundant) |
| Cable length limit               | 100 m at 400 Gb/s (passive MPO trunk) |
| Cable length extension           | Active optical if > 100 m           |

### Physical Arrangement

Three MPO-24 bulkheads at the CDU ECP (#5, #6, #7 in §4 schedule):
- Bulkhead A (uplink): east path to spine switch A
- Bulkhead B (downlink): same spine A return (for NDR full-duplex)
- Bulkhead C (redundant): west path to spine switch B (failover)

### What the Cassette Requires From Platform

- Two physically diverse fiber paths (A and B) to spine switches
- NVIDIA Quantum-X800 or compatible spine infrastructure
- Fiber polishing and attenuation test report per path at commissioning

### Fiber Maintenance

- Bulkhead covers rated for 500+ mating cycles
- Cleaning kit required for every re-connection (dust = attenuation)
- Cassette-side pigtails have 1 m service loop for future re-termination

---

## §11 DATA INTERFACE — OUT-OF-BAND MANAGEMENT

### Specification

| Parameter                        | Value                                |
|----------------------------------|--------------------------------------|
| Protocol                         | 1 GbE Ethernet (RJ-45)               |
| Cable                            | Cat6A shielded (STP)                 |
| Connector                        | Neutrik NE8FDX IP67                  |
| Redundancy                       | 2 independent ports (A and B)        |
| VLAN                             | Isolated from production InfiniBand  |
| Routing                          | To platform SCADA and OOB network    |

### What Flows Over OOB

- BMS telemetry (Jetson Orin aggregate) at 1 Hz normal, event-driven alerts
- Delta power shelf status (Redfish)
- CoolIT CDU status (Redfish)
- Munters skid Modbus RTU-over-Ethernet gateway
- VESDA-E alarms and status
- Novec 1230 panel status
- Console server access to NVIDIA switches (QM9700)
- Firmware updates (signed, scheduled only)

### What Does NOT Flow Over OOB

- Compute workload traffic (InfiniBand only)
- Live video from IR cameras (dedicated link, §12)
- Direct GPU access (requires InfiniBand fabric)

### Security

- Mutual TLS on all OPC-UA and MQTT links
- Certificate rotation every 90 days
- Audit log retained 1 year
- Platform-side firewall restricts OOB to specific SCADA hosts only

---

## §12 DATA INTERFACE — STARLINK / CELLULAR ANTENNAS

### Specification

| Parameter                        | Value                                |
|----------------------------------|--------------------------------------|
| Starlink                         | Maritime (offshore) or Business (onshore) terminal |
| Cellular                         | 4G/5G multi-carrier modem, Cradlepoint or equivalent |
| Antenna mounting                 | On ECP housing exterior (top of ELEC ECP cover) |
| Feed cables                      | N-type, LMR-400 or better, ≤ 6 m to Jetson Orin |
| Surge protection                 | Integrated at N-type connector entry |
| Primary use                      | BMS backhaul when fiber is unavailable |

### Automatic Failover

Jetson Orin manages three-tier backhaul:
1. Primary: fiber OOB (always preferred)
2. Secondary: Starlink (auto-activate on fiber loss > 30 sec)
3. Tertiary: cellular (activate on Starlink unavailability)

### Bandwidth Expectations

- Fiber OOB: 1 Gbps typical, sufficient for full telemetry + firmware push
- Starlink: 50–250 Mbps, sufficient for telemetry + compressed logs
- Cellular: 5–50 Mbps, sufficient for critical alerts only; suspend non-essential telemetry

---

## §13 SAFETY INTERFACE — EMERGENCY STOP

### Specification

| Parameter                        | Value                                |
|----------------------------------|--------------------------------------|
| Signal                           | 24 V DC dry contact, fail-safe (energized = safe) |
| Connector                        | MIL-DTL-5015 6-pin circular          |
| Redundancy                       | Dual-channel, Category 4 per ISO 13849 |
| Response time                    | ≤ 100 ms pod-side shutdown           |
| Hardwired (not software)         | Direct to main disconnect trip coil  |

### E-Stop Paths

**E-stop IN (from platform):** platform can assert Cassette shutdown. Wiring:
- Pin 1/2: Channel A (24 V DC loop)
- Pin 3/4: Channel B (24 V DC loop)
- Pin 5/6: Status feedback to platform

**E-stop OUT (to platform):** pod can assert platform shutdown (on fire, catastrophic leak, etc.). Same pin assignment.

### Assertion Events

Pod E-stop OUT is asserted on:
- Novec 1230 discharge
- Sump overflow (massive leak)
- Seawater detection (offshore)
- Cassette fire confirmation (VESDA Fire 2 + temperature)
- BMS critical fault

### De-Assertion (Reset)

Requires physical key-switch reset at the ELEC ECP after BMS verifies safe state. No remote reset. This is by design — an E-stop event means someone needs to inspect on-site before re-energization.

---

## §14 TEST & COMMISSIONING PORTS

### N2 Fill / Purge Port

| Parameter                    | Value                                |
|------------------------------|--------------------------------------|
| Connector                    | 1/2" NPT with check valve            |
| Pressure rating              | 250 psi                              |
| Purpose                      | Initial commissioning purge + post-maintenance dry gas fill |
| Gas                          | N2 (industrial grade) or dry air     |

### Annual Pressure Test Port

| Parameter                    | Value                                |
|------------------------------|--------------------------------------|
| Connector                    | 1/4" NPT with cap                    |
| Pressure rating              | 500 psi                              |
| Purpose                      | Pressure decay leak test (§19)       |
| Test gauge                   | Calibrated, 0–1,000 Pa or 0–10 kPa   |

### IR Camera Port (External)

| Parameter                    | Value                                |
|------------------------------|--------------------------------------|
| Connector                    | M12 A-coded, 4-pin (PoE)             |
| Camera                       | FLIR A500-EST or equivalent          |
| Purpose                      | External thermal imaging for annual skin temperature survey |
| BMS integration              | Optional — camera is handheld during survey |

---

## §15 GROUNDING & BONDING INTERFACE

### Cassette-to-Platform Ground

Single 50 mm² bond cable from the Cassette's ELEC ECP ground stud (#9 in §3) to the platform's single-point ground (SPG).

- Cable length: as required, no more than 10 m
- Routing: shortest practical path, no sharp bends
- Termination: compression lug, stainless hardware, conductive anti-seize
- Inspection: visual + continuity check at commissioning and annually

### Bond Resistance

Target: Cassette frame to platform SPG ≤ 1 Ω measured.

### What the Platform Provides

- SPG bar or rod accessible within 10 m of Cassette ELEC end
- Platform-wide bonding network at ≤ 1 Ω to earth/sea ground
- Documented grounding study per site

### Offshore Bonding

In addition to SPG:
- Cassette frame bonded to platform hull at ISO corner castings (all four)
- Bonding jumpers across every cable tray seam crossing between pod and platform
- Cathodic protection coordination (platform-side responsibility)

---

## §16 ENVIRONMENTAL RATINGS — ONSHORE vs OFFSHORE

### Onshore Variant

| ECP Component                  | Rating                             |
|--------------------------------|------------------------------------|
| Outer cover                    | NEMA 3R                            |
| Connectors (electrical)        | IP67                               |
| Connectors (data)              | IP54 minimum                       |
| Penetration gaskets            | Silicone single-bulb               |
| Fasteners                      | Stainless (18-8 or 316)            |
| Cover hardware                 | Dzus quarter-turn latches          |

### Offshore Variant

| ECP Component                  | Rating                             |
|--------------------------------|------------------------------------|
| Outer cover                    | NEMA 4X                            |
| Connectors (electrical)        | IP67 minimum, marine-grade         |
| Connectors (data)              | IP66 minimum                       |
| Penetration gaskets            | Silicone bulb + EPDM secondary     |
| Fasteners                      | Monel or Inconel                   |
| Cover hardware                 | Stainless bolts on 150 mm pitch    |
| EMI gaskets                    | Required at every penetration       |
| Cathodic protection            | Sacrificial anodes at bolted seams  |

---

## §17 CONNECTOR SPECIFICATIONS (REFERENCED)

Authoritative vendor products for each connector type. Equivalents acceptable only with Cassette integrator written approval.

| Function                     | Vendor Product Reference                    |
|------------------------------|---------------------------------------------|
| 800 V DC main                | Stäubli CombiTac 2500 series                |
| 415 V AC main                | Cam-Lok E1016 series (Marinco / Hubbell)    |
| DC-current blind-mate (internal) | Stäubli CombiTac 400 (rack feeds)       |
| UQD (fluid disconnect)       | Stäubli UQD-16                              |
| CHW Victaulic                | Victaulic Style 77, 6" (DN150) grooved, ductile iron |
| MPO fiber bulkhead           | Corning PRETIUM EDGE or Panduit FlexPlus    |
| Single-mode LC/APC           | Corning or Panduit OptiCam                  |
| Cat6A RJ-45 sealed           | Neutrik NE8FDX or Switchcraft EHRJ45P       |
| N-type RF                    | Times Microwave or Amphenol                 |
| MIL-5015 circular (E-stop)   | Amphenol or Souriau 97 series               |
| M12 A-coded                  | Phoenix Contact or Turck                    |
| Pin-and-Sleeve IEC 60309     | Mennekes or Meltric                         |
| NPT fittings                 | Swagelok or Parker Hannifin                 |
| Ground stud                  | Thomas & Betts or Burndy compression        |

---

## §18 CABLE SPECIFICATIONS (REFERENCED)

Minimum cable specifications. Higher ratings acceptable.

| Function                   | Cable Type                              |
|----------------------------|-----------------------------------------|
| 800 V DC main              | 2× 70 mm² UL 44 XHHW-2, 2 kV rated      |
| 415 V AC main              | 4× 120 mm² UL 44 XHHW-2 + 50 mm² ground |
| CHW piping                 | 6" (DN150) 304L stainless, ASME B31.3   |
| Munters duct               | 200 mm 304 stainless w/ 25 mm CCF       |
| MPO fiber trunk            | OS2 SMF, OFNR or OFNP riser             |
| Cat6A OOB                  | Shielded (F/UTP or S/FTP), 600 V plenum |
| N-type RF                  | LMR-400, 50 Ω, low-loss                 |
| MIL-5015 E-stop            | 16 AWG, shielded, teflon jacket         |
| Bonding                    | Bare copper or green-insulated, 50 mm²  |
| Offshore upgrades          | MIL-DTL-24643 equivalent throughout     |

---

## §19 ACCEPTANCE TESTING AT ECP

Commissioning sign-off requires the following at the ECP interface, in this order:

### 1. Visual & Dimensional

- [ ] All penetrations match §3 / §4 schedule count and location
- [ ] No damaged gaskets
- [ ] All fasteners at specified torque (witness marks)
- [ ] ECP covers open and close cleanly

### 2. Electrical Bonding

- [ ] Cassette frame to SPG: resistance ≤ 1 Ω
- [ ] All bonding jumpers visually verified
- [ ] SPD installed and test-fired

### 3. Electrical Primary (800 V DC or 415 V AC)

- [ ] Polarity verified (DC) or phase rotation verified (AC)
- [ ] Insulation test pass: ≥ 1 GΩ at 1 kV megger
- [ ] Voltage at ECP within spec before main breaker close
- [ ] Cassette main disconnect closes, rectifiers see input

### 4. Fluid

- [ ] Victaulic couplings torqued and pressure-tested to 1.5× working (900 kPa)
- [ ] Cassette primary loop pre-filled and circulating per ADC-CAS-001 §27
- [ ] Water chemistry certified in range at time of connection
- [ ] Isolation valves operate in both directions from BMS command

### 5. Data

- [ ] Each MPO bulkhead attenuation test: ≤ 0.5 dB per pair
- [ ] OOB RJ-45 continuity and PoE negotiation confirmed
- [ ] Starlink and cellular modems obtain signal ≥ -90 dBm
- [ ] GPS antenna locks ≥ 4 satellites within 5 minutes

### 6. Safety

- [ ] E-stop assertion from platform triggers Cassette shutdown within 100 ms
- [ ] E-stop assertion from pod triggers platform test response
- [ ] Key reset functions correctly at ELEC ECP
- [ ] Emergency strobes activate on test

### 7. Environmental

- [ ] ECP covers re-installed to torque spec
- [ ] Pressure decay test: ≤ 100 Pa in 5 min (onshore) / ≤ 50 Pa in 5 min (offshore)
- [ ] IR scan of all penetration gaskets — no cold spots indicating leak

Sign-off witnessed by pod integrator and platform owner representative. Any failed item requires re-test after correction. No partial acceptance.

---

## §20 CHANGE CONTROL

### Authority

Changes to this ICD require written agreement between pod vendor and platform owner. A pod vendor cannot unilaterally change the ECP interface. A platform cannot require Cassette modification without negotiated change.

### Change Categories

**Category A — Non-breaking:** adds a new service without modifying existing ones (e.g., adds a second redundant fiber bulkhead). Requires notification and updated drawing only.

**Category B — Backward-compatible:** modifies an existing service but keeps legacy interface operational (e.g., upgrades fiber from OS2 to OS3 — keeps OS2 path for existing pods).

**Category C — Breaking:** modifies an existing service such that legacy pods do not interoperate. Requires version bump (e.g., Rev 2.0), documented migration path, and joint sign-off.

### Rev History of This ICD

| Rev | Date       | Category | Description                                                      |
|-----|------------|----------|------------------------------------------------------------------|
| 1.0 | 2026-04-19 | Initial  | First release             |
| 2.0 | 2026-04-19 | C (breaking) | CHW: 1,800→2,200 LPM, ΔT 5→11 °C, DN100→DN150 Victaulic (Cassette-COOL-001 §8) |

---

**Cassette — External Connection Panel Interface Control Document**
**Cassette-ECP-001 · Rev 2.0 · 2026-04-19**
**Scott Tomsu · scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana**
**CONFIDENTIAL**
