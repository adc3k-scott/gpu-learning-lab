# Mission Control — Project State
Last updated: 2026-03-09 (Skydio deck session)

---

## What Was Done This Session

### Skydio Gulf Coast Deck — Built + Deployed to adc3k.com
- Extracted 41 images from Skydio PDF (PyMuPDF) → `web/skydio-images/` + `adc3k-deploy/skydio-images/`
- Built `web/skydio-deck.html`: 24-slide full-screen SPA (same format as KLFT/MARLIE decks)
  - Removed slides 4, 22, 23; split slide 12 → s12 + s12b (airport diagram gets its own full slide)
  - Mouse wheel + touch swipe navigation (650ms throttle, `passive:false`)
  - Vision statement photo removed; email updated to scott@adc3k.com
  - SLIDE_IDS array handles non-sequential IDs after removals; TOTAL=24
- Wired into `adc3k-deploy/index.html`:
  - `pg-skydio` iframe page with sticky nav bar (Back / title / Request Investor Package)
  - KLFT project card: single VIEW FULL DECK button → `showPage('skydio')`
  - `deckPages` + `pages` arrays updated; `#pg-skydio.active` CSS rule added
  - Null-safe forEach in `showPage` prevents TypeError on missing divs
- Deployed live at adc3k.com via Vercel (commit `bebfd46`)

---

## Project Status Board

| Project | Status | Next Action |
|---------|--------|-------------|
| **MARLIE I** | Engineering complete. Investor deck live at adc3k.com. | Sign LOI/lease. LUS power capacity (337-291-5577). LED Act 730 pre-app. |
| **ADC 3K** | 12 open investor items. Financial model needs fix. | Fix 5.5% tax rate, CapEx recon, 3-scenario model. Add competitive/exit/team slides. |
| **Trappeys** | Strategy defined. No standalone deck yet. | `marlie/Trappeys-Investor-Deck.html` → iframe treatment (same pattern as MARLIE/KLFT). |
| **KLFT 1.1** | Skydio partnership deck live at adc3k.com. | Schedule Airport Authority meeting. Building sq ft + condition report first. |
| **Skydio Deck** | LIVE at adc3k.com — accessible from KLFT card. | No blockers. |
| **Pipeline Sites** | 16 sites scored. 4 Tier A. | Sabine corridor pending (needs API credits). |
| **ADC3K.com** | LIVE. MARLIE I + KLFT/Skydio + ADC3K + Trappeys deck pages all wired. | Formspree ID (replace YOUR_FORM_ID). Trappeys iframe upgrade. |
| **Mission Control HD** | Live. Two deferred blockers. | Stripe live webhook + Supabase auth redirect URLs. |
| **Ground Zero** | EP001 private. EP002 pending. | PEXELS_API_KEY in .env — run EP002. |
| **Mission Control (repo)** | 160 tests green. All 10 agents operational. | No blockers. |

---

## adc3k.com Deck Architecture

| Deck | File | Entry Point |
|------|------|-------------|
| MARLIE I | `marlie-deck.html` | MARLIE I project card → VIEW FULL DECK |
| Skydio / KLFT | `skydio-deck.html` | KLFT project card → VIEW FULL DECK |
| ADC 3K | inline in index.html (pg-adc3k) | ADC 3K project card → VIEW FULL DECK |
| Trappeys | inline in index.html (pg-trappeys) | Trappeys card → VIEW FULL DECK |

**Next deck upgrade:** Trappeys → iframe loading `marlie/Trappeys-Investor-Deck.html` (same pattern as MARLIE I)

### SPA Navigation Pattern (index.html)
- `pages` array must match all `pg-*` div IDs
- `deckPages` controls footer hide + body overflow:hidden
- CSS: `#pg-X.active{display:block;height:100vh;min-height:0;overflow:hidden}` for iframe decks
- `showPage` forEach uses null-safe `if(el)` check — prevents TypeError if div missing

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

## Pipeline Scout — Top Sites
| Score | Tier | Site | Parish | Note |
|-------|------|------|--------|------|
| 83 | A | Common St & Arabie Rd, Lake Charles | Calcasieu | ON pipeline |
| 81 | A | Kinder Industrial (Hwy 165) | Allen | Zone X confirmed |
| 81 | A | Hwy 165/I-10, Iowa | Jefferson Davis | 27.75 acres |
| 80 | A | New Iberia (Hwy 90 & Hwy 14) | Iberia | Gas line ON property |
| 74 | B | Smede Hwy, Broussard | St. Martin | 46 acres, Zone X |
| 72 | B | Hwy 90 Energy Corridor, Gray | Terrebonne | 108 acres, Zone X |
ELIMINATE: Hulin Road, Erath — FEMA Zone VE.
Sabine corridor — NOT YET RUN (needs API credits).

