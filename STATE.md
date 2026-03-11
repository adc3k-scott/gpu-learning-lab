# Mission Control — Project State
Last updated: 2026-03-10 (Security audit + mobile fix session)

---

## What Was Done This Session

### Full Stack Security Audit
- Ran 3 parallel audit agents: backend (FastAPI/agents/skills), frontend (adc3k.com/web), git secrets scan
- Found 4 CRITICAL, 8 HIGH, 8 MEDIUM, 3 LOW issues across the full stack
- No real API keys or secrets found in git history (clean)

### API Key Authentication (CRITICAL fix #1 — DONE)
- Added `MC_API_KEY` env var auth middleware to FastAPI (main.py)
- 17 endpoints protected with `Depends(require_api_key)`
- Public paths exempt: `/`, `/mobile`, `/docs`, `/openapi.json`
- Auth accepts `X-API-Key` header or `?api_key=` query param (for EventSource/SSE)
- Dev mode: auth disabled when `MC_API_KEY` not set (backward compatible, tests pass)
- 160 tests still green

### CORS Lockdown (HIGH fix #5 — DONE)
- Changed `allow_origins=["*"]` to `MC_CORS_ORIGINS` env var
- Defaults to `http://localhost:8000,http://127.0.0.1:8000`
- Headers restricted to `X-API-Key` and `Content-Type`

### Dashboard Auth Wiring
- Updated `web/mobile.html` with `authHeaders()` helper
- API key loaded from `?key=` URL param or `localStorage`
- All 7 fetch calls + EventSource updated to pass credentials

### Mobile Swipe Fix (deployed live)
- Added touch swipe + wheel scroll to `willow-glen-deck.html` (was stuck on slide 1)
- Added same fix to `klft-deck.html` (also missing touch/wheel)
- Trappeys + Skydio already had touch support (confirmed)
- Marlie deck is long-scroll (no fix needed)
- Deployed to adc3k.com

---

## Project Status Board

| Project | Status | Next Action |
|---------|--------|-------------|
| **Willow Glen** | 14-slide deck live. Mobile swipe fixed. Score 94 Tier A. | Contact CBRE/Bryce French. NVIDIA Inception. WGT partnership proposal. |
| **MARLIE I** | Engineering complete. Investor deck live. | Sign LOI/lease. LUS power capacity. LED Act 730 pre-app. |
| **ADC 3K** | 12 open investor items. Financial model needs fix. | Fix 5.5% tax rate, CapEx recon, 3-scenario model. |
| **Trappeys** | Deck built (18 slides). Live at adc3k.com. | UL Lafayette first contact. |
| **KLFT 1.1** | Skydio deck live. Mobile swipe fixed. | Schedule Airport Authority meeting. |
| **ADC3K.com** | LIVE. 5 project decks. All mobile-swipeable. | Formspree ID (replace YOUR_FORM_ID). Security headers in vercel.json. |
| **Mission Control** | Auth middleware added. 160 tests green. | Set MC_API_KEY in .env. Fix remaining security items (browser eval, rate limiting). |
| **Pipeline Sites** | 16 pipeline sites + 15 river sites scored. | Sabine corridor pending. Second river pass. |
| **Mission Control HD** | Live. Two deferred blockers. | Stripe webhook + Supabase auth redirect. |
| **Ground Zero** | EP001 private. EP002 pending. | PEXELS_API_KEY + run EP002. |

---

## Security Audit Results (2026-03-10)

### Fixed This Session
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

### Git Secrets Scan — CLEAN
No real API keys, tokens, or passwords in git history. .gitignore gaps identified (*.pem, *.key, .env.*).

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

## Deployment
- Deploy site: `cd adc3k-deploy && npx vercel --prod --yes`
- Vercel: mission-control1 (adhscott@yahoo.com)
- Cloudflare: gofast@stfumotorcycles.com

## Next Session — Starting Points
1. **Security fixes** — browser eval restriction, vercel.json security headers, .gitignore gaps
2. **Willow Glen photos** — user mentioned adding more images later
3. **Second river scout pass** — updated keywords not yet run
4. **CBRE outreach draft** — warehouse lease inquiry email
5. **Formspree** — wire contact form
