# Cassette — DOCUMENT SET

**As of:** 2026-04-19 (Rev 2.0 issued on BOM-001, ECP-001, INT-001)
**Owner:** Scott Tomsu · scott@adc3k.com · Lafayette, Louisiana

This is the authoritative document set for the Cassette

---

## CURRENT DOCUMENTS

### Cassette-iNT-001 Rev 1 — Pod Interior Design Specification

The master document. Defines the complete interior design of the Cassette — a sealed, autonoumous, unmanned, stackable 40 ft HC ISO container housing 15 NVIDIA Vera Rubin NVL72 racks (13 compute + 1 InfiniBand + 1 storage/management). Covers both onshore Lafayette and offshore marine variants with deltas called out inline. 30 sections. Start here for any integration, procurement, or operational question about the pod.

### Cassette-ECP-001 Rev 1.0 — External Connection Panel Interface Control Document

The interface contract. Defines exactly what crosses the Cassette's external boundary at either end (ELEC ECP and CDU ECP) — every penetration, connector type, cable specification, environmental rating, and acceptance criterion. Use this when connecting the Cassette to any upstream platform, when specifying cable/pipe runs between Cassette and external infrastructure, or when doing commissioning sign-off at the ECP.

### Cassette-BOM-001 Rev 1.0 — Bill of Materials

The procurement document. Complete parts list for one Cassette, organized by subsystem. Includes vendor recommendations, onshore/offshore variant flags, and critical-path long-lead items. No pricing included — this supports RFQ, not budget. Use this to drive procurement packages and vendor RFQs.

### Cassette-FIRE-001 Rev 1.0 — Fire Suppression Engineering

NFPA 2001 engineering basis for the Novec 1230 total flood system. Calculates required agent (72 kg), evaluates cylinder sizing, verifies hold time, sizes the over-pressure vent, and defines the full detection-to-discharge interlock sequence. **Key finding: BOM cylinders are 4× oversized — 297.8 kg available vs 72 kg required. Correction reduces cassette mass by ~275 kg.**

### Cassette-ELEC-001 Rev 1.0 — Electrical Single-Line Diagram & Distribution Specification

The electrical engineering document. Covers all four power systems (800 V DC primary, 415 V AC alternate, 480 V AC auxiliary, 24 V DC life-safety), full conductor sizing, protective device coordination, fault current analysis, IMD architecture, and grounding. **Key findings: main DC feed requires laminated bus bar (not cable); DC busway must be upgraded to 4,000 A to support CPX upgrade path; AC alternate path has two BOM errors requiring correction.**

### Cassette-COOL-001 Rev 1.0 — Cooling Hydraulic Model

Primary loop hydraulics (PG25 glycol, CDU to racks), CDU selection verification, CHW secondary loop at ECP, and in-rack coupling analysis. **Key findings: (1) 2,100 LPM primary flow is correct for NVL72 but insufficient for CPX — need 2,350 LPM; (2) CHx2000 is 10.6% over nameplate at CPX full load; (3) ECP-001 CHW flow spec of 1,800 LPM is undersized — results in 20.3 °C return vs. 18 °C limit, corrected to 2,200 LPM; (4) ECP DN100 Victaulic connector undersized at corrected flow, upgrade to DN150; (5) UQD-16 in-rack coupling requires 7 parallel per rack, recommend upgrade to UQD-25.**

### Cassette-MASS-001 Rev 1.0 — Mass Statement & Weight Budget

The weight engineering document. Bottom-up component-level weight register against the ISO 30,480 kg gross limit. Includes longitudinal and vertical center of gravity, two-high stacking analysis, and sensitivity analysis for rack weight and Delta shelf inclusion scenarios. **Key finding: the 15-rack design is weight-critical and requires M-01/M-02 resolution before fabrication commitment.**

---

## HOW TO USE THE SET

**Engineering question?** → ask scott
**Integration question (platform-to-pod)?** → Cassette-ECP-001 Rev 1.0
**Procurement question?** → Cassette-BOM-001 Rev 1.0
**Something not in any of these?** → It hasn't been specified yet. Ask before assuming.

---

## KEY POD PARAMETERS (QUICK REFERENCE)

| Parameter                          | Value                                     |
|------------------------------------|-------------------------------------------|
| Enclosure                          | 40 ft HC ISO, CSC-plated                  |
| Internal dimensions                | 12,032 × 2,352 × 2,698 mm                 |
| Rack count                         | 15 Vera Rubin NVL72 (Oberon, 21" ORv3)    |
| Rack breakdown                     | 13 compute + 1 InfiniBand + 1 storage/mgmt |
| GPUs per pod                       | 936 Rubin GPUs (NVL72 tier)               |
| Pod IT load (NVL72)                | 1,585 kW                                  |
| Pod IT load (NVL144 CPX upgrade)   | 2,105 kW                                  |
| Pod facility load                  | 1,677–2,212 kW                            |
| Power conversion                   | Delta 110 kW shelves, in-rack (no sidecar) |
| Primary input                      | 800 V DC (or 415 V AC 3-ph alternate)     |
| CDU                                | CoolIT CHx2000 (2 MW)                     |
| Cold plate supply/return           | 45 °C / 55–60 °C                          |
| CHW supply/return at ECP           | 7–12 °C / 12–18 °C                        |
| Dehumidification                   | Munters HCD-600 (external skid)           |
| Fire suppression                   | Ansul Novec 1230 + VESDA-E VEU            |
| BMS                                | NVIDIA Jetson AGX Orin (N+1)              |
| Access panels                      | 12 (6 per long side, 900 × 2,000 mm)      |
| ECP zones                          | 2 (ELEC end + CDU end)                    |
| Operating weight                   | 30,085–31,565 kg (see MASS-001) — **weight-critical** |
| Variants                           | Onshore + Offshore (same pod, marine deltas) |

---

## CRITICAL OPEN ITEMS (P-0, GATING PROCUREMENT)

1. **C-01 / M-01/M-02** — Confirm Vera Rubin NVL72 loaded rack weight AND whether Delta power shelves are included in that figure. MASS-001 bottom-up analysis shows the 15-rack design is 1,085 kg over ISO limit if Delta shelves are counted separately at 1,500 kg/rack. 14-rack design is safe at all realistic weights.

2. **C-02** — Confirm Delta 110 kW shelf 800 V DC input variant availability and lead time. Selection of DC vs AC input at ECP depends on this.

3. **C-03** — CoolIT CHx2000 RFQ — lead time and delivery schedule.

Address these three before committing to container fabrication or rack procurement.

---

## WITHDRAWN DOCUMENTS

---

**Cassette Document Set — README**
**Scott Tomsu · scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana**
**CONFIDENTIAL**
