# CDU Liquid Cooling Schematics
*Notion backup — 2026-04-06*

> UPDATED 2026-03-23 -- POST-GTC REWRITE
## Cooling Architecture -- Post-GTC 2026
NVIDIA now ships complete liquid-cooled NVL72 racks. 45C hot water direct-to-chip. ADC does NOT engineer custom immersion cooling. EC-110 dielectric immersion is DEPRIORITIZED.
### What ADC Builds (cooling):
- Facility water loop (supply/return piping)
- Exterior heat rejection (dry coolers or river cooling depending on site)
- CDU connections to NVIDIA rack manifolds
### Per-Site Cooling:
Willow Glen: Mississippi River (once-through, unlimited) -- 260 MW ceiling
MARLIE I: Dry coolers on concrete pad -- 1.2 MW
Trappeys: Water tower + dry coolers -- 29 MW max
ADC 3K Pod: Integrated dry cooler per container -- 130-260 kW per pod
### ADC 3K Pod Cooling:
- 40-ft container with 1-2 NVL72 racks
- Integrated dry cooler mounted on container exterior
- 45C supply / 55-60C return glycol loop
- Self-contained -- no external water infrastructure needed
- Designed for field deployment (oil fields, remote sites)
### Temperature Specs:
- GPU junction: <83C
- Coolant supply: 45C
- Coolant return: 55-60C
- Ambient operating range: -20C to 50C (dry cooler rated)
---