# MARLIE 1 — Mission Control Hub / First 10 MW Deployment
Last updated: 2026-04-06

## What MARLIE 1 Is
Permanent AI Factory at 1201 SE Evangeline Thruway, Lafayette, Louisiana.
ADC3K HQ, Mission Control operations center, and first revenue-generating compute node.
Downstairs = compute floor (10 interior NVL72 racks). Upstairs = Mission Control AI ops center.
Home base proving ground for the Pure DC AI Factory model. Every future deployment cloned from this playbook.

## Site
- Address: 1201 SE Evangeline Thruway, Lafayette, Louisiana
- GPS: 30.21975 N, 92.00645 W
- Parcels: 3 adjacent parcels on Chag Street — cassette deployment pads
- Land debt: $15,000 — effectively debt-free. Owner-controlled. No lease risk.
- Zoning: Industrial — heavy use permitted. No rezoning required.
- Storm: FEMA Zone X, high ground, zero structural damage through multiple Cat hurricanes

## Utilities — ON SITE
- LUS Fiber: ON SITE — live and connected. City-owned gigabit municipal network.
- Natural gas (Atmos Energy): ON SITE — live. Henry Hub 40 miles (Erath, LA).
- 3-phase power: Confirmed on site.
- LUS Power Substation: ~1 mi

## Hardware — LOCKED
- NVIDIA Vera Rubin NVL72 (H2 2026 full production)
- 72 Rubin GPUs + 36 Vera CPUs per rack | HBM4 288 GB/GPU | NVLink 6 | 3.6 ExaFLOPS NVFP4/rack
- TOTAL SITE: 40 racks / 2,880 GPUs / 144 ExaFLOPS NVFP4

## Site Layout — LOCKED
- INTERIOR (building downstairs): 10 NVL72 racks — 770 sq ft (22×35 ft) — walkable demo + live compute
- EXTERIOR (Chag St parcels): 3 ADC 3K Cassettes × 10 racks each = 30 racks
- UPSTAIRS: Mission Control operations center — monitoring, control, engineering workspace
- Total: 10 interior + 30 exterior = 40 racks

## Power Architecture — LOCKED
- L1 PRIMARY: Bloom SOFC — 40 units × 250 kW = 10 MW, 800V DC direct, 54% efficiency, N+1
- L2 OFFSET: First Solar TR1 — 300 kW, 1500V DC, Louisiana-manufactured
- L3 BRIDGE: Eaton xStorage LFP — 600 kWh, DC-coupled, instant ATS, 4-hr min
- L4 BUS: 800V DC — Eaton Beam Rubin DSX — OCP Stage 1d — 800V operating / 1500V rated
- L5 SOFTWARE: Eaton Brightlayer + Siemens Omnivise + NVIDIA Omniverse DSX digital twin
- NO GRID. NO DIESEL. NO AC ANYWHERE.

## Cooling Architecture — LOCKED
Liquid loop: Boyd cold plates (GPU die, NVIDIA RVL) → Staubli UQD QDs (450/rack) →
CoolIT CHx2000 row CDU (2 MW, 12 racks/unit, NVIDIA RVL/AVL) → Danfoss CoolTrain TCS →
adiabatic dry cooler heat rejection. 100% liquid cooled. Zero air cooling in compute loop.

Humidity — Munters HCD desiccant (phased in per cassette as deployed):
- Lafayette: 75-80% RH, 8 months/year — condensation risk on cold cooling lines
- Munters: no compressor, ~500W draw, positive pressure, ±1°F dew point
- Waste heat from Bloom SOFC reactivates desiccant wheel — zero added energy cost

## Network
- Intra-rack: NVLink 6 — 260 TB/s aggregate
- Scale-out: InfiniBand NDR 400 Gb/s — NVIDIA Quantum-X800 switch
- Ethernet: Spectrum-X 800G | BlueField-4 DPU offload
- Inference acceleration: Groq LPU (real-time/deterministic) + NVL72 GPU (training/batch)
- External: LUS Fiber ON SITE — live

## Certifications / Execution
- 7 active NVIDIA certifications — DSX compliant from day one
- Louisiana GC license — Scott Tomsu pulls permits, no third-party GC
- FAA Private Pilot + Part 107 UAS

## Incentive Stack
- ITEP: Pre-qualify BEFORE groundbreaking. Non-negotiable.
- Louisiana Act 730: 20-yr tax exemption on qualifying equipment ($200M+ capex, 50+ jobs)
- OBBBA: FEOC-clean — Texas-manufactured NVIDIA, 100% US ownership, Louisiana GC
- BEAD: LUS Fiber on site — SE Evangeline corridor eligible
- Quality Jobs: 6% payroll rebate, 10 years | LED FastStart: free workforce training

## Deck / Files
- HTML deck: private-decks/marlie-deck.html (rebuilt 2026-04-06 — partner/NVIDIA/Bloom version)
- Plain text: private-decks/marlie-deck-text.txt
- Notion root: 31e88f09-7e31-8121-b4d2-d96b0084cc50 (9 sections)

## Timeline
- Site ready: NOW | Build + install: 3-6 months | H2 2026 hardware | Revenue: day one after install
