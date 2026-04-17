# ST-TRAP-ARCHDIAG-001 — Electrical Architecture Diagram Package — Rev 0.1

**Document:** Electrical Architecture Diagram Package
**Project:** Trappey's AI Center, Lafayette, Louisiana
**Revision:** 0.1 — first issue; companion to ELEC-001 Rev 1.2 and BOD-001 Rev 0.4
**Date:** April 17, 2026
**Owner:** Scott Tomsu
**Status:** Working draft

**Also issued as:** `ST-TRAP-ARCHDIAG-001_Rev0.1.pdf` and `ST-TRAP-ARCHDIAG-001_Rev0.1.docx` (visual layout with page breaks between diagrams).

---

## 1. Purpose

Visual companion to ST-TRAP-ELEC-001 Rev 1.2 and ST-TRAP-BOD-001 Rev 0.4. Captures the end-to-end electrical path of one Marlie-pattern block at Trappey's — from natural gas genset through MV paralleling, LV AC distribution, AC-DC conversion at the in-row power rack, 800 VDC common busway with DC-coupled BESS and solar, cassette umbilical, and cassette-internal distribution to the Vera Rubin GPU die.

Six diagrams: one orientation overview, four domain zooms (MV AC · LV AC + in-row rack · 800 VDC + DER · cassette internal), and a combined AMCL controls + 11-block campus view.

**This package is architectural, not construction-issue.** CT/PT designations, conductor sizing, breaker frame sizes, and trip settings belong in ST-TRAP-SLD-001 (formal single-line, not yet drafted) and ST-TRAP-PROT-001 (protection coordination study, not yet drafted). Those documents inherit the topology shown here.

## 2. Relationship to other documents

**Upstream (this package inherits from):**

- ELEC-001 Rev 1.2 — architecture anchor
- BOD-001 Rev 0.4 — ledger authority for every value
- eng-pack-5MW Rev 3.x — Marlie block reference
- 800 VDC Vendor Comparison sheet — Delta vs Eaton vs Schneider procurement analysis

**Downstream (inherits from this package):**

- ST-TRAP-SLD-001 — formal single-line
- ST-TRAP-PROT-001 — protection coordination study
- ST-TRAP-BESS-001 — DC-coupled BESS procurement spec
- ST-TRAP-SOLAR-001 — solar integration with DC-DC buck selection

## 3. Conventions — domain color coding

| Color | Domain | Elements |
|---|---|---|
| Blue | MV AC (13.8 kV) | Gensets, generator breakers, MV bus, paralleling switchgear, transformer primary |
| Amber | LV AC (480 V) | Transformer secondary, 480 VAC main, feeders, in-row rack AC side |
| Teal | 800 VDC | Common busway, SSCBs, blocking diodes, cassette umbilicals, overhead busbar |
| Purple | BESS / compute | LFP battery racks, bidirectional DC-DC, cassettes, ORV3/Kyber PDUs |
| Green | Solar / PV | First Solar array, combiners, DC-DC buck |
| Pink | Controls / GPU tray | AMCL tiers, sub-100 ms storage (PCS), NVL72 tray detail |
| Gray | Neutral / shared | Gas header, shared campus services, protection reference tables |

---

## 4. Diagram 1 — Block overview: generator to GPU

One of eleven identical Marlie-pattern blocks, end to end. Top-down: natural gas header → 4 × CG260-16 gensets → 13.8 kV MV bus (paralleled) → step-down transformer → 480 VAC main → in-row power racks (4 per cassette) → 800 VDC busway (with BESS and Solar PV as side taps) → 4 cassette umbilicals → 2,880 Vera Rubin GPUs per block.

![Block overview: generator to GPU](d1.png)

## 5. Diagram 2 — MV AC detail: protection and paralleling

MV AC-side detail for one block. Per-genset protection relay set (87G differential, 32 reverse power, 40 loss of excitation, 46 negative sequence, 47 phase sequence, 59/27 over/undervoltage, 64G stator ground, 78 out-of-step); neutral grounding resistor callout; generator circuit breakers; paralleling to 13.8 kV block bus with Cat ECS isochronous sharing and 87B bus differential; three-stage UFLS at 59.5 / 59.2 / 58.9 Hz at the block MV inlet; step-down transformer with 87T primary + secondary differential and 49T thermal; secondary main with LSIG trip and 50G residual ground. ANSI device number legend at the bottom.

