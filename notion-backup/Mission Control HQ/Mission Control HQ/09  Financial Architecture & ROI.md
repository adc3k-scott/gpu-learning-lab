# 09 — Financial Architecture & ROI
*Notion backup — 2026-03-28*

> This is not a data center. This is a money machine. Every watt generates revenue. Every dollar goes to compute. The comparison is not close.
---
## Capital Stack
- Infrastructure raise: ~$1.17M — covers facility buildout (electrical, cooling, fiber, power distribution, commissioning)
- GPU hardware financed separately: equipment financing + NVIDIA Capital programs + SBA facilities
- EBITDA figures below = facility-level operating cash flow
- Full investor pro forma with hardware financing and debt service available upon request
---
## MARLIE I vs Legacy Data Center — Key Comparison
- PUE: Legacy 1.4–1.8 (40–80% wasted) vs MARLIE I 1.10 (liquid-cooled, best-in-class)
- Energy cost: Legacy $0.10–$0.18/kWh national avg vs MARLIE I $0.065/kWh Louisiana industrial
- Cooling: Legacy air (CRAC units, chillers) vs MARLIE I 100% direct-to-chip liquid
- Revenue per rack per year: Legacy $200K–$500K (colo) vs MARLIE I $3M–$5M+ (AI compute)
- Operations: Legacy 20–50 FTE manual ops vs MARLIE I 3–5 FTE Mission Control AI
- On-site generation: Legacy none (grid dependent) vs MARLIE I Bloom Energy fuel cells + gas generators
- Domestic content: Legacy mixed overseas vs MARLIE I 100% USA — OBBBA compliant
---
## Revenue Model — AI Compute Rental (Conservative Basis)
- Rate basis: $6/GPU/hr conservative (H100 market: $2.50–$3.50). Vera Rubin 2.5x FP4 density — premium tier justified
- At $8/GPU/hr mid estimate, Year 3 two-floor gross reaches $121.5M. OPEX stays flat. Upside is asymmetric.
### Year 1 — 4 Racks Live, 40% Utilization
- 288 GPUs online (Floor 1 ramp)
- Gross revenue: $6.1M
- OPEX: ~$1.29M (4-rack scale)
- EBITDA: ~$4.78M
### Year 2 — 8 Racks Live, 65% Utilization
- 1,728 GPUs online (24 racks — Floor 1 full + Floor 2 partial)
- Gross revenue: $44.5M
- OPEX: ~$3.0M (24-rack scale)
- EBITDA: ~$41.5M
### Year 3 — 16 Racks Live, 75% Utilization
- 2,304 GPUs online (32 racks — both floors full)
- Gross revenue: $91.1M
- OPEX: ~$3.68M (full two-floor scale)
- EBITDA: ~$87.4M
---
## Power Resilience — 5 Independent Layers
- Layer 1: LUS Grid — primary utility ($0.065/kWh industrial)
- Layer 2: Bloom Energy fuel cells — 300 kW continuous, $0.07–$0.09/kWh effective, 60%+ efficiency, Newark Delaware
- Layer 3: Cat G3520H natural gas prime power (PARALLEL N+1) — 2x 2.5MW = 5MW total installed. Both units run in parallel at moderate load. True N+1 — if one requires service, the other carries full facility.
- Layer 4: UPS battery ride-through — millisecond switchover, protects compute hardware from power transients
- Layer 5: Diesel emergency backup — Cat C175-16, 3,365kW. 30,000-gal on-site tank, 110+ hours runtime. Hurricane layer.
- 5 independent power layers — 0 single points of failure — 96+ hour on-site fuel reserve
---
## Investor Benefits
- Reserved bandwidth: GPU compute access during off-peak hours proportional to investment tier. Estimated value: $50K–$500K/month compute credit.
- Early mover rate lock: investors before first rack goes live receive locked GPU rental rates below market for 24 months
- Ring Power dealer relationship: single service contract covers entire Cat generator fleet (nat gas + diesel)
---
> CORRECTED 2026-03-23: Multiple errors in financials above. Bloom Energy removed. Generator model corrected. Rack count corrected to 8 (not 16/24/32). LUS Grid is backup, NOT primary. Revenue projections above are based on wrong rack counts and must be recalculated.
## Corrected Power Stack
- Layer 1: Solar (300 kW rooftop + ground mount, First Solar TR1)
- Layer 2: Natural Gas (2x Cat G3520C, 1.5 MW each, N+1). THIS IS PRIMARY POWER.
- Layer 3: Diesel emergency backup
- Layer 4: Grid (LUS backup only. NOT primary. NOT sell-back at MARLIE I.)
- 600 kWh LFP battery (Eaton xStorage) for ride-through
- NO Bloom Energy fuel cells at MARLIE I.
- Generator model: Cat G3520C (not G3520H). 1.5 MW each (not 2.5 MW).
## Corrected Compute Capacity
- Total: 8 NVL72 racks, 576 GPUs, 1,040 kW IT load
- Downstairs: 4 racks (288 GPUs, 520 kW)
- Upstairs: 4 racks (288 GPUs, 520 kW)
- Prior Year 2 (24 racks) and Year 3 (32 racks) projections are IMPOSSIBLE for this building.
- Revenue projections must be recalculated against 8-rack maximum.
- 800V DC native via Eaton Beam Rubin DSX
## Corrected Energy Cost
- Natural gas primary: /usr/bin/bash.058-0.068/kWh (recip engines)
- LUS grid is backup only, not primary at /usr/bin/bash.065/kWh