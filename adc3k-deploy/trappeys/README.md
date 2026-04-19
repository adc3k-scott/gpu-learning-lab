# Trappey's Compute Campass — Engineering Document Index

**Project:** Trappey's 200MW Solar-Natural Gas Compute Campus, Lafayette, Louisiana
**Site:** 22-acre historic cannery, Vermilion River
**Owner:** Scott Tomsu
**Index Revision:** 1.0 — 2026-04-18
**Status:** Working draft — engineering package in active development

---

## Project Snapshot

| Parameter | Value | Status |
|---|---|---|
| Site | 22-acre Trappey's Cannery, Vermilion River, Lafayette, LA | L |
| Historic structures | 12 nationally registered | L |
| Stage 1 IT load | 101.2 MW (44 cassettes × 2,300 kW) | L |
| Full Build IT load | 202.4 MW (88 cassettes) | L |
| Stage 1 GPUs | 31,680 NVIDIA Vera Rubin (44 × 720) | W |
| Power architecture | Behind-the-meter permanent island, 800 VDC bus | L |
| Primary generation | Cat CG260-16 natural gas gensets, 13.8 kV, N+1 per block | W |
| Solar | 1,500 VDC → DC-DC buck → 800 VDC bus | W |
| BESS | DC-coupled LFP, block-level stabilizer, always active | W |
| Revenue model | Colocation only, base case | L |

L = Locked · W = Working · O = Open

---

## Master Index

### Master Engineering Package

| Doc # | File | Rev | Date | Description | Status |
|---|---|---|---|---|---|
| ST-TRAP-MASTER-ENG-001 | [ST-TRAP-MASTER-ENG-001_Rev0.1.md](ST-TRAP-MASTER-ENG-001_Rev0.1.md) | 0.1 | 2026-04-18 | **Master Engineering Package** — single consolidated summary of the full project engineering state. Executive summary, site/project basis (BOD ledger), power architecture, BESS, solar, thermal, CHP cascade (heat balance table), cooling tower field, master open items list (C1/C2), full document register, and 22-milestone critical path to construction package. Internal use only. | Working draft |

---

### 00-Basis — Design Foundations

| Doc # | File | Rev | Date | Description | Status |
|---|---|---|---|---|---|
| ST-TRAP-BOD-001 | [ST-TRAP-BOD-001_Rev0.4.md](00-Basis/ST-TRAP-BOD-001_Rev0.4.md) | 0.4 | 2026-04-17 | **Basis of Design** — single source of truth for all design parameters. Contains the Decision Ledger (P, R, E, T, B, S, A, N sections) with Locked / Working / Open tags. Downstream documents cite this; all value changes flow through here. | Working draft |
| ST-TRAP-THERMAL-BASIS | [ST-TRAP-THERMAL-BASIS_Rev0.4.md](00-Basis/ST-TRAP-THERMAL-BASIS_Rev0.4.md) | 0.4 | 2026-04-18 | **Thermal Architecture Basis** — cold sink architecture and CHP cascade framework. Option A (single-stage chiller) eliminated; architecture proceeds on Option B (double-effect hot-water) or C (multi-energy/exhaust-driven) pending chiller RFQ. LDEQ/LPDES regulatory framework, Vermilion River thermal limits, Munters 5.5 MW deduction. | Working draft |

---

### 01-Electrical — Power Architecture

| Doc # | File | Rev | Date | Description | Status |
|---|---|---|---|---|---|
| ST-TRAP-ELEC-001 | [ST-TRAP-ELEC-001_Rev1.2.md](01-Electrical/ST-TRAP-ELEC-001_Rev1.2.md) | 1.2 | 2026-04-17 | **Electrical Architecture** — N replicated Marlie-pattern blocks. Each block: 4 × Cat CG260-16 at 13.8 kV → step-down transformer → 480 VAC switchboard → 16 × Delta 660 kW in-row power racks → 800 VDC common busway with DC-coupled BESS and solar. Five feeder categories, cassette umbilical topology, AMCL five-tier control architecture. Visual companion: ARCHDIAG-001 Rev 0.1. | Working draft |

---

### 02-Bess — Battery Energy Storage

