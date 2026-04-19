# ST-TRAP-CHP-SCHEMATIC-001 — CHP Cascade Schematic — Rev 0.1

**Document:** CHP Thermal Cascade — End-to-End Schematic Package
**Project:** Trappey's AI Center, Lafayette, Louisiana
**Revision:** 0.1 — first issue
**Date:** April 18, 2026
**Owner:** Scott Tomsu
**Status:** Working draft
**Basis:** Option B (double-effect hot-water via HRU) — TB-5 open. Option C (direct exhaust to Broad BE) is the contingency; removing the HRU and substituting Broad BE for BH is the only topology change.
**Authority:** ST-TRAP-THERMAL-BASIS Rev 0.4 · ST-TRAP-COOLING-TOWER-001 Rev 0.1. No values originate here — this is a visual companion only.

W = Working estimate · L = Locked per BOD-001 · O = Open

---

## Diagram 1 — CHP Cascade: End-to-End Overview

Full thermal chain from genset combustion to atmospheric rejection. Condenser water return loop shown at bottom.

```mermaid
flowchart TB
    GEN(["44 × Cat CG260-16\n108,240 kW electrical\n~106,084 kW waste heat\n61.5% load (W)"])

    GEN -->|"~47,872 kW exhaust (W)"| EXH
    GEN -->|"~58,212 kW jacket water (W)"| JW

    EXH["Exhaust header\n372–420°C est. (W)"]
    JW["Jacket water circuit\n≤99°C outlet (W)"]

    EXH -->|"5,500 kW (L T-12)"| MUNT
    EXH -->|"~42,372 kW (W)"| HRU

    MUNT["Munters HCD/MCD\n44 × 125 kW — desiccant regen\nT-12 LOCKED"]
    HRU["Exhaust HRU\nCain / E-Tech / Rentech TBD\nOption B — TB-5 open\nBackpressure budget: ≤6.7 kPa (Cat)"]

    MUNT --> CASS(["Cassette enclosures\n≤50% RH"])
    HRU -->|"stack ~120°C leaving"| STACK(["Atmosphere\nvia stack"])

    HRU -->|"180°C / 165°C hot water (W)"| HEADER
    JW -->|"JW recovery — detail TBD"| HEADER

    HEADER["Absorption drive header\n~100,584 kW net (W)"]
    HEADER --> CHILLER

    CHILLER["Broad BH — Double-effect LiBr\nOption B · TB-5 open\nCOP 1.40 operating (W)\nStaging required — coverage >100% vs demand"]

    CHILLER -->|"6.7°C supply / 13.7°C return\n~107,300 kW staged (W)"| CHWDIST
    CHILLER -->|"37°C out"| CW_OUT

    CHWDIST["Chilled water distribution\nMunters cooling side · NOC\nOffices · electrical rooms"]

    CW_OUT["Condenser water out\n37°C"]
    CW_OUT -->|"~114,400 GPM · VFD pumps N+1 (W)"| CT

    CT["Cooling tower field\nWet mechanical draft · T-05 open\n~241 MW / 68,640 RT design duty (W)\nSPX/Marley · BAC · Evapco\nDesign WB 28°C (L)"]

    CT -->|"241 MW max (W)"| ATM(["Atmosphere"])
    CT -->|"≤31°C (W)"| CW_RET

    CW_RET["Condenser water return\n≤31°C to chiller"]
    CW_RET --> CHILLER
```

---

## Diagram 2 — Exhaust Path: Option B vs C Branch Point

TB-5 is the only structural topology decision in the CHP cascade. Everything downstream of the chiller is identical under both options.

```mermaid
flowchart LR
    GENX(["CG260-16 exhaust\n372–420°C est. (W)\n~47,872 kW campus (W)"])

    GENX -->|"5,500 kW (L)"| MUNT2["Munters slip-stream\nT-12 LOCKED\n→ desiccant regen"]
    GENX -->|"~42,372 kW (W)"| TB5{{"TB-5\nOpen"}}

    subgraph OPT_B["Option B — WORKING BASIS"]
        HRU2["Plate-fin HRU\nCain / E-Tech / Rentech TBD\nExhaust in: 372–420°C\nHot water out: 180°C\nStack leaving: ~120°C\nBP added: 2.0–2.5 kPa"]
        BH["Broad BH\nDouble-effect hot-water LiBr\nDrive: 180°C hot water\nCOP rated: 1.50 · COP operating: 1.40 (W)\nFull drive temp match from any exhaust ≥200°C"]
        HRU2 -->|"180°C hot water"| BH
    end

    subgraph OPT_C["Option C — CONTINGENCY (Cat CSA required)"]
        BE["Broad BE\nDirect exhaust-drive LiBr\nRated inlet: 500°C (L catalog)\nCG260-16 est.: 372–420°C (W)\nGap: 80–128°C below rated\nCOP and capacity derated — amount TBD\nLower BP vs Option B (no HRU)"]
    end

    TB5 -->|"PREFERRED\nfull drive temp match\nany exhaust ≥200°C"| HRU2
    TB5 -->|"CONTINGENCY\nif Cat CSA confirms\nexhaust ≥450°C"| BE

    BH -->|"→ Chilled water\n→ Condenser circuit"| BOTH(["Both options feed\nidentical downstream\ncooling loops\n(see Diagram 3)"])
    BE --> BOTH

    MUNT2 --> CASS2(["Cassettes\n≤50% RH"])
```

