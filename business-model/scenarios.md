# ADC Financial Scenarios — Bear / Base / Bull

## Assumptions Framework

### What We Know (Hard Numbers)
| Input | Value | Source |
|-------|-------|--------|
| Phase 1A power | 3 MW | Willow Glen warehouse |
| Phase 1A power cost | $0.058-0.068/kWh | power-economics.md |
| At-scale power cost | $0.04-0.05/kWh (100+ MW) | power-economics.md |
| Industry CapEx/MW | $8-15M/MW | Industry benchmarks |
| NVL72 rack output | 700M tokens/sec (NVIDIA spec) | GTC 2026 |
| Dynamo boost | 7x inference throughput | GTC 2026 |
| DSX Boost | 85% power → 93% throughput (+30% effective) | DSX architecture |
| MISO ancillary revenue | ~$4M/yr at scale | power-economics.md |
| Hut 8 comp | 245 MW, $454M avg NOI, 15-yr | River Bend |

### What We Estimate (Reasonable Ranges)
| Input | Bear | Base | Bull | Notes |
|-------|------|------|------|-------|
| GPU utilization (Y1) | 30% | 50% | 70% | Industry avg 30%, optimized 70-80% |
| GPU utilization (Y3) | 50% | 70% | 85% | Dynamo + customer ramp |
| Blended token price ($/M) | $0.50 | $1.00 | $2.00 | Weighted across tiers |
| Gross margin | 35% | 55% | 65% | Bear: early ops; Bull: mature Dynamo+Groq |
| Token price deflation | 40%/yr | 25%/yr | 15%/yr | Slowing from historical 10x/yr |
| Phase 1A CapEx | $45M | $35M | $28M | $15M/MW → $8M/MW + DSX efficiency |
| Time to first revenue | 12 months | 8 months | 5 months | From lease signing |

---

## Phase 1A — First Racks (3 MW)

### Power Cost (Annual)
| Scenario | $/kWh | Annual Power Cost |
|----------|-------|-------------------|
| Bear | $0.068 | $1.79M |
| Base | $0.063 | $1.66M |
| Bull | $0.058 | $1.53M |

*Formula: 3 MW × 8,760 hrs × utilization × $/kWh*

### Token Revenue (Annual, Year 1)

**Per-rack math:** NVL72 = 700M tokens/sec baseline. With Dynamo 7x = ~4,900M tokens/sec theoretical. Real-world at utilization:

| Scenario | Util | Effective tokens/sec/rack | $/M tokens | Racks (est) | Annual Revenue |
|----------|------|--------------------------|------------|-------------|----------------|
| Bear | 30% | 1,470M | $0.50 | 3 | $69.7M |
| Base | 50% | 2,450M | $1.00 | 4 | $309M |
| Bull | 70% | 3,430M | $2.00 | 5 | $1.08B |

**CRITICAL NOTE:** These numbers look absurdly high because NVIDIA's 700M tokens/sec spec for NVL72 is a peak marketing number. Real-world throughput with diverse workloads, mixed model sizes, and overhead will be MUCH lower. Until NVIDIA publishes validated per-rack throughput benchmarks for production workloads, these projections should be treated as illustrative only.

### Adjusted Revenue Estimates (Conservative)

Using industry-standard revenue-per-MW benchmarks instead of raw token math:

| Benchmark | Revenue/MW/yr | Source |
|-----------|---------------|--------|
| Hut 8 River Bend (NNN lease) | $1.85M/MW | $454M NOI ÷ 245 MW |
| CoreWeave (BMaaS) | $2-4M/MW | Public filings |
| Managed inference premium | 2-3x BMaaS | Token margin vs GPU rental |
| With Dynamo+Groq optimization | 3-5x BMaaS | ADC thesis |

| Scenario | Revenue/MW/yr | Phase 1A (3 MW) | Notes |
|----------|---------------|-----------------|-------|
| Bear | $2.0M | $6.0M | BMaaS-equivalent, no token premium |
| Base | $4.0M | $12.0M | Managed inference, moderate utilization |
| Bull | $7.0M | $21.0M | Full Dynamo+Groq, high utilization, premium tiers |

