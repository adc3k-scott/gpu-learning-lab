# Security Audit — 2026-03-25

**Auditor:** Mission Control (automated)
**Scope:** adc3k.com, louisianaai.net, mission-control-hd.com, source code, API endpoints, third-party integrations
**Date:** March 25, 2026

---

## EXECUTIVE SUMMARY

| Rating | Count |
|--------|-------|
| CRITICAL | 2 |
| HIGH | 3 |
| MEDIUM | 3 |
| LOW | 2 |
| CLEAN | 12 |

---

## 1. WEBSITE SECURITY

### adc3k.com (Vercel + Cloudflare)

| Check | Status | Rating |
|-------|--------|--------|
| SSL/TLS | Valid, HSTS enabled (max-age=31536000; includeSubDomains) | CLEAN |
| Content-Security-Policy | Present and restrictive (self + inline + Google Fonts + YouTube + FormSubmit) | CLEAN |
| X-Frame-Options | SAMEORIGIN | CLEAN |
| X-Content-Type-Options | nosniff | CLEAN |
| X-XSS-Protection | 1; mode=block | CLEAN |
| Referrer-Policy | strict-origin-when-cross-origin | CLEAN |
| .env exposure | Returns index.html (SPA fallback), not .env contents | CLEAN |
| robots.txt | Returns index.html (no robots.txt deployed, Vercel SPA catch-all) | LOW |

### louisianaai.net (Vercel)

| Check | Status | Rating |
|-------|--------|--------|
| SSL/TLS | Valid, HSTS enabled | CLEAN |
| Content-Security-Policy | **NOT PRESENT** — vercel.json has no CSP header | MEDIUM |
| X-Frame-Options | SAMEORIGIN | CLEAN |
| X-Content-Type-Options | nosniff | CLEAN |
| X-XSS-Protection | 1; mode=block | CLEAN |
| Referrer-Policy | strict-origin-when-cross-origin | CLEAN |
| .env exposure | Returns index.html (SPA fallback) | CLEAN |
| robots.txt | Returns index.html (no robots.txt deployed) | LOW |

### mission-control-hd.com (Vercel + Next.js)

| Check | Status | Rating |
|-------|--------|--------|
| SSL/TLS | Valid, HSTS enabled (max-age=63072000) | CLEAN |
| Content-Security-Policy | Present and well-scoped (self + Stripe + Supabase + Anthropic + Kit + Cloudflare) | CLEAN |
| X-Frame-Options | DENY (strongest setting) | CLEAN |
| X-Content-Type-Options | nosniff | CLEAN |
| X-XSS-Protection | 1; mode=block | CLEAN |
| Referrer-Policy | strict-origin-when-cross-origin | CLEAN |
| Permissions-Policy | camera=(), microphone=(), geolocation=() | CLEAN |
| .env exposure | Returns Next.js 404 page | CLEAN |
| robots.txt | Present, properly configured (allow public, block private routes) | CLEAN |

---

## 2. API SECURITY

### louisianaai.net API Endpoints

| Endpoint | Method | Auth Required? | Test Result | Rating |
|----------|--------|---------------|-------------|--------|
| /api/webhook | GET | N/A | Correctly returns 405 "Method not allowed" | CLEAN |
| /api/webhook | POST | **NONE** | Accepts ANY JSON payload, logs it, forwards to email | **HIGH** |
| /api/process-registration | POST | **NONE** | Processes fake data, triggers Brevo email send | **HIGH** |
| /api/brevo-sync | POST | **NONE** | Accepts any payload, syncs to Brevo CRM | **HIGH** |
| /api/filing-assistant | GET | N/A | Returns 405 | CLEAN |
| /api/filing-assistant | POST | **NONE** | Processes and sends emails to arbitrary addresses | MEDIUM |
| /api/registrations | GET | **NONE** | **Returns all registration data including names, emails, organizations, and Brevo delivery stats** | **CRITICAL** |

**Details on CRITICAL finding — /api/registrations:**
Anyone can GET `https://louisianaai.net/api/registrations` and receive:
- Full list of all registrants (names, emails, organizations, institution types, parishes)
- Brevo email campaign statistics (delivery counts, opens, clicks, bounces)
- No authentication, no rate limiting

