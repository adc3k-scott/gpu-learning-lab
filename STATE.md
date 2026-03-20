# Mission Control — Project State
Last updated: 2026-03-20 (DSX Architecture + Financial Scenarios)

---

## What Was Done This Session (2026-03-20)

### DSX Architecture Deep-Dive
- Researched NVIDIA DSX reference architecture from GTC video
- Created `memory/projects/dsx_architecture.md` — three pillars (Flex/Boost/Exchange), 800 VDC power, 5-phase deployment pipeline, partner ecosystem mapping
- Updated `memory/projects/willow_glen.md` — added DSX pillars, 800 VDC Day 1 requirement, software pipeline build sequence, updated next actions
- Updated `memory/projects/nvidia_strategy.md` — cross-referenced DSX deep-dive
- Key findings: DSX Boost gives 30% more throughput in same power envelope (critical for Phase 1's 3 MW constraint), 800 VDC cannot be retrofitted (Day 1 decision), 200+ certified partners for non-GPU infrastructure

### Financial Scenarios (Bear / Base / Bull)
- Built `business-model/scenarios.md` — complete 3-scenario financial model
- Phase 1A (3 MW): Bear -$3.4M EBITDA, Base +$3.8M, Bull +$14.1M
- Phase 1C (12 MW): Base turns cash-positive at $38.3M EBITDA (80% margin)
- Phase 2 (50 MW): Base $169.5M EBITDA — 1.8x Hut 8's NOI/MW
- Phase 3 (100+ MW): Base $600M revenue, $500M EBITDA
- Used revenue-per-MW benchmarks (not raw token math — NVIDIA's 700M tokens/sec is a marketing peak)
- Token deflation sensitivity, Louisiana tax incentive stack, valuation comps, risk matrix
- Cumulative CapEx: $88-140M Phase 1, $748M-$1.14B full campus

### SMB AI Install Playbooks (Prior Session)
- Built 12 vertical playbooks in `smb-ai-playbooks/playbooks/`
- Separated from ADC neocloud business (different company, name TBD)
- 5 workflow patterns, 3 hardware tiers (Cloud / Starter Kit / DGX Spark)
- Revenue model: $48K/month recurring per installer by month 12

---

## Previous Session (2026-03-19 Evening)

### Business Model Folder — Complete Build
Created `business-model/` with 8 documents from parallel research:
- **token-economics.md** — Full market pricing (OpenAI, Anthropic, Google, Groq, Together, Fireworks). Raw cost floor ~$0.004/M tokens. ADC pricing tiers $0.20-$150/M. 95%+ margins.
- **power-economics.md** — 4-layer power stack economics. Phase 1 (3 MW): $0.058-0.068/kWh (recip engines). At scale (100+ MW): $0.04-0.05/kWh (CCGT). MISO ancillary ~$4M/yr.
- **itep-filing.md** — Full ITEP filing process. NAICS code is a risk (AI compute ≠ manufacturing). Must pre-qualify with LED (Kristin Johnson, 225-342-2083). $8-16M savings at stake. Act 730 also identified ($200M+, 20-year sales tax exemption).
- **iberville-permits.md** — Full permitting timeline. 5-6 months optimistic, 8-10 conservative. M2 zoning = no variance. Brownfield advantage (EO 14318). ITEP is critical path driver.
- **ul-lafayette-approach.md** — Approach strategy for UL Lafayette. New president Dr. Ramesh Kolluru (CS PhD, built R1 profile, appointed Feb 2026) is perfect target. LEDA for warm intro. No GPU infra at UL (CPU-only Firebird cluster). $160M NSF FUEL consortium is natural co-funding opportunity.
- **npn-registration.md** — 5-minute web form checklist. NPN → DGX-Ready → NCP certification ladder.
- **investor-gaps.md** — Updated with ITEP NAICS risk + power cost numbers
- **partner-stack.md** — Named partners by function
- **capex-model.md** — CapEx by phase
- **revenue-streams.md** — 6 revenue streams with unit economics

### Home Page — Seven Chips Fix
- Updated "Six Chips" to "Seven Chips" in 3 places on index.html
- Added full-width Groq 3 LPX card (500 MB SRAM, 640 TB/s, 35x tokens/watt)
- Deployed to adc3k.com

### Key Discoveries
1. **NAICS code is a real risk for ITEP** — must frame as "emerging industry" token manufacturing, not data center
2. **Phase 1 power costs are higher than initially estimated** — $0.058-0.068/kWh at 3 MW (no CCGT at that scale)
3. **UL Lafayette's new president is ideal** — CS PhD, built R1 research profile, just appointed
4. **Act 730** — separate 20-year sales tax exemption for $200M+ facilities (can stack with ITEP)
5. **Iberville Parish is M2 zoning** — no variance needed, brownfield status is an advantage

---

## Previous Session (2026-03-19 Earlier)

### Stack Page — Full GTC 2026 Press Release Integration
- **Dynamo 1.0**: Updated to "SHIPPING NOW", Jensen "inference is the engine of intelligence" quote, KVBM/NIXL/Grove modules, LangChain/vLLM/SGLang integrations, full adoption list (AWS, Azure, Google Cloud, CoreWeave, Crusoe, Cursor, Perplexity, PayPal, BlackRock)
- **Vera Rubin GPU**: "FULL PRODUCTION", 1/4 GPUs vs Blackwell for MoE training, 10x inference throughput/watt, Anthropic/Meta/Mistral/OpenAI building on it
- **NemoClaw/OpenClaw**: Jensen "OS for personal AI" quote, privacy router, runs on RTX PCs/DGX Spark/Station
- **Nemotron Coalition**: 8 AI labs (Mistral, Perplexity, Cursor, LangChain, BFL, Reflection, Sarvam, Thinking Machines Lab), Nemotron 4 codeveloped with Mistral
- **BlueField-4 STX**: DOCA Memos framework, KV cache POD-wide context, 5x inference throughput, Mistral CTO quote
- **DSX Reference**: DSX Max-Q (30% more infra in fixed power), DSX Flex (100 GW stranded grid), 200+ partners
- **Spectrum-6**: 5x optical power efficiency from PR
- **GTC headline**: Added Nemotron Coalition, Physical AI (Cosmos 3, GR00T N2 #1), Dario Amodei + Sam Altman quotes endorsing Vera Rubin
- **Vera CPU**: 2x efficiency, 50% faster than traditional CPUs

### Investor Page (NEW — investor.html)
- Jensen token budget quote, Dario Amodei quote, Sam Altman quote, Jensen Dynamo quote
- Full neocloud pitch: $1T demand, token factory, 5 revenue streams
- Willow Glen property overview, power architecture, deployment phases
- Market comp table (CoreWeave $71B, Nebius $24B, Crusoe $10B+)
- Hut 8 River Bend local comp, NVIDIA partnership path, founder section
- All 4 "REQUEST INFO" buttons on index.html changed to "INVESTOR OVERVIEW" linking to /investor

### Lafayette City Pitch (NEW — lafayette.html)
- **Unified presentation for City Council**: MARLIE I + Trappeys + KLFT + UL Lafayette + first responders
- Three facilities overview, economic numbers, first responder drone operations (hurricane, pipeline, SAR, DFR, AI-RAN)
- NVIDIA Smart City platform section (Metropolis, Omniverse, Jetson, Dynamo, NemoClaw, AI-RAN)
- KLFT as NVIDIA reference site (three-ecosystem convergence)
- UL Lafayette partnership (anchor tenant, grants, workforce, preservation, credibility)
- Jobs for Acadiana (75+, ROV workforce, student pipeline)
- Louisiana tax advantage (ITEP, HB 827, historic 45%, R&D, Quality Jobs, Enterprise Zone)
- What ADC brings + What ADC needs from Lafayette (6 specific asks)
- Timeline (Q2 2026 → 2027)

### Research Completed + Saved to Memory
- **NVIDIA Smart Cities / Ports / Airports**: airports grouped under "Ports". Metropolis at BLR, Toronto Pearson, Incheon, Heathrow. Searidge ATC vision AI. → `nvidia_smart_cities.md`
- **Small drone stations**: Skydio Dock 2x2 ft, no container needed. FlytBase AI-R, Easy Aerial EGV. → `small_drone_stations.md`
- **DSX Air + Omniverse Blueprint**: Two tools, cloud vs local. → `dsx_air_omniverse.md`
- **NVIDIA + Nokia 6G AI-RAN**: $1B investment, ARC-Pro, ISAC, KLFT fit. → `nvidia_nokia_6g.md`

### Site Updates
- hub.html: Lafayette AI Initiative tile added (top position), Factory Sim + NCA Study + Quiz tiles added, dead Blackwell vs Rubin tile removed
- vercel.json: /investor and /lafayette rewrites added, dead /compare rewrite removed
- Decks moved to decks-private/ (not deployed, added to .gitignore)

### File Structure Cleanup
- Removed 4 duplicate deck files from web/ (originals in decks-private/)
- Deleted factory/nvidia-inception-draft.md (Inception is for software startups, not ADC)
- Added decks-private/ to .gitignore
- All deployed pages now linked from hub

### Git
- `88e0d7a` — feat: GTC 2026 press releases, investor page, Lafayette city pitch
- `b76d5c5` — fix: replace NVIDIA Inception refs with Partner Network (NPN)
- `38ba441` — fix: clean up file structure — remove duplicate decks, dead routes, outdated Inception draft

---

## Project Status Board

| Project | Status | Next Action |
|---------|--------|-------------|
| **Willow Glen** | Deck live. DSX reference. Neocloud pitch. Investor page live. | CBRE/Bryce French. NPN registration. WGT partnership. ITEP. |
| **MARLIE I** | Engineering complete. Part of Lafayette city pitch. | City alignment via Lafayette AI Initiative. |
| **ADC 3K** | DSX-compliant facility modules. Neocloud nodes. | Customer LOI. Financial model (token economics). |
| **Trappeys** | Part of Lafayette city pitch. Historic tax credits angle. | UL Lafayette first contact (critical unlock). |
| **KLFT 1.1** | Smart city convergence documented. Drone stations spec'd. Part of city pitch. | Airport Authority meeting. First responder pilot. |
| **Lafayette AI Initiative** | **NEW** — City pitch page LIVE at adc3k.com/lafayette. | Schedule City Council meeting. UL introduction. LEDA engagement. |
| **ADC3K.com** | LIVE. Stack updated with 4 press releases. Investor + Lafayette pages live. | Deep-dive education images (cosmetic). |
| **Mission Control** | Auth middleware. 303 tests. Full observability. | Set MC_API_KEY for production. |
| **NCA-AIIO Cert** | PASSED 2026-03-13. | Done. |
| **NCP-AII Cert** | Did not pass. NVIDIA updating exam. | Retake when new version available. |
| **GTC 2026** | Attended. All press releases integrated into stack page. | Debrief complete. |
| **Neocloud Strategy** | Complete. Investor page live. Lafayette pitch live. | NPN registration. Target DGX-Ready certification. |

---

## Open Blockers (Require Scott Action)

### Immediate — Time Sensitive
- **ITEP filing** — must file BEFORE groundbreaking. **NAICS code risk identified** — call LED (Kristin Johnson, 225-342-2083) to pre-qualify "emerging industry" angle. See `business-model/itep-filing.md`.
- **NVIDIA Partner Network (NPN)** — register ADC as partner. 5-minute web form. See `business-model/npn-registration.md`.
- **UL Lafayette contact** — target Dr. Ramesh Kolluru (new president, CS PhD, appointed Feb 2026). Via LEDA for warm intro. See `business-model/ul-lafayette-approach.md`.
- **Solar partner meeting** — 2026-03-20. Get company name, specs, EPC pricing.

### Willow Glen
- **CBRE contact** — Bryce French, Senior VP — warehouse lease inquiry
- **WGT partnership proposal** — neocloud angle (NVIDIA NCP on their site)

### Lafayette
- **City Council** — schedule presentation. Page ready at adc3k.com/lafayette
- **KLFT Airport Authority** — drone operations agreement
- **First responder pilot** — pick one department (fire or police) for DFR proof of concept
- **LEDA / LCG** — economic development alignment

### ADC 3K Investor-Critical
1. Customer LOI — zero signed anchor tenants
2. NVIDIA Vera Rubin NVL72 TDP — unpublished (blocks per-rack revenue calc)
3. Financial model: token economics DONE, power economics DONE, scenarios DONE (`business-model/scenarios.md`)
4. Deck: add management team slide

---

## Key Files
- `adc3k-deploy/index.html` — adc3k.com SPA
- `adc3k-deploy/stack.html` — NVIDIA technology stack (fully updated GTC 2026)
- `adc3k-deploy/investor.html` — Investor overview (Dario/Sam/Jensen quotes)
- `adc3k-deploy/lafayette.html` — Lafayette AI Initiative city pitch
- `adc3k-deploy/hub.html` — Mission Control hub (all pages linked)
- `main.py` — FastAPI server with auth middleware
- `memory/projects/neocloud_strategy.md` — Full neocloud playbook

## Deployment
- Deploy site: `cd adc3k-deploy && npx vercel --prod --yes`
- Vercel: mission-control1 (adhscott@yahoo.com)
- Cloudflare: gofast@stfumotorcycles.com

## Next Session — Starting Points
1. **Solar partner debrief** — update power-economics.md with EPC pricing after 2026-03-20 meeting
2. **SMB dispatch dashboard** — ServiceNow-inspired installer management UI (discussed, not built)
3. **SMB playbook pricing** — set install fees + monthly subscription rates for all 12 verticals
4. **Manufacturing re-scope** — factory station layout for DSX facility modules
5. **Update investor page** — add power partner names (Eaton, Siemens) + solar partner + DSX architecture
6. **Deep-dive education images** — replace remaining immersion images on site
7. **Raise structure** — define amount, structure, use of proceeds (needs advisor/attorney input)
8. **DSX Air signup** — model Willow Glen topology (free trial at air.nvidia.com)
