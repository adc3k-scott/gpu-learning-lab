# ADC AI Install Playbook — Veterinary Clinic

## Who This Is For
You're an ADC installer. This covers veterinary clinics, animal hospitals, mobile vets, emergency/specialty vet practices, and low-cost spay/neuter clinics. If they treat animals and deal with pet owners, this playbook applies.

---

## What You're Installing
An AI system that keeps the schedule full, automates reminders, and helps the front desk stop drowning in phone calls. When you're done, the clinic will be able to:

- **Online booking 24/7** — pet owners book on their phone anytime. *"Book Bella's annual exam: [link]"* — picks vet, service, date/time. No calling during office hours while the staff is handling a lobby full of anxious pets.
- **AI phone** — answers calls when the front desk is slammed. Books appointments, answers questions (*"Do you see exotic animals?" "How much is a spay?" "Are you accepting new patients?"*), gives directions and hours.
- **Vaccination + wellness reminders** — the #1 revenue driver. *"Bella is due for her rabies booster and annual heartworm test. Book here: [link]"* This single feature pays for the entire system.
- **Pet patient records** — AI-accessible summaries per pet. Species, breed, weight, vaccination history, allergies, medications, chronic conditions, behavioral notes (*"Max is fear-aggressive at the vet — muzzle required, needs exam room 3 with no other animals visible"*).
- **Prescription management** — refill reminders for ongoing medications. *"Luna's Apoquel prescription is due for refill. Approve refill: [link]. Or schedule a recheck if it's been more than 6 months."*
- **Post-visit follow-up** — *"How is Buddy doing after his dental cleaning today? Any concerns? Reply here or call us at [number]."*
- **Review building** — after positive visits: *"Thank you for bringing Cooper in! If you had a good experience, we'd love a review: [Google link]"*

**What it replaces:** The phone ringing 200 times a day while the receptionist is checking in patients, checking out patients, and explaining discharge instructions simultaneously. The dog that's 8 months overdue for vaccines because nobody sent a reminder. The client who went to another vet because they couldn't get through on the phone. The prescription that lapsed because the owner forgot. The 2-star review from someone who waited 45 minutes and nobody apologized.

---

## Client Minimum Requirements

### Tier 1: Cloud-Only

| Requirement | Minimum | Recommended | Why |
|-------------|---------|-------------|-----|
| **Internet** | 25 Mbps | 50+ Mbps | PIMS, booking, phone, all running simultaneously. |
| **Practice management software (PIMS)** | None required | Cornerstone, AVImark, eVetPractice, or Shepherd — we integrate | |
| **Computer** | Existing office PCs/Macs | Modern desktop at front desk + one per exam room | For scheduling, records, POS. |
| **Phone** | Any smartphone | Modern iPhone or Android | For notifications, schedule checks on the go. |
| **Printer** | Any | Label printer + standard laser | Prescription labels, discharge instructions. |

**Cost to client:** $0 + monthly subscription
**Best for:** Solo practitioners or small clinics (1-3 vets) with existing equipment

### Tier 2: ADC Starter Kit

| Item | Spec | Approx. Cost | Notes |
|------|------|-------------|-------|
| iPad (front desk) | iPad + stand + case | $450-600 | Check-in, appointment display |
| Tablet (exam room) | iPad or Android per room | $350-500 each | Records access during exam, client education |
| Card reader | Square or Clover | $0-50 | For payments |
| Label printer | DYMO or Brother | $80-150 | Prescription labels |
| UPS | 600VA | $60-80 | |
| **Total (2-room clinic)** | | **$1,290-1,880** | |

### Tier 3: ADC Clinic Kit

| Item | Spec | Approx. Cost | Notes |
|------|------|-------------|-------|
| Starter kit | | $1,290-1,880 | Everything above |
| Lobby display | 32-43" TV on wall | $200-350 | Pet health tips, wait times, promotions |
| Webcam (telemedicine) | Logitech Brio or similar | $100-200 | For virtual consultations, post-op checks |
| Digital scale (connected) | Wi-Fi or Bluetooth | $150-300 | Auto-logs weight to patient record |
| **Total** | | **$1,740-2,730** | |