**Details on HIGH findings — unauthenticated POST endpoints:**
- `/api/webhook`: Anyone can send fake call data. It gets forwarded to info@louisianaai.net and synced to Brevo CRM. An attacker could flood the inbox and pollute CRM data.
- `/api/process-registration`: Anyone can trigger the full registration pipeline with fake data, causing Brevo to send real emails to arbitrary addresses. This could burn Brevo credits and damage sender reputation.
- `/api/brevo-sync`: Direct Brevo CRM sync with no validation. Attacker can create fake contacts/deals.

---

## 3. SOURCE CODE — EXPOSED SECRETS

### .env File (Project Root)

| Finding | Rating |
|---------|--------|
| `.env` exists at repo root with ALL API keys (Anthropic, Notion, RunPod, Bland, HeyGen, Brevo, ElevenLabs, Pexels, NGC, MC_API_KEY) | **See git status below** |
| `.env` is in `.gitignore` — NOT tracked by git | CLEAN |
| `.env` never committed to git history (verified by searching for each key value) | CLEAN |

### Git History — Previously Committed Secrets

| Secret | Status | Rating |
|--------|--------|--------|
| RunPod API key (`rpa_G1QWM...`) | **WAS hardcoded in `scripts/render_willow_glen.py`** in commit `1373e4c`, removed in `55fd48f`. **STILL IN PUBLIC GIT HISTORY.** | **CRITICAL** |
| All other API keys | Never committed | CLEAN |

**The repo is PUBLIC** (`github.com/adc3k-scott/gpu-learning-lab`, visibility: public). Anyone can view commit `1373e4c` and extract the RunPod API key.

### Deployed HTML Files

| Check | Result | Rating |
|-------|--------|--------|
| API keys in HTML | `trappeys-dsx-prep.html` contains `RUNPOD_API_KEY='rp_...'` and `NVIDIA_API_KEY='nvapi-...'` — but these are placeholder examples (ellipsis, not real keys) | CLEAN |
| Bearer tokens in HTML | None found | CLEAN |
| Hardcoded secrets in louisianaai-site HTML | None found | CLEAN |

### Scripts / Server-Side Code

| Check | Result | Rating |
|-------|--------|--------|
| Bland.ai sync scripts | Keys loaded from `process.env` only, not hardcoded | CLEAN |
| Brevo API calls | Keys loaded from `process.env` only | CLEAN |
| HeyGen script | Key loaded from `os.environ.get()` only | CLEAN |
| Test files | `tests/test_security.py` contains `sk-1234567890abcdefghijklmnop` — this is a test fixture, not a real key | CLEAN |

---

## 4. BLAND.AI PHONE AGENT

| Check | Result | Rating |
|-------|--------|--------|
| API key in deployed files | Not exposed in any HTML/JS served to browsers | CLEAN |
| API key in source code | Loaded from env var only (`sync-louisiana.js`, `sync-ally.js`) | CLEAN |
| Webhook security | `/api/webhook` accepts ANY POST with no authentication or signature verification | **HIGH** (counted above) |
| Webhook abuse | Anyone can POST fake call data to `https://louisianaai.net/api/webhook`, triggering email notifications and Brevo CRM entries | See API section |

---

## 5. BREVO

| Check | Result | Rating |
|-------|--------|--------|
| API key in deployed files | Not exposed | CLEAN |
| API key in source code | Server-side only (`process.env.BREVO_API_KEY`) | CLEAN |
| Email lists accessible | Brevo stats exposed via `/api/registrations` GET (no auth) | See API section |

---

## 6. HEYGEN

| Check | Result | Rating |
|-------|--------|--------|
| API key in deployed HTML/JS | Not found in any deployed file | CLEAN |
| API key in source code | Loaded from env var only in `scripts/ai_daily_omniverse.py` | CLEAN |

---

## 7. RUNPOD

| Check | Result | Rating |
|-------|--------|--------|
| API key in deployed HTML/JS | Not found (placeholder `rp_...` only) | CLEAN |
| API key in current source | Loaded from env var only | CLEAN |
| API key in git history | **EXPOSED in public git history** (commit `1373e4c`) | **CRITICAL** (counted above) |

---

## 8. NVIDIA BUILD API KEY

| Check | Result | Rating |
|-------|--------|--------|
| NGC CLI API key in deployed files | Not found | CLEAN |
| NGC CLI API key in source | Loaded from env var only | CLEAN |
| NGC key in git history | Not found | CLEAN |

---

## ADDITIONAL FINDINGS

