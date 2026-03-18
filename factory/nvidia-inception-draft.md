# NVIDIA INCEPTION PROGRAM — APPLICATION DRAFT

**Ready for Scott's review. Submit at: https://www.nvidia.com/en-us/startups/**

---

## Company Information

| Field | Value |
|-------|-------|
| Company Name | Advantage Design Construction Inc. (ADC) |
| Website | adc3k.com |
| Founded | 2003 (ADC 3K AI Infrastructure division launched 2025) |
| Location | Lafayette, Louisiana, USA |
| Founder / CEO | Scott Tomsu |
| Employees | 1-10 |
| Stage | Pre-revenue / Prototype |
| Industry | AI Infrastructure / Edge Computing / Manufacturing |
| Funding | Self-funded (bootstrapped) |

---

## Company Description

*Suggested — edit to your voice before submitting:*

Advantage Design Construction Inc. (ADC) deploys NVIDIA Vera Rubin AI infrastructure on renewable micro grids across Louisiana. We offer two deployment paths — both 100% NVIDIA stack:

**Option A — Enterprise Rack Deployment (Revenue Now):** We lease and build out existing industrial facilities for immediate Vera Rubin NVL72 rack deployment. Our flagship site — Willow Glen Terminal on the Mississippi River — is a former 2,200 MW power station with a 230kV Entergy substation, 700 developable acres, deepwater dock, gas pipeline, and a 20,000 SF warehouse ready for rack rows today. We are a licensed Louisiana general contractor — we pull the permits, do the buildout, and take delivery. Operational in weeks, not years.

**Option B — ADC 3K Containerized Pods (Differentiated Product):** Our manufactured AI compute pods are self-contained, liquid-immersion-cooled SuperPOD building blocks inside modified shipping containers. Self-powered (natural gas + solar), self-cooled (EC-110 dielectric immersion at PUE 1.03), and remotely managed from our NOC. Field-deployable to any site with power and fiber.

Both options connect to a shared NVIDIA Quantum InfiniBand spine using fat-tree topology. Racks or pods — they're all leaves on the spine. AI-driven monitoring (DCGM + UFM) identifies bottlenecks in real time, and we add capacity at the exact point of need. The fabric grows organically.

We are building two manufacturing facilities: a manual pod assembly terminal (2-3 pods/month within 90 days) and a fully automated robotic factory designed in NVIDIA Omniverse (8-12 pods/month). The automated factory runs Isaac Sim for robot path programming, Metropolis for AI vision quality control at every station, and Omniverse for a full digital twin.

ADC is 100% NVIDIA stack — silicon to software. Vera Rubin or nothing. No legacy hardware, no backwards-compatible builds, no third-party alternatives. Louisiana has the most aggressive AI infrastructure tax incentive stack in the country (OBBBA 100% bonus depreciation, Act 730 sales tax exemption, ITEP 10-year property tax abatement, LED FastStart workforce training). We are the licensed general contractor in that state.

---

## How ADC Uses NVIDIA Technology

### Current / Planned Usage

| NVIDIA Product | How ADC Uses It | Status |
|----------------|----------------|--------|
| **Omniverse** | Full digital twin of our 52,800 SF automated pod factory. Building design, robot reach simulation, material flow optimization, and live production monitoring — all in OpenUSD. | Design phase |
| **Isaac Sim** | Robot path programming for 14 robotic systems across 7 assembly stations. Weld paths, spray foam coverage, pick-and-place, cable routing — all simulated before physical deployment. | Design phase |
| **Metropolis** | 22 AI vision cameras across all factory stations running edge inference on Jetson AGX Orin. Quality inspection at every step: weld analysis, foam coverage, wire verification, thermal signatures. | Design phase |
| **AI Enterprise** | Production scheduling optimization, predictive maintenance, defect root-cause analysis, and energy management across our factory and pod network. | Planned |
| **Jetson AGX Orin** | 7 edge inference nodes (one per factory station) running Metropolis models locally at <50ms latency. Also exploring Jetson in deployed pods for on-site AI inference. | Procurement |
| **DGX SuperPOD Architecture** | ADC 3K pods are modular SuperPOD building blocks. Each pod contains NVIDIA GPU racks (Vera Rubin NVL72) connected via NVLink + NVSwitch internally. Pods connect to NVIDIA Quantum InfiniBand spine in fat-tree topology for multi-pod fabric scaling. | Architecture |
| **Quantum InfiniBand (NDR)** | Inter-pod networking fabric. NVIDIA Quantum-2 spine switches + ConnectX-7/8 NICs in each pod. Fat-tree topology enables organic growth — add pods to scale wide, inject pods to eliminate bottlenecks. | Architecture |
| **Base Command Manager** | Cluster orchestration across all deployed pods. Single pane of glass for the entire SuperPOD fabric from our NOC at MARLIE I. | Planned |
| **DCGM + UFM** | Real-time GPU telemetry and InfiniBand fabric monitoring. AI-driven bottleneck detection tells us exactly where to inject the next pod. | Planned |
| **BlueField DPU** | Network acceleration and security isolation in deployed pods. Hardware-level data sovereignty for defense and sovereign AI customers. | Architecture |

