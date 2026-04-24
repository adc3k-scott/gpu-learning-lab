# ST-TRAP-ELEC-001 — Electrical Architecture — Rev 1.3

**Document:** Electrical Architecture
**Project:** Trappey's AI Center, Lafayette, Louisiana
**Revision:** 1.3 — cassette architecture updated to AC-in (480 VAC primary per Cassette-ELEC-001 Rev 1.3); block-level 800 VDC common bus eliminated; BESS and solar AC-coupled at block 480 VAC bus; in-row racks confirmed inside Cassette; fuel rate corrected; bus ampacity note updated; transformer protection corrected.
**Date:** April 23, 2026
**Owner:** Scott Tomsu
**Status:** Working draft — architecture anchor for downstream electrical engineering

**Companion visual:** ST-TRAP-ARCHDIAG-001 Rev 0.1 (requires update to reflect Rev 1.3 cassette architecture).

---

## 1. Purpose

Electrical architecture anchor for Trappey's AI Center. Defines topology, design philosophy, protection approach, and sizing basis for the behind-the-meter permanent island.

Architecture is **N replicated Marlie-pattern blocks**, each with a 480 VAC distribution bus feeding cassette primary feeds, AC-coupled BESS, and AC-coupled solar — aligned with Cassette-ELEC-001 Rev 1.3 which establishes 480 VAC as the cassette primary input. Downstream documents (ST-TRAP-SLD-001, ST-TRAP-PROT-001, ST-TRAP-BESS-001, ST-TRAP-SOLAR-001) inherit from this revision.

## 2. Relationship to other documents

- **BOD-001 Rev 0.6 §E** — ledger (E-01 through E-30) is authoritative; this document explains and justifies those entries
- **BOD-001 Rev 0.6 §C** — cassette platform product spec; 480 VAC primary feed is the cassette-to-facility electrical boundary per Cassette-ELEC-001 Rev 1.3
- **BOD-001 Rev 0.6 §I** — AI control scope; AMCL five-tier architecture (A-09)
- **Cassette-ELEC-001 Rev 1.3** — Cassette electrical authority; defines 480 VAC primary input, Delta in-row rack topology (R11–R15), cassette-internal 800 VDC bus
- **eng-pack-5MW Rev 3.x** — Marlie 5 MW reference; Trappey's is N replicated Marlie blocks with Cat CG260-16 substituted for Cat G3520K
- **ST-TRAP-ARCHDIAG-001 Rev 0.1** — six-diagram visual companion; requires update to Rev 1.3 cassette architecture

Downstream documents inheriting from Rev 1.3: SLD-001, PROT-001, BESS-001, SOLAR-001.

## 3. Design philosophy — behind-the-meter permanent island

Trappey's operates as a permanent electrical island from day one of Block 1.

- **No LUS interconnect on day one.** Spatial allocation only (BOD E-02).
- **BESS is the block-level stabilizer, not backup.** Sub-second transient response to genset governor lag and load swings via Hitachi AMPS PCS AC-coupled inverter on the block 480 VAC bus.
- **Protection is island-only and block-internal.** No anti-islanding, no external sync. Coordinates across AC boundary inside each block.
- **Revenue: colocation only.** No sell-back to LUS modeled.
- **Reliability from internal redundancy.** No utility backstop. Mode A: 4-of-4 running at 60–65%; Mode B: 3-of-4 at ~83% covers planned-maintenance windows; per-block BESS contingency.

## 4. Architecture overview — replicated Marlie block

Stage 1 comprises 11 identical blocks × 4 cassettes × ~2,295 kW facility load = ~101.0 MW total cassette facility load. Full Build doubles to 22 blocks.

**One block, top-down:**

1. **Generation.** 4 × Cat CG260-16 gas gensets at 13.8 kV, paralleled on the block MV bus via Cat ECS isochronous sharing. All 4 run in Mode A (60–65% each); Mode B — 3 at ~83% — covers planned-maintenance windows.
2. **Block MV bus.** 13.8 kV arc-resistant switchgear. 87B bus differential. UFLS three-stage at 59.5 / 59.2 / 58.9 Hz at the MV inlet.
3. **Block step-down transformer.** One per block, 13.8 kV Δ → 480Y/277 V, ~15 MVA continuous, Dyn11, dry-type / cast-resin. Feeds the block 480 VAC bus.
4. **480 VAC main switchboard.** Solidly grounded wye secondary with 50G residual ground sensing. LSIG main trip unit. Five feeder categories:
   - 4 × cassette 480 VAC primary feeds (~9.2 MVA total — the dominant feeder)
   - BESS inverter (Hitachi AMPS PCS, ~2.1 MVA continuous / ~4.2 MVA peak)
   - Solar inverter (~2.1 MVA peak)
   - Cooling tower MCC, VFD-driven (~136 kW/block; campus centralized plant ~1,500 kW total — tower fans, circulating pumps, makeup/blowdown/chemical dosing; see COOLING-TOWER-001 §10.4)
   - Facility ancillary (~200 kW: SCADA, NOC, site lighting, fire/life safety)
