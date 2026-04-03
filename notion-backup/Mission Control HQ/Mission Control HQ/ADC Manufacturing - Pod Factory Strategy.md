# ADC Manufacturing -- Pod Factory Strategy
*Notion backup — 2026-04-03*

# ADC Manufacturing -- Two-Step Strategy
Step 1: Bootstrap factory in existing building. Get pods built, get revenue flowing, learn what to automate. Step 2: Purpose-built automated factory with robots, solar roof, pipeline gas, and NVIDIA Omniverse digital twin. Step 1 funds Step 2.
---
## The Logic
```plain text
STEP 1: BATON ROUGE TERMINAL (LAFAYETTE)
  Lease existing building. Manual assembly. 6 stations.
  Output: 2-3 pods/month. Staff: 8-12.
  Timeline: 60-90 days to first pod.
  Revenue: $450K/month at capacity.
  PURPOSE: Cash flow + learn what to automate.

STEP 2: NEW IBERIA AUTOMATED FACTORY (14th & Hwy 90)
  Purpose-built. Robotic assembly. Solar roof. Pipeline gas.
  Output: 8-12 pods/month. Staff: 15-20.
  Timeline: 12-18 months to production.
  Revenue: $1.5M/month at capacity.
  PURPOSE: Scale + margins + the machine that builds the machine.

Step 1 revenue funds Step 2 construction.
Step 1 lessons optimize Step 2 automation.
Every pod built by hand teaches you what to automate.
```
---
## NVIDIA Technology Stack
```plain text
FACTORY DESIGN        Omniverse      Build the factory virtually first
ROBOT PROGRAMMING     Isaac Sim      Train arms in simulation
QUALITY INSPECTION    Metropolis     AI vision for automated QA
FACTORY OPERATIONS    AI Enterprise  Real-time optimization
POD HARDWARE          DGX / HGX      What goes inside every pod
```
> The factory that builds NVIDIA-powered pods is itself powered by NVIDIA technology. That's the story.
*[Child: Step 1: Baton Rouge Terminal -- Bootstrap Factory]*
# Step 1: Baton Rouge Terminal -- Bootstrap Factory
> Get pods built. Get revenue flowing. Learn what to automate. This is NOT the final factory -- it's the launchpad.
---
## Site: Baton Rouge Terminal, Lafayette
Existing industrial building. Lease, don't buy. The goal is speed -- pods shipping in 60-90 days, not 18 months waiting for a custom factory.
### Facility Requirements
  - 10,000-20,000 sq ft clear span (no interior columns)
  - Overhead crane -- 10-ton minimum for lifting containers and loaded racks
  - 3-phase power for welding, test benches, and UPS commissioning
  - Loading dock for flatbed truck access (pods ship on flatbeds)
  - Concrete floor rated for container weight (~40,000 lbs loaded)
  - Ventilation for welding and spray foam insulation
---
## Assembly Line -- 6 Stations
Containers flow left to right through 6 stations. Each station takes 2-3 days. Total build time per pod: 12-18 working days.
```plain text
ASSEMBLY FLOW -- BATON ROUGE TERMINAL

  STATION 1        STATION 2        STATION 3
  Container Prep   Insulation       Electrical
  ┌──────────┐     ┌──────────┐     ┌──────────┐
  │ Receive   │     │ Spray    │     │ Conduit  │
  │ Inspect   │ --> │ foam     │ --> │ Wire pull│
  │ Cut pens  │     │ walls +  │     │ PDUs     │
  │ Doors     │     │ ceiling  │     │ UPS      │
  └──────────┘     └──────────┘     └──────────┘
      2 days           2 days           3 days

  STATION 4        STATION 5        STATION 6
  Cooling          Compute          Test & QA
  ┌──────────┐     ┌──────────┐     ┌──────────┐
  │ Immersion │     │ Racks    │     │ Power on │
  │ tanks     │ --> │ Servers  │ --> │ Thermal  │
  │ CDU       │     │ Cables   │     │ Burn-in  │
  │ Dry cooler│     │ Network  │     │ Ship     │
  └──────────┘     └──────────┘     └──────────┘
      3 days           2 days           3 days

  TOTAL: 12-18 working days per pod
  OUTPUT: 2-3 pods/month with overlapping stations
```
---
## Staffing -- 8-12 People
  - 2 electricians (licensed) -- conduit, wire, terminations, UPS
  - 2 pipe fitters / mechanical -- immersion tanks, CDU plumbing, dry cooler
  - 2 electronics technicians -- server installation, networking, cable management
  - 1 insulation / finish contractor -- spray foam, sealing, penetration waterproofing
  - 1 QA / commissioning engineer -- test protocols, burn-in, documentation
  - 1 operations manager -- scheduling, inventory, shipping
  - 1-2 general assembly -- container prep, crane operation, material handling
