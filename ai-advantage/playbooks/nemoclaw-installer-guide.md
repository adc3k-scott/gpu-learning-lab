# NemoClaw Installer Guide — Secure AI Agent Deployment

**For AI Advantage installers.** This is how we deploy AI agents to client businesses safely. Read this before your first install that uses an always-on agent.

---

## What Is NemoClaw (Plain English)

NemoClaw is a security wrapper around the AI agent we install for clients. Think of it like this:

- The **AI agent** is the worker — it answers phones, drafts documents, tracks inventory, whatever the playbook says.
- **NemoClaw** is the locked room the worker operates in — it can only see what we allow, talk to who we allow, and touch the files we allow.

Without NemoClaw, an AI agent could theoretically access anything on the network, call any website, read any file. That's a liability nightmare, especially for medical, legal, and financial clients. NemoClaw locks it down from the first boot.

---

## Why This Matters for Our Installs

| Problem Without NemoClaw | How NemoClaw Fixes It |
|--------------------------|----------------------|
| Agent could access client files it shouldn't | Filesystem locked — only `/sandbox` and `/tmp` are writable |
| Agent could call random websites | Network policy — only approved endpoints allowed |
| Agent could use any AI model (cost risk) | Inference routing — all AI traffic goes through AI Advantage infrastructure |
| No visibility into what the agent is doing | Monitoring TUI — we see every network request in real time |
| Client worries about data leaving their building | DGX Spark/Mac Mini + NemoClaw = everything stays on-premises |
| HIPAA/legal compliance concerns | Sandboxed execution with audit trail |

---

## How It Works (The 3 Layers)

### Layer 1: The Sandbox
The agent runs inside an isolated container. It cannot see the rest of the computer. It has:
- **Landlock** — controls which files the agent can read/write
- **seccomp** — controls which system operations the agent can perform
- **Network namespace** — the agent has its own network, completely separate from the client's

### Layer 2: Network Policy
Every sandbox has a YAML policy file that lists exactly which websites/services the agent can reach. If the agent tries to contact anything not on the list, it gets blocked and we get notified. We can approve or deny from our monitoring dashboard.

**Example:** A law firm agent might be allowed to reach:
- The AI inference endpoint (through ADC)
- The firm's document management system
- Nothing else

### Layer 3: Inference Routing
When the agent needs to "think" (process a request through the AI model), that request doesn't go directly to the internet. It routes through our infrastructure:

```
Client's Agent → NemoClaw Sandbox → AI Advantage Infrastructure → AI Model → Response back
```

This means:
- We control which AI model is used (cost management)
- We can monitor usage (billing)
- The client's data travels through our secure pipeline
- We can upgrade models without touching the client's system

---

## What You Need to Know for Install Day

### Before You Arrive
- [ ] Know which tier the client is on (Cloud / Starter Kit / Mac Mini / DGX Spark)
- [ ] Have the vertical-specific sandbox policy file ready (from `policies/` folder)
- [ ] Have the client's NVIDIA API key or AI Advantage inference credentials
- [ ] Know the client's approved endpoints (what services does their business use?)

### The Install (NemoClaw-Specific Steps)

These steps happen AFTER the hardware and basic software setup from the vertical playbook.

**Step 1: Install NemoClaw**
```bash
curl -fsSL https://www.nvidia.com/nemoclaw.sh | bash
```
This installs everything. Follow the prompts. It will ask for:
- A sandbox name (use: `clientname-agent`, lowercase, hyphens only)
- The NVIDIA API key

**Step 2: Verify It's Running**
```bash
nemoclaw <sandbox-name> status
```
You should see the sandbox state as "running" and the inference provider as configured.

**Step 3: Apply the Vertical Policy**
Each vertical has a pre-built network policy. Apply it:
```bash
nemoclaw <sandbox-name> policy-add
```
Select the appropriate policy preset for the vertical (medical, legal, field-services, etc.).

**Step 4: Test the Agent**
```bash
nemoclaw <sandbox-name> connect
openclaw agent --agent main --local -m "Hello, this is a test" --session-id test
```
Verify you get a response. If you don't, check the troubleshooting section below.

