# Cassette PROJECT — CONVERSATION HANDOVER

**Date:** 2026-04-19
**Prepared by:** Scott Tomsu with Claude
**Purpose:** Transfer context to a fresh conversation so platform-level work can begin on solid ground.

---

## HOW TO USE THIS DOCUMENT

Upload this file plus the four current pod documents (listed in §2) at the start of the new conversation. Tell the new Claude: *"Read the handover document first, then the four pod documents. Do not propose anything that contradicts them. Ask before assuming."*

That's the whole protocol.

---

## §1  PROJECT ONE-PAGER

### What Cassette Is

A containerized AI compute Cassette — 40 ft HC ISO container, unmanned, sealed, stackable, marine-capable. Holds 15 NVIDIA Vera Rubin NVL72 racks. Delivered as a drop-in module to any platform that can supply 800 V DC (or 415 V AC), chilled water, fiber, and a bolted connection to ground. The Cassette is the product. Everything upstream of the pod's External Connection Panel (ECP) is the platform's problem.

### Current Scope Lock

- **Cassette design: LOCKED.** Cassette-INT-001 is the authoritative interior design. Cassette-ECP-001 Rev 1.0 is the authoritative interface. Cassette-BOM-001 Rev 1.0 is the authoritative parts list.
- **Platform design: NOT STARTED.** Microgrid, BESS, CHP cascade, site layout, Trappey's 100 MW, Marlie block topology — none of this has valid documentation yet. The next conversation picks up here.

### Current Numbers (Use These, Reject Anything Else)

| Parameter                          | Value                                     |
|------------------------------------|-------------------------------------------|
| Per-rack power (NVL72 tier)        | **120 kW** (NVIDIA-published, Oberon/MGX 3rd gen) |
| Per-rack power (NVL144 CPX upgrade) | **160 kW** (same rack, different compute trays) |
| Per-rack power (Rubin Ultra Kyber) | 600 kW (2027+, DIFFERENT RACK — not our pod) |
| Racks per pod                      | **15** (13 compute + 1 InfiniBand + 1 storage/mgmt) |
| Rack standard                      | **21" ORv3 / NVIDIA MGX 3rd gen (Oberon)** |
| GPUs per pod                       | **936 Rubin GPUs** (NVL72 tier)           |
| Pod IT load (NVL72)                | **1,585 kW**                              |
| Pod IT load (NVL144 CPX)           | **2,105 kW**                              |
| Pod facility load (NVL72)          | **1,677 kW**                              |
| Pod facility load (NVL144 CPX)     | **2,212 kW**                              |
| Pod cooling demand                 | **1.6–2.2 MW** secondary loop             |
| Pod operating weight               | **~30,000 kg** (98.6% ISO 40 ft HC gross) |
| Primary input                      | 800 V DC (or 415 V AC 3-ph alternate)     |
| CDU                                | CoolIT CHx2000 (2 MW, L2L)                |
| CHW supply/return at ECP           | 7–12 °C / 12–18 °C                        |
| Cold plate supply/return           | 45 °C / 55–60 °C                          |
| Fire suppression                   | Ansul Novec 1230 + VESDA-E VEU-A00        |
| Dehumidification                   | Munters HCD-600 on external skid          |
| Power conversion                   | In-rack Delta 110 kW shelves — NO sidecar |
| Access                             | 12 bolt-sealed panels, 6 per long side    |
| BMS                                | NVIDIA Jetson AGX Orin (N+1)              |

### What "Unmanned" and "Sealed" Mean

- No interior aisle. Nobody walks inside.
- No HVAC for personnel comfort.
- All service from outside via the 12 access panels.
- End doors Could still be used possibly For ease of installation of internal equipment.
- The Cassette is stackable — any protrusion goes on the long sides only (not top, not ends).

### What's Done / What's Not

**Done:**
- Cassette interior design (15 racks, full layout, floor-routed manifold and power)
- ECP definition (both ends, full pinout, commissioning acceptance criteria)
- BOM with vendor identification
- Onshore + offshore variants called out with marinization deltas