---
## Economics
```plain text
STEP 1 ECONOMICS

Startup Costs:
  Lease deposit + first/last       $25-35K
  Station buildout (6 stations)    $100-150K
  Tooling (crane, welders, etc.)   $50-75K
  Initial inventory (1st 3 pods)   $200-300K
  Total startup:                   $375-560K

Monthly Operating:
  Lease                            $8-12K
  Payroll (8-12 people)            $60-90K
  Materials per pod                $40-60K
  Utilities + misc                 $5-8K

Revenue (at capacity, 3 pods/month):
  3 pods x $120-180K each =        $360-540K/month
  Less operating costs:             $195-290K/month
  Gross margin:                     $165-250K/month
```
---
## What Step 1 Teaches You
Every pod you build by hand reveals what to automate. Track these metrics:
  - Time per station -- which station is the bottleneck?
  - Error rate per station -- where do mistakes happen?
  - Rework frequency -- what gets done twice?
  - Material waste -- where are you cutting and throwing away?
  - Worker idle time -- where are people waiting for the previous station?
> This data becomes the blueprint for Step 2 automation. Every manual pain point is a robot opportunity.
---
> UPDATED 2026-03-23 -- POST-GTC REWRITE
### Updated Assembly Line (40-ft containers):
Station 1: Container Prep
  - Receive 40-ft HC ISO container
  - Cut penetrations (power, cooling, cable)
  - Install vapor barrier + insulation (spray foam)
  - Time: 2 days
Station 2: Electrical
  - Install Eaton Beam Rubin DSX (800V DC rectifier + bus)
  - Run 800V DC busway
  - Install rack PDUs (Eaton HDX G4)
  - Generator hookup panel (external)
  - Time: 2 days
Station 3: Cooling
  - Mount exterior dry cooler
  - Run supply/return piping (45C/55C glycol loop)
  - Install CDU connection manifolds for NVL72 rack ports
  - Pressure test
  - Time: 1.5 days
Station 4: Compute Install
  - Receive NVIDIA NVL72 rack (ships complete, liquid cooled)
  - Position on pod floor (forklift)
  - Connect 800V DC power feed
  - Connect liquid cooling manifolds
  - Connect network cables (InfiniBand if multi-rack, Ethernet + management)
  - Time: 1 day
Station 5: Fire + Safety
  - Install Novec 1230 suppression system
  - Install VESDA aspirating detection
  - Leak detection (TraceTek)
  - Environmental sensors (temp, humidity, pressure)
  - Time: 1 day
Station 6: Test + QA
  - Power on, POST, BIOS config
  - Cooling flow test (verify temps under load)
  - Network connectivity to Willow Glen NOC
  - GPU burn-in (24-hr stress test)
  - Mission Control registration (node appears on dashboard)
  - Time: 2 days
---
Total per pod: ~9.5 days
Monthly output: 2-3 pods (with 8-12 staff)
Startup cost: $375-560K (facility lease, tools, initial materials)
### Key Difference from Pre-GTC:
  - NO immersion cooling station -- NVIDIA racks are self-contained liquid cooled
  - NO custom CDU engineering -- just connect manifolds
  - 800V DC simplifies electrical (fewer conversions, less copper)
  - Assembly is simpler because NVIDIA did the hard part
*[Child: Step 2: New Iberia -- AI-Automated Pod Factory]*
# Step 2: New Iberia -- AI-Automated Pod Factory
> The machine that builds the machine. Fully automated, solar-powered, pipeline-fed, designed in Omniverse before a single wall goes up.
---
## Site: 14th Street & Highway 90, New Iberia
### Why This Location
  - Natural gas pipeline ON PROPERTY -- power the factory and test pods with the same fuel
  - Corner of 14th & Hwy 90 -- direct highway access for shipping containers in and pods out
  - Hwy 90 connects to I-10, Port of New Iberia, and the entire Gulf corridor
  - Large footprint -- room for assembly line, solar array, testing yard, expansion
  - Iberia Parish -- eligible for PILOT, Quality Jobs, Enterprise Zone incentives
