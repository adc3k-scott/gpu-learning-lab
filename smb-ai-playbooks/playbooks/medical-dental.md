# ADC AI Install Playbook — Medical / Dental Office

## Who This Is For
You're an ADC installer. This guide covers medical practices (family medicine, urgent care, specialty clinics) AND dental offices. They're similar enough to share a playbook — the differences are called out where they matter.

---

## What You're Installing
You're setting up an AI system that handles the front-office grind so the clinical staff can focus on patients. When you're done, the office will be able to:

- **Answer every call** — AI picks up when staff is busy, schedules appointments, answers common questions ("Do you take Blue Cross?" "What are your hours?")
- **Patient intake** — new patients fill out forms on their phone BEFORE they arrive. No clipboard. Info goes straight into the system.
- **Insurance verification** — AI checks eligibility and benefits in real-time before the patient sits down. No more "surprise, your insurance doesn't cover that" after the procedure.
- **Smart scheduling** — AI books appointments based on procedure length, provider availability, and room/equipment needs. No double-booking the hygienist.
- **After-visit follow-up** — automated texts: "How are you feeling?" at 24 hours, "Time for your 6-month cleaning" at 5 months, "You have a balance of $85" at 30 days past due.
- **Clinical notes assist** — AI listens during the visit and drafts the note. Doctor/dentist reviews and signs. Cuts charting time from 15 minutes to 2.

**What it replaces:** The front desk person on hold with insurance for 20 minutes. The doctor doing charts at 9 PM. The no-show that could've been prevented with a reminder. The new patient filling out 6 pages of paper forms.

---

## HIPAA — Read This Before You Touch Anything

**HIPAA is federal law. Violations start at $100 per incident and go up to $1.9 million. You can personally be fined.**

### Rules for ADC Installers in Medical/Dental:
1. **NEVER look at patient records.** Not on their screen, not in their files, not anywhere. If you see patient info while setting up, look away. Don't read it, don't photograph it, don't mention it.
2. **All test data must use fake names.** When demoing the system, use "Jane Test" or "John Demo" — NEVER enter a real patient's name, DOB, or insurance info during setup.
3. **The ADC system must have a Business Associate Agreement (BAA) on file.** This should already be in your install folder. Have the office manager or doctor sign it during the install. If it's not in your folder, STOP and call ADC before proceeding.
4. **Wi-Fi must be secured.** If their office WiFi is open (no password), the AI system cannot go on that network. They need a password-protected network. Period.
5. **DGX Spark is the strongest HIPAA play.** Data stays on-site, encrypted, never leaves the building. For any practice handling sensitive records (mental health, substance abuse, STD clinics), recommend Tier 3.

---

## Client Minimum Requirements

### Tier 1: Cloud-Only (HIPAA-Compliant Cloud)
All data encrypted in transit and at rest on ADC's HIPAA-compliant servers.

| Requirement | Minimum | Recommended | Why |
|-------------|---------|-------------|-----|
| **Internet** | 50 Mbps down / 10 Mbps up | 100+ Mbps | Insurance verification + scheduling + intake all running at once. More than a law firm because multiple patients check in simultaneously. |
| **Computer (front desk)** | 8GB RAM, made after 2018 | 16GB RAM, SSD, dual monitors | Front desk runs scheduling + insurance + check-in all day. |
| **Computer (per provider room)** | Laptop or tablet | iPad with keyboard or laptop | For clinical notes assist — in the room during the visit. |
| **Browser** | Chrome or Edge | Chrome | |
| **Monitor (front desk)** | 22"+ | Dual 24" | One for scheduling, one for insurance/check-in. Front desk lives on two screens. |
| **Phone** | iPhone 12+ or Android 10+ | Any modern smartphone | For managers — notifications, approvals, dashboard. |
| **Check-in device** | N/A (patients use their own phones) | iPad on a stand ($400-600) | Kiosk for patients who don't want to use their phone. Some older patients prefer this. |
| **Scanner** | Any | Fujitsu ScanSnap | Insurance cards, referral letters, old records. |

**Cost to client:** $0-600 (iPad kiosk optional) + monthly subscription
**Best for:** Small practices (1-3 providers) with decent existing equipment

