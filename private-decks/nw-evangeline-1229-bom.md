# Bill of Materials — 1229 NW Evangeline Thruway, Lafayette LA

**Site:** Former Walmart shell, 228,569 SF, retrofit model, existing slab (no cutting)
**Rack Platform:** NVIDIA Vera Rubin NVL144, water-cooled, UQD08 manifold, 600 kW/rack
**Pod Definition:** 40 racks (2 rows × 20, rear-to-rear), 24 MW terminal load, single fault domain
**BOM Type:** Quantity and specification — no pricing

---

## SECTION 1 — PER-POD LINE ITEMS

*Quantities below are per single pod added. Multiply by phase 1 pod count for total.*

### 1.1 Rack Platform & Structure

| # | Description | Unit | Qty Basis | Notes / TBD |
|---|---|---|---|---|
| 1.1.1 | NVIDIA Vera Rubin NVL144 rack, water-cooled, 600 kW, UQD08 manifold | each | 40 per pod | Vendor scope terminates at twist-lock (cooling) and top-of-rack J-box (electrical) |
| 1.1.2 | Raised rack platform — height = trunk OD + drip tray depth + grating thickness + branch valve clearance | LF | 2 rows × 20 rack positions per pod (length per row TBD on trunk OD selection) | **TBD (STR-TBD-1):** platform height pending trunk pipe OD selection; branch valve operator clearance under grating may drive height |
| 1.1.3 | Steel grating, walkable, rated for whole-rack extraction load on casters | SF | Coverage of full trunk corridor between rear-facing rows (≈50 ft trunk run × corridor width) | Spec: removable panels for trunk access; load rating to whole-rack extraction wheel point load |
| 1.1.4 | Drip tray, slab-mounted, full length of trunk corridor, sloped to sump | LF | Full 50 ft trunk run | Sized to contain trunk volume + safety margin |

### 1.2 Cooling — Facility Scope (Trunk to Rack Base)

| # | Description | Unit | Qty Basis | Notes / TBD |
|---|---|---|---|---|
| 1.2.1 | Trunk line — supply, sized for 24 MW pod terminal load at installation | LF | 50 ft per pod | Sized once for full pod load; not incrementally upsized |
| 1.2.2 | Trunk line — return, sized for 24 MW pod terminal load at installation | LF | 50 ft per pod | Matches supply |
| 1.2.3 | Trunk isolation valve, supply side, full-port, at trunk end | each | 1 per pod | Pod = fault domain |
| 1.2.4 | Trunk isolation valve, return side, full-port, at trunk end | each | 1 per pod | |
| 1.2.5 | Trunk isolation valve actuator, BMS-tied | each | 2 per pod | One per isolation valve |
| 1.2.6 | Branch valve at each trunk tap pair (supply + return), with cap for unpopulated positions | pair | 40 pairs per pod | Allows incremental rack additions within pod |
| 1.2.7 | Trunk tap — mating half of rack twist-lock, ~3 inch class | each | 80 per pod (2 per rack position) | Supply + return per rack; **confirm exact connection size against NVL144 CDU spec before ordering** |
| 1.2.8 | Rack twist-lock fitting, ~3 inch class — **NOT** quick disconnect | each | 80 per pod (2 per rack) | Twist-lock spec is locked |
| 1.2.9 | Sump, slab-mounted, tied to drip tray, single per pod | each | 1 per pod | Receives any leak from trunk corridor |
| 1.2.10 | Conductivity leak detection sensor, sump-mounted, BMS-tied | each | 1 per pod (minimum) | Per-pod sump tie to BMS |
| 1.2.11 | Sump pump, with high-level alarm to BMS | each | 1 per pod | |
| 1.2.12 | Propylene glycol coolant charge for pod loop (trunk + branches + tap pigtails) | gallons | Per pod loop volume calc | **TBD (C-TBD-1):** glycol concentration pending engineering session |

### 1.3 Electrical — Per Pod (AC Day One, 1500 VDC Future-Sized)