### Phase 1A P&L (Annual, Steady State)

| Line Item | Bear | Base | Bull |
|-----------|------|------|------|
| **Revenue** | $6.0M | $12.0M | $21.0M |
| Power | ($1.8M) | ($1.7M) | ($1.5M) |
| Hardware depreciation (5-yr) | ($6.0M) | ($5.0M) | ($4.0M) |
| Staff (5-8 people) | ($0.8M) | ($0.7M) | ($0.6M) |
| Maintenance/software | ($0.5M) | ($0.5M) | ($0.5M) |
| Insurance/overhead | ($0.3M) | ($0.3M) | ($0.3M) |
| **EBITDA** | ($3.4M) | $3.8M | $14.1M |
| **EBITDA margin** | -57% | 32% | 67% |
| **Net (after depreciation)** | ($9.4M) | ($1.2M) | $10.1M |

**Bear case is negative** — this is expected at 3 MW with high CapEx. Phase 1A is a proof-of-concept, not a profit center. The goal is NVIDIA reference site status + first customer + certification.

---

## Phase 1C — Warehouse Maxed (12 MW)

### Power Cost (Annual)
| Scenario | $/kWh | Annual Power Cost |
|----------|-------|-------------------|
| Bear | $0.062 | $6.5M |
| Base | $0.058 | $6.1M |
| Bull | $0.055 | $5.8M |

*Slightly lower $/kWh as solar + battery scale up*

### Revenue & P&L (Annual, Steady State)

| Line Item | Bear | Base | Bull |
|-----------|------|------|------|
| **Revenue** | $24.0M | $48.0M | $84.0M |
| Power | ($6.5M) | ($6.1M) | ($5.8M) |
| Hardware depreciation | ($20.0M) | ($18.0M) | ($16.0M) |
| Staff (12-15 people) | ($1.5M) | ($1.3M) | ($1.2M) |
| Maintenance/software | ($1.5M) | ($1.5M) | ($1.5M) |
| Insurance/overhead | ($0.8M) | ($0.8M) | ($0.8M) |
| **EBITDA** | $13.7M | $38.3M | $74.7M |
| **EBITDA margin** | 57% | 80% | 89% |
| **Net (after depreciation)** | ($6.3M) | $20.3M | $58.7M |

**Base case turns cash-positive** at 12 MW. This is where the model starts working.

---

## Phase 2 — Campus Expansion (50 MW, Year 2-3)

### Power Cost (Annual)
| Scenario | $/kWh | Annual Power Cost |
|----------|-------|-------------------|
| Bear | $0.055 | $24.1M |
| Base | $0.050 | $21.9M |
| Bull | $0.045 | $19.7M |

*CCGT starts to come online at this scale*

### Revenue & P&L (Annual, Steady State)

| Line Item | Bear | Base | Bull |
|-----------|------|------|------|
| **Revenue** | $100M | $200M | $350M |
| Power | ($24M) | ($22M) | ($20M) |
| Hardware depreciation | ($70M) | ($60M) | ($50M) |
| Staff (30-40 people) | ($4M) | ($3.5M) | ($3M) |
| MISO ancillary | $2M | $3M | $4M |
| Maintenance/software | ($5M) | ($5M) | ($5M) |
| Insurance/overhead | ($3M) | ($3M) | ($3M) |
| **EBITDA** | $66M | $169.5M | $323M |
| **EBITDA margin** | 66% | 85% | 92% |
| **Net (after depreciation)** | ($4M) | $109.5M | $273M |

### Hut 8 Comparison (Same Corridor)
| Metric | Hut 8 River Bend | ADC Phase 2 (Base) |
|--------|------------------|-------------------|
| IT Load | 245 MW | 50 MW |
| Investment | $10B | ~$500M |
| Annual NOI | $454M | $169.5M |
| NOI/MW | $1.85M | $3.39M |
| Power source | Entergy grid | On-site gen + grid |
| Model | NNN colo lease | Token factory |

**ADC's NOI/MW is 1.8x Hut 8's** in base case because token factory (managed inference) generates higher margin than NNN colocation leasing.

---

