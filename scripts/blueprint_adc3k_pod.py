#!/usr/bin/env python3
"""ADC Pure DC AI Cassette — 40-ft AI Compute Module Blueprint (P-001 Rev B)
4-view engineering drawing: Top, Side, End, Schematic.
Output: adc3k-deploy/blueprints/adc3k-pod-layout.svg
"""

import svgwrite
from pathlib import Path

# --- Colors ---
BG = "#0a0b0f"
GREEN = "#00e87a"
GREEN_DIM = "#00a855"
BLUE = "#00b4d8"
BLUE_DIM = "#0077b6"
RED = "#ff4444"
RED_DIM = "#cc3333"
PURPLE = "#b44aff"
PURPLE_DIM = "#8833cc"
WHITE = "#e0e0e0"
GRAY = "#555555"
GRAY_DIM = "#333333"
YELLOW = "#ffd60a"
ORANGE = "#ff8c00"
CYAN = "#00e5ff"

OUT = Path(__file__).resolve().parent.parent / "adc3k-deploy" / "adc3k-pod" / "blueprints" / "adc3k-pod-layout.svg"

W, H = 1800, 2800

def draw_title_block(dwg, g):
    """Title block at bottom of drawing."""
    y0 = H - 130
    g.add(dwg.line((30, y0), (W - 30, y0), stroke=GREEN, stroke_width=2))
    g.add(dwg.line((30, y0 + 2), (W - 30, y0 + 2), stroke=GREEN_DIM, stroke_width=0.5))

    col1 = 50
    col2 = 900
    col3 = 1400

    g.add(dwg.text("ADC 3K POD — 40-FT AI COMPUTE MODULE", insert=(col1, y0 + 24),
                    fill=GREEN, font_size="18px", font_family="monospace", font_weight="bold"))
    g.add(dwg.text("10x NVIDIA NVL72 (GB200/Vera Rubin) | 720 GPUs | 1 SuperPOD + Network + Storage",
                    insert=(col1, y0 + 44), fill=WHITE, font_size="12px", font_family="monospace"))
    g.add(dwg.text("Eaton Beam Rubin 800V DC | Delta 660 kW Rack | CoolIT CHx2000 + Delta 140 kW CDU | First Solar | Jetson AGX Orin",
                    insert=(col1, y0 + 60), fill=WHITE, font_size="12px", font_family="monospace"))
    g.add(dwg.text("PRELIMINARY DESIGN — NOT FOR CONSTRUCTION",
                    insert=(col1, y0 + 80), fill=RED, font_size="11px", font_family="monospace", font_weight="bold"))
    g.add(dwg.text("Advantage Design & Construction | adc3k.com | Lafayette, Louisiana",
                    insert=(col1, y0 + 96), fill=GRAY, font_size="10px", font_family="monospace"))

    g.add(dwg.text("Sheet: P-001 Rev B", insert=(col2, y0 + 24), fill=WHITE, font_size="12px", font_family="monospace"))
    g.add(dwg.text("Date: 2026-03-24", insert=(col2, y0 + 44), fill=WHITE, font_size="12px", font_family="monospace"))
    g.add(dwg.text("Scale: NOT TO SCALE", insert=(col2, y0 + 60), fill=GRAY, font_size="10px", font_family="monospace"))
    g.add(dwg.text("Drawn: Mission Control", insert=(col2, y0 + 80), fill=GRAY, font_size="10px", font_family="monospace"))

    g.add(dwg.text("ADC", insert=(col3, y0 + 40), fill=GREEN, font_size="36px",
                    font_family="monospace", font_weight="bold"))
    g.add(dwg.text("3K", insert=(col3 + 120, y0 + 40), fill=WHITE, font_size="36px",
                    font_family="monospace", font_weight="bold"))


def draw_notes(dwg, g):
    """Engineering notes above title block."""
    y0 = H - 260
    g.add(dwg.text("ENGINEERING NOTES", insert=(50, y0), fill=GREEN, font_size="11px",
                    font_family="monospace", font_weight="bold"))
    notes = [
        "1. Racks: NVIDIA NVL72 (GB200/Vera Rubin). Height 88\" (Supermicro). HPE spec 98.2\" — VERIFY.",
        "2. Power: Eaton Beam Rubin DSX 800V DC + Delta 660 kW Power Rack (480 kW BBU, e-Fuse SiC <3us, 90 kW DC/DC 800V->50V MGX).",
        "3. Cooling: CoolIT CHx2000 (2,000 kW) row CDU + Delta 140 kW In-Rack CDU (4RU, NVL72 cert). Staubli UQD. N+1.",
        "4. Heat rejection: BAC TrilliumSeries Adiabatic (external). 1.3 MW capacity. Adiabatic assist >95F.",
        "5. Solar roof: First Solar Series 7 TR1 (6 kW). Dehumidifier: Munters HCD. Exhaust: Greenheck SBE-300.",
        "6. Fire suppression: Ansul Novec 1230. Smoke detection: VESDA-E VEU aspirating.",
        "7. Networking: NVIDIA Quantum-X800 InfiniBand. Controller: NVIDIA Jetson AGX Orin. 65 AI sensors.",
        "8. Zero on-site staff. Remote NOC at MARLIE 1. All service from exterior access panels.",
    ]
    for i, note in enumerate(notes):
        g.add(dwg.text(note, insert=(50, y0 + 16 + i * 14), fill=GRAY, font_size="9px", font_family="monospace"))