![MV AC detail: protection and paralleling](d2.png)

## 6. Diagram 3 — LV AC distribution and in-row rack internals

**Upper half — 480 VAC main switchboard** with five feeders:

- 16 × in-row power racks (~10.6 MVA — the dominant feeder)
- Cooling plant MCC (~600 kW, VFD-driven: absorption chiller solution pumps, condenser water pumps, tower makeup pumps, tower fans, adiabatic spray, Vermilion intake)
- BESS auxiliary (~80 kW: HVAC, BMS, fire)
- Solar buck auxiliary (~10 kW: controls, HVAC)
- Facility ancillary (~200 kW: SCADA, NOC, life safety)

**Lower half — one Delta 660 kW in-row power rack exploded:** six 110 kW PSU shelves at 98% AC-DC efficiency, 80 kW BBU per shelf (480 kW aggregate BBU), Power Capacitance Shelf with aluminum caps + supercaps to close the sub-100 ms GPU load-swing band, EVA variant for peak shaping, integrated DC fault protection, touch-safe 800 VDC output with mechanical interlock per NVIDIA MGX.

![LV AC distribution and in-row rack internals](d3.png)

## 7. Diagram 4 — 800 VDC common bus, BESS, solar, cassette umbilicals

Three DC sources converge on the 800 VDC common busway: in-row rack output (rectified from 480 VAC, integrated BBU and PCS storage), DC-coupled BESS via a bidirectional DC-DC converter (~2 MW continuous, ~4 MW peak, SiC-based), and DC-coupled solar via 1500→800 V buck with MPPT. SSCB + blocking diode at every source tie enforces DC-domain protection discipline. Four cassette umbilicals exit via load-break contactors and additional SSCBs. The bus carries approximately 12,075 A at full block load (9,660,000 W ÷ 800 V).

![800 VDC bus, BESS, solar, cassette umbilicals](d4.png)

## 8. Diagram 5 — Cassette internal distribution: umbilical to GPU

Inside one cassette. The 800 VDC umbilical (~3,000 A at 2,415 kW facility load) enters through a Staubli hot-swap disconnect at the cassette IP boundary — where vendor-neutral facility infrastructure ends and cassette IP begins per BOD C.10. The overhead busbar feeds two branches:

- **Main DC distribution:** 3 × Eaton ORV3 PDUs + NVIDIA Kyber PDUs → 10 × OCP ORV3 racks at 230 kW each = 2,300 kW cassette IT
- **Auxiliary DC-DC:** Boyd CDU pumps (2,000 kW water-glycol loop), Munters HCD/MCD blowers, Jetson AGX Orin BMS (148 channels)

One rack is expanded to show the NVL72 tray with 72 Vera Rubin GPUs, 288 GB HBM4 each (20.7 TB per rack), direct-to-chip water-glycol cooling with Boyd CDU supply ≤45°C.

![Cassette internal: umbilical to GPU](d5.png)

## 9. Diagram 6 — AMCL controls and campus replication

**Upper half — five-tier AMCL control hierarchy:**

- **L0 field devices** — Cat ECS governors, protection IEDs, VFDs, Jetson Orin BMS, RTDs, CTs/PTs
- **L1 block controller (PLC)** — genset paralleling, UFLS, DC-DC setpoints, MPPT, protection trip schemes, safety interlocks (deterministic, local)
- **L2 plant SCADA / data layer** — historian, alarming, OPC-UA backbone, cassette BMS aggregation
- **L3 AMCL dispatch (AI)** — cross-block optimization, gas/load/thermal coupling, solar recapture, BESS orchestration
- **L4 HMI + operator override + cybersecurity** — IEC 62443 segmentation, OT plane isolation, human-in-loop policy gates, incident response

