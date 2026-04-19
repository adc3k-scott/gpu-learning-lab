# ADC AI Install Playbook — E-Commerce / Online Business

## Who This Is For
You're an ADC installer. This covers online stores, Shopify sellers, Amazon FBA businesses, WooCommerce shops, Etsy sellers, dropshippers, DTC brands, and subscription box companies. If they sell products online and deal with orders, inventory, and customers, this playbook applies.

---

## What You're Installing
An AI system that handles customer service, keeps inventory in sync, and drives repeat purchases. When you're done, the business will be able to:

- **AI customer service chatbot** — handles 80% of tickets automatically. *"Where's my order?" "Can I return this?" "Do you have this in blue?"* — answered instantly, 24/7. No more 48-hour response times killing reviews.
- **Inventory sync** — real-time stock levels across every channel (Shopify, Amazon, WooCommerce, Etsy). Sell on Amazon, stock updates on Shopify. No more overselling, no more cancelled orders.
- **Order tracking + proactive updates** — customers get shipping updates before they ask. *"Your order shipped! Tracking: [link]. Estimated delivery: Thursday."* Then *"Your package was delivered today. Everything look good?"*
- **Returns processing** — AI handles return requests, generates labels, processes refunds. *"I'd like to return this shirt." → "Sorry to hear that. Here's your return label: [link]. Refund will process within 3 business days of receipt."*
- **Review management** — solicits reviews from happy customers, flags negative reviews for immediate response. *"Enjoying your new [product]? Leave a review: [link]"*
- **Abandoned cart recovery** — *"You left something in your cart! Your [product] is still waiting. Complete your order: [link]"* — recovers 10-15% of abandoned carts.
- **Reorder reminders** — for consumable products: *"Running low on [product]? Reorder now and save 10%: [link]"*

**What it replaces:** The owner answering "where's my order?" 50 times a day. The oversell that tanks your Amazon rating. The 200 abandoned carts per month nobody follows up on. The returns that sit in a pile because nobody has time to process them. The 3-star reviews that could've been 5-stars if someone had responded in time.

---

## Client Minimum Requirements

### Tier 1: Cloud-Only

| Requirement | Minimum | Recommended | Why |
|-------------|---------|-------------|-----|
| **Internet** | 25 Mbps | 100+ Mbps | Syncing inventory across channels, processing images, API calls. |
| **E-commerce platform** | Any (Shopify, WooCommerce, BigCommerce, Etsy, Amazon) | Shopify or WooCommerce | Best API support, most integrations. |
| **Computer** | Any modern laptop/desktop | MacBook or Windows 10+ with 16GB RAM | For dashboard, analytics, product management. |
| **Email** | Business email | Google Workspace or Microsoft 365 | For customer communication, order confirmations. |
| **Phone** | Smartphone | Modern iPhone or Android | For notifications, quick order checks on the go. |

**Cost to client:** $0 + monthly subscription
**Best for:** Solo sellers, small shops (under 500 orders/month) with existing platform

### Tier 2: ADC Starter Kit

| Item | Spec | Approx. Cost | Notes |
|------|------|-------------|-------|
| Dedicated workstation | Laptop or desktop, 16GB RAM, SSD | $800-1,200 | For dedicated order management |
| Label printer | DYMO 4XL or Rollo | $150-200 | Shipping labels, return labels |
| Barcode scanner (optional) | USB or Bluetooth | $50-100 | For inventory receiving/counting |
| UPS | 600VA | $60-80 | Keep processing during power blips |
| **Total** | | **$1,060-1,580** | |

### Tier 3: ADC Growth Kit

| Item | Spec | Approx. Cost | Notes |
|------|------|-------------|-------|
| Starter kit | | $1,060-1,580 | Everything above |
| Second monitor | 27" 4K | $300-400 | Dashboard on one screen, orders on the other |
| Thermal receipt printer | Star Micronics | $200-300 | Packing slips for warehouse |
| Warehouse tablet | iPad or Android | $300-500 | For pick/pack/ship in the warehouse |
| **Total** | | **$1,860-2,780** | |

### Tier 4: NVIDIA DGX Spark

| Item | Spec | Cost |
|------|------|------|
| **NVIDIA DGX Spark** | GB10 Grace Blackwell, 128GB, 1 PFLOPS FP4, 4TB encrypted NVMe | **$4,699** |
| Growth kit | | $1,860-2,780 |
| **Total** | | **~$6,560-7,480** |