5. **Cassette 480 VAC primary feeds.** Four per block. Each: load-break contactor at block switchboard → 480 VAC cable run → Eaton Magnum DS 6,000 A cassette main disconnect at cassette ECP boundary (per Cassette-ELEC-001 Rev 1.3 §1). Each feed ~2,295 kW at cassette facility load.
6. **DER ties to 480 VAC bus.** (a) BESS LFP battery racks → battery BMS → Hitachi AMPS PCS bidirectional inverter (~2 MW continuous, ~4 MW peak) → circuit breaker → block 480 VAC bus. (b) Solar 1500 VDC strings → combiner boxes + DC disconnects → DC-AC inverter → circuit breaker → block 480 VAC bus.
7. **Cassette internal (per Cassette-ELEC-001 Rev 1.3).** 480 VAC → Eaton Magnum DS 6,000 A main disconnect → 5 × Delta 660 kW in-row racks (R11–R15, AC-DC rectification) → 800 VDC cassette-internal busway → two branches:
   - **Compute distribution:** 9 × NVL72/CPX compute racks (R1–R9, 230 kW each) + 1 control rack (R10)
   - **Auxiliary:** Munters DSS Pro blowers, Jetson AGX Orin BMS (148 sensor channels)
8. **GPU die.** Direct-to-chip water-glycol cold plate fed by CoolIT CHx2000 CDU (external skid) at ≤45°C.

**Campus posture.** 11 electrically independent blocks. No inter-block MV ring. No inter-block tie (E-23 deferred). Shared services (gas header, water plant, NOC, security, AMCL) span the campus but do not carry power between blocks.

**Key boundaries.** (a) Cassette IP boundary at the cassette 480 VAC main disconnect (Eaton Magnum DS) — everything upstream is vendor-neutral facility infrastructure, everything downstream is cassette IP per BOD §C. (b) Block boundary — each block electrically self-contained. (c) AC bus — the block 480 VAC bus is the convergence point for generation, BESS, solar, and cassette feeds. The 800 VDC bus exists only inside each Cassette.

## 5. Generation (per block)

**4 × Cat CG260-16 gas gensets.** 4,000 ekW continuous per genset at 60 Hz, 900 rpm on natural gas. <250 mg/Nm³ NOx at 5% O₂. 25% hydrogen blending capable (future optionality, not Stage 1 input).

**Why CG260-16:** 4 MW class matches 1:1 genset:cassette ratio at block level. Lean-burn gas with CHP compatibility. US availability and Cat CSA in-region.

**Prime mover rule:** CG260-16 is for Trappey's and 100+ MW deployments. Cat G3520K is for Marlie 1 and ≤10 MW platforms. Not substitutable.

**Loading:** Design anchor 61.5% → 2,460 kW per genset → 9,840 kW per block at 4 running. Block cassette facility load ~9,180 kW (4 × ~2,295 kW). Margin at 61.5%: +660 kW positive. AI dispatch envelope 55–75%; 63–65% expected average.

**Block MV bus at 13.8 kV** (working; Cat CSA to confirm voltage option per E-6). 4 gensets parallel via Cat ECS isochronous sharing. Block MV bus feeds exactly one load: the block step-down transformer.

**Fuel:** ~3,660 Nm³/hr at full block load (100% of 4 × CG260-16). ~2,200 Nm³/hr corresponds to 61.5% anchor loading — not full load. Stage 1 full-load contingency total ~40,300 Nm³/hr across 11 blocks. Pipeline interconnect open.

## 6. Step-down and rectification (per block)

**Block step-down transformer:** one per block, 13.8 kV → 480Y/277 V, ~12–15 MVA continuous, Dyn11, dry-type or cast-resin (no oil handling, lower fire load), Z≈6%. Dedicated to the block; no cross-block sharing. This is the only topological addition vs Marlie — Marlie's G3520K generates 480 VAC directly.

