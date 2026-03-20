# BATON ROUGE TERMINAL — ENGINEERING SPECIFICATION

**Project:** ADC Manufacturing — Step 1 (Bootstrap Factory)
**Location:** Lafayette, LA (Baton Rouge Corridor — lease TBD)
**Owner:** Advantage Design & Construction (ADC)
**Document:** Terminal Engineering Specification v2.0 (DSX PIVOT)
**Date:** 2026-03-20 (Updated from v1.0 2026-03-11)

---

## DSX PIVOT (March 2026)

**This spec has been updated post-GTC 2026.** The pod product pivoted from immersion-cooled GPU pods to **DSX-compliant facility modules** — manufactured enclosures that receive NVIDIA's standard liquid-cooled racks.

### What Changed
- **No more immersion cooling.** EC-110 eliminated. No dielectric fluid, no immersion tanks, no GPU sled insertion.
- **Facility water loop replaces immersion.** Modules include plumbed water supply/return for NVIDIA's rack-level 45°C liquid cooling.
- **800 VDC power distribution** designed into every module. Cannot be retrofitted.
- **Rack receiving bays** replace compute install. NVIDIA ships complete racks — ADC builds the enclosure they go into.
- **Test scope changes.** Validate infrastructure (power, water, network) — not GPU burn-in. NVIDIA validates their own racks.
- **Consumables drop ~$6K/pod.** No EC-110 coolant. Add water loop components (~$3K).

### What Didn't Change
- 6-station linear flow (same layout)
- Container-based modular form factor
- Manual bootstrap → automated factory pipeline
- Two-step strategy (Baton Rouge → New Iberia)
- Electrical is still the bottleneck station

---

## 1. PURPOSE

The Baton Rouge Terminal is ADC's first pod assembly facility. It leases an existing industrial building, installs 6 manual assembly stations, and begins producing pods within 60-90 days. The goals are:

1. **Cash flow** — Revenue from day one while the New Iberia automated factory is designed and built
2. **Process validation** — Learn the real assembly sequence, identify bottlenecks, time every step
3. **Workforce development** — Train the team that will operate and supervise the automated line
4. **Customer demos** — Give customers a place to see a pod being built

**This facility does NOT close when New Iberia opens.** It becomes the custom shop — defense-spec, SCIF-rated, specialty builds, and short-run production. Two revenue streams.

---

## 2. BUILDING REQUIREMENTS

### Must-Have
| Requirement | Minimum | Ideal | Notes |
|-------------|---------|-------|-------|
| Floor space | 10,000 SF | 15,000-20,000 SF | Clear span, no columns in work area |
| Clear height | 20 ft | 24-28 ft | Must fit overhead crane + container on jig |
| Overhead crane | None (install our own) | Existing 5-10 ton | Saves $80-120K and 4 weeks if existing |
| Loading dock | 1 truck bay | 2 bays (1 receive, 1 ship) | Must accept flatbed with 20ft container |
| Drive-in door | 1 minimum | 2 | 12ft W × 14ft H minimum for container entry |
| Power | 200A 3-phase 480V | 400A 3-phase 480V | Welding + tools + test cell need 3-phase |
| Floor | Concrete slab | 6"+ reinforced | Must support 10,000 lb point loads |
| Parking | 15 spaces | 20+ | Staff + visitors |
| Zoning | Industrial (M-1 or M-2) | — | Manufacturing use required |

### Nice-to-Have
| Feature | Benefit |
|---------|---------|
| Existing compressed air | Saves $5K install |
| Office space built out | 200-400 SF for ops manager + QA desk |
| Restrooms | Required — cheaper if existing |
| Fenced yard | Outdoor container staging (4-6 units) |
| I-10 / I-49 access | Shipping route efficiency |
| Natural gas service | Future: test cell genset fuel |

### Disqualifiers
- No residential zoning or mixed-use
- No flood zone (unless elevated pad)
- No environmental liens or contamination
- Ceiling height below 20 ft
- No 3-phase power available

---

## 3. TARGET LEASE TERMS