| # | Description | Unit | Qty Basis | Notes / TBD |
|---|---|---|---|---|
| 1.3.1 | Pod power panel — AC distribution, sized for 24 MW pod load | each | 1 per pod | Day one AC; rack PSU shelves rectify at rack |
| 1.3.2 | Cable tray — overhead, full pod length, home run routing from pod power panel to rack J-boxes | LF | Per pod layout routing | Tray sized for 40 home runs; individual drops from tray to each top-of-rack J-box |
| 1.3.3 | Home run conduit — overhead routing, pod power panel to top-of-rack J-box | LF | 40 home runs per pod, length per as-built routing | Conduit fill sized for **1500 VDC upgrade path conductor** |
| 1.3.4 | Home run conductor — AC day one, sized for **1500 VDC upgrade path at full 600 kW rack load**; insulation voltage rating: 1500 VDC class | LF (set) | 40 sets per pod | Ampacity AND insulation voltage class must be sized now to avoid rip-and-replace at next-gen upgrade |
| 1.3.5 | Top-of-rack J-box, hard-wired terminations, torque-checked spec | each | 40 per pod | No plugs — hard-wired at every termination |
| 1.3.6 | Pod power panel breakers / OCPD, per home run | each | 40 per pod | Coordinated with home run conductor sizing |

### 1.4 Pod-Level BMS Integration

| # | Description | Unit | Qty Basis | Notes |
|---|---|---|---|---|
| 1.4.1 | BMS I/O point set per pod — conductivity sensor, sump high-level, isolation valve position (×2), valve actuator command (×2), trunk supply/return temp + pressure | set | 1 per pod | Tied to site BMS |

---

## SECTION 2 — SITE-LEVEL LINE ITEMS

### 2.1 Heat Rejection

| # | Description | Unit | Qty Basis | Notes / TBD |
|---|---|---|---|---|
| 2.1.1 | Dry cooler with adiabatic assist — roof-mount and/or surrounding pad | each | **TBD (HR-TBD-1):** quantity pending phase 1 pod count and ambient design day calc | Sealed dielectric closed loop. **No cooling tower. No river. No evaporative tower.** |
| 2.1.2 | Dry cooler structural support — roof curbs and/or pad | LS | Per dry cooler quantity and placement | Roof structural analysis for dry cooler dead loads required — see Section 3 |
| 2.1.3 | Adiabatic pre-cool water service to dry coolers | LS | Per dry cooler quantity | Make-up water only — not evaporative tower |
| 2.1.4 | Closed-loop circulation pumps (N+1 minimum), VFD-driven | each | **TBD:** sized to total pod count flow | Sealed loop, dielectric-compatible |
| 2.1.5 | Closed-loop expansion tank, air separator, fill station | LS | 1 per loop | |
| 2.1.6 | Heat exchanger between facility loop and pod trunk loops, if loop separation required | each | **TBD (E-TBD-1):** pending engineering decision on single-loop vs. dual-loop architecture | Flag for engineering decision |

### 2.2 Air Conditioning

| # | Description | Unit | Qty Basis | Notes / TBD |
|---|---|---|---|---|
| 2.2.1 | Desiccant dehumidification unit | each | **TBD (HVAC-TBD-1):** quantity and zone mapping | Active pods only — idle pods unconditioned |
| 2.2.2 | Zone partitioning / soft separation between active and idle pod areas | LS | **TBD:** zone count | Pending zone mapping |

### 2.3 Prime Power

| # | Description | Unit | Qty Basis | Notes / TBD |
|---|---|---|---|---|
| 2.3.1 | Cat CG260-16 genset, behind-the-meter natural gas | each | **TBD (P-TBD-1):** quantity pending phase 1 pod count | Trappeys-class platform — locked prime mover |
| 2.3.2 | Genset enclosure (sound-attenuated, weatherproof) | each | 1 per genset | |
| 2.3.3 | Genset pad — concrete, sized per genset spec sheet | each | 1 per genset | Geotech to confirm bearing |
| 2.3.4 | Natural gas lateral service to site | LS | 1 | **TBD (P-TBD-2):** Atmos vs. CenterPoint utility selection |
| 2.3.5 | Gas pressure regulation / metering skid | LS | 1 | Sized to total genset gas demand |
| 2.3.6 | Genset paralleling switchgear | LS | Sized to total genset count | **TBD (ELEC-TBD-1):** switchgear class pending genset output voltage confirmation |
| 2.3.7 | Genset exhaust stacks, silencers, emissions controls per LDEQ permit | LS | Per genset count | LDEQ air permit scope |
| 2.3.8 | Day tank / fuel system (lube oil, coolant make-up) | LS | Per genset count | |

