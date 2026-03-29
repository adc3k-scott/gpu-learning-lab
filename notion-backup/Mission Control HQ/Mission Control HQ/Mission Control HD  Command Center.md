# Mission Control HD — Command Center
*Notion backup — 2026-03-28*

> Live SaaS at missioncontrolhd.com — vehicle diagnostics platform with AI chat, 41 tools, Stripe subscriptions, and Supabase auth. Next.js 15 + Vercel.
---
## Quick Links
- Live site: https://missioncontrolhd.com
- GitHub: https://github.com/Scottay007/mission-control
- Vercel: mc-vehicle-app2 (Mission Control Pro team)
- Supabase: Mission Control project — us-west-2
- Stripe: dashboard.stripe.com (LIVE mode)
- Local code: C:\Users\adhsc\mission-control
---
## Sub-Pages
- Project Overview & Tech Stack
- Stripe & Payments Config
- Infrastructure & Auth Config
- Launch Roadmap & Open Issues
- Session Log
*[Child: Project Overview & Tech Stack]*
# Mission Control HD — Project Overview
> Vehicle diagnostics SaaS. All 41 tools are free. Premium and Pro unlock more AI, vehicles, and wiring/torque PRO tools.
---
## Tech Stack
  - Next.js 15 (App Router) — frontend + API routes
  - Supabase — Auth, Postgres database, Row Level Security
  - Stripe — subscriptions, webhooks (LIVE mode)
  - Anthropic Claude API — AI Diagnostic Chat
  - Vercel — hosting, serverless functions, edge
  - Kit / ConvertKit — email marketing automation
  - Tailwind CSS — dark theme, custom colors
  - Namecheap — domain registration, auto-renew ON
