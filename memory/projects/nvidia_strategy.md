---
name: NVIDIA Strategy
description: NVIDIA-only hardware stack, DGX SuperPOD architecture, and GTC positioning for ADC
type: project
---

# NVIDIA Strategy — ADC AI Factory Stack

Last updated: 2026-03-12

## Core Principle: NVIDIA-Only Stack
ADC builds exclusively on NVIDIA. No AMD, no Intel Gaudi, no custom ASICs. Every GPU, every switch, every software layer is NVIDIA. This is not a preference — it is a strategic lock-in that qualifies ADC for the highest-tier NVIDIA partnership programs and makes the ADC compute fabric plug-and-play with every major AI framework.

## NVIDIA-First Sequencing (Willow Glen)
**Rule**: Get NVIDIA on board FIRST. Then approach WGT with the partnership backed by NVIDIA.
- NVIDIA partnership gives WGT confidence that ADC is a serious counterparty
- NVIDIA certification validates the infrastructure thesis independently of ADC's own claims
- Investor deck backed by NVIDIA relationship = institutional-grade credibility
- Sequence: NVIDIA Inception → NVIDIA Enterprise Sales engagement → WGT approach with NVIDIA backing

## Hardware Platform
- **GPU**: NVIDIA Vera Rubin NVL72 (CES 2026, H2 2026 full production)
  - 72 Rubin GPUs + 36 Vera CPUs per rack
  - HBM4 — 288 GB per GPU
  - NVLink 6 for intra-rack GPU interconnect
- **Networking (Willow Glen)**: InfiniBand spine — NVIDIA Quantum switches
  - InfiniBand is the ONLY network fabric inside Willow Glen's compute fabric
  - Management traffic (MARLIE 1 ↔ Willow Glen) runs on dedicated fiber, NOT InfiniBand
- **Management**: NVIDIA Base Command Manager — cluster orchestration, job scheduling, health monitoring
- **Immersion (ADC 3K pods)**: EC-110 single-phase dielectric. Pod-level, not rack-level.

## DGX SuperPOD Architecture
Willow Glen is the SuperPOD home. The SuperPOD reference architecture calls for:
- InfiniBand spine (Quantum NDR switches) as the compute fabric
- Base Command Manager for job orchestration across the full pod cluster
- Standardized rack configurations (DGX B200 or NVL72 racks)
- NVIDIA-validated cooling and power specs per rack
- On-site NOC with NVIDIA-certified operators

SuperPOD is the benchmark NVIDIA uses to qualify partners for DGX Cloud and enterprise GPU-as-a-service contracts. Achieving SuperPOD certification at Willow Glen positions ADC as a first-tier NVIDIA partner in the Gulf South.

## NVIDIA Inception Program
- Application package prepared: `ADC-3K-NVIDIA_Inception_Application_Package_Rev1.docx`
- NOT yet submitted as of 2026-03-12
- Frame ADC-3K division as launched 2025/2026 — NOT ADC Inc. (founded 2003)
- Inception is the on-ramp to NVIDIA Enterprise Sales and DGX partnerships

## GTC Positioning
- NVIDIA GTC is the primary venue for advancing the ADC/NVIDIA relationship
- Scott attending GTC — bringing tape measure for real board dimensions (NVL72 form factor for immersion tank design)
- Goal at GTC: engage NVIDIA Enterprise Sales, get TDP spec for NVL72 (unpublished as of 2026-03-12)
- Secondary goal: DGX SuperPOD roadmap briefing, Quantum switch specs for Willow Glen fabric

## Software Stack (NVIDIA-only)
- NVIDIA CUDA — compute runtime, all accelerated workloads
- NVIDIA NIM — inference microservices for production AI deployment
- NVIDIA Base Command Manager — cluster management
- NVIDIA AI Enterprise — full software suite for partners
- No AMD ROCm, no OpenCL — CUDA-only codebase

## Open Items
- Submit NVIDIA Inception application (package ready)
- Engage NVIDIA Enterprise Sales for NVL72 TDP spec
- Obtain DGX SuperPOD certification roadmap for Willow Glen
- NVIDIA-first approach to WGT partnership (do not approach WGT without NVIDIA backing)