### Tier 2: ADC Starter Kit

| Item | Spec | Approx. Cost | Notes |
|------|------|-------------|-------|
| Front desk PC | Intel i5, 16GB RAM, 512GB SSD | $500-700 | Dedicated check-in/scheduling machine |
| Dual monitors | 24" 1080p x2 | $300-400 | Non-negotiable for front desk |
| iPad (check-in kiosk) | iPad 10th gen + stand + case | $450-600 | Patient self-check-in |
| Scanner | Fujitsu ScanSnap iX1600 | $400 | Insurance cards, referrals |
| Wireless keyboard + mouse | | $30-50 | |
| UPS | 600VA | $60-80 | |
| **Total** | | **$1,740-2,230** | |

**Per-provider add-on (for clinical notes):**

| Item | Spec | Approx. Cost |
|------|------|-------------|
| iPad + Apple Pencil (or laptop) | Latest iPad Air or equivalent | $700-900 |
| Bluetooth microphone | Jabra or similar | $100-150 |

### Tier 3: NVIDIA DGX Spark (On-Site HIPAA Fortress)

| Item | Spec | Cost |
|------|------|------|
| **NVIDIA DGX Spark** | GB10 Grace Blackwell, 128GB memory, 1 PFLOPS FP4, 4TB encrypted NVMe, ConnectX-7 | **$4,699** |
| **DGX Spark Bundle** (multi-provider practices) | Two units + connecting cable | **~$9,400** |
| Front desk kit (above) | | $1,740-2,230 |
| Per-provider iPad + mic | | $800-1,050 each |
| **Total (single Spark, 2 providers)** | | **~$8,040-8,930** |

**The pitch to the doctor/dentist:**
> *"Patient records never leave this box. It sits on a shelf in your server closet, it's encrypted, and it's HIPAA-compliant by design — not because we promise to be careful with a cloud server, but because the data physically cannot leave your building. Your malpractice carrier will love this."*

**When to recommend DGX Spark:**
- Mental health, substance abuse, HIV/STD clinic — extra-sensitive records
- Practice has been breached before or is paranoid about data
- Multi-provider practice (3+) where token volume makes cloud expensive
- Rural practice with unreliable internet

---

## The Install — Step by Step

### Step 1: Arrive + BAA First (10 minutes)

1. Introduce yourself: *"Hi, I'm [name] from ADC. I'm here to set up your AI front office system. Before we start anything technical, I need to get one piece of paperwork handled."*
2. **Hand them the BAA (Business Associate Agreement).** Say: *"This is a HIPAA Business Associate Agreement. It says ADC will protect patient data the same way you do. Your compliance officer or attorney should review it, but most practices sign it on the spot — it's standard."*
3. **Do NOT proceed with the install until the BAA is signed.** If they want their lawyer to review it, schedule a return visit. No BAA = no install.
4. Once signed, put the BAA in the ADC folder and take a photo for your records.

### Step 2: Create Workspace (10 minutes)

1. Go to `setup.adc3k.com` → "New Client Workspace"
2. Fill in:
   - Practice name
   - Address
   - Practice type: **Medical — [specialty]** or **Dental — General / Ortho / Perio / etc.**
   - Number of providers
   - Number of front desk staff
   - Main contact email
   - **Check the "HIPAA Compliant" box** — this enables encryption, audit logging, and access controls
3. Click "Create Workspace"

### Step 3: Set Up the Schedule Grid (20 minutes)

This is the backbone. Medical/dental scheduling is more complex than other businesses because every procedure takes a different amount of time and needs different resources.

