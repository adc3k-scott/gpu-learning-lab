# Edge AI Upgrade — Part 3: Bloom Energy Power Architecture
*Notion backup — 2026-04-06*

Status: 🟡 WRITTEN — Ready for insertion as dedicated section in next revision pass (not yet in .docx files as standalone section)
> Insert into Spec: After Power Distribution section or as new subsection of Power Architecture
> Insert into Financing: After Utility Integration section or within Engineering Layout
---
## On-Site Power Generation — Bloom Energy Fuel Cell Architecture
### Overview
The ADC edge infrastructure campus incorporates Bloom Energy solid oxide fuel cell systems as a core element of the site power architecture. Bloom Energy fuel cells convert natural gas into electricity through an electrochemical process — not combustion — producing continuous, utility-grade power with higher reliability and lower emissions than grid-delivered electricity or traditional generator backup.
This is not a backup power system. Bloom fuel cells operate continuously, generating baseload power that supplements or displaces grid electricity during normal operations. The result is a hybrid power architecture that reduces grid dependency, improves power quality, and provides economic advantages through lower effective energy cost and reduced demand charges.
### Why Fuel Cells for Edge AI Infrastructure
AI compute workloads are power-intensive and power-sensitive. GPU-accelerated systems require clean, continuous power with minimal voltage variation, no interruptions, and predictable cost. Traditional grid power in regional markets is subject to demand charges, rate variability, transmission losses, and reliability limitations that fuel cell generation mitigates directly.
Bloom Energy fuel cells deliver:
- Continuous UPS-Quality Power: Fuel cells produce steady-state DC power converted to AC at the point of generation. Power quality meets or exceeds utility grid specifications with less than 1% total harmonic distortion. This is inherently cleaner power than grid delivery, which accumulates distortion across transmission and distribution infrastructure.
- Reduced Grid Dependency: On-site generation reduces the facility’s draw from the local utility grid, mitigating exposure to grid outages, demand charges, rate increases, and capacity limitations that constrain expansion.
- Modular Scaling: Bloom Energy Server units are modular. A single unit generates approximately 300 kW. Units stack to match facility load, scaling in increments as the edge campus expands from Phase 1 through full buildout.
- Lower Transmission Loss: Power generated on-site eliminates the 5–8% transmission and distribution losses inherent in grid-delivered electricity. Every kilowatt generated on-site delivers more usable power to the compute load.
- High Reliability: Bloom fuel cells achieve 99.99%+ availability in commercial deployments. Combined with grid power and diesel backup, the site power architecture achieves redundancy levels comparable to Tier III+ data center facilities.
- Compact Footprint: A 300 kW Bloom Energy Server occupies approximately 900 square feet — significantly less than equivalent diesel generator capacity and compatible with the ADC site layout at 1201 SE Evangeline Thruway.
### Site Power Architecture — Three-Layer Model
The ADC edge infrastructure campus employs a three-layer power architecture:
Layer 1 — Grid Power (Primary).
Utility grid connection provides the primary power feed to the site. Three-phase electrical service from the local utility supplies the main switchgear, which distributes power to the edge compute nodes and shared utility plant. Grid power handles the base electrical load and provides the primary source during normal operations.
Layer 2 — Bloom Energy Fuel Cells (Supplemental Generation).
Bloom Energy fuel cell systems operate continuously, generating on-site power that supplements grid delivery. During normal operations, fuel cells offset grid consumption, reducing demand charges and providing a hedge against rate variability. During grid instability or planned maintenance, fuel cells carry a larger share of the facility load. Fuel cell output is synchronized with grid power through the site’s electrical distribution system.
Layer 3 — Diesel Generators (Emergency Backup).
Diesel generators provide emergency standby power for grid outages that exceed the combined capacity of grid and fuel cell systems, or for maintenance windows requiring full backup. Generators are sized for N+1 redundancy relative to the critical IT load and start automatically on grid failure detection.
Combined Redundancy Strategy:
The three-layer model provides N+1 power redundancy without relying on any single source. Grid failure triggers increased fuel cell output and generator start sequence. Fuel cell maintenance is performed on individual modules without total generation loss. Generator testing occurs under load without disrupting primary or supplemental power. This layered approach meets the reliability requirements of commercial compute hosting while maintaining the economic benefits of on-site generation.
### Gulf Coast Natural Gas Advantage
Louisiana sits at the center of the nation’s natural gas production and distribution infrastructure. The Gulf Coast natural gas supply provides:
- Price Stability: Louisiana natural gas prices are among the lowest and most stable in the nation due to proximity to production, pipeline infrastructure density, and regional supply surplus.
- Supply Reliability: Multiple interstate and intrastate pipeline systems serve the Lafayette area, providing redundant supply routes that mitigate single-point-of-failure risk.
- Infrastructure Availability: Natural gas service is available at the ADC site on existing utility infrastructure. No new pipeline construction or major service upgrades are required for Phase 1 fuel cell deployment.
- Scaling Capacity: Regional natural gas supply can support fuel cell capacity well beyond the Phase 1 deployment without infrastructure constraints.
### Future Renewable Fuel Transition
Bloom Energy fuel cells are compatible with hydrogen and biogas fuel sources. As renewable fuel infrastructure develops along the Gulf Coast — including green hydrogen production from offshore wind and solar, and biogas from agricultural and industrial waste streams — the ADC power architecture can transition from natural gas to renewable fuels without replacing the fuel cell hardware.
This positions the facility for long-term alignment with evolving emissions requirements, corporate sustainability mandates from enterprise tenants, and potential renewable energy credits — while deploying today on readily available, cost-effective natural gas.
### Bloom Energy Integration — Financial Impact (Financing Document Only)
For the financing proposal, the Bloom Energy integration supports the project’s financial positioning in several ways:
- Reduced Operating Cost: On-site generation at fuel cell efficiency rates (60%+) produces electricity at lower effective cost than grid-delivered power in most Louisiana utility rate structures, particularly when demand charges are factored.
- Predictable Energy Cost: Fuel cell generation provides a hedge against utility rate increases, supporting more reliable pro forma projections for lender analysis.
- Infrastructure Value: Bloom Energy systems are tangible, depreciable capital assets that add to the facility’s collateral value and support equipment financing structures.
- Incentive Eligibility: Fuel cell systems may qualify for federal Investment Tax Credit (ITC), Louisiana industrial tax incentives, and other clean energy programs that improve project economics.
- Tenant Attraction: Enterprise and institutional tenants increasingly require or prefer facilities with on-site generation capability and a pathway to renewable power. Fuel cell infrastructure is a competitive differentiator in tenant acquisition.
---
## Cooling Architecture — MARLIE I vs ADC 3K Pods
> MARLIE I and ADC 3K pods use different cooling systems by design. This is not inconsistency — it is the right technology for each deployment context.
### MARLIE I — Cold Plate Liquid Cooling (CDU + Fans)
- Technology: Direct-to-chip cold plate liquid cooling with CDU (Cooling Distribution Unit) and fan-assisted thermal management
- Why for MARLIE I: Building-based deployment with controlled mechanical room. Cold plate represents current state-of-the-art public-facing technology — proven, code-compliant, well-understood by building inspectors, lenders, and facility engineers.
- Vendor options: CoolIT Systems, Vertiv, Motivair — all established CDU suppliers with commercial support
- Grid integration: Standard CRAC/CRAH supplemental for ambient control in non-compute spaces
### ADC 3K Pods — Full Immersion Cooling (Engineered Fluids EC-110)
- Technology: Single-phase full immersion — GPUs and servers fully submerged in dielectric fluid (EC-110)
- Why immersion for Louisiana pods: Louisiana ambient conditions (regularly 95°F+ with 90%+ humidity) make air and fan-based cooling thermally inefficient and mechanically unreliable for remote unattended sites. Immersion eliminates ambient air from the cooling equation — GPU thermal performance is identical in New Orleans in August as in Shreveport in January.
- Why immersion for remote sites: No moving parts (no fans, no compressors, no HVAC). Dramatically lower maintenance burden — critical for sites without permanent on-site staff.
- Why immersion for pods: A sealed immersion tank inside a 20-ft ISO container is self-contained. No external cooling towers, no makeup water, no refrigerant circuits. The pod ships as a complete thermal system.
- Fluid: Engineered Fluids EC-110 (single-phase dielectric). NEVER reference 3M Novec — discontinued.
- PUE: Immersion cooling achieves PUE of 1.03-1.05 — among the lowest possible. Bloom Energy + immersion is an extremely efficient combined system.
### Why Two Different Systems
MARLIE I is a permanent building where code compliance, lender familiarity, and long-term maintainability by licensed mechanical contractors are priorities. Cold plate CDU is the right choice. ADC 3K pods are unattended remote deployments in Louisiana's extreme climate where mechanical simplicity, thermal reliability, and zero ambient dependence are priorities. Full immersion is the right choice. Both are correct — for their respective contexts.
---
## New Iberia Solar — Renewable Integration Path
- New solar manufacturing facility operational in New Iberia, Louisiana (Iberia Parish, ~30 miles SW of Lafayette)
- ADC pod sites with available roof or ground area can incorporate locally sourced solar arrays as supplemental generation
- Combined system: Bloom Energy fuel cell (baseload) + solar (daytime supplement) + LUS grid (backup) + diesel (emergency)
- Benefit: Reduces natural gas consumption per site, qualifies for renewable energy credits, strengthens ESG narrative for enterprise tenants
- Louisiana-first supply chain: Local solar sourcing shortens delivery timeline and supports regional economic development — relevant to LED incentive applications