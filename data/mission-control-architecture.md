# Mission Control Architecture

> ADC's Complete AI Factory Operating System
> Version 1.0 | March 25, 2026 | Classification: Internal -- ADC Engineering

---

## 1. System Overview

Mission Control is ADC's AI factory operating system -- the software stack that turns GPU hardware and power into sellable tokens, managed inference, and autonomous agent services.

### 5-Tier Architecture

```
                    CUSTOMERS / INTERNAL OPS
                           |
                    [Mission Control API]
                    (FastAPI + Auth + Billing)
                           |
        +------------------+------------------+
        |          |           |        |      |
     Tier 1     Tier 2     Tier 3   Tier 4  Tier 5
     Premium    Operations  Token    Edge   Security
      Brain      Brain     Factory          Layer
    (Claude)  (Self-Hosted) (Dynamo) (Jetson) (Guardrails)
```

**Self-hosted on ADC's own NVL72 hardware.** MARLIE 1 is the first deployment site (Lafayette command center). Expands to Trappeys (solar AI factory, proof-of-concept) and Willow Glen (SuperPOD, primary hub).

**ADC is its own first customer.** AI Advantage (SMB business), Ally chatbot, daily briefings, Notion sync, GPU monitoring, investor analysis -- all run on this stack before a single external token is sold.

### Infrastructure Layer (under all tiers)

The NVIDIA Cloud-Native Stack runs beneath every tier:

```
TOKEN SALES (customer-facing API)
    |
NVIDIA Dynamo 1.0 (inference orchestration)
    |
NVIDIA NIM Operator (model serving on K8s)
    |
Run:AI (scheduling + multi-tenant management)
    |
NVIDIA GPU Operator + Network Operator (GPU + InfiniBand lifecycle)
    |
NVIDIA Container Toolkit (GPU container runtime)
    |
Kubernetes (cluster orchestration)
    |
NVIDIA Base Command Manager (cluster provisioning)
    |
NVL72 HARDWARE (72 Blackwell GPUs, NVLink 5, 1,800 GB/s)
```

Source playbooks: `adc3k-deploy/vendors/nvidia/cloud-native-stack.md`, `gpu-operator-playbook.md`, `network-operator-playbook.md`, `inference-serving-playbook.md`, `runai-deployment-guide.md`

---

## 2. Tier 1 -- Premium Brain (Claude API)

**Purpose:** Complex reasoning, investor-facing analysis, multi-step research, document generation, strategic decisions.

| Attribute | Detail |
|-----------|--------|
| Provider | Anthropic (external API) |
| Model | Claude Opus 4.6 (1M context) |
| Hosting | Anthropic cloud -- NOT self-hosted |
| Cost | API per-call (~$500-2,000/month depending on usage) |
| Latency | Variable (network + queue time) |
| Context | 1M tokens (~78% match ratio at 1M, best in class) |

**When to route here:**
- Multi-step research across dozens of sources
- Investor pitch generation and strategic analysis
- Document drafting that requires nuanced judgment
- Code review and architecture decisions
- Anything where quality matters more than cost

**Why external:** Claude's reasoning quality on hard tasks exceeds what open models deliver today. For mission-critical outputs (investor decks, legal analysis, architecture design), the API cost is negligible compared to the value of getting it right. This tier shrinks over time as open models improve.

**Current integration:** Already running in `main.py` via `anthropic_async_client`. The FastAPI server uses Claude for `/chat/stream`, task planning (LLM fallback in orchestrator), and news analysis (NewsScoutAgent).

---

## 3. Tier 2 -- Operations Brain (Self-Hosted)

**Purpose:** ADC's internal operations -- GPU monitoring, customer support (Ally chatbot), daily briefings, Notion sync, knowledge queries, internal agent workflows.

### Model Selection

| Candidate | Params (Total/Active) | License | Benchmark | Status |
|-----------|-----------------------|---------|-----------|--------|
| **Qwen 3 235B** | 235B dense | Apache 2.0 | AIME 2025: 92.3, Arena: 1422 | ADC PRIMARY PICK |
| **DeepSeek-V3.2** | 671B / ~37B active (MoE) | MIT | AIME: 89.3, Arena: 1421 | ALTERNATE -- 30x throughput on NVL72 w/ Dynamo |
| **Nemotron Ultra 253B** | 253B | NVIDIA Open | Solid all-around | NVIDIA-native fallback |

**Decision:** Start with Qwen 3 235B for quality. Switch to DeepSeek-V3.2 if throughput demands exceed single-model capacity (MoE architecture gets 30x request throughput via Dynamo disaggregated serving on NVL72).

### Deployment

