# KLFT — Software Interface Control Document
*Notion backup — 2026-04-06*

AUTONOMOUS AIRSPACE OPERATIONS HUB
SOFTWARE INTERFACE CONTROL DOCUMENT
Message Formats, API Definitions & Data Models
Lafayette Regional Airport (KLFT), Louisiana
Companion to: System Architecture v1.0 & Phase 1 Spec v1.0
Document Version: 1.0 | February 2026
CLASSIFICATION: ENGINEERING DRAFT
1. DOCUMENT PURPOSE AND CONVENTIONS
1.1 Purpose
This Interface Control Document (ICD) defines every inter-subsystem interface in the KLFT Autonomous Airspace Operations Hub. It specifies message formats, API contracts, data models, protocol selections, timing constraints, error handling, and versioning rules. All implementations must conform to these interfaces; deviations require a formal Interface Change Request (ICR) approved by the Technical Lead.
1.2 Scope
Covers all interfaces between: Airspace Manager (ASM), Mission Dispatcher (MD), Safety Supervisor (SS), Fleet Health Manager (FHM), Compliance Engine (CE), Traffic Deconfliction Engine (TDE), Data Pipeline (DP), Operator Interface (OI), Vehicle Abstraction Layer (VAL), and external systems (LAANC, Remote ID, ADS-B, Weather).
1.3 Conventions
| Convention | Definition |
| Timestamps | ISO 8601 UTC microsecond: 2026-02-17T14:30:00.000000Z |
| Identifiers | UUID v4 for entities; BIGINT for event sequences |
| Coordinates | WGS84 decimal degrees; altitudes in feet (MSL/AGL specified) |
| Speeds | Knots (kts) horizontal; feet/min (fpm) vertical |
| Encoding | JSON (REST/WS); Protobuf (gRPC); binary (shared memory) |
| Versioning | Semantic: MAJOR.MINOR.PATCH |
| Error codes | SUBSYSTEM.CATEGORY.SPECIFIC |
2. INTERFACE MATRIX
| ID | Producer -> Consumer | Protocol | Direction | Criticality |
| IF-MD-FHM-001 | MD -> FHM | gRPC | Req/Reply | Mission-Critical |
| IF-MD-CE-001 | MD -> CE | gRPC | Req/Reply | Regulatory-Critical |
| IF-MD-ASM-001 | MD -> ASM | gRPC | Req/Reply | Safety-Critical |
| IF-MD-VAL-001 | MD -> VAL | gRPC | Req/Reply+Stream | Mission-Critical |
| IF-MD-OI-001 | MD -> OI | Kafka+WS | Pub/Sub | Operational |
| IF-MD-DP-001 | MD -> DP | Kafka | Publish | Operational |
| IF-FHM-DP-001 | FHM -> DP | Kafka | Publish | Operational |
| IF-CE-LAANC | CE -> LAANC | REST/HTTPS | Req/Reply | Regulatory |
| IF-ASM-TDE-001 | ASM -> TDE | Shared Mem | 10 Hz pub | Safety-Critical |
| IF-TDE-SS-001 | TDE -> SS | Shared Mem | Emergency | Safety-Critical |
| IF-SS-VAL-001 | SS -> Vehicle | Ded. RF | Command | Safety-Critical |
| IF-VAL-DP-001 | VAL -> DP | Kafka | Telemetry | Mission-Critical |
| IF-VAL-SS-001 | VAL -> SS | Shared Mem | Telem mirror | Safety-Critical |
| IF-OI-MD-001 | OI -> MD | REST/gRPC | Req/Reply | Mission-Critical |
| IF-EXT-RID | Remote ID rx | BT5/WiFi | Broadcast | Regulatory |
| IF-EXT-ADSB | ADS-B rx | 1090ES | Broadcast | Safety-Critical |
| IF-EXT-WX | Weather stn | Serial/UDP | Publish | Operational |
3. gRPC INTERFACE DEFINITIONS
All gRPC use proto3. Conventions: deadline on every RPC, google.rpc.Status errors, x-trace-id metadata, idempotency keys on mutations.
3.1 IF-MD-FHM-001: Mission Dispatcher <-> Fleet Health Manager
RPC: GetVehicleReadiness
Purpose: Query vehicle readiness. Timeout: 500 ms, 1 retry @ 200 ms.
Request: VehicleReadinessRequest
| Field | Type | Description |
| vehicle_id | string (UUID) | Specific vehicle or empty=auto |
| mission_type | MissionType | DFR, INSPECTION, DELIVERY, TEST |
| required_range_nm | float | Minimum range |
| required_payload | PayloadType | CAMERA, THERMAL, LIDAR, DELIVERY_BOX, NONE |
| required_endurance_min | int32 | Minimum flight time |
Response: VehicleReadinessResponse
| Field | Type | Description |
| vehicle_id | string (UUID) | Assigned vehicle |
| ready | bool | Overall result |
| gates | repeated ReadinessGate | Per-gate results |
| estimated_flight_time_min | int32 | Available time |
| recommendation | string | Action if not ready |
ReadinessGate
| Field | Type | Description |
| gate_name | string | BATTERY_SOC, GPS_FIX, IMU_HEALTH, REMOTE_ID, FIRMWARE, MAINTENANCE_DUE |
| required_value | string | Threshold |
| actual_value | string | Current |
| result | GateResult | PASS, FAIL, WARN |
RPC: ReportVehicleStatus
Purpose: VAL pushes health update. Timeout: 200 ms.
| Field | Type | Description |
| vehicle_id | string (UUID) | Identifier |
| timestamp | Timestamp | Measurement time |
| battery_soc_pct | float | 0-100 |
| battery_voltage | float | Pack voltage |
| battery_temp_c | float | Temperature |
| gps_fix | bool | Lock status |
| gps_sats | int32 | Satellites |
| gps_hdop | float | HDOP |
| imu_status | SensorStatus | OK, DEGRADED, FAIL |
| motor_status | repeated MotorStatus | Per-motor |
| remote_id_active | bool | Broadcasting |
| firmware_version | string | Firmware |
3.2 IF-MD-CE-001: Mission Dispatcher <-> Compliance Engine
RPC: EvaluateMission
Purpose: Regulatory eval. Timeout: 2000 ms (incl. LAANC).
Request
| Field | Type | Description |
| mission_id | string (UUID) | Reference |
| mission_type | MissionType | Type |
| route | Route | Waypoints+alt+speed |
| vehicle_type | string | Mfg + model |
| operator_id | string (UUID) | Operator |
| scheduled_start | Timestamp | Departure |
| scheduled_end | Timestamp | Completion |
| waiver_refs | repeated string | Waiver IDs |
Response
| Field | Type | Description |
| compliant | bool | Overall result |
| evaluations | repeated RuleEvaluation | Per-rule |
| laanc_required | bool | Enters controlled airspace |
| laanc_authorization | LaancAuth | If requested |
| blocking_rules | repeated string | Failing rule IDs |
RuleEvaluation
| Field | Type | Description |
| rule_id | string | e.g., PART107.MAX_ALT |
| rule_name | string | Human-readable |
| result | EvalResult | PASS, FAIL, WAIVED, N/A |
| detail | string | Explanation |
| input_snapshot | string(JSON) | Audit data |
RPC: RequestLaancAuthorization
Purpose: LAANC from USS. Timeout: 5000 ms, non-blocking.
Request
| Field | Type | Description |
| operation_area | GeoPolygon | 2D boundary |
| max_altitude_agl_ft | int32 | Requested ceiling |
| start_time | Timestamp | Start |
| end_time | Timestamp | End |
| pilot_id | string | Part 107 cert |
| uas_serial | string | Serial number |
Response
| Field | Type | Description |
| authorization_id | string | USS ID |
| status | LaancStatus | APPROVED, DENIED, PENDING |
| approved_altitude_ft | int32 | Approved ceiling |
| valid_from | Timestamp | Start |
| valid_to | Timestamp | End |
| conditions | repeated string | Conditions |
| denial_reason | string | If denied |
3.3 IF-MD-ASM-001: Airspace Manager
RPC: ReserveOperationalVolume (500 ms)
Request
| Field | Type | Description |
| mission_id | string (UUID) | Reference |
| operational_volume | Volume3D | 3D+time |
| contingency_volume | Volume3D | Extended |
| priority | int32 | 1-6 |
Volume3D
| Field | Type | Description |
| boundary | repeated LatLng | Polygon vertices |
| min_altitude_agl_ft | float | Floor |
| max_altitude_agl_ft | float | Ceiling |
| start_time | Timestamp | Active from |
| end_time | Timestamp | Active until |
| buffer_lateral_ft | float | Lateral buffer |
| buffer_vertical_ft | float | Vertical buffer |
Response
| Field | Type | Description |
| reservation_id | string (UUID) | Reservation |
| status | ReservationStatus | GRANTED, DENIED, MODIFIED |
| granted_volume | Volume3D | Actual |
| conflicts | repeated ConflictInfo | If denied |
RPC: ReleaseVolume
Req: { reservation_id, reason: COMPLETE|ABORT|TIMEOUT } Resp: { released: bool }
RPC: CheckGeofences
Req: { route, time_window } Resp: { clear: bool, intersections[] }
3.4 IF-MD-VAL-001: Vehicle Abstraction Layer
RPC: ExecuteMission (server-streaming)
Request
| Field | Type | Description |
| mission_id | string (UUID) | Reference |
| vehicle_id | string (UUID) | Target |
| commands | repeated VehicleCommand | Command sequence |
| lost_link_action | LostLinkAction | RTL, LAND, LOITER |
| geofence | Volume3D | Hard geofence |
VehicleCommand
| Field | Type | Description |
| sequence | int32 | Order index |
| type | CommandType | ARM, TAKEOFF, GOTO, ORBIT, LOITER, RTL, LAND, DOCK_RECOVER, PAYLOAD_ACTION |
| target | LatLngAlt | Position |
| speed_kts | float | Speed |
| altitude_agl_ft | float | Altitude |
| heading_deg | float | -1=auto |
| orbit_radius_ft | float | For ORBIT |
| duration_sec | int32 | For LOITER |
| payload_action | string | capture_photo, etc. |
Stream: MissionExecutionUpdate
| Field | Type | Description |
| mission_id | string (UUID) | Reference |
| timestamp | Timestamp | Time |
| status | ExecutionStatus | PREFLIGHT, ARMED, AIRBORNE, WAYPOINT_REACHED, ON_STATION, RTL, LANDING, DOCKED, COMPLETE, ABORTED, ERROR |
| current_command_seq | int32 | Current command |
| vehicle_position | LatLngAlt | Position |
| detail | string | Status/error detail |
RPC: SendOverride (200ms operator / 50ms SS)
| Field | Type | Description |
| vehicle_id | string (UUID) | Target |
| command | OverrideType | RTL, HOLD, LAND, RESUME, TERMINATE |
| authority | AuthorityLevel | OPERATOR, SS, ATC |
| confirmation_code | string | For OPERATOR |
| reason | string | Audit reason |
Response: { executed, vehicle_ack, execution_time_ms }
3.5 IF-OI-MD-001: Operator Interface
REST API: Per Phase 1 Spec Section 4. OpenAPI 3.1.
WebSocket Event Stream: ws://host/api/v1/events/stream
| Field | Type | Description |
| event_id | string | Unique ID |
| timestamp | string | ISO 8601 |
| event_type | string | MISSION_CREATED, VALIDATED, APPROVED, LAUNCHED, WAYPOINT_REACHED, COMPLETE, ABORTED, ALERT_RAISED, VEHICLE_STATUS_CHANGE, OVERRIDE_EXECUTED |
| resource_type | string | mission, vehicle, dock, alert |
| resource_id | string | Affected resource |
| severity | string | INFO, CAUTION, WARNING, EMERGENCY |
| payload | object | Event data |
| actor | string | system, operator:{id}, vehicle:{id} |
Heartbeat: ping/pong 15s. Reconnect with last_event_id.
4. KAFKA TOPIC AND MESSAGE DEFINITIONS
4.1 Topic Registry
| Topic | Producer | Consumers | Parts | Ret | Key |
| telemetry.raw | VAL | DP,SS,OI | 6 | 7d | vehicle_id |
| telemetry.processed | DP | OI,AI | 6 | 7d | vehicle_id |
| mission.events | MD | DP,OI,CE | 3 | 30d | mission_id |
| mission.commands | MD | VAL | 3 | 7d | vehicle_id |
| vehicle.status | VAL,FHM | DP,OI,MD | 3 | 7d | vehicle_id |
| dock.status | VAL | DP,OI,FHM | 1 | 7d | dock_id |
| compliance.events | CE | DP,OI | 2 | 30d | mission_id |
| alerts | SS,TDE,FHM | OI,DP | 2 | 30d | alert_id |
| airspace.state | ASM | DP,OI | 1 | 7d | region_id |
| audit.events | All | DP | 3 | 90d | subsystem |
| weather.obs | Edge | DP,CE,OI | 1 | 7d | station_id |
4.2 telemetry.raw (up to 50 Hz, key=vehicle_id)
| Field | Type | Req | Description |
| vehicle_id | UUID | Y | Vehicle |
| mission_id | UUID | N | Mission |
| timestamp_vehicle | ISO8601 | Y | Vehicle clock |
| timestamp_received | ISO8601 | Y | Edge rx time |
| lat | double | Y | Latitude |
| lng | double | Y | Longitude |
| alt_msl_ft | float | Y | Alt MSL |
| alt_agl_ft | float | Y | Alt AGL |
| heading_deg | float | Y | Heading |
| speed_kts | float | Y | Speed |
| vertical_speed_fpm | float | Y | Vert rate |
| battery_soc_pct | float | Y | Battery |
| battery_voltage | float | Y | Voltage |
| gps_sats | int | Y | Sats |
| gps_hdop | float | Y | HDOP |
| imu_status | string | Y | OK/DEGRADED/FAIL |
| remote_id_active | bool | Y | RID |
| motor_rpm | float[] | Y | Per-motor |
| source_protocol | string | Y | mavlink/dji/skydio |
4.3 mission.events (key=mission_id)
| Field | Type | Req | Description |
| mission_id | UUID | Y | Reference |
| event_type | string | Y | STATE_CHANGE, WAYPOINT, VALIDATION, APPROVAL, LAUNCH, ABORT, COMPLETE, OVERRIDE |
| timestamp | ISO8601 | Y | Time |
| previous_state | string | N | Old state |
| new_state | string | N | New state |
| actor | string | Y | Who/what |
| detail | object | Y | Payload |
| input_hash | string | Y | SHA-256 |
4.4 alerts (key=alert_id)
| Field | Type | Req | Description |
| alert_id | UUID | Y | ID |
| timestamp | ISO8601 | Y | Time |
| severity | string | Y | INFO/CAUTION/WARNING/EMERGENCY |
| source_subsystem | string | Y | SS/TDE/FHM/CE/ASM |
| category | string | Y | SAFETY/COMPLIANCE/VEHICLE/AIRSPACE/WEATHER/SYSTEM |
| title | string | Y | Short (<80ch) |
| detail | string | Y | Full desc |
| affected_vehicle_id | string | N | Vehicle |
| affected_mission_id | string | N | Mission |
| recommended_action | string | N | Suggestion |
| auto_action_taken | string | N | Auto action |
| acknowledged | bool | Y | Acked |
| resolved | bool | Y | Cleared |
4.5 audit.events (key=subsystem)
| Field | Type | Req | Description |
| subsystem | string | Y | Source |
| timestamp | ISO8601 | Y | Time |
| action | string | Y | Action |
| actor | string | Y | Who |
| resource_type | string | Y | Type |
| resource_id | string | Y | ID |
| input_hash | string | Y | Input SHA-256 |
| output_hash | string | Y | Output SHA-256 |
| decision | string | Y | Result |
| rationale_code | string | Y | Reason |
| trace_id | string | Y | Trace |
| detail | object | N | Context |
5. SHARED MEMORY INTERFACES
Lock-free single-writer/multi-reader via mmap. Sequence counter for consistency.
5.1 IF-ASM-TDE-001: Airspace State (10 Hz, 2 MB)
Region: /dev/shm/klft_airspace_state
Header
| Offset | Size | Field | Type |
| 0x0000 | 8 | sequence_counter | uint64 |
| 0x0008 | 8 | timestamp_us | uint64 |
| 0x0010 | 4 | num_volumes | uint32 |
| 0x0014 | 4 | num_geofences | uint32 |
| 0x0018 | 4 | num_corridors | uint32 |
| 0x001C | 4 | reserved | uint32 |
Volume3DCompact (64B each, max 256)
| Offset | Size | Field | Type |
| +0 | 16 | reservation_id | UUID |
| +16 | 4 | priority | int32 |
| +20 | 8 | center_lat | double |
| +28 | 8 | center_lng | double |
| +36 | 4 | radius_ft | float |
| +40 | 4 | min_alt_ft | float |
| +44 | 4 | max_alt_ft | float |
| +48 | 8 | valid_from_us | uint64 |
| +56 | 8 | valid_to_us | uint64 |
Read: seq -> data -> seq again. Mismatch = re-read.
5.2 IF-VAL-SS-001: Telemetry Mirror (50 Hz, 512 KB)
Region: /dev/shm/klft_vehicle_telemetry (max 64 vehicles x 256B)
Per-Vehicle (256B)
| Offset | Size | Field | Type |
| +0 | 16 | vehicle_id | UUID |
| +16 | 8 | timestamp_us | uint64 |
| +24 | 8 | lat | double |
| +32 | 8 | lng | double |
| +40 | 4 | alt_msl_ft | float |
| +44 | 4 | alt_agl_ft | float |
| +48 | 4 | heading_deg | float |
| +52 | 4 | speed_kts | float |
| +56 | 4 | vert_speed_fpm | float |
| +60 | 4 | battery_soc | float |
| +64 | 1 | gps_fix | bool |
| +65 | 1 | rid_active | bool |
| +66 | 1 | imu_status | uint8 |
| +67 | 1 | in_flight | bool |
| +68 | 16 | mission_id | UUID |
| +84 | 4 | geofence_dist | float |
| +88 | 168 | reserved | bytes |
5.3 IF-TDE-SS-001: Emergency Conflict (event-driven)
Region: /dev/shm/klft_emergency_conflicts
Record (128B)
| Offset | Size | Field | Type |
| +0 | 8 | sequence | uint64 |
| +8 | 8 | timestamp_us | uint64 |
| +16 | 16 | vehicle_a | UUID |
| +32 | 16 | vehicle_b | UUID |
| +48 | 4 | conflict_type | uint32 |
| +52 | 4 | time_to_los_s | float |
| +56 | 4 | action_a | uint32 |
| +60 | 4 | action_b | uint32 |
| +64 | 4 | min_sep_ft | float |
| +68 | 60 | reserved | bytes |
6. EXTERNAL INTERFACE SPECIFICATIONS
6.1 IF-CE-LAANC-001: LAANC USS Provider
Protocol: REST/HTTPS, OAuth 2.0 client credentials
Timeout: 5000 ms; async poll 30s interval, 5 min max for PENDING
Failover: Primary -> secondary USS -> manual coordination flag
Caching: Approved auths cached with TTL = valid_to. Valid offline.
6.2 IF-EXT-RID-001: Remote ID Receiver
Protocol: Bluetooth 5 LR + Wi-Fi NaN per ASTM F3411-22a
Coverage: ~1 km BT / ~2 km Wi-Fi per receiver. Rate: 1 Hz per UAS.
Normalized Remote ID Message
| Field | Type | Description |
| uas_id | string | Serial or session ID |
| id_type | string | SERIAL_NUMBER, SESSION_ID |
| timestamp | string | Broadcast time |
| lat | double | Latitude |
| lng | double | Longitude |
| alt_geodetic_ft | float | Geodetic alt |
| alt_baro_ft | float | Baro alt |
| speed_kts | float | Speed |
| heading_deg | float | Track |
| vert_speed_fpm | float | Vertical rate |
| operator_lat | double | Operator lat |
| operator_lng | double | Operator lng |
| emergency_status | string | NONE, EMERGENCY, LOST_LINK |
| receiver_id | string | Ground station |
| rssi_dbm | int | Signal |
| is_own_vehicle | bool | Fleet match |
6.3 IF-EXT-ADSB-001: ADS-B Receiver
Protocol: 1090ES via SBS-1 BaseStation or Beast binary/TCP
Hardware: Dual receivers (dump1090-fa + FlightAware Pro Stick Plus)
Normalized ADS-B Message
| Field | Type | Description |
| icao_hex | string | 6-char ICAO address |
| callsign | string | Callsign |
| timestamp | string | Time |
| lat | double | Latitude |
| lng | double | Longitude |
| alt_baro_ft | float | Baro altitude |
| speed_kts | float | Ground speed |
| track_deg | float | Track |
| vert_rate_fpm | float | Vertical rate |
| squawk | string | Transponder |
| on_ground | bool | Ground flag |
| receiver_id | string | Station |
6.4 IF-EXT-WX-001: Weather Station
Protocol: Davis WeatherLink serial/TCP -> Kafka. Rate: 1-min obs.
Weather Observation
| Field | Type | Description |
| station_id | string | Station ID |
| timestamp | string | Obs time |
| wind_speed_kts | float | Sustained wind |
| wind_gust_kts | float | Peak gust 10min |
| wind_dir_deg | float | From direction |
| temp_f | float | Temperature |
| humidity_pct | float | RH |
| pressure_inhg | float | Altimeter |
| visibility_sm | float | Visibility |
| precip_rate_in_hr | float | Rain rate |
| precip_type | string | NONE/RAIN/SNOW/MIXED/FREEZING |
| cloud_base_ft | float | Ceilometer |
7. SAFETY SUPERVISOR DEDICATED INTERFACES
SS on independent hardware. No Kafka/PostgreSQL dependency. Max reliability, min latency.
7.1 IF-SS-VAL-001: Safety Commands (868 MHz RF)
Encoding: 32-byte binary, CRC-16, AES-128. Latency: < 50 ms.
Safety Command Frame (32 bytes)
| Offset | Size | Field | Type | Description |
| +0 | 2 | sync | uint16 | 0xAA55 |
| +2 | 16 | vehicle_id | UUID | Target |
| +18 | 1 | command | uint8 | 0x01=HOLD, 0x02=RTL, 0x03=LAND, 0x04=TERMINATE, 0xFF=HEARTBEAT |
| +19 | 4 | alt_ft | float | For HOLD |
| +23 | 4 | hdg_deg | float | For HOLD |
| +27 | 1 | priority | uint8 | 0=NORMAL, 1=EMERGENCY |
| +28 | 2 | sequence | uint16 | Replay protection |
| +30 | 2 | crc16 | uint16 | CRC-16/CCITT |
Heartbeat: 50 Hz per vehicle. No HB for 5s -> vehicle onboard failsafe.
ACK: 16-byte ACK. 3 missed -> escalate EMERGENCY + alert.
7.2 SS Safety Envelope (10 Hz evaluation)
| Parameter | Threshold | Action |
| Altitude AGL | > 420 ft | DESCEND |
| Geofence proximity | < 50 ft | HOLD then RTL |
| Geofence breach | Beyond boundary | Immediate RTL |
| Battery SoC | < 20% | RTL |
| Battery SoC | < 10% | LAND immediately |
| GPS satellites | < 6 | HOLD |
| GPS HDOP | > 5.0 | HOLD |
| IMU status | FAIL | LAND immediately |
| C2 loss (primary) | 10s no heartbeat | Switch backup |
| C2 loss (all) | 30s | Vehicle failsafe |
| SS heartbeat loss | 5s (vehicle-side) | Vehicle RTL |
| Manned proximity | <0.25NM / <250ft vert | DESCEND+offset |
8. ENUMERATIONS AND COMMON TYPES
8.1 Mission Types
| Value | Description | Priority |
| DFR | Drone as First Responder | 1 |
| MEDICAL_DELIVERY | Medical supply | 2 |
| INSPECTION | Infrastructure | 4 |
| COMMERCIAL_DELIVERY | Package | 5 |
| TEST | Test/training | 6 |
8.2 Mission State Machine
| State | Description | Transitions |
| DRAFT | Created | VALIDATED, CANCELLED |
| VALIDATED | Checks passed | APPROVED, DRAFT, CANCELLED |
| APPROVED | Operator approved | PREFLIGHT, CANCELLED |
| PREFLIGHT | Pre-flight checks | ACTIVE, ABORTED |
| ACTIVE | Airborne | RTL, ON_STATION, ABORTED |
| ON_STATION | At target | RTL, ACTIVE, ABORTED |
| RTL | Returning | LANDING, ABORTED |
| LANDING | Approach | COMPLETE, ABORTED |
| COMPLETE | Done (terminal) | (none) |
| ABORTED | Terminated (terminal) | (none) |
| CANCELLED | Pre-launch (terminal) | (none) |
8.3 Vehicle States
| State | Description |
| READY | Dock, all gates pass |
| GROUNDED | Dock, gate fail |
| PREFLIGHT | Checking |
| IN_FLIGHT | Airborne |
| RETURNING | RTL |
| LANDING | Approach |
| DOCKED | Post-flight |
| CHARGING | Charging |
| MAINTENANCE | Offline maint |
| OFFLINE | No comms |
8.4 Alert Severities
| Severity | Criteria | Response |
| INFO | Informational | None |
| CAUTION | Abnormal, monitor | Ack 5 min |
| WARNING | Significant | Ack 60 sec |
| EMERGENCY | Critical safety | Immediate |
8.5 Common Types
LatLng / LatLngAlt / TimeWindow / GeoPolygon
| Type | Fields | Notes |
| LatLng | lat: double, lng: double | WGS84, -90/90, -180/180 |
| LatLngAlt | lat, lng, alt_msl_ft, alt_agl_ft | Feet |
| TimeWindow | start: Timestamp, end: Timestamp | UTC |
| GeoPolygon | vertices: LatLng[], type: INCLUSION|EXCLUSION | Min 3 vertices, closed |
9. ERROR HANDLING AND FAULT TOLERANCE
9.1 Error Code Registry
| Code | Description | Retry |
| MD.VALIDATION.ROUTE_INFEASIBLE | Cannot fly route | No |
| MD.VALIDATION.VEHICLE_NOT_READY | Readiness fail | Fix then yes |
| MD.VALIDATION.COMPLIANCE_FAIL | Rules failed | No (re-plan) |
| MD.STATE.INVALID_TRANSITION | Bad state change | No |
| FHM.READINESS.NO_VEHICLE | None available | Yes (30s) |
| FHM.READINESS.IN_FLIGHT | Vehicle airborne | Yes (poll) |
| CE.EVAL.ENGINE_ERROR | OPA error | Yes (1s) |
| CE.LAANC.TIMEOUT | USS timeout | Yes (1x) |
| CE.LAANC.DENIED | Auth denied | No (re-plan) |
| ASM.VOLUME.CONFLICT | Volume conflict | No (re-plan) |
| ASM.VOLUME.GEOFENCE | Hits geofence | No (re-route) |
| VAL.COMMAND.NACK | Vehicle reject | Yes (1s,1x) |
| VAL.COMMAND.LINK_LOST | C2 down | Yes (5s) |
| SS.OVERRIDE.SAFETY_ACTIVE | Safety in progress | No |
9.2 Circuit Breakers
| Interface | Trip | Open | Fallback |
| CE->LAANC | 3 fail/60s | 60s | Cached auth; manual flag |
| MD->FHM | 5 fail/30s | 30s | Last-known + STALE |
| MD->CE | 3 fail/30s | 30s | Block new approvals |
| MD->ASM | 3 fail/30s | 30s | Block new launches |
| OI->MD | 10 fail/60s | 30s | Unavailable banner |
9.3 Idempotency
All mutations: X-Idempotency-Key (REST) or idempotency_key metadata (gRPC). Server caches 24hr. Duplicate = stored response. UUID v4 keys.
10. INTERFACE VERSIONING
- Semantic versioning MAJOR.MINOR.PATCH. All interfaces currently 1.0.0.
- MAJOR: breaking. MINOR: backward-compatible addition. PATCH: docs/cosmetic.
- Protobuf: optional fields = MINOR. Remove = MAJOR + migration.
- Kafka: schema_version field. Unknown fields handled gracefully.
- Shared memory: fixed layout per MAJOR. Reserved bytes for expansion.
- REST: /api/v1/... URL versioned. MAJOR parallel 30+ days.
10.1 Change Request Process
1. Submit ICR: interface ID, change, rationale, impact
1. Tech Lead reviews compatibility
1. Affected owners approve
1. ICR merged, version incremented
1. PR references ICR, integration test validates
11. TIMING AND PERFORMANCE REQUIREMENTS
| Interface | Max Latency | Throughput | Availability |
| SS -> Vehicle (safety RF) | 50 ms | 50 Hz/vehicle | 99.999% |
| SS shared memory reads | 1 ms | 50 Hz/vehicle | 99.999% |
| TDE -> SS emergency | 1 ms (shmem) | Event-driven | 99.999% |
| ASM -> TDE state | 1 ms (shmem) | 10 Hz | 99.99% |
| MD -> FHM readiness | 500 ms | 10 req/s | 99.9% |
| MD -> CE compliance | 2000 ms | 5 req/s | 99.9% |
| MD -> ASM volume | 500 ms | 10 req/s | 99.9% |
| MD -> VAL execute | 200 ms (ack) | Per-vehicle | 99.9% |
| OI WebSocket | 200 ms display | 100 evt/s | 99.5% |
| Kafka telemetry | 50 ms e2e | 10,000 msg/s | 99.9% |
| CE -> LAANC | 5000 ms | 1 req/s | Best-effort |
| REST API | 200 ms p99 | 50 req/s | 99.9% |
12. INTERFACE SECURITY REQUIREMENTS
| Interface Type | Authentication | Encryption | Authorization |
| REST API | JWT (RS256, 1hr) | TLS 1.3 | RBAC (admin/operator/viewer) |
| gRPC (internal) | mTLS | TLS 1.3 | Service identity via cert CN |
| WebSocket | JWT in upgrade | TLS 1.3 (wss://) | Same as REST |
| Kafka | SASL/SCRAM-256 | TLS 1.3 | ACLs per topic |
| Shared memory | OS process isolation | N/A (local) | Unix file perms |
| Safety RF | Pre-shared key + seq | AES-128-CTR | SS sole transmitter |
| LAANC USS | OAuth 2.0 CC | TLS 1.3 | Scoped to LAANC ops |
- TLS certificates via internal CA; rotated every 90 days
- JWT signing keys rotated every 30 days; old keys valid 48 hr
- API rate limiting: 100 req/sec per client; 1000 req/sec global
- External endpoints behind API gateway with WAF
- Network segmentation: safety bus, ops LAN, external WAN on separate VLANs
END OF DOCUMENT
KLFT Autonomous Airspace Operations Hub — Software Interface Control Document v1.0