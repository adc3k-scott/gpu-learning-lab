# Cassette-CYBER-001 — Cassette Cybersecurity Specification — Rev 1.2

**Document ID:** Cassette-CYBER-001
**Revision:** 1.2
**Date:** 2026-04-22
**Classification:** CONFIDENTIAL
**Supersedes:** Rev 1.1 (deleted) — full clean rebuild
**Companion documents:** Cassette-CTRL-001 · Cassette-ELEC-001 · Cassette-INT-001 · Cassette-BOM-001
**Prepared by:** Scott Tomsu · CEO / Chief Engineer · scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana

---

## Revision log

| Rev | Date | Author | Summary |
|---|---|---|---|
| 1.0 | 2026-01-xx | Scott Tomsu | First issue. General posture outline, no concrete controls. |
| 1.1 | 2026-02-xx | Scott Tomsu | Withdrawn and deleted — architecture drift vs emerging CTRL-001. |
| **1.2** | **2026-04-22** | **Scott Tomsu** | **Full rebuild against CTRL-001 Rev 1.2. IEC 62443-3-3 / -4-2 SL 2 target. Closes CTRL-001 CL-07. OS hardening baseline locked (Ubuntu 22.04 / JetPack 6.x). OPC-UA PKI hierarchy locked — platform NOC is root CA, Cassette holds device certificate. SSH key-only from maintenance VLAN. USB kernel-disabled except attended maintenance. VLAN scheme formalized for all six VLANs named in CTRL-001 §4.5. Firewall default-deny with explicit allow per CTRL-001 §4.6 six protocol interfaces. Break-glass procedure defined through physical ECP access, not a network backdoor. Modbus TCP isolation-based posture documented as SL 2 accepted control.** |

---

## 1. Scope

This document specifies the cybersecurity posture for a single Cassette — the embedded control intelligence (BMS), its network interfaces, its operating system, its users, its secrets, and its update path. The target security level is **IEC 62443 SL 2** (protection against intentional violation using simple means, with low resources and generic skills), appropriate for a behind-the-fence AI factory component.

This document closes CTRL-001 open item CL-07.

**In scope:**

- OS hardening baseline for the Jetson AGX Orin (Ubuntu 22.04 / JetPack 6.x)
- Network segmentation and firewall ruleset (six VLANs, six protocol interfaces)
- Authentication and identity (local accounts, SSH, OPC-UA users, HMI access, break-glass)
- PKI / certificate management for OPC-UA
- OTA update signing chain and rollback validation
- Physical security of the ECP panel, serial console, USB, and removable media
- Secrets management (where keys, certs, and tokens live on the Jetson)
- Audit logging and monitoring at the Cassette
- Vulnerability management (patch cadence, CVE triage)
- Incident response within Cassette scope
- Commissioning security checklist (the F-14 hook referenced in CTRL-001 §10.1)

**Out of scope:**

- Platform NOC security posture (separate platform document)
- NVIDIA rack firmware security (GPU node BMC, BIOS, firmware — vendor-owned)
- InfiniBand fabric management security (separate network ops scope)
- Tenant workload security, tenant data isolation, tenant key management
- Cassette physical security beyond the ECP panel (site perimeter, parish AHJ, guard posture — facility-level scope)
- Offshore/marine hazardous-area cybersecurity variance (offshore variant adds IECEx/ATEX enclosure requirements but no different cyber posture; noted only in §9)
- Privacy / regulatory compliance framings (GDPR, CCPA) — Cassette holds no personal data

---

## 2. Threat model

One page by intent. This gives context for the controls that follow; it is not a substitute for a full risk assessment (CY-11).

### 2.1 Physical threats

- **Unauthorized ECP panel access** — opening the Cassette door and then the ECP panel to reach the Jetson, serial console, or USB ports. Compensating control: locked outer door + locked ECP panel, physical tamper evidence, audit log review (§9, §11).
- **Removable media insertion** — USB stick or SD card inserted into the Jetson to deliver malware or exfiltrate logs. Compensating control: kernel-level USB disable except during attended maintenance (§9.3).
- **Cable-cut / replacement on BMS network switch uplinks** — physical network tampering. Compensating control: tamper-evident enclosure, SNMP link-state alerting at platform NOC (§11).
- **Watchdog / safety circuit bypass** — jumpering the hardware watchdog safe-state relay to prevent fail-safe actuation. Explicitly out of the threat model for SL 2 — would require insider access and is a physical-integrity concern, not a cyber one. Noted as risk to operations, addressed by physical lock + audit.

### 2.2 Network threats

- **Lateral movement from Platform-IT into Cassette-OT** — an attacker who compromises a platform workstation or tenant tier attempts to reach Cassette subsystems. Compensating control: zone-and-conduit enforcement at the BMS network switch with default-deny firewall (§3, §5).
- **Eavesdropping on CDU skid Modbus traffic** — Modbus TCP is unauthenticated and unencrypted. Compensating control: VLAN confinement — the CDU VLAN is not reachable from Platform-IT or maintenance VLANs (§5.2). See §5.4 for explicit accept-and-document posture.
- **OPC-UA credential theft / replay** — capture and reuse of OPC-UA session credentials. Compensating control: Basic256Sha256 signing + encryption, per-user certificates, short-lived session tokens (§7).
- **SSH brute force or credential stuffing** — remote login attempts against the BMS. Compensating control: key-only auth, maintenance VLAN only, no password auth anywhere (§6.2).

### 2.3 Supply-chain threats

- **Compromised OTA artifact** — malicious update delivered through the platform release channel. Compensating control: signed OCI artifacts, signature verification before install, rollback on repeated failure (§8).
- **Compromised JetPack / Ubuntu package** — upstream package with CVE or trojan. Compensating control: package pinning, CVE triage, attended-only OS updates (§8, §12).
- **Compromised BOM component with embedded firmware** (e.g., managed switch, TraceTek controller) — pre-installed malware on a shipped component. Compensating control: factory acceptance test against a known configuration; flagged as residual risk for SL 2 (higher SLs would require supplier audit).

### 2.4 What SL 2 does not cover