---

## Diagram 3 — Cooling Water Loops

Two physically and thermally isolated circuits. No shared piping, no shared basin.

```mermaid
flowchart TB
    subgraph COND_LOOP["Absorption chiller condenser circuit — PRIMARY heat rejection"]
        CH_O["Chiller\ncondenser outlet\n37°C"]
        PUMP["Condenser water pumps\n~114,400 GPM max (W)\nVFD · N+1"]
        CT3["Cooling tower field\nWet mechanical draft · T-05 open\n~241 MW / 68,640 RT design (W)\nDesign WB 28°C (L)\n6–7 cells + N+1 spare\nSPX/Marley · BAC · Evapco"]
        CT_ATM(["Atmosphere\n241 MW max (W)"])
        MKP(["Makeup water\n~2,476 GPM design day (W)\nSource: Open\nMunicipal · well · Vermilion intake"])
        BLWD(["Blowdown\n~825 GPM (W)\nLPDES — cooling tower blowdown"])
        CH_I["Chiller\ncondenser inlet\n≤31°C"]

        CH_O --> PUMP --> CT3
        CT3 --> CT_ATM
        CT3 --> BLWD
        MKP --> CT3
        CT3 --> CH_I
    end

    CH_I -->|"condenser circuit\ncontinuous loop"| CH_O

    subgraph GPU_LOOP["GPU warm water loop — ISOLATED, no connection to condenser circuit"]
        GPU3(["NVIDIA Vera Rubin\nGPU cold plates\n101,200 kW IT (L)"])
        CDU3["Boyd CDU\n2,000 kW per cassette (L)\nN+1 pumps · 44 units"]
        DRY3["Adiabatic dry cooler\n~81 MW\n44 × 1,840 kW (BOD C-17 L)\nSeparate from cooling tower field"]
        DRYATM(["Atmosphere"])

        GPU3 -->|"~50–55°C return (W)"| CDU3
        CDU3 -->|"warm water header"| DRY3
        DRY3 --> DRYATM
        DRY3 -->|"≤45°C supply (L)"| CDU3
        CDU3 -->|"≤45°C to GPU rack (L)"| GPU3
    end
```

---

## Heat Balance Summary — Stage 1 Campus, Option B, 61.5% Load

| Stream | kW | Status | Disposition |
|---|---|---|---|
| Electrical generation (44 gensets) | 108,240 | W | IT + facility + aux |
| IT load (44 cassettes) | 101,200 | L | GPU compute |
| Facility aux (NOC, offices, controls) | ~6,100 | W | Facility load |
| **Total waste heat — exhaust + JW** | **~106,084** | **W** | → recovery cascade |
| Munters slip-stream (T-12 LOCKED) | 5,500 | L | → desiccant regen |
| Net to absorption chiller | ~100,584 | W | → Broad BH drive |
| Absorption COP (Option B, operating) | 1.40 | W | — |
| Absorption cooling produced (max) | ~140,818 | W | > campus demand |
| Campus cooling demand (IT + overhead) | ~107,300 | W | Staged chiller output |
| **Condenser + absorber rejection — nominal** | **~183,943** | **W** | → cooling towers |
| **Condenser + absorber rejection — maximum** | **~241,402** | **W** | → cooling towers (design sizing) |
| GPU warm water (Boyd CDU) | ~80,960 | L (C-17) | → adiabatic dry cooler (separate) |
| Stack exhaust (after HRU extraction) | TBD | O | → atmosphere via stack |
| Cooling tower makeup water | ~2,476 GPM | W | → evaporation + blowdown |

**Key: all campus cooling demand met by absorption cooling alone. No grid, no river, no auxiliary chiller required under Option B at 61.5% genset load.**

---

## Open Items Blocking Schematic Lock

| Ref | Impact on this document |
|---|---|
| TB-5 | Determines Diagram 2 branch — Option B or C. Until resolved, Option B is the working schematic. |
| Cat CSA | Confirms CG260-16 exhaust temperature and mass flow at 61.5% load — locks heat balance numbers. |
| JW integration detail | How jacket water heat interfaces with absorption drive (direct header supplement vs separate PHE cascade vs separate single-effect stage). |
| T-05 | Cooling tower type selection — locks tower specification in Diagrams 1 and 3. |
| COND-WB | Broad app eng confirmation on 31°C condenser water inlet — locks condenser water supply temperature in Diagram 3. |

---

## Revision Plan

| Rev | Trigger | Change |
|---|---|---|
| **0.1 (current)** | First issue | Full cascade overview, Option B/C branch, cooling loop isolation, heat balance table |
| 0.2 | TB-5 closes | Diagram 2 — remove contingency branch, lock working option; update chiller label with confirmed model |
| 0.3 | Cat CSA received | Update all W heat balance values with confirmed genset data |
| 1.0 | All C1 items closed | Lock schematic. Paired with THERMAL-BASIS Rev 1.0 and COOLING-TOWER-001 Rev 1.0 |

---

## Approval

Rev 0.1 is a working draft for internal engineering use. Not for external distribution. Sign-off follows BOD-001 Rev 0.4 approval path. External distribution waits for Rev 1.0.

---

**End of ST-TRAP-CHP-SCHEMATIC-001 Rev 0.1.**
