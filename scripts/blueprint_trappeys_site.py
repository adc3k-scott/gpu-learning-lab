"""
Trappeys Ragin' Cajun Compute Campus — Site Plan
22 acres, 4 buildings, water tower, concrete pad, bayou frontage
SVG output
"""
import svgwrite

W, H = 1400, 1000
OUT = "adc3k-deploy/trappeys/blueprints/site-plan.svg"

# Scale: 1 ft = 1.2 px (fits ~800 ft across ~960 px)
S = 1.2
OX, OY = 80, 120  # origin (top-left of property)


def ft(x, y):
    return (OX + x * S, OY + y * S)


def ft_rect(dwg, x, y, w, h, **kwargs):
    px, py = ft(x, y)
    dwg.add(dwg.rect((px, py), (w * S, h * S), **kwargs))


def ft_text(dwg, x, y, text, **kwargs):
    px, py = ft(x, y)
    dwg.add(dwg.text(text, insert=(px, py), **kwargs))


def dim_h(dwg, x, y, w, label, color="#555"):
    """Horizontal dimension line."""
    px1, py = ft(x, y)
    px2 = px1 + w * S
    py2 = py + 12
    dwg.add(dwg.line((px1, py2), (px2, py2), stroke=color, stroke_width=0.5))
    dwg.add(dwg.line((px1, py2 - 4), (px1, py2 + 4), stroke=color, stroke_width=0.5))
    dwg.add(dwg.line((px2, py2 - 4), (px2, py2 + 4), stroke=color, stroke_width=0.5))
    dwg.add(dwg.text(label, insert=((px1 + px2) / 2, py2 - 3), text_anchor="middle",
                      fill=color, font_size=7, font_family="Arial"))


def dim_v(dwg, x, y, h, label, color="#555"):
    """Vertical dimension line."""
    px, py1 = ft(x, y)
    py2 = py1 + h * S
    px2 = px + 15
    dwg.add(dwg.line((px2, py1), (px2, py2), stroke=color, stroke_width=0.5))
    dwg.add(dwg.line((px2 - 4, py1), (px2 + 4, py1), stroke=color, stroke_width=0.5))
    dwg.add(dwg.line((px2 - 4, py2), (px2 + 4, py2), stroke=color, stroke_width=0.5))
    dwg.add(dwg.text(label, insert=(px2 + 5, (py1 + py2) / 2 + 3), fill=color,
                      font_size=7, font_family="Arial"))


