# Mission Control HD — Full Codebase Audit
**Date:** 2026-03-24
**Repo:** C:\Users\adhsc\mission-control
**Branch:** main (clean, up to date with origin)

---

## 1. Summary Stats

| Metric | Count |
|--------|-------|
| Total source files (src + artifacts + emails) | 117 |
| Lines of code (JS/JSX/CSS/HTML/SQL) | ~5,010 |
| Git commits | 11 |
| Next.js pages/routes | 63 |
| API routes | 5 |
| Artifact tool files | 41 |
| Email templates | 6 |
| Supabase tables | 9 |
| Components | 4 |
| Env vars configured | 13 |

---

## 2. Tech Stack

- **Framework:** Next.js 15.1 (App Router)
- **React:** 19.0
- **Styling:** Tailwind CSS 3.4 + custom design system (globals.css)
- **Auth:** Supabase (SSR client, PKCE flow, magic link, OAuth Google/GitHub, password reset)
- **Database:** Supabase (PostgreSQL) — 9 tables, 22 RLS policies, 5 triggers, 3 views, 3 functions
- **Payments:** Stripe (checkout sessions, webhooks, 4 price IDs)
- **AI Chat:** Anthropic Claude (claude-sonnet-4-20250514, 5 platform-specific system prompts)
- **Email Marketing:** Kit (ConvertKit) integration stub
- **Deployment:** Vercel (iad1 region), daily health cron
- **Security:** CSP, X-Frame-Options DENY, X-Content-Type-Options, XSS-Protection, Referrer-Policy, Permissions-Policy, `poweredByHeader: false`

---

## 3. The 5 Vehicle Platforms & 41 Tools

### Harley-Davidson (7 tools)
1. DTC Database (`/harley/dtc`)
2. Diagnostic Flowcharts (`/harley/flowcharts`)
3. Service Reference (`/harley/service`)
4. Common Problems (`/harley/problems`)
5. Wiring Diagrams (`/harley/wiring`) — **PRO gated**
6. Torque Sequences (`/harley/torque`) — **PRO gated**
7. Morning Brief (`/harley/morning-brief`)

### Automotive (5 tools)
8. DTC Database (`/auto/dtc`)
9. Diagnostic Flowcharts (`/auto/flowcharts`)
10. Recalls & TSBs (`/auto/recalls`)
11. Fluid Color Guide (`/auto/fluid-guide`)
12. Morning Brief (`/auto/morning-brief`)

### Trucking (7 tools)
13. HOS Tracker (`/trucking/hos`)
14. Pre-Trip Checklist (`/trucking/pretrip`)
15. Profit Calculator (`/trucking/profit`)
16. IFTA Generator (`/trucking/ifta`)
17. Axle Weight Calculator (`/trucking/axle-weight`)
18. Calculator Suite (`/trucking/calculators`)
19. Morning Brief (`/trucking/morning-brief`)

### E-Bike (7 tools)
20. Error Codes (`/ebike/errors`)
21. Diagnostic Flowcharts (`/ebike/flowcharts`)
22. Battery & Range Calculator (`/ebike/battery`)
23. Class & Law Reference (`/ebike/laws`)
24. Wiring Diagrams (`/ebike/wiring`) — **PRO gated**
25. Build Calculator (`/ebike/build`)
26. Morning Brief (`/ebike/morning-brief`)

### Scooter (5 tools)
27. Error Codes (`/scooter/errors`)
28. Diagnostic Flowcharts (`/scooter/flowcharts`)
29. Maintenance Guide (`/scooter/maintenance`)
30. Comparison Calculator (`/scooter/compare`)
31. Morning Brief (`/scooter/morning-brief`)

### Universal Tools (10 tools)
32. Parts Locator (`/tools/parts`)
33. Unit Converter (`/tools/converter`)
34. Fuel Log Tracker (`/tools/fuel-log`)
35. Tire Size Calculator (`/tools/tire-calc`)
36. Maintenance Cost Estimator (`/tools/maintenance-cost`)
37. Fuel Economy Calculator (`/tools/fuel-economy`)
38. OBD Live Data Reference (`/tools/obd-reference`)
39. Emergency Roadside Guide (`/tools/emergency`)
40. Maintenance Schedule Builder (`/tools/schedule-builder`)
41. Service History Export (`/tools/service-export`) — **PRO gated**

