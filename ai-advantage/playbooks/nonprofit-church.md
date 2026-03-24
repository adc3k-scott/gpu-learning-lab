# ADC AI Install Playbook — Non-Profit / Church / School

## Who This Is For
You're an ADC installer. This covers churches, mosques, synagogues, temples, non-profit organizations, private schools, community centers, food banks, and charitable foundations. If they run on donations, volunteers, and a mission — not profit — this playbook applies.

---

## What You're Installing
An AI system that saves admin hours, keeps donors engaged, and helps them win grants. When you're done, the organization will be able to:

- **AI front desk** — answers calls and messages 24/7. *"What time is Sunday service?" "How do I sign up to volunteer?" "Where do I drop off donations?"* — handled instantly. No more missed calls during busy days.
- **Donation tracking + acknowledgment** — every donation logged, receipted, and thanked automatically. *"Thank you, [name]! Your gift of $100 to [org] has been received. Your tax receipt is attached."* Year-end giving statements generated in one click.
- **Volunteer scheduling** — AI matches volunteers to needs. *"We need 5 people for the food drive Saturday. [Name], you helped last month — can you make it? Reply YES to confirm."*
- **Event management** — registration, reminders, follow-up. *"Family Movie Night is this Friday at 6 PM. You're registered! Bring a blanket. [link to details]"*
- **Grant writing assistant** — AI drafts grant applications from templates and past submissions. Pulls org stats, financials, and impact data into the right format. Turns a 40-hour grant into an 8-hour grant.
- **Member communications** — newsletters, announcements, prayer requests, updates. Segmented by group (youth, seniors, small groups, volunteers). No more "reply all" email chains.
- **Attendance + engagement tracking** — who's showing up, who's drifting away, who's new. *"[Name] hasn't attended in 6 weeks. Suggested action: personal outreach from pastor/director."*

**What it replaces:** The church secretary buried in email. The volunteer coordinator making 40 phone calls for Saturday's event. The executive director spending 3 weeks on a grant application. The donor who gave $500 and never got a thank-you. The family who stopped coming and nobody noticed.

---

## Client Minimum Requirements

### Tier 1: Cloud-Only

| Requirement | Minimum | Recommended | Why |
|-------------|---------|-------------|-----|
| **Internet** | 25 Mbps | 50+ Mbps | Communications, video streaming, data sync. |
| **Existing software** | None required | Planning Center, Breeze, or Bloomerang — we integrate | |
| **Computer** | Any modern laptop/desktop | Chromebook is fine for most | For admin, communications, grant writing. |
| **Phone** | Any smartphone | Modern iPhone or Android | For notifications, volunteer coordination on the go. |
| **Email** | Any | Google Workspace for Nonprofits (free) or Microsoft 365 Nonprofit | |

**Cost to client:** $0 + monthly subscription
**Best for:** Small churches (under 200 members), small nonprofits (1-3 staff) with existing devices

### Tier 2: ADC Starter Kit

| Item | Spec | Approx. Cost | Notes |
|------|------|-------------|-------|
| Laptop or Chromebook | 8GB RAM, SSD | $300-500 | For office admin |
| Tablet (lobby/entrance) | iPad or Android on stand | $400-600 | Self-check-in, visitor registration, event sign-up |
| Label printer (optional) | Brother QL-820NWB | $100-150 | Name tags for visitors, volunteer badges |
| UPS | 600VA | $60-80 | |
| **Total** | | **$860-1,330** | |

### Tier 3: ADC Media Kit

| Item | Spec | Approx. Cost | Notes |
|------|------|-------------|-------|
| Starter kit | | $860-1,330 | Everything above |
| Webcam + mic | Logitech Brio + Blue Yeti | $250-350 | For livestreaming services, virtual events |
| Display (lobby) | 43-55" TV on wall mount | $300-500 | Announcements, event calendar, welcome screen |
| **Total** | | **$1,410-2,180** | |

### Tier 4: NVIDIA DGX Spark

| Item | Spec | Cost |
|------|------|------|
| **NVIDIA DGX Spark** | GB10 Grace Blackwell, 128GB, 1 PFLOPS FP4, 4TB encrypted NVMe | **$4,699** |
| Media kit | | $1,410-2,180 |
| **Total** | | **~$6,110-6,880** |

**When to recommend:**
- Large church (1,000+ members) with extensive data privacy needs (counseling records, sensitive pastoral notes)
- Non-profit handling protected health information (shelters, counseling centers)
- Private school managing student records (FERPA compliance)
- Organization wanting local AI for sermon transcription, meeting summarization, or content generation

---

## The Install — Step by Step

### Step 1: Arrive + Understand the Organization (15 minutes)

