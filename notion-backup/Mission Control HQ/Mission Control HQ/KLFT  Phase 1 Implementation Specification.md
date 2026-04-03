# KLFT — Phase 1 Implementation Specification
*Notion backup — 2026-04-03*

AUTONOMOUS AIRSPACE OPERATIONS HUB
PHASE 1 IMPLEMENTATION SPECIFICATION
Detailed Build Plan, Sprint Breakdown, API Contracts & Database Schemas
Lafayette Regional Airport (KLFT), Louisiana
Companion to: System Architecture Design Document v1.0
Document Version: 1.0 | February 2026
CLASSIFICATION: ENGINEERING DRAFT
1. PHASE 1 SCOPE AND OBJECTIVES
1.1 Mission Statement
Phase 1 delivers the Minimum Operational System (MOS): a single-operator, single-vehicle-type mission control capability supporting VLOS and EVLOS drone operations from KLFT. This system establishes the foundational software, hardware, and operational infrastructure upon which all subsequent phases build.
1.2 Phase 1 Operational Capabilities
| Capability | Description | Validation Criteria |
| Manual mission dispatch | Operator creates, approves, and monitors a drone mission end-to-end | Mission lifecycle from request through post-flight log in < 5 min |
| Single vehicle type support | One drone platform fully integrated (Skydio X10 + Skydio Dock) | Vehicle responds to all canonical commands; telemetry displayed in UI |
| Real-time telemetry display | Live position, altitude, battery, heading, speed on operator map | < 500 ms display latency from vehicle to screen |
| Flight logging and audit | Every flight event recorded with timestamp, actor, and decision rationale | Complete audit trail recoverable for any test flight |
| Part 107 compliance | All flights evaluated against Part 107 rules before approval | Compliance Engine blocks non-compliant mission plans |
| LAANC authorization | Automated LAANC request for flights in KLFT controlled airspace | Authorization received and cached; denial triggers route block |
| Remote ID verification | Vehicle Remote ID broadcast confirmed before launch | Pre-flight gate rejects launch if Remote ID not broadcasting |
| Basic fleet health | Battery SoC, GPS lock, IMU status tracked per vehicle | Pre-flight readiness gate enforced; under-threshold vehicles grounded |
| Single dock operations | Automated launch and recovery from one dock station | 10 consecutive autonomous dock cycles without manual intervention |
1.3 Explicitly Out of Scope (Phase 1)
- Multi-vehicle concurrent operations (Phase 2)
- Traffic deconfliction engine (Phase 2)
- Safety Supervisor on independent hardware (Phase 2)
- AI/ML components (Phase 3)
- ADS-B integration (Phase 2)
- BVLOS operations (Phase 3)
- Multi-operator access (Phase 4)
- UTM federation (Phase 3-4)
1.4 Exit Criteria
1. 10 successful end-to-end operational missions (dispatch through post-flight)
1. Zero unhandled safety events during test flights
1. Complete audit trail for all 10 missions passes FAA-style review
1. LAANC integration demonstrated with live authorization
1. Remote ID pre-flight gate demonstrated (block launch on failure)
1. Dock automated cycle demonstrated (10 consecutive without manual intervention)
1. Operator Interface supports full mission lifecycle without CLI/backend access
1. System operates for 8 continuous hours without restart or manual recovery
2. TEAM STRUCTURE AND ROLES
2.1 Core Engineering Team
| Role | Count | Responsibilities | Key Skills |
| Technical Lead / Architect | 1 | System design decisions, sprint planning, integration oversight, FAA coordination | Distributed systems, UAS, safety-critical design |
| Backend Engineer (Mission Services) | 2 | Mission Dispatcher, Fleet Health Manager, Compliance Engine | Go, PostgreSQL, gRPC, state machines |
| Backend Engineer (Data Pipeline) | 1 | Kafka setup, TimescaleDB schema, telemetry ingestion, logging | Kafka, TimescaleDB, Redis, data engineering |
| Frontend Engineer | 1 | Operator Interface, map rendering, WebSocket integration, alerting UI | React, Deck.gl/MapLibre, WebSocket |
| Integration Engineer | 1 | Vehicle abstraction layer, dock integration, RF/C2 link management, edge node | MAVLink, Skydio SDK, embedded Linux, RF systems |
| DevOps / Infrastructure | 1 | Server provisioning, K3s, networking, CI/CD, monitoring | Kubernetes, Ansible, Prometheus, networking |
| UAS Operations Specialist | 1 | Flight test planning, Part 107 compliance, LAANC coordination, safety procedures | Part 107 certified, operational experience |
2.2 External Dependencies
| Dependency | Provider | Deliverable | Timeline |
| Facility build-out | General contractor | Server room, ops floor, power, HVAC, antenna mounts | Months 1-3 |
| Network installation | ISP / network contractor | Dual ISP, LAN cabling, rack infrastructure | Months 1-2 |
| Drone platform vendor | Skydio | Dock hardware, SDK access, technical support | Month 1 (procurement) |
| LAANC USS provider | Airmap / DroneUp / Aloft | API access, test environment, production credentials | Month 2 |
| FAA coordination | FAA regional office | Part 107 waiver review, KLFT airspace coordination | Ongoing from Month 1 |
3. SPRINT BREAKDOWN
Phase 1 spans 26 weeks (6 months), organized into 13 two-week sprints across four work streams. Sprints are grouped into three stages: Foundation (S1-S4), Core Build (S5-S9), and Integration & Test (S10-S13).
3.1 Stage 1: Foundation (Sprints 1-4, Weeks 1-8)
Sprint 1 (Weeks 1-2): Infrastructure Bootstrap
| Task | Owner | Deliverable | Done When |
| Provision server hardware | DevOps | 2 server nodes racked, powered, networked | Nodes accessible via SSH, health checks green |
| Install base OS + K3s cluster | DevOps | Ubuntu 22.04 + K3s on both nodes | kubectl get nodes shows 2 Ready nodes |
| Deploy PostgreSQL (HA) | DevOps | Streaming replication primary/standby | Failover test passes; < 1 sec switchover |
| Deploy Kafka cluster (2 broker) | Data Pipeline | Kafka + Zookeeper on pipeline node | Topic create/produce/consume verified |
| Deploy Redis | Data Pipeline | Redis instance for hot cache | Read/write benchmark passes |
| Deploy TimescaleDB | Data Pipeline | TimescaleDB extension on PostgreSQL | Hypertable creation verified |
| CI/CD pipeline setup | DevOps | GitHub Actions / GitLab CI with container builds | Push to main triggers build + deploy to staging |
| Monitoring stack | DevOps | Prometheus + Grafana + node exporters | Dashboard shows CPU/mem/disk for all nodes |
| Network segmentation | DevOps | VLANs: operations, management, external | Ping tests confirm isolation |
Sprint 2 (Weeks 3-4): Data Layer & Schemas
| Task | Owner | Deliverable | Done When |
| Mission database schema | Backend (MS) | PostgreSQL tables: missions, mission_events, mission_plans | Migrations run clean; seed data loads |
| Vehicle database schema | Backend (MS) | Tables: vehicles, vehicle_status, vehicle_config, maintenance_log | CRUD operations verified |
| Compliance database schema | Backend (MS) | Tables: rules, rule_evaluations, authorizations, audit_log | Audit query returns complete trail |
| Telemetry ingestion pipeline | Data Pipeline | Kafka topic -> TimescaleDB hypertable for telemetry | Simulated 50 Hz stream persists correctly |
| Event sourcing framework | Backend (MS) | Append-only event log with replay capability | Event replay reconstructs mission state |
| API gateway setup | DevOps | Kong / Traefik with auth, rate limiting, CORS | API routes accessible with JWT auth |
| Facility: server room complete | Contractor | HVAC, power, rack, fire suppression operational | Temperature holds 68°F under load |
Sprint 3 (Weeks 5-6): Core Service Scaffolding
| Task | Owner | Deliverable | Done When |
| Mission Dispatcher service scaffold | Backend (MS) | Go service with gRPC + REST, health check, config | Service starts, responds to health probe |
| Mission state machine v1 | Backend (MS) | States: DRAFT, VALIDATED, APPROVED, PREFLIGHT, ACTIVE, RTL, COMPLETE, ABORTED | State transitions logged; invalid transitions rejected |
| Fleet Health Manager scaffold | Backend (MS) | Go service with vehicle registry, status polling | Service registers test vehicle, returns status |
| Compliance Engine scaffold | Backend (MS) | OPA rule engine with Part 107 base rule set | Rule eval returns PASS/FAIL for test mission |
| Telemetry consumer service | Data Pipeline | Kafka consumer writes to TSDB + publishes to Redis | Real-time read from Redis matches Kafka input |
| Operator Interface scaffold | Frontend | React app shell, auth flow, empty map view | Login -> map view renders; WebSocket connected |
| Edge node provisioning | Integration | Jetson Orin NX imaged, networked to central | Edge node reachable, telemetry relay test passes |
Sprint 4 (Weeks 7-8): Vehicle Integration Start
| Task | Owner | Deliverable | Done When |
| Vehicle Abstraction Layer (VAL) core | Integration | gRPC interface definition for canonical vehicle commands | Proto file reviewed and approved by team |
| Skydio SDK adapter | Integration | Protocol adapter translating vendor API to VAL | Adapter connects to dock, reads vehicle telemetry |
| Telemetry bridge: vehicle -> Kafka | Integration | Edge node captures vendor telemetry, publishes to Kafka topic | Telemetry visible in TimescaleDB within 500 ms |
| Command bridge: GCS -> vehicle | Integration | Canonical commands (arm, takeoff, goto, land) relayed to vehicle | Vehicle responds to each command in bench test |
| Pre-flight check framework | Backend (MS) | FHM evaluates readiness gates: battery, GPS, IMU, Remote ID | Gate blocks launch when threshold not met |
| Remote ID verification module | Integration | Reads vehicle Remote ID broadcast via ground receiver | Receiver confirms broadcast; pre-flight gate passes |
| Dock control adapter | Integration | Dock open/close, launch/recover commands via vendor API | Dock cycles open-close 5 times without error |
3.2 Stage 2: Core Build (Sprints 5-9, Weeks 9-18)
Sprint 5 (Weeks 9-10): Mission Lifecycle v1
| Task | Owner | Deliverable | Done When |
| Mission creation API | Backend (MS) | POST /missions with route, vehicle, priority, payload type | Mission created with valid ID, persisted to DB |
| Mission validation pipeline | Backend (MS) | Sequential: FHM readiness -> CE compliance -> route feasibility | Invalid missions rejected with specific failure reason |
| Mission approval workflow | Backend (MS) | Operator approve/reject via API; state transitions logged | Approved mission moves to PREFLIGHT state |
| LAANC integration v1 | Backend (MS) | CE sends LAANC request via USS API; caches approval | Live LAANC test returns authorization for KLFT ops |
| Operator UI: mission creation form | Frontend | Map-based route drawing, vehicle selection, parameter entry | Operator creates mission entirely through UI |
| Operator UI: mission list/status | Frontend | Table of missions with real-time status badges | Status updates within 1 sec of backend change |
| Simulated flight testing | Integration | MAVLink SITL generates realistic telemetry through full pipeline | Simulated flight appears correctly on operator map |
Sprint 6 (Weeks 11-12): Real-Time Operations
| Task | Owner | Deliverable | Done When |
| Live telemetry map display | Frontend | Vehicle icon on map with position, heading, altitude, speed | Position updates at 2 Hz minimum on map |
| Telemetry detail panel | Frontend | Side panel showing battery, GPS sats, IMU, motor status | All fields update in real-time during flight |
| Mission execution engine | Backend (MS) | MD sequences: preflight -> launch -> waypoints -> RTL -> land | Automated mission completes without manual intervention |
| Waypoint progression logic | Backend (MS) | MD advances waypoints based on vehicle proximity threshold | Vehicle follows full route; MD reports completion |
| Alert framework v1 | Backend (MS) | Event bus for alerts: INFO, CAUTION, WARNING, EMERGENCY | Alert raised and displayed in UI within 500 ms |
| Alert display in UI | Frontend | Toast + alert panel with severity color coding and acknowledgment | Operator sees and acknowledges test alert |
| Flight log recording | Data Pipeline | Complete flight log: events, telemetry summary, compliance results | Log retrievable for any completed mission |
Sprint 7 (Weeks 13-14): Compliance & Audit
| Task | Owner | Deliverable | Done When |
| Part 107 rule set complete | Backend (MS) | OPA rules: altitude < 400ft, daylight, VLOS, yield to manned | All Part 107 constraints evaluated; test cases pass |
| Rule evaluation audit trail | Backend (MS) | Every rule eval logged: rule ID, input, result, timestamp | Audit query returns complete eval chain for any mission |
| LAANC denial handling | Backend (MS) | Denied auth -> mission blocked -> operator notified -> re-plan offered | Simulated denial correctly blocks mission |
| Remote ID compliance logging | Integration | Broadcast status logged throughout flight; gap alerts raised | Compliance report shows 100% broadcast for test flight |
| Flight log export (PDF/CSV) | Data Pipeline | Export endpoint generates FAA-compatible flight summary | Exported log matches all recorded events |
| Audit dashboard v1 | Frontend | Searchable mission history with filter by date, vehicle, operator, status | Query returns correct results; pagination works |
| Compliance report generator | Backend (MS) | Automated daily/weekly compliance summary | Report generated on schedule; content verified |
Sprint 8 (Weeks 15-16): Dock Integration & Fleet Ops
| Task | Owner | Deliverable | Done When |
| Dock state machine | Integration | States: IDLE, OPENING, LAUNCHING, RECOVERING, CLOSING, CHARGING, FAULT | All transitions verified; fault recovery tested |
| Automated launch sequence | Integration | MD triggers dock open -> vehicle arm -> takeoff -> dock close | Automated launch completes in < 90 sec |
| Automated recovery sequence | Integration | Vehicle approach -> dock open -> precision land -> dock close -> charge | Recovery completes without manual positioning |
| Battery management v1 | Backend (MS) | FHM tracks battery SoC, cycle count, health estimate per battery | Low battery blocks mission; charge status visible in UI |
| Dock status in UI | Frontend | Dock icon on map with status, vehicle occupancy, charge level | Status updates match actual dock state |
| Weather station integration | Integration | Edge node reads weather data, publishes to Kafka | Wind/temp/visibility available in operator UI |
| Weather-based go/no-go | Backend (MS) | CE evaluates weather against Part 107 minimums | High wind correctly blocks new missions |
Sprint 9 (Weeks 17-18): Operator Workflow Polish
| Task | Owner | Deliverable | Done When |
| Mission templates | Frontend + Backend | Pre-defined mission types: DFR, inspection, delivery with default params | Operator selects template; fields auto-populated |
| Operator action logging | Backend (MS) | Every UI action (click, approve, override) recorded with timestamp | Action log complete for 1-hour test session |
| Manual override controls | Frontend | Emergency RTL button, mission abort, vehicle hold | Override command reaches vehicle within 2 sec |
| Role-based access control | Backend (MS) + Frontend | Roles: admin, operator, viewer with permission gates | Viewer cannot approve missions; operator can |
| Notification system | Frontend | Browser notifications + audio alerts for WARNING/EMERGENCY | Alert sounds when test warning generated |
| Session management | Backend (MS) | JWT auth with refresh, session timeout, audit of logins | Expired session forces re-auth |
| Performance optimization | All | UI renders at 60 fps with 1 vehicle; API p99 < 200 ms | Load test results within targets |
3.3 Stage 3: Integration & Test (Sprints 10-13, Weeks 19-26)
Sprint 10 (Weeks 19-20): End-to-End Integration
| Task | Owner | Deliverable | Done When |
| Full pipeline integration test | All | Mission request -> validation -> launch -> flight -> land -> log | 5 SITL missions complete without manual intervention |
| Dock + vehicle + GCS integration | Integration | Real hardware: dock opens, vehicle launches, flies route, returns | 3 live flights complete on test range |
| LAANC live integration test | Backend (MS) | Real LAANC authorization for KLFT airspace operation | Authorization received from production USS |
| Remote ID end-to-end | Integration | Vehicle broadcasts, ground receiver confirms, compliance logged | Compliance log shows full-flight coverage |
| Failsafe testing (simulated) | Integration | Simulate lost C2: vehicle executes RTL per lost-link procedure | Vehicle returns within expected time window |
| Data integrity verification | Data Pipeline | Compare vehicle-side logs vs. GCS logs vs. TimescaleDB records | < 0.1% telemetry message loss |
| Load test: sustained ops | DevOps | 8-hour continuous operation with simulated telemetry | No service restarts, memory leaks, or DB growth anomalies |
Sprint 11 (Weeks 21-22): Flight Test Campaign (Part A)
| Task | Owner | Deliverable | Done When |
| Flight test plan document | UAS Ops | Formal test plan: objectives, procedures, safety mitigations, go/no-go | Plan reviewed and signed by Tech Lead + UAS Ops |
| Test flights 1-3: basic operations | UAS Ops + Integration | Takeoff, hover, waypoint nav, RTL from dock | All 3 flights complete; logs clean |
| Test flights 4-5: mission profiles | UAS Ops + Integration | Simulated DFR response and inspection orbit patterns | Mission profiles execute as designed |
| Test flights 6-7: compliance validation | UAS Ops + Backend | Verify LAANC auth, Remote ID, altitude limits during live flight | Compliance checks pass for all flights |
| Defect triage and fixes | All | Priority bugs from flights 1-7 resolved | P0/P1 defects closed; P2 documented |
| Operator feedback collection | UAS Ops + Frontend | Structured feedback on UI usability, workflow efficiency | Feedback logged; critical items scheduled for S12 |
Sprint 12 (Weeks 23-24): Flight Test Campaign (Part B)
| Task | Owner | Deliverable | Done When |
| Test flights 8-10: exit criteria flights | UAS Ops + All | Three complete mission cycles meeting all exit criteria | All 3 flights pass; audit trail verified |
| Dock reliability test | Integration | 10 consecutive automated dock cycles | 10/10 successful without manual intervention |
| Weather response test | UAS Ops | Fly in marginal conditions; verify weather go/no-go logic | System correctly blocks flight when wind exceeds limit |
| UI/UX refinements | Frontend | Fixes from operator feedback in Sprint 11 | Operator confirms improved workflow |
| Security hardening | DevOps | TLS everywhere, API auth audit, network scan, firewall rules | Penetration scan shows no critical/high findings |
| Documentation: operator manual v1 | UAS Ops + All | Step-by-step procedures for all operator workflows | Manual covers all Phase 1 operations |
Sprint 13 (Weeks 25-26): Acceptance & Handoff
| Task | Owner | Deliverable | Done When |
| Exit criteria validation | Tech Lead | Formal review against all 8 exit criteria with evidence | All criteria met with documented evidence |
| System acceptance test | Tech Lead + UAS Ops | Witnessed end-to-end mission by stakeholders | Stakeholder sign-off obtained |
| Operational readiness review | All | Checklist: staffing, procedures, spares, contacts, escalation | All items green or accepted risk documented |
| Phase 2 planning kickoff | Tech Lead | Phase 2 scope confirmed, backlog groomed, team plan | Phase 2 Sprint 1 ready to start |
| Knowledge base + runbooks | DevOps + All | Troubleshooting guides, restart procedures, escalation paths | Runbooks cover top 20 failure scenarios |
| Lessons learned | All | Retrospective document with actionable items for Phase 2 | Document reviewed by full team |
4. API CONTRACTS
4.1 Mission Dispatcher API
Base path: /api/v1/missions. All endpoints require JWT authentication. Request/response format: JSON.
POST /api/v1/missions
Purpose: Create a new mission request.
Request body: { type: string (DFR|INSPECTION|DELIVERY), priority: int (1-6), route: { waypoints: [{lat, lng, alt_agl_ft}], speed_kts: float }, vehicle_id: string | null (auto-assign if null), payload_type: string | null, operator_notes: string | null }
Response 201: { mission_id: uuid, status: DRAFT, created_at: iso8601, estimated_duration_sec: int }
Response 400: { error: string, validation_errors: [{field, message}] }
POST /api/v1/missions/{id}/validate
Purpose: Run validation pipeline (FHM readiness, CE compliance, route feasibility).
Response 200: { mission_id, status: VALIDATED, checks: [{check_name, result: PASS|FAIL, detail}] }
Response 422: { mission_id, status: DRAFT, checks: [{check_name, result: FAIL, detail, remediation}] }
POST /api/v1/missions/{id}/approve
Purpose: Operator approves validated mission for execution.
Response 200: { mission_id, status: APPROVED, approved_by: operator_id, approved_at: iso8601 }
Response 409: Mission not in VALIDATED state.
POST /api/v1/missions/{id}/abort
Purpose: Abort active mission. Vehicle executes RTL.
Response 200: { mission_id, status: ABORTED, abort_reason: string, vehicle_action: RTL }
GET /api/v1/missions/{id}
Purpose: Retrieve full mission state including events, compliance results, telemetry summary.
Response 200: { mission_id, status, type, priority, route, vehicle_id, events: [{timestamp, type, detail}], compliance: {laanc_auth_id, remote_id_status, rule_results}, telemetry_summary: {duration_sec, distance_nm, max_alt_ft, avg_speed_kts} }
GET /api/v1/missions?status={s}&from={ts}&to={ts}&vehicle={id}
Purpose: List missions with filters. Paginated (limit/offset).
4.2 Fleet Health Manager API
Base path: /api/v1/fleet.
GET /api/v1/fleet/vehicles
Response: [{ vehicle_id, type, manufacturer, model, status: READY|GROUNDED|IN_FLIGHT|MAINTENANCE, battery_soc_pct, gps_fix: bool, imu_health: OK|DEGRADED|FAIL, remote_id_active: bool, last_seen: iso8601, flight_hours_total, next_maintenance_due }]
GET /api/v1/fleet/vehicles/{id}/readiness
Purpose: Evaluate vehicle against pre-flight readiness gates.
Response: { vehicle_id, ready: bool, gates: [{gate_name, required_value, actual_value, result: PASS|FAIL}] }
GET /api/v1/fleet/docks
Response: [{ dock_id, location: {lat, lng}, status: IDLE|LAUNCHING|RECOVERING|CHARGING|FAULT, vehicle_id: string|null, battery_charge_pct, weather: {wind_speed_kts, temp_f, visibility_sm} }]
4.3 Compliance Engine API
Base path: /api/v1/compliance.
POST /api/v1/compliance/evaluate
Purpose: Evaluate a mission plan against current rule set.
Request: { mission_plan: {route, altitude, time_window, vehicle_type} }
Response: { compliant: bool, evaluations: [{rule_id, rule_name, result: PASS|FAIL|WAIVED, detail, waiver_ref}] }
POST /api/v1/compliance/laanc/authorize
Purpose: Request LAANC authorization for controlled airspace operation.
Request: { operation_area: geojson_polygon, max_altitude_ft: int, start_time: iso8601, end_time: iso8601 }
Response: { authorization_id, status: APPROVED|DENIED|PENDING, valid_from, valid_to, conditions: [string] }
GET /api/v1/compliance/audit?mission_id={id}
Purpose: Retrieve complete audit trail for a mission.
Response: { mission_id, entries: [{timestamp, subsystem, action, actor, input_hash, decision, rationale_code}] }
4.4 Telemetry API (WebSocket)
Endpoint: ws://host/api/v1/telemetry/stream?vehicle_id={id}
Message format (JSON, 2-10 Hz): { vehicle_id, timestamp_utc, lat, lng, alt_msl_ft, alt_agl_ft, heading_deg, speed_kts, battery_soc_pct, battery_voltage, gps_sats, gps_hdop, imu_status, motor_status: [float], remote_id_active, mission_id, waypoint_index }
4.5 Operator Actions API
Base path: /api/v1/operator.
POST /api/v1/operator/override
Purpose: Operator issues manual override command to vehicle.
Request: { vehicle_id, command: RTL|HOLD|LAND|RESUME, confirmation_code: string }
Response: { override_id, command, executed_at, vehicle_ack: bool }
Confirmation code required for RTL, HOLD, LAND commands. Generated by UI with operator confirmation dialog. Logged to audit trail.
5. DATABASE SCHEMAS
5.1 Mission Database (PostgreSQL)
Table: missions
| Column | Type | Constraints | Description |
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique mission identifier |
| type | VARCHAR(32) | NOT NULL, CHECK (DFR, INSPECTION, DELIVERY, TEST) | Mission category |
| priority | SMALLINT | NOT NULL, CHECK (1-6) | Priority level per airspace rules |
| status | VARCHAR(32) | NOT NULL, DEFAULT DRAFT | Current state machine state |
| vehicle_id | UUID | FK -> vehicles.id, NULLABLE | Assigned vehicle (null until assigned) |
| operator_id | UUID | FK -> operators.id, NOT NULL | Creating/owning operator |
| route | JSONB | NOT NULL | Planned route (waypoints, speeds, altitudes) |
| operational_volume | JSONB | NULLABLE | 3D operational volume (generated) |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT now() | Creation timestamp |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT now() | Last state change |
| approved_at | TIMESTAMPTZ | NULLABLE | Operator approval timestamp |
| launched_at | TIMESTAMPTZ | NULLABLE | Actual launch time |
| completed_at | TIMESTAMPTZ | NULLABLE | Mission completion time |
| abort_reason | TEXT | NULLABLE | Reason if aborted |
| telemetry_summary | JSONB | NULLABLE | Post-flight summary stats |
Table: mission_events
| Column | Type | Constraints | Description |
| id | BIGSERIAL | PK | Event sequence ID |
| mission_id | UUID | FK -> missions.id, NOT NULL, INDEX | Parent mission |
| event_type | VARCHAR(64) | NOT NULL | Event category (STATE_CHANGE, WAYPOINT, ALERT, OVERRIDE, etc.) |
| timestamp | TIMESTAMPTZ | NOT NULL, INDEX | Event time (UTC) |
| actor | VARCHAR(64) | NOT NULL | system | operator:{id} | vehicle:{id} |
| detail | JSONB | NOT NULL | Event-specific payload |
| input_hash | VARCHAR(64) | NULLABLE | SHA-256 of input data for audit |
Table: rule_evaluations
| Column | Type | Constraints | Description |
| id | BIGSERIAL | PK | Evaluation sequence ID |
| mission_id | UUID | FK -> missions.id, NOT NULL, INDEX | Evaluated mission |
| rule_id | VARCHAR(128) | NOT NULL | OPA rule identifier |
| rule_version | VARCHAR(32) | NOT NULL | Rule set version |
| result | VARCHAR(16) | NOT NULL, CHECK (PASS, FAIL, WAIVED) | Evaluation outcome |
| input_data | JSONB | NOT NULL | Data evaluated (for reproducibility) |
| detail | TEXT | NULLABLE | Human-readable explanation |
| evaluated_at | TIMESTAMPTZ | NOT NULL, DEFAULT now() | Evaluation timestamp |
Table: laanc_authorizations
| Column | Type | Constraints | Description |
| id | UUID | PK | Authorization ID |
| mission_id | UUID | FK -> missions.id, INDEX | Associated mission |
| uss_provider | VARCHAR(64) | NOT NULL | LAANC USS provider name |
| request_payload | JSONB | NOT NULL | Sent request |
| response_payload | JSONB | NOT NULL | Received response |
| status | VARCHAR(32) | NOT NULL | APPROVED | DENIED | PENDING | EXPIRED |
| valid_from | TIMESTAMPTZ | NULLABLE | Auth validity start |
| valid_to | TIMESTAMPTZ | NULLABLE | Auth validity end |
| requested_at | TIMESTAMPTZ | NOT NULL | Request timestamp |
| responded_at | TIMESTAMPTZ | NULLABLE | Response timestamp |
5.2 Fleet Database (PostgreSQL)
Table: vehicles
| Column | Type | Constraints | Description |
| id | UUID | PK | Vehicle unique ID |
| manufacturer | VARCHAR(64) | NOT NULL | e.g., Skydio |
| model | VARCHAR(64) | NOT NULL | e.g., Skydio X10 |
| serial_number | VARCHAR(128) | UNIQUE, NOT NULL | Manufacturer serial |
| remote_id_serial | VARCHAR(128) | UNIQUE, NOT NULL | FAA Remote ID serial number |
| firmware_version | VARCHAR(32) | NOT NULL | Current firmware |
| status | VARCHAR(32) | NOT NULL, DEFAULT GROUNDED | READY | GROUNDED | IN_FLIGHT | MAINTENANCE |
| flight_hours_total | DECIMAL(10,2) | NOT NULL, DEFAULT 0 | Cumulative flight hours |
| flight_cycles_total | INT | NOT NULL, DEFAULT 0 | Cumulative launch/land cycles |
| next_maintenance_at | DECIMAL(10,2) | NULLABLE | Flight hours trigger for next maintenance |
| registered_at | TIMESTAMPTZ | NOT NULL, DEFAULT now() | System registration date |
| config | JSONB | NOT NULL | Vehicle-specific config (speeds, limits, sensors) |
Table: vehicle_status (time-series in TimescaleDB)
| Column | Type | Constraints | Description |
| time | TIMESTAMPTZ | NOT NULL | Measurement timestamp |
| vehicle_id | UUID | NOT NULL, INDEX | Vehicle reference |
| battery_soc_pct | REAL | NOT NULL | State of charge (0-100) |
| battery_voltage | REAL | NOT NULL | Pack voltage |
| battery_temp_c | REAL | NULLABLE | Battery temperature |
| gps_fix | BOOLEAN | NOT NULL | GPS lock status |
| gps_sats | SMALLINT | NOT NULL | Satellite count |
| gps_hdop | REAL | NOT NULL | Horizontal dilution of precision |
| imu_status | VARCHAR(16) | NOT NULL | OK | DEGRADED | FAIL |
| motor_status | JSONB | NOT NULL | Per-motor RPM/temp/current array |
| remote_id_active | BOOLEAN | NOT NULL | Remote ID broadcasting |
Hypertable partitioned by time (1-day chunks). Retention: 30 days hot, 1 year compressed.
Table: docks
| Column | Type | Constraints | Description |
| id | UUID | PK | Dock unique ID |
| name | VARCHAR(128) | NOT NULL | Human-readable name |
| location_lat | DECIMAL(10,7) | NOT NULL | Latitude |
| location_lng | DECIMAL(10,7) | NOT NULL | Longitude |
| location_alt_msl_ft | REAL | NOT NULL | Altitude MSL |
| manufacturer | VARCHAR(64) | NOT NULL | Dock manufacturer |
| model | VARCHAR(64) | NOT NULL | Dock model |
| status | VARCHAR(32) | NOT NULL, DEFAULT IDLE | IDLE | OPENING | LAUNCHING | RECOVERING | CLOSING | CHARGING | FAULT |
| vehicle_id | UUID | FK -> vehicles.id, NULLABLE | Currently docked vehicle |
| charge_pct | REAL | NULLABLE | Current charge level if charging |
| last_maintenance_at | TIMESTAMPTZ | NULLABLE | Last maintenance date |
| config | JSONB | NOT NULL | Dock-specific config |
5.3 Telemetry Database (TimescaleDB Hypertable)
Table: telemetry
| Column | Type | Constraints | Description |
| time | TIMESTAMPTZ | NOT NULL | Telemetry timestamp (vehicle clock, UTC) |
| vehicle_id | UUID | NOT NULL | Vehicle reference |
| mission_id | UUID | NULLABLE | Active mission (null if not on mission) |
| lat | DOUBLE PRECISION | NOT NULL | Latitude (WGS84) |
| lng | DOUBLE PRECISION | NOT NULL | Longitude (WGS84) |
| alt_msl_ft | REAL | NOT NULL | Altitude MSL feet |
| alt_agl_ft | REAL | NOT NULL | Altitude AGL feet (from terrain model or rangefinder) |
| heading_deg | REAL | NOT NULL | Heading (0-360 true north) |
| speed_kts | REAL | NOT NULL | Ground speed knots |
| vertical_speed_fpm | REAL | NOT NULL | Vertical speed feet/min |
| battery_soc_pct | REAL | NOT NULL | Battery state of charge |
| gps_sats | SMALLINT | NOT NULL | GPS satellite count |
| remote_id_active | BOOLEAN | NOT NULL | Remote ID status |
Hypertable partitioned by time (1-hour chunks for high-rate data). Continuous aggregate: 1-min downsampled view for historical queries. Retention: raw 30 days, aggregate 1 year, exported to cold storage at 1 year.
5.4 Audit Database (PostgreSQL, Append-Only)
Table: audit_log
| Column | Type | Constraints | Description |
| id | BIGSERIAL | PK | Monotonic sequence |
| timestamp | TIMESTAMPTZ | NOT NULL, INDEX | Event time UTC |
| subsystem | VARCHAR(32) | NOT NULL | MD | FHM | CE | OI | DP | VAL |
| action | VARCHAR(128) | NOT NULL | Action performed |
| actor | VARCHAR(128) | NOT NULL | system | operator:{id} | vehicle:{id} | api:{client_id} |
| resource_type | VARCHAR(64) | NOT NULL | mission | vehicle | dock | authorization | rule |
| resource_id | VARCHAR(128) | NOT NULL | ID of affected resource |
| input_hash | VARCHAR(64) | NOT NULL | SHA-256 of input/request |
| output_hash | VARCHAR(64) | NOT NULL | SHA-256 of output/response |
| decision | VARCHAR(32) | NOT NULL | Result: APPROVED, DENIED, EXECUTED, FAILED, etc. |
| rationale_code | VARCHAR(64) | NOT NULL | Machine-readable reason code |
| detail | JSONB | NULLABLE | Additional context |
| prev_hash | VARCHAR(64) | NOT NULL | SHA-256 of previous audit entry (hash chain) |
No UPDATE or DELETE permitted on this table (enforced via database role permissions). Hash chain provides tamper evidence. Index on (subsystem, timestamp), (resource_type, resource_id), and (actor).
6. INFRASTRUCTURE SPECIFICATION
6.1 Server Hardware (Phase 1 Minimum)
| Node | Hardware | OS | Services | Est. Cost |
| Node A (Mission) | Dell R660xs / HPE DL360: Xeon 4416+, 128GB ECC, 2x 1.92TB NVMe, 10GbE dual | Ubuntu 22.04 LTS | K3s worker: MD, FHM, CE, OI backend, API gateway | $8,000-$12,000 |
| Node B (Data) | Dell R660xs / HPE DL360: Xeon 4416+, 128GB ECC, 4x 3.84TB NVMe RAID-10, 10GbE dual | Ubuntu 22.04 LTS | K3s worker: Kafka (2 broker), TimescaleDB, Redis, Prometheus, Grafana | $12,000-$16,000 |
| Edge Node (Dock) | NVIDIA Jetson Orin NX 16GB, 256GB NVMe, weatherproof enclosure | Ubuntu 22.04 + JetPack | Telemetry relay, C2 bridge, local buffer, weather sensor interface | $2,000-$3,000 |
6.2 Network Equipment
| Item | Spec | Qty | Est. Cost |
| Managed switch (10GbE) | 24-port, 4x SFP+ uplink (e.g., Ubiquiti USW-Enterprise) | 2 | $1,500 |
| Firewall/router | pfSense/OPNsense appliance, dual WAN | 1 | $1,000 |
| Wireless backhaul | Ubiquiti airFiber 60 LR or similar PtP link to dock site | 1 pair | $1,500 |
| UPS | APC Smart-UPS 3000VA, 30 min runtime at load | 2 | $3,000 |
| Generator | 20 kW diesel, auto-transfer switch | 1 | $15,000 |
| Rack | 42U server rack with PDU, cable management | 1 | $2,000 |
6.3 Sensor Equipment
| Item | Spec | Qty | Est. Cost |
| Remote ID receiver | ANRA / Thales / open-source SDR-based | 1 | $2,000-$5,000 |
| Weather station | Davis Vantage Pro2 or equiv (wind, temp, humidity, pressure, rain) | 1 | $1,500 |
| Antenna (C2) | Dual-band 900 MHz / 2.4 GHz directional + omni | 1 set | $800 |
| PTZ camera | Axis Q6135-LE or equiv, 30 fps, weatherproof | 1 | $3,000 |
6.4 Drone Platform (Phase 1)
| Item | Spec | Qty | Est. Cost |
| Skydio Dock 2 | Automated dock with charging, weather resistant | 1 | $12,000-$15,000 |
| Skydio Skydio X10 | Multi-sensor drone, 55 min flight time, RTK GPS | 1 | $8,000-$11,000 |
| Spare batteries | Skydio TB65 battery pairs | 3 pairs | $2,400 |
| Payload (camera) | Zenmuse H30T (wide + zoom + thermal + rangefinder) | 1 | $10,000-$13,000 |
Alternative: Skydio X10 + Skydio Dock at comparable cost. Decision by Month 1 based on SDK maturity and KLFT operational needs.
6.5 Total Phase 1 Hardware Budget Estimate
| Category | Low Estimate | High Estimate |
| Servers (2 nodes) | $20,000 | $28,000 |
| Edge compute | $2,000 | $3,000 |
| Network equipment | $24,000 | $30,000 |
| Sensors | $7,300 | $10,300 |
| Drone platform + dock | $32,400 | $42,400 |
| Facility build-out | $150,000 | $250,000 |
| Contingency (15%) | $35,400 | $54,600 |
| TOTAL HARDWARE | $271,100 | $418,300 |
7. DEVELOPMENT ENVIRONMENT AND CI/CD
7.1 Repository Structure
Monorepo with service-specific directories:
- / - Root: CI/CD configs, deployment manifests, documentation
- /services/mission-dispatcher - Go service
- /services/fleet-health-manager - Go service
- /services/compliance-engine - Go + OPA rules
- /services/data-pipeline - Kafka configs, consumers, TSDB migrations
- /services/operator-ui - React application
- /services/vehicle-abstraction - Go/Rust protocol adapters
- /services/api-gateway - Kong/Traefik configuration
- /deploy - K3s manifests, Helm charts
- /migrations - All database migrations (Flyway/golang-migrate)
- /tests - Integration tests, E2E tests
- /docs - Architecture docs, API specs (OpenAPI), runbooks
7.2 CI/CD Pipeline
| Stage | Trigger | Actions | Gate |
| Lint + Unit Test | Every push | Go test, ESLint, OPA test, schema validation | All pass |
| Build | PR merge to main | Docker build for each changed service | Build succeeds |
| Integration Test | Post-build | Spin up test env, run API integration suite | All pass |
| Security Scan | Post-build | Trivy container scan, SAST (gosec, eslint-security) | No critical/high |
| Deploy to Staging | Auto on main | K3s rolling update to staging namespace | Health checks pass |
| Deploy to Production | Manual approval | K3s rolling update to production namespace | Operator approval + staging test pass |
7.3 Development Standards
- Language: Go 1.22+ for backend services, React 18+ for UI, Rust for VAL adapters where performance-critical
- API specification: OpenAPI 3.1 for REST, Protobuf for gRPC; spec-first development
- Database migrations: Version-controlled, forward-only, reviewed before merge
- Code review: All changes require 1 approval; safety-related changes require Tech Lead approval
- Testing: Minimum 80% unit test coverage for backend services; integration tests for all API endpoints
- Documentation: Each service has README with setup, API, configuration, troubleshooting
8. TESTING STRATEGY
8.1 Test Levels
| Level | Scope | Tools | Frequency |
| Unit | Individual functions, modules | Go testing, Jest, OPA test | Every commit |
| Service | Single service API contract | Testcontainers, mock dependencies | Every PR |
| Integration | Multi-service interaction | Docker Compose test environment | Daily / PR to main |
| End-to-End | Full mission lifecycle (simulated) | SITL + full stack | Weekly / pre-release |
| Hardware-in-Loop | Real vehicle + real dock + real sensors | Test range at KLFT | Sprint 10-12 |
| Acceptance | Exit criteria validation with stakeholders | Live flight + audit review | Sprint 13 |
8.2 Simulated Flight Environment
A MAVLink Software-In-The-Loop (SITL) environment provides realistic vehicle telemetry without physical hardware:
- ArduPilot SITL generates MAVLink telemetry at 50 Hz with realistic GPS, IMU, battery simulation
- Simulated dock responds to dock commands with realistic timing
- Simulated weather feed provides configurable conditions
- Environment runs in Docker alongside application stack for CI integration tests
- Supports multi-vehicle simulation for Phase 2 readiness testing
8.3 Flight Test Plan Summary
| Test ID | Objective | Success Criteria | Phase |
| FT-001 | Basic launch/hover/land from dock | Vehicle launches, hovers 30 sec at 50 ft, lands on dock | S11 |
| FT-002 | Waypoint navigation | Vehicle follows 5-waypoint route within 10m accuracy | S11 |
| FT-003 | RTL from mission | RTL command results in safe dock recovery | S11 |
| FT-004 | DFR profile simulation | Launch within 90 sec of trigger, fly to target, orbit, RTL | S11 |
| FT-005 | Inspection orbit | Vehicle maintains 100 ft orbit around target for 5 min | S11 |
| FT-006 | LAANC live auth flight | LAANC approval obtained and logged before launch in KLFT airspace | S11 |
| FT-007 | Remote ID verification flight | Ground receiver confirms broadcast throughout entire flight | S11 |
| FT-008 | Exit criteria flight A | Full DFR mission cycle with complete audit trail | S12 |
| FT-009 | Exit criteria flight B | Full inspection mission cycle with complete audit trail | S12 |
| FT-010 | Exit criteria flight C | Full mission with operator override (manual RTL mid-flight) | S12 |
9. PHASE 1 RISK REGISTER
| ID | Risk | Likelihood | Impact | Mitigation | Owner |
| R01 | Dock hardware delivery delayed | Medium | High - blocks flight testing | Order in Week 1; identify backup vendor; SITL testing unblocked | Integration Eng |
| R02 | Skydio Cloud API limitations discovered late | Medium | High - adapter rework | Prototype adapter in Sprint 3; escalate SDK issues to vendor early | Integration Eng |
| R03 | LAANC USS provider integration issues | Low | Medium - compliance testing delayed | Begin integration in Sprint 5; have backup USS provider identified | Backend Eng |
| R04 | Facility build-out delays | Medium | High - server deployment blocked | Temporary rack in existing space as fallback; critical path is power + HVAC | DevOps |
| R05 | Key engineer leaves during Phase 1 | Low | High - knowledge loss | Documentation-first; pair programming; cross-training in Sprints 1-4 | Tech Lead |
| R06 | Weather prevents flight testing in Sprints 11-12 | Medium | Medium - timeline slip | Buffer days built into schedule; SITL testing covers most validation | UAS Ops |
| R07 | Part 107 waiver issues for KLFT operations | Low | High - operations blocked | Begin FAA coordination in Month 1; design within standard Part 107 first | UAS Ops |
| R08 | Telemetry pipeline performance insufficient | Low | Medium - data loss | Load test with 10x target rate in Sprint 2; TimescaleDB tuning guide | Data Pipeline Eng |
| R09 | Cybersecurity vulnerability in API or auth | Medium | High - system compromise | Security scan in CI; penetration test in Sprint 12; TLS everywhere | DevOps |
| R10 | Scope creep from stakeholders | Medium | Medium - timeline slip | Strict Phase 1 scope document; change requests go through Tech Lead | Tech Lead |
10. CRITICAL PATH AND DEPENDENCIES
10.1 Critical Path
The longest dependency chain that determines Phase 1 completion:
1. Server procurement and facility build-out (Weeks 1-8)
1. Vehicle abstraction layer + dock adapter (Weeks 5-8)
1. Mission lifecycle implementation (Weeks 9-14)
1. Dock integration and automated flight (Weeks 15-18)
1. End-to-end integration testing (Weeks 19-20)
1. Flight test campaign (Weeks 21-24)
1. Acceptance and handoff (Weeks 25-26)
Facility and hardware procurement are the earliest critical-path items. Late delivery of dock hardware or facility delays directly impact the timeline.
10.2 Dependency Matrix
| Deliverable | Depends On | Blocks |
| K3s cluster operational | Server hardware, network, facility power | All service deployments |
| Database schemas deployed | K3s cluster | Mission Dispatcher, FHM, CE, Data Pipeline |
| Vehicle adapter functional | VAL proto, vendor SDK, edge node | Mission execution, telemetry display |
| Mission Dispatcher v1 | DB schemas, FHM API, CE API | Mission lifecycle testing |
| Compliance Engine v1 | DB schemas, OPA rule set, LAANC USS API | Mission validation |
| Operator Interface v1 | All backend APIs, WebSocket telemetry | Operator workflow testing |
| Dock integration | Dock hardware, dock adapter, edge node | Flight testing |
| Flight test campaign | All software, dock integration, FAA coordination | Exit criteria validation |
11. PHASE 1 DELIVERABLES SUMMARY
| Deliverable | Type | Acceptance Criteria |
| Mission Dispatcher service | Software | Creates, validates, approves, executes, completes missions via API |
| Fleet Health Manager service | Software | Tracks vehicle state; enforces readiness gates; blocks unready vehicles |
| Compliance Engine service | Software | Evaluates Part 107 rules; integrates LAANC; generates audit trail |
| Data Pipeline | Infrastructure | Ingests 50 Hz telemetry; persists to TimescaleDB; real-time via Redis |
| Operator Interface | Software | Full mission lifecycle via web UI; live map; alerts; override controls |
| Vehicle Abstraction Layer | Software | One vehicle type fully integrated; canonical API for all commands |
| Dock integration | Software + Hardware | Automated launch/recovery; 10 consecutive cycles |
| Edge compute node | Hardware | Telemetry relay; C2 bridge; local buffer; weather sensor interface |
| Sensor deployment | Hardware | 1 Remote ID receiver; 1 weather station; 1 PTZ camera operational |
| Server infrastructure | Hardware | 2-node cluster; K3s; monitoring; backup; UPS + generator |
| Flight test evidence | Documentation | 10 flight logs with complete audit trails |
| Operator manual v1 | Documentation | Step-by-step procedures for all Phase 1 operations |
| Runbooks | Documentation | Top 20 failure scenarios with troubleshooting steps |
END OF DOCUMENT
KLFT Autonomous Airspace Operations Hub — Phase 1 Implementation Specification v1.0