def build():
    dwg = svgwrite.Drawing(OUT, size=(f"{W}px", f"{H}px"), viewBox=f"0 0 {W} {H}")
    dwg.add(dwg.rect((0, 0), (W, H), fill="#0a0b0f"))

    # ── TITLE ──
    dwg.add(dwg.text("RAGIN' CAJUN COMPUTE CAMPUS — TRAPPEYS CANNERY, LAFAYETTE, LA",
                      insert=(W / 2, 22), text_anchor="middle", fill="#f0f2f5",
                      font_size=15, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("SITE PLAN | 22 ACRES | 112,500 SQ FT | 4 BUILDINGS | GPS: 30.2136N, 92.0016W",
                      insert=(W / 2, 36), text_anchor="middle", fill="#CE181E",
                      font_size=9, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("Sheet S-001 | MVP Design Intent | 2026-03-23 | NOT FOR CONSTRUCTION",
                      insert=(W / 2, 48), text_anchor="middle", fill="#6b7280",
                      font_size=8, font_family="Arial"))

    # ════════════════════════════════════════════
    # BAYOU VERMILION (TOP — RIVER SIDE)
    # ════════════════════════════════════════════
    bayou_y = -30
    bpx, bpy = ft(0, bayou_y)
    dwg.add(dwg.rect((bpx - 30, bpy), (W - 40, 35 * S),
                      fill="#0a1628", stroke="#1e3a5f", stroke_width=1.5, rx=4))
    ft_text(dwg, 150, bayou_y + 15, "BAYOU VERMILION", text_anchor="middle",
            fill="#1e3a5f", font_size=12, font_family="Arial", font_weight="bold")
    ft_text(dwg, 150, bayou_y + 25, "Brown bayou — calm, narrow. Seawall along property edge.",
            text_anchor="middle", fill="#1e3a5f", font_size=7, font_family="Arial")

    # Seawall line
    sx1, sy1 = ft(0, 0)
    sx2 = sx1 + 300 * S
    dwg.add(dwg.line((sx1, sy1 - 2), (sx2, sy1 - 2), stroke="#4fc3f7", stroke_width=2))
    ft_text(dwg, 310, -3, "SEAWALL", fill="#4fc3f7", font_size=7, font_family="Arial", font_weight="bold")

    # ════════════════════════════════════════════
    # BUILDING 1: FRONT (Bayou side)
    # 300 ft wide x 75 ft deep
    # ════════════════════════════════════════════
    b1_x, b1_y, b1_w, b1_h = 0, 5, 300, 75
    ft_rect(dwg, b1_x, b1_y, b1_w, b1_h, fill="#1a0a0a", stroke="#CE181E", stroke_width=2, rx=3)
    ft_text(dwg, b1_x + b1_w / 2, b1_y + 25, "FRONT BUILDING", text_anchor="middle",
            fill="#CE181E", font_size=11, font_family="Arial", font_weight="bold")
    ft_text(dwg, b1_x + b1_w / 2, b1_y + 38, "300' x 75' = 22,500 sq ft", text_anchor="middle",
            fill="#CE181E", font_size=8, font_family="Arial")
    ft_text(dwg, b1_x + b1_w / 2, b1_y + 50, "Museum | Education | Control Room | Meeting", text_anchor="middle",
            fill="#fca5a5", font_size=7, font_family="Arial")
    ft_text(dwg, b1_x + b1_w / 2, b1_y + 60, "Bayou view | Has vats | Phase 2", text_anchor="middle",
            fill="#888", font_size=6, font_family="Arial")
    dim_h(dwg, b1_x, b1_y + b1_h, b1_w, "300'-0\"", "#CE181E")
    dim_v(dwg, b1_x + b1_w, b1_y, b1_h, "75'-0\"", "#CE181E")

    # ════════════════════════════════════════════
    # BUILDING 2: MIDDLE LOW
    # 300 ft wide x 100 ft deep
    # ════════════════════════════════════════════
    gap = 15  # space between buildings
    b2_x, b2_y, b2_w, b2_h = 0, b1_y + b1_h + gap, 300, 100
    ft_rect(dwg, b2_x, b2_y, b2_w, b2_h, fill="#1a1a0a", stroke="#fbbf24", stroke_width=2, rx=3)
    ft_text(dwg, b2_x + b2_w / 2, b2_y + 30, "MIDDLE LOW", text_anchor="middle",
            fill="#fbbf24", font_size=11, font_family="Arial", font_weight="bold")
    ft_text(dwg, b2_x + b2_w / 2, b2_y + 43, "300' x 100' = 30,000 sq ft", text_anchor="middle",
            fill="#fbbf24", font_size=8, font_family="Arial")
    ft_text(dwg, b2_x + b2_w / 2, b2_y + 58, "Phase 2 Remodel", text_anchor="middle",
            fill="#888", font_size=7, font_family="Arial")
    dim_h(dwg, b2_x, b2_y + b2_h, b2_w, "300'-0\"", "#fbbf24")
    dim_v(dwg, b2_x + b2_w, b2_y, b2_h, "100'-0\"", "#fbbf24")

    # ════════════════════════════════════════════
    # BUILDING 3: MIDDLE HIGH (DEPLOY FIRST)
    # 300 ft wide x 75 ft deep — wooden trusses
    # ════════════════════════════════════════════
    b3_x, b3_y, b3_w, b3_h = 0, b2_y + b2_h + gap, 300, 75
    ft_rect(dwg, b3_x, b3_y, b3_w, b3_h, fill="#0a1a0a", stroke="#76b900", stroke_width=2.5, rx=3)
    ft_text(dwg, b3_x + b3_w / 2, b3_y + 20, "MIDDLE HIGH", text_anchor="middle",
            fill="#76b900", font_size=12, font_family="Arial", font_weight="bold")
    ft_text(dwg, b3_x + b3_w / 2, b3_y + 33, "300' x 75' = 22,500 sq ft", text_anchor="middle",
            fill="#76b900", font_size=8, font_family="Arial")
    ft_text(dwg, b3_x + b3_w / 2, b3_y + 46, "DEPLOY HERE FIRST — GPU Compute Hall", text_anchor="middle",
            fill="#76b900", font_size=8, font_family="Arial", font_weight="bold")
    ft_text(dwg, b3_x + b3_w / 2, b3_y + 58, "Wooden trusses | NVL72 racks | 800V DC | Cooling", text_anchor="middle",
            fill="#86efac", font_size=7, font_family="Arial")
    dim_h(dwg, b3_x, b3_y + b3_h, b3_w, "300'-0\"", "#76b900")
    dim_v(dwg, b3_x + b3_w, b3_y, b3_h, "75'-0\"", "#76b900")

    # Deploy arrow
    arrow_x = b3_x + b3_w + 25
    arrow_y = b3_y + b3_h / 2
    px, py = ft(arrow_x, arrow_y)
    dwg.add(dwg.text("PHASE 1", insert=(px, py - 5), fill="#76b900",
                      font_size=10, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("DEPLOY", insert=(px, py + 7), fill="#76b900",
                      font_size=10, font_family="Arial", font_weight="bold"))

    # ════════════════════════════════════════════
    # BUILDING 4: REAR HIGH (STAGING)
    # 250 ft wide x 150 ft deep — lines up on left
    # ════════════════════════════════════════════
    b4_x, b4_y, b4_w, b4_h = 0, b3_y + b3_h + gap, 250, 150
    ft_rect(dwg, b4_x, b4_y, b4_w, b4_h, fill="#0a0a1a", stroke="#3b82f6", stroke_width=2, rx=3)
    ft_text(dwg, b4_x + b4_w / 2, b4_y + 40, "REAR HIGH", text_anchor="middle",
            fill="#3b82f6", font_size=12, font_family="Arial", font_weight="bold")
    ft_text(dwg, b4_x + b4_w / 2, b4_y + 53, "250' x 150' = 37,500 sq ft", text_anchor="middle",
            fill="#3b82f6", font_size=8, font_family="Arial")
    ft_text(dwg, b4_x + b4_w / 2, b4_y + 68, "STAGING AREA — Big, Open, Locked, Weather-Protected", text_anchor="middle",
            fill="#93c5fd", font_size=7, font_family="Arial", font_weight="bold")
    ft_text(dwg, b4_x + b4_w / 2, b4_y + 80, "Equipment storage | Material staging | Phase 1 prep", text_anchor="middle",
            fill="#888", font_size=7, font_family="Arial")
    dim_h(dwg, b4_x, b4_y + b4_h, b4_w, "250'-0\"", "#3b82f6")
    dim_v(dwg, b4_x + b4_w, b4_y, b4_h, "150'-0\"", "#3b82f6")

    # Show the 50 ft offset on right side
    offset_x = b4_x + b4_w
    ft_text(dwg, offset_x + 5, b4_y + 10, "50' narrower", fill="#555", font_size=6, font_family="Arial")
    px1, py1 = ft(offset_x, b4_y)
    px2, py2 = ft(300, b4_y)
    dwg.add(dwg.line((px1, py1), (px2, py1), stroke="#333", stroke_width=0.5, stroke_dasharray="4,4"))

    # ════════════════════════════════════════════
    # WATER TOWER (behind rear high, to the right)
    # ════════════════════════════════════════════
    wt_x, wt_y = 280, b4_y + 50
    px, py = ft(wt_x, wt_y)
    dwg.add(dwg.circle((px, py), 15, fill="#1a1a2e", stroke="#4fc3f7", stroke_width=1.5))
    dwg.add(dwg.text("WT", insert=(px, py + 4), text_anchor="middle",
                      fill="#4fc3f7", font_size=9, font_family="Arial", font_weight="bold"))
    ft_text(dwg, wt_x - 5, wt_y + 20, "WATER TOWER", fill="#4fc3f7", font_size=7,
            font_family="Arial", font_weight="bold")
    ft_text(dwg, wt_x - 5, wt_y + 28, "100 ft tall | Thermal cooling", fill="#4fc3f7", font_size=6,
            font_family="Arial")

    # ════════════════════════════════════════════
    # STRUCTURE BEHIND REAR HIGH (not ready)
    # ════════════════════════════════════════════
    b5_x, b5_y = 0, b4_y + b4_h + gap
    ft_rect(dwg, b5_x, b5_y, 200, 60, fill="#0a0a0a", stroke="#333", stroke_width=1,
            stroke_dasharray="6,3", rx=3)
    ft_text(dwg, b5_x + 100, b5_y + 22, "FUTURE BUILDING", text_anchor="middle",
            fill="#555", font_size=9, font_family="Arial", font_weight="bold")
    ft_text(dwg, b5_x + 100, b5_y + 34, "Brick standing, metal gone, rebuildable", text_anchor="middle",
            fill="#444", font_size=7, font_family="Arial")
    ft_text(dwg, b5_x + 100, b5_y + 44, "NOT READY — Phase 3+", text_anchor="middle",
            fill="#444", font_size=6, font_family="Arial")

    # ════════════════════════════════════════════
    # CONCRETE PAD (Infrastructure Yard)
    # ════════════════════════════════════════════
    pad_x, pad_y = 320, b2_y
    pad_w, pad_h = 120, 200
    ft_rect(dwg, pad_x, pad_y, pad_w, pad_h, fill="#111318", stroke="#6b7280", stroke_width=1.5, rx=3)
    ft_text(dwg, pad_x + pad_w / 2, pad_y + 50, "CONCRETE PAD", text_anchor="middle",
            fill="#6b7280", font_size=9, font_family="Arial", font_weight="bold")
    ft_text(dwg, pad_x + pad_w / 2, pad_y + 65, "Infrastructure Yard", text_anchor="middle",
            fill="#9ca3af", font_size=7, font_family="Arial")
    ft_text(dwg, pad_x + pad_w / 2, pad_y + 80, "Caterpillar G3516J (1.6 MW) x3 N+1", text_anchor="middle",
            fill="#22c55e", font_size=7, font_family="Arial")
    ft_text(dwg, pad_x + pad_w / 2, pad_y + 92, "Eaton Beam Rubin DSX + ORV3 Sidecar", text_anchor="middle",
            fill="#8b5cf6", font_size=7, font_family="Arial")
    ft_text(dwg, pad_x + pad_w / 2, pad_y + 104, "ABB SACE Infinitus DC Protection", text_anchor="middle",
            fill="#8b5cf6", font_size=7, font_family="Arial")
    ft_text(dwg, pad_x + pad_w / 2, pad_y + 116, "Eaton xStorage BESS", text_anchor="middle",
            fill="#3b82f6", font_size=7, font_family="Arial")
    ft_text(dwg, pad_x + pad_w / 2, pad_y + 130, "NOT solar — equipment only", text_anchor="middle",
            fill="#555", font_size=6, font_family="Arial")

    # ════════════════════════════════════════════
    # SOLAR (Rooftop only — all 4 buildings)
    # ════════════════════════════════════════════
    # Solar indicators on each building roof
    for bx, by, bw, bh in [(b1_x, b1_y, b1_w, b1_h), (b2_x, b2_y, b2_w, b2_h),
                             (b3_x, b3_y, b3_w, b3_h), (b4_x, b4_y, b4_w, b4_h)]:
        px, py = ft(bx + 5, by + 5)
        dwg.add(dwg.text("SOLAR", insert=(px, py + 8), fill="#fbbf24", font_size=6,
                          font_family="Arial", font_weight="bold", opacity=0.6))

    # ════════════════════════════════════════════
    # ACCESS / ROADS
    # ════════════════════════════════════════════
    # SE Evangeline Thruway (right side)
    road_x = 470
    ft_rect(dwg, road_x, -30, 30, 600, fill="#1a1a1a", stroke="#333", stroke_width=1, rx=2)
    ft_text(dwg, road_x + 15, 200, "SE EVANGELINE THRUWAY", text_anchor="middle",
            fill="#444", font_size=8, font_family="Arial", font_weight="bold",
            transform=f"rotate(90, {ft(road_x + 15, 200)[0]}, {ft(road_x + 15, 200)[1]})")

    # UL Lafayette indicator
    ft_text(dwg, road_x + 50, 100, "UL LAFAYETTE", fill="#CE181E", font_size=10,
            font_family="Arial", font_weight="bold")
    ft_text(dwg, road_x + 50, 112, "0.5 miles east", fill="#888", font_size=7,
            font_family="Arial")

    # LUS Substation indicator
    ft_text(dwg, road_x + 50, 160, "LUS PIN HOOK", fill="#ef4444", font_size=8,
            font_family="Arial", font_weight="bold")
    ft_text(dwg, road_x + 50, 172, "SUBSTATION", fill="#ef4444", font_size=8,
            font_family="Arial", font_weight="bold")
    ft_text(dwg, road_x + 50, 182, "Next door (Curtis Rodemacher)", fill="#888", font_size=6,
            font_family="Arial")

    # ATMOS gas line
    ft_text(dwg, road_x + 50, 220, "ATMOS GAS", fill="#22c55e", font_size=8,
            font_family="Arial", font_weight="bold")
    ft_text(dwg, road_x + 50, 230, "Trunk line on property", fill="#888", font_size=6,
            font_family="Arial")

    # LUS Fiber
    ft_text(dwg, road_x + 50, 260, "LUS FIBER", fill="#3b82f6", font_size=8,
            font_family="Arial", font_weight="bold")
    ft_text(dwg, road_x + 50, 270, "0.8 mi municipal fiber", fill="#888", font_size=6,
            font_family="Arial")

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
    lx, ly = W - 320, 160
    dwg.add(dwg.rect((lx - 10, ly - 10), (310, 200), rx=6, fill="#111318", stroke="#1e2230"))
    dwg.add(dwg.text("LEGEND", insert=(lx, ly + 5), fill="#f0f2f5", font_size=9,
                      font_family="Arial", font_weight="bold"))

    legend = [
        ("#CE181E", "Front Building (museum, education, control)"),
        ("#fbbf24", "Middle Low (Phase 2 remodel)"),
        ("#76b900", "Middle High (PHASE 1 DEPLOY — compute)"),
        ("#3b82f6", "Rear High (staging area)"),
        ("#333333", "Future Building (not ready)"),
        ("#4fc3f7", "Water Tower (thermal cooling)"),
        ("#6b7280", "Concrete Pad (infrastructure yard)"),
        ("#fbbf24", "Solar (rooftop — all 4 buildings)"),
        ("#22c55e", "Gas (ATMOS trunk line)"),
        ("#ef4444", "Grid (LUS — sell-back only)"),
        ("#1e3a5f", "Bayou Vermilion"),
    ]
    for i, (color, text) in enumerate(legend):
        iy = ly + 20 + i * 16
        dwg.add(dwg.rect((lx, iy), (12, 8), fill=color, rx=2))
        dwg.add(dwg.text(text, insert=(lx + 18, iy + 7), fill="#9ca3af",
                          font_size=7, font_family="Arial"))

    # ════════════════════════════════════════════
    # DEPLOY SEQUENCE
    # ════════════════════════════════════════════
    sy = 780
    dwg.add(dwg.rect((OX - 10, sy), (900, 70), rx=6, fill="#111318", stroke="#1e2230"))
    dwg.add(dwg.text("DEPLOY SEQUENCE", insert=(OX, sy + 18), fill="#f0f2f5",
                      font_size=10, font_family="Arial", font_weight="bold"))

    steps = [
        ("1", "#3b82f6", "STAGE", "Rear High (37,500 sf)", "Equipment, materials, prep"),
        ("2", "#76b900", "DEPLOY", "Middle High (22,500 sf)", "GPU racks, 800V DC, cooling"),
        ("3", "#CE181E", "REMODEL", "Front (22,500 sf)", "Museum, education, control room"),
        ("4", "#fbbf24", "EXPAND", "Middle Low (30,000 sf)", "Additional compute + offices"),
    ]
    sx = OX + 10
    for num, color, phase, bldg, desc in steps:
        dwg.add(dwg.text(num, insert=(sx, sy + 40), fill=color, font_size=18,
                          font_family="Arial", font_weight="bold"))
        dwg.add(dwg.text(phase, insert=(sx + 18, sy + 38), fill=color, font_size=9,
                          font_family="Arial", font_weight="bold"))
        dwg.add(dwg.text(bldg, insert=(sx + 18, sy + 50), fill="#9ca3af", font_size=7,
                          font_family="Arial"))
        dwg.add(dwg.text(desc, insert=(sx + 18, sy + 60), fill="#6b7280", font_size=6,
                          font_family="Arial"))
        sx += 220

    # ════════════════════════════════════════════
    # BUILDING SUMMARY
    # ════════════════════════════════════════════
    by2 = 870
    dwg.add(dwg.rect((OX - 10, by2), (900, 55), rx=6, fill="#111318", stroke="#1e2230"))
    stats = [
        ("FRONT", "22,500 sf"),
        ("MIDDLE LOW", "30,000 sf"),
        ("MIDDLE HIGH", "22,500 sf"),
        ("REAR HIGH", "37,500 sf"),
        ("TOTAL", "112,500 sf"),
        ("SOLAR", "2.05 MW rooftop"),
        ("GENSETS", "3x Cat G3516J (4.8 MW N+1)"),
    ]
    sx2 = OX
    for label, value in stats:
        dwg.add(dwg.text(label, insert=(sx2, by2 + 18), fill="#6b7280",
                          font_size=7, font_family="Arial", font_weight="bold"))
        dwg.add(dwg.text(value, insert=(sx2, by2 + 32), fill="#CE181E",
                          font_size=10, font_family="Arial", font_weight="bold"))
        sx2 += 128

    # ════════════════════════════════════════════
    # SCALE BAR
    # ════════════════════════════════════════════
    sb_x, sb_y = OX, H - 30
    scales = [0, 50, 100, 150, 200, 250, 300]
    for s_ft in scales:
        sx3 = sb_x + s_ft * S
        dwg.add(dwg.line((sx3, sb_y), (sx3, sb_y - 6), stroke="#888", stroke_width=1))
        dwg.add(dwg.text(f"{s_ft}'", insert=(sx3, sb_y + 10), text_anchor="middle",
                          fill="#888", font_size=7, font_family="Arial"))
    dwg.add(dwg.line((sb_x, sb_y), (sb_x + 300 * S, sb_y), stroke="#888", stroke_width=1))

    # NOTES
    ny = 940
    notes = [
        "1. All 4 buildings line up on the left (river/bayou side). Rear High is 50 ft narrower on the right.",
        "2. Concrete pad is the infrastructure yard — generators, switchgear, battery. NOT solar.",
        "3. Solar is ROOFTOP ONLY on all 4 buildings. 3,731 First Solar Series 7 TR1 panels = 2.05 MW.",
        "4. Water tower = thermal cooling mass. 100 ft tall. Supplement to BAC TrilliumSeries adiabatic coolers for GPU cooling.",
        "5. LUS Pin Hook substation is next door. Grid = sell-back only. ATMOS gas trunk line on property.",
    ]
    for i, note in enumerate(notes):
        dwg.add(dwg.text(note, insert=(35, ny + i * 11), fill="#4b5563",
                          font_size=7, font_family="Arial"))

    dwg.save()
    print(f"Saved: {OUT}")


if __name__ == "__main__":
    import os
    os.makedirs("adc3k-deploy/trappeys/blueprints", exist_ok=True)
    build()
