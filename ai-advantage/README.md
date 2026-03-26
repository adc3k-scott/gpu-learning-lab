# AI Advantage — Master Index

**AI Advantage is a separate business from ADC's neocloud/AI factory operations.** Separate entity. Different customers. This folder is 100% standalone. ADC builds the AI factories. AI Advantage deploys AI agents to the businesses that use them.

## The Business Model
Turnkey AI systems for small and medium businesses. An AI Advantage installer walks into the business, sets everything up in 2-3 hours, trains the staff, and walks out. The business pays a monthly subscription. Recurring revenue.

**What makes this scalable:** The playbooks. Anyone who can follow instructions can do the install — your daughter, your brother Josh, a friend. No computer science degree needed. The playbooks tell them what to click, what to say, and what to do when things go wrong.

---

## 12 Verticals — 80% of Small Businesses in America

| # | Vertical | Playbook File | Install Time | Killer Feature | Workflow Pattern |
|---|----------|---------------|-------------|----------------|-----------------|
| 1 | **Law Firm** | `playbooks/law-firm.md` | ~2 hrs | Document Q&A + drafting | Document shop |
| 2 | **Field Services** (plumber, electrician, HVAC) | `playbooks/field-services.md` | ~2.5-3 hrs | AI phone + dispatch + field quoting | Dispatch shop |
| 3 | **Medical / Dental** | `playbooks/medical-dental.md` | ~2.5 hrs | Insurance verification + clinical notes | Appointment shop |
| 4 | **Restaurant / Bar** | `playbooks/restaurant.md` | ~2.5 hrs | Real-time food cost tracking | Inventory shop |
| 5 | **Auto Shop / Mechanic** | `playbooks/auto-shop.md` | ~2.5 hrs | Photo-to-estimate with customer approval | Inventory + approval shop |
| 6 | **Real Estate** | `playbooks/real-estate.md` | ~2 hrs | Speed-to-lead + instant listing descriptions | Deal shop |
| 7 | **Construction / GC** | `playbooks/construction.md` | ~3 hrs | Change orders + draw schedules + daily logs | Project shop |
| 8 | **Property Management** | `playbooks/property-management.md` | ~2.5 hrs | AI maintenance dispatch + tenant portal | Dispatch + portal shop |
| 9 | **Retail Store** | `playbooks/retail.md` | ~2.5 hrs | Auto-reorder + margin analysis | Inventory shop |
| 10 | **Accounting / CPA** | `playbooks/accounting-cpa.md` | ~2 hrs | Tax document AI intake + deadline tracking | Document shop |
| 11 | **Salon / Barber / Spa** | `playbooks/salon-barber.md` | ~1.5 hrs | Automated rebooking reminders | Appointment shop |
| 12 | **Insurance Agency** | `playbooks/insurance.md` | ~2 hrs | Multi-carrier comparative quoting + renewal tracking | Deal shop |

---

## 5 Workflow Patterns

Every business falls into one of these patterns. Once an installer learns the pattern, they can handle any vertical in that group.

### 1. Document Shops (Law, Accounting)
- **Core:** Upload → AI reads → Q&A → draft → deliver
- **Hardware focus:** Scanner, good monitor, DGX Spark for privacy
- **Key metric:** Documents processed per day

### 2. Dispatch Shops (Field Services, Property Management)
- **Core:** Call comes in → AI triages → dispatch to field → work → invoice → pay
- **Hardware focus:** Office dispatch screen + field phones
- **Key metric:** Response time, jobs completed per day

### 3. Appointment Shops (Medical/Dental, Salon)
- **Core:** Book → remind → check in → serve → follow up → rebook
- **Hardware focus:** Booking kiosk, provider tablet/phone
- **Key metric:** No-show rate, rebook rate

### 4. Inventory Shops (Restaurant, Retail, Auto Shop)
- **Core:** Track stock → predict demand → auto-reorder → sell → track margins
- **Hardware focus:** POS integration, counting tablet, vendor connections
- **Key metric:** Margin %, stock-out rate, sell-through

### 5. Deal Shops (Real Estate, Insurance, Construction)
- **Core:** Lead comes in → qualify → quote/propose → close → follow up
- **Hardware focus:** CRM, carrier/MLS connections, dual monitors
- **Key metric:** Speed-to-lead, conversion rate, retention rate

---

## Self-Hosted on ADC Infrastructure

AI Advantage runs on ADC's own NVL72 hardware at MARLIE I in Lafayette, Louisiana. No third-party cloud. No retail API fees. We generate our own power at $0.027/kWh and run our own compute — raw token cost drops to ~$0.004/M tokens (vs $0.20-$150/M at retail cloud pricing). That margin is the entire business model.

