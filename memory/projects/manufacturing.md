# ADC Manufacturing -- Two-Step Cassette Factory Strategy

## Step 1: Baton Rouge Terminal (Lafayette)
- **Type**: Lease existing industrial building. Manual assembly.
- **Requirements**: 10-20K sq ft clear span, overhead crane (10-ton), 3-phase power, loading dock
- **Stations**: 6 (container prep, insulation, electrical, cooling, compute, test/QA)
- **Staff**: 8-12 people (electricians, pipe fitters, electronics techs, QA, ops mgr)
- **Output**: 2-3 pods/month
- **Timeline**: 60-90 days to first pod
- **Revenue**: $360-540K/month at capacity
- **Purpose**: Cash flow + learn what to automate

## Step 2: New Iberia Automated Factory (14th & Hwy 90)
- **Type**: Purpose-built PEMB. 52,800 SF. 32ft clear height. U-flow layout.
- **Site advantages**: Gas pipeline on-property, Hwy 90 truck access to I-10, large footprint
- **Stations**: 7 automated (receiving/prep, CNC/fab, insulation, electrical, cooling, compute, test cell)
- **Robots**: 14 systems — Fanuc M-710iC/50, Arc Mate 120iD, CRX-25iA; ABB IRB 5500/2600; UR10e cobots
- **AI Vision**: 22 Metropolis cameras + 7 Jetson AGX Orin edge inference nodes
- **Staff**: 17 (plant mgr, Omniverse eng, 4 robot ops, 2 electricians, 2 QA, 2 pipe fitters, 2 material, 1 logistics, 2 maintenance)
- **Output**: 8-12 pods/month. Bottleneck = S4 Electrical at 8hr cycle.
- **Power**: 2x CAT G3516H gensets (2.8 MW) + 750 kW solar roof + 500 kWh battery + grid backup
- **Capital**: $7.5-10.0M
- **Revenue**: $1.8M/month (10 pods x $180K). $17.3M/year gross profit. ~6mo payback.
- **Timeline**: 12-14 months site survey to first production pod
- **Engineering files**: `factory/new-iberia/` (floor-plan.html + FACTORY-SPEC.md)

## NVIDIA Technology in Factory
- **Omniverse**: Full factory digital twin — design, simulate, build, live monitor. OpenUSD.
- **Isaac Sim**: Robot path programming — weld paths, spray paths, pick-and-place, cable routing
- **Metropolis**: 22-camera AI vision QA at every station. Edge inference on Jetson AGX Orin.
- **AI Enterprise**: Scheduling optimizer, predictive maintenance, defect root cause, energy optimizer

## Key Principle
Step 1 doesn't close when Step 2 opens. It becomes the custom shop -- defense-spec, SCIF, specialty builds. Two revenue streams.

## New Iberia Site
- Location: Corner of 14th Street & Highway 90, New Iberia, LA
- Gas pipeline: ON PROPERTY
- Need: Exact address for GPS coordinates and site evaluation
