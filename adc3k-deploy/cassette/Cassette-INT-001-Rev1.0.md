# Cassette — INTERIOR DESIGN SPECIFICATION

**Document:** Cassette-Interior-001
**Revision:** 2.0
**Date:** 2026-04-19
**Classification:** CONFIDENTIAL
**Status:** 

**40 ft HC ISO AI Compute Cassette — Sealed, Unmanned, Stackable, Autonoumous, No Air Conditioning**
Vera Rubin NVL72 · 15 Racks · 900 GPUs · ~1.6–2.2 MW IT
Onshore (Lafayette) + Offshore (Marine) Variants

| Rev | Date       | Description                                                             |
|-----|------------|-------------------------------------------------------------------------|
| 1.0 | 2026-04-12 | Initial release |
| 2.0 | 2026-04-19 | CHW 1,800→2,200 LPM, ΔT 5→11 °C, DN100→DN150 ECP pipe, DN100→DN125 primary manifolds, UQD-16→UQD-25, DC busway 2,500→4,000 A, Novec right-size noted (ELEC-001 / FIRE-001 / COOL-001) |


**Prepared by:** Scott Tomsu · CEO / Chief Engineer
scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana

---

## TABLE OF CONTENTS

- §1  Design Philosophy — Sealed Appliance
- §2  Cassette Nameplate
- §3  Container Shell — 40 ft HC ISO Baseline
- §4  Onshore vs Offshore Variants — Delta Summary
- §5  Interior Geometry & Rack Layout
- §6  Rack Specification — Vera Rubin NVL72
- §7  In-Rack Power Architecture — Delta Shelves
- §8  End Zones — ELEC and CDU
- §9  Access Panel System — 12 Panels
- §10 External Connection Panel (ECP) Schedule
- §11 Floor Routing — Manifold and Power Tray
- §12 Overhead Routing — Sensors, Lighting, Fire
- §13 CoolIT CDU Specification — CHx2000 Primary
- §14 Chilled Water Manifold Design
- §15 Leak Detection — TraceTek + Drip Management
- §16 Munters External Skid — HCD-600
- §17 Fire Suppression — Ansul Novec 1230 + VESDA-E
- §18 Grounding, Bonding & EMI Shielding
- §19 Sensor Instrumentation — Full Schedule
- §20 Autonomous Run System — Jetson AGX Orin
- §21 Networking — InfiniBand + OOB + Starlink
- §22 Terminal & Junction Box Schedule
- §23 Maintenance UPS & Life-Safety Power
- §24 Structural & Seismic Anchoring
- §25 Marinization — Offshore Variant Deltas
- §26 Acoustic & Thermal Envelope
- §27 Commissioning & Pressure-Test Procedure
- §28 Service Access Choreography
- §29 Bill of Materials (by Class)
- §30 Open Items, Risks & Rev 1.0→2.0 Delta

---

## §1  DESIGN PHILOSOPHY — SEALED APPLIANCE

The Cassette is a sealed, unmanned, stackable AI compute module. It accepts defined inputs at a single External Connection Panel (ECP), delivers compute capacity internally, and rejects heat and data across the same ECP. There is no interior aisle. There is no HVAC for personnel. Not design for human ingress. The pod is serviced exclusively via bolt-sealed access panels on the long sides with access from both ends, and is designed to be stacked two high on marine deck or purpose-built onshore racking.

### The Three Rules

**Rule 1 — The ECP is the contract.** Nothing outside the Cassette reaches past the ECP. Nothing inside the Cassette makes assumptions about upstream equipment. The ECP schedule in §10 is the sole interface document.

**Rule 2 — Everything inside is redundant or hot-swappable or bolted-for-life.** There is no middle category. If a component can fail during a deployment window, it is either redundant (N+1) or accessible through an access panel for hot swap. If neither, it is a bolted-for-life component commissioned once and never touched until Cassette retirement.

**Rule 3 — Diagnosis before dispatch.** The on-pod BMS (NVIDIA Jetson AGX Orin) is authoritative for Cassette state. External systems receive telemetry and issue high-level workload dispatch. The BMS executes protection and safety actions locally with zero network dependency.

### What the Cassette Is Not

- Not a data center in a box. There is no cold aisle, no hot aisle, no CRAC.
- Not human-occupiable. There is no safe method to work inside while energized.
- Not grid-dependent. The pod accepts 800 V DC at the ECP and has no utility-side awareness - optimized for natural gas Gen sets providing VAC.
- Not a rack enclosure. It is a platform for 15 independently-addressable Vera Rubin NVL72 racks that operate as a single InfiniBand-scaled cluster.

---

## §2  Cassette NAMEPLATE

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
| Cassette IT load — NVL72 tier   | 1,585 kW                                 |
| Cassette IT load —NVL144 CPX tier| 2,105 kW                                 |
| Cassette facility load — NVL72       | 1,677 kW                                 |
| Cassette facility load — NVL144 CPX  | 2,212 kW                                 |
| Cassette cooling demand (secondary)  | 1.6–2.2 MW                               |
| Primary input                   | 415 V AC 3-ph (Optional Direct DC input)
| Cold plate supply/return        | 45 °C / 55–60 °C                         |
| Facility CHW supply/return      | 7–12 °C / 12–18 °C                       |
| PUE (Cassette level)                 | ≤ 1.06                                   |
| Operating weight                | ~30,000 kg (within ISO 40 ft HC limit)   |
| Access panels                   | 12 (6 per long side)                     |
| Interior occupancy              | None — unmanned                          |
| Fire suppression                | Novec 1230, 5.85% design concentration   |
| BMS                             | NVIDIA Jetson AGX Orin (N+1 redundant)   |

---

## §3  Cassette SHELL — 40 FT HC ISO BASELINE

### Baseline Shell

Both variants start from a new-build 40 ft HC ISO container to CSC standard. Critical interior dimensions drive everything that follows:

| Dimension                     | mm    | inches | feet   |
|-------------------------------|-------|--------|--------|
| Interior length               | 12,032 | 473.7  | 39'-5" |
| Interior width                | 2,352 | 92.6   | 7'-8"  |
| Interior height               | 2,698 | 106.2  | 8'-10" |
| Corner casting rating         | 86,400 kg vertical stack per ISO 1161 |
| Tare weight (shell, unmodified) | 3,900 kg | | |

### Shell Modifications Applied (Both Variants)

Modifications performed at the fabrication partner prior to fitout:

1. **Internal floor reinforcement.** 6 mm steel plate laid over original plywood/steel floor, welded to corner channels, for distributed rack load of ~800 kg/m². Adds ~350 kg.
2. **12 access panel cutouts** — 6 per long side, 900 mm × 2,000 mm each, frame-reinforced perimeter, bolt pattern on 150 mm pitch, quadruple-bulb silicone gasket race.
3. **ECP cutouts** — at each short end per §10 penetration schedule.
4. **Overhead cable tray welded seats** — 12 equal-spaced perforated plate seats along interior ceiling at centerline, for sensor/lighting/fire tray support.
5. **Interior coating** — marine epoxy two-pack, white finish for light reflectance. All seams caulked. Floor coated with conductive anti-static epoxy.
6. **Lifting & stacking certification** — corner castings verified post-modification; pod re-CSC-plated at 30,480 kg gross.

### Not Modified

- Exterior skin, doors (end doors welded shut — no longer used), corner posts, corner castings.
- ISO 668 external footprint — remains compliant for intermodal shipping and stacking.

---

## §4  ONSHORE vs OFFSHORE VARIANTS — DELTA SUMMARY

Rev 2.0 covers both variants in one specification. Deltas are called out inline throughout the document. Summary here for reviewers:

| Topic                     | Onshore (Lafayette reference) | Offshore / Marine               |
|---------------------------|-------------------------------|----------------------------------|
| Corrosion protection      | Standard marine epoxy         | Offshore marine coating, salt-spray 2,000 hr per ASTM B117 |
| Roof solar                | Optional First Solar TR1, ~6 kW | Not applicable (stacking + salt) |
| Access panel gasket       | Silicone bulb, dual           | Silicone bulb, quadruple + EPDM secondary |
| Panel fastener            | Stainless bolts, anti-seize   | Monel or Inconel bolts, anti-galling compound |
| ECP connector ratings     | IP54 / NEMA 3R                | IP66 / NEMA 4X                   |
| Rack anchoring            | Bolt-down + minor snubber     | Full seismic + shock-isolated mounts per DNV |
| Internal bonding          | NEC grounding                 | NEC + bonding jumpers across every bolted seam (RFI, ESD) |
| Munters skid              | Open-frame adjacent to Cassette    | Enclosed skid, IP66, deck-mount clips |
| Fire suppression          | Novec 1230 (standard)         | Novec 1230 + marine-grade cylinders, USCG-approved bracketing |
| Certification target      | NEC 2023, NFPA 2001           | + ABS / DNV / Lloyd's Register module certification |
| ISO certification         | CSC-plate                     | CSC + marine lashing points for deck cleats |
| Operating ambient         | −20 to +50 °C                 | −40 to +55 °C                    |
| External finish           | Standard corten + epoxy       | Ice-class epoxy + UV topcoat     |
| Expected service life     | 10+ years                     | 15+ years with scheduled inspections |

Unless called out as a delta, every spec in §5–§30 applies to both variants identically.

---

## §5  INTERIOR GEOMETRY & RACK LAYOUT

### Single-File Longitudinal Rack Row

All 15 racks stand single-file along the container centerline, rack-width aligned to container length. Rack depth (1,200 mm) consumes most of the container width (2,352 mm), leaving 576 mm of clearance to each long wall for manifold drops, power busway, sensor cabling, and access panel reach.

```
Top-down view (not to scale):

 ELEC END                                               CDU END
 ┌──────────────────────────────────────────────────────────────┐
 │ AC main │ R1 R2 R3 R4 R5 R6 R7 R8 R9 R10 R11 R12 R13 R14 R15 │ CDU │
 │ disc.   │ [][][][][][][][][][][][][][][]                      │ Coo │
 │ surge   │                                                      │ lIT │
 │ meter   │ ◄── 9,000 mm rack zone ──►                          │ Ch  │
 └──────────────────────────────────────────────────────────────┘
  1,200 mm                                                   1,500 mm

 Long-side view:

 ┌──────────────────────────────────────────────────────────────┐
 │  [AP-1] [AP-2]   [AP-3] [AP-4]   [AP-5] [AP-6]               │  Side A
 ├──────────────────────────────────────────────────────────────┤
 │                                                                │
 │  R1  R2  R3  R4  R5  R6  R7  R8  R9  R10 R11 R12 R13 R14 R15 │
 │                                                                │
 ├──────────────────────────────────────────────────────────────┤
 │  [AP-7] [AP-8]   [AP-9] [AP-10]  [AP-11] [AP-12]             │  Side B
 └──────────────────────────────────────────────────────────────┘
```

### Dimensional Budget

| Zone                        | Length (mm) | Notes                             |
|-----------------------------|-------------|-----------------------------------|
| ELEC end zone               | 1,200       | Disconnect, surge, meter, IMD     |
| Rack zone                   | 9,000       | 15 racks × 600 mm                 |
| CDU end zone                | 1,500       | CoolIT CHx2000 + service clear    |
| Gap tolerance (distributed) | 332         | Seismic gaps + anchor clearances  |
| **Total**                   | **12,032**  | = interior length                 |

### Rack-to-Wall Clearances

| Dimension                              | mm  | Purpose                          |
|----------------------------------------|-----|----------------------------------|
| Rack face to long wall (Side A, B)     | 576 | Manifold drops + cable tray + access reach |
| Rack top to ceiling                    | 399 | Overhead manifold header + sensor tray |
| Rack base to floor (top of load plate) | 0   | Rack sits on load-spreader plate |
| Rack-to-rack gap                       | ~22 | Seismic gap, distributed 332 mm / 15 |

### Rack Numbering Convention

Rack R1 is at the ELEC end. R15 is at the CDU end. R1–R13 are compute (Vera Rubin NVL72). **R14 is Quantum-X800 InfiniBand spine.** R15 is storage + management.

Placement rationale: network and storage racks near CDU end put fiber patching close to the ECP data penetrations. Compute racks occupy the thermal "middle" of the manifold, which produces the most uniform cold-plate supply temperature across the cluster.

---

## §6  RACK SPECIFICATION — VERA RUBIN NVL72

### Baseline Rack (Both Variants, Compute Slots R1–R13)

| Parameter                            | Value                                  |
|--------------------------------------|----------------------------------------|
| Rack standard                        | OCP Open Rack v3 / NVIDIA MGX 3rd gen (Oberon) |
| External dimensions                  | 600 × 1,200 × 2,299 mm                 |
| Mounting width                       | 21 inch (ORv3)                         |
| Height                               | 48 U usable                            |
| GPU platform                         | NVIDIA Vera Rubin NVL72                |
| GPUs per rack                        | 72 Rubin (144 dies)                    |
| CPUs per rack                        | 36 Vera (Arm custom "Olympus" cores)   |
| Compute trays                        | 18 × 1 U liquid-cooled                 |
| NVLink switch trays                  | 9 × 1 U liquid-cooled                  |
| NVLink cartridges                    | 4 (vertical, part of rack spine)       |
| HBM4 memory                          | 20.7 TB per rack                       |
| LPDDR5x memory                       | 54 TB per rack                         |
| Rack power (typical)                 | 120 kW (NVL72 tier)                    |
| Rack power (CPX upgrade path)        | 160 kW (NVL144 CPX tier, field upgrade) |
| Cooling                              | Liquid direct-to-chip, warm water 45 °C supply |
| Rack loaded weight                   | ~1,500 kg (confirmed estimate; vendor-final pending) |
| Intelligent Power Smoothing          | Native, 400 J/GPU capacitor storage    |

### Alternative Slots

- **R14 — Quantum-X800 InfiniBand:** same Oberon rack frame, populated with NVIDIA QM9700/QM9790-class switches + NVLink 6 top-of-cassette switch trays. Power ~15 kW. Weight ~800 kg.
- **R15 — Storage + Management:** same Oberon rack frame, populated with BlueField-4 DPUs, NVMe storage trays, management servers, out-of-band console server. Power ~10 kW. Weight ~900 kg.

### Upgrade Path — NVL72 → NVL144 CPX

The Oberon rack and Delta power shelves support both tiers. Upgrading a compute rack from NVL72 (120 kW) to NVL144 CPX (160 kW) is a compute-tray-only swap — no rack, power shelf, manifold, or ECP changes. This enables phased deployment where initial pods ship as NVL72 and upgrade to CPX in-field as workloads demand.

---

## §7  IN-RACK POWER ARCHITECTURE — DELTA SHELVES

### Architecture Summary

Every compute rack (R1–R13) contains its own power shelf stack. There is **no separate rectifier cabinet**, **no sidecar**, and **no external power conversion skid** inside the pod.

### Power Shelf Stack — Per Compute Rack

Mounted in the Oberon rack's power zone (typically top-of-rack or split top/bottom):

| Shelf                                    | U  | Function                                 |
|------------------------------------------|----|------------------------------------------|
| Delta Vera Rubin NVL72 110 kW Power Shelf| 4 U | Primary AC→800 V DC or DC→DC first stage |
| Delta 800 V → 50 V DC/DC Power Shelf     | 2 U | Final rack bus conversion                |
| Delta GB200 or GB300 33 kW Shelf (optional) | 2 U | Redundant / N+1 capacity, hot-standby |

**Total U consumed per compute rack:** 6–8 U of the 48 U available, leaving 40+ U for compute trays, NVLink switches, and cable management.

### Per-Rack Power Input

- **Primary:** 800 V DC, ±5%, 150 A nominal at 120 kW
- **Alternative:** 415 V AC, 3-phase, 50/60 Hz (Delta shelf has dual input capability; selected at commissioning)
- **Conductor:** 2× 70 mm² DC cable or 3× 35 mm² AC cable per rack, from ECP ELEC zone via floor power tray

### Sidecar Usage — When It Applies, When It Doesn't

Delta markets a "Sidecar" product for high-density rectification. **It is not used in this Cassette** because Vera Rubin NVL72 at 120 kW/rack is within in-rack shelf capacity. Sidecars become relevant for:

- Legacy 19" EIA compute racks without integrated power shelves (not our case)
- Rubin Ultra Kyber NVL576 at 600 kW/rack (different rack, different pod — 2027+)
- Non-NVIDIA compute where vendor-specific in-rack shelves are unavailable