SL 2 does not defend against a skilled, resourced, targeted adversary (SL 3) or a nation-state adversary (SL 4). Those targets would require HSM-backed keys, attested boot, signed firmware from silicon on up, continuous deception and monitoring, and an operational security program at the facility that is out of Cassette scope. If the platform operator later raises the target SL, this document must be reissued.

---

## 3. Security architecture overview — IEC 62443 zones and conduits

### 3.1 Zone definition

The Cassette spans three security zones plus two external zones it connects to. Boundaries are enforced at the BMS network switch (ACLs) and at the Jetson (firewall), with physical boundaries where named.

| Zone | Location | Assets | Target SL |
|---|---|---|---|
| **Cassette-Safety** | Physically wired, no network | Hardware watchdog, MIV actuators, fire panel DI/DO, E-stop hardwired path, sump floats, TraceTek controller output contacts | SL 2 — physical only |
| **Cassette-OT** | VLAN: CDU, safety, BMC | CDU skid PLC, NVIDIA rack BMCs, BMS I/O scanner, IPMI/Redfish and Modbus clients | SL 2 |
| **Cassette-mgmt** | VLAN: platform-mgmt, IB-mgmt | OPC-UA server on Jetson, SNMP managers, InfiniBand switch mgmt, local HMI server | SL 2 |
| **Platform-IT** | External | Platform NOC / SCADA, historian, OTA release channel, platform PKI | Platform-owned |
| **CDU-OT** | External (physical adjacency) | CDU skid PLC and CDU skid local instrumentation | SL 2 (shared posture with this doc) |

### 3.2 Zone and conduit diagram

```
     ┌─────────────────────────────────────────────────────────────────┐
     │                        Platform-IT zone                          │
     │   Platform NOC / SCADA · Historian · PKI root · OTA channel      │
     └─────────────────────────┬───────────────────────────────────────┘
                               │
                    Conduit P1 │ (OPC-UA Basic256Sha256, OTA pull HTTPS)
                               │ (SSH from maint jumphost on maint VLAN)
     ═════════════════════════ ▼ ═══════ Cassette perimeter ═══════════
                               │
                  ┌────────────┴────────────┐
                  │   BMS network switch    │  ◄── all Cassette traffic
                  │   (managed L2/L3, ACLs) │      passes through here
                  └──┬───┬───┬───┬───┬──────┘
                     │   │   │   │   │
         ┌───────────┘   │   │   │   └───────────┐
         │               │   │   │               │
     ┌───▼──────┐   ┌────▼─┐ │ ┌─▼────────┐  ┌───▼──────────┐
     │ Cassette │   │ Cass │ │ │  Cass    │  │ Cassette-    │
     │   -mgmt  │   │ -OT  │ │ │  -OT     │  │ Safety       │
     │          │   │      │ │ │          │  │              │
     │ OPC-UA   │   │Modbus│ │ │IPMI/Red  │  │ (PHYSICAL —  │
     │ server   │   │ CDU  │ │ │ NVIDIA   │  │  no network) │
     │ HMI      │   │ skid │ │ │ BMCs     │  │ Watchdog,    │
     │ SNMP mgr │   │ PLC  │ │ │ (10x)    │  │ MIV, fire,   │
     │          │   │      │ │ │          │  │ E-stop DI/DO │
     └──────────┘   └──────┘ │ └──────────┘  └──────────────┘
                             │
                  Conduit C2 │ (Modbus TCP, VLAN-confined)
                             │
                        ┌────▼──────┐
                        │  CDU-OT   │   (physically adjacent skid)
                        │  skid PLC │
                        └───────────┘
```

### 3.3 Conduit inventory

| Conduit | From zone | To zone | Protocols | Controls | Justification |
|---|---|---|---|---|---|
| P1 | Platform-IT | Cassette-mgmt | OPC-UA (4840), HTTPS (443, OTA pull), SSH (22) from maint jumphost only | Basic256Sha256 + cert + user auth; TLS 1.2+; SSH key-only | Normal command/control, historian, updates |
| C2 | Cassette-OT | CDU-OT | Modbus TCP (502) | VLAN confinement only (no protocol crypto); bidirectional heartbeat; hardwired fallback safe-state per CTRL-001 §8.4 | Skid telemetry and setpoint (see §5.4 accept posture) |
| C3 | Cassette-mgmt | Cassette-OT | IPMI (UDP 623), Redfish (HTTPS 443), SNMPv3 (UDP 161) | Read-only from BMS; SNMPv3 AuthPriv; Redfish TLS + per-BMC credential | Telemetry from racks and switches; no control authority |
| C4 | Cassette-mgmt | Platform-IT | OPC-UA (4840 outbound session), HTTPS (OTA pull 443) | BMS initiates; mTLS; no inbound ports open | BMS-to-NOC publishing and update pull |
| C5 | Cassette-Safety | — | Hardwired only (DI/DO) | Physical isolation | Fire panel handshake, E-stop, watchdog — no network |

Conduits not in this table are not permitted. Any protocol traffic outside this inventory is dropped by the firewall (§5.3).

---

## 4. OS hardening — Jetson AGX Orin (Ubuntu 22.04 / JetPack 6.x)

### 4.1 Base image

- JetPack 6.x on Ubuntu 22.04 LTS. Factory image pulled from NVIDIA Developer portal, SHA-256 verified against NVIDIA's published digest before first flash.
- Single canonical "gold image" built per JetPack release, signed by the platform build team, and used for all Cassette first-flash deployments. Deviation from the gold image during first flash invalidates commissioning.

### 4.2 Services and packages

