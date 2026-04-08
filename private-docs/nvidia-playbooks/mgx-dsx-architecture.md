# NVIDIA MGX + DSX Architecture -- ADC Hardware Reference Guide

**Last updated**: 2026-03-25
**Sources**: NVIDIA developer blogs, GTC 2026 announcements, SuperPOD reference architecture docs, CERAWeek 2026, OCP Summit, vendor press releases

---

## Table of Contents

1. [MGX Modular Reference Architecture](#1-mgx-modular-reference-architecture)
2. [DSX Reference Design (Vera Rubin DSX)](#2-dsx-reference-design-vera-rubin-dsx)
3. [800V DC Architecture](#3-800v-dc-architecture)
4. [NVLink Architecture](#4-nvlink-architecture)
5. [SuperPOD Reference Architecture](#5-superpod-reference-architecture)
6. [ADC Alignment Summary](#6-adc-alignment-summary)

---

## 1. MGX Modular Reference Architecture

### What MGX Is

MGX (Modular GPU eXchange) is NVIDIA's standardized hardware reference design for building AI factory racks. It is NOT a product -- it is a specification that OEM/ODM partners build to. MGX defines the mechanical, electrical, and cooling interfaces so that GPU modules, CPU modules, networking, and power can be mixed and matched across generations without redesigning the entire rack.

### Standardized Components

| Component | Function | Spec |
|-----------|----------|------|
| **MGX 1400A Busbar** | High-current DC power distribution within rack | 1,400A capacity, liquid-cooled |
| **MGX 54V Busbar** | Intermediate voltage distribution to compute trays | 54V DC rail |
| **MGX Coldplate** | Direct-to-chip liquid cooling for GPUs | Standardized mounting, <15C coolant delta under 1,400A loads |
| **MGX 44RU Manifold** | Rack-level coolant distribution | 44RU height, connects all coldplates to facility loop |
| **MGX NVQD** | NVIDIA Quick Disconnect -- tool-free coolant coupling | Drip-free disconnect for rack maintenance |
| **MGX UQD** | Universal Quick Disconnect (Staubli) -- industry-standard coupling | Interoperable with non-NVIDIA cooling loops |
| **MGX Power Whip** | Pre-terminated power cable assembly | Rack-to-PDU connection, factory-tested |
| **33 kW Power Shelf** | Rack-mounted power conversion | AC/DC or DC/DC, hot-swappable |
| **90 kW DC/DC Power Shelf** | High-density 1RU power conversion for 800V DC | Delta-manufactured, MGX-compatible |
| **1RU Power Capacitance Shelf** | Energy storage for GPU transient loads | MGX-compatible, supercapacitor cells |
| **Power Shelf Bracket** | Standardized mechanical mounting | Universal across MGX racks |
| **Slide Rail** | Standardized server/tray mounting | OCP Open Rack V3 compatible |
| **Midplane** | Replaces traditional cable connections | Blind-mate backplane for compute trays |

### Configurations

- **100+ combinations** of GPU, CPU, DPU, networking, and storage modules
- **90+ systems** from **25+ partners** released or in development
- Supports: single-node servers, multi-node servers, rack-scale systems (NVL72)
- GPU options: Blackwell, Rubin, future generations
- CPU options: NVIDIA Grace, NVIDIA Vera, AMD Turin, Intel Xeon 6, other Arm
- Networking: Quantum InfiniBand, Spectrum Ethernet, ConnectX, BlueField
- Storage: Direct-attached, fabric-attached via BlueField-4 STX

### Multi-Generational Compatibility

This is the key selling point. The same MGX rack footprint supports:

| Generation | System | Status |
|------------|--------|--------|
| Blackwell | GB200 NVL72 | Shipping now |
| Blackwell Ultra | GB300 NVL72 | Shipping 2025-2026 |
| Rubin | Vera Rubin NVL72 | H2 2026 |
| Rubin | Vera Rubin NVL72 CPX | H2 2026 |
| Rubin | Vera Rubin CPX | H2 2026 |
| Rubin Ultra | Kyber rack (NVL144) | 2027 |

Investment in MGX infrastructure today (busbars, manifolds, QDs, power shelves, racks) carries forward through at least 3 GPU generations. This is how NVIDIA protects partner CapEx.

### Deployment Economics

| Metric | MGX | Traditional |
|--------|-----|-------------|
| Development cost | **75% reduction** ($2-4M saved per platform) | Baseline |
| Development time | **6 months** | 12-18 months |
| Factory pre-integration | **~80% of components** | Minimal |
| Field deployment | **<90 days** from order | 12+ months |
| Power supply efficiency | **94%** | 88-92% |
| Total cost of ownership | **Up to 50% lower** | Baseline |

### OEM Partner Ecosystem

**50+ MGX partners** for Vera Rubin NVL72. **200+ ecosystem partners** adopting MGX components.

#### System Builders / ODMs (Confirmed)
ASRock Rack, ASUS, GIGABYTE, Ingrasys (Foxconn), Inventec, Pegatron, QCT (Quanta), Supermicro, Wistron, Wiwynn

#### Tier 1 OEMs (MGX-based systems)
Dell Technologies, Hewlett Packard Enterprise (HPE), Lenovo, Cisco

#### CPU Partners (MGX host processor modules)
AMD (Turin), Intel (Xeon 6 P-cores), NVIDIA (Grace, Vera)

#### Infrastructure / Component Partners
Amphenol (connectors), Asia Vital Components / AVC (thermal), Cooler Master (cooling), Colder Products / CPC (fluid couplings), Danfoss (cooling valves), Delta Electronics (power, cooling), LITEON (power supplies), Staubli (UQD couplings)

### OCP Alignment

- MGX rack design targets **OCP Open Rack V3** standard
- NOT standard 19-inch racks -- wider form factor (600mm+ width)
- OCP rack design files shared with partners through NPN (NVIDIA Partner Network)
- Rack-scale liquid cooling designed to OCP immersion and direct-to-chip standards

### How ADC Pure DC AI Cassettes Align with MGX

ADC Pure DC AI Cassettes use MGX-compatible components:
- **Staubli UQD** = the "MGX UQD" quick disconnect
- **800V busbars** = MGX busbar standard
- **Liquid cooling manifolds** = MGX 44RU manifold spec
- **Delta power shelves** = MGX 90 kW DC/DC shelves
- Pod receives NVIDIA-standard liquid-cooled racks built to MGX spec
- No custom rack engineering needed -- pods are the enclosure, MGX racks drop in

---

## 2. DSX Reference Design (Vera Rubin DSX)

### What DSX Is

DSX is NVIDIA's complete AI factory reference design -- the full blueprint from grid connection to token output. Announced March 16, 2026 at GTC. DSX is modular, composable, and open. It sits above MGX (which handles rack-level hardware) and addresses facility-level architecture.

### The Five DSX Pillars

#### DSX Max-Q -- Tokens Per Watt Optimization

**Purpose**: Maximize computing output per watt within a fixed power budget.

| Metric | Result |
|--------|--------|
| Power efficiency | 85% power delivers 93% throughput |
| Infrastructure density | **30% more AI infrastructure** in same power envelope |
| Dynamic provisioning | Power allocated across entire facility in real-time |
| Phaidra integration | ~10% additional compute capacity via AI-driven optimization |

How it works:
- Monitors GPU utilization, thermal state, and power draw across all racks
- Dynamically shifts power budget from idle/underutilized racks to active ones
- Manages GPU frequency/voltage curves for optimal tokens-per-watt
- Critical for power-constrained Phase 1 deployments (ADC's 3 MW start at Trappeys)

#### DSX Flex -- Grid Flexibility

**Purpose**: Connect AI factories to power-grid services for dynamic power management.

| Feature | Detail |
|---------|--------|
| Power orchestration | Dynamically adjust facility power use |
| Hybrid generation | Coordinate onsite gen (gas, solar, battery) with grid |
| Grid services | Participate in demand response, frequency regulation |
| Revenue | Sell excess power back to grid |

**Energy Partners**: AES, Constellation, Invenergy, NextEra Energy, Nscale Energy & Power, Vistra

**Key Implementation**: Emerald AI's Conductor platform orchestrates computational + onsite power resources in real-time. Tested at 5 commercial facilities. Commercial deployment later in 2026 at NVIDIA's Virginia AI factory.

**ADC Mapping**: DSX Flex maps directly to ADC's 4-Layer Power Hierarchy -- nat gas (backbone), solar (offset), diesel (emergency), grid (sell-back only). DSX Flex is the software that manages that stack.

#### DSX Exchange -- IT/OT Bridge

**Purpose**: Scalable, secure integration between compute (IT), facility operations (OT), and autonomous operations agents.

| Signal Domain | Examples |
|---------------|----------|
| Compute | GPU utilization, job queue depth, inference throughput |
| Network | InfiniBand fabric health, link errors, congestion |
| Energy | Generator output, solar production, battery SOC, grid draw |
| Power | PDU loads, busbar temperatures, conversion efficiency |
| Cooling | CDU flow rates, coolant temps, pump speeds, facility water |

DSX Exchange provides real-time APIs for all these signals, enabling:
- Single pane of glass for full-stack visibility
- Autonomous agents that optimize across domains (e.g., reduce cooling pump speed when GPU utilization drops)
- Maps to NVIDIA Mission Control (facility management platform)

#### DSX Sim -- Digital Twin Validation

**Purpose**: Model and validate AI factories as high-fidelity digital twins before construction.

| Feature | Detail |
|---------|--------|
| SimReady assets | 3D geometry + logistics + system behavior for generators, electrical equipment, cooling, racks |
| Thermal simulation | Full CFD for airflow and liquid cooling loops |
| Power simulation | Load flow, transient analysis, fault scenarios |
| Construction planning | Logistics, phasing, crane placement, truck routing |

**Key Partners**: Cadence, Dassault Systemes, Jacobs, PTC, Procore, Siemens, Switch

**Implementation**: Hitachi built a full 3D simulation model of 800 VDC architecture in Omniverse -- replicates power behavior from utility grid to rack. CoreWeave uses DSX Sim for cloud-based validation.

#### DSX Air -- Network Simulation Platform

**Purpose**: Cloud-based simulation of GPU clusters, networking, and partner infrastructure.

| Feature | Detail |
|---------|--------|
| Access | Cloud SaaS at air.nvidia.com |
| Cost | Free trial available |
| Scope | Model InfiniBand spine, NVL72 placement, storage fabric, networking topology |
| Output | Validated network design, performance projections |
| Use case | Design verification BEFORE spending on hardware |

DSX Air models GPU traffic patterns, InfiniBand congestion, NVLink domain behavior, and storage I/O. ADC should use this to validate Willow Glen and Trappeys network designs before ordering switches.

### Full DSX Software Stack

```
DSX Max-Q (power/performance optimization)
    |
DSX Flex (grid/generation management)
    |
DSX Exchange (IT/OT signal integration)
    |
NVIDIA Mission Control (facility management -- includes Base Command Manager + Run:ai)
    |
NVIDIA Dynamo (inference OS -- 7x throughput, disaggregated prefill/decode)
    |
NVIDIA NIM Operator (model serving on Kubernetes)
    |
NVIDIA GPU Operator + Network Operator (GPU + InfiniBand lifecycle)
    |
NVIDIA Container Toolkit (GPU container runtime)
    |
NVIDIA DCGM (GPU monitoring, 30+ metrics, Prometheus export)
    |
NVIDIA UFM 3.5 (InfiniBand fabric management + telemetry)
    |
NVIDIA Base Command Manager / cmsh (cluster provisioning + management)
    |
NVIDIA AI Enterprise (framework optimization, NIM microservices, NGC catalog)
```

### DSX Partner Ecosystem (200+)

**Infrastructure Design**: Cadence, Dassault Systemes, Jacobs, PTC, Procore, Siemens, Switch
**Power/Cooling**: Eaton, Schneider Electric, Trane Technologies, Vertiv
**Energy**: Emerald AI, GE Vernova, Hitachi Energy, Siemens Energy
**AI Optimization**: Phaidra, NScale
**Cloud Validation**: CoreWeave (DSX Air)

### DSX Deployment Phases for ADC

| Phase | DSX Tool | ADC Action | Timeline |
|-------|----------|------------|----------|
| Design | DSX Air | Simulate Trappeys + Willow Glen topology | NOW |
| Simulate | DSX Sim / Omniverse | 3D digital twin, investor walkthroughs | Pre-construction |
| Build | Partner ecosystem | Eaton power, Vertiv cooling, Delta racks | Post-permit |
| Deploy | Base Command Manager | 2-hour rack drops, fabric bring-up | Post-build |
| Operate | Mission Control + Dynamo | Token factory live, continuous optimization | Ongoing |

---

## 3. 800V DC Architecture

### Why 800V DC

Traditional AI factories use 415/480 VAC three-phase power. At rack densities above 100 kW, this becomes impractical -- massive copper, multiple conversion stages, 78% end-to-end efficiency. 800V DC fixes all of this.

| Metric | 800V DC | Traditional AC |
|--------|---------|----------------|
| End-to-end efficiency | **94-98%** | ~78% |
| Power per copper run | **157% more** (same gauge) | Baseline |
| Copper mass | **45-80% less** | Baseline |
| Cable cost (140 kW/rack) | ~$5/ft (3/0 AWG, 175A) | ~$14/ft (500 MCM, 350A) |
| Conversion stages | **2** (800V->12V->core) | 4-5 |
| Wire configuration | 3-wire (POS, RTN, PE) | 4-wire |
| CapEx savings | **$5.8-8M per 10 MW** | Baseline |
| Annual OpEx savings | **~$711K per 10 MW** | Baseline |
| TCO reduction | **Up to 30%** | Baseline |
| Maintenance cost reduction | **Up to 70%** | Baseline |

### Power Path: 800V Bus to GPU Chip

```
Grid (13.8 kV AC)
    |
Medium-Voltage Solid-State Transformer (SST)
    | (13.8 kV AC --> 800V DC, 98-99% efficiency)
    |
800V DC Distribution Busway
    | (facility-level, liquid-cooled busbars)
    |
In-Row Power Rack (e.g., Delta 660 kW)
    | (800V DC --> rack-level distribution)
    |
Late-Stage 64:1 LLC Converter (inside compute tray)
    | (800V DC --> 12V DC, single-stage, 26% less area)
    |    OR
    | Two-Stage Conversion (TI architecture):
    |   Stage 1: 800V --> 6V isolated bus converter (GaN, 97.6%)
    |   Stage 2: 6V --> <1V multiphase buck
    |
GPU Core Voltage (~0.7-1.0V)
```

The **64:1 LLC converter** is NVIDIA's Kyber-native design. It converts 800V directly to 12V in a single stage immediately adjacent to the GPU, using 26% less board area than traditional multi-stage approaches. This is the endgame architecture.

The **TI two-stage** approach (800V->6V->core) is an alternative available now, shipping as reference designs with 97.6% efficiency GaN converters.

### Kyber Rack -- Next-Gen 800V Native

| Spec | Detail |
|------|--------|
| Name | Kyber (successor to Oberon) |
| GPU count | 576 Rubin Ultra GPUs per rack |
| Configuration | NVL144 (2x NVL72 domains) |
| Power | **600 kW - 1 MW per rack** |
| Voltage | 800V DC native -- NO AC conversion in rack |
| Power input | Two conductor 800V feeds |
| Energy storage | **20x more** than current racks (supercapacitors for GPU transients) |
| Cooling | 100% liquid-cooled, 45C hot water |
| Timeline | **2027 production** |

Kyber accepts 800V DC directly. DC/DC conversion happens inside the compute rack to step down to GPU-level voltages. There is no AC/DC conversion stage at the rack level at all.

### Integrated Energy Storage -- Multi-Timescale

800V DC architecture requires integrated energy storage at multiple timescales:

| Timescale | Technology | Purpose | Location |
|-----------|------------|---------|----------|
| Microseconds-milliseconds | High-power capacitors, supercapacitors | GPU dynamic power transients (load spikes during batch transitions) | In-rack, on power shelves |
| Seconds-minutes | Rack-level battery backup units (BBU) | Ride-through for power switching, generator start | In-row power rack (e.g., Delta 480 kW BBU) |
| Minutes-hours | Facility-level BESS (battery energy storage system) | Utility interconnection, demand response, solar smoothing | Facility perimeter |

Energy storage acts as a "low-pass filter" -- decoupling GPU power demands (violent, bursty) from the grid/generator (slow, steady). Delta's 660 kW power rack ships with 480 kW of embedded BBU per rack (80 kW per shelf x 6 shelves).

### When Does 800V Become Mandatory?

| Date | Milestone |
|------|-----------|
| Q1 2026 | Equipment commercially available (Delta, Schneider, TI, Infineon, Vicor, Navitas) |
| H2 2026 | Vertiv complete 800V DC portfolio ships |
| 2027 | **Rubin Ultra + Kyber rack production** -- 800V DC required for Kyber |
| 2027 | Heron Power SST pilot production (4.2 MW, 98.5%) |
| 2028 | **800V DC becomes industry standard** |

For ADC: Any facility designed for Vera Rubin NVL72 (H2 2026) can use either AC or 800V DC. But any facility targeting Kyber/Rubin Ultra (2027) **must** be 800V DC native. Design for 800V from day one -- it cannot be retrofitted.

### 800V DC Ecosystem Partners (NVIDIA Official)

**Silicon Providers (14)**: AOS, Analog Devices, Efficient Power Conversion, Infineon, Innoscience, MPS, Navitas, onsemi, Power Integrations, Renesas, Richtek, ROHM, STMicroelectronics, Texas Instruments

**Power System Components (6)**: Bizlink, Delta, Flex, Lead Wealth, LITEON, Megmeet

**Data Center Power Systems (9)**: ABB, Eaton, GE Vernova, Heron Power, Hitachi Energy, Mitsubishi Electric, Schneider Electric, Siemens, Vertiv

**SST Startups**: Amperesand, Heron Power, DG Matrix

**Grid Flexibility Partners**: AES, Constellation, Invenergy, NextEra Energy, Nscale Energy & Power, Vistra

### Key Equipment Available Now (Q1 2026)

| Vendor | Product | Key Spec |
|--------|---------|----------|
| Delta Electronics | 660 kW In-Row Power Rack | 6x 110 kW shelves, 480 kW BBU, 98% efficiency |
| Delta Electronics | 90 kW DC/DC Power Shelf | 1RU, MGX-compatible |
| Delta Electronics | SST | 98.5% efficiency, MV AC to 800V DC |
| Schneider Electric | 800V DC Sidecar | Up to 1.2 MW per rack |
| Eaton | Beam Rubin DSX Platform | Modular, Fibrebond enclosures, Boyd Thermal cooling |
| TI | 800V-to-6V GaN IBC | 97.6% efficiency, >2,000 W/in3 |
| Infineon | CoolGaN HV IBC | >98% efficiency, 60x60x11mm, 2.5 kW/in3 |
| Navitas | 800V-to-6V GaN PDB | 96.5% efficiency, 2,100 W/in3 |
| Vicor | BCM6135 800V-to-48V | 97% efficiency, 3.8 kW |
| Amperesand | MV SST | 30 MW contracted, shipping 2026 |

---

## 4. NVLink Architecture

### NVLink Generations

| Generation | Platform | Per-GPU BW | Rack BW | GPU Domain |
|------------|----------|------------|---------|------------|
| NVLink 4 | Hopper (H100) | 900 GB/s | N/A (8 GPU domains) | 8 GPUs |
| NVLink 5 | Blackwell (GB200) | 1.8 TB/s | 130 TB/s | 72 GPUs |
| NVLink 6 | Vera Rubin | **3.6 TB/s** | **260 TB/s** | **72 GPUs** |

### What "72 GPUs in One Domain" Means

An NVLink domain is a set of GPUs connected through NVLink switches in an **all-to-all topology**. Within a domain:

- Every GPU can communicate directly with every other GPU at full NVLink bandwidth
- All communication is **single-hop** (GPU -> NVLink switch -> GPU), no multi-hop routing
- The 72 GPUs behave as **one large accelerator** from the software perspective
- Memory across all 72 GPUs is addressable as a unified pool (20.7 TB HBM4 on Vera Rubin)
- Latency is **uniform and predictable** across all GPU pairs -- no NUMA effects within the domain
- Critical for: MoE (Mixture of Experts) routing, collective operations, KV cache sharing, synchronization-heavy inference

This is fundamentally different from a cluster of GPUs connected by InfiniBand. Within an NVLink domain, there are no network stacks, no protocol overhead, no software routing -- it is a hardware fabric with deterministic latency.

### NVLink 6 Switch Tray Architecture (Vera Rubin)

| Component | Spec |
|-----------|------|
| NVLink 6 switches per rack | **36 switches** |
| Bandwidth per switch | 28.8 TB/s total |
| In-network compute per switch | 14.4 TFLOPS FP8 |
| Total rack scale-up bandwidth | **260 TB/s** |
| Topology | All-to-all (full mesh via switch trays) |
| Hop count | **Single hop** between any two GPUs in domain |

The 36 NVLink switches are arranged in switch trays within the NVL72 rack. They provide the all-to-all connectivity fabric. Each switch tray handles a subset of the GPU-to-GPU connections, but the aggregate provides full bisection bandwidth.

**In-network compute** (14.4 TFLOPS FP8 per switch) is a new capability in NVLink 6. The switches themselves can perform reduction operations (allreduce, allgather) directly in the switch silicon, reducing GPU idle time during collective operations. This is similar to InfiniBand SHARP but at NVLink speeds.

### NVLink vs InfiniBand: Scale-Up vs Scale-Out

```
|<------ NVLink Domain (Scale-Up) ------>|<------ InfiniBand Fabric (Scale-Out) ------>|
|                                         |                                              |
| 72 GPUs in one NVL72 rack              | Multiple NVL72 racks in a SuperPOD           |
| 260 TB/s aggregate bandwidth            | 800 Gbps per link (XDR InfiniBand)           |
| All-to-all, single hop                  | Fat-tree, multi-hop                          |
| Hardware fabric, zero software overhead | RDMA, minimal software overhead              |
| Uniform latency (~1 us)                | Variable latency (1-5 us depending on hops)  |
| Fixed domain (72 GPUs)                  | Scales to thousands of GPUs                  |
```

**Scale-up (NVLink)**: Communication WITHIN a rack. Used for tensor parallelism, pipeline parallelism stages, MoE expert routing, KV cache sharing. Optimized for communication-dominated AI workloads where GPUs need to exchange data at every layer.

**Scale-out (InfiniBand or Spectrum-X Ethernet)**: Communication BETWEEN racks. Used for data parallelism, distributed training across nodes, model parallel stages that span racks. Uses RDMA for low-latency, high-bandwidth transfers.

**ConnectX-9 SuperNIC** (ships with Vera Rubin): 1.6 Tb/s, dual-protocol (InfiniBand + Ethernet). This is the scale-out NIC -- each NVL72 rack has multiple ConnectX-9 cards connecting to the InfiniBand or Ethernet fabric.

**BlueField-4 DPU** (ships 2026): 64 Arm cores, 800 Gb/s, integrated ConnectX-9. Offloads networking, security, and storage I/O from the main GPUs. Used for storage fabric connections (BlueField-4 STX racks).

### Vera Rubin NVL72 -- Complete Chip Lineup

| Chip | Role | Key Specs |
|------|------|-----------|
| **Rubin GPU** | Compute | 336B transistors, 224 SMs, 5th-gen Tensor Cores, 288 GB HBM4, 22 TB/s memory BW, 50 PFLOPS NVFP4 inference |
| **Vera CPU** | Host processor | 88 Olympus cores, 176 threads (Spatial Multithreading), 1.5 TB LPDDR5X, 1.2 TB/s memory BW, Arm v9.2 |
| **NVLink 6 Switch** | Intra-rack fabric | 28.8 TB/s, 14.4 TFLOPS FP8 in-network compute |
| **ConnectX-9 SuperNIC** | Scale-out networking | 1.6 Tb/s, dual-protocol IB/Ethernet |
| **BlueField-4 DPU** | Infrastructure offload | 64 Arm cores, 800 Gb/s, integrated CX-9 |
| **NVLink-C2C** | CPU-GPU coherent link | 1.8 TB/s bidirectional, unified CPU-GPU address space |

---

## 5. SuperPOD Reference Architecture

### What a SuperPOD Is

A DGX SuperPOD is NVIDIA's validated, tested reference architecture for large-scale AI compute clusters. It defines everything: rack layout, network topology, power, cooling, cabling, software stack, and operational procedures. Building to SuperPOD spec is how partners achieve DGX-Ready and NCP certification.

### Scalable Unit (SU) Definitions by Generation

| Generation | GPUs per System | Systems per SU | GPUs per SU | Max Validated Scale |
|------------|----------------|----------------|-------------|---------------------|
| DGX H100 | 8 | 32 (31 usable, 1 for UFM) | 248 | 4 SU = 1,016 GPUs |
| DGX B200 | 8 | 32 | 256 | TBD |
| DGX B300 (IB XDR) | 8 | 72 | 576 | **8 SU = 4,608 GPUs** |
| DGX B300 (Ethernet) | 8 | 64 | 512 | 4 SU = 2,048 GPUs |
| DGX GB200 NVL72 | 72 per rack | 8 racks | 576 | 16+ SU |
| Vera Rubin NVL72 | 72 per rack | 8 racks (expected) | 576 | TBD (128+ racks) |

**For NVL72 racks**: 1 SU = 8 NVL72 racks = 576 GPUs. This is the atomic deployment unit. You can deploy 1 SU and scale up. The B300 SuperPOD is validated to 8 SU (576 nodes, 4,608 GPUs). Larger deployments are possible but require custom validation.

### How SUs Connect -- Fat-Tree InfiniBand Topology

The compute fabric uses a **rail-optimized, non-blocking, twin-plane fat-tree topology**:

```
                    [Core Switches]
                    /    |    |    \
              [Spine Switches per SU]
              /    |    |    |    \
        [Leaf Switches - 1 per compute rack]
        /    |    |    |    |    \
    [DGX Systems / NVL72 Racks]
```

**Rail-optimized** means each GPU NIC in a multi-GPU system connects to a different leaf switch (one per "rail"). Traffic from the same rail across all nodes is always one hop away via the leaf switch. Cross-rail traffic traverses the spine layer.

**B300 XDR InfiniBand Fabric Scale**:

| SUs | Nodes | GPUs | Leaf Switches | Spine Switches | Total IB Links |
|-----|-------|------|---------------|----------------|----------------|
| 1 | 72 | 576 | 4 | -- | 576 |
| 2 | 144 | 1,152 | 8 | -- | 1,152 |
| 4 | 288 | 2,304 | 18 | -- | 2,304 |
| 8 | 576 | 4,608 | 36 | -- | 4,608 |

### Four Network Fabrics

Every SuperPOD implements four physically separate network fabrics:

#### 1. Compute Fabric (InfiniBand)

| Component | Spec |
|-----------|------|
| Protocol | InfiniBand XDR (800 Gbps) or NDR (400 Gbps) |
| Switch | Quantum-X800 Q3400-RA (XDR) or QM9700 (NDR) |
| Topology | Rail-optimized, non-blocking, twin-plane fat-tree |
| Purpose | GPU-to-GPU RDMA across racks (training collectives, distributed inference) |
| Management | UFM 3.5 Enterprise (connects to 4 FNM ports per Q3400) |
| Features | SHARPv4 in-network computing, adaptive routing, congestion control |

This is the high-performance fabric. ALL GPU-to-GPU traffic between racks flows over this fabric. Within a rack, NVLink handles GPU-to-GPU; between racks, InfiniBand handles it.

#### 2. Storage Fabric

| Option | Switch | Bandwidth | Protocol |
|--------|--------|-----------|----------|
| InfiniBand | QM9700 NDR | >80 GBps per node I/O | IB RDMA |
| Ethernet | SN5610 (AC) / SN5600D (DC) | >80 GBps per node I/O | RoCE |

Storage devices connected 1:1. DGX B300 systems at ~4:3 oversubscription. Storage targets: POSIX-compliant parallel file systems (DDN, VAST, WEKA). Minimum 40 GBps per-node sustained I/O.

#### 3. In-Band Management Network

| Component | Spec |
|-----------|------|
| Switch | SN5610 (Spectrum-4, 64x 800 Gbps) |
| Speed | 200 Gbps bonded per node |
| Purpose | Cluster management (Mission Control, BCM, Slurm, K8s), NFS, NGC registry, user SSH, data movement |
| Scope | Accessible by users and administrators |

#### 4. Out-of-Band (OOB) Management Network

| Component | Spec |
|-----------|------|
| Switch | SN2201 / SN2201M (48x 1 Gbps + 4x 100 Gbps) |
| Purpose | BMC/IPMI ports, fabric management switches, console servers |
| Scope | **Physically isolated** from users via VLAN/EVPN on dedicated VXLAN |
| Security | No user access -- infrastructure management only |

### Maximum Scale

| Configuration | Validated | Theoretical Max |
|---------------|-----------|-----------------|
| B300 + IB XDR | 8 SU (4,608 GPUs) | 72+ SU (2,000+ nodes) |
| B300 + Ethernet | 4 SU (2,048 GPUs) | TBD |
| GB200 NVL72 | 16+ SU (9,216 GPUs) | 128+ racks |
| Vera Rubin NVL72 | TBD | Expected 128+ racks (9,216+ GPUs) |

### Required Software Stack

| Software | Function | Licensing |
|----------|----------|-----------|
| **NVIDIA Mission Control** | Full-stack facility management (includes BCM + Run:ai) | Included with SuperPOD |
| **Base Command Manager (BCM)** | Cluster provisioning, OS imaging, node management (cmsh CLI) | Free tier: 8 GPUs/system |
| **Run:ai** | GPU workload scheduling, dynamic resource allocation | Included in Mission Control |
| **UFM 3.5 Enterprise** | InfiniBand fabric management, telemetry, health, adaptive routing | Enterprise license |
| **DCGM** | GPU health monitoring (30+ metrics), Prometheus export | Open source / included |
| **GPU Operator** | Kubernetes GPU lifecycle (drivers, device plugins, MIG) | Open source |
| **Network Operator** | Kubernetes networking lifecycle (GPUDirect RDMA) | Open source |
| **NIM Operator** | Inference microservice deployment on K8s | AI Enterprise license |
| **NGC** | Container registry, pretrained models, CVE-scanned images | Free tier available |
| **AI Enterprise** | End-to-end AI platform (frameworks, NIM, support) | Included with DGX |
| **Slurm** | HPC job scheduler (alternative to K8s for training) | Open source |

### SuperPOD Power and Cooling Requirements

| Generation | Power per Rack | Cooling |
|------------|---------------|---------|
| DGX H100 | ~40 kW | Air-cooled |
| DGX B300 | ~56 kW (4 systems/rack) | Air or liquid |
| GB200 NVL72 | 120-140 kW | **Liquid cooling mandatory** (45C hot water) |
| Vera Rubin NVL72 | 190-230 kW (Max-Q to Max-P) | **Liquid cooling mandatory** (45C hot water) |
| Kyber (Rubin Ultra) | 600 kW - 1 MW | **Liquid cooling mandatory** + 800V DC |

---

## 6. ADC Alignment Summary

### How Each Architecture Maps to ADC

| NVIDIA Architecture | ADC Application | Status |
|--------------------|-----------------|--------|
| **MGX** | ADC Pure DC AI Cassette rack compatibility -- pods receive MGX-standard racks | Aligned (Staubli UQD, 800V busbars, Delta shelves) |
| **DSX** | Facility-level blueprint for Trappeys + Willow Glen | Blueprint adopted, DSX Air trial pending |
| **800V DC** | Day-1 power architecture for all new facilities | Designed in (solar-direct validated) |
| **NVLink 6** | Intra-rack compute fabric (no ADC engineering needed -- comes with NVL72) | Built into rack purchase |
| **InfiniBand** | Inter-rack compute fabric at Willow Glen (Quantum-X800 spine) | Spec'd (SuperPOD topology) |
| **SuperPOD** | Willow Glen target architecture (8+ SU, 576+ GPUs first phase) | Reference architecture adopted |

### ADC's Build Sequence (DSX-Aligned)

```
1. DSX Air          --> Simulate Trappeys + Willow Glen network topology (NOW)
2. DSX Sim          --> 3D digital twin for investor walkthroughs (pre-construction)
3. MGX racks        --> Order NVL72 racks through OEM (Supermicro/Dell/HPE)
4. 800V DC          --> Eaton Beam / Delta power infrastructure (Phase 1 build)
5. SuperPOD fabric  --> Quantum-X800 InfiniBand + 4 network fabrics (Phase 1 deploy)
6. Mission Control  --> BCM + UFM + DCGM + Run:ai (Phase 1 operate)
7. DSX Max-Q        --> Optimize tokens/watt within power envelope (ongoing)
8. DSX Flex         --> Grid services + power sell-back (Phase 2+)
9. DSX Exchange     --> Full IT/OT integration + autonomous ops (Phase 2+)
```

### Key Numbers for Investor Deck

| Metric | Value | Source |
|--------|-------|--------|
| MGX configurations | 100+ | NVIDIA MGX spec |
| MGX partners | 200+ ecosystem, 50+ for Vera Rubin | NVIDIA OCP Summit 2025 |
| DSX Max-Q density gain | 30% more infrastructure in same power | GTC 2026 |
| 800V DC CapEx savings | $5.8-8M per 10 MW | Enteligent white paper |
| 800V DC TCO reduction | Up to 30% | NVIDIA 800V blog |
| NVLink 6 bandwidth | 260 TB/s per rack | CES 2026 |
| Vera Rubin inference | 50 PFLOPS NVFP4 per rack | NVIDIA spec |
| Vera Rubin cost/token | 10x lower than Blackwell | CES 2026 |
| SuperPOD max scale | 9,216+ GPUs (128+ racks) | NVIDIA ref arch |
| Rack install time | 2 hours (liquid-cooled, pre-integrated) | NVIDIA DSX |
| MGX deployment | <90 days from order | NVIDIA MGX spec |

---

## Source URLs

- [NVIDIA MGX Platform](https://www.nvidia.com/en-us/data-center/products/mgx/)
- [Building the Modular Foundation for AI Factories with NVIDIA MGX](https://developer.nvidia.com/blog/building-the-modular-foundation-for-ai-factories-with-nvidia-mgx/)
- [NVIDIA MGX Gives System Makers Modular Architecture](https://nvidianews.nvidia.com/news/nvidia-mgx-server-specification/)
- [Computer Industry Joins NVIDIA to Build AI Factories](https://nvidianews.nvidia.com/news/computer-industry-ai-factories-data-centers/)
- [NVIDIA Partners Drive Next-Gen Efficient Gigawatt AI Factories](https://blogs.nvidia.com/blog/gigawatt-ai-factories-ocp-vera-rubin/)
- [NVIDIA Vera Rubin DSX AI Factory Reference Design](https://nvidianews.nvidia.com/news/nvidia-releases-vera-rubin-dsx-ai-factory-reference-design-and-omniverse-dsx-digital-twin-blueprint-with-broad-industry-support)
- [Inside the NVIDIA Vera Rubin Platform: Six New Chips](https://developer.nvidia.com/blog/inside-the-nvidia-rubin-platform-six-new-chips-one-ai-supercomputer/)
- [NVIDIA Vera Rubin NVL72](https://www.nvidia.com/en-us/data-center/vera-rubin-nvl72/)
- [NVIDIA 800 VDC Architecture for AI Factories](https://developer.nvidia.com/blog/nvidia-800-v-hvdc-architecture-will-power-the-next-generation-of-ai-factories/)
- [Building the 800 VDC Ecosystem](https://developer.nvidia.com/blog/building-the-800-vdc-ecosystem-for-efficient-scalable-ai-factories/)
- [SuperPOD B300 XDR Reference Architecture](https://docs.nvidia.com/dgx-superpod/reference-architecture/scalable-infrastructure-b300-xdr/latest/dgx-superpod-components.html)
- [SuperPOD B300 Network Fabrics](https://docs.nvidia.com/dgx-superpod/reference-architecture/scalable-infrastructure-b300-xdr/latest/network-fabrics.html)
- [SuperPOD B300 Software](https://docs.nvidia.com/dgx-superpod/reference-architecture/scalable-infrastructure-b300/latest/dgx-software.html)
- [SuperPOD GB200 Reference Architecture](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-gb200/latest/abstract.html)
- [NVIDIA DSX Architecture Targets Token-Per-Watt Optimization](https://convergedigest.com/nvidia-dsx-architecture-targets-token-per-watt-optimization/)
- [NVLink 6 Backbone of Rubin Rack-Scale Architecture](https://convergedigest.com/nvlink-6-becomes-the-backbone-of-rubin-rack-scale-ai-architecture/)
- [Kyber Racks and Rubin Ultra (Tom's Hardware)](https://www.tomshardware.com/pc-components/gpus/nvidia-shows-off-rubin-ultra-with-600-000-watt-kyber-racks-and-infrastructure-coming-in-2027)
- [The Megawatt Shift: NVIDIA's 800 VDC Strategy](https://convergedigest.com/the-megawatt-shift-nvidias-800-vdc-strategy/)