For this Cassette: no sidecar.

### Intelligent Power Smoothing

Native to the Vera Rubin NVL72 rack. Each GPU has 400 J of capacitor storage; cluster-wide, the Cassette carries ~374 kJ of rack-level energy storage (936 GPUs × 400 J). Handles sub-100 ms load transients without drawing on the 800 V DC bus. **This eliminates the need for a separate UPS or BBU inside the pod** for anything faster than the upstream platform BESS can cover.

---

## §8  END ZONES — ELEC AND CDU

### ELEC End Zone — 1,200 mm

Located at the short end opposite the CDU. Houses the DC-side input gear and protection:

| Component                           | Purpose                                  |
|-------------------------------------|------------------------------------------|
| 800 V DC main disconnect, 2,500 A   | Padlockable isolation of entire pod      |
| Surge protection device (SPD)       | Lightning/switching transient clamp      |
| Ground fault detector / IMD         | Bender iso-PV1685 or equivalent, ungrounded IT system per IEC 61557-8 |
| Revenue-class meter                 | ANSI C12.20 0.5%, 800 V DC rated         |
| 24 V DC maintenance UPS             | 2 kWh, lead-acid or LiFePO4              |
| Life-safety DC panel                | Powers VESDA, Novec panel, BMS, lighting during main outage |
| Main terminal block / bus           | Landing point for 800 V DC feeder cable  |
| Emergency stop relay                | Trips main disconnect on any E-stop assertion |

**Not in ELEC zone:** rectifiers (in-rack), BESS (upstream at platform), transformers (upstream at platform).

### CDU End Zone — 1,500 mm

Houses the primary-to-secondary coolant distribution unit:

| Component                           | Specification                             |
|-------------------------------------|-------------------------------------------|
| CoolIT CHx2000 CDU                  | 2,000 kW capacity, 750 × 1,200 mm footprint |
| Primary flow (PG25 glycol)          | 2,100 LPM nominal                         |
| Secondary flow (CHW)                | 2,200 LPM nominal (revised per COOL-001)  |
| Approach temperature                | 5 °C design                               |
| Pumps                               | Hot-swappable, N+1 redundancy             |
| Filtration                          | 25 μm redundant                           |
| Fill/drain reservoir                | Integrated                                |
| Touchscreen                         | 10", front face (visible via access panel AP-6) |
| Controls                            | Redfish, TCP/IP, Modbus, BACnet           |
| Ultracap ride-through               | Integrated (pump continuity across input transients) |
| Fiber patch panel                   | 48 × LC/APC, single-mode OS2, at upper half of CDU zone |
| Network rack R14 connection        | Fiber pigtails from R14 to patch panel   |
| Storage rack R15 connection        | Ethernet + fiber to ECP via OOB tray     |

**Why CHx2000, not CHx1500:** 15-rack pod at NVL72 tier draws ~1.7 MW; CHx2000 runs at ~84% utilization — within published envelope. **COOL-001 finding:** CHx2000 is at 110.6% of nameplate at full CPX load (2,212 kW). CPX upgrade requires a second CDU or facility-side cooling augmentation — see COOL-001 open item CO-04.

---

## §9  ACCESS PANEL SYSTEM — 12 PANELS

### Configuration

**12 panels total, 6 per long side**, symmetric layout. Every rack is within 750 mm of a panel centerline on at least one side; most racks are within 300 mm.

### Panel Specification

| Parameter                           | Value                                    |
|-------------------------------------|------------------------------------------|
| Opening size (each panel)           | 900 × 2,000 mm                           |
| Pitch (center-to-center)            | 1,500 mm                                 |
| Quantity per side                   | 6                                        |
| Total                               | 12                                       |
| Panel construction                  | 3 mm steel, internal stiffener ribs, marine epoxy coating |
| Gasket — onshore                    | Quadruple-bulb silicone, retained in frame race |
| Gasket — offshore                   | Quadruple-bulb silicone + EPDM secondary, retained + caulked |
| Fasteners — onshore                 | Stainless M10 bolts on 150 mm pitch, captive washers |
| Fasteners — offshore                | Monel M10 bolts on 150 mm pitch, anti-galling compound |
| Number of fasteners per panel       | ~40 (perimeter on 150 mm pitch)          |
| Removal time (2-person crew)        | ~15 min onshore, ~25 min offshore        |
| Reseal time (2-person crew)         | ~30 min including torque check and gasket inspection |
| Interior latch                      | Magnetic reed switch feeds door-open signal to BMS |
| Exterior hazard label               | NFPA 70E arc-flash + 800 V DC + Novec discharge warning |

### Panel-to-Rack Mapping

| Panel ID   | Primary Racks Served | Secondary Reach |
|------------|----------------------|-----------------|
| AP-1 (A)   | R1, R2               | R3 edge         |
| AP-2 (A)   | R3, R4, R5           | —               |
| AP-3 (A)   | R6, R7               | R8 edge         |
| AP-4 (A)   | R8, R9, R10          | —               |
| AP-5 (A)   | R11, R12             | R13 edge        |
| AP-6 (A)   | R13, R14, R15        | — (also CDU face) |
| AP-7 (B)   | R1, R2               | R3 edge         |
| AP-8 (B)   | R3, R4, R5           | —               |
| AP-9 (B)   | R6, R7               | R8 edge         |
| AP-10 (B)  | R8, R9, R10          | —               |
| AP-11 (B)  | R11, R12             | R13 edge        |
| AP-12 (B)  | R13, R14, R15        | — (also CDU face) |

### Panel Closure Integrity

- Pre-deployment: each panel torque-tested with witness marks; bolt pattern verified.
- Annual: panel gaskets visually inspected via borescope (no full panel removal).
- Every 5 years: full gasket replacement at scheduled overhaul.
- Panel-open events logged by BMS reed switch; cumulative open-hour counter tracked per panel.

---

## §10 EXTERNAL CONNECTION PANEL (ECP) SCHEDULE

Two ECP zones — one at each short end — provide the sole physical interface between pod interior and platform.

### ELEC ECP (End Opposite CDU)

| Service                       | Specification                              |
|-------------------------------|--------------------------------------------|
| 800 V DC primary power        | 2× 70 mm² cable, 2,500 A capacity, Stäubli CombiTac blind-mate or equivalent marine-rated connector |
| 415 V AC 3-ph alternative     | 4× 35 mm² (3 phase + neutral + ground), Cam-lok or Pin-and-Sleeve |
| Chassis ground / bond         | 1× 50 mm² direct to pod frame bond stud    |
| Emergency stop (hardwire in)  | 24 V DC dry contact, dual-redundant, latching |
| BMS network uplink (primary)  | 2× single-mode fiber OS2, LC/APC, duplex   |
| Cellular / Starlink antenna   | N-type connector, 50 Ω, surge-protected    |
| GPS antenna (time sync)       | SMA connector, active antenna DC pass      |

### CDU ECP (End with CoolIT)

| Service                       | Specification                              |
|-------------------------------|--------------------------------------------|
| CHW supply (secondary in)     | 6" (DN150) Victaulic grooved, treated water, 7–12 °C, 2,200 LPM |
| CHW return (secondary out)    | 6" (DN150) Victaulic grooved, 12–18 °C     |
| Munters process air in (dry)  | 200 mm insulated duct from external Munters skid |
| Munters process air out (wet) | 200 mm duct to external Munters skid       |
| InfiniBand compute uplink     | 24× single-mode fiber OS2, MPO-24          |
| InfiniBand compute downlink   | 24× single-mode fiber OS2, MPO-24          |
| Out-of-band management        | 2× copper RJ-45 Cat6A, shielded, sealed feedthrough |
| Condensate drain              | 1" NPT female, with marine check valve and fume loop |
| Leak detection drain          | 1" NPT female, sealed under normal ops, opens via BMS-actuated solenoid for emergency dump |
| N2 fill / purge port          | 1/2" NPT with check valve, for commissioning and post-service purge |
| Pressure test port            | 1/4" NPT with capped fitting, annual leak integrity test |

### ECP Environmental Ratings

- **Onshore:** IP54 / NEMA 3R, standard blind-mate connectors
- **Offshore:** IP66 / NEMA 4X, all connectors marine-rated, stainless mounting hardware, EMI gasket at every penetration

