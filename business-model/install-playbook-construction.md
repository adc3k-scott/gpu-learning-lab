# ADC AI Install Playbook — Construction / General Contractor

## Who This Is For
You're an ADC installer. This covers general contractors, remodelers, custom home builders, roofing companies, and specialty contractors who manage projects with multiple subcontractors. If they run jobs with subs, permits, and draw schedules, this playbook applies.

**This is NOT the same as the field services playbook** (plumber/electrician). Field services = one-visit repairs. Construction = multi-week/month projects with subs, stages, and progress payments. Different animal.

---

## What You're Installing
An AI system that keeps the chaos organized. Construction projects have dozens of moving parts — subs, inspections, materials, change orders, weather delays, draw schedules, lien waivers. When you're done, the GC will be able to:

- **Project dashboard** — every active job on one screen. What stage it's in, what's next, who's scheduled, what's behind.
- **Sub management** — track every subcontractor: their schedule, their scope, their insurance certs, their lien waivers. AI alerts when a cert is expiring.
- **Change order workflow** — homeowner wants to add a bathroom? AI generates the change order with cost impact, schedule impact, and gets a digital signature. No more verbal agreements that turn into disputes.
- **Draw schedule / pay app** — AI tracks progress by stage. When framing is done, it generates the draw request with photos of completed work. Lender or owner approves. Money moves.
- **Daily log** — foreman takes photos and notes each day. AI compiles them into a daily report. Weather, crew, work completed, materials delivered, issues. Timestamped and photo-documented.
- **Permit tracking** — AI tracks what permits are needed, when inspections are scheduled, and alerts when an inspection is coming up or a permit is about to expire.
- **Material ordering** — AI tracks material lists by project, compares vendor pricing, and alerts when delivery needs to be scheduled to match the project timeline.
- **Customer updates** — homeowner gets a weekly text or email: photos of progress, what happened this week, what's coming next week. No more "when will my house be done?" calls.

**What it replaces:** The legal pad in the truck with the project schedule. The stack of lien waivers in the filing cabinet that nobody checks. The change order that was agreed to with a handshake and ended up in court. The draw request that took 2 weeks because the GC couldn't find the right photos.

---

## Client Minimum Requirements

### Tier 1: Cloud-Only

| Requirement | Minimum | Recommended | Why |
|-------------|---------|-------------|-----|
| **Internet (office)** | 25 Mbps | 50+ Mbps | Photo uploads, document generation, project management. |
| **Cell signal (job sites)** | Usable LTE | 5G preferred | Daily logs, photos, and sub coordination happen on-site. If they build in rural areas with no signal, they'll need to sync when they get signal. |
| **Computer (office)** | Any, 8GB RAM | 16GB RAM, dual monitors | For project management, draw schedules, vendor ordering. |
| **Phone / Tablet** | iPhone or Android, recent model | iPad or large phone | For daily logs, progress photos, change orders in the field. Camera quality matters. |
| **Current software** | None required | If they use Buildertrend, CoConstruct, Procore, or similar — we integrate alongside | |

**Cost to client:** $0-500 + monthly subscription
**Best for:** Small GCs running 2-5 projects at a time

### Tier 2: ADC Starter Kit

| Item | Spec | Approx. Cost | Notes |
|------|------|-------------|-------|
| Office PC | Intel i5, 16GB RAM, 512GB SSD | $500-700 | Project management hub |
| Dual monitors | 24" 1080p x2 | $300-400 | One for project dashboard, one for documents/email |
| Field tablet | iPad + Otterbox + screen protector | $500-650 | Job sites are dirty. Protect it. |
| Scanner | Fujitsu ScanSnap | $400 | For sub invoices, insurance certs, permits |
| Mobile printer (optional) | Brother PocketJet | $300-400 | Print change orders on-site for signature |
| UPS | 600VA | $60-80 | |
| **Total** | | **$2,060-2,630** | |

### Tier 3: NVIDIA DGX Spark

| Item | Spec | Cost |
|------|------|------|
| **NVIDIA DGX Spark** | GB10 Grace Blackwell, 128GB, 1 PFLOPS FP4, 4TB encrypted NVMe | **$4,699** |
| Office kit | | $2,060-2,630 |
| **Total** | | **~$6,760-7,330** |

