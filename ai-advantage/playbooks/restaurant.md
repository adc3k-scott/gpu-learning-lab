# ADC AI Install Playbook — Restaurant / Bar / Food Service

## Who This Is For
You're an ADC installer. This covers sit-down restaurants, fast casual, bars, catering operations, and food trucks. If they cook food and sell it, this playbook applies.

---

## What You're Installing
An AI system that watches the money — because in restaurants, the money disappears fast if nobody's watching. When you're done, the owner will be able to:

- **Know their food cost in real-time** — not at the end of the month when it's too late. AI tracks every ingredient, every plate, every waste event. "Your chicken cost went from 28% to 34% this week because your Thursday cook is over-portioning."
- **Automate ordering** — AI watches inventory levels and says "You need to order 40 lbs of chicken breast by tomorrow to make it through the weekend." One tap to send the order to the vendor.
- **Build the schedule** — AI builds staff schedule based on projected sales (weather, events, day of week, historical data). No more 8 servers on a Tuesday or 3 on a Saturday.
- **Answer the phone** — reservations, takeout orders, hours, directions. AI handles it so the host isn't juggling the phone and a line of guests.
- **Menu engineering** — AI tells the owner which menu items make money and which ones lose money. "Your $14 pasta costs $2.10 to make. Your $16 burger costs $7.20. Push the pasta."
- **Review + reputation management** — monitors Google, Yelp, TripAdvisor. Alerts on negative reviews so the owner can respond fast.

**What it replaces:** The owner doing inventory on a clipboard at midnight. The manager spending 3 hours on the schedule every week. The to-go order that got lost because the phone rang during the rush. The end-of-month surprise when food cost is at 38%.

---

## Client Minimum Requirements

### Tier 1: Cloud-Only (Use What They Have)

| Requirement | Minimum | Recommended | Why |
|-------------|---------|-------------|-----|
| **Internet** | 50 Mbps down / 10 Mbps up | 100+ Mbps | POS + phone + ordering all running. Restaurants already have WiFi for POS — it just needs to be decent. |
| **POS System** | Any modern POS (Toast, Square, Clover, Aloha, Lightspeed) | Toast or Square | We integrate with the POS to pull sales data. If they're using a cash register from 1995, they need a POS first — that's a separate conversation. |
| **Computer (office/back)** | Any laptop or desktop | Laptop in the office | For the owner/manager to view dashboards, reports, scheduling. |
| **Tablet (optional)** | iPad or Android tablet | iPad | For inventory counting (walk the cooler, tap items). |
| **Phone** | iPhone 12+ or Android 10+ | Any modern smartphone | Owner gets alerts, approves orders, checks reports on the go. |

**Cost to client:** $0 hardware (if they have a POS already) + monthly subscription
**Best for:** Single-location restaurants with an existing modern POS

### Tier 2: ADC Starter Kit

| Item | Spec | Approx. Cost | Notes |
|------|------|-------------|-------|
| Tablet (inventory) | iPad 10th gen + rugged case | $400-500 | Walk-in cooler proof. For inventory counts. |
| Kitchen display (optional) | 15" touchscreen, wall-mount | $400-600 | Replaces paper tickets. Shows orders from POS + phone. |
| Label printer (optional) | Brother QL-820NWB or similar | $150-200 | For prep labels, expiration dates. |
| Office laptop | Basic, 8GB RAM | $400-500 | For manager — schedule, reports, vendor orders. |
| UPS | 600VA | $60-80 | Keeps the system running during power dips. |
| **Total** | | **$1,410-1,880** | |

### Tier 3: NVIDIA DGX Spark

| Item | Spec | Cost |
|------|------|------|
| **NVIDIA DGX Spark** | GB10 Grace Blackwell, 128GB, 1 PFLOPS FP4, 4TB encrypted NVMe | **$4,699** |
| Starter kit additions (above) | | $1,410-1,880 |
| **Total** | | **~$6,110-6,580** |

**When to recommend DGX Spark for restaurants:**
- Multi-location operator (3+ restaurants) — centralized AI managing all locations
- High-volume catering operation processing hundreds of orders/day
- Owner who wants camera-based inventory (AI watches waste in real-time via kitchen cameras — requires local compute)
- Franchise owner who doesn't want data on someone else's cloud

