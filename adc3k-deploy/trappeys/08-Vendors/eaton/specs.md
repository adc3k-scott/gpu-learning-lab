# Eaton — Complete 800V DC Stack for ADC
Last updated: 2026-03-25

## Beam Rubin DSX Platform (Co-Designed with NVIDIA)
- End-to-end 800V DC from grid to chip
- Supports 130+ kW per rack (Vera Rubin NVL72)
- Scales from MW to hundreds of MW
- Supercapacitor fast-cycle backup
- ORV3-compatible busbar distribution
- SimReady 3D assets for Omniverse digital twin
- NOW includes Boyd Thermal liquid cooling (grid-to-chip complete)
- First deployments: late 2026 / early 2027
- **When NVIDIA says "build to DSX spec" the power blueprint IS Eaton**

## Key Contact: JP Buzzell
- VP and Chief Architect, Global Data Center Segment
- Co-chair of OCP Power Distribution Sub-Project
- Led GTC 2026 sessions. THE person driving 800V DC at Eaton.

## The Full Grid-to-Chip Stack
```
13.8 kV AC -> MV Switchgear (5-15 kV) -> 800V DC Rectifiers -> ORV3 Busbar
-> +/-400V DC Sidecar (800 kW/row) -> 64:1 LLC (NVIDIA Kyber) -> 12V at GPU
```

## Products

### ORV3 Sidecar (800V DC)
- +/-400V DC power rack
- Integrates PSU, BBU, capacitor tray
- Up to 800 kW per rack row
- Replaces traditional PDUs in 800V DC architecture

### PowerWave 2 Busway (AC applications)
- 250A to 1000A, overhead track-style
- Class 0.5 accuracy, Modbus/BACnet/SNMP
- For remaining AC distribution needs

### HDX Rack PDU G4 (AC/mixed applications)
- Up to 46 kW (100A), 0U mounting
- UL 2900-1 + IEC 62443-4-2 cybersecurity (only PDU with both)
- $3K-8K per unit

### 9395XC UPS (AC backup)
- 1,125 to 2,250 kW per unit
- 99% efficiency (ESS mode), 97.5% double-conversion
- Li-ion option (15-year lifespan)
- $150K-500K per unit

### xStorage BESS (Battery Energy Storage)
- 250 to 1,000 kWh usable (parallelable)
- LFP batteries
- DC voltage: 761-1,200 VDC (overlaps 800V bus!)
- Built-in microgrid islanding
- Self-contained liquid cooling
- IDEAL for ADC microgrid buffer storage

### Boyd Thermal CDUs ($9.5B acquisition, March 2026)
- ROL4000-48U65: 2 MW cooling, 3C approach temperature
- Designed for Vera Rubin NVL72 thermal envelope
- Cold plates, manifolds, complete cooling loops
- Single-phase and two-phase liquid cooling
- **One vendor for power AND cooling — Eaton now owns both**

### Fibrebond Enclosures ($1.4B acquisition, 2025)
- **MINDEN, LOUISIANA** — 250 miles from Lafayette
- Pre-integrated modular power enclosures
- Engineered-to-order, factory-tested
- ~$378M revenue, ~$110M EBITDA
- LOUISIANA-BUILT power enclosures for ADC sites

### Flexnode NX Modules (Eaton-invested)
- 3.5 MW to 35 MW per data hall
- 35% faster deployment vs traditional
- Integrated Eaton power + 800V DC
- Worth an RFI for rapid Phase 1

### Power Xpert Microgrid Controller
- Manages solar + storage + gensets + grid as integrated system
- Automatic islanding and reconnection
- Predictive control (weather + price forecasts)
- IEC 61850 open standards

### Brightlayer DCIM Software
- DCPM: asset monitoring, power/cooling/connectivity
- EPMS: real-time electrical power data
- IPM: predictive analytics, zero-trust security

## Key White Papers
- 800VDC Architecture: eaton.com/content/dam/eaton/markets/data-center/the-impact-of-ai/whitepapers/eaton-deploying-800vdc-architecture-whitepaper-en-us.pdf
- ORV3 Open Rack: eaton.com/content/dam/eaton/products/.../eaton-ocp-orv3-open-rack-solutions-brochure-br159022en.pdf

## Financial Context
- $12 BILLION electrical sector backlog (March 2026)
- Stock: $361.04 on Beam Rubin DSX announcement day

## Risk Assessment
- Full 800V DC products may not be fully productized until mid-2027
- ADC Phase 1 could start 480V AC and retrofit to 800V DC for Phase 2
- OR wait for Beam Rubin DSX timeline
- Eaton RFI will clarify

## AMERICAN MADE — Dublin, Ireland HQ but major US manufacturing (Ohio, Virginia, Louisiana/Fibrebond)
## Contact: eaton.com/us/en-us/markets/data-centers/contact-us.html
