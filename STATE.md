# Mission Control — Project State
Last updated: 2026-03-09 (post-power architecture + vendor outreach session)

---

## What Was Done This Session

### Power Architecture Document (new)
- `web/power-architecture.html` — 5-tab interactive power doc:
  - Tab 1: MARLIE I (2MW) — 4-layer resilience banner, SVG power flow, stack bars, layer table, "Why This Stack" card
  - Tab 2: ADC 3K Pod Site (750kW) — CORRECTED to nat gas PRIMARY → diesel hurricane backup → solar/battery → grid last resort. 4-layer banner matches MARLIE I.
  - Tab 3: Generator Comparison — CAT/Cummins/Waukesha/Generac/MTU full table, prime vs standby explainer, fast-lead strategy
  - Tab 4: Solar + Battery — Louisiana solar data, 300kW sizing, battery 3-job explainer, vendor options
  - Tab 5: ATS Switching — normal ops, grid failure event timeline, vendor questions checklist
- **CRITICAL ARCHITECTURE CONFIRMED**: Nat gas = Layer 1 PRIMARY on ALL sites (MARLIE I and pod sites). LUS grid = Layer 4 LAST RESORT ONLY. Diesel = Layer 2 hurricane backup (Ida proof). Solar/battery = Layer 3 offset.

### Vendor Outreach Command Center (new)
- `web/vendor-outreach.html` — full outreach tracker:
  - Lead time risk dashboard (18-24mo critical → weeks low, color-coded)
  - 8-step engagement sequence ordered by risk
  - Fast-lead alternatives: Aggreko rental (days), USP&E/LEL used (2-8 wks), Schneider Quick Ship (<8 wks) vs 18-24mo custom
  - 7 vendor cards: NVIDIA, Switchgear/MV Transformer, Nat Gas Gensets, Bloom Energy, CDU Cooling, Starline T5, LUS, Starlink, LED Act 730
  - Each card: what we need, position, contact path, copy-ready email template with clipboard button, contacted checkbox
  - Key spec note locked in: "60 Hz, 480V, nat gas, 1,000–1,500 kW, PRIME-RATED, Louisiana delivery"

### MARLIE I Phase 1 Deck Update
- `web/marlie-phase1.html` — added facility photo + SVG site plan side-by-side:
  - `marlie/Store_Front_Pic.jpg` — downloaded from Notion MARLIE I image block (not from local filesystem — it was in Notion)
  - SVG site plan: 3 parcels, Phase 1 compute floor (22×35 ft), dry cooler pad, genset pad, utility entries (LUS 3-phase green, nat gas amber, fiber purple)

### ADC3K.com Vercel Scaffold (parked)
- `adc3k-deploy/index.html` + `adc3k-deploy/vercel.json` — deployment scaffold ready
- Auth parked — wrong Vercel account. Need correct account to run `cd adc3k-deploy && npx vercel --prod`

---

## Project Status Board

| Project | Status | Next Action |
|---------|--------|-------------|
| **MARLIE I** | Engineering complete. Presentation assets built. Investor conversations active. | Sign LOI/lease. LUS power capacity confirmation (337-291-5577). LED Act 730 pre-app. |
| **ADC 3K** | 12 open investor items. Power architecture confirmed. Vendor outreach tracker live. | Fix financial model (5.5% tax, CapEx recon, 3-scenario). Add deck slides (competitive, exit, team). |
| **Trappeys** | Strategy defined. UL Lafayette = critical unlock. | First contact: UL president/provost/research computing director. City participation required. |
| **KLFT 1.1** | Full engineering package + airport meeting deck ready. | Schedule Airport Authority meeting. Get building sq footage + condition report first. |
| **Pipeline Sites** | 16 sites scored. 4 Tier A. Map operational. | Run Sabine corridor (needs API credits). Import sites.json to map via console. |
| **ADC3K.com** | Vercel scaffold built. Auth parked. | Find correct Vercel account → `cd adc3k-deploy && npx vercel --prod` |
| **Mission Control HD** | Live. Two deferred blockers. | Stripe live webhook + Supabase auth redirect URLs. |
| **Ground Zero** | EP001 private. EP002 pending. | PEXELS_API_KEY confirmed in .env — run EP002 now. |
| **Mission Control (repo)** | 160 tests green. All 10 agents operational. | No blockers. |

