# KLFT 1.1 — Project Overview & README
*Notion backup — 2026-03-28*

# SkyCommand Complete Package
## Autonomous Drone Operations Platform — Full Documentation Suite
Created: February 17, 2026
Total Documents: 11 files across 6 categories
Total Content: ~7,000+ paragraphs of engineering documentation
---
### 📁 01_KLFT_Foundation_Documents/
The original 5 backbone documents for the Lafayette Regional Airport (KLFT) autonomous airspace operations hub, plus the executive slide deck.
| Document | Pages (est.) | Paragraphs | Description |
| System Architecture | ~45 | 824 | 8-subsystem tiered architecture, data flows, technology selections |
| Phase 1 Implementation Spec | ~55 | 1,470 | 13-sprint build plan, API contracts, database schemas, test strategy |
| Software Interface Control Document | ~50 | 1,559 | gRPC, Kafka, shared memory, external interface specifications |
| CONOPS & Safety Case | ~40 | 1,041 | SORA risk assessment, 6-layer defense-in-depth, emergency procedures |
| Facility & Hardware Procurement | ~40 | 1,055 | Server specs, drone/dock hardware, network, budget estimates |
| Document Suite Overview (PPTX) | 5 slides | — | Executive summary slide deck with dark aerospace theme |
### 📁 02_Platform_Architecture/
Generalizes the KLFT concept into the full SkyCommand product platform.
| Document | Paragraphs | Description |
| SkyCommand Platform Architecture | 1,124 | 17 system components, 14 software modules, 7 AI agents, 3 UI layers, cloud infra, hardware integration, security (RBAC + certs), scalability to 50+ vehicles |
### 📁 03_Startup_Guide/
MVP definition for a 2-person drone operations startup.
| Document | Paragraphs | Description |
| SkyCommand MVP Specification | 562 | Smallest functional system ($13K hardware + $200/mo software), 8-week timeline, FlightLog MVP app spec, build order, unit economics, growth triggers |
### 📁 04_Technology_Stack/
Complete technology selection — US-manufactured & open-source edition (DJI-free).
| Document | Paragraphs | Description |
| SkyCommand Technology Stack | 1,186 | Claude AI integration, AWS/Hetzner cloud, Go + Fiber backend, Next.js frontend, Skydio X10 + ArduPilot drones, MapLibre maps, PostgreSQL + TimescaleDB, GitHub Actions CI/CD, Grafana monitoring |
### 📁 05_Dashboard_UI/
Interactive command center interface (React component).
| File | Description |
| SkyCommand_Dashboard.jsx | Live React dashboard: tactical map (canvas), telemetry sparklines, mission monitor, alert center, AI agent status, vehicle control panel, fleet status — dark aerospace HUD aesthetic |
### 📁 06_AI_Knowledge_Center/
Platform architecture for the AI Knowledge Command Center (AIKCC) — a separate product/content platform.
| Document | Paragraphs | Description |
| AIKCC Platform Architecture | 1,171 | 10-domain category tree, FAQ database schema, website architecture, navigation flows, content workflow, monetization (10 models), expansion roadmap, SaaS strategy, branding, first 50 articles |
---
### Document Lineage
```plain text
KLFT Concept (5 docs) → SkyCommand Platform (generalized) → MVP (2-person startup)
                                                            → Tech Stack (US-manufactured)
                                                            → Dashboard UI (React)
AIKCC (separate product track)
```
> KLFT 1.1 — Gulf Coast Emergency Drone Deployment Hub | Mission: first-response aerial coverage for Lafayette and the Gulf Coast corridor. Managed remotely from MARLIE I NOC at 1201 SE Evangeline Thruway, Lafayette LA.
---
## Strategic Role — Gulf Coast Emergency Hub
KLFT 1.1 is the Gulf Coast Emergency Drone Deployment Hub. Its primary mission is rapid aerial ISR and situational awareness during emergencies, natural disasters, infrastructure failures, and search-and-rescue operations across Lafayette and the broader Gulf Coast corridor.
- Platform: Skydio X10 + Skydio Dock (autonomous launch, land, charge, data relay)
- Command: SkyCommand — cloud-native fleet management, mission dispatch, and live video feed
- Remote NOC: MARLIE I at 1201 SE Evangeline Thruway — KLFT operates as a remote edge node
- Edge compute: ADC 3K pod at KLFT site provides on-site inference, video processing, and data buffering
- Power: Lafayette Utilities System (LUS) primary + Bloom Energy fuel cell UPS + diesel N+1 backup
- Target clients: Lafayette city/parish government, GOHSEP, Coast Guard sector, LNG/chemical plant operators
---
## ADC Ecosystem Position
KLFT 1.1 is the first operational showcase of the ADC 3K edge pod in a government/emergency services context. Each ADC 3K pod deployed at KLFT runs SkyCommand inference workloads locally, synchronizing to MARLIE I for fleet coordination and long-term data archiving.
- MARLIE I NOC: mission briefing, fleet telemetry aggregation, incident archive
- ADC 3K pod (KLFT site): video analytics, object detection, mission-local compute
- SkyCommand SaaS: operator interface, mission templates, regulatory compliance (FAA BVLOS)
- Ground Zero: KLFT operations featured as ADC ecosystem episode content
---
> NOTE (2026-03-23): Bloom Energy references elsewhere in this doc suite are superseded by the locked 4-layer power hierarchy (Solar -> Gas -> Diesel -> Grid). GPU spec updated from A4000 to L40S in Hardware Procurement. Skydio has not responded to outreach -- ArduPilot custom build remains the backup path. AIKCC knowledge platform is on hold while AI Advantage SMB business launches first. All other technical content remains current.