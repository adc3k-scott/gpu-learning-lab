# Cassette-MASS-001 — Mass Statement and Weight Budget — Rev 3.0

**Document ID:** Cassette-MASS-001
**Revision:** 3.0
**Date:** 2026-04-22
**Classification:** CONFIDENTIAL
**Supersedes:** Rev 2.0 (2026-04-19) — deleted. Rev 2.0 architecture (800 V DC primary, 13 compute racks, CoolIT CDU inside Cassette) is superseded by the Rev 1.3 electrical and Rev 1.1 cooling architecture.
**Companion documents:** Cassette-INT-001 Rev 1.3 · Cassette-BOM-001 Rev 1.3 · Cassette-ELEC-001 Rev 1.3 · Cassette-COOL-001 Rev 1.1 · Cassette-COOL2-001 Rev 1.0 · Cassette-FIRE-001 Rev 1.2 · Cassette-SIS-001 Rev 1.2 · Cassette-ECP-001 Rev 1.2
**Prepared by:** Scott Tomsu · CEO / Chief Engineer · scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana

---

## Revision log

| Rev | Date | Author | Summary |
|---|---|---|---|
| 1.0 | 2026-04-19 | Scott Tomsu | Initial release. Baseline mass statement built on Rev 1.0 interior BOM. |
| 2.0 | 2026-04-19 | Scott Tomsu | Fire suppression 455 → 180 kg (per FIRE-001 §12 Novec 1230 single-cylinder resolution). DC electrical distribution 425 → 520 kg (4,000 A busway and laminated bus bar per ELEC-001 Rev 1.2). Manifold subtotal 230 → 260 kg (DN125 MIV upgrade per COOL-001). Assumption A-02 adopted: Delta 110 kW power shelves included in NVL72 rack weight; A-02 conservative case flagged as compliance-gating. |
| **3.0** | **2026-04-22** | **Scott Tomsu** | **Major architecture rebuild. Cassette primary input changed from 800 V DC to 480 V AC per ELEC-001 Rev 1.3 §1. Five Delta 660 kW in-row power racks (R11–R15) added to Cassette interior — each AC-to-800 V DC converter is now a physical in-row rack inside the Cassette boundary. Cassette compute rack count reduced from 13 to 9. CDU skid moved to external scope (COOL2-001); the 600 kg CoolIT CHx2000 is removed from Cassette mass. In-cassette PG25 coolant reduced 400 → 185 kg (cassette interior only; manifold, HX, and expansion-tank coolant now in CDU skid per COOL2-001 §5). Eaton Magnum DS 6,000 A AC main disconnect (~270 kg estimate, M-09) replaces the 2,500 A DC main disconnect (80 kg). Eaton Pow-R-Way III bus duct entry section (~75 kg estimate, M-10) added at ELEC ECP. The CDU 480 V AC 80 A subpanel (18 kg) is removed — CDU skid has its own dedicated 480 V AC service per COOL2-001 §10. Per-Delta-rack 480 V AC feeder cables (~103 kg per feeder × 5 = ~515 kg) added in §10. 6,000 A DC busway at 22 kg/m confirmed (up from 4,000 A at 270 kg in Rev 2.0). Drip trays reduced from 15 to 10 positions (Delta in-row racks R11–R15 are air-cooled per COOL-001 §1 — no trays). Assumption A-02 obsolete — superseded by P3-03/P3-09. New open items M-07 (Delta in-row rack weight), M-08 (flex hose mass), M-09 (Magnum DS weight), M-10 (Pow-R-Way entry weight). Rev 2.0 M-01 and M-03 closed. Baseline total: 28,765 kg — ISO 668 compliant with 1,715 kg margin at the 1,000 kg/Delta-rack baseline estimate; compliance boundary at 1,343 kg/Delta rack; sensitivity-high total 30,765 kg at 1,400 kg/Delta rack exceeds the 30,480 kg ISO limit by 285 kg.** |

---

## Table of contents

- §1 Applicable standards and limits
- §2 Mass statement summary
- §3 Container shell and modifications
- §4 Racks
- §5 Delta DC/DC shelf allocation
- §6 Cooling (cassette interior only)
- §7 DC electrical distribution
- §8 Fire suppression
- §9 Leak detection and drip management
- §10 Cables
- §11 Controls, sensors, and miscellaneous
- §12 Sensitivity analysis
- §13 Longitudinal center of gravity
- §14 Vertical center of gravity
- §15 Two-high stacking analysis
- §16 Key assumptions
- §17 Findings and required actions
- §18 Open items

---

## 1. Applicable standards and limits

The mass budget is constrained by the following external standards. Values and interpretations are unchanged from Rev 2.0.

| Standard | Role in this mass statement |
|---|---|
| **ISO 668:2020** Series 1 freight containers — Classification, dimensions and ratings | Defines the 40-ft HC container maximum gross mass (R = 30,480 kg / 67,200 lb) and the tare-plus-payload equality. The Cassette, as an integrated unit, ships and lifts under the rating of the 40-ft HC container it is built into. Every mass total in this document is evaluated against R = 30,480 kg. |
| **ISO 1161:2016** Series 1 freight containers — Corner and intermediate fittings | Governs the corner casting geometry, fit, and design test loads. Used in §15 for the two-high stacking analysis. |
| **ISO 1496-1:2013** Series 1 freight containers — Specification and testing — Part 1: General cargo containers for general purposes | Governs the structural test requirements including the stacking test load (9 × R = 274.3 tonnes applied to the top corner castings of the lower container). Used in §15 to evaluate lower-container corner casting utilization. |
| **DNV-OS-D101** Marine and machinery systems and equipment (DNV standard for offshore classification of containers) | Applied if the Cassette is shipped offshore. Adds a 5g dynamic-load case on the corner castings, which sets a more restrictive ceiling than ISO 1496 for the same corners. Used in §15. The DNV corner casting review remains an open item (M-05). |
| **IBC 2021 Chapter 16 / ASCE 7-22** Building code / structural loads (applied to permanent site installation) | Governs anchorage and seismic design category loads once the Cassette is installed at Trappey's AI Center. Mass totals here are the input to the anchorage calculation; the anchorage design itself is out of scope of MASS-001. |

The single hardest binding limit in this document is the ISO 668 R value of **30,480 kg**. Every finding and every sensitivity scenario in §2, §12, and §17 is evaluated against that number.

---

## 2. Mass statement summary

### 2.1 Section totals — baseline scenario (1,000 kg per Delta in-row rack)

| § | Category | Mass (kg) | Change vs Rev 2.0 |
|---|---|---:|---:|
| 3 | Container shell and modifications | 6,100 | 0 |
| 4 | Racks (R1–R9 compute + R10 control + R11–R15 Delta + anchors) | 19,260 | **−1,000** (13→9 compute, R10 revised, 5 Delta added) |
| 5 | Delta DC/DC shelf allocation | 0 | 0 (in §4 rack weights) |
| 6 | Cooling (cassette interior only) | 445 | **−815** (CDU removed, coolant reduced, expansion tank in skid) |
| 7 | DC / AC electrical distribution | 833 | **+313** (Magnum DS, Pow-R-Way, 6,000 A busway upgrade) |
| 8 | Fire suppression | 180 | 0 |
| 9 | Leak detection and drip management | 160 | **−40** (10 trays vs 15) |
| 10 | Cables | 702 | **+250** (AC feeders added, DC primary removed) |
| 11 | Controls, sensors, miscellaneous | 170 | **−10** (CDU OOB switch deduplicated) |
|  | **Raw subtotal** | **27,850** | |
|  | Integration hardware and rigging contingency | 915 | |
|  | **Cassette baseline total** | **28,765** | **−1,170** vs Rev 2.0 (29,935 kg) |

