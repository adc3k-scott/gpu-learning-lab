# Louisiana Fiber Infrastructure — ADC Sites
Last updated: 2026-03-25

## Primary: LFT Fiber (Municipal)
- Rebranded from LUS Fiber in 2025. 100% fiber, municipally owned.
- Covers ALL of Lafayette including SE Evangeline Thruway
- Enterprise DIA up to 25 Gbps symmetric
- Point-to-point and dark fiber available
- Trappeys-to-MARLIE (0.5 mi) = standard P2P, trivial
- KLFT already has active LFT Fiber partnership (1 Gbps)
- Does NOT extend to Iberville Parish (can't reach Willow Glen)
- Contact: (337) 993-4237 | lftfiber.com/business-solutions

## Strategic: LONI (Louisiana Optical Network Initiative)
- Lafayette is one of ONLY 4 LONI core sites (+ BR, Shreveport, Jackson MS)
- 1,600+ miles backbone, upgrading to 400G optical
- UL Lafayette is a LONI member (supercomputer "Zeke" in Abdalla Hall)
- LONI allows industry partner access through member institutions
- Trappeys is 0.5 mi from UL Lafayette = direct peer with LONI core
- UL partnership = LONI access = 400G to every university + Internet2
- Contact: manager@institute.loni.org | ED: Lonnie Leger

## Lafayette to Willow Glen (60 mi)
- I-10 corridor = most fiber-dense route in LA outside NOLA
- Zayo: largest US dark fiber (133K route miles), on I-10
- Lumen: 450K route miles, Louisiana-based, on I-10
- Approach: dark fiber lease I-10 (45 mi) + last-mile build (15 mi)
- IRU: $180-300K/strand (20-yr) | Monthly: $900-1,800/strand
- Lit 100G wavelength: $5-15K/mo
- Latency: 60 mi = 1-2ms one-way, 2-4ms round-trip

## Redundancy Carriers
- AT&T: enterprise DIA up to 1 Tbps, long-haul on I-10. Contact: 877-818-4079
- Cox Business: up to 1 Gbps + LTE backup. Third-path diversity.
- REV (formerly EATEL): 5,000+ mi fiber, 11 parishes. NOT Lafayette but useful BR-side for WG.

## Recommended Multi-Path Architecture
```
Path 1 (Primary):    LFT Fiber 25G DIA
Path 2 (Redundant):  AT&T Dedicated Internet
Path 3 (Research):   LONI via UL Lafayette (400G backbone + Internet2)
Path 4 (Inter-site): Dark fiber Zayo/Lumen (Lafayette <-> Willow Glen)
Path 5 (Diverse):    Cox Business (separate last-mile)
```

## Grants
- Louisiana $1.355B BEAD allocation (first state approved Nov 2025)
- $1B federal Middle Mile program
- ConnectLA (connect.la.gov) coordinating body

## First 3 Calls
1. LFT Fiber (337) 993-4237 — Enterprise DIA + P2P quote
2. LONI manager@institute.loni.org — Industry partner access via UL Lafayette
3. Zayo zayo.com/network — Dark fiber I-10 availability