| Item | Setting | Rationale |
|---|---|---|
| Unused services | Disabled and masked: `cups`, `avahi-daemon`, `bluetooth`, `ModemManager`, `snapd` | Reduce attack surface |
| Unused kernel modules | Blacklisted: `bluetooth`, `firewire-*`, `cramfs`, `freevxfs`, `jffs2`, `hfs`, `hfsplus`, `squashfs`, `udf` (only those not needed) | Reduce kernel surface |
| SSH server (`sshd`) | Installed, enabled, listening on maintenance VLAN interface only (§5), key-only, root login disabled | Operational + break-glass |
| Package manager | `apt` with pinned distribution; upstream repo list restricted to Ubuntu 22.04 main/security + NVIDIA L4T | Controlled source set |
| Automatic updates | `unattended-upgrades` installed, **disabled for kernel and JetPack**, enabled for security patches in userspace only, applied during maintenance windows (§12) | Attended-only OS posture |
| Timezone / time sync | UTC; PTP (IEEE 1588) primary, NTP fallback to platform NTP only | Logging integrity |
| Kernel parameters | `kernel.kptr_restrict=2`, `kernel.dmesg_restrict=1`, `net.ipv4.conf.all.rp_filter=1`, `net.ipv4.conf.all.accept_redirects=0`, `net.ipv6.conf.all.disable_ipv6=1` (IPv6 not used) | Reduce info leak + spoof attack |
| AppArmor | Enforced; profile set for `adc-bms`, `sshd`, `snmpd` (if used) | Mandatory access control |
| Auditd | Enabled with ruleset covering: execve, connect, open on `/etc`, privilege changes, sudo invocations | Audit trail for §11 |

### 4.3 Filesystem layout

- `/` on 256 GB eMMC (boot + recovery). Ext4, mounted with `nodev,nosuid` where applicable on non-system mounts.
- `/var/bms`, `/var/log/bms` on 1 TB NVMe (application + logs). Ext4.
- `/tmp` tmpfs, `nodev,nosuid,noexec`.
- No swap file (Jetson has enough RAM; swap risks key material reaching disk).
- `/boot` read-only during normal operation; re-mounted read-write only during attended OS update.

### 4.4 User accounts on the Jetson

| Account | Purpose | Login method | Notes |
|---|---|---|---|
| `root` | System | Disabled for login (no password, no SSH) | Only via `sudo` from operator account |
| `bms` | Service account running `adc-bms` | No shell login (`/usr/sbin/nologin`) | Owns `/var/bms` and `/var/log/bms` |
| `operator` | Platform / field engineer account | SSH key from maintenance jumphost; `sudo` with per-command rules | Only human account |
| `hmiview` | Local HMI web session | No OS login; credential via HMI auth only | Bound to HMI scope, not OS |

Every other default Ubuntu account (`ubuntu`, `nvidia`, `guest`) is removed during gold-image build. Verified at commissioning §14.

### 4.5 Boot posture

- JetPack 6.x Secure Boot: enabled. BL (bootloader) signed by NVIDIA fuse-programmed key chain where supported; application bootloader signed by the platform build key.
- Measured-boot posture left at NVIDIA JetPack default; extension to full attested boot with remote attestation is **CY-01** (open, SL 3 feature).
- No external boot (USB/SD) allowed — `bootargs` locked in signed bootloader config; physical USB disabled at kernel (§9.3).

---

## 5. Network segmentation

### 5.1 VLAN scheme

Six VLANs, all terminated at the BMS network switch. VLAN IDs are assigned by platform networking; the numbers below are placeholders for the structure.

| VLAN name | Purpose | Members |
|---|---|---|
| **platform-mgmt** | Cassette-to-platform OPC-UA, OTA, SSH-jumphost traffic | Jetson mgmt NIC, BMS switch uplink to platform |
| **CDU** | Cassette-to-CDU-skid Modbus TCP | Jetson CDU NIC (logical via VLAN tag on mgmt port), CDU skid PLC port |
| **BMC** | NVIDIA rack BMC IPMI / Redfish traffic | Jetson BMC NIC, 10 × rack BMC ports |
| **IB-mgmt** | QM9700 InfiniBand switch SNMP mgmt (not IB data plane) | Jetson BMC NIC (shared VLAN policy), QM9700 mgmt ports |
| **safety** | TraceTek TT-SIM-2 Modbus TCP gateway (sensor telemetry only — actuation is hardwired) | Jetson safety NIC, TT-SIM-2 IP interface |
| **maintenance** | Attended-only SSH from platform jumphost, HMI privileged session | Jetson maintenance NIC, HMI WAP (if enabled under attended maintenance) |

VLANs do not route between each other except through the Jetson firewall (§5.3). The BMS network switch enforces VLAN isolation in hardware; no inter-VLAN routing on the switch itself.

### 5.2 Switch ACL rules (BMS network switch)

| Rule | Source VLAN | Destination VLAN | Action | Purpose |
|---|---|---|---|---|
| ACL-01 | Any | Any other VLAN | Deny (default) | Default isolation |
| ACL-02 | platform-mgmt | Jetson mgmt IP only | Permit | Uplink from platform |
| ACL-03 | CDU | Jetson CDU IP + CDU skid PLC IP only | Permit | Modbus conduit C2 |
| ACL-04 | BMC | Jetson BMC IP + 10 rack BMC IPs + QM9700 mgmt IPs | Permit | IPMI/Redfish/SNMP conduit C3 |
| ACL-05 | IB-mgmt | folds into BMC scope (same ACL set) | Permit | SNMPv3 to QM9700 |
| ACL-06 | safety | Jetson safety IP + TT-SIM-2 IP only | Permit | TraceTek Modbus read |
| ACL-07 | maintenance | Jetson maintenance IP only | Permit | Attended SSH / HMI |
| ACL-08 | Any | Any broadcast or multicast address outside local VLAN | Deny | No inter-VLAN broadcast |

### 5.3 Host firewall on the Jetson (`nftables`, default-deny)

The firewall is the last enforcement point after VLAN ACLs. Two layers are used because a misconfigured switch must not be the only control.

