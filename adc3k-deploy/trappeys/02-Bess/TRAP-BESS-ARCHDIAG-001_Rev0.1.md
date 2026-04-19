# ST-TRAP-BESS-ARCHDIAG-001 — BESS Architecture Diagram Package — Rev 0.1

**Document:** BESS Architecture Diagram Package
**Project:** Trappey's AI Center, Lafayette, Louisiana
**Revision:** 0.1 — first issue; visual companion to ST-TRAP-BESS-001 Rev 0.1
**Date:** April 17, 2026
**Owner:** Scott Tomsu
**Status:** Working draft — diagrams rendered as Mermaid (inline). Polished PDF/Word export targets Rev 1.0.

---

## 1. Purpose

Visual companion to ST-TRAP-BESS-001 Rev 0.1. Captures the BESS topology for one Marlie-pattern block at Trappey's — from the LFP battery pack through the bidirectional DC-DC converter to the 800 VDC common busway, with AMCL dispatch architecture and contingency scenario logic.

Five diagrams: one 800 VDC bus overview (block scope), one BESS DC stack zoom, one AMCL dispatch hierarchy, one contingency decision tree, and one rear slab physical layout.

**This package is architectural, not construction-issue.** CT designations, cable sizing, SSCB ratings, and trip coordination belong in ST-TRAP-SLD-001 and ST-TRAP-PROT-001. Those documents inherit the topology shown here.

**Rendering:** Diagrams use Mermaid flowchart syntax. Renders natively in VS Code (Mermaid extension), GitHub markdown preview, and Notion. For external distribution, export to PDF via VS Code Mermaid export or equivalent before Rev 1.0.

## 2. Relationship to other documents

**Upstream (this package inherits from):**

- BESS-001 Rev 0.1 — architecture anchor for this diagram package
- ELEC-001 Rev 1.2 — block electrical architecture; BESS sizing and coupling in §8
- BOD-001 Rev 0.4 — ledger authority; E-10 through E-13
- ARCHDIAG-001 Rev 0.1 — Diagram 4 shows BESS on 800 VDC bus at block scope

**Downstream (inherits from this package):**

- ST-TRAP-SLD-001 — formal single-line with BESS tie conductor sizing and SSCB ratings
- ST-TRAP-PROT-001 — DC protection coordination at BESS bus tie; SSCB pickup settings
- ST-TRAP-BESS-RFQ-001 — vendor procurement package (not yet drafted)

## 3. Conventions — domain color coding

Consistent with ARCHDIAG-001 Rev 0.1.

| Color | Domain | Elements |
|---|---|---|
| Amber | LV AC (480 V) | In-row rack AC input, BESS aux feed |
| Teal | 800 VDC | Common busway, SSCBs, blocking diodes, cassette umbilicals |
| Purple | BESS | LFP battery pack, BMS, bidirectional DC-DC, protection chain |
| Green | Solar / PV | First Solar array, DC-DC buck |
| Pink | Controls | AMCL tiers, L1 PLC, L2 SCADA, L3 AI dispatch |

*Mermaid does not apply color coding natively in all renderers. Color is noted in diagram titles and node labels.*

---

## 4. Diagram 1 — 800 VDC bus: three DC sources (block scope)

Three DC sources converge on the 800 VDC common busway for one block. In-row rack rectifier output, DC-coupled BESS via bidirectional DC-DC, and DC-coupled solar via DC-DC buck each connect through a dedicated SSCB and blocking diode. Four cassette umbilicals exit via load-break contactors and SSCBs. Bus current ~12,075 A at full block load (9,660,000 W ÷ 800 V).