| Item | Target |
|------|--------|
| Lease type | Industrial gross or NNN |
| Term | 2-3 years initial, 2 renewal options |
| Size | 12,000-18,000 SF |
| Rate | $4-7/SF/yr (Lafayette industrial market) |
| Monthly rent | $4,000-10,500 |
| TI allowance | Request $5-10/SF for crane + electrical |
| Move-in | 30 days from signing |
| Improvements | Landlord: roof/structure. Tenant: crane, electrical, stations. |

---

## 4. PRODUCTION LAYOUT

### 6-Station Linear Flow

```
    RECEIVING                                                    SHIPPING
    DOCK                                                         DOCK
     ┌──────────────────────────────────────────────────────────────┐
     │                                                              │
     │  ┌──────────┐  ┌──────────┐  ┌──────────┐                   │
     │  │ S1       │  │ S2       │  │ S3       │                   │
     │  │ CONTAINER│→ │ INSUL-   │→ │ ELEC-    │                   │
     │  │ PREP     │  │ ATION    │  │ TRICAL   │                   │
     │  │          │  │          │  │          │                   │
     │  └──────────┘  └──────────┘  └──────────┘                   │
     │       ↓ (crane moves container between stations)             │
     │  ┌──────────┐  ┌──────────┐  ┌──────────┐                   │
     │  │ S4       │  │ S5       │  │ S6       │                   │
     │  │ COOLING  │→ │ COMPUTE  │→ │ TEST     │                   │
     │  │ SYSTEM   │  │ INSTALL  │  │ & QA     │                   │
     │  │          │  │          │  │          │                   │
     │  └──────────┘  └──────────┘  └──────────┘                   │
     │                                                              │
     │  ┌─────────────────┐  ┌──────────┐  ┌───────────────┐       │
     │  │ MATERIAL        │  │ TOOL     │  │ OFFICE / QA   │       │
     │  │ STORAGE         │  │ CRIB     │  │ DESK          │       │
     │  └─────────────────┘  └──────────┘  └───────────────┘       │
     │                                                              │
     └──────────────────────────────────────────────────────────────┘
              FENCED YARD — CONTAINER STAGING (4-6 UNITS)
```

### Station Dimensions
Each station needs approximately 20ft × 12ft clear space (container footprint + 4ft working clearance on each side). Total production floor: ~3,600 SF for 6 stations + aisle.

---

## 5. STATION SPECIFICATIONS

### Station 1 — Container Prep
**Purpose:** Receive container, inspect, clean, mark and cut all penetration ports.

| Item | Detail |
|------|--------|
| Process | Inspect container (damage, corrosion). Chalk-mark all cut locations from template. Plasma-cut ports (power, coolant, network, access doors). Deburr all edges. |
| Equipment | Hypertherm Powermax 105 hand plasma cutter, angle grinder, deburring tools |
| Crane use | Lift container from truck to Station 1 jig position |
| Staff | 2 people (1 cutter + 1 helper/inspector) |
| Time | 6-8 hours |

### Station 2 — Insulation
**Purpose:** Interior insulation and vapor barrier.

