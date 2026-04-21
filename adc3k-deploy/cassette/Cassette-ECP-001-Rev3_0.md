# Cassette — EXTERNAL CONNECTION PANEL (ECP) INTERFACE CONTROL DOCUMENT

**Document:** Cassette-ECP-001
**Revision:** 3.0
**Date:** 2026-04-20
**Classification:** CONFIDENTIAL
**Companion documents:** Cassette-INT-001 Rev 3.0, Cassette-COOL-002 Rev 1.0, Cassette-CDUSKID-001 Rev 1.0, Cassette-ELEC-001 Rev 1.1, Cassette-FIRE-001 Rev 1.1, Cassette-BOM-001 Rev 3.0 (pending), Cassette-MASS-001 Rev 3.0 (pending)

**Purpose:** This document defines the sole physical and logical interface between the Cassette and any upstream platform. Anyone integrating a Cassette — platform electrical, mechanical, controls, or operations — works from this document. No exceptions.

| Rev | Date       | Description                                                       |
|-----|------------|-------------------------------------------------------------------|
| 1.0 | 2026-04-19 | Initial release |
| 2.0 | 2026-04-19 | CHW interface corrected: 1,800→2,200 LPM, ΔT 5→11 °C, DN100→DN150 Victaulic at CDU ECP (per Cassette-COOL-001 §8) |
| 2.1 | 2026-04-19 | Rev 2.0 cleanup: §4 ASCII diagram 4"→DN150, §5 main cable spec corrected to laminated bus bar, §17 connector reference UQD-16→UQD-25 |
| 2.2 | 2026-04-19 | Companion document cross-references updated; no interface changes |
| **3.0** | **2026-04-20** | **BREAKING CHANGE. External CDU architecture (COOL-002/CDUSKID-001) adopted. CDU-end ECP penetrations #1 and #2 changed from DN150 Victaulic CHW to DN150 PG25 quick-disconnects (Stäubli QBH-150 preferred). CHW penetrations deleted entirely — no CHW at Cassette ECP. §7 renamed from "Chilled Water" to "Primary PG25 Coolant" and rewritten. CDU power penetration (#10) deleted — no internal CDU. Condensate drain (#13) scope reduced to Munters only. §19 acceptance test updated.** |

**Prepared by:** Scott Tomsu · CEO / Chief Engineer
scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana

---

## TABLE OF CONTENTS

- §1  Purpose & Scope
- §2  ECP Zones — ELEC End and CDU End (Rev 3.0 — renamed)
- §3  ELEC ECP — Complete Penetration Schedule
- §4  CDU ECP — Complete Penetration Schedule (Rev 3.0 — PG25 QDs)
- §5  Electrical Interface — 800 V DC Primary
- §6  Electrical Interface — 415 V AC Alternative
- §7  Fluid Interface — Primary PG25 Coolant (Rev 3.0 — was Chilled Water)
- §8  Fluid Interface — Condensate & Drains (Rev 3.0 — reduced scope)
- §9  Fluid Interface — Munters Ducts
- §10 Data Interface — InfiniBand Fabric
- §11 Data Interface — Out-of-Band Management
- §12 Data Interface — Starlink / Cellular Antennas
- §13 Safety Interface — Emergency Stop
- §14 Test & Commissioning Ports
- §15 Grounding & Bonding Interface
- §16 Environmental Ratings — Onshore vs Offshore
- §17 Connector Specifications (Referenced)
- §18 Cable & Hose Specifications (Referenced) (Rev 3.0)
- §19 Acceptance Testing at ECP (Rev 3.0)
- §20 Change Control
- §21 Revision Impact Table (Rev 3.0)

---

## §1  PURPOSE & SCOPE

### What This Document Is

The ECP Interface Control Document (ICD) is the contract between the Cassette and the platform. Every physical penetration through the Cassette shell, every cable, every pipe, every fiber that crosses the container boundary is specified here — no more, no less.

### What This Document Is Not

- Not a platform design document (Cassette makes no assumptions about upstream).
- Not a CDU specification (see Cassette-CDUSKID-001 for the external CDU skid).
- Not a cooling system design (see Cassette-COOL-002 for the end-to-end cooling architecture).

### Rule of Contract

If a service is not listed in §3 or §4, it does not exist at the ECP. If a service is listed but its detailed specification is ambiguous, the numbered specification section (§5–§15) is authoritative.

### Two-Zone Architecture (Rev 3.0 — Refined)

The Cassette has two ECP zones at opposite short ends:

- **ELEC ECP** (end opposite Service End Zone): all electrical service, BMS uplink, E-stop, antennas
- **CDU ECP** (end with Service End Zone): **primary PG25 coolant QDs**, InfiniBand, Munters ducts, test ports

**Rev 3.0 note:** The "CDU ECP" name is retained for continuity with drawings and procedures. In Rev 3.0 there is no internal CDU — the CDU-end ECP is now the primary-coolant and data interface. The name remains; the contents changed.

