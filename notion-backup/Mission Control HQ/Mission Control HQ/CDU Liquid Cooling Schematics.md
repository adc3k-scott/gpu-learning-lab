# CDU Liquid Cooling Schematics
*Notion backup — 2026-04-03*

> NVL72 is 100% liquid cooled. No air cooling fallback. CDU units mount rear of each rack. Heat rejected to exterior dry coolers via closed glycol loop.
---
## System Overview
- Type: Rear-door liquid cooling — CDU (Coolant Distribution Unit) per rack
- Loop: Closed primary loop: rack CDU <-> exterior dry cooler
- Coolant: Deionized water + glycol mix (40/60 for Louisiana climate)
- Heat rejection: Exterior dry coolers — no chiller required at Phase 1 scale
- Phase 1 total heat load: NVIDIA rack TDP unconfirmed — size service for 150-250 kW/rack per analyst estimates (not NVIDIA-confirmed)
---
## Loop Topology
### Primary Loop (High Temp)
- Supply temp target: 45C supply to CDU inlet
- Return temp target: 55-60C return from CDU outlet
- Flow rate: Per NVIDIA CDU spec — typically 20-40 L/min per rack
- Pump: Variable speed — pressure regulated
---
### Secondary Loop (Dry Cooler)
- Location: Exterior — north wall or rooftop mount
- Type: Adiabatic dry cooler — air-cooled finned coil, optional misting for peak days
- Climate note: Lafayette avg high 93F summer — size dry cooler for 100F ambient
- Glycol loop: Runs through exterior wall penetration (insulated sleeve)
- Isolation valve: 1x ball valve per dry cooler — serviceable without rack downtime
---
## Pipe Routing Schematic — Phase 1
```plain text
Exterior wall (north)
  [Dry Cooler 1] [Dry Cooler 2] [Dry Cooler 3] [Dry Cooler 4]
       |               |               |               |
  ====[ Supply manifold — 4-inch insulated pipe along north wall ]====
       |               |               |               |
  [CDU A01-A04]  [CDU A05-A08]  [CDU B01-B04]  [CDU B05-B08]
  ====[ Return manifold — 4-inch insulated pipe along north wall ]====
       |               |               |               |
  [ Pump station — NW corner — 2x variable speed pumps, 1 redundant ]
```
---
## Key Components
- CDU units: 16x — 1 per NVL72 rack (NVIDIA-supplied or approved vendor)
- Dry coolers: 4x exterior — sized for 500 kW each (2 MW total capacity)
- Pump station: 2x variable speed pumps — N+1 redundancy
- Expansion tank: 1x — pressure relief, glycol makeup
- Flow meters: 1x per CDU loop — monitored via BMS
- Leak detection: Rope-style sensor along entire manifold run
- Isolation valves: Ball valves at each CDU inlet/outlet — hot-swap capable
---
## Wall Penetration Detail
- Penetration size: 6-inch core drill — north exterior wall
- Sleeve: Insulated pipe sleeve — vapor barrier sealed
- Fire stop: Intumescent firestop collar — maintain Type X fire rating
- Contractor: Licensed mechanical contractor — permit required
---
## Monitoring
- BMS: Building Management System — supply/return temps, flow rate, leak status
- Alerts: High temp (>62C return), low flow, leak detection — SMS + Mission Control event
- Integration: InfraManagerAgent monitors BMS via HTTP API or Modbus gateway
> SCOPE: This document applies to MARLIE I — the permanent AI Factory at 1201 SE Evangeline Thruway. NOT applicable to ADC 3K container pods, which use immersion cooling and a separate architecture.
---
## ADC 3K Container Pod Cooling — DIFFERENT ARCHITECTURE
> ADC 3K pods use immersion cooling, NOT rear-door CDU. Immersion eliminates HVAC requirements entirely — pods deploy into metal structures (e.g. Trappeys Cannery warehouse) with no air conditioning infrastructure needed. Separate engineering spec required for ADC 3K immersion loop, dielectric fluid selection, and heat rejection.
- Heat rejection: Dry cooler or liquid-to-liquid HX — same exterior rejection strategy as MARLIE I but different primary loop
- PUE target: 1.02-1.05 — immersion is more efficient than CDU at pod scale
- Advantage: No HVAC, no raised floor, no hot aisle containment — drops into any structure with power + fiber
- First deployment: Trappeys Cannery metal warehouse — immersion pods, no structural HVAC modifications required
---
## ADC 3K Pod — Immersion Cooling (Remote Deployments)
> ADC 3K pods use immersion cooling — NOT CDU/liquid cooling. CDU applies to MARLIE I (building racks). These are two separate products.
### Dielectric Fluid — Committed Specification
> COMMITTED: Engineered Fluids EC-110 (single-phase immersion). 3M Novec is DISCONTINUED — do not reference in investor materials or engineering specs.
- Fluid: Engineered Fluids EC-110 — single-phase dielectric, non-flammable, non-toxic, commercially available
- Cooling method: Single-phase immersion (servers submerged in fluid bath inside 40-ft ISO container)
- Heat rejection: Exterior dry cooler (primary) or liquid-to-liquid HX — no HVAC required at deployment site
- PUE target: 1.02–1.05 (immersion eliminates almost all cooling overhead)
- Vendor: Engineered Fluids — RFI package prepared, not yet submitted
- GPU platform: NVIDIA Vera Rubin NVL72 — TDP not yet published by NVIDIA. Final tank sizing pending TDP confirmation.
### Remote Site Power Spec (Per Pod)
- Input: 480V 3-phase, utility feed to pod junction box
- Backup: N+1 diesel generator, exterior pad mount, auto-start <15 sec
- Fiber: Site must have fiber connectivity — pod networks back to MARLIE I NOC
- Remote monitoring: MARLIE I NOC manages all deployed pods centrally — no on-site staff required at remote locations
---
> SCOPE OF THIS DOCUMENT: Cold plate CDU cooling schematics are for MARLIE I (1201 SE Evangeline Thruway ONLY). ADC 3K pods at Trappeys, KLFT, New Iberia, and all other remote sites use FULL IMMERSION (EC-110). Do NOT apply CDU schematics to ADC 3K pod deployments.
## Cooling Architecture — Two Systems, Same GPU Platform
- MARLIE I: Cold plate CDU — NVL72 racks in sealed hot aisle, CDU at each end, dry coolers exterior
- ADC 3K pods: EC-110 full immersion — NVL72 GPUs submerged in dielectric bath inside 40-ft ISO container
- Both systems: achieve PUE 1.02-1.10, zero rack-level air cooling, 100% direct liquid heat removal
- Why CDU for MARLIE I: permanent building, code compliance, public-facing, hot aisle containment standard
- Why immersion for ADC 3K: field deployment, variable ambient (Louisiana heat/humidity), no HVAC permitting
- NVL72 GPU compatibility: same hardware in both — different fluid delivery path, same thermal outcome
---
> UPDATED 2026-03-23 -- POST-GTC REWRITE
## Cooling Architecture -- Post-GTC 2026
NVIDIA now ships complete liquid-cooled NVL72 racks. 45C hot water direct-to-chip. ADC does NOT engineer custom immersion cooling. EC-110 dielectric immersion is DEPRIORITIZED.
### What ADC Builds (cooling):
- Facility water loop (supply/return piping)
- Exterior heat rejection (dry coolers or river cooling depending on site)
- CDU connections to NVIDIA rack manifolds
### Per-Site Cooling:
Willow Glen: Mississippi River (once-through, unlimited) -- 260 MW ceiling
MARLIE I: Dry coolers on concrete pad -- 1.2 MW
Trappeys: Water tower + dry coolers -- 29 MW max
ADC 3K Pod: Integrated dry cooler per container -- 130-260 kW per pod
### ADC 3K Pod Cooling:
- 40-ft container with 1-2 NVL72 racks
- Integrated dry cooler mounted on container exterior
- 45C supply / 55-60C return glycol loop
- Self-contained -- no external water infrastructure needed
- Designed for field deployment (oil fields, remote sites)
### Temperature Specs:
- GPU junction: <83C
- Coolant supply: 45C
- Coolant return: 55-60C
- Ambient operating range: -20C to 50C (dry cooler rated)
---
> CRITICAL WARNING (2026-03-24): This page has 4 CONFLICTING cooling architectures. ONLY the "POST-GTC REWRITE" section is correct. The 3 sections above it pushing EC-110 immersion are WRONG -- NVIDIA ships complete liquid-cooled racks, immersion is deprioritized. Ignore all immersion content.