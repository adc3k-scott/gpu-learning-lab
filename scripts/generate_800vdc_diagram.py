#!/usr/bin/env python3
"""Generate the ADC 800V DC Power Architecture SVG diagram.

Outputs: adc3k-deploy/shared/site-images/800vdc-power-chain.svg
"""

import os

# ── Dimensions ──────────────────────────────────────────────────────────
W, H = 1920, 1200
BG = "#0a0a0f"
GRID_TEXT = "#888"

# ── Vendor Colors ───────────────────────────────────────────────────────
C_EATON   = "#76b900"
C_DELTA   = "#00bcd4"
C_ABB     = "#3b9eff"
C_TI      = "#f5a623"
C_NVIDIA  = "#00e87a"
C_COOL    = "#4fc3f7"
C_CAT_SOL = "#ffffff"
C_ARROW   = "#aaaaaa"
C_LABEL   = "#cccccc"
C_VOLT    = "#ffdd57"
C_EFF     = "#ff6b6b"
C_SECTION = "#ffffff"

# ── Helpers ─────────────────────────────────────────────────────────────
def rect(x, y, w, h, fill, rx=6):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" fill-opacity="0.15" stroke="{fill}" stroke-width="1.5"/>'

def text(x, y, label, fill="#fff", size=12, anchor="middle", weight="normal"):
    return f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" font-family="Inter,Segoe UI,Arial,sans-serif">{label}</text>'