---

## §11 FLOOR ROUTING — MANIFOLD AND POWER TRAY

### Architecture

Both chilled water manifolds (supply + return) and power busway run **along the floor**, not overhead. Rationale:

1. Eliminates overhead weight concentration (maintains rack stability under seismic/marine motion)
2. Simplifies rack removal — rack is anchored to floor plate; all connections drop down, not hang from above
3. Leak capture is gravity-native: any primary coolant leak flows to the floor sump
4. Service access via side panels reaches both fluid and power at the same elevation (technician does not need to reach overhead)

### Floor Trench Layout

Running lengthwise between the rack row and each long wall (576 mm of lateral clearance per side):

```
Cross-section (not to scale):

 ┌──────────────────────────────────────────────┐
 │  Overhead (sensor + light + fire)   ~150 mm  │
 ├──────────────────────────────────────────────┤
 │                                               │
 │                                               │
 │           [    RACK    ]                      │
 │           [   600 mm   ]                      │
 │           [            ]                      │
 │           [  1,200 mm  ]                      │
 │           [   deep     ]                      │
 │           [            ]                      │
 │   ┌───┐  [            ]  ┌───┐                │
 │   │ P │  [            ]  │ M │                │
 │   │ W │  [            ]  │ F │                │
 │   └───┘  └────────────┘  └───┘                │
 │   Power  Load plate     Manifold             │
 │   tray   6mm steel      trench              │
 │   400mm                  450 mm              │
 └──────────────────────────────────────────────┘
 Container width 2,352 mm
```

### Power Tray (Side A, along long wall)

| Parameter                    | Value                                    |
|------------------------------|------------------------------------------|
| Tray material                | Aluminum ladder, 400 mm wide             |
| Elevation                    | Floor-mounted, 100 mm above load plate   |
| Primary busway               | 800 V DC, 2,500 A copper laminated       |
| Branch taps                  | 15 × per-rack drops via DC breaker       |
| Per-rack DC breaker          | 250 A frame, 200 A continuous, Class L   |
| Branch cable to rack         | 2× 70 mm² from breaker to rack Delta shelf |
| Separation from data cable   | Minimum 300 mm lateral, or metallic barrier |

### Manifold Trench (Side B, along long wall)

