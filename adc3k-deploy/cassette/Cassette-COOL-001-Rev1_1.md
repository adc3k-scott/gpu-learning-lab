# Cassette — PRIMARY PG25 COOLING LOOP SPECIFICATION

**Document:** Cassette-COOL-001
**Revision:** 1.1
**Date:** 2026-04-22
**Classification:** CONFIDENTIAL
**Companion to:** Cassette-INT-001 · Cassette-ECP-001 · Cassette-BOM-001 · Cassette-COOL2-001 · Cassette-ELEC-001

**Purpose:** Complete hydraulic and thermal specification for the primary PG25 coolant loop inside the Cassette. Covers every wetted component from the rack cold-plate quick-disconnect face (Stäubli UQD-25) back through the welded branch lateral, through the DN125 distribution header in the floor trench, to the Stäubli QBH-150 DN150 QD plate at the CDU-end ECP. Defines flow allocation, pressure drop budget, velocity envelope, manifold geometry, isolation schedule, fluid chemistry, and hydraulic commissioning. Everything downstream of the QBH-150 QD face (flexible hose, external CDU skid) is governed by Cassette-COOL2-001 and is out of scope here.

**Prepared by:** Scott Tomsu · CEO / Chief Engineer
scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana

---

## TABLE OF CONTENTS

- §1  Scope
- §2  Fluid Properties — PG25 at Design Temperatures
- §3  Heat Load Schedule
- §4  Flow Allocation per Rack
- §5  Pressure Drop Budget
- §6  Velocity Analysis
- §7  Manifold Design
- §8  Isolation Valve Schedule
- §9  PG25 Fluid Quality Requirements
- §10 Commissioning — Hydraulic Checkout
- §11 Open Items

---

## §1  SCOPE

### What This Document Covers

The sealed primary PG25 coolant loop inside the Cassette, specifically:

- Rack cold-plate UQD-25 mating faces (R1–R9 compute, R10 control) — Cassette-side half
- Branch laterals from UQD arrays to distribution header (DN40 compute, DN25 control)
- Per-rack isolation valves
- DN125 supply and return headers, full length (rack zone + Service End Zone extension)
- Manifold vents, drains, and instrumentation taps
- QD plate assembly (QBH-150 DN150 supply and return), Cassette-side half

### What This Document Does Not Cover

- External CDU skid, pumps, heat exchangers, expansion tank, PG25 makeup — governed by **Cassette-COOL2-001**
- Flexible DN150 braided hoses between Cassette QBH-150 and CDU skid — listed in BOM-001 §5.5, hydraulic detail in COOL2-001
- Cold-plate internals and rack-side UQD halves — NVIDIA MGX 3rd gen scope (Vera Rubin NVL72 / NVL144 CPX), not Cassette design
- Munters dehumidification circuit — INT-001 §15 and ECP-001 §9 (not a PG25 system)
- Delta in-row power racks R11–R15 — air-cooled internally; no PG25 connection

### Rule of Hydraulic Contract

The Cassette guarantees the specified heat removal and return temperature envelope **at the QBH-150 QD face** when the CDU skid delivers PG25 within the inlet specifications of this document. The CDU skid is responsible for maintaining loop pressure, flow, temperature, and chemistry at the QD face. The Cassette is a passive thermal load from the skid's perspective.

---

## §2  FLUID PROPERTIES — PG25 AT DESIGN TEMPERATURES

Inhibited propylene glycol 25% v/v in deionized water, food-grade acceptable (Dowfrost HD, DynaCool, or equivalent per C-02). Property values below are interpolated from manufacturer data at atmospheric pressure; pressurized-loop correction is negligible at 10 bar working.

| Property                       | Symbol | 45 °C (supply) | 50 °C (loop avg) | 60 °C (return max) | Units            |
|--------------------------------|--------|----------------|------------------|--------------------|------------------|
| Density                        | ρ      | 1,017          | 1,015            | 1,011              | kg/m³            |
| Dynamic viscosity              | μ      | 1.10 × 10⁻³    | 0.95 × 10⁻³      | 0.82 × 10⁻³        | Pa·s             |
| Kinematic viscosity            | ν      | 1.08 × 10⁻⁶    | 0.94 × 10⁻⁶      | 0.81 × 10⁻⁶        | m²/s             |
| Specific heat                  | Cₚ     | 3,990          | 4,000            | 4,010              | J/kg·K           |
| Thermal conductivity           | k      | 0.548          | 0.552            | 0.558              | W/m·K            |
| Prandtl number                 | Pr     | 8.0            | 6.9              | 5.9                | —                |
| Volumetric heat capacity (ρCₚ) | —      | 4.06 × 10⁶     | 4.06 × 10⁶       | 4.05 × 10⁶         | J/m³·K           |

**Sizing basis:** all flow calculations use ρ = 1,017 kg/m³ and Cₚ = 3,990 J/kg·K at supply temperature (45 °C), which is the worst case for volumetric flow demand at a given heat load. Reynolds number calculations use μ = 0.95 × 10⁻³ Pa·s at loop-average temperature (50 °C).

