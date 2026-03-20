# ADC AI Install Playbook — Property Management

## Who This Is For
You're an ADC installer. This covers residential property managers, apartment complexes, multi-family operators, HOA management companies, and commercial property managers. If they manage properties for owners and deal with tenants, this playbook applies.

---

## What You're Installing
An AI system that handles tenant communication and vendor coordination so the property manager isn't a 24/7 answering service. When you're done, the PM will be able to:

- **Tenant portal** — tenants submit maintenance requests, pay rent, view lease info, and communicate — all through one portal. No more calls and texts to the manager's personal phone at 11 PM.
- **AI maintenance dispatch** — tenant texts "my AC broke" → AI asks clarifying questions ("Is it blowing warm air or not turning on at all?") → AI dispatches the right vendor (HVAC company) with the details → vendor gets the work order on their phone → tenant gets an ETA. No human involved unless it's an emergency.
- **Rent collection** — automated reminders, online payment, late fee calculation, payment tracking. AI texts: *"Rent is due in 3 days"* → *"Rent is past due, a $50 late fee will apply on the 6th"* → escalation to PM if unpaid by Day 10.
- **Listing + showing** — vacant unit? AI lists it, handles inquiries, schedules showings, pre-qualifies applicants. *"Do you have any income requirements?"* → *"Yes, income must be 3x the rent. Would you like to schedule a tour?"*
- **Lease management** — AI tracks every lease: start date, end date, renewal date, rent amount, deposit, pet deposit, special terms. Alerts 90 days before expiration: *"Unit 204's lease expires June 30. Start renewal process?"*
- **Owner reporting** — monthly reports to property owners: rent collected, expenses, maintenance costs, occupancy rate, net income. Automated. Branded.
- **AI phone** — handles all incoming calls: tenants, prospective tenants, vendors, owners. Routes to the right place without PM answering every call.

**What it replaces:** The tenant calling at midnight because the toilet is running. The property manager's phone blowing up with rent questions. The owner who wants a monthly report and never gets one. The vacant unit sitting empty for 6 weeks because nobody followed up on the leads.

---

## Client Minimum Requirements

### Tier 1: Cloud-Only

| Requirement | Minimum | Recommended | Why |
|-------------|---------|-------------|-----|
| **Internet** | 25 Mbps | 50+ Mbps | Portal, phone, reporting all running. |
| **Computer** | Any modern, 8GB RAM | 16GB RAM, dual monitors | PM spends all day on screen — portal, email, accounting. |
| **Phone** | iPhone or Android, recent | Good smartphone | For after-hours emergency routing. |
| **Current software** | None required | If they use AppFolio, Buildium, Rent Manager, or Yardi — we integrate alongside. | |
| **Accounting** | QuickBooks or their PM software | | For rent tracking and owner reporting. |

**Cost to client:** $0 hardware + monthly subscription
**Best for:** PMs managing 20-100 units with existing equipment

### Tier 2: ADC Starter Kit

| Item | Spec | Approx. Cost | Notes |
|------|------|-------------|-------|
| Office PC | Intel i5, 16GB, SSD | $500-700 | Dedicated PM workstation |
| Dual monitors | 24" x2 | $300-400 | One for portal/tenants, one for accounting/email |
| Tablet | iPad | $400-500 | For property inspections + photos |
| Scanner | Fujitsu ScanSnap | $400 | Lease scanning, vendor invoices |
| UPS | 600VA | $60-80 | |
| **Total** | | **$1,660-2,080** | |

### Tier 3: NVIDIA DGX Spark

| Item | Spec | Cost |
|------|------|------|
| **NVIDIA DGX Spark** | GB10 Grace Blackwell, 128GB, 1 PFLOPS FP4, 4TB encrypted NVMe | **$4,699** |
| Office kit | | $1,660-2,080 |
| **Total** | | **~$6,360-6,780** |

**When to recommend DGX Spark:**
- Large portfolio (200+ units) — heavy data, lots of tenants, vendors, and owners
- Manages subsidized / Section 8 housing with HUD compliance requirements
- Commercial PM handling NDAs and tenant financials
- PM who doesn't want tenant SSNs, bank info, or lease documents in the cloud

**The pitch:**
> *"Every tenant application, every SSN, every bank account for rent autopay — it's all encrypted and on-site. Your tenants' data stays in your office, not on someone else's server. And for 200+ units, the AI processes maintenance requests, rent reminders, and owner reports all simultaneously without slowing down."*