**ADC is its own first customer.** AI Advantage is the reference deployment that proves the token factory works. Every client agent running through our infrastructure validates the neocloud model before we sell tokens to enterprise customers.

### Technology Stack
| Component | What It Does |
|-----------|-------------|
| **NVIDIA NIM microservices** | Containerized model inference — deploy any model as an API endpoint in minutes |
| **Dynamo 1.0** | NVIDIA's open-source inference OS — 7x performance on same Blackwell hardware |
| **Run:AI scheduling** | GPU workload orchestration — each customer gets a project with guaranteed quota |
| **MIG isolation** | Multi-Instance GPU — hardware-level tenant isolation, one GPU serves multiple customers safely |
| **DCGM + Mission Control** | Real-time GPU monitoring, utilization, thermals, error tracking from MARLIE I |

### Security Layer
Every agent we deploy runs inside a sandboxed environment with NVIDIA's security tooling. This is non-negotiable.

| What It Does | Why It Matters |
|-------------|---------------|
| **Sandboxed execution** | Agent can't access anything outside its workspace. Landlock + seccomp + network isolation. |
| **Network policy** | Only approved endpoints allowed. Unknown requests blocked and surfaced to our monitoring team. |
| **Inference routing** | All AI processing routes through ADC's NIM endpoints at MARLIE I — we control cost, model selection, and data flow. |
| **Remote monitoring** | AI Advantage manages every deployment from MARLIE I's Mission Control dashboard. We see blocked requests, approve/deny, push updates. |
| **Vertical-specific policies** | Medical gets HIPAA lockdown. Legal gets privilege lockdown. Restaurant gets basic lockdown. |
| **MIG isolation** | Each customer's inference runs on a hardware-isolated GPU partition. No shared memory, no data leakage between tenants. |

**Key docs:**
- `playbooks/nemoclaw-installer-guide.md` — Full installer training on secure agent deployment
- `client-process.md` — Client-facing 5-step process + advertising copy + FAQ
- `installer-kit.md` — Field kit checklist, scope of work, what you do and don't do

**How inference routing generates revenue:**
```
Client's Agent → Sandbox → ADC NIM Endpoint (MARLIE I NVL72) → Dynamo 1.0 → AI Model → Response
                            ↑
                   We bill per token here.
                   Client pays subscription.
                   Our cost: $0.004/M tokens.
                   We keep the spread (95%+ margin).
```

Every client agent consuming tokens flows through our infrastructure. 96 clients per installer per year x average 50,000+ tokens per day per agent = massive token volume on ADC GPUs. AI Advantage feeds the token factory.

---

## Hardware Tiers (Same Across All Verticals)

| Tier | What It Is | Cost Range | Best For |
|------|-----------|------------|----------|
| **Tier 1: Cloud-Only** | Use their existing stuff + our cloud | $0-500 | Small operations, good equipment already |
| **Tier 2: AI Advantage Starter Kit** | We sell/provide hardware | $1,000-2,700 | Old equipment, dedicated setup |
| **Tier 3: Mac Mini (On-Site AI)** | Apple M4 Pro/Max running local inference | $1,400-3,200 | Privacy-aware, good performance, cost-conscious |
| **Tier 4: NVIDIA DGX Spark** | On-site AI supercomputer | $5,500-10,000+ | Privacy-critical, high volume, HIPAA/legal, offline |

### Mac Mini M4 ($1,399-3,199) — When to Recommend
- Client wants local AI but doesn't need HIPAA/legal-grade compliance
- Good internet but client prefers data stays on-site
- Budget-conscious — wants on-prem without DGX Spark price tag
- Small team (1-5 users) with moderate AI usage
- Runs Nemotron Nano 30B locally at usable speeds
- Fits on a shelf, silent, draws ~40W, client forgets it's there
- NemoClaw sandbox runs the same way — sandboxed, policy-controlled, monitored

**Configs:**
| Model | RAM | Storage | Price | Best For |
|-------|-----|---------|-------|----------|
| M4 Pro (12-core) | 24 GB | 512 GB | ~$1,399 | 1-3 users, single agent, basic verticals |
| M4 Pro (14-core) | 48 GB | 1 TB | ~$2,199 | 3-5 users, runs larger models, room to grow |
| M4 Max | 64 GB | 1 TB | ~$3,199 | 5+ users, concurrent agents, multi-task |

