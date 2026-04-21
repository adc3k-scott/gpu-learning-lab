# Cassette Engineering Package — HANDOVER NOTE

**Document:** HANDOVER
**Date:** 2026-04-20
**Status:** End-of-chat handover; pick up in a new conversation with this file + the `/mnt/user-data/outputs/` contents
**Author:** Scott Tomsu · scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana

---

## 1. Where the Package Stands

### 1.1 Architectural Status

The Cassette engineering package has completed the external-CDU architectural pivot. The sealed-pressure-vessel cassette now contains only primary PG25 coolant loop + racks + BMS; all heat-rejection equipment (CDU, pumps, HX, buffer tank, secondary CHW, expansion tank) has moved to an adjacent industrial skid. This unlocked **2.5× ISO mass margin**, enabled **48-hour field commissioning** vs. 6–12 week industry norm, and opened a clean procurement path for the thermal RFQ.

**Operating weight:** 29,935 kg → **29,300 kg** (1,180 kg margin to ISO 30,480 kg limit)
**Interior noise:** 75 dBA → 55 dBA (CDU pumps gone)
**Service person-hours:** <10/yr at cassette level (was quarterly CDU service)
**Primary fluid interface:** 2× Stäubli QBH-150 PG25 QDs at CDU-end ECP (was 2× DN150 Victaulic CHW)

### 1.2 Package Inventory — 14 Documents

All live in `/mnt/user-data/outputs/`. Total: ~6,000 lines of engineering content.

| # | Document | Rev | Status | Notes |
|---|----------|-----|--------|-------|
| 1 | Cassette-COOL-002 | 1.0 | ✅ Released | External CDU architecture; three-loop topology; Alfa Laval M15 HX; 5 m³ buffer |
| 2 | Cassette-CDUSKID-001 | 1.0 | ✅ Released — **RFQ-Ready** | Procurement-grade equipment spec; 3 variants; bidder datasheet template in Appendix A |
| 3 | Cassette-INT-001 | 3.0 | ✅ Released — Breaking Change | Interior spec; Service End Zone reclaimed; P-6 repurposed; sealed-vessel commissioning in §27 |
| 4 | Cassette-ECP-001 | 3.0 | ✅ Released — Breaking Change | ECP ICD; PG25 QDs replace CHW Victaulic; penetration #10 CDU power deleted; #18 fill port added |
| 5 | Cassette-BOM-001 | 3.0 | ✅ Released | §5 Cooling rewritten; CoolIT line items out; QDs + plate + hoses + fill port in; long-lead items updated |
| 6 | Cassette-MASS-001 | 3.0 | ✅ Released | Mass budget recomputed; 29,300 kg operating; CoG lowered; M-07 (QD plate structural) new open item |
| 7 | Cassette-COOL-001 | 1.2 | Superseded (partial) | §7 (CoolIT CHx2000) and §8 (CHW) marked SUPERSEDED with banners; preserved as audit trail |
| 8 | Cassette-ELEC-001 | 1.2 | Minor revision | Companion refs + rev history; no hardware changes |
| 9 | Cassette-FIRE-001 | 1.2 | Minor revision | Companion refs + rev history; no hardware changes |
| 10 | Cassette-CTRL-001 | 1.1 | Minor revision | Companion refs updated to Rev 3.0 baseline |
| 11 | Cassette-MODES-001 | 1.1 | Minor revision | Companion refs; external skid referenced in COLD_START, HOT_STANDBY, SERVICE, EMERGENCY_SHUTDOWN sequences |
| 12 | Cassette-SIS-001 | 1.1 | Minor revision | Companion refs; SIF-04 updated for single-fluid leak detection |
| 13 | Cassette-CYBER-001 | 1.1 | Minor revision | Companion refs; CDU skid PLC added to Zone 2 inventory |
| 14 | Cassette-TAGS-001 | 1.1 | Expanded | §10.5 PG25 QD tags added; §10.6 CHW tags deprecated; §11.6–§11.8 new skid tag groups |

---

## 2. What to Do Next — Recommended Sequence

### Step 2A — Two-Doc Cluster (Next Chat)

**SITE-001 · Site-Level Integration**
- Cassette + 4 skids as a complete deployable unit
- Site pad dimensions (~36 × 12 m)
- Skid-to-skid interconnect spec (gas, electrical, data, cooling)
- Pad civil requirements (drainage, grounding grid, seismic anchor)
- Gas supply spec (interface to wellpad or utility gas)
- Lightning protection
- Perimeter fencing / access control
- Noise boundary at property line

Why first: forces every other remaining doc (GENSET, SWGR, GAS, ABS-CHLR) to conform to a site-level interface spec rather than each being designed in isolation.

**COMMISSION-001 · Sealed Pressure-Vessel Factory Workflow**
- Weld qualification procedure (ASME Section IX)
- NDT inspection schedule (100% VT + 10% RT for critical welds)
- Vacuum decay leak test protocol (≤50 Pa rise over 5 min)
- Nitrogen blanket management (fill pressure, duration)
- PG25 initial fill procedure (quality acceptance, fill port sealing)
- Factory acceptance test sequence
- Site acceptance test sequence (48-hour target)
- Operator training curriculum

