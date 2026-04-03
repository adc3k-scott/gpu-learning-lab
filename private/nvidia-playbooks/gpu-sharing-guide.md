# NVIDIA GPU Sharing & Monitoring — ADC Operations Guide
Last updated: 2026-03-25
Source: NVIDIA MIG, k8s-device-plugin, DCGM docs

## THREE WAYS TO SHARE GPUs (pick per use case)

### 1. MIG (Multi-Instance GPU) — Hardware Isolation
- Partition one GPU into up to 7 isolated instances
- Each instance has dedicated compute, memory, cache
- Hardware-level isolation between tenants
- Supported on A100, H100, Blackwell
- Two strategies:
  - **single** — all MIG devices same size, exposed as nvidia.com/gpu
  - **mixed** — different sizes, exposed as nvidia.com/mig-3g.20gb etc.
- **Best for:** Multi-tenant inference, different customers on same GPU
- **ADC use:** Sell fractional GPU access to smaller customers

### 2. Time-Slicing — Software Sharing
- Multiple containers share same GPU via CUDA time-slicing
- No memory isolation — all workloads share GPU memory
- No compute isolation — CUDA gives equal time to all processes
- Config: set replicas per GPU (e.g. replicas=10 turns 8 GPUs into 80 resources)
- If one workload crashes, all crash (shared fault domain)
- **Best for:** Dev/test, batch inference, non-critical workloads
- **ADC use:** Maximize utilization during off-peak hours

### 3. MPS (CUDA Multi-Process Service) — Space Partitioning
- Control daemon manages access to shared GPU
- Memory AND compute explicitly partitioned per workload
- Enforced limits per client
- Each client gets 1/N of memory and compute
- **Best for:** Parallel inference serving, production multi-tenant
- **ADC use:** Production token serving with guaranteed resource allocation

## MIG Quick Setup
```bash
# Enable MIG on GPU 0
sudo nvidia-smi -mig 1

# Create 7 equal slices (1g.5gb each on A100-40GB)
sudo nvidia-smi mig -cgi 19,19,19,19,19,19,19 -C

# Verify
nvidia-smi -L
# Shows 7 MIG devices

# GPU Operator handles this automatically with MIG Manager
# Set strategy in ClusterPolicy: mig.strategy=mixed
```

## DCGM Monitoring — GPU Telemetry
- DCGM Exporter scrapes GPU metrics for Prometheus
- Grafana dashboard ID: 12239 (pre-built NVIDIA dashboard)
- Metrics include: temperature, power, utilization, memory, ECC errors, XID errors
- ServiceMonitor included for Kubernetes integration
- **ADC use:** Mission Control dashboard shows real-time GPU health

### Key Prometheus Metrics
- DCGM_FI_DEV_GPU_UTIL — GPU utilization %
- DCGM_FI_DEV_MEM_COPY_UTIL — memory utilization %
- DCGM_FI_DEV_GPU_TEMP — temperature
- DCGM_FI_DEV_POWER_USAGE — power draw
- DCGM_FI_DEV_ECC_DBE_VOL — double-bit ECC errors (critical)
- DCGM_FI_DEV_XID_ERRORS — XID errors (GPU faults)

### Alert Rules for ADC
- GPU temp > 85C → warning
- GPU temp > 95C → critical (throttling imminent)
- ECC errors > 0 → investigate hardware
- XID errors → GPU fault, may need restart
- Utilization < 30% sustained → under-utilized, add workloads

## k8s-device-plugin — How GPUs Become Kubernetes Resources
- DaemonSet that runs on every GPU node
- Auto-detects GPUs and registers them with kubelet
- Resources appear as nvidia.com/gpu in kubectl describe node
- Supports MIG, time-slicing, MPS via config
- Apache 2.0 open source
- Current version: v0.17.1 (v0.19.0 in development)

### Quick Deploy
```bash
helm repo add nvdp https://nvidia.github.io/k8s-device-plugin
helm repo update
helm upgrade -i nvdp nvdp/nvidia-device-plugin \
    --namespace nvidia-device-plugin \
    --create-namespace \
    --version 0.17.1
```

Note: GPU Operator deploys this automatically — no separate install needed if using GPU Operator.

## ADC Sharing Strategy by Customer Tier

| Customer Tier | Sharing Method | Isolation | Use Case |
|--------------|---------------|-----------|----------|
| Enterprise ($45/M tokens) | Dedicated GPU or MIG | Hardware | Mission-critical, guaranteed performance |
| Premium ($6/M tokens) | MIG or MPS | Hardware/enforced | Production inference, SLA-backed |
| Standard ($1/M tokens) | MPS | Enforced partition | General inference |
| Batch ($0.20/M tokens) | Time-slicing | None (shared) | Dev/test, async, non-critical |
| Real-time ($150/M tokens) | Dedicated GPU | Full hardware | Groq decode, <50ms latency |