### 2.4 BESS (Supplemental, DC-Coupled)

| # | Description | Unit | Qty Basis | Notes / TBD |
|---|---|---|---|---|
| 2.4.1 | BESS enclosure, DC-coupled to 800 VDC site bus | each | **TBD (B-TBD-1):** vendor and sizing | Supplemental / upgrade path — not primary |
| 2.4.2 | BESS DC tie to site bus — DC-DC converter or direct tie per vendor topology | LS | Per BESS sizing | |
| 2.4.3 | BESS pad and enclosure | LS | Per BESS quantity | |
| 2.4.4 | BESS BMS / SCADA integration | LS | 1 | |

### 2.5 Solar & EV (Supplemental, DC-Coupled)

| # | Description | Unit | Qty Basis | Notes / TBD |
|---|---|---|---|---|
| 2.5.1 | Rooftop PV panels | each | **TBD (S-TBD-1):** panel count pending roof structural and shading study | Supplemental, not primary |
| 2.5.2 | Parking canopy structural — steel canopy with PV mounting; structure sized for future equipment load day one | SF | **TBD (S-TBD-2):** canopy footprint pending site plan | |
| 2.5.3 | Parking canopy PV panels | each | **TBD:** count pending canopy area | |
| 2.5.4 | DC fast chargers (EVSE), NEVI-compliant, mounted to canopy pedestals | each | **TBD:** count pending canopy footprint and NEVI application | Site is NEVI eligible (I-10/I-49 Alternative Fuel Corridor confirmed) — NEVI funding may offset this scope |
| 2.5.5 | EVSE conduit and electrical from site bus to charger pedestals | LS | Per charger count and routing | |
| 2.5.6 | DC combiners, string-level | LS | Per array sizing | |
| 2.5.7 | DC-DC buck converter — solar array tie to 800 VDC site bus | LS | Per array sizing | DC-coupled to site bus, not AC inverter |
| 2.5.8 | Roof structural reinforcement (if required by PV load) | LS | **TBD (S-TBD-3):** pending structural review of existing Walmart roof | Existing shell capacity unknown |

### 2.6 Site Bus & Power Conversion

| # | Description | Unit | Qty Basis | Notes |
|---|---|---|---|---|
| 2.6.1 | 800 VDC site bus — BESS and solar tie-in | LF | Per site routing | **Sized for 1500 VDC upgrade path** |
| 2.6.2 | Power conversion stage — 800 VDC site bus to AC pod power panels | each | **TBD:** 1 per pod or per conversion block — quantity basis to be confirmed | Day one bridge between DC site bus and AC pod distribution; bidirectional converter or DC-AC inverter per block |
| 2.6.3 | Site bus DC switchgear, OCPD, isolation | LS | 1 | |
| 2.6.4 | Utility AC service entrance and main switchgear (LUS interconnection) | LS | 1 | Coordinate with LUS; existing Walmart service likely disconnected — new application required |

### 2.7 Network / Fiber / MMR

| # | Description | Unit | Qty Basis | Notes |
|---|---|---|---|---|
| 2.7.1 | Meet-Me Room (MMR) build-out — racks, ladder rack, power, cooling, access control | LS | 1 | |
| 2.7.2 | Carrier service | LS | 1 | **TBD (N-TBD-2):** carrier and service availability at this address require verification; listed as LUSFiber in broker materials — not independently confirmed |
| 2.7.3 | Fiber path from MMR to street | LF | **TBD (N-TBD-1):** path and conduit count pending route survey | Flag path and conduit count as TBD |
| 2.7.4 | Outside plant conduit, handholes, vaults | LS | Per fiber path design | |
| 2.7.5 | Backbone fiber from MMR to each pod | LF | Per pod count and routing | |

### 2.8 Site BMS / SCADA