## Phase 3 — Full Campus (100+ MW, Year 3-5)

| Metric | Bear | Base | Bull |
|--------|------|------|------|
| Capacity | 100 MW | 150 MW | 200 MW |
| Revenue | $200M | $600M | $1.4B |
| EBITDA | $130M | $500M | $1.2B |
| EBITDA margin | 65% | 83% | 86% |
| Power cost | $0.045/kWh | $0.042/kWh | $0.040/kWh |
| Staff | 75 | 100 | 125 |
| MISO ancillary | $4M | $6M | $8M |
| Grid export revenue | $2M | $5M | $10M |

---

## Cumulative CapEx by Phase

| Phase | Bear | Base | Bull |
|-------|------|------|------|
| 1A (3 MW) | $45M | $35M | $28M |
| 1B (6 MW) | $35M | $28M | $22M |
| 1C (12 MW) | $60M | $48M | $38M |
| **Phase 1 total** | **$140M** | **$111M** | **$88M** |
| Phase 2 (50 MW) | $400M | $320M | $260M |
| Phase 3 (100+ MW) | $600M | $480M | $400M |
| **Total** | **$1.14B** | **$911M** | **$748M** |

---

## Payback Period

| Scenario | Phase 1A Payback | Phase 1 Payback | Full Campus Payback |
|----------|-----------------|-----------------|---------------------|
| Bear | Never (at 3 MW) | 8-10 years | 7-9 years |
| Base | 5-7 years | 4-5 years | 3-4 years |
| Bull | 2-3 years | 2-3 years | 2-3 years |

**Key insight:** Phase 1A alone doesn't pay back in the bear case. That's OK — Phase 1A exists to get NVIDIA reference status and prove the model. The business makes money at 12+ MW.

---

## Token Price Deflation Sensitivity

Token prices have been falling ~10x/year but are slowing. This is the biggest risk to the model.

| Year | Bear (40%/yr deflation) | Base (25%/yr) | Bull (15%/yr) |
|------|------------------------|---------------|---------------|
| Y1 blended $/M | $0.50 | $1.00 | $2.00 |
| Y2 blended $/M | $0.30 | $0.75 | $1.70 |
| Y3 blended $/M | $0.18 | $0.56 | $1.45 |
| Y5 blended $/M | $0.06 | $0.32 | $1.04 |

**How ADC survives deflation:**
1. **Power cost advantage** — Henry Hub gas doesn't deflate with token prices
2. **Dynamo software gains** — 7x today, improving each release
3. **DSX Boost** — 30% more throughput in same power envelope
4. **Groq decode** — 35x tokens/watt shifts cost curve
5. **Volume explosion** — Jensen's "inference is the engine of intelligence." Token consumption grows faster than prices fall
6. **Move up the stack** — managed AI services (Stream 6) have SaaS margins regardless of underlying token cost

---

## Revenue Stream Mix Over Time

### Year 1 (Phase 1A, 3 MW)
| Stream | Bear | Base | Bull |
|--------|------|------|------|
| Managed Inference | 40% | 50% | 60% |
| Training (BMaaS) | 50% | 35% | 20% |
| Grid Export | 5% | 5% | 5% |
| Pod Sales | 0% | 5% | 10% |
| Heat Recovery | 0% | 0% | 0% |
| Managed AI Services | 5% | 5% | 5% |

### Year 3 (Phase 2, 50 MW)
| Stream | Bear | Base | Bull |
|--------|------|------|------|
| Managed Inference | 45% | 55% | 65% |
| Training (BMaaS) | 30% | 20% | 10% |
| Grid Export | 5% | 5% | 5% |
| Pod Sales | 10% | 10% | 10% |
| Heat Recovery | 2% | 3% | 3% |
| Managed AI Services | 8% | 7% | 7% |

### Year 5 (Phase 3, 100+ MW)
| Stream | Bear | Base | Bull |
|--------|------|------|------|
| Managed Inference | 50% | 55% | 60% |
| Training (BMaaS) | 20% | 15% | 10% |
| Grid Export | 5% | 5% | 5% |
| Pod Sales | 15% | 15% | 15% |
| Heat Recovery | 3% | 3% | 3% |
| Managed AI Services | 7% | 7% | 7% |

