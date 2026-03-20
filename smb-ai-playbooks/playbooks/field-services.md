# ADC AI Install Playbook — Field Services (Plumber, Electrician, HVAC, Contractor)

## Who This Is For
You're an ADC installer. You don't need to be a computer person. This guide is written so that someone with a high school education and no tech background can follow it step by step. If you can follow a recipe, you can do this job.

This playbook covers **field service businesses** — plumbers, electricians, HVAC techs, general contractors, pest control, roofing, anyone who:
- Sends crews out to job sites
- Works with multiple vendors/suppliers
- Gives quotes and invoices in the field
- Has an office person answering phones and scheduling

---

## What You're Installing
You're setting up an AI system that runs the business side so the owner can focus on the work. When you're done, they'll be able to:

- **Answer every call** — AI answers the phone when the office is busy or closed, books the appointment, sends confirmation
- **Dispatch crews** — see all jobs on a map, assign the closest available tech, send them the job details on their phone
- **Quote on the spot** — tech takes photos at the job site, AI generates a quote with parts pricing from their vendors
- **Track parts + vendors** — know what's in the truck, what to order, who has the best price
- **Invoice + get paid** — send the invoice before the tech leaves the driveway, customer pays on their phone
- **Follow up automatically** — "How was your service?" text goes out the next day, review request goes out after 7 days

**What it replaces:** The owner's wife answering the phone between loads of laundry. The whiteboard on the wall with the schedule. The stack of invoices on the dashboard. The "I'll send you a quote" that never gets sent.

---

## Client Minimum Requirements — What They Need Before You Show Up

Field service is different from an office job. You've got the dispatch desk AND guys in trucks. Both sides need to work. Check these requirements BEFORE you schedule the install.

### Tier 1: Cloud-Only (Use What They Have)
Everything runs on ADC's servers. Client just needs internet and phones.

**Office / Dispatch:**

| Requirement | Minimum | Recommended | Why |
|-------------|---------|-------------|-----|
| **Internet** | 25 Mbps down / 10 Mbps up | 100 Mbps down / 25 Mbps up | Dispatch board, AI phone, quotes, and invoices all go through the internet. More trucks = more bandwidth. |
| **Computer** | Any computer made after 2018, 8GB RAM | 16GB RAM, SSD | Dispatch board runs in a browser but it's heavier than a simple website — map, live locations, multiple jobs. |
| **Browser** | Chrome or Edge (updated) | Chrome | NOT Internet Explorer. NOT Safari. Chrome works best with the dispatch map. |
| **Monitor** | 20"+ | 27"+ or dual monitors | Dispatch board has a lot going on — map + job list + crew status. A tiny screen makes it frustrating. Dual monitors are ideal: one for dispatch, one for everything else. |
| **Phone (office)** | Existing landline or cell | VoIP or cell with good signal | For AI receptionist integration. If they have a landline, we forward to the AI number. |

**Field / Trucks:**

| Requirement | Minimum | Recommended | Why |
|-------------|---------|-------------|-----|
| **Phone** | iPhone 12+ or Android 10+ | Any phone from the last 3 years with good battery | Runs the field app — job notifications, quoting, invoicing, GPS. Older phones drain battery fast with GPS on. |
| **Phone plan** | Unlimited data OR 5GB+/mo per tech | Unlimited data | The app uses ~500MB-1GB/month with photos and GPS. If a tech hits their data cap, the app stops working. |
| **Phone mount** | Suction cup or vent mount | RAM Mount or ProClip | Techs need hands-free navigation to job sites. Don't let them hold the phone while driving. $15-30 each. |
| **Phone charger** | Car charger cable | Fast charger (USB-C, 20W+) | GPS + app running all day kills the battery. They NEED a charger in the truck. $10-15 each. |

**Cost to client:** $0-100 in accessories (phone mounts, chargers) + monthly subscription
**Best for:** Small operations (1-3 techs) with decent phones and internet already

