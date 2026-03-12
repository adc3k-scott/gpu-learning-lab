# NVIDIA-Certified Associate: AI Infrastructure & Operations
## Practice Exam — 60 Questions with Answers

**Real exam: 50 questions, 60 minutes, online proctored, $125**
**Domains: Essential AI Knowledge (38%) | AI Infrastructure (40%) | AI Operations (22%)**

Answers are right below each question. Skim fast, flag what you don't know, circle back.

---

# DOMAIN 1: ESSENTIAL AI KNOWLEDGE (23 Questions)

---

### Q1. What is the primary difference between AI, machine learning, and deep learning?

**A)** AI is the broadest concept (machines mimicking human intelligence). Machine learning is a subset of AI where systems learn from data without explicit programming. Deep learning is a subset of ML using neural networks with many layers (deep neural networks) to learn complex patterns.

Think of it as nested circles: AI > ML > DL.

---

### Q2. What is the main architectural difference between a CPU and a GPU?

**A)** A CPU has a few powerful cores optimized for sequential processing (low latency, complex logic). A GPU has thousands of smaller cores optimized for parallel processing (high throughput, same operation on many data points simultaneously). GPUs excel at the matrix math that AI training and inference require.

---

### Q3. Why have GPUs become the standard for AI workloads instead of CPUs?

**A)** AI workloads (especially training deep neural networks) involve massive matrix multiplications and tensor operations that are highly parallelizable. GPUs can execute thousands of these operations simultaneously, delivering 10-100x speedup over CPUs for these specific workloads. Tensor Cores in NVIDIA GPUs add further acceleration for mixed-precision math.

---

### Q4. What is the difference between AI training and AI inference?

**A)**
- **Training**: Building the model. Feed massive datasets through a neural network, adjust weights over millions of iterations until the model learns. Requires enormous compute (days/weeks on GPU clusters). Write-heavy, high memory, high bandwidth.
- **Inference**: Using the trained model. Feed new data in, get predictions out. Requires less compute but demands low latency and high throughput. Read-heavy. This is the production deployment phase.

---

### Q5. Which requires more GPU compute — training or inference?

**A)** **Training** requires far more compute. A single training run can take days or weeks on hundreds/thousands of GPUs. Inference uses less total compute per request but must handle many concurrent requests with strict latency requirements. However, at scale, inference can consume MORE total GPU-hours because it runs 24/7 serving millions of requests.

---

### Q6. What is NVIDIA TensorRT and what is it used for?

**A)** TensorRT is NVIDIA's inference optimization engine. It takes a trained model and optimizes it for deployment — layer fusion, precision calibration (FP32 → FP16/INT8), kernel auto-tuning, and memory optimization. The result is faster inference with lower latency and higher throughput on NVIDIA GPUs. It's the bridge between training and production deployment.

---

### Q7. What are the key factors driving the recent rapid adoption of AI?

**A)** Four main factors:
1. **Compute power** — GPU acceleration making training feasible
2. **Data availability** — massive datasets from internet, IoT, enterprise systems
3. **Algorithm advances** — transformers, attention mechanisms, foundation models
4. **Software ecosystem** — frameworks (PyTorch, TensorFlow), pre-trained models, cloud APIs lowering the barrier to entry

---

### Q8. Name 5 major industries/use cases where AI is being deployed today.

**A)**
1. **Healthcare** — medical imaging, drug discovery, diagnostics
2. **Autonomous vehicles** — self-driving, ADAS, sensor fusion
3. **Financial services** — fraud detection, algorithmic trading, risk assessment
4. **Manufacturing** — quality inspection, predictive maintenance, digital twins
5. **Natural language** — chatbots, translation, content generation (LLMs)

Also: retail, energy, telecom, agriculture, defense, cybersecurity.

---

### Q9. What is the NVIDIA software stack for AI? List the key layers.

**A)** Bottom to top:
1. **GPU Hardware** — A100, H100, H200, Blackwell GPUs
2. **CUDA** — parallel computing platform and programming model
3. **cuDNN** — GPU-accelerated library for deep neural networks
4. **NVIDIA AI Enterprise** — end-to-end software platform (TensorRT, Triton, NIM, RAPIDS, etc.)
5. **Frameworks** — PyTorch, TensorFlow (built on CUDA/cuDNN)
6. **Applications** — NGC containers, pre-trained models, NIM microservices

