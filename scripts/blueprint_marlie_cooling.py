"""
MARLIE I — Lafayette AI Factory & Command Center
Cooling Flow Schematic
CDUs per floor -> Facility loop -> Exterior dry coolers -> Return
45C supply, no river, no water tower. Dry coolers only.
"""
import svgwrite

W, H = 1400, 950
OUT = "adc3k-deploy/marlie/blueprints/cooling-schematic.svg"

ACCENT = "#3b82f6"


def box(dwg, x, y, w, h, label, sublabel="", color="#1a1a2e", border="#3b82f6", text_color="#e0e0e0", font=11):
    g = dwg.g()
    g.add(dwg.rect((x, y), (w, h), rx=4, ry=4, fill=color, stroke=border, stroke_width=1.5))
    lines = label.split("\n")
    ty = y + 14 + (h - len(lines) * 14) / 2
    for i, line in enumerate(lines):
        weight = "bold" if i == 0 else "normal"
        sz = font if i == 0 else font - 1
        g.add(dwg.text(line, insert=(x + w / 2, ty + i * 14), text_anchor="middle",
                        fill=text_color, font_size=sz, font_family="Arial", font_weight=weight))
    if sublabel:
        g.add(dwg.text(sublabel, insert=(x + w / 2, y + h - 4), text_anchor="middle",
                        fill="#6b7280", font_size=8, font_family="Arial"))
    dwg.add(g)


def pipe(dwg, points, color="#4fc3f7", width=3, dashed=False):
    extra = {}
    if dashed:
        extra["stroke_dasharray"] = "8,4"
    dwg.add(dwg.polyline(points, fill="none", stroke=color, stroke_width=width, **extra))


def arrow_right(dwg, x, y, color="#4fc3f7"):
    dwg.add(dwg.polygon([(x, y - 5), (x, y + 5), (x + 8, y)], fill=color))


def arrow_down(dwg, x, y, color="#4fc3f7"):
    dwg.add(dwg.polygon([(x - 5, y), (x + 5, y), (x, y + 8)], fill=color))


def arrow_left(dwg, x, y, color="#ff6b6b"):
    dwg.add(dwg.polygon([(x, y - 5), (x, y + 5), (x - 8, y)], fill=color))


def arrow_up(dwg, x, y, color="#ff6b6b"):
    dwg.add(dwg.polygon([(x - 5, y), (x + 5, y), (x, y - 8)], fill=color))


def temp_label(dwg, x, y, text, color="#4fc3f7"):
    dwg.add(dwg.text(text, insert=(x, y), fill=color, font_size=9, font_family="Arial", font_weight="bold"))


def flow_label(dwg, x, y, text, color="#6b7280"):
    dwg.add(dwg.text(text, insert=(x, y), fill=color, font_size=8, font_family="Arial"))


