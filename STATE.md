# Mission Control — Project State
Last updated: 2026-04-04 (end of session — Pure DC AI Factory deck updated, rack numbers corrected to Vera Rubin Max P)

---

## SESSION SUMMARY — April 4, 2026 (Pure DC AI Factory — Deck Update)

### pure-dc-ai-factory-package.html — UPDATED
- **Hardware platform corrected:** Blackwell → Vera Rubin NVL72 (Max P, liquid cooled, full buildout)
- **kW per rack:** 130 kW → **230 kW** (Vera Rubin Max P)
- **Total racks:** 1,538 → **870**
- **Total GPUs:** 110,736 → **62,640**
- **Total HBM:** 8.86 PB → **18.04 PB** (Vera Rubin 288 GB/GPU vs Blackwell 192 GB/GPU)
- **Phase language removed entirely** — hyperscalers want full buildout at once, no phase 1/2 framing
- **New stat in Project Snapshot:** "870 NVL72 Racks" replaces "22 Months Phase 1"
- **new-iberia-200mw-spec.html:** NOT updated yet — hold until Bloom/FCE return with footprint
- **Feedback saved:** `memory/feedback_no_phase_language.md` — no phase 1/2 in hyperscaler decks

### Key Decisions — April 4
- Bloom and FuelCell Energy will design the building footprint — ADC gives them the hard compute numbers, they size their generation zone
- No diagrams handed to vendors — just numbers
- Full 200 MW single buildout, no phases
- Vendor strategy unchanged: send spec to both, don't tell them about each other, let them compete

---

## SESSION SUMMARY — April 3, 2026 (CONTINUED — New Iberia 200 MW)

### New Iberia — Site Pivoted to 200 MW Hyperscaler AI Factory
- **Decision:** Hwy 14 & US-90 New Iberia site (formerly pod factory Step 2) pivoted to 200 MW greenfield AI factory targeting hyperscaler customer. Pod factory Step 1 (Baton Rouge) carries manufacturing independently.
- **Rationale:** SNG mainline on property + hyperscaler demand at record levels. 200 MW can be sold before groundbreaking.
- **Layout locked:** Three-zone rectangle. One long pass. ~480 ft × 180 ft. Zone A (Bloom, 40 ft) | Zone B (Compute, 100 ft) | Zone C (BESS, 40 ft). 1500V DC bus punches through fire-rated walls — ≤15 ft run to rack.
- **Compute:** 1,538 NVL72 racks / 110,736 GPUs / 8.86 PB HBM / 38 Vera Rubin PODs
- **Power:** Bloom SOFC N+1 (~200 units) + LFP BESS 800 MWh + First Solar TR1 roof. Full DC microgrid. No grid.
- **PUE:** 1.05 target. Power cost: $0.058–$0.068/kWh.
- **Delivery:** Phase 1 (100 MW) Month 22. Full 200 MW Month 28.
- **Spec deck built:** `private-decks/new-iberia-200mw-spec.html` — 10 slides. CONFIDENTIAL. SVG floor plan is schematic only — NOT engineering quality. Proper CAD drawing needed before final hyperscaler submission.
- **Memory:** `memory/projects/new_iberia_200mw.md`

### Architecture Evolution — Corridor Module Design (SAVE THIS)
- **Not a room with rows — a corridor module.** Two rows of racks facing each other, sealed, glass door entry, overhead cable management. Liquid-cooled NVL72 = no hot/cold aisle needed. Tighter building, lower cost.
- **Distributed power cells.** Each corridor has its own Bloom + BESS immediately behind a firewall. DC run = 15-20 feet max per module. Not one central power room. Physics working FOR the design.
- **200 MW = N corridor modules stacked.** Phase 1 = subset. Phase 2 = add modules. Nothing running gets touched.
- **Open question for Bloom call:** Minimum efficient Bloom configuration per corridor module? That answer sets the module size.
- **The product is reproducible.** Same design, different parcel. Site qualification replaces engineering. ADC owns the design + Bloom relationship + site pipeline.
- **Hardware agnostic.** OCP Open Rack V3, 130 kW, accepts any hyperscaler OEM — NVIDIA, AMD, Google, whatever they bring.
- **No grid = competitive weapon.** Live when Bloom + BESS commission. 3-7 yr grid queue eliminated.

