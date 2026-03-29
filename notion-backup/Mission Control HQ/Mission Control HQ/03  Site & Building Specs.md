# 03 — Site & Building Specs
*Notion backup — 2026-03-28*

> Scott Tomsu designed and built this building himself, 20 years ago. Multiple direct Gulf hurricane impacts — zero structural damage.
---
## Address
1201 SE Evangeline Thruway, Lafayette, LA 70501 — ADC3K HQ
---
## Building Dimensions
- Exterior footprint: 24 ft x 40 ft
- Interior Phase 1 floor: 22 ft x 35 ft — 770 sq ft
- Second floor: available — Phase 2 vertical expansion
- Adjacent property: owned — Phase 3 horizontal expansion
---
## Ceiling & Structure
- Plate height: 7 ft 11 in to bottom of ceiling assembly (measured)
- Framing: 2x12
- Ceiling assembly: two layers 5/8" Type X sheetrock + insulation + full floor above
- Fire rating: UL-rated assembly — built-in from day one
- Insulation: heavy throughout — complete thermal shell — optimal for liquid cooling stability
- Foundation: reinforced concrete slab
---
## Phase 1 Floor Plan — Rack Layout (Concept)
- Configuration: hot aisle / cold aisle containment
- Row A: 8x NVL72 racks
- Sealed hot aisle: CDU units at each end — liquid heat rejection to exterior dry coolers
- Row B: 8x NVL72 racks
- Cold supply plenums above and below rack rows
- Network core / fiber MDA / CDU control — compact zone near entry
- ALL mechanical exterior: gas generators, dry coolers, UPS batteries, security monitoring
- Max Phase 1 capacity: 16 NVL72 racks = 57.6 ExaFLOPS
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
---
## Cooling Architecture — Cold Plate CDU (Marlie I Only)
> IMPORTANT DISTINCTION: Marlie I uses COLD PLATE CDU cooling. ADC 3K pods use FULL IMMERSION cooling (EC-110). These are different products with different cooling strategies.
- Marlie I: Cold plate CDU — direct-to-chip liquid, fans for air handling in sealed hot aisle
- CDU units at each end of hot aisle — liquid heat rejection to exterior dry coolers
- Code-compliant building installation — hot aisle/cold aisle containment, PUE 1.10
- ADC 3K pods (remote sites): full immersion in Engineered Fluids EC-110 — no fans, no HVAC, zero outdoor air
- Why the distinction matters: Marlie I is a building (CDU optimized for permanent structure + compliance)
- ADC 3K is a manufactured pod (immersion optimized for Louisiana heat/humidity + no HVAC permitting)
- NVL72 rack spec: '100% liquid cooled' = all heat removed by liquid, no rack-level air cooling — compatible with CDU
The NVL72 rack is designed for direct liquid cooling at the chip level. Marlie I's cold plate CDU delivers this. ADC 3K's immersion tank delivers this via a different fluid path. Both achieve the 1.10 PUE target. Different enclosures, same thermal outcome.
---
> CORRECTED 2026-03-23: Rack layout updated. Building is 24x40 ft, 2 floors, both active. 8 NVL72 racks total (not 16). Old 16-rack / single-floor layout above is superseded.
## Corrected Layout (2026-03-23)
- Building footprint: 24 ft x 40 ft, 2 floors = 1,920 sq ft total
- Staircase takes approx 3 ft width = 24 x 37 usable per floor = approx 888 sq ft/floor
- Same footprint as a 40-ft shipping container
- Downstairs (System 1): 4 NVL72 racks, 288 GPUs, 520 kW
- Upstairs (System 2): 4 NVL72 racks, 288 GPUs, 520 kW
- Total: 8 NVL72 racks, 576 GPUs, 1,040 kW IT load
- 1 CDU pair per floor, exterior dry coolers on concrete pad
- Both floors active from initial deployment. No Phase 2 vertical expansion needed.
## Adjacent Parcels
- 3 adjacent parcels on Chag Street, approx 0.60 acres total
- 3 blighted structures targeted for Phase 1 demolition
- Ground-mount solar + additional cooling infrastructure on cleared parcels
## GPS & References
- GPS: 30.21975N, 92.00645W
- Land debt: 5,000. Effectively debt-free.
- Role: Backup NOC for Willow Glen, edge compute, R&D/staging, Scott HQ
- Half mile from Trappeys, 60 miles from Willow Glen
- Blueprints: 6-sheet set COMPLETE at adc3k.com/blueprints-marlie
- Sheets: E-001 (electrical SLD), C-001 (cooling), S-001 (site plan), A-001 (floor plan), P-001 (power dist), L-001 (solar layout)
## Cooling (Corrected)
- CDU liquid cooling, NVIDIA integrated, 45C hot water
- Exterior dry coolers on concrete pad
- NO water tower. NO river cooling.
- 1 CDU pair per floor