### Plus (not counted in 41)
- AI Diagnostic Chat (`/ai-chat`) — free tier: 3/day, premium: 20/day, pro: unlimited

---

## 4. All Pages & Routes

### Core Pages
- `/` — Landing page (hero, platform tabs, features, testimonials, pricing preview, email capture, footer)
- `/login` — Sign in / Sign up / Magic link / Forgot password / Reset password
- `/onboarding` — 4-step wizard (platform select, add vehicle, preferences, launch)
- `/dashboard` — Main hub with sidebar nav, search, platform filter, tool grid
- `/pricing` — Full pricing page with comparison table, FAQ, Stripe checkout
- `/account` — Profile, subscription, vehicles, preferences tabs
- `/garage` — Vehicle management, service history
- `/ai-chat` — AI diagnostic chat with platform selector, suggested prompts, conversation history
- `/blog` — 10 hardcoded articles, platform filters, article reader
- `/community` — Forum with 8 mock threads, upvotes, new thread form, platform filter

### API Routes
- `POST /api/ai-chat` — Claude chat endpoint (IP rate limit: 10/min, history: last 10 msgs)
- `POST /api/email-signup` — Email capture to Supabase + Kit (30s IP cooldown)
- `POST /api/stripe/checkout` — Create Stripe checkout session (4 price IDs, promo code support)
- `POST /api/stripe/webhook` — Handles checkout.session.completed, subscription.updated, subscription.deleted, invoice.payment_failed
- `GET /api/health` — Service health check (runs daily via Vercel cron)

---

## 5. Stripe Checkout Flow (End to End)

1. User clicks "Start 7-Day Free Trial" or "Upgrade to Pro" on `/pricing`
2. `handleCheckout()` checks Supabase session — if not logged in, redirects to `/login?redirect=/pricing`
3. `POST /api/stripe/checkout` with `{ tier, interval, userId, email }`
4. Server validates tier/interval, looks up Stripe price ID from env vars
5. Creates Stripe Checkout Session with:
   - `mode: 'subscription'`
   - 7-day trial on Premium monthly only
   - `allow_promotion_codes: true`
   - `metadata: { userId, tier, interval }`
   - Success URL: `/account?checkout=success&session_id={CHECKOUT_SESSION_ID}`
   - Cancel URL: `/pricing?checkout=cancelled`
6. Client redirects to `session.url` (Stripe hosted checkout)
7. On success, Stripe fires `checkout.session.completed` webhook
8. Webhook handler uses admin Supabase client (bypasses RLS) to update `profiles` table with `tier`, `stripe_customer_id`, `stripe_subscription_id`
9. Subsequent webhook events handle upgrades/downgrades/cancellations/payment failures

**Pricing:**
- Free: $0 (3 AI/day, 1 vehicle)
- Premium: $9.99/mo or $7.99/mo annual ($95.88/yr) — 7-day trial on monthly
- Pro: $19.99/mo or $15.99/mo annual ($191.88/yr)

---

## 6. Auth Flow (End to End)

1. **Middleware** (`src/middleware.js`) runs on all routes except static/API
   - Protected routes (`/dashboard`, `/garage`, `/ai-chat`, `/account`, `/onboarding`): redirect to `/login?redirect=...` if no user
   - Guest-only routes (`/login`): redirect to `/dashboard` if already logged in
   - Supabase SSR cookie-based session refresh
2. **Login options:**
   - Email/password (sign in + sign up)
   - OAuth (Google, GitHub)
   - Magic link (OTP)
   - Forgot password -> email reset link -> set new password
3. **AuthProvider** (React context) wraps entire app via `layout.jsx`
   - Fetches user + profile on mount
   - Listens for `onAuthStateChange`
   - Exposes `{ user, profile, tier, loading, signOut, supabase }`
4. **Profile auto-creation**: Supabase trigger `handle_new_user()` creates profile row on `auth.users` INSERT
5. **Tier gating**: `ProGate` component wraps premium/pro content — shows blurred preview + upgrade modal
6. **Onboarding**: After signup, redirects to `/onboarding` (4-step wizard)