**Not done:**
- Platform electrical (how the Cassette gets its 800 V DC — microgrid, BESS, gensets)
- Platform thermal (how the Cassette gets its chilled water — CHP cascade, BROAD chillers, river cooling)
- Site layout (how many Cassette, what arrangement, what shared infrastructure)
- Trappey's 100 MW specific site engineering
- CG260-16 CHP comparison for larger platforms (G3520K work existed in withdrawn docs)
- Financial model
- 3-view dimensional drawings suitable for fabricator
- Updated SVG Cassette layout (the existing adc3k-pod-layout.svg shows 10 racks; needs update to 15)

---

## §2  CURRENT DOCUMENT SET

These four documents are the authoritative reference. Upload all four at the start of the next conversation along with this handover.

| File                         | Rev  | Purpose                                  |
|------------------------------|------|------------------------------------------|
| READMEa.md                    | 1.0  | Index + status + open items + withdrawn list |
| Cassette-INT-001-Rev2.0.md        | 1.0  | Cassette interior design specification — 30 sections |
| Cassette-ECP-001-Rev1.0.md        | 1.0  | ECP interface control document — pod↔platform contract |
| Cassette-BOM-001-Rev1.0.md    | 1.0  | Bill of materials — procurement-ready, no pricing |

---

## §3  TERMINOLOGY & NAMING CONVENTIONS

Use these exactly. Mismatches from past conversations caused real confusion.

### Product & Platform Names

- **Cassette** — the 40 ft container module. "Cassette" preferred over "Pod" going forward (pod was used in earlier withdrawn docs).
- **Marlie1** — the 10 MW platform architecture (one of N pods + shared infrastructure). Not yet documented in the current set.
- **Compute Cassette** — marketing umbrella for the overall Scott Tomsu.
- **Trappey's** — the Lafayette 100 MW site at the historic cannery. Uses Cassette blocks replicated N times.

### Technical Terms

- **ECP** — External Connection Panel. The Cassette's interface boundary. Two zones: ELEC and CDU.
- **Oberon** — NVIDIA's MGX 3rd-gen rack for Vera Rubin NVL72. 21" ORv3, 48U, ~120 kW per rack.
- **Kyber** — NVIDIA's future vertical-blade rack for Rubin Ultra NVL576. Different from Oberon. 600 kW/rack. Not this Cassette.
- **In-rack shelf** — Delta power shelves mounted inside the Oberon rack frame (Vera Rubin NVL72 110 kW, 800V→50V DC/DC, etc.). Not a separate cabinet.
- **Sidecar** — an external rectifier cabinet used for legacy 19" racks or for Kyber. **Not used in this Cassette.** Past conversations conflated "sidecar" and "in-rack shelf" — they are not the same thing.
- **Pinhook** — one word, not "Pin Hook." The substation near the Trappey's site.

### Critical Distinction