**When to recommend DGX Spark for construction:**
- Custom home builder handling high-net-worth clients (data privacy)
- GC with 10+ active projects (heavy compute for simultaneous project tracking)
- Government/military construction (data residency requirements)
- GC who wants AI-powered estimating trained on their actual project costs (local model training)

**The pitch:**
> *"Every photo, every change order, every draw request, every daily log — encrypted and on-site. Your project data is your competitive advantage. And the AI learns from your actual costs — after 10 projects, it estimates better than any database because it knows YOUR numbers, YOUR subs, YOUR market."*

---

## The Install — Step by Step

### Step 1: Arrive + Understand Their Operation (20 minutes)

This install requires more discovery than others. Construction is complex.

1. Meet with the GC/owner. Ask:
   - How many active projects at a time? (2-5 = small, 5-15 = mid, 15+ = large)
   - What types? (custom homes, remodels, commercial tenant buildout, roofing, etc.)
   - How many regular subs? (get names + trades)
   - How do they currently track projects? (Buildertrend, CoConstruct, Procore, Excel, paper)
   - How do they handle draw requests? (bank draws, owner progress payments, GMP billing)
   - How do they handle change orders? (verbal, written, formal CO forms)
   - Who does estimating? (owner, estimator, sub bids)
   - Do they pull their own permits or does the sub? (varies by trade)
2. Ask to see:
   - A current project folder (paper or digital)
   - A recent draw request or pay application
   - A recent change order
   - Their sub list with contact info

### Step 2: Create Workspace (10 minutes)

1. `setup.adc3k.com` → New Client Workspace
2. Type: Construction — Residential / Commercial / Remodeling / Specialty
3. Average project duration, average project value
4. Number of active projects
5. Number of in-house crew + office staff

### Step 3: Build the Sub List (15 minutes)

**Subs make or break a GC. This database is gold.**

1. Click **"Subcontractors"**
2. For each sub they regularly use:
   - Company name
   - Trade (concrete, framing, electrical, plumbing, HVAC, roofing, drywall, paint, flooring, landscape, etc.)
   - Contact name + phone + email
   - License number
   - Insurance: GL expiration, WC expiration, auto expiration
   - Bond info (if applicable)
   - Payment terms (progress billing, per milestone, upon completion)
   - Notes (reliability, quality, typical crew size)
3. **Insurance cert tracking:**
   - Upload current certificates of insurance
   - AI reads expiration dates and sets alerts
   - 30 days before expiration: *"[Sub name]'s GL policy expires in 30 days. Request updated cert."*
   - **Say:** *"If a sub's insurance lapses and someone gets hurt on your job, YOU'RE on the hook. This watches it so you don't have to."*

### Step 4: Set Up Project Template (20 minutes)

1. Click **"Projects"** → **"Project Templates"**
2. Build a template for their most common project type:

   **Example — Custom Home:**
   ```
   Phase 1: Pre-Construction
     □ Permits pulled
     □ Survey complete
     □ Engineering approved
     □ Sub contracts signed

   Phase 2: Site Work
     □ Clearing/grading
     □ Foundation (concrete sub)
     □ Plumbing rough-in (under slab)
     □ Foundation inspection ← INSPECTION

   Phase 3: Framing
     □ Framing complete
     □ Framing inspection ← INSPECTION
     □ Windows/doors installed
     □ Roof dried in

   Phase 4: Rough-In
     □ Electrical rough
     □ Plumbing rough
     □ HVAC rough
     □ Rough inspection ← INSPECTION
     □ Insulation
     □ Insulation inspection ← INSPECTION

   Phase 5: Finish
     □ Drywall
     □ Trim/cabinets
     □ Flooring
     □ Paint
     □ Electrical finish
     □ Plumbing finish
     □ HVAC finish

   Phase 6: Close-Out
     □ Final inspection ← INSPECTION
     □ Punch list
     □ Certificate of Occupancy
     □ Final draw/payment
     □ Warranty walkthrough (30/60/1yr)
   ```

3. **Each phase ties to:**
   - Which subs are involved
   - Which inspections are needed
   - What % of the total contract it represents (for draw schedule)
   - Materials needed

