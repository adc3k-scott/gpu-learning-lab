# ADC Power Economics — Willow Glen Terminal

## The 4-Layer Power Stack

```
LAYER 1: Natural Gas (CCGT/Reciprocating)   PRIMARY · 24/7 baseload · Henry Hub pricing
LAYER 2: Solar + Battery (BESS)             OFFSET · peak shaving · ITC subsidized
LAYER 3: Entergy Grid                       BACKUP · negotiated industrial rate
LAYER 4: Diesel Gensets                     EMERGENCY · on-site fuel · <200 hrs/yr
```

---

## Layer 1: Natural Gas — Henry Hub Pricing

### Current Pricing (March 2026)
| Metric | Value |
|--------|-------|
| Henry Hub spot (2026-03-16) | $3.03/MMBtu |
| April 2026 contract | $3.07/MMBtu |
| EIA 2026 full-year projection | $3.76/MMBtu |
| Delivered cost (spot + transport) | $5-7/MMBtu (est) |

### Heat Rate Conversion (Fuel → Electricity)
| Technology | Heat Rate (Btu/kWh) | Efficiency | Fuel Cost at $3.07/MMBtu |
|------------|---------------------|------------|--------------------------|
| Combined cycle gas turbine (CCGT) | 7,000 | ~49% | $21.49/MWh |
| Reciprocating engine | 8,000-8,400 | ~42-43% | $24.56/MWh |
| Simple cycle gas turbine | 9,000-15,000 | ~23-38% | $27.63-46.05/MWh |

**Formula:** Fuel $/MMBtu × Heat Rate (Btu/kWh) ÷ 1,000 = $/MWh

### All-In Gas Generation Cost
| Scenario | Fuel $/MWh | O&M + Emissions | Total $/MWh |
|----------|------------|-----------------|-------------|
| CCGT at $3.07/MMBtu | $21.49 | $5-10 | $26-32 |
| CCGT at $3.76/MMBtu (EIA avg) | $26.32 | $5-10 | $31-36 |
| Reciprocating at $3.07/MMBtu | $24.56 | $5-10 | $30-35 |

**ADC baseline:** ~$27-30/MWh for on-site gas generation (CCGT, Henry Hub spot).

---

## Layer 2: Solar + Battery

### Solar in Louisiana (St. Gabriel, 30.25°N)
| Metric | Value |
|--------|-------|
| Peak sun hours (fixed tilt) | 4.5 hrs/day avg |
| Peak sun hours (1-axis tracking) | 6.4 hrs/day |
| Capacity factor (fixed) | 16-25% |
| Unsubsidized LCOE | $50-60/MWh |
| With 30% ITC | $35-42/MWh |
| With ITC + domestic content + energy community | $28-35/MWh (potential) |

### Federal Tax Credits (2026)
- **30% Investment Tax Credit (ITC)** — projects must begin construction by July 4, 2026
- **+10% domestic content bonus** — US-made panels/inverters
- **+10% energy community bonus** — if Willow Glen qualifies (former fossil fuel site — likely yes)
- **100% first-year MACRS depreciation**
- **Total potential CAPEX reduction: 30-50%**

### Battery Storage (BESS)
| Metric | Value |
|--------|-------|
| Capital cost (4-hr system, installed) | $334/kWh |
| Battery pack alone | ~$105/kWh |
| 3 MW / 12 MWh system total | ~$4.01M |
| Round-trip efficiency | ~88% |
| Degradation | 2-3%/year |
| Replacement cycle | 10-15 years |
| O&M | $10-15/kWh/year |
| Levelized cost of stored energy | $80-100/MWh |

### Combined Solar + BESS Cost
| Configuration | $/MWh |
|---------------|-------|
| Solar direct (daytime only) | $35-42 |
| Solar + 4hr BESS (shifted to evening) | $115-140 |

---

## Layer 3: Entergy Grid (Backup)

### Industrial Rates
- Entergy Louisiana is the utility in Iberville Parish
- No published standard rate for large industrial — all custom negotiated
- Standard industrial range: $0.06-0.08/kWh ($60-80/MWh)
- **For 50+ MW anchor load (data center precedent): $0.04-0.06/kWh ($40-60/MWh)**

### Recent Precedent (March 2026)
- Entergy announced **$5B in customer savings** over 20 years from data center agreements
- Amazon, Meta, Hut 8, Avaio Digital all signed preferential rate agreements
- Amazon deal in Mississippi reduced residential bills by 16%
- **Utilities will build generation capacity for anchor loads** — Entergy co-investing with customers

### Grid Buyback (Export Revenue)
- MISO wholesale rates for Louisiana zone
- Expected buyback: $30-60/MWh (variable by season/time-of-use)

---

## Layer 4: Diesel (Emergency Only)
| Metric | Value |
|--------|-------|
| Generation cost | $150-200/MWh |
| Expected annual runtime | <200 hours |
| Purpose | True emergency, pipeline-independent |

---

## Blended Power Cost — ADC Willow Glen