### NVIDIA Technology in Our Factory (7 Stations)

1. **Receiving** — Metropolis inspects incoming containers for damage
2. **CNC/Fabrication** — Metropolis verifies weld quality; Isaac Sim programs Arc Mate welding robot paths
3. **Insulation** — Metropolis thermal camera validates foam coverage; Isaac Sim programs ABB spray paths
4. **Electrical** — Metropolis verifies every wire connection (color, gauge, torque, seating)
5. **Cooling** — Metropolis monitors pressure tests and fill levels
6. **Compute Install** — Metropolis verifies rack alignment, cable routing, connector seating
7. **Test Cell** — 20-camera Metropolis thermal array validates full pod during 4-hour GPU burn-in

### NVIDIA Technology in Our Deployed Pods

- **DGX SuperPOD architecture** — each pod is a fabric building block (Vera Rubin NVL72 / Blackwell Ultra B300)
- **NVIDIA Quantum InfiniBand** — fat-tree spine fabric connecting pods into scalable SuperPOD
- **NVLink 6 + NVSwitch** — intra-pod GPU-to-GPU interconnect (all-to-all within rack)
- **ConnectX-7/8 NICs** — per-pod InfiniBand connectivity to spine
- **BlueField-3 DPU** — network acceleration, hardware security isolation
- **DCGM** — GPU telemetry, health monitoring, performance optimization
- **UFM** — InfiniBand fabric management and AI-driven bottleneck detection
- **Base Command Manager** — cluster orchestration from MARLIE I NOC
- **Jetson AGX Orin** — on-pod health monitoring, edge inference, remote diagnostics
- **NVIDIA AI Enterprise** — workload orchestration, scheduling, optimization across fabric

---

## Market Opportunity

The AI compute infrastructure market is constrained by four bottlenecks: power, cooling, time-to-deploy, and scalability. ADC solves all four:

- **Power**: Louisiana has the cheapest energy in the US (Henry Hub natural gas at $2-3/MMBtu). Our pods generate their own power on renewable micro grids. Highest token-per-dollar value in the industry.
- **Cooling**: Full liquid immersion at PUE 1.03 vs. industry average 1.58 — 35% less energy wasted on cooling.
- **Time**: Option A (racks in a building) deploys in weeks. Option B (pods) deploys anywhere with power and fiber. Both faster than any new-build facility.
- **Scalability**: Fat-tree SuperPOD topology. Racks or pods — they're all leaves on the InfiniBand spine. Add leaves to scale wide. Inject capacity at bottlenecks. AI-managed fabric grows organically — unlike fixed facilities that fill once and stop.

### Target Markets
1. **Oil & Gas** — Edge AI at production sites (Louisiana, Texas, Gulf of America)
2. **Defense / Government** — SCIF-rated, self-powered AI pods for forward deployment
3. **Healthcare** — Medical AI inference at hospitals without data center buildout
4. **Manufacturing** — Factory-floor AI (quality inspection, predictive maintenance)
5. **Sovereign AI** — Nations and enterprises requiring on-premises AI compute

### Revenue Model
- Pod sales: $120K-250K per unit depending on configuration
- Managed services: NOC monitoring, GPU-as-a-Service from MARLIE I
- Site development: Willow Glen campus lease + power revenue

---

## What ADC Needs from NVIDIA Inception

### Immediate Value

| Need | How Inception Helps |
|------|--------------------|
| **Omniverse Enterprise license** | Design and simulate our automated factory before breaking ground |
| **Isaac Sim access** | Program 14 robot systems in simulation, validate before physical install |
| **Metropolis deployment support** | Train and deploy AI vision models for factory QA |
| **Jetson AGX Orin dev kits** | Prototype edge inference at factory stations |
| **Technical architecture review** | Validate our GPU deployment designs (NVL72 rack configs, cooling specs) |
| **Go-to-market support** | NVIDIA partner badge builds customer trust for pod sales |

