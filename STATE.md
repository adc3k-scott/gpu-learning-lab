# Mission Control — Project State
Last updated: 2026-03-10 (Website content + founder branding session)

---

## What Was Done This Session

### ADC3K.com Home Page Overhaul
- Removed "Three Platforms One Integrated System" section (duplicated Ecosystem)
- Moved The Thesis section between hero and pods-night photo to break up consecutive images
- Tightened hero section spacing to prevent text cutoff at bottom of viewport
- Doubled ADC logo + Made in USA badges to 96px on home page
- Changed "data centers" to "AI factories" in Thesis copy

### Why ADC Tab — Complete Rebuild
- Section 01: FOUNDER — 25-year deepwater robotics career, 3,000+ meters Gulf of America, 760-foot sat dive, West Africa ops (Pacific Wizard 2013-2018), customer testimonials
- Section 02: CROSS-DOMAIN EXPERTISE — 6 credential cards (deepwater, aviation, motorsports, construction, software, safety)
- Section 03: OPERATIONS LEADERSHIP — Mission Control callout (built in-house proof), 6-layer IN-HOUSE stack
- ROV photo above Section 02, winning photo at bottom
- "Data center" language replaced with "AI factory builder"

### Learning Center — New Section 01
- CPU vs GPU: THE FUNDAMENTAL DIFFERENCE — image, two-column comparison, old-vs-new framing
- Renumbered remaining sections 02-07

### Technology Tab
- Added immersion cooling image above 3-Layer Power Architecture

### Willow Glen Deck Updates
- Slide 9: SVG coverage map replaced with drone-grid.jpg photo
- Slide 1: Removed Score 94/Tier A stat
- ADC logo + Made in USA badges on slides 1 and 14 only (position:absolute, 48px, bottom:56px for taskbar clearance)

### Images Downloaded from Notion
- `drone-grid.jpg` — drone near electrical grid
- `immersion-cooling.jpg` — GRC single-phase immersion cooling
- `cpu-vs-gpu.jpg` — CPU vs GPU architecture comparison
- `rov.jpg` — ROV in deepwater operations
- `winning.jpg` — Scott in winner's circle

### Founder Profile Saved
- Downloaded Scott's resume from Notion, extracted key career data
- Created `memory/scott_tomsu.md` — full biography, career highlights, credentials
- Updated MEMORY.md with founder details

---

## Project Status Board

| Project | Status | Next Action |
|---------|--------|-------------|
| **Willow Glen** | 14-slide deck live. Badges on slides 1+14. Mobile swipe working. | Contact CBRE/Bryce French. NVIDIA Inception. WGT partnership proposal. |
| **MARLIE I** | Engineering complete. Investor deck live. | Sign LOI/lease. LUS power capacity. LED Act 730 pre-app. |
| **ADC 3K** | 12 open investor items. Financial model needs fix. | Fix 5.5% tax rate, CapEx recon, 3-scenario model. |
| **Trappeys** | Deck built (18 slides). Live at adc3k.com. | UL Lafayette first contact. |
| **KLFT 1.1** | Skydio deck live. Mobile swipe fixed. | Schedule Airport Authority meeting. |
| **ADC3K.com** | LIVE. Why ADC rebuilt. Learning Center expanded. Home page tightened. | Formspree ID. Security headers. Remaining "data center" sweep (Ecosystem, Louisiana, Security tabs). |
| **Mission Control** | Auth middleware added. 160 tests green. | Set MC_API_KEY in .env. Fix remaining security items. |
| **Pipeline Sites** | 16 pipeline sites + 15 river sites scored. | Sabine corridor pending. Second river pass. |
| **Mission Control HD** | Live. Two deferred blockers. | Stripe webhook + Supabase auth redirect. |
| **Ground Zero** | EP001 private. EP002 pending. | PEXELS_API_KEY + run EP002. |

---

## Security Audit Results (2026-03-10)