**Freeze protection:** PG25 inhibited mix freezes at approximately −10 °C and bursts at approximately −18 °C. Adequate for all onshore Lafayette, LA operating conditions and offshore Gulf of Mexico deployments. Not adequate for Arctic or North Atlantic service without a higher glycol fraction; any such deployment requires re-verification of this section plus re-sizing of §4 flows (viscosity at lower temperature increases Δp budget).

---

## §3  HEAT LOAD SCHEDULE

All infrastructure is sized to the **NVL144 CPX tier (160 kW/rack)**, consistent with the installed-capacity sizing philosophy applied in ELEC-001 §18. NVL72 tier (120 kW/rack) is shown as the nominal operating point; CPX is the sizing basis for pipe, manifold, QD, and flow envelope.

| Rack | Role                   | NVL72 load (kW) | CPX load (kW) | Return ΔT (design) |
|------|------------------------|-----------------|---------------|--------------------|
| R1   | Compute — Vera Rubin   | 120             | 160           | 10–15 °C           |
| R2   | Compute — Vera Rubin   | 120             | 160           | 10–15 °C           |
| R3   | Compute — Vera Rubin   | 120             | 160           | 10–15 °C           |
| R4   | Compute — Vera Rubin   | 120             | 160           | 10–15 °C           |
| R5   | Compute — Vera Rubin   | 120             | 160           | 10–15 °C           |
| R6   | Compute — Vera Rubin   | 120             | 160           | 10–15 °C           |
| R7   | Compute — Vera Rubin   | 120             | 160           | 10–15 °C           |
| R8   | Compute — Vera Rubin   | 120             | 160           | 10–15 °C           |
| R9   | Compute — Vera Rubin   | 120             | 160           | 10–15 °C           |
| R10  | Control / IB / mgmt    | 25              | 25            | 10 °C              |
| **TOTAL compute + control** | | **1,105** | **1,465** | — |

**Delta in-row power racks (R11–R15): excluded from PG25 loop.** Delta racks are air-cooled internally and reject their 2% conversion loss (~66 kW aggregate at 3,300 kW installed) into the pod interior volume, which is removed by the Munters DSS Pro dehumidification circuit (INT-001 §15). Delta heat load is not seen at the PG25 QD plate.

### Design Point vs Sizing Point

| Parameter                   | NVL72 (design op)  | CPX (sizing) |
|-----------------------------|--------------------|--------------|
| Total loop heat load        | 1,105 kW           | 1,465 kW     |
| Supply temperature          | 45 °C              | 45 °C        |
| Return temperature (design) | 55 °C (ΔT = 10 °C) | 57 °C (ΔT = 12 °C) |
| Bulk loop flow              | ~1,640 LPM         | **~1,810 LPM** |

**All piping, QDs, branches, and manifold geometry below are sized to the 1,810 LPM CPX case.** NVL72 operation at 1,640 LPM produces lower velocities and lower Δp — within the same envelope with additional margin.

---

## §4  FLOW ALLOCATION PER RACK

Flow per rack from Q = ṁ·Cₚ·ΔT, with ṁ = ρ·V̇:

$$ \dot{V} = \frac{Q}{\rho \cdot C_p \cdot \Delta T} $$

Using ρ = 1,017 kg/m³, Cₚ = 3,990 J/kg·K:

| Rack / Group       | Q (kW) | ΔT (°C) | ṁ (kg/s) | V̇ (L/s) | V̇ (LPM) |
|--------------------|--------|---------|----------|----------|----------|
| R1–R9 each (NVL72, design) | 120 | 12 | 2.51 | 2.47 | **148** |
| R1–R9 each (CPX, sizing)   | 160 | 12 | 3.34 | 3.29 | **197** |
| R1–R9 each (CPX, ΔT max)   | 160 | 15 | 2.67 | 2.63 | **158** |
| R10 (control, design)      | 25  | 10 | 0.627 | 0.617 | **37** |
| **TOTAL — NVL72 design**   | 1,105 | — | — | — | **1,369** |
| **TOTAL — CPX sizing**     | 1,465 | — | — | — | **1,810** |
| **TOTAL — CPX ΔT-max**     | 1,465 | — | — | — | **1,459** |

### Sizing Flow

**Cassette primary loop design flow: 1,810 LPM at CPX tier, ΔT = 12 °C.**

This supersedes the preliminary 1,650 LPM figure in ECP-001 Rev 1.2 §7 and INT-001 Rev 1.3 (which carried over from an earlier NVL72-at-ΔT-12 °C basis of 1,632 LPM). COOL-001 becomes authoritative for loop flow; ECP-001 and INT-001 to be synchronized on next revision. C-01 (this document) remains open pending NVIDIA/Foxconn confirmation of actual CPX sustained heat dissipation.

### Per-Rack Flow Tabulation