This separation is deliberate — electrical and fluid services enter from opposite ends, eliminating the possibility of cable/pipe crossovers inside the pod and giving service crews orthogonal approach paths.

---

## §2  ECP ZONES — ELEC END AND CDU END (REV 3.0 — RENAMED)

### ELEC ECP — Dimensions & Layout

Located at the short end of the Cassette opposite the Service End Zone.

| Parameter                  | Value                              |
|----------------------------|------------------------------------|
| Zone footprint             | Entire short end face, 2,438 × 2,896 mm exterior |
| Usable penetration area    | 2,000 × 2,400 mm centered          |
| Recessed housing depth     | 300 mm (weather protection + service loop) |
| Access for service         | Hinged outer cover, 1,600 × 2,000 mm |
| Cover fastener             | 12 quarter-turn Dzus latches (onshore) or 12 stainless bolts (offshore) |
| Interior side              | Inside ELEC end zone (1,200 mm interior length) |

### CDU ECP — Dimensions & Layout (Rev 3.0 Clarified)

Located at the short end of the Cassette adjacent to the Service End Zone (per INT-001 Rev 3.0 §5).

| Parameter                  | Value                              |
|----------------------------|------------------------------------|
| Zone footprint             | Entire short end face, 2,438 × 2,896 mm exterior |
| Usable penetration area    | 2,000 × 2,400 mm centered          |
| Recessed housing depth     | **350 mm (Rev 3.0)** — reduced from 400 mm Rev 2.2 (no Victaulic elbow clearance needed for PG25 QDs) |
| Access for service         | Hinged outer cover, 1,600 × 2,000 mm |
| Cover fastener             | 12 quarter-turn Dzus latches (onshore) or 12 stainless bolts (offshore) |
| Interior side              | Inside Service End Zone (1,200 mm per INT-001 Rev 3.0) |

### ECP Cover Inspection Windows

Both ECP covers have three 200 × 150 mm polycarbonate inspection windows (2,000 J impact rating):
- Cable entry status (LED backlit, shows connection status)
- **CDU ECP Rev 3.0**: PG25 QD connection status (seated / unseated indicator)
- Bond stud and grounding visual

---

## §3  ELEC ECP — COMPLETE PENETRATION SCHEDULE

Unchanged from Rev 2.2. All penetrations at the ELEC ECP, in physical order from top to bottom of the panel:

| # | Service                         | Connector / Interface                        | Rating            | Qty |
|---|----------------------------------|----------------------------------------------|-------------------|-----|
| 1 | GPS antenna (time sync)          | SMA connector, active antenna with DC pass   | IP66, surge-protected | 1   |
| 2 | Starlink antenna feed            | N-type connector, 50 Ω                       | IP66, marine rated| 1   |
| 3 | Cellular antenna feed            | N-type connector, 50 Ω                       | IP66, marine rated| 1   |
| 4 | BMS fiber uplink (primary)       | LC/APC duplex, single-mode OS2               | IP66 w/ EMI gland | 2 fibers |
| 5 | BMS fiber uplink (redundant)     | LC/APC duplex, single-mode OS2               | IP66 w/ EMI gland | 2 fibers |
| 6 | 800 V DC primary positive        | Stäubli CombiTac 2500 series, laminated bus bar landing | IP67, 2,500 A | 1 |
| 7 | 800 V DC primary negative        | Stäubli CombiTac 2500 series, laminated bus bar landing | IP67, 2,500 A | 1 |
| 8 | 415 V AC 3-ph alternate input    | Cam-Lok E1016 series (L1/L2/L3/N/G), optional | IP67, 400 A      | 5 (if used) |
| 9 | Chassis ground / bond            | 50 mm² bond stud, M12 stainless              | 10,000 A fault   | 1   |
|10 | Emergency stop (hardwire IN)     | MIL-DTL-5015 6-pin connector, 24 V DC dry    | IP67              | 1   |
|11 | Emergency stop (hardwire OUT)    | MIL-DTL-5015 6-pin connector, 24 V DC dry    | IP67              | 1   |
|12 | External strobe power            | Integral to ECP housing                      | —                 | 1   |

### Physical Arrangement (ELEC ECP — Unchanged)

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

## §4  CDU ECP — COMPLETE PENETRATION SCHEDULE (REV 3.0 — PG25 QDs)

All penetrations at the CDU ECP, in physical order. **Rev 3.0 changes marked with ★:**