4. Ask the GC: *"Walk me through your typical project from permit to CO. What are the stages?"* Build it in their words, their order.

### Step 5: Draw Schedule / Pay Application (15 minutes)

1. Click **"Financials"** → **"Draw Schedule Template"**
2. Set up the standard draw schedule:

   | Stage | % of Contract | Release Condition |
   |-------|--------------|-------------------|
   | Deposit / mobilization | 10% | Contract signed |
   | Foundation complete | 15% | Foundation inspection passed |
   | Framing / dry-in | 20% | Framing inspection passed |
   | Rough-in complete | 15% | Rough inspection passed |
   | Drywall / finish started | 15% | Drywall hung, finish materials on-site |
   | Substantial completion | 20% | Final inspection passed |
   | Final / retainage | 5% | Punch list complete, CO issued |

3. **How AI draws work:**
   - Foreman marks phase complete in the app
   - Uploads progress photos (required — banks/owners want documentation)
   - AI generates the draw request or AIA G702/G703 pay application
   - Includes: photos, completed items, requested amount, retainage balance
   - GC reviews and submits to bank/owner
   - **Say:** *"The draw request builds itself from the photos and progress your foreman logs. No more scrambling to put together a draw package at the end of the month."*

### Step 6: Change Order Workflow (10 minutes)

1. Click **"Change Orders"**
2. Set up the standard CO form with:
   - Description of change
   - Reason (owner request, unforeseen condition, code requirement, design error)
   - Cost impact (itemized: labor, material, sub markup, GC markup)
   - Schedule impact (adds X days)
   - Cumulative CO total (running total of all changes)
3. **Workflow:**
   - Change is identified → GC creates CO in the app
   - AI prices it using historical data + sub quotes
   - Owner/architect gets a text with the CO: description, photos (if applicable), cost, schedule impact
   - Owner approves digitally (signature on phone)
   - CO is logged, contract value updated, draw schedule adjusted
4. **Say:** *"Every change is documented, priced, and signed before the work happens. No more 'I thought that was included' arguments at the end of the job."*

### Step 7: Daily Log (10 minutes)

1. Click **"Daily Log"**
2. Set up the template:
   - Date, weather (high/low, precipitation, wind — auto-pulled by location)
   - Crew on-site (in-house + subs — who, how many)
   - Work performed (by trade)
   - Materials delivered
   - Visitors / inspections
   - Safety incidents (hopefully none)
   - Photos (minimum 5 per day — document everything)
   - Notes / issues
3. **Show the foreman:**
   - Open app → tap "Daily Log" → fill in → take photos → submit
   - Takes 10-15 minutes at end of day
   - AI compiles it into a formatted report
4. **Say:** *"If there's ever a dispute — a delay claim, a defect argument, an insurance claim — your daily logs with timestamped photos are your defense. This is your CYA system."*

### Step 8: Customer Updates (5 minutes)

1. Click **"Automations"**
   - [x] **Weekly owner update** — every Friday, AI compiles: photos from daily logs, work completed this week, plan for next week, any issues. Owner gets a beautiful email or text with photos.
   - [x] **Inspection passed** — "Great news — your [stage] inspection passed today!"
   - [x] **Milestone reached** — "Your home is now dried in. Here's what it looks like: [photos]"
   - [x] **Weather delay** — "Rain is expected Tuesday-Thursday. We'll resume [work] on Friday."
   - [x] **Completion notice** — "Your project is substantially complete. We'll schedule your walkthrough this week."
2. **Say:** *"Your homeowner will stop calling you every day asking for updates. They get photos and a progress report every Friday automatically. Happy customer = easier draws = more referrals."*

### Step 9: Permit + Inspection Tracking (5 minutes)

1. Click **"Permits"**
2. For each active project, enter:
   - Permit numbers
   - Inspection types required
   - Scheduled inspection dates
3. AI alerts:
   - 48 hours before inspection: *"Rough electrical inspection scheduled for Thursday. Is the work ready?"*
   - Inspection passed/failed: log result
   - Permit expiration: *"Building permit for [project] expires in 60 days. Renew or request extension."*

---

## Training (30 minutes)

