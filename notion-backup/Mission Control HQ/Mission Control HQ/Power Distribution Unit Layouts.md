# Power Distribution Unit Layouts
*Notion backup — 2026-04-03*

> Phase 1 target: ~2 MW total load (16 NVL72 racks + cooling + network). Natural gas generators and UPS batteries stay outside the thermal envelope.
---
## Power Architecture
- Source A: LUS Power utility feed — primary
- Source B: Natural gas generators (exterior) — automatic transfer switch (ATS)
- UPS: Exterior battery cabinet — bridges utility-to-generator gap (~10-15 sec)
- Distribution: 480V 3-phase to main panel — step-down to rack PDUs
- Phase 1 load estimate: NVIDIA rack TDP unconfirmed — engage NVIDIA Enterprise for facility power spec
---
## Exterior Equipment (Outside Thermal Envelope)
- Generators: 2x natural gas gensets — N+1 — exterior south pad mount
- ATS: Automatic Transfer Switch — exterior weatherproof enclosure
- UPS batteries: Battery cabinet — exterior weatherproof, climate controlled
- Main disconnect: Main breaker panel — exterior accessible
---
## Interior Distribution
### Main Distribution Panel
- Feed: 480V 3-phase from exterior ATS through conduit penetration
- Breakers: 1x 400A 3-phase breaker per 2-rack PDU zone (8 breakers total)
- Location: Network core — north end of room
---
### Per-Rack PDU
- Qty: 8x dual-feed PDUs — each serves 2 NVL72 racks
- Type: Metered, switched — remote outlet control via SNMP/REST
- Input: 480V 3-phase / 200A per PDU
- Monitoring: Per-outlet current metering — feeds InfraManagerAgent
---
## Generator Spec (Preliminary)
- Fuel: Natural gas — Atmos Energy supply line
- Size: 2x 1.25 MW continuous — N+1 for 2 MW load
- Startup: Auto-start on utility fail — <15 sec to full load
- Enclosure: Sound-attenuated weatherproof — exterior pad mount
- Fuel line: Atmos Energy commercial service — 2-inch minimum supply
---
## PUE Target
```plain text
PUE = Total Facility Power / IT Equipment Power
    = (1.92 MW compute + 0.06 MW cooling aux + 0.02 MW misc) / 1.92 MW
    = ~1.04  (liquid cooled, no CRAC units, no hot aisle air handling)

Industry best practice: <1.2
Hyperscale liquid-cooled target: <1.1
MARLIE I target: <1.05
```
---
## Monitoring
- Mission Control: InfraManagerAgent — real-time kW per rack, PUE, phase balance
- Alerts: Over-current, phase imbalance, generator ATS transfer events, UPS state
> CORRECTED POWER HIERARCHY (March 8, 2026): LUS grid = primary. Bloom Energy fuel cell = continuous supplemental generation (baseload, not backup). Diesel gensets = emergency backup only (N+1). Do not describe Bloom as primary or as backup — it is continuous supplemental.
---
> SCOPE: This document applies to MARLIE I — the permanent AI Factory at 1201 SE Evangeline Thruway. NOT applicable to ADC 3K container pods, which use immersion cooling and a separate architecture.
---
> UPDATED 2026-03-23 -- POST-GTC REWRITE
## Power Architecture -- 800V DC Native (ALL Sites)
### 4-Layer Power Hierarchy (LOCKED):
Layer 1: Solar (First Solar TR1) -- Primary offset
Layer 2: Natural Gas (Henry Hub) -- Backbone 24/7
Layer 3: Diesel Gensets -- Emergency backup
Layer 4: Grid -- SELL-BACK ONLY (Willow Glen: Entergy, Lafayette: LUS)
> Grid is NEVER for consumption. Gas is ALWAYS running. Bloom Energy is NOT in the power stack. REMOVED post-GTC.
### Power Chain:
Gas/Solar -> Generator/Panels -> Eaton Beam Rubin DSX Rectifier (AC->800V DC) -> 800V DC Bus -> Eaton Busway -> Rack PDU (Eaton HDX G4) -> 64:1 LLC Converter (built into NVIDIA rack) -> 12V DC -> GPU
### Per-Site Power:
Willow Glen: 2x Cat CG260-16 (2.8 MW, H2-ready), 400+ acres ground mount solar, Sell-back to Entergy, Phase 1 IT = 1.3 MW (10 racks)
MARLIE I: 2x Cat G3520C (1.5 MW), 300 kW rooftop + ground solar, LUS backup, Phase 1 IT = 1.04 MW (8 racks)
Trappeys: 2x Cat G3520C (1.5 MW), 2.05 MW rooftop (3,731 panels), LUS sell-back, Phase 1 IT = 520 kW (4 racks)
ADC 3K Pod: 1x portable genset (250-500 kW), Optional roof panels, Optional grid tie, Phase 1 IT = 130-260 kW (1-2 racks)
### ADC 3K Pod Power:
- Self-contained 800V DC system in 40-ft container
- Portable natural gas generator (field gas available at oil field sites)
- Eaton Beam Rubin DSX rectifier (containerized)
- Optional solar panels on container roof
- Optional grid tie for urban deployments
- 4-layer hierarchy applies to EVERY deployment
---
> CRITICAL WARNING (2026-03-24): This page has 3 CONFLICTING power hierarchies. ONLY the POST-GTC section is correct: 800V DC native, Eaton Beam Rubin DSX, 4-layer hierarchy (Solar > Gas > Diesel > Grid sell-back). Bloom Energy is REMOVED. LUS grid is backup only at MARLIE I. 480V 3-phase content is WRONG.