| Rule | Source | Dest | Protocol / Port | Direction | Action | Justification |
|---|---|---|---|---|---|---|
| F-01 | Any | Any | any | any | DROP (default) | Default-deny |
| F-02 | Jetson | Platform NOC OPC-UA endpoint | TCP 4840 | OUT | ALLOW | OPC-UA publish (CTRL-001 §4.2) |
| F-03 | Platform NOC | Jetson OPC-UA listener | TCP 4840 | IN | ALLOW (mTLS) | OPC-UA command subscribe |
| F-04 | Jetson | Platform OTA endpoint | TCP 443 | OUT | ALLOW | OTA artifact pull (§8) |
| F-05 | Jetson | CDU skid PLC IP | TCP 502 | OUT | ALLOW | Modbus master (CTRL-001 §8) |
| F-06 | CDU skid PLC | Jetson | TCP 502 | IN | DROP | BMS is master only; no inbound Modbus |
| F-07 | Jetson | Each rack BMC IP | UDP 623 | OUT | ALLOW | IPMI poll |
| F-08 | Jetson | Each rack BMC IP | TCP 443 | OUT | ALLOW | Redfish poll |
| F-09 | Jetson | QM9700 + BMS-switch mgmt IPs | UDP 161 | OUT | ALLOW | SNMPv3 poll |
| F-10 | QM9700 / BMS-switch | Jetson | UDP 162 | IN | ALLOW | SNMP traps |
| F-11 | Jetson | TT-SIM-2 | TCP 502 | OUT | ALLOW | TraceTek telemetry |
| F-12 | Maintenance jumphost IP | Jetson | TCP 22 | IN | ALLOW (key auth only) | Attended SSH |
| F-13 | Jetson loopback | Jetson loopback | TCP 8080 | any | ALLOW | Local HMI server |
| F-14 | Jetson | Platform PTP / NTP | UDP 123 / 319–320 | OUT | ALLOW | Time sync |
| F-15 | Any | Any | ICMP echo | IN / OUT | ALLOW, rate-limited | Operational diag |

Every rule is logged on accept and drop (§11).

### 5.4 Modbus TCP — accepted posture at SL 2

Modbus TCP has no native authentication or encryption. This is a well-known protocol limitation, not a gap in this specification. At SL 2, the compensating control is **network isolation** — the CDU VLAN is reachable only from the Jetson CDU interface and the CDU skid PLC itself, with strict switch ACLs and host firewall rules (§5.2, §5.3). There is no path from Platform-IT, the maintenance VLAN, or any other VLAN into the CDU VLAN.

Additional operational controls that reduce the residual risk:

- Bidirectional heartbeat between BMS and skid PLC (CTRL-001 §8.4); either side failing to hear the other drops into its own safe-state
- Hardwired safe-state dry contact between BMS watchdog and CDU skid PLC (CTRL-001 §6.3, §8.4) — physical fallback if Modbus comms are compromised or lost
- Setpoint range enforcement at the BMS (CTRL-001 §8.5): out-of-range setpoint writes are rejected and logged regardless of Modbus packet content

**Out of scope at SL 2:**

- Adding a Modbus-to-HTTPS gateway — injects a custom protocol wrapper, non-standard, creates a new attack surface, not required by IEC 62443 at SL 2, and does not improve the real-world posture given that the meaningful control is VLAN confinement.
- Modbus/TCP Security (the 2018 RFC proposing TLS over Modbus) — vendor support is minimal in industrial PLCs today and the CDU skid PLC does not support it per COOL2-001. Revisit at SL 3 or if the PLC is replaced with a TLS-capable unit.

This posture is the SL 2 decision for this revision and is not open.

---

## 6. Authentication & identity

### 6.1 Principle

No shared accounts. No default passwords. No password-based remote login on any interface. Every human action traceable to a named identity.

### 6.2 SSH

| Setting | Value |
|---|---|
| Listener VLAN | maintenance VLAN only (`ListenAddress` bound to that interface) |
| Port | 22 |
| Auth | Key-only — `PasswordAuthentication no`, `ChallengeResponseAuthentication no`, `KbdInteractiveAuthentication no` |
| Root | `PermitRootLogin no` |
| Allowed users | `AllowUsers operator` (only) |
| Source restriction | `AllowUsers operator@<maintenance jumphost CIDR>` |
| Host keys | Ed25519 + RSA 4096; regenerated on first boot per Cassette (no shared keys across Cassettes) |
| User keys | Ed25519 preferred; each field engineer has a personal key; no shared keys |
| Session logging | `audit`d records all `sshd` auth events + per-command `sudo` invocations |
| Idle timeout | `ClientAliveInterval 300`, `ClientAliveCountMax 2` — 10 min idle max |
| Max auth tries | `MaxAuthTries 3` |

### 6.3 OPC-UA users and sessions

| Item | Value |
|---|---|
| Security policy | Basic256Sha256 — sign + encrypt, mandatory |
| Transport | TCP 4840 (mTLS via device + user certs) |
| Anonymous | Disabled |
| User auth | Per-user X.509 certificate issued by platform CA (§7) |
| User roles | `observer` (read-only subscriptions), `operator` (read + issue setpoint writes within envelope), `platform` (issue E-stop-request, maintenance-isolation, workload-enable overrides) |
| Session token lifetime | 8 h maximum; renewable with re-auth |
| Subscription rate | Server-enforced minimum 500 ms to prevent DoS via aggressive sampling |

Role-to-method mapping:

| OPC-UA method / write | observer | operator | platform |
|---|---|---|---|
| Read tag tree | ✓ | ✓ | ✓ |
| Subscribe to tags | ✓ | ✓ | ✓ |
| Write CDU supply setpoint (via BMS proxy) | — | ✓ (30–45 °C) | ✓ |
| Issue E-stop-request | — | — | ✓ |
| Issue maintenance-isolation | — | — | ✓ |
| Issue safe-state reset | — | ✓ (two-person on platform side) | ✓ |
| Modify alarm thresholds | — | — | ✓ (requires signed config bundle, not a live write) |

### 6.4 Local HMI access

| Item | Value |
|---|---|
| Access point | ECP panel touchscreen only; no remote view in Rev 1.2 |
| Scope | Read + ack; no setpoint authority, no force outputs |
| Auth | PIN + (future) RFID badge per CY-03; Rev 1.2 default is 6-digit PIN with lockout on 5 bad attempts for 15 min |
| Session timeout | 5 min idle |
| Safe-state reset | Requires two-hand confirmation dialog (per CTRL-001 §5.3) **and** an authenticated session |

### 6.5 Break-glass / emergency local access

If OPC-UA is unreachable (platform down) **and** SSH is unreachable (network failed) **and** the local HMI is unresponsive, the following procedure applies. The procedure is **physical**, not a network backdoor.