CUDA is the foundation that everything else builds on.

---

### Q10. What is NVIDIA NGC?

**A)** NGC (NVIDIA GPU Cloud) is a catalog/registry of GPU-optimized containers, pre-trained models, and SDKs. It provides ready-to-use Docker containers for AI frameworks (PyTorch, TensorFlow), inference servers (Triton), and applications — all tested and optimized for NVIDIA GPUs. Think of it as an app store for GPU-accelerated AI software.

---

### Q11. What is the purpose of NVIDIA NIM (NVIDIA Inference Microservices)?

**A)** NIM packages optimized AI models as containerized microservices with a standard API. Instead of manually optimizing and deploying models, you pull a NIM container and get an inference endpoint that's already optimized with TensorRT, runs on NVIDIA GPUs, and exposes a simple REST API. It dramatically simplifies putting AI models into production.

---

### Q12. What is NVIDIA Triton Inference Server?

**A)** Triton is an open-source inference serving platform. It can serve multiple models simultaneously from multiple frameworks (PyTorch, TensorFlow, TensorRT, ONNX) on GPU or CPU. It handles model management, request batching, scheduling, and health monitoring. It's the production inference backend — accepts requests, routes to models, returns results.

---

### Q13. What is a Large Language Model (LLM) and why does it need GPU compute?

**A)** An LLM is a deep learning model trained on massive text data to understand and generate human language (GPT, Llama, Claude, etc.). LLMs have billions of parameters — GPT-4 class models have hundreds of billions. Training requires thousands of GPUs for weeks. Even inference requires multiple high-memory GPUs because the model weights must fit in GPU memory. The matrix multiplications at this scale are only feasible on GPUs.

---

### Q14. What is the difference between supervised, unsupervised, and reinforcement learning?

**A)**
- **Supervised**: Train on labeled data (input → known output). Model learns the mapping. Examples: image classification, spam detection.
- **Unsupervised**: Train on unlabeled data. Model finds patterns/clusters. Examples: anomaly detection, customer segmentation.
- **Reinforcement**: Agent learns by interacting with environment, receiving rewards/penalties. Examples: game AI, robotics, autonomous driving.

---

### Q15. What is transfer learning and why is it important?

**A)** Transfer learning takes a model pre-trained on a large general dataset and fine-tunes it on a smaller, domain-specific dataset. Important because: (1) drastically reduces training time and cost, (2) requires much less training data, (3) achieves good results even with small datasets. Foundation models (like GPT) enable transfer learning at massive scale.

---

### Q16. What does NVIDIA RAPIDS do?

**A)** RAPIDS is a suite of GPU-accelerated libraries for data science and analytics. It provides GPU-accelerated versions of pandas (cuDF), scikit-learn (cuML), and graph analytics (cuGraph). It speeds up the data preparation and feature engineering stages of the ML pipeline — the work that happens BEFORE model training.

---

### Q17. What is mixed-precision training and why does it matter?

**A)** Mixed-precision uses both FP16 (half precision) and FP32 (full precision) during training. Tensor Cores on NVIDIA GPUs can perform FP16 matrix operations much faster than FP32. By doing forward/backward passes in FP16 and keeping master weights in FP32 for accuracy, you get ~2x training speedup with minimal accuracy loss. Blackwell GPUs add FP4/FP8 for even more speedup.

---

### Q18. What is the AI development lifecycle?

**A)** The typical stages:
1. **Data collection** — gather and curate training data
2. **Data preparation** — clean, label, augment, split (train/val/test)
3. **Model development** — select architecture, train, tune hyperparameters
4. **Model evaluation** — validate accuracy, test against benchmarks
5. **Deployment** — optimize (TensorRT), containerize, serve (Triton/NIM)
6. **Monitoring** — track model performance, detect drift, retrain as needed

This is iterative — monitoring feeds back into data collection.

---

### Q19. What is the role of containers (Docker) in AI workflows?

