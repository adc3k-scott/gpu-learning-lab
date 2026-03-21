# Trappeys AI Factory — Electrical Architecture
## Prepared by ADC (Advantage Design & Construction)
### For discussion with First Solar and electrical engineering partners
### Date: March 2026

---

## 1. POWER HIERARCHY (LOCKED)

```
┌─────────────────────────────────────────────────────────────────┐
│                    TRAPPEYS POWER STACK                         │
│                                                                 │
│  LAYER 1: SOLAR (First Solar Series 7 TR1)                     │
│  ├── 2.05 MW rooftop DC                                        │
│  ├── Offset + ITC revenue + green story                        │
│  ├── DC-coupled to 800V bus (no inverters)                     │
│  └── When sun's out: reduces gas consumption                   │
│                                                                 │
│  LAYER 2: NATURAL GAS GENSETS (PRIMARY BACKBONE)               │
│  ├── Runs 24/7 — carries the main load                         │
│  ├── Henry Hub pricing — cheapest energy in the country         │
│  ├── Gas confirmed on-site (trunk lines + ATMOS hub nearby)    │
│  └── THIS IS THE COMPETITIVE ADVANTAGE                         │
│                                                                 │
│  LAYER 3: DIESEL GENSETS (EMERGENCY)                           │
│  ├── On-site fuel — pipeline independent                       │
│  └── Kicks in if gas supply interrupted                        │
│                                                                 │
│  LAYER 4: GRID / LUS (SELL-BACK ONLY)                          │
│  ├── NOT a power source — excess goes BACK to grid             │
│  ├── LUS Pin Hook Substation right next door                   │
│  └── Revenue opportunity, not dependency                       │
└─────────────────────────────────────────────────────────────────┘
```

**Key message: We don't need the grid. We don't scare anybody. We SELL BACK to the grid.**

---

## 2. SOLAR ARRAY — FIRST SOLAR SERIES 7 TR1

### Panel Specifications (from datasheets)
| Spec | Value |
|---|---|
| Model | FS-7550A-TR1 (US market, high bin) |
| Power | 550W per panel |
| Efficiency | 19.7% |
| Dimensions | 2300mm × 1216mm (7.55 ft × 3.99 ft = 30.14 sq ft) |
| Weight | 38.47 kg (84.8 lbs) per panel |
| Vmax (MPP) | 190.4V DC |
| Voc (open circuit) | 228.8V DC |
| Imax | 2.89A |
| Isc | 3.08A |
| Max system voltage | 1,500V DC |
| Temp coeff (Pmax) | -0.32%/°C |
| Temp coeff (Voc) | -0.28%/°C |
| Degradation | 0.3%/year (industry best, 30-year warranty) |
| Mounting | Portrait only, galvanized steel back rails |
| Load rating | 2,400 Pa |

### Rooftop Layout (Site Survey 2026-03-21)

