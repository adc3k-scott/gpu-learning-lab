# Cassette — EXTERNAL CONNECTION PANEL (ECP) INTERFACE CONTROL DOCUMENT

**Document:** Cassette-ECP-001
**Revision:** 1.2
**Date:** 2026-04-22
**Classification:** CONFIDENTIAL

**Purpose:** This document defines the sole physical and logical interface between the Cassette and any upstream platform. Every physical penetration through the Cassette shell — every cable, every pipe, every fiber, every duct that crosses the container boundary — is specified here. No exceptions.

**Prepared by:** Scott Tomsu · CEO / Chief Engineer
scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana

---

## TABLE OF CONTENTS

- §1  Purpose & Scope
- §2  ECP Zones — ELEC End and CDU End
- §3  ELEC ECP — Complete Penetration Schedule
- §4  CDU ECP — Complete Penetration Schedule
- §5  Electrical Interface — 480 V AC Primary
- §6  Electrical Interface — Maintenance AC Ports (Cam-Lok)
- §7  Fluid Interface — PG25 Primary Coolant
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

- Not a platform design document. The Cassette makes no assumptions about upstream source topology.
- Not a substitute for ELEC-001 (internal electrical), BOM-001 (bill of materials), or INT-001 (integration spec). Those documents govern internal pod design. This document governs only what crosses the boundary.

### Rule of Contract

If a service is not listed in §3 or §4, it does not exist at the ECP. If a service is listed but its detailed specification is ambiguous, the numbered specification section (§5–§15) is authoritative.

### Two-Zone Architecture

The Cassette has two ECP zones at opposite short ends:

- **ELEC ECP** (end opposite CDU): all electrical service, BMS uplink, E-stop
- **CDU ECP** (Service End Zone — where the external CDU skid and Munters skid connect): all fluid service, InfiniBand, Munters ducts, test ports

This separation is deliberate — electrical and fluid services enter from opposite ends, eliminating cable/pipe crossovers inside the pod and giving service crews orthogonal approach paths.

### Architecture Note — No Internal CDU

The Cassette contains no internal CDU unit. It is a sealed PG25 appliance. PG25 propylene glycol 25% v/v primary coolant circulates through the pod, absorbs heat at the rack cold plates (R1–R9) and control rack heat exchanger (R10), then exits at the CDU ECP for external rejection. Heat rejection to the intermediate loop is performed by the external CDU skid (COOL2-001, procured separately).

### Architecture Note — 480 V AC at the Boundary

The Cassette accepts 480 V AC 3-phase at the ELEC ECP. Conversion to 800 V DC occurs inside the pod via 5× Delta 660 kW in-row power racks (R11–R15). The 800 V DC bus is internal only and never appears at any ECP penetration.

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

Located at the short end of the Cassette at the Service End Zone, where the external CDU skid and Munters skid connect.

| Parameter                  | Value                              |
|----------------------------|------------------------------------|
| Zone footprint             | Entire short end face, 2,438 × 2,896 mm exterior |
| Usable penetration area    | 2,000 × 2,400 mm centered          |
| Recessed housing depth     | 400 mm (accommodates QBH-150 DN150 QD fittings + Munters 400×250 mm duct elbows) |
| Access for service         | Hinged outer cover, 1,600 × 2,000 mm |
| Cover fastener             | 12 quarter-turn Dzus latches (onshore) or 12 stainless bolts (offshore) |
| Interior side              | Inside CDU end zone (1,500 mm interior length) |

### ECP Cover Inspection Windows

Both ECP covers have three 200 × 150 mm polycarbonate inspection windows (2,000 J impact rating):
- Cable/duct entry status (LED backlit, shows connection status)
- Primary disconnect position indicator (ELEC ECP) / QD connection status indicator (CDU ECP)
- Bond stud and grounding visual

---

## §3  ELEC ECP — COMPLETE PENETRATION SCHEDULE

All penetrations at the ELEC ECP, in physical order from top to bottom of the panel:

