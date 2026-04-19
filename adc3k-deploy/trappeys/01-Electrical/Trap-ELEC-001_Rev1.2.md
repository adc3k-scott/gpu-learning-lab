# ST-TRAP-ELEC-001 — Electrical Architecture — Rev 1.2

**Document:** Electrical Architecture
**Project:** Trappey's AI Center, Lafayette, Louisiana
**Revision:** 1.2 — refinements from ARCHDIAG-001 rolled in (protection detail, LV grounding, feeder categorization, cassette internal topology, AMCL tiers, vendor anchor)
**Date:** April 17, 2026
**Owner:** Scott Tomsu
**Status:** Working draft — architecture anchor for downstream electrical engineering

**Companion visual:** ST-TRAP-ARCHDIAG-001 Rev 0.1 (six-diagram end-to-end SLD from genset to GPU).

---

## 1. Purpose

Electrical architecture anchor for Trappey's AI Center. Defines topology, design philosophy, protection approach, and sizing basis for the behind-the-meter permanent island.

Architecture is **N replicated Marlie-pattern blocks**, each with an 800 VDC common bus, DC-coupled BESS, and DC-coupled solar — identical to the Marlie 5 MW block (eng-pack-5MW Rev 3.x) except for the prime mover. Downstream documents (ST-TRAP-SLD-001, ST-TRAP-PROT-001, ST-TRAP-BESS-001, ST-TRAP-SOLAR-001) inherit from this revision.

## 2. Relationship to other documents

- **BOD-001 Rev 0.4 §E** — ledger (E-01 through E-30) is authoritative; this document explains and justifies those entries
- **BOD-001 Rev 0.4 §C** — cassette platform product spec; 800 VDC umbilical is the cassette-to-facility electrical boundary
- **BOD-001 Rev 0.4 §I** — AI control scope; AMCL five-tier architecture (A-09)
- **eng-pack-5MW Rev 3.x** — Marlie 5 MW reference; Trappey's is N replicated Marlie blocks with Cat CG260-16 substituted for Cat G3520K
- **800 VDC Vendor Comparison sheet** — Delta / Eaton / Schneider procurement analysis (Delta 4.75/5)
- **ST-TRAP-ARCHDIAG-001 Rev 0.1** — six-diagram visual companion to this document

Downstream documents inheriting from Rev 1.2: SLD-001, PROT-001, BESS-001, SOLAR-001.

## 3. Design philosophy — behind-the-meter permanent island

Trappey's operates as a permanent electrical island from day one of Block 1. The facility generates its own power, stores and stabilizes it with BESS, and never imports or exports across an external utility boundary in base-case operation.

- **No LUS interconnect on day one.** Spatial allocation only (BOD E-02).
- **BESS is the block-level stabilizer, not backup.** Sub-second transient response to genset governor lag and load swings. Always active on the 800 VDC bus.
- **Protection is island-only and block-internal.** No anti-islanding, no external sync. Coordinates across AC-DC boundary inside each block.
- **Revenue: colocation only.** No sell-back to LUS modeled.
- **Reliability from internal redundancy.** No utility backstop. 4-genset blocks with 3-needed posture; per-block BESS contingency.

## 4. Architecture overview — replicated Marlie block

Stage 1 comprises 11 identical blocks × 4 cassettes × 2,415 kW facility load = 106.3 MW total cassette facility load. Full Build doubles to 22 blocks.

**One block, top-down:**

