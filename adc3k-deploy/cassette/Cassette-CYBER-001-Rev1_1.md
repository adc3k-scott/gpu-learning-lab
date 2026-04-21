# Cassette — CYBERSECURITY ARCHITECTURE

**Document:** Cassette-CYBER-001
**Revision:** 1.1
**Date:** 2026-04-20
**Classification:** CONFIDENTIAL
**Status:** Released

**Companion documents:** Cassette-CTRL-001 Rev 1.1 · Cassette-MODES-001 Rev 1.1 · Cassette-SIS-001 Rev 1.1 · Cassette-TAGS-001 Rev 1.1 · Cassette-INT-001 Rev 3.0 · Cassette-CDUSKID-001 Rev 1.0

| Rev | Date       | Description                                                                        |
|-----|------------|------------------------------------------------------------------------------------|
| 1.0 | 2026-04-20 | Initial release. Applies IEC 62443 framework to the deployed Cassette edge AI compute node. Defines Security Levels, Zones & Conduits, network segmentation with hardware data diode, identity & access model, device authentication (certificate-based), firmware signing chain, patch management, monitoring (SIEM) integration, incident response playbook, and compliance mapping to IEC 62443, NIST CSF 2.0, and oil & gas customer audit frameworks (API 1164, TSA Pipeline Security Directives). Target SL-T = SL-3 for Zone 2 (basic control). |
| **1.1** | **2026-04-20** | **Companion documents updated to Rev 3.0 baseline. CDU skid PLC (Siemens S7-1500F per CDUSKID-001 §17) added to Zone 2 inventory. Skid-side OPC UA server authentication requirements noted against CDUSKID-001 cybersecurity clause. BMS rack relocation to Service End Zone (INT-001 Rev 3.0 §20) does not affect security boundary. No changes to zone architecture, data diode spec, or SL-T targets.** |

**Prepared by:** Scott Tomsu · CEO / Chief Engineer
scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana

---

## TABLE OF CONTENTS

- §1  Scope, Objectives & Standards
- §2  Threat Model
- §3  Zone & Conduit Model (IEC 62443-3-2)
- §4  Security Level Targets (SL-T)
- §5  Network Architecture & Segmentation
- §6  Data Diode — OT/IT Boundary
- §7  Asset Inventory & Hardening Baselines
- §8  Identity, Authentication, Access Control
- §9  Device Authentication & PKI
- §10 Encryption & Data Protection
- §11 Firmware & Software Supply Chain
- §12 Patch Management
- §13 Monitoring, Logging & SIEM Integration
- §14 Incident Response Playbook
- §15 Physical Security
- §16 Vendor / Third-Party Access
- §17 Testing & Assurance
- §18 Compliance Mapping
- §19 Open Items

---

## §1  SCOPE, OBJECTIVES & STANDARDS

### Scope

This document specifies the cybersecurity architecture for the deployed Cassette edge AI compute node. It covers the OT network (Zones 0–3 per IEC 62443), the OT/IT boundary (DMZ / data diode), and the cloud-side enterprise layer (Zone 4) as it pertains to OT data exchange.

### Objectives

1. **Prevent remote compromise** of OT systems from any internet-connected endpoint
2. **Detect** unauthorized access attempts, lateral movement, and anomalous commands
3. **Contain** compromise to the smallest possible zone
4. **Recover** to known-good state without data loss or extended downtime
5. **Comply** with oil & gas customer OT security requirements (audit-ready)
6. **Preserve safety** — cybersecurity controls must not impair SIS response times or safe-state transitions

### Standards

| Standard | Title | Application |
|----------|-------|-------------|
| IEC 62443-1-1 | Terminology, concepts, and models | Foundation |
| IEC 62443-2-1 | Security program requirements | ADC organizational |
| IEC 62443-2-4 | Requirements for service providers | Integrators, vendors |
| IEC 62443-3-2 | Risk assessment for system design | Zone & conduit determination |
| IEC 62443-3-3 | System security requirements and security levels | Primary technical spec (7 FRs) |
| IEC 62443-4-1 | Secure product development lifecycle | Software vendor requirement |
| IEC 62443-4-2 | Technical security requirements for IACS components | Device-level spec |
| NIST CSF 2.0 | Cybersecurity Framework | Governance mapping |
| NIST SP 800-82 | Guide to Operational Technology Security | US federal alignment |
| API 1164 | Pipeline SCADA Security | Oil & gas customer alignment |
| TSA Security Directive Pipeline-2021-02 | Mandatory pipeline OT controls | US pipeline customers |
| ISA/IEC 62443 SCA | Security Conformance Assessment | Certification pathway |

### Principle: Safety Overrides Security

No cybersecurity control may impair the operation of the Safety Instrumented System (SIS). If a control cannot be implemented without affecting SIS response time or availability, it is redesigned or omitted. This is an absolute rule from IEC 61511 clause 8.2.4 and IEC 62443-3-3.

---

## §2  THREAT MODEL

### Threat Actors

| Actor | Motivation | Capability | Likelihood (upstream oil & gas) |
|-------|-----------|------------|----------------------------------|
| Nation-state (APT) | Disruption of energy infrastructure | Very high (0-day, supply chain, custom) | Moderate |
| Organized criminal | Ransom payment | High (commodity ransomware, social eng) | High |
| Hacktivist | Publicity, climate agenda | Low–medium (opportunistic) | Moderate |
| Malicious insider | Revenge, payment | Medium (authorized access) | Low–moderate |
| Negligent insider | Accident | Variable | **Highest** (most common cause) |
| Supply chain | Compromised vendor, counterfeit part | Variable | Moderate |
| Physical intruder | Theft, sabotage, recon | Low technical but direct access | Site-specific |

### Attack Vectors (Ranked by Likelihood)