**The pitch:**
> *"This box watches your food cost like a hawk. It sees every order, every delivery, every plate that goes out. It'll tell you on Tuesday that you're trending 3% over food cost this week — not on the 30th when you can't do anything about it."*

### Pre-Install: POS Check (Critical)
1. Ask: *"What POS system do you use?"*
2. If Toast, Square, Clover, Lightspeed, or Aloha: we integrate. Proceed.
3. If they use a cash register or a POS from the early 2000s: **they need to upgrade their POS first.** Our system pulls data from the POS. No POS integration = no food cost tracking. Be honest: *"We need a modern POS to connect to. Once you have that, we can set everything up."*
4. If they don't know: ask to see it. Take a photo of the brand/model and send it to ADC to confirm compatibility.

---

## The Install — Step by Step

### Step 1: Arrive + Assess (15 minutes)

1. **Go during off-hours.** NOT during lunch or dinner rush. Best time: 2-4 PM (between services) or before open.
2. Introduce yourself to the owner AND the kitchen manager/head chef (if different people). Both need to buy in.
3. Walk the restaurant:
   - **Kitchen:** Where does prep happen? Where's the walk-in? Where do deliveries come in?
   - **Front of house:** Where's the POS? Where does the host stand? Is there a to-go station?
   - **Office:** Where does the owner do paperwork? This is where the dashboard computer goes.
4. Ask to see:
   - A recent food order / vendor invoice
   - Their current menu with prices
   - How they currently count inventory (clipboard? spreadsheet? "we don't"?)

### Step 2: Create Workspace + Connect POS (15 minutes)

1. `setup.adc3k.com` → New Client Workspace
2. Fill in:
   - Restaurant name
   - Type: Full service / Fast casual / Bar / Catering / Food truck
   - Cuisine type (this loads relevant ingredient lists)
   - POS system
   - Number of locations