---
## The Omniverse Digital Twin Workflow
Before spending a dollar on construction, the entire factory is designed and tested virtually in NVIDIA Omniverse. Here is exactly how that works:
### Phase 1: Virtual Design (Weeks 1-8)
Build the entire factory in Omniverse -- every wall, every robot arm, every conveyor belt, every electrical panel, every fire suppression head. Place them exactly where they'll go. The software is physically accurate -- if something doesn't fit in Omniverse, it won't fit in real life.
  - Architect delivers building shell design (steel frame, concrete, solar roof spec)
  - ADC engineering team places all 7 assembly stations inside the virtual building
  - Robot arms are modeled with real reach envelopes and payload limits
  - Material flow is mapped: container in loading dock to pod on flatbed
  - Solar roof layout optimized for maximum generation vs. structural load
### Phase 2: Simulate (Weeks 8-16)
Run the factory at full speed -- virtually. Process 100 pods through the digital assembly line. The simulation reveals every problem before you encounter it in real life.
  - Throughput test: how many pods/month at what robot speed?
  - Collision detection: do any robot paths intersect? Any pinch points?
  - Bottleneck identification: which station holds up the line?
  - Failure simulation: what happens when Robot Arm 3 goes down?
  - Energy simulation: does solar + gas produce enough for factory + pod testing?
### Phase 3: Build Physical Factory (Months 4-12)
The physical factory is a 1:1 copy of the digital model. Every measurement is pre-validated. Every robot position is pre-programmed. No surprises.
  - Steel frame + concrete pad construction
  - Solar roof installation (panels + inverters + battery storage)
  - Gas pipeline tap and distribution manifold
  - Robot arm installation in pre-validated positions
  - Conveyor and material handling systems
  - QA test cells with automated monitoring
### Phase 4: Live Digital Twin (Ongoing)
Once the physical factory is running, the digital twin stays alive. Every sensor in the real factory feeds the virtual model in real-time. The digital twin becomes the factory's brain.
  - Real-time production dashboard (accessible from MARLIE I NOC)
  - Predictive maintenance on every robot arm and motor
  - Production optimization -- AI adjusts station timing automatically
  - Remote monitoring -- Scott can watch the factory from his phone
---
## Automated Assembly Line -- 7 Stations
```plain text
AUTOMATED ASSEMBLY -- NEW IBERIA FACTORY

  [1] RECEIVING       Robotic crane unloads ISO containers from truck
                      Positions on assembly track automatically

  [2] CNC CUTTING     Automated plasma/laser cuts all penetrations
                      Pre-programmed from Omniverse model. Zero measuring.

  [3] INSULATION      Robotic spray foam application
                      Consistent thickness, no gaps, no human error

  [4] ELECTRICAL      Semi-automated wire pulling + robotic conduit bending
                      Human electrician for terminations and inspection

  [5] COOLING         Robotic tank placement + orbital pipe welding
                      Human for final connections and leak testing

  [6] COMPUTE         Robotic rack insertion and cable management
                      AI vision verifies every connection

  [7] TEST CELL       Automated power-on, thermal cycle, 24hr burn-in
                      AI monitors every parameter
                      Pod doesn't leave until 100% automated QA passes
```
---
## Power Architecture -- Factory Runs On What It Sells
```plain text
NEW IBERIA FACTORY POWER

  SOLAR ROOF          Primary daytime power for factory operations
  PIPELINE GAS        Baseload power + pod testing fuel
  BATTERY STORAGE     Overnight + peak shaving
  GRID (CLECO)        Emergency backup only

  The factory is its own showcase:
  'We power our factory the same way we power your pod.'
```
---
## Staffing -- 15-20 People
  - 3-4 robot operators / programmers
  - 2 electricians (final termination, code inspection)
  - 2 mechanical / pipe fitters (final connections, leak testing)
  - 2 QA engineers (automated test oversight, documentation)
  - 2 logistics (shipping, receiving, inventory management)
  - 1 plant manager
  - 2-3 maintenance technicians (robots, conveyors, facility)
  - 1 Omniverse / digital twin engineer