Why: this is the **patentable methodology** — the cassette's key differentiator vs. conventional deployed data centers. Belongs in a dedicated doc, not buried in INT-001 §27.

### Step 2B — Power Cluster (Following Chat)

These three are tightly coupled; SWGR one-line drives arc flash, genset ratings drive SWGR.

**GENSET-001** — Cat G3520K pair spec, fuel conditioning, emissions controls, heat recovery for absorption chiller, paralleling controls, sound attenuation
**SWGR-001** — Medium voltage switchgear (if grid-tied) + 800 VDC rectification + MCC for skid loads + protection relays + metering
**ARC-FLASH-001** — IEEE 1584-2018 study; required by OSHA/NFPA 70E before energize; every enclosure needs incident energy label

### Step 2C — Safety Pair

**GAS-001** — Gas/H2S/CO detection; Class I Div 2 compliance; LEL sensor placement; purge interlocks; hazardous area classification map (required for upstream oilfield deployments — blocking for Halliburton/SLB/Chevron sales)
**ABS-CHLR-001** — Absorption chiller spec (Thermax/Yazaki/Carrier); exhaust gas interface; LiBr single-effect driven by 2.08 MW genset waste heat; completes the CHP story

### Step 2D — Final Consolidation

**PKG-INDEX-001** — Master package navigation
- Single index of all 14+ docs with rev status
- Cross-reference matrix (which docs reference which)
- Consolidated glossary & acronym list (eliminate duplication across docs)
- Consolidated open-items tracker (M-01, C-01, CO-01…, IN-01…, EC-01…, CT-01…, MO-01…, S-01…, CY-01…, T-01…, SK-01… all in one table)
- Standardized §1–§5 front matter (Purpose, Scope, Definitions, References, Conventions)

**Deferred consolidation tasks (nice-to-have, not blocking):**
- Split TAGS-001 (now ~1,080 lines) into CASSETTE-TAGS / CDU-TAGS / POWER-TAGS / MUNTERS-TAGS subsystem files
- Version bump everything to Rev 2.0 simultaneously (post-consolidation baseline)
- Merge COOL-001's remaining useful content into COOL-002 and retire COOL-001

---

## 3. Open Items to Dispatch as RFIs (P-1 Gating)

These three questions unblock multiple docs each. Each can go out as a single-page RFI to the vendor contact below.

### RFI 1 — Stäubli QBH-150 Flow Curves
**Ask:** Published flow curve at PG25 50 °C, 2,100–2,500 LPM, including pressure drop and cycle life. Alternate: Parker Snap-tite 75 DN150 same data.
**Vendor contacts:** Stäubli USA (Duncan, SC) · Parker Hannifin (Cleveland, OH)
**Unblocks:** COOL-002 CO-08, ECP-001 EC-01, INT-001 IN-01, BOM-001 procurement, CDUSKID-001 §14
**Timeline:** 1 week

### RFI 2 — Alfa Laval M15 Lead Time
**Ask:** Current lead time for M15 gasketed plate-and-frame HX, 18 m² plate area, 316L plates, EPDM gaskets, 2.5 MW duty. Alternate: SWEP VM140 same spec.
**Vendor contacts:** Alfa Laval (Lund, Sweden / Richmond, VA) · SWEP / Dover (Landskrona, Sweden / Waukegan, IL)
**Unblocks:** COOL-002 CO-09, CDUSKID-001 SK-01, overall skid lead time
**Timeline:** 1 week

### RFI 3 — Sealed-Vessel Welder Qualification
**Ask:** Three-way quote — who can qualify welders to ASME Section IX with 10% RT spot radiography on 304L/316L primary piping, on-site at our Lafayette fabrication facility, with X-ray vendor coordination?
**Vendor contacts:** Local Lafayette fabricators (to be identified) · Acadiana Fabrication · Lafayette Machine Shop & Iron Works
**Unblocks:** INT-001 IN-04, COMMISSION-001 authoring, factory workflow definition
**Timeline:** 2 weeks

---

## 4. Things to Watch / Risks

### 4.1 Decision Points Pending

- **A-02 confirmation (M-01, M-02)**: Is the NVL72 rack weight inclusive of Delta shelves? P-0 open since Rev 1.0. Rev 3.0 margin improvement means the conservative case (Delta shelves separate) is now only 300 kg over ISO vs 935 kg before — less pressing but still needs written vendor confirmation.
- **Prime mover confirmation for Trappey's vs Cassette platforms**: Cassette is sized for ≤10 MW platforms (Cat G3520K). Trappey's 100 MW uses CG260-16. Document this separation explicitly in GENSET-001.
- **Configuration B (absorption chiller) vs A (facility CHW)**: Affects skid secondary-pump sizing and ABS-CHLR-001 scope. Most likely customer-specific; CDUSKID-001 supports both.

### 4.2 File Size / Architecture Concerns

