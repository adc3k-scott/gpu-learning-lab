"""
ADC 3K Pod — 40-ft Compute Module Blueprint
THREE views: Top, Side, End
10x NVL72 racks in 40-ft HC ISO container
Engineering data from data/adc3k-pod-engineering.md
"""
import svgwrite
import os

W, H = 1800, 1300
OUT = "adc3k-deploy/blueprints/adc3k-pod-layout.svg"

# Colors
BG = "#0a0b0f"
PANEL_BG = "#0d0d12"
ZONE_BG = "#111318"
BORDER = "#1e2230"
ACCENT = "#00e87a"  # ADC 3K green
BLUE = "#3b9eff"
PURPLE = "#a855f7"
CYAN = "#4fc3f7"
RED = "#ff6b6b"
DIM_COLOR = "#555"
DIM_TEXT = "#888"
NOTE_COLOR = "#4b5563"
LABEL_COLOR = "#9ca3af"

# Container internal dimensions (inches)
CONT_L_IN = 473.7   # 39 ft 5.4 in
CONT_W_IN = 92.6    # 7 ft 8.6 in
CONT_H_IN = 106.2   # 8 ft 10 in

# NVL72 rack dimensions (inches)
RACK_W_IN = 23.6     # width (across container)
RACK_D_IN = 42.0     # depth (along container length... but rack faces aisles)
RACK_H_IN = 88.0     # height (Supermicro)

# Layout zones (inches) - revised layout from engineering doc
ENTRY_IN = 36        # 3 ft entry zone at door end
ELEC_IN = 42         # 3.5 ft electrical panel
RACK_ZONE_IN = 276   # 10 racks x 24in + 9 gaps x 4in
PATCH_IN = 36        # 3 ft patch panel
CDU_IN = 72          # 6 ft CDU zone

# Side clearance
SIDE_CLEAR_IN = 25.3  # each side

# Overhead clearance
OVERHEAD_IN = 18.2    # above racks to ceiling

# Access panels (user spec: 8 panels, 4 per side)
AP_COUNT_PER_SIDE = 4
AP_WIDTH_IN = 96      # ~8 ft wide each
AP_HEIGHT_IN = 90     # ~7.5 ft tall


def dim_h(dwg, x1, x2, y, label, offset=16):
    """Horizontal dimension line."""
    dy = y + offset
    dwg.add(dwg.line((x1, dy), (x2, dy), stroke=DIM_COLOR, stroke_width=0.5))
    dwg.add(dwg.line((x1, dy - 4), (x1, dy + 4), stroke=DIM_COLOR, stroke_width=0.5))
    dwg.add(dwg.line((x2, dy - 4), (x2, dy + 4), stroke=DIM_COLOR, stroke_width=0.5))
    dwg.add(dwg.text(label, insert=((x1 + x2) / 2, dy - 3), text_anchor="middle",
                     fill=DIM_TEXT, font_size=6.5, font_family="Arial"))


def dim_v(dwg, x, y1, y2, label, offset=16):
    """Vertical dimension line."""
    dx = x + offset
    dwg.add(dwg.line((dx, y1), (dx, y2), stroke=DIM_COLOR, stroke_width=0.5))
    dwg.add(dwg.line((dx - 4, y1), (dx + 4, y1), stroke=DIM_COLOR, stroke_width=0.5))
    dwg.add(dwg.line((dx - 4, y2), (dx + 4, y2), stroke=DIM_COLOR, stroke_width=0.5))
    dwg.add(dwg.text(label, insert=(dx + 5, (y1 + y2) / 2 + 3), fill=DIM_TEXT,
                     font_size=6.5, font_family="Arial"))


def box(dwg, x, y, w, h, label="", color=ZONE_BG, border=ACCENT,
        text_color="#e0e0e0", font=8):
    """Draw a labeled rectangle."""
    dwg.add(dwg.rect((x, y), (w, h), fill=color, stroke=border, stroke_width=1))
    if label:
        lines = label.split("\n")
        for i, line in enumerate(lines):
            ty = y + h / 2 - (len(lines) - 1) * 6 + i * 12
            weight = "bold" if i == 0 else "normal"
            dwg.add(dwg.text(line, insert=(x + w / 2, ty), text_anchor="middle",
                             fill=text_color, font_size=font, font_family="Arial",
                             font_weight=weight))