The integration hardware and rigging contingency line at 915 kg (~3.3 % of raw subtotal) covers brackets, fasteners, cable glands, wire management, in-situ shims, small panel penetrations, and as-built delta that accumulates during integration but is too granular to enumerate at the BOM level. This line is held fixed across scenarios in §12 rather than scaled, reflecting the observation that integration hardware mass is substantially set by rack count and fit-out geometry, neither of which changes under the compute-rack or Delta-rack weight sensitivities.

### 2.2 Sensitivity — high scenario (1,400 kg per Delta in-row rack)

| Line | Mass (kg) |
|---|---:|
| Cassette baseline total | 28,765 |
| Delta in-row rack upcharge (5 racks × +400 kg) | +2,000 |
| **Sensitivity-high total** | **30,765** |

The sensitivity-high total **exceeds** the ISO 668 R value of 30,480 kg by 285 kg. At compute rack weight 1,500 kg (A-01) and Delta in-row rack weight 1,400 kg, the Cassette is not ISO compliant as a single unit.

### 2.3 Compliance summary against ISO 668 R = 30,480 kg

| Scenario | Total (kg) | Margin (kg) | Compliant? |
|---|---:|---:|:-:|
| Baseline (1,000 kg/Delta rack, 1,500 kg/compute rack) | 28,765 | +1,715 | **Yes** |
| Compliance boundary (1,343 kg/Delta rack, 1,500 kg/compute rack) | 30,480 | 0 | Boundary |
| Sensitivity-high (1,400 kg/Delta rack, 1,500 kg/compute rack) | 30,765 | −285 | **No** |

The compliance boundary at 1,343 kg per Delta in-row rack is the number that gates procurement. M-07 must resolve at or below this value for the Cassette to ship as a single ISO unit without special-load exception procedures.

---

## 3. Container shell and modifications

Unchanged from Rev 2.0.

| Item | Basis | Mass (kg) |
|---|---|---:|
| 40-ft High Cube ISO container base shell (steel frame + corrugated walls + roof + floor) | Published tare for one-trip 40-ft HC, Class A | 3,900 |
| Floor reinforcement — 10 mm plate overlay + cross-members for 45 kN/m² loaded area | Structural reinforcement per INT-001 §4.3 | 850 |
| Insulation (closed-cell spray foam 50 mm walls, 75 mm ceiling) | INT-001 §4.4 | 220 |
| Interior liner (FRP panels + stainless trim in wet areas) | INT-001 §4.5 | 180 |
| Door and penetration modifications (ECP door cut-outs, gasketed service door, air return grilles) | INT-001 §4.6 | 210 |
| Overhead cable tray and support rails | INT-001 §4.7 | 180 |
| Floor rail rack-mount channels (for R1–R15 positions) | BOM-001 §2, INT-001 §5 | 280 |
| Interior finish, sealants, paint, labels | INT-001 §4.8 | 80 |
| Corner casting reinforcement plates (for two-high stacking, per §15) | DNV-OS-D101 reinforcement, M-05 open | 200 |
| **§3 subtotal** | | **6,100** |

No change from Rev 2.0 — the shell is reused exactly. The corner casting reinforcement plates remain in place against M-05 offshore review; removing them is not contemplated even under domestic shipping.

---

## 4. Racks

Three rack classes populate the 15 rack positions. The count is unchanged at 15 total; the composition is redistributed vs Rev 2.0.

### 4.1 Compute racks R1–R9 — NVIDIA Vera Rubin NVL72 / CPX

Per BOM-001 Rev 1.3 §3 and COOL-001 Rev 1.1 §1. Each of R1–R9 is an NVL72 / CPX compute rack with direct liquid cooling via the cassette-interior manifold. The rack includes an integrated Delta 800 V → 50 V DC/DC power shelf (one per rack); that shelf mass is bundled into the rack estimate and is not accounted separately — see §5 and assumption A-07.

| Item | Qty | Unit mass (kg) | Mass (kg) | Basis |
|---|:-:|---:|---:|---|
| NVL72 / CPX compute rack (populated) | 9 | 1,500 | 13,500 | **Estimate — M-02 open** (NVIDIA Vera Rubin platform published reference mass pending confirmation — C-01 carryforward) |

Rev 2.0 carried 13 compute racks at 1,500 kg each = 19,500 kg. Rev 3.0 carries 9 compute racks = 13,500 kg. The 6,000 kg reduction is the single largest Rev 2.0 → Rev 3.0 subtraction.

### 4.2 Control rack R10 — InfiniBand, storage, DPUs, management

Per BOM-001 Rev 1.3 §3. R10 consolidates the Cassette-side management plane. Rev 2.0 split this across two control racks (R14 + R15, combined estimate ~900 kg). Rev 3.0 consolidates into a single 600 mm Oberon-style frame, R10.

| Item | Qty | Unit mass (kg) | Mass (kg) | Basis |
|---|:-:|---:|---:|---|
| Oberon 600 mm frame with cable management | 1 | 130 | 130 | Vendor published |
| InfiniBand NDR switches (NDR 400 Gb/s, 2U) | 2 | 22 | 44 | Mellanox published |
| NVMe storage shelf (all-flash, 24-bay, 2U) | 2 | 28 | 56 | Vendor published |
| Management servers (1U dual-socket) | 4 | 18 | 72 | Vendor published |
| BlueField-4 DPU host (2U) | 2 | 24 | 48 | NVIDIA published |
| Jetson AGX Orin BMS compute module + enclosure | 1 | 8 | 8 | Vendor published |
| KVM / console, DIN-rail accessories | 1 | 12 | 12 | Estimate |
| Internal cabling, patch panels, PDUs (control-rack-local) | — | — | 180 | Estimate |
| Airflow blanking panels, seal kit | — | — | 25 | Estimate |
| Allowance for additional 1U and 2U units (25 % of itemized) | — | — | 125 | Estimate (growth headroom) |
| **R10 total** | | | **700** | **Estimate — integrated; no single open item** |

Rev 2.0's 900 kg combined R14+R15 estimate compresses to 700 kg in R10 as a single rack. The 200 kg reduction is booked into the §4 rack total.

### 4.3 Delta 660 kW in-row power racks R11–R15

Per BOM-001 Rev 1.3 §4 and ELEC-001 Rev 1.3 §1. Each Delta 660 kW rack receives 480 V AC via a per-rack feeder (see §10), converts to 800 V DC internally via six 110 kW AC-DC rectifier shelves, and couples to the 6,000 A DC busway via a laminated copper bus stub (see §7). Each rack additionally contains an embedded 480 kW battery backup unit (BBU) providing ~15-second ride-through per BOM-001 §4. The racks are air-cooled internally — no drip trays (see §9) and no manifold tap (see §6).