| #  | Service                              | Connector / Interface                              | Rating                    | Qty      |
|----|--------------------------------------|----------------------------------------------------|---------------------------|----------|
|  1 | GPS antenna (time sync)              | SMA connector, active antenna with DC pass         | IP66, surge-protected     | 1        |
|  2 | Starlink antenna feed                | N-type connector, 50 Ω                             | IP66, marine rated        | 1        |
|  3 | Cellular antenna feed                | N-type connector, 50 Ω                             | IP66, marine rated        | 1        |
|  4 | BMS fiber uplink (primary)           | LC/APC duplex, single-mode OS2                     | IP66 w/ EMI gland         | 2 fibers |
|  5 | BMS fiber uplink (redundant)         | LC/APC duplex, single-mode OS2                     | IP66 w/ EMI gland         | 2 fibers |
|  6 | 480 V AC 3-phase primary input       | Eaton Pow-R-Way III wall entry fitting — 6,000 A, 600 V AC, UL 857; ECP panel cutout ≈ 400 × 280 mm with mounting flange; IP54 onshore / IP66 weatherproof housing offshore; catalog bus duct adapter to Magnum DS line stabs (E-01 closed) | 4,179 A/phase operating, 6,000 A rated [LONG LEAD] | 1 set    |
|  7 | Maintenance AC access (L1/L2/L3/N/G) | Cam-Lok E1016 series — maintenance only, not primary feed | IP67, 400 A          | 5        |
|  8 | Chassis ground / bond                | 50 mm² bond stud, M12 stainless                    | 10,000 A fault            | 1        |
|  9 | Emergency stop (hardwire IN)         | MIL-DTL-5015 6-pin connector, 24 V DC dry          | IP67                      | 1        |
| 10 | Emergency stop (hardwire OUT)        | MIL-DTL-5015 6-pin connector, 24 V DC dry          | IP67                      | 1        |
| 11 | External strobe power                | Integral to ECP housing                            | —                         | 1        |

### Physical Arrangement (ELEC ECP)

```
+--------------------------------------------------+
|  [1]GPS   [2]Starlink   [3]Cell               +  |  ← Top (antennas)
|                                                  |
|  [4]BMS fiber primary   [5]BMS fiber redundant   |  ← Upper (data)
|                                                  |
|  [9]E-STOP IN           [10]E-STOP OUT           |  ← Mid (safety)
|                                                  |
|  [6] 480V AC 3-PH PRIMARY                        |  ← Lower (power primary)
|      Bus duct entry — TBD per E-01               |
|                                                  |
|  [7] Cam-Lok L1 L2 L3 N G (maintenance only)     |  ← Maintenance AC
|                                                  |
|  [8] GND stud                            [11]    |  ← Bottom corners
+--------------------------------------------------+
     ELEC ECP outer cover removed
```

---

## §4  CDU ECP — COMPLETE PENETRATION SCHEDULE

All penetrations at the CDU ECP (Service End Zone), in physical order:

| #  | Service                              | Connector / Interface                             | Rating                              | Qty        |
|----|--------------------------------------|---------------------------------------------------|-------------------------------------|------------|
|  1 | PG25 supply QD                       | Stäubli QBH-150 DN150 dry-break QD                | 16 bar, 25–70 °C  [LONG LEAD]       | 1          |
|  2 | PG25 return QD                       | Stäubli QBH-150 DN150 dry-break QD                | 16 bar, 25–70 °C  [LONG LEAD]       | 1          |
|  3 | Munters process air supply (dry)     | 400×250 mm insulated flanged duct, 4-bolt         | Sealed, vapor barrier               | 1          |
|  4 | Munters process air return (wet)     | 400×250 mm insulated flanged duct, 4-bolt         | Sealed                              | 1          |
|  5 | InfiniBand compute uplink            | MPO-24 bulkhead, single-mode OS2                  | IP54 (onshore) / IP66 (offshore)    | 1 assembly |
|  6 | InfiniBand compute downlink          | MPO-24 bulkhead, single-mode OS2                  | IP54 / IP66                         | 1 assembly |
|  7 | InfiniBand compute redundant         | MPO-24 bulkhead, single-mode OS2                  | IP54 / IP66                         | 1 assembly |
|  8 | Out-of-band management A             | RJ-45 Cat6A shielded, Neutrik NE8FDX              | IP67                                | 1          |
|  9 | Out-of-band management B             | RJ-45 Cat6A shielded, Neutrik NE8FDX              | IP67                                | 1          |
| 10 | Munters power feed (from platform)   | Pin-and-Sleeve IEC 60309, 480 V AC 3-ph, spec TBD per MO-03 (~25 kW) | IP67   | 1          |
| 11 | PG25 fill / drain port               | 1/2" NPT female with ball valve + cap             | 16 bar                              | 1          |
| 12 | Condensate drain                     | 1" NPT female, with check valve + fume loop       | Gravity                             | 1          |
| 13 | Leak-detection emergency drain       | 1" NPT female, solenoid-actuated                  | Normally closed                     | 1          |
| 14 | N2 fill / purge port                 | 1/2" NPT with check valve                         | 250 psi                             | 1          |
| 15 | Annual pressure test port            | 1/4" NPT with cap                                 | 500 psi                             | 1          |
| 16 | External IR camera port              | M12 A-coded, 4-pin (PoE)                          | IP67                                | 1          |

