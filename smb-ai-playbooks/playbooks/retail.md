# ADC AI Install Playbook — Retail Store

## Who This Is For
You're an ADC installer. This covers boutiques, specialty shops, hardware stores, pet stores, vape shops, sporting goods, gift shops, convenience stores — any brick-and-mortar store that sells physical products. If they have shelves with stuff on them and a register, this playbook applies.

---

## What You're Installing
An AI system that watches inventory, predicts demand, and keeps customers coming back. When you're done, the store will be able to:

- **Never run out of best sellers** — AI watches what's selling, what's slowing, and what's about to run out. *"You've sold 14 of these this week. At this rate, you'll be out by Thursday. Reorder now?"*
- **Auto-reorder from vendors** — when inventory hits a reorder point, AI generates a PO with the right quantities and sends it to the vendor. One tap to approve.
- **Know what's making money** — margin by product, by category, by vendor. *"Your candle section has 62% margin but your greeting cards are at 18%. Consider replacing cards with more candle inventory."*
- **Customer loyalty + repeat business** — AI tracks purchase history, sends personalized texts: *"Hi Sarah, the skincare line you bought in January has a new product. Come see it this week — 10% off for returning customers."*
- **Seasonal planning** — AI analyzes last year's sales by month and says: *"Last December you sold 4x your normal volume of gift sets. Start ordering in October."*
- **Answer the phone** — *"Do you carry [product]? What are your hours? Do you have [item] in stock?"* AI checks inventory and answers.
- **Staff scheduling** — based on sales patterns: more staff on weekends, fewer on slow weekdays.

**What it replaces:** The owner counting inventory by hand on Sunday night. The best seller that's been out of stock for a week and nobody noticed. The loyal customer who stopped coming because nobody followed up. The $3,000 of dead stock gathering dust in the back.

---

## Client Minimum Requirements

### Tier 1: Cloud-Only

| Requirement | Minimum | Recommended | Why |
|-------------|---------|-------------|-----|
| **Internet** | 25 Mbps | 50+ Mbps | POS + inventory + customer texts all running. |
| **POS System** | Any modern POS (Square, Shopify POS, Lightspeed, Clover) | Square or Shopify POS | We integrate with the POS to pull sales data. If they're using a cash drawer with no tracking, they need a POS first. |
| **Computer** | Any, 8GB RAM | Laptop or tablet for back office | Inventory management, vendor ordering, reports. |
| **Phone** | iPhone or Android | Modern smartphone | Owner notifications, approvals, dashboard. |
| **Barcode scanner** | Not required but helpful | USB or Bluetooth scanner ($50-100) | For inventory counts. If they don't have barcodes, we work with manual SKUs. |

**Cost to client:** $0-100 + monthly subscription
**Best for:** Small shops with existing POS

### Tier 2: ADC Starter Kit

| Item | Spec | Approx. Cost | Notes |
|------|------|-------------|-------|
| Tablet (inventory counts) | iPad + case | $400-500 | Walk the store, count stock, scan barcodes. |
| Barcode scanner | Bluetooth | $80-120 | Speeds up inventory counts 10x. |
| Label printer | Brother QL-series | $100-150 | Shelf labels, price tags, barcodes for non-barcoded items. |
| Office laptop | Basic, 8GB RAM | $400-500 | For ordering, reports. |
| UPS | 600VA | $60-80 | |
| **Total** | | **$1,040-1,350** | |

### Tier 3: NVIDIA DGX Spark

| Item | Spec | Cost |
|------|------|------|
| **NVIDIA DGX Spark** | GB10 Grace Blackwell, 128GB, 1 PFLOPS FP4, 4TB encrypted NVMe | **$4,699** |
| Starter kit | | $1,040-1,350 |
| **Total** | | **~$5,740-6,050** |

**When to recommend:**
- Multi-location retailer (3+ stores) with centralized inventory management
- Store with 5,000+ SKUs where demand forecasting needs heavy compute
- Owner who wants AI-powered visual inventory (cameras watching shelves — needs local compute)
- Store handling customer financial data (layaway, financing programs)

---

## The Install — Step by Step

### Step 1: Arrive + Walk the Store (15 minutes)

1. Meet during off-peak hours (Tuesday morning, not Saturday afternoon).
2. Walk every aisle. Notice:
   - How are products organized? (By category, by brand, by price?)
   - Where are the best sellers? (Usually near the register or entrance)
   - What's in the back room? (Overstock, dead stock, seasonal storage?)
   - How do they price things? (Stickers, shelf labels, barcode scans?)