### Tier 4: NVIDIA DGX Spark

| Item | Spec | Cost |
|------|------|------|
| **NVIDIA DGX Spark** | GB10 Grace Blackwell, 128GB, 1 PFLOPS FP4, 4TB encrypted NVMe | **$4,699** |
| Clinic kit | | $1,740-2,730 |
| **Total** | | **~$6,440-7,430** |

**When to recommend:**
- Multi-location practice (5+ locations) wanting centralized AI with local data
- Emergency/specialty hospital with high-volume imaging (AI-assisted radiology reads)
- Practice wanting AI-powered dermatology screening (photo analysis of skin conditions)
- Research or teaching hospital needing on-premise processing of large datasets

---

## The Install — Step by Step

### Step 1: Arrive + Understand the Practice (10 minutes)

1. **Timing:** Weekday, ideally during a slow period (early afternoon, Tuesday-Thursday). NOT Saturday morning — that's their busiest time.
2. Walk the clinic:
   - Front desk setup? (How many receptionists? How chaotic is it?)
   - How many exam rooms?
   - How many veterinarians? Vet techs?
   - What species do they see? (Dogs/cats only? Exotics? Large animal? Mixed practice?)
   - Pharmacy/dispensary area? (In-house pharmacy or send to outside?)
   - Surgical suite? Dental station? Imaging?
3. Ask:
   - *"How do clients book right now?"* (Phone, walk-in, online through PIMS)
   - *"What's your biggest bottleneck?"* (Usually: the phone. Always the phone.)
   - *"Do you send vaccination reminders?"* How? (Postcards, emails, nothing?)
   - *"What practice management software are you using?"*
   - *"What's your no-show rate?"* (Vet clinics average 10-15%)

### Step 2: Create Workspace (10 minutes)

1. `setup.adc3k.com` → New Client Workspace
2. Type: Veterinary Clinic / Animal Hospital
3. Number of veterinarians
4. Species seen (small animal, exotic, equine, mixed)
5. Practice management software (Cornerstone, AVImark, eVetPractice, Shepherd, none)

### Step 3: Service Menu + Appointment Types (15 minutes)

1. Click **"Services"**
2. Enter every appointment type:

   | Service | Duration | Price Range | Notes |
   |---------|----------|-------------|-------|
   | Wellness exam (dog/cat) | 20-30 min | $55-75 | Annual checkup, vaccines |
   | Sick visit | 20-30 min | $65-85 | Illness, injury, not feeling right |
   | Puppy/kitten package | 30 min | $150-250 | Series of 3-4 visits, vaccines + deworm |
   | Vaccination only | 15 min | $25-45 per vaccine | Tech appointment, no doctor exam |
   | Spay (dog) | Surgery block | $250-450 | Drop off AM, pick up PM |
   | Neuter (dog) | Surgery block | $200-350 | Drop off AM, pick up PM |
   | Spay/neuter (cat) | Surgery block | $150-300 | Drop off AM, pick up PM |
   | Dental cleaning | Surgery block | $300-800+ | Pre-anesthetic bloodwork required |
   | Nail trim | 10 min | $15-25 | Tech appointment |
   | Anal gland expression | 10 min | $25-40 | Tech appointment |
   | Recheck / suture removal | 15 min | $0-40 | Post-surgical follow-up |
   | Euthanasia | 30-60 min | $100-300 | Block extra time. Private room. |

3. **Surgery scheduling:** Surgeries are different from exams. They need:
   - Drop-off window (usually 7-8 AM)
   - Pre-surgical instructions (*"No food after midnight, water OK until 6 AM"*)
   - Post-op discharge instructions (auto-generated per procedure)
   - Pick-up window (usually 3-5 PM)

