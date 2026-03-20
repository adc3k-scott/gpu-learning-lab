# ADC Capital Expenditure Model

## Phase 1A — First Racks (3 MW)
Target: Willow Glen 20K SF warehouse

### Facility CapEx
| Item | Estimate | Notes |
|------|----------|-------|
| Warehouse lease/deposit | TBD | CBRE negotiation with WGT |
| MEP buildout (power, plumbing, fire) | TBD | ADC is licensed GC — pull own permits |
| Facility water loop + heat rejection | TBD | Cooling towers or dry coolers |
| Eaton power distribution (PDUs, switchgear, UPS) | TBD | Beam Rubin DSX platform |
| Siemens Omnivise (control system) | $300K-700K | Software + hardware + integration |
| InfiniBand spine (Quantum switches) | TBD | Per-port pricing from NVIDIA |
| OOB management network | $50-100K | Standard enterprise networking |
| Physical security + environmental | $100-200K | Cameras, access control, sensors |
| Permitting + engineering | $50-100K | In-house GC |
| **Facility subtotal** | **TBD** | |

### Compute CapEx
| Item | Estimate | Notes |
|------|----------|-------|
| NVIDIA Vera Rubin NVL72 racks | TBD | UNPUBLISHED pricing. Critical gap. |
| Groq 3 LPX racks (~25% capacity) | TBD | UNPUBLISHED pricing |
| BlueField-4 STX storage | TBD | Part of DSX order |
| Spectrum-6 networking | TBD | Part of DSX order |
| **Compute subtotal** | **TBD** | |

### Power Generation CapEx
| Item | Estimate | Notes |
|------|----------|-------|
| Solar array (ground-mount, Phase 1) | TBD | From solar partner meeting |
| Battery storage (BESS) | TBD | Eaton xStorage or third-party |
| Natural gas gensets | TBD | Siemens SGT-800 or reciprocating |
| Diesel gensets (emergency) | $200-500K | Standard industrial backup |
| Grid interconnect engineering | $0 | Already live (230kV Entergy substation) |
| **Power subtotal** | **TBD** | |

### Industry Benchmarks
- AI-ready facility: $8-15M per MW (industry range)
- Phase 1A at 3 MW: $24-45M (benchmark range)
- Hut 8 River Bend: $17M for new substation + $34M for 190 CDUs at 245 MW scale

---

## Phase 1B — Scale to 6 MW
- Additional racks on existing InfiniBand spine
- Groq LPX inference racks added
- Power generation expansion (solar + battery)
- Incremental CapEx: primarily compute hardware

## Phase 1C — Warehouse Maxed (12 MW)
- Full fat-tree InfiniBand topology
- Warehouse at capacity
- Solar farm expanded
- Token revenue at scale

## Phase 2 — Campus Expansion (50+ MW, Y2-3)
- 2-3 new buildings on acreage
- Major solar farm (ground-mount, 200+ acres)
- Extended InfiniBand across buildings
- Siemens SGT-800 gas turbines (dedicated on-site generation)
- Eaton 800 VDC architecture for 1 MW rack support

## Phase 3 — Full Campus (100+ MW, Y3-5)
- Largest DSX-compliant deployment in Louisiana
- Grid export revenue
- NVIDIA reference site

---

## What's Missing (Blocks the Financial Model)
1. **NVIDIA rack pricing** — cannot build CapEx model without hardware cost
2. **Eaton Beam Rubin DSX pricing** — need quote for power distribution
3. **Solar EPC cost** — get from solar partner meeting ($/kW installed)
4. **Gas turbine pricing** — Siemens SGT-800 or alternative for Phase 1 scale
5. **Warehouse lease terms** — CBRE/Bryce French negotiation
6. **Battery storage pricing** — $/kWh for BESS at 3 MW scale

## Use of Proceeds (Draft — For Raise Deck)
| Use | Amount | What It Gets Us |
|-----|--------|----------------|
| Warehouse lease + buildout | TBD | Facility ready for racks |
| Power infrastructure | TBD | Generation + distribution |
| NVIDIA hardware (Phase 1A) | TBD | First racks operational |
| Working capital (6 months) | TBD | Ops runway to first revenue |
| **Total raise** | **TBD** | **Phase 1A operational, first token revenue** |