**Lower half — campus replication.** Shared services (gas header, water plant, NOC/SCADA, security, LUS-future tie) above 11 electrically independent blocks. E-23 inter-block tie for shared N+1 is a future option, not base case.

![AMCL controls and campus replication](d6.png)

---

## 10. Engineering notes

### 10.1 Anchored directly in ELEC-001 Rev 1.2 / BOD-001 Rev 0.4

- 4 × Cat CG260-16 gensets per block, 4,000 ekW each at 13.8 kV, isochronous paralleling via Cat ECS (E-03, E-04)
- Per-block step-down transformer 13.8 kV Δ → 480Y/277 V, ~15 MVA (E-08)
- In-row power racks at cassette; Delta 660 kW primary vendor per 4.75/5 score; 4 per cassette base, 5 for rack-level N+1 (E-24, E-25)
- Single 800 VDC common busway per block, single-ended, SSCB + blocking diodes at every source tie (E-18, E-22)
- DC-coupled BESS on 800 VDC bus via bidirectional DC-DC, LFP, 40 MWh facility (E-10, E-11, E-12, E-13)
- DC-coupled solar via 1500 VDC → buck → 800 VDC bus; First Solar Series 7 at 2.05 MW (E-14 through E-17)
- Three-stage UFLS at 59.5 / 59.2 / 58.9 Hz on block MV inlet; island-only posture (E-18, E-19)
- Integrated sub-100 ms GPU storage in in-row rack (BBU + PCS), closes NVIDIA MGX dual-layer storage (E-20)
- Touch-safe EV-heritage 800 VDC connectors with mechanical interlock (E-21)
- Staubli hot-swap at cassette boundary (C-22); 3 × Eaton ORV3 + Kyber PDUs inside (C-18); 10 × ORV3 racks, 720 GPUs per cassette (C-11, C-12)
- Boyd CDU 2,000 kW water-glycol, direct-to-chip, ≤45°C (C-03, C-04)
- 11 electrically independent blocks, no campus MV ring (E-07); inter-block tie deferred as E-23
- Generator protection relay set per E-26; transformer protection per E-27; LV grounding per E-28; 480 VAC feeder categories per E-29; cassette internal topology per E-30; AMCL five-tier per A-09

### 10.2 Filled in with standard engineering practice

These items are not locked in source documents but drawn with industry-standard values for a paralleled gas-genset permanent island. Expected to become Working entries in BOD-001 Rev 0.5 and then Locked after RFQs close.

- Cooling MCC feeder sized at ~600 kW — order-of-magnitude pending CHP heat balance (T-08). Real number sizes with absorption chiller solution pumps, tower fans, condenser water pumps, makeup pumps, and Vermilion intake.
- BESS aux ~80 kW, facility ancillary ~200 kW — placeholders within BOD §D.2 "3-5% of IT load" band.
- Arc-resistant MV switchgear, arc-flash reduction on LV main during maintenance.
- Five-tier AMCL template is a working architecture consistent with ISA-95 for industrial control systems; BOD §I calls out AI dispatch as operating model but leaves the layered architecture open.

### 10.3 Still open per source documents

These gate progression to Rev 1.0 of the architectural documents:

- CG260-16 factory MV voltage option (13.8 kV working, pending Cat CSA — E-5, E-6)
- CG260-16 governor response at island-mode 24/7 under AI dispatch — the single biggest technical risk per ELEC-001 §13
- CHW temperature compatibility between LiBr chiller (7–12°C) and Boyd CDU (T-11, C1 open)
- Inter-block tie for shared N+1 (E-23) — base case is 11 independent blocks
- Cassette-internal auxiliary DC-DC specifics for Boyd CDU pumps, Munters blowers, Jetson BMS — cassette IP decision not yet locked
- CHP heat balance including 5.5 MW Munters slip-stream deduction (T-08, T-12) — gates tower sizing and thus cooling MCC feeder sizing

### 10.4 Design choices subject to revision