**Cassette 480 VAC primary feeds.**

Each cassette receives its own dedicated 480 VAC feeder from the block switchboard. Feeder sized for cassette facility load (~2,295 kW per cassette). Four feeders per block — ~9.2 MVA total, dominant load on the block transformer secondary.

**In-row power racks (E-24, E-25) — inside Cassette.**

The five Delta 660 kW in-row racks per cassette (R11–R15) are located inside the Cassette boundary per Cassette-ELEC-001 Rev 1.3. They are not separate block-level loads on the 480 VAC bus — they are inside the cassette facility load. Each rack contains 6 × 110 kW PSU shelves (98% AC-DC efficiency), 480 kW aggregate BBU, Power Capacitance Shelf with aluminum caps + supercaps for sub-100 ms GPU swings, EVA variant for peak shaping, touch-safe 800 VDC output.

**Primary vendor: Delta Electronics** per 800 VDC Vendor Comparison scoring (Delta 4.75, Eaton 3.80, Schneider 3.15). Procurement-ready. 5 racks confirmed per cassette (rack-level N+1, 3,300 kW, 59.4% headroom vs 2,070 kW cassette IT).

**Performance spec (vendor-neutral, for RFQ benchmarking):** 480 VAC 3-ph 60 Hz input, 800 VDC single-ended ≤1% ripple output, ≥97% AC-DC at 50–100% load, PF ≥0.99 at rated, THDi ≤5%, integrated BBU for 10+ s cassette full load, integrated supercap for sub-100 ms smoothing, touch-safe EV-heritage output connector, integrated DC fault protection, hot-swap module architecture.

## 7. Block 480 VAC distribution bus

One 480 VAC bus per block. All sources and loads connect here:

- 1 × block step-down transformer secondary (source)
- BESS via Hitachi AMPS PCS bidirectional inverter (source / sink)
- Solar via DC-AC inverter (source)
- 4 × cassette 480 VAC primary feeds (sinks)
- Cooling tower MCC (sink)
- Facility ancillary (sink)

**Bus current at block full load:** ~12,125 A at 9.18 MW cassette load / 480 V (approximate, 3-phase, PF ~1.0). BESS inverter peak injection at 4 MW adds ~4,800 A — bus and main breaker sized to 17,000 A minimum to accommodate simultaneous BESS peak and solar injection.

**Per-cassette feeder:** ~2,760 A at 2,295 kW / 480 V (3-phase). Load-break contactor rated accordingly.

**Sub-100 ms GPU storage** covered by Delta rack-integrated BBU + PCS (inside each Cassette). Facility BESS on the same 480 VAC bus covers sub-second through multi-minute. AC-coupled BESS response via modern SiC-based Hitachi AMPS PCS is sub-cycle.

## 8. BESS — AC-coupled per block

**Role:** Block-level system stabilizer, not backup. Sub-second transient response to genset governor lag. Contingency support for single-genset trip inside the block. Graceful shutdown reserve on gas-supply loss. Solar recapture. Load shifting within AI dispatch envelope.

**Coupling:** AC-coupled to block 480 VAC bus via Hitachi AMPS PCS bidirectional inverter. BESS LFP battery racks connect to PCS DC side; PCS AC side connects to 480 VAC block bus.

**Sizing:** 39.6 MWh facility working (BOD E-10; 11 blocks × 3.6 MWh); 30–50 MWh envelope. Per-block allocation 3.6 MWh working. Contingency scenarios (block-scoped):

| Scenario | Per-block energy | Duration |
|---|---|---|
| Single genset trip inside block | ~1–2 MWh | Seconds to minutes |
| Block partial gas curtailment | ~2–3 MWh | Minutes (graceful ramp-down) |
| Full gas loss — graceful shutdown | ~3–4 MWh | 15–20 min orderly cassette cooldown |

**Power rating:** ~2 MW continuous, ~4 MW peak per block. Across 11 blocks: ~22 MW / ~44 MW peak.

**Chemistry:** LiFePO4. Vendor selection: Fluence, LG Energy Solution Vertech, Saft, Hitachi AMPS. Selection driven by: confirmed AC-coupled compatibility at 480 V, LFP chemistry, 2026–2027 delivery window, Louisiana service.

