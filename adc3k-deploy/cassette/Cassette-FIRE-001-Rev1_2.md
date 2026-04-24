# Cassette-FIRE-001 — Cassette Fire Suppression Specification — Rev 1.2

**Document ID:** Cassette-FIRE-001
**Revision:** 1.2
**Date:** 2026-04-22
**Classification:** CONFIDENTIAL
**Supersedes:** Rev 1.1 (deleted) — full clean rebuild
**Companion documents:** Cassette-CTRL-001 · Cassette-ELEC-001 · Cassette-BOM-001 · Cassette-COOL-001
**Prepared by:** Scott Tomsu · CEO / Chief Engineer · scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana

---

## Revision log

| Rev | Date | Author | Summary |
|---|---|---|---|
| 1.0 | 2026-01-xx | Scott Tomsu | First issue. Agent selection and high-level sequence only. |
| 1.1 | 2026-02-xx | Scott Tomsu | Withdrawn and deleted — inconsistent BMS interface definition vs. emerging CTRL-001. |
| **1.2** | **2026-04-22** | **Scott Tomsu** | **Full rebuild as the authoritative source for fire suppression and BMS fire interface. Novec 1230 locked as agent. Cross-zone 2-of-N detection locked. 30 s pre-discharge abort locked. Ansul listed clean agent panel is primary release authority — BMS is monitor, not release controller. Terminal-level definition of 3 DI + 2 DO interface to BMS. Munters hardwired interlock locked as separate path, not BMS-mediated. Agent quantity engineering estimate provided (~66 kg at 5.85%); final sizing flagged FIRE-01 for Ansul system designer.** |

---

## 1. Scope

This document is the authoritative specification for the Novec 1230 clean-agent fire suppression system installed in one ADC 3K Cassette (40 ft High-Cube ISO container). It defines the agent, design basis, detection scheme, control panel, interlocks, cylinder storage, personnel safety protocol, inspection cadence, and the terminal-level BMS interface.

**This document is the authority on everything FIRE-001.** When CTRL-001 Rev 1.2 says "per FIRE-001," this document is what that reference resolves to. §8 of this document is the definitive source for the 3 DI + 2 DO contacts between the fire panel and the BMS; CTRL-001 §3.2 and §4.6 point here.

**In scope:**

- Agent selection, design concentration, and NFPA 2001 compliance posture
- Protected space definition — 40 ft HC Cassette internal volume and enclosure integrity
- System design basis — agent quantity calculation, discharge time, cylinder configuration
- Detection — detector type, zone count, cross-zone logic, placement
- Ansul listed clean-agent control panel — release authority, power, manual and abort stations
- BMS interface — 3 DI + 2 DO terminal-level definition
- Interlocks — Munters hardwired shutdown, ELEC-001 ventilation kill, MIV closure via BMS
- Cylinder storage and pressure monitoring
- Personnel safety — pre-discharge alarm, egress, re-entry, MSDS reference
- Factory and site commissioning for the fire system and its BMS handshake
- Inspection and maintenance cadence per NFPA 2001 Chapter 7

**Out of scope — deferred to companion documents:**

- BMS application logic consuming the FIRE-DI inputs — CTRL-001 §6.2 (FIRE-TRIGGERED / FIRE-FAULT alarms) and §6.3 (safe-state sequence step 6)
- 480 V AC ventilation interlock circuit build and shunt-trip wiring — ELEC-001 (this document states the interface requirement; ELEC-001 implements it)
- PG25 coolant loop isolation (MIVs) on fire event — COOL-001 §8 (Belimo DN125) and CTRL-001 §7.2 (BMS closure command)
- Network monitoring of fire-event alarm records — CYBER-001 §11 (platform SIEM rule set)
- Site-perimeter fire response, fire-water supply outside the Cassette, and parish AHJ coordination beyond the Cassette envelope — facility-level fire plan

---

## 2. Governing standards and authority having jurisdiction

### 2.1 Primary standards

| Standard | Scope | Edition |
|---|---|---|
| **NFPA 2001** | Clean Agent Fire Extinguishing Systems — design, installation, acceptance | 2022 edition (or latest AHJ-accepted) |
| **NFPA 72** | National Fire Alarm and Signaling Code — detection and alarm | 2022 edition |
| **NFPA 70 (NEC)** | Electrical installation for the fire panel, detectors, and interface loops | 2023 edition |
| **UL 2166** | Standard for Halocarbon Clean Agent Extinguishing System Units — system-level listing | Current |
| **UL 268** | Smoke Detectors for Fire Alarm Systems — detector listing | 7th edition |
| **UL 864** | Control Units and Accessories for Fire Alarm Systems — panel listing | 10th edition |
| **ISO 14520-5** | Gaseous fire-extinguishing systems — Novec 1230 (FK-5-1-12) — physical properties and design data | Current (informational / design basis) |
| **FM 3500** | Class Number 3500 — Releasing Devices for Fire Protection Service — where FM-listed components are substituted | Current |

### 2.2 Authority having jurisdiction

- **Primary AHJ:** Lafayette Parish Fire Marshal (onshore site)
- **State:** Louisiana State Fire Marshal's office for industrial occupancy review
- **Federal:** 40 CFR Part 82 (EPA SNAP) — Novec 1230 is SNAP-approved for total flooding in occupied spaces; no phase-out schedule
- **Offshore variant AHJ:** USCG / ABS classification society for marine deployments (not covered in this revision — offshore posture uses the same agent and same design concentration but with marine-hazardous-area listed components; separate submittal)

### 2.3 Listing and acceptance posture

- Cylinder, valve, piping, nozzle, and control panel shipped and installed as a **single UL 2166-listed system** from the Ansul Sapphire product line (or equivalent UL 2166-listed alternative — **FIRE-10** covers substitution procedure).
- System design signed and sealed by an Ansul-authorized clean-agent designer (NICET Level III minimum in fire alarm systems or equivalent).
- Installation by Ansul-authorized distributor.
- Acceptance testing witnessed by the AHJ before Cassette is placed into production.

---

## 3. Protected space

### 3.1 Container dimensions and volume

| Parameter | Value | Basis |
|---|---|---|
| Container type | 40 ft High-Cube ISO | BOM-001 §1 |
| External length | 12.192 m (40 ft) | ISO 668 |
| External width | 2.438 m (8 ft) | ISO 668 |
| External height (HC) | 2.896 m (9 ft 6 in) | ISO 668 |
| Internal length | ~12.03 m | After wall thickness |
| Internal width | ~2.35 m | After wall thickness |
| Internal height | ~2.70 m | After floor and roof liner |
| **Gross internal volume** | **~76.3 m³** | L × W × H |
| **Net protected volume (design)** | **~76.0 m³** | Gross minus negligible solid displacement; conservative choice — NFPA 2001 does not require subtracting rack / equipment volume from V in the agent-quantity formula |
| Design reference temperature | 20 °C | §4.3 |

The 76 m³ number is used consistently through §5 (agent quantity), §6 (detector placement density), and §7 (discharge time profile).

### 3.2 Construction type

- Corten steel ISO container — inherently fire-resistive structural envelope
- Interior insulation: closed-cell spray foam on walls and ceiling (per BOM-001 enclosure spec); insulation is Class A rated and does not contribute significant fuel load
- Floor: steel plate over marine plywood subfloor; no raised access floor
- No false ceiling — nozzle sweep unobstructed from ceiling plane

### 3.3 Heat load and fire load context

