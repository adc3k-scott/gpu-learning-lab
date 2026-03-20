# Iberville Parish Permitting — Willow Glen Terminal

## Site Context
- **Location:** Willow Glen Terminal, 2605 LA-75, St. Gabriel, Iberville Parish, LA 70776
- **Zoning:** M2 Heavy Industrial (confirmed — no variance needed)
- **Prior use:** Former 2,200 MW Entergy power station (gas/oil, built 1960, retired 2016)
- **Developable acreage:** 400+ acres (not 50 — the 50-acre figure was the FTZ subzone application area)
- **Existing infrastructure:** 230kV substation, water intake, switchyard, transmission, dock (Mississippi River)
- **Foreign Trade Zone 154D:** Approved September 18, 2024. Duty deferral on imported equipment (GPU servers, networking, cooling hardware).
- **ADC is licensed GC** — can pull own permits
- **IMPORTANT:** Building permits go through **City of St. Gabriel** (not Iberville Parish) — site is within city limits

---

## Phase 1 Permitting Timeline (20,000 SF Warehouse Conversion)

### Critical Path Sequence

| Permit | Authority | Lead Time | Notes |
|--------|-----------|-----------|-------|
| **PILOT / Tax Incentive** | Iberville Parish IDB / LED | Parallel | **File before construction** (see itep-filing.md) |
| Zoning verification (M2) | St. Gabriel P&Z | 1-2 weeks | Should be straightforward |
| Building permit (plan review) | St. Gabriel | 2-4 weeks | Plans need LA-licensed architect/PE stamp |
| **Fire Marshal plan review** | LA State Fire Marshal (OSFM) | 4-8 weeks | Required before building permit issued |
| Electrical Installation | Parish Building | 2-4 weeks | Part of building permit |
| LPDES Water Discharge | LDEQ | 2-4 months | Parallel; 6 months if public notice |
| Army Corps Section 404 | Corps, New Orleans | 2-3 months | Only if new river intake |
| On-Site Generation Interconnect | Entergy / LPSC | 4-8 weeks | Parallel |
| **Air Quality (ATC)** | LDEQ | **3-6 months** | **CRITICAL PATH** — minor source. If PSD (major source): 12-18 months |
| Construction Stormwater | LDEQ | Immediate | Self-implementing, submit NOI with SWPPP |
| Industrial Stormwater (MSGP) | LDEQ | 30 days | After NOI receipt |
| Fire / Life Safety | LA State Fire Marshal | 2-4 weeks | Final inspection before occupancy |
| Phase I ESA | Environmental Consultant | 2-4 weeks | Recommended; $3-8K |

**Water discharge:** If closed-loop cooling (recommended), NO LPDES permit needed. Only if discharging to surface water.

### Realistic Timeline
- **Optimistic (minor source air):** 6-9 months
- **Conservative:** 9-12 months
- **If PSD triggered (major source):** 18+ months
- **Critical path driver:** LDEQ air quality ATC (not ITEP — that's a tax incentive, file in parallel)

### Month-by-Month (Optimistic — Minor Source)
| Month | Action |
|-------|--------|
| 0 | File PILOT/tax incentive + air quality ATC application + Phase I ESA |
| 1-2 | Building permit + fire marshal plan review + zoning verification |
| 2-4 | Air quality ATC processing (parallel) |
| 3-4 | Entergy interconnection agreement |
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

1. **Foreign Trade Zone 154D** — already approved (Sept 2024). Duty deferral on imported GPU servers, networking, cooling hardware.
2. **M2 zoning** — no variance needed, industrial AI compute is compatible
3. **230kV substation on-site** — eliminates what would otherwise be the longest lead item (utility infrastructure, typically 3-5 years)
4. **400+ developable acres** — massive campus expansion potential
5. **Existing permits may transfer** — old LPDES, air quality, Corps permits can be modified vs. new
6. **Brownfield accelerator** — EO 14318 prioritizes data center redevelopment on former power sites
7. **No wetland impact (Phase 1)** — warehouse conversion is on existing developed footprint
8. **Closed-loop cooling = no LPDES** — if no discharge to surface water, skip water discharge permit entirely
9. **ADC is licensed GC** — pull own permits, no contractor delays
10. **Lightning Amendment (Dec 2025)** — LPSC fast-track for utility-built power plants serving AI facilities (8 months vs 2 years)

---

## Key Contacts

| Entity | Contact | Phone |
|--------|---------|-------|
| **St. Gabriel City Hall (permits, zoning)** | 5035 Iberville St, St. Gabriel 70776 | **(225) 642-9600** |
| Iberville Parish Permits (outside city limits) | 58030 Meriam St, Plaquemine 70764 | (225) 687-5150 |
| LA State Fire Marshal (OSFM) | 8181 Independence Blvd, Baton Rouge | (800) 256-5452 |
| LDEQ Air Permits | deq.louisiana.gov/air | (225) 219-3417 |
| LDEQ Water Permits | DEQ-WWWWaterPermits@la.gov | (225) 219-9371 |
| Corps of Engineers (NOLA) | mvn.usace.army.mil | (504) 862-1001 |
| LED / PILOT / Incentives | opportunitylouisiana.gov | FastLane NextGen portal |
| Entergy Louisiana | entergylouisiana.com | |
| LPSC | lpsc.louisiana.gov | |

---

## Immediate Action Items

1. **File PILOT application** — contact Iberville Parish IDB before construction (see itep-filing.md)
2. **Start LDEQ air quality ATC** — this is the critical path permit (3-6 months for minor source)
3. **Get permit history from WGT/Entergy** — old LPDES, air, electrical permits for modification baseline
4. **Phase I ESA** — contract environmental firm ($3-8K, 2-3 week turnaround)
5. **Entergy meeting** — interconnection requirements for on-site generation
6. **Fire Marshal pre-check** — consult OSFM on GPU liquid cooling + battery fire suppression design
7. **Building permit pre-application** — submit to **St. Gabriel** (not Iberville Parish) to confirm M2 compatibility