## 9. Solar — AC-coupled per block

**Array:** First Solar Series 7 CdTe thin-film modules, 2.05 MW DC total across Building 1 and Building 2 rooftops, 1500 VDC string topology.

**Coupling:** 1500 VDC strings → combiner boxes + DC disconnects → DC-AC inverter → circuit breaker → block 480 VAC bus. No DC-DC buck stage. Inverter provides MPPT and anti-islanding disable (island-only operation).

**Allocation per block:** ~186 kW DC on paper (2.05 MW / 11 blocks). Actual allocation driven by rooftop proximity — blocks near B1/B2 receive the physical tie, others carry zero solar. AMCL dispatch models blocks with solar separately.

**Operating role:** Subordinate, supplemental, seasonal/diurnal. Not credited in primary sizing. Displaces genset loading during sunny hours.

## 10. Protection philosophy

**Island-only, block-internal.** No anti-islanding relays, no external sync, no external reverse-power. No campus MV ring → no ring-segment directional overcurrent. Protection coordinates inside each block.

**Per-genset AC protection (E-26):** 87G differential, 32 reverse power, 40 loss of field, 46 negative sequence, 47 phase sequence, 59 overvoltage, 27 undervoltage, 64G stator ground, 78 out-of-step, 51V voltage-restrained overcurrent. Each genset circuit breaker (52-G1 through 52-G4) carries 87G + 51V minimum.

**Block bus:** 87B bus differential, 51N neutral ground.

**Transformer protection (E-27):** 87T overall differential (single two-winding transformer — one differential zone covers both windings), 49T thermal via RTDs, 63 pressure/gas (cast-resin equivalent of Buchholz). Primary breaker (52-TP): 87T + 51 + 50. Secondary breaker (52-TS): 87T + 51 + 50G.

**480 VAC main secondary (E-28):** Solidly grounded wye. 52M main with LSIG trip unit. 50G residual ground sensing at neutral. Insulation resistance monitoring on outgoing feeders.

**Three-stage UFLS** applied at block MV inlet: 59.5 Hz (stage 1), 59.2 Hz (stage 2), 58.9 Hz (stage 3). Shed cassette lanes in priority order; AI dispatch holds shed list current.

**Cassette-internal DC-side protection** per Cassette-ELEC-001 Rev 1.3:

- Solid-state circuit breakers (SSCB) at each Delta rack output to 800 V cassette-internal bus
- Blocking diodes at each source to prevent reverse flow into faulted Delta racks
- Load-break contactor at 480 VAC cassette feed (block side) for isolation
- DC fault protection integrated in Delta racks (vendor-provided)
- Cassette-internal branch protection per Cassette-ELEC-001 Rev 1.3

**Arc flash:** arc-resistant switchgear at block MV bus. Arc-flash reduction on 480 VAC main during maintenance. Detailed study in PROT-001.

## 11. Load envelope (Stage 1)

- Cassette IT: 91.1 MW (44 × 2,070 kW)
- Cassette facility: ~101.0 MW (44 × ~2,295 kW)
- Per block (4 cassettes): ~9,180 kW cassette facility
- Non-cassette ancillary: ~3–5 MW distributed across NOC, security, site lighting, mechanical, BESS aux, SCADA, fire/life safety

**Total Stage 1 site:** ~104–106 MW. Generated at 9,840 kW/block × 11 = 108.24 MW at 61.5% loading. **Margin at 61.5%: +2–4 MW positive.** This is an improvement over Rev 1.2 which showed a negative margin at 61.5%. AI dispatch envelope 63–65% expected average well within comfortable headroom.

**Diversity factor:** 0.95 on IT load (AI control may flatten further; validate in operation).

## 12. AI dispatch interaction (BOD §I / A-09)

**AMCL five-tier architecture** (BOD A-09, Working):

- **L0 field devices** — Cat ECS governors, protection IEDs, VFDs, Jetson Orin BMS, RTDs, CTs/PTs
- **L1 block controller (PLC)** — paralleling, UFLS, BESS inverter setpoints, MPPT, protection trip schemes, safety interlocks. Deterministic, local, cannot be overridden from higher tiers.
- **L2 plant SCADA / data layer** — historian, alarming, OPC-UA backbone, cassette BMS aggregation
- **L3 AMCL dispatch (AI)** — cross-block optimization, gas/load/thermal coupling, solar recapture, BESS orchestration
- **L4 HMI + operator override + cybersecurity** — IEC 62443 segmentation, OT plane isolation, human-in-loop policy gates, incident response

