# ADC Token Economics — Pricing, Margins, Market Position

## The Market (Early 2026)

### Closed-Model API Pricing ($/M Tokens)
| Provider | Model | Input | Output |
|----------|-------|-------|--------|
| OpenAI | GPT-4o | $2.50 | $10.00 |
| OpenAI | GPT-4o-mini | $0.15 | $0.60 |
| Anthropic | Claude Opus 4.6 | $5.00 | $25.00 |
| Anthropic | Claude Sonnet 4.6 | $3.00 | $15.00 |
| Anthropic | Claude Haiku 4.5 | $1.00 | $5.00 |
| Google | Gemini 2.5 Pro | $1.25 | $10.00 |
| Google | Gemini Flash | $0.30 | $2.50 |

### Open-Model Inference Pricing ($/M Tokens)
| Provider | Model | Input | Output |
|----------|-------|-------|--------|
| Groq Cloud | Llama 3.3 70B | $0.59 | $0.59 |
| Together AI | Llama 3.1 70B | $0.88 | $0.88 |
| Together AI | Llama 4 Maverick | $0.27 | $0.27 |
| Fireworks AI | Qwen3 8B | $0.20 | $0.20 |
| DeepInfra | Nemotron 3 Nano 30B | $0.05 | $0.20 |
| DeepInfra | Nemotron 3 Super 120B | $0.10-0.30 | $0.50-0.75 |

### GPU Rental Market ($/GPU-hr, H100)
| Provider | H100 SXM | Notes |
|----------|----------|-------|
| RunPod | $2.69 | 40-60% cheaper than AWS |
| Lambda Labs | $2.99 | 8xH100 @ $23.92/hr |
| CoreWeave | ~$6.15 | 8xH100 HGX @ $49.24/hr |
| AWS (reference) | ~$3.50-4.00 | Hyperscaler baseline |

**Key finding:** H100 has stabilized at $2.85-3.50/hr across competitive vendors. Neoclouds are 40-60% cheaper than cloud giants.

---

## Raw Cost Floor

| Metric | Value | Notes |
|--------|-------|-------|
| Raw compute cost (14B model, full util) | ~$0.004/M tokens | Hardware depreciation only |
| Industry average GPU utilization | 15-50% (avg 30%) | Massive stranded capacity |
| Optimized inference cluster (Dynamo) | 70-80% utilization | vLLM, PagedAttention, continuous batching |
| Total efficiency gain since 2023 | ~1,000x | Hardware + software + quantization compound |

**The gap:** Raw compute costs ~$0.004/M tokens. Retail pricing is $0.10-$2.50/M. Even at aggressive pricing, gross margins exceed 95%.

---

## ADC's Advantage: Dynamo + Groq

### NVIDIA Dynamo 1.0
- 7x performance boost on Blackwell/Vera Rubin (software alone: 700 → 5,000 tokens/sec)
- Disaggregated inference: GPU handles prefill (compute-heavy), Groq handles decode (bandwidth-optimized)
- Open-source inference OS — no licensing cost

### Groq 3 LPX Decode Economics
| Metric | Value |
|--------|-------|
| Compute | 1.2 PF FP8 |
| Memory bandwidth | 150 TB/s (7x Vera Rubin) |
| On-chip SRAM | 500 MB |
| Throughput per watt | 35x vs prior gen |
| Revenue potential per MW | 10x vs GPU-only |
| Status | Samsung fab, Q3 2026 expected |

**ADC strategy:** Vera Rubin handles prefill + storage fabric. Groq handles decode at 35x tokens/watt. Dynamo orchestrates both. ~25% capacity allocated to Groq LPX.

---

## ADC Pricing Framework (Recommended)

| Tier | $/M Tokens | Target Workload | Gross Margin |
|------|-----------|-----------------|--------------|
| Batch | $0.20 | Dev, non-urgent, async | ~98% |
| Standard | $1.00 | General inference | ~99% |
| Premium | $6.00 | Real-time agents, low-latency | ~99% |
| Enterprise | $45.00 | Mission-critical, 99.99% SLA | ~98% (ops overhead) |
| Real-time Interactive | $150.00 | <50ms latency (Groq decode) | ~97% (premium LPU) |

**Positioning:** Undercut OpenAI ($2.50) but above Groq ($0.59) for mid-market enterprises seeking reliability + governance + confidential computing.