---
## Vehicle Platforms
  - Harley-Davidson (#E8720E) — 7 tools
  - Automotive (#8B5CF6) — 5 tools
  - Trucking (#FF6F00) — 7 tools
  - E-Bike (#22C55E) — 7 tools
  - Scooter (#06B6D4) — 5 tools
  - Universal — 10 tools
  - Total: 41 tools
---
## Pricing Tiers
  - Free — $0 | 3 AI queries/day | 1 vehicle
  - Premium — $9.99/mo ($95.88/yr) | 20 AI queries/day | 3 vehicles | 7-day free trial
  - Pro — $19.99/mo ($191.88/yr) | Unlimited AI | Unlimited vehicles | PRO-gated tools
---
## PRO-Gated Tools
  - HD_Wiring_Reference_v2
  - HD_Torque_Sequences_v2
  - EBike_Wiring_Reference_v2
  - Service_History_Export_v2
---
## Database Schema (Supabase)
  - profiles — user tier, stripe_customer_id, stripe_subscription_id
  - vehicles — user garage entries
  - chat_history — AI diagnostic sessions
  - community_posts — forum posts
  - community_comments — forum replies
  - email_signups — Kit integration
RLS enabled on all tables. Auto-profile trigger fires on signup. Email confirm ON.
---
## Accounts & Access
  - GitHub: Scottay007 — github.com/Scottay007/mission-control
  - Vercel: via GitHub — mc-vehicle-app2
  - Supabase: adhscott@yahoo.com — onvemzmhedyuropiruaf.supabase.co
  - Stripe: adhscott@yahoo.com — LIVE mode
  - Anthropic: adhscott@yahoo.com — console.anthropic.com
  - Kit: adhscott@yahoo.com — app.kit.com
  - Namecheap: Scottay007 — missioncontrolhd.com (expires Feb 23 2027)
*[Child: Stripe & Payments Config]*
# Stripe & Payments Configuration
> Stripe is in LIVE mode as of March 2026. Test mode keys are archived. Do NOT use test price IDs in production.
---
## Live Price IDs
  - Premium Monthly: price_1T2Nbc2a0QlcXNBji9gMD9cW
  - Premium Annual: price_1T2Nd42a0QlcXNBjlG3I0f5M
  - Pro Monthly: price_1T3oMt2a0QlcXNBj8538mT9A
  - Pro Annual: price_1T3oOg2a0QlcXNBj1UmvhyQ0
Archived: Mission Control Shop ($49.99/mo, $499/yr) — do not reactivate.
---
## Webhook Configuration
  - Required endpoint: https://missioncontrolhd.com/api/stripe/webhook
  - Events: checkout.session.completed, customer.subscription.updated, customer.subscription.deleted
  - Signing secret env var: STRIPE_WEBHOOK_SECRET
> OPEN ISSUE: Live mode webhook may not be configured yet. Old test webhook (fascinating-breeze) pointed to mc-vehicle-app2.vercel.app. Create a NEW live mode webhook in Stripe dashboard pointing to https://missioncontrolhd.com/api/stripe/webhook, then update STRIPE_WEBHOOK_SECRET in Vercel.
---
## Vercel Environment Variables — Stripe
  - STRIPE_SECRET_KEY — live sk_live_ key
  - NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY — live pk_live_ key
  - STRIPE_WEBHOOK_SECRET — whsec_ signing secret from live webhook
  - STRIPE_PREMIUM_MONTHLY_PRICE_ID — price_1T2Nbc2a0QlcXNBji9gMD9cW
  - STRIPE_PREMIUM_ANNUAL_PRICE_ID — price_1T2Nd42a0QlcXNBjlG3I0f5M
  - STRIPE_PRO_MONTHLY_PRICE_ID — price_1T3oMt2a0QlcXNBj8538mT9A
  - STRIPE_PRO_ANNUAL_PRICE_ID — price_1T3oOg2a0QlcXNBj1UmvhyQ0
---
## Checkout Flow
  - User clicks tier button on /pricing → handleCheckout(tier) fires
  - POST /api/stripe/checkout — creates Stripe Checkout Session with userId + tier in metadata
  - User completes payment on Stripe-hosted page
  - Stripe fires checkout.session.completed webhook
  - Webhook updates profiles table: tier, stripe_customer_id, stripe_subscription_id
  - Premium monthly: 7-day free trial automatically applied
---
## Annual Pricing
  - Premium Annual: $95.88/yr (equiv $7.99/mo — 20% off)
  - Pro Annual: $191.88/yr (equiv $15.99/mo — 20% off)
*[Child: Infrastructure & Auth Config]*
# Infrastructure & Auth Configuration
---
## Vercel
  - Project: mc-vehicle-app2 (Mission Control Pro team)
  - Region: iad1 (US East)
  - Live URL: https://missioncontrolhd.com
  - Old URL still works: https://mc-vehicle-app2.vercel.app
  - Health cron: /api/health runs daily at 12:00 UTC
To add/change env vars: Vercel dashboard → mc-vehicle-app2 → Settings → Environment Variables
---
## All Vercel Environment Variables
  - NEXT_PUBLIC_SITE_URL = https://missioncontrolhd.com
  - ANTHROPIC_API_KEY = sk-ant-... (set)
  - NEXT_PUBLIC_SUPABASE_URL = https://onvemzmhedyuropiruaf.supabase.co
  - NEXT_PUBLIC_SUPABASE_ANON_KEY = (set)
  - SUPABASE_SERVICE_ROLE_KEY = (set)
  - STRIPE_SECRET_KEY = sk_live_... (set)
  - NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY = pk_live_... (set)
  - STRIPE_WEBHOOK_SECRET = whsec_... (set — verify matches live webhook)
  - STRIPE_PREMIUM_MONTHLY_PRICE_ID = price_1T2Nbc2a0QlcXNBji9gMD9cW
  - STRIPE_PREMIUM_ANNUAL_PRICE_ID = price_1T2Nd42a0QlcXNBjlG3I0f5M
  - STRIPE_PRO_MONTHLY_PRICE_ID = price_1T3oMt2a0QlcXNBj8538mT9A
  - STRIPE_PRO_ANNUAL_PRICE_ID = price_1T3oOg2a0QlcXNBj1UmvhyQ0
  - KIT_API_KEY = (set)
> Local .env.local has wrong values from earlier sessions. Always use Vercel dashboard for production values.
---
## Supabase
  - Project: Mission Control (us-west-2, Oregon)
  - URL: https://onvemzmhedyuropiruaf.supabase.co
  - Auth: email/password, confirm email ON
> OPEN ISSUE: Supabase auth redirect URLs still pointing to old vercel.app domain. Go to Supabase → Authentication → URL Configuration → Set Site URL to https://missioncontrolhd.com and add https://missioncontrolhd.com/** to Redirect URLs.
---
## Domain & DNS (Namecheap)
  - Domain: missioncontrolhd.com
  - Registrar: Namecheap — Scottay007 account
  - Expires: Feb 23, 2027 — auto-renew ON
  - A Record: @ → 76.76.21.21
  - CNAME: www → 4211f3971db6198f.vercel-dns-016.com
---
## Key File Locations (local)
  - src/app/api/stripe/webhook/route.js — webhook handler
  - src/app/api/stripe/checkout/route.js — checkout session creator
  - src/app/pricing/page.jsx — pricing + checkout buttons
  - src/app/login/page.jsx — login + forgot password
  - src/lib/supabase.js — browser + admin clients
  - src/lib/constants.js — TIERS definition
  - artifacts/ — 41 tool source components
  - emails/ — 6 HTML email templates
*[Child: Launch Roadmap & Open Issues]*
# Launch Roadmap & Open Issues
> Site is LIVE. Most critical bugs are fixed. Remaining items are config tasks (Stripe webhook, Supabase URLs) and launch prep.
---
## Critical — Fix Before Marketing Push
  - [OPEN] Stripe live mode webhook — create at https://missioncontrolhd.com/api/stripe/webhook, update STRIPE_WEBHOOK_SECRET in Vercel
  - [OPEN] Supabase auth redirect URLs — update Site URL + add missioncontrolhd.com/** in Supabase Authentication settings
  - [VERIFY] Premium ($9.99) button — likely fixed by auth lock fix (c1eeee5), needs live test
  - [OPEN] Account page email field blank — email shows empty on profile page
---
## Medium Priority
  - Stripe webhook URL update — verify Vercel forwards correctly or update endpoint to missioncontrolhd.com
  - GitHub OAuth for production — set callback URL to missioncontrolhd.com
  - Google OAuth for production — set callback URL to missioncontrolhd.com
  - Supabase custom SMTP — switch from default to Resend
  - Supabase auth email templates — customize signup, reset password emails
---
## Launch Prep
  - OG images and app icons
  - Blog posts — 5 written, need adding to /blog page
  - Kit email automation sequences — morning briefs for Premium
  - ProductHunt launch
  - Reddit post (r/webdev, r/SaaS, r/Harley, r/ebike)
  - Social media (TikTok, Instagram, X/Twitter, LinkedIn)
---
## Completed (as of March 2026)
  - [DONE] Build error in harley/flowcharts/page.jsx — fixed in 6f9ee19
  - [DONE] Forgot password / password reset — fixed in ff7ba2a + fb6a988
  - [DONE] Stripe userId not passed to checkout — fixed in 5f48ba0
  - [DONE] Moved to live Stripe keys — fd1e6bd + 1141e5f
  - [DONE] Supabase auth lock timeout — fixed in c1eeee5
  - [DONE] Custom domain missioncontrolhd.com — live
  - [DONE] All 41 tools migrated to routes
  - [DONE] Stripe Pro checkout working end-to-end
---
## Git Quick Reference
Push changes to production:
  - cd C:\Users\adhsc\mission-control
  - git add .
  - git commit -m "describe change"
  - git push
Run locally: npm run dev → http://localhost:3000
---
> CRITICAL FIX CHECKLIST (2026-03-23)
Scott — do these 2 things to unblock MCHD launch:
## Fix 1: Stripe Webhook (5 minutes)
  1. Go to https://dashboard.stripe.com/webhooks
  1. Click 'Add endpoint'
  1. URL: https://missioncontrolhd.com/api/stripe/webhook
  1. Events to listen for: checkout.session.completed, customer.subscription.created, customer.subscription.updated, customer.subscription.deleted, invoice.payment_succeeded, invoice.payment_failed
  1. Copy the webhook signing secret (whsec_...)
  1. Go to Vercel Dashboard → mc-vehicle-app2 → Settings → Environment Variables
  1. Set STRIPE_WEBHOOK_SECRET = the whsec_ value you copied
  1. Redeploy (Vercel → Deployments → Redeploy latest)
## Fix 2: Supabase Redirect URLs (3 minutes)
  1. Go to https://supabase.com/dashboard → your project → Authentication → URL Configuration
  1. Change Site URL to: https://missioncontrolhd.com
  1. Add to Redirect URLs: https://missioncontrolhd.com/**, https://missioncontrolhd.com/auth/callback
  1. Remove any old vercel.app URLs (mc-vehicle-app2.vercel.app)
  1. Save
## Fix 3: Verify Premium Button (2 minutes)
After fixes 1 and 2, go to missioncontrolhd.com, sign up, click Premium, verify Stripe checkout loads.
## Fix 4: Account Page Email (investigate)
The account page reads email from user?.email (Supabase auth session). If email shows blank, the likely cause is the Supabase redirect URL issue (Fix 2) — the session is not persisting correctly on the custom domain. Fix 2 should resolve this. If email is still blank after Fix 2, check Supabase → Authentication → Users to confirm the email is stored.
---
Total time: ~10 minutes. Then MCHD is launch-ready.
Code verified: webhook handler at src/app/api/stripe/webhook/route.js handles all required events correctly. No old vercel.app URLs found in source code. The blockers are purely dashboard configuration.
*[Child: Session Log]*
# Mission Control HD — Session Log
Track what was done each work session.
---
## Session 3 — Feb 23, 2026
  - Custom domain missioncontrolhd.com purchased and connected
  - NEXT_PUBLIC_SITE_URL updated to https://missioncontrolhd.com
  - STRIPE_WEBHOOK_SECRET rolled to new secret
  - Supabase auth lock timeout fixed (lock: { enabled: false })
  - All 44 dashboard tools verified visible and clickable
  - Stripe Pro checkout tested end-to-end — payment succeeds
  - Claude AI diagnostic chat tested — working
---
## Session 4 — March 2026
  - Moved to live Stripe keys (fd1e6bd, 1141e5f)
  - Fixed: build error in harley/flowcharts/page.jsx (6f9ee19)
  - Fixed: forgot password / password reset (ff7ba2a, fb6a988)
  - Fixed: Stripe userId + email now passed to checkout (5f48ba0)
  - Project knowledge loaded into Mission Control (gpu-learning-lab) memory system
  - Mission Control HD Command Center created in Notion
---
## Session 5 — March 9, 2026 (Onboarding + CC Build)
  - Full project onboarded into Mission Control knowledge system (gpu-learning-lab)
  - memory/projects/missioncontrolhd.md created — full project snapshot
  - MCHD Command Center built in Notion under Mission Control HQ
  - 5 sub-pages created: Project Overview & Tech Stack, Stripe & Payments Config, Infrastructure & Auth Config, Launch Roadmap & Open Issues, Session Log
  - Confirmed page ID: 31e88f09-7e31-8182-900a-cac36f525edc
  - Two critical blockers confirmed open: Stripe live webhook + Supabase auth redirect URLs
  - All code bugs from pre-Feb 23 backup confirmed fixed — no code changes needed this session
  - Ecosystem cross-reference audit: MCHD is standalone SaaS — not part of ADC 3K pod product line