---

## 7. AI Chat Integration

- **SDK:** `@anthropic-ai/sdk` v0.39.0
- **Model:** `claude-sonnet-4-20250514`
- **Max tokens:** 1,024 per response
- **5 system prompts:** Platform-specific expert personas (Harley, Auto, Trucking, E-Bike, Scooter)
- **History:** Sends last 10 messages for context, truncated to 2,000 chars each
- **Rate limiting:** In-memory IP-based (10 requests/minute), cleanup every 5 min
- **User-facing rate limits:** Defined in constants (3/day free, 20/day premium, unlimited pro) — **BUT**: the API route does NOT enforce per-user daily limits. Only IP rate limiting is active server-side. The Supabase `checkAIRateLimit()` function exists in `lib/supabase.js` and the DB has `ai_chat_usage` table + `check_ai_rate_limit()` SQL function, but the API route never calls them.
- **Response includes:** `reply`, `platform`, `tokens.input`, `tokens.output`, `latencyMs`

---

## 8. Supabase Schema

9 tables, all with RLS enabled:

| Table | Purpose | RLS Policies |
|-------|---------|--------------|
| profiles | User profiles, tier, Stripe IDs, preferences | 3 (select/update/insert own) |
| vehicles | User vehicles (platform, make, model, VIN) | 4 (CRUD own) |
| service_records | Maintenance/service history per vehicle | 4 (CRUD own) |
| fuel_logs | Gas fill-up tracking | 3 (select/insert/delete own) |
| forum_threads | Community forum posts | 3 (public read, auth create, author update) |
| forum_replies | Thread replies (nested via parent_reply_id) | 3 (public read, auth create, author update) |
| upvotes | Thread/reply upvotes (unique constraints) | 3 (view/insert/delete own) |
| email_signups | Landing page email captures | 0 (service role only) |
| ai_chat_usage | Per-user AI query tracking | 2 (view/insert own) |

3 views: `forum_threads_with_author`, `forum_replies_with_author`, `ai_chat_daily_usage`
3 SQL functions: `can_add_vehicle()`, `check_ai_rate_limit()`, `calculate_mpg()`
5 triggers: auto-create profile, updated_at timestamps, reply count sync, upvote count sync

---

## 9. What's Working

- Landing page with email capture and platform tabs
- Full auth flow (email, OAuth, magic link, password reset)
- Onboarding wizard
- Dashboard with sidebar nav, search, platform filters
- All 41 tool pages render (migrated from artifacts via `migrate.js`)
- AI chat with 5 platform-specific expert modes
- Pricing page with comparison table, FAQ, Stripe checkout
- Account page with profile/subscription/vehicles/preferences tabs
- Vehicle garage with service history display
- Blog with 10 articles and article reader
- Community forum with threads, upvotes, platform filters
- ProGate component (blurred content + upgrade modal)
- Stripe webhook handler (checkout, subscription updates, cancellation, payment failures)
- Email signup API with cooldown
- Health check endpoint with Vercel cron
- Security headers (CSP, HSTS, etc.)
- Supabase schema with full RLS
- 6 email templates ready for Kit/ConvertKit

---

## 10. What's Broken or Missing

### Critical
1. **AI rate limiting per user NOT enforced** — The `checkAIRateLimit()` function exists in `lib/supabase.js` and the SQL function exists in the schema, but the `/api/ai-chat` route never checks per-user daily limits. Anyone can exceed their tier's daily AI quota. Only IP-based rate limiting (10/min) is active.
2. **AI chat usage NOT logged** — The `ai_chat_usage` table exists but the API never writes to it. No usage tracking.
3. **Garage is client-side only** — Uses `useState` with mock data (`MOCK_VEHICLES`). Vehicles, service records, and fuel logs are NOT persisted to Supabase. The "Add Vehicle" and "Add Service" buttons work in-memory only.
4. **Community forum is mock data** — `MOCK_THREADS` array. New thread form has UI but no backend. Upvotes are client-side only. No Supabase reads/writes despite the schema being ready.
5. **Blog is hardcoded** — 10 articles stored as a JS array in the component. No CMS, no Supabase, no markdown files.
6. **Account "Save Changes" button is non-functional** — Profile updates and preference saves do nothing (no Supabase write).
7. **Kit/ConvertKit form ID is placeholder** — `YOUR_FORM_ID` literal in email-signup route. Email marketing integration is broken.