**When to recommend:**
- High-volume seller (5,000+ orders/month) needing on-premise AI for product recommendations
- Seller with proprietary product data they want to keep off cloud servers
- Multi-brand operation running separate storefronts from one system
- AI-powered product photography or description generation at scale

---

## The Install — Step by Step

### Step 1: Arrive + Understand the Business (10 minutes)

1. **Timing:** This is a remote install — schedule a video call or screen share. No on-site visit needed unless they have a warehouse.
2. Understand their setup:
   - What platform(s) do they sell on? (Shopify, Amazon, WooCommerce, Etsy, eBay)
   - How many SKUs?
   - How many orders per day/month?
   - Do they ship themselves or use a 3PL (third-party logistics)?
   - Where is inventory stored? (Home, warehouse, 3PL, dropship)
3. Ask:
   - *"What's your biggest headache right now?"* (Usually: customer service volume or inventory sync)
   - *"How many customer service tickets do you get per day?"*
   - *"What's your return rate?"*
   - *"Are you selling on multiple channels?"* If yes: *"Have you ever oversold?"*
   - *"What's your abandoned cart rate?"* (They can find this in Shopify/WooCommerce analytics)

### Step 2: Create Workspace (10 minutes)

1. `setup.adc3k.com` → New Client Workspace
2. Type: E-Commerce / Online Retail
3. Number of sales channels
4. Monthly order volume (this sets the right tier)
5. Primary platform (Shopify, WooCommerce, etc.)

### Step 3: Connect Sales Channels (15 minutes)

1. Click **"Integrations"**
2. Connect each sales channel:

   **Shopify:**
   - Install the ADC AI app from the Shopify App Store
   - Authorize API access (orders, products, customers, inventory)
   - Sync products — verify SKU count matches

   **Amazon Seller Central:**
   - Connect via SP-API (Selling Partner API)
   - Authorize: orders, inventory, returns, messaging
   - Map Amazon ASINs to Shopify SKUs (if multi-channel)

   **WooCommerce:**
   - Install plugin or connect via REST API
   - Generate API keys (Consumer Key + Consumer Secret)
   - Sync products and orders

   **Etsy / eBay:**
   - OAuth connection
   - Map listings to master SKU list

3. **Inventory sync test:** Change a quantity on one channel, verify it updates on others within 60 seconds. This is the moment they realize the value.

### Step 4: AI Customer Service Chatbot (20 minutes)

This is the killer feature. 80% of e-commerce support tickets are the same 10 questions.

1. Click **"Customer Service AI"**
2. Configure knowledge base:
   - **Shipping policy:** Processing time, carriers used, delivery estimates by region, international shipping (yes/no)
   - **Return policy:** Window (30 days?), condition requirements, who pays return shipping, refund vs. exchange vs. store credit
   - **Product FAQ:** Size guides, material info, care instructions, compatibility
   - **Order status:** AI pulls real-time tracking from carrier APIs (USPS, UPS, FedEx, DHL)
3. Set up the chatbot widget:
   - Install on website (Shopify: add script to theme, WooCommerce: add plugin)
   - Customize appearance (colors, logo, greeting message)
   - Greeting: *"Hi! I can help with order tracking, returns, product questions, or anything else. What can I help with?"*
4. Configure escalation rules:
   - AI handles: order status, return labels, product questions, shipping estimates
   - Escalate to human: complaints, damaged items, custom orders, anything with emotional distress
   - Escalation method: email to owner with full conversation transcript
5. **Test it:** Open the website, ask common questions:
   - *"Where's my order?"* → AI asks for order number → pulls tracking
   - *"I want to return this"* → AI asks for order number → generates return label
   - *"What size should I get?"* → AI references size guide
   - *"This arrived damaged"* → AI escalates to human with photos

### Step 5: Shipping Integration (10 minutes)

1. Click **"Shipping"**
2. Connect carrier accounts:
   - USPS (via Pitney Bowes, EasyPost, or ShipStation)
   - UPS
   - FedEx
   - DHL (if international)
3. Set up shipping rules:
   - Under 1 lb → USPS First Class
   - 1-5 lbs → USPS Priority or UPS Ground (rate shop)
   - Over 5 lbs → UPS Ground
   - International → DHL eCommerce or USPS Priority International
4. **Proactive tracking notifications:**
   - Order confirmed → *"Thanks for your order! We're packing it now."*
   - Shipped → *"Your order is on its way! Track it here: [link]"*
   - Out for delivery → *"Your package is out for delivery today!"*
   - Delivered → *"Your package was delivered. Everything look good? [link to support]"*

### Step 6: Returns + Refund Automation (10 minutes)