1. **Phishing → remote access** — corporate email compromise pivots to VPN into OT
2. **Vendor remote support tunnel** — unmonitored, over-privileged maintenance connection
3. **USB / removable media** — engineering laptop carries malware into OT
4. **Supply chain compromise** — signed but malicious firmware update
5. **Stolen credentials** — reused password from enterprise breach
6. **Physical access → console** — direct port on a PLC, HMI, or switch
7. **Wireless** — rogue Wi-Fi, Bluetooth, Zigbee if mistakenly enabled
8. **Lateral from IT** — segmentation failure allows IT compromise to reach OT

### Assets to Protect (Priority Order)

| Rank | Asset | Why |
|------|-------|-----|
| 1 | Safety Instrumented System (SIS) | Personnel safety; loss of integrity = fatal incident |
| 2 | 800 VDC main breaker control + switchgear | Arc flash / fire initiation potential |
| 3 | Fuel control valves (genset) | Explosion, fire initiation |
| 4 | Cassette Jetson BMS | Could command thermal / power compromise of $15M+ of GPUs |
| 5 | CDU skid PLC | Loss of flow could damage GPU fleet |
| 6 | Protective relays (switchgear) | Mis-operation creates arc flash, prevents trip |
| 7 | Genset EMCPs | Overspeed, destructive shutdown |
| 8 | Historian / event logs | Forensic integrity after incident |
| 9 | Operator HMI & SCADA | Deception of operators |
| 10 | Business data (customer workloads) | Customer confidentiality |

### Key Design Consequences

- Safety and primary-power isolation gets the highest protection (redundant sensors, offline logic, no remote reconfiguration)
- Remote management of Zones 0–2 is **prohibited** — all changes go through a manual, signed, two-person process via physically-present engineering laptop
- Outbound telemetry is allowed through a hardware data diode; inbound commands from cloud are **impossible** at the hardware level

---

## §3  ZONE & CONDUIT MODEL (IEC 62443-3-2)

### Zones

A security zone is a grouping of logical or physical assets that share common security requirements.

| Zone | Name | Purpose | Assets |
|------|------|---------|--------|
| 0    | Safety | SIS only, complete isolation | SIS PLC, SIS sensors, SIS final elements, SIS HMI |
| 1    | Process I/O | L0 field devices, direct-attached | ADAM modules, TraceTek, VESDA, pressure sensors, actuators |
| 2    | Basic Control | L1 PLCs, embedded controllers | Siemens S7-1500 (CDU), S7-1200 (Munters), Cat EMCPs, SEL relays, Cassette Jetson Orin BMS |
| 3    | Site Operations | L2–L3 supervision | Ignition Gateway servers, Protocol Gateway, Historian, Digital Twin, Operator HMI |
| 3.5  | DMZ | Controlled OT/IT exchange | Jump server, PAM (privileged access mgmt), signed-update staging |
| 4    | Enterprise / Cloud | L4 analytics, dashboards | Fleet dashboard, Timestream/TimescaleDB, ML training, customer portal |
| B    | Business / Corporate | ADC enterprise IT | Email, file shares, ticketing — unrelated to deployment operations |

### Conduits

A conduit is an authorized communication path between zones.

| Conduit ID | From | To | Protocol(s) | Direction | Notes |
|------------|------|-----|-------------|-----------|-------|
| C-1 | 0 | 1 | hardwired analog/discrete | ←→ | SIS sensors read field devices physically |
| C-2 | 0 | 2 | dry-contact + MBTCP read-only | → | SIS publishes state to BPCS |
| C-3 | 1 | 2 | Modbus RTU, fieldbus, discrete | ←→ | Field I/O to PLCs |
| C-4 | 2 | 3 | OPC UA, MQTT Sparkplug B | ←→ | Gateway translation |
| C-5 | 2 | 2 | IEC 61850 GOOSE | ←→ | Switchgear peer-to-peer for trip coordination |
| C-6 | 3 | 3.5 | OPC UA, SSH (admin) | ←→ | Site ops to DMZ, authenticated |
| C-7 | 3.5 | 4 | HTTPS (TLS 1.3), MQTT/TLS | → only (data diode enforced) | Telemetry egress only |
| C-8 | 3.5 | 3 | Signed update payloads via USB or out-of-band | → | Firmware / config updates, manual promotion |
| C-9 | 4 | B | HTTPS | ←→ | Between ADC cloud and corp for business data |

Everything else is denied. No direct link 4→3, 3→2, or 2→1 for control commands from outside.

### Zone Boundary Enforcement

Each zone boundary has a defined enforcement mechanism:

| Boundary | Enforcement |
|----------|-------------|
| Zone 0 ←→ Zone 1 | Physical-layer separation (dedicated SIS sensor wiring) |
| Zone 0 → Zone 2 | Physical dry contacts + unidirectional Modbus gateway (SIS MODBUS slave only; BPCS cannot write) |
| Zone 1 ←→ Zone 2 | Cable terminations at PLC cabinet (physical, switch-controlled) |
| Zone 2 ←→ Zone 3 | Managed industrial firewall (stateful inspection, deep packet inspection for OPC UA / Modbus) |
| Zone 3 ←→ Zone 3.5 (DMZ) | Firewall with strict ACL |
| Zone 3.5 → Zone 4 | **Hardware data diode** (unidirectional physical layer) |
| Zone 3.5 ←→ Zone 4 for updates | USB air-gap with dual-authentication manual promotion |

---

## §4  SECURITY LEVEL TARGETS (SL-T)

### SL Definitions (IEC 62443-3-3)

| Level | Definition | Typical attacker |
|-------|-----------|-----------------|
| SL 1 | Protection against casual / coincidental | No specific skills; curiosity-driven |
| SL 2 | Protection against intentional violation with simple means | Low skills, generic tools |
| SL 3 | Protection against intentional violation with sophisticated means, moderate resources, IACS-specific skills | Organized, skilled, industry-knowledgeable |
| SL 4 | Protection against intentional violation with sophisticated means, extended resources, IACS-specific skills | Nation-state |