| Rack | NVL72 flow (LPM) | CPX flow (LPM) | Branch size | UQD count (per side) |
|------|------------------|----------------|-------------|----------------------|
| R1   | 148              | 197            | DN40        | 3                    |
| R2   | 148              | 197            | DN40        | 3                    |
| R3   | 148              | 197            | DN40        | 3                    |
| R4   | 148              | 197            | DN40        | 3                    |
| R5   | 148              | 197            | DN40        | 3                    |
| R6   | 148              | 197            | DN40        | 3                    |
| R7   | 148              | 197            | DN40        | 3                    |
| R8   | 148              | 197            | DN40        | 3                    |
| R9   | 148              | 197            | DN40        | 3                    |
| R10  | 37               | 37             | DN25        | 1                    |

Per-UQD flow (CPX, 3 parallel on compute branch): 197 ÷ 3 = **65.7 LPM (17.4 GPM)** per UQD, within Stäubli UQD-25 envelope (C-03 pending model confirmation).

---

## §5  PRESSURE DROP BUDGET

### Pipe Geometry (ANSI B36.10 / DN Sch 40 stainless)

| Nominal | Schedule | OD (mm) | Wall (mm) | ID (mm) | A (m²)       |
|---------|----------|---------|-----------|---------|--------------|
| DN125   | Sch 40   | 141.3   | 6.55      | 128.2   | 0.01291      |
| DN40    | Sch 40   | 48.3    | 3.68      | 40.9    | 1.314 × 10⁻³ |
| DN25    | Sch 40   | 33.4    | 3.38      | 26.6    | 5.55 × 10⁻⁴  |
| DN150   | Sch 40   | 168.3   | 7.11      | 154.1   | 0.01865      |

### Worst-Case Flow Path

**Worst case = most distant compute rack from the QBH-150 QD plate.** The QD plate sits in the Service End Zone at the CDU-end ECP (INT-001 §8). ELEC-001 §12 labels **R9 as farthest from the DC busway origin** (at the ELEC end, opposite the CDU end). R9 is therefore physically adjacent to the Service End Zone and **closest to the QD plate**. By the same geometry, **R1 is closest to the ELEC end and farthest from the QD plate** — R1 is the hydraulic worst case.

Header length, QD to R1 takeoff: 1.0 m (Service End Zone, QD plate to R10/R9 tees) + 9.332 m (rack zone, R9 to R1 takeoffs) = **10.332 m** supply, same for return.

#### Δp Breakdown — Supply Side (R1 Path)

| # | Segment                                   | Length | Conductor / Item | Flow     | V (m/s) | Δp (bar) |
|---|-------------------------------------------|--------|------------------|----------|---------|----------|
| 1 | QBH-150 supply QD face (Cassette side)    | —      | DN150 dry-break  | 1,810 LPM | 1.71   | 0.075    |
| 2 | DN125 header, QD to R1 takeoff            | 10.3 m | Sch 40 304L/316L | 197–1,810 LPM tapered | 0.25–2.34 | 0.017 |
| 3 | DN125 × DN40 branch tee (R1 takeoff)      | —      | Weld tee         | 197 LPM  | 2.50    | 0.032    |
| 4 | DN40 branch lateral + 90° elbow           | 0.5 m  | Sch 40 weld      | 197 LPM  | 2.50    | 0.036    |
| 5 | DN40 isolation ball valve (open)          | —      | Apollo 1"        | 197 LPM  | 2.50    | 0.005    |
| 6 | Branch manifold → 3-way UQD array reducer | —      | Custom fab       | 197 LPM  | —       | 0.010    |
| 7 | 3× parallel UQD-25 (supply)               | —      | Stäubli UQD-25   | 65.7 LPM each | 2.23 | 0.100    |
|   | **Supply subtotal (QD to rack UQD face)** |        |                  |          |         | **0.275** |

#### Rack Internal Loop (R1)

Cold-plate internal Δp is NVIDIA / Foxconn / HPE scope. Typical NVL72 Oberon rack internal loop: 0.5–0.8 bar at rated flow. **Not included in the COOL-001 budget.** The CDU skid pump head (COOL2-001) must add cassette loop Δp + rack internal Δp.

#### Δp Breakdown — Return Side (R1 Path)

| # | Segment                                   | Length | Conductor / Item | Flow     | V (m/s) | Δp (bar) |
|---|-------------------------------------------|--------|------------------|----------|---------|----------|
| 1 | 3× parallel UQD-25 (return)               | —      | Stäubli UQD-25   | 65.7 LPM each | 2.23 | 0.100    |
| 2 | UQD → branch manifold reducer             | —      | Custom fab       | 197 LPM  | —       | 0.010    |
| 3 | DN40 isolation ball valve (open)          | —      | Apollo 1"        | 197 LPM  | 2.50    | 0.005    |
| 4 | DN40 branch lateral + 90° elbow           | 0.5 m  | Sch 40 weld      | 197 LPM  | 2.50    | 0.036    |
| 5 | DN125 × DN40 branch tee (R1 merge)        | —      | Weld tee         | 197 LPM  | 2.50    | 0.032    |
| 6 | DN125 header, R1 merge to QD              | 10.3 m | Sch 40 304L/316L | 197–1,810 LPM tapered | 0.25–2.34 | 0.017 |
| 7 | QBH-150 return QD face (Cassette side)    | —      | DN150 dry-break  | 1,810 LPM | 1.71   | 0.075    |
|   | **Return subtotal (rack UQD face to QD)** |        |                  |          |         | **0.275** |

