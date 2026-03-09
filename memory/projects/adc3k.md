# ADC 3K — Project State
Last updated: 2026-03-08

## What ADC 3K Is
Manufactured containerized AI compute pod product line. NOT a building — a product.
Deployed as individual units to remote sites. Immersion cooling (no HVAC required).
Networked back to MARLIE I (the factory/HQ). Think of it as the product MARLIE I manufactures and deploys.

## Current Phase
Pre-production. Engineering specs complete. No hardware ordered. No site LOI signed.
First deployment target: Trappeys Cannery (metal warehouse, immersion pods, no HVAC needed).

## Product Specs (confirmed)
- Form factor: 40-ft High Cube ISO container
- Cooling: Immersion — single-phase dielectric. Committed fluid: **Engineered Fluids EC-110** (3M Novec DISCONTINUED — never reference it)
- PUE target: 1.02–1.05
- Heat rejection: Exterior dry cooler or liquid-to-liquid HX
- Power: 480V 3-phase input, N+1 generator backup
- No HVAC, no raised floor, no hot aisle — drops into any structure with power + fiber
- GPU platform: NVIDIA Vera Rubin NVL72 (H2 2026) — TDP NOT yet published by NVIDIA

## Open Action Items (Investor-Critical)
### First-pass gaps (original)
1. **Customer LOI** — zero signed anchor tenants. Fatal for institutional raise. Do first.
2. **NVIDIA TDP** — Vera Rubin NVL72 TDP unpublished. Cannot finalize CDU/power/electrical. Engage NVIDIA Enterprise Sales.
3. **HB 827 PILOT** — Phase 1 (~$19-30M) below $200M threshold. Develop parish-level PILOT agreement as HB 827 replacement. Brief investors honestly.
4. **CapEx reconciliation** — $33.2M stated vs analyst estimates $8-10M/rack × 14 racks. Reconcile before investor meeting.
5. **Financial model tax rate** — model uses ~25% LA corporate tax. Actual: 5.5%. Fix Assumptions tab. IRR is higher.

### Second-pass gaps (March 8, 2026)
6. **Unit economics per pod** — missing: pod CapEx, revenue/pod/month, OpEx/pod, payback period. Add to financial model.
7. **Remote site ops model** — define: MARLIE I NOC manages all pods remotely. Maintenance via local contract. SLA target 99.5%. No on-site staff required.
8. **Competitive landscape** — no comp analysis in deck. Add slide: CoreWeave, Lambda, Crusoe, Lancium vs ADC 3K differentiators.
9. **Exit strategy** — missing from deck. Options: strategic acquisition, build-to-sell pod swarms, REIT structure.
10. **Management team** — no team slide. Add: founder bio, key hires plan, advisors.
11. **3-scenario financial model** — bear (40% util, -30% GPU price), base (70% util), bull (90% util, 10+ sites Y3).
12. **Dielectric fluid** — RESOLVED. Engineered Fluids EC-110 committed. Novec references removed from all docs.

## Pending (Non-investor)
- NVIDIA Inception application: package ready (ADC3K_NVIDIA_Inception_Application_Package_Rev1.docx). Not submitted. Frame ADC-3K division as launched 2025/2026 (not ADC Inc. founded 2003).
- Cooling vendor RFIs: package ready. 4 emails to send.
- Patent disclosure: ready for counsel. Target provisional Q2 2026.
- ITEP: must file BEFORE breaking ground. Non-negotiable. Tie to site LOI execution.
- LUS/SLEMCO utility capacity confirmation: not yet obtained. Required before raise.

## Notion Location
ADC 3K — Project Command Center: 31488f09-7e31-816d-9fdc-c6aabba4e3fa
- Pod Swarm Engineering Suite: NVL72 rack config, CDU cooling, PDU, network topology, RunPod API (all labeled MARLIE I scope — ADC 3K uses immersion, separate spec needed)
- Master Task Tracker: 41 P0/P1/P2 tasks from container order → GO-LIVE
- Investor Review section: Items 1-5 open, Items 6-7 resolved (March 8, 2026)

## Key Documents (local files)
ADC-3K-Engineering-Lock-Package.docx | ADC-3K-Financial-Model.xlsx
ADC-3K-Investor-Pitch-Deck.pptx | ADC-3K-Vendor-Parts-List.xlsx
ADC-3K-Master-Website-V3.html (~728KB SPA, production-ready)

## Remote Operations Model (confirmed)
- NOC: MARLIE I manages all deployed pods remotely via Mission Control
- No on-site staff at remote sites — pods are lights-out
- Maintenance: on-site visits for fluid checks / GPU swaps via local contract firms
- Site owner provides: power, fiber, and space — ADC 3K handles everything inside the container
- SLA target: 99.5% uptime

## Power Architecture (confirmed standard)
- Primary: LUS grid utility feed
- Supplemental: Bloom Energy fuel cell (continuous baseload generation, NOT backup)
- Emergency: Diesel gensets N+1 (auto-start, exterior pad mount)
