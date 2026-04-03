# Ground Zero — Command Center
*Notion backup — 2026-04-03*

> YouTube channel @GroundZero-ai — AI news show. AIDO pipeline handles TTS, B-roll, render, and upload. EP001 is private and live. EP002 in pipeline.
---
## Quick Links
- Channel: @GroundZero-ai
- EP001: https://www.youtube.com/watch?v=2B-W9d6aLEw (private)
- Domain: groundzeroai.com
- Pipeline code: aido/ in gpu-learning-lab repo
---
## Sub-Pages
- Episode Production Guide
- AIDO Pipeline Reference
- Social & Distribution
- Episode Archive
*[Child: Episode Production Guide]*
# Episode Production Guide
> Standard process for producing a Ground Zero AI news episode end-to-end.
---
## Episode Format
  - Style: AI news show — lower-third news template
  - Audio: ElevenLabs eleven_multilingual_v2, stability=0.32, style=0.55
  - 6 audio segments per episode
  - B-roll: Pexels API (requires PEXELS_API_KEY)
  - Render: local or RunPod Omniverse (requires RUNPOD_POD_IP)
---
## Production Workflow
  - 1. Story selected and added to Story Pipeline database
  - 2. Manifest written (episode metadata, script, segment timing)
  - 3. TTS generated: python -m aido.tts_generate --episode EP00X
  - 4. B-roll injected: python -m aido.inject_content --episode EP00X
  - 5. Episode rendered: python -m aido.pipeline --episode EP00X --local-render
  - 6. Review and approve
  - 7. Upload: python -m aido.pipeline --episode EP00X --from-stage upload --privacy private
---
## Environment Variables Required
  - ANTHROPIC_API_KEY — script generation
  - ELEVENLABS_API_KEY — TTS audio
  - PEXELS_API_KEY — B-roll footage (NOT YET SET)
  - RUNPOD_POD_IP — Omniverse render mode (NOT YET SET)
  - youtube_token.json — OAuth token in project root
---
## Open Blockers
> PEXELS_API_KEY not set — B-roll falls back to noise. Get key at pexels.com/api.
> RUNPOD_POD_IP not set — Omniverse render blocked. Use --local-render as workaround.
*[Child: AIDO Pipeline Reference]*
# AIDO Pipeline Reference
AI Daily Omniverse pipeline modules — located in aido/ directory of gpu-learning-lab repo.
---
## Pipeline Modules
  - manifest_schema — episode manifest validation
  - tts_generate — ElevenLabs TTS audio generation
  - inject_content — B-roll and asset injection
  - render_episode — Omniverse scene render
  - assemble — combine audio, video, lower-thirds
  - render_local — local render fallback (no RunPod)
  - upload_youtube — YouTube OAuth upload
  - pipeline — full orchestrator, runs all stages
---
## TTS Settings (EP001 reference)
  - Model: eleven_multilingual_v2
  - Stability: 0.32
  - Style: 0.55
  - 6 segments per episode
---
## YouTube OAuth
  - Token file: youtube_token.json in project root
  - Google account: dedicated business account
  - Chrome profile: dedicated Ground Zero profile
  - Handle: @GroundZero-ai
---
## Common Commands
Full render from scratch: python -m aido.pipeline --episode EP002 --local-render
Upload only: python -m aido.pipeline --episode EP002 --from-stage upload --privacy private
TTS only: python -m aido.tts_generate --episode EP002
*[Child: Social & Distribution]*
# Social & Distribution
---
## YouTube
  - Channel: @GroundZero-ai
  - EP001: https://www.youtube.com/watch?v=2B-W9d6aLEw (private)
  - EP002: In production pipeline
---
## Social Accounts — NEEDED
> Social accounts not yet created. All should use handle @GroundZeroAI.
  - TikTok — @GroundZeroAI (NOT CREATED)
  - Instagram — @GroundZeroAI (NOT CREATED)
  - X/Twitter — @GroundZeroAI (NOT CREATED)
  - LinkedIn — @GroundZeroAI (NOT CREATED)
