# Cassette — CDU SKID EQUIPMENT SPECIFICATION

**Document:** Cassette-CDUSKID-001
**Revision:** 1.0
**Date:** 2026-04-20
**Classification:** CONFIDENTIAL
**Status:** Released — RFQ Ready

**Purpose:** Procurement-grade specification for the external Coolant Distribution Unit (CDU) skid that replaces the Cassette-internal CoolIT CHx2000. Issued for Request-for-Quotation to industrial process equipment integrators.

**Companion documents:** Cassette-COOL-002 Rev 1.0 (architecture), Cassette-INT-001 Rev 3.0, Cassette-ECP-001 Rev 3.0, Cassette-CTRL-001 Rev 1.0, Cassette-TAGS-001 Rev 1.0

| Rev | Date       | Description                                                                                                        |
|-----|------------|--------------------------------------------------------------------------------------------------------------------|
| 1.0 | 2026-04-20 | Initial release. Single-Cassette duty (2.5 MW class), primary PG25 + secondary CHW, plate-and-frame HX, 5 m³ buffer tank, Siemens S7-1500 skid PLC, N+1 pump redundancy, outdoor NEMA 4X enclosure. |

**Prepared by:** Scott Tomsu · CEO / Chief Engineer
scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana

---

## TABLE OF CONTENTS

- §1  Purpose & RFQ Context
- §2  References & Applicable Codes
- §3  Scope of Supply
- §4  Design Basis — Single Cassette
- §5  Site Conditions & Deployment Envelope
- §6  Skid General Arrangement
- §7  Plate-and-Frame Heat Exchanger
- §8  Primary Circulation Pumps (PG25 Side)
- §9  Secondary Circulation Pumps (CHW Side)
- §10 Strainer & Filtration
- §11 Expansion Tank & Air Separator
- §12 Thermal Buffer Tank
- §13 Piping & Materials
- §14 Quick-Disconnects, Flanges, Flexible Hoses
- §15 Valve Schedule
- §16 Instrumentation Schedule
- §17 Skid PLC & Controls Integration
- §18 Skid Enclosure & Weatherization
- §19 Electrical Service to Skid
- §20 Testing — Factory Acceptance
- §21 Shipping, Delivery & Installation
- §22 Commercial Terms
- §23 RFQ Response Format
- §24 Open Items
- Appendix A — Bidder Datasheet Template

---

## §1  PURPOSE & RFQ CONTEXT

### What We Are Buying

A fully assembled, factory-tested, skid-mounted industrial coolant distribution unit sized for a single 2.5 MW-class Vera Rubin NVL72 compute cassette. Delivered ready to hose up at the cassette ECP and tie into a facility chilled water loop. One quote per skid.

### What We Are Not Buying

- Custom-engineered one-off data center CDU
- Liquid-to-air finned-coil dry cooler
- Chiller plant (absorption, centrifugal, or otherwise)
- Piping from skid to facility chilled water (customer scope)
- Cooling tower, condenser, makeup water system

### Who Should Bid

Industrial process skid integrators with experience in:

- Plate-and-frame heat exchanger installation (Alfa Laval, SWEP, GEA, Tranter)
- Centrifugal pump packaging (Grundfos, Armstrong, Xylem)
- PLC-based process control (Siemens, Allen-Bradley, Schneider)
- Outdoor NEMA 4X enclosures for industrial service

Data-center-specific CDU vendors (CoolIT, Vertiv, Schneider, Nortek) may bid but must accept the industrial-process scope in §3 — this is not a packaged data center CDU.

### Anticipated Bidder Profile

Texas Gulf Coast process skid houses with oilfield service experience are preferred: EPIC Piping, Key Energy, Sunbelt Controls, or similar. Louisiana in-state bidders receive preference for freight and service response reasons but is not required.

---

## §2  REFERENCES & APPLICABLE CODES

### Referenced Documents

| Document              | Description                                  |
|-----------------------|----------------------------------------------|
| Cassette-COOL-002     | External CDU architecture, duty definition   |
| Cassette-ECP-001      | Cassette ECP interface                       |
| Cassette-CTRL-001     | Control architecture (skid PLC integration)  |
| Cassette-MODES-001    | Operating modes and sequences                |
| Cassette-TAGS-001     | OPC UA namespace for skid tags               |

### Applicable Standards

| Code / Standard       | Application                                  |
|-----------------------|----------------------------------------------|
| ASME B31.3            | Process piping (all skid piping)             |
| ASME Section VIII     | Pressure vessels (buffer tank, expansion tank) |
| ASME B16.5            | Flange ratings                               |
| ASHRAE 90.1 / 189.1   | Energy performance (pumping baselines)       |
| IEEE 841              | Severe-duty motor construction               |
| NEC (NFPA 70)         | Electrical installation                      |
| NEMA 250              | Enclosure ratings (4X for outdoor)           |
| NFPA 70E              | Arc flash labeling                           |
| UL 508A               | Industrial control panels                    |
| IEC 61131-3           | PLC programming languages                    |
| IEC 62443             | OT cybersecurity (per CYBER-001)             |
| API RP 14C            | Instrumented safety (Class I Div 2 variant)  |
| NFPA 496              | Purged enclosures (Class I Div 2 variant only) |

### Hazardous Area Classification

Default: **unclassified** (Class I Div 2 variant available for upstream oil & gas deployments — see §5.2).

---

## §3  SCOPE OF SUPPLY

### Included

