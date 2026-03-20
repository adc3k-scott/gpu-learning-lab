# ADC AI Install Playbooks — Master Index

## The Business Model
ADC sells turnkey AI systems to small and medium businesses. An ADC installer walks into the business, sets everything up in 2-3 hours, trains the staff, and walks out. The business pays a monthly subscription. Recurring revenue.

**What makes this scalable:** The playbooks. Anyone who can follow instructions can do the install — your daughter, your brother Josh, a friend. No computer science degree needed. The playbooks tell them what to click, what to say, and what to do when things go wrong.

---

## 12 Verticals — 80% of Small Businesses in America

| # | Vertical | Playbook File | Install Time | Killer Feature | Workflow Pattern |
|---|----------|---------------|-------------|----------------|-----------------|
| 1 | **Law Firm** | `install-playbook-law-firm.md` | ~2 hrs | Document Q&A + drafting | Document shop |
| 2 | **Field Services** (plumber, electrician, HVAC) | `install-playbook-field-services.md` | ~2.5-3 hrs | AI phone + dispatch + field quoting | Dispatch shop |
| 3 | **Medical / Dental** | `install-playbook-medical-dental.md` | ~2.5 hrs | Insurance verification + clinical notes | Appointment shop |
| 4 | **Restaurant / Bar** | `install-playbook-restaurant.md` | ~2.5 hrs | Real-time food cost tracking | Inventory shop |
| 5 | **Auto Shop / Mechanic** | `install-playbook-auto-shop.md` | ~2.5 hrs | Photo-to-estimate with customer approval | Inventory + approval shop |
| 6 | **Real Estate** | `install-playbook-real-estate.md` | ~2 hrs | Speed-to-lead + instant listing descriptions | Deal shop |
| 7 | **Construction / GC** | `install-playbook-construction.md` | ~3 hrs | Change orders + draw schedules + daily logs | Project shop |
| 8 | **Property Management** | `install-playbook-property-management.md` | ~2.5 hrs | AI maintenance dispatch + tenant portal | Dispatch + portal shop |
| 9 | **Retail Store** | `install-playbook-retail.md` | ~2.5 hrs | Auto-reorder + margin analysis | Inventory shop |
| 10 | **Accounting / CPA** | `install-playbook-accounting-cpa.md` | ~2 hrs | Tax document AI intake + deadline tracking | Document shop |
| 11 | **Salon / Barber / Spa** | `install-playbook-salon-barber.md` | ~1.5 hrs | Automated rebooking reminders | Appointment shop |
| 12 | **Insurance Agency** | `install-playbook-insurance.md` | ~2 hrs | Multi-carrier comparative quoting + renewal tracking | Deal shop |

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

## Hardware Tiers (Same Across All Verticals)

| Tier | What It Is | Cost Range | Best For |
|------|-----------|------------|----------|
| **Tier 1: Cloud-Only** | Use their existing stuff + our cloud | $0-500 | Small operations, good equipment already |
| **Tier 2: ADC Starter Kit** | We sell/provide hardware | $1,000-2,700 | Old equipment, dedicated setup |
| **Tier 3: NVIDIA DGX Spark** | On-site AI supercomputer | $5,500-10,000+ | Privacy-critical, high volume, offline capability |

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

## What's NOT in These Playbooks (Yet)

- [ ] Pricing tiers per vertical (need to set subscription rates)
- [ ] Commission structure for installers
- [ ] Referral program details
- [ ] Multi-location / franchise playbook variant
- [ ] E-commerce / online-only business playbook
- [ ] Non-profit / church / school playbook
- [ ] Government / municipal office playbook
- [ ] Trucking / logistics playbook
- [ ] Veterinary clinic (similar to medical but with pet-specific workflows)