1. Click **"Schedule"** in the left menu
2. Set up each provider:
   - Name, credentials (MD, DDS, DMD, PA, NP, RDH)
   - Working hours (example: Dr. Smith — Mon/Tue/Thu 8am-5pm, Wed 8am-12pm)
   - Lunch block (block it out — AI won't book during lunch)
3. Set up appointment types with durations:

   **Medical example:**
   | Appointment Type | Duration | Notes |
   |------------------|----------|-------|
   | New patient | 30-45 min | Longer — intake + exam |
   | Follow-up | 15 min | Quick check |
   | Physical / annual wellness | 45-60 min | Longest slot |
   | Sick visit | 15-20 min | Same-day availability |
   | Procedure (in-office) | 30-60 min | Varies by type |

   **Dental example:**
   | Appointment Type | Duration | Notes |
   |------------------|----------|-------|
   | New patient (exam + X-rays) | 60 min | First visit |
   | Cleaning (prophylaxis) | 45-60 min | Hygienist, not dentist |
   | Crown prep | 90 min | Dentist + assistant |
   | Filling | 30-60 min | Depends on surfaces |
   | Emergency / toothache | 30 min | Same-day slot |
   | Whitening | 60-90 min | Cosmetic — no insurance |

4. **Ask the office manager:** *"What's your most common appointment? How long does it actually take — not how long it's scheduled for, but how long it really takes?"* Adjust durations to reality, not the old schedule.

### Step 4: Insurance + Eligibility (15 minutes)

1. Click **"Insurance"** in the left menu
2. Add the insurance plans they accept:
   - **Don't type these in one by one.** Ask: *"Do you have a list of insurances you accept? Maybe on your website or a printed sheet?"*
   - Upload the list — AI will parse it
   - Or select from the common plans in the dropdown (Blue Cross, Aetna, Cigna, UnitedHealthcare, Humana, Medicaid, Medicare, Delta Dental, MetLife Dental, etc.)
3. Set up eligibility verification:
   - Click "Connect Clearinghouse"
   - If they already use a clearinghouse (Availity, Trizetto, Change Healthcare): enter their credentials
   - If they don't: ADC provides one — follow the enrollment prompts (takes 5-10 business days to activate, so START THIS NOW even though it won't work today)
4. **Say to the office manager:** *"Once this is connected, when a patient checks in, the system automatically verifies their insurance and tells you: 'Covered, $30 copay' or 'Not covered — needs prior auth' BEFORE they see the doctor. No more phone calls to the insurance company."*

### Step 5: Patient Intake Forms (15 minutes)

1. Click **"Intake Forms"** in the left menu
2. Load the template for their practice type
3. Standard fields (pre-loaded):
   - Name, DOB, address, phone, email
   - Insurance info (carrier, member ID, group number) — patients can photograph their card
   - Medical/dental history
   - Current medications
   - Allergies
   - HIPAA consent + signature
   - Payment authorization
