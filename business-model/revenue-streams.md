# ADC Revenue Streams

## Stream 1: Managed Inference (TOKEN FACTORY) — PRIMARY
**What:** Sell optimized tokens via NVIDIA Dynamo + Groq LPX decode
**How:** GPU handles prefill (heavy reasoning), Groq handles decode (fast output). Dynamo orchestrates both. Best price per token in the market.
**Margin advantage:** Software margin on top of hardware. Not commodity GPU rental.
**Pricing model:** $/million tokens (input + output), tiered by model size and latency SLA

### Unit Economics (NEEDS WORK)
- Revenue per rack per month: TBD
- Dynamo 7x inference boost = 7x more tokens from same hardware
- Groq 35x tokens/watt on decode = massive cost advantage on output tokens
- Target gross margin: 60-70% (vs 14-16% for pure BMaaS)
- Utilization assumption: 70% base case

### Comps
- Nebius "Token Factory" launched Nov 2025: 60+ models, 70% cost/latency improvement
- CoreWeave GPU-hour pricing: ~$2.50-3.50/GPU-hr for H100
- OpenAI API pricing: $15/M input tokens, $60/M output tokens (GPT-4o)
- Anthropic API pricing: $15/M input tokens, $75/M output tokens (Claude Opus)
- Open model inference (Nemotron, Llama): significantly cheaper per token

### Key Questions
- [ ] What's ADC's target $/M tokens for open model inference?
- [ ] What utilization rate is realistic for Year 1 vs Year 3?
- [ ] What's the rack-level revenue at 70% utilization?
- [ ] How does Dynamo 7x translate to actual $/token cost reduction?

---

## Stream 2: Training Capacity (BMaaS) — SECONDARY
**What:** Bare metal GPU rental for large model training contracts
**How:** Standard NVL72 rack rental by the hour/month. Enterprise training workloads.
**Margin:** Lower (14-16% net after power, labor, depreciation)
**Why still do it:** Fills capacity when inference demand is low. Anchor tenant revenue.

### Unit Economics (NEEDS WORK)
- Revenue per GPU-hour: ~$2.50-3.50 (H100 equivalent, Vera Rubin TBD)
- Revenue per rack per month at 70% util: TBD
- Contract structure: monthly/quarterly/annual commitments

### Key Questions
- [ ] What's the Vera Rubin NVL72 GPU-hour equivalent pricing?
- [ ] What % of capacity allocated to training vs inference?
- [ ] What anchor tenant pipeline exists?

---

## Stream 3: Grid Power Export — TERTIARY
**What:** Sell surplus power back to Entergy grid via 230kV bidirectional substation
**How:** When on-site generation (solar + gas) exceeds compute load, export to grid
**Also:** Grid ancillary services (frequency regulation, demand response) via Siemens Omnivise

### Unit Economics (NEEDS WORK)
- Grid export rate: TBD (Entergy buyback rate for Louisiana)
- Ancillary service revenue: $50-150K/year (from Siemens research)
- Peak shaving value: TBD
- DSX Flex angle: AI factory as grid-flexible asset (NVIDIA concept)

### Key Questions
- [ ] What's Entergy's buyback rate for industrial generation in Iberville Parish?
- [ ] What ancillary service programs are available (MISO market)?
- [ ] What's the realistic surplus generation capacity?

---

## Stream 4: ADC 3K Facility Module Sales — PRODUCT LINE
**What:** Sell manufactured DSX-compliant facility modules to other operators
**How:** ADC builds containerized enclosures that receive NVIDIA liquid-cooled racks. Sold as a product.
**Target buyers:** Other neoclouds, enterprise on-prem, edge deployment operators

### Unit Economics (NEEDS WORK)
- Cost per pod: TBD (container + MEP + water loop + heat rejection)
- Sale price per pod: TBD
- Margin: TBD
- Production capacity: Baton Rouge Terminal (Phase 1) + New Iberia automated (Phase 2)

### Key Questions
- [ ] What's the BOM for a DSX-compliant facility module?
- [ ] What's the target sale price?
- [ ] Who are the first 3 customers?
- [ ] What's the production timeline?

---

## Stream 5: Heat Recovery — FUTURE
**What:** Sell waste heat from NVIDIA liquid cooling (45C hot water) for secondary use
**How:** ORC (Organic Rankine Cycle) for electricity, district heating, industrial process heat
**Status:** Concept only. No engineering or customer pipeline.

### Key Questions
- [ ] What's the thermal output per rack at 45C?
- [ ] What industrial heat users are near Willow Glen?
- [ ] What's ORC economics at this temperature range?

---

## Stream 6: Managed AI Services (LOCAL/REGIONAL) — FUTURE
**What:** Set up and manage AI agents for local businesses on ADC compute
**How:** NemoClaw/OpenClaw privacy router + simple interface. ADC does the heavy lifting. Client gets a simplified dashboard.
**Model:** Monthly subscription per business. Low compute per client, high margin, recurring.
**Workforce:** UL Lafayette students build agents, ADC runs compute, businesses get service.

### Unit Economics (NEEDS WORK)
- Compute cost per small business client: minimal (inference only, shared capacity)
- Monthly subscription: $500-5,000/mo depending on complexity
- Setup fee: $2,000-10,000 one-time
- Margin: 70-80% (compute cost is negligible per client)
- Confidential computing angle: data never leaves ADC hardware boundary

### Key Questions
- [ ] What are the first 3 use cases? (scheduling, inventory, document processing, customer service?)
- [ ] What's the minimum viable product?
- [ ] How does this scale without custom engineering per client?

---

## Revenue Mix Target (Year 3)
| Stream | % of Revenue | Status |
|--------|-------------|--------|
| Managed Inference (tokens) | 50% | Primary focus |
| Training (BMaaS) | 25% | Anchor tenant revenue |
| Grid Power Export | 5% | Passive income |
| Facility Module Sales | 15% | Product line |
| Heat Recovery | 0% | Future |
| Managed AI Services | 5% | Growing |

---

## What We Need to Build the Financial Model
1. **Vera Rubin NVL72 rack pricing** — NVIDIA hasn't published. Critical for CapEx.
2. **Token pricing benchmarks** — what are neoclouds charging per M tokens for open models?
3. **Power cost model** — blended $/kWh across all 4 layers (see power-economics.md)
4. **Utilization ramp** — realistic month-by-month from first rack to Phase 1C
5. **Staffing model** — headcount and cost by phase
6. **Depreciation schedule** — GPU hardware lifecycle (3-5 years)
