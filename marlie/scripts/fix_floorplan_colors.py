"""
Fix floor plan: increase display size + improve color contrast/legibility.
"""
import re

with open(r"c:\Users\adhsc\OneDrive\Documents\GitHub\gpu-learning-lab\marlie\index.html", "r", encoding="utf-8") as f:
    html = f.read()

# ── 1. Increase SVG display size ─────────────────────────────────────────────
html = html.replace(
    'viewBox="0 0 590 490" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:590px;display:block;font-family:monospace;"',
    'viewBox="0 0 590 490" xmlns="http://www.w3.org/2000/svg" style="width:100%;display:block;font-family:monospace;"'
)

# ── 2. Color upgrades — all within the floor plan SVG ────────────────────────
# Map: old_color -> new_color (order matters — more specific first)

color_map = [
    # === EXTERIOR ZONES ===
    # Exterior background stays dark but text gets brighter
    ('"#3a3530" text-anchor="middle" letter-spacing="2">NORTH EXTERIOR',
     '"#a09060" text-anchor="middle" letter-spacing="2">NORTH EXTERIOR'),
    ('"#4a6050" text-anchor="middle" letter-spacing="1">▼  ENTRY DOOR',
     '"#80d090" text-anchor="middle" letter-spacing="1">▼  ENTRY DOOR'),
    ('"#2a4038" text-anchor="middle">RECEIVING',
     '"#60a070" text-anchor="middle">RECEIVING'),
    ('"#3a3530" text-anchor="middle" letter-spacing="2">SOUTH EXTERIOR',
     '"#a09060" text-anchor="middle" letter-spacing="2">SOUTH EXTERIOR'),

    # === CEILING STRIP ===
    ('"#4a4a38"', '"#9a9a68"'),

    # === COLD AISLES ===
    ('"#2a5070" text-anchor="middle" letter-spacing="2">↓', '"#60b0e0" text-anchor="middle" letter-spacing="2">↓'),
    ('"#1a3a50" text-anchor="middle">SHIPPING · EQUIPMENT STAGING',
     '"#50a0c0" text-anchor="middle">SHIPPING · EQUIPMENT STAGING'),
    ('"#102030" text-anchor="middle" letter-spacing="0.5">3 FT MIN WALL CLEARANCE',
     '"#406080" text-anchor="middle" letter-spacing="0.5">3 FT MIN WALL CLEARANCE'),
    ('"#2a5070" text-anchor="middle" letter-spacing="2">↑', '"#60b0e0" text-anchor="middle" letter-spacing="2">↑'),
    ('"#1a3a50" text-anchor="middle">SHIPPING · STAGING · RACK FRONT ACCESS',
     '"#50a0c0" text-anchor="middle">SHIPPING · STAGING · RACK FRONT ACCESS'),

    # === ROW LABELS ===
    ('"#1e2a14"', '"#3a5a28"'),   # row zone border
    ('"#3a6a3a" text-anchor="middle" letter-spacing="1">▼ FRONT FACE',
     '"#80d060" text-anchor="middle" letter-spacing="1">▼ FRONT FACE'),
    ('"#3a6a3a" text-anchor="middle" letter-spacing="1">▲ FRONT FACE',
     '"#80d060" text-anchor="middle" letter-spacing="1">▲ FRONT FACE'),

    # === STAGING POCKETS ===
    ('"#162010"', '"#2a4018"'),
    ('"#2a3a20" text-anchor="middle">STAGING', '"#70a050" text-anchor="middle">STAGING'),
    ('"#2a3a20" text-anchor="middle">WEST', '"#70a050" text-anchor="middle">WEST'),
    ('"#2a3a20" text-anchor="middle">EAST', '"#70a050" text-anchor="middle">EAST'),

    # === NVL72 RACK CELLS ===
    # Rack fill and border
    ('fill="#0c1a0c" stroke="#2a5a2a"', 'fill="#0f2a10" stroke="#50b050"'),
    # Rack labels A1-A8, B1-B8
    ('"#3a7a3a" text-anchor="middle" font-weight="bold"', '"#80f080" text-anchor="middle" font-weight="bold"'),
    # NVL72 sub-label
    ('"#2a5a2a" text-anchor="middle">NVL72', '"#50c050" text-anchor="middle">NVL72'),
    # GPU count
    ('"#1a4020" text-anchor="middle">72 GPU', '"#40a050" text-anchor="middle">72 GPU'),

    # === LIQUID MANIFOLD LINES ===
    ('stroke="#2a5a9a" stroke-width="2" stroke-dasharray="6,3"',
     'stroke="#50a0f0" stroke-width="2.5" stroke-dasharray="6,3"'),
    ('stroke="#8a2a2a" stroke-width="2" stroke-dasharray="6,3"',
     'stroke="#f05050" stroke-width="2.5" stroke-dasharray="6,3"'),

    # === HOT AISLE ===
    ('stroke="#3a1010" stroke-width="1.5" stroke-dasharray="8,3"',
     'stroke="#c02020" stroke-width="2" stroke-dasharray="8,3"'),
    # CDU boxes
    ('fill="#180808" stroke="#5a1a1a"', 'fill="#200c0c" stroke="#c03030"'),
    ('"#8a3030" text-anchor="middle" letter-spacing="1" font-weight="bold">CDU',
     '"#ff6060" text-anchor="middle" letter-spacing="1" font-weight="bold">CDU'),
    ('"#6a2020" text-anchor="middle">UNIT A', '"#e05050" text-anchor="middle">UNIT A'),
    ('"#4a1818" text-anchor="middle">LIQUID COOLING', '"#c04040" text-anchor="middle">LIQUID COOLING'),
    ('"#4a1818" text-anchor="middle">DISTRIBUTION', '"#c04040" text-anchor="middle">DISTRIBUTION'),
    ('"#6a2020" text-anchor="middle">UNIT B', '"#e05050" text-anchor="middle">UNIT B'),
    # Hot aisle label
    ('"#8a2020" text-anchor="middle" letter-spacing="3" font-weight="bold">HOT AISLE',
     '"#ff4040" text-anchor="middle" letter-spacing="3" font-weight="bold">HOT AISLE'),
    ('"#6a1818" text-anchor="middle" letter-spacing="1">SEALED CONTAINMENT',
     '"#e06060" text-anchor="middle" letter-spacing="1">SEALED CONTAINMENT'),
    ('"#4a1010" text-anchor="middle">← HOT LIQUID RETURN',
     '"#c05050" text-anchor="middle">← HOT LIQUID RETURN'),
    ('"#3a1010">⟵', '"#c05050">⟵'),
    ('"#3a1010">⟶', '"#c05050">⟶'),

    # === COOLANT LINES TO EXTERIOR ===
    ('stroke="#8a2a2a" stroke-width="2" stroke-dasharray="4,2"',
     'stroke="#f05050" stroke-width="2" stroke-dasharray="4,2"'),
    ('stroke="#2a5a9a" stroke-width="2" stroke-dasharray="4,2"',
     'stroke="#50a0f0" stroke-width="2" stroke-dasharray="4,2"'),

    # === EXTERIOR MECHANICAL ===
    # Dry coolers
    ('fill="#060e06" stroke="#1a3a1a"', 'fill="#081808" stroke="#40a040"'),
    ('"#2a6a2a" text-anchor="middle" letter-spacing="0.5">DRY COOLER',
     '"#70e070" text-anchor="middle" letter-spacing="0.5">DRY COOLER'),
    ('"#1a4a1a" text-anchor="middle">CDU HEAT REJECTION',
     '"#50b050" text-anchor="middle">CDU HEAT REJECTION'),
    # Generators
    ('fill="#100a06" stroke="#3a1a08"', 'fill="#180e06" stroke="#c05020"'),
    ('"#8a4020" text-anchor="middle" letter-spacing="0.5">GENERATORS',
     '"#f08040" text-anchor="middle" letter-spacing="0.5">GENERATORS'),
    ('"#5a2a10" text-anchor="middle">NAT. GAS — N+1',
     '"#d07040" text-anchor="middle">NAT. GAS — N+1'),
    ('"#3a1a08" text-anchor="middle">PRIMARY POWER',
     '"#b06030" text-anchor="middle">PRIMARY POWER'),
    # UPS
    ('fill="#080810" stroke="#18183a"', 'fill="#0a0a18" stroke="#5060c0"'),
    ('"#304070" text-anchor="middle" letter-spacing="0.5">UPS BATTERY',
     '"#7090e0" text-anchor="middle" letter-spacing="0.5">UPS BATTERY'),
    ('"#202850" text-anchor="middle">BACKUP POWER',
     '"#5070c0" text-anchor="middle">BACKUP POWER'),
    ('"#181830" text-anchor="middle">RIDE-THROUGH',
     '"#4060a0" text-anchor="middle">RIDE-THROUGH'),
    # Bloom Energy
    ('fill="#0a0810" stroke="#2a1a3a"', 'fill="#100a18" stroke="#8040c0"'),
    ('"#603080" text-anchor="middle" letter-spacing="0.5">BLOOM ENERGY',
     '"#c070f0" text-anchor="middle" letter-spacing="0.5">BLOOM ENERGY'),
    ('"#402060" text-anchor="middle">FUEL CELL — 300 kW',
     '"#a050e0" text-anchor="middle">FUEL CELL — 300 kW'),
    ('"#2a1040" text-anchor="middle">ON-SITE GENERATION',
     '"#8040c0" text-anchor="middle">ON-SITE GENERATION'),

    # === LEGEND ===
    ('"#2a5a9a">COLD LIQUID SUPPLY', '"#50a0f0">COLD LIQUID SUPPLY'),
    ('"#8a2a2a">HOT LIQUID RETURN', '"#f05050">HOT LIQUID RETURN'),
    ('"#3a7a3a">NVL72 RACK', '"#70e070">NVL72 RACK'),
    ('"#8a3030">CDU — COOLANT', '"#ff6060">CDU — COOLANT'),

    # === DIMENSION LABELS ===
    ('"#4a4040"', '"#808070"'),   # dimension lines
    ('"#6a5a40" text-anchor="middle" letter-spacing="1">35 FT',
     '"#d4a843" text-anchor="middle" letter-spacing="1">35 FT'),
    ('"#6a5a40" text-anchor="middle" transform="rotate(-90,18,200)">22 FT',
     '"#d4a843" text-anchor="middle" transform="rotate(-90,18,200)">22 FT'),
    ('"#4a2020"', '"#a04040"'),   # inner hot aisle dimension lines
    ('"#6a3030"', '"#d06060"'),   # inner hot aisle label
]

for old, new in color_map:
    html = html.replace(old, new)

with open(r"c:\Users\adhsc\OneDrive\Documents\GitHub\gpu-learning-lab\marlie\index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Done.")
