# ADC AI Install Playbook — Salon / Barber / Spa

## Who This Is For
You're an ADC installer. This covers hair salons, barbershops, nail salons, spas, med spas, waxing studios, and lash/brow bars. If they book appointments and work on people, this playbook applies.

---

## What You're Installing
An AI system that fills the book and keeps clients coming back. When you're done, the shop will be able to:

- **Online booking 24/7** — clients book on their phone anytime. No calling during business hours. *"Book your next appointment: [link]"* — picks provider, service, date/time. Done.
- **AI phone** — answers calls when the stylist has scissors in hand. Books the appointment, answers questions (*"Do you do balayage?" "How much is a men's cut?"*), gives directions.
- **Client preferences** — AI remembers everything. *"Sarah likes her layers long, always gets a blowout, prefers Aveda products, sits with Maria."* Next visit: *"Welcome back Sarah — same as last time?"*
- **Automatic rebooking** — *"It's been 6 weeks since your last cut. Ready to rebook? Tap here: [link]"* — this is the #1 revenue feature.
- **No-show protection** — confirmation texts 24hrs and 2hrs before. No-show? AI reschedules or fills the slot from the waitlist.
- **Product tracking** — retail products on the shelf (shampoo, styling products, skincare). AI tracks what sells and what doesn't. Alerts when stock is low.
- **Review building** — after every visit: *"How was your visit with [stylist]? Leave us a review: [Google link]"*

**What it replaces:** The phone ringing while the stylist is mid-highlight. The client who hasn't been in for 4 months and nobody noticed. The 2 PM Tuesday that sits empty because nobody's booking. The retail products gathering dust because nobody tracks them.

---

## Client Minimum Requirements

### Tier 1: Cloud-Only

| Requirement | Minimum | Recommended | Why |
|-------------|---------|-------------|-----|
| **Internet** | 25 Mbps | 50+ Mbps | Booking, phone, POS all running. |
| **Existing booking software** | None required | If they use Square Appointments, Vagaro, GlossGenius, Fresha, or Boulevard — we integrate | |
| **Computer or tablet** | iPad or any computer | iPad at the front desk | For check-in, booking, POS. |
| **Phone** | Any smartphone | Modern iPhone or Android | For stylists to check their book, get notifications. |
| **POS** | Any (Square, Clover) | Square | For retail sales tracking. |

**Cost to client:** $0 + monthly subscription
**Best for:** Solo stylists or small shops (1-4 chairs) with existing devices

### Tier 2: ADC Starter Kit

| Item | Spec | Approx. Cost | Notes |
|------|------|-------------|-------|
| iPad (front desk) | iPad + stand + case | $450-600 | Check-in, booking, POS |
| Wall-mount tablet (optional) | iPad or Android on wall bracket | $500-700 | Client self-check-in at entrance |
| Card reader | Square Reader or similar | $0-50 | For payments |
| Bluetooth speaker (optional) | | $50-100 | Play hold music or ambient sound |
| UPS | 600VA | $60-80 | |
| **Total** | | **$1,060-1,530** | |

### Tier 3: NVIDIA DGX Spark

| Item | Spec | Cost |
|------|------|------|
| **NVIDIA DGX Spark** | GB10 Grace Blackwell, 128GB, 1 PFLOPS FP4, 4TB encrypted NVMe | **$4,699** |
| Starter kit | | $1,060-1,530 |
| **Total** | | **~$5,760-6,230** |

**When to recommend:**
- Med spa handling patient health info (Botox, fillers, laser — HIPAA-adjacent)
- Multi-location salon/spa chain (5+ locations)
- High-end spa with celebrity or high-profile clientele (privacy)
- Salon wanting AI-powered consultation (photo analysis for style recommendations — local compute needed)

---

## The Install — Step by Step

### Step 1: Arrive + Understand the Vibe (10 minutes)

1. **Timing:** Before open or during a slow period (Tuesday/Wednesday morning).
2. Walk the shop:
   - How many chairs/stations?
   - Booth renters or employees? (This affects scheduling — booth renters set their own hours)
   - Retail area? What products?
   - Front desk setup? (Receptionist, or stylists answer their own phone?)
3. Ask:
   - *"How do clients book right now?"* (Phone, Instagram DM, walk-in, online)
   - *"What's your biggest no-show problem?"*
   - *"Do you sell retail products?"* How much per month?
   - *"Do your stylists have their own following/clientele or does the shop assign clients?"*

### Step 2: Create Workspace (10 minutes)

1. `setup.adc3k.com` → New Client Workspace
2. Type: Salon / Barbershop / Spa / Med Spa
3. Number of providers (stylists, barbers, estheticians, massage therapists)
4. Employee vs. booth renter model

### Step 3: Service Menu + Pricing (15 minutes)