def draw_top_view(dwg, ox, oy):
    """VIEW 1: Top view looking down at the container."""
    # Scale: 1 inch = 1.1 px for top view
    S = 1.1

    def si(v):
        return v * S

    view_w = si(CONT_L_IN)
    view_h = si(CONT_W_IN)

    # View panel background
    pad = 30
    dwg.add(dwg.rect((ox - pad, oy - 40), (view_w + pad * 2 + 80, view_h + pad + 70),
                     rx=6, fill=ZONE_BG, stroke=BORDER))

    # View title
    dwg.add(dwg.text("VIEW 1 — TOP VIEW (LOOKING DOWN)", insert=(ox + view_w / 2, oy - 22),
                     text_anchor="middle", fill=ACCENT, font_size=11,
                     font_family="Arial", font_weight="bold"))

    # Container outline
    dwg.add(dwg.rect((ox, oy), (view_w, view_h), fill=PANEL_BG, stroke=ACCENT, stroke_width=2))

    # Door opening at left (entry end)
    door_w = si(8)
    door_y = oy + view_h / 2 - si(4)
    dwg.add(dwg.rect((ox - 3, door_y), (6, si(8)), fill=ACCENT, rx=2))
    dwg.add(dwg.text("DOOR", insert=(ox - 10, door_y + si(4) + 3),
                     fill=ACCENT, font_size=5, font_family="Arial",
                     text_anchor="middle",
                     transform=f"rotate(-90,{ox - 10},{door_y + si(4) + 3})"))

    # Zone boundaries (vertical lines along container length)
    zones = [
        ("ENTRY\n3'-0\"", ENTRY_IN, "#2a3a2a", ACCENT),
        ("ELEC PANEL\n3'-6\"", ELEC_IN, "#1a1a2e", PURPLE),
    ]

    cx = ox  # current x position

    # Entry zone
    ez_w = si(ENTRY_IN)
    box(dwg, cx + 1, oy + 1, ez_w - 1, view_h - 2,
        "ENTRY\n3'-0\"", color="#0a1a0a", border="#1a3a1a", text_color=ACCENT, font=6)
    cx += ez_w

    # Electrical panel zone
    ep_w = si(ELEC_IN)
    box(dwg, cx, oy + 1, ep_w, view_h - 2,
        "ELEC PANEL\nEATON 800V DC\n3'-6\"", color="#1a0a2e", border=PURPLE, text_color="#c4b5fd", font=6)
    cx += ep_w

    # Rack zone
    rz_w = si(RACK_ZONE_IN)
    rack_zone_x = cx

    # Draw racks: 10 racks centered in container width
    # Rack depth faces the sides (across container width = RACK_D_IN)
    # Rack width goes along container length = RACK_W_IN
    rack_across = si(RACK_D_IN)  # across container (depth)
    rack_along = si(RACK_W_IN)   # along container (width)
    rack_cy = oy + view_h / 2    # center Y of container

    rack_top_y = rack_cy - rack_across / 2
    gap_px = si(4)  # 4-inch gaps

    # Rack colors
    COMPUTE_COLOR = "#0a2010"
    COMPUTE_BORDER = ACCENT
    NET_COLOR = "#0a1628"
    NET_BORDER = BLUE
    STOR_COLOR = "#1a0a2e"
    STOR_BORDER = PURPLE

    rack_types = [
        ("R1", "COMPUTE", COMPUTE_COLOR, COMPUTE_BORDER),
        ("R2", "COMPUTE", COMPUTE_COLOR, COMPUTE_BORDER),
        ("R3", "COMPUTE", COMPUTE_COLOR, COMPUTE_BORDER),
        ("R4", "COMPUTE", COMPUTE_COLOR, COMPUTE_BORDER),
        ("R5", "COMPUTE", COMPUTE_COLOR, COMPUTE_BORDER),
        ("R6", "COMPUTE", COMPUTE_COLOR, COMPUTE_BORDER),
        ("R7", "COMPUTE", COMPUTE_COLOR, COMPUTE_BORDER),
        ("R8", "COMPUTE", COMPUTE_COLOR, COMPUTE_BORDER),
        ("R9", "NET", NET_COLOR, NET_BORDER),
        ("R10", "STOR", STOR_COLOR, STOR_BORDER),
    ]

    rx = rack_zone_x
    for i, (name, rtype, rcolor, rborder) in enumerate(rack_types):
        # Draw rack rectangle
        dwg.add(dwg.rect((rx, rack_top_y), (rack_along, rack_across),
                         fill=rcolor, stroke=rborder, stroke_width=1.2, rx=2))
        # Rack label
        dwg.add(dwg.text(name, insert=(rx + rack_along / 2, rack_cy + 3),
                         text_anchor="middle", fill=rborder, font_size=7,
                         font_family="Arial", font_weight="bold"))
        rx += rack_along + gap_px

    cx = rack_zone_x + rz_w

    # Patch panel zone
    pp_w = si(PATCH_IN)
    box(dwg, cx, oy + 1, pp_w, view_h - 2,
        "PATCH\nPANEL\n3'-0\"", color="#0a1628", border=CYAN, text_color=CYAN, font=6)
    cx += pp_w

    # CDU zone
    cdu_w = si(CDU_IN)
    box(dwg, cx, oy + 1, cdu_w - 1, view_h - 2,
        "CDU ZONE\n6'-0\"\nPrimary + Redundant\n250 kW each", color="#0a1628", border=CYAN, text_color=CYAN, font=6)

    # Cooling pipe stubs at closed end
    dwg.add(dwg.line((ox + view_w, oy + view_h * 0.3), (ox + view_w + 15, oy + view_h * 0.3),
                     stroke=CYAN, stroke_width=2))
    dwg.add(dwg.text("SUPPLY 45C", insert=(ox + view_w + 18, oy + view_h * 0.3 + 3),
                     fill=CYAN, font_size=5, font_family="Arial"))
    dwg.add(dwg.line((ox + view_w, oy + view_h * 0.7), (ox + view_w + 15, oy + view_h * 0.7),
                     stroke=RED, stroke_width=2))
    dwg.add(dwg.text("RETURN 55-65C", insert=(ox + view_w + 18, oy + view_h * 0.7 + 3),
                     fill=RED, font_size=5, font_family="Arial"))

    # Power entry at door end
    dwg.add(dwg.line((ox, oy + view_h * 0.85), (ox - 15, oy + view_h * 0.85),
                     stroke=PURPLE, stroke_width=2))
    dwg.add(dwg.text("800V DC IN", insert=(ox - 18, oy + view_h * 0.85 + 3),
                     fill=PURPLE, font_size=5, font_family="Arial", text_anchor="end"))

    # Access panels (dashed lines on both long walls) - 4 per side
    # Panels span the rack zone area: 32 ft of panels, 8 ft structural at ends
    panel_zone_start = rack_zone_x  # panels start at rack zone
    panel_zone_end = rack_zone_x + rz_w  # panels end at rack zone
    panel_total_w = panel_zone_end - panel_zone_start
    single_panel_w = panel_total_w / AP_COUNT_PER_SIDE

    for i in range(AP_COUNT_PER_SIDE):
        px1 = panel_zone_start + i * single_panel_w + 2
        px2 = px1 + single_panel_w - 4
        # Top wall panels
        dwg.add(dwg.line((px1, oy), (px2, oy),
                         stroke=ACCENT, stroke_width=2, stroke_dasharray="6,3"))
        dwg.add(dwg.text(f"AP-{i+1}", insert=((px1 + px2) / 2, oy - 5),
                         text_anchor="middle", fill=ACCENT, font_size=5, font_family="Arial"))
        # Bottom wall panels
        dwg.add(dwg.line((px1, oy + view_h), (px2, oy + view_h),
                         stroke=ACCENT, stroke_width=2, stroke_dasharray="6,3"))
        dwg.add(dwg.text(f"AP-{i+5}", insert=((px1 + px2) / 2, oy + view_h + 10),
                         text_anchor="middle", fill=ACCENT, font_size=5, font_family="Arial"))

    # Side clearance labels
    clr_x = rack_zone_x + rz_w / 2
    dwg.add(dwg.text("25.3\" CLR", insert=(clr_x, oy + 10),
                     text_anchor="middle", fill=DIM_TEXT, font_size=5.5, font_family="Arial"))
    dwg.add(dwg.text("25.3\" CLR", insert=(clr_x, oy + view_h - 5),
                     text_anchor="middle", fill=DIM_TEXT, font_size=5.5, font_family="Arial"))

    # Dimension lines
    # Overall length
    dim_h(dwg, ox, ox + view_w, oy + view_h, "39'-5\" (12,032 mm)", 22)
    # Overall width (vertical)
    dim_v(dwg, ox + view_w, oy, oy + view_h, "7'-8\" (2,352 mm)", 60)

    # Zone dimensions along top
    zx = ox
    dim_h(dwg, zx, zx + si(ENTRY_IN), oy, "3'-0\"", -14)
    zx += si(ENTRY_IN)
    dim_h(dwg, zx, zx + si(ELEC_IN), oy, "3'-6\"", -14)
    zx += si(ELEC_IN)
    dim_h(dwg, zx, zx + si(RACK_ZONE_IN), oy, "23'-0\" RACK ZONE (10 racks + 9 gaps @ 4\")", -14)
    zx += si(RACK_ZONE_IN)
    dim_h(dwg, zx, zx + si(PATCH_IN), oy, "3'-0\"", -14)
    zx += si(PATCH_IN)
    dim_h(dwg, zx, zx + si(CDU_IN), oy, "6'-0\"", -14)