| Item | Detail |
|------|--------|
| Process | Spray closed-cell foam (3" depth, R-21) on all interior surfaces. Allow 1-hour cure. Apply vapor barrier membrane over foam, heat-seal all seams. |
| Equipment | Graco Reactor 2 E-10 proportioner (smaller unit than factory), spray gun, PPE (respirator, suit) |
| Ventilation | CRITICAL — spray foam requires exhaust fan during application. Confirm building ventilation. |
| Staff | 2 people (1 sprayer + 1 barrier installer) |
| Time | 4-6 hours (includes cure) |

### Station 3 — Electrical + 800 VDC (BOTTLENECK)
**Purpose:** Main panel, 800 VDC power distribution, sub-panels, PDUs, bus bars, all wire runs.

| Item | Detail |
|------|--------|
| Process | Mount main 400A panel and 800 VDC distribution. Run conduit and wire per module wiring diagram. Install 800 VDC bus bars, rack PDUs, and NVIDIA rack power connections. Terminate all connections. Megger test all circuits. |
| Equipment | Standard electrician hand tools, wire pulling equipment, Megger insulation tester, torque wrenches, DC-rated tools and PPE |
| Staff | 2 licensed electricians |
| Time | 10-14 hours (BOTTLENECK — most labor-intensive station, 800 VDC adds complexity) |
| NEC compliance | All work to NEC 2023. 800 VDC per Article 712 (Direct-Current Microgrids). Inspector sign-off on each module. |
| Safety | 800 VDC requires arc flash analysis, DC-rated PPE, lockout/tagout procedures specific to DC systems. |

### Station 4 — Facility Water Loop
**Purpose:** Plumb facility water supply/return for NVIDIA rack-level liquid cooling. CDU connections. Heat rejection interface.

| Item | Detail |
|------|--------|
| Process | Position CDU (Coolant Distribution Unit) connection points. Pipe all water supply/return lines (45°C hot water from NVIDIA racks). Thread and fit all connections. Install isolation valves, flow meters, temperature sensors. Pressure test (45 PSI, 30 min). Flush and fill with treated water. |
| Equipment | Pipe threader, pipe wrenches, pressure test gauge, water treatment chemicals, flow meter test equipment |
| Staff | 2 pipe fitters |
| Time | 6-8 hours |
| Notes | Simpler than old immersion station — no EC-110 coolant, no immersion tanks. Standard facility water plumbing. Water exits module to external heat rejection (cooling tower / dry cooler, customer-supplied or ADC-supplied). |

### Station 5 — Rack Receiving Bay + Network
**Purpose:** Prepare rack receiving positions, network infrastructure, and cable management for NVIDIA liquid-cooled racks.

| Item | Detail |
|------|--------|
| Process | Install rack mounting positions on vibration-damped floor mounts. Pre-route 800 VDC power cables to each rack position. Pre-route water supply/return to each rack CDU connection point. Route and terminate all network cables (InfiniBand or 400GbE — customer spec). Install cable management (overhead trays, vertical managers). Label all connections. |
| Equipment | Cable management tools, crimping tools, cable tester, laser level for rack alignment |
| Staff | 2 electronics technicians |
| Time | 6-8 hours |
| Notes | ADC does NOT install NVIDIA racks — they arrive pre-assembled with integrated liquid cooling and drop in. This station prepares the infrastructure the racks connect to. NVIDIA's 2-hour rack install happens at the customer site, not in our factory. |

### Station 6 — Test & QA
**Purpose:** Full infrastructure validation — power, water, network. Module-level QA (not GPU burn-in — NVIDIA validates their own racks).

| Item | Detail |
|------|--------|
| Process | Connect module to facility power + water + network. Power-on self-test (800 VDC energize, all circuits). Water loop flow test (pressure, flow rate, leak check under pressure). Network throughput test (all ports). Thermal test (run water at 45°C for 2 hours, verify no leaks under thermal expansion). Visual inspection of all connections. QA checklist + sign-off. Generate infrastructure test certificate. |
| Equipment | Facility power connection (100A 480V + 800 VDC test supply), water loop test rig (pump + heater), network test equipment, thermal camera (FLIR handheld), multimeter, laptop for monitoring |
| Staff | 1 QA technician + 1 electronics tech |
| Time | 4-6 hours (shorter — no 4hr GPU burn-in) |
| Notes | Test validates that the MODULE infrastructure works. GPU/rack validation is NVIDIA's responsibility after rack installation at customer site. |

---

## 6. CYCLE TIME ANALYSIS (DSX MODULE)

| Station | Process | Time | Crew |
|---------|---------|------|------|
| S1 | Container Prep | 6-8 hr | 2 |
| S2 | Insulation | 4-6 hr | 2 |
| S3 | Electrical + 800 VDC | 10-14 hr | 2 |
| S4 | Facility Water Loop | 6-8 hr | 2 |
| S5 | Rack Receiving Bay + Network | 6-8 hr | 2 |
| S6 | Infrastructure Test & QA | 4-6 hr | 2 |
| **Total** | **End-to-end** | **36-50 hr** | **—** |

**Improvement vs old spec:** 8-12 hours faster per module. No immersion tank install, no EC-110 fill, no GPU burn-in. Water loop is simpler than immersion. Rack bay prep is simpler than GPU sled insertion. Test is shorter without 4hr burn-in.

**Throughput calculation:**
- Working hours: 10 hr/day × 4 days/week = 40 hr/week
- Bottleneck: Station 3 (Electrical + 800 VDC) at 10-14 hours
- With 2 modules in pipeline: 1 module completes every 4-6 working days
- Monthly output: **3-4 modules/month** (up from 2-3)

**Bottleneck mitigation (future):**
- Pre-fabricate wire harnesses off-line (parallel work during other station ops)
- Pre-fabricate 800 VDC bus bar assemblies
- Add 3rd electrician during S3 to overlap tasks
- Template conduit runs for repeated module configs (cut learning curve)

---

## 7. EQUIPMENT LIST

### Major Equipment

| Qty | Item | Est. Cost | Notes |
|-----|------|-----------|-------|
| 1 | Overhead crane (5-ton) | $45,000 | Or $80-120K for 10-ton. Check if existing. |
| 1 | Hypertherm Powermax 105 | $4,500 | Hand plasma cutter for S1 |
| 1 | Graco Reactor 2 E-10 | $18,000 | Spray foam proportioner for S2 |
| 2 | Pipe threader (Ridgid 300) | $3,200 | S4 pipe fitting |
| 1 | Megger MIT525 | $3,800 | Insulation tester for S3 |
| 1 | FLIR E86 thermal camera | $8,500 | S6 QA inspection |
| 1 | Cable tester (Fluke DTX) | $4,200 | S5/S6 network validation |
| 1 | Server lift (ServerLIFT SL-500X) | $6,500 | S5 rack placement |
| 2 | Forklift (used, electric) | $12,000 | Material handling |
| 6 | Assembly jig (custom welded) | $18,000 | Container positioning at each station |
| 1 | Exhaust fan system | $3,500 | S2 ventilation during spray foam |
| 1 | Compressed air (if not existing) | $5,000 | 60-gallon, 175 PSI |
| 1 | Welding machine (Miller 350P) | $4,800 | Fabrication + jig welding |
| — | Hand tools (6 stations) | $15,000 | Wrenches, crimpers, drills, etc. |
| — | Safety equipment | $5,000 | PPE, fire extinguishers, first aid, eye wash |
| — | IT setup (office + QA station) | $8,000 | Laptops, monitors, network switch, printer |
| | | **Total: ~$165,000** | |

### Consumables (Per Module — DSX Updated)

| Item | Est. Cost/Module |
|------|-----------------|
| Shipping container (20ft, used, one-trip) | $3,000-4,000 |
| Spray foam (closed cell, 3" × ~900 SF) | $2,500 |
| Vapor barrier membrane | $400 |
| Electrical (panels, 800 VDC distribution, wire, conduit, PDUs, bus bars) | $10,000-15,000 |
| Facility water loop (pipe, fittings, valves, CDU connections, sensors) | $3,000-4,500 |
| Network cable + connectors (InfiniBand or 400GbE) | $2,000-3,500 |
| Rack mounting hardware (damped mounts, rails, cable management) | $1,500-2,500 |
| Misc (fasteners, sealant, labels, hardware) | $1,000 |
| **Total materials per module** | **$23,400-33,400** |

**vs old spec:** EC-110 coolant ($4-6K) eliminated. 800 VDC distribution adds ~$2-3K to electrical. Water loop components ~$3-4.5K (simpler than immersion). Net cost roughly neutral, but the module is simpler to build and test.

NVIDIA liquid-cooled racks are NOT installed at the factory — they ship directly to the customer site and drop into the prepared module. NVIDIA's 2-hour rack install happens on-site.

---

## 8. STAFFING

| Role | Count | Type | Hourly Rate | Notes |
|------|-------|------|------------|-------|
| Operations Manager | 1 | Salary | $75K/yr | Scheduling, inventory, customer interface |
| Licensed Electrician | 2 | Hourly | $35-45/hr | S3 + oversight. Must hold LA license. |
| Pipe Fitter | 2 | Hourly | $30-38/hr | S4 cooling system |
| Electronics Technician | 2 | Hourly | $28-35/hr | S5 compute + S6 QA |
| General Assembly / Helper | 2-3 | Hourly | $18-24/hr | S1 prep, S2 insulation, material handling |
| QA Technician | 1 | Hourly | $30-38/hr | S6 test + sign-off + documentation |
| **Total** | **10-11** | | | |

### Shift Schedule
- **1 shift × 10 hours** (7:00–17:00)
- **Monday through Thursday** (4 × 10)
- Friday available for maintenance, cleanup, and overtime

### Hiring Pipeline
- Licensed electricians: Lafayette area has strong industrial workforce (oil & gas). Post with Louisiana Workforce Commission + local trade unions.
- Pipe fitters: Same pool. Oil & gas downcycle means available talent.
- Electronics techs: ITI (Industrial Training Institute) graduates, SOWELA, or military veterans.

---

## 9. ECONOMICS

| Item | Value |
|------|-------|
| **Startup Costs** | |
| Lease deposit + first/last | $12,000-20,000 |
| Equipment (Section 7) | $165,000 |
| Tenant improvements (electrical, crane, ventilation) | $50,000-80,000 |
| Initial material inventory (3 pods) | $75,000-95,000 |
| Working capital (2 months payroll) | $80,000 |
| **Total Startup** | **$382,000-440,000** |
| | |
| **Monthly Operating** | |
| Rent | $4,000-10,500 |
| Payroll (10-11 people) | $55,000-70,000 |
| Materials (2-3 pods) | $45,000-95,000 |
| Utilities | $2,000-3,500 |
| Insurance | $2,500 |
| Misc (maintenance, supplies) | $2,000 |
| **Total Monthly OpEx** | **$110,500-183,500** |
| | |
| **Monthly Revenue** | |
| 3 modules × $180K (conservative) | $540,000 |
| 4 modules × $180K (capacity) | $720,000 |
| **Monthly Gross Profit** | **$356,500-609,500** |
| | |
| **Payback** | **1 month at capacity** |

### Key Economic Points
- Under $500K startup — financeable with equipment loan or SBA
- Profitable from Module #1 at $180K selling price
- DSX modules are faster to build than old immersion pods (36-50 hrs vs 44-58 hrs)
- Higher monthly output (3-4 vs 2-3) = faster cash flow for New Iberia
- Cash flow funds New Iberia factory construction
- Becomes specialty shop (higher margins) once New Iberia opens

---

## 10. TIMELINE TO FIRST POD

| Week | Activity |
|------|----------|
| 1-2 | Building search + tour (broker). Lease negotiation. |
| 3 | Lease signed. Equipment orders placed. |
| 4-5 | Tenant improvements: electrical upgrade, ventilation, crane install |
| 6-7 | Equipment delivery. Station setup. Jig fabrication. |
| 8 | Staff hiring complete. Safety training. Dry run (no material). |
| 9-10 | **First pod build** — full assembly, all 6 stations. |
| 11 | First pod test + QA. Punch list. Process refinements. |
| 12 | **Second pod ships. Production rhythm established.** |

**60-90 days from lease signing to first pod shipped.**

---

## 11. WHAT THIS FACILITY TEACHES US

Every pod built here generates data that directly feeds the New Iberia factory design:

| Observation | Feeds Into |
|-------------|-----------|
| Actual time per station | Robot cycle time targets |
| Bottleneck analysis (S3 electrical) | Cobot task allocation |
| Wiring patterns that repeat | Pre-fabricated harness design |
| Common cutting templates | CNC program library |
| Spray foam coverage technique | ABB IRB 5500 spray path |
| Failure modes in test cell | Metropolis AI training data |
| Material waste measurements | Omniverse BOM optimization |
| Worker ergonomic issues | Robot reach envelope design |

**The bootstrap factory is the training data for the automated one.**

---

## 12. TRANSITION TO CUSTOM SHOP

When New Iberia opens and takes over standard production, Baton Rouge Terminal transitions:

| Standard Production | Custom Shop |
|--------------------|------------|
| 2-3 standard pods/month | 1-2 specialty pods/month |
| Fixed configuration | Customer-specified |
| $180K each | $250-400K each |
| Commodity | Premium margin |

### Custom Shop Products
- **Defense-spec modules** — TEMPEST shielding, SCIF-rated, hardened connectors, anti-tamper
- **Mobile deployment** — rapid-deploy modules for disaster response, military forward operating
- **Edge/remote modules** — wetland-rated (pilings), offshore-rated (barge/rig), extreme environment hardening
- **R&D / prototype** — new water loop configs, new rack layouts, experimental form factors
- **Retrofit / upgrade** — field-returned modules for water loop upgrade or power distribution refresh

---

*ADC — Advantage Design & Construction*
*Mission Control — Document updated 2026-03-20 (DSX Pivot)*