- **Serving:** NIM microservice on dedicated MIG partition (hardware-isolated from customer workloads)
- **Fine-tuning:** LoRA via NeMo Customizer on NVL72 at MARLIE 1
- **Training data:** All memory files, vendor specs, playbooks, conversation history, Notion exports
- **Refresh:** Re-fine-tune monthly as knowledge base grows
- **Validation:** Test against known Q&A pairs from ADC domain before promoting new weights

### RAG Pipeline (feeds Tier 2)

| Component | Choice | License | Why |
|-----------|--------|---------|-----|
| Orchestration | LlamaIndex | MIT | Best for document-heavy RAG, tight indexing |
| Vector DB | Milvus | Apache 2.0 | Cheapest at scale (~$500/mo for 10M vectors), hybrid search |
| Embeddings | NV-Embed-v2 (7B) | NVIDIA | #1 MTEB overall, 62% Top-1 accuracy, NIM-native |
| Reranking | NV-Rerank via NIM | NVIDIA | Improves retrieval precision |
| Chunking | 512 tokens, 50-token overlap | -- | Standard for technical docs |
| Retrieval | Top-5 chunks by cosine similarity | -- | Balance recall vs. context window |
| Update freq | Daily (new documents auto-indexed) | -- | Cron job scans repo + Notion |

**Document sources:**
- All `.md` files from `gpu-learning-lab` repo (memory/, data/, adc3k-deploy/vendors/)
- Notion workspace export (all pages + databases)
- Vendor spec sheets and playbooks
- Conversation logs (instruction/response pairs for fine-tuning)

### Agent Framework

- **Primary:** NVIDIA AgentIQ (Apache 2.0) -- NIM-native, real-time telemetry, dynamic inference, open source
- **Custom layer:** Mission Control's existing agent framework (BaseAgent + OrchestratorAgent + skill dispatch) handles operational control, job/step state machines, pub/sub event bus
- **AgentIQ integration:** AgentIQ profiling data feeds into existing watchdog and metrics collector
- **NemoClaw (watch):** NVIDIA's autonomous agent platform (OpenClaw + Nemotron). Early preview since GTC 2026. Could become the foundation for ADC's managed agent offering.

### Guardrails (applied to Tier 2 + Tier 3)

| Layer | Tool | Function |
|-------|------|----------|
| Orchestration | NeMo Guardrails (Apache 2.0) | Topic control, PII detection, jailbreak prevention, RAG grounding checks |
| Classifier | Nemotron-Safety-Guard-8B-v3 (NVIDIA Open) | 23 safety categories, 20+ languages, reasoning-capable (v0.20.0) |

Both self-hosted, NVIDIA-native, run on NIM. Deployed as sidecar to every inference endpoint.

### Cost

$0 marginal cost per query. Hardware is sunk cost (NVL72 racks already purchased for customer workloads). Tier 2 runs on a dedicated MIG partition that would otherwise be idle.

---

## 4. Tier 3 -- Token Factory (Customer-Facing)

**Purpose:** Production inference serving for paying customers. This is ADC's primary revenue engine.

### Inference Engine

**NVIDIA Dynamo 1.0** -- non-negotiable. Open source (Apache 2.0, github.com/ai-dynamo/dynamo).

| Feature | Detail |
|---------|--------|
| Architecture | Distributed inference OS -- orchestrates GPU + memory across entire cluster |
| Backends | SGLang, TensorRT-LLM, vLLM |
| Key capability | Disaggregated serving -- separates prefill from decode across GPUs |
| NVL72 performance | DeepSeek-R1: 30x more requests. MoE models: 50x throughput vs Hopper. |
| Blackwell boost | 7x inference performance |
| Agentic routing | Priority-based routing, KV cache pinning across agent steps |
| Multimodal | Disaggregated encode/prefill/decode, embedding cache |
| Cold start | ModelExpress: 7x faster via checkpoint restore + weight streaming over NVLink (NIXL) |

**Three standalone building blocks:**

| Component | Function |
|-----------|----------|
| KVBM (KV Block Manager) | Multi-tier KV cache: GPU HBM -> CPU DRAM -> NVMe SSD -> Remote storage. Cost-aware eviction. |
| NIXL (Inference Xfer Library) | Low-latency point-to-point data transfer between GPUs and across memory tiers |
| Grove | Kubernetes-native gang scheduling with topology awareness for multi-node inference |

### Model Catalog (available to customers)

#### Reasoning / General

