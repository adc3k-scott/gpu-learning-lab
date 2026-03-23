"""
Willow Glen Tiger Compute Campus — Solar Array Layout
First Solar Series 7 TR1 ground-mount, DC-Direct to 800V bus
SVG output
"""
import svgwrite

W, H = 1400, 950
OUT = "adc3k-deploy/blueprints/solar-layout.svg"


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


def build():
    dwg = svgwrite.Drawing(OUT, size=(f"{W}px", f"{H}px"), viewBox=f"0 0 {W} {H}")
    dwg.add(dwg.rect((0, 0), (W, H), fill="#0a0b0f"))

    # ── TITLE ──
    dwg.add(dwg.text("TIGER COMPUTE CAMPUS — WILLOW GLEN, ST. GABRIEL, LA",
                      insert=(W / 2, 24), text_anchor="middle", fill="#f0f2f5",
                      font_size=16, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("SOLAR ARRAY LAYOUT | FIRST SOLAR SERIES 7 TR1 | DC-DIRECT TO 800V BUS",
                      insert=(W / 2, 40), text_anchor="middle", fill="#fbbf24",
                      font_size=10, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("Sheet L-001 | MVP Design Intent | 2026-03-22 | NOT FOR CONSTRUCTION",
                      insert=(W / 2, 54), text_anchor="middle", fill="#6b7280",
                      font_size=9, font_family="Arial"))

    # ════════════════════════════════════════════
    # ARRAY FIELD LAYOUT (TOP SECTION)
    # ════════════════════════════════════════════
    field_x, field_y = 50, 80
    field_w, field_h = 850, 480

    # Field boundary
    dwg.add(dwg.rect((field_x, field_y), (field_w, field_h), fill="#0d0d00",
                      stroke="#fbbf24", stroke_width=1.5, rx=6))
    dwg.add(dwg.text("SOLAR ARRAY ZONE A — 600' x 2,400' (~33 ACRES)", insert=(field_x + field_w / 2, field_y - 8),
                      text_anchor="middle", fill="#fbbf24", font_size=10, font_family="Arial", font_weight="bold"))

    # Panel rows
    num_rows = 18
    row_h = (field_h - 40) / num_rows
    panels_per_row = 30  # visual representation

    for r in range(num_rows):
        ry = field_y + 20 + r * row_h
        # Panel strip
        panel_w = field_w - 80
        dwg.add(dwg.rect((field_x + 40, ry), (panel_w, row_h * 0.5), fill="#1a1a3a",
                          stroke="#2a2a5a", stroke_width=0.5, rx=1))
        # Individual panel segments
        seg_w = panel_w / panels_per_row
        for p in range(panels_per_row):
            px = field_x + 40 + p * seg_w
            dwg.add(dwg.rect((px + 0.5, ry + 0.5), (seg_w - 1, row_h * 0.5 - 1),
                              fill="#1a1a4a", stroke="#2a2a6a", stroke_width=0.3))

        # Row label (every 3rd row)
        if r % 3 == 0:
            dwg.add(dwg.text(f"Row {r + 1}", insert=(field_x + 15, ry + row_h * 0.35),
                              fill="#555", font_size=6, font_family="Arial"))

    # Service roads between every 6 rows
    for r in [6, 12]:
        ry = field_y + 20 + r * row_h - 2
        dwg.add(dwg.rect((field_x + 30, ry), (field_w - 60, 4), fill="#333", rx=1))
        dwg.add(dwg.text("SERVICE ROAD", insert=(field_x + field_w / 2, ry + 3),
                          text_anchor="middle", fill="#555", font_size=5, font_family="Arial"))

    # Perimeter road
    dwg.add(dwg.rect((field_x + 5, field_y + 5), (field_w - 10, field_h - 10),
                      fill="none", stroke="#333", stroke_width=1, stroke_dasharray="4,4", rx=4))

    # Combiner boxes
    cb_positions = [(field_x + field_w - 35, field_y + 80),
                    (field_x + field_w - 35, field_y + 220),
                    (field_x + field_w - 35, field_y + 360)]
    for i, (cx, cy) in enumerate(cb_positions):
        dwg.add(dwg.rect((cx, cy), (25, 30), fill="#1a1a00", stroke="#fbbf24", stroke_width=1, rx=2))
        dwg.add(dwg.text(f"CB{i + 1}", insert=(cx + 12, cy + 18), text_anchor="middle",
                          fill="#fbbf24", font_size=7, font_family="Arial", font_weight="bold"))

    # DC conduit run from combiners to inverter/converter
    for cx, cy in cb_positions:
        dwg.add(dwg.line((cx + 25, cy + 15), (field_x + field_w + 30, cy + 15),
                          stroke="#fbbf24", stroke_width=1))

    # ════════════════════════════════════════════
    # RIGHT SIDE: ELECTRICAL EQUIPMENT
    # ════════════════════════════════════════════
    eq_x = field_x + field_w + 50

    # String combiner panel
    box(dwg, eq_x, 100, 160, 60, "STRING COMBINER\nPANEL\n18 strings x 5 panels", "Fused inputs | Monitoring",
        border="#fbbf24", text_color="#fbbf24")

    # DC-DC Converter
    dwg.add(dwg.line((eq_x + 80, 160), (eq_x + 80, 200), stroke="#fbbf24", stroke_width=1.5))
    box(dwg, eq_x, 200, 160, 60, "DC-DC BUCK\nCONVERTER\n952V --> 800V DC", "97% efficiency | MPPT tracking",
        border="#fbbf24", text_color="#fbbf24")

    # To 800V bus
    dwg.add(dwg.line((eq_x + 80, 260), (eq_x + 80, 310), stroke="#8b5cf6", stroke_width=2))
    box(dwg, eq_x, 310, 160, 50, "800V DC BUS\n(DSX Reference)", "Feeds directly to GPU racks",
        border="#8b5cf6", text_color="#c4b5fd")

    # AC path (alternative/future)
    dwg.add(dwg.line((eq_x + 160, 230), (eq_x + 200, 230), stroke="#fbbf24", stroke_width=1,
                      stroke_dasharray="4,3"))
    box(dwg, eq_x + 200, 200, 140, 60, "INVERTER\n(FUTURE/ALT)\nDC --> AC --> Grid\nSell-back path",
        "", border="#555", text_color="#555")

    # ════════════════════════════════════════════
    # PANEL SPECIFICATIONS
    # ════════════════════════════════════════════
    spec_y = 580
    dwg.add(dwg.rect((50, spec_y), (600, 180), rx=6, fill="#111318", stroke="#1e2230"))
    dwg.add(dwg.text("FIRST SOLAR SERIES 7 TR1 — PANEL SPECIFICATIONS", insert=(350, spec_y + 18),
                      text_anchor="middle", fill="#fbbf24", font_size=10, font_family="Arial", font_weight="bold"))

    specs = [
        ("Panel Model", "First Solar Series 7 TR1"),
        ("Rated Power", "550W per panel"),
        ("Efficiency", "19.7% (CdTe thin-film)"),
        ("Dimensions", "~2.5m x 1.2m (8.2' x 3.9')"),
        ("Vmp (max power voltage)", "190.4V"),
        ("String Configuration", "5 panels in series = 952V"),
        ("Degradation Rate", "0.3%/year (industry best)"),
        ("Warranty", "30-year manufacturer warranty"),
        ("Manufacturing", "New Iberia, LA ($1.1B factory)"),
        ("Distance to Site", "~90 miles (1.5 hr drive)"),
        ("Temperature Coefficient", "-0.28%/C (superior in heat)"),
        ("Humidity Performance", "CdTe outperforms Si in humidity"),
    ]

    sx = 70
    for i, (label, value) in enumerate(specs):
        col = i % 2
        row = i // 2
        x_pos = sx + col * 300
        y_pos = spec_y + 35 + row * 22
        dwg.add(dwg.text(label, insert=(x_pos, y_pos), fill="#6b7280",
                          font_size=8, font_family="Arial"))
        dwg.add(dwg.text(value, insert=(x_pos + 150, y_pos), fill="#fbbf24",
                          font_size=8, font_family="Arial", font_weight="bold"))

    # ════════════════════════════════════════════
    # STRING / ARRAY MATH
    # ════════════════════════════════════════════
    math_x = 680
    dwg.add(dwg.rect((math_x, spec_y), (670, 180), rx=6, fill="#111318", stroke="#1e2230"))
    dwg.add(dwg.text("DC-DIRECT ARRAY MATH", insert=(math_x + 335, spec_y + 18),
                      text_anchor="middle", fill="#fbbf24", font_size=10, font_family="Arial", font_weight="bold"))

    calcs = [
        ("Panels per String", "5 (series) = 952V Vmp"),
        ("Strings per Row", "~50 strings"),
        ("Rows", "18"),
        ("Total Strings", "~900"),
        ("Total Panels", "~4,500"),
        ("Total Capacity", "~2.475 MW (Zone A)"),
        ("Zone B (future)", "~2.5 MW additional"),
        ("Combined", "~5 MW Phase 1"),
        ("Annual Production", "~7,500 MWh (est)"),
        ("String Voltage", "952V (5 x 190.4V Vmp)"),
        ("Buck to Bus", "952V --> 800V DC"),
        ("Path Efficiency", "97% (vs 92% AC path)"),
    ]

    for i, (label, value) in enumerate(calcs):
        col = i % 2
        row = i // 2
        x_pos = math_x + 20 + col * 340
        y_pos = spec_y + 35 + row * 22
        dwg.add(dwg.text(label, insert=(x_pos, y_pos), fill="#6b7280",
                          font_size=8, font_family="Arial"))
        dwg.add(dwg.text(value, insert=(x_pos + 160, y_pos), fill="#fbbf24",
                          font_size=8, font_family="Arial", font_weight="bold"))

    # ════════════════════════════════════════════
    # DC-DIRECT vs AC PATH COMPARISON
    # ════════════════════════════════════════════
    cmp_y = 780
    dwg.add(dwg.rect((50, cmp_y), (1300, 55), rx=6, fill="#111318", stroke="#1e2230"))

    # DC-Direct path
    dwg.add(dwg.text("DC-DIRECT PATH (OUR DESIGN):", insert=(70, cmp_y + 18), fill="#fbbf24",
                      font_size=9, font_family="Arial", font_weight="bold"))
    dc_path = "Panel (190V) --> String (952V) --> Buck DC-DC (800V) --> DSX Bus --> Rack PDU --> 64:1 LLC --> GPU"
    dwg.add(dwg.text(dc_path, insert=(70, cmp_y + 32), fill="#fbbf24", font_size=8, font_family="Arial"))
    dwg.add(dwg.text("Total Path Efficiency: 97%", insert=(70, cmp_y + 45), fill="#76b900",
                      font_size=9, font_family="Arial", font_weight="bold"))

    # AC path
    dwg.add(dwg.text("TRADITIONAL AC PATH:", insert=(720, cmp_y + 18), fill="#555",
                      font_size=9, font_family="Arial", font_weight="bold"))
    ac_path = "Panel --> Inverter (DC-AC) --> Transformer --> UPS --> PDU --> PSU (AC-DC) --> GPU"
    dwg.add(dwg.text(ac_path, insert=(720, cmp_y + 32), fill="#555", font_size=8, font_family="Arial"))
    dwg.add(dwg.text("Total Path Efficiency: 88-92%", insert=(720, cmp_y + 45), fill="#ef4444",
                      font_size=9, font_family="Arial", font_weight="bold"))

    # ════════════════════════════════════════════
    # NOTES
    # ════════════════════════════════════════════
    ny = 855
    notes = [
        "1. First Solar Series 7 TR1 panels manufactured in New Iberia, LA — $1.1B factory, 30 miles from Trappeys, 90 miles from Willow Glen",
        "2. CdTe thin-film technology outperforms silicon in Louisiana's heat and humidity — superior temperature coefficient (-0.28%/C)",
        "3. 5-panel strings at 952V Vmp, buck-converted to 800V for direct feed into NVIDIA DSX bus — no AC conversion needed",
        "4. DC-Direct path saves 5-9% efficiency vs traditional AC path — at 5 MW, that's 250-450 kW saved continuously",
        "5. 0.3%/year degradation is industry best — after 30 years, panels still produce 91% of original capacity",
        "6. Array sized for Phase 1 (~5 MW). 400+ developable acres allow expansion to 50+ MW at full build-out",
        "7. Perimeter fencing, service roads between every 6 rows, gravel access paths for maintenance vehicles",
        "8. Made in America: First Solar is the only major US-headquartered solar manufacturer. Louisiana supply chain.",
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
