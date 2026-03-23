"""
Ragin' Cajun Compute Campus — Trappeys Cannery, Lafayette, LA
Solar Array Layout — Rooftop across all 4 buildings
3,731 First Solar TR1 panels = 2.05 MW | DC-Direct to 800V bus
"""
import svgwrite

W, H = 1400, 1000
OUT = "adc3k-deploy/blueprints/trappeys-solar-layout.svg"

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


def build():
    dwg = svgwrite.Drawing(OUT, size=(f"{W}px", f"{H}px"), viewBox=f"0 0 {W} {H}")
    dwg.add(dwg.rect((0, 0), (W, H), fill="#0a0b0f"))

    # -- TITLE --
    dwg.add(dwg.text("RAGIN' CAJUN COMPUTE CAMPUS — TRAPPEYS CANNERY, LAFAYETTE, LA",
                      insert=(W / 2, 24), text_anchor="middle", fill="#f0f2f5",
                      font_size=16, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("ROOFTOP SOLAR LAYOUT | FIRST SOLAR SERIES 7 TR1 | 3,731 PANELS | 2.05 MW | DC-DIRECT TO 800V BUS",
                      insert=(W / 2, 40), text_anchor="middle", fill=ACCENT,
                      font_size=10, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("Sheet L-001 | Design Intent | 2026-03-23 | NOT FOR CONSTRUCTION",
                      insert=(W / 2, 54), text_anchor="middle", fill="#6b7280",
                      font_size=9, font_family="Arial"))

    # ================================================================
    # ROOFTOP LAYOUT — ALL 4 BUILDINGS (TOP SECTION)
    # ================================================================
    # Scale: 1 ft = 1.6 px (to fit 300 ft width)
    scale = 1.6
    start_x = 50
    start_y = 80
    gap = 12  # gap between buildings

    buildings = [
        {
            "name": "FRONT BUILDING", "w": 300, "h": 75, "sf": 22500,
            "desc": "Museum / Education / Control Room",
            "panels": 658, "kw": 362, "color": "#3b82f6",
        },
        {
            "name": "MIDDLE LOW BUILDING", "w": 300, "h": 100, "sf": 30000,
            "desc": "Phase 2 Remodel",
            "panels": 1105, "kw": 608, "color": "#6b7280",
        },
        {
            "name": "MIDDLE HIGH BUILDING", "w": 300, "h": 75, "sf": 22500,
            "desc": "PHASE 1 DEPLOY — GPU Compute",
            "panels": 658, "kw": 362, "color": ACCENT,
        },
        {
            "name": "REAR HIGH BUILDING", "w": 250, "h": 150, "sf": 37500,
            "desc": "Staging Area",
            "panels": 1310, "kw": 721, "color": "#6b7280",
        },
    ]

    total_panels = 0
    total_kw = 0
    cy = start_y

    for bldg in buildings:
        bw = int(bldg["w"] * scale)
        bh = int(bldg["h"] * scale)
        total_panels += bldg["panels"]
        total_kw += bldg["kw"]

        # Building outline
        is_active = "PHASE 1" in bldg["desc"]
        fill = "#0d0d12"
        dwg.add(dwg.rect((start_x, cy), (bw, bh), fill=fill, stroke=bldg["color"],
                          stroke_width=2 if is_active else 1, rx=3))

        # Solar panel grid (visual representation)
        panel_margin = 8
        panel_area_w = bw - 2 * panel_margin
        panel_area_h = bh - 2 * panel_margin

        if panel_area_w > 0 and panel_area_h > 0:
            # Draw panel rows
            row_h = 6
            num_rows = max(1, panel_area_h // (row_h + 2))
            panels_per_visual_row = max(1, panel_area_w // 8)

            for r in range(num_rows):
                ry = cy + panel_margin + r * (row_h + 2)
                if ry + row_h > cy + bh - panel_margin:
                    break
                for p in range(panels_per_visual_row):
                    px = start_x + panel_margin + p * 8
                    if px + 7 > start_x + bw - panel_margin:
                        break
                    dwg.add(dwg.rect((px, ry), (7, row_h), fill="#1a1a4a",
                                      stroke="#2a2a6a", stroke_width=0.3, rx=0.5))

        # Building label (right side)
        label_x = start_x + bw + 15
        label_y = cy + bh / 2

        dwg.add(dwg.text(bldg["name"], insert=(label_x, label_y - 14),
                          fill=bldg["color"], font_size=10, font_family="Arial", font_weight="bold"))
        dwg.add(dwg.text(f"{bldg['w']}' x {bldg['h']}' = {bldg['sf']:,} sf",
                          insert=(label_x, label_y), fill="#9ca3af", font_size=8, font_family="Arial"))
        dwg.add(dwg.text(f"{bldg['panels']:,} panels = {bldg['kw']} kW",
                          insert=(label_x, label_y + 14), fill="#fbbf24",
                          font_size=9, font_family="Arial", font_weight="bold"))
        dwg.add(dwg.text(bldg["desc"], insert=(label_x, label_y + 28),
                          fill="#6b7280", font_size=7, font_family="Arial"))

        # Combiner box on right side of each building
        cb_x = start_x + bw - 20
        cb_y = cy + bh / 2 - 10
        dwg.add(dwg.rect((cb_x, cb_y), (16, 20), fill="#1a1a00", stroke="#fbbf24", stroke_width=1, rx=2))
        dwg.add(dwg.text("CB", insert=(cb_x + 8, cb_y + 13), text_anchor="middle",
                          fill="#fbbf24", font_size=6, font_family="Arial", font_weight="bold"))

        # DC conduit from combiner to main run
        dwg.add(dwg.line((cb_x + 16, cb_y + 10), (start_x + bw + 5, cb_y + 10),
                          stroke="#fbbf24", stroke_width=1))

        cy += bh + gap

    # Total summary below buildings
    dwg.add(dwg.text(f"TOTAL: {total_panels:,} panels = {total_kw:,} kW ({total_kw / 1000:.2f} MW)",
                      insert=(start_x, cy + 15), fill=ACCENT,
                      font_size=11, font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text("(Actual: 3,731 panels = 2.05 MW — panel counts per building are proportional estimates based on roof area)",
                      insert=(start_x, cy + 30), fill="#6b7280", font_size=7, font_family="Arial"))

    # Main DC conduit run (vertical line collecting all combiners)
    conduit_x = start_x + int(300 * scale) + 8
    dwg.add(dwg.line((conduit_x, start_y + 20), (conduit_x, cy - gap + 10),
                      stroke="#fbbf24", stroke_width=2))
    dwg.add(dwg.text("MAIN DC", insert=(conduit_x + 3, start_y + 15),
                      fill="#fbbf24", font_size=6, font_family="Arial"))
    dwg.add(dwg.text("CONDUIT", insert=(conduit_x + 3, start_y + 23),
                      fill="#fbbf24", font_size=6, font_family="Arial"))

    # ================================================================
    # RIGHT SIDE: ELECTRICAL EQUIPMENT
    # ================================================================
    eq_x = 760

    # String combiner panel
    box(dwg, eq_x, 100, 180, 60, "STRING COMBINER\nPANEL\n746 strings x 5 panels", "Fused inputs | Monitoring",
        border="#fbbf24", text_color="#fbbf24")

    # DC-DC Converter
    dwg.add(dwg.line((eq_x + 90, 160), (eq_x + 90, 200), stroke="#fbbf24", stroke_width=1.5))
    box(dwg, eq_x, 200, 180, 60, "DC-DC BUCK\nCONVERTER\n952V -> 800V DC", "97% efficiency | MPPT tracking",
        border="#fbbf24", text_color="#fbbf24")

    # To 800V bus
    dwg.add(dwg.line((eq_x + 90, 260), (eq_x + 90, 310), stroke="#8b5cf6", stroke_width=2))
    box(dwg, eq_x, 310, 180, 50, "800V DC BUS\n(DSX Reference)", "Feeds directly to GPU racks",
        border="#8b5cf6", text_color="#c4b5fd")

    # AC sell-back path
    dwg.add(dwg.line((eq_x + 180, 230), (eq_x + 220, 230), stroke="#fbbf24", stroke_width=1,
                      stroke_dasharray="4,3"))
    box(dwg, eq_x + 220, 200, 150, 60, "INVERTER\n(SELL-BACK PATH)\nDC -> AC -> LUS Grid\nLayer 4 revenue",
        "", border="#ef4444", text_color="#ef4444")

    # ================================================================
    # STRING / ARRAY MATH
    # ================================================================
    math_x = 760
    math_y = 400
    dwg.add(dwg.rect((math_x, math_y), (600, 160), rx=6, fill="#111318", stroke="#1e2230"))
    dwg.add(dwg.text("DC-DIRECT ARRAY MATH — TRAPPEYS ROOFTOP", insert=(math_x + 300, math_y + 18),
                      text_anchor="middle", fill="#fbbf24", font_size=10, font_family="Arial", font_weight="bold"))

    calcs = [
        ("Panel Model", "First Solar Series 7 TR1"),
        ("Rated Power", "550W per panel"),
        ("Vmp (max power voltage)", "190.4V"),
        ("Panels per String", "5 (series) = 952V Vmp"),
        ("Total Panels", "3,731"),
        ("Total Strings", "~746"),
        ("Total Capacity", "2.05 MW"),
        ("String Voltage", "952V (5 x 190.4V Vmp)"),
        ("Buck to Bus", "952V -> 800V DC"),
        ("Path Efficiency", "97% (vs 92% AC path)"),
        ("Annual Production", "~3,075 MWh (est)"),
        ("Distance to Factory", "30 miles (New Iberia)"),
    ]

    for i, (label, value) in enumerate(calcs):
        col = i % 2
        row = i // 2
        x_pos = math_x + 20 + col * 300
        y_pos = math_y + 35 + row * 20
        dwg.add(dwg.text(label, insert=(x_pos, y_pos), fill="#6b7280",
                          font_size=8, font_family="Arial"))
        dwg.add(dwg.text(value, insert=(x_pos + 160, y_pos), fill="#fbbf24",
                          font_size=8, font_family="Arial", font_weight="bold"))

    # ================================================================
    # PANEL SPECIFICATIONS
    # ================================================================
    spec_x = 50
    spec_y = 590
    dwg.add(dwg.rect((spec_x, spec_y), (600, 160), rx=6, fill="#111318", stroke="#1e2230"))
    dwg.add(dwg.text("FIRST SOLAR SERIES 7 TR1 — PANEL SPECIFICATIONS", insert=(spec_x + 300, spec_y + 18),
                      text_anchor="middle", fill="#fbbf24", font_size=10, font_family="Arial", font_weight="bold"))

    specs = [
        ("Panel Model", "First Solar Series 7 TR1"),
        ("Rated Power", "550W per panel"),
        ("Efficiency", "19.7% (CdTe thin-film)"),
        ("Dimensions", "~2.5m x 1.2m (8.2' x 3.9')"),
        ("Degradation Rate", "0.3%/year (industry best)"),
        ("Warranty", "30-year manufacturer warranty"),
        ("Manufacturing", "New Iberia, LA ($1.1B factory)"),
        ("Distance to Site", "~30 miles"),
        ("Temperature Coefficient", "-0.28%/C (superior in heat)"),
        ("Humidity Performance", "CdTe outperforms Si in humidity"),
    ]

    for i, (label, value) in enumerate(specs):
        col = i % 2
        row = i // 2
        x_pos = spec_x + 20 + col * 300
        y_pos = spec_y + 35 + row * 22
        dwg.add(dwg.text(label, insert=(x_pos, y_pos), fill="#6b7280",
                          font_size=8, font_family="Arial"))
        dwg.add(dwg.text(value, insert=(x_pos + 150, y_pos), fill="#fbbf24",
                          font_size=8, font_family="Arial", font_weight="bold"))

    # ================================================================
    # BUILDING PANEL DISTRIBUTION TABLE
    # ================================================================
    tbl_x = 680
    tbl_y = 590
    dwg.add(dwg.rect((tbl_x, tbl_y), (680, 160), rx=6, fill="#111318", stroke="#1e2230"))
    dwg.add(dwg.text("PANEL DISTRIBUTION BY BUILDING", insert=(tbl_x + 340, tbl_y + 18),
                      text_anchor="middle", fill=ACCENT, font_size=10, font_family="Arial", font_weight="bold"))

    headers = ["BUILDING", "DIMENSIONS", "ROOF AREA", "PANELS", "CAPACITY", "STRINGS"]
    hx_pos = tbl_x + 15
    for h in headers:
        dwg.add(dwg.text(h, insert=(hx_pos, tbl_y + 38), fill="#6b7280",
                          font_size=7, font_family="Arial", font_weight="bold"))
        hx_pos += 110

    rows = [
        ("Front", "300' x 75'", "22,500 sf", "658", "362 kW", "~132"),
        ("Middle Low", "300' x 100'", "30,000 sf", "1,105", "608 kW", "~221"),
        ("Middle High", "300' x 75'", "22,500 sf", "658", "362 kW", "~132"),
        ("Rear High", "250' x 150'", "37,500 sf", "1,310", "721 kW", "~262"),
        ("TOTAL", "—", "112,500 sf", "3,731", "2.05 MW", "~746"),
    ]

    for r, row in enumerate(rows):
        ry = tbl_y + 55 + r * 18
        hx_pos = tbl_x + 15
        is_total = r == len(rows) - 1
        color = ACCENT if is_total else "#9ca3af"
        weight = "bold" if is_total else "normal"
        for val in row:
            dwg.add(dwg.text(val, insert=(hx_pos, ry), fill=color,
                              font_size=8, font_family="Arial", font_weight=weight))
            hx_pos += 110

    # ================================================================
    # DC-DIRECT vs AC PATH COMPARISON
    # ================================================================
    cmp_y = 770
    dwg.add(dwg.rect((50, cmp_y), (1300, 55), rx=6, fill="#111318", stroke="#1e2230"))

    dwg.add(dwg.text("DC-DIRECT PATH (OUR DESIGN):", insert=(70, cmp_y + 18), fill="#fbbf24",
                      font_size=9, font_family="Arial", font_weight="bold"))
    dc_path = "Panel (190V) -> String (952V) -> Buck DC-DC (800V) -> DSX Bus -> Rack PDU -> 64:1 LLC -> GPU"
    dwg.add(dwg.text(dc_path, insert=(70, cmp_y + 32), fill="#fbbf24", font_size=8, font_family="Arial"))
    dwg.add(dwg.text("Total Path Efficiency: 97%", insert=(70, cmp_y + 45), fill="#76b900",
                      font_size=9, font_family="Arial", font_weight="bold"))

    dwg.add(dwg.text("TRADITIONAL AC PATH:", insert=(720, cmp_y + 18), fill="#555",
                      font_size=9, font_family="Arial", font_weight="bold"))
    ac_path = "Panel -> Inverter (DC-AC) -> Transformer -> UPS -> PDU -> PSU (AC-DC) -> GPU"
    dwg.add(dwg.text(ac_path, insert=(720, cmp_y + 32), fill="#555", font_size=8, font_family="Arial"))
    dwg.add(dwg.text("Total Path Efficiency: 88-92%", insert=(720, cmp_y + 45), fill="#ef4444",
                      font_size=9, font_family="Arial", font_weight="bold"))

    # ================================================================
    # NOTES
    # ================================================================
    ny = 845
    notes = [
        "1. First Solar Series 7 TR1 panels manufactured in New Iberia, LA — $1.1B factory, 30 miles from Trappeys campus",
        "2. CdTe thin-film technology outperforms silicon in Louisiana's heat and humidity — superior temperature coefficient (-0.28%/C)",
        "3. 5-panel strings at 952V Vmp, buck-converted to 800V for direct feed into NVIDIA DSX bus — no AC conversion needed",
        "4. DC-Direct path saves 5-9% efficiency vs traditional AC path — at 2.05 MW, that's 100-185 kW saved continuously",
        "5. 0.3%/year degradation is industry best — after 30 years, panels still produce 91% of original capacity",
        "6. Rooftop mount = no additional land required. All 4 buildings utilized. 112,500 sq ft total roof area.",
        "7. Panel counts per building are proportional estimates based on usable roof area (~80% coverage factor)",
        "8. Made in America: First Solar is the only major US-headquartered solar manufacturer. Louisiana supply chain.",
        "9. Excess solar production sold back to LUS (Layer 4) via AC inverter path — additional revenue stream",
        "10. Annual production ~3,075 MWh estimated based on Louisiana solar resource (4.5-5.2 kWh/m2/day, 15% losses)",
    ]
    for i, note in enumerate(notes):
        dwg.add(dwg.text(note, insert=(35, ny + i * 13), fill="#4b5563",
                          font_size=7, font_family="Arial"))

    dwg.save()
    print(f"Saved: {OUT}")


if __name__ == "__main__":
    import os
    os.makedirs("adc3k-deploy/blueprints", exist_ok=True)
    build()