| # | Service                         | Connector / Interface                     | Rating            | Qty |
|---|----------------------------------|-------------------------------------------|-------------------|-----|
| **★1** | **Primary PG25 supply to skid** | **Stäubli QBH-150 QD (or Parker Snap-tite 75 alternate), DN150 bore, dry-break** | **16 bar, 70 °C** | **1** |
| **★2** | **Primary PG25 return from skid** | **Stäubli QBH-150 QD (or Parker Snap-tite 75 alternate), DN150 bore, dry-break** | **16 bar, 70 °C** | **1** |
| 3 | Munters process air supply (dry) | 200 mm insulated flanged duct, 4-bolt    | Sealed, vapor barrier | 1   |
| 4 | Munters process air return (wet) | 200 mm insulated flanged duct, 4-bolt    | Sealed           | 1   |
| 5 | InfiniBand compute uplink        | MPO-24 bulkhead, single-mode OS2         | IP54 (onshore) / IP66 (offshore) | 1 assembly |
| 6 | InfiniBand compute downlink      | MPO-24 bulkhead, single-mode OS2         | IP54 / IP66      | 1 assembly |
| 7 | InfiniBand compute redundant     | MPO-24 bulkhead, single-mode OS2         | IP54 / IP66      | 1 assembly |
| 8 | Out-of-band management A         | RJ-45 Cat6A shielded, Neutrik NE8FDX     | IP67             | 1   |
| 9 | Out-of-band management B         | RJ-45 Cat6A shielded, Neutrik NE8FDX     | IP67             | 1   |
| **~~10~~** | **~~CDU power feed (from platform)~~** | **~~Pin-and-Sleeve IEC 60309~~** | **~~DELETED — no internal CDU~~** | **0** |
|11 | Munters power feed (from platform)| Pin-and-Sleeve IEC 60309, 80 A 3-ph     | IP67             | 1   |
|12 | Munters Modbus RTU (RS-485)      | M12 A-coded, 5-pin                       | IP67             | 1   |
| **★13** | **Condensate drain (Munters only)** | **1" NPT female, with check valve + fume loop** | **Gravity** | **1** |
|14 | Leak-detection emergency drain   | 1" NPT female, solenoid-actuated         | Normally closed  | 1   |
|15 | N2 fill / purge port             | 1/2" NPT with check valve                | 250 psi          | 1   |
|16 | Annual pressure test port        | 1/4" NPT with cap                        | 500 psi          | 1   |
|17 | External IR camera port          | M12 A-coded, 4-pin (power + Ethernet)    | IP67             | 1   |
| **★18** | **PG25 fill / top-off port (skid side)** | **1/2" NPT with isolation valve, on QD plate interior** | **16 bar** | **1** |

### Physical Arrangement (CDU ECP — Rev 3.0)

```
+--------------------------------------------------+
|  [3] Munters supply duct  [4] Munters return duct|  ← Top (air)
|  (200 mm insulated flanges)                      |
|                                                  |
|  [5]IB-UP   [6]IB-DN   [7]IB-RED (MPO-24 bulkhds)|  ← Upper (fiber)
|  [8]OOB-A   [9]OOB-B   [17]IR-CAM (small conn.)  |
|                                                  |
|  [11] Munters power   [12] MBUS                  |  ← Mid (skid power/control)
|                                                  |
|  ★[1] PG25 SUPPLY  DN150 Stäubli QBH-150         |  ← Lower (fluid Rev 3.0)
|  ★[2] PG25 RETURN  DN150 Stäubli QBH-150         |
|                                                  |
|  [13]Cond. [14]Leak [15]N2 [16]Test ★[18]Fill    |  ← Bottom (drains/test)
+--------------------------------------------------+
     CDU ECP outer cover removed
     ★ = Rev 3.0 change vs 2.2
```

### Spatial Reallocation (Rev 3.0)

PG25 QDs at positions #1 and #2 occupy the same panel zones as the deleted CHW Victaulic penetrations. The DN150 QD envelope (including male pipe adapter + hose flange) is ~300 mm axial × 220 mm diameter, fitting entirely within the 350 mm recess depth. No structural modification to the ECP housing required vs Rev 2.2 CHW Victaulic.

Deleted penetration #10 (CDU power) creates a blank area ~180 × 180 mm in the middle zone. Rev 3.0 uses this space for the added #18 PG25 fill/top-off port plus future expansion. Blank plate with EPDM gasket for offshore.

---

## §5  ELECTRICAL INTERFACE — 800 V DC PRIMARY

Unchanged from Rev 2.2. See Cassette-ECP-001 Rev 2.2 §5 for full content. Key parameters:

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
| Cable (pod-internal landing)     | Laminated copper bus bar, 100×10 mm per polarity |

### What the Cassette Guarantees

- Accepts inputs within the operating range without fault
- Trips its main disconnect within 100 ms on insulation resistance < 5 kΩ
- Reports bus voltage and current to BMS at 1 Hz minimum

### What the Cassette Requires From Platform

- Stable 800 V DC source with ripple ≤ 5 V p-p
- Ground-fault/insulation-monitoring coordinated with pod IMD
- Isolation means upstream (platform-side disconnect) for pod service
- No back-feed permitted: pod is a sink, never a source

### Polarity Keying

Stäubli CombiTac connectors are mechanically keyed for polarity. Platform-side cable assemblies must be assembled with matching keying to prevent reverse-polarity connection. Verification required at commissioning per §19.

---

## §6  ELECTRICAL INTERFACE — 415 V AC ALTERNATIVE

