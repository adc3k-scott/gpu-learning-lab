# Cassette — INTERIOR DESIGN SPECIFICATION

**Document:** Cassette-INT-001
**Revision:** 3.0
**Date:** 2026-04-20
**Classification:** CONFIDENTIAL
**Status:** Released — Breaking Change from Rev 2.2

**40 ft HC ISO AI Compute Cassette — Sealed, Unmanned, Stackable, Autonomous, No Air Conditioning, No Internal CDU**
Vera Rubin NVL72 · 15 Racks · 900 GPUs · ~1.6–2.2 MW IT
Onshore (Lafayette) + Offshore (Marine) Variants

| Rev | Date       | Description                                                             |
|-----|------------|-------------------------------------------------------------------------|
| 1.0 | 2026-04-12 | Initial release |
| 2.0 | 2026-04-19 | CHW 1,800→2,200 LPM, ΔT 5→11 °C, DN100→DN150 ECP pipe, DN100→DN125 primary manifolds, UQD-16→UQD-25, DC busway 2,500→4,000 A, Novec right-size noted |
| 2.1 | 2026-04-19 | Rev 2.0 cleanup pass: §2 primary input reconciled with ELEC-001, §7 DC cable spec distinguishes ECP landing vs. branch, §11 busway 2,500→4,000 A |
| 2.2 | 2026-04-19 | §2 operating weight 29,935 kg per MASS-001 Rev 2.0; companion cross-refs updated |
| **3.0** | **2026-04-20** | **BREAKING CHANGE: Internal CoolIT CHx2000 CDU removed. Cooling architecture moved to external skid per COOL-002/CDUSKID-001. CDU end zone reclaimed as Service End Zone (BMS, manifold termination, sensor concentration). ECP CDU-end penetrations changed from 2× DN150 CHW to 2× DN150 PG25 QDs. Operating weight 29,935→29,085 kg (850 kg reduction). Panel P-6 reclaimed for BMS rack. §13 deleted (external). §14 renamed Primary PG25 Manifold. No CHW inside cassette.** |

**Prepared by:** Scott Tomsu · CEO / Chief Engineer
scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana

---

## TABLE OF CONTENTS

- §1  Design Philosophy — Sealed PG25 Appliance
- §2  Cassette Nameplate (Rev 3.0)
- §3  Container Shell — 40 ft HC ISO Baseline
- §4  Onshore vs Offshore Variants — Delta Summary
- §5  Interior Geometry & Rack Layout (Rev 3.0)
- §6  Rack Specification — Vera Rubin NVL72
- §7  In-Rack Power Architecture — Delta Shelves
- §8  End Zones — ELEC and Service (Rev 3.0)
- §9  Access Panel System — 12 Panels (Rev 3.0 — P-6 Repurposed)
- §10 External Connection Panel (ECP) Summary
- §11 Floor Routing — Primary Manifold and Power Tray
- §12 Overhead Routing — Sensors, Lighting, Fire
- §13 ~~CoolIT CDU Specification — CHx2000 Primary~~ **DELETED · See COOL-002 + CDUSKID-001**
- §14 Primary PG25 Manifold Design (Rev 3.0 — was Chilled Water)
- §15 Leak Detection — TraceTek + Drip Management
- §16 Munters External Skid — HCD-600
- §17 Fire Suppression — Ansul Novec 1230 + VESDA-E
- §18 Grounding, Bonding & EMI Shielding
- §19 Sensor Instrumentation — Full Schedule
- §20 Autonomous Run System — Jetson AGX Orin (Relocated to P-6)
- §21 Networking — InfiniBand + OOB + Starlink
- §22 Terminal & Junction Box Schedule
- §23 Maintenance UPS & Life-Safety Power
- §24 Structural & Seismic Anchoring
- §25 Marinization — Offshore Variant Deltas
- §26 Acoustic & Thermal Envelope
- §27 Commissioning & Sealed Pressure-Vessel Procedure (Rev 3.0)
- §28 Service Access Choreography (Rev 3.0 — reduced scope)
- §29 Bill of Materials (by Class) (Rev 3.0)
- §30 Open Items, Risks & Revision Impact

---

## §1  DESIGN PHILOSOPHY — SEALED PG25 APPLIANCE

The Cassette is a sealed, unmanned, stackable AI compute module. It accepts defined inputs at a single External Connection Panel (ECP), delivers compute capacity internally, and rejects heat via a sealed primary PG25 coolant loop across that same ECP. There is no interior aisle. There is no HVAC for personnel. Not designed for human ingress. The pod is serviced exclusively via bolt-sealed access panels on the long sides and is designed to be stacked two high on marine deck or purpose-built onshore racking.

### The Three Rules — Updated Rev 3.0

**Rule 1 — The ECP is the contract.** Nothing outside the Cassette reaches past the ECP. Nothing inside the Cassette makes assumptions about upstream equipment. The ECP schedule in §10 is the sole interface document. **Rev 3.0: the ECP carries electrical + data at the ELEC end, PG25 coolant + Munters ducts at the opposite end. No CHW inside the Cassette.**

**Rule 2 — Everything inside is redundant, hot-swappable, or bolted-for-life.** There is no middle category. **Rev 3.0: with the CDU external, "hot-swap" now means manifold valves, UQDs, and sensor modules only. All rotating equipment — pumps, compressors, fans beyond rack — is external. This upgrades the Cassette from "intermittently-serviced appliance" to "sealed pressure vessel."**

