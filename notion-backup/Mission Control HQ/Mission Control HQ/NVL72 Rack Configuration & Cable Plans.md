# NVL72 Rack Configuration & Cable Plans
*Notion backup — 2026-04-06*

> NVIDIA Vera Rubin NVL72 — 72 Rubin GPUs + 36 Vera CPUs per rack. 3.6 ExaFLOPS NVFP4. 100% liquid cooled. Full production H2 2026.
---
## Phase 1 Layout — 22 x 35 ft Floor (770 sq ft)
- Total racks: 16 NVL72 units
- Arrangement: Row A (8 racks) + Row B (8 racks) — hot aisle contained between rows
- Walk-through: Cold aisle access front and rear — sealed hot aisle center
- Aggregate compute: 57.6 ExaFLOPS NVFP4
- Aggregate memory BW: 260 TB/s
---
## Per-Rack Specs (NVL72)
- GPUs: 72x Rubin GPU — 36 per NVLink domain, 2 domains per rack
- CPUs: 36x Vera CPU — 88 Olympus Arm cores (Armv9.2) each, 1.5 TB LPDDR5X, 1.2 TB/s memory BW per CPU
- NVLink 6 Switches: 9x switch trays per rack — 28.8 TB/s per tray, 260 TB/s aggregate, in-network SHARP FP8 compute
- Memory: HBM4 — 288 GB per Rubin GPU, 20.7 TB total per NVL72 rack, 1.58 PB/s aggregate bandwidth
- Power per rack: TDP not yet published by NVIDIA — contact NVIDIA Enterprise Sales for facility planning specs
- Cooling: Rear-door CDU manifold — 100% liquid, no air cooling
---
## Cable Plans
### NVLink Fabric (Intra-rack)
- Topology: NVLink 6 Switch — full mesh within rack via 9-switch rail
- Cable type: NVIDIA NVLink optical cables — pre-routed at factory
- Field cabling required: None for NVLink intra-rack
---
### InfiniBand NDR (Inter-rack)
- NIC: ConnectX-9 SuperNIC — 1.6 Tb/s per adapter (800 Gb/s per port) — >144 adapters per NVL72
- Fabric: NDR400 InfiniBand — 400 Gb/s per port
- Switch: NVIDIA Quantum-3 InfiniBand — top-of-rack or end-of-row
- Cable type: NVIDIA Quantum HDR/NDR DAC or optical — 2m intra-row, 5m cross-row
- Total uplinks: 16 racks x 2 ports = 32 uplinks to spine
---
### Ethernet Management (BlueField-4 DPU)
- DPU: BlueField-4 — 1x per NVL72 — OOB management + storage offload
- Uplink: 10GbE management — 1 cable per rack to management switch
- Switch: Dedicated 24-port 10GbE management switch in network core
---
## Rack Numbering Convention
```plain text
Row A: A01 A02 A03 A04 A05 A06 A07 A08  (cold aisle front)
              [sealed hot aisle]
Row B: B01 B02 B03 B04 B05 B06 B07 B08  (cold aisle rear)

Network Core: NC01 (north end, near entry)
CDU Manifold: Runs along exterior north wall
```
---
## NVIDIA Field Resources
- DGX-Ready colocation checklist: developer.nvidia.com/dgx-ready-data-center
- NVL72 power + cooling specs: Contact NVIDIA Enterprise Sales
- Field installation: NVIDIA-certified solution architect required
> SCOPE: This document applies to MARLIE I — the permanent AI Factory at 1201 SE Evangeline Thruway. NOT applicable to ADC 3K container pods, which use immersion cooling and a separate architecture.
---
> UPDATED 2026-03-23 -- POST-GTC REWRITE
## NVL72 Rack -- Vera Rubin Platform (December 2026 availability via HPE)
### Per Rack:
- 72 NVIDIA Rubin GPUs
- 36 NVIDIA Vera CPUs
- 9 NVLink 6 switches (6th generation)
- ConnectX-9 SuperNIC (1.6 Tb/s)
- BlueField-4 DPUs
- HBM4: 288 GB per GPU
- Power: 130 kW per rack
- Cooling: Direct-to-chip liquid, 45C hot water
- Power input: 800V DC (Eaton Beam Rubin DSX)
- Internal conversion: 64:1 LLC (800V -> 12V, 98% efficient, built-in)
### Rack Counts by Site:
Willow Glen: Phase 1 = 10 racks (8 VR + 2 Groq), Max = 2,000+, IT Power = 260 MW
MARLIE I: Phase 1 = 8 racks (4 per floor), Max = 8, IT Power = 1.04 MW
Trappeys: Phase 1 = 4 racks, Max = 225, IT Power = 29 MW
ADC 3K Pod: 1-2 per container, Max = 2, IT Power = 130-260 kW
### Cable Plan (per rack):
- NVLink 6: Factory-integrated (intra-rack, do not touch)
- InfiniBand: Quantum-X800 switches, 800 Gb/s per port
- Ethernet: Spectrum-X, BlueField-4 DPU per node
- Management: 10GbE OOB to NOC
- Power: Single 800V DC feed from Eaton bus
### Multi-Vendor Future:
- Primary: NVIDIA Vera Rubin NVL72
- Future: Tesla Terafab chips (when available)
- Future: AMD Instinct (if competitive)
Pod architecture is chip-agnostic at the facility level -- 800V DC and liquid cooling work for any vendor.
---
> WARNING (2026-03-24): Pre-GTC content above says 16 racks and InfiniBand NDR/Quantum-3. CORRECT specs are in the POST-GTC section: 8 racks per floor at MARLIE I, Quantum-X800 (800 Gb/s), 130 kW per rack.