**A)** Containers package the entire AI software stack — OS libraries, CUDA drivers, frameworks, model code, dependencies — into a portable, reproducible unit. Benefits: (1) works the same everywhere (dev → test → production), (2) easy scaling, (3) version control, (4) no dependency conflicts. NGC provides pre-built containers optimized for NVIDIA GPUs.

---

### Q20. What is an epoch in model training?

**A)** One epoch is a complete pass through the entire training dataset. Training typically runs for many epochs (tens to hundreds). Each epoch consists of multiple batches. The batch size determines how many training samples are processed before updating model weights. More epochs = more learning, but too many = overfitting.

---

### Q21. What is NVIDIA DGX and what is it designed for?

**A)** DGX is NVIDIA's purpose-built AI supercomputer platform. The DGX H100 system packages 8× H100 GPUs with NVLink/NVSwitch interconnect, high-bandwidth networking, and optimized software (Base Command) in a single node designed for AI training and inference. It's the building block for DGX SuperPOD — a reference architecture for scaling to hundreds/thousands of GPUs.

---

### Q22. What is NVIDIA Base Command?

**A)** Base Command is NVIDIA's cluster management and orchestration platform for DGX systems. It handles job scheduling, resource allocation, user management, and cluster monitoring for AI workloads. Think of it as the operating system for a DGX cluster — it makes sure the right jobs run on the right GPUs with the right priority.

---

### Q23. What is MLOps and why does it matter?

**A)** MLOps (Machine Learning Operations) applies DevOps principles to the ML lifecycle — automating model training, testing, deployment, and monitoring pipelines. It matters because: (1) models degrade over time (data drift), (2) manual deployment doesn't scale, (3) reproducibility requires version control of data + code + models, (4) governance and compliance require audit trails.

---

# DOMAIN 2: AI INFRASTRUCTURE (24 Questions)

---

### Q24. What is NVLink and what problem does it solve?

**A)** NVLink is NVIDIA's high-bandwidth GPU-to-GPU interconnect. It provides much higher bandwidth than PCIe for GPU-to-GPU communication. In the H100, NVLink provides 900 GB/s bidirectional bandwidth. It solves the communication bottleneck when a model is too large for one GPU and must be split across multiple GPUs (model parallelism, pipeline parallelism). Without NVLink, GPUs wait for slow PCIe transfers.

---

### Q25. What is NVSwitch?

**A)** NVSwitch is a chip that connects all GPUs within a node via NVLink into a fully connected fabric. In DGX H100, NVSwitch connects all 8 GPUs so any GPU can communicate with any other GPU at full NVLink bandwidth simultaneously — no bottleneck, no hop penalty. This creates a single unified GPU memory space across the node.

---

### Q26. What is InfiniBand and why is it used for AI clusters?

**A)** InfiniBand is a high-bandwidth, low-latency networking technology used to connect nodes in AI clusters. NVIDIA's ConnectX adapters and Quantum switches provide up to 400 Gb/s per port. AI training across multiple nodes requires GPUs to constantly exchange gradients — InfiniBand's low latency and high bandwidth minimize this communication overhead. It's the standard for GPU cluster interconnect.

---

### Q27. Compare InfiniBand vs Ethernet for AI workloads.

**A)**
| | InfiniBand | Ethernet |
|---|---|---|
| Bandwidth | 400 Gb/s (NDR) | 400 Gb/s (available) |
| Latency | ~1 microsecond | ~5-10 microseconds |
| RDMA | Native (built-in) | Requires RoCE (overlay) |
| AI Training | Preferred — lower latency, native RDMA | Improving, but higher latency |
| Cost | Higher | Lower |
| Use case | Multi-node GPU training | General DC networking, inference |

InfiniBand wins for training because RDMA (Remote Direct Memory Access) lets GPUs read/write each other's memory directly without CPU involvement.

---

### Q28. What is RDMA and why is it critical for AI training?

**A)** RDMA (Remote Direct Memory Access) allows one machine to read/write the memory of another machine directly, bypassing the CPU and OS kernel. This dramatically reduces latency and CPU overhead. For AI training, GPUs need to exchange gradient updates millions of times — RDMA lets them do this at wire speed without CPU bottleneck. InfiniBand has native RDMA; Ethernet uses RoCE (RDMA over Converged Ethernet).