Unchanged from Rev 2.2. The Delta in-rack 110 kW power shelf supports both 800 V DC and 415 V AC 3-phase input. For platforms without 800 V DC infrastructure, 415 V AC can be delivered to the Cassette and rectified by the per-rack shelves.

Key parameters:

| Parameter                        | Value                                    |
|----------------------------------|------------------------------------------|
| Nominal voltage                  | 415 V AC line-to-line ±10%               |
| Frequency                        | 50 or 60 Hz ±3%                          |
| Phase imbalance (voltage)        | ≤ 2% steady-state                        |
| THDv at ECP                      | ≤ 5% per IEEE 519                        |
| Pod peak current (NVL72 tier)    | 2,330 A per phase (1.68 MW @ 415 V, 0.95 PF) |
| Pod peak current (NVL144 CPX)    | 3,115 A per phase (2.24 MW @ 415 V)      |
| Design current                   | 3,200 A per phase continuous             |
| Connector                        | Cam-Lok E1016 series (L1/L2/L3/N/G)      |

See Cassette-ECP-001 Rev 2.2 §6 for detailed requirements. AC vs DC input is selected at commissioning; both sets of ECP connectors are physically present on every pod.

---

## §7  FLUID INTERFACE — PRIMARY PG25 COOLANT (REV 3.0 — REWRITTEN)

### Specification — Primary PG25 Coolant at CDU ECP

The Cassette primary coolant loop terminates at the CDU-end ECP with two DN150 quick-disconnects (one supply, one return). The coolant is 25% propylene glycol in DI water (PG25) with corrosion inhibitor package. Coolant chemistry is managed on the external CDU skid — the Cassette is hydraulically sealed from skid pump discharge to rack return.

| Parameter                    | Supply (to Skid, from Cassette) | Return (from Skid, to Cassette) |
|------------------------------|--------------------------------|---------------------------------|
| Fluid                        | PG25 glycol + inhibitor         | Same fluid (closed primary)     |
| Temperature                  | 55–60 °C (from racks)           | 45 °C (to racks)                |
| ΔT across cassette           | 11–15 °C (NVL72 / CPX design)   | (same)                          |
| Flow (design)                | 2,100 LPM (NVL72) / 2,350 LPM (CPX) | matched                      |
| Flow (operating range)       | 1,800–2,500 LPM                 | matched                         |
| Pressure at ECP              | 2.0–6.0 bar working             | 2.0–6.0 bar working             |
| Maximum design pressure      | 10 bar (working), 15 bar (hydrostatic test) | same              |
| Connector (primary)          | **Stäubli QBH-150 DN150 QD, dry-break, pipe class**     | same                 |
| Connector (offshore)         | Stäubli QBH-150 with FKM seals or Tema DryBreak DB-150 | same |
| Alternative                  | Parker Snap-tite 75 Series DN150 (if Stäubli unavailable) | same |
| Pipe material                | 304L SS (onshore) / 316L SS (offshore) | same                    |
| Interior plumbing            | All-welded per INT-001 Rev 3.0 §14 | (same, symmetric)           |

### PG25 Coolant Chemistry Specification

Chemistry is maintained by the CDU skid (expansion tank, chemistry dosing if needed). Cassette interior has no chemistry maintenance provisions. Required coolant properties:

| Parameter              | Limit                       |
|------------------------|-----------------------------|
| Glycol concentration   | 25% ± 2% propylene glycol   |
| pH                     | 8.5–9.5 (corrosion inhibitor adjusted) |
| Conductivity           | 200–800 μS/cm               |
| Chloride               | < 25 mg/L                   |
| Total suspended solids | < 5 mg/L (after 25 µm filter) |
| Dissolved oxygen       | < 0.5 mg/L                  |
| Inhibitor package      | Organic acid or nitrite, 2,000–3,000 mg/L active |

### What the Cassette Guarantees

- Primary PG25 loop is all-welded factory, X-ray inspected, vacuum decay leak-tested per INT-001 Rev 3.0 §27
- Zero fluid loss during QD connection / disconnection (dry-break design)
- No chemistry perturbation introduced by the Cassette (chemistry managed at skid)
- Return temperature stays ≤ 60 °C at all specified loads and supply temperatures
- Continues operation with skid primary pump N+1 failover (<5 s primary flow interruption)

### What the Cassette Requires From the Skid

- Primary PG25 supply at 45 ± 1 °C
- Primary PG25 flow at design rate (2,100 LPM NVL72 / 2,350 LPM CPX)
- Primary pressure at QD maintained 2.0–6.0 bar working
- Expansion, degassing, filtration, buffer all on skid (per CDUSKID-001)
- Chemistry monitoring with periodic sampling at skid sample ports (not cassette interior)

### Fluid Isolation

**No motorized isolation valves inside the Cassette** on the PG25 loop (unlike Rev 2.2 CHW scheme). The Cassette primary loop is hydraulically contiguous through the QDs to the skid. Isolation is provided by:

