# ADC AI Install Playbook — Law Firm

## Who This Is For
You're an ADC installer. You don't need to be a computer person. If you can follow steps and talk to people, you can do this job. This guide tells you exactly what to do, what to say, and what to click — start to finish.

---

## What You're Installing
You're setting up an AI assistant system for a law firm. When you're done, the lawyer and their staff will be able to:
- **Talk to their files** — ask questions about contracts, cases, or documents and get answers in seconds
- **Draft documents** — letters, contracts, motions, demand letters from templates + AI
- **Summarize anything** — drop in a 50-page document, get a 1-page summary
- **Client intake** — new clients fill out a smart form online, AI organizes it into their system
- **Calendar + follow-ups** — AI watches deadlines and reminds staff automatically

**What it replaces:** The paralegal spending 4 hours reading through discovery. The secretary re-typing the same letter 50 times. The lawyer forgetting a filing deadline.

---

## Client Minimum Requirements — What They Need Before You Show Up

Before you schedule an install, the client needs to meet these minimums. If they don't, you'll either need to sell them hardware or walk away.

### Tier 1: Cloud-Only (Cheapest — Uses Their Existing Stuff)
Everything runs on ADC's servers. The client just needs a screen and internet.

| Requirement | Minimum | Recommended | Why |
|-------------|---------|-------------|-----|
| **Internet** | 25 Mbps down / 5 Mbps up | 100 Mbps down / 20 Mbps up | AI responses stream over the internet. Slow internet = slow AI. |
| **Computer** | Any computer made after 2018 | Any computer with 8GB RAM or more | Just running a web browser. Nothing heavy. |
| **Browser** | Chrome, Edge, or Firefox (updated) | Chrome | Do NOT use Internet Explorer. Safari works but Chrome is better. |
| **Monitor** | Any | 22"+ for dispatch/dashboard | They need to see the screen. A tiny laptop works but a real monitor is better. |
| **Storage** | N/A (files stored on ADC servers) | N/A | All documents live in the cloud Vault. Their hard drive doesn't matter. |
| **Phone** | iPhone 12+ or Android 10+ | Any smartphone from the last 3 years | For the mobile app (intake form review, notifications). |
| **Scanner** | Any flatbed or sheet-fed | Fujitsu ScanSnap or similar ($300-500) | For uploading paper files. Phone camera works in a pinch. |

**Cost to client:** $0 hardware (they use what they have) + monthly subscription
**Best for:** Solo attorneys, small firms that already have decent computers

### Tier 2: ADC Starter Kit (We Sell/Provide the Hardware)
For clients with old or unreliable equipment. We bring everything they need.

| Item | Spec | Approx. Cost | Notes |
|------|------|-------------|-------|
| Mini PC | Intel N100 or AMD Ryzen 5, 16GB RAM, 512GB SSD | $300-500 | Runs the browser + local caching. Small, quiet, mounts behind the monitor. |
| Monitor | 24" 1080p | $150-200 | For the front desk / dispatch |
| Keyboard + Mouse | Basic wireless set | $30-50 | |
| Scanner | Fujitsu ScanSnap iX1600 | $400 | Sheet-fed, 40 pages/minute, WiFi direct |
| UPS (battery backup) | 600VA | $60-80 | Keeps the system running during a power flicker. 10 minutes of backup. |
| **Total kit** | | **$940-1,230** | |

**Cost to client:** ~$1,000 hardware + install fee + monthly subscription
**Best for:** Firms with junk computers, firms that want a clean dedicated setup

### Tier 3: NVIDIA DGX Spark (Local AI — The Premium Play)
This is the serious setup. AI runs ON-SITE — their data never leaves the building. For law firms that handle sensitive cases and won't put client data in the cloud.

