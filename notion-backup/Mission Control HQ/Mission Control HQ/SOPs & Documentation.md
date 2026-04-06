# 📝 SOPs & Documentation
*Notion backup — 2026-04-06*

Standard operating procedures and technical references for Mission Control.
---
## DNS Records (Namecheap → missioncontrolhd.com)
| Type | Host | Value |
| TXT | resend._domainkey | p=MIGfMA0GCSqGSIb3DQEB... (DKIM key) |
| TXT | send | v=spf1 include:amazonses.com ~all |
| TXT | _dmarc | v=DMARC1; p=none; |
---
## Supabase SMTP Settings
- Custom SMTP: ON
- Sender email: noreply@missioncontrolhd.com
- Sender name: Mission Control HD
- Host: smtp.resend.com
- Port: 465
- Username: resend
- Password: Resend API key (saved in Supabase)
---
## Deploying to Vercel
1. Push changes to GitHub (main branch)
1. Vercel auto-deploys from main
1. Check deployment at vercel.com dashboard
1. Verify at missioncontrolhd.com
---
## Password Reset (Emergency — When Email Is Broken)
If you can't reset via email, use the Supabase SQL Editor:
1. Go to Supabase dashboard → SQL Editor
1. Run: SELECT id FROM auth.users WHERE email = 'your@email.com';
1. Share the output with Claude to generate the password update query
---
## Vercel Environment Variables
| Variable | Value |
| NEXT_PUBLIC_SITE_URL | https://missioncontrolhd.com |
| STRIPE_WEBHOOK_SECRET | whsec_... (live) |
| KIT_API_KEY | (set) |
| STRIPE_PRO_ANNUAL_PRICE_ID | price_1T4BQuJt9Vd7LWdNXcMxqqQl |
| STRIPE_PRO_MONTHLY_PRICE_ID | price_1T4BQqJt9Vd7LWdNJ4odqhwg |
| ANTHROPIC_API_KEY | (set) |
| NEXT_PUBLIC_SUPABASE_URL | (set) |
| NEXT_PUBLIC_SUPABASE_ANON_KEY | (set) |
| SUPABASE_SERVICE_ROLE_KEY | (set) |
| STRIPE_SECRET_KEY | sk_live_... |
| NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY | pk_live_... |
| STRIPE_PREMIUM_MONTHLY_PRICE_ID | price_1T4BQqJt9Vd7LWdNZOAvZB2u |
| STRIPE_PREMIUM_ANNUAL_PRICE_ID | price_1T4BQrJt9Vd7LWdNixDFqmSN |
---
> NOTE (2026-03-23): This page contains SOPs for Mission Control HD SaaS (on hold). Content remains valid for when MCHD development resumes. DNS records, Supabase config, and Vercel deploy steps are still current.