| Item | Qty | Unit mass (kg) | Mass (kg) | Basis |
|---|:-:|---:|---:|---|
| Delta 660 kW in-row power rack (populated: 6× 110 kW AC-DC shelves + 480 kW BBU + Oberon-style frame) | 5 | 1,000 | 5,000 | **ESTIMATE — M-07 OPEN (CRITICAL)** |

The 1,000 kg per-rack baseline is a working estimate pending Delta Electronics publication. The Delta 660 kW platform is new (2026 release per ELEC-001 §18); published mass figures are not available. M-07 directly gates Cassette ISO compliance: each 100 kg change per rack shifts total Cassette mass by 500 kg.

### 4.4 Rack anchors and snubbers

Unchanged from Rev 2.0.

| Item | Qty | Unit mass (kg) | Mass (kg) | Basis |
|---|:-:|---:|---:|---|
| Rack-to-floor anchorage (M16 studs, captive washers, brackets) per rack | 15 | 3 | 45 | Estimate |
| Seismic snubbers (IBC Chapter 16 Sds 0.5 category) per rack | 15 | 1 | 15 | Estimate |
| **Anchors and snubbers total** | | | **60** | |

### 4.5 §4 section total

| Subsection | Mass (kg) |
|---|---:|
| §4.1 Compute racks R1–R9 | 13,500 |
| §4.2 Control rack R10 | 700 |
| §4.3 Delta in-row power racks R11–R15 | 5,000 |
| §4.4 Rack anchors and snubbers | 60 |
| **§4 subtotal** | **19,260** |

---

## 5. Delta DC/DC shelf allocation

This section exists to document the allocation logic that closes assumption A-02 and to make clear why no line-item mass contribution appears at §5.

Per position P3-09 and assumption A-07: the Delta 110 kW power shelves that perform AC-to-800 V DC conversion are physically located inside the five Delta 660 kW in-row racks R11–R15 (six 110 kW shelves per rack). Their mass is counted within the 1,000 kg per-rack Delta estimate in §4.3.

The separate 800 V → 50 V DC/DC power shelf that delivers 50 V to the Vera Rubin compute tray in each NVL72 / CPX rack (one per compute rack) is physically located inside each R1–R9 rack. Its mass is bundled into the 1,500 kg per-rack compute estimate per assumption A-07 / BOM-001 §4 note.

**Neither shelf class is counted separately at §5.** The §5 mass contribution is therefore 0 kg.

Rev 2.0 assumption A-02 ("are Delta power shelves included in the NVL72 rack weight?") is obsolete. The question was whether a standalone 110 kW shelf population might be unaccounted; in Rev 3.0 the 110 kW shelves are components of physically separate in-row racks that are separately listed in §4.3, so the question no longer applies. The Rev 2.0 conservative case of 31,415 kg (which built an additional Delta-shelf mass on top of the rack estimate) is obsolete and is not carried forward into Rev 3.0 compliance analysis. See M-01 (closed).

The new uncertainty driving compliance is not a shelf-level ambiguity; it is the Delta in-row rack total weight itself (M-07).

---

## 6. Cooling (cassette interior only)

Cassette-interior cooling mass only. The CDU skid — heat exchanger, primary pumps, expansion tank, makeup system — is external to the Cassette boundary per COOL2-001 Rev 1.0 §1 and has operating mass ~5,800 kg wet per COOL2-001 §8, documented there. Flex hose assemblies are supplied with the Cassette but are outside the ISO envelope during transport (open item M-08 resolves the transport-weight boundary).

| Item | Qty / length | Unit | Mass (kg) | Basis |
|---|:-:|:-:|---:|---|
| CDU unit (CoolIT CHx2000) | 0 | — | 0 | **Moved to COOL2-001 (external skid)** — was 600 kg in Rev 2.0 |
| Expansion tank | 0 | — | 0 | **Moved to CDU skid per COOL2-001 §5** — was 15 kg in Rev 2.0 |
| Primary PG25 coolant, cassette interior only | 180 L | 1.017 kg/L | 185 | COOL2-001 §5: cassette-interior volume 180 L × PG25 density ≈ 183 kg; rounded up to 185 |
| Supply and return manifolds (DN125, SCH40 steel, 5 m active length each, insulated) | 2 runs × 5 m | ~15 kg/m active | 150 | COOL-001 §3 |
| Manifold isolation valves MIV-S and MIV-R (Belimo DN125 spring-return, actuator + body) | 2 | 20 each | 40 | COOL-001 §8 |
| QBH-150 DN150 quick-disconnect boundary plate | 1 | 25 | 25 | COOL-001 §3 |
| Manifold supports, brackets, anti-drip kit (local only, main drip trays in §9) | — | — | 30 | Estimate |
| Piping small-bore (drains, vents, instrumentation tees — DN15 to DN25) | 15 m | 1.0 kg/m | 15 | Estimate |
| **§6 subtotal** | | | **445** | |

Rev 2.0 carried §6 at 1,260 kg. The 815 kg reduction comes from: CDU removal (−600 kg), coolant reduction (−215 kg: 400 → 185 kg), and expansion tank removal (−15 kg). Manifold plus valves plus QBH plus supports are essentially unchanged in mass terms (~260 kg), now itemized at 260 kg total (150 + 40 + 25 + 30 + 15 = 260 kg; the 185 kg coolant plus 260 kg piping/valves/supports = 445 kg).

The 185 kg coolant is the coolant actually present in the cassette interior during operation. At draining for shipment, this volume is captured at the CDU skid side of the QBH plate and the cassette-interior volume drains via a gravity path — the Cassette ships dry, so the 185 kg coolant is an operational mass not a shipping mass. For ISO compliance the shipping mass uses the dry figure; both scenarios in §2 state the operating mass for conservatism. No ISO margin is claimed by citing the dry mass.

---

## 7. DC electrical distribution

The section title is retained from Rev 2.0 for cross-document continuity, but the content is now a hybrid: the AC primary path (main disconnect, bus duct entry, AC feeders) is new to Rev 3.0 at the Cassette boundary, and the 800 V DC secondary path (busway, taps, branch breakers) is retained but upgraded from 4,000 A to 6,000 A.

### 7.1 AC-side primary (new in Rev 3.0)

| Item | Qty | Unit mass (kg) | Mass (kg) | Basis |
|---|:-:|---:|---:|---|
| Eaton Magnum DS 6,000 A, 480 V AC, UL 1066 air circuit breaker (main AC disconnect) | 1 | 270 | 270 | ELEC-001 Rev 1.3 §18 E-02 CLOSED; **Estimate — M-09 OPEN (±80 kg)** |
| Eaton Pow-R-Way III bus duct wall entry section, 6,000 A (wall penetration + transition hardware at ELEC ECP) | 1 | 75 | 75 | ELEC-001 §18 E-01 CLOSED; **Estimate — M-10 OPEN** |
| Revenue meter (Veris E50H6B or equivalent, 480 V 3-phase) | 1 | 5 | 5 | Vendor published |
| Surge protective device (SPD) Type 1, 480 V AC | 1 | 5 | 5 | Vendor published |
| **AC-side subtotal** | | | **355** | |

