# Secure Agent Deployment Guide — ADC Self-Hosted Infrastructure

**For AI Advantage installers.** This is how we deploy AI agents to client businesses safely using ADC's own compute at MARLIE I. Read this before your first install that uses an always-on agent.

---

## How It Works (Plain English)

Every AI agent we deploy for a client runs on ADC's own NVL72 GPU hardware at MARLIE I in Lafayette. The client gets a sandboxed agent that connects back to our infrastructure for AI inference. No third-party cloud. No retail API fees.

- The **AI agent** is the worker — it answers phones, drafts documents, tracks inventory, whatever the playbook says.
- The **sandbox** is the locked room the worker operates in — it can only see what we allow, talk to who we allow, and touch the files we allow.
- The **NIM microservice** on MARLIE I is the brain — it processes AI requests on our GPUs, isolated per customer via MIG partitioning.

Without sandboxing, an AI agent could theoretically access anything on the network, call any website, read any file. That's a liability nightmare, especially for medical, legal, and financial clients. Our deployment locks it down from the first boot.

---

## Why This Matters for Our Installs

| Problem Without Sandboxing | How ADC's Stack Fixes It |
|--------------------------|----------------------|
| Agent could access client files it shouldn't | Filesystem locked — only `/sandbox` and `/tmp` are writable |
| Agent could call random websites | Network policy — only approved endpoints allowed |
| Agent could use any AI model (cost risk) | Inference routing — all AI traffic goes through ADC NIM endpoints at MARLIE I |
| No visibility into what the agent is doing | Mission Control dashboard — we see every request, GPU utilization, and cost in real time |
| Client worries about data leaving their building | DGX Spark/Mac Mini = on-prem. Cloud tier = ADC hardware in Louisiana, not a third-party cloud |
| HIPAA/legal compliance concerns | Sandboxed execution with audit trail + MIG hardware isolation per customer |
| Multi-tenant GPU security | Run:AI project quotas + MIG partitioning = hardware-level tenant isolation |

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

### Layer 3: Inference Routing (ADC NIM Endpoints)
When the agent needs to "think" (process a request through the AI model), that request doesn't go to the internet. It routes through ADC's own compute at MARLIE I:

```
Client's Agent → Sandbox → ADC NIM Endpoint (MARLIE I NVL72) → Dynamo 1.0 → AI Model → Response back
```

This means:
- We control which AI model is used (cost management — $0.004/M tokens, not retail pricing)
- We monitor usage via DCGM + Mission Control dashboard (billing, GPU health, latency)
- The client's data stays on American-owned hardware in Louisiana
- We can upgrade models without touching the client's system
- Run:AI schedules workloads across GPUs — each customer gets a guaranteed quota
- MIG isolation ensures one customer's inference never touches another's memory

---

## What You Need to Know for Install Day

### Before You Arrive
- [ ] Know which tier the client is on (Cloud / Starter Kit / Mac Mini / DGX Spark)
- [ ] Have the vertical-specific sandbox policy file ready (from `policies/` folder)
- [ ] Have the client's NVIDIA API key or AI Advantage inference credentials
- [ ] Know the client's approved endpoints (what services does their business use?)

### The Install (Deployment Steps)

These steps happen AFTER the hardware and basic software setup from the vertical playbook.

**Step 1: Create Customer Project in Run:AI**
From your laptop (connected to MARLIE I via VPN or on-network):
```bash
# Create a Run:AI project for the customer with GPU quota
runai project create <clientname> --gpu-quota 0.25 --namespace ai-advantage
```
This gives the customer a guaranteed GPU slice. Scott or a senior installer sets the quota based on the subscription tier.

**Step 2: Deploy NIM Instance**
Create a NIMService custom resource for the customer's inference endpoint:
```bash
kubectl apply -f - <<EOF
apiVersion: nim.nvidia.com/v1
kind: NIMService
metadata:
  name: <clientname>-nim
  namespace: ai-advantage
spec:
  model: nemotron-nano-30b
  replicas: 1
  resources:
    gpu: 1
    migProfile: "1g.10gb"
EOF
```
This deploys a dedicated NIM microservice on MARLIE I hardware with MIG isolation. The client's inference runs on a hardware-partitioned GPU slice.

**Step 3: Install Client-Side Sandbox**
On the client's device (Mac Mini, DGX Spark, or Starter Kit):
```bash
# Run the AI Advantage agent installer from USB drive
./aia-install.sh --client <clientname> --endpoint https://nim.marlie1.adc3k.com/<clientname>
```
This installs the sandboxed agent and points inference to the customer's NIM endpoint on MARLIE I. Follow the prompts for:
- A sandbox name (use: `clientname-agent`, lowercase, hyphens only)
- The AI Advantage inference credentials (from your installer kit, NOT an NVIDIA API key)

