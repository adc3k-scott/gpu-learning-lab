#!/usr/bin/env python3
"""Generate 5 SVG layout options for MARLIE 1 hybrid expansion plan."""

import os

OUTPUT_DIR = os.path.join(
    os.path.dirname(__file__), "..", "adc3k-deploy", "marlie", "blueprints"
)

# Dimensions
W, H = 1200, 900

# Colors
BG       = "#0a0a0f"
BUILDING = "#3b9eff"
GROUND   = "#00e87a"
STACKED  = "#00d4ff"
GENERATOR= "#f5a623"
COOLER   = "#4fc3f7"
BOUNDARY = "rgba(255,255,255,0.25)"
TEXT     = "#ffffff"
DIM      = "#888888"
GRID     = "rgba(255,255,255,0.04)"

FONT = "'IBM Plex Mono', 'Consolas', monospace"

# Scale: 1 ft = 3.5 px  (property ~160 ft fits nicely)
SCALE = 3.5

# Property rough: 0.60 acres ~ 26,136 sq ft.  Model as ~180 ft x 145 ft
PROP_W = 180
PROP_H = 145

# Building: 24 x 40 ft
BLDG_W = 24
BLDG_H = 40

# Container: 40 x 8 ft
CONT_W = 40
CONT_H = 8

# Generator pad: 20 x 10 ft each
GEN_W = 20
GEN_H = 10

# Cooler: 12 x 6 ft each
COOL_W = 12
COOL_H = 6


def px(ft):
    return ft * SCALE


def svg_header(title, subtitle):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>
  <style>
    text {{ font-family: {FONT}; }}
    .title {{ font-size: 18px; fill: {TEXT}; font-weight: 700; }}
    .subtitle {{ font-size: 12px; fill: {DIM}; }}
    .label {{ font-size: 10px; fill: {TEXT}; font-weight: 500; }}
    .label-sm {{ font-size: 8px; fill: {DIM}; }}
    .stat {{ font-size: 11px; fill: {TEXT}; }}
    .stat-val {{ font-size: 14px; fill: {GROUND}; font-weight: 700; }}
  </style>
</defs>
<rect width="{W}" height="{H}" fill="{BG}"/>

<!-- Title Block -->
<text x="40" y="40" class="title">{title}</text>
<text x="40" y="58" class="subtitle">{subtitle}</text>
<text x="40" y="74" class="subtitle">MARLIE 1 — 1201 SE Evangeline Thruway, Lafayette LA  |  0.60 acres (3 parcels)</text>
"""


def svg_footer():
    return "</svg>\n"


def north_arrow(x, y):
    return f"""<!-- North Arrow -->
<g transform="translate({x},{y})">
  <line x1="0" y1="20" x2="0" y2="-15" stroke="{TEXT}" stroke-width="1.5" marker-end="url(#arrowN)"/>
  <defs><marker id="arrowN" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto">
    <path d="M0,8 L4,0 L8,8 Z" fill="{TEXT}"/></marker></defs>
  <text x="0" y="-22" text-anchor="middle" class="label">N</text>
</g>
"""


def scale_bar(x, y):
    bar_len = px(40)
    return f"""<!-- Scale Bar -->
<g transform="translate({x},{y})">
  <line x1="0" y1="0" x2="{bar_len}" y2="0" stroke="{TEXT}" stroke-width="2"/>
  <line x1="0" y1="-4" x2="0" y2="4" stroke="{TEXT}" stroke-width="1.5"/>
  <line x1="{bar_len}" y1="-4" x2="{bar_len}" y2="4" stroke="{TEXT}" stroke-width="1.5"/>
  <text x="{bar_len/2}" y="14" text-anchor="middle" class="label-sm">40 ft</text>
</g>
"""


def stats_box(x, y, racks, gpus, containers, mw, footprint_label):
    return f"""<!-- Stats Box -->