The Rev 2.0 2,500 A DC main disconnect (80 kg) and CDU 480 V AC 80 A subpanel (18 kg) are both removed. The Stäubli CombiTac 2500 DC connector at the ECP (Rev 2.0 §7 line item) is removed. Net AC-side add vs Rev 2.0 DC-side items removed: +355 − 80 − 18 = +257 kg (not counting the SPD, which was present in Rev 2.0 at the same mass).

### 7.2 DC-side distribution (retained, upgraded to 6,000 A)

| Item | Qty / length | Unit mass (kg) | Mass (kg) | Basis |
|---|:-:|---:|---:|---|
| 6,000 A DC busway (Starline or Siemens SIVACON 8PS equivalent, insulated plug-in) | 15 m × 22 kg/m | — | 330 | A-11 assumption; was 270 kg at 4,000 A in Rev 2.0 |
| Busway plug-in tap units (one per rack R1–R10, plus service tap) | 10 | 2.5 | 25 | Vendor published |
| Laminated copper bus stubs (Delta rack output to busway) | 5 | 6 | 30 | Estimate; short stubs, not full 0.6 m bus bars |
| Per-rack DC branch breakers (ABB XT4 DC-rated, 250 A trip class) | 10 | 3 | 30 | 9 × 250 A/250 A + 1 × 250 A/200 A per ELEC-001 |
| **DC-side subtotal** | | | **415** | |

The 6,000 A DC busway reflects the full power throughput — five Delta racks at 660 kW each = 3.3 MW peak DC delivered to R1–R9 compute racks. Rev 2.0 sized the busway at 4,000 A for a lower compute count and lower peak draw.

### 7.3 Life-safety and auxiliary electrical

| Item | Qty | Unit mass (kg) | Mass (kg) | Basis |
|---|:-:|---:|---:|---|
| Bender iso-PV1685 insulation monitoring device (IMD) | 1 | 8 | 8 | Vendor published |
| Maintenance UPS, 24 V DC, 2 kWh LiFePO4 | 1 | 20 | 20 | Vendor published |
| Life-safety 24 V DC distribution panel | 1 | 10 | 10 | Vendor published |
| Ground bar, terminal blocks, LED lights, panel control relay, misc DIN-rail | — | — | 25 | Estimate |
| **Auxiliary subtotal** | | | **63** | |

### 7.4 §7 section total

| Subsection | Mass (kg) |
|---|---:|
| §7.1 AC-side primary | 355 |
| §7.2 DC-side distribution | 415 |
| §7.3 Life-safety and auxiliary | 63 |
| **§7 subtotal** | **833** |

