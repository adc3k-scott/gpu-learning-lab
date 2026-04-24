# Trappey's AI Center — Engineering Document Index

**Project:** Trappey's AI Center — 91.1 MW Stage 1 / 182.2 MW Full Build AI Compute Facility, Lafayette, Louisiana
**Site:** 22-acre historic cannery, Vermilion River
**Owner:** Scott Tomsu
**Index Revision:** 1.7 — 2026-04-23 (cassette architecture reconciled per BOD Rev 0.6; 480 VAC block bus confirmed; IT load rebased to 91.1 MW / 44 × 2,070 kW; BESS and solar updated to AC-coupled on 480 VAC block bus)
**Status:** Working draft — engineering package in active development

---

## Project Snapshot

| Parameter | Value | Status |
|---|---|---|
| Site | 22-acre Trappey's Cannery, Vermilion River, Lafayette, LA | L |
| Historic structures | 12 nationally registered | L |
| Stage 1 IT load | 91.1 MW (44 cassettes × 2,070 kW) | L |
| Full Build IT load | 182.2 MW (88 × 2,070 kW) | L |
| Stage 1 GPUs | 28,512 NVIDIA Vera Rubin (44 × 648) | W |
| Power architecture | Behind-the-meter permanent island, 480 VAC block bus (cassette-internal 800 VDC only) | L |
| Primary generation | Cat CG260-16 natural gas gensets, 13.8 kV, N+1 per block | W |
| Solar | 1,500 VDC → inverter → 480 VAC block bus | W |
| BESS | AC-coupled LFP via Hitachi AMPS PCS on 480 VAC block bus, always active | W |
| Revenue model | Colocation only, base case | L |

L = Locked · W = Working · O = Open

---

## Master Index

### Master Engineering Package

| Doc # | File | Rev | Date | Description | Status |
|---|---|---|---|---|---|
| ST-TRAP-MASTER-ENG-001 | [TRAP-MASTER-ENG-001_Rev0.4.md](TRAP-MASTER-ENG-001_Rev0.4.md) | **0.4** | **2026-04-23** | **Master Engineering Package** — single consolidated summary of the full project engineering state. Executive summary, site/project basis (BOD ledger), power architecture, BESS, solar, thermal, CHP cascade (heat balance table), cooling tower field (GPU warm water via PHX-001), master open items list (C1/C2), full document register, and 22-milestone critical path to construction package. Cassette architecture reconciled 2026-04-23: 480 VAC block bus, 91.1 MW IT load, AC-coupled BESS/solar, CoolIT CHx2000 CDU, 72.9 MW tower duty. Internal use only. | Working draft |

---

### 00-Basis — Design Foundations

| Doc # | File | Rev | Date | Description | Status |
|---|---|---|---|---|---|
| ST-TRAP-BOD-001 | [TRAP-BOD-001_Rev0.6.md](TRAP-BOD-001_Rev0.6.md) | **0.6** | **2026-04-23** | **Basis of Design** — single source of truth for all design parameters. Contains the Decision Ledger (P, R, E, T, B, S, A, N sections) with Locked / Working / Open tags. Cassette architecture reconciled 2026-04-23: 480 VAC block bus, cassette-internal 800 VDC only, IT load 91.1 MW (44 × 2,070 kW), BESS/solar AC-coupled at 480 VAC bus. Downstream documents cite this; all value changes flow through here. | Working draft |
| ST-TRAP-THERMAL-BASIS | [ST-TRAP-THERMAL-BASIS_Rev0.5.md](ST-TRAP-THERMAL-BASIS_Rev0.5.md) | **0.5** | **2026-04-22** | **Thermal Architecture Basis** — cold sink architecture and CHP cascade framework. Absorption chiller eliminated. Cooling towers serve GPU warm water via plate HX. Munters exhaust recovery 5.5 MW only. Vermilion River eliminated. Rev 0.6 rebase to 72.9 MW tower duty in progress. | Working draft |