<g transform="translate({x},{y})">
  <rect x="0" y="0" width="220" height="140" rx="6" fill="rgba(255,255,255,0.05)" stroke="rgba(255,255,255,0.15)" stroke-width="1"/>
  <text x="14" y="22" class="label" fill="{DIM}">DEPLOYMENT STATS</text>
  <line x1="14" y1="28" x2="206" y2="28" stroke="rgba(255,255,255,0.1)" stroke-width="0.5"/>
  <text x="14" y="46" class="stat">Total Racks:</text><text x="140" y="46" class="stat-val">{racks}</text>
  <text x="14" y="64" class="stat">Total GPUs:</text><text x="140" y="64" class="stat-val">{gpus:,}</text>
  <text x="14" y="82" class="stat">Containers:</text><text x="140" y="82" class="stat-val">{containers}</text>
  <text x="14" y="100" class="stat">IT Load:</text><text x="140" y="100" class="stat-val">{mw} MW</text>
  <text x="14" y="118" class="stat">Footprint:</text><text x="140" y="118" class="stat-val" style="font-size:10px">{footprint_label}</text>
</g>
"""


def legend(x, y):
    items = [
        (BUILDING, "MARLIE 1 Building (8 racks)"),
        (GROUND, "Ground Container (10 racks)"),
        (STACKED, "Stacked Container (10 racks)"),
        (GENERATOR, "Generator (Cat G3516J)"),
        (COOLER, "BAC Adiabatic Cooler"),
    ]
    parts = [f'<g transform="translate({x},{y})">']
    parts.append(f'<text x="0" y="0" class="label" fill="{DIM}">LEGEND</text>')
    for i, (color, label) in enumerate(items):
        yy = 16 + i * 18
        parts.append(f'<rect x="0" y="{yy}" width="12" height="10" rx="2" fill="{color}" opacity="0.85"/>')
        parts.append(f'<text x="18" y="{yy+9}" class="label-sm">{label}</text>')
    parts.append("</g>")
    return "\n".join(parts)


def property_boundary(ox, oy):
    w = px(PROP_W)
    h = px(PROP_H)
    return f"""<!-- Property Boundary -->
<rect x="{ox}" y="{oy}" width="{w}" height="{h}" rx="4"
      fill="none" stroke="{BOUNDARY}" stroke-width="1" stroke-dasharray="8,4"/>
<text x="{ox+6}" y="{oy+h-6}" class="label-sm" fill="{DIM}">Property Boundary (~0.60 acres)</text>
"""


def building(ox, oy, label="BUILDING\n8 RACKS INSIDE"):
    w = px(BLDG_W)
    h = px(BLDG_H)
    lines = label.split("\n")
    text_parts = ""
    for i, line in enumerate(lines):
        text_parts += f'<text x="{ox + w/2}" y="{oy + h/2 - 6 + i*14}" text-anchor="middle" class="label">{line}</text>\n'
    return f"""<!-- Building -->
<rect x="{ox}" y="{oy}" width="{w}" height="{h}" rx="4"
      fill="{BUILDING}" fill-opacity="0.18" stroke="{BUILDING}" stroke-width="1.5"/>
{text_parts}
<text x="{ox + w/2}" y="{oy - 6}" text-anchor="middle" class="label-sm">24 ft x 40 ft (2 floors)</text>
"""


def container_ground(ox, oy, label="ADC 3K"):
    w = px(CONT_W)
    h = px(CONT_H)
    return f"""<rect x="{ox}" y="{oy}" width="{w}" height="{h}" rx="3"
      fill="{GROUND}" fill-opacity="0.15" stroke="{GROUND}" stroke-width="1.2"/>
<text x="{ox + w/2}" y="{oy + h/2 + 3}" text-anchor="middle" class="label-sm" fill="{GROUND}">{label}</text>
"""


def container_stacked(ox, oy, label="ADC 3K"):
    """Stacked container with offset shadow effect."""
    w = px(CONT_W)
    h = px(CONT_H)
    off = 5  # shadow offset
    return f"""<!-- Stacked shadow -->