---

### Q29. What is a DPU (Data Processing Unit) and what is NVIDIA BlueField?

**A)** A DPU is a programmable processor that offloads and accelerates networking, storage, and security tasks from the CPU. NVIDIA BlueField is their DPU product line. Benefits: (1) frees CPUs/GPUs for AI compute instead of infrastructure tasks, (2) provides hardware-level network isolation and security, (3) accelerates storage I/O, (4) enables zero-trust security at the hardware level. In AI clusters, BlueField DPUs handle the networking so GPUs can focus on training.

---

### Q30. How do you scale GPU infrastructure? Explain scale-up vs scale-out.

**A)**
- **Scale-up**: Add more GPUs within a single node. Connected via NVLink/NVSwitch for maximum bandwidth. Limited by physical node size (typically 8 GPUs per DGX node). Best for single large models.
- **Scale-out**: Add more nodes to the cluster. Connected via InfiniBand or high-speed Ethernet. Scales to thousands of GPUs. Required when workloads exceed single-node capacity.

In practice, you do both: scale up to max GPUs per node, then scale out to more nodes.

---

### Q31. What GPU memory considerations matter for AI training vs inference?

**A)**
- **Training**: Needs large GPU memory to hold model parameters, gradients, optimizer states, and activations. A 70B parameter model may need 8× 80GB GPUs just for the model state. Memory bandwidth is critical for feeding data to compute units.
- **Inference**: Needs enough memory to hold the model weights + KV cache for active requests. Memory bandwidth is often the bottleneck for LLM inference (memory-bound, not compute-bound). Techniques like quantization (FP16→INT8→INT4) reduce memory footprint.

---

### Q32. What are the key power and cooling considerations for an AI data center?

**A)**
- **Power density**: GPU servers draw 5-10 kW per node (DGX H100 = ~10.2 kW). Much higher than traditional servers (1-2 kW).
- **Cooling**: Air cooling struggles above 30 kW/rack. Liquid cooling (direct-to-chip or immersion) required for high-density GPU deployments.
- **PUE**: Power Usage Effectiveness = total facility power / IT equipment power. Target <1.3. Best liquid-cooled facilities hit 1.03-1.1.
- **Power distribution**: 480V 3-phase for efficiency. PDUs rated for high-density loads.
- **Redundancy**: N+1 or 2N power redundancy for mission-critical AI workloads.

---

### Q33. What is PUE and what is a good target?

**A)** PUE (Power Usage Effectiveness) = Total Facility Power / IT Equipment Power. A PUE of 1.0 means ALL power goes to computing (impossible in practice). Industry average for traditional air-cooled facilities: ~1.58. Modern AI facilities target 1.2-1.3. Best-in-class liquid-cooled/immersion: 1.03-1.1. Lower PUE = less energy wasted on cooling and overhead = lower operating cost and better environmental profile.

---

### Q34. Compare air cooling vs liquid cooling for GPU infrastructure.

**A)**
| | Air Cooling | Liquid Cooling |
|---|---|---|
| Capacity | Up to ~30 kW/rack | 50-100+ kW/rack |
| PUE | 1.3-1.6 | 1.03-1.2 |
| Cost | Lower upfront | Higher upfront, lower ongoing |
| Noise | High | Low |
| Density | Limited | Enables full GPU density |
| DGX H100 | Possible but limiting | Recommended/required |
| Types | CRAH/CRAC, hot/cold aisle | Direct-to-chip (CDU), rear door, full immersion |

For modern GPU clusters (H100/Blackwell), liquid cooling is effectively required to run at full power.

---

### Q35. What is the difference between direct-to-chip liquid cooling and immersion cooling?

**A)**
- **Direct-to-chip (CDU)**: Cold plates mounted directly on GPU chips. Coolant circulates through the plates, absorbing heat. Rest of the server still uses air. Most common in enterprise (used in DGX SuperPOD reference architecture).
- **Immersion**: Entire server submerged in dielectric fluid (like EC-110). ALL components cooled simultaneously. Maximum heat removal. Highest density. Lowest PUE. More complex infrastructure (tanks, fluid management).

---

### Q36. What are the key components of an AI cluster?