---

### 01-Electrical — Power Architecture

| Doc # | File | Rev | Date | Description | Status |
|---|---|---|---|---|---|
| ST-TRAP-ELEC-001 | [Trap-ELEC-001_Rev1.3.md](Trap-ELEC-001_Rev1.3.md) | **1.3** | **2026-04-23** | **Electrical Architecture** — N replicated Marlie-pattern blocks. Each block: 4 × Cat CG260-16 at 13.8 kV → step-down transformer → 480 VAC switchboard → 4 × cassette 480 VAC primary feeds. Cassette-internal 5 × Delta 660 kW in-row racks (R11–R15) convert 480 VAC → 800 VDC internally. BESS and solar AC-coupled to block 480 VAC bus via Hitachi AMPS PCS and PV inverter respectively. Five feeder categories, AMCL five-tier control architecture. Visual companion: ARCHDIAG-001 Rev 0.1. | Working draft |

---

### 02-Bess — Battery Energy Storage

| Doc # | File | Rev | Date | Description | Status |
|---|---|---|---|---|---|
| ST-TRAP-BESS-001 | [TRAP-BESS-001_Rev0.1.md](TRAP-BESS-001_Rev0.1.md) | ~~0.1~~ | 2026-04-17 | **BESS Architecture Basis** — ~~Rev 0.1 superseded by BOD Rev 0.6. DC-coupled 800 VDC architecture no longer current. Rev 0.2 rewrite for AC-coupled 480 VAC block bus topology in progress.~~ | **Superseded — Rev 0.2 in progress** |
| ST-TRAP-BESS-ARCHDIAG-001 | [TRAP-BESS-ARCHDIAG-001_Rev0.1.md](TRAP-BESS-ARCHDIAG-001_Rev0.1.md) | ~~0.1~~ | 2026-04-17 | **BESS Architecture Diagram Package** — ~~Rev 0.1 superseded by BOD Rev 0.6. Five Mermaid diagram rebuild for AC-coupled 480 VAC topology in progress.~~ | **Superseded — Rev 0.2 in progress** |
| ST-TRAP-BESS-RFQ-001 | [ST-TRAP-BESS-RFQ-001_Rev0.1.md](ST-TRAP-BESS-RFQ-001_Rev0.1.md) | ~~0.1~~ | 2026-04-18 | **BESS Vendor RFQ Package** — ~~**DO NOT DISTRIBUTE Rev 0.1.** Specifies DC-coupled 800 VDC bus topology, superseded by BOD Rev 0.6. Rev 0.2 rewrite required before vendor distribution.~~ | **Superseded — do not distribute** |

---

### 03-Architecture — Electrical Diagram Package

| Doc # | File | Rev | Date | Description | Status |
|---|---|---|---|---|---|
| ST-TRAP-ARCHDIAG-001 | [ST-TRAP-ARCHDIAG-001_Rev0.1.md](03-Architecture/ST-TRAP-ARCHDIAG-001_Rev0.1.md) | 0.1 | 2026-04-17 | **Electrical Architecture Diagram Package (MD)** — six-diagram end-to-end SLD: orientation overview, four domain zooms (MV AC · LV AC + in-row rack · 800 VDC + DER · cassette internal), combined AMCL controls + 11-block campus view. Mermaid syntax. Architectural, not construction-issue. | Working draft |
| ST-TRAP-ARCHDIAG-001 | [ST-TRAP-ARCHDIAG-001_Rev0.1-1.pdf](03-Architecture/ST-TRAP-ARCHDIAG-001_Rev0.1-1.pdf) | 0.1 | 2026-04-17 | **Same package as PDF** — polished layout with page breaks between diagrams. Use for external distribution. 1.5 MB. | Working draft |
| ST-TRAP-ARCHDIAG-001 | [ST-TRAP-ARCHDIAG-001_Rev0.1(1).docx](03-Architecture/ST-TRAP-ARCHDIAG-001_Rev0.1(1).docx) | 0.1 | 2026-04-17 | **Same package as Word** — editable source. 1.6 MB. | Working draft |

