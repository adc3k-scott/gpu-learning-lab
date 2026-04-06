# Network Topology Diagrams
*Notion backup — 2026-04-06*

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