### investor-neocloud page (adc3k.com)
- Publicly accessible at `https://adc3k.com/investor-neocloud`
- Contains button linking to `/alumni-investors` gate
- Page itself has financial projections and business model details visible without authentication
- Rating: **MEDIUM** — consider whether this should be gated

### /ops page (adc3k.com)
- Returns the main SPA (rewrites catch-all) — the actual Mission Control dashboard runs on localhost:8000, not on adc3k.com
- Rating: CLEAN

### CORS
- Both adc3k.com and louisianaai.net return `Access-Control-Allow-Origin: *` (Vercel default)
- Rating: MEDIUM for louisianaai.net (has API endpoints that could be called cross-origin)

### FormSubmit.co
- Email address `info@louisianaai.net` is visible in source code (form action and webhook.js)
- This is expected for FormSubmit but means the address is harvestable
- Rating: LOW (unavoidable with FormSubmit)

---

## IMMEDIATE ACTIONS REQUIRED

### CRITICAL — Do Today

1. **Rotate RunPod API key immediately.**
   - The key `rpa_G1QWM...` is in public git history (commit `1373e4c`).
   - Go to runpod.io > Settings > API Keys > regenerate.
   - Update `.env` with the new key.
   - GitHub push protection caught it on push, but the commit with the key still exists in history.

2. **Add authentication to `/api/registrations` endpoint.**
   - This endpoint exposes all registrant PII (names, emails, organizations) to anyone on the internet.
   - Minimum fix: require a secret query parameter or header (e.g., `?key=<MC_API_KEY>`).
   - Better fix: move to Supabase/database with proper auth.

### HIGH — This Week

3. **Add webhook signature verification to `/api/webhook`.**
   - Bland.ai supports webhook signing. Verify the signature on incoming requests.
   - Without this, anyone can send fake call data that pollutes CRM and triggers emails.

4. **Add rate limiting or auth to `/api/process-registration`.**
   - Currently anyone can trigger unlimited registration emails to arbitrary addresses.
   - This can burn Brevo credits and damage sender reputation (spam complaints).
   - Minimum: add CAPTCHA or rate limit. Better: require a token from the form submission.

5. **Add auth or rate limiting to `/api/brevo-sync`.**
   - Same issue — unauthenticated endpoint that writes to CRM.

### MEDIUM — This Sprint

6. **Add CSP header to louisianaai.net.**
   - `adc3k.com` and `mission-control-hd.com` both have CSP. `louisianaai.net` does not.
   - Add to `louisianaai-site/vercel.json` headers array.

7. **Consider gating investor-neocloud page.**
   - Financial projections and business model are publicly accessible.
   - Either gate behind `/alumni-investors` or accept the risk if it's intentional.

8. **Restrict CORS on louisianaai.net.**
   - `Access-Control-Allow-Origin: *` combined with unauthenticated POST endpoints means any website can make API calls to your endpoints.

### LOW — When Convenient

9. **Add robots.txt to adc3k.com and louisianaai.net.**
   - Prevents search engines from indexing internal pages (e.g., `/ops`, `/ai-ops`).

10. **Consider making the GitHub repo private** or use `git filter-repo` to remove the RunPod key from history.
    - Even after rotating the key, the old key in history confirms the repo has infrastructure secrets.
    - A private repo eliminates this entire attack surface.

---

## SERVICES STATUS SUMMARY

| Service | Key Secure | Endpoints Secure | Overall |
|---------|-----------|-----------------|---------|
| Anthropic (Claude) | CLEAN | N/A | CLEAN |
| Notion | CLEAN | N/A | CLEAN |
| RunPod | **CRITICAL** (in git history) | N/A | CRITICAL |
| Bland.ai | CLEAN | HIGH (no webhook auth) | HIGH |
| Brevo | CLEAN | HIGH (unauthed CRM sync) | HIGH |
| HeyGen | CLEAN | N/A | CLEAN |
| ElevenLabs | CLEAN | N/A | CLEAN |
| Pexels | CLEAN | N/A | CLEAN |
| NVIDIA NGC | CLEAN | N/A | CLEAN |
| FormSubmit | N/A | CLEAN | CLEAN |

---

*Audit complete. 2 CRITICAL, 3 HIGH, 3 MEDIUM, 2 LOW findings. Priority: rotate RunPod key and lock down /api/registrations today.*