| Item | Spec | Cost |
|------|------|------|
| **NVIDIA DGX Spark** | GB10 Grace Blackwell superchip, 128GB unified memory, 1 PFLOPS FP4, 4TB NVMe SSD with self-encryption, ConnectX-7 SmartNIC | **$4,699** |
| **DGX Spark Bundle** (optional) | Two DGX Spark units + connecting cable (for larger firms or heavier workloads) | **~$9,400** |
| Monitor | 24" 1080p | $150-200 |
| UPS (battery backup) | 1500VA (the Spark draws more power) | $150-200 |
| Scanner | Fujitsu ScanSnap iX1600 | $400 |
| **Total (single Spark)** | | **~$5,450-5,500** |
| **Total (Spark Bundle)** | | **~$10,150-10,200** |

**What makes DGX Spark different:**
- **Size:** About the size of a Mac Mini (150mm x 150mm x 50.5mm — roughly 6" x 6" x 2"). Sits on a desk or shelf. No server room needed.
- **Privacy:** AI model runs locally. Documents are processed on-site. Nothing goes to the cloud. For attorneys handling privileged communications, trade secrets, or criminal defense — this matters.
- **Speed:** 1 PFLOPS of AI compute. That's a petaflop — a thousand trillion math operations per second. In plain English: it reads a 100-page contract in under 5 seconds.
- **Storage:** 4TB of encrypted SSD. That's roughly 2 million documents. Self-encrypting — if someone steals the box, the data is useless without the key.
- **NemoClaw:** NVIDIA's personal AI operating system runs on this. Privacy router built in — decides what stays local vs. what can go to the cloud (the attorney controls this).
- **Runs NVIDIA Nemotron models** — open-source, no per-token API fees. After the hardware purchase, the AI itself is essentially free to run.

**The pitch to the attorney:**
> *"This is a personal AI supercomputer the size of a book. Your documents never leave this building. No cloud, no subscription AI fees, no one else can see your data. It's like having a paralegal with a photographic memory who works 24/7 and never bills you."*

**When to recommend DGX Spark:**
- Attorney handles high-profile criminal defense, trade secrets, IP litigation, or M&A
- Firm has strict data residency requirements (government contracts, HIPAA-adjacent work)
- Attorney is paranoid about cloud security (some are — don't argue, just sell them the Spark)
- Firm processes 500+ documents per month (the per-token savings pay back the hardware in 6-12 months)

**When NOT to recommend DGX Spark:**
- Solo attorney doing basic family law or traffic tickets — overkill
- Firm has no IT person and no one who can restart a box if it freezes — cloud is simpler
- Budget is tight — start with Tier 1 cloud and upgrade later

### Pre-Install Connectivity Check
Before you schedule the install, have the client run a speed test:

1. Tell them: *"Go to speedtest.net on your office computer and take a screenshot of the results. Text it to me."*
2. If below 25 Mbps down: they need to call their internet provider and upgrade before you come out. Do NOT install on slow internet — the AI will be sluggish and they'll blame us.
3. If they can't figure out speedtest.net: that tells you their tech level. Plan extra training time.

---

## Before You Go — Prep Checklist

### Get From the Office Manager (Phone Call, Day Before)
- [ ] How many people will use the system? (lawyers + paralegals + admin)
- [ ] What kind of law? (personal injury, family, criminal, corporate, real estate — this changes the templates)
- [ ] Do they already use case management software? (Clio, MyCase, PracticePanther, or nothing)
- [ ] Do they have a scanner? (for paper files)
- [ ] WiFi password
- [ ] Name + email of the main contact person (who you'll train)

### Pack Your Install Kit
- [ ] Laptop (yours — for setup, you don't leave this)
- [ ] ADC tablet or the client's computer (where the system will live)
- [ ] USB drive with offline installer (backup if WiFi is slow)
- [ ] Printed "Quick Start" card (laminated — you leave this with them)
- [ ] Printed "What Your AI Can Do" one-pager (you leave this too)
- [ ] Business cards
- [ ] ADC branded folder with service agreement inside

---

## The Install — Step by Step

### Step 1: Arrive + Set Up (15 minutes)

1. Introduce yourself: *"Hi, I'm [name] from ADC. I'm here to set up your AI assistant. It'll take about 2 hours and when I leave, your team will know how to use it."*
2. Ask to use a desk or conference room table
3. Connect to their WiFi
4. Open the ADC Setup Portal on their main computer (the one the office manager or front desk uses most):
   - Open Chrome or Edge (NOT Internet Explorer)
   - Go to: `setup.adc3k.com`
   - Log in with the account credentials from your install ticket

### Step 2: Create Their Workspace (10 minutes)

1. Click **"New Client Workspace"**
2. Fill in:
   - Business name (exactly as they say it — ask for spelling)
   - Address
   - Practice type (dropdown — pick the closest match)
   - Number of users
   - Main contact email
3. Click **"Create Workspace"**
4. The system will generate login credentials for each user — write these down or print them

**If it asks about a "plan tier":** Select whatever is on your install ticket. Don't upgrade or change the plan without calling the office first.

### Step 3: Set Up Document Vault (20 minutes)

This is where all their files live. The AI reads from here.

1. Click **"Document Vault"** in the left menu
2. Create folders to match how they organize their files. Common law firm structure:
   ```
   Active Cases/
   Closed Cases/
   Templates/
   Client Intake/
   Court Filings/
   Correspondence/
   ```
3. Ask the office manager: *"How do y'all organize your files right now?"* — match their system, don't force ours on them
4. If they have digital files already:
   - Click **"Upload"** → drag and drop their folders in
   - This can take a while for big firms. Start the upload and move to the next step while it runs.
5. If they're mostly paper:
   - Set up a **Scan-to-Vault** workflow:
   - Go to Settings → Integrations → Scanner
   - Follow the prompts to connect their scanner (or their phone camera — the app works too)
   - Show them: scan a document → it goes straight to the Vault → AI can read it in about 30 seconds

**Important:** The AI can only answer questions about documents that are IN the Vault. If a file isn't uploaded, the AI doesn't know about it. Make sure the client understands this.

### Step 4: Configure AI Assistant (15 minutes)

1. Click **"AI Assistant"** in the left menu
2. Set the **personality/tone:**
   - For law firms, select **"Professional — Legal"**
   - This makes the AI use legal language and always include disclaimers like "This is not legal advice"
3. Set the **practice area** (same as what you picked during workspace creation)
4. Turn ON these features:
   - [x] Document Q&A (ask questions about uploaded files)
   - [x] Document Drafting (create new documents from templates)
   - [x] Summarization (condense long documents)
   - [x] Deadline Tracking (watches for dates in documents)
   - [x] Client Intake Forms (smart online forms)
5. Turn OFF (unless the install ticket says otherwise):
   - [ ] External Research (searches the internet — some firms don't want this)
   - [ ] Email Integration (needs separate approval from the attorney — privacy rules)

### Step 5: Load Templates (15 minutes)

1. Click **"Templates"** in the left menu
2. The system comes with starter templates for each practice area. Click **"Load [Practice Type] Pack"**
3. Ask the attorney or paralegal: *"Do y'all have any letters or documents you send out over and over? Like demand letters, engagement letters, or standard contracts?"*
4. If yes:
   - Click **"Upload Custom Template"**
   - Upload their existing Word docs or PDFs
   - The AI will learn their style and use it for future drafts
5. **This is the biggest value-add.** Spend time here. The more templates you load, the more useful the system is on Day 1.

### Step 6: Client Intake Form (10 minutes)

1. Click **"Intake Forms"** in the left menu
2. Select the template that matches their practice type
3. Customize:
   - Add their logo (ask for a file, or take a photo of their business card and crop the logo)
   - Add/remove questions based on what they need from new clients
   - Set where completed forms go (usually: the main contact's email + Document Vault)
4. Click **"Publish"** — this generates a link they can put on their website or email to new clients
5. Write the link down on the Quick Start card

### Step 7: Set Up Each User (5 minutes per person)

For each person who will use the system:

1. Click **"Users"** → **"Invite User"**
2. Enter their name and email
3. Set their role:
   - **Attorney** — full access, can approve AI drafts, can delete files
   - **Paralegal** — full access except deleting files and changing settings
   - **Admin/Secretary** — can use AI assistant and intake forms, can't access case files unless given permission
4. Click **"Send Invite"** — they'll get an email with login instructions
5. If they're standing right there, help them log in on their computer/phone right now

---

## Training the Staff (30 minutes)

This is the most important part. The system is only worth something if they actually use it.

### Gather everyone who will use it. Show them these 5 things:

**Demo 1: Ask a Question (2 minutes)**
- Open the AI Assistant
- Upload a sample document (use one of their real documents if possible — a contract or letter)
- Type: *"Summarize this document in 3 bullet points"*
- Show them the result
- Then type: *"What are the key deadlines in this document?"*
- Say: *"See? You can ask it anything about your files. Just type like you're texting."*

**Demo 2: Draft a Document (3 minutes)**
- Click "New Draft"
- Pick a template (like a demand letter)
- Fill in the blanks the AI asks for (client name, incident date, amount, etc.)
- Show the generated draft
- Say: *"It writes the first draft. You review it and change whatever you want. It's a starting point, not a final product. An attorney should always review before sending."*

**Demo 3: Upload + Search (2 minutes)**
- Drag a document into the Vault
- Wait 30 seconds
- Go to AI Assistant and ask a question about what you just uploaded
- Say: *"Anything you put in the Vault, you can search and ask questions about. It reads everything."*

**Demo 4: Client Intake (2 minutes)**
- Open the intake form link on a phone
- Fill it out like you're a new client
- Show where it appears in the system
- Say: *"When a new client fills this out, it comes straight to you. No more paper forms, no more re-typing."*

**Demo 5: Deadlines (1 minute)**
- Show the deadline dashboard
- Say: *"The AI reads your documents and finds dates. If there's a court date, a statute of limitations, a contract renewal — it'll show up here. But always double-check against your own calendar. The AI is a helper, not a replacement for your own tracking."*

### After the Demos, Say This:
> *"This system gets smarter the more you use it. Every document you upload, every question you ask — it learns how your firm works. The first week is the hardest because you're building the habit. After that, you'll wonder how you worked without it."*

> *"If anything goes wrong or you have questions, call this number [point to Quick Start card]. That's ADC support. We're real people, not a robot."*

---

## Before You Leave — Final Checklist

- [ ] All users can log in on their own devices
- [ ] At least 10 documents are in the Vault (enough for the AI to be useful)
- [ ] At least 3 templates are loaded (customized with their info)
- [ ] Intake form is published and the link works
- [ ] Quick Start card is on the front desk (laminated)
- [ ] "What Your AI Can Do" one-pager is posted near the main computer
- [ ] Main contact has ADC support number saved in their phone
- [ ] You've watched each person do at least ONE task on their own (not you doing it for them)
- [ ] Service agreement is signed and in the ADC folder

### Hand-Off Script (Say This Before You Walk Out):
> *"You're all set. Here's your Quick Start card — it has your login, the intake form link, and our support number. The most important thing: just start using it. Upload files, ask questions, draft letters. The more you use it, the better it gets."*

> *"I'll check in with [main contact name] in about a week to see how it's going. If anything breaks or acts weird before then, call the number on the card."*

---

## After You Leave — Follow-Up

### Day 2: Text the Main Contact
> *"Hey [name], it's [your name] from ADC. Just checking in — have y'all had a chance to use the AI assistant today? Let me know if any questions come up."*

### Day 7: Call the Main Contact (5 minutes)
- Ask: "How's it going? Are people using it?"
- Ask: "Any documents you need help uploading?"
- Ask: "Any features you wish it had?"
- Log their answers in your install ticket — this feedback goes back to ADC

### Day 30: Check Usage Dashboard
- Log into `admin.adc3k.com`
- Pull up their workspace
- Check: Are they actually using it? (Look for: documents uploaded, questions asked, drafts created)
- If usage is low: call and offer a 15-minute refresher training
- If usage is high: call and ask for a testimonial or referral

---

## Troubleshooting — Common Problems

| Problem | What to Do |
|---------|------------|
| "It's not answering my question" | Check if the document is in the Vault. If it's not uploaded, the AI can't see it. |
| "The answer is wrong" | AI isn't perfect. Tell them: "It's a starting point — always verify important details yourself." Log the bad answer in your ticket so we can improve it. |
| "I can't log in" | Reset password from the admin portal. If you can't fix it, call ADC support. |
| "It's slow" | Check their internet speed (speedtest.net). Needs at least 10 Mbps. If their internet is fine, it might be a busy time — AI can slow down during peak hours. |
| "We don't want it anymore" | Don't argue. Say: "I understand. Let me connect you with our account team to discuss options." Call ADC immediately. |
| "Can it do [thing you don't know about]?" | Don't guess. Say: "Great question. Let me find out and get back to you today." Then call ADC. |

---

## What You Should NOT Do

1. **Don't promise it replaces a lawyer or paralegal.** It's a tool. Say "assistant" not "replacement."
2. **Don't access their case files yourself.** During install, only use sample or test documents unless they hand you real ones and tell you to upload them.
3. **Don't change their existing software.** We add to what they have. We don't remove Clio, MyCase, or anything else.
4. **Don't give legal advice.** Even if the AI spits out something that sounds like advice, you are not a lawyer. Say: "The AI generated this — your attorney should review it."
5. **Don't leave without watching them do it themselves.** If you do everything for them and leave, they won't use it. Make them drive.
6. **Don't badmouth their current process.** Even if they're using paper files and a fax machine. Say: "This will work alongside what you already do."

---

## Pricing — What the Customer Pays

(Fill in per your install ticket — these are standard tiers)

| Tier | Monthly | What They Get |
|------|---------|---------------|
| Solo | $___/mo | 1 user, 1,000 documents, AI assistant, intake forms |
| Small Firm | $___/mo | Up to 5 users, 10,000 documents, all features |
| Mid Firm | $___/mo | Up to 15 users, unlimited documents, priority support |

**Install fee:** $_____ (one-time, covers your visit + setup + training)

**What's NOT included:** Custom integrations with their existing software (Clio, MyCase, etc.) — that's a separate quote from ADC engineering.

---

## Glossary — Words You Might Hear

| Word | What It Means |
|------|---------------|
| **AI** | Artificial intelligence. The computer reads and writes like a person would. |
| **Vault** | Where all their documents are stored. The AI reads from here. |
| **Template** | A fill-in-the-blank document. The AI fills in the blanks. |
| **Intake form** | An online form new clients fill out. Like a digital version of the clipboard they hand you at the doctor. |
| **Portal** | A website you log into. Their system lives in a portal. |
| **Dashboard** | The main screen that shows everything at a glance. |
| **Upload** | Putting a file into the system. Drag and drop, like attaching a photo to a text message. |
| **LLM** | Large Language Model. The brain behind the AI. You don't need to know how it works, just that it does. If a customer asks, say: "It's the same technology behind ChatGPT, but private and secured for your firm." |
| **Tokens** | How AI measures work. Like how your phone plan measures data in gigabytes. You don't need to explain this to the customer unless they ask about billing. |
| **RAG** | Retrieval Augmented Generation. The AI looks up their documents before answering. This is why it can answer questions about THEIR files, not just general knowledge. Don't use this word with the customer — just say "it searches your files." |