**Rule 3 — Diagnosis before dispatch.** The on-pod BMS (NVIDIA Jetson AGX Orin, relocated to reclaimed Panel P-6 zone) is authoritative for Cassette state. External systems receive telemetry and issue high-level workload dispatch. The BMS executes protection and safety actions locally with zero network dependency.

### What the Cassette Is Not

- Not a data center in a box. There is no cold aisle, no hot aisle, no CRAC.
- Not human-occupiable. There is no safe method to work inside while energized.
- Not grid-dependent. The pod accepts 800 V DC at the ECP and has no utility-side awareness — optimized for natural gas gensets providing VAC converted at the external switchgear.
- Not a CDU. **(New in Rev 3.0.)** Heat rejection requires the external CDU skid per Cassette-CDUSKID-001. The cassette is a primary-coolant endpoint only.
- Not a rack enclosure. It is a platform for 15 independently-addressable Vera Rubin NVL72 racks that operate as a single InfiniBand-scaled cluster.

### Sealed Pressure-Vessel Posture

Rev 3.0 elevates the Cassette to **sealed pressure-vessel discipline**. All PG25 plumbing is factory-welded, X-ray inspected at critical joints, vacuum decay leak-tested, nitrogen-blanketed until commissioning fill, and then sealed for field life. Field commissioning is 48 hours, not 6–12 weeks. This is the submarine / ROV / satellite methodology applied to AI compute infrastructure.

---

## §2  CASSETTE NAMEPLATE (REV 3.0)