### Total Cassette-Internal Loop Δp (QD-to-QD, R1 path, excluding rack internal)

**Cassette primary loop Δp = 0.55 bar (CPX sizing, R1 worst case)**

- NVL72 operation (148 LPM per rack) scales flow² × 0.62 → cassette loop Δp ≈ 0.35 bar
- Margin to working pressure (10 bar): ample
- Margin to hydrotest (15 bar): ample
- CDU skid pump head requirement at QBH-150 face: **≥ 0.55 bar + rack internal (0.5–0.8 bar) = 1.05–1.35 bar**, plus COOL2-001 flexible-hose run and skid internal Δp

### Fitting K-Factors Used

| Fitting                          | K    | Notes                       |
|----------------------------------|------|-----------------------------|
| DN125 × DN40 branch tee (branch path) | 1.0  | Crane TP-410                |
| 90° weld elbow, long-radius     | 0.3  | In DN40 lateral             |
| Sch 40 ball valve (full open)    | 0.05 | Apollo/Watts                |
| Stäubli UQD-25 mated pair (est.) | Cv ≈ 14 gpm/psi⁰·⁵ | Per single mated pair; 3 parallel = effective Cv ≈ 24 for branch |
| Stäubli QBH-150 DN150 pair       | Cv ≈ 400 gpm/psi⁰·⁵ (est.) | C-05 pending Stäubli datasheet |

### Δp Sensitivity to C-01 / C-05

If actual CPX rack sustained load > 160 kW (e.g., 180 kW), flow scales linearly → velocity +13% → Δp +28%. New loop Δp ≈ 0.70 bar. Still within 10 bar envelope. No re-size required unless CPX exceeds ~220 kW sustained, which is not on NVIDIA's roadmap. **Header and branch geometry are not sensitive to ±20% flow variation.** QBH-150 Δp estimate is the largest single uncertainty; firm Stäubli Cv data (C-05) is required before COOL2-001 pump selection.

---

## §6  VELOCITY ANALYSIS

Target envelope for glycol–water in stainless: **1.0–3.0 m/s**. Below 1.0 m/s, sedimentation and microbial risk increase in long-duration idle conditions; above 3.0 m/s, erosion-corrosion risk (particularly at tees and bends) increases, and pump energy is wasted.

| Segment                         | V (m/s) at CPX | V (m/s) at NVL72 | Target      | Status     |
|---------------------------------|----------------|------------------|-------------|------------|
| QBH-150 DN150 QD (1,810 LPM)    | 1.71           | 1.55             | 1.0–3.0     | ✓          |
| DN125 header, QD end (full flow) | 2.34           | 1.91             | 1.0–3.0     | ✓          |
| DN125 header, R1 end (stub flow) | 0.25           | 0.21             | 1.0–3.0     | ⚠ low — see note |
| DN40 compute branch (197 LPM)   | 2.50           | 1.88             | 1.0–3.0     | ✓          |
| DN25 R10 branch (37 LPM)        | 1.11           | 1.11             | 1.0–3.0     | ✓          |
| UQD-25 bore (65.7 LPM)          | 2.23           | 1.68             | 1.0–3.0     | ✓          |

**Note on header far-end velocity:** The DN125 supply and return headers taper by flow (not by pipe diameter) from 1,810 LPM at the QD end to 197 LPM past the R1 takeoff, giving an end-stub velocity of 0.25 m/s at CPX. This is below the 1.0 m/s target but acceptable because:

1. The loop is closed, filled with inhibited PG25 with DO < 0.1 mg/L — no corrosion driver
2. No sediment source (sealed appliance, commissioned chemistry)
3. Header stub is the last 1.0 m past the R1 takeoff — short residence
4. Biocidal inhibitor package prevents microbial growth independent of velocity

The alternative — tapering pipe diameter along the header — adds manufacturing complexity, increases weld count, and is not justified by the low-velocity residual. **Recommendation: retain uniform DN125 header.** Commissioning (§10) includes flush procedure to purge any air or fines from the stub zones at startup.

### Reynolds Number Verification (Turbulent Flow Required for Good Mixing)

| Segment                       | Re at CPX | Flow Regime |
|-------------------------------|-----------|-------------|
| DN125 header, QD end          | 320,000   | Fully turbulent |
| DN125 header, R1 stub         | 34,200    | Turbulent (above transition at Re > 4,000) |
| DN40 compute branch           | 109,300   | Fully turbulent |
| DN25 R10 branch               | 31,600    | Turbulent   |
| UQD-25 bore                   | 59,600    | Turbulent   |
| QBH-150 DN150                 | 275,000   | Fully turbulent |

All segments operate in the turbulent regime. No laminar or transition-zone flow in any operating case.

---

## §7  MANIFOLD DESIGN

### Layout

