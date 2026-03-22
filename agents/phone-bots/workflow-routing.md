# Phone System Workflow — Louisiana's AI Infrastructure Initiative

## Phone Number
**(337) 448-4242** — Lafayette area code, Bland.ai

## Bland.ai Details
- Organization: louisianaaiinfrastructureinitiative
- Pathway ID: dbee8def-0c8e-451a-bbd7-d56b66af151c
- Webhook: https://louisianaai.net/api/webhook
- Transfer/Fallback: (337) 780-1535
- Voice Pronunciation: use "A eye" not "A.I." in all prompts
- **CREDITS: CHECK BEFORE BROADCAST**

## Architecture

```
CALLER DIALS MAIN NUMBER
         │
    ┌────▼────┐
    │  SARAH  │  Front Desk Bot
    │ (Triage)│  Greets, detects intent, routes
    └─┬──┬──┬─┘
      │  │  │
      │  │  └──────────────────────────────┐
      │  │                                 │
  ┌───▼──┐  ┌───▼───┐  ┌───▼───┐    ┌────▼────┐
  │MICHELLE│ │ JAMES │  │ JAMES │    │  SARAH  │
  │(Edu)  │ │(Invest)│ │(Vendor)│   │(Media/  │
  │       │ │       │  │       │    │ Careers)│
  └───┬───┘ └───┬───┘  └───┬───┘    └────┬───┘
      │         │          │              │
      ▼         ▼          ▼              ▼
  ┌──────────────────────────────────────────┐
  │           EMAIL ROUTING                   │
  │                                           │
  │  education@louisianaai.net  → Education   │
  │  investors@louisianaai.net  → Investment  │
  │  vendors@louisianaai.net    → Vendors     │
  │  media@louisianaai.net      → Press       │
  │  careers@louisianaai.net    → Hiring      │
  │  info@louisianaai.net       → General     │
  │                                           │
  │  ALL route to scott@adc3k.com for now     │
  │  Re-route individual addresses as team    │
  │  grows — no disruption to callers         │
  └──────────────────────────────────────────┘
         │
    ┌────▼────────────────────┐
    │  CRM / TRACKING SHEET   │
    │                         │
    │  Every interaction:     │
    │  - Name                 │
    │  - Email                │
    │  - Phone                │
    │  - Organization         │
    │  - Category             │
    │  - Summary              │
    │  - Date/time            │
    │  - Follow-up status     │
    │  - Source (phone/web/    │
    │    email)               │
    └────┬────────────────────┘
         │
    ┌────▼────┐
    │  SCOTT  │
    │         │  Daily digest email
    │         │  Priority callbacks
    │         │  Investor follow-ups
    └─────────┘
```

## Bland.ai Setup

### Bot 1: Sarah (Front Desk)
- Pathway: Main number → Sarah answers
- Voice: Female, warm, professional
- Prompt file: front-desk-prompt.md
- Transfer targets:
  - "Education" → Michelle bot
  - "Investor" → James bot
  - "Vendor" → James bot (same persona, different context)
  - "Media" → Sarah takes message, emails media@louisianaai.net
  - "Careers" → Sarah takes message, emails careers@louisianaai.net

### Bot 2: Michelle (Education)
- Pathway: Transfer from Sarah
- Voice: Female, knowledgeable, encouraging
- Prompt file: education-bot-prompt.md
- Handles: Schools, universities, grants, K-12, STEM, workforce
- Collects: Name, institution, role, email, phone, needs
- Emails summary to: education@louisianaai.net

### Bot 3: James (Investor/Vendor/Infrastructure)
- Pathway: Transfer from Sarah
- Voice: Male, confident, direct
- Prompt file: investor-bot-prompt.md
- Handles: Investment inquiries, financial questions, vendor partnerships, site specs
- Collects: Name, firm/company, email, phone, investment interest
- Emails summary to: investors@louisianaai.net or vendors@louisianaai.net

## Web Form Routing

| Form Location | Sends To | Subject Line |
|---|---|---|
| louisianaai.net | info@louisianaai.net | "Louisiana AI Infrastructure Initiative Inquiry" |
| adc3k.com/trappeys (Get Your School In) | education@louisianaai.net | "Ragin' Cajun Campus — School Inquiry" |
| adc3k.com/lsu (Get Your School In) | education@louisianaai.net | "Tiger Campus — School Inquiry" |
| adc3k.com/trappeys (Investor tab form, future) | investors@louisianaai.net | "Ragin' Cajun Campus — Investor Inquiry" |
| adc3k.com/lsu (Investor tab form, future) | investors@louisianaai.net | "Tiger Campus — Investor Inquiry" |

## Cloudflare Email Routing Setup

In Cloudflare → louisianaai.net → Email Routing:

| Address | Destination | Category |
|---|---|---|
| info@louisianaai.net | scott@adc3k.com | General |
| investors@louisianaai.net | scott@adc3k.com | Investment |
| education@louisianaai.net | scott@adc3k.com | Schools/Universities |
| careers@louisianaai.net | scott@adc3k.com | Employment |
| media@louisianaai.net | scott@adc3k.com | Press/News |
| vendors@louisianaai.net | scott@adc3k.com | Suppliers/Partners |

All route to scott@adc3k.com initially. As team grows, reroute individual addresses — zero disruption to callers or senders.

## CRM (Start Simple)

### Phase 1: Google Sheet
Columns: Date, Source (phone/web/email), Name, Email, Phone, Organization, Category (education/investor/vendor/media/careers/other), Summary, Follow-up Status, Notes

### Phase 2: Airtable or Supabase
- Automated intake from Bland.ai webhook + FormSubmit
- Category auto-tagging
- Follow-up reminders
- Daily digest email to Scott
- Dashboard view

## Daily Operations
1. Sarah answers all calls, routes to Michelle or James
2. Michelle/James handle their domain, collect info, email summaries
3. Web forms submit to category-specific emails
4. All emails land in scott@adc3k.com inbox (for now)
5. Scott reviews daily, handles priority callbacks
6. CRM sheet updated with every contact
