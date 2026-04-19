# ADC AI Install Playbook — Government / Municipal Office

## Who This Is For
You're an ADC installer. This covers city halls, parish/county offices, permitting departments, public works, code enforcement, parks and recreation, public libraries, and municipal utilities. If they serve citizens and run on tax dollars, this playbook applies.

---

## What You're Installing
An AI system that handles citizen inquiries, streamlines permits, and cuts paperwork. When you're done, the office will be able to:

- **AI citizen service line** — answers routine inquiries 24/7. *"When is my water bill due?" "How do I get a building permit?" "What day is trash pickup on my street?"* — handled instantly. No hold times, no voicemail.
- **Permit processing** — citizens submit permit applications online. AI validates completeness, routes to the right department, tracks status, sends updates. *"Your building permit application has been received. Estimated review time: 5-7 business days. Track status: [link]"*
- **Public records search** — AI-powered search across meeting minutes, ordinances, resolutions, and public documents. *"Show me the zoning ordinance for Section 14"* — found in seconds, not hours.
- **Meeting minutes transcription** — record council meetings, AI transcribes and generates searchable, indexed minutes. No more 3-day turnaround from the clerk's office.
- **Code enforcement tracking** — complaints logged, assigned, tracked, and resolved. *"Overgrown lot at 123 Main St"* → logged → assigned to inspector → inspected → notice issued → compliance verified → closed.
- **311-style request intake** — potholes, streetlight outages, water main breaks, animal control. Citizens report by phone, text, or web. AI routes to the right department, tracks resolution, updates the citizen.
- **Automated notifications** — boil advisories, road closures, meeting reminders, tax due dates. Segmented by ward, district, or zip code.

**What it replaces:** The citizen on hold for 25 minutes to ask when their water bill is due. The permit application that sits in someone's inbox for 2 weeks because it went to the wrong person. The code enforcement complaint nobody followed up on. The council meeting minutes that take a week to produce. The 311 call that gets lost between departments.

---

## Client Minimum Requirements

### Tier 1: Cloud-Only

| Requirement | Minimum | Recommended | Why |
|-------------|---------|-------------|-----|
| **Internet** | 50 Mbps | 100+ Mbps | Multiple staff, public portal, document management. |
| **Existing software** | None required | If they use CivicPlus, Tyler Technologies, Accela, or Granicus — we integrate | |
| **Computers** | Existing office PCs | Windows 10+ or Mac, 8GB+ RAM | Each department needs access. |
| **Phone system** | Existing PBX or VoIP | VoIP (RingCentral, 8x8, or similar) | For AI phone routing. |
| **Website** | Any municipal website | CivicPlus or WordPress | For citizen portal embedding. |

**Cost to client:** $0 + monthly subscription
**Best for:** Small municipalities (under 10,000 pop.) with existing IT infrastructure

### Tier 2: ADC Starter Kit