---

### 09-Solar — Solar Integration

| Doc # | File | Rev | Date | Description | Status |
|---|---|---|---|---|---|
| ST-TRAP-SOLAR-001 | [ST-TRAP-SOLAR-001_Rev0.1.md](ST-TRAP-SOLAR-001_Rev0.1.md) | ~~0.1~~ | 2026-04-18 | **Solar Array Integration — Architecture and Specification Basis** — First Solar FS-7550A-TR1, 3,731 panels, 2.05 MW DC, B1/B2 rooftops. String voltage analysis (§1–§5) valid and unchanged. ~~§6 DC-DC buck spec superseded by BOD Rev 0.6: 1,500 VDC strings → PV inverter → 480 VAC block bus. Rev 0.2 rewrite of §6–§7 in progress.~~ | **§6–§7 superseded — Rev 0.2 in progress** |

---

### 04-Drawings — Site and System Drawings

#### Current drawings (PNG set — 2026-04-17)

| File | Description |
|---|---|
| [d1.png](04-Drawings/d1.png) | Drawing 1 of 6 |
| [d2.png](04-Drawings/d2.png) | Drawing 2 of 6 |
| [d3.png](04-Drawings/d3.png) | Drawing 3 of 6 |
| [d4.png](04-Drawings/d4.png) | Drawing 4 of 6 |
| [d5.png](04-Drawings/d5.png) | Drawing 5 of 6 |
| [d6.png](04-Drawings/d6.png) | Drawing 6 of 6 |

#### Archived drawings (`old/` — SVG set, 2026-03-25, superseded)

| File | Description |
|---|---|
| [old/cooling-schematic.svg](04-Drawings/old/cooling-schematic.svg) | Cooling system schematic — superseded |
| [old/electrical-sld.svg](04-Drawings/old/electrical-sld.svg) | Electrical single-line diagram — superseded |
| [old/floor-plan.svg](04-Drawings/old/floor-plan.svg) | Floor plan — superseded |
| [old/power-distribution.svg](04-Drawings/old/power-distribution.svg) | Power distribution diagram — superseded |
| [old/site-plan.svg](04-Drawings/old/site-plan.svg) | Site plan — superseded |
| [old/solar-layout.svg](04-Drawings/old/solar-layout.svg) | Solar array layout — superseded (428 KB) |

---

### 07-Thermal — Thermal System Specifications

| Doc # | File | Rev | Date | Description | Status |
|---|---|---|---|---|---|
| ST-TRAP-CHP-SCHEMATIC-001 | [ST-TRAP-CHP-SCHEMATIC-001_Rev0.2.md](07-Thermal/ST-TRAP-CHP-SCHEMATIC-001_Rev0.2.md) | **0.2** | **2026-04-22** | **CHP Cascade Schematic Package** — three Mermaid diagrams revised: (1) end-to-end cascade genset → Munters (5,500 kW) + stack; JW → radiators; Boyd CDU → PHX-001 → towers, (2) exhaust split, (3) isolated cooling circuits (CDU + tower via PHX). Absorption chiller and HRU eliminated. Heat balance summary table updated. | Working draft |
| ST-TRAP-COOLING-TOWER-001 | [ST-TRAP-COOLING-TOWER-001_Rev0.2.md](07-Thermal/ST-TRAP-COOLING-TOWER-001_Rev0.2.md) | **0.2** | **2026-04-22** | **Cooling Tower Field — Vendor Specification Basis** — GPU warm water is sole tower load (80.96 MW Stage 1 / 161.9 MW Full Build). Plate HX PHX-001 as facility boundary between CDU circuit and tower circuit. Design WB 28°C; tower supply ≤34°C; flow ~30,700 GPM; 3 cells (~23,020 RT); makeup ~830 GPM; cooling MCC ~1,500 kW total. SPX/Marley + BAC + Evapco shortlist. Chiller-specific items cancelled. | Working draft |