| # | Description | Unit | Qty Basis | Notes |
|---|---|---|---|---|
| 2.8.1 | Site BMS head end — server, redundant controllers, operator workstations | LS | 1 | Aggregates all per-pod I/O sets, gensets, dry coolers, BESS, solar, site bus |
| 2.8.2 | Network infrastructure for BMS (segregated from production) | LS | 1 | |

### 2.9 Fire Suppression

| # | Description | Unit | Qty Basis | Notes / TBD |
|---|---|---|---|---|
| 2.9.1 | Fire suppression system — compute zones | LS | **TBD (FS-TBD-1):** system type (pre-action dry-pipe minimum; clean agent for critical zones) and zone mapping | Existing Walmart wet-pipe sprinklers are retail class — not suitable for compute zones; fire protection engineer of record required |
| 2.9.2 | Fire suppression — non-compute areas (corridors, utility rooms, office) | LS | Per zone mapping | Existing wet-pipe may be retained in non-compute zones pending inspection |

### 2.10 Security & Access Control

| # | Description | Unit | Qty Basis | Notes |
|---|---|---|---|---|
| 2.10.1 | Access control — perimeter doors, man-traps, server zone entries | LS | Per zone layout | |
| 2.10.2 | CCTV / surveillance — interior and exterior | LS | Per site layout | |
| 2.10.3 | Perimeter fencing and vehicle barriers | LF | Per site survey | |

### 2.11 Site Civil / Shell Modifications

| # | Description | Unit | Qty Basis | Notes |
|---|---|---|---|---|
| 2.11.1 | Shell envelope modifications — wall penetrations for gas, electrical service, fiber | LS | Per as-built routing | No slab cutting |
| 2.11.2 | Roof modifications — dry cooler curbs, PV mounting, exhaust penetrations | LS | Per equipment placement | |
| 2.11.3 | Existing slab assessment — **point load analysis** for rack platform concentrated loads; Walmart retail slab designed for distributed loads (~125 PSF typical), not NVL144 water-filled rack point loads | LS | 1 | Required prior to platform install; structural engineer must analyze point loads specifically, not general capacity |
| 2.11.4 | Existing RTU survey and disposition — inventory, condition assessment, removal/abandonment plan | LS | 1 | Large RTUs observed on roof; must be cleared before dry cooler placement; existing roof penetrations documented for reuse or patching |
| 2.11.5 | Interior retail demo — existing fixtures, shelving, ceiling grid, MEP rough-in | LS | Per zone mapping | Scope unknown until interior access; flag as open |
| 2.11.6 | Loading dock and rack ingress preparation — floor protection, staging area, access route confirmation | LS | 1 | Existing Walmart rear loading docks are primary rack delivery path |

---

## SECTION 3 — PRE-CONSTRUCTION SOFT COSTS

