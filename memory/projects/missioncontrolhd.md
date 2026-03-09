# Mission Control HD — Vehicle Diagnostics SaaS
Last updated: 2026-03-09

## What It Is
Live SaaS at https://missioncontrolhd.com — vehicle diagnostics platform with AI chat, 41 tools across 6 vehicle platforms, community forum, and garage management. Built with Next.js 15, Supabase, Stripe, Claude AI.

## Live Status
- **Live URL:** https://missioncontrolhd.com
- **Vercel project:** mc-vehicle-app2 (Mission Control Pro team)
- **GitHub:** https://github.com/Scottay007/mission-control
- **Local path:** C:\Users\adhsc\mission-control
- **Latest known commit:** fb6a988 "Fix: password reset now works, add redirect support"

## Tech Stack
- Next.js 15 (App Router)
- Supabase (Auth + Postgres + RLS) — us-west-2, onvemzmhedyuropiruaf.supabase.co
- Stripe (Subscriptions + Webhooks) — LIVE mode as of March 2026
- Claude AI / Anthropic API (Diagnostic Chat)
- Vercel (Hosting + Serverless)
- Kit / ConvertKit (Email marketing)
- Tailwind CSS (Dark theme)
- Namecheap — missioncontrolhd.com (expires Feb 23, 2027, auto-renew ON)

## Platforms & Tools
| Platform | Color | Tools |
|----------|-------|-------|
| Harley-Davidson | #E8720E | 7 |
| Automotive | #8B5CF6 | 5 |
| Trucking | #FF6F00 | 7 |
| E-Bike | #22C55E | 7 |
| Scooter | #06B6D4 | 5 |
| Universal | — | 10 |
| **Total** | | **41 tools** |

## Pricing Tiers
| Tier | Price | AI Queries | Vehicles |
|------|-------|-----------|----------|
| Free | $0 | 3/day | 1 |
| Premium | $9.99/mo ($95.88/yr) | 20/day | 3 |
| Pro | $19.99/mo ($191.88/yr) | Unlimited | Unlimited |

Annual saves 20%. Premium has 7-day free trial.

## Stripe Price IDs (LIVE mode)
- Premium Monthly: price_1T2Nbc2a0QlcXNBji9gMD9cW
- Premium Annual: price_1T2Nd42a0QlcXNBjlG3I0f5M
- Pro Monthly: price_1T3oMt2a0QlcXNBj8538mT9A
- Pro Annual: price_1T3oOg2a0QlcXNBj1UmvhyQ0

## PRO-Gated Tools
- HD_Wiring_Reference_v2
- HD_Torque_Sequences_v2
- EBike_Wiring_Reference_v2
- Service_History_Export_v2

## Database (Supabase)
6 tables: profiles, vehicles, chat_history, community_posts, community_comments, email_signups
RLS enabled on all tables. Auto-profile trigger on signup. Confirm email ON.

## Vercel Env Vars (14 total)
```
NEXT_PUBLIC_SITE_URL=https://missioncontrolhd.com
STRIPE_WEBHOOK_SECRET=whsec_ecyh4s1g4j3Di5IzuzbkScifSsovYQMV  ← may need updating for live mode
STRIPE_PRO_MONTHLY_PRICE_ID=price_1T3oMt2a0QlcXNBj8538mT9A
STRIPE_PRO_ANNUAL_PRICE_ID=price_1T3oOg2a0QlcXNBj1UmvhyQ0
STRIPE_PREMIUM_MONTHLY_PRICE_ID=price_1T2Nbc2a0QlcXNBji9gMD9cW
STRIPE_PREMIUM_ANNUAL_PRICE_ID=price_1T2Nd42a0QlcXNBjlG3I0f5M
ANTHROPIC_API_KEY=(set)
NEXT_PUBLIC_SUPABASE_URL=https://onvemzmhedyuropiruaf.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=(set)
SUPABASE_SERVICE_ROLE_KEY=(set)
STRIPE_SECRET_KEY=(set — live mode sk_live_)
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=(set — live mode pk_live_)
KIT_API_KEY=(set)
```
NOTE: Local .env.local has wrong values — always work from Vercel dashboard for prod values.

## Accounts
| Service | Login |
|---------|-------|
| GitHub | Scottay007 |
| Vercel | via GitHub |
| Supabase | adhscott@yahoo.com |
| Stripe | adhscott@yahoo.com |
| Anthropic | adhscott@yahoo.com |
| Kit | adhscott@yahoo.com |
| Namecheap | Scottay007 |

## DNS (Namecheap)
- A Record: @ → 76.76.21.21
- CNAME: www → 4211f3971db6198f.vercel-dns-016.com

## What's Fixed (as of March 9, 2026)
- Build error in harley/flowcharts/page.jsx — FIXED (6f9ee19)
- Forgot password / password reset — FIXED (ff7ba2a, fb6a988)
- Stripe userId not passed to checkout — FIXED (5f48ba0)
- Moved to live Stripe keys — DONE (fd1e6bd, 1141e5f)
- Supabase auth lock timeout — FIXED (c1eeee5)

## Open Issues (not yet resolved)
1. **Stripe live webhook** — Need to create a live-mode webhook in Stripe dashboard pointing to https://missioncontrolhd.com/api/stripe/webhook. Old test webhook (fascinating-breeze) pointed to mc-vehicle-app2.vercel.app. Until this is done, subscription tier will NOT update after payment.
2. **Supabase auth redirect URLs** — Need to add https://missioncontrolhd.com/** in Supabase → Authentication → URL Configuration. Site URL should be https://missioncontrolhd.com.
3. **Account page email field blank** — Profile page shows name but email is empty/uneditable.
4. **Premium button** — Likely fixed by auth lock fix (c1eeee5) but needs live test to confirm.

## Remaining TODO (post-fix)
- OG images / app icons
- Blog posts (5 written, need adding to blog page)
- Kit email automation sequences
- Supabase auth email template customization
- Marketing launch: ProductHunt, Reddit, social media
- Stripe webhook URL update to missioncontrolhd.com domain

## Key File Locations
- `src/app/api/stripe/webhook/route.js` — webhook handler
- `src/app/api/stripe/checkout/route.js` — checkout session creator
- `src/app/pricing/page.jsx` — pricing + checkout buttons
- `src/app/login/page.jsx` — login + forgot password
- `src/lib/supabase.js` — browser + admin clients
- `src/lib/constants.js` — TIERS definition
- `artifacts/` — 41 tool source components
- `emails/` — 6 HTML email templates