def draw_side_view(dwg, ox, oy):
    """VIEW 2: Side view (looking at long wall)."""
    # Scale for side view: length is long, height is shorter
    SL = 1.1   # length scale (same as top)
    SH = 3.5   # height scale (amplified for visibility)

    view_w = CONT_L_IN * SL
    view_h = CONT_H_IN * SH

    # View panel background
    pad = 30
    dwg.add(dwg.rect((ox - pad, oy - 40), (view_w + pad * 2 + 80, view_h + pad + 60),
                     rx=6, fill=ZONE_BG, stroke=BORDER))

    # View title
    dwg.add(dwg.text("VIEW 2 — SIDE VIEW (LOOKING AT LONG WALL)", insert=(ox + view_w / 2, oy - 22),
                     text_anchor="middle", fill=ACCENT, font_size=11,
                     font_family="Arial", font_weight="bold"))

    # Container outline
    dwg.add(dwg.rect((ox, oy), (view_w, view_h), fill=PANEL_BG, stroke=ACCENT, stroke_width=2))

    # Floor line
    floor_y = oy + view_h
    dwg.add(dwg.line((ox - 10, floor_y + 3), (ox + view_w + 10, floor_y + 3),
                     stroke="#4b5563", stroke_width=2))
    dwg.add(dwg.text("CONCRETE PAD", insert=(ox + view_w / 2, floor_y + 14),
                     text_anchor="middle", fill="#4b5563", font_size=6, font_family="Arial"))

    # Racks visible inside (starting after entry + elec zones)
    rack_start_x = ox + (ENTRY_IN + ELEC_IN) * SL
    rack_h = RACK_H_IN * SH
    rack_bottom = floor_y
    rack_top = rack_bottom - rack_h

    # Cable tray above racks
    cable_tray_h = 8
    cable_tray_y = rack_top - 10
    cable_tray_x1 = rack_start_x - 10
    cable_tray_x2 = rack_start_x + RACK_ZONE_IN * SL + 10
    dwg.add(dwg.rect((cable_tray_x1, cable_tray_y), (cable_tray_x2 - cable_tray_x1, cable_tray_h),
                     fill="none", stroke=PURPLE, stroke_width=1, stroke_dasharray="4,2"))
    dwg.add(dwg.text("CABLE TRAY (800V DC + FIBER)", insert=((cable_tray_x1 + cable_tray_x2) / 2, cable_tray_y - 3),
                     text_anchor="middle", fill=PURPLE, font_size=5, font_family="Arial"))

    # Overhead clearance dimension
    dim_v(dwg, cable_tray_x2 + 5, oy, rack_top, "18.2\" CLR", 5)

    # Draw racks as rectangles
    rack_w_px = RACK_W_IN * SL
    gap_px = 4 * SL
    rx = rack_start_x
    rack_types = [
        ("R1", ACCENT), ("R2", ACCENT), ("R3", ACCENT), ("R4", ACCENT),
        ("R5", ACCENT), ("R6", ACCENT), ("R7", ACCENT), ("R8", ACCENT),
        ("R9", BLUE), ("R10", PURPLE),
    ]
    for name, color in rack_types:
        dwg.add(dwg.rect((rx, rack_top), (rack_w_px, rack_h),
                         fill="#0a1a0a" if color == ACCENT else "#0a1628" if color == BLUE else "#1a0a2e",
                         stroke=color, stroke_width=1, rx=1))
        dwg.add(dwg.text(name, insert=(rx + rack_w_px / 2, rack_top + rack_h / 2 + 3),
                         text_anchor="middle", fill=color, font_size=6,
                         font_family="Arial", font_weight="bold"))
        rx += rack_w_px + gap_px

    # Electrical panel at door end
    ep_x = ox + ENTRY_IN * SL
    ep_w = ELEC_IN * SL
    ep_h = rack_h * 0.7
    dwg.add(dwg.rect((ep_x, rack_bottom - ep_h), (ep_w, ep_h),
                     fill="#1a0a2e", stroke=PURPLE, stroke_width=1))
    dwg.add(dwg.text("ELEC", insert=(ep_x + ep_w / 2, rack_bottom - ep_h / 2 + 3),
                     text_anchor="middle", fill=PURPLE, font_size=6, font_family="Arial", font_weight="bold"))

    # CDU at closed end
    cdu_x = ox + (ENTRY_IN + ELEC_IN + RACK_ZONE_IN + PATCH_IN) * SL
    cdu_w = CDU_IN * SL
    cdu_h = rack_h * 0.6
    dwg.add(dwg.rect((cdu_x, rack_bottom - cdu_h), (cdu_w, cdu_h),
                     fill="#0a1628", stroke=CYAN, stroke_width=1))
    dwg.add(dwg.text("CDU", insert=(cdu_x + cdu_w / 2, rack_bottom - cdu_h / 2 + 3),
                     text_anchor="middle", fill=CYAN, font_size=7, font_family="Arial", font_weight="bold"))

    # External connections at CDU end
    dwg.add(dwg.line((ox + view_w, rack_bottom - cdu_h * 0.3), (ox + view_w + 20, rack_bottom - cdu_h * 0.3 - 10),
                     stroke=CYAN, stroke_width=1.5))
    dwg.add(dwg.text("DRY COOLER", insert=(ox + view_w + 22, rack_bottom - cdu_h * 0.3 - 8),
                     fill=CYAN, font_size=5, font_family="Arial"))

    # Power connection at door end
    dwg.add(dwg.line((ox, rack_bottom - ep_h * 0.5), (ox - 20, rack_bottom - ep_h * 0.5 - 10),
                     stroke=PURPLE, stroke_width=1.5))
    dwg.add(dwg.text("800V DC POWER", insert=(ox - 22, rack_bottom - ep_h * 0.5 - 8),
                     fill=PURPLE, font_size=5, font_family="Arial", text_anchor="end"))

    # Access panels (4 on this side, shown as dashed outlines)
    panel_start_x = rack_start_x
    panel_zone_w = RACK_ZONE_IN * SL
    single_panel_w = panel_zone_w / AP_COUNT_PER_SIDE
    panel_h = AP_HEIGHT_IN * SH
    panel_bottom = floor_y
    panel_top = panel_bottom - panel_h

    for i in range(AP_COUNT_PER_SIDE):
        px = panel_start_x + i * single_panel_w + 3
        pw = single_panel_w - 6
        # Panel outline (dashed)
        dwg.add(dwg.rect((px, panel_top), (pw, panel_h),
                         fill="none", stroke=ACCENT, stroke_width=1, stroke_dasharray="4,3", rx=2))
        # Hinge at top
        dwg.add(dwg.line((px + 5, panel_top), (px + pw - 5, panel_top),
                         stroke=ACCENT, stroke_width=2))
        dwg.add(dwg.text(f"AP-{i+1}", insert=(px + pw / 2, panel_top + panel_h / 2),
                         text_anchor="middle", fill=ACCENT, font_size=5, font_family="Arial"))
        dwg.add(dwg.text("TOP-HINGED", insert=(px + pw / 2, panel_top + panel_h / 2 + 8),
                         text_anchor="middle", fill="#555", font_size=4, font_family="Arial"))

    # LED lighting indicators
    for lx in [rack_start_x + 50, rack_start_x + RACK_ZONE_IN * SL / 2, rack_start_x + RACK_ZONE_IN * SL - 50]:
        dwg.add(dwg.circle((lx, oy + 8), r=3, fill="#fbbf24", stroke="none", opacity=0.6))
        dwg.add(dwg.text("LED", insert=(lx, oy + 18), text_anchor="middle",
                         fill="#fbbf24", font_size=4, font_family="Arial"))

    # Dimensions
    dim_h(dwg, ox, ox + view_w, floor_y, "39'-5\" (40-FT HC CONTAINER)", 20)
    dim_v(dwg, ox + view_w, oy, floor_y, "8'-10\" INT HEIGHT", 60)
    # Rack height
    dim_v(dwg, rack_start_x - 15, rack_top, rack_bottom, "88\" RACK", -20)