4. **Block scheduling:** Most vet clinics don't book appointments every 15 minutes like a human doctor. They block time:
   - Morning: surgeries
   - Midday: appointments
   - Afternoon: appointments + walk-in urgent care
   - Get their actual schedule structure before configuring.

### Step 4: PIMS Integration (15 minutes)

1. Click **"Integrations" → "Practice Management"**
2. Connect their PIMS:

   **Cornerstone (IDEXX):**
   - API connection via IDEXX VetConnect PLUS
   - Sync: patients, clients, appointments, medical records, reminders

   **AVImark (Covetrus):**
   - API connection
   - Sync: patients, clients, appointments, inventory

   **eVetPractice:**
   - Cloud-based — API connection straightforward
   - Sync: all patient and appointment data

   **Shepherd:**
   - Modern cloud PIMS — REST API
   - Full sync: patients, records, billing, inventory

   **No PIMS (paper records or basic system):**
   - Start fresh with our system as the scheduling + reminder engine
   - Patient records build over time from appointment data

3. Verify sync:
   - Pull up a known patient → verify species, breed, weight, vaccine history
   - Check upcoming appointments → verify they match the PIMS calendar
   - Run a reminder report → verify overdue vaccines are flagged

### Step 5: Patient Profiles + Medical History (10 minutes)

1. Click **"Patients"**
2. Verify imported data or set up the structure:
   - **Per client (pet owner):** Name, phone, email, address, multiple pets
   - **Per patient (pet):**
     - Name, species, breed, color, sex (intact/altered), DOB, weight
     - Vaccination history (rabies, DHPP/FVRCP, bordetella, leptospirosis, canine influenza, FeLV)
     - Allergies: *"Max — allergic to cephalosporins, substitute with Clavamox"*
     - Chronic conditions: *"Bella — hypothyroid, on Soloxine 0.5mg BID"*
     - Behavioral notes: *"Rocky — fear-aggressive, needs muzzle for exams, sedate for nail trims"*
     - **Microchip number** (important for ID verification)
3. **Multi-pet households:** Most vet clients have 2+ pets. The system links all pets to one client. Reminders go to the owner, not the pet.
   - *"Both Bella and Max are due for their annual exams. Book them together? [link]"*

### Step 6: AI Phone (10 minutes)

1. Greeting: *"Thanks for calling [Clinic Name]. I can help you book an appointment, check on your pet's records, refill a prescription, or answer questions. How can I help?"*
2. Booking flow: AI asks for pet name, service needed, preferred vet (or any available), date/time preferences
3. Common questions:
   - *"How much is a spay?"* → pulls from service menu with weight-based pricing if applicable
   - *"Do you see rabbits/birds/reptiles?"* → checks species list
   - *"My dog ate chocolate — what do I do?"* → IMMEDIATE escalation: *"If your pet may have ingested something toxic, please call [clinic number] and press 0 for emergency, or call ASPCA Poison Control at 888-426-4435."*
   - *"What vaccines does my puppy need?"* → pulls standard puppy vaccine protocol
   - *"Are you accepting new patients?"* → configured per clinic policy
4. **CRITICAL ROUTING RULES:**
   - Emergency/toxicity → immediate transfer to staff or redirect to emergency hospital
   - Medication questions → transfer to vet tech (AI does NOT give medical advice)
   - Euthanasia inquiries → transfer to staff (this requires a human touch)
   - Pricing complaints → transfer to manager

### Step 7: Vaccination + Wellness Reminders (15 minutes)

This is the money feature. The average vet clinic has 30-40% of patients overdue for vaccines at any time. Each one is a $75-200 visit walking out the door.