1. Authorized field engineer (name on the platform operator roster) arrives on-site with photo ID.
2. Unlocks Cassette outer door using site key (issued per platform site-access policy, out of scope here).
3. Unlocks ECP panel using ECP key (separately issued; not the same as the outer door key).
4. Connects a platform-issued maintenance laptop to the Jetson **service port** (1 GbE on the Jetson, physically inside the ECP panel). The service port is on the maintenance VLAN by link, but the Jetson firewall treats this interface no differently than the mgmt VLAN — same SSH key-auth, same `operator` user, same sudo rules.
5. SSH in with the engineer's personal key, authenticate with sudo, perform recovery.
6. Full session auditd log uploads to platform historian as soon as connectivity recovers.
7. Every break-glass event generates a post-event report logged to platform NOC within 24 h.

There is **no** local console login with password. The service port is not a console port — it is a standard SSH endpoint accessible only behind two physical locks. If even SSH on the service port fails, the next step is Jetson replacement from a pre-staged spare (§13) — not bypassing authentication.

---

## 7. Certificate management

### 7.1 PKI structure

The Cassette BMS is **not** its own CA. All certificates used by the Cassette are issued by the platform PKI. This keeps the trust root off the Cassette and centralizes issuance and revocation.

```
Platform Root CA (offline, platform-owned, HSM-backed)
  │
  ├── Platform Device Issuing CA (online, platform-owned)
  │     │
  │     └── Cassette Device Certs (one per Cassette, per service)
  │             · Jetson OPC-UA server cert (CN = cassette-<serial>-opcua)
  │             · Jetson SSH host cert (optional if SSH CA used)
  │             · Jetson OTA client cert (for mTLS OTA pull)
  │
  └── Platform User Issuing CA (online, platform-owned)
        │
        └── User Certs (one per human operator / platform role)
                · OPC-UA user certs (observer / operator / platform role)
                · SSH user keys (enrolled by personal key fingerprint, not cert-signed in Rev 1.2)
```

### 7.2 Device certificate issuance (per Cassette)

1. At gold-image build, the Jetson generates an ECDSA P-256 keypair in software (TPM-backed keyring if available — §10.1) for each of its service certificates.
2. The Jetson produces CSRs for each service (OPC-UA, OTA client, optional SSH host).
3. CSRs are submitted out-of-band (over the platform build network at the factory, not over the production interfaces) to the platform Device Issuing CA.
4. CA signs and returns certificates with the Common Name = `cassette-<serial>-<service>` and a SAN list covering the Jetson's assigned IPs on each VLAN.
5. Certs are installed into `/etc/adc-bms/pki/` (root-owned, `0600` on keys, `0644` on certs).
6. Private keys never leave the Jetson.

### 7.3 Cert lifetimes and rotation

| Cert type | Lifetime | Rotation trigger |
|---|---|---|
| Device OPC-UA | 2 years | 60 days before expiry, auto-renewed via ACME-like protocol against platform CA |
| Device OTA client | 2 years | Same as above |
| SSH host keys | 5 years | Manual rotation during attended maintenance |
| User OPC-UA | 1 year | Per-user, platform-issued |

Auto-renewal requires platform CA to be reachable and the current cert to still be valid. If auto-renewal fails for 7 days before expiry, a WARN is raised at platform NOC; if the cert expires, OPC-UA sessions fail to establish and the Cassette continues in its last command state with local deterministic control (watchdog and safety layer unaffected — those are not network-dependent).

### 7.4 Revocation

- Platform issuing CAs publish CRLs; Jetson polls CRL every 6 h via HTTPS from the platform endpoint.
- OCSP is **not** used in Rev 1.2 — adds an external dependency and latency in a low-cert-count environment; CRL is sufficient at this scale.
- On revocation of a platform's OPC-UA user cert, subsequent sessions from that user are rejected on next handshake (up to 6 h stale window from CRL poll cadence — acceptable at SL 2; platform NOC can trigger immediate CRL re-pull via a signed OPC-UA method if urgency requires).

### 7.5 What happens on expiry

If a device cert expires with no rotation:

- OPC-UA listener refuses new sessions
- Existing OPC-UA session terminates at next keepalive failure
- OTA pull fails
- **Cassette continues operating on last commanded state**; CTRL-001 L1 deterministic control, watchdog, safe-state logic, and MIV commands are all local and unaffected
- Platform NOC sees the Cassette drop off OPC-UA and dispatches a field engineer via break-glass (§6.5) or remote reissuance path

Cert expiry is a connectivity loss event, not a safety event.

---

## 8. OTA update security

### 8.1 Artifact format

- Application updates (the `adc-bms` service) ship as signed OCI container images stored on the platform OTA endpoint.
- OS-level updates (kernel, JetPack) ship as signed package bundles and are **attended-only** (§12).

### 8.2 Signing chain

- Platform build team operates an offline code-signing key (platform Code Signing CA).
- Every OCI image is signed using Sigstore/`cosign`-compatible signatures chained to the platform Code Signing CA.
- The Jetson holds the Code Signing CA root cert pinned in `/etc/adc-bms/pki/codesign-ca.pem`; no other CA is trusted for artifact signatures.

### 8.3 Verification steps before install

On OTA pull:

1. Jetson fetches the OCI image and its signature over mTLS (device OTA client cert, §7.2).
2. Verify artifact SHA-256 matches the manifest's declared digest.
3. Verify signature against pinned Code Signing CA root.
4. Verify artifact metadata version > current version (no downgrade without explicit operator + platform-role override).
5. Verify the artifact declares compatibility with current JetPack / OS version.
6. Stage atomically at `/opt/adc-bms/releases/<version>/`.
7. Swap the `current` symlink atomically and restart `adc-bms` via `systemd`.

If any step fails, the artifact is deleted, a CRITICAL OTA-VERIFY-FAIL alarm is published to NOC, and the currently-running version continues.

### 8.4 Rollback

- Previous version retained at `/opt/adc-bms/releases/<previous>/` until next successful update.
- If the new `adc-bms` crashes 3 times within 5 min after OTA, `systemd` rollback script reverts the symlink, restarts, and publishes an OTA-ROLLBACK alarm.
- Rollback is the only automatic safety valve; beyond rollback, platform NOC dispatches an engineer.

### 8.5 Attended-only OS updates

- Kernel and JetPack updates never auto-install.
- Scheduled during a planned maintenance window with the Cassette **in safe-state**.
- Dual-copy boot partition on eMMC with known-good fallback — if the new partition fails to boot, bootloader selects the previous partition on next power cycle.
- On-site engineer present; full session logged.

