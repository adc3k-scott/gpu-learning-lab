# Stripe & Payments Config
*Notion backup — 2026-03-28*

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