### Physical Arrangement (CDU ECP)

```
+--------------------------------------------------+
|  [3] Munters supply duct  [4] Munters return duct|  ← Top (air)
|  (400×250 mm flanged)                            |
|                                                  |
|  [5]IB-UP   [6]IB-DN   [7]IB-RED (MPO-24 bulkhds)|  ← Upper (fiber)
|  [8]OOB-A   [9]OOB-B   [16]IR-CAM (small conn.) |
|                                                  |
|  [10] Munters power 480V AC 3-ph  ~25 kW TBD MO-03|  ← Mid (power)
|                                                  |
|  [1] PG25 supply   QBH-150 DN150 QD              |  ← Lower (fluid)
|  [2] PG25 return   QBH-150 DN150 QD              |
|                                                  |
|  [11]PG25fill [12]Cond. [13]Leak [14]N2 [15]Test |  ← Bottom (test/drain)
+--------------------------------------------------+
     CDU ECP outer cover removed
```

---

## §5  ELECTRICAL INTERFACE — 480 V AC PRIMARY

### Architecture

The Cassette accepts 480 V AC 3-phase at the ELEC ECP. No DC voltage appears at any external connection point. Internal AC-to-DC conversion is performed by 5× Delta 660 kW in-row power racks (R11–R15) inside the pod. The internal 800 V DC bus is isolated from the ECP entirely.

### Specification

| Parameter                          | Value                                                    |
|------------------------------------|----------------------------------------------------------|
| Nominal voltage                    | 480 V AC line-to-line ±5%                                |
| Operating range                    | 456–504 V AC                                             |
| Frequency                          | 60 Hz ±3% (50 Hz accepted; Delta racks rated both)       |
| Phase configuration                | 3-phase, 3-wire + ground (no neutral required)           |
| Phase imbalance (voltage)          | ≤ 2% steady-state                                        |
| THDv at ECP                        | ≤ 5% per IEEE 519                                        |
| Installed capacity                 | 3,300 kW (5 × 660 kW Delta in-row racks)                 |
| Operating load — NVL72 tier        | 1,080 kW IT; ~1,200 kW facility draw                     |
| Operating load — CPX tier          | 1,440 kW IT; ~1,600 kW facility draw                     |
| AC primary current (installed)     | 4,179 A/phase (3,300 kW ÷ (√3 × 480 × 0.95 PF))         |
| AC primary current (operating CPX) | ~2,025 A/phase                                           |
| NEC 125% rating (installed basis)  | 5,224 A minimum — 6,000 A main disconnect specified      |
| Fault current withstand            | Per main disconnect rating (Eaton Magnum DS / Siemens WL / ABB Emax2) |
| ECP connection method              | Eaton Pow-R-Way III wall entry fitting — 6,000 A, 600 V AC, UL 857; cutout ≈ 400 × 280 mm; IP54 onshore / IP66 offshore (E-01 closed) |
| Internal pod landing               | Eaton Magnum DS, 6,000 A, 480 V AC, UL 1066 — motor-operated (MODS), shunt trip 24 V DC (E-02 closed) |

### E-01 Closed — Bus Duct ECP Connector

Down-selected 2026-04-22: Eaton Pow-R-Way III wall entry fitting, 6,000 A rated, 600 V AC, UL 857. ECP panel cutout approximately 400 × 280 mm with mounting flange. IP54 standard; IP66 weatherproof housing for offshore variant. Mates to Eaton Magnum DS line-side bus stabs via Eaton catalog bus duct adapter — no custom coupling required. Exact product code (Pow-R-Way IIIx or extended-rating equivalent at 6,000 A) to be confirmed with Eaton engineering before fabrication PO. Standard Cam-Lok connectors (400 A each) confirmed impractical at 4,179 A/phase — 11 per phase required; not used as primary feed. See ELEC-001 §18.

### What the Cassette Guarantees

- Accepts 480 V AC input within the operating range without fault
- Internal 800 V DC bus remains fully isolated from the ECP; Bender iso-PV1685 IMD monitors internal bus continuously
- Reports AC input voltage, current, and kW to BMS at 1 Hz minimum
- Main disconnect opens within 100 ms on E-stop signal or BMS critical fault

### What the Cassette Requires From Platform

- Stable 480 V AC 3-phase within the operating range
- Phase rotation confirmed before energization
- THDv ≤ 5% at the ECP
- Upstream overcurrent protection coordinated with pod 6,000 A main disconnect
- Platform-side isolation means for pod service (disconnect upstream of bus duct entry)
- No back-feed permitted: Cassette is a sink, never a source