3. Ask:
   - *"What's your best seller?"* and *"What never sells?"* — these two answers tell you everything.
   - *"How do you know when to reorder?"* (Usually: "when I notice it's empty" — the system fixes this)
   - *"Who are your main vendors / distributors?"*
   - *"Do you sell online too?"* (Shopify, Etsy, Amazon — affects inventory sync)

### Step 2: Create Workspace + Connect POS (15 minutes)

1. `setup.adc3k.com` → New Client Workspace
2. Type: Retail — select subcategory
3. Connect POS:
   - Log into their POS admin → authorize ADC integration
   - Verify: pull today's sales to confirm data is flowing
   - POS gives us: every sale, every item, every timestamp. This is the foundation.

### Step 3: Load Inventory (30 minutes — This Is the Big One)

**This step takes the longest. The quality of the install depends on this.**

1. Click **"Inventory"**
2. Three ways to load:

   **Option A: POS already has inventory** (best case)
   - If they've been tracking inventory in their POS (Square, Shopify, Lightspeed), import it
   - Click "Import from POS" → pulls all products with SKUs, prices, and current quantities
   - Verify a sample: walk to the shelf, count 5 random items, compare to the system number

   **Option B: They have a spreadsheet**
   - Upload their Excel/CSV product list
   - AI maps columns to: product name, SKU, category, cost, retail price, quantity on hand, vendor, reorder point

   **Option C: Start from scratch** (they have nothing)
   - This is a longer process. Two approaches:
     - **Scan and count:** Walk the store with the barcode scanner. Scan each product, enter the count. For a small store (500-1,000 items), this takes 2-4 hours. May need to schedule a second visit.
     - **Start with top sellers only:** Enter the 50-100 items that sell the most. Add the rest over time.
   - **Be honest:** *"Getting your inventory into the system is the hardest part. Once it's in, the system keeps it updated automatically based on sales. But we need a clean starting count."*

3. For each product (at minimum):
   - Product name
   - SKU or barcode
   - Category
   - Cost (what they pay the vendor)
   - Retail price (what they sell it for)
   - Current quantity on hand
   - Reorder point (how many before they need to reorder)
   - Vendor

4. **Margin calculation:** Once cost and price are in, the system automatically shows:
   - Margin per item (retail - cost)
   - Margin % ((retail - cost) / retail)
   - Category-level margins
   - This is usually an eye-opener. Most retailers don't know their margins by product.

### Step 4: Set Up Vendors + Auto-Reorder (15 minutes)

1. Click **"Vendors"**
2. For each vendor:
   - Company name, account number
   - Contact / sales rep
   - Order method (phone, email, online portal, EDI)
   - Minimum order / free shipping threshold
   - Lead time (how many days from order to delivery)
   - Payment terms
3. **Auto-reorder rules:**
   - When quantity hits reorder point → generate a suggested PO
   - Include: what to order, how many (based on sales velocity + lead time), which vendor, estimated cost
   - Owner gets a notification: *"Reorder suggestion: 24 units of [product] from [vendor]. Estimated cost: $XXX. Approve?"*
   - One tap to approve → PO sends to vendor (email or portal)

### Step 5: AI Phone (10 minutes)

1. Set up: *"Thanks for calling [Store Name]. I can check if we have a product in stock, tell you our hours, or help with anything else. What are you looking for?"*
2. Key feature: **real-time inventory check**
   - Caller: *"Do you have the blue ceramic vase?"*
   - AI checks inventory → *"Yes, we have 3 in stock. Would you like me to hold one for you?"*
   - If holding: logs it with caller's name, holds for 24 hours, alerts staff
3. After hours: *"We're currently closed. Our hours are [hours]. I can check stock for you — what are you looking for?"*

### Step 6: Customer Loyalty / CRM (10 minutes)

1. Click **"Customers"**
2. Set up loyalty program:
   - Points per dollar spent (example: 1 point per $1)
   - Reward threshold (example: 100 points = $10 off)
   - Or simpler: spend $200, get $20 off next visit
3. Customer capture:
   - At checkout, POS prompts: "Enter phone number for rewards"
   - Customer enters phone → creates profile → tracks purchases
4. Automated outreach:
   - [x] **Welcome:** *"Thanks for joining [Store] rewards! You'll earn points with every purchase."*
   - [x] **Reward earned:** *"You've earned $10 in rewards! Use it on your next visit."*
   - [x] **Win-back (60 days inactive):** *"We miss you at [Store]! Come back this week and enjoy 15% off."*
   - [x] **Birthday:** *"Happy birthday, [name]! Enjoy 20% off your next purchase."*
   - [x] **New arrival:** *"New [product category] just arrived! Come see what's new: [link]"*
   - [x] **Review request:** *"How was your recent visit? We'd love your feedback: [Google link]"*

