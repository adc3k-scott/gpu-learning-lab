"""
MARLIE I — Lafayette AI Factory & Command Center
Electrical Single-Line Diagram
G3520C generators -> Eaton Beam Rubin DSX -> 800V DC bus -> rack PDUs -> 64:1 LLC -> GPU
"""
import svgwrite

W, H = 1400, 1000
OUT = "adc3k-deploy/blueprints/marlie-electrical-sld.svg"

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
    dwg.add(dwg.text("MARLIE I — LAFAYETTE AI FACTORY & COMMAND CENTER",
                      insert=(W / 2, 24), text_anchor="middle", fill="#f0f2f5",
                      font_size=16, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("ELECTRICAL SINGLE-LINE DIAGRAM | 800V DC NATIVE | EATON BEAM RUBIN DSX | 1,040 kW IT LOAD",
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
    box(dwg, 30, y1, 140, 50,
        "ATMOS ENERGY\nNatural Gas", "On-property | Henry Hub 40 mi",
        color="#0a1a0a", border="#22c55e", text_color="#22c55e")

    # Cat G3520C #1
    box(dwg, 200, y1, 130, 50, "CAT G3520C #1\n1.5 MW | 480V AC", "Natural Gas | Layer 2",
        color="#0a1a0a", border="#22c55e", text_color="#22c55e")
    box(dwg, 350, y1, 130, 50, "CAT G3520C #2\n1.5 MW | 480V AC", "N+1 Redundant",
        color="#0a1a0a", border="#22c55e", text_color="#22c55e")

    # Solar Rooftop
    box(dwg, 510, y1, 140, 50, "SOLAR ROOFTOP\n300 kW", "24x40 roof | DC-Direct",
        color="#1a1a00", border="#fbbf24", text_color="#fbbf24")

    # Diesel Emergency
    box(dwg, 680, y1, 120, 50, "DIESEL GENSET\nEmergency", "Layer 3 | Pipeline-Independent",
        color="#2e1a1a", border="#ef4444", text_color="#ef4444")

    # LUS Grid (backup)
    box(dwg, 830, y1, 120, 50, "LUS GRID\nBACKUP ONLY", "Layer 4 | Dual Feed Available",
        color="#1a0a0a", border="#ef4444", text_color="#ef4444")

    # Eaton BESS
    box(dwg, 980, y1, 120, 50, "EATON xStorage\nBESS 600 kWh", "800V DC | Ride-through",
        border=ACCENT, text_color="#93c5fd")

    # ================================================================
    # ROW 2: PARALLELING / SWITCHGEAR (y=170)
    # ================================================================
    y2 = 170
    arrow_down(dwg, 100, y1 + 50, y2, "#22c55e")
    arrow_down(dwg, 265, y1 + 50, y2, "#22c55e")
    arrow_down(dwg, 415, y1 + 50, y2, "#22c55e")
    arrow_down(dwg, 740, y1 + 50, y2, "#ef4444")

    box(dwg, 30, y2, 240, 45,
        "PARALLELING SWITCHGEAR + ATS\n480V AC | Auto-Sync | Load Sharing",
        "Louisiana Cat controls",
        border="#22c55e")

    box(dwg, 290, y2, 170, 45,
        "MAIN BREAKER + METERING\n480V AC | Protection Relays", "",
        border="#ff6b35", text_color="#ff6b35")

    box(dwg, 660, y2, 150, 45,
        "EMERGENCY ATS\nDiesel Auto-Transfer", "Auto-start on gas failure",
        border="#ef4444")

    # LUS backup feed
    wire(dwg, 890, y1 + 50, 890, y2 + 22, "#ef4444")
    wire(dwg, 810, y2 + 22, 890, y2 + 22, "#ef4444")
    dwg.add(dwg.text("BACKUP FEED", insert=(820, y2 + 18), fill="#ef4444", font_size=7, font_family="Arial"))

    # ================================================================
    # ROW 3: 480V AC BUS (y=255)
    # ================================================================
    y3 = 255
    arrow_down(dwg, 150, y2 + 45, y3, "#22c55e")
    arrow_down(dwg, 375, y2 + 45, y3, "#ff6b35")
    arrow_down(dwg, 735, y2 + 45, y3, "#ef4444")

    bus(dwg, 30, y3, 840, "480V AC DISTRIBUTION BUS", "#ff6b35")

    # ================================================================
    # ROW 4: RECTIFICATION (y=300)
    # ================================================================
    y4 = 300
    rect_positions = [150, 400, 650]
    for rx in rect_positions:
        arrow_down(dwg, rx, y3 + 3, y4, "#ff6b35")

    box(dwg, 60, y4, 190, 50, "EATON BEAM RUBIN DSX\n480V AC -> 800V DC\nRectifier #1",
        "96%+ Efficiency",
        border="#8b5cf6", text_color="#c4b5fd")

    box(dwg, 310, y4, 190, 50, "EATON BEAM RUBIN DSX\n480V AC -> 800V DC\nRectifier #2",
        "N+1 Redundant",
        border="#8b5cf6", text_color="#c4b5fd")

    # Solar DC-Direct bypass
    solar_dc_x = 560
    wire(dwg, 580, y1 + 50, 580, y1 + 65, "#fbbf24")
    wire(dwg, 580, y1 + 65, solar_dc_x + 70, y1 + 65, "#fbbf24")
    wire(dwg, solar_dc_x + 70, y1 + 65, solar_dc_x + 70, y4, "#fbbf24")
    box(dwg, solar_dc_x, y4, 190, 50, "DC-DC BUCK CONVERTER\n952V String -> 800V DC",
        "Solar DC-Direct | 97% Eff",
        border="#fbbf24", text_color="#fbbf24")

    # Diesel to 480V
    box(dwg, 770, y4, 100, 50, "DIESEL\nFEED\nTo 480V Bus", "",
        border="#ef4444", text_color="#fca5a5", font=9)
    arrow_down(dwg, 820, y3 + 3, y4, "#ef4444")

    # ================================================================
    # ROW 5: 800V DC BUS (y=400)
    # ================================================================
    y5 = 400
    for rx in [155, 405, 655]:
        arrow_down(dwg, rx, y4 + 50, y5, "#8b5cf6")

    bus(dwg, 30, y5, 840, "800V DC DISTRIBUTION BUS — NVIDIA DSX REFERENCE ARCHITECTURE", "#8b5cf6")

    # BESS connection
    wire(dwg, 1040, y1 + 50, 1040, y5, ACCENT)
    dwg.add(dwg.text("BESS on", insert=(1050, y5 - 20), fill="#93c5fd", font_size=7, font_family="Arial"))
    dwg.add(dwg.text("800V DC", insert=(1050, y5 - 10), fill="#93c5fd", font_size=7, font_family="Arial"))

    # ================================================================
    # ROW 6-9: BUSWAY -> PDU -> LLC -> RACKS (Split: Floor 1 + Floor 2)
    # ================================================================
    # FLOOR 1 (left side) — 4 racks
    f1_label_y = y5 + 20
    dwg.add(dwg.text("FLOOR 1 (DOWNSTAIRS) — SYSTEM 1", insert=(130, f1_label_y),
                      text_anchor="middle", fill=ACCENT, font_size=9, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("4 NVL72 RACKS | 288 GPUs | 520 kW", insert=(130, f1_label_y + 12),
                      text_anchor="middle", fill="#93c5fd", font_size=8, font_family="Arial"))

    y6 = y5 + 50
    y7 = y6 + 40
    y8 = y7 + 40
    y9 = y8 + 40

    f1_positions = [50, 155, 260, 365]
    for bx in f1_positions:
        arrow_down(dwg, bx + 40, y5 + 3, y6, "#8b5cf6")
        box(dwg, bx, y6, 80, 30, "BUSWAY\n800V DC", "",
            border="#8b5cf6", text_color="#c4b5fd", font=8)
        arrow_down(dwg, bx + 40, y6 + 30, y7, "#8b5cf6")
        box(dwg, bx, y7, 80, 30, "RACK PDU\n800V In", "",
            border="#8b5cf6", text_color="#c4b5fd", font=8)
        arrow_down(dwg, bx + 40, y7 + 30, y8, "#76b900")
        box(dwg, bx, y8, 80, 30, "64:1 LLC\n800V->12.5V", "99%+ eff",
            border="#76b900", text_color="#76b900", font=8)
        arrow_down(dwg, bx + 40, y8 + 30, y9, "#76b900")

    f1_rack_labels = ["NVL72 R1\n130 kW", "NVL72 R2\n130 kW", "NVL72 R3\n130 kW", "NVL72 R4\n130 kW"]
    for bx, label in zip(f1_positions, f1_rack_labels):
        box(dwg, bx, y9, 80, 45, label, "Liquid Cooled",
            color="#111a00", border="#76b900", text_color="#76b900", font=9)

    # FLOOR 2 (right side) — 4 racks
    f2_label_y = y5 + 20
    f2_offset = 520
    dwg.add(dwg.text("FLOOR 2 (UPSTAIRS) — SYSTEM 2", insert=(f2_offset + 210, f2_label_y),
                      text_anchor="middle", fill=ACCENT, font_size=9, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("4 NVL72 RACKS | 288 GPUs | 520 kW", insert=(f2_offset + 210, f2_label_y + 12),
                      text_anchor="middle", fill="#93c5fd", font_size=8, font_family="Arial"))

    f2_positions = [f2_offset + 30, f2_offset + 135, f2_offset + 240, f2_offset + 345]
    for bx in f2_positions:
        arrow_down(dwg, bx + 40, y5 + 3, y6, "#8b5cf6")
        box(dwg, bx, y6, 80, 30, "BUSWAY\n800V DC", "",
            border="#8b5cf6", text_color="#c4b5fd", font=8)
        arrow_down(dwg, bx + 40, y6 + 30, y7, "#8b5cf6")
        box(dwg, bx, y7, 80, 30, "RACK PDU\n800V In", "",
            border="#8b5cf6", text_color="#c4b5fd", font=8)
        arrow_down(dwg, bx + 40, y7 + 30, y8, "#76b900")
        box(dwg, bx, y8, 80, 30, "64:1 LLC\n800V->12.5V", "99%+ eff",
            border="#76b900", text_color="#76b900", font=8)
        arrow_down(dwg, bx + 40, y8 + 30, y9, "#76b900")

    f2_rack_labels = ["NVL72 R5\n130 kW", "NVL72 R6\n130 kW", "NVL72 R7\n130 kW", "NVL72 R8\n130 kW"]
    for bx, label in zip(f2_positions, f2_rack_labels):
        box(dwg, bx, y9, 80, 45, label, "Liquid Cooled",
            color="#111a00", border="#76b900", text_color="#76b900", font=9)

    # Divider line between floors
    div_x = f2_offset + 10
    dwg.add(dwg.line((div_x, y5 + 15), (div_x, y9 + 50), stroke="#333", stroke_width=1,
                      stroke_dasharray="8,4"))

    # ================================================================
    # SUMMARY BAR
    # ================================================================
    sy = 780
    dwg.add(dwg.rect((30, sy), (1340, 45), rx=6, fill="#111318", stroke="#1e2230"))
    stats = [
        ("FLOOR 1 IT", "520 kW (4 racks)"),
        ("FLOOR 2 IT", "520 kW (4 racks)"),
        ("TOTAL IT", "1,040 kW (8 racks)"),
        ("OVERHEAD", "~200 kW"),
        ("TOTAL DRAW", "~1,240 kW"),
        ("GEN CAPACITY", "3,000 kW (N+1)"),
    ]
    sx = 55
    for label, value in stats:
        dwg.add(dwg.text(label, insert=(sx, sy + 16), fill="#6b7280",
                          font_size=8, font_family="Arial", font_weight="bold"))
        dwg.add(dwg.text(value, insert=(sx, sy + 30), fill=ACCENT,
                          font_size=11, font_family="Arial", font_weight="bold"))
        sx += 220

    # ================================================================
    # NOTES
    # ================================================================
    ny = 840
    notes = [
        "1. 2x Cat G3520C natural gas generators: 1.5 MW each, 480V AC output — ATMOS gas on property, Henry Hub 40 mi",
        "2. N+1 redundancy: each genset at ~41% load (1,240 kW on 3,000 kW capacity)",
        "3. Eaton Beam Rubin DSX rectifiers convert 480V AC to 800V DC per NVIDIA DSX Reference Design",
        "4. 300 kW rooftop solar DC-Direct to 800V bus via buck converter at 97% efficiency",
        "5. 64:1 LLC resonant converters: 800V DC to 12.5V at GPU die — 99%+ efficiency",
        "6. LUS grid is BACKUP ONLY (Layer 4) — dual feed (LUS + SLEMCO) available for redundancy",
        "7. BESS 600 kWh on 800V DC bus — ride-through for transfer events + battery bridge",
        "8. Diesel genset (Layer 3) provides pipeline-independent backup, auto-start on gas failure",
        "9. 8 NVL72 racks across 2 floors: 576 GPUs total, 1,040 kW IT load, 1 CDU pair per floor",
    ]
    for i, note in enumerate(notes):
        dwg.add(dwg.text(note, insert=(35, ny + i * 13), fill="#4b5563",
                          font_size=8, font_family="Arial"))

    # 4-Layer legend at bottom
    ly = ny + len(notes) * 13 + 10
    layers = [
        ("LAYER 1: SOLAR", "#fbbf24", "Primary Offset — 300 kW rooftop"),
        ("LAYER 2: NATURAL GAS", "#22c55e", "Backbone — 2x G3520C 24/7"),
        ("LAYER 3: DIESEL", "#ef4444", "Emergency Only"),
        ("LAYER 4: GRID (LUS)", "#ef4444", "Backup Only — dual feed"),
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