Rev 2.0 §7 total was 520 kg. Net change +313 kg. The increase is driven by: Magnum DS 6,000 A AC disconnect (+270 kg) — DC disconnect removed (−80 kg) + Pow-R-Way III entry (+75 kg) + DC busway upgrade (+60 kg at 22 kg/m × 15 m new vs 18 kg/m × 15 m old) — CDU 480 V subpanel (−18 kg) + bus stubs reconfigured (±0 kg) + branch breaker count (10 vs Rev 2.0's 13, ±0 kg net at 3 kg each). The Magnum DS is the single largest driver and the item with the widest estimate tolerance (M-09, ±80 kg).

---

## 8. Fire suppression

Unchanged from Rev 2.0. Companion reference is now Cassette-FIRE-001 Rev 1.2 (not Rev 1.1 as Rev 2.0 referenced).

| Item | Qty | Unit mass (kg) | Mass (kg) | Basis |
|---|:-:|---:|---:|---|
| Ansul Sapphire 52 L Novec 1230 cylinder (populated, mounted), 66 kg agent design mass + 25 kg cylinder | 1 | 95 | 95 | FIRE-001 §5.2, §12 |
| Cylinder mounting bracket, floor strap kit | 1 | 8 | 8 | FIRE-001 §5.2 |
| Discharge nozzles (DN15, 4-nozzle layout for 76 m³ enclosure) | 4 | 1.5 | 6 | FIRE-001 §4.2 |
| Piping (DN15 to DN20 SCH40 carbon steel, ~30 m total run) | 30 m | 1.5 kg/m | 45 | FIRE-001 §4 |
| Ansul clean-agent panel (AutoPulse IQ-301 or equivalent) with 24 h battery | 1 | 18 | 18 | FIRE-001 §6 |
| Detectors (photoelectric, 6 units, cross-zone 2-of-N) | 6 | 0.5 | 3 | FIRE-001 §3 |
| Manual release and abort stations | 2 | 1 | 2 | FIRE-001 §3 |
| Notification appliances (horn/strobe, 2 units) | 2 | 1.5 | 3 | FIRE-001 §3 |
| **§8 subtotal** | | | **180** | |

Rev 2.0's reduction from 455 kg (original dual-cylinder FM-200 provision) to 180 kg via FIRE-001 §12 single-cylinder Novec 1230 resolution carries through Rev 3.0 unchanged.

---

## 9. Leak detection and drip management

Change from Rev 2.0: drip tray count reduced from 15 to 10. The Delta in-row power racks R11–R15 are air-cooled per COOL-001 Rev 1.1 §1 and have no liquid-cooling manifold connections; they do not need drip trays. The 10-tray population covers R1–R9 (nine compute racks, each with a manifold tap) + R10 (control rack drip tray per INT-001 standard practice, even though R10 is air-cooled, to catch any manifold-above condensate).

| Item | Qty | Unit mass (kg) | Mass (kg) | Basis |
|---|:-:|---:|---:|---|
| Under-rack drip trays (stainless, 600 × 800 × 50 mm, 1.5 mm gauge) | 10 | 8 | 80 | BOM-001; was 15 trays = 120 kg in Rev 2.0 |
| TraceTek TT-5000 leak sensor cable (two zones, ~40 m total) | 40 m | 0.15 kg/m | 6 | Vendor published |
| TraceTek TT-SIM-2 controller + zone module | 1 | 4 | 4 | Vendor published |
| Sump pan (400 × 200 × 150 mm, stainless, plus second float switch mount) | 1 | 12 | 12 | INT-001 §6.3 |
| Sump float switches (LT-SUMP-HI and LT-SUMP-HIHI, dual-float assembly) | 2 | 1 | 2 | Vendor published |
| Sump drain pipe (DN25, to external service port) | 5 m | 1 kg/m | 5 | Estimate |
| Containment moat sill at QBH-150 boundary | 1 | 20 | 20 | INT-001 §6.3 |
| Floor drain plumbing and seals | — | — | 15 | Estimate |
| Emergency coolant spill absorbent pillows (pre-staged) | — | — | 16 | Operational spares |
| **§9 subtotal** | | | **160** | |

Net change vs Rev 2.0: −40 kg. Five fewer drip trays × 8 kg = −40 kg; all other items unchanged.

---

## 10. Cables

Major restructure. Rev 2.0's 800 V DC primary cable entry at the ECP is removed — the AC primary now enters via the Pow-R-Way III bus duct wall section (counted in §7, not in §10). A new, substantial line item is added for per-Delta-rack 480 V AC feeders.

| Item | Qty | Unit | Mass (kg) | Basis |
|---|:-:|:-:|---:|---|
| Per-Delta-rack 480 V AC feeder — 2× 300 mm² XHHW-2 per phase × 3 phases + 1× 95 mm² XHHW-2 ground, ~5 m run | 5 feeders | — | 515 | Per-feeder: (6 conductors × 5 m × 3.3 kg/m) + (1 conductor × 5 m × 0.84 kg/m) = 99 + 4 ≈ 103 kg × 5 = 515 kg — ELEC-001 §8 |
| DC branch cables R1–R9 (2× 95 mm² polarity conductors × ~2 m per rack) | 50 m | 0.84 kg/m | 42 | Was 2× 70 mm² at 36 kg in Rev 2.0 (scaled to 6,000 A busway) |
| 800 V DC primary entry cable (Rev 2.0 ECP) | 0 | — | 0 | **Removed** — replaced by bus duct entry in §7 |
| Cat6A network trunks (management plane) | ~150 m | 0.05 kg/m — included with connectors | 50 | Estimate; unchanged from Rev 2.0 |
| Modbus RTU (RS-485) runs to CDU skid, Munters, ancillary | ~100 m | 0.07 kg/m | 15 | Estimate; unchanged from Rev 2.0 |
| 24 V DC life-safety distribution (BMS, watchdog, MIV actuators, fire interface, sensors) | ~300 m of various conductors | — | 35 | Estimate; unchanged from Rev 2.0 |
| Bonding and grounding conductors (2/0 AWG, 4/0 AWG, main ground, rack ground bars) | ~80 m total | — | 25 | Estimate; unchanged from Rev 2.0 |
| Sensor and control cabling (T/RH, leak, sump, fire panel, tamper, limit switches, analog 4–20 mA loops) | ~200 m | — | 20 | Estimate; unchanged from Rev 2.0 |
| **§10 subtotal** | | | **702** | |

Rev 2.0 §10 subtotal was approximately 450 kg (not explicitly tabulated in Rev 2.0, reconstructed from BOM). Rev 3.0 adds 515 kg for the five AC feeders and subtracts the 800 V DC primary entry (which in Rev 2.0 carried roughly 200 kg as 2× 500 mm² DC cable over ~8 m, now handled by the bus duct entry in §7). Net §10 increase: approximately +250 kg.

---

## 11. Controls, sensors, and miscellaneous

Minor updates vs Rev 2.0. Primary change: no separate out-of-band (OOB) management switch for CDU — the CDU skid has its own controls and Modbus TCP interface per COOL2-001 §9, and reports to the platform NOC independently of the Cassette BMS OPC-UA surface. Any Cassette-side double-counted CDU sensors are removed.

| Item | Qty | Unit mass (kg) | Mass (kg) | Basis |
|---|:-:|---:|---:|---|
| BMS ECP panel (steel enclosure, DIN rails, backplane, gland plates) | 1 | 45 | 45 | ECP-001 §4 |
| DIN-rail I/O modules (CPU, DI ×2, DO, AI, AO, Modbus TCP gateway, OPC-UA — per TAGS-001 §3) | 8 cards + accessories | — | 12 | Vendor published |
| Jetson AGX Orin compute carrier (in R10 per §4.2; listed here only for I/O wiring continuity — 0 kg here to avoid double count) | 0 | — | 0 | Counted in R10 §4.2 |
| Hardware watchdog relay (DIN-rail, IEC 61508 SIL 2 pending SIS-04) | 1 | 0.8 | 1 | Vendor published |
| 24 VDC life-safety UPS (separate from 2 kWh unit in §7.3 — smaller ECP-local, ~200 Wh) | 1 | 8 | 8 | Vendor published |
| Interior environment sensors (AT-INT-RH, TT-INT, AT-CO2 — ceiling mounted) | 3 | 1 | 3 | Vendor published |
| CDU skid coordination (OOB switch for CDU) | 0 | — | 0 | **Removed per P3-11 intent — CDU has its own controls** |
| HMI touchscreen panel (ECP door mount) | 1 | 6 | 6 | Vendor published |
| Terminal blocks, wire duct, labels, cable glands, ECP-internal wiring | — | — | 25 | Estimate |
| Platform network switches (Cassette-side TOR, management VLAN aggregation — R10 location but counted here for infrastructure class) | 2 | 15 | 30 | Vendor published |
| Fiber patch panels and LC/MPO cassettes | — | — | 15 | Estimate |
| Spare parts kit (fuses, relays, terminals, sensors — operational provisioning) | — | — | 25 | Estimate |
| **§11 subtotal** | | | **170** | |

Rev 2.0 §11 was 180 kg; Rev 3.0 §11 is 170 kg. Net −10 kg from the CDU OOB switch deduplication and minor consolidation.

---

## 12. Sensitivity analysis

Two independent variables drive Cassette mass uncertainty at Rev 3.0:

- **Variable 1: NVL72 / CPX compute rack weight.** Span 1,200–1,600 kg per rack. 9 racks. Each 100 kg/rack change = ±900 kg on the Cassette total. Source of uncertainty: M-02 (C-01 carryforward) — NVIDIA Vera Rubin platform published reference mass.
- **Variable 2: Delta 660 kW in-row power rack weight.** Span 800–1,400 kg per rack. 5 racks. Each 100 kg/rack change = ±500 kg on the Cassette total. Source of uncertainty: M-07 — Delta Electronics published specification.

### 12.1 Combined sensitivity matrix

Total Cassette mass (kg), at combinations of compute rack mass and Delta in-row rack mass, with the §2 integration contingency held fixed at 915 kg:

| | Compute = 1,200 kg | Compute = 1,500 kg (A-01 baseline) | Compute = 1,600 kg |
|---|---:|---:|---:|
| **Delta = 800 kg** | 25,065 | 27,765 | 28,665 |
| **Delta = 1,000 kg (baseline)** | 26,065 | **28,765** | 29,665 |
| **Delta = 1,200 kg** | 27,065 | 29,765 | 30,665 |
| **Delta = 1,400 kg** | 28,065 | **30,765** | 31,665 |

All values kg. ISO 668 R = 30,480 kg. **Bold** cells: baseline and sensitivity-high scenarios explicitly tracked in §2.3.

### 12.2 Compliance boundary

At the A-01 baseline compute-rack weight of 1,500 kg, the compliance boundary is the Delta rack weight that lands the Cassette at exactly 30,480 kg:

Cassette mass @ 1,500 kg compute, variable Delta = 22,850 (raw excl. Delta) + 5X + 915 (contingency) = 23,765 + 5X. Setting this to 30,480:

$$X_{boundary} = (30{,}480 - 23{,}765) / 5 = 1{,}343 \text{ kg per Delta rack}$$

**M-07 must resolve at or below 1,343 kg per Delta rack** for the Cassette to remain ISO-compliant at the A-01 baseline compute-rack weight. The 1,000 kg baseline carries a 343 kg per-rack margin against this boundary.

If M-02 resolves above 1,500 kg (for example, if the NVL72 / CPX populated rack lands at 1,600 kg), the boundary tightens:

| Compute rack mass (A-01) | Delta compliance boundary |
|---:|---:|
| 1,400 kg | 1,523 kg |
| 1,500 kg | 1,343 kg |
| 1,600 kg | 1,163 kg |
| 1,700 kg | 983 kg |

At 1,700 kg per compute rack, the Cassette is over the ISO limit even with Delta at 1,000 kg. The compound sensitivity of both major open items is the reason M-02 and M-07 are both P-0 / CRITICAL items in §18.

### 12.3 Non-compliance pathways

Three combinations of M-02 and M-07 put the Cassette over 30,480 kg:

- M-02 = 1,500 kg AND M-07 ≥ 1,343 kg (the §12.2 boundary)
- M-02 = 1,600 kg AND M-07 ≥ 1,163 kg
- M-02 ≥ 1,700 kg AND any M-07 ≥ 983 kg

If any of these land, mitigation options are: (a) remove mass elsewhere — most promising candidates are §3 corner casting reinforcement plates (200 kg; only if M-05 clears offshore shipping waiver), §11 spare parts kit relocation (25 kg; trivial), and the §2 integration contingency itself (915 kg; consuming it requires tight integration discipline); (b) ship under a special-load exception procedure with carrier acknowledgement; (c) split the Cassette into two ISO envelopes for transport and integrate on-site.

Mitigation option (c) is a significant architectural change and is not preferred; it is documented here as a known fall-back.

---

## 13. Longitudinal center of gravity

Reference: the ELEC end wall at X = 0 mm (Cassette interior). Overall cassette interior length ~11,800 mm per INT-001 §5. X increases from ELEC end (where the main disconnect, ECP, bus duct entry live) toward the COOLING end (where QBH-150, MIVs, manifold headers live).

Approximate X-coordinates for the major mass contributors, with rack positions from INT-001 §5 layout:

| Item | Mass (kg) | X (mm) | Mass·X (kg·mm) |
|---|---:|---:|---:|
| ELEC ECP + Magnum DS + Pow-R-Way + AC-side subtotal (§7.1 + portion of §7.3) | 420 | 400 | 168,000 |
| Delta R11 (Delta 660 kW in-row) | 1,000 | 1,600 | 1,600,000 |
| Delta R12 | 1,000 | 2,200 | 2,200,000 |
| Delta R13 | 1,000 | 2,800 | 2,800,000 |
| Delta R14 | 1,000 | 3,400 | 3,400,000 |
| Delta R15 | 1,000 | 4,000 | 4,000,000 |
| Control rack R10 | 700 | 4,700 | 3,290,000 |
| Compute rack R1 | 1,500 | 5,500 | 8,250,000 |
| Compute rack R2 | 1,500 | 6,100 | 9,150,000 |
| Compute rack R3 | 1,500 | 6,700 | 10,050,000 |
| Compute rack R4 | 1,500 | 7,300 | 10,950,000 |
| Compute rack R5 | 1,500 | 7,900 | 11,850,000 |
| Compute rack R6 | 1,500 | 8,500 | 12,750,000 |
| Compute rack R7 | 1,500 | 9,100 | 13,650,000 |
| Compute rack R8 | 1,500 | 9,700 | 14,550,000 |
| Compute rack R9 | 1,500 | 10,300 | 15,450,000 |
| DC busway 6,000 A (15 m along cassette) | 330 | 5,900 | 1,947,000 |
| Fire suppression (cylinder near ELEC end, nozzles distributed) | 180 | 3,500 | 630,000 |
| In-cassette PG25 coolant + manifolds + MIVs + QBH | 445 | 7,500 | 3,337,500 |
| Container shell + modifications (distributed) | 6,100 | 5,900 | 35,990,000 |
| Cables (distributed, weighted toward racks) | 702 | 6,200 | 4,352,400 |
| Leak / drip (under racks R1–R10) | 160 | 7,900 | 1,264,000 |
| Controls / §11 (ECP-concentrated) | 170 | 500 | 85,000 |
| Integration contingency (distributed) | 915 | 5,900 | 5,398,500 |
| Racks anchors (distributed at rack positions) | 60 | 5,900 | 354,000 |
| **Totals** | **28,765** | — | **177,516,400** |

X_CG = 177,516,400 / 28,765 ≈ **6,172 mm**, measured from the ELEC end wall.

Relative to the container center at X_center = 11,800 / 2 = 5,900 mm:

$$\Delta X_{CG} = 6{,}172 - 5{,}900 = +272 \text{ mm toward the COOLING end}$$

This is a 2.3 % bias from geometric center, well within the typical ±5 % container-center tolerance for safe handling. Rev 2.0 X_CG with 13 compute racks and an internal CDU was closer to center (~5,950 mm); Rev 3.0 is biased slightly toward the cooling end because the compute racks are now 9 and clustered in the aft 60 % of the Cassette, while the lighter Delta racks sit forward.

Rev 2.0 had the CDU at X = 11,282 mm contributing 600 kg × 11,282 mm = 6.8 million kg·mm; its removal pulls the CG back toward center. The Delta racks at X = 1,600–4,000 mm at 5,000 kg total pull the CG forward (toward ELEC end) — these two effects partly offset. The net residual +272 mm aftward bias is attributable to the 9 compute racks being dense and aft-clustered, now that 4 of the Rev 2.0 compute-rack positions are replaced by lighter Delta power racks near the ELEC end.

---

## 14. Vertical center of gravity

Reference: the Cassette floor at Z = 0 mm. Container interior height 2,700 mm (HC). Rack top of frame ~2,200 mm.

| Item | Mass (kg) | Z (mm) | Mass·Z (kg·mm) |
|---|---:|---:|---:|
| Container shell (floor + walls + roof — composite Z_CG) | 6,100 | 1,400 | 8,540,000 |
| Racks R1–R9 compute (populated, Z_CG — top-biased from heavy trays) | 13,500 | 1,150 | 15,525,000 |
| Control rack R10 | 700 | 1,100 | 770,000 |
| Delta racks R11–R15 (air-cooled, 6 shelves + BBU at mid-height, Z_CG ≈ 1,100 mm) | 5,000 | 1,100 | 5,500,000 |
| Rack anchors / snubbers | 60 | 100 | 6,000 |
| §6 cooling (manifolds at ceiling, coolant distributed) | 445 | 1,900 | 845,500 |
| §7 electrical (busway at ceiling ~2,200 mm, Magnum DS near floor ~800 mm, averaged) | 833 | 1,600 | 1,332,800 |
| §8 fire (cylinder floor-standing, piping at ceiling) | 180 | 1,700 | 306,000 |
| §9 leak / drip (below rack floor, Z ≈ 50 mm) | 160 | 50 | 8,000 |
| §10 cables (overhead tray + underfloor raceway, averaged) | 702 | 1,500 | 1,053,000 |
| §11 controls (ECP mid-height) | 170 | 1,200 | 204,000 |
| Integration contingency | 915 | 1,300 | 1,189,500 |
| **Totals** | **28,765** | — | **35,279,800** |

Z_CG = 35,279,800 / 28,765 ≈ **1,227 mm** above floor.

For a 40-ft HC container with interior height 2,700 mm, the geometric center is Z = 1,350 mm. The Cassette Z_CG is approximately 123 mm below center — a favorable (below-center) bias. This is primarily because the fully populated racks are floor-mounted and their own internal mass distribution is biased toward the bottom two-thirds of the rack frame (heavy compute trays and power shelves are low; lighter networking and cable management is high).

Rev 2.0's Z_CG was ~1,185 mm (slightly lower because the CDU sat low at Z ≈ 600 mm and pulled the CG down). Rev 3.0's Z_CG is 42 mm higher than Rev 2.0 but still well below the container center. No handling or two-high-stacking concern is raised by the Z_CG change.

---

## 15. Two-high stacking analysis

Analysis against ISO 1496-1 and DNV-OS-D101. M-05 open item covers the offshore DNV review; domestic two-high stacking is evaluated here.

### 15.1 Corner casting utilization (ISO 1496-1 stacking test)

ISO 1496-1 requires that a container support a stacking test load of **9 × R** applied vertically through the top corner castings (R being the max gross mass rating of the container). For R = 30,480 kg:

$$F_{stack} = 9 \times 30{,}480 = 274{,}320 \text{ kg-force} = 2{,}690 \text{ kN (nominal, per corner divided by 4)}$$

Per-corner design load = 2,690 / 4 = 672 kN per bottom corner casting when an identical loaded container sits on top.

Rev 3.0 Cassette at baseline 28,765 kg contributes 28,765 / 4 = 7,191 kg-force per bottom corner casting = 70.5 kN per corner to the upper container. Test load envelope relative to design = 70.5 / 672 = 10.5 % utilization per corner under two-high static stacking. At sensitivity-high (30,765 kg), utilization rises to 7,691 / 672 kN = 11.5 %.

Margin on ISO 1496-1 stacking test for the lower Cassette is therefore large — the lower Cassette's corner castings are specified for 9R loading and are being asked to carry only 1R from a single stacked Cassette above.

### 15.2 Offshore dynamic stacking (DNV-OS-D101)

DNV-OS-D101 adds a 5g dynamic vertical load component on corner castings for offshore shipment. The applicable case is the single upper Cassette at 5g vertical acceleration bearing on the lower Cassette's corners.

Per-corner dynamic load at baseline = (28,765 × 5) / 4 = 35,956 kg-force = 352 kN per corner. Utilization vs 672 kN/corner = 52.4 %.

At sensitivity-high (30,765 kg, if the Cassette were shipped in that state): (30,765 × 5) / 4 = 38,456 kg-force = 377 kN. Utilization = 56 %.

At either scenario, corner casting design capacity is adequate for DNV-OS-D101 5g offshore stacking. The 200 kg of corner casting reinforcement plates in §3 is retained as a conservative margin against local welding and seat-plate bearing stresses, pending the M-05 DNV review of the full detail design.

### 15.3 Stacking conclusion

Two-high stacking is structurally supported for both domestic (ISO 1496-1) and offshore (DNV-OS-D101) cases at the baseline mass. Two-high stacking at the sensitivity-high mass (30,765 kg) would be non-compliant with ISO 668 itself (the upper Cassette exceeds R), independent of any stacking-specific concern — this is the reason M-07 drives the compliance decision.

---

## 16. Key assumptions

Updated assumption register. A-02 is removed; A-01, A-03 through A-12 are issued new or carried forward. Status column: **L** = locked, **W** = working estimate, **O** = open (tied to a specific M-xx).

| ID | Assumption | Status | Open item link |
|---|---|:-:|---|
| A-01 | Compute rack (NVL72 / CPX) populated mass = 1,500 kg each (R1–R9) | O | M-02 (P-0) |
| A-02 | **REMOVED** — superseded by P3-03 / P3-09. The Delta 660 kW in-row racks are physically separate units counted in §4.3; the Delta 800 V → 50 V DC/DC shelf inside each compute rack is included in the 1,500 kg compute rack estimate per A-07. Rev 2.0's A-02 conservative case (31,415 kg) is obsolete. | CLOSED | M-01 (closed) |
| A-03 | Control rack R10 populated mass = 700 kg | W | — |
| A-04 | Delta 660 kW in-row power rack populated mass = 1,000 kg each (R11–R15) | O | M-07 (P-0 CRITICAL) |
| A-05 | CDU skid is external (COOL2-001 scope); Cassette contribution = 0 kg | L | — (COOL2-001 §1) |
| A-06 | In-cassette PG25 coolant = 185 kg (180 L × 1.017 kg/L; cassette interior only per COOL2-001 §5) | L | — |
| A-07 | The Delta 800 V → 50 V DC/DC shelf that sits inside each NVL72 / CPX compute rack is included in the 1,500 kg rack estimate. One such shelf per R1–R9. | L | — (BOM-001 §4 note) |
| A-08 | Eaton Magnum DS 6,000 A, 480 V AC main disconnect = 270 kg | O | M-09 (P-1) |
| A-09 | Eaton Pow-R-Way III bus duct wall entry section = 75 kg | O | M-10 (P-1) |
| A-10 | Per-Delta-rack 480 V AC feeder cable set = 103 kg per feeder (2× 300 mm²/phase × 3 phases + 95 mm² ground × ~5 m); 5 feeders × 103 kg = 515 kg total | L | — (ELEC-001 §8) |
| A-11 | 6,000 A DC busway linear mass = 22 kg/m (Starline or Siemens SIVACON 8PS equivalent) | W | — |
| A-12 | Drip trays populate 10 rack positions (R1–R10). Delta in-row power racks R11–R15 are air-cooled per COOL-001 §1 and carry no drip trays. | L | — |

---

## 17. Findings and required actions

### 17.1 Findings

**Finding 1 — Baseline is compliant with 1,715 kg margin.** At the A-01 baseline compute rack weight (1,500 kg) and the A-04 baseline Delta rack weight (1,000 kg), the Cassette totals 28,765 kg, which is 1,715 kg below the ISO 668 R value of 30,480 kg. This is the operational claim as of Rev 3.0.

**Finding 2 — Compliance is conditionally sensitive to M-07.** At the A-01 baseline compute rack weight (1,500 kg), the compliance boundary on Delta rack weight is 1,343 kg per rack. Above 1,300 kg per Delta rack, margin drops below 200 kg (below the §2 integration contingency line's own budget absorption of real-world drift). At 1,400 kg per Delta rack, the Cassette exceeds the ISO limit by 285 kg. **M-07 must resolve at or below 1,343 kg per rack** for the Cassette to ship as a single ISO-compliant unit. A resolution above this threshold forces mitigation per §12.3 options (a), (b), or (c).

**Finding 3 — The Delta in-row rack weight (M-07) has replaced Delta shelf inclusion (A-02) as the number-one compliance gate.** Rev 2.0 treated A-02 (whether the 110 kW Delta shelves were included in the NVL72 rack estimate) as the single most sensitive assumption, with a 31,415 kg conservative case that was over the ISO limit. Rev 3.0 eliminates that ambiguity architecturally: the Delta shelves are physically housed in five separate in-row racks that are separately counted in §4.3. The new compliance gate is the total weight of those in-row racks, which is an empirical vendor-data question rather than an accounting question.

**Finding 4 — CDU removal headroom is partially consumed by the new in-cassette electrical architecture.** The Rev 2.0 → Rev 3.0 reduction path has three large subtractions totaling about 6,930 kg — CDU removed (−600 kg), coolant reduced (−215 kg), and compute rack count reduced from 13 to 9 (4 × 1,500 kg = −6,000 kg). Partially offsetting, Rev 3.0 adds about 5,765 kg — five Delta in-row racks (+5,000 kg at baseline), heavier AC main disconnect net change (+190 kg), bus duct entry (+75 kg), and per-rack AC feeders (+515 kg), less the R10 consolidation savings (−200 kg) and drip tray reduction (−40 kg) and CDU subpanel removal (−18 kg). Net: approximately −1,170 kg vs Rev 2.0. The 28,765 kg total is the arithmetic result.

**Finding 5 — Compound sensitivity to M-02 + M-07 creates a small region of the (compute, Delta) plane where no single mitigation suffices.** Per §12.3, if M-02 resolves above 1,700 kg, no plausible M-07 outcome keeps the Cassette under ISO. This is not currently the expected NVL72 / CPX outcome — vendor reference suggests 1,400–1,550 kg is the working range — but it is a documented exposure. M-02 and M-07 are both P-0.

### 17.2 Required actions

| ID | Action | Priority | Owner | Gate |
|---|---|:-:|---|---|
| M-02 | Obtain NVIDIA Vera Rubin NVL72 / CPX populated rack mass (C-01 carryforward). Document any payload variants that would shift the estimate. | P-0 | NVIDIA Inception channel | Procurement; Cassette ISO compliance |
| M-07 | Obtain Delta Electronics 660 kW in-row power rack populated mass for the baseline SKU and a high-confidence upper bound. Include BBU mass contribution clearly. | P-0 CRITICAL | Delta Electronics direct | Cassette ISO compliance; procurement release |
| M-05 | DNV corner casting review for offshore two-high stacking. Validate that the 200 kg corner casting reinforcement in §3 is adequate at the baseline mass and at the sensitivity-high mass. | P-1 | Marine surveyor + mechanical lead | Offshore shipping qualification |
| M-06 | Update Cassette-INT-001 nameplate and weight placard after M-02 and M-07 resolve. | P-2 | Scott Tomsu | Cross-document consistency; final nameplate |
| M-08 | Confirm whether the 2× DN150 × 5 m flex hoses (COOL2-001 §6, Parker ParFlex 797TC or Gates Mega4000) are inside the Cassette mass boundary at shipment. Estimated 75–100 kg per hose if included. | P-1 | Mechanical lead + logistics | Ship-weight boundary; possible ±200 kg shift |
| M-09 | Obtain Eaton Magnum DS 6,000 A shipping weight (±80 kg sensitivity). | P-1 | Eaton Engineering | A-08 close; §7 subtotal accuracy |
| M-10 | Obtain Eaton Pow-R-Way III bus duct wall entry section weight. | P-1 | Eaton Engineering | A-09 close; §7 subtotal accuracy |
| M-04 | Cold plate internal volume per NVL72 / CPX rack — supports A-06 cassette-interior coolant validity and cross-checks COOL2-001 §5 cassette vs skid volume allocation. | P-2 | NVIDIA + thermal lead | A-06 supporting evidence |

---

## 18. Open items

| ID | Item | Priority | Resolves |
|---|---|:-:|---|
| M-01 | **A-02 Delta shelf inclusion — CLOSED / SUPERSEDED.** Delta 660 kW in-row racks are separate physical units counted in §4.3. The 800 V → 50 V DC/DC shelf inside each compute rack is included in the 1,500 kg compute rack estimate per A-07. No separate §5 mass contribution. | CLOSED | A-02 (obsolete) |
| M-02 | NVL72 / CPX compute rack weight confirmation (C-01 carryforward). Obtain NVIDIA Vera Rubin published reference mass for the populated NVL72 / CPX rack configuration specified in BOM-001 Rev 1.3 §3. Each 100 kg change = ±900 kg Cassette total. | P-0 | A-01, §4.1, compliance |
| M-03 | **CDU skid weight — CLOSED / MOVED.** CDU is external per COOL2-001 Rev 1.0 §1; §8 of COOL2-001 documents ~5,800 kg wet. Not a Cassette mass open item. | CLOSED | — |
| M-04 | Cold plate internal volume per NVL72 / CPX rack. Feeds A-06 cassette-interior coolant volume validity. | P-2 | A-06 |
| M-05 | DNV corner casting review for offshore two-high stacking at Rev 3.0 mass. Validate §3 corner reinforcement adequacy. | P-1 | §15 stacking analysis |
| M-06 | Update Cassette-INT-001 nameplate after M-02 and M-07 resolve. | P-2 | Cross-doc consistency |
| M-07 | **Delta 660 kW in-row rack weight (R11–R15) — CRITICAL.** Obtain from Delta Electronics. Each 100 kg change = ±500 kg Cassette total. Compliance boundary at 1,343 kg/rack assuming A-01 compute = 1,500 kg. Gates procurement release. | **P-0 CRITICAL** | A-04, §4.3, compliance |
| M-08 | Flex hose assembly weight (COOL2-001 §6: 2× DN150 × 5 m, Parker ParFlex 797TC or Gates Mega4000). Supplied with Cassette per COOL2-001 §6 — confirm whether inside Cassette ISO-envelope mass boundary at transport. Estimate ~75–100 kg per hose if included. Possible ±200 kg shift to Cassette shipping mass. | P-1 | Cassette / skid mass boundary |
| M-09 | Eaton Magnum DS 6,000 A actual shipping weight (baseline estimate 270 kg; ±80 kg tolerance). Obtain from Eaton Engineering. | P-1 | A-08, §7.1 |
| M-10 | Eaton Pow-R-Way III bus duct wall entry section weight (baseline estimate 75 kg). Confirm from Eaton Engineering. | P-1 | A-09, §7.1 |

---

## Document control

**Cassette-MASS-001 — Rev 3.0 — CONFIDENTIAL**
**Prepared by:** Scott Tomsu · CEO / Chief Engineer · scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana
**Companion to:** Cassette-INT-001 Rev 1.3 · Cassette-BOM-001 Rev 1.3 · Cassette-ELEC-001 Rev 1.3 · Cassette-COOL-001 Rev 1.1 · Cassette-COOL2-001 Rev 1.0 · Cassette-FIRE-001 Rev 1.2 · Cassette-SIS-001 Rev 1.2 · Cassette-ECP-001 Rev 1.2
**Supersedes:** Cassette-MASS-001 Rev 2.0 (deleted)
**Authority scope:** the mass statement and weight budget for one ADC 3K Cassette — by-section mass totals (§3 through §11), integration contingency basis (§2), sensitivity analysis against the two P-0 open-item variables (§12), longitudinal and vertical center-of-gravity (§13–§14), two-high stacking analysis against ISO 1496-1 and DNV-OS-D101 (§15), the assumption register (§16) and findings / required-action set (§17) against ISO 668 R = 30,480 kg, and the open-item register (§18).

**Compliance claim at Rev 3.0.** Baseline Cassette mass 28,765 kg, compliant with ISO 668 R = 30,480 kg with 1,715 kg margin. Compliance at the A-01 baseline compute weight is conditional on M-07 resolving at or below 1,343 kg per Delta in-row rack. The sensitivity-high case (M-07 = 1,400 kg) exceeds the ISO limit by 285 kg and is explicitly non-compliant as a single ISO unit.

**End of Cassette-MASS-001 Rev 3.0.**