```mermaid
flowchart TD
    subgraph RACKS["In-row racks — LV AC source (Amber)"]
        R["16 × Delta 660 kW in-row racks<br/>480 VAC input · 800 VDC output · 98% eff<br/>BBU 480 kW + PCS sub-100 ms per rack"]
    end

    subgraph BESS_SRC["BESS — DC-coupled (Purple)"]
        PACK["LFP battery pack<br/>3.6 MWh working · 1,100–1,500 VDC output"]
        DCDC["Bidirectional DC-DC · SiC<br/>2 MW continuous · 4 MW peak · ≥97% eff"]
        PACK --> DCDC
    end

    subgraph SOLAR_SRC["Solar PV — DC-coupled (Green)"]
        PV["First Solar Series 7 · 2.05 MW<br/>1,500 VDC strings"]
        BUCK["DC-DC buck · MPPT<br/>1,500 V → 800 V regulated"]
        PV --> BUCK
    end

    R_SSCB["SSCB + blocking diode<br/>rack output × 16"]
    B_SSCB["SSCB + blocking diode<br/>BESS bus tie"]
    S_SSCB["SSCB + blocking diode<br/>solar bus tie"]

    BUS["800 VDC common busway — copper · single-ended<br/>~12,075 A at 9.66 MW full block load<br/>Voltage regulated by in-row rectifiers + BESS DC-DC"]

    U1["Load-break contactor + SSCB<br/>Cassette 1 · ~3,000 A · 2,415 kW"]
    U2["Load-break contactor + SSCB<br/>Cassette 2 · ~3,000 A · 2,415 kW"]
    U3["Load-break contactor + SSCB<br/>Cassette 3 · ~3,000 A · 2,415 kW"]
    U4["Load-break contactor + SSCB<br/>Cassette 4 · ~3,000 A · 2,415 kW"]

    R --> R_SSCB --> BUS
    DCDC --> B_SSCB --> BUS
    BUCK --> S_SSCB --> BUS
    BUS --> U1
    BUS --> U2
    BUS --> U3
    BUS --> U4
```

---

## 5. Diagram 2 — BESS DC stack: battery pack to bus

Zoom into the BESS source. LFP cells → BMS → internal battery contactor → bidirectional DC-DC → SSCB → blocking diode → 800 VDC bus. Three-layer protection hierarchy. Communication paths to L1 block PLC shown with protocol callouts.

```mermaid
flowchart TD
    subgraph CONT["BESS container — 20-ft outdoor pad · rear slab"]
        CELLS["LiFePO4 cells<br/>Series / parallel strings<br/>Pack output: 1,100–1,500 VDC"]
        BMS["Battery BMS<br/>Cell voltage · temperature · SOC<br/>Over/undervoltage · overcurrent detection"]
        IBATT["Internal battery contactor<br/>Protection layer 1 — trips on BMS fault"]
        CELLS --> BMS --> IBATT
    end

    subgraph SKID["DC-DC converter skid"]
        DCDC2["SiC bidirectional DC-DC<br/>Input: 1,100–1,500 VDC from pack<br/>Output: 800 VDC regulated<br/>2 MW continuous · 4 MW peak · ≥97% eff<br/>Galvanic isolation · internal overcurrent"]
    end

    SSCB2["SSCB · sub-millisecond trip<br/>Protection layer 2"]
    DIODE["Blocking diode<br/>Prevents bus fault backfeed into DC-DC<br/>Protection layer 3"]
    BUS2["800 VDC common busway"]
    PLC["L1 block PLC<br/>Deterministic control"]

    IBATT --> DCDC2
    DCDC2 --> SSCB2 --> DIODE --> BUS2

    BMS -- "SOC · temp · alarms<br/>Modbus TCP / CANBUS" --> PLC
    DCDC2 -- "Mode · power · faults<br/>IEC 61850 GOOSE (protection)<br/>Modbus TCP (dispatch)" --> PLC
    PLC -- "Charge / discharge setpoints<br/>within safety envelope" --> DCDC2
```

---

## 6. Diagram 3 — AMCL BESS dispatch: L1 deterministic and L3 AI

Two-tier dispatch. L1 block PLC holds all safety interlocks — SOC floor, temperature, cell voltage limits — and cannot be overridden by L3. L3 AMCL AI optimizes across all 11 blocks within the L1 safety envelope. Setpoints flow L3 → L1 → DC-DC. Protection trips flow DC-DC → L1 → local action, no L3 involvement.

```mermaid
flowchart TD
    subgraph L0["L0 — Field devices"]
        SENS["Bus voltage · DC-DC power output<br/>BESS SOC · cell temperatures<br/>Hz meter · fault status"]
    end

    subgraph L1["L1 — Block PLC · deterministic · local · cannot be overridden"]
        SAFETY2["Safety interlocks<br/>SOC floor: 10% hard limit<br/>Cell temp limits · voltage limits<br/>Emergency shutdown path"]
        FREQ["Hz response<br/>Drop detected → DC-DC inject<br/>Before UFLS fires · response: ms"]
        CTGY["Contingency dispatch<br/>Genset trip → peak inject mode<br/>Gas loss → graceful shutdown reserve"]
    end

    subgraph L2["L2 — Plant SCADA"]
        HIST2["BESS historian · OPC-UA<br/>~50 points per block<br/>SOC · power · voltage · temp · fault codes"]
    end

    subgraph L3["L3 — AMCL AI dispatch"]
        AI["Cross-block BESS optimization<br/>Load shifting: charge off-peak · discharge peak<br/>Solar recapture: charge on PV overproduction<br/>SOC floor maintenance across 11 blocks<br/>Gas pre-charge on curtailment forecast"]
    end

    DCDC3["Bidirectional DC-DC converter"]

    SENS --> L1
    L1 -- "Historian data · OPC-UA" --> HIST2
    HIST2 -- "Aggregated BESS state · 11 blocks" --> AI
    AI -- "Setpoints within L1 safety envelope" --> L1
    L1 -- "Direct setpoints" --> DCDC3
```