<rect x="{ox + off}" y="{oy - off}" width="{w}" height="{h}" rx="3"
      fill="{STACKED}" fill-opacity="0.08" stroke="{STACKED}" stroke-width="0.6" stroke-dasharray="3,2"/>
<!-- Stacked container -->
<rect x="{ox}" y="{oy}" width="{w}" height="{h}" rx="3"
      fill="{STACKED}" fill-opacity="0.2" stroke="{STACKED}" stroke-width="1.2"/>
<text x="{ox + w/2}" y="{oy + h/2 + 3}" text-anchor="middle" class="label-sm" fill="{STACKED}">{label} (2H)</text>
"""


def generator_pad(ox, oy, label="GEN"):
    w = px(GEN_W)
    h = px(GEN_H)
    return f"""<rect x="{ox}" y="{oy}" width="{w}" height="{h}" rx="3"
      fill="{GENERATOR}" fill-opacity="0.15" stroke="{GENERATOR}" stroke-width="1"/>
<text x="{ox + w/2}" y="{oy + h/2 + 3}" text-anchor="middle" class="label-sm" fill="{GENERATOR}">{label}</text>
"""


def cooler_unit(ox, oy, label="BAC"):
    w = px(COOL_W)
    h = px(COOL_H)
    return f"""<rect x="{ox}" y="{oy}" width="{w}" height="{h}" rx="2"
      fill="{COOLER}" fill-opacity="0.15" stroke="{COOLER}" stroke-width="1"/>
<text x="{ox + w/2}" y="{oy + h/2 + 3}" text-anchor="middle" class="label-sm" fill="{COOLER}">{label}</text>
"""


# ──────────────────────────────────────────────
# Layout A: Single Row, Ground Level
# ──────────────────────────────────────────────
def layout_a():
    svg = svg_header(
        "OPTION A — Single Row, Ground Level",
        "4 containers in a line behind the building | Easiest service access, lowest cost"
    )

    prop_x, prop_y = 60, 100
    svg += property_boundary(prop_x, prop_y)

    # Building front-left
    bx = prop_x + px(10)
    by = prop_y + px(15)
    svg += building(bx, by)

    # 4 containers in a row behind building
    cont_start_x = prop_x + px(10)
    cont_y = by + px(BLDG_H) + px(8)  # gap behind building
    for i in range(4):
        cx = cont_start_x + i * (px(CONT_W) + 6)
        svg += container_ground(cx, cont_y, f"POD {i+1}")

    # Footprint label
    fp_w = 4 * px(CONT_W) + 3 * 6
    svg += f'<text x="{cont_start_x + fp_w/2}" y="{cont_y + px(CONT_H) + 16}" text-anchor="middle" class="label-sm" fill="{DIM}">~160 ft x 10 ft container zone</text>'

    # Generators on right side
    gx = prop_x + px(PROP_W) - px(GEN_W) - px(8)
    gy = prop_y + px(15)
    for i in range(4):
        svg += generator_pad(gx, gy + i * (px(GEN_H) + 4), f"G3516J #{i+1}")

    # Coolers along right
    cx_cool = gx - px(COOL_W) - px(4)
    for i in range(3):
        svg += cooler_unit(cx_cool, gy + i * (px(COOL_H) + 4))

    svg += stats_box(940, 100, 48, 3456, 4, "~6.2", "160x10 ft")
    svg += legend(940, 260)
    svg += north_arrow(1140, 130)
    svg += scale_bar(60, 860)
    svg += svg_footer()
    return svg


# ──────────────────────────────────────────────
# Layout B: Single Row, 2-High Stacked
# ──────────────────────────────────────────────
def layout_b():
    svg = svg_header(
        "OPTION B — Single Row, 2-High Stacked",
        "2 ground + 2 stacked = 4 containers | Half footprint of Option A"
    )

    prop_x, prop_y = 60, 100
    svg += property_boundary(prop_x, prop_y)

    bx = prop_x + px(10)
    by = prop_y + px(15)
    svg += building(bx, by)

    # 2 ground containers
    cont_start_x = prop_x + px(10)
    cont_y = by + px(BLDG_H) + px(8)
    for i in range(2):
        cx = cont_start_x + i * (px(CONT_W) + 6)
        svg += container_ground(cx, cont_y, f"POD {i+1} (GND)")

    # 2 stacked on top (offset visual)
    stack_y = cont_y - px(3)  # slight upward offset for stacking visual
    for i in range(2):
        cx = cont_start_x + i * (px(CONT_W) + 6)
        svg += container_stacked(cx, stack_y, f"POD {i+3}")

    # Access platform between
    plat_x = cont_start_x + px(CONT_W) + 1
    svg += f"""<rect x="{plat_x - 8}" y="{stack_y - 8}" width="16" height="{px(CONT_H) + 16}" rx="1"
      fill="rgba(255,255,255,0.1)" stroke="rgba(255,255,255,0.3)" stroke-width="0.8"/>
