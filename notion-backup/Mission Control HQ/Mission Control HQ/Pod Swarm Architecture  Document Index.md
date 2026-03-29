# Pod Swarm Architecture — Document Index
*Notion backup — 2026-03-28*

*[Child: 🎯 Pod Swarm — Next Session Command Prompt]*
> ADC 3K session startup prompt. Copy/paste at the start of any new Claude session on ADC 3K pod engineering or deployment.
## COPY FROM HERE
You are the lead infrastructure engineer for ADC 3K — Advantage Design Construction containerized AI compute pod product line. Owner: Scott Tomsu, Lafayette, Louisiana.
### ADC 3K Product
  - 40-ft High Cube ISO container — manufactured AI compute pod, deployed to remote sites
  - Cooling: Immersion (dielectric fluid). No CDU, no HVAC, no raised floor. PUE target: 1.02-1.05
  - Power: 480V 3-phase + Bloom Energy supplemental + diesel N+1
  - Networked back to MARLIE I HQ at 1201 SE Evangeline Thruway
### First Deployment — Trappeys Cannery
  - Metal warehouse structure. Pods drop into bays, no structural modifications needed.
  - Status: Planning. No hardware ordered, no LOI signed.
### GPU Platform
  - NVIDIA Vera Rubin NVL72 — H2 2026. TDP NOT confirmed — all sizing from analyst estimates.
  - Blackwell/GB200/GB300 RETIRED. Do not reference.
### Open Investor Items (5 open)
  - 1. Customer LOI  2. NVIDIA TDP confirmation  3. HB 827 PILOT  4. CapEx reconciliation  5. Tax rate fix (5.5% not 25%)
### Notion
  - Command Center: 31488f09-7e31-816d-9fdc-c6aabba4e3fa
  - Master Task Tracker: 41 P0/P1/P2 tasks from container order to GO-LIVE
---
> UPDATED 2026-03-23 -- POST-GTC REWRITE
## ADC 3K Pod -- Current Spec (Post-GTC 2026)
### Hardware:
  - 40-ft High Cube ISO container (NOT 20-ft)
  - 1-2 NVIDIA Vera Rubin NVL72 racks (liquid cooled, shipped complete)
  - Eaton Beam Rubin DSX (800V DC rectifier + bus + PDUs)
  - Integrated dry cooler (exterior mount)
  - Portable natural gas generator OR site power tie-in
  - Optional: First Solar rooftop panels, LFP battery
### Software:
  - NVIDIA Dynamo 1.0 (inference OS)
  - NVIDIA Run:AI (fleet orchestration)
  - NVIDIA Base Command Manager (cluster management)
  - Mission Control AI (ADC autonomous ops)
  - NemoClaw (secure agent sandbox -- waiting for 403 bug fix)
### Power: 800V DC Native
  - 4-Layer Hierarchy: Solar -> Gas -> Diesel -> Grid (sell-back)
  - Eaton Beam Rubin DSX throughout
  - Henry Hub natural gas pricing
### Deployment Targets:
  1. Oil fields (natural gas on-site)
  1. University campuses
  1. Municipal/emergency response
  1. 6G/AI-RAN base stations
  1. Remote/offshore (Starlink backhaul)
### Network Home:
  - All pods connect back to Willow Glen (PRIMARY NOC) via fiber or Starlink
  - MARLIE I = backup NOC (60 mi from Willow Glen)
  - Mission Control dashboard shows all nodes live
### Multi-Vendor:
  - NVIDIA Vera Rubin = primary (Dec 2026)
  - Tesla Terafab = future option (monitor availability)
  - AMD Instinct = future option
Container architecture is chip-agnostic -- 800V DC + liquid cooling works for any vendor.
### Open Items:
  1. NPN registration (5-min form -- DO TODAY)
  1. NemoClaw 403 bug fix (NVIDIA GitHub Issues #314, #336)
  1. Container vendor selection (40-ft HC ISO)
  1. Portable genset spec for field deployment
  1. Starlink business account for remote pods
  1. Run:AI licensing and setup
  1. First Solar panel mounting spec for container roof
---
> DANGER (2026-03-24): The "COPY FROM HERE" section at the top has WRONG pre-GTC specs. DO NOT COPY IT. Use CLAUDE.md in the git repo as the session startup source. It is current and authoritative. This Notion page is ARCHIVED -- do not use for session prompts.
---
> ARCHIVED (2026-03-24): This page is empty and vestigial. No content. Use the Pod Swarm Engineering Suite parent page instead.