# Infrastructure & Auth Config
*Notion backup — 2026-04-03*

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