### 8.6 What OTA cannot change unattended

- CA root certificates in `/etc/adc-bms/pki/` — changing these is an attended maintenance operation
- Firewall ruleset
- Watchdog configuration (cannot be changed from software at all — §2.1)
- User account list

---

## 9. Physical security

### 9.1 ECP panel access

- Cassette outer door: keyed lock plus tamper-evident seal. Outer key issued per platform site-access policy.
- ECP panel (inside the Cassette): separately keyed. ECP key issued only to named field engineers on the platform operator roster.
- Opening the ECP panel physically interrupts an anti-tamper switch (DI wired to CTRL-001 §3.2 spare channel — **CY-04** captures formal wiring); open triggers a WARN event logged to NOC with timestamp.

### 9.2 Jetson serial console

The Jetson carrier has a UART / serial console header physically exposed on the PCB inside the ECP panel. Policy:

- Header is **not wired out** to any external connector. Access requires the ECP panel to be open.
- Bootloader console output is enabled (for recovery); bootloader **does not** permit arbitrary boot commands without a signed bootloader config (§4.5).
- OS console login on the serial line is **disabled** (`getty` on the serial TTY removed from `systemd`).
- Even with physical serial access, there is no password-based console login path — the operator must bring a laptop and SSH over the service port (§6.5).

### 9.3 USB port policy

- USB ports on the Jetson carrier are **disabled at the kernel level** in the gold image:
  - `/etc/modprobe.d/blacklist-usb-storage.conf` blacklists `usb-storage`, `uas`, `usbhid` is retained only for the HMI touchscreen if USB-connected; otherwise all USB is blacklisted
  - Kernel build parameter: `modprobe.blacklist=usb_storage,uas`
- **Attended maintenance re-enable procedure:**
  1. Field engineer authenticates via SSH (§6.2) or break-glass (§6.5)
  2. Runs `sudo /usr/local/sbin/usb-maintenance-enable` which modprobes `usb_storage` and starts a 60 min auto-revert timer
  3. At 60 min (or on explicit `usb-maintenance-disable` invocation), the kernel module is unloaded and USB storage is dead again
  4. Every enable/disable event is auditd-logged

### 9.4 Removable media policy

- No SD cards, USB sticks, optical media accepted into the Jetson in normal operation.
- Updates are network-delivered only (§8).
- If a physical recovery is needed (e.g., OS re-flash), the Jetson is removed from the ECP panel and taken to a secure platform provisioning workbench; it does not receive removable media in the field.

### 9.5 Offshore / marine variance

The offshore Cassette variant adds IECEx / ATEX hazardous-area certified enclosures, marine-grade coatings, and condensation management inside the ECP panel. It does **not** change the cybersecurity posture — the network interfaces, VLAN scheme, user model, and OTA chain are identical. Offshore deployments add a platform-side VSAT / LTE uplink constraint (higher latency, smaller OTA window) but the same signing chain applies.

---

## 10. Secrets management

### 10.1 Where secrets live

| Secret | Location | Protection |
|---|---|---|
| Jetson device OPC-UA key | `/etc/adc-bms/pki/opcua-device.key`, `0600 root:root` | TPM-backed keyring if `/dev/tpmrm0` present; otherwise filesystem-encrypted at rest via LUKS-protected `/var` partition (fallback posture — **CY-06** tracks TPM rollout) |
| Jetson OTA client key | `/etc/adc-bms/pki/ota-client.key`, `0600 root:root` | Same as above |
| SSH host keys | `/etc/ssh/ssh_host_*`, `0600 root:root` | Filesystem permissions; regenerated per Cassette |
| CDU skid Modbus — none | — | Modbus has no auth; no credential to store |
| SNMPv3 AuthPriv shared secret | `/etc/adc-bms/secrets/snmp.conf`, `0600 bms:bms` | Filesystem-encrypted at rest; rotated per §10.3 |
| NVIDIA BMC credentials | `/etc/adc-bms/secrets/bmc.conf`, `0600 bms:bms` | Filesystem-encrypted at rest; per-BMC unique credential from platform secrets manager |
| Platform historian forwarder token | `/etc/adc-bms/secrets/historian.token`, `0600 bms:bms` | Short-lived token (8 h), refreshed by `adc-bms` on expiry via OPC-UA method |

### 10.2 What is prohibited

- No credentials in source code, config YAML, or environment variables visible to `ps`
- No credentials in logs (auditd redacts known secret paths; `adc-bms` logs never emit cleartext credentials)
- No credentials in the gold image — all per-Cassette secrets are provisioned at first boot via platform enrollment
- No shared credentials across Cassettes — each Cassette has unique device keys, unique BMC credentials, unique SNMPv3 shared secret

### 10.3 Rotation

| Secret | Rotation cadence | Trigger |
|---|---|---|
| Device certs | 2 years (auto, §7.3) | Time-based |
| SSH host keys | 5 years (attended) | Time-based |
| SNMPv3 shared secret | 1 year | Time-based or on suspected compromise |
| BMC credentials | Per-BMC lifecycle (NVIDIA vendor process) | Hardware event |
| Historian token | 8 h | Session-based |

---

## 11. Audit logging & monitoring

### 11.1 What is logged

At the Jetson, every security-relevant event is logged:

- Auth: SSH logins (success/fail), sudo invocations (per command), HMI logins, OPC-UA session establishment and close, break-glass events
- Privilege changes: user add/remove, group changes, file permission changes on `/etc`
- Firewall: every ACCEPT and DROP on inbound TCP, plus rate-limited DROP on outbound (to catch egress anomalies)
- Crypto: cert install, cert rotation, CRL refresh, signature verification (pass/fail)
- OTA: every pull attempt, verification outcome, install, restart, rollback
- Application: alarm events per CTRL-001 §6.2, safe-state triggers, MIV commands, setpoint writes
- Physical: ECP panel tamper DI state changes (CY-04)

### 11.2 Where logs live

