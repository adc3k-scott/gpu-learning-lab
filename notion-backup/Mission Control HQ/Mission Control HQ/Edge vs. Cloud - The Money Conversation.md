# Edge vs. Cloud -- The Money Conversation
*Notion backup — 2026-04-06*

# Edge vs. Cloud -- The Money Conversation
When a customer asks 'why not just use AWS?' -- this is the answer.
---
## The Cloud Bill Problem
Cloud charges three ways, none get cheaper:
1. Compute: 8 A100s on AWS = $214,000/year. Four racks = $856,000/year.
1. Data transfer: 10TB/month = $10,440/year just to upload your own data.
1. Storage: Monthly forever. More data = more cost. It never stops.
> Cloud bills go UP every year. Hardware costs go DOWN. Over 3 years, owning always wins.
---
## 3-Year Total Cost -- Side by Side
```plain text
3-YEAR TOTAL COST -- 4 GPU RACKS

                    CLOUD (AWS)      EDGE (ADC 3K POD)
Year 1              $890,440         $720,000
Year 2              $945,440         $720,000
Year 3              $1,002,440       $720,000
                    ----------       ----------
3-YEAR TOTAL        $2,838,320       $2,160,000

SAVINGS WITH EDGE:  $678,320 (24% less)

Plus: data sovereignty, 5ms vs 200ms latency,
runs during outages, no vendor lock-in
```
---
## ADC Revenue Per Pod
```plain text
ADC 3K EDGE POD -- UNIT ECONOMICS

Monthly managed fee:        $60,000 (Tier 2)

Costs:
  Hardware depreciation      $12,000 (3-yr straight line)
  Power (nat gas $0.04/kWh)  $5,800 (200 kW continuous)
  NOC allocation              $3,000 (shared monitoring)
  Maintenance reserve         $2,000
  Insurance + misc            $1,200
Total cost:                  $24,000/mo

GROSS MARGIN:  $36,000/mo = 60%
ANNUAL GROSS PROFIT PER POD: $432,000

10 PODS DEPLOYED:
  Revenue:      $7,200,000/year
  Gross Profit: $4,320,000/year
  Margin:       60%
```
---
## Why Big Companies Choose Edge
### 1. Control
Your AI on someone else's computer = they control pricing, terms, access. Own the hardware = own your destiny.
### 2. Compliance
HIPAA, GDPR, CMMC, ITAR, SOX -- all have data residency rules. Edge solves compliance by default. Data physically cannot leave.
### 3. Speed
Self-driving trucks can't wait 200ms. Factory robots can't wait for AWS. Edge AI: under 10ms.
### 4. Resilience
Internet down? Cloud down. Grid fails? Connection fails. Edge pod with own power runs through hurricanes.
### 5. Competitive Advantage
Same cloud = same speed as competitors. Edge = dedicated compute nobody shares. Your models, your data, your moat.
---
## The Investor Pitch
```plain text
ADC 3K: EDGE AI INFRASTRUCTURE

The market is moving AI from the cloud
to the customer's doorstep.

We build the doorstep.

  Manufactured in Lafayette, LA
  Self-powered, self-cooled, remotely managed
  NVIDIA AI Enterprise certified
  60% gross margin per deployed pod
  $4.3M annual gross profit at 10 pods
  Customers: Oil & Gas, Defense, Healthcare

Your data never leaves your building.
Your AI never goes down.
```