| Model | Params (Total/Active) | License | Strength |
|-------|-----------------------|---------|----------|
| Qwen 3 235B | 235B dense | Apache 2.0 | Best all-around open model |
| Qwen 3.5 397B-A17B | 397B / 17B MoE | Apache 2.0 | Highest GPQA Diamond (88.4) |
| DeepSeek-V3.2 | 671B / ~37B MoE | MIT | 30x throughput on NVL72 w/ Dynamo |
| DeepSeek-R1 | 671B / 37B MoE | MIT | Chain-of-thought reasoning specialist |
| Llama 4 Scout | 109B / 17B MoE | Llama | 10M context, multimodal, fits single GPU |
| Llama 4 Maverick | ~400B / 17B MoE | Llama | Beats GPT-4o on multimodal |
| Nemotron Ultra 253B | 253B | NVIDIA Open | NVIDIA-native, zero-friction NIM deploy |
| Nemotron Super 49B | 49B | NVIDIA Open | Best throughput/accuracy ratio |

#### Coding

| Model | Params (Total/Active) | License | Strength |
|-------|-----------------------|---------|----------|
| Qwen3-Coder 480B-A35B | 480B / 35B MoE | Apache 2.0 | 256K-1M context, repo-scale code |
| Kimi-Dev-72B | 72B | MIT | Top SWE-Bench among open models |
| Qwen3-Coder-Next | 80B / 3B MoE | Apache 2.0 | Edge-viable, matches 10-20x larger models |

#### Multimodal / Vision

| Model | Params | License | Strength |
|-------|--------|---------|----------|
| GLM-4.5V | 106B / 12B MoE | Open | Best open VLM, 66K context |
| Qwen2.5-VL-32B | 32B | Apache 2.0 | MMMU 70.2, strong visual reasoning |
| Pixtral 12B | 12B | Apache 2.0 | Camera/surveillance workloads |

#### Voice

| Model | Type | Params | License |
|-------|------|--------|---------|
| NVIDIA Canary Qwen 2.5B | STT | 2.5B | NVIDIA |
| Orpheus 3B | TTS | 3B | Apache 2.0 |
| Fish Speech V1.5 | TTS | ~500M | Apache 2.0 |
| Kokoro | TTS | 82M | Apache 2.0 |

Full model catalog with benchmarks: `memory/projects/model_catalog.md`

### Optimization

**NVFP4 quantization** (Blackwell-native):
- 4-bit floating point with FP8 scale per 16 values (4.5 effective bits)
- 3.5x model memory reduction vs FP16
- Doubles effective model capacity per GPU compared to FP8
- Supported in TensorRT-LLM 0.17+, vLLM
- Available for: Llama 4 Scout, DeepSeek-R1, DeepSeek-V3.2, Llama 3.3 70B, Llama 3.1 405B

**Speculative decoding** (automatic via Dynamo):
- EAGLE-3: 2-4x speedup via lightweight autoregressive head
- SSD (ICLR 2026): up to 5x speedup, parallelizes speculation AND verification
- Dynamo handles this transparently -- it is why 7x performance claims hold

### KV Cache -- Multi-Tier Memory Hierarchy

```
Tier 1: GPU HBM         -- hottest working set, lowest latency
Tier 2: CPU DRAM         -- warm state, ~10x more capacity
Tier 3: Local NVMe SSD   -- cold state, ~100x more capacity (BlueField-4 ICMSP)
Tier 4: Remote storage    -- archive, cross-node sharing
```

Managed by Dynamo's KVBM (KV Block Manager). Cost-aware eviction across all tiers.

**BlueField-4 DPU** powers NVIDIA ICMSP (Inference Context Memory Storage Platform) -- standardizes KV cache offload from GPU HBM to NVMe. Every NVL72 rack should include BlueField-4 DPUs.

**NVMe spec priority:** High random read IOPS over sequential throughput. KV cache workload is fundamentally different from training checkpoint I/O.

### Decode Acceleration -- Groq LPU

NVIDIA acquired Groq for $20B. Groq 3 LPX racks ship H2 2026.

| Spec | Detail |
|------|--------|
| Chip | Groq LP30: 512 MB SRAM, 1.23 FP8 PFLOPS |
| Rack | 256 LP30 LPUs, fully liquid-cooled, MGX infrastructure |
| Integration | Dynamo routes prefill to GPU, decode FFN/MoE to LPU |
| Performance | Up to 35x inference throughput per megawatt |
| Pricing tier | "Ultra" at $100+/M tokens for latency-sensitive workloads |
| ADC impact | Power advantage becomes even more valuable at 35x tokens/watt |

### Scheduling -- Run:AI

Run:AI provides GPU scheduling, multi-tenant access control, and workload management.

**ADC customer tier mapping:**

| ADC Tier | Run:AI Project | GPU Allocation | Scheduling | Price Point |
|----------|---------------|----------------|------------|-------------|
| Enterprise | Dedicated project | Guaranteed quota (MIG) | Priority | ~$45/M tokens |
| Premium | Shared project | Guaranteed minimum (MPS) | Fair-share | ~$6/M tokens |
| Standard | Shared project | Burst capacity | Best-effort | ~$1/M tokens |
| Batch | Low-priority project | Preemptible | Fill gaps | ~$0.20/M tokens |