**A)**
1. **GPU compute nodes** — DGX or HGX systems with 8 GPUs each
2. **High-speed network fabric** — InfiniBand or high-speed Ethernet (spine-leaf topology)
3. **Storage** — High-throughput parallel file system (GPFS, Lustre, or NFS with high IOPS)
4. **Network switches** — NVIDIA Quantum InfiniBand switches or Spectrum Ethernet switches
5. **Management plane** — BMC (Baseboard Management Controller), Base Command, DCGM
6. **Job scheduler** — Slurm or Kubernetes for workload management
7. **Power + cooling** — High-density PDUs, liquid cooling infrastructure

---

### Q37. What is a DGX SuperPOD?

**A)** DGX SuperPOD is NVIDIA's reference architecture for large-scale AI clusters. It defines how to connect multiple DGX systems with InfiniBand networking, shared storage, and management software into a validated, scalable design. A SuperPOD can scale from 20 to 140+ DGX nodes (160-1000+ GPUs). It specifies the exact network topology, storage configuration, and cabling — taking the guesswork out of building an AI cluster.

---

### Q38. What facility requirements must be considered for a GPU data center?

**A)**
1. **Power capacity** — 20-50+ MW for large clusters. Dedicated utility feed.
2. **Power density** — 30-100 kW per rack (vs 5-10 kW traditional)
3. **Cooling** — Liquid cooling infrastructure (CDU loops, chilled water, cooling towers)
4. **Floor loading** — GPU racks are heavy (2,000-3,000+ lbs per rack)
5. **Network** — Fiber-ready for InfiniBand/high-speed Ethernet cabling
6. **Physical security** — Access control, cameras, mantrap
7. **Fire suppression** — Clean agent (FM-200, Novec) for electronics
8. **Redundancy** — N+1 power, N+1 cooling, redundant network paths
9. **Compliance** — Uptime Institute tier rating, SOC 2, HIPAA if applicable

---

### Q39. What storage considerations matter for AI workloads?

**A)**
- **Training data**: Needs high-throughput reads — parallel file systems (Lustre, GPFS, BeeGFS) or high-performance NAS
- **Checkpointing**: Models checkpoint periodically during training — needs high write throughput to not stall GPUs
- **IOPS**: Random I/O for data loading. NVMe SSDs recommended for local scratch.
- **Capacity**: Datasets can be petabytes. Tiered storage (hot NVMe, warm HDD, cold object store)
- **Network bandwidth**: Storage fabric must keep up with GPU demand — a cluster of H100s can consume 100+ GB/s of data

---

### Q40. What is on-prem vs cloud for AI infrastructure? Key tradeoffs?

**A)**
| | On-Premises | Cloud |
|---|---|---|
| Control | Full hardware/software control | Limited to provider offerings |
| Cost (short-term) | High CapEx | Pay-per-use (OpEx) |
| Cost (long-term) | Lower TCO at sustained utilization | Higher TCO if always-on |
| Scaling | Weeks/months to add capacity | Minutes to scale up/down |
| Data sovereignty | Data stays on-site | Data in provider's region |
| GPU availability | Guaranteed once purchased | Subject to cloud capacity/pricing |
| Customization | Full (cooling, networking, etc.) | Limited by cloud provider |
| Best for | Sustained workloads, security-sensitive | Bursty workloads, experimentation |

---

### Q41. What is a spine-leaf network topology and why is it used in AI clusters?

**A)** Spine-leaf is a two-tier network architecture: every leaf switch connects to every spine switch. This provides: (1) predictable low latency (max 2 hops between any two servers), (2) high bandwidth (multiple parallel paths), (3) easy horizontal scaling (add leaf switches for more servers, add spine switches for more bandwidth). It's the standard for AI clusters because GPU-to-GPU communication needs consistent, low-latency paths.

---

### Q42. What networking bandwidth is typically needed for multi-node GPU training?

**A)** Each GPU node needs at least 400 Gb/s of inter-node bandwidth for efficient multi-node training. DGX H100 has 8× 400 Gb/s ConnectX-7 InfiniBand ports (3.2 Tb/s total per node). The rule: network bandwidth between nodes should be proportional to compute capability — otherwise GPUs idle waiting for gradient synchronization. This is why InfiniBand is preferred over standard Ethernet.

