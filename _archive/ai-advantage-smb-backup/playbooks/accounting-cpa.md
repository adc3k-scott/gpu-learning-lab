# ADC AI Install Playbook — Accounting / CPA / Bookkeeping Firm

## Who This Is For
You're an ADC installer. This covers CPA firms, tax preparation offices, bookkeeping services, enrolled agents, and general accounting practices. If they do taxes, bookkeeping, payroll, or financial advisory, this playbook applies.

---

## What You're Installing
An AI system that processes documents and handles the parts of tax/accounting work that eat the most time. When you're done, the firm will be able to:

- **Tax document intake** — client uploads W-2s, 1099s, K-1s, mortgage statements, and other tax docs through a portal. AI reads them, extracts the data, organizes by category, and flags what's missing. *"Client has uploaded W-2 and 1099-DIV but is missing 1099-INT and mortgage statement."*
- **Client portal** — secure document exchange. No more emailing tax documents (insecure) or mailing paper. Client logs in, uploads, signs, downloads.
- **Document Q&A** — accountant asks the AI: *"What was this client's total Schedule C income?"* or *"Did this client's rental property generate a loss?"* — AI answers from the uploaded documents.
- **Engagement letter + proposal generation** — AI drafts engagement letters, fee proposals, and service agreements from templates. Customized per client.
- **Automated follow-up** — *"Hi [name], we're still missing your 1099-INT from your bank. Please upload it at your earliest convenience: [link]"* — goes out automatically until the document arrives.
- **Deadline tracking** — April 15, October 15, quarterly estimates, payroll deposits, 1099 filings. AI watches all deadlines and alerts the team.
- **AI phone** — handles scheduling, basic questions (*"When are my taxes due?" "What documents do I need to bring?" "Is my return ready?"*), and routes complex questions to staff.

**What it replaces:** The February email chaos — 200 clients all sending tax documents in different formats to different email addresses. The file on the desk that's missing one document and nobody followed up for 3 weeks. The extension filed because the client never sent their K-1.

---

## IMPORTANT: Data Security

Accounting firms handle SSNs, bank account numbers, income data, and business financials. This data is a goldmine for identity thieves.

### Rules for ADC Installers:
1. **NEVER look at client financial data.** Use test/dummy data during setup.
2. **All demo entries must use fake names and SSNs.** "John Test, SSN 000-00-0000."
3. **The firm should have cybersecurity insurance.** If they don't, mention it: *"You should talk to your insurance agent about cyber liability coverage. It's not required for our system, but it's important for your firm."*
4. **DGX Spark is the strongest play** for firms handling high-net-worth clients or businesses with sensitive financials.
5. **Portal must use MFA (multi-factor authentication).** Enable it during setup. Non-negotiable.

---

## Client Minimum Requirements

### Tier 1: Cloud-Only

| Requirement | Minimum | Recommended | Why |
|-------------|---------|-------------|-----|
| **Internet** | 25 Mbps | 50+ Mbps | Document uploads from multiple clients during tax season. |
| **Computer** | 8GB RAM | 16GB RAM, SSD, dual monitors | Tax software + AI system + client portal all running. Accountants live on two screens. |
| **Scanner** | Any | Fujitsu ScanSnap iX1600 or similar high-speed scanner | Tax season = hundreds of documents. A slow scanner is a bottleneck. |
| **Tax software** | Any (Drake, Lacerte, ProSeries, UltraTax, ATX) | | We work alongside their tax software, not instead of it. |
| **Phone** | iPhone or Android | Modern smartphone | For notifications, deadline alerts, approvals. |

**Cost to client:** $0 hardware + monthly subscription
**Best for:** Solo practitioners or small firms (1-5 CPAs) with decent equipment

### Tier 2: ADC Starter Kit

| Item | Spec | Approx. Cost | Notes |
|------|------|-------------|-------|
| Office PC (per preparer) | Intel i5, 16GB RAM, 512GB SSD | $500-700 | Running tax software + AI + portal |
| Dual monitors (per preparer) | 24" 1080p x2 | $300-400 | Accountants need two screens |
| High-speed scanner | Fujitsu fi-8170 or ScanSnap | $400-700 | Tax season throughput |
| UPS (per workstation) | 600VA | $60-80 | |
| Shredder (cross-cut, P-4) | | $100-200 | For paper originals after scanning |
| **Total (per preparer)** | | **$1,360-2,080** | |