Source: `adc3k-deploy/vendors/nvidia/runai-deployment-guide.md`

### Multi-Tenant Isolation

| Method | Isolation Level | Best For |
|--------|----------------|----------|
| MIG (Multi-Instance GPU) | Hardware: dedicated compute, memory, cache per instance | Enterprise customers |
| MPS (CUDA Multi-Process Service) | Space partitioning: explicit memory + compute limits | Premium customers |
| Time-slicing | Software: CUDA time-slicing, shared fault domain | Standard/Batch |

Source: `adc3k-deploy/vendors/nvidia/gpu-sharing-guide.md`

### Autoscaling

- Knative HPA on latency, throughput, and concurrency metrics
- Scale-to-zero when no requests (saves power -- critical for gas cost optimization)
- Wildcard DNS: `*.runai-inference.adc3k.com`
- TLS termination at ingress

---

## 5. Tier 4 -- Edge (Jetson AGX Orin)

**Purpose:** Local inference at ADC Pure DC AI Cassettes, KLFT drone hub, and remote sites. Autonomous operation when disconnected.

### Hardware
- NVIDIA Jetson AGX Orin: 275 TOPS, up to ~8B dense models
- Deployed in: ADC Pure DC AI Cassettes, KLFT 1.1 (drone hub), remote/offshore sites, wetland pilings

### Edge Model Stack

| Layer | Model | Params | License | Use Case |
|-------|-------|--------|---------|----------|
| General LLM | Gemma 3 4B | 4B | Apache 2.0 | Multimodal, 140+ languages, 128K context |
| General LLM (alt) | Phi-4 Mini 3.8B | 3.8B | MIT | Beats GPT-4o on math |
| Vision | NVIDIA VILA 1.5-3B | 3B | NVIDIA | Drone feeds, security cameras, video understanding |
| Vision (alt) | Gemma 3 4B | 4B | Apache 2.0 | Multimodal vision on Jetson |
| Embeddings | E5-small (33M) | 33M | MIT | Edge RAG, runs on CPU |
| STT | Whisper Large V3 Turbo (quantized) | 809M | MIT | Multilingual, 100+ languages |
| TTS | Kokoro | 82M | Apache 2.0 | Tiny, fast, high quality |

### Edge Operating Modes

| Mode | Network | Behavior |
|------|---------|----------|
| Connected | Fiber or Starlink to central cluster | Route complex queries to Tier 2/3, local handles latency-sensitive |
| Degraded | Intermittent connectivity | Queue non-urgent requests, serve locally for real-time |
| Air-gapped | No network | Full autonomous operation, all inference local |

### KLFT Drone Hub Integration
- NVIDIA Metropolis for real-time video analytics at KLFT
- VLMs (VILA 1.5-3B, Gemma 3 4B) complement Metropolis for custom analysis
- Jetson Orin processes drone feeds locally, sends alerts to central cluster
- FAA Part 108 BVLOS compliant (spring 2026)

---

## 6. Tier 5 -- Security Layer

**Purpose:** Enterprise-grade security across all tiers. Enables defense, government, healthcare, and financial customers.

### Content Safety

| Layer | Tool | Function |
|-------|------|----------|
| Orchestration | NeMo Guardrails (Apache 2.0) | Content filtering, topic restriction, jailbreak prevention, PII detection, RAG grounding |
| Classifier | Nemotron-Safety-Guard-8B-v3 (NVIDIA Open) | 23 safety categories, 20+ languages, reasoning-capable |
| Agent security | NemoClaw | File access control, code execution sandboxing, policy-based privacy |

### Compute Isolation

| Method | Technology | Use Case |
|--------|-----------|----------|
| Confidential Containers | AMD SEV-SNP hardware TEE + GPU attestation | Defense/government customers |
| KubeVirt | VM-level GPU passthrough | Maximum isolation per tenant |
| MIG | Hardware GPU partitioning | Standard multi-tenant isolation |

### Air-Gap Deployment

Full offline deployment for classified environments:
- GPU Operator supports air-gapped install (pre-loaded container images)
- All models, NIM containers, and Dynamo components pre-staged on local registry
- No external network dependency after initial provisioning
- Source: `adc3k-deploy/vendors/nvidia/gpu-operator-playbook.md` (Section 11)

### Federated Learning -- NVIDIA FLARE

Train across ADC sites without sharing customer data:

```
Trappeys (Lafayette)  -----> Aggregation Server <----- Willow Glen (St. Gabriel)
       |                          |                          |
  Local training            Global model              Local training
  on local data             updates only              on local data
       |                          |                          |
MARLIE 1 (Lafayette)  -----> Aggregation Server <----- Edge nodes
```