---

## 4-Layer Power Stack — Confirmed Architecture (ALL ADC SITES)
```
Layer 1 — Nat Gas Gensets     PRIMARY · prime-rated · 24/7 · Henry Hub pricing
Layer 2 — Diesel Gensets      HURRICANE BACKUP · on-site fuel · pipeline-independent (Ida proof)
Layer 3 — Solar + Battery     SUPPLEMENT · daytime offset · instant ATS bridge
Layer 4 — LUS / Grid          LAST RESORT · never primary · rate exposure avoided
```
MARLIE I: 2MW total. Two 1,500 kW nat gas (N+1). One 1,500 kW diesel. 300kW solar + 600kWh battery.
Pod sites: 750kW total. Two 750kW nat gas (N+1). One 750kW diesel. 200kW solar + 400kWh battery.

---

## Pipeline Scout — Top Sites (2026-03-09)
| Score | Tier | Site | Parish | Note |
|-------|------|------|--------|------|
| 83 | A | Common St & Arabie Rd, Lake Charles | Calcasieu | ON pipeline |
| 81 | A | Kinder Industrial (Hwy 165) | Allen | Zone X confirmed |
| 81 | A | Hwy 165/I-10, Iowa | Jefferson Davis | 27.75 acres |
| 80 | A | New Iberia (Hwy 90 & Hwy 14) | Iberia | Gas line ON property |
| 74 | B | Smede Hwy, Broussard | St. Martin | 46 acres, Zone X |
| 72 | B | Hwy 90 Energy Corridor, Gray | Terrebonne | 108 acres, Zone X |
ELIMINATE: Hulin Road, Erath — FEMA Zone VE (coastal, high risk).
Sabine corridor (Calcasieu/Beauregard/Vernon) — NOT YET RUN. Run when API credits restored.

---

## Open Blockers (Require Scott Action)

### Immediate
- **Sabine corridor scout** — `python scripts/pipeline_scout.py --corridors "Sabine" --max-sites 4` (needs Anthropic API credits)
- **Import sites to map** — open site-intel.html → F12 Console → paste `data/pipeline_sites_import.js`
- **ADC3K.com deploy** — find correct Vercel account → `cd adc3k-deploy && npx vercel --prod`
- **Building photo cleanup** — upload `marlie/Store_Front_Pic.jpg` to cleanup.pictures → remove Dynojet banners + Dino mascot + tire pile → save back
- **KLFT Airport Authority** — schedule meeting; get building sq footage + condition report first
- **UL Lafayette first contact** — president / provost / research computing director (Trappeys unlock)

### ADC 3K Investor-Critical
1. Customer LOI — zero signed anchor tenants (fatal for institutional raise)
2. NVIDIA Vera Rubin NVL72 TDP — unpublished; contact NVIDIA Enterprise Sales
3. HB 827 → replace with parish-level PILOT agreement; brief investors honestly
4. CapEx reconciliation — $33.2M stated vs analyst estimate ~$110M
5. Financial model: fix 5.5% tax rate, 3-scenario model (bear/base/bull), unit economics per pod
6. Deck slides: competitive landscape (vs CoreWeave/Lambda/Crusoe/Lancium), exit strategy, management team

### MARLIE I
- LOI or lease — must have paper before investor conversations advance
- LUS utility capacity confirmation — (337) 291-5577 — ask for 1201 SE Evangeline power availability
- LED Act 730 pre-application meeting — schedule before investor close

### Ground Zero
- EP002 is ready to run — `python -m aido.pipeline --episode EP002 --local-render` — PEXELS_API_KEY confirmed
- Social accounts: TikTok, Instagram, X/Twitter, LinkedIn as @GroundZeroAI
- groundzeroai.com domain — verify ownership