---
## Domain
  - groundzeroai.com — register/verify ownership
---
## Launch Checklist — Do These In Order
> Complete these before publishing EP001 publicly. Each one is a 15-30 minute task.
  - [ ] Create TikTok account — @GroundZeroAI
  - [ ] Create Instagram account — @GroundZeroAI
  - [ ] Create X/Twitter account — @GroundZeroAI
  - [ ] Create LinkedIn page — @GroundZeroAI
  - [ ] Register groundzeroai.com domain (or verify ownership)
  - [ ] Get PEXELS_API_KEY — free at pexels.com/api — paste into Vercel + local .env
  - [ ] Set channel description, banner, and profile photo on YouTube
  - [ ] Link groundzeroai.com to YouTube channel (YouTube Studio → Customization → Basic Info)
  - [ ] Set EP001 to Public
  - [ ] Post EP001 clip to TikTok, Instagram Reels, X on same day
---
## Content Distribution Per Episode
  - YouTube: Full episode upload (primary)
  - TikTok: 60-90 second highlight clip from best segment
  - Instagram Reels: Same clip as TikTok or separate angle
  - X/Twitter: Thread summarizing 3 key points + YouTube link
  - LinkedIn: Long-form post with business angle + YouTube link (Gulf Coast / ADC ecosystem audience)
*[Child: Episode Archive]*
# Episode Archive
---
## EP001 — NVIDIA's $4B Photonics Play
  - Status: Rendered, private on YouTube
  - URL: https://www.youtube.com/watch?v=2B-W9d6aLEw
  - Version: v3 (final)
---
## EP002 — Apple M5 Fusion, OpenAI GitHub Rival, Nuclear Powers AI
  - Status: In Story Pipeline — not yet rendered
---
## Story Pipeline (5 stories queued)
  - AI inference identified as critical cybersecurity battleground
  - Amazon acquires 122-acre GWU campus in Ashburn VA for $427M
  - Apple unveils M5 Pro and M5 Max with Fusion Architecture
  - Largest anti-AI protest marches through London King's Cross tech hub
  - NVIDIA invests $4B in photonics companies Lumentum and Coherent
---
## ADC Ecosystem Episodes — Planned
> These episodes leverage the ADC insider advantage. Produce as projects develop.
  - EP-ADC-01: Why Louisiana for AI Infrastructure
  - EP-ADC-02: Immersion Cooling Explained — Louisiana heat + ADC 3K pods
  - EP-ADC-03: NVIDIA Vera Rubin NVL72 — 3.6 ExaFLOPS per rack explained
  - EP-ADC-04: Bloom Energy + Natural Gas — powering edge compute off-grid
  - EP-ADC-05: Gulf Coast Emergency Drone Hub — KLFT + SkyCommand
  - EP-ADC-06: Building MARLIE I — Phase 1 documentary
  - EP-ADC-07: New Iberia Solar — Louisiana renewable manufacturing
  - EP-ADC-08: Edge vs. Hyperscale — why distributed AI wins for the Gulf Coast
*[Child: Content Strategy & Mission]*
> Ground Zero is not just a YouTube channel. It is the media and public relations arm of the entire ADC infrastructure ecosystem — building audience credibility, documenting the journey, and creating awareness in the Louisiana business and tech community before MARLIE I goes live.
---
## Mission Statement
Ground Zero covers the AI infrastructure revolution from the inside. While every other AI news channel reports on what NVIDIA, Google, and OpenAI are doing, Ground Zero reports on what those technologies mean for the Gulf Coast, for Louisiana industry, and for the businesses and communities that will run on this infrastructure. We have the insider angle — because we are building it.
---
## Target Audience — Three Layers
### Layer 1 — AI & Tech Enthusiasts (Broad)
  - Demographics: 25-45, tech-curious, follows AI news, works in tech or adjacent fields
  - What they want: Clear explanations of AI breakthroughs, what matters vs. hype, real-world applications
  - How we serve them: Fast, well-produced AI news with context — no jargon, no filler
