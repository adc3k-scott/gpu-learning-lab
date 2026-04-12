# gpu-learning-lab — Mission Control

## Project Purpose
Multi-agent AI platform for CUDA/GPU computing and RunPod management. FastAPI backend + SSE dashboard.
Owner: **Scott Tomsu** — ADC3K, MARLIE 1 project lead, 1201 SE Evangeline Thruway, Lafayette LA.

## Project Knowledge Files
- `memory/projects/marlie_i.md` — MARLIE 1 AI Factory: site, hardware, financials, incentives
- `memory/projects/adc3k.md` — ADC 3K pod product: specs, open investor items, action list
- `memory/projects/trappeys.md` — Trappeys Cannery: first ADC 3K deployment site
- `memory/projects/ground_zero.md` — Ground Zero YouTube: pipeline status, episode format, blockers
- `memory/projects/klft.md` — KLFT 1.1: Gulf Coast Emergency Drone Deployment Hub, SkyCommand, AIKCC
- `memory/projects/missioncontrolhd.md` — Mission Control HD: vehicle diagnostics SaaS, missioncontrolhd.com
- `memory/projects/nsf_fuel_louisiana.md` — **NSF FUEL (Future Use of Energy in Louisiana)**: $160M NSF Engines grant (largest ever), $45M renewal March 2026, LSU-led, 53+ partners, POC fund, energy innovation. Key contacts: Girard Melancon (partnerships, girardmelancon@lsu.edu), Stephen Loy (commercialization), Michael Mazzola (exec director). ADC fit: 800V DC solar-direct, waste heat, digital twins, workforce.

## ADC Infrastructure — Core Architecture
- **MARLIE 1** = permanent AI Factory, 1201 SE Evangeline Thruway. GPS: 30.21975N, 92.00645W (corner 16th St). CDU cold plate cooling. NVL72 racks. HQ + NOC.
- **Autonomous AI Cassette** = manufactured containerized cassette. No HVAC. Deployed remotely, managed from MARLIE 1.
- **KLFT 1.1** = Gulf Coast Emergency Drone Hub. Lafayette Regional Airport. GPS: 30.21256N, 91.99069W. Skydio X10 + Dock + SkyCommand.
- **Trappeys Cannery** = first planned ADC 3K pod site. GPS: 30.21356N, 92.00163W. Metal warehouse, Vermilion River frontage. SEPARATE site from MARLIE 1.
- **New Iberia Solar Factory** = renewable energy partner. GPS: 30.03768N, 91.87524W. Site 2 ADC candidate.
- **ADC 3K geography**: cassettes follow Louisiana natural gas pipeline map — Henry Hub corridor, Gulf Coast industrial belt.
- NEVER conflate MARLIE 1 (CDU, permanent building) with ADC 3K (immersion, field pod). Different products.

## Site Acquisition Pipeline (GPS verified 2026-03-09)
Notion root: `31e88f09-7e31-8136-9d4f-dbc128f55757`
- **Coteau LA** `31e88f09-7e31-8186` — GPS: 30.04182N, 91.95573W. PRIORITY 1. Sugar cane field, south of Lafayette. Full AI Factory candidate. Get: acreage, FEMA zone, 3-phase, gas proximity, owner terms.
- **Airport Frontage** `31e88f09-7e31-81fb` — GPS: 30.20146N, 91.99873W. Former Alpha office, Hwy 90. CDU rack + KLFT integration.
- **Pinhook Urban** `31e88f09-7e31-81d2` — GPS: 30.21749N, 92.00325W. 1421 SE Evangeline Thruway. ADC 3K pods + EV charging.
- **Site Eval Framework** `31e88f09-7e31-8128` — Type A/B/C/D + 7-factor scoring. Score 28+ = Priority 1.
- EV charging standard: every site, DC fast charge + Level 2, utility substation aesthetic.

## Network Visualization Map
`web/network-map.html` — interactive Louisiana AI Infrastructure map. All 7 nodes GPS-locked. Public/Technical view toggle. Community services + energy layers. Opens as standalone HTML.

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
- `marlie/` — MARLIE 1 investor deck HTML + PDF
- `aido/` — Ground Zero video pipeline
- `pyproject.toml` — source of truth for deps

## Notion Integration
- Key: `.env` or `.venv/.env` as `NOTION_API_KEY`
- **"Show me Notion files"** = run `python scripts/notion_tree.py` — permanent script, pre-approved, always works.
- Edits: write temp Python script → run → delete in ONE bash call: `python _script.py 2>&1 && rm _script.py`
- **Chain git operations:** `git add FILE && git commit -m "..."` — one approval not two
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
  [PAGE] MARLIE 1  (31e88f09-8121) — 9 sub-pages
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
