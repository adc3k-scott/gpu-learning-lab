# ADC AI Install Playbook — Real Estate Office

## Who This Is For
You're an ADC installer. This covers real estate brokerages, independent agents, property management companies that also sell, and commercial real estate offices. If they list and sell properties, this playbook applies.

---

## What You're Installing
An AI system that does the homework so the agent can do the handshake. When you're done, the agent/office will be able to:

- **Listing descriptions from photos** — agent takes photos of the house, AI writes the MLS listing description. Professional, accurate, SEO-optimized. What used to take 30 minutes takes 30 seconds.
- **Market comps on demand** — *"What are the comps for 123 Main Street?"* AI pulls recent sales, active listings, price per square foot, days on market. Agent gets a comp report in seconds, not an hour of MLS searching.
- **Lead follow-up that never sleeps** — new lead comes in from Zillow, Realtor.com, Facebook ad, or the website. AI responds within 60 seconds: *"Hi [name], I'm with [agent name]. I see you're interested in [property]. Are you available for a showing this week?"* No more leads going cold because the agent was at a closing.
- **Answer every call** — AI handles: *"What are your hours? Do you have any listings in [area]? How much is [property]? I'd like to schedule a showing."*
- **Contract + disclosure generation** — AI generates purchase agreements, listing agreements, disclosure forms from templates. Agent reviews and sends. No more blank-filling for 45 minutes.
- **Showing scheduler** — AI coordinates between buyer's schedule, seller's availability, and agent's calendar. Sends confirmation to all parties.
- **Client CRM** — every lead, buyer, seller, past client in one place with full history, preferences, and next action.

**What it replaces:** The lead that came in at 9 PM and never got a call back. The agent spending 2 hours on a CMA. The listing description that says "charming 3BR" for the 400th time. The buyer who texted 3 agents and went with whoever responded first.

---

## Client Minimum Requirements

### Tier 1: Cloud-Only (Use What They Have)

| Requirement | Minimum | Recommended | Why |
|-------------|---------|-------------|-----|
| **Internet** | 25 Mbps | 50+ Mbps | Photo uploads, MLS access, CRM all running. |
| **Computer** | Any modern laptop | MacBook or Windows laptop with good screen | Agents are mobile — laptop is their office. |
| **Phone** | iPhone 12+ or Android 10+ | Latest iPhone or Samsung | Camera quality matters for listings. Phone IS the business tool. |
| **MLS Access** | Active MLS subscription | | Required for comp data integration. |
| **Email** | Gmail or Outlook | Gmail (integrates better) | For lead capture and client communication. |
| **CRM (existing)** | None required | If they have one (Follow Up Boss, KVCore, LionDesk) we can integrate | |

**Cost to client:** $0 hardware + monthly subscription
**Best for:** Individual agents or small teams who work from laptops and phones

### Tier 2: ADC Starter Kit (For the Office)

| Item | Spec | Approx. Cost | Notes |
|------|------|-------------|-------|
| Reception PC | Intel i5, 16GB RAM | $500-700 | Front desk — lead management, phone system |
| Monitor | 27" 4K | $300-400 | For reviewing listing photos and comps |
| Large display (lobby) | 43-55" TV | $300-500 | Shows active listings in the lobby — professional look |
| Wireless keyboard + mouse | | $30-50 | |
| UPS | 600VA | $60-80 | |
| **Total** | | **$1,190-1,730** | |

### Tier 3: NVIDIA DGX Spark

| Item | Spec | Cost |
|------|------|------|
| **NVIDIA DGX Spark** | GB10 Grace Blackwell, 128GB, 1 PFLOPS FP4, 4TB encrypted NVMe | **$4,699** |
| Office kit | | $1,190-1,730 |
| **Total** | | **~$5,890-6,430** |

**When to recommend DGX Spark for real estate:**
- Brokerage with 10+ agents (token volume makes cloud expensive)
- Commercial RE office handling sensitive client financials and NDAs
- Brokerage that wants custom-trained AI on their local market data (on-site training = better comps)
- Broker who wants competitive advantage — their AI knows the local market better than anyone else's generic AI

**The pitch to the broker:**
> *"Your AI is trained on YOUR market. It knows every sale, every price trend, every neighborhood. When your agents pull comps, they're not getting generic national data — they're getting hyperlocal intelligence that no other brokerage has. And the client data stays in your office."*

---

## The Install — Step by Step

### Step 1: Arrive + Understand Their Business (15 minutes)

1. Meet with the broker/team lead. Ask:
   - How many agents? (solo, small team, full brokerage)
   - What MLS? (Realtor.com, local board MLS, IRES, etc.)
   - What CRM? (Follow Up Boss, KVCore, LionDesk, Chime, or "I use my phone contacts")
   - What lead sources? (Zillow, Realtor.com, Facebook, yard signs, referrals, open houses)
   - What's their biggest time waste? (Usually: writing listings, doing CMAs, or chasing leads)
2. If it's a brokerage with admin staff: talk to the admin too. They'll be handling the AI phone and lead routing.