**Step 4: Apply the Vertical Policy**
Each vertical has a pre-built network policy. Apply it:
```bash
aia-sandbox <sandbox-name> policy-add
```
Select the appropriate policy preset for the vertical (medical, legal, field-services, etc.).

**Step 5: Test the Agent**
```bash
aia-sandbox <sandbox-name> connect
aia-agent test --message "Hello, this is a test" --session-id test
```
Verify you get a response. If you don't, check the troubleshooting section below.

**Step 6: Verify in Mission Control**
Open Mission Control dashboard (`http://marlie1.local:8000` or via VPN). Confirm:
- Customer project appears in Run:AI with correct GPU quota
- NIM service shows "Running" status
- DCGM metrics show the MIG partition is active
- Client sandbox is sending heartbeats

### Before You Leave
- [ ] Agent is responding to test prompts
- [ ] Monitoring shows no unexpected blocked requests
- [ ] Client knows how to chat with their agent (TUI or Telegram)
- [ ] You've noted any endpoints you approved (report back to AI Advantage)
- [ ] Remote monitoring is configured (MARLIE I Mission Control shows the client's sandbox)
- [ ] NIM service healthy in Run:AI dashboard
- [ ] DCGM metrics flowing for the customer's MIG partition

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
| Agent not responding | Check `aia-sandbox <name> status` — is the sandbox running? Check NIM service status in Run:AI dashboard. |
| Agent can't reach a service the client uses | Check sandbox network policy, find the blocked request, approve it |
| NIM service not starting | `kubectl describe nimservice <clientname>-nim -n ai-advantage` — check events for GPU quota or image pull errors |
| Run:AI project quota exceeded | Contact Scott — customer may need a tier upgrade or quota increase |
| "OOM killer" during install on DGX Spark | Add 8 GB swap: `sudo fallocate -l 8G /swapfile && sudo mkswap /swapfile && sudo swapon /swapfile` |
| Sandbox shows "stopped" | Run `aia-sandbox <name> restart` to recreate |
| Port conflict on client device | Find the process: `lsof -i :<port>`, kill it, retry |
| Client's internet is slow | Consider switching to local inference (Nemotron Nano 30B on Mac Mini or DGX Spark) — sandbox still reports metrics to MARLIE I when connection recovers |
| Inference requests timing out | Check NIM endpoint connectivity: `curl https://nim.marlie1.adc3k.com/<clientname>/health`. If MARLIE I is unreachable, check VPN/network. |
| DCGM metrics not showing | Verify MIG partition is active: `kubectl exec -n ai-advantage <pod> -- nvidia-smi` |
| Can't access Mission Control | Verify VPN connection. Dashboard is at `http://marlie1.local:8000`. Not accessible from public internet. |

---

## What You Should NOT Do

1. **NEVER approve a network request you don't recognize.** If the agent is trying to reach a website you haven't heard of, deny it and report to AI Advantage.
2. **NEVER give the client access to modify the sandbox policy or Run:AI project.** That's AI Advantage's job. They chat with their agent — we manage security and infrastructure.
3. **NEVER skip the Mission Control verification before leaving.** Confirm the client's NIM service, sandbox heartbeat, and DCGM metrics are all green.
4. **NEVER deploy without a vertical-specific policy.** The default policy is too open for production client use.
5. **NEVER store client credentials on your laptop.** Inference credentials go in the sandbox config on the client's hardware, not yours.
6. **NEVER modify Run:AI GPU quotas without Scott's approval.** Quotas are tied to subscription tiers and billing.
7. **NEVER point a client's agent at a third-party cloud endpoint.** All inference goes through ADC's MARLIE I NIM endpoints. That's the whole point.

---

## Key Terms (If a Client Asks)

| They Say | You Say |
|----------|---------|
| "Is my data safe?" | "Your AI agent runs in an isolated sandbox. It can only access the services we approved together. Nothing else gets through. And all AI processing happens on our own hardware in Lafayette — not a third-party cloud." |
| "Can the AI see my files?" | "Only the files in its workspace. It cannot see your personal files, emails, or anything outside the sandbox." |
| "What if it tries to do something weird?" | "We monitor every request from our Mission Control facility in Lafayette. If it tries to reach something it shouldn't, it gets blocked automatically and we get notified." |
| "Can you see my data?" | "We monitor the agent's behavior — what it's connecting to, not what it's reading. Your business data stays on your hardware." |
| "Where does the AI run?" | "On our own NVIDIA GPU hardware at our facility in Lafayette, Louisiana. American-owned, American-operated. We don't use Amazon, Google, or Microsoft cloud. We generate our own power and run our own compute." |
| "What about HIPAA?" | "The sandbox is designed for exactly this. Strict filesystem isolation, hardware-level GPU partitioning per customer, no data leaves the device, full audit logging." |