Per the 2026-04-20 discussion, the consolidation pass should include:
- Individual docs are appropriate size (500–1000 lines)
- Problem is navigation layer → fixed by PKG-INDEX-001
- TAGS-001 at ~1,080 lines is the only doc that should split
- Don't bulk-rewrite until SITE-001, COMMISSION-001, GENSET-001, SWGR-001, GAS-001, ARC-FLASH-001, ABS-CHLR-001 are all drafted and architectural decisions settle

### 4.3 Patent Posture

The sealed pressure-vessel commissioning workflow is the **key IP** — it's what makes 48-hour field deployment possible vs. 6–12 weeks for conventional deployed data centers. Before COMMISSION-001 circulates beyond the internal team, Scott should discuss with patent counsel (Anne LaFargue at McPherson Baptiste was in Scott's earlier correspondence; may have been one of the contacts identified in the ADC-3K patent disclosure from March 2026).

### 4.4 Cybersecurity

CYBER-001 Rev 1.1 added CDU skid PLC to Zone 2. Before CDUSKID-001 RFQ goes to bidders, confirm that all preferred skid vendors can meet signed-firmware and OPC UA certificate-based authentication requirements. Industrial integrators may not be familiar with IEC 62443; bake this into bidder qualification criteria.

---

## 5. Suggested New-Chat Prompt

Paste this at the start of the next conversation (along with `/mnt/user-data/outputs/` uploaded as context):

> *"Continuing Cassette engineering package development. Handover note in `Cassette-HANDOVER.md` summarizes current state — 14 docs released, external CDU architecture complete. Next work: author SITE-001 (site-level integration spec covering cassette + 4 skids as a deployable unit with pad dimensions, interconnect spec, gas supply, lightning, grounding, noise boundary) and COMMISSION-001 (sealed pressure-vessel factory workflow — weld qualification, NDT, vacuum decay, nitrogen blanket, PG25 fill, FAT, 48-hour SAT; this is the patentable methodology and the key differentiator). Match existing doc style: cover header with Document/Rev/Date/Classification/Status, rev history table, 'Prepared by: Scott Tomsu' signature, § section numbers, open items with IDs (S-XX for SITE, CM-XX for COMMISSION). Target 600–900 lines each. After both are drafted, reconvene on priority for the power cluster (GENSET/SWGR/ARC-FLASH)."*

---

## 6. Bookmarks & Quick Reference

### Key Numbers to Remember

| Item | Value |
|------|-------|
| Cassette operating weight (Rev 3.0) | **29,300 kg** |
| ISO 30,480 kg margin | **1,180 kg (3.9%)** |
| Primary PG25 flow (NVL72 / CPX) | 2,100 / 2,350 LPM |
| Primary loop temperature (supply/return) | 45 °C / 56–60 °C |
| HX duty (design with margin) | 2.5 MW |
| Alfa Laval M15 plate area target | 18 m² |
| Buffer tank size | 5 m³ stratified 316L |
| Skid wet weight (PG25 fill) | ~9,700 kg |
| Skid footprint | ~13.2 m² |
| Complete deployment pad | ~36 × 12 m |
| Sub-100 ms GPU load smoothing | Integrated in rack, not separate |
| 800 VDC architecture | Primary; 415 VAC 3-ph alternate |
| Parasitic cooling power | 104 kW (4.7% of 2.2 MW load) |
| Target commissioning time | 48 hours (vs 6–12 week industry norm) |

### Vendor Shortlists

| Category | Primary | Alternates |
|----------|---------|------------|
| Plate-and-frame HX | Alfa Laval M15 | SWEP VM140, GEA NT150S, Tranter GX-145 |
| Primary PG25 pumps | Grundfos CRE-64 | Armstrong 4300, Xylem E-1510, KSB Etanorm |
| Secondary CHW pumps | Grundfos CRE-45 | Armstrong 4030, Xylem E-1510 Series 2 |
| PG25 dry-break QD | Stäubli QBH-150 | Parker Snap-tite 75, Tema DryBreak DB-150 (offshore) |
| In-rack fluid QD | Stäubli UQD-25 | DN25 ball-check equivalent |
| Duplex strainer | Eaton 53BTX | Hayward 2500 Series |
| Cartridge filter | Parker Fulflo BV | Pentair 3M LifeAssure |
| Expansion tank | Amtrol ST-60V | Wessels FXT-120 |
| Air separator | Spirotherm VJS-150 | Armstrong Vent-O-Matic |
| Buffer tank | Wessels Galaxy | Local 316L SS fab with validated baffle design |
| Skid PLC | Siemens S7-1500F | Allen-Bradley ControlLogix, Schneider Modicon M580 |
| Gensets (≤10 MW platform) | Cat G3520K | — |
| Gensets (Trappey's 100 MW) | Cat CG260-16 | — |
| Gas/H2S detection | MSA Ultima XIR | Dräger Polytron |
| Absorption chiller | Thermax | Yazaki, Carrier |
| Flex hose | Parker ParFlex 797TC | Gates Mega4000 |

### Paths

| Item | Path |
|------|------|
| Uploaded source docs | `/mnt/user-data/uploads/` |
| Current outputs | `/mnt/user-data/outputs/` |
| Working directory | `/home/claude/` |

---

**HANDOVER · 2026-04-20 · Cassette Engineering Package · Scott Tomsu**