---

### 05-Photos — Site Photography

**Total:** ~120 files. Organized by subject group below.

| Group | Files | Description |
|---|---|---|
| Front exterior | Front1–5.jpg | Building frontage shots |
| Middle buildings | Middle1–4.jpg, Middle_high_5–8.jpg, Middle_low_1–4.jpg, Middle3.jpg | Mid-campus structures, high and low angles |
| Rear warehouse | Rear_warehouse1–6.jpg | Rear warehouse exterior and interior |
| Riverfront | Riverfront_1–6.jpg, Riverfront_8.jpg | Vermilion River frontage |
| Water tower | WT1–3.jpg, restoration-water-tower-before.jpg | Water tower — before restoration |
| Power infrastructure | E_Grid1–4.jpg, Power1–2.jpg | LUS/SLEMCO grid, existing power equipment |
| Gas infrastructure | ATMOS_Gas_by_Pinhook.jpg | ATMOS gas line near Pinhook Rd |
| Cassette House (ch-) | ch-back-exit.jpg, ch-ceiling.jpg, ch-front-after.jpg, ch-front-before.jpg, ch-front-entrance.jpg, ch-interior-rendering.jpg, ch-modules-*.jpg, ch-site-block.jpg | Cassette House concept — before/after, interior, module layout |
| Slide deck set | slide_01–20.jpg | Presentation-ready photos (ordered sequence) |
| Historical Trappeys | 1946TrappeysDehydratedSweetPotatoesAdvertisement.webp, trappeysbeans.webp, trappeysyams.webp, 6052359*.webp/jpg (×11) | Historical Trappeys brand and facility photos |
| Document-extracted | p01–p14 series (PNG/JPG) | Images extracted from source documents |
| three-pic.jpg | — | Three-panel composite |

---

### 06-Renders — AI-Generated Visualizations

**Total:** 50 files. Do not use for construction documents.

| Series | Files | Description |
|---|---|---|
| v1 / flux | flux-trappeys-aerial.jpg | Early Flux T2I aerial render |
| v1 named | trappeys-800v-switchgear.jpg, trappeys-building3-interior.jpg, trappeys-campus-aerial-sunset.jpg, trappeys-dry-cooler.jpg, trappeys-entrance-restored.jpg, trappeys-fiber-optic.jpg, trappeys-first-solar-panels.jpg, trappeys-front-restored.jpg, trappeys-front-wide.jpg, trappeys-infrastructure-yard.jpg, trappeys-night-exterior.jpg, trappeys-nvl72-server-room.jpg, trappeys-riverwalk.jpg, trappeys-solar-rooftop.jpg, trappeys-water-tower-cooling.jpg, trappeys-watertower-restored.jpg, trappeys-warehouse-interior.jpg | First-pass renders — key site elements |
| v2 | v2-trappeys-*.jpg (×15) | Second-pass renders — improved quality, full campus coverage including NVIDIA meeting room, war room |
| v3 | v3-trappeys-from-bank-*.jpg (×5), v3-trappeys-solar-roof-*.jpg (×2) | River-bank perspective set, solar roof aerials |
| v4 | v4-warehouse-after-1–5.jpg, v4-warehouse-before-after.jpg | Warehouse before/after transformation series |
| Kontext | kontext-29-full-vision.jpg, kontext-29-servers-inside.jpg | Kontext photo-edit renders from real building photos |
| CH renders | trappeys-middle-front-render.jpg, trappeys-middle3-render.jpg, trappeys-museum-rendering.jpg | Cassette House and museum rendering set (2026-04-03) |

---

## Document Dependency Map