### Fixed
- [x] #1 CRITICAL: No auth on FastAPI endpoints — MC_API_KEY middleware added
- [x] #5 HIGH: Wildcard CORS — locked to MC_CORS_ORIGINS

### Remaining (Priority Order)
- [ ] #2 CRITICAL: File upload + ZIP extraction — add auth (now covered by MC_API_KEY)
- [ ] #3 CRITICAL: Browser skill hardcodes Edge profile path — move to env var
- [ ] #4 CRITICAL: Browser `eval` action — restrict or remove
- [ ] #6 HIGH: LLM prompt injection — sanitize planner input/output
- [ ] #7 HIGH: API keys in RunPod error messages — mask error responses
- [ ] #8 HIGH: Credentials to plaintext .env via POST /config — now auth-gated
- [ ] #9 HIGH: No rate limiting — add per-IP throttle
- [ ] #10 HIGH: Missing security headers on adc3k.com — add CSP/HSTS to vercel.json
- [ ] #11 HIGH: Unsafe iframes — add sandbox attribute
- [ ] #12 HIGH: DOM XSS in site-intel.html — safe event listeners
- [ ] #13-#20 MEDIUM: Docker config, HTTPS, job TTL, audit logging, .gitignore gaps, Formspree

---

## adc3k.com — Deck Architecture

| Deck | File | Mobile Swipe | Entry Point |
|------|------|-------------|-------------|
| Willow Glen | `willow-glen-deck.html` | FIXED | FIRST project card |
| MARLIE I | `marlie-deck.html` | N/A (scroll) | MARLIE I card |
| Skydio / KLFT | `skydio-deck.html` | Already worked | KLFT card |
| Trappeys | `trappeys-deck.html` | Already worked | Trappeys card |
| KLFT (internal) | `klft-deck.html` | FIXED | Not on SPA |
| ADC 3K | inline in index.html | N/A | ADC 3K card |

---

## Open Blockers (Require Scott Action)

### Immediate — Security
- **MC_API_KEY** — add to `.env` before any public deployment of Mission Control server

### Immediate — Willow Glen
- **CBRE contact** — Bryce French, Senior VP — warehouse lease inquiry
- **NVIDIA Inception** — application package + NVL72 TDP request
- **WGT partnership proposal** — lease + revenue share pitch
- **ITEP filing** — must file BEFORE any groundbreaking

### Immediate — Other
- **Formspree** — create account, replace `YOUR_FORM_ID` in connect form
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

## Key Files
- `adc3k-deploy/index.html` — adc3k.com SPA (master deployment)
- `adc3k-deploy/willow-glen-deck.html` — Willow Glen AI Factory + Mini Grid deck (14 slides)
- `adc3k-deploy/marlie-deck.html` — MARLIE I investor deck
- `adc3k-deploy/trappeys-deck.html` — Trappeys investor deck
- `adc3k-deploy/skydio-deck.html` — Skydio/KLFT pitch deck
- `main.py` — FastAPI server with auth middleware
- `web/mobile.html` — Mission Control mobile dashboard (auth-enabled)
- `memory/scott_tomsu.md` — Scott Tomsu founder biography + career data

## Deployment
- Deploy site: `cd adc3k-deploy && npx vercel --prod --yes`
- Vercel: mission-control1 (adhscott@yahoo.com)
- Cloudflare: gofast@stfumotorcycles.com

## Next Session — Starting Points
1. **"Data center" sweep** — remaining instances in Ecosystem, Louisiana, Security tabs, alt tags
2. **Security fixes** — browser eval restriction, vercel.json security headers, .gitignore gaps
3. **Formspree** — wire contact form
4. **Home page hero** — verify text no longer cut off on various screen sizes; may need further mobile tweaks
5. **Willow Glen photos** — user mentioned adding more images later
6. **CBRE outreach draft** — warehouse lease inquiry email