---

## 7. Diagram 4 — Contingency scenario decision tree

L1 PLC detects a trigger event and dispatches BESS accordingly. Three branches cover the full contingency envelope defined in BESS-001 §6. Energy values bound the 3–5 MWh per-block sizing envelope. SOC floor (10%) is a hard limit enforced by L1 — cannot be discharged below this regardless of L3 command.

```mermaid
flowchart TD
    START2["L1 PLC detects trigger event<br/>Bus voltage deviation · Hz drop · genset trip signal · gas pressure alarm"]

    START2 --> Q1{"Single genset<br/>trip inside block?"}

    Q1 -- Yes --> A1["BESS: peak inject mode<br/>~4 MW · duration: seconds to minutes<br/>Energy consumed: ~1–2 MWh<br/>Goal: hold 800 VDC bus voltage<br/>while 3 remaining gensets ramp"]
    A1 --> R1["Block continues on 3 gensets<br/>Mode B: ~83% loading per genset<br/>SOC replenished when 4th genset restored"]

    Q1 -- No --> Q2{"Partial gas<br/>curtailment ordered?"}

    Q2 -- Yes --> A2["BESS: sustained discharge<br/>~2 MW · duration: minutes<br/>Energy consumed: ~2–3 MWh<br/>Goal: bridge while L3 ramps down<br/>IT load gracefully"]
    A2 --> R2["Orderly workload migration<br/>Gas restored or load reduced<br/>SOC replenished on recovery"]

    Q2 -- No --> Q3{"Full gas loss —<br/>all gensets trip?"}

    Q3 -- Yes --> A3["BESS: graceful shutdown reserve<br/>~2 MW sustained · 15–20 min<br/>Energy consumed: ~3–4 MWh<br/>GPU checkpoint + cassette cooldown<br/>SOC floor 10% hard limit — L1 enforced"]
    A3 --> R3["Clean shutdown · no data loss<br/>Await gas restoration or manual restart<br/>Block isolated · safe state"]

    Q3 -- No --> A4["Normal operation<br/>L3 AI dispatch active<br/>Load shifting + solar recapture<br/>SOC managed within L1 envelope"]
```

---

## 8. Diagram 5 — Physical installation: rear slab layout

One block shown. Eleven identical block footprints on the 42,000 sq ft rear slab behind Buildings 3 and 4. BESS containers subject to NFPA 855 (2026) setback distances from gensets, gas lines, property lines, and compute hall walls. Setback distances to be confirmed with Lafayette Parish AHJ at pre-application meeting.

```mermaid
flowchart LR
    subgraph SLAB2["Rear slab — 42,000 sq ft · Building 3 / 4 perimeter"]
        subgraph GENSETS["Genset bank · per block"]
            G1B["CG260-16 No.1<br/>4,000 ekW · 13.8 kV"]
            G2B["CG260-16 No.2<br/>4,000 ekW · 13.8 kV"]
            G3B["CG260-16 No.3<br/>4,000 ekW · 13.8 kV"]
            G4B["CG260-16 No.4 N+1<br/>4,000 ekW · 13.8 kV"]
        end
        subgraph BESS_PAD["BESS pad · per block · NFPA 855 setback enforced"]
            BC2["BESS container · 20-ft<br/>3.6–5.1 MWh LFP<br/>Aux power: ~80 kW from 480 VAC feeder"]
            DCDC4["DC-DC skid<br/>2 MW continuous"]
            BC2 --> DCDC4
        end
    end

    subgraph HALLS2["Compute halls"]
        B3B["Building 3<br/>20 cassettes"]
        B4B["Building 4<br/>24 cassettes"]
    end

    GENSETS -- "13.8 kV MV cable" --> XFMR2["Block transformer<br/>~15 MVA · Dyn11"]
    XFMR2 -- "480 VAC feeders<br/>to in-row power racks" --> B3B
    XFMR2 -- "480 VAC feeders<br/>to in-row power racks" --> B4B
    DCDC4 -- "800 VDC cable<br/>SSCB + blocking diode" --> BBUS["800 VDC busway<br/>inside compute halls"]
    BBUS --> B3B
    BBUS --> B4B
```

