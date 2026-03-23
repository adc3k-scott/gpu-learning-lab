"""
Ragin' Cajun Compute Campus — Trappeys Cannery, Lafayette, LA
Electrical Single-Line Diagram
ATMOS gas -> Cat G3520C (480V AC) -> Eaton rectifier -> 800V DC bus -> busway -> PDU -> 64:1 LLC -> GPU
"""
import svgwrite

W, H = 1400, 1000
OUT = "adc3k-deploy/blueprints/trappeys-electrical-sld.svg"

ACCENT = "#CE181E"  # Vermilion red


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


def bus(dwg, x, y, w, label, color="#fbbf24"):
    dwg.add(dwg.rect((x, y - 3), (w, 6), fill=color, rx=2))
    dwg.add(dwg.text(label, insert=(x + w / 2, y - 8), text_anchor="middle",
                      fill=color, font_size=10, font_family="Arial", font_weight="bold"))


def wire(dwg, x1, y1, x2, y2, color="#555"):
    dwg.add(dwg.line((x1, y1), (x2, y2), stroke=color, stroke_width=1.5))


def arrow_down(dwg, x, y1, y2, color="#555"):
    wire(dwg, x, y1, x, y2, color)
    dwg.add(dwg.polygon([(x - 4, y2 - 6), (x + 4, y2 - 6), (x, y2)], fill=color))


