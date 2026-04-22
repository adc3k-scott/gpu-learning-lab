# Cassette — BILL OF MATERIALS

**Document:** Cassette-BOM-001
**Revision:** 1.2
**Date:** 2026-04-22
**Classification:** CONFIDENTIAL
**Companion to:** Cassette-INT-001 · Cassette-ECP-001 · Cassette-COOL-001 · Cassette-ELEC-001 · Cassette-FIRE-001 · Cassette-MASS-001

**Purpose:** Complete parts list for one Cassette (40 ft HC ISO, 9 compute racks + 1 control rack + 5 Delta in-row power racks, 15 positions total). Organized by subsystem for procurement workflow. Quantities are per pod. Pricing intentionally excluded — this BOM supports RFQ, not budget. Covers Cassette interior only; external CDU skid, Munters skid, gensets, and switchgear are covered by separate procurement documents.

**Prepared by:** Scott Tomsu · CEO / Chief Engineer
scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana

---

## TABLE OF CONTENTS

- §1  BOM Structure & Conventions
- §2  Container Shell & Structure
- §3  Compute Racks (NVIDIA)
- §4  Power Conversion (Delta)
- §5  Cooling — Primary PG25 Loop
- §6  Dehumidification (Munters External Skid)
- §7  Fire Suppression (Ansul Novec + VESDA)
- §8  Leak Detection & Drains
- §9  Electrical Distribution
- §10 Grounding & Bonding
- §11 Sensors & Instrumentation
- §12 Controls (Jetson + Network)
- §13 Networking Hardware
- §14 ECP Hardware (Connectors, Bulkheads, Penetrations)
- §15 Cable & Conductor Summary
- §16 Miscellaneous Hardware
- §17 Offshore-Variant Additions
- §18 Long-Lead Items & Critical Path
- §19 Vendor Contact Summary

---

## §1  BOM STRUCTURE & CONVENTIONS

- All quantities are **per cassette** unless noted.
- "Vendor" column shows the manufacturer of first choice. Equivalents are acceptable where noted.
- Items flagged **[LONG LEAD]** are critical-path procurement items — order first.
- Items flagged **[OFFSHORE]** apply only to the offshore variant.
- Items flagged **[ONSHORE]** apply only to the onshore variant.
- Items without a flag apply to both variants.

---

## §2  CONTAINER SHELL & STRUCTURE

| Item                                           | Qty | Vendor / Source                  | Notes                              |
|------------------------------------------------|-----|----------------------------------|------------------------------------|
| 40 ft HC ISO container, new-build              | 1   | Sea Box / Conex / SEA Containers | CSC plated, corten steel [LONG LEAD] |
| Floor reinforcement steel plate, 6 mm          | ~29 m² | Local fab                    | Welded to corner channels          |
| Access panel cutouts (factory-cut)             | 12  | Container fabricator             | 900 × 2,000 mm, frame-reinforced   |
| Access panel steel doors                       | 12  | Container fabricator             | 3 mm steel w/ stiffener ribs       |
| Access panel gasket race (integral to cutout)  | 12  | Container fabricator             | Retains quadruple-bulb gasket      |
| ECP cutout (ELEC end)                          | 1   | Container fabricator             | 2,000 × 2,400 mm penetration zone  |
| ECP cutout (CDU end)                           | 1   | Container fabricator             | 2,000 × 2,400 mm penetration zone  |
| ECP outer cover assemblies                     | 2   | Container fabricator             | Hinged, Dzus-latched (onshore) or bolted (offshore) |
| ECP inspection windows (polycarbonate)         | 6   | Plaskolite or equivalent         | 200 × 150 mm, 2,000 J impact rated |
| Interior marine epoxy coating                  | 1 lot | Jotun / Hempel / International | Two-pack, white finish             |
| Interior acoustic foam (ceiling + ends)        | ~45 m² | Armacell or equivalent        | 50 mm melamine, Class A fire       |
| Closed-cell PU insulation (walls)              | ~55 m² | Dow Froth-Pak or equivalent   | 75 mm thickness, R-22              |
| Aluminum foil vapor barrier                    | ~55 m² | Reflectix or equivalent       | Continuous seam                    |
| Overhead cable tray ceiling seats              | 12  | Welded to ceiling interior       | Per-meter distributed              |
| Floor load-spreader plate                      | 1   | Local fab                        | 6 mm × 9 m × 700 mm                |
| ISO corner castings (re-certified post-mod)    | 8   | OEM (pre-existing on container)  | Re-CSC plate at 30,480 kg gross    |

---

## §3  COMPUTE RACKS (NVIDIA)