**What AI controls:** per-block genset loading within 55–75%, per-block BESS state (charge/discharge via PCS inverter setpoint), solar MPPT coordination, ancillary dispatch (tower fans, condenser water pumps, makeup water), inter-block load balancing (if E-23 tie added).

**What AI does not control:** protective functions (deterministic, local, cannot be overridden), emergency shutdown (local safety interlocks priority), manual maintenance postures, initial commissioning.

**AI failure mode:** Last-known-good deterministic control. Gensets hold setpoint, BESS PCS holds mode, VFDs hold speed. Governors and protection continue autonomously.

## 13. Single biggest technical risk

**Cat CG260-16 governor response in island-mode 24/7 at variable loading under AI dispatch, paired with block-level AC-coupled BESS (Hitachi AMPS PCS) on 480 VAC bus.**

BESS transient support runs through the Hitachi AMPS PCS inverter. Modern SiC-based inverters respond in sub-cycle (milliseconds), which is adequate for governor support in island-mode operation. The Delta rack-integrated BBU and PCS inside each Cassette handles the sub-100 ms GPU load swing window independently.

**Mitigation path:** Cat CSA engagement — documented governor performance at 55/60/65/70/75% loading. Black-box testing at commissioning. BESS sized conservative enough to ride through governor degradation.

**If Cat CSA returns unfavorable governor data:** add gensets per block (5:4) or oversize BESS. Both engineerable; neither preferred.

## 14. LUS interconnect — explicit no-provisioning

Per BOD E-02: no physical provisioning for LUS on day one. Spatial allocation only. LUS builds at their cost and schedule. No sell-back revenue in base-case financial model.

## 15. Open items and dependencies

**Blocked on Cat CSA:**

- E-5 — CG260-16 factory voltage options (confirm 13.8 kV assumption)
- E-6 — Governor response at island-mode 24/7 duty under AI dispatch
- E-6b — Part-load exhaust temperature, mass flow, jacket water heat rate curves
- E-6c — Maximum exhaust backpressure

**Blocked on vendor RFQs:**

- E-24 / E-25 — Delta 660 kW rack RFQ (racks now inside Cassette; RFQ coordinated through cassette procurement); lead times at 44-cassette and 88-cassette quantities
- E-8 — Block step-down transformer (13.8 kV → 480 V, ~15 MVA) RFQ
- E-10 — BESS vendor RFQ: AC-coupled at 480 V via Hitachi AMPS PCS; per-block 3.6 MWh / 2 MW continuous / 4 MW peak
- E-11 — Block MV switchgear vendor RFQ

**Blocked on contingency analysis:**

- E-10 — Per-block BESS sizing validation (3.6 MWh working)
- E-23 — Inter-block tie decision (11 independent vs inter-block N+1 sharing)

**Blocked on downstream documents:**

- ARCHDIAG-001 — requires update to reflect Rev 1.3 cassette architecture (AC-in, internal Delta racks, no block 800 VDC bus)
- PROT-001 — protection coordination study covering 480 VAC block bus; pickup settings and CT ratios

**Independent:** Gas supply interconnect (gates Block 1 energization). LPDES permitting (no electrical dependency).

## 16. Revision plan

- **Rev 1.3 (current)** — cassette architecture updated to AC-in (480 VAC primary, per Cassette-ELEC-001 Rev 1.3); block-level 800 VDC bus eliminated; BESS and solar AC-coupled; fuel rate corrected (3,660 Nm³/hr full load); bus current sizing updated (17,000 A minimum); transformer protection corrected (87T overall differential); load envelope updated (91.1 MW IT, positive margin at 61.5%)
- **Rev 1.4** — after Cat CSA returns voltage confirmation and governor characterization; locks E-5, E-6
- **Rev 1.5** — after Delta / BESS / solar RFQ closes; locks rack and BESS specs
- **Rev 1.6** — after PROT-001; refines §10 with CT ratios, pickup settings, coord intervals; after ARCHDIAG-001 update
- **Rev 2.0** — ready for external circulation; all C1 dependencies closed

## 17. Approval

Requires Scott's sign-off before downstream electrical documents (SLD, PROT, BESS, SOLAR) can reference it as an architectural anchor.

---

**End of ST-TRAP-ELEC-001 Rev 1.3.**