# =====================================================================
# VIEW 1: TOP VIEW
# =====================================================================
def draw_top_view(dwg, g):
    """Top view — bird's eye of container layout."""
    ox, oy = 80, 60
    label_y = oy - 8

    g.add(dwg.text("VIEW 1 — TOP VIEW (BIRD'S EYE)", insert=(ox, label_y),
                    fill=GREEN, font_size="13px", font_family="monospace", font_weight="bold"))

    # Container outline — proportional
    # Real: 39'5" x 7'8.6" -> use scale ~38px per foot
    # Length 39.45ft -> 1500px, Width 7.72ft -> 200px
    cw = 1500
    ch = 200
    cx, cy = ox + 60, oy + 20

    # Solar hatching (roof) — draw first so container outline is on top
    for sx in range(0, cw, 20):
        g.add(dwg.line((cx + sx, cy), (cx + sx + 10, cy + ch),
                        stroke=YELLOW, stroke_width=0.3, opacity=0.2))

    # Container outline
    g.add(dwg.rect((cx, cy), (cw, ch), fill="none", stroke=GREEN, stroke_width=2))

    # Door end indicator (left side)
    g.add(dwg.line((cx, cy), (cx, cy + ch), stroke=WHITE, stroke_width=3))
    g.add(dwg.text("DOOR", insert=(cx - 5, cy + ch + 14), fill=WHITE, font_size="8px",
                    font_family="monospace", text_anchor="middle"))
    g.add(dwg.text("END", insert=(cx - 5, cy + ch + 24), fill=WHITE, font_size="8px",
                    font_family="monospace", text_anchor="middle"))

    # Closed end
    g.add(dwg.line((cx + cw, cy), (cx + cw, cy + ch), stroke=WHITE, stroke_width=3))
    g.add(dwg.text("CLOSED", insert=(cx + cw + 5, cy + ch + 14), fill=WHITE, font_size="8px",
                    font_family="monospace", text_anchor="middle"))
    g.add(dwg.text("END", insert=(cx + cw + 5, cy + ch + 24), fill=WHITE, font_size="8px",
                    font_family="monospace", text_anchor="middle"))

    # Zone proportions (in inches, total ~462 in used of 473.7)
    # Entry: 36in, Elec: 42in, Racks: 276in, Patch: 36in, CDU: 72in -> 462in
    total_in = 462.0
    def ix(inches):
        return cx + (inches / total_in) * cw

    # Zone boundaries
    entry_end = 36
    elec_end = 36 + 42
    racks_start = elec_end
    racks_end = elec_end + 276
    patch_end = racks_end + 36
    cdu_start = patch_end

    # Zone dividers
    for boundary in [entry_end, elec_end, racks_end, patch_end]:
        x = ix(boundary)
        g.add(dwg.line((x, cy), (x, cy + ch), stroke=GRAY, stroke_width=1, stroke_dasharray="4,4"))

    # Zone labels (above container)
    zones = [
        (0, entry_end, "ENTRY\nZONE", "36\""),
        (entry_end, elec_end, "ELEC\nPANEL", "42\""),
        (racks_start, racks_end, "RACK ZONE (10 RACKS)", "276\""),
        (racks_end, patch_end, "PATCH\nPANEL", "36\""),
        (patch_end, total_in, "CDU\nZONE", "72\""),
    ]
    for z_start, z_end, label, dim in zones:
        mid = ix((z_start + z_end) / 2)
        lines = label.split("\n")
        for li, line in enumerate(lines):
            g.add(dwg.text(line, insert=(mid, cy - 14 + li * 10), fill=WHITE, font_size="8px",
                            font_family="monospace", text_anchor="middle"))

    # Dimension lines below container
    dim_y = cy + ch + 40
    # Overall dimension
    g.add(dwg.line((cx, dim_y), (cx + cw, dim_y), stroke=GRAY, stroke_width=0.5))
    g.add(dwg.line((cx, dim_y - 5), (cx, dim_y + 5), stroke=GRAY, stroke_width=0.5))
    g.add(dwg.line((cx + cw, dim_y - 5), (cx + cw, dim_y + 5), stroke=GRAY, stroke_width=0.5))
    g.add(dwg.text("39'-5\" (12,032 mm)", insert=(cx + cw / 2, dim_y - 4),
                    fill=WHITE, font_size="9px", font_family="monospace", text_anchor="middle"))

    # Width dimension (right side)
    wd_x = cx + cw + 30
    g.add(dwg.line((wd_x, cy), (wd_x, cy + ch), stroke=GRAY, stroke_width=0.5))
    g.add(dwg.line((wd_x - 5, cy), (wd_x + 5, cy), stroke=GRAY, stroke_width=0.5))
    g.add(dwg.line((wd_x - 5, cy + ch), (wd_x + 5, cy + ch), stroke=GRAY, stroke_width=0.5))
    g.add(dwg.text("7'-8.6\"", insert=(wd_x + 8, cy + ch / 2 + 3), fill=WHITE, font_size="8px",
                    font_family="monospace"))

    # --- RACKS (center row) ---
    rack_w_in = 23.6
    rack_d_in = 42.0
    gap_in = 4.0
    container_w_in = 92.6
    side_clearance = (container_w_in - rack_d_in) / 2  # 25.3"

    # Scale within container
    def iy(inches_from_top_wall):
        return cy + (inches_from_top_wall / container_w_in) * ch

    rack_top_y = iy(side_clearance)
    rack_bot_y = iy(side_clearance + rack_d_in)
    rack_h_px = rack_bot_y - rack_top_y

    rack_names = ["R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10"]
    rack_colors = [GREEN] * 8 + [BLUE, PURPLE]
    rack_fill = [GREEN_DIM] * 8 + [BLUE_DIM, PURPLE_DIM]

    for i in range(10):
        rack_start_in = racks_start + i * (rack_w_in + gap_in)
        rx = ix(rack_start_in)
        rw = (rack_w_in / total_in) * cw

        g.add(dwg.rect((rx, rack_top_y), (rw, rack_h_px),
                        fill=rack_fill[i], fill_opacity=0.25, stroke=rack_colors[i], stroke_width=1.5))
        g.add(dwg.text(rack_names[i], insert=(rx + rw / 2, rack_top_y + rack_h_px / 2 + 3),
                        fill=rack_colors[i], font_size="9px", font_family="monospace",
                        text_anchor="middle", font_weight="bold"))

    # --- FLOOR CABLE TRAYS (dashed lines along both walls) ---
    tray_offset = 8  # px from wall
    tray_start_x = ix(entry_end)
    tray_end_x = ix(racks_end + 20)
    # Top wall tray
    g.add(dwg.line((tray_start_x, cy + tray_offset), (tray_end_x, cy + tray_offset),
                    stroke=ORANGE, stroke_width=2, stroke_dasharray="8,4"))
    # Bottom wall tray
    g.add(dwg.line((tray_start_x, cy + ch - tray_offset), (tray_end_x, cy + ch - tray_offset),
                    stroke=ORANGE, stroke_width=2, stroke_dasharray="8,4"))

    # Cable tray labels
    g.add(dwg.text("FLOOR CABLE TRAY", insert=(tray_start_x - 2, cy + tray_offset - 3),
                    fill=ORANGE, font_size="6px", font_family="monospace"))
    g.add(dwg.text("FLOOR CABLE TRAY", insert=(tray_start_x - 2, cy + ch - tray_offset + 9),
                    fill=ORANGE, font_size="6px", font_family="monospace"))

    # --- COOLING PIPES (blue dashed on floor, from CDU to racks) ---
    pipe_y_top = cy + tray_offset + 6
    pipe_y_bot = cy + ch - tray_offset - 6
    pipe_start = ix(racks_start - 5)
    pipe_end = ix(total_in - 10)
    # Supply (blue)
    g.add(dwg.line((pipe_start, pipe_y_top), (pipe_end, pipe_y_top),
                    stroke=BLUE, stroke_width=1.5, stroke_dasharray="6,3"))
    # Return (red)
    g.add(dwg.line((pipe_start, pipe_y_bot), (pipe_end, pipe_y_bot),
                    stroke=RED, stroke_width=1.5, stroke_dasharray="6,3"))
    g.add(dwg.text("SUPPLY 45C", insert=(pipe_end + 4, pipe_y_top + 3),
                    fill=BLUE, font_size="5px", font_family="monospace"))
    g.add(dwg.text("RETURN 55C", insert=(pipe_end + 4, pipe_y_bot + 3),
                    fill=RED, font_size="5px", font_family="monospace"))

    # --- POWER BUS (red line from elec panel along floor) ---
    pwr_y = cy + ch / 2 - 15
    g.add(dwg.line((ix(entry_end + 5), pwr_y), (ix(racks_end), pwr_y),
                    stroke=RED, stroke_width=2))
    g.add(dwg.text("800V DC BUS (FLOOR)", insert=(ix(entry_end + 60), pwr_y - 4),
                    fill=RED, font_size="6px", font_family="monospace"))

    # --- ACCESS PANELS (4 per side, 8 total) ---
    ap_width_in = (racks_end - racks_start) / 4  # ~69" each
    for side in range(2):
        for ap in range(4):
            ap_start = racks_start + ap * ap_width_in
            ap_x = ix(ap_start)
            ap_w = (ap_width_in / total_in) * cw
            if side == 0:
                ap_y = cy - 2
                ap_h = 6
            else:
                ap_y = cy + ch - 4
                ap_h = 6
            g.add(dwg.rect((ap_x, ap_y), (ap_w, ap_h),
                            fill="none", stroke=YELLOW, stroke_width=1, stroke_dasharray="3,2"))
            label_num = ap + 1 + side * 4
            lx = ap_x + ap_w / 2
            ly = ap_y - 3 if side == 0 else ap_y + ap_h + 8
            g.add(dwg.text(f"AP-{label_num}", insert=(lx, ly), fill=YELLOW, font_size="6px",
                            font_family="monospace", text_anchor="middle"))

    # --- ELECTRICAL PANEL icon ---
    ep_x = ix(entry_end + 10)
    ep_y = cy + ch / 2 - 8
    g.add(dwg.rect((ep_x, ep_y), (20, 16), fill=RED_DIM, fill_opacity=0.4, stroke=RED, stroke_width=1))
    g.add(dwg.text("EP", insert=(ep_x + 10, ep_y + 11), fill=RED, font_size="7px",
                    font_family="monospace", text_anchor="middle"))

    # --- CDU icon ---
    cdu_x = ix(cdu_start + 10)
    cdu_y = cy + ch / 2 - 12
    g.add(dwg.rect((cdu_x, cdu_y), (35, 24), fill=BLUE_DIM, fill_opacity=0.3, stroke=BLUE, stroke_width=1))
    g.add(dwg.text("CDU", insert=(cdu_x + 17, cdu_y + 15), fill=BLUE, font_size="8px",
                    font_family="monospace", text_anchor="middle"))

    # --- DEHUMIDIFIER icon ---
    dh_x = ix(entry_end + 30)
    dh_y = cy + ch - 25
    g.add(dwg.rect((dh_x, dh_y), (14, 10), fill="none", stroke=CYAN, stroke_width=1))
    g.add(dwg.text("DH", insert=(dh_x + 7, dh_y + 8), fill=CYAN, font_size="5px",
                    font_family="monospace", text_anchor="middle"))

    # --- EXHAUST FAN (circle at closed end) ---
    fan_x = ix(total_in - 20)
    fan_y = cy + 18
    g.add(dwg.circle((fan_x, fan_y), 8, fill="none", stroke=CYAN, stroke_width=1))
    g.add(dwg.text("FAN", insert=(fan_x, fan_y + 3), fill=CYAN, font_size="5px",
                    font_family="monospace", text_anchor="middle"))

    # --- SENSORS ---
    sensor_positions = [
        (racks_start + 30, "T1"), (racks_start + 100, "T2"),
        (racks_start + 180, "T3"), (racks_start + 250, "T4"),
    ]
    for s_in, label in sensor_positions:
        sx = ix(s_in)
        g.add(dwg.circle((sx, cy + ch / 2 + 15), 3, fill="none", stroke=YELLOW, stroke_width=0.8))
        g.add(dwg.text(label, insert=(sx, cy + ch / 2 + 18), fill=YELLOW, font_size="4px",
                        font_family="monospace", text_anchor="middle"))

    # Humidity sensors
    for h_in, label in [(entry_end + 20, "H1"), (cdu_start + 20, "H2")]:
        hx = ix(h_in)
        g.add(dwg.circle((hx, cy + 20), 3, fill="none", stroke=CYAN, stroke_width=0.8))
        g.add(dwg.text(label, insert=(hx, cy + 17), fill=CYAN, font_size="4px",
                        font_family="monospace", text_anchor="middle"))

    # Cameras
    for c_in, label in [(10, "CAM-1"), (total_in - 10, "CAM-2")]:
        camx = ix(c_in)
        g.add(dwg.polygon([(camx - 4, cy + ch / 2 - 3), (camx + 4, cy + ch / 2 - 3),
                            (camx + 6, cy + ch / 2), (camx + 4, cy + ch / 2 + 3),
                            (camx - 4, cy + ch / 2 + 3), (camx - 6, cy + ch / 2)],
                           fill="none", stroke=WHITE, stroke_width=0.8))
        g.add(dwg.text(label, insert=(camx, cy + ch / 2 + 12), fill=WHITE, font_size="5px",
                        font_family="monospace", text_anchor="middle"))

    # Solar panel label
    g.add(dwg.text("FIRST SOLAR SERIES 7 TR1 ON ROOF (hatched)", insert=(cx + 10, cy + ch + 58),
                    fill=YELLOW, font_size="7px", font_family="monospace"))

    # Side clearance dimensions
    # Top side
    g.add(dwg.line((cx + 2, cy + 4), (cx + 2, rack_top_y), stroke=GRAY_DIM, stroke_width=0.5))
    g.add(dwg.text("25.3\"", insert=(cx + 5, (cy + rack_top_y) / 2 + 3), fill=GRAY, font_size="6px",
                    font_family="monospace"))
    # Bottom side
    g.add(dwg.line((cx + 2, rack_bot_y), (cx + 2, cy + ch - 4), stroke=GRAY_DIM, stroke_width=0.5))
    g.add(dwg.text("25.3\"", insert=(cx + 5, (rack_bot_y + cy + ch) / 2 + 3), fill=GRAY, font_size="6px",
                    font_family="monospace"))

    # Legend
    leg_x = cx + cw + 60
    leg_y = cy + 10
    g.add(dwg.text("LEGEND", insert=(leg_x, leg_y), fill=GREEN, font_size="9px",
                    font_family="monospace", font_weight="bold"))
    legend_items = [
        (GREEN, "R1-R8 NVIDIA NVL72 Compute"),
        (BLUE, "R9 Quantum-X800 InfiniBand"),
        (PURPLE, "R10 Storage + Mgmt"),
        (ORANGE, "Floor Cable Tray"),
        (RED, "Eaton Beam Rubin 800V DC"),
        (BLUE, "CoolIT CHx2000 Supply (45C)"),
        (RED_DIM, "CoolIT CHx2000 Return (55C)"),
        (YELLOW, "Access Panels (AP)"),
        (CYAN, "Munters HCD / Greenheck SBE"),
    ]
    for i, (color, text) in enumerate(legend_items):
        ly = leg_y + 14 + i * 13
        g.add(dwg.rect((leg_x, ly - 6), (8, 8), fill=color, fill_opacity=0.5))
        g.add(dwg.text(text, insert=(leg_x + 12, ly + 1), fill=WHITE, font_size="7px",
                        font_family="monospace"))

    # Rack type labels
    g.add(dwg.text("R1-R8: NVIDIA NVL72 (72 GPUs each) | R9: Quantum-X800 InfiniBand | R10: STORAGE + MGMT",
                    insert=(cx, dim_y + 14), fill=GRAY, font_size="7px", font_family="monospace"))