| Item                                           | Qty | Vendor / Source                  | Notes                              |
|------------------------------------------------|-----|----------------------------------|------------------------------------|
| NVIDIA Vera Rubin NVL72 rack, Oberon, fully loaded | 9 | NVIDIA via Foxconn / HPE / Supermicro / GIGABYTE | Compute R1–R9 [LONG LEAD] |
| Control rack (R10, Oberon frame)               | 1   | Integrator (Foxconn / Supermicro) | Quantum-X800 IB switches + NVMe storage + BlueField-4 DPUs + mgmt servers + Jetson Orin mount |
| Rack seismic anchor kit (M16 × 4 per rack)     | 60  | Simpson Strong-Tie or similar    | Bolt to load-spreader plate (15 positions × 4) |
| Rack-to-rack seismic snubbers [ONSHORE]        | 14 sets | Mason Industries              | Rubber-isolated                    |
| Rack shock isolators [OFFSHORE]                | 60  | Barry Controls or Vibration Mountings | Spring-damper, DNV rated       |
| Diagonal bracing kit [OFFSHORE]                | 6 sets | Local fab                     | Rack-to-container, every 3rd rack  |

**Notes:**
- Rack loaded weight: estimated 1,500 kg (3,307 lbs) per rack. **C-01 open item** — confirm with NVIDIA/Foxconn/HPE before procurement. Estimated weight is within OCP Next-Generation ML Infrastructure Design Principles v0.5.0 rolling load limit of 6,000 lbs per rack; confirm when actual weight is available.
- Racks ship with integrated NVLink cartridges, compute trays, switch trays, and NVLink copper spines per NVIDIA MGX 3rd gen spec.
- One Delta 800 V → 50 V DC/DC Power Shelf installed in each compute rack (R1–R9) for final DC voltage conversion; see §4.
- Delta in-row power racks (R11–R15) occupy the remaining 5 rack positions; see §4.

---

## §4  POWER CONVERSION (DELTA)

| Item                                           | Qty | Vendor / Source          | Notes                              |
|------------------------------------------------|----- |--------------------------|------------------------------------|
| Delta 660 kW In-Row Power Rack (6× 110 kW AC-DC shelves) | 5 | Delta Electronics | R11–R15; 480V AC 3-ph input, 800V DC output, 480 kW embedded BBU per rack; 3,300 kW installed [LONG LEAD] |
| Delta Vera Rubin NVL72 110 kW Power Shelf      | 30  | Delta Electronics        | 6 per Delta in-row power rack × 5 racks = 3,300 kW total [LONG LEAD] |
| Delta 800 V → 50 V DC/DC Power Shelf (2U)      | 9   | Delta Electronics        | One per compute rack (R1–R9) — final DC conversion inside compute rack |
| Delta power shelf mounting rails               | 9 sets | Delta or rack integrator | Per DC/DC shelf (compute racks R1–R9 only) |
| Per-compute-rack 800V DC input cable assembly  | 10  | Assembled by integrator  | 2× 95 mm² × 2 m with lugs (R1–R9); 2× 70 mm² × 2 m (R10) |
| Per-Delta-rack 480V AC feeder cable assembly   | 5   | Assembled by integrator  | 2× 300 mm² per phase + 95 mm² G, ~5 m, to 1,200 A feeder breaker |

**Notes:**
- Delta 660 kW In-Row Power Rack = assembly of 6× Delta Vera Rubin NVL72 110 kW Power Shelves. 6 × 110 kW = 660 kW. 5 racks × 660 kW = 3,300 kW installed. Made in Plano, TX.
- No external rectifier cabinets. No sidecar. All AC-to-DC conversion is in-rack.
- Embedded BBU (5 × 480 kW = 2,400 kW total) eliminates the need for a separate cassette UPS.
- 800 V → 50 V DC/DC shelves in compute racks (R1–R9) are powered from the 800V DC busway branch circuit and perform final voltage conversion for GPU operation.

---

## §5  COOLING — PRIMARY PG25 LOOP

### §5.1  Primary PG25 Piping & Manifolds (Cassette Interior)

