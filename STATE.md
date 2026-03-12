# Mission Control — Project State
Last updated: 2026-03-12 (Session 5 — Networking content + Heat recovery research + Hub architecture + NCA-AIIO quiz rebuild)

---

## What Was Done This Session (2026-03-12, Session 5)

### adc3k.com Learn Page — AI Factory Networking (4 new sections)
- Sections 08-11 added: Four Networks, InfiniBand vs Ethernet, NVIDIA Networking Stack, Modular Networking Advantage
- Rewrote NVIDIA worksheet content using "AI factory" language
- Framed ADC's modular advantage: software-controlled N/S and E/W scaling
- Deployed to Vercel

### Heat Recovery Research (3-agent deep investigation)
- **TEGs ruled out**: 0.66W per module at 40°C delta-T. BMW/Ford/GM all abandoned. Not viable.
- **ORC viable at 70°C**: ElectraTherm (75-150 kWe, US), Enogia (10-180 kWe, France), Infinity Turbine (native DC output, markets to AI)
- **Solar thermal boost**: Rice University 2025 — flat-plate collectors bump 65°C to 85-90°C, 60-80% more electricity from ORC
- **LAVA Power** (Israel): emerging tech, claims 70-80% Carnot efficiency. Early stage, verify.
- **District heating**: cold climate play (Nordic model). Louisiana = aquaculture/greenhouse in winter months.
- Full research saved to `memory/projects/heat-reuse.md`

### Hub-Spoke Architecture Decision
- **Willow Glen = PRIMARY HUB** ("Big Daddy") — InfiniBand spine, Base Command Manager, primary NOC
- **MARLIE I = Backup NOC / War Room** — 60mi dedicated fiber, edge compute, R&D/staging
- **Edge nodes** (wetland/offshore) = inference-only, connect back via fiber/satellite
- Rationale: InfiniBand needs microsecond latency, 60mi fiber = 1-2ms — compute fabric must live at Willow Glen
- Strategy: get NVIDIA on board first → approach WGT with partnership backed by NVIDIA
- Updated `memory/projects/willow_glen.md` and `memory/projects/marlie_i.md`

### Interactive Network Architecture Diagram
- `factory/network-architecture.html` — 4-tab interactive viewer
- Layer Stack: 7 expandable layers (L0 Physical Transport through L6 Operations)
- Hub & Spoke: SVG topology with animated connection lines
- Data Flow: compute/management/edge/thermal/power paths
- Site Roles: tier cards (Primary Hub, Command Center, Edge Node)

### NCA-AIIO Practice Quiz — Complete Rebuild
- Downloaded all 14 Unit PDFs from Notion (`output/cert-pdfs/`)
- 100 multiple-choice questions sourced ONLY from course material (no guessing)
- Weighted by exam domain: 37 D1 (Essential AI), 40 D2 (Infrastructure), 23 D3 (Operations)
- Cheat sheet tab with quick-reference cards by domain
- Domain filter tabs (D1/D2/D3), shuffle/reset/flag/grade, 60-minute timer
- UI fixes: cheat sheet button always visible in action bar, header overflow fix, tab scrollbar

### Scott Bio Updates
- ECM/closed-loop systems knowledge (FuelTech ECU → AI factory networking parallel)
- Networking foundation (Network+, fiber optic multiplexing from aviation)
- Cross-domain pattern recognition documented

### NCA-AIIO Exam Scheduled
- **Tomorrow, 2026-03-13 at 6:00 PM** — 50 questions, 60 minutes, online proctored
- GTC 2026: March 16-19, San Jose
- Walk into GTC certified = instant credibility

---

## What Was Done Session 4 (2026-03-12, earlier)

### NVIDIA DGX SuperPOD Architecture (Full Stack Alignment)
- Committed to NVIDIA-only stack across every layer — no third-party alternatives
- Fat-tree (spine-leaf) topology: pods = leaf nodes on NVIDIA Quantum InfiniBand spine
- Updated all materials: Inception draft, website (adc3k.com), memory files, one-pager
- Replaced Mellanox/Arista references in marlie-phase1.html with NVIDIA Quantum
- Created `memory/projects/nvidia_strategy.md` — strategy doc for GTC positioning

### Remote Deployment Strategy — Wetlands + Offshore
- Wetland piling concept: pods on wood pilings in marshland along gas pipelines
- Offshore extension: pods on rigs/barges in Gulf of America, flare gas capture, ocean cooling
- 4-tier deployment strategy: MARLIE I (HQ) → Willow Glen (flagship) → Wetland swarm → Offshore
- Core equation locked: SITE VIABILITY = POWER + COOLING
- Gas line property arbitrage documented — discounted land because gas lines are a liability to everyone else
- Created `memory/projects/wetland_deployment.md` with full strategy
- Top 10 deployment sites ranked (all data from pipeline_sites.json + river_sites.json)