1. **Generation.** 4 × Cat CG260-16 gas gensets at 13.8 kV, paralleled on the block MV bus via Cat ECS isochronous sharing. 3-of-4 carry load; 4th is N+1.
2. **Block MV bus.** 13.8 kV arc-resistant switchgear. 87B bus differential. UFLS three-stage at 59.5 / 59.2 / 58.9 Hz at the MV inlet.
3. **Block step-down transformer.** One per block, 13.8 kV Δ → 480Y/277 V, ~15 MVA continuous, Dyn11, dry-type / cast-resin. Feeds the block's in-row power racks and facility ancillary loads.
4. **480 VAC main switchboard.** Solidly grounded wye secondary with 50G residual ground sensing. LSIG main trip unit. Five feeder categories:
   - 16 × Delta 660 kW in-row power racks (~10.6 MVA — the dominant feeder)
   - Cooling plant MCC, VFD-driven (~600 kW working: absorption chiller solution pumps, condenser water pumps, tower makeup pumps, cooling tower fans, adiabatic spray pumps, Vermilion intake pumps)
   - BESS auxiliary (~80 kW: battery HVAC, BMS, fire system)
   - Solar DC-DC buck auxiliary (~10 kW: controls, HVAC)
   - Facility ancillary (~200 kW: SCADA, NOC, site lighting, fire/life safety)
5. **In-row power racks (cassette-side rectification).** ~4 × Delta 660 kW per cassette (5 for rack-level N+1). Internal: 6 × 110 kW PSU shelves, 80 kW BBU per shelf (480 kW aggregate BBU per rack), Power Capacitance Shelf with aluminum caps + supercaps for sub-100 ms GPU swings, EVA for peak shaping, 98% AC-DC at full load, integrated DC fault protection, touch-safe 800 VDC output connector.
6. **Block 800 VDC common busway.** Copper busway. Single-ended 800 VDC. ~12,500 A at 9.66 MW full block load. Voltage regulated by in-row rack rectifiers coordinated with BESS DC-DC converter.
7. **DER ties to 800 VDC bus.** (a) BESS LFP battery racks → battery BMS → bidirectional DC-DC converter (~2 MW continuous, ~4 MW peak) → SSCB + blocking diode → bus. (b) Solar 1500 VDC strings → combiner boxes + DC disconnects → 1500→800 V DC-DC buck with MPPT → SSCB + blocking diode → bus.
8. **Cassette umbilicals.** Four per block. Each: load-break contactor + SSCB at bus tap → 800 VDC cable run → Staubli hot-swap disconnect at cassette boundary. ~3,000 A at 2,415 kW cassette facility load.
9. **Cassette internal (BOD C.10 single panel, BOD E-30 topology).** Staubli hot-swap → cassette 800 VDC overhead busbar → two branches:
   - **Main DC distribution:** 3 × Eaton ORV3 PDUs + NVIDIA Kyber PDUs → 10 × OCP ORV3 racks with NVL72 trays → 72 Vera Rubin GPUs × 10 = 720 GPUs per cassette, 230 kW/rack, 2,300 kW cassette IT
   - **Auxiliary DC-DC:** Boyd CDU pumps (part of 2,000 kW water-glycol primary loop, N+1), Munters HCD/MCD blowers, Jetson AGX Orin BMS (148 sensor channels)
10. **GPU die.** Direct-to-chip water-glycol cold plate fed by Boyd CDU at ≤45°C.

**Campus posture.** 11 electrically independent blocks. No inter-block MV ring. No inter-block 800 VDC tie (E-23 deferred). Shared services (gas header, water plant, NOC, security, AMCL) span the campus but do not carry power between blocks.

**Key boundaries.** (a) Cassette IP boundary at the 800 VDC umbilical — everything upstream is vendor-neutral facility infrastructure, everything downstream is cassette IP per BOD §C. (b) Block boundary — each block electrically self-contained. (c) AC/DC boundary — within each block, the 800 VDC bus is the convergence point; gensets are AC-side, BESS/solar/cassettes are DC-side.

## 5. Generation (per block)

**4 × Cat CG260-16 gas gensets.** 4,000 ekW continuous per genset at 60 Hz, 900 rpm on natural gas. <250 mg/Nm³ NOx at 5% O₂. 25% hydrogen blending capable at the same continuous rating (future optionality, not Stage 1 input).

**Why CG260-16:** 4 MW class matches 1:1 genset:cassette ratio at block level. Lean-burn gas with CHP compatibility. US availability and Cat CSA in-region. Hydrogen blend preserves fuel-transition optionality.