### Layer 2 — Business & Industry (Gulf Coast Focus)
  - Demographics: Louisiana/Gulf Coast business owners, energy sector, industrial, municipal decision-makers
  - What they want: How AI affects their industry, what infrastructure is coming to their region, who the local players are
  - How we serve them: Louisiana-specific angles, local economic impact stories, Gulf Coast infrastructure coverage
### Layer 3 — Investors & Partners (High Value)
  - Demographics: Angel investors, VCs, economic development officials, potential ADC tenants and partners
  - What they want: Credibility signals, proof of execution, evidence that the team knows the space
  - How we serve them: Deep technical accuracy, infrastructure investment angles, demonstrating that ADC leadership understands the market
---
## Content Pillars
### 1. AI Infrastructure News (Weekly)
  - NVIDIA, AMD, Intel hardware releases — what they mean for edge compute
  - Data center industry moves — hyperscale vs. edge, capacity announcements
  - Energy and power for AI — natural gas, nuclear, solar, hydrogen
  - Drone and autonomous systems — FAA policy, platform developments, Gulf Coast applications
### 2. Louisiana & Gulf Coast AI (Bi-weekly)
  - Local infrastructure development — what's being built and by whom
  - Energy sector AI — petrochemical, pipeline, offshore applications
  - Municipal AI — smart city, emergency response, public safety
  - University research — UL Lafayette, LSU, Tulane AI programs
### 3. ADC Insider Series (Monthly — when ready)
  - Building MARLIE I — documentary-style build journal
  - ADC 3K pod deployment — first unit install at Trappeys Cannery
  - KLFT SkyCommand — Gulf Coast Emergency Drone Hub development
  - Behind the infrastructure — cooling systems, power architecture, network design
---
## The ADC Insider Advantage
> No other Gulf Coast media outlet can cover AI infrastructure from the inside. Ground Zero is built by the people building the infrastructure. This is the unfair advantage — and it compounds over time as ADC projects go live.
  - EP001 covered NVIDIA photonics — we have NVIDIA Vera Rubin NVL72 on order. We are the customer.
  - Every story about GPU compute, data centers, and edge AI is a story about what we are building
  - KLFT/SkyCommand episodes establish credibility before the hub is operational
  - MARLIE I build journal creates investor awareness before the fundraise closes
  - Louisiana audience: No competing voice covering Gulf Coast AI infrastructure from this angle
---
## ADC Ecosystem Story Pipeline
These episodes should be produced as ADC projects develop. Each one builds credibility and awareness.
  - EP-ADC-01: Why Louisiana for AI Infrastructure — natural gas, LUS Fiber, low power cost, ITEP incentives
  - EP-ADC-02: Immersion Cooling Explained — why ADC 3K pods use full immersion in Louisiana heat
  - EP-ADC-03: NVIDIA Vera Rubin NVL72 — what 3.6 ExaFLOPS per rack means for regional AI
  - EP-ADC-04: Bloom Energy + Natural Gas — how ADC powers edge compute without grid dependency
  - EP-ADC-05: Gulf Coast Emergency Drone Hub — KLFT, SkyCommand, and hurricane response AI
  - EP-ADC-06: Building MARLIE I — Phase 1 construction documentary
  - EP-ADC-07: New Iberia Solar — supporting Louisiana's renewable manufacturing industry
  - EP-ADC-08: The Edge vs. Hyperscale Debate — why distributed AI wins for the Gulf Coast
---
## Monetization Roadmap
### Phase 1 — Build Audience (Now → 1,000 subscribers)
  - YouTube AdSense (minimal revenue — not the goal yet)
  - Establish credibility and consistent publishing cadence
  - Goal: Be the recognized voice for Gulf Coast AI infrastructure