| Parameter                       | Value                                    |
|---------------------------------|------------------------------------------|
| Enclosure                       | 40 ft HC ISO, CSC-plated                 |
| External dimensions             | 12,192 × 2,438 × 2,896 mm (40' × 8' × 9'6") |
| Internal dimensions             | 12,032 × 2,352 × 2,698 mm (39'5" × 7'8" × 8'10") |
| Rack count                      | 15 × Vera Rubin NVL72 (Oberon, MGX 3rd gen) |
| Compute racks                   | 13                                       |
| Network rack                    | 1 (Quantum-X800 InfiniBand)              |
| Storage + management rack       | 1                                        |
| GPUs (compute racks only)       | 936 Rubin GPUs (1,872 dies, NVL72 tier)  |
| Cassette IT load — NVL72 tier        | 1,585 kW                                 |
| Cassette IT load — NVL144 CPX tier   | 2,105 kW                                 |
| Cassette facility load — NVL72       | 1,677 kW                                 |
| Cassette facility load — NVL144 CPX  | 2,212 kW                                 |
| Cassette cooling demand (primary)    | 1.6–2.2 MW (PG25)                        |
| Primary input                   | 800 V DC (415 V AC 3-ph alternate, selected at commissioning) |
| Cold plate supply/return        | 45 °C / 55–60 °C (PG25)                  |
| **~~Facility CHW supply/return~~** | **N/A — No CHW at cassette ECP (Rev 3.0)** |
| **Primary PG25 interface**      | **2× Stäubli QBH-150 QDs at CDU-end ECP** |
| **External CDU skid requirement** | **Yes — per Cassette-CDUSKID-001**       |
| PUE (cassette level)                 | ≤ 1.06 (PUE including external skid ~1.10–1.12) |
| **Operating weight (Rev 3.0)**  | **29,085 kg** (was 29,935 kg Rev 2.2; 850 kg reduction from CDU removal) |
| ISO 40-ft HC gross limit        | 30,480 kg                                |
| **Mass margin to ISO limit**    | **1,395 kg (Rev 3.0)** (was 545 kg Rev 2.2) |
| Access panels                   | 12 (6 per long side) — P-6 repurposed per §9 |
| Interior occupancy              | None — unmanned                          |
| Fire suppression                | Novec 1230, 5.85% design concentration   |
| BMS                             | NVIDIA Jetson AGX Orin (N+1 redundant), **relocated to P-6 zone** |

### Key Architectural Change vs Rev 2.2

The 850 kg mass reduction comes from removing:

| Item removed (Rev 2.2 → Rev 3.0)      | Mass (kg) |
|---------------------------------------|-----------|
| CoolIT CHx2000 unit                   | 650       |
| Internal CHW piping + Victaulic       | 120       |
| CDU service mounting and access       | 80        |
| **Total reduction**                   | **850**   |

The 1,500 mm CDU end zone interior length is reclaimed per §5 and §8.

---

## §3  CONTAINER SHELL — 40 FT HC ISO BASELINE

Baseline shell unchanged from Rev 2.2. Summary for reference:

| Dimension                     | mm     | Notes            |
|-------------------------------|--------|------------------|
| Interior length               | 12,032 | 39'-5"           |
| Interior width                | 2,352  | 7'-8"            |
| Interior height               | 2,698  | 8'-10"           |
| Total interior volume         | 76.4 m³ |                 |
| Corner casting rating         | 4 × ISO (CSC)   | Stackable 8-high empty |

Both variants start from a new-build 40-ft HC ISO container to CSC standard. Structural frame, corner castings, floor tie-downs, and lifting provisions unchanged from Rev 2.2.

Gas tightness requirement (Rev 3.0): container shell and all penetrations must pass IEC 60529 IP54 test at commissioning; final seal is a condition of pod release.

---

## §4  ONSHORE VS OFFSHORE VARIANTS — DELTA SUMMARY

Variant delta unchanged from Rev 2.2. Summary:

| Parameter              | Onshore (Lafayette)        | Offshore (Marine)           |
|------------------------|----------------------------|-----------------------------|
| Painting               | 2-coat polyurethane        | 3-coat marine epoxy         |
| Hardware               | 304 SS (majority)          | 316L SS throughout          |
| Seals                  | EPDM                       | FKM (fuel-resistant)        |
| Panel fasteners        | Dzus quarter-turn          | 316L SS bolts + captive washers |
| Ambient rating         | −5 to +45 °C, 95% RH        | −10 to +45 °C, 100% RH salt spray |
| Shock rating           | Land transport (Class 2)    | Marine (Class 4) with lashing points |
| Ventilation seals      | Gasketed                   | IP67-gasketed + pressure test |

Offshore variant adds ~300 kg; operating weight becomes 29,385 kg (Rev 3.0). Still 1,095 kg margin to ISO limit.

---

## §5  INTERIOR GEOMETRY & RACK LAYOUT (REV 3.0)

### Zone Allocation (Rev 3.0)

Interior 12,032 mm length is divided into four zones (was three zones + internal CDU in Rev 2.2):

| Zone | Length (mm) | Purpose |
|------|-------------|---------|
| ELEC End Zone | 1,200 | 800 V DC landing, primary electrical, BMS network switch |
| Rack Zone | 9,332 | 15 racks + aisle + manifolds (+300 mm from Rev 2.2 — extra pump/lift clearance) |
| **Service End Zone** (reclaimed) | **1,200** | **BMS rack (P-6 zone), manifold termination, sensor concentration, PG25 QDs to ECP, Munters duct termination. Was CoolIT CHx2000 bay in Rev 2.2.** |
| Short-end wall allowances | 300 | 150 mm each short end for ECP housing depth |
| **Total** | **12,032 mm** | |

### Rack Zone Detail (Rev 3.0)

Rack zone extended from 9,000 mm (Rev 2.2) to 9,332 mm by reclaiming partial end-zone clearances. This permits:

- **Manifold slack** — tapered manifold reducers no longer need to cram into 9 m run
- **Service aisle width** — 300 mm more working length at R1 end for maintenance access from Service End Zone
- **Future rack expansion** — marginal provision for a 16th rack at R0 position (pending structural/power/cooling re-analysis)

Rack spacing remains per Rev 2.2: 600 mm rack pitch, 13 compute + 1 network (R14) + 1 storage (R15).

### Service End Zone (New in Rev 3.0)

The 1,200 mm zone previously occupied by the CoolIT CHx2000 becomes the **Service End Zone** containing:

| Item                              | Position                       | Notes |
|-----------------------------------|--------------------------------|-------|
| BMS rack (Jetson Orin N+1)        | Port side, upper 800 mm        | Repurposed from P-6 panel zone |
| Primary manifold termination header | Centerline, floor trench       | Final header expansion chamber before QD |
| PG25 supply QD plate              | Aft wall, centerline           | Plate holds Stäubli QBH-150 supply QD (wetted surface inside, connector face at ECP) |
| PG25 return QD plate              | Aft wall, centerline (adjacent) | Same, return QD |
| Munters duct termination          | Aft wall, port side            | HVAC duct flange to ECP |
| TraceTek leak sensor concentrator | Starboard wall                 | 4× sensor cable terminations converge |
| Pressure & temperature gauges     | Below BMS rack                 | Local gauge panel for site tech |
| Service light (24 VDC)            | Overhead                       | Not for occupancy — for IR camera & maintenance |
| Ceiling sensor cluster            | Centerline                     | VESDA sampling port, CO detector, smoke witness |

**No rotating equipment, no air conditioning, no fluid pumps inside the Service End Zone.** The zone exists to concentrate passive instrumentation and terminate manifolds.

---

## §6  RACK SPECIFICATION — VERA RUBIN NVL72

Unchanged from Rev 2.2. Reference for context:

| Parameter                  | Value                                    |
|----------------------------|------------------------------------------|
| Rack standard              | NVIDIA MGX 3rd gen, Oberon 19"            |
| Height                     | 48U (2,200 mm overall frame)             |
| Width                      | 600 mm                                   |
| Depth                      | 1,200 mm                                 |
| NVL72 load (compute)       | 120 kW per rack                          |
| NVL144 CPX load            | 160 kW per rack                          |
| Primary coolant            | PG25 glycol, 45 °C supply                |
| Rack-level connection      | Stäubli UQD-25 (3 per side, supply + return) |
| DC primary input           | 800 V DC (primary) or 415 V AC 3-ph (alternate) |
| Network                    | Quantum-X800 InfiniBand at R14            |
| Storage                    | DPU + NVMe servers at R15                 |

See COOL-002 §4 for heat load derivation; see ELEC-001 Rev 1.1 for rack power architecture.

---

## §7  IN-RACK POWER ARCHITECTURE — DELTA SHELVES

Unchanged from Rev 2.2 / ELEC-001 Rev 1.1. Key elements for Rev 3.0 cross-reference:

- 800 V DC primary input from ECP (ELEC end) via laminated bus bar landing
- 800 V DC distributed to 15 racks via DC busway (4,000 A rating)
- In-rack Delta shelves (or equivalent in-row power rack per NVIDIA 800 VDC convention)
- 5% conversion losses aggregated in facility load (see COOL-002 §4)

No change to power architecture in Rev 3.0.

---

## §8  END ZONES — ELEC AND SERVICE (REV 3.0)

### ELEC End Zone

Unchanged from Rev 2.2.

| Parameter                | Value                                 |
|--------------------------|---------------------------------------|
| Length                   | 1,200 mm                               |
| Function                 | Electrical landing, network, E-stop   |
| Contents                 | ECP terminations (DC bus bars + network + E-stop + Starlink/5G junction) |

### Service End Zone (New Name for Former CDU End Zone)

Unchanged dimensions from Rev 2.2 CDU zone. Repurposed contents:

| Parameter                | Rev 2.2 Contents (OLD)   | Rev 3.0 Contents (NEW)        |
|--------------------------|--------------------------|-------------------------------|
| Length                   | 1,500 mm                 | 1,200 mm (300 mm returned to rack zone) |
| Primary function         | CoolIT CHx2000 + service | BMS rack + manifold termination + passive instrumentation |
| Heavy equipment          | 650 kg CDU, 120 kg piping | None — rotating equipment is external |
| Service interval         | Quarterly filter swap    | None — no consumables inside |
| Personnel access         | Required for CDU service | **Not required during life** |
| ECP connections          | 2× DN150 CHW Victaulic   | 2× DN150 PG25 QD (Stäubli QBH-150 or Parker Snap-tite 75) |

### Panel Access to Service End Zone

Formerly Panel P-6 (CDU service). In Rev 3.0:
- P-6 opens to Service End Zone for BMS rack access (hot-swap of Jetson modules)
- Access frequency expected: <2×/year for BMS maintenance
- Not required for cooling system service (that happens at external skid)

---

## §9  ACCESS PANEL SYSTEM — 12 PANELS (REV 3.0 — P-6 REPURPOSED)

12 bolt-sealed access panels (6 per long side). Panel layout unchanged from Rev 2.2 — panel repurposing only.

| Panel | Side | Zone              | Rev 2.2 Purpose       | Rev 3.0 Purpose         |
|-------|------|-------------------|----------------------|-------------------------|
| P-1   | Port | ELEC End         | DC busbar landing    | Unchanged               |
| P-2   | Stbd | ELEC End         | Network / Starlink   | Unchanged               |
| P-3   | Port | Rack Zone fwd    | R1-R4 maintenance    | Unchanged               |
| P-4   | Stbd | Rack Zone fwd    | R1-R4 mirror + Munters duct | Unchanged        |
| P-5   | Port | Rack Zone mid    | R5-R10 maintenance   | Unchanged               |
| P-6   | Stbd | CDU End (Rev 2.2) / Service End (Rev 3.0) | **CDU service** | **BMS rack access** |
| P-7   | Port | Rack Zone aft    | R11-R15 maintenance  | Unchanged               |
| P-8   | Stbd | Rack Zone aft    | R11-R15 mirror       | Unchanged               |
| P-9   | Port | Service End      | Manifold / leak detect | Unchanged             |
| P-10  | Stbd | Service End      | Munters duct access  | Unchanged               |
| P-11  | Port | ELEC End         | E-stop + BMS aux    | Unchanged               |
| P-12  | Stbd | ELEC End         | UPS / Starlink aux  | Unchanged               |

### Fastener Schedule (Onshore / Offshore)

- Onshore: 12 Dzus quarter-turn latches per panel
- Offshore: 12 stainless 316L M10 bolts with captive washers per panel
- Seal: EPDM (onshore) / FKM (offshore), ≥6 years design life

### Safety Interlock

P-1 (DC busbar) has mechanical interlock with 800 V DC disconnect. Cannot open without breaker trip. All panels subject to electrical lockout-tagout when accessed.

---

## §10  EXTERNAL CONNECTION PANEL (ECP) SUMMARY

See Cassette-ECP-001 Rev 3.0 for detailed schedule. Summary for reference:

### ELEC End ECP (no change from Rev 2.2)

- 800 V DC primary input (single laminated bus bar set)
- 415 V AC 3-ph alternate (selected at commissioning)
- BMS uplink (fiber × 4)
- E-stop (dual-contact 24 VDC)
- Starlink / 5G antenna pass-through

### CDU End ECP (CHANGED in Rev 3.0)

| Penetration      | Rev 2.2 Spec                    | Rev 3.0 Spec                          |
|------------------|---------------------------------|---------------------------------------|
| Primary fluid #1 | N/A                              | **PG25 supply — Stäubli QBH-150 QD** |
| Primary fluid #2 | N/A                              | **PG25 return — Stäubli QBH-150 QD** |
| Secondary fluid #1 | CHW supply — DN150 Victaulic   | **DELETED — no CHW at Cassette**     |
| Secondary fluid #2 | CHW return — DN150 Victaulic    | **DELETED**                           |
| Munters supply duct | 400 × 250 mm flange            | Unchanged                             |
| Munters return duct | 400 × 250 mm flange            | Unchanged                             |
| InfiniBand pass-through | 8× LC-terminated fibers     | Unchanged                             |
| Condensate drain | DN40 with air gap                | Unchanged (per Munters only)          |
| Test / vent port | DN20 ball valve                  | Unchanged                             |

**Net change: 2 new PG25 QD penetrations, 2 deleted CHW penetrations. Penetration count at CDU-end ECP unchanged.**

---

## §11  FLOOR ROUTING — PRIMARY MANIFOLD AND POWER TRAY

### Primary PG25 Manifold Trench

Manifold routing unchanged from Rev 2.2 in dimension; content clarified:

| Parameter              | Value                                    |
|------------------------|------------------------------------------|
| Trench location        | Side B (starboard), floor-integrated     |
| Trench dimensions      | 250 mm wide × 200 mm deep × 9,332 mm long |
| Cover                  | Removable floor grate, 4 × 25 mm bars   |
| Contents (Rev 3.0)     | Primary supply manifold (DN125) + primary return manifold (DN125) + TraceTek leak cable |
| **Rev 2.2 Contents**   | **~~Same + CHW supply + CHW return (DN150) — now deleted~~** |

Manifold headers tie to the termination headers in the Service End Zone which then connect through the PG25 QDs at the CDU-end ECP. See §14 for hydraulics.

### DC Power Tray

Unchanged from Rev 2.2.

| Parameter              | Value                           |
|------------------------|--------------------------------|
| Location               | Side A (port), overhead (2.4 m) |
| Type                   | Ladder tray, 600 × 150 mm      |
| Load                   | 800 V DC busway, 4,000 A rated  |

---

## §12  OVERHEAD ROUTING — SENSORS, LIGHTING, FIRE

Unchanged from Rev 2.2.

- Overhead cable tray (separate from power tray): BMS sensors, fire detection, lighting
- Linear LED lighting: service-only, manually switched from outside panel
- Novec 1230 distribution piping: 5× nozzles along centerline
- VESDA sampling ports: 8 ports distributed
- IR camera: single unit at Service End for health monitoring

---

## §13  ~~COOLIT CDU SPECIFICATION — CHX2000 PRIMARY~~

### DELETED IN REV 3.0

Internal CoolIT CHx2000 specification removed. External CDU architecture replaces this section.

**See:**
- **Cassette-COOL-002 Rev 1.0** — External CDU cooling architecture (thermodynamic model, loop topology, pump/HX/buffer sizing)
- **Cassette-CDUSKID-001 Rev 1.0** — External CDU skid equipment specification (procurement-grade RFQ document)

Legacy CHx2000 data preserved in COOL-001 Rev 1.1 §7 for reference only (not production).

---

## §14  PRIMARY PG25 MANIFOLD DESIGN (REV 3.0)

### Scope

This section covers the primary PG25 manifold system entirely inside the Cassette, from the rack branches through the trenched headers to the PG25 QDs at the CDU-end ECP. The intermediate loop, skid HX, and secondary CHW are all external — see COOL-002.

### Primary Supply and Return Headers

| Parameter              | Value                                    |
|------------------------|------------------------------------------|
| Material               | 304L SS (onshore) / 316L SS (offshore)   |
| Diameter               | DN125 (125 mm bore)                       |
| Schedule               | Schedule 40                               |
| Design pressure        | 10 bar working, 15 bar hydrostatic        |
| Design temperature     | 5–70 °C                                   |
| Length                 | 9,000 mm (rack zone) + 1,000 mm (Service End Zone termination) |
| Joints                 | All-welded inside cassette (no serviceable joints) |
| Insulation             | 25 mm Aeroflex EPDM with aluminum jacket |

### Branch Laterals

Per compute rack (R1–R13):

| Parameter              | Value                                    |
|------------------------|------------------------------------------|
| Material               | Matched to headers (304L or 316L SS)     |
| Diameter               | DN40                                      |
| Connection to header   | Welded tee with full-port isolation valve |
| Connection to rack     | Stäubli UQD-25 (3 per side per rack)    |
| Design flow            | 159 LPM (NVL72) / 179 LPM (CPX)          |

Per network rack (R14) and storage rack (R15):

| Parameter              | Value                                    |
|------------------------|------------------------------------------|
| Material               | 304L/316L SS                              |
| Diameter               | DN25                                      |
| Flow                   | 20 LPM (R14) / 13 LPM (R15)              |

### QD Termination Plate (Service End Zone)

The two DN150 PG25 QDs at the CDU-end ECP are mounted on a single-piece 316L stainless plate, 300 × 600 × 20 mm, bolted to the Cassette aft interior wall and sealed with FKM gaskets. Penetration through the wall is TIG-welded and pressure-tested.

QDs pass through to the ECP outer recess where the flexible hoses from the skid mate. Connector model per §5 detail.

### Hydraulics

All hydraulics unchanged from COOL-001 §4–§5. See that document for pressure drop budget, flow allocation per rack, and velocity analysis. This section only captures what's inside the Cassette; everything from the QD outward is in COOL-002.

---

## §15  LEAK DETECTION — TRACETEK + DRIP MANAGEMENT

Unchanged from Rev 2.2 with one clarification.

- TraceTek cable in manifold trench (full 9,332 mm length)
- TraceTek cable in Service End Zone under QD termination plate (1,000 mm loop)
- TraceTek cable along branch laterals (aggregated to TTDM-128 in Service End Zone)
- TraceTek cable on ceiling drip tray (safety layer; expected never wet in normal operation)

Total TraceTek coverage: ~14 m wet-sensitive cable + 3 m bleed-sensitive cable.

**Rev 3.0 clarification:** since no CHW enters the Cassette, TraceTek is only looking for PG25 leaks (single-fluid system). This simplifies the sensor logic in BMS.

---

## §16  MUNTERS EXTERNAL SKID — HCD-600

Unchanged from Rev 2.2. Munters HCD-600 humidity management is not affected by the CDU architectural change. See INT-001 Rev 2.2 §16 for full spec (preserved intact):

- HCD-600 desiccant wheel, 600 scfm
- Process air 50 m³/h to interior
- Regen air 600 scfm exhaust
- Siemens S7-1200 skid PLC
- Modbus TCP to cassette BMS

Open item from Rev 2.2 (Munters sizing verification at CPX load) carried forward — MO-03 in §30.

---

## §17  FIRE SUPPRESSION — ANSUL NOVEC 1230 + VESDA-E

Unchanged from Rev 2.2. Reference FIRE-001 Rev 1.1.

- Novec 1230 at 5.85% design concentration
- VESDA-E aspirating smoke detection with 8 sampling ports
- Release interlocked with BMS + operator dual-action
- Panel P-3 or P-5 preserves emergency access

---

## §18  GROUNDING, BONDING & EMI SHIELDING

Unchanged from Rev 2.2. Reference ELEC-001 Rev 1.1.

- Equipotential bonding throughout Cassette
- Single ground reference at ELEC End ECP
- EMI shielding at all cable tray crossings
- RTE on 800 V DC bus per ELEC-001

---

## §19  SENSOR INSTRUMENTATION — FULL SCHEDULE

Rev 3.0 clarifies sensor count; no CHW sensors in Cassette.

### Sensor Summary (Per Cassette)

| Category                           | Rev 2.2 Count | Rev 3.0 Count | Change |
|------------------------------------|---------------|---------------|--------|
| Per-rack temperature (supply/return) | 30          | 30            | none   |
| Per-rack flow                      | 15            | 15            | none   |
| Per-rack DC current                | 15            | 15            | none   |
| Per-rack vibration                 | 15            | 15            | none   |
| Per-rack leak (integrated)         | 15            | 15            | none   |
| Environmental (T/RH, pressure)     | 6             | 6             | none   |
| Tilt / shock                       | 4             | 4             | none   |
| Fire: VESDA sampling ports         | 8             | 8             | none   |
| Electrical: bus V/I, IMD           | 6             | 6             | none   |
| Breaker status (24 VDC)            | 8             | 8             | none   |
| UPS SoC                            | 2             | 2             | none   |
| Fluid: sump levels                 | 2             | 2             | none   |
| Fluid: manifold pressure + temp    | 4             | 4             | none   |
| ~~CDU pressure + temp internal~~   | ~~6~~         | ~~0~~         | **−6 (CDU removed)** |
| **PG25 QD pressure + temp at QD plate** | ~~0~~    | **4**         | **+4** |
| Expansion tank pressure            | 1             | 0             | −1 (now on skid) |
| **Total per-cassette sensors**     | **137**       | **134**       | **−3**  |

Sensor reduction at cassette level; sensors migrate to the skid and appear in TAGS-001 §SKID-CDU namespace.

### Wiring

All sensors terminate at Advantech ADAM-6000 I/O modules in the Service End Zone, networked via Ethernet to the BMS rack (Jetson Orin).

---

## §20  AUTONOMOUS RUN SYSTEM — JETSON AGX ORIN (RELOCATED TO P-6)

### BMS Rack (Rev 3.0)

With Panel P-6 repurposed (formerly CDU service access), the BMS rack relocates from the dispersed INT-001 Rev 2.2 configuration to a consolidated position in the Service End Zone, accessible through P-6.

| Parameter                       | Value                                    |
|---------------------------------|------------------------------------------|
| Location                        | Service End Zone, upper 800 mm of port side wall |
| Rack size                       | 19" × 12U, wall-mounted                  |
| BMS nodes                       | 2× NVIDIA Jetson AGX Orin 64 GB (N+1)    |
| Failover                        | Keepalived, <200 ms                       |
| Power                           | 24 VDC from life-safety UPS              |
| Cooling                         | None required (Orin low TDP, passive heatsink) |
| Network                         | 4× 1 Gbps Ethernet (redundant)           |
| OS                              | Ubuntu 22.04 LTS                          |
| Software stack                  | Telegraf → InfluxDB → MQTT → Kafka, TensorRT for inference |
| Uplink                          | Fiber to ELEC End ECP                    |

### Autonomous Functions (Unchanged Scope)

All autonomous functions from Rev 2.2 preserved:
- Leak detection and isolation
- Thermal runaway protection  
- Fire detection and suppression command
- Power quality alarm
- Panel-open interlock monitoring
- Predictive maintenance inference
- Workload-aware feedforward (new in Rev 3.0 per CTRL-001)

### Non-Autonomous (Supervisor Responsibility)

- Workload scheduling and dispatch
- Firmware updates (signed only)
- Operating mode transitions (initiated by orchestrator)

---

## §21  NETWORKING — INFINIBAND + OOB + STARLINK

Unchanged from Rev 2.2.

- 8× InfiniBand fibers at R14 Quantum-X800 switch, passed through CDU-end ECP
- Out-of-band management: dedicated Ethernet VLAN, separate from InfiniBand
- Starlink + 5G backup at ELEC End ECP
- BMS network isolated from data plane (OT/IT segmentation per CYBER-001)

---

## §22  TERMINAL & JUNCTION BOX SCHEDULE

Unchanged in dimension. Rev 3.0 updates:

- J-Box 01 (Service End Zone): now hosts BMS power + sensor aggregation
- Rev 2.2 J-Box for CDU control: DELETED (no internal CDU)
- Total junction boxes: reduced from 18 to 15

---

## §23  MAINTENANCE UPS & LIFE-SAFETY POWER

Unchanged from Rev 2.2. 24 VDC maintenance UPS for BMS, leak detection, fire panel, emergency lighting. 30-minute runtime from full charge, 4 hour recharge from external power.

---

## §24  STRUCTURAL & SEISMIC ANCHORING

Unchanged from Rev 2.2. Mass reduction (850 kg) slightly improves seismic margins; no structural re-analysis required.

---

## §25  MARINIZATION — OFFSHORE VARIANT DELTAS

Offshore variant deltas unchanged from Rev 2.2. Rev 3.0 addition:

- Stäubli QBH-150 QDs specified with FKM seals for offshore
- PG25 QD plate 316L stainless (vs 304L onshore)
- Flexible hose to skid: Tema DryBreak alternative for subsea-rated deployments

---

## §26  ACOUSTIC & THERMAL ENVELOPE

Rev 3.0 update: acoustic baseline improves significantly with internal CDU removed.

| Parameter              | Rev 2.2                    | Rev 3.0                       |
|------------------------|----------------------------|-------------------------------|
| Interior noise at BMS position (CDU running) | ~75 dBA       | ~55 dBA (no internal CDU)  |
| Exterior noise at 1 m (cassette only)        | ~65 dBA       | ~50 dBA                       |
| Combined noise (cassette + skid at 1 m)     | N/A           | ~75 dBA (skid dominant)       |

Internal thermal envelope unchanged — still "no AC, no personnel."

---

## §27  COMMISSIONING & SEALED PRESSURE-VESSEL PROCEDURE (REV 3.0)

### Factory Commissioning (Sealed-Vessel Workflow — New Process)

Rev 3.0 elevates factory commissioning to sealed-pressure-vessel discipline. Full workflow:

1. **Weld fabrication complete.** All primary PG25 piping, headers, branches, QD plate welds, and manifold joints finished.
2. **NDT inspection.** 100% visual inspection of all welds; 10% radiographic inspection of critical joints (manifold tees, QD plate, header terminations). Acceptance per ASME B31.3.
3. **Pneumatic proof test.** Pressurize primary loop (with QDs capped) to 15 bar air for 30 minutes. Soap test all welds. Zero leaks.
4. **Vacuum decay test.** Evacuate loop to 50 Pa absolute. Allow 5 minute stabilization. Monitor pressure rise. Acceptance: ≤ 50 Pa decay in 5 min.
5. **Nitrogen purge.** Vent vacuum with dry N₂ to 1.5 bar positive. Nitrogen blanket maintained through rack installation.
6. **Rack installation.** 15 Vera Rubin NVL72 racks installed, UQDs mated at per-rack laterals. Each rack connection individually hydrostat-tested (local to branch) to 12 bar.
7. **Sensor and electrical commissioning.** Cable all sensors to ADAM modules. Energize BMS. Boot checkout.
8. **Initial PG25 fill.** Via dedicated fill port on QD plate. PG25 quality verified (pH 8.5–9.5, conductivity <500 µS/cm, visual clarity). Loop filled to ~180 L (Cassette interior only — skid portion filled at skid).
9. **Final seal.** Fill port sealed with blind cap, witnessed and inspected.
10. **QD caps installed.** Dust/moisture caps on exposed QD faces for shipping.
11. **Ship.** Cassette is a sealed unit from this point until site commissioning.

### Site Commissioning (48 Hour Target)

1. **Arrival inspection.** TraceTek integrity, QD cap integrity, no shipping damage.
2. **Connect to CDU skid.** Remove QD caps, mate to pre-filled flexible hoses. Hoses pressurized to 10 bar for 2 hours, confirm seal.
3. **Top-off PG25.** Minor top-off from skid expansion tank (accounts for hose fill).
4. **Connect Munters skid.** Mate ducts, confirm flow.
5. **Connect ELEC ECP.** 800 V DC, network, E-stop.
6. **BMS + orchestrator handshake.** Confirm telemetry, mode commands.
7. **Workload dispatch test.** Dry run workloads at low compute to verify thermal envelope.
8. **Full rated test.** 75% load for 4 hours, confirm thermal steady-state.
9. **Release to service.**

Target: 48 hours arrival-to-production vs. 6-12 weeks industry standard for traditional container-based data center deployments.

---

## §28  SERVICE ACCESS CHOREOGRAPHY (REV 3.0 — REDUCED SCOPE)

Rev 3.0: service access requirements reduced substantially. Categories:

| Service Event                    | Frequency   | Access Required        | Duration    |
|----------------------------------|-------------|-----------------------|-------------|
| BMS module swap (failover verified) | <2×/year  | Panel P-6              | 45 minutes   |
| VESDA filter                     | Annual      | Any panel              | 30 minutes   |
| Sensor calibration (PG25 QD gauges) | Annual   | Panel P-9 or P-10      | 60 minutes   |
| TraceTek cable health check      | Annual      | Panel P-9              | 30 minutes   |
| Rack hot-swap (per-rack)         | As needed   | Panel P-3 through P-8 (per rack) | 60 min per rack |
| InfiniBand fiber swap            | As needed   | CDU-end ECP external   | 15 minutes   |
| **~~CDU filter/pump service~~**  | **~~Quarterly~~** | **~~P-6~~**         | **~~EXTERNAL SKID ONLY~~** |

Total service person-hours per Cassette per year (steady-state): <10 hours. This is an order of magnitude below typical data center.

---

## §29  BILL OF MATERIALS (BY CLASS) (REV 3.0)

Rev 3.0 BOM summary — see Cassette-BOM-001 Rev 3.0 (pending) for per-line detail.

### Mass Budget Summary

| Class                          | Rev 2.2 (kg) | Rev 3.0 (kg) | Change |
|--------------------------------|--------------|--------------|--------|
| Container shell (40' HC ISO)   | 4,800        | 4,800        | 0      |
| Racks (15 × NVL72 with Delta)  | 11,200       | 11,200       | 0      |
| Manifolds, piping, valves (interior) | 480    | 365          | −115 (no CHW piping)  |
| **CoolIT CHx2000 (deleted)**   | **650**      | **0**        | **−650** |
| **CDU internal plumbing (deleted)** | **120** | **0**        | **−120** |
| **CDU mounting, service provisions (deleted)** | **80** | **0** | **−80** |
| BMS rack (relocated, same mass) | 45          | 45           | 0      |
| Fire suppression (Novec + VESDA) | 180        | 180          | 0      |
| Munters HCD-600 interface      | 60           | 60           | 0      |
| Cable tray, lighting, sensors  | 220          | 220          | 0      |
| Access panels and hardware     | 120          | 120          | 0      |
| QD plate + PG25 QDs (new)      | 0            | 35           | +35    |
| Miscellaneous / allowances     | 500          | 500          | 0      |
| Operator allowance (sensors, documentation, small fittings) | 380 | 380 | 0 |
| Initial PG25 charge (interior only, ~180 L) | 0 | 180         | +180   |
| **Total onshore operating**    | **29,935**   | **29,085**   | **−850** |

Margin to ISO 30,480 kg limit: **1,395 kg** (was 545 kg in Rev 2.2).

Margin recovery allocations (proposed):
- 300 kg structural reinforcement (seismic / offshore)
- 500 kg extra racks or reinforcement (future CPX-Next)
- 595 kg reserve

---

## §30  OPEN ITEMS, RISKS & REVISION IMPACT

### Revision Impact Table

| Area          | Impact            | Gate                          |
|---------------|-------------------|-------------------------------|
| BOM-001       | Rev 3.0 required  | Remove CoolIT; add QD plate + PG25 QDs |
| COOL-001      | Superseded (§7)   | Preserved for reference only  |
| COOL-002      | NEW (released)    | This revision depends on it   |
| ECP-001       | Rev 3.0 required  | CHW penetrations → PG25 QDs   |
| ELEC-001      | No change         | Power architecture unchanged  |
| FIRE-001      | No change         | Fire architecture unchanged   |
| MASS-001      | Rev 3.0 required  | Update mass budget            |
| CDUSKID-001   | NEW (released)    | External CDU procurement      |
| CTRL-001      | References Rev 3.0 | Skid integration at L1       |
| MODES-001     | References Rev 3.0 | Sealed-vessel commissioning added to modes list |
| SIS-001       | References Rev 3.0 | SIS unchanged; gas detection moves to skid |

### Open Items (New in Rev 3.0)

| ID    | Priority | Description                                                                 | Owner  |
|-------|----------|-----------------------------------------------------------------------------|--------|
| IN-01 | P-1      | Stäubli QBH-150 vs Parker Snap-tite 75 selection for PG25 QDs (gates BOM Rev 3.0 and CDUSKID-001 §14) | ADC engineering |
| IN-02 | P-1      | Service End Zone detailed layout drawings — BMS rack, QD plate, manifold termination | ADC engineering |
| IN-03 | P-1      | Panel P-6 repurposing acceptance — confirm access frequency <2×/year is operationally acceptable | ADC operations |
| IN-04 | P-1      | Sealed pressure-vessel commissioning workflow — qualify welders, X-ray vendor, vacuum decay test equipment | ADC engineering |
| IN-05 | P-2      | 300 mm rack zone extension opportunity — structural re-analysis for future 16th rack position | ADC engineering |
| IN-06 | P-2      | PG25 initial charge logistics — fill port, factory-to-site PG25 supply chain | ADC operations |
| IN-07 | P-2      | Internal noise reduction opportunity — with CDU removed, possible to reduce rack acoustic damping | ADC engineering |
| IN-08 | P-3      | Acoustic measurements of Rev 3.0 vs Rev 2.2 for marketing/customer documentation | ADC marketing |

### Preserved Open Items from Rev 2.2

- C-01 through C-10: See INT-001 Rev 2.2 §30. All carry forward except C-10 (UQD-16, closed in Rev 2.0).
- MO-03 (Munters CPX sizing verification): carried forward.

---

## REVISION HISTORY — DETAILED CHANGE LOG (REV 2.2 → REV 3.0)

| Section | Rev 2.2 | Rev 3.0 | Rationale |
|---------|---------|---------|-----------|
| Cover | "Sealed appliance" | "Sealed PG25 appliance, no internal CDU" | Architectural change |
| §1 | 3 rules | 3 rules with Rev 3.0 annotations | Clarify sealed-vessel posture |
| §2 | 29,935 kg, CoolIT CHx2000 listed | 29,085 kg, no CHx2000, PG25 QDs | CDU removed |
| §5 | 3 zones: ELEC, Rack, CDU | 4 zones: ELEC, Rack, Service End, short-end allowances | CDU end reclaimed |
| §8 | ELEC + CDU End Zones | ELEC + Service End Zones | Naming and content |
| §9 | P-6 for CDU service | P-6 for BMS access | Panel repurposed |
| §10 | CDU-end ECP: CHW | CDU-end ECP: PG25 QDs | Primary interface |
| §11 | CHW + PG25 in trench | PG25 only in trench | CHW deleted |
| §13 | CHx2000 specification | DELETED — external | Architecture change |
| §14 | Chilled Water Manifold | Primary PG25 Manifold | CHW not in cassette |
| §19 | 137 sensors | 134 sensors | CDU sensors migrated to skid |
| §20 | BMS position unclear | BMS in Service End Zone at P-6 | Consolidation |
| §22 | 18 junction boxes | 15 junction boxes | CDU J-box deleted |
| §26 | 75 dBA interior | 55 dBA interior | CDU noise removed |
| §27 | Standard commissioning | Sealed pressure-vessel workflow | Key IP |
| §28 | Monthly CDU service | <2×/year BMS only | Service cadence reduction |
| §29 | 29,935 kg total | 29,085 kg total | Mass budget |

---

**Cassette-INT-001 — Interior Design Specification · Rev 3.0 · 2026-04-20**
**Scott Tomsu · scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana**
**CONFIDENTIAL · BREAKING CHANGE FROM REV 2.2**