### Critical Path — New Iberia
1. SNG capacity call — confirm gas volume/pressure for 200 MW Bloom load
2. Site option agreement — 90-day option before spec goes out. Keaty (337) 235-7770
3. Williams Companies outreach — $5.1B committed to gas+AI co-location. media@williams.com
4. Engineering-quality floor plan — CAD/architectural drawing for final submission
5. ITEP pre-application — before groundbreaking. Kristin Johnson 225-342-2083

---

## SESSION SUMMARY — April 3, 2026 (EARLIER — Power Stack + Notion + Financial)

### Power Stack — FINAL, LOCKED, NO EXCEPTIONS
```
1500V DC  FIRST SOLAR TR1    OFFSET — site-dependent, DC-direct 97%
800V DC   BLOOM SOFC (N+1)   PRIMARY — dual units, DC direct, no inverter
          LFP BESS (3-day)   BRIDGE — off-site, ~720 MWh at 10 MW
          DC INTERCONNECT    REDUNDANCY — neighboring AI factory, live backup
```
- **Diesel eliminated.** Louisiana gas pipelines survive Cat 4. Power lines are irrelevant — ADC is behind-the-meter.
- **No grid consumption.** Grid does not appear in the stack.
- **No AC anywhere.** Full DC microgrid.
- Scope 2 = zero. Source water = zero. PUE 1.02-1.05. Scope 1 = Bloom SOFC only.
- Memory file: `memory/projects/power_stack_final.md`

### Notion Cleanup — Done
- Power Distribution Unit Layouts: 20 pre-GTC blocks deleted
- Network Topology Diagrams: 35 pre-GTC blocks deleted (Quantum-3 NDR removed, Quantum-X800 is authoritative)
- CDU Liquid Cooling: already clean
- Session Prompts: no POST-GTC marker found, needs manual review

### Financial Model — Tax Rate Clarified
- LA corporate income tax = 5.5% flat (effective Jan 2025)
- ~25% in old xlsx model = accidentally correct at combined federal+state level
- Assumptions tab must show: LA = 5.5%, Federal = 21%, Combined ~24.2%
- Fixed in `business-model/scenarios.md` — new Corporate Income Tax Rate section added

### OCP Whitepapers Reviewed
- **ESUN** (Meta + Microsoft, Feb 2026): Open Ethernet standard for GPU scale-up fabric. Alternative to NVIDIA InfiniBand. Relevant if ADC deploys non-NVIDIA pods. Not relevant to current NVIDIA-primary build.
- **Energy/Water/Carbon Guidelines** (OCP, March 2026): Validates ADC's dry cooler choice for Louisiana (hot/humid = no evaporative benefit). Confirms ADC's pure DC microgrid = best-in-class on every sustainability metric vs grid-connected competitors.

### Open Items Carried Forward
1. Customer LOI — zero signed. Fatal for institutional investors.
2. NVIDIA TDP confirmation — facility sizing incomplete.
3. HB 827 PILOT — parish-level agreement needed (below $200M threshold).
4. BESS vendor selection — Saft / LG ES Vertech / Fluence.
5. Bus interconnect between sites — open engineering item.
6. Session Prompts Notion page — needs manual cleanup (no POST-GTC marker).

---

## SESSION SUMMARY — March 31, 2026 (SESSION 2)

### Key Decisions This Session

**Trappeys Building Layout — LOCKED**
- Building 3 = Compute Hall (75×300 ft) — racks go here
- Building 4 = Power Hall (150×250 ft) — CDUs, 800V bulk transformer, MV switchgear, batteries, all power equipment. Generators stay outside.
- Buildings 1 & 2 = Trappeys Museum — full restoration, historic value, public-facing, park out front
- 170,000 sq ft total rooftop solar across campus