| Building | Dimensions | Rooftop Sq Ft | Panels | Power (kW) | Weight (lbs) |
|---|---|---|---|---|---|
| Rear High Ground (#4) | 150 × 250 ft | 37,500 | 1,244 | 684 | 105,500 |
| Middle High (#3) | 75 × 300 ft | 22,500 | 746 | 410 | 63,300 |
| Middle Low (#2) | 100 × 300 ft | 30,000 | 995 | 547 | 84,400 |
| Front Lower (#1) | 75 × 300 ft | 22,500 | 746 | 410 | 63,300 |
| **TOTAL ROOFTOP** | | **112,500** | **~3,731** | **2,052** | **~316,500** |

### Additional Solar Potential (not yet surveyed)
- Ground-mount around water tower base
- Infrastructure yard perimeter
- Adjacent parcels if acquired
- Estimated additional: 500 kW–1 MW possible

### Annual Production Estimate
| Metric | Value |
|---|---|
| Peak sun hours (Lafayette, LA) | ~4.5 hrs/day average |
| Annual production | ~3,370 MWh/year |
| Capacity factor | ~18.7% |
| 30-year warranted output | 91% of nameplate at year 30 |
| Annual value (@$0.08/kWh avoided cost) | ~$270,000/year |

---

## 3. THE 800 VDC ARCHITECTURE

### Why 800V DC?
NVIDIA's DSX reference design specifies 800 VDC power distribution to compute racks. Traditional facilities use 480V AC, which requires multiple conversion steps. Going DC-direct from solar eliminates conversions and saves 5% efficiency.

### String Configuration
```
5 panels in series = 1 string
├── Voltage at max power point: 5 × 190.4V = 952V DC
├── Open circuit voltage: 5 × 228.8V = 1,144V DC
├── Current at max power: 2.89A
├── String power: 2,751W (2.75 kW)
└── Well under 1,500V system limit in all conditions
```

### Temperature Effects (Lafayette climate)
| Condition | Cell Temp | String Vmpp | String Voc | Status |
|---|---|---|---|---|
| STC (lab) | 25°C | 952V | 1,144V | Reference |
| Summer peak | 45°C | 891V | 1,080V | Above 800V — OK |
| Winter morning | 5°C | 1,005V | 1,208V | Under 1,500V — OK |
| Extreme cold | -5°C | 1,032V | 1,244V | Under 1,500V — OK |

**Result: 800V bus stays fed in all Lafayette weather conditions.**

### String Count Per Building
| Building | Panels | Strings (÷5) | String Power | Building DC Output |
|---|---|---|---|---|
| Rear High (#4) | 1,244 | 248 | 2.75 kW | 682 kW |
| Middle High (#3) | 746 | 149 | 2.75 kW | 410 kW |
| Middle Low (#2) | 995 | 199 | 2.75 kW | 547 kW |
| Front Lower (#1) | 746 | 149 | 2.75 kW | 410 kW |
| **TOTAL** | **3,731** | **745** | | **2,049 kW** |

### DC Power Path
```
SOLAR PANELS (rooftop)
    │
    │  5-panel series strings (952V DC nominal)
    │
    ▼
┌──────────────────┐
│  STRING COMBINER  │  Fused, per-string AFCI, rapid shutdown
│  BOXES (rooftop)  │  NEC 690.12 compliant
└────────┬─────────┘
         │
         │  Combined DC feeds (952V, multiple strings per combiner)
         │
         ▼
┌──────────────────┐
│  MPPT CONTROLLERS │  Maximum Power Point Tracking
│  (per building)   │  Adjusts load to extract max power
│                   │  Input: 800-1,100V DC (variable)
│                   │  Output: regulated DC
└────────┬─────────┘
         │
         │  Regulated DC
         │
         ▼
┌──────────────────┐
│  DC-DC CONVERTER  │  Buck converter: 952V → 800V
│  (switchgear rm)  │  98%+ efficiency
│                   │  Galvanic isolation
└────────┬─────────┘
         │
         │  800V DC bus
         │
         ▼
┌──────────────────────────────────────────────┐
│              800V DC BUS                      │
│                                              │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐     │
│  │ Solar   │  │ Gas Gen │  │ Battery │     │
│  │ DC feed │  │ AC→DC   │  │ Storage │     │
│  │ (direct)│  │ rectify │  │ (buffer)│     │
│  └────┬────┘  └────┬────┘  └────┬────┘     │
│       │            │            │            │
│       └────────────┼────────────┘            │
│                    │                         │
│              ┌─────▼─────┐                   │
│              │  800V DC   │                   │
│              │  BUSBAR    │                   │
│              └─────┬─────┘                   │
│                    │                         │
│     ┌──────────────┼──────────────┐          │
│     ▼              ▼              ▼          │
│  ┌──────┐     ┌──────┐     ┌──────┐        │
│  │Rack 1│     │Rack 2│     │Rack N│        │
│  │NVL72 │     │NVL72 │     │NVL72 │        │
│  │800VDC│     │800VDC│     │800VDC│        │
│  └──────┘     └──────┘     └──────┘        │
└──────────────────────────────────────────────┘
```

### Switching Logic — Multi-Source 800V Bus
```
NORMAL OPERATION (sunny day):
  Solar → 800V bus (primary feed)
  Gas genset → 800V bus (supplements, carries base load)
  Battery → standby (charging from excess)

CLOUDY / NIGHT:
  Gas genset → 800V bus (carries full load)
  Solar → zero or minimal
  Battery → supplements transients

EMERGENCY (gas supply interrupted):
  Diesel genset → 800V bus (via AC rectifier)
  Battery → bridge power during switchover (~30 seconds)
  Solar → whatever's available

EXCESS PRODUCTION (sunny day, low compute load):
  Solar excess → battery charging
  Battery full → inverter → grid sell-back (LUS)
  Revenue from grid: net metering or PPA
```

### Efficiency Comparison
| Architecture | Solar→Rack Efficiency | Annual Loss on 2 MW |
|---|---|---|
| Traditional AC (inverter + transformer + PSU) | ~92% | ~160 MWh wasted |
| **DC-direct (MPPT + DC-DC buck)** | **~97%** | **~60 MWh wasted** |
| **Savings** | **+5%** | **~100 MWh/year saved** |

At $0.08/kWh, that's ~$8,000/year in avoided losses. Small on its own, but at scale (Willow Glen 30+ MW) it becomes $120,000+/year.

---

## 4. GAS GENSET INTEGRATION

### How Gas Ties Into 800V DC
Gas generators produce AC power (typically 480V 3-phase). To feed the 800V DC bus:

```
GAS GENSET (natural gas, runs 24/7)
    │
    │  480V AC 3-phase output
    │
    ▼
┌──────────────────┐
│  ACTIVE RECTIFIER │  AC → DC conversion
│  (thyristor or    │  480V AC → 800V DC
│   IGBT based)     │  95-97% efficiency
│                   │  Power factor correction built in
└────────┬─────────┘
         │
         │  800V DC
         │
         ▼
    800V DC BUS (same bus as solar)
```

### Gas Genset Sizing (Phased)
| Phase | Racks | IT Load | Total Load (1.3 PUE) | Genset Size |
|---|---|---|---|---|
| Phase 1 (start) | 4 | 520 kW | ~675 kW | 1 MW genset |
| Phase 2 | 8 | 1,040 kW | ~1,350 kW | 1.5 MW genset |
| Phase 3 | 20 | 2,600 kW | ~3,380 kW | 2× 2 MW gensets |
| Phase 4 | 36 | 4,680 kW | ~6,080 kW | 3× 2.5 MW gensets |
| Full buildout | 50+ | 6,500+ kW | ~8,450 kW | 4× 2.5 MW gensets |

### Gas Supply
- ATMOS Energy gas pipeline hub confirmed at Pinhook (photo evidence)
- Gas trunk lines running through Middle Low building
- Gas heaters throughout buildings (existing infrastructure)
- Henry Hub pricing: ~$2-3/MMBtu = $0.02-0.03/kWh fuel cost
- Recip engine efficiency: ~40% = $0.05-0.07/kWh delivered

---

## 5. GRID INTERCONNECTION (SELL-BACK ONLY)

### LUS Pin Hook Substation
- Curtis Rodemacher building — right next door (photo evidence)
- Above-ground high-voltage switchyard
- New poles running to Public Works facility adjacent to Trappeys
- Established infrastructure — short interconnection path

### Grid Strategy
- **NOT a power source** — we generate our own
- **Sell-back only** — excess solar + gas capacity sold to LUS
- Net metering or PPA (Power Purchase Agreement) with LUS
- Revenue stream, not a dependency
- Infrastructure improvement opportunity: propose buried utilities to city as joint project

### City Infrastructure Pitch
- "We're modernizing this corridor anyway — let's bury the lines together"
- ADC buries fiber + DC power conduit
- LUS buries distribution lines
- City gets upgraded infrastructure, ADC gets connectivity
- Shared trench = shared cost
- Cannery Street area needs it — exposed HV lines are aging

---

## 6. PROTECTION & SAFETY

### Solar DC Protection (NEC 690)
- **String fusing** — each 5-panel string individually fused
- **Arc fault detection (AFCI)** — NEC 690.11 required for DC systems
- **Ground fault detection (GFDI)** — NEC 690.41
- **Rapid shutdown** — NEC 690.12: within 30 seconds, all conductors outside array boundary must be < 80V
- **Disconnect switches** — per building, at combiner boxes, at DC bus entry
- **Signage** — NEC 690.56: labels at all disconnect points

### 800V DC Bus Protection
- **Bus overcurrent protection** — DC-rated breakers (not AC breakers)
- **Isolation monitoring** — continuous ground fault monitoring on ungrounded bus
- **Arc flash** — 800V DC arc flash analysis required, PPE rated for DC arc energy
- **Emergency shutdown** — single-button kills all sources to bus

### Fire Suppression
- Existing fire suppression piping in Middle Low building (confirmed on site)
- Compute areas: clean agent (FK-5-1-12 or Novec 1230)
- Non-compute: standard wet pipe sprinkler
- VESDA early warning aspiration detection in compute rooms

---

## 7. WHAT TO TELL FIRST SOLAR

### The Pitch
"We're building Louisiana's first AI factory at the historic Trappeys Cannery in Lafayette — half a mile from our existing facility, 30 miles from your New Iberia factory. We need 3,731 Series 7 TR1 panels for 2.05 MW of rooftop solar across 112,500 square feet of roof space. We're wiring DC-direct into an 800 volt bus — no inverters — feeding NVIDIA compute racks. Your panels go from your production line to our roof in a U-Haul. We want your name on the water tower."

### What We Need From Them
1. **Pricing** — ~3,731 panels (FS-7550A-TR1, 550W high bin)
2. **Structural engineering support** — roof load analysis for 316,500 lbs of panels
3. **Mounting system recommendation** — back rail compatible racking for metal rooftops
4. **DC string design review** — validate 5-panel series string for 800V bus application
5. **EPC referral** — their preferred installer in Louisiana (or we hire our own)
6. **Delivery logistics** — New Iberia to Lafayette, 30 miles, returnable packaging
7. **Warranty terms** — 12-year product + 30-year linear performance confirmation
8. **Branding partnership** — water tower logo, showcase installation, case study

### What We Offer Them
1. **Showcase installation** — 2 MW, 30 miles from factory, tours for their customers
2. **Water tower branding** — their logo on the most visible landmark on Evangeline Thruway
3. **American-made story** — Louisiana factory, Louisiana installation, Louisiana AI factory
4. **Ongoing business** — Willow Glen (30+ MW), edge nodes, every ADC site = First Solar
5. **PR value** — "AI factory powered by panels made 30 miles away" = press coverage
6. **800V DC innovation** — cutting-edge application they can reference in their marketing

### Contact
- modulesales@firstsolar.com
- 419-662-6899
- First Solar, Inc. — 1400 Corporate Drive, Iberia Parish, LA (New Iberia factory)

---

## 8. PHASE 1 BILL OF MATERIALS (ELECTRICAL)

### Solar (Phase 1 — Building #3 rooftop only, 410 kW)
| Item | Qty | Notes |
|---|---|---|
| First Solar FS-7550A-TR1 panels | 746 | 550W, portrait mount |
| Mounting racking (metal roof) | ~746 sets | Back rail clips, portrait |
| String combiner boxes (10-string) | 15 | Fused, AFCI, rapid shutdown |
| DC cable (USE-2, 10 AWG) | ~15,000 ft | Panel to combiner |
| DC trunk cable (4/0 AWG) | ~2,000 ft | Combiner to switchgear |
| MPPT controller (100 kW) | 5 | 1000V input, DC output |
| DC-DC buck converter (100 kW) | 5 | 952V → 800V, 98%+ eff |
| 800V DC switchgear | 1 | Main bus, breakers, monitoring |
| Grounding kit | 1 | Equipment + system ground |
| Monitoring (revenue grade meter) | 1 | For net metering / ITC |

### Gas (Phase 1 — 1 MW genset)
| Item | Qty | Notes |
|---|---|---|
| Natural gas genset (1 MW) | 1 | Cat/Cummins, prime rated |
| Active rectifier (480V AC → 800V DC) | 1 | 95%+ efficiency |
| Gas service connection | 1 | Tie into existing trunk line |
| Fuel management system | 1 | Metering, pressure reg |
| Sound attenuation enclosure | 1 | Outdoor rated |

### Grid Interconnect (Phase 1 — sell-back)
| Item | Qty | Notes |
|---|---|---|
| Grid-tie inverter (for sell-back) | 1 | DC bus → AC for LUS |
| Utility meter (bidirectional) | 1 | LUS net metering |
| Interconnection agreement | 1 | LUS application |
| Transfer switch (manual) | 1 | Grid disconnect |

---

*Prepared by ADC — Advantage Design & Construction*
*scott@adc3k.com | adc3k.com*