---

## Open Blockers (Require Scott Action)

### Immediate
- **Formspree** — create formspree.io account → replace `YOUR_FORM_ID` in connect form
- **Trappeys deck upgrade** — iframe treatment using `marlie/Trappeys-Investor-Deck.html`
- **Building photo cleanup** — upload `marlie/Store_Front_Pic.jpg` to cleanup.pictures (remove Dynojet/Dino)
- **KLFT Airport Authority** — schedule meeting; get building sq footage + condition report first
- **UL Lafayette first contact** — president / provost / research computing director (Trappeys unlock)
- **Sabine corridor scout** — `python scripts/pipeline_scout.py --corridors "Sabine" --max-sites 4` (needs API credits)

### ADC 3K Investor-Critical
1. Customer LOI — zero signed anchor tenants (fatal for institutional raise)
2. NVIDIA Vera Rubin NVL72 TDP — unpublished; contact NVIDIA Enterprise Sales
3. HB 827 → replace with parish-level PILOT agreement
4. CapEx reconciliation — $33.2M stated vs analyst estimate ~$110M
5. Financial model: fix 5.5% tax rate, 3-scenario model, unit economics per pod
6. Deck slides: competitive landscape, exit strategy, management team

### MARLIE I
- LOI or lease — must have paper before investor conversations advance
- LUS utility capacity — (337) 291-5577 — ask for 1201 SE Evangeline power availability
- LED Act 730 pre-application meeting

### Ground Zero
- EP002 ready: `python -m aido.pipeline --episode EP002 --local-render`
- Social: TikTok, Instagram, X/Twitter, LinkedIn as @GroundZeroAI
- groundzeroai.com domain — verify ownership

### Mission Control HD (Deferred)
1. Stripe live webhook → endpoint missioncontrolhd.com/api/stripe/webhook → copy whsec_ → update STRIPE_WEBHOOK_SECRET → redeploy
2. Supabase auth redirect URLs → set Site URL + add missioncontrolhd.com/**

---

## Confirmed GPS Coordinates
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
```

---

## Notion API Patterns (confirmed working)
- All edits: write temp Python script → run → delete: `python _script.py 2>&1 && rm _script.py`
- Full tree: `python scripts/notion_tree.py` → paste full output. Never browser. Never summary.
- Chain git: `git add FILE && git commit -m "..."` — one approval
- Page move to workspace root: NOT POSSIBLE via API — UI only

---

## Key Files
- `main.py` — FastAPI app, 10 agents, SSE, streaming chat
- `adc3k-deploy/index.html` — adc3k.com SPA (master deployment file)
- `adc3k-deploy/skydio-deck.html` — Skydio/KLFT pitch deck (24 slides, deployed)
- `adc3k-deploy/skydio-images/` — 41 images extracted from Skydio PDF
- `web/skydio-deck.html` + `web/skydio-images/` — source copies
- `web/klft-deck.html` — original KLFT 10-slide deck (separate from Skydio deck)
- `marlie/` — MARLIE I investor deck HTML + PDF + Store_Front_Pic.jpg
- `marlie/Trappeys-Investor-Deck.html` — Trappeys deck (needs iframe treatment)
- `aido/` — Ground Zero video pipeline
- `scripts/notion_tree.py` — zero-friction Notion tree print
- `data/pipeline_sites.json` — 16 scored pipeline sites
- `pyproject.toml` — source of truth for deps

---

## adc3k.com — Deployment Info (LIVE)
- Vercel: mission-control1 account (adhscott@yahoo.com)
- Cloudflare: gofast@stfumotorcycles.com — Zone ID: 7869891ccc4bb74419d38bd749c24af1
- Deploy: `cd adc3k-deploy && npx vercel --prod --yes`

## Next Session — Starting Points
1. **Formspree** — create account, replace `YOUR_FORM_ID` in connect form, redeploy
2. **Trappeys deck** — iframe upgrade using `marlie/Trappeys-Investor-Deck.html`
3. **ADC 3K financials** — fix 5.5% tax, CapEx recon ($33.2M vs ~$110M), 3-scenario model
4. **Building photo** — cleanup.pictures for Store_Front_Pic.jpg
5. **KLFT meeting prep** — Airport Authority packet + building condition report