def arrow_down(x, y1, y2, color=C_ARROW):
    mid = (y1 + y2) / 2
    return (
        f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{color}" stroke-width="1.5" marker-end="url(#ah)"/>'
    )

def arrow_right(x1, x2, y, color=C_ARROW):
    return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{color}" stroke-width="1.5" marker-end="url(#ah)"/>'

def arrow_elbow_right_down(x1, y1, x2, y2, color=C_ARROW):
    """Right then down elbow."""
    return f'<polyline points="{x1},{y1} {x2},{y1} {x2},{y2}" fill="none" stroke="{color}" stroke-width="1.5" marker-end="url(#ah)"/>'

def arrow_elbow_down_right(x1, y1, x2, y2, color=C_ARROW):
    """Down then right elbow."""
    return f'<polyline points="{x1},{y1} {x1},{y2} {x2},{y2}" fill="none" stroke="{color}" stroke-width="1.5" marker-end="url(#ah)"/>'

def voltage_label(x, y, label):
    return text(x, y, label, fill=C_VOLT, size=10, weight="bold")

def eff_label(x, y, label):
    return text(x, y, label, fill=C_EFF, size=10)

def block(x, y, w, h, fill, lines, sub_lines=None):
    """Draw a colored block with centered text lines."""
    parts = [rect(x, y, w, h, fill)]
    # Main label lines
    total_lines = len(lines) + (len(sub_lines) if sub_lines else 0)
    line_h = 15
    start_y = y + h/2 - (total_lines - 1) * line_h / 2 + 4
    for i, line in enumerate(lines):
        parts.append(text(x + w/2, start_y + i * line_h, line, fill="#fff", size=12, weight="bold"))
    if sub_lines:
        for j, sl in enumerate(sub_lines):
            parts.append(text(x + w/2, start_y + (len(lines) + j) * line_h, sl, fill=fill, size=10))
    return "\n".join(parts)


# ── Build SVG ───────────────────────────────────────────────────────────
parts = []

# Defs
parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>
  <marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
    <path d="M 0 0 L 10 5 L 0 10 z" fill="{C_ARROW}"/>
  </marker>
  <marker id="ah-cool" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
    <path d="M 0 0 L 10 5 L 0 10 z" fill="{C_COOL}"/>
  </marker>
</defs>
<rect width="{W}" height="{H}" fill="{BG}"/>''')

# ── Title ───────────────────────────────────────────────────────────────
parts.append(text(W/2, 36, "ADC 800V DC Power Architecture — Complete Vendor Stack", "#fff", 22, weight="bold"))
parts.append(text(W/2, 58, "From Gas Molecule to GPU Chip — Every Component, Every Vendor", C_LABEL, 14))

# ── Section backgrounds ────────────────────────────────────────────────
# Facility level
parts.append(f'<rect x="30" y="80" width="1260" height="470" rx="10" fill="#76b900" fill-opacity="0.04" stroke="{C_EATON}" stroke-width="0.5" stroke-dasharray="6,4"/>')
parts.append(text(660, 100, "FACILITY LEVEL  (Eaton + Partners)", C_EATON, 14, weight="bold"))

# Rack level
parts.append(f'<rect x="30" y="565" width="1260" height="480" rx="10" fill="#00bcd4" fill-opacity="0.04" stroke="{C_DELTA}" stroke-width="0.5" stroke-dasharray="6,4"/>')
parts.append(text(660, 585, "RACK LEVEL  (Delta + Partners)", C_DELTA, 14, weight="bold"))

# Cooling chain
parts.append(f'<rect x="1320" y="80" width="570" height="965" rx="10" fill="#4fc3f7" fill-opacity="0.04" stroke="{C_COOL}" stroke-width="0.5" stroke-dasharray="6,4"/>')
parts.append(text(1605, 100, "COOLING CHAIN  (Parallel)", C_COOL, 14, weight="bold"))

# ═══════════════════════════════════════════════════════════════════════
# FACILITY LEVEL
# ═══════════════════════════════════════════════════════════════════════

BX = 60   # left column x
BW = 260  # block width
BH = 60   # block height

# Row 1: Sources
# Gas pipeline -> Generator
parts.append(block(BX, 120, 220, BH, C_CAT_SOL,
    ["ATMOS Gas Pipeline"],
    ["Henry Hub · 13 pipelines"]))

parts.append(arrow_right(BX+220, BX+260, 150))

parts.append(block(BX+260, 120, BW, BH, C_CAT_SOL,
    ["Cat G3516J Generator"],
    ["1.6 MW · 480V AC 3-phase"]))
parts.append(voltage_label(BX+260+BW/2, 190, "480V AC"))

# Solar -> Buck converter
parts.append(block(BX, 220, 220, BH, C_CAT_SOL,
    ["First Solar Series 7 TR1"],
    ["550W · 5-panel string @ 952V DC"]))
parts.append(voltage_label(BX+110, 290, "952V DC"))

parts.append(arrow_right(BX+220, BX+260, 250))

parts.append(block(BX+260, 220, BW, BH, C_TI,
    ["TI GaN Buck Converter"],
    ["952V → 800V · SiC/GaN"]))
parts.append(voltage_label(BX+260+BW/2, 290, "800V DC"))
parts.append(eff_label(BX+260+BW+10, 255, "~97%"))

# Both feed into switchgear — arrows converge
# Generator arrow down
GEN_CX = BX + 260 + BW/2  # center of generator
SOLAR_CX = BX + 260 + BW/2  # center of buck (same column)
SW_X = 370  # switchgear x
SW_CX = SW_X + BW/2

parts.append(arrow_down(GEN_CX, 180, 220))

# Switchgear
parts.append(block(SW_X, 310, BW, BH, C_EATON,
    ["Eaton MV Switchgear"],
    ["Medium voltage distribution"]))
parts.append(arrow_down(SW_CX, 280, 310))

# Beam Rubin DSX Rectifier
parts.append(block(SW_X, 395, BW, BH, C_EATON,
    ["Eaton Beam Rubin DSX"],
    ["Rectifier · 480V AC → 800V DC"]))
parts.append(arrow_down(SW_CX, 370, 395))
parts.append(voltage_label(SW_CX, 465, "800V DC"))
parts.append(eff_label(SW_X + BW + 10, 430, "97% eff"))

# ABB SACE Infinitus
ABB_X = 700
parts.append(block(ABB_X, 310, BW, BH, C_ABB,
    ["ABB SACE Infinitus"],
    ["Solid-state DC breaker · <3ms"]))
parts.append(arrow_right(SW_X + BW, ABB_X, 340))
parts.append(voltage_label(ABB_X + BW/2, 380, "800V DC (protected)"))

# Eaton ORV3 Sidecar
ORV_X = 700
parts.append(block(ORV_X, 395, BW, BH, C_EATON,
    ["Eaton ORV3 Sidecar"],
    ["±400V DC · 800 kW/row"]))
parts.append(arrow_down(ABB_X + BW/2, 370, 395))
parts.append(voltage_label(ORV_X + BW/2, 465, "±400V DC"))

# Eaton xStorage BESS
BESS_X = 700
parts.append(block(BESS_X, 480, BW, BH, C_EATON,
    ["Eaton xStorage BESS"],
    ["761-1200 VDC · Microgrid buffer"]))
parts.append(arrow_down(ORV_X + BW/2, 455, 480))

# ═══════════════════════════════════════════════════════════════════════
# RACK LEVEL
# ═══════════════════════════════════════════════════════════════════════

RX = 120  # rack column x
RW = 280

# Connecting arrow from facility to rack
parts.append(f'<line x1="{ORV_X + BW/2}" y1="{540}" x2="{RX + RW/2}" y2="{605}" stroke="{C_ARROW}" stroke-width="1.5" stroke-dasharray="6,3" marker-end="url(#ah)"/>')
parts.append(voltage_label((ORV_X + BW/2 + RX + RW/2)/2, 570, "800V DC Bus"))

# Delta Power Rack
parts.append(block(RX, 610, RW, 70, C_DELTA,
    ["Delta 660 kW Power Rack"],
    ["6× 110 kW shelves", "480 kW embedded BBU"]))
parts.append(eff_label(RX + RW + 10, 650, "98% AC-DC"))

# Delta e-Fuse
parts.append(arrow_down(RX + RW/2, 680, 710))
parts.append(block(RX, 710, RW, BH, C_DELTA,
    ["Delta e-Fuse (SiC)"],
    ["<3 μs fault cutoff"]))

# Delta DC/DC Shelf
parts.append(arrow_down(RX + RW/2, 770, 800))
parts.append(voltage_label(RX + RW/2, 795, "800V → 50V"))
parts.append(block(RX, 800, RW, BH, C_DELTA,
    ["Delta 90 kW DC/DC Shelf"],
    ["800V → 50V · NVIDIA MGX"]))
parts.append(eff_label(RX + RW + 10, 835, "98.5% eff"))

# TI + Infineon VRM
parts.append(arrow_down(RX + RW/2, 860, 890))
parts.append(block(RX - 30, 890, RW + 60, 70, C_TI,
    ["TI 800V-to-6V GaN (97.6% eff)"],
    ["Infineon CoolGaN IBC", "800V → 50V (>98% eff)"]))

# NVIDIA NVL72
parts.append(arrow_down(RX + RW/2, 960, 990))
parts.append(voltage_label(RX + RW/2, 985, "800V → 12V (64:1 LLC)"))
parts.append(block(RX - 30, 990, RW + 60, 70, C_NVIDIA,
    ["NVIDIA NVL72 Rack"],
    ["72 Blackwell GPUs · 130 kW", "On-chip LLC converter 800V → 12V"]))

# Voltage labels along right side of rack chain
VLX = RX + RW + 80
parts.append(text(VLX, 645, "800V DC", C_VOLT, 11, "start", "bold"))
parts.append(text(VLX, 745, "800V DC", C_VOLT, 11, "start", "bold"))
parts.append(text(VLX, 835, "50V DC", C_VOLT, 11, "start", "bold"))
parts.append(text(VLX, 930, "6-50V DC", C_VOLT, 11, "start", "bold"))
parts.append(text(VLX, 1030, "12V → GPU die", C_VOLT, 11, "start", "bold"))

# ═══════════════════════════════════════════════════════════════════════
# COOLING CHAIN (right side)
# ═══════════════════════════════════════════════════════════════════════

CX = 1370
CW = 480
CH = 75

# BAC Adiabatic Cooler
parts.append(block(CX, 140, CW, CH, C_COOL,
    ["BAC TrilliumSeries Adiabatic Cooler"],
    ["External · optimized for Louisiana humidity", "Dry operation >80% of year"]))

# Arrow down
parts.append(arrow_down(CX + CW/2, 215, 270))
parts.append(text(CX + CW/2, 248, "Facility water loop", C_COOL, 10))

# CoolIT CDU
parts.append(block(CX, 270, CW, CH, C_COOL,
    ["CoolIT CHx2000 CDU"],
    ["2,000 kW row-level cooling", "Staubli UQD quick-disconnect couplings"]))

# Arrow down
parts.append(arrow_down(CX + CW/2, 345, 400))
parts.append(text(CX + CW/2, 378, "Rack cooling loop", C_COOL, 10))

# Delta In-Rack CDU
parts.append(block(CX, 400, CW, CH, C_DELTA,
    ["Delta 140 kW In-Rack CDU"],
    ["4 RU · NVL72 certified", "Rack-level liquid distribution"]))

# Arrow down
parts.append(arrow_down(CX + CW/2, 475, 530))
parts.append(text(CX + CW/2, 508, "Chip-level cooling", C_COOL, 10))

# NVIDIA cooling manifolds
parts.append(block(CX, 530, CW, CH, C_NVIDIA,
    ["NVIDIA NVL72 Cooling Manifolds"],
    ["45°C supply → 55-65°C return", "Direct-to-chip liquid cooling"]))

# Temperature labels
parts.append(text(CX + CW/2, 640, "Temperature Cascade", "#fff", 13, weight="bold"))
parts.append(text(CX + 60, 665, "External ambient:", C_LABEL, 11, "start"))
parts.append(text(CX + 280, 665, "35°C (Louisiana peak)", C_COOL, 11, "start"))
parts.append(text(CX + 60, 685, "Facility water supply:", C_LABEL, 11, "start"))
parts.append(text(CX + 280, 685, "30-35°C", C_COOL, 11, "start"))
parts.append(text(CX + 60, 705, "Rack water supply:", C_LABEL, 11, "start"))
parts.append(text(CX + 280, 705, "40-45°C", C_COOL, 11, "start"))
parts.append(text(CX + 60, 725, "GPU junction:", C_LABEL, 11, "start"))
parts.append(text(CX + 280, 725, "75-85°C (max 90°C)", "#ff6b6b", 11, "start"))
parts.append(text(CX + 60, 745, "Return water:", C_LABEL, 11, "start"))
parts.append(text(CX + 280, 745, "55-65°C → waste heat recovery", C_COOL, 11, "start"))

# ── Efficiency waterfall ────────────────────────────────────────────────
EWX = CX + 20
EWY = 790
parts.append(f'<rect x="{CX}" y="{EWY - 10}" width="{CW}" height="190" rx="8" fill="#ff6b6b" fill-opacity="0.05" stroke="#ff6b6b" stroke-width="0.5"/>')
parts.append(text(CX + CW/2, EWY + 10, "END-TO-END EFFICIENCY", "#ff6b6b", 13, weight="bold"))

steps = [
    ("Gas → Electricity (Cat G3516J)", "42%", "0.42"),
    ("AC → DC Rectifier (Eaton Beam)", "97%", "0.97"),
    ("DC Breaker (ABB SACE)", "99.9%", "0.999"),
    ("Row PDU (Eaton ORV3)", "99.5%", "0.995"),
    ("Power Rack (Delta 660 kW)", "98%", "0.98"),
    ("DC/DC Shelf (Delta 90 kW)", "98.5%", "0.985"),
    ("VRM to chip (TI/Infineon)", "97.6%", "0.976"),
]
for i, (label, pct, _) in enumerate(steps):
    y = EWY + 30 + i * 20
    parts.append(text(EWX + 10, y, label, C_LABEL, 10, "start"))
    parts.append(text(CX + CW - 20, y, pct, C_EFF, 10, "end", "bold"))

# Combined
parts.append(f'<line x1="{EWX}" y1="{EWY + 175}" x2="{CX + CW - 20}" y2="{EWY + 175}" stroke="#ff6b6b" stroke-width="0.5"/>')
parts.append(text(EWX + 10, EWY + 190, "Combined electrical path (post-gen):", "#fff", 11, "start", "bold"))
parts.append(text(CX + CW - 20, EWY + 190, "~91%", "#ff6b6b", 13, "end", "bold"))

# Solar path note
parts.append(text(CX + CW/2, EWY + 215, "Solar DC-direct path: ~95% (no AC conversion)", C_EATON, 10))

# ── Legend ──────────────────────────────────────────────────────────────
LX = 60
LY = 1080
LW = 1200
LH = 90
parts.append(f'<rect x="{LX}" y="{LY}" width="{LW}" height="{LH}" rx="8" fill="#ffffff" fill-opacity="0.03" stroke="#444" stroke-width="0.5"/>')
parts.append(text(LX + LW/2, LY + 18, "VENDOR COLOR LEGEND", "#fff", 12, weight="bold"))

legend_items = [
    (C_EATON, "Eaton (Distribution)"),
    (C_DELTA, "Delta (Rack Power + Cooling)"),
    (C_ABB, "ABB (Protection)"),
    (C_TI, "TI / Infineon (VRM)"),
    (C_NVIDIA, "NVIDIA (Compute + Cooling)"),
    (C_COOL, "CoolIT / BAC (Cooling)"),
    (C_CAT_SOL, "Cat / First Solar (Generation)"),
]
cols = 4
col_w = LW // cols
for i, (color, label) in enumerate(legend_items):
    col = i % cols
    row = i // cols
    lx = LX + 20 + col * col_w
    ly = LY + 40 + row * 24
    parts.append(f'<rect x="{lx}" y="{ly - 10}" width="14" height="14" rx="3" fill="{color}" fill-opacity="0.3" stroke="{color}" stroke-width="1"/>')
    parts.append(text(lx + 22, ly + 2, label, C_LABEL, 11, "start"))

# ── Footer ──────────────────────────────────────────────────────────────
parts.append(text(W/2, H - 12, "ADC 3K — Advantage Design & Construction · adc3k.com · 2026", "#555", 10))

# Close SVG
parts.append("</svg>")

# ── Write file ──────────────────────────────────────────────────────────
svg = "\n".join(parts)
out_dir = os.path.join(os.path.dirname(__file__), "..", "adc3k-deploy", "shared", "site-images")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "800vdc-power-chain.svg")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(svg)
print(f"Written {len(svg):,} bytes -> {os.path.abspath(out_path)}")