---
## Economics
```plain text
STEP 2 ECONOMICS

Capital Investment:
  Land + construction             $3-5M
  Robot arms + tooling            $1.5-2M
  Solar roof + battery            $500K-800K
  Gas pipeline connection          $100-200K
  Omniverse design + simulation   $150-250K
  Total:                           $5.25-8.25M

Monthly Operating:
  Payroll (15-20 people)           $100-140K
  Materials per pod                $35-50K (bulk pricing)
  Energy (solar offsets 40%)       $8-12K
  Maintenance + misc              $10-15K
  Total operating:                $153-217K/month

Revenue (at capacity, 10 pods/month):
  10 pods x $150K avg =            $1,500,000/month
  Less operating:                  $217K/month
  Less material (10 pods):         $500K/month
  GROSS MARGIN:                    $783K/month
  ANNUAL GROSS PROFIT:             $9.4M/year
```
> Step 1 revenue ($165-250K/month gross margin) accumulates during the 12-18 month Step 2 build period. That's $2-4.5M toward the $5-8M capital investment before the automated factory even opens.
---
## Timeline
```plain text
MONTH 1-3:     Step 1 running. First pods shipping.
MONTH 3-6:     Omniverse design of Step 2 factory begins.
MONTH 6-8:     Simulation testing. Site acquisition in New Iberia.
MONTH 8-10:    Construction begins. Permits, foundation, steel.
MONTH 10-14:   Building enclosed. Robot installation.
MONTH 14-16:   Commissioning. Digital twin goes live.
MONTH 16-18:   First automated pod off the line.
MONTH 18+:     Ramp to 8-12 pods/month. Step 1 becomes
               overflow / custom / defense-spec facility.
```
> Step 1 doesn't shut down when Step 2 opens. It becomes the custom shop -- defense-spec pods, SCIF modifications, specialty builds that don't fit the automated line. Two revenue streams.
---
> UPDATED 2026-03-23 -- POST-GTC REWRITE
### Updated for 40-ft Pods + 800V DC:
Same Omniverse-first design philosophy. Same 7-station automated line. Updated specs:
  - Containers: 40-ft HC ISO (not 20-ft)
  - Power system per pod: Eaton Beam Rubin DSX (800V DC)
  - Cooling: Integrated dry cooler (no immersion tanks)
  - Compute: NVIDIA NVL72 racks (arrive complete, forklift into position)
  - QA: NVIDIA Metropolis AI vision inspection still applies
### Automation Advantage:
The shift from immersion to NVIDIA liquid-cooled racks actually SIMPLIFIES automation:
  - No fluid filling station
  - No immersion tank fabrication
  - No custom CDU builds
  - Rack install is forklift + connect 3 things (power, cooling, network)
  - Robot arms handle repetitive tasks (insulation, cable routing, sensor placement)
  - Metropolis inspects welds, connections, sensor placement
---
Capital: $5.25-8.25M (unchanged)
Revenue at capacity: $1.5M/month (unchanged)
Timeline: 12-18 months after Step 1 proves demand
### Site: 14th & Hwy 90, New Iberia
  - Pipeline natural gas on property
  - Solar roof
  - Near First Solar factory (panel supply)
  - Near Louisiana Cat (generator supply)