- **In-row rack count:** 4 × Delta 660 kW (2,640 kW, 9.3% headroom) is the base spec; 5 × Delta 660 kW (3,300 kW, 36.6% headroom) gives rack-level N+1 — preferred for 24/7 duty if vendor-comparison scoring holds. Alternative: 3 × Delta 1.1 MW per cassette. Rev 1.4 of ELEC-001 will lock after RFQ closes.
- **Transformer MVA:** 15 MVA is comfortable at 9.66 MW cassette load + 1 MW ancillary + BESS charging headroom. 12 MVA is tight and will be limited by absorbed reactive power during paralleling transients. RFQ-dependent.
- **Per-block BESS:** 3.6 MWh is 40 MWh / 11 blocks. Envelope is 3–5 MWh (§8); contingency analysis refines. If single-genset-trip scales higher or gas-loss graceful shutdown requires >15 minutes, per-block BESS scales up.
- **Solar allocation:** 186 kW per block is uniform math. Actual allocation driven by rooftop proximity — B1/B2-adjacent blocks receive physical tie, others zero. Affects AMCL dispatch modeling, not individual block design.
- **480 VAC secondary grounding:** solidly grounded wye drawn. High-resistance grounding preserves uptime on first-fault at cost of additional ground-fault detection complexity. Worth reconfirming with insurance underwriters given 800 VDC downstream.

---

## 11. Open items ledger

Blocked on external validation (vendor RFQ, Cat CSA, thermal engineering) or on downstream documents not yet drafted. Priority codes follow BOD-001 §M convention.

| Ref | Item | Blocked on | Priority |
|---|---|---|---|
| E-05 | CG260-16 nominal loading (61.5% working) | Cat CSA | C1 |
| E-06 | CG260-16 factory MV voltage option (13.8 kV assumed) | Cat CSA | C1 |
| E-06 | Governor response at island-mode 24/7 under AI dispatch | Cat CSA black-box test | C1 |
| E-08 | Block step-down transformer RFQ (~15 MVA working) | Vendor RFQ | C1 |
| E-24 / E-25 | In-row power rack count per cassette (4 vs 5 for N+1) | Delta / Eaton / Schneider RFQ | C1 |
| E-10 | BESS per-block sizing (3.6 MWh working, 3-5 envelope) | Contingency analysis | C1 |
| E-22 | Solar DC-DC buck converter vendor selection | Vendor RFQ | C2 |
| E-23 | Inter-block tie for shared N+1 (base case 11 independent) | Contingency analysis | C2 |
| T-11 | Chiller CHW supply temperature vs Boyd CDU requirement | Chiller + Boyd spec confirmation | C1 |
| T-08 | CHP heat balance including Munters slip-stream | Thermal engineering | C1 |
| PROT-001 | Protection coordination across AC-DC boundary | Downstream document | C1 |
| SLD-001 | Formal single-line with CT/PT designations and conductor sizing | Downstream document | C1 |
| GAS | Gas supply interconnect (gates Block 1 energization) | Pipeline agreement | C1 |

## 12. Revision plan

- **Rev 0.1 (current)** — first issue. Companion to ELEC-001 Rev 1.2, BOD-001 Rev 0.4.
- **Rev 0.2** — after Cat CSA returns voltage confirmation and governor characterization. Updates MV voltage annotation on Diagrams 1 and 2.
- **Rev 0.3** — after 800 VDC vendor RFQs close. Updates Diagrams 1 and 3 with locked in-row rack vendor, per-rack kW rating, rack count per cassette.
- **Rev 0.4** — after BESS RFQ closes. Updates Diagram 4 BESS annotations with locked bidirectional DC-DC specifics.
- **Rev 0.5** — after PROT-001 completes. Updates Diagram 2 with locked CT ratios, pickup settings, coordination intervals.
- **Rev 1.0** — ready for external circulation. All C1 dependencies closed. Paired with SLD-001 Rev 1.0 and PROT-001 Rev 1.0.

## 13. Approval

Rev 0.1 does not carry external circulation approval. Architecture sign-off inherits from ELEC-001 Rev 1.2 and BOD-001 Rev 0.4 approval status. External distribution waits for Rev 1.0, gated on all C1 external dependencies closing per BOD-001 §M.

---

**End of ST-TRAP-ARCHDIAG-001 Rev 0.1.**