---

## 9. Engineering notes

### 9.1 What these diagrams lock

- DC coupling path: battery pack → bidirectional DC-DC → SSCB → blocking diode → 800 VDC bus. This topology is locked (BOD-001 E-11, E-12).
- Three-layer DC protection hierarchy: BMS contactor (L1) → DC-DC internal (L2) → SSCB (L3) → blocking diode (L4). Coordination logic flows to PROT-001.
- Two-tier AMCL dispatch: L1 holds all safety interlocks; L3 optimizes within envelope. L1 cannot be overridden by L3 on any safety parameter.
- Three contingency scenarios bound the 3–5 MWh per-block sizing envelope.

### 9.2 What these diagrams do not lock

- BESS container vendor (Saft / LG ES Vertech / Fluence) — open pending RFQ (E-13)
- Bidirectional DC-DC vendor (integrated with BESS vs. Hitachi AMPS standalone) — open pending RFQ (E-12)
- SSCB ratings, cable sizing, coordination intervals — belong in SLD-001 and PROT-001
- Rear slab setback distances — require NFPA 855 (2026) AHJ interpretation and physical layout study
- LG ES Vertech JF2 DC LINK is 23 ft wide (non-standard ISO) — pad logistics and crane requirements require confirmation before that vendor is selected

### 9.3 Mermaid rendering notes

These diagrams are working-draft architectural representations. Mermaid flowchart does not produce IEC 60617-compliant symbols or IEEE Std 315 one-line annotations — those belong in ST-TRAP-SLD-001 (formal single-line, not yet drafted). Mermaid topology correctly represents source-to-load paths, protection insertion points, and control signal routing.

For Rev 1.0 external distribution: export diagrams from VS Code Mermaid Preview (SVG or PNG), embed in the companion Word/PDF document, and archive alongside the markdown source.

---

## 10. Open items

| Ref | Item | Blocked on | Priority |
|---|---|---|---|
| E-12 | DC-DC vendor — integrated with BESS pack or Hitachi AMPS standalone | BESS RFQ | C1 |
| E-13 | BESS container vendor — Saft / LG ES Vertech / Fluence | BESS RFQ | C1 |
| PROT | DC protection coordination — SSCB ratings, blocking diode spec, BMS contactor coordination | ST-TRAP-PROT-001 | C1 |
| NFPA | NFPA 855 (2026) setback distances — Lafayette Parish AHJ interpretation | AHJ pre-application | C1 |
| PHYS | Rear slab layout study — BESS container setbacks vs genset placement and gas lines | Physical layout study | C2 |
| RENDER | Rev 1.0 diagram export — Mermaid → SVG/PNG for external distribution | Internal | C2 |

---

## 11. Revision plan

- **Rev 0.1 (current)** — first issue. Five Mermaid diagrams. Companion to BESS-001 Rev 0.1, ELEC-001 Rev 1.2, BOD-001 Rev 0.4.
- **Rev 0.2** — after Cat CSA governor data returns. Updates contingency scenario energy values in Diagram 4 if sizing envelope shifts.
- **Rev 0.3** — after BESS RFQ closes. Updates Diagrams 2 and 5 with locked vendor, container dimensions, and DC-DC skid configuration. Adds vendor-specific protection callouts to Diagram 2.
- **Rev 0.4** — after PROT-001 completes. Updates Diagram 2 with locked SSCB ratings and blocking diode spec.
- **Rev 1.0** — ready for external circulation. Mermaid diagrams exported to SVG/PNG. All C1 items closed. Paired with SLD-001 Rev 1.0 and PROT-001 Rev 1.0.

## 12. Approval

Rev 0.1 does not carry external circulation approval. Architecture inherits from BESS-001 Rev 0.1 and ELEC-001 Rev 1.2 approval status. External distribution waits for Rev 1.0, gated on all C1 items per §10.

---

**End of ST-TRAP-BESS-ARCHDIAG-001 Rev 0.1.**
