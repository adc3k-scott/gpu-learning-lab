# ADC AI Install Playbook — Insurance Agency

## Who This Is For
You're an ADC installer. This covers independent insurance agencies, State Farm/Allstate/Farmers captive agents, health insurance brokers, life insurance agencies, and commercial insurance brokers. If they sell and service insurance policies, this playbook applies.

---

## What You're Installing
An AI system that handles the quote-compare-bind cycle faster and follows up better than any human can. When you're done, the agency will be able to:

- **Multi-carrier quoting** — client needs auto insurance. Instead of logging into 5 different carrier portals, the AI pulls quotes from all carriers at once. Side-by-side comparison in seconds.
- **Lead follow-up** — new inquiry comes in → AI responds within 60 seconds. Qualifies the lead: *"What type of coverage? How many vehicles? Any claims in the last 5 years?"* Schedules a call with the agent.
- **Renewal tracking** — AI watches every policy expiration date. 90 days out: *"Mrs. Johnson's homeowner's policy renews March 15. Current premium: $2,100. Market check: [carrier] is offering $1,850 for similar coverage."*
- **Claims intake** — client calls about a claim. AI collects: what happened, when, policy number, photos. Routes to the carrier claims department with a complete file.
- **Cross-sell intelligence** — *"Client has auto and home with you but no umbrella. Net worth indicates umbrella is appropriate. Recommend?"*
- **AI phone** — *"I need to add a car to my policy." "How much is renters insurance?" "I need to file a claim." "What's my deductible?"* — AI handles routine calls and routes complex ones to the agent.
- **Client portal** — view policies, download ID cards, request certificates, update info, pay premiums.

**What it replaces:** The agent logging into 6 carrier portals to run one quote. The renewal that lapsed because nobody noticed until the client called. The cross-sell opportunity that walked out the door because the agent was too busy quoting to mention umbrella coverage.

---

## Client Minimum Requirements

### Tier 1: Cloud-Only

| Requirement | Minimum | Recommended | Why |
|-------------|---------|-------------|-----|
| **Internet** | 25 Mbps | 50+ Mbps | Multiple carrier portal connections + quoting + CRM running simultaneously. |
| **Computer** | 8GB RAM | 16GB RAM, SSD, dual monitors | Agents live on dual screens — quotes on one, client info on the other. |
| **Agency management system** | Not required but helpful | If they use Applied Epic, Hawksoft, EZLynx, QQ Catalyst, or AMS360 — we integrate | |
| **Phone** | Any smartphone | Modern smartphone | For notifications, client texts, mobile access. |
| **Carrier appointments** | Active carrier contracts | | We can't quote carriers they're not appointed with. |

**Cost to client:** $0 + monthly subscription
**Best for:** Small agencies (1-5 agents)

### Tier 2: ADC Starter Kit

| Item | Spec | Approx. Cost | Notes |
|------|------|-------------|-------|
| Agent workstation | Intel i5, 16GB RAM, 512GB SSD | $500-700 | Per agent |
| Dual monitors | 24" x2 | $300-400 | Per agent |
| Scanner | Fujitsu ScanSnap | $400 | Policy documents, dec pages, driver's licenses |
| UPS | 600VA | $60-80 | Per workstation |
| **Total (per agent)** | | **$1,260-1,580** | |

### Tier 3: NVIDIA DGX Spark

| Item | Spec | Cost |
|------|------|------|
| **NVIDIA DGX Spark** | GB10 Grace Blackwell, 128GB, 1 PFLOPS FP4, 4TB encrypted NVMe | **$4,699** |
| Workstation kit (2 agents) | | $2,520-3,160 |
| **Total** | | **~$7,220-7,860** |

**When to recommend:**
- Agency handles commercial lines with sensitive business financials
- Large agency (10+ agents) with high quote volume
- Agency handling professional liability (E&O for doctors, lawyers) with sensitive client data
- Agent who wants AI-powered risk analysis trained on their book of business

**The pitch:**
> *"Your clients' financial information — net worth, property values, business revenue, claims history — stays on this box in your office. Encrypted. And the AI learns your book: it knows which clients are under-insured, which renewals are at risk, and which carriers are most competitive in your market."*

---

## The Install — Step by Step

### Step 1: Arrive + Understand Their Book (15 minutes)

1. Ask:
   - What lines do they write? (Personal: auto, home, umbrella, life, health. Commercial: GL, WC, commercial auto, property, E&O, D&O, cyber.)
   - How many clients / policies?
   - What carriers are they appointed with?
   - What agency management system? (Applied, Hawksoft, EZLynx, QQ, or "spreadsheet and filing cabinet")
   - What's their biggest pain? (Usually: quoting speed, renewal follow-up, or cross-selling)
   - Independent or captive? (Captive = one carrier. Independent = multiple. This changes the quoting setup.)
2. If independent: get their carrier list with login credentials for each portal (they type these, not you).

### Step 2: Create Workspace (10 minutes)

1. `setup.adc3k.com` → New Client Workspace
2. Type: Insurance — Personal Lines / Commercial Lines / Life & Health / Full Agency
3. Number of agents / CSRs
4. Agency management system (if any)

