# ADC AI Install Playbook — Trucking / Logistics

## Who This Is For
You're an ADC installer. This covers trucking companies, freight brokers, hotshot haulers, LTL carriers, moving companies, courier services, and logistics/dispatch operations. If they move freight on wheels and deal with drivers, loads, and deadlines, this playbook applies.

---

## What You're Installing
An AI system that dispatches smarter, keeps trucks rolling, and cuts empty miles. When you're done, the company will be able to:

- **AI dispatch** — matches available loads to drivers based on location, equipment, hours remaining, and preferred lanes. *"Driver 14 is dropping in Houston at 2 PM, 6 hours left on his clock. Three loads available within 30 miles heading back toward Dallas — best rate is $2.85/mile on a 280-mile run."* No more manual board-scrolling.
- **Load matching + rate analysis** — pulls loads from DAT, Truckstop, and direct shipper portals. AI filters by equipment type, weight, lane, and rate per mile. Flags loads below your minimum rate. Shows historical lane rates so you don't haul cheap.
- **Route optimization** — considers fuel stops, weigh stations, truck restrictions, weather, and HOS (Hours of Service) windows. *"Take I-10 to I-49 — saves 22 miles and avoids the Houston construction delay. Fuel stop at Pilot in Beaumont, cheapest diesel on route."*
- **ELD compliance monitoring** — real-time HOS tracking. AI alerts before violations happen. *"Driver 7 has 45 minutes left on driving time. Next safe stop: Love's at mile marker 214."* No more CSA points from logbook violations.
- **Customer updates** — proactive tracking. Shippers and receivers get updates without calling. *"Your load is 2 hours from delivery. Estimated arrival: 3:15 PM."*
- **Fuel tracking** — monitors fuel purchases, flags anomalies, finds cheapest fuel on route. *"Driver 3 fueled 80 gallons in Memphis — average for that truck is 55 gallons at that interval. Investigate."*
- **Document management** — BOLs, PODs, rate confirmations, invoices. Scan at delivery, AI matches to load, generates invoice, sends to broker/shipper.

**What it replaces:** The dispatcher juggling 15 drivers on a whiteboard and a cell phone. The $1.50/mile load that got booked because nobody checked the rate. The HOS violation that happened because the driver didn't check his clock. The customer calling 6 times asking "where's my load?" The fuel card getting used at a gas station 200 miles from the truck's route. The invoice that took 2 weeks because the BOL was sitting in a driver's cab.

---

## Client Minimum Requirements

### Tier 1: Cloud-Only

| Requirement | Minimum | Recommended | Why |
|-------------|---------|-------------|-----|
| **Internet (office)** | 25 Mbps | 50+ Mbps | Load boards, dispatch, ELD monitoring. |
| **ELD provider** | Required by law | KeepTruckin/Motive, Samsara, or Omnitracs | AI integrates for HOS + GPS data. |
| **Computer** | Any modern laptop/desktop | Windows 10+ or Mac, dual monitors | Dispatch needs screen real estate. |
| **Phone** | Smartphone per driver | Modern iPhone or Android | Driver app, GPS, document scanning. |
| **Load board** | DAT or Truckstop subscription | DAT Power or Truckstop Pro | For load matching AI. |
| **Fuel cards** | Any fleet fuel card | Comdata, WEX, or EFS | For fuel tracking integration. |

**Cost to client:** $0 + monthly subscription
**Best for:** Small fleets (1-10 trucks) with existing ELD and load board subscriptions

### Tier 2: ADC Starter Kit

| Item | Spec | Approx. Cost | Notes |
|------|------|-------------|-------|
| Dual-monitor setup | 2x 27" monitors + stand | $500-700 | Dispatch needs two screens minimum |
| Document scanner | Portable or desktop duplex | $200-400 | BOLs, PODs, rate confirmations |
| Dash camera (per truck) | Forward + driver-facing | $200-400 each | Insurance discount, incident protection |
| UPS | 1000VA | $100-150 | Dispatch can't go down during a load |
| **Total (5-truck fleet)** | | **$1,800-2,650** | Plus $1,000-2,000 for dash cams |

### Tier 3: ADC Fleet Kit