### GC / Project Manager (15 minutes)
- Dashboard: all projects at a glance — status, budget, schedule
- Draw request: how it auto-generates from progress logs
- Change orders: create, price, get approval
- Sub insurance tracking: where to see expiring certs

### Foreman / Field (10 minutes)
Two things:
1. **Daily log:** Fill it out every day. Photos, crew, work done, issues. 10-15 minutes.
2. **Mark phase complete:** When a stage is done, tap "Complete" and take the photos. This triggers the draw.

### Office / Admin (5 minutes)
1. Sub cert tracking — where alerts show up
2. Draw requests — how to review and submit
3. Permit calendar — upcoming inspections

---

## Before You Leave — Final Checklist

- [ ] Sub list built with at least their top 10 subs (name, trade, contact, insurance dates)
- [ ] At least 1 project template created for their most common project type
- [ ] Draw schedule template configured
- [ ] Change order template configured
- [ ] Daily log template set up and tested (one test entry with photos)
- [ ] Customer auto-updates turned on
- [ ] At least 1 active project entered with current status
- [ ] Foreman can fill out a daily log without help
- [ ] GC can create a change order without help
- [ ] Quick Start card in the office and in the GC's truck
- [ ] Service agreement signed

---

## Troubleshooting

| Problem | What to Do |
|---------|------------|
| "My foreman won't do the daily log" | This is the hardest habit to build. Start with just photos + one sentence. Lower the bar. 5 photos and "framing continued, electrician here tomorrow" is better than nothing. |
| "The draw schedule doesn't match my bank's format" | Customize the output template. Some banks want AIA G702/G703, some want their own form. Get a copy of their bank's format and we'll match it. |
| "I need to track costs differently" | Construction accounting varies wildly. If they need job costing by CSI division or phase, adjust the budget categories. If they need something we don't support, log it and call ADC. |
| "Sub won't send updated insurance" | That's between the GC and the sub. Our system just flags it. The GC has to enforce it. Some GCs hold payment until certs are current — that works. |
| "Change order pricing is off" | AI pricing is based on averages. The GC should always adjust based on actual sub quotes. The AI gives a starting point, the GC refines it. |

---

## What You Should NOT Do

1. **Don't give construction advice.** You're installing software, not managing a job site. Don't comment on their build quality, schedule, or pricing.
2. **Don't go on the job site without a hard hat and closed-toe shoes.** If they invite you to see a project, dress for it. Safety first.
3. **Don't access financial data beyond what's needed for setup.** Contract values and draw amounts are sensitive.
4. **Don't promise the system replaces their estimator or project manager.** It's a tool, not a person.
5. **Don't interfere with sub relationships.** If a GC and sub have beef, stay out of it.

---

## Glossary

| Word | What It Means |
|------|---------------|
| **GC** | General Contractor. The boss of the job. Hires subs, manages the project, deals with the owner. |
| **Sub** | Subcontractor. A specialist hired by the GC for a specific trade (plumbing, electrical, framing, etc.). |
| **Draw** | A progress payment. The GC completes a phase of work and "draws" money from the bank/owner based on the contract. |
| **Pay app** | Pay application. A formal request for payment (usually AIA G702/G703 format for commercial). Same concept as a draw. |
| **CO** | Change Order. A formal modification to the original contract — changes scope, cost, or schedule. |
| **Punch list** | A list of small items that need to be fixed or completed before the project is officially done. Usually cosmetic — paint touch-ups, missing hardware, etc. |
| **Retainage** | A percentage of each payment held back until the project is complete. Usually 5-10%. Protects the owner against incomplete work. |
| **CO / Certificate of Occupancy** | A document from the building department saying the structure is safe to live in / use. Required before the owner can move in. |
| **Lien waiver** | A document where a sub or supplier gives up their right to file a lien against the property. GCs collect these from subs with every payment. Critical for protecting the owner and getting final draws. |
| **AIA G702/G703** | Standard payment application forms used in commercial construction. Named after the American Institute of Architects. |
| **Rough-in** | The stage where plumbing, electrical, and HVAC are installed inside the walls BEFORE drywall goes up. |
| **Dry-in** | When the building is weather-tight — roof on, windows in, doors hung. Rain can't get in. |