---

### Q43. What is GPU Direct RDMA and GPU Direct Storage?

**A)**
- **GPU Direct RDMA**: Allows network adapters to directly access GPU memory without going through system memory or CPU. Eliminates copy overhead for GPU-to-GPU communication across nodes. Critical for training scalability.
- **GPU Direct Storage**: Allows storage devices (NVMe) to transfer data directly to GPU memory, bypassing CPU and system memory. Eliminates the CPU bottleneck for data loading. Speeds up training data pipeline.

Both eliminate unnecessary data copies to keep GPUs fed and communicating at maximum speed.

---

### Q44. What is data parallelism vs model parallelism?

**A)**
- **Data parallelism**: Same model replicated on every GPU. Each GPU trains on a different batch of data. Gradients are synchronized across GPUs after each step. Works when the model fits on one GPU. Most common approach.
- **Model parallelism**: Model is split across multiple GPUs (different layers on different GPUs). Required when the model is too large for one GPU's memory. More complex, requires high-bandwidth interconnect (NVLink).
- **Pipeline parallelism**: A form of model parallelism where different stages of the model run on different GPUs in a pipeline fashion.

---

### Q45. How does GPU power consumption compare to traditional servers?

**A)** A single NVIDIA H100 GPU draws up to 700W TDP. A DGX H100 with 8 GPUs draws ~10.2 kW total. Compare to a traditional 1U server: 300-500W. This means GPU racks are 5-10x more power-dense, requiring: (1) higher amperage circuits, (2) liquid cooling, (3) more robust power distribution, (4) facility power upgrades. A 1,000-GPU cluster can consume 1-2 MW just for the GPUs.

---

### Q46. What is Multi-Instance GPU (MIG)?

**A)** MIG is an NVIDIA technology (available on A100 and H100) that partitions a single GPU into up to 7 isolated instances. Each instance has dedicated compute, memory, and memory bandwidth — fully isolated (a fault in one instance doesn't affect others). Use case: run multiple inference workloads on one GPU, or give multiple users dedicated GPU resources without interference. Maximizes GPU utilization for inference.

---

### Q47. What factors determine GPU hardware selection for a specific AI workload?

**A)** Key factors:
1. **Model size** — How much GPU memory is needed? (parameter count × bytes per parameter)
2. **Training vs inference** — Training needs max FLOPs; inference needs memory bandwidth + latency
3. **Precision requirements** — FP32, FP16, INT8, FP4? Determines which Tensor Core features matter
4. **Scaling needs** — Single GPU, single node (NVLink), or multi-node (InfiniBand)?
5. **Budget** — H100 vs A100 vs L40S vs consumer GPUs
6. **Throughput vs latency** — Batch size optimization, request queuing
7. **Software compatibility** — CUDA version, framework support, container availability

---

# DOMAIN 3: AI OPERATIONS (13 Questions)

---

### Q48. What is NVIDIA DCGM (Data Center GPU Manager)?

**A)** DCGM is NVIDIA's tool for monitoring and managing GPUs in data center environments. It provides: (1) GPU health monitoring (temperature, power, ECC errors, throttling), (2) diagnostic testing, (3) policy-based management (alert when thresholds crossed), (4) integration with monitoring systems (Prometheus, Grafana). It's the core GPU monitoring tool for any NVIDIA GPU deployment.

---

### Q49. What GPU metrics should you monitor in a production AI cluster?

**A)** Critical metrics:
1. **GPU utilization %** — Is the GPU actually computing? Low = workload bottleneck elsewhere
2. **Memory utilization** — How much GPU memory is in use vs available
3. **Temperature** — Thermal throttling starts at ~83°C. Monitor trends.
4. **Power draw** — Watts consumed vs TDP limit. Sustained max = thermal risk.
5. **ECC errors** — Memory errors. Correctable = watch trend. Uncorrectable = replace GPU.
6. **SM clock frequency** — If dropping below base, GPU is throttling
7. **PCIe/NVLink throughput** — Communication bottlenecks
8. **Memory bandwidth utilization** — Is memory the bottleneck?

DCGM exposes all of these via `nvidia-smi` or Prometheus metrics.