---

## §6  ELECTRICAL INTERFACE — MAINTENANCE AC PORTS (CAM-LOK)

### Purpose

Five Cam-Lok E1016 ports (L1 / L2 / L3 / N / G) are present at the ELEC ECP for low-current maintenance access only. They are not the primary power feed. The primary feed is the 480 V AC bus duct entry (§5).

### Specification

| Parameter                  | Value                                              |
|----------------------------|----------------------------------------------------|
| Connector                  | Cam-Lok E1016 series, Marinco / Hubbell            |
| Ports                      | L1 / L2 / L3 / N / G (5 connectors)               |
| Rating                     | 400 A per connector, IP67                          |
| Use cases                  | Portable generator tie-in during commissioning; temporary maintenance power with primary bus de-energized |
| Interlock                  | Electrically interlocked with primary bus duct entry — only one path active at a time |
| Primary feed               | Capped with weather-tight cover during normal operation |

### Selection

Cam-Lok ports are capped during normal operation. They are activated only under controlled conditions with the primary bus duct entry isolated and locked out. No simultaneous energization of both paths is permitted.

---

## §7  FLUID INTERFACE — PG25 PRIMARY COOLANT

### Architecture Note

The Cassette contains no internal CDU unit. It is a sealed PG25 appliance. PG25 propylene glycol 25% v/v primary coolant circulates inside the pod, absorbs heat at the rack cold plates (R1–R9) and at the control rack heat exchanger (R10), and exits at the CDU ECP for external rejection. Heat rejection to the intermediate loop is performed by the external CDU skid (COOL2-001, procured separately). The Cassette is the primary-coolant endpoint only.

### Specification

| Parameter                    | Supply (from CDU skid)         | Return (to CDU skid)           |
|------------------------------|--------------------------------|--------------------------------|
| Fluid                        | Propylene glycol 25% v/v (PG25), inhibited, in deionized water | same |
| Supply temperature           | 45 °C (design)                 | —                              |
| Return temperature           | —                              | 55–60 °C (design)              |
| ΔT design                    | 10–15 °C                       | —                              |
| Flow (design)                | ~1,650 LPM (preliminary — COOL-001 pending) | matched       |
| Working pressure             | 16 bar                         | 16 bar                         |
| Max pressure (test)          | 24 bar (1.5× working)          | —                              |
| Connector                    | Stäubli QBH-150 DN150 dry-break QD | same                       |
| Hose / piping material       | 304 SS braided flexible hose, DN150 5 m (Parker ParFlex 797TC or Gates Mega4000) | same |
| Fluid standard               | OCP Stage 1d primary coolant fluid spec | —                  |

**Note:** Flow and heat load numbers are preliminary for the 9-compute-rack configuration (R1–R9 + R10 control). Cassette-COOL-001 (pending) will confirm final flow spec. Open item C-01. Delta in-row power racks (R11–R15) are air-cooled internally and do not draw from the PG25 circuit.

### Fluid Quality Requirements (CDU Skid / Platform Responsibility)

| Parameter              | Limit                                                   |
|------------------------|---------------------------------------------------------|
| Glycol concentration   | 25% v/v ±2% (inhibited propylene glycol, food-grade acceptable) |
| pH                     | 8.0–9.0 (inhibitor package per manufacturer)            |
| Chlorides              | < 25 mg/L                                               |
| Conductivity           | < 200 μS/cm                                             |
| Total suspended solids | < 5 mg/L                                                |
| Dissolved oxygen       | < 0.1 mg/L                                              |
| Biological load        | Non-detectable (closed loop)                            |

### QD Connector Protocol

QBH-150 dry-break QDs (Stäubli — IN-01 closed; Parker Snap-tite 75 DN150 removed as qualified alternate) lock by quarter-turn. Connection procedure:

1. Verify both halves de-pressurized (< 0.5 bar)
2. Clean face seals with lint-free cloth
3. Align and engage — audible click confirms seating
4. Quarter-turn lock (torque wrench not required — positive engagement by design)
5. Pressurize and verify zero external leakage at connection face

Disconnection reverses steps. PG25 will not drip on disconnect (dry-break design).

### What the Cassette Guarantees

- Removes ~1.0 MW minimum / ~1.4 MW peak heat load into the PG25 return stream (9 compute racks + 1 control rack)
- Return temperature stays within 55–60 °C when supply is maintained at 45 °C ±3 °C
- No chemical addition to PG25 loop (pod-side is sealed)
- Stops drawing flow (internal isolation valve closes) if supply exceeds 65 °C or pressure falls below 5 bar
- PG25 fill volume reported to BMS; low-level alarm before pressure loss