```
BOD-001 Rev 0.6  ──────────────────────────────────────────┐
│                                                           │
├── THERMAL-BASIS Rev 0.5  (T-xx ledger)                   │
│   ├── CHP-SCHEMATIC-001 Rev 0.2  (07-Thermal/)           │
│   ├── COOLING-TOWER-001 Rev 0.2  (07-Thermal/)           │
│   └── [RIVER-001 cancelled — Vermilion River eliminated]  │
│                                                           │
├── ELEC-001 Rev 1.3  (E-xx ledger)  ◄── eng-pack-5MW      │
│   ├── ARCHDIAG-001 Rev 0.1  (visual companion)           │
│   │   ├── [pending] ST-TRAP-SLD-001                      │
│   │   └── [pending] ST-TRAP-PROT-001                     │
│   ├── BESS-001 Rev 0.1  (E-10 to E-13)                   │
│   │   ├── BESS-ARCHDIAG-001 Rev 0.1  (visual companion)  │
│   │   └── ST-TRAP-BESS-RFQ-001 Rev 0.1  (02-Bess/) ✓     │
│   └── ST-TRAP-SOLAR-001 Rev 0.1  (09-Solar/) ✓          │
│                                                           │
└── [pending] ST-TRAP-SLD-001, ST-TRAP-PROT-001            │
```

---

## Open Engineering Items (as of 2026-04-22)

| ID | Item | Blocking |
|---|---|---|
| PHX-001 | Plate HX sizing + vendor RFQ (Alfa Laval / GEA / API) — ~72.9 MW Stage 1 | COOLING-TOWER-001 CW temp confirmation; tower RFQ |
| Cat CSA | CG260-16 part-load exhaust temp / mass-flow / JW curves; N-1 governor; CO emissions | T-08 heat balance; JW-RAD sizing; E-31 CO baseline |
| T-05 | Cooling tower type selection (wet / hybrid / adiabatic) — GPU warm water basis | Tower RFQ |
| JW-RAD | Jacket water radiator vendor + sizing RFQ (~58,212 kW) | CHP cascade JW path |
| E-31 | CO oxidation catalyst — control strategy for Title V major-source path | LDEQ Title V pre-app |
| E-23 | Inter-block tie — 11 independent vs. tied at aux point | ELEC-001 §15 |
| SHPO R-05/R-06 | Historic Tax Credit Part 1 / Part 2 filing | HTC financing |
| SLD-001 | Formal single-line — not yet drafted | Construction package |
| PROT-001 | Protection coordination study — not yet drafted | Construction package |
| ~~SOLAR-001~~ | ~~Issued~~ — ST-TRAP-SOLAR-001 Rev 0.1 in 09-Solar/ | — |
| ~~BESS-RFQ-001~~ | ~~Issued~~ — ST-TRAP-BESS-RFQ-001 Rev 0.1 in 02-Bess/ | — |
| ~~TB-5~~ | ~~Absorption chiller RFQ~~ | **CANCELLED 2026-04-22** |
| ~~T-11~~ | ~~Boyd CDU CHW compatibility~~ | **CANCELLED 2026-04-22** |
| ~~COND-WB~~ | ~~Broad chiller condenser water inlet~~ | **CANCELLED 2026-04-22** |

---

## Pending Documents (not yet in this folder)

| Doc # | Description |
|---|---|
| ST-TRAP-SLD-001 | Formal single-line diagram (inherits ARCHDIAG-001 + ELEC-001) |
| ST-TRAP-PROT-001 | Protection coordination study |
~~ST-TRAP-SOLAR-001~~ | Issued Rev 0.1 — see 09-Solar/ |
~~ST-TRAP-BESS-RFQ-001~~ | Issued Rev 0.1 — see 02-Bess/ |

---

## Revision Log

