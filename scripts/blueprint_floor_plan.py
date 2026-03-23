"""
Willow Glen Tiger Compute Campus — Compute Hall Floor Plan
NVL72 rack layout, hot/cold aisles, CDUs, mechanical room, NOC
SVG output — Scale: 1/8" = 1'-0" (conceptual)
Building: ~200 ft x 100 ft = 20,000 sq ft compute hall
"""
import svgwrite

W, H = 1400, 950
OUT = "adc3k-deploy/blueprints/floor-plan.svg"

# Building dimensions in feet (conceptual)
BLDG_W_FT = 200
BLDG_H_FT = 100
# Scale: 1 ft = 5 pixels
SCALE = 5
BLDG_W = BLDG_W_FT * SCALE  # 1000px
BLDG_H = BLDG_H_FT * SCALE  # 500px
ORIGIN_X = 180
ORIGIN_Y = 100


def ft_to_px(ft_x, ft_y):
    return (ORIGIN_X + ft_x * SCALE, ORIGIN_Y + ft_y * SCALE)


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
    """Dimension line with label."""
    if y1 == y2:  # horizontal
        dy = offset
        dwg.add(dwg.line((x1, y1 + dy), (x2, y2 + dy), stroke="#555", stroke_width=0.5))
        dwg.add(dwg.line((x1, y1 + dy - 4), (x1, y1 + dy + 4), stroke="#555", stroke_width=0.5))
        dwg.add(dwg.line((x2, y2 + dy - 4), (x2, y2 + dy + 4), stroke="#555", stroke_width=0.5))
        dwg.add(dwg.text(label, insert=((x1 + x2) / 2, y1 + dy - 3), text_anchor="middle",
                          fill="#888", font_size=7, font_family="Arial"))
    else:  # vertical
        dx = offset
        dwg.add(dwg.line((x1 + dx, y1), (x2 + dx, y2), stroke="#555", stroke_width=0.5))
        dwg.add(dwg.line((x1 + dx - 4, y1), (x1 + dx + 4, y1), stroke="#555", stroke_width=0.5))
        dwg.add(dwg.line((x2 + dx - 4, y2), (x2 + dx + 4, y2), stroke="#555", stroke_width=0.5))
        dwg.add(dwg.text(label, insert=(x1 + dx + 5, (y1 + y2) / 2), fill="#888",
                          font_size=7, font_family="Arial"))


