# Heat Reuse — Second Product Line Concept

## Core Insight
Every watt into a GPU comes out as heat. 100%. A 270 kW pod is a 270 kW heater that also does math. Don't get rid of heat — SELL it twice (compute + thermal energy).

## Immersion Tank Design (ADC 3K Pod)
- Boards vertical in stainless steel tank, card guides on sides (ROV-style)
- EC-110 dielectric oil, can run 60-70°C bulk temp (250°C max before degradation)
- Ship dry, fill on-site. Reseat cards on arrival (like ROV mobilization)
- 2-stack baseline (two tiers of tanks in 20ft container)
- 3-stack stretch goal (three tiers, ~192 GPUs, ~2 exaFLOPS per pod)
- Tilt-out service mechanism for board access
- Pump oil through heat exchanger, return cool to tank bottom
- WAITING ON: Real board dimensions from GTC (Scott bringing tape measure)

## Heat Reuse Product Concepts

### 1. Residential / Apartment Building
- GPU pod or single-board unit in basement
- Oil-to-water heat exchanger → building hot water + radiant floor
- Tenants get free heat. Owner earns compute revenue. Gas bill → zero in winter.
- One superchip (2,800W) = more than half a home's hot water

### 2. Commercial Building
- Immersion tank in server closet
- Oil loop → building hydronic heating system
- HVAC bill near zero in winter. Compute pays for itself.

### 3. Industrial
- Greenhouses, aquaculture (fish farms), district heating
- Iceland does this with geothermal. ADC does it with GPUs.

### 4. Small Business / Home Office ("GPU Water Heater")
- One board in sealed box, size of a water heater
- Oil circulates to heat exchanger plumbed into domestic hot water tank
- Earns revenue running AI inference. Gas bill → zero.
- Typical home water heater = 4,500W. Two GPU boards and you never pay for hot water again.

### 5. Restaurant / Food Service
- 24/7 operations (Waffle House, diners, fast food)
- Oil-to-griddle or oil-to-fryer heat exchange
- Flat-top griddle pulls ~6,000W continuously. GPU waste heat supplements it.
- These places never close = perfect for 24/7 AI inference workloads.

## Key Principle
The question isn't "how do we cool the GPUs" — it's "who wants to buy 270 kW of continuous heat?"

## Market Positioning
- **Southern US / hot climates**: Heat is waste → reject to air, focus on PUE
- **Northern US / cold climates**: Heat is a PRODUCT → sell compute + thermal
- **24/7 commercial**: Restaurants, laundromats, hospitals → always need heat
- ADC builds the same pod for both. Different heat exchanger output = different product.