### Important
8. **Onboarding doesn't save to Supabase** — The wizard collects platform preferences and vehicle data but `handleFinish()` just redirects to `/dashboard` without persisting.
9. **No `og-image.png`** — Referenced in layout metadata but missing from `/public`.
10. **No `apple-touch-icon.png`** or `site.webmanifest** — Referenced but missing from `/public`.
11. **Morning Brief emails** — Templates exist but no send logic. No cron job, no email provider integration.
12. **Service History Export** — PRO-gated but the tool page doesn't appear to have actual export functionality (CSV/PDF).
13. **Tool pages are minified/compressed** — All 41 tools were migrated via `migrate.js` and are single-line minified JSX with hardcoded data arrays. No external data sources.
14. **No test suite** — Zero tests. No testing framework in devDependencies.
15. **Two layout files** — Both `layout.js` (Next.js default) and `layout.jsx` (custom) exist in `src/app/`. The `.jsx` takes precedence but the `.js` is dead code.
16. **Two PostCSS configs** — Both `postcss.config.js` and `postcss.config.mjs` at root.
17. **Two Next configs** — Both `next.config.js` and `next.config.mjs` at root.
18. **`MC_Files/` directory** — Contains all original source files before migration. Entire dev history/backup. Could be .gitignored.

### Nice to Have
19. **No search indexing for tools** — Tool search on dashboard is name/section only, not content-aware.
20. **No PWA support** — Manifest referenced but missing.
21. **No analytics** — No GA, Plausible, PostHog, or any tracking.
22. **No error boundary** — `error.jsx` exists but is minimal.
23. **No loading states on protected routes** — AuthProvider `loading` state is available but pages don't show skeletons during auth check.
24. **Platform index pages missing** — `/harley`, `/auto`, `/trucking`, `/ebike`, `/scooter` routes are referenced in constants but don't have `page.jsx` files. They would 404.

---

## 11. Email Templates

6 HTML templates in `/emails/`:
1. `email_welcome.html` — Post-signup welcome (3 steps: dashboard, AI chat, add vehicle)
2. `email_launch_teaser.html` — Pre-launch teaser
3. `email_launch_day.html` — Launch day announcement
4. `email_launch_followup.html` — Follow-up after launch
5. `email_morning_brief.html` — Daily/weekly morning brief template
6. `email_upgrade_nudge.html` — Upgrade prompt for free users

All use inline CSS, dark theme matching the app. `{{unsubscribe}}` placeholders for Kit. **No send infrastructure wired up.**

---

## 12. Environment Variables

```
ANTHROPIC_API_KEY=         # Claude API
KIT_API_KEY=               # ConvertKit (has placeholder form ID)
NEXT_PUBLIC_SITE_URL=      # Base URL
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=  # Stripe public key
NEXT_PUBLIC_SUPABASE_URL=  # Supabase project URL
NEXT_PUBLIC_SUPABASE_ANON_KEY=       # Supabase anon key
STRIPE_PREMIUM_MONTHLY_PRICE_ID=     # Stripe price IDs (4)
STRIPE_PREMIUM_ANNUAL_PRICE_ID=
STRIPE_PRO_MONTHLY_PRICE_ID=
STRIPE_PRO_ANNUAL_PRICE_ID=
STRIPE_SECRET_KEY=         # Stripe secret
STRIPE_WEBHOOK_SECRET=     # Stripe webhook signing
SUPABASE_SERVICE_ROLE_KEY= # Supabase admin (bypasses RLS)
```

---

## 13. Design System

Dark theme built on Tailwind with custom CSS variables:
- **Background:** #0A0A0B, **Surface:** #111113, **Border:** #1E1E21
- **Platform colors:** Harley #E8720E, Auto #8B5CF6, Trucking #FF6F00, E-Bike #22C55E, Scooter #06B6D4
- **Tier colors:** Premium #8B5CF6 (purple), Pro #F59E0B (amber)
- **Fonts:** Outfit (sans), JetBrains Mono (mono)
- **Component classes:** `.mc-card`, `.mc-card-hover`, `.mc-btn-primary/-secondary/-ghost`, `.mc-input`, `.mc-badge`, `.mc-skeleton`
- **Border radius:** Custom `rounded-mc` token
- **Animations:** shimmer (skeletons), fade-in, slide-down, bounce (typing indicator)

---

## 14. Improvement Recommendations

### Priority 1 — Fix broken core features
1. **Wire up per-user AI rate limiting** — Call `checkAIRateLimit()` in the API route, write to `ai_chat_usage` table
2. **Connect Garage to Supabase** — Replace mock data with real CRUD operations
3. **Connect Community to Supabase** — Forum threads/replies/upvotes are schema-ready
4. **Wire up Account Save** — Profile updates and preference changes
5. **Wire up Onboarding Save** — Persist platform selections and first vehicle
6. **Fix Kit form ID** — Replace `YOUR_FORM_ID` with actual ConvertKit form

### Priority 2 — Complete the product
7. **Add platform index pages** — `/harley`, `/auto`, etc. need `page.jsx` files
8. **Build Morning Brief cron** — Use Vercel cron + Resend/SES to send templates
9. **Add missing PWA assets** — `og-image.png`, `apple-touch-icon.png`, `site.webmanifest`
10. **Clean up dead files** — Remove duplicate configs (`layout.js`, `postcss.config.mjs`, `next.config.mjs`)
11. **Move MC_Files to .gitignore** — It's a dev backup, not needed in production

### Priority 3 — Scale & polish
12. **Add analytics** — PostHog or Plausible for usage tracking
13. **Add tests** — At minimum, API route tests with vitest
14. **Blog CMS** — Move articles to markdown files or Supabase
15. **Expand tool data** — Current tools have small hardcoded data arrays (10-20 items each). DTC databases should have hundreds of codes.
16. **Streaming AI responses** — Current implementation waits for full response. Add SSE streaming for better UX.
17. **Stripe Customer Portal** — Add link to manage/cancel subscription without custom UI
18. **Image generation for blog/tools** — OG images, tool screenshots

---

## 15. ADC Ecosystem Connection

Mission Control HD fits ADC's broader ecosystem in several ways:

- **AI Advantage installer model** — This is a template SaaS product that could be white-labeled or sold through the AI Advantage SMB business (ai-advantage.info). The vehicle niche is proven (Harley riders, truckers, fleet managers), and the freemium + Stripe model is ready.
- **Proof of concept for Claude integration** — The Anthropic SDK integration with platform-specific system prompts demonstrates the same pattern used in ADC's Mission Control agent system. Could share prompting patterns.
- **Revenue diversification** — Even at modest scale (1,000 paying users), this generates $10-20K/mo MRR with near-zero infrastructure cost (Vercel + Supabase free tier covers a lot).
- **Workforce demo** — Shows ADC can ship production SaaS, not just infrastructure. Useful for NVIDIA partnership credibility.
- **Kit/email list** — The email capture pipeline (once Kit form ID is fixed) builds a direct audience for ADC announcements, Ground Zero YouTube, or Louisiana AI Initiative awareness.

---

## 16. Git History

```
fb6a988 Fix: password reset now works, add redirect support
5f48ba0 Fix: pass userId and email to Stripe checkout
1141e5f redeploy with live price IDs
fd1e6bd redeploy with live stripe keys
ff7ba2a add forgot password to login page
6f9ee19 fix syntax errors in 7 minified tool pages
c1eeee5 fix supabase auth lock timeout
2479be9 migrate 41 tools to routes
4a2ee49 remove duplicate page
9697464 fix vercel config
5292500 first commit
```

Working tree: **clean** (no uncommitted changes)

---

*Audit complete. 117 files, 5,010 lines of code, 41 tools across 5 platforms. Core infrastructure (auth, payments, AI chat) is solid. Main gaps: Supabase data persistence for garage/community/account, per-user AI rate limiting, and Kit email integration.*