### Tier 3: NVIDIA DGX Spark

| Item | Spec | Cost |
|------|------|------|
| **NVIDIA DGX Spark** | GB10 Grace Blackwell, 128GB, 1 PFLOPS FP4, 4TB encrypted NVMe | **$4,699** |
| Per-preparer kit x2 | | $2,720-4,160 |
| **Total** | | **~$7,420-8,860** |

**When to recommend DGX Spark:**
- Firm handles high-net-worth clients (complex returns, sensitive financials)
- Firm handles business clients with trade secrets in their financials
- Tax season crunch — local AI processes 100+ documents simultaneously without cloud latency
- Firm has compliance requirements (IRS Pub 4557, FTC Safeguards Rule) that prefer local data storage

**The pitch:**
> *"Your clients' SSNs, bank accounts, and income — all encrypted on a box in your office. During tax season, the AI processes 50 documents at once without slowing down. No cloud delays, no data leaving your building. And your cyber insurance carrier will love that your client data isn't floating around on someone else's servers."*

---

## The Install — Step by Step

### Step 1: Arrive + Understand Their Workflow (15 minutes)

1. Ask:
   - How many clients? (returns per year)
   - What types? (individual 1040, business 1120/1065/1120-S, trusts 1041, estates 706, non-profit 990)
   - What tax software? (Drake, Lacerte, ProSeries, UltraTax, ATX)
   - How do clients currently send documents? (email, drop off, mail, portal)
   - Do they do bookkeeping/payroll? (QBO, Xero, ADP, Gusto)
   - What's their busiest period? (Usually Jan 15 - Apr 15 and Sep-Oct for extensions)
   - How many staff? (preparers, reviewers, admin)
2. Ask to see:
   - Their client intake checklist (what documents they request)
   - Their engagement letter template
   - How they track return status (spreadsheet, practice management software, whiteboard)

### Step 2: Create Workspace (10 minutes)

1. `setup.adc3k.com` → New Client Workspace
2. Type: Accounting — Tax / Bookkeeping / Full Service
3. Number of clients, number of staff
4. **Enable: MFA required for all users and clients.** Non-negotiable.

### Step 3: Client Portal Setup (20 minutes)

**This is the highest-impact feature.** It replaces the email chaos.

1. Click **"Client Portal"**
2. Configure:
   - Firm branding (logo, colors)
   - Login method: email + password + MFA (text code or authenticator app)
   - Client capabilities:
     - [x] Upload documents
     - [x] View uploaded documents
     - [x] Download completed returns
     - [x] E-sign engagement letters and authorizations
     - [x] Message the firm securely
     - [x] View status of their return ("Received" → "In Progress" → "Review" → "Ready for Signature" → "Filed")