| Parameter                    | Value                                    |
|------------------------------|------------------------------------------|
| Trench material              | Stainless 316L, 450 mm wide × 150 mm deep, welded to floor plate |
| Supply manifold              | 125 mm (5") stainless, insulated (COOL-001 §5: DN100 undersized at CPX) |
| Return manifold              | 125 mm (5") stainless, insulated         |
| Per-rack drops               | 15 × Stäubli UQD-25 blind-mate, 3/rack/side = 86 total (COOL-001 §6) |
| Per-drop isolation valve     | 1" ball valve, lockout-capable           |
| Air bleed points             | 1 at each manifold end, 3 distributed along length |
| Drain ports                  | 1 at lowest point, gravity to floor sump |
| Temperature sensor per rack  | Supply + return + ΔT logic               |
| Flow meter per rack          | Ultrasonic clamp-on, non-intrusive       |

### Load Spreader Plate

6 mm steel plate under the rack row, welded to floor reinforcement. Purpose:
- Distributes ~22,500 kg of rack weight across floor
- Provides grounded conductive surface for rack chassis bonds
- Takes seismic anchor bolts (racks bolt to plate, plate is structurally welded to container)
- Protects underlying plywood/steel floor from point loads

---

## §12 OVERHEAD ROUTING — SENSORS, LIGHTING, FIRE

### What Goes Overhead

With manifold and power on the floor, overhead is reserved for low-mass systems:

| System                            | Location            | Notes                           |
|-----------------------------------|---------------------|---------------------------------|
| LED work lighting                 | Ceiling centerline  | Auto-on when any panel opens    |
| VESDA sampling tubes              | Ceiling + above racks | 18 sampling points total       |
| Novec 1230 discharge piping       | Ceiling lateral     | 8 nozzles for total flood       |
| Fire pull station (external)      | Not applicable      | Unmanned — all triggers auto/BMS |
| Sensor cable trays                | Ceiling edges       | Fiber + Cat6A for BMS           |
| Emergency strobe (internal)       | Center ceiling      | Pre-discharge warning           |
| Emergency strobe (external)       | Above each end ECP  | Visible at 30 m minimum         |
| IR cameras                        | Ceiling, 2 ×        | One at each end, wide-angle covering rack aisle |

### Overhead Tray Loading Budget

Total overhead mass: ~150 kg distributed across 12 m length = 12.5 kg/m linear. Ceiling plate seats rated for 50 kg/m each. 4× safety margin on design load.

---

## §13 COOLIT CDU SPECIFICATION — CHx2000 PRIMARY

### Product: CoolIT CHx2000 Row-Based CDU

| Parameter                        | Value                                    |
|----------------------------------|------------------------------------------|
| Type                             | Liquid-to-liquid CDU                     |
| Capacity                         | 2,000 kW at 5 °C approach                |
| Footprint                        | 750 × 1,200 mm (single-rack footprint)   |
| Height                           | Compatible with Oberon envelope          |
| Primary flow (to cold plates)    | 2,100 LPM                                |
| Secondary flow (facility CHW)    | 2,200 LPM (revised per COOL-001)         |
| Primary coolant                  | PG25 (25% propylene glycol)              |
| Secondary coolant                | Treated water (facility)                 |
| Pump redundancy                  | N+1, hot-swappable                       |
| Filter                           | 25 μm redundant (50 μm option)           |
| Piping                           | All stainless steel, 4" Victaulic        |
| Controls                         | Redfish, SNMP, TCP/IP, Modbus, BACnet    |
| Ultracap                         | Integrated, pump continuity during transients |
| Touchscreen                      | 10" front-face, aligned with AP-6        |
| Group control                    | Up to 20 units (multi-pod support)       |
| Availability target              | Six 9s (99.9999%) per CoolIT published   |

### Secondary-Side Interface (to ECP)

- Supply: 7–12 °C at ECP
- Return: 12–18 °C at ECP
- ΔT design: 11 °C (pod receives 7 °C water, returns 18 °C at full NVL72 load — COOL-001)
- Flow: 2,200 LPM nominal, matched by facility-side pumping (revised per COOL-001)

### Primary-Side (to Racks)

- Supply to rack manifold: 45 °C (warm-water cooling, ASHRAE W+ class)
- Return from rack manifold: 55–60 °C
- Pressure delivery: 53 psi secondary head (CoolIT published, exceeds Vera Rubin requirement)

---

## §14 CHILLED WATER MANIFOLD DESIGN

### Primary Loop (Cassette-Internal, PG25 Glycol)

| Segment                          | Description                              |
|----------------------------------|------------------------------------------|
| CDU → supply manifold            | 4" stainless, insulated, 1 × 2,100 LPM   |
| Supply manifold (floor trench)   | 125 mm stainless, horizontal, length of rack zone |
| Per-rack supply drop             | 1¼" (DN32) stainless, Stäubli UQD-25     |
| Per-rack return drop             | 1¼" (DN32) stainless, Stäubli UQD-25     |
| Return manifold (floor trench)   | 125 mm stainless                         |
| Return manifold → CDU            | 4" stainless, insulated                  |

### Flow Per Rack

- Vera Rubin NVL72: ~140 LPM per rack at 120 kW (1.17 LPM/kW CoolIT reference)
- NVL144 CPX upgrade: ~187 LPM per rack at 160 kW
- Total Cassette flow: 2,100 LPM at NVL72 tier (13 compute × 140) + overhead for R14/R15

### Valves, Bleeds, Drains

- Isolation valve at each rack drop (supply + return) — 1" ball valve, lockable
- Air bleed at each manifold end + 3 distributed — high points, manual
- Drain at lowest point of each manifold — floor sump connection
- Expansion tank at CDU — handles thermal volume change of PG25
- Pressure relief at CDU — 100 psi set point

### Fill / Flush Ports

- Fill port at CDU (front face, accessible via AP-6)
- Flush drain at ELEC end (via floor sump, for annual fluid service)

### Manifold Instrumentation

Per rack drop:
- Supply temperature (RTD, 1/8" NPT thermowell)
- Return temperature (RTD, 1/8" NPT thermowell)
- Flow (ultrasonic clamp-on, 0.1 LPM resolution)
- ΔT computed at BMS — per-rack heat-load accounting

---

## §15 LEAK DETECTION — TRACETEK + DRIP MANAGEMENT

### Leak Detection Cable (TraceTek TT1000-OHP)

Routed continuous under:
- Primary manifold (both supply and return, full length)
- Each rack's drip tray perimeter
- CDU skid perimeter
- ECP fluid penetration points (interior side)

Total cable length: ~80 m. Alarm to BMS within 30 seconds of any conductive fluid contact.

### Drip Management

| Component                    | Purpose                                     |
|------------------------------|---------------------------------------------|
| Per-rack drip tray           | 600 × 1,200 × 50 mm stainless, sloped 2°   |
| Rack tray drain              | Gravity to manifold trench                  |
| Manifold trench              | Collects all drops, sloped 1° toward ELEC end |
| Floor sump                   | 200 × 200 × 150 mm at ELEC-end corner       |
| Sump pump                    | Float-activated, 20 LPM, drains via ECP    |
| Sump level sensor            | Three-stage: low/mid/high + overflow alarm  |
| Sump conductivity probe      | Distinguishes glycol vs water vs seawater (offshore) |

### Leak Response (Automated)

| Stage               | BMS Action                                        |
|---------------------|---------------------------------------------------|
| TraceTek triggered  | Log, alert operator, increase sensor poll rate   |
| Sump level mid      | Start sump pump, continue monitoring             |
| Sump level high     | Isolate affected rack (close UQD + power off)    |
| Sump overflow       | Isolate all racks, E-stop primary loop, notify   |

### Offshore-Specific

- Sump conductivity measures seawater signature (high conductivity, Na+/Cl-)
- Seawater detection → pod-wide E-stop and isolation valves close at ECP
- Purge port opens to N2 backfill to displace any ingress

---

## §16 MUNTERS EXTERNAL SKID — HCD-600

### Why External

The Munters HCD-600 sits on an external skid adjacent to (onshore) or deck-mounted near (offshore) the Cassette. Rationale:

1. Munters is a moisture-management system; placing it inside a sealed moisture-sensitive pod is architecturally backward
2. External Munters is serviceable without breaking Cassette seal
3. HCD-600 is NEMA 4 rated — fully weather-tight per Munters datasheet, safe outdoors
4. Preserves all 15 rack slots inside the Cassette
5. On marine/offshore deployments, one Munters can serve multiple pods via a shared air manifold (single point of failure concern noted — prefer 1:1 Cassette:Munters for critical sites)

### HCD-600 Specification

| Parameter                  | Value                                    |
|----------------------------|------------------------------------------|
| Process airflow            | 600 SCFM (300–1,125 adjustable)          |
| Moisture removal           | 16 lbs/hr at 75 °F / 50% RH              |
| Dew point capability       | −40 °F                                   |
| Dimensions                 | 1,930 × 787 × 1,422 mm (76 × 31 × 56 in) |
| Weight                     | 181 kg (400 lb)                          |
| Casing                     | Welded strain-hardened aluminum, zero air leakage |
| Reactivation               | Electric (preferred for marine — no fuel handling) or steam or indirect NG |
| Reactivation heater power  | ~20–30 kW electric                       |
| Controls                   | Siemens S7-1200 PLC, KTP400 HMI, Modbus to pod BMS |
| Enclosure                  | NEMA 4 weathertight                      |
| Certifications             | UL 1995 (cETLus), UL 508A                |

### Skid Configuration (Both Variants)

| Component                       | Purpose                                |
|---------------------------------|----------------------------------------|
| HCD-600 unit                    | Core dehumidification                  |
| Process fan (integral)          | 2 HP TEFC                              |
| Reactivation fan (integral)     | 1 HP TEFC                              |
| MERV 8 prefilter                | Side-loaded, serviceable on skid       |
| Process air supply duct         | 200 mm insulated, to pod CDU-end ECP   |
| Process air return duct         | 200 mm, from pod CDU-end ECP           |
| Reactivation exhaust stack      | Vertical, 150 mm, with rain cap        |
| Power feed                      | 480 V AC 3-ph, 60 A from platform, ~30 kW running |
| BMS link                        | Modbus RTU over RS-485, 1 pair STP     |

### Offshore Delta

- Skid enclosed in IP66 marine cabinet (HCD inside its own outer box)
- Ducts wrapped with UV-resistant insulation
- Electric reactivation only (no fuel-fired on deck)
- Skid mounted via Dynamat vibration isolators, bolted to deck with Monel hardware
- Ducts to pod ECP include marine flame-arrestor fittings

---

## §17 FIRE SUPPRESSION — ANSUL NOVEC 1230 + VESDA-E

### Detection — VESDA-E VEU Aspirating Smoke Detection

| Parameter                    | Value                                     |
|------------------------------|-------------------------------------------|
| Model                        | Xtralis VESDA-E VEU-A00                   |
| Sampling ports — rack zone   | 15 × (one above each rack)                |
| Sampling ports — power zone  | 2 × (each Delta shelf cluster, high priority) |
| Sampling ports — ceiling     | 1 × (general volume reference)            |
| Total sampling points        | 18                                        |
| Alarm stages                 | Alert, Action, Fire 1, Fire 2 (per VESDA standard) |
| Sensitivity — rack zone      | 0.005% obs/m at Alert                    |
| BMS interface                | VESDAnet + Modbus TCP + dry-contact backup |

### Suppression — Ansul Novec 1230

| Parameter                    | Value                                     |
|------------------------------|-------------------------------------------|
| Agent                        | 3M Novec 1230 (FK-5-1-12)                 |
| Design concentration         | 5.85 % v/v                                |
| Hold time                    | 10 minutes per NFPA 2001                  |
| Cylinder bank                | Right-size per FIRE-001: 72 kg agent required; 2× 180 L = 4× oversized (~275 kg excess mass) |
| Cylinder weight (each)       | ~190 kg                                   |
| Cylinder mounting            | Stainless bracket welded to frame, offshore-grade marine bracket |
| Discharge nozzles            | 8 (distributed along ceiling, 360° coverage) |
| Discharge time               | ≤ 10 seconds to design concentration      |
| Over-pressure vent           | 250 × 250 mm powered damper, opens during discharge to prevent shell over-pressure |
| Pre-discharge alarm          | 30 seconds (strobe + horn + BMS notification) |
| Abort                        | External key switch at each end ECP       |
| Post-discharge recovery      | Cross-vent via ECP ports, agent analysis, recharge |

### Interlocks on Discharge

1. BMS asserts pod shutdown — all Delta shelves commanded off
2. Manifold isolation valves close (prevents coolant pumping during fire)
3. Munters process ducts damper closed at ECP
4. Over-pressure vent opens for 15 seconds during discharge window
5. External strobe + audible at both ECP ends activate
6. Platform SCADA notified within 1 second

### Offshore Delta

- USCG-approved cylinder brackets (marine standard, welded, shock-rated)
- Fire suppression control panel dual-powered (main + backup)
- Additional CO2 or water-mist FDC connection at CDU-end ECP for external fire department augmentation
- Certification to SOLAS Chapter II-2 for gas-flooding systems
- 10-year cylinder hydrotest (marine standard vs 12-year onshore)

---

## §18 GROUNDING, BONDING & EMI SHIELDING

### Single-Point Ground Bar

Located at ELEC end, bolted to container frame with conductive epoxy interface. All grounds converge here:

| Path                          | Connection                               |
|-------------------------------|------------------------------------------|
| Cassette frame                     | Direct weld to ground bar stud           |
| Rack chassis (each of 15)     | 25 mm² flat braid to ground bar          |
| CDU chassis                   | 35 mm² cable to ground bar               |
| Munters skid external         | Via ECP bond stud, separate skid ground  |
| Cable tray (both power + data)| Bonded at each tray section, common path to ground bar |
| Floor load plate              | Welded to container, naturally bonded    |
| Each access panel frame       | Bonded via bolted connection (exterior) + jumper (interior) |
| External platform ground      | Via ECP ground stud, 50 mm² cable to platform SPG |

### Bonding Jumpers (Offshore Variant)

Every removable seam or bolted joint receives a dedicated bonding jumper:
- Access panel frame to container (12 jumpers, one per panel)
- CDU skid to floor plate (2 jumpers)
- ECP bulkhead plate to container (4 jumpers, both ECP ends)
- Any ductwork to chassis (Munters ducts, Novec discharge pipe)

### EMI / RFI Shielding

| Zone                          | Shielding Approach                       |
|-------------------------------|------------------------------------------|
| Container body                | Steel shell = inherent Faraday cage      |
| Access panels                 | EMI gasket (conductive elastomer) inside bolt race |
| ECP penetrations              | Conductive grommets + gland plates       |
| Data fiber bulkheads          | Metallic bulkhead with single-point bond |
| Power cable penetrations      | Shielded cable glands, 360° termination  |

### Lightning Protection (Onshore Variant)

Integrated into platform LPS (Cassette is a node, not a standalone LPS). Pod frame bonded to platform ground grid at ECP. SPD at ELEC ECP protects against residual surges. Not applicable offshore (grounded via platform hull in marine service).

---

## §19 SENSOR INSTRUMENTATION — FULL SCHEDULE

Total sensor count: **~110 points** aggregated at Jetson AGX Orin BMS.

### Per-Rack Sensors (15 racks × 6 points = 90 points)

| Sensor                    | Type                      | Purpose                           |
|---------------------------|---------------------------|-----------------------------------|
| Supply coolant temp       | RTD in thermowell         | Cold-plate inlet monitoring       |
| Return coolant temp       | RTD in thermowell         | Rack ΔT + heat accounting         |
| Coolant flow              | Ultrasonic clamp-on       | Flow integrity + per-rack heat    |
| Rack DC current           | Hall-effect CT            | Load monitoring, anomaly detect   |
| Rack vibration            | 3-axis MEMS accelerometer | Oberon rail integrity, marine motion |
| Leak proximity            | TraceTek tap              | Per-rack leak isolation           |

### Cassette-Level Environmental

| Sensor                        | Qty | Notes                             |
|-------------------------------|-----|-----------------------------------|
| Interior temperature          | 4   | Distributed — ends + middle       |
| Interior humidity             | 2   | Upper + lower zone                |
| Interior static pressure      | 1   | Seal integrity indicator          |
| External temperature          | 1   | Ambient reference (ECP-mounted)   |
| External humidity             | 1   | Ambient reference                 |
| External barometric pressure  | 1   | Weather reference                 |
| Cassette tilt / inclinometer       | 1   | Marine stability + stacking check |
| Cassette shock (container frame)   | 1   | Transit and deployment logging    |

### Fire & Safety

| Sensor                        | Qty | Notes                             |
|-------------------------------|-----|-----------------------------------|
| VESDA sampling points         | 18  | (sampling, not discrete sensors — one VESDA unit aggregates) |
| Novec cylinder pressure       | 2   | Per-cylinder low-pressure alarm   |
| Novec discharge detect        | 1   | Confirms discharge event          |
| Access panel reed switch      | 12  | One per panel, door-open signal   |

### Electrical

| Sensor                        | Qty | Notes                             |
|-------------------------------|-----|-----------------------------------|
| 800 V DC bus voltage          | 1   | At ELEC ECP                       |
| 800 V DC bus current          | 1   | At ELEC ECP                       |
| IMD insulation resistance     | 1   | Ungrounded IT system monitoring   |
| Per-rack breaker status       | 15  | Aux contact to BMS                |
| Maintenance UPS SoC           | 1   | Life-safety battery state         |

### Fluid

| Sensor                        | Qty | Notes                             |
|-------------------------------|-----|-----------------------------------|
| Sump level                    | 3   | Low/mid/high/overflow             |
| Sump conductivity             | 1   | Seawater detection (offshore)     |
| CDU pressure (primary)        | 2   | Supply + return                   |
| CDU pressure (secondary)      | 2   | Supply + return                   |
| Expansion tank level          | 1   | PG25 volume monitoring            |

---

## §20 AUTONOMOUS RUN SYSTEM — JETSON AGX ORIN

### BMS Platform

**NVIDIA Jetson AGX Orin 64 GB industrial**, installed in R15 (storage + management rack). Hot-standby second unit for N+1.

### Software Stack

| Layer                          | Component                               |
|--------------------------------|-----------------------------------------|
| OS                             | Ubuntu 22.04 LTS (JetPack 6.x)          |
| Data collection                | Telegraf (sensor polling, Modbus/SNMP)  |
| Time-series storage            | InfluxDB (local, 30-day retention)      |
| Dashboard (local)              | Grafana (accessible via OOB)            |
| Dispatch / control logic       | Custom Python + MQTT bridge             |
| ML anomaly detection           | TensorRT-optimized models on Orin GPU   |
| External telemetry             | MQTT to platform SCADA + cloud          |
| Backhaul fallback              | Starlink / 4G/5G modem (R15-mounted)    |

### Autonomous Functions (No Network Required)

- Per-rack leak isolation (close UQDs + power off rack)
- Thermal runaway detection (rack temp vs load anomaly)
- Seismic / shock event response (verify all racks bolted, alert, pause workloads)
- Fire detection → Novec discharge sequence
- Power quality deviation → graceful shutdown
- Panel open event → workload pause + arc-flash alert strobe

### Non-Autonomous (Network Required)

- Workload scheduling (from platform cluster manager)
- Firmware updates (signed, scheduled)
- New compute tray commissioning
- Historical analytics beyond 30-day local buffer

### I/O Expansion

Advantech ADAM-6000 series Modbus I/O aggregators in R15:
- 4× ADAM-6017 for 8-channel analog input (RTDs, 4-20 mA loops)
- 2× ADAM-6060 for digital I/O (breaker status, panel reeds, valves)
- 1× ADAM-6050 for high-speed discrete (E-stop, VESDA, Novec)

### Communication Hierarchy

```
Pod sensors  →  ADAM I/O  →  Jetson Orin BMS  →  Platform SCADA
                              ↓                      ↓
                          Local storage         Cloud telemetry
                          (InfluxDB)              (MQTT)
                              ↓
                          Starlink/4G (backup)
```

---

## §21 NETWORKING — INFINIBAND + OOB + STARLINK

### Production Fabric — Quantum-X800 InfiniBand (R14)

- 2× NVIDIA Quantum-X800 QM9700 switches
- 64 × NDR 400 Gb/s ports each
- Internal fabric to compute racks: 15 racks × 4 uplinks = 60 ports used
- External uplinks to platform spine: 24 × 400 Gb/s per switch = 48 ports total
- Total external compute bandwidth: 19.2 Tb/s per pod

### Out-of-Band Management Network

Separate physical LAN:
- Management switch in R15 (NVIDIA SN4000 or Aruba equivalent)
- Cat6A to every Delta shelf (power telemetry)
- Cat6A to CDU (CoolIT Redfish)
- Cat6A to Munters skid (via ECP RJ-45)
- Fiber uplink to platform OOB network

### Starlink / Cellular Backhaul

- Starlink Maritime terminal (offshore) or Business (onshore) mounted on external ECP housing
- 4G/5G modem (Cradlepoint or equivalent) for terrestrial fallback
- Automatic failover via Jetson Orin routing: Primary fiber → Starlink → Cellular
- Emergency telemetry only (not production compute traffic)

### External Fiber Path at ECP

- 24-strand single-mode OS2 MPO for IB uplink
- 24-strand single-mode OS2 MPO for IB downlink
- 2× Cat6A shielded for OOB
- All cables service-looped inside ECP zone for replacement without disassembly

---

## §22 TERMINAL & JUNCTION BOX SCHEDULE

### ELEC End — Terminal Boxes

| Box ID | Purpose                                      | Rating               |
|--------|----------------------------------------------|----------------------|
| TB-1   | 800 V DC main input landing                  | 2,500 A, IP66        |
| TB-2   | 24 V DC maintenance UPS                      | 100 A, IP54          |
| TB-3   | Emergency stop hardwire (2 pairs, latched)   | 24 V DC dry contact  |
| TB-4   | Grounding / bonding central                  | 50 mm² ground bar    |
| JB-E1  | Fiber + OOB data from platform (BMS uplink)  | IP66 with EMI gland  |

### CDU End — Terminal Boxes

| Box ID | Purpose                                      | Rating               |
|--------|----------------------------------------------|----------------------|
| TB-5   | CDU power feed (from platform via ECP)       | 480 V AC 3-ph, 60 A  |
| TB-6   | Munters control & power (to external skid)   | 480 V AC 3-ph, 80 A + Modbus |
| JB-C1  | InfiniBand fiber uplink patch                | 24 × MPO, IP54       |
| JB-C2  | InfiniBand fiber downlink patch              | 24 × MPO, IP54       |
| JB-C3  | OOB copper + console access                  | 8 × RJ-45, shielded  |

### Distributed Junction Boxes (Along Rack Row)

| Box ID           | Purpose                                   | Location          |
|------------------|-------------------------------------------|-------------------|
| JB-R1 to JB-R15  | Per-rack sensor aggregation (6 sensors/rack) | Floor trench, one per rack |
| JB-M1, JB-M2     | Manifold instrumentation (bleed + drain)  | Supply & return ends |
| JB-F1, JB-F2     | Fire/VESDA/Novec interface                | Ceiling, each end |
| JB-L1 to JB-L12  | Panel reed switch + work light control    | Each panel interior |

All boxes bond to single-point ground, all cable entries use EMI-rated glands.

---

## §23 MAINTENANCE UPS & LIFE-SAFETY POWER

### Maintenance UPS Specification

| Parameter                    | Value                                    |
|------------------------------|------------------------------------------|
| Type                         | 24 V DC, LiFePO4 chemistry (preferred) or sealed lead-acid |
| Capacity                     | 2 kWh                                    |
| Runtime (life-safety loads)  | ≥ 2 hours                                |
| Location                     | ELEC end, adjacent to TB-1               |
| Charger                      | Integrated, switches to mains when 800 V DC present |

### Life-Safety Loads (Supported by UPS)

| Load                               | Power (W) |
|------------------------------------|-----------|
| VESDA-E aspirating unit            | 35        |
| Novec 1230 control panel           | 25        |
| Jetson AGX Orin BMS                | 40        |
| Starlink modem (for alerting)      | 75        |
| Interior lighting (LED strips)     | 50 (auto-on panel open only) |
| Access panel reed switches         | 1         |
| Sensor I/O (ADAM modules)          | 30        |
| Emergency strobes (external)       | 40        |
| **Total continuous**               | **~220**  |
| **Total during panel-open event**  | **~270**  |

At 2 kWh capacity and 270 W peak draw: ~7.4 hours of ride-through. Well beyond the 2-hour design target.

---

## §24 STRUCTURAL & SEISMIC ANCHORING

### Rack Anchoring — Both Variants

Each of 15 racks bolts to the load-spreader plate via 4× M16 anchors (one per corner). Anchor torque per OCP ORv3 specification. Removable via same access panel that serves the rack.

### Seismic Rating — Onshore

- IBC 2021 Site Class D
- Sds = 1.0g vertical
- Rack anchoring sized per ASCE 7-22
- Snubbers: rubber-isolated front-to-back and side-to-side, limit rack sway to ±5 mm at design seismic

### Shock & Marine Motion — Offshore

- DNV-OS-D101 marine structural standard
- Roll: up to 30° at 10-second period
- Pitch: up to 15° at 8-second period
- Slam / green water: 5 g vertical peak
- Rack shock isolators: Barry Controls or equivalent, spring-damper type
- Additional diagonal bracing rack-to-container at each rack base
- Cross-brace front-to-rear between every 3rd rack

### Container Anchoring

- Onshore: ISO twist-lock at each corner casting to concrete pad with embedded plate
- Offshore: ISO twist-lock + supplementary marine lashing to deck cleats (minimum 8 lashing points per pod)

---

## §25 MARINIZATION — OFFSHORE VARIANT DELTAS

Single-reference summary (detail throughout document):

**Materials:**
- All exterior steel: grit-blasted to SA 2.5, ice-class epoxy primer, polysiloxane topcoat
- All fasteners: Monel or Inconel
- All interior bolts / brackets: 316L stainless
- Gaskets: quadruple-bulb silicone + EPDM secondary
- Paint system certified 20-year offshore by Jotun, International, or Hempel

**Sealing:**
- Access panels: IP66 minimum, witness-tested to 0.05 ACH at commissioning
- ECP: IP66 / NEMA 4X connectors only
- Every ECP penetration: compression gland + EMI gasket + internal vapor barrier

**Electrical:**
- Marine cable throughout (MIL-DTL-24643 or IEC 60092)
- Bonding jumpers across every bolted seam (§18)
- SPD rated for marine lightning environment

**Certifications:**
- ABS, DNV, or Lloyd's Register module certification
- USCG approval for Novec 1230 on offshore facility
- SOLAS Chapter II-2 gas-flooding system compliance

**Mechanical:**
- All rack shock isolators installed (not optional)
- Diagonal bracing installed
- Tilt sensor active with BMS alerting
- Lashing points: 8× deck cleats minimum per pod

**Maintenance:**
- Cylinder hydrotest every 10 years (vs 12 onshore)
- Gasket replacement every 3 years (vs 5 onshore)
- Panel torque verification every 12 months (vs 24 onshore)
- Annual pressure decay test at 0.05 ACH

---

## §26 ACOUSTIC & THERMAL ENVELOPE

### Acoustic

Interior sound pressure at full load: estimated 95–105 dBA (15 racks of fans + in-shelf power fans + CDU pumps). Exterior with panels closed: ~65–70 dBA at 1 m. Exterior with panel open: 90+ dBA at 1 m.

- Interior acoustic damping: ceiling + end walls lined with 50 mm melamine acoustic foam (Class A fire rated)
- Exterior labels: hearing PPE required when any panel is open
- Service procedures: 2-person crews with communication headsets

### Thermal — External Skin Temperature

Container skin temperature at full load, design-day ambient:
- Onshore Louisiana (35 °C ambient): skin 38–40 °C (minimal internal heat escape, chilled water carries everything)
- Offshore North Sea (5 °C ambient): skin 8–12 °C
- No thermal protection concerns; standard touch-safe with 100 °C cutoff well clear

### Envelope Insulation

- 75 mm closed-cell polyurethane foam against interior walls
- Vapor barrier (aluminum foil laminate) between insulation and shell
- Effective R-value: ~R-22
- Reduces solar gain (Louisiana) by ~85% vs bare steel
- Keeps interior within 5 °C of ambient with cooling off (passive safe state)

---

## §27 COMMISSIONING & PRESSURE-TEST PROCEDURE

### Factory Acceptance Test (FAT) — Before Ship

1. Shell leak test at 500 Pa positive pressure — decay < 50 Pa in 5 min
2. All ECP penetrations individually pressure-verified
3. Primary coolant loop hydrostatic test at 1.5× working pressure
4. Delta power shelf dry run at each rack position
5. BMS sensor verification — all 110+ points report correctly
6. VESDA sensitivity test per stage
7. Novec discharge circuit continuity (no actual discharge)
8. Access panel torque witness per bolt pattern

### Site Acceptance Test (SAT) — After Install

1. All ECP connections torque-verified
2. Cold-loop coolant circulation — 4 hour baseline
3. Power-on sequence — racks staged 10% → 25% → 50% → 75% → 100%
4. Thermal equilibrium verified: cold plate supply ≤ 45 °C at 100% load for 4 hours continuous
5. Simulated leak (water injection at test port) — verify TraceTek + sump response
6. Panel-open event simulation — verify reed switch + BMS response
7. Munters skid commissioning (external) — process air loop verified
8. InfiniBand fabric loopback at each QM9700 port
9. Workload test — NVIDIA dgxcheck or CUDA-AI benchmark at 24 hours

### Annual Integrity Test

1. Pressure decay test — 500 Pa positive, decay ≤ 100 Pa in 5 min (onshore), ≤ 50 Pa in 5 min (offshore)
2. Panel gasket borescope inspection
3. Novec cylinder pressure check
4. VESDA airflow test
5. TraceTek resistance walk

---

## §28 SERVICE ACCESS CHOREOGRAPHY

Unmanned Cassette — all service from outside. Three primary service scenarios:

### Scenario 1 — Rack Hot-Swap (Failed Compute Tray)

1. Platform drains workload from affected rack (BMS commands)
2. Rack power-off via Delta shelf remote command
3. Coolant isolation: BMS closes Stäubli UQD disconnects
4. Identify panel serving affected rack (AP-X per §9 mapping)
5. External crew:
   - De-torque panel bolts (~40 bolts, 15 min)
   - Remove panel, place on service stand
   - Remove failed compute tray (NVIDIA MGX standard tool-free tray pull)
   - Insert replacement tray
   - Reseal panel with fresh gasket + torque sequence (30 min)
6. BMS re-verifies panel closure (reed + pressure)
7. Re-open UQDs, re-power rack, re-join fabric
8. Total: ~90 minutes for tray swap, not including shipping of replacement

### Scenario 2 — CDU Filter Change

1. CDU has redundant filters — bypass to standby
2. Remove AP-6 (CDU-side panel)
3. CoolIT CHx2000 is front-serviceable — touchscreen + filter access
4. Swap filter cartridge, verify pressure normal
5. Reseal AP-6
6. Total: ~60 minutes

### Scenario 3 — No-Service Inspection

For annual checks without breaking seal:
- Borescope port on each panel — verify gasket integrity without removal
- Thermal imaging via ECP IR camera port
- BMS telemetry review via OOB network

### Tooling Required Per Service

- Torque wrench calibrated to panel bolt spec
- Panel service stand (keeps removed panel vertical, prevents gasket damage)
- Gasket replacement kit (pre-cut to panel perimeter)
- Anti-galling compound (offshore only, for Monel bolts)
- Fresh EMI gasket (offshore only)
- Clean room pop-up tent (offshore, for dust/salt control during open event)

---

## §29 BILL OF MATERIALS (BY CLASS)

### Major Equipment

| Class                                    | Qty | Notes                              |
|------------------------------------------|-----|------------------------------------|
| 40 ft HC ISO container (modified)        | 1   | Per §3                             |
| Vera Rubin NVL72 rack, Oberon            | 13  | Compute R1–R13                     |
| NVIDIA Quantum-X800 InfiniBand rack      | 1   | R14                                |
| Storage + management rack                | 1   | R15 with Jetson Orin + NVMe        |
| Delta 110 kW Vera Rubin NVL72 Power Shelf | 13 | One per compute rack               |
| Delta 800 V → 50 V DC/DC Power Shelf      | 13 | One per compute rack               |
| CoolIT CHx2000 CDU                       | 1   | CDU end zone                       |
| Munters HCD-600 on external skid         | 1   | Per §16                            |
| Jetson AGX Orin BMS (N+1)                | 2   | In R15                             |

### Electrical

| Item                                    | Qty |
|-----------------------------------------|-----|
| 800 V DC main disconnect, 2,500 A       | 1   |
| Surge protection device                 | 1   |
| Bender iso-PV1685 IMD                   | 1   |
| Revenue meter                           | 1   |
| Maintenance UPS, 2 kWh                  | 1   |
| Power busway, 800 V DC 4,000 A          | 1 lot |
| Per-rack DC breaker, 250 A              | 15  |
| Cable tray (aluminum ladder)            | 1 lot |
| Ground bar                              | 1   |
| Bonding jumpers (offshore)              | 24+ |

### Fluid

| Item                                    | Qty |
|-----------------------------------------|-----|
| Stainless manifold, 125 mm (floor trench) | 2 × 9 m |
| Stäubli UQD-25 blind-mate              | 86 (43 supply + 43 return) |
| Isolation valves (per rack)             | 30 |
| Air bleed points                        | 8 |
| Drain ports                             | 3 |
| Floor sump + pump                       | 1 |
| Expansion tank                          | 1 |
| Pressure relief valve                   | 1 |

### Fire & Life Safety

| Item                                    | Qty |
|-----------------------------------------|-----|
| VESDA-E VEU-A00 aspirating unit         | 1   |
| VESDA sampling tube network             | 1 lot |
| Novec 1230 cylinder (180 L)             | 2   |
| Novec discharge nozzle                  | 8   |
| Novec control panel                     | 1   |
| Over-pressure vent (powered damper)     | 1   |
| External strobe                         | 2   |
| Emergency stop switches                 | 4   |

### Sensors & Controls

| Item                                    | Qty |
|-----------------------------------------|-----|
| RTD thermowells (per rack, 2 per rack)  | 30  |
| Ultrasonic flow meters (per rack)       | 15  |
| Hall-effect CTs (per rack)              | 15  |
| 3-axis MEMS accelerometers (per rack)   | 15  |
| Interior T/RH sensors                   | 6   |
| External T/RH/pressure sensor           | 1   |
| Tilt / inclinometer                     | 1   |
| Shock sensor                            | 1   |
| Sump sensors (level, conductivity)      | 4   |
| Access panel reed switches              | 12  |
| ADAM I/O modules                        | 7   |
| TraceTek leak cable                     | 80 m |

### Offshore-Only Additions

| Item                                    | Qty |
|-----------------------------------------|-----|
| Marine cable (MIL-DTL-24643)            | 1 lot |
| Monel / Inconel fasteners               | 1 lot |
| Shock isolators per rack                | 60 (4 per rack × 15) |
| Diagonal bracing                        | 6 sets |
| Marine lashing points                   | 8   |
| EMI gaskets (panels)                    | 12  |
| FDC connection                          | 1   |
| USCG-approved cylinder brackets         | 2   |

---

## §30 OPEN ITEMS, 


### Open Items

| ID    | Item                                                                  | Priority |
|-------|-----------------------------------------------------------------------|----------|
| C-01  | Confirm Vera Rubin NVL72 loaded rack weight with NVIDIA/Foxconn/HPE  | P-0      |
| C-02  | Delta 110 kW shelf — confirm 800 V DC input variant spec             | P-0      |
| C-03  | CoolIT CHx2000 RFQ — lead time and delivery schedule                  | P-0      |
| C-04  | Munters HCD-600 RFQ — electric reactivation, IP66 skid option         | P-1      |
| C-05  | Ansul Novec 1230 — USCG-approved cylinder bracket source (offshore)   | P-1      |
| C-06  | ABS / DNV module certification path (offshore variant)                | P-1      |
| C-07  | Bender iso-PV1685 IMD — 800 V DC variant confirmation                 | P-1      |
| C-08  | VESDA-E VEU-A00 vs VEP-A00 for 18-sampling-point pod                 | P-2      |
| C-09  | Container fabrication partner — 40 ft HC with 12-panel modifications  | P-2      |
| C-10  | Stäubli UQD-16 lead time at 30-unit quantity                         | P-2      |

### Risk Register (Pod-Level Only)

| ID   | Risk                                                   | L | C | Rating | Mitigation                                    |
|------|--------------------------------------------------------|---|---|--------|-----------------------------------------------|
| R-01 | Rack weight > 1,500 kg → ISO gross exceeded            | M | 4 | HIGH   | Confirm C-01 before procurement commits      |
| R-02 | Vera Rubin NVL72 rack delivery slip → pod schedule slip | M | 4 | HIGH   | Oberon is industry-common; multi-vendor pool |
| R-03 | Panel gasket leak in marine service                    | M | 3 | MED    | Quadruple-bulb + annual pressure test        |
| R-04 | Novec discharge over-pressures shell                   | L | 4 | MED    | Powered vent damper sized per NFPA 2001      |
| R-05 | Munters skid single-point failure                      | L | 3 | MED    | N+1 at platform level; pod M4 fallback exists |
| R-06 | Delta 110 kW shelf not yet shipping in volume          | M | 3 | MED    | Confirm availability in C-02                 |
| R-07 | CHx2000 CDU ultracap insufficient for Kyber future     | L | 2 | LOW    | Kyber is different pod — not this pod        |
| R-08 | Floor load concentration damages ISO shell             | L | 3 | MED    | 6 mm load-spreader plate per §24             |
| R-09 | Salt spray ingress despite IP66 ECP                    | L | 4 | MED    | Double-gland + annual inspection             |
| R-10 | Panel torque creep under thermal cycling               | M | 2 | MED    | Annual torque verification per §27           |

---

**Cassette — Interior Design Specification · Cassette-Interior-001 · Rev 2.0 · 2026-04-19**
**Scott Tomsu · scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana**
**CONFIDENTIAL**