### Output Tokens Are the Profit Center
- Input pricing: $0.10-$1.00/M (low margin relative to output)
- Output pricing: $0.40-$25.00/M (3-8x markup over input)
- Enterprise RAG = input-heavy (lower margin)
- Agentic reasoning = output-heavy (premium margin)
- Reasoning models use 10-100x internal tokens per query (hidden cost enterprises underestimate)

---

## Enterprise Token Consumption Benchmarks

| Workload | Monthly Volume | Cost at $1.00/M | Notes |
|----------|---------------|------------------|-------|
| Customer support agent | 50M-500M | $50K-$500K | 10K daily chats |
| Coding assistant | 100M-1B | $100K-$1M | Per developer team |
| Knowledge base RAG | 10M-100M | $10K-$100K | Low-latency retrieval |
| Agentic reasoning | 1B-10B | $1M-$10M | Reasoning tokens 10-100x query |

**Token-to-words:** 1 token = ~0.75 words. 1,000-word doc = ~1,300-1,500 tokens.

---

## Revenue Projections by Utilization

### Per NVL72 Rack (Vera Rubin)
Assumptions: Dynamo 7x boost, 70% utilization, blended $1.50/M tokens

| Utilization | Tokens/sec (est) | Monthly Revenue (est) | Annual Revenue (est) |
|-------------|------------------|-----------------------|----------------------|
| 50% | 2,500 | TBD (need rack throughput) | TBD |
| 70% (base case) | 3,500 | TBD | TBD |
| 85% (bull case) | 4,250 | TBD | TBD |

**Blocking item:** Cannot calculate per-rack revenue without Vera Rubin NVL72 throughput specs (tokens/sec per rack). NVIDIA hasn't published this for Vera Rubin yet.

---

## Competitive Landscape

| Provider | Model | Positioning | Margin Strategy |
|----------|-------|-------------|-----------------|
| OpenAI | GPT-4o | Closed, quality premium | Ultra-high (99%+), brand tax |
| Groq | Native LPU | Speed + cost leader | Aggressive ($0.59), high volume |
| DeepSeek | R1 + open | Reasoning at scale | 80% margins at low price |
| Anthropic | Claude | Reasoning + safety | Mid-tier ($3-5) |
| Google | Gemini | Multimodal + caching | Mid-tier ($0.30-$1.25) |
| CoreWeave | BMaaS + managed | GPU rental + inference | Lower margin (14-16% BMaaS) |
| Nebius | Token Factory | 60+ models, 70% cost improvement | Volume play |

### 2027 Outlook
- Token prices continue 3-5x annual reduction (slowing from 10x)
- Inference = 85% of enterprise AI spend (training is commodity)
- $1+ trillion inference market (Jensen Huang, GTC 2026)
- Winners: providers with power + compliance + real-time SLA + agentic AI
- Losers: generic BMaaS / hourly GPU rentals (margin collapse)

---

## Key Insights for ADC

1. **Margin floor is ~$0.004/M, but service delivery costs 10-100x more.** Smart providers maintain 70-90% margins even at $0.10/M by automating compliance and running Dynamo at 70%+ utilization.

2. **Output tokens are the profit center.** Input is cheap, output is 3-8x markup. Agentic workloads (output-heavy) are where the money is.

3. **GPU utilization is the real moat.** Industry average 30%, optimized 70-80%. At 2.5x utilization, ADC's cost floor drops from $0.004 to $0.0016/M.

4. **Power efficiency (tokens/watt) beats GPU cost.** Vera Rubin does 10x throughput/MW. Groq does 35x vs prior gen. ADC's renewable power stack means ADC can afford 25% Groq capacity while competitors can't.

5. **The LLM Cost Paradox = opportunity.** Prices dropped 10x, usage up 100x. Enterprises can't control costs. ADC offers token budgeting + transparent reasoning cost + per-request caps as premium features.

6. **Reasoning models break traditional economics.** o1/o3/Claude Opus internal reasoning eats 10-100x tokens per query. Enterprise must budget for hidden cost or face surprise bills. ADC positions as "transparent token economics."

7. **ADC should NOT compete on price alone.** Compete on: energy cost advantage, confidential computing (BlueField-4 + NemoClaw), Louisiana tax incentives (lower OpEx), and real-time SLA (Groq decode).

---

## What's Still Needed
1. Vera Rubin NVL72 throughput specs (tokens/sec per rack)
2. Groq 3 LPX per-unit pricing
3. Dynamo 7x — validated throughput on Vera Rubin (not just Blackwell)
4. ADC blended power cost (see power-economics.md)
5. Staffing model for managed inference operations
6. Per-rack revenue calculation once specs are available
