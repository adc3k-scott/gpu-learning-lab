# ADC Site Scoring System v2 — Summary
Last updated: 2026-03-25
Full criteria: data/site-scoring-criteria.md
Score data: data/site_scores.json
Scoring engine: agents/site_scout/scorer_v2.py

## Scoring Variables (100 pts base + 24 pts bonus = 124 max)

### Base Variables (10 pts each, 100 max)
1. Gas pipeline proximity (0-5 mi = 10)
2. Water access for cooling (adjacent = 10)
3. Flood zone (Zone X = 10)
4. Foundation type (slab on grade = 10)
5. Electrical grid proximity (substation <1 mi = 10)
6. Fiber optic proximity (lit fiber <0.5 mi = 10)
7. Road access (highway frontage = 10)
8. Rail access (on-site = 10)
9. Zoning (industrial = 10)
10. Acquisition cost (<$500K = 10)

### Bonus Variables
- Historic tax credit eligible (+5)
- Brownfield/EPA eligible (+5)
- University within 5 miles (+5)
- Existing structure (+3)
- Municipal utility (LUS vs Entergy) (+3)
- Port/dock access (+3)

## Tier System
| Tier | Base Score | Description |
|------|-----------|-------------|
| S | 90-100 | Deploy immediately |
| A | 75-89 | Strong candidate |
| B | 60-74 | Viable with investment |
| C | 45-59 | Marginal |
| D | <45 | Not viable |

## Reference Site Scores

| Site | Base | Bonus | Total | Tier |
|------|------|-------|-------|------|
| Willow Glen Terminal | 94 | 11 | 105 | S |
| Trappeys Cannery | 84 | 21 | 105 | S |
| MARLIE 1 | 89 | 8 | 97 | S |
| KLFT Airport | 74 | 11 | 85 | A |

Trappeys and Willow Glen TIE at 105 total — different reasons:
- Willow Glen: highest base (94) — on-site everything
- Trappeys: highest bonus (21) — historic credits, brownfield, UL Lafayette, existing structures, municipal utility

## Key Findings
- Most of Evangeline Thruway corridor is Zone X (minimal flood)
- Zone AE only along Vermilion River bank itself
- 18 of 31 scout sites need flood zone verification
- 5 scout sites likely upgrade to Tier A with expanded bonus scoring
- New Iberia I-1 duplicate in both pipeline and river databases — needs merge