1. Click **"Returns"**
2. Configure return flow:
   - Customer requests return (via chatbot, email, or returns portal)
   - AI checks: within return window? Order verified? Reason?
   - Auto-approve if within policy → generate return label → email to customer
   - Flag for review if: outside window, high-value item, suspected abuse
3. Refund rules:
   - Auto-refund on carrier scan (item received at warehouse)
   - Or: manual approval required for refunds over $X
4. Return reasons tracking:
   - AI categorizes: wrong size, didn't like it, damaged, wrong item, other
   - Monthly report: if "wrong size" is 40% of returns, you need a better size guide

### Step 7: Abandoned Cart Recovery (10 minutes)

1. Click **"Automations"**
2. Abandoned cart sequence:
   - [x] **1 hour after abandonment:** *"Still thinking about [product]? Your cart is saved: [link]"*
   - [x] **24 hours:** *"Your [product] is waiting! Complete your order: [link]"*
   - [x] **72 hours (with incentive):** *"Last chance — get 10% off your cart with code COMEBACK10: [link]"*
3. **Browse abandonment** (visited product page but didn't add to cart):
   - [x] **24 hours:** *"Still interested in [product]? It's selling fast: [link]"*
4. **Post-purchase:**
   - [x] **Day 3:** *"Your [product] should be arriving soon! Need anything? [support link]"*
   - [x] **Day 14:** *"How are you liking your [product]? Leave a review: [link]"*
   - [x] **Day 30 (consumables only):** *"Time for a refill? Reorder [product] and save 10%: [link]"*
   - [x] **Day 60:** *"We miss you! Here's what's new: [link to new arrivals]"*

### Step 8: Review Management (10 minutes)

1. Click **"Reviews"**
2. Set up review solicitation:
   - Trigger: 7 days after delivery (give them time to use the product)
   - Channel: email + SMS
   - Message: *"How's your [product]? Your review helps other shoppers: [link]"*
3. Review monitoring:
   - AI scans for new reviews on Google, Amazon, Trustpilot, Yelp
   - Positive (4-5 stars): auto-thank — *"Thanks for the kind words! We're glad you love it."*
   - Negative (1-2 stars): alert owner immediately with suggested response
   - 3 stars: AI drafts a response for owner approval
4. **Amazon review strategy:** AI can identify customers who received their order and had no issues — these are your best review candidates.

### Step 9: Analytics Dashboard (10 minutes)

1. Click **"Dashboard"**
2. Configure key metrics:
   - Orders today / this week / this month
   - Revenue by channel
   - Customer service tickets (AI-resolved vs. escalated)
   - Abandoned cart recovery rate
   - Return rate by reason
   - Inventory alerts (low stock, out of stock)
   - Review score trending
3. Set up alerts:
   - Inventory below threshold → email + SMS
   - Negative review posted → instant notification
   - Customer service escalation → instant notification
   - Daily sales summary at end of day

---

## Training (15 minutes)

### Owner / Operator (10 minutes)
1. **Dashboard overview:** Where to see orders, revenue, customer service metrics
2. **Customer service escalations:** How to handle tickets the AI couldn't resolve
3. **Inventory management:** How to update stock, add new products, set reorder points
4. **Review responses:** How to approve/edit AI-drafted responses to negative reviews
5. **Reports:** Weekly and monthly performance reports

### Staff (if any — 5 minutes)
1. **Order processing:** How to view and fulfill orders from the dashboard
2. **Customer inquiries:** When and how to take over from the AI chatbot
3. **Returns processing:** How to check returned items and approve refunds
4. **Inventory updates:** How to log received inventory

**Key line:** *"The AI handles the repetitive stuff — tracking questions, return labels, cart reminders. You focus on product, marketing, and growth. That's how you scale without hiring a customer service team."*

---

## Before You Leave — Final Checklist

- [ ] All sales channels connected and inventory synced (change a quantity, verify it updates everywhere)
- [ ] AI chatbot live on website and tested (ask 5 common questions, verify correct answers)
- [ ] Shipping carriers connected and rate shopping working
- [ ] Abandoned cart recovery sequence active (create a test abandoned cart, verify emails trigger)
- [ ] Return portal live and tested (submit a test return, verify label generation)
- [ ] Review solicitation emails scheduled
- [ ] Proactive shipping notifications configured
- [ ] Analytics dashboard showing live data
- [ ] Escalation routing tested (trigger an escalation, verify owner receives it)
- [ ] Owner can access dashboard on phone
- [ ] Quick Start guide emailed to owner
- [ ] Service agreement signed

---

## After You Leave

### Day 2 — Text
*"Hey [name] — how's the AI chatbot doing? Check your dashboard for the customer service stats. If any responses need tweaking, let me know and I'll adjust the knowledge base."*

### Day 7 — Call
- How many tickets has the AI handled vs. escalated? (Target: 70%+ AI-resolved in week 1)
- Any abandoned cart recoveries? Check the revenue recovered number.
- Any inventory sync issues? (Oversells, stock discrepancies)
- Review the customer service transcripts — are the AI responses accurate?
- Adjust: chatbot answers, escalation rules, cart recovery timing

### Day 30 — Metrics Review
Pull these numbers and compare to pre-install:
- Customer service response time (should be instant now vs. 24-48 hrs before)
- Tickets resolved by AI (target: 80%+)
- Abandoned cart recovery rate (target: 10-15%)
- Review volume (should be increasing)
- Return processing time (should be same-day now)
- Revenue recovered from abandoned carts ($X)
- Time saved on customer service (hours/week)

---

## Troubleshooting

| Problem | What to Do |
|---------|------------|
| "Inventory isn't syncing between channels" | Check API connections. Most sync issues are expired tokens — reconnect the channel. If using Amazon, verify SP-API permissions haven't changed. |
| "The chatbot is giving wrong answers" | Review the knowledge base. 90% of bad answers come from incomplete product info or outdated shipping policies. Update the source data, not the AI. |
| "Customers say the chatbot feels robotic" | Adjust the tone in settings. Add the brand's voice — casual, professional, quirky, whatever matches them. Add their actual product names, not generic descriptions. |
| "Abandoned cart emails aren't converting" | Check timing and incentive. If the 10% off isn't working, try free shipping. If nothing converts, the problem is pricing or product-market fit — not the automation. |
| "I'm getting too many escalations" | The AI needs more training data. Review escalated tickets, add the answers to the knowledge base. Every escalation that gets resolved should become a new AI response. |
| "Return rate went up since install" | It didn't go up — you're just tracking it now. Making returns easier increases customer satisfaction and repeat purchases. Show them the lifetime value data. |
| "Amazon and Shopify prices don't match" | Inventory syncs, but pricing is managed per channel. If they want uniform pricing, set it in the master product catalog. If they price differently per channel (common on Amazon), that's intentional. |

---

## What You Should NOT Do

1. **Don't access their payment processor.** You don't need Stripe/PayPal credentials. The platform handles payments.
2. **Don't change product prices or descriptions.** Enter what they tell you. If their pricing is wrong, that's their call.
3. **Don't promise specific revenue numbers.** "Most stores recover 10-15% of abandoned carts" is fine. "You'll make $10K more per month" is not.
4. **Don't store their platform passwords.** Use API keys and OAuth tokens only.
5. **Don't disable their existing customer service channels.** The AI supplements — it doesn't replace human support for complex issues.
6. **Don't set up discount codes without approval.** The abandoned cart 10% off needs the owner's explicit sign-off.

---

## Glossary

| Word | What It Means |
|------|---------------|
| **SKU** | Stock Keeping Unit. A unique identifier for each product variant. "Blue T-Shirt, Size M" and "Blue T-Shirt, Size L" are different SKUs. |
| **3PL** | Third-Party Logistics. A warehouse that stores and ships your products for you (ShipBob, Deliverr, Amazon FBA). |
| **FBA** | Fulfillment by Amazon. Amazon stores, packs, and ships your product. You send them inventory, they handle the rest. Higher fees, but Prime badge. |
| **Abandoned cart** | A customer added products to their cart but didn't complete checkout. Industry average: 70% of carts are abandoned. |
| **AOV** | Average Order Value. Total revenue divided by number of orders. Higher AOV = more profit per transaction. |
| **DTC** | Direct to Consumer. Selling directly to customers through your own website, not through Amazon or retailers. Higher margins but you handle everything. |
| **Dropship** | Selling products you don't physically hold. Customer orders from you, you order from supplier, supplier ships to customer. No inventory risk but slim margins. |
| **SP-API** | Selling Partner API. Amazon's API for accessing orders, inventory, and customer data programmatically. Replaced MWS (Marketplace Web Service). |
| **Rate shopping** | Comparing shipping rates across carriers in real-time to find the cheapest/fastest option for each package. |
| **Chargeback** | When a customer disputes a charge with their credit card company. You lose the sale amount plus a fee ($15-25). AI can help prevent these by resolving issues before they escalate. |
