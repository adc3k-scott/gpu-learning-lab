# Iberville Parish Permitting — Willow Glen Terminal

## Site Context
- **Location:** Willow Glen Terminal, St. Gabriel, Iberville Parish, LA
- **Zoning:** M2 Heavy Industrial (confirmed — no variance needed)
- **Prior use:** Former 2,200 MW Entergy power station
- **Existing infrastructure:** 230kV substation, water intake, switchyard, transmission
- **ADC is licensed GC** — can pull own permits

---

## Phase 1 Permitting Timeline (20,000 SF Warehouse Conversion)

### Critical Path Sequence

| Permit | Authority | Lead Time | Notes |
|--------|-----------|-----------|-------|
| **ITEP Application** | LED / BC&I | 4-6 months | **FIRST — before any construction** |
| Building / Use Change | Iberville Parish | 4-12 weeks | Parallel with ITEP |
| Planning Commission | Iberville Parish | 4-6 weeks | Parallel with building permit |
| Electrical Installation | Parish Building | 2-4 weeks | Part of building permit |
| LPDES Water Discharge | LDEQ | 2-4 months | Parallel; 6 months if public notice |
| Army Corps Section 404 | Corps, New Orleans | 2-3 months | Only if new river intake |
| On-Site Generation Interconnect | Entergy / LPSC | 4-8 weeks | Parallel |
| Air Quality | LDEQ | 2-4 months | Minor permit likely |
| Fire / Life Safety | Iberville Fire Marshal | 2-4 weeks | Final inspection before occupancy |
| Phase I ESA | Environmental Consultant | 2-4 weeks | Recommended; may be LDEQ requirement |

### Realistic Timeline
- **Optimistic:** 5-6 months
- **Conservative:** 8-10 months
- **Critical path driver:** ITEP filing (must be first)

### Month-by-Month (Optimistic)
| Month | Action |
|-------|--------|
| 0 | ITEP application filed |
| 1-2 | Building permit + planning commission approval |
| 2-4 | LPDES + air quality permits (parallel) |
| 3-4 | Corps Section 404 (if river intake) + interconnection |
| 4-5 | Electrical + fire safety final inspection |
| 5-6 | ITEP contract execution + groundbreaking authorized |

---

## Permit Details

### 1. Local — Iberville Parish

**Building Permit & Change of Use**
- Authority: Iberville Parish Permits & Inspections, (225) 687-5150
- Application: Online only (mandatory user account)
- Required: Change of Occupancy notice (warehouse → AI compute), site plans, GPU rack layout, cooling systems, electrical runs
- M2 zoning = no variance needed for industrial AI compute

**Planning Commission Review**
- 30-45 days for public notice + comment
- M2 industrial use presumed compatible with former power station — expedited approval likely

### 2. State Environmental — LDEQ

**Water Discharge (LPDES)**
- Authority: LDEQ Water Permits Division, (225) 219-9371
- Forms: Permit Application to Discharge Wastewater from Industrial Facilities
- Covers: Cooling water discharge volume/temperature, treatment systems, outfall location
- Monthly Discharge Monitoring Reports (DMRs) via NetDMR
- Mississippi River Basin surcharge: 20% of permit fee (max $150 additional)
- **If reusing old power plant intake: modification vs new application (much faster)**

**Air Quality**
- Exemption threshold: <5 TPY any single pollutant, <15 TPY all combined
- If exempt: Self-certifying, no permit needed
- If over: Minor Source General Permit (2-4 months) or Major Source Title V (6-12 months)
- **Important:** Multiple gensets may cross exemption threshold — evaluate combined emission profile

### 3. Federal — Army Corps of Engineers

**Section 404 / Section 10 (Rivers & Harbors)**
- Authority: Corps of Engineers, New Orleans District
- Triggered by: Water intake structure from Mississippi River
- Timeline: 2-3 months + 30-day public comment
- **Key advantage:** Former power station = existing permitted infrastructure may already exist. Reuse = modification, not new permit.

### 4. Electrical & Power

**High-Voltage Installation**
- Louisiana Electrical Code 2020 (NFPA 70-2020)
- Electrical contractor license needed for >$50K installation
- Reviewed as part of building permit

**On-Site Generation Interconnection**
- Solar: Net metering available for ≤300 kW commercial
- Natural gas: NOT eligible for net metering (separate utility agreement required)
- LPSC filing may be required if >10 MW
- Timeline: 4-8 weeks

### 5. Fire & Life Safety

**GPU Liquid Cooling + Battery Storage**
- NFPA 855 (Stationary Energy Storage Systems)
- 2-hour fire-rated barrier required for battery storage
- Expanded sprinkler density per 2024 IFC
- Continuous gas detection for thermal runaway
- 45°C hot water loops + lithium batteries = dual-risk assessment
- No Louisiana-specific liquid cooling standard — performance-based design approval via local AHJ
- Timeline: 2-4 weeks

### 6. Environmental Assessment

**Phase I ESA (Recommended)**
- Former power station may have historical contamination
- Phase I ESA: 2-4 weeks, $3K-$8K
- Phase II ESA (if Phase I flags issues): 4-8 weeks, $10K-$50K
- Federal EO 14318 (2025) prioritizes brownfield data center redevelopment with expedited review

---

## Strategic Advantages

1. **Brownfield accelerator** — EO 14318 prioritizes data center redevelopment on former power sites
2. **M2 zoning** — no variance needed, industrial AI compute is compatible
3. **Existing permits may transfer** — old LPDES, air quality, Corps permits can be modified vs. new
4. **No wetland impact (Phase 1)** — warehouse conversion is on existing developed footprint
5. **ITEP timing** — 2025 rules favor data center/AI facilities under Governor Landry
6. **ADC is licensed GC** — pull own permits, no contractor delays

---

## Key Contacts

| Entity | Contact | Phone |
|--------|---------|-------|
| Iberville Parish Permits | Online portal | (225) 687-5150 |
| LDEQ Water Permits | DEQ-WWWWaterPermits@la.gov | (225) 219-9371 |
| LDEQ Air Permits | deq.louisiana.gov/air | |
| Corps of Engineers (NOLA) | mvn.usace.army.mil | (504) 862-1001 |
| LED / ITEP | opportunitylouisiana.gov | FastLane NextGen portal |
| Entergy Louisiana | entergylouisiana.com | |
| LPSC | lpsc.louisiana.gov | |

---

## Immediate Action Items

1. **File ITEP** — before lease signed or construction starts (FastLane NextGen portal)
2. **Get permit history from WGT/Entergy** — old LPDES, air, electrical permits for modification baseline
3. **Phase I ESA** — contract environmental firm ($3-8K, 2-3 week turnaround)
4. **Entergy meeting** — interconnection requirements for on-site generation
5. **Fire Marshal pre-check** — consult on GPU liquid cooling + battery fire suppression design
6. **Building permit pre-application** — submit preliminary site/cooling plan to confirm M2 compatibility