| Source | Heat / fuel load | Fire risk |
|---|---|---|
| 9 × NVIDIA NVL72 / CPX compute racks | ~2.07 MW aggregate electrical | Primary risk: lithium-ion cell thermal runaway from battery backup inside racks, cable/insulation fault, PSU fault |
| 5 × Delta in-row power cabinets | AC-DC conversion + BBU | Primary risk: BBU battery fault, SCR / capacitor fault |
| 1 × control rack (BMS ECP, networking, mgmt switch) | Low | Primary risk: PSU fault |
| PG25 liquid loop | Propylene glycol / water mix | Non-flammable at operating concentration; not an ignition source |
| Munters DSS Pro | Air-handling, desiccant rotor | Not a significant fuel load itself; can worsen a fire by supplying airflow (addressed by interlock §9.1) |

Combustible loading is dominated by electrical insulation, printed-circuit substrates, and internal rack plastics. Liquid fuel is not present. The fire class posture is **Class A (ordinary combustibles, primarily electrical) with Class C energized-equipment characteristics**. Class B liquid-fire scenario is not a design case.

### 3.4 Openings inventory — enclosure integrity for NFPA 2001

For Novec 1230 to hold design concentration for the NFPA 2001-required 10-minute retention period, the enclosure must be demonstrably tight. The following openings must be sealed, gasketed, or equipped with fire-alarm-triggered closure:

| Opening | Status | Mitigation |
|---|---|---|
| Personnel entry door (1 × side) | Gasketed ISO door; closes tight | Door position sensor DI (wired to BMS) — alarm if open when panel armed |
| QBH-150 coolant QD plate penetration (supply + return) | Seal at penetration | Boot seal and fire-rated caulk around QD body |
| Power penetrations (ELEC-001 feeders) | Multi-cable transits (MCT blocks) with fire-rated seals | Per ELEC-001 |
| Fiber / copper data penetrations | MCT blocks with fire-rated seals | Per CTRL-001 §2.4 panel build |
| Munters supply/return ducts (if ducted to exterior — not in base design) | Fire/smoke damper actuated by fire panel alarm contact | Only if Munters is externally ducted; base design recirculates |
| ECP panel door | Interior panel, does not breach Cassette envelope | N/A |
| Roof / wall HVAC penetrations | None in base design | If added, require fire damper per above |
| Weep / drain penetrations | Labyrinth weep or internal trap | Seal or trap per NFPA 2001 enclosure integrity |

**Enclosure integrity test:** a door-fan (blower door) integrity test per NFPA 2001 Annex C is required at factory acceptance and at site commissioning. Target: equivalent leakage area ≤ 0.4% of gross floor area for a 10-min retention at design concentration with the container floor as the leak pressure boundary. **FIRE-02** captures the acceptance criteria and the vendor.

---

## 4. Agent selection

### 4.1 Locked: Novec 1230 (FK-5-1-12)

Novec 1230 is the locked agent. Not FM-200 (HFC-227ea). Not CO₂. Not Halon 1301 (banned). Not inert gas (IG-100, IG-541 — cylinder-bank footprint excessive for the container space available).

| Criterion | Novec 1230 | FM-200 (HFC-227ea) | CO₂ | Halon 1301 |
|---|---|---|---|---|
| NOAEL | 10 % | 9 % | N/A — kills by O₂ displacement | 5 % |
| Design concentration, Class A/C (NFPA 2001) | ≥ 5.85 % | ≥ 7.0 % | ≥ 34 % | ≥ 5 % |
| Safety margin (NOAEL — design) | 4.15 % | 2.0 % | — | 0 % |
| Occupied-space rated | Yes | Yes (tight) | No — lethal | No (phased out) |
| ODP | 0 | 0 | 0 | 10 |
| GWP (100-yr) | 1 | 3,220 | 1 | 7,140 |
| EPA SNAP status | Listed, no phase-out | Listed, under review | Listed with restrictions | Banned for new installs |
| Residue on electronics | None | None | None | None |
| Boiling point | 49 °C (liquid at room temp) | −17 °C | −78 °C (sublimes) | −58 °C |
| Storage pressure | 25 bar (superpressurized with N₂) | 25 bar | 50+ bar | 25 bar |
| Cylinder footprint per kg agent | Best | Comparable | ~10× larger | Comparable |