**Step 5: Open Monitoring**
```bash
openshell term
```
This shows you live network activity. Watch for any blocked requests — these are endpoints the agent tried to reach that aren't in the policy. If they're legitimate (like the client's accounting software), approve them. If they look wrong, deny them.

### Before You Leave
- [ ] Agent is responding to test prompts
- [ ] Monitoring shows no unexpected blocked requests
- [ ] Client knows how to chat with their agent (TUI or Telegram)
- [ ] You've noted any endpoints you approved (report back to AI Advantage)
- [ ] Remote monitoring is configured (AI Advantage MARLIE I can see the sandbox)

---

## Vertical-Specific Policies (What Gets Locked Down)

### Medical / Dental (HIPAA)
- **Filesystem:** Patient data stays in `/sandbox/patient-data/` — never leaves
- **Network:** Only the practice management system + ADC inference
- **Blocked:** All social media, all cloud storage, all email services
- **Special:** Audit logging enabled — every agent action is recorded

### Law Firm (Privilege)
- **Filesystem:** Case files in `/sandbox/case-files/`
- **Network:** Only document management system + ADC inference + legal research databases
- **Blocked:** Everything else
- **Special:** No data leaves the DGX Spark/Mac Mini (recommend Tier 3 or 4 for all law firms)

### Field Services / Construction
- **Filesystem:** Job records, estimates, photos
- **Network:** CRM, dispatch system, ADC inference, mapping services
- **Blocked:** Social media, personal sites
- **Special:** Field phones connect through Telegram bridge — messages flow through the sandbox

### Restaurant / Retail
- **Filesystem:** Inventory, recipes, vendor lists
- **Network:** POS system, supplier ordering platforms, ADC inference
- **Blocked:** Everything else
- **Special:** Lower security tier — less sensitive data, simpler policy

---

## Troubleshooting (Installer Quick Reference)

| Problem | Fix |
|---------|-----|
| "nemoclaw not found" after install | Run `source ~/.bashrc` or open a new terminal |
| Agent not responding | Check `nemoclaw <name> status` — is the sandbox running? |
| Agent can't reach a service the client uses | Open `openshell term`, find the blocked request, approve it |
| "OOM killer" during install on DGX Spark | Add 8 GB swap: `sudo fallocate -l 8G /swapfile && sudo mkswap /swapfile && sudo swapon /swapfile` |
| Sandbox shows "stopped" | Run `nemoclaw onboard` to recreate |
| Port 18789 already in use | Find the process: `lsof -i :18789`, kill it, retry |
| Client's internet is slow | Consider switching to local inference (Nemotron Nano 30B on Mac Mini or DGX Spark) |
| Inference requests timing out | Check `openclaw nemoclaw status` for provider/endpoint, verify API key |

---

## What You Should NOT Do

1. **NEVER approve a network request you don't recognize.** If the agent is trying to reach a website you haven't heard of, deny it and report to AI Advantage.
2. **NEVER give the client access to modify the sandbox policy.** That's AI Advantage's job. They chat with their agent — we manage security.
3. **NEVER skip the monitoring check before leaving.** Watch `openshell term` for at least 5 minutes during testing.
4. **NEVER deploy without a vertical-specific policy.** The default policy is too open for production client use.
5. **NEVER store client credentials on your laptop.** API keys go in the sandbox's `~/.nemoclaw/credentials.json` on the client's hardware, not yours.

---

## Key Terms (If a Client Asks)

| They Say | You Say |
|----------|---------|
| "Is my data safe?" | "Your AI agent runs in an isolated sandbox. It can only access the services we approved together. Nothing else gets through." |
| "Can the AI see my files?" | "Only the files in its workspace. It cannot see your personal files, emails, or anything outside the sandbox." |
| "What if it tries to do something weird?" | "We monitor every network request. If it tries to reach something it shouldn't, it gets blocked automatically and we get notified." |
| "Can you see my data?" | "We monitor the agent's behavior — what it's connecting to, not what it's reading. Your business data stays on your hardware." |
| "What about HIPAA?" | "The sandbox is designed for exactly this. Strict filesystem isolation, no data leaves the device, full audit logging." |