def build():
    dwg = svgwrite.Drawing(OUT, size=(f"{W}px", f"{H}px"), viewBox=f"0 0 {W} {H}")
    dwg.add(dwg.rect((0, 0), (W, H), fill="#0a0b0f"))

    # -- TITLE BLOCK --
    dwg.add(dwg.text("RAGIN' CAJUN COMPUTE CAMPUS — TRAPPEYS CANNERY, LAFAYETTE, LA",
                      insert=(W / 2, 24), text_anchor="middle", fill="#f0f2f5",
                      font_size=16, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("ELECTRICAL SINGLE-LINE DIAGRAM | 800V DC NATIVE ARCHITECTURE | NVIDIA DSX REFERENCE DESIGN",
                      insert=(W / 2, 40), text_anchor="middle", fill=ACCENT,
                      font_size=10, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("Sheet E-001 | Design Intent | 2026-03-23 | NOT FOR CONSTRUCTION",
                      insert=(W / 2, 54), text_anchor="middle", fill="#6b7280",
                      font_size=9, font_family="Arial"))

    # ================================================================
    # ROW 1: SOURCES (y=75)
    # ================================================================
    y1 = 75

    # ATMOS Gas Supply
    box(dwg, 30, y1, 150, 55,
        "ATMOS ENERGY\nGas Trunk Line",
        "On-property | Henry Hub pricing",
        color="#0a1a0a", border="#22c55e", text_color="#22c55e")

    # Cat G3520C #1
    gen_kw = {"color": "#0a1a0a", "border": "#22c55e", "text_color": "#22c55e"}
    box(dwg, 220, y1, 140, 55, "CAT G3520C #1\n1.5 MW | 480V AC", "Natural Gas | Layer 2", **gen_kw)
    box(dwg, 380, y1, 140, 55, "CAT G3520C #2\n1.5 MW | 480V AC", "N+1 Redundant", **gen_kw)

    # First Solar Rooftop
    box(dwg, 560, y1, 160, 55, "FIRST SOLAR\nRooftop Arrays", "3,731 panels | 2.05 MW | All 4 buildings",
        color="#1a1a00", border="#fbbf24", text_color="#fbbf24")

    # Diesel Emergency
    box(dwg, 760, y1, 130, 55, "DIESEL GENSET\nEmergency", "Layer 3 | Pipeline-Independent",
        color="#2e1a1a", border="#ef4444", text_color="#ef4444")

    # LUS Grid (sell-back)
    box(dwg, 930, y1, 130, 55, "LUS GRID\nSELL-BACK ONLY", "Layer 4 | Excess to grid",
        color="#1a0a0a", border="#ef4444", text_color="#ef4444")

    # Eaton BESS
    box(dwg, 1100, y1, 130, 55, "EATON xStorage\nBESS", "800V DC | Ride-through\nPeak shaving",
        border="#3b82f6", text_color="#93c5fd")

    # ================================================================
    # ROW 2: PARALLELING / SWITCHGEAR (y=180)
    # ================================================================
    y2 = 180

    arrow_down(dwg, 100, y1 + 55, y2, "#22c55e")
    arrow_down(dwg, 290, y1 + 55, y2, "#22c55e")
    arrow_down(dwg, 450, y1 + 55, y2, "#22c55e")
    arrow_down(dwg, 825, y1 + 55, y2, "#ef4444")

    box(dwg, 30, y2, 240, 50,
        "PARALLELING SWITCHGEAR + ATS\n480V AC | Auto-Sync | Load Sharing",
        "Louisiana Cat controls | Both G3520C to common bus",
        border="#22c55e")

    box(dwg, 290, y2, 180, 50,
        "MAIN BREAKER + METERING\n480V AC Rated | Protection Relays",
        "", border="#ff6b35", text_color="#ff6b35")

    box(dwg, 740, y2, 170, 50,
        "EMERGENCY ATS\nDiesel Auto-Transfer", "Auto-start on dual gas failure",
        border="#ef4444")

    # ================================================================
    # ROW 3: 480V AC BUS (y=275)
    # ================================================================
    y3 = 275
    arrow_down(dwg, 150, y2 + 50, y3, "#22c55e")
    arrow_down(dwg, 380, y2 + 50, y3, "#ff6b35")
    arrow_down(dwg, 825, y2 + 50, y3, "#ef4444")

    bus(dwg, 30, y3, 940, "480V AC DISTRIBUTION BUS", "#ff6b35")

    # LUS sell-back arrow
    wire(dwg, 995, y1 + 55, 995, y3 - 20, "#ef4444")
    dwg.add(dwg.text("SELL-BACK TO LUS (Layer 4)", insert=(1005, y3 - 25),
                      fill="#ef4444", font_size=8, font_family="Arial"))
    wire(dwg, 940, y3, 995, y3, "#ef4444")

    # ================================================================
    # ROW 4: RECTIFICATION (y=320)
    # ================================================================
    y4 = 320

    rect_positions = [150, 450, 750]
    for rx in rect_positions:
        arrow_down(dwg, rx, y3 + 3, y4, "#ff6b35")

    box(dwg, 60, y4, 200, 55, "EATON BEAM RUBIN DSX\n480V AC -> 800V DC\nRectifier Module #1",
        "96%+ Efficiency",
        border="#8b5cf6", text_color="#c4b5fd")

    box(dwg, 350, y4, 200, 55, "EATON BEAM RUBIN DSX\n480V AC -> 800V DC\nRectifier Module #2",
        "N+1 Redundant",
        border="#8b5cf6", text_color="#c4b5fd")

    # Solar DC-Direct bypass
    solar_dc_x = 640
    wire(dwg, 640, y1 + 55, 640, y1 + 70, "#fbbf24")
    wire(dwg, 640, y1 + 70, solar_dc_x + 70, y1 + 70, "#fbbf24")
    wire(dwg, solar_dc_x + 70, y1 + 70, solar_dc_x + 70, y4, "#fbbf24")
    box(dwg, solar_dc_x, y4, 200, 55, "DC-DC BUCK CONVERTER\n952V String -> 800V DC",
        "Solar DC-Direct | 97% Eff | Bypasses AC",
        border="#fbbf24", text_color="#fbbf24")

    # Diesel to 480V bus
    box(dwg, 860, y4, 110, 55, "DIESEL\nFEED\nTo 480V Bus", "",
        border="#ef4444", text_color="#fca5a5", font=9)
    arrow_down(dwg, 915, y3 + 3, y4, "#ef4444")

    # ================================================================
    # ROW 5: 800V DC BUS (y=425)
    # ================================================================
    y5 = 425
    for rx in [160, 450, 740]:
        arrow_down(dwg, rx, y4 + 55, y5, "#8b5cf6")

    bus(dwg, 30, y5, 940, "800V DC DISTRIBUTION BUS — NVIDIA DSX REFERENCE ARCHITECTURE", "#8b5cf6")

    # BESS connection to 800V bus
    wire(dwg, 1165, y1 + 55, 1165, y5, "#3b82f6")
    dwg.add(dwg.text("BESS on", insert=(1175, y5 - 20), fill="#93c5fd", font_size=7, font_family="Arial"))
    dwg.add(dwg.text("800V DC", insert=(1175, y5 - 10), fill="#93c5fd", font_size=7, font_family="Arial"))

    # ================================================================
    # ROW 6: EATON BUSWAY (y=480)
    # ================================================================
    y6 = 480

    busway_positions = [150, 370, 590, 810]
    for bx in busway_positions:
        arrow_down(dwg, bx + 55, y5 + 3, y6, "#8b5cf6")
        box(dwg, bx, y6, 110, 40, "EATON BUSWAY\n800V DC", "",
            border="#8b5cf6", text_color="#c4b5fd", font=9)

    # ================================================================
    # ROW 7: RACK PDUs (y=555)
    # ================================================================
    y7 = 555
    for bx in busway_positions:
        arrow_down(dwg, bx + 55, y6 + 40, y7, "#8b5cf6")
        box(dwg, bx, y7, 110, 40, "RACK PDU\n800V DC Input", "",
            border="#8b5cf6", text_color="#c4b5fd", font=9)

    # ================================================================
    # ROW 8: LLC CONVERTERS (y=630)
    # ================================================================
    y8 = 630
    for bx in busway_positions:
        arrow_down(dwg, bx + 55, y7 + 40, y8, "#8b5cf6")
        box(dwg, bx, y8, 110, 40, "64:1 LLC DC-DC\n800V -> 12.5V", "99%+ Efficiency",
            border="#76b900", text_color="#76b900", font=9)

    # ================================================================
    # ROW 9: GPU RACKS (y=710)
    # ================================================================
    y9 = 710
    rack_labels = [
        "NVIDIA NVL72\nRACK 1\n130 kW",
        "NVIDIA NVL72\nRACK 2\n130 kW",
        "NVIDIA NVL72\nRACK 3\n130 kW",
        "NVIDIA NVL72\nRACK 4\n130 kW",
    ]
    for bx, label in zip(busway_positions, rack_labels):
        arrow_down(dwg, bx + 55, y8 + 40, y9, "#76b900")
        box(dwg, bx, y9, 110, 60, label, "Vera Rubin | Liquid Cooled",
            color="#111a00", border="#76b900", text_color="#76b900", font=9)

    # ================================================================
    # PHASE 1 SUMMARY BAR
    # ================================================================
    sy = 800
    dwg.add(dwg.rect((30, sy), (1340, 45), rx=6, fill="#111318", stroke="#1e2230", stroke_width=1))
    stats = [
        ("PHASE 1 IT LOAD", "520 kW (4 racks)"),
        ("COOLING", "~65 kW"),
        ("FACILITY", "~50 kW"),
        ("NETWORK", "~15 kW"),
        ("TOTAL DRAW", "~650 kW"),
        ("GENSET CAPACITY", "3,000 kW (N+1)"),
    ]
    sx = 60
    for label, value in stats:
        dwg.add(dwg.text(label, insert=(sx, sy + 16), fill="#6b7280",
                          font_size=8, font_family="Arial", font_weight="bold"))
        dwg.add(dwg.text(value, insert=(sx, sy + 30), fill=ACCENT,
                          font_size=11, font_family="Arial", font_weight="bold"))
        sx += 220

    # ================================================================
    # NOTES
    # ================================================================
    ny = 860
    notes = [
        "1. 2x Cat G3520C natural gas generators: 1.5 MW each, 480V AC output — ATMOS gas trunk line on property",
        "2. N+1 redundancy: each genset at ~22% load in Phase 1 (650 kW on 3,000 kW capacity)",
        "3. Eaton Beam Rubin DSX rectifiers convert 480V AC to 800V DC per NVIDIA DSX Reference Design",
        "4. First Solar rooftop arrays connect DC-Direct: 952V strings buck to 800V at 97% efficiency, bypassing AC",
        "5. 64:1 LLC resonant converters: 800V DC to 12.5V at GPU die — 99%+ conversion efficiency",
        "6. LUS grid is SELL-BACK ONLY (Layer 4) — excess power returns to grid, never consumed from grid",
        "7. Eaton xStorage BESS on 800V DC bus — ride-through for transfer events + peak shaving",
        "8. Diesel emergency genset (Layer 3) provides pipeline-independent backup, auto-start on dual gas failure",
        "9. All 4 buildings receive rooftop solar: 3,731 First Solar TR1 panels = 2.05 MW total",
    ]
    for i, note in enumerate(notes):
        dwg.add(dwg.text(note, insert=(35, ny + i * 13), fill="#4b5563",
                          font_size=8, font_family="Arial"))

    # 4-Layer legend
    ly = ny + len(notes) * 13 + 10
    layers = [
        ("LAYER 1: SOLAR", "#fbbf24", "Primary Offset — 2.05 MW rooftop"),
        ("LAYER 2: NATURAL GAS", "#22c55e", "Backbone — 2x G3520C 24/7"),
        ("LAYER 3: DIESEL", "#ef4444", "Emergency Only"),
        ("LAYER 4: GRID (LUS)", "#ef4444", "Sell-Back Only"),
    ]
    lx = 35
    for label, color, desc in layers:
        dwg.add(dwg.rect((lx, ly - 8), (8, 8), fill=color))
        dwg.add(dwg.text(f"{label} — {desc}", insert=(lx + 14, ly), fill="#6b7280",
                          font_size=8, font_family="Arial", font_weight="bold"))
        lx += 330

    dwg.save()
    print(f"Saved: {OUT}")


if __name__ == "__main__":
    import os
    os.makedirs("adc3k-deploy/blueprints", exist_ok=True)
    build()