- [ ] Structural skid base (steel C-channel or wide-flange, painted)
- [ ] Plate-and-frame heat exchanger assembly with frame, gaskets, tie bars
- [ ] (3) Primary PG25 circulation pumps with VFDs and motor starters
- [ ] (3) Secondary CHW circulation pumps with VFDs and motor starters (omitted for Configuration B — absorption chiller direct drive)
- [ ] (1) Duplex strainer, 40 mesh basket, DN150 bore
- [ ] (3) Cartridge filter housings with 25 µm elements, manifolded for N+1 swap
- [ ] (1) Bladder-type expansion tank, 200 L, ASME stamped
- [ ] (1) Micro-bubble coalescing air separator
- [ ] (1) Stratified thermal buffer tank, 5 m³, 316L SS, insulated to R-15
- [ ] All inter-equipment piping per §13
- [ ] All isolation, drain, vent, and balancing valves per §15
- [ ] Instrumentation package per §16
- [ ] Skid PLC with I/O, HMI, networking per §17
- [ ] Motor control center (MCC) per §19
- [ ] Weatherized skid enclosure per §18
- [ ] Factory Acceptance Testing per §20
- [ ] All nameplate, labeling, arc-flash stickers
- [ ] Installation, commissioning, training support per §21

### Excluded (Customer / ADC Scope)

- [ ] Site civil pad and drainage
- [ ] Cassette-to-skid flexible hoses (ADC-furnished; connector data in §14)
- [ ] PG25 glycol fluid charge (ADC-furnished)
- [ ] Facility chilled water piping beyond skid flange
- [ ] Facility electrical feed beyond skid MCC
- [ ] Structural seismic anchoring analysis (ADC engineering)
- [ ] Permitting (ADC / customer)
- [ ] Any rigging, crane service, or post-delivery repositioning

---

## §4  DESIGN BASIS — SINGLE CASSETTE

### Thermal Duty

| Parameter                            | NVL72 Tier   | CPX Tier     |
|--------------------------------------|--------------|--------------|
| Cassette facility heat load          | 1,677 kW     | 2,212 kW     |
| Skid heat rejection capacity (design) | 2,500 kW     | 2,500 kW     |
| Design margin at CPX                 | —            | 13%          |

Design duty is set to 2.5 MW (not the CPX facility load of 2.212 MW) to accommodate:
- Future 3 MW-class racks (CPX-Next / Rubin Ultra)
- Ambient excursions that drop HX effectiveness
- 1 of 3 primary pumps offline

### Primary Circuit (PG25 Side)

| Parameter                    | Value                |
|------------------------------|----------------------|
| Working fluid                | PG25 glycol (propylene glycol 25% v/v in DI water + inhibitor) |
| Design pressure              | 10 bar (145 psi)     |
| Design temperature range     | 25–65 °C (operation 45–57 °C) |
| Supply to cassette (HX outlet) | 45 °C ± 1 °C       |
| Return from cassette (HX inlet) | 55–60 °C           |
| Design flow range            | 2,100–2,500 LPM (2,500 LPM at CPX + margin) |
| PG25 charge volume (skid side) | ~5,500 L           |

### Secondary Circuit (Facility CHW Side)

| Parameter                    | Value                                          |
|------------------------------|------------------------------------------------|
| Working fluid                | Water (nominal)                                |
| Design pressure              | 10 bar or match facility (confirm per site)    |
| Design temperature range     | 5–40 °C                                        |
| Supply to HX                 | 7–12 °C (facility-provided)                    |
| Return from HX               | 18–25 °C                                       |
| Design flow range            | 2,200–2,900 LPM                                |
| Configuration options        | A: Facility CHW · B: Absorption chiller · C: Cooling tower |

### Ambient

- Design ambient air temperature: −5 to +50 °C
- Design humidity: 0–100% RH condensing
- Solar heat gain: full direct sun, unshaded
- Wind loading: 130 mph (exposure C), ASCE 7 per location
- Seismic: SDC D default; SDC E optional offshore Gulf

---

## §5  SITE CONDITIONS & DEPLOYMENT ENVELOPE

### Default Deployment Environments

| Environment                   | Example Site                         | Special Requirements            |
|-------------------------------|--------------------------------------|--------------------------------|
| Industrial site (onshore)     | Lafayette LA service yard            | Baseline                        |
| Upstream oil & gas (onshore)  | Eagle Ford wellpad                    | Class I Div 2 variant           |
| Offshore platform             | Gulf of Mexico production rig         | Marinized + Class I Div 2       |
| Data center colocation        | Houston DLR / Equinix                | Seismic Zone certification       |
| Industrial process site       | LNG export facility                  | Class I Div 1 variant (by exception) |

### §5.1  Baseline (Industrial Site)

- Outdoor installation with protective roof recommended but not required
- No hazardous area classification
- Service access from all four sides
- PG25 drum storage shed within 30 m
- Electrical service: 480 V 3-phase 4-wire, 200 A

### §5.2  Class I Div 2 Variant (Upstream Oil & Gas)

For deployment within 3 m of gas-containing equipment or wellhead piping:

- All motors rated Class I Div 2 Group D (TEFC, internally-sealed)
- Junction boxes certified Class I Div 2
- Skid enclosure purged per NFPA 496 Type Z (low pressure), or skid positioned outside classified area with local junction boxes only
- Heat detector in skid enclosure (gas ignition protection)
- Gas detection (LEL) at skid perimeter, interfaced to ESD system
- VFDs in Class I Div 2 enclosure OR in building MCC outside classified area
- All electrical enclosures minimum NEMA 7 where within classified area

Variant pricing: +15% of base skid price.