**"Rack"** refers to one Oberon frame (one NVL72). **"Cassette"** refers to a container with 15 racks. **"Block"** (or "Marlie1 block") refers to a platform-level aggregation of Cassette (TBD count, not yet specified). **"Site"** refers to the full deployed set of blocks (e.g., Trappey's 100 MW).

Never say "rack" when you mean "Cassette" or vice versa.

---

## §4  HARD CONSTRAINTS (DO NOT VIOLATE)

Any future work must respect these. If a proposal appears to require violating one, stop and raise the conflict.

### Numerical Hard Constraints

1. **Per-rack power is 120 kW (NVL72) or 160 kW (NVL144 CPX).** Never 230 kW, 200 kW, or any other fabricated number. These are the only NVIDIA-published values for Vera Rubin on Oberon.

2. **15 racks per Cassette maximum.** Geometry allows up to 20 physically, but ISO gross-weight limit and ECP end-zone requirements cap the useful number at 15. Weight is the binding constraint, not length.

3. **~30,000 kg operating weight per Cassette.** ISO 40 ft HC gross weight limit is 30,480 kg. The pod is 98.6% of that at 1,500 kg/rack estimate. If NVIDIA confirms rack weight ≥1,600 kg, drop to 14 racks.

4. **Cassette facility load: 1.6–2.2 MW.** Never quote a pod load outside this band unless the compute spec changes.

5. **No rectifier cabinet inside the pod.** All AC→DC conversion happens in-rack via Delta shelves.

### Architectural Hard Constraints

6. **The ECP is the contract.** No pod component reaches past the ECP. No platform component reaches past the ECP. The ECP schedule in Cassette-ECP-001 is authoritative.

7. **800 V DC single-ended.** NOT ±400 V. This matches NVIDIA Kyber ecosystem and the Oberon power envelope.

8. **Ungrounded DC (IT system) with IMD.** Not solidly grounded. Per IEC 61557-8.

9. **Cassette is a sink, never a source.** No grid export, no back-feed, no power flow outward at the ECP.

10. **Unmanned interior.** No future "what if a tech could just pop inside" thinking. All service is external.

### Process Hard Constraints

11. **Every factual number gets a source.** If it's a vendor spec, cite the vendor document. If it's a calculation, show the math. If it's an estimate, label it as an estimate with the basis. No fabrication — this is what caused the month of tail-chasing.

12. **Search before citing current product specs.** NVIDIA, Delta, CoolIT, Munters, Ansul, Bender — their product lines move. Don't rely on memory.

13. **When in doubt, stop and ask.** Better to ask one question than to produce a document that has to be withdrawn.

---

## §5  HISTORY OF REVISIONS AND WITHDRAWALS

For continuity in case questions arise about earlier work:

### Key Corrections in Rev 

### P-0 Critical / Gating

- **C-01** — Confirm Vera Rubin NVL72 loaded rack weight with NVIDIA/Foxconn/HPE. Current 1,500 kg estimate. If ≥1,600 kg → drop to 14 racks. This is the single most important outstanding number.
- **C-02** — Delta 110 kW shelf 800 V DC input variant availability + lead time.
- **C-03** — CoolIT CHx2000 lead time and delivery schedule.

### P-1 High Priority

- **C-04** — Munters HCD-600 RFQ (electric reactivation, IP66 skid for marine).
- **C-05** — Ansul Novec 1230 USCG-approved cylinder brackets (offshore variant).
- **C-06** — ABS/DNV module certification path (offshore variant).
- **C-07** — Bender iso-PV1685 IMD 800 V DC variant confirmation.

### Long-Lead Items

NVIDIA racks (18–24 weeks), Quantum-X800 switches (16–20 weeks), CoolIT CHx2000 (14–20 weeks), Delta 110 kW shelves (14–18 weeks), new-build 40 ft HC container (12–16 weeks). Any of these on the critical path.

---

## §7  WHAT THE NEXT CONVERSATION SHOULD TACKLE

Scott's explicit next priority: **-Cassette level documents — .**


---

## §8  WORKING RELATIONSHIP NOTES

For the next Claude, context on how Scott works:

- Direct communication style. Doesn't want hedging. Wants technical answers, not hedges.
- Pushes back hard on fabricated or inconsistent numbers. This is correct — it caught multiple real errors.
- Prefers "engineer says X" framing over "here are five options." Give the answer, show the reasoning, flag the uncertainties.
- Hands-on technical background — construction GC, aviation, robotics, subsea ROV. Treat him as a peer, not a client to be led.
- Marine/offshore deployment matters to this project — not a marketing angle, an actual engineering target.
- When frustrated, it's usually because Claude is being evasive or proposing things that contradict earlier locked-in decisions. Re-ground in the current document set and get specific.

### What Worked

- Walking through math in code blocks, showing the computation, then summarizing the answer
- Pushing back constructively on Scott's pushbacks when the earlier work was actually wrong (but owning the error clearly)
- Searching vendor specs instead of guessing from training data
- Asking narrow clarifying questions via the interactive input tool, not open-ended prose

### What Did Not Work

- Fabricating numbers without sources
- Carrying stale figures forward across revisions unchecked
- "I'll note that as an open item" when the right response is "stop and get the real number now"
- Reframing Scott's corrections as "pushback" when they were legitimate corrections to fabricated content
- Proposing alternate architectures without first aligning to the locked pod spec

---

## §9  ONE-PARAGRAPH STARTING PROMPT FOR THE NEXT CONVERSATION

Suggested opener to paste into the new conversation (edit as you see fit):

> *I'm continuing a project from a prior conversation. I'm uploading the handover document and four current Cassette design documents. Read the handover first — §4 has the hard constraints and §5 has the list of withdrawn documents that should not be used. After you've read all five files, confirm you understand the Cassette

---

**Cassette Project — Conversation Handover**
**2026-04-19 · Scott Tomsu · scott@adc3k.com · (337) 780-1535 · Lafayette, Louisiana**
**CONFIDENTIAL**