**Prime mover rule:** CG260-16 is for Trappey's and 100+ MW deployments. Cat G3520K is for Marlie 1 and ≤10 MW platforms. Not substitutable.

**Loading:** Design anchor 61.5% → 2,460 kW per genset → 9,840 kW per block at 4 running, or 7,380 kW at 3 running. Block cassette facility load is 9,660 kW (4 × 2,415 kW). **Operational reality:** all 4 gensets run at 60–65% in Mode A, or 3 run at ~83% in Mode B (mirrors eng-pack-5MW mode philosophy at block scale). AI dispatch envelope 55–75%; 63–65% expected average.

**Block MV bus at 13.8 kV** (working; Cat CSA to confirm voltage option per E-6). 4 gensets parallel via Cat ECS isochronous sharing. Block MV bus feeds exactly one load: the block step-down transformer.

**Fuel:** ~2,200 Nm³/hr at full block load. Stage 1 total ~24,000 Nm³/hr across 11 blocks. Pipeline interconnect open.

## 6. Step-down and rectification (per block)

**Block step-down transformer:** one per block, 13.8 kV → 480Y/277 V, ~12–15 MVA continuous, Dyn11, dry-type or cast-resin (no oil handling, lower fire load), Z≈6%. Dedicated to the block; no cross-block sharing. This is the only topological addition vs Marlie — Marlie's G3520K generates 480 VAC directly.

**In-row power racks (E-24, E-25).**

The industry-standard product at 800 VDC scale is the in-row power rack (also called "sidecar" by Eaton/Schneider — same architectural concept): a rack adjacent to compute housing AC-DC conversion, BBU/supercap storage, and 800 VDC busway output. No 2.5 MW single-SKU rectifier skid exists in this market.

**Primary vendor selection: Delta Electronics** per 800 VDC Vendor Comparison scoring (Delta 4.75, Eaton 3.80, Schneider 3.15). Delta is procurement-ready today (OCP 2025, GTC 2026 showcased); Eaton has reference design, SKU-level specs need RFQ; Schneider is pre-release.

**Base configuration: 4 × Delta 800 VDC In-Row 660 kW Power Rack per cassette.** Per rack: 6 × 110 kW Power Shelves on 18.5 kW PSU building blocks at 98% efficiency. 80 kW BBU per shelf = 480 kW aggregate BBU per rack. Aluminum capacitor Power Capacitance Shelf (PCS) + EVA Rack variant for sub-100 ms GPU load-swing smoothing (closes NVIDIA MGX dual-layer storage lower band). Touch-safe DC output with mechanical interlock per NVIDIA MGX. Integrated DC fault protection coordinated with downstream cassette breakers.

**4 racks = 2,640 kW = 9.3% headroom** against 2,415 kW cassette facility load. **5 racks = 3,300 kW = 36.6% headroom** and rack-level N+1. Scott decides 4 vs 5 at RFQ close based on duty-cycle risk tolerance.

**Alternative: 3 × Delta 800 VDC In-Row 1.1 MW Power System per cassette** (headroom built-in) — also Delta, larger scale SKU. Tracked as backup if Delta 660 kW lead times slip.

**Performance spec (vendor-neutral, for RFQ benchmarking):** 480 VAC 3-ph 60 Hz input, 800 VDC single-ended ≤1% ripple output, ≥97% AC-DC at 50–100% load, PF ≥0.99 at rated, THDi ≤5%, integrated BBU for 10+ s cassette full load, integrated supercap for sub-100 ms smoothing, touch-safe EV-heritage output connector with mechanical interlock, integrated DC fault protection, hot-swap module architecture with concurrent maintenance.

**Cassette electrical boundary:** everything upstream of the 800 VDC umbilical is vendor-neutral facility infrastructure; everything downstream (ORV3 PDUs, Kyber PDUs, rack-internal distribution) is cassette IP per BOD C.3.

## 7. Block 800 VDC common bus

One copper busway per block. Connected sources and loads:

- 16 in-row power rack outputs (4 racks × 4 cassettes) — source
- BESS via bidirectional DC-DC — source / sink
- Solar via DC-DC buck — source
- 4 cassette umbilicals — sinks