### Mission Control HD (Deferred)
1. Stripe live webhook — Stripe dashboard (live mode) → endpoint at missioncontrolhd.com/api/stripe/webhook → copy whsec_ → update STRIPE_WEBHOOK_SECRET in Vercel → redeploy
2. Supabase auth redirect URLs — Authentication → URL Configuration → set Site URL + add missioncontrolhd.com/**

---

## Confirmed GPS Coordinates (verified by Scott 2026-03-09)
```
MARLIE I:         30.21975 N, 92.00645 W  — 1201 SE Evangeline Thruway (corner 16th St)
Trappeys:         30.21356 N, 92.00163 W  — SE Evangeline Thruway corridor
KLFT Hub:         30.21256 N, 91.99069 W  — Lafayette Regional Airport
Airport Frontage: 30.20146 N, 91.99873 W  — Hwy 90 frontage
Pinhook Urban:    30.21749 N, 92.00325 W  — 1421 SE Evangeline Thruway
Coteau LA:        30.04182 N, 91.95573 W  — Priority 1 site, south of Lafayette
NI Solar:         30.03768 N, 91.87524 W  — New Iberia Solar Factory
```

## Key Notion IDs (confirmed)
```
Mission Control HQ:        31288f09-7e31-81a5-bf43-e2af16379346
MARLIE I root:             31e88f09-7e31-8121-b4d2-d96b0084cc50
Trappeys AI Center:        31288f09-7e31-80a2-8712-ef09878afd53
ADC 3K Command Center:     31488f09-7e31-816d-9fdc-c6aabba4e3fa
KLFT 1.1:                  31d88f09-7e31-80ec-b055-f69b9108355e
AI Daily Omniverse:        31988f09-7e31-81a5-b33c-f57653d42863
Mission Control HD CC:     31e88f09-7e31-8182-900a-cac36f525edc
Ground Zero CC:            31e88f09-7e31-81f9-b372-fbfb99c995ed
Site Acquisition Pipeline: 31e88f09-7e31-8136-9d4f-dbc128f55757
  Coteau LA:               31e88f09-7e31-8186-b2f2-eee7d2ef394c
  Airport Frontage:        31e88f09-7e31-81fb-825a-f733cc0a93ae
  Pinhook Hotel Base:      31e88f09-7e31-81d2-bbde-f1400136190a
  Site Eval Framework:     31e88f09-7e31-8128-864e-d8f088c423a9
```

---

## Notion API Patterns (confirmed working)
- All edits: write temp Python script → run → delete in ONE bash call: `python _script.py 2>&1 && rm _script.py`
- Full tree: `python scripts/notion_tree.py` → paste full output inline in chat response. Never browser. Never summary.
- Chain git: `git add FILE && git commit -m "..."` — one approval, not two
- Page move to workspace root: NOT POSSIBLE via API — UI only
- Always verify page ID after creation: output can truncate IDs → 404s
- IDs in session summaries can be truncated — search Notion to confirm before scripting

---

## Key Files
- `main.py` — FastAPI app, 10 agents, SSE, streaming chat
- `skills/builtin/notion_util.py` — Notion client. `python notion_util.py` prints full tree.
- `skills/builtin/marlie_notion.py` — all project Notion IDs + ADC 3K specs
- `scripts/notion_tree.py` — zero-friction tree print (pre-approved in settings.json)
- `scripts/pipeline_scout.py` — Claude agent pipeline site finder
- `agents/site_scout/` — fema.py + scorer.py (pipeline site enrichment)
- `data/pipeline_sites.json` — 16 scored listings
- `web/` — all presentation/intelligence HTML tools (marlie-phase1, adc3k-site, power-architecture, vendor-outreach, klft-deck, site-intel, network-map, infrastructure-layers)
- `marlie/` — MARLIE I investor deck HTML + PDF + Store_Front_Pic.jpg
- `adc3k-deploy/` — Vercel deployment scaffold (index.html + vercel.json)
- `aido/` — Ground Zero video pipeline
- `pyproject.toml` — source of truth for deps

---

## Next Session — Starting Points
1. **ADC3K.com deploy** — find correct Vercel account, run `cd adc3k-deploy && npx vercel --prod`
2. **Building photo cleanup** — cleanup.pictures for Store_Front_Pic.jpg (remove signage/Dino)
3. **Sabine corridor scout** — run when API credits restored
4. **Import pipeline sites** — paste pipeline_sites_import.js in site-intel.html console
5. **Vendor outreach** — open vendor-outreach.html, work down the 8-step sequence, mark vendors contacted