### §5.3  Offshore Marinized Variant

Adds to Class I Div 2:

- 316L stainless piping throughout (vs 304L baseline)
- All external hardware 316L
- Marine-grade paint system (3-coat epoxy)
- Tiedown points at all four skid corners, certified 4g lateral
- CE/ABS/DNV certification as required by customer
- Tropical / tropical salt marine ambient rating

Variant pricing: +30% of base skid price.

---

## §6  SKID GENERAL ARRANGEMENT

### Dimensional Envelope

| Parameter                 | Maximum               | Preferred             |
|---------------------------|-----------------------|-----------------------|
| Overall length            | 6,500 mm              | 6,000 mm              |
| Overall width             | 2,400 mm              | 2,200 mm              |
| Overall height            | 2,800 mm              | 2,500 mm              |
| Skid dry weight           | 5,000 kg              | 4,200 kg              |
| Skid wet weight (PG25 fill) | 11,000 kg           | 9,700 kg              |
| Footprint                 | 15.6 m²               | 13.2 m²               |

These dimensions must permit skid transport on a standard flatbed trailer without overwidth permits (US DOT: ≤2,600 mm width for normal haul). Bidders exceeding 2,600 mm width must identify the transport impact.

### General Arrangement Requirements

Bidder shall provide a scaled GA drawing showing:

1. Plan view with all major equipment labeled
2. Side elevation (both sides)
3. End elevations (both ends)
4. Plumbing isometric summarizing piping routes
5. Electrical one-line
6. Major equipment removal paths (how to extract pump or HX plates)
7. Minimum service clearances per equipment vendor

Layout should place:
- Pumps at one end (noise containment)
- HX and piping in center (primary load area)
- Buffer tank at opposite end (structural balance)
- Control panel / MCC accessible from skid side panel
- All instrumentation accessible from grating walkway

### Walkway & Access

- Grating walkway on both long sides, 900 mm wide clear
- Handrails 1,100 mm tall both sides, OSHA-compliant
- Ladder or step-up at each end
- All valves, sight glasses, sensors, sample ports reachable from walkway without entering skid interior

### Skid Base Construction

- Welded steel frame, minimum C10 channel or equivalent wide-flange
- All welds continuous, NDT per ASME B31.3 Category M for critical welds
- Drip pan beneath entire skid, 50 mm deep, sloped to drain connection
- Lifting lugs at four corners rated for 1.5× wet weight
- Tiedown points for tie-down during ocean transport (offshore variant)

---

## §7  PLATE-AND-FRAME HEAT EXCHANGER

### Specification

| Parameter                    | Value                               |
|------------------------------|-------------------------------------|
| Type                         | Gasketed plate-and-frame            |
| Design duty                  | 2,500 kW (heat rejection)           |
| UA required (at LMTD 33 °C)  | ≥ 75,000 W/K (10% margin)           |
| Plate material               | AISI 316L                           |
| Gasket material              | EPDM (glycol + water service)       |
| Plate count                  | As required for UA                  |
| Plate area (estimated)       | 16–25 m² (bidder to confirm)        |
| Design pressure, both sides  | 10 bar                              |
| Design temperature           | 5 to 70 °C                          |
| Primary connections          | DN150 flanged (PN16)                |
| Secondary connections        | DN150 flanged (PN16)                |
| Foundation                   | Adjustable mounting feet on skid    |

### Preferred Models

In descending order of preference:

1. **Alfa Laval M15** — 18–22 m² recommended, proven in HVAC and industrial service
2. **SWEP VM140** — lower cost, tighter lead time
3. **GEA NT150S** — overspec for single cassette; use if 2-cassette skid variant needed
4. **Tranter GX-145** — alternate source

### Performance Requirements

At design conditions (2,212 kW, primary 57→45 °C, secondary 12→23 °C):

- LMTD ≥ 30 °C
- Approach ≤ 3 °C at design flow both sides
- Primary-side ΔP ≤ 0.8 bar at 2,350 LPM
- Secondary-side ΔP ≤ 0.6 bar at 2,900 LPM

### Fouling & Service

- Fouling resistance: R_f ≤ 0.00018 m²·K/W on both sides
- Plate stack removable with on-skid hoist rail above HX
- Plates designed for clean-in-place (CIP) with 3% citric acid
- All gaskets replaceable without plate replacement
- Complete plate stack service time ≤ 4 hours with 2 technicians

---

## §8  PRIMARY CIRCULATION PUMPS (PG25 SIDE)

### Configuration

N+1 redundancy: **2 operating + 1 standby** on common manifold with motorized isolation valves.

### Specification (Each Pump)

| Parameter                    | Value                                    |
|------------------------------|------------------------------------------|
| Type                         | Vertical multistage centrifugal, close-coupled |
| Design flow per pump         | 1,200 LPM at 5.5 bar head                |
| Maximum flow                 | 1,500 LPM (N operation, 2 running)       |
| Motor rating                 | 30 kW                                    |
| Motor class                  | IE3 premium efficiency, TEFC             |
| Motor voltage                | 480 V 3-ph, 60 Hz                        |
| Motor construction (Class I Div 2 variant) | Class I Div 2 rated         |
| Seal                         | Mechanical, double-cartridge, EPDM       |
| Casing material              | Stainless 316L                            |
| Impeller material            | Stainless 316L                            |
| Service factor               | 1.15                                     |

### Preferred Models

1. **Grundfos CRE-64** (30 kW, 2,400 LPM at 5.5 bar, VFD-ready)
2. **Armstrong 4300 end-suction** with VFD
3. **Xylem Bell & Gossett E-1510** with VFD
4. **KSB Etanorm / Secochem**

