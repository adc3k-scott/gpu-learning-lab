---
name: Wetland & Offshore Deployment
description: Remote ADC 3K pod deployment strategy — wetland pilings (Atchafalaya), offshore rigs/barges (Gulf of America), and 5-tier edge network
type: project
---

# Wetland & Offshore Deployment — ADC 3K Edge Nodes

Last updated: 2026-03-12

## What These Are
Remote deployment sites for ADC 3K inference pods. These are edge nodes — inference-only, no training. All management, orchestration, and NOC functions run from Willow Glen (primary) and MARLIE 1 (backup). Sites are lights-out after deployment.

## Connectivity Architecture
- **Terrestrial sites** (wetland/pipeline corridor): Dedicated fiber back to Willow Glen
- **Offshore sites** (rigs, platforms, barges): Starlink (primary) + VSAT (backup) to Willow Glen
- Management plane: Mission Control HD SaaS + MARLIE 1 NOC
- All sites connect TO Willow Glen — never to each other directly

## Deployment Environments

### 1. Wetland — Atchafalaya Basin (Pilings)
- ADC 3K pods mounted on elevated pilings above wetland/marsh terrain
- Atchafalaya River delta: largest river delta/swamp system in North America
- Connectivity: fiber run along existing pipeline or utility ROW (right-of-way)
- Power: nat gas from existing pipeline corridor (same ROW as fiber)
- Use case: low-latency AI inference for Louisiana industrial corridor customers
- Structural: pods are ISO containers — adapt piling mount to standard container corner castings
- Environmental: no ground disturbance beyond pilings, no fill, wetland-compatible footprint

### 2. Offshore — Rigs & Platforms (Gulf of America)
- ADC 3K pods installed on existing offshore production platforms or jackup rigs
- Platform operators need AI inference for: wellbore monitoring, predictive maintenance, ROV ops, safety systems
- Connectivity: Starlink primary (SpaceX maritime service), VSAT backup
- Power: platform electrical (existing diesel/gas gensets on platform)
- Use case: offshore AI inference — no latency tolerance for shore-based compute in real-time ops
- ROV operations context: Scott's 25+ years ROV Superintendent experience directly informs this use case

### 3. Barges (Gulf of America / Inland Waterways)
- Floating deployment on work barges or dedicated compute barges
- Mobility advantage: reposition pod to highest-value location
- Connectivity: Starlink maritime
- Power: barge gensets (standard 480V 3-phase available on most work barges)
- Use case: construction operations AI, pipeline inspection, fleet management AI

## 5-Tier Edge Strategy
```
Tier 1: Willow Glen          PRIMARY HUB — training, large-scale inference, storage
Tier 2: MARLIE 1             REGIONAL HUB — edge AI, R&D, backup NOC (Lafayette)
Tier 3: ADC 3K (urban/industrial)  NEAR-EDGE — Trappeys model, industrial corridors
Tier 4: ADC 3K (wetland/piling)    MID-EDGE — Atchafalaya, pipeline ROW sites
Tier 5: ADC 3K (offshore/barge)    FAR-EDGE — rigs, platforms, maritime
```
All tiers 3-5 are inference-only. Training and fine-tuning stay at Tier 1-2.

## Why Louisiana / Gulf South Is the Right Region
- Atchafalaya Basin: existing pipeline ROW = power + fiber path, no new easements needed
- Offshore Gulf of America: largest concentration of offshore oil + gas infrastructure in US
- Existing ROV operator network (Scott's contact base) = ready customer pipeline
- No other AI infrastructure company is targeting this deployment environment
- ADC 3K immersion pods = no HVAC = works in humid coastal environments

## Operational Model
- Pods ship dry, filled on-site with EC-110 dielectric
- Installation: crane lift onto piling mount or platform deck
- Power: connect to site electrical (480V 3-phase)
- Fiber/Starlink: connect and register with Mission Control
- Zero on-site staff after commissioning
- Maintenance: scheduled fluid checks + GPU swaps via local marine/industrial contractors
- SLA target: 99.5% uptime

## Key Differentiators vs Land-Based Competitors
- No competitors are targeting offshore platforms or wetland/piling environments
- Immersion cooling eliminates HVAC failure mode in humid/salt air environments
- Scott's ROV/offshore background = credibility with platform operators
- Existing infrastructure (pipelines, platforms) = minimal new construction

## Open Items
- Site survey: identify candidate wetland corridor sites along Atchafalaya ROW
- Offshore RFI: identify candidate platforms for pilot deployment (Scott's contact network)
- Starlink maritime service agreement (SpaceX Business)
- Structural engineering: piling spec for wetland ISO container mount
- Offshore safety certification: ATEX/hazardous area classification for pod electrical