| Item | Spec | Approx. Cost | Notes |
|------|------|-------------|-------|
| Starter kit | | $1,800-2,650 | Everything above |
| Wall-mounted dispatch board | 55-65" TV | $400-700 | Live fleet map, driver status, load board |
| Tablet (per truck) | Rugged mount tablet | $300-500 each | In-cab document scanning, load details |
| Printer (office) | Laser, duplex | $200-400 | Rate confirmations, BOLs, settlements |
| **Total (10-truck fleet)** | | **$5,400-9,750** | Scales with fleet size |

### Tier 4: NVIDIA DGX Spark

| Item | Spec | Cost |
|------|------|------|
| **NVIDIA DGX Spark** | GB10 Grace Blackwell, 128GB, 1 PFLOPS FP4, 4TB encrypted NVMe | **$4,699** |
| Fleet kit | | $5,400-9,750 |
| **Total** | | **~$10,100-14,450** |

**When to recommend:**
- Large fleet (50+ trucks) needing on-premise route optimization with real-time data
- Company with proprietary lane data they want to keep off cloud servers
- Fleet doing hazmat, oversize, or specialized freight with complex routing rules
- Company wanting predictive maintenance AI using telematics data

---

## The Install — Step by Step

### Step 1: Arrive + Understand the Operation (15 minutes)

1. **Timing:** Weekday, early morning (dispatchers are busiest 6-10 AM). Schedule for an afternoon or arrive before the morning rush to observe.
2. Walk the operation:
   - Dispatch setup? (How many dispatchers? Screens? Boards?)
   - How many trucks? Owner-operators or company drivers? Mix?
   - What do they haul? (Dry van, reefer, flatbed, tanker, hotshot)
   - Geographic lanes? (Regional, OTR, dedicated)
   - Do they broker loads to other carriers?
3. Ask:
   - *"How do you find loads right now?"* (Load boards, direct shippers, brokers, contracts)
   - *"What's your target rate per mile?"* (Dry van: $2.50-3.50/mi, flatbed: $3.00-4.00/mi, reefer: $3.00-4.50/mi — varies by market)
   - *"How many loads do your drivers deadhead per week?"* (Empty miles = lost money)
   - *"What ELD are you running?"*
   - *"How do you handle billing/invoicing?"* (QuickBooks, TruckingOffice, manual)

### Step 2: Create Workspace (10 minutes)

1. `setup.adc3k.com` → New Client Workspace
2. Type: Trucking / Logistics
3. Fleet size (number of trucks)
4. Equipment types (dry van, reefer, flatbed, etc.)
5. Primary lanes (where they run most often)
6. ELD provider

### Step 3: Fleet + Driver Setup (15 minutes)

1. Click **"Fleet"**
2. Enter each truck:
   - Unit number
   - Type (tractor, straight truck, hotshot)
   - Trailer type(s) it pulls
   - Weight capacity
   - Special equipment (chains, tarps, reefer unit, liftgate)
   - Current location (from ELD GPS)
3. Enter each driver:
   - Name, phone, CDL number, CDL class + endorsements (hazmat, tanker, doubles/triples)
   - Assigned truck
   - Home base (where they want to get back to)
   - Preferred lanes (*"runs Texas to Louisiana, doesn't want to go north of I-40"*)
   - HOS status (from ELD integration)
4. **Owner-operators:** Flag separately — they may have their own insurance, authority, and rate preferences.

### Step 4: ELD Integration (10 minutes)

1. Click **"Integrations" → "ELD"**
2. Connect ELD provider:

   **KeepTruckin/Motive:**
   - API key from Motive dashboard
   - Sync: GPS, HOS, DVIR (vehicle inspections), fuel

   **Samsara:**
   - API token from Samsara dashboard
   - Sync: GPS, HOS, driver scores, vehicle diagnostics

   **Omnitracs:**
   - API credentials
   - Sync: GPS, HOS, messaging

3. Verify data flowing:
   - See each driver's current location on the map
   - See each driver's remaining HOS (drive time, on-duty time, cycle)
   - Verify last DVIR status per truck
4. **HOS alerts** — configure:
   - [x] 2-hour warning: *"Driver [name] has 2 hours drive time remaining."*
   - [x] 30-minute warning: *"Driver [name] — 30 minutes! Plan your stop NOW."*
   - [x] Violation risk: *"Driver [name] will violate 14-hour rule if not off duty by [time]."*
   - [x] 34-hour restart available: *"Driver [name] completes 34-hour restart at [time]. Available for dispatch."*