| Item | Spec | Approx. Cost | Notes |
|------|------|-------------|-------|
| Public kiosk | Ruggedized touchscreen (15-22") | $1,200-2,000 | Lobby self-service — permits, payments, records |
| Webcam + mic | Conference room quality | $200-350 | Council meeting recording |
| Document scanner | Duplex ADF scanner | $300-500 | Digitizing paper records |
| UPS (per critical workstation) | 1000VA | $100-150 each | Government can't go down |
| **Total** | | **$1,800-3,000** | |

### Tier 3: ADC Municipal Kit

| Item | Spec | Approx. Cost | Notes |
|------|------|-------------|-------|
| Starter kit | | $1,800-3,000 | Everything above |
| Council chamber recording system | PTZ camera + ceiling mics + mixer | $2,000-4,000 | Professional meeting recording for transcription |
| Lobby display | 55" digital signage | $400-600 | Announcements, wait times, department status |
| Tablets for field staff | Rugged tablets (Samsung Active, Panasonic) | $500-800 each | Code enforcement, inspections, field reports |
| **Total** | | **$4,700-8,400** | |

### Tier 4: NVIDIA DGX Spark

| Item | Spec | Cost |
|------|------|------|
| **NVIDIA DGX Spark** | GB10 Grace Blackwell, 128GB, 1 PFLOPS FP4, 4TB encrypted NVMe | **$4,699** |
| Municipal kit | | $4,700-8,400 |
| **Total** | | **~$9,400-13,100** |

**When to recommend:**
- Municipality handling sensitive citizen data that must stay on-premise (CJIS compliance for law enforcement integration)
- Large city (50,000+ pop.) with high document volume needing local AI search
- Municipality wanting AI-powered video analysis of council meetings (speaker identification, topic indexing)
- Parish/county seat managing records for the entire jurisdiction

---

## The Install — Step by Step

### Step 1: Arrive + Understand the Operation (15 minutes)

1. **Timing:** Weekday during office hours. Schedule through the City Manager, Parish Administrator, or IT Director. Expect a procurement process — this may take weeks before you're even on-site.
2. Walk the office:
   - Front counter / lobby setup? (How do citizens interact today?)
   - How many departments? (Utilities, permits, code enforcement, parks, public works, clerk)
   - IT setup? (Dedicated IT staff, or does someone wear multiple hats?)
   - Council chamber? (Recording equipment, seating, public comment setup)
3. Ask:
   - *"What's your highest-volume citizen inquiry?"* (Usually: utility billing or permits)
   - *"How are complaints/requests tracked today?"* (Spreadsheet, sticky notes, email, 311 system)
   - *"How long does a typical permit take from application to approval?"*
   - *"Who transcribes council meeting minutes? How long does it take?"*
   - *"Do you have a public records request process? How many per month?"*

### Step 2: Create Workspace (10 minutes)

1. `setup.adc3k.com` → New Client Workspace
2. Type: Government / Municipal
3. Population served
4. Number of departments
5. Existing management software (Tyler, CivicPlus, Accela, none)

**IMPORTANT:** Government installs may require a formal procurement process, IT security review, and/or council approval BEFORE you begin. The workspace creation and demo may be part of the sales process, not the install itself. Adapt accordingly.

### Step 3: Citizen Service AI (20 minutes)

This is the killer feature. Build the knowledge base from the most common citizen questions.

1. Click **"Citizen Services"**
2. Build FAQ by department:

   **Utility Billing:**
   | Question | Answer Source |
   |----------|---------------|
   | When is my bill due? | Billing cycle schedule |
   | How do I pay? | Payment options (online, in-person, mail, auto-pay) |
   | How do I start/stop service? | Application process + timeline |
   | Why is my bill so high? | → Escalate to billing staff with account lookup |
   | I have a leak — who do I call? | Emergency number + after-hours process |

   **Permits / Planning:**
   | Question | Answer Source |
   |----------|---------------|
   | How do I get a building permit? | Application checklist + submission link |
   | What's my property zoned? | GIS lookup or zoning map link |
   | Do I need a permit for a fence/shed/deck? | Permit requirement matrix |
   | What's the status of my permit? | → Lookup by permit number or address |

   **General:**
   | Question | Answer Source |
   |----------|---------------|
   | What are your office hours? | Schedule by department |
   | Where do I pay a traffic ticket? | Court clerk info |
   | When is the next council meeting? | Meeting calendar |
   | How do I get a copy of [document]? | Public records request process |

3. Configure AI phone:
   - Greeting: *"Thank you for calling the [City/Parish] of [Name]. I can help with utility billing, permits, public records, or connect you with a department. How can I help?"*
   - Routing: if AI can't answer → transfer to correct department (not general voicemail)
   - After hours: *"Our offices are closed. I can still help with [list of AI-capable tasks]. For emergencies, call [emergency number]."*

4. **Web portal chatbot:**
   - Embed on municipal website
   - Same knowledge base as phone
   - Add: document links, form downloads, payment portal links

### Step 4: Permit Processing (20 minutes)

1. Click **"Permits"**
2. Set up permit types:

   | Permit Type | Required Documents | Review Dept. | Typical Timeline |
   |-------------|-------------------|--------------|-----------------|
   | Building (residential) | Application, plans, survey, contractor license | Building Dept | 5-10 business days |
   | Building (commercial) | Application, engineered plans, fire review | Building + Fire | 10-20 business days |
   | Electrical | Application, contractor license | Building Dept | 3-5 business days |
   | Plumbing | Application, contractor license | Building Dept | 3-5 business days |
   | Sign permit | Application, design specs, location | Planning | 5-10 business days |
   | Occupancy permit | Inspection request | Building Dept | Scheduled inspection |

3. Application workflow:
   - Citizen submits online (or staff enters from paper at the counter)
   - AI validates: all required documents attached? All fields complete?
   - Incomplete → auto-response: *"Your application is missing [list]. Please upload and resubmit: [link]"*
   - Complete → route to reviewer → set review deadline → notify citizen of receipt
4. Status tracking:
   - Submitted → Under Review → Approved / Revisions Required / Denied
   - At each stage: auto-notify applicant
   - *"Your building permit for [address] has been approved. Permit #[number]. Pick up at [location] or download: [link]"*
5. **Inspection scheduling:**
   - Applicant requests inspection online
   - AI checks inspector availability, schedules, confirms
   - *"Your inspection is scheduled for [date] between 8 AM - 12 PM. Inspector: [name]. Please ensure access to [areas]."*

### Step 5: Code Enforcement Tracking (15 minutes)

1. Click **"Code Enforcement"**
2. Set up violation categories:
   - Property maintenance (overgrown lots, junk vehicles, exterior disrepair)
   - Zoning violations (home business, unpermitted structures)
   - Nuisance (noise, odor, abandoned property)
   - Sign violations
   - Building without permit
3. Complaint workflow:
   - Citizen reports (phone, web, text, walk-in) → AI creates case with address, description, photos
   - Auto-assign to inspector by zone/district
   - Inspector inspects → documents with photos → issues notice or clears
   - Notice issued → compliance deadline set → auto-follow-up at deadline
   - Non-compliance → escalation (second notice, citation, lien)
4. **Citizen updates:**
   - *"Your complaint about [address] has been received. Case #[number]. An inspector will visit within [X] business days."*
   - *"Case #[number] update: notice of violation issued to property owner. Compliance deadline: [date]."*
   - *"Case #[number] resolved: property is now in compliance."*
5. **Field tablets:** Inspectors photograph violations, update case status, and issue notices from the field. No more going back to the office to type up reports.

### Step 6: Meeting Minutes + Transcription (15 minutes)

1. Click **"Meetings"**
2. Connect recording source:
   - Council chamber audio/video system
   - Zoom/Teams recording (if hybrid meetings)
   - USB audio recorder (minimum viable)
3. Transcription workflow:
   - Record meeting → upload recording (or auto-upload from Zoom/Teams)
   - AI transcribes within 1 hour
   - AI generates: searchable transcript, summary, action items, roll call votes
   - Clerk reviews and approves
   - Published to municipal website
4. **Meeting types:**
   - City/Parish Council meetings
   - Planning and Zoning Commission
   - Board of Adjustments
   - Committee meetings
   - Special sessions
5. **Search:** Citizens can search across all meeting minutes. *"Show me every time the council discussed the water treatment plant"* — AI finds every mention across years of transcripts.

### Step 7: Public Records + Document Search (10 minutes)

1. Click **"Records"**
2. Document categories:
   - Ordinances and resolutions
   - Meeting minutes (auto-populated from Step 6)
   - Budget documents
   - Contracts and agreements
   - Public notices
   - GIS/property data
3. **Public records request workflow:**
   - Citizen submits request (online form, email, walk-in)
   - AI categorizes, checks if document is already public (instant response)
   - If not available: routes to records custodian, sets response deadline (per state public records law — Louisiana = 3 business days)
   - Tracks all requests for compliance reporting

### Step 8: 311-Style Service Requests (10 minutes)

1. Click **"Service Requests"**
2. Request categories:

   | Category | Routes To | SLA |
   |----------|-----------|-----|
   | Pothole | Public Works | 5 business days |
   | Streetlight out | Public Works / Utility | 3 business days |
   | Water main break | Utility (EMERGENCY) | Immediate dispatch |
   | Sewer backup | Utility (EMERGENCY) | Immediate dispatch |
   | Fallen tree | Public Works | 2 business days |
   | Animal control | Animal Control | 1 business day |
   | Illegal dumping | Code Enforcement | 3 business days |
   | Road debris | Public Works | 1 business day |

3. Citizen submits by phone, text, web, or in-person
4. AI logs: location (address or GPS), description, photo (if available), contact info
5. Auto-route to department → assign to crew/individual → track to resolution
6. Citizen updates: *"Your pothole report at [location] has been received. Work order #[number]. Estimated repair: [date]."*

### Step 9: Notification System (10 minutes)

1. Click **"Notifications"**
2. Set up alert types:
   - [x] **Emergency alerts:** Boil advisories, severe weather, road closures, evacuations
   - [x] **Utility notices:** Planned outages, rate changes, billing due dates
   - [x] **Meeting reminders:** *"City Council meets tomorrow at 6 PM. Agenda: [link]. Public comment period available."*
   - [x] **Tax reminders:** Property tax due dates, payment options
   - [x] **Event announcements:** Community events, public hearings, workshops
3. **Segmentation:**
   - By ward/district (council meeting reminders go to that ward's residents)
   - By service area (water boil advisory goes only to affected zone)
   - By opt-in topic (events, meetings, emergencies)
4. **Channels:** Text, email, phone (automated voice), app push notification, social media auto-post

---

## Training (20 minutes)

### Front Counter Staff (10 minutes)
1. **Citizen lookup:** How to search for a citizen's account, permit, or case
2. **Walk-in intake:** How to enter a service request, permit application, or complaint for a citizen at the counter
3. **Dashboard:** How to see open cases, pending permits, today's appointments
4. **Escalation:** How to transfer a call from the AI to their extension

### Department Heads (5 minutes)
1. **Queue management:** How to see and assign work in their department
2. **Reports:** How to pull monthly stats (permits issued, cases closed, response times)
3. **SLA monitoring:** How to see which items are approaching or past deadline

### City Manager / Administrator (5 minutes)
1. **Executive dashboard:** All departments at a glance — open items, response times, citizen satisfaction
2. **Notification system:** How to trigger emergency alerts
3. **Meeting minutes:** How to review and approve transcriptions before publishing

**Key line:** *"Citizens expect Amazon-speed service from government now. This system doesn't replace your staff — it gives them superpowers. Instant answers for routine questions, automatic routing for everything else, and a dashboard so nothing falls through the cracks."*

---

## Before You Leave — Final Checklist

- [ ] AI citizen service line live and answering (call it, ask 10 common questions, verify correct answers)
- [ ] Chatbot embedded on municipal website and tested
- [ ] Permit application portal live with at least 3 permit types configured
- [ ] Code enforcement complaint intake working (submit a test complaint, verify routing)
- [ ] Service request system (311) active with department routing
- [ ] Meeting recording + transcription tested (record a 5-minute test, verify transcript quality)
- [ ] Notification system configured and tested (send a test alert to admin)
- [ ] Public records search indexed with existing documents
- [ ] Public kiosk set up in lobby (if applicable)
- [ ] Each department head has dashboard access
- [ ] City Manager has executive dashboard on phone
- [ ] Field tablets configured for inspectors (if applicable)
- [ ] IT staff briefed on system architecture and support contacts
- [ ] Service agreement signed (may require council approval)

---

## After You Leave

### Day 2 — Text (to IT contact and City Manager)
*"System is live. How are the first calls going? Check the dashboard for today's citizen inquiry stats. Let me know if any AI answers need adjusting."*

### Day 7 — Call
- How many citizen calls has the AI handled? What percentage resolved without transfer?
- Any permit applications submitted through the new portal?
- Any code enforcement cases logged?
- Review AI phone transcripts — are answers accurate for local policies?
- Adjust: FAQ entries, department routing, SLA timelines

### Day 30 — Metrics Review
Pull these numbers for the City Manager:
- Citizen calls handled by AI vs. transferred to staff (target: 60%+ AI-resolved)
- Average hold time / wait time (should be near zero for AI-handled calls)
- Permit processing time (application to decision — should be trending faster)
- Code enforcement cases: opened vs. closed, average resolution time
- Service requests: opened vs. closed, SLA compliance rate
- Meeting minutes turnaround time (should be same-day now vs. days/weeks before)
- Public records request response time
- Citizen satisfaction (if survey enabled)

---

## Troubleshooting

| Problem | What to Do |
|---------|------------|
| "The AI is giving outdated info" | Government info changes with every ordinance and policy update. Set a quarterly review schedule to update the knowledge base. Assign one person as the AI content owner. |
| "Citizens don't trust the AI" | Normal for government. Add a prominent "Press 0 to speak to a person" option. Over time, as the AI resolves issues correctly, adoption increases. Don't force it. |
| "Permits are still slow" | The AI handles intake and routing, not decision-making. If the bottleneck is the reviewer, that's a staffing/process issue. The system shows where delays happen — use the data to justify resources. |
| "Council members don't want meetings recorded" | Public meetings are public record (Louisiana Open Meetings Law). Recording is legal and standard. If they object, this is a policy discussion, not a technology issue. Refer to the City Attorney. |
| "Code enforcement officers resist the tablets" | Start with voluntary adoption. The officers who use it close cases faster and have better documentation. The others will follow or get left behind. Don't mandate — demonstrate value. |
| "IT is worried about security" | The system uses encrypted APIs, no citizen PII is stored in plain text, and access is role-based. Provide the security documentation and offer a call with our security team. Government IT will want to vet this — that's normal and correct. |

---

## What You Should NOT Do

1. **Don't access citizen financial accounts.** Utility billing data, tax records, court records — hands off. Set up the system; staff enters the data.
2. **Don't make policy decisions.** If you're asked "should this permit be approved?" — that's not your call. The system routes and tracks. Humans decide.
3. **Don't set up the system without IT involvement.** Government IT must be in the loop from day one. Security, network access, and data governance are their responsibility.
4. **Don't promise specific cost savings to elected officials.** "Most municipalities reduce phone hold times by 70%" is fine. "This will save you $200K" is not.
5. **Don't bypass procurement.** If they need a PO, RFQ, or council vote — wait for it. Don't start work on a handshake.
6. **Don't store law enforcement data.** If they mention police records, warrants, or CJIS data — stop. That requires a separate, CJIS-compliant system. Not this install.

---

## Glossary

| Word | What It Means |
|------|---------------|
| **311** | A non-emergency citizen service line (like 911 but for potholes and streetlights). Many cities use it. Ours replicates the function without needing a dedicated call center. |
| **SLA** | Service Level Agreement. The promised response time. "Potholes repaired within 5 business days" is an SLA. The system tracks compliance. |
| **Ordinance** | A law passed by the city/parish council. Has the force of law within the municipality. Different from a resolution (which is a statement of intent, not law). |
| **PBX** | Private Branch Exchange. The phone system that routes calls within the building. VoIP (internet-based) is easier to integrate than legacy PBX. |
| **GIS** | Geographic Information System. Maps with data layers — zoning, parcels, utilities, flood zones. The AI can reference GIS data for address-based questions. |
| **CJIS** | Criminal Justice Information Services. FBI security standard for law enforcement data. If they mention police data, this is a hard stop — different system, different compliance level. |
| **Open Meetings Law** | Louisiana law requiring government meetings to be open to the public with proper notice. Recording and transcribing supports compliance. |
| **Public Records Request** | A citizen's legal right to access government documents. Louisiana Public Records Act (R.S. 44:1) requires response within 3 business days. The system tracks these for compliance. |
| **RFQ / RFP** | Request for Quote / Request for Proposal. Formal procurement documents. Governments often require these for purchases over a threshold ($5K-$25K varies by municipality). |
| **Procurement** | The formal process governments use to buy things. May require quotes, bids, council approval, or all three. Be patient — this is the law, not red tape. |
