# KLFT Digital Twin — Complete Data Sheet
Last updated: 2026-03-23
Purpose: All measurements needed to programmatically generate USD scene files for NVIDIA Omniverse.

---

## 1. AIRPORT IDENTITY

| Field | Value |
|-------|-------|
| Official Name | Lafayette Regional Airport / Paul Fournet Field |
| ICAO | KLFT |
| IATA | LFT |
| FAA Identifier | LFT |
| Owner | City Parish of Lafayette |
| Executive Director | Steven L. Picou |
| Activation Date | April 1940 |
| Acreage | 1,116 acres (some sources say 746 — FAA data says 1,116) |
| Address | 200 Terminal Drive, Suite 200, Lafayette, LA 70508 |

---

## 2. AIRPORT REFERENCE POINT & ELEVATION

| Field | Value |
|-------|-------|
| Latitude | 30.2050267 N (30 deg 12' 18.0960" N) |
| Longitude | 91.9877539 W (91 deg 59' 15.9140" W) |
| Elevation (surveyed) | 40.9 ft / 12.5 m MSL |
| Magnetic Variation | 03 deg East (epoch 1990) |
| Time Zone | UTC-6 (CST) / UTC-5 (CDT) |

---

## 3. RUNWAYS

### 3.1 Runway 04R/22L (PRIMARY)

| Field | Value |
|-------|-------|
| Length | 8,000 ft / 2,438 m |
| Width | 150 ft / 46 m |
| Surface | Asphalt, grooved, good condition |
| Edge Lighting | High intensity (HIRL) |
| Weight Limit (Single Wheel) | 140,000 lbs |
| Weight Limit (Double Wheel) | 170,000 lbs |
| Weight Limit (Double Tandem) | 290,000 lbs |
| Distance Remaining Signs | Yes |

**Runway 04R Threshold:**

| Field | Value |
|-------|-------|
| Latitude | 30.19593611 N (30 deg 11' 45.37" N) |
| Longitude | 91.99373333 W (91 deg 59' 37.44" W) |
| Elevation | 38.2 ft MSL |
| True Heading | 039 deg |
| Magnetic Heading | 036 deg |
| Traffic Pattern | Right |
| Landing Distance Available | 8,000 ft |
| PAPI | 4-light, 3.00 deg glide path, left side |
| EMAS | 223 ft x 170 ft |

**Runway 22L Threshold:**

| Field | Value |
|-------|-------|
| Latitude | 30.21305278 N (30 deg 12' 46.99" N) |
| Longitude | 91.97788333 W (91 deg 58' 40.38" W) |
| Elevation | 31.9 ft MSL |
| True Heading | 219 deg |
| Magnetic Heading | 216 deg |
| Traffic Pattern | Left |
| Displaced Threshold | 342 ft |
| Landing Distance Available | 7,659 ft |
| Approach Lighting | MALSR (1,400 ft medium intensity approach lighting system) |
| Instrument Approach | ILS/DME |
| PAPI | 4-light, 3.00 deg glide path, left side |
| EMAS | 380.7 ft x 170 ft |

### 3.2 Runway 11/29 (SECONDARY / CROSSWIND)

| Field | Value |
|-------|-------|
| Length | 5,403 ft / 1,647 m |
| Width | 150 ft / 46 m |
| Surface | Asphalt, grooved, good condition |
| Edge Lighting | Medium intensity (MIRL) |
| Weight Limit (Single Wheel) | 85,000 lbs |
| Weight Limit (Double Wheel) | 110,000 lbs |
| Weight Limit (Double Tandem) | 175,000 lbs |
| Distance Remaining Signs | Yes |

**Runway 11 Threshold:**

| Field | Value |
|-------|-------|
| Latitude | 30.20764722 N (30 deg 12' 27.53" N) |
| Longitude | 91.99810278 W (91 deg 59' 53.17" W) |
| Elevation | 36.5 ft MSL |
| True Heading | 110 deg |
| Magnetic Heading | 107 deg |
| Traffic Pattern | Right |
| Landing Distance Available | 5,403 ft |
| Approach | VOR/DME (non-precision) |
| PAPI | 4-light, 3.00 deg glide path, left side |
| EMAS | 300 ft x 170 ft |

**Runway 29 Threshold:**

| Field | Value |
|-------|-------|
| Latitude | 30.20256389 N (30 deg 12' 09.23" N) |
| Longitude | 91.98206389 W (91 deg 58' 55.43" W) |
| Elevation | 33.9 ft MSL |
| True Heading | 290 deg |
| Magnetic Heading | 287 deg |
| Traffic Pattern | Left |
| Displaced Threshold | 248 ft |
| Landing Distance Available | 5,155 ft |
| Approach | RNAV GPS |
| PAPI | 4-light, 3.00 deg glide path, left side |
| EMAS | 448 ft x 170 ft |

### 3.3 Runway 04L/22R (TERTIARY / GA)

| Field | Value |
|-------|-------|
| Length | 4,098 ft / 1,249 m |
| Width | 75 ft / 23 m |
| Surface | Asphalt, fair condition |
| Edge Lighting | Medium intensity (MIRL) |
| Weight Limit (Single Wheel) | 25,000 lbs |
| Weight Limit (Double Wheel) | 32,000 lbs |
| Operational Restriction | CLOSED 2230-0530 local |
| Distance Remaining Signs | Yes |

**Runway 04L Threshold:**

| Field | Value |
|-------|-------|
| Latitude | 30.20160278 N (30 deg 12' 05.77" N) |
| Longitude | 91.99251667 W (91 deg 59' 33.06" W) |
| Elevation | 40.2 ft MSL |
| True Heading | 039 deg |
| Magnetic Heading | 036 deg |
| Traffic Pattern | Left |
| PAPI | 2-light, 3.00 deg glide path, left side |

**Runway 22R Threshold:**

| Field | Value |
|-------|-------|
| Latitude | 30.21040278 N (30 deg 12' 37.45" N) |
| Longitude | 91.98440000 W (91 deg 59' 03.84" W) |
| Elevation | 40.7 ft MSL |
| True Heading | 219 deg |
| Magnetic Heading | 216 deg |
| Traffic Pattern | Right |
| PAPI | 2-light, 3.00 deg glide path, left side |

### 3.4 Computed Runway Bearings (verified via haversine)

| Runway Pair | Computed True Bearing | Published True Heading | Delta |
|-------------|-----------------------|------------------------|-------|
| 04R -> 22L | 38.67 deg | 039 deg | 0.33 deg |
| 11 -> 29 | 110.14 deg | 110 deg | 0.14 deg |
| 04L -> 22R | 38.56 deg | 039 deg | 0.44 deg |

All coordinate-derived bearings match published headings within < 0.5 deg. Data is verified.

---

## 4. TAXIWAYS

Known taxiway designations (from AirNav and SkyVector — FAA airport diagram required for full layout):

| Taxiway | Notes |
|---------|-------|
| Taxilane A | Non-movement area (no ATC clearance required) |
| Taxiway E | Connects runway complex; blind spots noted east and west of Taxiway M |
| Taxiway M | Intersects with Taxiway E; blind spot areas noted |

**Hot Spots / Safety Notes:**
- Limited ATC visibility of north parking ramp
- Blind spots east and west of Taxiway E at Taxiway M intersection
- Taxiway ramps are non-movement areas

**NOTE:** The full FAA Airport Diagram (APD) chart contains the complete taxiway network. The diagram is published by the FAA and available through SkyVector, FlightAware, and the FAA Chart Supplement. It should be obtained as a reference image for the digital twin build. Only partial taxiway data is available in text form.

---

## 5. TERMINAL BUILDING

| Field | Value |
|-------|-------|
| Name | Lafayette Regional Airport Passenger Terminal |
| Opened | January 20, 2022 |
| Size | 120,000 sq ft (11,148 sq m) |
| Gates | 5 (expandable to 7) |
| Active Gates | 4 (Delta, United, American) |
| Cost | ~$150 million (terminal + supporting infrastructure) |
| Canopy | Structural-steel, 17,603 sq ft standing seam roof with skylights |
| Address | 200 Terminal Drive, Lafayette, LA 70508 |
| Approx. GPS | 30.2065 N, 91.9870 W (estimated from satellite — east side of field) |

**Notes for 3D modeling:**
- Terminal is on the EAST side of the airfield, between Runway 04R/22L and Runway 04L/22R
- Modern design (2022), steel-and-glass construction
- Distinctive curved canopy entrance structure
- Rental car quick-turnaround facility adjacent

---

## 6. CONTROL TOWER

| Field | Value |
|-------|-------|
| Staffed | Continuous (0530-2230 active control; after hours CTAF) |
| CTAF Frequency | 118.5 MHz |
| Tower Frequency | 118.5 / 257.8 MHz |
| Ground Frequency | 121.8 MHz |
| Approx. GPS | 30.2058 N, 91.9885 W (estimated — west of terminal, near ramp) |

**Notes:** Tower location should be confirmed from satellite imagery. It is typically positioned to have line-of-sight to all runway intersections and the primary ramp area.

---

## 7. FBO & GENERAL AVIATION FACILITIES

### 7.1 Signature Aviation (Primary FBO)

| Field | Value |
|-------|-------|
| Address | 123 Grissom Drive, Lafayette, LA 70508 |
| Phone | 337-234-3100 |
| Email | LFT@signatureaviation.com |
| Hours | 24/7 |
| Fuel | 100LL ($7.75 full/$4.65 self), Jet A ($9.17 full) |
| Services | Hangars, GPU/power cart, oxygen, parking, pilot lounge, crew cars, flight training |
| Approx. GPS | 30.208 N, 91.990 W (estimated — north side of field) |

### 7.2 Other GA Operators

| Name | Address |
|------|---------|
| Lafayette Aircraft Services | 125 Shepard Drive |
| Castille Aviation | 203 Shepard Drive |
| Metro Gulf (maintenance) | On-field |

---

## 8. COMMUNICATIONS & NAVIGATION

### 8.1 Radio Frequencies

| Service | Frequency (MHz) | Hours |
|---------|-----------------|-------|
| ATIS / ASOS | 134.05 | Continuous |
| CTAF | 118.5 | — |
| Tower | 118.5 / 257.8 | 0530-2230 |
| Ground | 121.8 | 0530-2230 |
| Clearance Delivery | 125.55 | — |
| Approach (020-210 deg) | 121.1 / 363.0 | 0530-2230 |
| Approach (211-019 deg) | 128.7 / 268.7 | 0530-2230 |
| UNICOM | 122.95 | — |
| Emergency | 121.5 / 243.0 | — |

### 8.2 ASOS

| Field | Value |
|-------|-------|
| Frequency | 134.05 MHz |
| Phone | 337-262-2757 |
| Location | On-field (exact position TBD from diagram) |

### 8.3 Navigation Aids

| Name | Type | Frequency | Distance |
|------|------|-----------|----------|
| LAFAYETTE | VORTAC | 109.80 MHz | On-field (0.7 nm) |
| LAFFS (LF) | NDB | 375 kHz | 6.5 nm, 216 deg |
| ABBEVILLE (BNZ) | NDB | 230 kHz | 11.1 nm, 037 deg |
| WHITE LAKE | VOR/DME | 114.95 MHz | 38.2 nm, r028 |
| FIGHTING TIGER | VORTAC | 116.50 MHz | 39.7 nm, r239 |

---

## 9. AIRSPACE

| Field | Value |
|-------|-------|
| Airspace Class | C |
| ARTCC | Houston Center (ZHU) |
| FSS | De Ridder Flight Service Station |
| Traffic Pattern Altitude | 1,041 ft MSL (1,000 ft AGL) |
| Beacon | White-green (lighted land airport), sunset to sunrise |

### Class C Dimensions (standard, verify on current sectional)

| Ring | Radius | Floor | Ceiling |
|------|--------|-------|---------|
| Inner (surface area) | 5 nm from airport | Surface | 4,000 ft AGL (~4,041 ft MSL) |
| Outer shelf | 10 nm from airport | 1,200 ft AGL (~1,241 ft MSL) | 4,000 ft AGL (~4,041 ft MSL) |

**NOTE:** Lafayette's Class C was amended per Federal Register 2019-20689 (Sept 25, 2019). Exact sector boundaries may deviate from standard. Verify against current VFR sectional chart.

---

## 10. OPERATIONS & SAFETY

| Field | Value |
|-------|-------|
| ARFF Index | B |
| Customs | Yes (landing rights) |
| Segmented Circle | Yes |
| Wind Indicator | Lighted |
| Wildlife Hazard | Migratory birds on/in vicinity |
| International | Customs landing rights airport |
| Prior Permission Required | Unscheduled aircraft ops with 30+ passenger seats |

### EMAS (Engineered Materials Arresting Systems)

| Runway End | EMAS Dimensions |
|------------|-----------------|
| Runway 04R | 223 ft x 170 ft |
| Runway 11 | 300 ft x 170 ft |
| Runway 22L | 380.7 ft x 170 ft |
| Runway 29 | 448 ft x 170 ft |

### Obstructions

| Type | Details |
|------|---------|
| Oil rig | 155 ft AGL, 1 nm SE of field |
| Trees/poles | Documented per runway approach (see Chart Supplement) |

---

## 11. SURROUNDING ROADS

| Road | Relation to Airport |
|------|---------------------|
| US Highway 90 | Adjacent, east side of airport. Primary east-west corridor. |
| NW Evangeline Thruway (US-167) | Major north-south access route from I-10 |
| Surrey Street | Final approach road to terminal |
| I-10 | ~3 miles north of airport |
| I-49 | Merges into NW Evangeline Thruway south of I-10 |

---

## 12. ADC PROPERTY PROXIMITY

### MARLIE I (30.21975 N, 92.00645 W)

| Field | Value |
|-------|-------|
| Distance | 2,431 m / 7,974 ft / 1.51 mi / 1.31 nm |
| Bearing from airport | 312.3 deg true (NW) |
| Within Class C surface area | YES (inside 5 nm ring) |
| Drone flight time (est.) | ~3 min at 30 mph |

### Trappeys Cannery (30.21356 N, 92.00163 W)

| Field | Value |
|-------|-------|
| Distance | 1,637 m / 5,369 ft / 1.02 mi / 0.88 nm |
| Bearing from airport | 305.4 deg true (NW) |
| Within Class C surface area | YES (inside 5 nm ring) |
| Drone flight time (est.) | ~2 min at 30 mph |

**Both properties are INSIDE Class C surface area.** All drone operations require LAANC authorization or Part 107 waiver. This is a feature, not a bug — proximity to the airport is what makes KLFT the SkyCommand hub.

---

## 13. DRONE INFRASTRUCTURE ZONES (SkyCommand Planning)

### 13.1 Recommended Drone Dock Locations

| Zone | Location | Rationale |
|------|----------|-----------|
| Dock Alpha | Near GA hangars / Signature FBO (north side) | Protected area, power/data available, away from primary runway |
| Dock Bravo | MARLIE I rooftop or pad | Edge compute co-located, 1.31 nm from field |
| Dock Charlie | Trappeys campus (infrastructure yard) | 0.88 nm from field, solar power, concrete pad |
| Dock Delta | Near Runway 04L/22R midfield | GA runway side, shorter taxi/flight distances |

### 13.2 BVLOS Corridor Concepts

| Corridor | Route | Distance | Notes |
|----------|-------|----------|-------|
| KLFT -> MARLIE I | 312 deg true, 1.31 nm | Low altitude (200-400 ft AGL), Class C auth required |
| KLFT -> Trappeys | 305 deg true, 0.88 nm | Short hop, within visual range of tower |
| KLFT -> Pipeline corridor (south) | 180 deg true | Pipeline inspection runs toward Vermilion Parish |
| KLFT -> I-10 corridor (north) | ~000 deg true, 3 nm | Infrastructure inspection, exits Class C surface at ~5 nm |

### 13.3 Restricted Zones (No Drone Ops)

| Zone | Description |
|------|-------------|
| Runway Protection Zones | Extended centerline 04R/22L, 11/29, 04L/22R — 1,000 ft beyond threshold, 500 ft wide expanding to 1,010 ft |
| ILS Critical Area | Runway 22L approach path (MALSR extends 1,400 ft) |
| Active runway surfaces | All 3 runways + taxiways during operations |
| Terminal ramp | Active apron area |

### 13.4 Airspace Integration Notes

- Class C = two-way radio communication required for manned aircraft
- LAANC provides near-real-time Part 107 authorization for sUAS
- BVLOS operations require separate FAA waiver (Part 107.31)
- DAA (Detect and Avoid) sensors required for BVLOS — Phase 3 of KLFT 1.1 roadmap
- ADS-B Out may be required for drone operations above 400 ft AGL in Class C

---

## 14. 3D MODEL / CAD RESOURCES

### Available Reference Sources

| Source | Type | Access |
|--------|------|--------|
| FAA Airport Diagram (APD) | 2D chart (taxiways, buildings, runways) | Free — SkyVector, FlightAware, FAA Chart Supplement |
| OpenNav KLFT diagram | SVG | https://opennav.com/diagrams/KLFT.svg |
| Google Earth / Maps satellite | Aerial imagery | Free — 30.2050 N, 91.9877 W |
| FAA Airport Layout Plan (ALP) | Engineering drawing | Contact airport (337-703-4800) — may be public record |
| NAIP aerial photography | Ortho imagery | USDA — high-res, free |

### No Known Existing 3D Models

No publicly available 3D models, CAD files (.dwg/.dxf), or USD scenes of KLFT were found. The digital twin will need to be built from scratch using the data in this document plus satellite/aerial reference imagery.

---

## 15. SCENE CONSTRUCTION REFERENCE (for USD generation)

### Coordinate System

For Omniverse USD, use a local coordinate system with the Airport Reference Point as origin:
- Origin: 30.2050267 N, 91.9877539 W
- X axis: East (positive)
- Y axis: Up
- Z axis: South (positive) — or North (positive) per Omniverse convention
- Scale: 1 unit = 1 meter

### Key Dimensions Summary (meters)

| Element | Length (m) | Width (m) | Heading (deg true) |
|---------|-----------|-----------|---------------------|
| Runway 04R/22L | 2,438 | 46 | 039 / 219 |
| Runway 11/29 | 1,647 | 46 | 110 / 290 |
| Runway 04L/22R | 1,249 | 23 | 039 / 219 |
| Terminal building | ~180 (est.) | ~65 (est.) | ~039 (parallel to primary runway) |
| EMAS 04R | 68 x 52 | — | — |
| EMAS 11 | 91 x 52 | — | — |
| EMAS 22L | 116 x 52 | — | — |
| EMAS 29 | 137 x 52 | — | — |

### Runway Threshold Offsets from Origin (meters, approximate)

Using airport reference point as (0, 0):

| Threshold | X (East) | Z (North) | Elevation offset (m) |
|-----------|----------|-----------|---------------------|
| 04R | -558 | -1,034 | -0.8 |
| 22L | +932 | +878 | -2.7 |
| 11 | -877 | +289 | -1.3 |
| 29 | +627 | -272 | -2.1 |
| 04L | -400 | -378 | -0.2 |
| 22R | +361 | +554 | -0.1 |

**NOTE:** These offsets are computed from the decimal degree coordinates. They should be verified against the FAA APD chart before final scene construction. Use WGS84 projection for conversion.

---

## 16. DATA GAPS — TO RESOLVE

| Gap | Resolution Path |
|-----|-----------------|
| Full taxiway network (all designations, widths, intersections) | Obtain FAA Airport Diagram (APD) — trace from chart |
| Terminal building exact footprint dimensions | Satellite imagery measurement or contact airport |
| Control tower exact coordinates and height | Satellite imagery or FAA obstruction data |
| Hangar locations and dimensions | Satellite imagery or airport property records |
| Parking lot layout | Satellite imagery |
| VORTAC antenna exact location | Chart Supplement or satellite imagery |
| Class C exact sector boundaries | Current VFR sectional chart |
| Runway markings (precision, non-precision, basic) | FAA APD chart |
| Taxiway widths | FAA design standards (TDG-based) or ALP |

---

## Sources

- AirNav: https://www.airnav.com/airport/KLFT
- SkyVector: https://skyvector.com/airport/LFT
- OurAirports: https://ourairports.com/airports/KLFT/runways.html
- iFlightPlanner: https://www.iflightplanner.com/Airports/KLFT
- OpenNav: https://opennav.com/airport/KLFT
- Airport Improvement Magazine (terminal): https://airportimprovement.com/article/new-terminal-lafayette-regional-was-true-community-effort
- LFT Airport official: https://lftairport.com/
- Federal Register Class C amendment: https://www.federalregister.gov/documents/2019/09/25/2019-20689/amendment-of-class-c-airspace-lafayette-la
- FAA LAANC: https://www.faa.gov/uas/programs_partnerships/data_exchange/laanc_facilities
