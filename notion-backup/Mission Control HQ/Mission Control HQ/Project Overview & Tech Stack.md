# Project Overview & Tech Stack
*Notion backup — 2026-03-28*

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