### What the Cassette Requires From Platform (CDU Skid)

- PG25 supply at 45 °C ±3 °C at design flow (COOL-001 to confirm)
- QBH-150 mating half on CDU skid piping (or Parker qualified alternate per IN-01)
- Flow control maintained by CDU skid; Cassette is a passive thermal load
- Expansion tank / makeup reservoir on CDU skid
- Annual glycol chemistry audit

### Fluid Isolation

Motorized isolation valves at both CDU ECP fluid penetrations, pod-side. BMS can command closure on any fluid emergency (leak, sump overflow). CDU skid side should have matching manual valves for service isolation.

---

## §8  FLUID INTERFACE — CONDENSATE & DRAINS

### Condensate Drain

| Parameter                    | Value                                                        |
|------------------------------|--------------------------------------------------------------|
| Source                       | Interior condensation + connection area drip pan             |
| Expected flow                | 0–2 L/hr normal, up to 20 L/hr peak                          |
| Connector                    | 1" NPT female at ECP                                         |
| Check valve                  | Integrated (prevents back-flow)                              |
| Fume loop                    | 150 mm water seal                                            |
| Platform side                | Routed to platform condensate collection or environment per local permit |

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

| Parameter                        | Process Supply (Dry)         | Process Return (Wet)         |
|----------------------------------|------------------------------|------------------------------|
| Duct cross-section               | 400×250 mm rectangular       | 400×250 mm rectangular       |
| Insulation                       | 25 mm closed-cell foam       | 25 mm closed-cell foam       |
| Flange standard                  | 4-bolt rectangular flange    | 4-bolt rectangular flange    |
| Gasket                           | EPDM or silicone             | EPDM or silicone             |
| Flow                             | 600 SCFM (~1,020 m³/hr)      | 600 SCFM                     |
| Temperature                      | 5–30 °C dry                  | 20–30 °C wet                 |
| Interior RH design target        | 10–38% RH (OCP v0.5.0)       | —                            |
| Relative humidity                | 5–30% (Munters output)       | 30–100% (pod return)         |
| Material                         | 304 stainless or aluminum, weather-rated | same               |

### Munters Skid Interface

