# Mission Control — Project State
Last updated: 2026-03-26

---

## SESSION SUMMARY — March 26, 2026

### ROXY: AI Advantage Agent Platform (23 tools)

Built ROXY from scratch — a tool-calling AI agent that runs on ADC's own GPU hardware. Started as a simple chatbot, ended as a 23-tool SaaS platform.

**Architecture:**
- ReAct-style agent loop (max 3 tool iterations per request)
- Vercel serverless functions (ai-advantage.info)
- Primary: vLLM + Qwen 3 8B on RunPod (pod 38df7s7h46h8u4, $0.20/hr)
- Fallback: Anthropic Claude (native tool calling)
- vLLM restarted with `--enable-auto-tool-choice --tool-call-parser hermes` — full tool calling LIVE
- Multi-turn conversation with client-side history (20 messages)
- RAG index: 480 chunks from 21 files, TF-IDF keyword search

**Sales & Closing Tools (7):**
1. `search_playbooks` — RAG over 17 industry playbooks
2. `build_quote` — Pricing calculator with industry recommendations
3. `calculate_roi` — Dollar ROI math ("pays for itself in 3 days, $6,680/mo net")
4. `generate_payment_link` — Stripe checkout in-chat (needs STRIPE_SECRET_KEY)
5. `franchise_qualifier` — 8x revenue multi-location quotes with volume discounts
6. `create_urgency_offer` — Time-limited offers with unique promo codes
7. `generate_live_demo` — "Day in the life" before/after scenarios by industry

**CRM & Outreach Tools (6):**
8. `capture_lead` — Brevo CRM with auto-segmentation to 12 industry lists + 7 custom attributes
9. `crm_lookup` — Returning visitor detection
10. `send_followup_email` — Personalized HTML email with industry playbook highlights
11. `send_sms` — Text messages via Brevo (needs SMS credits)
12. `book_appointment` — Booking link generation
13. `log_conversation` — Saves summaries for training data flywheel

**Intelligence Tools (4):**
14. `get_contact_info` — Prevents hallucinated details
15. `business_lookup` — Web research on prospect's business
16. `competitor_intel` — Positions against 11 competitors (ServiceTitan, Toast, Dentrix, etc.)
17. `local_market_intel` — "Only 2 of 47 plumbers in Lafayette use AI" FOMO data

**SaaS Marketing Suite (6):**
18. `generate_ad_copy` — Facebook, Instagram, Google ads with multiple angles
19. `generate_social_posts` — Week of social media content (tips, humor, behind-scenes)
20. `respond_to_review` — Professional responses to positive/negative reviews
21. `request_review` — Review request templates via email/SMS
22. `generate_lead_magnet` — Downloadable guides and checklists by industry
23. `build_email_campaign` — Drip campaign sequences (welcome, reactivation, referral)

**Brevo CRM Setup:**
- 7 custom contact attributes: INDUSTRY, INTEREST_LEVEL, RECOMMENDED_PLAN, SOURCE, ROXY_QUOTE, ROI_MONTHLY, LAST_ROXY_CHAT
- 12 industry-specific lists (IDs 13-24) + master "AI Advantage Leads" (ID 9)
- Auto-segmentation: every lead tagged by industry, interest level, source
- 141 total contacts, 3 campaigns sent
- BREVO_API_KEY + BREVO_LIST_ID set on Vercel

**Investor Pitch Updated:**
- Slide 8 (Inside the Factory): "PROOF OF CONCEPT — TOKENS FLOWING TODAY" section with pulsing LIVE indicator
- Operations Center page: "Tokens Flowing Today" section with production path timeline
- Both deployed at adc3k.com

**File Structure — ROXY Agent:**
```
ai-advantage/site/
  api/chat.js                    — Agent entry point
  lib/agent/loop.js              — ReAct agent loop (max 3 iterations)
  lib/agent/providers.js         — vLLM + Anthropic abstraction
  lib/agent/system-prompt.js     — Dynamic prompt builder
  lib/tools/index.js             — Tool registry (23 tools)
  lib/tools/*.js                 — Individual tool files
  lib/rag/build-index.js         — Playbook index builder
  lib/rag/playbook-index.json    — Pre-built search index (603 KB)
  lib/util/rate-limiter.js       — 20 req/min per IP
  index.html                     — Frontend with multi-turn chat + tool indicators
  vercel.json                    — Function config (512MB, 30s, includeFiles)
  package.json                   — Dependencies + build:index script
```

**Other:**
- Renamed Ally → ROXY across all files
- Fine-tuning dataset generated: 93 examples in data/roxy-training-data.jsonl
- RunPod pod: 38df7s7h46h8u4, A4500, vLLM with tool calling enabled
- Vercel env vars: ADC_INFERENCE_URL, ADC_MODEL, ANTHROPIC_API_KEY, BREVO_API_KEY, BREVO_LIST_ID, BOOKING_URL

### Prior Session (March 25, 2026)
- EP002 published, $5M pitch deck, Operations Center, KLFT page
- 22 vendors spec'd, 24 blueprints, 8 NVIDIA playbooks
- 5 competitive intel reports, 4 Louisiana infrastructure reports
- File structure reorganized into job folders
- AI Advantage migrated to self-hosted model

---

## Action Items — Priority Order

1. **Stripe account** — Set up Stripe, add STRIPE_SECRET_KEY to Vercel. Unlocks in-chat payments.
2. **SMS credits** — Buy Brevo SMS credits. Unlocks text message follow-ups.
3. **Cal.com/Calendly** — Set up booking tool, update BOOKING_URL on Vercel.
4. **Fine-tune ROXY** — Upload roxy-training-data.jsonl to RunPod, fine-tune Qwen 3 8B.
5. **Brevo drip campaigns** — Build industry-specific email automations using the 12 lists.
6. **LinkedIn outreach** — CERAWeek contacts + Delta
7. **NPN** — Follow up with Jim Hennessy (NVIDIA). Invitation only.
8. **Episode 3 production** — briefing ready
9. **Answering service on (337) 780-1535**
10. **Louisiana Cat** (337-837-2476) — G3516J quote + lead times
11. **MARLIE I expansion** — pick layout, begin site prep

---

## Phone Numbers (LOCKED)
- ADC business: (337) 780-1535 (AT&T, Scott's line)
- Louisiana AI Initiative: (337) 448-4242 (Bland.ai bot)
- AI Advantage: (337) 486-3149 (Bland.ai bot)
- NEVER cross these numbers between sites

---

## Dual Power Stack (LOCKED)
- Eaton Beam Rubin DSX = FACILITY power (800V bus, ORV3 sidecar)
- Delta Electronics = RACK power (660 kW rack, e-Fuse, 90 kW DC/DC, 140 kW CDU)
- Both on EVERY drawing, EVERY page, EVERY spec

---

## Raise
- $5M seed round
- MARLIE I owned (collateral)
- Trappeys ~$1M acquisition
- Pitch deck LIVE at /investor-pitch (14 slides, self-hosted proof of concept)
- Master doc: business-model/MASTER-INVESTOR-PACKAGE.md