### SL-T Assignments by Zone

| Zone | Name | SL-T | Rationale |
|------|------|------|-----------|
| 0 | Safety | **SL 3** | SIS integrity failure = safety incident; IEC 61511 / NAMUR NA 163 guidance |
| 1 | Process I/O | SL 2 | Field I/O compromise limited by PLC-level interlocks |
| 2 | Basic Control | **SL 3** | Direct control over valves, breakers, pumps; attacker with IACS skills should not succeed |
| 3 | Site Operations | SL 2 | Higher attack surface but compensating controls at Z3↔Z2 boundary |
| 3.5 | DMZ | SL 2 | Isolation zone; strict protocols only |
| 4 | Enterprise | SL 2 | IT-class controls; not operationally critical with data diode in place |

### Seven Foundational Requirements (IEC 62443-3-3)

| FR | Foundational Requirement | Zone 2 Target |
|----|--------------------------|---------------|
| FR 1 | Identification and Authentication Control | SL 3 |
| FR 2 | Use Control | SL 3 |
| FR 3 | System Integrity | SL 3 |
| FR 4 | Data Confidentiality | SL 2 |
| FR 5 | Restricted Data Flow | SL 3 (strong conduits) |
| FR 6 | Timely Response to Events | SL 2 |
| FR 7 | Resource Availability | SL 3 (mustn't compromise uptime) |

Detailed control-by-control mapping in §18.

---

## §5  NETWORK ARCHITECTURE & SEGMENTATION

### Physical Networks

Three physically separate Ethernet networks:

1. **Process Bus** (Zones 0 + 1 + 2) — industrial Ethernet, PTP-aware, redundant ring (RSTP or PRP)
2. **Control LAN** (Zone 3) — SCADA, historian, HMI, orchestrator
3. **Business LAN** (Zone 4 + B) — cloud-bound via Starlink / fiber

### Segmentation Controls

| Segment boundary | Mechanism | Rules |
|------------------|-----------|-------|
| Zone 0 (SIS) | Dedicated switch, dedicated PLC, dedicated I/O, dedicated cabinet | No Ethernet to any other zone; dry contacts + unidirectional Modbus only |
| Zone 1 ↔ Zone 2 | PLC chassis — I/O is inherent to the PLC | — |
| Zone 2 ↔ Zone 3 | Industrial DMZ firewall (Cisco ISA-3000, Fortinet FortiGate Rugged, Hirschmann Tofino) | Stateful, DPI for OPC UA/Modbus; allowlist only |
| Zone 3 ↔ Zone 3.5 | Same firewall, different ACL | Jump server access only; no direct HMI ↔ cloud path |
| Zone 3.5 → Zone 4 | **Hardware data diode** (Waterfall, Owl, Siemens DiodeX) | Physically unidirectional |
| Firmware updates | USB air-gap + dual-person approval | Manual, logged, signed |

### VLAN Allocations

| VLAN | Zone | Purpose |
|------|------|---------|
| 10 | 0 | SIS (physically separate switch, not a VLAN on shared infra) |
| 20 | 1 | Field I/O trunk |
| 30 | 2 | PLC ↔ PLC (CDU, Munters, chiller, gensets, EMCP gateway) |
| 35 | 2 | Protective relay process bus (IEC 61850) — physically separate in production |
| 40 | 3 | SCADA server cluster |
| 45 | 3 | Historian |
| 50 | 3 | Operator HMI workstations |
| 60 | 3.5 | DMZ — jump server, PAM, update staging |
| 80 | 4 | Cloud egress (diode output side) |

### Wireless

- **No wireless in Zones 0–2** under any circumstances
- Wi-Fi and Bluetooth explicitly **disabled in firmware** on all OT devices that support it (ADAM modules, Jetson Orin — verify BT/Wi-Fi off)
- Wireless permitted only in Zone B (corporate, unrelated to operations)

### Remote Site Link

- Starlink primary, 4G/5G secondary — terminates in Zone 4 (cloud-side)
- **No inbound route from internet to any OT zone** — hardware diode enforces this
- Outbound telemetry allowed per §6

---

## §6  DATA DIODE — OT/IT BOUNDARY

### Purpose

Physical-layer unidirectional transfer of telemetry from OT (Zone 3.5) to IT / Cloud (Zone 4). Prevents remote compromise from any internet-connected endpoint.

### Product

- **Waterfall Security Unidirectional Security Gateway (USG)** — preferred; strong industry adoption in oil & gas, refineries, and utilities
- **Owl Cyber Defense DualDiode** — alternative with similar characteristics
- **Siemens DiodeX** (where Siemens-aligned customer preference exists)

All three products are optical-fiber-based: a transmitting laser on the OT side pipes through an air gap to a receiving photodetector on the IT side. There is physically no return path for light or electrical signal.

### Protocols Supported

- OPC UA publisher → subscriber (via vendor's OPC UA proxy)
- MQTT Sparkplug B publisher (OT) → broker (IT)
- Syslog push (OT → IT SIEM)
- File transfer (FTP, SCP) one-way
- Database replication (one-way CDC streaming)

### Firmware Update Path

Updates cannot flow through the diode (that would require a reverse channel, which is physically impossible). Instead:

1. Update package prepared on Zone 4 (enterprise)
2. Update package signed by ADC release engineer (private key kept in HSM)
3. Package burned to write-once media (USB drive configured as read-only at filesystem level, or CD-R)
4. Media physically delivered to site (hand-carried by authorized personnel)
5. On-site engineer (two-person rule) inserts media into staging jump server in Zone 3.5
6. Jump server verifies signature against trusted CA
7. Jump server stages package; operator promotes to target PLC / HMI / server
8. Update applied during maintenance window
9. Media securely disposed

This process is deliberate and cannot be bypassed. It is slower than internet-based patch management; that's acceptable given the threat model.

### Return-Path for Emergencies

If a remote reset or tele-support is genuinely needed, the **only** authorized path is:
- ADC engineer calls customer on phone (out-of-band authentication)
- Customer operator physically goes to the jump server and initiates a PAM session with short-duration, least-privilege credentials
- Session is recorded, logged, and monitored in real time
- Credentials auto-expire at session end

Remote support tunnels (TeamViewer, AnyDesk, cellular modems) — **explicitly prohibited on OT assets**.

---

## §7  ASSET INVENTORY & HARDENING BASELINES

### Asset Classification

Every asset is inventoried with:
- Vendor + model + firmware version
- Serial number + physical location + zone assignment
- Network interfaces + MAC + IP
- Role (controller, HMI, server, gateway, IED, etc.)
- Criticality (for patch prioritization)
- Asset owner + support vendor

Inventory maintained in CMDB — single source of truth. OT Discovery (Claroty, Nozomi, or Dragos agents, see §13) auto-updates inventory from network observation.

### Hardening Baselines by Class

**PLCs (Siemens S7-1500/1200, Cat EMCP, SEL relays)**
- Default passwords changed; strong per-device unique passwords
- Factory test / debug interfaces disabled (`PLCSIM`, remote programming mode off)
- Unused Ethernet ports disabled at the switch and physically blocked
- Firmware locked via keyswitch in RUN position during operation
- Only approved communication protocols enabled (no HTTP, FTP, Telnet)

**Jetson Orin BMS (Ubuntu 22.04)**
- CIS Ubuntu 22.04 benchmark Level 2
- No `root` login via SSH; key-based authentication only, 4096-bit RSA or Ed25519
- `fail2ban` against SSH brute force
- Firewall (`nftables`) default-deny, allowlist only for required protocols
- Unattended-upgrades disabled — patches applied via §12 controlled process
- `auditd` enabled, logs shipped to SIEM
- No development tools in production image (gcc, make, python-dev removed)

**Ignition Gateway servers (Linux)**
- Hardened Linux per CIS L2
- Ignition Gateway runs as unprivileged user; access restricted to its install directory
- Ignition authentication set to Active Directory or LDAP with MFA (not local accounts)
- Module installations restricted; no ad-hoc scripting by operators
- TLS required for all client connections (Perspective, Gateway Network)

**HMI workstations (VisuNet, Beijer, desktop Ignition clients)**
- Full-disk encryption (BitLocker or LUKS)
- Application whitelisting (AppLocker / fapolicyd) — only approved apps run
- USB ports disabled except for authenticated peripherals
- Screen lock after 5 min idle
- No local admin for operator accounts
- Remote sessions logged and recorded

**Network switches (Hirschmann, Cisco IE)**
- Out-of-band management only (dedicated VLAN)
- SSH + SNMPv3 (no Telnet, no SNMPv1/2c)
- Port security: MAC address pinning on field ports
- 802.1X where feasible
- Disabled services: HTTP, TFTP, CDP on external ports
- NTP with authentication

---

## §8  IDENTITY, AUTHENTICATION, ACCESS CONTROL

### Identity Sources

| Zone | Primary | Backup |
|------|---------|--------|
| 4 (Enterprise) | Corporate Azure AD / Okta | — |
| 3, 3.5 | Enterprise AD (joined) + MFA | Local emergency accounts (SOP-restricted) |
| 2 | Local accounts on each device (unique per device) + PAM for elevation | Break-glass paper-stored credentials |
| 1 | Per CTRL-001 ACL roles (§9 of TAGS-001) | — |
| 0 (SIS) | Dedicated SIS accounts (hardware key + credential) | Dual-person break-glass |

### Roles (from TAGS-001 §9)

- Viewer, Operator, Supervisor, Engineer, Integrator, SIS_Authorized, System

### Multi-Factor Authentication

MFA required for:
- Any administrator-level account (Zone 3+)
- Any remote access attempt
- SIS-related operations (hardware key + credential)
- Firmware update promotion
- Mode transitions higher than Operator privilege

MFA factors accepted:
- TOTP app (Google Authenticator, Duo, Authy)
- FIDO2 hardware token (YubiKey 5 NFC) — preferred for engineers
- Push-based (Duo, Okta Verify)
- **SMS explicitly NOT accepted** for OT access (SIM swap attacks)

### Privileged Access Management (PAM)

All privileged sessions routed through a PAM solution (CyberArk, BeyondTrust, HashiCorp Vault) in Zone 3.5.

Functions:
- Password vaulting — OT device passwords rotated automatically, humans never see them
- Session recording — every privileged session fully recorded (screen + keystrokes + protocol)
- Just-in-time elevation — credentials checked out for limited time
- Session review — security team reviews sample of recorded sessions weekly

### Break-Glass Procedure

For emergencies when normal authentication is unavailable:
- Paper-stored credentials in a tamper-evident envelope at site
- Stored in a locked cabinet with access only to shift supervisor + site manager
- Use requires phone call to ADC security (out-of-band authentication)
- Use automatically triggers incident response procedure
- Credentials rotated after any use

### Role Separation

- Operators cannot perform engineering changes (no write access to tuning, limits, SIS)
- Engineers cannot perform SIS reset (requires SIS_Authorized + hardware key)
- Integrators cannot operate the system in production (installation & config only)
- Security team has no operational authority (auditing only)

---

## §9  DEVICE AUTHENTICATION & PKI

### Certificate-Based Device Identity

Every device in Zones 2 and 3 carries a unique X.509 certificate:
- **Root CA** — ADC-operated, offline root, air-gapped HSM
- **Intermediate CA** — online, signs device certificates
- **Device certs** — per device, unique, 1-year validity, auto-rotated

### Certificate Uses

- OPC UA client/server authentication (Basic256Sha256 profile minimum)
- MQTT client authentication (TLS mutual auth)
- PLC/HMI session authentication (where supported — S7-1500 V2.8+, GE/Emerson equivalent)
- Ignition Gateway Network authentication

### Certificate Distribution

- Initial: via secure onboarding at commissioning (technician physically present, device under controlled condition)
- Renewal: automated via EST protocol (RFC 7030) over authenticated conduit
- Revocation: CRL + OCSP, with network appliances pulling the CRL every 1 hour

### No Shared Credentials

The architecture has **zero** shared credentials between devices. Every TLS / OPC UA connection uses unique per-device certs. If one device is compromised, others remain trusted.

---

## §10  ENCRYPTION & DATA PROTECTION

### Data in Transit

| Conduit | Protocol | Encryption |
|---------|----------|------------|
| OPC UA sessions | OPC UA Binary + TLS or OPC UA over Secure Channel | **Basic256Sha256** minimum, Aes128_Sha256_RsaOaep preferred (per OPC UA v1.05) |
| MQTT | MQTT over TLS 1.3 | Required |
| IEC 61850 MMS | MMS + TLS | Required |
| Modbus TCP (legacy) | *Plaintext* — cannot be encrypted | **Mitigate** with strict network segmentation; plan to replace with OPC UA over time |
| IEC 61850 GOOSE | *Plaintext by design* | Physical segmentation + MACsec on supporting switches |
| IEC 61850 SV | *Plaintext by design* | Physical segmentation + MACsec |
| HTTP admin interfaces | TLS 1.3 | Required; plain HTTP disabled |
| SSH | OpenSSH 8+, modern ciphers only | Ed25519 keys; no password auth |
| Syslog to SIEM | TLS 1.3 | Required |

### Data at Rest

- Ignition Gateway server disks: full-disk encryption (LUKS)
- Jetson Orin storage: LUKS-encrypted data partition (InfluxDB + historical data)
- Windows HMI workstations: BitLocker
- USB media for updates: encrypted; signed content + checksum verified on each read
- Backup archives (historian, config): encrypted with per-backup key; keys managed in HSM

### Key Management

- Primary keystore: Hardware Security Module (HSM) — SafeNet Luna or AWS CloudHSM
- Per-device certificate keys: stored in device's TPM (Jetson) or secure element where hardware supports
- Rotation: annual for device certs; 3-year for intermediate CA; 10-year for root CA (offline)
- Backup: root CA private key split via Shamir's Secret Sharing across 5 trustees (3-of-5 threshold)

### Cryptographic Algorithm Policy

**Approved (at time of writing):**
- Symmetric: AES-256-GCM, ChaCha20-Poly1305
- Asymmetric: RSA ≥ 3072-bit, ECDSA P-256 / P-384, Ed25519
- Hash: SHA-256, SHA-384, SHA-512
- KDF: HKDF, Argon2id (for password storage)

**Deprecated / forbidden:**
- MD5, SHA-1 (any use)
- 3DES, RC4, DES
- RSA < 2048-bit
- TLS 1.0, TLS 1.1, SSL any version
- Password-only authentication for OT

**Post-quantum readiness:** monitor NIST PQC standards; be prepared to migrate to hybrid classical/PQ (ML-KEM, ML-DSA) within 5 years of broad support landing in OT products.

---

## §11  FIRMWARE & SOFTWARE SUPPLY CHAIN

### Vendor Requirements

Every software / firmware vendor used in the deployment must:
- Certify IEC 62443-4-1 compliance (secure development lifecycle) — ADC requires vendor statement at procurement
- Provide signed firmware with documented signing key / certificate chain
- Publish Software Bill of Materials (SBOM) — SPDX or CycloneDX format
- Notify ADC of security advisories affecting any installed version within 72 hours
- Support firmware verification at the device (signature check on boot or at install)

### SBOM Management

- Every installed version's SBOM archived in the CMDB
- Weekly automated CVE scan against known vulnerabilities (NIST NVD)
- High/Critical CVEs triggers the patch management workflow (§12)
- All Log4Shell-class supply-chain lessons internalized — if a component is compromised, we can enumerate every affected device within 1 hour

### Firmware Signing Chain

```
Vendor Root CA (offline)
  │
  └── Vendor Intermediate CA
        │
        └── Firmware Release Signing Key
              │
              └── signs firmware image
                    │
                    └── verified at device boot via embedded public key
```

Devices that do not support signed firmware verification at boot (some legacy PLCs) are constrained to Zone 1 or 2 with strict network controls and prioritized for replacement.

### In-House (ADC) Software

- Jetson BMS Python code, Ignition scripts, ML models: all under version control (git)
- Signed commits (GPG) required from all authorized developers
- CI/CD pipeline produces signed release artifacts
- No developer has the ability to push signed artifacts directly to production — release manager (separate person) signs
- Release artifacts verified at install (via dual-person promotion per §6)

---

## §12  PATCH MANAGEMENT

### Patch Sources

| Asset | Source | Typical cadence |
|-------|--------|-----------------|
| PLC firmware (Siemens, Cat, SEL) | Vendor portals + signed release | Quarterly, or CVE-triggered |
| Jetson Orin OS | NVIDIA JetPack + Ubuntu security repo | Monthly |
| Ignition SCADA | Inductive Automation portal | 6–12 months |
| HMI (VisuNet, Beijer) | Vendor portal | Quarterly |
| Switches (Hirschmann, Cisco) | Vendor portal | Quarterly |
| SIS logic solver | Vendor portal; requires FSA-5 after patch | Annually or critical-only |
| VESDA / Novec panel | Vendor portal | Annually |

### Patch Classification

| Class | SLA | Example |
|-------|-----|---------|
| **Critical** (CVE ≥ 9.0, actively exploited) | Within 7 days | Log4Shell-type |
| **High** (CVE 7.0–8.9) | Within 30 days | Remote code execution, not yet exploited |
| **Medium** (CVE 4.0–6.9) | Next maintenance window (≤ 90 days) | DoS, local privilege escalation |
| **Low** (CVE < 4.0 or informational) | Annual review | Hardening, deprecations |

### Patch Workflow

1. Vulnerability observed in CVE monitoring or vendor notification
2. Impact assessment: does this affect our deployment? which zones?
3. Vendor patch available? (if no — compensating controls applied, risk accepted until patch)
4. Patch tested in ADC lab environment (identical configuration)
5. Patch staged to Zone 3.5 via USB air-gap (per §6)
6. Patch applied during approved maintenance window with dual-person oversight
7. Post-patch verification: system function, SIS integrity, no regressions
8. If Zone 0 (SIS) patch: trigger FSA-5 per SIS-001 §16

### Anti-Patterns Explicitly Avoided

- ❌ Automatic internet patch downloads to OT devices (supply chain risk, network dependency)
- ❌ Vendor direct-push updates (uncontrolled cadence, no testing)
- ❌ Skipping testing "because it's a minor version"
- ❌ Patching during live production without rollback plan

---

## §13  MONITORING, LOGGING & SIEM INTEGRATION

### Logging Sources

| Zone | Source | Events logged |
|------|--------|---------------|
| 2 | PLC event logs | Mode changes, setpoint writes, login attempts, errors |
| 2 | Cassette BMS | All HTTP/OPC UA requests, tag writes, failover events |
| 3 | Ignition Gateway | Authentication, authorization, alarm events, scripting errors |
| 3 | Network switches | Port state, MAC changes, SNMP traps |
| 3 | Industrial firewall | ACL denies, intrusion events, DPI alerts |
| 3.5 | Jump server / PAM | Login, session start/end, commands executed |
| 3, 3.5 | OT discovery tool (Claroty/Nozomi/Dragos) | Network anomalies, new devices, protocol anomalies |

### SIEM

- Platform: **Splunk** (if customer has), **Microsoft Sentinel**, or **Elastic Security**; open-source alternative **Wazuh + ELK**
- Deployment: cloud (Zone 4) with forwarders in Zone 3
- Log transport: TLS syslog or dedicated forwarder (data diode compatible)

### Alert Classes

| Class | Example | Response time |
|-------|---------|---------------|
| Critical | SIS event, unauthorized PLC write, anomalous protocol traffic | Immediate (on-call page) |
| High | Failed authentication > 5 in 10 min, new device on OT network, firmware anomaly | < 15 min |
| Medium | Patch-lag alert, cert expiring in 30 days, account lockout | Same business day |
| Low | Informational, audit | Next business day |

### OT-Specific Detection Rules

- Unauthorized Modbus function codes attempted
- Unusual tag write patterns (rapid-fire writes, writes outside operator hours, writes from non-HMI source)
- OPC UA session from non-whitelisted client
- ICMP from outside OT zones
- DNS queries from OT hosts (should be zero; OT hosts use static IPs)
- File execution on HMI (AppLocker denies)
- USB device insertion (Zone 2 or 3 — should be zero in normal operation)

### Forensic Readiness

- Historian + SIS event log + network PCAPs preserved for minimum 90 days
- Network PCAP capture at Zone 2↔3 firewall (rolling 30 days)
- Forensic snapshot capability: Jetson, Ignition, PLC config exports triggered automatically on any critical alert
- Tamper-evident log signing (each log batch cryptographically hashed with previous batch; Merkle-style)

---

## §14  INCIDENT RESPONSE PLAYBOOK

### Principles

1. **Safety first** — if an incident creates safety concern, SIS handles it; security response is secondary to safety
2. **Contain before investigate** — isolate the affected zone before deep analysis
3. **Preserve evidence** — images and logs captured before cleanup
4. **Communicate** — customer, ADC leadership, potentially regulators informed per SLA
5. **Learn** — every incident produces an After-Action Report and updates to this document

### Playbook — Suspected Compromise

| Phase | Timing | Actions |
|-------|--------|---------|
| Identify | T+0 to T+15 min | Alert received; on-call responder acknowledges; preliminary triage: is this safety-affecting? |
| Contain | T+15 min to T+2 hr | Isolate affected network segment; disable accounts if credential compromise suspected; verify SIS still armed |
| Eradicate | T+2 hr to T+24 hr | Forensic analysis; root cause; if confirmed breach, reimage affected systems from known-good images |
| Recover | T+24 hr to T+72 hr | Controlled restart via COLD_START per MODES-001; extensive validation before returning to NORMAL |
| Lessons | T+72 hr to T+30 days | After-Action Report; controls updated; threat intel shared with industry |

### Key Contacts

- **Site supervisor** (customer-side) — first to know, confirms safety
- **ADC NOC on-call** — triages OT alerts
- **ADC Security lead** — escalation for confirmed incidents
- **Customer OT security team** — notification per customer contract
- **CISA or sector ISAC** (e.g., ONG-ISAC for oil & gas) — voluntary threat intel sharing

### Safety-First Fallback

If at any point during a security incident there is uncertainty about SIS integrity, the response is to:
1. Manual EMERGENCY_SHUTDOWN of the entire unit
2. Do not re-energize until root cause is understood and SIS integrity verified
3. Document the shutdown reason as "Security precaution pending SIS verification"

This may cost production hours but never compromises personnel safety.

---

## §15  PHYSICAL SECURITY

### Site Enclosure

- Deployment unit perimeter fenced (customer-provided, typical oilfield security fence)
- Gate with either keycard or padlock — access logged
- Cassette itself is a sealed, tamper-evident unit (no field access after factory commissioning per design intent)
- ECP covers have reed switches — opening triggers intrusion alarm
- Genset enclosures: keyed access only; alarm on open during non-maintenance

### Cabinet Security

- SIS cabinet: separate lock from BPCS; different key / code; only SIS_Authorized personnel
- BPCS control cabinet: locked; keyed alike with other operations-critical cabinets
- Switchgear: arc-flash-rated physical barrier; locked during operation
- Network cabinets: locked; tamper sensors

### USB / Portable Media

- USB ports in Zones 2–3 either physically plugged (polymer USB blockers, DataLocker port blockers) or disabled in BIOS/firmware
- Authorized USB only: encrypted, write-protected, logged
- No personal devices plugged into OT network equipment

### Environmental

- Surveillance cameras at access points (customer-provided typical)
- Motion detection in unattended skid areas (feeds to site security)
- Door position status in BMS as informational (non-safety) input

---

## §16  VENDOR / THIRD-PARTY ACCESS

### Principles

- No "always-on" vendor remote access
- No shared credentials — one vendor account per engagement, created and destroyed per-session
- All vendor sessions: MFA + PAM (see §8) + recorded
- Vendor site visits: escorted, logged, no unattended access to cabinets

### Approved Vendor Access Scenarios

| Vendor | Typical access | Security measure |
|--------|---------------|------------------|
| Cat (genset) | On-site technician, occasional remote diagnostic | Escorted; PAM session for remote |
| Siemens (PLC) | On-site commissioning, remote support rare | Escorted; PAM session for remote |
| Inductive Automation (Ignition) | Remote support tickets | PAM session, time-limited |
| GRC / CoolIT (cooling) | Commissioning + annual PM | Escorted site access |
| MSA / Dräger (gas detection) | Calibration every 6 months | Escorted; SIS Authorized key for access |

### Vendor Agreement Requirements (ADC to require before integration)

- IEC 62443-4-1 certification or equivalent evidence of secure development
- Vulnerability disclosure policy + 72-hour security advisory commitment
- SBOM delivery
- Signed firmware capability
- Support for our certificate-based device authentication (preferred) or strong fallback

Vendors that do not meet these requirements are constrained to Zone 1 with strict compensating controls and prioritized for eventual replacement.

---

## §17  TESTING & ASSURANCE

### Pre-Deployment Testing

| Test | Scope | Frequency | Conducted by |
|------|-------|-----------|--------------|
| Factory Acceptance Test (FAT) — cybersecurity | Configuration review, hardening check, basic pen test | Before shipping | ADC + integrator |
| Site Acceptance Test (SAT) — cybersecurity | Network topology verification, firewall rules, PAM setup | Before going live | ADC + customer |
| Penetration test — external | Internet-facing, cloud (Zone 4) | Annual | Third-party firm (ideally certified OT pen tester: Dragos, Claroty, etc.) |
| Penetration test — internal | Simulate insider / compromised workstation | Annual | Third-party firm |
| Tabletop exercise — incident response | Scenario-based IR practice | Annual | Customer + ADC + ideally regulator observer |
| Red team exercise | Full-scope simulated APT | Every 2–3 years | Third-party with OT expertise |

### Vulnerability Management

- Automated vulnerability scanning in Zone 4 + Zone 3.5 (Tenable, Rapid7, Qualys)
- **Zone 2 scanning is passive only** — active probes can crash legacy PLCs. Use Claroty/Nozomi/Dragos passive monitoring.
- Results tracked to closure with SLA per patch classification (§12)

### Continuous Compliance

- Quarterly internal audit against this document
- Annual third-party audit against IEC 62443-3-3 for Zone 2 SL-3
- Customer-specific audits per contract (API 1164 for pipeline customers, TSA SD-02 for regulated pipelines)

---

## §18  COMPLIANCE MAPPING

### IEC 62443-3-3 Control Mapping (Zone 2 SL-3)

| FR | Control | Implementation reference |
|----|---------|--------------------------|
| SR 1.1 | Human user identification and authentication | §8 Identity, §9 PKI |
| SR 1.2 | Software process and device identification and authentication | §9 PKI (per-device certs) |
| SR 1.3 | Account management | §8 PAM + enterprise AD |
| SR 1.4 | Identifier management | §8 MFA, §9 cert management |
| SR 1.5 | Authenticator management | §10 key management |
| SR 1.7 | Strength of password-based authentication | §8 (MFA required; no password-only) |
| SR 1.11 | Unsuccessful login attempts | §8 lockout policy; §13 SIEM alert |
| SR 1.12 | System use notification | HMI banner (to be added at integration) |
| SR 2.1 | Authorization enforcement | §8 RBAC, TAGS-001 §9 |
| SR 2.2 | Wireless use control | §5 wireless prohibited |
| SR 2.4 | Mobile code | §7 application whitelisting |
| SR 2.8 | Auditable events | §13 SIEM scope |
| SR 2.9 | Audit storage capacity | §13 rolling 90 days + SIEM long-term |
| SR 2.10 | Response to audit processing failures | §14 incident response |
| SR 3.1 | Communication integrity | §10 TLS, signed firmware §11 |
| SR 3.2 | Malicious code protection | §7 whitelisting, §11 signed updates |
| SR 3.3 | Security functionality verification | §17 pre-deployment + annual |
| SR 3.4 | Software and information integrity | §11 SBOM, signed artifacts |
| SR 3.8 | Session integrity | §10 TLS; OPC UA secure channel |
| SR 4.1 | Information confidentiality | §10 encryption in transit + at rest |
| SR 4.2 | Information persistence | §13 logs 90+ days, §17 forensics |
| SR 4.3 | Use of cryptography | §10 algorithm policy |
| SR 5.1 | Network segmentation | §5 three physical networks, firewalls |
| SR 5.2 | Zone boundary protection | §3 zones, §6 data diode |
| SR 5.3 | General purpose person-to-person communication restrictions | §5 (no chat, email, etc. on OT) |
| SR 6.1 | Audit log accessibility | §13 SIEM |
| SR 6.2 | Continuous monitoring | §13 SIEM + OT discovery |
| SR 7.1 | Denial of service protection | §5 rate limiting, firewall |
| SR 7.3 | Control system backup | §11 config backup, encrypted |
| SR 7.4 | Control system recovery and reconstitution | §14 recovery phase |
| SR 7.6 | Network and security configuration settings | §7 hardening baselines |
| SR 7.8 | Control system component inventory | §7 CMDB |

### NIST CSF 2.0 Function Mapping

| Function | This document |
|----------|---------------|
| **Govern (GV)** | §1 Scope, §18 Compliance, ADC security program (separate doc) |
| **Identify (ID)** | §2 Threat model, §7 Asset inventory |
| **Protect (PR)** | §5 Segmentation, §6 Diode, §7 Hardening, §8 IAM, §9 PKI, §10 Crypto, §11 Supply chain, §12 Patching, §15 Physical |
| **Detect (DE)** | §13 Monitoring, SIEM, OT discovery |
| **Respond (RS)** | §14 Incident response |
| **Recover (RC)** | §14 Recovery phase, §17 testing |

### API 1164 (Pipeline SCADA Security) Alignment

Applicable for deployments at pipeline compressor / pumping stations. Key mapping:
- Account management (§8) — aligns with API 1164 §5
- Logical access control (§5, §8) — §6
- Physical access (§15) — §7
- Incident response (§14) — §8
- Baseline config management (§7) — §9
- System patching (§12) — §10
- Monitoring (§13) — §11

### TSA Security Directive Pipeline-2021-02 Alignment (if applicable)

- Cybersecurity coordinator designated (ADC) — yes
- CISA-reportable incidents within 12 hours — §14 playbook
- Vulnerability assessment — §17 annual pen test
- Security plan — this document + customer-specific addenda

---

## §19  OPEN ITEMS

| ID | Priority | Description | Owner | Notes |
|----|----------|-------------|-------|-------|
| CY-01 | P-0 | Data diode vendor selection — Waterfall vs Owl vs Siemens DiodeX; cost and customer acceptance drivers | ADC procurement | Gates §6 |
| CY-02 | P-0 | SIEM platform selection — customer has existing Splunk? Azure Sentinel? Own deployment? | ADC ↔ customer | Affects §13 |
| CY-03 | P-0 | OT discovery tool selection — Claroty vs Nozomi vs Dragos; customer preference and cost | ADC ↔ customer | Affects §7, §13 |
| CY-04 | P-0 | PKI root CA — ADC-operated or customer's existing internal CA? | ADC ↔ customer | Gates §9 |
| CY-05 | P-1 | HSM selection — SafeNet Luna vs AWS CloudHSM vs YubiHSM | ADC engineering | Gates §10 key management |
| CY-06 | P-1 | PAM solution — CyberArk (enterprise price), BeyondTrust, HashiCorp Vault (open source) | ADC engineering | Gates §8 |
| CY-07 | P-1 | Initial ADC cybersecurity team staffing — security lead, SOC staffing model, on-call rotation | ADC HR | Gates §14 |
| CY-08 | P-1 | Vendor assessment program — formal IEC 62443-4-1 assessment of each software supplier | ADC procurement | Affects §11, §16 |
| CY-09 | P-2 | Jump server / bastion architecture in Zone 3.5 — Teleport, AWS SSM, home-grown | ADC engineering | Gates §6 |
| CY-10 | P-2 | Post-quantum cryptography migration plan — schedule vendor readiness review annually | ADC engineering | Future-proofing |
| CY-11 | P-2 | Incident response retainer — DFIR firm for surge capacity (Mandiant, CrowdStrike, Dragos) | ADC procurement | Affects §14 |
| CY-12 | P-2 | Bug bounty program scope — should production deployments be in scope? | ADC | Affects §17 |
| CY-13 | P-3 | Deception technology (honeypots in OT zones) — additional detection value vs complexity | ADC engineering | Optional enhancement |
| CY-14 | P-3 | IEC 62443-4-2 certification for ADC in-house components (Jetson BMS, custom Ignition modules) | ADC engineering | Competitive advantage |

---

## SUMMARY OF KEY DESIGN DECISIONS

| # | Decision | Rationale |
|---|----------|-----------|
| 1 | IEC 62443 framework | Industry-standard for IACS; required by most oil & gas majors; maps cleanly to NIST CSF |
| 2 | Hardware data diode at OT/IT boundary | Eliminates entire class of remote attack vectors; required for SL-3 target |
| 3 | SL-3 target for Zone 2 (basic control) | Threat model (nation-state + sophisticated criminal) justifies; lower levels leave material risk |
| 4 | Zero shared credentials, per-device certs | Limits blast radius; eliminates one of the top ICS attack patterns |
| 5 | MFA required for all privileged access, hardware token preferred | Password + SMS insufficient given SIM-swap reality |
| 6 | No internet-based patch downloads to OT | Supply-chain and availability risk; manual air-gapped process mandatory |
| 7 | Passive OT discovery only (no active scanning of Zone 2) | Active scans crash legacy PLCs; unacceptable risk for forensic gain |
| 8 | SIS independence preserved (read-only exposure to BPCS) | IEC 61511 compliance; cybersecurity does not compromise safety |
| 9 | Safety-first fallback — shut down if SIS uncertainty | Better to lose hours of production than risk personnel |
| 10 | Customer-audit-ready by default | Sales enablement for oil & gas majors (Shell, Chevron, BP all audit OT security) |

---

**Cassette-CYBER-001 — Cybersecurity Architecture · Rev 1.1 · 2026-04-20**
**Scott Tomsu · scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana**
**CONFIDENTIAL**
