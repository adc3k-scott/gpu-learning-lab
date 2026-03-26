"""
MARLIE I — Lafayette AI Factory & Command Center
Power Distribution Schematic
4-Layer Hierarchy: Solar -> Gas -> Diesel -> Grid (backup, NOT sell-back)
MARLIE I is DIFFERENT from Trappeys — grid is Layer 4 BACKUP, not sell-back
"""
import svgwrite

W, H = 1400, 1200
OUT = "adc3k-deploy/marlie/blueprints/power-distribution.svg"

ACCENT = "#3b82f6"


def box(dwg, x, y, w, h, label, sublabel="", color="#1a1a2e", border="#3b82f6", text_color="#e0e0e0", font=10):
    g = dwg.g()
    g.add(dwg.rect((x, y), (w, h), rx=4, ry=4, fill=color, stroke=border, stroke_width=1.5))
    lines = label.split("\n")
    ty = y + 12 + (h - len(lines) * 13) / 2
    for i, line in enumerate(lines):
        weight = "bold" if i == 0 else "normal"
        sz = font if i == 0 else font - 1
        g.add(dwg.text(line, insert=(x + w / 2, ty + i * 13), text_anchor="middle",
                        fill=text_color, font_size=sz, font_family="Arial", font_weight=weight))
    if sublabel:
        g.add(dwg.text(sublabel, insert=(x + w / 2, y + h - 4), text_anchor="middle",
                        fill="#6b7280", font_size=7, font_family="Arial"))
    dwg.add(g)


def wire(dwg, x1, y1, x2, y2, color="#555", width=1.5):
    dwg.add(dwg.line((x1, y1), (x2, y2), stroke=color, stroke_width=width))


def pipe(dwg, points, color="#555", width=1.5, dashed=False):
    extra = {}
    if dashed:
        extra["stroke_dasharray"] = "6,3"
    dwg.add(dwg.polyline(points, fill="none", stroke=color, stroke_width=width, **extra))


def arrow_down(dwg, x, y1, y2, color="#555"):
    wire(dwg, x, y1, x, y2, color)
    dwg.add(dwg.polygon([(x - 4, y2 - 6), (x + 4, y2 - 6), (x, y2)], fill=color))


def arrow_right(dwg, x1, y, x2, color="#555"):
    wire(dwg, x1, y, x2, y, color)
    dwg.add(dwg.polygon([(x2 - 6, y - 4), (x2 - 6, y + 4), (x2, y)], fill=color))