1. **QD itself** — Stäubli QBH-150 closes automatically on disconnect (dry-break)
2. **Skid-side isolation valves** — motorized butterfly valves on skid inlet/outlet per CDUSKID-001 §15
3. **Emergency shutdown** — BMS commands skid pumps off; QDs close check valves automatically on pump off

This architecture is simpler than the Rev 2.2 scheme (motorized valves inside pod + external platform valves). Single point of isolation (the QD) is sealed-appliance-correct.

### Fluid Loss Calculation (For Informational Purposes)

If both QDs are disconnected while pod is full:
- Pod interior fluid trapped by QD check valves: ~180 L retained
- Exposed residual from QD mating face: ~30 mL per QD (total 60 mL)
- Total uncontrolled release: ~60 mL on normal disconnect

This is a dramatic improvement over Rev 2.2 Victaulic couplings which could release 100+ L if opened without proper platform-side isolation.

---

## §8  FLUID INTERFACE — CONDENSATE & DRAINS (REV 3.0 — REDUCED SCOPE)

### Condensate Drain (Rev 3.0 — Munters Only)

Rev 2.2 condensate drain covered both CDU drip pan and interior condensation. With CDU external, only Munters-generated interior condensation appears at this drain.

| Parameter                    | Value                                |
|------------------------------|--------------------------------------|
| Source                       | Interior condensation via Munters return duct |
| Expected flow                | 0–1 L/hr normal (reduced from Rev 2.2 — no CDU drip) |
| Connector                    | 1" NPT female at ECP                 |
| Check valve                  | Integrated (prevents back-flow)      |
| Fume loop                    | 150 mm water seal                    |
| Platform side                | Routed to platform condensate collection or direct to environment per local permit |

### Leak-Detection Emergency Drain

Unchanged from Rev 2.2:

| Parameter                    | Value                                |
|------------------------------|--------------------------------------|
| Source                       | Sump overflow path                   |
| Normally                     | Closed (solenoid)                    |
| BMS-actuated open            | On sump high-high alarm              |
| Connector                    | 1" NPT female at ECP                 |
| Platform side                | Emergency drain to approved disposal |