### VFDs

- Skid-mounted (NEMA 4X enclosure) or MCC-mounted (bidder preference, note in quote)
- Rated 40 kW each (safety margin)
- **ABB ACH580** or **Siemens SINAMICS G120P** or equivalent
- Modbus TCP or Profinet to skid PLC
- Integrated bypass contactor for mains-direct operation on VFD fault

### Failover

- N+1 swap time: <5 seconds per CTRL-001
- Motorized isolation valves close on failed pump, open on standby
- Standby pump pre-rolled at 10% speed (ready to accept flow)

---

## §9  SECONDARY CIRCULATION PUMPS (CHW SIDE)

### Configuration

N+1 redundancy: **2 operating + 1 standby.** Identical control scheme to primary.

### Specification (Each Pump)

| Parameter                    | Value                                    |
|------------------------------|------------------------------------------|
| Type                         | End-suction centrifugal                  |
| Design flow per pump         | 1,450 LPM at 3.3 bar head                |
| Maximum flow                 | 1,900 LPM                                |
| Motor rating                 | 22 kW                                    |
| Motor class                  | IE3 premium efficiency, TEFC             |
| Motor voltage                | 480 V 3-ph, 60 Hz                        |
| Seal                         | Mechanical, single, EPDM                 |
| Casing material              | Ductile iron or cast steel with epoxy lining |
| Impeller material            | Bronze or 316L                           |

### Preferred Models

1. **Grundfos CRE-45** (22 kW, 2,900 LPM at 3.3 bar)
2. **Armstrong 4030 vertical inline**
3. **Xylem Bell & Gossett E-1510 Series 2**

### Omission for Configuration B

For absorption chiller direct-drive (Configuration B per COOL-002 §12), secondary pumps are omitted and replaced by:
- Primary-to-chiller piping spool piece (interface to absorption chiller)
- Pressure sensor monitoring chiller side feedback
- Pricing credit ~$45K for pump assembly omission

---

## §10  STRAINER & FILTRATION

### Duplex Strainer (Primary Loop, Upstream of Pumps)

| Parameter                    | Value                                 |
|------------------------------|---------------------------------------|
| Type                         | Cast iron or SS body, duplex basket   |
| Connections                  | DN150 flanged                         |
| Basket material              | Stainless 316 wire cloth              |
| Mesh                         | 40 mesh (400 µm)                       |
| Design flow                  | 2,500 LPM                              |
| Clean ΔP                     | <0.05 bar                              |
| Alarm ΔP                     | 0.3 bar (basket change indicator)     |
| Change-over mechanism        | Manual lever, no tools required       |

**Preferred: Eaton Model 53BTX DN150 or Hayward 2500-Series DN150.**

### Cartridge Filters (Primary Loop, Downstream of HX)

| Parameter                    | Value                                 |
|------------------------------|---------------------------------------|
| Configuration                | 3 vessels in parallel, 1 online minimum |
| Cartridge rating             | 25 µm nominal, 50 µm absolute         |
| Cartridge length             | 40 inch / 1,016 mm                    |
| Cartridge material           | Polypropylene spun, glycol compatible |
| Vessel material              | 316L stainless                        |
| Design flow per vessel       | 1,250 LPM                              |
| Alarm ΔP (vessel)            | 0.5 bar                                |

**Preferred: Parker Fulflo BV or Pentair 3M LifeAssure series.**

---

## §11  EXPANSION TANK & AIR SEPARATOR

### Expansion Tank

| Parameter                    | Value                                      |
|------------------------------|--------------------------------------------|
| Type                         | Bladder tank, ASME Section VIII stamped    |
| Capacity                     | 200 L                                      |
| Bladder material             | EPDM                                       |
| Shell material               | Carbon steel with epoxy-lined interior    |
| Design pressure              | 10 bar (145 psi)                            |
| Design temperature           | 5–70 °C                                     |
| Precharge pressure           | 1.5 bar (bidder to confirm against system static) |
| Automatic air vent           | Stainless body, at tank high point          |

**Preferred: Amtrol ST-60V or Wessels FXT-120.**

### Air Separator

| Parameter                    | Value                                      |
|------------------------------|--------------------------------------------|
| Type                         | Micro-bubble coalescing                     |
| Position                     | Highest point in piping, upstream of expansion tank |
| Flow rating                  | 2,500 LPM                                   |
| Automatic bleeder            | Yes, corrosion-resistant SS                 |

**Preferred: Spirotherm VJS-150 or Armstrong Vent-O-Matic.**

---

## §12  THERMAL BUFFER TANK

### Specification

| Parameter                    | Value                                      |
|------------------------------|--------------------------------------------|
| Capacity                     | 5,000 L (5.0 m³) nominal                   |
| Geometry                     | Vertical cylindrical, 1,600 mm dia × 2,600 mm tall |
| Material                     | AISI 316L stainless (ASME Section VIII stamped) |
| Design pressure              | 10 bar                                     |
| Design temperature           | 5–70 °C                                    |
| Insulation                   | 75 mm polyurethane foam with aluminum jacket (R-15) |
| Stratification baffles       | 3 internal perforated plates at ~25, 50, 75% height |
| Supply diffuser              | At top, slot-plate radial distributor      |
| Return diffuser              | At bottom, similar                          |
| Temperature probes           | 5-point thermowell array (top, 25%, 50%, 75%, bottom) |
| Level transmitter            | Differential pressure or radar             |
| Access                       | 18" top manway, 10" side manway             |
| Sample / drain ports         | Top, mid, bottom                            |
| Instrumentation ports        | Pressure, temperature, level, sample, vent |