**Trade-offs vs DGX Spark:**
| | Mac Mini M4 | DGX Spark |
|--|-------------|-----------|
| Price | $1,400-3,200 | $4,700-9,400 |
| AI performance | Good (Nano 30B) | Excellent (Super 120B locally) |
| Compliance-grade | No (privacy-aware, not HIPAA-certified) | Yes (full isolation, audit trail) |
| Concurrent agents | 1-2 | 3-5+ |
| Power draw | ~40W | ~200W |
| When to pick | Cost matters, basic privacy | Compliance matters, heavy workload |

### DGX Spark ($4,699) — When to Recommend
- Client handles sensitive data (HIPAA, financial, legal privilege)
- High-volume operation where cloud AI fees add up
- Unreliable internet (rural areas)
- Client is privacy-conscious or has compliance requirements
- Multi-location business wanting centralized on-site AI

### DGX Spark Bundle ($~9,400) — When to Recommend
- Large operation (10+ users, heavy concurrent AI usage)
- Running multiple AI tasks simultaneously (phone + dispatch + quoting + notes)
- Want redundancy (if one unit fails, the other keeps working)

---

## Revenue Model Per Install

| Revenue Stream | Amount | Frequency |
|----------------|--------|-----------|
| **Install fee** | $500-2,000 | One-time |
| **Hardware markup** (Tier 2/3) | 15-25% on equipment | One-time |
| **Monthly subscription** | $200-1,500/mo | Recurring |
| **Annual renewal** | Subscription continues | Recurring |
| **Add-ons** (integrations, extra users) | $50-200/mo each | Recurring |
| **Referral from client** | 10% of first year | One-time per referral |

### Revenue Per Installer Per Month (Conservative)
```
2 installs per week × 4 weeks = 8 installs/month
Average install fee: $750
Average hardware sold: $1,500 × 20% margin = $300
Average monthly subscription: $500

Monthly install revenue: 8 × $750 = $6,000
Monthly hardware margin: 8 × $300 = $2,400
Recurring revenue added: 8 × $500 = $4,000/month (compounds)

Month 1:  $6,000 + $2,400 + $4,000 = $12,400
Month 6:  $6,000 + $2,400 + $24,000 = $32,400
Month 12: $6,000 + $2,400 + $48,000 = $56,400
```

**By month 12, each installer has built $48,000/month in recurring revenue from 96 installed clients.**

---

## Installer Training Path

### Week 1: Learn the System
- Day 1-2: Complete own install (set up a test workspace, go through every step)
- Day 3-4: Shadow a senior installer on 2 real installs
- Day 5: Solo install (simple vertical — salon or law firm) with senior on standby

### Week 2: First Solo Installs
- 3-4 installs with phone support available
- Focus on 1-2 verticals first (learn the pattern, not all 12)

### Week 3+: Full Speed
- 2 installs per week target
- Expand to additional verticals as comfort grows

### Vertical Difficulty (Easiest → Hardest)
1. **Salon/Barber** — simplest, fewest integrations
2. **Law Firm** — document-focused, clean workflow
3. **Real Estate** — straightforward CRM + lead response
4. **Insurance** — carrier connections take time but workflow is clear
5. **Accounting/CPA** — document-heavy, seasonal considerations
6. **Retail** — inventory loading is time-consuming
7. **Field Services** — dual training (office + field), phone setup
8. **Property Management** — many moving parts (tenants + vendors + owners)
9. **Medical/Dental** — HIPAA adds complexity, BAA required
10. **Auto Shop** — WiFi issues + shop floor logistics
11. **Restaurant** — POS integration + recipe costing is detailed
12. **Construction** — most complex, longest discovery phase

**Start new installers on Salon or Law Firm. Build to harder verticals.**

---

## Common Elements (Every Playbook Has These)

Every playbook follows the same structure so installers only learn one format:

1. **Who This Is For** — context for the installer
2. **What You're Installing** — what the client gets (in plain English)
3. **Client Minimum Requirements** — Tier 1/2/3 hardware
4. **The Install** — numbered steps, 2-3 hours
5. **Training** — what to show, what to say
6. **Before You Leave** — checklist
7. **After You Leave** — Day 2 text, Day 7 call, Day 30 metrics
8. **Troubleshooting** — common problems + solutions
9. **What You Should NOT Do** — rules to prevent problems
10. **Glossary** — industry terms explained simply

---

## Pricing by Vertical (DRAFT — Scott to Approve)

Based on value delivered, complexity, and what the market will bear. Three subscription tiers per vertical.