1. Click **"Services"**
2. Enter every service they offer:

   **Salon example:**
   | Service | Duration | Price |
   |---------|----------|-------|
   | Women's cut + style | 45 min | $55 |
   | Men's cut | 30 min | $30 |
   | Kids' cut | 20 min | $20 |
   | Blowout | 30 min | $40 |
   | Single process color | 60 min | $85+ |
   | Highlights (partial) | 90 min | $120+ |
   | Highlights (full) | 120 min | $175+ |
   | Balayage | 120-180 min | $200+ |
   | Deep conditioning | 15 min add-on | $25 |
   | Keratin treatment | 120-180 min | $250+ |

   **Barbershop example:**
   | Service | Duration | Price |
   |---------|----------|-------|
   | Men's cut | 30 min | $25 |
   | Skin fade | 30 min | $30 |
   | Beard trim | 15 min | $15 |
   | Cut + beard | 45 min | $35 |
   | Kids' cut | 20 min | $18 |
   | Hot towel shave | 30 min | $30 |
   | Line up | 15 min | $15 |

3. **Get their real prices.** Many salons have a menu on the wall — use it. Some stylists have different pricing (senior stylist vs. junior) — set this up per provider.
4. **Processing time:** For color services, set "processing time" separately. A color might be 15 min application + 30 min processing + 15 min rinse/style. The chair is occupied but the stylist can do another client during processing (advanced scheduling).

### Step 4: Provider Schedules (10 minutes)

1. Click **"Providers"**
2. For each stylist/barber:
   - Name
   - Services they offer (not all stylists do all services)
   - Working hours (may vary by day)
   - Lunch break
   - Days off
   - **For booth renters:** They may set their own schedule — enter it and they can adjust via the app.
3. **If they have a receptionist:** Set them up as admin (sees all schedules, can book for any provider).
4. **If no receptionist (most barbershops, small salons):** Each provider manages their own book via the app. Online booking goes directly to their calendar.

### Step 5: Online Booking (10 minutes)

1. Click **"Online Booking"**
2. Generate the booking link
3. Configure:
   - Which services are bookable online (some shops want color consultations by phone only)
   - How far in advance (30 days? 60 days?)
   - Minimum notice for booking (24 hours? Same-day?)
   - Cancellation policy (24-hour cancellation? Late cancel fee?)
4. **Where the link goes:**
   - Instagram bio (most important for salons — this is where clients find them)
   - Google Business profile
   - Facebook page
   - Their website (if they have one)
   - Printed on business cards or table cards in the shop
5. **Demo it:** Open the link on your phone, book an appointment, show it appear on the schedule. This is usually the "oh nice" moment.

### Step 6: Client Profiles + Preferences (10 minutes)

1. Click **"Clients"**
2. If they have existing clients in another system, import them
3. For each client (builds over time):
   - Name, phone, email
   - Preferred provider
   - Service history (auto-populated from bookings)
   - **Preferences / notes:**
     - Hair: *"Prefers 2" off length, doesn't like layers too short around face, always blow-dry style"*
     - Color: *"Formula: 6N + 7A, 20vol, 35min process"*
     - Products: *"Uses Olaplex #3 at home"*
     - Personal: *"Has a daughter named Emma starting kindergarten"* (relationship building)
   - Allergies (important for color, skin treatments)
4. **Say:** *"When a client comes in and you remember their name, their kid's name, and exactly how they like their hair — that's why they come back to YOU and not the shop down the street. This system remembers it for you."*

### Step 7: AI Phone (10 minutes)

1. Greeting: *"Thanks for calling [Shop Name]. I can help you book an appointment, check pricing, or answer questions. How can I help?"*
2. Booking flow: AI asks for service, preferred provider (or "anyone available"), date/time preferences, books it
3. Common questions:
   - *"How much is a haircut?"* → pulls from service menu
   - *"Do you do extensions?"* → checks service list
   - *"What are your hours?"* → reads from schedule
   - *"Do you take walk-ins?"* → configured per shop policy
4. **Walk-in management:** If the shop takes walk-ins, AI can check current availability: *"We have an opening in about 20 minutes with [stylist]. Would you like to come in?"*

### Step 8: Automated Rebooking + Communication (10 minutes)

This is the money feature. The average salon loses 30% of its revenue to clients who just... forget to rebook.

1. Click **"Automations"**
   - [x] **Booking confirmation:** *"Your appointment with [stylist] is confirmed for [date] at [time]."*
   - [x] **24-hour reminder:** *"See you tomorrow at [time]! Reply C to confirm or R to reschedule."*
   - [x] **2-hour reminder:** *"Almost time! [Stylist] is looking forward to seeing you at [time]."*
   - [x] **Post-visit thank you (same day):** *"Thanks for coming in today, [name]! Loving the new look?"*
   - [x] **Review request (2 days):** *"How was your experience with [stylist]? We'd love a review: [Google link]"*
   - [x] **Rebook reminder (based on service cycle):**
     - Haircut: 4-6 weeks → *"It's been 5 weeks since your last cut. Ready to rebook? [link]"*
     - Color: 4-8 weeks → *"Time for a touch-up? Your color appointment is overdue. Book here: [link]"*
     - Brow wax: 3-4 weeks
     - Facial: 4-6 weeks
   - [x] **Birthday:** *"Happy birthday, [name]! Treat yourself — enjoy 20% off your next visit this month."*
   - [x] **Win-back (90 days no visit):** *"We miss you, [name]! Come back and enjoy $10 off your next service: [link]"*