- Open source, production-ready (Apache 2.0)
- Privacy-preserving: only model weight updates cross the wire, never raw data
- Built-in FedAvg, FedOpt, FedProx algorithms
- Compliance selling point for healthcare, finance, government customers
- No single-site competitor can match this

---

## 7. Mission Control FastAPI Server

The existing Mission Control server (`main.py`) is the custom business logic layer that sits above the NVIDIA stack. It handles everything NVIDIA does not provide out of the box.

### Current Architecture (running today)

```
FastAPI Server (main.py)
    |
    +-- Authentication (MC_API_KEY, X-API-Key header or query param)
    +-- Rate Limiting (RateLimitMiddleware)
    +-- CORS (MC_CORS_ORIGINS)
    |
    +-- 10 Agents:
    |   |-- OrchestratorAgent (job/step state machines, planner, task routing)
    |   |-- RepoAnalystAgent (file listing, code explanation)
    |   |-- CoderAgent (read/write/patch/generate code)
    |   |-- InfraManagerAgent (GPU/CPU/RAM/Docker/Redis health)
    |   |-- IntegrationAgent (HTTP, RunPod GraphQL, webhooks)
    |   |-- UIAgent (SSE broadcast, dashboard state)
    |   |-- NotionSyncAgent (work folder sync)
    |   |-- NewsScoutAgent (AI news analysis)
    |   |-- PublisherAgent (content distribution)
    |   +-- SocialAgent (social media)
    |
    +-- Event Bus (in-memory pub/sub, fnmatch wildcards, Redis Streams ready)
    +-- State Store (in-memory KV with TTL, Redis ready)
    +-- Skill Registry (auto-discovery: file_manager, runpod, http_client, notion)
    +-- Metrics Collector (counters, gauges, histograms)
    +-- Agent Watchdog (stall detection + alerts)
    +-- Dead Letter Queue (failed event recovery)
    |
    +-- API Endpoints:
        +-- /chat, /chat/stream (Claude direct + SSE streaming)
        +-- /tasks, /tasks/{id}, /tasks/{id}/stream (job management + SSE)
        +-- /events (SSE live dashboard)
        +-- /agents (agent status)
        +-- /infra, /infra/check (GPU health)
        +-- /metrics (observability)
        +-- /health, /ready (probes)
        +-- /config (runtime config)
        +-- /upload, /files (file management)
        +-- /snapshot (polling fallback)
        +-- /notion/tree (workspace tree)
```

### Evolution Path

The current server becomes the **API gateway and business logic layer** in the full stack:

| Function | Current (Claude API only) | Target (full 5-tier) |
|----------|--------------------------|---------------------|
| Chat/reasoning | Claude API via Anthropic SDK | Model router (Tier 1/2/3 based on request type) |
| Task planning | Regex fast-path + Claude LLM fallback | Self-hosted Qwen 3 235B (Tier 2) with Claude fallback |
| GPU monitoring | InfraManagerAgent (local checks) | DCGM + Prometheus + Grafana + custom alerts |
| Customer API | Not yet | Token metering, Stripe billing, usage dashboards |
| Auth | MC_API_KEY (single key) | Keycloak (SSO, RBAC, per-customer API keys) |
| Agent framework | Custom BaseAgent + skill dispatch | Same core + AgentIQ integration for profiling |

---

## 8. Model Router Logic

Every request hits Mission Control's API gateway first. The router decides which tier handles it.

```
Request arrives at Mission Control API
  |
  Is this an internal ADC operation?
  (GPU monitoring, daily briefing, Notion sync, Ally chatbot, knowledge query)
    YES --> Route to Tier 2 (self-hosted Qwen 3 235B / DeepSeek-V3.2)
            Cost: $0
  |
  Is this a complex research / investor / strategic task?
  (multi-step analysis, document generation, architecture review)
    YES --> Route to Tier 1 (Claude API)
            Cost: API per-call
  |
  Is this a customer inference request?
    YES --> Route to Tier 3 (Dynamo + NIM token factory)
            |
            Sub-route based on customer tier (Run:AI project):
            |
            Enterprise ($45/M) --> Dedicated MIG partition + priority scheduling
            Premium ($6/M)     --> MPS partition + guaranteed quota
            Standard ($1/M)    --> Shared pool + fair-share scheduling
            Batch ($0.20/M)    --> Time-slicing + preemptible (fills idle capacity)
  |
  Is this an edge / IoT / drone request?
    YES --> Route to Tier 4 (local Jetson inference)
            Fallback: queue for Tier 2/3 if connected
```

### Router Implementation

