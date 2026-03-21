# Trappeys AI Factory — US Vendor Procurement Matrix
## Primary + Backup for Every Component — 3-Month Target, 6-Month Max
### ADC Rule: American-Made. No Exceptions. No Waiting.

---

## GENERATION — POWER SOURCES

### Solar Panels
| | Primary | Backup |
|---|---|---|
| **Vendor** | **First Solar** | **Qcells (Hanwha USA)** |
| **HQ** | Tempe, AZ | Dalton, GA |
| **US Factory** | New Iberia, LA (30 mi!) | Dalton, GA |
| **Product** | Series 7 TR1 (550W) | Q.PEAK DUO ML-G11 (420W) |
| **Why Primary** | 30 mi from site, best degradation (0.3%), CdTe thin film, humidity advantage, American steel back rails | Largest US c-Si manufacturer, readily available |
| **Lead Time** | 6-12 weeks (production line 30 mi away) | 4-8 weeks |
| **Phase 1 Qty** | 746 panels (Building #3 rooftop) | Same coverage = ~980 panels (lower wattage) |
| **Contact** | modulesales@firstsolar.com / 419-662-6899 | sales.us@qcells.com |

### Natural Gas Gensets (PRIMARY POWER — runs 24/7)
| | Primary | Backup |
|---|---|---|
| **Vendor** | **Caterpillar (Cat)** | **Cummins** |
| **HQ** | Irving, TX | Columbus, IN |
| **US Factory** | Multiple (Lafayette, IN; Griffin, GA) | Multiple (Fridley, MN; Rocky Mount, NC) |
| **Product** | CG260-16 (2 MW) or G3520C (1.5 MW) | QSK60G (1.5 MW) or HSK78G (2.5 MW) |
| **Why Primary** | Deepest dealer network in LA, parts everywhere, Cat Financial leasing, proven gas prime power | Equally proven, excellent gas engines, strong in LA |
| **Lead Time** | 12-20 weeks (standard), 6-8 weeks (dealer stock) | 12-20 weeks (standard), 8-12 weeks (emergency) |
| **Phase 1 Qty** | 1× 1 MW prime-rated gas genset | Same |
| **LA Dealer** | Louisiana Cat (multiple locations) | Cummins Sales & Service, Harahan LA |
| **Note** | Cat also makes excellent diesel backup gensets | Cummins also makes diesel — could standardize on one vendor |

### Diesel Gensets (EMERGENCY BACKUP)
| | Primary | Backup |
|---|---|---|
| **Vendor** | **Caterpillar** | **Generac** |
| **HQ** | Irving, TX | Waukesha, WI |
| **Product** | C18 (600 kW) or C32 (1 MW) | SD600-SD1000 (600 kW-1 MW) |
| **Why Primary** | Same dealer as gas genset — single service relationship | Domestic manufacturer, fast delivery, lower cost |
| **Lead Time** | 8-16 weeks | 4-8 weeks (often in stock) |
| **Phase 1 Qty** | 1× 500-750 kW diesel backup | Same |

---

## DISTRIBUTION — GETTING POWER TO THE RACKS

### 800V DC Switchgear + PDUs
| | Primary | Backup |
|---|---|---|
| **Vendor** | **Eaton** | **Powell Industries** |
| **HQ** | Cleveland, OH | Houston, TX |
| **Product** | Beam Rubin DSX (co-designed with NVIDIA) | Custom DC switchgear, bus duct |
| **Why Primary** | NVIDIA's official power partner. 800 VDC reference. Beam Rubin DSX = the standard. | 100% American, custom-engineered, publicly traded |
| **Lead Time** | 12-24 weeks (custom), 8-12 weeks (standard configs) | 16-24 weeks (custom engineered) |
| **Phase 1 Qty** | 1× 800V DC main bus, 4× rack PDUs | Same |
| **Includes** | PDUs (HDX G4), busway (PowerWave 2), microgrid controller | MV switchgear, custom bus duct, protection |

### Transformers
| | Primary | Backup |
|---|---|---|
| **Vendor** | **Eaton** | **GE Vernova** |
| **HQ** | Cleveland, OH | Cambridge, MA |
| **Product** | Dry-type transformer (480V/800V) | Prolec GE transformers (US mfg) |
| **Lead Time** | 12-20 weeks | 16-24 weeks |
| **Phase 1 Qty** | 1× step-down transformer (utility → facility) | Same |

### UPS / Battery Storage
| | Primary | Backup |
|---|---|---|
| **Vendor** | **Eaton** | **Vertiv** |
| **HQ** | Cleveland, OH | Westerville, OH |
| **Product** | 9395XC UPS + xStorage BESS | Liebert EXL S1 UPS |
| **Why Primary** | Integrates with Beam Rubin DSX, supercapacitor option, LFP lithium | Proven in compute facilities, US manufactured |
| **Lead Time** | 12-16 weeks | 10-16 weeks |
| **Phase 1 Qty** | 1× 500 kW UPS + battery rack for cloud transient buffering | Same |

---

## SOLAR BALANCE OF SYSTEM (BOS)

### MPPT Controllers / Solar Charge Controllers
| | Primary | Backup |
|---|---|---|
| **Vendor** | **SMA America** | **Enphase Energy** |
| **HQ** | Rocklin, CA (US division) | Fremont, CA |
| **Product** | Sunny Central UP (1000V+ DC input, utility scale) | IQ8 Commercial (string-level, modular) |
| **Why Primary** | Proven utility-scale MPPT, 1500V DC input, First Solar compatible | US designed/manufactured, per-panel optimization |
| **Lead Time** | 8-12 weeks | 4-8 weeks (widely stocked) |
| **Phase 1 Qty** | 5× 100 kW MPPT controllers | Equivalent string-level units |

### DC-DC Buck Converters (952V → 800V)
| | Primary | Backup |
|---|---|---|
| **Vendor** | **Eaton (integrated in Beam Rubin)** | **ABB Power Conversion** |
| **HQ** | Cleveland, OH | New Berlin, WI (US mfg) |
| **Product** | Integrated DC-DC in Beam Rubin DSX platform | PCS100 / ACS880 DC converter |
| **Why Primary** | Part of the NVIDIA reference architecture — one vendor, one system | Proven industrial DC-DC, US manufactured |
| **Lead Time** | Included in Beam Rubin lead time | 12-20 weeks |
| **Note** | This may be the cleanest path — Eaton handles the entire DC bus | ABB is backup if Eaton can't deliver custom DC-DC config |

### Mounting Racking (Metal Roof)
| | Primary | Backup |
|---|---|---|
| **Vendor** | **Unirac (now part of Enstall)** | **IronRidge** |
| **HQ** | Albuquerque, NM | Hayward, CA |
| **Product** | SolarMount, metal roof clamps, portrait config | XR1000 rail system |
| **Why Primary** | Designed for standing seam metal roofs, First Solar compatible clips | Widely available, strong dealer network |
| **Lead Time** | 4-8 weeks | 2-4 weeks (distributor stock) |
| **Phase 1 Qty** | 746 panel mounts + rail + hardware | Same |

### Combiner Boxes
| | Primary | Backup |
|---|---|---|
| **Vendor** | **SMA / Shoals Technologies** | **Bentek Solar** |
| **HQ** | Rocklin, CA / Portland, TN | Tucson, AZ |
| **Product** | String combiner with AFCI + rapid shutdown | DC combiner boxes (utility scale) |
| **Lead Time** | 6-10 weeks | 4-8 weeks |
| **Phase 1 Qty** | 15× 10-string combiners | Same |

### DC Cable + Conduit
| | Primary | Backup |
|---|---|---|
| **Vendor** | **Southwire** | **Encore Wire** |
| **HQ** | Carrollton, GA | McKinney, TX |
| **Product** | USE-2 PV wire, THHN, building wire | Same product lines |
| **Why Primary** | Largest US wire manufacturer, multiple plants | Texas-based, fast shipping to LA |
| **Lead Time** | 1-3 weeks (stock items) | 1-3 weeks |
| **Phase 1 Qty** | ~15,000 ft string wire + ~2,000 ft trunk cable | Same |

---

## COOLING

### Dry Coolers (Heat Rejection)
| | Primary | Backup |
|---|---|---|
| **Vendor** | **Baltimore Aircoil (BAC)** | **Heatcraft (Lennox)** |
| **HQ** | Jessup, MD | Stone Mountain, GA |
| **Product** | TrilliumSeries dry cooler | SmartComfort dry cooler |
| **Lead Time** | 10-16 weeks | 8-12 weeks |
| **Phase 1 Qty** | 1× 500 kW dry cooler (for 4 liquid-cooled racks) | Same |

### HVLS Fans (Dehumidification + Airflow)
| | Primary | Backup |
|---|---|---|
| **Vendor** | **Big Ass Fans** | **Hunter Industrial** |
| **HQ** | Lexington, KY | Memphis, TN |
| **Product** | Powerfoil X4 (24 ft) | Titan HVLS (24 ft) |
| **Lead Time** | 4-8 weeks | 4-8 weeks |
| **Phase 1 Qty** | 2-4× fans for Building #3 | Same |

---

## CONTROL + MONITORING

### Power Plant Control System
| | Primary | Backup |
|---|---|---|
| **Vendor** | **Siemens Energy (US)** | **Eaton (Brightlayer)** |
| **HQ** | Alpharetta, GA | Cleveland, OH |
| **Product** | Omnivise Hybrid Control (OHC) | Brightlayer EPMS + Microgrid Controller |
| **Why Primary** | Dispatch optimizer every 15 min, proven microgrid control, black start | Integrates with Beam Rubin DSX, simpler, lower cost |
| **Lead Time** | 16-24 weeks (design + commission) | 12-16 weeks |
| **Note** | Siemens for full-scale (Willow Glen). Eaton may be simpler for Phase 1 Trappeys. |

### Fire Suppression
| | Primary | Backup |
|---|---|---|
| **Vendor** | **Fike Corporation** | **Kidde (Carrier)** |
| **HQ** | Blue Springs, MO | Mebane, NC |
| **Product** | FM-200 / Novec 1230 clean agent | Sapphire clean agent |
| **Lead Time** | 8-12 weeks | 8-12 weeks |
| **Phase 1 Qty** | 1× system for Building #3 compute area | Same |

### Fire Detection (Early Warning)
| | Primary | Backup |
|---|---|---|
| **Vendor** | **Xtralis (Honeywell)** | **System Sensor (Honeywell)** |
| **HQ** | Norwood, MA | St. Charles, IL |
| **Product** | VESDA-E VEA aspirating smoke detection | Beam detection + point sensors |
| **Lead Time** | 4-8 weeks | 2-4 weeks |

---

## NETWORKING + FIBER

### LUS Fiber
| | Primary | Only Option |
|---|---|---|
| **Vendor** | **LUS Fiber** | — |
| **Product** | Carrier-grade municipal fiber | |
| **Note** | 0.8 miles from site. Part of city infrastructure upgrade pitch. | |
| **Lead Time** | Depends on city coordination | |

### InfiniBand (Compute Fabric)
| | Primary | Backup |
|---|---|---|
| **Vendor** | **NVIDIA (Quantum switches)** | None — NVIDIA only |
| **Product** | Quantum-2 InfiniBand switches, ConnectX-7/8 NICs | |
| **Lead Time** | Allocation-dependent. NPN → DGX-Ready helps. | |

---

## PHASE 1 CRITICAL PATH (3-MONTH TARGET)

### Week 1-2: Orders Placed
- [ ] First Solar: 746 panels (Building #3)
- [ ] Cat/Cummins: 1 MW gas genset (check dealer stock FIRST)
- [ ] Eaton: Beam Rubin DSX quote + lead time confirmation
- [ ] Southwire: DC wire order (stock items, ships fast)
- [ ] Unirac/IronRidge: Mounting hardware
- [ ] Big Ass Fans: 2-4 HVLS units

### Week 3-6: Site Prep
- [ ] Roof assessment (structural engineer — 316,500 lbs total, Phase 1 = 63,300 lbs)
- [ ] Gas connection (tie into existing trunk line)
- [ ] Electrical permit (City of Lafayette)
- [ ] LUS Fiber connection request
- [ ] Concrete pad prep for genset + switchgear

### Week 6-10: Installation
- [ ] Mounting racking installed
- [ ] Panels installed (Building #3 first)
- [ ] Genset delivered and set
- [ ] Switchgear/PDU installed
- [ ] DC wiring: panels → combiners → MPPT → 800V bus

### Week 10-12: Commission
- [ ] String testing (Voc, Imp verification per string)
- [ ] Genset commissioning
- [ ] 800V DC bus energized
- [ ] Grid interconnect (sell-back) — LUS agreement
- [ ] Fire suppression tested
- [ ] VESDA online

### Week 12: POWER ON
- [ ] First rack powered
- [ ] Production workload running
- [ ] Monitoring live

---

## BUDGET ESTIMATE — PHASE 1 (Building #3, 410 kW Solar + 1 MW Gas)

| Category | Estimated Cost | Notes |
|---|---|---|
| Solar panels (746× TR1) | $280,000-350,000 | ~$0.37-0.47/W before ITC |
| Mounting + BOS | $80,000-120,000 | Racking, wire, combiners |
| MPPT + DC-DC converters | $60,000-100,000 | 5× 100 kW units |
| 800V DC switchgear (Eaton) | $150,000-250,000 | Beam Rubin DSX config |
| Gas genset (1 MW Cat) | $300,000-500,000 | Prime rated, enclosed |
| Active rectifier (AC→DC) | $50,000-80,000 | For gas → 800V bus |
| UPS + battery buffer | $100,000-180,000 | Cloud transient ride-through |
| Fire suppression + detection | $40,000-70,000 | Novec 1230 + VESDA |
| Electrical installation labor | $100,000-150,000 | Licensed electricians |
| Roof structural engineering | $15,000-25,000 | Load analysis |
| Permits + inspections | $10,000-20,000 | City of Lafayette |
| **SUBTOTAL** | **$1,185,000-1,845,000** | |
| **30% Federal Solar ITC** | **(-$84,000 to -$105,000)** | On solar components only |
| **NET PHASE 1** | **$1,100,000-1,740,000** | |

---

*Prepared by ADC — Advantage Design & Construction*
*scott@adc3k.com | adc3k.com*
*All vendors US-manufactured. No exceptions.*
