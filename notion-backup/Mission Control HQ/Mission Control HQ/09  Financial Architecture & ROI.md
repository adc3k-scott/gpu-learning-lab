# 09 — Financial Architecture & ROI
*Notion backup — 2026-04-03*

> This is not an AI factory. This is a money machine. Every watt generates revenue. Every dollar goes to compute. The comparison is not close.
---
## Capital Stack
- Infrastructure raise: ~$1.17M — covers facility buildout (electrical, cooling, fiber, power distribution, commissioning)
- GPU hardware financed separately: equipment financing + NVIDIA Capital programs + SBA facilities
- EBITDA figures below = facility-level operating cash flow
- Full investor pro forma with hardware financing and debt service available upon request
---
## MARLIE I vs Legacy AI Factory — Key Comparison
- PUE: Legacy 1.4-1.8 (40-80% wasted) vs MARLIE I 1.10 (liquid-cooled, best-in-class)
- Energy cost: Legacy $0.10-0.18/kWh national avg vs MARLIE I $0.058-0.068/kWh (Bloom SOFC on Henry Hub gas)
- Cooling: Legacy air (CRAC units, chillers) vs MARLIE I 100% direct-to-chip liquid
- Revenue per rack per year: Legacy $200K-$500K (colo) vs MARLIE I $3M-$5M+ (AI compute)
- Operations: Legacy 20-50 FTE manual ops vs MARLIE I 3-5 FTE Mission Control AI
- On-site generation: Legacy none (grid dependent) vs MARLIE I 40 Bloom SOFC units, 10 MW
- Domestic content: Legacy mixed overseas vs MARLIE I 100% USA — OBBBA compliant
---
## MARLIE I Configuration
> 40 NVL72 racks — 2,880 Rubin GPUs — 5,200 kW IT — 10 MW Bloom generation
- Building downstairs: 10 racks, 720 GPUs, 1,300 kW IT — single-row layout, same as pod
- Building upstairs: NOC only — no compute racks
- Pod 1: 10 racks, 720 GPUs, 1,300 kW IT
- Pod 2: 10 racks, 720 GPUs, 1,300 kW IT
- Pod 3: 10 racks, 720 GPUs, 1,300 kW IT
---
## Revenue Model — AI Compute Rental (Conservative Basis)
Rate basis: $6/GPU/hr base case (H100 spot: $2.50-$3.50/hr; Rubin delivers 2.5x FP4 density and 22 TB/s HBM4 bandwidth — premium tier justified). At $8/GPU/hr mid estimate, Phase 3 gross reaches $151.6M.
### Phase 1 — Building Downstairs (720 GPUs, 10 Racks)
- 720 GPUs online — building downstairs only
- 40% utilization (ramp year): 720 x $6 x 8,760 x 0.40 = $15.2M gross
- 65% utilization (stabilized): 720 x $6 x 8,760 x 0.65 = $24.7M gross
- OPEX at 65%: ~$2.8M (Bloom fuel + staffing + maintenance)
- EBITDA at 65%: ~$21.9M
### Phase 2 — Building + Pod 1 (1,440 GPUs, 20 Racks)
- 1,440 GPUs online — building + Pod 1
- 65% utilization: 1,440 x $6 x 8,760 x 0.65 = $49.3M gross
- OPEX: ~$4.5M
- EBITDA: ~$44.8M
### Phase 3 — Full Footprint (2,880 GPUs, 40 Racks)
- 2,880 GPUs online — building + all 3 pods
- 75% utilization at $6/hr: 2,880 x $6 x 8,760 x 0.75 = $113.7M gross
- 75% utilization at $8/hr: 2,880 x $8 x 8,760 x 0.75 = $151.6M gross
- OPEX: ~$7.0M
- EBITDA at $6/hr: ~$106.7M
- EBITDA at $8/hr: ~$144.6M
---
## Power Resilience — 5 Independent Layers
> Bloom SOFC is PRIMARY. The grid is never used for consumption at MARLIE I.
1. Solar (Offset): 300 kW — First Solar TR1 — pod roofs + Chag Street ground mount
1. Bloom SOFC (Primary): 40 units x 250 kW = 10 MW — 800V DC direct — gas in, DC out — 54% efficiency
1. LFP Battery (Bridge): 600 kWh Eaton xStorage — millisecond ATS — ride-through
1. Diesel Genset (Emergency): on-site fuel reserve — hurricane insurance — zero production dependency
1. Grid (Never): LUS emergency backup only — not used for consumption — no sell-back at MARLIE I
Zero single points of failure. 5 independent power layers. Bloom headroom: ~4,280 kW above full facility draw.
---
## Power Economics
- Bloom SOFC effective cost: $0.058-0.068/kWh (fuel + maintenance, Henry Hub gas basis)
- IT load: 5,200 kW — facility total at PUE 1.10: ~5,720 kW
- Bloom generation: 10,000 kW — headroom buffer: ~4,280 kW
- Annual power cost at Phase 3 / 75% utilization: ~$2.4M
---
## Investor Benefits
- Reserved bandwidth: GPU compute access during off-peak hours proportional to investment tier. Estimated value: $50K-$500K/month compute credit.
- Early mover rate lock: investors before first rack goes live receive locked GPU rental rates below market for 24 months
- Single operator: Scott pulls GC permits, handles NVIDIA integration, runs Mission Control — no markup, no middlemen, revenue from day one