"""
MARLIE I — Lafayette AI Factory & Command Center
Floor Plans: Floor 1 + Floor 2 Side by Side + Cross Section
Building: 24 ft wide x 40 ft long, 2 identical floors
Staircase: south end, 24 ft wide x 3 ft deep
Usable per floor: 24 ft wide x 37 ft long
12 racks per floor (center-mounted single row), 24 total
"""
import svgwrite

W, H = 1600, 1100
OUT = "adc3k-deploy/blueprints/marlie-floor-plan.svg"

ACCENT = "#3b82f6"
BG = "#0a0b0f"
PANEL_BG = "#0d0d12"
ZONE_BG = "#111318"
BORDER = "#1e2230"

# Building dimensions (feet)
BLDG_W_FT = 24
BLDG_L_FT = 40
STAIR_DEPTH_FT = 3
USABLE_L_FT = 37  # 40 - 3 staircase

# Rack layout
CDU_ZONE_FT = 3       # north end
ELEC_ZONE_FT = 3      # south end (next to staircase)
RACK_ZONE_FT = 31     # 37 - 3 - 3
RACK_PITCH_FT = 2.5   # center-to-center
RACKS_PER_FLOOR = 12   # 31 / 2.5 = 12.4, use 12
RACK_W_FT = 2
RACK_D_FT = 4

# Aisle math: 24ft width, 2ft rack in center
LEFT_AISLE_FT = 11
RIGHT_AISLE_FT = 11

SCALE = 10  # 1 ft = 10 px


def ft(v):
    return int(v * SCALE)


def box(dwg, x, y, w, h, label="", color=ZONE_BG, border=ACCENT,
        text_color="#e0e0e0", font=9, bold_first=True):
    dwg.add(dwg.rect((x, y), (w, h), fill=color, stroke=border, stroke_width=1))
    if label:
        lines = label.split("\n")
        for i, line in enumerate(lines):
            ty = y + h / 2 - (len(lines) - 1) * 6 + i * 12
            weight = "bold" if (i == 0 and bold_first) else "normal"
            dwg.add(dwg.text(line, insert=(x + w / 2, ty), text_anchor="middle",
                             fill=text_color, font_size=font, font_family="Arial",
                             font_weight=weight))


def dim_h(dwg, x1, x2, y, label, offset=18):
    """Horizontal dimension line below y."""
    dy = y + offset
    dwg.add(dwg.line((x1, dy), (x2, dy), stroke="#555", stroke_width=0.5))
    dwg.add(dwg.line((x1, dy - 4), (x1, dy + 4), stroke="#555", stroke_width=0.5))
    dwg.add(dwg.line((x2, dy - 4), (x2, dy + 4), stroke="#555", stroke_width=0.5))
    dwg.add(dwg.text(label, insert=((x1 + x2) / 2, dy - 3), text_anchor="middle",
                     fill="#888", font_size=7, font_family="Arial"))


def dim_v(dwg, x, y1, y2, label, offset=18):
    """Vertical dimension line to the right of x."""
    dx = x + offset
    dwg.add(dwg.line((dx, y1), (dx, y2), stroke="#555", stroke_width=0.5))
    dwg.add(dwg.line((dx - 4, y1), (dx + 4, y1), stroke="#555", stroke_width=0.5))
    dwg.add(dwg.line((dx - 4, y2), (dx + 4, y2), stroke="#555", stroke_width=0.5))
    dwg.add(dwg.text(label, insert=(dx + 5, (y1 + y2) / 2 + 3), fill="#888",
                     font_size=7, font_family="Arial"))