2. **No-show recovery:**
   - If client no-shows → text within 1 hour: *"We missed you today! Would you like to reschedule? [link]"*
   - If client no-shows 3 times: flag for the shop to decide (some charge a deposit on future bookings)

### Step 9: Retail Inventory (if applicable — 5 minutes)

1. Click **"Retail"**
2. Enter products on the shelf:
   - Product name, brand, cost, retail price, quantity
3. Connect to POS (Square, etc.) so sales automatically deduct from inventory
4. Reorder alerts when stock is low
5. **Upsell prompt:** After a haircut, AI can text: *"The Olaplex treatment [stylist] used today keeps your hair healthy between visits. Get it at the shop or order here: [link]"*

---

## Training (15 minutes)

### Receptionist / Front Desk (if applicable — 5 minutes)
1. How to check the booking schedule
2. How to add walk-ins
3. How to check a client in
4. How to process retail sales

### Stylists / Barbers (10 minutes)
1. **Their schedule:** How to see their book, block time off, adjust hours
2. **Client notes:** How to add preferences and formulas after a service
3. **Rebooking:** How the automated reminders work — they don't have to ask "when do you want to come back?" anymore. The system does it.
4. **Online booking link:** Where it is, how to share it on their personal Instagram

**Key line:** *"Share the booking link in your Instagram bio. When a follower wants an appointment, they don't have to call — they just tap and book. You get clients while you sleep."*

---

## Before You Leave — Final Checklist

- [ ] All providers set up with services, hours, and pricing
- [ ] Online booking link generated and tested (book a test appointment on your phone)
- [ ] AI phone live and answering (call it, book an appointment by voice)
- [ ] Automated rebooking reminders turned on (with correct cycle times per service)
- [ ] Client profiles started (import existing or at minimum enter 10-20 regulars)
- [ ] Retail inventory loaded (if applicable)
- [ ] Booking link placed on: Instagram bio, Google Business, business cards/table cards
- [ ] Each provider can view their schedule and add client notes
- [ ] Quick Start card at the front desk or each station
- [ ] Service agreement signed

---

## Troubleshooting

| Problem | What to Do |
|---------|------------|
| "Clients are booking the wrong service" | Make service names clearer in the online menu. "Haircut" is vague — use "Women's Cut + Blowdry" and "Men's Buzz Cut" instead. |
| "I'm getting double-booked" | Check processing time settings. If a color service takes 2 hours total but only 30 min of it is in-chair, make sure the system accounts for the processing gap correctly. |
| "My booth renters won't use it" | Show them the Instagram booking link angle. If their clients can book directly to them with zero effort, most will adopt it. If they still resist, that's their choice — don't force it. |
| "Rebooking texts are annoying my clients" | Adjust the frequency. Some clients don't want texts every 4 weeks. Set those specific clients to "low touch" (every 8-12 weeks only). |
| "Walk-ins aren't showing in the system" | Someone needs to enter walk-ins. If there's no receptionist, the stylist needs to tap "Walk-In" before they start. Takes 10 seconds. |

---

## What You Should NOT Do

1. **Don't touch their products or tools.** Stay at the desk.
2. **Don't give opinions on hairstyles, colors, or treatments.** Not your lane.
3. **Don't share one client's info with another.** Client notes (especially color formulas) are proprietary to the stylist.
4. **Don't set prices.** Enter what they tell you.
5. **Don't promise specific revenue increases.** "Most salons fill 15-20% more slots with automated rebooking" is okay. "You'll make $50K more" is not.
6. **Don't photograph clients or their work without permission.** Even for demo purposes.

---

## Glossary

| Word | What It Means |
|------|---------------|
| **Booth renter** | A stylist who rents a chair/station and runs their own business within the salon. They set their own prices, hours, and clients. They're not employees. |
| **Processing time** | Time a chemical treatment (color, perm, keratin) needs to sit. Client is in the chair but stylist can do other things. |
| **Formula** | The specific color mixture used on a client. Example: "6N + 7A, 20 vol, 35 min." This is gold — if a stylist leaves and takes the formulas, clients follow. The system keeps the formulas for the shop. |
| **Rebook rate** | Percentage of clients who book their next appointment before leaving (or within the cycle window). Higher = better. Industry average is about 30%. Target: 60%+. |
| **Walk-in** | A client who shows up without an appointment. Some shops love them (barbershops). Some hate them (high-end salons). |
| **Upsell** | Selling an additional service or product. "Would you like a deep conditioning treatment today?" or "Take home this styling cream." |
| **Back bar** | Professional products used during services (not sold to clients). Shampoo, conditioner, color tubes. These are a cost — track usage. |
