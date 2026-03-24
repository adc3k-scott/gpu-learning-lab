# Terafab Research — Deep Dive (March 23, 2026)

## What Is Terafab?

**Terafab** is a $20-25 billion joint semiconductor fabrication venture announced by Elon Musk on March 21, 2026, at the Seaholm Historic Power Plant in Austin, Texas. Texas Governor Greg Abbott attended. Musk called it "the most epic chip building exercise in history by far."

It is a **joint venture between three Musk-controlled entities**:
- **Tesla** (publicly traded, TSLA)
- **SpaceX** (private, ~$1T valuation)
- **xAI** (acquired by SpaceX in February 2026 via all-stock deal; combined entity valued at ~$1.25T)

Musk is CEO of all three. No independent corporate entity for "Terafab" has been announced — it operates under the combined Tesla/SpaceX/xAI umbrella.

### The SpaceX-xAI Merger Context
- **February 3, 2026**: SpaceX acquired xAI in an all-stock deal (0.1433 SpaceX shares per xAI share)
- Largest merger in history: SpaceX valued at $1T, xAI at $250B
- 9 of 11 xAI co-founders have departed; only Musk and one other remain
- SpaceX IPO expected at $1.5-1.75T valuation — Terafab announcement seen by some analysts as narrative-building for that IPO

---

## What Chips Are They Making?

### Two chip families:

**1. AI5 / AI6 — Terrestrial Inference Chips**
- For Tesla Full Self-Driving, Cybercab robotaxis, and Optimus humanoid robots
- AI5 specs vs AI4: 40-50x more compute, 9x memory capacity, 10x raw compute, 5x improvement in hardened block quantization and softmax
- Small-batch AI5 production: late 2026 (likely at Samsung, NOT Terafab)
- Volume AI5 production: 2027
- AI6 also mentioned but no specs disclosed

**2. D3 — Space-Grade Radiation-Hardened Chips**
- Designed for orbital AI satellite constellation
- Must withstand extreme temperatures and cosmic radiation
- Optimized for high-power operation in space
- Feeds SpaceX's planned constellation of 1 million AI satellites (FCC application filed January 2026)

### Production Allocation
- **80% of output**: Space-based orbital AI satellites
- **20% of output**: Terrestrial (Tesla vehicles, robots)

---

## Production Targets

