# Digital Twin Video Production — Research & Options

## Objective
Create Vertiv OneCore-quality 3D animated videos showing ADC AI factory infrastructure: exploded/assembly views, shipping container deployment, power chain animations, cooling flow, facility flythroughs, and professional product renders.

## Reference: How Vertiv Does It
- Vertiv maintains a full 3D model library on Sketchfab (animated OneCore AI-ready Data Center model live there)
- Vertiv uses **Axonom Powertrak VR** for interactive product configurator/visualization
- Their high-end keynote animations (GTC, Computex) are produced by specialized studios like **Provis Media** (Wilmington, NC) — 23 years in tech marketing, clients include Supermicro and major data center companies
- The OneCore Rubin DSX video is studio-grade work — custom 3D modeling in professional DCC tools (likely 3ds Max or Cinema 4D), rendered with V-Ray or similar offline renderer, composited in After Effects
- **Estimated production cost**: $30,000–$80,000+ for a 2–3 minute cinematic piece at that quality level

---

## TOP 3 OPTIONS (Ranked by Quality)

### Option 1: Professional Studio (Vertiv-Quality)
**Quality: 10/10 | Cost: $15,000–$80,000 | Timeline: 4–10 weeks**

**What it is**: Hire a specialized 3D animation studio that does data center / industrial infrastructure videos.

**Studios to contact**:
- **Provis Media** (Wilmington, NC) — data center animation specialist. Supermicro keynotes, Cisco data center work. Phone: 888.880.6682 / new.business@provismedia.com
- **Austin Visuals** (Austin, TX) — engineering & technical animation studio, data center marketing videos. Phone: (512) 591-8024
- **3deeit** (Squamish, BC) — technical product animation from CAD data, trade show videos
- **FUSE Animation** — high-end 3D animation/rendering/VFX, replaces traditional production
- **Broadcast2World (B2W)** — state-of-art 3D animation infrastructure

**Cost breakdown (per minute of finished video)**:
- Entry-level 3D product animation: $5,000–$10,000/min
- Mid-tier product demo / exploded views: $10,000–$20,000/min
- High-end cinematic quality (Vertiv-level): $20,000–$50,000+/min

**What you get**: Photorealistic renders, smooth camera work, professional lighting, labeled callouts, branded color palette, broadcast-ready 4K output. Full exploded views, assembly sequences, power chain animations, cooling flow visualization.

**ADC-specific deliverables**:
1. 60s facility flythrough with labeled components — ~$15,000–$25,000
2. 60s exploded/assembly view of ADC 3K pod — ~$10,000–$20,000
3. 60s power chain animation (solar to chip) — ~$10,000–$15,000
4. 60s cooling flow animation (chip to heat reuse) — ~$10,000–$15,000
5. Full 3-minute cinematic reel combining all — ~$40,000–$80,000

**Pros**: Best possible quality. Professional studios handle modeling, texturing, lighting, animation, rendering, compositing, sound design. Reusable 3D assets for future videos.
**Cons**: Expensive. Longest timeline. Requires detailed briefs and revision cycles.

---

### Option 2: Blender + Freelancer (Best Value)
**Quality: 7–8/10 | Cost: $2,000–$15,000 | Timeline: 2–6 weeks**

**What it is**: Hire a skilled Blender freelancer on Upwork/Fiverr to create the animations using pre-made data center 3D models plus custom modeling.

**Platform pricing (2026)**:
- **Fiverr**: 3D product animation services from $70 (basic) to $5,000+ (premium). Average delivery: 17 days. Exploded view specialists available.
- **Upwork**: $500–$3,000/min for freelance 3D animation. Industrial machinery animation jobs posted at ~$2,000 for 2–3 min video ($667–$1,000/min).
- **CGTrader**: 139+ data center 3D models available for purchase ($20–$200 each) — saves modeling time.

**Recommended approach**:
1. Buy data center rack/container/infrastructure 3D models from CGTrader/TurboSquid ($200–$500 total)
2. Hire Blender freelancer on Upwork ($40–$80/hr, or $2,000–$5,000 fixed per 60s video)
3. Provide reference video (Vertiv OneCore), SVG blueprints (already have 6-sheet package), site photos
4. Render in Blender Cycles (photorealistic) or EEVEE (fast, good enough)