| Rev | Date | Author | Summary |
|---|---|---|---|
| 1.0 | 2026-04-18 | Scott Tomsu | Initial index created. Folder restructured from flat `blueprints/` + `md files/` layout to numbered folders 00–06. Old SVG drawings archived to `04-Drawings/old/`. Six engineering documents at current rev levels indexed. Open items and pending document list populated. |
| 1.1 | 2026-04-18 | Scott Tomsu | ST-TRAP-THERMAL-BASIS_Rev0.4.md drafted and added to 00-Basis. First issue of thermal architecture basis — CHP cascade framework, Option B vs C analysis, Broad/Cat data, Munters accounting. Vermilion River eliminated as heat sink (tidal reversal + Gulf Coast ambient temps); dry cooling tower confirmed as sole rejection path. RIVER-001 cancelled; LPDES item removed. TB-5 and T-11 remain open. |
| 1.2 | 2026-04-18 | Scott Tomsu | ST-TRAP-COOLING-TOWER-001_Rev0.1.md drafted and added to new 07-Thermal/ folder. First issue of cooling tower field spec — maximum duty 241.4 MW / 68,640 RT, nominal staged 183.9 MW. System boundary established (absorption chiller condenser only; Boyd CDU GPU warm water to separate dry cooler). Tower type analysis complete (wet mechanical draft recommended). COND-WB approach temperature gap documented (31°C practical vs 29°C Broad rated). Water consumption ~2,476 GPM makeup at design day. Infrastructure yard siting flag raised. COOLING-TOWER-001 removed from pending documents; dependency map updated. |
| 1.3 | 2026-04-18 | Scott Tomsu | ST-TRAP-CHP-SCHEMATIC-001_Rev0.1.md drafted and added to 07-Thermal/. Three Mermaid diagrams: full cascade overview, Option B/C exhaust branch, isolated cooling water loops. Heat balance summary table. Visual companion to THERMAL-BASIS and COOLING-TOWER-001. |
| 1.4 | 2026-04-18 | Scott Tomsu | ST-TRAP-BESS-RFQ-001_Rev0.1.md drafted and added to 02-Bess/. Procurement-ready vendor RFQ — LFP DC-coupled, 11 × 3.6 MWh working (3/4/5 MWh tiers), 2 MW continuous / 4 MW peak, 800 VDC island-mode. SiC DC-DC spec, NFPA 855/UL 9540A requirements, AMCL comms interface, evaluation criteria, Fluence-first vendor sequence. Portfolio context (~100+ containers ADC sites). BESS-RFQ-001 removed from pending documents. |
| 1.5 | 2026-04-18 | Scott Tomsu | ST-TRAP-SOLAR-001_Rev0.1.md drafted and added to new 09-Solar/ folder. First Solar FS-7550A-TR1, 3,731 panels, 2.05 MW. String voltage analysis complete — 5-panel strings confirmed >800V MPP across full Louisiana temperature range. DC-DC buck spec issued (E-22). ITC basis documented. SOLAR-001 removed from pending documents. |
| 1.6 | 2026-04-22 | Scott Tomsu | Absorption chiller eliminated; thermal architecture revised to cooling-tower-primary with CHP serving Munters only. BOD Rev 0.5, MASTER-ENG Rev 0.3, CHP-SCHEMATIC Rev 0.2, COOLING-TOWER Rev 0.2, THERMAL-BASIS Rev 0.5 all issued. Document register updated. |
| 1.7 | 2026-04-23 | Scott Tomsu | Cassette architecture reconciled — 480 VAC block bus confirmed per BOD Rev 0.6 and ELEC-001 Rev 1.3. IT load rebased to 91.1 MW (44 × 2,070 kW). GPU count updated to 28,512 (44 × 648). BESS updated to AC-coupled via Hitachi AMPS PCS on 480 VAC block bus. Solar updated to PV inverter coupling. CoolIT CHx2000 replaces Boyd CDU reference. Tower duty rebased to ~72.9 MW. BESS-001, BESS-ARCHDIAG, BESS-RFQ, SOLAR-001 Rev 0.1 all marked superseded pending Rev 0.2 rewrites. |

---

*All documents are working drafts unless marked Locked in BOD-001. Do not cite values from any document without confirming BOD-001 ledger status.*
