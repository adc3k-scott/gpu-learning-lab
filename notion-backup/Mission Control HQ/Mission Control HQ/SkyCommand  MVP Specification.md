# SkyCommand — MVP Specification
*Notion backup — 2026-03-28*

SKYCOMMAND MVP
2-PERSON DRONE OPERATIONS
Minimum Viable Product Specification
The Smallest System That Flies Revenue Missions
8-Week Timeline • <$25K Budget • Build Only What You Must
Document Version: 1.0 | February 2026
STARTUP OPERATIONS GUIDE
1. MVP DEFINITION
This document defines the Minimum Viable Product for a two-person drone operations company launching from a single site. The MVP strips the full SkyCommand platform to the absolute smallest functional system that can fly revenue missions legally, safely, and repeatably. Every feature below earns its place by answering one question: does the business stop without this?
1.1 Company Profile
| Parameter | Specification |
| Team size | 2 people: Pilot-in-Command / Operations Lead + Technical Lead / Developer |
| Operating model | Part 107 VLOS commercial operations (inspection, mapping, DFR-ready) |
| Vehicle count | 1 drone + 1 spare (no dock automation at MVP) |
| Operating area | Single site, 5 NM radius, Class G or LAANC-authorized Class C/D/E |
| Daily mission target | 2-4 missions per day |
| Revenue model | Per-mission fees ($500-$2,000/mission) for inspection, mapping, emergency support |
| Budget constraint | < $50K total (hardware + software + first 3 months operating cost) |
| Timeline constraint | Operational in 8 weeks from start |
1.2 The MVP Test
A feature makes the MVP cut if and only if at least one of these is true:
- Legal requirement: FAA mandates it (Part 107 compliance, Remote ID, registration)
- Safety requirement: without it, someone could get hurt (pre-flight checks, weather awareness, emergency procedures)
- Revenue requirement: without it, you cannot complete a paid mission (mission planning, telemetry display, deliverable generation)
- Audit requirement: without it, you cannot prove compliance if FAA asks (flight logs, operator records)
Everything else is a luxury for Week 9 and beyond.
2. SMALLEST FUNCTIONAL SYSTEM
2.1 Hardware (Buy, Not Build)
| Item | Specific Product | Why This One | Cost |
| Drone | DJI Mavic 3 Enterprise | 4/3 CMOS + thermal, 45 min flight, RTK-ready, enterprise SDK, small enough for 2-person ops | $4,500 |
| Spare drone | DJI Mavic 3 Enterprise (identical) | Identical spare eliminates training on second platform; fly same day if primary fails | $4,500 |
| Batteries (6 total) | DJI Mavic 3 Enterprise battery | 3 per aircraft; enough for full day (6-8 flights) | $900 |
| Charging hub | DJI 100W portable charger | Field charging between missions | $80 |
| Controller | DJI RC Pro Enterprise | Built-in screen, DJI Pilot 2 app, reliable link | Included with drone |
| Tablet (backup display) | iPad Air + DJI Fly app | Backup display; client demo screen; post-processing review | $600 |
| Laptop | MacBook Pro M3 or equiv | Development, mission planning, post-processing, admin, client deliverables | $2,000 |
| Hard drives | 2x 2TB portable SSD | Primary + backup for flight data, imagery, deliverables | $200 |
| Safety equipment | Fire-resistant LiPo bag, hi-vis vests (2), cones (4), first aid kit | FAA/client site requirements | $150 |
| Transport | Pelican case for drone gear; vehicle-mountable | Protect equipment in transit | $300 |
Total hardware: ~$13,230. Under budget with margin for insurance and operating costs.
2.2 Software (Use, Not Build)
At MVP, you build only what doesn’t exist. Everything else is off-the-shelf or free.
| Function | Tool | Cost | Why Not Build It |
| Flight planning | DJI Pilot 2 (on controller) | Free (included) | Native to hardware; waypoint planning built in; reliable |
| Airspace / LAANC | Aloft (formerly Kittyhawk) or DroneUp | Free tier or $30/mo | LAANC pre-built; airspace map; TFR/NOTAM overlay; would take months to replicate |
| Weather | Windy.com + local METAR (aviationweather.gov) | Free | Sufficient for VLOS; real-time wind/ceiling/visibility |
| Flight logging | The One Build (see Section 3) | Custom (your dev time) | Nothing on market combines logging + compliance + client deliverables the way you need |
| Client deliverables | DJI Terra (mapping) or third-party (Pix4D, DroneDeploy) | $150-300/mo | Orthomosaic / 3D model generation is commoditized; don’t reinvent |
| Invoicing | Stripe + simple invoice template | 2.9% per transaction | Billing is solved; don’t build a payment system |
| CRM / scheduling | Notion or Google Sheets | Free | 2-person company doesn’t need Salesforce |
| Communication | Phone + email + Signal (encrypted) | Free | Simple is reliable |
| Cloud storage | Google Drive or Backblaze B2 | $6-10/mo | Cheap, reliable, shared access |
| Website | Carrd or simple Next.js landing page | $19/yr or free | One-page site with services, contact, booking link |
Total software: ~$200-$350/month recurring. No enterprise SaaS needed at this stage.
2.3 The One Build: FlightLog MVP
The single piece of custom software you build. Everything else is bought. FlightLog MVP is a lightweight web application that serves as the system of record for your operations. It exists because no off-the-shelf tool combines FAA-compliant logging, pre-flight checklists, and client-facing mission reports in one place.
FlightLog MVP Features (and nothing more)
| Feature | Description | Why MVP |
| Digital pre-flight checklist | Tap-through checklist: weather check, airspace authorization confirmed, Remote ID active, battery >80%, visual inspection pass, crew briefing done | FAA compliance; proves you did due diligence; blocks mission if gate fails |
| Mission log entry | Auto-timestamped record: date, time, location (GPS), pilot, aircraft serial, battery ID, mission type, duration, max altitude, notes | FAA audit trail; insurance requirement; client proof of service |
| Post-flight log | Landing time, flight time, anomalies noted, battery cycles logged, maintenance items flagged | Maintenance tracking; FAA compliance; fleet health baseline |
| Mission report generator | One-click PDF: mission summary, map with flight path, key photos, timestamps, pilot credentials | Client deliverable; professional appearance; saves 30 min per mission |
| Aircraft / battery tracker | Serial numbers, flight hours, battery cycles, next maintenance due | Part 107 continued airworthiness; know when to service/retire |
| Pilot credential tracker | Part 107 cert number, expiry, medical (if applicable), training log | FAA compliance; always know cert status |
FlightLog MVP Tech Stack
| Layer | Choice | Rationale |
| Framework | Next.js 14 (App Router) | SSR for speed; React for UI; API routes for backend; deploys to Vercel free tier |
| Database | Supabase (PostgreSQL) | Free tier: 500 MB, 50K rows, auth built in; enough for years of 2-4 flights/day |
| Auth | Supabase Auth | Built-in; email + password; 2 users is trivial |
| Storage | Supabase Storage or S3 | Flight photos, PDF reports, checklist evidence |
| PDF generation | @react-pdf/renderer or html-pdf | Mission report PDFs generated server-side |
| Hosting | Vercel free tier | Zero ops; auto-deploy from Git; HTTPS included |
| Mobile access | Responsive web (not native app) | Works on phone/tablet browser in the field; no App Store hassle |
Estimated build time: 40-60 hours of development (2 weeks full-time or 4 weeks part-time). One developer can build and ship this.
3. REQUIRED FEATURES ONLY
3.1 Feature Priority Matrix
Every feature is classified into one of three tiers. Tier 1 ships at launch. Tier 2 ships within 30 days. Everything else waits.
| Tier | Feature | Category | Effort | Justification |
| 1: LAUNCH | Part 107 compliance verification | Legal | 2 hrs | Cannot fly without confirming cert, registration, airspace auth |
| 1: LAUNCH | Digital pre-flight checklist | Safety | 8 hrs | FAA expects documented pre-flight; liability protection |
| 1: LAUNCH | Mission log (auto-timestamped) | Audit | 12 hrs | FAA can request logs; insurance requires records |
| 1: LAUNCH | Post-flight log + anomaly notes | Audit | 4 hrs | Complete the record; flag maintenance items |
| 1: LAUNCH | Aircraft and battery tracker | Safety | 6 hrs | Know your fleet status; prevent flying degraded equipment |
| 1: LAUNCH | Weather go/no-go checklist item | Safety | 2 hrs | Document that you checked weather; link to Windy/METAR |
| 1: LAUNCH | Remote ID confirmation gate | Legal | 1 hr | Pre-flight confirms Remote ID broadcasting before takeoff |
| 1: LAUNCH | Basic mission report (PDF) | Revenue | 12 hrs | Client expects professional deliverable; this closes the sale |
| 2: MONTH 1 | Client portal (view reports) | Revenue | 16 hrs | Clients self-serve their reports; reduces email back-and-forth |
| 2: MONTH 1 | Maintenance scheduling alerts | Safety | 8 hrs | Auto-flag when battery hits cycle limit or airframe hits hours threshold |
| 2: MONTH 1 | Financial tracker (revenue/cost per mission) | Business | 8 hrs | Know your unit economics; critical for pricing decisions |
| 2: MONTH 1 | Photo/video gallery per mission | Revenue | 8 hrs | Organized deliverables impress clients; reduces post-processing time |
| 2: MONTH 1 | Dashboard: flights this month, hours, revenue | Business | 6 hrs | At-a-glance business health; motivation; investor-ready metrics |
3.2 What Is NOT in the MVP
This is equally important. These features are valuable but will kill your timeline if you try to include them at launch:
| Feature | Why It Seems Important | Why It Waits | When to Add |
| Automated dock operations | Hands-free launch/recovery | $15K+ hardware; months of integration; 2-person team hand-launches fine | Phase 2 (month 6+, after revenue) |
| Real-time telemetry dashboard | See everything on a big screen | DJI controller already shows telemetry; a dashboard duplicates it at MVP scale | Phase 2 (when you add remote monitoring) |
| ADS-B integration | Know where manned aircraft are | VLOS operations: you can see and hear traffic; ADS-B is for BVLOS | Phase 3 (BVLOS waiver pursuit) |
| AI route optimization | Optimal flight paths | 2-4 missions/day with a human pilot who knows the area doesn’t need AI routing | Phase 3 (when scaling to 10+ daily missions) |
| Safety Supervisor (independent HW) | Defense-in-depth | Single vehicle VLOS with a human pilot IS the safety system; SS is for autonomous/BVLOS | Phase 3 (BVLOS) |
| Multi-vehicle management | Fly multiple drones | You have 2 people and 1 active drone; multi-vehicle is a Phase 2+ problem | Phase 2 (month 6+) |
| Traffic deconfliction | Avoid mid-air collisions | VLOS + see-and-avoid + low altitude; TDE is for dense autonomous operations | Phase 4 |
| Custom mobile app | Native iOS/Android | Responsive web works on phone; App Store review adds weeks; users don’t need it | Phase 2 if user feedback demands it |
| Compliance Engine (OPA rules) | Automated rule checking | 2-person team knows Part 107 by heart; a checklist is the compliance engine at this scale | Phase 2 (when adding operators who aren’t the founder) |
| Kafka / event streaming | Real-time data pipeline | You’re logging 2-4 flights/day; a PostgreSQL INSERT is your data pipeline | Phase 3 (when telemetry volume matters) |
4. BUILD ORDER
4.1 Week-by-Week Timeline
| Week | Focus | Deliverables | Hours (Dev) | Hours (Ops) |
| Week 1 | Business foundation + hardware procurement | LLC formed, Part 107 certs verified, insurance purchased ($1M liability), FAA registration for both aircraft, order all hardware, set up bank account + Stripe, buy domain | 0 | 40 |
| Week 2 | Hardware setup + airspace familiarization | Unbox and configure both drones, firmware update, controller pairing, battery labeling (serial tracking), test flights (3-5 practice flights), LAANC account setup, identify first 3 operating areas, weather source bookmarked | 0 | 40 |
| Week 3 | FlightLog MVP: database + auth + checklist | Supabase project created, database schema (aircraft, batteries, pilots, missions, checklist_items), auth working (2 users), pre-flight checklist UI (mobile-responsive), checklist gates logic | 30 | 10 |
| Week 4 | FlightLog MVP: mission logging + post-flight | Mission creation form (date, location, type, aircraft, battery, notes), auto-timestamp on start/stop, post-flight form (anomalies, battery cycles), mission list view with search/filter | 30 | 10 |
| Week 5 | FlightLog MVP: reports + tracker | PDF mission report generator (summary, map placeholder, timestamps, pilot info), aircraft/battery tracker (hours, cycles, next maintenance), pilot credential tracker, deploy to Vercel | 30 | 10 |
| Week 6 | Operational rehearsal | 5 full dress-rehearsal missions using FlightLog: drive to site, pre-flight checklist, fly mission, post-flight log, generate report, review for gaps. Fix bugs found in field. Refine checklist based on real-world friction | 10 | 30 |
| Week 7 | Client acquisition + soft launch | Website live (services, pricing, booking), first 2-3 client outreach calls, first paid mission (or deeply discounted pilot mission with real client), collect feedback on report quality and process | 5 | 35 |
| Week 8 | Iterate + go live | Fix issues from first missions, refine report template, update checklist, establish daily operating rhythm, go live for full commercial operations | 5 | 35 |
4.2 Day-One Operating Rhythm
By Week 8, your daily operating cadence looks like this:
1. Morning briefing (15 min): check weather (Windy + METAR), review TFRs/NOTAMs (Aloft), confirm today’s missions, battery status
1. Pre-mission (per mission, 20 min): open FlightLog, start pre-flight checklist, confirm LAANC auth (if needed), confirm Remote ID active, visual inspection, brief crew
1. Mission execution (30-90 min): fly mission using Skydio Fleet Manager app, FlightLog running for timestamps
1. Post-mission (15 min): complete post-flight log in FlightLog, note anomalies, swap batteries, download imagery
1. Post-processing (30-60 min): process imagery (Skydio Terra or Pix4D), generate FlightLog mission report PDF, deliver to client
1. End of day (15 min): review all logs, check battery cycles, update maintenance tracker, respond to client inquiries, plan tomorrow
4.3 Critical Path
The single longest dependency chain that determines when you’re operational:
| Item | Depends On | Lead Time | Blocks |
| LLC formation | Decision to start | 1-5 days (state dependent) | Bank account, insurance, contracts |
| Insurance ($1M liability) | LLC formed | 3-7 days | Cannot fly commercially |
| Hardware delivery | Order placed | 3-7 days (Amazon/DJI direct) | Test flights, configuration |
| Part 107 certification | Study + exam | Already held (assumed); if not: 2-4 weeks | Everything |
| FAA drone registration | Aircraft serial number | Immediate (online) | Cannot fly |
| FlightLog MVP build | Developer available | 3 weeks (Weeks 3-5) | Formal logging and reports |
| Operational rehearsal | Hardware + FlightLog ready | 1 week (Week 6) | Client missions |
| First client | Website + outreach | 1-2 weeks (Weeks 7-8) | Revenue |
Critical path: LLC (3 days) -> Insurance (5 days) -> Hardware (5 days) -> Test flights (3 days) -> FlightLog build (15 days) -> Rehearsal (5 days) -> First client (5 days) = ~41 calendar days. Week 8 launch is achievable.
5. WHAT TO DELAY (AND WHEN TO ADD IT)
5.1 Growth Trigger Framework
Don’t add complexity until the business demands it. Each feature below has a specific trigger that tells you it’s time.
| Feature | Trigger | Why This Trigger | Estimated Add Time |
| Second pilot / operator | You’re turning down missions because both founders are booked | Revenue opportunity cost exceeds hiring cost | Hire: 2-4 weeks onboarding |
| Dock automation (DJI Dock 2) | Recurring DFR or site-monitoring contract that requires on-demand launch | Manual launch can’t meet response time SLA | $15K + 4-6 weeks integration |
| Real-time telemetry dashboard | You have a client or contract requiring remote monitoring or multi-person ops | Controller display insufficient for team coordination | 2-3 weeks development |
| Client portal (self-serve reports) | You’re spending >5 hrs/week emailing reports to clients | Email delivery doesn’t scale; clients want on-demand access | 2 weeks development |
| Compliance Engine (automated rules) | You hire a third operator who didn’t build the system | Founders know the rules; new hires need guardrails | 3-4 weeks development |
| AI route optimization | You’re planning 10+ missions/day across multiple sites | Human planning breaks down at volume | 6-8 weeks development |
| BVLOS capability | You have a signed contract requiring BVLOS, or FAA Part 108 is published | BVLOS waiver requires ADS-B, DAA, SS — don’t build speculatively | 6-12 months of hardware + software + waiver |
| Multi-site operations | You have contracts at 3+ locations requiring simultaneous coverage | Single-site architecture doesn’t support remote dock management | 3-6 months to add edge infrastructure |
| SaaS platform (sell to other operators) | Other operators ask to use your FlightLog tool | Product-market fit signal for platform play | 6-12 months to productize |
| Safety Supervisor (independent HW) | BVLOS waiver application or autonomous operations planned | Regulatory requirement for beyond-visual-line-of-sight | $5K hardware + 8 weeks integration |
5.2 Phase Evolution
| Phase | Timeline | Trigger | Team | Revenue Target | Key Additions |
| MVP | Month 1-2 | Start of business | 2 people | $0 (building) | FlightLog, 1 drone, manual everything |
| Revenue | Month 3-6 | First paying clients | 2 people | $5K-15K/mo | Client portal, maintenance alerts, financial tracking |
| Growth | Month 6-12 | Turning down work; repeating contracts | 3-4 people | $15K-40K/mo | Second pilot, dock automation, real-time dashboard, compliance engine |
| Scale | Year 2 | Multi-site demand; BVLOS opportunity | 5-8 people | $40K-100K/mo | Multi-site, ADS-B, Safety Supervisor, AI agents, BVLOS waiver |
| Platform | Year 3 | Other operators want your tools | 8-15 people | $100K-300K/mo | SaaS productization, multi-tenant, API, enterprise sales |
6. BUDGET AND ECONOMICS
6.1 Startup Budget
| Category | Item | Cost | Notes |
| Hardware | 2x DJI Mavic 3 Enterprise + batteries + accessories | $10,200 | Primary + identical spare |
| Hardware | Laptop, tablet, hard drives, safety equipment | $3,250 | Development + field ops |
| Software | DJI Terra or Pix4D (annual) | $2,000 | Post-processing for client deliverables |
| Software | Aloft / airspace tool (annual) | $360 | LAANC + airspace awareness |
| Software | Hosting, storage, domain, misc SaaS | $300 | First year estimate |
| Legal | LLC formation + operating agreement | $500 | State-dependent |
| Insurance | $1M liability drone insurance (annual) | $1,200 | Required for commercial operations |
| Insurance | General liability (annual) | $800 | Client site requirements |
| Marketing | Website, business cards, initial outreach | $500 | Minimal at launch |
| Operating cash | 3 months runway (fuel, maintenance, misc) | $3,000 | Buffer for slow start |
Total startup investment: ~$22,310. Well under $50K budget with $27,690 in reserve.
6.2 Unit Economics Per Mission
| Metric | Inspection Mission | Mapping Mission | DFR / Emergency |
| Revenue per mission | $800 | $1,500 | $500/dispatch + $200/hr |
| Direct costs (battery wear, travel, processing) | $50 | $100 | $30 |
| Time investment (travel + fly + post-process) | 3 hours | 5 hours | 1.5 hours |
| Effective hourly rate | $250/hr | $280/hr | $313/hr |
| Breakeven missions per month (cover $3K/mo fixed costs) | 4 missions | 2 missions | 6 dispatches |
Path to profitability: At 3 missions/week average ($900 avg revenue), monthly revenue = $10,800. After fixed costs ($3,000/mo), net margin = $7,800/month. Two-person split: $3,900/person/month from Week 8 onward, scaling with volume.
6.3 Investment Priorities After Revenue
Once revenue is flowing, reinvest in this order:
1. Month 3: Client portal ($0 dev cost, just your time) — reduces admin overhead, impresses clients
1. Month 4: Better post-processing software if needed — directly improves deliverable quality
1. Month 5: Marketing spend ($500-1,000/mo) — SEO, local networking, LinkedIn content, conference attendance
1. Month 6: Third team member (contractor pilot) — unblocks capacity constraint
1. Month 9: Dock automation ($15K) — enables recurring automated site monitoring contracts
1. Month 12: Real-time dashboard + compliance engine — enables team operations without founder supervision
END OF DOCUMENT
SkyCommand MVP — 2-Person Drone Operations Startup Guide v1.0