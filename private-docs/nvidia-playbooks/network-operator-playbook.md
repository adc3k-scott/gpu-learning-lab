# NVIDIA Network Operator — ADC Deployment Playbook
Last updated: 2026-03-25
Source: NVIDIA Network Operator v26.1.0 docs

## What It Does
Automates provisioning and management of NVIDIA networking (InfiniBand, RDMA, SR-IOV) on Kubernetes. Works WITH GPU Operator to deliver high-throughput, low-latency networking for GPU clusters.

## Version: v26.1.0
- Supports: ConnectX-8, ConnectX-9 SuperNIC, Spectrum-X Ethernet
- Supports: DGX/HGX GB200 NVL72 (GA), DGX/HGX B200 (GA)
- Kubernetes: 1.31-1.35
- Government Ready (STIG/FIPS hardening)
- Air-gapped deployment supported
- Apache 2.0 open source

## ADC Quick Install
```bash
helm repo add nvidia https://helm.ngc.nvidia.com/nvidia
helm repo update
helm install network-operator nvidia/network-operator \
    -n nvidia-network-operator \
    --create-namespace \
    --version v26.1.0 \
    --set sriovNetworkOperator.enabled=true \
    --wait
```

## What Gets Deployed
- DOCA-OFED networking drivers (containerized, auto-managed)
- RDMA Shared Device Plugin (InfiniBand + RoCE)
- SR-IOV Network Operator (VF partitioning for multi-tenant)
- Multus CNI (multiple network interfaces per pod)
- NVIDIA IPAM Plugin (IP address management)
- NIC Feature Discovery (auto-detect NIC capabilities)
- DOCA Telemetry Service (network metrics)
- IPoIB CNI (IP over InfiniBand)

## Supported Hardware for ADC
| Adapter | Speed | Protocol | Status |
|---------|-------|----------|--------|
| ConnectX-7 | 400 Gb/s | IB + Ethernet | GA |
| ConnectX-8 SuperNIC | 800 Gb/s | IB + Ethernet | GA |
| ConnectX-9 SuperNIC | 800 Gb/s | IB + Ethernet | GA (v26.1.0) |
| BlueField-3 DPU | 200 Gb/s | NIC mode, RoCE | GA |
| BlueField-3 SuperNIC | 400 Gb/s | NIC mode, RoCE | GA |

## ADC Networking Scenarios

### 1. InfiniBand RDMA (Primary — for NVL72 compute fabric)
- NVLink handles intra-rack GPU-to-GPU (260 TB/s)
- InfiniBand handles inter-rack GPU-to-GPU (scale-out)
- GPUDirect RDMA bypasses CPU entirely
- This is the compute fabric for training and large inference

### 2. SR-IOV (For multi-tenant isolation)
- Partition NICs into Virtual Functions
- Each customer gets dedicated network bandwidth
- Hardware-level isolation between tenants
- Required for enterprise/government customers

### 3. Spectrum-X Ethernet (For east-west AI traffic)
- 800G per port co-packaged optics
- Scale-out fabric for token serving
- Lower cost than InfiniBand for inference-heavy workloads

### 4. Air-Gapped (For military/defense)
- Full offline deployment supported
- Mirror all container images to local registry
- No internet required after initial setup
- Government Ready (FedRAMP High equivalent)

## GPUDirect RDMA Setup
Enables GPU memory to transfer directly over network without CPU involvement.
Critical for distributed training across multiple NVL72 racks.

```yaml
# In NicClusterPolicy
spec:
  ofedDriver:
    image: doca-driver
    repository: nvcr.io/nvidia/mellanox
    version: doca3.3.0-26.01-1.0.0.0-0
  rdmaSharedDevicePlugin:
    image: k8s-rdma-shared-dev-plugin
    repository: nvcr.io/nvidia/mellanox
    version: network-operator-v26.1.0
```

## Integration with GPU Operator
- Install GPU Operator FIRST, then Network Operator
- Share Node Feature Discovery (NFD) — only install once
- Together they enable GPUDirect RDMA automatically
- DCGM monitors GPU metrics, DOCA Telemetry monitors network metrics

## ADC Deployment Order
1. Install GPU Operator (manages GPUs + drivers)
2. Install Network Operator (manages InfiniBand + RDMA)
3. Install NIM Operator (manages model serving)
4. Deploy Dynamo (inference orchestration)
5. Expose API endpoint
6. Start serving tokens

Three Helm installs. Full AI factory on Kubernetes.