# =====================================================================
# VIEW 2: LONG SIDE VIEW (Elevation)
# =====================================================================
def draw_side_view(dwg, g):
    """Side elevation — looking through open access panels."""
    ox, oy = 80, 370
    g.add(dwg.text("VIEW 2 — LONG SIDE ELEVATION (LOOKING THROUGH OPEN ACCESS PANELS)",
                    insert=(ox, oy - 8), fill=GREEN, font_size="13px", font_family="monospace", font_weight="bold"))

    # Container profile: 39'5" long x 8'10" tall
    cw = 1500
    ch = 260
    cx, cy = ox + 60, oy + 15

    # Container walls
    g.add(dwg.rect((cx, cy), (cw, ch), fill="none", stroke=GREEN, stroke_width=2))

    # Corrugated wall texture (vertical lines)
    for wx in range(0, cw, 12):
        g.add(dwg.line((cx + wx, cy), (cx + wx, cy + ch), stroke=GRAY_DIM, stroke_width=0.3))

    # Solar panels on roof (angled slightly)
    solar_h = 10
    for sx in range(0, cw, 40):
        sw = min(38, cw - sx)
        pts = [(cx + sx + 1, cy - 2), (cx + sx + sw, cy - 4),
               (cx + sx + sw, cy - 4 - solar_h), (cx + sx + 1, cy - 2 - solar_h)]
        g.add(dwg.polygon(pts, fill=YELLOW, fill_opacity=0.15, stroke=YELLOW, stroke_width=0.5))
    g.add(dwg.text("FIRST SOLAR SERIES 7 TR1 (6 kW, shade + power)", insert=(cx + 10, cy - solar_h - 6),
                    fill=YELLOW, font_size="7px", font_family="monospace"))

    # Zone proportions (same as top view)
    total_in = 462.0
    def ix(inches):
        return cx + (inches / total_in) * cw
    def iy_h(inches, total_h=106.2):
        """Convert inches from floor to pixel y (bottom = floor)."""
        return cy + ch - (inches / total_h) * ch

    entry_end = 36
    elec_end = 78
    racks_start = elec_end
    racks_end = elec_end + 276
    patch_end = racks_end + 36
    cdu_start = patch_end

    # Floor line
    floor_y = cy + ch
    g.add(dwg.line((cx, floor_y), (cx + cw, floor_y), stroke=WHITE, stroke_width=2))

    # --- FLOOR CABLE TRAYS ---
    tray_h = 8
    tray_y = floor_y - tray_h
    g.add(dwg.rect((ix(elec_end), tray_y), (ix(racks_end + 10) - ix(elec_end), tray_h),
                    fill=ORANGE, fill_opacity=0.2, stroke=ORANGE, stroke_width=1, stroke_dasharray="4,2"))
    g.add(dwg.text("FLOOR CABLE TRAY", insert=(ix(racks_start + 20), tray_y + 6),
                    fill=ORANGE, font_size="6px", font_family="monospace"))

    # Optional grating
    for gx in range(int(ix(elec_end)), int(ix(racks_end + 10)), 8):
        g.add(dwg.line((gx, tray_y), (gx + 4, tray_y - 3), stroke=ORANGE, stroke_width=0.3))
    g.add(dwg.text("(optional grating)", insert=(ix(racks_start + 100), tray_y - 4),
                    fill=ORANGE, font_size="5px", font_family="monospace"))

    # --- COOLING PIPES ON FLOOR ---
    pipe_y = tray_y - 5
    g.add(dwg.line((ix(racks_start), pipe_y), (ix(total_in - 10), pipe_y),
                    stroke=BLUE, stroke_width=1.5, stroke_dasharray="5,3"))
    g.add(dwg.line((ix(racks_start), pipe_y - 4), (ix(total_in - 10), pipe_y - 4),
                    stroke=RED, stroke_width=1.5, stroke_dasharray="5,3"))
    g.add(dwg.text("SUPPLY 45C", insert=(ix(total_in - 50), pipe_y + 3),
                    fill=BLUE, font_size="5px", font_family="monospace"))
    g.add(dwg.text("RETURN 55C", insert=(ix(total_in - 50), pipe_y - 5),
                    fill=RED, font_size="5px", font_family="monospace"))

    # --- RACKS ---
    rack_w_in = 23.6
    gap_in = 4.0
    rack_height_in = 88.0
    rack_top = iy_h(rack_height_in)
    rack_bottom = floor_y - tray_h

    for i in range(10):
        r_start = racks_start + i * (rack_w_in + gap_in)
        rx = ix(r_start)
        rw = (rack_w_in / total_in) * cw
        color = GREEN if i < 8 else (BLUE if i == 8 else PURPLE)
        dim_color = GREEN_DIM if i < 8 else (BLUE_DIM if i == 8 else PURPLE_DIM)

        g.add(dwg.rect((rx, rack_top), (rw, rack_bottom - rack_top),
                        fill=dim_color, fill_opacity=0.2, stroke=color, stroke_width=1.2))

        # 98" dashed option line
        rack_98_top = iy_h(98.2)
        g.add(dwg.line((rx, rack_98_top), (rx + rw, rack_98_top),
                        stroke=color, stroke_width=0.5, stroke_dasharray="2,2"))

        # Label
        g.add(dwg.text(f"R{i+1}", insert=(rx + rw / 2, rack_top + 12), fill=color, font_size="7px",
                        font_family="monospace", text_anchor="middle", font_weight="bold"))

    # 88" and 98" dimension labels
    dim_x = ix(racks_start) - 8
    g.add(dwg.line((dim_x, rack_top), (dim_x, rack_bottom), stroke=GRAY, stroke_width=0.5))
    g.add(dwg.text("88\"", insert=(dim_x - 18, (rack_top + rack_bottom) / 2 + 3), fill=WHITE,
                    font_size="7px", font_family="monospace"))
    g.add(dwg.text("98\"", insert=(dim_x - 18, (iy_h(98.2) + rack_bottom) / 2 + 3), fill=GRAY,
                    font_size="6px", font_family="monospace"))
    g.add(dwg.text("(HPE)", insert=(dim_x - 22, (iy_h(98.2) + rack_bottom) / 2 + 12), fill=GRAY,
                    font_size="5px", font_family="monospace"))

    # --- ACCESS PANELS (4, shown open -- hinged at top, propped out) ---
    ap_width_in = (racks_end - racks_start) / 4
    for ap in range(4):
        ap_start = racks_start + ap * ap_width_in
        ap_x = ix(ap_start)
        ap_w = (ap_width_in / total_in) * cw
        # Panel shown swung out from top hinge
        hinge_y = cy + 8
        panel_end_y = cy + ch * 0.55
        panel_out = 40
        # Panel body (hinged at top, swung out)
        pts = [
            (ap_x + 4, hinge_y),
            (ap_x + ap_w - 4, hinge_y),
            (ap_x + ap_w - 4 + panel_out, panel_end_y),
            (ap_x + 4 + panel_out, panel_end_y),
        ]
        g.add(dwg.polygon(pts, fill=YELLOW, fill_opacity=0.08, stroke=YELLOW, stroke_width=0.8))
        # Hinge indicator
        g.add(dwg.line((ap_x + 4, hinge_y), (ap_x + ap_w - 4, hinge_y),
                        stroke=YELLOW, stroke_width=1.5))
        # Prop leg
        g.add(dwg.line((ap_x + ap_w / 2 + panel_out, panel_end_y),
                        (ap_x + ap_w / 2 + panel_out * 0.7, floor_y),
                        stroke=YELLOW, stroke_width=0.5, stroke_dasharray="3,2"))
        # Label
        g.add(dwg.text(f"AP-{ap+1}", insert=(ap_x + ap_w / 2 + panel_out / 2, panel_end_y + 10),
                        fill=YELLOW, font_size="6px", font_family="monospace", text_anchor="middle"))

    # --- TECHNICIAN SILHOUETTE ---
    tech_x = ix(racks_start + ap_width_in * 1.5) + 45
    head_y = cy + ch * 0.35
    g.add(dwg.circle((tech_x, head_y), 6, fill="none", stroke=WHITE, stroke_width=0.8))
    g.add(dwg.line((tech_x, head_y + 6), (tech_x, head_y + 35), stroke=WHITE, stroke_width=0.8))
    g.add(dwg.line((tech_x, head_y + 35), (tech_x - 8, floor_y + 15), stroke=WHITE, stroke_width=0.8))
    g.add(dwg.line((tech_x, head_y + 35), (tech_x + 8, floor_y + 15), stroke=WHITE, stroke_width=0.8))
    g.add(dwg.line((tech_x, head_y + 14), (tech_x - 20, head_y + 8), stroke=WHITE, stroke_width=0.8))
    g.add(dwg.line((tech_x, head_y + 14), (tech_x - 22, head_y + 20), stroke=WHITE, stroke_width=0.8))
    g.add(dwg.text("TECH", insert=(tech_x + 10, head_y + 20), fill=GRAY, font_size="5px",
                    font_family="monospace"))

    # --- ELECTRICAL PANEL ---
    ep_x = ix(entry_end + 10)
    ep_w = 25
    ep_h = ch * 0.5
    ep_y = cy + ch * 0.2
    g.add(dwg.rect((ep_x, ep_y), (ep_w, ep_h), fill=RED_DIM, fill_opacity=0.2, stroke=RED, stroke_width=1))
    g.add(dwg.text("ELEC", insert=(ep_x + ep_w / 2, ep_y + ep_h / 2 - 4), fill=RED, font_size="6px",
                    font_family="monospace", text_anchor="middle"))
    g.add(dwg.text("PANEL", insert=(ep_x + ep_w / 2, ep_y + ep_h / 2 + 6), fill=RED, font_size="6px",
                    font_family="monospace", text_anchor="middle"))

    # --- CDU ---
    cdu_x = ix(cdu_start + 8)
    cdu_w = 40
    cdu_h = ch * 0.55
    cdu_y = cy + ch * 0.2
    g.add(dwg.rect((cdu_x, cdu_y), (cdu_w, cdu_h), fill=BLUE_DIM, fill_opacity=0.2, stroke=BLUE, stroke_width=1))
    g.add(dwg.text("CDU", insert=(cdu_x + cdu_w / 2, cdu_y + cdu_h / 2 + 3), fill=BLUE, font_size="8px",
                    font_family="monospace", text_anchor="middle"))

    # External connection through wall
    wall_x = cx + cw
    g.add(dwg.line((cdu_x + cdu_w, cdu_y + cdu_h / 2), (wall_x + 30, cdu_y + cdu_h / 2),
                    stroke=BLUE, stroke_width=1.5))
    g.add(dwg.circle((wall_x, cdu_y + cdu_h / 2), 4, fill=BLUE_DIM, stroke=BLUE, stroke_width=1))
    g.add(dwg.text("WALL", insert=(wall_x - 2, cdu_y + cdu_h / 2 - 8), fill=GRAY, font_size="5px",
                    font_family="monospace", text_anchor="middle"))
    g.add(dwg.text("PENETRATION", insert=(wall_x - 2, cdu_y + cdu_h / 2 + 14), fill=GRAY, font_size="5px",
                    font_family="monospace", text_anchor="middle"))

    # External dry cooler
    dc_x = wall_x + 35
    dc_y = cdu_y + cdu_h / 2 - 20
    g.add(dwg.rect((dc_x, dc_y), (55, 40), fill="none", stroke=CYAN, stroke_width=1))
    g.add(dwg.text("BAC TRILLIUM", insert=(dc_x + 27, dc_y + 14), fill=CYAN, font_size="6px",
                    font_family="monospace", text_anchor="middle"))
    g.add(dwg.text("ADIABATIC", insert=(dc_x + 27, dc_y + 24), fill=CYAN, font_size="6px",
                    font_family="monospace", text_anchor="middle"))
    g.add(dwg.text("1.3 MW", insert=(dc_x + 27, dc_y + 34), fill=CYAN, font_size="5px",
                    font_family="monospace", text_anchor="middle"))

    # --- DEHUMIDIFIER ---
    dh_x = ix(entry_end + 30)
    dh_y = floor_y - 18
    g.add(dwg.rect((dh_x, dh_y), (16, 12), fill="none", stroke=CYAN, stroke_width=0.8))
    g.add(dwg.text("DH", insert=(dh_x + 8, dh_y + 9), fill=CYAN, font_size="5px",
                    font_family="monospace", text_anchor="middle"))

    # --- EXHAUST FAN (near ceiling at closed end) ---
    fan_x = ix(total_in - 20)
    fan_y = cy + 15
    g.add(dwg.circle((fan_x, fan_y), 8, fill="none", stroke=CYAN, stroke_width=1))
    g.add(dwg.line((fan_x - 5, fan_y), (fan_x + 5, fan_y), stroke=CYAN, stroke_width=0.5))
    g.add(dwg.line((fan_x, fan_y - 5), (fan_x, fan_y + 5), stroke=CYAN, stroke_width=0.5))
    g.add(dwg.text("EXHAUST", insert=(fan_x, fan_y - 12), fill=CYAN, font_size="5px",
                    font_family="monospace", text_anchor="middle"))
    g.add(dwg.text("FAN", insert=(fan_x, fan_y - 5), fill=CYAN, font_size="5px",
                    font_family="monospace", text_anchor="middle"))

    # --- CAMERAS ---
    for c_in, label in [(8, "CAM-1"), (total_in - 15, "CAM-2")]:
        camx = ix(c_in)
        camy = cy + 20
        g.add(dwg.rect((camx - 5, camy), (10, 7), fill="none", stroke=WHITE, stroke_width=0.8))
        g.add(dwg.text(label, insert=(camx, camy + 15), fill=WHITE, font_size="5px",
                        font_family="monospace", text_anchor="middle"))

    # Dimension: container height
    ht_x = cx - 15
    g.add(dwg.line((ht_x, cy), (ht_x, cy + ch), stroke=GRAY, stroke_width=0.5))
    g.add(dwg.line((ht_x - 4, cy), (ht_x + 4, cy), stroke=GRAY, stroke_width=0.5))
    g.add(dwg.line((ht_x - 4, cy + ch), (ht_x + 4, cy + ch), stroke=GRAY, stroke_width=0.5))
    g.add(dwg.text("8'-10\"", insert=(ht_x - 28, cy + ch / 2 + 3), fill=WHITE, font_size="7px",
                    font_family="monospace"))

    # Door opening
    door_x = cx
    door_h = ch * 0.92
    door_y = cy + ch - door_h
    g.add(dwg.rect((door_x - 3, door_y), (6, door_h), fill="none", stroke=WHITE, stroke_width=1.5))
    g.add(dwg.text("DOOR", insert=(door_x - 25, door_y + door_h / 2), fill=WHITE, font_size="6px",
                    font_family="monospace"))