### Step 5: Load Board Integration + AI Matching (20 minutes)

This is the killer feature. AI dispatch that matches loads to drivers.

1. Click **"Load Boards"**
2. Connect:

   **DAT:**
   - API access (requires DAT Power subscription)
   - Configure: equipment type, origin/destination zones, minimum rate

   **Truckstop:**
   - API access (requires Pro subscription)
   - Same configuration

   **Direct shipper portals (if any):**
   - Connect each portal or enter contract rates manually

3. Configure AI matching rules:
   - **Minimum rate per mile:** $X.XX (varies by equipment and lane)
   - **Maximum deadhead:** XX miles (typically 50-100 miles)
   - **Equipment match:** Only show loads that match the driver's equipment
   - **HOS feasibility:** Only show loads the driver can legally complete (AI calculates based on remaining drive time + distance)
   - **Home time:** If a driver needs to be home by Friday, weight loads heading toward home base
   - **Lane preferences:** Respect driver lane preferences when possible
   - **Broker reputation:** Flag brokers with payment history issues

4. **How it works in practice:**
   - Driver drops a load in Houston
   - AI scans all load boards + direct tenders
   - Filters: dry van, within 50 miles of Houston, minimum $2.75/mile, driver has 8+ hours remaining
   - Ranks: by rate/mile, then deadhead distance, then direction toward home
   - Dispatcher sees top 5 options with one-click booking
   - Or: auto-book if within pre-approved parameters (advanced, requires dispatcher approval)

5. **Rate intelligence:**
   - AI shows historical rates for each lane (last 30/60/90 days)
   - *"Houston to Dallas averages $2.90/mile this month, up from $2.65 last month."*
   - Flags loads below market: *"This load is $0.40/mile below the lane average. Negotiate or skip."*

### Step 6: Route Optimization (10 minutes)

1. Click **"Routing"**
2. Configure route preferences:
   - Avoid: low bridges, restricted roads, toll roads (optional), construction zones
   - Prefer: truck stops with driver amenities, cheapest fuel on route
   - HOS-aware: calculate where the driver needs to stop based on remaining drive time
3. Fuel optimization:
   - Connect fuel card API (Comdata, WEX, EFS)
   - AI shows cheapest fuel on route (within X miles of the path)
   - *"Fuel at Pilot in Beaumont ($3.12/gal) instead of the Shell in Lake Charles ($3.38/gal) — saves $18.20 on this fill."*
4. Weather integration:
   - Alerts for route-affecting weather (ice, flooding, high winds for flatbeds)
   - *"Winter storm warning on I-40 west of Amarillo. Recommend delay or alternate route via I-20."*

### Step 7: Customer Communication (10 minutes)

1. Click **"Customer Updates"**
2. Configure automated updates:
   - [x] **Load accepted:** *"Your shipment from [origin] to [destination] has been assigned. Driver [name], Truck #[unit]. Pickup: [date/time]."*
   - [x] **Loaded / picked up:** *"Your shipment has been picked up. BOL #[number]. Estimated delivery: [date/time]."*
   - [x] **In transit (every 4-6 hours or at milestones):** *"Your shipment is in transit. Current location: [city, state]. On schedule."*
   - [x] **Delay alert:** *"Your shipment is running approximately [X] hours behind schedule due to [weather/traffic/mechanical]. Updated ETA: [time]."*
   - [x] **Approaching delivery:** *"Your shipment is 1 hour from delivery. ETA: [time]."*
   - [x] **Delivered:** *"Your shipment has been delivered. POD attached. Thank you for your business."*
3. **Tracking portal:** Give shippers a tracking link. They check status instead of calling dispatch. Eliminates 30-50% of inbound calls.

### Step 8: Document Management + Invoicing (15 minutes)

1. Click **"Documents"**
2. Document workflow:
   - **At pickup:** Driver scans BOL with phone camera → AI reads, matches to load, stores
   - **At delivery:** Driver gets POD signed → scans → AI matches to load
   - **Rate confirmation:** Stored when load is booked
   - **Lumper receipts, scale tickets:** Scanned and attached to load file