---
When Step 2 opens, Step 1 (Baton Rouge) becomes the custom/defense spec shop for non-standard builds.
*[Child: NVIDIA Omniverse -- Factory Design Guide]*
# NVIDIA Omniverse -- Factory Design Guide
This page explains Omniverse in plain English so anyone on the team can understand what it does, why we use it, and how it saves us millions.
---
## What Is Omniverse?
Imagine you could build an entire factory inside a video game -- but it's not a game. Every wall, every pipe, every robot arm is physically accurate. If you drop a wrench in Omniverse, it falls at the right speed and bounces the right way. If a robot arm swings left, it shows you exactly what it would hit.
That's Omniverse. It's NVIDIA's platform for building digital twins -- perfect virtual copies of real-world things. Factories, warehouses, cities, robots, cars. If it exists in the physical world, you can build a digital copy in Omniverse and test it before spending a dollar on the real thing.
> Think of it like a flight simulator for factories. Pilots don't learn to fly in a real plane first -- they learn in a simulator where crashing costs nothing. We don't build a $5M factory first -- we build it in Omniverse where mistakes cost nothing.
---
## What We Use It For
### 1. Factory Layout
Before pouring concrete, we place every machine, every wall, every doorway in the virtual factory. We walk through it. We drive a forklift through it. We find out that Station 4 is too close to the wall BEFORE we build the wall.
### 2. Robot Programming
Every robot arm in the factory gets programmed in simulation first. We teach it to pick up a server rack, move it into the container, and set it down -- all virtually. When we install the real robot, we upload the program and it works on day one. No weeks of on-site programming.
### 3. Production Testing
We run 1,000 pods through the virtual factory in a single afternoon. We find out that Station 3 takes 20 minutes longer than Station 2, creating a bottleneck. We fix it in the design -- add a second Station 3, rearrange the flow, or speed up the process. All before construction starts.
### 4. Live Monitoring
After the real factory is built, every sensor feeds data into the digital twin. If a motor is running hot, the digital twin shows it glowing red before it fails. If production is slowing down, the twin shows exactly where and why. Scott can watch the whole factory from his phone.
---
## What This Saves Us
```plain text
WITHOUT OMNIVERSE (Traditional Factory Build):
  Design errors found during construction     $200-500K in rework
  Robot programming on-site                   6-8 weeks of downtime
  Bottleneck discovery after opening           3-6 months of lost output
  Unplanned equipment failure                  $50-100K per incident
  TOTAL WASTE: $500K-1.5M in first 2 years

WITH OMNIVERSE:
  Design errors found in simulation            $0 to fix
  Robot programming in simulation              0 weeks of downtime
  Bottleneck discovery before construction     0 months of lost output
  Predictive maintenance via digital twin      Near-zero unplanned failure
  TOTAL WASTE: Near zero

  Omniverse license + design time: ~$150-250K
  Savings in first 2 years: $500K-1.5M
  ROI: 3-6x return
```
---
## NVIDIA Isaac Sim -- The Robot Trainer
Isaac Sim is the part of Omniverse specifically for robots. Here's what it does in plain language:
Instead of buying a $200,000 robot arm and spending 6 weeks teaching it to pick up a server rack in the real world (where it might crash into things, drop expensive equipment, or hurt someone), you teach it in Isaac Sim first. The virtual robot practices 10,000 times in one night. When you put the program into the real robot, it already knows exactly what to do.
  - Train in simulation: robot practices millions of movements overnight
  - Transfer to real hardware: upload program, robot works on day one
  - Update remotely: change the program in simulation, push to factory floor
  - Test edge cases: what if the container is 2 inches off-center? Sim handles it
---
## NVIDIA Metropolis -- The Quality Inspector
Metropolis is NVIDIA's AI vision platform. In our factory, it does one critical job: making sure every pod is built correctly before it ships.
Cameras at each station feed images to an AI that's been trained on thousands of correct assemblies. If a cable is in the wrong port, a screw is missing, or a tank isn't seated properly -- the AI flags it instantly. No human inspector can match this speed or consistency.
  - Camera at every station: automatic visual inspection
  - AI trained on correct vs incorrect assembly: catches defects humans miss
  - Real-time alerts: stops the line if critical defect detected
  - Documentation: every pod gets a photographic build record
---
> UPDATED 2026-03-23 -- POST-GTC REWRITE
## Pod Factory Strategy -- Updated
### Key Changes Post-GTC:
- Pods are now 40-ft High Cube ISO containers (NOT 20-ft)
- NVIDIA ships complete liquid-cooled NVL72 racks -- no custom immersion engineering
- EC-110 immersion cooling DEPRIORITIZED
- 800V DC native power via Eaton Beam Rubin DSX in every pod
- Multi-vendor chip support (NVIDIA primary, Terafab/AMD ready)
- Each pod is a self-contained AI factory node: compute + cooling + power + network
### Two-Step Strategy (unchanged concept, updated specs):
- Step 1: Baton Rouge Terminal -- manual assembly, 40-ft containers, 2-3 pods/month
- Step 2: New Iberia -- Omniverse-designed automated factory, 8-12 pods/month
### What Goes In Each 40-ft Pod:
- 10 NVIDIA NVL72 racks per pod (8 compute + 1 network + 1 storage) — 576 GPUs (C1 SuperPOD), 1.3 MW IT load, 800V DC native
- Eaton Beam Rubin DSX (800V DC rectifier + busway + PDU)
- Integrated dry cooler (exterior mount, self-contained cooling)
- Portable natural gas generator hookup OR grid tie
- Optional: First Solar rooftop panels, LFP battery
- Network: Starlink or fiber backhaul to Willow Glen NOC
- Fire suppression: Novec 1230 + VESDA
- Total power per pod: 130-260 kW IT + ~30 kW overhead