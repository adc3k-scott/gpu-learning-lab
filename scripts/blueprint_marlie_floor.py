"""
MARLIE I — Lafayette AI Factory & Command Center
Floor Plans: Downstairs + Upstairs Side by Side
Each floor: 24x37 usable (3 ft staircase), 4 NVL72 racks, CDU pair, hot/cold aisle
"""
import svgwrite

W, H = 1400, 950
OUT = "adc3k-deploy/blueprints/marlie-floor-plan.svg"

ACCENT = "#3b82f6"

# Building dimensions
BLDG_W_FT = 24  # width
BLDG_H_FT = 40  # depth
USABLE_W_FT = 21  # minus 3 ft staircase
USABLE_H_FT = 37  # adjusted for notes
STAIR_W_FT = 3

SCALE = 8  # 1 ft = 8 px (large for detail)
BLDG_W = int(BLDG_W_FT * SCALE)
BLDG_H = int(BLDG_H_FT * SCALE)


def box(dwg, x, y, w, h, label="", color="#1a1a2e", border="#3b82f6", text_color="#e0e0e0", font=9):
    dwg.add(dwg.rect((x, y), (w, h), fill=color, stroke=border, stroke_width=1))
    if label:
        lines = label.split("\n")
        for i, line in enumerate(lines):
            ty = y + h / 2 - (len(lines) - 1) * 6 + i * 12
            dwg.add(dwg.text(line, insert=(x + w / 2, ty), text_anchor="middle",
                              fill=text_color, font_size=font, font_family="Arial",
                              font_weight="bold" if i == 0 else "normal"))


def dim_line(dwg, x1, y1, x2, y2, label, offset=15):
    if y1 == y2:
        dy = offset
        dwg.add(dwg.line((x1, y1 + dy), (x2, y2 + dy), stroke="#555", stroke_width=0.5))
        dwg.add(dwg.line((x1, y1 + dy - 4), (x1, y1 + dy + 4), stroke="#555", stroke_width=0.5))
        dwg.add(dwg.line((x2, y2 + dy - 4), (x2, y2 + dy + 4), stroke="#555", stroke_width=0.5))
        dwg.add(dwg.text(label, insert=((x1 + x2) / 2, y1 + dy - 3), text_anchor="middle",
                          fill="#888", font_size=7, font_family="Arial"))
    else:
        dx = offset
        dwg.add(dwg.line((x1 + dx, y1), (x2 + dx, y2), stroke="#555", stroke_width=0.5))
        dwg.add(dwg.line((x1 + dx - 4, y1), (x1 + dx + 4, y1), stroke="#555", stroke_width=0.5))
        dwg.add(dwg.line((x2 + dx - 4, y2), (x2 + dx + 4, y2), stroke="#555", stroke_width=0.5))
        dwg.add(dwg.text(label, insert=(x1 + dx + 5, (y1 + y2) / 2), fill="#888",
                          font_size=7, font_family="Arial"))


