"""
Ragin' Cajun Compute Campus — Trappeys Cannery, Lafayette, LA
Power Distribution Schematic
4-Layer Hierarchy: Solar -> Gas -> Diesel -> Grid (sell-back)
Gas G3520C -> Switchgear -> Eaton 800V DC -> Busway -> Racks
"""
import svgwrite

W, H = 1400, 1050
OUT = "adc3k-deploy/blueprints/trappeys-power-distribution.svg"

ACCENT = "#CE181E"


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
    dwg.add(dwg.text("RAGIN' CAJUN COMPUTE CAMPUS — TRAPPEYS CANNERY, LAFAYETTE, LA",
                      insert=(W / 2, 24), text_anchor="middle", fill="#f0f2f5",
                      font_size=16, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("POWER DISTRIBUTION SCHEMATIC | FUEL TO CHIP | 4-LAYER POWER HIERARCHY",
                      insert=(W / 2, 40), text_anchor="middle", fill=ACCENT,
                      font_size=10, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("Sheet P-001 | Design Intent | 2026-03-23 | NOT FOR CONSTRUCTION",
                      insert=(W / 2, 54), text_anchor="middle", fill="#6b7280",
                      font_size=9, font_family="Arial"))

    # ================================================================
    # ROW 1: FUEL SOURCES (y=75)
    # ================================================================
    y1 = 75

    # ATMOS Gas
    box(dwg, 30, y1, 140, 55, "ATMOS ENERGY\nNatural Gas\nTrunk Line on Property", "Henry Hub Pricing",
        color="#0a1a0a", border="#22c55e", text_color="#22c55e")

    # Gas meter
    box(dwg, 200, y1, 110, 55, "GAS METER\n+ REGULATOR\nStation", "Custody transfer",
        border="#22c55e", text_color="#86efac")

    # Diesel storage
    box(dwg, 340, y1, 120, 55, "DIESEL FUEL\nSTORAGE\n5,000 gal", "Layer 3 backup",
        color="#2e1a1a", border="#ef4444", text_color="#ef4444")

    # Solar resource
    box(dwg, 490, y1, 140, 55, "SOLAR\nIRRADIANCE\n4.5-5.2 kWh/m2/day", "Louisiana avg | Rooftop",
        color="#1a1a00", border="#fbbf24", text_color="#fbbf24")

    # LUS Grid
    box(dwg, 660, y1, 140, 55, "LUS GRID\n480V Service\nSELL-BACK ONLY", "NOT a source",
        color="#1a0a0a", border="#ef4444", text_color="#ef4444")

    # Wires down
    arrow_down(dwg, 100, y1 + 55, y1 + 85, "#22c55e")
    arrow_down(dwg, 255, y1 + 55, y1 + 85, "#22c55e")
    arrow_down(dwg, 400, y1 + 55, y1 + 85, "#ef4444")
    arrow_down(dwg, 560, y1 + 55, y1 + 85, "#fbbf24")

    # ================================================================
    # ROW 2: GENERATION (y=165)
    # ================================================================
    y2 = 165

    gen_w = 155
    box(dwg, 30, y2, gen_w, 70, "CAT G3520C #1\n1.5 MW | 480V AC\nNatural Gas Prime\nLayer 2 Backbone",
        "Louisiana Cat | American Made",
        color="#0a1a0a", border="#22c55e", text_color="#22c55e")
    box(dwg, 200, y2, gen_w, 70, "CAT G3520C #2\n1.5 MW | 480V AC\nN+1 REDUNDANT\nMaintenance Spare",
        "Any unit offline = no impact",
        color="#0a1a0a", border="#22c55e", text_color="#4ade80")

    # Diesel genset
    box(dwg, 370, y2, 120, 70, "DIESEL GENSET\n250 kW\n480V | Emergency\nAuto-Start", "Layer 3 only",
        color="#2e1a1a", border="#ef4444", text_color="#ef4444")

    # Solar array
    box(dwg, 510, y2, 150, 70, "FIRST SOLAR ARRAY\n2.05 MW Rooftop\nSeries 7 TR1 Panels\n952V DC Strings",
        "3,731 panels | All 4 buildings",
        color="#1a1a00", border="#fbbf24", text_color="#fbbf24")

    # ================================================================
    # ROW 3: PARALLELING + SWITCHGEAR (y=285)
    # ================================================================
    y3 = 285

    for gx in [107, 277, 430]:
        arrow_down(dwg, gx, y2 + 70, y3, "#22c55e" if gx != 430 else "#ef4444")

    box(dwg, 30, y3, 330, 55, "PARALLELING SWITCHGEAR + ATS\nLouisiana Cat Controls | Auto-Sync | Load Sharing\nBoth G3520C parallel to common 480V AC bus",
        "Automatic load balancing | Generator protection relays",
        border="#22c55e", text_color="#86efac")

    box(dwg, 380, y3, 120, 55, "EMERGENCY\nATS\nDiesel Auto\nTransfer", "",
        border="#ef4444", text_color="#fca5a5")

    # Solar combiner
    arrow_down(dwg, 585, y2 + 70, y3, "#fbbf24")
    box(dwg, 520, y3, 120, 55, "SOLAR\nCOMBINER\nBOX\nString Fusing", "",
        border="#fbbf24", text_color="#fbbf24")

    # ================================================================
    # ROW 4: 480V AC BUS (y=385)
    # ================================================================
    y4 = 385
    for bx in [195, 440, 580]:
        arrow_down(dwg, bx, y3 + 55, y4, "#ff6b35")

    dwg.add(dwg.rect((30, y4 - 3), (780, 6), fill="#ff6b35", rx=2))
    dwg.add(dwg.text("480V AC DISTRIBUTION BUS", insert=(420, y4 - 10), text_anchor="middle",
                      fill="#ff6b35", font_size=10, font_family="Arial", font_weight="bold"))

    # Grid sell-back arrow
    wire(dwg, 730, y1 + 55, 730, y4 - 20, "#ef4444")
    dwg.add(dwg.text("SELL-BACK", insert=(740, y4 - 25), fill="#ef4444", font_size=7, font_family="Arial"))
    dwg.add(dwg.text("to LUS", insert=(740, y4 - 15), fill="#ef4444", font_size=7, font_family="Arial"))

    # ================================================================
    # ROW 5: METERING + PROTECTION (y=420)
    # ================================================================
    y5 = 420
    arrow_down(dwg, 200, y4 + 3, y5, "#ff6b35")
    arrow_down(dwg, 450, y4 + 3, y5, "#ff6b35")

    box(dwg, 130, y5, 150, 45, "REVENUE METER\n+ PROTECTION\nRelays | CT/PT", "",
        border="#ff6b35", text_color="#ff6b35", font=9)
    box(dwg, 380, y5, 150, 45, "MAIN BREAKER\n+ DISCONNECT\n480V Rated", "",
        border="#ff6b35", text_color="#ff6b35", font=9)

    # ================================================================
    # ROW 6: RECTIFICATION (y=510)
    # ================================================================
    y6 = 510
    arrow_down(dwg, 200, y5 + 45, y6, "#ff6b35")
    arrow_down(dwg, 450, y5 + 45, y6, "#ff6b35")

    box(dwg, 80, y6, 250, 65, "EATON BEAM RUBIN DSX\nAC/DC RECTIFIER #1\n480V AC -> 800V DC\n96%+ Conversion Efficiency",
        "Grid-to-chip platform | Modular",
        border="#8b5cf6", text_color="#c4b5fd")

    box(dwg, 370, y6, 250, 65, "EATON BEAM RUBIN DSX\nAC/DC RECTIFIER #2\n480V AC -> 800V DC\nN+1 Redundant Module",
        "Automatic failover",
        border="#8b5cf6", text_color="#c4b5fd")

    # Solar DC-Direct bypass
    solar_bypass_x = 660
    pipe(dwg, [(580, y3 + 55), (580, y3 + 70), (solar_bypass_x + 50, y3 + 70),
               (solar_bypass_x + 50, y6)], "#fbbf24", 2)
    box(dwg, solar_bypass_x, y6, 180, 65, "DC-DC BUCK\nCONVERTER\n952V String -> 800V Bus\n97% Efficiency",
        "Bypasses AC entirely | Solar DC-Direct",
        border="#fbbf24", text_color="#fbbf24")

    # ================================================================
    # ROW 7: 800V DC BUS (y=620)
    # ================================================================
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
        "Peak shaving | Reserve",
        border="#3b82f6", text_color="#93c5fd")

    # ================================================================
    # ROW 8: BUSWAY + RACKS (y=680)
    # ================================================================
    y8 = 680
    y9 = 740
    y10 = 790
    y11 = 840

    busway_positions = [(200, "Rack 1-2"), (400, "Rack 3-4"), (600, "Expansion")]
    for bx, label in busway_positions:
        arrow_down(dwg, bx + 50, y7 + 3, y8, "#8b5cf6")
        box(dwg, bx, y8, 100, 35, f"EATON BUSWAY\n{label}", "",
            border="#8b5cf6", text_color="#c4b5fd", font=8)

    for bx, label in busway_positions[:2]:
        cx = bx + 50
        arrow_down(dwg, cx, y8 + 35, y9, "#8b5cf6")
        box(dwg, bx + 10, y9, 80, 30, "RACK PDU\n800V DC", "",
            border="#8b5cf6", text_color="#c4b5fd", font=7)

        arrow_down(dwg, cx, y9 + 30, y10, "#76b900")
        box(dwg, bx + 5, y10, 90, 30, "64:1 LLC DC-DC\n800V -> 12.5V", "99%+ eff",
            border="#76b900", text_color="#76b900", font=7)

        arrow_down(dwg, cx, y10 + 30, y11, "#76b900")

    # GPU Racks
    rack_labels = ["NVL72 x2\nRACKS 1-2\n260 kW", "NVL72 x2\nRACKS 3-4\n260 kW"]
    for i, (bx_label, _) in enumerate(busway_positions[:2]):
        bx = bx_label
        box(dwg, bx - 5, y11, 110, 50, rack_labels[i], "Vera Rubin | 130 kW | Liquid Cooled",
            color="#111a00", border="#76b900", text_color="#76b900", font=8)

    # Expansion placeholder
    exp_bx = busway_positions[2][0]
    box(dwg, exp_bx - 5, y9, 110, y11 - y9 + 50, "EXPANSION\nPHASE 2\n\nUp to 32\nmore racks\nin Middle Low\n\nPre-wired",
        "", border="#333", text_color="#555", font=8)

    # ================================================================
    # RIGHT SIDE: 4-LAYER HIERARCHY DIAGRAM
    # ================================================================
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
                "Rooftop arrays across all 4 buildings",
                "3,731 panels = 2.05 MW total",
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
                "Cat G3520C generators (1.5 MW each)",
                "2 units: 3.0 MW total (N+1 redundant)",
                "ATMOS Energy trunk line on property",
                "Henry Hub pricing = cheapest in USA",
                "480V AC output to Eaton rectifiers",
                "Louisiana Cat service contract",
                "Carries FULL load 24/7/365",
            ]
        },
        {
            "num": "3", "name": "DIESEL", "color": "#ef4444",
            "role": "EMERGENCY ONLY",
            "details": [
                "Diesel emergency generator",
                "On-site fuel storage",
                "Auto-start on dual gas failure",
                "Pipeline-independent fuel source",
                "Bridges until gas restored",
                "Required for NVIDIA certification",
            ]
        },
        {
            "num": "4", "name": "GRID (LUS)", "color": "#ef4444",
            "role": "SELL-BACK ONLY — NOT A SOURCE",
            "details": [
                "Lafayette Utilities System (LUS)",
                "480V service connection",
                "Excess power sold BACK to grid",
                "Revenue generation, not consumption",
                "Grid is NEVER used to power GPUs",
                "Cloudy day = gas carries the load",
            ]
        },
    ]

    ly = hy + 40
    for layer in layers:
        dwg.add(dwg.rect((hx + 15, ly), (460, 25), rx=4, fill="#111318",
                          stroke=layer["color"], stroke_width=1))
        dwg.add(dwg.text(f"LAYER {layer['num']}: {layer['name']}", insert=(hx + 25, ly + 16),
                          fill=layer["color"], font_size=11, font_family="Arial", font_weight="bold"))
        dwg.add(dwg.text(layer["role"], insert=(hx + 470, ly + 16), text_anchor="end",
                          fill=layer["color"], font_size=8, font_family="Arial", font_weight="bold"))

        for i, detail in enumerate(layer["details"]):
            dwg.add(dwg.text(f"  {detail}", insert=(hx + 30, ly + 38 + i * 13),
                              fill="#9ca3af", font_size=8, font_family="Arial"))

        ly += 30 + len(layer["details"]) * 13 + 15

    # ================================================================
    # BOTTOM: PHASE 1 STATS
    # ================================================================
    sy = 920
    dwg.add(dwg.rect((30, sy), (1340, 40), rx=6, fill="#111318", stroke="#1e2230"))
    stats = [
        ("GAS GENERATION", "3.0 MW (N+1)"),
        ("SOLAR", "2.05 MW Rooftop"),
        ("IT LOAD", "520 kW"),
        ("TOTAL FACILITY", "~650 kW"),
        ("GENSET LOAD", "~22% each"),
        ("RACKS", "4 NVL72"),
        ("GPUs", "288"),
    ]
    sx = 55
    for label, value in stats:
        dwg.add(dwg.text(label, insert=(sx, sy + 14), fill="#6b7280",
                          font_size=7, font_family="Arial", font_weight="bold"))
        dwg.add(dwg.text(value, insert=(sx, sy + 28), fill=ACCENT,
                          font_size=10, font_family="Arial", font_weight="bold"))
        sx += 190

    # ================================================================
    # NOTES
    # ================================================================
    ny = 975
    notes = [
        "1. Gas is the BACKBONE (Layer 2) — always running, carries full facility load 24/7. Solar offsets but does not replace gas.",
        "2. Grid (LUS) is SELL-BACK ONLY (Layer 4) — excess generation returns to LUS. GPUs NEVER run on grid power.",
        "3. N+1 generator redundancy: 2x G3520C for single-unit load. Either unit offline = zero impact to operations.",
        "4. Solar DC-Direct bypasses all AC conversion — 952V strings buck to 800V, feeds DSX bus at 97% efficiency.",
        "5. BESS provides ride-through during generator sync/transfer events + peak shaving for GPU training spikes.",
        "6. All equipment American-made: Cat generators (Louisiana Cat), Eaton power distribution, First Solar panels.",
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