| Doc # | File | Rev | Date | Description | Status |
|---|---|---|---|---|---|
| ST-TRAP-BESS-001 | [ST-TRAP-BESS-001_Rev0.1.md](02-Bess/ST-TRAP-BESS-001_Rev0.1.md) | 0.1 | 2026-04-17 | **BESS Architecture Basis** — LFP chemistry, DC-coupled to 800 VDC bus, always active as block-level stabilizer (not backup). Four operating functions: transient buffering, peak shaving, dispatch optimization, contingency reserve. Vendor shortlist, AMCL integration, RFQ anchor. | Working draft |
| ST-TRAP-BESS-ARCHDIAG-001 | [ST-TRAP-BESS-ARCHDIAG-001_Rev0.1.md](02-Bess/ST-TRAP-BESS-ARCHDIAG-001_Rev0.1.md) | 0.1 | 2026-04-17 | **BESS Architecture Diagram Package** — five Mermaid diagrams: 800 VDC bus overview (block scope), BESS DC stack zoom, AMCL dispatch hierarchy, contingency decision tree, rear slab physical layout. Renders in VS Code / GitHub / Notion. | Working draft |
| ST-TRAP-BESS-RFQ-001 | [ST-TRAP-BESS-RFQ-001_Rev0.1.md](02-Bess/ST-TRAP-BESS-RFQ-001_Rev0.1.md) | 0.1 | 2026-04-18 | **BESS Vendor RFQ Package** — procurement-ready. LFP DC-coupled, 11 × 3.6 MWh working (3/4/5 MWh tiers quoted), 2 MW continuous / 4 MW peak per block, 800 VDC bus, island-mode required. SiC bidirectional DC-DC spec, NFPA 855 / UL 9540A compliance requirements, AMCL communications interface. Vendor sequence: Fluence (preferred) → LG ES Vertech → Saft → Hitachi AMPS. Portfolio context (~100+ containers across ADC sites). Evaluation criteria with disqualifying conditions. | Working draft — ready for vendor distribution |

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
| ST-TRAP-SOLAR-001 | [ST-TRAP-SOLAR-001_Rev0.1.md](09-Solar/ST-TRAP-SOLAR-001_Rev0.1.md) | 0.1 | 2026-04-18 | **Solar Array Integration — Architecture and Specification Basis** — First Solar FS-7550A-TR1, 3,731 panels, 2.05 MW DC, B1/B2 rooftops. 5-panel strings at 952V MPP → DC-DC buck → 800 VDC bus. String voltage analysis confirms >800V MPP across full Louisiana temperature range (891V summer / 1,013V winter), <1,500V Voc in all conditions. DC-DC buck spec: 800–1,500V input MPPT, 800V regulated output, ≥97%, 4-unit preferred (one per roof section). ITC: 30% base, +10% domestic content adder (First Solar US-manufactured). E-22 open (DC-DC vendor RFQ). AMCL L1/L3 dispatch integration. | Working draft |

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
| ST-TRAP-CHP-SCHEMATIC-001 | [ST-TRAP-CHP-SCHEMATIC-001_Rev0.1.md](07-Thermal/ST-TRAP-CHP-SCHEMATIC-001_Rev0.1.md) | 0.1 | 2026-04-18 | **CHP Cascade Schematic Package** — three Mermaid diagrams: (1) end-to-end cascade overview genset → HRU → Broad BH → cooling towers → atmosphere, (2) Option B vs C exhaust path branch at TB-5 decision point, (3) two isolated cooling water loops (condenser circuit + Boyd CDU GPU warm water). Heat balance summary table. Option B working basis throughout; TB-5 noted as open. Visual companion to THERMAL-BASIS and COOLING-TOWER-001. | Working draft |
| ST-TRAP-COOLING-TOWER-001 | [ST-TRAP-COOLING-TOWER-001_Rev0.1.md](07-Thermal/ST-TRAP-COOLING-TOWER-001_Rev0.1.md) | 0.1 | 2026-04-18 | **Cooling Tower Field — Vendor Specification Basis** — system boundary (absorption chiller condenser/absorber circuit; Boyd CDU GPU warm water to separate dry cooler), maximum duty 241.4 MW / 68,640 RT, nominal staged duty 183.9 MW / 52,310 RT, design wet-bulb 28°C ASHRAE 0.4%, condenser water 37°C return / ≤31°C supply (3°C approach), COND-WB open item, tower type analysis (wet preferred), water consumption ~2,476 GPM makeup at design day, cooling MCC ~4,800 kW, AMCL L0–L3 integration, SPX/Marley + BAC + Evapco shortlist, RFQ anchor conditions. Siting flag: 28,000 sq ft yard may be tight for full field — siting study C2. | Working draft |

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
BOD-001 Rev 0.4  ──────────────────────────────────────────┐
│                                                           │
├── THERMAL-BASIS Rev 0.4  (T-xx ledger)                   │
│   ├── COOLING-TOWER-001 Rev 0.1  (07-Thermal/)           │
│   └── [RIVER-001 cancelled — Vermilion River eliminated]  │
│                                                           │
├── ELEC-001 Rev 1.2  (E-xx ledger)  ◄── eng-pack-5MW      │
│   ├── ARCHDIAG-001 Rev 0.1  (visual companion)           │
│   │   ├── [pending] ST-TRAP-SLD-001                      │
│   │   └── [pending] ST-TRAP-PROT-001                     │
│   ├── BESS-001 Rev 0.1  (E-10 to E-13)                   │
│   │   ├── BESS-ARCHDIAG-001 Rev 0.1  (visual companion)  │
│   │   └── [pending] ST-TRAP-BESS-RFQ-001                 │
│   └── [pending] ST-TRAP-SOLAR-001                        │
│                                                           │
└── [pending] ST-TRAP-SOLAR-001, ST-TRAP-SLD-001,          │
    ST-TRAP-PROT-001, ST-TRAP-BESS-RFQ-001                 │
