# Fibrebond Partnership -- Master Session Prompt
**ADC Pure DC AI Factory -- Cassette Engineering Engagement**
Author: Scott Tomsu, ADC
Last updated: 2026-04-08
Status: PRE-VISIT WORKING DOCUMENT -- CONFIDENTIAL

---

## Who You Are Talking To

Fibrebond has been engineering purpose-built modular structures for the data center and telecom industry for decades. Eaton acquired Fibrebond because the combination of Fibrebond's enclosure and integration capability with Eaton's power distribution portfolio (including Boyd Thermal) creates the only company in North America that can deliver a fully integrated, factory-tested modular AI compute enclosure under a single contract.

ADC is presenting an architecture and asking Fibrebond to engineer the production solution alongside us. All Eaton equipment throughout: ORV3 sidecars for DC power distribution at the rack, Eaton protection devices on the DC bus, Boyd CDUs for liquid cooling, Staubli quick-disconnects (Boyd-stocked, NVIDIA-approved). This is not a competitive bid for equipment -- Eaton is the stack. What we need from Fibrebond is the engineering, the factory production capability, and the Louisiana supply chain.

ADC's first cassette is a reference deployment at our MARLIE 1 facility in Lafayette. Once that cassette runs production workloads, the locked spec goes to Fibrebond for factory production. Every future site receives factory-tested cassettes from Minden. The scale is real: New Iberia alone is 87 cassettes at 200 MW. That is a production contract, not a prototype.

---

## The Architecture

**The ADC Pure DC AI Factory.** No AC anywhere in generation, storage, distribution, or delivery. Every power source outputs DC natively into a DC bus that runs unbroken to the rack.

Bloom SOFC fuel cells generate DC electrochemically. First Solar TR1 panels output DC natively. BESS stores and discharges DC natively. The GPU needs DC. Every AC conversion between the power source and the chip is an efficiency loss that this architecture eliminates by design.

**The cassette is the repeatable unit.** A purpose-built modular enclosure containing 10 NVIDIA NVL72 racks (Vera Rubin, Max P profile), factory-wired for 800V DC, factory-cooled with liquid-first architecture, factory-tested before it leaves Minden. Site provides: DC bus stub, cooling loop, fiber, concrete pad. Four connections.