def draw_floor(dwg, ox, oy, floor_name, floor_num, rack_start):
    """Draw a single floor plan at origin (ox, oy)."""

    bx, by = ox, oy

    # Building envelope
    dwg.add(dwg.rect((bx, by), (BLDG_W, BLDG_H), fill="#0d0d12", stroke=ACCENT, stroke_width=2))

    # Dimensions
    dim_line(dwg, bx, by + BLDG_H, bx + BLDG_W, by + BLDG_H, f"{BLDG_W_FT}'-0\"", 18)
    dim_line(dwg, bx + BLDG_W, by, bx + BLDG_W, by + BLDG_H, f"{BLDG_H_FT}'-0\"", 18)

    # Floor label
    dwg.add(dwg.text(floor_name, insert=(bx + BLDG_W / 2, by - 25),
                      text_anchor="middle", fill=ACCENT, font_size=12, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text(f"4 NVL72 RACKS | 288 GPUs | 520 kW | 1 CDU PAIR",
                      insert=(bx + BLDG_W / 2, by - 12),
                      text_anchor="middle", fill="#93c5fd", font_size=8, font_family="Arial"))

    # ── STAIRCASE (left side, 3 ft wide) ──
    stair_w = int(STAIR_W_FT * SCALE)
    stair_x = bx
    box(dwg, stair_x, by, stair_w, BLDG_H,
        "STAIR\nCASE\n3' x 40'", color="#111318", border="#8b5cf6", text_color="#8b5cf6", font=7)

    # Stair treads (visual)
    for sy in range(0, BLDG_H, int(2 * SCALE)):
        dwg.add(dwg.line((stair_x + 2, by + sy), (stair_x + stair_w - 2, by + sy),
                          stroke="#8b5cf6", stroke_width=0.3))

    # Usable dimension
    usable_x = bx + stair_w
    usable_w = BLDG_W - stair_w
    dim_line(dwg, usable_x, by + BLDG_H, usable_x + usable_w, by + BLDG_H,
             f"{BLDG_W_FT - STAIR_W_FT}'-0\" usable", 30)

    # ── CDU AREA (top/north, 6 ft deep) ──
    cdu_depth = int(6 * SCALE)
    box(dwg, usable_x, by, usable_w, cdu_depth,
        "CDU PAIR (N+1)\nPumps + Valves\n6' deep", color="#111318", border="#4fc3f7", text_color="#4fc3f7", font=7)

    # CDU boxes
    cdu_unit_w = int(3 * SCALE)
    cdu_unit_h = int(3 * SCALE)
    for i in range(2):
        cx = usable_x + int(2 * SCALE) + i * int(8 * SCALE)
        cy = by + int(1.5 * SCALE)
        box(dwg, cx, cy, cdu_unit_w, cdu_unit_h, f"CDU\n{i+1}",
            color="#0a1628", border="#4fc3f7", text_color="#4fc3f7", font=6)

    # Cooling pipe labels
    dwg.add(dwg.line((usable_x + 2, by), (usable_x + 2, by - 15), stroke="#4fc3f7", stroke_width=2))
    dwg.add(dwg.text("SUPPLY", insert=(usable_x + 6, by - 5), fill="#4fc3f7", font_size=6, font_family="Arial"))
    dwg.add(dwg.line((usable_x + usable_w - 5, by), (usable_x + usable_w - 5, by - 15), stroke="#ff6b6b", stroke_width=2))
    dwg.add(dwg.text("RETURN", insert=(usable_x + usable_w - 20, by - 5), fill="#ff6b6b", font_size=6, font_family="Arial"))

    # ── ELECTRICAL PANEL (bottom-right corner, 4x4 ft) ──
    elec_w = int(4 * SCALE)
    elec_h = int(4 * SCALE)
    elec_x = bx + BLDG_W - elec_w
    elec_y = by + BLDG_H - elec_h
    box(dwg, elec_x, elec_y, elec_w, elec_h,
        "ELEC\nPANEL\n800V DC", color="#111318", border="#8b5cf6", text_color="#c4b5fd", font=7)

    # ── COMPUTE AREA — 4 NVL72 RACKS ──
    # NVL72 rack: 2 ft wide x 4 ft deep
    rack_w = int(2 * SCALE)
    rack_d = int(4 * SCALE)

    # Rack layout: 2 rows of 2 racks, hot aisle between
    compute_x = usable_x + int(1 * SCALE)
    compute_y = by + cdu_depth + int(2 * SCALE)

    # Available compute space
    compute_area_w = usable_w - int(2 * SCALE)
    compute_area_h = BLDG_H - cdu_depth - elec_h - int(4 * SCALE)

    # Center racks horizontally
    total_rack_row_w = 2 * rack_w + int(4 * SCALE)  # 2 racks + gap
    rack_start_x = compute_x + (compute_area_w - total_rack_row_w) // 2

    # Row 1 (top, facing down)
    row1_y = compute_y + int(2 * SCALE)
    for r in range(2):
        rx = rack_start_x + r * (rack_w + int(4 * SCALE))
        box(dwg, rx, row1_y, rack_w, rack_d, "", color="#1a2e0a", border="#76b900")
        dwg.add(dwg.text(f"R{rack_start + r}", insert=(rx + rack_w / 2, row1_y + rack_d / 2 + 3),
                          text_anchor="middle", fill="#76b900", font_size=8, font_family="Arial", font_weight="bold"))

    # Hot aisle between rows
    hot_y = row1_y + rack_d
    hot_h = int(3 * SCALE)
    dwg.add(dwg.rect((rack_start_x - int(1 * SCALE), hot_y),
                      (total_rack_row_w + int(2 * SCALE), hot_h),
                      fill="#1a0a0a", rx=3))
    dwg.add(dwg.text("HOT AISLE", insert=(rack_start_x + total_rack_row_w / 2, hot_y + hot_h / 2 + 3),
                      text_anchor="middle", fill="#ef4444", font_size=7, font_family="Arial", font_weight="bold"))

    # Row 2 (bottom, facing up)
    row2_y = hot_y + hot_h
    for r in range(2):
        rx = rack_start_x + r * (rack_w + int(4 * SCALE))
        box(dwg, rx, row2_y, rack_w, rack_d, "", color="#1a2e0a", border="#76b900")
        dwg.add(dwg.text(f"R{rack_start + r + 2}", insert=(rx + rack_w / 2, row2_y + rack_d / 2 + 3),
                          text_anchor="middle", fill="#76b900", font_size=8, font_family="Arial", font_weight="bold"))

    # Cold aisles
    cold_h = int(2 * SCALE)
    for cy in [row1_y - cold_h, row2_y + rack_d]:
        dwg.add(dwg.rect((rack_start_x - int(1 * SCALE), cy),
                          (total_rack_row_w + int(2 * SCALE), cold_h),
                          fill="#0a0a1e", rx=3))
        dwg.add(dwg.text("COLD", insert=(rack_start_x + total_rack_row_w / 2, cy + cold_h / 2 + 3),
                          text_anchor="middle", fill=ACCENT, font_size=6, font_family="Arial", font_weight="bold"))

    # Cable tray (dashed, from elec panel to racks)
    cable_x = elec_x - int(0.5 * SCALE)
    dwg.add(dwg.line((cable_x, elec_y), (cable_x, row1_y),
                      stroke="#8b5cf6", stroke_width=1, stroke_dasharray="6,3"))
    dwg.add(dwg.text("CABLE", insert=(cable_x + 3, (elec_y + row1_y) / 2),
                      fill="#8b5cf6", font_size=5, font_family="Arial"))

    # Entry door
    door_y = by + BLDG_H / 2 - 8
    dwg.add(dwg.rect((bx + BLDG_W - 2, door_y), (5, 16), fill=ACCENT, rx=2))
    dwg.add(dwg.text("DOOR", insert=(bx + BLDG_W + 6, door_y + 10),
                      fill="#6b7280", font_size=6, font_family="Arial"))


def build():
    dwg = svgwrite.Drawing(OUT, size=(f"{W}px", f"{H}px"), viewBox=f"0 0 {W} {H}")
    dwg.add(dwg.rect((0, 0), (W, H), fill="#0a0b0f"))

    # -- TITLE BLOCK --
    dwg.add(dwg.text("MARLIE I — LAFAYETTE AI FACTORY & COMMAND CENTER",
                      insert=(W / 2, 24), text_anchor="middle", fill="#f0f2f5",
                      font_size=16, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("FLOOR PLANS | 24' x 40' | 2 FLOORS | 8 NVL72 RACKS | 576 GPUs | 1,040 kW IT LOAD",
                      insert=(W / 2, 40), text_anchor="middle", fill=ACCENT,
                      font_size=10, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("Sheet A-001 | Design Intent | Scale: Conceptual | 2026-03-23 | NOT FOR CONSTRUCTION",
                      insert=(W / 2, 54), text_anchor="middle", fill="#6b7280",
                      font_size=9, font_family="Arial"))

    # Draw both floors side by side
    floor1_x = 100
    floor2_x = 750
    floor_y = 120

    draw_floor(dwg, floor1_x, floor_y, "FLOOR 1 — DOWNSTAIRS (SYSTEM 1)", 1, rack_start=1)
    draw_floor(dwg, floor2_x, floor_y, "FLOOR 2 — UPSTAIRS (SYSTEM 2)", 2, rack_start=5)

    # ================================================================
    # CROSS SECTION INDICATOR
    # ================================================================
    cs_y = 530
    dwg.add(dwg.rect((100, cs_y), (550, 100), rx=6, fill="#111318", stroke="#1e2230"))
    dwg.add(dwg.text("BUILDING CROSS-SECTION (CONCEPTUAL)", insert=(375, cs_y + 18),
                      text_anchor="middle", fill=ACCENT, font_size=10, font_family="Arial", font_weight="bold"))

    # Simple 2-story cross section
    sect_x = 150
    sect_y = cs_y + 30
    floor_h = 28
    floor_w = 450

    # Floor 1
    dwg.add(dwg.rect((sect_x, sect_y + floor_h + 2), (floor_w, floor_h),
                      fill="#0d0d12", stroke=ACCENT, stroke_width=1.5))
    dwg.add(dwg.text("FLOOR 1: 4 NVL72 racks | 520 kW | CDU pair | Elec panel",
                      insert=(sect_x + floor_w / 2, sect_y + floor_h + 20), text_anchor="middle",
                      fill="#76b900", font_size=8, font_family="Arial"))

    # Floor 2
    dwg.add(dwg.rect((sect_x, sect_y), (floor_w, floor_h),
                      fill="#0d0d12", stroke=ACCENT, stroke_width=1.5))
    dwg.add(dwg.text("FLOOR 2: 4 NVL72 racks | 520 kW | CDU pair | Elec panel",
                      insert=(sect_x + floor_w / 2, sect_y + 18), text_anchor="middle",
                      fill="#76b900", font_size=8, font_family="Arial"))

    # Staircase
    stair_sect_x = sect_x
    dwg.add(dwg.rect((stair_sect_x, sect_y), (20, floor_h * 2 + 2),
                      fill="#111318", stroke="#8b5cf6", stroke_width=1))
    dwg.add(dwg.text("STAIR", insert=(stair_sect_x + 10, sect_y + floor_h + 3),
                      text_anchor="middle", fill="#8b5cf6", font_size=6, font_family="Arial"))

    # Roof solar
    dwg.add(dwg.line((sect_x, sect_y - 3), (sect_x + floor_w, sect_y - 3),
                      stroke="#fbbf24", stroke_width=2))
    dwg.add(dwg.text("300 kW SOLAR ROOF", insert=(sect_x + floor_w / 2, sect_y - 8),
                      text_anchor="middle", fill="#fbbf24", font_size=7, font_family="Arial", font_weight="bold"))

    # ================================================================
    # LEGEND + STATS
    # ================================================================
    ly = 530
    leg_x = 700
    dwg.add(dwg.rect((leg_x, ly), (640, 100), rx=6, fill="#111318", stroke="#1e2230"))

    lx = leg_x + 20
    items = [
        ("#76b900", "#1a2e0a", "NVL72 Rack (2' x 4') — 130 kW, liquid cooled"),
        ("#ef4444", "#1a0a0a", "Hot Aisle (Contained)"),
        (ACCENT, "#0a0a1e", "Cold Aisle"),
        ("#4fc3f7", None, "Supply Pipe (Cold from dry coolers)"),
        ("#ff6b6b", None, "Return Pipe (Hot to dry coolers)"),
        ("#8b5cf6", None, "Cable Tray (800V DC busway)"),
    ]
    for i, (color, fill, text) in enumerate(items):
        iy = ly + 12 + i * 14
        if fill:
            dwg.add(dwg.rect((lx, iy - 6), (14, 10), fill=fill, stroke=color, stroke_width=1, rx=2))
        else:
            dwg.add(dwg.line((lx, iy), (lx + 14, iy), stroke=color, stroke_width=2))
        dwg.add(dwg.text(text, insert=(lx + 20, iy + 3), fill="#9ca3af", font_size=8, font_family="Arial"))

    # Stats
    stat_x = leg_x + 380
    stats = [
        ("PER FLOOR", "24' x 37' usable\n888 sq ft"),
        ("RACKS/FLOOR", "4x NVL72\n520 kW IT"),
        ("TOTAL", "8 NVL72 racks\n576 GPUs"),
    ]
    for i, (label, value) in enumerate(stats):
        sy_pos = ly + 12 + i * 28
        dwg.add(dwg.text(label, insert=(stat_x, sy_pos), fill="#6b7280",
                          font_size=8, font_family="Arial", font_weight="bold"))
        for j, line in enumerate(value.split("\n")):
            dwg.add(dwg.text(line, insert=(stat_x + 90, sy_pos + j * 11), fill=ACCENT,
                              font_size=9, font_family="Arial", font_weight="bold"))

    # ================================================================
    # NOTES
    # ================================================================
    ny = 650
    notes = [
        "1. Building footprint: 24' x 40' = 960 sq ft per floor, 1,920 sq ft total. Same as a 40-ft shipping container.",
        "2. Staircase takes 3 ft off one side = 21' x 40' usable per floor (actual ~37' accounting for CDU + elec area = ~888 sq ft).",
        "3. Each floor: 4x NVL72 racks in hot/cold aisle containment, 1 CDU pair (N+1), 1 electrical panel.",
        "4. NVL72 rack: ~2' wide x 4' deep, 130 kW, liquid cooled, 45C hot water supply, ~2,500 lbs loaded.",
        "5. Hot/cold aisle containment: cold supply from CDUs, hot exhaust contained and returned to CDU loop.",
        "6. 800V DC busway runs via overhead cable tray from electrical panel to each rack position.",
        "7. CDU pairs located at building edge for shortest pipe run to exterior dry coolers.",
        "8. Floor loading: NVL72 ~250 lb/sq ft concentrated — structural reinforcement at rack positions required.",
        "9. Each floor is a self-contained compute system (System 1 + System 2) with independent CDU and power feeds.",
        "10. Total building: 8 NVL72 racks, 576 GPUs, 1,040 kW IT load, 2 CDU pairs, ~1.24 MW total with overhead.",
    ]
    for i, note in enumerate(notes):
        dwg.add(dwg.text(note, insert=(35, ny + i * 13), fill="#4b5563",
                          font_size=7.5, font_family="Arial"))

    # Building comparison callout
    cmp_y = ny + len(notes) * 13 + 15
    dwg.add(dwg.rect((35, cmp_y), (600, 40), rx=6, fill="#111318", stroke="#1e2230"))
    dwg.add(dwg.text("MARLIE I vs TRAPPEYS:", insert=(50, cmp_y + 15), fill=ACCENT,
                      font_size=9, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("MARLIE I = 1,920 sq ft / 8 racks / 576 GPUs  |  Trappeys = 112,500 sq ft / 4-84 racks / scalable",
                      insert=(50, cmp_y + 28), fill="#9ca3af", font_size=8, font_family="Arial"))

    dwg.save()
    print(f"Saved: {OUT}")


if __name__ == "__main__":
    import os
    os.makedirs("adc3k-deploy/blueprints", exist_ok=True)
    build()
