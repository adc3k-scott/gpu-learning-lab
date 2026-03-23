"""
Willow Glen Tiger Compute Campus — Cooling Flow Schematic
Mississippi River → Heat Exchangers → CDU Loops → NVL72 Racks
SVG output
"""
import svgwrite

W, H = 1400, 900
OUT = "adc3k-deploy/blueprints/cooling-schematic.svg"


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
    """Draw a pipe (polyline) with optional dashing."""
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

    # ── TITLE BLOCK ──
    dwg.add(dwg.text("TIGER COMPUTE CAMPUS — WILLOW GLEN, ST. GABRIEL, LA",
                      insert=(W / 2, 24), text_anchor="middle", fill="#f0f2f5",
                      font_size=16, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("COOLING FLOW SCHEMATIC | MISSISSIPPI RIVER ONCE-THROUGH + LIQUID-COOLED GPU RACKS",
                      insert=(W / 2, 40), text_anchor="middle", fill="#4fc3f7",
                      font_size=10, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("Sheet C-001 | MVP Design Intent | 2026-03-22 | NOT FOR CONSTRUCTION",
                      insert=(W / 2, 54), text_anchor="middle", fill="#6b7280",
                      font_size=9, font_family="Arial"))

    # ════════════════════════════════════════════
    # MISSISSIPPI RIVER (LEFT SIDE)
    # ════════════════════════════════════════════
    # River representation
    river_x = 30
    dwg.add(dwg.rect((river_x, 80), (100, 680), rx=8, fill="#0a1628", stroke="#1e3a5f", stroke_width=2))
    dwg.add(dwg.text("MISSISSIPPI", insert=(river_x + 50, 120), text_anchor="middle",
                      fill="#1e3a5f", font_size=14, font_family="Arial", font_weight="bold",
                      transform=f"rotate(90, {river_x + 50}, 120)"))
    dwg.add(dwg.text("RIVER", insert=(river_x + 50, 180), text_anchor="middle",
                      fill="#1e3a5f", font_size=14, font_family="Arial", font_weight="bold",
                      transform=f"rotate(90, {river_x + 50}, 180)"))
    # River temp
    temp_label(dwg, river_x + 10, 760, "Avg: 68-82F", "#1e3a5f")
    temp_label(dwg, river_x + 10, 772, "3,500 ft frontage", "#1e3a5f")

    # ════════════════════════════════════════════
    # STAGE 1: INTAKE STRUCTURE
    # ════════════════════════════════════════════
    intake_x = 170
    intake_y = 120

    # Cold supply pipe from river
    pipe(dwg, [(130, 200), (intake_x, 200)], "#4fc3f7", 4)
    arrow_right(dwg, intake_x - 2, 200, "#4fc3f7")
    temp_label(dwg, 135, 190, "COLD SUPPLY", "#4fc3f7")

    box(dwg, intake_x, intake_y, 150, 160,
        "RIVER WATER\nINTAKE\nSTRUCTURE\n\nTrash Racks\nTraveling Screens\nIntake Pumps",
        "43 ft depth | Existing infrastructure",
        border="#4fc3f7", text_color="#4fc3f7")

    # Warm return pipe to river
    pipe(dwg, [(intake_x, 500), (130, 500)], "#ff6b6b", 4)
    arrow_left(dwg, 132, 500, "#ff6b6b")
    temp_label(dwg, 135, 490, "WARM RETURN", "#ff6b6b")

    # ════════════════════════════════════════════
    # STAGE 2: FILTRATION
    # ════════════════════════════════════════════
    filter_x = 370
    filter_y = 140

    pipe(dwg, [(320, 200), (filter_x, 200)], "#4fc3f7", 3)
    arrow_right(dwg, filter_x - 2, 200, "#4fc3f7")
    temp_label(dwg, 330, 190, "68-82F", "#4fc3f7")

    box(dwg, filter_x, filter_y, 130, 120,
        "FILTRATION\nSYSTEM\n\nSand Filters\nStrainers\nChemical Treatment",
        "Prevent fouling",
        border="#4fc3f7", text_color="#93c5fd")

    # ════════════════════════════════════════════
    # STAGE 3: PLATE HEAT EXCHANGERS
    # ════════════════════════════════════════════
    hx_x = 550
    hx_y = 100

    pipe(dwg, [(500, 200), (hx_x, 200)], "#4fc3f7", 3)
    arrow_right(dwg, hx_x - 2, 200, "#4fc3f7")

    box(dwg, hx_x, hx_y, 180, 200,
        "PLATE HEAT\nEXCHANGERS\n(PHX)\n\nRiver Water (Primary)\nvs\nFacility Loop (Secondary)\n\nIsolates river from\nIT cooling loop",
        "Titanium plates | Corrosion-resistant",
        border="#22c55e", text_color="#86efac")

    # River water return from HX
    pipe(dwg, [(hx_x + 90, 300), (hx_x + 90, 380), (filter_x + 65, 380), (filter_x + 65, 500),
               (intake_x + 75, 500)], "#ff6b6b", 3)
    arrow_left(dwg, intake_x + 77, 500, "#ff6b6b")
    temp_label(dwg, hx_x - 20, 375, "RIVER RETURN 78-92F", "#ff6b6b")
    flow_label(dwg, filter_x + 70, 510, "Thermal discharge to Mississippi (LPDES LA0005851)")

    # ════════════════════════════════════════════
    # STAGE 4: FACILITY COOLING LOOP
    # ════════════════════════════════════════════
    # Cool side out of HX
    loop_y = 180
    cdu_x = 800

    pipe(dwg, [(730, loop_y), (cdu_x, loop_y)], "#22c55e", 3)
    arrow_right(dwg, cdu_x - 2, loop_y, "#22c55e")
    temp_label(dwg, 740, loop_y - 10, "FACILITY LOOP 75-85F", "#22c55e")
    flow_label(dwg, 740, loop_y + 15, "Treated water / glycol mix")

    # CDU Bank
    cdu_y = 100
    box(dwg, cdu_x, cdu_y, 160, 180,
        "COOLANT\nDISTRIBUTION\nUNITS (CDUs)\n\nFacility Loop In\nvs\nRack Loop Out\n\nPumps + Controls\nFlow Regulation",
        "Per-row CDU pairs | N+1",
        border="#76b900", text_color="#76b900")

    # ════════════════════════════════════════════
    # STAGE 5: RACK COOLING MANIFOLDS
    # ════════════════════════════════════════════
    rack_x = 1020
    manifold_y = 110

    pipe(dwg, [(960, 160), (rack_x, 160)], "#76b900", 3)
    arrow_right(dwg, rack_x - 2, 160, "#76b900")
    temp_label(dwg, 965, 150, "TO RACKS 45C (113F)", "#76b900")

    # Rack manifold header
    box(dwg, rack_x, manifold_y, 140, 60,
        "SUPPLY\nMANIFOLD\nHEADER",
        "",
        border="#76b900", text_color="#76b900", font=10)

    # Individual rack connections
    rack_positions = [200, 280, 360, 440, 520]
    rack_labels = ["NVL72\nRack 1-7", "NVL72\nRack 8-14", "NVL72\nRack 15-21", "NVL72\nRack 22-28", "NVL72\nRack 29-36"]

    for i, (ry, label) in enumerate(zip(rack_positions, rack_labels)):
        # Supply down
        pipe(dwg, [(rack_x + 70, manifold_y + 60), (rack_x + 70, ry)], "#76b900", 2)

        # Rack box
        box(dwg, rack_x, ry, 140, 55,
            f"{label}\n130 kW each\nLiquid Cooled",
            "Cold plates on GPU/HBM",
            color="#111a00", border="#76b900", text_color="#76b900", font=9)

        # Return right side
        pipe(dwg, [(rack_x + 140, ry + 28), (rack_x + 180, ry + 28)], "#ff6b6b", 2)

    # Return manifold
    ret_x = rack_x + 180
    box(dwg, ret_x, manifold_y, 140, 60,
        "RETURN\nMANIFOLD\nHEADER",
        "",
        border="#ff6b6b", text_color="#ff6b6b", font=10)

    # Return lines to return manifold
    for ry in rack_positions:
        pipe(dwg, [(ret_x + 70, ry + 28), (ret_x + 70, manifold_y + 60)], "#ff6b6b", 2)

    # Return from manifold back to CDU
    pipe(dwg, [(ret_x + 70, manifold_y + 60), (ret_x + 70, 620), (cdu_x + 80, 620),
               (cdu_x + 80, 280)], "#ff6b6b", 3)
    temp_label(dwg, ret_x + 80, 615, "RETURN FROM RACKS 55-60C (131-140F)", "#ff6b6b")

    # CDU return to HX
    pipe(dwg, [(cdu_x, 250), (hx_x + 180, 250), (hx_x + 180, loop_y + 60),
               (hx_x + 90, loop_y + 60)], "#ff6b6b", 3)
    temp_label(dwg, hx_x + 190, 245, "FACILITY RETURN 95-105F", "#ff6b6b")

    # ════════════════════════════════════════════
    # WASTE HEAT RECOVERY (OPTIONAL)
    # ════════════════════════════════════════════
    whr_y = 650
    box(dwg, 550, whr_y, 200, 70,
        "ORC WASTE HEAT\nRECOVERY (FUTURE)\n8-11 MW from exhaust",
        "Ormat Technologies | $10-18M/yr value",
        border="#fbbf24", text_color="#fbbf24")

    box(dwg, 800, whr_y, 200, 70,
        "ABSORPTION CHILLER\n(FUTURE)\n11,000+ tons cooling",
        "YORK/Trane | Waste heat driven",
        border="#fbbf24", text_color="#fbbf24")

    # Dotted lines for future
    pipe(dwg, [(650, whr_y), (650, 620)], "#fbbf24", 1, dashed=True)
    pipe(dwg, [(900, whr_y), (900, 620)], "#fbbf24", 1, dashed=True)
    flow_label(dwg, 555, whr_y - 8, "FUTURE WASTE HEAT RECOVERY — Exhaust heat from generators + hot return water")

    # ════════════════════════════════════════════
    # TEMPERATURE LEGEND
    # ════════════════════════════════════════════
    ly = 760
    dwg.add(dwg.rect((170, ly - 5), (500, 55), rx=6, fill="#111318", stroke="#1e2230"))

    legend_items = [
        ("#4fc3f7", "Cold Supply (River Water 68-82F)"),
        ("#22c55e", "Facility Loop (Treated 75-85F)"),
        ("#76b900", "Rack Supply (45C / 113F)"),
        ("#ff6b6b", "Warm Return (55-60C / 131-140F)"),
        ("#fbbf24", "Future Waste Heat Recovery"),
    ]
    lx = 185
    for i, (color, text) in enumerate(legend_items):
        ey = ly + 5 + i * 10
        dwg.add(dwg.rect((lx, ey), (12, 6), fill=color, rx=1))
        dwg.add(dwg.text(text, insert=(lx + 18, ey + 6), fill="#9ca3af",
                          font_size=8, font_family="Arial"))

    # ════════════════════════════════════════════
    # KEY SPECS
    # ════════════════════════════════════════════
    sy = 760
    dwg.add(dwg.rect((720, sy - 5), (650, 55), rx=6, fill="#111318", stroke="#1e2230"))

    specs = [
        ("RIVER FRONTAGE", "3,500 ft"),
        ("DOCK DEPTH", "43 ft"),
        ("COOLING SOURCE", "Once-Through"),
        ("RACK COOLING", "45C Hot Water"),
        ("DISCHARGE PERMIT", "LPDES LA0005851"),
    ]
    sx = 735
    for label, value in specs:
        dwg.add(dwg.text(label, insert=(sx, sy + 12), fill="#6b7280",
                          font_size=7, font_family="Arial", font_weight="bold"))
        dwg.add(dwg.text(value, insert=(sx, sy + 24), fill="#4fc3f7",
                          font_size=10, font_family="Arial", font_weight="bold"))
        sx += 130

    # ════════════════════════════════════════════
    # NOTES
    # ════════════════════════════════════════════
    ny = 830
    notes = [
        "1. Mississippi River provides unlimited cooling capacity — 3,500 ft of frontage, 43-ft deepwater dock on-site",
        "2. Once-through cooling was the original system for the 2,200 MW Entergy plant — intake infrastructure may still exist (verify on site visit)",
        "3. Plate heat exchangers isolate river water from the facility cooling loop — prevents contamination of IT systems",
        "4. NVIDIA NVL72 racks use direct liquid cooling with 45C (113F) hot water supply — no chillers needed in most conditions",
        "5. CDUs regulate flow and temperature per rack row — N+1 redundancy ensures no single point of failure",
        "6. LPDES permit LA0005851 already transferred to Willow Glen Ventures (Aug 2019) — thermal discharge pre-permitted",
        "7. ORC waste heat recovery (future) can generate 8-11 MW of electricity from generator exhaust — Ormat Technologies",
        "8. Absorption chillers (future) can produce 11,000+ tons of cooling from waste heat — eliminates mechanical cooling entirely",
    ]
    for i, note in enumerate(notes):
        dwg.add(dwg.text(note, insert=(35, ny + i * 12), fill="#4b5563",
                          font_size=7, font_family="Arial"))

    dwg.save()
    print(f"Saved: {OUT}")


if __name__ == "__main__":
    import os
    os.makedirs("adc3k-deploy/blueprints", exist_ok=True)
    build()