### Step 3: Carrier Connections (20 minutes)

**This is the core feature. More carriers connected = more value.**

1. Click **"Carriers"**
2. For each carrier they're appointed with:
   - Carrier name
   - Lines of business (auto, home, commercial, etc.)
   - Login credentials for their agent portal (agent types these)
   - API connection if available (many carriers now offer comparative rater APIs)
3. **Comparative rating:**
   - If they already use a comparative rater (EZLynx, ITC, TurboRater): connect it — our system feeds into it
   - If they don't: our system becomes their rater — agent enters client info once, gets quotes from all connected carriers
4. **Rate accuracy:** AI learns which carriers are most competitive for specific profiles:
   - *"For young drivers with clean records, Progressive wins 60% of the time in your area."*
   - *"For homes over $500K, Chubb is typically 15% cheaper than Hartford."*
   - This intelligence builds over time from their actual quotes.

### Step 4: Client / Policy Import (15 minutes)

1. Click **"Clients"**
2. Import existing book of business:
   - From AMS: export client list + policy data as CSV
   - From carrier downloads: many carriers provide book-of-business downloads
   - Manual: for small agencies, enter key clients first
3. For each client:
   - Name, address, phone, email, DOB
   - Policies: type, carrier, policy number, effective date, expiration date, premium, coverage limits
   - Cross-sell status: what lines they have vs. what they should have
4. **Policy expiration import is critical.** This is what drives the renewal pipeline.

### Step 5: Renewal Pipeline (15 minutes)

1. Click **"Renewals"**
2. Pipeline stages:
   ```
   90 Days Out → Market Check → Quote Ready → Presented to Client →
   Renewed / Re-written → Bound
   ```
3. **AI automation:**
   - **90 days before expiration:** AI alerts agent + runs market check against connected carriers
   - **60 days:** If a better option exists, AI drafts a comparison for the client
   - **30 days:** If client hasn't responded, AI sends reminder: *"Your [type] policy renews on [date]. We've found some options that could save you money. Let's review: [link to schedule call]"*
   - **7 days:** Urgent alert to agent: *"Policy expires in 7 days — no action taken."*
4. **Retention metric:** Track retention rate (target: 85%+). The system shows which policies are at risk of non-renewal.

### Step 6: Lead Management + Speed-to-Lead (10 minutes)

1. Click **"Leads"**
2. Connect lead sources:
   - Website quote request form
   - Google Ads / Facebook leads
   - Referrals (manual entry or referral link)
   - Phone inquiries (AI captures info)
3. **Speed-to-lead response:**
   - New lead → AI responds within 60 seconds via text
   - Qualifies: *"Hi [name], thanks for reaching out about [coverage type]. I have a few quick questions to get you an accurate quote: [questions]"*
   - Once qualified → AI presents to agent with pre-filled quote request
   - Agent reviews → runs final quote → presents to client
4. **Lead scoring:**
   - Hot: ready to bind, policy expiring soon
   - Warm: shopping, comparing, 30-60 days out
   - Cold: just browsing, no urgency
   - AI prioritizes agent's time on hot leads

### Step 7: Cross-Sell Engine (10 minutes)

1. Click **"Cross-Sell"**
2. Configure coverage gap rules:
   - Has auto but no home → recommend homeowners
   - Has auto + home but no umbrella → recommend umbrella (especially if net worth > $500K)
   - Has home but no flood → recommend flood (especially in Louisiana!)
   - Business client with no cyber liability → recommend cyber
   - Client with kids turning 16 → recommend adding to auto
3. AI generates cross-sell lists:
   - *"124 clients have auto + home but no umbrella. Estimated additional premium: $180/yr avg. Estimated commission: $2,232/yr total."*
4. Agent can send targeted outreach: *"Hi [name], I noticed you don't currently have an umbrella policy. Given your home and auto coverage, an umbrella would protect your assets for about $15/month. Worth a quick conversation?"*

### Step 8: Claims Intake (10 minutes)

1. Click **"Claims"**
2. Set up intake flow:
   - AI asks: What happened? When? Where? Anyone injured? Police report? Photos?
   - Captures all details + photos
   - Pulls the client's policy and coverage details
   - Generates a claims submission package
   - Routes to the correct carrier claims department
3. Agent reviews before submission (or auto-submits for straightforward claims)
4. **Tracking:** Status updates from carrier → forwarded to client: *"Your claim #XXXXX has been assigned to adjuster [name]. They'll contact you within 48 hours."*

### Step 9: AI Phone (10 minutes)

1. Greeting: *"Thank you for calling [Agency Name]. I can help you with a quote, policy question, or claims. How can I help?"*
2. Routing:
   - **"I need a quote"** → qualifies the lead, schedules agent callback
   - **"I need to add/remove a vehicle"** → collects details, creates service request for agent
   - **"I need proof of insurance / ID card"** → pulls from policy, texts or emails to client
   - **"I need to file a claim"** → claims intake flow
   - **"What's my deductible?"** → looks up policy → *"Your auto comprehensive deductible is $500 and your collision deductible is $1,000."*
   - **"I want to make a payment"** → provides carrier payment link or phone number
