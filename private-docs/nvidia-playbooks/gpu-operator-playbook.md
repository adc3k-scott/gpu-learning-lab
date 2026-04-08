# NVIDIA GPU Operator — ADC Deployment Playbook

> **Version**: GPU Operator v26.3.0 | Driver 580.126.20 | CUDA Toolkit 1.19.0
> **Last Updated**: 2026-03-25
> **Scope**: Willow Glen (SuperPOD), Trappeys (proof-of-concept), MARLIE 1 (edge), ADC 3K pods

---

## Table of Contents

1. [What the GPU Operator Does](#1-what-the-gpu-operator-does)
2. [Supported Hardware and Platforms](#2-supported-hardware-and-platforms)
3. [Architecture and Components](#3-architecture-and-components)
4. [Prerequisites Checklist](#4-prerequisites-checklist)
5. [Standard Installation](#5-standard-installation)
6. [Pre-Installed Driver Mode (DGX/HGX Systems)](#6-pre-installed-driver-mode-dgxhgx-systems)
7. [MIG — Multi-Instance GPU Partitioning](#7-mig--multi-instance-gpu-partitioning)
8. [Time-Slicing — GPU Sharing Without MIG](#8-time-slicing--gpu-sharing-without-mig)
9. [GPUDirect RDMA and Storage](#9-gpudirect-rdma-and-storage)
10. [DCGM Exporter — Monitoring with Prometheus/Grafana](#10-dcgm-exporter--monitoring-with-prometheusgrafana)
11. [Air-Gapped Deployment (Defense/Secure Sites)](#11-air-gapped-deployment-defensesecure-sites)
12. [Driver Upgrades — Rolling Updates](#12-driver-upgrades--rolling-updates)
13. [Operator Upgrades](#13-operator-upgrades)
14. [Base Command Manager Integration](#14-base-command-manager-integration)
15. [NVL72 Rack Considerations](#15-nvl72-rack-considerations)
16. [Troubleshooting](#16-troubleshooting)
17. [ADC Site-Specific Deployment Matrix](#17-adc-site-specific-deployment-matrix)

---

## 1. What the GPU Operator Does

The GPU Operator automates provisioning of every NVIDIA software component needed to run GPU workloads on Kubernetes. Without it, you manually install drivers, container toolkit, device plugins, and monitoring on every node. The Operator does all of it via DaemonSets controlled by a single `ClusterPolicy` custom resource.

**Components it manages:**
- NVIDIA GPU drivers (containerized or pre-installed)
- NVIDIA Container Toolkit
- Kubernetes Device Plugin (advertises GPUs to scheduler)
- GPU Feature Discovery (auto-labels nodes with GPU model, memory, driver version)
- Node Feature Discovery (detects PCI devices, CPU features)
- DCGM + DCGM Exporter (telemetry/monitoring)
- MIG Manager (partitions GPUs into isolated instances)
- GDRCopy Driver (low-latency GPU memory copies)
- Confidential Computing Manager
- KubeVirt GPU Device Plugin (VM passthrough and vGPU)
- Driver Manager (handles driver lifecycle and upgrades)

**How it detects GPU nodes:** Node Feature Discovery scans PCI bus for vendor ID `0x10DE` (NVIDIA). Nodes with that label get all components deployed automatically. No manual per-node setup.

---

## 2. Supported Hardware and Platforms

### Supported GPUs (v26.3.0)

**Blackwell (ADC primary target):**
- DGX B300, DGX B200, DGX Spark
- HGX B200, HGX B300
- HGX GB200 NVL72, HGX GB200 NVL4, HGX GB300 NVL72

**Hopper:**
- H100, H100 NVL, H200, H200 NVL, H800, H20
- DGX H100, DGX H200, HGX H100, HGX H200
- GH200 (requires open kernel module)

**Ampere:**
- A100, A100X, A800, A40, A30, A30X, A16, A10, A2
- DGX A100, HGX A100

**Older (edge/lab use):**
- L40, L40S, L4, L20, T4, V100, P100, P40, P4

**Professional:**
- RTX PRO 6000 Blackwell, RTX PRO 6000D, RTX Pro 4500 Blackwell
- RTX A6000, A5000, A4500, A4000

### Kubernetes Versions
- 1.32 through 1.35

### Linux Distributions
- Ubuntu 20.04, 22.04, 24.04 LTS
- RHEL 8.8, 8.10, 9.2, 9.4, 9.6, 9.7, 10.0, 10.1
- Red Hat CoreOS 4.17-4.21
- Rocky Linux 9.7

### Container Runtimes
- containerd 1.7-2.2
- CRI-O (all supported OS versions)

### Architectures
- x86_64 (primary)
- ARM64 (A100X, A30X, IGX Orin, DGX Spark, GB200/GB300 NVL72)

---

## 3. Architecture and Components

```
┌─────────────────────────────────────────────────────┐
│                  ClusterPolicy CRD                   │
│         (single source of truth for config)          │
└─────────────────────┬───────────────────────────────┘
                      │ watches
┌─────────────────────▼───────────────────────────────┐
│              GPU Operator Controller                  │
│           (gpu-operator namespace)                   │
└─────────────────────┬───────────────────────────────┘
                      │ deploys DaemonSets
    ┌─────────────────┼─────────────────┐
    ▼                 ▼                 ▼
┌────────┐    ┌────────────┐    ┌──────────────┐
│  NFD   │    │   Driver   │    │   Toolkit    │
│DaemonSet│    │ DaemonSet  │    │  DaemonSet   │
└────────┘    └────────────┘    └──────────────┘
    ▼                 ▼                 ▼
┌────────┐    ┌────────────┐    ┌──────────────┐
│  GPU   │    │  Device    │    │    DCGM      │
│Feature │    │  Plugin    │    │  Exporter    │
│Discover│    │ DaemonSet  │    │  DaemonSet   │
└────────┘    └────────────┘    └──────────────┘
                      ▼
              ┌────────────┐
              │    MIG     │
              │  Manager   │
              │ DaemonSet  │
              └────────────┘
```

**State machine**: The Operator deploys components sequentially with validation at each step. It schedules test CUDA workloads (vectoradd) to verify each stage before proceeding. If validation fails, it stops and reports.

**CDI (Container Device Interface)**: Default since v25.10.0. Standardizes GPU injection across container runtimes. No runtime-specific plugins needed. Transparent to workloads.

---

## 4. Prerequisites Checklist

Before touching Helm:

- [ ] **Kubernetes cluster running** (1.32-1.35) with functional control plane
- [ ] **kubectl and helm installed** on admin workstation
- [ ] **Container runtime**: containerd 1.7+ or CRI-O configured on all GPU worker nodes
- [ ] **Matching OS**: All GPU worker nodes should run same OS version (unless using pre-installed drivers)
- [ ] **Nouveau driver blacklisted** on all GPU nodes:
  ```bash
  # /etc/modprobe.d/blacklist-nouveau.conf
  blacklist nouveau
  options nouveau modeset=0
  # Then: update-initramfs -u && reboot
  ```
- [ ] **Secure Boot disabled** in BIOS (GPU Operator does not support EFI Secure Boot)
- [ ] **IOMMU enabled** (if using KubeVirt/VM passthrough): `intel_iommu=on` or `amd_iommu=on` in kernel params
- [ ] **Kernel modules loaded**: `i2c_core`, `ipmi_msghandler`
- [ ] **Check if NFD already running**:
  ```bash
  kubectl get nodes -o json | jq '.items[].metadata.labels | keys | any(startswith("feature.node.kubernetes.io"))'
  ```
  If `true`, set `--set nfd.enabled=false` during install to avoid conflicts.

---

## 5. Standard Installation

### Step 1: Create namespace with privileged PSA
```bash
kubectl create ns gpu-operator
kubectl label --overwrite ns gpu-operator pod-security.kubernetes.io/enforce=privileged
```

### Step 2: Add NVIDIA Helm repo
```bash
helm repo add nvidia https://helm.ngc.nvidia.com/nvidia
helm repo update
```

### Step 3: Install with defaults
```bash
helm install gpu-operator \
  -n gpu-operator --create-namespace \
  nvidia/gpu-operator \
  --version=v26.3.0 \
  --wait
```

### Step 4: Verify
```bash
# Watch all pods come up
kubectl get pods -n gpu-operator -w

# Run CUDA test
cat <<'EOF' | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: cuda-vectoradd
spec:
  restartPolicy: OnFailure
  containers:
  - name: cuda-vectoradd
    image: nvcr.io/nvidia/k8s/cuda-sample:vectoradd-cuda11.7.1-ubuntu20.04
    resources:
      limits:
        nvidia.com/gpu: 1
EOF

# Check result
kubectl logs cuda-vectoradd
# Expected: "Test PASSED"
kubectl delete pod cuda-vectoradd
```

### Common Install Variations

**Open kernel modules (required for GH200, recommended for Blackwell):**
```bash
helm install gpu-operator \
  -n gpu-operator --create-namespace \
  nvidia/gpu-operator --version=v26.3.0 \
  --set driver.kernelModuleType=open
```

**Custom containerd socket/config paths:**
```bash
helm install gpu-operator -n gpu-operator --create-namespace \
  nvidia/gpu-operator --version=v26.3.0 \
  --set toolkit.env[0].name=CONTAINERD_CONFIG \
  --set toolkit.env[0].value=/etc/containerd/config.toml \
  --set toolkit.env[1].name=CONTAINERD_SOCKET \
  --set toolkit.env[1].value=/run/containerd/containerd.sock
```

**RHEL/Rocky with SELinux:**
```bash
helm install gpu-operator \
  -n gpu-operator --create-namespace \
  nvidia/gpu-operator --version=v26.3.0 \
  --set toolkit.version=v1.16.1-ubi8
```
SELinux must be in permissive or enforcing mode (not disabled).

**Exclude specific nodes from getting drivers:**
```bash
kubectl label nodes $NODE nvidia.com/gpu.deploy.driver=false
```

**Exclude nodes from all GPU Operator components:**
```bash
kubectl label nodes $NODE nvidia.com/gpu.deploy.operands=false
```

---

## 6. Pre-Installed Driver Mode (DGX/HGX Systems)

DGX systems ship with NVIDIA drivers baked into the OS (DGX OS). The GPU Operator should NOT deploy containerized drivers on these nodes. Same applies to any node where you installed drivers manually.

### DGX / Pre-installed drivers only
```bash
helm install gpu-operator \
  -n gpu-operator --create-namespace \
  nvidia/gpu-operator --version=v26.3.0 \
  --set driver.enabled=false
```

### Pre-installed drivers AND toolkit
If the node already has both NVIDIA drivers and nvidia-container-toolkit:
```bash
# First ensure nvidia is the default runtime
# Then:
helm install gpu-operator \
  -n gpu-operator --create-namespace \
  nvidia/gpu-operator --version=v26.3.0 \
  --set driver.enabled=false \
  --set toolkit.enabled=false
```

### Detection behavior
The Operator auto-detects: "If a node has an NVIDIA GPU driver installed in the operating system, then no driver container runs on the node." This means mixed clusters (some DGX, some bare metal) work automatically — DGX nodes skip driver pods, bare metal nodes get them.

### MIG on DGX with pre-installed drivers
MIG Manager still works. It stops systemd services listed in the `default-gpu-clients` ConfigMap before reconfiguring MIG geometry, then restarts them.

---

## 7. MIG — Multi-Instance GPU Partitioning

MIG (Multi-Instance GPU) splits a single physical GPU into up to 7 isolated instances, each with dedicated memory, cache, and compute. Available on A100, A30, H100, H200, B200, and Blackwell GPUs.

### When to use MIG
- Multi-tenant inference (university partners, managed customers)
- Isolating workloads that need guaranteed GPU memory and fault isolation
- Running multiple small models on one GPU

### Strategies

| Strategy | Meaning | Use case |
|----------|---------|----------|
| `single` | ALL GPUs on a node use MIG | Dedicated inference nodes |
| `mixed` | Some GPUs use MIG, others don't | Mixed training + inference nodes |

### Installation with MIG
```bash
helm install gpu-operator \
  -n gpu-operator --create-namespace \
  nvidia/gpu-operator --version=v26.3.0 \
  --set mig.strategy=single
```

### Configure MIG profiles on a node
```bash
# Apply a profile — all GPUs get 1g.10gb slices
kubectl label nodes <node-name> nvidia.com/mig.config=all-1g.10gb --overwrite

# Check status
kubectl get nodes <node-name> --show-labels | grep mig.config.state
# state cycles: pending -> success (or failed)
```

### Built-in profiles
- `all-disabled` — MIG off (default)
- `all-enabled` — MIG on, no specific geometry
- `all-1g.10gb` — 7x smallest instances (A100 40GB)
- `all-2g.20gb` — 3x medium instances
- `all-3g.40gb` — 2x large instances
- `all-balanced` — mixed sizes

### Custom MIG ConfigMap
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: custom-mig-config
  namespace: gpu-operator
data:
  config.yaml: |
    version: v1
    mig-configs:
      all-disabled:
        - devices: all
          mig-enabled: false

      inference-7way:
        - devices: all
          mig-enabled: true
          mig-devices:
            "1g.10gb": 7

      training-plus-inference:
        - devices: [0,1]
          mig-enabled: false
        - devices: [2,3]
          mig-enabled: true
          mig-devices:
            "3g.40gb": 1
            "1g.10gb": 4
```

Install with custom config:
```bash
helm install gpu-operator nvidia/gpu-operator \
  -n gpu-operator --create-namespace \
  --version=v26.3.0 \
  --set mig.strategy=mixed \
  --set migManager.config.name=custom-mig-config
```

### Reconfiguration workflow (what happens when you change the label)
1. MIG Manager sees label change, sets `mig.config.state: pending`
2. Stops all GPU pods and host GPU clients on that node
3. Enables/disables MIG mode via `nvidia-smi`
4. Applies geometry via `mig-parted`
5. Restarts pods, sets `mig.config.state: success`

**Important**: This causes brief GPU downtime on the node. Schedule during maintenance windows for production.

### Requesting MIG instances in pods
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: inference-pod
spec:
  containers:
  - name: model
    image: my-inference-image:latest
    resources:
      limits:
        nvidia.com/gpu: 1
  nodeSelector:
    nvidia.com/gpu.product: H100-SXM5-80GB-MIG-1g.10gb
```

### Disable MIG
```bash
kubectl label nodes <node-name> nvidia.com/mig.config=all-disabled --overwrite
```

### Monitor MIG Manager
```bash
kubectl logs -n gpu-operator -l app=nvidia-mig-manager -f
```

---

## 8. Time-Slicing — GPU Sharing Without MIG

Time-slicing multiplexes GPU access across multiple pods. Unlike MIG, there is NO memory isolation and NO fault isolation. All pods share the full GPU and get equal time slices.

### When to use time-slicing
- Older GPUs without MIG support (T4, V100, L4)
- Lightweight inference workloads that don't need isolation
- Dev/test environments with GPU oversubscription
- Combined with MIG for further subdivision

### When NOT to use time-slicing
- Production multi-tenant (use MIG instead — memory isolation matters)
- Workloads sensitive to GPU memory contention
- Training jobs (need dedicated GPU memory)

### ConfigMap
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: time-slicing-config
  namespace: gpu-operator
data:
  any: |-
    version: v1
    flags:
      migStrategy: none
    sharing:
      timeSlicing:
        renameByDefault: true
        failRequestsGreaterThanOne: true
        resources:
        - name: nvidia.com/gpu
          replicas: 4
```

**Key flags:**
- `renameByDefault: true` — advertises as `nvidia.com/gpu.shared` instead of `nvidia.com/gpu`. Prevents accidentally scheduling production training on shared GPUs.
- `failRequestsGreaterThanOne: true` — rejects pods requesting >1 GPU replica (requesting 2 does NOT give 2x compute, so fail it to prevent confusion).
- `replicas: 4` — each physical GPU advertises as 4 schedulable units.

### Apply cluster-wide
```bash
kubectl apply -f time-slicing-config.yaml

kubectl patch clusterpolicies.nvidia.com/cluster-policy \
  -n gpu-operator --type merge \
  -p '{"spec": {"devicePlugin": {"config": {"name": "time-slicing-config", "default": "any"}}}}'
```

### Apply per-node (different GPU models)
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: time-slicing-config
  namespace: gpu-operator
data:
  h100: |-
    version: v1
    sharing:
      timeSlicing:
        resources:
        - name: nvidia.com/gpu
          replicas: 2
  t4: |-
    version: v1
    sharing:
      timeSlicing:
        resources:
        - name: nvidia.com/gpu
          replicas: 8
```

Label nodes:
```bash
kubectl label node gpu-node-01 nvidia.com/device-plugin.config=h100
kubectl label node gpu-node-02 nvidia.com/device-plugin.config=t4
```

### Verify
```bash
kubectl describe node <node-name> | grep -A5 "Allocatable"
# Should show: nvidia.com/gpu: 16 (4 physical x 4 replicas)
```

Node labels change to include `-SHARED` suffix: `nvidia.com/gpu.product: H100-SXM5-80GB-SHARED`

### Limitations
- DCGM Exporter cannot associate metrics to individual containers when time-slicing is active
- ConfigMap changes require manual restart: `kubectl rollout restart -n gpu-operator daemonset/nvidia-device-plugin-daemonset`

---

## 9. GPUDirect RDMA and Storage

GPUDirect RDMA enables direct data transfer between GPUs and network adapters (InfiniBand/RoCE) over PCIe, bypassing CPU. GPUDirect Storage does the same for NVMe/storage. Critical for NVL72 NVLink/InfiniBand fabric performance.

### Two implementation paths

| Approach | Requirements | Recommended |
|----------|-------------|-------------|
| **DMA-BUF** (recommended) | Open kernel module, CUDA 11.7+, Linux kernel 5.12+, Turing+ GPU | Yes |
| **Legacy nvidia-peermem** | Any driver, MLNX_OFED/DOCA-OFED required | Only if DMA-BUF not possible |

### DMA-BUF with Network Operator
If you run NVIDIA Network Operator alongside GPU Operator (manages MOFED/DOCA drivers):
```bash
helm install gpu-operator \
  -n gpu-operator --create-namespace \
  nvidia/gpu-operator --version=v26.3.0
# DMA-BUF works automatically with open kernel module (default for Blackwell)
```

### DMA-BUF with host-installed MOFED
If MOFED/DOCA is installed directly on the host (not via Network Operator):
```bash
helm install gpu-operator \
  -n gpu-operator --create-namespace \
  nvidia/gpu-operator --version=v26.3.0 \
  --set driver.rdma.useHostMofed=true
```

### Legacy peermem (older systems)
```bash
helm install gpu-operator \
  -n gpu-operator --create-namespace \
  nvidia/gpu-operator --version=v26.3.0 \
  --set driver.rdma.enabled=true
```

### GPUDirect Storage
Requires open kernel module exclusively:
```bash
helm install gpu-operator \
  -n gpu-operator --create-namespace \
  nvidia/gpu-operator --version=v26.3.0 \
  --set gds.enabled=true
```

### Verify RDMA
Check for these containers in driver pods:
- `nvidia-driver-ctr` — main driver
- `nvidia-peermem-ctr` — peermem (legacy path only)
- `nvidia-fs-ctr` — GDS (if enabled)

Validation init container `mofed-validation` confirms network drivers are functional before GPU driver starts.

### ADC relevance
- **Willow Glen (NVL72 + InfiniBand)**: GPUDirect RDMA is mandatory. DMA-BUF path with Network Operator managing Quantum switches.
- **Trappeys**: GPUDirect RDMA for any multi-node training. Start with DMA-BUF.
- **MARLIE 1 (edge)**: GPUDirect Storage for fast model loading from NVMe.

---

## 10. DCGM Exporter — Monitoring with Prometheus/Grafana

DCGM (Data Center GPU Manager) Exporter collects GPU telemetry and exposes it as Prometheus metrics. Enabled by default in the GPU Operator.

### What it collects
- GPU utilization (compute and memory)
- GPU temperature
- Power draw
- Memory usage (used/free/total)
- ECC error counts (single-bit and double-bit)
- PCIe throughput
- NVLink throughput
- Clock speeds
- XID errors
- MIG instance metrics (when MIG enabled)

### Key Prometheus metrics
```
DCGM_FI_DEV_GPU_UTIL          — GPU utilization %
DCGM_FI_DEV_MEM_COPY_UTIL     — Memory bandwidth utilization %
DCGM_FI_DEV_GPU_TEMP           — GPU temperature (C)
DCGM_FI_DEV_POWER_USAGE        — Power usage (W)
DCGM_FI_DEV_FB_USED            — Framebuffer memory used (MiB)
DCGM_FI_DEV_FB_FREE            — Framebuffer memory free (MiB)
DCGM_FI_DEV_ECC_SBE_VOL_TOTAL  — Single-bit ECC errors (volatile)
DCGM_FI_DEV_ECC_DBE_VOL_TOTAL  — Double-bit ECC errors (volatile)
DCGM_FI_DEV_PCIE_TX_THROUGHPUT — PCIe TX bytes
DCGM_FI_DEV_PCIE_RX_THROUGHPUT — PCIe RX bytes
DCGM_FI_DEV_NVLINK_BANDWIDTH_TOTAL — NVLink bandwidth
DCGM_FI_DEV_XID_ERRORS         — XID error codes
```

### Prometheus ServiceMonitor
If running Prometheus Operator (kube-prometheus-stack), the GPU Operator automatically creates a ServiceMonitor. Prometheus discovers DCGM Exporter endpoints without manual config.

To verify:
```bash
kubectl get servicemonitor -n gpu-operator
kubectl get endpoints -n gpu-operator | grep dcgm
```

### Custom metrics ConfigMap
Override which metrics are collected:
```bash
# Download default metrics file
curl -o dcgm-metrics.csv \
  https://raw.githubusercontent.com/NVIDIA/dcgm-exporter/main/etc/dcp-metrics-included.csv

# Edit to add/remove metrics, then create ConfigMap
kubectl create configmap dcgm-metrics -n gpu-operator \
  --from-file=dcgm-metrics.csv

# Patch ClusterPolicy
kubectl patch clusterpolicies.nvidia.com/cluster-policy \
  --type merge \
  -p '{"spec": {"dcgmExporter": {"config": {"name": "dcgm-metrics"}}}}'
```

### Grafana dashboards
NVIDIA provides pre-built Grafana dashboards:
- **NVIDIA DCGM Exporter Dashboard** (ID: 12239) — import directly in Grafana
- Shows per-GPU utilization, temperature, power, memory, ECC errors
- For MIG: shows per-instance metrics

### Critical alerts to configure

```yaml
# Example PrometheusRule
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: gpu-alerts
  namespace: gpu-operator
spec:
  groups:
  - name: gpu.rules
    rules:
    - alert: GPUTemperatureHigh
      expr: DCGM_FI_DEV_GPU_TEMP > 83
      for: 5m
      labels:
        severity: warning
    - alert: GPUTemperatureCritical
      expr: DCGM_FI_DEV_GPU_TEMP > 90
      for: 1m
      labels:
        severity: critical
    - alert: GPUDoublebitECC
      expr: DCGM_FI_DEV_ECC_DBE_VOL_TOTAL > 0
      labels:
        severity: critical
        action: "Replace GPU — double-bit ECC = hardware failure"
    - alert: GPUXidError
      expr: DCGM_FI_DEV_XID_ERRORS > 0
      labels:
        severity: warning
    - alert: GPUMemoryFull
      expr: DCGM_FI_DEV_FB_FREE < 512
      for: 5m
      labels:
        severity: warning
```

### Limitation
DCGM Exporter cannot associate metrics to individual containers when GPU time-slicing is active. MIG metrics work fine.

---

## 11. Air-Gapped Deployment (Defense/Secure Sites)

For military, defense, or ITAR-restricted environments with no internet access.

### Container images to mirror

Pull these from NGC, push to your private registry:

| Component | Image |
|-----------|-------|
| GPU Operator | `nvcr.io/nvidia/gpu-operator:v26.3.0` |
| GPU Driver | `nvcr.io/nvidia/driver:580.126.20-ubuntu22.04` |
| Container Toolkit | `nvcr.io/nvidia/k8s/container-toolkit:v1.19.0-ubuntu20.04` |
| Device Plugin | `nvcr.io/nvidia/k8s-device-plugin:v0.19.0` |
| DCGM Exporter | `nvcr.io/nvidia/k8s/dcgm-exporter:v4.5.1-4.8.0` |
| GPU Feature Discovery | `nvcr.io/nvidia/gpu-feature-discovery:v0.19.0` |
| Node Feature Discovery | `registry.k8s.io/nfd/node-feature-discovery:v0.17.1` |
| MIG Manager | `nvcr.io/nvidia/cloud-native/k8s-mig-manager:v0.10.0` |
| Validator | `nvcr.io/nvidia/cloud-native/gpu-operator-validator:v26.3.0` |

### Mirror workflow
```bash
# For each image:
docker pull nvcr.io/nvidia/gpu-operator:v26.3.0
docker tag nvcr.io/nvidia/gpu-operator:v26.3.0 registry.airgap.local/nvidia/gpu-operator:v26.3.0
docker push registry.airgap.local/nvidia/gpu-operator:v26.3.0
```

### OS package repository (for driver compilation)
The driver container compiles kernel modules at startup. It needs OS packages.

**Ubuntu**: Mirror `linux-headers`, `linux-image`, `linux-modules` (matching kernel version) using `apt-mirror`.

**RHEL**: Mirror `kernel-headers`, `kernel-devel`, `kernel-core`, `gcc` using `reposync`.

Create ConfigMap:
```bash
kubectl create configmap repo-config -n gpu-operator \
  --from-file=/path/to/local-repo.list
```

### Shortcut: precompiled drivers
Using precompiled driver containers eliminates the need for OS package repos entirely. Set `driver.usePrecompiled=true` and specify branch:
```bash
--set driver.usePrecompiled=true --set driver.version="580"
```

### Helm chart download
```bash
# On internet-connected machine:
helm fetch https://helm.ngc.nvidia.com/nvidia/charts/gpu-operator-v26.3.0.tgz

# Transfer .tgz to air-gapped network
```

### Air-gapped values.yaml
```yaml
operator:
  repository: registry.airgap.local/nvidia
  image: gpu-operator
  version: v26.3.0

driver:
  repository: registry.airgap.local/nvidia
  image: driver
  version: "580.126.20"
  imagePullPolicy: IfNotPresent
  repoConfig:
    configMapName: repo-config

toolkit:
  repository: registry.airgap.local/nvidia/k8s
  image: container-toolkit
  version: v1.19.0-ubuntu20.04

devicePlugin:
  repository: registry.airgap.local/nvidia
  image: k8s-device-plugin
  version: v0.19.0

dcgmExporter:
  repository: registry.airgap.local/nvidia/k8s
  image: dcgm-exporter
  version: v4.5.1-4.8.0

gfd:
  repository: registry.airgap.local/nvidia
  image: gpu-feature-discovery
  version: v0.19.0

nfd:
  repository: registry.airgap.local/nfd
  image: node-feature-discovery
  version: v0.17.1

migManager:
  repository: registry.airgap.local/nvidia/cloud-native
  image: k8s-mig-manager
  version: v0.10.0
```

### Install
```bash
helm install gpu-operator \
  -n gpu-operator --create-namespace \
  ./gpu-operator-v26.3.0.tgz \
  -f values.yaml \
  --wait
```

### Image pull secrets (if private registry requires auth)
```bash
kubectl create secret docker-registry ngc-secret \
  -n gpu-operator \
  --docker-server=registry.airgap.local \
  --docker-username=<user> \
  --docker-password=<pass>

# Add to Helm install:
--set operator.imagePullSecrets[0]=ngc-secret
```

---

## 12. Driver Upgrades — Rolling Updates

Driver upgrades require unloading and reloading kernel modules, which means brief GPU downtime per node. The GPU Operator has a built-in upgrade controller that handles this safely.

### Trigger a driver upgrade
```bash
kubectl patch clusterpolicies.nvidia.com/cluster-policy \
  --type='json' \
  -p='[{"op": "replace", "path": "/spec/driver/version", "value":"580.95.05"}]'
```

### Upgrade state machine per node

```
upgrade-required → cordon-required → wait-for-jobs-required →
pod-deletion-required → drain-required → pod-restart-required →
validation-required → uncordon-required → upgrade-done
```

If anything fails: `upgrade-failed`

### Monitor progress
```bash
kubectl get node -l nvidia.com/gpu.present \
  -ojsonpath='{range .items[*]}{.metadata.name}{"\t"}{.metadata.labels.nvidia\.com/gpu-driver-upgrade-state}{"\n"}{end}'

# Watch events
kubectl get events -n default --sort-by='.lastTimestamp' | grep GPUDriverUpgrade
```

### Upgrade policy configuration
```yaml
driver:
  upgradePolicy:
    autoUpgrade: true
    maxParallelUpgrades: 1       # upgrade 1 node at a time (safe for production)
    maxUnavailable: "25%"        # never take down >25% of GPU fleet
    waitForCompletion:
      timeoutSeconds: 0          # 0 = wait forever
    gpuPodDeletion:
      force: false               # don't force-kill unmanaged pods
      timeoutSeconds: 300        # 5 min grace period
      deleteEmptyDir: false
    drain:
      enable: false              # only enable if pod deletion isn't enough
      force: false
      timeoutSeconds: 300
      deleteEmptyDir: false
```

### Prometheus metrics for upgrades
```
gpu_operator_auto_upgrade_enabled         — 1 if controller active
gpu_operator_nodes_upgrades_in_progress   — nodes currently upgrading
gpu_operator_nodes_upgrades_done          — successful completions
gpu_operator_nodes_upgrades_failed        — failed nodes
gpu_operator_nodes_upgrades_available     — ready to upgrade
gpu_operator_nodes_upgrades_pending       — waiting in queue
```

### Operational controls

**Pause all upgrades:**
```bash
kubectl patch clusterpolicies.nvidia.com/cluster-policy \
  --type='json' \
  -p='[{"op": "replace", "path": "/spec/driver/upgradePolicy/autoUpgrade", "value":false}]'
```

**Skip a specific node:**
```bash
kubectl label node <node-name> nvidia.com/gpu-driver-upgrade.skip=true
```

**Retry failed upgrade:**
```bash
kubectl label node <node-name> nvidia.com/gpu-driver-upgrade-state=upgrade-required --overwrite
```

### ADC production settings
- `maxParallelUpgrades: 1` for Trappeys/MARLIE 1 (small fleet)
- `maxParallelUpgrades: 4` for Willow Glen (large fleet, keep 75%+ capacity)
- Always `drain.enable: false` first — only enable if GPU pod eviction alone fails
- Schedule driver upgrades during maintenance windows
- Test new driver version on MARLIE 1 edge node first, then Trappeys, then Willow Glen

---

## 13. Operator Upgrades

Upgrading the GPU Operator itself (not just drivers).

### Method 1: Automatic CRD upgrade (recommended, v24.9.0+)
```bash
export RELEASE_TAG=v26.3.0
helm repo update nvidia
helm show values nvidia/gpu-operator --version=$RELEASE_TAG > values-$RELEASE_TAG.yaml
# Edit values file as needed

helm upgrade gpu-operator nvidia/gpu-operator \
  -n gpu-operator \
  --disable-openapi-validation \
  -f values-$RELEASE_TAG.yaml \
  --version $RELEASE_TAG
```

The `--disable-openapi-validation` flag is required to handle CRD transitions.

### Method 2: Manual CRD upgrade
```bash
export RELEASE_TAG=v26.3.0

# Update CRDs first
kubectl apply -f https://raw.githubusercontent.com/NVIDIA/gpu-operator/refs/tags/$RELEASE_TAG/deployments/gpu-operator/crds/nvidia.com_clusterpolicies.yaml
kubectl apply -f https://raw.githubusercontent.com/NVIDIA/gpu-operator/refs/tags/$RELEASE_TAG/deployments/gpu-operator/crds/nvidia.com_nvidiadrivers.yaml
kubectl apply -f https://raw.githubusercontent.com/NVIDIA/gpu-operator/refs/tags/$RELEASE_TAG/deployments/gpu-operator/charts/node-feature-discovery/crds/nfd-api-crds.yaml

# Then upgrade
helm repo update nvidia
helm show values nvidia/gpu-operator --version=$RELEASE_TAG > values-$RELEASE_TAG.yaml
helm upgrade gpu-operator nvidia/gpu-operator \
  -n gpu-operator \
  -f values-$RELEASE_TAG.yaml \
  --version $RELEASE_TAG
```

### Edit ClusterPolicy directly
For minor config changes (not version upgrades):
```bash
kubectl edit clusterpolicy
# Changes apply automatically after save
```

### Version support lifecycle
- **Current**: 26.3.x (supported, actively maintained)
- **Deprecated**: 25.10.x (security fixes only)
- **EOL**: 25.3.x and older (no support)

Versioning follows YY.MM.PP calendar format.

---

## 14. Base Command Manager Integration

NVIDIA Base Command Manager (BCM) is the fleet management layer that sits above the GPU Operator. It handles cluster provisioning, workload scheduling, and infrastructure monitoring across DGX/HGX systems.

### How they work together
- **BCM** provisions the physical cluster: OS, networking, storage, Kubernetes bootstrap
- **GPU Operator** manages the GPU software stack within Kubernetes
- BCM calls Helm to install/upgrade the GPU Operator
- BCM's monitoring layer consumes DCGM Exporter metrics
- BCM handles job scheduling (Slurm or Kubernetes) while GPU Operator handles device allocation

### BCM capabilities relevant to ADC
- Cluster administration and provisioning
- Cloudbursting (hybrid cloud overflow)
- Container orchestration integration
- Edge deployment management
- User environment and job submission
- Developer APIs for custom automation

### ADC deployment path
1. Willow Glen gets BCM as the primary management plane (comes with DGX-Ready/NCP certification)
2. BCM manages GPU Operator lifecycle across all Willow Glen nodes
3. MARLIE 1 connects as a satellite cluster (BCM can manage remote sites)
4. ADC 3K pods at customer sites managed via BCM's edge features
5. Trappeys may use standalone GPU Operator (smaller scale, no BCM needed initially)

---

## 15. NVL72 Rack Considerations

The GB200 NVL72 is a full-rack system with 36 Grace CPUs and 72 Blackwell GPUs connected via NVLink. The GPU Operator works on NVL72 but there are specific considerations.

### NVL72 architecture facts
- 72 GPUs act as a single NVLink domain (900 GB/s bisection bandwidth)
- Grace CPUs are ARM-based (aarch64) — GPU Operator supports ARM
- Liquid-cooled, 120 kW per rack
- Ships as a complete unit with DGX OS pre-installed

### GPU Operator on NVL72
- **Use pre-installed driver mode**: `driver.enabled=false` (DGX OS has drivers)
- **Open kernel modules**: Required for Blackwell GPUs (default with DGX OS)
- **NVSwitch/Fabric Manager**: Required and pre-installed. If you see `Fabric State: In Progress` in `nvidia-smi -q`, fabricmanager needs to be running
- **GPUDirect RDMA**: Mandatory for NVLink fabric. Use DMA-BUF path
- **MIG on NVL72**: Supported but uncommon — NVL72 is designed for large-scale training where all 72 GPUs work as one unit. MIG would partition individual GPUs within the NVLink domain. Use case: if running mixed inference+training, partition some GPUs for inference via MIG while keeping others for training
- **DCGM monitors all 72 GPUs**: Each GPU reports individually. NVLink bandwidth metrics show inter-GPU fabric health

### NVL72 Helm install
```bash
helm install gpu-operator \
  -n gpu-operator --create-namespace \
  nvidia/gpu-operator --version=v26.3.0 \
  --set driver.enabled=false \
  --set driver.rdma.useHostMofed=true \
  --set gds.enabled=true
```

### Monitoring NVL72 fabric health
Key metrics to watch:
- `DCGM_FI_DEV_NVLINK_BANDWIDTH_TOTAL` — NVLink bandwidth per GPU
- `DCGM_FI_DEV_GPU_TEMP` — critical at 72-GPU density
- `DCGM_FI_DEV_POWER_USAGE` — per-GPU power draw
- NVSwitch error counts via DCGM

---

## 16. Troubleshooting

### First step: must-gather
```bash
curl -o must-gather.sh -L \
  https://raw.githubusercontent.com/NVIDIA/gpu-operator/main/hack/must-gather.sh
chmod +x must-gather.sh
./must-gather.sh
# Produces archive with all manifests and logs
```

### Common issues

**Pods stuck in Init state:**
```bash
kubectl logs -n gpu-operator nvidia-driver-daemonset-<pod> -c nvidia-driver-ctr
kubectl exec -n gpu-operator <pod> -c nvidia-driver-ctr -- dmesg
sudo dmesg | grep -i NVRM
sudo dmesg | grep -i Xid
```
Usually: driver compilation failed (missing packages), or kernel module load failure.

**CrashLoopBackOff on GPU Feature Discovery:**
Indicates driver or hardware issue. Check for Xid errors:
```
XidCriticalError: Xid=48 on Device=GPU-[id]; marking device as unhealthy
```
Reference: https://docs.nvidia.com/deploy/xid-errors

**"No runtime for nvidia is configured":**
Container toolkit pod failed to start. Check:
```bash
kubectl logs -n gpu-operator nvidia-container-toolkit-daemonset-<id> -c nvidia-container-toolkit-ctr
```

**Fewer GPUs than expected:**
Device plugin marks unhealthy GPUs as unallocatable. Check for Xid errors. If GPU has infoROM corruption (`nvidia-smi` return code 14), GPU needs physical replacement.

**NVSwitch systems missing GPUs:**
Fabric Manager must be running. Check:
```bash
nvidia-smi -q | grep "Fabric State"
# "In Progress" = fabricmanager not installed/running
cat /var/log/fabricmanager.log
```

**Large clusters (300+ nodes) — Operator OOM:**
```bash
kubectl patch deployment gpu-operator -n gpu-operator --type='json' \
  -p='[{"op":"replace", "path":"/spec/template/spec/containers/0/resources/limits/memory", "value":"1400Mi"}]'
```

**Known driver bugs (avoid these versions):**
- 570.124.06, 570.133.20, 570.148.08, 570.158.01 — pods stuck in Pending with mixed MIG + full GPU. Downgrade to 570.86.15 or upgrade past 580.x.

**Nouveau module conflict:**
```bash
# /etc/modprobe.d/blacklist-nouveau.conf
blacklist nouveau
options nouveau modeset=0
sudo update-initramfs -u
sudo reboot
```

**Secure Boot:**
Not supported. Disable in BIOS.

---

## 17. ADC Site-Specific Deployment Matrix

| Setting | Willow Glen | Trappeys | MARLIE 1 | ADC Pure DC AI Cassette |
|---------|------------|----------|----------|------------|
| **Scale** | SuperPOD (NVL72 racks) | 36-84 NVL72 racks | Edge NVL72 | 1-4 racks |
| **Driver mode** | Pre-installed (DGX OS) | Pre-installed | Pre-installed | Containerized |
| **Kernel module** | Open (Blackwell) | Open | Open | Open |
| **MIG strategy** | Mixed (train + infer) | Single (inference) | Disabled | Per customer |
| **Time-slicing** | No (dedicated training) | Yes (university lab) | No | Per customer |
| **GPUDirect RDMA** | DMA-BUF + Network Op | DMA-BUF | DMA-BUF | DMA-BUF |
| **GPUDirect Storage** | Enabled | Enabled | Enabled | Optional |
| **DCGM Exporter** | Enabled + full alerts | Enabled | Enabled | Enabled |
| **BCM managed** | Yes (primary) | No (standalone K8s) | Satellite | Remote |
| **Air-gapped** | No | No | No | Customer-dependent |
| **Upgrade policy** | maxParallel=4, drain=false | maxParallel=1 | maxParallel=1 | Customer SLA |
| **NVLink fabric** | 72-GPU domain per rack | 72-GPU domain | Single rack | Single rack |

### Deployment order
1. **MARLIE 1** — smallest, Scott's war room. Install GPU Operator, validate monitoring, test MIG/time-slicing, run CUDA benchmarks. This is the staging ground.
2. **Trappeys** — proof of concept. Full GPU Operator + DCGM + Grafana. University partner access via MIG. First Solar power validation.
3. **Willow Glen** — production SuperPOD. BCM manages GPU Operator. Full RDMA/GDS stack. Rolling upgrades tested on MARLIE 1 first.
4. **ADC Pure DC AI Cassettes** — templated Helm values per customer. Air-gapped config for defense customers.

### Helm values template per site

Save as `values-<site>.yaml` and version control:

```yaml
# values-marlie.yaml
driver:
  enabled: false              # DGX OS pre-installed
  rdma:
    useHostMofed: true
  upgradePolicy:
    autoUpgrade: true
    maxParallelUpgrades: 1

gds:
  enabled: true

mig:
  strategy: mixed

dcgmExporter:
  enabled: true

toolkit:
  enabled: true

nfd:
  enabled: true
```

```bash
# Deploy to MARLIE 1
helm install gpu-operator \
  -n gpu-operator --create-namespace \
  nvidia/gpu-operator --version=v26.3.0 \
  -f values-marlie.yaml \
  --wait
```

---

## Quick Reference — Essential Commands

```bash
# Install
helm install gpu-operator -n gpu-operator --create-namespace nvidia/gpu-operator --version=v26.3.0 --wait

# Check status
kubectl get pods -n gpu-operator
kubectl get clusterpolicy

# GPU inventory
kubectl get nodes -l nvidia.com/gpu.present -o custom-columns=NAME:.metadata.name,GPU:.metadata.labels.nvidia\\.com/gpu\\.product,COUNT:.metadata.labels.nvidia\\.com/gpu\\.count

# Test GPU
kubectl run gpu-test --image=nvcr.io/nvidia/k8s/cuda-sample:vectoradd-cuda11.7.1-ubuntu20.04 --restart=Never --limits=nvidia.com/gpu=1 && kubectl logs gpu-test -f

# MIG config
kubectl label nodes <node> nvidia.com/mig.config=all-1g.10gb --overwrite

# Driver upgrade
kubectl patch clusterpolicies.nvidia.com/cluster-policy --type='json' -p='[{"op":"replace","path":"/spec/driver/version","value":"580.95.05"}]'

# Operator upgrade
helm upgrade gpu-operator nvidia/gpu-operator -n gpu-operator --disable-openapi-validation --version=v26.3.0

# Diagnostics
curl -o must-gather.sh -L https://raw.githubusercontent.com/NVIDIA/gpu-operator/main/hack/must-gather.sh && chmod +x must-gather.sh && ./must-gather.sh
```

---

## Sources

- NVIDIA GPU Operator Documentation v26.3.0: https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/
- NVIDIA Developer Blog — GPU Operator: https://developer.nvidia.com/blog/nvidia-gpu-operator-simplifying-gpu-management-in-kubernetes/
- NVIDIA Base Command Manager: https://docs.nvidia.com/base-command-manager/
- NVIDIA DCGM: https://docs.nvidia.com/datacenter/dcgm/latest/
- Xid Error Reference: https://docs.nvidia.com/deploy/xid-errors
