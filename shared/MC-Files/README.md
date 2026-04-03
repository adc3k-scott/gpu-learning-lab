# Mission Control

**Multi-platform vehicle intelligence for Harley-Davidson riders, car owners, CDL truckers, e-bike riders, and scooter owners.**

41 free diagnostic tools, AI-powered chat, vehicle garage, community forum, and more.

## Quick Start

```bash
# Install dependencies
npm install

# Set up environment variables
cp .env.template .env.local
# Edit .env.local with your API keys

# Run development server
npm run dev

# Open http://localhost:3000
```

## Stack

- **Framework:** Next.js 15 (App Router)
- **Hosting:** Vercel
- **Database:** Supabase (PostgreSQL + Auth)
- **Payments:** Stripe
- **AI:** Anthropic Claude API
- **Email:** Kit (ConvertKit)
- **Styling:** Tailwind CSS

## Platforms

| Platform | Color | Tools |
|----------|-------|-------|
| Harley-Davidson | `#E8720E` | 7 |
| Automotive | `#8B5CF6` | 5 |
| Trucking | `#FF6F00` | 7 |
| E-Bike | `#22C55E` | 7 |
| Scooter | `#06B6D4` | 5 |
| Universal | — | 10 |

## Pricing

| Tier | Price | AI Chat | Garage |
|------|-------|---------|--------|
| Free | $0 | 3/day | 1 vehicle |
| Premium | $9.99/mo | 20/day | 3 vehicles |
| Pro | $19.99/mo | Unlimited | Unlimited |

## Deploy

```bash
# Build for production
npm run build

# Deploy to Vercel
npx vercel --prod
```

## Database

Run `supabase_schema.sql` in your Supabase SQL Editor to create all tables, RLS policies, triggers, views, and functions.

## Environment Variables

See `.env.template` for all required variables and where to find them.

---

Built in Baton Rouge, Louisiana. Powered by Claude.
