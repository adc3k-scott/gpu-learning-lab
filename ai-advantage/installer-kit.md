# AI Advantage — Installer Field Kit

**Everything fits in one backpack + laptop bag.** If it doesn't fit, you're overcomplicating it.

---

## The Laptop (Your Main Tool)

- Secured AI Advantage company laptop — pre-configured, encrypted, no personal use
- NIM deployment toolkit pre-downloaded (don't rely on client WiFi for the big download)
- All vertical sandbox policy files loaded locally
- SSH keys for MARLIE I remote monitoring already configured
- Mission Control dashboard bookmarked and credentials tested (http://marlie1.local:8000)
- Hotspot-capable phone paired (backup internet)

---

## The Backpack

### Always Bring (Every Install)

| Item | Why | Est. Cost |
|------|-----|-----------|
| **Ethernet cables (2x — 6ft and 15ft)** | Client WiFi might be garbage. Hardwire the agent device to their router for install. Leave the short one if needed. | $15 |
| **USB-C hub / dongle** | HDMI out, USB-A ports, Ethernet port. One adapter covers every laptop and device situation. | $35 |
| **USB drive (128GB)** | Pre-loaded with NIM deployment configs, vertical policies, and offline model weights (Nemotron Nano for DGX Spark). Backup if internet is slow or down. | $15 |
| **Phone hotspot** | Company phone or dedicated hotspot. If their internet is down or terrible, you still finish the install. | (company phone) |
| **Power strip (3ft, 3-outlet + USB)** | You need power for your laptop + their device. Their outlets are always in the wrong place or full. Compact travel strip. | $15 |
| **Velcro cable ties (10-pack)** | Clean up the cables you run. Looks professional. Takes 2 minutes. | $5 |
| **Sharpie + labels** | Label the ethernet cable, label the power cable, label the device. When their nephew comes in and starts unplugging stuff, labels save you a service call. | $5 |
| **Business cards + referral cards (10 each)** | Leave cards with the owner. Leave referral cards with every employee who touches the system. | $10 |
| **Microfiber cloth** | Clean the screen after you set up their dashboard view. Small thing, looks professional. | $2 |
| **Notepad + pen** | Write down anything client-specific during discovery/install. Don't rely on your phone for notes in front of a client — looks like you're texting. | $3 |

**Backpack subtotal: ~$105 (one-time, reusable)**

### Mac Mini Installs — Tier 3 (Add These)

| Item | Why | Est. Cost |
|------|-----|-----------|
| **Mac Mini M4 (pre-configured)** | Ship to client ahead of time OR bring it. 7.7" square, under 2 lbs. Pre-load sandbox agent, Nemotron Nano, and vertical configs before arrival. | $1,399-3,199 (client cost) |
| **USB-C to Ethernet adapter** | Mac Mini has one ethernet port. If you need a second connection or their port is USB-C only. | $15 |
| **Extra ethernet cable (3ft)** | Mini to their router/switch. Short and clean. | $5 |
| **HDMI cable (6ft)** | For initial setup — connect to their monitor to verify. After setup, runs headless. | $8 |

**Pre-install prep (do this at the office, not on-site):**
- Install sandbox agent + Nemotron Nano 30B model weights (~15 GB download, don't do this on client WiFi)
- Apply vertical-specific sandbox policy
- Test inference locally — verify the model responds before you drive out
- Configure NIM endpoint to route cloud inference through ADC's MARLIE I infrastructure
- Set up SSH so MARLIE I can monitor remotely
- Verify client appears in Mission Control dashboard
- Total prep time: ~45 minutes

### DGX Spark Installs — Tier 4 (Add These)

| Item | Why | Est. Cost |
|------|-----|-----------|
| **DGX Spark unit** | Ship to client ahead of time OR bring it. Similar size to Mac Mini but heavier. | $4,699 (client cost) |
| **Extra ethernet cable (3ft)** | Spark to their router/switch. Short and clean. | $5 |

### Starter Kit Installs — Tier 2 (Add These)

| Item | Why | Est. Cost |
|------|-----|-----------|
| **Tablet (pre-configured)** | If the kit includes a tablet for the client. Pre-load their vertical app/dashboard before arrival. | (client cost) |
| **Scanner** | For document shops (law, accounting). USB scanner, plug and play. | (client cost) |
| **Travel router** | If their WiFi is genuinely unusable and they need a dedicated network for the agent device. Cheap GL.iNet travel router creates an isolated network in 2 minutes. | $30 |

---

## What You Do NOT Bring

- **No tools.** You're not opening walls, running conduit, or mounting anything. If they need electrical work, they find their own electrician.
- **No crimping kit / cable tester.** You're not making cables. You bring pre-made cables. If their existing network is broken, that's not your job.
- **No monitor / keyboard / mouse.** Use what they have. If they don't have a screen for the agent, that's a Tier 2 upsell (Starter Kit), not something you haul around.
- **No server rack hardware.** DGX Spark sits on a desk or shelf. If they want it rack-mounted, they hire someone for that.

---

## Scope of Work — What You Do and Don't Do

### You DO:
- Set up the AI agent software (sandbox, NIM inference routing, policies)
- Connect the agent device to their EXISTING network (plug in ethernet or connect to WiFi)
- Configure vertical-specific AI workflows
- Train the staff
- Verify remote monitoring is working
- Clean up your cables with velcro ties and labels

### You DO NOT:
- Run cable through walls or ceilings
- Install electrical outlets
- Configure their router, firewall, or network
- Set up their email, POS system, or other business software
- Recommend or refer electricians, IT companies, or other contractors
- Touch their server room / network closet / patch panel
- Promise anything outside the AI agent scope

**If a client needs network or electrical work before you can install:**
> "Your network will need to be ready before we can install. You'll want to get that sorted with your IT person or electrician, and then we'll come back and get your AI agent set up."

That's it. Don't name anyone. Don't suggest anyone. Don't get in the middle. You learned this one the hard way.

---

## Pre-Install Checklist (Before You Leave the Office)

- [ ] Laptop charged, hotspot tested
- [ ] USB drive has latest NIM deployment toolkit + vertical configs
- [ ] Client's vertical playbook reviewed (know what you're installing)
- [ ] Backpack packed (cables, hub, power strip, USB drive, labels, cards)
- [ ] DGX Spark shipped/received if Tier 4 (confirm with client)
- [ ] Client confirmed: working internet, a desk/shelf for the device, and 30 minutes for staff training
- [ ] MARLIE I remote monitoring credentials tested (can you SSH in?)
- [ ] Mission Control dashboard accessible — client workspace visible

---

## Post-Install Kit Check (Before You Drive Home)

- [ ] Nothing left at the client site that's yours (except the ethernet cable you labeled and left)
- [ ] USB drive back in your bag (don't leave configs at client sites)
- [ ] Business cards and referral cards distributed
- [ ] Notes from install written up (submit to AI Advantage by end of day)
- [ ] Next install's playbook pulled up for review tonight