### Phase 1A (3 MW) — CORRECTED
**Note:** At 3 MW, CCGT is not available (minimum ~50 MW). Use reciprocating gas engines (Cat CG260, Wartsila, Jenbacher). Solar at this scale is commercial, not utility-scale (higher LCOE).

| Source | Share | $/MWh | Weighted | Notes |
|--------|-------|-------|----------|-------|
| Gas recip engine (baseload) | 70% | $55-65 | $38.50-45.50 | Heat rate 8.0 MMBtu/MWh, all-in |
| Solar + battery (offset) | 15% | $50-70 | $7.50-10.50 | Commercial-scale, higher than utility |
| Grid / Entergy (backup) | 14% | $70 | $9.80 | Industrial rate |
| Diesel (emergency) | 1% | $250 | $2.50 | Pipeline-independent |
| **Phase 1A blended** | **100%** | | **$58-68/MWh** | **$0.058-0.068/kWh** |

**Phase 1A annual power cost at 3 MW:** ~$1.5-1.8M/yr

### At Scale (100+ MW) — CCGT Unlocked
At 100+ MW, combined cycle gas turbines become viable ($38-48/MWh all-in) and solar hits utility-scale LCOE.

| Source | Mix | $/MWh | Weighted | Notes |
|--------|-----|-------|----------|-------|
| Gas CCGT (baseload) | 75% | $38-48 | $28.50-36.00 | Henry Hub, combined cycle |
| Solar + battery (offset) | 18% | $30-40 | $5.40-7.20 | Utility-scale, ITC subsidized |
| Grid (backup) | 6% | $70 | $4.20 | Entergy industrial |
| Diesel (emergency) | 1% | $250 | $2.50 | |
| **At-scale blended** | **100%** | | **$40-50/MWh** | **$0.04-0.05/kWh** |
| **With MISO ancillary offset** | | | **$36-46/MWh** | ~$4M/yr credit |

**ADC target blended cost: $0.04-0.05/kWh at 100+ MW scale**
**Phase 1A reality: $0.058-0.068/kWh (still 20-30% below Entergy grid-only)**

---

## MISO Market Access — Ancillary Revenue

Willow Glen is in MISO South (Entergy Louisiana joined MISO in 2013).

### Ancillary Services Pricing (January 2026)
| Service | $/MWh | Notes |
|---------|-------|-------|
| Frequency regulation (Day-Ahead) | $27.88 | Up 59% YoY from $17.34 avg in 2025 |
| Spinning reserves | $5-15 | Varies by season |
| Demand response | $10-30 | DRR-Type II only |
| Ramp capability | $20-50 | Emerging market, fast-ramping |

### Revenue Potential (At Scale)
| Service | Capacity | Hours/day | Annual Revenue |
|---------|----------|-----------|----------------|
| Frequency regulation | 50 MW | 2 hrs avg | ~$1.02M/yr |
| Spinning reserves | 100 MW | 8 hrs | ~$2.92M/yr |
| **Combined ancillary** | | | **~$4M/yr** |

---

## Competitive Position

| Benchmark | $/kWh | ADC Phase 1 (3 MW) | ADC At Scale (100+ MW) |
|-----------|-------|---------------------|------------------------|
| U.S. industrial average | $0.073 | $0.058-0.068 (20-30% lower) | $0.04-0.05 (30-45% lower) |
| Data center industry target | $0.047-0.05 | Above target (small scale) | At or below target |
| Best hyperscaler (hydro regions) | <$0.04 | Not competitive at Phase 1 | Approaching at scale |
| Crusoe stranded gas model | $0.02-0.03 | Not competitive at Phase 1 | Approaching with optimization |

### Why Willow Glen is a Power Advantage
1. **On-site gas** — Henry Hub pipeline corridor, ~$27/MWh CCGT, low fuel volatility
2. **Solar + ITC** — 4.5 PSH, 30-50% CAPEX reduction with federal credits
3. **Former power plant site** — existing infrastructure, environmental permits, transmission designed for massive load (2,200 MW historical)
4. **230kV Entergy substation on-site** — no interconnect build needed
5. **Entergy co-investment precedent** — utility will build generation for anchor tenants
6. **MISO market access** — ancillary services revenue (~$4M/yr at scale)
7. **Energy community bonus** — former fossil fuel site likely qualifies for +10% ITC

---

## What's Still Needed

1. **Pipeline access fee** — confirm transport cost ($2-4/MMBtu) from Henry Hub to Willow Glen
2. **Entergy rate negotiation** — contact for custom industrial rate (50+ MW commitment)
3. **Solar EPC quote** — get from solar partner meeting (2026-03-20)
4. **Gas turbine selection** — Siemens SGT-800 vs reciprocating engines for Phase 1 scale
5. **BESS sizing** — 4-6 hour system for peak shaving + freq regulation
6. **Energy community certification** — confirm Willow Glen qualifies for +10% ITC bonus
7. **MISO registration** — register as market participant for ancillary services