### GTC 2026 Materials (March 16-19, San Jose)
- `factory/gtc-one-pager.md` — One-pager with fat-tree diagram, comparison table, declining cost curve, workforce section
- `factory/infrastructure-topology.html` — Interactive 3-view topology viewer (fat-tree, LA map, cost curve)
- `factory/wetland-rendering.html` — Concept rendering of pods on pilings + hurricane resilience cross-section
- `factory/nvidia-cert-quiz.html` — 60-question practice exam (later rebuilt to 100 questions from PDFs)

### Declining Cost Curve Business Model
- Every pod makes every other pod more efficient
- Fixed costs spread thinner, AI optimization compounds, power cheaper at scale, manufacturing costs drop
- Documented in one-pager with ASCII cost curve graph

### Workforce Advantage (ROV Industry)
- ROV crews = perfect pod deployment workforce (LARS setup = pod installation)
- Thermal analogy: oil-compensated ROV motors = EC-110 immersion cooling
- Deck pack testing with seawater heat exchangers = exact same cooling concept
- Hiring moat: talent pool no other AI company knows exists
- Scott bio updated with Katrina piling experience, offshore piling knowledge, workforce section

### Honest Analysis — Mega-Facilities vs ADC Model
- Documented structural advantages of both approaches
- ADC risks identified: InfiniBand latency between sites, wetland permitting, capital gap, EC-110 at scale
- Mega-facility risks: GPU obsolescence, training-only optimization, power lock-in, community backlash
- Conclusion: modular wins for inference (90%+ of demand), fixed wins for frontier training

### File Organization
- Created missing `heat-reuse.md` memory file
- Updated STATE.md (this file)
- Verified all 11 memory project files exist and match MEMORY.md index
- Confirmed .gitignore covers credentials.json, youtube_token.json, output/
- "Gulf of Mexico" → "Gulf of America" in all memory files

---

## What Was Done Session 3 (2026-03-11)

### Security Hardening (adc3k.com + Mission Control)
- Full 3-agent security audit (web/SPA, server/API, git history)
- vercel.json: Added CSP, HSTS, X-Frame-Options, X-Content-Type-Options, XSS-Protection, Referrer-Policy
- Iframe sandboxing: All 5 deck iframes got `sandbox="allow-same-origin allow-scripts allow-popups"`
- Browser eval restriction: `BROWSER_ALLOW_EVAL` env var gate on `skills/builtin/browser.py`
- "Data center" language sweep: 20 instances changed across 4 files (index.html, marlie-deck, trappeys-deck, klft-deck). 16 instances kept with documented rationale (legal/contrast/external).
- Security headers verified live on production via curl

### Energy Efficiency (adc3k.com Home Page)
- Hero description rewritten: efficiency + immersion cooling messaging
- New Energy Efficiency section added between "Why Here" grid and NVIDIA Platform: 3 cards (PUE 1.03, 3-5c/kWh, Solar First) + savings math callout

### Willow Glen Renewable Energy
- Created `memory/projects/willow_glen.md` — 4-Layer Mini Grid (solar, nat gas, grid, biodiesel)
- Green hydrogen roadmap: electrolysis via solar excess, stored in existing tank farm, burned in modified generators
- Ship terminal = marine hydrogen/biodiesel delivery capability

### Edge AI — Notion (9 pages created)
- Edge AI section (5 pages): What It Is, Customer Profiles, Pod as Edge Node, NVIDIA Certification & GTM, Edge vs Cloud Economics
- Manufacturing section (4 pages): Parent strategy, Step 1 Bootstrap, Step 2 Automated, Omniverse Guide

### Manufacturing — New Iberia Factory Engineering Package
- `factory/new-iberia/floor-plan.html` — Interactive factory floor plan (52,800 SF, 7 stations, U-flow, 14 robots, 22 AI cameras)
- `factory/new-iberia/production-sim.html` — Live production line simulator with real cycle times
- `factory/new-iberia/power-system.html` — Single-line electrical diagram (2.8 MW gas + 750 kW solar + 500 kWh battery)
- `factory/new-iberia/timeline.html` — 14-month construction Gantt chart with critical path
- `factory/new-iberia/FACTORY-SPEC.md` — 12-section master engineering spec
- `factory/new-iberia/BOM.md` — Complete BOM with 18 vendors, $7.9-9.3M total
- `memory/projects/manufacturing.md` — Updated with full factory specs