**Supply header:** DN125 Sch 40 stainless (304L onshore / 316L offshore), total length ≈ 10.3 m end-to-end, welded construction per INT-001 §26 sealed pressure-vessel spec. Installed in the floor trench along the centerline of the Cassette. Insulated with 25 mm Armacell closed-cell foam (BOM-001 §5.1).

**Return header:** Identical construction, parallel to supply in the same trench.

**Branch tees:** 9 × DN125 × DN40 tees for compute racks (R1–R9); 1 × DN125 × DN25 tee for control rack (R10). Spacing per INT-001 §5 rack layout: 1,036 mm between rack centerlines in the 9,332 mm rack zone, with R10 tee offset into the Service End Zone.

**Branch laterals:** DN40 × ~500 mm vertical drops per compute rack; DN25 × ~500 mm for R10. Each terminates at a per-rack manifold with 3× UQD-25 parallel outlets (compute) or 1× UQD-25 (control).

### Header Taper Decision

Options evaluated:

| Approach                          | Pros                                   | Cons                                    | Decision |
|-----------------------------------|----------------------------------------|-----------------------------------------|----------|
| Uniform DN125 end-to-end          | Simple fab, fewer welds, low Δp (0.017 bar), easy NDT | Low V at far-end stub (0.25 m/s) | **Selected** |
| Tapered DN125 → DN80 → DN50      | Uniform velocity along length          | 2–3 weld transitions, higher fab cost, higher Δp per meter at tapered sections, marginal hydraulic benefit | Rejected |
| Reverse-return (Tichelmann) loop  | Inherent flow balance across all branches | Adds 10+ m of pipe, doubles manifold mass, doesn't fit floor trench geometry | Rejected |

**Decision:** uniform DN125 headers. Flow balance at the branches is addressed by branch-level throttling valves (see below) if required at commissioning, not by header diameter change.

### Flow Uniformity

The header-to-branch velocity ratio is the primary hydraulic indicator of flow distribution uniformity in a multi-branch manifold. At each branch tee:

$$ \frac{V_{branch}}{V_{header, \; at \; tee}} $$

A ratio > 1 means the branch takeoff attracts flow preferentially — good for uniformity. A ratio < 0.5 means the header has enough inertia to starve the far branches.

| Branch tee (R1 = farthest, R9 = nearest to QD) | V_header at tee (m/s) | V_branch (m/s) | Ratio | Uniformity |
|------------------------------------------------|-----------------------|----------------|-------|------------|
| R9 tee (near QD, full header flow)             | 2.34                  | 2.50           | 1.07  | Borderline — slight flow preference |
| R5 tee (mid-header)                            | 1.30                  | 2.50           | 1.92  | Strong branch preference |
| R1 tee (far end, last compute takeoff)         | 0.44                  | 2.50           | 5.68  | Strong branch preference |

**Conclusion:** the header geometry naturally favors uniform flow distribution because branch velocity exceeds header velocity at every tee except R9. Theoretical maldistribution at R9 is ≤ 5% without any balancing valve.

### Balancing Provisions

Each per-rack branch lateral includes a **DN40 balancing/isolation ball valve** (BOM-001 §5.1, 20 units). During commissioning (§10), clamp-on ultrasonic flow meters at each branch verify actual distribution. If any branch deviates > 5% from design flow at the CPX design point:

1. Throttle the nearer-branch valves partially closed
2. Re-measure all branches
3. Iterate until all branches within ±3%

Post-commissioning, the valves are locked in position with tamper-indicating wire ties. In practice, the velocity-ratio analysis above predicts that no throttling is required and commissioning will confirm.

### Branch Tee Geometry

| Parameter                | Value                              |
|--------------------------|------------------------------------|
| Tee type                 | Weld-saddle forged tee, DN125 × DN40 (9 units), DN125 × DN25 (1 unit) |
| Material                 | 304L SS (onshore) / 316L SS (offshore), forged, full-penetration weld |
| Flow direction marking   | Directional arrow stamped on forged tee body |
| Orientation              | Branch takeoff vertical (upward) — avoids trapping air in header |
| NDT per tee              | 100% dye penetrant at weld root; 100% radiographic on the QD-end 3 tees (R7, R8, R9) per INT-001 §26 |

### Manifold Air Bleed and Drain Layout

- **Air bleeds:** 8 × DN15 brass manual vent valves (BOM-001 §5.1) at header high points — both ends of supply and return, mid-span above each pair of compute branches, and at the QD plate
- **Drains:** 3 × DN25 ball valves at the three lowest points of the headers (at ELEC-side stub, mid-span floor trench low point, QD end)
- **Expansion allowance:** all header sections include a welded bellows-type expansion joint or guided-loop expansion joint (one per 5 m of straight run) to accommodate thermal expansion between ambient fill (~25 °C) and operating (50 °C average) — linear expansion ≈ 4.3 mm per meter per 100 °C for 304L, so 25 °C ΔT across 10 m gives ~1.1 mm — small but accommodated

---

## §8  ISOLATION VALVE SCHEDULE

Per-rack isolation enables single-rack service without draining the loop. All valves are lockable and BMS-readable (position-sensed) per INT-001 §18 sensor schedule.