1. Click **"Reminders"**
2. Configure vaccine schedules:

   **Dogs:**
   | Vaccine | Initial Series | Booster Frequency |
   |---------|---------------|-------------------|
   | Rabies | 12-16 weeks | 1 year, then every 3 years |
   | DHPP (distemper combo) | 3 doses, 3-4 weeks apart | Every 1-3 years |
   | Bordetella | 1 dose | Every 6-12 months |
   | Leptospirosis | 2 doses, 3-4 weeks apart | Annually |
   | Canine Influenza | 2 doses, 3 weeks apart | Annually |
   | Lyme (if in endemic area) | 2 doses, 3-4 weeks apart | Annually |

   **Cats:**
   | Vaccine | Initial Series | Booster Frequency |
   |---------|---------------|-------------------|
   | Rabies | 12-16 weeks | 1 year, then every 3 years |
   | FVRCP (distemper combo) | 3 doses, 3-4 weeks apart | Every 1-3 years |
   | FeLV (kittens/outdoor cats) | 2 doses, 3-4 weeks apart | Annually |

3. **Reminder sequence:**
   - [x] **30 days before due:** *"Bella's rabies vaccine is due next month. Book her appointment: [link]"*
   - [x] **7 days before due:** *"Bella's rabies booster is due in one week. Available this Thursday at 2 PM? Book: [link]"*
   - [x] **Due date (if not booked):** *"Bella's rabies vaccine is due today. She needs this to stay current. Book now: [link]"*
   - [x] **30 days overdue:** *"Bella is now overdue for her rabies vaccine. Don't wait — book today: [link]"*
   - [x] **90 days overdue (final):** *"It's been 3 months since Bella's rabies vaccine was due. We want to keep her protected. Book: [link] or call us at [number]."*

4. **Wellness reminders (non-vaccine):**
   - [x] Annual heartworm test (dogs): *"Time for Max's annual heartworm test and prevention refill."*
   - [x] Dental check: *"Bella's last dental was over a year ago. Schedule a dental exam: [link]"*
   - [x] Senior wellness (pets 7+): *"Cooper is 8 now — time for his senior bloodwork panel. Catching things early matters."*
   - [x] Flea/tick prevention refill: *"Luna's flea prevention is running low. Refill: [link]"*

5. **Say to the clinic:** *"Every reminder that turns into a visit is $75-200 in revenue. If you have 500 active patients and 30% are overdue, that's 150 appointments waiting to be booked. At $100 average, that's $15,000 sitting on the table."*

### Step 8: Prescription + Refill Management (10 minutes)

1. Click **"Pharmacy"**
2. For clinics with in-house pharmacy:
   - Medication list: name, dosage forms, pricing
   - Refill rules: maximum refills before recheck required (usually 2-3 refills or 6 months, whichever comes first)
3. Refill reminder workflow:
   - Calculate when current prescription runs out based on dispensing date + days' supply
   - 7 days before empty: *"Luna's Apoquel is running low. Approve refill: [reply YES] or schedule a recheck: [link]"*
   - If refill approved + within refill limit → ready for pickup, notify client
   - If recheck required: *"Luna needs a recheck before we can refill her Apoquel. It's been 6 months since her last exam. Book: [link]"*
4. **Controlled substances (if applicable):** Extra rules — no auto-refills, requires vet authorization every time, DEA-compliant logging. The system flags these separately.

### Step 9: Post-Visit Communication + Reviews (10 minutes)

1. Click **"Automations"**
   - [x] **Appointment confirmation:** *"Bella's appointment is confirmed for [date] at [time] with Dr. [name]."*
   - [x] **Surgery pre-op instructions (day before):** *"Reminder: no food for Bella after midnight tonight. Water OK until 6 AM. Drop off between 7-8 AM tomorrow."*
   - [x] **24-hour reminder:** *"See you tomorrow at [time] with [pet name]! Reply C to confirm."*
   - [x] **Post-visit check-in (same day):** *"How is Bella doing after her visit today? Any questions? Reply here or call us."*
   - [x] **Post-surgery check-in (day 1 and day 3):** *"How is Max recovering from surgery? Watch for: [specific signs]. Call immediately if: [emergency signs]. Otherwise, recheck in 10-14 days."*
   - [x] **Review request (3 days after positive visit):** *"We loved seeing Cooper! If you had a good experience, a review means the world to us: [Google link]"*
   - [x] **New client welcome (after first visit):** *"Welcome to the [Clinic] family! Here's what you need to know: [hours, emergency contact, online portal link, booking link]."*