- Primary: Jetson local `/var/log/bms/*.jsonl` and auditd log at `/var/log/audit/audit.log`
- Forwarded: to platform historian over OPC-UA method call (`WriteHistoryEvents`) in 10 s batches
- Retention: 30 days local ring buffer on NVMe; platform historian retention per platform data governance (CL-11 in CTRL-001)
- Integrity: logs signed per-batch before forwarding; platform verifies signature on receipt to detect tampering

### 11.3 What the platform NOC watches for

At minimum — platform SIEM rules reference these events:

| Event | Rule |
|---|---|
| SSH auth fail rate | ≥ 5 fails in 1 min on any Cassette → alert |
| Successful SSH from unexpected source IP | Not on maintenance jumphost allowlist → alert |
| Sudo command list anomaly | Commands outside the approved field-engineer set → alert |
| Firewall DROP surge | ≥ 100 DROPs/min on inbound → alert |
| OPC-UA session from unknown cert | Any cert not in the platform user issuing CA set → alert |
| Cert signature verification fail | Any OTA verify fail → alert + block that artifact |
| Watchdog trip | Any WATCHDOG-TRIPPED event → dispatch |
| ECP panel tamper DI | State change outside a scheduled maintenance window → dispatch |
| Break-glass | Any break-glass session → 24 h report mandatory |
| USB enable | Any `usb-maintenance-enable` outside a scheduled maintenance window → alert |

---

## 12. Vulnerability management

### 12.1 Patch cadence by severity

| CVSS severity | Action | Timeline |
|---|---|---|
| Critical (9.0–10.0) | Emergency attended patch; may warrant unplanned maintenance window | ≤ 14 days from disclosure |
| High (7.0–8.9) | Next scheduled maintenance window | ≤ 30 days |
| Medium (4.0–6.9) | Next quarterly window | ≤ 90 days |
| Low (< 4.0) | Grouped into next major release | Best effort |

These targets assume platform-side CVE feed is live; CVE triage process in §12.3 drives the actual decision.

### 12.2 JetPack update path

- NVIDIA JetPack releases are reviewed by the platform build team within 7 days of release
- New JetPack gets integration-tested against `adc-bms` in a lab environment for ≥ 14 days
- Qualified JetPack releases are signed into the gold image and rolled out per §8.5 attended maintenance
- Jetson stays on the current qualified JetPack until the next major release is qualified — no skipping qualification

### 12.3 Package pinning

- The Jetson's apt sources are pinned to Ubuntu 22.04 main/security + NVIDIA L4T repos only
- No third-party PPAs
- `unattended-upgrades` applies only `main/security` and specifically excludes `linux-*`, `nvidia-*`, and `nvidia-jetpack` packages
- Python packages for `adc-bms` are version-pinned in the OCI image's `requirements.lock`; the OCI build process verifies hashes against PyPI

### 12.4 CVE triage process

For any CVE that mentions a package present in the `adc-bms` OCI image or the Jetson base OS:

1. Platform security reviews within 7 days of disclosure
2. Severity mapped to §12.1 timeline
3. Exploitability in the Cassette context assessed:
   - Is the vulnerable code path actually reachable given the firewall and VLAN scheme?
   - Is there a mitigating config already in place?
4. Decision: patch, mitigate (e.g., tighten firewall rule), or accept with compensating control
5. Decision recorded in platform vulnerability log; per-Cassette status tracked

A CVE that is unexploitable on the Cassette due to firewall or VLAN confinement is still patched on schedule — defense in depth — but on the §12.1 timeline, not emergency.

---

## 13. Incident response

### 13.1 Scope

This section covers incidents that are **local to a Cassette** — suspected compromise of the Jetson, anomalous OPC-UA traffic, unexplained safe-state trigger, physical tamper. Platform-wide incidents (tenant breach, platform NOC compromise, supply-chain event) route through platform IR and are out of scope here.

### 13.2 Phases

| Phase | Actions |
|---|---|
| **Declare** | Platform NOC or on-site engineer raises a Cassette security incident ticket, noting: Cassette serial, observed indicator, timestamp. Classification: `CY-INC-S` (suspected), `CY-INC-C` (confirmed). |
| **Isolate** | Platform issues an OPC-UA `maintenance-isolation` command (CTRL-001 §7.2), which puts the Cassette in safe-state and freezes workload. If OPC-UA is compromised, platform requests on-site break-glass (§6.5). If even SSH is not trusted, the BMS network switch uplink is severed at the platform edge — Cassette continues on local deterministic control. |
| **Preserve** | Before any remediation, platform pulls a full log snapshot from the Cassette (`/var/log/bms/*.jsonl`, auditd log, `/var/log/syslog`) and a filesystem snapshot of `/opt/adc-bms/releases/current` and `/etc/adc-bms/`. Snapshots are stored on the platform forensic volume, not modified on the Cassette. |
| **Recover** | Options, from lightest to heaviest: <br>(a) Restart `adc-bms` service <br>(b) Rollback to previous OCI release (§8.4) <br>(c) Rotate affected credentials (device certs, SNMPv3 secret, BMC credentials) <br>(d) Attended gold-image re-flash from a pre-staged spare eMMC <br>(e) Jetson module swap (spare kept on-site per platform spares policy) |
| **Post-mortem** | Platform IR authors a report within 14 days; updates to firewall rules, auditd rules, or this document are proposed as amendments to Rev 1.3. |

### 13.3 Non-recovery from cyber incident

At no point does an active cyber incident override the safety layer. MIV closure, watchdog, fire panel interface, and E-stop all continue to function even if the Jetson is unreachable or compromised — they are physically wired (CTRL-001 §2.2, §6.3). The worst-case cyber incident on the Jetson still leaves the Cassette in a controlled physical state.

### 13.4 Escalation to platform NOC

- All suspected incidents escalate to platform NOC within 1 h of detection
- Confirmed incidents trigger platform-wide review within 24 h
- Incidents with evidence of lateral movement beyond one Cassette escalate immediately to platform IR lead

---

## 14. Commissioning security checklist

This is the content of F-14 referenced in CTRL-001 §10.1 and the security gate for S-15 site sign-off.