**Decision and rationale:** Novec 1230 selected. Occupied-space safety margin is the primary driver (4.15 % NOAEL headroom vs FM-200's 2.0 %), GWP 1 aligns with platform environmental posture, no ODP, no residue on electronics. Locked in Rev 1.2; not open.

### 4.2 NFPA 2001 design concentration

NFPA 2001 Table B.5.1.1 (2022 edition, extracted): for Novec 1230 (FK-5-1-12) protecting Class A surface fires and Class C electronics, the minimum design concentration is **5.85 % by volume at 20 °C**. The higher Class B heptane cup-burner minimum is 4.5 %; the Class A minimum of 5.85 % governs here.

**Design concentration selected: 5.85 % (minimum).** The system may be specified by the Ansul designer at a modest margin above this (typical practice 6.0–6.25 %) to account for installation tolerances; final concentration is set at **FIRE-03** at system sizing lock.

### 4.3 NOAEL / LOAEL safety margins at design concentration

- NOAEL (No Observed Adverse Effect Level) for Novec 1230: **10 %**
- LOAEL (Lowest Observed Adverse Effect Level): > 10 % (no LOAEL observed in testing up to 10 %)
- Design concentration: **5.85 %** — margin to NOAEL is **4.15 percentage points** — the largest margin of any commercial clean agent for Class A protection

Result: spaces may be occupied at design concentration for up to 5 minutes per NFPA 2001 without exceeding NOAEL exposure, **but the pre-discharge alarm and abort procedure (§11) still require personnel to egress within 30 s**. The occupied-space margin is a safety backstop, not a permit to stay in the space.

### 4.4 Agent storage conditions

| Condition | Value |
|---|---|
| Cylinder storage temperature range (NFPA 2001) | 0 °C to 54 °C |
| Design point (this Cassette) | 20 °C nominal; expect 15–30 °C actual (ECP area of Cassette, conditioned) |
| Superpressurization | Nitrogen to 25 bar at 20 °C |
| Cylinder material | Seamless steel or composite, stamped and labeled per DOT / TC / ISO |
| Hydrostatic test | Per §13 — 12-year interval |

### 4.5 Incompatibilities

- Novec 1230 decomposes at temperatures > ~500 °C to produce **hydrogen fluoride (HF)**. This is addressed under §11 (personnel safety) and §9 (no internal ventilation running during discharge).
- Not compatible with alkali metals (sodium, potassium) — not present in the Cassette.
- No known adverse interactions with PG25 coolant (spill scenario inside Cassette does not produce dangerous byproducts with Novec 1230 vapor).

---

## 5. System design basis

### 5.1 Agent quantity calculation

Per NFPA 2001 Annex B (2022 edition), the minimum agent mass is:

```
W = (V / S) × (C / (100 - C))

where
  W = agent mass (kg)
  V = protected volume (m³) = 76.0
  S = specific vapor volume of Novec 1230 (m³/kg) at design minimum temperature
    S = k1 + k2 × T
    k1 = 0.0664 m³/kg
    k2 = 0.0002741 m³/kg/°C
    T  = 20 °C
    S  = 0.0664 + 0.0002741 × 20 = 0.07188 m³/kg
  C = design concentration (% v/v) = 5.85
```

Substituting:

```
W = (76.0 / 0.07188) × (5.85 / 94.15)
W = 1,057.3 × 0.06214
W ≈ 65.7 kg at 5.85 %
```

At common margin concentrations:

| C | W (kg) |
|---|---:|
| 5.85 % (NFPA min) | 65.7 |
| 6.00 % | 67.5 |
| 6.25 % | 70.5 |
| 6.70 % (typical fail-safe margin) | 75.9 |

**Engineering estimate: ~66–76 kg Novec 1230.** Final sizing by the Ansul clean-agent designer is **FIRE-01**; this estimate is the RFQ anchor.

### 5.2 Discharge time

NFPA 2001 §5.7.2 requires clean-agent discharge to achieve ≥ 95 % of design concentration within **10 s** for halocarbon agents. For W = 66 kg, average discharge rate is ~6.6 kg/s — well within typical Ansul Sapphire nozzle capacity (single-zone total-flooding nozzles rated to 20+ kg/s).

### 5.3 Cylinder configuration

| Parameter | Value |
|---|---|
| Agent quantity basis | ~66–76 kg (§5.1) |
| Fill density (NFPA 2001 max) | 1.41 kg/L |
| Cylinder volume required | 66 / 1.41 = 46.8 L minimum |
| **Primary cylinder — preferred configuration** | **1 × 52 L Ansul Sapphire cylinder (or equivalent UL 2166-listed)** |
| Cylinder mounting | Vertical, chain-braced to Cassette sidewall in the ELEC end, upstream of the ECP panel |
| Cylinder valve | Pneumatically actuated release valve (N₂ pilot from solenoid on panel command) |
| Piping | Schedule 40 black steel, threaded or grooved; pipe network sized by Ansul designer at FIRE-01 |
| Nozzle count and placement | Single central ceiling nozzle for 76 m³ volume is within Ansul coverage envelope; final nozzle count and aim per hydraulic calc at FIRE-01 |

### 5.4 Reserve cylinder — position

**No reserve cylinder in Rev 1.2.** A reserve cylinder (second 52 L cylinder, switched automatically if the primary fails to discharge or re-ignites after discharge) is considered and explicitly excluded for the following reasons:

1. NFPA 2001 does not require a reserve for a single protected enclosure unless the hazard is classified as continuous-occupancy-critical and the AHJ has required it. Lafayette Parish does not require it for an ISO-container datacenter module.
2. The BMS + CDU + MIV + ELEC-001 shunt-trip combination removes ignition energy (480 V AC dropped, workload off, coolant isolated) within seconds of FIRE-TRIGGERED, dramatically reducing re-ignition likelihood.
3. The Cassette is a replaceable unit. Loss-of-cassette is a platform-scope operational event, not a life-safety event, once occupants are out.
4. Cylinder footprint and weight inside the Cassette are real constraints; a second 52 L cylinder consumes ECP-area floor space that is better used for spares and maintenance access.

If the platform operator later classifies the Cassette hazard as requiring reserve, **FIRE-04** covers adding a reserve bank without redesigning the primary system.

---

## 6. Detection

### 6.1 Detector type

**Photoelectric smoke detectors, UL 268-listed, addressable, intelligent.** Chosen over ionization detectors for:

- Better early response to smoldering Class A / Class C fires (PCB substrate smoldering, cable insulation) that dominate the Cassette fire risk
- Lower nuisance-alarm rate in high-airflow environments

Optional — high-sensitivity air-sampling (VESDA-style) is considered as an upgrade (**FIRE-05**) but not base Rev 1.2. The photoelectric array is sufficient for NFPA 2001 and NFPA 72 compliance at SL-equivalent facility risk classification.

### 6.2 Zone layout in the 40 ft HC container

Two independent detection zones. Cross-zone 2-of-N logic: both zones must detect before the system advances past pre-alarm to pre-discharge countdown.

| Zone | Coverage | Detectors | Placement |
|---|---|---|---|
| **Zone A — Compute end** | Racks 1–7 (compute + networking) and immediate plenum | 3 × photoelectric | Ceiling-mounted, spaced ~3.0 m along the container centerline above the hot aisle |
| **Zone B — ELEC + Control end** | Racks 8–15 (5 Delta power cabinets, control rack, ECP area), Munters plenum | 3 × photoelectric | Ceiling-mounted, spaced ~3.0 m along the container centerline over the power end |

6 detectors total. Spacing is within NFPA 72 Chapter 17 guidance for smooth ceilings at ≤ 3 m height in high-airflow environments (the reduced spacing vs the nominal 9 m detector spacing accounts for the forced-airflow environment — Munters supply and rack fans will dilute smoke more than in an unmoved air space).

**Cross-zone logic:**

- Single-detector alarm on either zone — **pre-alarm** (audible horn + strobe inside; FIRE-DI-1 NOT asserted yet; Level-1 state)
- Any detector on the second zone also alarms — **confirmed alarm, pre-discharge countdown begins** (FIRE-DI-1 asserts here — see §8.2)
- Manual release station activation — bypasses cross-zone; treated as confirmed alarm immediately

### 6.3 Detector placement — high-density compute considerations

- **Hot aisle / cold aisle orientation:** in the Cassette the aisles are perpendicular to the container long axis; detectors run down the centerline above the hot aisle where rising thermal plume brings smoke to the ceiling first
- **Munters airflow:** Munters DSS Pro supply throw is directional; detectors are placed at least 1.5 m from Munters supply registers per NFPA 72 to avoid supply-air dilution
- **Rack-top thermal layer:** in dense compute the rack top may run 10–15 °C above ambient; ceiling detectors are rated for the elevated ambient (operating range includes up to 38 °C per UL 268 with optional high-temp variants)
- **No raised floor in the base design:** no under-floor detection required; if a future revision adds a raised floor or a cable tray plenum, **FIRE-06** covers sub-floor detection
- **In-rack smoke detection (optional, future):** VESDA-style aspirating detection sampling inside each rack is considered as an upgrade (**FIRE-05**), providing even earlier detection for PCB smoldering before smoke reaches the ceiling. Not in Rev 1.2.

### 6.4 Alarm and discharge sequence

```
t = 0 s     First-zone detector alarms
              · Panel enters PRE-ALARM state
              · Audible horn + strobe active inside Cassette
              · FIRE-DI-2 (ARM) remains normal (still armed)
              · FIRE-DI-1 NOT asserted
              · Platform NOC receives pre-alarm event via BMS FIRE-FAULT?  No — pre-alarm is a separate event.
                   Rev 1.2 decision: pre-alarm is NOT published as a BMS alarm because it is not a
                   confirmed event. A separate FIRE-PRE-ALARM DI could be added in a future revision
                   (FIRE-07) but is not base Rev 1.2.

t = T_x    Second-zone detector alarms  (T_x occurs whenever cross-zone confirms)
              · Panel enters CONFIRMED ALARM state
              · FIRE-DI-1 asserts (NC contact opens) — BMS sees FIRE-TRIGGERED CRITICAL
              · Pre-discharge countdown begins: 30 s
              · Panel commands Munters shutdown via the hardwired NC interlock (§9.1)
              · Panel commands ELEC-001 ventilation shutdown (§9.2)
              · BMS in parallel executes safe-state: close MIV-S and MIV-R, stop CDU pumps,
                de-energize workload-enable (CTRL-001 §6.3)

t = T_x + 30 s  Unless abort asserted:
              · Solenoid on cylinder valve energizes
              · Agent discharges; ≥ 95 % of design concentration in ≤ 10 s
              · Panel latches in DISCHARGED state; manual reset required
```

If the **abort station** is pressed during the 30 s countdown (§7.3), discharge is inhibited but the alarm state is maintained. Release of the abort button after the countdown expires re-arms discharge, unless the panel is manually reset.

---

## 7. Control panel

### 7.1 Panel selection

- **Ansul Autopulse IQ-636 clean-agent releasing panel** (or equivalent UL 864 / UL 2166-listed releasing panel in the Ansul Sapphire product family)
- Panel mounted inside the Cassette at the ELEC end, on the wall adjacent to the ECP panel, at operator eye height
- Panel has local annunciator LEDs and backlit display showing: POWER, ARMED, PRE-ALARM, CONFIRMED ALARM, DISCHARGED, INHIBIT, FAULT, BATTERY LOW

### 7.2 Power source

- Primary: 120 V AC from a dedicated ELEC-001 panel breaker, fed upstream of the main AC shunt-trip that the ELEC-001 E-stop and this document's §9.2 interlock command (the panel must **not** be killed by its own discharge interlock)
- Secondary: internal sealed lead-acid battery sized per NFPA 72 for 24 h supervisory + 15 min alarm load
- Tertiary (not required by code for 120 VAC systems but used here): 24 VDC life-safety UPS loop feed to the **BMS interface circuit only** — the panel itself runs on its own AC + battery posture; only the 3 DI + 2 DO loop between the fire panel terminal strip and the BMS ECP panel uses CTRL-001 §2.5 F10 24 VDC (2 W budgeted there)

Loss of 120 V AC primary triggers a panel FAULT (asserts FIRE-DI-3 to BMS) and the battery carries the panel for 24 h. The panel continues to detect and respond to fire throughout the battery hold-up period.

### 7.3 Stations

| Station | Type | Location | Function |
|---|---|---|---|
| **Manual release** | Break-glass key-operated release station, UL-listed | Inside Cassette, adjacent to personnel door, at 1.4 m AFF | Activating this station bypasses cross-zone detection; immediately advances to confirmed alarm + countdown. Used by personnel discovering a fire. |
| **Abort-1 (interior)** | Maintained-contact mushroom pushbutton, green, clearly labeled "ABORT" | Inside Cassette, on the wall immediately next to the personnel door (so a person exiting can hit it on the way out) | Pressed and held — inhibits agent discharge during countdown. Countdown pauses while held. Release of button during countdown resumes the countdown from where it paused. |
| **Abort-2 (exterior)** | Same type as Abort-1 | Exterior wall of Cassette, adjacent to door, at 1.2 m AFF | Same function as Abort-1. Allows a responder outside to inhibit discharge without entering. |
| **Reset** | Key-operated, with Ansul service key | Behind panel door | Clears latched alarm states after event response. Reset is never remote. |

Abort does **not** reset the system. Abort inhibits the solenoid for as long as the button is held. When the button is released, the countdown logic proceeds. If the alarm condition still satisfies cross-zone confirmation, the system will re-enter countdown and discharge. Abort is for responder judgment during the 30 s window, not a permanent disable.

### 7.4 Panel annunciator at the exterior

In addition to the interior panel display, a **remote annunciator** mounted on the exterior door frame provides outside visibility of panel state without opening the Cassette. Indicator lamps only:

- POWER (green, steady)
- ARMED (green, steady)
- PRE-ALARM (amber, flashing)
- DISCHARGED (red, steady)
- FAULT (amber, steady)

The remote annunciator does not carry abort or reset functions; those are on the exterior at Abort-2 and at the service key only.

---

## 8. BMS interface — authoritative terminal-level definition

This section is the source of truth. CTRL-001 §3.2 and §4.6 reference this definition.

### 8.1 Interface summary

Five dry-contact signals between the Ansul panel's interface terminal strip and the BMS ECP panel:

- **3 DI** (fire panel → BMS): FIRE-DI-1 (FIRE-TRIGGERED), FIRE-DI-2 (FIRE-ARM), FIRE-DI-3 (FIRE-FAULT)
- **2 DO** (BMS → fire panel): DO-FIRE-ARM (maintenance inhibit), DO-FIRE-RELEASE (remote release)

All five are dry contacts on the panel side. All five are interrogated by the BMS 24 VDC F10 circuit (CTRL-001 §2.5). The interface is **fail-safe NC** throughout — the normal, alarm-free, powered state for every DI is contact closed with loop current; every fault condition opens the contact and drops the loop.

### 8.2 FIRE-DI-1 — FIRE-TRIGGERED

| Attribute | Value |
|---|---|
| BMS tag | FIRE-DI |
| Panel terminal | Ansul panel alarm output terminals (factory-standard "AUX ALARM" or "ALARM OUT" contact set) |
| Contact type | **Normally Closed** dry contact |
| Normal state (no alarm) | Contact closed — loop current flowing — BMS sees logical 0 (not-alarm) |
| Asserted state | Contact opens the instant the panel enters **CONFIRMED ALARM** state (cross-zone satisfied or manual release activated) — this is the **start** of the 30 s pre-discharge countdown, not the moment of actual agent discharge |
| Loop | 24 VDC from BMS, ~4 mA steady-state interrogation, shielded twisted pair |
| Wiring | Pair from panel terminals to BMS AI/DI input module in ECP; shield grounded single-point at BMS panel |
| Fail-safe posture | Cable cut, panel power failure, or loop open — BMS sees FIRE-TRIGGERED (safe failure toward alarm) |
| Debounce in BMS | 0 s (per CTRL-001 §6.2 TTA) — immediate CRITICAL |
| BMS response | FIRE-TRIGGERED CRITICAL — safe-state per CTRL-001 §6.3 (MIV close, pump stop, workload off, arm fire via DO-FIRE-ARM de-energize) |

**Position on what FIRE-DI-1 captures:** FIRE-DI-1 asserts at **CONFIRMED ALARM** (start of 30 s countdown), **not** at actual agent discharge. Rationale: the BMS must begin MIV closure, workload drain, and coolant pump shutdown at the earliest confirmed event so those actions complete **before** discharge, not concurrent with it. Waiting for actual discharge to signal the BMS would mean MIVs close while agent is flooding — too late. This is locked.

A second DI reflecting actual discharge (FIRE-DI-DISCHARGED) is considered and excluded from Rev 1.2 — the BMS does not need a separate actual-discharge signal because the safe-state response is the same in both cases and the platform NOC can reconstruct actual discharge from panel logs during incident response. Covered under **FIRE-07** if later required.

### 8.3 FIRE-DI-2 — FIRE-ARM

| Attribute | Value |
|---|---|
| BMS tag | FIRE-ARM (one of the three channels in CTRL-001 §3.2 FIRE-DI × 3) |
| Panel terminal | Ansul panel "SYSTEM ARMED" or "INHIBIT STATE" contact |
| Contact type | **Normally Closed** dry contact |
| Normal state (system armed, ready to discharge) | Contact closed — BMS sees logical 0 (armed / OK) |
| Asserted state (system inhibited or in maintenance mode — not ready to discharge) | Contact open |
| Loop | Same 24 VDC loop scheme as FIRE-DI-1 |
| Fail-safe posture | Loss of loop — BMS sees INHIBITED (panel treated as not-ready — WARN to NOC, not CRITICAL — the system being inhibited is a maintenance-window condition, not a fire event) |
| BMS response | Publishes panel-arm state as a monitored tag; does not auto-trigger safe-state on inhibit. A WARN is raised if INHIBITED state persists > 24 h outside a scheduled maintenance window |

### 8.4 FIRE-DI-3 — FIRE-FAULT

| Attribute | Value |
|---|---|
| BMS tag | FIRE-FAULT (one of the three channels in CTRL-001 §3.2 FIRE-DI × 3) |
| Panel terminal | Ansul panel "TROUBLE" or "SUPERVISORY FAULT" contact |
| Contact type | **Normally Closed** dry contact |
| Normal state (no fault) | Closed — loop current — BMS sees logical 0 (no fault) |
| Asserted state (any panel fault: detector trouble, cylinder low pressure, battery low, loss of AC > battery threshold, communication fault, ground fault) | Open |
| Loop | Same scheme as FIRE-DI-1 |
| Fail-safe posture | Loss of loop — BMS sees FAULT (safe failure toward ALARM notification) |
| BMS response | FIRE-FAULT ALARM per CTRL-001 §6.2 — SCADA alert; on-site response required |

### 8.5 DO-FIRE-ARM — BMS maintenance-inhibit output to panel

**Locked position: this DO is a maintenance-inhibit relay driving the panel's INHIBIT input. DO energized = INHIBIT ACTIVE (panel will not discharge — safe for personnel entry). DO de-energized = INHIBIT REMOVED (panel armed and ready).**

| Attribute | Value |
|---|---|
| BMS tag | FIRE-ARM-DO (in CTRL-001 §3.2 DO totals) |
| Direction | BMS → fire panel |
| Relay type | DPDT interposing relay, 24 VDC coil, gold-plated contacts, Din-rail mount in BMS ECP panel |
| Panel input | Ansul panel dedicated "REMOTE INHIBIT" terminal pair (or "MAINTENANCE MODE IN") |
| Coil power | BMS DO module, fed from CTRL-001 §2.5 F10 24 VDC |
| DO **energized** behavior | Interposing relay contacts CLOSE across the panel's remote-inhibit terminals — panel enters INHIBIT state — detection still functions, alarms still annunciate locally, but discharge solenoid is inhibited and agent will not release |
| DO **de-energized** behavior | Interposing relay contacts OPEN — inhibit released — panel is armed and ready to discharge on confirmed alarm |
| Power-loss behavior | DO is de-energized on any BMS power loss or BMS failure — panel is armed by default. **Fail-safe toward arming, not toward inhibit.** This is the intent — if the BMS dies, we want the panel armed, not inhibited. |
| Watchdog behavior | Safe-state relay (CTRL-001 §2.2) drops — DO driver de-energizes — panel armed |
| BMS application usage | During normal operation: DO de-energized (panel armed). During maintenance windows when a person is inside the Cassette: DO energized (panel inhibited). On safe-state entry per CTRL-001 §6.3 step 6: DO explicitly de-energized (panel armed) — even if it was energized a moment before. |

**Handshake interaction with FIRE-DI-2:** when the BMS energizes DO-FIRE-ARM (inhibit active), FIRE-DI-2 should open (panel reports inhibited) within 1 s. The BMS verifies this round-trip; mismatch > 10 s generates a WARN. When the BMS de-energizes DO-FIRE-ARM, FIRE-DI-2 should close (panel reports armed) within 1 s. Same mismatch monitoring.

### 8.6 DO-FIRE-RELEASE — BMS remote-release output to panel

**Locked position: this DO is a remote-release contact wired to the panel's manual-release input. BMS may assert it only if FIRE-DI-1 has been continuously asserted > 60 s AND FIRE-DI-3 is not active AND a specific platform-NOC-authenticated OPC-UA command has been issued. This is a belt-and-suspenders backup for a panel that has confirmed alarm but failed to discharge — it does not bypass the Ansul panel release logic.**

| Attribute | Value |
|---|---|
| BMS tag | FIRE-RELEASE-DO (in CTRL-001 §3.2 DO totals) |
| Direction | BMS → fire panel |
| Relay type | DPDT interposing relay, 24 VDC coil, gold-plated contacts |
| Panel input | Ansul panel "REMOTE MANUAL RELEASE" terminal pair (same electrical input as the interior manual release station; momentary closure = treat as manual pull-station activation) |
| Coil power | BMS DO module, F10 24 VDC |
| DO energized behavior | Relay momentarily closes (≥ 500 ms pulse) across the panel's remote-release terminals — panel treats as manual release command — advances to confirmed alarm + countdown if not already — discharges after 30 s abort window |
| Default state | De-energized. Always. |
| Conditions for BMS to assert DO-FIRE-RELEASE | **All four must be true simultaneously:**<br>(1) FIRE-DI-1 has been continuously asserted for > 60 s<br>(2) FIRE-DI-3 is NOT active<br>(3) Platform NOC has issued a specific `fire-remote-release-request` authenticated OPC-UA command with the Cassette serial and a signed confirmation token<br>(4) DO-FIRE-ARM is de-energized (i.e., panel is not in maintenance inhibit) |
| Why the 60 s gate | If the Ansul panel were going to discharge on its own, it would have done so by t = confirmed + 30 s. At 60 s after confirmation the BMS infers a probable panel-side failure of the release solenoid path. Only then does remote release make sense. |
| Why platform NOC gate | Discharging agent is a consequential action. It must not be under fully autonomous BMS control. A human-in-loop decision from NOC, authenticated via OPC-UA per CYBER-001 §6.3 platform role, is required. |
| Logging | Every assertion logged to /var/log/bms/alarms.jsonl at CRITICAL level, forwarded to historian, and included in mandatory post-event report |

**NFPA 2001 compliance condition on remote release:** NFPA 2001 §4.3.3 permits electrical remote-manual-release provided the remote-release means is clearly identified and protected against inadvertent operation. Wiring DO-FIRE-RELEASE to a relay that requires the four-condition gate above satisfies "protected against inadvertent operation." Acceptance by the AHJ is at **FIRE-08**.

### 8.7 Interface loop power and wiring summary

| Attribute | Value |
|---|---|
| Loop supply | 24 VDC from BMS ECP panel bus (CTRL-001 §2.5 F10), 2 W budget |
| Loop current (all three DI, steady state) | ~12 mA total (~4 mA × 3 DI) |
| DO coil current (each) | ~50 mA when energized |
| Total steady-state (DIs live, DO-FIRE-ARM de-energized at normal operation) | ~12 mA at 24 V — 0.3 W |
| Peak (maintenance inhibit active, DO-FIRE-ARM energized) | ~62 mA at 24 V — 1.5 W |
| **All within the 2 W F10 budget in CTRL-001 §2.5** | ✓ |
| Cable type | 4-pair overall-shielded instrumentation cable, 18 AWG, in separate conduit from 480 V AC |
| Terminations | Numbered terminal blocks at both ends per ECP-001 wiring practice; tag per CTRL-001 §3.2 |

---

## 9. Interlocks

### 9.1 Munters DSS Pro — hardwired NC interlock, not BMS-mediated

**Locked position: a Normally Closed dry contact from the Ansul panel's discharge alarm output is wired in series with the Munters DSS Pro run circuit. When the panel enters CONFIRMED ALARM (or pre-discharge or discharge — the contact operates at confirmed alarm, same point as FIRE-DI-1), the contact OPENS and the Munters run circuit breaks. Munters stops within its own internal response time (< 2 s). The BMS plays no role in this interlock. The BMS Munters run/stop DO (CTRL-001 §6.3 step 5 "Munters continues running during safe-state") is wired in parallel with the fire interlock NC contact, not in place of it.**

```
Munters DSS Pro run circuit (schematic):

   +24V ──[BMS Munters Run DO, NO]──┬── Munters run coil
                                    │
   +24V ──[Fire panel NC alarm contact]──┘
         (opens on CONFIRMED ALARM — BMS has no role)

Logic: Munters runs iff (BMS Munters DO energized) AND (fire NC contact still closed).
       When fire event occurs, the NC contact opens — Munters stops immediately,
       regardless of what the BMS DO is doing.
```

**Why this architecture:**

- The BMS's CTRL-001 §6.3 step 5 rule "Munters continues running during safe-state (needed for humidity control during cool-down)" applies to non-fire safe-state events (e.g., coolant leak, TraceTek wet, CDU loss). In those events, Munters should keep humidity under control while cassettes cool down.
- But during a **fire** event, Munters running would defeat the Novec 1230 flooding — agent concentration would drop below 5.85 % within seconds of discharge because Munters is pushing conditioned air through the enclosure.
- The resolution is not to have the BMS conditionally decide which safe-state it is in and act accordingly — that is slow, software-dependent, and reversible by a bug. The resolution is to make the fire-vs-Munters interlock **physical, in the wiring, independent of the BMS**.
- The NC contact from the fire panel and the BMS DO are logical AND. Fire panel asserts — NC opens — Munters off regardless of BMS state. BMS can keep its Munters DO energized the whole time without contradicting the fire interlock.

**This architecture is locked in Rev 1.2 and not open to CTRL-001 or BMS-software-side changes.**

The fire panel's NC alarm contact is a different physical output from the fire panel than FIRE-DI-1 (which the BMS reads). Both derive from the same panel-internal event (confirmed alarm state), but they are separate terminal pairs wired to separate loads. This is standard Ansul panel practice — their clean-agent panels provide multiple independent alarm output contacts.

### 9.2 ELEC-001 ventilation interlock

If the ELEC-001 design includes any ventilation fan inside the Cassette envelope other than Munters (e.g., an electrical-room exhaust fan for the ECP area in higher-power variants), that fan **must** be killed on fire panel confirmed alarm.

**Interface to ELEC-001 (requirement stated here; ELEC-001 implements):** the fire panel provides a separate NC dry contact ("480 VAC VENTILATION KILL" output) that ELEC-001 wires in series with any internal ventilation fan's contactor coil. ELEC-001 acknowledges this interface and wires accordingly.

In the base Rev 1.2 Cassette design, the only airflow device is Munters DSS Pro, which is handled by §9.1. If a future variant adds a forced-air electrical-room fan or any other envelope ventilation, this §9.2 interface is already budgeted at the fire panel.

### 9.3 MIV closure via BMS safe-state

MIV closure is BMS-mediated, not directly commanded by the fire panel. The path is:

1. Fire panel enters CONFIRMED ALARM
2. FIRE-DI-1 asserts — BMS sees FIRE-TRIGGERED CRITICAL
3. BMS safe-state (CTRL-001 §6.3) executes: MIV-S and MIV-R close via Belimo spring-return (COOL-001 §8)
4. CDU pumps stopped via Modbus to CDU skid PLC (CTRL-001 §8.3)
5. Workload-enable relay de-energized — platform-side workload drains

If the BMS is for any reason not processing the FIRE-DI (Jetson crash, BMS cable cut), the hardware watchdog (CTRL-001 §2.2) independently opens the safe-state relay within 5 s of heartbeat loss and drives MIV-S / MIV-R closed via de-energization of their respective DOs. The BMS is the ordinary path; the watchdog is the backup.

The fire panel does not have a direct wire to the MIV actuators and does not need one — the BMS and the watchdog provide dual, independent paths to MIV closure.

### 9.4 Workload-enable de-energization

Via CTRL-001 §6.3 step 4 — same BMS path as §9.3. Workload drains when the BMS drops the workload-enable DO on entering safe-state for FIRE-TRIGGERED. Platform NOC is responsible for translating loss-of-enable into GPU workload drain on the compute side; the BMS does not wait for ack before going to safe-state.

### 9.5 480 V AC shunt trip — explicit position

The fire panel does **not** command ELEC-001 shunt-trip in Rev 1.2. Reason: shunt-tripping 480 V AC removes power from the Munters interlock circuit (§9.1 depends on 24 VDC loop interrogation which is on UPS, but the Munters run circuit itself is 480 VAC — it goes dead when 480 VAC drops, which accomplishes the same result), removes power from all computing equipment (desirable, but workload drain via §9.4 is cleaner), and removes power from the CDU skid pumps (addressed by the Modbus stop command in §9.3).

Current posture: 480 V AC is **not** shunt-tripped on fire. It is dropped only via ELEC-001 §6 E-stop (either the panel E-stop button or the platform-OPC-UA E-stop-request). Fire event relies on workload drain (§9.4) and Munters interlock (§9.1). If a future revision concludes that fire should also shunt-trip 480 VAC, **FIRE-09** covers adding that interface; not base Rev 1.2.

---

## 10. Cylinder and agent storage

### 10.1 Location and mounting

- Cylinder mounted inside the Cassette at the ELEC end (opposite the personnel door), chain-braced to the interior sidewall
- Vertical orientation, valve upward, per Ansul installation manual
- Minimum 150 mm clearance from walls for inspection access
- Not within the direct splash envelope of any coolant header (per COOL-001 piping routing — coolant runs down the opposite wall)
- Pressure relief device (disc) on cylinder is oriented upward and outward, not toward equipment or personnel access path

### 10.2 Pressure monitoring

| Device | Purpose | Interface |
|---|---|---|
| **Cylinder pressure switch** | Continuous supervisory monitoring — any pressure drop below ~20 bar at 20 °C asserts cylinder-trouble | Wired to Ansul panel supervisory loop — FIRE-DI-3 asserts |
| **Pressure gauge** | Local visual inspection aid | No electrical output |
| **Load cell / weight monitoring** | Agent mass supervision — load cell under cylinder mount, continuous weight measurement; weight loss beyond a threshold asserts supervisory trouble | Wired to Ansul panel supervisory loop — FIRE-DI-3 asserts |

Both pressure and weight are supervised — the pressure switch detects gas-space leaks, the load cell detects slow agent loss that pressure alone would not reveal until near-empty. Belt-and-suspenders supervision is specified by Ansul on recent Sapphire installations and is adopted here.

### 10.3 Temperature limits

- Storage range: 0 °C to 54 °C (NFPA 2001)
- Cassette ECP area conditioned by Munters DSS Pro to 15–30 °C typical
- No direct solar exposure (cylinder is interior)
- Thermal monitoring: the cylinder area is covered by the interior T/RH sensors per CTRL-001 §3.2 (TT-INT-01 is on the ECP-end side); if TT-INT-01 reports > 45 °C, the BMS raises a WARN under the INT-T-HI-W threshold

### 10.4 Visual inspection access

- Cylinder valve, pressure gauge, load cell, and label visible from the ECP-end aisle without moving racks or panels
- NFPA 2001 monthly visual inspection completes in < 2 min per Cassette

### 10.5 Cylinder replacement procedure

Cylinder replacement is an **Ansul-authorized service provider** task, not a site tech task. Steps summarized:

1. Schedule maintenance window; coordinate with platform NOC
2. BMS energizes DO-FIRE-ARM — panel in INHIBIT state (fire panel FIRE-DI-2 opens, BMS verifies)
3. Service tech key-disconnects pilot pressure line to cylinder valve
4. Service tech removes discharge piping flange at cylinder valve outlet
5. Service tech de-chains cylinder, removes via the personnel door (cylinder on wheeled cart)
6. Replacement cylinder installed, chained, connected
7. Supervisory pressure and weight verified at panel
8. BMS de-energizes DO-FIRE-ARM — panel re-armed (FIRE-DI-2 closes, BMS verifies)
9. Service record filed

Empty or near-empty cylinders are returned to Ansul under the service agreement. Novec 1230 is not disposed as waste; it is recovered and reused.

---

## 11. Personnel safety

### 11.1 Pre-discharge alarm and egress

From the moment FIRE-DI-1 asserts (start of 30 s countdown):

- Audible horn: continuous > 90 dBA inside Cassette at the aisle, per NFPA 72
- Visual: strobe ≥ 110 cd inside Cassette
- Remote annunciator at exterior door shows PRE-ALARM (amber flashing) then DISCHARGED (red steady) when agent released
- **Egress requirement: occupant clears the Cassette within 30 s from first audible alarm.** The personnel door is within 6 m of any interior position; 30 s is comfortable for an unimpaired adult. A person inside at the moment of alarm either (a) exits and closes the door, or (b) hits the Abort-1 button on the way out if a responder needs time to assess

### 11.2 Novec 1230 decomposition products

Novec 1230 decomposes at temperatures > ~500 °C. The primary decomposition product of concern is **hydrogen fluoride (HF)**, which forms when agent vapor contacts a high-temperature surface during or after discharge.

**Detection and response:**

- The interior CO₂ sensor (CTRL-001 §3.2 CO2-INT-01) is not HF-specific, but HF is a combustion/decomposition marker alongside CO₂ buildup; a spike in CO₂ after discharge is an indicator that decomposition has occurred
- Post-discharge protocol (§11.3) requires a minimum hold-and-vent time before re-entry, during which any HF would be vented
- A dedicated HF sensor is considered as an upgrade (**FIRE-11**) but not base Rev 1.2 — the NFPA 2001 posture and hold-time protocol are sufficient at SL-equivalent facility risk

### 11.3 Re-entry protocol

After a confirmed discharge:

1. **Hold: 10 min minimum** — NFPA 2001 required retention time at design concentration. No entry.
2. **Vent: open personnel door from exterior; open opposite-end access hatch if provided; run portable forced ventilation (not Munters — Munters is interlocked off per §9.1) for a minimum of 20 min or until portable air-quality meters show <1 ppm HF and normal O₂**
3. **Survey: authorized responder in full PPE (SCBA, chemical-resistant coverall) enters and surveys**
4. **Decontaminate as needed**, repair, reset panel with service key
5. **Platform post-incident report filed within 24 h**

Re-entry before step 3 is prohibited. On-site signage at the personnel door states this.

### 11.4 MSDS reference

Novec 1230 MSDS / SDS supplied by 3M (manufacturer). Platform-side MSDS library carries current revision. Hard copy in waterproof sleeve mounted adjacent to the fire panel, updated on agent refill.

### 11.5 Oxygen depletion — explicitly not a concern

At the 5.85 % design concentration, Novec 1230 occupies ~5.85 % of the enclosure volume and the remaining ~94.15 % is normal atmosphere. Oxygen partial pressure is therefore 20.9 % × 94.15 % = **~19.7 % O₂ in the enclosure during agent hold** — above the 19.5 % OSHA oxygen-deficient threshold and nowhere near an asphyxiation hazard.

This is the fundamental difference between Novec 1230 (a heat-absorbing agent that interrupts combustion chemistry at low concentration) and CO₂ or inert-gas systems (which suppress by oxygen displacement at 34 %+ concentrations and are lethal to occupants). It is the physical reason Novec 1230 is rated for occupied spaces. State this explicitly for the record.

---

## 12. Commissioning checklist

### 12.1 Factory acceptance (panel + cylinder assembly before Cassette integration)

| Step | Description | Pass criterion |
|---|---|---|
| FP-01 | Ansul panel power-on; panel posts to normal-ready state | Green POWER + ARMED LEDs; no active trouble |
| FP-02 | Battery discharge test — disconnect 120 VAC, verify battery holds supervisory load ≥ 24 h | Measured hold time ≥ 24 h at spec battery load |
| FP-03 | Each smoke detector alarm-inject with canned smoke; verify per-zone annunciation | Each detector triggers only its assigned zone; no cross-talk |
| FP-04 | Cross-zone logic verified — alarm zone A alone does not advance past PRE-ALARM; alarm zone A + zone B advances to CONFIRMED ALARM with 30 s countdown | Countdown begins only on confirmed cross-zone |
| FP-05 | Pre-alarm audible + visual verified | Horn > 90 dBA at aisle position; strobe fires |
| FP-06 | Abort-1 and Abort-2 functional test — assert during countdown, verify countdown inhibited while held | Countdown pauses; resumes on release; does not fire while held |
| FP-07 | Manual release station functional test | Activates CONFIRMED ALARM + countdown immediately, bypasses cross-zone |
| FP-08 | Cylinder supervisory — drop cylinder pressure (test valve); verify FIRE-DI-3 / panel trouble asserts; remove load cell — verify trouble asserts | Both supervisory paths trigger FAULT |
| FP-09 | BMS interface DI handshake — assert each of FIRE-DI-1, FIRE-DI-2, FIRE-DI-3 via panel test mode; verify BMS sees each, alarm level matches §8 | All three DIs correctly read, correctly fail-safe on loop-open |
| FP-10 | BMS interface DO handshake — BMS energizes DO-FIRE-ARM; verify FIRE-DI-2 opens (panel reports INHIBIT); BMS de-energizes; verify FIRE-DI-2 closes | Round-trip < 1 s each direction |
| FP-11 | DO-FIRE-RELEASE blocked by gate — attempt to assert in BMS test mode without all four conditions of §8.6 satisfied; verify BMS refuses to drive the DO | Gate logic enforces all four conditions |
| FP-12 | Munters interlock — loop the fire panel NC contact through a dummy Munters coil; assert panel confirmed alarm; verify coil drops within 2 s | Coil drop time ≤ 2 s |
| FP-13 | Panel reset procedure with service key — verify key-only reset after latched alarm | Reset succeeds only with key; annunciators clear |
| FP-14 | Nozzle pressure-test (no agent) — pressurize pipe network with nitrogen to 25 bar; verify no leaks at joints | No pressure decay over 30 min |
| FP-15 | As-built documentation — hydraulic calc, nozzle locations, cylinder label, panel program | Documentation file complete |

Signed by Ansul-authorized service provider + Scott Tomsu before Cassette ships to integration.

### 12.2 Site commissioning (expands CTRL-001 §10.1 S-08)

| Step | Description | Pass criterion |
|---|---|---|
| SP-01 | Enclosure integrity test (door-fan) per NFPA 2001 Annex C | Equivalent leakage area ≤ 0.4 % floor area; predicted 10-min retention ≥ design concentration |
| SP-02 | AHJ walk-through and witness test — Lafayette Parish fire marshal | AHJ signs acceptance form |
| SP-03 | Panel 120 VAC primary power confirmed from ELEC-001 dedicated breaker | Panel shows normal-ready; trouble log clear |
| SP-04 | 24 VDC BMS interface loop energized from F10 (CTRL-001 §2.5) | Loop current ~12 mA measured at panel terminals |
| SP-05 | Live DI assertion test — smoke-inject zone A detector in the installed Cassette; verify panel PRE-ALARM; add zone B smoke; verify CONFIRMED ALARM | Cross-zone still works in installed environment with Munters airflow active |
| SP-06 | **BMS FIRE-TRIGGERED CRITICAL verification** — at SP-05 cross-zone confirm, simultaneously verify BMS alarm log shows FIRE-TRIGGERED CRITICAL within 1 s and BMS executes safe-state | FIRE-TRIGGERED logged; MIV-S and MIV-R reach closed limit within 10 s; CDU skid reports pumps stopped; workload-enable DO de-energized |
| SP-07 | **Munters interlock confirmed off on simulated alarm** — at the same moment as SP-05, verify Munters DSS Pro run status goes from RUNNING to STOPPED within 2 s; verify Munters did not restart for the duration of the alarm | Munters stops; does not restart without manual re-arm after panel reset |
| SP-08 | **Pre-discharge abort test** — simulate cross-zone alarm, press Abort-1 during countdown, hold for 35 s, release | Countdown does not reach zero while held; resumes on release; does not discharge (verify via test-mode interlock that solenoid circuit was armed but inhibited) |
| SP-09 | **MIV closure confirmed on fire trigger via BMS safe-state** — verified in SP-06 alongside; document close times | MIV-S and MIV-R both reach closed limit in < 10 s of FIRE-TRIGGERED |
| SP-10 | Platform NOC integration — FIRE-TRIGGERED event visible on NOC within 3 s; NOC can issue fire-remote-release-request (verified without actual release by isolating solenoid) | NOC receives event; remote-release command reaches BMS; all four gate conditions required, tested |
| SP-11 | Remote annunciator at exterior door verified — all five LED indicators cycle correctly | All LEDs function |
| SP-12 | Panel service key + reset procedure walked through with site operator | Reset succeeds; site operator signs training log |
| SP-13 | MSDS and signage posted — personnel door interior and exterior | Correctly posted |
| SP-14 | 7-day soak — no fire panel troubles, no nuisance alarms, no BMS-side FIRE-FAULT | Soak log clean |

Signed by Ansul-authorized service provider + Scott Tomsu + platform NOC lead before Cassette enters production.

---

## 13. Inspection and maintenance cadence — NFPA 2001 Chapter 7

| Cadence | Activity | Responsibility |
|---|---|---|
| **Monthly** | Visual inspection: cylinder pressure gauge in green band; panel normal-ready; no obvious physical damage; detector LEDs; remote annunciator; no active supervisory troubles; abort station accessibility | Site tech |
| **Monthly** | Log review: any WARN or FIRE-FAULT events in the past 30 days from BMS historian; root cause if present | Site tech + platform NOC |
| **Semi-annual** | Detector cleaning / sensitivity test per UL 268 and manufacturer; verify cross-zone logic still functions without forcing | Ansul-authorized service |
| **Semi-annual** | Agent quantity verification: cylinder weight measured and compared to nameplate; cylinder pressure measured at 20 °C and compared to nameplate; deviations > 5 % of agent mass trigger refill | Ansul-authorized service |
| **Annual** | Full system inspection per NFPA 2001 Chapter 7: discharge piping inspection, nozzle inspection, manual stations tested, abort stations tested, BMS interface handshake re-verified (repeat FP-09 through FP-12 in-place), panel battery replaced if near end of service life | Ansul-authorized service |
| **Annual** | BMS interface end-to-end test: assert each DI, verify BMS response; toggle each DO, verify panel response; confirm documentation matches as-installed | Ansul-authorized service + site tech |
| **Every 5 years** | Comprehensive evaluation — hydraulic calc re-verified; enclosure integrity re-tested if any Cassette penetrations have been modified | Ansul-authorized designer |
| **Every 6 years** | Cylinder internal inspection per DOT / CGA C-6 — cylinder removed, emptied, inspected, refilled | Ansul-authorized service (at 3M or authorized cylinder facility) |
| **Every 12 years** | Hydrostatic test of cylinder per DOT / CGA C-6 — or at **500 discharges**, whichever comes first | Ansul-authorized service |

All inspection records filed with the platform maintenance database. Any non-conforming condition is reported within 24 h and corrective action scheduled.

---

## 14. Open items

IDs use the **FIRE-xx** series to avoid collision with CTRL-001 **CL-xx**, COOL-001 **C-xx**, COOL2-001 **CX-xx**, and CYBER-001 **CY-xx**.

| ID | Priority | Description | Blocks |
|---|---|---|---|
| FIRE-01 | C1 | Final agent quantity, nozzle count, and hydraulic calc — sealed by Ansul-authorized clean-agent designer (NICET III min); targets 66–76 kg Novec 1230 at 5.85–6.7 % design concentration; confirms discharge time ≤ 10 s at installed pipe length | System PO; FP-14 nozzle pressure test; site commissioning |
| FIRE-02 | C1 | Enclosure integrity — door-fan test vendor, acceptance criteria confirmation (≤ 0.4 % ELA, ≥ 10 min retention at design concentration) | SP-01; AHJ acceptance |
| FIRE-03 | C1 | Design concentration margin — final selection 5.85 % vs 6.25 % vs 6.7 %; Ansul designer recommendation with rationale | FIRE-01 close |
| FIRE-04 | C2 | Reserve cylinder architecture — pre-wired provisions for a future second-cylinder addition without system redesign; Rev 1.2 ships without reserve | Future platform-side SL or AHJ requirement |
| FIRE-05 | C2 | VESDA aspirating smoke detection upgrade — evaluate in-rack aspirating detection for earlier warning; pricing and bench test before decision | Optimization, not gating |
| FIRE-06 | C3 | Sub-floor detection if raised-floor variant is adopted | Future Cassette variant only |
| FIRE-07 | C2 | Additional BMS DIs — (a) FIRE-PRE-ALARM to capture single-zone state, (b) FIRE-DISCHARGED to capture actual discharge moment separate from confirmed alarm; Rev 1.2 ships with 3 DI only, per CTRL-001 | Optimization, event reconstruction granularity |
| FIRE-08 | C1 | AHJ acceptance of DO-FIRE-RELEASE four-condition gate as "protected against inadvertent operation" per NFPA 2001 §4.3.3 | Production release with remote release capability; if AHJ rejects, DO-FIRE-RELEASE is disabled at BMS (FIRE-TRIGGERED + workload drain + Munters interlock are sufficient) |
| FIRE-09 | C2 | 480 V AC shunt-trip on fire — evaluate; Rev 1.2 posture is no shunt-trip on fire, but revisit if AHJ or platform ops requires | Platform ops decision |
| FIRE-10 | C2 | Substitution procedure for non-Ansul UL 2166 clean-agent systems (e.g., Kidde, Fike) — technical acceptance criteria and interface compatibility matrix | Procurement flexibility |
| FIRE-11 | C2 | Dedicated HF sensor post-discharge — evaluate; Rev 1.2 relies on hold-and-vent protocol + CO₂ sensor as combustion marker | Enhanced post-discharge safety |
| FIRE-12 | C1 | AHJ submittal package — sealed drawings, hydraulic calc, agent selection justification, device data sheets, battery calc, enclosure integrity report | AHJ acceptance; production rollout |
| FIRE-13 | C2 | Offshore / marine variant — hazardous-area (IECEx / ATEX) listed detectors and manual stations; marine-grade panel enclosure; separate submittal to classification society | Offshore deployment only |

---

## Document control

**Cassette-FIRE-001 — Rev 1.2 — CONFIDENTIAL**
**Prepared by:** Scott Tomsu · CEO / Chief Engineer · scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana
**Companion to:** Cassette-CTRL-001 · Cassette-ELEC-001 · Cassette-BOM-001 · Cassette-COOL-001
**Supersedes:** Cassette-FIRE-001 Rev 1.1 (deleted)
**Authority scope:** agent selection, design concentration, detection, control panel, BMS interface (3 DI + 2 DO terminal-level definition), interlocks (Munters hardwired, ELEC-001 ventilation, MIV closure), cylinder storage, personnel safety, commissioning, and inspection cadence.

This document is the source of truth for fire suppression and its BMS interface. CTRL-001 §3.2 FIRE-DI × 3, CTRL-001 §3.2 DO outputs for fire arm and fire release, CTRL-001 §6.3 step 6 fire-arm behavior, CTRL-001 §7.2 fire-panel MIV trigger, and CTRL-001 §10.1 S-08 all resolve against the definitions in this document. Any change to the interface requires a revision of this document **and** of CTRL-001 in parallel.

**End of Cassette-FIRE-001 Rev 1.2.**
