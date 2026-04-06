# SkyCommand — Platform Architecture
*Notion backup — 2026-04-06*

SKYCOMMAND
DRONE OPERATIONS PLATFORM
Full Platform Architecture & Systems Engineering Specification
From KLFT Concept to Generalizable Product
System Components • Software Modules • Data Flow • AI Agents • UI Layers
Cloud Infrastructure • Hardware Integration • Command Center • Security • Scalability
Document Version: 1.0 | February 2026
ENGINEERING SPECIFICATION
1. SYSTEM COMPONENTS
SkyCommand is a full-stack autonomous drone operations platform architected as a modular, microservices-based system. It generalizes the KLFT single-site architecture into a multi-site, multi-tenant product deployable as on-premises, cloud, or hybrid.
1.1 Component Inventory
| Component ID | Component Name | Category | Deployment | Description |
| SC-CORE-01 | Mission Control Engine (MCE) | Core | Server / Cloud | Central orchestrator: mission lifecycle, state machines, sequencing, priority resolution, multi-mission coordination |
| SC-CORE-02 | Fleet Intelligence Manager (FIM) | Core | Server / Cloud | Vehicle registry, health monitoring, predictive maintenance, battery lifecycle, readiness gating |
| SC-CORE-03 | Compliance & Authorization Service (CAS) | Core | Server / Cloud | Regulatory rule engine (Part 107/108, EU regs), LAANC integration, waiver management, audit trail |
| SC-CORE-04 | Airspace Awareness Engine (AAE) | Core | Server / Cloud | 4D airspace model, traffic deconfliction, operational volume management, ADS-B integration |
| SC-CORE-05 | Telemetry Data Engine (TDE) | Core | Server / Cloud | High-throughput ingest (50 Hz per vehicle), time-series storage, real-time streaming, anomaly detection |
| SC-CORE-06 | Safety Supervisor (SS) | Safety-Critical | Dedicated HW | Independent safety monitor: geofence enforcement, envelope protection, deterministic failsafe, RF override |
| SC-EDGE-01 | Vehicle Abstraction Layer (VAL) | Edge | Edge Node | Protocol adapter per vehicle type (DJI, Skydio, MAVLink, custom), canonical command/telemetry interface |
| SC-EDGE-02 | Dock Controller | Edge | Edge Node | Dock lifecycle management, battery swap sequencing, weather sensor interface, local autonomy on link loss |
| SC-EDGE-03 | Sensor Fusion Hub | Edge | Edge Node | ADS-B receiver, Remote ID receiver, weather station, PTZ camera feeds — fused into unified sensor stream |
| SC-UI-01 | Command Center Interface | UI | Browser / Desktop | Operator workspace: live map, mission management, alerts, telemetry panels, multi-vehicle situational awareness |
| SC-UI-02 | Field Operations App | UI | Mobile (iOS/Android) | Field crew app: dock status, vehicle check-in, maintenance logging, emergency override |
| SC-UI-03 | Executive Dashboard | UI | Browser | High-level KPIs: fleet utilization, mission success rate, compliance score, cost per flight hour |
| SC-INFRA-01 | API Gateway & Auth | Infrastructure | Server / Cloud | Kong/Traefik: rate limiting, JWT auth, RBAC, API versioning, webhook management |
| SC-INFRA-02 | Event Bus (Kafka) | Infrastructure | Server / Cloud | Pub/sub backbone: telemetry, mission events, alerts, audit events, vehicle status, dock status |
| SC-INFRA-03 | Data Platform | Infrastructure | Server / Cloud | PostgreSQL (state), TimescaleDB (telemetry), Redis (hot cache), S3-compatible (cold archive) |
| SC-INFRA-04 | Observability Stack | Infrastructure | Server / Cloud | Prometheus metrics, Grafana dashboards, structured logging (Loki), distributed tracing (Jaeger) |
| SC-AI-01 | AI Agent Cluster | Intelligence | Server / GPU | ML models for route optimization, anomaly detection, predictive maintenance, demand forecasting |
1.2 Deployment Topology
| Deployment Model | Use Case | Components at Site | Cloud Components |
| On-Premises (Air-Gapped) | Military, high-security, no internet | All SC-CORE, SC-EDGE, SC-UI, SC-INFRA, SC-AI on local servers | None |
| Hybrid (Primary) | Enterprise drone programs, airports | SC-EDGE on-site; SC-CORE/SC-INFRA in private cloud; SC-UI anywhere | SC-CORE, SC-INFRA, SC-AI |
| Fully Cloud | Small operators, SaaS customers | SC-EDGE at dock sites only (minimal compute) | Everything except SC-EDGE |
| Multi-Site Federated | Regional drone networks | SC-EDGE per site; shared SC-CORE; federated AAE across sites | Shared control plane |
2. SOFTWARE MODULES
2.1 Module Decomposition
| Module | Language | Framework | Internal Services | Lines (Est.) |
| mission-control-engine | Go 1.22+ | gRPC + REST | MissionDispatcher, MissionScheduler, PriorityResolver, StateManager | 15,000 |
| fleet-intelligence | Go 1.22+ | gRPC + REST | VehicleRegistry, HealthMonitor, ReadinessGate, MaintenancePredictor, BatteryLifecycle | 12,000 |
| compliance-auth | Go 1.22+ | gRPC + OPA | RuleEngine, LaancClient, WaiverManager, AuditLogger, RegulationAdapter | 10,000 |
| airspace-engine | Go / Rust | gRPC + shared mem | AirspaceModel, ConflictDetector, VolumeManager, TrafficTracker, WellClearEval | 18,000 |
| telemetry-engine | Go / Rust | Kafka + TSDB | Ingestor, Processor, Anomaly Detector, StreamPublisher, Archiver | 8,000 |
| safety-supervisor | Rust | Bare-metal / RTOS | EnvelopeMonitor, GeofenceEnforcer, FailsafeController, RFCommander, Watchdog | 6,000 |
| vehicle-abstraction | Go / Rust | gRPC | DJIAdapter, SkydioAdapter, MAVLinkAdapter, GenericAdapter, CommandTranslator | 10,000 |
| dock-controller | Go | gRPC + REST | DockStateMachine, BatterySwap, WeatherReader, LocalAutonomy | 5,000 |
| sensor-fusion | Rust / C++ | Shared mem + Kafka | ADSBDecoder, RemoteIDParser, WeatherNormalizer, CameraManager, FusionEngine | 8,000 |
| command-center-ui | TypeScript | React 18 + Next.js | MapView, MissionPanel, AlertCenter, TelemetryDashboard, AuditExplorer | 25,000 |
| field-ops-app | TypeScript | React Native | DockView, ChecklistModule, MaintenanceLog, EmergencyOverride | 12,000 |
| exec-dashboard | TypeScript | React + Recharts | KPICards, FleetUtilChart, ComplianceScore, CostAnalysis, TrendView | 8,000 |
| api-gateway | Config + Go | Kong + custom plugins | AuthPlugin, RateLimiter, VersionRouter, WebhookDispatcher | 3,000 |
| ai-agents | Python 3.11+ | PyTorch + FastAPI | RouteOptimizer, AnomalyModel, MaintenancePredictor, DemandForecaster | 15,000 |
Total estimated codebase: ~155,000 lines across 14 modules. Monorepo structure with per-module CI/CD pipelines.
2.2 Service Communication Matrix
| From | To | Protocol | Pattern | Frequency |
| MCE | FIM | gRPC | Request/Reply | Per mission (readiness check) |
| MCE | CAS | gRPC | Request/Reply | Per mission (compliance eval) |
| MCE | AAE | gRPC | Request/Reply + Stream | Per mission (volume reserve) + continuous (traffic) |
| MCE | VAL | gRPC (server-stream) | Command + Stream | Per mission (execute) + continuous (telemetry) |
| VAL | TDE | Kafka | Pub (telemetry.raw) | 50 Hz per vehicle |
| TDE | Command Center UI | WebSocket | Pub/Sub | 2-10 Hz per vehicle |
| SS | VAL | 868 MHz RF + Ethernet | Binary frame | 50 Hz heartbeat, <50 ms commands |
| CAS | LAANC USS | REST/HTTPS | Request/Reply (async) | Per mission (authorization) |
| Sensor Hub | TDE | Kafka | Pub | ADS-B: variable; RID: 1 Hz; Wx: 1/min |
| All services | Kafka (audit) | Kafka | Pub | Every action/decision |
| All services | Observability | Prometheus + Loki | Push/Pull | Metrics: 15s; Logs: realtime |
| API Gateway | All services | gRPC / REST | Proxy | Per external request |
3. DATA FLOW ARCHITECTURE
3.1 Primary Data Flows
Flow 1: Mission Lifecycle (Command Path)
1. Operator creates mission via Command Center UI -> REST to API Gateway -> MCE
1. MCE calls FIM.GetVehicleReadiness(vehicle_id) -> gRPC -> FIM queries vehicle_status -> returns readiness gates
1. MCE calls CAS.EvaluateMission(plan) -> gRPC -> CAS runs OPA rules + LAANC check -> returns compliance result
1. MCE calls AAE.ReserveVolume(operational_volume) -> gRPC -> AAE checks conflicts -> reserves 4D volume
1. Operator approves -> MCE transitions to APPROVED -> publishes mission.events to Kafka
1. MCE calls VAL.ExecuteMission(plan) -> gRPC server-stream -> VAL translates to vendor commands -> vehicle executes
1. VAL streams telemetry back to MCE + publishes to Kafka telemetry.raw -> TDE persists + processes
1. TDE publishes telemetry.processed to Redis -> WebSocket server pushes to Command Center UI
1. Mission complete -> MCE finalizes state -> publishes audit event -> FIM updates flight hours -> CAS logs compliance
Flow 2: Safety Supervision (Independent Path)
1. VAL mirrors vehicle telemetry to shared memory (/dev/shm/klft_vehicle_telemetry) at 50 Hz
1. SS reads shared memory at 10 Hz, evaluates safety envelope (altitude, geofence, battery, GPS, IMU)
1. Violation detected -> SS sends RF override command via 868 MHz (HOLD, RTL, LAND, TERMINATE)
1. SS publishes alert to Kafka alerts topic -> MCE receives -> UI displays EMERGENCY alert
1. SS operates on independent hardware with independent power -> no single point of failure with MCE
Flow 3: Sensor Fusion (Awareness Path)
1. ADS-B receivers decode 1090ES transmissions -> Sensor Hub normalizes to canonical traffic format
1. Remote ID receivers capture BT5 + Wi-Fi NaN broadcasts -> Sensor Hub matches to known vehicles
1. Weather station publishes observations every 60s -> Sensor Hub normalizes and enriches with terrain data
1. All sensor data published to Kafka -> AAE consumes for traffic picture -> CAS consumes for weather go/no-go
1. TDE persists all sensor data for historical analysis and replay
3.2 Data Volume Projections
| Data Type | Rate (per vehicle) | Storage (per vehicle/day) | Retention | Growth at 50 vehicles |
| Raw telemetry | 50 Hz x 256 bytes | ~1.1 GB/day | 30 days hot, 1 yr compressed | 55 GB/day |
| Processed telemetry | 1 Hz x 128 bytes | ~11 MB/day | 1 year | 550 MB/day |
| Mission events | ~200 events/mission | ~50 KB/mission | 7 years (FAA) | Minimal |
| Audit log | ~500 entries/mission | ~100 KB/mission | 7 years (immutable) | Minimal |
| ADS-B traffic | Variable (airport-dependent) | ~500 MB/day (KLFT) | 90 days | Same (not per-vehicle) |
| Video/imagery | Optional, mission-dependent | 1-10 GB/mission | 30 days hot, 1 yr cold | 50-500 GB/day if enabled |
4. AI AGENTS AND RESPONSIBILITIES
SkyCommand embeds purpose-built AI agents at strategic decision points. Each agent operates within strict safety boundaries: AI recommends, humans (or the Safety Supervisor) decide on safety-critical actions.
4.1 Agent Registry
| Agent ID | Name | Input | Output | Decision Authority | Update Cycle |
| AI-001 | Route Optimizer | Mission request, weather, airspace, traffic, vehicle performance | Optimal route (waypoints, altitudes, speeds), fuel estimate, ETA | Advisory: operator selects from top-3 routes | Retrained monthly on flight data |
| AI-002 | Anomaly Detector | Real-time telemetry stream (50 Hz) | Anomaly score (0-1) per parameter, anomaly classification, recommended action | Escalation: score >0.7 triggers CAUTION alert; >0.9 triggers WARNING; SS handles EMERGENCY | Online learning, updated weekly |
| AI-003 | Predictive Maintenance | Battery cycles, motor hours, vibration history, environmental exposure | Component health score, predicted failure window, maintenance recommendation | Advisory: flags to FIM for scheduling; never grounds a vehicle alone (FIM decides) | Retrained quarterly |
| AI-004 | Demand Forecaster | Historical mission data, time-of-day, day-of-week, events calendar, weather forecast | Predicted mission demand by time window, recommended vehicle/dock pre-positioning | Advisory: informs MCE scheduling and dock battery pre-charge | Retrained monthly |
| AI-005 | Traffic Predictor | Historical ADS-B data, airport schedules, airspace model | Predicted traffic density heatmap for next 1-6 hours | Advisory: informs AAE volume reservation timing and route planning | Retrained weekly |
| AI-006 | Weather Impact Assessor | Wx observations, NWS forecasts, historical mission-weather correlation | Go/no-go confidence score, window recommendations, risk assessment per route segment | Advisory: supplements CAS weather evaluation; operator makes final call | Retrained seasonally |
| AI-007 | Compliance Drift Monitor | Regulatory database changes, waiver expirations, new TFR/NOTAM data | Rule change alerts, impact assessment on active operations, recommended policy updates | Escalation: notifies CAS admin of rule changes; auto-blocks if hard regulation violated | Continuous (rule feed) |
4.2 AI Safety Boundaries
- No AI agent can autonomously ground a vehicle, abort a mission, or override a human operator decision
- AI agents operate in advisory mode by default; escalation mode requires human-configured thresholds
- All AI recommendations are logged with input features, model version, confidence score, and outcome (accepted/rejected)
- Model updates require Tech Lead + Safety Officer dual approval before production deployment
- Fallback: if AI agent is unavailable, system operates normally with human decision-making (graceful degradation)
- Explainability: every recommendation includes top-3 contributing factors for operator transparency
5. USER INTERFACE LAYERS
5.1 Command Center Interface (SC-UI-01)
| View | Description | Key Elements | Update Rate |
| Tactical Map | Primary situational awareness: live vehicle positions, routes, airspace, traffic, geofences | Deck.gl/MapLibre GL JS, WGS84, terrain layer, weather overlay, airspace boundaries | 2-10 Hz |
| Mission Control Panel | Mission lifecycle management: create, validate, approve, monitor, abort | State machine visualization, timeline, checklist, approval buttons | Real-time events |
| Fleet Status Board | All vehicles and docks at a glance: health, location, availability | Card grid with status badges, battery gauges, maintenance alerts | 5s refresh |
| Alert Center | Priority-sorted alerts with acknowledgment workflow | Severity-colored list, audio for WARNING/EMERGENCY, ack + escalation buttons | Real-time push |
| Telemetry Detail | Deep-dive into single vehicle: all sensor data, charts, historical | Sparklines for battery/altitude/speed, GPS sky plot, motor status bars | 2-10 Hz |
| Airspace View | 3D airspace visualization: operational volumes, traffic, restrictions | 3D globe or cross-section view, TFR/NOTAM overlays, conflict warnings | 5s refresh |
| Audit Explorer | Searchable mission history with complete audit trail | Filter by date/vehicle/operator/status, event timeline, export (PDF/CSV) | On-demand |
| Weather Dashboard | Current conditions + forecast with go/no-go indicators | Wind rose, visibility, ceiling, temperature, trend charts, threshold lines | 60s |
5.2 Field Operations App (SC-UI-02)
| Feature | Description | Offline Capable? |
| Dock Status | Real-time dock state, vehicle occupancy, charge level | Yes (cached) |
| Pre-Flight Checklist | Digital checklist synced with FIM readiness gates | Yes (queue sync) |
| Maintenance Logging | Log inspections, repairs, part replacements with photos | Yes (queue sync) |
| Emergency Override | Direct RTL/HOLD/LAND commands via cellular or local network | No (requires connectivity) |
| Vehicle Check-In/Out | Register vehicle arrival/departure at dock site | Yes (queue sync) |
| Battery Management | Log battery swap, cycle count, storage temperature | Yes (queue sync) |
| Incident Reporting | Occurrence report with photos, location, narrative | Yes (queue sync) |
5.3 Executive Dashboard (SC-UI-03)
| Widget | Metric | Visualization | Refresh |
| Fleet Utilization | % vehicles in productive flight vs idle/maintenance | Donut chart + trend line | Hourly |
| Mission Success Rate | % missions completed without abort or incident | KPI card + 30-day sparkline | Daily |
| Compliance Score | % flights fully compliant (all rules passed) | Gauge (target: 100%) | Daily |
| Cost Per Flight Hour | Operating cost breakdown: energy, maintenance, personnel, infra | Stacked bar chart | Weekly |
| Safety Incidents | Occurrence count by severity over time | Stacked area chart | Daily |
| Mean Time to Launch | Average seconds from mission request to airborne | KPI card + histogram | Daily |
| Dock Availability | % time each dock is operational vs maintenance/fault | Heat map (dock x day) | Daily |
| AI Agent Performance | Recommendation acceptance rate, prediction accuracy | Table with trend arrows | Weekly |
6. CLOUD INFRASTRUCTURE
6.1 Cloud Architecture (Hybrid Deployment)
| Layer | Service | Provider Options | Sizing (Phase 1) | Scaling Strategy |
| Compute (Core Services) | Kubernetes cluster | AWS EKS / GCP GKE / Azure AKS / On-prem K3s | 3 nodes (4 vCPU, 16 GB each) | Horizontal pod autoscaling; add nodes per 10 vehicles |
| Compute (AI/ML) | GPU instances | AWS p3 / GCP A2 / On-prem NVIDIA A4000 | 1 GPU node (training); CPU inference Phase 1 | Scale GPU nodes for batch training; CPU inference scales with core |
| Database (State) | PostgreSQL HA | AWS RDS / GCP Cloud SQL / On-prem Patroni | db.r6g.xlarge or equiv (4 vCPU, 32 GB, 500 GB SSD) | Read replicas for dashboard queries; vertical scaling |
| Database (Time-Series) | TimescaleDB | Timescale Cloud / On-prem TimescaleDB | 32 GB RAM, 2 TB SSD, compression enabled | Partition by time; tiered storage (hot/warm/cold) |
| Message Bus | Kafka | Confluent Cloud / AWS MSK / On-prem | 3 brokers, 100 GB each | Add brokers per 25 vehicles; increase partitions |
| Cache | Redis Cluster | AWS ElastiCache / On-prem | 3 nodes, 8 GB each | Shard by vehicle_id |
| Object Storage | S3-compatible | AWS S3 / GCP GCS / MinIO (on-prem) | 1 TB (flight logs, imagery, exports) | Lifecycle policies: hot -> warm -> glacier |
| CDN / Edge | Static assets + API caching | CloudFront / Cloudflare | Standard tier | Auto-scales |
| DNS / Load Balancer | Traffic routing | Route 53 + ALB / Cloudflare LB | Standard | Auto-scales |
| VPN / Connectivity | Site-to-cloud link | AWS Site-to-Site VPN / WireGuard | 1 tunnel per site | 1 tunnel per additional site |
6.2 Network Architecture
| Zone | CIDR | Purpose | Firewall Rules |
| Operations VLAN | 10.10.10.0/24 | Core services, inter-service communication | Allow all internal; deny external except API Gateway |
| Safety VLAN | 10.10.30.0/29 | SS nodes only, isolated from ops network | Allow only SS <-> VAL; deny all other |
| Edge VLAN | 10.10.40.0/24 | Edge nodes at dock sites | Allow VPN tunnel to Operations; deny direct internet |
| Management VLAN | 10.10.50.0/24 | iDRAC, IPMI, switch management, UPS SNMP | Allow SSH from bastion only; deny all external |
| DMZ | 10.10.70.0/24 | API Gateway, LAANC integration, Remote ID upload | Allow HTTPS in/out; deny internal except API Gateway |
| Public | Dynamic | CDN, DNS, public API endpoint | WAF + rate limiting; DDoS protection |
6.3 Disaster Recovery
| Component | RPO | RTO | Backup Strategy | Failover |
| PostgreSQL (state) | < 1 min | < 5 min | Streaming replication + daily snapshots to S3 | Auto-failover via Patroni / RDS Multi-AZ |
| TimescaleDB (telemetry) | < 5 min | < 15 min | Continuous archiving + daily base backup | Manual failover; data loss acceptable for raw telemetry |
| Kafka | 0 (replicated) | < 2 min | In-sync replicas (ISR=2); topic replication factor 3 | Automatic partition leader election |
| Redis (cache) | N/A (cache) | < 1 min | No backup needed; rebuilt from source on restart | Sentinel auto-failover |
| Application state | N/A (stateless) | < 1 min | Container images in registry; K8s manifests in Git | Rolling restart; Kubernetes self-healing |
| Safety Supervisor | N/A | < 10 sec | Hot standby SS node | Automatic switchover on heartbeat loss |
| Edge Nodes | < 1 hr | < 5 min (local) | Local buffer; replay on reconnect | Local autonomy mode; queue-and-forward |
7. HARDWARE INTEGRATION
7.1 Supported Hardware Matrix
| Category | Hardware | Interface | Adapter Module | Status |
| Drone: Multi-Rotor | DJI Matrice 350 RTK | DJI Cloud API v2 (REST + MQTT) | DJIAdapter | Phase 1 (primary) |
| Drone: Multi-Rotor | Skydio X10 | Skydio SDK (gRPC) | SkydioAdapter | Phase 2 |
| Drone: Multi-Rotor | ArduPilot/PX4 (custom) | MAVLink 2.0 (serial/UDP) | MAVLinkAdapter | Phase 3 |
| Drone: Fixed-Wing | Textron Aerosonde / custom | MAVLink 2.0 | MAVLinkAdapter (extended) | Phase 4 |
| Dock | DJI Dock 2 | DJI Cloud API v2 | DJIDockController | Phase 1 |
| Dock | Skydio Dock | Skydio SDK | SkydioDockController | Phase 2 |
| Dock | Custom / ValqariDrone | REST API / Modbus | GenericDockController | Phase 3 |
| ADS-B Receiver | FlightAware Pro Stick Plus | dump1090 SBS/Beast TCP | ADSBDecoder | Phase 1 |
| Remote ID Receiver | ANRA SmartSkies / SDR-based | BT5 + Wi-Fi NaN (ASTM F3411) | RemoteIDParser | Phase 1 |
| Weather Station | Davis Vantage Pro2 | WeatherLink IP (TCP) | WeatherNormalizer | Phase 1 |
| PTZ Camera | Axis Q6135-LE | ONVIF / RTSP | CameraManager | Phase 1 |
| Safety RF | Digi XBee 900HP / LoRa | 868 MHz serial | RFCommander | Phase 1 |
| C2 Link (Primary) | 900 MHz directional | Serial / UDP over RF | C2LinkManager | Phase 1 |
| C2 Link (Backup) | 4G/5G cellular modem | TCP/IP over cellular | CellularBackup | Phase 1 |
7.2 Vehicle Abstraction Layer Design
Every vehicle type is integrated through a canonical interface. The VAL pattern ensures that adding a new vehicle type requires only a new adapter module, with zero changes to core services.
| Canonical Command | Parameters | Behavior | Timeout |
| ARM | confirmation_code | Enable motors, enter flight-ready state | 5s |
| TAKEOFF | target_altitude_ft | Vertical climb to target altitude | 30s |
| GOTO_WAYPOINT | lat, lng, alt_ft, speed_kts | Navigate to waypoint at specified speed | Per distance |
| ORBIT | center_lat, center_lng, radius_ft, alt_ft, speed_kts, direction | Circle a point at fixed radius | Continuous |
| HOLD | (none) | Hover at current position (multi-rotor) or loiter (fixed-wing) | Indefinite |
| RTL | (none) | Return to launch/dock site via safe altitude | Per distance |
| LAND | (none) or target_lat, target_lng | Precision land at dock or specified coordinates | 60s |
| DISARM | confirmation_code | Disable motors (ground only) | 5s |
| SET_SPEED | speed_kts | Change cruise speed mid-mission | Immediate |
| SET_ALTITUDE | alt_ft | Change altitude mid-mission | Per distance |
| PAYLOAD_ACTION | action, params | Trigger payload (camera capture, release, gimbal) | 5s |
| TERMINATE | emergency_code | Flight termination system activation (parachute or motor kill) | Immediate |
7.3 Dock Integration Architecture
| Dock State | Entry Condition | Actions | Exit Condition | Timeout |
| IDLE | Vehicle docked, fully charged | Monitor battery, report status | Mission assigned | Indefinite |
| PREPARING | Mission approved, preflight pass | Open dock lid, run pre-launch checks | Checks pass + lid open | 60s |
| LAUNCHING | Preparation complete | Arm vehicle, initiate takeoff | Vehicle airborne + altitude > 10 ft | 30s |
| ACTIVE | Vehicle airborne | Monitor dock for recovery readiness | Vehicle approaching for landing | Mission duration |
| RECOVERING | Vehicle in approach | Guide precision landing, close lid | Vehicle landed + lid closed | 90s |
| CHARGING | Vehicle recovered | Initiate battery charge, report SOC | SOC >= charge_target (95%) | Variable (60-120 min) |
| MAINTENANCE | Fault detected or scheduled | Lock out for maintenance, alert operator | Maintenance complete + operator clear | Manual |
| FAULT | Hardware error or safety event | Emergency stop, alert operator, log fault | Manual reset by field crew | Manual |
8. COMMAND CENTER ARCHITECTURE
8.1 Physical Layout
| Zone | Size | Equipment | Purpose |
| Operations Floor | 800 sq ft | 4 operator workstations (32"+27" displays each), 6-display video wall, raised floor, dimmable lighting | Primary mission control |
| Server Room | 400 sq ft | 2x 42U racks, precision HVAC (N+1), fire suppression (Novec 1230), biometric access | Core compute and storage |
| Communications Room | 200 sq ft | RF equipment rack, antenna feedlines (6 runs), network demarcation, grounding bus | RF and network infrastructure |
| Equipment Staging | 300 sq ft | 2 ESD workbenches, fire-rated battery cabinet, charging station (4 bays), tool storage | Vehicle maintenance and prep |
| NOC / IT Support | 200 sq ft | 2 workstations, direct server room access, monitoring displays | Infrastructure management |
| Briefing Room | 250 sq ft | 75" display, whiteboard, table for 8, network drops | Shift briefing and training |
8.2 Operator Workstation Specification
| Component | Specification | Rationale |
| Primary Display | 32" 4K IPS (3840x2160) | Tactical map with sufficient resolution for multi-vehicle tracking |
| Secondary Display | 27" 4K IPS (3840x2160) | Data panels: telemetry, alerts, mission details, audit |
| Desk | L-shaped (72"x72"), adjustable height, cable management | Ergonomic for 12-hour shifts; space for peripherals |
| Input | Keyboard + trackball (not mouse for precision on map), dedicated RTL/HOLD/ABORT hardware buttons | Trackball for continuous map interaction; hardware buttons for muscle-memory emergency actions |
| Audio | Headset with active noise cancellation + desk speaker for EMERGENCY alerts | Noise reduction for focus; unmissable emergency audio |
| Comms | Push-to-talk radio (ATC coordination) + internal intercom | Direct ATC contact for controlled airspace operations |
| Chair | Herman Miller Aeron or equiv, fully adjustable | 12-hour shift ergonomics |
| UPS | Per-workstation 1500VA sinewave UPS | Survive power transfer to generator |
8.3 Video Wall Configuration
| Display Position | Default Content | Override Content |
| Top-Left | Regional map: all vehicles, docks, airspace boundaries | Zoom to incident area |
| Top-Center | Airspace status: TFRs, NOTAMs, active LAANC authorizations | ATC coordination display |
| Top-Right | Weather: current conditions, radar, ceiling/visibility | Severe weather detail |
| Bottom-Left | Fleet status board: all vehicles with health badges | Single vehicle deep-dive |
| Bottom-Center | Active missions timeline with status | Emergency procedure checklist |
| Bottom-Right | Alert feed + KPI summary (missions today, success rate) | Incident response log |
9. SECURITY AND PERMISSIONS
9.1 Security Architecture
| Layer | Control | Implementation | Standard |
| Network | Segmentation | VLANs: Ops, Safety, Edge, Mgmt, DMZ (see Section 6.2) | NIST 800-53 SC-7 |
| Network | Encryption in transit | TLS 1.3 all interfaces; mTLS for gRPC inter-service | NIST 800-53 SC-8 |
| Network | Firewall | Zone-based firewall rules; default deny; explicit allow | NIST 800-53 SC-7 |
| Application | Authentication | JWT RS256 tokens (REST/WS); mTLS certificates (gRPC); SASL/SCRAM (Kafka) | NIST 800-53 IA-2 |
| Application | Authorization | RBAC with 6 roles (see 9.2); attribute-based for multi-tenant | NIST 800-53 AC-3 |
| Application | API Security | Rate limiting, input validation, CORS, anti-replay (idempotency keys) | OWASP API Top 10 |
| Application | Prompt injection defense | AI agent inputs sanitized; output validated against schema; no direct LLM access to commands | Custom |
| Data | Encryption at rest | AES-256 for database volumes; encrypted S3 buckets | NIST 800-53 SC-28 |
| Data | Audit integrity | Append-only audit log with SHA-256 hash chain; no UPDATE/DELETE | NIST 800-53 AU-10 |
| Data | Backup encryption | All backups encrypted with separate key; key rotation quarterly | NIST 800-53 CP-9 |
| Safety RF | RF encryption | AES-128 per-frame encryption; pre-shared keys; sequence counter anti-replay | Custom (aviation-grade) |
| Physical | Facility access | Biometric + badge for server room; camera on all entries; visitor log | NIST 800-53 PE-3 |
9.2 Role-Based Access Control
| Role | Command Center | Mission Actions | Fleet Actions | System Admin | Safety Override |
| Super Admin | Full access | All | All | Full (user mgmt, config, deployment) | View only (cannot override) |
| Operations Supervisor | Full access | Approve, abort, override | Readiness override, grounding | View config | Safety hold authority |
| RPIC (Remote Pilot) | Full access | Create, validate, approve, monitor, abort, override | View, pre-flight check | None | Direct vehicle override |
| Mission Operator | Assigned missions only | Create, validate, monitor | View assigned vehicles | None | None |
| Maintenance Tech | Fleet status only | None | Log maintenance, update status, battery management | None | None |
| Viewer / Auditor | Read-only all views | None | None | Audit log access | None |
9.3 Certificate and Key Management
| Asset | Type | Rotation | Storage | Revocation |
| TLS server certs | X.509 (Let's Encrypt or internal CA) | 90 days auto-renew | Kubernetes secrets (encrypted) | CRL + OCSP |
| mTLS client certs | X.509 (internal CA) | 180 days | Kubernetes secrets | CRL checked per-request |
| JWT signing keys | RSA-2048 keypair | 30 days | HashiCorp Vault or AWS KMS | Key ID in token; old keys kept 48 hrs for grace |
| Kafka SASL credentials | SCRAM-SHA-512 | 90 days | Kubernetes secrets | Immediate rotation on compromise |
| Safety RF pre-shared keys | AES-128 | 180 days | Hardware security module (HSM) or secure enclave | Physical key ceremony |
| Database credentials | Password (pgBouncer-managed) | 90 days | Kubernetes secrets + Vault | Immediate rotation |
| API keys (external) | Opaque tokens (256-bit) | Annual or on compromise | Hashed in DB; plain in client config | Instant revocation via admin UI |
10. SCALABILITY DESIGN
10.1 Scaling Dimensions
| Dimension | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Scaling Mechanism |
| Concurrent vehicles | 1 | 5 | 20 | 50+ | Horizontal pod scaling; Kafka partition increase; TSDB partition growth |
| Telemetry throughput | 50 msg/s | 250 msg/s | 1,000 msg/s | 2,500+ msg/s | Kafka brokers + partitions; TDE consumer group scaling; Redis sharding |
| Concurrent operators | 2 | 5 | 10 | 20+ | UI server instances; WebSocket connection pooling; read replicas for queries |
| Dock sites | 1 | 3 | 10 | 25+ | Edge node per site; VPN tunnels; federated AAE; regional MCE instances |
| Geographic regions | 1 (KLFT) | 1 | 2-3 | 5+ | Multi-region deployment; regional data residency; federated control plane |
| API requests | 100/min | 500/min | 2,000/min | 10,000+/min | API Gateway horizontal scaling; CDN caching; read replicas |
| Data retention | 30 days hot | 30 days hot + 1 yr compressed | 30 days hot + 3 yr tiered | 30 days hot + 7 yr tiered | Tiered storage: NVMe -> SSD -> S3 -> Glacier |
10.2 Horizontal Scaling Architecture
Stateless services (MCE, CAS, FIM, API Gateway): Scale by adding Kubernetes replicas. Load balanced via K8s Service. No session affinity required. Target: 1 replica per 10 concurrent vehicles.
Kafka: Scale by adding brokers and increasing partitions. Telemetry topic partitioned by vehicle_id for ordered per-vehicle processing. Consumer groups scale with partition count.
TimescaleDB: Scale vertically (RAM, SSD) first. Then: read replicas for dashboard queries; continuous aggregates to reduce query load; tiered storage for cost management. At extreme scale: multi-node TimescaleDB.
Redis: Scale via Redis Cluster with sharding by vehicle_id. Each shard handles ~500 vehicles at 50 Hz update rate. Add shards as fleet grows.
Edge Nodes: One edge node per dock site. Independent operation (local autonomy on link loss). Connected via VPN to nearest regional control plane.
Safety Supervisor: One SS per site. Hot standby for failover. Does not scale horizontally (intentionally isolated). One SS handles up to 50 vehicles at 10 Hz evaluation rate.
AI Agents: CPU inference scales with core services (co-located). GPU training runs on separate schedule (off-peak or dedicated GPU node). Model serving via TorchServe with autoscaling.
10.3 Multi-Tenant Architecture (SaaS)
| Isolation Level | Description | Use Case | Cost Efficiency |
| Shared compute, shared DB (logical isolation) | All tenants on same cluster; data isolated by tenant_id column + row-level security | Small operators, free/starter tier | Highest |
| Shared compute, dedicated DB | Each tenant gets own database instance; shared K8s cluster | Mid-market; compliance-sensitive | Medium |
| Dedicated compute, dedicated DB | Tenant gets own K8s namespace or cluster + own DB | Enterprise; government; air-gapped | Lowest |
Tenant isolation is enforced at API Gateway (tenant_id from JWT), database (RLS policies), Kafka (tenant-prefixed topics or shared topics with tenant_id filtering), and storage (tenant-prefixed S3 paths).
10.4 Performance Targets
| Metric | Target | Measurement | Scaling Trigger |
| Telemetry end-to-end latency | < 500 ms (vehicle to screen) | p99 measured at UI WebSocket receive | Scale TDE consumers if >400 ms p95 |
| Safety command latency | < 50 ms (SS to vehicle) | p99 measured at RF acknowledgment | Hardware upgrade (cannot software-scale SS) |
| API response time | < 200 ms (p99) | Measured at API Gateway | Scale service replicas if >150 ms p95 |
| Mission state transition | < 100 ms | Measured at MCE event publish | Scale MCE replicas if >80 ms p95 |
| Search / query response | < 500 ms | Measured at UI for audit/history queries | Add read replica if >400 ms p95 |
| System availability | 99.9% (core); 99.999% (safety) | Monthly uptime calculation | Incident review; redundancy upgrade |
| Data durability | 99.999999% (11 nines) | Calculated from replication + backup | Verify replication health daily |
| Recovery time (core) | < 5 min | Tested quarterly | DR drill; improve automation |
END OF DOCUMENT
SkyCommand Drone Operations Platform — Full Platform Architecture v1.0
---
## MARLIE I NOC Integration
SkyCommand instances at remote sites (starting with KLFT 1.1) synchronize to the MARLIE I Network Operations Center at 1201 SE Evangeline Thruway, Lafayette LA. MARLIE I serves as the persistent command backbone for the Gulf Coast drone network.
- Fleet telemetry: real-time from all Skydio Dock units to MARLIE I dashboard
- Mission archive: all flight logs, video, and incident reports stored on MARLIE I NVL72 storage tier
- Multi-site coordination: MARLIE I NOC can dispatch missions to any registered KLFT site
- Failover: each KLFT ADC 3K pod operates autonomously if WAN link drops
- NVIDIA Vera Rubin NVL72 at MARLIE I: runs fleet-wide video analytics, anomaly detection, report generation
---
## ADC 3K Edge Pod at KLFT Site
- One ADC 3K pod per KLFT site — full immersion cooling (Engineered Fluids EC-110)
- Local inference: object detection, video compression, scene classification
- SkyCommand edge agent: buffers missions and video during WAN outage, syncs on reconnect
- Power: LUS grid primary — pod runs on facility circuit, no dedicated HVAC needed