| Tag       | Service                           | Location                | Size      | Actuation     | Function                          |
|-----------|-----------------------------------|-------------------------|-----------|---------------|-----------------------------------|
| ISV-S-R1  | Supply isolation, R1              | R1 branch lateral       | DN40, 1"  | Manual, lockable | Rack service                   |
| ISV-R-R1  | Return isolation, R1              | R1 branch lateral       | DN40, 1"  | Manual, lockable | Rack service                   |
| ISV-S-R2  | Supply isolation, R2              | R2 branch lateral       | DN40, 1"  | Manual, lockable | Rack service                   |
| ISV-R-R2  | Return isolation, R2              | R2 branch lateral       | DN40, 1"  | Manual, lockable | Rack service                   |
| …         | (R3 through R9, same pattern)     | …                       | DN40, 1"  | Manual, lockable | Rack service                   |
| ISV-S-R9  | Supply isolation, R9              | R9 branch lateral       | DN40, 1"  | Manual, lockable | Rack service                   |
| ISV-R-R9  | Return isolation, R9              | R9 branch lateral       | DN40, 1"  | Manual, lockable | Rack service                   |
| ISV-S-R10 | Supply isolation, R10             | R10 branch lateral      | DN25, 1"  | Manual, lockable | Rack service                   |
| ISV-R-R10 | Return isolation, R10             | R10 branch lateral      | DN25, 1"  | Manual, lockable | Rack service                   |
| **Compute + control totals** | **10 supply + 10 return = 20 per-rack valves** | | | | |
| MIV-S     | Main supply isolation, pod side   | Adjacent to QBH-150 supply | DN125 | Motorized (Belimo), 24 VDC, BMS-commanded | Emergency leak isolation |
| MIV-R     | Main return isolation, pod side   | Adjacent to QBH-150 return | DN125 | Motorized (Belimo), 24 VDC, BMS-commanded | Emergency leak isolation |
| DV-1      | Header drain — ELEC stub          | End of rack-zone header | DN25, 1"  | Manual        | Service drain                 |
| DV-2      | Header drain — mid-span low point | Floor trench low point  | DN25, 1"  | Manual        | Service drain                 |
| DV-3      | Header drain — QD plate end       | Under QD plate          | DN25, 1"  | Manual        | Service drain                 |
| VV-1…VV-8 | Manual air vents                  | Header high points (×8) | DN15, ½" | Manual brass  | Commissioning air purge       |
| PRV-1     | Pressure relief valve             | At QD plate, supply manifold | DN20  | Spring, 12 bar set | Over-pressure protection per BOM-001 §5.3 |

### Lockout / Tagout Protocol

1. Isolate the rack by closing ISV-S-Rn and ISV-R-Rn
2. Apply padlocks (one per valve) with unique rack-assignment tags
3. Bleed residual pressure through the rack-side UQD male half (reverse-flow)
4. Open the rack access panel; perform UQD disconnect per ECP-001 §7 protocol
5. On completion: reverse — reconnect UQDs, verify seating, re-open ISV valves, purge air at VV-n if header was drained

### Motorized Main Isolation Valves (MIV-S and MIV-R)

MIV-S and MIV-R are commanded **closed** by the BMS on any of the following events (INT-001 §14):
- TraceTek leak detection alarm Level 2 (confirmed leak)
- Sump high-high level alarm
- Supply temperature > 65 °C (CDU skid fault → pod self-isolation)
- Loop pressure < 5 bar (loss of CDU skid pump → pod self-isolation)
- E-stop assertion from platform or pod

Typical closure time: 2 seconds. Valves fail-closed on loss of 24 VDC (life-safety bus spec per ELEC-001 §5).

---

## §9  PG25 FLUID QUALITY REQUIREMENTS

Matches ECP-001 §7 fluid quality table (CDU skid / platform responsibility for ongoing maintenance of this chemistry).

| Parameter                  | Limit                                                        |
|----------------------------|--------------------------------------------------------------|
| Glycol concentration       | 25% v/v ±2% (inhibited propylene glycol, food-grade acceptable) |
| Glycol product             | Dowfrost HD or DynaCool (C-02 pending final selection)       |
| Inhibitor package          | Per glycol manufacturer — organic acid technology (OAT) preferred |
| pH                         | 8.0–9.0                                                      |
| Chlorides                  | < 25 mg/L                                                    |
| Sulfates                   | < 50 mg/L                                                    |
| Conductivity               | < 200 μS/cm                                                  |
| Total suspended solids     | < 5 mg/L                                                     |
| Dissolved oxygen           | < 0.1 mg/L                                                   |
| Biological load            | Non-detectable (closed loop)                                 |
| Iron (dissolved)           | < 0.5 mg/L                                                   |
| Copper (dissolved)         | < 0.2 mg/L                                                   |
| Reserve alkalinity         | Per glycol manufacturer spec (typically 8–12 mL 0.1N HCl per 10 mL sample) |

### Audit Protocol