def build():
    dwg = svgwrite.Drawing(OUT, size=(f"{W}px", f"{H}px"), viewBox=f"0 0 {W} {H}")
    dwg.add(dwg.rect((0, 0), (W, H), fill="#0a0b0f"))

    # ── TITLE BLOCK ──
    dwg.add(dwg.text("TIGER COMPUTE CAMPUS — WILLOW GLEN, ST. GABRIEL, LA",
                      insert=(W / 2, 24), text_anchor="middle", fill="#f0f2f5",
                      font_size=16, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("COMPUTE HALL FLOOR PLAN | PHASE 1: 36 NVL72 RACKS | 4.68 MW IT LOAD",
                      insert=(W / 2, 40), text_anchor="middle", fill="#76b900",
                      font_size=10, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("Sheet A-001 | MVP Design Intent | Scale: Conceptual 1/8\"=1'-0\" | 2026-03-22 | NOT FOR CONSTRUCTION",
                      insert=(W / 2, 54), text_anchor="middle", fill="#6b7280",
                      font_size=9, font_family="Arial"))

    # ════════════════════════════════════════════
    # BUILDING ENVELOPE
    # ════════════════════════════════════════════
    bx, by = ORIGIN_X, ORIGIN_Y
    dwg.add(dwg.rect((bx, by), (BLDG_W, BLDG_H), fill="#0d0d12", stroke="#3b82f6", stroke_width=2))

    # Building dimensions
    dim_line(dwg, bx, by + BLDG_H, bx + BLDG_W, by + BLDG_H, f"{BLDG_W_FT}'-0\"", 20)
    dim_line(dwg, bx + BLDG_W, by, bx + BLDG_W, by + BLDG_H, f"{BLDG_H_FT}'-0\"", 20)

    # Grid lines (columns at 25 ft spacing)
    for i in range(9):  # 8 bays x 25 ft = 200 ft
        gx = bx + i * 25 * SCALE
        dwg.add(dwg.line((gx, by - 10), (gx, by + BLDG_H + 5), stroke="#1e2230", stroke_width=0.5,
                          stroke_dasharray="4,4"))
        dwg.add(dwg.text(chr(65 + i), insert=(gx, by - 15), text_anchor="middle",
                          fill="#555", font_size=8, font_family="Arial", font_weight="bold"))

    # ════════════════════════════════════════════
    # MECHANICAL ROOM (LEFT SIDE)
    # ════════════════════════════════════════════
    mech_w = 30 * SCALE  # 30 ft
    box(dwg, bx, by, mech_w, BLDG_H, "MECHANICAL\nROOM\n\nCDUs (N+1)\nPumps\nValves\nPipe Headers\nElec Panels\n\n30' x 100'",
        color="#111318", border="#4fc3f7", text_color="#4fc3f7")

    # CDU positions inside mech room
    cdu_positions = [130, 210, 290, 370, 450]
    for cy in cdu_positions:
        box(dwg, bx + 10, by + (cy - ORIGIN_Y) - 5, 50, 25, "CDU", color="#0a1628", border="#4fc3f7", text_color="#4fc3f7", font=7)

    # ════════════════════════════════════════════
    # NOC / OFFICE (RIGHT SIDE)
    # ════════════════════════════════════════════
    noc_w = 25 * SCALE  # 25 ft
    noc_x = bx + BLDG_W - noc_w
    box(dwg, noc_x, by, noc_w, BLDG_H * 0.5, "NOC\nNetwork Ops\nCenter\n\nMonitor Wall\nWorkstations\n\n25' x 50'",
        color="#111318", border="#3b82f6", text_color="#93c5fd")

    # Loading dock below NOC
    box(dwg, noc_x, by + BLDG_H * 0.5, noc_w, BLDG_H * 0.25, "LOADING\nDOCK\n\n25' x 25'",
        color="#111318", border="#6b7280", text_color="#9ca3af")

    # Electrical room
    box(dwg, noc_x, by + BLDG_H * 0.75, noc_w, BLDG_H * 0.25, "ELECTRICAL\nROOM\n\nPDUs\n800V DC\nBusway\n\n25' x 25'",
        color="#111318", border="#8b5cf6", text_color="#c4b5fd")

    # ════════════════════════════════════════════
    # COMPUTE FLOOR — NVL72 RACKS
    # ════════════════════════════════════════════
    compute_x = bx + mech_w + 5  # Start after mech room
    compute_w = BLDG_W - mech_w - noc_w - 10  # Available width
    # 145 ft x 100 ft compute area

    # Rack dimensions: NVL72 is roughly 24" wide x 48" deep = 2ft x 4ft
    rack_w = 2 * SCALE  # 10px
    rack_d = 4 * SCALE  # 20px

    # Hot aisle / cold aisle layout
    # 6 rows of racks, paired into 3 hot-aisle containment pods
    # Each row: 6 racks = 12 ft wide, with 4 ft aisles

    row_spacing = 14 * SCALE  # 14 ft center-to-center between paired rows
    pod_spacing = 8 * SCALE   # 8 ft between pods (cold aisle)
    racks_per_row = 6

    # Calculate vertical centering
    total_depth = 3 * row_spacing + 2 * pod_spacing
    start_y = by + (BLDG_H - total_depth) / 2

    row_configs = []  # Store positions for labeling

    pod_colors = [
        {"hot": "#2a1a1a", "cold": "#1a1a2a"},
        {"hot": "#2a1a1a", "cold": "#1a1a2a"},
        {"hot": "#2a1a1a", "cold": "#1a1a2a"},
    ]

    current_y = start_y
    for pod in range(3):
        # Cold aisle label
        cold_y = current_y
        if pod > 0:
            dwg.add(dwg.rect((compute_x, cold_y - pod_spacing + 5), (compute_w, pod_spacing - 10),
                              fill="#0a0a1e", rx=3))
            dwg.add(dwg.text("COLD AISLE", insert=(compute_x + compute_w / 2, cold_y - pod_spacing / 2 + 4),
                              text_anchor="middle", fill="#3b82f6", font_size=8, font_family="Arial", font_weight="bold"))

        # Row A (facing right →)
        for r in range(racks_per_row):
            rx = compute_x + 15 + r * (rack_w + 8)
            ry = current_y
            box(dwg, rx, ry, rack_w, rack_d, "", color="#1a2e0a", border="#76b900")

        row_label_a = f"Row {pod * 2 + 1} — Racks {pod * 12 + 1}-{pod * 12 + 6}"
        dwg.add(dwg.text(row_label_a, insert=(compute_x + compute_w - 20, current_y + rack_d / 2 + 3),
                          text_anchor="end", fill="#76b900", font_size=7, font_family="Arial"))

        # Hot aisle between paired rows
        hot_y = current_y + rack_d
        hot_h = row_spacing - 2 * rack_d
        dwg.add(dwg.rect((compute_x + 5, hot_y), (compute_w - 10, hot_h),
                          fill="#1a0a0a", rx=3))
        dwg.add(dwg.text("HOT AISLE (CONTAINED)", insert=(compute_x + compute_w / 2, hot_y + hot_h / 2 + 3),
                          text_anchor="middle", fill="#ef4444", font_size=7, font_family="Arial", font_weight="bold"))

        # Row B (facing left ←)
        row_b_y = current_y + row_spacing - rack_d
        for r in range(racks_per_row):
            rx = compute_x + 15 + r * (rack_w + 8)
            box(dwg, rx, row_b_y, rack_w, rack_d, "", color="#1a2e0a", border="#76b900")

        row_label_b = f"Row {pod * 2 + 2} — Racks {pod * 12 + 7}-{pod * 12 + 12}"
        dwg.add(dwg.text(row_label_b, insert=(compute_x + compute_w - 20, row_b_y + rack_d / 2 + 3),
                          text_anchor="end", fill="#76b900", font_size=7, font_family="Arial"))

        current_y += row_spacing + pod_spacing

    # Final cold aisle
    dwg.add(dwg.rect((compute_x, current_y - pod_spacing + 5), (compute_w, pod_spacing - 10),
                      fill="#0a0a1e", rx=3))
    dwg.add(dwg.text("COLD AISLE", insert=(compute_x + compute_w / 2, current_y - pod_spacing / 2 + 4),
                      text_anchor="middle", fill="#3b82f6", font_size=8, font_family="Arial", font_weight="bold"))

    # Cooling pipe runs (supply and return headers along mech room wall)
    pipe_x = compute_x - 3
    dwg.add(dwg.line((pipe_x, by + 10), (pipe_x, by + BLDG_H - 10), stroke="#4fc3f7", stroke_width=2))
    dwg.add(dwg.line((pipe_x - 5, by + 10), (pipe_x - 5, by + BLDG_H - 10), stroke="#ff6b6b", stroke_width=2))
    dwg.add(dwg.text("S", insert=(pipe_x + 2, by + 20), fill="#4fc3f7", font_size=6, font_family="Arial"))
    dwg.add(dwg.text("R", insert=(pipe_x - 8, by + 20), fill="#ff6b6b", font_size=6, font_family="Arial"))

    # ════════════════════════════════════════════
    # DOORS
    # ════════════════════════════════════════════
    # Main entrance (bottom center)
    door_x = bx + BLDG_W / 2 - 15
    dwg.add(dwg.rect((door_x, by + BLDG_H - 2), (30, 6), fill="#3b82f6", rx=2))
    dwg.add(dwg.text("MAIN ENTRY", insert=(door_x + 15, by + BLDG_H + 12), text_anchor="middle",
                      fill="#6b7280", font_size=7, font_family="Arial"))

    # Loading dock door
    dwg.add(dwg.rect((noc_x + noc_w - 2, by + BLDG_H * 0.55), (6, 30), fill="#6b7280", rx=2))
    dwg.add(dwg.text("DOCK", insert=(noc_x + noc_w + 10, by + BLDG_H * 0.57), fill="#6b7280",
                      font_size=7, font_family="Arial"))

    # ════════════════════════════════════════════
    # NORTH ARROW
    # ════════════════════════════════════════════
    na_x, na_y = 80, 130
    dwg.add(dwg.polygon([(na_x, na_y - 25), (na_x - 8, na_y), (na_x + 8, na_y)], fill="#fff"))
    dwg.add(dwg.text("N", insert=(na_x, na_y - 30), text_anchor="middle", fill="#fff",
                      font_size=12, font_family="Arial", font_weight="bold"))

    # ════════════════════════════════════════════
    # LEGEND + STATS
    # ════════════════════════════════════════════
    ly = 660
    dwg.add(dwg.rect((ORIGIN_X, ly), (BLDG_W, 120), rx=6, fill="#111318", stroke="#1e2230"))

    # Rack legend
    lx = ORIGIN_X + 20
    items = [
        ("#76b900", "#1a2e0a", "NVL72 Rack (2' x 4')"),
        ("#ef4444", "#1a0a0a", "Hot Aisle (Contained)"),
        ("#3b82f6", "#0a0a1e", "Cold Aisle"),
        ("#4fc3f7", None, "Supply Pipe (Cold)"),
        ("#ff6b6b", None, "Return Pipe (Hot)"),
    ]
    for i, (color, fill, text) in enumerate(items):
        iy = ly + 15 + i * 16
        if fill:
            dwg.add(dwg.rect((lx, iy - 6), (14, 10), fill=fill, stroke=color, stroke_width=1, rx=2))
        else:
            dwg.add(dwg.line((lx, iy), (lx + 14, iy), stroke=color, stroke_width=2))
        dwg.add(dwg.text(text, insert=(lx + 20, iy + 3), fill="#9ca3af", font_size=8, font_family="Arial"))

    # Stats
    sx = ORIGIN_X + 250
    stats = [
        ("BUILDING", "200' x 100'\n20,000 sq ft"),
        ("COMPUTE FLOOR", "145' x 100'\n14,500 sq ft"),
        ("RACKS", "36 NVL72\n6 rows x 6 racks"),
        ("IT LOAD", "4.68 MW\n130 kW/rack"),
        ("GPUs", "2,592 total\n72 per rack"),
        ("COOLING", "Hot/Cold Aisle\nContained Hot"),
        ("AISLE WIDTH", "4' hot\n8' cold"),
        ("FLOOR LOAD", "~250 lb/sq ft\nReinforced slab"),
    ]
    for i, (label, value) in enumerate(stats):
        col = i % 4
        row = i // 4
        sx_pos = ORIGIN_X + 250 + col * 190
        sy_pos = ly + 12 + row * 50
        dwg.add(dwg.text(label, insert=(sx_pos, sy_pos), fill="#6b7280",
                          font_size=8, font_family="Arial", font_weight="bold"))
        for j, line in enumerate(value.split("\n")):
            dwg.add(dwg.text(line, insert=(sx_pos, sy_pos + 12 + j * 11), fill="#76b900",
                              font_size=10, font_family="Arial", font_weight="bold"))

    # ════════════════════════════════════════════
    # NOTES
    # ════════════════════════════════════════════
    ny = 800
    notes = [
        "1. NVL72 rack: 72 Vera Rubin GPUs, 130 kW, liquid cooled, 45C hot water supply, ~2,500 lbs loaded",
        "2. Hot aisle containment prevents mixing of exhaust and supply air — critical for 130 kW/rack density",
        "3. CDUs in mechanical room: N+1 redundancy, one pair per row, facility loop to rack manifolds",
        "4. 800V DC busway runs overhead from electrical room to each rack position (not shown for clarity)",
        "5. Reinforced concrete slab required: ~250 lb/sq ft concentrated load at rack positions",
        "6. 18\" raised floor optional — NVIDIA DSX allows overhead cable tray + underfloor cooling manifold",
        "7. Phase 1 = 36 racks. Building designed for expansion to 72 racks (double rows, add 3 pods)",
        "8. Fire suppression: clean agent (FM-200 or Novec 1230) in compute area, wet pipe in support spaces",
    ]
    for i, note in enumerate(notes):
        dwg.add(dwg.text(note, insert=(35, ny + i * 13), fill="#4b5563",
                          font_size=7.5, font_family="Arial"))

    dwg.save()
    print(f"Saved: {OUT}")


if __name__ == "__main__":
    import os
    os.makedirs("adc3k-deploy/blueprints", exist_ok=True)
    build()