- **Annual compute output goal**: 1 terawatt (current global AI chip output: ~20 gigawatts — so 50x the entire world's current production)
- **Chip volume**: 100-200 billion custom AI and memory chips annually
- **Terrestrial compute**: 100-200 gigawatts for robotics/vehicles
- **Initial wafer starts**: 100,000 per month
- **Full-scale wafer starts**: 1,000,000 per month (~70% of TSMC's entire current global capacity)
- **Process node target**: 2-nanometer (GAAFET — Gate-All-Around Field Effect Transistors)

For context: TSMC's current global capacity is 1.4-1.6 million wafer starts/month, built over 35+ years with hundreds of billions in investment.

---

## Where Is the Factory?

**Announced location**: Austin, Texas — North Campus of Giga Texas (Tesla's existing gigafactory)

**Key details**:
- Initial "advanced technology fab" starts at Giga Texas campus
- Full-scale Terafab requires "thousands of acres" — cannot fit on existing Giga Texas campus
- Musk stated facility could be 100 million square feet (~15 Pentagons, ~3 Central Parks)
- Full-scale site location NOT yet determined
- Permit documents show plans for 5.2 million sq ft of new building space by end of 2026
- **Not built yet** — site preparation underway for prototype/initial fab only

**Full-scale site still TBD** — this is the key opportunity for other states.

---

## Funding

- **Estimated cost**: $20-25 billion
- **NOT yet in Tesla's budget**: Tesla CFO acknowledged Terafab cost is NOT incorporated into Tesla's 2026 capex plan (which already exceeds $20 billion independently)
- **Potential capital raise**: Tesla's 10-K filing states the company "may decide it is best to raise additional capital or seek alternative financing sources" — market reads this as likely secondary stock offering (dilution)
- **CHIPS Act**: Could potentially qualify for federal CHIPS and Science Act funding ($52B total pool), but no application or award announced
- **Texas TSIF**: Texas Semiconductor Innovation Fund has ~$948M available; Governor Abbott already gave SpaceX a TSIF grant (amount not disclosed in sources)

---

## Timeline

| Milestone | Date |
|-----------|------|
| Terafab announced | March 21, 2026 |
| Site prep at Giga Texas North Campus | Underway |
| AI5 small-batch production (at Samsung, not Terafab) | Late 2026 |
| AI5 volume production (at Samsung) | 2027 |
| Terafab construction timeline | NOT announced |
| Realistic first Terafab chip production (analyst estimate) | 2028 earliest, more likely 2030-2032 |
| Industry benchmark: US fab construction time | ~38 months |
| TSMC Arizona 2nm production | 2029 |

Musk said chips needed "within three to four years" (by 2029-2030) from January 2026 comments.

---

## Who's Leading Engineering?

**Major problem: Tesla lost its entire chip leadership team.**

| Person | Role | Status |
|--------|------|--------|
| Jim Keller | Legendary chip architect (AMD Zen, Apple A4/A5) | Left Tesla 2018 (now CEO of Tenstorrent) |
| Peter Bannon | Chief of all custom silicon at Tesla (from Apple PA Semi) | Left August 2025 when Dojo killed |
| Ganesh Venkataramanan | Led Dojo AI training chip project | Left late 2023; ~20 team members followed to DensityAI |

**Current known personnel**:
- **Dan Priestley**: Tesla Semi Program Director (mentioned in Terafab context)
- **Franz von Holzhausen**: Tesla Chief Designer (mentioned at event)
- Tesla actively recruiting: lithography engineers, process integration specialists, fab construction managers
- Recent hires from xAI side: Devendra Singh Chaplot (ex-Mistral AI co-founder), Andrew Milich and Jason Ginsberg (ex-Cursor engineers)

**The talent gap is the biggest red flag.** TSMC has ~50,000 dedicated fab engineers. Tesla has zero semiconductor manufacturing experience. The global pool of qualified fab construction managers numbers in the hundreds.

---

## Competition and Market Context

### Who Terafab competes with:
- **TSMC**: World's dominant foundry. 35 years experience. $165B invested in Arizona fabs alone. 2nm pilot in 2026, Arizona 2nm by 2029.
- **Samsung**: Working on 2nm GAAFET; facing yield challenges at 3nm
- **Intel**: Struggling despite 100+ years of fab experience and $100B+ investment
- **NVIDIA**: Designs but doesn't fabricate; CUDA moat remains strongest competitive advantage
- **Broadcom**: Custom silicon for hyperscalers (Google TPU)
- **AMD, Qualcomm, Apple**: All fabless — design chips, use TSMC/Samsung to manufacture

### Custom silicon trend (everyone doing it):
- Google: TPU (designed in-house, fabbed at TSMC)
- Amazon: Trainium, Inferentia (for AWS)
- Microsoft: Custom AI accelerators (Maia)
- Meta: MTIA chips
- Tesla/Musk: Now proposing to own the ENTIRE stack — design AND fabrication

**Jensen Huang's response**: "Building advanced chip manufacturing is extremely hard... matching TSMC's capabilities is 'virtually impossible.'"

---

## Skepticism and Execution Risk

### The Bear Case (extensive):

1. **Zero fab experience**: Tesla has never manufactured a single semiconductor. Chip design =/= chip fabrication.

2. **Battery Day parallel**: In September 2020, Tesla promised 4680 cells at 100 GWh by 2022, reaching 3 TWh by 2030. Five years later: ~20 GWh production, ~2% of target. Supplier L&F Co. wrote down Tesla deal by 99%.

3. **Cost reality**: A single 2nm fab with 50,000 wafer starts/month costs ~$28 billion. Terafab's $20-25B budget may not cover even Phase 1.

4. **Equipment bottleneck**: ASML is the ONLY manufacturer of EUV lithography scanners globally. Cost: $150-200M each ($380M for High-NA). Lead time: 2+ years. Supply chain: 5,000+ suppliers per machine.

5. **Talent crisis**: All key chip leaders (Keller, Bannon, Venkataramanan) have left. TSMC itself struggles to recruit qualified US workers for its Arizona fabs.

6. **Supply chain dependencies**: 300mm silicon wafers (Shin-Etsu, Sumco, Siltronic), photoresists (JSR, Shin-Etsu Chemical — all Japan), neon gas (Ukraine/Russia disrupted), ultrapure chemicals.

7. **Power**: 150-200 MW continuous for the fab alone; 10+ GW for the full vision. Austin's grid already strained.

8. **Water**: Millions of gallons daily for wafer cleaning. Austin has water scarcity issues.

9. **The orbital compute claim**: 80% of output for space satellites is "essentially zero connection to any near-term business reality" per Electrek. 50,000 Starship launches/year (~135/day) would be needed.

10. **Stock price**: TSLA down 17% from March highs; three consecutive down days post-announcement. Market sees unfunded liability.

### The Bull Case:
- Musk has done "impossible" things before (reusable rockets, mass-market EVs)
- Vertical integration eliminates supply chain dependency on TSMC/Samsung
- SpaceX's launch cost advantage ($100/kg to orbit) enables orbital compute vision
- $1.25T combined SpaceX/xAI entity has financial capacity
- CHIPS Act + Texas incentives could offset costs
- AI chip demand is structurally infinite — any capacity gets absorbed

---

## The Orbital AI Satellite Angle

SpaceX filed FCC application (January 2026) for **1 million AI data center satellites**:
- Called "AI Sat Mini"
- Each ~170 meters long
- 100 kW onboard processing per satellite
- Operating at 500-2,000 km altitude
- Solar power advantage: 1,361 W/m2 in orbit vs 250-300 W/m2 on Earth's surface

Musk claims orbital compute will be cheaper per watt than terrestrial "within 2-3 years." Industry experts are deeply skeptical — radiation hardening reduces performance, launch logistics are staggering, and thermal management in vacuum is unsolved at scale.

---

## ADC Strategic Implications

### Opportunities:

1. **Full-scale Terafab site is TBD.** The Austin prototype fab is confirmed, but the "thousands of acres" full-scale facility has no announced location. Louisiana has:
   - Cheapest industrial power in the US (Henry Hub natural gas)
   - CHIPS Act eligibility
   - Act 730 (20-year sales tax exemption)
   - ITEP ($8-16M savings for qualifying facilities)
   - Brownfield sites with existing heavy industrial infrastructure (Willow Glen = former 2,200 MW power station)
   - Mississippi River water access (fabs need millions of gallons/day)
   - Workforce development via UL Lafayette partnership

2. **Chip-agnostic infrastructure.** ADC's 800V DC + liquid cooling architecture works for ANY vendor's chips. If Terafab produces inference chips, ADC pods can deploy them. The pod architecture doesn't care if the silicon says NVIDIA, AMD, or Tesla.

3. **Vendor diversification narrative.** Terafab's existence (even as vaporware) strengthens ADC's pitch that the AI compute market is multi-vendor. Being NVIDIA-first but not NVIDIA-only is the right positioning.

4. **Power partner angle.** Terafab needs 10+ GW at full scale. If any satellite facilities or edge deployments spin off, Louisiana's power economics are compelling. ADC's 4-layer power hierarchy (solar + gas + diesel + grid sell-back) is exactly what a chip fab needs for reliability.

5. **Inference deployment.** If AI5/AI6 chips are available commercially (big if), ADC could be an early deployment partner for inference workloads — especially if they're cheaper/watt than NVIDIA for specific use cases.

### Risks:

1. **Terafab may never ship.** Battery Day history. Zero fab experience. Unfunded. This could be a nothing-burger.

2. **Vertical integration means captive.** Terafab chips may ONLY go to Tesla/SpaceX/xAI — never sold commercially. In that case, zero relevance to ADC.

3. **Timeline mismatch.** Even optimistically, Terafab chips won't exist until 2028-2030. ADC is building NOW. NVIDIA DSX is available NOW.

4. **Distraction risk.** Don't let Terafab speculation distract from the NVIDIA certification ladder that's actually happening.

### Bottom Line for ADC:
- **Watch, don't pivot.** Terafab is interesting but 3-5 years away from mattering.
- **Strengthen the vendor-flexible pitch.** "Our infrastructure works with NVIDIA, AMD, or whatever Terafab produces."
- **If they need a site in Louisiana, be ready.** Have the power economics, incentive packages, and site data ready to pitch.
- **Keep NVIDIA as primary.** Jensen's $1T capex plan is real and shipping now. Terafab is a PowerPoint.

---

## Source URLs

### Primary Coverage
- [Electrek — Tesla and SpaceX announce $25B 'Terafab' chip factory](https://electrek.co/2026/03/22/tesla-spacex-terafab-chip-factory-ai-desperation/)
- [Teslarati — Elon Musk launches TERAFAB](https://www.teslarati.com/elon-musk-lanuches-terafab-tesla-spacexai-chip-factory/)
- [KUT Radio Austin — Musk announces chip manufacturing project in Austin](https://www.kut.org/business/2026-03-22/austin-tx-elon-musk-ai-chip-terafab-tesla-spacex)
- [Bloomberg — Elon Musk Plans Terafab Chip Facility in Austin](https://www.bloomberg.com/news/articles/2026-03-22/elon-musk-says-tesla-xai-spacex-terafab-to-start-in-austin)
- [TechCrunch — Elon Musk unveils chip manufacturing plans](https://techcrunch.com/2026/03/22/elon-musk-unveils-chip-manufacturing-plans-for-spacex-and-tesla/)
- [Benzinga — Elon Musk Unveils Ambitious Terafab Plans](https://www.benzinga.com/news/26/03/51396624/elon-musk-unveils-ambitious-terafab-plans-for-tesla-spacex-were-starting-a-galactic-civilization)
- [The Register — Elon Musk proposes 'Terafab' to level up chip production](https://www.theregister.com/2026/03/23/musk_terafab/)
- [Tom's Hardware — Elon Musk formally launches $20B TeraFab chip project](https://www.tomshardware.com/tech-industry/elon-musk-formally-launches-20-billion-terafab-chip-project)

### Deep Analysis
- [Kingy AI — Terafab: Elon Musk's $25 Billion Bet](https://kingy.ai/ai/terafab-elon-musks-25-billion-bet-to-build-the-worlds-biggest-chip-factory-and-why-it-might-be-the-most-audacious-gamble-in-tech-history/)
- [Teslarati — TERAFAB: Everything you need to know](https://www.teslarati.com/elon-musk-terafab-project-everything-you-need-to-know/)
- [FinTech Weekly — TERAFAB Launched: What Elon Musk Actually Built](https://www.fintechweekly.com/news/terafab-launch-tesla-spacex-xai-chip-factory-austin-march-2026)
- [WebProNews — Terafab: A $10 Billion Bet That America Can Build Its Own AI Chip Empire](https://www.webpronews.com/elon-musks-terafab-a-10-billion-bet-that-america-can-build-its-own-ai-chip-empire/)
- [igor'sLAB — TeraFab: grandiosity project or first step?](https://www.igorslab.de/en/elon-musk-unveils-terafab-just-another-grandiose-announcement-or-actually-the-first-step-toward-a-vertically-integrated-ai-silicon-megafactory/)
- [Electrek — Tesla's Terafab chip fab ambitions ignore total lack of semiconductor experience](https://electrek.co/2026/03/16/teslas-terafab-chip-fab-ambitions-ignore-its-total-lack-of-semiconductor-experience/)
- [New Atlas — Elon Musk's Terafab: massive AI chip plant plans](https://newatlas.com/ai-humanoids/elon-musk-terafab-chip-manufacturing-ai-data-center/)
- [NotebookCheck — Musk pitches pie-in-the-sky Terafab 2nm foundry](https://www.notebookcheck.net/Musk-pitches-pie-in-the-sky-Terafab-2-nm-foundry-for-SpaceX-and-Tesla-AI-chip-fare.1256767.0.html)

### Financial / Investor Analysis
- [TipRanks — Elon Drops $25B Terafab Bomb: Declare War on TSMC](https://www.tipranks.com/news/elon-drops-25b-terafab-bomb-tesla-spacex-xai-declare-war-on-tsmc-tsm)
- [Superintelligence Newsletter — Nvidia's $1T Bet vs. Musk's Terafab](https://www.superintelligencenewsletter.com/p/nvidias-1t-bet-vs-musks-terafab)
- [TheStreet — Elon Musk's Terafab bet: what it means for Tesla investors](https://www.thestreet.com/investing/elon-musks-terafab-bet-what-it-means-for-tesla-investors)
- [Electrek — Tesla Terafab plans point to inevitable capital raise](https://electrek.co/2026/03/17/tesla-tsla-terafab-capital-raise-secondary-offering/)
- [Phemex — TSLA Drops Despite Musk's Biggest Launch](https://phemex.com/blogs/tesla-tsla-drops-despite-terafab-launch-march-23)
- [Kavout — The AI Chip War Just Fractured: What Nvidia's $4.4T Dominance Faces in 2026](https://www.kavout.com/market-lens/the-ai-chip-war-just-fractured-what-nvidia-s-4-4-trillion-dominance-faces-in-2026)

### SpaceX / Orbital
- [SpaceNews — SpaceX offers details on orbital data center satellites](https://spacenews.com/spacex-offers-details-on-orbital-data-center-satellites/)
- [Data Center Dynamics — SpaceX files for million satellite orbital AI data center megaconstellation](https://www.datacenterdynamics.com/en/news/spacex-files-for-million-satellite-orbital-ai-data-center-megaconstellation/)
- [CNBC — Musk's xAI, SpaceX combo is the biggest merger of all time, valued at $1.25 trillion](https://www.cnbc.com/2026/02/03/musk-xai-spacex-biggest-merger-ever.html)

### Merger / Corporate
- [Sherwood News — SpaceX merges with xAI, reportedly will seek IPO valuation of $1.25 trillion](https://sherwood.news/tech/spacex-to-merge-with-xai-according-to-internal-memo-bloomberg-reports/)
- [ALM Corp — xAI Loses 9 of 11 Co-Founders](https://almcorp.com/blog/xai-co-founders-exodus-spacex-ipo-elon-musk-rebuild-2026/)

### Location / Austin
- [KVUE Austin — Elon Musk announces $20B chip plant coming to Austin](https://www.kvue.com/article/tech/elon-musk-announces-chip-plant-austin-travis-county-texas/269-fd28ad7c-2e20-4c9b-a358-f56835c5355a)
- [Community Impact — Musk announces largest chip manufacturing facility Terafab coming to Austin](https://communityimpact.com/austin/south-central-austin/development/2026/03/23/elon-musk-announces-largest-chip-manufacturing-facility-terafab-coming-to-austin/)
- [The Real Deal — Elon Musk's $20B Terafab will start in Austin](https://therealdeal.com/texas/austin/2026/03/23/elon-musk-20b-terafab-will-start-in-austin/)
- [Fortune — Musk says Tesla, SpaceX, xAI chip project to kick off in Texas](https://fortune.com/2026/03/22/musk-terafab-chip-project-tesla-spacex-xai-space-data-center-satellite/)

### Government / Incentives
- [Texas Governor — Texas Semiconductor Innovation Fund](https://gov.texas.gov/business/page/tsif)
- [Texas Governor — TSIF Grant to SpaceX](https://gov.texas.gov/news/post/governor-abbott-announces-texas-semiconductor-innovation-fund-grant-to-spacex)
- [CBS News — What is Elon Musk's Terafab chip project?](https://www.cbsnews.com/news/terafab-elon-musk-chips-semiconductors-what-to-know/)
- [Engadget — Musk announces Terafab project](https://www.engadget.com/science/elon-musk-announces-terafab-project-he-claims-will-be-the-largest-chip-manufacturing-facility-ever-171718545.html)