2. **Euthanasia follow-up:**
   - This is SENSITIVE. Configure carefully with the clinic.
   - 3 days after: *"Our hearts are with you during this difficult time. [Pet name] was special, and we were honored to care for them."* (No review request. No rebooking. Just compassion.)
   - Optional: sympathy card mailed (physical, not digital)
   - Flag in system: do NOT send vaccine reminders for deceased pets. This is a common and painful mistake.

---

## Training (15 minutes)

### Front Desk / Receptionist (10 minutes)
1. **Appointment schedule:** How to see the daily schedule, add walk-ins, check in patients
2. **Phone system:** How AI calls work, when calls transfer to them, how to take over
3. **Client communication:** How to send a message to a specific client, check message history
4. **Reminders dashboard:** How to see which reminders went out, who booked, who didn't
5. **Prescription refills:** How to process an AI-approved refill request

### Veterinarians + Vet Techs (5 minutes)
1. **Patient record access:** How to see a pet's full history, allergies, and behavioral notes from the exam room tablet
2. **Notes:** How to add exam notes, update weight, update medications
3. **Reminders:** How the automated vaccine/wellness system works — they set the next-due dates, the system handles the rest

**Key line:** *"Your front desk is answering the same 10 questions 200 times a day. The AI handles those so your team can focus on the animals in front of them and the clients in the lobby. That's the difference between a clinic that feels rushed and one that feels caring."*

---

## Before You Leave — Final Checklist

- [ ] PIMS integration connected and patient data synced (verify 5 random patients)
- [ ] All appointment types configured with correct durations and pricing
- [ ] Online booking link generated and tested (book a test appointment)
- [ ] AI phone live and answering (call it, ask about pricing, ask about species, try to book)
- [ ] Vaccination reminder sequences active (verify an overdue patient triggers correctly)
- [ ] Prescription refill reminders configured
- [ ] Post-visit automations active (confirmation, follow-up, review request)
- [ ] Euthanasia follow-up configured correctly (no vaccine reminders for deceased pets!)
- [ ] Emergency routing tested (say "my dog ate chocolate" — verify it escalates)
- [ ] Booking link placed on: website, Google Business, Facebook, lobby signage
- [ ] Front desk trained on dashboard and phone system
- [ ] At least one vet shown the exam room tablet/record access
- [ ] Quick Start card at front desk
- [ ] Service agreement signed

---

## After You Leave

### Day 2 — Text
*"How's the phone system working? Check the dashboard — you should see how many calls the AI handled yesterday. Any answers that need fixing? Also, look at the overdue vaccine list and see how many reminders went out."*

### Day 7 — Call
- How many calls has the AI handled vs. transferred to front desk? (Target: 50%+ AI-resolved in week 1)
- Any vaccine reminders convert to booked appointments? (Check the conversion rate)
- Are the post-visit follow-ups going out? Any client feedback?
- Any PIMS sync issues? (Records not matching, duplicate entries)
- Review the AI phone transcripts — are the answers accurate for their specific pricing and policies?
- Adjust: service descriptions, pricing, reminder timing, phone routing rules

### Day 30 — Metrics Review
Pull these numbers and compare to pre-install:
- Phone calls handled by AI vs. staff (target: 60%+ AI-resolved)
- Vaccination compliance rate (% of patients current on vaccines — should be climbing)
- Appointments booked from reminders (track revenue directly attributable to automated reminders)
- No-show rate (should decrease with confirmation texts)
- Prescription refill compliance (are pets staying on their meds?)
- Online booking adoption (% of appointments booked online vs. phone)
- Review volume and average rating (should be increasing)
- Front desk phone time reduced (hours/week saved)
- Revenue from reactivated lapsed patients (clients who came back because of reminders)