### Step 2: Create Workspace (10 minutes)

1. `setup.adc3k.com` → New Client Workspace
2. Type: Real Estate — Residential / Commercial / Both
3. Market area (city, county, or MSA)
4. MLS system
5. Number of agents

### Step 3: Connect Lead Sources (15 minutes)

**Speed-to-lead is everything in real estate.** The first agent to respond gets the client 78% of the time.

1. Click **"Lead Sources"**
2. Connect each source:
   - **Zillow Premier Agent:** API integration — leads auto-import
   - **Realtor.com:** API integration
   - **Facebook Lead Ads:** Connect Facebook Business account
   - **Website forms:** Add our lead capture form or connect their existing website form
   - **Google Business:** Connect for direct inquiries
3. Set up **instant AI response** for each source:
   - Lead comes in → AI responds within 60 seconds via text
   - Template: *"Hi [name], this is the AI assistant for [agent name] at [brokerage]. I see you're interested in [property/area]. [Agent] would love to help — are you available for a quick call today or tomorrow?"*
   - If the lead responds: AI continues the conversation, qualifies them (buyer/seller, timeline, budget, pre-approved?), and books a call/showing
   - If no response: AI follows up at Day 1, Day 3, Day 7, Day 14, Day 30

4. **Lead routing** (for teams/brokerages):
   - Round-robin (fair distribution)
   - By area (Agent A gets Northside, Agent B gets Southside)
   - By type (Agent A gets buyers, Agent B gets listings)
   - By price point (Agent A gets luxury, Agent B gets first-time buyers)

### Step 4: Listing Description Generator (10 minutes)

1. Click **"Listings"**
2. Show the agent(s) how it works:
   - Upload listing photos
   - Enter: address, beds, baths, sqft, lot size, year built, key features
   - Click "Generate Description"
   - AI writes a professional MLS description highlighting the best features
   - Agent reviews, edits, and copies to MLS
3. **Style settings:**
   - Tone: Professional / Warm / Luxury / Casual
   - Length: Short (MLS summary) / Medium (full description) / Long (marketing brochure)
   - Compliance: Include required disclosures for their state/board

**Demo this live.** Pull up a current listing photo on their phone, enter the details, and show them the description. This is usually the "wow" moment.

### Step 5: Comp Report / CMA Generator (10 minutes)

1. Click **"Market Analysis"**
2. Connect to MLS data feed (requires MLS credentials + RETS/IDX authorization)
3. Demo:
   - Enter an address or area
   - AI pulls: recent sales (6 months), active listings, pending, expired
   - Filters by: similar sqft, beds/baths, lot size, year built, condition
   - Generates a CMA report with:
     - Price range recommendation
     - Price per sqft analysis
     - Days on market trends
     - Absorption rate
   - Agent can brand it with their logo and send to the client as a PDF
4. **Say:** *"Instead of spending an hour pulling comps and building a report in Excel, you get this in 30 seconds. And it looks more professional than anything you'd build by hand."*

### Step 6: Contract + Document Generation (10 minutes)

1. Click **"Documents"**
2. Load state-specific templates:
   - Purchase agreement
   - Listing agreement
   - Seller's disclosure
   - Buyer agency agreement
   - Counter-offer
   - Addendums (inspection, financing, appraisal, HOA)
   - Commission referral agreement
3. AI fills in the blanks from the CRM data:
   - Buyer/seller names, property address, price, terms
   - Agent reviews, edits, sends for e-signature
4. **Important:** *"The AI fills in the blanks. The agent reads every word before sending. This is a legal document — the AI is a helper, not a lawyer."*

### Step 7: AI Phone + Showing Scheduler (10 minutes)

1. Set up AI receptionist:
   - *"Thank you for calling [Brokerage/Agent Name]. I can help you with property information, schedule a showing, or connect you with an agent. How can I help?"*
2. Showing scheduler:
   - Buyer requests showing → AI checks agent calendar + seller availability (if configured)
   - Proposes times → confirms with all parties → sends confirmation with address + access instructions
   - Day-of reminder to buyer AND seller
3. **Seller lockbox integration** (if applicable): instructions for ShowingTime or SentriLock codes

### Step 8: CRM + Pipeline (10 minutes)

1. Click **"CRM"**
2. Import existing contacts:
   - Upload CSV from their old CRM or phone contacts
   - Or connect existing CRM (Follow Up Boss, etc.) for two-way sync
3. Set up pipeline stages:

   **Buyer pipeline:**
   ```
   New Lead → Qualified → Showing → Offer → Under Contract → Closed
   ```

   **Seller pipeline:**
   ```
   New Lead → Listing Appointment → Active Listing → Under Contract → Closed
   ```

4. Each contact tracks:
   - Source (Zillow, referral, open house, etc.)
   - Timeline (looking now, 3-6 months, just browsing)
   - Budget / price range
   - Property preferences
   - All communication history
   - Next action date

### Step 9: Automated Drip Campaigns (10 minutes)