| # | Description | Unit | Qty Basis | Notes |
|---|---|---|---|---|
| 3.1 | Phase I Environmental Site Assessment (ASTM E1527-21) | LS | 1 | Walmart shell — retail/commercial history, screen for prior tenants and adjacent uses |
| 3.2 | Phase II ESA (if Phase I identifies RECs) | LS | Conditional — 1 if warranted | Soil/groundwater sampling, scope per Phase I findings |
| 3.3 | Property Condition Report (PCR) | LS | 1 | Building has been vacant; PCR covers deferred maintenance, roof integrity, water intrusion, structural, MEP condition; distinct from Phase I ESA |
| 3.4 | Subsurface Utility Engineering (SUE) / GPR scan | LS | 1 | Walmart sites have extensive underground infrastructure (sprinkler mains, electrical conduits, plumbing laterals); required before any new exterior penetrations or pad work |
| 3.5 | ALTA/NSPS Land Title Survey | LS | 1 | Required for title/easement and lender |
| 3.6 | Title commitment and easement review | LS | 1 | Identify existing utility easements, access, encroachments |
| 3.7 | Easement work — new utility easements (gas lateral, fiber, LUS service) as required | LS | Per as-built routing | |
| 3.8 | Louisiana ITEP pre-qualification filing | LS | 1 | **Must file before any construction begins** — Louisiana Economic Development pre-construction requirement |
| 3.9 | Enterprise Zone certification filing | LS | 1 | EZ confirmed — file before construction; parallel track with ITEP |
| 3.10 | NMTC structuring — legal/advisory fees for QLICI and CDE engagement | LS | Conditional — if NMTC financing pursued | New Markets Tax Credit eligible; structuring costs are real and front-loaded |
| 3.11 | NEVI application — federal EV infrastructure funding | LS | 1 | I-10/I-49 Alternative Fuel Corridor confirmed NEVI eligible; application offsets EVSE scope cost |
| 3.12 | Roof structural load analysis — dry cooler dead loads | LS | 1 | Explicit analysis of existing Walmart deck capacity for dry cooler weights (20,000–60,000 lbs each); separate from general roof modification scope |
| 3.13 | Fire protection engineer of record — suppression system design | LS | 1 | Required for compute zone suppression type selection and permitting |
| 3.14 | Geotechnical investigation — borings for genset pads, dry cooler pads, canopy footings | LS | 1 | Existing slab not impacted; new exterior loads require geotech |
| 3.15 | LDEQ air permit — genset emissions | LS | 1 | Long lead time — start early |
| 3.16 | Load flow and short circuit study | LS | 1 | Required for permitting, equipment sizing, and LUS coordination |
| 3.17 | LUS interconnection study and application | LS | 1 | |
| 3.18 | Atmos / CenterPoint gas service application and load study | LS | 1 | **TBD (P-TBD-2):** application contingent on utility selection |

---

## TBD CONSOLIDATED FLAG LIST

| Flag | Description | Section |
|---|---|---|
| C-TBD-1 | Propylene glycol concentration | 1.2.12 |
| STR-TBD-1 | Platform height pending trunk pipe OD selection; branch valve clearance may drive height | 1.1.2 |
| E-TBD-1 | Loop architecture — single facility loop vs. facility/pod heat exchanger separation | 2.1.6 |
| HVAC-TBD-1 | Desiccant dehumidification quantity and zone mapping | 2.2.1, 2.2.2 |
| P-TBD-1 | Genset quantity — depends on phase 1 pod count | 2.3.1 |
| P-TBD-2 | Gas utility selection — Atmos vs. CenterPoint | 2.3.4, 3.18 |
| ELEC-TBD-1 | Genset output voltage configuration — drives switchgear class | 2.3.6 |
| B-TBD-1 | BESS vendor and sizing | 2.4.1 |
| S-TBD-1 | Solar rooftop panel count pending structural and shading study | 2.5.1 |
| S-TBD-2 | Solar canopy footprint and panel count | 2.5.2, 2.5.3 |
| S-TBD-3 | Roof structural reinforcement scope pending PV load analysis | 2.5.8 |
| HR-TBD-1 | Dry cooler quantity and pump sizing — depends on pod count and design day | 2.1.1, 2.1.4 |
| N-TBD-1 | Fiber path and conduit count from MMR to street | 2.7.3 |
| N-TBD-2 | Carrier verification — LUSFiber availability at this address not independently confirmed | 2.7.2 |
| FS-TBD-1 | Fire suppression system type and zone mapping — fire protection engineer of record required | 2.9.1 |

---

## SCOPE BOUNDARY NOTES (LOCKED)

- Rack vendor scope terminates at twist-lock (cooling) and top-of-rack J-box (electrical). Everything upstream is facility scope.
- No plugs anywhere in the system — hard-wired terminations only.
- Plane separation: cooling low (slab level), electrical high (overhead). No coolant fitting above any energized conductor under any failure mode.
- Trunk sized once for 24 MW full pod terminal load at installation. Branch valves and caps allow incremental rack populating within the pod.
- Day one electrical is AC at the pod power panel; rack PSU shelves rectify to DC at the rack. Conduit and conductors sized for 1500 VDC upgrade path — ampacity AND insulation voltage class.
- Pod = single fault domain. Isolation valves at trunk ends.
- No cooling tower. No river. No evaporative tower. Sealed dielectric closed loop to dry coolers only.
- Interior demo scope and zone layout remain open until site access.
