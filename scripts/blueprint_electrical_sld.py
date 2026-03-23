"""
Willow Glen Tiger Compute Campus — Electrical Single-Line Diagram
500kV substation → 800V DC → GPU rack
SVG output — web-ready + print-quality
"""
import svgwrite

W, H = 1400, 1000
OUT = "adc3k-deploy/blueprints/electrical-sld.svg"


def box(dwg, x, y, w, h, label, sublabel="", color="#1a1a2e", border="#3b82f6", text_color="#e0e0e0", font=11):
    """Draw a labeled box."""
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
    """Draw a horizontal bus bar."""
    dwg.add(dwg.rect((x, y - 3), (w, 6), fill=color, rx=2))
    dwg.add(dwg.text(label, insert=(x + w / 2, y - 8), text_anchor="middle",
                      fill=color, font_size=10, font_family="Arial", font_weight="bold"))


def wire(dwg, x1, y1, x2, y2, color="#555"):
    """Draw a wire/connection."""
    dwg.add(dwg.line((x1, y1), (x2, y2), stroke=color, stroke_width=1.5))


def arrow_down(dwg, x, y1, y2, color="#555"):
    """Wire with arrow pointing down."""
    wire(dwg, x, y1, x, y2, color)
    dwg.add(dwg.polygon([(x - 4, y2 - 6), (x + 4, y2 - 6), (x, y2)], fill=color))