---

## Louisiana Tax Incentive Impact

These incentives are NOT included in the P&L above. They stack on top.

| Incentive | Value | Status |
|-----------|-------|--------|
| ITEP (Industrial Tax Exemption) | 80% property tax exempt, 10 yr | Must pre-qualify NAICS code |
| Act 730 (Sales Tax) | 100% exempt, 20 yr ($200M+, 50 jobs) | Eligible at Phase 2 |
| Historic Tax Credits | 25% state + 20% federal | If using existing structures |
| Quality Jobs | $750-1,000/job/yr rebate | 5+ jobs, $18.74/hr min |
| Enterprise Zone | $2,500/job one-time | State + local credits |
| R&D Tax Credit | 30% of qualified spending | UL Lafayette partnership |
| ITC Solar | 30-50% of solar CapEx | Must begin construction by Jul 2026 |

### Combined Tax Impact (Estimated)
| Phase | ITEP (10yr) | Act 730 (20yr) | Solar ITC | Total Savings |
|-------|-------------|----------------|-----------|---------------|
| Phase 1 (12 MW) | $8-16M | N/A (below $200M) | $2-5M | $10-21M |
| Phase 2 (50 MW) | $20-40M | $40-80M | $15-30M | $75-150M |
| Phase 3 (100+ MW) | $40-80M | $80-160M | $30-60M | $150-300M |

---

## Valuation Benchmarks

| Company | Valuation | Revenue Multiple | EBITDA Multiple | Notes |
|---------|-----------|-----------------|-----------------|-------|
| CoreWeave | $71B (2026) | ~30x | ~50x | BMaaS, NVIDIA strategic |
| Nebius | $24B (2025) | ~40x | N/A | Token Factory, NVIDIA $2B |
| Crusoe | $10B+ (2025) | ~25x | N/A | Energy-first, stranded gas |
| Lambda Labs | $2.5B (2024) | ~20x | N/A | BMaaS |

### ADC Implied Valuation (Base Case)
| Milestone | Revenue | Multiple | Implied Value |
|-----------|---------|----------|---------------|
| Phase 1A proof (Y1) | $12M | 15-25x | $180-300M |
| Phase 1C (Y2) | $48M | 15-20x | $720M-$960M |
| Phase 2 (Y3) | $200M | 12-18x | $2.4-3.6B |
| Phase 3 (Y5) | $600M | 10-15x | $6-9B |

*Revenue multiples compress as revenue scales. Early-stage neoclouds command higher multiples.*

---

## Risk Matrix

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| NVIDIA rack pricing higher than expected | CapEx +30-50% | Medium | DSX partner pricing vs list |
| Token price deflation faster than 25%/yr | Revenue below base | High | Energy moat, move up stack |
| Vera Rubin NVL72 delayed past H2 2026 | Revenue delayed 6-12 months | Low | Start with Blackwell B300 |
| ITEP NAICS code rejected | Lose $8-16M incentive | Medium | Pre-qualify with LED now |
| WGT lease terms unfavorable | CapEx +$5-10M | Medium | Revenue share structure |
| Low utilization Y1 (<30%) | Revenue below bear | Medium | Anchor tenant LOI first |
| Grid interconnect issues | Power cost +20% | Low | 230kV substation already live |
| Groq 3 LPX delayed | Lose decode advantage | Medium | GPU-only inference still works |
| Competition (Hut 8, others) | Pricing pressure | High | Speed, power cost, NVIDIA relationship |

---

## What Unlocks Better Numbers

1. **NVIDIA rack pricing** — Cannot finalize CapEx without this. Blocks entire financial model precision.
2. **Anchor tenant LOI** — De-risks utilization assumption. Changes everything.
3. **ITEP pre-qualification** — $8-16M swing. Call Kristin Johnson.
4. **Entergy rate negotiation** — Could drop Phase 1 power cost 10-15%.
5. **Solar EPC pricing** — From today's meeting. Fills Layer 2 cost gap.
6. **Vera Rubin throughput benchmark** — Real tokens/sec per rack under production workloads.
