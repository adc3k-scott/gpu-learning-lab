# Solid-State Transformer Comparison — ADC
Last updated: 2026-03-25

## Why SSTs Matter
Traditional: Utility MV (13.8-34.5kV AC) -> transformer -> 480V AC -> rectifier -> 800V DC = 88-92% efficiency
SST: Utility MV -> SST -> 800V DC direct = 97-99% efficiency
At 100 MW, 5% savings = 5 MW = $2-3M/year in fuel costs

## Vendor Comparison

| Company | Rating | Efficiency | Status | Risk | ADC Fit |
|---------|--------|-----------|--------|------|---------|
| Delta Electronics | ~1-5 MW | 98.5% | Established OEM, shipping | Low | Safest bet |
| Heron Power | 4.2 MW | 98.5% | $140M Series B (a16z) | Medium | Good for phased WG |
| Amperesand | 30 MW | TBD | $80M Series A, shipping 2026 | High | 3 units = Willow Glen |
| SolarEdge+Infineon | 2-5 MW | >99% | Joint venture, verify financial health | Medium-High | Trappeys/MARLIE |
| Navitas/EPFL | 250 kW | ~97-98% | Lab demo APEC 2026 | High | Edge only, 2028+ |

## Action Items
1. Contact Delta first — ask for MV-to-800V DC SST product SKU and lead time
2. Contact Heron Power — ask for pilot slots 2026-2027
3. Monitor Amperesand — get on early access list
4. Verify SolarEdge financial viability before investing time
5. Watch Navitas/EPFL — too early for our needs

## Key Questions for Every SST Vendor
- Input voltage: 13.8 kV or 34.5 kV?
- Output: 800V DC, NVIDIA DSX compatible?
- Fault isolation in a stack?
- UL/IEEE certification?
- US manufacturing?
- NVIDIA validation?
- Pilot at Louisiana site 2026-2027?