| Vertical | Install Fee | Basic/mo | Pro/mo | Enterprise/mo | Notes |
|----------|-----------|----------|--------|---------------|-------|
| **Salon/Barber** | $500 | $199 | $349 | $499 | Simplest install, lowest touch |
| **Law Firm** | $750 | $499 | $799 | $1,299 | High value per doc, privacy premium |
| **Real Estate** | $750 | $399 | $699 | $999 | Per-agent pricing potential |
| **Insurance** | $750 | $499 | $799 | $1,299 | Multi-carrier = high complexity value |
| **Accounting/CPA** | $750 | $399 | $699 | $1,099 | Seasonal — discount off-season |
| **Retail** | $1,000 | $349 | $599 | $999 | POS integration complexity |
| **Field Services** | $1,000 | $499 | $899 | $1,499 | Dispatch + field = dual value |
| **Property Mgmt** | $1,000 | $599 | $999 | $1,499 | Per-unit pricing potential ($/door) |
| **Medical/Dental** | $1,500 | $699 | $1,199 | $1,999 | HIPAA compliance premium |
| **Auto Shop** | $1,000 | $499 | $799 | $1,299 | DVI = high close value |
| **Restaurant** | $1,000 | $399 | $699 | $1,099 | POS integration + food cost |
| **Construction** | $1,500 | $799 | $1,299 | $1,999 | Most complex, highest value |

### Tier Breakdown
- **Basic**: Core AI features for the vertical. 1-2 users. Email support.
- **Pro**: All features + integrations + AI phone. 5 users. Phone support. Most installs land here.
- **Enterprise**: Unlimited users, multi-location, priority support, custom workflows. DGX Spark recommended.

### Hardware Pricing (On Top of Subscription)
| Hardware | Our Cost (est) | Sale Price | Margin |
|----------|---------------|------------|--------|
| Starter Kit (tablet + router + scanner) | ~$800 | $1,200 | $400 (33%) |
| Mac Mini M4 Pro 24GB | $1,399 | $1,699 | $300 (18%) |
| Mac Mini M4 Pro 48GB | $2,199 | $2,599 | $400 (15%) |
| Mac Mini M4 Max 64GB | $3,199 | $3,699 | $500 (14%) |
| DGX Spark (single) | $4,699 | $5,499 | $800 (15%) |
| DGX Spark Bundle (2-pack) | ~$9,400 | $10,500 | $1,100 (12%) |
| Field Truck Kit (mount + charger + case) | ~$65 | $105 | $40 (38%) |

---

## Dashboard

`dashboard.html` — AI Advantage Install Command Center (ServiceNow-inspired dispatch UI)

Features:
- Team roster with real-time status (available / on-install / training / off)
- 6-column Kanban: Leads > Scheduled > Installing > Training > Active > Follow-Up
- Right panel: metrics, client health, activity feed, top verticals
- Tabs: Dispatch Board, Client Pipeline, Playbooks (quick reference), Revenue
- Revenue tab: per-installer performance, monthly growth chart, YTD totals

---

## Employee Onboarding / New Computer Setup

When a new installer or team member joins, they need to get set up with the AI Advantage tools and repo access.

### Day 1 Setup
1. **Clone the repo:**
   ```bash
   git clone https://github.com/ADC3K/gpu-learning-lab.git
   cd gpu-learning-lab/ai-advantage
   ```
2. **Install Python dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```
3. **Configure environment:** Copy `.env.example` to `.env` and fill in credentials (Scott provides API keys — never share them outside the team).
4. **Test Mission Control access:** Open `http://marlie1.local:8000` (on ADC network) or VPN in. Verify the dashboard loads and you can see agent status.
5. **SSH key for MARLIE I:** Generate a key pair, send the public key to Scott. Once added, verify: `ssh installer@marlie1.local`
6. **Read the playbooks:** Start with `installer-kit.md`, then your first vertical (Salon or Law Firm). Do a practice install on your own test workspace before going to a client.
7. **Join the team channel:** Scott will add you to the AI Advantage installer group for real-time support during your first installs.

---

## What's NOT in These Playbooks (Yet)

- [x] Commission structure → `commission-structure.md`
- [x] Referral program → `referral-program.md`
- [x] Multi-location / franchise → `franchise-playbook.md`
- [x] E-commerce → `playbooks/ecommerce.md`
- [x] Non-profit / church / school → `playbooks/nonprofit-church.md`
- [x] Government / municipal → `playbooks/government-municipal.md`
- [x] Trucking / logistics → `playbooks/trucking-logistics.md`
- [x] Veterinary → `playbooks/veterinary.md`