**Bus current at block full load:** ~12,075 A at 9.66 MW / 800 V (9,660,000 W ÷ 800 V). Within practical copper busway range (comparable to Delta 800 VDC busway or equivalent).

**Per-cassette umbilical:** ~3,000 A at 2,415 kW / 800 V. **Per-rack output:** ~825 A at 660 kW / 800 V.

**Sub-100 ms GPU storage** covered by rack-integrated BBU + PCS per E-20. Facility BESS on the same bus covers sub-second through multi-minute. Dual-layer storage per NVIDIA MGX, implemented cleanly on a single DC bus.

## 8. BESS — DC-coupled per block

**Role:** Block-level system stabilizer, not backup. Sub-second transient response to genset governor lag. Contingency support for single-genset trip inside the block. Graceful shutdown reserve on gas-supply loss. Solar clip-recapture. Load shifting within AI dispatch envelope.

Note that "grid-forming" in the traditional MV-ring sense does not apply — there is no MV ring to form. 800 VDC bus voltage is regulated by the bidirectional DC-DC converter in coordination with the in-row rectifiers. Block MV-side voltage/frequency is set by the CG260-16 governors.

**Sizing:** 40 MWh facility working (BOD E-10), 30–50 MWh envelope. Per-block allocation 3–5 MWh (working midpoint 3.6 MWh). Contingency scenarios (block-scoped):

| Scenario | Per-block energy | Duration |
|---|---|---|
| Single genset trip inside block | ~1–2 MWh | Seconds to minutes |
| Block partial gas curtailment | ~2–3 MWh | Minutes (graceful ramp-down) |
| Full gas loss — graceful shutdown | ~3–4 MWh | 15–20 min orderly cassette cooldown |

**Power rating:** ~2 MW continuous, ~4 MW peak per block. Across 11 blocks: ~22 MW / ~44 MW peak.

**Coupling:** DC-coupled to block 800 VDC bus via bidirectional DC-DC converter. Vendor must confirm DC-coupling capability at the required power rating — primary vendor filter.

**Chemistry:** LiFePO4. Eaton xStorage is the working vendor per eng-pack-5MW Rev 3.0 §24. Alternatives: Tesla Megapack, Fluence, Wärtsilä, Honeywell. Selection driven by: confirmed DC-coupling at 800 V, LFP chemistry, 2026–2027 delivery window, Louisiana service, Cat gas genset paralleling integration history.

## 9. Solar — DC-coupled per block

**Array:** First Solar Series 7 CdTe thin-film modules, 2.05 MW DC total across Building 1 and Building 2 rooftops, 1500 VDC string topology.

**Coupling:** 1500 VDC strings → combiner boxes + DC disconnects → DC-DC buck converter (1500→800 V, MPPT) → SSCB + blocking diode → block 800 VDC bus. No solar inverter. No MV tie.

**Allocation per block:** ~186 kW DC on paper (2.05 MW / 11 blocks). Actual allocation driven by rooftop proximity — blocks near B1/B2 receive the physical tie, others carry zero solar. Does not affect individual block electrical design but affects AMCL dispatch modeling.

**Why DC-coupled:** Matches Marlie block pattern. Eliminates the inverter stage (1–2% efficiency gain over AC-coupled). Places solar on the same bus as the load. 1500→800 V DC-DC buck is a mature product at 2 MW scale (Delta and competitors).

**Operating role:** Subordinate, supplemental, seasonal/diurnal. Not credited in primary sizing. Displaces genset loading during sunny hours.

## 10. Protection philosophy

**Island-only, block-internal.** No anti-islanding relays, no external sync, no external reverse-power. No campus MV ring → no ring-segment directional overcurrent. Protection coordinates inside each block across AC and DC domains.

**Per-genset AC protection (E-26):** 87G differential, 32 reverse power, 40 loss of field, 46 negative sequence, 47 phase sequence, 59 overvoltage, 27 undervoltage, 64G stator ground, 78 out-of-step, 51V voltage-restrained overcurrent. Each genset circuit breaker (52-G1 through 52-G4) carries 87G + 51V minimum.

