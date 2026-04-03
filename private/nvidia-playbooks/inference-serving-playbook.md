# ADC Inference Serving Deployment Playbook

> NVIDIA Dynamo 1.0 + NIM Microservices + Mission Control
> Compiled: 2026-03-25 | Classification: Internal — ADC Engineering

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [NVIDIA Dynamo 1.0](#2-nvidia-dynamo-10)
3. [NIM Microservices](#3-nim-microservices)
4. [NVIDIA Mission Control — Cluster Management](#4-nvidia-mission-control--cluster-management)
5. [The Complete Token-Serving Pipeline](#5-the-complete-token-serving-pipeline)
6. [Licensing and Costs](#6-licensing-and-costs)
7. [ADC-Specific Deployment Plan](#7-adc-specific-deployment-plan)

---

## 1. Executive Summary

ADC's inference serving stack is three layers of NVIDIA software on top of our GPU hardware:

| Layer | Component | What It Does | Open Source? |
|-------|-----------|-------------|--------------|
| **Orchestration** | Mission Control (Base Command Manager + Run:AI) | Provision K8s clusters, schedule GPU workloads, monitor utilization | Free (BCM Essentials), paid enterprise support |
| **Inference Framework** | Dynamo 1.0 | Multi-node disaggregated inference — routes, caches, scales | Yes — Apache 2.0 on GitHub |
| **Model Serving** | NIM Microservices | Pre-optimized model containers with OpenAI-compatible API | Free to develop, NVAIE license for production |
| **ADC Custom** | Billing, Auth, Rate Limiting, Customer Portal | Token metering, API key management, usage dashboards | We build this |

**Bottom line**: NVIDIA provides everything from Kubernetes cluster to API endpoint. ADC builds the customer-facing billing/auth wrapper and owns the power + site + hardware. This is the neocloud model.

---

## 2. NVIDIA Dynamo 1.0

### 2.1 What It Is

Dynamo is an open-source, distributed inference-serving framework built for multi-node AI deployments at data center scale. It sits as an **orchestration layer above inference engines** (SGLang, TensorRT-LLM, vLLM) — it does not replace them, it coordinates them into a unified, optimized system.

- **GitHub**: [github.com/ai-dynamo/dynamo](https://github.com/ai-dynamo/dynamo)
- **Docs**: [docs.dynamo.nvidia.com](https://docs.dynamo.nvidia.com) / [docs.nvidia.com/dynamo](https://docs.nvidia.com/dynamo/latest/)
- **License**: Open source (Apache 2.0), enterprise support via NVIDIA AI Enterprise
- **Announced**: GTC 2025, production-ready release as Dynamo 1.0

### 2.2 Architecture — Core Components

```
                    ┌─────────────────────────────────────┐
                    │           Dynamo Frontend            │
                    │  (Request routing + load balancing)  │
                    └──────────┬──────────────────────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
     ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
     │  KV-Aware    │ │  GPU Planner │ │ AIConfigurator│
     │   Router     │ │  (autoscale) │ │ (auto-config) │
     └──────┬───────┘ └──────┬───────┘ └──────────────┘
            │                │
     ┌──────┴────────────────┴──────┐
     │      Worker Pool             │
     │  ┌────────┐ ┌────────┐      │
     │  │Prefill │ │Decode  │ ...  │
     │  │Workers │ │Workers │      │
     │  └────────┘ └────────┘      │
     │      (SGLang / TRT-LLM / vLLM)      │
     └──────────────────────────────┘
            │
     ┌──────┴──────────────────────┐
     │   KV Block Manager (KVBM)   │
     │   GPU → CPU → SSD → Remote  │
     └─────────────────────────────┘
```

**Key components:**

| Component | Function |
|-----------|----------|
| **KV-Aware Router** | Routes requests to workers based on KV cache overlap — avoids redundant recomputation |
| **GPU Planner** | Monitors capacity, dynamically reallocates workers between prefill and decode to meet SLOs |
| **KV Block Manager (KVBM)** | Multi-tier cache: GPU VRAM → CPU RAM → local SSD → remote storage (S3, Azure Blob) |
| **AIConfigurator** | Auto-recommends cluster config based on model, GPU budget, and SLO targets |
| **AIPerf** | Benchmarking tool for measuring performance across inference solutions |
| **NIXL** | Low-latency data transfer library across GPUs, CPUs, networks, and storage |
| **ModelExpress** | Rapid model loading via weight streaming + checkpoint restore |
| **Grove** | Topology-aware Kubernetes scheduling (NVLink fabric-aware on GB200/GB300 NVL72) |

### 2.3 Prefill/Decode Disaggregation

This is the core innovation. Traditional inference runs prefill and decode on the same GPU. Dynamo separates them:

**Three-stage disaggregation (E/P/D):**

| Stage | What It Does | Compute Profile | Scaling |
|-------|-------------|-----------------|---------|
| **Encode** | Process images/video for multimodal models | Varies | Independent |
| **Prefill** | Process entire input prompt, generate first token | **Compute-bound** (FLOP-heavy) | Scale independently |
| **Decode** | Generate subsequent tokens one at a time | **Memory-bound** (bandwidth-heavy) | Scale independently |

**Why this matters for ADC:**
- Prefill workers need raw compute (Blackwell excels here)
- Decode workers need memory bandwidth (can use different GPU configs)
- Independent scaling means fewer GPUs wasted sitting idle
- During bursty traffic, spin up more prefill workers without touching decode
- KV cache transfers between stages via NIXL at wire speed over NVLink

**How it works in practice:**
1. Request arrives at Frontend
2. KV-Aware Router checks which worker already has relevant KV cache from prior requests
3. If cache hit → route to that worker (saves recomputation)
4. If miss → route to least-loaded prefill worker
5. Prefill worker processes input, generates KV cache
6. KV cache transferred to decode worker via NIXL
7. Decode worker generates tokens until completion
8. GPU Planner continuously rebalances prefill/decode worker counts based on queue depths

### 2.4 Multi-Node Inference

Dynamo handles models too large for a single GPU (or single node) natively:

- **Tensor Parallelism (TP)**: Split model layers across GPUs within a node (NVLink)
- **Pipeline Parallelism (PP)**: Split model stages across nodes
- **Expert Parallelism (EP)**: For MoE models, route experts across GPUs
- **Grove API**: Topology-aware scheduling that understands NVLink fabric on NVL72 systems
- **Request migration**: If a worker fails mid-request, transparently migrates to healthy worker
- **KV cache persistence**: Cache survives worker failures via multi-tier storage

### 2.5 Supported Inference Engines

| Engine | Disaggregated Serving | KV-Aware Routing | KVBM Status |
|--------|----------------------|-------------------|-------------|
| **TensorRT-LLM** | Yes | Yes | Production-ready |
| **vLLM** | Yes | Yes | Production-ready |
| **SGLang** | Yes | Yes | Experimental |
| **PyTorch** | Via integration | Via integration | N/A |

All three major backends support disaggregated serving and KV-aware routing. SGLang also has a Diffusion variant for image generation. vLLM-Omni supports video generation via FastVideo.

### 2.6 Installation

**Option 1: Docker (fastest for testing)**
```bash
docker run --gpus all --network host --rm -it \
  nvcr.io/nvidia/ai-dynamo/sglang-runtime:1.0.1
```

**Option 2: pip install**
```bash
# Pick your backend
pip install "ai-dynamo[sglang]"
pip install "ai-dynamo[vllm]"
pip install "ai-dynamo[trtllm]"
```

**Option 3: Kubernetes (production)**

Prerequisites:
- Kubernetes v1.24+
- Helm v3.0+
- NVIDIA GPU Operator installed
- kubectl access with admin or namespace-scoped permissions

```bash
# Step 1: Add Helm repo
helm repo add nvidia https://helm.ngc.nvidia.com/nvidia/ai-dynamo
helm repo update

# Step 2: Install CRDs
RELEASE_VERSION=0.9.0-post1
helm install dynamo-crds nvidia/dynamo-crds --version $RELEASE_VERSION

# Step 3: Install Dynamo Platform
helm install dynamo-platform nvidia/dynamo-platform \
  --namespace dynamo-system --create-namespace \
  --version $RELEASE_VERSION \
  --set "grove.enabled=true" \
  --set "kai-scheduler.enabled=true" \
  --set dynamo-operator.controllerManager.manager.image.tag=0.9.0
```

> **Note**: Grove (topology-aware scheduling) and KAI Scheduler are NOT installed by default. Enable them explicitly for NVL72 deployments.

**System requirements:**
- Ubuntu 24.04+ or compatible Linux
- CUDA-capable GPUs: H100, H200, B200, GB200 NVL72, GB300 NVL72
- Rust toolchain (for source compilation only)
- Python 3.8+

### 2.7 Configuration — Zero-Config Mode

Dynamo's **DGDR (Dynamo Graph Deployment Request)** enables zero-config deployment:
1. Specify model name and SLO targets (latency, throughput)
2. AIConfigurator profiles the model on available hardware
3. Automated Planner generates optimal worker configuration
4. Deploy with a single manifest

### 2.8 Performance Benchmarks

| Benchmark | Result | Hardware | Model |
|-----------|--------|----------|-------|
| Throughput improvement | **7x** | GB200 NVL72 (Blackwell) | DeepSeek R1-0528, FP4 |
| TTFT + throughput | **4x lower TTFT, 1.5x higher throughput** | Hopper | Llama 3.1 (NeMo Agent Toolkit) |
| Model loading | **7x faster** | H200 | Large MoE (weight streaming) |
| Multimodal | **30% TTFT accel, 25% throughput gain** | — | Qwen3-VL-30B (embedding cache) |
| MoE throughput | **Up to 50x** vs Hopper | GB300 NVL72 | MoE models |
| SLA compliance | **80% fewer breaches** | — | Planner autoscaling |

### 2.9 Pre-Built Recipes

| Model | Backend | Mode |
|-------|---------|------|
| Llama-3-70B | vLLM | Aggregated |
| DeepSeek-R1 | SGLang | Disaggregated |
| Qwen3-32B-FP8 | TensorRT-LLM | Aggregated |

Cloud-specific deployment guides available for AWS EKS, Google GKE, Azure AKS, Alibaba Cloud, and OCI.

### 2.10 Agentic AI Optimizations

Dynamo has specific features for AI agent workloads (critical for ADC's token factory model):

- **Priority-based request routing**: Latency-sensitive agent calls get priority
- **Cache pinning**: Frequently-used system prompts resist eviction
- **Frontend hints**: Agent frameworks can signal latency sensitivity, expected output length, cache control
- **LangChain integration**: `ChatNVIDIADynamo` connector
- **NeMo Agent Toolkit**: Full integration for multi-step agent pipelines

### 2.11 Resilience Features

- Canary health checks per worker
- Network-level fault detection
- Request cancellation and transparent migration to healthy workers
- KV cache persists across worker failures (multi-tier storage)
- Global KV event emission for cluster-wide visibility

### 2.12 Ecosystem

**Early adopters**: AstraZeneca, ByteDance, Baseten, CoreWeave, Meituan, Pinterest, Tencent, Together AI, 50+ organizations

**Storage partners**: NetApp, Pure Storage, HPE, IBM, VAST, WEKA

**Cloud providers**: AWS, Azure, Google Cloud, Alibaba, OCI (all have published Dynamo deployment guides)

---

## 3. NIM Microservices

### 3.1 What They Are

NVIDIA NIM (NVIDIA Inference Microservices) are pre-optimized, containerized inference services. Each NIM container packages a model with the best inference engine for the target GPU, exposes an OpenAI-compatible API, and handles all optimization automatically.

Think of it this way: **Dynamo is the orchestra conductor, NIM containers are the musicians.**

- **Registry**: [build.nvidia.com](https://build.nvidia.com/models) (try free) / nvcr.io (self-host)
- **Docs**: [docs.nvidia.com/nim](https://docs.nvidia.com/nim/large-language-models/latest/)
- **GitHub (deployment)**: [github.com/NVIDIA/nim-deploy](https://github.com/NVIDIA/nim-deploy)

### 3.2 How NIM Works

```
┌──────────────────────────────────────┐
│          NIM Container               │
│  ┌──────────────────────────────┐    │
│  │  Model Weights (cached)      │    │
│  └──────────────────────────────┘    │
│  ┌──────────────────────────────┐    │
│  │  Optimized Engine            │    │
│  │  (TensorRT-LLM / vLLM /     │    │
│  │   SGLang — auto-selected)    │    │
│  └──────────────────────────────┘    │
│  ┌──────────────────────────────┐    │
│  │  OpenAI-Compatible API       │    │
│  │  Port 8000                   │    │
│  │  /v1/chat/completions        │    │
│  │  /v1/completions             │    │
│  │  /v1/models                  │    │
│  │  /v1/health/ready            │    │
│  │  /v1/health/live             │    │
│  │  /v1/metrics (Prometheus)    │    │
│  └──────────────────────────────┘    │
└──────────────────────────────────────┘
```

NIM auto-selects the optimal inference engine (TensorRT-LLM, vLLM, or SGLang) for each model+GPU combination. No manual engine tuning required.

### 3.3 Deploying a NIM Container (Docker)

**Prerequisites:**
- NGC API Key (get from [ngc.nvidia.com](https://ngc.nvidia.com))
- NVIDIA Container Toolkit installed
- CUDA-capable GPU

**Step 1: Set up NGC credentials**
```bash
# Export API key
export NGC_API_KEY="your-key-here"

# Login to container registry
echo "$NGC_API_KEY" | docker login nvcr.io --username '$oauthtoken' --password-stdin
```

**Step 2: Run a NIM container**
```bash
export CONTAINER_NAME="llama3-nim"
export IMG_NAME="nvcr.io/nim/meta/llama-3.1-8b-instruct:latest"
export LOCAL_NIM_CACHE="$HOME/.cache/nim"
mkdir -p "$LOCAL_NIM_CACHE"

docker run -it --rm \
  --name=$CONTAINER_NAME \
  --runtime=nvidia \
  --gpus all \
  --shm-size=16GB \
  -e NGC_API_KEY=$NGC_API_KEY \
  -v "$LOCAL_NIM_CACHE:/opt/nim/.cache" \
  -u $(id -u) \
  -p 8000:8000 \
  $IMG_NAME
```

**Step 3: Test the endpoint**
```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta/llama-3.1-8b-instruct",
    "messages": [{"role": "user", "content": "What is CUDA?"}],
    "max_tokens": 256,
    "stream": true
  }'
```

### 3.4 API Format — OpenAI Compatible

NIM exposes a fully **OpenAI-compatible API**. Any application built for the OpenAI API works with NIM by changing the base URL:

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="not-used"  # NIM doesn't require API key locally
)

response = client.chat.completions.create(
    model="meta/llama-3.1-8b-instruct",
    messages=[{"role": "user", "content": "Explain GPU computing"}],
    stream=True
)
```

**Supported endpoints:**
| Endpoint | Function |
|----------|----------|
| `POST /v1/chat/completions` | Chat completions (streaming and non-streaming) |
| `POST /v1/completions` | Text completions |
| `GET /v1/models` | List available models |
| `GET /v1/health/ready` | Readiness probe (200 when model loaded) |
| `GET /v1/health/live` | Liveness probe (200 immediately) |
| `GET /v1/metrics` | Prometheus metrics |

**Features**: Streaming SSE, function/tool calling (model-dependent), JSON mode, temperature/top_p/top_k, stop sequences, logprobs.

### 3.5 Available Models (Selected — Full Catalog at build.nvidia.com)

**LLMs:**
| Model | Parameters | Notes |
|-------|-----------|-------|
| Meta Llama 3.1 8B Instruct | 8B | 1x GPU, great for testing |
| Meta Llama 3.1 70B Instruct | 70B | Multi-GPU (TP=4 or TP=8) |
| Meta Llama 3.3 70B Instruct | 70B | Latest Llama |
| Llama 3.1 Nemotron 70B Instruct | 70B | NVIDIA-tuned variant |
| Mistral NeMo 12B Instruct | 12B | Efficient mid-size |
| Mixtral 8x7B Instruct v0.1 | 46.7B MoE | Sparse MoE |
| DeepSeek R1 | 671B MoE | Reasoning model, multi-node |
| Qwen 3.5 VLM 400B MoE | 400B MoE | Multimodal |

**Other NIM domains:**
- Vision Language Models (VLMs)
- Embedding models (retrieval/RAG)
- Reranking models
- Speech (ASR/TTS)
- Biology/drug discovery

> **Note on DeepSeek**: DeepSeek models do NOT support tool/function calling in NIM.

### 3.6 NIM on Kubernetes — NIM Operator

The **NIM Operator** is a Kubernetes operator that manages the full lifecycle of NIM deployments.

**GitHub**: [github.com/NVIDIA/k8s-nim-operator](https://github.com/NVIDIA/k8s-nim-operator)

#### 3.6.1 Prerequisites
- Kubernetes 1.26+
- NVIDIA GPU Operator installed
- Persistent storage provisioner (for model caching)
- NGC API Key

#### 3.6.2 Custom Resources

| CRD | Purpose |
|-----|---------|
| **NIMCache** | Pre-downloads model weights to persistent storage (download once, reuse across pods/restarts) |
| **NIMService** | Manages NIM deployment lifecycle (pods, health probes, service exposure, GPU scheduling) |
| **NIMPipeline** | Groups multiple NIMService resources for coordinated deployment |
| **NIMBuild** | Pre-builds optimized TensorRT-LLM engines for target GPUs |

#### 3.6.3 Installation

```bash
# Create namespace
kubectl create namespace nim-service

# Create NGC secrets
kubectl create secret docker-registry ngc-secret \
  --docker-server=nvcr.io \
  --docker-username='$oauthtoken' \
  --docker-password=$NGC_API_KEY \
  -n nim-service

kubectl create secret generic ngc-api-secret \
  --from-literal=NGC_API_KEY=$NGC_API_KEY \
  -n nim-service

# Install NIM Operator via Helm
helm repo add nvidia https://helm.ngc.nvidia.com/nvidia
helm repo update
helm install nim-operator nvidia/k8s-nim-operator \
  --namespace nim-operator --create-namespace
```

#### 3.6.4 Deploy a Model — NIMCache + NIMService

**Step 1: Cache the model**
```yaml
apiVersion: apps.nvidia.com/v1alpha1
kind: NIMCache
metadata:
  name: llama3-8b-cache
  namespace: nim-service
spec:
  source:
    ngc:
      modelPuller: nvcr.io/nim/meta/llama-3.1-8b-instruct:2.0.0
      pullSecret: ngc-secret
      authSecret: ngc-api-secret
      model:
        engine: "vllm"
        tensorParallelism: "1"
  storage:
    pvc:
      create: true
      size: "80Gi"
      volumeAccessMode: ReadWriteOnce
```

```bash
kubectl apply -f nimcache.yaml
kubectl get nimcache -n nim-service -w  # Wait for "Ready"
```

**Step 2: Deploy the NIMService**
```yaml
apiVersion: apps.nvidia.com/v1alpha1
kind: NIMService
metadata:
  name: llama3-8b
  namespace: nim-service
spec:
  image:
    repository: nvcr.io/nim/meta/llama-3.1-8b-instruct
    tag: "2.0.0"
  pullSecrets:
    - ngc-secret
  authSecret: ngc-api-secret
  storage:
    nimCache: llama3-8b-cache
  resources:
    limits:
      nvidia.com/gpu: "1"
  expose:
    service:
      port: 8000
  env:
    - name: NIM_PASSTHROUGH_ARGS
      value: "--enable-prefix-caching --max-num-batched-tokens 4096"
  scale:
    enabled: true
    hpa:
      minReplicas: 1
      maxReplicas: 4
      metrics:
        - type: Pods
          pods:
            metric:
              name: vllm:num_requests_waiting
            target:
              type: AverageValue
              averageValue: "10"
  metrics:
    enabled: true
```

```bash
kubectl apply -f nimservice.yaml
kubectl get nimservice -n nim-service
kubectl get pods -n nim-service
```

#### 3.6.5 Health Probes

| Endpoint | Behavior |
|----------|----------|
| `/v1/health/live` | Returns 200 immediately (container running) |
| `/v1/health/ready` | Returns 200 only after model fully loaded |

Default startup probe: failureThreshold=120, periodSeconds=10 (~20 min timeout). For large models (70B+), increase to failureThreshold=240.

#### 3.6.6 Autoscaling

NIM Operator supports HPA based on inference-specific Prometheus metrics:
- `vllm:num_requests_waiting` — queue depth
- `vllm:num_requests_running` — active requests
- Custom DCGM metrics via GPU Operator

Requires Prometheus + Prometheus Adapter for custom metrics exposure.

#### 3.6.7 Monitoring

- Prometheus metrics at `/v1/metrics`
- ServiceMonitor support via `spec.metrics.enabled: true`
- Latency, throughput, queue depth, GPU utilization
- Aggregated logging across namespaces

#### 3.6.8 Air-Gapped Deployment

NIMCache supports air-gapped environments — pre-download models on a connected machine, copy PVCs to air-gapped cluster. Critical for government/FedRAMP deployments.

#### 3.6.9 NIM Operator + Dynamo (Experimental)

The NIM Operator now includes **experimental Dynamo CRDs** for disaggregated inference within the Kubernetes-native NIM workflow. This merges NIM's ease-of-deployment with Dynamo's multi-node disaggregation.

---

## 4. NVIDIA Mission Control — Cluster Management

### 4.1 What It Is

NVIDIA Mission Control is the unified operations platform for AI factories. It combines:

| Component | Function |
|-----------|----------|
| **Base Command Manager (BCM)** | Cluster provisioning, OS imaging, bare-metal management, monitoring dashboards |
| **Run:AI** (acquired ~$700M, 2024) | GPU scheduling, workload orchestration, resource quotas, multi-tenant GPU sharing |
| **GPU Operator** | Kubernetes-native GPU driver management, DCGM monitoring, MIG support |
| **Network Operator** | InfiniBand/RoCE fabric management |

### 4.2 Base Command Manager

**Now FREE** for all cluster sizes (up to 8 accelerators per system). Enterprise support available separately.

**Capabilities:**
- Automated cluster provisioning (bare-metal to Kubernetes in minutes)
- Supports clusters from 2 nodes to hundreds of thousands
- Real-time GPU/memory utilization dashboards (drag-and-drop customizable)
- Dual orchestration: Kubernetes AND Slurm (same cluster)
- OS imaging and node management
- Heterogeneous cluster support (mix GPU types)

**Licensing tiers:**
| Tier | Cost | Support |
|------|------|---------|
| BCM Essentials (free) | $0 | Community forums only |
| BCM + Enterprise Support | Included with NVAIE or Mission Control purchase | 24/7 enterprise |

### 4.3 Run:AI — GPU Scheduling

Run:AI is now NVIDIA's GPU orchestration engine, integrated into Mission Control:

- **GPU virtualization**: Fraction GPUs for smaller workloads (e.g., give a job 0.5 GPU)
- **Fair-share scheduling**: Multi-tenant GPU quotas with preemption
- **Gang scheduling**: All-or-nothing allocation for distributed training
- **Topology-aware placement**: Considers NVLink, NVSwitch, InfiniBand topology
- **Workload types**: Training, inference, interactive (notebooks), batch
- **5x GPU utilization improvement** vs static allocation (NVIDIA's claim)

### 4.4 How to Provision a K8s Cluster

```
BCM provisions bare-metal nodes
    → OS imaging (Ubuntu 24.04)
    → NVIDIA drivers + CUDA toolkit
    → GPU Operator (auto-manages GPU drivers in K8s)
    → Network Operator (InfiniBand fabric)
    → Kubernetes control plane
    → Run:AI scheduler plugin
    → Monitoring stack (Prometheus + Grafana)
```

BCM handles the entire stack from bare metal to running Kubernetes cluster. No manual driver installation, no manual K8s setup.

### 4.5 Monitoring Dashboard

- Real-time GPU utilization, memory, temperature, power
- Job queue depth and scheduling efficiency
- Per-tenant resource consumption
- Cluster health and node status
- Customizable drag-and-drop widgets
- Exportable metrics to external monitoring (Datadog, Splunk, etc.)

---

## 5. The Complete Token-Serving Pipeline

### 5.1 End-to-End Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    NVIDIA-PROVIDED STACK                        │
│                                                                 │
│  ┌───────────────┐  ┌──────────────┐  ┌──────────────────┐    │
│  │ Base Command   │  │  Run:AI      │  │  GPU Operator    │    │
│  │ Manager        │  │  Scheduler   │  │  + Network Op    │    │
│  │ (bare metal →  │  │  (GPU quota, │  │  (drivers,       │    │
│  │  K8s cluster)  │  │  sharing)    │  │  DCGM, fabric)   │    │
│  └───────┬───────┘  └──────┬───────┘  └────────┬─────────┘    │
│          └─────────────────┼───────────────────┘               │
│                            ▼                                    │
│  ┌─────────────────────────────────────────────────────┐       │
│  │              Kubernetes Cluster                      │       │
│  │  ┌─────────────────────────────────────────────┐    │       │
│  │  │           NIM Operator                       │    │       │
│  │  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  │    │       │
│  │  │  │ NIMCache  │  │NIMService│  │NIMPipeline│  │    │       │
│  │  │  │(model DL) │  │(deploy)  │  │(multi-svc)│  │    │       │
│  │  │  └──────────┘  └──────────┘  └──────────┘  │    │       │
│  │  └─────────────────────────────────────────────┘    │       │
│  │  ┌─────────────────────────────────────────────┐    │       │
│  │  │           Dynamo 1.0                         │    │       │
│  │  │  KV Router → Prefill Pool → Decode Pool      │    │       │
│  │  │  KVBM (multi-tier) + NIXL (data transfer)    │    │       │
│  │  │  GPU Planner (autoscale) + Grove (topology)   │    │       │
│  │  └─────────────────────────────────────────────┘    │       │
│  │  ┌─────────────────────────────────────────────┐    │       │
│  │  │      NIM Containers (per model)              │    │       │
│  │  │  Llama 70B │ DeepSeek R1 │ Mixtral │ ...     │    │       │
│  │  │  OpenAI API on :8000 each                    │    │       │
│  │  └─────────────────────────────────────────────┘    │       │
│  └─────────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ADC-BUILT LAYER                              │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐     │
│  │ API Gateway   │  │  Auth +      │  │  Billing +       │     │
│  │ (rate limit,  │  │  API Keys    │  │  Token Metering  │     │
│  │  routing)     │  │  (per-tenant)│  │  (usage tracking)│     │
│  └──────┬───────┘  └──────┬───────┘  └────────┬─────────┘     │
│         └─────────────────┼───────────────────┘                │
│                           ▼                                     │
│  ┌─────────────────────────────────────────────────────┐       │
│  │              Customer Portal                         │       │
│  │  API key management, usage dashboards, billing,      │       │
│  │  model catalog, docs, support                        │       │
│  └─────────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
                     Customer Applications
                 (OpenAI SDK, LangChain, etc.)
```

### 5.2 What NVIDIA Provides (Everything Below the API Gateway)

| Component | Provided By | Notes |
|-----------|-------------|-------|
| Cluster provisioning | Base Command Manager | Free |
| GPU scheduling | Run:AI (Mission Control) | Included with NVAIE |
| GPU drivers + monitoring | GPU Operator + DCGM | Free / open source |
| InfiniBand fabric | Network Operator | Free / open source |
| Model containers | NIM | NVAIE license for production |
| Inference optimization | Dynamo 1.0 | Open source |
| KV caching + routing | Dynamo KVBM + Router | Open source |
| Multi-node orchestration | Dynamo + Grove | Open source |
| Autoscaling | Dynamo GPU Planner + NIM HPA | Open source |
| Monitoring metrics | NIM /v1/metrics + DCGM | Prometheus-compatible |

### 5.3 What ADC Must Build Custom

| Component | Purpose | Build vs Buy |
|-----------|---------|-------------|
| **API Gateway** | Rate limiting, request routing, DDoS protection | Kong / Traefik / NGINX (open source) or cloud (Cloudflare) |
| **Authentication** | API key issuance, OAuth2/JWT, per-tenant isolation | Build or use Auth0/Clerk |
| **Token Metering** | Count input/output tokens per request per customer | Build — intercept NIM responses, count tokens, log to DB |
| **Billing Engine** | Usage-based billing, invoicing, payment processing | Stripe Billing + custom metering integration |
| **Customer Portal** | API key management, usage dashboards, docs | Build — Next.js or similar |
| **Model Router** | Route customer requests to correct NIM backend | Build — thin routing layer (model name → NIM endpoint) |
| **SLA Monitoring** | Per-customer latency/throughput tracking, alerting | Grafana + custom dashboards on NIM metrics |
| **Audit Logging** | Compliance, request/response logging (opt-in) | ELK stack or similar |

### 5.4 Request Flow (Customer to Token)

```
1. Customer sends POST /v1/chat/completions to api.adc3k.com
2. Cloudflare → DDoS protection, TLS termination
3. API Gateway → validates API key, checks rate limit, checks quota
4. Model Router → maps request to correct NIM backend cluster
5. Dynamo Frontend → receives request
6. KV-Aware Router → checks cache, selects optimal worker
7. Prefill Worker → processes input, generates KV cache
8. NIXL → transfers KV cache to decode worker
9. Decode Worker → generates tokens (streaming SSE)
10. Tokens flow back through: Dynamo → NIM → Gateway → Customer
11. Token Metering → counts tokens, logs usage
12. Billing Engine → aggregates usage, generates invoice
```

---

## 6. Licensing and Costs

### 6.1 What's Open Source (Free)

| Component | License | Cost |
|-----------|---------|------|
| **Dynamo 1.0** | Apache 2.0 | $0 |
| **GPU Operator** | Apache 2.0 | $0 |
| **Network Operator** | Apache 2.0 | $0 |
| **NIM Operator** | Apache 2.0 (operator code) | $0 |
| **Base Command Manager Essentials** | Free license (1-year renewable) | $0 |
| **NIM (development/testing)** | Free for development | $0 |
| **NVIDIA Build API** | Free tier for prototyping | $0 (rate-limited) |

### 6.2 What Requires NVIDIA AI Enterprise (NVAIE) License

Production deployment of NIM containers requires NVAIE. Dynamo itself is open source, but NIM containers pulled from nvcr.io for production use require the license.

**Self-Managed Pricing (per GPU):**

| Term | Cost per GPU | Notes |
|------|-------------|-------|
| 1 year subscription | $4,500 | Includes Business Standard support |
| 2 year subscription | $9,000 | |
| 3 year subscription | $13,500 | |
| 5 year subscription | $18,000 | Multi-year discount |
| Perpetual license | $22,500 | Includes 5 years support |

**EDU / NVIDIA Inception Pricing (75% discount):**

| Term | Cost per GPU |
|------|-------------|
| 1 year | $1,125 |
| 5 year | $4,500 |
| Perpetual | $5,625 |

> **Critical for ADC**: H100, H200 NVL, and A800 PCIe GPUs come with a **5-year NVAIE subscription included at no additional cost**. Blackwell NVL72 racks likely include this as well (confirm with NVIDIA rep). This means ADC's GPU hardware purchase may already cover the software license.

**Cloud Marketplace (pay-as-you-go):**
- Production: $1/hour/GPU + CSP instance cost
- Development: Free (or BYOL)

### 6.3 Mission Control / Run:AI Pricing

Mission Control pricing is bundled differently:
- **BCM Essentials**: Free, community support only
- **Mission Control (full)**: Included with NVAIE at enterprise tier, or purchased separately (contact NVIDIA sales)
- **Run:AI**: Now part of Mission Control, not sold separately

### 6.4 ADC Cost Model (Per NVL72 Rack)

Assuming NVL72 rack with 72 Blackwell GPUs, NVAIE included with hardware:

| Item | Annual Cost | Notes |
|------|------------|-------|
| NVAIE license (72 GPUs) | $0 — $324,000 | $0 if included with hardware, $4,500/GPU/yr if not |
| Dynamo | $0 | Open source |
| BCM Essentials | $0 | Free |
| Enterprise Support (optional) | Contact NVIDIA | 24/7 support |
| ADC custom software | Engineering cost | API gateway, billing, portal |

**Bottom line for ADC**: If NVAIE is bundled with the NVL72 rack purchase (highly likely given H100/H200 precedent), the entire inference stack software cost is **$0**. The only cost is ADC's custom billing/auth layer.

---

## 7. ADC-Specific Deployment Plan

### 7.1 Phase 1 — Trappeys Proof of Concept

**Hardware**: Initial NVL72 rack(s)
**Stack**:
1. Base Command Manager Essentials (free) for cluster provisioning
2. GPU Operator for driver management
3. NIM Operator for model deployment
4. Dynamo in aggregated mode (single-node, simpler to start)
5. NIM containers: Llama 3.1 70B, Mixtral 8x7B
6. Simple API gateway (Kong or Traefik)
7. Token metering prototype

**Goal**: Serve first tokens to pilot customers. Validate throughput/latency numbers.

### 7.2 Phase 2 — Multi-Model + Disaggregation

**Hardware**: 2-4 NVL72 racks
**Stack additions**:
1. Dynamo disaggregated mode (separate prefill/decode workers)
2. KV-Aware Router for multi-tenant cache efficiency
3. KVBM with CPU offload tier
4. Additional NIM models: DeepSeek R1, Qwen, embedding models
5. Full billing engine (Stripe integration)
6. Customer portal launch

**Goal**: Production neocloud service. Multiple models, multiple customers.

### 7.3 Phase 3 — Willow Glen Scale

**Hardware**: 8+ NVL72 racks, InfiniBand fabric (Quantum switches)
**Stack additions**:
1. Full Mission Control (Run:AI scheduler for multi-tenant)
2. Dynamo multi-node inference for 671B+ models
3. Grove for NVLink-topology-aware scheduling
4. KVBM with remote storage tier (VAST/WEKA)
5. NIMPipeline for coordinated multi-model deployments
6. NIMBuild for pre-optimized TensorRT-LLM engines
7. Dynamo + Groq hybrid (Groq for decode, Dynamo for prefill) — 35x tokens/watt

**Goal**: Full-scale Louisiana AI factory. Hundreds of customers. Token factory at scale.

### 7.4 ADC Custom Software Requirements

| Component | Priority | Estimated Effort |
|-----------|----------|-----------------|
| API Gateway + Rate Limiting | P0 (launch blocker) | 1-2 weeks (Kong/Traefik config) |
| API Key Management | P0 | 2-3 weeks |
| Token Metering | P0 | 2-3 weeks |
| Billing Integration (Stripe) | P0 | 3-4 weeks |
| Customer Dashboard | P1 | 4-6 weeks |
| Model Catalog UI | P1 | 2-3 weeks |
| SLA Monitoring Dashboard | P1 | 2-3 weeks |
| Audit Logging | P2 | 2-3 weeks |
| Multi-tenant Isolation | P1 | 3-4 weeks |

### 7.5 Key Contacts at NVIDIA

- **Jim Hennessy** — Getting ADC into NPN (NVIDIA Partner Network)
- **Marc Spieler** — NVIDIA Energy vertical (CERAWeek contact)
- **NPN Portal** — Invitation-only, Jim is handling registration

### 7.6 Certification Path

```
NPN Registration (Jim Hennessy)
    → DGX-Ready Certification (Willow Glen)
    → NCP (NVIDIA Cloud Partner)
    → Reference Platform NCP
```

Each certification level unlocks deeper NVIDIA support, co-marketing, and priority hardware allocation.

---

## Appendix A: Quick Reference Commands

### Deploy Dynamo on K8s
```bash
helm repo add nvidia https://helm.ngc.nvidia.com/nvidia/ai-dynamo
helm install dynamo-crds nvidia/dynamo-crds
helm install dynamo-platform nvidia/dynamo-platform \
  --namespace dynamo-system --create-namespace \
  --set "grove.enabled=true" \
  --set "kai-scheduler.enabled=true"
```

### Deploy NIM Container (Docker)
```bash
export NGC_API_KEY="your-key"
echo "$NGC_API_KEY" | docker login nvcr.io --username '$oauthtoken' --password-stdin
docker run --rm --gpus all --shm-size=16GB \
  -e NGC_API_KEY=$NGC_API_KEY \
  -v ~/.cache/nim:/opt/nim/.cache \
  -p 8000:8000 \
  nvcr.io/nim/meta/llama-3.1-8b-instruct:latest
```

### Test NIM Endpoint
```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"meta/llama-3.1-8b-instruct","messages":[{"role":"user","content":"Hello"}],"max_tokens":64}'
```

### Check NIM Health
```bash
curl http://localhost:8000/v1/health/ready
curl http://localhost:8000/v1/health/live
curl http://localhost:8000/v1/models
curl http://localhost:8000/v1/metrics
```

---

## Appendix B: Key URLs

| Resource | URL |
|----------|-----|
| Dynamo GitHub | https://github.com/ai-dynamo/dynamo |
| Dynamo Docs | https://docs.nvidia.com/dynamo/latest/ |
| NIM Catalog | https://build.nvidia.com/models |
| NIM Docs | https://docs.nvidia.com/nim/large-language-models/latest/ |
| NIM Operator | https://github.com/NVIDIA/k8s-nim-operator |
| NIM Deploy Examples | https://github.com/NVIDIA/nim-deploy |
| NIM Operator Docs | https://docs.nvidia.com/nim-operator/latest/ |
| NVAIE Pricing | https://docs.nvidia.com/ai-enterprise/planning-resource/licensing-guide/latest/pricing.html |
| BCM Docs | https://docs.nvidia.com/base-command-manager/index.html |
| Mission Control | https://docs.nvidia.com/mission-control/index.html |
| GPU Operator | https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/ |
| NGC Container Registry | https://catalog.ngc.nvidia.com |
| Dynamo on AWS EKS | https://aws.amazon.com/blogs/machine-learning/accelerate-generative-ai-inference-with-nvidia-dynamo-and-amazon-eks/ |
| Dynamo on Azure AKS | https://blog.aks.azure.com/2025/10/24/dynamo-on-aks |
| Dynamo on GKE | https://cloud.google.com/blog/products/compute/ai-inference-recipe-using-nvidia-dynamo-with-ai-hypercomputer |

---

*Compiled by Mission Control. Last updated 2026-03-25.*