**Blender capabilities**:
- Cycles renderer = physically accurate path tracing, near-photorealistic output
- Native exploded view animation from CAD imports (OBJ format)
- Blender 4.5 LTS: Vulkan support, faster renders, production-grade
- Blender MCP: AI-powered modeling with natural language (experimental)
- FREE software — zero licensing cost

**Cost estimate for ADC project**:
- 3-minute full video package: $5,000–$15,000
- Individual 60s segments: $1,500–$5,000 each
- Simple exploded view only: $500–$2,000

**Pros**: 10x cheaper than studio. Blender is free. Huge freelancer pool. Can iterate quickly. You own all assets.
**Cons**: Quality depends entirely on the freelancer. Need to vet portfolios carefully. No sound design included (add $500–$1,500).

---

### Option 3: AI-Assisted Pipeline (Fastest / Cheapest)
**Quality: 4–6/10 | Cost: $100–$2,000 | Timeline: 1–7 days**

**What it is**: Combine AI 3D model generation + AI video generation for rapid prototyping. Not Vertiv-quality, but good for pitch decks, social media, and concept visualization.

**AI 3D Model Generation (text/image to 3D)**:
- **Meshy AI** — #1 AI 3D model generator. Clean meshes, good edge flow. Text-to-3D in minutes. Best for iteration.
- **Tripo v3.0 Ultra** — Full pipeline: modeling, texturing, retopology, rigging. PBR support. Quad-based topology. 50% faster than competitors.
- **NVIDIA Edify 3D** — High-quality assets in <2 min. 4K textures, PBR materials, clean topology. Available via Shutterstock (early access). NOTE: NIM microservice preview discontinued as of June 2025.
- **World Labs Marble** — Generates explorable 3D worlds from text/images. World API launched Jan 2026. $1B funding (incl. $200M from Autodesk). "Neural CAD" in development — could generate component systems.

**AI Video Generation (text/image to video)**:
- **Runway Gen-4.5** — Industry standard for branded content. Best details, most professional quality. Cleanest output.
- **Kling 2.6** — Up to 60 seconds (longest of any platform). Audio-visual generation in single pass. Rivals Runway quality at fraction of cost.
- **Pika 2.5** — Easiest to use. $8/month. Realistic visuals, smooth motion.
- **Luma Ray3** — Physics-first approach. Best for product shots. Native HDR. Can accept .obj/.fbx uploads as structure reference. 16-bit EXR export for pro workflows.
- **Google Veo 3** — Strong competitor, native 4K.

**Recommended AI pipeline**:
1. Generate 3D models with Meshy/Tripo (server rack, container, cooling unit, solar panel)
2. Arrange in Blender (free) or Tripo Studio
3. Render key frames / turntable views
4. Feed to Luma Ray3 or Runway Gen-4.5 for animated sequences
5. OR: Use World Labs API to generate explorable 3D scene from text description
6. Composite in DaVinci Resolve (free) with labels, callouts, branding

**Current AI limitations**:
- AI video generators struggle with precise technical accuracy (labels, specific component shapes)
- No AI tool can reliably generate a technically accurate data center exploded view from text alone — yet
- Physics consistency improving but not reliable for engineering-grade visualization
- Best used for: concept videos, social media clips, pitch deck backgrounds, mood boards

**Cost estimate**:
- AI models + video generation: $50–$200 in API credits
- Blender compositing (DIY): $0 (your time)
- Freelancer to polish AI output: $500–$2,000
- Total: $100–$2,000

**Pros**: Incredibly fast. Can generate 10 concepts in a day. Perfect for rapid prototyping before committing to expensive studio work.
**Cons**: Not Vertiv-quality. Technical accuracy issues. Requires manual cleanup.

---

## OMNIVERSE + RUNPOD: CAN WE DO IT OURSELVES?

### Short answer: Partially yes, but not for the marketing video.

**What Omniverse DSX Blueprint actually does**:
- It's a **digital twin simulation tool**, not a marketing video production tool
- Designed for AI factory design validation, thermal simulation, power analysis
- Can render photorealistic views of the facility
- Supports headless cloud deployment (could run on RunPod)
- Requires: Linux (Ubuntu 22.04/24.04), Docker + NVIDIA Container Toolkit, Git LFS

**What we already have on RunPod**:
- Kit SDK 109.0.4 installed on network volume
- DSX Blueprint v2.1 (42GB) already downloaded
- Render agent deployed (FastAPI on port 8501)
- L40S pod available ($0.79/hr when running)