| Item                                           | Qty | Vendor / Source      | Notes                              |
|------------------------------------------------|-----|----------------------|------------------------------------|
| Stainless supply manifold, 125 mm (5"), 304L   | ~9.3 m | Victaulic or Swagelok | Floor trench, insulated (9,332 mm per INT-001 §5) |
| Stainless return manifold, 125 mm (5"), 304L   | ~9.3 m | Victaulic or Swagelok | Floor trench, insulated           |
| Per-rack supply drop, 1½" (DN40) stainless     | 9   | Local fab            | DN40 × ~500 mm each (compute racks R1–R9) |
| Per-rack return drop, 1½" (DN40) stainless     | 9   | Local fab            | DN40 × ~500 mm each                |
| Per-rack supply drop, 1" (DN25) stainless      | 1   | Local fab            | R10 control rack                   |
| Per-rack return drop, 1" (DN25) stainless      | 1   | Local fab            | R10 control rack                   |
| Stäubli UQD-25 blind-mate disconnect           | 58  | Stäubli              | 29 supply + 29 return (3 per compute rack R1–R9; 1 per R10) |
| Per-rack isolation valve (1" ball, lockable)   | 20  | Apollo or Watts      | Supply + return, lockout-capable   |
| Manifold air bleed valves                      | 8   | Apollo or Watts      | 1/2" brass, manual                 |
| Manifold drain valves                          | 3   | Apollo or Watts      | 1" ball, to sump                   |
| Manifold insulation, 25 mm closed-cell         | ~20 m | Armacell           | Supply + return manifolds          |
| Pipe hangers and supports (304L SS onshore / 316L offshore) | 40+ | Unistrut or Bline | Floor-mount, marine-grade |
| Welding consumables (308L or 316L filler, argon) | AR | Local welding supply | Sealed-vessel weld spec per INT-001 §26 |

### §5.2  PG25 QD Plate & Termination (Service End Zone → CDU-end ECP)

| Item                                           | Qty | Vendor / Source      | Notes                              |
|------------------------------------------------|-----|----------------------|------------------------------------|
| QD mounting plate, 316L stainless, 300×600×20 mm | 1 | Local fab          | TIG-welded to interior bulkhead per ECP-001 §7 |
| Stäubli QBH-150 DN150 PG25 QD (primary)        | 2   | Stäubli              | 1 supply + 1 return; dry-break, pipe-class [LONG LEAD] |
| Parker Snap-tite 75 Series DN150 (alternate)   | —   | Parker               | Qualified alternate if Stäubli unavailable |
| Tema DryBreak DB-150 (offshore alternative)    | —   | Tema                 | Subsea/MODU deployments only       |
| QD plate FKM gaskets (offshore) / EPDM (onshore) | 2  | Parker/Stäubli OEM  | Sealing face                       |
| PG25 fill/top-off port assembly                | 1   | Swagelok             | 1/2" NPT ball valve + blind cap on QD plate |
| QD dust/moisture caps (shipping)               | 2   | Stäubli/Parker OEM   | Protective caps for transport      |

### §5.3  Pressure Vessel & Instrumentation (Cassette-Internal)

| Item                                           | Qty | Vendor / Source      | Notes                              |
|------------------------------------------------|-----|----------------------|------------------------------------|
| Pressure relief valve (primary, cassette side) | 1   | Watts or Apollo      | 12 bar set, 316L body              |
| Primary supply pressure gauge (QD plate)       | 1   | WIKA or Ashcroft     | 0–10 bar, 4-20 mA transmitter      |
| Primary return pressure gauge (QD plate)       | 1   | WIKA or Ashcroft     | Same                               |
| Primary supply RTD (at QD plate)               | 1   | Pyromation           | Pt100 3-wire, ±0.2 °C              |
| Primary return RTD (at QD plate)               | 1   | Pyromation           | Same                               |
| QD seating limit switches                      | 2   | Honeywell            | Integral to QD or piggyback        |

### §5.4  PG25 Coolant Charge

| Item                                           | Qty | Vendor / Source      | Notes                              |
|------------------------------------------------|-----|----------------------|------------------------------------|
| PG25 coolant initial charge (Cassette interior) | ~180 L | Dowfrost HD or DynaCool | Propylene glycol 25% v/v + organic acid inhibitor; factory-filled per INT-001 §26 |
| PG25 top-off supply (site spare)               | ~40 L | same                | 20% contingency for field top-off  |
| Nitrogen (N2) for pre-fill blanket             | 1 bottle | Airgas           | UHP grade, 6,000 psi, 300 cuft     |

### §5.5  Cassette-to-Skid Interconnect

Supplied with Cassette, installed on-site.

| Item                                           | Qty | Vendor / Source      | Notes                              |
|------------------------------------------------|-----|----------------------|------------------------------------|
| Flexible hose, 304 SS braided, DN150, 5 m      | 2   | Parker ParFlex 797TC or Gates Mega4000 | 1 supply + 1 return; 16 bar working; QBH-150 male fittings [LONG LEAD] |
| Aeroflex EPDM insulation for hose, 25 mm       | 2 sets | Armacell          | UV-protected aluminum jacket       |
| Hose ID tags + service labels                  | 4   | McMaster             | Supply/return, service direction   |

---

## §6  DEHUMIDIFICATION (MUNTERS EXTERNAL SKID)

| Item                                           | Qty | Vendor / Source      | Notes                              |
|------------------------------------------------|-----|----------------------|------------------------------------|
| Munters DSS Pro dehumidifier                   | 1   | Munters              | Spec TBD pending vendor call [LONG LEAD] |
| DSS Pro skid base (steel)                      | 1   | Munters or local fab | With Dynamat vibration isolators   |
| DSS Pro enclosure upgrade to IP66 [OFFSHORE]   | 1   | Munters or custom    | Marine cabinet around unit         |
| Process air supply duct, 400×250 mm × 3 m      | 1   | Local fab            | 304 SS rectangular, 25 mm CCF insulation |
| Process air return duct, 400×250 mm × 3 m      | 1   | Local fab            | 304 SS rectangular, 25 mm CCF insulation |
| Duct flanges (4-bolt, rectangular)             | 4   | Local fab            | 2 at skid, 2 at pod ECP — match ECP-001 §4 #3/#4 |
| Duct EPDM gaskets                              | 4   | McMaster or Grainger | 400×250 mm, 4-bolt pattern         |
| Skid-to-ECP duct run (field-cut)               | As req | Local fab          | Depends on skid placement          |
| Marine flame arrestor duct fittings [OFFSHORE] | 2   | Protectoseal         | In-line with ducts                 |
| Munters power feed cable (480 V AC 3-ph)       | ~10 m | MIL-DTL-24643 (offshore) / standard industrial (onshore) | 80 A rated |
| Modbus RTU cable (RS-485, shielded)            | ~10 m | Belden 3106A        | To pod BMS                         |
| Reactivation exhaust stack kit                 | 1   | Munters              | 150 mm vertical with rain cap      |

---

## §7  FIRE SUPPRESSION (ANSUL NOVEC + VESDA)

| Item                                           | Qty | Vendor / Source      | Notes                              |
|------------------------------------------------|-----|----------------------|------------------------------------|
| Xtralis VESDA-E VEU-A00 aspirating unit        | 1   | Honeywell / Xtralis  | 18-port sampling                   |
| VESDA sampling pipe network (CPVC, 25 mm)      | 1 lot | Xtralis            | ~40 m distributed                  |
| VESDA sampling ports (holes)                   | 18  | Drilled per spec     | 2.2 mm diameter                    |
| Ansul Novec 1230 cylinder — right-size per FIRE-001 | TBD | Johnson Controls (Ansul) | 72 kg agent required; specify correct size per FIRE-001 §4 [LONG LEAD] |
| Novec discharge nozzles (360°)                 | 8   | Johnson Controls (Ansul) | Ceiling-distributed            |
| Novec discharge piping (copper or SS)          | 1 lot | Johnson Controls   | Per NFPA 2001                      |
| Novec control panel                            | 1   | Johnson Controls     | Fire alarm control unit            |
| Novec pre-discharge strobe (interior)          | 1   | Edwards / Wheelock   | Ceiling center                     |
| Novec pre-discharge horn                       | 1   | Edwards / Wheelock   | Ceiling center                     |
| Pre-discharge strobe (exterior, per ECP)       | 2   | Edwards / Wheelock   | Above each ECP                     |
| Novec abort station (each ECP)                 | 2   | Johnson Controls     | Key-switch type                    |
| Over-pressure vent (powered damper, 250 × 250) | 1   | Greenheck or similar | Ceiling-mounted                    |
| Novec cylinder bracket [ONSHORE]               | 2   | Johnson Controls standard | Wall-mount                    |
| USCG-approved cylinder bracket [OFFSHORE]      | 2   | Johnson Controls marine | Marine-rated, shock-tested     |
| Fire suppression control panel battery backup  | 1   | Integral to panel    | 24 hr standby                      |

---

## §8  LEAK DETECTION & DRAINS

| Item                                           | Qty | Vendor / Source      | Notes                              |
|------------------------------------------------|-----|----------------------|------------------------------------|
| TraceTek TT1000-OHP leak detection cable       | 80 m | TE Connectivity     | Water + glycol detect              |
| TraceTek TTDM-128 alarm panel                  | 1   | TE Connectivity      | Modbus TCP to BMS                  |
| TraceTek zone terminators                      | 5   | TE Connectivity      | Per-zone endpoint                  |
| Per-rack drip tray (600 × 1,200 × 50 mm)       | 15  | Local fab, stainless | Sloped 2° to trench                |
| Floor sump (200 × 200 × 150 mm)                | 1   | Local fab, stainless | ELEC-end corner                    |
| Sump pump (20 LPM, float-activated)            | 1   | Little Giant or Goulds | Submersible, 24 V DC            |
| Sump level sensor (3-stage + overflow)         | 1   | Ifm Electronic       | Capacitive, 4-point                |
| Sump conductivity probe                        | 1   | Endress+Hauser       | Seawater discrimination (offshore) |
| Condensate drain solenoid valve                | 1   | ASCO                 | 1" NPT, 24 V DC, normally closed   |
| Marine check valve (condensate) [OFFSHORE]     | 1   | Apollo / Nibco       | 316L stainless                     |
| Fume loop fitting (150 mm water seal)          | 1   | Local fab            | Condensate line                    |
| Leak isolation motorized valves (supply/return) | 2  | Belimo               | At ECP, BMS-commanded              |

---

## §9  ELECTRICAL DISTRIBUTION

| Item                                           | Qty | Vendor / Source      | Notes                              |
|------------------------------------------------|-----|----------------------|------------------------------------|
| 480 V AC main disconnect, 6,000 A, 3-phase, motor-operated | 1 | Eaton Magnum DS / Siemens WL / ABB Emax2 | NEC 125% of 4,179 A/phase = 5,224 A; lockable, shunt trip [LONG LEAD] |
| AC feeder breaker, 1,200 A, 480 V AC 3-phase   | 5   | Eaton or Siemens     | One per Delta in-row rack (R11–R15); NEC 125% of 836 A/phase |
| Surge protection device (SPD)                  | 1   | Phoenix Contact or nVent | Type 1 SPD, 200 kA, 480 V AC     |
| Bender iso-PV1685 IMD                          | 1   | Bender               | Ungrounded 800 V DC monitoring (internal bus) [LONG LEAD] |
| Revenue meter (ANSI C12.20 0.5%)               | 1   | Schneider or Eaton   | 480 V AC 3-phase rated            |
| Maintenance UPS, 24 V DC / 2 kWh (LiFePO4)    | 1   | Victron or Battle Born | Controls and BMS only; compute covered by embedded BBU |
| Life-safety DC panel, 24 V DC distribution     | 1   | Blue Sea Systems or similar | Marine-grade               |
| Per-rack DC branch breaker, 250 A frame, 250 A trip | 9  | ABB SACE or Schneider | 800 V DC listed; R1–R9. **DO NOT RELEASE PO until E-07 closed (Delta fault current + SiC coordination required).** |
| Per-rack DC branch breaker, 250 A frame, 200 A trip | 1  | ABB SACE or Schneider | 800 V DC listed; R10 (control rack). **DO NOT RELEASE PO until E-07 closed.** |
| DC busway, 6,000 A, 800 V DC rated             | 1 lot (~15 m) | Starline or similar | NEC 80%: 5,156 A min, 6,000 A specified; floor-mount ladder |
| Busway taps (per position)                     | 15  | Same as busway       | Bolted compression (5 Delta rack outputs + 10 branch draws) |
| Grounding bar (50 mm² capacity)                | 1   | Burndy or Erico      | Bolted to frame                    |
| CDU power panel (480 V AC 3-ph, 80 A)          | 1   | Eaton or Siemens     | Subpanel at CDU end                |
| Interior LED work light strips                 | 8   | Philips TrueLine or equivalent | 24 V DC, auto-on per panel |
| Panel open activation relay                    | 1   | Phoenix Contact      | Reeds to light control             |

---

## §10 GROUNDING & BONDING

| Item                                           | Qty | Vendor / Source      | Notes                              |
|------------------------------------------------|-----|----------------------|------------------------------------|
| Single-point ground bar                        | 1   | Burndy or Erico      | ELEC end, bonded to frame          |
| Ground bar mounting stud (M12 stainless)       | 1   | Thomas & Betts       | With conductive grease             |
| Rack chassis bond braid (25 mm²)               | 15  | Burndy or similar    | Per rack, to ground bar            |
| CDU chassis bond cable (35 mm²)                | 1   | Burndy               | CDU skid to ground bar             |
| ECP external bond cable (50 mm²)               | 2   | Burndy               | ELEC + CDU ECP bond studs          |
| Bonding jumpers (seam-to-seam) [OFFSHORE]      | 24+ | Erico or Burndy      | Across every bolted seam           |
| Cable tray bond jumpers                        | 30+ | Erico                | Tray section to section            |
| EMI gaskets (access panels)                    | 12  | Chomerics or Laird   | Conductive elastomer               |
| EMI gaskets (ECP penetrations)                 | 30+ | Chomerics or Laird   | Per connector / penetration        |

---

## §11 SENSORS & INSTRUMENTATION

| Item                                           | Qty | Vendor / Source      | Notes                              |
|------------------------------------------------|-----|----------------------|------------------------------------|
| RTD thermowell (per rack supply + return)      | 20  | Omega or Pyromation  | 1/8" NPT, Pt100 (R1–R10)          |
| Ultrasonic flow meter (per rack)               | 10  | Keyence or Ifm       | Clamp-on, non-intrusive (R1–R10)  |
| Hall-effect current transformer (per rack)     | 10  | LEM or Ifm           | 0–300 A DC range (R1–R10)         |
| 3-axis MEMS accelerometer (per rack)           | 15  | Analog Devices ADXL or Ifm | Vibration + seismic (all 15 positions) |
| Interior temperature sensor                    | 4   | Vaisala HMP60        | Distributed                        |
| Interior humidity sensor                       | 2   | Vaisala HMP60        | Upper + lower zone                 |
| Interior static pressure sensor                | 1   | Setra 265            | Low-range differential             |
| External temperature + RH sensor (at ECP)      | 1   | Vaisala HMP110       | Reference                          |
| External barometric pressure sensor            | 1   | Vaisala PTB110       | Weather reference                  |
| Tilt / inclinometer                            | 1   | Ifm JN2100           | 2-axis, marine stability           |
| Shock sensor (container frame)                 | 1   | Omega SHK series     | Event-logging                      |
| PG25 QD pressure sensors (supply + return)     | 4   | Ifm PN7070 or similar | 0–1,000 kPa                        |
| Access panel reed switches                     | 12  | Honeywell 5SM series | Magnetic, IP67                     |
| External IR camera (per ECP)                   | 2   | FLIR A400 series or Axis Q19 | PoE, thermal + visible       |
| Novec cylinder pressure switch                 | 2   | Pre-included w/ Ansul | Already listed §7                  |

---

## §12 CONTROLS (JETSON + NETWORK)

| Item                                           | Qty | Vendor / Source      | Notes                              |
|------------------------------------------------|-----|----------------------|------------------------------------|
| NVIDIA Jetson AGX Orin 64 GB, industrial       | 2   | NVIDIA               | Primary + hot-standby              |
| Jetson development kit mounting (in R10)       | 1   | Connect Tech or Aetina | Industrial carrier board          |
| Advantech ADAM-6017 (8-ch analog in)           | 4   | Advantech            | RTDs, 4–20 mA loops                |
| Advantech ADAM-6060 (6-ch relay + 6-ch DI)     | 2   | Advantech            | Breakers, panels, valves           |
| Advantech ADAM-6050 (12-ch DI + 6-ch DO)       | 1   | Advantech            | E-stop, VESDA, Novec               |
| DIN rail kit for I/O aggregation (R10 interior) | 1  | Phoenix Contact      | 35 mm rail + terminals             |
| Managed Ethernet switch (OOB, 24-port)         | 1   | Aruba 2930F or NVIDIA SN2010 | In R10                     |
| Console server (32-port serial)                | 1   | Digi or Lantronix    | For switch/rack OOB                |
| Time source (GPS-disciplined clock)            | 1   | Meinberg or Microsemi | Integrated with GPS antenna        |
| BMS storage (2 TB NVMe)                        | 2   | Samsung or Micron    | Per Orin, 30-day buffer            |

---

## §13 NETWORKING HARDWARE

| Item                                           | Qty | Vendor / Source      | Notes                              |
|------------------------------------------------|-----|----------------------|------------------------------------|
| Quantum-X800 QM9700/QM9790 switch              | 2   | NVIDIA               | In R10 control rack                |
| InfiniBand cables (NDR, within rack)           | As needed | NVIDIA or Panduit | Passive copper where possible      |
| InfiniBand fiber (NDR, inter-rack + external)  | As needed | Corning           | Single-mode OS2                    |
| MPO-24 trunk cables (external path)            | 3   | Panduit or Corning   | East, west, redundant              |
| LC/APC patch cables (internal CDU zone)        | 48+ | Panduit              | 1 m and 3 m mix                    |
| Fiber patch panel (48 LC/APC)                  | 1   | Panduit or Corning   | CDU zone, in R10 control rack      |
| Starlink Maritime terminal [OFFSHORE]          | 1   | SpaceX               |                                    |
| Starlink Business terminal [ONSHORE]           | 1   | SpaceX               |                                    |
| Cellular modem (4G/5G multi-carrier)           | 1   | Cradlepoint IBR or Sierra Wireless | LTE fallback              |
| GPS antenna (active, timing-grade)             | 1   | Trimble or Jackson Labs | For clock discipline           |
| N-type antenna cables (LMR-400, 6 m)           | 3   | Times Microwave      | Starlink + cellular + GPS          |

---

## §14 ECP HARDWARE (CONNECTORS, BULKHEADS, PENETRATIONS)

### ELEC ECP

| Item                                           | Qty | Vendor / Source      | Notes                              |
|------------------------------------------------|-----|----------------------|------------------------------------|
| 480 V AC primary connection (bus duct coupling) | TBD | Eaton / ABB / Schneider | 4,179 A/phase 3-phase; bus duct specification pending open item E-01 |
| Cam-Lok E1016 series (L1/L2/L3/N/G)           | 5   | Marinco / Hubbell    | Low-current maintenance access only — not primary feed |
| MIL-DTL-5015 6-pin circular (E-stop IN + OUT)  | 2   | Amphenol or Souriau  | 24 V DC dry contact                |
| N-type bulkhead connectors                     | 3   | Amphenol             | GPS + Starlink + cellular          |
| LC/APC bulkhead (BMS fiber primary + redundant) | 2  | Corning              | IP66 fiber bulkhead                |
| Ground stud (M12 stainless, 10 kA fault)       | 1   | Thomas & Betts       | With inspection label              |

### CDU ECP

| Item                                           | Qty | Vendor / Source      | Notes                              |
|------------------------------------------------|-----|----------------------|------------------------------------|
| Stäubli QBH-150 DN150 PG25 QD (primary)        | 2   | Stäubli              | Supply + return; see §5.2 [LONG LEAD] |
| QD mounting plate, 316L SS                     | 1   | Local fab            | See §5.2                           |
| 400×250 mm rectangular flanged duct collars (4-bolt) | 2 | Local fab          | Munters supply + return (see ECP-001 §4) |
| MPO-24 bulkhead (IB uplink + downlink + redundant) | 3 | Corning PRETIUM    | Single-mode OS2                    |
| Neutrik NE8FDX RJ-45 sealed (OOB A + B)        | 2   | Neutrik              | Cat6A shielded, IP67               |
| M12 A-coded sealed (IR camera + Munters Modbus) | 2  | Phoenix Contact      | 4- and 5-pin                       |
| Pin-and-Sleeve IEC 60309 (Munters power only)  | 1   | Mennekes or Meltric  | 80 A, Munters DSS Pro power feed   |
| NPT fittings (condensate, leak, N2, test, fill) | 5  | Swagelok             | 1", 1", 1/2", 1/4", 1/2"           |
| ASCO solenoid valve (leak emergency drain)     | 1   | ASCO                 | 1" NPT, 24 V DC, NC                |
| Marine check valve (condensate) [OFFSHORE]     | 1   | Apollo / Nibco       | 316L stainless                     |
| N2 check valve                                 | 1   | Swagelok             | 1/2" NPT, 250 psi                  |
| Test port cap (1/4" NPT)                       | 1   | Swagelok             | With retention chain               |
| PG25 fill port ball valve + blind cap          | 1   | Swagelok             | 1/2" NPT, post-commissioning seal  |

### ECP Common

| Item                                           | Qty | Vendor / Source      | Notes                              |
|------------------------------------------------|-----|----------------------|------------------------------------|
| ECP outer cover hinge assemblies (per cover)   | 4   | McMaster-Carr        | Marine-grade stainless             |
| Dzus quarter-turn latches [ONSHORE]            | 24  | McMaster-Carr        | 12 per ECP cover                   |
| Stainless cover bolts [OFFSHORE]               | 24  | McMaster-Carr (or Monel) | 12 per ECP cover, M10          |
| Polycarbonate inspection windows (200 × 150)   | 6   | McMaster or Plaskolite | 3 per ECP cover                  |
| ECP housing gasket race                        | 2   | Integral to cover    | Silicone retained                  |
| ECP gaskets (cover-to-shell)                   | 2   | Silicone bulb        | Onshore: single; Offshore: dual    |

---

## §15 CABLE & CONDUCTOR SUMMARY

| Cable Type                                     | Length (m) | Vendor / Source     |
|------------------------------------------------|------------|---------------------|
| 480 V AC primary (ECP to AC main disconnect) — bus duct per E-01 | TBD | TBD — Eaton / ABB / Schneider |
| Per-Delta-rack 480V AC feeder, 2× 300 mm² per phase + 95 mm² G | ~25 (5 × ~5 m) | Southwire or General Cable |
| 800 V DC internal busway stubs (Delta rack outputs) — 100×10 mm bar per polarity | ~7.5 m (5 × 1.5 m) | Custom fab — Eaton/ABB/Schneider |
| Per-rack 800V DC branch cable, 2× 95 mm² (R1–R9) / 2× 70 mm² (R10) | ~20 (10 × 2 m) | Southwire           |
| 480 V AC Munters power feed, 4× 16 mm² (to ECP) | ~6        | Southwire           |
| MPO-24 trunk, OS2 SMF                           | ~15 (in pod) | Corning           |
| LC/APC patch OS2 SMF                            | ~50       | Panduit             |
| Cat6A shielded (OOB, console, sensor I/O)       | ~200      | Panduit or Berk-Tek |
| Modbus RTU cable (Belden 3106A)                 | ~30       | Belden              |
| 24 V DC low-voltage cable (life-safety, sensors) | ~150     | Belden              |
| Bonding cable, 25 mm² (rack chassis)           | ~40 (15 × 2.5 m) | Burndy        |
| Bonding cable, 50 mm² (ECP external)           | ~10       | Burndy              |
| Bare copper ground, 50 mm²                      | ~15       | Southwire           |
| Sensor cable, shielded pair (RTD)               | ~80       | Belden              |
| LMR-400 RF cable                                | ~20       | Times Microwave     |
| **TOTAL COPPER/CABLE ESTIMATE**                 | **~810 m (+bus duct TBD)** | —      |
| **TOTAL FIBER ESTIMATE**                        | **~65 m**  | —                  |

---

## §16 MISCELLANEOUS HARDWARE

| Item                                           | Qty | Vendor / Source      | Notes                              |
|------------------------------------------------|-----|----------------------|------------------------------------|
| Panel fasteners (stainless M10 × 40 mm) [ONSHORE] | ~480 | McMaster           | 40 per panel × 12 panels           |
| Panel fasteners (Monel M10 × 40 mm) [OFFSHORE] | ~480 | Boltport or Bolt-Tech | 40 per panel × 12 panels         |
| Anti-galling compound [OFFSHORE]               | 1 tin | Jet-Lube SS-30      | For Monel fasteners                |
| Captive washer kit (panel bolts)               | ~480 | McMaster             | Stainless                          |
| Cable gland kit (MIL-DTL or IP66)              | ~20  | Roxtec or Hawke      | ECP penetrations                   |
| Cable tray (aluminum ladder, 400 mm wide)      | ~12 m | Cablofil or BLine   | Floor-mount power tray             |
| Sensor cable tray (perforated, 150 mm)         | ~12 m | Cablofil            | Overhead                           |
| DIN rail, terminal blocks, end stops           | 1 lot | Phoenix Contact     | For junction boxes                 |
| Junction boxes (NEMA 4, IP66)                  | 25  | Hoffman              | Per §22 schedule of ADC-CAS-001    |
| Pop-up service tent (clean room) [OFFSHORE]    | 1   | Portafab or equiv.  | For panel-open events              |
| QR code labels (rack, valve, sensor, shelf)    | ~300 | Durable label vendor | Tap-to-docs                       |
| Exterior hazard labels (NFPA + ANSI Z535)      | 1 set | Grainger or Seton   | ECPs + each panel                  |
| Commissioning tools / gaskets / wrenches       | 1 kit | Per SAT procedure   | Ships with pod                     |

---

## §17 OFFSHORE-VARIANT ADDITIONS

Summary of items flagged [OFFSHORE] elsewhere, plus marine-specific additions:

| Item                                           | Qty | Vendor / Source      | Notes                              |
|------------------------------------------------|-----|----------------------|------------------------------------|
| Marine-grade external coating (ice-class epoxy) | 1 lot | Jotun SeaQuantum XP / International Intershield | Full exterior |
| Marine lashing points (weld-on cleats)         | 8   | SeaCatch or similar  | Deck securing                      |
| Fire Department Connection (FDC)               | 1   | AWG Fittings         | CDU-end ECP, external              |
| Explosive gas sensor (H2S/LEL)                 | 1   | Honeywell BW or RKI  | If O&G hazardous zone              |
| USCG inspection tags                           | 1 set | USCG-approved       | Annual                             |
| ABS/DNV certification plate                    | 1   | Class society        | Post-certification                 |
| 10-year Novec cylinder hydrotest certification | 1   | Johnson Controls     | At procurement                     |
| MARPOL-compliant drain routing kit             | 1   | Local fab            | Condensate + emergency             |

---

## §18 LONG-LEAD ITEMS & CRITICAL PATH

Items requiring earliest procurement action (ordered by lead time):

| Item                                           | Est. Lead Time | Criticality |
|------------------------------------------------|----------------|-------------|
| NVIDIA Vera Rubin NVL72 rack (9)               | **18–24 weeks** | BLOCKING    |
| NVIDIA Quantum-X800 QM9700 switches            | 16–20 weeks    | BLOCKING    |
| Delta 660 kW In-Row Power Rack (5)             | 14–18 weeks    | BLOCKING    |
| Delta 800 V → 50 V DC/DC Power Shelf (9)       | 12–16 weeks    | BLOCKING    |
| 40 ft HC ISO container (new-build, modified)   | 12–16 weeks    | BLOCKING    |
| Stäubli QBH-150 DN150 PG25 QDs (2)            | 12–16 weeks    | BLOCKING    |
| 480 V AC main disconnect, 6,000 A              | 10–14 weeks    | HIGH        |
| Flexible DN150 braided hoses, 5 m (2)          | 10–12 weeks    | HIGH        |
| Bender iso-PV1685 IMD                          | 10 weeks       | HIGH        |
| Ansul Novec 1230 cylinders                     | 10–12 weeks    | HIGH        |
| Munters DSS Pro                                | TBD            | HIGH        |
| Stäubli UQD-25 (58 units)                      | 8 weeks        | MEDIUM      |
| VESDA-E VEU                                    | 6–8 weeks      | MEDIUM      |

**Recommendation:** Place RFQ on all BLOCKING and HIGH items within the first 30 days of program start. Integrate delivery into pod assembly schedule with 4-week contingency.

---

## §19 VENDOR CONTACT SUMMARY

| Category                  | Primary Vendor          | Alternate(s)                    |
|---------------------------|-------------------------|----------------------------------|
| Vera Rubin NVL72 racks    | NVIDIA via Foxconn      | HPE, Supermicro, GIGABYTE, ASUS  |
| Delta in-row power racks  | Delta Electronics       | —                                |
| AC main disconnect        | Eaton, ABB, Siemens     | (open item E-01 for ECP bus duct)|
| External CDU skid         | TBD — Gulf Coast fabricator | EPIC Piping, Key Energy       |
| Dehumidification          | Munters                 | Bry-Air (backup)                 |
| Fire suppression          | Johnson Controls (Ansul) | Firetrace, Fike                 |
| Aspirating smoke detect   | Honeywell / Xtralis (VESDA) | Wagner Titanus               |
| Leak detection            | TE Connectivity (TraceTek) | RLE Technologies             |
| Insulation monitoring     | Bender                  | Megger, Littelfuse               |
| PG25 QDs (DN150)          | Stäubli                 | Parker, Tema                     |
| InfiniBand fabric         | NVIDIA (Quantum-X800)   | (vendor-locked to NVIDIA)        |
| Fiber bulkheads + patch   | Corning, Panduit        | CommScope                        |
| Shielded RJ-45            | Neutrik                 | Switchcraft                      |
| Container (new-build)     | Sea Box                 | Conex, SEA Containers, BSL Containers |
| Marine coating            | Jotun, Hempel, International | (all 3 are offshore-qualified) |
| Controls (Jetson)         | NVIDIA                  | —                                |
| I/O aggregation           | Advantech (ADAM)        | Beckhoff, Wago                   |
| Marine fasteners          | Boltport, Bolt-Tech     | (any Monel/Inconel certified)    |

---

**Cassette — Bill of Materials · Cassette-BOM-001 · Rev 1.2 · 2026-04-22**
**Scott Tomsu · scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana**
**CONFIDENTIAL**
