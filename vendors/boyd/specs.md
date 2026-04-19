# Boyd Corporation (Eaton) — Thermal Management for ADC
Last updated: 2026-03-30

## Ownership
- **Acquired by Eaton** — closed March 12, 2026 ($9.5B)
- Now Eaton's thermal management division (alongside Eaton electrical distribution)
- This means JP Buzzell (Eaton VP, OCP co-chair) is now ALSO the contact for cold plates + manifolds + CDUs
- HQ: Modesto, CA (retained post-acquisition)

---

## NVIDIA RVL/AVL Status
- **CONFIRMED on NVIDIA RVL** for GB200 NVL72 deployments
- Products certified: cold plates + rack manifolds + CDUs
- Pre-validated for liquid cooling integration into NVIDIA DSX reference design

---

## Product Portfolio

### Cold Plates
- High-performance copper cold plates for GPU/CPU die-level cooling
- Compatible with Blackwell GB200/GB300 form factors
- Thermal interface materials (TIMs) qualified for NVIDIA spec
- Engineering: custom geometry to match die footprint + flow optimization

### Rack Manifolds
- Supply/return headers inside the rack
- Connects cold plates (via QDs) back to CDU circuit
- Compatible with EIA, ORV3, and NVIDIA MGX rack formats

### CDUs (Cooling Distribution Units)
- Range from rack-level to row-level capacities
- Liquid-to-liquid heat exchange
- Integrated into Eaton facility power + thermal stack

---

## ADC Stack Position
- Boyd = **coldplate layer** (dies → manifold)
- CoolIT = **CDU + TCS layer** (manifold → facility cooling loop)
- Eaton acquisition creates a single-vendor option from: grid → distribution → cold plates → CDUs
- Competitive consideration: single-vendor vs. best-of-breed (CoolIT CHx2000 still outperforms on NVL72 density)

---

## Key Contact
- **JP Buzzell** — VP & Chief Architect, Global Data Center Segment, Eaton
  - Also OCP Power Distribution Sub-Project co-chair
  - Now covers facility power + thermal in one relationship
  - Contact via Eaton corporate: eaton.com/contact

## URLs
- Boyd (legacy): boydcorp.com
- Eaton Data Center: eaton.com/us/en-us/markets/data-center.html