4. Customize:
   - Add their logo
   - Add/remove questions (some practices want social history, some don't)
   - Add their specific consent forms (surgical consent, cosmetic consent, etc.)
5. Publish the form — generates a link
6. **Two ways patients access it:**
   - **Text before visit:** System texts the link when appointment is booked: *"Your appointment with Dr. Smith is confirmed for Tuesday at 2pm. Please complete your intake form before your visit: [link]"*
   - **In-office kiosk:** iPad at the front desk for walk-ins or patients who didn't complete it at home

### Step 6: AI Phone Setup (15 minutes)

Same as field services playbook, but with medical-specific scripts.

1. Click **"Phone"** → set up AI receptionist
2. Medical greeting: *"Thank you for calling [Practice Name]. I can help you schedule an appointment, refill a prescription, or answer questions about our services. How can I help you?"*
3. Set routing rules:
   - Appointment requests → book directly
   - Prescription refills → route to clinical staff (AI takes the message, doesn't handle controlled substances)
   - "I'm having chest pain / can't breathe / emergency" → *"If this is a medical emergency, please hang up and call 911. I'll stay on the line if you need me to."* → routes to nurse line or provider cell
   - After hours → booking for next available + emergency routing
4. **Important for dental:** Add: *"Are you in pain right now?"* — if yes, flag as emergency/same-day slot

### Step 7: Clinical Notes Assist (15 minutes — Provider Must Be Present)

**This step requires the doctor or dentist.** Don't try to set it up without them.

1. Click **"Clinical Notes"** in the left menu
2. Set up note templates by visit type (SOAP format for medical, periodontal charting for dental)
3. Show the provider:
   - Start an exam → tap "Record" on iPad/laptop
   - AI listens to the visit and transcribes
   - AI drafts the clinical note in their preferred format
   - Provider reviews, edits, and signs
4. **Key line:** *"You talk to the patient like normal. When you're done, the note is already written. You just review it and sign. That's 10-15 minutes of charting you get back per patient."*
5. **For dental:** The AI can also assist with treatment planning — "Patient has #14 MOD amalgam with recurrent decay, recommend crown" — dentist confirms or modifies.

### Step 8: Automated Patient Communication (10 minutes)

1. Click **"Automations"**
2. Turn on:
   - [x] **Appointment confirmation** — immediately after booking
   - [x] **Reminder (48 hours)** — text + option to confirm or reschedule
   - [x] **Reminder (2 hours)** — "See you soon" text
   - [x] **Post-visit follow-up (24 hours)** — "How are you feeling after your visit?"
   - [x] **Recall / preventive care** — "It's time for your annual physical" or "Your 6-month cleaning is due"
   - [x] **Balance reminder (30 days)** — "You have a balance of $X. Pay online: [link]"
   - [x] **Review request (7 days)** — Google review link
3. **No-show recovery:**
   - [x] If patient no-shows → text within 1 hour: *"We missed you today. Would you like to reschedule? Reply YES and we'll find a time."*
   - Show the office manager the no-show stats dashboard — no-shows cost the average practice $150-200 each

### Step 9: Set Up Users + Roles (10 minutes)

| Role | Access | Who |
|------|--------|-----|
| **Provider** (MD, DDS, NP, PA, RDH) | Full clinical notes, schedule, patient records | Doctors, dentists, hygienists, PAs |
| **Front Desk** | Schedule, check-in, insurance, payments | Receptionists, office manager |
| **Billing** | Insurance claims, payments, balance reports | Billing staff (if separate) |
| **Admin/Owner** | Everything + settings + reports + user management | Practice owner/manager |

**HIPAA minimum necessary rule:** Each person only sees what they need. The front desk doesn't need to read clinical notes. The billing person doesn't need to see the chart. Set roles correctly.

---

## Training (30 minutes)

### Front Desk (20 minutes)
Walk through a full patient cycle:
1. New patient calls → AI books appointment → confirmation text goes out
2. Patient gets intake form link → fills it out on phone
3. Day of visit → patient arrives → check in on kiosk → insurance auto-verifies
4. "Covered, $30 copay" pops up on front desk screen
5. Patient sees provider → note is drafted → signed
6. Check out → balance calculated → patient pays or gets statement
7. Next day → follow-up text goes out
8. 6 months later → recall text goes out

**Say:** *"That entire cycle used to be: answer phone, write it down, pull the chart, call insurance, wait on hold, photocopy the card, file the paper form, type the note, print the statement, mail the statement, call to remind them about their next visit. Now the system does it all. You just handle the humans."*

### Provider (10 minutes)
Only show them two things:
1. **Their schedule** — how to see today's patients, what's coming in, any cancellations
2. **Clinical notes** — record, review, sign. That's it.

Providers are busy. Don't show them insurance verification or billing. They don't care and they won't remember. Keep it to what affects their workflow: schedule and notes.

---

## Before You Leave — Final Checklist

- [ ] BAA signed and photographed
- [ ] All providers' schedules are built with correct hours + appointment types
- [ ] Insurance list loaded (at least top 10 plans they accept)
- [ ] Clearinghouse connected OR enrollment started
- [ ] Intake form published and working (test it on your phone)
- [ ] AI phone is live and answering correctly (call it)
- [ ] At least 1 provider has used clinical notes assist (recorded, reviewed, signed a test note)
- [ ] All users can log in with correct roles
- [ ] Automated texts are turned on (confirmation, reminder, follow-up, recall, balance)
- [ ] iPad kiosk is set up at front desk (if applicable)
- [ ] Quick Start card on front desk
- [ ] Office manager has ADC support number
- [ ] You watched the front desk person check in a fake patient without help
- [ ] Service agreement + BAA are in the ADC folder

### Hand-Off Script:
> *"You're live. The phone is answering, intake forms are going out, and your schedule is set up. The biggest thing you'll notice this week is fewer phone calls to insurance — the system checks eligibility automatically."*

> *"Dr./Dr. [name] — your charting is going to be different. Let the AI draft the note, then fix what it gets wrong. First few days you'll spend time correcting it. By week two, it'll know your style and you'll barely touch it."*

> *"I'll check in Thursday. If anything breaks before then, number's on the card."*

---

## After You Leave

### Day 2: Text the Office Manager
> *"Hey [name], how's the first full day? Is the check-in working smoothly? Any hiccups with scheduling?"*

### Day 7: Call (10 minutes)
- How many patients used the digital intake form?
- Is the AI phone catching calls?
- Has the provider used clinical notes assist? If not — why? (Usually it's "I forgot" — offer a 5-minute phone refresher)
- Any insurance verification issues? (Clearinghouse might not be active yet — check status)

### Day 30: Metrics Check
- Intake form completion rate (target: 60%+ of new patients)
- No-show rate (should be dropping — reminders working?)
- Average chart completion time (should be decreasing)
- AI phone calls handled vs. human-answered
- Patient review requests sent vs. reviews received
- Balance collection rate (are patients paying through the text link?)

---

## Troubleshooting

| Problem | What to Do |
|---------|------------|
| "Insurance verification isn't working" | Clearinghouse enrollment takes 5-10 business days. Check status. If enrolled and still failing, check the payer ID — some small insurers need manual setup. |
| "The AI note is wrong" | It learns over time. First week is the roughest. Tell the provider: "Correct it and sign. It learns from your edits." If it's consistently wrong about medical terminology, adjust the specialty setting. |
| "Patients won't use the intake form" | Two fixes: (1) have front desk TEXT the link while the patient is on the phone booking, (2) put the iPad kiosk in the waiting room with a sign: "Check in here." |
| "The AI told a patient medical advice" | **This should never happen.** The system is configured to NOT give medical advice. Check the AI settings — "Medical Advice" should be OFF. If it somehow gave advice, document exactly what happened and call ADC immediately. |
| "We got a HIPAA complaint" | STOP. Do not try to handle this yourself. Call ADC compliance immediately. Document nothing on your personal phone or email. |

---

## What You Should NOT Do

1. **NEVER look at patient records.** Not even for setup. Use fake/test data only.
2. **NEVER give medical or dental advice.** Even if a patient asks you during the install. Say: *"I'm the tech guy — you'll want to ask the doctor/dentist about that."*
3. **NEVER take photos of screens showing patient information.**
4. **NEVER email yourself patient data, login credentials, or anything with PHI (Protected Health Information).**
5. **NEVER skip the BAA.** No BAA = no install. No exceptions.
6. **NEVER set up clinical notes assist without the provider present.** They need to see it, test it, and approve it. You can't decide how their notes should look.
7. **NEVER tell the practice to stop using their existing EHR/EMR.** We integrate alongside it. We don't replace Epic, Athena, eClinicalWorks, Dentrix, Eaglesoft, or whatever they use.

---

## Glossary

| Word | What It Means |
|------|---------------|
| **HIPAA** | Health Insurance Portability and Accountability Act. Federal law that protects patient data. Break it and you get fined. |
| **BAA** | Business Associate Agreement. A contract that says ADC will follow HIPAA. Must be signed before any patient data touches our system. |
| **PHI** | Protected Health Information. Anything that identifies a patient + their health info. Name + diagnosis = PHI. Don't touch it. |
| **EHR/EMR** | Electronic Health Record / Electronic Medical Record. Their existing charting system (Epic, Athena, Dentrix, etc.). We work alongside it, not instead of it. |
| **Clearinghouse** | A middleman that checks insurance eligibility and submits claims. Like a translator between the practice and insurance companies. |
| **Copay** | What the patient owes at the time of visit. Insurance pays the rest. |
| **Prior auth** | Prior authorization. Insurance requires approval BEFORE the procedure. If the AI flags "needs prior auth," the office staff handles it. |
| **SOAP note** | Subjective, Objective, Assessment, Plan. Standard medical note format. The AI drafts it, the provider signs it. |
| **Recall** | A reminder to come back. "You're due for your 6-month cleaning." Not a product recall — dental/medical term. |
| **No-show** | Patient who doesn't show up for their appointment. Costs the practice $150-200 in lost revenue. Our reminders reduce these. |
