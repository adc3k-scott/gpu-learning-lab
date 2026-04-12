# ADC AI Install Playbook — Auto Shop / Mechanic / Body Shop

## Who This Is For
You're an ADC installer. This covers independent auto repair shops, tire shops, body shops, transmission shops, diesel/fleet shops, and quick lube/oil change places. If they fix vehicles, this playbook applies.

---

## What You're Installing
An AI system that turns estimates into approvals and approvals into payments — faster than the customer can shop around. When you're done, the shop will be able to:

- **Photo-to-estimate** — tech takes photos under the car, AI identifies the parts, pulls pricing from their vendors, builds the estimate with labor. Customer sees photos of what's broken + the price. Approval rate goes way up when the customer can SEE the problem.
- **Answer every call** — AI handles appointment scheduling, status checks ("is my car ready?"), and basic questions. No more missed calls while the service writer is under a hood.
- **Digital vehicle inspection (DVI)** — tech goes through a checklist on a tablet. Green/yellow/red for each item. Photos of worn brakes, leaking gaskets, cracked belts. Customer gets a text with the full report — sees exactly what needs attention now vs. later.
- **Parts lookup + ordering** — AI searches multiple vendors (AutoZone Commercial, O'Reilly Pro, NAPA, Worldpac, OE dealer) for best price and availability. One screen, all vendors.
- **Customer approval workflow** — estimate goes to customer by text. They see photos + line items + total. They tap "Approve" or "Call me to discuss." No more phone tag.
- **Invoicing + payment** — when the job is done, invoice auto-generates from the approved estimate. Customer pays by link before they pick up the car.
- **Vehicle history** — every car that comes in builds a history. Next time: *"Mr. Johnson, last time you were here we flagged your rear brakes at 3mm. They're probably due now."*

**What it replaces:** The service writer hand-writing estimates on carbon copies. The tech who can't explain what's wrong to a customer who doesn't speak car. The owner calling every customer to get approval. The estimate that sits on the counter for 3 days because nobody followed up.

---

## Client Minimum Requirements

### Tier 1: Cloud-Only (Use What They Have)

| Requirement | Minimum | Recommended | Why |
|-------------|---------|-------------|-----|
| **Internet** | 25 Mbps down / 5 Mbps up | 50+ Mbps | Photo uploads from the shop floor + parts lookups + customer texts. |
| **WiFi coverage** | Must reach the shop floor | WiFi extender or mesh to reach bays | If WiFi doesn't reach the bays, techs can't upload inspection photos. This is the #1 install killer. |
| **Computer (front counter)** | Any, 8GB RAM | 16GB, SSD, 24"+ monitor | Service writer lives here — estimates, approvals, scheduling, invoicing. |
| **Tablet (shop floor)** | iPad or Android tablet | iPad with rugged case (OtterBox, Gumdrop) | Techs use this for inspections + photos. It WILL get dirty and dropped. |
| **Phone** | iPhone or Android, any modern | Good camera phone | For photos under the car if they don't want a tablet per bay. |
| **Shop management software** | None required, but if they have one... | If they use Mitchell, ShopWare, Tekmetric, AutoFluent, or Shop-Ware — we integrate. | We can work standalone or alongside their existing system. |

**Cost to client:** $0-500 (tablet for shop floor) + monthly subscription
**Best for:** Small shops (1-3 bays) with existing computer and decent WiFi

### Tier 2: ADC Starter Kit

| Item | Spec | Approx. Cost | Notes |
|------|------|-------------|-------|
| Front counter PC | Intel i5, 16GB RAM, 512GB SSD | $500-700 | Dedicated estimate/invoicing machine |
| Monitor | 24" 1080p | $150-200 | Service writer's main screen |
| Shop tablet(s) | iPad + OtterBox Defender + screen protector | $500-650 each | One per 2-3 bays. Will get greasy. OtterBox is mandatory. |
| WiFi extender / mesh | TP-Link mesh or similar | $150-250 | Gets WiFi to the back bays. Critical. |
| Label/receipt printer | Thermal printer | $100-150 | For work orders, bay tags |
| UPS | 600VA | $60-80 | |
| **Total (3-bay shop, 1 tablet)** | | **$1,460-2,030** | |
| **Total (6-bay shop, 2 tablets)** | | **$1,960-2,680** | |

### Tier 3: NVIDIA DGX Spark

| Item | Spec | Cost |
|------|------|------|
| **NVIDIA DGX Spark** | GB10 Grace Blackwell, 128GB, 1 PFLOPS FP4, 4TB encrypted NVMe | **$4,699** |
| Starter kit additions | | $1,460-2,680 |
| **Total** | | **~$6,160-7,380** |

**When to recommend DGX Spark for auto shops:**
- Fleet/commercial shop handling sensitive client data (government vehicles, police fleets)
- Multi-location shop owner who wants centralized AI across all shops
- Shop in a rural area with bad internet (Spark runs parts lookup from cached catalogs offline)
- Body shop doing insurance estimates — keeps photo evidence on-site, encrypted

**The pitch:**
> *"Every photo your tech takes, every estimate, every customer's vehicle history — it all lives on this encrypted box in your office. Nobody else has access. And the AI runs your parts lookup locally, so even when the internet hiccups, your guys are still building estimates."*

### Pre-Install: WiFi Check (Most Common Problem)

**This will make or break the install.** Shops are metal buildings with lifts and heavy equipment. WiFi dies in the back.

1. Before the install, go to the shop with your phone
2. Stand in the furthest bay from the router
3. Run speedtest.net
4. If below 10 Mbps in the bays: they need a WiFi extender or mesh system. Add it to the hardware list.
5. If their WiFi doesn't reach the shop floor AT ALL: install a mesh system as part of the setup (bill it)

---

## The Install — Step by Step

### Step 1: Arrive + Walk the Shop (15 minutes)

1. **Go during a slow time.** Early morning before the first car is on the lift, or late afternoon when they're wrapping up.
2. Introduce yourself to the owner AND the lead tech/foreman. Both need to be on board.
3. Walk the shop:
   - How many bays? Which ones are used for which (alignment, tires, general, diesel)?
   - Where's the parts counter / ordering computer?
   - Where does the service writer sit?
   - Where do customers wait?
   - Where's the WiFi router? (Check signal strength in each bay)
4. Ask:
   - *"What shop management software do you use?"* (Mitchell, ShopWare, Tekmetric, pen and paper?)
   - *"Where do you order parts?"* (AutoZone Pro, O'Reilly Pro, NAPA, Worldpac, dealer?)
   - *"How do you give estimates right now?"* (Phone call? Paper? Software?)
   - *"What's your biggest headache?"* (Usually: getting customer approval on estimates, or parts ordering, or missed calls)

### Step 2: Create Workspace + Integrations (15 minutes)

1. `setup.adc3k.com` → New Client Workspace
2. Fill in:
   - Shop name
   - Type: General repair / Tire / Body / Transmission / Quick lube / Diesel-Fleet
   - Number of bays
   - Number of techs
   - Shop management system (if any)
3. Connect integrations:
   - **Parts vendors:** Log into each vendor's pro portal (they type credentials). This lets the AI search all vendors at once for parts + pricing.
   - **Shop management software:** If they have one, connect it. If they don't, our system IS their shop management.
   - **Accounting:** QuickBooks, if they use it — for invoice sync. Not required Day 1.

### Step 3: Set Up Service Menu + Labor Rates (15 minutes)

1. Click **"Services"**
2. Load the standard service list for their shop type
3. Set their labor rate:
   - Ask: *"What's your labor rate per hour?"*
   - Common range: $100-175/hr (varies by market and shop type)
   - Body shops: may have separate rates for body, paint, mechanical, frame
4. Go through the top services and set labor times:

   | Service | Typical Labor Hours | At $130/hr |
   |---------|--------------------:|------------|
   | Oil change | 0.3-0.5 | $39-65 |
   | Brake pads (front) | 1.0-1.5 | $130-195 |
   | Brake pads + rotors (front) | 1.5-2.0 | $195-260 |
   | Alternator replacement | 1.0-2.0 | $130-260 |
   | Timing belt | 3.0-6.0 | $390-780 |
   | AC recharge | 0.5-1.0 | $65-130 |
   | Transmission flush | 1.0-1.5 | $130-195 |
   | Engine diagnostic | 1.0 | $130 |

5. **If they use a labor guide (Mitchell, ALLDATA, Chilton):** The system can pull book times automatically. Ask if they have a subscription and connect it.

### Step 4: Digital Vehicle Inspection (DVI) Setup (15 minutes)

**This is the killer feature for auto shops. This is what sells the work.**

1. Click **"Inspections"**
2. Load the standard inspection template (or customize):
   - Brakes (pads, rotors, calipers, lines, fluid)
   - Tires (tread depth, pressure, age, wear pattern)
   - Suspension (shocks/struts, ball joints, tie rods, bushings)
   - Steering (rack, pump, fluid, belt)
   - Engine (oil level, coolant, belts, hoses, leaks)
   - Transmission (fluid, mounts, leaks)
   - Electrical (battery, alternator, starter, lights)
   - Exhaust (muffler, catalytic converter, hangers, leaks)
   - Body/underbody (rust, frame, damage)
   - Fluids (all levels + condition)
   - Wipers, cabin filter, engine filter
3. Each item gets a status:
   - **Green** = good, no action needed
   - **Yellow** = monitor / will need attention soon
   - **Red** = needs repair now (safety or reliability concern)
4. **Photo capability:** For every yellow or red item, the tech takes a photo
5. Show the tech on the tablet:
   - Open inspection → select vehicle → go down the checklist → tap green/yellow/red → take photos for yellow/red → add notes → submit
   - **Takes 10-15 minutes per car**
6. Show the service writer:
   - Inspection comes in → review → convert yellow/red items to an estimate → send to customer
   - Customer gets a text: *"Your vehicle inspection is ready. Tap to view: [link]"*
   - Customer sees: photos of their worn brakes, tread depth measurement, leaking gasket — with green/yellow/red ratings and the price to fix each item
   - Customer taps "Approve All" or selects specific items to approve

**Say to the owner:**
> *"When your customer sees a photo of their brake pad at 1mm next to a new pad at 12mm, they don't need to be convinced. The photo sells the job. Your approval rate on recommended work will go up 30-50% in the first month."*

### Step 5: Parts Lookup + Ordering (15 minutes)

1. Click **"Parts"**
2. Connect each vendor account (tech types their credentials):
   - AutoZone Commercial / AllData
   - O'Reilly First Call
   - NAPA TRACS
   - Worldpac (if they do import/European)
   - Dealer parts portals (if applicable)
   - Local machine shop (manual entry — name, phone, common items)
3. Show the parts search:
   - Enter year/make/model + part needed
   - System searches ALL connected vendors simultaneously
   - Shows: price, availability (in stock vs. order), delivery time
   - One tap to order from the best option
4. **Key selling point:** *"Instead of logging into 4 different websites and comparing prices, your guy searches once and sees everything. He picks the best price in-stock and orders in one tap. Saves 15-20 minutes per estimate."*

### Step 6: Estimate + Approval Workflow (10 minutes)

1. Click **"Estimates"**
2. Walk through the workflow:
   - Inspection flags red/yellow items
   - Service writer clicks "Create Estimate"
   - Parts auto-populate from the lookup (price, part number)
   - Labor auto-calculates from the service menu (book time × labor rate)
   - Total generates automatically
   - Shop supplies / environmental fees / tax added per their settings
3. **Customer gets a text:**
   - Photos of the issues
   - Line items with prices
   - "Approve" / "Decline" / "Call Me" buttons
   - Digital signature for approval
4. Once approved:
   - Work order generates automatically
   - Parts order submits (if not already in stock)
   - Tech gets the work order on their tablet
5. When job is complete:
   - Tech marks "Complete"
   - Invoice auto-generates from approved estimate
   - Customer gets text with payment link
   - Payment processes before pickup

### Step 7: AI Phone (10 minutes)

1. Set up greeting: *"Thanks for calling [Shop Name]. I can help you schedule a service appointment, check on the status of your vehicle, or answer questions. How can I help?"*
2. Key routing:
   - **"Is my car ready?"** → AI checks work order status → gives update: *"Your 2019 Camry is still in the bay. The tech is working on the brake job now. We expect it to be ready by 3 PM."*
   - **Appointment booking** → AI books based on bay availability and service type
   - **"How much for..."** → AI gives a range from the service menu: *"A front brake job typically runs $350-500 depending on the vehicle. Would you like to schedule a free inspection?"*
   - **Tow truck / emergency** → route to shop owner's cell
3. **After-hours:** AI takes messages and books appointments for next business day

### Step 8: Automated Customer Communication (5 minutes)

- [x] **Appointment confirmation** — "Your appointment is confirmed for Tuesday 8 AM. Please drop off the keys if you arrive before we open."
- [x] **Vehicle status update** — when tech marks milestones: "Inspection complete — check your text for results" / "Parts ordered — expected tomorrow" / "Your car is ready for pickup"
- [x] **Pickup notification** — "Your [year make model] is ready! Total: $XXX. Pay online and skip the wait: [link]"
- [x] **Follow-up (3 days)** — "How's the car running? Any concerns after your recent service?"
- [x] **Review request (7 days)** — Google review link
- [x] **Maintenance reminder** — "Your [year make model] is due for an oil change (last one was 4 months ago / 4,500 miles ago)"
- [x] **Declined work follow-up (30 days)** — "Hi [name], last month we flagged your rear brakes as needing attention. Would you like to schedule that? They're only going to get worse."

---

## Training (30 minutes)

### Service Writer / Front Counter (15 minutes)
Full cycle:
1. Car arrives → look up customer + vehicle (or create new)
2. Create inspection → assign to tech
3. Tech completes inspection with photos
4. Review inspection → create estimate from red/yellow items
5. Send estimate to customer → wait for approval
6. Approval comes in → create work order → order parts
7. Tech completes work → invoice generates → send payment link
8. Customer pays → car goes home

### Techs (10 minutes)
Three things:
1. **Inspection:** Open tablet → select vehicle → go through checklist → green/yellow/red → photos → submit
2. **Work order:** See approved jobs → work the job → mark milestones (parts in, in progress, complete)
3. **Parts:** Search parts → compare prices → order

**For techs who resist:**
> *"The photos sell the work. When the customer sees the photo, they approve it. When they can't see it, they say 'let me think about it' and never come back. More approved work = more hours for you."*

### Owner (5 minutes)
Dashboard overview:
- Sales today/this week/this month
- Average repair order (ARO) — target varies, but trending up is good
- Inspection-to-estimate conversion rate
- Estimate approval rate (target: 70%+)
- Parts margin
- Tech productivity (hours billed vs. hours clocked)

---

## Before You Leave — Final Checklist

- [ ] WiFi reaches all bays (verified with speed test in the furthest bay)
- [ ] POS/shop management connected (if applicable)
- [ ] At least 2 parts vendors connected
- [ ] Service menu loaded with their labor rate and times
- [ ] DVI template set up and tested (one test inspection completed)
- [ ] AI phone is live
- [ ] One full cycle demonstrated: inspection → estimate → (simulated) approval → work order → invoice
- [ ] Tablet(s) set up in the shop with rugged cases
- [ ] All users can log in (service writer, techs, owner)
- [ ] Automated texts turned on
- [ ] Quick Start card at the front counter and in the shop
- [ ] Service agreement signed

---

## Troubleshooting

| Problem | What to Do |
|---------|------------|
| "WiFi keeps dropping in the bays" | Metal buildings kill WiFi. Add a mesh node or access point closer to the bays. This is the #1 problem in auto shops. |
| "Customer didn't get the estimate text" | Check phone number. Wrong numbers are the most common issue. Also check if their phone blocks unknown texts. |
| "Parts prices are wrong" | Vendor pricing changes constantly. The system pulls live pricing at search time. If prices seem stale, re-authorize the vendor connection. |
| "The inspection takes too long" | First few inspections take 20+ minutes. By week two, techs get it down to 10-12 minutes. It's like learning any new tool — clunky at first, fast later. |
| "Customer won't approve from a text" | Some customers (especially older) want a phone call. The system has a "Call Me" button on the estimate. When they tap it, it routes to the service writer with the estimate pulled up on screen. |
| "Tech took a blurry photo" | Show them: wipe the lens, hold still, make sure the flash is on. Bad photos don't sell work. Take 2 seconds to get a clear shot. |

---

## What You Should NOT Do

1. **Don't diagnose cars.** You're a tech installer, not a mechanic. If someone asks what's wrong with their car, say: *"That's a question for the guys here — I just set up the software."*
2. **Don't touch their tools, lifts, or vehicles.** Stay in the office area and use the shop floor only for WiFi testing and tablet setup.
3. **Don't set their labor rate.** Ask what it is, enter it. If they ask what it should be, say: *"That depends on your market — your shop, your call."*
4. **Don't promise approval rate increases with specific numbers.** Say "most shops see improvement" — don't say "you'll get 50% more approvals."
5. **Don't trash their current system.** Even if they're writing estimates on a napkin. Say: *"This builds on what you already know how to do."*
6. **Don't give your opinion on their prices.** Even if their $80 oil change seems high or their $350 brake job seems low. Their pricing is their business.

---

## Glossary

| Word | What It Means |
|------|---------------|
| **DVI** | Digital Vehicle Inspection. A checklist the tech does on a tablet with photos. This is the big sell. |
| **ARO** | Average Repair Order. The average dollar amount per visit. Higher = better. |
| **Book time** | The standard labor time for a job, from a labor guide (Mitchell, ALLDATA). Example: "Front brakes are 1.5 hours book time." |
| **Flag hours** | Hours a tech bills (based on book time), not clock hours. A good tech flags 8-10 hours in an 8-hour day. |
| **Service writer** | The person at the front counter who talks to customers, writes estimates, and manages workflow. Sometimes the owner. |
| **RO** | Repair Order. The work order for a job. Each car gets an RO number. |
| **Come-back** | A car that comes back because the repair wasn't done right. Track these — they cost money and reputation. |
| **Parts margin** | The markup on parts. Shop buys a brake pad for $40, sells it for $70 = 43% margin. AI can track this. |
| **Core charge** | A deposit on old parts (alternators, starters). When the old part is returned to the vendor, the deposit is refunded. Track these — free money if you remember. |
| **Estimate vs. Invoice** | Estimate = what you think it'll cost. Invoice = what it actually cost. They should be close. If they're always different, your estimating process needs work. |
