# Mississippi River Hydrokinetic Energy — Willow Glen Terminal

## Site Parameters
- **Location**: Willow Glen Terminal, St. Gabriel, LA (30.24700N, 91.09850W)
- **River frontage**: 3,500 ft with 43-ft deepwater dock
- **River current**: ~2-4 fps (1.5-3 mph / 0.7-1.3 m/s) at this location
  - Mid-channel: likely 3-5 fps during normal flow
  - Near-bank: slower (1-2 fps)
  - Flood stage: can exceed 6 fps
  - Low water (drought): can drop below 2 fps (killed Free Flow Power's project in 2012)
- **USGS gauge**: Mississippi River at Baton Rouge (07374000) — closest monitoring station
- **Army Corps velocity data**: mvn.usace.army.mil/Missions/Engineering/Stage-and-Hydrologic-Data/RiverVelocityBatonRouge/
- **Measured velocity** (March 2026, Belle Chasse): 4.19 fps mean

---

## POWER DENSITY CALCULATION

### Physics
Power = 0.5 x rho x A x V^3 x Cp
- rho (water density) = 1000 kg/m3
- A = swept area of turbine (m2)
- V = water velocity (m/s)
- Cp = power coefficient (max 0.59 Betz limit, practical ~0.25-0.35)

### Power Density at Mississippi River Velocities

| Velocity | fps | m/s | Power Density (W/m2) | With Cp=0.30 |
|----------|-----|-----|---------------------|--------------|
| Low water | 2.0 | 0.61 | 113 | 34 W/m2 |
| Low normal | 3.0 | 0.91 | 380 | 114 W/m2 |
| Average | 4.0 | 1.22 | 907 | 272 W/m2 |
| High normal | 5.0 | 1.52 | 1,764 | 529 W/m2 |
| Flood | 6.0 | 1.83 | 3,065 | 920 W/m2 |

**Key insight**: Power scales with CUBE of velocity. A 2x increase in current speed = 8x more power. This is why velocity matters enormously.

### Rough Estimate for 3,500 ft Frontage

Assumptions:
- Use 1,000 ft of frontage for turbine array (leaving 2,500 ft for navigation/dock ops)
- 1,000 ft = 305 meters
- Turbines spaced 3D apart (D = 5m diameter turbines, so 15m spacing)
- ~20 turbines in a single row
- Each turbine: 5m diameter = 19.6 m2 swept area
- Average velocity: 1.2 m/s (4 fps)

**Per turbine**: 0.5 x 1000 x 19.6 x 1.2^3 x 0.30 = **5.1 kW**
**20 turbines**: **~100 kW**
**Multiple rows** (3 rows, 10D longitudinal spacing): **~250-300 kW**

### Honest Assessment
At typical Mississippi River velocities near St. Gabriel (2-4 fps average), **a realistic hydrokinetic installation produces 100-500 kW** — useful but NOT a game-changer for a 40-45 MW facility. This is supplemental power, not baseload.

If the river runs faster (5+ fps sustained), numbers improve dramatically. But drought conditions can drop it to near-zero output.

---

## HYDROKINETIC TURBINE COMPANIES

### ORPC (Ocean Renewable Power Company) — Portland, ME — **TOP PICK**
- **AMERICAN COMPANY**
- Only US company to deliver hydrokinetic power to a utility grid
- **RivGen Power System**: 25-35 kW per unit at 2 m/s (6.75 fps)
- **Modular RivGen**: 7 kW current, targeting 18 kW per device
- **CRITICAL**: Signed contract with Shell to deploy on LOWER MISSISSIPPI RIVER in Louisiana (2024)
  - LSU partnership for site assessment
  - Assessed three Shell sites in Louisiana
  - This is literally the same river, same region as Willow Glen
- Cross-flow turbine design (patented)
- FERC pilot license issued for Igiugig, Alaska (2019) — operational on Kvichak River
- Contact: orpc.co

### Verdant Power — New York, NY — **PROVEN BUT TIDAL-FOCUSED**
- **AMERICAN COMPANY**
- Gen5 turbine: 70 kW rated, generates at >1 m/s
- TriFrame mount: 3 turbines per frame (210 kW)
- First commercially licensed tidal project in US (East River, NYC)
- Achieved Technology Readiness Level 9
- More focused on tidal than river current
- Needs >2.0 m/s for economic viability and >6.5m depth
- Contact: verdantpower.com

### Emrgy — Atlanta, GA — **CANAL-FOCUSED, MODULAR**
- **AMERICAN COMPANY**
- 5-25 kW per turbine (some models 10-40 kW)
- Twin vertical-axis turbines, 70%+ water-to-wire efficiency claimed
- Manufacturing facility in Aurora, CO (5 MW/month capacity)
- Designed for canals and water infrastructure channels
- LCOE: $0.07-0.10/kWh
- ARPA-E funded
- Could work in controlled-flow scenarios but designed for smaller channels
- Contact: emrgy.com

### Oceana Energy — US
- Partnered with US Navy (NSWC), Alaska Energy Authority, UAF
- R&D stage
- Less commercially mature

### Natel Energy — Alameda, CA — **FISH-SAFE, LOW-HEAD**
- **AMERICAN COMPANY**
- FishSafe turbines: 98-100% fish survival (tested with sturgeon, eels, trout, salmon)
- D190 RHT: 1 MW class, commercially released
- Monroe Hydro Project in Oregon: operational
- Requires head (elevation drop) — NOT purely hydrokinetic
- Could work if there's any elevation differential at the dock
- Contact: natelenergy.com

### International Companies (for reference)
- **HydroQuest** (France): vertical-axis, river and tidal
- **Smart Hydro Power** (Germany): horizontal-axis, in-stream
- **GKinetic Energy** (Ireland): floating dual-turbine platform

---

## SIMPLER TECHNOLOGIES

### Water Wheels
- Ancient technology, proven for centuries
- Modern versions: 5-500 kW range
- Need head (elevation drop) to work efficiently
- NOT well-suited for pure river current harvesting on the Mississippi
- Could work if there's a side channel or intake with engineered head

### Archimedes Screw Generators
- Work on heads as low as 1.0-1.5 meters
- 60-80% water-to-wire efficiency
- Fish-friendly (debris tolerant)
- 5 kW to 500 kW per unit
- Companies: GreenBug Energy, Renewables First, Freeflow69
- Same limitation: needs head/elevation drop, not suitable for pure kinetic current
- **Manufacturer**: GreenBug Energy (Ontario, Canada — close to US)

---

## REGULATORY REQUIREMENTS

### FERC (Federal Energy Regulatory Commission)
1. **Preliminary Permit** (first step):
   - Grants priority to study a site for up to 4 years
   - Does NOT authorize construction or land disturbance
   - Establishes site priority over competing applicants
2. **Pilot License**:
   - For small-scale testing (typically <5 MW)
   - Faster process than full license
3. **Full License**:
   - Required for commercial operation
   - Can take 2-5+ years

### Army Corps of Engineers
- Must approve any structure in navigable waterway
- Section 10 Rivers and Harbors Act permit
- Must not interfere with commercial navigation (critical on Mississippi — one of busiest commercial waterways in the world)
- Environmental impact assessment required

### Other Federal Requirements
- **US Fish & Wildlife Service**: Endangered species review (pallid sturgeon is native to Mississippi/Missouri basin)
- **NOAA Fisheries**: If threatened/endangered aquatic species impacted
- **Clean Water Act Section 404**: If any dredge/fill in waterway
- **NEPA**: Environmental review

### State Requirements
- Louisiana Department of Natural Resources
- Louisiana Department of Environmental Quality
- State water quality certification (Section 401)

### Timeline Reality
- **Preliminary permit**: 3-6 months
- **Environmental studies**: 1-2 years
- **Pilot license**: 1-2 years
- **Full commercial license**: 3-5 years
- **Total from start to commercial operation**: Realistically 3-7 years

---

## PRECEDENT: FREE FLOW POWER — LESSONS LEARNED

### What They Tried
- 88 preliminary permits on Mississippi River (St. Louis to Gulf)
- 1,000+ MW planned across 53 sites
- 120 turbines per site
- Successfully deployed and tested full-scale turbine in 2011

### Why They Failed
1. **2012 drought**: Record low water on Mississippi killed feasibility at many sites
2. **Low electricity prices**: Natural gas boom dropped wholesale electricity prices
3. **Permitting complexity**: 53 sites = massive regulatory burden
4. **Surrendered all permits**: June 28, 2013

### Lessons for Willow Glen
- **Variable river flow is a REAL risk** — output can drop to near-zero in drought
- **Don't depend on hydrokinetic as primary power** — it's supplemental
- **Start small**: One or two ORPC Modular RivGen units as proof of concept
- **The technology works** — Free Flow's turbine performed as expected with no fish harm
- **Economics only work if electricity is expensive** — at $0.06/kWh wholesale, payback is long
- **ORPC's Shell deployment on the same river is the key reference** — wait for their results

---

## PRACTICAL RECOMMENDATION FOR WILLOW GLEN

### Phase 1: Study and Permit (Year 1-2)
- Contact ORPC directly — they are ALREADY deploying on the Lower Mississippi with Shell
- Request site assessment for Willow Glen frontage
- File FERC preliminary permit for hydrokinetic study
- Install USGS-grade current meters at the dock to get 12 months of velocity data
- Cost: ~$50-100K for studies + permitting

### Phase 2: Pilot Deployment (Year 2-3)
- Deploy 2-4 ORPC Modular RivGen units at the dock
- Target: 30-70 kW continuous
- Use power for dock lighting, security systems, monitoring equipment
- Cost: ~$500K-$1M (estimated, ORPC doesn't publish pricing)

### Phase 3: Scale (Year 3-5, if Phase 2 succeeds)
- Expand to full 1,000 ft of frontage
- Multiple rows of turbines
- Target: 250-500 kW
- Could power all non-compute facility loads (lighting, security, office, HVAC controls)

### What It Won't Do
- Will NOT produce MW-scale power for compute operations
- At 3 mph average current, even 3,500 ft of turbines = <500 kW
- Compare: the gas generators produce 40-45 MW, solar is 2.05 MW
- Hydrokinetic is a **nice-to-have supplemental source**, not a pillar

### What It WILL Do
- Diversify energy portfolio (adds a 5th layer to power hierarchy)
- PR/marketing value: "Powered by the Mississippi River" is compelling
- Continuous 24/7 generation (unlike solar)
- Demonstrate innovation for NVIDIA partnership narrative
- Potential research partnership with LSU (they're already working with ORPC)

---

## COST SUMMARY

| Item | Estimated Cost | Annual Output | LCOE |
|------|---------------|---------------|------|
| ORPC Modular RivGen (2 units) | $500K-$1M | ~60-120 MWh | $0.15-0.30/kWh |
| Verdant Gen5 TriFrame | $1-2M | ~150-500 MWh | $0.10-0.20/kWh |
| Full array (20 turbines) | $3-8M | ~800-2,000 MWh | $0.10-0.15/kWh |
| FERC permitting + studies | $100-300K | N/A | N/A |

Note: Hydrokinetic LCOE is currently $0.07-0.30/kWh depending on velocity and scale. At Mississippi River velocities near St. Gabriel, expect the higher end of that range. Compare to grid at ~$0.06/kWh wholesale and gas generation at $0.04-0.06/kWh.

### Honest Bottom Line
Hydrokinetic on the Mississippi at St. Gabriel is **technically feasible but economically marginal** at current river velocities. The real value is portfolio diversification, innovation narrative, and potential research partnerships — not raw energy economics. If ORPC's Shell deployment succeeds on the Lower Mississippi, that changes the calculus. Watch their results closely.