3. After hours: AI handles everything, queues action items for next business day

### Step 10: Automated Communications (5 minutes)

- [x] **Welcome (new client):** *"Welcome to [Agency]! Your policy is bound. Here's your agent's direct line and your online portal access: [link]"*
- [x] **ID cards issued:** *"Your insurance ID cards are ready. Download here: [link]"*
- [x] **Renewal reminder (90/60/30 days)**
- [x] **Payment reminder:** *"Your premium payment of $X is due on [date]."*
- [x] **Cross-sell outreach** (per cross-sell engine above)
- [x] **Policy change confirmation:** *"Your policy has been updated. Here's a summary of the changes: [link]"*
- [x] **Birthday:** *"Happy birthday, [name]! As a reminder, if you've had any life changes this year (new home, new car, marriage), let's review your coverage."*
- [x] **Review request:** *"How's your experience with [Agency]? Leave a review: [Google link]"*
- [x] **Referral program:** *"Know someone who needs insurance? Refer them and receive $X gift card when they bind a policy."*

---

## Training (20 minutes)

### Agents (10 minutes)
1. Comparative quoting — enter client info, see all carrier quotes side by side
2. Renewal pipeline — how to work the 90-day board
3. Cross-sell lists — how to identify and act on coverage gaps
4. Lead response — how speed-to-lead works

### CSRs (5 minutes)
1. AI phone — how calls are routed, what AI handles vs. what CSRs handle
2. Policy lookups — how to find client info and policy details quickly
3. Service requests — how to process endorsements, add vehicles, issue certificates

### Owner / Principal (5 minutes)
1. Dashboard — retention rate, new business, cross-sell revenue, agent productivity
2. Book-of-business analytics — where the money is, where the risk is
3. Revenue opportunities — total cross-sell potential in current book

---

## Before You Leave — Final Checklist

- [ ] At least 3 carriers connected for comparative quoting
- [ ] Client/policy data imported (at minimum: expiration dates for renewal tracking)
- [ ] Renewal pipeline configured and alerts turned on
- [ ] Cross-sell rules set up (auto→home, auto+home→umbrella, home→flood)
- [ ] Lead sources connected with speed-to-lead response
- [ ] AI phone live and routing correctly
- [ ] Claims intake flow tested
- [ ] Automated communications turned on (renewals, welcome, cross-sell)
- [ ] Each agent can run a comparative quote without help
- [ ] Quick Start card at each workstation
- [ ] Service agreement signed

---

## Troubleshooting

| Problem | What to Do |
|---------|------------|
| "Carrier portal login isn't working" | Carrier passwords expire frequently. Re-enter credentials. Some carriers also require MFA that needs to be completed on the carrier's site first. |
| "Quotes from the system don't match the carrier portal" | Comparative raters use simplified inputs. For exact quotes, always verify on the carrier portal before presenting to the client. The system gets you close; the portal gets you exact. |
| "My book is too big to import" | Start with renewals in the next 90 days. Work backwards from there. The most important data is expiration dates. |
| "Client doesn't want to use a portal" | Some clients (especially older ones) want paper or phone calls only. Flag them as "no portal" and handle them the traditional way. Don't force it. |
| "The cross-sell texts feel pushy" | Adjust the frequency and tone. Once per quarter is reasonable. More than monthly and clients will opt out. |

---

## What You Should NOT Do

1. **NEVER give insurance advice.** You're not licensed. Don't recommend coverage, carriers, or limits. *"That's a great question for your agent."*
2. **NEVER access client personal data** (SSN, driver's license, financial info) beyond what's needed for system setup. Use dummy data for demos.
3. **NEVER share carrier login credentials.** Each agent's portal access is their own.
4. **NEVER tell a client their coverage is inadequate.** That's between them and their agent.
5. **NEVER quote a policy or bind coverage.** Only licensed agents can do this.
6. **NEVER share one client's info with another client.**

---

## Glossary

| Word | What It Means |
|------|---------------|
| **Bind** | When a policy becomes active. "We bound the policy" = coverage started. |
| **Premium** | What the client pays for insurance. Monthly, quarterly, or annual. |
| **Carrier** | The insurance company. State Farm, Progressive, Hartford, etc. |
| **Appointed** | The agent has a contract with the carrier to sell their products. You can only quote carriers you're appointed with. |
| **Endorsement** | A change to an existing policy. Adding a car, changing a deductible, adding a rider. |
| **Dec page** | Declarations page. The summary page of a policy — shows what's covered, limits, deductibles, premium. |
| **Comparative rater** | Software that pulls quotes from multiple carriers at once. Our system does this. |
| **Cross-sell** | Selling additional coverage to an existing client. They have auto → sell them home. |
| **Retention rate** | Percentage of clients who renew their policy. Higher = better. Target: 85%+. |
| **Book of business** | All of an agent's clients and policies. "My book" = all my clients. |
| **E&O** | Errors & Omissions insurance. Professional liability for the agent. If the agent makes a mistake, E&O covers the lawsuit. |
| **Certificate of Insurance (COI)** | A document proving someone has insurance. Contractors need these constantly. AI can generate them instantly. |