---

### Q50. What is a Baseboard Management Controller (BMC)?

**A)** BMC is an embedded microcontroller on the server motherboard that provides out-of-band management. It allows: (1) remote power on/off/reset, (2) hardware health monitoring (fans, temps, voltages), (3) remote console access (KVM over IP), (4) BIOS/firmware updates, (5) event logging. It works even when the server OS is crashed or powered off. Critical for managing servers in a data center remotely. Uses IPMI protocol.

---

### Q51. What is Kubernetes and how is it used for AI workloads?

**A)** Kubernetes (K8s) is an open-source container orchestration platform. For AI: (1) deploys and scales inference serving containers, (2) manages GPU resources across a cluster, (3) handles health checks and auto-restart of failed services, (4) enables rolling updates for model deployments, (5) integrates with NVIDIA GPU Operator for automatic GPU driver/toolkit management. Best suited for inference serving (Triton/NIM). Training often uses Slurm instead.

---

### Q52. What is the NVIDIA GPU Operator for Kubernetes?

**A)** The GPU Operator automates the management of all NVIDIA software components needed to run GPU workloads on Kubernetes — GPU drivers, container toolkit, device plugin, DCGM monitoring, MIG manager, and GFD (GPU Feature Discovery). Without it, admins must manually install and maintain all these components on every node. The GPU Operator installs them as containers, making GPU Kubernetes deployment plug-and-play.

---

### Q53. What is Slurm and why is it preferred for AI training over Kubernetes?

**A)** Slurm is a workload manager / job scheduler originally designed for HPC. For AI training it's preferred because: (1) native support for multi-node GPU jobs (MPI, NCCL), (2) efficient gang scheduling (all GPUs for a job allocated simultaneously), (3) lightweight — no container orchestration overhead, (4) mature priority/fairshare scheduling. Kubernetes is better for inference serving; Slurm is better for large training jobs that need guaranteed multi-node GPU allocations.

---

### Q54. What is the difference between gang scheduling and backfill scheduling?

**A)**
- **Gang scheduling**: All resources for a job are allocated simultaneously. If 64 GPUs are requested, the job waits until all 64 are available, then starts. Required for distributed training where all GPUs must start together.
- **Backfill scheduling**: Smaller jobs are allowed to run on idle resources while a large job waits for its full allocation — as long as the small jobs will finish before the large job's resources are ready. Improves cluster utilization.

---

### Q55. How do you virtualize GPU resources?

**A)** Three main approaches:
1. **MIG (Multi-Instance GPU)**: Hardware-level partitioning. Full isolation. A100/H100 only. Up to 7 instances per GPU.
2. **vGPU (NVIDIA Virtual GPU)**: Software virtualization. Shares a GPU across multiple VMs with time-slicing. Works with VMware/KVM. Good for VDI and multi-tenant inference.
3. **MPS (Multi-Process Service)**: Allows multiple CUDA processes to share a GPU concurrently. Less isolation than MIG but works on all NVIDIA GPUs.

MIG for strongest isolation. vGPU for VM environments. MPS for maximizing utilization on shared GPUs.

---

### Q56. What is the difference between time-slicing and MIG for GPU sharing?

**A)**
- **Time-slicing (vGPU)**: GPU rapidly switches between workloads. Processes share all GPU memory and compute — no isolation. One workload can impact another's performance. Simpler to set up.
- **MIG**: GPU is physically partitioned into separate instances with dedicated compute, memory, and bandwidth. Full isolation — one instance can't see or affect another. Better for production multi-tenant but only available on A100/H100 and reduces max per-workload resources.

---

### Q57. What data center management protocols and tools should an AI infrastructure operator know?

**A)**
- **IPMI/BMC**: Out-of-band server management (power, console, health)
- **SNMP**: Network device monitoring (switches, PDUs)
- **Redfish**: Modern REST API replacement for IPMI
- **DCGM**: NVIDIA GPU monitoring and diagnostics
- **Prometheus + Grafana**: Metrics collection and visualization
- **Syslog/ELK**: Log aggregation and analysis
- **Ansible/Terraform**: Infrastructure automation and configuration management
- **NVIDIA Base Command**: DGX cluster management

