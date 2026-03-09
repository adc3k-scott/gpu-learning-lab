# Mission Control — Project State
Last updated: 2026-03-09 (post-pipeline-scout + presentation suite session)

---

## What Was Done This Session

### Presentation & Intelligence Suite (5 web tools built)
- `web/infrastructure-layers.html` — 4-layer interactive stack (Power→Compute→Edge→Airspace). Audience tabs: Investor / City / FAA / UL Lafayette. Nodes clickable with GPS + next action.
- `web/adc3k-site.html` — Full ADC3K.com marketing site. Hero → MARLIE I → Pod → Network → Tech Stack → Vision → Contact. 6 sites, status badges.
- `web/klft-deck.html` — 9-slide KLFT airport meeting deck. Arrow-key nav. Covers: Opportunity → Facility → Tech → First Responders → MARLIE I → Ask (3 items) → Timeline → Close.
- `web/site-intel.html` — Pipeline Site Intelligence Map. Leaflet + 5 Louisiana pipeline corridor overlays. Add/score/filter sites. FEMA auto-check. Tier A-D. Export CSV/JSON.
- `web/network-map.html` — Louisiana AI network map, 7 GPS-locked nodes (exists from prior session).

### Pipeline Site Scout System (agent-based data collection)
- `scripts/pipeline_scout.py` — Claude tool_use agent runner. 5 corridors: Henry Hub, Tennessee Gas, Southern Natural, Teche, Sabine.
- `agents/site_scout/fema.py` — FEMA NFHL flood zone API. Endpoint: `hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer/28/query`.
- `agents/site_scout/scorer.py` — Scoring engine (matches site-intel.html JS exactly). 6 criteria, weighted 0-100, Tier A-D.
- `data/pipeline_sites.json` — 16 real listings found (4 corridors complete). 4 Tier A sites identified.
- `data/pipeline_sites_import.js` — Paste in browser console → imports all 16 sites to map.

### Memory & State
- `memory/MEMORY.md` — updated with full session state, pipeline scout system, top sites table
- `memory/projects/trappeys.md` — updated: UL Lafayette added as PRIMARY STAKEHOLDER (critical unlock)

---

## Project Status Board

| Project | Status | Next Action |
|---------|--------|-------------|
| **MARLIE I** | Engineering complete. Investor conversations active. | Scott: sign LOI/lease on paper. LUS power capacity confirmation. LED Act 730 pre-app meeting. |
| **ADC 3K** | 12 open investor items. Presentation assets built. | Fix financial model (tax rate 5.5%, CapEx recon, 3-scenario). Add deck slides (competitive, exit, team). |
| **Trappeys** | Strategy defined. UL Lafayette = critical unlock. | First contact: UL president/provost/research computing director. City participation required. |
| **KLFT 1.1** | Full engineering package + airport meeting deck ready. | Schedule Airport Authority meeting. Get building sq footage + condition report first. |
| **Pipeline Sites** | 16 sites scored. 4 Tier A. Map operational. | Run Sabine corridor (needs API credits). Import sites.json to map via console. |
| **Mission Control HD** | Live. Two deferred blockers. | Stripe live webhook + Supabase auth redirect URLs. |
| **Ground Zero** | EP001 private. EP002 pending. | Set PEXELS_API_KEY → run EP002 pipeline. |
| **Site Acquisition** | Coteau LA = Priority 1. | Get Coteau site plan from owner. Confirm FEMA/power/gas/acreage. |
| **Mission Control (repo)** | 160 tests green. All 10 agents operational. | No blockers. Pen testing environment not yet built. |

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
- **Sabine corridor scout** — `python scripts/pipeline_scout.py --corridors "Sabine" --max-sites 4` (needs API credits)
- **Import sites to map** — open site-intel.html → F12 Console → paste `data/pipeline_sites_import.js`
- **KLFT Airport Authority** — schedule meeting; get building sq footage + condition report first
- **UL Lafayette first contact** — president / provost / research computing director (Trappeys unlock)

### ADC 3K Investor-Critical
1. Customer LOI — zero signed anchor tenants
2. NVIDIA Vera Rubin NVL72 TDP — unpublished; contact NVIDIA Enterprise Sales
3. HB 827 → replace with parish-level PILOT agreement
4. CapEx reconciliation — $33.2M stated vs analyst estimate ~$110M
5. Financial model: fix 5.5% tax rate, 3-scenario model, unit economics per pod
6. Deck slides: competitive landscape, exit strategy, management team

### MARLIE I
- LOI or lease — must have paper before investor conversations advance
- LUS utility capacity confirmation — contact LUS for 1201 SE Evangeline power availability
- LED Act 730 pre-application meeting — schedule before investor close

### Ground Zero
- PEXELS_API_KEY not set (B-roll fallback to noise)
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
- `get_blocks()` not `get_block_children()` — check method signatures before scripting
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
- `web/` — all 5 presentation/intelligence HTML tools
- `marlie/` — MARLIE I investor deck HTML + PDF
- `aido/` — Ground Zero video pipeline
- `pyproject.toml` — source of truth for deps

---

## Next Session — Starting Points
1. **Sabine corridor** — run scout when API credits restored. Calcasieu/Beauregard/Vernon parishes. ~4 more sites expected.
2. **Import pipeline sites** — paste `data/pipeline_sites_import.js` in site-intel.html console → all 16 sites load onto map.
3. **Coteau LA** — if site plan received, analyze and build full site concept.
4. **KLFT meeting prep** — schedule Airport Authority meeting. Building condition report.
5. **Pen testing environment** — authorized scope: own systems, firewall rules, posture report.