### Step 7: Reports + Insights (5 minutes)

Show the owner the dashboard:
- **Sales today / this week / this month** — with comparison to same period last year
- **Top sellers** — what's moving
- **Slow movers** — what's collecting dust (markdown candidates)
- **Margin report** — by product, by category, by vendor
- **Inventory value** — total dollars sitting on shelves
- **Sell-through rate** — how fast inventory turns over
- **Reorder alerts** — what's running low

**Say:** *"Check this every morning. 5 minutes. You'll know what's selling, what's dying, and what needs to be reordered. No more guessing."*

### Step 8: Staff Scheduling (if applicable — 5 minutes)

1. Click **"Schedule"**
2. Add employees, availability, roles
3. AI schedules based on:
   - Historical sales by day of week and hour
   - More staff during peak hours (Saturday, holiday seasons)
   - Fewer during slow periods
4. Employees get schedule via text

---

## Training (20 minutes)

### Owner (15 minutes)
1. Dashboard — daily numbers, margins, alerts
2. Reorder approval — how to review and approve suggested POs
3. Customer loyalty — how to see purchase history, send targeted promos
4. Slow movers — what to markdown or discontinue

### Staff (5 minutes)
1. How to check inventory on the tablet/phone (*"Does a customer ask if you have something? Check here."*)
2. How to capture a customer for loyalty (*"Always ask for their phone number at checkout."*)
3. How to log a return or damaged item

---

## Before You Leave — Final Checklist

- [ ] POS connected and pulling sales data
- [ ] Inventory loaded (at minimum: top 50 products with accurate counts)
- [ ] At least 2 vendors set up with reorder points
- [ ] AI phone is live (call it and ask "do you have [item]?")
- [ ] Customer loyalty program active (test: enter a fake customer, make a test purchase)
- [ ] Owner can read the dashboard — top sellers, slow movers, margins
- [ ] Staff knows how to check inventory and capture customer info
- [ ] Quick Start card at the register
- [ ] Service agreement signed

---

## Troubleshooting

| Problem | What to Do |
|---------|------------|
| "Inventory counts are wrong" | Start with a recount on the items that are off. Counts drift because of theft, damage, and returns that weren't logged. The system gets more accurate over time as it learns from sales data. |
| "The AI said we have it but we don't" | The system relies on accurate starting counts. If a sale wasn't rung up or an item was stolen, the system doesn't know. This self-corrects with regular cycle counts (count a few items each day). |
| "I don't want to enter all this inventory" | Start with just the top sellers. Add more over time. 50 products managed well is better than 1,000 products entered sloppily. |
| "My vendor doesn't accept email orders" | Some vendors are old school — phone only. The system generates the PO; the owner calls and reads it off. Still saves time. |
| "Customers won't give their phone number" | Some won't. That's fine. Don't force it. But most will if there's a clear reward: "Enter your number and you'll earn $10 off after 10 visits." |

---

## What You Should NOT Do

1. **Don't tell them what to stock.** You're setting up the system, not running their store.
2. **Don't set prices or markups.** Enter what they tell you.
3. **Don't reorganize their store.** Even if their layout makes no sense to you.
4. **Don't handle cash or operate the register.** You're not a cashier.
5. **Don't photograph their vendor pricing.** That's their competitive info.
6. **Don't promise the system prevents theft.** It tracks inventory, which helps detect theft patterns, but it's not a security system.

---

## Glossary

| Word | What It Means |
|------|---------------|
| **SKU** | Stock Keeping Unit. A unique code for each product. Like a social security number for an item. |
| **POS** | Point of Sale. The register system. Where they ring up sales. |
| **Margin** | How much money they make on an item. Retail price minus cost. |
| **Reorder point** | The inventory level that triggers a reorder. When stock hits this number, the system says "time to buy more." |
| **PO** | Purchase Order. An order sent to a vendor for products. |
| **Dead stock** | Products that haven't sold in months. Tying up cash and shelf space. |
| **Sell-through rate** | How fast inventory sells. High = good (products flying off shelves). Low = bad (products sitting). |
| **Shrinkage** | Inventory loss from theft, damage, or errors. The gap between what the system says you have and what you actually have. |
| **Cycle count** | Counting a small section of inventory each day instead of doing a full count once a year. More accurate, less painful. |
| **MOQ** | Minimum Order Quantity. The smallest amount a vendor will sell you. Sometimes you have to buy 24 even if you only need 6. |