### Stratification Requirement

The tank must maintain thermal stratification during design-case flow events:

- Flow through tank: 0–2,500 LPM
- Allowed thermal mixing: top-to-bottom ΔT must remain ≥ 10 °C during steady-state operation with 1,500 LPM throughput

Bidder shall provide CFD analysis or reference case demonstrating this requirement, or use a pre-validated stratification design (e.g., Wessels Galaxy stratified storage).

**Preferred: Wessels Galaxy SS series with engineered diffusers, or bidder-designed 316L tank with baffle validation.**

---

## §13  PIPING & MATERIALS

### Piping Class Summary

| Service                | Material      | Schedule | Joining Method        |
|------------------------|---------------|----------|----------------------|
| Primary PG25 (main)    | 304L SS (316L for offshore) | Sch 40    | Welded + Victaulic 77 where serviceable |
| Primary PG25 (branch)  | 304L SS       | Sch 40    | Welded or flanged     |
| Secondary CHW (main)   | 304L SS       | Sch 10S   | Victaulic 77          |
| Secondary CHW (branch) | 304L SS       | Sch 10S   | Victaulic 77          |
| Drain & vent           | 304L SS       | Sch 40    | Welded                |
| Instrument tubing      | 316L SS       | —         | Compression (Swagelok) |

### Pipe Sizing

Primary loop at design flow (2,500 LPM):

| Location          | Diameter | Velocity |
|-------------------|----------|----------|
| Main headers      | DN150    | 2.36 m/s |
| Pump suction      | DN200    | 1.33 m/s |
| Pump discharge    | DN150    | 2.36 m/s |
| HX primary side   | DN150    | per vendor |
| Buffer tank inlet/outlet | DN200 | 1.33 m/s |

Secondary loop at design flow (2,900 LPM):

| Location          | Diameter | Velocity |
|-------------------|----------|----------|
| Main headers      | DN150    | 2.74 m/s |
| Pump suction      | DN200    | 1.54 m/s |
| Pump discharge    | DN150    | 2.74 m/s |
| HX secondary side | DN150    | per vendor |

### Code & Inspection

- All pressure piping: ASME B31.3 Category D (normal fluid) at minimum
- Critical welds (pressure vessels, headers, pump discharges) subject to 100% visual inspection + 10% spot radiography
- Hydrostatic test: 15 bar for 60 minutes, both loops, post-fabrication

---

## §14  QUICK-DISCONNECTS, FLANGES, FLEXIBLE HOSES

### Cassette-Side Interface (Primary PG25)

Two connections (supply + return) at the Cassette CDU-end ECP:

| Parameter                    | Specification                              |
|------------------------------|--------------------------------------------|
| Type                         | Dry-break quick disconnect, pipe class     |
| Bore                         | DN150 (6 inch)                              |
| Material (baseline)          | 316L stainless with EPDM seals             |
| Material (offshore)          | 316L stainless with FKM seals              |
| Rated flow                   | 2,500 LPM at 2.0 m/s nominal                |
| Rated pressure               | 16 bar working                              |
| Burst pressure               | 64 bar (4:1 safety factor)                 |
| Cycle life                   | 2,500 connects/disconnects at rated        |

**Approved vendors (per COOL-002 §5):**
- **Stäubli QBH-150 or QBH-200** (preferred — pipe-class, dry-break)
- **Parker Snap-tite 75 Series** (DN150 bore)
- **Tema DryBreak DB-150** (offshore / subsea only)

Bidder to confirm specific model against published flow curve at 2,350 LPM PG25 at 50 °C — flow curve data required with bid.

### Facility Secondary Connection

DN150 class 150 flanged, ASME B16.5 standard. No QD required on secondary side (facility maintenance-scheduled).

### Flexible Hoses (ADC-Furnished, Bidder-Interfaced)

Interface at skid inlet:

| Parameter                    | Specification                              |
|------------------------------|--------------------------------------------|
| Type                         | Stainless steel braided overlay on synthetic inner liner |
| Liner material               | PTFE or EPDM (glycol-compatible)          |
| Bore                         | DN150                                       |
| Length                       | 5 m (standard), 8 m optional               |
| Pressure rating              | 16 bar working, 64 bar burst               |
| Fittings                     | Male Stäubli QBH-150 (skid end), Flanged 150# (optional) |

**Reference: Parker ParFlex 797TC or Gates Mega4000.**

Bidder's responsibility: mating receptacle on skid, thermal insulation for hose (25 mm Aeroflex).

---

## §15  VALVE SCHEDULE

### Summary

Bidder shall provide complete valve list. Key requirements:

| Function                       | Type                              | Material | Actuation |
|--------------------------------|-----------------------------------|----------|-----------|
| Pump isolation (suction/discharge) | Triple-offset butterfly          | 316L     | Manual + motorized |
| HX isolation                   | Triple-offset butterfly            | 316L     | Motorized |
| Buffer tank isolation          | Full-port ball                     | 316L     | Motorized + lockout |
| Expansion tank isolation       | Full-port ball                     | 316L     | Manual + LO |
| Fill / drain                   | Full-port ball                     | 316L     | Manual    |
| Vent                           | Full-port ball + stem-seal         | 316L     | Manual    |
| Flow balancing (per branch)    | Globe-style balancing, static     | 316L     | Manual set |
| Pressure relief (PG25 loop)    | Spring-loaded, soft-seat           | 316L     | Auto — set at 12 bar |
| Pressure relief (secondary)    | Spring-loaded                      | 316L     | Auto — set per facility |
| Check (pump discharge)         | Silent check, vertical-oriented    | 316L     | Auto      |