1. **Timing:** Weekday, during office hours. NOT Sunday morning. NOT during services or events.
2. Walk the space:
   - Office setup? (Dedicated admin, shared space, pastor's office)
   - Lobby or welcome area? (Check-in, visitor registration)
   - Event spaces? (Fellowship hall, classrooms, gym)
   - How many staff? How many are volunteer vs. paid?
3. Ask:
   - *"What's your biggest admin time sink?"* (Usually: communications, volunteer coordination, or donation tracking)
   - *"How do people find out about events?"* (Bulletin, email, social media, word of mouth)
   - *"How do you track donations?"* (Spreadsheet, QuickBooks, church management software, envelopes in a drawer)
   - *"Do you apply for grants?"* How many per year? What's your success rate?
   - *"How many volunteers do you coordinate regularly?"*

### Step 2: Create Workspace (10 minutes)

1. `setup.adc3k.com` → New Client Workspace
2. Type: Church / Non-Profit / Private School
3. Membership size (this sets the tier)
4. Number of staff (paid + regular volunteers)
5. Primary management software (Planning Center, Breeze, Bloomerang, none)

### Step 3: Member / Contact Database (15 minutes)

1. Click **"Members"**
2. Import existing contacts:

   **From Planning Center:**
   - Connect via API → sync members, groups, teams, attendance
   - Map fields: name, email, phone, address, groups, tags

   **From Breeze:**
   - Connect via API → sync people, tags, giving
   - Map fields accordingly

   **From spreadsheet (common):**
   - Upload CSV with name, email, phone, address
   - AI deduplicates and formats

   **From nothing:**
   - Start fresh — members will be added as they check in or register

3. **Segmentation groups** — set up based on the org:

   **Church example:**
   | Group | Who |
   |-------|-----|
   | All Members | Everyone |
   | First-Time Visitors | Checked in once |
   | Youth (13-18) | Teens |
   | Young Adults (18-30) | College + young professionals |
   | Small Groups | By group name |
   | Volunteers | By team (greeting, worship, kids, setup) |
   | Deacons / Elders | Leadership |

   **Non-profit example:**
   | Group | Who |
   |-------|-----|
   | Donors | Anyone who's given |
   | Major Donors ($1,000+) | High-touch list |
   | Volunteers | Active volunteers |
   | Board Members | Governance |
   | Clients / Beneficiaries | People served |
   | Newsletter Subscribers | General interest |

### Step 4: Donation Tracking + Tax Receipts (15 minutes)

1. Click **"Giving"**
2. Connect donation sources:
   - Online giving platform (Tithe.ly, Pushpay, Subsplash, PayPal, Stripe)
   - Planning Center Giving or Breeze Giving
   - QuickBooks (for financial reconciliation)
3. Configure auto-receipts:
   - Immediate: *"Thank you, [name]! Your gift of $[amount] to [org] has been received. [Date] | [Transaction ID]"*
   - Year-end statement (auto-generated in January): *"Your total giving to [org] in [year] was $[total]. This letter serves as your tax receipt. [EIN number]"*
4. Giving categories:
   - General fund / tithes
   - Building fund
   - Missions
   - Youth programs
   - Specific campaigns (*"Roof Repair Fund"*)
5. **Giving trends dashboard:**
   - Monthly giving total vs. previous year
   - Donor retention rate
   - Average gift amount
   - New donors this month
   - Lapsed donors (gave last year, not this year) — flag for outreach

### Step 5: Volunteer Scheduling (10 minutes)

1. Click **"Volunteers"**
2. Set up volunteer teams:

   **Church example:**
   - Greeting / Welcome team
   - Worship team
   - Children's ministry
   - Youth leaders
   - Setup / teardown crew
   - Sound / AV tech
   - Parking lot

   **Non-profit example:**
   - Event volunteers
   - Food drive team
   - Office help
   - Tutoring / mentoring
   - Board committees

3. Configure scheduling:
   - Recurring needs (every Sunday: 3 greeters, 2 kids' ministry, 1 AV tech)
   - Event-based needs (food drive: 10 volunteers on Saturday 8 AM - noon)
4. AI scheduling messages:
   - *"You're scheduled for greeting this Sunday at 9:15 AM. Can you make it? Reply YES or SWAP."*
   - If SWAP: AI finds a replacement from the team and confirms
   - If no reply by Thursday: AI follows up, then alerts the coordinator

### Step 6: Event Management (10 minutes)

1. Click **"Events"**
2. Set up event types:
   - Recurring (weekly service, monthly potluck, quarterly business meeting)
   - One-time (fundraiser gala, mission trip, VBS, conference)
   - Classes (new member class, Bible study, support group)
3. Registration flow:
   - Event page with details, date/time, location, capacity
   - Registration: *"Register for [event]: [link]"*
   - Confirmation: *"You're registered for [event] on [date]! Add to calendar: [link]"*
   - Reminder (24 hrs): *"[Event] is tomorrow at [time]. See you there!"*
   - Follow-up (1 day after): *"Thanks for coming to [event]! How was it? [feedback link]"*
4. **Childcare registration** (important for churches):
   - Parent registers kids for event childcare
   - Allergy/medical info on file
   - Check-in/check-out system with security codes

### Step 7: AI Phone + Messaging (10 minutes)

1. Greeting: *"Thanks for calling [org name]. I can help with service times, events, directions, or connect you with someone. How can I help?"*
2. Common questions:
   - *"What time is service?"* → reads from schedule
   - *"Where are you located?"* → address + directions
   - *"How do I volunteer?"* → registration link
   - *"I need help / I'm in crisis"* → IMMEDIATE escalation to pastor or director (never AI-handled)
   - *"How do I donate?"* → giving link
3. **Pastoral care routing:**
   - Hospital visit request → alert pastor
   - Prayer request → log and route to prayer team (with permission)
   - Counseling request → schedule with appropriate staff
   - **CRITICAL:** AI never gives spiritual advice, counseling, or crisis intervention. Always routes to a human.

### Step 8: Grant Writing Assistant (15 minutes)

This is the killer feature for non-profits. Grant applications are brutal — 20-40 hours each.

1. Click **"Grants"**
2. Build the organization profile:
   - Mission statement
   - History and timeline
   - Programs and services offered
   - Impact metrics (people served, outcomes, testimonials)
   - Financial data (annual budget, revenue sources, expenses by program)
   - Board of directors list
   - Staff bios
   - Past grants received
3. **Template library:**
   - AI stores common grant sections:
     - Organization description (250 words, 500 words, full page)
     - Need statement / problem description
     - Program description
     - Evaluation plan
     - Budget narrative
     - Sustainability plan
4. **Grant drafting workflow:**
   - Paste the grant RFP (Request for Proposal)
   - AI analyzes requirements, maps to template sections
   - AI generates first draft pulling from org profile + templates
   - Human reviews, edits, adds specifics
   - AI formats to funder requirements (word counts, sections, formatting)
5. **Grant tracking:**
   - Deadlines calendar
   - Submission status (researching, drafting, submitted, awarded, denied)
   - Follow-up reminders for reporting requirements
   - *"The [Foundation] report is due in 30 days. Last year's data: [link]"*

### Step 9: Communications + Newsletter (10 minutes)

1. Click **"Communications"**
2. Connect email platform:
   - Mailchimp (free for nonprofits up to 500 contacts)
   - Constant Contact
   - Or built-in email from Planning Center / Breeze
3. Set up recurring communications:
   - [x] **Weekly update** (Friday): upcoming events, volunteer needs, prayer requests
   - [x] **Monthly newsletter**: highlights, impact stories, giving update, upcoming events
   - [x] **New visitor follow-up** (Monday after first visit): *"Great to see you Sunday! Here's what's happening this week: [link]"*
   - [x] **Birthday message**: *"Happy birthday, [name]! Your [org] family is thinking of you today."*
   - [x] **Engagement check** (90 days no attendance): alert staff for personal outreach
   - [x] **Year-end giving appeal** (November): *"As 2026 comes to a close, your gift helps us [mission]. Give here: [link]"*
4. **Segmented messaging:** Youth events go to youth families. Senior lunch goes to seniors. Board meetings go to board. No more "this doesn't apply to me" emails.

---

## Training (15 minutes)

### Admin / Office Staff (10 minutes)
1. **Dashboard overview:** Members, giving, events, volunteers at a glance
2. **Communication tools:** How to send an email or text to a group
3. **Event creation:** How to set up an event with registration
4. **Giving reports:** How to pull donation reports, generate tax receipts
5. **Grant assistant:** How to start a new grant draft, edit AI output, submit

### Pastor / Executive Director (5 minutes)
1. **Engagement alerts:** Who's new, who's drifting, who needs a call
2. **Giving dashboard:** Overall health, trends, major donor activity
3. **Quick communications:** How to send a personal text or email from the app
4. **Grant pipeline:** What's in progress, what's due

**Key line:** *"This doesn't replace the personal touch — it makes sure nobody falls through the cracks. The AI handles the admin so you can focus on the people."*

---

## Before You Leave — Final Checklist

- [ ] Member database imported and groups set up
- [ ] Donation tracking connected to giving platform (test with a $1 donation, verify receipt)
- [ ] AI phone live and answering (call it, ask for service times, ask about volunteering)
- [ ] Volunteer scheduling set up for at least one recurring need
- [ ] One event created with registration link (test it)
- [ ] Grant writing assistant loaded with org profile and at least one template
- [ ] Communications connected (send a test email to admin)
- [ ] Engagement tracking active (verify attendance logging)
- [ ] Check-in tablet set up in lobby (if applicable)
- [ ] Admin and pastor/director both have dashboard access on phone
- [ ] Quick Start card at front desk
- [ ] Service agreement signed

---

## After You Leave

### Day 2 — Text
*"Hey [name] — how's it going? Did you get a chance to try the volunteer scheduling for this week's needs? Any questions about the dashboard?"*

### Day 7 — Call
- How many calls has the AI handled? Any wrong answers? (Check common: service times, location, events)
- Did they send a communication to any group? How did it go?
- Any donation tracking issues? (Receipts sending? Amounts matching?)
- Review the grant assistant if they have an upcoming application
- Adjust: AI phone answers, group segmentation, communication templates

### Day 30 — Metrics Review
Pull these numbers and share with the client:
- AI calls handled (and what was asked)
- Volunteer fill rate (% of needed spots filled without manual calls)
- Donation acknowledgment speed (should be instant now)
- Communication open rates (emails, texts)
- Events registered vs. attended
- Grant applications in progress (hours saved estimate)
- New visitors logged and followed up
- Admin hours saved per week (estimate based on tasks automated)

---

## Troubleshooting

| Problem | What to Do |
|---------|------------|
| "Our older members don't use email or text" | Set up a phone tree option. AI can make outbound calls with announcements. Also: print a bulletin with a QR code to the event page — some will adopt it. |
| "Donations aren't matching our bank deposits" | Check the integration sync. Most issues are timing — online gifts process in 2-3 business days. Make sure they're not comparing today's donations to today's deposits. |
| "The grant writer output doesn't sound like us" | Feed it more source material. Past newsletters, annual reports, the pastor's/director's actual words. The more voice samples, the better the output matches their tone. |
| "Volunteers aren't responding to scheduling texts" | Check the timing. Sending Wednesday for Sunday is too late. Send the previous Sunday or Monday. If they still don't respond, the coordinator needs to call — some people just don't text. |
| "We're worried about data privacy for counseling notes" | Counseling notes should NOT go in the system. The AI handles scheduling the session, not documenting it. Pastoral/counseling notes stay in a separate, restricted system or paper files. |
| "The check-in tablet isn't working" | Check WiFi at the lobby location. Thick walls = weak signal. A WiFi extender near the entrance usually fixes it. Also check that the tablet isn't in sleep mode. |

---

## What You Should NOT Do

1. **Don't give spiritual, pastoral, or theological advice.** You're an installer, not a counselor.
2. **Don't access individual giving records.** Set up the system; the admin enters the data. Donor information is extremely sensitive.
3. **Don't promise grant success.** "This tool helps you write stronger applications faster" is fine. "You'll win the grant" is not.
4. **Don't photograph members, especially children.** Child safety policies are serious.
5. **Don't share one organization's data or templates with another.** Even if they're similar orgs.
6. **Don't set up AI to give counseling or crisis advice.** Always route to a human. No exceptions.

---

## Glossary

| Word | What It Means |
|------|---------------|
| **Tithe** | A traditional 10% gift of income to the church. Not all members tithe. Don't use this word with non-church clients. |
| **EIN** | Employer Identification Number. The org's tax ID. Required on donation receipts for tax deductibility. Every 501(c)(3) has one. |
| **501(c)(3)** | IRS designation for tax-exempt charitable organizations. Donations to these are tax-deductible. Most churches, nonprofits, and private schools have this status. |
| **RFP** | Request for Proposal. A funder's document describing what they want to fund, requirements, and application instructions. This is what the grant assistant helps respond to. |
| **Pledge** | A commitment to give a specific amount over time. *"I pledge $1,200 this year"* = $100/month. Track pledges separately from actual giving. |
| **Planning Center** | Church management software — people, giving, services, check-in, groups. Very common in mid-to-large churches. API available. |
| **Breeze** | Simpler church management software. Common in smaller churches. API available. |
| **FERPA** | Family Educational Rights and Privacy Act. If the org is a school, student records are protected. The AI system doesn't store grades or disciplinary records — just contact info and event registration. |
| **Restricted funds** | Donations given for a specific purpose (*"for the building fund"*). Legally must be used for that purpose. The system tracks these separately. |
| **In-kind donation** | Non-cash gifts — food, clothing, services, equipment. Track these separately from monetary donations for reporting and tax purposes. |
