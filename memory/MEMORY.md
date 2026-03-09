# gpu-learning-lab — Mission Control

## Project Purpose
Multi-agent AI platform for CUDA/GPU computing and RunPod management. FastAPI backend + SSE dashboard.
Owner: **Scott Tomsu** — ADC3K, MARLIE I project lead, 1201 SE Evangeline Thruway, Lafayette LA.

## Project Knowledge Files
- `memory/projects/marlie_i.md` — MARLIE I AI Factory: site, hardware, financials, incentives
- `memory/projects/adc3k.md` — ADC 3K pod product: specs, open investor items, action list
- `memory/projects/trappeys.md` — Trappeys Cannery: first ADC 3K deployment site
- `memory/projects/ground_zero.md` — Ground Zero YouTube: pipeline status, episode format, blockers
- `memory/projects/klft.md` — KLFT 1.1: Gulf Coast Emergency Drone Deployment Hub, SkyCommand, AIKCC
- `memory/projects/missioncontrolhd.md` — Mission Control HD: vehicle diagnostics SaaS, missioncontrolhd.com

## ADC Infrastructure — Core Architecture
- **MARLIE I** = permanent AI Factory, 1201 SE Evangeline Thruway. CDU cold plate cooling. NVL72 racks. HQ + NOC.
- **ADC 3K** = manufactured containerized pods. EC-110 full immersion. No HVAC. Deployed remotely, managed from MARLIE I.
- **KLFT 1.1** = Gulf Coast Emergency Drone Hub. First live ADC 3K node. Skydio X10 + Dock + SkyCommand pod.
- **Trappeys Cannery** = first planned ADC 3K pod site. Metal warehouse, Vermilion River frontage.
- **New Iberia Solar Factory** = renewable energy partner (~30 mi). Site 2 ADC candidate. Solar PPA path.
- **ADC 3K geography**: pods follow Louisiana natural gas pipeline map — Henry Hub corridor, Gulf Coast industrial belt.
- NEVER conflate MARLIE I (CDU, permanent building) with ADC 3K (immersion, field pod). Different products.

## Site Acquisition Pipeline (NEW — 2026-03-09)
Notion root: `31e88f09-7e31-8136-9d4f-dbc128f55757`
- **Coteau LA** `31e88f09-7e31-8186` — PRIORITY 1. Sugar cane field, clean slate, pipeline + solar proximity. Full AI Factory / Omniverse candidate. Owner meeting scheduled. Get: acreage, FEMA zone, 3-phase confirmation, gas proximity, owner terms.
- **Airport Frontage** `31e88f09-7e31-81fb` — Former Alpha office, Hwy 90, for sale. CDU rack facility. Airport AI + KLFT hub.
- **Pinhook & Hwy 90** `31e88f09-7e31-81d2` — Former hotel base. ADC 3K pods + EV charging. Urban core.
- **Site Eval Framework** `31e88f09-7e31-8128` — Type A/B/C/D + 7-factor scoring. Score 28+ = Priority 1.
- EV charging standard: every site, DC fast charge + Level 2, utility substation aesthetic.

## ADC 3K Investor Review — Open Items
12 items in `memory/projects/adc3k.md`. Key: Customer LOI (none), NVIDIA TDP (unpublished), CapEx ($33.2M vs ~$110M), tax rate (5.5% not 25%), unit economics per pod, competitive landscape, team slide, 3-scenario model.

## Ground Zero — YouTube (LIVE)
- Handle: @GroundZero-ai | EP001: private | EP002: in pipeline
- Blockers: PEXELS_API_KEY, social accounts (@GroundZeroAI), groundzeroai.com domain verify

## Mission Control HD — missioncontrolhd.com (LIVE)
- Stack: Next.js 15 + Supabase + Stripe (live) + Claude AI + Vercel. Repo: C:\Users\adhsc\mission-control
- Deferred: Stripe live webhook + Supabase auth redirect URLs. See `memory/projects/missioncontrolhd.md`.

## Key Files
- `main.py` — FastAPI app, 10 agents, SSE, streaming chat
- `skills/builtin/notion_util.py` — Notion client. `python notion_util.py` prints full tree.
- `skills/builtin/marlie_notion.py` — all project Notion IDs + ADC 3K specs
- `marlie/` — MARLIE I investor deck HTML + PDF
- `aido/` — Ground Zero video pipeline
- `pyproject.toml` — source of truth for deps

## Notion Integration
- Key: `.env` or `.venv/.env` as `NOTION_API_KEY`
- **"Show me Notion files"** = FULL paginated tree query always. Never partial.
- Edits: write temp Python script → run → delete. Use `notion_util.py`.
- **BASH EFFICIENCY — ALWAYS combine run + delete into ONE bash call:**
  `python _script.py 2>&1 && rm _script.py` — never two separate approvals for run then delete
- **BASH EFFICIENCY — chain git operations:** `git add FILE && git commit -m "..."` — one approval not two
- Workspace root moves: NOT POSSIBLE via API — UI only.
- Always verify page ID after creation: `nc.get_page(id)` — output can truncate IDs.
- IDs in session summaries can be truncated — search Notion to confirm before scripting.
- `get_blocks()` not `get_block_children()` — check method names before scripting.

## Notion Workspace (snapshot 2026-03-09 — run full tree for live state)
```
[ROOT] Mission Control HQ  (31288f09)
  [DB] Task Tracker | [DB] Dev Session Log
  [PAGE] Edge AI Infrastructure Documents (6 sub-pages)
  [PAGE] KLFT 1.1  (31d88f09) — 10 sub-pages
  [PAGE] MARLIE I  (31e88f09-8121) — 9 sub-pages
  [PAGE] Trappeys AI Center  (31288f09-80a2) — 3 sub-pages
  [PAGE] ADC 3K  (31488f09) — DB + 3 page suites
  [PAGE] Mission Control HD CC  (31e88f09-8182) — 5 sub-pages
  [PAGE] Ground Zero CC  (31e88f09-81f9) — 5 sub-pages
  [PAGE] Site Acquisition Pipeline  (31e88f09-8136) — 4 sub-pages

[ROOT] AI Daily Omniverse  (31988f09)
  [DB] Story Pipeline | [DB] Episode Archive
```

## Planner Patterns
read/list file→file_manager | pod ops→runpod | http→http_client
notion ops→notion | browser→browser | marlie/notion sync→marlie_notion | infra→infra_manager

## User Preferences
- Direct, no filler. No emojis. Apply changes immediately. Mission Control framing.
- HTML/web edits: `start "" "path\to\file.html"` immediately after edit.
- Document viewing: convert to HTML, open in browser — never native apps.
- "Show me Notion files": full paginated tree, printed indented. Never filtered/partial.