**10 MW Phase 1 Plan — LOCKED (replaces 3 MW)**
- Previous phase plan was sized to $5M seed raise — not a physical site constraint
- Physical room holds 720 racks. Power is always the constraint.
- New Phase 1: 10 MW, 50 NVL72 racks, 3,600 GPUs
- Genset: Wärtsilä 34SG (~10 MW, partial load efficient) — one unit handles full Phase 1
- Total project CapEx: ~$198-204M gross
- Cash needed after 80% equipment financing (Ornn RVS) + tax credits: ~$55-60M
- Year 2 base case EBITDA: ~$32M → $480-640M implied valuation at 15-20x
- Raise target: ~$55-60M (not $5M — Ornn partnership changes the capital structure)

**OCP LVDC White Paper — Saved as Industry Bible**
- Released March 30, 2026 — Open Compute Project
- ADC = Stage 1d: SST (13.8kV → 800V DC) for racks, separate transformer for building AC
- Training AI factory: 99.9% availability. Inference: 99.999%
- No DC UPS bypass exists — must have N+1 SST modules from day one
- NVIDIA, Eaton, ABB, Amperesand, Trane all co-authored
- Memory file: `memory/projects/ocp_lvdc_standard.md`

**13.8kV confirmed from internal docs** — LUS runs 69/13.8kV across 18 substations. Pin Hook near Trappeys is one of those. Pre-development meeting (337) 291-8426 needed to confirm Pin Hook specific rating.

**Rendering — Middle3.jpg** — Water tower painted white. Natural red brick kept. Black-frame industrial windows replacing bay doors. File: `adc3k-deploy/trappeys-middle3-render.jpg`

### NVIDIA Meeting Cheat Sheet Updates (adc3k.com/nvidia-meeting)
- Added Q7: 50 racks / 10 MW / H2 2026 allocation question
- Added Q8: Ornn capital card — committed buyer, not just a prospect
- Added new tab: **10 MW PLAN** — full CapEx, revenue, tax stack, OCP standard reference, one-liner for Jack

### Next Actions
1. **NVIDIA call** — Mike Pulice + Antonio Rivera. Use adc3k.com/nvidia-meeting. Key new questions: rack allocation minimum for DGX-Ready, H2 2026 feasibility at 50 racks.
2. **After call** — Rewrite phase plan with 10 MW as Phase 1. Update investor package.
3. **Jack / Ornn outreach** — After NVIDIA call confirms allocation path. One-liner ready: "50 racks, 10 MW, $55-60M raise, $32M EBITDA Year 2."
4. **ATMOS call** — Confirm existing gas service size + pressure at Trappeys meter. Sets genset sizing ceiling.
5. **LUS pre-development** — (337) 291-8426. Confirm Pin Hook transformer rating for emergency backstop + sell-back interconnection.
6. **Electrical PE** — N+1 SST module design, DC protection coordination study per OCP standard.

---

## SESSION SUMMARY — March 31, 2026 (SESSION 1)

### NVIDIA Meeting Cheat Sheet — LIVE at adc3k.com/nvidia-meeting

Built full meeting cheat sheet for call with Mike Pulice (NVIDIA AEC Account Exec) and Antonio Rivera (NVIDIA Account Manager, ex-Run:ai Head of BD West).

**8 tabs:** WHO THEY ARE / ADC POSITION / OPENING SCRIPT / POWER STACK / QUESTIONS / LOGISTICS / HUMIDITY / SITE VISIT / CLOSE / 10 MW PLAN

