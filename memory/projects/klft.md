# KLFT 1.1 — Autonomous Airspace Operations Hub
Last updated: 2026-03-08

## What It Is
Full engineering package for an autonomous drone operations hub at Lafayette Regional Airport (KLFT), Louisiana.
Covers mission control software, safety-critical systems, fleet management, compliance/FAA integration, and commercial drone operations (DFR, medical delivery, inspection, logistics).

## Product Tracks (two separate things in this folder)
1. **KLFT / SkyCommand** — autonomous airspace operations hub and scalable drone platform product
2. **AIKCC** (AI Knowledge Command Center) — separate SaaS product: AI knowledge website with learning paths, tool reviews, monetization. Not airspace-related. Should eventually be moved to its own Notion page.

## Notion Location
KLFT 1.1 page: 31d88f09-7e31-80ec-b055-f69b9108355e (under Mission Control HQ)

## 10 Sub-Pages
| Page | Status |
|------|--------|
| README | Document index — SkyCommand package overview |
| KLFT_Autonomous_Airspace_Ops_Hub_System_Architecture | 8-subsystem architecture, DO-178C DAL-C safety design |
| KLFT_CONOPS_and_Safety_Case | SORA hazard methodology, FAA submission framework |
| KLFT_Phase1_Implementation_Specification | 26-week sprint plan, full API contracts, DB schemas |
| KLFT_Software_Interface_Control_Document | gRPC, Kafka, shared memory interfaces |
| KLFT_Facility_Hardware_Procurement_Spec | BOM, rack layouts, network, sensor, drone procurement |
| SkyCommand_Platform_Architecture | Generalized multi-site drone platform |
| SkyCommand_MVP_Specification | 8-week, <$25K, 2-person startup guide |
| SkyCommand_Technology_Stack | US-manufactured/open-source stack (no DJI) |
| AIKCC_Platform_Architecture | Separate product — AI knowledge website/SaaS |

## Key Hardware Decisions (confirmed March 2026)
- **Drone platform: COMMITTED — Skydio X10 + Skydio Dock**. DJI REMOVED — Countering CCP Drones Act regulatory risk.
- **Edge compute: NVIDIA Jetson Orin NX 16GB** — dock-side. Current. No change needed.
- **AI inference server (Phase 3, not Phase 1):** NVIDIA L40S (Ada Lovelace, 48GB) preferred. A4000 deprecated. H100 PCIe as alternative if training required.
- **Mission services servers (Phase 1):** Dell PowerEdge R660xs × 2 — Xeon 4416+, 128GB DDR5. No GPU.

## Phase Roadmap
- Phase 1 (Months 1-6): Single-operator, single Skydio vehicle, VLOS/EVLOS. $800K-$1.2M. 10 operational missions as exit criteria.
- Phase 2 (Months 6-12): Multi-vehicle, Safety Supervisor on dedicated hardware, ADS-B, deconfliction. $600K-$1M.
- Phase 3 (Months 12-24): AI inference node, 3-5 docks, BVLOS readiness, DAA sensors. $1.5M-$2.5M.
- Phase 4 (Months 24-36): 50+ concurrent ops, 10+ dock sites across Acadiana. $600K-$1.2M.

## Current Status
Engineering package created February 2026. All docs are v1.0 engineering drafts. Not yet in active development. No contracts signed, no hardware ordered.

## What Was Fixed (March 8, 2026)
- Removed DJI as platform option — deleted DJI BOM table, removed DJI from all table cells across both facility and phase 1 specs
- Updated all references to Skydio as the sole committed platform
- Updated GPU-001 spec: deprecated A4000, committed to L40S for Phase 3 inference
- Added callout noting DJI regulatory risk with explanation