<text x="{plat_x}" y="{stack_y - 12}" text-anchor="middle" class="label-sm" fill="{DIM}">ACCESS</text>
"""

    fp_w = 2 * px(CONT_W) + 6
    svg += f'<text x="{cont_start_x + fp_w/2}" y="{cont_y + px(CONT_H) + 16}" text-anchor="middle" class="label-sm" fill="{DIM}">~80 ft x 10 ft container zone</text>'

    # Generators
    gx = prop_x + px(PROP_W) - px(GEN_W) - px(8)
    gy = prop_y + px(15)
    for i in range(4):
        svg += generator_pad(gx, gy + i * (px(GEN_H) + 4), f"G3516J #{i+1}")

    # Coolers
    cx_cool = gx - px(COOL_W) - px(4)
    for i in range(3):
        svg += cooler_unit(cx_cool, gy + i * (px(COOL_H) + 4))

    svg += stats_box(940, 100, 48, 3456, 4, "~6.2", "80x10 ft")
    svg += legend(940, 260)
    svg += north_arrow(1140, 130)
    svg += scale_bar(60, 860)
    svg += svg_footer()
    return svg


# ──────────────────────────────────────────────
# Layout C: Double Row, Ground Level
# ──────────────────────────────────────────────
def layout_c():
    svg = svg_header(
        "OPTION C — Double Row, Ground Level",
        "2x2 arrangement | Shared cooling infrastructure in center aisle"
    )

    prop_x, prop_y = 60, 100
    svg += property_boundary(prop_x, prop_y)

    bx = prop_x + px(10)
    by = prop_y + px(10)
    svg += building(bx, by)

    # Row 1: 2 containers
    cont_start_x = prop_x + px(10)
    row1_y = by + px(BLDG_H) + px(8)
    for i in range(2):
        cx = cont_start_x + i * (px(CONT_W) + 6)
        svg += container_ground(cx, row1_y, f"POD {i+1}")

    # Center aisle with coolers
    aisle_y = row1_y + px(CONT_H) + px(3)
    aisle_w = 2 * px(CONT_W) + 6
    svg += f"""<rect x="{cont_start_x}" y="{aisle_y}" width="{aisle_w}" height="{px(6)}" rx="2"
      fill="rgba(79,195,247,0.06)" stroke="{COOLER}" stroke-width="0.5" stroke-dasharray="4,2"/>
