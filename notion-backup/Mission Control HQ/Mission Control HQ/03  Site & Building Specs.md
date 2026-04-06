# 03 — Site & Building Specs
*Notion backup — 2026-04-06*

> Scott Tomsu designed and built this building himself, 20 years ago. Multiple direct Gulf hurricane impacts — zero structural damage.
---
## Address
1201 SE Evangeline Thruway, Lafayette, LA 70501 — ADC3K HQ
---
## Building Dimensions
- Exterior footprint: 24 ft x 40 ft
- Downstairs (compute): 24 ft wide x 37 ft usable — staircase takes 3 ft
- Upstairs (NOC): full second floor — operations center, no compute racks
- Adjacent Chag Street: 3 parcels, ~0.60 acres — owned, targeted for pod deployment
---
## Ceiling & Structure
- Plate height: 7 ft 11 in to bottom of ceiling assembly (measured)
- Framing: 2x12
- Ceiling assembly: two layers 5/8 Type X sheetrock + insulation + full floor above
- Fire rating: UL-rated assembly — built-in from day one
- Insulation: heavy throughout — complete thermal shell — optimal for liquid cooling stability
- Foundation: reinforced concrete slab
---
## Downstairs Layout — Single Row, 10 NVL72 Racks
> Same design as ADC 3K pod. 10 racks in a single row along the 37 ft length. 24 ft width gives full cold aisle + CDU space — no second row needed.
- Single row of 10 NVL72 racks running 37 ft length
- 24 ft width: cold aisle on front face, hot aisle + CDU equipment space at rear
- CDU pair at row ends — liquid heat rejection to exterior dry coolers on concrete pad
- Network core / fiber MDA / CDU controls — compact zone near entry
- ALL mechanical exterior: dry coolers, UPS batteries, Bloom units, security, fuel systems
The extra width vs a container (24 ft vs ~8 ft interior) provides full maintenance access and CDU equipment space without requiring a second rack row. Building and pods share the same thermal architecture and power design — different enclosures, same playbook.
---
## Upstairs — NOC
- Mission Control operations center
- Network monitoring, telemetry, command ops
- Backup NOC for Willow Glen (60 mi, dedicated fiber, management traffic only)
- No compute racks — no IT load
---
## Site Specs
- FEMA Zone: Zone X — Minimal Flood Hazard
- Ground elevation: high ground — above regional base flood elevation
- Zoning: Industrial — heavy use permitted
- Property debt: $15,000 total
- Storm history: multiple direct hurricanes — zero structural damage
- GC Permits: Louisiana GC License — active
- NVIDIA Certs: 7 active certifications
- FAA Certs: Private Pilot + Part 107 UAS
---
## Infrastructure Proximity
- LUS Fiber: ~0.8 mi — 214 Jefferson St
- LUS Power / Utilities: ~1 mi — 1314 Walker Rd
- Atmos Energy: ~3 mi — 1818 Eraste Landry Rd
- SLEMCO Electric: 2727 SE Evangeline Thruway
- LFT Airport: adjacent — GPS 30.20529, -91.98760
- Henry Hub: ~40 mi — Erath, LA
- NVIDIA TX Manufacturing: ~4 hrs — Foxconn Houston / Wistron Fort Worth
- Trappeys Cannery: 0.5 mi
- Willow Glen: 60 mi — dedicated fiber (management traffic only, NOT InfiniBand)
---
## Cooling Architecture — Building
- NVIDIA integrated cold plate CDU — direct-to-chip liquid cooling
- 45C hot water output — liquid heat rejection to exterior dry coolers on concrete pad
- 1 CDU pair — covers 10-rack single row
- PUE target: 1.10
- No CRAC units, no chiller plant, no raised floor
---
## Adjacent Parcels — Chag Street
- 3 adjacent parcels, approx 0.60 acres total
- 3 blighted structures targeted for Phase 1 demolition
- Ground-mount First Solar TR1 panels + exterior cooling infrastructure on cleared parcels
- Pod deployment zone: 3 ADC 3K pods side by side adjacent to building
---
## GPS & References
- GPS: 30.21975N, 92.00645W
- Land debt: $5,000. Effectively debt-free.
- Role: Backup NOC for Willow Glen, edge compute, R&D staging, Scott HQ
- Half mile from Trappeys. 60 miles from Willow Glen.
- Blueprints: 6-sheet set at adc3k.com/blueprints-marlie
- Sheets: E-001 (electrical SLD), C-001 (cooling), S-001 (site plan), A-001 (floor plan), P-001 (power dist), L-001 (solar layout)