The router is an extension of the existing `OrchestratorAgent` planner pattern:
1. Regex fast-path catches obvious patterns (zero LLM cost)
2. Metadata check: customer tier, API key scope, request headers
3. LLM fallback for ambiguous requests (routed to Tier 2 self-hosted model, not Claude)

---

## 9. Fine-Tuning Pipeline

### Data Preparation

| Source | Format | Volume |
|--------|--------|--------|
| Memory files (`memory/`) | Instruction/response pairs (JSON-L) | ~50 files, growing |
| Vendor specs (`adc3k-deploy/vendors/`) | Technical Q&A extraction | 22 vendors, ~100 docs |
| Conversation logs | Multi-turn dialogue (JSON-L) | Continuous growth |
| Playbooks | Step-by-step procedures | ~10 playbooks |
| Notion workspace | Structured knowledge | ~200 pages |

### Pipeline

```
Source docs --> Extract instruction/response pairs (script)
    |
    v
JSON-L dataset (validated, deduplicated)
    |
    v
NeMo Customizer (LoRA, on NVL72 at MARLIE 1)
    |
    v
Validation: test against known Q&A pairs from ADC domain
    |
    v
NIM model version swap (zero-downtime blue/green)
    |
    v
Production (Tier 2 operations brain)
```

| Setting | Value |
|---------|-------|
| Method | LoRA (10,000x fewer trainable params, 3x less GPU) |
| Base model | Qwen 3 235B or DeepSeek-V3.2 |
| Tool | NeMo Customizer (microservice, API-driven) |
| Rapid iteration | Unsloth for fast LoRA experiments before promoting to NeMo |
| Schedule | Monthly re-training as knowledge grows |
| Advanced | GRPO (reward-model-free alignment) when behavior tuning needed |
| Hardware | NVL72 at MARLIE 1 (same racks that serve inference) |

---

## 10. RAG Pipeline

### Architecture

```
                    Query
                      |
                      v
              [NV-Embed-v2 (7B)]
              Embed query --> 4096-dim vector
                      |
                      v
              [Milvus Vector DB]
              Top-5 chunks by cosine similarity
                      |
                      v
              [NV-Rerank via NIM]
              Re-score and re-order retrieved chunks
                      |
                      v
              [Context injection into model prompt]
                      |
                      v
              [Qwen 3 235B / DeepSeek-V3.2]
              Generate response grounded in retrieved context
```

### Document Ingestion

| Step | Detail |
|------|--------|
| Sources | All `.md` files from repo + Notion export + vendor PDFs |
| Chunking | 512 tokens with 50-token overlap |
| Embeddings | NV-Embed-v2 (7B, Mistral-based, NIM-native) |
| Vector store | Milvus (Apache 2.0, self-hosted, ~$500/mo at 10M vectors) |
| Retrieval | Top-5 chunks by cosine similarity |
| Reranking | NV-Rerank via NIM (improves precision) |
| Update frequency | Daily cron (new docs auto-indexed) |
| Edge RAG | E5-base-instruct (110M, <30ms, runs on CPU) for Jetson nodes |

### Grounding Check

NeMo Guardrails verifies that generated responses are grounded in retrieved context. If the model hallucinates beyond what the chunks support, the response is flagged and re-generated with stricter grounding constraints.

---

## 11. Monitoring and Alerting

### GPU Telemetry (DCGM)

DCGM Exporter scrapes GPU metrics for Prometheus every 15 seconds.

**Key metrics:**

| Metric | Prometheus Name | What It Measures |
|--------|----------------|------------------|
| GPU utilization | DCGM_FI_DEV_GPU_UTIL | Compute engine activity % |
| Memory utilization | DCGM_FI_DEV_MEM_COPY_UTIL | Memory bandwidth usage % |
| Temperature | DCGM_FI_DEV_GPU_TEMP | GPU die temperature |
| Power draw | DCGM_FI_DEV_POWER_USAGE | Current power consumption |
| ECC errors (double-bit) | DCGM_FI_DEV_ECC_DBE_VOL | Critical memory errors |
| XID errors | DCGM_FI_DEV_XID_ERRORS | GPU fault codes |

Source: `adc3k-deploy/vendors/nvidia/gpu-sharing-guide.md`

### Alert Rules

| Condition | Severity | Action |
|-----------|----------|--------|
| GPU temp > 85C | Warning | Notify ops team |
| GPU temp > 95C | Critical | Throttling imminent, check cooling |
| ECC double-bit errors > 0 | Critical | Investigate hardware, RMA if persistent |
| XID errors | Critical | GPU fault, may need restart |
| Customer utilization < 30% sustained | Info | Suggest rightsizing (save customer money, free capacity) |
| Token throughput drop > 20% | Warning | Investigate model serving pipeline |
| Dynamo worker pool < 50% healthy | Critical | Check node health, autoscaler |

### Dashboards

