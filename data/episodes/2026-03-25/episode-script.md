# AI Daily Omniverse -- Episode Script
## March 25, 2026

**Runtime**: ~8 minutes
**Anchors**: Armando (desk), Adriana (field reporter)
**Stories**: 5

---

## OPEN

**Armando**: Good morning and welcome to AI Daily Omniverse. I'm Armando at the desk. We have a packed show today -- NVIDIA just redefined what an AI factory can do for the power grid, Eaton and NVIDIA locked in the 800-volt future, Jensen Huang wants to pay engineers in tokens, the FAA is about to unlock autonomous drones across America, and Skydio just landed the biggest drone deal in US Army history. Let's get into it. Adriana, where are you this morning?

**Adriana**: I'm standing outside CERAWeek in Houston, Armando, where the energy industry and the AI industry just collided in a way nobody expected. Let's start there.

---

## STORY 1: NVIDIA + Emerald AI -- AI Factories as Grid Assets

**Adriana**: So here's the headline. NVIDIA and a company called Emerald AI just announced a partnership with six major energy companies -- AES, Constellation, Invenergy, NextEra, Nscale, and Vistra -- to build a new class of AI factory that doesn't just consume power. It gives power back to the grid.

**Armando**: Wait. AI factories selling electricity back to the grid? That flips the entire narrative. Everyone's been talking about how much power these facilities drain. Now NVIDIA is saying they can be grid assets?

**Adriana**: Exactly. The key is a new software layer called DSX Flex, built into the Vera Rubin reference design. It lets an AI factory coordinate its on-site generation -- solar, gas, batteries -- with its compute workloads in real time. When the grid needs power, the factory can throttle non-critical jobs and push electricity back out. Emerald AI says this approach could unlock up to 100 gigawatts of capacity across the US power system.

**Armando**: One hundred gigawatts. That's not a rounding error. That's a structural change to how we think about AI infrastructure. If you're building an AI factory with behind-the-meter generation -- solar, natural gas, batteries -- this architecture turns your facility from a power consumer into a power partner.

**Adriana**: And that's the whole point. These facilities can start on bridge power -- co-located generation -- and transition into grid-connected flexible assets over time. The interconnection queue gets shorter because you're not just asking the grid for power. You're offering something back.

---

## STORY 2: Eaton Beam Rubin DSX -- 800 Volt DC is the Standard

**Armando**: Staying on the infrastructure theme, Eaton and NVIDIA made it official at GTC. The Beam Rubin DSX platform is here -- a modular, pre-engineered power system designed specifically for NVL72 racks running on 800-volt DC. Adriana, why does this matter?

**Adriana**: Because it kills the old power architecture. Traditional facilities run AC power through multiple conversion stages -- transformer, UPS, PDU, rack PSU -- and every stage wastes energy as heat. The 800-volt DC path from Eaton eliminates most of those stages. Texas Instruments showed the math: two conversion stages from 800 volts down to the sub-one-volt GPU core. That's it. Higher efficiency, less cooling, more compute per megawatt.

**Armando**: And the ecosystem is massive. ABB, Delta, Schneider Electric, Infineon, Vertiv -- over 200 partners are aligned behind this standard. If you're designing a new AI factory today and you're not planning for 800-volt DC, you're building something that will be obsolete before you turn it on.

**Adriana**: The companies that figured out 800-volt DC early -- the ones pairing it with solar-direct architectures -- they're going to have a significant cost advantage for years.

---

## STORY 3: Jensen Huang -- Tokens as Employee Compensation

**Armando**: Jensen Huang made waves again this week, and not just with his AGI comments on the Lex Fridman podcast. During his GTC keynote, Huang predicted that AI tokens will become a standard employee benefit -- like a 401k or health insurance, but for compute.

Here's the exact quote: "I could totally imagine in the future every single engineer in our company will need an annual token budget. I'm going to give them probably half of that on top of it as tokens so that they could be amplified 10x."

**Adriana**: Think about what that means at scale, Armando. If every knowledge worker at every tech company gets an annual token allocation, the demand for inference compute doesn't just grow -- it explodes. We're not talking about a few companies buying API access. We're talking about tokens becoming as fundamental as bandwidth.

**Armando**: And every one of those tokens has to be generated somewhere. On physical GPUs. In physical AI factories. With physical power. The companies that can produce tokens at the lowest cost per unit -- because they own their power, they run Dynamo, they operate at scale -- those are the companies that win.

**Adriana**: The token economy just got a lot more real.

---

## STORY 4: FAA Part 108 -- BVLOS Drones About to Go Nationwide

**Armando**: Switching gears to the skies. The FAA's Part 108 rule -- the one that will finally allow beyond-visual-line-of-sight drone operations at scale -- is expected to drop as a final rule this spring. That could be weeks away.

**Adriana**: This has been years in the making. Part 107 required waivers for every BVLOS flight, which basically made commercial drone operations a paperwork nightmare. Part 108 replaces that with a standardized framework. Two tiers: operating permits for lower-risk flights, operating certificates for complex operations. Drones up to 1,320 pounds. And a new class of FAA-certified Automated Data Service Providers to handle real-time airspace deconfliction.

**Armando**: And that connects directly to our next story, because the hardware is ready. Skydio just proved it.

---

## STORY 5: Skydio $52M Army Contract -- American Drones at Scale

**Armando**: The US Army awarded Skydio a $52 million contract for over 2,500 X10D autonomous drones. That is the largest single-vendor tactical small UAS order in Army history. And here's the kicker -- bid to award in 72 hours.

**Adriana**: Seventy-two hours. That tells you everything about urgency. Every drone is manufactured in Hayward, California, 550 quality checkpoints per unit. The X10D navigates GPS-denied environments using onboard cameras to map terrain in real time. Skydio systems are now deployed across all US military branches and 29 allied nations.

**Armando**: American-made autonomous drones, proven at military scale, with Part 108 about to unlock civilian BVLOS. The convergence here is obvious. Emergency response, pipeline inspection, infrastructure monitoring, search and rescue -- all of it is about to accelerate. The facilities that can serve as drone operation hubs, with AI compute on-site for real-time video processing, are going to be in very high demand.

**Adriana**: The hardware is ready. The regulations are coming. The only question is who builds the ground infrastructure to support it.

---

## CLOSE

**Armando**: That's our show for March 25th. Let's recap: NVIDIA and Emerald AI are turning AI factories into grid assets with DSX Flex. Eaton's 800-volt DC Beam Rubin platform is the new power standard. Jensen Huang sees tokens becoming employee compensation -- a massive demand signal. Part 108 BVLOS is imminent. And Skydio just locked in the biggest drone contract in Army history. The theme today is convergence -- power, compute, and autonomy are all moving in the same direction, and they're moving fast.

**Adriana**: From CERAWeek in Houston, I'm Adriana. See you tomorrow.

**Armando**: And I'm Armando. Stay locked in. This is AI Daily Omniverse.

---

## SPONSOR TAG

*"Today's episode is brought to you by ADC -- Advantage Design & Construction. Louisiana's energy-first AI factory builder. From 800-volt solar-direct power to NVIDIA DSX reference design, ADC is building the infrastructure that powers the token economy. Learn more at adc3k.com."*

---

**END OF SCRIPT**
