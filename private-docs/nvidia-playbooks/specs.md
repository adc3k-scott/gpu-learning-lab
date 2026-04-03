# NVIDIA Hardware Catalog for ADC
Last updated: 2026-03-25
Full catalog: memory/projects/nvidia_hardware_catalog.md

## NVL72 Rack (GB200 — Shipping Now)
- 72 Blackwell GPUs + 36 Grace CPUs per rack
- 1,440 PFLOPS NVFP4, 13.4 TB HBM3e
- 130 TB/s NVLink bandwidth
- 120-140 kW per rack
- 600mm x 1,068mm x 2,236mm, 1,360 kg
- OCP Open Rack V3 (NOT standard 19-inch)
- Direct-to-chip liquid cooling mandatory
- Est. $2.8-3.4M (training), $6-6.5M (GB300 inference)

## Vera Rubin NVL72 (H2 2026 — ADC Target)
- 72 Rubin GPUs + 36 Vera CPUs
- 3,600 PFLOPS NVFP4, 20.7 TB HBM4
- 260 TB/s NVLink 6 (2x Blackwell)
- Max Q: ~190 kW/rack | Max P: ~230 kW/rack
- 5x inference, 10x lower cost/token vs Blackwell
- In production Q1 2026, partner availability H2 2026
- Est. $5-8.8M per rack

## Networking
- Quantum-X800: 144-port, 800 Gb/s XDR InfiniBand, 115.2 Tb/s, SHARPv4
- ConnectX-8 SuperNIC: 800 Gb/s, dual-protocol IB/Ethernet, ships in GB200
- ConnectX-9 SuperNIC: 1.6 Tb/s, ships in Vera Rubin
- BlueField-4 DPU: 64 Arm cores, 800 Gb/s, integrated CX-9, ships 2026
- Spectrum-X800: 64-port 800G Ethernet (shipping)
- Spectrum-6 SPX: silicon photonics, 409.6 Tb/s (H2 2026)

## Edge
- Jetson AGX Orin: 275 TOPS, 15-60W, ~$1,599 module

## Software
- Base Command Manager: cluster management (free tier: 8 GPUs/system)
- GPU Operator: K8s GPU lifecycle automation
- DCGM: fleet monitoring, 30+ metrics, Prometheus
- DSX: Max-Q + Flex + Exchange + Sim
- Dynamo: inference OS (open-source)
- Mission Control: scheduling + orchestration

## DGX SuperPOD
- 1 SU = 8 NVL72 racks = 576 GPUs
- Scales to 128+ racks (9,216 GPUs)
- Fat-tree IB topology
- 4 network fabrics: compute, storage, in-band mgmt, OOB mgmt

## Ordering Path
- NPN registration -> DGX-Ready -> NCP -> Reference Platform NCP
- Order through OEM: Supermicro, HPE, Dell (50+ MGX partners for Vera Rubin)
- Allocation driven by: relationship + power readiness + site readiness
- NPN is INVITATION ONLY for ADC — Jim Hennessy (NVIDIA) working on portal access