The Munters DSS Pro (model and airflow TBD per open item MO-03) sits on an external skid. The Cassette provides the duct penetrations; the platform provides the skid, its power (§4 #10), and the duct connections between skid and Cassette.

### What the Cassette Guarantees

- Maintains positive pressure at process return duct
- Returns moist air to Munters within stated flow and temperature window
- Dampers at ECP close on fire suppression activation (prevents Novec escape + prevents duct draft-feeding fire)

### What the Cassette Requires From Platform

- Munters DSS Pro or approved equivalent on external skid per MO-03
- 480 V AC 3-ph power to skid at CDU ECP #10 (spec TBD per MO-03)
- Process air supply at 5–30% RH (Munters output spec)
- Skid Modbus RTU communication routed to OOB network

### Duct Failure Mode

If Munters skid fails or is offline, Cassette continues to operate with elevated interior humidity (up to 50–60% RH). BMS warning alert triggers at humidity > 38% (OCP v0.5.0 upper limit); BMS alarm triggers at > 55% sustained. No automatic pod shutdown — pod tolerates elevated humidity as long as no dew-point breach occurs at cold plates. Note: sustained operation above 38% RH is outside the OCP facility specification and should be flagged to the platform operator.

---

## §10 DATA INTERFACE — INFINIBAND FABRIC

### Specification

| Parameter                        | Value                                      |
|----------------------------------|--------------------------------------------|
| Fabric standard                  | NVIDIA Quantum-X800 InfiniBand NDR         |
| Line rate                        | 400 Gb/s per port                          |
| Fiber type                       | Single-mode OS2 (9/125 μm)                 |
| Bulkhead connector               | MPO-24 female (12 fiber pairs each)        |
| Uplink bandwidth (per bulkhead)  | 24 × 400 Gb/s = 9.6 Tb/s                   |
| Uplink bulkheads                 | 2 primary (uplink + downlink) + 1 redundant |
| Total pod bandwidth              | 28.8 Tb/s aggregate (primary + redundant)  |
| Cable length limit               | 100 m at 400 Gb/s (passive MPO trunk)      |
| Cable length extension           | Active optical if > 100 m                  |

### Physical Arrangement

Three MPO-24 bulkheads at the CDU ECP (#5, #6, #7 in §4 schedule):
- Bulkhead A (uplink): east path to spine switch A
- Bulkhead B (downlink): same spine A return (NDR full-duplex)
- Bulkhead C (redundant): west path to spine switch B (failover)

InfiniBand fabric originates at the Quantum-X800 switch in R10 (control rack), Service End Zone.

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

- BMS telemetry (Jetson Orin aggregate, R10) at 1 Hz normal, event-driven alerts
- Delta in-row power rack status (Redfish, R11–R15)
- Munters skid Modbus RTU-over-Ethernet gateway
- VESDA-E alarms and status
- Novec 1230 panel status
- Console server access to NVIDIA Quantum-X800 switch
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

| Parameter                        | Value                                             |
|----------------------------------|---------------------------------------------------|
| Starlink                         | Maritime (offshore) or Business (onshore) terminal |
| Cellular                         | 4G/5G multi-carrier modem, Cradlepoint or equivalent |
| Antenna mounting                 | On ECP housing exterior (top of ELEC ECP cover)  |
| Feed cables                      | N-type, LMR-400 or better, ≤ 6 m to Jetson Orin  |
| Surge protection                 | Integrated at N-type connector entry              |
| Primary use                      | BMS backhaul when fiber is unavailable            |

### Automatic Failover

Jetson Orin (R10) manages three-tier backhaul:
1. Primary: fiber OOB (always preferred)
2. Secondary: Starlink (auto-activate on fiber loss > 30 sec)
3. Tertiary: cellular (activate on Starlink unavailability)

### Bandwidth Expectations

- Fiber OOB: 1 Gbps typical — full telemetry + firmware push
- Starlink: 50–250 Mbps — telemetry + compressed logs
- Cellular: 5–50 Mbps — critical alerts only; non-essential telemetry suspended

---

## §13 SAFETY INTERFACE — EMERGENCY STOP

### Specification

| Parameter                        | Value                                                |
|----------------------------------|------------------------------------------------------|
| Signal                           | 24 V DC dry contact, fail-safe (energized = safe)    |
| Connector                        | MIL-DTL-5015 6-pin circular                          |
| Redundancy                       | Dual-channel, Category 4 per ISO 13849               |
| Response time                    | ≤ 100 ms pod-side shutdown                           |
| Hardwired (not software)         | Direct to 480 V AC main disconnect trip coil         |

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

Requires physical key-switch reset at the ELEC ECP after BMS verifies safe state. No remote reset. This is by design — an E-stop event means someone must inspect on-site before re-energization.

---

## §14 TEST & COMMISSIONING PORTS

### PG25 Fill / Drain Port

| Parameter                    | Value                                                   |
|------------------------------|---------------------------------------------------------|
| Connector                    | 1/2" NPT female with ball valve + cap                   |
| Pressure rating              | 16 bar                                                  |
| Purpose                      | Initial PG25 fill, post-maintenance refill, and controlled drain |
| Fluid                        | PG25 propylene glycol 25% v/v only                      |

### N2 Fill / Purge Port

| Parameter                    | Value                                                   |
|------------------------------|---------------------------------------------------------|
| Connector                    | 1/2" NPT with check valve                               |
| Pressure rating              | 250 psi                                                 |
| Purpose                      | Initial commissioning purge + post-maintenance dry gas fill |
| Gas                          | N2 (industrial grade) or dry air                        |

### Annual Pressure Test Port

| Parameter                    | Value                                              |
|------------------------------|----------------------------------------------------|
| Connector                    | 1/4" NPT with cap                                  |
| Pressure rating              | 500 psi                                            |
| Purpose                      | Pressure decay leak test (§19)                     |
| Test gauge                   | Calibrated, 0–1,000 Pa or 0–10 kPa                 |

### IR Camera Port (External)

| Parameter                    | Value                                              |
|------------------------------|----------------------------------------------------|
| Connector                    | M12 A-coded, 4-pin (PoE)                           |
| Camera                       | FLIR A500-EST or equivalent                        |
| Purpose                      | External thermal imaging for annual skin temperature survey |
| BMS integration              | Optional — camera is handheld during survey        |

---

## §15 GROUNDING & BONDING INTERFACE

### Cassette-to-Platform Ground

Single 50 mm² bond cable from the Cassette's ELEC ECP ground stud (#8 in §3) to the platform's single-point ground (SPG).

- Cable length: as required, no more than 10 m
- Routing: shortest practical path, no sharp bends
- Termination: compression lug, stainless hardware, conductive anti-seize
- Inspection: visual + continuity check at commissioning and annually

A second 50 mm² bond cable from the CDU ECP housing to the platform SPG is required on all installations — both ends of the Cassette are bonded independently.

### Bond Resistance

Target: Cassette frame to platform SPG ≤ 1 Ω measured at each bond point.

### What the Platform Provides

- SPG bar or rod accessible within 10 m of each Cassette end
- Platform-wide bonding network at ≤ 1 Ω to earth/sea ground
- Documented grounding study per site

### Offshore Bonding

In addition to SPG:
- Cassette frame bonded to platform hull at ISO corner castings (all four)
- Bonding jumpers across every cable tray seam crossing between pod and platform
- Cathodic protection coordination (platform-side responsibility)

### Internal DC Bus Grounding Note

The internal 800 V DC bus is an ungrounded IT system (OCP Stage 1d). It is not bonded to chassis ground. The Bender iso-PV1685 IMD monitors internal bus insulation resistance continuously and alerts BMS on fault. Platform grounding system interfaces only with the 480 V AC side via the main disconnect's grounding conductor.

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

| ECP Component                  | Rating                              |
|--------------------------------|-------------------------------------|
| Outer cover                    | NEMA 4X                             |
| Connectors (electrical)        | IP67 minimum, marine-grade          |
| Connectors (data)              | IP66 minimum                        |
| Penetration gaskets            | Silicone bulb + EPDM secondary      |
| Fasteners                      | Monel or Inconel                    |
| Cover hardware                 | Stainless bolts on 150 mm pitch     |
| EMI gaskets                    | Required at every penetration       |
| Cathodic protection            | Sacrificial anodes at bolted seams  |

---

## §17 CONNECTOR SPECIFICATIONS (REFERENCED)

Authoritative vendor products for each connector type. Equivalents acceptable only with Cassette integrator written approval.

| Function                            | Vendor Product Reference                               |
|-------------------------------------|--------------------------------------------------------|
| 480 V AC primary (bus duct)         | Eaton Pow-R-Way III wall entry fitting — 6,000 A, 600 V AC, UL 857 (E-01 closed) |
| 480 V AC maintenance (Cam-Lok)      | Cam-Lok E1016 series (Marinco / Hubbell) — maintenance only |
| PG25 primary QD (CDU ECP)          | Stäubli QBH-150 DN150 dry-break — confirmed primary (IN-01 closed). Parker Snap-tite 75 DN150 removed as qualified alternate — poppet-valve design, not dry-break; spills ~2–5 mL on disconnect. Emergency alternate only, requires dry-break verification before any use. Offshore alt: Tema DryBreak DB-150 (MODU/subsea only). |
| MPO fiber bulkhead                  | Corning PRETIUM EDGE or Panduit FlexPlus               |
| Single-mode LC/APC                  | Corning or Panduit OptiCam                             |
| Cat6A RJ-45 sealed                  | Neutrik NE8FDX or Switchcraft EHRJ45P                  |
| N-type RF                           | Times Microwave or Amphenol                            |
| MIL-5015 circular (E-stop)          | Amphenol or Souriau 97 series                          |
| M12 A-coded                         | Phoenix Contact or Turck                               |
| Pin-and-Sleeve IEC 60309 (Munters power) | Mennekes or Meltric                               |
| NPT fittings                        | Swagelok or Parker Hannifin                            |
| Ground stud                         | Thomas & Betts or Burndy compression                   |

---

## §18 CABLE SPECIFICATIONS (REFERENCED)

Minimum cable specifications at the ECP boundary. Higher ratings acceptable.

| Function                            | Cable Type / Notes                                          |
|-------------------------------------|-------------------------------------------------------------|
| 480 V AC primary (ECP entry)        | Bus duct — TBD per E-01; no cable at ECP primary penetration |
| 480 V AC maintenance (Cam-Lok)      | 4× 120 mm² UL 44 XHHW-2 + 50 mm² ground (maintenance use only) |
| Per-Delta-rack AC feeder (internal) | 2× 300 mm² per phase + 95 mm² G per feeder, ~5 m per rack — inside pod only, not at ECP |
| PG25 primary hose                   | 304 SS braided flexible hose, DN150 5 m — Parker ParFlex 797TC or Gates Mega4000 |
| Munters duct                        | 400×250 mm rectangular, 304 stainless w/ 25 mm closed-cell foam |
| MPO fiber trunk                     | OS2 SMF, OFNR or OFNP riser                                 |
| Cat6A OOB                           | Shielded (F/UTP or S/FTP), 600 V plenum                     |
| N-type RF                           | LMR-400, 50 Ω, low-loss                                     |
| MIL-5015 E-stop                     | 16 AWG, shielded, Teflon jacket                             |
| Bonding                             | Bare copper or green-insulated, 50 mm²                      |
| Offshore upgrades                   | MIL-DTL-24643 equivalent throughout                         |

---

## §19 ACCEPTANCE TESTING AT ECP

Commissioning sign-off requires the following at the ECP interface, in this order:

### 1. Visual & Dimensional

- [ ] All penetrations match §3 / §4 schedule count and location
- [ ] No damaged gaskets
- [ ] All fasteners at specified torque (witness marks)
- [ ] ECP covers open and close cleanly
- [ ] Bus duct entry fitting (§5) installed and sealed per E-01 product specification

### 2. Electrical Bonding

- [ ] Cassette ELEC end frame to SPG: resistance ≤ 1 Ω
- [ ] Cassette CDU end frame to SPG: resistance ≤ 1 Ω
- [ ] All bonding jumpers visually verified
- [ ] SPD installed and test-fired

### 3. Electrical Primary — 480 V AC

- [ ] Phase rotation verified (A-B-C) at ECP before main disconnect close
- [ ] Insulation test of internal wiring pass: ≥ 1 GΩ at 1 kV megger
- [ ] Voltage at ECP within 456–504 V AC range on all three phases before main breaker close
- [ ] Cassette 480 V AC main disconnect (6,000 A) closes
- [ ] All 5 Delta in-row power racks (R11–R15) confirm AC input via BMS / Redfish
- [ ] Cam-Lok maintenance ports verified capped and interlocked
- [ ] Internal 800 V DC bus voltage confirmed at 800 V ±5% via BMS after Delta rack energization
- [ ] Bender iso-PV1685 IMD reports healthy insulation on internal 800 V DC bus

### 4. Fluid — PG25 Primary Coolant

- [ ] QBH-150 supply QD (#1) mated — audible click, zero-leak verified at connection face
- [ ] QBH-150 return QD (#2) mated — audible click, zero-leak verified at connection face
- [ ] PG25 glycol concentration certified 25% v/v ±2% at time of first fill
- [ ] Pod PG25 loop pressurized to 24 bar (1.5× working); 30-minute hold; ≤ 0.2 bar drop acceptable
- [ ] Supply RTD and return RTD within ±1 °C of each other at equal flow conditions before heating
- [ ] Isolation valves operate in both directions from BMS command
- [ ] PG25 fill level and pressure confirmed in BMS; low-level alarm activates on test trigger

### 5. Data

- [ ] Each MPO bulkhead attenuation test: ≤ 0.5 dB per pair
- [ ] OOB RJ-45 continuity and PoE negotiation confirmed (both ports A and B)
- [ ] Starlink and cellular modems obtain signal ≥ -90 dBm
- [ ] GPS antenna locks ≥ 4 satellites within 5 minutes

### 6. Safety

- [ ] E-stop assertion from platform triggers Cassette 480 V AC main disconnect open within 100 ms
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

**Category A — Non-breaking:** adds a new service without modifying existing ones. Requires notification and updated drawing only.

**Category B — Backward-compatible:** modifies an existing service but keeps legacy interface operational. Requires version bump and documentation.

**Category C — Breaking:** modifies an existing service such that existing integrations do not interoperate. Requires version bump, documented migration path, and joint sign-off.

### Open Items Affecting This ICD

| ID    | Section | Description                                          | Status  |
|-------|---------|------------------------------------------------------|---------|
| E-01  | §3, §5  | 480 V AC ECP primary connector — **CLOSED 2026-04-22.** Eaton Pow-R-Way III wall entry fitting, 6,000 A, 600 V AC, UL 857. Cutout ≈ 400 × 280 mm. Confirm product code with Eaton before fabrication PO. See §5 and ELEC-001 §18. | Closed |
| E-02  | §5      | 480 V AC main disconnect — **CLOSED 2026-04-22.** Eaton Magnum DS, 6,000 A, UL 1066, motor-operated (MODS), shunt trip 24 V DC. See ELEC-001 §18 and BOM-001 §9. | Closed |
| IN-01 | §4, §7  | PG25 QD selection — **CLOSED 2026-04-22.** Stäubli QBH-150 DN150 confirmed primary. Parker Snap-tite 75 removed as qualified alternate — poppet valve, not dry-break. See §7 and BOM-001 §5.2. | Closed |
| MO-03 | §9      | Munters DSS Pro model confirmation, airflow, FW coil ΔP, CHP regen interface | Open |
| C-01  | §7      | PG25 flow confirmation for 9-compute-rack config — COOL-001 pending | Open |

---

**Cassette — External Connection Panel Interface Control Document**
**Cassette-ECP-001 · Rev 1.2 · 2026-04-22**
**Scott Tomsu · scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana**
**CONFIDENTIAL**