3. **Document categories** (pre-built for tax):
   - Income: W-2, 1099-INT, 1099-DIV, 1099-NEC, 1099-MISC, 1099-B, K-1, SSA-1099
   - Deductions: Mortgage interest (1098), property tax, charitable receipts, medical expenses
   - Business: P&L, balance sheet, mileage log, home office worksheet
   - Prior year return
   - ID verification (driver's license, SSN card — required by some firms)
4. **AI document reading:**
   - Client uploads a W-2 → AI reads it → extracts: employer, wages, federal tax withheld, state tax, SS wages
   - Client uploads a 1099-DIV → AI reads → extracts: ordinary dividends, qualified dividends, capital gains distributions
   - Data is organized by category and pre-populated for the preparer
5. **Missing document detection:**
   - AI compares uploaded docs to prior year return
   - *"Client had 1099-INT from Chase last year but hasn't uploaded one this year. Flag?"*
   - Auto-sends: *"Hi [name], we noticed you haven't uploaded your 1099-INT from Chase. Please upload it when you receive it: [link]"*

### Step 4: Engagement Letters + Intake (10 minutes)

1. Click **"Documents"** → **"Templates"**
2. Upload their engagement letter template (or use the standard one)
3. AI personalizes per client:
   - Client name, services, fee, tax year
   - E-signature enabled — client signs in the portal
4. **Intake questionnaire:**
   - Load the standard tax intake (or customize):
     - Filing status, dependents, life changes (married, divorced, new baby, bought/sold home)
     - Income sources, deductions, credits
     - Estimated tax payments made
     - Bank info for direct deposit of refund
   - Client completes in the portal before their appointment or before prep begins

### Step 5: Workflow / Return Tracking (15 minutes)

1. Click **"Workflow"**
2. Set up return status pipeline:
   ```
   Engagement Signed → Documents Received → Waiting for Missing Docs →
   In Preparation → In Review → Ready for Client Signature →
   Client Signed → E-Filed → Accepted by IRS/State → Complete
   ```
3. Assign roles:
   - **Preparer:** moves return from "In Preparation" to "In Review"
   - **Reviewer:** moves from "In Review" to "Ready for Client Signature" (or back to Preparer if issues)
   - **Admin:** monitors overall pipeline, sends follow-ups
4. **Dashboard view:**
   - How many returns at each stage
   - Bottleneck alerts: "23 returns waiting for missing documents" or "5 returns in review for 7+ days"
   - Due date alerts: "42 returns due April 15 are still in preparation"

### Step 6: Deadline Tracker (10 minutes)

1. Click **"Deadlines"**
2. Pre-loaded deadlines:
   - **Jan 31:** W-2, 1099 filing deadline (employers/payers)
   - **Mar 15:** S-Corp (1120-S), Partnership (1065) due
   - **Apr 15:** Individual (1040), C-Corp (1120), Trust (1041) due
   - **Jun 15:** Q2 estimated tax payment
   - **Sep 15:** Extended S-Corp/Partnership due, Q3 estimated
   - **Oct 15:** Extended Individual due
   - **Dec 15:** Q4 estimated tax payment
   - **Jan 15 (next year):** Q4 estimated (some jurisdictions)
3. Payroll deadlines (if applicable):
   - 941 quarterly, 940 annual, state withholding
4. Custom deadlines: add per-client items (e.g., entity state filings, local returns)
5. AI alerts:
   - 30 days before: *"42 individual returns due April 15. 18 are not yet in preparation."*
   - 7 days before: *"URGENT: 5 returns due April 15 are still waiting for missing documents."*
   - Day of: *"Today is the deadline. 2 returns not filed — extend or complete NOW."*

### Step 7: AI Phone (10 minutes)

1. Greeting: *"Thank you for calling [Firm Name]. I can help you check the status of your return, schedule an appointment, or answer questions about tax documents. How can I help?"*
2. Key routing:
   - **"Is my return ready?"** → AI checks status → *"Your return is currently in review. We expect it to be ready for your signature by [date]."*
   - **"What documents do I need?"** → AI provides the standard checklist for their client type
   - **"I need to schedule an appointment"** → books on the calendar
   - **"I have a tax question"** → routes to a preparer (AI does NOT give tax advice)
   - **Tax season overflow:** When all lines are busy, AI catches every call
3. **After hours:** AI takes messages and answers status questions 24/7

### Step 8: Automated Communications (5 minutes)

- [x] **Tax season kickoff (January):** *"It's tax time! Log into your portal to upload your documents: [link]. Here's your personalized checklist of what we need."*
- [x] **Document received confirmation:** *"We received your W-2. We're still waiting for: 1099-INT, mortgage statement."*
- [x] **Missing document reminder (weekly):** *"Reminder: we still need your [document] to complete your return."*
- [x] **Return ready for signature:** *"Your [year] tax return is ready! Log in to review and sign: [link]"*
- [x] **Return filed:** *"Your return has been e-filed. Expected refund: $X, estimated deposit date: [date]."*
- [x] **Estimated tax reminders (quarterly):** *"Your Q2 estimated tax payment of $X is due June 15. Pay online: [link]"*
- [x] **Referral request (after filing):** *"Thank you for choosing [Firm]! Know someone who needs tax help? Refer them and receive $X off next year's prep."*
- [x] **Year-end planning (November):** *"Year-end tax planning: let's review your situation before December 31. Schedule a call: [link]"*

---

## Training (25 minutes)

### Preparers (10 minutes)
1. Client portal — how documents appear, how AI-extracted data looks
2. Workflow — how to move returns through the pipeline
3. Document Q&A — how to ask the AI questions about a client's uploaded docs
4. **Key line:** *"The AI reads the W-2 for you. Verify it, don't re-enter it. Check the numbers against the document — if the AI read it right (it's right 95%+ of the time), just move on."*

### Admin (10 minutes)
1. Pipeline dashboard — where things are stuck
2. Missing document follow-ups — how the automated reminders work
3. Phone system — how AI routes calls

### Partners/Owners (5 minutes)
1. Dashboard — returns by status, deadline tracker, capacity
2. Revenue report — fees by client, by service type
3. Referral tracking — who's sending new clients

---

## Before You Leave — Final Checklist

- [ ] Client portal live with MFA enabled
- [ ] Document categories configured for their practice type
- [ ] AI document reading tested (upload a sample W-2, verify extraction)
- [ ] Engagement letter template loaded and working
- [ ] Workflow pipeline configured with correct stages
- [ ] All deadline dates entered (federal + state)
- [ ] AI phone live and routing correctly
- [ ] Automated communications turned on
- [ ] At least 1 preparer has done a full demo: upload doc → AI reads → verify → pipeline movement
- [ ] MFA confirmed working for staff AND client logins
- [ ] Quick Start card on each preparer's desk
- [ ] Service agreement signed

---

## Seasonal Considerations

**This business is SEASONAL.** The install should be timed appropriately.

| Install Window | Pros | Cons |
|----------------|------|------|
| **November-December** (BEST) | Full system ready before January rush. Staff has time to learn. | Firm may be distracted by year-end planning work. |
| **January** (OK) | Urgent motivation — they feel the pain. | Limited time to train before the flood starts. |
| **February-April** (AVOID) | | They are drowning. Don't install during tax season. |
| **May-September** (GOOD) | Off-season. Time to train, load clients, customize. | Less urgency — they may procrastinate on adoption. |
| **October** (OK) | Extension deadline creates urgency, gives 2 months before Jan. | Still busy with extensions. |

**If they call you in March wanting an install:** Say *"Let's schedule for May when tax season is over. You'll have time to set it up right, and it'll be ready for next January."*

---

## Troubleshooting

| Problem | What to Do |
|---------|------------|
| "The AI misread a document" | It happens, especially with handwritten docs or poor scans. The preparer should always verify against the source document. AI accuracy improves with higher-quality scans. |
| "My client can't figure out the portal" | Walk the client through it via phone if needed. Or: set up the firm to accept documents via a simple text-to-upload (client texts a photo → it goes to their portal). Lower friction. |
| "The workflow doesn't match how we do things" | Customize the pipeline stages. Every firm is different. Some don't have a formal review step. Some have multiple review levels. Match their process. |
| "We have 800 clients and can't enter them all" | Import from their tax software. Drake, Lacerte, ProSeries all export client lists as CSV. Load the batch. |
| "The AI gave tax advice" | It should NOT. Check settings — "Tax Advice" must be OFF. If it somehow happened, document it and call ADC. |

---

## What You Should NOT Do

1. **NEVER look at client financial data.** SSNs, income, bank accounts — none of your business. Use dummy data.
2. **NEVER give tax advice.** Even if you know the answer. *"That's a great question for your accountant."*
3. **NEVER skip MFA setup.** This is non-negotiable for financial data portals.
4. **NEVER email yourself client data or screenshots.**
5. **NEVER install during peak tax season** (Feb-Apr) unless they specifically insist and understand the training limitations.
6. **NEVER tell them to stop using their tax software.** We supplement, not replace. Drake/Lacerte/ProSeries stays.

---

## Glossary

| Word | What It Means |
|------|---------------|
| **CPA** | Certified Public Accountant. Licensed by the state. Can sign tax returns and audit financials. |
| **EA** | Enrolled Agent. Federally licensed tax preparer. Can represent clients before the IRS. |
| **Engagement letter** | A contract between the firm and the client that defines what services will be provided, fees, and responsibilities. |
| **Extension** | Filing Form 4868 to get more time to file (usually 6 months). The tax is still due by the original deadline — only the paperwork is extended. |
| **E-file** | Electronic filing with the IRS. Faster refunds, confirmation of receipt. |
| **MFA** | Multi-Factor Authentication. Login requires password + a code from their phone. Prevents unauthorized access. |
| **Portal** | A secure website where clients upload documents and download returns. Replaces insecure email. |
| **Preparer** | The person who actually prepares the tax return. May or may not be a CPA. |
| **Reviewer** | A senior person (usually a CPA or partner) who checks the preparer's work before it goes to the client. |
| **K-1** | A tax form from partnerships or S-corps showing the owner's share of income, deductions, and credits. These are ALWAYS late and ALWAYS the document holding up the return. |