---

## Troubleshooting

| Problem | What to Do |
|---------|------------|
| "Clients are booking the wrong appointment type" | Simplify the online menu. Pet owners don't know the difference between "comprehensive exam" and "problem-focused visit." Use plain language: "Annual checkup," "My pet is sick," "Vaccines only." |
| "Vaccine reminders are going out for deceased pets" | Check the PIMS sync. The deceased flag must propagate to the AI system. If it's not syncing, manually flag the patient as deceased in our system. This is the #1 complaint — fix it immediately. |
| "The AI told someone their pet would be fine" | The AI should NEVER give medical advice or prognosis. Review the knowledge base and phone configuration. Medical questions always route to staff. If this happened, apologize to the client and tighten the escalation rules. |
| "We're getting booked solid from reminders and can't fit new clients" | Good problem. Adjust reminder volume — send fewer per day, spread them out. Or: this means they need another vet. The data proves it. |
| "Our PIMS doesn't have an API" | Some older PIMS (older versions of Cornerstone, Infinity) don't have modern APIs. Options: upgrade PIMS, use CSV export/import on a schedule, or run our system standalone alongside the PIMS (less integration, but reminders and booking still work). |
| "Clients want to text photos of their pet's issue" | Enable photo receiving in the messaging system. Photos route to a vet tech for triage. Not a diagnosis — just a triage tool. "That looks like it needs an in-person visit" or "Monitor it, and come in if it gets worse." |

---

## What You Should NOT Do

1. **Don't give medical advice.** If a client asks you a health question about their pet during install, say: *"That's a great question for the vet."* You are not a veterinarian.
2. **Don't set vaccine protocols.** Enter what the clinic tells you. Vaccine schedules vary by region, risk factors, and veterinary judgment. Don't question their medical decisions.
3. **Don't handle controlled substances or pharmacy access.** Set up the reminder system — the clinic handles the actual medications.
4. **Don't photograph animals or clients without permission.** Even if the puppy is cute.
5. **Don't share one clinic's pricing with another.** Vet pricing varies enormously — what one clinic charges is their business.
6. **Don't configure the system to diagnose or recommend treatments.** The AI books, reminds, and communicates. It does not practice veterinary medicine.

---

## Glossary

| Word | What It Means |
|------|---------------|
| **PIMS** | Practice Information Management System. The software that runs the clinic — medical records, scheduling, billing, inventory. Cornerstone and AVImark are the big ones. Like an EHR for animals. |
| **DHPP** | Distemper, Hepatitis, Parainfluenza, Parvovirus. The "distemper combo" vaccine for dogs. Sometimes called DA2PP or DAPP. Core vaccine — every dog needs it. |
| **FVRCP** | Feline Viral Rhinotracheitis, Calicivirus, Panleukopenia. The "distemper combo" for cats. Core vaccine. |
| **Bordetella** | "Kennel cough" vaccine. Required by most boarding facilities, groomers, and daycares. Given every 6-12 months. |
| **Heartworm** | A parasitic worm transmitted by mosquitoes. Fatal if untreated. Dogs need monthly prevention and an annual test. This is a major revenue line for vet clinics. |
| **Titer** | A blood test measuring antibody levels. Some owners request titers instead of revaccination. The clinic decides whether to accept titers in lieu of boosters. |
| **Fear Free** | A certification program for low-stress veterinary visits. Clinics with this certification may have specific handling protocols — the system should note these per patient. |
| **Recheck** | A follow-up appointment to assess treatment progress. Often free or reduced cost. These should be tracked separately from billable visits. |
| **Drop-off** | When the owner brings the pet in the morning and picks up later (usually for surgery or dental). The pet stays all day. Requires specific intake and discharge workflows. |
| **Discharge instructions** | Written care instructions given to the owner when the pet goes home after a procedure. AI can auto-generate these per procedure type, customized with the pet's name and specific details. |