```

---

## Open Engineering Items (as of 2026-04-18)

| ID | Item | Blocking |
|---|---|---|
| TB-5 | Absorption chiller RFQ — Option B or C selection | THERMAL-BASIS →  architecture lock |
| T-11 | Boyd CDU confirmation — CHW supply 7–12°C compatibility call | Cooling loop design |
| Cat CSA | CG260-16 part-load exhaust temp / mass-flow curves | THERMAL-BASIS Option C |
| E-14 | Bus interconnect topology between blocks | ELEC-001 §9 |
| SHPO R-05/R-06 | Historic Tax Credit Part 1 / Part 2 filing | HTC financing |
| SLD-001 | Formal single-line — not yet drafted | Construction package |
| PROT-001 | Protection coordination study — not yet drafted | Construction package |
| SOLAR-001 | Solar integration document — not yet drafted | DC-DC buck spec |
| BESS-RFQ-001 | ~~Issued~~ — ST-TRAP-BESS-RFQ-001 Rev 0.1 in 02-Bess/ | — |
| COND-WB | Broad chiller condenser water inlet at 30–31°C — derating confirmation | Cooling tower CW supply spec |
| T-05 | Cooling tower type selection (wet / hybrid / adiabatic) | Tower RFQ |
| SITING-001 | Cooling tower field siting study — 28,000 sq ft yard vs full field footprint | Tower vendor RFQ |

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
| 1.5 | 2026-04-18 | Scott Tomsu | ST-TRAP-SOLAR-001_Rev0.1.md drafted and added to new 09-Solar/ folder. First Solar FS-7550A-TR1, 3,731 panels, 2.05 MW. String voltage analysis complete — 5-panel strings confirmed >800V MPP across full Louisiana temperature range. DC-DC buck spec issued (E-22). ITC basis documented. SOLAR-001 removed from pending documents. |
| 1.4 | 2026-04-18 | Scott Tomsu | ST-TRAP-BESS-RFQ-001_Rev0.1.md drafted and added to 02-Bess/. Procurement-ready vendor RFQ — LFP DC-coupled, 11 × 3.6 MWh working (3/4/5 MWh tiers), 2 MW continuous / 4 MW peak, 800 VDC island-mode. SiC DC-DC spec, NFPA 855/UL 9540A requirements, AMCL comms interface, evaluation criteria, Fluence-first vendor sequence. Portfolio context (~100+ containers ADC sites). BESS-RFQ-001 removed from pending documents. |
| 1.3 | 2026-04-18 | Scott Tomsu | ST-TRAP-CHP-SCHEMATIC-001_Rev0.1.md drafted and added to 07-Thermal/. Three Mermaid diagrams: full cascade overview, Option B/C exhaust branch, isolated cooling water loops. Heat balance summary table. Visual companion to THERMAL-BASIS and COOLING-TOWER-001. |
| 1.2 | 2026-04-18 | Scott Tomsu | ST-TRAP-COOLING-TOWER-001_Rev0.1.md drafted and added to new 07-Thermal/ folder. First issue of cooling tower field spec — maximum duty 241.4 MW / 68,640 RT, nominal staged 183.9 MW. System boundary established (absorption chiller condenser only; Boyd CDU GPU warm water to separate dry cooler). Tower type analysis complete (wet mechanical draft recommended). COND-WB approach temperature gap documented (31°C practical vs 29°C Broad rated). Water consumption ~2,476 GPM makeup at design day. Infrastructure yard siting flag raised. COOLING-TOWER-001 removed from pending documents; dependency map updated. |

---

*All documents are working drafts unless marked Locked in BOD-001. Do not cite values from any document without confirming BOD-001 ledger status.*