# =====================================================================
# VIEW 3: END VIEW (Cross-section)
# =====================================================================
def draw_end_view(dwg, g):
    """End view cross-section through rack zone."""
    ox, oy = 80, 710
    g.add(dwg.text("VIEW 3 — END VIEW (CROSS-SECTION THROUGH RACK ZONE)",
                    insert=(ox, oy - 8), fill=GREEN, font_size="13px", font_family="monospace", font_weight="bold"))

    # Container cross-section: 7'8.6" wide x 8'10" tall
    cw = 350
    ch = 400
    cx = ox + 200
    cy = oy + 15

    # Container outline
    g.add(dwg.rect((cx, cy), (cw, ch), fill="none", stroke=GREEN, stroke_width=2))

    # Corrugated wall texture
    for wy in range(0, ch, 10):
        g.add(dwg.line((cx, cy + wy), (cx + 6, cy + wy), stroke=GRAY_DIM, stroke_width=0.3))
        g.add(dwg.line((cx + cw - 6, cy + wy), (cx + cw, cy + wy), stroke=GRAY_DIM, stroke_width=0.3))

    # Solar panel on roof
    g.add(dwg.rect((cx - 5, cy - 12), (cw + 10, 10), fill=YELLOW, fill_opacity=0.15,
                    stroke=YELLOW, stroke_width=0.8))
    g.add(dwg.text("FIRST SOLAR SERIES 7 TR1", insert=(cx + cw / 2, cy - 16), fill=YELLOW, font_size="7px",
                    font_family="monospace", text_anchor="middle"))

    # Floor
    floor_y = cy + ch
    g.add(dwg.line((cx, floor_y), (cx + cw, floor_y), stroke=WHITE, stroke_width=2))

    # Scaling
    def sx(inches):
        return cx + (inches / 92.6) * cw
    def sy(inches_from_floor):
        return floor_y - (inches_from_floor / 106.2) * ch

    # Rack centered
    rack_left = sx(25.3)
    rack_right = sx(25.3 + 42.0)
    rack_top = sy(88.0)

    g.add(dwg.rect((rack_left, rack_top), (rack_right - rack_left, floor_y - rack_top),
                    fill=GREEN_DIM, fill_opacity=0.2, stroke=GREEN, stroke_width=1.5))
    g.add(dwg.text("NVIDIA NVL72", insert=((rack_left + rack_right) / 2, (rack_top + floor_y) / 2 - 14),
                    fill=GREEN, font_size="10px", font_family="monospace", text_anchor="middle"))
    g.add(dwg.text("(GB200/Vera Rubin)", insert=((rack_left + rack_right) / 2, (rack_top + floor_y) / 2 - 2),
                    fill=GREEN, font_size="7px", font_family="monospace", text_anchor="middle"))
    g.add(dwg.text("42\" deep x 23.6\" wide", insert=((rack_left + rack_right) / 2, (rack_top + floor_y) / 2 + 12),
                    fill=GREEN, font_size="7px", font_family="monospace", text_anchor="middle"))
    g.add(dwg.text("88\" tall", insert=((rack_left + rack_right) / 2, (rack_top + floor_y) / 2 + 24),
                    fill=GREEN, font_size="7px", font_family="monospace", text_anchor="middle"))

    # Cooling manifold connections on rack
    manifold_y = sy(30)
    g.add(dwg.circle((rack_left + 10, manifold_y), 4, fill=BLUE, fill_opacity=0.5, stroke=BLUE, stroke_width=1))
    g.add(dwg.circle((rack_right - 10, manifold_y), 4, fill=RED, fill_opacity=0.5, stroke=RED, stroke_width=1))
    g.add(dwg.text("S", insert=(rack_left + 10, manifold_y + 3), fill=WHITE, font_size="5px",
                    font_family="monospace", text_anchor="middle"))
    g.add(dwg.text("R", insert=(rack_right - 10, manifold_y + 3), fill=WHITE, font_size="5px",
                    font_family="monospace", text_anchor="middle"))
    g.add(dwg.text("MANIFOLD", insert=((rack_left + rack_right) / 2, manifold_y + 14),
                    fill=GRAY, font_size="5px", font_family="monospace", text_anchor="middle"))

    # Floor cable trays on both sides
    tray_h_px = 14
    tray_w_px = 30
    lt_x = sx(6)
    lt_y = floor_y - tray_h_px
    g.add(dwg.rect((lt_x, lt_y), (tray_w_px, tray_h_px), fill=ORANGE, fill_opacity=0.2,
                    stroke=ORANGE, stroke_width=1))
    g.add(dwg.text("CABLE", insert=(lt_x + tray_w_px / 2, lt_y + 6), fill=ORANGE, font_size="5px",
                    font_family="monospace", text_anchor="middle"))
    g.add(dwg.text("TRAY", insert=(lt_x + tray_w_px / 2, lt_y + 12), fill=ORANGE, font_size="5px",
                    font_family="monospace", text_anchor="middle"))
    rt_x = sx(92.6 - 6) - tray_w_px
    g.add(dwg.rect((rt_x, lt_y), (tray_w_px, tray_h_px), fill=ORANGE, fill_opacity=0.2,
                    stroke=ORANGE, stroke_width=1))
    g.add(dwg.text("CABLE", insert=(rt_x + tray_w_px / 2, lt_y + 6), fill=ORANGE, font_size="5px",
                    font_family="monospace", text_anchor="middle"))
    g.add(dwg.text("TRAY", insert=(rt_x + tray_w_px / 2, lt_y + 12), fill=ORANGE, font_size="5px",
                    font_family="monospace", text_anchor="middle"))

    # Cooling pipes on floor
    pipe_r = 4
    g.add(dwg.circle((lt_x + tray_w_px + 10, floor_y - pipe_r - 2), pipe_r,
                      fill=BLUE, fill_opacity=0.3, stroke=BLUE, stroke_width=0.8))
    g.add(dwg.circle((lt_x + tray_w_px + 22, floor_y - pipe_r - 2), pipe_r,
                      fill=RED, fill_opacity=0.3, stroke=RED, stroke_width=0.8))
    g.add(dwg.text("S  R", insert=(lt_x + tray_w_px + 10, floor_y - pipe_r - 8),
                    fill=GRAY, font_size="5px", font_family="monospace"))

    # Access panels on both walls (shown open)
    panel_h_px = ch * 0.75
    panel_top = cy + 20
    # Left panel
    g.add(dwg.rect((cx - 2, panel_top), (6, panel_h_px), fill="none", stroke=YELLOW, stroke_width=1.5))
    panel_out = 60
    pts = [(cx - 2, panel_top), (cx + 4, panel_top),
           (cx + 4 - panel_out, panel_top + panel_h_px * 0.6),
           (cx - 2 - panel_out, panel_top + panel_h_px * 0.6)]
    g.add(dwg.polygon(pts, fill=YELLOW, fill_opacity=0.06, stroke=YELLOW, stroke_width=0.6))
    g.add(dwg.text("ACCESS", insert=(cx - panel_out - 5, panel_top + panel_h_px * 0.3), fill=YELLOW,
                    font_size="7px", font_family="monospace"))
    g.add(dwg.text("PANEL", insert=(cx - panel_out - 5, panel_top + panel_h_px * 0.3 + 10), fill=YELLOW,
                    font_size="7px", font_family="monospace"))
    g.add(dwg.text("(OPEN)", insert=(cx - panel_out - 5, panel_top + panel_h_px * 0.3 + 20), fill=YELLOW,
                    font_size="6px", font_family="monospace"))

    # Right panel
    g.add(dwg.rect((cx + cw - 4, panel_top), (6, panel_h_px), fill="none", stroke=YELLOW, stroke_width=1.5))
    pts_r = [(cx + cw - 4, panel_top), (cx + cw + 2, panel_top),
             (cx + cw + 2 + panel_out, panel_top + panel_h_px * 0.6),
             (cx + cw - 4 + panel_out, panel_top + panel_h_px * 0.6)]
    g.add(dwg.polygon(pts_r, fill=YELLOW, fill_opacity=0.06, stroke=YELLOW, stroke_width=0.6))
    g.add(dwg.text("ACCESS", insert=(cx + cw + panel_out + 8, panel_top + panel_h_px * 0.3), fill=YELLOW,
                    font_size="7px", font_family="monospace"))
    g.add(dwg.text("PANEL", insert=(cx + cw + panel_out + 8, panel_top + panel_h_px * 0.3 + 10), fill=YELLOW,
                    font_size="7px", font_family="monospace"))
    g.add(dwg.text("(OPEN)", insert=(cx + cw + panel_out + 8, panel_top + panel_h_px * 0.3 + 20), fill=YELLOW,
                    font_size="6px", font_family="monospace"))

    # Dimensions
    dim_y = floor_y + 30
    g.add(dwg.line((cx, dim_y), (cx + cw, dim_y), stroke=GRAY, stroke_width=0.5))
    g.add(dwg.line((cx, dim_y - 5), (cx, dim_y + 5), stroke=GRAY, stroke_width=0.5))
    g.add(dwg.line((cx + cw, dim_y - 5), (cx + cw, dim_y + 5), stroke=GRAY, stroke_width=0.5))
    g.add(dwg.text("7'-8.6\" (2,352 mm)", insert=(cx + cw / 2, dim_y - 4), fill=WHITE, font_size="8px",
                    font_family="monospace", text_anchor="middle"))

    # Side clearances
    dim_y2 = dim_y + 18
    g.add(dwg.line((cx, dim_y2), (rack_left, dim_y2), stroke=GRAY, stroke_width=0.4))
    g.add(dwg.text("25.3\"", insert=((cx + rack_left) / 2, dim_y2 - 3), fill=WHITE, font_size="7px",
                    font_family="monospace", text_anchor="middle"))
    g.add(dwg.line((rack_left, dim_y2), (rack_right, dim_y2), stroke=GRAY, stroke_width=0.4))
    g.add(dwg.text("42.0\"", insert=((rack_left + rack_right) / 2, dim_y2 - 3), fill=WHITE, font_size="7px",
                    font_family="monospace", text_anchor="middle"))
    g.add(dwg.line((rack_right, dim_y2), (cx + cw, dim_y2), stroke=GRAY, stroke_width=0.4))
    g.add(dwg.text("25.3\"", insert=((rack_right + cx + cw) / 2, dim_y2 - 3), fill=WHITE, font_size="7px",
                    font_family="monospace", text_anchor="middle"))

    # Height
    ht_x = cx - 25
    g.add(dwg.line((ht_x, cy), (ht_x, floor_y), stroke=GRAY, stroke_width=0.5))
    g.add(dwg.line((ht_x - 4, cy), (ht_x + 4, cy), stroke=GRAY, stroke_width=0.5))
    g.add(dwg.line((ht_x - 4, floor_y), (ht_x + 4, floor_y), stroke=GRAY, stroke_width=0.5))
    g.add(dwg.text("8'-10\"", insert=(ht_x - 30, cy + ch / 2 + 3), fill=WHITE, font_size="8px",
                    font_family="monospace"))

    # Overhead clearance
    g.add(dwg.line((rack_right + 15, cy), (rack_right + 15, rack_top), stroke=GRAY_DIM, stroke_width=0.4))
    g.add(dwg.text("18.2\"", insert=(rack_right + 20, (cy + rack_top) / 2 + 3), fill=GRAY, font_size="6px",
                    font_family="monospace"))
    g.add(dwg.text("CLEAR", insert=(rack_right + 20, (cy + rack_top) / 2 + 12), fill=GRAY, font_size="6px",
                    font_family="monospace"))

    # Interior label
    g.add(dwg.text("CEILING CLEAR — NO OVERHEAD CABLES", insert=(cx + cw / 2, cy + 14),
                    fill=ORANGE, font_size="7px", font_family="monospace", text_anchor="middle"))
    g.add(dwg.text("ALL ROUTING ON FLOOR", insert=(cx + cw / 2, cy + 25),
                    fill=ORANGE, font_size="7px", font_family="monospace", text_anchor="middle"))


