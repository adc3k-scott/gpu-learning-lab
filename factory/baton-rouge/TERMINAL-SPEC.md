# BATON ROUGE TERMINAL — ENGINEERING SPECIFICATION

**Project:** ADC Manufacturing — Step 1 (Bootstrap Factory)
**Location:** Lafayette, LA (Baton Rouge Corridor — lease TBD)
**Owner:** Advantage Design & Construction (ADC)
**Document:** Terminal Engineering Specification v1.0
**Date:** 2026-03-11

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

### Station 3 — Electrical (BOTTLENECK)
**Purpose:** Main panel, sub-panels, PDUs, bus bars, all wire runs.

| Item | Detail |
|------|--------|
| Process | Mount main 400A panel and sub-panels. Run conduit and wire per pod wiring diagram. Terminate all connections. Install bus bars and PDUs. Megger test all circuits. |
| Equipment | Standard electrician hand tools, wire pulling equipment, Megger insulation tester, torque wrenches |
| Staff | 2 licensed electricians |
| Time | 10-14 hours (BOTTLENECK — most labor-intensive station) |
| NEC compliance | All work to NEC 2023. Inspector sign-off on each pod. |

### Station 4 — Cooling System
**Purpose:** Immersion tanks, plumbing, coolant fill.

| Item | Detail |
|------|--------|
| Process | Position immersion cooling tanks on mounts. Pipe all coolant supply/return lines. Thread and fit all connections. Pressure test (45 PSI, 30 min). Fill with EC-110 coolant. |
| Equipment | Pipe threader, pipe wrenches, pressure test gauge, EC-110 drum + pump |
| Staff | 2 pipe fitters |
| Time | 8-10 hours |

### Station 5 — Compute Install
**Purpose:** GPU server racks, networking, cabling.

| Item | Detail |
|------|--------|
| Process | Position server racks on vibration-damped mounts. Insert GPU sleds into immersion tanks. Route and terminate all network cables (100GbE spine, 25GbE leaf). Route and terminate power cables. Verify all connectors seated. |
| Equipment | Server lift, cable management tools, crimping tools, cable tester |
| Staff | 2 electronics technicians |
| Time | 8-10 hours |

### Station 6 — Test & QA
**Purpose:** Full system validation, burn-in, and sign-off.

| Item | Detail |
|------|--------|
| Process | Connect pod to facility power + network. Power-on self-test. Network throughput test. Thermal ramp to 100% GPU load. 4-hour burn-in at full TDP. Cooldown + visual inspection. QA checklist + sign-off. Generate test certificate. |
| Equipment | Facility power connection (100A 480V), network test equipment, thermal camera (FLIR handheld), multimeter, laptop for monitoring |
| Staff | 1 QA technician + 1 electronics tech |
| Time | 8-10 hours (includes 4hr burn-in) |

---

## 6. CYCLE TIME ANALYSIS

| Station | Process | Time | Crew |
|---------|---------|------|------|
| S1 | Container Prep | 6-8 hr | 2 |
| S2 | Insulation | 4-6 hr | 2 |
| S3 | Electrical | 10-14 hr | 2 |
| S4 | Cooling | 8-10 hr | 2 |
| S5 | Compute | 8-10 hr | 2 |
| S6 | Test & QA | 8-10 hr | 2 |
| **Total** | **End-to-end** | **44-58 hr** | **—** |

**Throughput calculation:**
- Working hours: 10 hr/day × 4 days/week = 40 hr/week
- Bottleneck: Station 3 (Electrical) at 10-14 hours
- With 2 pods in pipeline: 1 pod completes every 5-7 working days
- Monthly output: **2-3 pods/month**

**Bottleneck mitigation (future):**
- Pre-fabricate wire harnesses off-line (parallel work during other station ops)
- Add 3rd electrician during S3 to overlap tasks
- Template conduit runs for repeated pod configs (cut learning curve)

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

### Consumables (Per Pod)

| Item | Est. Cost/Pod |
|------|---------------|
| Shipping container (20ft, used, one-trip) | $3,000-4,000 |
| Spray foam (closed cell, 3" × ~900 SF) | $2,500 |
| Vapor barrier membrane | $400 |
| Electrical (panels, wire, conduit, PDUs, bus bars) | $8,000-12,000 |
| Plumbing (pipe, fittings, valves) | $2,000-3,000 |
| EC-110 coolant | $4,000-6,000 |
| Network cable + connectors | $1,500-2,500 |
| Misc (fasteners, sealant, labels, hardware) | $1,000 |
| **Total materials per pod** | **$22,400-31,900** |

GPU hardware and server racks are customer-supplied or purchased separately per order — not included in pod cost.

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
| 2 pods × $180K (conservative) | $360,000 |
| 3 pods × $180K (capacity) | $540,000 |
| **Monthly Gross Profit** | **$176,500-429,500** |
| | |
| **Payback** | **1-2 months** |

### Key Economic Points
- Under $500K startup — financeable with equipment loan or SBA
- Profitable from Pod #1 at $180K selling price
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
- **Defense-spec pods** — TEMPEST shielding, SCIF-rated, hardened connectors, anti-tamper
- **Mobile deployment** — rapid-deploy pods for disaster response, military forward operating
- **R&D / prototype** — new cooling configs, new rack layouts, experimental hardware
- **Retrofit / upgrade** — field-returned pods for cooling system upgrade or GPU refresh

---

*ADC — Advantage Design & Construction*
*Mission Control — Document generated 2026-03-11*