### Tier 2: ADC Starter Kit (We Sell/Provide the Hardware)
For the office that's running on a 10-year-old Dell and the techs have cracked-screen phones.

**Office Kit:**

| Item | Spec | Approx. Cost | Notes |
|------|------|-------------|-------|
| Mini PC | Intel i5 or AMD Ryzen 5, 16GB RAM, 512GB SSD | $400-600 | Runs the dispatch browser smoothly. Mounts behind the monitor. |
| Monitor | 27" 1080p | $200-250 | Big enough for the dispatch map. |
| Second monitor (optional) | 24" 1080p | $150-200 | One for dispatch, one for invoices/email. Game-changer for the office person. |
| Keyboard + Mouse | Wireless set | $30-50 | |
| UPS (battery backup) | 600VA | $60-80 | Keeps dispatch running during power flickers. |
| **Office kit total** | | **$840-1,180** | |

**Field Kit (per truck):**

| Item | Spec | Approx. Cost | Notes |
|------|------|-------------|-------|
| Phone mount | RAM Mount X-Grip | $30 | Bulletproof. Works in any truck. |
| Car charger | Anker 30W USB-C | $15 | Fast charges while navigating. |
| Rugged phone case | OtterBox or equivalent | $40-60 | These guys drop phones. A lot. |
| **Per truck total** | | **$85-105** | |

**Total for a 3-truck operation:** ~$1,100-1,500 (office kit + 3 truck kits)
**Best for:** Operations with outdated equipment, owner who wants a clean dedicated setup

### Tier 3: NVIDIA DGX Spark (Local AI — The Premium Play)
For the larger contractor who wants everything running on-site. AI lives in the office, not in the cloud.

| Item | Spec | Cost |
|------|------|------|
| **NVIDIA DGX Spark** | GB10 Grace Blackwell superchip, 128GB unified memory, 1 PFLOPS FP4, 4TB NVMe SSD with self-encryption, ConnectX-7 SmartNIC | **$4,699** |
| **DGX Spark Bundle** (optional) | Two DGX Spark units + connecting cable (for 10+ tech operations with heavy dispatch) | **~$9,400** |
| Monitor | 27" 1080p | $200-250 |
| UPS (battery backup) | 1500VA | $150-200 |
| Truck kits (per truck) | Mount + charger + case | $85-105 each |
| **Total (single Spark, 5 trucks)** | | **~$5,875-6,225** |

