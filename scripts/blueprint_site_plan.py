"""
Willow Glen Tiger Compute Campus — Site Plan
700 acres, buildings, substations, solar zones, river, dock, generators
SVG output
"""
import svgwrite

W, H = 1400, 1000
OUT = "adc3k-deploy/willow-glen/blueprints/site-plan.svg"

# Approximate site layout based on satellite imagery and helicam photos
# Property is roughly 3,500 ft along river (N-S) x ~4,000 ft deep (E-W)
# Scale: 1 ft = 0.25 px (1 pixel = 4 ft)
S = 0.25
OX, OY = 100, 80  # origin offset


def ft(x, y):
    return (OX + x * S, OY + y * S)


def ft_rect(dwg, x, y, w, h, **kwargs):
    px, py = ft(x, y)
    dwg.add(dwg.rect((px, py), (w * S, h * S), **kwargs))


def ft_text(dwg, x, y, text, **kwargs):
    px, py = ft(x, y)
    dwg.add(dwg.text(text, insert=(px, py), **kwargs))


def build():
    dwg = svgwrite.Drawing(OUT, size=(f"{W}px", f"{H}px"), viewBox=f"0 0 {W} {H}")
    dwg.add(dwg.rect((0, 0), (W, H), fill="#0a0b0f"))

    # ── TITLE BLOCK ──
    dwg.add(dwg.text("TIGER COMPUTE CAMPUS — WILLOW GLEN, ST. GABRIEL, LA",
                      insert=(W / 2, 22), text_anchor="middle", fill="#f0f2f5",
                      font_size=15, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("SITE PLAN | 700 ACRES | GPS: 30.2767N, 91.1160W | IBERVILLE PARISH",
                      insert=(W / 2, 36), text_anchor="middle", fill="#3b82f6",
                      font_size=9, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("Sheet S-001 | MVP Design Intent | Scale: ~1\"=400' | 2026-03-22 | NOT FOR CONSTRUCTION",
                      insert=(W / 2, 48), text_anchor="middle", fill="#6b7280",
                      font_size=8, font_family="Arial"))

    # ════════════════════════════════════════════
    # MISSISSIPPI RIVER (LEFT EDGE)
    # ════════════════════════════════════════════
    river_pts = [(OX - 30, OY - 10), (OX - 10, OY + 50), (OX - 25, OY + 300),
                 (OX - 15, OY + 500), (OX - 30, OY + 700), (OX - 20, OY + 850),
                 (OX - 40, OY + 900)]
    # Fill river area
    river_fill = [(OX - 80, OY - 20)] + river_pts + [(OX - 80, OY + 910)]
    dwg.add(dwg.polygon(river_fill, fill="#0a1628", stroke="none"))
    dwg.add(dwg.polyline(river_pts, fill="none", stroke="#1e3a5f", stroke_width=2))

    # River label
    dwg.add(dwg.text("MISSISSIPPI RIVER", insert=(OX - 55, OY + 400),
                      fill="#1e3a5f", font_size=11, font_family="Arial", font_weight="bold",
                      transform=f"rotate(-90, {OX - 55}, {OY + 400})"))
    dwg.add(dwg.text("43 ft depth | 3,500 ft frontage", insert=(OX - 42, OY + 400),
                      fill="#1e3a5f", font_size=7, font_family="Arial",
                      transform=f"rotate(-90, {OX - 42}, {OY + 400})"))

    # ════════════════════════════════════════════
    # PROPERTY BOUNDARY
    # ════════════════════════════════════════════
    # Approximate 700-acre boundary (roughly 3500 x 4000 ft + tank farm area)
    prop_pts = [ft(0, 0), ft(4000, 0), ft(4000, 3200), ft(2500, 3500),
                ft(0, 3500)]
    dwg.add(dwg.polygon(prop_pts, fill="none", stroke="#3b82f6", stroke_width=1.5,
                         stroke_dasharray="8,4"))
    dwg.add(dwg.text("PROPERTY BOUNDARY — 700 ACRES", insert=ft(2000, -30),
                      text_anchor="middle", fill="#3b82f6", font_size=8, font_family="Arial"))

    # ════════════════════════════════════════════
    # DOCK (RIVER EDGE)
    # ════════════════════════════════════════════
    dock_y = 600
    # Pier extending into river
    px, py = ft(-100, dock_y)
    dwg.add(dwg.rect((px, py), (100 * S + 30, 15), fill="#2a2a2a", stroke="#6b7280", stroke_width=1))
    dwg.add(dwg.text("DEEPWATER DOCK", insert=(px + 10, py - 5), fill="#6b7280",
                      font_size=7, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("43 ft draft | Oceangoing vessels", insert=(px + 10, py + 25), fill="#555",
                      font_size=6, font_family="Arial"))

    # ════════════════════════════════════════════
    # WATER INTAKE STRUCTURE
    # ════════════════════════════════════════════
    intake_y = 400
    px, py = ft(-50, intake_y)
    dwg.add(dwg.rect((px, py), (80, 20), fill="#0a1628", stroke="#4fc3f7", stroke_width=1.5))
    dwg.add(dwg.text("WATER INTAKE", insert=(px + 5, py + 13), fill="#4fc3f7",
                      font_size=7, font_family="Arial", font_weight="bold"))

    # ════════════════════════════════════════════
    # TANK FARM (NORTH — EXISTING WGT)
    # ════════════════════════════════════════════
    tank_x, tank_y = 1500, 100
    ft_rect(dwg, tank_x, tank_y, 2000, 1200, fill="#111318", stroke="#6b7280", stroke_width=1,
            stroke_dasharray="6,3", rx=4)
    ft_text(dwg, tank_x + 1000, tank_y + 100, "TANK FARM — WGT OPERATIONS",
            text_anchor="middle", fill="#6b7280", font_size=9, font_family="Arial", font_weight="bold")
    ft_text(dwg, tank_x + 1000, tank_y + 200, "8 x 280,000 bbl = 2.33M bbl",
            text_anchor="middle", fill="#555", font_size=7, font_family="Arial")
    # Draw 8 tanks
    tank_positions = [(1600, 200), (1900, 200), (2200, 200), (2500, 200),
                      (1600, 600), (1900, 600), (2200, 600), (2500, 600)]
    for tx, ty in tank_positions:
        cx, cy = ft(tx, ty)
        dwg.add(dwg.circle((cx + 15, cy + 15), 15, fill="#1a1a1a", stroke="#555", stroke_width=0.5))

    # ════════════════════════════════════════════
    # EXISTING SUBSTATIONS
    # ════════════════════════════════════════════
    # 500kV substation
    sub500_x, sub500_y = 2800, 400
    ft_rect(dwg, sub500_x, sub500_y, 600, 400, fill="#1a0a1a", stroke="#ef4444", stroke_width=1.5, rx=3)
    ft_text(dwg, sub500_x + 300, sub500_y + 150, "500kV SUBSTATION",
            text_anchor="middle", fill="#ef4444", font_size=9, font_family="Arial", font_weight="bold")
    ft_text(dwg, sub500_x + 300, sub500_y + 250, "Entergy — LIVE",
            text_anchor="middle", fill="#ef4444", font_size=7, font_family="Arial")
    ft_text(dwg, sub500_x + 300, sub500_y + 330, "Willow Glen-Waterford Line",
            text_anchor="middle", fill="#888", font_size=6, font_family="Arial")

    # 230kV substation
    sub230_x, sub230_y = 2800, 900
    ft_rect(dwg, sub230_x, sub230_y, 600, 400, fill="#1a0a1a", stroke="#ef4444", stroke_width=1.5, rx=3)
    ft_text(dwg, sub230_x + 300, sub230_y + 150, "230kV SUBSTATION",
            text_anchor="middle", fill="#ef4444", font_size=9, font_family="Arial", font_weight="bold")
    ft_text(dwg, sub230_x + 300, sub230_y + 250, "Entergy — LIVE",
            text_anchor="middle", fill="#ef4444", font_size=7, font_family="Arial")
    ft_text(dwg, sub230_x + 300, sub230_y + 330, "Willow Glen-Conway Line (15 mi)",
            text_anchor="middle", fill="#888", font_size=6, font_family="Arial")

    # ════════════════════════════════════════════
    # SMOKESTACKS (EXISTING LANDMARKS)
    # ════════════════════════════════════════════
    stack_positions = [(1200, 1200), (1600, 1200)]
    for sx_ft, sy_ft in stack_positions:
        cx, cy = ft(sx_ft, sy_ft)
        dwg.add(dwg.circle((cx, cy), 6, fill="#333", stroke="#666", stroke_width=1))
        dwg.add(dwg.text("STACK", insert=(cx + 8, cy + 3), fill="#666", font_size=6, font_family="Arial"))

    # ════════════════════════════════════════════
    # NEW CONSTRUCTION — COMPUTE HALL
    # ════════════════════════════════════════════
    hall_x, hall_y = 400, 1500
    hall_w, hall_h = 800, 400  # 200 ft x 100 ft
    ft_rect(dwg, hall_x, hall_y, hall_w, hall_h, fill="#111a00", stroke="#76b900", stroke_width=2, rx=4)
    ft_text(dwg, hall_x + hall_w / 2, hall_y + 120, "COMPUTE HALL",
            text_anchor="middle", fill="#76b900", font_size=11, font_family="Arial", font_weight="bold")
    ft_text(dwg, hall_x + hall_w / 2, hall_y + 200, "36 NVL72 Racks | 4.68 MW",
            text_anchor="middle", fill="#76b900", font_size=8, font_family="Arial")
    ft_text(dwg, hall_x + hall_w / 2, hall_y + 280, "200' x 100' | 20,000 sq ft",
            text_anchor="middle", fill="#76b900", font_size=7, font_family="Arial")

    # ════════════════════════════════════════════
    # GENERATOR YARD
    # ════════════════════════════════════════════
    gen_x, gen_y = 1400, 1500
    gen_w, gen_h = 600, 400
    ft_rect(dwg, gen_x, gen_y, gen_w, gen_h, fill="#0a1a0a", stroke="#22c55e", stroke_width=1.5, rx=4)
    ft_text(dwg, gen_x + gen_w / 2, gen_y + 100, "GENERATOR YARD",
            text_anchor="middle", fill="#22c55e", font_size=9, font_family="Arial", font_weight="bold")
    ft_text(dwg, gen_x + gen_w / 2, gen_y + 180, "3x Caterpillar G3616A4 (8.7 MW ea)",
            text_anchor="middle", fill="#22c55e", font_size=7, font_family="Arial")
    ft_text(dwg, gen_x + gen_w / 2, gen_y + 250, "Natural Gas | H2-Ready",
            text_anchor="middle", fill="#22c55e", font_size=7, font_family="Arial")
    ft_text(dwg, gen_x + gen_w / 2, gen_y + 320, "150' x 100' | Fenced",
            text_anchor="middle", fill="#555", font_size=6, font_family="Arial")

    # ════════════════════════════════════════════
    # ELECTRICAL / POWER BUILDING
    # ════════════════════════════════════════════
    elec_x, elec_y = 400, 2000
    elec_w, elec_h = 600, 300
    ft_rect(dwg, elec_x, elec_y, elec_w, elec_h, fill="#0a0a1a", stroke="#8b5cf6", stroke_width=1.5, rx=4)
    ft_text(dwg, elec_x + elec_w / 2, elec_y + 100, "POWER BUILDING",
            text_anchor="middle", fill="#8b5cf6", font_size=9, font_family="Arial", font_weight="bold")
    ft_text(dwg, elec_x + elec_w / 2, elec_y + 170, "Eaton Beam Rubin DSX + ORV3 Sidecar",
            text_anchor="middle", fill="#c4b5fd", font_size=7, font_family="Arial")
    ft_text(dwg, elec_x + elec_w / 2, elec_y + 230, "ABB SACE Infinitus | Eaton xStorage BESS",
            text_anchor="middle", fill="#c4b5fd", font_size=7, font_family="Arial")

    # ════════════════════════════════════════════
    # SOLAR ARRAY ZONES
    # ════════════════════════════════════════════
    # Zone 1: South of compute area
    solar1_x, solar1_y = 200, 2500
    solar1_w, solar1_h = 2400, 800
    ft_rect(dwg, solar1_x, solar1_y, solar1_w, solar1_h, fill="#1a1a00", stroke="#fbbf24",
            stroke_width=1, stroke_dasharray="6,3", rx=4)
    ft_text(dwg, solar1_x + solar1_w / 2, solar1_y + 300, "SOLAR ARRAY ZONE A",
            text_anchor="middle", fill="#fbbf24", font_size=10, font_family="Arial", font_weight="bold")
    ft_text(dwg, solar1_x + solar1_w / 2, solar1_y + 420, "First Solar Series 7 TR1 (550W) | 5-panel strings @ 952V",
            text_anchor="middle", fill="#fbbf24", font_size=7, font_family="Arial")
    ft_text(dwg, solar1_x + solar1_w / 2, solar1_y + 520, "~3 MW | DC-Direct to 800V Bus",
            text_anchor="middle", fill="#fbbf24", font_size=7, font_family="Arial")
    # Draw panel rows
    for row in range(6):
        ry = solar1_y + 100 + row * 120
        px, py = ft(solar1_x + 100, ry)
        dwg.add(dwg.line((px, py), (px + solar1_w * S - 60, py), stroke="#fbbf24", stroke_width=0.5,
                          stroke_dasharray="2,4"))

    # Zone 2: East side
    solar2_x, solar2_y = 2200, 1600
    solar2_w, solar2_h = 1200, 800
    ft_rect(dwg, solar2_x, solar2_y, solar2_w, solar2_h, fill="#1a1a00", stroke="#fbbf24",
            stroke_width=1, stroke_dasharray="6,3", rx=4)
    ft_text(dwg, solar2_x + solar2_w / 2, solar2_y + 300, "SOLAR ARRAY\nZONE B",
            text_anchor="middle", fill="#fbbf24", font_size=9, font_family="Arial", font_weight="bold")
    ft_text(dwg, solar2_x + solar2_w / 2, solar2_y + 450, "~2 MW",
            text_anchor="middle", fill="#fbbf24", font_size=7, font_family="Arial")

    # ════════════════════════════════════════════
    # ROADS
    # ════════════════════════════════════════════
    # Main access road from LA-75
    road_pts = [ft(4000, 1800), ft(2200, 1800), ft(2000, 1700), ft(1200, 1500),
                ft(800, 1500), ft(400, 1500)]
    dwg.add(dwg.polyline(road_pts, fill="none", stroke="#444", stroke_width=3))
    ft_text(dwg, 3500, 1730, "ACCESS ROAD FROM LA-75", fill="#444", font_size=7, font_family="Arial")

    # Internal road loop
    loop_pts = [ft(400, 1450), ft(400, 2400), ft(1200, 2400), ft(2000, 2000),
                ft(2000, 1450), ft(400, 1450)]
    dwg.add(dwg.polyline(loop_pts, fill="none", stroke="#333", stroke_width=2))

    # ════════════════════════════════════════════
    # EXISTING WAREHOUSE
    # ════════════════════════════════════════════
    wh_x, wh_y = 1200, 2100
    ft_rect(dwg, wh_x, wh_y, 400, 200, fill="#111318", stroke="#6b7280", stroke_width=1, rx=3)
    ft_text(dwg, wh_x + 200, wh_y + 80, "EXISTING WAREHOUSE",
            text_anchor="middle", fill="#6b7280", font_size=7, font_family="Arial", font_weight="bold")
    ft_text(dwg, wh_x + 200, wh_y + 140, "20,000+ sq ft | Available",
            text_anchor="middle", fill="#555", font_size=6, font_family="Arial")

    # ════════════════════════════════════════════
    # CN RAILROAD
    # ════════════════════════════════════════════
    rail_pts = [ft(3800, 0), ft(3600, 1000), ft(3500, 2000), ft(3400, 3500)]
    dwg.add(dwg.polyline(rail_pts, fill="none", stroke="#8b4513", stroke_width=2,
                          stroke_dasharray="10,5"))
    ft_text(dwg, 3700, 500, "CN RAILROAD", fill="#8b4513", font_size=8, font_family="Arial",
            font_weight="bold", transform=f"rotate(-80, {ft(3700, 500)[0]}, {ft(3700, 500)[1]})")

    # ════════════════════════════════════════════
    # PIPELINE CORRIDOR
    # ════════════════════════════════════════════
    pipe_pts = [ft(100, 3400), ft(1500, 3300), ft(3000, 3400), ft(4000, 3300)]
    dwg.add(dwg.polyline(pipe_pts, fill="none", stroke="#ff6b35", stroke_width=1.5,
                          stroke_dasharray="6,3"))
    ft_text(dwg, 2000, 3350, "GAS PIPELINE CORRIDOR", text_anchor="middle",
            fill="#ff6b35", font_size=7, font_family="Arial", font_weight="bold")

    # ════════════════════════════════════════════
    # NORTH ARROW
    # ════════════════════════════════════════════
    na_x, na_y = W - 60, 100
    dwg.add(dwg.polygon([(na_x, na_y - 25), (na_x - 8, na_y), (na_x + 8, na_y)], fill="#fff"))
    dwg.add(dwg.text("N", insert=(na_x, na_y - 30), text_anchor="middle", fill="#fff",
                      font_size=12, font_family="Arial", font_weight="bold"))

    # ════════════════════════════════════════════
    # LEGEND
    # ════════════════════════════════════════════
    lx, ly = W - 300, 140
    dwg.add(dwg.rect((lx - 10, ly - 10), (290, 220), rx=6, fill="#111318", stroke="#1e2230"))
    dwg.add(dwg.text("LEGEND", insert=(lx, ly + 5), fill="#f0f2f5", font_size=9,
                      font_family="Arial", font_weight="bold"))

    legend = [
        ("#76b900", "New Compute Hall"),
        ("#22c55e", "Generator Yard"),
        ("#8b5cf6", "Power Building (800V DC)"),
        ("#fbbf24", "Solar Array Zones"),
        ("#ef4444", "Substations (500kV + 230kV)"),
        ("#6b7280", "Existing Structures (WGT)"),
        ("#4fc3f7", "Water Intake Structure"),
        ("#444444", "Access Roads"),
        ("#8b4513", "CN Railroad"),
        ("#ff6b35", "Gas Pipeline Corridor"),
        ("#3b82f6", "Property Boundary"),
        ("#1e3a5f", "Mississippi River"),
    ]
    for i, (color, text) in enumerate(legend):
        iy = ly + 20 + i * 16
        dwg.add(dwg.rect((lx, iy), (12, 8), fill=color, rx=2))
        dwg.add(dwg.text(text, insert=(lx + 18, iy + 7), fill="#9ca3af",
                          font_size=8, font_family="Arial"))

    # ════════════════════════════════════════════
    # SCALE BAR
    # ════════════════════════════════════════════
    sb_x, sb_y = OX, H - 30
    scales = [0, 500, 1000, 1500, 2000]
    for s_ft in scales:
        sx = sb_x + s_ft * S
        dwg.add(dwg.line((sx, sb_y), (sx, sb_y - 6), stroke="#888", stroke_width=1))
        dwg.add(dwg.text(f"{s_ft}'", insert=(sx, sb_y + 10), text_anchor="middle",
                          fill="#888", font_size=7, font_family="Arial"))
    dwg.add(dwg.line((sb_x, sb_y), (sb_x + 2000 * S, sb_y), stroke="#888", stroke_width=1))
    dwg.add(dwg.text("SCALE (FEET)", insert=(sb_x + 1000 * S, sb_y + 20), text_anchor="middle",
                      fill="#888", font_size=7, font_family="Arial"))

    dwg.save()
    print(f"Saved: {OUT}")


if __name__ == "__main__":
    import os
    os.makedirs("adc3k-deploy/willow-glen/blueprints", exist_ok=True)
    build()