**Block bus:** 87B bus differential, 51N neutral ground.

**Transformer protection (E-27):** 87T primary + 87T secondary differential (both windings), 49T thermal via RTDs, 63 pressure/gas (cast-resin equivalent of Buchholz). Primary breaker (52-TP): 87T primary + 51 + 50. Secondary breaker (52-TS): 87T secondary + 51 + 50G.

**480 VAC main secondary (E-28):** Solidly grounded wye. 52M main with LSIG trip unit. 50G residual ground sensing at neutral. Insulation resistance monitoring on outgoing feeders.

**Three-stage UFLS** applied at block MV inlet: 59.5 Hz (stage 1), 59.2 Hz (stage 2), 58.9 Hz (stage 3). Shed cassette lanes in priority order; AI dispatch holds shed list current.

**DC-side protection (per NVIDIA 17.5 MW reference pattern):**

- Solid-state circuit breakers (SSCB) at each source tie to 800 V bus (each in-row rack output, BESS tie, solar tie)
- Blocking diodes at each source to prevent reverse flow into faulted sources
- Load-break contactors at each cassette umbilical for isolation
- DC fault protection integrated in the in-row power rack (vendor-provided, coordinated with upstream)
- Cassette-internal DC protection (Eaton ORV3 + Kyber PDUs) coordinated with umbilical

**Coordinated trip schemes across AC-DC boundary:** AC-side fault → SSCB trip isolates DC bus from faulted rack bank before reverse flow. DC-side fault → blocking diodes prevent back-feed; SSCB isolates faulted cassette lane. Internal storage rides through the coordination interval (BBU 10 s + PCS sub-100 ms).

**Arc flash:** arc-resistant switchgear at block MV bus. Arc-flash reduction on 480 VAC main during maintenance. Detailed study in PROT-001.

## 11. Load envelope (Stage 1)

- Cassette IT: 101.2 MW (44 × 2,300 kW)
- Cassette facility: 106.3 MW (44 × 2,415 kW)
- Per block (4 cassettes): 9.66 MW cassette facility
- Non-cassette ancillary: ~3–5 MW distributed across NOC, security, site lighting, mechanical, BESS aux, SCADA, fire/life safety

**Total Stage 1 site:** 109.3–111.3 MW. Generated at 9,840 kW/block × 11 = 108.24 MW at 61.5% loading. **Margin is −1 to −3 MW.** Resolution: operational loading averages 63–65% → 11,160 kW/block × 11 = 122.8 MW. Comfortable. 61.5% design anchor is for Cat longevity discussions; operational reality is slightly higher.

**Diversity factor:** 0.95 on IT load (AI control may flatten further; validate in operation).

## 12. AI dispatch interaction (BOD §I / A-09)

**AMCL five-tier architecture** (BOD A-09, Working):

- **L0 field devices** — Cat ECS governors, protection IEDs, VFDs, Jetson Orin BMS, RTDs, CTs/PTs
- **L1 block controller (PLC)** — paralleling, UFLS, DC-DC setpoints (BESS + solar buck), MPPT, protection trip schemes, safety interlocks. Deterministic, local, cannot be overridden from higher tiers.
- **L2 plant SCADA / data layer** — historian, alarming, OPC-UA backbone, cassette BMS aggregation
- **L3 AMCL dispatch (AI)** — cross-block optimization, gas/load/thermal coupling, solar recapture, BESS orchestration
- **L4 HMI + operator override + cybersecurity** — IEC 62443 segmentation, OT plane isolation, human-in-loop policy gates, incident response

**What AI controls:** per-block genset loading within 55–75%, per-block BESS state (charge/discharge via DC-DC), solar MPPT coordination with BESS state, ancillary dispatch (tower fans, chiller pumps, makeup water), inter-block load balancing (if E-23 tie added).

**What AI does not control:** protective functions (deterministic, local, cannot be overridden), emergency shutdown (local safety interlocks priority), manual maintenance postures (human-in-loop), initial commissioning (human dispatch).

