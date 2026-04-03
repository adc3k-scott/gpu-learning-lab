# Step 1: Baton Rouge Terminal -- Bootstrap Factory
*Notion backup — 2026-04-03*

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