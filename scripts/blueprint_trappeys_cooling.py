"""
Ragin' Cajun Compute Campus — Trappeys Cannery, Lafayette, LA
Cooling Flow Schematic
Water Tower -> Dry Coolers -> Plate Heat Exchangers -> CDU -> Rack Manifolds -> Return
"""
import svgwrite

W, H = 1400, 950
OUT = "adc3k-deploy/blueprints/trappeys-cooling-schematic.svg"

ACCENT = "#CE181E"


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
    dwg.add(dwg.text("RAGIN' CAJUN COMPUTE CAMPUS — TRAPPEYS CANNERY, LAFAYETTE, LA",
                      insert=(W / 2, 24), text_anchor="middle", fill="#f0f2f5",
                      font_size=16, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("COOLING FLOW SCHEMATIC | WATER TOWER + DRY COOLERS | LIQUID-COOLED GPU RACKS",
                      insert=(W / 2, 40), text_anchor="middle", fill=ACCENT,
                      font_size=10, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("Sheet C-001 | Design Intent | 2026-03-23 | NOT FOR CONSTRUCTION",
                      insert=(W / 2, 54), text_anchor="middle", fill="#6b7280",
                      font_size=9, font_family="Arial"))

    # ================================================================
    # WATER TOWER (LEFT SIDE)
    # ================================================================
    tower_x = 30
    tower_y = 80

    # Tower representation (tall rectangle with dome top)
    dwg.add(dwg.rect((tower_x, tower_y + 40), (100, 200), rx=4, fill="#0a1628", stroke="#4fc3f7", stroke_width=2))
    # Dome top
    dwg.add(dwg.ellipse((tower_x + 50, tower_y + 40), (50, 20), fill="#0a1628", stroke="#4fc3f7", stroke_width=2))
    # Legs
    for lx in [tower_x + 15, tower_x + 85]:
        dwg.add(dwg.line((lx, tower_y + 240), (lx, tower_y + 300), stroke="#4fc3f7", stroke_width=2))

    dwg.add(dwg.text("WATER", insert=(tower_x + 50, tower_y + 100), text_anchor="middle",
                      fill="#4fc3f7", font_size=14, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("TOWER", insert=(tower_x + 50, tower_y + 118), text_anchor="middle",
                      fill="#4fc3f7", font_size=14, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("100 ft tall", insert=(tower_x + 50, tower_y + 140), text_anchor="middle",
                      fill="#6b7280", font_size=9, font_family="Arial"))
    dwg.add(dwg.text("Thermal Mass", insert=(tower_x + 50, tower_y + 155), text_anchor="middle",
                      fill="#6b7280", font_size=9, font_family="Arial"))
    dwg.add(dwg.text("Cooling Reservoir", insert=(tower_x + 50, tower_y + 170), text_anchor="middle",
                      fill="#6b7280", font_size=9, font_family="Arial"))

    # Temperature labels
    temp_label(dwg, tower_x + 5, tower_y + 200, "Storage: 70-85F", "#4fc3f7")
    temp_label(dwg, tower_x + 5, tower_y + 215, "Buffer capacity", "#6b7280")

    # ================================================================
    # DRY COOLERS (BELOW WATER TOWER)
    # ================================================================
    dc_x = 30
    dc_y = tower_y + 320

    box(dwg, dc_x, dc_y, 130, 100,
        "DRY COOLERS\n(Concrete Pad)\n\nFan-assisted\nAir-cooled\nHeat Rejection",
        "Infrastructure Yard | Outdoor",
        border="#22c55e", text_color="#22c55e")

    # Pipe from tower to dry coolers
    pipe(dwg, [(tower_x + 60, tower_y + 240), (tower_x + 60, dc_y)], "#ff6b6b", 3)
    temp_label(dwg, tower_x + 65, tower_y + 280, "HOT RETURN", "#ff6b6b")

    # Pipe from dry coolers back to tower
    pipe(dwg, [(tower_x + 40, dc_y), (tower_x + 40, tower_y + 240)], "#4fc3f7", 3)
    temp_label(dwg, tower_x - 15, tower_y + 290, "COOLED", "#4fc3f7")

    # ================================================================
    # PLATE HEAT EXCHANGERS
    # ================================================================
    hx_x = 220
    hx_y = 130

    # Cold supply pipe from water tower to PHX
    pipe(dwg, [(130, tower_y + 150), (hx_x, tower_y + 150)], "#4fc3f7", 4)
    arrow_right(dwg, hx_x - 2, tower_y + 150, "#4fc3f7")
    temp_label(dwg, 140, tower_y + 140, "COLD SUPPLY 70-85F", "#4fc3f7")

    box(dwg, hx_x, hx_y, 180, 200,
        "PLATE HEAT\nEXCHANGERS\n(PHX)\n\nTower Water (Primary)\nvs\nFacility Loop (Secondary)\n\nIsolates tower water\nfrom IT cooling loop",
        "Stainless steel plates",
        border="#22c55e", text_color="#86efac")

    # Return from PHX to water tower
    pipe(dwg, [(hx_x + 90, hx_y + 200), (hx_x + 90, hx_y + 250), (tower_x + 80, hx_y + 250),
               (tower_x + 80, tower_y + 240)], "#ff6b6b", 3)
    temp_label(dwg, hx_x - 30, hx_y + 245, "TOWER RETURN 85-95F", "#ff6b6b")
    flow_label(dwg, hx_x + 95, hx_y + 260, "Warm water returns to tower for thermal buffer / dry cooler rejection")

    # ================================================================
    # FACILITY COOLING LOOP
    # ================================================================
    cdu_x = 480
    cdu_y = 100

    pipe(dwg, [(400, 180), (cdu_x, 180)], "#22c55e", 3)
    arrow_right(dwg, cdu_x - 2, 180, "#22c55e")
    temp_label(dwg, 410, 170, "FACILITY LOOP 75-85F", "#22c55e")
    flow_label(dwg, 410, 195, "Treated water / glycol mix")

    box(dwg, cdu_x, cdu_y, 160, 200,
        "COOLANT\nDISTRIBUTION\nUNITS (CDUs)\n\nFacility Loop In\nvs\nRack Loop Out\n\nPumps + Controls\nFlow Regulation",
        "Per-row CDU pairs | N+1",
        border="#76b900", text_color="#76b900")

    # CDU location label
    flow_label(dwg, cdu_x, cdu_y - 12, "Inside Middle High Building (Compute Hall)")

    # ================================================================
    # RACK COOLING MANIFOLDS
    # ================================================================
    rack_x = 710
    manifold_y = 110

    pipe(dwg, [(640, 160), (rack_x, 160)], "#76b900", 3)
    arrow_right(dwg, rack_x - 2, 160, "#76b900")
    temp_label(dwg, 650, 150, "TO RACKS 45C (113F)", "#76b900")

    # Supply manifold header
    box(dwg, rack_x, manifold_y, 140, 55,
        "SUPPLY\nMANIFOLD\nHEADER", "",
        border="#76b900", text_color="#76b900", font=10)

    # Individual rack connections (4 racks)
    rack_positions = [200, 280, 360, 440]
    rack_labels = ["NVL72\nRack 1", "NVL72\nRack 2", "NVL72\nRack 3", "NVL72\nRack 4"]

    for i, (ry, label) in enumerate(zip(rack_positions, rack_labels)):
        # Supply down
        pipe(dwg, [(rack_x + 70, manifold_y + 55), (rack_x + 70, ry)], "#76b900", 2)

        # Rack box
        box(dwg, rack_x, ry, 140, 55,
            f"{label}\n130 kW\nLiquid Cooled",
            "Cold plates on GPU/HBM",
            color="#111a00", border="#76b900", text_color="#76b900", font=9)

        # Return right side
        pipe(dwg, [(rack_x + 140, ry + 28), (rack_x + 180, ry + 28)], "#ff6b6b", 2)

    # Return manifold
    ret_x = rack_x + 180
    box(dwg, ret_x, manifold_y, 140, 55,
        "RETURN\nMANIFOLD\nHEADER", "",
        border="#ff6b6b", text_color="#ff6b6b", font=10)

    # Return lines to return manifold
    for ry in rack_positions:
        pipe(dwg, [(ret_x + 70, ry + 28), (ret_x + 70, manifold_y + 55)], "#ff6b6b", 2)

    # Return from manifold back to CDU
    pipe(dwg, [(ret_x + 70, manifold_y + 55), (ret_x + 70, 540), (cdu_x + 80, 540),
               (cdu_x + 80, 300)], "#ff6b6b", 3)
    temp_label(dwg, ret_x + 80, 535, "RETURN FROM RACKS 55-60C (131-140F)", "#ff6b6b")

    # CDU return to PHX
    pipe(dwg, [(cdu_x, 260), (hx_x + 180, 260), (hx_x + 180, 210),
               (hx_x + 90, 210)], "#ff6b6b", 3)
    temp_label(dwg, hx_x + 190, 255, "FACILITY RETURN 95-105F", "#ff6b6b")

    # ================================================================
    # NO RIVER COOLING CALLOUT
    # ================================================================
    nr_x = 1080
    nr_y = 100
    dwg.add(dwg.rect((nr_x, nr_y), (280, 120), rx=6, fill="#111318", stroke="#555", stroke_width=1))
    dwg.add(dwg.text("TRAPPEYS vs WILLOW GLEN", insert=(nr_x + 140, nr_y + 18),
                      text_anchor="middle", fill=ACCENT, font_size=10, font_family="Arial", font_weight="bold"))

    comparisons = [
        "Trappeys: Water tower + dry coolers",
        "Willow Glen: Mississippi River once-through",
        "",
        "Water tower provides thermal buffer",
        "Dry coolers reject heat to ambient air",
        "No river = no discharge permits needed",
        "Simpler permitting, faster deployment",
        "Adequate for Phase 1 (4 racks, 650 kW)",
    ]
    for i, line in enumerate(comparisons):
        dwg.add(dwg.text(line, insert=(nr_x + 15, nr_y + 35 + i * 11),
                          fill="#9ca3af", font_size=8, font_family="Arial"))

    # ================================================================
    # THERMAL BUDGET
    # ================================================================
    tb_x = 1080
    tb_y = 250
    dwg.add(dwg.rect((tb_x, tb_y), (280, 140), rx=6, fill="#111318", stroke="#1e2230"))
    dwg.add(dwg.text("PHASE 1 THERMAL BUDGET", insert=(tb_x + 140, tb_y + 18),
                      text_anchor="middle", fill=ACCENT, font_size=10, font_family="Arial", font_weight="bold"))

    budget = [
        ("IT Load (4x NVL72)", "520 kW"),
        ("Cooling Load", "~65 kW"),
        ("Facility Load", "~50 kW"),
        ("Network Load", "~15 kW"),
        ("Total Heat Rejection", "~650 kW"),
        ("Dry Cooler Capacity", "~1,000 kW"),
        ("Headroom", "~350 kW (54%)"),
    ]
    for i, (label, value) in enumerate(budget):
        by_pos = tb_y + 35 + i * 14
        dwg.add(dwg.text(label, insert=(tb_x + 15, by_pos), fill="#6b7280",
                          font_size=8, font_family="Arial"))
        dwg.add(dwg.text(value, insert=(tb_x + 200, by_pos), fill="#76b900",
                          font_size=8, font_family="Arial", font_weight="bold"))

    # ================================================================
    # TEMPERATURE LEGEND
    # ================================================================
    ly = 620
    dwg.add(dwg.rect((50, ly - 5), (500, 60), rx=6, fill="#111318", stroke="#1e2230"))

    legend_items = [
        ("#4fc3f7", "Cold Supply (Tower Water 70-85F)"),
        ("#22c55e", "Facility Loop (Treated 75-85F)"),
        ("#76b900", "Rack Supply (45C / 113F)"),
        ("#ff6b6b", "Warm Return (55-60C / 131-140F)"),
    ]
    lx = 65
    for i, (color, text) in enumerate(legend_items):
        ey = ly + 5 + i * 12
        dwg.add(dwg.rect((lx, ey), (12, 6), fill=color, rx=1))
        dwg.add(dwg.text(text, insert=(lx + 18, ey + 6), fill="#9ca3af",
                          font_size=8, font_family="Arial"))

    # KEY SPECS
    dwg.add(dwg.rect((600, ly - 5), (650, 60), rx=6, fill="#111318", stroke="#1e2230"))
    specs = [
        ("WATER TOWER", "100 ft tall"),
        ("COOLING TYPE", "Dry Coolers"),
        ("RACK COOLING", "45C Hot Water"),
        ("TOTAL REJECTION", "~650 kW"),
        ("PUE TARGET", "< 1.25"),
    ]
    sx = 615
    for label, value in specs:
        dwg.add(dwg.text(label, insert=(sx, ly + 12), fill="#6b7280",
                          font_size=7, font_family="Arial", font_weight="bold"))
        dwg.add(dwg.text(value, insert=(sx, ly + 24), fill="#4fc3f7",
                          font_size=10, font_family="Arial", font_weight="bold"))
        sx += 130

    # ================================================================
    # FLOW DIAGRAM: COMPLETE COOLING PATH
    # ================================================================
    fd_y = 700
    dwg.add(dwg.text("COMPLETE COOLING PATH:", insert=(50, fd_y), fill=ACCENT,
                      font_size=10, font_family="Arial", font_weight="bold"))
    path = ("Water Tower (70-85F) -> Plate HX -> Facility Loop (75-85F) -> CDU -> "
            "Rack Manifold (45C) -> GPU Cold Plates -> Return (55-60C) -> CDU -> PHX -> Tower -> Dry Coolers")
    dwg.add(dwg.text(path, insert=(50, fd_y + 16), fill="#9ca3af",
                      font_size=8, font_family="Arial"))

    # ================================================================
    # NOTES
    # ================================================================
    ny = 740
    notes = [
        "1. Water tower (100 ft tall, on-property) serves as thermal mass / cooling reservoir — massive thermal buffer for GPU load spikes",
        "2. Dry coolers on concrete pad (infrastructure yard) reject heat to ambient air — no water consumption, no discharge permits",
        "3. Plate heat exchangers isolate tower water from facility cooling loop — prevents contamination of IT systems",
        "4. NVIDIA NVL72 racks use direct liquid cooling with 45C (113F) hot water supply — no chillers needed in most conditions",
        "5. CDUs regulate flow and temperature per rack row — N+1 redundancy, located inside Middle High building",
        "6. No river cooling like Willow Glen — Trappeys uses closed-loop water tower + dry cooler system",
        "7. Water tower thermal buffer absorbs GPU training spike loads — dry coolers handle steady-state rejection",
        "8. Phase 1 thermal load ~650 kW with ~1,000 kW dry cooler capacity — 54% headroom for expansion or hot days",
        "9. Summer ambient ~95F peak: dry coolers may need supplemental evaporative pre-cooling (future upgrade path)",
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
