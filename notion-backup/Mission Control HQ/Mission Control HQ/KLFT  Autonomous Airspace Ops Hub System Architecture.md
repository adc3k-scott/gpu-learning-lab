# KLFT — Autonomous Airspace Ops Hub System Architecture
*Notion backup — 2026-03-28*

AUTONOMOUS AIRSPACE OPERATIONS HUB
AI-ASSISTED MISSION CONTROL SYSTEM
System Architecture Design Document
Lafayette Regional Airport (KLFT), Louisiana
Production-Grade Infrastructure Specification
Document Version: 1.0 | February 2026
CLASSIFICATION: ENGINEERING DRAFT
1. SYSTEM ARCHITECTURE OVERVIEW
1.1 High-Level Architecture
The KLFT Autonomous Airspace Operations Hub is a layered, safety-critical system designed to manage autonomous UAS operations across the Acadiana region. The architecture follows a defense-in-depth model with deterministic safety layers that cannot be overridden by AI or optimization components. The system is partitioned into five architectural tiers, each with clearly defined responsibilities and failure boundaries.
Architectural Tiers
| Tier | Name | Responsibility | Failure Mode |
| T0 | Safety Kernel | Deterministic failsafe execution, geofence enforcement, lost-link response | Independent hardware watchdog triggers RTL/land |
| T1 | Real-Time Control | Vehicle telemetry processing, command relay, sensor fusion | Degrades to T0 autonomous safety mode |
| T2 | Mission Management | Flight planning, dispatch, traffic deconfliction, compliance | Suspends new missions; active flights continue on T1/T0 |
| T3 | AI/Optimization | Predictive routing, demand forecasting, anomaly detection, scheduling | System operates on rule-based fallbacks at T2 |
| T4 | External Integration | FAA LAANC, Remote ID broadcast, UTM federation, ATC coordination | Local operations continue; external reporting queued |
1.2 Major Subsystems
The system comprises eight major subsystems, each deployable as an independent service with defined interfaces.
| Subsystem | Function | Criticality |
| Airspace Manager (ASM) | Low-altitude airspace structure, dynamic volumes, geofencing | Safety-Critical |
| Mission Dispatcher (MD) | Mission lifecycle management, dispatch sequencing, task allocation | Mission-Critical |
| Safety Supervisor (SS) | Independent safety monitoring, override authority, watchdog | Safety-Critical |
| Fleet Health Manager (FHM) | Vehicle state tracking, maintenance, battery management, readiness | Mission-Critical |
| Compliance Engine (CE) | Regulatory rule evaluation, LAANC integration, audit logging | Regulatory-Critical |
| Traffic Deconfliction Engine (TDE) | Conflict detection, resolution, separation assurance | Safety-Critical |
| Data Pipeline (DP) | Telemetry ingestion, storage, event processing, analytics | Operational |
| Operator Interface (OI) | Situational awareness displays, manual override controls, alerting | Mission-Critical |
1.3 System Boundaries
Internal boundary: All real-time decision-making, safety enforcement, and vehicle control execute within the local facility. No external dependency is required for safe operation.
External boundary: FAA integration (LAANC, Remote ID network), UTM federation, and third-party data services are treated as non-critical external interfaces. Loss of external connectivity does not degrade safety or halt active operations.
Operator boundary: Human operators retain ultimate override authority at all times. The system enforces a minimum staffing model where at least one qualified operator monitors active operations. AI recommendations require operator acceptance for safety-relevant actions until the system reaches full Part 108 certification.
2. MISSION CONTROL SOFTWARE ARCHITECTURE
2.1 Airspace Manager (ASM)
Runtime: Rust-based core with deterministic memory management
Update rate: 10 Hz for dynamic volume management, 1 Hz for structure updates
- Maintains the canonical low-altitude airspace model (surface to 400 ft AGL)
- Manages dynamic operational volumes (DOVs) for each active mission
- Enforces static and dynamic geofences including NOTAMs, TFRs, and operator-defined exclusions
- Publishes airspace state to all consuming subsystems via shared memory bus
- Evaluates airspace reservation requests against current state and rules
2.2 Mission Dispatcher (MD)
Runtime: Go service with PostgreSQL state store
Throughput: Supports 200+ concurrent mission plans
- Accepts mission requests from operators, automated triggers, and API clients
- Validates missions against airspace availability, fleet readiness, and compliance rules
- Sequences multi-step missions (preflight, launch, en-route, on-station, RTL, post-flight)
- Manages mission state machine transitions with full audit trail
- Coordinates with Fleet Health Manager for vehicle assignment
2.3 Safety Supervisor (SS)
Runtime: Independent RTOS process on dedicated safety-rated hardware
Update rate: 50 Hz heartbeat monitoring, 10 Hz state evaluation
- Operates independently of all other subsystems on separate compute hardware
- Monitors all active vehicle telemetry against safety envelopes
- Executes deterministic failsafe actions: RTL, loiter, emergency land, flight termination
- Cannot be overridden by AI layer, Mission Dispatcher, or Operator Interface
- Implements hardware watchdog; if SS itself fails, all vehicles execute onboard failsafes
- Maintains independent communication path to vehicles via dedicated radio link
2.4 Fleet Health Manager (FHM)
Runtime: Python/Go hybrid service
- Tracks per-vehicle state: battery SoC, motor health, sensor calibration, firmware version
- Enforces pre-flight readiness gates (minimum battery, GPS lock, IMU health, Remote ID active)
- Manages maintenance schedules and flight-hour tracking per FAA Part 107/108 requirements
- Assigns vehicles to missions based on capability, range, payload, and readiness score
- Interfaces with vendor-specific health APIs via abstraction layer (Section 9)
2.5 Compliance Engine (CE)
Runtime: Rule engine (OPA/Drools) with PostgreSQL audit store
- Evaluates every mission plan against current regulatory rules before approval
- Manages LAANC authorization requests and approval caching
- Validates Remote ID broadcast compliance for all active vehicles
- Generates audit records for every decision, override, and exception
- Maintains versioned rule sets that can be updated without system restart
- Produces FAA-required reports: flight logs, incident reports, waiver compliance
2.6 Traffic Deconfliction Engine (TDE)
Runtime: C++ with lock-free concurrent processing
Update rate: 10 Hz conflict detection, 1 Hz strategic deconfliction
- Performs continuous pairwise separation analysis for all active aircraft
- Implements three-tier conflict resolution: strategic, tactical, and emergency
- Generates conflict-free 4D trajectory amendments when separation minima are projected to be violated
- Ingests ADS-B and Remote ID data for cooperative traffic awareness
- Applies well-clear definitions per ASTM F3442 standard
2.7 Data Processing Pipeline (DP)
Runtime: Apache Kafka + TimescaleDB + Redis
- Ingests all telemetry streams at full rate (50 Hz per vehicle, 200+ concurrent vehicles)
- Provides real-time event stream for all subsystem consumers
- Manages time-series storage with configurable retention (hot: 30 days, warm: 1 year, cold: 7 years)
- Processes derived metrics: fleet utilization, airspace density, response times
- Feeds AI/ML training pipelines with anonymized operational data
2.8 Operator Interface (OI)
Runtime: React + WebSocket backend, hardware-accelerated map rendering
- Provides primary situational awareness display: 2D/3D airspace, traffic, weather overlay
- Supports manual mission creation, modification, and cancellation
- Displays real-time alerts with severity-based prioritization (caution/warning/emergency)
- Implements manual override controls with confirmation gates for safety-critical actions
- Supports multi-operator concurrent access with role-based permissions
- Records all operator interactions for audit and training purposes
2.9 Inter-Subsystem Communication
All subsystems communicate via shared-memory bus (safety-critical, sub-ms latency), message broker (mission-critical, Kafka), and REST/gRPC APIs (configuration, non-real-time).
| Path | Protocol | Latency Requirement |
| SS <-> Vehicle | Dedicated RF + shared memory | < 50 ms |
| TDE <-> ASM | Shared memory bus | < 10 ms |
| MD <-> FHM | gRPC | < 100 ms |
| CE <-> LAANC | REST/HTTPS | < 5 sec (non-blocking) |
| OI <-> All subsystems | WebSocket + Kafka consumer | < 200 ms display update |
| DP ingestion | Kafka topics | < 50 ms end-to-end |
3. AIRSPACE MANAGEMENT MODEL
3.1 Low-Altitude Airspace Structure
The KLFT operations area is structured as a three-dimensional managed airspace volume extending from surface to 400 ft AGL. Lateral boundary: 15 NM radius from KLFT, expandable as operations scale.
Altitude Layer Definitions
| Layer | Altitude (AGL) | Purpose | Speed Limit | Priority |
| L0 - Surface | 0 - 50 ft | Launch, land, ground ops, dock approach | 15 kts | Highest (emergency) |
| L1 - Low Transit | 50 - 150 ft | Local delivery, short-range inspection | 35 kts | High |
| L2 - Primary Transit | 150 - 300 ft | Corridor transit, cross-region routing | 55 kts | Standard |
| L3 - High Transit | 300 - 400 ft | Long-range transit, emergency priority | 65 kts | Standard/Emergency |
3.2 Priority Rules
Traffic priority is enforced by the TDE and ASM in the following precedence order:
1. Emergency response / DFR: Absolute priority, may claim any airspace volume
1. Medical delivery (organ, blood, critical meds): High priority, pre-cleared corridors
1. Active safety maneuvers (conflict avoidance, RTL): High priority within maneuvering volume
1. Infrastructure inspection (scheduled, utility-critical): Standard priority
1. Commercial delivery: Standard priority, yield to categories 1-4
1. Training / test flights: Lowest priority, restricted to designated practice areas
3.3 Routing Logic
- Transit corridors: 200 ft wide, directional (eastbound at L2, westbound at L3 to reduce head-on conflicts)
- Approach corridors: 100 ft wide, converging on launch/land sites, speed-restricted to 15 kts
- Free-flight zones: Designated areas for deviation from corridor structure (e.g., inspection orbits)
- Dynamic re-routing: TDE may issue re-routes in real-time to resolve predicted conflicts
3.4 Geofence System
Static geofences: Airport control zones, restricted areas, NOTAMs, permanent exclusions (schools, hospitals, prisons). Loaded at startup from FAA data and local config.
Dynamic geofences: Active manned aircraft proximity zones, TFRs, weather exclusions. Updated in real-time from sensor network and ATC feeds.
Mission geofences: Per-flight operational volume (OV) and contingency volume (CV) per ASTM F3548. Generated by MD, enforced by SS.
Geofence penetration triggers immediate automated response: alert to operator, vehicle hold/RTL command, compliance logging.
3.5 Conflict Resolution Logic
Strategic (T-5+ min): Pre-departure deconfliction. MD adjusts departure time or route before launch. No vehicle impact.
Tactical (T-30s to 5 min): In-flight deconfliction. TDE issues trajectory amendments. Automated execution with operator notification.
Emergency (T < 30 sec): SS takes direct control. Deterministic avoidance maneuver. Overrides all other commands. Immediate operator alert.
3.6 Emergency Handling
- DFR launch triggers immediate airspace reservation along predicted route; conflicting traffic receives hold/re-route within 2 seconds
- Manned aircraft incursion triggers automatic lateral/vertical clearance for all UAS within 0.5 NM
- Lost-link aircraft assigned protected volumes based on pre-programmed contingency trajectory
- Weather deterioration below minimums triggers phased stand-down: new launches suspended, then active flights RTL by priority
4. SAFETY AND FAILSAFE DESIGN
4.1 Design Philosophy
System designed to DO-178C DAL-C equivalent for safety-critical components (SS, ASM, TDE). Core principle: system must remain safe with any single subsystem in a failed state.
4.2 Lost Link Handling
| Condition | Detection | Response | Timeout |
| C2 link degraded | Packet loss > 20% over 5 sec | Alert operator, switch to backup link | 5 sec |
| C2 link lost (primary) | No heartbeat for 10 sec | Auto-switch to backup RF path, notify operator | 10 sec |
| C2 link lost (all paths) | No heartbeat on any link for 30 sec | Vehicle executes onboard lost-link procedure (RTL or land) | 30 sec |
| SS link lost | Hardware watchdog timeout | Vehicle onboard failsafe (pre-programmed RTL waypoint) | 5 sec |
| GCS total failure | Heartbeat from independent watchdog | All vehicles execute contingency trajectories | 15 sec |
4.3 System Failure Modes
| Component | Failure Mode | Impact | Mitigation |
| Mission Dispatcher | Process crash | No new missions dispatched | Auto-restart; active missions unaffected (T1) |
| Airspace Manager | State corruption | Invalid airspace model | Hot standby takeover < 500 ms |
| TDE | Processing overload | Delayed conflict detection | Auto traffic density reduction; launches paused |
| AI Layer | Model failure | Bad recommendations | All AI outputs validated by deterministic rules |
| Data Pipeline | Kafka broker failure | Telemetry gaps | Multi-broker cluster; local buffer on edge |
| Operator Interface | Display failure | Loss of SA | Redundant displays; audio alerts independent of UI |
| Network (internal) | Switch failure | Comms loss | Redundant paths; safety bus on separate HW |
| Power | Facility power loss | Full system down | UPS (30 min) + generator (72 hr) + graceful shutdown |
4.4 Override Authority Hierarchy
1. FAA ATC directive (highest authority, always obeyed)
1. Safety Supervisor automated failsafe (deterministic, not overridable for safety-critical actions)
1. Qualified operator manual command (full vehicle control within safety envelope)
1. Mission Dispatcher automated sequencing
1. AI optimization recommendations (lowest authority, advisory only)
4.5 Redundancy Model
- Compute: Dual-redundant active-active for safety-critical; hot standby for mission-critical
- Network: Dual independent LAN segments; safety bus on physically separate cabling
- RF links: Primary C2 (900 MHz), backup C2 (2.4 GHz), emergency safety link (868 MHz)
- Power: Dual utility feeds, ATS, UPS, diesel generator
- Storage: RAID-10 operational, replicated PostgreSQL with streaming replication
- Sensors: Dual ADS-B, redundant weather stations, overlapping Remote ID receivers
4.6 Deterministic Safety vs. AI Decisions
| Decision Type | Handler | AI Role | Override |
| Geofence enforcement | Safety Supervisor (deterministic) | None | No |
| Lost-link response | Safety Supervisor (deterministic) | None | No |
| Collision avoidance (< 30s) | TDE (deterministic) | None | No |
| Route optimization | MD + AI | Recommends optimal route | Yes (operator) |
| Mission scheduling | MD + AI | Proposes schedule | Yes (operator) |
| Traffic flow mgmt | TDE + AI | Predicts congestion | Yes (rules engine) |
| Anomaly alerting | AI + SS | Detects anomaly pattern | AI alert only; SS acts on threshold |
5. AI CONTROL LAYER DESIGN
5.1 Architecture Principle
AI operates exclusively at Tier 3 (optimization/advisory). All AI outputs pass through a deterministic validation gate before reaching any actuator or command path. The AI layer has no direct command authority over any vehicle. It recommends; the deterministic layers decide.
5.2 AI Components
5.2.1 Mission Planner AI
Function: Generates optimal mission plans considering weather, airspace, traffic density, fleet availability, energy constraints, and delivery windows.
Model: Constraint-satisfaction solver with RL for route optimization. Trained on historical flight data.
Validation: All proposed plans evaluated by Compliance Engine and Airspace Manager before acceptance.
5.2.2 Traffic Prediction Engine
Function: Forecasts airspace density and conflict probability 5-30 minutes ahead.
Model: Spatiotemporal graph neural network trained on historical traffic patterns and event data.
Validation: Predictions are advisory inputs to TDE; TDE applies deterministic separation rules regardless.
5.2.3 Anomaly Detection System
Function: Identifies abnormal vehicle behavior, sensor degradation, and unusual traffic patterns.
Model: Autoencoder + isolation forest ensemble trained on nominal flight profiles.
Validation: Raises alerts; Safety Supervisor evaluates against deterministic thresholds before acting.
5.2.4 Demand Forecasting
Function: Predicts mission demand by type, location, and time window for fleet pre-positioning and staffing.
Model: Time-series forecasting (Prophet/LSTM) with external features (weather, events, historical patterns).
5.2.5 Energy Management Optimizer
Function: Optimizes battery swap/charge schedules, fleet rotation, and dock utilization.
Model: Mixed-integer linear program (MILP) with battery degradation model.
5.3 AI Safety Constraints
- No AI model has write access to vehicle command channels
- All AI recommendations carry confidence scores; low-confidence flagged for operator review
- Continuous performance monitoring; drift detection triggers fallback to rule-based operation
- AI training data versioned and auditable; model updates require formal change control
- Shadow mode: New models run in parallel with production for minimum 30 days before promotion
6. PHYSICAL INFRASTRUCTURE REQUIREMENTS
6.1 Mission Control Facility Layout
Purpose-built or retrofitted space at/adjacent to KLFT, approximately 3,000 sq ft:
| Zone | Size (sq ft) | Function | Requirements |
| Operations Floor | 800 | Operator workstations, primary displays | Raised floor, low noise, dimmable lighting |
| Server Room | 400 | Core compute, networking, storage | Dedicated HVAC (68°F), fire suppression, access ctrl |
| Communications Room | 200 | RF equipment, antenna interfaces | RF shielding, cable trays to roof antennas |
| Equipment Staging | 300 | Drone maintenance, battery storage | Ventilation, fire-rated battery cabinets |
| Briefing Room | 250 | Mission planning, shift briefings | Display wall, whiteboard, network access |
| NOC/Support | 200 | Network monitoring, IT support | Adjacent to server room |
| Common Area | 200 | Break room, storage | Standard |
| Entry/Security | 150 | Badge access, visitor logging | Access control, camera |
6.2 Server Infrastructure
| Role | Spec | Qty | Notes |
| Safety Supervisor Node | Safety-rated SBC, ECC RAM, RTOS | 2 | Active-standby, physically isolated |
| Real-Time Control Node | Xeon/EPYC, 64 GB ECC, NVMe, 10 GbE | 2 | Active-active, runs ASM + TDE |
| Mission Services Node | Xeon/EPYC, 128 GB, NVMe, 10 GbE | 2 | Active-active, runs MD + FHM + CE |
| AI/ML Inference Node | 64 GB + NVIDIA A4000/L40 GPU | 1 | Dedicated inference, non-safety |
| Data Pipeline Node | 128 GB, high-throughput NVMe RAID | 2 | Kafka brokers + TimescaleDB |
| Operator UI Server | Standard server, 32 GB | 1 | Web UI + WebSocket backend |
6.3 Edge Compute Hardware
- Ruggedized mini-PC (Jetson Orin NX or equiv.) at each dock site
- Local telemetry buffering (minimum 24 hours at full rate)
- Local RF interface for C2 and Remote ID
- Mesh network backhaul to central facility
- Independent power: solar + battery with 72-hour autonomy
6.4 Network Architecture
| Network | Purpose | Media | Bandwidth |
| Safety Bus | SS <-> vehicle safety commands | Dedicated Ethernet + serial | Low BW, < 1 ms |
| Operations LAN A | Primary inter-subsystem | 10 GbE fiber | 10 Gbps |
| Operations LAN B | Redundant inter-subsystem | 10 GbE fiber (sep. path) | 10 Gbps |
| RF Network | C2, Remote ID, ADS-B | 900/2400/1090 MHz | Per-link variable |
| WAN | FAA integration, cloud backup | Dual ISP, MPLS/VPN | 100 Mbps min |
| Edge Backhaul | Dock sites to central | PtP wireless or fiber | 50 Mbps/site |
6.5 Sensor Network
| Sensor | Qty | Purpose | Data Rate |
| ADS-B Receiver (1090ES) | 2 | Cooperative manned traffic awareness | ~1 msg/sec/aircraft |
| Remote ID Receiver | 4+ | UAS position/ID across ops area | Continuous |
| Weather Station | 2 | Wind, temp, visibility, pressure, precip | 1-min interval |
| Ceilometer | 1 | Cloud base height | 30-sec interval |
| Rain/Icing Sensor | 2 | Precipitation type and intensity | 1-min interval |
| PTZ Camera | 4 | Visual monitoring of launch/land sites | 30 fps HD |
| RF Spectrum Monitor | 1 | EMI/RFI detection, link quality | Continuous |
6.6 Drone Dock Infrastructure
Initial deployment: 3-5 automated drone docks. Each dock provides:
- Automated launch and precision landing
- Battery swap or rapid charge system
- Onboard edge compute node and RF ground station
- Weather sensor (wind speed/direction minimum)
- Physical security: locked enclosure, tamper detection, camera
- Power: grid + UPS + solar backup
- Network: primary (fiber/wireless) + cellular failover
7. DATA FLOW ARCHITECTURE
7.1 Event Detection to Dispatch
1. Event trigger received (911 CAD, operator request, scheduled task, API call)
1. Mission Dispatcher validates: mission type, priority, geographic feasibility
1. Fleet Health Manager queried for available, mission-capable vehicles
1. AI Mission Planner generates candidate plans (route, altitude, timing)
1. Compliance Engine evaluates against rules (airspace auth, Remote ID, waiver limits)
1. Airspace Manager reserves operational volume
1. TDE validates separation from all known traffic
1. Operator receives proposal for approval (or auto-approved per policy)
1. Mission Dispatcher issues pre-flight commands to vehicle and dock
7.2 Flight Execution
1. Vehicle pre-flight checks; FHM confirms readiness gates passed
1. Launch command; telemetry stream begins (50 Hz)
1. Telemetry: Vehicle -> Edge Node -> Kafka -> all consumers
1. TDE evaluates separation; ASM tracks airspace occupancy
1. Safety Supervisor independently monitors safety envelope
1. AI Anomaly Detection evaluates telemetry in real-time
1. MD manages waypoint progression and state transitions
1. On-station ops (loiter, deliver, inspect) per mission profile
1. RTL / landing; dock recovery
1. Post-flight data offload, log archival, vehicle state update
7.3 Communication Flows
| Flow | Source | Destination | Protocol | Rate |
| Vehicle telemetry | Vehicle | Edge->Kafka->consumers | MAVLink over C2 RF | 50 Hz |
| Vehicle commands | MD | Vehicle via C2 RF | MAVLink/custom | On-demand |
| Safety commands | SS | Vehicle via ded. RF | Custom safety proto | 50 Hz HB |
| Airspace state | ASM | TDE, MD, OI | Shared memory | 10 Hz |
| Conflict alerts | TDE | MD, SS, OI | Kafka + shmem | Event-driven |
| Operator actions | OI | MD, FHM | WebSocket/gRPC | Event-driven |
| FAA reporting | CE | FAA systems | REST/HTTPS | Batch + event |
| Audit log | All | DP (Kafka->TSDB) | Kafka | Continuous |
7.4 Storage Architecture
| Tier | Technology | Data | Retention |
| Hot | Redis + TimescaleDB | Current state, 24hr telemetry, active missions | 30 days rolling |
| Warm | TimescaleDB + obj store | Historical telemetry, completed missions | 1 year |
| Cold | MinIO local + cloud | Full audit trail, regulatory records, incidents | 7 years (FAA) |
| Stream | Apache Kafka | All event streams, telemetry, commands | 7-day retention |
7.5 Logging and Audit
Every action logged with: timestamp (UTC, microsecond), subsystem ID, action type, actor (human/system/AI), input data hash, output/decision, rationale code. Append-only storage with cryptographic hash chain. FAA inspector access with role-based filtering. Full system state replay from logs for incident reconstruction.
8. FAA / UTM INTEGRATION STRATEGY
8.1 Remote ID Compliance
- Onboard Remote ID module validation as pre-flight readiness gate
- Ground-based receivers verify broadcast compliance of own and third-party UAS
- Remote ID data ingested into traffic picture for non-cooperative awareness
- Data forwarded to FAA Remote ID network when WAN available; locally logged always
8.2 LAANC Integration
- Compliance Engine maintains current UASFM grid data
- Controlled airspace penetration auto-triggers LAANC authorization request
- Approved authorizations cached locally; flights proceed if LAANC temporarily unavailable
- Denials auto-trigger route re-planning to avoid controlled airspace
8.3 ATC Coordination
- Dedicated phone line / radio frequency for UAS-ATC coordination
- Automated notifications to ATC for ops within Class C/D surface area
- ATC hold/release capability: hold command immediately enforced by system
- Future: digital ATC coordination interface per FAA UTM ConOps v2
8.4 Part 108 Readiness
- DAA architecture: cooperative (ADS-B, Remote ID) + non-cooperative (radar, visual) sensor fusion
- Well-clear compliance per ASTM F3442
- Operational volume / contingency volume management per ASTM F3548
- Flight termination system interface for vehicles requiring FTS
- Full operational data recording for post-incident analysis
- Scalable to multi-operator USS interoperability
8.5 External UTM Integration
- Implements USS-to-USS interface per ASTM F3548 for operational intent sharing
- Publishes/consumes operational intents with external UTM networks
- Supports standalone (no external UTM) and federated operation
- DSS client for future FAA UTM ecosystem participation
- Vendor-neutral: supports Wing UTM, OneSky, AirMap, or other USS platforms
9. VENDOR-NEUTRAL FLEET SUPPORT
9.1 Vehicle Abstraction Layer (VAL)
| Layer | Function | Implementation |
| Physical Interface | RF link, telemetry/command encoding | Vendor-specific driver (MAVLink, DJI SDK, proprietary) |
| Protocol Adapter | Translates vendor protocol to canonical messages | Per-vendor adapter plugin (Go/Rust) |
| Canonical Vehicle API | arm, takeoff, goto, RTL, land, payload, telemetry | gRPC service definition, version-controlled |
| Capability Registry | Per-vehicle capabilities: range, payload, speed, sensors | Config database per vehicle type |
9.2 Integration Process
1. Protocol adapter implementation (2-4 weeks engineering)
1. Capability profile definition (performance envelope, sensors, failsafes)
1. Ground station / dock integration (if vendor-specific dock)
1. Safety certification of failsafe behaviors (lost-link, geofence, FTS)
1. Integration test suite: minimum 50 test flights in controlled environment
9.3 Initial Target Platforms
| Platform | Use Case | Protocol | Phase |
| DJI Dock 2 / Matrice 350 | DFR, inspection | DJI Cloud API | Phase 1 |
| Skydio X10 | DFR, inspection, mapping | Skydio SDK / MAVLink | Phase 1 |
| Wingcopter 198 | Medical / commercial delivery | Custom API + MAVLink | Phase 2 |
| Zipline P2 | Medical delivery | Proprietary | Phase 2 |
| Custom VTOL (PX4) | Long-range, heavy payload | MAVLink 2.0 | Phase 2-3 |
10. IMPLEMENTATION ROADMAP
Phase 1: Minimal Operational System (Months 1-6)
Objective: Single-operator, single-vehicle VLOS/EVLOS with manual mission control.
- Deploy initial server infrastructure (2 nodes)
- Core Mission Dispatcher with basic state machine
- Fleet Health Manager for single vehicle type
- Operator Interface v1 (map, manual controls, telemetry)
- Basic Compliance Engine (Part 107, flight logging)
- Single Remote ID receiver + weather station
- Single dock integration (DJI or Skydio)
- LAANC integration for KLFT controlled airspace
Exit: 10 operational missions, Part 107 compliance validated, audit trail complete.
Phase 2: Airspace Awareness (Months 6-12)
Objective: Multi-vehicle operations with traffic awareness and deconfliction.
- Safety Supervisor on dedicated hardware with independent RF
- Airspace Manager with altitude layers and static geofences
- Traffic Deconfliction Engine (strategic)
- ADS-B receiver network + expanded Remote ID coverage
- Dynamic geofencing (NOTAMs, TFRs)
- Second vehicle type (vendor-neutral validated)
- Operator alerting framework
Exit: 5 concurrent vehicles with deconfliction, ADS-B verified, SS failsafe demonstrated.
Phase 3: Automation Expansion (Months 12-24)
Objective: AI-assisted operations, multi-operator, BVLOS readiness.
- AI inference node; Mission Planner AI + Traffic Prediction
- Tactical deconfliction (in-flight re-routing)
- Anomaly Detection (shadow mode -> production)
- Full Compliance Engine with Part 108 rule set
- 3-5 docks with edge compute
- Corridor-based routing
- DAA sensor integration
- USS-to-USS interface for UTM federation
- BVLOS waivers / Part 108 application
Exit: 20+ concurrent ops, AI active, BVLOS waiver or Part 108 submitted.
Phase 4: Regional Scaling (Months 24-36)
Objective: Full regional autonomous airspace operations hub.
- 50+ concurrent vehicle operations
- 10+ dock sites across Acadiana
- Full AI suite (demand forecasting, energy management)
- External UTM federation
- Multi-operator access
- Redundant mission control (backup facility or cloud-hybrid)
- Designation as local airspace management authority
Exit: Sustained high-density, multi-operator, full Part 108, regional coverage.
Budget Estimates
| Phase | Duration | Est. Cost | Key Investments |
| Phase 1 | 6 months | $800K-$1.2M | Facility, hardware, core software, single dock+vehicle |
| Phase 2 | 6 months | $600K-$1.0M | Safety HW, sensors, add'l vehicles, TDE dev |
| Phase 3 | 12 months | $1.5M-$2.5M | AI infra, docks, DAA sensors, BVLOS cert |
| Phase 4 | 12 months | $2.0M-$3.5M | Regional expansion, redundancy, multi-operator |
11. ARCHITECTURE DIAGRAM DESCRIPTION
11.1 Top-Level System Diagram
Layer 0 (bottom): Physical assets — drone fleet, docks, sensors (ADS-B, Remote ID, weather), RF ground stations. Connected via RF and edge network.
Layer 1: Edge compute — ruggedized nodes at each dock providing telemetry processing, C2 relay, buffering. Mesh/PtP wireless to central facility.
Layer 2: Central compute — server cluster running all eight subsystems. Dual-redundant for safety-critical. Dual 10 GbE + shared memory bus.
Layer 3: Application — Operator Interface, API gateway, FAA integration. Accessible from Operations Floor.
Layer 4 (top): External — FAA LAANC, Remote ID network, UTM providers, 911 CAD, cloud backup. Via dual ISP WAN.
Cross-cutting: Safety Supervisor on independent hardware with dedicated RF, depicted as separate vertical column spanning L0-L2.
11.2 Data Flow Diagram
Directed graph: Event source -> MD -> [CE, ASM, FHM] -> AI Planner -> TDE validation -> Operator approval -> Vehicle command -> Telemetry return -> DP -> [Storage, AI training, Audit]. SS shown as parallel monitor with independent command path.
12. RECOMMENDED TECHNOLOGY STACK
| Component | Technology | Rationale |
| Safety Supervisor | Rust on RTOS (Zephyr/VxWorks) | Memory safety, deterministic, safety-critical |
| ASM / TDE core | Rust / C++ | Performance, low-latency, deterministic |
| Mission Dispatcher | Go | Concurrency, reliability, operational tooling |
| Fleet Health Manager | Go + Python | Go service; Python for vendor SDK integration |
| Compliance Engine | OPA + PostgreSQL | Declarative rules, auditability, versioning |
| Data Pipeline | Kafka + TimescaleDB + Redis | Stream processing, time-series, fast cache |
| AI/ML Inference | PyTorch + ONNX + TensorRT | Flexibility, optimized GPU inference |
| Operator Interface | React + Deck.gl/MapLibre + WS | HW-accelerated maps, real-time |
| Object Storage | MinIO (local) + S3 cloud | Local-first with cloud backup |
| Orchestration | K3s | Lightweight K8s for small cluster |
| Monitoring | Prometheus + Grafana | Industry-standard observability |
| Vehicle Protocol | MAVLink 2.0 + vendor adapters | De facto standard, extensible |
13. MAJOR ENGINEERING RISKS
| Risk | Severity | Likelihood | Mitigation |
| Part 108 delayed/differs from assumptions | High | Medium | Modular compliance engine; design to current waiver standards |
| RF reliability in Gulf Coast weather | High | High | Triple-redundant links, aggressive lost-link timeouts |
| Vendor lock-in (dock/vehicle) | Medium | High | VAL architecture; multi-vendor strategy |
| AI model drift | Medium | Medium | Continuous monitoring, deterministic validation gates |
| Cybersecurity on C2 | Critical | Low-Med | Encrypted C2, freq hopping, segmentation, pen testing |
| TDE scaling at 50+ vehicles | Medium | Medium | Lock-free C++, horizontal scaling, load test at 2x |
| Key personnel dependency | Medium | High | Documentation-first, cross-training, modular arch |
| FAA authorization delays | High | High | Phased approach; build data for waiver applications |
| Hurricane facility damage | High | Low | Generator, cloud replication, facility hardening |
END OF DOCUMENT
KLFT Autonomous Airspace Operations Hub — System Architecture v1.0