### Manufacturing — Website Project Cards
- Added 2 manufacturing project cards to Projects page (Baton Rouge Terminal + New Iberia Factory)
- Updated project count: "Five active projects" → "Seven active projects"
- Deployed to Vercel

### Baton Rouge Terminal (Step 1) Engineering
- `factory/baton-rouge/` — Building requirements, station layout, lease spec sheet, staffing plan
- Designed for real estate broker handoff: "find me this building"

### NVIDIA Inception Application
- Full application draft ready for review and submission

---

## Project Status Board

| Project | Status | Next Action |
|---------|--------|-------------|
| **Willow Glen** | 14-slide deck live. Badges. 4-layer mini grid documented. | Contact CBRE/Bryce French. NVIDIA Inception. WGT partnership. ITEP. |
| **MARLIE I** | Engineering complete. Investor deck live. | Sign LOI/lease. LUS power capacity. LED Act 730 pre-app. |
| **ADC 3K** | 12 open investor items. Financial model needs fix. | Fix 5.5% tax rate, CapEx recon, 3-scenario model. |
| **Trappeys** | Deck built (18 slides). Live at adc3k.com. | UL Lafayette first contact. |
| **KLFT 1.1** | Skydio deck live. Mobile swipe fixed. | Schedule Airport Authority meeting. |
| **New Iberia Factory** | Full engineering package complete. 6 documents. | Site survey. Land acquisition. ITEP filing. Robot POs. |
| **Baton Rouge Terminal** | Engineering package complete. Lease spec ready. | Real estate broker search. Building tour. |
| **ADC3K.com** | LIVE. Security hardened. Energy efficiency added. Contact form FIXED (FormSubmit.co). | Confirm activation email in scott@adc3k.com inbox. |
| **Mission Control** | Auth middleware. 222 tests. RunPod SSH exec. Adaptive replanning. Prompt injection defense. Secret masking. Rate limiting. Dead letter queue. | Set MC_API_KEY. Remaining: browser profile env var, DOM XSS in site-intel. |
| **NCA-AIIO Cert** | 100-question quiz rebuilt from PDFs. Cheat sheet ready. | **EXAM TOMORROW 6 PM (2026-03-13)** |
| **GTC 2026** | One-pager, topology viewer, wetland rendering, network architecture, quiz all ready. | Print PDF. Submit Inception. Book travel. |
| **Remote Deployment** | Wetland + offshore strategy documented. Top 10 sites ranked. | Wetland permitting research. USACE Section 404. Krotz Springs site visit. |
| **Pipeline Sites** | 16 pipeline + 15 river sites. Top 10 ranked. | Sabine corridor. Second river pass. |
| **Mission Control HD** | Live. Two deferred blockers. | Stripe webhook + Supabase auth redirect. |
| **Ground Zero** | EP001 private. EP002 pending. | PEXELS_API_KEY + run EP002. |

---

## Security Status (2026-03-11)

### Fixed This Session
- [x] #10 HIGH: Security headers on adc3k.com — CSP/HSTS/X-Frame/nosniff added to vercel.json
- [x] #11 HIGH: Unsafe iframes — sandbox attribute added to all 5 deck iframes
- [x] #4 CRITICAL: Browser `eval` action — restricted behind BROWSER_ALLOW_EVAL env var
- [x] "Data center" language sweep — 20 instances changed, 16 kept with rationale

### Previously Fixed
- [x] #1 CRITICAL: No auth on FastAPI endpoints — MC_API_KEY middleware
- [x] #5 HIGH: Wildcard CORS — MC_CORS_ORIGINS locked

### Remaining (Priority Order)
- [x] #13 CRITICAL: Contact form — switched to FormSubmit.co (scott@adc3k.com), deployed, needs activation click
- [ ] #2 CRITICAL: File upload + ZIP extraction — add auth (covered by MC_API_KEY but verify)
- [ ] #3 CRITICAL: Browser skill hardcodes Edge profile path — move to env var
- [x] #6 HIGH: LLM prompt injection — sanitize_input() + _validate_step_dicts() in planner
- [x] #7 HIGH: API keys in RunPod error messages — core/sanitize.py mask_secrets + safe_error
- [ ] #8 HIGH: Credentials to plaintext .env via POST /config — now auth-gated
- [x] #9 HIGH: No rate limiting — RateLimitMiddleware (60rpm default, MC_RATE_LIMIT env var)
- [ ] #12 HIGH: DOM XSS in site-intel.html — safe event listeners
- [ ] #13-#20 MEDIUM: Docker config, HTTPS, job TTL, audit logging, .gitignore gaps

---

## Manufacturing Engineering Files

