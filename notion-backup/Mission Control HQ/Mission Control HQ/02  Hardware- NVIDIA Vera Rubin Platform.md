# 02 — Hardware: NVIDIA Vera Rubin Platform
*Notion backup — 2026-03-28*

> Jensen Huang: "Rubin arrives at exactly the right moment... Rubin takes a giant leap toward the next frontier of AI."
> Sam Altman: "Intelligence scales with compute... The NVIDIA Rubin platform helps us keep scaling this progress."
---
## NVL72 Rack System
- 72 Rubin GPUs per rack
- 36 Vera CPUs per rack
- 3.6 ExaFLOPS NVFP4 inference per rack
- 100% liquid cooled — zero air cooling
- NVLink 6 switch fabric — 3.6 TB/s GPU-to-GPU per rack
- 260 TB/s NVLink bandwidth across 14-rack DGX SuperPOD
- 50.4 ExaFLOPS per 14-rack SuperPOD
- Ships fully integrated from Texas factory — 5-minute install (18x faster than prior gen)
---
## Six-Chip Architecture
### 1. Rubin GPU
- 288 GB HBM4 — 22 TB/s memory bandwidth — 72 per rack
### 2. Vera CPU
- 88 custom Olympus cores — replaces x86 for AI workload orchestration — 36 per rack
### 3. NVLink 6 Switch
- 3.6 TB/s GPU-to-GPU fabric per rack — 260 TB/s at SuperPOD scale
### 4. ConnectX-9 SuperNIC
- 1.6 Tb/s aggregate per GPU — AI traffic with zero CPU involvement
### 5. BlueField-4 DPU
- Rack-scale confidential computing — unlocks healthcare, finance, government workloads
- Encryption, firewall, storage I/O offloaded — GPU cycles reserved for inference
### 6. Spectrum-X Ethernet
- 800G per port — co-packaged optics — AI east-west traffic at rack scale
---
## 5 Investor Facts
- Fact 01: First rack-scale confidential computing — new market segments unlocked
- Fact 02: 18x faster deployment — 5 min install vs 1.5 hours prior gen
- Fact 03: 50.4 ExaFLOPS from 14 racks (DGX SuperPOD)
- Fact 04: 260 TB/s NVLink bandwidth across full SuperPOD cluster
- Fact 05: Full production H2 2026 — 4 hours from Marlie I
---
> UPDATED 2026-03-23: MARLIE I compute allocation corrected to match 24x40 ft building footprint.
## MARLIE I Compute Allocation
- Downstairs (System 1): 4 NVL72 racks, 288 GPUs, 520 kW IT load
- Upstairs (System 2): 4 NVL72 racks, 288 GPUs, 520 kW IT load
- Total: 8 NVL72 racks, 576 GPUs, 1,040 kW IT load
- NOT 16 racks. Prior spec exceeded building footprint and power envelope.
- Each floor: approx 888 sq ft usable (24x37 after staircase)
- 1 CDU pair per floor. NVIDIA integrated liquid cooling at 45C.
- Power: 800V DC native via Eaton Beam Rubin DSX