All valves: ANSI Class 150, end connections matching piping class.

### Actuation Conventions

- Motorized valves: 480 V 3-ph or 24 V DC where fail-safe required
- Position feedback: limit switches for open/close + 4-20 mA for modulating
- Fail-safe: fail-last-position or fail-closed (specified per valve)
- All motorized valves on skid PLC network

---

## §16  INSTRUMENTATION SCHEDULE

### Sensor Summary (Publishes to Skid PLC, then Orchestrator)

| Tag Family                        | Count | Type                                |
|-----------------------------------|-------|-------------------------------------|
| Temperature (RTDs, Pt100)         | 24    | 3-wire, ±0.2 °C accuracy, thermowell-mounted |
| Pressure (gauge, 0–16 bar)        | 12    | 4-20 mA transmitter, ±0.5% FS       |
| Pressure differential             | 6     | 4-20 mA transmitter, ±0.5% FS        |
| Flow (insertion magnetic or ultrasonic) | 4 | 4-20 mA, ±1% accuracy                |
| Level (buffer, expansion)         | 2     | Radar or differential pressure       |
| pH + conductivity                 | 2     | PG25 chemistry monitoring           |
| Vibration (pump bearings)         | 6     | MEMS accelerometer, 4-20 mA RMS      |
| Motor current (each pump)         | 6     | From VFD, native protocol           |
| Valve position (per motor valve)  | 12    | 4-20 mA + limit switches             |
| Leak (skid perimeter TraceTek)    | 1     | TraceTek cable + TTDM-128 controller |
| Skid enclosure ambient            | 2     | Temp + RH                            |
| Gas detect (LEL, Class I Div 2 variant only) | 3 | MSA Ultima XIR or Dräger Polytron |

All tags match Cassette-TAGS-001 §SKID-CDU namespace.

### Minimum Instrument Accuracy (At-Operating-Point)

- Temperature: ±0.2 °C (RTDs preferred over thermocouples)
- Pressure: ±0.5% of full scale
- Flow: ±1% of reading
- Level: ±5 mm or ±1% FS

### Tag Naming Convention

Bidder shall use `SKID-CDU-<section>-<instrument-type>-<sequence>` format per TAGS-001. Bidder tag cross-reference table shall be provided with FAT documentation.

---

## §17  SKID PLC & CONTROLS INTEGRATION

### Primary Controller

**Siemens SIMATIC S7-1500F** preferred (F variant has safety-rated CPU for emergency shutdown logic integration).

Alternate: Allen-Bradley ControlLogix, Schneider Modicon M580, Phoenix Contact AXC F 2152.

### I/O Requirements

- Digital inputs: 64 (limit switches, valve feedback, pushbuttons)
- Digital outputs: 48 (valve actuation, alarm horns, status lights)
- Analog inputs: 48 (4-20 mA + RTD)
- Analog outputs: 16 (valve modulation, setpoints)
- Communications: Profinet (pumps, VFDs), Modbus TCP (instruments), OPC UA (to orchestrator), MQTT Sparkplug B (telemetry stream)

### Programming Requirements

- IEC 61131-3 structured text and/or function block
- Modular: separate FBs for each subsystem (primary pumps, secondary pumps, HX, buffer, filtration, VFD management)
- Alarm management per ISA-18.2
- Logs to onboard historian (30-day local retention) + orchestrator historian (InfluxDB) per CTRL-001

### HMI

- 15" touchscreen, panel-mounted on skid, NEMA 4X
- Pepperl+Fuchs VisuNet if Class I Div 2 variant
- Minimum three overview screens (primary loop, secondary loop, buffer tank state)
- Trending, alarm log, event log
- Read/write only for on-site operators; supervisory access via orchestrator

### Cybersecurity

- Per Cassette-CYBER-001 Rev 1.0
- Firewall between skid OT network and site IT
- Certificate-based authentication for OPC UA
- Signed firmware only (PLC and VFDs)

### Operating Modes

Skid PLC shall implement modes per Cassette-MODES-001:

- COLD_OFF
- COLD_START
- NORMAL
- DEGRADED (one pump failed)
- HOT_STANDBY
- SERVICE (filter/strainer swap, no pumps running)
- EMERGENCY_SHUTDOWN

---

## §18  SKID ENCLOSURE & WEATHERIZATION

### Enclosure Requirements

- **Baseline (industrial):** Open-air skid with equipment-specific weather covers; no full skid enclosure
- **Class I Div 2 variant:** Enclosed NEMA 4X with Type Z purge
- **Offshore variant:** Fully enclosed, double-gasketed, 316L body, chemical-resistant coatings

### Weather Protection (All Variants)

- VFDs, MCC, PLC: NEMA 4X enclosures with climate control (cooling vortex tubes or 200 W HVAC)
- Pumps: canopy-covered, direct rain protection
- HX: direct-exposed (stainless, corrosion-proof) but shaded with sun hood
- Piping insulation: external PUR or Aeroflex with UV-protected aluminum jacket
- All electrical penetrations: Roxtec or equivalent IP66 sealed entries

### Drainage & Containment

- Skid base drip pan 50 mm deep, full skid footprint
- Sloped to drain at skid low point, DN40 connection
- Customer tie-in to site stormwater or oil-water separator
- Chemical-resistant coating on drip pan interior (PG25 is mildly acidic if oxidized)