def draw_floor(dwg, ox, oy, floor_name, system_num):
    """Draw a single floor plan at origin (ox, oy).
    North = top, South = bottom.
    South end has staircase.
    """
    bw = ft(BLDG_W_FT)
    bl = ft(BLDG_L_FT)

    # Building envelope (north at top)
    dwg.add(dwg.rect((ox, oy), (bw, bl), fill=PANEL_BG, stroke=ACCENT, stroke_width=2))

    # Floor label
    dwg.add(dwg.text(floor_name, insert=(ox + bw / 2, oy - 28),
                     text_anchor="middle", fill=ACCENT, font_size=12,
                     font_family="Arial", font_weight="bold"))

    # Compute racks
    compute_count = 8
    net_count = 2
    stor_count = 2
    total_kw = compute_count * 130 + net_count * 20 + stor_count * 20
    dwg.add(dwg.text(
        f"12 NVL72 RACKS | {compute_count} COMPUTE + {net_count} NETWORK + {stor_count} STORAGE | {total_kw} kW",
        insert=(ox + bw / 2, oy - 14),
        text_anchor="middle", fill="#93c5fd", font_size=8, font_family="Arial"))

    # Compass
    dwg.add(dwg.text("N", insert=(ox + bw + 30, oy + 8), text_anchor="middle",
                     fill="#6b7280", font_size=9, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.line((ox + bw + 30, oy + 12), (ox + bw + 30, oy + 28),
                     stroke="#6b7280", stroke_width=1.5))
    dwg.add(dwg.text("S", insert=(ox + bw + 30, oy + bl - 4), text_anchor="middle",
                     fill="#6b7280", font_size=9, font_family="Arial", font_weight="bold"))

    # ── DIMENSIONS ──
    dim_h(dwg, ox, ox + bw, oy + bl, f"{BLDG_W_FT}'-0\"", 20)
    dim_v(dwg, ox + bw, oy, oy + bl, f"{BLDG_L_FT}'-0\"", 40)

    # ── STAIRCASE — south end (bottom), full width, 3 ft deep ──
    stair_y = oy + bl - ft(STAIR_DEPTH_FT)
    stair_h = ft(STAIR_DEPTH_FT)
    box(dwg, ox, stair_y, bw, stair_h,
        f"STAIRCASE  {BLDG_W_FT}' x {STAIR_DEPTH_FT}'",
        color="#111318", border="#8b5cf6", text_color="#8b5cf6", font=8)
    # Stair treads
    for sx in range(0, bw, ft(2)):
        dwg.add(dwg.line((ox + sx, stair_y + 2), (ox + sx, stair_y + stair_h - 2),
                         stroke="#8b5cf6", stroke_width=0.3))

    # ── USABLE ZONE: 24 x 37, from top of building down to staircase ──
    usable_y = oy
    usable_h = ft(USABLE_L_FT)
    # Show usable dimension
    dim_v(dwg, ox + bw, oy, oy + usable_h, f"{USABLE_L_FT}'-0\" usable", 60)

    # ── CDU AREA — north end (top), 24 ft wide x 3 ft deep ──
    cdu_h = ft(CDU_ZONE_FT)
    box(dwg, ox + 1, oy + 1, bw - 2, cdu_h - 2,
        f"CDU / COOLING CONNECTIONS\n{BLDG_W_FT}' x {CDU_ZONE_FT}'",
        color="#0a1628", border="#4fc3f7", text_color="#4fc3f7", font=7)

    # Cooling pipe stubs
    dwg.add(dwg.line((ox + 8, oy), (ox + 8, oy - 12), stroke="#4fc3f7", stroke_width=2))
    dwg.add(dwg.text("SUPPLY", insert=(ox + 14, oy - 4), fill="#4fc3f7",
                     font_size=5, font_family="Arial"))
    dwg.add(dwg.line((ox + bw - 8, oy), (ox + bw - 8, oy - 12), stroke="#ff6b6b", stroke_width=2))
    dwg.add(dwg.text("RETURN", insert=(ox + bw - 35, oy - 4), fill="#ff6b6b",
                     font_size=5, font_family="Arial"))

    # ── ELECTRICAL PANEL — south end of usable zone, 24 ft wide x 3 ft deep ──
    elec_y = oy + ft(USABLE_L_FT) - ft(ELEC_ZONE_FT)
    elec_h = ft(ELEC_ZONE_FT)
    box(dwg, ox + 1, elec_y + 1, bw - 2, elec_h - 2,
        f"ELEC PANEL (EATON 800V DC)\n{BLDG_W_FT}' x {ELEC_ZONE_FT}'",
        color="#111318", border="#8b5cf6", text_color="#c4b5fd", font=7)

    # ── RACK ZONE — center row, 31 ft long ──
    rack_zone_top = oy + cdu_h
    rack_zone_h = ft(RACK_ZONE_FT)

    # Center the rack column (2 ft wide) in the 24 ft width
    rack_cx = ox + ft(LEFT_AISLE_FT)  # left edge of rack
    rack_w = ft(RACK_W_FT)

    # Aisle labels
    dwg.add(dwg.text(f"{LEFT_AISLE_FT}' AISLE", insert=(ox + ft(LEFT_AISLE_FT / 2), rack_zone_top + rack_zone_h / 2),
                     text_anchor="middle", fill="#4b5563", font_size=7, font_family="Arial",
                     transform=f"rotate(-90,{ox + ft(LEFT_AISLE_FT / 2)},{rack_zone_top + rack_zone_h / 2})"))
    dwg.add(dwg.text(f"{RIGHT_AISLE_FT}' AISLE", insert=(ox + ft(LEFT_AISLE_FT + RACK_W_FT + RIGHT_AISLE_FT / 2), rack_zone_top + rack_zone_h / 2),
                     text_anchor="middle", fill="#4b5563", font_size=7, font_family="Arial",
                     transform=f"rotate(-90,{ox + ft(LEFT_AISLE_FT + RACK_W_FT + RIGHT_AISLE_FT / 2)},{rack_zone_top + rack_zone_h / 2})"))

    # Draw center dotted line for rack row alignment
    dwg.add(dwg.line((rack_cx + rack_w / 2, rack_zone_top),
                     (rack_cx + rack_w / 2, rack_zone_top + rack_zone_h),
                     stroke="#333", stroke_width=0.5, stroke_dasharray="4,4"))

    # Draw racks: 12 positions, evenly spaced in 31 ft
    # Start 0.5 ft from CDU zone edge, pitch 2.5 ft
    rack_pitch = ft(RACK_PITCH_FT)
    rack_h_px = ft(RACK_W_FT)  # rack is 2ft wide (along the row = vertical in plan)
    # rack_d_px = ft(RACK_D_FT)  # 4ft deep but we show 2ft width for plan view center-mounted
    # Actually in plan view: rack width across building = 2ft, rack depth along building = 4ft? No.
    # The racks sit in a single row down the center. In plan view:
    #   - Horizontal (across building) = 2 ft (rack width)
    #   - Vertical (along building length) = 2 ft (we use the pitch minus gap)
    # NVL72 is 2ft wide x 4ft deep but in a single row the "depth" faces the aisles (left-right).
    # So in plan view: horizontal span = 4ft (depth into aisles), vertical span = 2ft (width).
    # But user said "2ft wide racks" in the center, aisles 11ft each side.
    # This means the 2ft is the cross-building dimension. The 4ft depth extends into aisles.
    # Let's show the rack as 4ft wide (across building, into aisles) x 2ft tall (along building).

    rack_across = ft(RACK_D_FT)  # 4ft across building (depth)
    rack_along = ft(RACK_W_FT)   # 2ft along building length
    rack_left_x = ox + ft(BLDG_W_FT / 2) - rack_across / 2  # centered

    # Re-derive aisle widths for display: (24 - 4) / 2 = 10 ft each side with 4ft rack
    actual_aisle = (BLDG_W_FT - RACK_D_FT) / 2  # 10 ft

    # Update aisle labels with actual dimension
    # (Overwrite the previous aisle labels — let's remove those and redo)
    # Actually SVG appends, so the old ones stay. Let me just draw over them.
    # Better: skip the aisle labels above and draw them here.

    # Rack colors
    COMPUTE_COLOR = "#1a2e0a"
    COMPUTE_BORDER = "#76b900"
    NET_COLOR = "#0a1628"
    NET_BORDER = "#4fc3f7"
    STOR_COLOR = "#1a0a2e"
    STOR_BORDER = "#a78bfa"

    # Rack assignment: 8 compute, 2 network, 2 storage
    # Layout: NET - COMPUTE x8 - NET - STOR x2 (or interleave networking)
    # Better: STOR, NET, COMPUTE x8, NET, STOR
    rack_types = (
        [("STOR", STOR_COLOR, STOR_BORDER, "S", 20)] * 1 +
        [("NET", NET_COLOR, NET_BORDER, "N", 20)] * 1 +
        [("COMP", COMPUTE_COLOR, COMPUTE_BORDER, "C", 130)] * 8 +
        [("NET", NET_COLOR, NET_BORDER, "N", 20)] * 1 +
        [("STOR", STOR_COLOR, STOR_BORDER, "S", 20)] * 1
    )

    start_offset = ft(0.25)  # small gap from CDU zone
    for i, (rtype, rcolor, rborder, rlabel, rkw) in enumerate(rack_types):
        ry = rack_zone_top + start_offset + i * rack_pitch
        rx = rack_left_x

        dwg.add(dwg.rect((rx, ry), (rack_across, rack_along), fill=rcolor,
                         stroke=rborder, stroke_width=1.2, rx=2))

        # Rack label
        rack_num = i + 1 + (12 if system_num == 2 else 0)
        dwg.add(dwg.text(f"{rlabel}{rack_num}", insert=(rx + rack_across / 2, ry + rack_along / 2 + 3),
                         text_anchor="middle", fill=rborder, font_size=7,
                         font_family="Arial", font_weight="bold"))

    # Aisle dimension lines (use actual 10ft with 4ft racks)
    aisle_label_y = rack_zone_top + rack_zone_h + 6
    dim_h(dwg, ox, rack_left_x, aisle_label_y, f"{actual_aisle:.0f}' aisle", 0)
    dim_h(dwg, rack_left_x + rack_across, ox + bw, aisle_label_y, f"{actual_aisle:.0f}' aisle", 0)
    dim_h(dwg, rack_left_x, rack_left_x + rack_across, aisle_label_y, f"{RACK_D_FT}' racks", 12)

    # Entry door (east wall, centered on rack zone)
    door_cy = rack_zone_top + rack_zone_h / 2
    dwg.add(dwg.rect((ox + bw - 2, door_cy - 8), (5, 16), fill=ACCENT, rx=2))
    dwg.add(dwg.text("DOOR", insert=(ox + bw + 6, door_cy + 3),
                     fill="#6b7280", font_size=6, font_family="Arial"))

    # Cable tray (dashed, from elec panel to rack row)
    cable_x = rack_left_x + rack_across + ft(1)
    dwg.add(dwg.line((cable_x, elec_y), (cable_x, rack_zone_top + start_offset),
                     stroke="#8b5cf6", stroke_width=1, stroke_dasharray="6,3"))
    dwg.add(dwg.text("800V DC\nBUSWAY", insert=(cable_x + 4, (elec_y + rack_zone_top) / 2),
                     fill="#8b5cf6", font_size=5, font_family="Arial"))


def draw_cross_section(dwg, ox, oy, section_w, section_h):
    """Side view cross-section showing both floors stacked."""
    dwg.add(dwg.rect((ox - 10, oy - 25), (section_w + 20, section_h + 35),
                     rx=6, fill=ZONE_BG, stroke=BORDER))
    dwg.add(dwg.text("BUILDING CROSS-SECTION (EAST ELEVATION)", insert=(ox + section_w / 2, oy - 10),
                     text_anchor="middle", fill=ACCENT, font_size=10,
                     font_family="Arial", font_weight="bold"))

    floor_h = section_h // 2 - 5
    slab_h = 4

    # Ground line
    ground_y = oy + section_h
    dwg.add(dwg.line((ox - 10, ground_y), (ox + section_w + 10, ground_y),
                     stroke="#4b5563", stroke_width=2))
    dwg.add(dwg.text("GRADE", insert=(ox + section_w + 14, ground_y + 3),
                     fill="#4b5563", font_size=6, font_family="Arial"))

    # Floor 1 (bottom)
    f1_y = ground_y - floor_h
    dwg.add(dwg.rect((ox, f1_y), (section_w, floor_h), fill=PANEL_BG, stroke=ACCENT, stroke_width=1.5))
    dwg.add(dwg.text("FLOOR 1 (SYSTEM 1) — 12 NVL72 RACKS | 1,120 kW",
                     insert=(ox + section_w / 2, f1_y + floor_h / 2 + 4),
                     text_anchor="middle", fill="#76b900", font_size=8, font_family="Arial"))

    # Slab between floors
    slab_y = f1_y - slab_h
    dwg.add(dwg.rect((ox, slab_y), (section_w, slab_h), fill="#333", stroke="#555", stroke_width=0.5))

    # Floor 2 (top)
    f2_y = slab_y - floor_h
    dwg.add(dwg.rect((ox, f2_y), (section_w, floor_h), fill=PANEL_BG, stroke=ACCENT, stroke_width=1.5))
    dwg.add(dwg.text("FLOOR 2 (SYSTEM 2) — 12 NVL72 RACKS | 1,120 kW",
                     insert=(ox + section_w / 2, f2_y + floor_h / 2 + 4),
                     text_anchor="middle", fill="#76b900", font_size=8, font_family="Arial"))

    # Staircase (south end = right side in elevation)
    stair_w = 30
    dwg.add(dwg.rect((ox + section_w - stair_w, f2_y), (stair_w, floor_h * 2 + slab_h),
                     fill=ZONE_BG, stroke="#8b5cf6", stroke_width=1))
    dwg.add(dwg.text("STAIR", insert=(ox + section_w - stair_w / 2, f1_y + floor_h / 2 - 5),
                     text_anchor="middle", fill="#8b5cf6", font_size=7, font_family="Arial"))

    # Roof
    roof_y = f2_y - 4
    dwg.add(dwg.line((ox, roof_y), (ox + section_w, roof_y), stroke="#fbbf24", stroke_width=2))
    dwg.add(dwg.text("300 kW SOLAR ROOF", insert=(ox + section_w / 2, roof_y - 5),
                     text_anchor="middle", fill="#fbbf24", font_size=7,
                     font_family="Arial", font_weight="bold"))

    # Height dimensions
    total_h = ground_y - roof_y
    dim_v(dwg, ox + section_w, f1_y, ground_y, "~10' CLR", 12)
    dim_v(dwg, ox + section_w, f2_y, slab_y, "~10' CLR", 12)
    dim_v(dwg, ox + section_w, roof_y, ground_y, f"~{2 * 10 + 1}' TOTAL", 30)

    # Width dimension
    dim_h(dwg, ox, ox + section_w, ground_y, f"{BLDG_L_FT}'-0\" (BUILDING LENGTH)", 12)


def build():
    dwg = svgwrite.Drawing(OUT, size=(f"{W}px", f"{H}px"), viewBox=f"0 0 {W} {H}")
    dwg.add(dwg.rect((0, 0), (W, H), fill=BG))

    # ── TITLE BLOCK ──
    dwg.add(dwg.text("MARLIE I — LAFAYETTE AI FACTORY & COMMAND CENTER",
                     insert=(W / 2, 26), text_anchor="middle", fill="#f0f2f5",
                     font_size=16, font_family="Arial", font_weight="bold"))

    total_compute = 16  # 8 per floor
    total_net = 4
    total_stor = 4
    total_racks = 24
    total_gpus = total_compute * 72  # NVL72 = 72 GPUs
    total_kw = total_compute * 130 + (total_net + total_stor) * 20
    dwg.add(dwg.text(
        f"FLOOR PLANS | 24' x 40' | 2 FLOORS | {total_racks} NVL72 RACKS | {total_gpus} GPUs | {total_kw/1000:.1f} MW IT LOAD",
        insert=(W / 2, 44), text_anchor="middle", fill=ACCENT,
        font_size=10, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text(
        "Sheet A-001 | Design Intent | Scale: Conceptual | 2026-03-24 | NOT FOR CONSTRUCTION",
        insert=(W / 2, 58), text_anchor="middle", fill="#6b7280",
        font_size=9, font_family="Arial"))

    # ── FLOOR PLANS SIDE BY SIDE ──
    floor_y = 110
    floor1_x = 120
    floor2_x = 500

    draw_floor(dwg, floor1_x, floor_y, "FLOOR 1 — SYSTEM 1", 1)
    draw_floor(dwg, floor2_x, floor_y, "FLOOR 2 — SYSTEM 2", 2)

    # ── CROSS SECTION ──
    cs_ox = 900
    cs_oy = 210
    draw_cross_section(dwg, cs_ox, cs_oy, 400, 180)

    # ── LEGEND ──
    leg_x = 900
    leg_y = 110
    dwg.add(dwg.rect((leg_x - 10, leg_y - 10), (420, 80), rx=6, fill=ZONE_BG, stroke=BORDER))
    dwg.add(dwg.text("LEGEND", insert=(leg_x, leg_y + 4), fill=ACCENT, font_size=9,
                     font_family="Arial", font_weight="bold"))

    items = [
        ("#76b900", "#1a2e0a", "Compute Rack (NVL72) — 130 kW, liquid cooled"),
        ("#4fc3f7", "#0a1628", "Networking Rack (QX800 IB / SX Ethernet) — 20 kW"),
        ("#a78bfa", "#1a0a2e", "Storage Rack (NVMe nodes) — 20 kW"),
        ("#8b5cf6", None, "800V DC Busway (cable tray)"),
        ("#4fc3f7", None, "Cold supply pipe"),
        ("#ff6b6b", None, "Hot return pipe"),
    ]
    lx = leg_x + 5
    for i, (color, fill_c, text) in enumerate(items):
        iy = leg_y + 18 + i * 11
        if fill_c:
            dwg.add(dwg.rect((lx, iy - 6), (14, 8), fill=fill_c, stroke=color,
                             stroke_width=1, rx=2))
        else:
            dwg.add(dwg.line((lx, iy - 2), (lx + 14, iy - 2), stroke=color, stroke_width=2))
        dwg.add(dwg.text(text, insert=(lx + 20, iy + 1), fill="#9ca3af",
                         font_size=7, font_family="Arial"))

    # ── STATS BOX ──
    stat_x = 900
    stat_y = 430
    dwg.add(dwg.rect((stat_x - 10, stat_y - 10), (420, 100), rx=6, fill=ZONE_BG, stroke=BORDER))
    dwg.add(dwg.text("BUILDING SUMMARY", insert=(stat_x, stat_y + 6), fill=ACCENT,
                     font_size=9, font_family="Arial", font_weight="bold"))

    stats_lines = [
        f"Footprint: {BLDG_W_FT}' x {BLDG_L_FT}' = {BLDG_W_FT * BLDG_L_FT} sq ft/floor, {BLDG_W_FT * BLDG_L_FT * 2:,} sq ft total",
        f"Usable per floor: {BLDG_W_FT}' x {USABLE_L_FT}' = {BLDG_W_FT * USABLE_L_FT} sq ft ({STAIR_DEPTH_FT}' staircase at south end)",
        f"Racks per floor: {RACKS_PER_FLOOR} (8 compute + 2 networking + 2 storage)",
        f"Total racks: {total_racks} across 2 floors (2 full SuperPODs)",
        f"Total GPUs: {total_gpus} (B200 via NVL72)",
        f"IT Load: {total_kw:,} kW ({total_kw/1000:.1f} MW) — est. {total_kw * 1.2 / 1000:.1f} MW with cooling overhead",
        f"Rack layout: center-mounted single row, {LEFT_AISLE_FT:.0f}' aisles each side (shipping container concept)",
        f"CDU zone: {CDU_ZONE_FT}' at north end | Elec panel: {ELEC_ZONE_FT}' at south end",
    ]
    for i, line in enumerate(stats_lines):
        dwg.add(dwg.text(line, insert=(stat_x, stat_y + 20 + i * 11), fill="#9ca3af",
                         font_size=7, font_family="Arial"))

    # ── NOTES ──
    ny = 570
    notes = [
        f"1. Building footprint: {BLDG_W_FT}' x {BLDG_L_FT}' = {BLDG_W_FT * BLDG_L_FT} sq ft per floor, {BLDG_W_FT * BLDG_L_FT * 2:,} sq ft total.",
        f"2. Staircase: {BLDG_W_FT}' wide x {STAIR_DEPTH_FT}' deep at south end. Usable space: {BLDG_W_FT}' x {USABLE_L_FT}' per floor.",
        f"3. Center-mounted single rack row (shipping container concept): {RACK_D_FT}' deep racks centered, {(BLDG_W_FT - RACK_D_FT) / 2:.0f}' access aisles each side.",
        f"4. {RACKS_PER_FLOOR} rack positions per floor: {CDU_ZONE_FT}' CDU zone (N) + {RACK_ZONE_FT}' rack zone + {ELEC_ZONE_FT}' elec panel (S) = {USABLE_L_FT}' usable.",
        f"5. Each floor: 8 compute NVL72 (130 kW ea, liquid cooled) + 2 networking (Quantum-X800 IB + Spectrum-X) + 2 storage (NVMe).",
        f"6. 2 complete SuperPODs: System 1 (Floor 1) + System 2 (Floor 2). Each independently cooled and powered.",
        f"7. NVL72 rack: ~2' wide x 4' deep x 6.5' tall, 130 kW, 45C hot water, ~2,500 lbs loaded.",
        f"8. Floor loading: NVL72 ~250 lb/sq ft concentrated — structural reinforcement at all rack positions required.",
        f"9. 800V DC power distribution via overhead busway from Eaton panel to each rack position.",
        f"10. CDU connections at north wall for shortest pipe run to exterior dry coolers / cooling tower.",
        f"11. Total: {total_racks} racks, {total_gpus} GPUs, {total_kw/1000:.1f} MW IT, est. {total_kw * 1.2 / 1000:.1f} MW total with cooling.",
    ]
    for i, note in enumerate(notes):
        dwg.add(dwg.text(note, insert=(35, ny + i * 13), fill="#4b5563",
                         font_size=7.5, font_family="Arial"))

    # ── MARLIE I vs TRAPPEYS comparison ──
    cmp_y = ny + len(notes) * 13 + 15
    dwg.add(dwg.rect((35, cmp_y), (800, 40), rx=6, fill=ZONE_BG, stroke=BORDER))
    dwg.add(dwg.text("MARLIE I vs TRAPPEYS:", insert=(50, cmp_y + 15), fill=ACCENT,
                     font_size=9, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text(
        f"MARLIE I = {BLDG_W_FT * BLDG_L_FT * 2:,} sq ft / {total_racks} racks / {total_gpus} GPUs  |  "
        f"Trappeys = 112,500 sq ft / 36-84 racks / scalable SuperPOD deployment",
        insert=(50, cmp_y + 28), fill="#9ca3af", font_size=8, font_family="Arial"))

    dwg.save()
    print(f"Saved: {OUT}")


if __name__ == "__main__":
    import os
    os.makedirs("adc3k-deploy/blueprints", exist_ok=True)
    build()