---

### Q58. What are the key considerations for GPU cluster job scheduling?

**A)**
1. **Priority queues** — Different priorities for training vs inference vs research
2. **Fair-share scheduling** — Prevent one user from monopolizing GPUs
3. **Gang scheduling** — Multi-GPU training needs all GPUs simultaneously
4. **Preemption** — High-priority jobs can preempt lower-priority ones
5. **Resource quotas** — Per-user or per-team GPU limits
6. **Job dependencies** — Data pipeline must complete before training starts
7. **Multi-node awareness** — Scheduler must understand GPU topology and network placement
8. **Checkpointing** — Long training jobs need checkpoint/restart capability

---

### Q59. What happens when a GPU develops ECC memory errors in a production cluster?

**A)** Two types:
- **Correctable (CE)**: Detected and corrected by hardware. Logged by DCGM. A few per day is normal. A rapidly increasing count indicates failing memory — schedule replacement during maintenance window.
- **Uncorrectable (UCE)**: Cannot be corrected. Will cause job failure or data corruption. Requires immediate action: (1) drain the node (stop scheduling new jobs), (2) complete or checkpoint running jobs, (3) run DCGM diagnostics, (4) RMA the GPU if persistent.

Monitor CE trend — it's the early warning for UCE failures.

---

### Q60. You're asked to design an AI cluster for training a 70B parameter LLM. What infrastructure would you specify?

**A)** A 70B parameter model at FP16 = ~140 GB just for weights. With optimizer states (Adam) and gradients, training needs ~4x = ~560 GB of GPU memory total.

**Spec:**
- **Compute**: Minimum 8× H100 80GB GPUs (1 DGX H100 node). For reasonable training time, 4-8 DGX nodes (32-64 H100s).
- **Interconnect**: NVLink within node, InfiniBand NDR 400 Gb/s between nodes
- **Network topology**: Spine-leaf, non-blocking
- **Storage**: Parallel file system (Lustre/GPFS), 100+ TB, 50+ GB/s read throughput for data loading
- **Memory**: 80GB per GPU × 64 GPUs = 5.12 TB total GPU memory (handles model + optimizer + activations with parallelism)
- **Software**: PyTorch + FSDP or Megatron-LM for distributed training, Slurm for scheduling, DCGM for monitoring
- **Cooling**: Liquid cooling (10.2 kW per DGX × 8 nodes = ~82 kW)
- **Power**: ~100 kW with overhead

---

# QUICK-REFERENCE CHEAT SHEET

## Key Numbers to Know

| Item | Number |
|------|--------|
| H100 TDP | 700W |
| H100 Memory | 80 GB HBM3 |
| H100 NVLink bandwidth | 900 GB/s |
| DGX H100 GPUs per node | 8 |
| DGX H100 total power | ~10.2 kW |
| InfiniBand NDR speed | 400 Gb/s per port |
| MIG max instances (H100) | 7 |
| Good PUE target | <1.3 (liquid: <1.1) |
| Industry average PUE | ~1.58 |
| CUDA cores purpose | Parallel compute (FP32) |
| Tensor Cores purpose | Matrix multiply (mixed precision) |

## Product → Purpose (Quick Map)

| Product | One-Line Purpose |
|---------|-----------------|
| CUDA | GPU parallel programming platform |
| TensorRT | Inference optimization engine |
| Triton | Multi-model inference server |
| NIM | Containerized inference microservices |
| NGC | GPU-optimized container/model registry |
| DCGM | GPU monitoring + diagnostics |
| Base Command | DGX cluster management |
| GPU Operator | Kubernetes GPU automation |
| NVLink | GPU-to-GPU high-bandwidth interconnect |
| NVSwitch | In-node all-to-all GPU fabric |
| InfiniBand | Inter-node high-speed network |
| BlueField DPU | Offload network/storage/security from CPU |
| MIG | Hardware GPU partitioning |
| RAPIDS | GPU-accelerated data science |
| Omniverse | Digital twin platform |
| Isaac Sim | Robot simulation |
| Metropolis | AI vision for video analytics |

---

*Go take a nap. Wake up, skim this once, crush that exam.*

*Mission Control — 2026-03-11*
