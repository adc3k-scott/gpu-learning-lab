# Launch Roadmap & Open Issues
*Notion backup — 2026-03-28*

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