| Dashboard | Tool | Content |
|-----------|------|---------|
| GPU Health | Grafana (Dashboard ID 12239, NVIDIA pre-built) | Per-GPU temp, power, utilization, ECC |
| Custom ADC | Grafana (custom) | Token throughput, customer utilization, revenue per rack |
| Run:AI | Run:AI console | Workload status, queue depth, customer quotas |
| Mission Control | Web dashboard (`web/index.html`) | Agent status, jobs, events, infra health |

### Existing Monitoring (running today)

Mission Control already has:
- Agent watchdog (stall detection + alerts)
- Metrics collector (counters, gauges, histograms) at `/metrics`
- Dead letter queue monitoring at `/infra/dlq`
- Health/readiness probes at `/health` and `/ready`
- InfraManagerAgent (GPU/CPU/RAM/Docker/Redis health checks)
- SSE live dashboard with 20s heartbeat keepalive

---

## 12. Cost Structure

### Software

| Item | Cost | Notes |
|------|------|-------|
| Dynamo 1.0 | $0 | Open source (Apache 2.0) |
| NIM (development) | $0 | Free to develop/test |
| NIM (production) | $0 (bundled) | Included with NVIDIA AI Enterprise (bundled with NVL72 purchase) |
| GPU Operator | $0 | Open source |
| Network Operator | $0 | Open source |
| Run:AI | $0 (base) | Free tier sufficient initially; enterprise licensing later |
| Base Command Manager | $0 | Free tier: 8 accelerators per system, any cluster size |
| Milvus | $0 | Self-hosted (Apache 2.0), ~$500/mo compute |
| LlamaIndex | $0 | MIT |
| NeMo Guardrails | $0 | Apache 2.0 |
| NeMo Customizer | $0 (bundled) | Part of NVIDIA AI Enterprise |
| AgentIQ | $0 | Apache 2.0 |
| NVIDIA FLARE | $0 | Apache 2.0 |
| Claude API (Tier 1) | $20-50/mo (current actual) | Optional — drops to $0 when self-hosted ops brain handles most tasks |
| **Total software** | **$0-50/month** | Effectively zero once self-hosted. All components open source or bundled. |

### Power

| Source | Cost/kWh | Role |
|--------|----------|------|
| Natural gas (Henry Hub) | $0.027-0.035 | Backbone -- carries main load 24/7 |
| Solar (First Solar rooftop) | $0 marginal | Primary offset |
| Diesel gensets | Emergency only | Pipeline-independent backup |
| Grid (LUS) | $0.12 (sell-back only) | NOT a consumption source |

### Comparison

| Deployment | Monthly Cost (equivalent compute) |
|------------|----------------------------------|
| ADC self-hosted (full 5-tier stack) | ~$0-50 software + power costs |
| Cloud equivalent (RunPod/CoreWeave/Lambda) | $50,000-100,000/month for same compute |
| Software licensing savings | 100% (open source + bundled NVAIE) |

---

## 13. Deployment Timeline

### Phase 1 -- MARLIE 1 First Rack

| Component | Status |
|-----------|--------|
| Mission Control FastAPI server | Running (current) |
| Claude API (Tier 1) | Running (current) |
| First NVL72 rack | Install + power-on |
| GPU Operator + Network Operator | Deploy on K8s |
| Dynamo 1.0 | Deploy single model (Qwen 3 235B) |
| NIM | Deploy operations brain (Tier 2) |
| Tier 3 | Single model for customer beta (DeepSeek-V3.2 or Nemotron Ultra) |
| Monitoring | DCGM + Prometheus + Grafana |

### Phase 2 -- MARLIE 1 Full 8 Racks

| Component | Status |
|-----------|--------|
| All tiers operational | Tier 1-4 running |
| Multi-model serving | Full model catalog on Tier 3 |
| RAG pipeline | LlamaIndex + Milvus + NV-Embed-v2 |
| Fine-tuning | NeMo Customizer running monthly LoRA |
| Run:AI | Customer projects, quotas, billing |
| Customer API | Token metering, Stripe, usage dashboards |
| Keycloak | SSO + RBAC replacing MC_API_KEY |
| Edge nodes | Jetson AGX Orin at KLFT |

### Phase 3 -- Trappeys Expansion

| Component | Status |
|-----------|--------|
| Trappeys solar AI factory | 36-84 NVL72 racks at scale |
| Federated learning | NVIDIA FLARE across MARLIE 1 + Trappeys |
| Groq LPX racks | Mixed GPU+LPU for ultra-low-latency decode (H2 2026) |
| Confidential Containers | Defense/government customer readiness |
| Self-hosted SaaS replacement | Mattermost, n8n, Keycloak, LiteLLM, Nextcloud |

### Phase 4 -- Willow Glen SuperPOD

