"""
MARLIE I — Lafayette AI Factory & Command Center
Site Plan: 24x40 building on 0.60 acres, 3 parcels, Chag Street
GPS: 30.21975N, 92.00645W
"""
import svgwrite

W, H = 1400, 1000
OUT = "adc3k-deploy/marlie/blueprints/site-plan.svg"

ACCENT = "#3b82f6"  # Blue accent for MARLIE I

# Scale: 1 ft = 4 px (fits small building well)
S = 4
OX, OY = 200, 200  # origin


def ft(x, y):
    return (OX + x * S, OY + y * S)


def ft_rect(dwg, x, y, w, h, **kwargs):
    px, py = ft(x, y)
    dwg.add(dwg.rect((px, py), (w * S, h * S), **kwargs))


def ft_text(dwg, x, y, text, **kwargs):
    px, py = ft(x, y)
    dwg.add(dwg.text(text, insert=(px, py), **kwargs))


def dim_h(dwg, x, y, w, label, color="#555"):
    px1, py = ft(x, y)
    px2 = px1 + w * S
    py2 = py + 12
    dwg.add(dwg.line((px1, py2), (px2, py2), stroke=color, stroke_width=0.5))
    dwg.add(dwg.line((px1, py2 - 4), (px1, py2 + 4), stroke=color, stroke_width=0.5))
    dwg.add(dwg.line((px2, py2 - 4), (px2, py2 + 4), stroke=color, stroke_width=0.5))
    dwg.add(dwg.text(label, insert=((px1 + px2) / 2, py2 - 3), text_anchor="middle",
                      fill=color, font_size=7, font_family="Arial"))