| Check | Pass criterion |
|---|---|
| **C-01** Gold image SHA-256 verified at first flash | Hash matches platform-published digest |
| **C-02** Default Ubuntu accounts removed | `ubuntu`, `nvidia`, `guest` — none present in `/etc/passwd` |
| **C-03** Root login disabled | `PermitRootLogin no` in `/etc/ssh/sshd_config`; root has no password |
| **C-04** SSH key-only auth verified | Password login attempt rejected; key login succeeds for `operator` only |
| **C-05** SSH source IP restriction verified | SSH from non-maintenance-jumphost source IP rejected |
| **C-06** AppArmor enforcing | `aa-status` shows `adc-bms`, `sshd` in enforce mode |
| **C-07** Auditd rules loaded | `auditctl -l` lists expected rules from §4.2 |
| **C-08** Unused services masked | `systemctl is-enabled` returns `masked` for each service in §4.2 table |
| **C-09** Firewall default-deny | `nft list ruleset` shows default DROP; explicit allow rules match §5.3 |
| **C-10** VLAN ACLs on BMS network switch match §5.2 | Switch config diffs clean against signed-off template |
| **C-11** Device OPC-UA cert installed and chain-verifies | Certificate chain resolves to platform Device Issuing CA; expiry > 90 days |
| **C-12** OTA client cert installed; OTA pull succeeds with signature verification | One test artifact pulled, verified, rejected (deliberately bad sig), then accepted (good sig) |
| **C-13** OPC-UA Basic256Sha256 enforced | Anonymous connect attempt rejected; weaker policy connect attempt rejected |
| **C-14** OPC-UA user roles verified | `observer` cannot write; `operator` write accepted within envelope, rejected out of envelope; `platform` role isolated to platform users |
| **C-15** USB storage disabled at kernel | Inserting a USB stick produces no block device; `/proc/modules` shows no `usb_storage`; syslog shows blacklist match |
| **C-16** Serial console getty disabled | `/etc/systemd/system/getty.target.wants` has no serial TTY unit |
| **C-17** Watchdog independence verified | Pausing Jetson heartbeat drops safe-state relay within 5 s (overlap with CTRL-001 F-02 / F-12) |
| **C-18** Time sync live | PTP lock acquired; Jetson time within 100 ms of platform reference |
| **C-19** Auditd log forwarding to platform historian | Test event visible at platform historian within 60 s |
| **C-20** CRL poll works | Jetson pulls CRL from platform endpoint on schedule; test revocation propagates on next poll |
| **C-21** Break-glass procedure rehearsed | Field engineer successfully executes §6.5 on a commissioning-staged Cassette; session audited and reported |
| **C-22** Gold image digest and per-Cassette secrets inventory recorded | Cassette-as-built security document filed with platform IR and platform PKI |

All 22 checks pass → Cassette passes security commissioning and is eligible for S-15 soak. Any check fails → block production deployment, return to platform build team, re-issue commissioning report.

---

## 15. Open items

IDs use the **CY-xx** series to avoid collision with CTRL-001 **CL-xx**, COOL-001 **C-xx**, and COOL2-001 **CX-xx**.

| ID | Priority | Description | Blocks |
|---|---|---|---|
| CY-01 | C2 | Attested / measured boot with remote attestation to platform — SL 3 feature; out of scope at SL 2 but flagged for roadmap | SL 3 target, if platform raises target SL |
| CY-02 | C1 | Platform PKI readiness — Platform Root CA, Device Issuing CA, User Issuing CA must be operational with ACME-like endpoint before first Cassette commissioning | C-11, C-12 commissioning checks; production deployment |
| CY-03 | C2 | HMI multi-factor — RFID badge + PIN; Rev 1.2 ships with PIN-only; badge integration requires platform identity provider tie-in | HMI MFA; SIEM correlation of HMI + badge events |
| CY-04 | C1 | ECP panel tamper DI — formal wiring into CTRL-001 §3.2 spare DI channel; terminal block assignment; panel switch part number | C-22 sign-off; tamper event coverage in SIEM |
| CY-05 | C2 | Platform SIEM rule set — concrete rule definitions for the §11.3 watch list; tuning against real traffic during first 90-day soak | Alert quality |
| CY-06 | C2 | TPM-backed keyring rollout — Jetson AGX Orin TPM support via OP-TEE; Rev 1.2 ships with LUKS-at-rest as fallback; upgrade path documented | Key material protection beyond filesystem perms |
| CY-07 | C1 | Field engineer roster and key enrollment process — platform-side operational process for issuing SSH keys and OPC-UA user certs; revocation flow | Production deployment; break-glass procedure |
| CY-08 | C2 | OPC-UA role model review — role definitions (observer / operator / platform) reviewed against real operator workflows; may need additional roles | Operations ergonomics |
| CY-09 | C2 | Modbus TCP Security (RFC-based TLS wrapper) evaluation — revisit when CDU skid PLC replacement or firmware update enables TLS; not required at SL 2 | Future SL 3 migration |
| CY-10 | C2 | Supply-chain verification for BOM components with firmware — BMS switch, TraceTek controller, Munters DSS Pro — factory config audit procedure | Residual supply-chain risk |
| CY-11 | C2 | Full risk assessment per IEC 62443-3-2 — formal HAZOP-style security risk assessment by a qualified assessor | Compliance audit, insurance |
| CY-12 | C3 | Signed SSH user keys via SSH CA (instead of personal keys enrolled per-Cassette) — reduces per-Cassette enrollment overhead at scale | Scale to > 50 Cassettes |
| CY-13 | C2 | Red-team engagement — external penetration test against one commissioned Cassette before first production rollout | Real-world validation before scale |

---

## Document control

**Cassette-CYBER-001 — Rev 1.2 — CONFIDENTIAL**
**Prepared by:** Scott Tomsu · CEO / Chief Engineer · scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana
**Companion to:** Cassette-CTRL-001 · Cassette-ELEC-001 · Cassette-INT-001 · Cassette-BOM-001
**Supersedes:** Cassette-CYBER-001 Rev 1.1 (deleted)
**Closes:** CTRL-001 CL-07

Target security level: IEC 62443 SL 2. Any change to target SL, to the six-VLAN scheme, to the six protocol interfaces in CTRL-001 §4.6, or to the PKI hierarchy in §7.1 requires a new revision of this document and re-execution of the §14 commissioning checklist on any Cassette already in the field.

**End of Cassette-CYBER-001 Rev 1.2.**