### New Iberia Factory (Step 2 — AI Automated)
```
factory/new-iberia/
├── floor-plan.html      — Interactive floor plan (7 stations, 14 robots, 22 cameras)
├── production-sim.html  — Live production simulator with cycle times
├── power-system.html    — Single-line electrical diagram
├── timeline.html        — 14-month construction Gantt chart
├── FACTORY-SPEC.md      — Master engineering specification (12 sections)
└── BOM.md               — Bill of materials ($7.9-9.3M, 18 vendors)
```

### Baton Rouge Terminal (Step 1 — Bootstrap)
```
factory/baton-rouge/
├── TERMINAL-SPEC.md     — Building requirements + station layout
└── lease-requirements.md — Real estate broker handoff document
```

---

## adc3k.com — Deck Architecture

| Deck | File | Mobile Swipe | Entry Point |
|------|------|-------------|-------------|
| Willow Glen | `willow-glen-deck.html` | FIXED | FIRST project card |
| MARLIE I | `marlie-deck.html` | N/A (scroll) | MARLIE I card |
| Skydio / KLFT | `skydio-deck.html` | Already worked | KLFT card |
| Trappeys | `trappeys-deck.html` | Already worked | Trappeys card |
| KLFT (internal) | `klft-deck.html` | FIXED | Not on SPA |

---

## Open Blockers (Require Scott Action)

### Immediate — CRITICAL
- **Formspree** — create account, replace `YOUR_FORM_ID` in connect form (BROKEN IN PRODUCTION)
- **NVIDIA Inception** — application drafted, needs review and submit (THIS WEEK)

### Immediate — Willow Glen
- **CBRE contact** — Bryce French, Senior VP — warehouse lease inquiry
- **WGT partnership proposal** — lease + revenue share pitch
- **ITEP filing** — must file BEFORE any groundbreaking

### Immediate — Manufacturing
- **New Iberia site survey** — exact address for GPS coordinates
- **Baton Rouge building search** — engage real estate broker with lease spec

### Immediate — Other
- **UL Lafayette first contact** — Trappeys unlock
- **KLFT Airport Authority** — schedule meeting
- **MC_API_KEY** — add to `.env` before public deployment

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
New Iberia:       PENDING                 — 14th St & Hwy 90, New Iberia
Baton Rouge:      PENDING                 — Lafayette area (lease TBD)
```

## Key Files
- `adc3k-deploy/index.html` — adc3k.com SPA (master deployment)
- `adc3k-deploy/willow-glen-deck.html` — Willow Glen AI Factory + Mini Grid deck (14 slides)
- `adc3k-deploy/marlie-deck.html` — MARLIE I investor deck
- `adc3k-deploy/trappeys-deck.html` — Trappeys investor deck
- `adc3k-deploy/skydio-deck.html` — Skydio/KLFT pitch deck
- `factory/new-iberia/` — New Iberia factory engineering package (6 files)
- `factory/baton-rouge/` — Baton Rouge Terminal engineering package
- `main.py` — FastAPI server with auth middleware
- `web/mobile.html` — Mission Control mobile dashboard (auth-enabled)
- `memory/scott_tomsu.md` — Scott Tomsu founder biography + career data

## Deployment
- Deploy site: `cd adc3k-deploy && npx vercel --prod --yes`
- Vercel: mission-control1 (adhscott@yahoo.com)
- Cloudflare: gofast@stfumotorcycles.com

## Next Session — Starting Points
1. **NCA-AIIO EXAM (2026-03-13, 6 PM)** — Final study. Quiz at `factory/nvidia-cert-quiz.html`. Cheat sheet tab.
2. **GTC PREP (March 16-19)** — Print one-pager PDF. Submit Inception application. Book flights/hotel.
3. **Contact form** — FIXED (FormSubmit.co). Confirm activation email in scott@adc3k.com.
4. **Wetland permitting** — USACE Section 404 research for piling deployment
5. **Krotz Springs site visit** — 160 acres, $3K/acre, pipeline ON SITE
6. **New Iberia factory site** — get exact address, GPS, parcel boundaries
7. **CBRE outreach** — Willow Glen warehouse lease inquiry

## GTC 2026 — Phone-Ready Materials
```
factory/gtc-one-pager.md             — Print this (front/back)
factory/infrastructure-topology.html  — Fat-tree + LA map + cost curve
factory/network-architecture.html     — 4-tab interactive network diagram (Layer Stack, Hub & Spoke, Data Flow, Site Roles)
factory/wetland-rendering.html        — Pods on pilings + hurricane resilience
factory/nvidia-cert-quiz.html         — 100-question practice exam (study tool) + cheat sheet
factory/nvidia-inception-draft.md     — Submit BEFORE flying
```