# =====================================================================
# VIEW 4: ELECTRICAL / COOLING SCHEMATIC
# =====================================================================
def draw_schematic(dwg, g):
    """Simplified electrical and cooling flow diagram."""
    ox, oy = 80, 1210
    g.add(dwg.text("VIEW 4 — ELECTRICAL + COOLING SCHEMATIC (SYSTEM FLOW)",
                    insert=(ox, oy - 8), fill=GREEN, font_size="13px", font_family="monospace", font_weight="bold"))

    # ===== POWER SECTION (top half) =====
    psy = oy + 20
    g.add(dwg.text("POWER DISTRIBUTION", insert=(ox, psy), fill=RED, font_size="10px",
                    font_family="monospace", font_weight="bold"))

    # External generator / grid
    bx, by = ox + 30, psy + 25
    box_w, box_h = 120, 45
    g.add(dwg.rect((bx, by), (box_w, box_h), fill="none", stroke=RED, stroke_width=1.5))
    g.add(dwg.text("EXTERNAL", insert=(bx + box_w / 2, by + 16), fill=RED, font_size="8px",
                    font_family="monospace", text_anchor="middle"))
    g.add(dwg.text("GENERATOR", insert=(bx + box_w / 2, by + 28), fill=RED, font_size="8px",
                    font_family="monospace", text_anchor="middle"))
    g.add(dwg.text("OR GRID", insert=(bx + box_w / 2, by + 40), fill=RED, font_size="7px",
                    font_family="monospace", text_anchor="middle"))

    # Arrow to rectifier
    ax1 = bx + box_w
    ay = by + box_h / 2
    ax2 = ax1 + 60
    g.add(dwg.line((ax1, ay), (ax2, ay), stroke=RED, stroke_width=1.5))
    g.add(dwg.polygon([(ax2, ay), (ax2 - 6, ay - 4), (ax2 - 6, ay + 4)], fill=RED))

    # Eaton rectifier
    rx, ry = ax2, by
    rw, rh = 130, 45
    g.add(dwg.rect((rx, ry), (rw, rh), fill="none", stroke=RED, stroke_width=1.5))
    g.add(dwg.text("EATON BEAM RUBIN", insert=(rx + rw / 2, ry + 14), fill=RED, font_size="7px",
                    font_family="monospace", text_anchor="middle"))
    g.add(dwg.text("DSX 800V DC", insert=(rx + rw / 2, ry + 26), fill=RED, font_size="8px",
                    font_family="monospace", text_anchor="middle"))
    g.add(dwg.text("ORV3 Sidecar", insert=(rx + rw / 2, ry + 37), fill=GRAY, font_size="6px",
                    font_family="monospace", text_anchor="middle"))

    # Arrow to Delta Power Rack
    bx2 = rx + rw
    ax3 = bx2 + 40
    g.add(dwg.line((bx2, ay), (ax3, ay), stroke=RED, stroke_width=1.5))
    g.add(dwg.polygon([(ax3, ay), (ax3 - 6, ay - 4), (ax3 - 6, ay + 4)], fill=RED))

    # Delta 660 kW Power Rack
    dx, dy = ax3, by
    dw, dh = 110, 45
    g.add(dwg.rect((dx, dy), (dw, dh), fill="none", stroke=CYAN, stroke_width=1.5))
    g.add(dwg.text("DELTA 660 kW", insert=(dx + dw / 2, dy + 12), fill=CYAN, font_size="6px",
                    font_family="monospace", text_anchor="middle"))
    g.add(dwg.text("POWER RACK", insert=(dx + dw / 2, dy + 22), fill=CYAN, font_size="7px",
                    font_family="monospace", text_anchor="middle"))
    g.add(dwg.text("480 kW BBU | e-Fuse", insert=(dx + dw / 2, dy + 32), fill=GRAY, font_size="5px",
                    font_family="monospace", text_anchor="middle"))
    g.add(dwg.text("90kW DC/DC 800V->50V", insert=(dx + dw / 2, dy + 41), fill=GRAY, font_size="5px",
                    font_family="monospace", text_anchor="middle"))

    # Arrow to bus
    dx2 = dx + dw
    ax4 = dx2 + 40
    g.add(dwg.line((dx2, ay), (ax4, ay), stroke=CYAN, stroke_width=1.5))
    g.add(dwg.polygon([(ax4, ay), (ax4 - 6, ay - 4), (ax4 - 6, ay + 4)], fill=CYAN))

    # 800V DC Bus
    bus_x = ax4
    bus_y = ay - 6
    bus_w = 600
    bus_h = 12
    g.add(dwg.rect((bus_x, bus_y), (bus_w, bus_h), fill=RED, fill_opacity=0.2, stroke=RED, stroke_width=2))
    g.add(dwg.text("800V DC BUS (FLOOR-LEVEL)", insert=(bus_x + bus_w / 2, bus_y - 5),
                    fill=RED, font_size="8px", font_family="monospace", text_anchor="middle"))

    # Solar input to bus
    solar_x = bus_x + bus_w / 2
    solar_y = bus_y - 60
    sw, sh = 100, 35
    g.add(dwg.rect((solar_x - sw / 2, solar_y), (sw, sh), fill="none", stroke=YELLOW, stroke_width=1.2))
    g.add(dwg.text("FIRST SOLAR", insert=(solar_x, solar_y + 12), fill=YELLOW, font_size="7px",
                    font_family="monospace", text_anchor="middle"))
    g.add(dwg.text("SERIES 7 TR1", insert=(solar_x, solar_y + 23), fill=YELLOW, font_size="6px",
                    font_family="monospace", text_anchor="middle"))
    g.add(dwg.text("(6 kW roof)", insert=(solar_x, solar_y + 33), fill=YELLOW, font_size="5px",
                    font_family="monospace", text_anchor="middle"))

    # DC-DC buck
    buck_y = solar_y + sh + 5
    g.add(dwg.line((solar_x, buck_y), (solar_x, bus_y), stroke=YELLOW, stroke_width=1))
    g.add(dwg.polygon([(solar_x, bus_y), (solar_x - 4, bus_y - 6), (solar_x + 4, bus_y - 6)], fill=YELLOW))
    bk_w, bk_h = 60, 16
    g.add(dwg.rect((solar_x - bk_w / 2, buck_y), (bk_w, bk_h), fill="none", stroke=YELLOW, stroke_width=0.8))
    g.add(dwg.text("DC-DC BUCK", insert=(solar_x, buck_y + 11), fill=YELLOW, font_size="5px",
                    font_family="monospace", text_anchor="middle"))

    # Rack PDU drops from bus
    rack_drop_y = bus_y + bus_h
    rack_pdu_y = rack_drop_y + 50
    for i in range(10):
        drop_x = bus_x + 20 + i * (bus_w - 40) / 9
        g.add(dwg.line((drop_x, rack_drop_y), (drop_x, rack_pdu_y), stroke=RED, stroke_width=0.8))
        g.add(dwg.polygon([(drop_x, rack_pdu_y), (drop_x - 3, rack_pdu_y - 5),
                            (drop_x + 3, rack_pdu_y - 5)], fill=RED))
        color = GREEN if i < 8 else (BLUE if i == 8 else PURPLE)
        g.add(dwg.rect((drop_x - 14, rack_pdu_y), (28, 20), fill=color, fill_opacity=0.15,
                        stroke=color, stroke_width=0.8))
        g.add(dwg.text(f"R{i+1}", insert=(drop_x, rack_pdu_y + 9), fill=color, font_size="6px",
                        font_family="monospace", text_anchor="middle"))
        g.add(dwg.text("PDU", insert=(drop_x, rack_pdu_y + 17), fill=color, font_size="5px",
                        font_family="monospace", text_anchor="middle"))

    # Solar-powered aux
    aux_x = bus_x + bus_w + 30
    g.add(dwg.line((bus_x + bus_w, ay), (aux_x, ay), stroke=YELLOW, stroke_width=0.8))
    g.add(dwg.text("SOLAR AUX", insert=(aux_x + 4, ay - 8), fill=YELLOW, font_size="6px",
                    font_family="monospace"))
    for idx, (label, yoff) in enumerate([("MUNTERS HCD DEHUM", -15), ("GREENHECK SBE-300", 5), ("LED LIGHTS", 25)]):
        ly = ay + yoff
        g.add(dwg.line((aux_x, ay), (aux_x + 30, ly), stroke=YELLOW, stroke_width=0.5))
        g.add(dwg.text(label, insert=(aux_x + 34, ly + 3), fill=CYAN, font_size="6px",
                        font_family="monospace"))

    # ===== COOLING SECTION (bottom half) =====
    csy = psy + 200
    g.add(dwg.text("COOLING LOOP", insert=(ox, csy), fill=BLUE, font_size="10px",
                    font_family="monospace", font_weight="bold"))

    # CDU box
    cdu_x, cdu_y = ox + 80, csy + 25
    cdu_w, cdu_h = 100, 55
    g.add(dwg.rect((cdu_x, cdu_y), (cdu_w, cdu_h), fill="none", stroke=BLUE, stroke_width=1.5))
    g.add(dwg.text("CoolIT CHx2000", insert=(cdu_x + cdu_w / 2, cdu_y + 16), fill=BLUE, font_size="7px",
                    font_family="monospace", text_anchor="middle", font_weight="bold"))
    g.add(dwg.text("(2,000 kW)", insert=(cdu_x + cdu_w / 2, cdu_y + 28), fill=BLUE, font_size="6px",
                    font_family="monospace", text_anchor="middle"))
    g.add(dwg.text("N+1 redundant", insert=(cdu_x + cdu_w / 2, cdu_y + 39), fill=GRAY, font_size="5px",
                    font_family="monospace", text_anchor="middle"))
    g.add(dwg.text("Staubli UQD", insert=(cdu_x + cdu_w / 2, cdu_y + 49), fill=GRAY, font_size="5px",
                    font_family="monospace", text_anchor="middle"))

    # Supply pipe to Delta In-Rack CDU
    supply_y = cdu_y + 15
    return_y = cdu_y + 40

    # Delta 140 kW In-Rack CDU
    dcdu_x = cdu_x + cdu_w + 20
    dcdu_w, dcdu_h = 90, 55
    g.add(dwg.line((cdu_x + cdu_w, supply_y + 12), (dcdu_x, supply_y + 12), stroke=BLUE, stroke_width=1.5))
    g.add(dwg.rect((dcdu_x, cdu_y), (dcdu_w, dcdu_h), fill="none", stroke=CYAN, stroke_width=1.2))
    g.add(dwg.text("DELTA 140 kW", insert=(dcdu_x + dcdu_w / 2, cdu_y + 14), fill=CYAN, font_size="6px",
                    font_family="monospace", text_anchor="middle", font_weight="bold"))
    g.add(dwg.text("IN-RACK CDU", insert=(dcdu_x + dcdu_w / 2, cdu_y + 25), fill=CYAN, font_size="6px",
                    font_family="monospace", text_anchor="middle"))
    g.add(dwg.text("4RU | NVL72 Cert", insert=(dcdu_x + dcdu_w / 2, cdu_y + 36), fill=GRAY, font_size="5px",
                    font_family="monospace", text_anchor="middle"))
    g.add(dwg.text("Per-Rack Precision", insert=(dcdu_x + dcdu_w / 2, cdu_y + 47), fill=GRAY, font_size="5px",
                    font_family="monospace", text_anchor="middle"))

    pipe_end_x = dcdu_x + dcdu_w + 440

    g.add(dwg.line((dcdu_x + dcdu_w, supply_y), (pipe_end_x, supply_y), stroke=BLUE, stroke_width=2))
    g.add(dwg.polygon([(pipe_end_x, supply_y), (pipe_end_x - 8, supply_y - 4),
                        (pipe_end_x - 8, supply_y + 4)], fill=BLUE))
    g.add(dwg.text("SUPPLY 45C (113F)", insert=(dcdu_x + dcdu_w + 20, supply_y - 5),
                    fill=BLUE, font_size="7px", font_family="monospace"))

    # Rack manifold connections
    for i in range(10):
        rmx = dcdu_x + dcdu_w + 20 + i * 42
        color = GREEN if i < 8 else (BLUE if i == 8 else PURPLE)
        g.add(dwg.line((rmx, supply_y), (rmx, supply_y + 12), stroke=color, stroke_width=0.8))
        g.add(dwg.line((rmx, return_y - 12), (rmx, return_y), stroke=color, stroke_width=0.8))
        g.add(dwg.rect((rmx - 10, supply_y + 12), (20, return_y - 12 - supply_y - 12),
                        fill=color, fill_opacity=0.1, stroke=color, stroke_width=0.6))
        g.add(dwg.text(f"R{i+1}", insert=(rmx, (supply_y + return_y) / 2 + 3), fill=color, font_size="5px",
                        font_family="monospace", text_anchor="middle"))

    # Return pipe
    g.add(dwg.line((pipe_end_x, return_y), (cdu_x + cdu_w, return_y), stroke=RED, stroke_width=2))
    g.add(dwg.polygon([(cdu_x + cdu_w, return_y), (cdu_x + cdu_w + 8, return_y - 4),
                        (cdu_x + cdu_w + 8, return_y + 4)], fill=RED))
    g.add(dwg.text("RETURN 55C (131F)", insert=(cdu_x + cdu_w + 40, return_y + 12),
                    fill=RED, font_size="7px", font_family="monospace"))

    # CDU to External dry cooler
    ext_y = cdu_y + cdu_h + 30
    g.add(dwg.line((cdu_x + cdu_w / 2 - 15, cdu_y + cdu_h), (cdu_x + cdu_w / 2 - 15, ext_y),
                    stroke=RED, stroke_width=1.5))
    g.add(dwg.polygon([(cdu_x + cdu_w / 2 - 15, ext_y),
                        (cdu_x + cdu_w / 2 - 19, ext_y - 6),
                        (cdu_x + cdu_w / 2 - 11, ext_y - 6)], fill=RED))
    g.add(dwg.line((cdu_x + cdu_w / 2 + 15, ext_y), (cdu_x + cdu_w / 2 + 15, cdu_y + cdu_h),
                    stroke=BLUE, stroke_width=1.5))
    g.add(dwg.polygon([(cdu_x + cdu_w / 2 + 15, cdu_y + cdu_h),
                        (cdu_x + cdu_w / 2 + 11, cdu_y + cdu_h + 6),
                        (cdu_x + cdu_w / 2 + 19, cdu_y + cdu_h + 6)], fill=BLUE))

    # External dry cooler box
    dc_w, dc_h = 160, 50
    dc_x = cdu_x + cdu_w / 2 - dc_w / 2
    dc_y = ext_y + 5
    g.add(dwg.rect((dc_x, dc_y), (dc_w, dc_h), fill="none", stroke=CYAN, stroke_width=1.5))
    g.add(dwg.text("BAC TrilliumSeries", insert=(dc_x + dc_w / 2, dc_y + 14), fill=CYAN, font_size="8px",
                    font_family="monospace", text_anchor="middle"))
    g.add(dwg.text("ADIABATIC COOLER", insert=(dc_x + dc_w / 2, dc_y + 26), fill=CYAN, font_size="7px",
                    font_family="monospace", text_anchor="middle"))
    g.add(dwg.text("1.3 MW rejection capacity", insert=(dc_x + dc_w / 2, dc_y + 38), fill=CYAN, font_size="6px",
                    font_family="monospace", text_anchor="middle"))
    g.add(dwg.text("Adiabatic assist >95F", insert=(dc_x + dc_w / 2, dc_y + 48), fill=GRAY, font_size="5px",
                    font_family="monospace", text_anchor="middle"))

    # Heat to atmosphere
    atm_y = dc_y + dc_h + 25
    g.add(dwg.line((dc_x + dc_w / 2, dc_y + dc_h), (dc_x + dc_w / 2, atm_y), stroke=GRAY, stroke_width=1))
    g.add(dwg.text("HEAT TO ATMOSPHERE", insert=(dc_x + dc_w / 2, atm_y + 12), fill=GRAY, font_size="6px",
                    font_family="monospace", text_anchor="middle"))

    # ===== MONITORING SECTION =====
    msx = ox + 900
    msy = csy
    g.add(dwg.text("MONITORING + CONTROL", insert=(msx, msy), fill=YELLOW, font_size="10px",
                    font_family="monospace", font_weight="bold"))

    # Sensor controller
    sc_x, sc_y = msx + 30, msy + 25
    sc_w, sc_h = 130, 45
    g.add(dwg.rect((sc_x, sc_y), (sc_w, sc_h), fill="none", stroke=YELLOW, stroke_width=1.2))
    g.add(dwg.text("NVIDIA JETSON", insert=(sc_x + sc_w / 2, sc_y + 16), fill=YELLOW, font_size="8px",
                    font_family="monospace", text_anchor="middle"))
    g.add(dwg.text("AGX ORIN", insert=(sc_x + sc_w / 2, sc_y + 28), fill=YELLOW, font_size="8px",
                    font_family="monospace", text_anchor="middle"))
    g.add(dwg.text("(Controller)", insert=(sc_x + sc_w / 2, sc_y + 40), fill=GRAY, font_size="5px",
                    font_family="monospace", text_anchor="middle"))

    # Sensors feeding in
    sensors = [
        "40x TEMP SENSORS",
        "4x HUMIDITY SENSORS",
        "10x FLOW METERS",
        "LEAK DETECTION ROPE",
        "2x IR CAMERAS",
        "VESDA-E VEU ASPIRATING",
        "ANSUL NOVEC 1230 FIRE",
        "8x DOOR/PANEL REED SW",
    ]
    for i, s in enumerate(sensors):
        ssy = sc_y - 10 + i * 14
        ssx = sc_x - 10
        g.add(dwg.line((ssx - 80, ssy), (ssx, ssy), stroke=YELLOW, stroke_width=0.4))
        g.add(dwg.text(s, insert=(ssx - 84, ssy + 3), fill=YELLOW, font_size="5px",
                        font_family="monospace", text_anchor="end"))

    # Arrow to network
    net_x = sc_x + sc_w + 50
    net_y = sc_y + sc_h / 2
    g.add(dwg.line((sc_x + sc_w, net_y), (net_x, net_y), stroke=YELLOW, stroke_width=1))
    g.add(dwg.polygon([(net_x, net_y), (net_x - 6, net_y - 4), (net_x - 6, net_y + 4)], fill=YELLOW))

    # Network box
    nw, nh = 100, 35
    g.add(dwg.rect((net_x, net_y - nh / 2), (nw, nh), fill="none", stroke=WHITE, stroke_width=1))
    g.add(dwg.text("QUANTUM-X800", insert=(net_x + nw / 2, net_y - 2), fill=WHITE, font_size="7px",
                    font_family="monospace", text_anchor="middle"))
    g.add(dwg.text("4G/5G/STARLINK", insert=(net_x + nw / 2, net_y + 10), fill=WHITE, font_size="6px",
                    font_family="monospace", text_anchor="middle"))

    # Arrow to Mission Control
    mc_x = net_x + nw + 50
    g.add(dwg.line((net_x + nw, net_y), (mc_x, net_y), stroke=WHITE, stroke_width=1))
    g.add(dwg.polygon([(mc_x, net_y), (mc_x - 6, net_y - 4), (mc_x - 6, net_y + 4)], fill=WHITE))

    mw, mh = 130, 45
    g.add(dwg.rect((mc_x, net_y - mh / 2), (mw, mh), fill=GREEN, fill_opacity=0.1,
                    stroke=GREEN, stroke_width=1.5))
    g.add(dwg.text("MISSION", insert=(mc_x + mw / 2, net_y - 5), fill=GREEN, font_size="9px",
                    font_family="monospace", text_anchor="middle", font_weight="bold"))
    g.add(dwg.text("CONTROL", insert=(mc_x + mw / 2, net_y + 8), fill=GREEN, font_size="9px",
                    font_family="monospace", text_anchor="middle", font_weight="bold"))
    g.add(dwg.text("(MARLIE 1 NOC)", insert=(mc_x + mw / 2, net_y + 20), fill=GRAY, font_size="5px",
                    font_family="monospace", text_anchor="middle"))

    # Total sensor count
    g.add(dwg.text("65 SENSORS TOTAL — ZERO ON-SITE STAFF — AI MANAGED",
                    insert=(msx, msy + 140), fill=GREEN, font_size="7px", font_family="monospace"))


def main():
    dwg = svgwrite.Drawing(str(OUT), size=(f"{W}px", f"{H}px"), profile="full")

    # Background
    dwg.add(dwg.rect((0, 0), (W, H), fill=BG))

    # Border
    dwg.add(dwg.rect((10, 10), (W - 20, H - 20), fill="none", stroke=GREEN_DIM, stroke_width=1))
    dwg.add(dwg.rect((15, 15), (W - 30, H - 30), fill="none", stroke=GRAY_DIM, stroke_width=0.5))

    g = dwg.g()
    dwg.add(g)

    draw_top_view(dwg, g)
    draw_side_view(dwg, g)
    draw_end_view(dwg, g)
    draw_schematic(dwg, g)
    draw_notes(dwg, g)
    draw_title_block(dwg, g)

    dwg.save()
    print(f"Created: {OUT}")
    print(f"Size: {OUT.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
