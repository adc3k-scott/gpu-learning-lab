# Who Buys Edge AI — Customer Profiles
*Notion backup — 2026-04-06*

# Who Buys Edge AI — And Why They Pay Premium
Edge computing isn't for startups on a budget. It's for organizations with three things: sensitive data, real-time needs, and money. Here are the five customer segments that will buy ADC 3K pods as edge nodes.
---
## 1. Oil & Gas / Petrochemical
> Scott knows these people personally. 25 years in deepwater ROV operations. Same industry, new product.
### The Problem They Have
Every offshore platform, refinery, and pipeline corridor generates massive amounts of sensor data — pressure, flow rates, vibration, thermal imaging, subsea camera feeds. Right now, most of this data gets sent to Houston or the cloud for analysis. By the time the answer comes back, the anomaly that could have prevented a $50M blowout has already happened.
### What They Need
- Real-time predictive maintenance — catch equipment failure BEFORE it happens
- Autonomous inspection — AI analyzing camera feeds 24/7 without human fatigue
- Data sovereignty — proprietary drilling and production data stays on-site
- Works offshore and in remote locations — can't depend on fiber internet
### Why the Pod Fits
- Self-powered (nat gas generator) — no grid dependency
- Immersion cooled — works in Gulf Coast heat, desert, offshore platforms
- Container form factor — crane it onto a platform or pad site
- Managed from MARLIE I — 24/7 NOC monitoring, no on-site AI staff needed
### The Money
A single unplanned shutdown on an offshore platform costs $1-5M per day. A pod running predictive maintenance AI costs $50-80K/month managed. The ROI sells itself.
```plain text

    OFFSHORE PLATFORM — EDGE AI DEPLOYMENT

    ┌──────────────────────────────────────────┐
    │  PLATFORM DECK                            │
    │                                           │
    │   [Sensors] ──┐                           │
    │   [Cameras] ──┤                           │
    │   [Vibration]─┤    ┌─────────────────┐   │
    │   [Thermal] ──┼───→│  ADC 3K POD     │   │
    │   [Pressure]──┤    │  4 GPU racks    │   │
    │   [Flow] ────┘    │  Self-cooled     │   │
    │                    │  Self-powered    │   │
    │                    └────────┬────────┘   │
    │                             │             │
    │                    ┌────────▼────────┐   │
    │                    │ REAL-TIME ALERTS │   │
    │                    │ "Pump 3 bearing  │   │
    │                    │  failure in 72h" │   │
    │                    └─────────────────┘   │
    │                             │             │
    └─────────────────────────────┼─────────────┘
                                  │ VSAT uplink
                         ┌────────▼────────┐
                         │   MARLIE I NOC   │
                         │   Lafayette, LA  │
                         │  24/7 monitoring │
                         └─────────────────┘

```
---
## 2. Defense & Military
> Classified data cannot leave the building. Period. That's not a preference — it's the law.
### The Problem They Have
The Department of Defense needs AI for everything — drone surveillance analysis, logistics optimization, communications intelligence, predictive maintenance on vehicles and aircraft. But classified workloads cannot run on commercial cloud (AWS GovCloud has limits). They need on-base, air-gapped compute that they physically control.
### What They Need
- SCIF-compatible enclosure — physically secured, no wireless emissions
- Air-gapped operation — zero internet dependency for classified inference
- Rapid deployment — ship a pod to a forward operating base in weeks, not months
- Ruggedized — works in extreme heat, cold, dust, humidity
### Why the Pod Fits
- 20-foot ISO container = military standard shipping size (fits on trucks, ships, aircraft)
- Self-powered — diesel genset for forward bases with no grid
- No HVAC dependency — immersion cooling works in desert and arctic
- Managed or unmanaged — DoD can run it themselves or ADC manages remotely
### The Money
Defense contracts pay 3-5x commercial rates. A SCIF-rated edge AI pod could command $150-300K/month. Fort Polk, Barksdale AFB, NAS JRB New Orleans, and Camp Beauregard are all within 200 miles of Lafayette.
---
## 3. Healthcare Systems
> HIPAA says patient data must be protected. The easiest way to protect it? Never let it leave the hospital.
### The Problem They Have
AI is transforming medical imaging — radiology, pathology, dermatology. An AI can read an X-ray in 2 seconds with 95% accuracy. But hospitals are terrified of sending patient images to the cloud because of HIPAA liability. One breach = millions in fines. So most hospitals just... don't use AI yet.
### What They Need
- On-premises AI inference — patient images never leave the building
- Low latency — radiologist needs results during the exam, not after
- HIPAA-compliant infrastructure — encrypted, audited, physically secured
- Managed service — hospitals don't have GPU engineers on staff
### Why the Pod Fits
- Deploy in hospital parking structure or utility yard — 50 feet from the imaging center
- Fully managed from MARLIE I — hospital IT doesn't touch it
- NVIDIA AI Enterprise certified NIMs for medical imaging are ready today
- Self-powered backup — when the grid goes down during a hurricane, the AI stays up
### The Money
Hospital systems spend $2-5M/year on radiology outsourcing. A managed edge pod running AI-assisted imaging costs $40-60K/month. Ochsner Health (40+ facilities), Our Lady of Lourdes, LGMC — all within driving distance.
---
## 4. Manufacturing & Ports
> Quality inspection at the speed of the assembly line. Not tomorrow. Not in an hour. RIGHT NOW.
### The Problem They Have
Manufacturing plants run 24/7. Every product coming off the line needs quality inspection. Human inspectors miss things — they get tired, they blink, they take breaks. AI vision systems can inspect every single unit at full line speed. But the cloud adds 200ms of latency, which at high-speed production means missed units and wasted product.
### What They Need
- Real-time visual inspection — camera to decision in under 10ms
- Digital twin modeling — simulate production changes before implementing
- Logistics optimization — container routing, warehouse robotics
- On-site data — proprietary manufacturing processes stay proprietary
### Why the Pod Fits
- Container sits on the factory floor or adjacent lot — zero network latency
- Handles the heat and vibration of industrial environments
- Scales with production — add another pod when you add another line
- Port Fourchon, Port of New Orleans, I-10 industrial corridor — all ADC territory
### The Money
A single quality defect that reaches a customer costs 10-100x more than catching it on the line. Manufacturing AI inspection saves $1-10M/year per facility. Pod cost: $50-80K/month managed.
---
## 5. Sovereign AI — Foreign Governments & State Agencies
> Some countries legally CANNOT use American cloud providers. A pod is a turnkey sovereign AI node.
### The Problem They Have
Data sovereignty laws in the EU (GDPR), Middle East, Southeast Asia, and Latin America require that citizen data stays within national borders. Many governments want AI capabilities but cannot — by law — use AWS, Azure, or Google Cloud. They need physical hardware in their country, managed by a trusted partner.
### What They Need
- Physical hardware on sovereign soil — legally required
- Turnkey deployment — most countries don't have GPU infrastructure expertise
- Managed remotely — ADC provides the expertise, country provides the location
- Self-contained — many deployment sites have unreliable power and cooling
### Why the Pod Fits
- Ship a container anywhere in the world — standard ISO shipping
- Self-powered, self-cooled — works in any climate, any grid condition
- MARLIE I manages it remotely — sovereign nation gets AI without building expertise
- "Made in Lafayette, Louisiana" — American-built, American-managed, deployed globally
### The Money
Sovereign AI contracts are typically multi-year, government-funded, and premium-priced. A single sovereign deployment could be $3-5M/year. The Middle East and Southeast Asia are the hottest markets right now.
---
## Summary — The Edge Customer Matrix
```plain text

┌──────────────────┬───────────────┬──────────────┬──────────────────────────┐
│ CUSTOMER         │ WHY EDGE      │ POD/MONTH    │ ADC ADVANTAGE            │
├──────────────────┼───────────────┼──────────────┼──────────────────────────┤
│ Oil & Gas        │ Remote sites, │ $50-80K      │ Scott's 25yr network.    │
│                  │ real-time     │              │ Same industry, new tool. │
├──────────────────┼───────────────┼──────────────┼──────────────────────────┤
│ Defense          │ Classified    │ $150-300K    │ ISO container = mil-spec.│
│                  │ data, SCIF    │              │ 4 bases within 200 mi.   │
├──────────────────┼───────────────┼──────────────┼──────────────────────────┤
│ Healthcare       │ HIPAA, patient│ $40-60K      │ Ochsner, Lourdes,        │
│                  │ data on-prem  │              │ 40+ facilities nearby.   │
├──────────────────┼───────────────┼──────────────┼──────────────────────────┤
│ Manufacturing    │ Line-speed    │ $50-80K      │ I-10 corridor, ports,    │
│                  │ QA, zero lag  │              │ petrochemical plants.    │
├──────────────────┼───────────────┼──────────────┼──────────────────────────┤
│ Sovereign AI     │ Data must stay│ $250K+/mo    │ Ship globally, manage    │
│                  │ in-country    │              │ from Lafayette.          │
└──────────────────┴───────────────┴──────────────┴──────────────────────────┘

```