def build():
    dwg = svgwrite.Drawing(OUT, size=(f"{W}px", f"{H}px"), viewBox=f"0 0 {W} {H}")
    dwg.add(dwg.rect((0, 0), (W, H), fill="#0a0b0f"))

    # -- TITLE BLOCK --
    dwg.add(dwg.text("MARLIE I — LAFAYETTE AI FACTORY & COMMAND CENTER",
                      insert=(W / 2, 24), text_anchor="middle", fill="#f0f2f5",
                      font_size=16, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("COOLING FLOW SCHEMATIC | DRY COOLERS ONLY | 2 CDU PAIRS | LIQUID-COOLED GPU RACKS",
                      insert=(W / 2, 40), text_anchor="middle", fill=ACCENT,
                      font_size=10, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("Sheet C-001 | Design Intent | 2026-03-23 | NOT FOR CONSTRUCTION",
                      insert=(W / 2, 54), text_anchor="middle", fill="#6b7280",
                      font_size=9, font_family="Arial"))

    # ================================================================
    # EXTERIOR DRY COOLERS (LEFT SIDE — on concrete pad)
    # ================================================================
    dc_x = 30
    dc_y = 100

    box(dwg, dc_x, dc_y, 160, 180,
        "BAC TrilliumSeries\nADIABATIC COOLER\n(Concrete Pad)\n\nFan-Assisted\nAdiabatic\nHeat Rejection\n\nNo Water Tower\nNo River",
        "Infrastructure Yard | Outdoor",
        border="#22c55e", text_color="#22c55e")

    # Dry cooler details
    temp_label(dwg, dc_x + 5, dc_y + 200, "Ambient Rejection", "#22c55e")
    flow_label(dwg, dc_x + 5, dc_y + 215, "Louisiana peak: ~95F ambient")
    flow_label(dwg, dc_x + 5, dc_y + 228, "Capacity: ~1,500 kW rejection")
    flow_label(dwg, dc_x + 5, dc_y + 241, "Headroom for hot days + expansion")

    # ================================================================
    # FACILITY COOLING LOOP (CENTER)
    # ================================================================
    loop_x = 260
    loop_y = 90

    # Cold supply out of dry coolers
    pipe(dwg, [(190, dc_y + 60), (loop_x, dc_y + 60)], "#4fc3f7", 4)
    arrow_right(dwg, loop_x - 2, dc_y + 60, "#4fc3f7")
    temp_label(dwg, 195, dc_y + 50, "COLD SUPPLY 30-35C (86-95F)", "#4fc3f7")

    # Facility loop header
    box(dwg, loop_x, loop_y, 180, 100,
        "FACILITY\nCOOLING LOOP\n\nTreated Water/Glycol\nCirculation Pumps\nFlow Control", "",
        border="#22c55e", text_color="#86efac")

    flow_label(dwg, loop_x, loop_y - 12, "Inside building — mechanical room")

    # Return to dry coolers (hot)
    pipe(dwg, [(loop_x + 90, loop_y + 100), (loop_x + 90, loop_y + 130),
               (dc_x + 100, loop_y + 130), (dc_x + 100, dc_y + 180)], "#ff6b6b", 3)
    temp_label(dwg, loop_x - 30, loop_y + 125, "HOT RETURN TO DRY COOLERS 50-55C (122-131F)", "#ff6b6b")

    # ================================================================
    # FLOOR 1 CDU PAIR
    # ================================================================
    cdu1_x = 520
    cdu1_y = 80

    pipe(dwg, [(440, 130), (cdu1_x, 130)], "#22c55e", 3)
    arrow_right(dwg, cdu1_x - 2, 130, "#22c55e")
    temp_label(dwg, 445, 120, "FACILITY LOOP 30-35C", "#22c55e")

    box(dwg, cdu1_x, cdu1_y, 160, 110,
        "FLOOR 1\nCoolIT CHx200 (200 kW)\nCDU PAIR (N+1)\n\nStaubli UQD\nQuick-Disconnect\n\nPumps + Controls",
        "Downstairs — System 1",
        border="#76b900", text_color="#76b900")

    # ================================================================
    # FLOOR 1 DELTA IN-RACK CDU
    # ================================================================
    delta1_x = 710
    delta1_y = 85

    pipe(dwg, [(680, 110), (delta1_x, 110)], "#76b900", 3)
    arrow_right(dwg, delta1_x - 2, 110, "#76b900")

    box(dwg, delta1_x, delta1_y, 100, 60,
        "DELTA 140 kW\nIN-RACK CDU\n4RU | NVL72 Cert",
        "Per-rack precision",
        border="#00bcd4", text_color="#00e5ff", font=8)

    # ================================================================
    # FLOOR 1 RACKS
    # ================================================================
    rack1_x = 850
    r1_y = 80

    pipe(dwg, [(delta1_x + 100, 110), (rack1_x, 110)], "#76b900", 3)
    arrow_right(dwg, rack1_x - 2, 110, "#76b900")
    temp_label(dwg, delta1_x + 105, 100, "45C (113F)", "#76b900")

    # Supply manifold
    box(dwg, rack1_x, r1_y, 100, 40,
        "SUPPLY\nMANIFOLD", "", border="#76b900", text_color="#76b900", font=9)

    # 4 racks
    rack_labels = ["NVL72 R1\n130 kW", "NVL72 R2\n130 kW", "NVL72 R3\n130 kW", "NVL72 R4\n130 kW"]
    rack_ys = [130, 190, 250, 310]
    for ry, label in zip(rack_ys, rack_labels):
        pipe(dwg, [(rack1_x + 50, r1_y + 40), (rack1_x + 50, ry)], "#76b900", 2)
        box(dwg, rack1_x, ry, 100, 45, label, "Cold plates on GPU/HBM",
            color="#111a00", border="#76b900", text_color="#76b900", font=9)
        # Return right
        pipe(dwg, [(rack1_x + 100, ry + 22), (rack1_x + 130, ry + 22)], "#ff6b6b", 2)

    # Return manifold
    ret1_x = rack1_x + 130
    box(dwg, ret1_x, r1_y, 100, 40,
        "RETURN\nMANIFOLD", "", border="#ff6b6b", text_color="#ff6b6b", font=9)

    for ry in rack_ys:
        pipe(dwg, [(ret1_x + 50, ry + 22), (ret1_x + 50, r1_y + 40)], "#ff6b6b", 2)

    # Return from floor 1 manifold to CDU
    pipe(dwg, [(ret1_x + 50, r1_y + 40), (ret1_x + 50, 380), (cdu1_x + 80, 380),
               (cdu1_x + 80, cdu1_y + 110)], "#ff6b6b", 3)
    temp_label(dwg, ret1_x + 60, 375, "RETURN 55-60C (131-140F)", "#ff6b6b")

    # CDU 1 return to facility loop
    pipe(dwg, [(cdu1_x, 170), (loop_x + 180, 170)], "#ff6b6b", 3)
    temp_label(dwg, loop_x + 185, 165, "CDU1 RETURN", "#ff6b6b")

    # ================================================================
    # FLOOR 2 CDU PAIR
    # ================================================================
    cdu2_x = 520
    cdu2_y = 430

    pipe(dwg, [(440, 460), (cdu2_x, 460)], "#22c55e", 3)
    arrow_right(dwg, cdu2_x - 2, 460, "#22c55e")
    temp_label(dwg, 445, 450, "FACILITY LOOP 30-35C", "#22c55e")

    # Loop connection down to floor 2
    pipe(dwg, [(loop_x + 50, loop_y + 100), (loop_x + 50, 460), (440, 460)], "#22c55e", 3)

    box(dwg, cdu2_x, cdu2_y, 160, 110,
        "FLOOR 2\nCoolIT CHx200 (200 kW)\nCDU PAIR (N+1)\n\nStaubli UQD\nQuick-Disconnect\n\nPumps + Controls",
        "Upstairs — System 2",
        border="#76b900", text_color="#76b900")

    # ================================================================
    # FLOOR 2 DELTA IN-RACK CDU
    # ================================================================
    delta2_x = 710
    delta2_y = 435

    pipe(dwg, [(680, 460), (delta2_x, 460)], "#76b900", 3)
    arrow_right(dwg, delta2_x - 2, 460, "#76b900")

    box(dwg, delta2_x, delta2_y, 100, 60,
        "DELTA 140 kW\nIN-RACK CDU\n4RU | NVL72 Cert",
        "Per-rack precision",
        border="#00bcd4", text_color="#00e5ff", font=8)

    # ================================================================
    # FLOOR 2 RACKS
    # ================================================================
    rack2_x = 850
    r2_y = 430

    pipe(dwg, [(delta2_x + 100, 460), (rack2_x, 460)], "#76b900", 3)
    arrow_right(dwg, rack2_x - 2, 460, "#76b900")
    temp_label(dwg, delta2_x + 105, 450, "45C (113F)", "#76b900")

    box(dwg, rack2_x, r2_y, 100, 40,
        "SUPPLY\nMANIFOLD", "", border="#76b900", text_color="#76b900", font=9)

    rack_labels2 = ["NVL72 R5\n130 kW", "NVL72 R6\n130 kW", "NVL72 R7\n130 kW", "NVL72 R8\n130 kW"]
    rack_ys2 = [480, 540, 600, 660]
    for ry, label in zip(rack_ys2, rack_labels2):
        pipe(dwg, [(rack2_x + 50, r2_y + 40), (rack2_x + 50, ry)], "#76b900", 2)
        box(dwg, rack2_x, ry, 100, 45, label, "Cold plates on GPU/HBM",
            color="#111a00", border="#76b900", text_color="#76b900", font=9)
        pipe(dwg, [(rack2_x + 100, ry + 22), (rack2_x + 130, ry + 22)], "#ff6b6b", 2)

    ret2_x = rack2_x + 130
    box(dwg, ret2_x, r2_y, 100, 40,
        "RETURN\nMANIFOLD", "", border="#ff6b6b", text_color="#ff6b6b", font=9)

    for ry in rack_ys2:
        pipe(dwg, [(ret2_x + 50, ry + 22), (ret2_x + 50, r2_y + 40)], "#ff6b6b", 2)

    pipe(dwg, [(ret2_x + 50, r2_y + 40), (ret2_x + 50, 730), (cdu2_x + 80, 730),
               (cdu2_x + 80, cdu2_y + 110)], "#ff6b6b", 3)
    temp_label(dwg, ret2_x + 60, 725, "RETURN 55-60C (131-140F)", "#ff6b6b")

    # CDU 2 return to facility loop
    pipe(dwg, [(cdu2_x, 510), (loop_x + 130, 510), (loop_x + 130, loop_y + 100)], "#ff6b6b", 3)
    temp_label(dwg, loop_x + 135, 505, "CDU2 RETURN", "#ff6b6b")

    # ================================================================
    # COMPARISON CALLOUT
    # ================================================================
    nr_x = 30
    nr_y = 410
    dwg.add(dwg.rect((nr_x, nr_y), (200, 100), rx=6, fill="#111318", stroke="#555", stroke_width=1))
    dwg.add(dwg.text("MARLIE I vs TRAPPEYS", insert=(nr_x + 100, nr_y + 18),
                      text_anchor="middle", fill=ACCENT, font_size=10, font_family="Arial", font_weight="bold"))

    comparisons = [
        "MARLIE I: Dry coolers only",
        "Trappeys: Water tower + dry coolers",
        "",
        "No water tower (not on site)",
        "No river (not nearby)",
        "Simpler system, faster deploy",
    ]
    for i, line in enumerate(comparisons):
        dwg.add(dwg.text(line, insert=(nr_x + 10, nr_y + 35 + i * 11),
                          fill="#9ca3af", font_size=8, font_family="Arial"))

    # ================================================================
    # THERMAL BUDGET
    # ================================================================
    tb_x = 30
    tb_y = 530
    dwg.add(dwg.rect((tb_x, tb_y), (200, 180), rx=6, fill="#111318", stroke="#1e2230"))
    dwg.add(dwg.text("THERMAL BUDGET", insert=(tb_x + 100, tb_y + 18),
                      text_anchor="middle", fill=ACCENT, font_size=10, font_family="Arial", font_weight="bold"))

    budget = [
        ("Floor 1 IT (4x NVL72)", "520 kW"),
        ("Floor 2 IT (4x NVL72)", "520 kW"),
        ("Total IT Load", "1,040 kW"),
        ("Cooling Overhead", "~100 kW"),
        ("Facility/Network", "~100 kW"),
        ("Total Heat Rejection", "~1,240 kW"),
        ("Dry Cooler Capacity", "~1,500 kW"),
        ("Headroom", "~260 kW (21%)"),
    ]
    for i, (label, value) in enumerate(budget):
        by_pos = tb_y + 35 + i * 17
        dwg.add(dwg.text(label, insert=(tb_x + 10, by_pos), fill="#6b7280",
                          font_size=8, font_family="Arial"))
        dwg.add(dwg.text(value, insert=(tb_x + 150, by_pos), fill="#76b900",
                          font_size=8, font_family="Arial", font_weight="bold"))

    # ================================================================
    # TEMPERATURE LEGEND + SPECS
    # ================================================================
    ly = 750
    dwg.add(dwg.rect((50, ly - 5), (500, 55), rx=6, fill="#111318", stroke="#1e2230"))

    legend_items = [
        ("#4fc3f7", "Cold Supply (Dry Cooler Out 30-35C / 86-95F)"),
        ("#22c55e", "Facility Loop (Treated Water/Glycol)"),
        ("#76b900", "Rack Supply (45C / 113F)"),
        ("#ff6b6b", "Warm Return (55-60C / 131-140F)"),
    ]
    lx = 65
    for i, (color, text) in enumerate(legend_items):
        ey = ly + 5 + i * 12
        dwg.add(dwg.rect((lx, ey), (12, 6), fill=color, rx=1))
        dwg.add(dwg.text(text, insert=(lx + 18, ey + 6), fill="#9ca3af",
                          font_size=8, font_family="Arial"))

    dwg.add(dwg.rect((600, ly - 5), (650, 55), rx=6, fill="#111318", stroke="#1e2230"))
    specs = [
        ("COOLING TYPE", "BAC TrilliumSeries Adiabatic"),
        ("CDU PAIRS", "2x CoolIT CHx200 (1/floor)"),
        ("RACK COOLING", "45C Hot Water"),
        ("TOTAL REJECTION", "~1,240 kW"),
        ("PUE TARGET", "< 1.20"),
    ]
    sx = 615
    for label, value in specs:
        dwg.add(dwg.text(label, insert=(sx, ly + 12), fill="#6b7280",
                          font_size=7, font_family="Arial", font_weight="bold"))
        dwg.add(dwg.text(value, insert=(sx, ly + 24), fill="#4fc3f7",
                          font_size=10, font_family="Arial", font_weight="bold"))
        sx += 130

    # ================================================================
    # COMPLETE COOLING PATH
    # ================================================================
    fd_y = 820
    dwg.add(dwg.text("COMPLETE COOLING PATH:", insert=(50, fd_y), fill=ACCENT,
                      font_size=10, font_family="Arial", font_weight="bold"))
    path = ("BAC TrilliumSeries (30-35C) -> Facility Loop -> CoolIT CHx200 CDU (per floor) -> "
            "Delta 140 kW In-Rack CDU -> Rack Manifold (45C) -> GPU Cold Plates -> Return (55-60C) -> CDU -> Facility Loop -> BAC TrilliumSeries")
    dwg.add(dwg.text(path, insert=(50, fd_y + 16), fill="#9ca3af",
                      font_size=8, font_family="Arial"))

    # ================================================================
    # NOTES
    # ================================================================
    ny = 850
    notes = [
        "1. BAC TrilliumSeries adiabatic coolers on concrete pad — no water tower, no discharge permits, minimal water use",
        "2. No water tower at MARLIE I — unlike Trappeys. BAC TrilliumSeries sized with margin for Louisiana summer peaks (~95F)",
        "3. NVIDIA NVL72 racks use direct liquid cooling with 45C (113F) hot water supply — no chillers needed in most conditions",
        "4. 2x CoolIT CHx200 row-level CDU pairs + Delta 140 kW In-Rack CDUs (4RU, NVL72 cert) per rack — Staubli UQD — N+1 redundancy",
        "5. Facility loop uses treated water/glycol mix, Munters HCD humidity control — isolated from IT rack cooling loops via CDUs",
        "6. Total building heat rejection ~1,240 kW with ~1,500 kW BAC TrilliumSeries capacity — 21% headroom",
        "7. Ansul Novec 1230 clean-agent fire suppression + VESDA-E VEU very early smoke detection in all compute zones",
    ]
    for i, note in enumerate(notes):
        dwg.add(dwg.text(note, insert=(35, ny + i * 13), fill="#4b5563",
                          font_size=7.5, font_family="Arial"))

    dwg.save()
    print(f"Saved: {OUT}")


if __name__ == "__main__":
    import os
    os.makedirs("adc3k-deploy/marlie/blueprints", exist_ok=True)
    build()