---

## §19  ELECTRICAL SERVICE TO SKID

### Incoming Service

Single three-phase service to skid MCC:

| Parameter                | Value                               |
|--------------------------|-------------------------------------|
| Voltage                  | 480 V ± 10%, 60 Hz                  |
| Phases                   | 3-phase 4-wire + ground             |
| Rated current            | 250 A (with 25% growth margin)      |
| Incoming breaker         | 300 A molded case                   |
| Short circuit withstand  | 35 kA (bidder to confirm per site)  |
| Grounding                | Separate ground conductor, bonded to skid frame |

### Internal Distribution

Skid MCC with:
- Main breaker 300 A
- 3× VFD feeders for primary pumps (40 A each with 25% margin)
- 3× VFD feeders for secondary pumps (30 A each)
- Control power transformer (480→120/240 V, 5 kVA)
- Lighting/convenience outlets (from control transformer)
- Skid heater feed (if enclosed variant)

### Arc Flash

Bidder shall:
- Provide short-circuit study for all components
- Apply NFPA 70E arc flash labels on MCC (Category 2 or 3 typical)
- Incident energy calculations using IEEE 1584-2018

### Ground Fault Protection

- Main GFI (20 mA trip, Class A)
- Individual GFI on convenience outlets
- Ground loop impedance monitoring (Bender IMD) on 480 V bus

---

## §20  TESTING — FACTORY ACCEPTANCE

### FAT Scope (At Vendor Facility, Before Shipping)

ADC engineering or designee present for witness. Minimum 3-day FAT window.

#### Day 1: Mechanical

- [ ] Hydrostatic pressure test: primary circuit 15 bar for 60 minutes, <50 mbar decay
- [ ] Hydrostatic pressure test: secondary circuit 15 bar for 60 minutes, <50 mbar decay
- [ ] All welds: 100% VT + 10% RT spot radiography
- [ ] Drain and vent all high points; confirm drainability

#### Day 2: Electrical & Instrumentation

- [ ] All motors bumped and rotation verified
- [ ] Instrument calibration at 3 points each (0%, 50%, 100%)
- [ ] VFDs commissioned, tuned, response verified
- [ ] MCC energization, protection verified
- [ ] Arc flash labels affixed
- [ ] Grounding continuity confirmed <1 Ω

#### Day 3: Controls & Integration

- [ ] PLC program loaded, I/O checkout 100%
- [ ] HMI screens exercised
- [ ] All tag values published to test orchestrator
- [ ] OPC UA connection verified
- [ ] MQTT Sparkplug B verified
- [ ] Operating modes simulated per MODES-001
- [ ] Alarm flood test — verify ISA-18.2 compliance
- [ ] Emergency shutdown test (hard-wired E-stop)
- [ ] Documentation package review

### FAT Acceptance

Skid is released to ship when:
- All line items above complete and signed
- All calibration records attached to PLC database
- All vendor certs collected (pressure vessels, motors, pumps, HX)
- As-built P&ID and one-line delivered
- Spare parts list and recommended spares stock delivered
- Operations manual (draft) delivered

### Site Acceptance Test (SAT)

SAT conducted post-installation per Cassette-COOL-002 §16. Bidder support during SAT for 5 business days minimum.

---

## §21  SHIPPING, DELIVERY & INSTALLATION

### Shipping

- Skid shipped on flatbed trailer, tarped
- All openings blanked or shrink-wrapped
- Drying agent desiccant packs inside control enclosures
- Shock recorder attached, data reviewed on arrival
- Lifting instructions stenciled on skid

### Delivery Coordination

- 10 business days notice for delivery
- Delivery window 7 AM – 5 PM local time
- Site must confirm crane availability for unload (skid weight 4–10 tonne)

### Installation Support

- Bidder field technician on-site for skid setting and first connection (2 days)
- Piping interface supervision (facility CHW tie-in) as customer scope
- Startup commissioning assistance per Cassette-COOL-002 §16 (3 business days)
- Operator training: 2 sessions × 4 hours on-site, plus runbook walk-through

### Warranty

Minimum 2 years from commissioning on all equipment. Extended warranty (5 years) available at quote time, priced separately.

### Spare Parts

Bidder to include with quote:
- Recommended 2-year spares list with part numbers and pricing
- Optional: 5-year spare parts kit
- Consumables (gaskets, cartridge filters, seals) priced separately

---

## §22  COMMERCIAL TERMS

### Pricing Structure

Bidder to provide:

1. **Base skid price** — industrial (unclassified) variant, all equipment listed §3
2. **Class I Div 2 variant adder** (per §5.2)
3. **Offshore marinized variant adder** (per §5.3)
4. **Configuration B adder** — absorption chiller interface (deletes secondary pumps)
5. **2-year spares kit** price
6. **5-year spares kit** price (option)
7. **Extended warranty (3-year, 5-year)** pricing
8. **Training (additional sessions)** pricing per day
9. **Field service rate** per hour + travel expenses schedule

### Payment Terms

- 30% at PO
- 30% at FAT passing
- 30% on delivery
- 10% on successful SAT / commissioning

### Delivery Lead Time

Target: 16 weeks from PO. Bidder to confirm based on:
- HX lead time (Alfa Laval M15 is typically 12 weeks; longer for newer configs)
- Buffer tank lead time (316L stainless pressure vessel, 10 weeks typical)
- Motor / VFD lead time (current market, 8–14 weeks)
- Skid fabrication and integration (6 weeks after long-lead items arrive)

