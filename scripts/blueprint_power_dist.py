"""
Willow Glen Tiger Compute Campus — Power Distribution Schematic
Detailed view: Generators → Switchgear → ATS → Rectifiers → Busway → PDU → Rack
Includes fuel system, BESS, and 4-layer hierarchy
SVG output
"""
import svgwrite

W, H = 1400, 1050
OUT = "adc3k-deploy/blueprints/power-distribution.svg"


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

    # ── TITLE ──
    dwg.add(dwg.text("TIGER COMPUTE CAMPUS — WILLOW GLEN, ST. GABRIEL, LA",
                      insert=(W / 2, 24), text_anchor="middle", fill="#f0f2f5",
                      font_size=16, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("POWER DISTRIBUTION SCHEMATIC | FUEL TO CHIP | 4-LAYER POWER HIERARCHY",
                      insert=(W / 2, 40), text_anchor="middle", fill="#22c55e",
                      font_size=10, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("Sheet P-001 | MVP Design Intent | 2026-03-22 | NOT FOR CONSTRUCTION",
                      insert=(W / 2, 54), text_anchor="middle", fill="#6b7280",
                      font_size=9, font_family="Arial"))

    # ════════════════════════════════════════════
    # ROW 1: FUEL SOURCES (y=70)
    # ════════════════════════════════════════════
    y1 = 75

    # ATMOS Gas
    box(dwg, 30, y1, 140, 55, "ATMOS ENERGY\nNatural Gas\nPipeline Feed", "Henry Hub Pricing | On-site",
        color="#0a1a0a", border="#22c55e", text_color="#22c55e")

    # Gas meter/regulator
    box(dwg, 200, y1, 110, 55, "GAS METER\n+ REGULATOR\nStation", "Custody transfer",
        border="#22c55e", text_color="#86efac")

    # Fuel storage
    box(dwg, 340, y1, 120, 55, "DIESEL FUEL\nSTORAGE\n10,000 gal", "Layer 3 backup",
        color="#2e1a1a", border="#ef4444", text_color="#ef4444")

    # Solar resource
    box(dwg, 490, y1, 140, 55, "SOLAR\nIRRADIANCE\n4.5-5.2 kWh/m2/day", "Louisiana avg | 250+ sun days",
        color="#1a1a00", border="#fbbf24", text_color="#fbbf24")

    # Grid connection
    box(dwg, 660, y1, 140, 55, "ENTERGY GRID\n500kV + 230kV\nSubstations", "SELL-BACK ONLY\nNOT a source",
        color="#1a0a0a", border="#ef4444", text_color="#ef4444")

    # Wires down
    arrow_down(dwg, 100, y1 + 55, y1 + 85, "#22c55e")
    arrow_down(dwg, 255, y1 + 55, y1 + 85, "#22c55e")
    arrow_down(dwg, 400, y1 + 55, y1 + 85, "#ef4444")
    arrow_down(dwg, 560, y1 + 55, y1 + 85, "#fbbf24")

    # ════════════════════════════════════════════
    # ROW 2: GENERATION (y=165)
    # ════════════════════════════════════════════
    y2 = 165

    # Gas generators
    gen_w = 155
    box(dwg, 30, y2, gen_w, 70, "CAT CG260-16 #1\n2.8 MW | 13.8kV\nNatural Gas Prime\nH2-Ready 25% Blend",
        "Louisiana Cat | American Made",
        color="#0a1a0a", border="#22c55e", text_color="#22c55e")
    box(dwg, 200, y2, gen_w, 70, "CAT CG260-16 #2\n2.8 MW | 13.8kV\nNatural Gas Prime\nH2-Ready 25% Blend",
        "Louisiana Cat | American Made",
        color="#0a1a0a", border="#22c55e", text_color="#22c55e")

    # Diesel genset
    box(dwg, 370, y2, 120, 70, "DIESEL GENSET\n500 kW\n480V | Emergency\nAuto-Start", "Layer 3 only",
        color="#2e1a1a", border="#ef4444", text_color="#ef4444")

    # Solar array
    box(dwg, 510, y2, 150, 70, "FIRST SOLAR ARRAY\n5+ MW Ground Mount\nSeries 7 TR1 Panels\n952V DC Strings",
        "30 mi from New Iberia factory",
        color="#1a1a00", border="#fbbf24", text_color="#fbbf24")

    # N+1 spare
    box(dwg, 680, y2, gen_w, 70, "CAT CG260-16 #3\n2.8 MW | 13.8kV\nN+1 REDUNDANT\nMaintenance Spare",
        "Any unit offline = no impact",
        color="#0a1a0a", border="#22c55e", text_color="#4ade80")

    # ════════════════════════════════════════════
    # ROW 3: PARALLELING + SWITCHGEAR (y=280)
    # ════════════════════════════════════════════
    y3 = 285

    for gx in [107, 277, 430, 757]:
        arrow_down(dwg, gx, y2 + 70, y3, "#22c55e" if gx != 430 else "#ef4444")

    # Main switchgear
    box(dwg, 30, y3, 360, 55, "PARALLELING SWITCHGEAR\nLouisiana Cat Controls | Auto-Sync | Load Sharing\nAll generators parallel to common 13.8kV bus",
        "Automatic load balancing | Generator protection relays",
        border="#22c55e", text_color="#86efac")

    # Emergency ATS
    box(dwg, 410, y3, 120, 55, "EMERGENCY\nATS\nDiesel Auto\nTransfer", "",
        border="#ef4444", text_color="#fca5a5")

    # Solar combiner
    arrow_down(dwg, 585, y2 + 70, y3, "#fbbf24")
    box(dwg, 550, y3, 120, 55, "SOLAR\nCOMBINER\nBOX\nString Fusing", "",
        border="#fbbf24", text_color="#fbbf24")

    # N+1 to switchgear
    box(dwg, 690, y3, 145, 55, "AUTO-SYNC\nCONTROLLER\nBrings N+1 online\non failure detect", "< 10 sec transfer",
        border="#22c55e", text_color="#4ade80")

    # ════════════════════════════════════════════
    # ROW 4: 13.8kV BUS (y=380)
    # ════════════════════════════════════════════
    y4 = 385
    for bx in [210, 470, 610]:
        arrow_down(dwg, bx, y3 + 55, y4, "#ff6b35")

    # Bus bar
    dwg.add(dwg.rect((30, y4 - 3), (810, 6), fill="#ff6b35", rx=2))
    dwg.add(dwg.text("13.8kV AC DISTRIBUTION BUS", insert=(435, y4 - 10), text_anchor="middle",
                      fill="#ff6b35", font_size=10, font_family="Arial", font_weight="bold"))

    # Grid sell-back arrow
    wire(dwg, 730, y4, 730, y4 - 25, "#ef4444")
    dwg.add(dwg.text("SELL-BACK", insert=(740, y4 - 15), fill="#ef4444", font_size=7, font_family="Arial"))
    dwg.add(dwg.text("to Entergy", insert=(740, y4 - 6), fill="#ef4444", font_size=7, font_family="Arial"))

    # ════════════════════════════════════════════
    # ROW 5: METERING + PROTECTION (y=420)
    # ════════════════════════════════════════════
    y5 = 420
    arrow_down(dwg, 200, y4 + 3, y5, "#ff6b35")
    arrow_down(dwg, 450, y4 + 3, y5, "#ff6b35")

    box(dwg, 130, y5, 150, 45, "REVENUE METER\n+ PROTECTION\nRelays | CT/PT", "",
        border="#ff6b35", text_color="#ff6b35", font=9)
    box(dwg, 380, y5, 150, 45, "MAIN BREAKER\n+ DISCONNECT\n13.8kV Rated", "",
        border="#ff6b35", text_color="#ff6b35", font=9)

    # ════════════════════════════════════════════
    # ROW 6: RECTIFICATION (y=505)
    # ════════════════════════════════════════════
    y6 = 510
    arrow_down(dwg, 200, y5 + 45, y6, "#ff6b35")
    arrow_down(dwg, 450, y5 + 45, y6, "#ff6b35")

    box(dwg, 80, y6, 250, 65, "EATON BEAM RUBIN DSX\nAC/DC RECTIFIER MODULE #1\n13.8kV AC --> 800V DC\n96%+ Conversion Efficiency",
        "Grid-to-chip platform | Modular | Hot-swappable",
        border="#8b5cf6", text_color="#c4b5fd")

    box(dwg, 370, y6, 250, 65, "EATON BEAM RUBIN DSX\nAC/DC RECTIFIER MODULE #2\n13.8kV AC --> 800V DC\nN+1 Redundant Module",
        "Automatic failover | No single point of failure",
        border="#8b5cf6", text_color="#c4b5fd")

    # Solar DC-Direct bypass
    solar_bypass_x = 660
    pipe(dwg, [(610, y3 + 55), (610, y3 + 70), (solar_bypass_x + 50, y3 + 70),
               (solar_bypass_x + 50, y6)], "#fbbf24", 2)
    box(dwg, solar_bypass_x, y6, 180, 65, "DC-DC BUCK\nCONVERTER\n952V String --> 800V Bus\n97% Efficiency",
        "Bypasses AC entirely | Direct solar to GPU",
        border="#fbbf24", text_color="#fbbf24")

    # ════════════════════════════════════════════
    # ROW 7: 800V DC BUS (y=615)
    # ════════════════════════════════════════════
    y7 = 620
    for rx in [205, 495, 750]:
        arrow_down(dwg, rx, y6 + 65, y7, "#8b5cf6")

    dwg.add(dwg.rect((30, y7 - 3), (810, 6), fill="#8b5cf6", rx=2))
    dwg.add(dwg.text("800V DC MAIN DISTRIBUTION BUS — NVIDIA DSX REFERENCE", insert=(435, y7 - 10),
                      text_anchor="middle", fill="#8b5cf6", font_size=10, font_family="Arial", font_weight="bold"))

    # BESS on 800V bus
    bess_x = 30
    wire(dwg, bess_x + 60, y7 + 3, bess_x + 60, y7 + 15, "#8b5cf6")
    box(dwg, bess_x, y7 + 15, 120, 55, "EATON xStorage\nBATTERY (BESS)\n800V DC Native\nRide-Through",
        "Peak shaving | 15-min reserve",
        border="#3b82f6", text_color="#93c5fd")

    # ════════════════════════════════════════════
    # ROW 8: BUSWAY DISTRIBUTION (y=670)
    # ════════════════════════════════════════════
    y8 = 680

    busway_positions = [(200, "Row 1-2"), (350, "Row 3-4"), (500, "Row 5-6"), (650, "Expansion")]
    for bx, label in busway_positions:
        arrow_down(dwg, bx + 50, y7 + 3, y8, "#8b5cf6")
        box(dwg, bx, y8, 100, 35, f"EATON BUSWAY\n{label}", "",
            border="#8b5cf6", text_color="#c4b5fd", font=8)

    # ════════════════════════════════════════════
    # ROW 9: RACK PDU + LLC + GPU (y=750)
    # ════════════════════════════════════════════
    y9 = 740
    y10 = 790
    y11 = 840

    for bx, label in busway_positions[:3]:
        cx = bx + 50
        arrow_down(dwg, cx, y8 + 35, y9, "#8b5cf6")

        # PDU
        box(dwg, bx + 10, y9, 80, 30, "RACK PDU\n800V DC", "",
            border="#8b5cf6", text_color="#c4b5fd", font=7)

        # LLC
        arrow_down(dwg, cx, y9 + 30, y10, "#76b900")
        box(dwg, bx + 5, y10, 90, 30, "64:1 LLC DC-DC\n800V --> 12.5V", "99%+ eff",
            border="#76b900", text_color="#76b900", font=7)

        # GPU Rack
        arrow_down(dwg, cx, y10 + 30, y11, "#76b900")

    # GPU Rack row
    rack_labels = ["NVL72 x12\nRACKS 1-12\n1.56 MW", "NVL72 x12\nRACKS 13-24\n1.56 MW", "NVL72 x12\nRACKS 25-36\n1.56 MW"]
    for i, (bx_label, _) in enumerate(busway_positions[:3]):
        bx = bx_label
        box(dwg, bx - 5, y11, 110, 50, rack_labels[i], "Vera Rubin | 130 kW | Liquid Cooled",
            color="#111a00", border="#76b900", text_color="#76b900", font=8)

    # Expansion placeholder
    exp_bx = busway_positions[3][0]
    box(dwg, exp_bx - 5, y9, 110, y11 - y9 + 50, "EXPANSION\nPHASE 2\n\nRacks 37-72\n4.68 MW\n\nInfrastructure\npre-wired",
        "", border="#333", text_color="#555", font=8)

    # ════════════════════════════════════════════
    # RIGHT SIDE: 4-LAYER HIERARCHY DIAGRAM
    # ════════════════════════════════════════════
    hx = 880
    hy = 75

    dwg.add(dwg.rect((hx, hy), (490, 820), rx=8, fill="#111318", stroke="#1e2230", stroke_width=1))
    dwg.add(dwg.text("4-LAYER POWER HIERARCHY", insert=(hx + 245, hy + 20), text_anchor="middle",
                      fill="#f0f2f5", font_size=12, font_family="Arial", font_weight="bold"))

    layers = [
        {
            "num": "1", "name": "SOLAR", "color": "#fbbf24",
            "role": "PRIMARY OFFSET",
            "details": [
                "First Solar Series 7 TR1 panels",
                "Ground-mounted on 400+ acres",
                "5+ MW Phase 1, expandable to 50+ MW",
                "DC-Direct to 800V bus (97% eff)",
                "Made 30 miles away in New Iberia, LA",
                "0.3%/yr degradation (industry best)",
                "30-year manufacturer warranty",
            ]
        },
        {
            "num": "2", "name": "NATURAL GAS", "color": "#22c55e",
            "role": "BACKBONE — ALWAYS RUNNING",
            "details": [
                "Cat CG260-16 generators (2.8 MW each)",
                "3 units: 8.4 MW total (N+1 redundant)",
                "ATMOS Energy pipeline on-site",
                "Henry Hub pricing = cheapest in USA",
                "H2-ready (25% hydrogen blend)",
                "Louisiana Cat service contract",
                "Carries FULL load 24/7/365",
            ]
        },
        {
            "num": "3", "name": "DIESEL", "color": "#ef4444",
            "role": "EMERGENCY ONLY",
            "details": [
                "500 kW diesel generator",
                "10,000 gal on-site fuel storage",
                "Auto-start on dual gas failure",
                "Pipeline-independent fuel source",
                "Bridges until gas restored",
                "Required for NVIDIA certification",
            ]
        },
        {
            "num": "4", "name": "GRID (SELL-BACK)", "color": "#ef4444",
            "role": "SELL-BACK ONLY — NOT A SOURCE",
            "details": [
                "500kV + 230kV substations on-site",
                "Entergy bidirectional interconnect",
                "Excess power sold BACK to grid",
                "Revenue generation, not consumption",
                "Grid is NEVER used to power GPUs",
                "Former 2,200 MW plant infrastructure",
            ]
        },
    ]

    ly = hy + 40
    for layer in layers:
        # Layer header
        dwg.add(dwg.rect((hx + 15, ly), (460, 25), rx=4, fill="#111318",
                          stroke=layer["color"], stroke_width=1))
        dwg.add(dwg.text(f"LAYER {layer['num']}: {layer['name']}", insert=(hx + 25, ly + 16),
                          fill=layer["color"], font_size=11, font_family="Arial", font_weight="bold"))
        dwg.add(dwg.text(layer["role"], insert=(hx + 470, ly + 16), text_anchor="end",
                          fill=layer["color"], font_size=8, font_family="Arial", font_weight="bold"))

        # Details
        for i, detail in enumerate(layer["details"]):
            dwg.add(dwg.text(f"  {detail}", insert=(hx + 30, ly + 38 + i * 13),
                              fill="#9ca3af", font_size=8, font_family="Arial"))

        ly += 30 + len(layer["details"]) * 13 + 15

    # ════════════════════════════════════════════
    # BOTTOM: PHASE 1 STATS
    # ════════════════════════════════════════════
    sy = 920
    dwg.add(dwg.rect((30, sy), (1340, 40), rx=6, fill="#111318", stroke="#1e2230"))
    stats = [
        ("GAS GENERATION", "8.4 MW (N+1)"),
        ("SOLAR", "5+ MW DC-Direct"),
        ("IT LOAD", "4.68 MW"),
        ("TOTAL FACILITY", "~6.5 MW"),
        ("PUE TARGET", "< 1.15"),
        ("RACKS", "36 NVL72"),
        ("GPUs", "2,592"),
    ]
    sx = 55
    for label, value in stats:
        dwg.add(dwg.text(label, insert=(sx, sy + 14), fill="#6b7280",
                          font_size=7, font_family="Arial", font_weight="bold"))
        dwg.add(dwg.text(value, insert=(sx, sy + 28), fill="#22c55e",
                          font_size=10, font_family="Arial", font_weight="bold"))
        sx += 190

    # ════════════════════════════════════════════
    # NOTES
    # ════════════════════════════════════════════
    ny = 975
    notes = [
        "1. Gas is the BACKBONE (Layer 2) — always running, carries full facility load 24/7. Solar offsets but does not replace gas.",
        "2. Grid is SELL-BACK ONLY (Layer 4) — excess generation returns to Entergy. GPUs NEVER run on grid power.",
        "3. N+1 generator redundancy: 3x CG260 for 2-unit load. Any single unit offline = zero impact to operations.",
        "4. Solar DC-Direct bypasses all AC conversion — 952V strings buck to 800V, feeds DSX bus at 97% efficiency.",
        "5. BESS provides ride-through during generator sync/transfer events + peak shaving for GPU training spikes.",
        "6. All fuel equipment American-made: Cat generators (Louisiana Cat), Eaton power distribution, First Solar panels.",
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