| Component | Status |
|-----------|--------|
| Full SuperPOD | 100+ MW scale, InfiniBand spine |
| Base Command Manager | Enterprise cluster management |
| All tiers at scale | Thousands of concurrent customers |
| Physical AI offering | Isaac + Cosmos + Omniverse (drone/robot simulation) |
| Synthetic data pipeline | Nemotron-4 340B + Cosmos + Isaac Sim |
| Vera Rubin NVL72 | HBM4 (288 GB/GPU) when available |

---

## Appendix A -- Self-Hosted SaaS Replacements

ADC eats its own dog food. Every tool runs on ADC infrastructure.

| SaaS | Open-Source Replacement | License | ADC Status |
|------|----------------------|---------|------------|
| OpenAI API | LocalAI (drop-in replacement) | MIT | Deploy Phase 2 |
| Slack | Mattermost | MIT | Deploy Phase 3 |
| Dropbox/Drive | Nextcloud | AGPL | Deploy Phase 3 |
| Auth0 | Keycloak | Apache 2.0 | Deploy Phase 2 |
| Zapier | n8n | Fair-code | Deploy Phase 3 |
| OpenRouter | LiteLLM or Bifrost | MIT | Deploy Phase 2 |
| Datadog | Prometheus + Grafana | Apache 2.0 | Deploy Phase 1 |

Source: `data/ai-infrastructure-march-2026.md` (Section 11)

---

## Appendix B -- License Summary

All production deployments use commercial-friendly licenses:

| License | Models / Tools | Restrictions |
|---------|---------------|-------------|
| MIT | DeepSeek (all), Kimi K2.5, Kokoro, BGE, E5, Mattermost | None |
| Apache 2.0 | Qwen (all), Gemma, Fish Speech, Milvus, AgentIQ, NeMo Guardrails, Keycloak, Prometheus, Grafana | None |
| NVIDIA Open | Nemotron (all), Canary, VILA | Commercial OK, NVIDIA terms |
| Llama License | Llama 4 (all) | Commercial OK, 700M MAU threshold, attribution required |
| AGPL | XTTS-v2, Nextcloud | Copyleft -- avoid for proprietary customer-facing services |

---

## Appendix C -- What to Watch (H2 2026)

| Item | Expected | Impact |
|------|----------|--------|
| Llama 4 Behemoth | 2T total / 288B active | Could reset open-model leaderboard |
| Vera Rubin NVL72 | Late 2026 | HBM4 (288 GB/GPU), NVLink 6 -- every model gets memory upgrade |
| Groq 3 LPX racks | H2 2026 | 35x tokens/watt, ultra-premium pricing tier |
| Dynamo 2.0 | GTC 2027 (likely) | Multi-node disaggregated serving improvements |
| Qwen 4 | Q3 2026 (Alibaba 6-month cadence) | Potential new best open model |
| DeepSeek-V4 | TBD | If V3.2 trajectory holds, formidable |
| NemoClaw maturity | H2 2026 | Self-hosted autonomous agents at production quality |

---

## Document References

| Document | Path | Content |
|----------|------|---------|
| Model Catalog | `memory/projects/model_catalog.md` | Full model specs, benchmarks, ADC picks |
| Innovation Report | `data/ai-infrastructure-march-2026.md` | Dynamo, Groq, FP4, MoE, KV cache, federated learning |
| Inference Playbook | `adc3k-deploy/vendors/nvidia/inference-serving-playbook.md` | Dynamo + NIM + Mission Control deployment |
| GPU Operator Playbook | `adc3k-deploy/vendors/nvidia/gpu-operator-playbook.md` | GPU lifecycle, MIG, air-gap, driver management |
| GPU Sharing Guide | `adc3k-deploy/vendors/nvidia/gpu-sharing-guide.md` | MIG, MPS, time-slicing, DCGM monitoring |
| Run:AI Guide | `adc3k-deploy/vendors/nvidia/runai-deployment-guide.md` | Scheduling, RBAC, customer tiers, install order |
| Cloud-Native Stack | `adc3k-deploy/vendors/nvidia/cloud-native-stack.md` | Full NVIDIA software layer map |
| Network Operator | `adc3k-deploy/vendors/nvidia/network-operator-playbook.md` | InfiniBand, RDMA, GPUDirect |
| MGX/DSX Architecture | `adc3k-deploy/vendors/nvidia/mgx-dsx-architecture.md` | Hardware reference design |
| Neocloud Strategy | `memory/projects/neocloud_strategy.md` | ADC business model, competitive positioning |
| NVIDIA Strategy | `memory/projects/nvidia_strategy.md` | DSX, Dynamo, certification ladder |
| FastAPI Server | `main.py` | Current Mission Control implementation |