- **Factory fill:** full chemistry panel documented at commissioning; certificate retained with Cassette records
- **Annual:** sample drawn from DV-2 mid-span drain; full panel re-analyzed; inhibitor top-off if reserve alkalinity below manufacturer threshold
- **Corrosion coupons:** optional — CDU skid side, not Cassette interior (avoids unsealing the pod)

### Compatibility

All wetted metallic materials in the Cassette primary loop are stainless steel (304L onshore / 316L offshore). No copper, brass, galvanized, or aluminum wetted parts. PG25 inhibitor packages are compatible with stainless; no galvanic cell risk within the loop.

**Note:** manual air-vent valves (VV-1…VV-8) are DN15 brass (BOM-001 §5.1). Brass-to-stainless galvanic contact is localized at the vent and not in the main flow path; stagnant volume is negligible; inhibitor package handles localized corrosion. For offshore variant, upgrade to 316L stainless vent valves is optional (C-04 pending).

### Chemistry Drift Monitoring

PG25 chemistry is monitored indirectly by:
- Conductivity probe at the sump (INT-001 §14, seawater discrimination dual-purpose) — not in the primary loop
- Supply and return RTDs — thermal drift indicates fouling
- Pressure drop monitoring — increase in loop Δp at fixed flow indicates scaling or biofouling

There is no in-loop chemistry sensor in the Cassette; the pod is a sealed appliance and chemistry is verified by annual sample. Real-time chemistry monitoring, if required, is implemented at the CDU skid (COOL2-001 scope).

---

## §10  COMMISSIONING — HYDRAULIC CHECKOUT

This section covers hydraulic-specific commissioning steps. Overall commissioning sequence is governed by INT-001 §26; §10 below replaces / supplements §26 steps 3–8 for the PG25 loop specifically.

### Factory Hydraulic Commissioning

#### H-1  Weld NDT

Per INT-001 §26 step 2. Specific to the cooling loop:
- 100% visual inspection of every weld
- 100% dye penetrant on branch tees (10 tees) and QD plate welds (2 QBH-150 weldments)
- 10% radiographic inspection — sampled across supply header, return header, and all QD plate weldments
- Acceptance per ASME B31.3 for normal fluid service

#### H-2  Pneumatic Proof Test

- With UQD male halves capped and QBH-150 QD halves capped
- Charge to 15 bar dry compressed air (clean, oil-free)
- Hold 30 min
- Soap-test every weld, flange, valve packing, and cap
- Acceptance: zero visible bubbles at any joint

#### H-3  Vacuum Decay Test

- Evacuate loop to ≤ 50 Pa absolute using two-stage rotary vane pump
- Isolate pump, allow 5 min stabilization
- Monitor pressure rise over next 5 min
- **Acceptance: ≤ 50 Pa rise in 5 min** (indicates virtual-leak-free system)
- Failure mode: if > 50 Pa rise, re-test after 30 min additional evacuation to drive off adsorbed moisture. Persistent failure triggers helium mass-spectrometer leak search on suspect welds.

#### H-4  Nitrogen Purge and Blanket

- Break vacuum with ultra-high-purity dry N₂ (Airgas UHP, per BOM-001 §5.4)
- Pressurize to 1.5 bar positive (prevents ambient moisture ingress)
- Blanket maintained through rack installation window

#### H-5  Rack Installation and Branch Hydrostat

Per INT-001 §26 step 6:
- UQD-25 halves mated at each rack branch (3 per side per compute rack, 1 per side per R10)
- Each rack branch individually hydrostat-tested to **15 bar** for 15 min
- Branch-to-header isolation via ISV-S-Rn / ISV-R-Rn (closed during branch test; branch-side hydrostat only)
- Acceptance: ≤ 0.1 bar decay in 15 min per branch

#### H-6  Initial PG25 Fill