**What makes DGX Spark different:**
- **Size:** About the size of a Mac Mini (6" x 6" x 2"). Sits on a shelf in the office. No server room needed.
- **Speed:** 1 PFLOPS of AI compute. In plain English: the AI phone answering, dispatch routing, quote generation, and invoice processing all run at the same time without slowing down.
- **Storage:** 4TB of encrypted SSD. All customer records, job history, vendor pricing — stored locally and encrypted. If someone breaks in and steals the box, the data is useless without the key.
- **Offline capability:** If the internet goes down, the office-side AI keeps working — dispatch board, quoting from cached parts lists, invoice generation. Field app still needs cell data, but the brain doesn't go down with the WiFi.
- **No per-use AI fees:** After the hardware purchase, the AI models run locally for free. No token costs. For a busy operation running 50+ jobs/week, this pays for itself in 6-12 months vs. cloud AI fees.
- **Runs NVIDIA Nemotron + NemoClaw** — the personal AI operating system. Handles the phone answering, document processing, and quote generation all on one box.

**The pitch to the owner:**
> *"This is a personal AI computer the size of a paperback book. Your customer data stays in your office — not on somebody else's server. The AI phone, dispatch, quoting — all of it runs off this box. And after you buy it, there's no monthly AI fee. The computer does the work."*

**When to recommend DGX Spark:**
- Owner has 5+ techs and runs 30+ jobs/week (high volume = cloud AI fees add up)
- Owner handles government or commercial contracts with data requirements
- Owner is in a rural area with unreliable internet (Spark keeps the office running offline)
- Owner is privacy-conscious or has been burned by a cloud service going down

**When NOT to recommend DGX Spark:**
- Solo operator running 5-10 jobs/week — overkill, Tier 1 cloud is fine
- Owner can barely use a smartphone — keep it simple with cloud
- Budget under $5K for everything — start Tier 1, upgrade later

### Pre-Install Checks (Non-Negotiable)

**Internet speed test:**
1. Tell the owner: *"Before I come out, go to speedtest.net on the office computer and text me a screenshot."*
2. Below 25 Mbps down: they need to upgrade internet first. Don't install on slow internet.
3. If they're in a rural area with no good internet options: this is a DGX Spark candidate (runs locally).

**Tech phone check:**
1. Ask the owner: *"What phones do your guys have?"*
2. If any tech has a phone older than 4 years or a cracked screen they can barely read: that phone needs to be replaced or the field app won't work well for them.
3. If a tech refuses to use their personal phone for work: the owner needs to provide a work phone. That's between them — don't get in the middle of it, but flag it now so it doesn't blow up on install day.

**Cell coverage check:**
1. Ask: *"Do your guys ever lose cell signal on the job?"*
2. If they work in rural areas, basements, or metal buildings with bad signal: the field app caches the last job info, but they won't get new dispatches until they have signal again. Set expectations.

---

## Before You Go — Prep Checklist

### Get From the Owner (Phone Call, Day Before)
- [ ] How many trucks / techs in the field?
- [ ] What trade? (plumbing, electrical, HVAC, general — this changes templates and parts lists)
- [ ] Do they have a website? (we'll link the booking form to it)
- [ ] What do they use now for scheduling? (paper, whiteboard, Google Calendar, ServiceTitan, Housecall Pro, or nothing)
- [ ] What do they use for invoicing? (QuickBooks, paper invoices, nothing)
- [ ] Who answers the phone? (office person, owner, spouse, answering service)
- [ ] Do they have a parts supplier they buy from most? (get the name — like Ferguson, Johnstone, Grainger, local supplier)
- [ ] WiFi password at their office
- [ ] Name + phone of the owner AND the office person (if different)

### Pack Your Install Kit
- [ ] Laptop (yours — for setup)
- [ ] Tablet (theirs — this stays at the office for dispatch)
- [ ] Phone charging cable (you'll set up the field app on techs' phones)
- [ ] Printed "Daily Cheat Sheet" cards (laminated, one for the office, one per truck)
- [ ] Printed "What Your AI Can Do" one-pager
- [ ] Business cards
- [ ] ADC branded folder with service agreement

---

## The Install — Step by Step

### Step 1: Arrive + Read the Room (15 minutes)

1. Introduce yourself: *"Hey, I'm [name] from ADC. I'm here to set up the AI system. It's gonna take about 2-3 hours. By the time I leave, you'll have a system that answers your phone, schedules your jobs, and sends invoices — and your guys will know how to use it from the truck."*

2. **Important:** These business owners are busy. They don't care how it works. They care that it works. Keep it simple. Don't use tech words.

3. Ask to sit at the desk where the office person usually works. If there's no office person, sit wherever the owner does their paperwork.

4. Look around. Notice:
   - Do they have a whiteboard with a schedule? Take a photo — you'll recreate it digitally.
   - Do they have a stack of invoices or work orders? Ask if you can look at one — you'll match the format.
   - Do they have vendor catalogs or price sheets? You'll load these into the system.

### Step 2: Set Up the Workspace (10 minutes)

1. Open Chrome on their office computer (or the tablet you brought)
2. Go to: `setup.adc3k.com`
3. Log in with your install ticket credentials
4. Click **"New Client Workspace"**
5. Fill in:
   - Business name
   - Address (this becomes the "home base" on the dispatch map)
   - Trade type (dropdown)
   - Number of field techs
   - Owner email and phone
   - Office person email and phone (if different)
6. Click **"Create Workspace"**

### Step 3: Build the Crew List (10 minutes)

1. Click **"Crew"** in the left menu
2. For each tech/crew member, add:
   - Name
   - Phone number (this is how they get job notifications)
   - Skills / certifications (example: "licensed journeyman electrician" or "backflow certified")
   - Truck number or vehicle (helps dispatch know who's where)
3. The system will text each person a link to download the field app
4. **If techs are there right now:** Help them install the app on their phone while you do the rest of the setup. It takes 2 minutes:
   - Open the text message from ADC
   - Tap the link
   - Allow location (this is how dispatch sees where they are)
   - Allow notifications (this is how they get new jobs)
   - Log in with the code from the text
5. **If techs aren't there:** Tell the owner: *"Your guys will get a text with a link. They just tap it, allow location and notifications, and they're set. Takes 2 minutes. If anyone has trouble, they can call the number on the card."*

### Step 4: Set Up the Service Menu (15 minutes)

This is the list of everything they do, with pricing.

1. Click **"Services"** in the left menu
2. The system comes with a starter list for their trade. Click **"Load [Trade] Services"**
3. Go through the list WITH the owner. For each service:
   - Is the price right? (They'll tell you their actual prices — adjust)
   - Do they offer this? (Turn off anything they don't do)
   - Missing anything? (Add their specialty services)
4. Example for a plumber:

   | Service | Their Price |
   |---------|-------------|
   | Service call / diagnostic | $89 |
   | Drain cleaning (main line) | $250-450 |
   | Water heater install (tank) | $1,200-2,500 |
   | Water heater install (tankless) | $3,000-5,500 |
   | Faucet replacement | $150-350 |
   | Toilet replacement | $300-600 |
   | Slab leak repair | $2,000-5,000 |

5. **Get their real prices.** Don't guess. Don't use the defaults. This is what goes on quotes to their customers.

### Step 5: Set Up Vendors + Parts (20 minutes)

This is what makes this different from the law firm install. Field service businesses live and die by parts and vendors.

1. Click **"Vendors"** in the left menu
2. Add each vendor/supplier they buy from:
   - Company name
   - Account number (if they have one)
   - Phone number
   - What they buy there (example: "Ferguson — all plumbing fittings and fixtures")
   - Do they have net terms? (Net 30, COD, credit card on file)
3. Click **"Parts Catalog"**
4. Two ways to load parts:

   **Option A — Quick Load (recommended for Day 1):**
   - Select their trade
   - Click "Load Standard Parts List"
   - This gives them the 200-300 most common parts for their trade with average pricing
   - They can update prices later as they buy

   **Option B — Upload Their Price Sheet:**
   - If they have a vendor price sheet (PDF, Excel, or even a photo of a catalog page)
   - Click "Upload Price Sheet"
   - The AI will read it and pull out part numbers, descriptions, and prices
   - This takes 5-10 minutes to process

5. **Truck Inventory (if they want it):**
   - Click "Truck Stock"
   - For each truck, enter what parts they keep on board
   - When a tech uses a part on a job, they mark it in the app
   - System tells the office when a truck is low on something
   - Say to the owner: *"This isn't mandatory to start. But if your guys are always running to the supply house mid-job, this'll fix that. We can set it up later if you want to start simple."*

### Step 6: Phone Answering / AI Receptionist (15 minutes)

This is usually the feature that sells them. Set it up and demo it live.

1. Click **"Phone"** in the left menu
2. Two options:

   **Option A — New Business Number (simple):**
   - System generates a local number
   - All AI-answered calls go through this number
   - They forward their existing number to this one when busy/after hours

   **Option B — Integrate with Existing Number:**
   - Click "Connect Existing"
   - Follow the prompts for their phone provider
   - AI picks up after X rings (they choose — usually 3-4)

3. Set the greeting: *"Thanks for calling [Business Name]. I can help you schedule a service appointment. What do you need help with today?"*
   - Let the owner hear it and adjust the wording to their style
   - Some want formal, some want casual. Match their vibe.

4. Set business hours:
   - During hours: AI answers overflow (when office person is on another call)
   - After hours: AI answers everything, books appointments for next business day
   - Emergency: AI asks "Is this an emergency?" — if yes, routes to owner's cell

5. **Demo it live:**
   - Call the number from your phone
   - Let the owner listen as the AI answers, asks what you need, and books an appointment
   - Show the appointment pop up on the dispatch screen
   - Say: *"That call would have gone to voicemail before. Now it's a booked job."*

### Step 7: Dispatch Board (10 minutes)

1. Click **"Dispatch"** in the left menu
2. The board shows:
   - Map with tech locations (blue dots) and jobs (red pins)
   - Today's schedule (who's going where)
   - Unassigned jobs (new calls that need a tech)
3. Show the office person (or owner):
   - How to drag a job to a tech (assign it)
   - How to see a tech's current location
   - How the tech gets a notification on their phone with:
     - Customer name + address
     - What the job is
     - Any notes from the phone call
     - One-tap navigation to the address
4. Say: *"When a call comes in — whether a person takes it or the AI takes it — it shows up here as an unassigned job. You just drag it to whoever's closest or whoever can do that type of work."*

### Step 8: Quoting + Invoicing (15 minutes)

1. Click **"Quotes & Invoices"** in the left menu
2. Set up their invoice template:
   - Upload their logo
   - Add their license number (required in most states for plumbing/electrical)
   - Add their payment methods (check, card, Venmo, Zelle — whatever they take)
   - Add their terms ("Due upon completion" or "Net 15" or whatever)
3. Show how quoting works from the field:
   - Tech opens app on their phone
   - Taps "New Quote"
   - Takes a photo of the problem (optional but powerful — customer sees what's wrong)
   - Selects services from the menu (prices auto-fill)
   - Adds parts from the catalog (prices auto-fill)
   - Taps "Send to Customer"
   - Customer gets a text with the quote — they can approve right there on their phone
   - Once approved, it becomes a work order
4. Show how invoicing works:
   - When the job is done, tech taps "Complete Job"
   - Invoice auto-generates from the approved quote
   - Customer gets a text with a link to pay
   - Payment goes to their bank account (set up Stripe or their existing processor)
5. Say: *"Your guy sends the quote from the truck. Customer approves on their phone. Work gets done. Invoice goes out before he leaves the driveway. You get paid that day. No more chasing checks."*

### Step 9: Automated Follow-Ups (5 minutes)

1. Click **"Automations"** in the left menu
2. Turn on the defaults:
   - [x] **Appointment reminder** — text to customer 24 hours before ("We'll be there tomorrow between 8-10am")
   - [x] **On-the-way notification** — text when tech marks "en route" ("Your technician is on the way, ETA 20 minutes")
   - [x] **After-service follow-up** — text next day ("How was your service? Reply with any concerns")
   - [x] **Review request** — text after 7 days ("Would you mind leaving us a review?" + link to Google)
   - [x] **Maintenance reminder** — for seasonal businesses like HVAC ("It's been 6 months since your last AC tune-up")
3. Let the owner read each message and change the wording
4. Say: *"These go out automatically. You don't have to remember to follow up. And that review request? That's how you build your Google rating without begging customers."*

---

## Training — Two Groups

### Group A: Office Person / Dispatcher (20 minutes)

Sit with them at the computer. Walk through a full cycle:

1. **A call comes in** (simulate it — call the AI number from your phone)
2. **Job appears on dispatch board** (unassigned)
3. **Assign it to a tech** (drag to the closest one)
4. **Tech gets notification** (show on your phone)
5. **Tech completes job** (mark complete in app)
6. **Invoice goes out** (show the customer text)
7. **Payment comes in** (show the dashboard)

**Say:** *"That's the whole cycle. Call comes in, job goes out, money comes back. The system handles the paperwork. You handle the people."*

### Group B: Field Techs (15 minutes — Can Do by Phone if Not Present)

If techs are there, gather them. If not, the owner can show them, or you can do a quick phone call with each one.

Show them 4 things:

1. **Getting a job:** Notification pops up → tap it → see customer info + address → tap "Navigate" → drive there
2. **Quoting:** Tap "New Quote" → pick services → pick parts → send to customer → customer approves
3. **Completing:** Tap "Complete Job" → take a photo of the finished work → invoice auto-sends
4. **Parts:** If a tech uses a part from the truck, tap "Used Part" → select it → truck inventory updates

**Say:** *"Four taps. That's all your day is. Get the job, give the quote, do the work, close it out. The app does the rest."*

**For techs who push back ("I don't need an app"):**
> *"I get it. But here's the thing — the quote goes out while you're still at the job. The customer pays before you leave. No more waiting on checks. No more filling out paper work orders at the end of the day. It's actually less work for you, not more."*

---

## Before You Leave — Final Checklist

- [ ] Office person can take a call from the dispatch board and assign it
- [ ] At least 1 tech has the field app installed and working
- [ ] Phone answering is live (call it from your phone to verify)
- [ ] Service menu has THEIR real prices (not defaults)
- [ ] At least 1 vendor is in the system with parts
- [ ] Invoice template has their logo, license number, and payment methods
- [ ] Auto follow-up texts are turned on and the owner approved the wording
- [ ] Daily Cheat Sheet card is on the dispatch desk (laminated)
- [ ] Daily Cheat Sheet card is in each truck (laminated)
- [ ] Owner has ADC support number saved in their phone
- [ ] You watched the office person do a full dispatch cycle without your help
- [ ] You watched at least 1 tech open and close a job in the app without your help
- [ ] Service agreement is signed

### Hand-Off Script:
> *"You're all set. The phone is live — it'll catch every call you miss. Your guys have the app. Quotes and invoices go out from the truck. The Daily Cheat Sheet on your desk has everything you need day-to-day."*

> *"The first week, you'll want to watch the dispatch board to make sure jobs are flowing right. After a week, it'll feel like second nature."*

> *"I'll check in with you in a couple days to make sure everything's smooth. If anything goes sideways before then, call the number on the card."*

---

## After You Leave — Follow-Up

### Day 2: Text the Owner
> *"Hey [name], it's [your name] from ADC. How did the first full day go? Any jobs run through the system yet? Holler if you need anything."*

### Day 7: Call the Owner (10 minutes)
- Ask: "How many jobs came through the AI phone this week?"
- Ask: "Are your techs using the app or fighting it?"
- Ask: "Any parts or services I need to add to the system?"
- Ask: "How's invoicing going — are customers paying through the link?"
- If a tech isn't using the app: offer to call them directly for a 5-minute walkthrough
- Log everything in your install ticket

### Day 30: Usage Check
- Pull up their dashboard at `admin.adc3k.com`
- Key metrics to check:
  - Calls answered by AI (should be going up)
  - Quotes sent from field (vs. quotes sent from office — field is the goal)
  - Average time from job complete to invoice sent (should be under 1 hour)
  - Customer review requests sent vs. reviews received
- If numbers are low: schedule a 30-minute refresher at their office
- If numbers are strong: ask for a referral to another business owner they know

---

## Troubleshooting — Common Problems

| Problem | What to Do |
|---------|------------|
| "The AI phone sounds weird" | Adjust the voice/greeting. Go to Phone → Settings → re-record or re-type the greeting. |
| "My tech won't use the app" | Talk to the tech directly. Usually it's a login issue or they didn't allow notifications. Fix the technical problem and the resistance usually goes away. If they still refuse, that's between them and the owner — not your problem to solve. |
| "Parts prices are wrong" | Go to Parts Catalog → find the item → update the price. Or upload a new vendor price sheet. Prices change — show the office person how to update them so they don't need to call you. |
| "Customer didn't get the invoice" | Check the customer's phone number in the job. 90% of the time it's a wrong number. Resend from the job screen. |
| "I need to add a new service we don't have listed" | Services → Add Service → fill in name, price range, estimated time. Takes 30 seconds. |
| "The dispatch map isn't showing my tech" | Tech needs to have location turned on in their phone settings AND in the app. Walk them through: Settings → Location → "Always" or "While Using App." |
| "I want to go back to the old way" | Don't argue. Say: "I understand. Let me connect you with our account team." Call ADC immediately. Usually they're just frustrated about one specific thing — find out what it is and fix THAT. |

---

## What You Should NOT Do

1. **Don't set prices for them.** Ask, confirm, enter. Their prices are their business.
2. **Don't promise the AI replaces their office person.** Say "it helps them" or "it catches what they miss." If the owner fires their office person and blames you, that's a problem.
3. **Don't touch their accounting.** We send invoices. We don't do their books. If they ask about QuickBooks integration, say: "We can connect to QuickBooks — let me put in a request with our team."
4. **Don't access their customer data after the install.** Your job ends when you walk out the door. If they need changes, they call support, or you go back on a new ticket.
5. **Don't install the app on a tech's personal phone without asking them.** Some people are private about their phones. Always ask: "Mind if I set up the work app on your phone?"
6. **Don't trash-talk their current system.** Even if it's a whiteboard and a shoebox full of receipts. Say: "This builds on what you already know."

---

## Key Difference: Law Firm vs. Field Services

| | Law Firm | Field Services |
|---|---------|----------------|
| **Main value** | Reading + writing documents | Answering phones + dispatching + getting paid |
| **Biggest pain** | Finding info in files, missing deadlines | Missed calls, slow quotes, chasing payments |
| **Who uses it most** | Paralegal (desk) | Office person (desk) + techs (field) |
| **Hardware** | Just a computer | Computer (office) + phones (field) |
| **Vendors/parts** | N/A | Central to the system |
| **Phone answering** | Nice to have | The killer feature |
| **Complexity** | Medium (documents) | High (people + trucks + parts + vendors) |
| **Install time** | ~2 hours | ~2.5-3 hours |
| **Follow-up effort** | Low (they either use it or don't) | Medium (techs need hand-holding, parts need updating) |

---

## Pricing — What the Customer Pays

(Fill in per your install ticket — these are standard tiers)

| Tier | Monthly | What They Get |
|------|---------|---------------|
| Solo Operator | $___/mo | 1 user, AI phone, quoting, invoicing |
| Small Crew (2-5 techs) | $___/mo | Dispatch board, crew management, vendor tracking, all features |
| Full Operation (6-15 techs) | $___/mo | Everything + priority support + dedicated account rep |

**Install fee:** $_____ (one-time, covers your visit + setup + training + hardware if included)

**Add-ons:**
- Truck inventory tracking: $___/truck/mo
- QuickBooks integration: $___/mo
- Custom vendor catalog upload: $_____ one-time

---

## Glossary — Words You Might Hear

| Word | What It Means |
|------|---------------|
| **Dispatch** | Sending a tech to a job. Like calling someone on the radio and telling them where to go. |
| **AI receptionist** | A computer that answers the phone like a person. It asks what the customer needs and books the appointment. |
| **Quote** | An estimate of what a job will cost. The app builds it from the service menu and parts list. |
| **Invoice** | The bill. Sent after the work is done. Customer pays through a link on their phone. |
| **CRM** | Customer Relationship Management. A list of all their customers with history of every job. Don't use this word with the customer — just say "your customer list." |
| **Vendor** | A company they buy parts from. Like Ferguson, Johnstone Supply, or the local electrical wholesaler. |
| **Net 30** | The vendor gives them 30 days to pay for parts. This is important for their cash flow. |
| **Parts catalog** | A list of every part with prices. Like a digital version of those thick catalogs in the back of the truck. |
| **Geo-fence** | An invisible boundary on the map. When a tech crosses it (arrives at or leaves a job site), the system knows. This is how "on-the-way" texts work. |
| **Truck stock** | The parts a tech keeps in their truck. The system tracks what's there so they don't run out. |
