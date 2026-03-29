# KLFT — Facility Hardware Procurement Spec
*Notion backup — 2026-03-28*

AUTONOMOUS AIRSPACE OPERATIONS HUB
FACILITY & HARDWARE PROCUREMENT
SPECIFICATION
Bills of Material, Rack Layouts, Network Diagrams & Vendor Frameworks
Lafayette Regional Airport (KLFT), Louisiana
Companion to: System Architecture v1.0, Phase 1 Spec v1.0, ICD v1.0, CONOPS v1.0
Document Version: 1.0 | February 2026
CLASSIFICATION: ENGINEERING DRAFT
1. DOCUMENT PURPOSE AND SCOPE
1.1 Purpose
This document provides the complete Facility and Hardware Procurement Specification for the KLFT Autonomous Airspace Operations Hub. It defines facility construction requirements, server and network hardware bills of materials, drone platform and dock procurement, sensor equipment, rack layouts, power and cooling infrastructure, and vendor evaluation frameworks. This specification enables procurement execution with minimal ambiguity.
1.2 Procurement Phases
| Phase | Timeline | Procurement Focus | Budget Range |
| Phase 1 | Months 1-6 | Facility build-out, core servers, single dock+vehicle, sensors, network | $800K - $1.2M |
| Phase 2 | Months 6-12 | Safety hardware, additional sensors, second vehicle type, expanded network | $600K - $1.0M |
| Phase 3 | Months 12-24 | AI compute, additional docks (3-5), DAA sensors, edge nodes | $1.5M - $2.5M |
| Phase 4 | Months 24-36 | Regional dock expansion (10+), redundant facility, multi-operator infra | $2.0M - $3.5M |
This document focuses primarily on Phase 1 procurement with forward-looking requirements for Phases 2-4 to ensure infrastructure decisions do not constrain future scaling.
2. FACILITY SPECIFICATION
2.1 Site Requirements
| Requirement | Specification | Rationale |
| Location | At or adjacent to KLFT airport property; within 1 mile of primary dock site | Minimize C2 link distance; ATC proximity; airport access |
| Building size | Minimum 3,000 sq ft usable; 3,500 sq ft preferred | Ops floor + server room + support spaces |
| Ceiling height | Minimum 10 ft clear in ops floor; 9 ft in server room | Display mounting, cable trays, airflow |
| Roof access | Flat roof section or antenna mount points for 6+ antennas | ADS-B, Remote ID, C2, weather, cellular, PtP wireless |
| Parking | Minimum 10 spaces; 1 loading dock or roll-up door | Staff, visitors, equipment staging |
| Zoning | Commercial/industrial; airport-compatible land use | No residential restrictions on 24/7 ops or RF emissions |
| Flood zone | Outside 100-year flood plain preferred; if in zone: elevated 3+ ft | Gulf Coast flood risk; equipment protection |
| Utility access | Commercial 3-phase power (200A minimum); dual ISP availability | Redundant power and network feeds |
2.2 Floor Plan Specification
2.2.1 Operations Floor (800 sq ft)
| Element | Specification | Quantity |
| Operator workstations | L-shaped desk (72"x72"), adjustable height, integrated cable management, anti-fatigue mat | 4 stations |
| Primary display per station | 32" 4K monitor (map/SA display) + 27" 4K monitor (data/alerts) | 4 sets (8 monitors) |
| Video wall | 3x2 array of 55" narrow-bezel displays, total ~165" diagonal | 1 (6 displays) |
| Flooring | Raised access floor (12" plenum) with static-dissipative tile | 800 sq ft |
| Lighting | Dimmable LED, 30-50 fc adjustable, no direct glare on screens | Zone controlled |
| Acoustic treatment | Ceiling absorption panels, NRC >= 0.80; ambient < 45 dBA | Full ceiling |
| HVAC | Dedicated zone, 72°F ±4°F, humidity 40-60% | Separate from server room |
| UPS outlets | Dedicated UPS circuit per workstation | 4 circuits |
2.2.2 Server Room (400 sq ft)
| Element | Specification | Quantity |
| Server racks | 42U, 24" deep, front/rear doors, top cable entry, PDU rails | 2 racks |
| Hot/cold aisle | Contained cold aisle with blanking panels; hot aisle exhaust to HVAC return | 1 aisle |
| Cooling | Precision HVAC: 5-ton minimum, 68°F ±2°F, N+1 redundancy | 2 units (1 primary, 1 standby) |
| Fire suppression | Clean agent (FM-200 or Novec 1230); VESDA early detection | Full room |
| Flooring | Raised floor (18" plenum) with perforated tiles in cold aisle | 400 sq ft |
| Access control | Biometric + badge reader; logged entry/exit; camera | 1 door |
| Environmental monitoring | Temperature/humidity sensors (4 points), water leak detection, smoke | 1 system |
| Power | Dual 30A 208V circuits per rack from separate panels; metered PDUs | 4 circuits |
2.2.3 Communications Room (200 sq ft)
| Element | Specification | Quantity |
| RF equipment rack | Open-frame 24U rack for RF transceivers, amplifiers, combiners | 1 |
| Antenna feedlines | LMR-400 or equivalent low-loss coax; conduit to roof penetrations | 6 runs |
| Network demarcation | ISP handoff point; dual ISP termination | 2 demarcs |
| Grounding | Single-point ground bus; all coax and equipment grounded per NFPA 780 | 1 system |
| RF shielding | Copper mesh or foil on walls if EMI testing indicates interference | As needed |
| Cable trays | Overhead trays from server room through comms room to roof | Continuous |
2.2.4 Equipment Staging Area (300 sq ft)
| Element | Specification | Quantity |
| Workbench | Heavy-duty, 72"x30", ESD-safe surface, integrated power strip | 2 |
| Battery storage cabinet | Fire-rated (UL 1275), ventilated, LiPo-rated, temp-monitored | 1 (holds 20+ batteries) |
| Battery charging station | Manufacturer charger (Skydio); dedicated 20A circuit per station | 4 charging bays |
| Shelving | Heavy-duty, 48"x24"x72", for vehicle spares and accessories | 4 units |
| Tool storage | Lockable tool cabinet, organized per manufacturer maintenance kit | 1 |
| Ventilation | Exhaust fan, 200 CFM minimum, activated by smoke/thermal sensor | 1 |
| Sink | Utility sink for cleaning; eye wash station | 1 |
2.2.5 Support Spaces
| Space | Size (sq ft) | Key Requirements |
| Briefing Room | 250 | Display (75" or projector), whiteboard, table for 8, network drops |
| NOC / IT Support | 200 | 2 workstations, direct access to server room, monitoring displays |
| Break Room | 200 | Kitchenette, table for 6, lockers (10) |
| Entry / Security | 150 | Badge reader, visitor sign-in kiosk, camera, waiting area |
| Restrooms | 150 (2) | ADA compliant |
| Storage | 100 | Janitorial, spare parts overflow, document storage |
2.3 Electrical Specification
| System | Specification | Details |
| Utility service | 400A, 208/120V, 3-phase, 4-wire | Primary feed from utility |
| Secondary feed | 200A from separate utility transformer or second service | Redundancy; ATS switches between feeds |
| Automatic Transfer Switch (ATS) | 400A rated, < 10 sec transfer time | Switches between utility feeds and generator |
| Generator | 30 kW diesel, weatherproof enclosure, 500-gal belly tank | 72+ hours runtime at 50% load; auto-start on utility loss |
| UPS (server room) | 10 kVA online double-conversion, 30 min runtime at full load | Covers transfer gap + graceful shutdown if extended outage |
| UPS (ops floor) | 5 kVA online double-conversion, 20 min runtime | Workstations and displays |
| PDU (per rack) | Dual metered PDU, 30A 208V, C13/C19 outlets, network-monitored | Redundant A+B power per server |
| Surge protection | Whole-building SPD at main panel; per-circuit SPDs on sensitive loads | Gulf Coast lightning protection |
| Grounding | NEC-compliant grounding electrode system; isolated technical ground for server room | Single-point ground reference |
2.4 Network Cabling Specification
| Cable Type | Application | Specification | Quantity |
| Cat 6A shielded | Operations LAN, workstations, sensors, PoE cameras | Plenum-rated (CMP), tested to 500 MHz | 60 runs |
| OM4 multimode fiber | Server-to-switch, inter-rack, long runs | 50/125μm, LC duplex, plenum | 12 runs |
| Single-mode fiber | Future WAN/PtP expansion | OS2 9/125μm, LC duplex | 4 runs (pre-install) |
| LMR-400 coax | Antenna feeds (ADS-B, C2, Remote ID) | Low-loss, UV-resistant jacket, N-type connectors | 6 runs to roof |
| Cat 6 standard | Non-critical: break room, briefing room, entry | Plenum-rated | 12 runs |
2.5 Antenna and Roof Infrastructure
| Antenna | Purpose | Spec | Mount |
| ADS-B (1090 MHz) | Manned traffic reception | Omnidirectional, gain 5.5 dBi, N-female | Mast, 10 ft above roof (x2 for redundancy) |
| C2 Primary (900 MHz) | Vehicle command/telemetry | Directional sector, 120°, gain 12 dBi | Mast, adjustable tilt (x2 sectors for coverage) |
| C2 Backup (2.4 GHz) | Backup vehicle link | Omnidirectional, gain 8 dBi | Mast, 8 ft |
| Safety RF (868 MHz) | SS dedicated safety link | Omnidirectional, gain 6 dBi | Separate mast, physically isolated |
| Remote ID (BT5/Wi-Fi) | Ground RID receiver | Integrated antenna on receiver unit | Roof-mount bracket |
| PtP Wireless Backhaul | Link to dock site | 60 GHz PtP dish (e.g., airFiber 60 LR) | Pole mount, line-of-sight to dock |
| Cellular (4G/5G) | WAN backup, edge node failover | MIMO panel antenna, wideband | Mast, 6 ft |
| Weather station | Wx sensor array | Davis VP2 or equiv., integrated mount | Mast, unobstructed, 10 ft above roof |
3. SERVER AND COMPUTE HARDWARE
3.1 Phase 1 Server Bill of Materials
| ID | Item | Specification | Qty | Unit Cost | Ext. Cost |
| SRV-001 | Mission Services Server | Dell PowerEdge R660xs: 1x Xeon 4416+ (20C/40T), 128GB DDR5 ECC (4x32GB), 2x 1.92TB NVMe SSD (RAID 1), dual 10GbE SFP+, iDRAC Enterprise, redundant 800W PSU, 1U rackmount, 5-year ProSupport | 2 | $9,500 | $19,000 |
| SRV-002 | Data Pipeline Server | Dell PowerEdge R660xs: 1x Xeon 4416+ (20C/40T), 128GB DDR5 ECC, 4x 3.84TB NVMe SSD (RAID 10), dual 10GbE SFP+, iDRAC Enterprise, redundant 800W PSU, 1U rackmount, 5-year ProSupport | 2 | $14,000 | $28,000 |
| SRV-003 | Operator UI Server (Phase 1 can colocate on SRV-001) | Reserved slot for Phase 2 dedicated server | 0 | $0 | $0 |
| GPU-001 | AI/ML Inference Server (Phase 3) | Reserved: GPU server with NVIDIA L40 or A4000. Not procured Phase 1. | 0 | $0 | $0 |
3.2 Safety-Critical Compute
| ID | Item | Specification | Qty | Unit Cost | Ext. Cost |
| SAF-001 | Safety Supervisor Node | Kontron KBox A-203-AI or SECO SBC: ARM/x86 safety-rated SBC, 8GB ECC RAM, 128GB industrial SSD, RTOS-compatible, dual Ethernet, serial ports, wide-temp (-20 to 60°C), DIN-rail mount | 2 | $2,500 | $5,000 |
| SAF-002 | Safety RF Transceiver | Custom or COTS 868 MHz transceiver module (e.g., Digi XBee 900HP or LoRa gateway), AES-128 capable, SMA antenna port | 2 | $500 | $1,000 |
3.3 Edge Compute
| ID | Item | Specification | Qty | Unit Cost | Ext. Cost |
| EDG-001 | Dock Edge Node | NVIDIA Jetson Orin NX 16GB dev kit + carrier board, 256GB NVMe, IP65 weatherproof enclosure, PoE+ powered, dual Ethernet, USB3, serial | 1 | $1,800 | $1,800 |
| EDG-002 | Edge UPS | CyberPower CP1500PFCLCD or equiv., 1500VA, sinewave, 10-min runtime | 1 | $300 | $300 |
| EDG-003 | Edge Solar + Battery (off-grid docks) | 100W panel + 50Ah LiFePO4 battery + MPPT controller; 72-hr autonomy at edge load | 0 (Phase 3) | $1,200 | $0 |
3.4 Rack Layout
Two 42U racks in server room. Rack A: compute. Rack B: data + network.
Rack A: Compute (42U)
| U Position | Equipment | Power (A feed) | Power (B feed) |
| U1-U2 | Patch panel + cable management | -- | -- |
| U3 | 10GbE Switch A (Ops LAN A) | PDU-A | PDU-B |
| U4 | Blank (airflow) | -- | -- |
| U5 | SRV-001a (Mission Services Primary) | PDU-A | PDU-B |
| U6 | SRV-001b (Mission Services Standby) | PDU-A | PDU-B |
| U7 | Blank | -- | -- |
| U8-U9 | SAF-001a (Safety Supervisor Primary) + DIN mount shelf | PDU-A | -- |
| U10-U11 | SAF-001b (Safety Supervisor Standby) + DIN mount shelf | -- | PDU-B |
| U12 | Blank | -- | -- |
| U13-U14 | UPS A (server room) | Utility A | -- |
| U15-U42 | Reserved for Phase 2-4 expansion | -- | -- |
Rack B: Data + Network (42U)
| U Position | Equipment | Power (A feed) | Power (B feed) |
| U1-U2 | Patch panel + cable management | -- | -- |
| U3 | 10GbE Switch B (Ops LAN B) | PDU-A | PDU-B |
| U4 | Firewall/Router appliance | PDU-A | PDU-B |
| U5 | Blank | -- | -- |
| U6 | SRV-002a (Data Pipeline Primary) | PDU-A | PDU-B |
| U7 | SRV-002b (Data Pipeline Standby) | PDU-A | PDU-B |
| U8 | Blank | -- | -- |
| U9 | Redis / auxiliary services (if separate) | PDU-A | PDU-B |
| U10 | Blank | -- | -- |
| U11-U12 | UPS B (server room) | Utility B | -- |
| U13 | Prometheus / Grafana monitoring | PDU-A | -- |
| U14-U42 | Reserved for Phase 2-4 | -- | -- |
4. NETWORK EQUIPMENT
4.1 Network Bill of Materials
| ID | Item | Specification | Qty | Unit Cost | Ext. Cost |
| NET-001 | Core Switch (10GbE) | Ubiquiti USW-Enterprise-24-PoE or equiv: 24x 2.5GbE PoE+, 2x 10G SFP+, managed, VLAN, L3 lite | 2 | $800 | $1,600 |
| NET-002 | 10GbE SFP+ modules | Compatible 10GBASE-SR SFP+ for server uplinks | 8 | $30 | $240 |
| NET-003 | Firewall / Router | Protectli Vault FW6E or Netgate 6100: 6x GbE, pfSense/OPNsense, dual WAN, VPN, IDS/IPS | 1 | $900 | $900 |
| NET-004 | PtP Wireless Backhaul | Ubiquiti airFiber 60 LR pair: 60 GHz, 1+ Gbps, 12+ km range | 1 pair | $1,400 | $1,400 |
| NET-005 | Cellular Modem (WAN backup) | Sierra Wireless RV55 or Cradlepoint: 4G LTE Cat 12, dual SIM, Ethernet out | 1 | $600 | $600 |
| NET-006 | PoE Injector (outdoor) | Ubiquiti POE-48-24W or equiv for edge/outdoor equipment | 4 | $30 | $120 |
| NET-007 | Patch cables (Cat 6A) | Various lengths: 3ft, 7ft, 15ft, shielded | 50 | $8 | $400 |
| NET-008 | Fiber patch cables (OM4) | LC-LC duplex, 1m and 3m | 12 | $15 | $180 |
4.2 Network Architecture Diagram Description
Dual-path architecture ensuring no single point of failure for operational traffic:
- ISP A -> Firewall WAN1 -> Core Switch A (Ops LAN A) -> Server NIC A (all servers) -> Workstation NIC A
- ISP B -> Firewall WAN2 -> Core Switch B (Ops LAN B) -> Server NIC B (all servers) -> Workstation NIC B
- Inter-switch link: 10GbE fiber between Switch A and Switch B for cross-path redundancy
- Safety bus: Dedicated Ethernet from SAF-001 nodes, NOT connected to Ops LAN switches. Direct crossover or isolated mini-switch.
- Edge backhaul: PtP wireless from dock site -> dedicated VLAN on Ops LAN A + cellular failover on separate VLAN
- Management VLAN: Separate VLAN for iDRAC/IPMI, switch management, UPS SNMP, environmental monitoring
4.3 VLAN Design
| VLAN ID | Name | Purpose | Subnet |
| 10 | OPS-A | Operations LAN A (primary inter-subsystem) | 10.10.10.0/24 |
| 20 | OPS-B | Operations LAN B (redundant) | 10.10.20.0/24 |
| 30 | SAFETY | Safety bus (SS nodes only) | 10.10.30.0/29 |
| 40 | EDGE | Edge node backhaul | 10.10.40.0/24 |
| 50 | MGMT | Management (iDRAC, IPMI, switches, UPS) | 10.10.50.0/24 |
| 60 | WAN | Internet-facing (firewall external) | DHCP from ISP |
| 70 | DMZ | API gateway, LAANC, Remote ID upload | 10.10.70.0/24 |
| 80 | WIFI | Guest/visitor Wi-Fi (isolated) | 10.10.80.0/24 |
5. SENSOR EQUIPMENT
5.1 Sensor Bill of Materials
| ID | Item | Specification | Qty | Unit Cost | Ext. Cost |
| SEN-001 | ADS-B Receiver | FlightAware Pro Stick Plus (1090 MHz) + Raspberry Pi 4 (4GB) + outdoor enclosure + filtered preamp. Runs dump1090-fa, outputs Beast/SBS TCP. | 2 | $350 | $700 |
| SEN-002 | Remote ID Receiver | ANRA Smart Skies receiver or open-source SDR-based (Bluetooth 5 + Wi-Fi NaN). ASTM F3411 compliant. Edge node integration. | 1 | $3,500 | $3,500 |
| SEN-003 | Weather Station | Davis Vantage Pro2 Plus: wind speed/dir, temp, humidity, barometric pressure, rain gauge, UV/solar. WeatherLink IP data logger. | 1 | $1,200 | $1,200 |
| SEN-004 | Ceilometer (Phase 2) | Vaisala CL31 or equivalent cloud base sensor. Serial/Ethernet output. Not procured Phase 1. | 0 | $15,000 | $0 |
| SEN-005 | PTZ Camera | Axis Q6135-LE: 32x optical zoom, 1080p60, IR illuminator (200m), PoE+, IP67, ONVIF. For dock/ops monitoring. | 1 | $4,500 | $4,500 |
| SEN-006 | RF Spectrum Monitor (Phase 2) | ThinkRF R5750 or equiv real-time spectrum analyzer, 9 kHz - 27 GHz. | 0 | $25,000 | $0 |
| SEN-007 | Outdoor Environmental Sensor | Temp/humidity/pressure sensor for dock site, RS-485 or Modbus output | 1 | $200 | $200 |
5.2 Sensor Placement
| Sensor | Location | Mounting | Coverage/Notes |
| ADS-B #1 | Facility roof, south side | 10 ft mast, ground plane | Primary: covers south approach to KLFT |
| ADS-B #2 | Facility roof, north side | 10 ft mast, ground plane | Redundant: covers north; combined 360° |
| Remote ID #1 | Facility roof, center | Bracket on existing mast | ~1 km BT / ~2 km Wi-Fi radius from facility |
| Weather Station | Facility roof, unobstructed | Tripod mount, 10 ft AGL | 30 ft clear of obstacles per WMO guidelines |
| PTZ Camera #1 | Facility roof or dock site | Pole mount, weatherproof | Covers primary dock launch/recovery area |
| Env. Sensor | Dock site, integrated with edge node | Bracket on dock enclosure | Local conditions at dock |
6. DRONE PLATFORM AND DOCK PROCUREMENT
6.1 DJI — REMOVED (Regulatory Risk: Countering CCP Drones Act)
> DJI REMOVED — REGULATORY RISK (March 2026)

The Countering CCP Drones Act (passed US House, advancing Senate) would add DJI to the FCC Covered List, effectively banning DJI from US commercial airspace operations. DJI hardware is NOT approved for this project.

DJI specs in the table below are retained for historical reference ONLY. Do not procure.

COMMITTED PLATFORM: Skydio X10 + Skydio Dock. See section 6.1 (Committed Platform) and SkyCommand_Technology_Stack for full rationale.
6.1 COMMITTED PLATFORM: Skydio X10 + Skydio Dock
| ID | Item | Specification | Qty | Unit Cost | Ext. Cost |
| DRN-B01 | Skydio Dock | Autonomous dock, weatherproof, battery charging, Skydio Cloud integration | 1 | $14,000 | $14,000 |
| DRN-B02 | Skydio X10 | Visual/thermal sensors, GPS-denied navigation, 35 min flight, autonomous obstacle avoidance, Skydio Autonomy Engine | 1 | $12,000 | $12,000 |
| DRN-B03 | Skydio X10 Payload (Thermal Wide) | Wide + thermal dual payload for DFR/inspection | 1 | $5,000 | $5,000 |
| DRN-B04 | Skydio X10 Battery | Additional batteries | 4 | $350 | $1,400 |
| DRN-B05 | Skydio Care | Extended support | 1 | $2,000 | $2,000 |
6.3 Platform Selection Criteria
PLATFORM DECISION (March 2026): Skydio X10 + Skydio Dock is the committed primary platform. DJI has been removed from consideration due to Countering CCP Drones Act regulatory risk — DJI would be added to FCC Covered List, banning it from US commercial operations. Proceed with Skydio SDK evaluation sprint in Month 1. All DJI procurement items are deprecated — do not order.
6.4 Dock Site Infrastructure (Per Site)
| ID | Item | Specification | Qty | Unit Cost | Ext. Cost |
| DOCK-001 | Concrete pad | 10 ft x 10 ft, 6" thick, rebar reinforced, level ±1/4", anchor bolts for dock | 1 | $3,000 | $3,000 |
| DOCK-002 | Security enclosure | Chain-link or welded wire, 12 ft x 12 ft, 6 ft high, lockable gate, tamper sensor | 1 | $2,500 | $2,500 |
| DOCK-003 | Power connection | 200A service panel, 20A circuit for dock, 20A for edge node, ground rod | 1 | $3,500 | $3,500 |
| DOCK-004 | Edge node enclosure | NEMA 4X weatherproof box, DIN rail, fan/filter, cable glands | 1 | $400 | $400 |
| DOCK-005 | Security camera | Axis M3116-LVE or equiv, 4MP, PoE, IR, vandal-resistant | 1 | $350 | $350 |
| DOCK-006 | Signage | FAA-required UAS operations signage; no trespassing | 1 | $100 | $100 |
7. VENDOR EVALUATION FRAMEWORK
7.1 Vendor Qualification Requirements
- Minimum 3 years in business with UAS/defense/critical infrastructure customers
- Demonstrated product support: US-based technical support, < 4 hour response SLA for critical issues
- API/SDK documentation quality: complete, versioned, with changelog and migration guides
- Security posture: SOC 2 Type II or equivalent; vulnerability disclosure process
- Supply chain: ability to deliver within 30 days of PO; identify lead-time risks
- References: minimum 2 customer references in similar operational context
7.2 Evaluation Scorecard
| Category | Weight | Scoring (1-5) | Evidence Required |
| Technical fit | 30% | Meets all functional requirements in spec | Feature matrix comparison; proof-of-concept |
| Integration complexity | 20% | SDK quality, API completeness, adapter effort estimate | 2-week SDK evaluation sprint results |
| Reliability / track record | 15% | Field failure rates, uptime data, customer satisfaction | References, public incident data, forums |
| Support and responsiveness | 15% | SLA, escalation path, local presence, training offered | Support contract review, trial support interaction |
| Total cost (3-year) | 10% | Hardware + SW licensing + support + consumables | TCO model with all line items |
| Strategic alignment | 10% | Roadmap alignment, openness, multi-vendor friendly | Roadmap presentation, contract terms review |
7.3 Procurement Process
1. Technical Lead issues Requirements Specification to candidate vendors
1. Vendors submit technical response + pricing within 3 weeks
1. Evaluation team scores submissions per scorecard
1. Top 2 vendors invited for SDK proof-of-concept (2 weeks each)
1. Final selection based on POC results + scorecard + references
1. Contract negotiation: SLA, warranty, IP terms, API stability guarantees
1. Purchase order issued; delivery tracked against critical path
8. COMPLETE BUDGET SUMMARY
8.1 Phase 1 Hardware and Facility Budget
| Category | Item Range | Low Est. | High Est. |
| Facility build-out | Lease improvement, construction, HVAC, electrical, fire suppression | $150,000 | $250,000 |
| Servers (SRV-001, SRV-002) | 4 servers (2 mission + 2 data pipeline) | $38,000 | $52,000 |
| Safety compute (SAF-001/002) | 2 safety nodes + 2 RF transceivers | $5,000 | $7,000 |
| Edge compute (EDG-001/002) | 1 edge node + UPS | $2,100 | $3,000 |
| Network equipment | Switches, firewall, PtP wireless, cabling, cellular | $5,440 | $8,000 |
| UPS and power | Rack UPS, PDUs, surge protection | $6,000 | $10,000 |
| Generator + ATS | 30 kW diesel + automatic transfer switch + fuel tank | $18,000 | $25,000 |
| Sensors | ADS-B, Remote ID, weather, PTZ camera, env sensor | $10,100 | $15,000 |
| Drone platform (Skydio (committed)) | Dock + vehicle + payload + batteries + warranty | $38,100 | $42,000 |
| Dock site infrastructure | Concrete, security, power, enclosure, camera, signage | $9,850 | $14,000 |
| Operator workstations | 4 desks + 8 monitors + video wall (6 displays) + peripherals | $18,000 | $25,000 |
| Miscellaneous (tools, spares, consumables) | Maintenance tools, spare props, cables, connectors | $5,000 | $8,000 |
8.2 Phase 1 Total
|  | Low Estimate | High Estimate |
| Hardware + Facility Subtotal | $305,590 | $459,000 |
| Contingency (15%) | $45,839 | $68,850 |
| TOTAL HARDWARE + FACILITY | $351,429 | $527,850 |
Note: Software development labor, licensing, FAA fees, insurance, and operational staffing costs are not included in this hardware/facility budget. Total Phase 1 program cost including labor is estimated at $800K - $1.2M per the System Architecture Document.
8.3 Phase 2-4 Forward Procurement Estimates
| Phase | Key Additions | Est. Hardware Cost |
| Phase 2 | Safety Supervisor dedicated HW, ADS-B expansion, 2nd vehicle type + dock, additional sensors, expanded network | $150K - $250K |
| Phase 3 | AI/GPU server, 3 additional docks + edge nodes, DAA radar/visual sensor, corridor infrastructure | $400K - $700K |
| Phase 4 | 5+ additional docks, redundant facility or cloud-hybrid, multi-operator network expansion | $600K - $1.2M |
9. PROCUREMENT TIMELINE
9.1 Critical Path Procurement Schedule
| Item | Order By | Lead Time | Needed By | Critical Path? |
| Server hardware (SRV-001/002) | Week 1 | 2-4 weeks | Week 4 (Sprint 1) | YES |
| Network equipment (switches, firewall) | Week 1 | 1-2 weeks | Week 3 | YES |
| Drone platform + dock (Skydio) | Week 1 | 4-6 weeks | Week 8 (Sprint 4) | YES |
| Safety compute (SAF-001) | Week 4 | 3-4 weeks | Week 12 (Phase 2 prep) | No |
| Edge node (Jetson Orin NX) | Week 2 | 2-3 weeks | Week 6 | YES |
| UPS + PDU | Week 1 | 1-2 weeks | Week 3 | YES |
| Generator | Week 1 | 6-8 weeks | Week 10 | No (UPS covers interim) |
| ADS-B receivers | Week 2 | 1 week (COTS) | Week 6 | No |
| Remote ID receiver | Week 2 | 4-6 weeks | Week 8 | No |
| Weather station | Week 2 | 1-2 weeks | Week 6 | No |
| PTZ camera | Week 2 | 2-3 weeks | Week 8 | No |
| Operator workstations + monitors | Week 2 | 2-3 weeks | Week 6 | No |
| Dock site construction | Week 1 (contract) | 6-8 weeks | Week 8 | YES |
| Facility build-out | Week 1 (contract) | 8-12 weeks | Week 8 (server room critical) | YES |
9.2 Procurement Responsibilities
| Role | Responsibilities |
| Technical Lead | Approve all technical specifications; final vendor selection; change requests |
| DevOps / Infrastructure | Server, network, UPS specs; rack layout; receive and configure equipment |
| Integration Engineer | Drone platform, dock, sensors, edge node specs; vendor SDK evaluation |
| Operations Manager | Facility build-out oversight; dock site construction; generator; furniture |
| Procurement / Admin | PO issuance, delivery tracking, warranty registration, invoice processing |
9.3 Warranty and Support Summary
| Equipment | Warranty | Support Level | Renewal |
| Dell servers | 5 yr ProSupport | 4-hr onsite response | Renew at Year 5 |
| Network switches | Limited lifetime | RMA replacement | N/A |
| Firewall appliance | 1 yr hardware | Community support (pfSense) | Netgate TAC optional |
| REMOVED (Skydio deprecated) | 1 yr standard + Enterprise Shield | REMOVED — use Skydio support | Renew annually |
| Skydio (if selected) | 1 yr + Skydio Care | Skydio enterprise support | Renew annually |
| NVIDIA Jetson | 2 yr | Developer community + NVIDIA enterprise | N/A |
| Davis Weather Station | 2 yr | Email/phone support | N/A |
| Axis Camera | 3 yr | Axis partner support | Extended warranty available |
| Generator | 2 yr / 2000 hrs | Dealer service agreement | Service contract recommended |
END OF DOCUMENT
KLFT Autonomous Airspace Operations Hub — Facility & Hardware Procurement Specification v1.0
---
> GPU HARDWARE UPDATE — March 2026

GPU-001 (AI/ML Inference Server, Phase 3) spec has been revised:

DEPRECATED: NVIDIA A4000 (Ampere, 16GB) — two generations old. Do not procure.

CURRENT SPEC (Phase 3, AI inference node):
• Primary: NVIDIA L40S (Ada Lovelace, 48GB GDDR6, 91.6 TFLOPS FP32) — optimal for inference workloads, available in standard PCIe servers. ~$8,000-10,000 per card.
• Alternative: NVIDIA H100 PCIe 80GB — for combined training + inference. ~$25,000+ per card. Overkill for Phase 3 inference-only workloads; evaluate based on actual AI model requirements.
• Edge compute (EDG-001): NVIDIA Jetson Orin NX 16GB — CURRENT. No change needed. Still the right choice for dock-side edge nodes.

Phase 3 GPU procurement: confirm actual AI model inference requirements before purchasing. L40S in a 1U Dell PowerEdge R7525 or R760 is the recommended Phase 3 config.
> UPDATED 2026-03-23: GPU spec confirmed as L40S (Ada Lovelace, 48GB) -- correct and current. DJI removal confirmed (CCP Drones Act). Skydio X10 + Dock remains primary platform. Power hierarchy for KLFT facility follows the locked 4-layer standard: Solar -> Natural Gas -> Diesel -> Grid (backup). Any Bloom Energy references in other docs are superseded.