- Via fill port on QD plate (BOM-001 §5.2, ½" NPT ball valve)
- Pre-blended PG25 (Dowfrost HD or DynaCool) delivered to factory in sealed drums; certificate of analysis matches §9 chemistry table
- Fill volume: 180 L (Cassette interior only; CDU skid fills separately)
- Bleeding sequence: open all 8 VV vents in sequence as loop rises, lowest to highest
- Target fill pressure: 3.5 bar with pod at 25 °C ambient

#### H-7  Pressure Decay Confirmation (Filled Loop)

- Pressurize to 15 bar (hydrostatic test pressure)
- Hold 60 min
- Monitor pressure decay; acceptance per INT-001 §26 step 3 (≤ 0.2 bar drop) — this supersedes the 30-min air test for the final fill-state verification

#### H-8  Instrumentation Verification

- Supply RTD and return RTD readings within ±1 °C of each other with zero flow
- Supply and return pressure transmitters (QD plate) calibrated to 0–10 bar, reading matches dead-weight tester within ±0.05 bar
- QD seating limit switches report mated = true
- BMS logging active and timestamps agree with GPS reference

#### H-9  QD Cap Install and Ship

- QD protective caps (Stäubli OEM) installed on both QBH-150 faces
- Cassette shipped as sealed unit

### Site Hydraulic Commissioning (≤ 12 hours of the 48-hour site target)

#### S-1  Arrival Check

- QBH-150 caps intact — no evidence of contamination or mechanical impact
- TraceTek cable continuity confirmed via BMS
- Loop pressure at arrival within 2.5–4.5 bar (temperature-adjusted from factory 3.5 bar at 25 °C)

#### S-2  Mate to CDU Skid Hoses

- Remove QBH-150 caps; inspect and clean face seals with lint-free cloth
- Mate to pre-filled flexible DN150 hoses (COOL2-001 scope)
- Quarter-turn lock confirmed — audible click on both halves
- Top-off pressure and thermometer check

#### S-3  Flow Distribution Verification

**Critical step — unique to COOL-001 sealed-appliance methodology.**

- Start CDU skid pump, ramp to 50% of design flow (~900 LPM)
- Install clamp-on ultrasonic flow meter (Keyence or Ifm rental kit) on each of the 10 branch laterals, one at a time
- Record flow in each branch; compare to design allocation (197 LPM per compute branch, 37 LPM R10 branch, scaled to 50%)
- **Acceptance: all 10 branches within ±5% of proportional design flow**
- If any branch deviates > 5%, throttle the ISV valve on the nearer branches until distribution is uniform
- Lock ISV valves at final position with tamper wire

#### S-4  Full-Flow Thermal Test

- Ramp CDU skid to design 1,810 LPM at supply 45 °C
- Dispatch compute workload at ~50% of CPX (roughly NVL72 equivalent at 120 kW per rack)
- Run 4 hours
- Verify: supply 45 ± 1 °C, return 52–56 °C (expected at half-load), ΔT across each rack within ±1 °C of adjacent racks, all pressure transmitters and RTDs within range
- No leak alarms on TraceTek

#### S-5  Ramp to Rated and Hold

- Dispatch workload at full CPX (160 kW/rack)
- Verify thermal steady-state within 45 min
- Return temperature: 57 ± 1 °C
- Loop Δp at QD plate (external skid measurement): consistent with COOL2-001 prediction
- Hold 4 hours at rated

#### S-6  Release to Service

Sign-off per ECP-001 §19 acceptance criteria. COOL-001 hydraulic sign-off is a prerequisite to workload dispatch.

---

## §11  OPEN ITEMS

| ID   | Priority | Description                                                                                           | Blocks |
|------|----------|-------------------------------------------------------------------------------------------------------|--------|
| C-01 | P-1      | Confirm NVIDIA Vera Rubin NVL144 CPX actual sustained heat dissipation per rack (currently sized at 160 kW). Required to validate 1,810 LPM design flow and lock CDU skid pump selection in COOL2-001. Request from NVIDIA via Foxconn / HPE / Supermicro channel. | Flow validation; does not block Cassette fabrication |
| C-02 | P-1      | Final PG25 glycol product selection: Dowfrost HD vs DynaCool vs equivalent. Evaluate ASTM D1384 corrosion coupon data, compatibility with 304L/316L stainless, organic acid inhibitor package reserve alkalinity, and food-grade certification (offshore regulatory compatibility). | Initial fill procurement |
| C-03 | P-0      | Confirm exact Stäubli UQD-25 product model and published Cv / Δp curve. "UQD-25" as used in upstream specs may refer to Stäubli UQD08 size (25 mm bore) or a custom/private-label designation. Required before pressure-drop budget in §5 can be firmed. | §5 Δp budget final; branch fabrication |
| C-04 | P-2      | Verify brass manual vent valve compatibility with offshore PG25 chemistry over 20-year service life. Upgrade to 316L SS vent valves optional; decision depends on inhibitor package galvanic tolerance and operator preference. | Offshore variant BOM |
| C-05 | P-0      | Obtain firm Stäubli QBH-150 Cv / Δp curve from manufacturer. Current estimate (Cv ≈ 400 gpm/psi⁰·⁵, Δp ≈ 0.075 bar per half at 1,810 LPM) is the largest single uncertainty in the §5 budget. | CDU skid pump head selection (COOL2-001) |
| C-06 | P-1      | Validate flow uniformity prediction (§7) by commissioning measurement (S-3). No action until first cassette; recorded here for tracking. If real-world deviation > ±5%, revise §7 balancing provisions for subsequent units. | First-article commissioning |
| C-07 | P-2      | R10 control rack heat load (25 kW) is a preliminary estimate. Actual load depends on final IB switch count (Quantum-X800 QM9700 vs QM9790), NVMe storage configuration, and Jetson Orin thermal footprint. Verify when R10 integration spec locks. | R10 branch sizing (currently DN25 with 3× margin — not sensitive) |
| C-08 | P-1      | Cross-document synchronization: ECP-001 §7 states "Flow (design) ~1,650 LPM (preliminary)" and INT-001 §5 / nameplate carries same. COOL-001 supersedes with 1,810 LPM (CPX basis). Update ECP-001 and INT-001 on next revision of each. | Document consistency |

---

**Cassette — Primary PG25 Cooling Loop Specification**
**Cassette-COOL-001 · Rev 1.1 · 2026-04-22**
**Scott Tomsu · scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana**
**CONFIDENTIAL**