### Phase 2 — Sponsorships (1,000 → 10,000 subscribers)
  - Infrastructure vendors: cooling systems, power equipment, networking gear
  - Louisiana business services: energy, legal, finance, construction
  - AI software platforms: inference, monitoring, MLOps tools
### Phase 3 — Strategic Value (ADC launches)
  - Ground Zero audience = pre-warmed investor and tenant pipeline for MARLIE I
  - Media credibility accelerates ADC partnership conversations
  - Channel becomes a recruiting and awareness tool for ADC talent pipeline
  - Potential: ADC-branded content series, sponsored episodes, paid workshops
---
## Publishing Cadence Target
  - Minimum: 1 episode per week once social accounts are live
  - Ideal: 2 episodes per week — 1 general AI news, 1 Gulf Coast / ADC angle
  - Format: 8-12 minutes per episode — long enough for depth, short enough for retention
  - Distribution: YouTube (primary) + TikTok clips + Instagram Reels + LinkedIn long-form
---
## Strategic Role
> Ground Zero is the media arm of the ADC ecosystem. Every episode builds audience credibility, investor awareness, and Louisiana business recognition before MARLIE I opens and ADC 3K pods deploy. See Content Strategy & Mission for full plan.
- Channel: @GroundZero-ai (YouTube) | Handle everywhere: @GroundZeroAI
- ADC Insider Series: Document MARLIE I build, ADC 3K first deployment, KLFT SkyCommand hub
- Audience: AI/tech enthusiasts (broad) + Gulf Coast business (regional) + investors/partners (high value)
---
> MERGED 2026-03-23: Ground Zero and AI Daily Omniverse are now ONE project.
## Ground Zero - Unified YouTube Strategy
### Channel: @ScottTomsu (YouTube)
NOT @GroundZero-ai. Use Scott's existing channel which already has the LinkedIn post live and connections building. One person, one brand, one channel.
### Content Strategy (Merged):
- Short-form (2-5 min): Screen record + voiceover. Louisiana initiative, blueprints, renders, tech explainers. Weekly.
- Long-form (8-12 min): Omniverse-rendered episodes when pipeline is ready. Monthly goal.
- LinkedIn cross-post everything - LinkedIn is the primary audience right now (14 impressions in 2 hrs with zero subscribers)
### 5 Video Scripts Ready (2026-03-23):
- 1. "Louisiana Has ZERO GPUs. Florida Has 504." (~2:30)
- 2. "Two Abandoned Buildings -> AI Factories" (~3:00)
- 3. "AI Runs My Entire Business" (~3:30)
- 4. "800 Volts DC - Why This Changes Everything" (~2:30)
- 5. "Nobody Is Filing the Paperwork" (~3:00) - RECORD THIS FIRST (8 days to NVIDIA deadline)
Scripts at: scripts/youtube/ground-zero-scripts.md
### Production Pipeline:
- Quick videos: Phone + screen capture. No fancy editing needed.
- Omniverse episodes: RunPod L40S pod (ml4cl3icn37ys1), Kit SDK 109, render agent on port 8501, 250GB network volume
- TTS: ElevenLabs (configured, stability=0.32, style=0.55)
- Thumbnails: FLUX Schnell ($0.003 each)
### What's Done:
- EP001 rendered, private on YouTube (make PUBLIC)
- EP002 scripted, not rendered
- 5 new scripts from today
- Scene Design Package v1.0 (20m command floor, 6 zones)
- React dashboard component
- Branding defined (dark #06080d, cyan #00f0ff)
### What's NOT Done:
- Social accounts (TikTok, Instagram, X) - NOT CREATED
- groundzeroai.com domain - NOT REGISTERED
- PEXELS_API_KEY - NOT SET
- Full Omniverse render pipeline - NOT TESTED end-to-end with current Kit SDK 109
### Priority
Ship imperfect content NOW. Stop waiting for world-class production. Record Video 5 with a phone and screen capture this week.