<text x="{cont_start_x + aisle_w/2}" y="{aisle_y + px(3) + 3}" text-anchor="middle" class="label-sm" fill="{COOLER}">SHARED COOLING AISLE</text>
"""

    # Row 2: 2 containers
    row2_y = aisle_y + px(6) + px(3)
    for i in range(2):
        cx = cont_start_x + i * (px(CONT_W) + 6)
        svg += container_ground(cx, row2_y, f"POD {i+3}")

    fp_end = row2_y + px(CONT_H)
    svg += f'<text x="{cont_start_x + aisle_w/2}" y="{fp_end + 16}" text-anchor="middle" class="label-sm" fill="{DIM}">~80 ft x 25 ft container zone</text>'

    # Generators right side
    gx = prop_x + px(PROP_W) - px(GEN_W) - px(8)
    gy = prop_y + px(15)
    for i in range(4):
        svg += generator_pad(gx, gy + i * (px(GEN_H) + 4), f"G3516J #{i+1}")

    # Coolers near generators
    cx_cool = gx - px(COOL_W) - px(4)
    for i in range(3):
        svg += cooler_unit(cx_cool, gy + i * (px(COOL_H) + 4))

    svg += stats_box(940, 100, 48, 3456, 4, "~6.2", "80x25 ft")
    svg += legend(940, 260)
    svg += north_arrow(1140, 130)
    svg += scale_bar(60, 860)
    svg += svg_footer()
    return svg


# ──────────────────────────────────────────────
# Layout D: Double Row, 2-High Stacked
# ──────────────────────────────────────────────
def layout_d():
    svg = svg_header(
        'OPTION D — Double Row, 2-High Stacked',
        '2x2 ground + 2x2 stacked = 8 containers | Maximum density — "AI campus in a parking lot"'
    )

    prop_x, prop_y = 60, 100
    svg += property_boundary(prop_x, prop_y)

    bx = prop_x + px(10)
    by = prop_y + px(10)
    svg += building(bx, by)

    cont_start_x = prop_x + px(10)

    # Row 1 ground
    row1_y = by + px(BLDG_H) + px(8)
    for i in range(2):
        cx = cont_start_x + i * (px(CONT_W) + 6)
        svg += container_ground(cx, row1_y, f"POD {i+1} (GND)")

    # Row 1 stacked
    stack1_y = row1_y - px(3)
    for i in range(2):
        cx = cont_start_x + i * (px(CONT_W) + 6)
        svg += container_stacked(cx, stack1_y, f"POD {i+5}")

    # Center aisle
    aisle_y = row1_y + px(CONT_H) + px(3)
    aisle_w = 2 * px(CONT_W) + 6
    svg += f"""<rect x="{cont_start_x}" y="{aisle_y}" width="{aisle_w}" height="{px(6)}" rx="2"
      fill="rgba(79,195,247,0.06)" stroke="{COOLER}" stroke-width="0.5" stroke-dasharray="4,2"/>
<text x="{cont_start_x + aisle_w/2}" y="{aisle_y + px(3) + 3}" text-anchor="middle" class="label-sm" fill="{COOLER}">SHARED COOLING AISLE</text>
"""

    # Row 2 ground
    row2_y = aisle_y + px(6) + px(3)
    for i in range(2):
        cx = cont_start_x + i * (px(CONT_W) + 6)
        svg += container_ground(cx, row2_y, f"POD {i+3} (GND)")

    # Row 2 stacked
    stack2_y = row2_y - px(3)
    for i in range(2):
        cx = cont_start_x + i * (px(CONT_W) + 6)
        svg += container_stacked(cx, stack2_y, f"POD {i+7}")

    fp_end = row2_y + px(CONT_H)
    svg += f'<text x="{cont_start_x + aisle_w/2}" y="{fp_end + 16}" text-anchor="middle" class="label-sm" fill="{DIM}">~80 ft x 25 ft container zone</text>'

    # Generators
    gx = prop_x + px(PROP_W) - px(GEN_W) - px(8)
    gy = prop_y + px(15)
    for i in range(4):
        svg += generator_pad(gx, gy + i * (px(GEN_H) + 4), f"G3516J #{i+1}")

    # Extra generators for 8 containers
    for i in range(2):
        svg += generator_pad(gx, gy + (4 + i) * (px(GEN_H) + 4), f"G3516J #{i+5}")

    # Coolers
    cx_cool = gx - px(COOL_W) - px(4)
    for i in range(4):
        svg += cooler_unit(cx_cool, gy + i * (px(COOL_H) + 4))

    svg += stats_box(940, 100, 88, 6336, 8, "~11.4", "80x25 ft")
    svg += legend(940, 260)
    svg += north_arrow(1140, 130)
    svg += scale_bar(60, 860)

    # "AI campus in a parking lot" callout
    svg += f"""<g transform="translate(940,420)">
  <rect x="0" y="0" width="220" height="36" rx="4" fill="rgba(0,232,122,0.1)" stroke="{GROUND}" stroke-width="0.8"/>
  <text x="110" y="22" text-anchor="middle" class="label" fill="{GROUND}">AI CAMPUS IN A PARKING LOT</text>