**AI failure mode:** Last-known-good deterministic control. Gensets hold setpoint, BESS DC-DC holds mode, VFDs hold speed. Governors and protection continue autonomously. Operations takes manual dispatch until AI restored.

## 13. Single biggest technical risk

**Cat CG260-16 governor response in island-mode 24/7 at variable loading under AI dispatch, paired with block-level DC-coupled BESS on 800 VDC bus via bidirectional DC-DC converter.**

BESS transient support runs through the DC-DC converter rather than an MV grid-forming inverter. Modern SiC-based DC-DC converters respond in microseconds to milliseconds, so this is not a regression vs Rev 1.0's MV-coupled posture. But it does mean BESS vendor selection must confirm **bidirectional DC-DC response spec, not just grid-forming AC capability**.

**Mitigation path:** Cat CSA engagement — documented governor performance at 55/60/65/70/75% loading. Black-box testing at commissioning. BESS sized conservative enough to ride through governor degradation. AI dispatch avoids rapid transitions where possible.

**If Cat CSA returns unfavorable governor data:** add gensets per block (5:4 instead of 4:4) to reduce per-genset loading variability, or oversize BESS. Both engineerable; neither preferred.

## 14. LUS interconnect — explicit no-provisioning

Per BOD E-02 and Session 2 BTM correction: no physical provisioning for LUS on day one. Spatial allocation only. LUS builds at their cost and schedule. No sell-back revenue in base-case financial model.

## 15. Open items and dependencies

**Blocked on Cat CSA:**

- E-5 — CG260-16 factory voltage options (confirm 13.8 kV assumption)
- E-6 — Governor response at island-mode 24/7 duty under AI dispatch
- E-6b — Part-load exhaust temperature, mass flow, jacket water heat rate curves
- E-6c — Maximum exhaust backpressure

**Blocked on vendor RFQs:**

- E-24 / E-25 — Delta 660 kW rack RFQ; confirm 4 vs 5 per cassette; lead times at 10-unit and 100+ unit quantities
- E-8 — Block step-down transformer (13.8 kV → 480 V, ~15 MVA) RFQ
- E-10 — BESS vendor RFQ with DC-coupled bidirectional DC-DC requirement
- E-11 — Block MV switchgear vendor RFQ
- E-22 — Solar DC-DC buck converter vendor RFQ

**Blocked on contingency analysis:**

- E-10 — Per-block BESS sizing validation (3.6 MWh working)
- E-23 — Inter-block tie decision (11 independent vs inter-block N+1 sharing)

**Blocked on downstream documents:**

- E-9 — Protection coordination study (ST-TRAP-PROT-001), covering AC-DC boundary per block; pickup settings and CT ratios
- E-10 — Per-block single-line (ST-TRAP-SLD-001) plus campus overview

**Independent:** Gas supply interconnect (gates Block 1 energization). LPDES permitting (no electrical dependency).

## 16. Revision plan

- **Rev 1.2 (current)** — refinements from ARCHDIAG-001: protection detail (E-26, E-27), LV grounding (E-28), feeder categories (E-29), cassette internal (E-30), AMCL tiers (A-09), Delta vendor anchor (E-24, E-25)
- **Rev 1.3** — after Cat CSA returns voltage confirmation and governor characterization
- **Rev 1.4** — after Delta / Eaton / Schneider RFQ closes; locks in-row rack count and per-rack specs
- **Rev 1.5** — after BESS RFQ closes; updates §8 with DC-coupled DC-DC specifics
- **Rev 1.6** — after PROT-001; refines §10 with CT ratios, pickup settings, coord intervals
- **Rev 2.0** — ready for external circulation; all C1 dependencies closed

## 17. Approval

Requires Scott's sign-off before downstream electrical documents (SLD, PROT, BESS, SOLAR) can reference it as an architectural anchor. ARCHDIAG-001 Rev 0.1 is the companion visual.

---

**End of ST-TRAP-ELEC-001 Rev 1.2.**