def draw_end_view(dwg, ox, oy):
    """VIEW 3: End view (looking through door toward racks)."""
    # Scale for end view: width and height both visible
    SE = 3.5   # scale factor

    view_w = CONT_W_IN * SE
    view_h = CONT_H_IN * SE

    # View panel background
    pad = 30
    dwg.add(dwg.rect((ox - pad, oy - 40), (view_w + pad * 2 + 60, view_h + pad + 60),
                     rx=6, fill=ZONE_BG, stroke=BORDER))

    # View title
    dwg.add(dwg.text("VIEW 3 — END VIEW (THROUGH DOOR)", insert=(ox + view_w / 2, oy - 22),
                     text_anchor="middle", fill=ACCENT, font_size=11,
                     font_family="Arial", font_weight="bold"))

    # Container cross-section outline
    dwg.add(dwg.rect((ox, oy), (view_w, view_h), fill=PANEL_BG, stroke=ACCENT, stroke_width=2))

    # Floor
    floor_y = oy + view_h
    dwg.add(dwg.line((ox - 10, floor_y + 3), (ox + view_w + 10, floor_y + 3),
                     stroke="#4b5563", stroke_width=2))
    dwg.add(dwg.text("STEEL CORRUGATED FLOOR + SPREADER PLATES", insert=(ox + view_w / 2, floor_y + 14),
                     text_anchor="middle", fill="#4b5563", font_size=5, font_family="Arial"))

    # Rack centered in cross-section
    rack_w_px = RACK_D_IN * SE   # depth faces us in end view
    rack_h_px = RACK_H_IN * SE
    rack_narrow_px = RACK_W_IN * SE  # width (into the screen)

    rack_cx = ox + view_w / 2
    rack_left = rack_cx - rack_w_px / 2
    rack_bottom = floor_y
    rack_top = rack_bottom - rack_h_px

    # Rack body
    dwg.add(dwg.rect((rack_left, rack_top), (rack_w_px, rack_h_px),
                     fill="#0a2010", stroke=ACCENT, stroke_width=1.5, rx=3))

    # Rack internal detail lines (compute trays)
    tray_count = 9
    for i in range(tray_count):
        ty = rack_top + (i + 1) * rack_h_px / (tray_count + 1)
        dwg.add(dwg.line((rack_left + 5, ty), (rack_left + rack_w_px - 5, ty),
                         stroke=ACCENT, stroke_width=0.3, opacity=0.4))

    # Rack label
    dwg.add(dwg.text("NVL72 RACK", insert=(rack_cx, rack_top + rack_h_px / 2 - 8),
                     text_anchor="middle", fill=ACCENT, font_size=8,
                     font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("42\" DEEP x 23.6\" WIDE", insert=(rack_cx, rack_top + rack_h_px / 2 + 4),
                     text_anchor="middle", fill=LABEL_COLOR, font_size=6, font_family="Arial"))
    dwg.add(dwg.text("88\" TALL / 48U", insert=(rack_cx, rack_top + rack_h_px / 2 + 14),
                     text_anchor="middle", fill=LABEL_COLOR, font_size=6, font_family="Arial"))

    # Side clearances
    left_clear = rack_left - ox
    right_clear = (ox + view_w) - (rack_left + rack_w_px)

    # Left clearance shading
    dwg.add(dwg.rect((ox + 2, rack_top), (left_clear - 4, rack_h_px),
                     fill="none", stroke=DIM_COLOR, stroke_width=0.5, stroke_dasharray="3,3"))
    dwg.add(dwg.text("25.3\"", insert=(ox + left_clear / 2, rack_top + rack_h_px / 2),
                     text_anchor="middle", fill=DIM_TEXT, font_size=7, font_family="Arial"))
    dwg.add(dwg.text("CLR", insert=(ox + left_clear / 2, rack_top + rack_h_px / 2 + 10),
                     text_anchor="middle", fill=DIM_TEXT, font_size=6, font_family="Arial"))

    # Right clearance
    dwg.add(dwg.rect((rack_left + rack_w_px + 2, rack_top), (right_clear - 4, rack_h_px),
                     fill="none", stroke=DIM_COLOR, stroke_width=0.5, stroke_dasharray="3,3"))
    rc_cx = rack_left + rack_w_px + right_clear / 2
    dwg.add(dwg.text("25.3\"", insert=(rc_cx, rack_top + rack_h_px / 2),
                     text_anchor="middle", fill=DIM_TEXT, font_size=7, font_family="Arial"))
    dwg.add(dwg.text("CLR", insert=(rc_cx, rack_top + rack_h_px / 2 + 10),
                     text_anchor="middle", fill=DIM_TEXT, font_size=6, font_family="Arial"))

    # Cable tray overhead
    ct_y = oy + 10
    ct_h = 12
    ct_w = rack_w_px + 30
    ct_left = rack_cx - ct_w / 2
    dwg.add(dwg.rect((ct_left, ct_y), (ct_w, ct_h),
                     fill="none", stroke=PURPLE, stroke_width=1, stroke_dasharray="4,2"))
    dwg.add(dwg.text("CABLE TRAY", insert=(rack_cx, ct_y + ct_h / 2 + 3),
                     text_anchor="middle", fill=PURPLE, font_size=5, font_family="Arial"))

    # Overhead clearance
    dim_v(dwg, rack_left + rack_w_px + 5, rack_top, ct_y + ct_h, "18.2\" OVERHEAD", -25)

    # Access panels on both walls
    ap_h = AP_HEIGHT_IN * SE
    ap_bottom = floor_y
    ap_top = ap_bottom - ap_h

    # Left wall access panel
    dwg.add(dwg.rect((ox, ap_top), (4, ap_h),
                     fill="none", stroke=ACCENT, stroke_width=1.5, stroke_dasharray="5,3"))
    dwg.add(dwg.text("ACCESS", insert=(ox - 8, ap_top + ap_h / 2 - 5),
                     text_anchor="middle", fill=ACCENT, font_size=5, font_family="Arial",
                     transform=f"rotate(-90,{ox - 8},{ap_top + ap_h / 2 - 5})"))
    dwg.add(dwg.text("PANEL", insert=(ox - 16, ap_top + ap_h / 2 - 5),
                     text_anchor="middle", fill=ACCENT, font_size=5, font_family="Arial",
                     transform=f"rotate(-90,{ox - 16},{ap_top + ap_h / 2 - 5})"))

    # Right wall access panel
    dwg.add(dwg.rect((ox + view_w - 4, ap_top), (4, ap_h),
                     fill="none", stroke=ACCENT, stroke_width=1.5, stroke_dasharray="5,3"))
    dwg.add(dwg.text("ACCESS", insert=(ox + view_w + 10, ap_top + ap_h / 2 - 5),
                     text_anchor="middle", fill=ACCENT, font_size=5, font_family="Arial",
                     transform=f"rotate(90,{ox + view_w + 10},{ap_top + ap_h / 2 - 5})"))
    dwg.add(dwg.text("PANEL", insert=(ox + view_w + 18, ap_top + ap_h / 2 - 5),
                     text_anchor="middle", fill=ACCENT, font_size=5, font_family="Arial",
                     transform=f"rotate(90,{ox + view_w + 18},{ap_top + ap_h / 2 - 5})"))

    # Dimension lines
    dim_h(dwg, ox, ox + view_w, floor_y, "7'-8\" (2,352 mm)", 22)
    dim_v(dwg, ox + view_w, oy, floor_y, "8'-10\" (2,698 mm)", 30)
    dim_h(dwg, rack_left, rack_left + rack_w_px, rack_top, "42.0\" RACK DEPTH", -14)
    dim_v(dwg, rack_left - 5, rack_top, rack_bottom, "88\" (7'-4\")", -25)


def build():
    dwg = svgwrite.Drawing(OUT, size=(f"{W}px", f"{H}px"), viewBox=f"0 0 {W} {H}")
    dwg.add(dwg.rect((0, 0), (W, H), fill=BG))

    # Title block
    dwg.add(dwg.text("ADC 3K POD — 40-FT COMPUTE MODULE",
                     insert=(W / 2, 28), text_anchor="middle", fill="#f0f2f5",
                     font_size=18, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("10x NVL72 Racks | 1 SuperPOD + Network + Storage | 1.3 MW",
                     insert=(W / 2, 46), text_anchor="middle", fill=ACCENT,
                     font_size=11, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text(
        "Sheet P-001 | Design Intent | Scale: Conceptual | 2026-03-24 | NOT FOR CONSTRUCTION \u2014 PRELIMINARY DESIGN",
        insert=(W / 2, 60), text_anchor="middle", fill="#6b7280",
        font_size=9, font_family="Arial"))

    # VIEW 1: Top view (upper portion)
    draw_top_view(dwg, 40, 95)

    # VIEW 2: Side view (middle portion)
    draw_side_view(dwg, 40, 310)

    # VIEW 3: End view (lower right)
    draw_end_view(dwg, 620, 720)

    # Legend (lower left)
    leg_x = 40
    leg_y = 720
    dwg.add(dwg.rect((leg_x - 10, leg_y - 10), (540, 170), rx=6, fill=ZONE_BG, stroke=BORDER))
    dwg.add(dwg.text("LEGEND", insert=(leg_x, leg_y + 6), fill=ACCENT, font_size=10,
                     font_family="Arial", font_weight="bold"))

    items = [
        (ACCENT, "#0a2010", "Compute Rack (NVL72 R1-R8) \u2014 130 kW ea, liquid cooled, 72 GPUs + 36 CPUs"),
        (BLUE, "#0a1628", "Networking Rack (R9) \u2014 Quantum InfiniBand spine, Ethernet ToR, patch"),
        (PURPLE, "#1a0a2e", "Storage + Mgmt Rack (R10) \u2014 NVMe-oF, Base Command, monitoring"),
        (CYAN, None, "CDU / Cooling connections (45C supply, 55-65C return)"),
        (PURPLE, None, "800V DC power bus (Eaton Beam Rubin DSX)"),
        (ACCENT, None, "Access panels (dashed) \u2014 8 total, 4 per side, top-hinged, ~8' x 7.5'"),
        ("#fbbf24", None, "LED lighting"),
    ]
    for i, (color, fill_c, text) in enumerate(items):
        iy = leg_y + 22 + i * 14
        if fill_c:
            dwg.add(dwg.rect((leg_x + 5, iy - 6), (14, 8), fill=fill_c, stroke=color,
                             stroke_width=1, rx=2))
        else:
            dwg.add(dwg.line((leg_x + 5, iy - 2), (leg_x + 19, iy - 2), stroke=color, stroke_width=2))
        dwg.add(dwg.text(text, insert=(leg_x + 26, iy + 1), fill=LABEL_COLOR,
                         font_size=7, font_family="Arial"))

    # Key specs summary
    spec_y = leg_y + 128
    specs = [
        "CONTAINER: 40-ft HC ISO (39'5\" x 7'8\" x 8'10\" internal) | TARE: 8,686 lbs | PAYLOAD: 38,864 lbs | GROSS: 47,550 lbs",
        "COMPUTE: 8 NVL72 (576 GPUs, 1 SuperPOD) + 1 NET + 1 STOR = 10 racks | IT LOAD: 1.3 MW | POWER: 800V DC native",
        "COOLING: Direct-to-chip liquid, 45C supply, dual CDU (250 kW ea), external dry cooler | FIRE: Novec 1230 + VESDA",
    ]
    for i, spec in enumerate(specs):
        dwg.add(dwg.text(spec, insert=(leg_x, spec_y + i * 11), fill=NOTE_COLOR,
                         font_size=6.5, font_family="Arial"))

    # Notes
    notes_x = 40
    notes_y = 920
    dwg.add(dwg.rect((notes_x - 10, notes_y - 10), (W - 60, 100), rx=6, fill=ZONE_BG, stroke=BORDER))
    dwg.add(dwg.text("ENGINEERING NOTES", insert=(notes_x, notes_y + 6), fill=ACCENT, font_size=9,
                     font_family="Arial", font_weight="bold"))
    notes = [
        "1. NVL72 is OCP Open Rack V3 (600mm/23.6\" wide), NOT standard 19\" EIA-310. Rack depth 1,068mm (42\").",
        "2. Side clearance 25.3\" does NOT meet NEC 110.26 (30\" min). Access panels solve this \u2014 work from outside.",
        "3. 8 access panels (4/side), top-hinged, ~8' wide x 7.5' tall. 32' of panels span rack zone. 8' structural at ends.",
        "4. CDU zone at closed end: dual 250 kW CDUs, quick-disconnect bulkhead to external dry cooler / facility loop.",
        "5. Floor: 1/4\" steel plate overlay + 1/2\" A36 spreader plates (24\"x44\") under each rack. Point load: 450 PSF.",
        "6. Weight: 10 racks @ 3,300 lbs = 33,000 lbs. Total payload 38,864 lbs. Highway gross 62,550 lbs (under 80K limit).",
        "7. Vera Rubin (H2 2026) may increase to 190-230 kW/rack and ~4,000 lbs/rack. Power/cooling redesign required.",
    ]
    for i, note in enumerate(notes):
        dwg.add(dwg.text(note, insert=(notes_x, notes_y + 20 + i * 11), fill=NOTE_COLOR,
                         font_size=6.5, font_family="Arial"))

    # Footer
    dwg.add(dwg.text("ADC 3K \u2014 Advantage Design & Construction | adc3k.com | scott@adc3k.com",
                     insert=(W / 2, H - 20), text_anchor="middle", fill="#4b5563",
                     font_size=8, font_family="Arial"))
    dwg.add(dwg.text("CONFIDENTIAL \u2014 NOT FOR CONSTRUCTION \u2014 PRELIMINARY DESIGN",
                     insert=(W / 2, H - 8), text_anchor="middle", fill="#333",
                     font_size=7, font_family="Arial"))

    dwg.save()
    print(f"Saved: {OUT}")


if __name__ == "__main__":
    os.makedirs("adc3k-deploy/blueprints", exist_ok=True)
    build()