### Liquidated Damages

Per week of delivery delay past agreed date: 1% of contract value, capped at 10%.

---

## §23  RFQ RESPONSE FORMAT

Bidder proposal shall include:

1. **Executive summary** — 2 pages max, scope confirmation, pricing summary
2. **Scope of supply matrix** — explicit compliance with each §3 line item (Comply / Deviate with explanation)
3. **Specification matrix** — compliance with each numbered section §4–§21
4. **General arrangement drawings** (§6) preliminary
5. **Heat exchanger selection** — model, plate area, performance curve (§7)
6. **Pump selection** — primary and secondary models, pump curves at design flow (§8, §9)
7. **Instrument list** — vendor / model / tag per §16
8. **PLC proposal** — platform, I/O count, communications (§17)
9. **Electrical one-line diagram** (§19)
10. **Detailed pricing** per §22 structure
11. **Lead time schedule** week-by-week
12. **Past project references** — minimum 3 installations of similar scope (2 MW+ industrial HX + pump skid)
13. **Quality certifications** — ISO 9001 minimum, ASME R or U stamp for pressure vessels
14. **Safety certifications** — relevant trade experience (Class I Div 2, offshore) if variants quoted
15. **Deviations list** — any departure from this spec, with rationale

Proposal due: 6 weeks from RFQ issue.

---

## §24  OPEN ITEMS

| ID      | Priority | Description                                                                                  | Owner              |
|---------|----------|----------------------------------------------------------------------------------------------|--------------------|
| SK-01   | P-1      | Final HX selection between Alfa Laval M15 and SWEP VM140 — trade lead time vs. service experience | ADC engineering |
| SK-02   | P-1      | Skid width decision: 2,200 mm (DOT standard) vs. 2,400 mm (better service access) — trade offroad flexibility for service time | ADC engineering |
| SK-03   | P-1      | Class I Div 2 variant scope: enclosed vs. open with local junction boxes only — cost vs. code simplicity | ADC ↔ first upstream customer |
| SK-04   | P-2      | Configuration B detailed scope: absorption chiller interface, secondary pump deletion, piping spool dimensions | ADC ↔ absorption chiller vendor |
| SK-05   | P-2      | Preferred pump vendor: Grundfos vs. Armstrong — Grundfos has better CDU track record, Armstrong has better LA service presence | ADC procurement |
| SK-06   | P-2      | PLC platform: Siemens S7-1500F baseline acceptable to all likely integrators, or require Allen-Bradley ControlLogix alternate? | ADC ↔ bidder pool |
| SK-07   | P-2      | Spares level of service: 2-year kit baseline cost threshold for go/no-go | ADC procurement |
| SK-08   | P-3      | Warranty extension pricing acceptance: 5-year vs. standard 2-year | ADC commercial |
| SK-09   | P-3      | Transportation mode for interstate: flatbed vs. Conestoga vs. rail — cost/risk trade on 10 tonne skid | ADC logistics |
| SK-10   | P-3      | Post-installation SAT support duration: 3 days adequate, or should we require 5 days minimum? | ADC operations |
| SK-11   | P-3      | Bidder qualification: minimum financial/bonding requirements for projects up to $1M | ADC procurement |

---

## APPENDIX A — BIDDER DATASHEET TEMPLATE

Bidder shall complete the following data summary:

```
BIDDER: _______________________________________
DATE:   _______________________________________
QUOTE REF: ____________________________________

BASE SKID PRICE (USD):             $_______________
CLASS I DIV 2 ADDER (USD):         $_______________
OFFSHORE VARIANT ADDER (USD):      $_______________
CONFIGURATION B ADDER (USD):       $_______________

EQUIPMENT SELECTIONS:
  HX Make/Model:                   _____________________
  HX Plate Area:                   _____ m²
  HX Rated UA:                     _____ W/K
  HX Primary ΔP at 2,350 LPM:      _____ bar
  HX Secondary ΔP at 2,900 LPM:    _____ bar
  Primary Pump Make/Model:         _____________________
  Primary Pump Rated Flow:         _____ LPM at _____ bar
  Secondary Pump Make/Model:       _____________________
  Secondary Pump Rated Flow:       _____ LPM at _____ bar
  Buffer Tank Make/Model:          _____________________
  Buffer Tank Capacity:            _____ L
  Strainer Make/Model:             _____________________
  Filter Housing Make/Model:       _____________________

PLC & CONTROLS:
  PLC Platform:                    _____________________
  HMI Size/Model:                  _____________________
  Historian Spec:                  _____________________

PERFORMANCE AT DESIGN CONDITIONS:
  Total Heat Rejection:            _____ kW
  Primary Pump Head Required:      _____ bar
  Secondary Pump Head Required:    _____ bar
  PUE Contribution (parasitic):    _____% of rejected heat

DIMENSIONS:
  Overall L × W × H:               _____ × _____ × _____ mm
  Dry Weight:                      _____ kg
  Wet Weight (PG25 fill):          _____ kg

LEAD TIME:
  PO to Ready-to-Ship:             _____ weeks
  Shipping + Install + SAT:        _____ weeks
  Total to Commissioning:          _____ weeks

DEVIATIONS FROM SPEC (list items by section):
  _______________________________________________
  _______________________________________________

SIGNED: _______________________________________
TITLE:  _______________________________________
```

---

**Cassette-CDUSKID-001 — CDU Skid Equipment Specification · Rev 1.0 · 2026-04-20**
**Scott Tomsu · scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana**
**CONFIDENTIAL · RFQ READY**