3. **Connect the POS:**
   - Click "Integrations" → select their POS brand
   - Log in with THEIR POS admin credentials (they type these in, not you — you don't need to know their password)
   - Authorize the connection
   - Verify: pull up today's sales to confirm data is flowing

### Step 3: Build the Menu (20 minutes)

**This is the most important step.** The menu is how the AI calculates food cost.

1. Click **"Menu"** in the left menu
2. Two ways to load:

   **Option A: Upload the menu** (fastest)
   - Take a photo of their printed menu OR get a PDF
   - Upload it — AI reads the menu items and prices
   - Go through each item with the owner/chef and verify

   **Option B: Manual entry**
   - Enter each menu item with price
   - Group by category (Appetizers, Entrees, Desserts, Drinks, etc.)

3. **Recipe costing (do this for their top 10 items at minimum):**
   - Click an item → "Add Recipe"
   - Enter ingredients and amounts:
     ```
     Cheeseburger ($14):
       8 oz ground beef    - $0.90 per patty
       1 brioche bun       - $0.45
       2 slices cheese     - $0.30
       Lettuce/tomato/onion - $0.25
       Fries (6 oz)        - $0.35
       Packaging (if to-go) - $0.15
       TOTAL FOOD COST: $2.40
       FOOD COST %: 17.1%
     ```
   - **Ask the chef:** *"Walk me through what goes on this plate and how much of each."* They know this in their sleep.
   - Don't try to cost every single item on Day 1. Start with the top sellers and the most expensive dishes. Build out over time.

4. **Say to the owner:** *"Right now you can see that your burger makes you $11.60 per plate and your steak makes you $8.00. This is menu engineering — we put the high-profit items where customers' eyes go first."*

### Step 4: Set Up Vendors + Ordering (15 minutes)

1. Click **"Vendors"**
2. Add each food vendor:
   - Name (Sysco, US Foods, local meat purveyor, produce guy, beverage distributor, etc.)
   - Account number
   - Order contact (phone, email, or online portal)
   - Delivery days (example: Sysco delivers Mon/Thu)
   - Payment terms
3. **Load their last few orders:**
   - If they have invoices (paper or email): upload them. AI reads the items, quantities, and prices.
   - This builds their purchase history and price tracking
4. Set up **auto-order suggestions:**
   - AI watches sales velocity + current inventory
   - Before each vendor's delivery cutoff, the system suggests an order
   - Manager reviews and approves with one tap
   - If vendor has an online portal, order can submit automatically

### Step 5: Inventory Setup (15 minutes)

1. Click **"Inventory"**
2. Load the standard ingredient list for their cuisine type
3. **Walk-in count (do this with the chef/kitchen manager):**
   - Open the app on the tablet
   - Walk into the walk-in cooler together
   - Count each item: *"How many cases of chicken? How many boxes of lettuce?"*
   - Enter counts in the app
   - This establishes the baseline. After this, the system tracks usage based on POS sales + recipe costs
4. **Set par levels:**
   - For each key ingredient, ask: *"How much do you want to have on hand at all times?"*
   - Example: "I always want at least 3 cases of chicken" → set par at 3
   - When inventory drops below par, the system alerts and suggests a vendor order
5. **Waste tracking:**
   - Show the kitchen staff how to log waste: burned steak, dropped plate, expired product
   - Tap "Waste" → select item → enter quantity → reason (burned, expired, dropped, returned)
   - *"This is how you find the leaks. If you're throwing away $200 in food every week, this tells you exactly what and why."*

### Step 6: AI Phone + Online Ordering (15 minutes)

1. Click **"Phone"** → set up AI receptionist
2. Restaurant greeting: *"Thanks for calling [Restaurant Name]. I can help you make a reservation, place a to-go order, or answer questions about our menu. What can I do for you?"*
3. Set up:
   - **Reservations:** Party size → date/time → available tables → confirm → text confirmation
   - **To-go orders:** AI walks through the menu with the caller, takes the order, gives a total, gives a pickup time
   - **Common questions:** Hours, location, parking, do-you-have, allergens, dress code
   - **Large parties / events:** Route to manager
4. **Online ordering (if they want it):**
   - Click "Online Menu" → generates a link
   - Customer browses menu, places order, pays online
   - Order appears on POS / kitchen display
   - Can put on their website or Google Business profile

### Step 7: Staff Scheduling (10 minutes)

1. Click **"Schedule"**
2. Add each employee:
   - Name, role (server, bartender, cook, host, dishwasher, manager)
   - Availability (when they CAN work)
   - Max hours (full-time cap, overtime rules)
   - Pay rate (this feeds labor cost calculations)
3. AI builds the schedule based on:
   - Projected sales (historical data + weather + day of week + local events)
   - Labor cost target (industry standard: 25-30% of sales)
   - Employee availability + preferences
4. Manager reviews → adjusts if needed → publishes → employees get notified on their phones
5. **Say:** *"The system builds the schedule in 2 minutes based on how busy you'll actually be. If there's a Saints game Thursday night, it knows you'll be busier than a normal Thursday and adds staff."*

### Step 8: Automated Communications (5 minutes)

1. Click **"Automations"**
   - [x] Reservation confirmation text
   - [x] Reservation reminder (2 hours before)
   - [x] To-go order ready notification
   - [x] Review request (day after dine-in): *"How was your meal at [name]? We'd love your feedback: [Google link]"*
   - [x] Birthday/anniversary (if collected): *"Happy birthday! Come celebrate with us — enjoy a free dessert this week."*
   - [x] Negative review alert to owner (immediate — any review under 3 stars)

---

## Training (30 minutes)

### Owner/Manager (20 minutes)
Show them the dashboard — this is what they'll check every morning:
1. **Yesterday's sales** — pulled from POS automatically
2. **Food cost %** — actual vs. target (target: 28-32% for most restaurants)
3. **Labor cost %** — actual vs. target (target: 25-30%)
4. **Prime cost** — food + labor combined (target: under 60%)
5. **Inventory alerts** — what's low, what needs to be ordered
6. **Waste log** — what got thrown away yesterday
7. **Reviews** — any new reviews with sentiment score

**Say:** *"Check this every morning with your coffee. 5 minutes. If food cost is creeping up, you'll see it Monday — not at the end of the month. If a cook is over-portioning, you'll see it in the waste log. This is your early warning system."*

### Kitchen Staff (10 minutes)
Two things:
1. **Waste logging** — when you throw something away, log it. Takes 5 seconds.
2. **Inventory counting** — once a week (or daily for key items), walk the cooler with the tablet and count.

**For cooks who push back:**
> *"I know it's one more thing. But when the owner sees that food cost is on target, nobody's getting their hours cut. This protects your shifts."*

---

## Before You Leave — Final Checklist

- [ ] POS is connected and pulling sales data
- [ ] Menu is loaded with prices (at minimum — recipe costing on top 10 is bonus)
- [ ] At least 3 vendors are set up with order history
- [ ] Baseline inventory count is done (walk-in + dry storage at minimum)
- [ ] Par levels set for top 20 ingredients
- [ ] AI phone is live and answering
- [ ] Staff schedule is built for current/next week
- [ ] Owner can read the morning dashboard
- [ ] Kitchen staff knows how to log waste
- [ ] Quick Start card is posted in the office AND the kitchen
- [ ] Service agreement signed

### Hand-Off Script:
> *"You're set up. The system is watching your food cost, your labor cost, and your inventory. Check the dashboard every morning — it takes 5 minutes and it'll save you thousands."*

> *"The biggest thing: make your kitchen staff log waste. That's where the leaks are. If they log it, you can fix it. If they don't log it, the money just disappears."*

---

## Troubleshooting

| Problem | What to Do |
|---------|------------|
| "Food cost numbers look wrong" | Recipe costing is probably off. Go back to the top-selling items and verify ingredient amounts + prices with the chef. Garbage in = garbage out. |
| "My POS isn't syncing" | Check the POS integration — sometimes the token expires and needs to be re-authorized. Log into POS admin and re-connect. |
| "Staff won't log waste" | Talk to the owner. This is a management problem, not a tech problem. Some owners put a tablet ON the waste bin — you have to log before you dump. |
| "The AI phone took a wrong order" | Check the order in the system. If the AI misheard, adjust the menu item names to be more distinct (example: "chicken parm" vs. "chicken parmesan" — pick one). |
| "The schedule is wrong" | AI needs 2-4 weeks of sales data to predict accurately. First week, tell the manager to override as needed. It gets better fast. |

---

## What You Should NOT Do

1. **Don't install during a rush.** 2-4 PM or before open. Never during service.
2. **Don't touch the food.** You're setting up tech, not prepping salads. Stay out of the kitchen's way.
3. **Don't tell the chef how to run their kitchen.** You show them the tools. They decide how to use them.
4. **Don't promise exact food cost savings.** Say: "Most restaurants find 2-5% savings in the first 90 days" — not "you'll save $50,000."
5. **Don't remove or change their POS.** We plug into it. We don't replace it.
6. **Don't eat for free.** If they offer you a meal, graciously accept or decline. Don't ask for one or expect one.

---

## Glossary

| Word | What It Means |
|------|---------------|
| **Food cost %** | Cost of ingredients ÷ menu price. A $14 burger that costs $2.40 to make = 17.1% food cost. Industry target: 28-32%. |
| **Labor cost %** | Total labor (wages + taxes + benefits) ÷ total sales. Target: 25-30%. |
| **Prime cost** | Food cost + labor cost. The two biggest expenses. Target: under 60% of sales. |
| **Par level** | The minimum amount of an ingredient you want on hand. When inventory drops below par, the system alerts. |
| **86'd** | Restaurant term for "we're out of it." If the AI sees an ingredient hit zero, it can auto-86 menu items that use it. |
| **POS** | Point of Sale. The system they ring up orders on (Toast, Square, etc.). |
| **Covers** | Number of guests served. "We did 180 covers tonight" = 180 guests. |
| **COGS** | Cost of Goods Sold. Same as food cost for restaurants. |
| **Comp** | A free item given to a guest (usually to fix a complaint). Track these — they affect food cost. |
| **Waste** | Food that gets thrown away without being sold. Burned, expired, dropped, over-portioned, or returned. Track it. |