def build():
    dwg = svgwrite.Drawing(OUT, size=(f"{W}px", f"{H}px"), viewBox=f"0 0 {W} {H}")
    dwg.add(dwg.rect((0, 0), (W, H), fill="#0a0b0f"))

    # -- TITLE --
    dwg.add(dwg.text("MARLIE I — LAFAYETTE AI FACTORY & COMMAND CENTER",
                      insert=(W / 2, 24), text_anchor="middle", fill="#f0f2f5",
                      font_size=16, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("POWER DISTRIBUTION SCHEMATIC | FUEL TO CHIP | 4-LAYER POWER HIERARCHY | 1,040 kW IT",
                      insert=(W / 2, 40), text_anchor="middle", fill=ACCENT,
                      font_size=10, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("Sheet P-001 | Design Intent | 2026-03-23 | NOT FOR CONSTRUCTION",
                      insert=(W / 2, 54), text_anchor="middle", fill="#6b7280",
                      font_size=9, font_family="Arial"))

    # ================================================================
    # ROW 1: FUEL SOURCES (y=75)
    # ================================================================
    y1 = 75

    box(dwg, 30, y1, 130, 55, "ATMOS ENERGY\nNatural Gas\nOn Property", "Henry Hub 40 mi",
        color="#0a1a0a", border="#22c55e", text_color="#22c55e")

    box(dwg, 180, y1, 100, 55, "GAS METER\n+ REGULATOR\nStation", "Custody transfer",
        border="#22c55e", text_color="#86efac")

    box(dwg, 310, y1, 120, 55, "DIESEL FUEL\nSTORAGE\n2,000 gal", "Layer 3 backup",
        color="#2e1a1a", border="#ef4444", text_color="#ef4444")

    box(dwg, 460, y1, 130, 55, "SOLAR\nIRRADIANCE\n4.5-5.2 kWh/m2/day", "300 kW Rooftop",
        color="#1a1a00", border="#fbbf24", text_color="#fbbf24")

    box(dwg, 620, y1, 130, 55, "LUS BACKUP\nGRID\nBACKUP ONLY", "Layer 4 — dual feed",
        color="#1a0a0a", border="#ef4444", text_color="#ef4444")

    arrow_down(dwg, 95, y1 + 55, y1 + 85, "#22c55e")
    arrow_down(dwg, 230, y1 + 55, y1 + 85, "#22c55e")
    arrow_down(dwg, 370, y1 + 55, y1 + 85, "#ef4444")
    arrow_down(dwg, 525, y1 + 55, y1 + 85, "#fbbf24")

    # ================================================================
    # ROW 2: GENERATION (y=165)
    # ================================================================
    y2 = 165

    box(dwg, 30, y2, 140, 65, "CAT G3512H #1\n1.03 MW | 480V AC\nNatural Gas Prime\nLayer 2 Backbone",
        "Caterpillar | American Made",
        color="#0a1a0a", border="#22c55e", text_color="#22c55e")
    box(dwg, 185, y2, 140, 65, "CAT G3512H #2\n1.03 MW | 480V AC\nN+1 REDUNDANT\nMaintenance Spare",
        "Either offline = no impact",
        color="#0a1a0a", border="#22c55e", text_color="#4ade80")

    box(dwg, 340, y2, 110, 65, "DIESEL GENSET\n250 kW\n480V | Emergency\nAuto-Start", "Layer 3 only",
        color="#2e1a1a", border="#ef4444", text_color="#ef4444")

    box(dwg, 470, y2, 140, 65, "SOLAR ARRAY\n300 kW Rooftop\nFirst Solar Series 7 TR1\n5-panel strings @ 952V",
        "550W panels | DC-Direct",
        color="#1a1a00", border="#fbbf24", text_color="#fbbf24")

    # ================================================================
    # ROW 3: PARALLELING + SWITCHGEAR (y=280)
    # ================================================================
    y3 = 280

    for gx in [100, 255, 395]:
        arrow_down(dwg, gx, y2 + 65, y3, "#22c55e" if gx != 395 else "#ef4444")

    box(dwg, 30, y3, 300, 50, "PARALLELING SWITCHGEAR + ATS\nLouisiana Cat Controls | Auto-Sync\nBoth G3520C parallel to common 480V AC bus",
        "Automatic load balancing",
        border="#22c55e", text_color="#86efac")

    box(dwg, 345, y3, 110, 50, "EMERGENCY\nATS\nDiesel Auto\nTransfer", "",
        border="#ef4444", text_color="#fca5a5")

    # Solar combiner
    arrow_down(dwg, 540, y2 + 65, y3, "#fbbf24")
    box(dwg, 480, y3, 110, 50, "SOLAR\nCOMBINER\nBOX\nString Fusing", "",
        border="#fbbf24", text_color="#fbbf24")

    # Grid backup feed
    wire(dwg, 685, y1 + 55, 685, y3 + 25, "#ef4444")
    wire(dwg, 620, y3 + 25, 685, y3 + 25, "#ef4444")
    dwg.add(dwg.text("BACKUP ONLY", insert=(625, y3 + 20), fill="#ef4444", font_size=7, font_family="Arial"))
    dwg.add(dwg.text("NOT PRIMARY", insert=(625, y3 + 30), fill="#ef4444", font_size=6, font_family="Arial"))

    # ================================================================
    # ROW 4: 480V AC BUS (y=375)
    # ================================================================
    y4 = 375
    for bx in [180, 400, 535]:
        arrow_down(dwg, bx, y3 + 50, y4, "#ff6b35")

    dwg.add(dwg.rect((30, y4 - 3), (680, 6), fill="#ff6b35", rx=2))
    dwg.add(dwg.text("480V AC DISTRIBUTION BUS", insert=(370, y4 - 10), text_anchor="middle",
                      fill="#ff6b35", font_size=10, font_family="Arial", font_weight="bold"))

    # ================================================================
    # ROW 5: RECTIFICATION (y=415)
    # ================================================================
    y5 = 415
    arrow_down(dwg, 150, y4 + 3, y5, "#ff6b35")
    arrow_down(dwg, 370, y4 + 3, y5, "#ff6b35")

    box(dwg, 60, y5, 200, 55, "EATON BEAM RUBIN DSX\nORV3 Sidecar | ABB SACE Infinitus\n480V AC -> 800V DC #1",
        "96%+ Efficiency",
        border="#8b5cf6", text_color="#c4b5fd")

    box(dwg, 290, y5, 200, 55, "EATON BEAM RUBIN DSX\nORV3 Sidecar | ABB SACE Infinitus\n480V AC -> 800V DC #2",
        "N+1 Redundant",
        border="#8b5cf6", text_color="#c4b5fd")

    # Solar DC-Direct bypass
    solar_bypass_x = 520
    pipe(dwg, [(535, y3 + 50), (535, y3 + 60), (solar_bypass_x + 50, y3 + 60),
               (solar_bypass_x + 50, y5)], "#fbbf24", 2)
    box(dwg, solar_bypass_x, y5, 170, 55, "DC-DC BUCK\nCONVERTER\n952V -> 800V Bus\n97% Efficiency",
        "Solar DC-Direct",
        border="#fbbf24", text_color="#fbbf24")

    # ================================================================
    # ROW 6: 800V DC BUS (y=515)
    # ================================================================
    y6 = 515
    for rx in [160, 390, 605]:
        arrow_down(dwg, rx, y5 + 55, y6, "#8b5cf6")

    dwg.add(dwg.rect((30, y6 - 3), (680, 6), fill="#8b5cf6", rx=2))
    dwg.add(dwg.text("800V DC MAIN DISTRIBUTION BUS — NVIDIA DSX REFERENCE", insert=(370, y6 - 10),
                      text_anchor="middle", fill="#8b5cf6", font_size=10, font_family="Arial", font_weight="bold"))

    # BESS on 800V bus
    bess_x = 30
    wire(dwg, bess_x + 50, y6 + 3, bess_x + 50, y6 + 15, "#8b5cf6")
    box(dwg, bess_x, y6 + 15, 100, 50, "Eaton xStorage\nBESS 600 kWh\n800V DC Native\nRide-through",
        "Ride-through + bridge",
        border=ACCENT, text_color="#93c5fd")

    # ================================================================
    # ROW 7-8: BUSWAY -> DELTA -> RACKS (Floor 1 + Floor 2)
    # ================================================================
    y7 = y6 + 25
    y7b = y7 + 35
    y7c = y7b + 35
    y8 = y7c + 35
    y9 = y8 + 30
    y10 = y9 + 40

    # Floor 1
    f1_positions = [(160, "F1 R1-2"), (310, "F1 R3-4")]
    for bx, label in f1_positions:
        arrow_down(dwg, bx + 40, y6 + 3, y7, "#8b5cf6")
        box(dwg, bx, y7, 80, 28, f"BUSWAY\n{label}", "",
            border="#8b5cf6", text_color="#c4b5fd", font=7)
        arrow_down(dwg, bx + 40, y7 + 28, y7b, "#8b5cf6")
        box(dwg, bx, y7b, 80, 28, "DELTA 660 kW\n480 kW BBU", "",
            border="#00bcd4", text_color="#00e5ff", font=7)
        arrow_down(dwg, bx + 40, y7b + 28, y7c, "#00bcd4")
        box(dwg, bx, y7c, 80, 28, "e-FUSE <3us\n90kW 800V->50V", "",
            border="#00bcd4", text_color="#00e5ff", font=7)
        arrow_down(dwg, bx + 40, y7c + 28, y8, "#00bcd4")
        box(dwg, bx + 5, y8, 70, 24, "TI GaN + Infineon\nCoolGaN 800V->6V", "",
            border="#76b900", text_color="#76b900", font=7)
        arrow_down(dwg, bx + 40, y8 + 24, y9, "#76b900")

    box(dwg, 150, y9, 100, 45, "FLOOR 1\nRACKS 1-4\n520 kW", "4x NVL72 | Liquid Cooled",
        color="#111a00", border="#76b900", text_color="#76b900", font=9)
    box(dwg, 300, y9, 100, 45, "FLOOR 1\n(continued)\n288 GPUs", "System 1 | CDU Pair",
        color="#111a00", border="#76b900", text_color="#76b900", font=9)

    # Floor 2
    f2_positions = [(460, "F2 R5-6"), (600, "F2 R7-8")]
    for bx, label in f2_positions:
        arrow_down(dwg, bx + 40, y6 + 3, y7, "#8b5cf6")
        box(dwg, bx, y7, 80, 28, f"BUSWAY\n{label}", "",
            border="#8b5cf6", text_color="#c4b5fd", font=7)
        arrow_down(dwg, bx + 40, y7 + 28, y7b, "#8b5cf6")
        box(dwg, bx, y7b, 80, 28, "DELTA 660 kW\n480 kW BBU", "",
            border="#00bcd4", text_color="#00e5ff", font=7)
        arrow_down(dwg, bx + 40, y7b + 28, y7c, "#00bcd4")
        box(dwg, bx, y7c, 80, 28, "e-FUSE <3us\n90kW 800V->50V", "",
            border="#00bcd4", text_color="#00e5ff", font=7)
        arrow_down(dwg, bx + 40, y7c + 28, y8, "#00bcd4")
        box(dwg, bx + 5, y8, 70, 24, "TI GaN + Infineon\nCoolGaN 800V->6V", "",
            border="#76b900", text_color="#76b900", font=7)
        arrow_down(dwg, bx + 40, y8 + 24, y9, "#76b900")

    box(dwg, 450, y9, 100, 45, "FLOOR 2\nRACKS 5-8\n520 kW", "4x NVL72 | Liquid Cooled",
        color="#111a00", border="#76b900", text_color="#76b900", font=9)
    box(dwg, 590, y9, 100, 45, "FLOOR 2\n(continued)\n288 GPUs", "System 2 | CDU Pair",
        color="#111a00", border="#76b900", text_color="#76b900", font=9)

    # ================================================================
    # RIGHT SIDE: 4-LAYER HIERARCHY
    # ================================================================
    hx = 780
    hy = 75

    dwg.add(dwg.rect((hx, hy), (590, 960), rx=8, fill="#111318", stroke="#1e2230", stroke_width=1))
    dwg.add(dwg.text("4-LAYER POWER HIERARCHY — MARLIE I", insert=(hx + 295, hy + 20), text_anchor="middle",
                      fill="#f0f2f5", font_size=12, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("(DIFFERENT from Trappeys — Grid is BACKUP here, not sell-back)",
                      insert=(hx + 295, hy + 35), text_anchor="middle",
                      fill="#ef4444", font_size=9, font_family="Arial", font_weight="bold"))

    layers = [
        {
            "num": "1", "name": "SOLAR", "color": "#fbbf24",
            "role": "PRIMARY OFFSET",
            "details": [
                "300 kW rooftop on 24x40 building",
                "First Solar Series 7 TR1 (550W) panels",
                "DC-Direct to 800V bus (97% eff)",
                "Small scale but meaningful offset (~24%)",
                "Eaton xStorage BESS (600 kWh) battery bridge",
                "Made 30 miles away in New Iberia, LA",
            ]
        },
        {
            "num": "2", "name": "NATURAL GAS", "color": "#22c55e",
            "role": "BACKBONE — ALWAYS RUNNING",
            "details": [
                "Caterpillar G3512H generators (1.03 MW each)",
                "2 units: 2.06 MW total (N+1 redundant)",
                "ATMOS Energy gas on property",
                "Henry Hub 40 miles — cheapest in USA",
                "480V AC output to Eaton Beam Rubin DSX rectifiers",
                "Carries FULL load 24/7/365",
                "~60% load per unit (1.24 MW on 2.06 MW)",
            ]
        },
        {
            "num": "3", "name": "DIESEL", "color": "#ef4444",
            "role": "EMERGENCY ONLY",
            "details": [
                "Diesel emergency generator (250 kW)",
                "On-site fuel storage (2,000 gal)",
                "Auto-start on dual gas failure",
                "Pipeline-independent fuel source",
                "Bridges until gas restored",
                "Required for NVIDIA certification",
            ]
        },
        {
            "num": "4", "name": "GRID (LUS + SLEMCO)", "color": "#ef4444",
            "role": "BACKUP ONLY — NOT SELL-BACK",
            "details": [
                "Lafayette Utilities System (LUS)",
                "SLEMCO dual feed available",
                "3-phase power confirmed on site",
                "BACKUP power source (unlike Trappeys)",
                "NOT sell-back — grid supports building",
                "Cloudy day + gas down = grid bridges",
                "Industrial corridor = reliable service",
            ]
        },
    ]

    ly = hy + 50
    for layer in layers:
        dwg.add(dwg.rect((hx + 15, ly), (560, 25), rx=4, fill="#111318",
                          stroke=layer["color"], stroke_width=1))
        dwg.add(dwg.text(f"LAYER {layer['num']}: {layer['name']}", insert=(hx + 25, ly + 16),
                          fill=layer["color"], font_size=11, font_family="Arial", font_weight="bold"))
        dwg.add(dwg.text(layer["role"], insert=(hx + 570, ly + 16), text_anchor="end",
                          fill=layer["color"], font_size=8, font_family="Arial", font_weight="bold"))

        for i, detail in enumerate(layer["details"]):
            dwg.add(dwg.text(f"  {detail}", insert=(hx + 30, ly + 38 + i * 13),
                              fill="#9ca3af", font_size=8, font_family="Arial"))

        ly += 30 + len(layer["details"]) * 13 + 15

    # KEY DIFFERENCE callout
    kd_y = ly + 10
    dwg.add(dwg.rect((hx + 15, kd_y), (560, 60), rx=6, fill="#1a0a0a", stroke="#ef4444", stroke_width=1.5))
    dwg.add(dwg.text("KEY DIFFERENCE: MARLIE I vs TRAPPEYS/WILLOW GLEN", insert=(hx + 295, kd_y + 18),
                      text_anchor="middle", fill="#ef4444", font_size=10, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("Trappeys/Willow Glen: Grid = SELL-BACK only (Layer 4 revenue)",
                      insert=(hx + 30, kd_y + 35), fill="#fca5a5", font_size=8, font_family="Arial"))
    dwg.add(dwg.text("MARLIE I: Grid = BACKUP power (Layer 4 safety net) — smaller facility, grid supports ops",
                      insert=(hx + 30, kd_y + 50), fill="#fca5a5", font_size=8, font_family="Arial"))

    # ================================================================
    # BOTTOM: STATS
    # ================================================================
    sy = 1060
    dwg.add(dwg.rect((30, sy), (1340, 40), rx=6, fill="#111318", stroke="#1e2230"))
    stats = [
        ("GAS GENERATION", "2.06 MW (N+1)"),
        ("SOLAR", "300 kW Rooftop"),
        ("IT LOAD", "1,040 kW"),
        ("TOTAL FACILITY", "~1,240 kW"),
        ("GENSET LOAD", "~60% each"),
        ("RACKS", "8 NVL72"),
        ("GPUs", "576"),
    ]
    sx = 55
    for label, value in stats:
        dwg.add(dwg.text(label, insert=(sx, sy + 14), fill="#6b7280",
                          font_size=7, font_family="Arial", font_weight="bold"))
        dwg.add(dwg.text(value, insert=(sx, sy + 28), fill=ACCENT,
                          font_size=10, font_family="Arial", font_weight="bold"))
        sx += 190

    # NOTES
    ny = 1115
    notes = [
        "1. Gas is BACKBONE (Layer 2) — always running, carries full facility load. Solar offsets but does not replace gas.",
        "2. Grid (LUS + SLEMCO) is BACKUP (Layer 4) — different from Trappeys where grid is sell-back only.",
        "3. DUAL POWER STACK: Eaton (facility) + Delta (rack). Delta 660 kW Rack (6x 110 kW, 480 kW BBU). e-Fuse SiC <3 us. 90 kW DC/DC 800V->50V MGX.",
        "4. N+1 generator redundancy: 2x Caterpillar G3512H (1.03 MW) for 1.24 MW load. Either unit offline = zero impact.",
        "5. Solar DC-Direct: First Solar Series 7 TR1, buck to 800V bus at 97% eff. Eaton BESS 600 kWh ride-through.",
        "6. All equipment American-made. Complete power chain: generator -> Eaton rectifier -> Delta rack power -> NVIDIA GPU.",
    ]
    for i, note in enumerate(notes):
        dwg.add(dwg.text(note, insert=(35, ny + i * 12), fill="#4b5563",
                          font_size=7, font_family="Arial"))

    dwg.save()
    print(f"Saved: {OUT}")


if __name__ == "__main__":
    import os
    os.makedirs("adc3k-deploy/marlie/blueprints", exist_ok=True)
    build()
