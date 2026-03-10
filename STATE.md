# Mission Control — Project State
Last updated: 2026-03-10 (Willow Glen AI Factory + Mini Grid session)

---

## What Was Done This Session

### Willow Glen Terminal — AI Factory + Mini Grid (NEW)
- Built complete 14-slide engineering blueprint deck (willow-glen-deck.html)
- SVG engineering diagrams: warehouse floor plan, river cooling system, power mini grid, drone coverage, campus buildout
- Aerial helicopter photo from Notion (wgt-aerial.jpg) on cover slide
- Hut 8 River Bend comparison slide ($10B market validation)
- Skydio X10 drone security + infrastructure inspection slide
- NVIDIA pitch slide (what we bring / what we need / why they care)
- Power architecture rewritten as "Mini Grid" — renewable-first, grid export revenue
- Execution sequence removed from closing slide (not public)
- Added as FIRST project on adc3k.com Projects page (blue accent, Tier A badge)
- Wired into SPA: pages array, deckPages array, CSS, iframe deck page
- Deployed live to adc3k.com

### River + Pipeline Site Scout (NEW)
- Built `scripts/river_scout.py` — 3-corridor agent (Atchafalaya, Mississippi, Bayou Teche)
- 15 sites found: 4 Tier A, 11 Tier B
- Top site: Willow Glen Terminal — Score 94, Tier A
- Output: data/river_sites.json, data/river_sites.csv, data/river_sites_import.js

### Willow Glen Terminal Deep Dive
- Former Entergy power station: 2,200 MW, built 1960, decommissioned 2016
- Acquired by Zydeco Equity Holdings / Willow Glen Ventures, August 2020
- Genover did demolition: 30,000+ tons steel recycled, 1M+ lbs copper
- 700 acres, 400+ developable, M2 Heavy Industrial, Zone X
- On-site 230kV + 138kV Entergy substation (live)
- 3,500 ft Mississippi River frontage, 43-ft deepwater dock
- 2.33M barrel tank farm, CN Railway, pipeline corridor
- 20,000 SF warehouse available for lease
- Currently operated as bulk liquids terminal (renewable diesel feedstock)
- CBRE listing: Bryce French, Senior VP — "Price Upon Request"
- Hut 8 River Bend campus 45 min north: $10B Phase 1, 245 MW, $7B Fluidstack lease (Google backstop)

---

## Project Status Board

| Project | Status | Next Action |
|---------|--------|-------------|
| **Willow Glen** | 14-slide deck live at adc3k.com. Score 94 Tier A. | Contact CBRE/Bryce French. NVIDIA Inception. WGT partnership proposal. |
| **MARLIE I** | Engineering complete. Investor deck live. | Sign LOI/lease. LUS power capacity. LED Act 730 pre-app. |
| **ADC 3K** | 12 open investor items. Financial model needs fix. | Fix 5.5% tax rate, CapEx recon, 3-scenario model. |
| **Trappeys** | Deck built (18 slides). Live at adc3k.com. | UL Lafayette first contact. |
| **KLFT 1.1** | Skydio deck live at adc3k.com. | Schedule Airport Authority meeting. |
| **ADC3K.com** | LIVE. 5 project decks. Willow Glen first. | Formspree ID (replace YOUR_FORM_ID). |
| **Pipeline Sites** | 16 pipeline sites + 15 river sites scored. | Sabine corridor pending. Second river pass with updated keywords. |
| **Mission Control HD** | Live. Two deferred blockers. | Stripe webhook + Supabase auth redirect. |
| **Ground Zero** | EP001 private. EP002 pending. | PEXELS_API_KEY + run EP002. |

---

## adc3k.com — Deck Architecture

| Deck | File | Entry Point |
|------|------|-------------|
| Willow Glen | `willow-glen-deck.html` | FIRST project card → VIEW FULL DECK |
| MARLIE I | `marlie-deck.html` | MARLIE I project card → VIEW FULL DECK |
| Skydio / KLFT | `skydio-deck.html` | KLFT project card → VIEW FULL DECK |
| Trappeys | `trappeys-deck.html` | Trappeys project card → VIEW FULL DECK |
| ADC 3K | inline in index.html (pg-adc3k) | ADC 3K project card → VIEW FULL DECK |

---

## adc3k.com — Image Assets

| File | Source | Placement |
|------|--------|-----------|
| wgt-aerial.jpg | Notion: Henry Hub & Power | Willow Glen deck cover (helicopter aerial) |
| three-pic.jpg | Notion: ADC 3K Pods | Hero background (3 pod deployments) |
| store-front.jpg | Notion: MARLIE I | marlie-deck.html Section 05 |
| henry-hub-1.jpg | Notion: Henry Hub & Power | Front page above punch cards |
| henry-hub-2.jpg | Notion: Henry Hub & Power | Louisiana page top |
| henry-hub-3.jpg | Notion: Henry Hub & Power | Technology tab |
| pod-img-1.jpg | Notion: ADC 3K Pods | Ecosystem page |
| pod-img-2.jpg | Notion: ADC 3K Pods | Ecosystem page |
| pod-img-3.jpg | Notion: ADC 3K Pods | Technology tab |

---