def dim_v(dwg, x, y, h, label, color="#555"):
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

    # -- TITLE BLOCK --
    dwg.add(dwg.text("MARLIE I — LAFAYETTE AI FACTORY & COMMAND CENTER",
                      insert=(W / 2, 22), text_anchor="middle", fill="#f0f2f5",
                      font_size=15, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("SITE PLAN | 1201 SE EVANGELINE THRUWAY | 0.60 ACRES | 3 PARCELS | GPS: 30.2198N, 92.0065W",
                      insert=(W / 2, 36), text_anchor="middle", fill=ACCENT,
                      font_size=9, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("Sheet S-001 | MVP Design Intent | 2026-03-23 | NOT FOR CONSTRUCTION",
                      insert=(W / 2, 48), text_anchor="middle", fill="#6b7280",
                      font_size=8, font_family="Arial"))

    # ================================================================
    # PROPERTY BOUNDARY — 3 PARCELS on 0.60 acres
    # Approximate: 130 ft wide x 200 ft deep = ~0.60 acres
    # ================================================================
    prop_w, prop_h = 130, 200
    ft_rect(dwg, -10, -10, prop_w + 20, prop_h + 20,
            fill="none", stroke="#333", stroke_width=1, stroke_dasharray="8,4", rx=0)
    ft_text(dwg, prop_w / 2, -15, "PROPERTY LINE — 3 PARCELS, 0.60 ACRES",
            text_anchor="middle", fill="#555", font_size=8, font_family="Arial")

    # Parcel dividers (dashed)
    for py_ft in [65, 130]:
        px1, py1 = ft(-10, py_ft)
        px2, py2 = ft(prop_w + 10, py_ft)
        dwg.add(dwg.line((px1, py1), (px2, py1), stroke="#333", stroke_width=0.5,
                          stroke_dasharray="4,4"))

    ft_text(dwg, -18, 30, "PARCEL 1", fill="#555", font_size=7, font_family="Arial",
            transform=f"rotate(-90, {ft(-18, 30)[0]}, {ft(-18, 30)[1]})")
    ft_text(dwg, -18, 95, "PARCEL 2", fill="#555", font_size=7, font_family="Arial",
            transform=f"rotate(-90, {ft(-18, 95)[0]}, {ft(-18, 95)[1]})")
    ft_text(dwg, -18, 160, "PARCEL 3", fill="#555", font_size=7, font_family="Arial",
            transform=f"rotate(-90, {ft(-18, 160)[0]}, {ft(-18, 160)[1]})")

    # ================================================================
    # MAIN BUILDING — 24 x 40, 2 floors
    # ================================================================
    bldg_x, bldg_y, bldg_w, bldg_h = 30, 20, 24, 40
    ft_rect(dwg, bldg_x, bldg_y, bldg_w, bldg_h,
            fill="#0a1028", stroke=ACCENT, stroke_width=2.5, rx=3)
    ft_text(dwg, bldg_x + bldg_w / 2, bldg_y + 10, "MARLIE I",
            text_anchor="middle", fill=ACCENT, font_size=12, font_family="Arial", font_weight="bold")
    ft_text(dwg, bldg_x + bldg_w / 2, bldg_y + 15, "24' x 40' = 1,920 sq ft",
            text_anchor="middle", fill=ACCENT, font_size=8, font_family="Arial")
    ft_text(dwg, bldg_x + bldg_w / 2, bldg_y + 20, "2 FLOORS | 8 NVL72 RACKS",
            text_anchor="middle", fill="#93c5fd", font_size=7, font_family="Arial", font_weight="bold")
    ft_text(dwg, bldg_x + bldg_w / 2, bldg_y + 25, "576 GPUs | 1,040 kW IT",
            text_anchor="middle", fill="#93c5fd", font_size=7, font_family="Arial")
    ft_text(dwg, bldg_x + bldg_w / 2, bldg_y + 30, "Backup NOC + Edge Compute",
            text_anchor="middle", fill="#6b7280", font_size=7, font_family="Arial")
    ft_text(dwg, bldg_x + bldg_w / 2, bldg_y + 35, "Scott's Operations HQ",
            text_anchor="middle", fill="#6b7280", font_size=6, font_family="Arial")

    dim_h(dwg, bldg_x, bldg_y + bldg_h, bldg_w, "24'-0\"", ACCENT)
    dim_v(dwg, bldg_x + bldg_w, bldg_y, bldg_h, "40'-0\"", ACCENT)

    # Staircase indicator on left side
    stair_w, stair_h = 3, 10
    ft_rect(dwg, bldg_x, bldg_y + 15, stair_w, stair_h,
            fill="#1a1a2e", stroke="#8b5cf6", stroke_width=1, rx=1)
    ft_text(dwg, bldg_x + 1.5, bldg_y + 21, "STAIR",
            text_anchor="middle", fill="#8b5cf6", font_size=5, font_family="Arial")

    # Solar roof indicator
    ft_text(dwg, bldg_x + bldg_w - 2, bldg_y + 2, "SOLAR",
            fill="#fbbf24", font_size=5, font_family="Arial", font_weight="bold", opacity=0.7)

    # ================================================================
    # CONCRETE PAD — Generators + Dry Coolers
    # ================================================================
    pad_x, pad_y = 70, 20
    pad_w, pad_h = 50, 60
    ft_rect(dwg, pad_x, pad_y, pad_w, pad_h,
            fill="#111318", stroke="#6b7280", stroke_width=1.5, rx=3)
    ft_text(dwg, pad_x + pad_w / 2, pad_y + 8, "CONCRETE PAD",
            text_anchor="middle", fill="#6b7280", font_size=9, font_family="Arial", font_weight="bold")
    ft_text(dwg, pad_x + pad_w / 2, pad_y + 14, "Infrastructure Yard",
            text_anchor="middle", fill="#9ca3af", font_size=7, font_family="Arial")

    # Generator boxes
    gen_y = pad_y + 18
    ft_rect(dwg, pad_x + 3, gen_y, 20, 10,
            fill="#0a1a0a", stroke="#22c55e", stroke_width=1, rx=2)
    ft_text(dwg, pad_x + 13, gen_y + 6, "Cat G3512H #1",
            text_anchor="middle", fill="#22c55e", font_size=6, font_family="Arial", font_weight="bold")
    ft_text(dwg, pad_x + 13, gen_y + 9, "1.03 MW",
            text_anchor="middle", fill="#22c55e", font_size=5, font_family="Arial")

    ft_rect(dwg, pad_x + 27, gen_y, 20, 10,
            fill="#0a1a0a", stroke="#22c55e", stroke_width=1, rx=2)
    ft_text(dwg, pad_x + 37, gen_y + 6, "Cat G3512H #2",
            text_anchor="middle", fill="#22c55e", font_size=6, font_family="Arial", font_weight="bold")
    ft_text(dwg, pad_x + 37, gen_y + 9, "N+1",
            text_anchor="middle", fill="#4ade80", font_size=5, font_family="Arial")

    # Dry coolers
    dc_y = gen_y + 14
    ft_rect(dwg, pad_x + 3, dc_y, 44, 12,
            fill="#0a1628", stroke="#4fc3f7", stroke_width=1, rx=2)
    ft_text(dwg, pad_x + 25, dc_y + 5, "BAC TrilliumSeries",
            text_anchor="middle", fill="#4fc3f7", font_size=7, font_family="Arial", font_weight="bold")
    ft_text(dwg, pad_x + 25, dc_y + 9, "Adiabatic Cooler | Heat Rejection",
            text_anchor="middle", fill="#4fc3f7", font_size=5, font_family="Arial")

    # Eaton switchgear
    sw_y = dc_y + 15
    ft_rect(dwg, pad_x + 3, sw_y, 44, 8,
            fill="#111318", stroke="#8b5cf6", stroke_width=1, rx=2)
    ft_text(dwg, pad_x + 25, sw_y + 5, "EATON BEAM RUBIN DSX | ORV3 SIDECAR",
            text_anchor="middle", fill="#c4b5fd", font_size=5, font_family="Arial", font_weight="bold")

    # Diesel genset
    diesel_y = sw_y + 10
    ft_rect(dwg, pad_x + 3, diesel_y, 20, 8,
            fill="#2e1a1a", stroke="#ef4444", stroke_width=1, rx=2)
    ft_text(dwg, pad_x + 13, diesel_y + 5, "DIESEL GENSET",
            text_anchor="middle", fill="#ef4444", font_size=5, font_family="Arial", font_weight="bold")

    # Battery
    ft_rect(dwg, pad_x + 27, diesel_y, 20, 8,
            fill="#0a0a1a", stroke=ACCENT, stroke_width=1, rx=2)
    ft_text(dwg, pad_x + 37, diesel_y + 5, "Eaton xStorage 600kWh",
            text_anchor="middle", fill="#93c5fd", font_size=5, font_family="Arial", font_weight="bold")

    dim_h(dwg, pad_x, pad_y + pad_h, pad_w, "~50'-0\"", "#6b7280")

    # ================================================================
    # BLIGHTED STRUCTURES — Phase 1 Demolition
    # ================================================================
    blight_positions = [(10, 80, 25, 20), (40, 110, 30, 25), (80, 110, 35, 20)]
    for i, (bx, by, bw, bh) in enumerate(blight_positions):
        ft_rect(dwg, bx, by, bw, bh,
                fill="#0a0a0a", stroke="#555", stroke_width=1, stroke_dasharray="4,3", rx=2)
        ft_text(dwg, bx + bw / 2, by + bh / 2 - 2, f"BLIGHTED #{i + 1}",
                text_anchor="middle", fill="#555", font_size=7, font_family="Arial", font_weight="bold")
        ft_text(dwg, bx + bw / 2, by + bh / 2 + 6, "PHASE 1 DEMO",
                text_anchor="middle", fill="#ef4444", font_size=5, font_family="Arial")

    # ================================================================
    # CHAG STREET (bottom/south)
    # ================================================================
    ft_rect(dwg, -20, prop_h + 15, prop_w + 40, 12,
            fill="#1a1a1a", stroke="#333", stroke_width=1, rx=2)
    ft_text(dwg, prop_w / 2, prop_h + 23, "CHAG STREET",
            text_anchor="middle", fill="#444", font_size=9, font_family="Arial", font_weight="bold")

    # ================================================================
    # SE EVANGELINE THRUWAY (right/east)
    # ================================================================
    road_x = prop_w + 25
    ft_rect(dwg, road_x, -20, 12, prop_h + 50,
            fill="#1a1a1a", stroke="#333", stroke_width=1, rx=2)
    rx, ry = ft(road_x + 6, prop_h / 2)
    dwg.add(dwg.text("SE EVANGELINE THRUWAY", insert=(rx, ry),
                      text_anchor="middle", fill="#444", font_size=9, font_family="Arial", font_weight="bold",
                      transform=f"rotate(90, {rx}, {ry})"))

    # ================================================================
    # PROXIMITY MARKERS
    # ================================================================
    marker_x = road_x + 20

    # Trappeys
    ft_text(dwg, marker_x, 20, "TRAPPEYS CANNERY", fill="#CE181E", font_size=10,
            font_family="Arial", font_weight="bold")
    ft_text(dwg, marker_x, 28, "0.5 miles south", fill="#888", font_size=7,
            font_family="Arial")
    ft_text(dwg, marker_x, 34, "Solar AI factory | 112,500 sq ft", fill="#888", font_size=6,
            font_family="Arial")

    # UL Lafayette
    ft_text(dwg, marker_x, 50, "UL LAFAYETTE", fill="#CE181E", font_size=10,
            font_family="Arial", font_weight="bold")
    ft_text(dwg, marker_x, 58, "0.5 miles east", fill="#888", font_size=7,
            font_family="Arial")
    ft_text(dwg, marker_x, 64, "Anchor tenant | Grants | Workforce", fill="#888", font_size=6,
            font_family="Arial")

    # Willow Glen
    ft_text(dwg, marker_x, 80, "WILLOW GLEN", fill="#76b900", font_size=10,
            font_family="Arial", font_weight="bold")
    ft_text(dwg, marker_x, 88, "60 miles east (fiber)", fill="#888", font_size=7,
            font_family="Arial")
    ft_text(dwg, marker_x, 94, "PRIMARY HUB | Management traffic only", fill="#888", font_size=6,
            font_family="Arial")

    # LUS Fiber
    ft_text(dwg, marker_x, 112, "LUS FIBER", fill=ACCENT, font_size=9,
            font_family="Arial", font_weight="bold")
    ft_text(dwg, marker_x, 120, "0.8 mi municipal fiber conduit", fill="#888", font_size=7,
            font_family="Arial")

    # Natural Gas
    ft_text(dwg, marker_x, 135, "ATMOS GAS", fill="#22c55e", font_size=9,
            font_family="Arial", font_weight="bold")
    ft_text(dwg, marker_x, 143, "Natural gas on property", fill="#888", font_size=7,
            font_family="Arial")
    ft_text(dwg, marker_x, 149, "Henry Hub 40 mi", fill="#888", font_size=6,
            font_family="Arial")

    # LUS/SLEMCO
    ft_text(dwg, marker_x, 165, "LUS + SLEMCO", fill="#ef4444", font_size=9,
            font_family="Arial", font_weight="bold")
    ft_text(dwg, marker_x, 173, "Dual feed available | 3-phase confirmed", fill="#888", font_size=7,
            font_family="Arial")
    ft_text(dwg, marker_x, 179, "Backup only — NOT primary", fill="#ef4444", font_size=6,
            font_family="Arial")

    # ================================================================
    # NORTH ARROW
    # ================================================================
    na_x, na_y = W - 60, 100
    dwg.add(dwg.polygon([(na_x, na_y - 25), (na_x - 8, na_y), (na_x + 8, na_y)], fill="#fff"))
    dwg.add(dwg.text("N", insert=(na_x, na_y - 30), text_anchor="middle", fill="#fff",
                      font_size=12, font_family="Arial", font_weight="bold"))

    # ================================================================
    # LEGEND
    # ================================================================
    lx, ly = W - 380, 160
    dwg.add(dwg.rect((lx - 10, ly - 10), (370, 180), rx=6, fill="#111318", stroke="#1e2230"))
    dwg.add(dwg.text("LEGEND", insert=(lx, ly + 5), fill="#f0f2f5", font_size=9,
                      font_family="Arial", font_weight="bold"))

    legend = [
        (ACCENT, "MARLIE I — 24x40 building, 2 floors, 1,920 sq ft"),
        ("#6b7280", "Concrete Pad (generators, adiabatic coolers, switchgear)"),
        ("#22c55e", "Caterpillar G3512H (1.03 MW) x2 N+1"),
        ("#4fc3f7", "BAC TrilliumSeries Adiabatic Cooler"),
        ("#8b5cf6", "Eaton Beam Rubin DSX + ORV3 Sidecar"),
        ("#ef4444", "Diesel Emergency + LUS Backup"),
        ("#fbbf24", "First Solar Series 7 TR1 (300 kW rooftop)"),
        ("#555555", "Blighted Structures (Phase 1 demolition)"),
        ("#CE181E", "Nearby: Trappeys + UL Lafayette"),
    ]
    for i, (color, text) in enumerate(legend):
        iy = ly + 20 + i * 16
        dwg.add(dwg.rect((lx, iy), (12, 8), fill=color, rx=2))
        dwg.add(dwg.text(text, insert=(lx + 18, iy + 7), fill="#9ca3af",
                          font_size=7, font_family="Arial"))

    # ================================================================
    # SITE STATS BAR
    # ================================================================
    sy = 780
    dwg.add(dwg.rect((40, sy), (1320, 50), rx=6, fill="#111318", stroke="#1e2230"))

    stats = [
        ("BUILDING", "24' x 40' x 2 floors"),
        ("TOTAL AREA", "1,920 sq ft"),
        ("LAND", "0.60 acres (3 parcels)"),
        ("LAND DEBT", "$15,000"),
        ("GPU RACKS", "8 NVL72 (576 GPUs)"),
        ("IT LOAD", "1,040 kW"),
        ("GENERATION", "2.06 MW (N+1)"),
    ]
    sx = 65
    for label, value in stats:
        dwg.add(dwg.text(label, insert=(sx, sy + 18), fill="#6b7280",
                          font_size=7, font_family="Arial", font_weight="bold"))
        dwg.add(dwg.text(value, insert=(sx, sy + 32), fill=ACCENT,
                          font_size=10, font_family="Arial", font_weight="bold"))
        sx += 190

    # ================================================================
    # DEPLOY SEQUENCE
    # ================================================================
    ds_y = 845
    dwg.add(dwg.rect((40, ds_y), (1320, 55), rx=6, fill="#111318", stroke="#1e2230"))
    dwg.add(dwg.text("DEPLOY SEQUENCE", insert=(60, ds_y + 16), fill="#f0f2f5",
                      font_size=10, font_family="Arial", font_weight="bold"))

    steps = [
        ("1", "#ef4444", "DEMO", "3 blighted structures", "Clear site for pad + access"),
        ("2", "#6b7280", "PAD", "Concrete pad + utilities", "Generators, dry coolers, switchgear"),
        ("3", ACCENT, "FLOOR 1", "Downstairs compute", "4 NVL72 racks, 288 GPUs, CDU"),
        ("4", "#76b900", "FLOOR 2", "Upstairs compute", "4 NVL72 racks, 288 GPUs, CDU"),
    ]
    sx = 80
    for num, color, phase, target, desc in steps:
        dwg.add(dwg.text(num, insert=(sx, ds_y + 37), fill=color, font_size=16,
                          font_family="Arial", font_weight="bold"))
        dwg.add(dwg.text(phase, insert=(sx + 16, ds_y + 35), fill=color, font_size=9,
                          font_family="Arial", font_weight="bold"))
        dwg.add(dwg.text(target, insert=(sx + 16, ds_y + 45), fill="#9ca3af", font_size=7,
                          font_family="Arial"))
        sx += 330

    # ================================================================
    # NOTES
    # ================================================================
    ny = 915
    notes = [
        "1. 1201 SE Evangeline Thruway, Lafayette, LA — industrial corridor zoning, 3 adjacent parcels on Chag Street",
        "2. Land debt $15,000 — effectively debt-free. 0.60 acres total across 3 parcels.",
        "3. 3 blighted structures require Phase 1 demolition before concrete pad construction",
        "4. Building footprint matches 40-ft shipping container (24' x 40'). 2 floors = 1,920 sq ft total.",
        "5. Concrete pad houses Cat G3512H generators, BAC TrilliumSeries coolers, Eaton Beam Rubin DSX, diesel genset, Eaton xStorage BESS",
        "6. 0.5 miles from Trappeys Cannery, 0.5 miles from UL Lafayette, 60 miles from Willow Glen (fiber)",
    ]
    for i, note in enumerate(notes):
        dwg.add(dwg.text(note, insert=(35, ny + i * 11), fill="#4b5563",
                          font_size=7, font_family="Arial"))

    dwg.save()
    print(f"Saved: {OUT}")


if __name__ == "__main__":
    import os
    os.makedirs("adc3k-deploy/marlie/blueprints", exist_ok=True)
    build()
