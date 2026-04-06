# KLFT — CONOPS and Safety Case
*Notion backup — 2026-04-06*

AUTONOMOUS AIRSPACE OPERATIONS HUB
CONCEPT OF OPERATIONS & SAFETY CASE
Operational Procedures, Safety Analysis, Hazard Mitigations & FAA Submission Framework
Lafayette Regional Airport (KLFT), Louisiana
Companion to: System Architecture v1.0, Phase 1 Spec v1.0, ICD v1.0
Document Version: 1.0 | February 2026
CLASSIFICATION: ENGINEERING DRAFT — SAFETY SENSITIVE
1. DOCUMENT PURPOSE AND AUTHORITY
1.1 Purpose
This document defines the Concept of Operations (CONOPS) and Safety Case for the KLFT Autonomous Airspace Operations Hub. It establishes the operational framework, safety argument, hazard analysis, risk mitigations, and operational procedures required to conduct UAS operations from Lafayette Regional Airport. This document serves as the primary safety reference for FAA waiver applications, Part 108 readiness, and internal operational governance.
1.2 Applicable Documents
| Document | Version | Relationship |
| KLFT System Architecture Design Document | 1.0 | Defines system design this CONOPS operates within |
| KLFT Phase 1 Implementation Specification | 1.0 | Build plan for initial operational capability |
| KLFT Software Interface Control Document | 1.0 | Interface contracts between subsystems |
| 14 CFR Part 107 | Current | Baseline regulatory framework |
| 14 CFR Part 89 (Remote ID) | Current | Remote ID compliance requirements |
| 14 CFR Part 108 (anticipated) | Draft | Future BVLOS regulatory framework |
| ASTM F3442 (Well-Clear) | Current | DAA well-clear definition |
| ASTM F3548 (UTM) | Current | UTM operational volume conventions |
| DO-178C | Current | Software assurance guidance for safety-critical |
| JARUS SORA 2.5 | Current | Specific Operations Risk Assessment methodology |
1.3 Approval Authority
| Role | Responsibility | Authority |
| Chief Pilot / UAS Operations Manager | Overall operational safety, flight authorization | Final go/no-go for all flights |
| Technical Lead / System Architect | System safety, software integrity, change control | System readiness certification |
| Safety Officer | Hazard tracking, incident investigation, safety culture | Safety hold authority (can stop any operation) |
| FAA Regional Flight Standards (FSDO) | Regulatory oversight, waiver review | Waiver approval/revocation |
2. CONCEPT OF OPERATIONS
2.1 Operational Overview
The KLFT Hub operates autonomous and remotely-piloted UAS from Lafayette Regional Airport and distributed dock sites across the Acadiana region. Operations span five mission categories: Drone-as-First-Responder (DFR), medical delivery, infrastructure inspection, commercial delivery, and training/test flights. All operations are managed through a centralized mission control facility staffed by qualified operators with AI-assisted decision support.
2.2 Operational Environment
| Parameter | Specification |
| Primary operating area | 15 NM radius from KLFT (30.2050°N, 91.9876°W) |
| Airspace classification | Class C (KLFT surface area), Class E, Class G |
| Altitude envelope | Surface to 400 ft AGL (standard); up to published LAANC ceiling in Class C |
| Operating hours | Phase 1: Daylight (civil twilight to civil twilight). Phase 3+: 24/7 with appropriate lighting/DAA |
| Weather minimums | Visibility >= 3 SM, cloud ceiling >= 500 ft AGL, sustained wind <= 25 kts, gusts <= 35 kts, no icing, no thunderstorms within 10 NM |
| Temperature range | 32°F to 110°F (vehicle-dependent) |
| Terrain | Flat to gently rolling; predominant land use: agricultural, suburban, industrial |
| Population density | Varies: rural (< 100/sq mi) to urban (> 1000/sq mi near Lafayette) |
| Obstacles | KLFT airport structures, communication towers, power transmission lines, elevated roadways |
2.3 Operational Phases
| Phase | Operations | Airspace | Staffing |
| Phase 1 (Months 1-6) | Single vehicle, VLOS/EVLOS, manual dispatch | KLFT vicinity, LAANC authorized | 1 RPIC + 1 operator |
| Phase 2 (Months 6-12) | Multi-vehicle, VLOS/EVLOS, traffic-aware | 15 NM radius, layered airspace | 1 RPIC + 2 operators |
| Phase 3 (Months 12-24) | Multi-vehicle, BVLOS (waiver), AI-assisted | Full ops area, corridor-based | 1 RPIC + 2 operators + supervisor |
| Phase 4 (Months 24-36) | High-density, multi-operator, autonomous | Regional, federated UTM | 2 RPIC + 3 operators + supervisor |
2.4 Mission Profiles
2.4.1 Drone-as-First-Responder (DFR)
Trigger: 911 CAD dispatch or law enforcement request
Response time target: Airborne within 90 seconds of trigger
Profile: Vertical launch from dock -> climb to L2/L3 transit altitude -> direct route to incident -> descend to loiter altitude (100-200 ft AGL) -> orbit/station-keep over scene -> stream video to command -> RTL on release
Duration: 15-45 minutes typical
Priority: 1 (highest) - preempts all other traffic
2.4.2 Medical Delivery
Trigger: Hospital/clinic request via API or operator
Profile: Launch from dock -> transit at L2/L3 -> descend at delivery site -> payload release/winch -> RTL
Payload: Blood products, lab samples, medications (< 5 lbs typical)
Priority: 2
2.4.3 Infrastructure Inspection
Trigger: Scheduled or operator-initiated
Profile: Launch -> transit to inspection area -> enter free-flight zone -> execute inspection pattern (orbit, linear, grid) -> capture imagery -> RTL
Assets inspected: Power lines, pipelines, bridges, levees, cell towers, solar farms
Priority: 4
2.4.4 Commercial Delivery
Trigger: E-commerce/logistics API integration
Profile: Launch -> corridor transit at L2 -> descend at delivery waypoint -> payload release -> RTL
Priority: 5
2.5 Operator Roles and Qualifications
| Role | Qualifications | Responsibilities | Max Concurrent Vehicles |
| Remote Pilot in Command (RPIC) | FAA Part 107 certificate; hub-specific type rating; current medical (if req'd under Part 108) | Legal authority for flight; go/no-go; override authority; ATC communication | 1 (Phase 1-2), 3 (Phase 3+) |
| Mission Operator | Hub operator certification (internal); Part 107 recommended | Mission monitoring; routine dispatch; alert acknowledgment; data review | 5 (with automation assist) |
| Operations Supervisor | Senior operator cert; 500+ hrs UAS ops; safety officer training | Shift management; escalation point; multi-mission oversight; incident command | Oversight of all active ops |
| Maintenance Technician | Manufacturer maintenance cert; hub maintenance training | Vehicle/dock maintenance; battery management; hardware troubleshooting | N/A |
2.6 Shift Structure
| Shift | Hours | Minimum Staffing (Phase 1) | Minimum Staffing (Phase 3+) |
| Day (primary ops) | 0700-1900 local | 1 RPIC + 1 operator | 1 RPIC + 2 operators + supervisor |
| Night (future 24/7) | 1900-0700 local | N/A (Phase 1 daylight only) | 1 RPIC + 1 operator |
| On-call | 24/7 | 1 RPIC (30-min response) | 1 RPIC + 1 technician (30-min) |
3. SAFETY CASE
3.1 Safety Argument Structure
The safety case follows a Goal Structuring Notation (GSN) approach with the following top-level argument:
Top Claim (C1): KLFT UAS operations are acceptably safe for the defined operational environment and mission profiles.
Strategy (S1): Argument over identified hazards, demonstrating that each is mitigated to an acceptable risk level per SORA methodology.
Context: Operations within the defined CONOPS (Section 2), using the system architecture (Architecture Doc), with trained personnel (Section 2.5).
Sub-Claims
1. C1.1: All credible hazards have been identified and assessed (Section 3.2)
1. C1.2: Each hazard has mitigations that reduce risk to acceptable levels (Section 3.3)
1. C1.3: The ground risk is acceptable for the operational area (Section 3.4)
1. C1.4: The air risk is acceptable given traffic awareness and deconfliction (Section 3.5)
1. C1.5: The system is designed to fail safely under all identified failure modes (Section 3.6)
1. C1.6: Personnel are trained and procedures are adequate (Section 4)
1. C1.7: Continuous safety monitoring detects and responds to emerging risks (Section 5)
3.2 Hazard Identification
Hazards identified through Functional Hazard Assessment (FHA), HAZOP, and operational experience review:
| ID | Hazard | Category | Severity | Exposure |
| H01 | UAS collision with manned aircraft | Air Risk | Catastrophic | Moderate (Class C env) |
| H02 | UAS collision with another UAS | Air Risk | Hazardous | Low (Phase 1), High (Phase 4) |
| H03 | UAS ground impact in populated area | Ground Risk | Catastrophic | Moderate |
| H04 | UAS ground impact on critical infrastructure | Ground Risk | Hazardous | Low |
| H05 | Loss of command and control link | System | Major | Moderate |
| H06 | Navigation/GPS failure during flight | System | Hazardous | Low |
| H07 | Battery failure / fire in flight | Vehicle | Catastrophic | Low |
| H08 | Battery fire at dock/facility | Vehicle | Hazardous | Low |
| H09 | Payload release failure (medical) | Mission | Major | Low |
| H10 | Geofence breach into restricted area | Airspace | Hazardous | Low |
| H11 | Unauthorized airspace entry (KLFT Class C without auth) | Airspace | Hazardous | Low |
| H12 | Weather deterioration during flight | Environment | Major | Moderate |
| H13 | RF interference / jamming | System | Hazardous | Low |
| H14 | Cybersecurity breach of C2 link | Security | Catastrophic | Low |
| H15 | Operator error / wrong command | Human | Hazardous | Moderate |
| H16 | Software defect causing incorrect behavior | System | Hazardous | Low |
| H17 | Dock mechanical failure during launch/recovery | System | Major | Low |
| H18 | Multiple simultaneous failures (common cause) | System | Catastrophic | Very Low |
3.3 Risk Assessment and Mitigation Matrix
Risk assessed per JARUS SORA methodology. Severity x Likelihood -> Initial Risk Class. Mitigations applied to achieve Residual Risk.
| ID | Initial Risk | Mitigations | Residual Risk | ALARP |
| H01 | Extreme | ADS-B traffic awareness; altitude separation from manned traffic; LAANC/ATC coordination; right-of-way rules; DAA system (Phase 3); well-clear definition per F3442 | Medium | Yes |
| H02 | High | Traffic deconfliction engine; 4D separation assurance; corridor-based routing; priority rules; emergency avoidance maneuvers | Low | Yes |
| H03 | High | Flight over populated areas only on approved corridors; operational volume with ground risk buffer; contingency procedures; flight termination system (Phase 3); parachute system on larger vehicles | Medium | Yes |
| H04 | Medium | Geofenced exclusion zones around critical infrastructure; route planning avoids critical sites; pre-programmed contingency avoids critical areas | Low | Yes |
| H05 | High | Triple-redundant C2 (900 MHz + 2.4 GHz + 868 MHz safety); automatic link failover; pre-programmed lost-link procedure (RTL); SS independent heartbeat | Low | Yes |
| H06 | High | Dual GPS/GNSS receivers on vehicle; IMU dead-reckoning fallback; HOLD command on GPS degradation; RTL on GPS failure with last-known position | Low | Yes |
| H07 | High | Battery management system with cell monitoring; pre-flight SoC/temp/voltage gates; manufacturer-certified batteries; immediate LAND on battery anomaly | Low | Yes |
| H08 | Medium | Fire-rated battery cabinets; smoke/thermal detection; automatic suppression; ventilation; battery storage procedures per NFPA | Low | Yes |
| H09 | Medium | Redundant release mechanism; pre-mission payload verification; abort-to-safe-area if release fails | Low | Yes |
| H10 | High | Three-layer geofence system; SS enforces hard geofence with RTL; geofence validated pre-flight; real-time geofence monitoring | Low | Yes |
| H11 | High | LAANC auto-authorization; pre-flight compliance check blocks unapproved flights; ATC coordination procedures; CE rule enforcement | Low | Yes |
| H12 | Medium | Real-time weather monitoring; automated go/no-go; phased stand-down procedure; RTL on weather deterioration | Low | Yes |
| H13 | Medium | Frequency hopping; RF spectrum monitoring; automatic failover to alternate frequency; lost-link procedure on sustained interference | Low | Yes |
| H14 | Extreme | AES-128 encrypted C2; pre-shared keys; sequence counters (replay protection); network segmentation; penetration testing; RF link authentication | Medium | Yes |
| H15 | High | Confirmation dialogs for critical commands; two-step override process; action logging; RPIC training; CRM procedures; undo capability where safe | Low | Yes |
| H16 | High | DO-178C DAL-C for safety-critical software; formal testing; code review; AI isolated from safety path; deterministic safety decisions | Low | Yes |
| H17 | Medium | Dock state machine with fault detection; pre-launch mechanical check; manual recovery procedure; maintenance schedule | Low | Yes |
| H18 | Extreme | Defense-in-depth architecture; independent safety layers; no common compute/power/network for safety-critical; FMEA review; common-cause analysis | Low | Yes |
3.4 Ground Risk Assessment (SORA)
Ground Risk Class (GRC) determination per JARUS SORA 2.5:
| Parameter | Value | Rationale |
| Max UAS dimension | < 3 m | Matrice 350 class vehicles |
| Max kinetic energy | < 34 kJ (typical) | Based on MTOW and max speed |
| Operational scenario | BVLOS over sparsely populated (Phase 3) | Initial ops over controlled areas; expanding |
| Initial GRC | 7 | BVLOS, populated, < 25 kg, < 34 kJ |
| M1 - Strategic mitigation (ground risk buffer) | Medium robustness (-1) | Op volume + contingency volume with ground buffer |
| Final GRC | 6 | After M1 mitigation |
| SAIL | IV | Per SORA table; GRC 6 maps to SAIL IV |
3.5 Air Risk Assessment (SORA)
| Parameter | Value | Rationale |
| Airspace classification | Class C (near KLFT) / Class E / Class G | Mixed airspace environment |
| Initial ARC | ARC-c | Controlled airspace, airport environment |
| TMPR (Tactical Mitigation Performance Req.) | Medium robustness | ADS-B awareness + LAANC + ATC coordination |
| Residual ARC | ARC-b | After TMPR mitigation |
| Air risk mitigations | ADS-B receiver network, Remote ID, LAANC, ATC phone/radio coordination, altitude layering, corridor-based routing, TDE strategic/tactical deconfliction | Multiple layers of air risk mitigation |
3.6 Failure Mode Summary
Complete FMEA documented in separate Failure Mode and Effects Analysis workbook. Summary of critical failure modes:
| Failure Mode | Effect | Detection | Severity | Mitigation | RPN |
| Total C2 link loss | Uncontrolled flight | Heartbeat timeout (30s) | Catastrophic | Pre-programmed RTL; SS independent link; vehicle onboard failsafe | Medium |
| GPS loss in flight | Navigation failure | GPS monitor (< 6 sats) | Hazardous | IMU dead-reckoning; HOLD; RTL on last-known | Low |
| Battery cell failure | Forced landing | BMS cell voltage monitor | Hazardous | Immediate LAND; redundant cells; pre-flight screening | Low |
| Safety Supervisor failure | Loss of safety monitoring | Hardware watchdog | Catastrophic | Hot standby SS; vehicle onboard failsafe; operator alert | Low |
| TDE failure | Loss of deconfliction | Heartbeat + output stale | Hazardous | Pause new launches; active flights have separation buffer; operator manual monitoring | Low |
| Airspace Manager failure | Invalid airspace model | State validation + standby | Hazardous | Hot standby takeover; TDE cached state; conservative defaults | Low |
| Dock mechanical jam | Vehicle trapped/dropped | Dock state timeout | Major | Manual recovery procedure; vehicle hover-safe mode; maintenance | Low |
| Operator incapacitation | No human oversight | Activity timeout (5 min) | Hazardous | Second operator alert; auto-RTL all aircraft if no response | Low |
4. OPERATIONAL PROCEDURES
4.1 Pre-Mission Procedures
4.1.1 Daily Operations Startup
1. Operations Supervisor reviews NOTAMs, TFRs, and weather forecast for operating area
1. Verify all server infrastructure healthy (Grafana dashboard green)
1. Verify C2 link test to all active docks (automated test sequence)
1. Verify ADS-B receiver operational and receiving traffic
1. Verify Remote ID receivers operational
1. Verify weather station data current and within operating limits
1. Confirm LAANC system reachable and UASFM data current
1. Confirm operator staffing meets minimum requirements for planned operations
1. Log daily startup checklist completion in operations log
4.1.2 Pre-Flight Checklist (Per Mission)
1. Mission plan reviewed: route, altitude, waypoints, payload, estimated duration
1. Compliance Engine evaluation: PASS (all rules green)
1. LAANC authorization: APPROVED (if controlled airspace)
1. Vehicle readiness: All gates PASS (battery >= 80% for full mission, GPS lock, IMU OK, Remote ID broadcasting)
1. Dock status: READY, no faults, weather at dock within limits
1. Airspace clear: No conflicting volumes, no active geofence conflicts
1. Weather current: Within operating minimums at launch site, en route, and recovery site
1. RPIC confirms go/no-go and approves mission
1. System logs pre-flight approval with RPIC identity and timestamp
4.2 In-Flight Procedures
4.2.1 Normal Operations
- Operator monitors telemetry display: position, altitude, speed, battery, heading
- System auto-advances waypoints; operator confirms progression on display
- Operator acknowledges INFO and CAUTION alerts within 5 minutes
- Operator acknowledges WARNING alerts within 60 seconds and assesses situation
- RPIC maintains awareness of manned traffic via ADS-B display overlay
- RPIC maintains communication readiness with KLFT tower (phone/radio)
4.2.2 Abnormal Situations
| Situation | Detection | Immediate Action | Follow-Up |
| CAUTION alert | Yellow alert on UI + audio chime | Operator acknowledges; monitors condition | Assess if mission can continue; log decision |
| WARNING alert | Orange alert + audio tone | Acknowledge within 60s; assess severity | Prepare contingency action; brief RPIC |
| Battery below 30% | Telemetry + auto-alert | System recommends RTL; operator confirms | Initiate RTL; monitor descent |
| Weather approaching limits | Weather station + forecast | RPIC assesses continue/RTL decision | If marginal: RTL. If deteriorating rapidly: RTL all active flights |
| C2 link degraded (>20% loss) | Telemetry gap detection | Monitor; system auto-switches backup link | If persistent: consider RTL |
| ADS-B target within 1 NM | TDE alert + map highlight | RPIC assesses conflict geometry | TDE may issue deconfliction; RPIC coordinates with ATC if needed |
| Unexpected vehicle behavior | Anomaly detection + operator | RPIC assesses; prepare override | If unresolved: manual RTL |
4.2.3 Emergency Procedures
| Emergency | Trigger | Automated Response | Operator Action |
| EMERGENCY: Loss of C2 (all links) | 30s no heartbeat on all links | Vehicle executes onboard lost-link procedure (RTL to home waypoint) | Monitor for link recovery; notify ATC; prepare ground recovery team |
| EMERGENCY: Manned aircraft incursion | ADS-B target < 0.5 NM, converging | TDE commands all UAS: descend + lateral offset. SS enforces. | RPIC contacts ATC immediately; do not countermand automated avoidance |
| EMERGENCY: Geofence breach | Vehicle crosses hard geofence | SS commands immediate RTL | Notify ATC if airspace violation; file report; investigate cause |
| EMERGENCY: Battery critical (<10%) | BMS telemetry | SS commands LAND immediately at nearest safe point | Dispatch ground recovery; secure vehicle; file report |
| EMERGENCY: Flyaway / uncontrolled | Vehicle not responding to commands, trajectory diverging | SS attempts FLIGHT_TERMINATE if equipped. Lost-link timeout engages onboard failsafe. | Notify ATC with last known position and trajectory; activate emergency contacts; file FAA report |
| EMERGENCY: Fire at dock/facility | Smoke/thermal sensor | Dock shuts down; nearby vehicles hold/RTL | Activate fire response; evacuate if needed; notify fire department |
| EMERGENCY: Operator incapacitation | No UI activity for 5 min during active ops | System alerts backup operator; after 10 min: auto-RTL all aircraft | Backup operator assumes; notify supervisor; log incident |
4.3 Post-Flight Procedures
1. Verify vehicle safely recovered to dock
1. Confirm dock status returns to IDLE or CHARGING
1. Review flight log: any alerts, deviations, anomalies
1. Review compliance log: Remote ID coverage 100%, altitude compliance, geofence compliance
1. If any anomaly: file Operational Occurrence Report (Section 5.3)
1. Update vehicle flight hours and cycle count in FHM
1. If maintenance threshold reached: ground vehicle, schedule maintenance
1. Export flight log to archive (7-year retention)
4.4 ATC Coordination Procedures
4.4.1 Standard Coordination
- Before first flight of day in Class C: phone call to KLFT tower advising UAS operations active, area, and max altitude
- LAANC authorization obtained via system before any Class C operation
- If LAANC unavailable: phone coordination with tower for verbal authorization; log in compliance system
- Notify tower of any off-nominal situation that may affect manned traffic
- End of day: phone call to tower advising UAS operations complete
4.4.2 Emergency ATC Coordination
- RPIC contacts KLFT tower immediately on any: flyaway, loss of control, geofence breach into controlled airspace, or near-miss with manned aircraft
- Provide: operator ID, UAS type, last known position, altitude, heading, nature of emergency
- Follow all ATC instructions immediately; system enforces ATC hold/release commands
- File NASA ASRS report within 10 days of any ATC-relevant incident
4.5 Maintenance Procedures
| Activity | Frequency | Performed By | Documentation |
| Pre-flight automated check | Every flight | System (FHM) | Auto-logged in vehicle record |
| Visual inspection | Every 10 flights or weekly | Maintenance Tech | Inspection checklist in maintenance log |
| Propeller inspection/replacement | Every 50 hrs or per manufacturer | Maintenance Tech | Part number, hours, tech signature |
| Battery health check | Every 50 cycles or per manufacturer | Maintenance Tech | Cell balance, internal resistance, capacity test |
| Battery retirement | Per manufacturer cycle limit or health threshold | Maintenance Tech | Retired battery logged, disposed per regulations |
| Firmware update | Per manufacturer release + internal validation | Maintenance Tech + Tech Lead | Version, test results, rollback plan |
| Dock mechanical inspection | Monthly | Maintenance Tech | Mechanical function test, lubrication, calibration |
| Sensor calibration (weather, RID) | Quarterly | Maintenance Tech | Calibration data, reference comparison |
| Server/network maintenance | Monthly (scheduled window) | DevOps | Patch log, restart verification, backup test |
| Full system backup test | Quarterly | DevOps | Backup restore verified, RTO measured |
5. SAFETY MANAGEMENT
5.1 Safety Management System (SMS) Framework
The KLFT Hub operates under a Safety Management System aligned with FAA Order 8000.369C and ICAO Doc 9859 principles. The SMS has four pillars:
- Safety Policy and Objectives: Documented safety policy signed by accountable executive; safety objectives with measurable targets
- Safety Risk Management: Hazard identification, risk assessment (SORA-based), mitigation tracking, periodic review
- Safety Assurance: Continuous monitoring, operational data analysis, audit program, change management
- Safety Promotion: Training program, safety reporting culture, lessons learned dissemination
5.2 Safety Performance Indicators
| Indicator | Target | Measurement | Review Frequency |
| Loss of separation events (UAS-manned) | 0 per year | TDE logs + ADS-B analysis | Monthly |
| Loss of separation events (UAS-UAS) | 0 per year | TDE conflict logs | Monthly |
| Geofence breach events | 0 per year | ASM + SS logs | Monthly |
| Unplanned landing rate | < 1 per 1000 flights | Mission completion analysis | Monthly |
| C2 link loss events (> 30 sec) | < 2 per 1000 flights | Telemetry gap analysis | Monthly |
| Safety Supervisor activation rate | < 5 per 1000 flights | SS action log | Monthly |
| Operational Occurrence Reports filed | Track (no target - encourage reporting) | OOR database | Monthly |
| Mean time to operator alert response | < 30 sec for WARNING, < 5 sec for EMERGENCY | OI action log | Weekly |
| Pre-flight gate rejection rate | Track (healthy fleet metric) | FHM logs | Weekly |
| Flight hours between incidents | Track (increasing trend desired) | Incident database / flight hours | Quarterly |
5.3 Occurrence Reporting
5.3.1 Reporting Categories
| Category | Criteria | Report Within | Report To |
| Accident | Property damage > $500, serious injury, fatality | Immediately | FAA (NTSB if serious), internal Safety Officer |
| Serious Incident | Near mid-air collision, flyaway, fire, emergency landing in populated area | Within 4 hours | FAA FSDO, internal Safety Officer |
| Incident | Geofence breach, C2 loss > 60 sec, unplanned landing in safe area, equipment failure affecting flight | Within 24 hours | Internal Safety Officer; FAA if applicable |
| Occurrence | Alert activation, minor anomaly, near-miss (no conflict), maintenance finding | Within 48 hours | Internal safety database |
| Hazard Report | Identified potential hazard not yet realized | Within 1 week | Internal Safety Officer for hazard register update |
5.3.2 Operational Occurrence Report (OOR) Contents
- Date, time, location of occurrence
- Mission ID, vehicle ID, operator ID
- Weather conditions at time of occurrence
- Narrative description of events
- System logs (auto-attached from audit trail)
- Immediate actions taken
- Root cause analysis (for Incident and above)
- Corrective actions recommended
- Follow-up status tracking
5.4 Safety Review Process
| Review | Frequency | Participants | Outputs |
| Daily safety briefing | Start of each ops day | Shift operators + RPIC | Brief on NOTAMs, weather, known risks, today's ops plan |
| Weekly safety review | Weekly | Ops Supervisor + Safety Officer + Tech Lead | Review week's OORs, SPI trends, open corrective actions |
| Monthly safety board | Monthly | All leadership + Safety Officer | SPI dashboard review, hazard register update, policy changes |
| Quarterly safety audit | Quarterly | Safety Officer + external (if available) | Compliance audit, procedure review, training assessment |
| Annual safety assessment | Annually | Full team + FAA (if participating) | Comprehensive risk re-assessment, CONOPS update, SORA refresh |
5.5 Change Management
Any change to the following requires formal safety assessment before implementation:
- New vehicle type or dock type integration
- Software update to safety-critical subsystems (SS, ASM, TDE)
- AI model update or promotion to production
- Operational area expansion
- New mission type or profile
- Airspace structure modification
- Staffing model change
- Regulatory rule set update
Change assessment includes: hazard impact review, updated risk assessment, test plan, rollback plan, Safety Officer sign-off. Changes to safety-critical software require Tech Lead + Safety Officer dual approval.
6. EMERGENCY RESPONSE PLAN
6.1 Emergency Classification
| Level | Definition | Example | Response Lead |
| Level 1: Minor | Operational disruption, no safety impact | Single dock offline, minor SW bug | Mission Operator |
| Level 2: Significant | Potential safety impact, contained | C2 degradation, weather stand-down, single vehicle RTL | RPIC |
| Level 3: Serious | Active safety concern, possible external impact | Geofence breach, C2 total loss, emergency landing | RPIC + Operations Supervisor |
| Level 4: Critical | Confirmed external impact or imminent danger | Flyaway, fire, injury, collision, airspace violation | Operations Supervisor + Safety Officer |
6.2 Emergency Contact List
| Contact | Phone | When to Call |
| KLFT ATC Tower | (337) XXX-XXXX | Any airspace issue, manned traffic conflict, emergency in Class C |
| Lafayette Fire Department | 911 | Fire at dock or facility, crash with fire |
| Lafayette Police Department | 911 | Crash in populated area, security incident |
| FAA Houston FSDO | (XXX) XXX-XXXX | Accident/serious incident reporting |
| NTSB | (844) 373-9922 | Accident involving serious injury or significant property damage |
| Operations Supervisor (on-call) | Internal | Any Level 2+ event outside normal hours |
| Safety Officer | Internal | Any Level 3+ event; any occurrence report |
| Technical Lead | Internal | System failure, SW defect causing safety issue |
6.3 Crash/Impact Response Procedure
1. Operator confirms vehicle location via last telemetry or visual
1. If in populated area: call 911, provide location and UAS description
1. If near KLFT: notify tower immediately
1. Secure the area if accessible: 50 ft perimeter, do not touch battery if damaged
1. If battery is smoking/swelling: evacuate 100 ft, notify fire department
1. Photograph scene before disturbing evidence
1. Do not move vehicle until Safety Officer authorizes (unless immediate danger)
1. File Occurrence Report within 4 hours
1. Preserve all system logs (auto-preserved by DP, but confirm)
1. Conduct root cause investigation within 72 hours
6.4 Flyaway Response Procedure
1. Confirm flyaway: vehicle not responding to commands AND trajectory diverging from plan
1. SS attempts FLIGHT_TERMINATE if vehicle equipped with FTS
1. If no FTS: lost-link timeout will engage onboard failsafe (RTL or land)
1. Notify ATC with: last known position, heading, speed, altitude, estimated battery endurance
1. Track vehicle via ADS-B (if transponder equipped) or Remote ID ground receivers
1. Notify law enforcement with predicted impact area if vehicle leaves ops area
1. Activate ground recovery team to predicted landing area
1. File Serious Incident report; preserve all logs
1. Ground all same-type vehicles pending investigation
7. TRAINING PROGRAM
7.1 Initial Training Requirements
| Role | Training Module | Duration | Assessment |
| All operators | Hub systems overview: architecture, subsystems, data flows | 8 hours | Written exam (80% pass) |
| All operators | Operator Interface proficiency: UI, alerts, map, controls | 16 hours | Practical exam: complete simulated missions |
| All operators | Normal procedures: pre-flight, in-flight, post-flight | 8 hours | Checklist walk-through + observed execution |
| All operators | Abnormal and emergency procedures | 16 hours | Scenario-based simulation (all Level 2-4 emergencies) |
| All operators | Safety management: reporting, SMS, safety culture | 4 hours | Written exam |
| RPIC | ATC coordination procedures | 4 hours | Role-play ATC communication scenarios |
| RPIC | Override authority and decision-making | 8 hours | Decision scenarios + CRM exercise |
| RPIC | Multi-vehicle operations (Phase 2+) | 16 hours | Simulated multi-vehicle with injected failures |
| Maintenance Tech | Vehicle maintenance per manufacturer | Per mfg program | Manufacturer certification |
| Maintenance Tech | Dock maintenance and troubleshooting | 8 hours | Practical: dock fault diagnosis and repair |
| Maintenance Tech | Battery handling and safety | 4 hours | Practical: battery inspection, storage, disposal |
7.2 Recurrent Training
| Training | Frequency | Duration | Assessment |
| Emergency procedures refresher | Every 6 months | 4 hours | Scenario-based simulation |
| System updates briefing | After every major SW release | 1-2 hours | Briefing + walkthrough of changes |
| ATC coordination refresher | Every 12 months | 2 hours | Role-play scenarios |
| Safety management refresher | Every 12 months | 2 hours | Review of incidents, SPI trends, policy updates |
| Proficiency check | Every 12 months | 4 hours | Observed: complete mission cycle + injected emergency |
| CRM/decision-making | Every 12 months | 4 hours | Scenario debrief + group discussion |
7.3 Training Records
- All training records maintained in digital training management system
- Records include: operator ID, training module, date, instructor, assessment result, expiration
- Expired training auto-flags operator as NOT QUALIFIED in system; blocked from active operations
- Training records retained for duration of employment + 3 years
- Available for FAA inspection upon request
8. FAA COMPLIANCE AND SUBMISSION STRATEGY
8.1 Phase 1: Part 107 Operations
| Requirement | Compliance Method | Evidence |
| RPIC holds Part 107 certificate | Verify certificate before granting system access | Certificate copy in operator file |
| Visual line of sight maintained | VLOS/EVLOS operations only; visual observer if needed | Mission type restriction in CE rule set |
| Maximum altitude 400 ft AGL | CE rule: PART107.MAX_ALT; SS hard ceiling at 420 ft | Rule evaluation log + SS enforcement log |
| Yield right of way to manned aircraft | ADS-B awareness + operator training + right-of-way rules | ADS-B integration + operator training records |
| No flight over non-participating persons | Route planning avoids crowds; operational area restrictions | Route validation log + geofence config |
| Daylight operations (or civil twilight with anti-collision lights) | CE rule: PART107.DAYLIGHT; time-of-day restriction | Rule evaluation log |
| Weather minimums (3 SM vis, 500 ft below clouds) | CE rule: PART107.WEATHER; weather station data | Weather log + rule evaluation |
| Remote ID compliance | Pre-flight gate: RID broadcasting; ground verification | RID compliance log per flight |
| Registration current | Vehicle registration verified at enrollment | Registration copy in vehicle file |
8.2 Phase 2-3: Part 107 Waiver Strategy
| Waiver | Justification | Supporting Evidence |
| 107.31 - VLOS (BVLOS operations) | DAA system (ADS-B + radar/visual); well-clear compliance; corridor-based routing; TDE; trained operators; operational data from Phase 1-2 | Flight hours, separation data, DAA test results, training records |
| 107.29 - Operations at Night | Anti-collision lighting on all vehicles; operator training for night ops; enhanced situational awareness displays | Lighting specs, night training completion, risk assessment |
| 107.35 - Operations Over People | Parachute/FTS on applicable vehicles; ground risk analysis; population density mapping; operational volume buffers | FTS test data, SORA ground risk assessment, trajectory simulations |
| 107.39 - Operations Over Moving Vehicles | Altitude above roadway traffic; route planning avoids major roads at low altitude; contingency procedures | Route analysis, altitude compliance data |
8.3 Phase 3-4: Part 108 Readiness
The system is designed for compliance with anticipated Part 108 BVLOS rules. Key readiness elements:
- Detect-and-avoid system meeting well-clear definition (ASTM F3442) with cooperative and non-cooperative detection
- Operational volume management per ASTM F3548 with contingency and flight geography
- Command and control link performance meeting Part 108 expected reliability requirements
- Flight termination system integration for operations over populated areas
- Remote pilot station meeting expected human factors requirements
- Maintenance program meeting expected continued airworthiness requirements
- Training program meeting expected pilot qualification requirements
- Data recording meeting expected operational data requirements (7-year retention)
- Safety management system meeting expected SMS requirements
Part 108 compliance will be validated against final rule text when published. The modular Compliance Engine allows rapid rule set updates.
8.4 FAA Engagement Timeline
| Milestone | Target Date | Action |
| Initial FAA coordination | Phase 1, Month 1 | Meet with Houston FSDO; present CONOPS; discuss waiver path |
| Part 107 operations commence | Phase 1, Month 4 | Standard Part 107 ops; begin accumulating operational data |
| BVLOS waiver pre-application meeting | Phase 2, Month 8 | Present operational data, DAA design, safety case to FSDO |
| BVLOS waiver submission | Phase 2, Month 10 | Submit formal waiver application with full safety case |
| BVLOS waiver operations | Phase 3, Month 14 (target) | Commence BVLOS per waiver conditions |
| Part 108 NPRM comment | When published | Submit comments based on operational experience |
| Part 108 application | Phase 3-4, when rule final | Apply under Part 108 framework |
9. DOCUMENT CONTROL
9.1 Revision History
| Version | Date | Author | Changes |
| 1.0 | February 2026 | KLFT Engineering Team | Initial release |
9.2 Review Schedule
- This CONOPS/Safety Case is a living document reviewed and updated:
- After any Level 3 or Level 4 incident
- Before each operational phase transition (Phase 1->2, 2->3, 3->4)
- After any significant system change (per Section 5.5 change management)
- At minimum annually as part of the annual safety assessment
- When new FAA regulations are published that affect operations
9.3 Distribution
| Recipient | Copy Type | Purpose |
| All operators and RPIC | Controlled (digital, version-tracked) | Operational reference |
| FAA Houston FSDO | Uncontrolled (submitted with waiver applications) | Regulatory review |
| Safety Officer | Controlled (master copy) | Safety management |
| Technical Lead | Controlled | System alignment |
| Contractor/vendor (relevant sections only) | Uncontrolled excerpts | Integration reference |
END OF DOCUMENT
KLFT Autonomous Airspace Operations Hub — CONOPS and Safety Case v1.0
---
## Gulf Coast Operational Theater
KLFT 1.1 serves the Gulf Coast operational theater: Lafayette metro, Acadiana parish network, and coastal industrial corridor (Port of New Iberia, Morgan City, Cameron Parish LNG terminals). Natural disaster frequency (hurricanes, flooding, industrial incidents) drives the emergency-first mission.
- Primary AOR: Lafayette Parish + adjacent Acadiana parishes
- Secondary AOR: Gulf Coast industrial corridor — refineries, LNG plants, port infrastructure
- Disaster scenarios: hurricane landfall, flood surge mapping, post-storm SAR, levee monitoring
- Industrial scenarios: chemical plume tracking, pipeline leak detection, facility perimeter patrol
- City partnership path: Lafayette Consolidated Government → state GOHSEP → federal FEMA integration
---
## Multi-Site Expansion Model
KLFT 1.1 is the pilot site. Successful deployment creates the template for Gulf Coast network expansion. Each new site deploys one ADC 3K pod + Skydio Dock + SkyCommand edge agent, managed from MARLIE I NOC.
- Site 2 target: New Iberia (proximity to solar factory partner + petrochemical corridor)
- Site 3 target: Lake Charles / Cameron Parish (LNG terminal corridor)
- Site 4 target: Morgan City (offshore supply hub, flooding vulnerability)
- Scaling: each additional site = one ADC 3K pod + $X SkyCommand site license