### Core Specs
- **Enclosure:** 40-ft High Cube ISO external dimensions (40' x 8' x 9'6"), purpose-built steel, ISO corner castings
- **Layout:** Single row of 10 racks running the length, mechanical bay at one end, external connection panel at the other. All utilities overhead. 8 top-hinged access panels (4 per side) for service -- no internal walkable aisle.
- **Racks:** 10 x NVIDIA NVL72 (OCP Open Rack V3) -- Vera Rubin Max P
- **Power per rack:** 230 kW
- **IT load per cassette:** 2,300 kW (2.3 MW)
- **Total facility draw per cassette:** ~2,415 kW (PUE <= 1.05)
- **DC bus input:** 800V DC, OCP Stage 1d, 1500V insulation-rated throughout
- **DC bus current:** ~3,019A @ 800V (total facility draw). Conductor sized to ~3,774A (NEC 125%).
- **Cooling:** Liquid-first. >80% of rack heat removed via direct-to-chip liquid cooling. Boyd CDU (2,000 kW capacity), N+1 pumps.
- **PUE target:** <= 1.05
- **Manufacturer:** Fibrebond, Minden, Louisiana

Full engineering detail: `cassette-spec.md` (in this folder).

---

## Engineering Standards -- Basis of Design

All ADC engineering is grounded in these OCP and industry standards. These are design spec basis, not aspirational references.

### 1. OCP DCF -- LVDC Power Distribution (v1.0, March 2026)
**File:** `wp-dcf-lvdc-power-distribution.pdf`

The foundational LVDC framework. JP Buzzell of Eaton is a sub-project lead. Key constraints:
- 1500 VDC is the LVDC ceiling (NEC, IEC, all major regulatory bodies)
- 800 VDC at the rack, 1500V rated bus throughout
- OCP Stage 1d: DC bus supplies IT racks directly
- Grounding: TN-S or IT systems only -- no TN-C, no TT (DC corrosion risk)
- Series 800V source operation: firmware-cap required to hold steady-state below 1500V (750V per pole)
- Protection: SSCB preferred for microsecond DC fault response
- Tiered ESS: supercaps (us-ms) -> BBU in ORV3 sidecar (s-min) -> facility BESS (min-hr)
- Eaton ORV3 sidecar and Mt. Diablo spec directly cited as OCP-conformant power delivery

This document defines the distribution voltage architecture. Every busbar, cable, and penetration in the cassette is specified against it.

### 2. OCP Ready -- Requirements for Energy Storage Systems (January 2026, Rev 1.0)
**File:** `wp-OCP READY REQUIREMENTS FOR ENERGY STORAGE SYSTEMS_FINAL (1).pdf`

BESS architecture spec. Relevant to cassette-level BBU and site-level BESS. Key callouts:
- OCP confirms 400-1500V range for ESS in data centers (page 15)
- DC-coupled ESS = OCP-recognized architecture (Table 1, page 18)
- Outdoor containerized BESS = FM Global #1 preferred location
- Chemistry: LFP for pad-level BESS, NiZn (ZincFive) for rack-level BBU (no thermal runaway, NFPA 855 aqueous chemistry exemption)
- Supercapacitors for sub-second GPU load spike buffering in ORV3 sidecar
- NFPA 855 (2026) is primary installation code -- HMA required from licensed FPE before permitting
- UL 9540A (5th Ed. 2025) thermal runaway testing required of all BESS vendors

BBU chemistry selection for the ORV3 sidecar is an open item for Fibrebond engineering review.

### 3. OCP DCF -- Impact of Strategies on DC Energy, Carbon, and Water Consumption (March 2026)
**File:** `wp-DCF Water-Heat-Energy-2026March.pdf`

Efficiency and sustainability framework. Key implications:
- Liquid-cooled facilities at PUE <= 1.05 represent the current performance frontier
- Air-cooled facilities at 230 kW/rack cannot achieve PUE below ~1.3
- Closed-loop CDU + dry cooler / adiabatic cooler eliminates evaporative water consumption
- Louisiana (95 deg F+ design day, 75-80% RH): adiabatic assist during peak days preferred over wet cooling towers
- Behind-the-meter generation with no grid draw eliminates grid carbon attribution

This is the basis for the PUE <= 1.05 target and selection of BAC TrilliumSeries adiabatic cooler as the secondary heat rejection path.

### 4. OCP -- Dielectric Heat Transfer Fluids in Two-Phase Cold Plate Racks
**File:** `wp-Guidelines for Using Dielectric Heat Transfer Fluids in Two-Phase Cold Plate-Based Liquid-Cooled Racks-FINAL.pdf`

Relevant to liquid cooling forward path:
- Approved dielectric fluid classes for two-phase cold plate systems (engineered fluorocarbons, HFOs)
- Material compatibility requirements for seals, gaskets, tubing, manifolds
- Two-phase operation: latent heat capture improves heat transfer coefficient vs. single-phase water-glycol at same flow rate
- System-level: saturation pressure management, vapor return line sizing, non-condensable gas management

**ADC position:** Current cassette spec uses single-phase water-glycol (Boyd CDU). Two-phase dielectric is the forward path for rack densities beyond 230 kW. Fibrebond should advise: (a) whether current enclosure penetrations and CDU bay can accommodate a two-phase upgrade, and (b) what fluid containment provisions should be designed in from day one.

### 5. OCP -- Rope Leak Sensor Base Specification (R1.0.0)
**File:** `wp-Rope Leak Sensor Base Specification_R1.0.0_FINAL.pdf`

The cassette uses TraceTek rope-style leak detection throughout. Fibrebond to confirm: (a) TraceTek or OCP-conformant equivalent can be factory-installed and tested before shipment, and (b) sensor routing is compatible with enclosure layout and penetrations.

### 6. Network Fabric -- NVIDIA InfiniBand NDR
Cassette compute fabric is NVIDIA InfiniBand NDR (400 Gb/s, native to NVL72). Spine switch: NVIDIA QM9700, factory-mounted in cassette network bay. Multi-cassette sites require site-level InfiniBand fabric. Key specs:
- Within cassette: all IB cables factory-terminated
- Cassette-to-cassette: site-provided, passive copper (<=2m) or active optical (>2m)
- Management: 1 GbE isolated VLAN, fiber to site NOC
- External: 2x single-mode OS2 per cassette at wall penetration
- NVIDIA UFM required at scale -- runs on management server at site NOC
- DSX compliance validation before shipment -- Fibrebond to flag if network bay layout requires NVIDIA AE coordination

---

## What We Need Fibrebond To Engineer

### 1. Cassette Factory Production -- Engineering Package
Starting from `cassette-spec.md`, develop the full manufacturing engineering package:
- **Structural:** Purpose-built enclosure, 40-ft HC ISO external dimensions (40' x 8' x 9'6"), ISO corner castings for crane + 2-high stacking, floor rated for NVL72 point loads (1,360 kg per rack on four leveling feet), spray foam insulation R-19 minimum, ASCE 7-22 wind loads for 150 mph basic wind speed
- **Power:** 1500V-rated DC busbar backbone factory-installed, 3x ORV3 sidecar positions pre-wired, DC bus penetration at one end (single-face site connection), ground fault protection per NEC 210.13(B), arc flash labeling per NFPA 70E
- **Cooling:** Boyd CDU (2,000 kW, N+1 pumps), isolation valves per CDU for hot-swap, overhead supply/return headers sized for ~1,300 LPM, Staubli UQD at every rack and at cassette wall, TraceTek rope leak sensor per OCP spec
- **Fire:** VESDA-E VEU aspirating detection, Ansul Sapphire Novec 1230 total flood, door fan test fixture provision, cylinder sizing per NFPA 2001, discharge <= 10 sec, hold time >= 10 min
- **Environmental:** Munters desiccant dehumidification with waste-heat regeneration from cooling return loop, hot-aisle containment, positive pressure envelope
- **BMS:** NVIDIA Jetson AGX Orin, pre-wired sensor harness per OCP Signal Conditioner spec, fiber to site NOC
- **Access:** 8 hinged access panels (4/side, top-hinged), NEC 110.26 DC clearance compliant, gasket seals for positive pressure
- **Factory test:** Full FAT protocol per cassette-spec.md -- cooling pressure, DC insulation, ground fault, BMS sensors, VESDA, leak detection, door fan, network, power meters

### 2. Open Items for Fibrebond to Resolve
1. **Enclosure internal clearances:** Single-row layout with NVL72 rack depth 1,068mm (~42 in) in a 40-ft HC ISO external (40' x 8' x 9'6"). Internal width is ~7.7 ft (~92 in). With single row, rear clearance is ~50 in from rack rear to opposite wall. Fibrebond to confirm this meets NEC 110.26 working space requirements for 800V DC equipment with rear access panels. Confirm mechanical bay length at one end accommodates CDU + PDU + Munters + QM9700.
2. Boyd CDU (2,000 kW, N+1 pumps): factory-integrated with isolation valves, or field-assembled? Single PO possible for CDU + ORV3 + enclosure under Eaton?
3. ORV3 sidecar: 3 units at 800 kW each (2,400 kW total). IT load is 2,300 kW. Mechanical loads (~115 kW) need to be fed -- from sidecars or separate PDU branch? If from sidecars, total draw (~2,415 kW) is at sidecar capacity. Resolve feed path.
4. Munters desiccant integration: waste-heat regeneration requires ~55-60 deg C from cooling return. Confirm compatibility and routing in enclosure.
5. 1500V DC insulation rating: current Fibrebond spec or engineering change required?
6. Two-phase cooling readiness: enclosure layout accommodate future dielectric CDU without structural retrofit?
7. Rope leak sensor (OCP spec): factory installation and pre-ship test protocol?
8. Production capacity: cassettes per month at Minden once tooled? Lead time after spec lock?
9. 2-high stacking: structural certification, fire suppression implications (does upper cassette Novec discharge path change?), and wind load anchoring for ASCE 7-22 / 150 mph.
10. Network bay: QM9700 factory mount -- bay sized to accept Quantum-X800 XDR form factor for future upgrade?
11. Total cassette weight (loaded with empty racks + all mechanical, no servers): for crane spec and pad design.

### 3. Full Site Design -- The Engineered Building
ADC needs more than a cassette spec. Fibrebond's building and site expertise applies to the full AI factory layout. The cassette is the compute module. The site is the machine.

**Site layout:**
- Cassette pad array: spacing, orientation, crane access lanes, service clearances
- DC bus infrastructure: pad-level busbar routing from generation zone to cassette tie-in points, rated 1500V throughout
- Cooling loop infrastructure: site-level secondary loop routing (supply/return from cassette CDU to external dry cooler / BAC TrilliumSeries adiabatic cooler), Louisiana ambient design conditions (95 deg F, 75-80% RH)
- BESS placement: outdoor containerized LFP on separate pad, FM Global DS 5-33 separation distances (6 ft minimum non-combustible face, 9 ft to combustibles)
- Generation zone: Bloom SOFC N+1 positioning, gas line routing, DC bus tie-in, future FCE MCFC provision
- NOC / operations building: fiber hub, UFM management server, BMS aggregation, technician workspace

**Code and structural:**
- NFPA 855 (2026) for BESS, NFPA 72 fire detection, NFPA 2001 clean agent, IFC Louisiana adoption
- NEC DC provisions: ground fault protection per NEC 210.13(B) for >=1,000A disconnecting means, SSCB on DC distribution busbars, arc flash analysis per NFPA 70E
- Concrete pad: cassette + BESS loads (BESS containers up to 80,000 lbs), anchor bolt design for 150 mph wind, seismic per Louisiana code
- Environmental: LDEQ LPDES pre-application (cooling loop discharge if applicable), Act 730 LED certification

**Design deliverables requested from Fibrebond:**
- [ ] Site layout drawing (cassette array, BESS pad, generation zone, NOC, service lanes)
- [ ] Cassette manufacturing engineering package
- [ ] DC busbar routing drawing (generation zone to cassette tie-ins)
- [ ] Cooling loop routing drawing (CDU secondary -> dry cooler / adiabatic cooler)
- [ ] Bill of materials (Eaton stack: ORV3 sidecars, DC protection, Boyd CDUs, Staubli UQD)
- [ ] NFPA 855 compliance checklist for BESS placement
- [ ] Factory acceptance test protocol (aligned with cassette-spec.md FAT table)

---

## Business Case

**Time to compute is money.** Every week between pad-ready and first GPU workload is lost revenue at 720 GPUs per cassette running inference. Factory-tested cassettes with a 4-connection site interface compress commissioning from months to days.

**Louisiana is the supply chain.** Fibrebond (Minden) + First Solar (New Iberia, 30 mi from site) + Bloom Energy (90-day delivery, DC-native) + Cajun Industries (New Iberia, fabrication backup) + natural gas on Henry Hub 40 miles away. Every major component has a Louisiana path. US-manufactured, TAA compliant.

**Sustained GPU performance = revenue.** Liquid-first cooling (>80% direct-to-chip) sustains full TDP on Vera Rubin NVL72 at 230 kW per rack without thermal throttling. Air-cooled systems cannot maintain GPU boost clocks at sustained load above ~100 kW/rack. PUE <= 1.05 means more useful compute per watt delivered. Fibrebond's factory integration of CDU, containment, and environmental control directly enables this.

**The DC bus is the moat.** Traditional data centers convert AC -> DC -> AC -> DC between generator and chip. ADC eliminates every conversion. Bloom SOFC -> 800V DC bus -> Eaton ORV3 sidecar -> NVIDIA NVL72. Each eliminated conversion stage is 2-5% efficiency recovered -- compounding across 62,640 GPUs at New Iberia.

**Fibrebond is the production infrastructure.** ADC specs the architecture. NVIDIA specifies the compute. Eaton specifies the power. Fibrebond builds and tests the unit that delivers all three. Every future AI factory operator who comes through this facility sees Fibrebond's name on the cassette.

---

## Reference Files in This Folder

| File | Contents |
|------|----------|
| `cassette-spec.md` | Full cassette engineering specification |
| `wp-dcf-lvdc-power-distribution.pdf` | OCP LVDC power distribution (Eaton co-authored) |
| `wp-OCP READY REQUIREMENTS FOR ENERGY STORAGE SYSTEMS_FINAL (1).pdf` | OCP ESS requirements |
| `wp-DCF Water-Heat-Energy-2026March.pdf` | OCP energy/carbon/water strategy |
| `wp-Guidelines for Using Dielectric Heat Transfer Fluids in Two-Phase Cold Plate-Based Liquid-Cooled Racks-FINAL.pdf` | Two-phase dielectric cooling guidelines |
| `wp-Rope Leak Sensor Base Specification_R1.0.0_FINAL.pdf` | OCP rope leak sensor spec |

All files are confidential -- ADC internal and Fibrebond direct discussion only.

---

*ADC contact: Scott Tomsu -- scott@adc3k.com -- (337) 780-1535*
