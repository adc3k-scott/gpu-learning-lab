# The ADC 3K Pod — Your Edge AI Node
*Notion backup — 2026-04-03*

# The ADC 3K Pod Is Already an Edge Product
> We don't need to build a new product. We need to NAME the product we already have. The pod is a self-powered, self-cooled, remotely-managed edge AI node. That's not marketing spin — that's literally what it does.
---
## What Makes Something an "Edge" Product?
Here's the checklist. If a product does all five of these things, it's edge infrastructure:
```plain text

EDGE INFRASTRUCTURE CHECKLIST          ADC 3K POD
─────────────────────────────────      ──────────────────────
✅ 1. Deploys AT the customer site     40-ft ISO container, crane-ready
✅ 2. Runs WITHOUT cloud dependency    Self-powered (Bloom SOFC + solar + battery)
✅ 3. Processes data LOCALLY            GPU racks running NVIDIA AI Enterprise
✅ 4. Survives harsh environments      Liquid cooled, desiccant humidity control
✅ 5. Managed REMOTELY                 MARLIE I NOC, 24/7 monitoring

                    SCORE: 5 out of 5 — THIS IS AN EDGE PRODUCT

```
---
## How the Pod Works as an Edge Node
Let's walk through a real deployment — step by step — so anyone can understand it.
### Step 1: The Customer Has a Problem
A hospital in Baton Rouge wants to run AI on their radiology images. They can't send patient X-rays to Amazon's cloud because of HIPAA laws. They don't have GPU engineers on staff. They need a solution that works without changing how their hospital operates.
### Step 2: We Ship a Pod
We manufacture the pod at our facility in Lafayette. It's a 40-foot High Cube ISO container — the same kind you see on cargo ships. Inside: 10 NVL72 GPU racks (8 compute + 1 network + 1 storage), a liquid cooling loop with external dry cooler, 800V DC power system, networking equipment, and Novec 1230 fire suppression. Everything is pre-configured before it leaves our building.
```plain text

INSIDE AN ADC 3K EDGE POD
┌──────────────────────────────────────────────────────────────┐
│                   20-FOOT ISO CONTAINER                       │
│                                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ GPU RACK │  │ GPU RACK │  │ GPU RACK │  │ GPU RACK │    │
│  │  NVL72   │  │  NVL72   │  │  NVL72   │  │  NVL72   │    │
│  │ immersed │  │ immersed │  │ immersed │  │ immersed │    │
│  │ in fluid │  │ in fluid │  │ in fluid │  │ in fluid │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
│                                                               │
│  ┌─────────────────┐  ┌──────────┐  ┌───────────────────┐  │
│  │  POWER SYSTEM   │  │ COOLING  │  │  FIRE SUPPRESSION │  │
│  │  UPS + Transfer │  │  CDU +   │  │  VESDA + FK-5-1-12│  │
│  │  Switch         │  │  Dry     │  │  (clean agent,    │  │
│  │                 │  │  Cooler  │  │   safe for GPUs)   │  │
│  └─────────────────┘  └──────────┘  └───────────────────┘  │
│                                                               │
│  ← GAS IN    ← NETWORK IN    → EXHAUST OUT                  │
└──────────────────────────────────────────────────────────────┘

```
### Step 3: We Drop It On-Site
A flatbed truck delivers the pod to the hospital's utility yard. A crane sets it on a concrete pad. We connect three things: a natural gas line (for power), a network cable (for data), and a water line (for the cooling system's dry cooler). That's it. No construction. No HVAC installation. No building permits for a server room.
### Step 4: We Turn It On From Lafayette
Our team at MARLIE I — our network operations center in Lafayette — powers up the pod remotely. They configure the AI software (NVIDIA NIMs for medical imaging), run diagnostics, and hand the hospital a simple login: "Here's your dashboard. Your radiologists can now get AI-assisted reads in 2 seconds instead of sending films out for 24-hour turnaround."
### Step 5: We Manage It Forever
The hospital never touches the pod. MARLIE I monitors it 24/7 — temperature, power draw, GPU health, software updates, security patches. If a GPU fails, we dispatch a technician. If the hospital needs more compute, we ship another pod. The hospital's IT department does nothing.
```plain text

THE EDGE LIFECYCLE — HOW IT FLOWS

  MANUFACTURE           DEPLOY              OPERATE              SCALE
  ┌─────────┐          ┌─────────┐         ┌─────────┐         ┌─────────┐
  │ Build in │   ───→   │ Ship to │   ───→  │Manage   │   ───→  │ Add more│
  │Lafayette │          │customer │         │from     │         │ pods as │
  │ Pre-test │          │  site   │         │MARLIE I │         │ needed  │
  │ Pre-load │          │ 3 plugs │         │  24/7   │         │         │
  └─────────┘          └─────────┘         └─────────┘         └─────────┘
     2-4 weeks           1 day               Ongoing              2 weeks

```
---
## Edge vs. Cloud vs. AI Factory — When to Use Each
Not everything belongs at the edge. Here's the simple rule:
```plain text

┌──────────────────┬─────────────────────────┬────────────────────────┐
│                  │ USE THIS WHEN...         │ ADC PRODUCT            │
├──────────────────┼─────────────────────────┼────────────────────────┤
│ ☁️  CLOUD        │ You're a startup with no │ Not our business.      │
│ (Amazon/Google)  │ sensitive data and don't │ Let Amazon have it.    │
│                  │ need real-time speed.    │                        │
├──────────────────┼─────────────────────────┼────────────────────────┤
│ 🏭 AI FACTORY    │ You need massive compute │ MARLIE I               │
│ (Regional hub)   │ for AI training, or you  │ Willow Glen            │
│                  │ want colocation.         │                        │
├──────────────────┼─────────────────────────┼────────────────────────┤
│ 📦 EDGE          │ Data can't leave your    │ ADC 3K POD             │
│ (On your site)   │ building, you need       │ Shipped to your door.  │
│                  │ instant AI, or you're    │ Managed from ours.     │
│                  │ in a remote location.    │                        │
└──────────────────┴─────────────────────────┴────────────────────────┘

```
> The power of ADC's model: we don't just sell one ring. We sell all three. MARLIE I is the brain. The pods are the hands. The customer picks where they need compute, and we deliver it — in a building or in a box.
---
## The NVIDIA AI Enterprise Connection
NVIDIA makes the GPUs (the chips). But they also make the software that runs ON those chips in business environments. It's called NVIDIA AI Enterprise, and it has three tiers:
```plain text

NVIDIA AI ENTERPRISE — THREE TIERS

  CLOUD TIER          FACTORY TIER         EDGE TIER
  ┌─────────┐         ┌─────────┐         ┌─────────────┐
  │ Runs on  │         │ Runs on  │         │ Runs on     │
  │ Amazon   │         │ your own │         │ ADC 3K POD  │  ← THIS IS US
  │ Google   │         │ AI       │         │ at customer │
  │ Azure    │         │ factory  │         │ site        │
  └─────────┘         └─────────┘         └─────────────┘

  NVIDIA sells the software.
  ADC sells the HARDWARE + MANAGEMENT that runs it.
  Together = turnkey edge AI for any industry.

```
If ADC gets NVIDIA AI Enterprise certified, every pod we ship comes pre-loaded with enterprise-grade AI software. The customer doesn't need to figure out how to install AI — it's ready to go. That certification is the single biggest unlock for edge sales.