- [x] **Speed-to-lead** — instant response on new inquiries
- [x] **Nurture (buyers not ready yet)** — monthly market update: "Here's what's happening in [area] this month"
- [x] **Just listed** — to buyer leads matching the listing criteria
- [x] **Open house invite** — to leads in the area
- [x] **Under contract update** — to seller: "Your home has been on market for X days, Y showings"
- [x] **Post-closing** — "Congratulations on your new home!" + "How was your experience?" + review request
- [x] **Anniversary** — 1 year after closing: "Happy homeiversary! Your home has appreciated approximately $X since you bought it."
- [x] **Sphere of influence** — quarterly touch to past clients and referral sources

---

## Training (25 minutes)

### Agents (15 minutes)
Show them the 4 things they'll use daily:
1. **Lead response** — show how fast the AI responds. Send a test lead and watch it answer.
2. **Listing description** — generate one from a current listing. Let them edit it. Copy to MLS.
3. **Comp report** — pull comps for a current listing appointment. Show the PDF output.
4. **Showing scheduler** — book a test showing. Show the confirmation texts.

**Say:** *"The AI does the grunt work. You do the relationship. Every minute you're NOT writing a listing description or pulling comps is a minute you're meeting clients, showing houses, and closing deals."*

### Admin/Front Desk (10 minutes)
1. AI phone — how calls are routed, how to override
2. Lead routing — how leads are assigned to agents
3. CRM — how to look up a contact, add notes, change pipeline stage

---

## Before You Leave — Final Checklist

- [ ] At least 1 lead source connected and auto-responding
- [ ] Listing description generator tested with a real listing
- [ ] CMA/comp tool connected to MLS data
- [ ] Document templates loaded for their state
- [ ] AI phone live
- [ ] CRM has existing contacts imported
- [ ] Pipeline stages configured
- [ ] Drip campaigns turned on (at minimum: speed-to-lead + post-closing + anniversary)
- [ ] Each agent can generate a listing description and pull comps without help
- [ ] Quick Start card distributed to each agent
- [ ] Service agreement signed

### Hand-Off Script:
> *"You're live. Leads are being caught and responded to automatically. Listings get written in 30 seconds. Comps pull in one click. The biggest thing: TRUST the speed-to-lead. Let the AI respond first, then you follow up with the personal touch. The agents who respond fastest win — and now you're always first."*

---

## Troubleshooting

| Problem | What to Do |
|---------|------------|
| "Leads aren't coming in" | Check the lead source connection. Zillow/Realtor.com APIs sometimes need re-authorization. Also check: is the agent's subscription active with the lead source? |
| "The listing description is generic" | Add more details in the input. The more specific you are (granite countertops, not "updated kitchen"), the better the output. Also adjust the style/tone setting. |
| "Comps are pulling wrong properties" | Tighten the filters — sqft range, year built, property type. The AI defaults to broad; narrow it down. |
| "The AI is texting leads weird things" | Check the response templates. Customize them to match the agent's voice. Some agents are formal, some are casual — the AI should match. |
| "I already have a CRM" | We can sync with it or run alongside it. Don't force them to switch. If they love Follow Up Boss, let them keep it — our AI feeds into it. |

---

## What You Should NOT Do

1. **Don't give real estate advice.** You're not a licensed agent. Don't comment on property values, market conditions, or investment potential.
2. **Don't access MLS with their credentials for your own use.** You're connecting their system, not browsing listings for yourself.
3. **Don't promise lead conversion rates.** Say "faster response = more conversions" — don't say "you'll close 30% more deals."
4. **Don't remove their existing CRM.** We integrate or supplement. Never replace something they're comfortable with.
5. **Don't share agent contact lists or lead data between competing agents** (if installing at a brokerage). Each agent's leads are their own.

---

## Glossary

| Word | What It Means |
|------|---------------|
| **MLS** | Multiple Listing Service. The database where all listed properties live. Agents pay to access it. |
| **CMA** | Comparative Market Analysis. A report showing what similar homes sold for. Used to price a listing. Our AI generates these. |
| **Comp** | A comparable sale. A recently sold property similar to the subject property. Used to determine value. |
| **IDX** | Internet Data Exchange. How MLS data gets displayed on websites. |
| **Speed-to-lead** | How fast you respond to a new inquiry. Industry data: responding in under 5 minutes = 100x more likely to connect than responding in 30 minutes. Our AI responds in under 60 seconds. |
| **Drip campaign** | A series of automated messages sent over time. "Drip" because they go out slowly, like a dripping faucet — not all at once. |
| **Pipeline** | The stages a client moves through: lead → qualified → showing → offer → closed. Like a funnel. |
| **Sphere of influence** | Past clients, friends, family, referral sources. People who know the agent and might send business. |
| **DOM** | Days on Market. How long a listing has been active. Lower = better. |
| **Pre-approval** | A letter from a lender saying the buyer qualifies for a mortgage up to $X. Sellers want to see this before accepting an offer. |