## Willow Glen — Power Architecture (Mini Grid)
```
Layer 1 — Renewable Fuels + Solar     PRIMARY · Dock-imported renewable feedstock + solar roof/farm
Layer 2 — Natural Gas                 SECONDARY · Pipeline corridor on-site · Henry Hub ~60mi
Layer 3 — Grid (Bidirectional)        230kV substation · Import OR export · Revenue from excess generation
Layer 4 — Diesel                      EMERGENCY · Hurricane backup · Pipeline-independent
```
Key insight: This was a 2,200 MW power station. The substation goes both ways. Generate + compute + sell excess = three revenue streams.

## Standard ADC 3K Power Stack (all other sites)
```
Layer 1 — Nat Gas + Solar + Battery   PRIMARY · 24/7 · Henry Hub pricing + daytime solar offset
Layer 2 — LUS / Grid                  BACKUP · never primary
Layer 3 — Diesel Gensets              EMERGENCY · on-site fuel · pipeline-independent
```

---

## River Scout — Top Sites
| Score | Tier | Site | Parish | River | Pipeline |
|-------|------|------|--------|-------|----------|
| 94 | A | Willow Glen Terminal | Iberville | Mississippi @ 0.0 mi | 0.0 mi |
| 82 | A | Krotz Springs West Levee | St. Landry | Atchafalaya @ 0.3 mi | 0.0 mi |
| 82 | A | Hwy 190 Industrial, Port Allen | West Baton Rouge | Mississippi @ 0.3 mi | 0.5 mi |
| 80 | A | Belle Grove Industrial, White Castle | Iberville | Mississippi @ 0.1 mi | 1.0 mi |

## Pipeline Scout — Top Sites
| Score | Tier | Site | Parish | Note |
|-------|------|------|--------|------|
| 83 | A | Common St & Arabie Rd, Lake Charles | Calcasieu | ON pipeline |
| 81 | A | Kinder Industrial (Hwy 165) | Allen | Zone X confirmed |
| 81 | A | Hwy 165/I-10, Iowa | Jefferson Davis | 27.75 acres |
| 80 | A | New Iberia (Hwy 90 & Hwy 14) | Iberia | Gas line ON property |

---

## Open Blockers (Require Scott Action)

### Immediate — Willow Glen
- **CBRE contact** — Bryce French, Senior VP — warehouse lease inquiry
- **NVIDIA Inception** — application package + NVL72 TDP request
- **WGT partnership proposal** — lease + revenue share pitch
- **ITEP filing** — must file BEFORE any groundbreaking

### Immediate — Other
- **Formspree** — create account → replace `YOUR_FORM_ID` in connect form
- **UL Lafayette first contact** — Trappeys unlock
- **KLFT Airport Authority** — schedule meeting

### ADC 3K Investor-Critical
1. Customer LOI — zero signed anchor tenants
2. NVIDIA Vera Rubin NVL72 TDP — unpublished
3. HB 827 → parish-level PILOT agreement
4. CapEx reconciliation — $33.2M vs ~$110M
5. Financial model: fix 5.5% tax rate, 3-scenario, unit economics
6. Deck slides: competitive landscape, exit strategy, management team

---

## Confirmed GPS Coordinates
```
Willow Glen:      30.24700 N, 91.09850 W  — 2605 LA-75, St. Gabriel
MARLIE I:         30.21975 N, 92.00645 W  — 1201 SE Evangeline Thruway
Trappeys:         30.21356 N, 92.00163 W  — SE Evangeline Thruway corridor
KLFT Hub:         30.21256 N, 91.99069 W  — Lafayette Regional Airport
```

## Key Notion IDs
```
Site Assets — Images:      31f88f09-7e31-81bd-8141-f00014c5b837
  Henry Hub & Power:       31f88f09-7e31-818c-997b-e3efd1f01fdd
  ADC 3K Pods:             31f88f09-7e31-819f-8d12-c3f6cb4b9aef
  MARLIE I images:         31f88f09-7e31-81eb-a27f-d90d7f37c37c
```

---

## Key Files
- `adc3k-deploy/index.html` — adc3k.com SPA (master deployment)
- `adc3k-deploy/willow-glen-deck.html` — Willow Glen AI Factory + Mini Grid deck (14 slides)
- `adc3k-deploy/marlie-deck.html` — MARLIE I investor deck
- `adc3k-deploy/trappeys-deck.html` — Trappeys investor deck
- `adc3k-deploy/skydio-deck.html` — Skydio/KLFT pitch deck
- `scripts/river_scout.py` — River + pipeline site scout agent
- `scripts/pipeline_scout.py` — Pipeline corridor site scout agent
- `data/river_sites.json` — 15 river scout sites
- `data/pipeline_sites.json` — 16 pipeline scout sites

## Deployment
- Deploy: `cd adc3k-deploy && npx vercel --prod --yes`
- Vercel: mission-control1 (adhscott@yahoo.com)
- Cloudflare: gofast@stfumotorcycles.com

## Next Session — Starting Points
1. **Willow Glen photos** — user mentioned adding more images later
2. **Second river scout pass** — updated keywords (swamp, timber, camp, hunting) in script but not re-run
3. **CBRE outreach draft** — warehouse lease inquiry email to Bryce French
4. **NVIDIA pitch package** — formal Inception application using Willow Glen as showcase site
5. **Formspree** — create account, wire contact form
6. **Mobile audit** — verify Willow Glen deck renders on phone
