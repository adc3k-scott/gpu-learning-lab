# Mission Control — Project State
Last updated: 2026-03-19 (GTC 2026 Press Release Sprint + Lafayette City Pitch)

---

## What Was Done This Session (2026-03-19)

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
- hub.html: Lafayette AI Initiative tile added (top position)
- vercel.json: /investor and /lafayette rewrites added
- Decks moved to decks-private/ (not deployed)

### Git
- Commit pending (this close-out)

---

## Project Status Board

| Project | Status | Next Action |
|---------|--------|-------------|
| **Willow Glen** | Deck live. DSX reference. Neocloud pitch. Investor page live. | CBRE/Bryce French. NVIDIA Inception. WGT partnership. ITEP. |
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
| **Neocloud Strategy** | Complete. Investor page live. Lafayette pitch live. | Submit NVIDIA Inception. Target DGX-Ready. |

---

## Open Blockers (Require Scott Action)

### Immediate — Time Sensitive
- **ITEP filing** — must file BEFORE groundbreaking. Most critical single item.
- **NVIDIA Inception** — application package ready, submit now
- **UL Lafayette contact** — president, provost, or research computing director. Single biggest domino.

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
2. NVIDIA Vera Rubin NVL72 TDP — unpublished
3. Financial model: token factory economics, fix 5.5% tax rate
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
1. **ITEP filing prep** — what's needed, timeline, forms
2. **UL Lafayette approach** — who to contact, what to say, how to frame
3. **NVIDIA Inception submission** — final review and submit
4. **Financial model update** — token factory economics (Dynamo 7x, Groq 35x)
5. **Manufacturing re-scope** — factory station layout for DSX facility modules
6. **Deep-dive education images** — replace remaining immersion images on site
