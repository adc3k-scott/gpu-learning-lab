# 🚀 Mission Control HQ
*Notion backup — 2026-04-06*

*[Child: 📋 Task Tracker]*
*[Child: Dev Session Log]*
*[Child: 📝 SOPs & Documentation]*
Standard operating procedures and technical references for Mission Control.
---
## DNS Records (Namecheap → missioncontrolhd.com)
| Type | Host | Value |
| TXT | resend._domainkey | p=MIGfMA0GCSqGSIb3DQEB... (DKIM key) |
| TXT | send | v=spf1 include:amazonses.com ~all |
| TXT | _dmarc | v=DMARC1; p=none; |
---
## Supabase SMTP Settings
  - Custom SMTP: ON
  - Sender email: noreply@missioncontrolhd.com
  - Sender name: Mission Control HD
  - Host: smtp.resend.com
  - Port: 465
  - Username: resend
  - Password: Resend API key (saved in Supabase)
---
## Deploying to Vercel
  1. Push changes to GitHub (main branch)
  1. Vercel auto-deploys from main
  1. Check deployment at vercel.com dashboard
  1. Verify at missioncontrolhd.com
---
## Password Reset (Emergency — When Email Is Broken)
If you can't reset via email, use the Supabase SQL Editor:
  1. Go to Supabase dashboard → SQL Editor
  1. Run: SELECT id FROM auth.users WHERE email = 'your@email.com';
  1. Share the output with Claude to generate the password update query
---
## Vercel Environment Variables
| Variable | Value |
| NEXT_PUBLIC_SITE_URL | https://missioncontrolhd.com |
| STRIPE_WEBHOOK_SECRET | whsec_... (live) |
| KIT_API_KEY | (set) |
| STRIPE_PRO_ANNUAL_PRICE_ID | price_1T4BQuJt9Vd7LWdNXcMxqqQl |
| STRIPE_PRO_MONTHLY_PRICE_ID | price_1T4BQqJt9Vd7LWdNJ4odqhwg |
| ANTHROPIC_API_KEY | (set) |
| NEXT_PUBLIC_SUPABASE_URL | (set) |
| NEXT_PUBLIC_SUPABASE_ANON_KEY | (set) |
| SUPABASE_SERVICE_ROLE_KEY | (set) |
| STRIPE_SECRET_KEY | sk_live_... |
| NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY | pk_live_... |
| STRIPE_PREMIUM_MONTHLY_PRICE_ID | price_1T4BQqJt9Vd7LWdNZOAvZB2u |
| STRIPE_PREMIUM_ANNUAL_PRICE_ID | price_1T4BQrJt9Vd7LWdNixDFqmSN |
---
> NOTE (2026-03-23): This page contains SOPs for Mission Control HD SaaS (on hold). Content remains valid for when MCHD development resumes. DNS records, Supabase config, and Vercel deploy steps are still current.
*[Child: 💡 Notes & Ideas]*
Quick capture space for ideas, meeting notes, and reference material.
---
## Feature Ideas
  - Morning brief email automation via Kit
  - Google/GitHub OAuth for easier sign-in
  - Social sharing / OG images for marketing
## Notes
Add notes here as you go. Each major topic can become its own sub-page.
> ARCHIVED 2026-03-23: Content duplicated in Task Tracker. No longer maintained.
*[Child: Edge AI -- Strategy, Customers & Go-To-Market]*
> Edge AI deployment specs, drone/UAS integration, and distributed inference architecture documents.
---
## Contents
  - Edge node hardware specs
  - Part 107 UAS AI integration
  - Distributed inference network design
  - LTE/5G backhaul configurations
*[Child: Edge AI Infrastructure Upgrade — Master Prompt]*
Purpose: This is the master instruction set for upgrading all ADC project documents from "containerized data center pods" to Modular Edge AI Infrastructure Platform for Gulf Coast deployment. This prompt should be loaded into any future session where document updates are being made.
Date: February 27, 2026
> ✅ STATUS: V4 Documents Generated — February 28, 2026
> Terminology updates, exec summary rewrites, and positioning upgrades applied to Spec V4 and Financing V4. New sections (Edge Positioning + Bloom Energy) written and staged in Parts 2–3. One-Pager V2 updated.
---
## PRIMARY OBJECTIVE
Transform the project from "containerized data center pods" into Modular Edge AI Infrastructure Platform for Gulf Coast deployment.
This includes: financing narrative, technical architecture, power systems, site design, deployment strategy, economic impact positioning, investor positioning, manufacturing narrative, and municipal/industry use cases.
---
## SECTION 1 — EDGE INFRASTRUCTURE POSITIONING (NEW CORE SECTION)
Definition:
    - Edge computing = compute placed near data demand
    - Low latency, bandwidth reduction, regional resilience, distributed AI capacity
ADC Positioning — ADC builds:
    - Deployable edge compute nodes
    - Modular regional AI infrastructure
    - Distributed GPU capacity
    - Local compute power for industry and public systems
Target Edge Markets:
    - Drone operations infrastructure
    - Public safety compute
    - Industrial AI workloads
    - Energy sector analytics
    - Autonomous systems support
    - University research compute
    - Enterprise AI hosting
    - Municipal services
    - Low-latency regional content delivery
Explain why Lafayette is ideal for regional edge infrastructure.
---
## SECTION 2 — ARCHITECTURE UPDATE
Update all architecture language to:
    - Modular edge compute node
    - Distributed deployment model
    - Site-agnostic infrastructure
    - Rapid deployment compute platform
    - Local AI processing capacity
Explain advantages vs centralized hyperscale: lower latency, faster deployment, smaller capital increments, resilience, infrastructure flexibility.
---
## SECTION 3 — BLOOM ENERGY POWER ARCHITECTURE
Bloom Energy Fuel Cell Systems:
    - Natural gas powered
    - Continuous UPS-quality power
    - Reduced grid dependency
    - On-site generation
    - Modular scaling
    - Lower transmission loss
    - High reliability architecture
Deployment Model:
    - Primary grid power
    - Bloom fuel cell supplemental generation
    - Diesel emergency backup
    - N+1 redundancy strategy
Explain Gulf Coast natural gas supply reliability. Explain future renewable fuel transition potential.
---
## SECTION 4 — SITE STRATEGY UPDATE (1201 SE EVANGELINE THRUWAY)
Update site plan to include:
    - Distributed edge compute campus
    - Container pod layout
    - Cooling plant infrastructure
    - Bloom Energy generation zone
    - Generator backup area
    - Fiber connectivity
    - Expansion to multi-pod deployment
    - Municipal infrastructure access
Explain why location supports edge deployment: existing utilities, city infrastructure access, proximity to airport, regional network coverage, industrial compatibility.
---
## SECTION 5 — FINANCIAL + BANK POSITIONING
Update financing narrative to explain:
    - Growing regional demand for AI compute
    - Distributed infrastructure model
    - Scalable deployment
    - Phased capital deployment
    - Infrastructure-backed revenue model
    - Regional economic impact
Explain project in simple terms: "regional AI compute infrastructure similar to a power plant for digital services."
---
## SECTION 6 — MANUFACTURING & DEPLOYMENT STRATEGY UPDATE
Explain pods as:
    - Standardized edge compute modules
    - Rapidly deployable infrastructure units
    - Transportable compute systems
    - Scalable manufacturing product line
Explain national deployment potential.
---
## SECTION 7 — TERMINOLOGY UPDATES THROUGHOUT DOCUMENT
Replace or upgrade language:
    - "data center pods" → "edge compute nodes"
    - "container data center" → "modular edge infrastructure"
    - "GPU pod" → "deployable AI compute module"
    - "data center site" → "edge infrastructure campus"
Keep technical accuracy.
---
## SECTION 8 — EXECUTIVE SUMMARY REVISION
Rewrite executive summary to emphasize:
    - Distributed edge AI infrastructure
    - Gulf Coast energy advantage
    - Modular deployment
    - Scalable regional compute capacity
    - Infrastructure modernization opportunity
Tone: institutional, credible, non-hype.
---
## OUTPUT FORMAT
Produce:
    1. Updated document structure
    1. New sections inserted
    1. Revised language examples
    1. Executive summary rewrite
    1. Technical architecture update
    1. Financing narrative update
    1. Site architecture update
    1. Clear implementation roadmap
Maintain professional engineering and investment report tone.
*[Child: Edge AI Upgrade — Part 1: Executive Summary Rewrites]*
Status: ✅ APPLIED to V4 documents — Both exec summaries rewritten and inserted into Spec V4 and Financing V4 .docx files
---
## 1A — Product Specification Executive Summary (Replaces Existing)
> Insert into: ADC-Compute-Pod-V3-800kW-Specification.docx → Executive Summary section
The ADC Compute Pod is a 20-foot ISO shipping container engineered as a deployable edge AI compute node — the highest-density modular edge infrastructure unit available today. Manufactured by Advantage Design Construction Inc. in Lafayette, Louisiana, each unit is designed around a single principle: build the infrastructure for 800 kW on Day 1, even if first deployments operate at 130 kW.
The ADC Compute Pod enables distributed edge AI infrastructure across the Gulf Coast and beyond. Rather than concentrating compute capacity in centralized hyperscale facilities hundreds of miles from end users, ADC deploys standardized, site-agnostic compute nodes directly into the regions where processing demand originates. This distributed architecture delivers lower latency, faster deployment timelines, smaller capital increments, and regional infrastructure resilience that centralized models cannot match.
Each edge compute node ships as a self-contained infrastructure module with integrated power distribution, direct-to-chip liquid cooling, fire protection, environmental monitoring, and deterministic safety controls. The modular block architecture allows any subsystem to be upgraded independently — power, cooling, compute payload, or controls — without affecting adjacent systems. A unit deployed in 2026 with NVIDIA Vera Rubin NVL72 architecture is designed for forward compatibility with next-generation NVIDIA GPU platforms without modification to the container shell.
Version 3.0 incorporates dual-mode high-power delivery (480V AC active with 800V DC pre-wired), a dedicated 48V DC facility bus for infrastructure systems, Bloom Energy fuel cell integration provisions for on-site power generation, microgrid and solar integration, container yard deployment models, a vendor-agnostic rack interface, expanded fire protection and safety sequencing, and a deterministic two-layer control architecture with AI optimization capability.
The platform supports deployment across edge computing markets including energy sector analytics, industrial AI workloads, public safety compute, autonomous systems support, drone operations infrastructure, university research computing, enterprise AI hosting, and municipal digital services. Each node connects to any site providing power, coolant, and fiber — from industrial yards to purpose-built edge campuses.
This is not a prototype. Every component specified in this document is commercially available as of Q1 2026. The ADC Compute Pod is a manufactured product with a 12-week factory-to-ship timeline, designed for rapid regional deployment at scale.
---
## 1B — Financing Proposal Executive Summary (Replaces Existing)
> Insert into: ADC-Project-Financing-Proposal-V3.docx → Executive Summary section
Advantage Design Construction Inc. ("ADC") respectfully submits this project financing proposal for the development of a modular edge AI infrastructure campus in Lafayette, Louisiana. The project involves the acquisition and improvement of three adjacent parcels on Chag Street, the removal of existing blighted structures, and the phased deployment of modular edge compute nodes and supporting power generation infrastructure on the cleared and improved site.
The facility represents a new class of regional digital infrastructure — comparable in concept to a distributed power plant for computing services. Rather than constructing a single large-scale data center, ADC deploys standardized, rapidly deployable edge compute modules that provide AI processing capacity directly within the region where demand is growing. This distributed infrastructure model enables phased capital deployment, modular revenue scaling, and infrastructure flexibility that traditional centralized facilities cannot achieve.
The project is positioned at the intersection of three converging market forces: rapidly growing regional demand for AI and high-performance compute capacity; the strategic shift toward distributed edge infrastructure that places processing power closer to end users and industrial operations; and Louisiana’s competitive advantages in energy cost, natural gas availability, fiber connectivity, and workforce development incentives.
Phase 1 deploys four edge compute nodes and a shared utility plant — including provisions for Bloom Energy fuel cell power generation — on approximately 0.60 acres adjacent to the borrower’s existing commercial facility. The site is located within an established urban utility corridor with existing access to three-phase electrical service, fiber connectivity, natural gas, and municipal water and drainage.
The borrower is a Louisiana-licensed general contractor with over 20 years of commercial construction experience, currently completing the Certified Data Centre Design Professional (CDCDP) certification through the Uptime Institute. The borrower built and owns the adjacent commercial facility at 1201 SE Evangeline Thruway, which serves as the operations base for the edge infrastructure campus.
Total Phase 1 project cost is estimated at $1.75–$2.25 million. The borrower seeks a 5-year commercial term loan with a 12-month interest-only construction period, followed by 48 months of principal and interest payments. Conservative pro forma projections indicate breakeven at approximately 45% utilization and a debt service coverage ratio exceeding 1.35x at 65% stabilized utilization.
Key Project Characteristics:
    - Distributed Edge Infrastructure: Modular compute nodes deployable across multiple sites, serving growing regional demand for AI processing, industrial analytics, and enterprise computing.
    - Phased Capital Deployment: Phase 1 is a controlled pilot. Future phases expand capacity on the same site or deploy to additional locations without additional land acquisition.
    - On-Site Power Generation: Bloom Energy fuel cell integration reduces grid dependency, provides UPS-quality continuous power, and leverages Gulf Coast natural gas supply.
    - Relocatable, Collateralizable Assets: Containerized modules retain substantial residual value independent of the real estate and can be physically relocated if necessary.
    - Conservative Initial Deployment: 520 kW initial IT capacity across four modules, well within available utility service, with infrastructure designed for up to 3.2 MW expansion.
    - Existing Operations Base: Adjacent commercial facility eliminates new office/shop construction, significantly reducing project cost and timeline.
    - Blight Removal and Economic Development: Project removes three blighted structures, improves the tax base, and positions Lafayette as a regional edge AI infrastructure hub.
*[Child: Edge AI Upgrade — Part 2: Edge Infrastructure Positioning]*
Status: 🟡 WRITTEN — Ready for insertion as dedicated section in next revision pass (not yet in .docx files as standalone section)
> Insert after: Executive Summary in both documents
---
## Edge AI Infrastructure — Market Context and ADC Positioning
### What Is Edge Computing Infrastructure
Edge computing places processing capacity at or near the point of data demand rather than routing workloads to centralized facilities hundreds or thousands of miles away. For AI workloads specifically, edge infrastructure provides the low-latency, high-bandwidth local processing that real-time applications require — autonomous vehicle systems cannot wait 50 milliseconds for a response from a data center in Virginia, and industrial process control cannot tolerate the variability of long-haul network routing.
The architectural shift from centralized to distributed compute follows the same pattern as electrical power generation: the first generation was centralized (large power plants), the current generation is increasingly distributed (solar, microgrid, on-site generation). Computing infrastructure is following the same trajectory. Hyperscale data centers serve bulk processing and storage, but the fastest-growing segment of the market is edge infrastructure — compute capacity deployed regionally, close to the operations and populations it serves.
Edge infrastructure delivers four primary advantages over centralized models:
    - Lower Latency: Processing occurs within the region, eliminating long-haul network delays. Critical for real-time AI inference, autonomous systems, and industrial control.
    - Bandwidth Reduction: Data is processed locally rather than transmitted to distant facilities. This reduces network costs and eliminates bottlenecks for data-intensive workloads like video analytics and sensor fusion.
    - Regional Resilience: Distributed infrastructure is inherently more resilient than centralized models. A regional edge node operates independently; a centralized facility failure affects all dependent users.
    - Incremental Scalability: Edge nodes deploy in standardized increments rather than requiring the billion-dollar capital commitments of hyperscale construction. This enables market-responsive capacity additions.
### ADC’s Position in the Edge Infrastructure Market
Advantage Design Construction manufactures and deploys modular edge AI compute nodes — self-contained, site-agnostic infrastructure units that deliver GPU-accelerated processing capacity to any location with power, coolant supply, and fiber connectivity.
ADC’s core capability is:
    - Deployable Edge Compute Nodes: Standardized 20-foot ISO containers engineered for 50–800+ kW of AI compute, shipped fully integrated with power distribution, liquid cooling, fire protection, and monitoring.
    - Modular Regional AI Infrastructure: Multiple nodes deploy as an edge compute campus on prepared sites, scaling capacity in standardized increments as demand grows.
    - Distributed GPU Capacity: Each node supports current and next-generation GPU architectures (NVIDIA Vera Rubin NVL72, AMD MI-series, or any vendor), providing local AI processing for inference, training, and analytics workloads.
    - Infrastructure for Industry and Public Systems: Edge nodes serve commercial enterprises, industrial operations, municipal agencies, research institutions, and defense applications with locally deployed compute power.
### Target Edge Markets
The ADC Compute Pod addresses deployment across the following edge computing segments:
Energy Sector Analytics. Oil and gas operations, pipeline monitoring, refinery process optimization, and renewable energy management generate massive sensor data streams that require real-time AI processing. Gulf Coast energy operations represent a natural anchor market for regionally deployed edge compute.
Industrial AI Workloads. Manufacturing quality inspection, predictive maintenance, process optimization, and digital twin simulation require local compute capacity that cannot depend on distant centralized facilities. Edge nodes deployed at or near industrial sites provide dedicated AI processing.
Drone Operations Infrastructure. Commercial drone operations for inspection, surveying, agriculture, and logistics require real-time AI inference for navigation, obstacle avoidance, and payload processing. Edge compute nodes provide the local processing backbone for regional drone operations.
Public Safety Compute. Emergency response coordination, real-time video analytics, disaster modeling, and communications infrastructure benefit from locally deployed processing that operates independently of distant facilities and long-haul networks.
Autonomous Systems Support. Autonomous vehicles, robotic systems, and unmanned maritime operations require regional AI inference infrastructure with sub-millisecond response times that only edge deployment can provide.
University and Research Computing. Regional universities and research institutions require GPU-accelerated compute for AI research, simulation, and training workloads. Edge infrastructure provides dedicated local capacity without the cost and complexity of building institutional data centers.
Enterprise AI Hosting. Regional businesses adopting AI for operations, customer service, analytics, and automation need local compute infrastructure. Edge nodes provide enterprise-grade AI hosting without requiring businesses to build their own facilities or depend on distant cloud regions.
Municipal Digital Services. Smart city systems, traffic management, public health analytics, permitting automation, and constituent services increasingly depend on AI processing that benefits from local deployment within the municipality.
Low-Latency Content Delivery. Streaming media, gaming, AR/VR applications, and real-time collaboration tools benefit from regional compute and content caching that reduces latency and improves user experience.
### Why Lafayette, Louisiana
Lafayette occupies a strategic position for Gulf Coast edge infrastructure deployment:
    - LUS Fiber: Lafayette’s municipal fiber network provides carrier-grade connectivity infrastructure already in place — a competitive advantage that most regional markets lack.
    - Energy Cost and Supply: Louisiana electricity rates are among the lowest in the nation, and the Gulf Coast natural gas supply infrastructure supports on-site power generation (including Bloom Energy fuel cells) with exceptional reliability.
    - Geographic Position: Lafayette serves as a regional hub for energy sector operations, petrochemical industry, agriculture technology, and military/defense operations across the Gulf Coast corridor.
    - Workforce and Incentives: Louisiana offers aggressive economic development incentives (ITEP, Quality Jobs, Enterprise Zone, LED FastStart) and a growing technical workforce supported by regional universities.
    - Industrial Compatibility: The ADC site at 1201 SE Evangeline Thruway is located in an established commercial/industrial corridor with existing utility infrastructure, zoning compatibility, and expansion capacity.
    - Underserved Market: There is no significant AI compute infrastructure deployed in the Lafayette-to-Lake Charles corridor today. ADC’s edge campus fills a regional infrastructure gap that the market has not yet addressed.
---
## KLFT / SkyCommand — Gulf Coast Emergency Drone Deployment Hub
> The KLFT project at Lafayette Regional Airport is the emergency response and autonomous operations arm of the ADC ecosystem. This is not a commercial drone startup — it is a Gulf Coast Emergency Drone Deployment Hub providing AI-coordinated emergency response, infrastructure inspection, and public safety operations across the region.
    - Base: Lafayette Regional Airport (KLFT) — city-owned, municipally operated
    - Platform: Skydio X10 + Skydio Dock — US-manufactured, no CCP regulatory exposure
    - Emergency missions: Hurricane response, flood mapping, search and rescue, industrial incident response
    - Commercial missions: Pipeline inspection, tower inspection, precision agriculture, logistics
    - Compute: MARLIE I NOC remote fleet management + Jetson Orin NX dock-side edge inference
    - Market position: No comparable AI drone infrastructure exists in the Lafayette-to-New Orleans corridor
---
## New Iberia Solar — Local Renewable Energy Partner
> A solar manufacturing facility has been established in New Iberia, Louisiana (~30 miles from Lafayette). ADC is positioned to source solar panels locally, supporting Louisiana's renewable energy industry while reducing supply chain distance and demonstrating Louisiana-first economic commitment.
    - Location: New Iberia, Louisiana (Iberia Parish)
    - ADC integration: Solar arrays on pod sites and MARLIE I — supplemental generation alongside Bloom Energy fuel cells
    - Strategic value: Local sourcing strengthens financing narrative, investor appeal, and economic development positioning
    - Energy transition: Natural gas (now) + solar (supplement) + hydrogen/biogas (future) — full renewable pathway documented
*[Child: Edge AI Upgrade — Part 3: Bloom Energy Power Architecture]*
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
*[Child: Edge AI Upgrade — Part 4: Terminology Map, Site Strategy & Roadmap]*
> Status: DRAFT — March 2026. Covers official project terminology, site layout strategy, and phased deployment roadmap.
## PART A — TERMINOLOGY MAP
Official language for all ADC project documents, presentations, financing proposals, and investor materials. Use the right-column term in all new and revised documents. The left column is deprecated.
### Architecture & Product Language
    - data center pods  ->  edge compute nodes
    - container data center  ->  modular edge infrastructure
    - GPU pod  ->  deployable AI compute module
    - data center site  ->  edge infrastructure campus
    - containerized data center  ->  modular edge compute node
    - GPU cluster  ->  distributed AI compute array
    - server rack  ->  compute payload (within the node context)
    - data center build  ->  edge infrastructure deployment
    - pod manufacturer  ->  edge infrastructure manufacturer
### NVIDIA Hardware Language
    - Blackwell / GB200 / GB300 / B200 / B100  ->  RETIRED — do not reference
    - Grace CPU / Grace Hopper  ->  Vera CPU (88 Olympus Arm cores, Armv9.2)
    - HBM3e  ->  HBM4 (288 GB per Rubin GPU, 20.7 TB per NVL72 rack, 1.58 PB/s aggregate)
    - NVLink 5  ->  NVLink 6 (3.6 TB/s per GPU bidirectional, 260 TB/s aggregate per rack)
    - Spectrum-X SN5000  ->  Spectrum-6 (SN6810 / SN6800)
    - ConnectX-8 / BlueField-3  ->  ConnectX-9 SuperNIC / BlueField-4 DPU
    - Feynman / Kyber  ->  UNCONFIRMED — do not reference until officially announced
    - Current platform reference  ->  NVIDIA Vera Rubin NVL72 (H2 2026, confirmed CES 2026)
### Performance & Compute Language
    - 10x lower token cost vs Blackwell  ->  REMOVE — not NVIDIA-sourced
    - 4x fewer GPUs  ->  REMOVE — not NVIDIA-sourced
    - ~120 kW TDP per rack  ->  TDP not published by NVIDIA — contact NVIDIA Enterprise Sales
    - 2.5x FP4 compute density vs GB200 NVL72  ->  USE THIS (3.6 vs 1.44 ExaFLOPS per rack, NVFP4)
    - 260 TB/s connecting 14-rack cluster  ->  260 TB/s aggregate per NVL72 rack (intra-rack only via NVLink 6)
    - Scale-out networking  ->  InfiniBand NDR (cross-rack) — not NVLink 6
### Financial & Business Language
    - GPU rental business  ->  edge infrastructure hosting
    - cloud GPU provider  ->  regional edge AI infrastructure operator
    - data center investor  ->  edge infrastructure capital partner
    - compute rental  ->  edge infrastructure services
    - pod revenue  ->  edge compute hosting revenue
---
## PART B — SITE STRATEGY: 1201 SE EVANGELINE THRUWAY
Primary deployment site for MARLIE I — Lafayette AI Factory. Located in an established commercial/industrial corridor in Lafayette, Louisiana, with direct access to three-phase electrical service, LUS Fiber, natural gas, and municipal water and drainage.
### Site Overview
    - Address: 1201 SE Evangeline Thruway, Lafayette, Louisiana
    - Site area: Three adjacent parcels on Chag Street — approximately 0.60 acres Phase 1 footprint
    - Existing asset: Borrower-owned commercial facility adjacent to site serves as operations base
    - Current condition: Three blighted structures — removal included in Phase 1 scope
    - Zoning: Commercial/industrial corridor — compatible with edge compute deployment
    - Utility access: Three-phase electrical service, LUS Fiber, natural gas, municipal water and drainage
### Phase 1 Site Layout
    - Four 20-foot ISO edge compute nodes — deployed in 2x2 grid with maintenance clearance
    - Shared utility plant — central CDU (coolant distribution unit), switchgear, and MDF
    - Bloom Energy fuel cell zone — reserved pad adjacent to utility plant, natural gas service pre-run
    - Diesel generator backup — N+1 standby units, auto-start on grid failure
    - Fiber entry point — LUS Fiber primary, diverse second carrier conduit pre-installed
    - Security perimeter — fenced and monitored yard, camera coverage, access control
    - Operations base — existing adjacent building handles NOC, storage, and staff functions
### Utility Infrastructure
    - Power: Utility grid three-phase primary + Bloom Energy fuel cell supplemental + diesel emergency
    - Cooling: Closed-loop liquid cooling plant — warm-water CDU serving all nodes, dry coolers on perimeter
    - Connectivity: LUS Fiber primary (carrier-grade municipal network) + diverse carrier secondary
    - Gas: Natural gas service for Bloom Energy fuel cells — Gulf Coast supply, existing infrastructure
    - Water: Municipal water and drainage for cooling plant makeup water and fire suppression
### Expansion Capacity
    - Phase 1 IT capacity: 520 kW across four nodes
    - Phase 1 infrastructure ceiling: Designed to 800 kW per node — 3.2 MW total site capacity
    - Phase 2 expansion: Additional node rows on same parcels — no new land acquisition required
    - Phase 3 multi-site: Replicate site model to additional Gulf Coast locations using same manufactured nodes
    - Power expansion path: Additional Bloom Energy server units stack in modular increments (300 kW each)
    - Cooling expansion path: Additional CDU modules add in-line with node deployment — no plant redesign
---
## PART C — DEPLOYMENT ROADMAP
Phased deployment schedule from site preparation through regional multi-site buildout. All timelines are based on 12-week node manufacturing lead time and standard commercial construction sequencing.
### Phase 1 — MARLIE I Lafayette (2026)
    1. Site prep and blight removal — Q1 2026
    1. Financing close and infrastructure procurement — Q1/Q2 2026
    1. Utility plant construction (CDU, switchgear, fiber, gas) — Q2 2026
    1. First two node deliveries and commissioning — Q2/Q3 2026
    1. NVIDIA Vera Rubin NVL72 compute payload installation — H2 2026 (per NVIDIA availability)
    1. Nodes 3 and 4 deployment — Q3 2026
    1. Bloom Energy Phase 1 fuel cell installation — Q3/Q4 2026
    1. Full Phase 1 operational: 520 kW IT capacity, 4 nodes — Q4 2026
### Phase 2 — Capacity Expansion (2027)
    1. Add nodes 5-8 on existing site — no new land required
    1. Scale Bloom Energy fuel cell capacity to match expanded load
    1. Upgrade fiber to additional carrier for redundancy
    1. Target: 1.0 MW+ IT capacity on Lafayette site
    1. Begin site evaluation for second Gulf Coast location
### Phase 3 — Gulf Coast Regional Deployment (2027-2028)
    1. Deploy edge compute campus at second Gulf Coast location (New Orleans corridor or Lake Charles)
    1. Leverage manufactured node inventory for rapid site-to-site replication
    1. Establish regional fiber backbone between edge campuses
    1. Target markets: energy sector clients, municipal contracts, enterprise AI hosting
    1. Scale to 5+ regional edge campuses across Louisiana and Gulf Coast
### Manufacturing & Supply Chain Notes
    - Node manufacturing lead time: 12 weeks factory-to-ship
    - NVIDIA Vera Rubin NVL72 availability: H2 2026 (confirmed CES 2026 — full production)
    - Bloom Energy server lead time: 6-12 months — order in parallel with site construction
    - CDU and cooling plant: Standard commercial HVAC procurement — 8-12 weeks
    - LUS Fiber service order: 60-90 day lead time for commercial service activation
    - All Phase 1 components commercially available as of Q1 2026
---
## PART C — KLFT / SKYCOMMAND TERMINOLOGY
Use this language when referencing the KLFT drone operations project in any document.
    - autonomous drone hub  ->  Gulf Coast Emergency Drone Deployment Hub
    - drone operations center  ->  AI-Coordinated Drone Operations Hub
    - KLFT drone project  ->  KLFT / SkyCommand — Gulf Coast Emergency Drone Deployment Hub
    - commercial drones  ->  autonomous air systems (AAS) or unmanned aircraft systems (UAS)
    - DJI  ->  REMOVED — do not reference. Platform: Skydio X10 + Skydio Dock only.
    - drone AI compute  ->  Jetson Orin NX 16GB (edge, dock-side) | NVIDIA L40S (Phase 3, MARLIE I networked)
---
## PART D — DEPLOYMENT GEOGRAPHY STRATEGY
> ADC 3K pod deployment sites are selected based on natural gas pipeline accessibility. Louisiana's natural gas infrastructure is the deployment map.
    - Primary deployment criterion: Active natural gas service at site (for Bloom Energy fuel cell integration)
    - Secondary criteria: Three-phase electrical service, broadband fiber, industrial/commercial zoning, physical security
    - Phase 1 hub: Lafayette — MARLIE I base station + Trappeys Cannery first pod site
    - Expansion corridor: I-10 corridor — Baton Rouge (east), Lake Charles (west), New Orleans (southeast)
    - Gulf Coast coverage target: Houma-Thibodaux (offshore energy support), Morgan City, Patterson (industrial)
    - Renewable overlay: Sites near New Iberia solar distribution range prioritized for solar+fuel cell hybrid systems
    - Airport hub: Lafayette Regional Airport (KLFT) — drone operations base, not a compute pod site
---
## PART E — ENERGY HIERARCHY (USE IN ALL DOCUMENTS)
    - Now (2026): Natural gas + Bloom Energy fuel cells as primary supplemental generation
    - Near-term: New Iberia solar arrays added to pod sites as daytime supplement
    - Mid-term: Biogas and renewable natural gas (RNG) blended into fuel cell supply
    - Long-term: Green hydrogen from Gulf Coast offshore wind — Bloom fuel cells are hydrogen-compatible
    - Baseline: LUS grid primary + diesel N+1 emergency backup maintained throughout all phases
*[Child: System Architecture Overview]*
> This is the master cross-reference document for all ADC infrastructure projects. Read this first to understand how MARLIE I, ADC 3K pods, KLFT/SkyCommand, New Iberia Solar, and the City of Lafayette connect as one ecosystem.
---
# ADC Infrastructure Ecosystem — How It All Connects
Advantage Design Construction operates an integrated AI infrastructure ecosystem across South Louisiana. Every project is designed to interconnect. MARLIE I is the permanent command center. ADC 3K pods are the deployable field units. KLFT/SkyCommand is the autonomous operations arm. New Iberia Solar is the renewable energy partner. The City of Lafayette — its power grid, fiber network, and airport — is the foundation that makes all of it possible.
---
## MARLIE I — Lafayette AI Factory (Base Station)
> MARLIE I is the permanent headquarters and primary compute facility. It is NOT a pod — it is a building-based AI factory at 1201 SE Evangeline Thruway, Lafayette LA.
    - Location: 1201 SE Evangeline Thruway, Lafayette, Louisiana
    - Role: HQ + NOC + primary AI compute + customer operations center
    - Hardware: NVIDIA Vera Rubin NVL72 racks (H2 2026 deployment target)
    - Cooling: Cold plate liquid cooling (CDU) with fan-assisted thermal management — direct-to-chip liquid, no immersion
    - Power: LUS grid (primary) + Bloom Energy fuel cells (supplemental) + diesel N+1 (emergency backup)
    - Connectivity: LUS Fiber — carrier-grade municipal fiber, already in place
    - NOC function: Remotely monitors and manages all ADC 3K pod deployments across Louisiana — no on-site staff at remote sites
MARLIE I cooling note: Cold plate CDU with fans represents the current state-of-the-art public-facing approach — proven, code-compliant, and well-understood by inspectors and lenders.
---
## ADC 3K — Deployable Edge Compute Pods
> ADC 3K pods are the manufactured containerized product line. Each pod is a self-contained, site-agnostic AI compute module deployed to remote Louisiana sites. All pods are managed remotely from MARLIE I NOC.
    - Form factor: 20-ft ISO shipping container — fully integrated, ships complete
    - Cooling: FULL IMMERSION (Engineered Fluids EC-110, single-phase) — no HVAC, no fans, no external cooling towers
    - Why immersion for Louisiana: Ambient temperatures regularly exceed 95°F with 90%+ humidity. Traditional air and even cold plate systems struggle with Louisiana climate. Immersion eliminates ambient air from the cooling equation entirely — GPU thermal performance is identical whether deployed in New Orleans in August or Shreveport in January.
    - Power: 480V AC active + 800V DC pre-wired. Bloom Energy fuel cell integration port standard on all units.
    - Deployment trigger: Natural gas pipeline accessibility. Pod sites are selected where Gulf Coast natural gas infrastructure provides reliable, low-cost fuel for on-site Bloom Energy generation.
    - Remote management: All pods networked back to MARLIE I NOC. No permanent on-site staff required.
    - First deployment: Trappeys Cannery — 1201 SE Evangeline Thruway. Metal warehouse structure. Pods drop in.
    - Dielectric fluid: Engineered Fluids EC-110. NEVER reference 3M Novec — discontinued.
---
## Louisiana Deployment Geography
ADC 3K pods follow the natural gas pipeline map. Louisiana has one of the densest natural gas distribution networks in the nation — the same infrastructure that powers the petrochemical industry also powers ADC pod sites. This gives ADC a cost and supply advantage that no out-of-state operator can match.
    - Primary hub: Lafayette (MARLIE I + Trappeys — Phase 1)
    - Expansion priority: Sites with existing natural gas service and industrial zoning along the I-10 corridor
    - Gulf Coast coverage: Baton Rouge, Lake Charles, New Orleans, Houma-Thibodaux corridor
    - Each pod site requires: natural gas service, three-phase electrical, broadband fiber, and basic security infrastructure
---
## KLFT / SkyCommand — Gulf Coast Emergency Drone Deployment Hub
> KLFT is not just an autonomous drone operations project. It is a Gulf Coast Emergency Drone Deployment Hub — AI-coordinated drone response for disasters, search and rescue, infrastructure inspection, and public safety operations across the Gulf Coast region, based at Lafayette Regional Airport.
    - Location: Lafayette Regional Airport (KLFT) — Lafayette, Louisiana
    - Platform: Skydio X10 + Skydio Dock (committed). DJI removed — Countering CCP Drones Act regulatory compliance.
    - Primary mission: Gulf Coast emergency response — hurricanes, flooding, industrial incidents, search and rescue
    - Secondary missions: Infrastructure inspection (pipelines, towers, bridges), precision agriculture, commercial logistics
    - AI compute: Jetson Orin NX 16GB at dock (edge inference). NVIDIA L40S (Phase 3 inference node, networked to MARLIE I).
    - Integration: MARLIE I NOC provides remote fleet management. SkyCommand platform scales to multi-site, multi-vehicle ops.
    - Lafayette connection: KLFT is a city asset. This project keeps AI drone infrastructure locally owned and operated — not contracted to out-of-state platforms.
---
## New Iberia Solar — Renewable Energy Partner
> A new solar manufacturing facility has been built in New Iberia, Louisiana (Iberia Parish, ~30 miles from Lafayette). ADC is committed to supporting this local industry as the renewable energy transition accelerates.
    - New Iberia, Louisiana — Iberia Parish, approximately 30 miles southwest of Lafayette
    - Significance: Local solar manufacturing capability means ADC can source panels regionally — shorter supply chain, economic development impact, alignment with Louisiana energy transition goals
    - Integration path: ADC 3K pod sites with roof or ground space can incorporate solar arrays sourced from New Iberia as supplemental generation — reducing natural gas consumption and qualifying for renewable energy credits
    - MARLIE I application: Rooftop or adjacent ground-mount solar at 1201 SE Evangeline Thruway — supplements Bloom Energy + LUS grid
    - Narrative value: Every investor deck and financing proposal should reference New Iberia solar as evidence of Louisiana-first supply chain commitment
---
## City of Lafayette — Infrastructure Foundation
Every ADC project is designed around Lafayette's existing infrastructure advantages. This is not incidental — it is strategic. Lafayette has built public infrastructure that most cities its size do not have, and ADC is purpose-built to leverage it.
    - LUS (Lafayette Utilities System): Municipal electric and fiber — low-cost power, carrier-grade fiber, local control
    - LUS Fiber: Direct fiber connectivity already in place at MARLIE I site — no construction required
    - Lafayette Regional Airport (KLFT): Municipal airport = city asset. KLFT/SkyCommand keeps drone AI infrastructure locally controlled
    - University of Louisiana Lafayette: AI research pipeline, workforce development, potential compute tenant
    - Economic incentives: ITEP, Quality Jobs, Enterprise Zone, LED FastStart — all available to ADC projects
    - Goal: Lafayette becomes the regional hub for Gulf Coast AI infrastructure — not a branch office of a Dallas or Atlanta firm
---
## How the Projects Reinforce Each Other
    - MARLIE I NOC manages all ADC 3K pod sites — more pods = more NOC revenue per fixed overhead
    - MARLIE I NOC manages KLFT drone fleet — same NOC, multiple revenue streams
    - ADC 3K pods at natural gas sites serve energy sector customers — same customers who benefit from KLFT pipeline inspection drones
    - New Iberia solar panels on pod sites reduce energy cost across entire fleet
    - Lafayette city partnerships create regulatory goodwill and preferred access to public infrastructure contracts
    - Every project creates local jobs, local tax revenue, local infrastructure — reinforcing the city partnership narrative
*[Child: Edge AI — What It Is and Why It Matters]*
# What Is Edge Computing?
Imagine you run a factory. Every second, your machines produce data — temperature readings, camera feeds, vibration sensors, quality checks. Right now, most companies send all that data to a big computer building hundreds of miles away (the "cloud") to be analyzed, then wait for the answer to come back.
That's like mailing a letter to get a yes or no answer. It works, but it's slow.
> Edge computing puts the brain RIGHT NEXT TO the work. Instead of sending data across the country, you process it on-site — in seconds, not minutes.
---
## The Three Places AI Can Live
Think of it like three rings getting closer and closer to where the actual work happens:
```plain text

┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   RING 1: THE CLOUD                                                │
│   ┌─────────────────────────────────────┐                          │
│   │  Amazon, Google, Microsoft           │                          │
│   │  Massive buildings, 1000s of miles   │  ← Cheap storage         │
│   │  away. Great for email & backups.    │  ← Slow for real-time    │
│   │  Terrible for split-second decisions │  ← Your data leaves      │
│   └─────────────────────────────────────┘                          │
│                                                                     │
│   RING 2: THE AI FACTORY                                           │
│   ┌─────────────────────────────────────┐                          │
│   │  MARLIE I, Willow Glen              │                          │
│   │  Regional hub. 50-100 miles away.   │  ← Big compute power     │
│   │  Handles heavy AI training.         │  ← Your region's brain   │
│   │  Feeds the edge nodes.              │  ← You control it        │
│   └─────────────────────────────────────┘                          │
│                                                                     │
│   RING 3: THE EDGE                                                 │
│   ┌─────────────────────────────────────┐                          │
│   │  ADC 3K Pod — ON YOUR PROPERTY      │                          │
│   │  Right next to your operation.      │  ← Instant decisions     │
│   │  Self-powered. Self-cooled.         │  ← Data never leaves     │
│   │  Managed remotely from MARLIE I.    │  ← Your building, our pod│
│   └─────────────────────────────────────┘                          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

```
Most companies today are stuck in Ring 1 — the cloud. They're paying Amazon or Google to hold their data and run their AI. That means:
    - Their sensitive data leaves their building
    - They're dependent on someone else's internet connection
    - They wait in line behind millions of other customers
    - If the internet goes down, their AI goes down
> Edge computing eliminates all four of those problems. The ADC 3K pod IS the edge.
---
## Why Edge Is Exploding Right Now
Three things changed in the last 2 years that made edge computing go from "nice idea" to "urgent need":
### 1. AI Models Got Small Enough to Deploy Anywhere
In 2023, running an AI model required a room full of servers. By 2026, NVIDIA's software (called NIMs — Neural Inference Microservices) lets you run powerful AI on a single GPU rack. A 20-foot container with 4 racks can now do what a whole building used to do.
### 2. Data Privacy Laws Got Serious
HIPAA (healthcare), ITAR (defense), CMMC (government contracts) — all of these now have strict rules about WHERE your data lives. The cloud doesn't cut it anymore for sensitive workloads. If your data crosses a state line, you might be in violation. Edge keeps data on-site.
### 3. Real-Time AI Needs Zero Delay
Self-driving vehicles, drone swarms, robotic surgery, oil rig safety monitoring — these can't wait 200 milliseconds for a cloud response. They need answers in under 10 milliseconds. That's only possible if the computer is in the same building — or the same parking lot.
---
## What This Means in Plain English
```plain text

THE OLD WAY (Cloud):
  Your cameras → Internet → Amazon's building in Virginia → Internet → Your screen
  Time: 200-500ms  |  Cost: Monthly cloud bill forever  |  Risk: Internet goes down = blind

THE NEW WAY (Edge — ADC 3K Pod):
  Your cameras → 50 feet of cable → Pod in your parking lot → Your screen
  Time: 5-10ms  |  Cost: Fixed hardware, you own it  |  Risk: Self-powered, runs during outages

```
> The edge isn't a new product for ADC. It's what the pod was BUILT to be. We just need to say it.
*[Child: Who Buys Edge AI — Customer Profiles]*
# Who Buys Edge AI — And Why They Pay Premium
Edge computing isn't for startups on a budget. It's for organizations with three things: sensitive data, real-time needs, and money. Here are the five customer segments that will buy ADC 3K pods as edge nodes.
---
## 1. Oil & Gas / Petrochemical
> Scott knows these people personally. 25 years in deepwater ROV operations. Same industry, new product.
### The Problem They Have
Every offshore platform, refinery, and pipeline corridor generates massive amounts of sensor data — pressure, flow rates, vibration, thermal imaging, subsea camera feeds. Right now, most of this data gets sent to Houston or the cloud for analysis. By the time the answer comes back, the anomaly that could have prevented a $50M blowout has already happened.
### What They Need
    - Real-time predictive maintenance — catch equipment failure BEFORE it happens
    - Autonomous inspection — AI analyzing camera feeds 24/7 without human fatigue
    - Data sovereignty — proprietary drilling and production data stays on-site
    - Works offshore and in remote locations — can't depend on fiber internet
### Why the Pod Fits
    - Self-powered (nat gas generator) — no grid dependency
    - Immersion cooled — works in Gulf Coast heat, desert, offshore platforms
    - Container form factor — crane it onto a platform or pad site
    - Managed from MARLIE I — 24/7 NOC monitoring, no on-site AI staff needed
### The Money
A single unplanned shutdown on an offshore platform costs $1-5M per day. A pod running predictive maintenance AI costs $50-80K/month managed. The ROI sells itself.
```plain text

    OFFSHORE PLATFORM — EDGE AI DEPLOYMENT

    ┌──────────────────────────────────────────┐
    │  PLATFORM DECK                            │
    │                                           │
    │   [Sensors] ──┐                           │
    │   [Cameras] ──┤                           │
    │   [Vibration]─┤    ┌─────────────────┐   │
    │   [Thermal] ──┼───→│  ADC 3K POD     │   │
    │   [Pressure]──┤    │  4 GPU racks    │   │
    │   [Flow] ────┘    │  Self-cooled     │   │
    │                    │  Self-powered    │   │
    │                    └────────┬────────┘   │
    │                             │             │
    │                    ┌────────▼────────┐   │
    │                    │ REAL-TIME ALERTS │   │
    │                    │ "Pump 3 bearing  │   │
    │                    │  failure in 72h" │   │
    │                    └─────────────────┘   │
    │                             │             │
    └─────────────────────────────┼─────────────┘
                                  │ VSAT uplink
                         ┌────────▼────────┐
                         │   MARLIE I NOC   │
                         │   Lafayette, LA  │
                         │  24/7 monitoring │
                         └─────────────────┘

```
---
## 2. Defense & Military
> Classified data cannot leave the building. Period. That's not a preference — it's the law.
### The Problem They Have
The Department of Defense needs AI for everything — drone surveillance analysis, logistics optimization, communications intelligence, predictive maintenance on vehicles and aircraft. But classified workloads cannot run on commercial cloud (AWS GovCloud has limits). They need on-base, air-gapped compute that they physically control.
### What They Need
    - SCIF-compatible enclosure — physically secured, no wireless emissions
    - Air-gapped operation — zero internet dependency for classified inference
    - Rapid deployment — ship a pod to a forward operating base in weeks, not months
    - Ruggedized — works in extreme heat, cold, dust, humidity
### Why the Pod Fits
    - 20-foot ISO container = military standard shipping size (fits on trucks, ships, aircraft)
    - Self-powered — diesel genset for forward bases with no grid
    - No HVAC dependency — immersion cooling works in desert and arctic
    - Managed or unmanaged — DoD can run it themselves or ADC manages remotely
### The Money
Defense contracts pay 3-5x commercial rates. A SCIF-rated edge AI pod could command $150-300K/month. Fort Polk, Barksdale AFB, NAS JRB New Orleans, and Camp Beauregard are all within 200 miles of Lafayette.
---
## 3. Healthcare Systems
> HIPAA says patient data must be protected. The easiest way to protect it? Never let it leave the hospital.
### The Problem They Have
AI is transforming medical imaging — radiology, pathology, dermatology. An AI can read an X-ray in 2 seconds with 95% accuracy. But hospitals are terrified of sending patient images to the cloud because of HIPAA liability. One breach = millions in fines. So most hospitals just... don't use AI yet.
### What They Need
    - On-premises AI inference — patient images never leave the building
    - Low latency — radiologist needs results during the exam, not after
    - HIPAA-compliant infrastructure — encrypted, audited, physically secured
    - Managed service — hospitals don't have GPU engineers on staff
### Why the Pod Fits
    - Deploy in hospital parking structure or utility yard — 50 feet from the imaging center
    - Fully managed from MARLIE I — hospital IT doesn't touch it
    - NVIDIA AI Enterprise certified NIMs for medical imaging are ready today
    - Self-powered backup — when the grid goes down during a hurricane, the AI stays up
### The Money
Hospital systems spend $2-5M/year on radiology outsourcing. A managed edge pod running AI-assisted imaging costs $40-60K/month. Ochsner Health (40+ facilities), Our Lady of Lourdes, LGMC — all within driving distance.
---
## 4. Manufacturing & Ports
> Quality inspection at the speed of the assembly line. Not tomorrow. Not in an hour. RIGHT NOW.
### The Problem They Have
Manufacturing plants run 24/7. Every product coming off the line needs quality inspection. Human inspectors miss things — they get tired, they blink, they take breaks. AI vision systems can inspect every single unit at full line speed. But the cloud adds 200ms of latency, which at high-speed production means missed units and wasted product.
### What They Need
    - Real-time visual inspection — camera to decision in under 10ms
    - Digital twin modeling — simulate production changes before implementing
    - Logistics optimization — container routing, warehouse robotics
    - On-site data — proprietary manufacturing processes stay proprietary
### Why the Pod Fits
    - Container sits on the factory floor or adjacent lot — zero network latency
    - Handles the heat and vibration of industrial environments
    - Scales with production — add another pod when you add another line
    - Port Fourchon, Port of New Orleans, I-10 industrial corridor — all ADC territory
### The Money
A single quality defect that reaches a customer costs 10-100x more than catching it on the line. Manufacturing AI inspection saves $1-10M/year per facility. Pod cost: $50-80K/month managed.
---
## 5. Sovereign AI — Foreign Governments & State Agencies
> Some countries legally CANNOT use American cloud providers. A pod is a turnkey sovereign AI node.
### The Problem They Have
Data sovereignty laws in the EU (GDPR), Middle East, Southeast Asia, and Latin America require that citizen data stays within national borders. Many governments want AI capabilities but cannot — by law — use AWS, Azure, or Google Cloud. They need physical hardware in their country, managed by a trusted partner.
### What They Need
    - Physical hardware on sovereign soil — legally required
    - Turnkey deployment — most countries don't have GPU infrastructure expertise
    - Managed remotely — ADC provides the expertise, country provides the location
    - Self-contained — many deployment sites have unreliable power and cooling
### Why the Pod Fits
    - Ship a container anywhere in the world — standard ISO shipping
    - Self-powered, self-cooled — works in any climate, any grid condition
    - MARLIE I manages it remotely — sovereign nation gets AI without building expertise
    - "Made in Lafayette, Louisiana" — American-built, American-managed, deployed globally
### The Money
Sovereign AI contracts are typically multi-year, government-funded, and premium-priced. A single sovereign deployment could be $3-5M/year. The Middle East and Southeast Asia are the hottest markets right now.
---
## Summary — The Edge Customer Matrix
```plain text

┌──────────────────┬───────────────┬──────────────┬──────────────────────────┐
│ CUSTOMER         │ WHY EDGE      │ POD/MONTH    │ ADC ADVANTAGE            │
├──────────────────┼───────────────┼──────────────┼──────────────────────────┤
│ Oil & Gas        │ Remote sites, │ $50-80K      │ Scott's 25yr network.    │
│                  │ real-time     │              │ Same industry, new tool. │
├──────────────────┼───────────────┼──────────────┼──────────────────────────┤
│ Defense          │ Classified    │ $150-300K    │ ISO container = mil-spec.│
│                  │ data, SCIF    │              │ 4 bases within 200 mi.   │
├──────────────────┼───────────────┼──────────────┼──────────────────────────┤
│ Healthcare       │ HIPAA, patient│ $40-60K      │ Ochsner, Lourdes,        │
│                  │ data on-prem  │              │ 40+ facilities nearby.   │
├──────────────────┼───────────────┼──────────────┼──────────────────────────┤
│ Manufacturing    │ Line-speed    │ $50-80K      │ I-10 corridor, ports,    │
│                  │ QA, zero lag  │              │ petrochemical plants.    │
├──────────────────┼───────────────┼──────────────┼──────────────────────────┤
│ Sovereign AI     │ Data must stay│ $250K+/mo    │ Ship globally, manage    │
│                  │ in-country    │              │ from Lafayette.          │
└──────────────────┴───────────────┴──────────────┴──────────────────────────┘

```
*[Child: The ADC 3K Pod — Your Edge AI Node]*
# The ADC 3K Pod Is Already an Edge Product
> We don't need to build a new product. We need to NAME the product we already have. The pod is a self-powered, self-cooled, remotely-managed edge AI node. That's not marketing spin — that's literally what it does.
---
## What Makes Something an "Edge" Product?
Here's the checklist. If a product does all five of these things, it's edge infrastructure:
```plain text

EDGE INFRASTRUCTURE CHECKLIST          ADC 3K POD
─────────────────────────────────      ──────────────────────
✅ 1. Deploys AT the customer site     40-ft ISO container, crane-ready
✅ 2. Runs WITHOUT cloud dependency    Self-powered (Bloom SOFC + solar + battery)
✅ 3. Processes data LOCALLY            GPU racks running NVIDIA AI Enterprise
✅ 4. Survives harsh environments      Liquid cooled, desiccant humidity control
✅ 5. Managed REMOTELY                 MARLIE I NOC, 24/7 monitoring

                    SCORE: 5 out of 5 — THIS IS AN EDGE PRODUCT

```
---
## How the Pod Works as an Edge Node
Let's walk through a real deployment — step by step — so anyone can understand it.
### Step 1: The Customer Has a Problem
A hospital in Baton Rouge wants to run AI on their radiology images. They can't send patient X-rays to Amazon's cloud because of HIPAA laws. They don't have GPU engineers on staff. They need a solution that works without changing how their hospital operates.
### Step 2: We Ship a Pod
We manufacture the pod at our facility in Lafayette. It's a 40-foot High Cube ISO container — the same kind you see on cargo ships. Inside: 10 NVL72 GPU racks (8 compute + 1 network + 1 storage), a liquid cooling loop with external dry cooler, 800V DC power system, networking equipment, and Novec 1230 fire suppression. Everything is pre-configured before it leaves our building.
```plain text

INSIDE AN ADC 3K EDGE POD
┌──────────────────────────────────────────────────────────────┐
│                   20-FOOT ISO CONTAINER                       │
│                                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ GPU RACK │  │ GPU RACK │  │ GPU RACK │  │ GPU RACK │    │
│  │  NVL72   │  │  NVL72   │  │  NVL72   │  │  NVL72   │    │
│  │ immersed │  │ immersed │  │ immersed │  │ immersed │    │
│  │ in fluid │  │ in fluid │  │ in fluid │  │ in fluid │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
│                                                               │
│  ┌─────────────────┐  ┌──────────┐  ┌───────────────────┐  │
│  │  POWER SYSTEM   │  │ COOLING  │  │  FIRE SUPPRESSION │  │
│  │  UPS + Transfer │  │  CDU +   │  │  VESDA + FK-5-1-12│  │
│  │  Switch         │  │  Dry     │  │  (clean agent,    │  │
│  │                 │  │  Cooler  │  │   safe for GPUs)   │  │
│  └─────────────────┘  └──────────┘  └───────────────────┘  │
│                                                               │
│  ← GAS IN    ← NETWORK IN    → EXHAUST OUT                  │
└──────────────────────────────────────────────────────────────┘

```
### Step 3: We Drop It On-Site
A flatbed truck delivers the pod to the hospital's utility yard. A crane sets it on a concrete pad. We connect three things: a natural gas line (for power), a network cable (for data), and a water line (for the cooling system's dry cooler). That's it. No construction. No HVAC installation. No building permits for a server room.
### Step 4: We Turn It On From Lafayette
Our team at MARLIE I — our network operations center in Lafayette — powers up the pod remotely. They configure the AI software (NVIDIA NIMs for medical imaging), run diagnostics, and hand the hospital a simple login: "Here's your dashboard. Your radiologists can now get AI-assisted reads in 2 seconds instead of sending films out for 24-hour turnaround."
### Step 5: We Manage It Forever
The hospital never touches the pod. MARLIE I monitors it 24/7 — temperature, power draw, GPU health, software updates, security patches. If a GPU fails, we dispatch a technician. If the hospital needs more compute, we ship another pod. The hospital's IT department does nothing.
```plain text

THE EDGE LIFECYCLE — HOW IT FLOWS

  MANUFACTURE           DEPLOY              OPERATE              SCALE
  ┌─────────┐          ┌─────────┐         ┌─────────┐         ┌─────────┐
  │ Build in │   ───→   │ Ship to │   ───→  │Manage   │   ───→  │ Add more│
  │Lafayette │          │customer │         │from     │         │ pods as │
  │ Pre-test │          │  site   │         │MARLIE I │         │ needed  │
  │ Pre-load │          │ 3 plugs │         │  24/7   │         │         │
  └─────────┘          └─────────┘         └─────────┘         └─────────┘
     2-4 weeks           1 day               Ongoing              2 weeks

```
---
## Edge vs. Cloud vs. AI Factory — When to Use Each
Not everything belongs at the edge. Here's the simple rule:
```plain text

┌──────────────────┬─────────────────────────┬────────────────────────┐
│                  │ USE THIS WHEN...         │ ADC PRODUCT            │
├──────────────────┼─────────────────────────┼────────────────────────┤
│ ☁️  CLOUD        │ You're a startup with no │ Not our business.      │
│ (Amazon/Google)  │ sensitive data and don't │ Let Amazon have it.    │
│                  │ need real-time speed.    │                        │
├──────────────────┼─────────────────────────┼────────────────────────┤
│ 🏭 AI FACTORY    │ You need massive compute │ MARLIE I               │
│ (Regional hub)   │ for AI training, or you  │ Willow Glen            │
│                  │ want colocation.         │                        │
├──────────────────┼─────────────────────────┼────────────────────────┤
│ 📦 EDGE          │ Data can't leave your    │ ADC 3K POD             │
│ (On your site)   │ building, you need       │ Shipped to your door.  │
│                  │ instant AI, or you're    │ Managed from ours.     │
│                  │ in a remote location.    │                        │
└──────────────────┴─────────────────────────┴────────────────────────┘

```
> The power of ADC's model: we don't just sell one ring. We sell all three. MARLIE I is the brain. The pods are the hands. The customer picks where they need compute, and we deliver it — in a building or in a box.
---
## The NVIDIA AI Enterprise Connection
NVIDIA makes the GPUs (the chips). But they also make the software that runs ON those chips in business environments. It's called NVIDIA AI Enterprise, and it has three tiers:
```plain text

NVIDIA AI ENTERPRISE — THREE TIERS

  CLOUD TIER          FACTORY TIER         EDGE TIER
  ┌─────────┐         ┌─────────┐         ┌─────────────┐
  │ Runs on  │         │ Runs on  │         │ Runs on     │
  │ Amazon   │         │ your own │         │ ADC 3K POD  │  ← THIS IS US
  │ Google   │         │ AI       │         │ at customer │
  │ Azure    │         │ factory  │         │ site        │
  └─────────┘         └─────────┘         └─────────────┘

  NVIDIA sells the software.
  ADC sells the HARDWARE + MANAGEMENT that runs it.
  Together = turnkey edge AI for any industry.

```
If ADC gets NVIDIA AI Enterprise certified, every pod we ship comes pre-loaded with enterprise-grade AI software. The customer doesn't need to figure out how to install AI — it's ready to go. That certification is the single biggest unlock for edge sales.
*[Child: NVIDIA Certification & Edge Go-To-Market]*
# NVIDIA Certification & Go-To-Market Path
What ADC needs to do to go from 'we build pods' to 'we sell NVIDIA-certified edge AI infrastructure.'
---
## Phase 1: NVIDIA Inception (Now)
NVIDIA Inception is their startup program. Free to join:
    - Access to NVIDIA engineering support
    - Hardware discounts on DGX and HGX systems
    - Co-marketing opportunities
    - Path to AI Enterprise certification
> File the Inception application THIS WEEK. Gateway to everything else.
### Application Language
ADC3K manufactures self-contained, immersion-cooled AI compute pods powered by on-site natural gas generation. We deploy edge AI infrastructure to oil & gas, defense, healthcare, and manufacturing customers across the Gulf South. We seek NVIDIA AI Enterprise certification for our ADC 3K pod product line to deliver turnkey edge AI solutions.
---
## Phase 2: AI Enterprise Certification (60-90 Days)
NVIDIA tests your hardware and validates their software stack runs correctly. Once certified:
    - Pods ship with pre-installed NVIDIA NIMs (inference microservices)
    - Customers get NVIDIA enterprise support alongside ADC management
    - ADC appears in NVIDIA partner directory
    - You can use the NVIDIA AI Enterprise Certified badge
### Certification Requirements
    1. Hardware validation -- GPU config, networking, cooling under load
    1. Software compatibility -- AI Enterprise stack passes all benchmarks
    1. Support agreement -- ADC commits to Tier 1 hardware support
    1. Training -- ADC team completes NVIDIA certification courses
---
## Phase 3: Edge Product Tiers
```plain text
ADC 3K EDGE PRODUCT LINE

TIER 1: EDGE INFERENCE POD
  2 GPU racks, inference-optimized
  For: Hospital, factory, single-site real-time AI
  Power: 100 kW | Price: $40-60K/month managed

TIER 2: EDGE COMPUTE POD
  4 GPU racks, inference + fine-tuning
  For: Companies customizing AI models on-site
  Power: 200 kW | Price: $80-120K/month managed

TIER 3: SOVEREIGN AI POD
  Full compute + air-gapped security + SCIF options
  For: Governments, military, classified workloads
  Power: 200 kW + redundant | Price: $150-300K/month managed
```
---
## Phase 4: Go-To-Market -- Who to Call First
### Tier A -- Warm Leads (Scott's Network)
    - Oil & gas operators Scott worked with -- 25 years of relationships
    - Offshore platform operators needing predictive maintenance AI
    - Pipeline companies along the Gulf Coast corridor
Phone calls, not cold emails. 'I used to run your ROV operations. Now I build the AI that replaces manual inspection.'
### Tier B -- Regional Healthcare
    - Ochsner Health System -- 40+ facilities, largest in Louisiana
    - Our Lady of Lourdes -- Lafayette, our backyard
    - LGMC, Baton Rouge General, Tulane Medical Center
Approach through LEDA or LED. Louisiana-built AI for Louisiana healthcare.
### Tier C -- Defense (Longer Cycle, Biggest Payoff)
    - Fort Polk (JRTC) -- 2 hours north
    - Barksdale AFB -- Shreveport
    - NAS JRB New Orleans
    - Camp Beauregard -- Louisiana National Guard HQ
12-18 month sales cycle. Multi-year, premium-priced contracts.
---
## The Pitch -- One Sentence
> We ship a self-powered, NVIDIA-certified AI computer to your parking lot, connect three cables, and manage it forever from our operations center in Lafayette. Your data never leaves your building. Your AI never goes down.
---
## Timeline
```plain text
WEEK 1-2:   File NVIDIA Inception application
WEEK 2-4:   Begin AI Enterprise certification
WEEK 4-8:   Build edge product tier specs and pricing
WEEK 4-12:  Certification testing and validation
WEEK 8-12:  First edge sales conversations (oil & gas)
WEEK 12-16: First edge pod deployment (pilot customer)
WEEK 16+:   Scale -- healthcare, defense, manufacturing, sovereign
```
*[Child: Edge vs. Cloud -- The Money Conversation]*
# Edge vs. Cloud -- The Money Conversation
When a customer asks 'why not just use AWS?' -- this is the answer.
---
## The Cloud Bill Problem
Cloud charges three ways, none get cheaper:
    1. Compute: 8 A100s on AWS = $214,000/year. Four racks = $856,000/year.
    1. Data transfer: 10TB/month = $10,440/year just to upload your own data.
    1. Storage: Monthly forever. More data = more cost. It never stops.
> Cloud bills go UP every year. Hardware costs go DOWN. Over 3 years, owning always wins.
---
## 3-Year Total Cost -- Side by Side
```plain text
3-YEAR TOTAL COST -- 4 GPU RACKS

                    CLOUD (AWS)      EDGE (ADC 3K POD)
Year 1              $890,440         $720,000
Year 2              $945,440         $720,000
Year 3              $1,002,440       $720,000
                    ----------       ----------
3-YEAR TOTAL        $2,838,320       $2,160,000

SAVINGS WITH EDGE:  $678,320 (24% less)

Plus: data sovereignty, 5ms vs 200ms latency,
runs during outages, no vendor lock-in
```
---
## ADC Revenue Per Pod
```plain text
ADC 3K EDGE POD -- UNIT ECONOMICS

Monthly managed fee:        $60,000 (Tier 2)

Costs:
  Hardware depreciation      $12,000 (3-yr straight line)
  Power (nat gas $0.04/kWh)  $5,800 (200 kW continuous)
  NOC allocation              $3,000 (shared monitoring)
  Maintenance reserve         $2,000
  Insurance + misc            $1,200
Total cost:                  $24,000/mo

GROSS MARGIN:  $36,000/mo = 60%
ANNUAL GROSS PROFIT PER POD: $432,000

10 PODS DEPLOYED:
  Revenue:      $7,200,000/year
  Gross Profit: $4,320,000/year
  Margin:       60%
```
---
## Why Big Companies Choose Edge
### 1. Control
Your AI on someone else's computer = they control pricing, terms, access. Own the hardware = own your destiny.
### 2. Compliance
HIPAA, GDPR, CMMC, ITAR, SOX -- all have data residency rules. Edge solves compliance by default. Data physically cannot leave.
### 3. Speed
Self-driving trucks can't wait 200ms. Factory robots can't wait for AWS. Edge AI: under 10ms.
### 4. Resilience
Internet down? Cloud down. Grid fails? Connection fails. Edge pod with own power runs through hurricanes.
### 5. Competitive Advantage
Same cloud = same speed as competitors. Edge = dedicated compute nobody shares. Your models, your data, your moat.
---
## The Investor Pitch
```plain text
ADC 3K: EDGE AI INFRASTRUCTURE

The market is moving AI from the cloud
to the customer's doorstep.

We build the doorstep.

  Manufactured in Lafayette, LA
  Self-powered, self-cooled, remotely managed
  NVIDIA AI Enterprise certified
  60% gross margin per deployed pod
  $4.3M annual gross profit at 10 pods
  Customers: Oil & Gas, Defense, Healthcare

Your data never leaves your building.
Your AI never goes down.
```
> PRE-GTC 2026 ARCHIVE: This folder references Bloom Energy and NVIDIA Inception strategy, both superseded by the neocloud/NPN strategy post-GTC March 2026. Kept for historical reference. Current strategy: memory/projects/neocloud_strategy.md
*[Child: Trappeys AI Center]*
> THE CORE PROJECT. Solar AI factory at former Trappeys Cannery, Lafayette LA. 112,500 sq ft across 4 buildings. 2.05 MW First Solar rooftop. Water tower cooling. Site walked 2026-03-21 -- all buildings structurally sound.
GPS: 30.21356N, 92.00163W  |  Acquisition: ~$1M  |  Half mile from MARLIE I  |  30 mi from First Solar
---
# Live Pages (adc3k.com)
  - /trappeys -- Landing page
  - /trappeys-campus -- Photo tour (4 buildings)
  - /trappeys-technology -- DSX stack + NVIDIA architecture
  - /trappeys-university -- UL Lafayette partnership
  - /trappeys-responders -- First responder drone ops
  - /trappeys-investors -- Investment case
  - /trappeys-plan -- Master plan (buildings, solar, phasing)
  - /trappeys-dsx-prep -- DSX Air input package (copy-paste ready)
  - /trappeys-presentation -- Pitch deck (28 slides)
  - /trappeys-gallery -- 56 numbered site photos for reference
---
# Buildings -- 112,500 sq ft Total Rooftop
## Rear High Ground -- 37,500 sq ft
150 x 250 ft. Tallest building. Connects via walkway to brick building (roof torn off but walls + metal repairable). ~1,276 solar panels = 676 kW.
## Middle High -- 22,500 sq ft
75 x 300 ft. Same height as Rear High. Wooden beams, roof good. Ready for solar panels. ~765 panels = 406 kW.
## Middle Low -- 30,000 sq ft
100 x 300 ft. ~2 ft lower than Middle High. Roof good, metal good. Extensive gas piping + fire suppression piping already installed. Gas heaters, huge trunk line. Could be primary compute space with elevated floors. ~1,020 panels = 541 kW.
## Front Lower -- 22,500 sq ft (on the water)
75 x 300 ft. Has vat holes in concrete floor -- perfect for cable risers and cooling plumbing. River views, park visible across bayou. Some roof sections off. NOT compute space -- this is the showcase, partner hub, tour stop, investor wow moment. ~765 panels = 406 kW.
---
# Solar -- 2.05 MW First Solar Rooftop
3,827 First Solar Series 7 TR1 panels across all 4 rooftops. Panels manufactured 30 miles away in New Iberia. 550W each, 19.7% efficiency, 0.3%/year degradation (industry best). 30-year warranty. Superior in humidity (+4% vs silicon) -- perfect for Lafayette.
  - 30% federal solar ITC + state credits -- government pays for most of it
  - 800V DC solar-direct to DSX bus possible (97% efficiency vs 92% AC path)
  - Plan: seal roofs > build platform/racking > mount panels
---
# Power -- 4-Layer Hierarchy
> Gas is PRIMARY. Solar is offset. Grid is sell-back only. We don't need the grid. We don't scare anybody.
  1. Solar -- primary offset, rooftop arrays, First Solar panels
  1. Natural Gas -- BACKBONE, carries main load 24/7, Henry Hub pricing
  1. Diesel Gensets -- emergency, on-site fuel, pipeline-independent
  1. Grid (LUS) -- SELL-BACK ONLY, excess goes back to grid, NOT a source
Gas confirmed on-site: trunk lines, city hub up the road, heaters throughout Middle Low.
---
# Water Tower -- Branding + Cooling
### Branding
THE landmark. First thing to paint. Dark navy blue. NVIDIA, ADC, First Solar, UL Lafayette, City of Lafayette logos. Visible from Evangeline Thruway/US 90. DO FIRST.
### Cooling (engineering innovation)
Repurpose as thermal buffer tank in liquid cooling loop. 15,000+ gallon elevated steel tank. Hot water from NVL72 racks pumps up, gravity-feeds cold water back down to CDUs (no pump needed on return). Tower is a giant radiator. Thermal mass = cooling UPS -- if pumps trip, gravity-feeds racks for 10-15 minutes.
100-year-old water tower repurposed as AI factory cooling infrastructure = magazine cover, NVIDIA case study material.
---
# Infrastructure Yard -- Concrete Pad
~28,000 sq ft heavy-duty concrete slab. NOT solar -- this is where the power plant goes.
  - Natural gas gensets (backbone, 24/7)
  - Transformer/switchgear yard (Eaton Beam Rubin DSX)
  - Dry coolers (backup to water tower)
  - Battery storage (future)
  - Diesel emergency genset
  - Visible from US 90 -- make it look professional, it's marketing
---
# Adjacent Infrastructure -- Already There
  - LUS Pin Hook Substation (Curtis Rodemacher) -- right next door, established
  - Public Works -- next door, city uses area for vehicle parking. Infrastructure zone, NOT residential.
  - Gas infrastructure -- confirmed on site. Trunk line, city hub up the road.
  - ATMOS Energy -- gas utility hub visible from Pinhook
  - Water department -- across street on US 90
  - City sewer -- across street, permitted discharge path
  - KLFT airport -- control tower visible from site
  - Park across the river -- visible from Front Lower
---
# Front Building -- Partner Hub
Restore brick facade. Convert loading bays to entrance/lobby. This is the FRONT DOOR.
  - ADC -- operations, reception, visitor intake
  - NVIDIA -- regional presence, certification lab
  - UL Lafayette -- research liaison, student workspace
  - First Solar -- O&M monitoring for rooftop arrays
  - City of Lafayette -- smart city coordination
  - Shared conference room -- partner meetings, investor tours
---
# Phased Buildout
  - Phase 3 (start): 4 racks, 288 GPUs, 520 kW IT. Solar + 1 MW gas genset.
  - Phase 4: 8 racks, 576 GPUs, 1 MW IT. Solar + 1.5 MW gas.
  - Phase 5: 20 racks, 1,440 GPUs, 2.6 MW IT. Solar + 3 MW gas.
  - Phase 6: 36 racks, 2,592 GPUs, 4.7 MW IT. Solar + 6 MW gas.
  - Phase 7: 50+ racks, 3,600+ GPUs, 6.5+ MW IT. Full power yard.
---
# Incentive Stack
  - 45% historic tax credits (federal 20% + state 25%) on rehab costs
  - 30% federal solar ITC on panels
  - 10-year property tax abatement (ITEP -- must file BEFORE groundbreaking)
  - 20-year Act 730 sales tax exemption ($200M+, 50 jobs)
  - NSF/DOE grants through UL Lafayette partnership ($28-55M+ potential)
  - LED FastStart -- FREE customized workforce training
---
# Business Documents (in repo)
  - business-model/vendor-procurement-matrix.md -- full US vendor matrix, primary + backup, Phase 1 budget ($1.1-1.7M)
  - business-model/trappeys-electrical-architecture.md -- 800V DC electrical design
  - business-model/token-economics.md -- raw cost $0.004/M, ADC pricing $0.20-$150/M, 95%+ margins
  - business-model/power-economics.md -- Phase 1 $0.058-0.068/kWh
  - business-model/capex-model.md -- capital expenditure model
---
# Vendor Strategy (in Notion)
Full vendor tiers under Vendor & Partner Strategy:
  - Tier 1 -- must-have hardware (NVIDIA, Atmos, LUS, Cat, Bloom, Vertiv/CoolIT)
  - Tier 2 -- operational partners & professional services (PE, FPE, structural, EPC, GC, legal, insurance)
  - Tier 3 -- government & institutional (LED, City, UL Lafayette, DOE, EDA)
---
# Action Items
  - [ ] Site LOI -- secure the property (~$1M)
  - [ ] ITEP filing -- call LED (Kristin Johnson, 225-342-2083). Must file BEFORE groundbreaking.
  - [ ] NPN registration -- 5-minute web form
  - [ ] First Solar outreach -- modulesales@firstsolar.com / 419-662-6899
  - [ ] UL Lafayette intro -- Dr. Ramesh Kolluru via LEDA warm intro
  - [ ] Structural engineer -- roof load analysis before solar
  - [ ] Environmental consultant -- Phase I ESA before closing
  - [ ] City council presentation -- schedule meeting
  - [ ] Water tower rendering -- Kontext edit of real photo
  - [ ] DSX Air trial -- inputs ready at /trappeys-dsx-prep
---
Last updated: 2026-03-21. Full details in memory/projects/trappeys.md (24 KB).
*[Child: 01 -- Investment Thesis]*
> THE CORE PROJECT. Solar AI factory at former Trappeys Cannery, Lafayette LA. Proof of concept for the Louisiana AI network.
Content source: Main page above + memory/projects/trappeys.md
## Key Points
    - 112,500 sq ft across 4 buildings -- existing industrial structures
    - 2.05 MW First Solar rooftop array (3,827 panels, manufactured 30 mi away)
    - Acquisition ~$1M -- historic cannery, half mile from MARLIE I
    - 45-55% historic tax credits on rehab costs (federal 20% + state 25-35%)
    - Proof of concept: earn NVIDIA certification, validate vendor stack, then scale to Willow Glen
    - UL Lafayette anchor tenant -- workforce, grants, credibility
*[Child: 02 -- Hardware: NVIDIA Vera Rubin Platform]*
> NVIDIA technology stack for Trappeys -- same as Willow Glen, smaller initial scale.
## Platform
    - Vera Rubin NVL72 (72 GPUs/rack, 130 kW, liquid cooled)
    - Quantum InfiniBand (400 Gb/s per GPU)
    - Dynamo 1.0 (7x performance on same hardware)
    - Groq 3 LPX decode (5-10x revenue per MW)
    - Eaton Beam Rubin DSX (800V DC, co-designed with NVIDIA)
## Phased Rack Count
    - Phase 3 (start): 4 racks, 288 GPUs, 520 kW IT
    - Phase 5: 20 racks, 1,440 GPUs, 2.6 MW IT
    - Phase 7: 50+ racks, 3,600+ GPUs, 6.5+ MW IT
*[Child: 03 -- Site & Building Specs]*
> Trappeys Cannery -- Lafayette, LA. 4 buildings on the Vermilion River.
GPS: 30.21356N, 92.00163W | Acquisition: ~$1M | Half mile from MARLIE I
## Buildings -- 112,500 sq ft Total
    - Rear High Ground: 37,500 sq ft (150x250). Tallest building. ~1,275 panels.
    - Middle High: 22,500 sq ft (75x300). Wooden beams, roof good. ~765 panels.
    - Middle Low: 30,000 sq ft (100x300). Gas piping + fire suppression already in place. ~1,020 panels.
    - Front Lower: 22,500 sq ft (75x300). Vat holes = cable risers. River views. ~765 panels.
## Infrastructure Yard
~28,000 sq ft heavy-duty concrete slab. Gas gensets, transformer/switchgear, dry coolers, battery storage.
## Water Tower
15,000+ gallon elevated steel tank. Repurpose as thermal buffer in liquid cooling loop. Branding landmark.
*[Child: 04 -- Government Funding Stack]*
> Incentive stack for Trappeys -- historic tax credits are the differentiator.
## Programs
    - 45% historic tax credits (federal 20% + state 25%) on rehab costs
    - 30% federal solar ITC on panels
    - 10-year property tax abatement (ITEP -- must file BEFORE groundbreaking)
    - 20-year Act 730 sales tax exemption ($200M+, 50 jobs)
    - NSF/DOE grants through UL Lafayette partnership ($28-55M+ potential)
    - LED FastStart -- FREE customized workforce training
*[Child: 05 -- Infrastructure Partners]*
> Vendor stack for Trappeys. Prove them here, scale them to Willow Glen.
## Partners
    - First Solar -- TR1 panels, rooftop mount. Factory 30 mi away in New Iberia.
    - Louisiana Cat -- gensets, switchgear. New Iberia.
    - Eaton -- Beam Rubin DSX 800V DC distribution
    - ATMOS Energy -- gas supply confirmed on-site
    - LUS -- sell-back only grid connection. Pin Hook substation next door.
    - UL Lafayette -- research liaison, student workspace, grant co-applicant
    - City of Lafayette -- smart city coordination
*[Child: 06 -- ADC3K Credentials]*
> ADC qualifications and track record.
Same credentials as MARLIE I and Willow Glen sections. See adc3k.com.
## Key Credentials
    - Scott Tomsu -- 25+ year ROV Superintendent, deepwater robotics worldwide
    - FAA Private Pilot, IMCA ROV Supervisor, Electronic Technician, Commercial Diver
    - FuelTech engine management certified
    - NVIDIA Partner Network registered
    - ADC3K.com live with full project portfolio
*[Child: 07 -- Louisiana AI Network: Multi-Site Vision]*
> Trappeys is the proof of concept. Willow Glen is the flagship.
## Network Role
    - Trappeys = UL Lafayette anchor | 29 MW ceiling | Proof of concept
    - Willow Glen = LSU anchor | 260 MW ceiling | Flagship
    - MARLIE I = Backup NOC, R&D, edge compute (half mile from Trappeys)
    - KLFT 1.1 = Autonomous airspace ops hub (control tower visible from site)
Every vendor who helps on Trappeys earns their place on Willow Glen.
*[Child: 08 -- Contact & Next Steps]*
> Action items for Trappeys acquisition and buildout.
## Immediate Actions
    - Site LOI -- secure the property (~$1M)
    - ITEP filing -- call LED (Kristin Johnson, 225-342-2083). Must file BEFORE groundbreaking.
    - NPN registration -- 5-minute web form
    - First Solar outreach -- modulesales@firstsolar.com / 419-662-6899
    - UL Lafayette intro -- Dr. Ramesh Kolluru via LEDA warm intro
    - Structural engineer -- roof load analysis before solar
    - Environmental consultant -- Phase I ESA before closing
    - City council presentation -- schedule meeting
## Contact
Scott Tomsu -- scott@adc3k.com -- adc3k.com
*[Child: 09 -- Financial Architecture & ROI]*
> Trappeys financial model. Smaller scale than Willow Glen, faster to revenue.
## Phased Revenue
    - Phase 3 (start): 4 racks | 520 kW IT | Solar + 1 MW gas
    - Phase 5: 20 racks | 2.6 MW IT | Solar + 3 MW gas
    - Phase 7: 50+ racks | 6.5+ MW IT | Full power yard
---
## Trappeys vs Willow Glen
    - Trappeys: $4.5M start | $82M Y5 | 225 racks | 29 MW | $47M net 5yr
    - Willow Glen: $8M start | $360M Y5 | 1,000 racks | 130 MW | $128M net 5yr
    - COMBINED: $12.5M start | $442M Y5 | 1,225 racks | 159 MW | $175M net 5yr
*[Child: 🏗️ ADC 3K — Project Command Center]*
| Gate | Description | Target | Status |
| P-1 | Provisional patent filed | Week 6 | 🟡 Disclosure ready — needs counsel |
| N-1 | NVIDIA Inception accepted | Week 6 | 🟡 Application package ready — SUBMIT NOW |
| C-1 | Cooling vendor RFI responses received | Week 8 | 🟡 Cover emails ready — SEND NOW |
| H-1 | Lab hardware ordered (D1 decision) | Week 3 | 🔴 BOM ready — no PO issued |
| L-1 | Site LOI executed | Week 12 | 🔴 Site package ready — no conversations started |
| S-1 | Pilot customer LOI signed | Week 12 | 🔴 LOI template ready — no conversations started |
---
> TWO-PRODUCT MODEL — READ FIRST

ADC has two distinct products. Do not conflate them.

MARLIE I = Permanent AI Factory building at 1201 SE Evangeline Thruway, Lafayette LA. CDU liquid cooling, NVL72 racks, Bloom Energy + LUS grid power. This is the HQ, NOC, and primary compute facility.

ADC 3K = Manufactured containerized AI compute pod. 40-ft ISO container. Immersion cooling (Engineered Fluids EC-110). Deployed to remote sites. No HVAC required. Networked back to MARLIE I. This is the PRODUCT that MARLIE I manufactures and deploys.

All engineering in this Command Center labeled 'MARLIE I scope' refers to the building. ADC 3K pods have their own separate cooling, power, and deployment spec.
> ADC 3K POD — ALL CONTENT
Live pages:  adc3k.com/adc3k-pod  +  adc3k.com/adc3k-pod-spec
Manufacturing strategy:  ADC Manufacturing -- Pod Factory Strategy
GTM / sales angle:  The ADC 3K Pod — Your Edge AI Node
Engineering specs:  Pod Swarm Engineering Suite
---
---
## 🚀 Monday Morning Priority List
  1. Submit NVIDIA Inception — ADC3K_NVIDIA_Inception_Application_Package_Rev1.docx · Portal: nvidia.com/en-us/startups · 15 minutes
  1. Send cooling vendor RFIs — ADC3K_Cooling_Vendor_RFI_Outreach_Pack_Rev1.docx · Attach ADC-3K-Cooling-Vendor-RFI.html to all 4 emails
  1. Deliver patent disclosure to counsel — ADC3K_Patent_Disclosure_Rev1.docx · Attorney-Client Privileged · Target provisional filing Q2 2026
  1. Send pitch deck to 2 investors — ADC3K_Investor_Pitch_Deck_Rev1.pptx + ADC3K_Financial_Model_Rev1.xlsx · Use ADC3K_Investor_Outreach_Email_Pack_Rev1.docx for targeting
  1. Start site conversations — ADC3K_Phase1_Site_Assessment_Package_Rev1.docx · Call Port of Iberia + LEDA + one industrial park contact
  1. File ITEP application BEFORE any construction — ADC3K_Louisiana_Incentive_Stack_Brief_Rev1.docx §3 · opportunitylouisiana.gov · Do this at site LOI execution
---
## ⚠️ Critical Flags for Next Session
  - Financial model needs update: Louisiana corporate tax rate is now 5.5% (not ~25% blended). IRR is higher than currently modeled — update Assumptions tab before next investor meeting
  - HB 827 threshold: ADC Phase 1 alone (~$19–30M) is below the $200M eligibility threshold. Pursue parish-level PILOT agreement as alternative. Brief investors honestly.
  - ITEP timing: Must file BEFORE breaking ground. Non-negotiable. Tie to site LOI execution.
  - NVIDIA Inception eligibility: ADC Inc. founded 2003 — frame ADC-3K as the AI infrastructure division launched 2025/2026 to satisfy the <10-year rule.
---
## 🌐 Website Build (V3 — March 1, 2026)
File: ADC-3K-Master-Website-V3.html (~728 KB, single-file SPA)
Status: Production-ready, 10-page site with embedded images
Branding: ADC-3K POD (global rename complete)
Contact: (337) 780-1535 / scott@adc3k.com / Data Center Design Professional
Full build log, edit history, and source image inventory:
*[Child: Master Task Tracker]*
*[Child: Pod Swarm Engineering Suite]*
> MARLIE I engineering specs — NVL72 racks, CDU liquid cooling, PDU layouts, network topology, RunPod API. All docs apply to the permanent building at 1201 SE Evangeline. ADC 3K pods use immersion cooling — separate spec required.
---
## Contents
    - NVL72 rack configurations and cable plans
    - CDU liquid cooling schematics
    - Power distribution unit layouts
    - Network topology diagrams
    - RunPod API integration notes
*[Child: NVL72 Rack Configuration & Cable Plans]*
> NVIDIA Vera Rubin NVL72 — 72 Rubin GPUs + 36 Vera CPUs per rack. 3.6 ExaFLOPS NVFP4. 100% liquid cooled. Full production H2 2026.
---
## Phase 1 Layout — 22 x 35 ft Floor (770 sq ft)
      - Total racks: 16 NVL72 units
      - Arrangement: Row A (8 racks) + Row B (8 racks) — hot aisle contained between rows
      - Walk-through: Cold aisle access front and rear — sealed hot aisle center
      - Aggregate compute: 57.6 ExaFLOPS NVFP4
      - Aggregate memory BW: 260 TB/s
---
## Per-Rack Specs (NVL72)
      - GPUs: 72x Rubin GPU — 36 per NVLink domain, 2 domains per rack
      - CPUs: 36x Vera CPU — 88 Olympus Arm cores (Armv9.2) each, 1.5 TB LPDDR5X, 1.2 TB/s memory BW per CPU
      - NVLink 6 Switches: 9x switch trays per rack — 28.8 TB/s per tray, 260 TB/s aggregate, in-network SHARP FP8 compute
      - Memory: HBM4 — 288 GB per Rubin GPU, 20.7 TB total per NVL72 rack, 1.58 PB/s aggregate bandwidth
      - Power per rack: TDP not yet published by NVIDIA — contact NVIDIA Enterprise Sales for facility planning specs
      - Cooling: Rear-door CDU manifold — 100% liquid, no air cooling
---
## Cable Plans
### NVLink Fabric (Intra-rack)
      - Topology: NVLink 6 Switch — full mesh within rack via 9-switch rail
      - Cable type: NVIDIA NVLink optical cables — pre-routed at factory
      - Field cabling required: None for NVLink intra-rack
---
### InfiniBand NDR (Inter-rack)
      - NIC: ConnectX-9 SuperNIC — 1.6 Tb/s per adapter (800 Gb/s per port) — >144 adapters per NVL72
      - Fabric: NDR400 InfiniBand — 400 Gb/s per port
      - Switch: NVIDIA Quantum-3 InfiniBand — top-of-rack or end-of-row
      - Cable type: NVIDIA Quantum HDR/NDR DAC or optical — 2m intra-row, 5m cross-row
      - Total uplinks: 16 racks x 2 ports = 32 uplinks to spine
---
### Ethernet Management (BlueField-4 DPU)
      - DPU: BlueField-4 — 1x per NVL72 — OOB management + storage offload
      - Uplink: 10GbE management — 1 cable per rack to management switch
      - Switch: Dedicated 24-port 10GbE management switch in network core
---
## Rack Numbering Convention
```plain text
Row A: A01 A02 A03 A04 A05 A06 A07 A08  (cold aisle front)
              [sealed hot aisle]
Row B: B01 B02 B03 B04 B05 B06 B07 B08  (cold aisle rear)

Network Core: NC01 (north end, near entry)
CDU Manifold: Runs along exterior north wall
```
---
## NVIDIA Field Resources
      - DGX-Ready colocation checklist: developer.nvidia.com/dgx-ready-data-center
      - NVL72 power + cooling specs: Contact NVIDIA Enterprise Sales
      - Field installation: NVIDIA-certified solution architect required
> SCOPE: This document applies to MARLIE I — the permanent AI Factory at 1201 SE Evangeline Thruway. NOT applicable to ADC 3K container pods, which use immersion cooling and a separate architecture.
---
> UPDATED 2026-03-23 -- POST-GTC REWRITE
## NVL72 Rack -- Vera Rubin Platform (December 2026 availability via HPE)
### Per Rack:
      - 72 NVIDIA Rubin GPUs
      - 36 NVIDIA Vera CPUs
      - 9 NVLink 6 switches (6th generation)
      - ConnectX-9 SuperNIC (1.6 Tb/s)
      - BlueField-4 DPUs
      - HBM4: 288 GB per GPU
      - Power: 130 kW per rack
      - Cooling: Direct-to-chip liquid, 45C hot water
      - Power input: 800V DC (Eaton Beam Rubin DSX)
      - Internal conversion: 64:1 LLC (800V -> 12V, 98% efficient, built-in)
### Rack Counts by Site:
Willow Glen: Phase 1 = 10 racks (8 VR + 2 Groq), Max = 2,000+, IT Power = 260 MW
MARLIE I: Phase 1 = 8 racks (4 per floor), Max = 8, IT Power = 1.04 MW
Trappeys: Phase 1 = 4 racks, Max = 225, IT Power = 29 MW
ADC 3K Pod: 1-2 per container, Max = 2, IT Power = 130-260 kW
### Cable Plan (per rack):
      - NVLink 6: Factory-integrated (intra-rack, do not touch)
      - InfiniBand: Quantum-X800 switches, 800 Gb/s per port
      - Ethernet: Spectrum-X, BlueField-4 DPU per node
      - Management: 10GbE OOB to NOC
      - Power: Single 800V DC feed from Eaton bus
### Multi-Vendor Future:
      - Primary: NVIDIA Vera Rubin NVL72
      - Future: Tesla Terafab chips (when available)
      - Future: AMD Instinct (if competitive)
Pod architecture is chip-agnostic at the facility level -- 800V DC and liquid cooling work for any vendor.
---
> WARNING (2026-03-24): Pre-GTC content above says 16 racks and InfiniBand NDR/Quantum-3. CORRECT specs are in the POST-GTC section: 8 racks per floor at MARLIE I, Quantum-X800 (800 Gb/s), 130 kW per rack.
*[Child: CDU Liquid Cooling Schematics]*
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
*[Child: Power Distribution Unit Layouts]*
> UPDATED 2026-03-23 -- POST-GTC REWRITE
## Power Architecture -- 800V DC Native (ALL Sites)
### 4-Layer Power Hierarchy (LOCKED):
Layer 1: Solar (First Solar TR1) -- Primary offset
Layer 2: Natural Gas (Henry Hub) -- Backbone 24/7
Layer 3: Diesel Gensets -- Emergency backup
Layer 4: Grid -- SELL-BACK ONLY (Willow Glen: Entergy, Lafayette: LUS)
> Grid is NEVER for consumption. Gas is ALWAYS running. Bloom Energy is NOT in the power stack. REMOVED post-GTC.
### Power Chain:
Gas/Solar -> Generator/Panels -> Eaton Beam Rubin DSX Rectifier (AC->800V DC) -> 800V DC Bus -> Eaton Busway -> Rack PDU (Eaton HDX G4) -> 64:1 LLC Converter (built into NVIDIA rack) -> 12V DC -> GPU
### Per-Site Power:
Willow Glen: 2x Cat CG260-16 (2.8 MW, H2-ready), 400+ acres ground mount solar, Sell-back to Entergy, Phase 1 IT = 1.3 MW (10 racks)
MARLIE I: 2x Cat G3520C (1.5 MW), 300 kW rooftop + ground solar, LUS backup, Phase 1 IT = 1.04 MW (8 racks)
Trappeys: 2x Cat G3520C (1.5 MW), 2.05 MW rooftop (3,731 panels), LUS sell-back, Phase 1 IT = 520 kW (4 racks)
ADC 3K Pod: 1x portable genset (250-500 kW), Optional roof panels, Optional grid tie, Phase 1 IT = 130-260 kW (1-2 racks)
### ADC 3K Pod Power:
      - Self-contained 800V DC system in 40-ft container
      - Portable natural gas generator (field gas available at oil field sites)
      - Eaton Beam Rubin DSX rectifier (containerized)
      - Optional solar panels on container roof
      - Optional grid tie for urban deployments
      - 4-layer hierarchy applies to EVERY deployment
---
*[Child: Network Topology Diagrams]*
> UPDATED 2026-03-23 -- POST-GTC REWRITE
## Network Architecture -- Hub and Spoke
### Fabric 1: NVLink 6 (Intra-Rack)
      - 6th generation NVLink
      - 260 TB/s aggregate bandwidth per rack
      - Factory-integrated -- DO NOT modify
### Fabric 2: InfiniBand (Inter-Rack, Intra-Site)
      - NVIDIA Quantum-X800 switches
      - 144 ports x 800 Gb/s per switch
      - Willow Glen: Full fat-tree topology (PRIMARY compute fabric)
      - MARLIE I: Single spine switch (8 racks)
      - ADC 3K Pod: No InfiniBand (single rack = NVLink only)
### Fabric 3: Ethernet (Services + WAN)
      - NVIDIA Spectrum-X (Spectrum-6 switches)
      - BlueField-4 DPU per node
      - Site-to-site: Dedicated fiber (Willow Glen <-> MARLIE I, 60 mi)
      - Remote pods: Starlink or cellular backhaul
      - LUS Fiber: 100GbE municipal fiber for MARLIE I/Trappeys (0.8 mi)
### Fabric 4: Management (OOB)
      - 10GbE out-of-band management
      - WireGuard/Tailscale mesh VPN across all sites
      - Mission Control dashboard at Willow Glen NOC
      - Backup NOC at MARLIE I
### Fleet Orchestration:
      - NVIDIA Run:AI for workload scheduling across all nodes
      - NVIDIA Dynamo 1.0 for inference optimization (7x performance)
      - Mission Control AI (ADC-built) for autonomous operations
      - NVIDIA Base Command Manager for cluster management
### Hub-Spoke Connectivity:
Willow Glen <-> MARLIE I: Dedicated fiber, 100 Gbps (Management only, NOT InfiniBand)
Willow Glen <-> Trappeys: Dedicated fiber, 100 Gbps (Via Lafayette fiber)
Willow Glen <-> Remote Pods: Starlink/VSAT, 100-500 Mbps (Inference results only)
MARLIE I <-> Trappeys: LUS Fiber, 10 Gbps (0.5 mi)
---
*[Child: RunPod API Integration Notes]*
> Mission Control manages RunPod cloud GPU pods via GraphQL API. IntegrationAgent dispatches via runpod skill. When MARLIE I goes live, on-prem racks replace RunPod cloud as primary.
---
## Current Setup — RunPod Cloud
      - Endpoint: https://api.runpod.io/graphql
      - Auth: Bearer token — RUNPOD_API_KEY in .venv/.env
      - Skill: skills/builtin/runpod.py — list / start / stop / terminate
      - Planner patterns: list pods | pod status | start pod | stop pod | terminate pod
---
## GraphQL Operations
### List Pods
```graphql
query {
  myself {
    pods {
      id name status
      runtime { uptimeInSeconds gpus { id gpuUtilPercent } }
      machine { gpuDisplayName }
    }
  }
}
```
### Start Pod
```graphql
mutation {
  podResume(input: { podId: "POD_ID", gpuCount: 1 }) {
    id status
  }
}
```
### Stop Pod
```graphql
mutation {
  podStop(input: { podId: "POD_ID" }) {
    id status
  }
}
```
---
## Mission Control Flow
      - Chat trigger: "list pods" / "start pod XYZ" / "stop pod XYZ"
      - Planner: Regex fast-path -> IntegrationAgent -> runpod skill
      - SSE stream: /tasks/{id}/stream — live step events during pod ops
      - Dashboard: Mission Control HQ at http://localhost:8000
---
## MARLIE I Transition Plan (H2 2026)
> When NVL72 racks go live, on-prem becomes primary. RunPod cloud is overflow. Mission Control routes by cost/latency/availability.
      - Phase 1 (now): RunPod cloud — dev/test workloads
      - Phase 2 (H2 2026): MARLIE I on-prem — production inference + training
      - Phase 3: Hybrid routing — Mission Control schedules across on-prem + cloud
---
## On-Prem API Design (Future)
      - Protocol: OpenAI-compatible REST — drop-in for cloud providers
      - Auth: API key per customer — managed by Mission Control
      - Billing: Per-GPU-hour metering via PDU current sensors
      - Scheduler: OrchestratorAgent — job queue, priority, multi-tenant isolation
```plain text
POST /v1/chat/completions    -- inference
POST /v1/embeddings         -- embeddings
GET  /v1/models             -- available models
GET  /v1/pods               -- active compute pods (internal)
POST /v1/jobs               -- batch job submission
```
---
> UPDATED 2026-03-23 -- POST-GTC REWRITE
RunPod remains the cloud GPU provider for Phase 0 (pre-facility). The existing GraphQL integration and Mission Control planner patterns are still valid.
### Current Status:
      - RunPod balance: ~$184
      - Network volume: aido-workspace (250GB, US-TX-3)
      - Active pod: ml4cl3icn37ys1 (L40S, EXITED)
      - Image gen endpoints: FLUX Schnell + Kontext (live on RunPod Hub)
### Transition Plan (unchanged):
      - Phase 0: RunPod cloud (NOW)
      - Phase 1: On-prem at MARLIE I (H2 2026 when Vera Rubin ships Dec 2026)
      - Phase 2: Hybrid (Willow Glen primary + RunPod overflow)
      - Phase 3: Full on-prem fleet (Willow Glen + MARLIE I + pods)
### Fleet Management Stack:
      - NVIDIA Run:AI -- workload orchestration across all on-prem nodes
      - NVIDIA Dynamo 1.0 -- inference optimization (7x performance boost)
      - NVIDIA Base Command Manager -- cluster lifecycle management
      - Mission Control AI (ADC-built) -- autonomous operations, monitoring, SSE dashboard
      - NVIDIA Mission Control (HPE offering) -- available 2026, evaluate for integration
*[Child: Pod Swarm Architecture — Document Index]*
*[Child: 🎯 Pod Swarm — Next Session Command Prompt]*
> ADC 3K session startup prompt. Copy/paste at the start of any new Claude session on ADC 3K pod engineering or deployment.
## COPY FROM HERE
You are the lead infrastructure engineer for ADC 3K — Advantage Design Construction containerized AI compute pod product line. Owner: Scott Tomsu, Lafayette, Louisiana.
### ADC 3K Product
        - 40-ft High Cube ISO container — manufactured AI compute pod, deployed to remote sites
        - Cooling: Direct-to-chip liquid cooling (NVIDIA reference). External dry cooler. No immersion, no HVAC. PUE target: 1.03
        - Power: 800V DC native. Bloom SOFC primary. Dual Bloom + CNG backup per site. No diesel — network redundancy via distributed sites.
        - Networked back to MARLIE I HQ at 1201 SE Evangeline Thruway
### First Deployment — Trappeys Cannery
        - Metal warehouse structure. Pods drop into bays, no structural modifications needed.
        - Status: Planning. No hardware ordered, no LOI signed.
### GPU Platform
        - NVIDIA Vera Rubin NVL72 — H2 2026. TDP NOT confirmed — all sizing from analyst estimates.
        - Blackwell/GB200/GB300 RETIRED. Do not reference.
### Open Investor Items (5 open)
        - 1. Customer LOI  2. NVIDIA TDP confirmation  3. HB 827 PILOT  4. CapEx reconciliation  5. Tax rate fix (5.5% not 25%)
### Notion
        - Command Center: 31488f09-7e31-816d-9fdc-c6aabba4e3fa
        - Master Task Tracker: 41 P0/P1/P2 tasks from container order to GO-LIVE
---
> UPDATED 2026-03-23 -- POST-GTC REWRITE
## ADC 3K Pod -- Current Spec (Post-GTC 2026)
### Hardware:
        - 40-ft High Cube ISO container (NOT 20-ft)
        - 10 NVIDIA Vera Rubin NVL72 racks (8 compute + 1 network + 1 storage) — C1 SuperPOD, 576 GPUs, 1.3 MW IT load
        - Eaton Beam Rubin DSX (800V DC rectifier + bus + PDUs)
        - Integrated dry cooler (exterior mount)
        - Portable natural gas generator OR site power tie-in
        - Optional: First Solar rooftop panels, LFP battery
### Software:
        - NVIDIA Dynamo 1.0 (inference OS)
        - NVIDIA Run:AI (fleet orchestration)
        - NVIDIA Base Command Manager (cluster management)
        - Mission Control AI (ADC autonomous ops)
        - NemoClaw (secure agent sandbox -- waiting for 403 bug fix)
### Power: 800V DC Native
        - Power hierarchy: Solar/First Solar 1500V DC -> Bloom SOFC 800V DC (primary) -> LFP BESS (bridge/ATS) -> Grid (sell-back only). No diesel — network redundancy via distributed sites.
        - Eaton Beam Rubin DSX throughout
        - Henry Hub natural gas pricing
### Deployment Targets:
        1. Oil fields (natural gas on-site)
        1. University campuses
        1. Municipal/emergency response
        1. 6G/AI-RAN base stations
        1. Remote/offshore (Starlink backhaul)
### Network Home:
        - All pods connect back to Willow Glen (PRIMARY NOC) via fiber or Starlink
        - MARLIE I = backup NOC (60 mi from Willow Glen)
        - Mission Control dashboard shows all nodes live
### Multi-Vendor:
        - NVIDIA Vera Rubin = primary (Dec 2026)
        - Tesla Terafab = future option (monitor availability)
        - AMD Instinct = future option
Container architecture is chip-agnostic -- 800V DC + liquid cooling works for any vendor.
### Open Items:
        1. NemoClaw 403 bug fix (NVIDIA GitHub Issues #314, #336)
        1. Container vendor selection (40-ft HC ISO)
        1. Portable genset spec for field deployment
        1. Starlink business account for remote pods
        1. Run:AI licensing and setup
        1. First Solar panel mounting spec for container roof
---
---
## Session Closeout — 2026-04-03
Notion fixes already pushed this session (do not redo): cooling corrected to direct-to-chip liquid throughout; rack count corrected to 10 NVL72 racks (C1 SuperPOD, 576 GPUs, 1.3 MW IT); email corrected to scott@adc3k.com; Bloom SOFC confirmed as PRIMARY; First Solar 1500V DC layer + grid sell-back only; deleted NPN 5-min form block, DANGER callout, duplicate cooling bullets, March 8 Bloom demotion.
### 10 MW Canonical Site Layout — LOCKED
        - 4 pods x 10 NVL72 racks per pad = one 10 MW site (40 racks, 2,880 GPUs)
        - Dual Bloom A + Bloom B — N+1 at generation level. Either covers full load solo.
        - One Atmos gas tap, manifold splits to both Bloom units
        - BESS vendor slot OPEN — do not lock supplier. Architecture = DC-coupled containerized BESS.
        - First Solar panels on pod rooftops. 1500V DC forward design. Operating at 800V today.
        - Two utility connections only per site: Atmos gas tap + LUS fiber drop. No grid. No water.
### Two-Bus Architecture — LOCKED
        - Bus 1 — COMPUTE (sacred): AI racks, liquid cooling, Mission Control. Hitachi AMPS + BESS. Zero interruptions. Nothing else on this bus.
        - Bus 2 — AUXILIARY (separate): site lighting, LED screen, EV/e-bike/scooter/phone/laptop DC charging, drone dock, security cameras. Separate smaller BESS.
        - Split happens after Bloom output. A fault on Bus 2 NEVER touches Bus 1. Both buses can be fed by either Bloom unit.
### Public-Facing Auxiliary Layer — LOCKED
        - LED screen on container exterior — advertising revenue + AI education content at night
        - DC charging hub: CCS fast charge EVs, e-bikes, scooters, phones, laptops. All DC-native — no AC conversion loss.
        - Scooter/bike docking — Lime, Bird, VeoRide partnership angle. Drop off, charge, pick up.
        - Site lighting: ADC owns its perimeter. Full LED flood + pathway. No city lighting dependence.
        - Drone security dock at every site. Autonomous patrol tied to Mission Control / SkyCommand. Mini KLFT node.
### City Neural Network Concept — INTERNAL ONLY
        - Lafayette pod network physically resembles a neural network. Each pod cluster = node, LUS fiber = axons, Bloom = synapse fuel.
        - Framing: We are not building a data center. We are building a brain for the city.
        - Map visualization: Lafayette street map, nodes lit at each site, edges showing fiber. MUST BUILD before investor meetings. NOT on website yet.
        - Scale target: 300-500 MW city-wide distributed. Do NOT publish a number. Frame as city-scale only.
        - Inference runs at nearest edge node. Training routes to Trappeys/Willow Glen. Network self-balances.
### Deployment Zones — Inner-City Infrastructure Corridors
        - Target: areas that cannot be traditionally developed (by water, gas infra, old neighborhoods) — already have Atmos gas + LUS fiber.
        - Only two utility connections needed: Atmos commercial gas tap + LUS fiber drop. No grid. No city plumbing. No building permits for occupied structures.
### OPEN ITEMS — Must Resolve Before Renders
        - OPEN: Cooling aesthetics — dry cooler is industrial-looking. Options: (1) louvered screen enclosure, (2) roof-mount low-profile, (3) visible design feature. Pick one. Must share design language with pod + LED screen + charging canopy + drone dock.
        - OPEN: Pad top-down site drawing — concrete pad, fenced perimeter, setback, Bloom A/B, BESS, AMPS PCS, 4 pods, cooler, charging canopy, drone dock. Lock this before renders.
### Next Actions
        1. Lock cooling aesthetics decision (choose one option)
        1. Produce pad top-down site drawing (concrete, perimeter, all equipment positions)
        1. Once pad is locked, begin renders — single design language, reusable across all sites
        1. Build city neural network map visualization (internal, before investor meetings)
New memory files: memory/projects/adc3k_city_network.md | memory/projects/adc3k_site_design.md | adc3k_pod_power_architecture.md updated with two-bus section at top.
---
> ARCHIVED (2026-03-24): This page is empty and vestigial. No content. Use the Pod Swarm Engineering Suite parent page instead.
---
> UPDATED 2026-03-23 -- POST-GTC REWRITE. All pre-GTC references to EC-110 immersion, Bloom Energy, 20-ft containers, and LUS-as-primary are SUPERSEDED by content below.
## ADC 3K Pod -- Post-GTC 2026 Architecture
The ADC 3K Pod is a 40-ft ISO container housing NVIDIA liquid-cooled racks (NOT immersion). DSX-compliant. 800V DC native power via Eaton Beam Rubin DSX. Self-powered on natural gas + solar. Managed remotely from Willow Glen (primary NOC) or MARLIE I (backup NOC).
### Key Changes Post-GTC:
    - 40-ft containers (NOT 20-ft -- too small for NVL72 racks)
    - NVIDIA ships complete liquid-cooled racks -- no custom immersion engineering needed
    - EC-110 immersion DEPRIORITIZED for main deployments
    - 800V DC native power distribution (Eaton Beam Rubin DSX)
    - 4-Layer Power Hierarchy: Solar -> Natural Gas -> Diesel -> Grid (sell-back only)
    - Bloom Energy SOFC = PRIMARY power source (800V DC direct, 3 units in series, ~750 kW/cell, no inverter needed)
    - Willow Glen = PRIMARY HUB, MARLIE I = backup NOC + edge
    - Multi-vendor chip ready (NVIDIA primary, Terafab/AMD future-proofed)
    - NVIDIA Run:AI for fleet orchestration across all pods
    - 6G/AI-RAN deployment capability via Nokia partnership
### Hub-and-Spoke Architecture:
    - HUB: Willow Glen Terminal (700 acres, 500kV/230kV, Mississippi River)
    - SPOKE 1: MARLIE I (Lafayette, backup NOC, 8 NVL72 racks)
    - SPOKE 2: Trappeys Cannery (Lafayette, UL Lafayette, 4 buildings)
    - SPOKE 3+: ADC 3K Pods (oil fields, remote sites, edge deployments)
    - All spokes connect back to Willow Glen via fiber (terrestrial) or Starlink (remote)
    - Mission Control AI manages all nodes from single dashboard
### Deployment Use Cases:
    1. Oil field edge compute (natural gas on-site, zero grid dependency)
    1. University research nodes (campus deployments)
    1. Municipal AI services (smart city, emergency response)
    1. 6G/AI-RAN base stations (NVIDIA + Nokia)
    1. Remote/offshore inference (Starlink backhaul)
    1. Disaster response mobile compute
---
> IMPORTANT (2026-03-24): This page has been audited. The ONLY current content is in the "POST-GTC REWRITE" section below. Everything ABOVE that section is pre-GTC (March 2026) and contains wrong specs: EC-110 immersion (deprioritized), Bloom Energy (removed), 480V AC (now 800V DC), MARLIE I as primary NOC (now Willow Glen). DO NOT use pre-GTC content for any purpose.
*[Child: Session Prompts & Claude Context]*
> Saved Claude session prompts and AI context documents for ADC 3K mission continuity. Contains the master session startup prompt and engineering package backup.
---
## Contents
    - ADC 3K master session startup prompt (copy/paste to begin any new session)
    - March 4, 2026 engineering package backup and document inventory
*[Child: March 4 2026 — Engineering Package Backup & Status]*
> Engineering package produced Feb 28 - Mar 4, 2026. Complete ADC 3K document set as of that date.
## Document Inventory (March 4, 2026)
### Engineering
      1. ADC-3K-Engineering-Lock-Package.docx — thermal model, CFD, 107 sensors, derate playbook (~99 pages)
      1. ADC-3K-Hard-Confirmation-Pack-RFI.docx — 80+ vendor questions, 5 sections
      1. ADC-3K-Single-Line-Diagram.html — interactive power distribution, PUE 1.083
      1. ADC-3K-Liquid-Loop-PID.html — dual-loop piping, valves, 64 sensors
      1. ADC-3K-Floor-Plan.html — plan view, cross section, dimensions + weight
      1. ADC-3K-Closed-Loop-Air-Strategy-v1.1a.docx — Section 6 insert
### Financial
      1. ADC-3K-Financial-Model.xlsx — 5-tab, 180 formulas, $33.2M CapEx, $9.4M EBITDA Y3 (NOTE: tax rate error, use 5.5% not 25%)
      1. ADC-3K-Investor-Pitch-Deck.pptx — 9-slide deck
      1. ADC-3K-Vendor-Parts-List.xlsx — 59 line items, $29.5M BOM, lead times
      1. ADC-3K-Session-Handoff-Final.md — full inventory and cross-reference map
### Outreach
      1. ADC3K_NVIDIA_Inception_Application_Package_Rev1.docx — ready to submit
      1. ADC3K_Cooling_Vendor_RFI_Outreach_Pack_Rev1.docx — 4 emails ready to send
      1. ADC3K_Patent_Disclosure_Rev1.docx — deliver to counsel, Q2 2026 provisional
      1. ADC3K_Investor_Pitch_Deck_Rev1.pptx + ADC3K_Financial_Model_Rev1.xlsx
### Website
      1. ADC-3K-Master-Website-V3.html — 728 KB SPA, 10 pages, production-ready
> ARCHITECTURE NOTE (March 8, 2026): ADC 3K cooling changed from CDU to immersion. These docs reflect older spec. Review before sending to vendors or investors.
*[Child: ADC 3K — Master Session Prompt]*
Last Updated: February 28, 2026 — Original engineering brief. Updated architecture below (March 8, 2026).
Use this prompt to start any new Claude session working on ADC project documents.
Copy everything below the line and paste it as your first message.
## START COPYING HERE
You are the lead infrastructure architect, financial strategist, and technical writer for Advantage Design Construction Inc.'s ADC 3K program.
## PROJECT CONTEXT
ADC (Advantage Design Construction Inc.) is a Louisiana-licensed general contractor (est. 2003) based in Lafayette, LA. Owner: Scott. ADC is developing the ADC 3K — a 3 Megawatt-class liquid-cooled AI compute pod built inside a standard 40-ft High Cube ISO container. 1,008 NVIDIA Rubin GPUs across 14 NVL72 racks (72 GPUs/rack). Direct-to-chip liquid cooling via 3x Vertiv XDU450 CDUs (N+1 redundant).
The project has evolved from: site-specific Trappey's concept → 20-ft 800 kW (V1-V4) → 40-ft 2,400 kW Model 2400X (V5) → ADC 3K (refined engineering, confirmed thermal model, complete documentation package).
## COMPLETE ADC 3K DOCUMENT SET
All produced February 28, 2026:
      1. ADC-3K-Engineering-Lock-Package.docx — Thermal model, CFD plan, 107 sensors, controls, derate playbook (~99 pages)
      1. ADC-3K-Hard-Confirmation-Pack-RFI.docx — 80+ vendor questions, 5 sections, email template
      1. ADC-3K-Single-Line-Diagram.html — Interactive: power distribution, breaker schedule, PUE 1.083
      1. ADC-3K-Liquid-Loop-PID.html — Interactive: dual-loop piping, valves, 64 liquid-loop sensors
      1. ADC-3K-Financial-Model.xlsx — 5-tab, 180 formulas: $33.2M CapEx, $9.4M EBITDA Y3
      1. ADC-3K-Investor-Pitch-Deck.pptx — 9-slide deck with charts and financial summary
      1. ADC-3K-Floor-Plan.html — Interactive: plan view, cross section, dimensions + weight
      1. ADC-3K-Vendor-Parts-List.xlsx — 59 line items, $29.5M BOM, lead times, vendor contacts
      1. ADC-3K-Session-Handoff-Final.md — Complete inventory, priorities, cross-reference map
      1. ADC-3K-Closed-Loop-Air-Strategy-v1.1a.docx — Section 6 insert: closed-loop air environment, capacity-based DOAS gating, dew point margin framework, Protect Mode, commissioning protocol, 29+ air-side sensors, 22 RFIs (AIR-01–A22)
## THREE CRITICAL ENGINEERING FLAGS
      1. CDU Capacity Short at 4°C ATD: 1,359 kW < 1,680 kW. Must operate ≥5.4°C ATD. Target 6–7°C.
      1. Flow Rate (GATING): At 10 deg C dT = 636 GPM (FAIL). At 20 deg C dT = 318 GPM (OK). MUST confirm Vera Rubin GPU dT >= 20 deg C (RFI S-01) — contact NVIDIA Enterprise for thermal spec.
      1. Busway Fit: 4,000A Starline T5 must fit 18" ceiling space. Derating at 45–55°C ambient (RFI B-01, B-02).
## TECHNICAL SPECS — ADC 3K
      - Container: 40-ft High Cube ISO, 93" internal width (TIGHT), 106" internal height
      - GPU: 1,008x NVIDIA Rubin GPU in 14x NVL72 racks (72 GPUs/rack)
      - IT Load: 2,100 kW peak (150 kW/rack), 1,848 kW typical (132 kW/rack)
      - PUE: 1.083 → 2,274 kW total facility load
      - Cooling: 3× Vertiv XDU450 CDU, manifolded N+1. 30% PG / 70% DI water. 318 GPM @ 20°C ΔT server-side. 1,680 kW liquid (80%), 420 kW air (20%).
      - Electrical: 480V / 4,000A Starline T5 busway. 14 tap-off boxes (250AF/200AT each). Active Power CLEANSOURCE flywheel UPS (external).
      - Controls: 107 sensors (48 temp, 4 flow, 6 pressure/ΔP, 1 RH, 4 leak, 3 vibration, 16 ambient, 14 rack power, 11 misc). 10-state MPC controller. Safety PLC with <100ms hardwired shutdown.
      - Container Zones: A (Power/2.5 ft), B (Cooling/3.5 ft), C (Compute/28 ft), D (Controls/3 ft), E (Access/2.4 ft)
      - Weight: ~60,000 lb estimated. Floor loading ~194 PSF.
      - Cost: $33.2M CapEx per pod ($25M GPU + $8.2M infrastructure)
      - Revenue: $11.6M/yr at 92% utilization (Year 3). EBITDA margin 80.8%. Payback ~3.5 years.
## VENDOR RFI STATUS (as of Feb 28, 2026)
All RFIs written and ready to send:
      - Supermicro/NVIDIA: 24 questions (S-01 through S-24). S-01 (ΔT) is GATING.
      - Vertiv: 21 questions (V-01 through V-21). V-01 (ATD curve) is CRITICAL.
      - Starline: 14 questions (B-01 through B-14). B-01 (profile dims) is CRITICAL.
      - Heat Rejection: 3 options with questions (dry cooler, wet tower, river HX).
      - Controls/BMS/PLC: 15 questions (C-01 through C-15).
## FINANCIAL MODEL KEY NUMBERS
      - CapEx: $33.2M (75% GPU, 8% racks, 6% cooling/power/container, 10% integration/engineering, 1% contingency)
      - Revenue (Y3): $11.6M (GPUaaS: $1.75/hr reserved, $2.50/hr spot, 70/30 mix, 92% utilization)
      - OpEx (Y3): $2.2M (power $982K, maintenance $1.0M, network $127K, staff $64K)
      - EBITDA (Y3): $9.4M (80.8% margin)
      - 5-Year Cum FCF: $39.4M
      - 10-pod deployment: $292M adjusted CapEx (12% volume discount), ~28% IRR
## TONE
Institutional, credible, engineering-first. Professional language suitable for PE-stamped documents, bank loan packages, and investor presentations. Not hype.
## INSTRUCTIONS FOR THIS SESSION
[EDIT THIS SECTION EACH SESSION — tell Claude what to work on]
Examples:
      - "Finalize thermal model with Supermicro's confirmed ΔT value"
      - "Update CDU operating point after Vertiv provides ATD curve"
      - "Create arc flash study after LUS provides fault current"
      - "Build container mechanical detail drawings (penetrations, structural)"
      - "Update financial model with actual vendor quotes"
## END COPYING HERE
---
> UPDATED BRIEF — March 8, 2026. Use this section for new sessions. Original Feb 28 brief above is preserved for document reference.
## COPY FROM HERE FOR NEW SESSIONS
You are the lead infrastructure architect and technical strategist for Advantage Design Construction Inc. (ADC). Owner: Scott Tomsu. Lafayette, Louisiana.
### TWO PRODUCTS — Never conflate them
      - MARLIE I = permanent AI Factory at 1201 SE Evangeline Thruway. Building-based. NVL72 racks inside existing structure. HQ + NOC + primary compute. CDU liquid cooling + Bloom Energy (continuous supplemental) + LUS grid (primary) + diesel N+1.
      - ADC 3K = manufactured containerized pod product line. 40-ft ISO containers deployed to remote sites as units. Immersion cooling (no HVAC, no CDU — works inside any metal structure). First deployment: Trappeys Cannery warehouse.
### Current Hardware Platform (both products)
      - NVIDIA Vera Rubin NVL72 — confirmed CES 2026, H2 2026 full production
      - 72 Rubin GPUs + 36 Vera CPUs per rack | HBM4 288 GB/GPU | NVLink 6 | 3.6 ExaFLOPS NVFP4
      - TDP NOT published by NVIDIA — all power/cooling sizing based on analyst estimates. Engage NVIDIA Enterprise Sales.
      - Blackwell / GB200 / GB300 / NVLink 5 / HBM3e — all RETIRED. Do not reference.
### Open Investor Action Items (must resolve before raise)
      1. Customer LOI — zero signed anchor tenants. Fatal for institutional investors.
      1. NVIDIA TDP — facility design unfinished without it.
      1. HB 827 — Phase 1 below 00M threshold. Develop parish-level PILOT.
      1. CapEx — 3.2M stated vs analyst -10M/rack × 14 racks. Reconcile.
      1. Financial model tax rate — 5.5% not ~25%. Fix Assumptions tab.
### Notion Workspace IDs
      - HQ: 31288f09-7e31-81a5-bf43-e2af16379346
      - MARLIE I: 31e88f09-7e31-8121-b4d2-d96b0084cc50
      - ADC 3K Command Center: 31488f09-7e31-816d-9fdc-c6aabba4e3fa
      - Trappeys AI Center: 31288f09-7e31-80a2-8712-ef09878afd53
### Louisiana Incentives
      - ITEP: file BEFORE breaking ground — non-negotiable
      - LA corporate tax: 5.5% | Henry Hub proximity: 40 miles — lowest natural gas cost in US
      - Historic Tax Credits: 45% combined | NVIDIA Inception: application ready, not submitted
---
> MARCH 21, 2026 UPDATE -- Post-GTC Strategic Pivot + Trappeys Core Project
This section supersedes conflicting info above. The Feb 28 and March 8 briefs are preserved for reference but the strategic direction has fundamentally shifted after GTC 2026 (March 17-21).
## Strategic Pivot: ADC Is a Neocloud
      - ADC is a NEOCLOUD -- GPU-first cloud provider, not a colocation facility. Energy-first model (Crusoe's playbook). Full NVIDIA stack. Sell tokens, not GPU hours.
      - Token Factory model -- managed inference via Dynamo 1.0 + Groq LPU decode. 7x performance on same Blackwell hardware. GPU prefill + Groq decode = 35x tokens/watt. Higher margin than bare metal GPU rental.
      - DSX Reference Design -- NVIDIA's complete AI factory blueprint. ADC builds to spec. 800V DC power (Eaton Beam Rubin). Direct-to-chip liquid cooling. InfiniBand fabric.
      - EC-110 immersion DEPRIORITIZED -- NVIDIA ships complete liquid-cooled racks (45 deg C hot water, 2-hr install). Immersion may still apply to edge/remote only.
## Trappeys = THE Core Project
      - Trappeys Cannery -- 112,500 sq ft across 4 buildings. Former cannery, Lafayette LA. ~$1M acquisition. Brownfield (M2 zoning). Half mile from MARLIE I. 30 mi from First Solar New Iberia factory.
      - 2.05 MW solar -- 3,731 First Solar TR1 panels across 4 rooftops. 800V DC solar-direct to DSX bus (97% efficiency vs 92% AC path).
      - 4-layer power hierarchy -- Solar (primary offset) > Natural Gas (backbone 24/7) > Diesel (emergency) > Grid (sell-back ONLY, not a source).
      - 9-page mini-site LIVE -- adc3k.com/trappeys + campus + technology + university + responders + investors + plan + dsx-prep + presentation
      - Phase 1 budget: $1.1-1.7M (equipment) + $300-500K (engineering/services). Full procurement matrix with primary + backup US vendors for every component.
## Certification Ladder
      - NPN (register NOW, 5-min form)  > DGX-Ready (Willow Glen)  > NCP (NVIDIA Cloud Partner)  > Reference Platform NCP
      - Inception is for software startups, NOT infrastructure. ADC goes through Partner Network.
## Key Contacts & Next Steps
      - UL Lafayette -- New president Dr. Ramesh Kolluru (CS PhD, R1 builder). No GPU infra. LEDA for warm intro. $28-55M+ grant potential.
      - ITEP -- NAICS code risk. Must pre-qualify with LED as 'emerging industry.' $8-16M savings. Contact: Kristin Johnson, 225-342-2083.
      - Act 730 -- Separate 20-year sales tax exemption ($200M+, 50 jobs).
      - First Solar -- LOCKED IN. Series 7 TR1. $1.1B New Iberia factory 30 mi away. modulesales@firstsolar.com / 419-662-6899.
      - Vendor tiers complete in Notion -- Tier 1 (hardware), Tier 2 (operational partners & professional services), Tier 3 (government & institutional). All under Vendor & Partner Strategy.
## Deployed Assets (adc3k.com)
      - 73+ HTML pages deployed to Vercel. Trappeys mini-site (9 pages + 40 photos). Omniverse DSX renders (v4 batch, 12 investor-grade). Investor page. Lafayette city pitch. Hub page links everything.
      - Business model docs in repo: token economics, power economics, capex model, revenue streams, vendor procurement matrix, ITEP filing, permits timeline, UL Lafayette approach, NPN registration checklist.
---
> ARCHIVED (2026-03-23): These session prompts are from early March 2026 (pre-GTC). The current session context is managed via CLAUDE.md in the git repo and memory files in .claude/projects/. These Notion pages are historical reference only.
*[Child: ADC-3K Website Build Logs]*
> Build logs, design decisions, and content for the ADC3K public website.
---
## Contents
    - Site architecture and page structure
    - Content drafts and copy
    - Design system and branding
    - Deployment notes
*[Child: ADC-3K POD — Website Build Log (V3)]*
> Build summary for ADC-3K-Master-Website-V3.html — production-ready SPA, March 1, 2026.
## V3 Build Summary
      - File: ADC-3K-Master-Website-V3.html | Size: ~728 KB single-file SPA with embedded images
      - Pages: 10 | Status: Production-ready as of March 1, 2026
      - Branding: ADC-3K POD — global rename complete
      - Contact: (337) 780-1535 / ADHSCOTT@yahoo.com
## Version History
      - V1-V4: 20-ft container, 800 kW, Trappeys site-specific
      - V5 (Model 2400X): 40-ft container, 2,400 kW
      - V3 Website: ADC-3K POD branding, 3 MW class
## Architecture Note (March 8, 2026)
> Website may reference CDU liquid cooling from original spec. Current ADC 3K architecture uses immersion cooling. Update copy before publishing.
## Deployment
      - Currently local file — not deployed to public URL
      - Target domain: adc3k.com | Hosting: Vercel, Cloudflare Pages, or ADC-hosted (TBD)
> ADC3K — Advanced Computing 3000, Lafayette LA. AI Factory + Edge AI + Infrastructure. Owner: Scott Tomsu.
---
## Active Projects
  - MARLIE I — Lafayette AI Factory (pre-deployment, investor outreach active)
---
## Engineering Groups
  - Pod Swarm Engineering Suite
  - Edge AI Infrastructure Documents
  - Session Prompts & Claude Context
  - ADC-3K Website Build Logs
---
## Quick Links
  - MARLIE I Pitch Deck: marlie/index.html in gpu-learning-lab repo
  - Mission Control Dashboard: http://localhost:8000
  - RunPod GPU Pods: via Mission Control > Integration Agent
---
> Everything AI, everything sovereign, everything Louisiana.
> Engineering & operations sub-workspace for ADC 3K infrastructure builds. Lives inside Mission Control HQ.
---
## Contents
  - Pod Swarm Engineering Suite — NVL72 rack configs, CDU schematics, PDU layouts, network topology, RunPod API
  - Session Prompts & Claude Context — AI session backups and master prompt archive
  - ADC-3K Website Build Logs — V3 website build history
  - Master Task Tracker — project task database
---
## Active Projects
  - MARLIE I — Lafayette AI Factory: see Mission Control HQ → MARLIE I (Sections 01-09)
  - Pod Swarm: NVL72 rack engineering package — see Pod Swarm Engineering Suite
---
> New root sections are being added to Mission Control HQ. This workspace handles engineering sub-documents.
---
> INVESTOR REVIEW — CRITICAL FIXES (March 8, 2026) | Items 6 & 7 RESOLVED. Items 1-5 require action.
## Issues That Will Kill the Deal in Diligence
### 1. No Customer — Fatal for Institutional Investors
  - Zero signed LOIs or anchor tenant commitments documented anywhere
  - All financial projections rest on assumed utilization with no demand validation
  - ACTION: Secure at least one signed LOI before next investor meeting
### 2. TDP Not Confirmed by NVIDIA
  - NVL72 Vera Rubin TDP not published — entire power, cooling, and electrical design built on analyst estimates (150-250 kW/rack)
  - Cannot finalize CDU sizing, generator spec, or panel design without confirmed TDP
  - ACTION: Engage NVIDIA Enterprise Sales — get written facility planning spec
### 3. HB 827 — Phase 1 Does Not Qualify
  - HB 827 requires 00M minimum eligible investment. Phase 1 at 9-30M is below threshold
  - This is listed as a named incentive in pitch materials — investors who know LA law will catch it
  - ACTION: Fully develop parish-level PILOT agreement NOW as the replacement. Brief investors honestly.
### 4. CapEx Does Not Add Up
  - 3.2M total CapEx stated. Analyst estimates for prior-gen GB200 NVL72 were -10M per rack.
  - 14 Vera Rubin NVL72 racks at even half that = 6-70M hardware alone
  - ACTION: Either reconcile CapEx with actual NVIDIA pricing OR reduce rack count to match 3.2M budget
### 5. Financial Model Tax Rate Error
  - Model uses ~25% blended Louisiana corporate tax rate. Actual rate: 5.5%
  - IRR is higher than currently shown — but model presented to investors is wrong
  - ACTION: Update financial model Assumptions tab before next investor meeting
### 6. Bloom Energy Language — CORRECTED (2026-04-03)
  - LOCKED: Bloom Energy SOFC = PRIMARY generation (800V DC direct, no inverter, Henry Hub gas). First Solar = 1500V DC layer. LUS grid = sell-back only. Diesel = emergency N+1 only.
  - FIXED: Power Distribution page now has corrected hierarchy callout at top of page.
---
## What Institutional Investors Expect That Is Missing
  - Signed LOI or anchor tenant term sheet
  - Independent engineering validation — third-party thermal/electrical stamp
  - 3-scenario financial model: bear (50% utilization), base (75%), bull (90%) with sensitivity tables
  - Capital stack and waterfall — equity, debt, mezzanine structure with return hurdles
  - Management team bios — LinkedIn-level detail on all team members with hyperscale or data center experience
  - Written utility capacity confirmation from LUS or SLEMCO
  - NVIDIA Enterprise relationship — Inception application submitted (listed as open task)
  - Comparable transaction analysis — what did similar GPU campus deals trade at
  - Exit strategy — 5-year path to liquidity: acquisition target, cash yield, or IPO path
---
## What Is Strong — Do Not Change
  - Site ownership: 5K debt-free land, no lease risk — lead with this
  - Henry Hub proximity — verifiable natural gas cost advantage
  - Bloom Energy 3-layer power architecture — modern, ESG-aligned, differentiating
  - ADC Inc. as GC (est. 2003) — construction risk internally managed, not outsourced
  - Edge AI repositioning and terminology — polished, market-correct
  - Louisiana incentive awareness — ITEP timing, parish PILOT — shows operational sophistication
---
> ARCHITECTURE CLARIFICATION — TWO SEPARATE PRODUCTS (March 8, 2026)
## Product 1: MARLIE I — Lafayette AI Factory (Fixed Facility)
  - Location: 1201 SE Evangeline Thruway, Lafayette, Louisiana — owner-controlled, debt-free
  - Type: Permanent building-based AI Factory — NVL72 racks inside existing structure
  - Role: ADC HQ, primary compute facility, NOC, operations base
  - Phase 1: 16 NVL72 racks on 22x35 ft floor — 57.6 ExaFLOPS NVFP4
  - Cooling: Direct-to-chip CDU liquid cooling, exterior dry coolers. Power: Bloom SOFC primary + First Solar + LUS grid sell-back
## Product 2: ADC 3K — Containerized AI Pod (Manufactured Product Line)
  - Type: Standardized containerized compute nodes — manufactured, sold, and deployed as units
  - Role: Remote site deployments — edge AI distribution centers tied into the network
  - Cooling: Direct-to-chip liquid cooling. External dry cooler. No HVAC required — enables deployment into metal structures without AC.
  - First deployment site: Trappeys Cannery — metal warehouse structure, liquid-cooled pods
  - Future sites: Industrial yards, commercial facilities, any site with power + fiber — no special building required
  - Scale: Multiple pods per site, networked back to MARLIE I
> These are two different products serving different purposes. MARLIE I is the factory. ADC 3K pods are the distributed product deployed from it.
---
## Investor Review — Second Pass Gaps (March 8, 2026)
> These 7 gaps must be addressed before institutional investor meetings. Items marked [SCOTT ACTION] require work outside Notion.
### Gap 1 — Unit Economics Per Pod [SCOTT ACTION]
Missing: Revenue per pod, CapEx per pod, payback period per pod, gross margin per pod. Institutional investors need to evaluate the unit economics of the product — not just the aggregate financial model.
  - Add to financial model: pod CapEx (container + hardware + liquid cooling system + install), monthly revenue per pod (colocation rate x GPU capacity), OpEx per pod (fluid maintenance, remote NOC, power), payback period per pod
  - Target: 18–36 month payback per pod at base-case utilization
### Gap 2 — Remote Site Operations Model [SCOTT ACTION]
Missing: Who manages the pod at the remote site? What is the SLA? How is maintenance handled? This is a core differentiator — answer it explicitly.
  - Model: MARLIE I NOC manages all pods remotely via Mission Control — no on-site staff at remote locations
  - Maintenance: Fluid checks and GPU swap require on-site visit — contract with local HVAC/electrical firm per deployment site
  - SLA target: 99.5% uptime — document in investor deck and customer contracts
  - Site owner role: Provides power, fiber, and space — ADC 3K handles everything inside the container
### Gap 3 — Dielectric Fluid: RESOLVED (March 8, 2026)
> COMMITTED: Engineered Fluids EC-110 (single-phase). All 3M Novec references removed. Novec is discontinued — Engineered Fluids is the standard replacement.
### Gap 4 — Competitive Landscape [SCOTT ACTION]
No competitive analysis in investor materials. Institutional investors will ask: who else does this and why will you win?
  - Direct competitors: CoreWeave (cloud GPU), Lambda Labs, Crusoe Energy (stranded gas), Lancium (remote compute)
  - ADC 3K differentiators: (1) Site-agnostic liquid-cooled pod — deploy anywhere with power + fiber, (2) Louisiana incentive stack + Henry Hub gas proximity, (3) Owner-operator with captive manufacturing base (MARLIE I), (4) Small-footprint pod enables enterprise edge AI, not just hyperscale
  - Add competitive landscape slide to investor deck — 1 slide, 4 quadrants or simple table
### Gap 5 — Exit Strategy [SCOTT ACTION]
  - Option A: Acqui-hire / strategic acquisition — ADC 3K as manufactured AI infrastructure product is acquisition target for hyperscalers or REITs
  - Option B: Build-to-sell — sell deployed pod swarms to data center operators or PE-backed infra funds
  - Option C: REIT structure — pool pods into income-producing AI infrastructure fund (public or private)
  - Add 1-slide exit strategy to investor deck — show realistic 5–7 year horizon
### Gap 6 — Management Team [SCOTT ACTION]
No team slide in investor materials. Investors bet on people as much as ideas. This gap can kill a raise regardless of how good the tech is.
  - Add team slide: founder bio, relevant construction/real estate/AI experience, any advisors or anchor relationships
  - Key hires to identify: CTO/engineering lead, CFO or fractional CFO for raise, NVIDIA/hyperscaler enterprise sales contact
### Gap 7 — 3-Scenario Financial Model [SCOTT ACTION]
  - Bear case: GPU utilization 40%, GPU price correction -30%, deployment delays 12 months
  - Base case: GPU utilization 70%, current market rates, H2 2026 Vera Rubin delivery on schedule
  - Bull case: GPU utilization 90%, premium enterprise pricing, multi-site pod swarm at 10+ locations by Y3
  - ALSO FIX: Tax rate in model is ~25% — Louisiana corporate tax is 5.5%. IRR is materially higher than currently modeled.
  - ALSO FIX: CapEx $33.2M stated vs analyst estimate $8-10M/rack x 14 racks = $112-140M. Reconcile or explain.
  - ALSO FIX: HB 827 threshold: Phase 1 is below $200M — replace HB 827 with parish-level PILOT and brief investors honestly
---
## ADC 3K Deployment Geography — Natural Gas Pipeline Map
ADC 3K liquid-cooled pods deploy along Louisiana natural gas pipeline corridor. This is not arbitrary. Gas pipeline infrastructure means: existing utility roads, 3-phase power stubs, industrial zoning, and co-location opportunity with captive industrial customers.
  - Deployment logic: pods follow Atmos/CenterPoint gas pipeline map — industrial site co-location
  - Henry Hub corridor: Erath, LA (~40 mi from MARLIE I) — Vermilion Parish gas distribution hub
  - Gulf Coast industrial belt: refineries, LNG export terminals, petrochemical plants — captive ADC customers
  - New Iberia (Site 2 candidate): solar factory + industrial port + pipeline access — ADC pod + energy partner
  - Lake Charles / Cameron Parish: LNG export corridor — security, monitoring, AI inference pods
  - Morgan City: offshore supply base, pipeline terminus — SAR + industrial AI
  - Scaling rule: one ADC 3K pod per industrial customer — liquid-cooled pod drops into existing metal structure
---
## Ecosystem Network — How ADC 3K Connects to Everything
> ADC 3K is NOT a standalone product. It is the field arm of the ADC ecosystem. MARLIE I is the brain. ADC 3K pods are the muscle. KLFT is the showcase. Ground Zero tells the story.
  - MARLIE I (HQ/NOC): all ADC 3K pods managed from 1201 SE Evangeline Thruway — Mission Control AI
  - Trappeys Cannery (Site 1 planned): first remote pod deployment — metal warehouse, liquid cooling
  - KLFT 1.1 (first live node): ADC 3K pod at Lafayette airport — SkyCommand compute, emergency drone ops
  - New Iberia (Site 2): solar factory + ADC pod — renewable energy anchor + industrial AI customer
  - Ground Zero: YouTube channel @GroundZero-ai — ADC ecosystem documentary, 8 planned ADC episodes
  - SkyCommand SaaS: drone fleet management — runs on ADC 3K pod at KLFT, scales to multi-site
---
## Cooling Architecture (Updated Post-GTC 2026)
NVIDIA ships complete liquid-cooled racks (45 deg C hot water, 2-hour install). EC-110 immersion cooling DEPRIORITIZED for main facilities post-GTC 2026. The standard is now NVIDIA reference liquid cooling with direct-to-chip cold plates. Dry coolers for heat rejection. PUE target: 1.03. EC-110 may still apply to edge/remote deployments where standard rack cooling is impractical.
  - Direct-to-chip liquid cooling: 45 deg C hot water loop. No massive AC systems. No loud fans. NVIDIA-standard for all Blackwell/Vera Rubin racks. Eaton Beam Rubin DSX handles 800V DC power delivery.
  - Louisiana rationale: 95°F+ summers, 80%+ humidity — air cooling costs 40-80% of power budget
  - No HVAC: zero air conditioning, zero CRAC, zero raised floor — pods deploy into raw warehouse space
  - No fans: sealed fluid bath — silent, zero vibration, maximum GPU lifespan
  - MARLIE I is DIFFERENT: cold plate CDU — building-based, code-compliant, public-facing state of the art
---
## New Iberia Solar Factory — Strategic Energy Partner
Local utility-scale solar production facility ~30 miles from MARLIE I in New Iberia, LA. New Iberia is simultaneously a candidate for ADC 3K Site 2 deployment and a renewable energy supplier.
  - Energy role: solar PPA or wheeled credits through LUS grid — supplements Bloom + LUS + nat gas stack
  - Site 2 role: ADC pod deployed at or near solar factory — captive AI compute for solar ops analytics
  - Industrial port access: New Iberia has port and petrochemical industrial base — additional pod customers
  - KLFT expansion: New Iberia is Site 2 candidate for KLFT Gulf Coast drone network expansion
  - FEOC compliance: domestic renewable energy source — reinforces OBBBA clean-energy qualification
> MCHD ON HOLD: 18 tasks frozen as of 2026-03-23. Resume when Mission Control HD SaaS project restarts.
---
> MASTER TASK TRACKER — POST-GTC UPDATE (2026-03-23): The 35 tasks in this tracker reference 20-ft ISO containers and old specs. Post-GTC reality: 40-ft HC ISO containers, NVIDIA ships complete liquid-cooled racks (no custom immersion), 800V DC via Eaton Beam Rubin DSX. Tasks referencing 'Order 20-ft ISO container', CDU procurement, and immersion cooling are SUPERSEDED. Keep tasks for reference but specs must be updated when pod build restarts.
---
> CRITICAL UPDATE (2026-03-24): AUDIT RESULTS -- This page has severe stale content:
- "Two-Product Model" says MARLIE I is HQ -- WRONG. Willow Glen is PRIMARY.
- References NVIDIA Inception -- WRONG. ADC goes through Partner Network (NPN).
- Lists Bloom Energy as a strength -- REMOVED from power stack.
- Says 16 racks Phase 1 -- WRONG. MARLIE I is 8 racks per floor (16 total, 2 SuperPODs).
- Says immersion cooling for ADC 3K pods -- DEPRIORITIZED. NVIDIA ships liquid-cooled racks.
- Email shows ADHSCOTT@yahoo.com -- WRONG. Use scott@adc3k.com.
- All content below "POST-GTC" callouts is current. Everything above is pre-GTC and largely wrong.
- CLAUDE.md and memory files in .claude/projects/ are the authoritative source of truth.
*[Child: Workspace Index & Navigation]*
> Last updated: March 21, 2026 (post-GTC pivot). Master navigation reference for the Mission Control HQ workspace.
> Start here. Every active project, archive, and document in the workspace is mapped below.
---
## MARLIE I — Lafayette AI Factory
Primary investor + engineering workbook for the Lafayette AI Factory build. 9 sections covering the full project from investment thesis to financial ROI.
  - 01 — Investment Thesis: why MARLIE I, market timing, Louisiana advantage
  - 02 — Hardware: NVIDIA Vera Rubin Platform: NVL72 specs, 3.6 ExaFLOPS/rack, HBM4, NVLink 6
  - 03 — Site & Building Specs: 1201 SE Evangeline Thruway, parcels, utility access
  - 04 — Government Funding Stack: OBBBA, CHIPS Act, Louisiana incentives
  - 05 — Infrastructure Partners: Bloom Energy, Vertiv, LUS Fiber, NVIDIA Enterprise
  - 06 — ADC3K Credentials: Scott Tomsu background, 7-layer expertise, certifications
  - 07 — Multi-Site Vision: Louisiana AI Network: Phase 1-3 Gulf Coast expansion
  - 08 — Contact & CTA: investor contact and next steps
  - 09 — Financial Architecture & ROI: revenue model, calculator, energy arbitrage, investor benefits
---
## Edge AI Infrastructure Documents
Terminology updates and positioning documents for rebranding from containerized pods to edge AI infrastructure. Covers NVIDIA platform updates (Blackwell → Vera Rubin), Bloom Energy architecture, and deployment roadmap.
  - Master Prompt: session context and instructions
  - Part 1: Executive Summary Rewrites — updated language for all public-facing docs
  - Part 2: Edge Infrastructure Positioning — market narrative and competitive framing
  - Part 3: Bloom Energy Power Architecture — fuel cell specs, Henry Hub advantage, cost model
  - Part 4: Terminology Map, Site Strategy & Roadmap — deprecated → current term map, Phase 1-3 roadmap
---
## ADC 3K — Project Command Center
Engineering sub-workspace. Contains Pod Swarm technical documentation, session logs, and website build history.
  - Pod Swarm Engineering Suite: NVL72 rack configs, CDU liquid cooling schematics, PDU layouts, network topology, RunPod API notes, architecture index
  - Session Prompts & Claude Context: AI session backups — March 4 2026 engineering package, master session prompt
  - ADC-3K Website Build Logs: V3 website build history
---
## Trappeys AI Center THE CORE PROJECT
THE primary project. Solar AI factory at 112,500 sq ft former Trappeys Cannery. 2.05 MW First Solar rooftop. Water tower cooling. Infrastructure yard. Partner hub. Half mile from MARLIE I. 9-page mini-site LIVE at adc3k.com/trappeys. Pitch presentation deck LIVE.
  - 9-page mini-site: /trappeys, /trappeys-campus, /trappeys-technology, /trappeys-university, /trappeys-responders, /trappeys-investors, /trappeys-plan, /trappeys-dsx-prep, /trappeys-presentation
  - Business model: Vendor procurement matrix, token economics, power economics, capex model in business-model/
  - DSX renders: Omniverse renders gallery at /dsx-renders (v4 batch, 12 investor-grade images)
  - Vendor strategy: Tier 1 (hardware), Tier 2 (operational partners), Tier 3 (government) in Notion Vendor & Partner Strategy
  - Power hierarchy: Solar (primary offset) > Natural Gas (backbone 24/7) > Diesel (emergency) > Grid (sell-back ONLY)
  - Lafayette AI Initiative: MARLIE I + Trappeys + KLFT + UL Lafayette + first responders. City pitch LIVE at /lafayette
---
## Local Files (GitHub Repo)
Primary working files live in the gpu-learning-lab repo: c:/Users/adhsc/OneDrive/Documents/GitHub/gpu-learning-lab/
  - marlie/index.html — MARLIE I pitch deck (HTML, dark theme, interactive ROI calculator)
  - marlie/*.py — build scripts: inject_roi, condense_roi, fix_floorplan_colors, populate_part4, notion_sync_financials
  - agents/ — Mission Control multi-agent platform (FastAPI + SSE)
  - web/index.html — Mission Control dashboard
  - main.py — FastAPI server, 10 agents
---
## Current Priority Stack
  - NPN Registration -- NVIDIA Partner Network. 5-min web form. Do today.
  - Trappeys site acquisition -- ~$1M. Structural engineer + Phase I ESA before closing.
  - UL Lafayette intro -- New president Dr. Ramesh Kolluru. LEDA for warm intro. Critical unlock for grants + workforce.
---
> ⚠️ UPDATED 2026-03-23
## Current Workspace Structure
### Active Projects
  - LSU + Willow Glen — Tiger Compute Campus (PRIMARY HUB). 9 sub-pages (01-09). Blueprints at adc3k.com/blueprints
  - Trappeys AI Center — Ragin' Cajun Compute Campus. 9 sub-pages (01-09). Blueprints at adc3k.com/blueprints-trappeys
  - MARLIE I — Lafayette AI Factory & Command Center. 9 sub-pages (01-09). Blueprints at adc3k.com/blueprints-marlie. 24x40 ft, 2 floors, 8 NVL72 racks.
  - KLFT 1.1 — Autonomous Airspace Ops Hub. 10 sub-pages. SkyCommand platform. Digital twin built (USD scene). Part 108 BVLOS final rule expected Spring 2026.
  - ADC 3K — Project Command Center — Pod Swarm engineering, Master Task Tracker, build playbooks
  - ADC Manufacturing — Two-step pod factory (Baton Rouge manual → New Iberia automated)
  - Vendor & Partner Strategy — 3 tiers + First Solar workbook + outreach sequence. Louisiana Cat contacts: Spencer Landry 985-498-9336, Ken Johnson 504-544-2074.
### Active Websites
  - louisianaai.net — Louisiana's AI Infrastructure Initiative (FREE public service)
  - adc3k.com — ADC corporate site + all project pages
  - ai-advantage.info — AI Advantage SMB business (NemoClaw-based installer model)
### On Hold
  - Mission Control HD — SaaS product. 5 sub-pages. Stripe/Supabase configured. Paused while infrastructure projects launch.
  - AI Daily Omniverse — YouTube production pipeline. 5 stories + 2 episodes. Dormant since March 4.
  - Ground Zero — YouTube channel (@ScottTomsu). 5 video scripts ready. Channel live.
### Archived (Pre-GTC 2026)
  - Edge AI — 11 pages. Bloom Energy + Inception references superseded by neocloud/NPN strategy.
  - Site Acquisition Pipeline — Airport and hotel sites dead. Trappeys + Willow Glen locked.
  - Notes & Ideas — Duplicated in Task Tracker.
  - Dev Session Log — Single entry.
### Key References
  - NVIDIA contacts: John Rendek (Head AI Factories NPN), Doug Traill (Sr Dir AI Factory)
  - Vera Rubin NVL72 available December 2026 via HPE
  - NemoClaw installed (Node 0: adc-node0) — waiting for 403 bug fix
  - Phone agent live: (337) 448-4242 — combined Sarah/Michelle/James
  - 136 email contacts ready to blast (70 districts + 46 universities + 20 media)
> Command center for all ADC 3K / MARLIE I projects. Everything lives here — organized by project.
---
## Active Projects
- MARLIE I — Lafayette AI Factory: 9-section investor + engineering workbook (Sections 01-09)
- Edge AI Infrastructure Documents: terminology, site strategy, Bloom Energy architecture (Parts 1-4)
- ADC 3K — Project Command Center: Pod Swarm engineering, session logs, website build logs
---
## Archive
- Trappeys AI Center: predecessor project docs — V1/V2/V3 containerized pod era, original investor deck
---
## Workspace Map
- Mission Control HQ  (this page)
-   └─ MARLIE I — Lafayette AI Factory
-        └─ 01 Investment Thesis  /  02 Hardware  /  03 Site  /  04 Gov Funding
-        └─ 05 Infrastructure Partners  /  06 Credentials  /  07 Multi-Site  /  08 CTA
-        └─ 09 Financial Architecture & ROI
-   └─ Edge AI Infrastructure Documents
-        └─ Master Prompt  /  Part 1 Exec Summary  /  Part 2 Positioning
-        └─ Part 3 Bloom Energy  /  Part 4 Terminology + Site Strategy + Roadmap
-   └─ Trappeys AI Center  [ARCHIVE]
-        └─ 5 legacy files  /  Hardware Evolution Log  /  Site History
-   └─ ADC 3K — Project Command Center
-        └─ Pod Swarm Engineering Suite  (NVL72 / CDU / PDU / Network / RunPod)
-        └─ Session Prompts & Claude Context
-        └─ ADC-3K Website Build Logs
---
## Coming Soon
- New root section — in planning (to be added at Mission Control HQ level)
- AI Daily Omniverse — Command Center: separate root for media/YouTube pipeline
*[Child: MARLIE I — Lafayette AI Factory]*
> Louisiana's first next-generation AI factory — 1201 SE Evangeline Thruway, Lafayette LA 70501 — ADC3K / Scott Tomsu — CONFIDENTIAL INVESTOR DECK
---
## Project Status
  - Phase: Pre-deployment — investor & partner outreach active
  - Hardware: NVIDIA Vera Rubin NVL72 — Full Production — H2 2026 availability
  - Site: Owner-built, debt-free — $15K total property debt
  - Permits: Louisiana GC License active — build-ready
  - Certifications: 7 NVIDIA + FAA Private Pilot + Part 107 UAS
---
## Workbook Sections
  - 01 — Investment Thesis
  - 02 — Hardware: NVIDIA Vera Rubin Platform
  - 03 — Site & Building Specs
  - 04 — Government Funding Stack
  - 05 — Infrastructure Partners
  - 06 — ADC3K Credentials
  - 07 — Multi-Site Vision: Louisiana AI Network
  - 08 — Contact & CTA
  - 09 — Financial Architecture & ROI
*[Child: 01 — Investment Thesis]*
> The market is building for Blackwell. Marlie I is built for Rubin. That gap is the investment.
---
## Thesis 01 — Skip Blackwell. Deploy Rubin.
    - 10x lower token cost vs Blackwell
    - 4x fewer GPUs for equivalent training runs
    - 22 TB/s memory bandwidth per GPU (HBM4)
    - 3.6 ExaFLOPS NVFP4 inference per NVL72 rack
    - H2 2026 — full production — Texas factories 4 hours from Marlie I
---
## Thesis 02 — Infrastructure Already Exists
    - Property debt: $15,000 total — owner-built, 20 years standing
    - LUS Fiber: ~0.8 miles — 214 Jefferson St
    - Atmos Energy (natural gas): ~3 miles — 1818 Eraste Landry Rd
    - Henry Hub gas benchmark: ~40 miles — Erath, LA
    - Lafayette Regional Airport (LFT): adjacent — Part 107 UAS
    - NVIDIA TX Manufacturing: ~4 hours — Foxconn Houston / Wistron Fort Worth
---
## Thesis 03 — Federal & State Money Is Already Flowing
    - Stargate AI Program ($500B) + One Big Beautiful Bill Act (OBBBA): federal domestic AI infrastructure push — FEOC-clean mandate, Gulf OCS revenue, BEAD broadband funding
    - Louisiana Act 730: 20-year state/local sales & use tax rebate on AI factory equipment
    - BEAD Broadband Program: federal backhaul expansion — LUS Fiber path
    - Gulf OCS Revenue: $650M/year to Louisiana through 2034
    - Marlie I: 100% FEOC-clean, Texas-manufactured hardware, Louisiana GC — qualifies for all programs
---
## Key Stats
    - 10x — Lower token cost vs Blackwell
    - 6 months — Estimated deploy timeline
    - $15K — Total property debt
    - 20 years — Louisiana tax exemption on equipment
    - #1 — Louisiana industrial power rates in USA
*[Child: 02 — Hardware: NVIDIA Vera Rubin Platform]*
> Jensen Huang: "Rubin arrives at exactly the right moment... Rubin takes a giant leap toward the next frontier of AI."
> Sam Altman: "Intelligence scales with compute... The NVIDIA Rubin platform helps us keep scaling this progress."
---
## NVL72 Rack System
    - 72 Rubin GPUs per rack
    - 36 Vera CPUs per rack
    - 3.6 ExaFLOPS NVFP4 inference per rack
    - 100% liquid cooled — zero air cooling
    - NVLink 6 switch fabric — 3.6 TB/s GPU-to-GPU per rack
    - 260 TB/s NVLink bandwidth across 14-rack DGX SuperPOD
    - 50.4 ExaFLOPS per 14-rack SuperPOD
    - Ships fully integrated from Texas factory — 5-minute install (18x faster than prior gen)
---
## Six-Chip Architecture
### 1. Rubin GPU
288 GB HBM4 — 22 TB/s memory bandwidth — 72 per rack
### 2. Vera CPU
88 custom Olympus cores — replaces x86 for AI workload orchestration — 36 per rack
### 3. NVLink 6 Switch
3.6 TB/s GPU-to-GPU fabric per rack — 260 TB/s at SuperPOD scale
### 4. ConnectX-9 SuperNIC
1.6 Tb/s aggregate per GPU — AI traffic with zero CPU involvement
### 5. BlueField-4 DPU
Rack-scale confidential computing — unlocks healthcare, finance, government workloads. Encryption, firewall, storage I/O offloaded — GPU cycles reserved for inference.
### 6. Spectrum-X Ethernet
800G per port — co-packaged optics — AI east-west traffic at rack scale
---
## 5 Investor Facts
    - Fact 01: First rack-scale confidential computing — new market segments unlocked
    - Fact 02: 18x faster deployment — 5 min install vs 1.5 hours prior gen
    - Fact 03: 50.4 ExaFLOPS from 14 racks (DGX SuperPOD)
    - Fact 04: 260 TB/s NVLink bandwidth across full SuperPOD cluster
    - Fact 05: Full production H2 2026 — 4 hours from Marlie I (Foxconn Houston / Wistron Fort Worth)
---
## MARLIE I + 3 Pod Compute Allocation
> 40 NVL72 racks total — 2,880 GPUs — 5,200 kW IT load — 10 MW Bloom SOFC generation
### Building — Downstairs (Compute)
    - 10 NVL72 racks — single row along 37 ft usable length
    - Same single-row layout as ADC 3K pod — 24 ft width provides full cold aisle + CDU equipment space
    - 720 GPUs — 1,300 kW IT load
    - 10 Bloom SOFC units — 2,500 kW generation
    - 1 CDU pair — NVIDIA-integrated liquid cooling, 45C hot water, exterior dry coolers
### Building — Upstairs (NOC)
    - Mission Control operations center — no compute racks
    - Network core, fiber MDA, monitoring, command ops
    - Backup NOC for Willow Glen (60 mi, dedicated fiber, management traffic only)
### Pod 1
    - 10 NVL72 racks — single row, 40 ft container
    - 720 GPUs — 1,300 kW IT load
    - 10 Bloom SOFC units — 2,500 kW generation
### Pod 2
    - 10 NVL72 racks — single row, 40 ft container
    - 720 GPUs — 1,300 kW IT load
    - 10 Bloom SOFC units — 2,500 kW generation
### Pod 3
    - 10 NVL72 racks — single row, 40 ft container
    - 720 GPUs — 1,300 kW IT load
    - 10 Bloom SOFC units — 2,500 kW generation
---
### Total MARLIE I Footprint
    - 40 NVL72 racks
    - 2,880 Rubin GPUs
    - 5,200 kW IT load
    - 40 Bloom SOFC units x 250 kW = 10,000 kW (10 MW) generation
    - Facility draw at PUE 1.10: ~5,720 kW — Bloom headroom: ~4,280 kW
    - 800V DC native via Eaton Beam Rubin DSX
*[Child: 03 — Site & Building Specs]*
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
*[Child: 04 — Government Funding Stack]*
> Marlie I was designed around the incentives — not retrofitted to qualify.
---
## Federal: One Big Beautiful Bill Act (OBBBA)
    - Signed July 4, 2025
    - FEOC restrictions: Chinese/Russian/Iranian/North Korean supply chain = disqualified
    - Marlie I: Texas-manufactured NVIDIA hardware, 100% US ownership, Louisiana GC — fully compliant
    - $500M added to BEAD broadband program
    - Gulf OCS revenue raised to $650M/year through 2034
    - $500B Stargate AI program — Marlie I FEOC-clean structure qualifies
---
## Federal: BEAD Broadband Program
    - LUS Fiber ~0.8 miles from site
    - Marlie I connection accelerates BEAD eligibility for City of Lafayette
---
## State: Louisiana Act 730
    - Effective July 1, 2024
    - 20-year state/local sales & use tax rebate on qualifying AI factory equipment
    - 10-year renewal option (30 years total)
    - Qualification: $200M+ capital investment + 50+ permanent jobs
    - Direct Payment Number eliminates tax liability on GPU hardware
    - Stackable: Quality Jobs Program (6% payroll rebate, 10yr) + LED FastStart (free workforce training)
> 100% US ownership. Texas-manufactured NVIDIA hardware. Louisiana-licensed GC. Zero foreign entity involvement. Marlie I is not just eligible — it is the ideal candidate.
*[Child: 05 — Infrastructure Partners]*
> Every infrastructure partner is not a vendor. They are a node in the same network.
---
## LUS Fiber
    - 214 Jefferson St, Lafayette, LA 70501 — ~0.8 miles from Marlie I
    - Municipal gigabit network — city-owned, no incumbent telco gatekeeping
    - What LUS Fiber gains: anchor industrial fiber customer + BEAD backhaul justification for SE Evangeline corridor
---
## LUS Power / Utilities
    - 1314 Walker Rd, Lafayette, LA 70506 — ~1 mile
    - MARLIE I is off-grid by design (Bloom SOFC primary). LUS Power = emergency backup only.
    - Grid not used for consumption. No sell-back at MARLIE I.
---
## Atmos Energy — Natural Gas
    - 1818 Eraste Landry Rd, Lafayette, LA 70506 — ~3 miles
    - Fuel supply for Bloom SOFC primary generation — 40 units, 10 MW installed
    - Henry Hub benchmark (Erath, LA, ~40 mi) — fuel costs locked to most competitive gas price on earth
    - What Atmos gains: long-term industrial contract, high-volume predictable load, rate stability
---
## SLEMCO Electric
    - 2727 SE Evangeline Thruway — same corridor as Marlie I
    - Emergency backup only
---
## Lafayette Regional Airport (LFT)
    - GPS: 30.20529, -91.98760 — adjacent to Marlie I site
    - ADC3K: FAA Private Pilot Certificate + Part 107 Remote Pilot Certificate
    - Commercial UAS operations: inspection, survey, logistics from day one
    - What LFT gains: active commercial Part 107 operator on the doorstep
---
## City of Lafayette / Louisiana Economic Development (LED)
    - Act 730 qualified — 20-year equipment tax exemption
    - OBBBA compliant — FEOC-clean, Texas-manufactured, Louisiana GC
    - 50+ permanent jobs required for Act 730 certification
    - Lafayette becomes home to Louisiana's first Rubin-class AI factory
    - Hub of ADC3K Louisiana AI Network — three sites planned
---
## Bloom Energy — Primary Power Generation
> 40 Bloom SOFC units. 10 MW installed capacity. Natural gas to 800V DC — no inverter, no rectifier. PRIMARY power for MARLIE I building and all 3 pods.
    - Building downstairs: 10 units — 2,500 kW generation
    - Pod 1: 10 units — 2,500 kW generation
    - Pod 2: 10 units — 2,500 kW generation
    - Pod 3: 10 units — 2,500 kW generation
    - Total: 40 units x 250 kW = 10,000 kW (10 MW)
    - 54% electrical efficiency — best-in-class for on-site generation
    - 800V DC direct output — native to DSX power bus, no conversion loss
    - No battery array required for steady-state — Bloom provides continuous base load
    - 90-day delivery window — no grid interconnect required to operate
---
## Eaton — Power Distribution
    - Eaton Beam Rubin DSX: 800V DC native power distribution
    - Eaton xStorage: 600 kWh LFP battery — ride-through bridge, ATS, millisecond switchover
    - Contact made post-GTC 2026
---
## First Solar — Renewable Energy
    - First Solar Series 7 TR1 panels — $1.1B factory in New Iberia, LA (~30 mi)
    - 300 kW: pod roofs + ground mount on cleared Chag Street parcels
    - Note: No solar on main building roof — tree coverage
    - LOCKED American-made partner. FEOC-clean.
---
## Power Stack — MARLIE I (Locked)
> Bloom SOFC is PRIMARY. Grid is NEVER used for consumption at MARLIE I.
    - Layer 1 (Offset):   Solar — 300 kW — First Solar TR1 — pod roofs + Chag Street ground mount
    - Layer 2 (Primary):  Bloom SOFC — 40 units — 10 MW — 800V DC direct — gas in, DC out
    - Layer 3 (Bridge):   LFP Battery — 600 kWh Eaton xStorage — millisecond ATS — ride-through
    - Layer 4 (Emergency): Diesel genset — hurricane insurance — on-site fuel reserve
    - Layer 5 (Never):    Grid — emergency backup only — not used for consumption — no sell-back
*[Child: 06 — ADC3K Credentials]*
> Scott Tomsu — Owner/Operator — ADC3K (Advantage Design Construction) — Lafayette, LA
---
## Certifications
    - Louisiana General Contractor License — active — eliminates 10-15% GC markup, single accountability
    - 7 NVIDIA Certifications — AI infrastructure design, GPU compute deployment, NVIDIA partner program
    - FAA Private Pilot Certificate
    - FAA Part 107 Remote Pilot Certificate (commercial UAS)
    - CompTIA A+ — earned late 1990s
    - CompTIA Network+ — earned late 1990s
---
## Background
    - 20 years underwater robotics / ROV — Gulf of Mexico oil and gas industry
    - Systems at depth, under pressure, hostile environments — zero tolerance for failure
    - AI factory ops demand the same: continuous uptime, redundant systems, immediate fault response
    - Built 1201 SE Evangeline Thruway himself — 20 years standing, hurricane-proven
---
## Why This Matters
    - No third-party GC — Scott pulls permits, hires trades, executes buildout directly
    - No third-party NVIDIA integrator — 7 certifications = receive, rack, power on
    - Revenue from day one — no markup, no delay, no middlemen
    - Field-hardened systems thinking — not finance, not software — infrastructure operations
*[Child: 07 — Louisiana AI Network: Multi-Site Vision]*
> We are not building an AI factory. We are building a network.
---
## Phase 1 — MARLIE I (Active)
    - Location: 1201 SE Evangeline Thruway, Lafayette, LA 70501
    - Target: H2 2026 operational
    - Building: 24 x 40 ft, 2 floors — downstairs compute (10 racks, single row), upstairs NOC
    - 3 ADC 3K pods on adjacent Chag Street parcels (cleared, prepped)
    - Total: 40 NVL72 racks, 2,880 Rubin GPUs, 40 Bloom SOFC units, 10 MW generation
    - Purpose: home base — cash flow, credibility, playbook for Phases 2 and 3
    - Activation: NOW — investor and infrastructure partner outreach active
---
## Phase 2 — Site Two (In Development)
    - Location: TBD — ADC3K Louisiana Network
    - Funded by Marlie I cash flow — no external fundraising required
    - Playbook: written. Infrastructure relationships: established. Hardware: understood.
    - Activation trigger: Marlie I reaches revenue threshold -> Site Two deploys
---
## Phase 3 — Site Three (In Development)
    - Location: TBD — ADC3K Louisiana Network
    - Completes hub-and-spoke Louisiana AI architecture
    - Combined: enterprise + government + city infrastructure at statewide scale
    - Three sites. One network. One operator.
    - Activation trigger: Site Two operational -> Site Three deploys
---
## Partner Gains Across the Full Network
    - LUS FIBER: Anchor industrial fiber customer + BEAD backhaul justification
    - ATMOS GAS: Long-term industrial gas contract — high-volume predictable load for Bloom fuel supply
    - LFT AIRPORT: Active Part 107 commercial UAS on the doorstep
    - CITY / LED: Louisiana's first Rubin-class AI factory — Act 730, OBBBA, 50+ jobs, Lafayette on national map
ADC3K is not asking the city for a favor. ADC3K is inviting Lafayette's infrastructure partners to build the city's next chapter with us. Every site we add is another node in Lafayette's economic future.
---
## KLFT 1.1 — First Operational Remote Node
    - KLFT 1.1 (Gulf Coast Emergency Drone Deployment Hub) — first remote edge node managed from Marlie I NOC
    - KLFT site: Lafayette Regional Airport adjacent — Part 107 UAS operations hub
    - Command: SkyCommand fleet management, mission dispatch, live video feed
    - Drone platform: Skydio X10 + Skydio Dock (autonomous launch, charge, relay)
    - Edge compute: ADC 3K pod at KLFT site — on-site inference, video processing
    - NOC link: Marlie I aggregates KLFT telemetry, archives incidents, coordinates multi-site missions
    - Revenue model: government/emergency services SaaS + per-mission fees
---
## ADC 3K Pod Deployment Geography — Natural Gas Pipeline Map
ADC 3K pods deploy along Louisiana's natural gas pipeline corridor. Each pod connects to Marlie I via fiber or cellular backhaul. Bloom SOFC in every pod: gas in, tokens out — no grid required.
    - Henry Hub corridor (~40 mi): Erath, LA — Vermilion Parish gas hub — high-density pipeline node
    - Gulf Coast industrial corridor: refineries, LNG terminals, petrochemical plants — captive ADC pod customers
    - New Iberia (Site 2 candidate): solar factory + industrial port + pipeline access
    - Lake Charles / Cameron Parish: LNG export terminals — security/monitoring pod deployment
    - Morgan City: offshore supply base, pipeline terminus — SAR + industrial ADC pod
---
## Ground Zero — Media Arm of the Louisiana AI Network
Ground Zero (@GroundZero-ai) is the YouTube documentary arm that translates ADC ecosystem operations into public-facing content.
    - Audience 1 — General public: AI infrastructure explained at civilian level
    - Audience 2 — Technical/industry: GPU specs, deployment architecture, ROI models
    - Audience 3 — Investor/government: live proof-of-concept — Marlie I, ADC 3K pods, KLFT operations
    - ADC Insider Series: 8 planned episodes documenting MARLIE I buildout, ADC 3K pod deploy, KLFT launch
    - Monetization: YouTube revenue + sponsorships + investor lead generation + NVIDIA partner content
    - Status: EP001 live (private), EP002 in pipeline. Channel: @GroundZero-ai
Ground Zero turns every infrastructure milestone into investor-grade content. The construction of Marlie I IS the content strategy.
---
## MARLIE I Key Specs — Reference
    - 40 NVL72 racks (10 building downstairs + 10 per pod x 3 pods), 2,880 GPUs
    - Building: 24 x 40 ft, single-row 10-rack layout downstairs, NOC upstairs
    - 3 ADC 3K pods: single-row 10-rack layout, 40 ft containers, Chag Street parcels adjacent
    - Power: 40 Bloom SOFC units, 10 MW primary generation, 800V DC native
    - Fiber: LUS (0.8 mi) + dedicated to Willow Glen (60 mi, management only)
    - 0.5 mi from Trappeys. 60 mi from Willow Glen.
*[Child: 08 — Contact & Next Steps]*
## ADC3K — Advantage Design Construction
    - Owner/Operator: Scott Tomsu
    - Address: 1201 SE Evangeline Thruway, Lafayette, LA 70501
    - Email: SCOTT@ADC3K.COM
    - Phone: 337-780-1535
    - Web: www.adc3k.com
---
## Next Steps
    - Infrastructure partner meetings: LUS Fiber, Atmos Energy, LUS Power, LFT Airport
    - Louisiana Economic Development — Act 730 pre-qualification
    - NVIDIA partner program — NVL72 procurement pipeline
    - Investor term sheet discussions
    - Phase 1 buildout kickoff — 6 month deploy timeline
---
> The federal money is flowing. The hardware is in production. The site is ready. The only question is who is at the table when Marlie I goes live.
*[Child: 09 — Financial Architecture & ROI]*
> This is not an AI factory. This is a money machine. Every watt generates revenue. Every dollar goes to compute. The comparison is not close.
---
## Capital Stack
    - Infrastructure raise: ~$1.17M — covers facility buildout (electrical, cooling, fiber, power distribution, commissioning)
    - GPU hardware financed separately: equipment financing + NVIDIA Capital programs + SBA facilities
    - EBITDA figures below = facility-level operating cash flow
    - Full investor pro forma with hardware financing and debt service available upon request
---
## MARLIE I vs Legacy AI Factory — Key Comparison
    - PUE: Legacy 1.4-1.8 (40-80% wasted) vs MARLIE I 1.10 (liquid-cooled, best-in-class)
    - Energy cost: Legacy $0.10-0.18/kWh national avg vs MARLIE I $0.058-0.068/kWh (Bloom SOFC on Henry Hub gas)
    - Cooling: Legacy air (CRAC units, chillers) vs MARLIE I 100% direct-to-chip liquid
    - Revenue per rack per year: Legacy $200K-$500K (colo) vs MARLIE I $3M-$5M+ (AI compute)
    - Operations: Legacy 20-50 FTE manual ops vs MARLIE I 3-5 FTE Mission Control AI
    - On-site generation: Legacy none (grid dependent) vs MARLIE I 40 Bloom SOFC units, 10 MW
    - Domestic content: Legacy mixed overseas vs MARLIE I 100% USA — OBBBA compliant
---
## MARLIE I Configuration
> 40 NVL72 racks — 2,880 Rubin GPUs — 5,200 kW IT — 10 MW Bloom generation
    - Building downstairs: 10 racks, 720 GPUs, 1,300 kW IT — single-row layout, same as pod
    - Building upstairs: NOC only — no compute racks
    - Pod 1: 10 racks, 720 GPUs, 1,300 kW IT
    - Pod 2: 10 racks, 720 GPUs, 1,300 kW IT
    - Pod 3: 10 racks, 720 GPUs, 1,300 kW IT
---
## Revenue Model — AI Compute Rental (Conservative Basis)
Rate basis: $6/GPU/hr base case (H100 spot: $2.50-$3.50/hr; Rubin delivers 2.5x FP4 density and 22 TB/s HBM4 bandwidth — premium tier justified). At $8/GPU/hr mid estimate, Phase 3 gross reaches $151.6M.
### Phase 1 — Building Downstairs (720 GPUs, 10 Racks)
    - 720 GPUs online — building downstairs only
    - 40% utilization (ramp year): 720 x $6 x 8,760 x 0.40 = $15.2M gross
    - 65% utilization (stabilized): 720 x $6 x 8,760 x 0.65 = $24.7M gross
    - OPEX at 65%: ~$2.8M (Bloom fuel + staffing + maintenance)
    - EBITDA at 65%: ~$21.9M
### Phase 2 — Building + Pod 1 (1,440 GPUs, 20 Racks)
    - 1,440 GPUs online — building + Pod 1
    - 65% utilization: 1,440 x $6 x 8,760 x 0.65 = $49.3M gross
    - OPEX: ~$4.5M
    - EBITDA: ~$44.8M
### Phase 3 — Full Footprint (2,880 GPUs, 40 Racks)
    - 2,880 GPUs online — building + all 3 pods
    - 75% utilization at $6/hr: 2,880 x $6 x 8,760 x 0.75 = $113.7M gross
    - 75% utilization at $8/hr: 2,880 x $8 x 8,760 x 0.75 = $151.6M gross
    - OPEX: ~$7.0M
    - EBITDA at $6/hr: ~$106.7M
    - EBITDA at $8/hr: ~$144.6M
---
## Power Resilience — 5 Independent Layers
> Bloom SOFC is PRIMARY. The grid is never used for consumption at MARLIE I.
    1. Solar (Offset): 300 kW — First Solar TR1 — pod roofs + Chag Street ground mount
    1. Bloom SOFC (Primary): 40 units x 250 kW = 10 MW — 800V DC direct — gas in, DC out — 54% efficiency
    1. LFP Battery (Bridge): 600 kWh Eaton xStorage — millisecond ATS — ride-through
    1. Diesel Genset (Emergency): on-site fuel reserve — hurricane insurance — zero production dependency
    1. Grid (Never): LUS emergency backup only — not used for consumption — no sell-back at MARLIE I
Zero single points of failure. 5 independent power layers. Bloom headroom: ~4,280 kW above full facility draw.
---
## Power Economics
    - Bloom SOFC effective cost: $0.058-0.068/kWh (fuel + maintenance, Henry Hub gas basis)
    - IT load: 5,200 kW — facility total at PUE 1.10: ~5,720 kW
    - Bloom generation: 10,000 kW — headroom buffer: ~4,280 kW
    - Annual power cost at Phase 3 / 75% utilization: ~$2.4M
---
## Investor Benefits
    - Reserved bandwidth: GPU compute access during off-peak hours proportional to investment tier. Estimated value: $50K-$500K/month compute credit.
    - Early mover rate lock: investors before first rack goes live receive locked GPU rental rates below market for 24 months
    - Single operator: Scott pulls GC permits, handles NVIDIA integration, runs Mission Control — no markup, no middlemen, revenue from day one
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/5a788f09-7e31-81eb-a3dc-00039a1662d6/9e682da1-85a0-44a9-94e4-61045a297666/Store_Front_Pic.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466SJSNONW6%2F20260406%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260406T214349Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEA0aCXVzLXdlc3QtMiJGMEQCIHhmaK9WQOAhah80dmBsUx1vcZhwT%2F7CDqkeWEoiR%2B%2BDAiBTaEQ8V5D8ZsrcPN6fMT0%2BcK%2Fb2FYqXBW%2Fea15t9w2XiqIBAjW%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMoq6COW0J9VqfS%2F9JKtwDo4NWM9gHSz%2F896BSv6AOxQRktTpG4KPwZhgJNxZFkSwha7RKwxx2vApoBPELJIMET0DfgLtt5gQKrL2fGNkHWd3U9pClz5yr0t33HIT%2BmrlpVZAKDlRKfFgEHKbu4J4g0JYEjbmvY8YtMNdZb%2BCahoKd945AVJmmXBVohPwyRpXy8LHNRO1ZzT0VQDPx6QBSw5lmVoUjlWPLzd%2FjHhJB60Ou9fKlYr2CHYTpz65j%2FCfbl5OlZHzkSMqdns1ApD6wky5gj7JxRvZiU1Re5N%2BpjLYEfYogWJaDJX6BbQlo1ROg7BzePt%2F2SL7s6tv5kkbTQAY34dD0AZuZVvLVyxmFVAuoeQZrQMVlT4wkJXbQOKCT2skmNh6enQk90SyFPVnngMP1Ka9TfusCjkw3kN5FOaGm%2BqyHui7H7OGRSErGHGoSSnR4cuhuRllwQ2v81vLY%2BX5ohhjMdphm4uzIyHVNHzmYaeMgPDUmvMHyNEZK%2BC5b3GgdfgmCZwlY%2FBXgjMRzM29QpwzIyM3BllSjN%2FhsmMFinYxxjxuc%2BH7MUY9zNYV3KcPFE1ZwIIfg3KG6CAEw06%2B%2FyHbU2kBPA%2BAp%2BiI34LYB6aAGa12czDH2gWeq2an%2FNrC55AJ%2Ba3yvr1AwpcTQzgY6pgFjkKPWVHRbJEHF7pfcHu4M%2F16A6AnN0hqkJHQfSO4fXZF8p4Uv8WYw7IR%2BsHpoXHveQhxEhFjscTkFA9sC6fizuLoCDmGsPGQ9tLhilHnkaEKgRyiI%2B33GpxscBtULqkQl%2Bjy0vQstP0ahQbHWp4o9iDiIe766HzJPs0L%2BWoewkT9xnFoDQ01j1VATlPFuQZ21CeDbysMgJukvXal5lORYSx1WObh6&X-Amz-Signature=2f9958dd4fdabb805c18e7d85d599c9589c243319560888e40849a0e2eb0b8c7&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
*[Child: KLFT 1.1]*
### 
*[Child: Mission Control HD — Command Center]*
> Live SaaS at missioncontrolhd.com — vehicle diagnostics platform with AI chat, 41 tools, Stripe subscriptions, and Supabase auth. Next.js 15 + Vercel.
---
## Quick Links
  - Live site: https://missioncontrolhd.com
  - GitHub: https://github.com/Scottay007/mission-control
  - Vercel: mc-vehicle-app2 (Mission Control Pro team)
  - Supabase: Mission Control project — us-west-2
  - Stripe: dashboard.stripe.com (LIVE mode)
  - Local code: C:\Users\adhsc\mission-control
---
## Sub-Pages
  - Project Overview & Tech Stack
  - Stripe & Payments Config
  - Infrastructure & Auth Config
  - Launch Roadmap & Open Issues
  - Session Log
*[Child: Project Overview & Tech Stack]*
# Mission Control HD — Project Overview
> Vehicle diagnostics SaaS. All 41 tools are free. Premium and Pro unlock more AI, vehicles, and wiring/torque PRO tools.
---
## Tech Stack
    - Next.js 15 (App Router) — frontend + API routes
    - Supabase — Auth, Postgres database, Row Level Security
    - Stripe — subscriptions, webhooks (LIVE mode)
    - Anthropic Claude API — AI Diagnostic Chat
    - Vercel — hosting, serverless functions, edge
    - Kit / ConvertKit — email marketing automation
    - Tailwind CSS — dark theme, custom colors
    - Namecheap — domain registration, auto-renew ON
---
## Vehicle Platforms
    - Harley-Davidson (#E8720E) — 7 tools
    - Automotive (#8B5CF6) — 5 tools
    - Trucking (#FF6F00) — 7 tools
    - E-Bike (#22C55E) — 7 tools
    - Scooter (#06B6D4) — 5 tools
    - Universal — 10 tools
    - Total: 41 tools
---
## Pricing Tiers
    - Free — $0 | 3 AI queries/day | 1 vehicle
    - Premium — $9.99/mo ($95.88/yr) | 20 AI queries/day | 3 vehicles | 7-day free trial
    - Pro — $19.99/mo ($191.88/yr) | Unlimited AI | Unlimited vehicles | PRO-gated tools
---
## PRO-Gated Tools
    - HD_Wiring_Reference_v2
    - HD_Torque_Sequences_v2
    - EBike_Wiring_Reference_v2
    - Service_History_Export_v2
---
## Database Schema (Supabase)
    - profiles — user tier, stripe_customer_id, stripe_subscription_id
    - vehicles — user garage entries
    - chat_history — AI diagnostic sessions
    - community_posts — forum posts
    - community_comments — forum replies
    - email_signups — Kit integration
RLS enabled on all tables. Auto-profile trigger fires on signup. Email confirm ON.
---
## Accounts & Access
    - GitHub: Scottay007 — github.com/Scottay007/mission-control
    - Vercel: via GitHub — mc-vehicle-app2
    - Supabase: adhscott@yahoo.com — onvemzmhedyuropiruaf.supabase.co
    - Stripe: adhscott@yahoo.com — LIVE mode
    - Anthropic: adhscott@yahoo.com — console.anthropic.com
    - Kit: adhscott@yahoo.com — app.kit.com
    - Namecheap: Scottay007 — missioncontrolhd.com (expires Feb 23 2027)
*[Child: Stripe & Payments Config]*
# Stripe & Payments Configuration
> Stripe is in LIVE mode as of March 2026. Test mode keys are archived. Do NOT use test price IDs in production.
---
## Live Price IDs
    - Premium Monthly: price_1T2Nbc2a0QlcXNBji9gMD9cW
    - Premium Annual: price_1T2Nd42a0QlcXNBjlG3I0f5M
    - Pro Monthly: price_1T3oMt2a0QlcXNBj8538mT9A
    - Pro Annual: price_1T3oOg2a0QlcXNBj1UmvhyQ0
Archived: Mission Control Shop ($49.99/mo, $499/yr) — do not reactivate.
---
## Webhook Configuration
    - Required endpoint: https://missioncontrolhd.com/api/stripe/webhook
    - Events: checkout.session.completed, customer.subscription.updated, customer.subscription.deleted
    - Signing secret env var: STRIPE_WEBHOOK_SECRET
> OPEN ISSUE: Live mode webhook may not be configured yet. Old test webhook (fascinating-breeze) pointed to mc-vehicle-app2.vercel.app. Create a NEW live mode webhook in Stripe dashboard pointing to https://missioncontrolhd.com/api/stripe/webhook, then update STRIPE_WEBHOOK_SECRET in Vercel.
---
## Vercel Environment Variables — Stripe
    - STRIPE_SECRET_KEY — live sk_live_ key
    - NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY — live pk_live_ key
    - STRIPE_WEBHOOK_SECRET — whsec_ signing secret from live webhook
    - STRIPE_PREMIUM_MONTHLY_PRICE_ID — price_1T2Nbc2a0QlcXNBji9gMD9cW
    - STRIPE_PREMIUM_ANNUAL_PRICE_ID — price_1T2Nd42a0QlcXNBjlG3I0f5M
    - STRIPE_PRO_MONTHLY_PRICE_ID — price_1T3oMt2a0QlcXNBj8538mT9A
    - STRIPE_PRO_ANNUAL_PRICE_ID — price_1T3oOg2a0QlcXNBj1UmvhyQ0
---
## Checkout Flow
    - User clicks tier button on /pricing → handleCheckout(tier) fires
    - POST /api/stripe/checkout — creates Stripe Checkout Session with userId + tier in metadata
    - User completes payment on Stripe-hosted page
    - Stripe fires checkout.session.completed webhook
    - Webhook updates profiles table: tier, stripe_customer_id, stripe_subscription_id
    - Premium monthly: 7-day free trial automatically applied
---
## Annual Pricing
    - Premium Annual: $95.88/yr (equiv $7.99/mo — 20% off)
    - Pro Annual: $191.88/yr (equiv $15.99/mo — 20% off)
*[Child: Infrastructure & Auth Config]*
# Infrastructure & Auth Configuration
---
## Vercel
    - Project: mc-vehicle-app2 (Mission Control Pro team)
    - Region: iad1 (US East)
    - Live URL: https://missioncontrolhd.com
    - Old URL still works: https://mc-vehicle-app2.vercel.app
    - Health cron: /api/health runs daily at 12:00 UTC
To add/change env vars: Vercel dashboard → mc-vehicle-app2 → Settings → Environment Variables
---
## All Vercel Environment Variables
    - NEXT_PUBLIC_SITE_URL = https://missioncontrolhd.com
    - ANTHROPIC_API_KEY = sk-ant-... (set)
    - NEXT_PUBLIC_SUPABASE_URL = https://onvemzmhedyuropiruaf.supabase.co
    - NEXT_PUBLIC_SUPABASE_ANON_KEY = (set)
    - SUPABASE_SERVICE_ROLE_KEY = (set)
    - STRIPE_SECRET_KEY = sk_live_... (set)
    - NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY = pk_live_... (set)
    - STRIPE_WEBHOOK_SECRET = whsec_... (set — verify matches live webhook)
    - STRIPE_PREMIUM_MONTHLY_PRICE_ID = price_1T2Nbc2a0QlcXNBji9gMD9cW
    - STRIPE_PREMIUM_ANNUAL_PRICE_ID = price_1T2Nd42a0QlcXNBjlG3I0f5M
    - STRIPE_PRO_MONTHLY_PRICE_ID = price_1T3oMt2a0QlcXNBj8538mT9A
    - STRIPE_PRO_ANNUAL_PRICE_ID = price_1T3oOg2a0QlcXNBj1UmvhyQ0
    - KIT_API_KEY = (set)
> Local .env.local has wrong values from earlier sessions. Always use Vercel dashboard for production values.
---
## Supabase
    - Project: Mission Control (us-west-2, Oregon)
    - URL: https://onvemzmhedyuropiruaf.supabase.co
    - Auth: email/password, confirm email ON
> OPEN ISSUE: Supabase auth redirect URLs still pointing to old vercel.app domain. Go to Supabase → Authentication → URL Configuration → Set Site URL to https://missioncontrolhd.com and add https://missioncontrolhd.com/** to Redirect URLs.
---
## Domain & DNS (Namecheap)
    - Domain: missioncontrolhd.com
    - Registrar: Namecheap — Scottay007 account
    - Expires: Feb 23, 2027 — auto-renew ON
    - A Record: @ → 76.76.21.21
    - CNAME: www → 4211f3971db6198f.vercel-dns-016.com
---
## Key File Locations (local)
    - src/app/api/stripe/webhook/route.js — webhook handler
    - src/app/api/stripe/checkout/route.js — checkout session creator
    - src/app/pricing/page.jsx — pricing + checkout buttons
    - src/app/login/page.jsx — login + forgot password
    - src/lib/supabase.js — browser + admin clients
    - src/lib/constants.js — TIERS definition
    - artifacts/ — 41 tool source components
    - emails/ — 6 HTML email templates
*[Child: Launch Roadmap & Open Issues]*
# Launch Roadmap & Open Issues
> Site is LIVE. Most critical bugs are fixed. Remaining items are config tasks (Stripe webhook, Supabase URLs) and launch prep.
---
## Critical — Fix Before Marketing Push
    - [OPEN] Stripe live mode webhook — create at https://missioncontrolhd.com/api/stripe/webhook, update STRIPE_WEBHOOK_SECRET in Vercel
    - [OPEN] Supabase auth redirect URLs — update Site URL + add missioncontrolhd.com/** in Supabase Authentication settings
    - [VERIFY] Premium ($9.99) button — likely fixed by auth lock fix (c1eeee5), needs live test
    - [OPEN] Account page email field blank — email shows empty on profile page
---
## Medium Priority
    - Stripe webhook URL update — verify Vercel forwards correctly or update endpoint to missioncontrolhd.com
    - GitHub OAuth for production — set callback URL to missioncontrolhd.com
    - Google OAuth for production — set callback URL to missioncontrolhd.com
    - Supabase custom SMTP — switch from default to Resend
    - Supabase auth email templates — customize signup, reset password emails
---
## Launch Prep
    - OG images and app icons
    - Blog posts — 5 written, need adding to /blog page
    - Kit email automation sequences — morning briefs for Premium
    - ProductHunt launch
    - Reddit post (r/webdev, r/SaaS, r/Harley, r/ebike)
    - Social media (TikTok, Instagram, X/Twitter, LinkedIn)
---
## Completed (as of March 2026)
    - [DONE] Build error in harley/flowcharts/page.jsx — fixed in 6f9ee19
    - [DONE] Forgot password / password reset — fixed in ff7ba2a + fb6a988
    - [DONE] Stripe userId not passed to checkout — fixed in 5f48ba0
    - [DONE] Moved to live Stripe keys — fd1e6bd + 1141e5f
    - [DONE] Supabase auth lock timeout — fixed in c1eeee5
    - [DONE] Custom domain missioncontrolhd.com — live
    - [DONE] All 41 tools migrated to routes
    - [DONE] Stripe Pro checkout working end-to-end
---
## Git Quick Reference
Push changes to production:
    - cd C:\Users\adhsc\mission-control
    - git add .
    - git commit -m "describe change"
    - git push
Run locally: npm run dev → http://localhost:3000
---
> CRITICAL FIX CHECKLIST (2026-03-23)
Scott — do these 2 things to unblock MCHD launch:
## Fix 1: Stripe Webhook (5 minutes)
    1. Go to https://dashboard.stripe.com/webhooks
    1. Click 'Add endpoint'
    1. URL: https://missioncontrolhd.com/api/stripe/webhook
    1. Events to listen for: checkout.session.completed, customer.subscription.created, customer.subscription.updated, customer.subscription.deleted, invoice.payment_succeeded, invoice.payment_failed
    1. Copy the webhook signing secret (whsec_...)
    1. Go to Vercel Dashboard → mc-vehicle-app2 → Settings → Environment Variables
    1. Set STRIPE_WEBHOOK_SECRET = the whsec_ value you copied
    1. Redeploy (Vercel → Deployments → Redeploy latest)
## Fix 2: Supabase Redirect URLs (3 minutes)
    1. Go to https://supabase.com/dashboard → your project → Authentication → URL Configuration
    1. Change Site URL to: https://missioncontrolhd.com
    1. Add to Redirect URLs: https://missioncontrolhd.com/**, https://missioncontrolhd.com/auth/callback
    1. Remove any old vercel.app URLs (mc-vehicle-app2.vercel.app)
    1. Save
## Fix 3: Verify Premium Button (2 minutes)
After fixes 1 and 2, go to missioncontrolhd.com, sign up, click Premium, verify Stripe checkout loads.
## Fix 4: Account Page Email (investigate)
The account page reads email from user?.email (Supabase auth session). If email shows blank, the likely cause is the Supabase redirect URL issue (Fix 2) — the session is not persisting correctly on the custom domain. Fix 2 should resolve this. If email is still blank after Fix 2, check Supabase → Authentication → Users to confirm the email is stored.
---
Total time: ~10 minutes. Then MCHD is launch-ready.
Code verified: webhook handler at src/app/api/stripe/webhook/route.js handles all required events correctly. No old vercel.app URLs found in source code. The blockers are purely dashboard configuration.
*[Child: Session Log]*
# Mission Control HD — Session Log
Track what was done each work session.
---
## Session 3 — Feb 23, 2026
    - Custom domain missioncontrolhd.com purchased and connected
    - NEXT_PUBLIC_SITE_URL updated to https://missioncontrolhd.com
    - STRIPE_WEBHOOK_SECRET rolled to new secret
    - Supabase auth lock timeout fixed (lock: { enabled: false })
    - All 44 dashboard tools verified visible and clickable
    - Stripe Pro checkout tested end-to-end — payment succeeds
    - Claude AI diagnostic chat tested — working
---
## Session 4 — March 2026
    - Moved to live Stripe keys (fd1e6bd, 1141e5f)
    - Fixed: build error in harley/flowcharts/page.jsx (6f9ee19)
    - Fixed: forgot password / password reset (ff7ba2a, fb6a988)
    - Fixed: Stripe userId + email now passed to checkout (5f48ba0)
    - Project knowledge loaded into Mission Control (gpu-learning-lab) memory system
    - Mission Control HD Command Center created in Notion
---
## Session 5 — March 9, 2026 (Onboarding + CC Build)
    - Full project onboarded into Mission Control knowledge system (gpu-learning-lab)
    - memory/projects/missioncontrolhd.md created — full project snapshot
    - MCHD Command Center built in Notion under Mission Control HQ
    - 5 sub-pages created: Project Overview & Tech Stack, Stripe & Payments Config, Infrastructure & Auth Config, Launch Roadmap & Open Issues, Session Log
    - Confirmed page ID: 31e88f09-7e31-8182-900a-cac36f525edc
    - Two critical blockers confirmed open: Stripe live webhook + Supabase auth redirect URLs
    - All code bugs from pre-Feb 23 backup confirmed fixed — no code changes needed this session
    - Ecosystem cross-reference audit: MCHD is standalone SaaS — not part of ADC 3K pod product line
*[Child: Ground Zero — Command Center]*
> YouTube channel @GroundZero-ai — AI news show. AIDO pipeline handles TTS, B-roll, render, and upload. EP001 is private and live. EP002 in pipeline.
---
## Quick Links
  - Channel: @GroundZero-ai
  - EP001: https://www.youtube.com/watch?v=2B-W9d6aLEw (private)
  - Domain: groundzeroai.com
  - Pipeline code: aido/ in gpu-learning-lab repo
---
## Sub-Pages
  - Episode Production Guide
  - AIDO Pipeline Reference
  - Social & Distribution
  - Episode Archive
*[Child: Episode Production Guide]*
# Episode Production Guide
> Standard process for producing a Ground Zero AI news episode end-to-end.
---
## Episode Format
    - Style: AI news show — lower-third news template
    - Audio: ElevenLabs eleven_multilingual_v2, stability=0.32, style=0.55
    - 6 audio segments per episode
    - B-roll: Pexels API (requires PEXELS_API_KEY)
    - Render: local or RunPod Omniverse (requires RUNPOD_POD_IP)
---
## Production Workflow
    - 1. Story selected and added to Story Pipeline database
    - 2. Manifest written (episode metadata, script, segment timing)
    - 3. TTS generated: python -m aido.tts_generate --episode EP00X
    - 4. B-roll injected: python -m aido.inject_content --episode EP00X
    - 5. Episode rendered: python -m aido.pipeline --episode EP00X --local-render
    - 6. Review and approve
    - 7. Upload: python -m aido.pipeline --episode EP00X --from-stage upload --privacy private
---
## Environment Variables Required
    - ANTHROPIC_API_KEY — script generation
    - ELEVENLABS_API_KEY — TTS audio
    - PEXELS_API_KEY — B-roll footage (NOT YET SET)
    - RUNPOD_POD_IP — Omniverse render mode (NOT YET SET)
    - youtube_token.json — OAuth token in project root
---
## Open Blockers
> PEXELS_API_KEY not set — B-roll falls back to noise. Get key at pexels.com/api.
> RUNPOD_POD_IP not set — Omniverse render blocked. Use --local-render as workaround.
*[Child: AIDO Pipeline Reference]*
# AIDO Pipeline Reference
AI Daily Omniverse pipeline modules — located in aido/ directory of gpu-learning-lab repo.
---
## Pipeline Modules
    - manifest_schema — episode manifest validation
    - tts_generate — ElevenLabs TTS audio generation
    - inject_content — B-roll and asset injection
    - render_episode — Omniverse scene render
    - assemble — combine audio, video, lower-thirds
    - render_local — local render fallback (no RunPod)
    - upload_youtube — YouTube OAuth upload
    - pipeline — full orchestrator, runs all stages
---
## TTS Settings (EP001 reference)
    - Model: eleven_multilingual_v2
    - Stability: 0.32
    - Style: 0.55
    - 6 segments per episode
---
## YouTube OAuth
    - Token file: youtube_token.json in project root
    - Google account: dedicated business account
    - Chrome profile: dedicated Ground Zero profile
    - Handle: @GroundZero-ai
---
## Common Commands
Full render from scratch: python -m aido.pipeline --episode EP002 --local-render
Upload only: python -m aido.pipeline --episode EP002 --from-stage upload --privacy private
TTS only: python -m aido.tts_generate --episode EP002
*[Child: Social & Distribution]*
# Social & Distribution
---
## YouTube
    - Channel: @GroundZero-ai
    - EP001: https://www.youtube.com/watch?v=2B-W9d6aLEw (private)
    - EP002: In production pipeline
---
## Social Accounts — NEEDED
> Social accounts not yet created. All should use handle @GroundZeroAI.
    - TikTok — @GroundZeroAI (NOT CREATED)
    - Instagram — @GroundZeroAI (NOT CREATED)
    - X/Twitter — @GroundZeroAI (NOT CREATED)
    - LinkedIn — @GroundZeroAI (NOT CREATED)
---
## Domain
    - groundzeroai.com — register/verify ownership
---
## Launch Checklist — Do These In Order
> Complete these before publishing EP001 publicly. Each one is a 15-30 minute task.
    - [ ] Create TikTok account — @GroundZeroAI
    - [ ] Create Instagram account — @GroundZeroAI
    - [ ] Create X/Twitter account — @GroundZeroAI
    - [ ] Create LinkedIn page — @GroundZeroAI
    - [ ] Register groundzeroai.com domain (or verify ownership)
    - [ ] Get PEXELS_API_KEY — free at pexels.com/api — paste into Vercel + local .env
    - [ ] Set channel description, banner, and profile photo on YouTube
    - [ ] Link groundzeroai.com to YouTube channel (YouTube Studio → Customization → Basic Info)
    - [ ] Set EP001 to Public
    - [ ] Post EP001 clip to TikTok, Instagram Reels, X on same day
---
## Content Distribution Per Episode
    - YouTube: Full episode upload (primary)
    - TikTok: 60-90 second highlight clip from best segment
    - Instagram Reels: Same clip as TikTok or separate angle
    - X/Twitter: Thread summarizing 3 key points + YouTube link
    - LinkedIn: Long-form post with business angle + YouTube link (Gulf Coast / ADC ecosystem audience)
*[Child: Episode Archive]*
# Episode Archive
---
## EP001 — NVIDIA's $4B Photonics Play
    - Status: Rendered, private on YouTube
    - URL: https://www.youtube.com/watch?v=2B-W9d6aLEw
    - Version: v3 (final)
---
## EP002 — Apple M5 Fusion, OpenAI GitHub Rival, Nuclear Powers AI
    - Status: In Story Pipeline — not yet rendered
---
## Story Pipeline (5 stories queued)
    - AI inference identified as critical cybersecurity battleground
    - Amazon acquires 122-acre GWU campus in Ashburn VA for $427M
    - Apple unveils M5 Pro and M5 Max with Fusion Architecture
    - Largest anti-AI protest marches through London King's Cross tech hub
    - NVIDIA invests $4B in photonics companies Lumentum and Coherent
---
## ADC Ecosystem Episodes — Planned
> These episodes leverage the ADC insider advantage. Produce as projects develop.
    - EP-ADC-01: Why Louisiana for AI Infrastructure
    - EP-ADC-02: Immersion Cooling Explained — Louisiana heat + ADC 3K pods
    - EP-ADC-03: NVIDIA Vera Rubin NVL72 — 3.6 ExaFLOPS per rack explained
    - EP-ADC-04: Bloom Energy + Natural Gas — powering edge compute off-grid
    - EP-ADC-05: Gulf Coast Emergency Drone Hub — KLFT + SkyCommand
    - EP-ADC-06: Building MARLIE I — Phase 1 documentary
    - EP-ADC-07: New Iberia Solar — Louisiana renewable manufacturing
    - EP-ADC-08: Edge vs. Hyperscale — why distributed AI wins for the Gulf Coast
*[Child: Content Strategy & Mission]*
> Ground Zero is not just a YouTube channel. It is the media and public relations arm of the entire ADC infrastructure ecosystem — building audience credibility, documenting the journey, and creating awareness in the Louisiana business and tech community before MARLIE I goes live.
---
## Mission Statement
Ground Zero covers the AI infrastructure revolution from the inside. While every other AI news channel reports on what NVIDIA, Google, and OpenAI are doing, Ground Zero reports on what those technologies mean for the Gulf Coast, for Louisiana industry, and for the businesses and communities that will run on this infrastructure. We have the insider angle — because we are building it.
---
## Target Audience — Three Layers
### Layer 1 — AI & Tech Enthusiasts (Broad)
    - Demographics: 25-45, tech-curious, follows AI news, works in tech or adjacent fields
    - What they want: Clear explanations of AI breakthroughs, what matters vs. hype, real-world applications
    - How we serve them: Fast, well-produced AI news with context — no jargon, no filler
### Layer 2 — Business & Industry (Gulf Coast Focus)
    - Demographics: Louisiana/Gulf Coast business owners, energy sector, industrial, municipal decision-makers
    - What they want: How AI affects their industry, what infrastructure is coming to their region, who the local players are
    - How we serve them: Louisiana-specific angles, local economic impact stories, Gulf Coast infrastructure coverage
### Layer 3 — Investors & Partners (High Value)
    - Demographics: Angel investors, VCs, economic development officials, potential ADC tenants and partners
    - What they want: Credibility signals, proof of execution, evidence that the team knows the space
    - How we serve them: Deep technical accuracy, infrastructure investment angles, demonstrating that ADC leadership understands the market
---
## Content Pillars
### 1. AI Infrastructure News (Weekly)
    - NVIDIA, AMD, Intel hardware releases — what they mean for edge compute
    - Data center industry moves — hyperscale vs. edge, capacity announcements
    - Energy and power for AI — natural gas, nuclear, solar, hydrogen
    - Drone and autonomous systems — FAA policy, platform developments, Gulf Coast applications
### 2. Louisiana & Gulf Coast AI (Bi-weekly)
    - Local infrastructure development — what's being built and by whom
    - Energy sector AI — petrochemical, pipeline, offshore applications
    - Municipal AI — smart city, emergency response, public safety
    - University research — UL Lafayette, LSU, Tulane AI programs
### 3. ADC Insider Series (Monthly — when ready)
    - Building MARLIE I — documentary-style build journal
    - ADC 3K pod deployment — first unit install at Trappeys Cannery
    - KLFT SkyCommand — Gulf Coast Emergency Drone Hub development
    - Behind the infrastructure — cooling systems, power architecture, network design
---
## The ADC Insider Advantage
> No other Gulf Coast media outlet can cover AI infrastructure from the inside. Ground Zero is built by the people building the infrastructure. This is the unfair advantage — and it compounds over time as ADC projects go live.
    - EP001 covered NVIDIA photonics — we have NVIDIA Vera Rubin NVL72 on order. We are the customer.
    - Every story about GPU compute, data centers, and edge AI is a story about what we are building
    - KLFT/SkyCommand episodes establish credibility before the hub is operational
    - MARLIE I build journal creates investor awareness before the fundraise closes
    - Louisiana audience: No competing voice covering Gulf Coast AI infrastructure from this angle
---
## ADC Ecosystem Story Pipeline
These episodes should be produced as ADC projects develop. Each one builds credibility and awareness.
    - EP-ADC-01: Why Louisiana for AI Infrastructure — natural gas, LUS Fiber, low power cost, ITEP incentives
    - EP-ADC-02: Immersion Cooling Explained — why ADC 3K pods use full immersion in Louisiana heat
    - EP-ADC-03: NVIDIA Vera Rubin NVL72 — what 3.6 ExaFLOPS per rack means for regional AI
    - EP-ADC-04: Bloom Energy + Natural Gas — how ADC powers edge compute without grid dependency
    - EP-ADC-05: Gulf Coast Emergency Drone Hub — KLFT, SkyCommand, and hurricane response AI
    - EP-ADC-06: Building MARLIE I — Phase 1 construction documentary
    - EP-ADC-07: New Iberia Solar — supporting Louisiana's renewable manufacturing industry
    - EP-ADC-08: The Edge vs. Hyperscale Debate — why distributed AI wins for the Gulf Coast
---
## Monetization Roadmap
### Phase 1 — Build Audience (Now → 1,000 subscribers)
    - YouTube AdSense (minimal revenue — not the goal yet)
    - Establish credibility and consistent publishing cadence
    - Goal: Be the recognized voice for Gulf Coast AI infrastructure
### Phase 2 — Sponsorships (1,000 → 10,000 subscribers)
    - Infrastructure vendors: cooling systems, power equipment, networking gear
    - Louisiana business services: energy, legal, finance, construction
    - AI software platforms: inference, monitoring, MLOps tools
### Phase 3 — Strategic Value (ADC launches)
    - Ground Zero audience = pre-warmed investor and tenant pipeline for MARLIE I
    - Media credibility accelerates ADC partnership conversations
    - Channel becomes a recruiting and awareness tool for ADC talent pipeline
    - Potential: ADC-branded content series, sponsored episodes, paid workshops
---
## Publishing Cadence Target
    - Minimum: 1 episode per week once social accounts are live
    - Ideal: 2 episodes per week — 1 general AI news, 1 Gulf Coast / ADC angle
    - Format: 8-12 minutes per episode — long enough for depth, short enough for retention
    - Distribution: YouTube (primary) + TikTok clips + Instagram Reels + LinkedIn long-form
---
## Strategic Role
> Ground Zero is the media arm of the ADC ecosystem. Every episode builds audience credibility, investor awareness, and Louisiana business recognition before MARLIE I opens and ADC 3K pods deploy. See Content Strategy & Mission for full plan.
  - Channel: @GroundZero-ai (YouTube) | Handle everywhere: @GroundZeroAI
  - ADC Insider Series: Document MARLIE I build, ADC 3K first deployment, KLFT SkyCommand hub
  - Audience: AI/tech enthusiasts (broad) + Gulf Coast business (regional) + investors/partners (high value)
---
> MERGED 2026-03-23: Ground Zero and AI Daily Omniverse are now ONE project.
## Ground Zero - Unified YouTube Strategy
### Channel: @ScottTomsu (YouTube)
NOT @GroundZero-ai. Use Scott's existing channel which already has the LinkedIn post live and connections building. One person, one brand, one channel.
### Content Strategy (Merged):
  - Short-form (2-5 min): Screen record + voiceover. Louisiana initiative, blueprints, renders, tech explainers. Weekly.
  - Long-form (8-12 min): Omniverse-rendered episodes when pipeline is ready. Monthly goal.
  - LinkedIn cross-post everything - LinkedIn is the primary audience right now (14 impressions in 2 hrs with zero subscribers)
### 5 Video Scripts Ready (2026-03-23):
  - 1. "Louisiana Has ZERO GPUs. Florida Has 504." (~2:30)
  - 2. "Two Abandoned Buildings -> AI Factories" (~3:00)
  - 3. "AI Runs My Entire Business" (~3:30)
  - 4. "800 Volts DC - Why This Changes Everything" (~2:30)
  - 5. "Nobody Is Filing the Paperwork" (~3:00) - RECORD THIS FIRST (8 days to NVIDIA deadline)
Scripts at: scripts/youtube/ground-zero-scripts.md
### Production Pipeline:
  - Quick videos: Phone + screen capture. No fancy editing needed.
  - Omniverse episodes: RunPod L40S pod (ml4cl3icn37ys1), Kit SDK 109, render agent on port 8501, 250GB network volume
  - TTS: ElevenLabs (configured, stability=0.32, style=0.55)
  - Thumbnails: FLUX Schnell ($0.003 each)
### What's Done:
  - EP001 rendered, private on YouTube (make PUBLIC)
  - EP002 scripted, not rendered
  - 5 new scripts from today
  - Scene Design Package v1.0 (20m command floor, 6 zones)
  - React dashboard component
  - Branding defined (dark #06080d, cyan #00f0ff)
### What's NOT Done:
  - Social accounts (TikTok, Instagram, X) - NOT CREATED
  - groundzeroai.com domain - NOT REGISTERED
  - PEXELS_API_KEY - NOT SET
  - Full Omniverse render pipeline - NOT TESTED end-to-end with current Kit SDK 109
### Priority
Ship imperfect content NOW. Stop waiting for world-class production. Record Video 5 with a phone and screen capture this week.
*[Child: Site Acquisition Pipeline]*
> Mission: identify, evaluate, and onboard Louisiana AI infrastructure sites. Every site gets the right technology: Full Factory (CDU racks) | ADC 3K Pods (immersion) | Mixed. All sites connect back to MARLIE I NOC. All sites get EV charging.
---
## Active Site Registry
Current pipeline — sorted by priority / meeting date:
  - COTEAU LA — Sugar Cane Field (PRIORITY 1 — meeting tomorrow) | Full AI Factory candidate
  - Lafayette Airport Frontage — Former Alpha Office (Hwy 90) | CDU Rack facility candidate
  - Pinhook & Hwy 90 — Former Hotel Base Structure | ADC 3K Pod candidate
  - New Iberia Solar Factory — Energy partner + Site 2 ADC pod (already in MARLIE I docs)
---
## Site Classification Framework
Each site gets classified on first visit. Classification drives tech selection.
  - TYPE A — Full AI Factory: large lot or building, CDU liquid cooling, NVL72 racks, NOC-capable. Clean slate preferred. Examples: Coteau lot, Airport building
  - TYPE B — ADC 3K Pod Site: any metal structure, full immersion (EC-110), no HVAC. Examples: Trappeys, Hotel base, pipeline-adjacent industrial
  - TYPE C — Mixed Hub: Type A facility + Type B pod farm on same or adjacent property. Highest value per site.
---
## Standard Site Evaluation Checklist
Run this checklist on every site visit. Answers determine type + investment tier.
  - LAND: Size (acres/sq ft), ownership (buy vs lease), blighted/clear title, flood zone (FEMA X preferred)
  - POWER: 3-phase service available? Utility provider. Service size (amps/kW). Upgrade cost estimate.
  - GAS: Natural gas line proximity. Provider (Atmos/CenterPoint). Distance to tap.
  - FIBER: LUS Fiber or carrier conduit path. Distance. Lit or dark.
  - ZONING: Industrial, commercial, or residential? Rezoning risk?
  - STRUCTURE: Existing building usable (CDU rack type)? Or clear lot (new build / pod drop)?
  - COOLING: If building — ceiling height, HVAC load, structural capacity for CDU. If lot — space for dry coolers.
  - EV: Utility transformer upgrade for EV charging? Parking/access for charger placement?
  - NEIGHBORS: Proximity to pipeline, airport, LNG, port, city infrastructure = customer or partner?
  - OWNER: Buy price or lease rate. Owner motivation. Timeline. Known for 30 years = fast track?
---
## EV Charging Standard — Every Site
> Every ADC site gets EV charging. Designed as infrastructure — not a gas station. Aesthetic: utility substation look. Low profile, fits urban/industrial context. Revenue stream: charging fees + grid relationship + future autonomous vehicle positioning.
  - Level 2 (AC): 7-19 kW per port — standard vehicles, overnight fleet charging
  - DC Fast Charge: 50-150 kW per port — commercial vehicles, public use, grid demand response
  - Design standard: metal enclosure, utility aesthetic, no gas station branding
  - Integration: powered from site generation (nat gas / solar / Bloom) — not grid-dependent
  - KLFT tie-in: drone recharge pad at EV charging sites — shared power infrastructure
  - Future: autonomous vehicle charging — same hardware, software upgrade only
---
## Louisiana Infrastructure Network — Vision
The goal is a distributed Louisiana AI + energy + airspace network. Each node generates compute revenue, EV charging revenue, and drone operations capability. MARLIE I is the brain. Every other site is a node. Mission Control AI manages all of them.
  - Lafayette core: MARLIE I (HQ/NOC) + KLFT (drone hub) + Airport site + Pinhook hotel site
  - Coteau corridor: Full AI Factory + pipeline access + New Iberia Solar proximity
  - New Iberia: Solar factory + ADC pod + KLFT Site 2 (drone)
  - Gulf Coast expansion: Lake Charles, Morgan City, Cameron Parish — pipeline-driven pod drops
  - EV grid: every node a charging point — city infrastructure, not a destination
  - Airspace: KLFT drone network covers Lafayette → Coteau → New Iberia corridor
*[Child: Lafayette Airport Frontage — Former Alpha Office (Hwy 90)]*
> STATUS: PROSPECT — For sale sign observed. Airport property. Large one-story building. CDU rack installation candidate (TYPE A). Not suited for immersion pods — existing structure optimized for rack cooling.
---
## Site Overview
    - Location: Hwy 90 frontage road, Lafayette Regional Airport (LFT) adjacent
    - Structure: Former Alpha office building — large, one-story
    - Status: For sale (airport listing observed)
    - Classification: TYPE A — CDU rack facility (same model as MARLIE I)
    - Why not pods: existing building optimized for rack cooling, not immersion container drop
---
## Strategic Value
> Airport AI is inevitable. Air traffic control AI agents will replace human controllers — safer, faster, never fatigued. Being the compute provider at the airport positions ADC as the foundational infrastructure for Lafayette's autonomous airspace.
    - Primary customer: Lafayette Regional Airport — AI for ATC, ground ops, logistics
    - Secondary: airline ops AI, baggage handling optimization, gate scheduling
    - KLFT integration: drone network hub adjacent to airport = Part 107 + future BVLOS airspace
    - EV: airport EV charging = rental car fleet, employee parking, future autonomous ground vehicles
    - Backup compute: every airport will need N+1 AI redundancy — we own the backup site
---
## Site Evaluation — Needed
    - Contact: Lafayette Regional Airport authority — identify listing agent or contact
    - Building size: get sq ft, ceiling height, structural load capacity
    - Power: airport will have heavy 3-phase service — confirm capacity for NVL72 racks
    - Cooling: CDU schematics apply — hot aisle/cold aisle, exterior dry coolers
    - Fiber: LFT adjacent to MARLIE I (adjacent lot) — direct dark fiber path possible
    - FAA considerations: Part 77 obstruction surfaces — height limits near runway
    - Zoning: airport-adjacent commercial/industrial — confirm data center use permitted
---
## KLFT Tie-In
    - Airport site + KLFT = unified airspace intelligence platform
    - SkyCommand runs on ADC 3K pod at KLFT, syncs to Airport site NOC
    - Airport site becomes the South Louisiana drone operations backup NOC
    - Future: autonomous air taxi (eVTOL) charging and dispatch infrastructure
*[Child: Pinhook & Hwy 90 — Former Hotel Base Structure]*
> STATUS: PROSPECT — Demolished hotel, base structure remains. Urban core location. ADC 3K pod site (TYPE B). Key intersection visibility. Identify owner before approaching.
---
## Site Overview
    - Location: Corner of Pinhook Rd and Hwy 90, Lafayette — high-visibility urban intersection
    - Structure: Former hotel — demolished, base/slab structure remaining
    - Classification: TYPE B — ADC 3K immersion pod deployment
    - Why pods: cleared base structure = drop-in container deployment, no full rebuild needed
---
## Strategic Value
> Urban core pod sites are the most visible proof of concept. A clean, utility-aesthetic pod installation at a major Lafayette intersection is the physical billboard for the ADC ecosystem. Every commuter sees it.
    - Urban density: Pinhook/90 = high-traffic, high-visibility — ADC brand presence in the city core
    - Blighted to productive: ideal ADC narrative — turning Lafayette's deteriorating properties into infrastructure
    - EV charging: this intersection is perfect for a public-facing DC fast charge hub
    - Nearby customers: commercial corridor, retail, office — edge compute for local businesses
    - Ground Zero: abandoned hotel turned AI infrastructure = documentary episode
---
## Site Evaluation — Needed
    - Owner: identify current owner — tax assessor record for parcel at Pinhook/Hwy 90
    - Base structure: assess slab condition, utility stubs (power, gas, water) still in place?
    - Power: 3-phase available at the road? Utility transformer upgrade cost?
    - Zoning: commercial/urban — data center/industrial use permitted?
    - Size: how many 40-ft ISO containers fit on the footprint?
    - Flood zone: Pinhook corridor — verify FEMA zone (some areas flood-prone)
---
## Pod Deployment Concept
    - 2-4 ADC 3K pods on the slab — immersion cooled, EC-110
    - EV charging canopy: integrated aesthetic structure covering charging ports and pod exterior
    - Drone pad: rooftop of pod enclosure = KLFT relay point in the city core
    - Ground-level: utility substation aesthetic — metal cladding, no branding overkill
    - NOC link: LUS Fiber down Pinhook — connect to MARLIE I
*[Child: Site Evaluation Framework & Scoring]*
> Use this framework on every site visit and property evaluation. Produces a TYPE classification and Priority Score. Run before any LOI or acquisition conversation.
---
## Step 1 — Classify the Site
    - TYPE A (Full AI Factory): Large lot OR existing large building. CDU rack cooling. NVL72 racks. NOC build-out.
    - TYPE B (ADC 3K Pod Site): Any metal structure OR cleared slab. Full EC-110 immersion. Container drop-in.
    - TYPE C (Mixed Hub): Enough land/building for BOTH Type A facility AND Type B pod farm.
    - TYPE D (EV/Drone Only): Location too small or wrong zoning for compute, but valid for EV charging + KLFT relay.
---
## Step 2 — Score the Location (1-5 each)
    - Power access: 5=3-phase on property, 4=3-phase at road, 3=upgrade needed, 2=residential only, 1=none
    - Gas access: 5=line on property, 4=within 1 mile, 3=1-5 miles, 2=5+ miles, 1=none
    - Fiber access: 5=LUS Fiber lit, 4=conduit in road, 3=wireless backhaul viable, 2=long haul needed, 1=none
    - Owner situation: 5=known 30 years/motivated seller, 4=known contact, 3=cold approach, 2=complicated title, 1=unavailable
    - Flood risk: 5=Zone X high ground, 4=Zone X, 3=Zone AE with mitigation, 2=Zone AE, 1=Zone VE/flood plain
    - Customer proximity: 5=anchor tenant identified, 4=multiple industries adjacent, 3=commercial corridor, 2=residential, 1=isolated
    - Zoning: 5=industrial/heavy, 4=commercial, 3=mixed use (variance possible), 2=residential (hard rezone), 1=protected
---
## Step 3 — Determine Infrastructure Stack
Based on type and score, assign the standard infrastructure stack:
    - Compute: NVL72 racks (CDU) for Type A | EC-110 immersion pods for Type B | Both for Type C
    - Power: LUS/CLECO grid primary + Bloom Energy fuel cell + nat gas generator + diesel N+1
    - Energy supplement: New Iberia Solar PPA where feasible (south Acadiana sites)
    - Network: LUS Fiber primary + diverse second carrier + MARLIE I NOC backhaul
    - EV: DC fast charge + Level 2 at every site, utility aesthetic
    - Drone: KLFT relay node at every site — Skydio Dock if primary hub, relay antenna if secondary
---
## Scoring Thresholds
    - Score 28-35: PRIORITY 1 — move immediately, LOI within 30 days
    - Score 21-27: PRIORITY 2 — active engagement, 90-day target
    - Score 14-20: PRIORITY 3 — monitor, re-evaluate when capital available
    - Score below 14: HOLD — document but do not pursue until fundamentals improve
---
## Scoring System v2 — 10 Base + 6 Bonus Variables (2026-03-25)
> v2 replaces the original 7-variable system. 10 base variables (100 pts max) + 6 bonus variables (24 pts max) = 124 total possible. Scoring engine: agents/site_scout/scorer_v2.py
---
### Base Variables (10 x 10 pts = 100 pts max)
    1. Power Access (0-10): Grid capacity, voltage, distance to substation
    1. Natural Gas (0-10): Pipeline proximity, Henry Hub pricing zone, ATMOS service
    1. Fiber/Network (0-10): LUS Fiber, LONI backbone, dark fiber availability
    1. Water/Cooling (0-10): Water source for cooling, discharge permits, adiabatic viability
    1. Flood Risk (0-10): FEMA zone, elevation, historical flooding
    1. Zoning/Permits (0-10): Current zoning, variance difficulty, environmental review
    1. Building/Land (0-10): Existing structure quality, sq footage, clear span, ceiling height
    1. Road/Logistics (0-10): Interstate access, truck routes, equipment delivery path
    1. Workforce (0-10): Proximity to labor pool, university pipeline, training programs
    1. Acquisition Cost (0-10): Price per sq ft, seller motivation, deal complexity
---
### Bonus Variables (6 x 4 pts = 24 pts max)
    1. University Partnership (0-4): Anchor tenant, research collaboration, grant eligibility
    1. Solar Potential (0-4): Rooftop area, orientation, First Solar proximity
    1. Historical/Tax Credits (0-4): Historic designation, Brownfield, Opportunity Zone
    1. Community Impact (0-4): Job creation narrative, revitalization story, political support
    1. Multi-Site Synergy (0-4): Proximity to other ADC sites, shared infrastructure
    1. Strategic Value (0-4): Unique capabilities (river access, airport, rail)
---
### Tier Classification
    - Tier S (100+): Exceptional — move immediately, flagship site
    - Tier A (85-99): Excellent — priority development, strong fundamentals
    - Tier B (70-84): Good — viable with targeted investment
    - Tier C (55-69): Marginal — significant gaps, monitor only
    - Tier D (<55): Not viable — pass
---
### Current Site Scores (v2)
> Trappeys Cannery: 84 base + 21 bonus = 105 (Tier S)
Willow Glen Terminal: 94 base + 11 bonus = 105 (Tier S)
MARLIE I Command Center: 89 base + 8 bonus = 97 (Tier A/S)
KLFT 1.1 Drone Hub: 74 base + 11 bonus = 85 (Tier B/A)
---
### Trappeys Cannery — 105 (Tier S)
    - Base: 84/100 — Strong power (ATMOS gas, LUS grid), LUS Fiber lit, 112,500 sq ft across 4 buildings, I-10 access, UL Lafayette 2 miles
    - Bonus: 21/24 — UL Lafayette partnership (+4), 2.05 MW solar rooftop (+4), Historic tax credits 45-55% (+4), Riverwalk/revitalization narrative (+4), Half mile from MARLIE I (+4), Near KLFT (+1)
    - Key advantage: Highest bonus score of any site. University + solar + historic credits stack.
---
### Willow Glen Terminal — 105 (Tier S)
    - Base: 94/100 — Former 2,200 MW Entergy station, existing heavy industrial infrastructure, river cooling (Mississippi), massive land parcel, transmission-grade power
    - Bonus: 11/24 — LSU partnership potential (+4), River access strategic value (+4), Multi-site synergy with Baton Rouge (+3)
    - Key advantage: Highest base score. Raw infrastructure is unmatched. 100+ MW scale potential.
---
### MARLIE I Command Center — 97 (Tier A/S)
    - Base: 89/100 — Scott's existing location, LUS Fiber lit, ATMOS gas on property, I-49 access, Lafayette workforce
    - Bonus: 8/24 — Multi-site synergy with Trappeys (+4), Strategic NOC/war room value (+4)
    - Key advantage: Operational NOW. Backup NOC, R&D staging, Scott's war room. Zero acquisition cost.
---
### KLFT 1.1 — 85 (Tier B/A)
    - Base: 74/100 — Airport infrastructure, FAA Part 108 BVLOS pending, limited compute space, specialized zoning
    - Bonus: 11/24 — Strategic drone hub value (+4), NVIDIA Smart City convergence (+4), Proximity to Trappeys <1 mi (+3)
    - Key advantage: Autonomous airspace ops. Not a compute site — it's a drone/AI-RAN command node.
---
Scoring engine source: agents/site_scout/scorer_v2.py — run programmatically against any new site prospect.
> ARCHIVED 2026-03-23: Airport frontage and hotel sites are dead. Trappeys (Lafayette) and Willow Glen (St. Gabriel) are locked. Site Evaluation Framework still useful for future sites.
*[Child: Vendor & Partner Strategy]*
> Strategic outreach framework for MARLIE I, ADC 3K pod network, KLFT, and the Louisiana AI ecosystem. Goal: lock in Tier 1 supply agreements before investor close, build Tier 3 partnerships for federal positioning, plant seeds with Tier 4 for long-term network effect.
---
## Why Vendors Want This Deal
Most AI infrastructure projects are asking vendors to take a risk on a speculative build. MARLIE I is different. Every vendor here gets a long-term, high-volume industrial customer with federal backing, state tax incentives, and a GC who controls the timeline. The pitch is not 'support our project.' The pitch is 'be the anchor supplier for Louisiana's AI network.'
  - NVIDIA: first Rubin-class factory in Louisiana = reference site, partner credibility, Southern US beachhead
  - Atmos Energy: baseload industrial gas contract — flat, forecastable, long-term, no seasonal spike
  - LUS Fiber: largest single-site industrial fiber customer, BEAD expansion justification, federal co-marketing
  - Ring Power / Cat: full generator fleet contract — nat gas + diesel — one relationship, recurring maintenance revenue
  - Tesla: I-10/I-49 Supercharger gap filled, Southern US coverage, EV charging revenue at zero land cost
  - NVIDIA Omniverse: Louisiana industrial base (oil/gas/ports/robotics) is a tier-1 digital twin market
---
## The Structural Advantage No Northern Competitor Has
Legacy data centers in the Northeast and California are trapped: air-cooled infrastructure, $0.12-0.19/kWh grid power, aging facilities, local opposition, and Blackwell-era hardware. They will keep patching because that is their sunk cost. ADC starts with the right architecture, the right location, and the right hardware — from day one.
  - Power: $0.065/kWh Louisiana industrial vs. $0.19/kWh California = $1.2M+/year savings per 16-rack build
  - Gas: Henry Hub 40 miles away — most liquid nat gas benchmark on earth — price certainty they cannot match
  - Cooling: liquid-cooled NVL72 at PUE 1.10 vs. legacy air-cooled at PUE 1.4-1.8 — 40-80% wasted power eliminated
  - Space: no grid capacity constraints, no NIMBY opposition, industrial zoning, owned land
  - Regulatory: FEOC-clean, OBBBA-compliant, Act 730 qualified — federal money flows here, not to them
  - Location: I-10 / I-49 corridor = center of Southern US compute network, not an afterthought
---
## The Autonomous Vehicle + Robotics Wave
95% of the public does not understand what is coming. Every robotaxi, every Optimus robot, every autonomous port crane, every AI-managed refinery requires continuous edge inference. That compute has to live somewhere. It will not live in a cold-climate legacy data center 1,500 miles away. It will live at the closest high-density compute node with cheap power and a fiber backbone. ADC is building that node — in the South, first.
  - Robotaxi: Southern US expansion (Tesla FSD, Waymo) needs Gulf Coast compute infrastructure — Lafayette is the hub
  - Optimus / factory robots: Omniverse digital twin simulation = NVL72 workload, runs on MARLIE I
  - Port AI: Port of New Orleans, Port of Morgan City, Port of Lake Charles — autonomous logistics = ADC 3K pod customers
  - Refinery AI: Exxon, Chevron, Valero Gulf Coast operations — predictive maintenance AI = captive pod customers
  - Air traffic: KLFT + Lafayette Regional Airport AI = first step toward autonomous airspace management
*[Child: Tier 1 — Must-Have Supply Agreements (Get These First)]*
> Cannot close investors or break ground without these. Each is a bilateral win — ADC gets supply certainty, vendor gets anchor industrial customer.
---
## NVIDIA — Hardware Allocation + Partner Program
The most critical relationship in the stack. Without a confirmed NVL72 allocation, the financial model is entirely speculative. NVIDIA wants reference sites in new markets — Lafayette is the first Rubin-class factory in Louisiana. That is a reference site NVIDIA values.
    - Ask 1: Hardware allocation letter — confirmed NVL72 rack allocation for Phase 1 (4-8 racks, H2 2026)
    - Ask 2: NVIDIA Partner Network enrollment — preferred pricing, technical support, co-marketing eligibility
    - Ask 3: NVIDIA Capital / financing program introduction — GPU hardware financing path
    - Ask 4: DGX-Ready or AI Factory designation — validation that MARLIE I meets NVIDIA's reference architecture
    - Ask 5: NVIDIA Omniverse Enterprise license discussion — digital twin platform for Louisiana industrial market
    - Pitch angle: 'First Rubin-class factory in Louisiana. Federal compliance. 7 NVIDIA certs. GC on site. Ready H2 2026.'
    - Contact path: NVIDIA Enterprise Sales -> NVIDIA Partner Network portal -> GTC 2026 meeting
---
## Atmos Energy — Industrial Gas Supply Agreement
    - Ask: Long-term industrial supply agreement with rate stabilization — 10-year minimum
    - Ask: Priority service classification for on-site prime generation (Cat G3520H baseload)
    - Volume: 2x Cat G3520H at 2.5 MW each = continuous high-volume industrial load, flat and forecastable
    - Pitch: 'Baseload industrial customer 3 miles from your distribution line. No seasonal spike. 10-year contract.'
    - Contact: Atmos Energy industrial sales — 1818 Eraste Landry Rd, Lafayette
---
## LUS — Grid Interconnect + LUS Fiber Service
    - Ask 1 (LUS Power): 3-phase industrial interconnect agreement + industrial rate classification
    - Ask 2 (LUS Fiber): Redundant fiber service agreement — direct dark fiber from 214 Jefferson St to 1201 SE Evangeline
    - Ask 3: Letter of support for federal BEAD and OBBBA applications (co-marketing value to both parties)
    - Pitch: 'Lafayette-built, Lafayette-powered, Lafayette-connected. LUS is the backbone. MARLIE I is the anchor tenant.'
    - Contact: Lafayette Consolidated Government -> LUS Director -> LUS Fiber Director
---
## Ring Power / Caterpillar — Generator Fleet Contract
    - Ask: Single service contract covering all Cat equipment — G3520H nat gas generators + C175-16 diesel backup
    - Ask: Priority storm-response SLA — 4-hour response window during Gulf storm events
    - Ask: Fuel logistics coordination — diesel delivery contract tied to storm prep protocol
    - Volume: 2x G3520H (5 MW nat gas) + 2x C175-16 (6.7 MW diesel) — largest Cat gen fleet in the Lafayette corridor
    - Pitch: 'One dealer, one contract, one call. You service the whole power stack. We give you a 20-year industrial anchor.'
---
## Bloom Energy — Fuel Cell Supply + Service
    - Ask: 300 kW Phase 1 fuel cell supply agreement — scalable in 300 kW increments for Phase 2+
    - Ask: Long-term service contract — Bloom handles maintenance, ADC gets uptime SLA
    - Pitch: 'Gulf Coast industrial customer. Natural gas primary. Bloom is Layer 2 in a 5-layer stack. Continuous load, no cycling.'
    - Contact: Bloom Energy commercial sales (Newark, DE) — reference OBBBA domestic content compliance
---
## Vertiv / CoolIT — CDU Procurement
    - Ask: CDU supply agreement for Phase 1 (NVL72-compatible, sized to design basis TDP)
    - Ask: Extended service contract + 24/7 remote monitoring integration with Mission Control
    - Note: Size to conservative 150 kW/rack until NVIDIA publishes official NVL72 TDP
    - Contact: Vertiv (Columbus OH) or CoolIT Systems (Calgary) — both NVIDIA-validated CDU suppliers
---
> POST-GTC 2026 UPDATE (2026-03-23) -- Major changes to Tier 1 vendor stack. Bloom Energy REMOVED. Ring Power replaced by Louisiana Cat. Eaton elevated. New suppliers added. NVIDIA contacts identified.
---
## Louisiana Cat Power Systems -- Generator Fleet (REPLACES Ring Power)
Louisiana Cat Power Systems, New Iberia, LA. Main: 337-374-1901. 21 locations across Louisiana, services offshore rigs. THE Cat dealer for ADC.
    - Contact: Spencer Landry -- 985-498-9336
    - Contact: Ken Johnson -- 504-544-2074
    - Product (Trappeys/MARLIE I): Cat G3520C -- 1.5 MW natural gas genset. Proven industrial prime power. Perfect for Layer 2 backbone.
    - Product (Willow Glen): Cat CG260-16 -- 2.8 MW natural gas genset. H2-ready (25% hydrogen blend TODAY). Future-proofed for Hidrogenii hydrogen supply.
    - Cat Financial available for equipment financing -- lease or loan through Louisiana Cat.
    - Storm-response SLA: 4-hour response window. Louisiana Cat services offshore rigs, they understand 24/7 ops.
    - Pitch angle: One dealer, one contract. Largest Cat gen fleet in the Lafayette-to-Baton-Rouge corridor. 20-year industrial anchor.
---
## Eaton (Beam Rubin DSX) -- Complete 800V DC Platform (NEW Tier 1)
Contact made at GTC 2026. Eaton Beam Rubin DSX is co-designed with NVIDIA. THE reference standard for AI factory power distribution.
    - TX + LA manufacturing. Fibrebond acquisition gives Louisiana presence.
    - Product stack: 800V DC rectifier + busway + rack PDUs + supercapacitors + microgrid controller + xStorage BESS
    - Single vendor for entire power distribution path from genset output to GPU input.
    - Eaton Capital -- equipment financing available for power infrastructure.
    - Application engineering: Eaton provides design assist for DSX integration. Still need Louisiana PE to stamp drawings.
    - Pitch angle: NVIDIA co-designed. DSX reference standard. One vendor for the entire 800V DC path.
---
## Diamond Green Diesel -- Renewable Diesel Supply (NEW Tier 1)
Norco, LA -- 60 river miles from Willow Glen. Joint venture (Valero + Darling Ingredients).
    - 1.2 billion gallons/year renewable diesel production
    - Willow Glen already ships them feedstock -- existing relationship
    - Barge delivery to Willow Glen 43-ft dock -- no trucking needed
    - Layer 3 emergency diesel gensets run on renewable diesel -- carbon neutral backup power
    - Pitch angle: Existing logistics relationship. Barge delivery to our dock. Renewable diesel = carbon-neutral emergency power.
---
## Hidrogenii (Plug Power + Olin) -- Hydrogen Supply (NEW Tier 1)
St. Gabriel, LA -- LITERALLY next door to Willow Glen.
    - 15 TPD hydrogen production, commissioned April 2025
    - Cat CG260-16 supports 25% H2 blend TODAY -- no modifications needed
    - Future path: 100% hydrogen gensets as technology matures
    - Pipeline delivery possible -- proximity eliminates trucking
    - Pitch angle: Hydrogen supplier next door. 25% blend reduces natural gas consumption immediately. Full hydrogen path for the future.
---
## NVIDIA -- Updated Contact Intelligence (Post-GTC 2026)
> InMails sent 2026-03-23 to Rendek and Traill. Awaiting responses. These are the two highest-priority contacts for NPN enrollment and AI Factory designation.
    - John Rendek -- Head of AI Factories for NPN. DIRECT path to hardware allocation + NPN enrollment. InMail SENT.
    - Doug Traill -- Snr Director Solutions Architecture, AI Factory. Technical validation for DGX-Ready. InMail SENT.
    - Craig Weinstein -- VP Americas Partner Organization. Partner program structure + pricing.
    - Garren Givens -- VP Ecosystem Enablement. Ecosystem programs, co-marketing.
    - Marc Hamilton -- VP Solutions Architecture. Technical reference architecture review.
    - Jim Hennessy -- Senior Partner Business Manager. Day-to-day partner operations.
Certification ladder: NPN (register now) > DGX-Ready (Willow Glen) > NCP > Reference Platform NCP. ADC goes through Partner Network, NOT Inception (Inception is for software startups).
---
## REMOVED / DEPRIORITIZED
> Bloom Energy -- REMOVED from vendor stack. Fuel cells no longer in power hierarchy. 4-layer model: Solar > Natural Gas > Diesel Gensets > Grid (sell-back only).
> Vertiv / CoolIT CDU -- DEPRIORITIZED. NVIDIA ships complete liquid-cooled racks (NVL72). CDU is part of NVIDIA rack delivery, not a separate procurement item. May still need for custom edge deployments.
> Ring Power -- REPLACED by Louisiana Cat Power Systems. Louisiana Cat has 21 locations statewide, closer proximity, offshore rig experience, same Cat product line.
---
## CERAWeek 2026 Update — Validated Tier 1 Vendors (2026-03-25)
> Updated after CERAWeek 2026. All vendors below are validated, pricing confirmed, contacts made. 800V DC architecture consensus across the industry.
---
### NVIDIA — NVL72 + Vera Rubin + DSX Reference Design
    - NVL72 liquid-cooled racks — standard delivery, 45C hot water, 2-hour rack install
    - Vera Rubin GPU — H2 2026 availability confirmed at GTC 2026
    - Quantum-X800 InfiniBand switches — 800 Gb/s, spine for SuperPOD
    - BlueField-4 DPU — network offload, security, zero-trust at NIC level
    - ConnectX-8 SuperNIC — 800 Gb/s per port, NVL72 standard
    - DSX Reference Design — NVIDIA's complete AI factory blueprint. ADC builds to spec.
    - Dynamo 1.0 — open-source inference OS, 7x perf on Blackwell
    - Status: NPN registration in progress (Jim Hennessy facilitating)
---
### Eaton — 800V DC Power Distribution (Full Stack)
    - Beam Rubin DSX — 800V DC power platform, purpose-built for NVIDIA DSX
    - ORV3 Sidecar — rack-level power distribution for NVL72
    - Boyd Thermal CDUs — liquid cooling distribution integrated with Eaton power
    - Fibrebond enclosures — manufactured in Minden, Louisiana (US-made)
    - HDX G4 PDU — high-density power distribution
    - PowerWave2 busway — 800V DC bus distribution
    - Contact: JP Buzzell (met at CERAWeek 2026)
    - Status: Active engagement, spec sheets received
---
### Caterpillar — G3516J Natural Gas Generator (Standardized)
    - G3516J: 1.6 MW continuous rating, natural gas prime
    - Standardized across all ADC sites — single model simplifies parts/training
    - Louisiana Cat dealer: 337-837-2476 (local support, storm-response SLA)
    - Nscale ($14.6B competitor) using same Cat equipment — validates choice
    - Henry Hub pricing advantage: $0.027-$0.035/kWh on-site generation
    - Status: Dealer relationship established, quoting in progress
---
### First Solar — Series 7 TR1 (Layer 1 Solar)
    - Series 7 TR1: 550W per panel, 19.7% efficiency, CdTe thin-film
    - New Iberia factory: $1.1B investment, 3.5 GW/year, 826+ employees
    - 30 miles from Trappeys — shortest supply chain in the industry
    - 3,731 panels = 2.05 MW at Trappeys rooftops
    - 5-panel strings at 952V, buck to 800V DC bus — DC-direct architecture
    - ZERO Chinese supply chain — American glass, steel, fabrication
    - Contact: modulesales@firstsolar.com
    - Status: Spec locked, site survey pending
---
### ABB — SACE Infinitus Solid-State DC Breaker
    - SACE Infinitus: first IEC-certified solid-state breaker for 800V DC
    - Critical for 800V DC bus protection — no mechanical parts, microsecond trip
    - Eliminates arc flash risk on DC distribution
    - CERAWeek 2026: ABB confirmed production availability
    - Status: Spec sheet received, integration design pending
---
### CoolIT Systems — CHx2000 CDU
    - CHx2000: 2,000 kW cooling capacity per CDU
    - Six 9s reliability (99.9999% uptime)
    - Direct liquid cooling for NVL72 racks
    - Status: Spec sheets in hand, sizing for Trappeys Phase 1
---
### BAC — TrilliumSeries Adiabatic Cooler
    - TrilliumSeries: adiabatic cooling (NOT dry cooler — critical for Louisiana 95F+ summers)
    - Water-assisted evaporative cooling reduces approach temperature vs dry-only
    - Sized for heat rejection from CDU loop
    - Status: Application engineering contact needed
*[Child: Tier 3 — Government & Institutional Partners]*
> Government partners do not write checks — they open doors. A letter of support from the City of Lafayette is worth more than a financial projection in a federal funding application. Get these relationships in writing before investor meetings.
---
## Louisiana Economic Development (LED)
    - Ask 1: Act 730 pre-qualification letter — confirms project meets $200M+ / 50+ jobs threshold
    - Ask 2: Quality Jobs Program enrollment — 6% payroll rebate for 10 years on qualifying jobs
    - Ask 3: LED FastStart workforce training — free customized training for MARLIE I technical staff
    - Ask 4: Co-marketing support — LED promotes MARLIE I as Louisiana's flagship AI infrastructure project
    - Pitch: 'First Rubin-class AI factory in Louisiana. 50+ jobs at $65-90K. 20-year tax base. Act 730 ready.'
    - Action: Schedule LED pre-application meeting. Bring the investor deck. Ask for the pre-qual letter in writing.
---
## City of Lafayette / Lafayette Consolidated Government
    - Ask: Letter of support for federal OBBBA / CHIPS / EDA applications — city co-signature
    - Ask: EDA Tech Hub designation nomination — Lafayette as Gulf Coast AI infrastructure hub
    - Ask: Economic development agreement — fast-track permitting, city co-marketing
    - Pitch: 'Lafayette builds this, Lafayette owns this. 50+ jobs. $45M+ 5-year economic impact. First in the South.'
    - Action: Meet with Mayor-President's office. Bring LED Act 730 pre-qual letter. Ask for the support letter.
---
## UL Lafayette + LSU — Talent Pipeline + R&D
    - Ask: Workforce partnership MOU — computer science, electrical engineering, data center operations pipeline
    - Ask: Research partnership — GPU computing research, energy efficiency, Louisiana industrial AI applications
    - Ask: Industry advisory board seat — ADC/MARLIE I as industry partner for AI curriculum development
    - Value to universities: students get internships and placements at Louisiana's only Rubin-class facility
---
## US Department of Energy (DOE)
    - Program: Grid Modernization Initiative — on-site nat gas generation + solar PPA + Bloom = grid resilience model
    - Program: Industrial Decarbonization — Bloom Energy fuel cells + future hydrogen blend path
    - Program: Data Center Energy Efficiency — PUE 1.10 liquid cooling at scale is a DOE showcase candidate
    - Action: Identify DOE Office of Electricity program manager for Gulf South region. Letter of inquiry.
---
## EDA Tech Hub Designation — Lafayette as Gulf Coast AI Hub
The Economic Development Administration's Tech Hub program designates regions as national technology hubs and unlocks federal matching dollars — not just for MARLIE I, but for the entire Lafayette tech ecosystem.
    - Consortium required: MARLIE I + UL Lafayette + City of Lafayette + Louisiana Economic Development + LUS
    - Application angle: Gulf Coast AI + Energy Infrastructure Hub — unique intersection of AI compute and energy sector
    - Federal match: EDA awards $50-75M to designated hubs — transforms the entire regional funding landscape
    - Action: Contact EDA regional rep. Assemble consortium. File Phase 1 application (no cost, low commitment).
---
> POST-GTC 2026 UPDATE (2026-03-23) -- Key institutional contacts identified. University partnerships now span 3 campuses. Iberville Parish IDB added for Willow Glen.
## Updated Institutional Partners
    - LEDA (Lafayette Economic Development Authority) -- warm intro path to UL Lafayette, City Council, LED. Use for Trappeys + MARLIE I.
    - LED (Louisiana Economic Development) -- Act 730 pre-qualification + ITEP (NAICS code risk, must pre-qualify as "emerging industry"). Contact: Kristin Johnson, 225-342-2083. -16M ITEP savings. Act 730 = 00M+ / 50 jobs threshold.
    - Iberville Parish IDB -- Industrial Development Board for Willow Glen site. M2 zoning, brownfield advantage. 5-6 months optimistic for permits.
## University Partners -- 3 Campus Strategy
    - UL Lafayette -- Dr. Ramesh Kolluru, new Interim President (CS PhD, R1 builder). NO GPU infrastructure on campus. LEDA for warm intro. Anchor tenant for Trappeys. 10+ grant programs, 8-55M+ potential (NSF MRI M, EPSCoR 0M, LED FastStart free, Historic Tax Credits 45-55%).
    - LSU -- Vicki Colvin, Dean of Engineering. Tiger AI Factory concept (Willow Glen). SEC flagship, governor's city. Former 2,200 MW station, 100+ MW scale, Mississippi River cooling. Parallel to Trappeys/UL Lafayette.
    - Southern University -- 8M CSTEM building. HBCU pipeline. Baton Rouge proximity to Willow Glen. Federal HBCU funding advantages.
## NVIDIA 50-State Plan Alignment
GTC 2026 "50-State Plan" panel (Chris Malachowsky). UF = THE blueprint (80M, HiPerGator, K-12 pipeline, all 12 FL universities). ADC + UL Lafayette = Louisiana's version. Two white papers by Brittany Wise. Pitches needed for Dr. Kolluru, NVIDIA, and City Council.
    - NPN registration = 5-minute web form. DO TODAY.
    - Certification ladder: NPN > DGX-Ready > NCP > Reference Platform NCP.
*[Child: Outreach Sequence & Talking Points]*
> Execute in this order. Each completed agreement strengthens the next conversation. Do not pitch investors until Tier 1 supply agreements are in progress.
---
## 30-Day Sprint — Tier 1
    - Week 1: Schedule LED pre-application meeting. Schedule LUS Director meeting. Contact Atmos industrial sales.
    - Week 2: Submit Tesla Supercharger host application (tesla.com/charging/partners) for MARLIE I site
    - Week 3: NVIDIA Partner Network enrollment. Request Enterprise Sales intro. Target GTC 2026 meeting.
    - Week 4: Ring Power generator fleet contract discussion. Bloom Energy commercial sales call.
---
## 60-Day Sprint — Investor Readiness
    - Atmos industrial supply agreement — term sheet or LOI
    - LUS interconnect agreement — formal application submitted
    - LUS Fiber service agreement — direct fiber path confirmed
    - Act 730 pre-qualification letter from LED in hand
    - City of Lafayette letter of support signed
    - NVIDIA partner program enrollment confirmed, hardware allocation conversation started
    - Tesla Supercharger host application status — response typically 4-6 weeks
---
## Universal Talking Points — Use With Every Vendor
These three points land with every audience regardless of industry:
    - 1. FEDERAL BACKING: 'OBBBA-compliant, Act 730 qualified, FEOC-clean. The federal money is designed for exactly this project.'
    - 2. COST STRUCTURE: 'Louisiana industrial power at $0.065/kWh. Henry Hub gas 40 miles away. Every competitor pays 2-3x more for the same compute.'
    - 3. FIRST MOVER: 'Louisiana has no Rubin-class AI factory. We are building it. You can be the anchor partner, or you can watch someone else fill that role.'
---
## The Elon Pitch — If the Opportunity Arises
If there is ever a direct channel to Tesla/xAI/Boring, the three-sentence pitch is:
> 'You need cheap, reliable compute in the South. We have the cheapest industrial power in the country, natural gas prime power that doesn't depend on a grid, and we're building the first Vera Rubin AI factory in Louisiana. Put Superchargers on our sites, put your Southern inference workload in our racks, and we both build the infrastructure the South doesn't have yet.'
---
## The Market Timing Argument — For Every Meeting
The data centers being built right now in the Northeast and California are building on the wrong foundation. Air cooling, expensive grid power, legacy architecture. They will keep adding capacity to a broken system because that is their sunk cost. Every year they operate, their cost disadvantage compounds. We are not patching anything. We start with liquid cooling, nat gas prime power, and Rubin-class hardware. The vendors who want to be on the right side of that transition need to be in Louisiana now, not in 5 years.
    - Power-hungry legacy DC (national avg): $0.122/kWh → $2.57M/year at 2.4 MW load
    - MARLIE I (Louisiana industrial): $0.065/kWh → $1.37M/year same load
    - Savings: $1.2M/year before the first customer pays a dollar
    - Cooling efficiency: PUE 1.10 (MARLIE I) vs PUE 1.4-1.8 (legacy air) = 22-40% wasted power eliminated
    - Hardware timing: Vera Rubin NVL72 = 2.5x FP4 density vs legacy Blackwell — same floor space, 2.5x revenue
---
> POST-GTC 2026 UPDATE (2026-03-23) -- Outreach priorities reshuffled. NVIDIA InMails sent. Bloom removed. Louisiana Cat and Eaton are top priorities.
## Updated 30-Day Sprint (Starting 2026-03-23)
    - DONE: NVIDIA InMails sent to John Rendek (Head of AI Factories for NPN) and Doug Traill (Snr Director Solutions Architecture). Awaiting responses.
    - Week 1: Follow up on NVIDIA InMails. Call Louisiana Cat -- Spencer Landry (985-498-9336) for G3520C quote (Trappeys/MARLIE I). Call Ken Johnson (504-544-2074) for CG260-16 quote (Willow Glen).
    - Week 1: NPN registration -- 5-minute web form. No cost. Do immediately.
    - Week 2: Eaton Beam Rubin DSX engagement -- follow up on GTC 2026 contact. Request application engineering support for 800V DC design.
    - Week 2: ATMOS Energy -- trunk line confirmed at Trappeys. Formalize industrial supply agreement.
    - Week 3: First Solar -- modulesales@firstsolar.com or 419-662-6899. Get Series 7 TR1 pricing for Trappeys (3,731 panels, 2.05 MW) and Willow Glen (ground mount, 400+ acres).
    - Week 4: Diamond Green Diesel + Hidrogenii outreach for Willow Glen fuel supply agreements.
## REMOVED from Sprint
    - Bloom Energy -- removed from power hierarchy entirely. No longer a vendor target.
    - Tesla Supercharger -- deprioritized. Not core to AI factory mission.
    - Ring Power -- replaced by Louisiana Cat Power Systems statewide.
## Updated Talking Points
    - NEW: "ADC is a neocloud -- GPU-first cloud provider. We sell tokens, not GPU hours. Energy-first model with 95%+ margins."
    - NEW: "NVIDIA ships complete liquid-cooled racks. We build to DSX reference spec. Eaton 800V DC from solar to GPU."
    - NEW: "3 sites online: Trappeys (solar AI factory, proof of concept), MARLIE I (command center + edge), Willow Glen (100+ MW primary hub). All connected."
    - UPDATED cost: "/usr/bin/bash.058-0.068/kWh Phase 1 (recip engines). At scale /usr/bin/bash.04-0.05/kWh (CCGT). Louisiana industrial vs /usr/bin/bash.19/kWh California."
*[Child: First Solar — Partner Workbook]*
> Drop spec sheets, proposals, meeting notes, and technical docs here. This is the living workbook for ADC's #1 solar partner.
## Company Overview
| Company | First Solar, Inc. |
| HQ | Tempe, Arizona |
| LA Factory | 1400 Corporate Drive, New Iberia, LA ($1.1B) |
| Product | Series 7 thin-film CdTe — 525-550W panels |
| Output | 3.5 GW/year |
| Contact | Info@FirstSolar.com | 419-662-6899 |
| Website | firstsolar.com |
## Why First Solar for ADC
    - 30 miles from Trappeys — panels manufactured next door
    - $1.1B invested in Louisiana — deep commitment, not a fly-by
    - ZERO Chinese supply chain — American glass, steel, fabrication
    - Deep investor network — billion-dollar backers who want solar deployed
    - Mutual interest: they need panels on rooftops, we need Layer 1 power
    - Government funding aligned on both sides (30% ITC + state incentives)
## ADC Solar Deployment Roadmap
| Phase | Site | Capacity | Panels |
| 1 | Trappeys Cannery (rooftop) | ~1 MW | 1,830 |
| 2 | Willow Glen (ground-mount) | 30+ MW | TBD |
| 3+ | Every ADC site | Scales | TBD |
---
## Spec Sheets & Technical Docs
Upload Series 7 datasheets, installation guides, warranty docs, and technical specifications here.
---
## Proposals & Quotes
Site survey results, pricing quotes, project proposals, and installation estimates.
---
## Meeting Notes & Correspondence
Call notes, email threads, agreements, and partnership updates.
---
## Action Items
    - [ ] Contact First Solar: Info@FirstSolar.com or 419-662-6899
    - [ ] Request site survey for Trappeys Cannery rooftops
    - [ ] Get Series 7 pricing for 2+ MW commercial installation
    - [ ] Discuss branding/sponsorship (water tower, website)
    - [ ] Explore investor introductions — mutual interest in solar-powered AI
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/5a788f09-7e31-81eb-a3dc-00039a1662d6/f213bebd-bc63-437f-9d7c-657fed0168ec/Screenshot_2026-03-21_at_16-23-51_FirstSolar_Series7-TR1_BR.pdf.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466W4WNCMCB%2F20260406%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260406T214418Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEA0aCXVzLXdlc3QtMiJHMEUCICYBhZ1VbvBK4p9VxC4t9skrlfJZLJXbHZ7Ym1xN6holAiEA2ajbrB7v9bTm%2FkfFAqxpax54tHug9mLmoy%2Bj%2FthBHCkqiAQI1v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDFQX%2BFTTemryhSM%2BAircA3WL2VvnWcLoAO8%2Fm4BqATPlXMBk2b683p0%2FVe0zoTrgtVHxvPOWR0d97KOwCeWFKakSQl6fyr4rSJ0NQ7fFdR5U%2FBKTijp7p5nSuNKkv7rrQ9ay%2FPwulNONGxNQJoYibBZD0IjJgFd%2FATjdvw6cwbejwUaHPKo9eVl0xDbJi39hgSPzJW8WRF2wP5%2FI71dNg3y51FK7er%2FAtDPNG%2FYzssE52CWhB6A0bVozZ4LgoKgGzCG267J%2FIofzsqvV6vqieQ05lsqBOuYGq3UzGtWWFS2VZy4yeVgv0MfqxFXfM%2FljwJ6fyL9xBdTj1zjR%2FUHTDERVGsORBiqtbdq5uG7eqyAZ75Jdn%2Biq9x%2Fzia8h3dHxXgj8ozIpznOXormfFidNtqWwa6t%2B484g1WiDKNRk3diCKTHzxKSslRnWzNu9RLr4Xwrpbe5g27i1%2FLtpX2b89NJTT6uBfi7C6jwOgIakBX%2B2E8dNfU%2BBiKsEzZP5ZvAlO15ptW2%2BcTgdJ%2F9j8BVpyt2z4PF%2BNNcy4wM9JydhRgXdJEdO3n6kREk9GoEEhjvSOETiiysk%2BSh4tt5lIgQq9joMgXrHKYU5q4A7fnOInIJkzVaNxpPXjsuHQ4cqcyY2xEJAnUbwp3wSQRoCMLvE0M4GOqUBO4wgdSjmAK84JJFrFhHXiMmKujVHiYhIZejuRonRlGYrZSPHYbiTXgezJA%2Fg1wGD5E5l9av6vmNR6wfu%2FV4ZBuwfwxrHMAoH%2F37qdjSEkkZpDhcCPAfaaYmF58foaALTlC7iSOvCXH57VyFksXMnkjNJpqHgxsd8udUfDbpPBtsJsuKscUs4wO1fLoO5vBaLJnbCiFfEg3ctYRivHpaECoIXqkbG&X-Amz-Signature=f9d2a56bf95945fa8811a86c8ee9836566ec33f33746005e01dcb467d5fb6370&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/5a788f09-7e31-81eb-a3dc-00039a1662d6/a8cfac1d-a574-4600-ac5e-631eb886c640/Screenshot_2026-03-21_at_16-23-29_FirstSolar_Series7-TR1_BR.pdf.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466W4WNCMCB%2F20260406%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260406T214418Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEA0aCXVzLXdlc3QtMiJHMEUCICYBhZ1VbvBK4p9VxC4t9skrlfJZLJXbHZ7Ym1xN6holAiEA2ajbrB7v9bTm%2FkfFAqxpax54tHug9mLmoy%2Bj%2FthBHCkqiAQI1v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDFQX%2BFTTemryhSM%2BAircA3WL2VvnWcLoAO8%2Fm4BqATPlXMBk2b683p0%2FVe0zoTrgtVHxvPOWR0d97KOwCeWFKakSQl6fyr4rSJ0NQ7fFdR5U%2FBKTijp7p5nSuNKkv7rrQ9ay%2FPwulNONGxNQJoYibBZD0IjJgFd%2FATjdvw6cwbejwUaHPKo9eVl0xDbJi39hgSPzJW8WRF2wP5%2FI71dNg3y51FK7er%2FAtDPNG%2FYzssE52CWhB6A0bVozZ4LgoKgGzCG267J%2FIofzsqvV6vqieQ05lsqBOuYGq3UzGtWWFS2VZy4yeVgv0MfqxFXfM%2FljwJ6fyL9xBdTj1zjR%2FUHTDERVGsORBiqtbdq5uG7eqyAZ75Jdn%2Biq9x%2Fzia8h3dHxXgj8ozIpznOXormfFidNtqWwa6t%2B484g1WiDKNRk3diCKTHzxKSslRnWzNu9RLr4Xwrpbe5g27i1%2FLtpX2b89NJTT6uBfi7C6jwOgIakBX%2B2E8dNfU%2BBiKsEzZP5ZvAlO15ptW2%2BcTgdJ%2F9j8BVpyt2z4PF%2BNNcy4wM9JydhRgXdJEdO3n6kREk9GoEEhjvSOETiiysk%2BSh4tt5lIgQq9joMgXrHKYU5q4A7fnOInIJkzVaNxpPXjsuHQ4cqcyY2xEJAnUbwp3wSQRoCMLvE0M4GOqUBO4wgdSjmAK84JJFrFhHXiMmKujVHiYhIZejuRonRlGYrZSPHYbiTXgezJA%2Fg1wGD5E5l9av6vmNR6wfu%2FV4ZBuwfwxrHMAoH%2F37qdjSEkkZpDhcCPAfaaYmF58foaALTlC7iSOvCXH57VyFksXMnkjNJpqHgxsd8udUfDbpPBtsJsuKscUs4wO1fLoO5vBaLJnbCiFfEg3ctYRivHpaECoIXqkbG&X-Amz-Signature=442bfc99995ecbb00204cb837799e65042bf3c1661b338815579a3511fedc814&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/5a788f09-7e31-81eb-a3dc-00039a1662d6/8fe4b630-be60-4cb1-aae8-42695d218c82/Screenshot_2026-03-21_at_16-38-20_FirstSolar_Series7-TR1_BR.pdf.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466W4WNCMCB%2F20260406%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260406T214418Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEA0aCXVzLXdlc3QtMiJHMEUCICYBhZ1VbvBK4p9VxC4t9skrlfJZLJXbHZ7Ym1xN6holAiEA2ajbrB7v9bTm%2FkfFAqxpax54tHug9mLmoy%2Bj%2FthBHCkqiAQI1v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDFQX%2BFTTemryhSM%2BAircA3WL2VvnWcLoAO8%2Fm4BqATPlXMBk2b683p0%2FVe0zoTrgtVHxvPOWR0d97KOwCeWFKakSQl6fyr4rSJ0NQ7fFdR5U%2FBKTijp7p5nSuNKkv7rrQ9ay%2FPwulNONGxNQJoYibBZD0IjJgFd%2FATjdvw6cwbejwUaHPKo9eVl0xDbJi39hgSPzJW8WRF2wP5%2FI71dNg3y51FK7er%2FAtDPNG%2FYzssE52CWhB6A0bVozZ4LgoKgGzCG267J%2FIofzsqvV6vqieQ05lsqBOuYGq3UzGtWWFS2VZy4yeVgv0MfqxFXfM%2FljwJ6fyL9xBdTj1zjR%2FUHTDERVGsORBiqtbdq5uG7eqyAZ75Jdn%2Biq9x%2Fzia8h3dHxXgj8ozIpznOXormfFidNtqWwa6t%2B484g1WiDKNRk3diCKTHzxKSslRnWzNu9RLr4Xwrpbe5g27i1%2FLtpX2b89NJTT6uBfi7C6jwOgIakBX%2B2E8dNfU%2BBiKsEzZP5ZvAlO15ptW2%2BcTgdJ%2F9j8BVpyt2z4PF%2BNNcy4wM9JydhRgXdJEdO3n6kREk9GoEEhjvSOETiiysk%2BSh4tt5lIgQq9joMgXrHKYU5q4A7fnOInIJkzVaNxpPXjsuHQ4cqcyY2xEJAnUbwp3wSQRoCMLvE0M4GOqUBO4wgdSjmAK84JJFrFhHXiMmKujVHiYhIZejuRonRlGYrZSPHYbiTXgezJA%2Fg1wGD5E5l9av6vmNR6wfu%2FV4ZBuwfwxrHMAoH%2F37qdjSEkkZpDhcCPAfaaYmF58foaALTlC7iSOvCXH57VyFksXMnkjNJpqHgxsd8udUfDbpPBtsJsuKscUs4wO1fLoO5vBaLJnbCiFfEg3ctYRivHpaECoIXqkbG&X-Amz-Signature=8d132bb81ed0d75e1ef22c306989a398007d9d4f2d20629860ef6b39996e6050&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/5a788f09-7e31-81eb-a3dc-00039a1662d6/c1190c69-7c12-4d31-868a-644fc3d0eeca/Screenshot_2026-03-21_at_16-38-58_FirstSolar_Series7-TR1_BR.pdf.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466W4WNCMCB%2F20260406%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260406T214418Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEA0aCXVzLXdlc3QtMiJHMEUCICYBhZ1VbvBK4p9VxC4t9skrlfJZLJXbHZ7Ym1xN6holAiEA2ajbrB7v9bTm%2FkfFAqxpax54tHug9mLmoy%2Bj%2FthBHCkqiAQI1v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDFQX%2BFTTemryhSM%2BAircA3WL2VvnWcLoAO8%2Fm4BqATPlXMBk2b683p0%2FVe0zoTrgtVHxvPOWR0d97KOwCeWFKakSQl6fyr4rSJ0NQ7fFdR5U%2FBKTijp7p5nSuNKkv7rrQ9ay%2FPwulNONGxNQJoYibBZD0IjJgFd%2FATjdvw6cwbejwUaHPKo9eVl0xDbJi39hgSPzJW8WRF2wP5%2FI71dNg3y51FK7er%2FAtDPNG%2FYzssE52CWhB6A0bVozZ4LgoKgGzCG267J%2FIofzsqvV6vqieQ05lsqBOuYGq3UzGtWWFS2VZy4yeVgv0MfqxFXfM%2FljwJ6fyL9xBdTj1zjR%2FUHTDERVGsORBiqtbdq5uG7eqyAZ75Jdn%2Biq9x%2Fzia8h3dHxXgj8ozIpznOXormfFidNtqWwa6t%2B484g1WiDKNRk3diCKTHzxKSslRnWzNu9RLr4Xwrpbe5g27i1%2FLtpX2b89NJTT6uBfi7C6jwOgIakBX%2B2E8dNfU%2BBiKsEzZP5ZvAlO15ptW2%2BcTgdJ%2F9j8BVpyt2z4PF%2BNNcy4wM9JydhRgXdJEdO3n6kREk9GoEEhjvSOETiiysk%2BSh4tt5lIgQq9joMgXrHKYU5q4A7fnOInIJkzVaNxpPXjsuHQ4cqcyY2xEJAnUbwp3wSQRoCMLvE0M4GOqUBO4wgdSjmAK84JJFrFhHXiMmKujVHiYhIZejuRonRlGYrZSPHYbiTXgezJA%2Fg1wGD5E5l9av6vmNR6wfu%2FV4ZBuwfwxrHMAoH%2F37qdjSEkkZpDhcCPAfaaYmF58foaALTlC7iSOvCXH57VyFksXMnkjNJpqHgxsd8udUfDbpPBtsJsuKscUs4wO1fLoO5vBaLJnbCiFfEg3ctYRivHpaECoIXqkbG&X-Amz-Signature=1741a3f592198db6200870584de5a53f4fc13d2ea9785c0e9f62d18b7ce13ba1&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/5a788f09-7e31-81eb-a3dc-00039a1662d6/83118598-51d9-4688-81ea-672acb22a697/FD9D72BC-69FA-4F62-821E-E6641EF9E0A8.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466W4WNCMCB%2F20260406%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260406T214418Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEA0aCXVzLXdlc3QtMiJHMEUCICYBhZ1VbvBK4p9VxC4t9skrlfJZLJXbHZ7Ym1xN6holAiEA2ajbrB7v9bTm%2FkfFAqxpax54tHug9mLmoy%2Bj%2FthBHCkqiAQI1v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDFQX%2BFTTemryhSM%2BAircA3WL2VvnWcLoAO8%2Fm4BqATPlXMBk2b683p0%2FVe0zoTrgtVHxvPOWR0d97KOwCeWFKakSQl6fyr4rSJ0NQ7fFdR5U%2FBKTijp7p5nSuNKkv7rrQ9ay%2FPwulNONGxNQJoYibBZD0IjJgFd%2FATjdvw6cwbejwUaHPKo9eVl0xDbJi39hgSPzJW8WRF2wP5%2FI71dNg3y51FK7er%2FAtDPNG%2FYzssE52CWhB6A0bVozZ4LgoKgGzCG267J%2FIofzsqvV6vqieQ05lsqBOuYGq3UzGtWWFS2VZy4yeVgv0MfqxFXfM%2FljwJ6fyL9xBdTj1zjR%2FUHTDERVGsORBiqtbdq5uG7eqyAZ75Jdn%2Biq9x%2Fzia8h3dHxXgj8ozIpznOXormfFidNtqWwa6t%2B484g1WiDKNRk3diCKTHzxKSslRnWzNu9RLr4Xwrpbe5g27i1%2FLtpX2b89NJTT6uBfi7C6jwOgIakBX%2B2E8dNfU%2BBiKsEzZP5ZvAlO15ptW2%2BcTgdJ%2F9j8BVpyt2z4PF%2BNNcy4wM9JydhRgXdJEdO3n6kREk9GoEEhjvSOETiiysk%2BSh4tt5lIgQq9joMgXrHKYU5q4A7fnOInIJkzVaNxpPXjsuHQ4cqcyY2xEJAnUbwp3wSQRoCMLvE0M4GOqUBO4wgdSjmAK84JJFrFhHXiMmKujVHiYhIZejuRonRlGYrZSPHYbiTXgezJA%2Fg1wGD5E5l9av6vmNR6wfu%2FV4ZBuwfwxrHMAoH%2F37qdjSEkkZpDhcCPAfaaYmF58foaALTlC7iSOvCXH57VyFksXMnkjNJpqHgxsd8udUfDbpPBtsJsuKscUs4wO1fLoO5vBaLJnbCiFfEg3ctYRivHpaECoIXqkbG&X-Amz-Signature=f9ec164e75224325fb3bab46430204a3d5b7cb64983d0e7bc5c245903db44e59&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
---
> POST-GTC 2026 UPDATE (2026-03-23) -- First Solar LOCKED IN as solar partner. Deployment scope now covers 3 sites. 800V DC solar-direct architecture confirmed.
## Updated Deployment Scope
    - Trappeys Cannery: 3,731 Series 7 TR1 panels across 4 rooftops = 2.05 MW. Phase 1: Building #3 (746 panels). Full campus: 112,500 sq ft.
    - Willow Glen: Ground mount array, 400+ acres available. Scale TBD but potentially 10-50+ MW.
    - MARLIE I: Smaller rooftop array, scope TBD.
## 800V DC Solar-Direct Architecture
First Solar TR1 panels feed directly into 800V DC bus via DC-DC converters (no AC inversion). 5-panel strings at 952V, buck to 800V. 97% efficiency vs 92% AC path. Eliminates 3 conversion stages.
    - Eaton Beam Rubin DSX handles the 800V DC distribution from solar input to GPU rack PDUs.
    - 10 open engineering questions documented in memory/projects/800vdc_solar_direct.md
## Contact Info (Current)
    - Module sales: modulesales@firstsolar.com
    - Phone: 419-662-6899
    - General: Info@FirstSolar.com
    - New Iberia factory: .1B investment, 30 mi from Trappeys, 90 mi from Willow Glen
## Key Selling Points for First Solar
    - ADC buys AMERICAN panels from their Louisiana factory -- validates their .1B investment
    - 3 sites = large-volume, multi-year relationship
    - 800V DC direct = showcases CdTe thin-film voltage characteristics (better than silicon for DC strings)
    - Federal alignment: 30% ITC + state incentives. FEOC-clean. Both parties benefit.
    - Co-marketing: First Solar panels powering Louisiana AI factory = great story for both brands
---
## CERAWeek 2026 Update — Technical Specs & 800V DC-Direct Architecture
> Updated 2026-03-25. First Solar Series 7 TR1 is LOCKED as ADC's Layer 1 solar panel. Nobody has coupled First Solar DC-direct to an 800V AI factory bus yet. ADC would be first.
---
### Series 7 TR1 — Updated Specifications
    - Power output: 550W per panel
    - Efficiency: 19.7% (CdTe thin-film)
    - Vmp (voltage at max power): 190.4V
    - Technology: Cadmium Telluride (CdTe) thin-film — no silicon, no polysilicon supply chain
    - Form factor: large-format commercial panel, optimized for rooftop and ground-mount
    - Degradation: <0.5%/year — best-in-class long-term performance
    - Temperature coefficient: superior to crystalline silicon in Louisiana heat
---
### 800V DC-Direct String Architecture
    - 5-panel series string: 5 x 190.4V = 952V open circuit
    - DC-DC buck conversion: 952V stepped down to 800V DC bus voltage
    - Efficiency gain: 97% DC-direct vs 92% AC inverter path (5% savings)
    - No AC inverter stage — eliminates conversion losses, harmonics, and failure points
    - Compatible with Eaton Beam Rubin DSX 800V DC power platform
    - ABB SACE Infinitus solid-state breaker for DC bus protection
    - OPEN QUESTION: DC-DC converter selection (SST candidates: Heron Power, Amperesand, Delta)
---
### New Iberia Factory — Updated Intel
    - Location: New Iberia, Louisiana — 30 miles from Trappeys
    - Investment: $1.1 billion
    - Capacity: 3.5 GW/year production
    - Workforce: 826+ employees (as of commissioning 2025)
    - Commissioned: 2025 — fully operational
    - This is the closest tier-1 solar manufacturing to any AI factory site in the US
---
### Trappeys Deployment — 2.05 MW Array
    - Total panels: 3,731 (Series 7 TR1)
    - Total capacity: 2.05 MW DC
    - Deployment: across 4 building rooftops (112,500 sq ft total)
    - Infrastructure yard concrete pad reserved for cooling/power, NOT solar
    - String configuration: 5-panel strings (952V) across all rooftops
    - Annual generation estimate: ~3,000 MWh (Louisiana solar irradiance)
---
### First-Mover Advantage
Nobody has coupled First Solar CdTe panels DC-direct to an 800V AI factory bus. The industry standard is AC inverter + AC-DC rectifier, losing 8-10% in double conversion. ADC's architecture eliminates both conversion stages.
This is a publishable engineering first — potential co-marketing with First Solar, NVIDIA (DSX), and Eaton (800V DC platform). White paper opportunity.
    - Prior art: Zero. No CdTe DC-direct to 800V DC bus in production anywhere
    - Closest analog: Some solar-direct EV charging at 400V — but not 800V, not AI factory scale
    - Patent opportunity: String architecture + DC-DC topology for AI factory integration
*[Child: Tier 2 — Operational Partners & Professional Services]*
> Tier 2 partners BUILD, INSTALL, CONNECT, and MAINTAIN the facility. Without them, Tier 1 hardware sits in crates.
Tier 1 = Hardware you can't run without (NVIDIA, Cat, Eaton, First Solar)
Tier 2 = People who build, install, and operate it (THIS PAGE)
Tier 3 = Government & institutional (LED, DOE, UL Lafayette, City Council)
---
# Engineering Services
These are the licensed professionals who stamp drawings, certify systems, and get permits approved. Without them, nothing gets energized.
## Licensed Electrical PE — 800V DC System Design
Scope: Design and stamp the 800V DC power distribution system. Solar string layout, genset interconnect, Beam Rubin DSX integration, arc flash study, short circuit analysis, NEC compliance.
    - Must have DC power experience — 800V DC is not standard commercial electrical. Most PEs do 480V AC. Find one who has done utility-scale solar or EV charging infrastructure.
    - Louisiana PE license required — stamps must be valid in-state
    - Eaton may provide design assist — Beam Rubin DSX comes with application engineering. PE still needed to stamp and take liability.
    - [ ] Contact Eaton rep — ask if they have preferred PE firms for DSX projects in Louisiana
    - [ ] Search Louisiana PE board for firms with DC power / renewable energy experience
    - [ ] Budget: $50,000-80,000 for full electrical engineering package
## Fire Protection Engineer (FPE) — Suppression & Detection Design
Scope: Design VESDA-E aspirating detection + Novec 1230/FM-200 clean agent suppression for compute area. Room integrity testing. AHJ coordination. Insurance carrier approval.
    - Must understand lithium battery fire risks — NVL72 racks have UPS batteries. Clean agent alone may not be sufficient. FPE must address thermal runaway scenarios.
    - Fike and Xtralis (Honeywell) both offer design services — but independent FPE stamps the drawings
    - [ ] Identify FPE firms in Louisiana with compute facility / clean agent experience
    - [ ] Budget: $25,000-40,000 for fire protection engineering package
## Structural Engineer — Roof Load Analysis
Scope: Verify all 4 Trappeys buildings can support rooftop solar. Phase 1 = Building #3 (63,300 lbs). Full campus = 316,500 lbs across 4 buildings. Seismic and wind load calcs (hurricane zone).
    - First Solar TR1 panels are heavier than silicon — CdTe glass-glass construction. ~85 lbs per panel. 746 panels = 63,410 lbs on Building #3 alone.
    - Historic buildings may have load restrictions — Trappeys is pre-1950s construction. Structural assessment is FIRST before any solar goes up.
    - [ ] Get structural engineering firm — Lafayette area, commercial/industrial roof experience
    - [ ] Budget: $15,000-25,000 for roof load analysis (all 4 buildings)
## Environmental Consultant — Permitting & Thermal Modeling
Scope: LDEQ LPDES permit application. Thermal discharge modeling (liquid cooling heat rejection). Brownfield assessment (former cannery — potential soil contamination). Noise study for gas gensets.
    - Brownfield advantage — former industrial site means zoning is already M2. But brownfield also means potential remediation costs. Environmental Phase I/II assessment tells you what is in the ground.
    - [ ] Engage environmental firm — Phase I ESA before closing on property
    - [ ] Budget: $20,000-40,000 (Phase I: $5K, Phase II if needed: $15-35K)
---
# Construction & Installation
## Solar EPC Contractor — Panel Installation
Scope: Engineer, procure (mounting hardware), and construct the rooftop solar array. Phase 1: 746 panels on Building #3. Full build: 3,731 panels across 4 buildings. Includes racking, wiring, combiners, commissioning.
    - First Solar may have preferred EPC partners — ask modulesales@firstsolar.com for Louisiana commercial installers with CdTe experience
    - Must be licensed in Louisiana (LLR contractor license, electrical license)
    - Look for NABCEP-certified installers — industry gold standard
    - [ ] Ask First Solar for Louisiana EPC referrals
    - [ ] Get 3 bids for Phase 1 installation (746 panels, Building #3)
## General Contractor — Building Modifications
Scope: Building penetrations (cable runs, cooling piping, exhaust). Concrete pad for genset + switchgear yard. Door modifications. Interior buildout for compute area (vapor barrier, insulation, flooring). Loading dock prep.
    - Historic building considerations — if pursuing 45% historic tax credits, all exterior modifications must comply with NPS Standards. GC must understand Secretary of Interior guidelines.
    - Lafayette-based preferred — local knowledge, relationships with inspectors, fast response
    - [ ] Identify 3 commercial GCs in Lafayette with industrial/warehouse renovation experience
## Licensed Electrical Contractor — Installation
Scope: Install everything the Electrical PE designs. Conduit runs, wire pulls, switchgear installation, PDU mounting, genset connection, utility interconnect, grounding grid. Separate from solar EPC (different skill set).
    - 800V DC experience is rare — most commercial electricians work 480V AC. Need a shop that has done industrial DC, mining, or EV charging infrastructure.
    - Budget from procurement matrix: $100,000-150,000 for Phase 1 electrical labor
    - [ ] Find electrical contractors with DC power experience in Louisiana
---
# Connectivity & Networking
## Dark Fiber / Backbone Provider
Scope: Dedicated fiber connecting Trappeys to MARLIE I (0.5 mi), and long-haul backbone to Willow Glen (60 mi). LUS Fiber handles last-mile metro. Need dark fiber or lit services for inter-site fabric and internet transit.
    - LUS Fiber — municipal fiber, 0.8 mi from site. Metro connectivity + sell-back grid interconnect. Part of Tier 1 (city relationship).
    - Zayo / Lumen / AT&T — long-haul dark fiber for Trappeys to Willow Glen backbone. Zayo has Louisiana fiber presence.
    - Starlink Business — backup/redundant internet. Not for compute fabric, but for management plane failover.
    - [ ] Check Zayo fiber map for Lafayette coverage
    - [ ] Get LUS Fiber commercial service quote for Trappeys address
---
# Security & Compliance
## Physical Security Integrator
Scope: Access control (badge readers, biometric), CCTV (AI-powered analytics), perimeter fencing, vehicle barriers. Required for NVIDIA NCP certification — physical security is an audit item.
    - NVIDIA Metropolis compatible cameras preferred — runs on Jetson edge compute. Same stack as KLFT. One vendor, one platform.
    - [ ] Identify security integrators in Acadiana — must support IP-based access control + AI video analytics
## Cybersecurity / SOC Provider
Scope: SOC-2 Type II compliance (required for enterprise customers). Network security monitoring. Penetration testing. Incident response plan. Required for NCP certification path.
    - Can start with managed SOC service — do not need in-house team for Phase 1
    - NVIDIA BlueField DPUs handle infrastructure-level security — but still need compliance framework and monitoring
    - [ ] Research managed SOC providers with compute facility experience
---
# Financial & Legal Services
## Equipment Financing / Leasing
Scope: Finance major equipment (gensets, switchgear, UPS) to preserve cash for site acquisition and NVIDIA hardware allocation. Explore vendor financing programs.
    - Cat Financial — built-in financing for all Caterpillar equipment. Lease or loan. Louisiana Cat handles everything.
    - Eaton Capital — Eaton offers equipment financing for power infrastructure. Ask during Beam Rubin engagement.
    - SBA 504 loan — up to $5.5M for equipment + real estate. 10% down, 25-year term. Perfect for site acquisition + Phase 1 buildout.
    - [ ] Ask Louisiana Cat about Cat Financial terms for prime-rated gas genset
    - [ ] Research SBA 504 lenders in Lafayette (LEDA may have contacts)
## Insurance & Bonding
Scope: Builder's risk (during construction), general liability, professional liability (E&O), property insurance, equipment breakdown, cyber liability. Required before any construction begins and before any customer workloads.
    - Compute facility insurance is specialized — standard commercial property will not cover $2M+ of GPU hardware. Need a broker who understands technology infrastructure.
    - NVIDIA may require minimum coverage levels for NCP certification
    - [ ] Find insurance broker with AI compute / technology infrastructure experience
## Legal Counsel
Scope: Entity structure (LLC vs C-Corp for investor readiness), vendor contracts, lease/purchase agreement for Trappeys, Act 730 application, ITEP filing, historic tax credit NPS applications, customer MSAs, IP protection.
    - Need two types: (1) Louisiana real estate/tax attorney for property + incentives, (2) technology/IP attorney for customer contracts + NVIDIA agreements
    - [ ] Identify Louisiana attorneys with LED incentive program experience (Act 730, ITEP)
---
# Workforce — First Hires
From ADC 3K Master Task Tracker — these are the first three hires before go-live.
## Site Manager / Ops Lead
    - First hire. Owns facility operations, vendor relationships on-site, safety, scheduling.
    - ROV industry background ideal — Lafayette has hundreds of experienced remote operations supervisors. Same skillset: complex equipment, safety-critical, 24/7 ops.
## 2x AI Compute Technicians
    - Rack, cable, monitor, troubleshoot GPU servers. Liquid cooling maintenance. Network fabric.
    - UL Lafayette pipeline — CS/EE students, LED FastStart training program (FREE customized training). This is why the university partnership matters.
    - [ ] Write job descriptions for all 3 roles
    - [ ] Contact LED FastStart for customized training program design
---
# Tier 2 Action Summary
23 action items above. Priority order:
    1. Structural engineer — nothing happens until roof loads are verified
    1. Environmental consultant — Phase I ESA before closing on property
    1. Electrical PE — 800V DC design is longest engineering lead time
    1. Legal counsel — entity structure + incentive applications need to start in parallel
    1. Insurance broker — builder's risk needed before construction begins
    1. Everything else — sequences after engineering designs are done

Estimated Tier 2 budget (engineering + services, NOT equipment): $300,000-500,000
This is on top of the $1.1-1.7M Phase 1 equipment budget in the procurement matrix.
---
> POST-GTC 2026 UPDATE (2026-03-23) -- Key Tier 2 changes driven by NVIDIA shipping complete racks and Eaton as 800V DC partner.
## Tier 2 Updates Post-GTC 2026
    - Electrical PE scope updated: Eaton Beam Rubin DSX provides application engineering + design assist. PE still needed to stamp drawings, but engineering workload reduced. Budget may decrease 20-30%.
    - CDU procurement REMOVED from Tier 2: NVIDIA ships liquid-cooled NVL72 racks complete with CDU. No separate Vertiv/CoolIT procurement for main racks.
    - Louisiana Cat Financial available for genset financing -- reduces upfront capital needs for Layer 2 power. Ask Spencer Landry (985-498-9336).
    - Eaton Capital available for power infrastructure financing -- reduces upfront capital for 800V DC distribution. Ask during Beam Rubin engagement.
    - SBA 504 loan still the best path for site acquisition + Phase 1 buildout (.5M, 10% down, 25-year term).
    - Workforce note: LED FastStart is FREE customized training. UL Lafayette pipeline stronger than ever -- Dr. Ramesh Kolluru (new Interim President) is a CS PhD and R1 builder. No GPU infra at UL means they NEED this partnership.
    - Multi-site scope: Tier 2 vendors now cover Trappeys + MARLIE I + Willow Glen. Same engineering firms, larger scope, better pricing.
---
> POST-GTC 2026 UPDATE (2026-03-23) -- ADC is now a NEOCLOUD. GPU-first cloud provider, not a colo. Energy-first model. Full NVIDIA stack. Sell tokens, not GPU hours. Major vendor stack changes below.
## Strategic Vendor Stack Changes (Post-GTC 2026)
  - Bloom Energy REMOVED from vendor stack -- fuel cells no longer in power hierarchy. 4-layer model: Solar > Natural Gas > Diesel Gensets > Grid (sell-back only).
  - EC-110 immersion vendors DEPRIORITIZED -- NVIDIA ships complete liquid-cooled racks (NVL72, 45C hot water, 2-hr install). Less custom cooling vendor work needed.
  - Eaton (Beam Rubin DSX) is THE 800V DC partner -- rectifier + busway + rack PDUs + supercapacitors + microgrid controller + xStorage BESS. Co-designed with NVIDIA. Contact made at GTC 2026.
  - Louisiana Cat Power Systems replaces Ring Power as generator partner -- 21 locations across Louisiana, services offshore rigs. Cat G3520C (1.5 MW, Trappeys/MARLIE I) + Cat CG260-16 (2.8 MW, Willow Glen, H2-ready 25% blend).
  - Diamond Green Diesel added as Tier 1 -- renewable diesel supply for Willow Glen emergency gensets. Norco, LA (60 river miles). 1.2B gallons/year. Barge delivery to 43-ft dock.
  - Hidrogenii (Plug Power + Olin) added as Tier 1 -- hydrogen supplier NEXT DOOR to Willow Glen. 15 TPD, commissioned April 2025. Cat CG260-16 supports 25% H2 blend.
  - NVIDIA contacts identified from GTC 2026 + LinkedIn outreach (March 2026). 2 InMails sent.
  - Multi-vendor future: Terafab (Tesla), AMD as options. But NVIDIA-first strategy remains.
## NVIDIA Key Contacts (Post-GTC 2026)
  - John Rendek -- Head of AI Factories for NPN (InMail SENT 2026-03-23)
  - Doug Traill -- Snr Director Solutions Architecture, AI Factory (InMail SENT 2026-03-23)
  - Craig Weinstein -- VP Americas Partner Organization
  - Garren Givens -- VP Ecosystem Enablement
  - Marc Hamilton -- VP Solutions Architecture
  - Jim Hennessy -- Senior Partner Business Manager
Priority: Rendek (AI Factories lead = direct path to NPN enrollment + hardware allocation) and Traill (Solutions Architecture = technical validation for DGX-Ready designation).
*[Child: Site Assets — Images & Media]*
*[Child: MARLIE I]*
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/5a788f09-7e31-81eb-a3dc-00039a1662d6/78df31df-3f50-45ce-b942-1775bf4729c8/Store_Front_Pic.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466VOL5FXRM%2F20260406%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260406T214423Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEA0aCXVzLXdlc3QtMiJHMEUCICmSIAFEGK6PNYPjea%2FgMvdiMFqWlU38f6vw%2B1ETDwmoAiEAosRj8OIn0lkYyO6wKt5ZLLXEyDtmAfj%2BtKzzc7EW8lAqiAQI1v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDEeXHiTv5U85TQ%2FgsCrcAyN9V2b%2Fm49EGDp5nsjFvmKziqBVSRT4gGpHiJ9oXQj7qJSbx6bbKxMsAS0SuesIqQpOtr3gRa4FuX6T%2Fsb04DutUpMTlGK64enbN0zpomFrpLysQ6EGQ%2FStL7YNW9hRhhJS9wppUN5XJ0hClWGZTA7PCVyLy2l%2BAfjkQ4hxULa4q5gVBoZZiha3R%2B%2FhazfwhZfm7%2BSHZaLBVB5hH4pX8yDeCJiAvp8eFfmVC%2Ba%2BzFQBZxs04b0EN84PDr%2BmDhsAoRndbzda4wJ1wLjDe615q%2BJCMGTxuVnSJUN1XKy%2B2mSL29ehsUsorOcQllV2K94BZtNdMUxl8W%2B%2FoivB7MwCw%2F1pOb%2FsR9VZJhaF2gvyyHV6%2FT9urKdmQcHehPlfTjqmZL8g7F2wpYIIaymIZArJm8omZhPROrkHeRPBx%2FFOJJly0E1%2BYnWLP18Pj66Mf1EZ8h1IO3G8yAajtqPxFNNdpxl7pKxum%2BlyDCaxyU0%2FBeIIlCLYvKwYj8%2FP6fO1rigCH9OTuNtm7HQfZmMqIP6kEUgB6CJP6ZP2qvkxL4C5j5H7lauFV9c%2FPwOBj58yZ9Hlz4Oay42wZ5tA4mK83xAVKY00%2FDwlH%2BTttYEGvoolmfAd6iNnvlDyOiZ63gelMKbE0M4GOqUB7RczH4MW42hLCopNmzF9JcVakgXqJR4yhYmgq72NUywAGJO8uQr%2FwKpge0vcSHomTy3CbZhSxG3Y%2Fddz%2FVxnzZR5Ty8e6v8bUaT%2Bf6RhfjHnqIa8k22jNoopdPY1i2Nzm4Fzj1J8fHEEa%2FfRdr1yJEYbCtfdb9LWdktCG%2BDSrTfZWotCVggSfK78eUiKzIqGylGr6nZ%2B2yJRhBojhSwA1Av1C5Ip&X-Amz-Signature=9335d4725468c0d1e0ee5c54281a6d8e8bc03be4b58e199ed10ad58adfcd22ad&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
*[Child: ADC 3K Pods]*
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/5a788f09-7e31-81eb-a3dc-00039a1662d6/e48f2b60-e445-4694-b3ac-d68bdac59527/Pod_hardware_and_software_stack.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466U6WD6QII%2F20260406%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260406T214423Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEA0aCXVzLXdlc3QtMiJIMEYCIQDXhXdYRVt%2Fe1l43ccEgiXjbR3%2BZXIFApaToPeru70uSgIhAOf5tHnukmjC8WqaVvIYuzdrN1mexkJ2demXgd6S3RUxKogECNb%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1Igz5tkxf%2FqwQMUt3AMsq3AOkt8ahN3vZpl8jxBLtdebXRaNOBr43DKJ4qU%2BiMnZsl04sjInTqUwJJfLCjwJsY7Ipt0M3%2BOo%2FQc5VeFJYtt0hf1zHzygjI8xyIObNmf7gOwKiYzlcbysug464FEkcdjS24kxuEsf8tNE4ABX9MJ7iANOdEeCZN%2FWXkTYegPXjraPA9KR04YSzBdqb4kW13wZYard7m5Z%2BsulKsaD%2BUrGMjGXCbkiyiLFROdVpyLwaPyNqcKUpGe3kzz1bT20oTY4DD3liI50aWXrwwJitSkBINWFeKV%2Fnz6dSPtHW%2BkyEZpqRHWQMzAkREC%2FzOZwbEFkYfQPDe7hci3WOul1OfURMwFM%2FW42EzVHtslJwKzFsq7iClxM%2B4sWJsxIk51bH2n3iBXLYVgbYhfjoQxMS3VNlSftYkyl4%2B0f6ESefs4cqKtf05%2F7HkjUcd7FBJlR4niuAktIe%2B7SPci86Dm5giqsXZXdtaywmFSS%2BtR6WChfiUrScEuKzqEFtKR3A0n8IXl8oZmsxXPHwxoAyoTfSen2AUxLz%2BPB9pzssCv4cYmNl2fA37yahdm68TRGWS5IWUX4J%2BoookHAC9ucPh5K7l%2FosTH72rGRl%2F%2BPzaNUKrKeVKuoix%2BordDojHdNSMzDaxdDOBjqkAUyfE857qGX7IHsitx6vwvghcxO6Y%2B5EqQugY8Znc5PHQJMJdYatK5ugfrfyWU9fTDAWsxrwNq6IGy%2FTP%2Fkl4lt16HPav6VFL2QPnNIf4qjO%2FnVkTEKQH4naiVZnop2FqtJU0lwmlEVo%2B1UyGGD39ppe%2BsUkEsKaIUco8CD3vkYl70sfaiEBTxEq2%2Fk%2BOixyCBQ0ngRJR8uI2nmYC6dCXCI2Yh1v&X-Amz-Signature=56582ca90d1ddc07209132e3798fbfec76cc536342a4576c6bc59ff50fe4d475&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/5a788f09-7e31-81eb-a3dc-00039a1662d6/3b4175b6-8fd9-4eaf-9063-26ffd5ddba58/FCEA0460-4A3F-49BC-9EB9-294B1EBF7C76.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466U6WD6QII%2F20260406%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260406T214423Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEA0aCXVzLXdlc3QtMiJIMEYCIQDXhXdYRVt%2Fe1l43ccEgiXjbR3%2BZXIFApaToPeru70uSgIhAOf5tHnukmjC8WqaVvIYuzdrN1mexkJ2demXgd6S3RUxKogECNb%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1Igz5tkxf%2FqwQMUt3AMsq3AOkt8ahN3vZpl8jxBLtdebXRaNOBr43DKJ4qU%2BiMnZsl04sjInTqUwJJfLCjwJsY7Ipt0M3%2BOo%2FQc5VeFJYtt0hf1zHzygjI8xyIObNmf7gOwKiYzlcbysug464FEkcdjS24kxuEsf8tNE4ABX9MJ7iANOdEeCZN%2FWXkTYegPXjraPA9KR04YSzBdqb4kW13wZYard7m5Z%2BsulKsaD%2BUrGMjGXCbkiyiLFROdVpyLwaPyNqcKUpGe3kzz1bT20oTY4DD3liI50aWXrwwJitSkBINWFeKV%2Fnz6dSPtHW%2BkyEZpqRHWQMzAkREC%2FzOZwbEFkYfQPDe7hci3WOul1OfURMwFM%2FW42EzVHtslJwKzFsq7iClxM%2B4sWJsxIk51bH2n3iBXLYVgbYhfjoQxMS3VNlSftYkyl4%2B0f6ESefs4cqKtf05%2F7HkjUcd7FBJlR4niuAktIe%2B7SPci86Dm5giqsXZXdtaywmFSS%2BtR6WChfiUrScEuKzqEFtKR3A0n8IXl8oZmsxXPHwxoAyoTfSen2AUxLz%2BPB9pzssCv4cYmNl2fA37yahdm68TRGWS5IWUX4J%2BoookHAC9ucPh5K7l%2FosTH72rGRl%2F%2BPzaNUKrKeVKuoix%2BordDojHdNSMzDaxdDOBjqkAUyfE857qGX7IHsitx6vwvghcxO6Y%2B5EqQugY8Znc5PHQJMJdYatK5ugfrfyWU9fTDAWsxrwNq6IGy%2FTP%2Fkl4lt16HPav6VFL2QPnNIf4qjO%2FnVkTEKQH4naiVZnop2FqtJU0lwmlEVo%2B1UyGGD39ppe%2BsUkEsKaIUco8CD3vkYl70sfaiEBTxEq2%2Fk%2BOixyCBQ0ngRJR8uI2nmYC6dCXCI2Yh1v&X-Amz-Signature=8b9c101440b3ac01162b6d80fafb429d0f773689ee64142037f3b67d6985eede&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/5a788f09-7e31-81eb-a3dc-00039a1662d6/85c92be2-5e3e-48fe-ad86-28338ac2307d/E6F1DC2C-BBAB-43B1-8A74-2F9E4EDE8A8A.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466U6WD6QII%2F20260406%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260406T214423Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEA0aCXVzLXdlc3QtMiJIMEYCIQDXhXdYRVt%2Fe1l43ccEgiXjbR3%2BZXIFApaToPeru70uSgIhAOf5tHnukmjC8WqaVvIYuzdrN1mexkJ2demXgd6S3RUxKogECNb%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1Igz5tkxf%2FqwQMUt3AMsq3AOkt8ahN3vZpl8jxBLtdebXRaNOBr43DKJ4qU%2BiMnZsl04sjInTqUwJJfLCjwJsY7Ipt0M3%2BOo%2FQc5VeFJYtt0hf1zHzygjI8xyIObNmf7gOwKiYzlcbysug464FEkcdjS24kxuEsf8tNE4ABX9MJ7iANOdEeCZN%2FWXkTYegPXjraPA9KR04YSzBdqb4kW13wZYard7m5Z%2BsulKsaD%2BUrGMjGXCbkiyiLFROdVpyLwaPyNqcKUpGe3kzz1bT20oTY4DD3liI50aWXrwwJitSkBINWFeKV%2Fnz6dSPtHW%2BkyEZpqRHWQMzAkREC%2FzOZwbEFkYfQPDe7hci3WOul1OfURMwFM%2FW42EzVHtslJwKzFsq7iClxM%2B4sWJsxIk51bH2n3iBXLYVgbYhfjoQxMS3VNlSftYkyl4%2B0f6ESefs4cqKtf05%2F7HkjUcd7FBJlR4niuAktIe%2B7SPci86Dm5giqsXZXdtaywmFSS%2BtR6WChfiUrScEuKzqEFtKR3A0n8IXl8oZmsxXPHwxoAyoTfSen2AUxLz%2BPB9pzssCv4cYmNl2fA37yahdm68TRGWS5IWUX4J%2BoookHAC9ucPh5K7l%2FosTH72rGRl%2F%2BPzaNUKrKeVKuoix%2BordDojHdNSMzDaxdDOBjqkAUyfE857qGX7IHsitx6vwvghcxO6Y%2B5EqQugY8Znc5PHQJMJdYatK5ugfrfyWU9fTDAWsxrwNq6IGy%2FTP%2Fkl4lt16HPav6VFL2QPnNIf4qjO%2FnVkTEKQH4naiVZnop2FqtJU0lwmlEVo%2B1UyGGD39ppe%2BsUkEsKaIUco8CD3vkYl70sfaiEBTxEq2%2Fk%2BOixyCBQ0ngRJR8uI2nmYC6dCXCI2Yh1v&X-Amz-Signature=09107ad5e327fc67fb6d3b2cd97c4edb4822fb9010f3c5b8dda43e46a33c2f76&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/5a788f09-7e31-81eb-a3dc-00039a1662d6/6bbc2355-6c0c-492d-a3cc-e80531a393bf/261A06BC-6DAA-4BF0-9C53-D8C918B78A3A.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466U6WD6QII%2F20260406%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260406T214423Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEA0aCXVzLXdlc3QtMiJIMEYCIQDXhXdYRVt%2Fe1l43ccEgiXjbR3%2BZXIFApaToPeru70uSgIhAOf5tHnukmjC8WqaVvIYuzdrN1mexkJ2demXgd6S3RUxKogECNb%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1Igz5tkxf%2FqwQMUt3AMsq3AOkt8ahN3vZpl8jxBLtdebXRaNOBr43DKJ4qU%2BiMnZsl04sjInTqUwJJfLCjwJsY7Ipt0M3%2BOo%2FQc5VeFJYtt0hf1zHzygjI8xyIObNmf7gOwKiYzlcbysug464FEkcdjS24kxuEsf8tNE4ABX9MJ7iANOdEeCZN%2FWXkTYegPXjraPA9KR04YSzBdqb4kW13wZYard7m5Z%2BsulKsaD%2BUrGMjGXCbkiyiLFROdVpyLwaPyNqcKUpGe3kzz1bT20oTY4DD3liI50aWXrwwJitSkBINWFeKV%2Fnz6dSPtHW%2BkyEZpqRHWQMzAkREC%2FzOZwbEFkYfQPDe7hci3WOul1OfURMwFM%2FW42EzVHtslJwKzFsq7iClxM%2B4sWJsxIk51bH2n3iBXLYVgbYhfjoQxMS3VNlSftYkyl4%2B0f6ESefs4cqKtf05%2F7HkjUcd7FBJlR4niuAktIe%2B7SPci86Dm5giqsXZXdtaywmFSS%2BtR6WChfiUrScEuKzqEFtKR3A0n8IXl8oZmsxXPHwxoAyoTfSen2AUxLz%2BPB9pzssCv4cYmNl2fA37yahdm68TRGWS5IWUX4J%2BoookHAC9ucPh5K7l%2FosTH72rGRl%2F%2BPzaNUKrKeVKuoix%2BordDojHdNSMzDaxdDOBjqkAUyfE857qGX7IHsitx6vwvghcxO6Y%2B5EqQugY8Znc5PHQJMJdYatK5ugfrfyWU9fTDAWsxrwNq6IGy%2FTP%2Fkl4lt16HPav6VFL2QPnNIf4qjO%2FnVkTEKQH4naiVZnop2FqtJU0lwmlEVo%2B1UyGGD39ppe%2BsUkEsKaIUco8CD3vkYl70sfaiEBTxEq2%2Fk%2BOixyCBQ0ngRJR8uI2nmYC6dCXCI2Yh1v&X-Amz-Signature=71262db04ef9b8950e820564560b0a2f645b16dce77ee5f41badad760556a4a2&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/5a788f09-7e31-81eb-a3dc-00039a1662d6/383d5d4e-fd6c-404a-a89e-3bddc8a7c87b/7F1FED12-14E2-484F-8D3F-45926324094D.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466U6WD6QII%2F20260406%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260406T214423Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEA0aCXVzLXdlc3QtMiJIMEYCIQDXhXdYRVt%2Fe1l43ccEgiXjbR3%2BZXIFApaToPeru70uSgIhAOf5tHnukmjC8WqaVvIYuzdrN1mexkJ2demXgd6S3RUxKogECNb%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1Igz5tkxf%2FqwQMUt3AMsq3AOkt8ahN3vZpl8jxBLtdebXRaNOBr43DKJ4qU%2BiMnZsl04sjInTqUwJJfLCjwJsY7Ipt0M3%2BOo%2FQc5VeFJYtt0hf1zHzygjI8xyIObNmf7gOwKiYzlcbysug464FEkcdjS24kxuEsf8tNE4ABX9MJ7iANOdEeCZN%2FWXkTYegPXjraPA9KR04YSzBdqb4kW13wZYard7m5Z%2BsulKsaD%2BUrGMjGXCbkiyiLFROdVpyLwaPyNqcKUpGe3kzz1bT20oTY4DD3liI50aWXrwwJitSkBINWFeKV%2Fnz6dSPtHW%2BkyEZpqRHWQMzAkREC%2FzOZwbEFkYfQPDe7hci3WOul1OfURMwFM%2FW42EzVHtslJwKzFsq7iClxM%2B4sWJsxIk51bH2n3iBXLYVgbYhfjoQxMS3VNlSftYkyl4%2B0f6ESefs4cqKtf05%2F7HkjUcd7FBJlR4niuAktIe%2B7SPci86Dm5giqsXZXdtaywmFSS%2BtR6WChfiUrScEuKzqEFtKR3A0n8IXl8oZmsxXPHwxoAyoTfSen2AUxLz%2BPB9pzssCv4cYmNl2fA37yahdm68TRGWS5IWUX4J%2BoookHAC9ucPh5K7l%2FosTH72rGRl%2F%2BPzaNUKrKeVKuoix%2BordDojHdNSMzDaxdDOBjqkAUyfE857qGX7IHsitx6vwvghcxO6Y%2B5EqQugY8Znc5PHQJMJdYatK5ugfrfyWU9fTDAWsxrwNq6IGy%2FTP%2Fkl4lt16HPav6VFL2QPnNIf4qjO%2FnVkTEKQH4naiVZnop2FqtJU0lwmlEVo%2B1UyGGD39ppe%2BsUkEsKaIUco8CD3vkYl70sfaiEBTxEq2%2Fk%2BOixyCBQ0ngRJR8uI2nmYC6dCXCI2Yh1v&X-Amz-Signature=e4d9353c68069d4024bb14032da2a2d5510ce7cff80b29bf22a4f81dceb6277a&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/5a788f09-7e31-81eb-a3dc-00039a1662d6/12dac1cc-18fa-47fc-8f7a-ccd975144f49/adc3k_side_view.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466U6WD6QII%2F20260406%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260406T214423Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEA0aCXVzLXdlc3QtMiJIMEYCIQDXhXdYRVt%2Fe1l43ccEgiXjbR3%2BZXIFApaToPeru70uSgIhAOf5tHnukmjC8WqaVvIYuzdrN1mexkJ2demXgd6S3RUxKogECNb%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1Igz5tkxf%2FqwQMUt3AMsq3AOkt8ahN3vZpl8jxBLtdebXRaNOBr43DKJ4qU%2BiMnZsl04sjInTqUwJJfLCjwJsY7Ipt0M3%2BOo%2FQc5VeFJYtt0hf1zHzygjI8xyIObNmf7gOwKiYzlcbysug464FEkcdjS24kxuEsf8tNE4ABX9MJ7iANOdEeCZN%2FWXkTYegPXjraPA9KR04YSzBdqb4kW13wZYard7m5Z%2BsulKsaD%2BUrGMjGXCbkiyiLFROdVpyLwaPyNqcKUpGe3kzz1bT20oTY4DD3liI50aWXrwwJitSkBINWFeKV%2Fnz6dSPtHW%2BkyEZpqRHWQMzAkREC%2FzOZwbEFkYfQPDe7hci3WOul1OfURMwFM%2FW42EzVHtslJwKzFsq7iClxM%2B4sWJsxIk51bH2n3iBXLYVgbYhfjoQxMS3VNlSftYkyl4%2B0f6ESefs4cqKtf05%2F7HkjUcd7FBJlR4niuAktIe%2B7SPci86Dm5giqsXZXdtaywmFSS%2BtR6WChfiUrScEuKzqEFtKR3A0n8IXl8oZmsxXPHwxoAyoTfSen2AUxLz%2BPB9pzssCv4cYmNl2fA37yahdm68TRGWS5IWUX4J%2BoookHAC9ucPh5K7l%2FosTH72rGRl%2F%2BPzaNUKrKeVKuoix%2BordDojHdNSMzDaxdDOBjqkAUyfE857qGX7IHsitx6vwvghcxO6Y%2B5EqQugY8Znc5PHQJMJdYatK5ugfrfyWU9fTDAWsxrwNq6IGy%2FTP%2Fkl4lt16HPav6VFL2QPnNIf4qjO%2FnVkTEKQH4naiVZnop2FqtJU0lwmlEVo%2B1UyGGD39ppe%2BsUkEsKaIUco8CD3vkYl70sfaiEBTxEq2%2Fk%2BOixyCBQ0ngRJR8uI2nmYC6dCXCI2Yh1v&X-Amz-Signature=b9f3c0f481c9f3672c8338a4c0a76281855b2fe084cb944876dde206625a60c7&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/5a788f09-7e31-81eb-a3dc-00039a1662d6/86c7b3ed-ec53-466d-a435-d34ede152683/made_in_usa.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466U6WD6QII%2F20260406%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260406T214423Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEA0aCXVzLXdlc3QtMiJIMEYCIQDXhXdYRVt%2Fe1l43ccEgiXjbR3%2BZXIFApaToPeru70uSgIhAOf5tHnukmjC8WqaVvIYuzdrN1mexkJ2demXgd6S3RUxKogECNb%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1Igz5tkxf%2FqwQMUt3AMsq3AOkt8ahN3vZpl8jxBLtdebXRaNOBr43DKJ4qU%2BiMnZsl04sjInTqUwJJfLCjwJsY7Ipt0M3%2BOo%2FQc5VeFJYtt0hf1zHzygjI8xyIObNmf7gOwKiYzlcbysug464FEkcdjS24kxuEsf8tNE4ABX9MJ7iANOdEeCZN%2FWXkTYegPXjraPA9KR04YSzBdqb4kW13wZYard7m5Z%2BsulKsaD%2BUrGMjGXCbkiyiLFROdVpyLwaPyNqcKUpGe3kzz1bT20oTY4DD3liI50aWXrwwJitSkBINWFeKV%2Fnz6dSPtHW%2BkyEZpqRHWQMzAkREC%2FzOZwbEFkYfQPDe7hci3WOul1OfURMwFM%2FW42EzVHtslJwKzFsq7iClxM%2B4sWJsxIk51bH2n3iBXLYVgbYhfjoQxMS3VNlSftYkyl4%2B0f6ESefs4cqKtf05%2F7HkjUcd7FBJlR4niuAktIe%2B7SPci86Dm5giqsXZXdtaywmFSS%2BtR6WChfiUrScEuKzqEFtKR3A0n8IXl8oZmsxXPHwxoAyoTfSen2AUxLz%2BPB9pzssCv4cYmNl2fA37yahdm68TRGWS5IWUX4J%2BoookHAC9ucPh5K7l%2FosTH72rGRl%2F%2BPzaNUKrKeVKuoix%2BordDojHdNSMzDaxdDOBjqkAUyfE857qGX7IHsitx6vwvghcxO6Y%2B5EqQugY8Znc5PHQJMJdYatK5ugfrfyWU9fTDAWsxrwNq6IGy%2FTP%2Fkl4lt16HPav6VFL2QPnNIf4qjO%2FnVkTEKQH4naiVZnop2FqtJU0lwmlEVo%2B1UyGGD39ppe%2BsUkEsKaIUco8CD3vkYl70sfaiEBTxEq2%2Fk%2BOixyCBQ0ngRJR8uI2nmYC6dCXCI2Yh1v&X-Amz-Signature=5fce9f5f2f0cad01330d04f6c9f4a0c8579868e3af329479c621c0267639246e&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/5a788f09-7e31-81eb-a3dc-00039a1662d6/5f6eb5b8-c320-40ce-b22a-6588a0f790c8/adc_logo.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466U6WD6QII%2F20260406%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260406T214423Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEA0aCXVzLXdlc3QtMiJIMEYCIQDXhXdYRVt%2Fe1l43ccEgiXjbR3%2BZXIFApaToPeru70uSgIhAOf5tHnukmjC8WqaVvIYuzdrN1mexkJ2demXgd6S3RUxKogECNb%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1Igz5tkxf%2FqwQMUt3AMsq3AOkt8ahN3vZpl8jxBLtdebXRaNOBr43DKJ4qU%2BiMnZsl04sjInTqUwJJfLCjwJsY7Ipt0M3%2BOo%2FQc5VeFJYtt0hf1zHzygjI8xyIObNmf7gOwKiYzlcbysug464FEkcdjS24kxuEsf8tNE4ABX9MJ7iANOdEeCZN%2FWXkTYegPXjraPA9KR04YSzBdqb4kW13wZYard7m5Z%2BsulKsaD%2BUrGMjGXCbkiyiLFROdVpyLwaPyNqcKUpGe3kzz1bT20oTY4DD3liI50aWXrwwJitSkBINWFeKV%2Fnz6dSPtHW%2BkyEZpqRHWQMzAkREC%2FzOZwbEFkYfQPDe7hci3WOul1OfURMwFM%2FW42EzVHtslJwKzFsq7iClxM%2B4sWJsxIk51bH2n3iBXLYVgbYhfjoQxMS3VNlSftYkyl4%2B0f6ESefs4cqKtf05%2F7HkjUcd7FBJlR4niuAktIe%2B7SPci86Dm5giqsXZXdtaywmFSS%2BtR6WChfiUrScEuKzqEFtKR3A0n8IXl8oZmsxXPHwxoAyoTfSen2AUxLz%2BPB9pzssCv4cYmNl2fA37yahdm68TRGWS5IWUX4J%2BoookHAC9ucPh5K7l%2FosTH72rGRl%2F%2BPzaNUKrKeVKuoix%2BordDojHdNSMzDaxdDOBjqkAUyfE857qGX7IHsitx6vwvghcxO6Y%2B5EqQugY8Znc5PHQJMJdYatK5ugfrfyWU9fTDAWsxrwNq6IGy%2FTP%2Fkl4lt16HPav6VFL2QPnNIf4qjO%2FnVkTEKQH4naiVZnop2FqtJU0lwmlEVo%2B1UyGGD39ppe%2BsUkEsKaIUco8CD3vkYl70sfaiEBTxEq2%2Fk%2BOixyCBQ0ngRJR8uI2nmYC6dCXCI2Yh1v&X-Amz-Signature=1c0aa48a4bbbb3d931a9a5bb171388be35be7c905da7be6ef95ab04add9fb36a&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/5a788f09-7e31-81eb-a3dc-00039a1662d6/cda0ec66-1c25-4dab-b277-a432b5329d9a/immersion_technology.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466U6WD6QII%2F20260406%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260406T214423Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEA0aCXVzLXdlc3QtMiJIMEYCIQDXhXdYRVt%2Fe1l43ccEgiXjbR3%2BZXIFApaToPeru70uSgIhAOf5tHnukmjC8WqaVvIYuzdrN1mexkJ2demXgd6S3RUxKogECNb%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1Igz5tkxf%2FqwQMUt3AMsq3AOkt8ahN3vZpl8jxBLtdebXRaNOBr43DKJ4qU%2BiMnZsl04sjInTqUwJJfLCjwJsY7Ipt0M3%2BOo%2FQc5VeFJYtt0hf1zHzygjI8xyIObNmf7gOwKiYzlcbysug464FEkcdjS24kxuEsf8tNE4ABX9MJ7iANOdEeCZN%2FWXkTYegPXjraPA9KR04YSzBdqb4kW13wZYard7m5Z%2BsulKsaD%2BUrGMjGXCbkiyiLFROdVpyLwaPyNqcKUpGe3kzz1bT20oTY4DD3liI50aWXrwwJitSkBINWFeKV%2Fnz6dSPtHW%2BkyEZpqRHWQMzAkREC%2FzOZwbEFkYfQPDe7hci3WOul1OfURMwFM%2FW42EzVHtslJwKzFsq7iClxM%2B4sWJsxIk51bH2n3iBXLYVgbYhfjoQxMS3VNlSftYkyl4%2B0f6ESefs4cqKtf05%2F7HkjUcd7FBJlR4niuAktIe%2B7SPci86Dm5giqsXZXdtaywmFSS%2BtR6WChfiUrScEuKzqEFtKR3A0n8IXl8oZmsxXPHwxoAyoTfSen2AUxLz%2BPB9pzssCv4cYmNl2fA37yahdm68TRGWS5IWUX4J%2BoookHAC9ucPh5K7l%2FosTH72rGRl%2F%2BPzaNUKrKeVKuoix%2BordDojHdNSMzDaxdDOBjqkAUyfE857qGX7IHsitx6vwvghcxO6Y%2B5EqQugY8Znc5PHQJMJdYatK5ugfrfyWU9fTDAWsxrwNq6IGy%2FTP%2Fkl4lt16HPav6VFL2QPnNIf4qjO%2FnVkTEKQH4naiVZnop2FqtJU0lwmlEVo%2B1UyGGD39ppe%2BsUkEsKaIUco8CD3vkYl70sfaiEBTxEq2%2Fk%2BOixyCBQ0ngRJR8uI2nmYC6dCXCI2Yh1v&X-Amz-Signature=9c2c344e5e12966eac6b63e978c5b7fb42971ec9bf4bd972f134336cf0116b53&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
*[Child: KLFT / SkyCommand]*
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/5a788f09-7e31-81eb-a3dc-00039a1662d6/971bfed4-d525-4cef-9823-f0978816a579/drone.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466TGN2VF5L%2F20260406%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260406T214423Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEA0aCXVzLXdlc3QtMiJIMEYCIQC%2FyHe88OKL2qm4aWlpX1pOt1%2BsfBwQ37sy4WMuSDcV8wIhANQQF%2BvEhmaDLlQdDBhOLAVKgkY1mf0bTuqVD3OlKffwKogECNb%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1IgyAFkrU0K3UdImz3O8q3ANyNtDsB4XGT7SHKjbSTNYcy7muY4KU%2BDUlWadUksQbtfPShZVhMW07orN%2FoH82JWLafOrJSmHx6bMesTb2yxNnwaOMfg%2FSXiBEyDSZHSrQ2%2Fl5I3353ceBfbaa0ha5GFGnVyW10aFSvtzw5jmzx2FVCMMqkxZ%2Big9gYIB4udikHiOhAvTCjSlO9JS3l1saR2ynUGDYRloW2jee7C9P%2BAMvj8MOSZa5GQF2I4A7i7Sdvmd53IEwGUXOW2yoipqPax2dsySPDVerUGqkYru5maaP81tFBOb6KKUaGreNw%2BZzk%2F3D%2FWzxoXRaNZWFLbeVIDqLsW%2B32cNzBvHhYzfJxJeW70UCStsHuB5bpmKwx7lcg75lzKjBe6Xmaez%2F6goQ5gUkAAc%2Fzbnkh%2F6vZYeSsOII4w0p9RcukN89Ftzq2Y2K63K338KeIYR4jiYlE08JRu9NapVA7ZKGNDo5qh2d0PRwtBZOxdQyYpTcG9sNIugJL1d9z1TXuVM35Rh%2BD%2FqbK94iInR%2BGRE3BxXoM0FN8dpnXASJGVinnrvkP4O9vQMAWW3OHVpOJ4CvqbbRRQtUuUhCFyvoaFKDdtbjI81GBq5B3gLwraK07OifEvM%2BacOZr8bhNfCdWfP8UsE6TzCaxNDOBjqkAdNYtD3Pie4pGKwTaVK7MLblNrA9I6mDDah%2BgUFMf9HioiyNVLFmnFHMWjoW%2BATzpy4w9xK0fLFEfpjs2769szaCa681Ss9H%2FjWPcvT4T0Pb2%2F%2Ft36amz6HvleBafJKTqZydwSjk%2B%2BavBFPJES4zaoDKc8f5mi41ijncB5XmzNDOtjIi346SodA2E0rkEnZSauYr%2BxcCUqIHH43gH6shzer%2BnKNr&X-Amz-Signature=7252ff0999a752e240552ebc8d45eba18c9c9d16998770d160ffd5b93a08d84d&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/5a788f09-7e31-81eb-a3dc-00039a1662d6/be1d0e65-6c31-432e-8672-1c79b2d92abe/nvidia_security.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466TGN2VF5L%2F20260406%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260406T214423Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEA0aCXVzLXdlc3QtMiJIMEYCIQC%2FyHe88OKL2qm4aWlpX1pOt1%2BsfBwQ37sy4WMuSDcV8wIhANQQF%2BvEhmaDLlQdDBhOLAVKgkY1mf0bTuqVD3OlKffwKogECNb%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1IgyAFkrU0K3UdImz3O8q3ANyNtDsB4XGT7SHKjbSTNYcy7muY4KU%2BDUlWadUksQbtfPShZVhMW07orN%2FoH82JWLafOrJSmHx6bMesTb2yxNnwaOMfg%2FSXiBEyDSZHSrQ2%2Fl5I3353ceBfbaa0ha5GFGnVyW10aFSvtzw5jmzx2FVCMMqkxZ%2Big9gYIB4udikHiOhAvTCjSlO9JS3l1saR2ynUGDYRloW2jee7C9P%2BAMvj8MOSZa5GQF2I4A7i7Sdvmd53IEwGUXOW2yoipqPax2dsySPDVerUGqkYru5maaP81tFBOb6KKUaGreNw%2BZzk%2F3D%2FWzxoXRaNZWFLbeVIDqLsW%2B32cNzBvHhYzfJxJeW70UCStsHuB5bpmKwx7lcg75lzKjBe6Xmaez%2F6goQ5gUkAAc%2Fzbnkh%2F6vZYeSsOII4w0p9RcukN89Ftzq2Y2K63K338KeIYR4jiYlE08JRu9NapVA7ZKGNDo5qh2d0PRwtBZOxdQyYpTcG9sNIugJL1d9z1TXuVM35Rh%2BD%2FqbK94iInR%2BGRE3BxXoM0FN8dpnXASJGVinnrvkP4O9vQMAWW3OHVpOJ4CvqbbRRQtUuUhCFyvoaFKDdtbjI81GBq5B3gLwraK07OifEvM%2BacOZr8bhNfCdWfP8UsE6TzCaxNDOBjqkAdNYtD3Pie4pGKwTaVK7MLblNrA9I6mDDah%2BgUFMf9HioiyNVLFmnFHMWjoW%2BATzpy4w9xK0fLFEfpjs2769szaCa681Ss9H%2FjWPcvT4T0Pb2%2F%2Ft36amz6HvleBafJKTqZydwSjk%2B%2BavBFPJES4zaoDKc8f5mi41ijncB5XmzNDOtjIi346SodA2E0rkEnZSauYr%2BxcCUqIHH43gH6shzer%2BnKNr&X-Amz-Signature=3931846377999dc356e10ec4a7a4d4a151c590b198f567299d4402c3072aa2eb&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/5a788f09-7e31-81eb-a3dc-00039a1662d6/f650740e-08b0-46ad-99fa-91cf9ee64f7d/Drone_2.jpeg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466TGN2VF5L%2F20260406%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260406T214423Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEA0aCXVzLXdlc3QtMiJIMEYCIQC%2FyHe88OKL2qm4aWlpX1pOt1%2BsfBwQ37sy4WMuSDcV8wIhANQQF%2BvEhmaDLlQdDBhOLAVKgkY1mf0bTuqVD3OlKffwKogECNb%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1IgyAFkrU0K3UdImz3O8q3ANyNtDsB4XGT7SHKjbSTNYcy7muY4KU%2BDUlWadUksQbtfPShZVhMW07orN%2FoH82JWLafOrJSmHx6bMesTb2yxNnwaOMfg%2FSXiBEyDSZHSrQ2%2Fl5I3353ceBfbaa0ha5GFGnVyW10aFSvtzw5jmzx2FVCMMqkxZ%2Big9gYIB4udikHiOhAvTCjSlO9JS3l1saR2ynUGDYRloW2jee7C9P%2BAMvj8MOSZa5GQF2I4A7i7Sdvmd53IEwGUXOW2yoipqPax2dsySPDVerUGqkYru5maaP81tFBOb6KKUaGreNw%2BZzk%2F3D%2FWzxoXRaNZWFLbeVIDqLsW%2B32cNzBvHhYzfJxJeW70UCStsHuB5bpmKwx7lcg75lzKjBe6Xmaez%2F6goQ5gUkAAc%2Fzbnkh%2F6vZYeSsOII4w0p9RcukN89Ftzq2Y2K63K338KeIYR4jiYlE08JRu9NapVA7ZKGNDo5qh2d0PRwtBZOxdQyYpTcG9sNIugJL1d9z1TXuVM35Rh%2BD%2FqbK94iInR%2BGRE3BxXoM0FN8dpnXASJGVinnrvkP4O9vQMAWW3OHVpOJ4CvqbbRRQtUuUhCFyvoaFKDdtbjI81GBq5B3gLwraK07OifEvM%2BacOZr8bhNfCdWfP8UsE6TzCaxNDOBjqkAdNYtD3Pie4pGKwTaVK7MLblNrA9I6mDDah%2BgUFMf9HioiyNVLFmnFHMWjoW%2BATzpy4w9xK0fLFEfpjs2769szaCa681Ss9H%2FjWPcvT4T0Pb2%2F%2Ft36amz6HvleBafJKTqZydwSjk%2B%2BavBFPJES4zaoDKc8f5mi41ijncB5XmzNDOtjIi346SodA2E0rkEnZSauYr%2BxcCUqIHH43gH6shzer%2BnKNr&X-Amz-Signature=fbe39f2108018ae9b372184d3553c5bda341f50d93a02f49da123debe3969dc9&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
*[Child: Henry Hub & Power]*
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/5a788f09-7e31-81eb-a3dc-00039a1662d6/13493b4e-9f74-4af7-b136-4979abb2bc48/A%21_Growth.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4664TUWQHPS%2F20260406%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260406T214424Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEA0aCXVzLXdlc3QtMiJGMEQCIHhbRO0Xo5bi5cSFrUE9895wVySC3oHu8kXDX%2FVURLLtAiAS5hvsSQE9Um0S0WTvAsXHslebr%2BPb1e3FefvtUgbcCSqIBAjW%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMQga8vsmP7lU%2BHah9KtwDKYeNh1OIfFyIeXOUqYzyCbXvHY7HaCJHw8FMHcvesPDdVlPeM2mo9Ayyf7%2B5QEXSBxvF%2BGepm8IRRAVPrZJbZ37TKBSXIWV4aJohmcLUO6NKmPyizQei8PiEMbxLNBxfCelYkw4WzAyqY%2BwK4MgrFqTmJyo%2B9kGbe3cj5LK7MTARU%2B%2FR5yZHQXwqI%2BFrXvYuv1RGlAKteFUNbnUNxX6Hv9CLtRcyeOS5HPUTNAxBagvDChGL%2BG54wpH1SdfRxfc4uaqi3r0RzeoPb0310zAnBWR2cT4XrVOE0keNtoBV7VANtK%2B8D39GXiyJ12WiWCl66lOEpVfevn52v%2FCJvRG9BIeRiknhlJ3kc8gx753%2BQcvlNHSoidt%2BslJDzlfTOCnFoc6PPWW1fW0yTMdSDgm%2BCU3g8BRxI9Lrj%2F3jp7NeZCIOhRLRDSG04IUYoGU%2FWVXhx7Ow18LsQ53hkPE5LAm7DKiIYFTv%2FUY3rGno8wUTOElVJ1uIuPG3C6x%2B%2B2nlSC3hqGRc4HICwUb27WKjklYCI8yMYJTSw%2FgFxzNSp5ji0t47VNSpPSDLjjPV0l7%2Fcd1uxeRciChhYjRAuJ6fuGcaQhiXro6d2NIyZHDdZMkeK5sX%2F8gJ%2BTwnKfZZ%2FCUwncTQzgY6pgEpMV5iukza7%2BxZWVWBJC%2BCM5FyBj6IkadzUpwe6sn%2Bs4gE7wwoEa6LPP0sF4nrodUOmzIkzL0bgRx1NA1Dj0iRFv4kR6o1iZXa1%2BuFrTarurjtT0XwDZrUBjTZjIH4WW9pHTFm0F%2FIgbmuKmM0pc%2FAEcbWAOmESpQABw%2FqMxx4fQC2jqWyTv%2FzymOmjCRG3IWnM%2ByEMPYq68vsJafUQHFeUAeKKZ80&X-Amz-Signature=c7f437b0701a81f30b98be7e446f49b925b83a68f4fa7060bbd26ce6e50987ac&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/5a788f09-7e31-81eb-a3dc-00039a1662d6/003331d0-ba72-45ce-9d18-ca5f82c7d77e/64F5C3E2-6276-49B5-AA9A-EA4E9EEEB804.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4664TUWQHPS%2F20260406%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260406T214424Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEA0aCXVzLXdlc3QtMiJGMEQCIHhbRO0Xo5bi5cSFrUE9895wVySC3oHu8kXDX%2FVURLLtAiAS5hvsSQE9Um0S0WTvAsXHslebr%2BPb1e3FefvtUgbcCSqIBAjW%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMQga8vsmP7lU%2BHah9KtwDKYeNh1OIfFyIeXOUqYzyCbXvHY7HaCJHw8FMHcvesPDdVlPeM2mo9Ayyf7%2B5QEXSBxvF%2BGepm8IRRAVPrZJbZ37TKBSXIWV4aJohmcLUO6NKmPyizQei8PiEMbxLNBxfCelYkw4WzAyqY%2BwK4MgrFqTmJyo%2B9kGbe3cj5LK7MTARU%2B%2FR5yZHQXwqI%2BFrXvYuv1RGlAKteFUNbnUNxX6Hv9CLtRcyeOS5HPUTNAxBagvDChGL%2BG54wpH1SdfRxfc4uaqi3r0RzeoPb0310zAnBWR2cT4XrVOE0keNtoBV7VANtK%2B8D39GXiyJ12WiWCl66lOEpVfevn52v%2FCJvRG9BIeRiknhlJ3kc8gx753%2BQcvlNHSoidt%2BslJDzlfTOCnFoc6PPWW1fW0yTMdSDgm%2BCU3g8BRxI9Lrj%2F3jp7NeZCIOhRLRDSG04IUYoGU%2FWVXhx7Ow18LsQ53hkPE5LAm7DKiIYFTv%2FUY3rGno8wUTOElVJ1uIuPG3C6x%2B%2B2nlSC3hqGRc4HICwUb27WKjklYCI8yMYJTSw%2FgFxzNSp5ji0t47VNSpPSDLjjPV0l7%2Fcd1uxeRciChhYjRAuJ6fuGcaQhiXro6d2NIyZHDdZMkeK5sX%2F8gJ%2BTwnKfZZ%2FCUwncTQzgY6pgEpMV5iukza7%2BxZWVWBJC%2BCM5FyBj6IkadzUpwe6sn%2Bs4gE7wwoEa6LPP0sF4nrodUOmzIkzL0bgRx1NA1Dj0iRFv4kR6o1iZXa1%2BuFrTarurjtT0XwDZrUBjTZjIH4WW9pHTFm0F%2FIgbmuKmM0pc%2FAEcbWAOmESpQABw%2FqMxx4fQC2jqWyTv%2FzymOmjCRG3IWnM%2ByEMPYq68vsJafUQHFeUAeKKZ80&X-Amz-Signature=cbf65aab6d4a758a3be78bea496de724aa1d55e0211cfcf8234f9bda542c1b56&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/5a788f09-7e31-81eb-a3dc-00039a1662d6/93773b7b-be0d-4e39-966c-e317163639a2/35297B0E-4219-4050-8998-03AA18351CDF.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4664TUWQHPS%2F20260406%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260406T214424Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEA0aCXVzLXdlc3QtMiJGMEQCIHhbRO0Xo5bi5cSFrUE9895wVySC3oHu8kXDX%2FVURLLtAiAS5hvsSQE9Um0S0WTvAsXHslebr%2BPb1e3FefvtUgbcCSqIBAjW%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMQga8vsmP7lU%2BHah9KtwDKYeNh1OIfFyIeXOUqYzyCbXvHY7HaCJHw8FMHcvesPDdVlPeM2mo9Ayyf7%2B5QEXSBxvF%2BGepm8IRRAVPrZJbZ37TKBSXIWV4aJohmcLUO6NKmPyizQei8PiEMbxLNBxfCelYkw4WzAyqY%2BwK4MgrFqTmJyo%2B9kGbe3cj5LK7MTARU%2B%2FR5yZHQXwqI%2BFrXvYuv1RGlAKteFUNbnUNxX6Hv9CLtRcyeOS5HPUTNAxBagvDChGL%2BG54wpH1SdfRxfc4uaqi3r0RzeoPb0310zAnBWR2cT4XrVOE0keNtoBV7VANtK%2B8D39GXiyJ12WiWCl66lOEpVfevn52v%2FCJvRG9BIeRiknhlJ3kc8gx753%2BQcvlNHSoidt%2BslJDzlfTOCnFoc6PPWW1fW0yTMdSDgm%2BCU3g8BRxI9Lrj%2F3jp7NeZCIOhRLRDSG04IUYoGU%2FWVXhx7Ow18LsQ53hkPE5LAm7DKiIYFTv%2FUY3rGno8wUTOElVJ1uIuPG3C6x%2B%2B2nlSC3hqGRc4HICwUb27WKjklYCI8yMYJTSw%2FgFxzNSp5ji0t47VNSpPSDLjjPV0l7%2Fcd1uxeRciChhYjRAuJ6fuGcaQhiXro6d2NIyZHDdZMkeK5sX%2F8gJ%2BTwnKfZZ%2FCUwncTQzgY6pgEpMV5iukza7%2BxZWVWBJC%2BCM5FyBj6IkadzUpwe6sn%2Bs4gE7wwoEa6LPP0sF4nrodUOmzIkzL0bgRx1NA1Dj0iRFv4kR6o1iZXa1%2BuFrTarurjtT0XwDZrUBjTZjIH4WW9pHTFm0F%2FIgbmuKmM0pc%2FAEcbWAOmESpQABw%2FqMxx4fQC2jqWyTv%2FzymOmjCRG3IWnM%2ByEMPYq68vsJafUQHFeUAeKKZ80&X-Amz-Signature=307175631e6fe45bfdd7d2bdcde252464a0a4b164eda8196bc938eae4c62d556&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/5a788f09-7e31-81eb-a3dc-00039a1662d6/513797e3-3315-4377-a87b-c12adc31da1b/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4664TUWQHPS%2F20260406%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260406T214424Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEA0aCXVzLXdlc3QtMiJGMEQCIHhbRO0Xo5bi5cSFrUE9895wVySC3oHu8kXDX%2FVURLLtAiAS5hvsSQE9Um0S0WTvAsXHslebr%2BPb1e3FefvtUgbcCSqIBAjW%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMQga8vsmP7lU%2BHah9KtwDKYeNh1OIfFyIeXOUqYzyCbXvHY7HaCJHw8FMHcvesPDdVlPeM2mo9Ayyf7%2B5QEXSBxvF%2BGepm8IRRAVPrZJbZ37TKBSXIWV4aJohmcLUO6NKmPyizQei8PiEMbxLNBxfCelYkw4WzAyqY%2BwK4MgrFqTmJyo%2B9kGbe3cj5LK7MTARU%2B%2FR5yZHQXwqI%2BFrXvYuv1RGlAKteFUNbnUNxX6Hv9CLtRcyeOS5HPUTNAxBagvDChGL%2BG54wpH1SdfRxfc4uaqi3r0RzeoPb0310zAnBWR2cT4XrVOE0keNtoBV7VANtK%2B8D39GXiyJ12WiWCl66lOEpVfevn52v%2FCJvRG9BIeRiknhlJ3kc8gx753%2BQcvlNHSoidt%2BslJDzlfTOCnFoc6PPWW1fW0yTMdSDgm%2BCU3g8BRxI9Lrj%2F3jp7NeZCIOhRLRDSG04IUYoGU%2FWVXhx7Ow18LsQ53hkPE5LAm7DKiIYFTv%2FUY3rGno8wUTOElVJ1uIuPG3C6x%2B%2B2nlSC3hqGRc4HICwUb27WKjklYCI8yMYJTSw%2FgFxzNSp5ji0t47VNSpPSDLjjPV0l7%2Fcd1uxeRciChhYjRAuJ6fuGcaQhiXro6d2NIyZHDdZMkeK5sX%2F8gJ%2BTwnKfZZ%2FCUwncTQzgY6pgEpMV5iukza7%2BxZWVWBJC%2BCM5FyBj6IkadzUpwe6sn%2Bs4gE7wwoEa6LPP0sF4nrodUOmzIkzL0bgRx1NA1Dj0iRFv4kR6o1iZXa1%2BuFrTarurjtT0XwDZrUBjTZjIH4WW9pHTFm0F%2FIgbmuKmM0pc%2FAEcbWAOmESpQABw%2FqMxx4fQC2jqWyTv%2FzymOmjCRG3IWnM%2ByEMPYq68vsJafUQHFeUAeKKZ80&X-Amz-Signature=05f5d2e430cbb2cf96c9619c1114b69b402ca0d1a7dc63806779801c71e7deb4&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/5a788f09-7e31-81eb-a3dc-00039a1662d6/933960ab-712d-4741-b84e-eb89a7314603/AI_Factory_archtecture.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4664TUWQHPS%2F20260406%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260406T214424Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEA0aCXVzLXdlc3QtMiJGMEQCIHhbRO0Xo5bi5cSFrUE9895wVySC3oHu8kXDX%2FVURLLtAiAS5hvsSQE9Um0S0WTvAsXHslebr%2BPb1e3FefvtUgbcCSqIBAjW%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMQga8vsmP7lU%2BHah9KtwDKYeNh1OIfFyIeXOUqYzyCbXvHY7HaCJHw8FMHcvesPDdVlPeM2mo9Ayyf7%2B5QEXSBxvF%2BGepm8IRRAVPrZJbZ37TKBSXIWV4aJohmcLUO6NKmPyizQei8PiEMbxLNBxfCelYkw4WzAyqY%2BwK4MgrFqTmJyo%2B9kGbe3cj5LK7MTARU%2B%2FR5yZHQXwqI%2BFrXvYuv1RGlAKteFUNbnUNxX6Hv9CLtRcyeOS5HPUTNAxBagvDChGL%2BG54wpH1SdfRxfc4uaqi3r0RzeoPb0310zAnBWR2cT4XrVOE0keNtoBV7VANtK%2B8D39GXiyJ12WiWCl66lOEpVfevn52v%2FCJvRG9BIeRiknhlJ3kc8gx753%2BQcvlNHSoidt%2BslJDzlfTOCnFoc6PPWW1fW0yTMdSDgm%2BCU3g8BRxI9Lrj%2F3jp7NeZCIOhRLRDSG04IUYoGU%2FWVXhx7Ow18LsQ53hkPE5LAm7DKiIYFTv%2FUY3rGno8wUTOElVJ1uIuPG3C6x%2B%2B2nlSC3hqGRc4HICwUb27WKjklYCI8yMYJTSw%2FgFxzNSp5ji0t47VNSpPSDLjjPV0l7%2Fcd1uxeRciChhYjRAuJ6fuGcaQhiXro6d2NIyZHDdZMkeK5sX%2F8gJ%2BTwnKfZZ%2FCUwncTQzgY6pgEpMV5iukza7%2BxZWVWBJC%2BCM5FyBj6IkadzUpwe6sn%2Bs4gE7wwoEa6LPP0sF4nrodUOmzIkzL0bgRx1NA1Dj0iRFv4kR6o1iZXa1%2BuFrTarurjtT0XwDZrUBjTZjIH4WW9pHTFm0F%2FIgbmuKmM0pc%2FAEcbWAOmESpQABw%2FqMxx4fQC2jqWyTv%2FzymOmjCRG3IWnM%2ByEMPYq68vsJafUQHFeUAeKKZ80&X-Amz-Signature=3d754c7353a7b266c8d172e34c2698b8cf1071417a0c1ca615e2bc2b87dd2a06&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/5a788f09-7e31-81eb-a3dc-00039a1662d6/deae9729-dffe-436f-bed3-c181c2d8a809/immersion_cooling.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466VMARKJUU%2F20260406%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260406T214429Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEA0aCXVzLXdlc3QtMiJHMEUCIC1K34ZEIFV88N2KzVJWHiq%2BQI3LyNq7W9TFdrRCmWszAiEAuuCF%2B%2FjM0ZqWWDR56OrfHLBkjv9qF5d%2BQQqW90cfG9gqiAQI1v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDFgxj6JQSDYG3bWUZyrcAwNHM4PxJE5MKSp2yEyWfw3SbxcUzH%2B7%2FD9MVTM2oi2efS1LuaLIUHx6p2pnLxfQIdYa%2FyDvWbBDjDvxVicSIw4XXPn%2FqJtlF81IuWSf3Fr3fnz3dqxtJ0flMmEOnLmWa%2FHVoxukcyYSLQO3OSxtc%2FlTFLRfQo%2BxIbHenVFv3yeI0ZdoHXyw1bacbH67YLOk9b79mnjZTLrunyUeaU0E52%2FDVexis%2FFqMyD2PuL6GShwunQP51DHqutxanbB7l6lLFrKsmJmrCMjsD9Rjk1OfuS1%2FYAayEAsE8Mj%2BqsS1efrHYGcbRBlAJDQDq8kUgcWQ%2Bta0xiWKZfJV9yo7NDgwx7VGM8GeJtawYYvq5KopEYLu7L0r1BY4KPXKRVpKtzf%2FpdoMFFpkU4kl6EhF1XyUwYC09RmyrVOtoWsWK0ZHjQ17pEpCd7NiSjdeQKG6Q5dp5WuRXhrV0GVTCNKOP5o%2BS%2FYFQXoWzdUiYwEXsFdFSlHxJ7d5gLOvSIsH8uO6SKXy7kh%2BMB9f4Gb54LdYD9aNIt442f8ZexhCMzAVy7GuFf3D0hnv%2B5ZYzqPCE6pVN5DQeSYDl6zrY81kz1zHEusOfuQBSJzepQsHYQQC30i%2BRNuTKllUgY6iPTyK1XvMKXE0M4GOqUByDX7RRwVcFRkdGJM7MA79ctj9Un7emTGbaYS8cenoLQkKQGjkLn30ZYoW2ReQPtlbNFuLP7zezfmvFCoRkpmhE7PD22f5oqkQBx8xdVusR048X5TNSavqoQA33kp4IYxUMFpbvgqB7bIaZP4b4OzvjjQ8zU%2FSSr7kWxoH6GGvDeVaLjBxEZdjaRDLUAjsHyG%2FlRL1Rh8r3fc4yewVSPgx89jn5XJ&X-Amz-Signature=1ced2267a02016bda6ca2c9ae68e841809a29beba474446ea79aea969baf23a5&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/5a788f09-7e31-81eb-a3dc-00039a1662d6/31fef9ca-ed83-49a6-bbe4-d4cbdd35dd2d/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466SZV3YMLC%2F20260406%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260406T214430Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEA0aCXVzLXdlc3QtMiJIMEYCIQDt5k4aWZ0IbEmL%2B76Hg3TsxG2RMc8%2B5K1It11XLHC7tgIhANdpSienN%2FWvYZpJnUbVd0LVe6mr5KtDD9XiYFBbB8JGKogECNb%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1Igy6MkPndrvUjbIWwQAq3APKwi606kM%2BMVPjdG1EqDPO9MjU4MzGlCEhCWY0CtSPF%2FjVtZEdZGmMib90vnpQPTpCAoTq40iHq87u1iPS1sDu8lLfZ6NdlO%2FGMMhHTkKeskv77zSyO7mHJeqRwaeoRwb0mlVTX1zHuJNroj9Idv6yS%2FJzJiv9PTArU65ECQri1L2gHqHUcQIbhXUQ8IW4a92CplSHTT8qKSCgxWptX24uKKWR4HZaLsr3NgKyIkyFv56QotenKvU92wvnRYbnkXIm8LDT7cjkEr8kwfH0hh8PHn1h986T93FmDNwFRWbis7oWdTEOfigWQUwO7N1YWSuCjVye0EzHXIeEr1Oy31fivlf20cOEZL0ENAs6mxwuAFwhzHlenqIS9o9ubAIj5nJixruRQn%2F2e094SY%2BpSXNWHTlMvGf4MItbXJZo3NOlUDauChHui1QZp2ejd8R%2F9JUIBHYVOTWTrzR4Y3SstlOLrUpKu41TyMnGcS95s0GR0Pv%2BNU2t1B0htFpmItqJqvr96EkvcritCJM8Hveus26cQS9XZY%2FhV8NraBdiM8nJnX7bDKDZtdJAmDBGYVc2wVueq4eB1IWtOFLV8vUs10oSOvCJ3aWSOT%2B3T4TKEhdH61PlXC5TqH%2FGKKd%2FMDCaxNDOBjqkAXCZlZmrM88ODHKEplOHpCnTgYbj1si4JC%2Bn9ulRUuCC506c75dHMui4AG8xfZ4PA3h%2BCxFivtK%2BZZ91P1sdYhV4gLoUEtTYrwB5SclsSUXs1O%2BPEcGdVKfcDQvHjSCTZDcpsj0Q7GtMR9atT%2BdGXcaqaIB2xwP2slzzlVsQ4C3rb0By5hymERtgleCIkqaY856k%2BFlZUXRu%2FW5w47%2FvpJVhUyc6&X-Amz-Signature=fb803c28e03f5953346e417614840f6fc148cac716731e3a8d8738bab2b6fc85&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/5a788f09-7e31-81eb-a3dc-00039a1662d6/72bc3434-4b45-421d-92fc-7835228efeff/Willow-Glen.webp?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4664TUWQHPS%2F20260406%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260406T214424Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEA0aCXVzLXdlc3QtMiJGMEQCIHhbRO0Xo5bi5cSFrUE9895wVySC3oHu8kXDX%2FVURLLtAiAS5hvsSQE9Um0S0WTvAsXHslebr%2BPb1e3FefvtUgbcCSqIBAjW%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMQga8vsmP7lU%2BHah9KtwDKYeNh1OIfFyIeXOUqYzyCbXvHY7HaCJHw8FMHcvesPDdVlPeM2mo9Ayyf7%2B5QEXSBxvF%2BGepm8IRRAVPrZJbZ37TKBSXIWV4aJohmcLUO6NKmPyizQei8PiEMbxLNBxfCelYkw4WzAyqY%2BwK4MgrFqTmJyo%2B9kGbe3cj5LK7MTARU%2B%2FR5yZHQXwqI%2BFrXvYuv1RGlAKteFUNbnUNxX6Hv9CLtRcyeOS5HPUTNAxBagvDChGL%2BG54wpH1SdfRxfc4uaqi3r0RzeoPb0310zAnBWR2cT4XrVOE0keNtoBV7VANtK%2B8D39GXiyJ12WiWCl66lOEpVfevn52v%2FCJvRG9BIeRiknhlJ3kc8gx753%2BQcvlNHSoidt%2BslJDzlfTOCnFoc6PPWW1fW0yTMdSDgm%2BCU3g8BRxI9Lrj%2F3jp7NeZCIOhRLRDSG04IUYoGU%2FWVXhx7Ow18LsQ53hkPE5LAm7DKiIYFTv%2FUY3rGno8wUTOElVJ1uIuPG3C6x%2B%2B2nlSC3hqGRc4HICwUb27WKjklYCI8yMYJTSw%2FgFxzNSp5ji0t47VNSpPSDLjjPV0l7%2Fcd1uxeRciChhYjRAuJ6fuGcaQhiXro6d2NIyZHDdZMkeK5sX%2F8gJ%2BTwnKfZZ%2FCUwncTQzgY6pgEpMV5iukza7%2BxZWVWBJC%2BCM5FyBj6IkadzUpwe6sn%2Bs4gE7wwoEa6LPP0sF4nrodUOmzIkzL0bgRx1NA1Dj0iRFv4kR6o1iZXa1%2BuFrTarurjtT0XwDZrUBjTZjIH4WW9pHTFm0F%2FIgbmuKmM0pc%2FAEcbWAOmESpQABw%2FqMxx4fQC2jqWyTv%2FzymOmjCRG3IWnM%2ByEMPYq68vsJafUQHFeUAeKKZ80&X-Amz-Signature=a4ea2aef4dca7d2ab1c03e8e8ad23a83bb29e75231277c05edff4eadfc4e802c&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
*[Child: General / Branding]*
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/5a788f09-7e31-81eb-a3dc-00039a1662d6/4cfdff54-c0af-4fb0-b71d-a8a90c2bf974/cpu_vs_gpu.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466ZTWGJJNP%2F20260406%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260406T214430Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEA4aCXVzLXdlc3QtMiJHMEUCICzfbF7v58v0U3GE7FA3LuK0cO9ApKqSU5HjWJtg8vIrAiEA1kVbU%2BaON%2BIdAKzT%2BuhCGbReVIcCEDQdVL1GiKXaf1MqiAQI1%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDFkDu6RXlGQXQPBRCCrcA%2BUYt%2BQOy9%2Fz1ZBW6W9Y22YELf%2FWG7ka4r1PXzjcpbxWhizahQwBIWA%2BWeeaJ7YZD9itPL8FYyZca4fNtIGOI2I0IyOOi18KUnzxjTIEY4Hao4m6%2BY9G7iRTQSzwt%2Bt5qHj2P0WCTM2KWel%2BnaEzpgEwcBF3m7qZoffPSohjoWRrRZO6Tzo5Rs0uWb7OQKR7PDVPsX7KaF5Gwyw%2B%2BvIb72Zmco4CzNZD%2FDC29MZ3%2BIGdznjFRm1DTo6leewHnr9e2JzzIBzcRAYqJ%2BIA75vZI1TLXZ86bt%2F2dmg8Rn0KnyTRFFFPCTqzhmE1Xf6Rrihjfs8eykvjEl9OnYOPpCmhT84JVwDjHSCwP795IntZCa2hNJKIMBSoxEk3JtYPLKrh6qI7biP5TOcTAVBYsRqd%2FvRyXtYTUieoZm6FtKEmMtBR53e7hb0SDHd%2FCy7v5NbWVUZEHl4Fx7LfGM95HU2Q9kml2QdGWcMHtpVwjyTF904BDA2rRAUGp%2BFiDgaRmzEZN5KYRi%2FpSCZPQ%2FJvMSKVPr%2F0Ch2gAMHLNJQiw5SLnIhnDxTvXtA3CXamjrGynjpewQFmVN6JLe80PBnzFcH72uYn%2FEm315WZ5UZjBQTJ35dZXjXDGyDWYb1VNRLdMP3L0M4GOqUBahn%2Foi3G8VrsifKjK2wqRtojAiZKMto3BDORsVdy8L%2FJaWxO%2FkUsQ%2FxlmRrxGyTSje6sspMIix09d5t1UUbyr4iKBa9Lcz%2FEbTqWJWbKM31XHi2jWWuYUQ%2FHPViD7kgrH4giacSrXivGEKx%2BIGl0M3aN0IHUvRXKh7folf0Ks4w1uQuccudJGo5BzzmxfrST1kLYdGH27nNUaulSYIyGX0MA1n3R&X-Amz-Signature=7a9d77107fb4ffd736ad85cdb6ae70ceba06830df445db15aedf95e66444b60b&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/5a788f09-7e31-81eb-a3dc-00039a1662d6/b3fdaf65-7a57-4f89-ad30-a544ce98d3d1/ROV.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466ZTWGJJNP%2F20260406%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260406T214430Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEA4aCXVzLXdlc3QtMiJHMEUCICzfbF7v58v0U3GE7FA3LuK0cO9ApKqSU5HjWJtg8vIrAiEA1kVbU%2BaON%2BIdAKzT%2BuhCGbReVIcCEDQdVL1GiKXaf1MqiAQI1%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDFkDu6RXlGQXQPBRCCrcA%2BUYt%2BQOy9%2Fz1ZBW6W9Y22YELf%2FWG7ka4r1PXzjcpbxWhizahQwBIWA%2BWeeaJ7YZD9itPL8FYyZca4fNtIGOI2I0IyOOi18KUnzxjTIEY4Hao4m6%2BY9G7iRTQSzwt%2Bt5qHj2P0WCTM2KWel%2BnaEzpgEwcBF3m7qZoffPSohjoWRrRZO6Tzo5Rs0uWb7OQKR7PDVPsX7KaF5Gwyw%2B%2BvIb72Zmco4CzNZD%2FDC29MZ3%2BIGdznjFRm1DTo6leewHnr9e2JzzIBzcRAYqJ%2BIA75vZI1TLXZ86bt%2F2dmg8Rn0KnyTRFFFPCTqzhmE1Xf6Rrihjfs8eykvjEl9OnYOPpCmhT84JVwDjHSCwP795IntZCa2hNJKIMBSoxEk3JtYPLKrh6qI7biP5TOcTAVBYsRqd%2FvRyXtYTUieoZm6FtKEmMtBR53e7hb0SDHd%2FCy7v5NbWVUZEHl4Fx7LfGM95HU2Q9kml2QdGWcMHtpVwjyTF904BDA2rRAUGp%2BFiDgaRmzEZN5KYRi%2FpSCZPQ%2FJvMSKVPr%2F0Ch2gAMHLNJQiw5SLnIhnDxTvXtA3CXamjrGynjpewQFmVN6JLe80PBnzFcH72uYn%2FEm315WZ5UZjBQTJ35dZXjXDGyDWYb1VNRLdMP3L0M4GOqUBahn%2Foi3G8VrsifKjK2wqRtojAiZKMto3BDORsVdy8L%2FJaWxO%2FkUsQ%2FxlmRrxGyTSje6sspMIix09d5t1UUbyr4iKBa9Lcz%2FEbTqWJWbKM31XHi2jWWuYUQ%2FHPViD7kgrH4giacSrXivGEKx%2BIGl0M3aN0IHUvRXKh7folf0Ks4w1uQuccudJGo5BzzmxfrST1kLYdGH27nNUaulSYIyGX0MA1n3R&X-Amz-Signature=d151e0ac8b8a8df8a2666227393c224f60f23696677978ddda142665e922eafe&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/5a788f09-7e31-81eb-a3dc-00039a1662d6/e336a97e-fefc-43e1-bdb9-4a40bc75f825/winnig.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466ZTWGJJNP%2F20260406%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260406T214430Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEA4aCXVzLXdlc3QtMiJHMEUCICzfbF7v58v0U3GE7FA3LuK0cO9ApKqSU5HjWJtg8vIrAiEA1kVbU%2BaON%2BIdAKzT%2BuhCGbReVIcCEDQdVL1GiKXaf1MqiAQI1%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDFkDu6RXlGQXQPBRCCrcA%2BUYt%2BQOy9%2Fz1ZBW6W9Y22YELf%2FWG7ka4r1PXzjcpbxWhizahQwBIWA%2BWeeaJ7YZD9itPL8FYyZca4fNtIGOI2I0IyOOi18KUnzxjTIEY4Hao4m6%2BY9G7iRTQSzwt%2Bt5qHj2P0WCTM2KWel%2BnaEzpgEwcBF3m7qZoffPSohjoWRrRZO6Tzo5Rs0uWb7OQKR7PDVPsX7KaF5Gwyw%2B%2BvIb72Zmco4CzNZD%2FDC29MZ3%2BIGdznjFRm1DTo6leewHnr9e2JzzIBzcRAYqJ%2BIA75vZI1TLXZ86bt%2F2dmg8Rn0KnyTRFFFPCTqzhmE1Xf6Rrihjfs8eykvjEl9OnYOPpCmhT84JVwDjHSCwP795IntZCa2hNJKIMBSoxEk3JtYPLKrh6qI7biP5TOcTAVBYsRqd%2FvRyXtYTUieoZm6FtKEmMtBR53e7hb0SDHd%2FCy7v5NbWVUZEHl4Fx7LfGM95HU2Q9kml2QdGWcMHtpVwjyTF904BDA2rRAUGp%2BFiDgaRmzEZN5KYRi%2FpSCZPQ%2FJvMSKVPr%2F0Ch2gAMHLNJQiw5SLnIhnDxTvXtA3CXamjrGynjpewQFmVN6JLe80PBnzFcH72uYn%2FEm315WZ5UZjBQTJ35dZXjXDGyDWYb1VNRLdMP3L0M4GOqUBahn%2Foi3G8VrsifKjK2wqRtojAiZKMto3BDORsVdy8L%2FJaWxO%2FkUsQ%2FxlmRrxGyTSje6sspMIix09d5t1UUbyr4iKBa9Lcz%2FEbTqWJWbKM31XHi2jWWuYUQ%2FHPViD7kgrH4giacSrXivGEKx%2BIGl0M3aN0IHUvRXKh7folf0Ks4w1uQuccudJGo5BzzmxfrST1kLYdGH27nNUaulSYIyGX0MA1n3R&X-Amz-Signature=baf26d41c59301ae7b7a69dbf13d655160d6a5535cac9b52c55c93bcf86b8619&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/5a788f09-7e31-81eb-a3dc-00039a1662d6/f96db7a6-3b7b-43cb-9ef5-1087236e8e81/DLS.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466ZTWGJJNP%2F20260406%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260406T214430Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEA4aCXVzLXdlc3QtMiJHMEUCICzfbF7v58v0U3GE7FA3LuK0cO9ApKqSU5HjWJtg8vIrAiEA1kVbU%2BaON%2BIdAKzT%2BuhCGbReVIcCEDQdVL1GiKXaf1MqiAQI1%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDFkDu6RXlGQXQPBRCCrcA%2BUYt%2BQOy9%2Fz1ZBW6W9Y22YELf%2FWG7ka4r1PXzjcpbxWhizahQwBIWA%2BWeeaJ7YZD9itPL8FYyZca4fNtIGOI2I0IyOOi18KUnzxjTIEY4Hao4m6%2BY9G7iRTQSzwt%2Bt5qHj2P0WCTM2KWel%2BnaEzpgEwcBF3m7qZoffPSohjoWRrRZO6Tzo5Rs0uWb7OQKR7PDVPsX7KaF5Gwyw%2B%2BvIb72Zmco4CzNZD%2FDC29MZ3%2BIGdznjFRm1DTo6leewHnr9e2JzzIBzcRAYqJ%2BIA75vZI1TLXZ86bt%2F2dmg8Rn0KnyTRFFFPCTqzhmE1Xf6Rrihjfs8eykvjEl9OnYOPpCmhT84JVwDjHSCwP795IntZCa2hNJKIMBSoxEk3JtYPLKrh6qI7biP5TOcTAVBYsRqd%2FvRyXtYTUieoZm6FtKEmMtBR53e7hb0SDHd%2FCy7v5NbWVUZEHl4Fx7LfGM95HU2Q9kml2QdGWcMHtpVwjyTF904BDA2rRAUGp%2BFiDgaRmzEZN5KYRi%2FpSCZPQ%2FJvMSKVPr%2F0Ch2gAMHLNJQiw5SLnIhnDxTvXtA3CXamjrGynjpewQFmVN6JLe80PBnzFcH72uYn%2FEm315WZ5UZjBQTJ35dZXjXDGyDWYb1VNRLdMP3L0M4GOqUBahn%2Foi3G8VrsifKjK2wqRtojAiZKMto3BDORsVdy8L%2FJaWxO%2FkUsQ%2FxlmRrxGyTSje6sspMIix09d5t1UUbyr4iKBa9Lcz%2FEbTqWJWbKM31XHi2jWWuYUQ%2FHPViD7kgrH4giacSrXivGEKx%2BIGl0M3aN0IHUvRXKh7folf0Ks4w1uQuccudJGo5BzzmxfrST1kLYdGH27nNUaulSYIyGX0MA1n3R&X-Amz-Signature=dc44470e3cdc3e6aa4d92ab5368423dfde1e189b3f84ebc30c75007a8d7cb675&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/5a788f09-7e31-81eb-a3dc-00039a1662d6/cd40a625-575b-45b3-b76d-39981b749bed/oil_filled.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466ZTWGJJNP%2F20260406%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260406T214430Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEA4aCXVzLXdlc3QtMiJHMEUCICzfbF7v58v0U3GE7FA3LuK0cO9ApKqSU5HjWJtg8vIrAiEA1kVbU%2BaON%2BIdAKzT%2BuhCGbReVIcCEDQdVL1GiKXaf1MqiAQI1%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDFkDu6RXlGQXQPBRCCrcA%2BUYt%2BQOy9%2Fz1ZBW6W9Y22YELf%2FWG7ka4r1PXzjcpbxWhizahQwBIWA%2BWeeaJ7YZD9itPL8FYyZca4fNtIGOI2I0IyOOi18KUnzxjTIEY4Hao4m6%2BY9G7iRTQSzwt%2Bt5qHj2P0WCTM2KWel%2BnaEzpgEwcBF3m7qZoffPSohjoWRrRZO6Tzo5Rs0uWb7OQKR7PDVPsX7KaF5Gwyw%2B%2BvIb72Zmco4CzNZD%2FDC29MZ3%2BIGdznjFRm1DTo6leewHnr9e2JzzIBzcRAYqJ%2BIA75vZI1TLXZ86bt%2F2dmg8Rn0KnyTRFFFPCTqzhmE1Xf6Rrihjfs8eykvjEl9OnYOPpCmhT84JVwDjHSCwP795IntZCa2hNJKIMBSoxEk3JtYPLKrh6qI7biP5TOcTAVBYsRqd%2FvRyXtYTUieoZm6FtKEmMtBR53e7hb0SDHd%2FCy7v5NbWVUZEHl4Fx7LfGM95HU2Q9kml2QdGWcMHtpVwjyTF904BDA2rRAUGp%2BFiDgaRmzEZN5KYRi%2FpSCZPQ%2FJvMSKVPr%2F0Ch2gAMHLNJQiw5SLnIhnDxTvXtA3CXamjrGynjpewQFmVN6JLe80PBnzFcH72uYn%2FEm315WZ5UZjBQTJ35dZXjXDGyDWYb1VNRLdMP3L0M4GOqUBahn%2Foi3G8VrsifKjK2wqRtojAiZKMto3BDORsVdy8L%2FJaWxO%2FkUsQ%2FxlmRrxGyTSje6sspMIix09d5t1UUbyr4iKBa9Lcz%2FEbTqWJWbKM31XHi2jWWuYUQ%2FHPViD7kgrH4giacSrXivGEKx%2BIGl0M3aN0IHUvRXKh7folf0Ks4w1uQuccudJGo5BzzmxfrST1kLYdGH27nNUaulSYIyGX0MA1n3R&X-Amz-Signature=8736980fbbb0771c8d70d914139eff60b27973c2bf50051e536dd72c8850ca82&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/5a788f09-7e31-81eb-a3dc-00039a1662d6/7af60f6d-b513-46fd-9b97-6cbd1e3ae40f/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466ZTWGJJNP%2F20260406%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260406T214430Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEA4aCXVzLXdlc3QtMiJHMEUCICzfbF7v58v0U3GE7FA3LuK0cO9ApKqSU5HjWJtg8vIrAiEA1kVbU%2BaON%2BIdAKzT%2BuhCGbReVIcCEDQdVL1GiKXaf1MqiAQI1%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDFkDu6RXlGQXQPBRCCrcA%2BUYt%2BQOy9%2Fz1ZBW6W9Y22YELf%2FWG7ka4r1PXzjcpbxWhizahQwBIWA%2BWeeaJ7YZD9itPL8FYyZca4fNtIGOI2I0IyOOi18KUnzxjTIEY4Hao4m6%2BY9G7iRTQSzwt%2Bt5qHj2P0WCTM2KWel%2BnaEzpgEwcBF3m7qZoffPSohjoWRrRZO6Tzo5Rs0uWb7OQKR7PDVPsX7KaF5Gwyw%2B%2BvIb72Zmco4CzNZD%2FDC29MZ3%2BIGdznjFRm1DTo6leewHnr9e2JzzIBzcRAYqJ%2BIA75vZI1TLXZ86bt%2F2dmg8Rn0KnyTRFFFPCTqzhmE1Xf6Rrihjfs8eykvjEl9OnYOPpCmhT84JVwDjHSCwP795IntZCa2hNJKIMBSoxEk3JtYPLKrh6qI7biP5TOcTAVBYsRqd%2FvRyXtYTUieoZm6FtKEmMtBR53e7hb0SDHd%2FCy7v5NbWVUZEHl4Fx7LfGM95HU2Q9kml2QdGWcMHtpVwjyTF904BDA2rRAUGp%2BFiDgaRmzEZN5KYRi%2FpSCZPQ%2FJvMSKVPr%2F0Ch2gAMHLNJQiw5SLnIhnDxTvXtA3CXamjrGynjpewQFmVN6JLe80PBnzFcH72uYn%2FEm315WZ5UZjBQTJ35dZXjXDGyDWYb1VNRLdMP3L0M4GOqUBahn%2Foi3G8VrsifKjK2wqRtojAiZKMto3BDORsVdy8L%2FJaWxO%2FkUsQ%2FxlmRrxGyTSje6sspMIix09d5t1UUbyr4iKBa9Lcz%2FEbTqWJWbKM31XHi2jWWuYUQ%2FHPViD7kgrH4giacSrXivGEKx%2BIGl0M3aN0IHUvRXKh7folf0Ks4w1uQuccudJGo5BzzmxfrST1kLYdGH27nNUaulSYIyGX0MA1n3R&X-Amz-Signature=ded0d0b2980f09996f76136b5d6609346332ae867a7d477eb87810795a7b913e&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
*[Child: NVIDIA Certifications]*
> NCA-AIIO course materials (Units 1-14) and certification documents. Exam: 2026-03-13.
## NCA-AIIO — AI Infrastructure and Operations
50 questions, 60 minutes, 3 domains:
D1: Essential AI Knowledge (38%) — Units 1-5
D2: AI Infrastructure (40%) — Units 6-10
D3: AI Operations (22%) — Units 11-14
---
### Course Materials (Units 1-14)
PDFs are currently in General/Branding — drag them here in Notion to organize.

Unit 01 — AI Transformation Across Industries
Unit 02 — Introduction to Artificial Intelligence
Unit 03 — Generative AI and Beyond
Unit 04 — Accelerating AI with GPUs
Unit 05 — AI Software Ecosystem
Unit 06 — Data Center and Cloud Computing
Unit 07 — Compute Platforms for AI
Unit 08 — Networking for AI
Unit 09 — Storage for AI
Unit 10 — Energy Efficient Computing
Unit 11 — Reference Architectures
Unit 12 — AI in the Cloud
Unit 13 — Provisioning, Monitoring and Management
Unit 14 — Orchestration and Job Scheduling
---
### Other NVIDIA Certifications
Add future certs here as you earn them (DGX-Ready, Omniverse, etc.)
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/5a788f09-7e31-81eb-a3dc-00039a1662d6/88e4fb61-41a4-4dc7-b3d3-0eea214fad79/A.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466QYP7VYCP%2F20260406%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260406T214431Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEA0aCXVzLXdlc3QtMiJHMEUCIQCxcNNb10fgzZP5AGsgk26HCV2ABfZY1CZ9hXc9fswC0gIgNz5CxaGlHzRAyFWfBEQKB%2BU%2BawLnV7aj9ajsXZxxcS4qiAQI1v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDCxWBagVQGvVn3Dr%2BSrcA08nAsT3mUUvE6KLWTO2noCVtptud1pnnbmyCQ7r1KAslmuqaYo2f2ueOXxEcewK83LHw8GKPMfmJT%2BtHGh8Qul6Uoa8HXK6%2FMvsSOHLz1B%2F9gtZrY%2FuFf0YTGt7FD%2Fnl3cce7vATG53WHUevO%2BG6obGndMaCAVsekL0AT74Zi%2B0cN40eKTBVI7W6BL%2BtXy1DiiIolJAvtUdFOZowMiHINhzQoI0Vy3AxTfHkHQ%2FWZeFrFoYxEDx40OdWrtEBb3ZKxxhtocTsnFWNSnlqcvjgULmp6ot%2Fo573FlnaYLoc%2BQYZzNH8Y9ODztqRq5XwpjPMmcIcZxnp2xsz1sb85QSGhIa7266Xdtfry08FlK0tJqUbc3T5xVaCA6tamkU98CEIdIUU%2FIjOkVUIFrkLDTZ5meGu6Qdk6tkgRq%2BX5HeCrInd3q4Ik2wfVKo9WtxXYq8KugRlGFt1VNOXy8fkucE1gpSatn7t94XA2grGtPnA838nN8mnkGi6dp05RA19qxyGBBgi8Idqo%2BzcRvDaQUWS6HFL%2FdLNhrneQl%2FRqeFeoBNxFRXDmcJ7mKLAdjZrzGW83mUwaru6qpTLNtX5J2ppURBRkDppBhcQ6JkxppBxXk%2FWGuM5oOsHND%2FZwkVMKTE0M4GOqUB%2F86h1EIE71llzj5fTNoN3I6OEa5YmnbVpZdxr75TAcsA1UeHJ%2FNuAWPNy%2B%2F0QEfI3PwFh%2F%2B%2FB7KRWx4JyphQXvrRh59Yn2Wfe%2BHkOc9eMIUWm%2FiMtpSmDq2JbARZd5e64ANabb43pzDh5u41OrkKso641DjzQUcuvDC8j6qX1mdzTBietPA39caQPx2EebSeAD0Pms%2Fgw1zFa83pTiSd0FshzCc1&X-Amz-Signature=393d2826dfdd34a1de00e5edb9ca11d94fa7b01b31b14c53f37e2a90a3f1c48f&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/5a788f09-7e31-81eb-a3dc-00039a1662d6/2967dedf-a965-41ca-8e03-a7c4a45dc7e7/Electronics_cert.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466QYP7VYCP%2F20260406%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260406T214431Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEA0aCXVzLXdlc3QtMiJHMEUCIQCxcNNb10fgzZP5AGsgk26HCV2ABfZY1CZ9hXc9fswC0gIgNz5CxaGlHzRAyFWfBEQKB%2BU%2BawLnV7aj9ajsXZxxcS4qiAQI1v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDCxWBagVQGvVn3Dr%2BSrcA08nAsT3mUUvE6KLWTO2noCVtptud1pnnbmyCQ7r1KAslmuqaYo2f2ueOXxEcewK83LHw8GKPMfmJT%2BtHGh8Qul6Uoa8HXK6%2FMvsSOHLz1B%2F9gtZrY%2FuFf0YTGt7FD%2Fnl3cce7vATG53WHUevO%2BG6obGndMaCAVsekL0AT74Zi%2B0cN40eKTBVI7W6BL%2BtXy1DiiIolJAvtUdFOZowMiHINhzQoI0Vy3AxTfHkHQ%2FWZeFrFoYxEDx40OdWrtEBb3ZKxxhtocTsnFWNSnlqcvjgULmp6ot%2Fo573FlnaYLoc%2BQYZzNH8Y9ODztqRq5XwpjPMmcIcZxnp2xsz1sb85QSGhIa7266Xdtfry08FlK0tJqUbc3T5xVaCA6tamkU98CEIdIUU%2FIjOkVUIFrkLDTZ5meGu6Qdk6tkgRq%2BX5HeCrInd3q4Ik2wfVKo9WtxXYq8KugRlGFt1VNOXy8fkucE1gpSatn7t94XA2grGtPnA838nN8mnkGi6dp05RA19qxyGBBgi8Idqo%2BzcRvDaQUWS6HFL%2FdLNhrneQl%2FRqeFeoBNxFRXDmcJ7mKLAdjZrzGW83mUwaru6qpTLNtX5J2ppURBRkDppBhcQ6JkxppBxXk%2FWGuM5oOsHND%2FZwkVMKTE0M4GOqUB%2F86h1EIE71llzj5fTNoN3I6OEa5YmnbVpZdxr75TAcsA1UeHJ%2FNuAWPNy%2B%2F0QEfI3PwFh%2F%2B%2FB7KRWx4JyphQXvrRh59Yn2Wfe%2BHkOc9eMIUWm%2FiMtpSmDq2JbARZd5e64ANabb43pzDh5u41OrkKso641DjzQUcuvDC8j6qX1mdzTBietPA39caQPx2EebSeAD0Pms%2Fgw1zFa83pTiSd0FshzCc1&X-Amz-Signature=47c574517f50e472946a88bb6eccd06334c77ab01d097607526904d2d6325855&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/5a788f09-7e31-81eb-a3dc-00039a1662d6/f224fff2-cf47-428b-8487-9593bf4d600a/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466QYP7VYCP%2F20260406%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260406T214431Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEA0aCXVzLXdlc3QtMiJHMEUCIQCxcNNb10fgzZP5AGsgk26HCV2ABfZY1CZ9hXc9fswC0gIgNz5CxaGlHzRAyFWfBEQKB%2BU%2BawLnV7aj9ajsXZxxcS4qiAQI1v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDCxWBagVQGvVn3Dr%2BSrcA08nAsT3mUUvE6KLWTO2noCVtptud1pnnbmyCQ7r1KAslmuqaYo2f2ueOXxEcewK83LHw8GKPMfmJT%2BtHGh8Qul6Uoa8HXK6%2FMvsSOHLz1B%2F9gtZrY%2FuFf0YTGt7FD%2Fnl3cce7vATG53WHUevO%2BG6obGndMaCAVsekL0AT74Zi%2B0cN40eKTBVI7W6BL%2BtXy1DiiIolJAvtUdFOZowMiHINhzQoI0Vy3AxTfHkHQ%2FWZeFrFoYxEDx40OdWrtEBb3ZKxxhtocTsnFWNSnlqcvjgULmp6ot%2Fo573FlnaYLoc%2BQYZzNH8Y9ODztqRq5XwpjPMmcIcZxnp2xsz1sb85QSGhIa7266Xdtfry08FlK0tJqUbc3T5xVaCA6tamkU98CEIdIUU%2FIjOkVUIFrkLDTZ5meGu6Qdk6tkgRq%2BX5HeCrInd3q4Ik2wfVKo9WtxXYq8KugRlGFt1VNOXy8fkucE1gpSatn7t94XA2grGtPnA838nN8mnkGi6dp05RA19qxyGBBgi8Idqo%2BzcRvDaQUWS6HFL%2FdLNhrneQl%2FRqeFeoBNxFRXDmcJ7mKLAdjZrzGW83mUwaru6qpTLNtX5J2ppURBRkDppBhcQ6JkxppBxXk%2FWGuM5oOsHND%2FZwkVMKTE0M4GOqUB%2F86h1EIE71llzj5fTNoN3I6OEa5YmnbVpZdxr75TAcsA1UeHJ%2FNuAWPNy%2B%2F0QEfI3PwFh%2F%2B%2FB7KRWx4JyphQXvrRh59Yn2Wfe%2BHkOc9eMIUWm%2FiMtpSmDq2JbARZd5e64ANabb43pzDh5u41OrkKso641DjzQUcuvDC8j6qX1mdzTBietPA39caQPx2EebSeAD0Pms%2Fgw1zFa83pTiSd0FshzCc1&X-Amz-Signature=e4fe6a3de977dcdba76fce1e0d5c0f5324951a5369a185375a90e1f5c1cc5698&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)
*[Child: Willow Glen / Tiger AI Factory]*
> Willow Glen Terminal — former 2,200 MW Entergy station, St. Gabriel, LA. ADC x LSU Tiger AI Factory. Upload aerial photos, site shots, infrastructure images here.
Current images: wgt-aerial.jpg (helicopter aerial). Need: drone shots, warehouse, substation, tank farm, dock, river frontage, surrounding area.
*[Child: Trappeys Cannery]*
> Trappeys Cannery — 112,500 sq ft solar AI factory, Lafayette, LA. 56 site photos in repo at adc3k-deploy/trappeys-photos/. Numbered gallery at adc3k.com/trappeys-gallery
Photo categories: Front/Bank (5), Riverfront Interior (7), Middle Low (4), Middle High (4), Middle Other (4), Rear Warehouse (6), Water Tower (4), Power (2), Electrical Grid (4), ATMOS Gas (1), Historic (14)
---
> ⚠️ UPDATED 2026-03-23
## Current Asset Inventory (also in git repo adc3k-deploy/)
### Willow Glen / Tiger AI Factory
  - 8 helicopter/satellite photos (willow-glen-*.jpg)
  - 8 renders (renders/wg-*.jpg) — 4 Kontext + 4 Schnell
  - 6 blueprint SVGs (blueprints/*.svg)
### Trappeys Cannery
  - 56 numbered photos (trappeys-photos/)
  - 5 restoration renders (renders/trappeys-*.jpg) — Kontext
  - 6 blueprint SVGs (blueprints/trappeys-*.svg)
### MARLIE I
  - 6 blueprint SVGs (blueprints/marlie-*.svg)
  - No photos yet (need site visit)
### KLFT / SkyCommand
  - 5 concept renders (renders/klft-*.jpg) — Schnell
  - 7 geometric renders (renders/klft_*.png) — pyrender from USD
  - USD scene file (klft-digital-twin.usda)
  - No real airport photos yet (need to capture)
### ADC 3K Pods
  - Check Notion for any existing pod renders/photos
### General / Branding
  - Check Notion for logos, brand assets
### NVIDIA Certifications
  - Check Notion for cert screenshots
### Henry Hub & Power
  - Check Notion for power infrastructure images
Note: Primary image storage is now in the git repo (adc3k-deploy/renders/ and adc3k-deploy/). Notion Site Assets is for original source images and brand assets.
*[Child: ADC Manufacturing -- Pod Factory Strategy]*
# ADC Manufacturing -- Two-Step Strategy
Step 1: Bootstrap factory in existing building. Get pods built, get revenue flowing, learn what to automate. Step 2: Purpose-built automated factory with robots, solar roof, pipeline gas, and NVIDIA Omniverse digital twin. Step 1 funds Step 2.
---
## The Logic
```plain text
STEP 1: BATON ROUGE TERMINAL (LAFAYETTE)
  Lease existing building. Manual assembly. 6 stations.
  Output: 2-3 pods/month. Staff: 8-12.
  Timeline: 60-90 days to first pod.
  Revenue: $450K/month at capacity.
  PURPOSE: Cash flow + learn what to automate.

STEP 2: NEW IBERIA AUTOMATED FACTORY (14th & Hwy 90)
  Purpose-built. Robotic assembly. Solar roof. Pipeline gas.
  Output: 8-12 pods/month. Staff: 15-20.
  Timeline: 12-18 months to production.
  Revenue: $1.5M/month at capacity.
  PURPOSE: Scale + margins + the machine that builds the machine.

Step 1 revenue funds Step 2 construction.
Step 1 lessons optimize Step 2 automation.
Every pod built by hand teaches you what to automate.
```
---
## NVIDIA Technology Stack
```plain text
FACTORY DESIGN        Omniverse      Build the factory virtually first
ROBOT PROGRAMMING     Isaac Sim      Train arms in simulation
QUALITY INSPECTION    Metropolis     AI vision for automated QA
FACTORY OPERATIONS    AI Enterprise  Real-time optimization
POD HARDWARE          DGX / HGX      What goes inside every pod
```
> The factory that builds NVIDIA-powered pods is itself powered by NVIDIA technology. That's the story.
*[Child: Step 1: Baton Rouge Terminal -- Bootstrap Factory]*
# Step 1: Baton Rouge Terminal -- Bootstrap Factory
> Get pods built. Get revenue flowing. Learn what to automate. This is NOT the final factory -- it's the launchpad.
---
## Site: Baton Rouge Terminal, Lafayette
Existing industrial building. Lease, don't buy. The goal is speed -- pods shipping in 60-90 days, not 18 months waiting for a custom factory.
### Facility Requirements
    - 10,000-20,000 sq ft clear span (no interior columns)
    - Overhead crane -- 10-ton minimum for lifting containers and loaded racks
    - 3-phase power for welding, test benches, and UPS commissioning
    - Loading dock for flatbed truck access (pods ship on flatbeds)
    - Concrete floor rated for container weight (~40,000 lbs loaded)
    - Ventilation for welding and spray foam insulation
---
## Assembly Line -- 6 Stations
Containers flow left to right through 6 stations. Each station takes 2-3 days. Total build time per pod: 12-18 working days.
```plain text
ASSEMBLY FLOW -- BATON ROUGE TERMINAL

  STATION 1        STATION 2        STATION 3
  Container Prep   Insulation       Electrical
  ┌──────────┐     ┌──────────┐     ┌──────────┐
  │ Receive   │     │ Spray    │     │ Conduit  │
  │ Inspect   │ --> │ foam     │ --> │ Wire pull│
  │ Cut pens  │     │ walls +  │     │ PDUs     │
  │ Doors     │     │ ceiling  │     │ UPS      │
  └──────────┘     └──────────┘     └──────────┘
      2 days           2 days           3 days

  STATION 4        STATION 5        STATION 6
  Cooling          Compute          Test & QA
  ┌──────────┐     ┌──────────┐     ┌──────────┐
  │ Immersion │     │ Racks    │     │ Power on │
  │ tanks     │ --> │ Servers  │ --> │ Thermal  │
  │ CDU       │     │ Cables   │     │ Burn-in  │
  │ Dry cooler│     │ Network  │     │ Ship     │
  └──────────┘     └──────────┘     └──────────┘
      3 days           2 days           3 days

  TOTAL: 12-18 working days per pod
  OUTPUT: 2-3 pods/month with overlapping stations
```
---
## Staffing -- 8-12 People
    - 2 electricians (licensed) -- conduit, wire, terminations, UPS
    - 2 pipe fitters / mechanical -- immersion tanks, CDU plumbing, dry cooler
    - 2 electronics technicians -- server installation, networking, cable management
    - 1 insulation / finish contractor -- spray foam, sealing, penetration waterproofing
    - 1 QA / commissioning engineer -- test protocols, burn-in, documentation
    - 1 operations manager -- scheduling, inventory, shipping
    - 1-2 general assembly -- container prep, crane operation, material handling
---
## Economics
```plain text
STEP 1 ECONOMICS

Startup Costs:
  Lease deposit + first/last       $25-35K
  Station buildout (6 stations)    $100-150K
  Tooling (crane, welders, etc.)   $50-75K
  Initial inventory (1st 3 pods)   $200-300K
  Total startup:                   $375-560K

Monthly Operating:
  Lease                            $8-12K
  Payroll (8-12 people)            $60-90K
  Materials per pod                $40-60K
  Utilities + misc                 $5-8K

Revenue (at capacity, 3 pods/month):
  3 pods x $120-180K each =        $360-540K/month
  Less operating costs:             $195-290K/month
  Gross margin:                     $165-250K/month
```
---
## What Step 1 Teaches You
Every pod you build by hand reveals what to automate. Track these metrics:
    - Time per station -- which station is the bottleneck?
    - Error rate per station -- where do mistakes happen?
    - Rework frequency -- what gets done twice?
    - Material waste -- where are you cutting and throwing away?
    - Worker idle time -- where are people waiting for the previous station?
> This data becomes the blueprint for Step 2 automation. Every manual pain point is a robot opportunity.
---
> UPDATED 2026-03-23 -- POST-GTC REWRITE
### Updated Assembly Line (40-ft containers):
Station 1: Container Prep
    - Receive 40-ft HC ISO container
    - Cut penetrations (power, cooling, cable)
    - Install vapor barrier + insulation (spray foam)
    - Time: 2 days
Station 2: Electrical
    - Install Eaton Beam Rubin DSX (800V DC rectifier + bus)
    - Run 800V DC busway
    - Install rack PDUs (Eaton HDX G4)
    - Generator hookup panel (external)
    - Time: 2 days
Station 3: Cooling
    - Mount exterior dry cooler
    - Run supply/return piping (45C/55C glycol loop)
    - Install CDU connection manifolds for NVL72 rack ports
    - Pressure test
    - Time: 1.5 days
Station 4: Compute Install
    - Receive NVIDIA NVL72 rack (ships complete, liquid cooled)
    - Position on pod floor (forklift)
    - Connect 800V DC power feed
    - Connect liquid cooling manifolds
    - Connect network cables (InfiniBand if multi-rack, Ethernet + management)
    - Time: 1 day
Station 5: Fire + Safety
    - Install Novec 1230 suppression system
    - Install VESDA aspirating detection
    - Leak detection (TraceTek)
    - Environmental sensors (temp, humidity, pressure)
    - Time: 1 day
Station 6: Test + QA
    - Power on, POST, BIOS config
    - Cooling flow test (verify temps under load)
    - Network connectivity to Willow Glen NOC
    - GPU burn-in (24-hr stress test)
    - Mission Control registration (node appears on dashboard)
    - Time: 2 days
---
Total per pod: ~9.5 days
Monthly output: 2-3 pods (with 8-12 staff)
Startup cost: $375-560K (facility lease, tools, initial materials)
### Key Difference from Pre-GTC:
    - NO immersion cooling station -- NVIDIA racks are self-contained liquid cooled
    - NO custom CDU engineering -- just connect manifolds
    - 800V DC simplifies electrical (fewer conversions, less copper)
    - Assembly is simpler because NVIDIA did the hard part
*[Child: Step 2: New Iberia -- AI-Automated Pod Factory]*
# Step 2: New Iberia -- AI-Automated Pod Factory
> The machine that builds the machine. Fully automated, solar-powered, pipeline-fed, designed in Omniverse before a single wall goes up.
---
## Site: 14th Street & Highway 90, New Iberia
### Why This Location
    - Natural gas pipeline ON PROPERTY -- power the factory and test pods with the same fuel
    - Corner of 14th & Hwy 90 -- direct highway access for shipping containers in and pods out
    - Hwy 90 connects to I-10, Port of New Iberia, and the entire Gulf corridor
    - Large footprint -- room for assembly line, solar array, testing yard, expansion
    - Iberia Parish -- eligible for PILOT, Quality Jobs, Enterprise Zone incentives
---
## The Omniverse Digital Twin Workflow
Before spending a dollar on construction, the entire factory is designed and tested virtually in NVIDIA Omniverse. Here is exactly how that works:
### Phase 1: Virtual Design (Weeks 1-8)
Build the entire factory in Omniverse -- every wall, every robot arm, every conveyor belt, every electrical panel, every fire suppression head. Place them exactly where they'll go. The software is physically accurate -- if something doesn't fit in Omniverse, it won't fit in real life.
    - Architect delivers building shell design (steel frame, concrete, solar roof spec)
    - ADC engineering team places all 7 assembly stations inside the virtual building
    - Robot arms are modeled with real reach envelopes and payload limits
    - Material flow is mapped: container in loading dock to pod on flatbed
    - Solar roof layout optimized for maximum generation vs. structural load
### Phase 2: Simulate (Weeks 8-16)
Run the factory at full speed -- virtually. Process 100 pods through the digital assembly line. The simulation reveals every problem before you encounter it in real life.
    - Throughput test: how many pods/month at what robot speed?
    - Collision detection: do any robot paths intersect? Any pinch points?
    - Bottleneck identification: which station holds up the line?
    - Failure simulation: what happens when Robot Arm 3 goes down?
    - Energy simulation: does solar + gas produce enough for factory + pod testing?
### Phase 3: Build Physical Factory (Months 4-12)
The physical factory is a 1:1 copy of the digital model. Every measurement is pre-validated. Every robot position is pre-programmed. No surprises.
    - Steel frame + concrete pad construction
    - Solar roof installation (panels + inverters + battery storage)
    - Gas pipeline tap and distribution manifold
    - Robot arm installation in pre-validated positions
    - Conveyor and material handling systems
    - QA test cells with automated monitoring
### Phase 4: Live Digital Twin (Ongoing)
Once the physical factory is running, the digital twin stays alive. Every sensor in the real factory feeds the virtual model in real-time. The digital twin becomes the factory's brain.
    - Real-time production dashboard (accessible from MARLIE I NOC)
    - Predictive maintenance on every robot arm and motor
    - Production optimization -- AI adjusts station timing automatically
    - Remote monitoring -- Scott can watch the factory from his phone
---
## Automated Assembly Line -- 7 Stations
```plain text
AUTOMATED ASSEMBLY -- NEW IBERIA FACTORY

  [1] RECEIVING       Robotic crane unloads ISO containers from truck
                      Positions on assembly track automatically

  [2] CNC CUTTING     Automated plasma/laser cuts all penetrations
                      Pre-programmed from Omniverse model. Zero measuring.

  [3] INSULATION      Robotic spray foam application
                      Consistent thickness, no gaps, no human error

  [4] ELECTRICAL      Semi-automated wire pulling + robotic conduit bending
                      Human electrician for terminations and inspection

  [5] COOLING         Robotic tank placement + orbital pipe welding
                      Human for final connections and leak testing

  [6] COMPUTE         Robotic rack insertion and cable management
                      AI vision verifies every connection

  [7] TEST CELL       Automated power-on, thermal cycle, 24hr burn-in
                      AI monitors every parameter
                      Pod doesn't leave until 100% automated QA passes
```
---
## Power Architecture -- Factory Runs On What It Sells
```plain text
NEW IBERIA FACTORY POWER

  SOLAR ROOF          Primary daytime power for factory operations
  PIPELINE GAS        Baseload power + pod testing fuel
  BATTERY STORAGE     Overnight + peak shaving
  GRID (CLECO)        Emergency backup only

  The factory is its own showcase:
  'We power our factory the same way we power your pod.'
```
---
## Staffing -- 15-20 People
    - 3-4 robot operators / programmers
    - 2 electricians (final termination, code inspection)
    - 2 mechanical / pipe fitters (final connections, leak testing)
    - 2 QA engineers (automated test oversight, documentation)
    - 2 logistics (shipping, receiving, inventory management)
    - 1 plant manager
    - 2-3 maintenance technicians (robots, conveyors, facility)
    - 1 Omniverse / digital twin engineer
---
## Economics
```plain text
STEP 2 ECONOMICS

Capital Investment:
  Land + construction             $3-5M
  Robot arms + tooling            $1.5-2M
  Solar roof + battery            $500K-800K
  Gas pipeline connection          $100-200K
  Omniverse design + simulation   $150-250K
  Total:                           $5.25-8.25M

Monthly Operating:
  Payroll (15-20 people)           $100-140K
  Materials per pod                $35-50K (bulk pricing)
  Energy (solar offsets 40%)       $8-12K
  Maintenance + misc              $10-15K
  Total operating:                $153-217K/month

Revenue (at capacity, 10 pods/month):
  10 pods x $150K avg =            $1,500,000/month
  Less operating:                  $217K/month
  Less material (10 pods):         $500K/month
  GROSS MARGIN:                    $783K/month
  ANNUAL GROSS PROFIT:             $9.4M/year
```
> Step 1 revenue ($165-250K/month gross margin) accumulates during the 12-18 month Step 2 build period. That's $2-4.5M toward the $5-8M capital investment before the automated factory even opens.
---
## Timeline
```plain text
MONTH 1-3:     Step 1 running. First pods shipping.
MONTH 3-6:     Omniverse design of Step 2 factory begins.
MONTH 6-8:     Simulation testing. Site acquisition in New Iberia.
MONTH 8-10:    Construction begins. Permits, foundation, steel.
MONTH 10-14:   Building enclosed. Robot installation.
MONTH 14-16:   Commissioning. Digital twin goes live.
MONTH 16-18:   First automated pod off the line.
MONTH 18+:     Ramp to 8-12 pods/month. Step 1 becomes
               overflow / custom / defense-spec facility.
```
> Step 1 doesn't shut down when Step 2 opens. It becomes the custom shop -- defense-spec pods, SCIF modifications, specialty builds that don't fit the automated line. Two revenue streams.
---
> UPDATED 2026-03-23 -- POST-GTC REWRITE
### Updated for 40-ft Pods + 800V DC:
Same Omniverse-first design philosophy. Same 7-station automated line. Updated specs:
    - Containers: 40-ft HC ISO (not 20-ft)
    - Power system per pod: Eaton Beam Rubin DSX (800V DC)
    - Cooling: Integrated dry cooler (no immersion tanks)
    - Compute: NVIDIA NVL72 racks (arrive complete, forklift into position)
    - QA: NVIDIA Metropolis AI vision inspection still applies
### Automation Advantage:
The shift from immersion to NVIDIA liquid-cooled racks actually SIMPLIFIES automation:
    - No fluid filling station
    - No immersion tank fabrication
    - No custom CDU builds
    - Rack install is forklift + connect 3 things (power, cooling, network)
    - Robot arms handle repetitive tasks (insulation, cable routing, sensor placement)
    - Metropolis inspects welds, connections, sensor placement
---
Capital: $5.25-8.25M (unchanged)
Revenue at capacity: $1.5M/month (unchanged)
Timeline: 12-18 months after Step 1 proves demand
### Site: 14th & Hwy 90, New Iberia
    - Pipeline natural gas on property
    - Solar roof
    - Near First Solar factory (panel supply)
    - Near Louisiana Cat (generator supply)
---
When Step 2 opens, Step 1 (Baton Rouge) becomes the custom/defense spec shop for non-standard builds.
*[Child: NVIDIA Omniverse -- Factory Design Guide]*
# NVIDIA Omniverse -- Factory Design Guide
This page explains Omniverse in plain English so anyone on the team can understand what it does, why we use it, and how it saves us millions.
---
## What Is Omniverse?
Imagine you could build an entire factory inside a video game -- but it's not a game. Every wall, every pipe, every robot arm is physically accurate. If you drop a wrench in Omniverse, it falls at the right speed and bounces the right way. If a robot arm swings left, it shows you exactly what it would hit.
That's Omniverse. It's NVIDIA's platform for building digital twins -- perfect virtual copies of real-world things. Factories, warehouses, cities, robots, cars. If it exists in the physical world, you can build a digital copy in Omniverse and test it before spending a dollar on the real thing.
> Think of it like a flight simulator for factories. Pilots don't learn to fly in a real plane first -- they learn in a simulator where crashing costs nothing. We don't build a $5M factory first -- we build it in Omniverse where mistakes cost nothing.
---
## What We Use It For
### 1. Factory Layout
Before pouring concrete, we place every machine, every wall, every doorway in the virtual factory. We walk through it. We drive a forklift through it. We find out that Station 4 is too close to the wall BEFORE we build the wall.
### 2. Robot Programming
Every robot arm in the factory gets programmed in simulation first. We teach it to pick up a server rack, move it into the container, and set it down -- all virtually. When we install the real robot, we upload the program and it works on day one. No weeks of on-site programming.
### 3. Production Testing
We run 1,000 pods through the virtual factory in a single afternoon. We find out that Station 3 takes 20 minutes longer than Station 2, creating a bottleneck. We fix it in the design -- add a second Station 3, rearrange the flow, or speed up the process. All before construction starts.
### 4. Live Monitoring
After the real factory is built, every sensor feeds data into the digital twin. If a motor is running hot, the digital twin shows it glowing red before it fails. If production is slowing down, the twin shows exactly where and why. Scott can watch the whole factory from his phone.
---
## What This Saves Us
```plain text
WITHOUT OMNIVERSE (Traditional Factory Build):
  Design errors found during construction     $200-500K in rework
  Robot programming on-site                   6-8 weeks of downtime
  Bottleneck discovery after opening           3-6 months of lost output
  Unplanned equipment failure                  $50-100K per incident
  TOTAL WASTE: $500K-1.5M in first 2 years

WITH OMNIVERSE:
  Design errors found in simulation            $0 to fix
  Robot programming in simulation              0 weeks of downtime
  Bottleneck discovery before construction     0 months of lost output
  Predictive maintenance via digital twin      Near-zero unplanned failure
  TOTAL WASTE: Near zero

  Omniverse license + design time: ~$150-250K
  Savings in first 2 years: $500K-1.5M
  ROI: 3-6x return
```
---
## NVIDIA Isaac Sim -- The Robot Trainer
Isaac Sim is the part of Omniverse specifically for robots. Here's what it does in plain language:
Instead of buying a $200,000 robot arm and spending 6 weeks teaching it to pick up a server rack in the real world (where it might crash into things, drop expensive equipment, or hurt someone), you teach it in Isaac Sim first. The virtual robot practices 10,000 times in one night. When you put the program into the real robot, it already knows exactly what to do.
    - Train in simulation: robot practices millions of movements overnight
    - Transfer to real hardware: upload program, robot works on day one
    - Update remotely: change the program in simulation, push to factory floor
    - Test edge cases: what if the container is 2 inches off-center? Sim handles it
---
## NVIDIA Metropolis -- The Quality Inspector
Metropolis is NVIDIA's AI vision platform. In our factory, it does one critical job: making sure every pod is built correctly before it ships.
Cameras at each station feed images to an AI that's been trained on thousands of correct assemblies. If a cable is in the wrong port, a screw is missing, or a tank isn't seated properly -- the AI flags it instantly. No human inspector can match this speed or consistency.
    - Camera at every station: automatic visual inspection
    - AI trained on correct vs incorrect assembly: catches defects humans miss
    - Real-time alerts: stops the line if critical defect detected
    - Documentation: every pod gets a photographic build record
---
> UPDATED 2026-03-23 -- POST-GTC REWRITE
## Pod Factory Strategy -- Updated
### Key Changes Post-GTC:
  - Pods are now 40-ft High Cube ISO containers (NOT 20-ft)
  - NVIDIA ships complete liquid-cooled NVL72 racks -- no custom immersion engineering
  - EC-110 immersion cooling DEPRIORITIZED
  - 800V DC native power via Eaton Beam Rubin DSX in every pod
  - Multi-vendor chip support (NVIDIA primary, Terafab/AMD ready)
  - Each pod is a self-contained AI factory node: compute + cooling + power + network
### Two-Step Strategy (unchanged concept, updated specs):
  - Step 1: Baton Rouge Terminal -- manual assembly, 40-ft containers, 2-3 pods/month
  - Step 2: New Iberia -- Omniverse-designed automated factory, 8-12 pods/month
### What Goes In Each 40-ft Pod:
  - 10 NVIDIA NVL72 racks per pod (8 compute + 1 network + 1 storage) — 576 GPUs (C1 SuperPOD), 1.3 MW IT load, 800V DC native
  - Eaton Beam Rubin DSX (800V DC rectifier + busway + PDU)
  - Integrated dry cooler (exterior mount, self-contained cooling)
  - Portable natural gas generator hookup OR grid tie
  - Optional: First Solar rooftop panels, LFP battery
  - Network: Starlink or fiber backhaul to Willow Glen NOC
  - Fire suppression: Novec 1230 + VESDA
  - Total power per pod: 130-260 kW IT + ~30 kW overhead
*[Child: LSU + Willow Glen -- Tiger AI Factory]*
> TIGER AI FACTORY -- LSU + Willow Glen Terminal. Former 2,200 MW Entergy station on the Mississippi River, 20 min from LSU campus. 700 acres, 100+ MW scale ceiling. Parallel project to Trappeys. Purple and gold. Geaux Tigers.
GPS: 30.24700N, 91.09850W  |  St. Gabriel, Iberville Parish  |  Scout Score: 94/100 Tier A
---
# Live Page
  - adc3k.com/lsu -- full partnership pitch (purple and gold, LIVE)
---
# Willow Glen Terminal -- The Site
## Infrastructure Already On-Site
  - 700 acres total, 400+ developable, subdividable to 1 acre
  - Former 2,200 MW Entergy power station (built 1960, decommissioned 2016)
  - 230kV + 138kV Entergy substation -- LIVE, bidirectional
  - 2.33 million barrel tank farm -- renewable diesel storage
  - 3,500 ft Mississippi River frontage + 43-ft deepwater dock
  - 20,000 SF warehouse available for lease (Phase 1 building)
  - Clean-burning natural gas pipeline on-site (pipeline corridor)
  - River water cooling intake infrastructure from power station era
  - CN Railway access  |  I-10 highway access  |  M2 Heavy Industrial zoning
  - FEMA Zone X (minimal flood risk)
## Ownership
  - Zydeco Equity Holdings LLC (Yorktown Energy Partners)
  - Willow Glen Ventures LLC
  - CBRE listing broker: Bryce French, Senior VP
  - Currently operating as bulk liquids terminal (renewable diesel feedstock to Diamond Green Diesel)
---
# Site History -- 300+ Years
  - Pre-1699: Indigenous tribes (Bayogoula) on the Mississippi River corridor
  - 1699: Pierre LeMoyne explores, Iberville Parish named after him
  - 1800s: 'Sweet Iberville' -- state's leading sugarcane producer. Willow Glen Plantation on this land.
  - 1960: Entergy builds 2,200 MW power station -- 5 generating units, powered Louisiana for 56 years
  - 2016: Entergy decommissions -- 'replaced by more efficient means'
  - 2020: Zydeco acquires 700 acres. Genover demolition: 30,000+ tons steel, 1M+ lbs copper recovered.
  - 2026: ADC proposes Tiger AI Factory. Same land, same river, same grid -- new mission.
'This place has been powering Louisiana since before Louisiana was a state. We're just giving it a new mission.'
---
# LSU Partnership
## Why LSU
  - SEC flagship -- national visibility, alumni network, political weight
  - R1 Carnegie Classification -- 35,000+ students
  - Governor's university -- Baton Rouge is the state capital
  - ZERO GPU infrastructure -- 62 A100s on campus (2020 generation) vs UF's 504 Blackwell
  - 20 minutes from Willow Glen
## The HiPerGator Gap
  - UF HiPerGator 4: 504 Blackwell GPUs, $180M+ investment, #3 in the world, 7,000 users, 230 AI courses
  - LSU today: 62 A100s on campus, sub-$1M investment, not ranked, launching first AI degree 2027 with NO compute
  - $37B+ in AI compute being built in Louisiana (Meta, Amazon, Hut 8) -- NONE serving universities
  - ADC fills the gap without asking NVIDIA or the state for donations
---
# Research Departments That Benefit
## Petroleum Engineering -- Ranked #3 Nationally
  - Craft & Hawkins Department -- tied Penn State
  - PERTT Lab -- ONLY US university with 6 full-scale research wells
  - Industry partners: ExxonMobil, Shell, BP, Chevron
  - Generative AI for seismic imaging, physics-informed ML, deepwater drilling safety
  - Currently running on 2018 V100S GPUs
## Center for Computation & Technology (CCT)
  - 44 joint faculty -- AI, cybersecurity, coastal modeling, quantum, astrophysics
  - Deep learning, neuromorphic computing, LLM development
  - AI wildfire prediction (XPRIZE finalist), drug discovery
## Robotics -- iCORE Lab
  - Underwater autonomy (BlueROV2), industrial arms (FANUC/UR), quadcopter drones
  - Military, subsea, agriculture, medicine applications
## Computer Science & Engineering
  - Launching first BS in AI in Louisiana (spring 2027)
  - First Digital Twin Certificate in the US (Bentley Systems)
  - Built MikeGPT (custom AI, 35,000 documents)
  - ONLY Louisiana institution in the AI Alliance
## College of Agriculture (AgCenter)
  - Drone/satellite imagery for crop yield prediction
  - Funded graduate positions in Agricultural Robotics and AI
## Medical / Health Sciences
  - Pennington Biomedical Research Center -- world-renowned (precision nutrition, obesity, diabetes)
  - LSU Health Sciences -- bioinformatics, genomics, AI burn imaging
## Southern University (HBCU, also Baton Rouge)
  - $68M CSTEM building unveiled February 2026 -- 86K sq ft, 20 labs
  - Zero dedicated GPU compute
  - HBCU partnership = strong equity angle for federal grants
---
# K-12 Education Pipeline
## Iberville Parish (St. Gabriel -- where the factory lives)
  - 8 schools. ZERO STEM programs. ZERO robotics teams. ZERO CS curriculum.
  - ADC = the STEM anchor for the entire parish
## Baton Rouge (88 schools)
  - Baton Rouge Magnet High -- #1 public school in LA. VEX robotics state champs 5/6 years.
  - Scotlandville Magnet High -- Academy of Engineering + IT. ONLY nationally certified STEAM school in LA.
  - University Lab School -- LSU-operated K-12 on campus
## Private Schools
  - Episcopal (Newsweek Top 500 STEM), Catholic High (STREAM), St. Joseph's (JoeBotics), Parkview Baptist (FRC Team 3753)
## State Programs
  - K-12 CS Standards live 2025-2026 | AI Essentials Course Fall 2026 (LSU Cain Center)
  - LED FastStart -- #1 ranked workforce training 12 years. FREE.
  - LSU STEM Pathways -- 4 high school pathways + diploma seals
---
# Power Architecture -- 800V DC Native
  - Layer 1: Solar -- ground mount + rooftop (400+ acres available). First Solar 90 mi.
  - Layer 2: Clean-burning natural gas -- BACKBONE 24/7. Henry Hub ~60 mi. Pipeline on-site.
  - Layer 3: Diesel gensets -- emergency. Renewable diesel (HVO) from Diamond Green Diesel.
  - Layer 4: Grid (Entergy) -- SELL-BACK ONLY. Existing 230kV substation.
800V DC native (Eaton Beam Rubin DSX). 96% delivery efficiency. PUE target 1.03. Same architecture as Trappeys but bigger scale.
## Willow Glen Advantages Over Trappeys
  - Existing 2,200 MW electrical grid -- substation, switchyard already built
  - Mississippi River cooling -- unlimited thermal capacity
  - 400+ acres for ground-mount solar (not limited to rooftops)
  - Pipeline corridor (massive gas infrastructure)
  - Scale ceiling 100+ MW vs 29 MW at Trappeys
  - CCGT at scale: $0.04-0.05/kWh vs $0.058-0.068 reciprocating
---
# Renewable Fuel Options
  - Renewable Diesel (HVO): Diamond Green Diesel in Norco (60 river miles). 1.2B gal/yr. WGT already ships them feedstock. Zero generator mods. 65-90% carbon reduction.
  - RNG: Pipeline on-site. Cat generators approved. Book-and-claim contracts available now.
  - Hydrogen: Hidrogenii (Plug Power + Olin) IN ST. GABRIEL. 15 TPD. Cat CG260 supports 25% blend TODAY.
  - B20 Biodiesel: Price-neutral. Zero mods. Switch immediately.
  - ESG premium: 10-30% green token premium on compute = $8-25M additional Y5 revenue.
---
# Energy Recovery
## Waste Heat Recovery
  - Absorption Chillers: Use 40 MW waste heat to produce 11,000+ tons cooling. Eliminates electric chillers. YORK/Trane. 4-5 month payback.
  - ORC (Organic Rankine Cycle): 8-11 MW free electricity from exhaust heat. Ormat Technologies (Reno, NV). Mississippi River as cold sink = 15-25% more efficient.
  - Combined value: $10-18M/year
## Mississippi River Hydrokinetic
  - ORPC (Portland, ME) deploying on Lower Mississippi with Shell
  - 100-500 kW realistic from 3,500 ft frontage
  - Supplemental power for dock, monitoring, security
  - 'Powered by the Mississippi' narrative
---
# Vendor Stack
  - Louisiana Cat -- CG260 gensets (H2 ready), switchgear, ATS. New Iberia, 90 mi.
  - First Solar -- TR1 panels, ground mount. New Iberia factory, 90 mi.
  - Eaton -- Beam Rubin DSX 800V DC, xStorage batteries, supercapacitors. TX + LA manufacturing.
  - Diamond Green Diesel -- Renewable diesel. Norco, 60 river miles. Relationship exists.
  - Hidrogenii -- Hydrogen. IN St. Gabriel. Next door.
  - ATMOS Energy -- Natural gas supply. Pipeline on-site.
Every vendor who helps on Trappeys earns their place on Willow Glen. Two projects, one team.
---
# Incentive Stack
  - ITEP: 80% property tax abatement, 10 years ($8-16M+)
  - Act 730: 20-year sales tax exemption ($200M+ threshold)
  - Solar ITC: 30% federal on larger array
  - Quality Jobs: Cash rebate on payroll
  - LED FastStart: FREE workforce training
  - NSF MRI: Up to $4M through LSU
  - NSF EPSCoR: Up to $10M (Louisiana qualifies)
  - DOE Grid Modernization: $5-20M (800V DC microgrid qualifies)
  - Total pipeline: $28-55M+
---
# Action Items
  - [ ] Willow Glen site visit / drone footage
  - [ ] Contact CBRE / Bryce French re: property access and terms
  - [ ] LSU outreach -- Ram Ramanujam (Special Advisor on AI) is contact #1
  - [ ] Robert Twilley (VP Research) -- knows both LSU and UL Lafayette
  - [ ] Build LSU-specific grant application outlines
  - [ ] Research major LSU donors who might fund AI infrastructure
  - [ ] Southern University outreach -- $68M CSTEM building, zero GPU compute
  - [ ] Sponsor FIRST Robotics team in Iberville Parish (zero teams exist)
  - [ ] Louisiana Cat -- spec CG260 (hydrogen-ready) instead of G3520C for this site
  - [ ] Diamond Green Diesel -- Valero marketing desk for HVO pricing + barge delivery
  - [ ] Hidrogenii (St. Gabriel) -- hydrogen supply conversation
  - [ ] Set up automated phone line (Bland.ai) for broadcast response
  - [ ] Email capture form live on /lsu page (FormSubmit to scott@adc3k.com)
  - [ ] Monday broadcast -- news channels, LSU departments, city officials, alumni
---
Last updated: 2026-03-22. Full details in memory/projects/lsu_willow_glen.md.
# Phased Buildout Plan
## Phase 1 -- Year 1: Proof of Concept (20K SF Warehouse)
  - 10 racks (8 VR + 2 Groq) | 1.3 MW IT | $8M CapEx | $4M revenue
  - Existing 20K SF warehouse -- available NOW, no construction needed
  - 2x Cat CG260 (hydrogen-ready) + 10-acre solar + 1 MWh battery
  - Mississippi River cooling. First tokens flowing. LSU research access live.
## Phase 2 -- Year 2: Fill the Warehouse
  - 33 racks (25 VR + 8 Groq) | 4.3 MW IT | $5M CapEx | $15M revenue
  - Warehouse at capacity. Revenue self-funding Phase 3. NCP certification.
## Phase 3 -- Year 3: First New Building (100K SF)
  - 160 racks (120 VR + 40 Groq) | 20.8 MW IT | $35M CapEx | $57M revenue
  - CCGT turbine online -- $0.04-0.05/kWh, cheapest power in neocloud space
  - ORC waste heat recovery generating 4-5 MW free electricity
## Phase 4 -- Year 4: Campus Expansion (300K SF)
  - 530 racks (400 VR + 130 Groq) | 69 MW IT | $80M CapEx | $190M revenue
  - 3 compute halls. 2nd CCGT. Hydrogen blending. Full waste heat recovery.
## Phase 5 -- Year 5: Full Campus (500K+ SF)
  - 1,000 racks (750 VR + 250 Groq) | 130 MW IT | $120M CapEx | $360M revenue
  - Largest university-accessible AI factory in the United States.
  - Scale ceiling: 2,000+ racks, 260 MW, $480M+ annual on 400 acres
---
# 5-Year Financial Model
75% Vera Rubin / 25% Groq. Blended $2.00/M tokens. 70% utilization. 60% gross margin.
  - Year 1: $4M revenue | $8M CapEx | -$5.6M cumulative
  - Year 2: $15M revenue | $5M CapEx | -$1.6M cumulative
  - Year 3: $57M revenue | $35M CapEx | -$2.4M cumulative
  - Year 4: $190M revenue | $80M CapEx | +$31.6M cumulative
  - Year 5: $360M revenue | $120M CapEx | +$127.6M cumulative
## Summary
  - Total 5-year revenue: $626M
  - Total 5-year CapEx: $248M
  - 5-year net profit: $127.6M
  - Breakeven: Late Year 3 (~34 months)
  - Initial investment: $8M
  - Incentive stack: $93-190M
  - With incentives: $220-320M net positive in 5 years
## Willow Glen vs Trappeys
  - Trappeys: $4.5M start | $82M Y5 | 225 racks | 29 MW | $47M net 5yr
  - Willow Glen: $8M start | $360M Y5 | 1,000 racks | 130 MW | $128M net 5yr
  - COMBINED: $12.5M start | $442M Y5 | 1,225 racks | 159 MW | $175M net 5yr
---
# What LSU Gets
  1. Dedicated GPU compute -- reserved allocation, no AWS retail rates
  1. Student workforce pipeline -- train on real infrastructure 20 min from campus
  1. Grant co-applicant -- NSF MRI ($4M), EPSCoR ($10M), DOE ($5-20M)
  1. Office at the AI factory -- physical presence, research liaison
  1. NVIDIA reference site -- LSU name on certification
  1. Every Louisiana university benefits -- anchor for the entire state
---
# NVIDIA Technology Stack
  - Platform: Vera Rubin NVL72 (72 GPUs/rack, 130 kW, liquid cooled)
  - Networking: Quantum InfiniBand (400 Gb/s per GPU)
  - Software: Dynamo 1.0 (7x performance on same hardware)
  - Decode: Groq 3 LPX (5-10x revenue per MW)
  - Power: Eaton Beam Rubin DSX (800V DC, co-designed with NVIDIA)
  - Certification: NPN > DGX-Ready > NCP > Reference Platform NCP
NOT a data center. GPU compute, liquid cooled, self-powered, 800V DC native. 96% delivery efficiency vs 83% traditional.
---
# Two-Site Network
  - Trappeys (Lafayette) -- UL Lafayette | 29 MW | Proof of concept
  - Willow Glen (St. Gabriel) -- LSU | 260 MW | The flagship
  - Connected by dedicated fiber. Same NVIDIA stack. Same power model.
  - Every vendor who helps on Trappeys earns their place on Willow Glen.
Louisiana's first AI compute network. Privately funded. Energy-first. American-made. Geaux Tigers.
*[Child: 01 -- Investment Thesis]*
> Tiger AI Factory
Content source: Main page above + memory/projects/lsu_willow_glen.md
## Key Points
    - Louisiana has $37B+ in AI compute being built -- NONE serving universities
    - LSU has 62 A100s (2020 generation) vs UF HiPerGator 504 Blackwell GPUs
    - ADC fills the gap without asking NVIDIA or the state for donations
    - Two-site network: Trappeys (proof of concept) + Willow Glen (flagship)
    - Energy-first model: self-powered, 800V DC native, sell-back only grid
    - Former 2,200 MW Entergy station -- same land, same river, same grid, new mission
*[Child: 02 -- Hardware: NVIDIA Vera Rubin Platform]*
> NVIDIA technology stack for Willow Glen.
## Platform
    - Vera Rubin NVL72 (72 GPUs/rack, 130 kW, liquid cooled)
    - Quantum InfiniBand (400 Gb/s per GPU)
    - Dynamo 1.0 (7x performance on same hardware)
    - Groq 3 LPX decode (5-10x revenue per MW)
    - Eaton Beam Rubin DSX (800V DC, co-designed with NVIDIA)
## Certification Ladder
    - NPN (register) > DGX-Ready > NCP > Reference Platform NCP
*[Child: 03 -- Site & Building Specs]*
> Willow Glen Terminal -- St. Gabriel, Iberville Parish
GPS: 30.24700N, 91.09850W | Scout Score: 94/100 Tier A
## Infrastructure Already On-Site
    - 700 acres total, 400+ developable
    - Former 2,200 MW Entergy power station (1960-2016)
    - 230kV + 138kV Entergy substation -- LIVE, bidirectional
    - 3,500 ft Mississippi River frontage + 43-ft deepwater dock
    - 20,000 SF warehouse available for Phase 1
    - Natural gas pipeline on-site
    - River water cooling intake infrastructure
    - CN Railway + I-10 highway + M2 Heavy Industrial zoning
*[Child: 04 -- Government Funding Stack]*
> Incentive pipeline: $28-55M+ through combined programs.
## Programs
    - ITEP: 80% property tax abatement, 10 years ($8-16M+)
    - Act 730: 20-year sales tax exemption ($200M+ threshold)
    - Solar ITC: 30% federal on larger array
    - Quality Jobs: Cash rebate on payroll
    - LED FastStart: FREE workforce training
    - NSF MRI: Up to $4M through LSU
    - NSF EPSCoR: Up to $10M (Louisiana qualifies)
    - DOE Grid Modernization: $5-20M (800V DC microgrid qualifies)
*[Child: 05 -- Infrastructure Partners]*
> Vendor stack for Willow Glen. Every vendor who helps on Trappeys earns their place here.
## Confirmed / Target Partners
    - Louisiana Cat -- CG260 gensets (H2 ready), switchgear, ATS. New Iberia, 90 mi.
    - First Solar -- TR1 panels, ground mount. New Iberia factory, 90 mi.
    - Eaton -- Beam Rubin DSX 800V DC, xStorage batteries
    - Diamond Green Diesel -- Renewable diesel. Norco, 60 river miles.
    - Hidrogenii -- Hydrogen. IN St. Gabriel. Next door.
    - ATMOS Energy -- Natural gas supply. Pipeline on-site.
*[Child: 06 -- ADC3K Credentials]*
> ADC qualifications and track record.
Mirrors MARLIE I credentials section. See main ADC3K deck at adc3k.com.
## Key Credentials
    - Scott Tomsu -- 25+ year ROV Superintendent, deepwater robotics worldwide
    - FAA Private Pilot, IMCA ROV Supervisor, Electronic Technician, Commercial Diver
    - FuelTech engine management certified, multi-time drag racing champion
    - NVIDIA Partner Network registered
    - ADC3K.com live with full project portfolio
*[Child: 07 -- Louisiana AI Network: Multi-Site Vision]*
> Two-site network forming Louisiana AI compute backbone.
## Network Topology
    - Trappeys (Lafayette) -- UL Lafayette | 29 MW | Proof of concept
    - Willow Glen (St. Gabriel) -- LSU | 260 MW ceiling | Flagship
    - MARLIE I (Lafayette) -- Backup NOC, R&D, edge compute
    - KLFT 1.1 -- Autonomous airspace ops hub
    - Connected by dedicated fiber. Same NVIDIA stack. Same power model.
Louisiana first AI compute network. Privately funded. Energy-first. American-made.
*[Child: 08 -- Contact & Next Steps]*
> Action items and contact information.
## Immediate Actions
    - Willow Glen site visit / drone footage
    - Contact CBRE / Bryce French re: property access and terms
    - LSU outreach -- Ram Ramanujam (Special Advisor on AI) is contact #1
    - Robert Twilley (VP Research) -- knows both LSU and UL Lafayette
    - Southern University outreach -- $68M CSTEM building, zero GPU compute
## Contact
Scott Tomsu -- scott@adc3k.com -- adc3k.com
*[Child: 09 -- Financial Architecture & ROI]*
> 5-year financial model. 75% Vera Rubin / 25% Groq. Blended $2.00/M tokens.
## 5-Year Summary
    - Year 1: $4M revenue | $8M CapEx | 10 racks | 1.3 MW
    - Year 2: $15M revenue | $5M CapEx | 33 racks | 4.3 MW
    - Year 3: $57M revenue | $35M CapEx | 160 racks | 20.8 MW
    - Year 4: $190M revenue | $80M CapEx | 530 racks | 69 MW
    - Year 5: $360M revenue | $120M CapEx | 1,000 racks | 130 MW
---
    - Total 5-year revenue: $626M
    - Total 5-year CapEx: $248M
    - 5-year net profit: $127.6M
    - Breakeven: Late Year 3 (~34 months)
    - Initial investment: $8M
> ARCHIVED 2026-03-23: Single entry (Session 6). Low priority reference.