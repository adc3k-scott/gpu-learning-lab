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

## Realistic Margin Analysis

**Raw compute cost ($0.004/M tokens) is misleading.** Operational margins include depreciation, power, staffing, MLOps, support, and SLA overhead.

| Business Model | Gross Margin | Notes |
|----------------|-------------|-------|
| BMaaS (bare metal GPU rental) | 55-65% | Declining due to H100 price collapse (60-75% from peak) |
| Managed inference (early stage) | ~25% | Unoptimized infra, experimental pricing |
| Managed inference (mature) | ~60% | Custom models, refined pricing, optimized stack |
| Traditional SaaS (benchmark) | 80-90% | What investors expect |
| AI-native companies (average) | 50-60% | General range across sector |

**ADC target: 60% gross margin at maturity** (managed inference via Dynamo + Groq decode). The energy-first model (Henry Hub gas) is what sustains margins as token prices deflate ~10x/year.

---

## ADC Pricing Framework (Recommended)

| Tier | $/M Tokens | Target Workload |
|------|-----------|-----------------|
| Batch | $0.20 | Dev, non-urgent, async |
| Standard | $1.00 | General inference |
| Premium | $6.00 | Real-time agents, low-latency |
| Enterprise | $45.00 | Mission-critical, 99.99% SLA |
| Real-time Interactive | $150.00 | <50ms latency (Groq decode) |

**Positioning:** Price between commodity open-model floor ($0.13-$0.25 input) and Groq speed-premium ($0.50+ input). Capture latency advantage margin.

**Closest comp: Nebius** — literally calling their product "Token Factory." NVIDIA $2B investment. Will get Vera Rubin NVL72 in H2 2026. Pricing Llama 3.3 70B at $0.13/$0.40 (base tier).

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
| OpenAI | GPT-5 ($1.25/$10) | Closed, quality premium | Brand tax, high volume |
| Groq | Native LPU | Speed + cost leader | Aggressive ($0.11-$0.59), latency premium |
| **Nebius** | **Token Factory** | **Closest ADC comp** | **$0.13/$0.40 base, NVIDIA $2B invested, Vera Rubin H2 2026** |
| DeepSeek | R1 + open | Reasoning at scale | Aggressive pricing |
| Anthropic | Claude | Reasoning + safety | Mid-tier ($3-5) |
| Google | Gemini | Multimodal + caching | Mid-tier ($0.30-$1.25) |
| CoreWeave | BMaaS + managed | GPU rental + inference | 55-65% gross (BMaaS), declining |

### 2027 Outlook
- Token prices continue 3-5x annual reduction (slowing from 10x)
- Inference = 85% of enterprise AI spend (training is commodity)
- $1+ trillion inference market (Jensen Huang, GTC 2026)
- Winners: providers with power + compliance + real-time SLA + agentic AI
- Losers: generic BMaaS / hourly GPU rentals (margin collapse)

---

## Key Insights for ADC

1. **Realistic margins are 25-60%, not 95%.** Raw compute ($0.004/M) ignores depreciation, power, staffing, MLOps, support. Target 60% gross at maturity with Dynamo + Groq optimization.

2. **Nebius is the closest competitor.** Same "Token Factory" branding, NVIDIA $2B invested, getting Vera Rubin H2 2026. ADC differentiates on: energy cost (Henry Hub), confidential computing, Louisiana incentives.

3. **Output tokens are the profit center.** Input is cheap, output is 3-8x markup. Agentic workloads (output-heavy) are where the money is.

4. **GPU utilization is the real moat.** Industry average 30%, optimized 70-80%. At 2.5x utilization, ADC's cost-per-token drops proportionally.

5. **Token prices deflate ~10x/year.** GPT-4-equivalent performance now costs $0.40/M vs $20 in late 2022. Energy-first model (Henry Hub gas) is the moat that survives deflation.

6. **BMaaS is a race to the bottom.** H100 rental prices collapsed 60-75% from peak. BMaaS margins (55-65%) are structurally declining. Managed inference is the play.

7. **Speed-premium pricing works.** Groq charges more for LPU inference ($0.50+ vs $0.13 for same model elsewhere). ADC's Groq 3 LPX decode enables similar premium positioning.

8. **ADC should NOT compete on price alone.** Compete on: energy cost advantage, confidential computing (BlueField-4 + NemoClaw), Louisiana tax incentives (lower OpEx), and real-time SLA (Groq decode).

---

## What's Still Needed
1. Vera Rubin NVL72 throughput specs (tokens/sec per rack)
2. Groq 3 LPX per-unit pricing
3. Dynamo 7x — validated throughput on Vera Rubin (not just Blackwell)
4. ADC blended power cost (see power-economics.md)
5. Staffing model for managed inference operations
6. Per-rack revenue calculation once specs are available