---

## The Install — Step by Step

### Step 1: Arrive + Understand the Portfolio (15 minutes)

1. Ask the PM:
   - How many units? What types? (apartments, SFH, duplexes, commercial)
   - How many properties / locations?
   - How many owners? (self-owned vs. managing for others)
   - How do tenants currently pay rent? (check, Venmo, online portal, cash)
   - How do they handle maintenance? (tenant calls PM → PM calls vendor, or tenant calls vendor directly)
   - What's their biggest headache? (Usually: after-hours calls, rent collection, or vacant units)
2. Get:
   - A unit list (address, unit #, tenant name, rent amount, lease dates)
   - A vendor list (who they call for plumbing, HVAC, electrical, appliances, pest, lawn, cleaning)
   - A sample owner report (so we can match the format)

### Step 2: Create Workspace (10 minutes)

1. `setup.adc3k.com` → New Client Workspace
2. Type: Property Management — Residential / Commercial / Mixed
3. Number of units, number of properties, number of owners

### Step 3: Load Properties + Units (20 minutes)

1. Click **"Properties"**
2. For each property:
   - Address
   - Property type (apartment complex, SFH, duplex, commercial)
   - Number of units
   - Owner (if managing for someone else)
3. For each unit:
   - Unit number/identifier
   - Bedrooms/bathrooms
   - Square footage
   - Monthly rent
   - Current tenant (or "Vacant")
   - Lease start/end date
   - Security deposit amount
   - Pet deposit (if applicable)
   - Special terms (parking spot, storage unit, utility arrangement)
4. **If they have a spreadsheet or CSV:** Upload it. AI parses and loads the data.
5. **If it's all on paper or in their head:** This step takes longer. Sit with them and enter it.

### Step 4: Set Up Vendor Network (15 minutes)

**Property management vendors are different from field service vendors.** PMs don't buy parts — they dispatch entire vendors.

1. Click **"Vendors"**
2. For each vendor:
   - Company name
   - Trade (plumbing, HVAC, electrical, appliance repair, pest control, lawn care, cleaning/turnover, locksmith, general handyman)
   - Contact name + phone + email
   - Service area (which properties can they serve?)
   - Pricing: flat rate, hourly, or "call for quote"
   - Do they have a tenant access policy? (some vendors will go direct to the unit with tenant authorization)
   - Insurance on file? (upload cert)
   - Preferred or backup? (for each trade, flag the primary and the backup)
3. **AI dispatch rules:**
   - Plumbing emergency → call Primary Plumber first. If no answer in 15 min → call Backup Plumber.
   - Non-emergency → create work order, vendor picks up next business day
   - After-hours emergency (no hot water, flooding, no AC in summer, no heat in winter, lockout) → route to emergency vendor list

### Step 5: Tenant Portal + Maintenance Requests (15 minutes)

1. Click **"Tenant Portal"**
2. Configure:
   - Login method: email + password, or phone number + code (simpler for tenants)
   - Features visible to tenants:
     - [x] Submit maintenance request
     - [x] Pay rent online
     - [x] View lease info
     - [x] View payment history
     - [x] Contact management
     - [ ] View other tenants' info (NEVER — privacy)
3. **Maintenance request flow:**
   - Tenant opens portal → "Submit Maintenance Request"
   - Selects category: Plumbing / Electrical / HVAC / Appliance / Pest / Locks / Other
   - AI asks clarifying questions:
     - Plumbing: "Is water actively leaking?" → Yes = emergency dispatch → No = standard work order
     - HVAC: "Is it not cooling/heating at all, or just not well?" → determines urgency
     - Pest: "What type of pest? How long has this been happening?"
   - Tenant adds photos (optional but encouraged)
   - Request generates a work order
   - AI dispatches to the right vendor based on trade + property + urgency
   - Vendor gets: tenant name, unit, property address, issue description, photos, access instructions
   - Tenant gets: *"Your maintenance request has been submitted. [Vendor name] will contact you to schedule. Reference #12345."*
4. **Show the PM:** *"You don't touch any of this unless it's flagged as an emergency or the tenant escalates. The AI handles the triage, the dispatch, and the tenant communication. You see it all on your dashboard, but you're not in the middle of every toilet problem."*

### Step 6: Rent Collection + Automation (15 minutes)

1. Click **"Rent"**
2. Set up payment processing:
   - Connect Stripe, or their existing payment processor
   - Enable ACH (bank transfer — lower fees), credit/debit card
   - Set rent due date (typically 1st of month)
   - Set grace period (typically 3-5 days)
   - Set late fee amount and trigger date
3. Automated rent communication:
   - **5 days before due:** *"Reminder: your rent of $X is due on the 1st. Pay online: [link]"*
   - **Due date:** *"Rent is due today. Pay online: [link]"*
   - **Grace period expired:** *"Your rent is past due. A late fee of $X will be applied on [date]. Pay now to avoid the fee: [link]"*
   - **10 days late:** Alert to PM: *"Unit 204 — [tenant name] — rent 10 days past due, $X + late fee. Action needed."*
   - **30 days late:** PM decides next step (notice to pay or quit, etc.)
4. **Auto-pay:** Tenants can set up autopay through the portal. AI confirms each month: *"Your autopay of $X will be processed on [date]."*

### Step 7: Lease Management (10 minutes)

1. Click **"Leases"**
2. Upload existing leases (scan or PDF) — AI reads them and extracts:
   - Tenant name, unit, rent, deposit, start/end date, renewal terms, special clauses
3. Set up renewal workflow:
   - **90 days before expiration:** Alert PM → "Unit 204 lease expires June 30. Renew or let expire?"
   - If renew: AI generates renewal offer with new terms (PM sets the rent increase, if any)
   - Tenant gets: *"Your lease at [address] expires June 30. We'd like to offer a renewal at $X/month. Review and sign online: [link]"*
   - If not renewing: AI starts vacancy prep (schedule turnover cleaning, listing creation, showing availability)
4. **Move-in/move-out checklists:**
   - Condition report template with photos
   - AI compares move-in vs. move-out photos
   - Flags potential deposit deductions: *"Move-out inspection: bedroom wall has hole not present at move-in. Estimated repair: $150."*

### Step 8: Owner Reporting (10 minutes)

1. Click **"Owner Reports"**
2. For each owner, set:
   - Properties they own
   - Reporting frequency (monthly is standard)
   - Report format:
     - Rent collected
     - Expenses (maintenance, utilities, insurance, management fee)
     - Net income
     - Occupancy rate
     - Maintenance summary
     - Upcoming lease expirations
3. AI generates and sends the report automatically on the 5th of each month (after rent is collected)
4. **Say:** *"Your owners get a professional report every month without you lifting a finger. It pulls from actual data — rent payments, vendor invoices, maintenance costs. No more spreadsheets."*

### Step 9: Vacancy + Leasing (10 minutes)

1. Click **"Leasing"**
2. When a unit is vacant (or will be):
   - AI generates a listing description from unit details + photos
   - Posts to: Zillow, Apartments.com, Facebook Marketplace, Craigslist (as configured)
   - AI handles inquiries: *"Hi, I'm the leasing assistant for [property]. The unit is a 2BR/1BA at $1,200/month. Would you like to schedule a tour?"*
   - AI pre-qualifies: income, credit range, move-in date, pets
   - Schedules showings (self-guided or with PM)
   - After showing: *"Thank you for visiting [property]. Would you like to apply? Here's the link: [link]"*
   - Application processing: AI collects info, runs credit/background (through integrated screening service), presents results to PM for decision
3. **Say:** *"From the day a unit goes vacant to the day a new tenant signs, the AI handles the advertising, the inquiries, the showings, and the applications. You just make the final call on who gets the keys."*

### Step 10: AI Phone (10 minutes)

1. Set up greeting: *"Thank you for calling [Management Company / Property Name]. I can help with maintenance requests, rent payments, leasing inquiries, or connect you with your property manager. How can I help?"*
2. Routing:
   - **"Something is broken"** → maintenance flow (see Step 5)
   - **"I want to pay rent"** → sends payment link via text
   - **"I'm interested in renting"** → leasing flow (see Step 9)
   - **"I'm an owner"** → route to PM
   - **Emergency (flooding, fire, gas leak, break-in)** → immediate route to PM cell + emergency vendor dispatch
3. After hours: AI handles everything except emergencies (those ring PM's cell)

---

## Training (25 minutes)

### Property Manager (15 minutes)
Dashboard walkthrough:
1. **Units overview** — occupancy, rent status (paid, pending, late), maintenance open/closed
2. **Maintenance queue** — open requests, vendor status, tenant updates
3. **Rent tracker** — who paid, who hasn't, autopay enrolled, late fees
4. **Lease calendar** — upcoming expirations, renewals in progress
5. **Owner reports** — preview what owners will see

### Maintenance Coordinator (if separate person — 5 minutes)
1. How to review AI-dispatched work orders
2. How to override vendor assignment
3. How to close out completed work orders
4. How to handle emergency escalations

### Front Desk / Leasing (if applicable — 5 minutes)
1. How to handle walk-in leasing inquiries
2. How to schedule showings manually
3. How to process applications

---

## Before You Leave — Final Checklist

- [ ] All properties and units loaded (address, unit, tenant, rent, lease dates)
- [ ] At least 5 vendors set up across key trades (plumbing, HVAC, electrical, handyman, cleaning)
- [ ] Tenant portal live (test: submit a maintenance request from your phone)
- [ ] Rent collection set up with payment processor connected
- [ ] Automated rent reminders turned on
- [ ] Lease expiration alerts configured (90/60/30 day)
- [ ] Owner report template configured for at least 1 owner
- [ ] AI phone is live
- [ ] Vacancy/leasing flow tested (if they have a vacant unit)
- [ ] PM can view dashboard without help
- [ ] Quick Start card at PM's desk
- [ ] Service agreement signed

---

## Troubleshooting

| Problem | What to Do |
|---------|------------|
| "Tenant says they can't log into the portal" | Reset their password. If they never set one up, resend the invite text/email. Most "can't log in" = never activated. |
| "The AI dispatched the wrong vendor" | Check the vendor-trade mapping and service area. Adjust if a vendor was assigned to the wrong trade or the wrong property. |
| "Tenant is complaining about getting too many texts" | Adjust communication frequency in their tenant profile. Some tenants hate texts — offer email as an alternative. |
| "Owner wants a different report format" | Customize their report template. Some owners want a simple P&L, others want every receipt itemized. Adjust to their preference. |
| "Rent payment failed" | Check if the tenant's bank info is correct. ACH failures are usually wrong account/routing numbers. Resend payment link for them to re-enter. |
| "The AI approved a maintenance request I wouldn't have" | AI dispatches based on your rules. If the threshold for auto-dispatch is too low, increase it. Set certain request types to require PM approval before dispatch. |

---

## What You Should NOT Do

1. **Don't access tenant personal information** (SSN, bank accounts, credit reports). Use test data during setup.
2. **Don't advise on landlord-tenant law.** Evictions, security deposit disputes, fair housing — that's for their attorney. Don't give legal advice.
3. **Don't set rent amounts.** Enter what they tell you. If they ask what rent should be, say: *"That's a market question — you know your market better than I do."*
4. **Don't interact with tenants as if you're the property manager.** During install, if a tenant approaches you, say: *"I'm just the tech person — check with [PM name] for any questions about your unit."*
5. **Don't promise reduced maintenance costs.** The AI dispatches faster, not cheaper. Vendor prices are vendor prices.

---

## Glossary

| Word | What It Means |
|------|---------------|
| **PM** | Property Manager. The person who manages the property on behalf of the owner. |
| **Unit** | An individual rental space — an apartment, a house, a suite. |
| **Turnover** | When a tenant leaves and the unit is prepped for the next tenant. Cleaning, painting, repairs. |
| **Vacancy rate** | Percentage of units that are empty. Lower = better. |
| **NOI** | Net Operating Income. Rent collected minus expenses. What the owner actually makes. |
| **Cap rate** | Capitalization rate. NOI ÷ property value. How investors measure return. Don't worry about this unless an owner asks. |
| **Section 8** | Government housing assistance. Tenant pays partial rent, government pays the rest. Extra compliance requirements. |
| **Work order** | A maintenance task assigned to a vendor. |
| **Lease renewal** | Extending a tenant's lease for another term (usually 12 months). |
| **Move-in / move-out inspection** | A documented walkthrough with photos at the start and end of a lease. Used to determine deposit deductions. |
| **Grace period** | Days after rent is due before a late fee applies. Typically 3-5 days. Set by lease terms and sometimes by state law. |