**Key decisions locked this session:**
- Power vendor language = vendor-neutral. Ask NVIDIA who they see working in DSX deployments. Never name-drop Eaton as locked.
- NCP exam: Scott sat for it at GTC, did NOT pass. All references updated. Never say passed.
- Humidity/dehumidification: Munters desiccant top pick. Waste heat from racks regenerates desiccant wheel. Solar powers dehumidifiers during peak humidity hours. Run:ai controls full factory environment — not just GPU scheduling.
- Logistics: I-10/I-49 + barge + rail. 28K sq ft concrete pad + receiving warehouse. Diesel bridge power. Texas supply chain = one drive. MARLIE I and Trappeys dug simultaneously.
- 800V DC MVSST topology confirmed: genset AC → MVSST → 800V DC bus ← solar strings ← battery. Rack PDU steps 800V → 48V (16:1, OCP ORV3 internal).

**New memory files:**
- `memory/projects/nvidia_meeting_prep.md`
- `memory/projects/trappeys_humidity_cooling.md`
- `memory/projects/trappeys_logistics.md`
- `memory/projects/ocp_lvdc_standard.md`

---

## SESSION SUMMARY — March 29, 2026 (DAY 3 — SHELVED)

### DSX Blueprint — ABANDONED after 3 days, WSL unfixable

**Root cause:** WSL Ubuntu on Windows crashes every time under the I/O load of the DSX packman build. Not fixable on Windows with WSL.

**DO NOT attempt WSL-based DSX build again. Ever.**

**To resume DSX (only two valid options):**

Option A — Docker Desktop (16GB RAM in settings):
```
.\scripts\build-dsx-docker.ps1
```

Option B — Native Linux (RunPod CPU pod $0.03/hr):
```
git clone ... && ./repo.sh build && ./repo.sh package --container && docker push
```

Option C — Skip the build entirely, use NVIDIA's hosted version:
```
https://build.nvidia.com/nvidia/omniverse-dsx-blueprint-for-ai-factories
```

**DSX is NOT the priority. Come back to it when there's time and patience.**

---

## ROXY STATUS — LIVE
- **Pod:** g5t4hxa9rjm7cm (RTX A6000, 48GB VRAM, 58GB RAM)
- **Model:** Qwen 3 8B fine-tuned v1 (118 examples), baked into weights
- **VRAM:** 90% used — DO NOT train on this pod
- **Cost:** $0.33/hr
- **27 tools**, smart tool selector, session persistence, job manager
- **DO NOT TOUCH THIS POD**

## Action Items — Priority Order

1. **NVIDIA call** — Tomorrow. adc3k.com/nvidia-meeting.
2. **10 MW plan** — Update investor package after NVIDIA call confirms allocation path.
3. **Jack / Ornn outreach** — Post-NVIDIA call. 50 racks, $55-60M raise.
4. **ATMOS** — Confirm gas service size at Trappeys meter.
5. **LUS pre-development** — (337) 291-8426 — Pin Hook capacity.
6. **Electrical PE** — N+1 SST design, OCP coordination study.
7. **Twilio 10DLC approval** — Submitted, waiting on carrier.
8. **Stripe live mode** — Swap sk_test_ to sk_live_ when ready.
9. **ROXY v2 training** — Separate pod. 334 examples ready.
10. **Episode 3 production** — briefing ready.

---

## Phone Numbers (LOCKED)
- ADC business: (337) 780-1535 (AT&T, Scott's line)
- Louisiana AI Initiative: (337) 448-4242 (Bland.ai bot)
- AI Advantage: (337) 486-3149 (Bland.ai bot)
- NEVER cross these numbers between sites

---

## Dual Power Stack (LOCKED)
- Eaton Beam Rubin DSX = FACILITY power (800V bus, ORV3 sidecar)
- Delta Electronics = RACK power (660 kW rack, e-Fuse, 90 kW DC/DC, 140 kW CDU)
- Both on EVERY drawing, EVERY page, EVERY spec

---

## Raise
- **REVISED: ~$55-60M** (up from $5M seed — Ornn partnership changes capital structure)
- MARLIE I owned (collateral)
- Trappeys ~$1M acquisition
- 80% equipment financing via Ornn RVS on $180M rack CapEx
- Master doc: business-model/MASTER-INVESTOR-PACKAGE.md (needs update to 10 MW numbers)