3. Invoice generation:
   - Load delivered + POD scanned → AI generates invoice
   - Pulls: rate from rate confirmation, accessorial charges, fuel surcharge
   - Formats per broker/shipper requirements (some want PDF, some want EDI)
   - Sends to broker/shipper within 24 hours of delivery
4. Connect to accounting:
   - QuickBooks: invoice syncs automatically
   - TruckingOffice: load data syncs
   - Or: export CSV for manual entry
5. **Aging tracking:** AI monitors unpaid invoices.
   - 30 days: *"Invoice #[number] to [broker] is 30 days outstanding. Amount: $[X]. Auto-sending reminder."*
   - 45 days: *"Invoice #[number] is 45 days. Escalate to collections?"*
   - Flag brokers with slow-pay patterns

### Step 9: Fuel + Expense Tracking (10 minutes)

1. Click **"Fuel"**
2. Connect fuel card API
3. Configure alerts:
   - Fuel purchase more than 20% above truck average → flag
   - Fuel purchase at location off-route → flag
   - DEF purchases tracked separately
4. **Per-truck cost tracking:**
   - Fuel cost per mile
   - Revenue per mile
   - Net per mile (what the truck actually makes after fuel)
5. **Driver settlements (for owner-operators):**
   - Revenue from loads
   - Minus: fuel, tolls, advances, insurance deductions
   - Settlement generated weekly or per-load

---

## Training (15 minutes)

### Dispatchers (10 minutes)
1. **Fleet map:** Where every driver is, their HOS status, next available time
2. **Load matching:** How to review AI suggestions, book a load, assign to driver
3. **Rate intelligence:** How to check lane rates before accepting a load
4. **HOS alerts:** What each alert means and what action to take
5. **Customer tracking:** How the auto-updates work, how to override if needed

### Drivers (5 minutes — phone call or group text)
1. **App basics:** How to see their assigned load, route, and fuel stops
2. **Document scanning:** How to scan BOL and POD with their phone
3. **Communication:** How to message dispatch through the app (instead of calling)
4. **HOS:** How to check their remaining time in the app

**Key line:** *"Your best dispatcher can handle maybe 10-15 trucks well. This AI doesn't replace them — it makes one dispatcher as effective as three. They stop scrolling load boards and start managing drivers."*

---

## Before You Leave — Final Checklist

- [ ] All trucks and drivers entered with correct equipment and endorsements
- [ ] ELD integration live — GPS and HOS data flowing (verify each driver on the map)
- [ ] Load board(s) connected — AI matching configured with correct rate minimums and deadhead limits
- [ ] Route optimization tested (pick a real upcoming load, show the optimized route + fuel stops)
- [ ] Customer tracking notifications configured and tested (send a test update)
- [ ] Document scanning tested (driver scans a BOL with their phone, verify it matches to the load)
- [ ] Invoice generation tested (generate a sample invoice from a completed load)
- [ ] Fuel card integration live — purchases showing in the system
- [ ] HOS alerts configured and tested (verify a 2-hour warning triggers)
- [ ] Dispatch board display set up (if using wall TV)
- [ ] Dispatchers trained on AI load matching
- [ ] At least 2 drivers trained on phone app
- [ ] Quick Start card at dispatch desk
- [ ] Service agreement signed

---

## After You Leave

### Day 2 — Text
*"How's dispatch going with the new system? Check the load matching — it should have suggestions ready for any drivers dropping today. Let me know if the rate filters need adjusting."*

### Day 7 — Call
- How many loads has the AI matched vs. dispatcher found manually?
- Are the rate suggestions accurate for their lanes?
- Any HOS alerts triggered? Were they helpful or too early/late?
- Are drivers using the document scanning? Any issues?
- Check: deadhead miles this week vs. last week (should be trending down)
- Adjust: rate minimums, deadhead limits, lane preferences, alert timing

### Day 30 — Metrics Review
Pull these numbers and compare to pre-install:
- Revenue per mile (should be up — AI rejects low-rate loads)
- Deadhead percentage (target: under 15% of total miles)
- HOS violations (should be zero — AI catches them before they happen)
- Average invoice turnaround (should be under 48 hours now)
- Customer check calls eliminated (% reduction in "where's my load?" calls)
- Fuel cost per mile (trending down with route optimization + fuel stop selection)
- Loads dispatched per dispatcher per day (should increase 30-50%)
- Driver satisfaction (are they getting better loads and getting home on time?)

