# NVIDIA Cloud-Native Stack — ADC Operations Layer
Last updated: 2026-03-25
Source: developer.nvidia.com/cloud-native-technologies

## What This Is
The SOFTWARE layer that manages GPU compute on Kubernetes. This is how ADC operates the hardware after it's powered on. Sits between the physical racks and the token sales.

## The Stack (bottom to top)

### 1. NVIDIA Container Toolkit
- Builds and runs GPU-accelerated containers
- Automatically configures containers to use NVIDIA GPUs
- Foundation layer — everything else sits on top of this

### 2. NVIDIA GPU Operator
- Automates lifecycle management of GPU software on Kubernetes
- Handles drivers, device plugins, monitoring, MIG configuration
- Certified for: Red Hat OpenShift, VMware vSphere with Tanzu
- ADC deploys this on every cluster — it's how GPUs become available to workloads

### 3. NVIDIA Network Operator
- Automates deployment of accelerated networking on K8s
- Enables GPUDirect RDMA (GPU-to-GPU across network without CPU)
- Critical for InfiniBand fabric performance
- Paired with GPU Operator for full stack

### 4. NVIDIA NIM Operator
- Deploys NVIDIA NIM inference microservices on Kubernetes
- Automates lifecycle of generative AI applications
- This is the MLOps/LLMOps layer — manages model serving
- ADC's token factory runs NIM microservices

### 5. NVIDIA Cloud-Native Stack (Reference Architecture)
- Combines GPU Operator + Network Operator + upstream Kubernetes
- Supports: MIG (Multi-Instance GPU), GPUDirect RDMA, GPUDirect Storage, GPU monitoring
- Runs on: x86, Arm, servers, workstations, cloud, embedded
- Available on GitHub as open source

### 6. NVIDIA Base Command Manager (on top of all this)
- Cluster management layer
- Free tier: 8 accelerators per system, any cluster size
- Enterprise: per-GPU licensing
- This is ADC's control plane

## How This Maps to ADC

```
TOKEN SALES (customer-facing API)
    |
NVIDIA Dynamo (inference orchestration)
    |
NVIDIA NIM Operator (model serving on K8s)
    |
NVIDIA GPU Operator + Network Operator (GPU + InfiniBand lifecycle)
    |
NVIDIA Container Toolkit (GPU container runtime)
    |
Kubernetes (cluster orchestration)
    |
NVIDIA Base Command Manager (cluster management)
    |
NVIDIA DCGM (GPU monitoring, 30+ metrics, Prometheus)
    |
PHYSICAL HARDWARE (NVL72 racks, Delta power, Eaton distribution)
```

## What ADC Needs to Deploy
1. Kubernetes cluster on every compute site (MARLIE 1, Trappeys)
2. GPU Operator + Network Operator installed (automated)
3. NIM Operator for inference microservice management
4. Base Command Manager for cluster-level control
5. DCGM for monitoring (feeds into Mission Control dashboard)
6. Dynamo for inference optimization (7x throughput boost)

## Key Insight
All of this software is either open source or included with NVIDIA AI Enterprise licensing. The hardware is the capital expense. The operations software is essentially free or subscription-based. ADC doesn't need to build any of this — just deploy it on the racks.

## MGX Reference Architecture
- MGX = modular hardware standard for building AI factory racks
- Over 100 combinations of GPU, CPU, networking configurations
- Pre-integration of ~80% of components at factory (deploy in <90 days vs 12 months)
- 200+ ecosystem partners adopting MGX components
- ADC Pure DC AI Cassettes use MGX-compatible components (Staubli UQD = "MGX UQD", 800V busbars, liquid cooling manifolds)
- Partners: Supermicro, Lenovo, Gigabyte, ASUS, Cisco, MSI, Wistron, etc.

## MGX Key Specs
- R&D savings: $2-4M per platform through shared reference designs
- Power supply efficiency: 94%
- Cooling: liquid-cooled busbars/manifolds, <15C coolant delta under 1400A loads
- Deploy timeline: <90 days (vs 12 months traditional)
- Supports: Blackwell, Rubin, Grace, Vera, x86, Arm
- Multi-generational compatibility — today's investment works with future GPUs
