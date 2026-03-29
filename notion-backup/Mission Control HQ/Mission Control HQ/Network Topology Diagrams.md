# Network Topology Diagrams
*Notion backup — 2026-03-28*

> Three separate fabrics: NVLink 6 (intra-rack GPU), InfiniBand NDR (inter-rack compute), Spectrum-X Ethernet (external/storage). Management on isolated 10GbE.
---
## Fabric 1 — NVLink 6 (Intra-Rack GPU Fabric)
- Scope: Within each NVL72 rack only
- Bandwidth: 3.6 TB/s per GPU bidirectional (NVLink 6) — 260 TB/s aggregate across rack
- Topology: Rail-optimized via 9x NVLink 6 Switch per rack
- Cabling: Factory-integrated — no field assembly
- Latency: Sub-microsecond GPU-to-GPU within rack
---
## Fabric 2 — InfiniBand NDR (Inter-Rack Compute Fabric)
```plain text
                 [ IB Spine Switch (64-port NDR400) ]
                /              |              \
       [IB Leaf 1]        [IB Leaf 2]        [IB Leaf 3]
       (32-port NDR)      (32-port NDR)      (32-port NDR)
      / | | | | \        / | | | | \        / | | | | \
    A01 A02 A03 A04   A05 A06 A07 A08   B01 B02 B03 B04
                                         B05 B06 B07 B08

Each rack: 2x ConnectX-9 SuperNIC (1.6 Tb/s each)
Each leaf: 16 downlinks (rack) + 8 uplinks (spine)
Total bisection BW: ~25.6 Tb/s
Oversubscription: 2:1 leaf-to-spine
```
- Switch vendor: NVIDIA Quantum-3 InfiniBand
- Per-port BW: 400 Gb/s NDR
---
## Fabric 3 — Spectrum-X Ethernet (External / Storage)
```plain text
[ LUS Fiber Uplink -- 100GbE (upgrade path: 400GbE) ]
        |
  [ Spectrum-6 (SN6810 / SN6800) Top-of-Row Switch ]
   /    |    |    |    |    |    |    \
 A01  A02  ...  B08  [NAS] [Object Store] [Customer VPN]

Each NVL72: 1x 400GbE to Spectrum-X via BlueField-4 DPU
Purpose: external customer traffic, storage, internet uplink
```
- LUS Fiber uplink: 100GbE day 1 — upgrade path to 400GbE / dark fiber
- BlueField-4 DPU: Offloads networking/storage from Vera CPU — 1 per rack
- Switch: NVIDIA Spectrum-6 SN6810 (102.4 Tb/s) / SN6800 (409.6 Tb/s) — co-packaged optics, 800 Gb/s ports
---
## Fabric 4 — Management Network (OOB)
```plain text
[ Management Switch -- 24-port 10GbE ]
  |  |  |  |  ...  |  |  |  |
 A01 A02 ... B08  [MC Server] [BMS GW] [KVM/IPMI]

Purpose: out-of-band management, independent of compute fabrics
Access: BMC/IPMI per rack + BlueField-4 DPU management port
Remote: WireGuard / Tailscale VPN
```
---
## WAN / Uplink
- Provider: LUS Fiber — city-owned, direct negotiation, no Big Telecom premium
- Day 1: 100GbE dedicated
- Upgrade path: 400GbE or dark fiber as customer demand grows
- Redundancy: SLEMCO or secondary carrier as failover
- BGP: Own AS number + IP block for sovereign routing — Phase 2 target
---
## IP Plan (Draft)
```plain text
Management:    10.0.0.0/24    -- BMC, switches, BMS
Compute IB:    10.1.0.0/16    -- InfiniBand fabric
Storage/Eth:   10.2.0.0/16    -- Spectrum-X tenant fabric
Customer VMs:  10.100.0.0/16  -- NAT to LUS uplink
Mission Ctrl:  10.0.0.1
DNS/NTP:       10.0.0.2
```
> SCOPE: This document applies to MARLIE I — the permanent AI Factory at 1201 SE Evangeline Thruway. NOT applicable to ADC 3K container pods, which use immersion cooling and a separate architecture.
---
> UPDATED 2026-03-23 -- POST-GTC REWRITE
## Network Architecture -- Hub and Spoke
### Fabric 1: NVLink 6 (Intra-Rack)
- 6th generation NVLink
- 260 TB/s aggregate bandwidth per rack
- Factory-integrated -- DO NOT modify
### Fabric 2: InfiniBand (Inter-Rack, Intra-Site)
- NVIDIA Quantum-X800 switches
- 144 ports x 800 Gb/s per switch
- Willow Glen: Full fat-tree topology (PRIMARY compute fabric)
- MARLIE I: Single spine switch (8 racks)
- ADC 3K Pod: No InfiniBand (single rack = NVLink only)
### Fabric 3: Ethernet (Services + WAN)
- NVIDIA Spectrum-X (Spectrum-6 switches)
- BlueField-4 DPU per node
- Site-to-site: Dedicated fiber (Willow Glen <-> MARLIE I, 60 mi)
- Remote pods: Starlink or cellular backhaul
- LUS Fiber: 100GbE municipal fiber for MARLIE I/Trappeys (0.8 mi)
### Fabric 4: Management (OOB)
- 10GbE out-of-band management
- WireGuard/Tailscale mesh VPN across all sites
- Mission Control dashboard at Willow Glen NOC
- Backup NOC at MARLIE I
### Fleet Orchestration:
- NVIDIA Run:AI for workload scheduling across all nodes
- NVIDIA Dynamo 1.0 for inference optimization (7x performance)
- Mission Control AI (ADC-built) for autonomous operations
- NVIDIA Base Command Manager for cluster management
### Hub-Spoke Connectivity:
Willow Glen <-> MARLIE I: Dedicated fiber, 100 Gbps (Management only, NOT InfiniBand)
Willow Glen <-> Trappeys: Dedicated fiber, 100 Gbps (Via Lafayette fiber)
Willow Glen <-> Remote Pods: Starlink/VSAT, 100-500 Mbps (Inference results only)
MARLIE I <-> Trappeys: LUS Fiber, 10 Gbps (0.5 mi)
---
> WARNING (2026-03-24): Pre-GTC fabric specs above reference Quantum-3 NDR 400 Gb/s. CORRECT: Quantum-X800 at 800 Gb/s. Hub-and-spoke architecture in POST-GTC section is authoritative.