---

## Troubleshooting

| Problem | What to Do |
|---------|------------|
| "The AI keeps suggesting loads I don't want" | Tighten the filters. Add lane exclusions (avoid northeast in winter), raise the minimum rate, lower the deadhead radius. The AI learns from what the dispatcher accepts and rejects. |
| "ELD data isn't updating" | Check the API connection. Most ELD providers rate-limit API calls — if data is stale, it's usually a sync interval issue. Set to 5-minute refresh minimum. |
| "Drivers won't scan documents" | Make it dead simple: open app, tap camera, snap photo. If the BOL is crumpled or in a dark cab, the scan fails — tell drivers to flatten it on the dash. If they still won't do it, the dispatcher scans from faxed copies (less ideal but workable). |
| "Rate suggestions seem wrong" | Check the lane data period. If the market shifted this week, historical 90-day data won't reflect it. Shorten to 7-day or 14-day averages during volatile markets. |
| "Customer updates are going out late" | Check the GPS polling interval. If location updates only every 30 minutes, milestone triggers fire late. Increase GPS polling frequency in the ELD settings. |
| "Fuel alerts are flagging legitimate purchases" | Adjust the thresholds. If a truck was running on fumes, an 80-gallon fill is normal. Set the alert threshold per truck based on tank size and typical fill pattern. Give it 2 weeks of data before trusting the anomaly detection. |
| "Owner-operators want different rate minimums than company drivers" | Set rate rules per driver or group. Company drivers might accept $2.50/mile (company covers fuel), but O/Os need $3.00+ (they pay their own fuel). The AI handles this with driver-level rate floors. |

---

## What You Should NOT Do

1. **Don't negotiate rates with brokers or shippers.** You set up the system — the dispatcher makes the deals.
2. **Don't access driver personal information beyond what's needed.** CDL number and endorsements, yes. Medical card details, SSN, home address — no. That's HR data.
3. **Don't promise fuel savings numbers.** "Route optimization typically saves 5-10% on fuel" is fine. "You'll save $2,000/month" is not.
4. **Don't configure the system to auto-book loads without dispatcher approval** unless the owner specifically requests it and understands the risk.
5. **Don't touch ELD settings.** ELD configuration is a compliance matter. If something looks wrong, flag it for the safety manager. FMCSA violations are serious.
6. **Don't give HOS advice.** If a driver asks "can I make it?" — the system shows the math. You don't interpret regulations.

---

## Glossary

| Word | What It Means |
|------|---------------|
| **Deadhead** | Driving empty (no load). Every deadhead mile costs money and makes nothing. The AI's job is to minimize these. |
| **HOS** | Hours of Service. Federal rules limiting how long a driver can drive (11 hours) and be on duty (14 hours) before a mandatory rest. The ELD enforces this electronically. |
| **ELD** | Electronic Logging Device. Federally mandated device that records driving time. Replaced paper logbooks. Connected to the truck's engine — can't be faked. |
| **BOL** | Bill of Lading. The shipping document that describes the freight — what it is, how much, where it's going. The most important document in trucking. |
| **POD** | Proof of Delivery. Signed by the receiver confirming the freight arrived. No POD = no payment. |
| **Rate per mile** | Revenue divided by loaded miles. The primary metric for evaluating a load. $3.00/mile on a 500-mile run = $1,500 gross. |
| **Lane** | A specific origin-to-destination route. "Houston to Dallas" is a lane. Rates vary by lane, season, and market conditions. |
| **DAT** | DAT Freight & Analytics. The largest load board in North America. Where brokers post loads and carriers find freight. |
| **CSA** | Compliance, Safety, Accountability. FMCSA's scoring system for carriers. High CSA scores = more inspections, potential shutdown. HOS violations, crashes, and maintenance issues all add points. |
| **Lumper** | A third-party labor service that unloads freight at warehouses. The fee ($150-400) is usually paid by the driver and reimbursed. Always get a receipt. |
| **Broker** | A middleman who connects shippers with carriers. They don't own trucks — they arrange transportation and take a cut. Most loads on load boards come from brokers. |
| **Accessorial** | Extra charges beyond the base rate — detention, layover, lumper, fuel surcharge, tarp. Always get these in writing on the rate confirmation. |
