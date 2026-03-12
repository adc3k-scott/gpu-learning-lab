# ADC 3K — Modular DGX SuperPOD Infrastructure
## One-Pager for GTC 2026

---

**Advantage Design & Construction (ADC)** | Lafayette, Louisiana | adc3k.com
Scott Tomsu, Founder | 25-year ROV Superintendent & Robotics Specialist

---

## The Problem

AI compute infrastructure has four bottlenecks: **power, cooling, time, and scalability.**

Fixed facilities take 2-3 years to build, cost $500M+, fill once, and stop. When demand shifts, you build another building. When GPUs advance, you do a forklift upgrade. When one site goes down, everything stops.

## The Solution: Containerized DGX SuperPOD

The **ADC 3K** is a self-contained AI compute pod inside a 40-foot shipping container. Each pod is a **DGX SuperPOD building block** — self-powered, self-cooled, and remotely managed.

```
                    NVIDIA Quantum InfiniBand Spine
              ┌────────┼────────┼────────┐
              │        │        │        │
           [POD 1]  [POD 2]  [POD 3]  [POD 4]
            Leaf     Leaf     Leaf     Leaf

   Bottleneck at Pod 2? Inject another pod:

              ┌────────┼────────┼────────┐
              │        │        │        │
           [POD 1] [2a][2b]  [POD 3]  [POD 4]
                    ↑
              Fabric rebalances automatically
```

**Fat-tree topology.** Each pod connects to a shared NVIDIA Quantum InfiniBand spine. Add pods to scale wide. Inject pods to eliminate bottlenecks. AI monitoring (DCGM + UFM) identifies exactly where to deploy next. The fabric grows organically — no upper limit.

## Why This Can't Be Done With Fixed Buildings

| | Fixed Facility | ADC 3K Fabric |
|---|---|---|
| **Time to first revenue** | 2-3 years | 16 weeks |
| **Scale** | Fill once, build another | Add a leaf, fabric grows |
| **GPU upgrade** | Forklift swap, downtime | New pod, old pods keep running |
| **Failure mode** | Entire site goes dark | Fabric routes around it |
| **Power** | Utility-dependent | Self-powered micro grid |
| **Geographic flexibility** | Stuck where you built | Deploy anywhere |
| **Cost curve** | Flat | Declining — every pod makes every other pod more efficient |

## The Declining Cost Curve

```
COST PER TOKEN
  |\
  | \
  |  \___
  |      \____
  |           \_________
  |_________________________
                        PODS DEPLOYED
```

- **Fixed costs spread thinner**: NOC, spine switches, management — same cost at 4 pods or 40
- **AI optimization compounds**: More nodes = smarter scheduling = higher utilization
- **Power gets cheaper at scale**: Larger solar arrays, better genset load factors, amortized infrastructure
- **Manufacturing costs drop**: Volume pricing, faster assembly, amortized factory robots

## 100% NVIDIA Stack

| Layer | NVIDIA Technology |
|-------|-------------------|
| **Silicon** | Vera Rubin NVL72, Blackwell Ultra B300, Jetson AGX Orin, BlueField-3 DPU |
| **Intra-Pod** | NVLink 6 + NVSwitch (all-to-all GPU interconnect) |
| **Inter-Pod** | NVIDIA Quantum InfiniBand NDR (fat-tree spine fabric) |
| **Management** | Base Command Manager, DCGM, UFM, GPU Operator |
| **Software** | CUDA, TensorRT, Triton, NCCL, NIM, NGC, AI Enterprise |
| **Factory** | Omniverse (digital twin), Isaac Sim (robot paths), Metropolis (AI vision QA) |

Every layer is NVIDIA. No third-party alternatives. When NVIDIA looks at ADC, they see their own platform at every level.

## Flagship Site: Willow Glen Terminal

- **Location**: Former 2,200 MW Entergy power station, Mississippi River, St. Gabriel LA
- **Infrastructure already on-site**: 230kV Entergy substation (bidirectional), 3,500 ft deepwater dock, 700 acres, pipeline corridor, CN Railway, M2 zoning
- **Phase 1**: 4 pods (3 MW) in existing 20K SF warehouse — InfiniBand spine established
- **Phase 3**: 100+ MW AI campus — largest modular SuperPOD deployment in the country
- **Power**: Renewable micro grid — dock-imported fuels + solar + 230kV grid export
- **Cooling**: Mississippi River intake → plate heat exchanger → EC-110 immersion at PUE 1.03

## Pod Manufacturing

| | Step 1: Baton Rouge Terminal | Step 2: New Iberia Factory |
|---|---|---|
| **Type** | Leased building, manual assembly | Purpose-built, AI-automated |
| **Output** | 2-3 pods/month | 8-12 pods/month |
| **Timeline** | 60-90 days from lease | 14 months to build |
| **NVIDIA tech** | — | Omniverse, Isaac Sim, Metropolis, Jetson |
| **Capital** | $382-440K | $7.9-9.3M |

## The Numbers

| Metric | Value |
|--------|-------|
| PUE | 1.03 (vs. industry 1.58) |
| Energy cost | 3-5 cents/kWh (Henry Hub + solar) |
| Deploy time | 16 weeks (vs. 2-3 years) |
| Pod price | $120K-250K depending on config |
| Monthly revenue per pod | ~$150K (GPU-as-a-Service) |
| Cooling | Zero water consumption |
| Failure resilience | Fabric routes around any downed pod |

## What We Need from NVIDIA

1. **Inception membership** — validation, go-to-market support, partner badge
2. **Architecture review** — validate our NVL72 rack configs and InfiniBand fabric design
3. **Omniverse Enterprise** — simulate our automated factory before breaking ground
4. **Isaac Sim + Metropolis** — program robots and AI vision QA in simulation
5. **Technical partnership** — ADC becomes the reference implementation for containerized SuperPOD

## The Founder

**Scott Tomsu** — 25+ years operating robotics in the most extreme environments on earth. ROV Superintendent managing 24/7 deepwater operations at 3,000+ meters. Commercial saturation diver at 760 feet. FAA Private Pilot. FuelTech engine management certified. Multi-time drag racing champion.

ROVs are modular. They deploy to where the work is. They're managed remotely from a control room. They're upgraded component by component. Scott ran that system for 25 years underwater. Now he's doing the same thing with AI compute pods on land.

## Ready-Made Workforce

ADC's deployment crews come from the offshore ROV industry — operators who already set up shipping containers with computers, hook up generators, manage power switching, and troubleshoot electronic systems in remote environments. Pod deployment is a LARS mobilization with different payload. Scott knows where to find them, how to recruit them, and can explain GPU cooling in terms they already understand (oil-compensated motors, heat rejection, compensated housings). No other AI infrastructure company has access to this talent pool.

---

**ADC 3K: A supercomputer, a substation, and a renewable energy platform — all in shipping containers.**

adc3k.com | Lafayette, Louisiana

---

*Prepared for GTC 2026 — San Jose, CA — March 16-19*
