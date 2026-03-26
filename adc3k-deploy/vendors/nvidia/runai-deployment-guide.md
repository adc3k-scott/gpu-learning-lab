# NVIDIA Run:AI — ADC Deployment Guide
Last updated: 2026-03-25
Source: Run:AI v2.24 documentation

## What Run:AI Does for ADC
- GPU scheduling and workload management across clusters
- Multi-tenant access control (RBAC across multiple clusters)
- Fair-share resource allocation between customers
- Training, inference, and workspace workload types
- Autoscaling (latency, throughput, concurrency metrics)
- Distributed training (PyTorch, TensorFlow, MPI, JAX)
- Distributed inference (multi-node via Leader Worker Set)
- Network topology-aware scheduling (keeps pods close)
- SSO authentication (SAML, OIDC, OpenShift)
- Self-hosted or SaaS deployment options

## Hardware Requirements

### System Nodes (Run:AI services)
- CPU: 10 cores minimum
- Memory: 20GB minimum
- Disk: 50GB minimum
- Recommend: 3+ system nodes for high availability

### Worker Nodes (GPU workloads)
- CPU: 2 cores minimum per node
- Memory: 4GB minimum per node
- Supports: x86 and ARM (Grace) CPUs
- Supports: any NVIDIA GPU via GPU Operator
- Supports: GB200 NVL72 multi-node NVLink
- Does NOT support: vGPU, DGX Spark, Jetson

## Software Requirements
- Kubernetes: 1.33-1.35 (v2.24)
- GPU Operator: 25.3-25.10
- Network Operator: v24.4+ (required for RDMA/NVLink)
- Container runtime: containerd or CRI-O
- Prometheus required (for metrics)
- Knative Serving required (for inference, v1.11-1.18)

## Installation — Two Methods

### Method 1: Helm (recommended for ADC)
```bash
kubectl create ns runai
kubectl label --overwrite ns runai pod-security.kubernetes.io/enforce=privileged
helm install runai <chart> -n runai --values values.yaml
```

### Method 2: Base Command Manager (BCM)
- BCM wizard provisions K8s cluster + installs Run:AI automatically
- Recommended for new deployments from bare metal

## Node Roles for ADC
```bash
# System nodes (Run:AI services — CPU only)
kubectl label nodes <node> node-role.kubernetes.io/runai-system=true

# GPU worker nodes (compute workloads)
kubectl label nodes <node> node-role.kubernetes.io/runai-gpu-worker=true

# CPU worker nodes (non-GPU workloads)
kubectl label nodes <node> node-role.kubernetes.io/runai-cpu-worker=true
```

## Authentication for ADC
- SSO via SAML or OIDC (connect to ADC customer auth)
- Username/password for admin breakglass account
- Service accounts with secret keys for API automation
- RBAC: roles assigned per project, department, cluster, or account-wide

## RBAC Structure
```
<Subject> is a <Role> in a <Scope>

Subject: user, group, or service account
Role: predefined permission set (view, edit, create, delete)
Scope: project, department, cluster, or all clusters
```

## ADC Customer Mapping
| ADC Customer Tier | Run:AI Project | GPU Allocation | Scheduling |
|-------------------|---------------|----------------|------------|
| Enterprise ($45/M) | Dedicated project | Guaranteed quota | Priority |
| Premium ($6/M) | Shared project | Guaranteed minimum | Fair-share |
| Standard ($1/M) | Shared project | Burst capacity | Best-effort |
| Batch ($0.20/M) | Low-priority project | Preemptible | Fill gaps |

## Inference Setup (for token serving)
Requires Knative Serving + Kourier ingress:
- Wildcard DNS: *.runai-inference.adc3k.com
- TLS certificate for HTTPS
- Autoscaling on latency, throughput, or concurrency
- Scale-to-zero supported (saves power when idle)

## Distributed Training Frameworks
- PyTorch, TensorFlow, XGBoost, JAX via Kubeflow Training Operator
- MPI v2 via MPI Operator
- Distributed inference via Leader Worker Set (LWS v0.7.0+)

## Integrations (works out of box)
- NIM Operator — model serving
- Dynamo Operator — inference orchestration
- GPU Operator — GPU lifecycle
- Network Operator — InfiniBand/RDMA
- DCGM — GPU monitoring
- Prometheus/Grafana — metrics and dashboards

## ADC Deployment Order (complete)
1. Install Kubernetes (BCM wizard or manual)
2. Install GPU Operator (Helm)
3. Install Network Operator (Helm)
4. Install Prometheus (Helm)
5. Install Run:AI (Helm or BCM)
6. Install Knative Serving (for inference)
7. Install NIM Operator (for model serving)
8. Deploy Dynamo (inference orchestration)
9. Configure customer projects and quotas in Run:AI
10. Expose API endpoints with TLS
11. Start serving tokens
