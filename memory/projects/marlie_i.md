# MARLIE I — Lafayette AI Factory
Last updated: 2026-03-09

## What MARLIE I Is
Permanent AI Factory at 1201 SE Evangeline Thruway, Lafayette, Louisiana.
Building-based — NVL72 racks inside existing structure. This is the HQ, NOC, and primary compute facility.
It is also the factory/home base from which ADC 3K pods are deployed.

## Site
- Address: 1201 SE Evangeline Thruway, Lafayette, Louisiana
- GPS: 30.21975 N, 92.00645 W (corner of Evangeline Thruway & 16th Street)
- Parcels: 3 adjacent parcels on Chag Street — ~0.60 acres Phase 1 footprint
- Land debt: $15,000 — effectively debt-free. Owner-controlled. No lease risk.
- Adjacent: Borrower-owned commercial facility (interim ops base, NOC, storage)
- Zoning: Industrial corridor — no rezoning needed
- Utilities confirmed: 3-phase power, natural gas, LUS Fiber conduit path, municipal water

## Current Phase
Pre-deployment. Investor outreach active. Engineering complete. No hardware ordered.
Three blighted structures on site — demolition in Phase 1 scope.

## Hardware Platform
- NVIDIA Vera Rubin NVL72 (confirmed CES 2026, H2 2026 full production)
- 72 Rubin GPUs + 36 Vera CPUs per rack | HBM4 — 288 GB/GPU | NVLink 6
- Phase 1: 16 racks on 22×35 ft floor (770 sq ft) = 1,152 GPUs = 57.6 ExaFLOPS NVFP4
- TDP per rack: NOT published by NVIDIA. Contact NVIDIA Enterprise Sales for facility spec.
- Cooling: Rear-door CDU liquid cooling + glycol loop + exterior dry coolers. No chiller at Phase 1.
- PUE target: 1.04–1.08

## Power Architecture
- Primary: LUS grid (dual feed — LUS + SLEMCO available)
- Supplemental: Bloom Energy fuel cell (continuous baseload, ~300 kW per unit, stackable)
- Emergency: 2× natural gas gensets, N+1, exterior pad mount, auto-start <15s
- Distribution: 480V 3-phase → Starline T5 busway spine → rack PDUs
- Phase 1 load: ~2 MW (based on analyst estimates — confirm with NVIDIA TDP)

## Incentive Stack
- ITEP: Must file BEFORE groundbreaking. Non-negotiable. Tie to site LOI.
- HB 827: Phase 1 below $200M threshold — pursue parish-level PILOT as alternative
- Historic Tax Credits: 45% combined (NPS Part 1/2/3 application needed)
- Louisiana corporate tax: 5.5% (NOT ~25% — financial model needs correction)
- Henry Hub proximity: 40 miles — lowest natural gas input cost in the country

## Financial Model (needs update)
- CapEx: $33.2M stated (reconcile with NVIDIA pricing — unconfirmed)
- EBITDA Y3: $9.4M (based on unvalidated utilization assumptions)
- IRR: Higher than currently modeled (tax rate error — 5.5% not 25%)
- Phase 1 capacity: 520 kW across 4 nodes → site ceiling 3.2 MW

## Notion Location
MARLIE I root: 31e88f09-7e31-8121-b4d2-d96b0084cc50 (9 sections, fully populated)
Sections: Investment Thesis | Hardware | Site Specs | Government Funding | Infrastructure Partners
         ADC3K Credentials | Louisiana AI Network | Contact & Next Steps | Financial Architecture & ROI

## Investor Deck
marlie/index.html (local) | marlie/MARLIE-I-Lafayette-Partnership-SHARE.html (shareable version)
marlie/MARLIE-I-Lafayette-Partnership.pdf