</g>
"""

    svg += svg_footer()
    return svg


# ──────────────────────────────────────────────
# Layout E: L-Shape Around Building
# ──────────────────────────────────────────────
def layout_e():
    svg = svg_header(
        "OPTION E — L-Shape Around Building",
        "Containers wrap behind and beside building | Building remains command center"
    )

    prop_x, prop_y = 60, 100
    svg += property_boundary(prop_x, prop_y)

    # Building more centered to allow L-wrap
    bx = prop_x + px(40)
    by = prop_y + px(12)
    svg += building(bx, by)

    # 3 containers behind building (horizontal)
    cont_behind_x = prop_x + px(10)
    cont_behind_y = by + px(BLDG_H) + px(6)
    for i in range(3):
        cx = cont_behind_x + i * (px(CONT_W) + 6)
        svg += container_ground(cx, cont_behind_y, f"POD {i+1}")

    # 2 containers along right side of building (rotated = vertical placement)
    # These run parallel to the building's right side
    side_x = bx + px(BLDG_W) + px(6)
    side_y = by
    for i in range(2):
        cy = side_y + i * (px(CONT_W) + 6)
        # Rotated container: swap w/h visually (8 wide x 40 tall)
        cw = px(CONT_H)  # 8 ft width
        ch = px(CONT_W)  # 40 ft length
        svg += f"""<rect x="{side_x}" y="{cy}" width="{cw}" height="{ch}" rx="3"
      fill="{GROUND}" fill-opacity="0.15" stroke="{GROUND}" stroke-width="1.2"/>
<text x="{side_x + cw/2}" y="{cy + ch/2 + 3}" text-anchor="middle" class="label-sm" fill="{GROUND}">POD {i+4}</text>
"""

    # L-shape annotation
    svg += f"""<path d="M {cont_behind_x - 4} {cont_behind_y - 4}
               L {cont_behind_x - 4} {cont_behind_y + px(CONT_H) + 4}
               L {cont_behind_x + 3*(px(CONT_W)+6) + 4} {cont_behind_y + px(CONT_H) + 4}"
      fill="none" stroke="{DIM}" stroke-width="0.5" stroke-dasharray="4,3"/>
"""

    # Generators on far right
    gx = prop_x + px(PROP_W) - px(GEN_W) - px(6)
    gy = prop_y + px(15)
    for i in range(4):
        svg += generator_pad(gx, gy + i * (px(GEN_H) + 4), f"G3516J #{i+1}")

    # Coolers
    cx_cool = prop_x + px(6)
    cy_cool = prop_y + px(15)
    for i in range(3):
        svg += cooler_unit(cx_cool, cy_cool + i * (px(COOL_H) + 4))

    svg += stats_box(940, 100, 58, 4176, 5, "~7.5", "L-shape")
    svg += legend(940, 260)
    svg += north_arrow(1140, 130)
    svg += scale_bar(60, 860)
    svg += svg_footer()
    return svg


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    layouts = {
        "expansion-layout-a.svg": layout_a,
        "expansion-layout-b.svg": layout_b,
        "expansion-layout-c.svg": layout_c,
        "expansion-layout-d.svg": layout_d,
        "expansion-layout-e.svg": layout_e,
    }

    for fname, func in layouts.items():
        path = os.path.join(OUTPUT_DIR, fname)
        svg_content = func()
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg_content)
        size_kb = os.path.getsize(path) / 1024
        print(f"  Created: {fname} ({size_kb:.1f} KB)")

    print(f"\nAll 5 SVGs written to: {os.path.abspath(OUTPUT_DIR)}")


if __name__ == "__main__":
    main()