In Rev 3.0, this drain primarily serves PG25 leak events (given there's no CHW inside cassette). BMS logic updated: emergency drain opens on TraceTek alarm from manifold trench or Service End Zone.

### Offshore-Specific

Unchanged from Rev 2.2 (condensate to deck scupper, emergency drain to platform collection).

---

## §9  FLUID INTERFACE — MUNTERS DUCTS

Unchanged from Rev 2.2. Summary for reference:

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

The Munters HCD-600 sits on an external skid. Cassette provides the duct penetrations; platform provides the skid, its power (penetration #11), and the duct connections between skid and Cassette. Control interface via Modbus RTU (penetration #12).

See Cassette-ECP-001 Rev 2.2 §9 for complete detail (unchanged).

---

## §10  DATA INTERFACE — INFINIBAND FABRIC

Unchanged from Rev 2.2. Key parameters:

| Parameter                        | Value                                |
|----------------------------------|--------------------------------------|
| Fabric standard                  | NVIDIA Quantum-X800 InfiniBand NDR   |
| Line rate                        | 400 Gb/s per port                    |
| Fiber type                       | Single-mode OS2 (9/125 μm)           |
| Bulkhead connector               | MPO-24 female (12 fiber pairs each)  |
| Uplink bandwidth (per bulkhead)  | 24 × 400 Gb/s = 9.6 Tb/s             |
| Uplink bulkheads                 | 2 primary (uplink + downlink) + 1 redundant |
| Total pod bandwidth              | 28.8 Tb/s aggregate (primary + redundant) |

Three MPO-24 bulkheads at the CDU ECP (#5, #6, #7 in §4 schedule): A (uplink to spine A), B (downlink spine A), C (redundant to spine B).

See Cassette-ECP-001 Rev 2.2 §10 for detailed fiber requirements.

---

## §11  DATA INTERFACE — OUT-OF-BAND MANAGEMENT

Unchanged from Rev 2.2. Two redundant 10 Gb Ethernet uplinks from internal OOB switch, primary and redundant paths.

| Parameter                        | Value                                |
|----------------------------------|--------------------------------------|
| Line rate                        | 10 Gb Ethernet (1 Gb fallback)       |
| Connector                        | Cat6A RJ-45, Neutrik NE8FDX          |
| VLAN                             | Isolated from compute fabric         |
| Security                         | VPN terminated inside pod at BMS    |

See Cassette-ECP-001 Rev 2.2 §11 for full content.

---

## §12  DATA INTERFACE — STARLINK / CELLULAR ANTENNAS

Unchanged from Rev 2.2. Antennas feed internal Starlink router + 5G cellular router mounted in ELEC End Zone (not CDU end). Connectors at ELEC ECP penetrations #2 and #3.

See Cassette-ECP-001 Rev 2.2 §12 for full content.

---

## §13  SAFETY INTERFACE — EMERGENCY STOP

Unchanged from Rev 2.2. Dual-contact 24 V DC hardwire loop (penetrations #10 and #11 at ELEC ECP).

- IN: platform emergency signal opens pod master disconnect
- OUT: pod internal emergency (fire, major fault) signals platform to shed load

See Cassette-ECP-001 Rev 2.2 §13 for interlock logic.

---

## §14  TEST & COMMISSIONING PORTS

### Rev 3.0 Updates

Penetrations #15, #16 retain Rev 2.2 function. Penetration #18 added (Rev 3.0).

| # | Port                          | Purpose                              | Rev 3.0 Usage                |
|---|-------------------------------|--------------------------------------|-----------------------------|
| 15| N2 fill / purge               | Shipping blanket, annual test purge  | Used for sealed-vessel workflow per INT-001 §27 |
| 16| Pressure test port            | Annual hydrostatic at 12 bar         | Essential for sealed-vessel integrity verification |
| 18| **PG25 fill / top-off (new)** | **Initial factory fill + site top-off** | **On QD plate interior; accessed during commissioning only; sealed after fill** |

### Sealed-Vessel Test Flow (Rev 3.0)

Factory commissioning:
1. Vacuum loop (QDs capped with test caps) to 50 Pa
2. Monitor decay (≤50 Pa / 5 min pass)
3. Pressurize via N2 port to 15 bar
4. Soap test all welds
5. Vent N2, refill with PG25 via port #18
6. Final seal

Site commissioning:
- Port #18 accessed only if top-off needed
- Routine operation: port #18 remains sealed
- Annual integrity check: hydrostatic via port #16

---

## §15  GROUNDING & BONDING INTERFACE

Unchanged from Rev 2.2. See Cassette-ECP-001 Rev 2.2 §15 for detailed requirements.

- 50 mm² chassis bond stud at ELEC ECP (penetration #9)
- Fault current withstand 10,000 A
- Bonded to platform ground system via M12 stainless hardware
- Ground resistance verified at commissioning <0.1 Ω to platform ground

---

## §16  ENVIRONMENTAL RATINGS — ONSHORE VS OFFSHORE

Unchanged from Rev 2.2. Offshore variant upgrades:
- All external hardware 316L stainless
- FKM seals in place of EPDM
- QD selection for PG25: Tema DryBreak DB-150 alternative to Stäubli QBH-150 (preferred for subsea-rated offshore)
- Panel fasteners: stainless bolts in place of Dzus latches
- 3-coat marine epoxy paint system

See Cassette-ECP-001 Rev 2.2 §16 for detailed environmental specifications.

---

## §17  CONNECTOR SPECIFICATIONS (REFERENCED)

### Primary PG25 QDs (Rev 3.0 — New Section)

| Vendor / Model                  | Type                       | Bore   | Rated Flow     | Cycle Life |
|---------------------------------|----------------------------|--------|----------------|-------------|
| **Stäubli QBH-150**             | Dry-break pipe-class QD    | DN150  | 2,121 LPM at 2 m/s | 2,500 cycles |
| Parker Snap-tite 75 Series DN150 | Dry-break QD              | DN150  | 2,300 LPM at 2 m/s | 3,000 cycles |
| Tema DryBreak DB-150 (offshore) | Subsea-rated break-away QD | DN150  | 2,500 LPM at 2 m/s | 500 cycles |

**Recommendation: Stäubli QBH-150 for onshore and general offshore deployments. Tema DB-150 reserved for subsea / Mobile Offshore Drilling Unit applications where emergency disconnect with fluid containment is legal requirement.**

Cycle life of 2,500 (Stäubli) is adequate for routine service — QDs are only disconnected at skid replacement or major maintenance, estimated <10 cycles per 15-year Cassette lifetime.

### In-Rack UQDs

Stäubli UQD-25 (unchanged from Rev 2.0 corrections in COOL-001).

### Electrical Connectors

Unchanged from Rev 2.2: Stäubli CombiTac 2500 for 800 V DC, Cam-Lok E1016 for 415 V AC alternate.

### Data Connectors

Unchanged from Rev 2.2: MPO-24 for InfiniBand, Neutrik NE8FDX for OOB, LC/APC for BMS, SMA / N-type for antennas.

---

## §18  CABLE & HOSE SPECIFICATIONS (REFERENCED) (REV 3.0)

### Flexible Hoses — Cassette to Skid (Rev 3.0 New)

Platform-side responsibility to provide hoses matching these specs. ADC may furnish as accessory.

| Parameter                    | Specification                                      |
|------------------------------|----------------------------------------------------|
| Type                         | Stainless 304 braided overlay on PTFE or synthetic liner |
| Bore                         | DN150                                               |
| Length                       | 5 m standard / 8 m optional                         |
| Pressure rating              | 16 bar working, 64 bar burst                       |
| Temperature rating           | −10 to +70 °C                                       |
| Fittings (Cassette end)      | Male Stäubli QBH-150 (or Parker / Tema equivalent) |
| Fittings (skid end)          | DN150 flanged per CDUSKID-001 §14                   |
| Insulation                   | 25 mm Aeroflex EPDM with UV-protected aluminum jacket |
| Jacket color                 | Black (default) / identified per service per site  |
| Minimum bend radius          | 10 × OD = 1,500 mm                                  |
| Cycle life                   | 500,000 flex cycles at rated pressure              |

**Reference products: Parker ParFlex 797TC, Gates Mega4000, or equivalent industrial process hose.**

### Data Cables

Unchanged from Rev 2.2: MPO trunk for InfiniBand (100 m max passive, longer runs active optical), Cat6A for OOB (100 m max), single-mode OS2 for BMS fiber.

### Power Cables

Unchanged from Rev 2.2: laminated copper bus bar at pod landing (800 V DC), Cam-Lok cable assemblies (415 V AC alternate), appropriate feeder cable per NEC / IEC specification.

See Cassette-ELEC-001 Rev 1.1 for pod-interior cable runs.

---

## §19  ACCEPTANCE TESTING AT ECP (REV 3.0)

### Factory Acceptance (At Cassette Manufacturer)

Pre-ship verification that all ECP penetrations are correctly built, sealed, and functional:

1. **Visual inspection.** All penetrations per §3 and §4 schedules. Each connector type matches spec. Sealing gaskets intact. Bolt torques per drawing.

2. **Electrical insulation test.** Megger test 800 V DC positive to ground, negative to ground. Acceptance: >100 MΩ.

3. **800 V DC connector mating.** Dummy platform cable mated and unmated 3× per side. Verify positive mechanical seating, polarity keying, and no mechanical interference.

4. **Fiber path verification.** Each BMS fiber, each InfiniBand bulkhead: OTDR trace, insertion loss ≤0.3 dB per path.

5. **★ PG25 QD seating verification (Rev 3.0 New).** Both primary QDs fitted with test plugs. Pressurize to 15 bar for 30 minutes. Acceptance: zero decay >50 mbar.

6. **★ Sealed-vessel integrity (Rev 3.0 Enhanced).** Post-fabrication, pre-rack-install:
   - Vacuum whole primary loop to 50 Pa absolute
   - Hold for 5 minutes
   - Acceptance: ≤50 Pa rise (indicates no leak)

7. **Penetration count audit.** Physical count vs §4 schedule; no extras, no missing.

8. **Cover operation.** Both ECP covers open/close 3× on their hinges and fasteners. Weather seal compresses correctly.

9. **Grounding continuity.** Chassis bond stud to any pod-internal ground reference: <0.1 Ω.

### Site Acceptance (Post-Installation, Pre-Energize)

1. **★ PG25 hose connection (Rev 3.0).** Both flexible hoses (from skid) connected to Cassette QDs. Pressure hold at 10 bar for 2 hours. Acceptance: <100 mbar decay.

2. **All ECP connectors mated, verified, sealed.** Walk-around inspection.

3. **Insulation test at ECP.** Platform-side 800 V DC source NOT yet energized. Megger test with platform cables in place.

4. **Ground loop verification.** Platform ground ↔ Cassette ground: <0.1 Ω.

5. **BMS link activation.** Fiber link to platform orchestrator. Telemetry flows.

6. **Munters link.** Duct flow verified, Modbus handshake complete.

7. **First PG25 flow.** Skid pumps started, primary PG25 circulates through Cassette, returns to skid. Verify:
   - Supply temperature reaches 45 ± 1 °C in 10 minutes
   - Return temperature stable within design
   - No leak alarms on TraceTek

8. **Energize 800 V DC.** Apply platform power. Pod rectifiers start. Progressive load application per commissioning plan.

9. **First workload dispatch.** Low-load test via orchestrator, verify full loop stability.

10. **Release to production.**

---

## §20  CHANGE CONTROL

Unchanged from Rev 2.2. Changes to this ICD require:
- Engineering change request submitted to ADC engineering lead (Scott Tomsu)
- Impact analysis on all downstream documents (BOM, INT, COOL, ELEC, FIRE)
- Written acceptance from at least one customer integrator if interface affects existing deployments
- Revision issued with impact table
- Minimum 90-day advance notice before mandatory adoption of breaking changes

**Rev 3.0 was issued as a breaking change with internal-only customer base. Future Rev 4.0+ changes that modify §5 (800 V DC), §7 (PG25), §10 (InfiniBand) interfaces will require customer notice and transition plan.**

---

## §21  REVISION IMPACT TABLE (REV 3.0)

### Documents Requiring Update

| Document              | Rev Before | Rev Required | Nature of Change                              |
|-----------------------|------------|--------------|-----------------------------------------------|
| Cassette-INT-001      | 2.2        | 3.0 (released) | CDU removed, end zone reclaimed, P-6 repurposed |
| Cassette-COOL-001     | 1.1        | Superseded (partial) | §7 CHx2000 no longer production          |
| Cassette-COOL-002     | —          | 1.0 (released) | New document — external CDU architecture   |
| Cassette-CDUSKID-001  | —          | 1.0 (released) | New document — RFQ spec                    |
| Cassette-BOM-001      | 2.2        | 3.0 (pending) | Remove CoolIT line items, add QDs + skid interconnect |
| Cassette-MASS-001     | 2.0        | 3.0 (pending) | −850 kg CoolIT + plumbing, +35 kg QD plate |
| Cassette-ELEC-001     | 1.1        | No change     | Electrical architecture unchanged          |
| Cassette-FIRE-001     | 1.1        | No change     | Fire detection unchanged                   |
| Cassette-CTRL-001     | 1.0        | No change     | Control architecture already references external skid |
| Cassette-MODES-001    | 1.0        | No change     | Modes already reference sealed-vessel      |
| Cassette-SIS-001      | 1.0        | No change     | SIF definitions unchanged                  |
| Cassette-CYBER-001    | 1.0        | No change     | Cyber posture unchanged                    |
| Cassette-TAGS-001     | 1.0        | Minor update  | Skid-CDU tag namespace needs expansion     |

### Deleted Penetrations (Historical)

| Rev 2.2 Penetration | Rev 3.0 Disposition |
|---------------------|---------------------|
| #1 CHW supply (Victaulic) | Replaced with #1 PG25 supply (QBH-150 QD) |
| #2 CHW return (Victaulic) | Replaced with #2 PG25 return (QBH-150 QD) |
| #10 CDU power feed | Deleted (no internal CDU) |

### Added Penetrations

| Rev 3.0 New      | Purpose |
|------------------|---------|
| #18 PG25 fill / top-off port | Sealed-vessel workflow; access during commissioning only |

---

## OPEN ITEMS — REV 3.0

| ID      | Priority | Description                                                                                  | Owner              |
|---------|----------|----------------------------------------------------------------------------------------------|--------------------|
| EC-01   | P-1      | Stäubli QBH-150 vs Parker Snap-tite 75 selection — vendor flow curves at PG25 50 °C, cycle life, delivery | ADC ↔ Stäubli/Parker |
| EC-02   | P-1      | Confirm QD plate structural analysis: 2× DN150 QDs, 10 bar working, on 316L stainless plate 300×600×20 mm | ADC engineering |
| EC-03   | P-1      | Flexible hose selection for cassette↔skid: bore DN150, 16 bar, stainless braided, length 5 m standard | ADC procurement |
| EC-04   | P-1      | Site SAT protocol — pressure hold duration (2 hr confirmed adequate? Longer for offshore?) | ADC operations |
| EC-05   | P-2      | Penetration #18 (PG25 fill) access protocol — single-use during commissioning vs annual maintenance | ADC engineering |
| EC-06   | P-2      | Offshore QD selection: Stäubli QBH-150 with FKM + marine coating vs Tema DryBreak DB-150 | ADC ↔ first offshore customer |
| EC-07   | P-2      | BOM Rev 3.0 line items for QDs, plate, fill port — part numbers and pricing | ADC procurement |
| EC-08   | P-3      | Recessed housing depth 400→350 mm (Rev 3.0) — confirm no interference with hose bend radius | ADC engineering |
| EC-09   | P-3      | Spatial drawing update — mark deleted CHW ports, new QD positions, position #18 | ADC engineering (drafting) |
| EC-10   | P-3      | Update platform-side ECP integration guide — customer documentation for hose connection, QD mating procedure | ADC documentation |

---

## SUMMARY — KEY CHANGES FROM REV 2.2

| # | Change | Impact |
|---|--------|--------|
| 1 | **CHW penetrations deleted; PG25 QDs added at CDU-end ECP** | Cassette becomes sealed PG25 appliance; all CHW is external |
| 2 | **CDU power feed (penetration #10) deleted** | No internal CDU; electrical penetration count drops by 1 |
| 3 | **Condensate drain scope reduced to Munters only** | Flow 0–1 L/hr vs 0–2 L/hr Rev 2.2 |
| 4 | **PG25 fill/top-off port (penetration #18) added** | Supports sealed-vessel commissioning workflow |
| 5 | **Recessed housing depth 400→350 mm** | QDs more compact than Victaulic elbows |
| 6 | **§7 renamed and rewritten** | Primary PG25 replaces Chilled Water |
| 7 | **Dry-break QD architecture** | Reduces field fluid loss from 100+ L to <60 mL |
| 8 | **No motorized isolation valves inside cassette on primary loop** | Simplification — skid-side isolation is sufficient |
| 9 | **SAT protocol adds QD pressure hold test** | 2-hour hold at 10 bar before first flow |
| 10 | **Rev impact clean across companion docs** | INT, COOL, CDUSKID all released concurrently |

---

**Cassette-ECP-001 — External Connection Panel ICD · Rev 3.0 · 2026-04-20**
**Scott Tomsu · scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana**
**CONFIDENTIAL · BREAKING CHANGE FROM REV 2.2**