### Long-Term Partnership
- ADC becomes the reference implementation for NVIDIA Vera Rubin deployment in Louisiana — both rack and containerized
- 100% NVIDIA stack — silicon, networking, software, management. Vera Rubin or nothing. No third-party alternatives.
- Louisiana's first Omniverse-designed, AI-automated manufacturing facility
- Every rack and pod we deploy runs NVIDIA GPUs on NVIDIA InfiniBand with NVIDIA software — fully aligned incentives
- Flagship site (Willow Glen): 700 acres, 230kV substation, Mississippi River cooling, renewable micro grid, 20K SF warehouse ready NOW — ready for NVIDIA showcase
- Hut 8 is 45 min north with $10B and Google's money. ADC is doing it smarter, latest gen only, in the best tax state in the country.
- ADC proves NVIDIA's platform works from factory floor (Omniverse) to deployed infrastructure (SuperPOD) to remote management (Base Command) — the full loop

---

## Traction / Progress

| Milestone | Status |
|-----------|--------|
| ADC 3K pod design complete | Done |
| adc3k.com live with 5 project decks | Done |
| Willow Glen site scored (94/100, Tier A) | Done |
| MARLIE I engineering complete | Done |
| Trappeys first deployment site identified | Done |
| KLFT autonomous airspace hub designed | Done |
| New Iberia factory — full engineering package | Done (6 documents, interactive floor plan, production simulator) |
| Baton Rouge Terminal — lease spec ready | Done |
| Edge AI strategy — 5 customer segments defined | Done |
| Omniverse factory digital twin architecture designed | Done |
| Pod factory BOM priced ($7.9-9.3M) | Done |
| Founder: 8 NVIDIA certifications including NCA-AIIO | Done |
| Founder: CompTIA A+ & Network+ (since late 1990s) | Done |

---

## Founder Background

**Scott Tomsu** — 25+ year career in robotics, remote operations, and complex system integration:

- **ROV Superintendent** — Managed deepwater robotic operations worldwide (West Africa, Gulf of America, global). Operated remotely piloted vehicles in extreme environments at depths exceeding 10,000 feet.
- **NVIDIA Certified (8 credentials)** — NCA-AIIO (AI Infrastructure & Operations), Base Command Manager Administration, InfiniBand Essentials, NetQ Network Operations, NVIDIA License System, AI Fundamentals, Ansible for Network Engineers, Introduction to Networking.
- **CompTIA A+ & Network+** — Certified since late 1990s. OSI model, switching, routing, subnets.
- **Commercial Diver** — Divers Academy graduate. IMCA ROV Supervisor certification. Electronic Technician certification.
- **FAA Private Pilot** — Fixed wing. Instrument written (90%).
- **FuelTech Certified** — Advanced engine management and electronic control systems. Closed-loop optimization directly maps to AI factory networking (sensors → processing → SDN adjustment).
- **Construction** — Founded Advantage Design & Construction. Louisiana General Contractor license. Hands-on builder with industrial construction experience.

Scott brings the rare combination of robotics expertise, NVIDIA infrastructure certification, remote operations management, construction knowledge, and electronic systems integration that this venture requires. He has personally managed robotic systems in environments more demanding than any factory floor — and holds the certifications to design, deploy, and manage the NVIDIA stack that runs inside every pod.

---

## Application Checklist

Before submitting, verify:
- [ ] Company email (not personal) — use scott@adc3k.com or similar
- [ ] Website URL: adc3k.com
- [ ] LinkedIn profile linked
- [ ] "AI Infrastructure" or "Edge Computing" selected as primary category
- [ ] NVIDIA products listed: DGX SuperPOD, Quantum InfiniBand, Omniverse, Isaac Sim, Metropolis, Jetson, AI Enterprise, Base Command Manager, DCGM, UFM, BlueField DPU, ConnectX, NVLink, NVSwitch
- [ ] Describe how NVIDIA tech is used (copy from Section 2 above)
- [ ] Stage: Pre-revenue
- [ ] Funding: Self-funded

---

*Draft prepared by Mission Control — 2026-03-11*
*Scott: Review, edit to your voice, and submit at nvidia.com/startups*