**What Omniverse CAN do for us**:
- Generate photorealistic still renders of the facility layout (already proven — 4 render batches completed)
- Create turntable/flythrough camera animations and export frames
- Validate facility design with real physics simulation
- Provide source material for a professional studio to use

**What Omniverse CANNOT easily do**:
- Exploded/assembly animations (not a motion graphics tool)
- Branded callouts, labels, kinetic typography
- Sound design, music sync
- The polished, edited final video product

**Recommendation**: Use Omniverse renders as SOURCE MATERIAL for the studio/freelancer. This saves them modeling time and ensures technical accuracy. The render agent can batch-produce stills and camera paths; the studio handles animation, editing, and polish.

---

## RECOMMENDED STRATEGY (PHASED)

### Phase 1: AI Rapid Prototypes (This Week — $100–$300)
- Generate concept animations with Luma Ray3 / Runway Gen-4.5 using existing site photos + blueprints
- Create 3–5 short clips (10–15s each) for social media and pitch deck
- Use Meshy/Tripo to generate 3D models of server racks, containers, solar panels
- Test World Labs API for explorable 3D scene of Trappeys campus
- **Purpose**: Quick content for immediate use; concept validation before big spend

### Phase 2: Blender Freelancer Package (Weeks 2–4 — $5,000–$10,000)
- Hire top-rated Upwork Blender freelancer with industrial/product animation portfolio
- Provide: SVG blueprints (6-sheet package), Omniverse renders, site photos, Vertiv reference video
- Deliverables: 4x 60-second segments (exploded view, power chain, cooling flow, flythrough)
- Render in Blender Cycles at 4K
- Add labels, callouts, branding in After Effects or DaVinci Resolve
- **Purpose**: Website hero videos, investor presentations, NVIDIA partnership pitch

### Phase 3: Studio Cinematic Reel (Month 2–3 — $30,000–$50,000, IF funded)
- Engage Provis Media or Austin Visuals for broadcast-quality 3-minute reel
- Reuse 3D assets from Phase 2 as starting point
- Full cinematic treatment: voiceover, sound design, music, color grading
- **Purpose**: GTC presentation, city council, major investor meetings, YouTube channel

---

## COST SUMMARY TABLE

| Option | Quality | Cost Range | Timeline | Best For |
|--------|---------|-----------|----------|----------|
| AI Pipeline (DIY) | 4–6/10 | $100–$2,000 | 1–7 days | Social media, pitch decks, rapid prototyping |
| Blender Freelancer | 7–8/10 | $2,000–$15,000 | 2–6 weeks | Website, investor deck, NVIDIA pitch |
| Professional Studio | 9–10/10 | $15,000–$80,000 | 4–10 weeks | GTC keynote, broadcast, flagship marketing |
| Omniverse (existing) | 7/10 stills | $0.79/hr RunPod | Days | Source renders, design validation |

## KEY CONTACTS

| Company | Specialty | Contact |
|---------|-----------|---------|
| Provis Media | Data center animation (Supermicro, Cisco) | 888.880.6682 / new.business@provismedia.com |
| Austin Visuals | Engineering/technical animation | (512) 591-8024 |
| 3deeit | CAD-to-animation, trade show videos | squamish, BC (website: 3deeit.com) |
| FUSE Animation | High-end 3D/VFX | fuseanimation.com |

## TOOLS REFERENCE

| Tool | Type | Cost | Best For |
|------|------|------|----------|
| Blender 4.5 | 3D DCC + renderer | FREE | Modeling, animation, Cycles rendering |
| Unreal Engine 5.7 | Real-time renderer | FREE (5% royalty >$1M) | Interactive walkthroughs, real-time viz |
| NVIDIA Omniverse | Digital twin platform | FREE (Kit SDK) | Design validation, source renders |
| Meshy AI | AI 3D model gen | Subscription | Quick 3D assets from text/image |
| Tripo v3.0 Ultra | AI 3D model gen | Subscription | Full pipeline, PBR, game-ready |
| Runway Gen-4.5 | AI video gen | Credits | Professional AI video, brand control |
| Luma Ray3 | AI video gen | Credits | Physics-accurate product shots, HDR |
| Kling 2.6 | AI video gen | Credits | Long-form (60s), cost-effective |
| World Labs Marble | AI 3D world gen | API credits | Explorable 3D scenes from text |
| DaVinci Resolve | Video editor | FREE | Compositing, color grading, export |

---

*Research completed 2026-03-24. Prices are estimates based on market research — get quotes for exact numbers.*