def build():
    dwg = svgwrite.Drawing(OUT, size=(f"{W}px", f"{H}px"), viewBox=f"0 0 {W} {H}")
    dwg.add(dwg.rect((0, 0), (W, H), fill="#0a0b0f"))

    # ── TITLE BLOCK ──
    dwg.add(dwg.text("TIGER COMPUTE CAMPUS — WILLOW GLEN, ST. GABRIEL, LA",
                      insert=(W / 2, 24), text_anchor="middle", fill="#f0f2f5",
                      font_size=16, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("ELECTRICAL SINGLE-LINE DIAGRAM | 800V DC NATIVE ARCHITECTURE | NVIDIA DSX REFERENCE DESIGN",
                      insert=(W / 2, 40), text_anchor="middle", fill="#3b82f6",
                      font_size=10, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("Sheet E-001 | MVP Design Intent | 2026-03-22 | NOT FOR CONSTRUCTION",
                      insert=(W / 2, 54), text_anchor="middle", fill="#6b7280",
                      font_size=9, font_family="Arial"))

    # ════════════════════════════════════════════
    # ROW 1: SOURCES (y=70)
    # ════════════════════════════════════════════
    y1 = 75

    # 500kV Substation
    box(dwg, 20, y1, 160, 55,
        "ENTERGY 500kV\nSUBSTATION",
        "On-site | Willow Glen–Waterford Line",
        color="#1a1a2e", border="#ef4444", text_color="#ef4444")

    # 230kV Substation
    box(dwg, 200, y1, 160, 55,
        "ENTERGY 230kV\nSUBSTATION",
        "On-site | Willow Glen–Conway Line",
        color="#1a1a2e", border="#ef4444", text_color="#ef4444")

    # Cat CG260 Generators
    gen_colors = {"color": "#1a2e1a", "border": "#22c55e", "text_color": "#22c55e"}
    box(dwg, 520, y1, 120, 55, "CAT CG260-16\n#1 — 2.8 MW", "Natural Gas | H2-Ready 25%", **gen_colors)
    box(dwg, 660, y1, 120, 55, "CAT CG260-16\n#2 — 2.8 MW", "Natural Gas | H2-Ready 25%", **gen_colors)
    box(dwg, 800, y1, 120, 55, "CAT CG260-16\n#3 (N+1)", "Redundant | Maintenance Spare", **gen_colors)

    # First Solar
    box(dwg, 980, y1, 140, 55, "FIRST SOLAR\nGround Mount", "Series 7 TR1 | 5+ MW Phase 1",
        color="#1a1a2e", border="#fbbf24", text_color="#fbbf24")

    # Diesel Emergency
    box(dwg, 1180, y1, 120, 55, "DIESEL GENSET\nEmergency", "Layer 3 | Pipeline-Independent",
        color="#2e1a1a", border="#ef4444", text_color="#ef4444")

    # ════════════════════════════════════════════
    # ROW 2: STEP-DOWN + SWITCHGEAR (y=175)
    # ════════════════════════════════════════════
    y2 = 180

    # Wires down from sources
    arrow_down(dwg, 100, y1 + 55, y2, "#ef4444")
    arrow_down(dwg, 280, y1 + 55, y2, "#ef4444")

    # Main transformer
    box(dwg, 80, y2, 240, 50, "MAIN STEP-DOWN TRANSFORMERS\n500kV/230kV → 13.8kV AC",
        "Oil-filled | Entergy-owned | Bidirectional for sell-back",
        border="#ef4444")

    # Generator wires down
    for gx in [580, 720, 860]:
        arrow_down(dwg, gx, y1 + 55, y2, "#22c55e")

    # Paralleling switchgear
    box(dwg, 500, y2, 500, 50, "PARALLELING SWITCHGEAR + ATS\nLouisiana Cat Switchgear & Paralleling Controls",
        "Auto-sync generators to bus | Auto-transfer on loss | Load sharing",
        border="#22c55e")

    # Diesel wire
    arrow_down(dwg, 1240, y1 + 55, y2, "#ef4444")
    box(dwg, 1160, y2, 160, 50, "EMERGENCY ATS\nDiesel Transfer", "Auto-start on dual failure",
        border="#ef4444")

    # ════════════════════════════════════════════
    # ROW 3: 13.8kV AC BUS (y=270)
    # ════════════════════════════════════════════
    y3 = 275
    arrow_down(dwg, 200, y2 + 50, y3, "#ef4444")
    arrow_down(dwg, 750, y2 + 50, y3, "#22c55e")
    arrow_down(dwg, 1240, y2 + 50, y3, "#ef4444")

    bus(dwg, 30, y3, 1290, "13.8kV AC DISTRIBUTION BUS", "#ff6b35")

    # ════════════════════════════════════════════
    # ROW 4: RECTIFICATION (y=310)
    # ════════════════════════════════════════════
    y4 = 320

    # Main rectifier bank
    arrow_down(dwg, 400, y3 + 3, y4, "#ff6b35")
    arrow_down(dwg, 700, y3 + 3, y4, "#ff6b35")
    arrow_down(dwg, 1000, y3 + 3, y4, "#ff6b35")

    box(dwg, 300, y4, 230, 55, "AC/DC RECTIFIER #1\n13.8kV AC → 800V DC",
        "Eaton Beam Rubin DSX | 96%+ Efficiency",
        border="#8b5cf6", text_color="#c4b5fd")
    box(dwg, 600, y4, 230, 55, "AC/DC RECTIFIER #2\n13.8kV AC → 800V DC",
        "Eaton Beam Rubin DSX | 96%+ Efficiency",
        border="#8b5cf6", text_color="#c4b5fd")
    box(dwg, 900, y4, 230, 55, "AC/DC RECTIFIER #3\n13.8kV AC → 800V DC",
        "Eaton Beam Rubin DSX | N+1 Redundant",
        border="#8b5cf6", text_color="#c4b5fd")

    # Solar DC-Direct bypass
    solar_dc_x = 1130
    wire(dwg, 1050, y1 + 55, 1050, y1 + 70, "#fbbf24")
    wire(dwg, 1050, y1 + 70, solar_dc_x, y1 + 70, "#fbbf24")
    wire(dwg, solar_dc_x, y1 + 70, solar_dc_x, y4, "#fbbf24")
    box(dwg, solar_dc_x - 55, y4, 130, 55, "DC-DC CONVERTER\n952V → 800V DC",
        "Buck converter | 97% Eff | Bypasses AC",
        border="#fbbf24", text_color="#fbbf24")

    # ════════════════════════════════════════════
    # ROW 5: 800V DC BUS (y=420)
    # ════════════════════════════════════════════
    y5 = 425
    for rx in [415, 715, 1015, solar_dc_x]:
        arrow_down(dwg, rx, y4 + 55, y5, "#8b5cf6")

    bus(dwg, 30, y5, 1290, "800V DC DISTRIBUTION BUS — NVIDIA DSX REFERENCE ARCHITECTURE", "#8b5cf6")

    # ── BESS on 800V bus ──
    bess_x = 40
    wire(dwg, bess_x + 60, y5 + 3, bess_x + 60, y5 + 20, "#8b5cf6")
    box(dwg, bess_x, y5 + 20, 120, 50, "EATON xStorage\nBESS", "800V DC | Grid Buffer\nRide-through | Peak Shaving",
        border="#3b82f6", text_color="#93c5fd")

    # Grid sell-back indicator
    wire(dwg, 100, y3, 100, y3 - 15, "#ef4444")
    dwg.add(dwg.text("↑ SELL-BACK TO ENTERGY (Layer 4)", insert=(110, y3 - 8),
                      fill="#ef4444", font_size=8, font_family="Arial"))

    # ════════════════════════════════════════════
    # ROW 6: EATON BUSWAY (y=475)
    # ════════════════════════════════════════════
    y6 = 480

    busway_positions = [200, 420, 640, 860, 1080]
    for bx in busway_positions:
        arrow_down(dwg, bx + 55, y5 + 3, y6, "#8b5cf6")
        box(dwg, bx, y6, 110, 40, "EATON BUSWAY\n800V DC", "",
            border="#8b5cf6", text_color="#c4b5fd", font=9)

    # ════════════════════════════════════════════
    # ROW 7: RACK PDUs (y=555)
    # ════════════════════════════════════════════
    y7 = 555
    for bx in busway_positions:
        arrow_down(dwg, bx + 55, y6 + 40, y7, "#8b5cf6")
        box(dwg, bx, y7, 110, 40, "RACK PDU\n800V DC Input", "",
            border="#8b5cf6", text_color="#c4b5fd", font=9)

    # ════════════════════════════════════════════
    # ROW 8: LLC CONVERTERS (y=630)
    # ════════════════════════════════════════════
    y8 = 630
    for bx in busway_positions:
        arrow_down(dwg, bx + 55, y7 + 40, y8, "#8b5cf6")
        box(dwg, bx, y8, 110, 40, "64:1 LLC DC-DC\n800V → 12.5V", "99%+ Efficiency",
            border="#76b900", text_color="#76b900", font=9)

    # ════════════════════════════════════════════
    # ROW 9: GPU RACKS (y=710)
    # ════════════════════════════════════════════
    y9 = 710
    rack_labels = [
        "NVIDIA NVL72\nRACKS 1-7\n130 kW each\n0.91 MW",
        "NVIDIA NVL72\nRACKS 8-14\n130 kW each\n0.91 MW",
        "NVIDIA NVL72\nRACKS 15-21\n130 kW each\n0.91 MW",
        "NVIDIA NVL72\nRACKS 22-28\n130 kW each\n0.91 MW",
        "NVIDIA NVL72\nRACKS 29-36\n130 kW each\n1.04 MW",
    ]
    for bx, label in zip(busway_positions, rack_labels):
        arrow_down(dwg, bx + 55, y8 + 40, y9, "#76b900")
        box(dwg, bx, y9, 110, 60, label, "Vera Rubin | Liquid Cooled",
            color="#111a00", border="#76b900", text_color="#76b900", font=9)

    # ════════════════════════════════════════════
    # PHASE 1 SUMMARY BAR
    # ════════════════════════════════════════════
    sy = 800
    dwg.add(dwg.rect((30, sy), (1340, 45), rx=6, fill="#111318", stroke="#1e2230", stroke_width=1))
    stats = [
        ("PHASE 1 IT LOAD", "4.68 MW"),
        ("TOTAL FACILITY", "~6.5 MW"),
        ("GENERATORS", "3x CG260 = 8.4 MW (N+1)"),
        ("SOLAR", "5+ MW (DC-Direct)"),
        ("RACKS", "36 NVL72 (2,592 GPUs)"),
        ("ARCHITECTURE", "800V DC Native"),
    ]
    sx = 60
    for label, value in stats:
        dwg.add(dwg.text(label, insert=(sx, sy + 16), fill="#6b7280",
                          font_size=8, font_family="Arial", font_weight="bold"))
        dwg.add(dwg.text(value, insert=(sx, sy + 30), fill="#76b900",
                          font_size=11, font_family="Arial", font_weight="bold"))
        sx += 220

    # ════════════════════════════════════════════
    # NOTES
    # ════════════════════════════════════════════
    ny = 860
    notes = [
        "1. 500kV and 230kV substations are EXISTING Entergy assets on-site — LIVE and accepting new interconnections",
        "2. Cat CG260-16 generators are hydrogen-ready (25% blend) — future-proof for green fuel transition",
        "3. First Solar arrays connect DC-direct to 800V bus at 97% efficiency, bypassing AC conversion entirely",
        "4. 800V DC per NVIDIA DSX Reference Design — 85% more power through same copper vs 415V AC",
        "5. 64:1 LLC resonant converters: 800V DC to 12.5V at GPU die — 99%+ conversion efficiency",
        "6. Eaton Beam Rubin DSX: complete grid-to-chip platform (rectification + distribution + rack PDU)",
        "7. N+1 generator redundancy — any single unit offline for maintenance without load reduction",
        "8. Grid is SELL-BACK ONLY (Layer 4) — excess power returns to Entergy, never consumed from grid",
        "9. BESS provides ride-through for transfer events + peak shaving for GPU training spike loads",
    ]
    for i, note in enumerate(notes):
        dwg.add(dwg.text(note, insert=(35, ny + i * 13), fill="#4b5563",
                          font_size=8, font_family="Arial"))

    # 4-Layer legend
    ly = ny + len(notes) * 13 + 10
    layers = [
        ("LAYER 1: SOLAR", "#fbbf24", "Primary Offset"),
        ("LAYER 2: NATURAL GAS", "#22c55e", "Backbone — 24/7"),
        ("LAYER 3: DIESEL", "#ef4444", "Emergency Only"),
        ("LAYER 4: GRID", "#ef4444", "Sell-Back Only"),
    ]
    lx = 35
    for label, color, desc in layers:
        dwg.add(dwg.rect((lx, ly - 8), (8, 8), fill=color))
        dwg.add(dwg.text(f"{label} — {desc}", insert=(lx + 14, ly), fill="#6b7280",
                          font_size=8, font_family="Arial", font_weight="bold"))
        lx += 300

    dwg.save()
    print(f"Saved: {OUT}")


if __name__ == "__main__":
    import os
    os.makedirs("adc3k-deploy/blueprints", exist_ok=True)
    build()
