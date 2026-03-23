"""
Ragin' Cajun Compute Campus — Trappeys Cannery, Lafayette, LA
Middle High Building Floor Plan (300x75 ft)
Phase 1: 4 NVL72 racks, hot/cold aisle, CDU area, wooden trusses
"""
import svgwrite

W, H = 1400, 950
OUT = "adc3k-deploy/blueprints/trappeys-floor-plan.svg"

ACCENT = "#CE181E"

# Building dimensions in feet
BLDG_W_FT = 300
BLDG_H_FT = 75
SCALE = 3.5  # 1 ft = 3.5 pixels
BLDG_W = int(BLDG_W_FT * SCALE)  # 1050px
BLDG_H = int(BLDG_H_FT * SCALE)  # 262px
ORIGIN_X = 160
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

    # -- TITLE BLOCK --
    dwg.add(dwg.text("RAGIN' CAJUN COMPUTE CAMPUS — TRAPPEYS CANNERY, LAFAYETTE, LA",
                      insert=(W / 2, 24), text_anchor="middle", fill="#f0f2f5",
                      font_size=16, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("MIDDLE HIGH BUILDING FLOOR PLAN | PHASE 1: 4 NVL72 RACKS | 520 kW IT LOAD",
                      insert=(W / 2, 40), text_anchor="middle", fill=ACCENT,
                      font_size=10, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("Sheet A-001 | Design Intent | Scale: Conceptual | 2026-03-23 | NOT FOR CONSTRUCTION",
                      insert=(W / 2, 54), text_anchor="middle", fill="#6b7280",
                      font_size=9, font_family="Arial"))

    bx, by = ORIGIN_X, ORIGIN_Y

    # ================================================================
    # BUILDING ENVELOPE
    # ================================================================
    dwg.add(dwg.rect((bx, by), (BLDG_W, BLDG_H), fill="#0d0d12", stroke=ACCENT, stroke_width=2))

    # Dimensions
    dim_line(dwg, bx, by + BLDG_H, bx + BLDG_W, by + BLDG_H, f"{BLDG_W_FT}'-0\"", 20)
    dim_line(dwg, bx + BLDG_W, by, bx + BLDG_W, by + BLDG_H, f"{BLDG_H_FT}'-0\"", 20)

    # Wooden trusses (shown as dashed lines across the ceiling)
    truss_spacing = 20 * SCALE  # 20 ft spacing
    for i in range(1, int(BLDG_W_FT / 20)):
        tx = bx + i * truss_spacing
        dwg.add(dwg.line((tx, by), (tx, by + BLDG_H), stroke="#2a1a0a", stroke_width=0.5,
                          stroke_dasharray="6,4"))
    # Truss label
    dwg.add(dwg.text("WOODEN TRUSSES (20' O.C.)", insert=(bx + BLDG_W / 2, by + 12),
                      text_anchor="middle", fill="#5a3a1a", font_size=7, font_family="Arial"))

    # Grid column labels
    for i in range(0, int(BLDG_W_FT / 25) + 1):
        gx = bx + i * 25 * SCALE
        dwg.add(dwg.line((gx, by - 10), (gx, by + BLDG_H + 5), stroke="#1e2230", stroke_width=0.5,
                          stroke_dasharray="4,4"))
        dwg.add(dwg.text(chr(65 + i), insert=(gx, by - 15), text_anchor="middle",
                          fill="#555", font_size=8, font_family="Arial", font_weight="bold"))

    # ================================================================
    # CDU AREA (LEFT SIDE — 25 ft)
    # ================================================================
    cdu_w = int(25 * SCALE)
    box(dwg, bx, by, cdu_w, BLDG_H,
        "CDU AREA\n\nCoolant Distribution\nUnits (N+1)\nPumps + Valves\nPipe Headers\n\n25' x 75'",
        color="#111318", border="#4fc3f7", text_color="#4fc3f7")

    # CDU boxes inside
    for cy_offset in [25, 95, 165]:
        box(dwg, bx + 8, by + cy_offset, int(10 * SCALE), int(8 * SCALE),
            "CDU", color="#0a1628", border="#4fc3f7", text_color="#4fc3f7", font=7)

    # ================================================================
    # ELECTRICAL ROOM (RIGHT SIDE — 20 ft)
    # ================================================================
    elec_w = int(20 * SCALE)
    elec_x = bx + BLDG_W - elec_w
    box(dwg, elec_x, by, elec_w, int(40 * SCALE),
        "ELECTRICAL\nROOM\n\n800V DC Busway\nPDUs | Panels\n\n20' x 40'",
        color="#111318", border="#8b5cf6", text_color="#c4b5fd")

    # Network room below electrical
    box(dwg, elec_x, by + int(40 * SCALE), elec_w, BLDG_H - int(40 * SCALE),
        "NETWORK\nROOM\n\nTOR Switches\nSpine/Leaf\n\n20' x 35'",
        color="#111318", border="#3b82f6", text_color="#93c5fd")

    # ================================================================
    # COMPUTE FLOOR — 4 NVL72 RACKS
    # ================================================================
    compute_x = bx + cdu_w + int(5 * SCALE)
    compute_w = BLDG_W - cdu_w - elec_w - int(10 * SCALE)

    # Rack dimensions: NVL72 ~2ft wide x 4ft deep
    rack_w = int(2 * SCALE)
    rack_d = int(4 * SCALE)

    # 2 rows of 2 racks (paired for hot aisle containment)
    # Center the rack cluster in the compute area
    cluster_w = 2 * rack_w + int(6 * SCALE)  # 2 racks + gap
    cluster_start_x = compute_x + (compute_w - cluster_w) // 2

    row_center_y = by + BLDG_H // 2

    # Row 1 (2 racks facing down)
    row1_y = row_center_y - rack_d - int(3 * SCALE)
    for r in range(2):
        rx = cluster_start_x + r * (rack_w + int(6 * SCALE))
        box(dwg, rx, row1_y, rack_w, rack_d, "", color="#1a2e0a", border="#76b900")
        dwg.add(dwg.text(f"R{r + 1}", insert=(rx + rack_w / 2, row1_y + rack_d / 2 + 3),
                          text_anchor="middle", fill="#76b900", font_size=7, font_family="Arial", font_weight="bold"))

    # Hot aisle between rows
    hot_y = row1_y + rack_d
    hot_h = int(6 * SCALE)
    dwg.add(dwg.rect((cluster_start_x - int(2 * SCALE), hot_y),
                      (cluster_w + int(4 * SCALE), hot_h),
                      fill="#1a0a0a", rx=3))
    dwg.add(dwg.text("HOT AISLE (CONTAINED)", insert=(cluster_start_x + cluster_w / 2, hot_y + hot_h / 2 + 3),
                      text_anchor="middle", fill="#ef4444", font_size=7, font_family="Arial", font_weight="bold"))

    # Row 2 (2 racks facing up)
    row2_y = hot_y + hot_h
    for r in range(2):
        rx = cluster_start_x + r * (rack_w + int(6 * SCALE))
        box(dwg, rx, row2_y, rack_w, rack_d, "", color="#1a2e0a", border="#76b900")
        dwg.add(dwg.text(f"R{r + 3}", insert=(rx + rack_w / 2, row2_y + rack_d / 2 + 3),
                          text_anchor="middle", fill="#76b900", font_size=7, font_family="Arial", font_weight="bold"))

    # Cold aisles above and below
    cold_above_y = row1_y - int(4 * SCALE)
    cold_below_y = row2_y + rack_d
    for cy in [cold_above_y, cold_below_y]:
        dwg.add(dwg.rect((cluster_start_x - int(2 * SCALE), cy),
                          (cluster_w + int(4 * SCALE), int(4 * SCALE)),
                          fill="#0a0a1e", rx=3))
        dwg.add(dwg.text("COLD AISLE",
                          insert=(cluster_start_x + cluster_w / 2, cy + int(2 * SCALE) + 3),
                          text_anchor="middle", fill="#3b82f6", font_size=7, font_family="Arial", font_weight="bold"))

    # Rack labels
    dwg.add(dwg.text("4x NVIDIA NVL72 RACKS | 130 kW each | 520 kW total",
                      insert=(cluster_start_x + cluster_w / 2, row1_y - int(6 * SCALE)),
                      text_anchor="middle", fill="#76b900", font_size=8, font_family="Arial", font_weight="bold"))

    # Cable tray (overhead, shown as dashed)
    cable_y1 = by + int(5 * SCALE)
    cable_y2 = by + BLDG_H - int(5 * SCALE)
    cable_x = cluster_start_x + cluster_w + int(8 * SCALE)
    dwg.add(dwg.line((cable_x, cable_y1), (cable_x, cable_y2),
                      stroke="#8b5cf6", stroke_width=1, stroke_dasharray="8,4"))
    dwg.add(dwg.text("CABLE TRAY", insert=(cable_x + 5, by + BLDG_H / 2),
                      fill="#8b5cf6", font_size=6, font_family="Arial",
                      transform=f"rotate(90, {cable_x + 5}, {by + BLDG_H / 2})"))

    # Cooling pipe runs (supply and return along CDU wall)
    pipe_x = compute_x - int(2 * SCALE)
    dwg.add(dwg.line((pipe_x, by + 10), (pipe_x, by + BLDG_H - 10), stroke="#4fc3f7", stroke_width=2))
    dwg.add(dwg.line((pipe_x - 5, by + 10), (pipe_x - 5, by + BLDG_H - 10), stroke="#ff6b6b", stroke_width=2))
    dwg.add(dwg.text("S", insert=(pipe_x + 2, by + 20), fill="#4fc3f7", font_size=6, font_family="Arial"))
    dwg.add(dwg.text("R", insert=(pipe_x - 8, by + 20), fill="#ff6b6b", font_size=6, font_family="Arial"))

    # Cooling pipes from water tower (external, top of building)
    dwg.add(dwg.line((bx + cdu_w / 2, by), (bx + cdu_w / 2, by - 30), stroke="#4fc3f7", stroke_width=2))
    dwg.add(dwg.text("FROM WATER TOWER", insert=(bx + cdu_w / 2 + 5, by - 20),
                      fill="#4fc3f7", font_size=7, font_family="Arial"))
    dwg.add(dwg.line((bx + cdu_w / 2 + 15, by), (bx + cdu_w / 2 + 15, by - 30), stroke="#ff6b6b", stroke_width=2))
    dwg.add(dwg.text("RETURN", insert=(bx + cdu_w / 2 + 20, by - 12),
                      fill="#ff6b6b", font_size=7, font_family="Arial"))

    # ================================================================
    # LOADING ACCESS (REAR / RIGHT SIDE)
    # ================================================================
    # Loading door at right side of building
    door_y = by + BLDG_H / 2 - 15
    dwg.add(dwg.rect((bx + BLDG_W - 2, door_y), (6, 30), fill=ACCENT, rx=2))
    dwg.add(dwg.text("LOADING", insert=(bx + BLDG_W + 10, door_y + 12),
                      fill="#6b7280", font_size=7, font_family="Arial"))
    dwg.add(dwg.text("ACCESS", insert=(bx + BLDG_W + 10, door_y + 22),
                      fill="#6b7280", font_size=7, font_family="Arial"))
    dwg.add(dwg.text("(from Rear High)", insert=(bx + BLDG_W + 10, door_y + 32),
                      fill="#555", font_size=6, font_family="Arial"))

    # Main entry (front / left end)
    dwg.add(dwg.rect((bx - 2, by + BLDG_H / 2 - 12), (6, 24), fill=ACCENT, rx=2))
    dwg.add(dwg.text("ENTRY", insert=(bx - 30, by + BLDG_H / 2 + 4),
                      fill="#6b7280", font_size=7, font_family="Arial"))

    # ================================================================
    # EXPANSION ZONE label
    # ================================================================
    # Show expansion area within the building
    exp_x = compute_x
    exp_y = by + BLDG_H + 35
    dwg.add(dwg.rect((exp_x, exp_y), (compute_w, 40), fill="#111318", stroke="#333",
                      stroke_width=1, stroke_dasharray="6,3", rx=4))
    dwg.add(dwg.text("FUTURE EXPANSION ZONE — Phase 2: up to 36 racks (Middle Low building remodel)",
                      insert=(exp_x + compute_w / 2, exp_y + 22), text_anchor="middle",
                      fill="#555", font_size=8, font_family="Arial"))

    # ================================================================
    # NORTH ARROW
    # ================================================================
    na_x, na_y = 80, 130
    dwg.add(dwg.polygon([(na_x, na_y - 25), (na_x - 8, na_y), (na_x + 8, na_y)], fill="#fff"))
    dwg.add(dwg.text("N", insert=(na_x, na_y - 30), text_anchor="middle", fill="#fff",
                      font_size=12, font_family="Arial", font_weight="bold"))

    # ================================================================
    # CAMPUS CONTEXT (show all 4 buildings, small)
    # ================================================================
    ctx_x = 50
    ctx_y = 490
    dwg.add(dwg.text("CAMPUS CONTEXT — 4 BUILDINGS", insert=(ctx_x, ctx_y - 8),
                      fill="#6b7280", font_size=9, font_family="Arial", font_weight="bold"))

    campus_scale = 0.8  # pixels per foot
    bldgs = [
        ("FRONT", 300, 75, "Museum / Education / Control Room / Bayou View", "#3b82f6"),
        ("MIDDLE LOW", 300, 100, "Phase 2 Remodel — 30,000 sq ft", "#6b7280"),
        ("MIDDLE HIGH", 300, 75, "PHASE 1 DEPLOY — GPU Compute Hall (THIS DRAWING)", ACCENT),
        ("REAR HIGH", 250, 150, "Staging Area — 37,500 sq ft", "#6b7280"),
    ]
    cy = ctx_y
    for name, w_ft, h_ft, desc, color in bldgs:
        bw = int(w_ft * campus_scale)
        bh = int(h_ft * campus_scale)
        is_active = "PHASE 1" in desc
        fill = "#1a0a0a" if is_active else "#0d0d12"
        dwg.add(dwg.rect((ctx_x, cy), (bw, bh), fill=fill, stroke=color,
                          stroke_width=2 if is_active else 1, rx=3))
        dwg.add(dwg.text(f"{name} ({w_ft}' x {h_ft}' = {w_ft * h_ft:,} sf)",
                          insert=(ctx_x + 10, cy + 14), fill=color,
                          font_size=8, font_family="Arial", font_weight="bold"))
        dwg.add(dwg.text(desc, insert=(ctx_x + 10, cy + 26), fill="#6b7280",
                          font_size=7, font_family="Arial"))
        cy += bh + 8

    # Total
    dwg.add(dwg.text("TOTAL: 112,500 sq ft across 4 buildings", insert=(ctx_x, cy + 10),
                      fill=ACCENT, font_size=9, font_family="Arial", font_weight="bold"))

    # ================================================================
    # LEGEND + STATS
    # ================================================================
    ly = 490
    leg_x = 400
    dwg.add(dwg.rect((leg_x, ly), (550, 120), rx=6, fill="#111318", stroke="#1e2230"))

    lx = leg_x + 20
    items = [
        ("#76b900", "#1a2e0a", "NVL72 Rack (2' x 4') — 130 kW liquid cooled"),
        ("#ef4444", "#1a0a0a", "Hot Aisle (Contained)"),
        ("#3b82f6", "#0a0a1e", "Cold Aisle"),
        ("#4fc3f7", None, "Supply Pipe (Cold — from water tower)"),
        ("#ff6b6b", None, "Return Pipe (Hot — to dry coolers)"),
        ("#8b5cf6", None, "Cable Tray (overhead 800V DC busway)"),
        ("#5a3a1a", None, "Wooden Trusses (existing structure)"),
    ]
    for i, (color, fill, text) in enumerate(items):
        iy = ly + 12 + i * 14
        if fill:
            dwg.add(dwg.rect((lx, iy - 6), (14, 10), fill=fill, stroke=color, stroke_width=1, rx=2))
        else:
            dwg.add(dwg.line((lx, iy), (lx + 14, iy), stroke=color, stroke_width=2))
        dwg.add(dwg.text(text, insert=(lx + 20, iy + 3), fill="#9ca3af", font_size=8, font_family="Arial"))

    # Stats column
    stat_x = leg_x + 310
    stats = [
        ("BUILDING", f"{BLDG_W_FT}' x {BLDG_H_FT}'\n22,500 sq ft"),
        ("PHASE 1 RACKS", "4x NVL72\n520 kW IT"),
        ("GPUs", "288 total\n72 per rack"),
        ("COOLING", "Water Tower\n+ Dry Coolers"),
    ]
    for i, (label, value) in enumerate(stats):
        sx_pos = stat_x
        sy_pos = ly + 12 + i * 26
        dwg.add(dwg.text(label, insert=(sx_pos, sy_pos), fill="#6b7280",
                          font_size=8, font_family="Arial", font_weight="bold"))
        for j, line in enumerate(value.split("\n")):
            dwg.add(dwg.text(line, insert=(sx_pos + 100, sy_pos + j * 11), fill=ACCENT,
                              font_size=9, font_family="Arial", font_weight="bold"))

    # ================================================================
    # NOTES
    # ================================================================
    ny = 800
    notes = [
        "1. Middle High building: 300' x 75' = 22,500 sq ft — existing wooden truss structure, highest ceiling clearance",
        "2. Phase 1 deploys 4x NVL72 racks in hot/cold aisle containment — 130 kW each, 520 kW total IT load",
        "3. CDU area houses coolant distribution units with N+1 redundancy — pipes run to/from water tower via dry coolers",
        "4. 800V DC busway runs overhead via cable tray from electrical room to each rack position",
        "5. Loading access from Rear High building (37,500 sf staging area) — forklifts, crates, rack delivery",
        "6. Wooden trusses are original Trappeys Cannery construction — structural assessment required before rack loading",
        "7. Reinforced slab required at rack positions: NVL72 ~2,500 lbs loaded, ~250 lb/sq ft concentrated",
        "8. Phase 2 expansion into Middle Low building (300' x 100' = 30,000 sf) adds up to 32 more racks",
        "9. Fire suppression: clean agent (Novec 1230) in compute area, wet pipe in support spaces",
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
