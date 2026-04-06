# SkyCommand — Technology Stack
*Notion backup — 2026-04-06*

SKYCOMMAND
TECHNOLOGY STACK
RECOMMENDATION
US-Manufactured & Open-Source Edition
Complete Technology Selection for a Reliable, Lean, Sanctions-Proof Drone Operations Platform
Zero Chinese-manufactured hardware. Skydio + ArduPilot + Blue UAS approved alternatives.
AI Models • Cloud • Backend • Frontend • Drones • Maps • Databases • Automation • Monitoring
Document Version: 2.0 | February 2026
ENGINEERING RECOMMENDATION
1. STACK SELECTION PHILOSOPHY
This technology stack is designed for a 2-4 person engineering team operating a commercial drone platform. Every choice is evaluated against three constraints in this exact priority order: reliability (the system must not fail during flight operations), minimal staffing (one engineer must be able to maintain each layer), and cost efficiency (start cheap, scale without rewriting). A fourth constraint now applies to all hardware selections: supply chain resilience. All drone and dock hardware is sourced from US-manufactured, allied-nation, or open-source platforms to eliminate regulatory risk from foreign adversary bans.
1.1 Decision Framework
| Criterion | Weight | Test Question |
| Reliability | 35% | Will this component cause a flight safety incident if it fails? Can it self-heal? |
| Supply chain / regulatory safety | 20% | Could this vendor be banned, sanctioned, or restricted by US law within 3 years? |
| Operational simplicity | 20% | Can one person deploy, monitor, and troubleshoot this at 3 AM? |
| Team skill fit | 10% | Can a full-stack engineer be productive within one week? |
| Cost at scale | 10% | Does pricing stay reasonable at 50 vehicles and 10K API calls/day? |
| Ecosystem maturity | 5% | Are there 5+ years of production usage, Stack Overflow answers, and active maintenance? |
1.2 Why Zero Chinese-Manufactured Drones
The Countering CCP Drones Act (passed by the US House in June 2024 and advancing through the Senate) would add DJI to the FCC Covered List, effectively banning new DJI drones from operating on US communications infrastructure. Multiple federal agencies (DoD, DOI, DHS) have already restricted or banned DJI products. Even if the full ban does not pass, the trend is unmistakable: US commercial drone operators who build on Chinese platforms face escalating regulatory risk, client restrictions (especially government and enterprise), and potential stranded hardware assets. This stack eliminates that risk entirely.
| Risk Factor | Impact | Mitigation in This Stack |
| FCC Covered List addition | New DJI drones cannot use US radio spectrum; existing units may be grandfathered but no new purchases | All hardware is US-manufactured (Skydio) or open-source (ArduPilot/PX4) with US/allied components |
| Government contract eligibility | Blue UAS list required for DoD/federal work; DJI is not on Blue UAS | Skydio X10 is Blue UAS approved; ArduPilot builds can be sourced from US integrators |
| Enterprise client restrictions | Fortune 500 and critical infrastructure increasingly require non-Chinese drones | US-manufactured drones remove procurement friction; opens enterprise and gov market |
| Data sovereignty concerns | DJI Cloud API routes data through DJI servers (Chinese-owned infrastructure) | Skydio offers on-prem data option; ArduPilot is fully self-hosted; zero foreign data routing |
| Firmware update risk | Vendor could push firmware that degrades or disables functionality | Skydio firmware is US-controlled; ArduPilot firmware is open-source and community-audited |
| Spare parts and support | Sanctions could disrupt supply chain for parts, batteries, accessories | US/allied supply chains; ArduPilot components from multiple US/EU sources |
1.3 Stack Summary
| Layer | Primary Choice | Backup/Alternative | Monthly Cost (MVP) | Monthly Cost (Scale) |
| AI Models | Anthropic Claude API | OpenAI GPT-4o (fallback) | $50-200 | $500-2,000 |
| Cloud Platform | AWS (primary) or Hetzner (budget) | GCP, Azure, or on-prem K3s | $150-300 | $2,000-5,000 |
| Backend Framework | Go + Fiber + gRPC | Node.js / TypeScript (if Go skill unavailable) | $0 (language) | $0 |
| Frontend | Next.js 14 (App Router) + Tailwind | SvelteKit (lighter alternative) | $0 (Vercel free) | $20-100 |
| Drone Platform | Skydio X10 (primary) + ArduPilot custom (secondary) | Inspired Flight IF1200, Teal 2, Parrot ANAFI USA | $0 (SDK) | $0 |
| Dock Platform | Skydio Dock + Valqari custom | DroneShield Nest, Airobotics (allied-nation) | $0 (SDK) | $0 |
| Mapping | MapLibre GL JS + PMTiles | Mapbox GL JS (paid), Deck.gl (3D) | $0 (self-hosted tiles) | $0-200 |
| Primary Database | Supabase (PostgreSQL) | Neon, AWS RDS, self-hosted Patroni | $0-25 | $75-300 |
| Time-Series DB | TimescaleDB Cloud | InfluxDB Cloud, QuestDB | $0-29 | $100-500 |
| Cache | Upstash Redis | AWS ElastiCache, Dragonfly | $0-10 | $50-200 |
| Message Queue | Upstash Kafka or RedPanda Cloud | Confluent Cloud, AWS MSK | $0-30 | $200-800 |
| Object Storage | Cloudflare R2 | AWS S3, Backblaze B2 | $0-5 | $20-100 |
| Automation / CI/CD | GitHub Actions | GitLab CI, Dagger | $0 (free tier) | $0-20 |
| Monitoring | Grafana Cloud (free tier) | Datadog, self-hosted Prometheus+Grafana | $0 | $50-400 |
| Auth | Clerk | Supabase Auth, Auth.js | $0-25 | $50-200 |
Total MVP monthly cost: $200-625/month all-in. Total at scale (50 vehicles): $3,000-10,000/month.
2. AI MODEL PROVIDERS
2.1 Primary: Anthropic Claude API
| Use Case | Model | Why Claude | Input/Output | Est. Cost/Month (MVP) |
| Mission report generation | Claude Sonnet 4 | Best-in-class structured output; follows templates precisely; handles technical aviation language | Mission log JSON -> formatted report prose + analysis | $20-50 |
| Anomaly narrative | Claude Haiku 4.5 | Fast + cheap; explains telemetry anomalies in operator-readable language | Anomaly detection output -> plain-English explanation + recommended action | $5-10 |
| Compliance interpretation | Claude Sonnet 4 | Interprets regulatory text against mission parameters; cites specific rule sections | Mission plan + Part 107 text -> compliance assessment with citations | $10-30 |
| Client communication | Claude Sonnet 4 | Drafts professional client emails, proposals, status updates from mission data | Mission summary + client context -> email/proposal draft | $5-15 |
| Maintenance recommendations | Claude Haiku 4.5 | Translates predictive maintenance model output into actionable maintenance orders | Component health scores + history -> prioritized maintenance tasks | $5-10 |
| Natural language search | Claude Haiku 4.5 | Operators query flight logs in plain English instead of SQL | 'Show me all flights near downtown with high wind' -> structured query | $5-10 |
2.2 Fallback: OpenAI GPT-4o
Maintain a thin abstraction layer over LLM calls so you can swap providers. Use OpenAI GPT-4o as fallback for availability (if Anthropic API is down) and for specific capabilities like Whisper (speech-to-text for pilot voice notes). Never hard-code to a single provider.
2.3 AI Integration Architecture
| Pattern | Implementation | Safety Boundary |
| LLM abstraction layer | Single Go/TS module with provider interface: Claude, OpenAI, local (Ollama). Swap via config, not code change | All LLM calls logged with input, output, model version, latency, cost |
| Prompt management | Prompts stored in version-controlled YAML files, not hardcoded. A/B test prompt versions | Prompt changes require review; production prompts tagged and immutable |
| Output validation | Every LLM output parsed against expected schema (JSON Schema validation). Reject and retry on malformed output | LLM never directly executes commands; output is always validated then acted on by deterministic code |
| Cost controls | Per-user and per-feature daily spend limits. Alert at 80% threshold. Hard cutoff at limit | Runaway prompt loops cannot exceed $50/day without manual override |
| Caching | Cache identical prompt+input combinations in Redis (TTL: 1 hour for reports, 5 min for real-time). Saves 40-60% on repeat queries | Cache key includes model version; cache invalidated on prompt version change |
| Graceful degradation | If AI provider is unavailable: reports generated without AI narrative (data only), anomaly alerts show raw data, compliance shows rule pass/fail without explanation | System never blocks a mission because an AI API is down |
2.4 Local / Edge AI
| Model | Purpose | Hardware | Framework |
| YOLOv8-nano | Airspace intrusion detection from PTZ camera feed | Jetson Orin NX (edge node) | TensorRT / ONNX Runtime |
| Custom anomaly model | Real-time telemetry anomaly scoring (isolation forest + autoencoder) | Server CPU | PyTorch -> ONNX -> Go inference |
| Whisper-small | Pilot voice note transcription (offline-capable) | Laptop / phone | whisper.cpp (C++ port, runs on CPU) |
3. CLOUD PLATFORM
3.1 Primary Recommendation: AWS (Standard) or Hetzner (Budget)
| Decision Factor | AWS | Hetzner | When to Choose |
| Cost (MVP) | $150-400/mo | $50-100/mo | Hetzner if budget is king; AWS if you need managed services |
| Cost (scale, 50 vehicles) | $2,000-5,000/mo | $300-800/mo + more ops effort | Hetzner saves 60-70% but you manage more yourself |
| Managed services | RDS, MSK, ElastiCache, S3, CloudWatch, IAM | None (self-managed VPS + block storage) | AWS if team < 3; Hetzner if team has strong DevOps person |
| Compliance (FedRAMP, SOC 2) | Full compliance certifications available | No formal compliance certs | AWS mandatory if pursuing government/enterprise contracts |
| Geographic presence | 25+ regions worldwide | EU + US (limited) | AWS for multi-region; Hetzner fine for single region |
| Edge / IoT integration | AWS IoT Core, Greengrass for edge nodes | WireGuard VPN to Hetzner VPS | AWS IoT Core simplifies edge management significantly |
| Reliability (SLA) | 99.99% compute SLA with multi-AZ | 99.9% SLA; single-DC risk | AWS for production safety-critical workloads |
| Vendor lock-in risk | Medium-High (managed services create dependencies) | Low (standard Linux VPS, portable) | Hetzner for maximum portability |
3.2 Recommended AWS Architecture (MVP)
| Service | AWS Product | Sizing | Monthly Cost | Purpose |
| Compute | ECS Fargate (or EC2 t3.medium) | 2 vCPU, 4 GB (auto-scale to 4 tasks) | $30-60 | Backend services in containers |
| Database | RDS PostgreSQL (db.t3.micro) | 2 vCPU, 1 GB, 20 GB SSD, Multi-AZ | $25-50 | Mission state, fleet, compliance, audit |
| Time-series | TimescaleDB on EC2 (t3.small) | 2 vCPU, 2 GB, 100 GB SSD | $20-30 | Telemetry storage (or use TimescaleDB Cloud $29/mo) |
| Cache | ElastiCache Redis (cache.t3.micro) | Single node, 0.5 GB | $12 | Real-time telemetry, session cache |
| Message queue | Amazon MQ (RabbitMQ) or SQS | Single broker, t3.micro | $15-25 | Event pub/sub (Kafka overkill at MVP) |
| Object storage | S3 Standard | 50 GB initial | $1 | Flight logs, imagery, reports, backups |
| CDN | CloudFront | Standard tier | $1-5 | Static assets, map tiles |
| Secrets | AWS Secrets Manager | 10 secrets | $4 | API keys, DB credentials, cert material |
| DNS | Route 53 | 1 hosted zone | $0.50 | Domain management |
| Monitoring | CloudWatch (basic) | Standard metrics + 5 custom dashboards | $0-10 | Infra monitoring (supplement with Grafana Cloud) |
Total AWS MVP: ~$110-195/month. Scales to ~$2,000-5,000/month at 50 vehicles without re-architecting.
3.3 Recommended Hetzner Architecture (Budget)
| Service | Product | Spec | Monthly Cost | Purpose |
| App server | CX31 Cloud VPS | 4 vCPU, 8 GB RAM, 80 GB SSD | $8 | All backend services (Docker Compose) |
| Database server | CX21 Cloud VPS | 2 vCPU, 4 GB RAM, 40 GB SSD | $5 | PostgreSQL + TimescaleDB |
| Block storage | Volume | 100 GB | $5 | Database storage, logs |
| Object storage | Hetzner Object Storage (S3-compat) | 50 GB | $1 | Flight imagery, reports, backups |
| Backup | Hetzner Backup | Automated daily snapshots | $2 | Full server backup |
| Firewall | Hetzner Cloud Firewall | Standard rules | $0 (free) | Network security |
Total Hetzner MVP: ~$21/month. Add Cloudflare ($0 free tier) for CDN/DNS/DDoS protection. Total: ~$25-35/month.
4. BACKEND FRAMEWORK
4.1 Primary: Go + Fiber + gRPC
| Dimension | Go (Recommended) | Node.js / TypeScript (Alternative) | When to Choose Alternative |
| Performance | Compiled, 10-100x faster than Node for compute-heavy tasks (telemetry processing, geofence math) | V8 JIT is fast enough for most API workloads | If your team is 100% TypeScript and hiring Go devs is impossible |
| Concurrency | Goroutines: lightweight, built-in, handles 100K+ concurrent connections trivially | Event loop + worker threads; async/await; good but requires discipline | If team is deeply experienced with Node async patterns |
| Memory | ~10-50 MB per service (important for edge nodes / Jetson) | ~80-200 MB per service (Node runtime overhead) | If memory is not a constraint (cloud-only deployment) |
| Type safety | Strong static typing catches bugs at compile time | TypeScript provides types but runtime is still JS; type erasure at runtime | If rapid prototyping speed matters more than runtime safety |
| Ecosystem (drone) | MAVLink libraries exist in Go; Skydio SDK is gRPC (native Go fit); ArduPilot tools are C++/Python | MAVLink better supported in Python/C++; REST wrappers fine from Node | If heavy Python ML integration needed (Go calls Python via gRPC) |
| Deployment | Single static binary; tiny Docker images (~10 MB); instant startup | node_modules; larger images (~200+ MB); slower cold start | If using serverless (Node Lambda cold starts are acceptable) |
| Hiring pool | Smaller but growing; Go devs tend to be systems-oriented | Massive pool; easier to hire | If hiring quickly is the priority |
| Learning curve | 1-2 weeks for experienced developers; simple language | Immediate if team knows JS/TS | If timeline is < 4 weeks and team has no Go experience |
4.2 Service Architecture
| Service | Framework | Transport | Key Libraries | Lines (Est.) |
| api-gateway | Fiber (Go HTTP) | REST + WebSocket | fiber, jwt-go, rate-limiter, cors | 2,000 |
| mission-engine | Fiber + gRPC server | REST (external) + gRPC (internal) | fiber, grpc-go, protobuf, fsm (state machine) | 8,000 |
| fleet-manager | Fiber + gRPC server | REST + gRPC | fiber, grpc-go, cron (scheduled health checks) | 5,000 |
| compliance-service | Fiber + gRPC server | REST + gRPC | fiber, grpc-go, opa-go (embedded OPA) | 4,000 |
| telemetry-service | gRPC server + Kafka consumer | gRPC + Kafka + WebSocket | grpc-go, sarama (Kafka), gorilla/websocket | 4,000 |
| vehicle-adapter | gRPC server | gRPC + MAVLink + vendor SDK | grpc-go, gomavlib (MAVLink), Skydio SDK client | 6,000 |
| ai-service | Python FastAPI | REST (internal only) | fastapi, anthropic SDK, pydantic, numpy | 3,000 |
| report-generator | Fiber | REST (internal) | fiber, go-pdf, chromedp (HTML-to-PDF) | 2,000 |
Total backend: ~34,000 lines of Go + ~3,000 lines of Python. One senior Go developer can maintain this.
4.3 Key Go Libraries
| Library | Purpose | Why This One |
| gofiber/fiber | HTTP framework | Express-like API but 10x faster; excellent middleware ecosystem; great docs |
| grpc-go | Inter-service RPC | Industry standard; protobuf schema enforcement; streaming for telemetry; native fit for Skydio SDK |
| gomavlib | MAVLink 2.0 protocol | Pure Go MAVLink library; encode/decode all message types; serial + UDP + TCP transports |
| sarama | Kafka client | Most mature Go Kafka client; supports consumer groups, exactly-once |
| pgx | PostgreSQL driver | Fastest Go Postgres driver; native connection pooling; COPY support for bulk inserts |
| opa-go | Policy engine | Embedded Open Policy Agent; evaluate Part 107 rules without network call |
| looplab/fsm | State machines | Clean finite state machine library for mission and dock lifecycle |
| gorilla/websocket | WebSocket server | Battle-tested; handles telemetry streaming to frontend |
| zap | Structured logging | Uber’s high-performance logger; JSON output for Loki/Grafana ingestion |
| otel | OpenTelemetry SDK | Distributed tracing; metrics; vendor-neutral observability |
5. FRONTEND INTERFACE
5.1 Primary: Next.js 14 + Tailwind CSS + shadcn/ui
| Dimension | Specification | Rationale |
| Framework | Next.js 14 (App Router, React Server Components) | SSR for fast initial load; RSC for reduced client JS; API routes for lightweight BFF; Vercel deployment is zero-config |
| Styling | Tailwind CSS 3.4 + shadcn/ui | Utility-first eliminates CSS architecture decisions; shadcn/ui provides accessible, unstyled components you own (not a dependency) |
| State management | Zustand (global) + React Query (server state) | Zustand is 1 KB, no boilerplate; React Query handles caching, revalidation, optimistic updates for API data |
| Map engine | MapLibre GL JS 4.x (open-source Mapbox fork) | Free, no API key, no usage fees; WebGL-accelerated; PMTiles for self-hosted vector tiles |
| 3D / advanced viz | Deck.gl (on top of MapLibre) | GPU-accelerated layers for flight paths, heatmaps, 3D airspace volumes; Uber-proven at scale |
| Charts | Recharts (simple) + Plotly.js (complex) | Recharts for KPI cards and sparklines; Plotly for interactive telemetry charts with zoom/pan |
| Real-time | Native WebSocket + React Query subscriptions | WebSocket for telemetry stream; React Query for polling fleet status; no heavy lib needed |
| PDF generation | @react-pdf/renderer | Client-side PDF for mission reports; same React components render on screen and in PDF |
| Forms | React Hook Form + Zod validation | RHF for performance (uncontrolled); Zod for schema validation shared with backend |
| Auth UI | Clerk components (drop-in) | Pre-built sign-in, user management, role display; matches Clerk backend auth |
5.2 Map Tile Strategy (Zero Cost)
| Component | Solution | Cost | Notes |
| Vector tiles | OpenMapTiles + PMTiles format | $0 | Download region, convert to PMTiles, host on R2/S3; no tile server needed |
| Satellite imagery | USGS/Sentinel-2 (public domain) or MapTiler free tier | $0-50/mo | Public imagery for planning; MapTiler for higher-res if needed |
| Terrain / elevation | Mapzen Terrain Tiles (open, PMTiles) | $0 | 3D terrain for airspace visualization |
| Airspace boundaries | FAA UAS Facility Maps (public GeoJSON) | $0 | Overlay controlled airspace, TFRs; update weekly from FAA API |
| Custom overlays | GeoJSON layers (flight paths, geofences, dock locations) | $0 | Generated from your data; rendered client-side by MapLibre |
5.3 UI Component Architecture
| Component | Type | Data Source | Update Pattern |
| TacticalMap | Page (full-screen with overlays) | WebSocket (vehicles), REST (airspace, geofences), PMTiles (base map) | Vehicle positions: 2-10 Hz via WS; airspace: on-load + 5 min refresh |
| MissionPanel | Drawer (right side) | REST (mission CRUD), WebSocket (status updates) | Optimistic updates on user action; WS for external state changes |
| FleetBoard | Page (card grid) | React Query polling /api/fleet/vehicles every 5s | Polling; could upgrade to WS if latency matters |
| AlertCenter | Persistent overlay (bottom-right) | WebSocket (alert stream) | Push: alerts appear immediately; user acks via REST |
| TelemetryChart | Panel (within mission detail) | WebSocket (raw telemetry) | Streaming: ring buffer of last 300 points; chart redraws at 2 Hz |
| AuditExplorer | Page (table + timeline) | REST with pagination + filters | On-demand; no real-time needed |
| WeatherWidget | Widget (top bar) | REST polling /api/weather every 60s | Polling; low frequency |
| ReportViewer | Modal (PDF preview) | REST (fetch generated PDF) | On-demand; cached after first load |
6. DRONE INTEGRATION (US-MANUFACTURED & OPEN SOURCE)
6.1 Primary Platform: Skydio X10
| Attribute | Specification | Advantage for SkyCommand |
| Manufacturer | Skydio (San Mateo, CA, USA) | US-manufactured; Blue UAS approved; zero CCP ban risk; eligible for all federal contracts |
| Airframe | Skydio X10 | Enterprise-grade; dual visual + thermal cameras; 35+ min flight time; IP55 weather resistance |
| Autonomy | Skydio Autonomy Engine (on-device AI) | Best-in-class obstacle avoidance; autonomous navigation; reduces pilot workload and enables BVLOS path |
| SDK | Skydio SDK (gRPC + REST) | Native gRPC = perfect fit for Go backend; well-documented; local data processing (no cloud dependency) |
| Dock | Skydio Dock | Automated launch, land, charge; weather-hardened; designed for X10; US-manufactured |
| Data handling | On-device processing; optional Skydio Cloud (US-hosted) or fully on-prem | No data leaves your network if desired; eliminates data sovereignty concerns |
| Blue UAS status | Approved | Required for DoD, DHS, DOI, and many state/local government contracts |
| Pricing | ~$11,000-14,000 (drone) + ~$10,000-15,000 (dock) | Comparable to DJI Dock 2 + M350; slightly higher upfront but eliminates regulatory risk |
| Support | US-based engineering support; enterprise SLAs available | No timezone/language barriers; responsive to integration questions |
6.2 Secondary Platform: ArduPilot / PX4 Custom Build
| Attribute | Specification | Advantage for SkyCommand |
| Flight controller | Cube Orange+ (HEX/ProfiCNC, manufactured in Australia) or Holybro Pixhawk 6X | Open-source hardware; multiple vendors; no single-vendor dependency; extensive community |
| Airframe | Freefly Alta X (US) or custom hex/quad from US frame manufacturers | US-manufactured frames available; custom sensor payloads; fully configurable |
| Firmware | ArduPilot 4.5+ (open source, GPLv3) | Fully auditable source code; community of thousands; 15+ years of development; US-based core team |
| Communication | MAVLink 2.0 over serial, UDP, TCP | Universal protocol; gomavlib (Go) for integration; works with any GCS |
| Dock | Custom integration via Valqari or DroneShield Nest or custom-built | Open design; no vendor lock-in; can integrate with any ArduPilot vehicle |
| Data handling | Fully self-hosted; all data stays on your infrastructure | Complete data sovereignty; no third-party cloud; log everything locally |
| Regulatory status | Not platform-specific; compliance depends on your build and registration | Flexible; can be configured to meet any standard; FAA treats as custom UAS |
| Pricing | $5,000-15,000 (complete build depending on sensors/frame) | Lower cost per unit; higher integration effort; ideal for volume deployments |
| Best for | High-volume fleets, specialized payloads, maximum customization, BVLOS research | When you need 10+ vehicles and want to control every aspect of the hardware stack |
6.3 Blue UAS Approved Alternatives
| Manufacturer | Model | Category | Country | Blue UAS | Best For | Price Range |
| Skydio | X10 | Multi-rotor | USA | Yes | Primary platform; enterprise inspection, DFR, security | $11K-14K |
| Skydio | X2E | Multi-rotor | USA | Yes | Budget option; lighter missions; legacy but still supported | $6K-8K |
| Inspired Flight | IF1200A | Heavy-lift hex | USA | Yes | Large payloads (LiDAR, cinema cameras); long endurance | $20K-30K |
| Teal Drones | Golden Eagle 2 | Multi-rotor | USA (FLIR subsidiary) | Yes | Defense/security; thermal-first; ruggedized | $15K-20K |
| Parrot | ANAFI USA | Multi-rotor | France (NATO ally) | Yes | Lightweight; 32-min flight; 3 cameras; budget enterprise | $7K-9K |
| Vantage Robotics | Vesper | Multi-rotor | USA | Yes | Ultra-safe (enclosed rotors); indoor/confined space operations | $5K-8K |
| Altavian | Nova F7200 | Fixed-wing | USA | Yes | Long-range mapping/survey (60+ min endurance); BVLOS-ready | $25K-40K |
| Harris Aerial | H6 Hybrid | VTOL/hybrid | USA | Yes | Extended range (120+ min); hybrid gas-electric; infrastructure inspection | $30K-50K |
All above platforms can be integrated via MAVLink or vendor-specific SDK. The Vehicle Abstraction Layer (VAL) pattern means adding any platform requires only a new adapter module.
6.4 Vehicle Abstraction Layer (VAL) Interface
All vehicle communication flows through a canonical gRPC interface. Adding a new vehicle type means writing one adapter file, not touching core services.
| gRPC Method | Direction | Parameters | Returns |
| Connect(vehicle_id) | Client -> VAL | Vehicle ID, connection config | Connection status stream |
| ExecuteCommand(cmd) | Client -> VAL | Command enum + params (ARM, TAKEOFF, GOTO, ORBIT, HOLD, RTL, LAND, DISARM, TERMINATE) | Command ACK with vehicle response |
| StreamTelemetry(vehicle_id) | VAL -> Client (server-stream) | Vehicle ID, rate_hz | Continuous telemetry frames at requested rate |
| GetVehicleInfo(vehicle_id) | Client -> VAL | Vehicle ID | Static info: model, serial, firmware, capabilities |
| GetVehicleStatus(vehicle_id) | Client -> VAL | Vehicle ID | Current status: battery, GPS, IMU, flight mode, Remote ID |
| StreamAlerts(vehicle_id) | VAL -> Client (server-stream) | Vehicle ID | Alert stream: lost link, low battery, geofence approach, hardware fault |
6.5 Skydio SDK Integration Detail
| Feature | Skydio SDK Method | Your System Action | Notes |
| Vehicle discovery | gRPC: VehicleService.ListVehicles | Register vehicles in FIM; update status to READY | Discovers all Skydio vehicles on network |
| Telemetry | gRPC: TelemetryService.Subscribe | Parse, normalize, publish to Kafka telemetry.raw | Native gRPC stream; 10-30 Hz |
| Flight plan upload | gRPC: MissionService.UploadMission | MCE sends mission plan -> Skydio SDK -> Vehicle | Waypoint format; supports orbit, survey patterns |
| Flight control | gRPC: FlightService.SendCommand | Direct commands: takeoff, RTL, hover, land | Used for operator overrides; low latency |
| Media download | REST: GET /media/files/{id} | Pull photos/video after mission for report generation | Can also stream live during flight |
| Dock control | gRPC: DockService.SendCommand | Open/close dock, initiate charge, run diagnostics | Skydio Dock native integration |
| Autonomy features | gRPC: SkillService.Execute | Trigger autonomous behaviors: 3D Scan, Inspect, Track | Skydio Autonomy Engine runs on-device; unique advantage |
| Firmware management | REST: PATCH /devices/{id}/firmware | Scheduled OTA updates during maintenance windows | Never during operations; gated by MCE |
6.6 ArduPilot / MAVLink Integration Detail
| Feature | MAVLink Message / Protocol | Your System Action | Notes |
| Heartbeat | HEARTBEAT (msg #0) | Monitor vehicle online status; detect lost link if heartbeat stops | 1 Hz; fundamental liveness signal |
| Telemetry (position) | GLOBAL_POSITION_INT (msg #33) | Parse lat/lng/alt, publish to Kafka telemetry.raw | 10 Hz typical; primary position source |
| Telemetry (attitude) | ATTITUDE (msg #30) | Roll/pitch/yaw for flight dynamics display | 10 Hz; useful for anomaly detection |
| Telemetry (battery) | SYS_STATUS (msg #1) + BATTERY_STATUS (msg #147) | Battery SoC, voltage, current; publish to FIM | 1 Hz; critical for readiness gating |
| Command (arm) | COMMAND_LONG (cmd #400, MAV_CMD_COMPONENT_ARM_DISARM) | Arm/disarm motors | Requires safety switch or param override |
| Command (takeoff) | COMMAND_LONG (cmd #22, MAV_CMD_NAV_TAKEOFF) | Initiate takeoff to specified altitude | Vehicle must be armed first |
| Command (waypoint) | MISSION_ITEM_INT (msg #73) sequence | Upload mission waypoints; vehicle follows autonomously | Use MISSION_COUNT -> MISSION_ITEM_INT sequence |
| Command (RTL) | SET_MODE (msg #11) to RTL mode | Return to launch; vehicle navigates home autonomously | Also triggered automatically on lost link |
| Command (land) | COMMAND_LONG (cmd #21, MAV_CMD_NAV_LAND) | Precision land at specified coordinates or current position | Integrates with IR precision landing systems |
| Remote ID | OPEN_DRONE_ID_* messages (msg #12900-12904) | Verify Remote ID broadcast; log for compliance | ArduPilot 4.4+ supports Open Drone ID natively |
7. MAPPING SOFTWARE
7.1 Complete Mapping Stack
| Layer | Technology | Purpose | Cost | Alternative |
| Map renderer | MapLibre GL JS 4.x | WebGL-accelerated vector map rendering in browser | $0 (open source, BSD) | Mapbox GL JS ($0.60/1K loads after free tier) |
| Vector tiles (base map) | OpenMapTiles + PMTiles | Streets, buildings, land use, water, POIs | $0 (download + self-host on R2) | MapTiler Cloud ($0-100/mo) |
| Satellite / aerial | USGS NAIP (US) + Sentinel-2 (global) | High-res imagery for site planning and post-flight review | $0 (public domain) | Nearmap ($500+/mo), Google Earth ($) |
| Terrain / elevation | Mapzen Terrain Tiles (PMTiles) | 3D terrain visualization, line-of-sight analysis | $0 (open data) | Mapbox Terrain ($) |
| Airspace data | FAA UAS Facility Maps + TFR feed | Controlled airspace boundaries, altitude ceilings, temporary restrictions | $0 (public FAA API) | Aloft API ($30/mo for enhanced data) |
| Flight path rendering | Deck.gl LineLayer + IconLayer | Real-time vehicle tracks, planned routes, historical paths | $0 (open source) | Custom MapLibre layers (also $0) |
| 3D airspace volumes | Deck.gl PolygonLayer (extruded) | Operational volumes, conflict zones, geofences visualized in 3D | $0 | CesiumJS (heavier but more 3D features) |
| Geocoding | Nominatim (self-hosted or public) | Address search for mission planning | $0 | Google Geocoding ($5/1K requests) |
| Tile hosting | Cloudflare R2 + Workers | Serve PMTiles with range requests; global CDN; zero egress fees | $0-5/mo | AWS S3 + CloudFront ($5-20/mo) |
| Offline tiles | PMTiles extract for operating area | Pre-download tiles for field use when connectivity is poor | $0 | MBTiles + local tile server |
| Post-flight mapping | OpenDroneMap (open source) | Stitch aerial photos into orthomosaics, 3D models, point clouds | $0 (self-hosted) | Pix4D ($350/mo), DroneDeploy ($300/mo) |
Total mapping cost: $0-5/month. Open-source maps and processing tools are now production-grade.
7.2 Geospatial Processing
| Task | Tool | Usage | Integration |
| Geofence math (point-in-polygon) | Turf.js (browser) + S2 geometry (Go) | Real-time geofence evaluation for every telemetry frame | Turf.js in frontend for display; S2 in backend for authoritative checks |
| Route distance / bearing | S2 geometry (Go) | Mission planning: distance, duration estimates, waypoint spacing | Backend calculation; results sent to frontend for display |
| Airspace intersection | PostGIS (PostgreSQL extension) | Check if planned route intersects controlled airspace or TFRs | SQL query: ST_Intersects(route_geom, airspace_geom) |
| Terrain elevation lookup | GDAL + DEM tiles | Calculate AGL from MSL altitude using digital elevation model | Backend service; called during mission planning |
| Orthomosaic generation | OpenDroneMap (open source) | Post-flight: stitch photos into georeferenced map | Async job; results stored in R2; displayed as map overlay |
| Wind field visualization | Custom WebGL shader on MapLibre | Animated wind particles showing current conditions over operating area | Browser-side rendering from weather API data |
8. DATABASES
8.1 Database Architecture
| Database | Engine | Hosting | Purpose | Data Lifecycle |
| Operations DB | PostgreSQL 16 | Supabase (MVP) or AWS RDS (scale) | Missions, fleet, compliance, pilots, clients, invoices | 7 year retention (FAA); daily backup |
| Telemetry DB | TimescaleDB 2.x | TimescaleDB Cloud (MVP) or self-hosted (scale) | 50 Hz vehicle telemetry, sensor data, ADS-B tracks | 30 days hot, 1 year compressed, 3 years cold (S3) |
| Audit DB | PostgreSQL 16 (append-only) | Same instance as Ops DB (separate schema) | Immutable audit log with SHA-256 hash chain | 7 years minimum; never deleted |
| Cache | Redis 7.x (or Valkey) | Upstash (MVP) or ElastiCache (scale) | Real-time telemetry, session state, rate limit counters | Ephemeral; no backup needed |
| Search | PostgreSQL full-text search (MVP) or Meilisearch (scale) | Embedded (MVP) or managed (scale) | Mission search, audit search, glossary | Rebuilt from primary DB on demand |
| Object store | S3-compatible (R2) | Cloudflare R2 | Flight imagery, PDFs, map tiles, backups, cold telemetry | Lifecycle: hot (30d) -> archive (3y) -> delete |
8.2 PostgreSQL Schema Design Principles
- UUID primary keys everywhere: enables distributed ID generation; no sequence contention; merge-friendly across sites
- JSONB for flexible fields: vehicle config, mission route, telemetry summary. Indexed with GIN for fast queries
- PostGIS for geospatial: ST_Point for locations, ST_LineString for routes, ST_Polygon for geofences and airspace
- Row-Level Security (RLS) for multi-tenancy: tenant_id on every table; RLS policies enforce isolation at the database level
- Partitioning: audit_log partitioned by month; large tables partitioned by created_at for faster queries and easier archival
- Soft deletes (status = ARCHIVED): never physically delete operational data; FAA may ask for records years later
- Change Data Capture: Supabase Realtime or PostgreSQL logical replication to stream changes to Kafka for event-driven architecture
8.3 TimescaleDB Configuration
| Parameter | MVP Setting | Scale Setting | Rationale |
| Chunk interval | 1 hour | 15 minutes | Smaller chunks at scale for faster queries and parallel compression |
| Compression | After 1 day | After 2 hours | Compress early to save storage; 90%+ compression ratio on telemetry |
| Retention (raw) | 30 days | 30 days | Raw 50 Hz data is large; 30 days is sufficient for incident review |
| Continuous aggregate | 1-minute rollup | 1-minute + 5-minute + 1-hour | Multi-level aggregates for dashboard performance at scale |
| Retention (aggregates) | 1 year | 3 years | Aggregates are small; keep for trend analysis and reporting |
| Replication | None (MVP) | Streaming replication to read replica | Read replica for dashboard queries; primary for writes only |
| Connection pooling | Supabase pooler (MVP) or PgBouncer | PgBouncer (transaction mode) | 50 Hz writes need connection pooling to avoid connection exhaustion |
9. AUTOMATION AND CI/CD
9.1 CI/CD Pipeline: GitHub Actions
| Stage | Trigger | Actions | Duration | Cost |
| Lint + Format | Every push | golangci-lint, eslint, prettier, protobuf lint | 1-2 min | $0 (free tier) |
| Unit Test | Every push | go test ./..., jest, opa test | 2-4 min | $0 |
| Build | PR to main | Docker build per changed service (multi-stage, cached) | 3-5 min | $0 |
| Integration Test | PR to main | Docker Compose up full stack + run API integration suite | 5-10 min | $0-5 (runner minutes) |
| Security Scan | PR to main | Trivy (container), gosec (Go SAST), npm audit (frontend) | 2-3 min | $0 |
| Deploy to Staging | Merge to main | Push images to GHCR; deploy to staging (ECS or K3s) | 3-5 min | $0 |
| Deploy to Production | Manual approval tag | Rolling update to production; health check; auto-rollback on failure | 5-8 min | $0 |
Total CI/CD cost: $0/month on GitHub Actions free tier (2,000 minutes/month). Sufficient for a 2-4 person team.
9.2 Infrastructure as Code
| Tool | Purpose | Why This One |
| Terraform | Cloud infrastructure provisioning (AWS/Hetzner resources) | Declarative; state management; drift detection; massive provider ecosystem |
| Docker + Docker Compose | Local development + MVP deployment | Every developer runs the full stack locally; Compose is the MVP production deployment |
| Kubernetes (K3s) | Scale deployment (Phase 2+) | Lightweight K8s; runs on a single node; upgrades to multi-node seamlessly |
| GitHub Actions | CI/CD orchestration | Free; YAML-based; integrates with GHCR, AWS, notifications |
| Renovate Bot | Dependency updates | Auto-creates PRs for dependency updates; security patches applied within 24 hours |
| Doppler or dotenv-vault | Secret management (MVP) | Sync secrets across dev/staging/prod; cheaper than HashiCorp Vault for small teams |
9.3 Operational Automation
| Automation | Tool | Trigger | Action |
| Database backup | pg_dump + cron + S3 upload | Daily 02:00 UTC | Full backup to S3; retain 30 daily + 12 monthly |
| Telemetry archival | Custom Go job + S3 | Daily 03:00 UTC | Compress and archive telemetry older than 30 days to S3 cold storage |
| SSL cert renewal | Caddy or Let’s Encrypt certbot | Auto (60 day cycle) | Zero-downtime cert rotation |
| Health check alerting | UptimeRobot or Better Stack | Every 60 seconds | Ping all endpoints; alert via SMS/Slack/email on failure |
| Log rotation | logrotate + Loki ingestion | Daily | Compress logs older than 7 days; ship to Loki for searchable retention |
| Dependency security scan | GitHub Dependabot + Renovate | On new CVE publication | Auto-PR for security patches; Slack notification |
| Database migration | golang-migrate in CI/CD | On deploy (if new migration exists) | Forward-only migrations; tested in staging before production |
| Fleet health digest | Custom Go cron job | Daily 07:00 local | Email/Slack summary: fleet status, upcoming maintenance, battery health |
10. MONITORING AND OBSERVABILITY
10.1 Monitoring Stack
| Layer | Tool | Purpose | Cost (MVP) | Cost (Scale) |
| Metrics | Grafana Cloud (Prometheus-compatible) | System metrics (CPU, memory, disk), app metrics (request rate, latency, error rate), business metrics (missions/day, fleet utilization) | $0 (free: 10K series) | $50-200/mo |
| Logs | Grafana Loki | Structured JSON logs from all services; searchable by service, level, trace ID, mission ID | $0 (free: 50 GB/mo) | $50-150/mo |
| Traces | Grafana Tempo | Distributed tracing across services; trace a mission request from UI through every backend service | $0 (free: 50 GB/mo) | $20-50/mo |
| Uptime | Better Stack (formerly Better Uptime) | External ping monitoring; status page; incident management; on-call scheduling | $0 (free tier) | $25-85/mo |
| Error tracking | Sentry | Frontend and backend exception tracking with stack traces, breadcrumbs, release tracking | $0 (free: 5K events/mo) | $26-80/mo |
| APM (optional) | Grafana Cloud APM | Application performance monitoring; flame graphs; query analysis | $0 (included in free) | $50-100/mo |
Total monitoring MVP: $0/month. Grafana Cloud free tier is remarkably generous for a small team.
10.2 Critical Dashboards
| Dashboard | Panels | Alert Threshold | Notification Channel |
| System Health | CPU%, memory%, disk%, network I/O per service; pod restart count | CPU >80% for 5 min; memory >85%; disk >90%; restart count >2 | Slack #ops-alerts + SMS to on-call |
| Telemetry Pipeline | Kafka consumer lag, messages/sec, TSDB write latency, dropped messages | Consumer lag >1000; write latency >500 ms; any dropped messages | Slack #ops-alerts (immediate) |
| API Performance | Request rate, p50/p95/p99 latency, error rate (4xx, 5xx), active WebSocket connections | p99 >500 ms; error rate >1%; WebSocket drops >5/min | Slack #ops-alerts |
| Mission Operations | Active missions, mission state distribution, avg time-to-launch, abort rate | Abort rate >10% over 24 hrs; zero active missions during business hours (unexpected) | Slack #ops-alerts + email to ops lead |
| Fleet Health | Vehicle status distribution, battery health trend, maintenance overdue count, uptime | Any vehicle overdue for maintenance; battery below 80% health; dock in FAULT state | Slack #fleet-alerts + email |
| Safety | Safety alerts per hour, geofence violations, lost-link events, emergency overrides | Any EMERGENCY alert; geofence violation; lost link >30 sec | SMS + phone call to on-call + Slack #safety-critical |
| Business | Missions completed/day, revenue/week, client satisfaction, cost per flight hour | Revenue below 7-day average by >30% (demand drop signal) | Weekly email digest |
10.3 On-Call and Incident Response
| Severity | Definition | Response Time | Who | Action |
| SEV-1 (Critical) | Safety incident, vehicle lost, system down during active flight | Immediate (< 5 min) | Both founders | All hands; ground all flights; incident commander declared; post-incident review within 24 hrs |
| SEV-2 (Major) | Core service down, telemetry pipeline stalled, compliance system offline | < 15 min | On-call engineer | Investigate and restore; consider grounding flights if safety-relevant; RCA within 48 hrs |
| SEV-3 (Minor) | Dashboard slow, non-critical feature broken, intermittent errors | < 2 hours | On-call engineer | Investigate during business hours; fix in next deploy; no client impact |
| SEV-4 (Low) | Cosmetic UI bug, log noise, non-urgent maintenance item | Next business day | Whoever is available | Add to backlog; fix in normal sprint cycle |
10.4 Hardware Supply Chain Monitoring
Given the regulatory landscape around drone hardware, maintain a supply chain dashboard:
- Track legislative status of Countering CCP Drones Act and state-level drone bans; alert team on any movement
- Maintain relationships with 2+ Blue UAS vendors to avoid single-vendor dependency
- Keep 90-day spare parts inventory for primary platform (Skydio X10 batteries, propellers, cameras)
- Monitor Skydio financial health and acquisition risk; ArduPilot custom builds are the ultimate hedge
- Document all hardware serial numbers, firmware versions, and country of origin for compliance audits
- Review Blue UAS list quarterly for new approved platforms that may offer better price/performance
END OF DOCUMENT
SkyCommand Technology Stack (US-Manufactured / Open-Source Edition) — v2.0