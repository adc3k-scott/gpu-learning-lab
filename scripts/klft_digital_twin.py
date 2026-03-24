"""
KLFT Digital Twin — Lafayette Regional Airport
Generates a USD scene file for NVIDIA Omniverse rendering.

Airport data from FAA (verified 2026-03-23):
- ICAO: KLFT / FAA: LFT
- Elevation: 40.9 ft MSL
- Airport Reference Point: 30.2050267N, 91.9877539W
- Runway 04R/22L (PRIMARY): 8,000 ft x 150 ft, heading 039 deg, HIRL, ILS 22L, MALSR
- Runway 11/29 (CROSSWIND): 5,403 ft x 150 ft, heading 110 deg, MIRL
- Runway 04L/22R (GA): 4,098 ft x 75 ft, heading 039 deg, MIRL, closed 2230-0530
- Class C airspace

GPS-to-meter conversion from airport reference point:
- 1 deg lat ~ 111,139 m
- 1 deg lon ~ 96,157 m (at lat 30.205)

Generates USD with:
- Three runways with markings + EMAS overrun areas
- Taxiways connecting runways
- New terminal building ($150M, opened Jan 2022, 5 gates, L-shape)
- Control tower (~40m)
- FBO (Signature Aviation, 123 Grissom Dr, south side)
- Fire station (near runway intersection)
- SkyCommand drone operations area (near GA runway)
- Drone dock positions
- Animated drone flight paths
- Conflict detection zones
"""

import math
import json
import os

# All measurements in meters (USD standard)
FT_TO_M = 0.3048

# Airport reference point (FAA verified)
AIRPORT_LAT = 30.2050267
AIRPORT_LON = -91.9877539
AIRPORT_ELEV_FT = 40.9

# GPS-to-meter conversion at this latitude
DEG_LAT_TO_M = 111139.0
DEG_LON_TO_M = 96157.0  # 111139 * cos(30.205 deg)

# Runway threshold GPS coordinates
RUNWAY_THRESHOLDS = {
    "04R/22L": {
        "04R": (30.19593611, -91.99373333),
        "22L": (30.21305278, -91.97788333),
    },
    "11/29": {
        "11": (30.20764722, -91.99810278),
        "29": (30.20256389, -91.98206389),
    },
    "04L/22R": {
        "04L": (30.20160278, -91.99251667),
        "22R": (30.21040278, -91.98440000),
    },
}

def _gps_to_offset(lat, lon):
    """Convert GPS to meters offset from airport reference point. X=east, Z=north."""
    x = (lon - AIRPORT_LON) * DEG_LON_TO_M
    z = (lat - AIRPORT_LAT) * DEG_LAT_TO_M
    return (x, z)

def _runway_center(name):
    """Compute runway center offset in meters from threshold GPS."""
    t = RUNWAY_THRESHOLDS[name]
    keys = list(t.keys())
    lat1, lon1 = t[keys[0]]
    lat2, lon2 = t[keys[1]]
    return _gps_to_offset((lat1 + lat2) / 2, (lon1 + lon2) / 2)

# Runway data — 3 runways (verified FAA 2026-03-23)
# Center offsets computed from threshold GPS coordinates
RUNWAYS = {
    "04R/22L": {
        "length_ft": 8000,
        "width_ft": 150,
        "heading_deg": 39,  # true heading of Rwy 04R end
        "surface": "asphalt",
        "lighting": "HIRL",
        "ils": "22L",
        "approach_lights": "MALSR",
        "center_offset_m": _runway_center("04R/22L"),  # (187, -59) approx
    },
    "11/29": {
        "length_ft": 5403,
        "width_ft": 150,
        "heading_deg": 110,  # true heading of Rwy 11 end
        "surface": "asphalt",
        "lighting": "MIRL",
        "center_offset_m": _runway_center("11/29"),  # (-224, 9) approx
    },
    "04L/22R": {
        "length_ft": 4098,
        "width_ft": 75,  # narrower GA runway
        "heading_deg": 39,  # parallel to 04R/22L
        "surface": "asphalt",
        "lighting": "MIRL",
        "restrictions": "closed 2230-0530",
        "center_offset_m": _runway_center("04L/22R"),  # (-68, 108) approx
    },
}

# EMAS (Engineered Materials Arresting System) — overrun areas at runway ends
EMAS_ZONES = []
for rwy_name, thresholds in RUNWAY_THRESHOLDS.items():
    for end_name, (lat, lon) in thresholds.items():
        offset = _gps_to_offset(lat, lon)
        EMAS_ZONES.append({
            "runway": rwy_name,
            "end": end_name,
            "position_m": offset,
            "length_m": 100,  # standard EMAS length
            "width_m": RUNWAYS[rwy_name]["width_ft"] * FT_TO_M,
            "heading_deg": RUNWAYS[rwy_name]["heading_deg"],
        })

# Buildings — positioned relative to verified runway geometry
# Terminal is east of Runway 04R/22L, FBO south side, SkyCommand near GA runway
BUILDINGS = {
    "terminal": {
        # New $150M terminal, opened Jan 2022, 120,000 sq ft, 5 gates
        # L-shaped with canopy — main wing + perpendicular gate concourse
        "width_m": 100,       # main wing (east-west)
        "depth_m": 110,       # gate concourse (north-south)
        "height_m": 14,
        "position_m": (350, 0, -59),  # east of Rwy 04R/22L center
        "color": (0.88, 0.88, 0.90),  # light gray/white modern facade
        "shape": "L",
        "notes": "$150M, 5 gates, opened Jan 2022",
    },
    "terminal_canopy": {
        # Covered drop-off / curbside canopy extending from terminal
        "width_m": 80,
        "depth_m": 12,
        "height_m": 6,
        "position_m": (410, 0, -59),  # east face of terminal
        "color": (0.75, 0.75, 0.78),  # slightly darker canopy
    },
    "control_tower": {
        "width_m": 10,
        "depth_m": 10,
        "height_m": 40,  # ~40m tall
        "position_m": (310, 0, -30),  # near terminal, good sightlines
        "color": (0.82, 0.82, 0.85),
    },
    "fbo_signature": {
        # Signature Aviation — 123 Grissom Drive, south side of airport
        "width_m": 45,
        "depth_m": 35,
        "height_m": 10,
        "position_m": (200, 0, -350),  # south side
        "color": (0.6, 0.6, 0.65),
        "notes": "Signature Aviation, 123 Grissom Dr",
    },
    "fbo_hangar": {
        # Hangar associated with FBO
        "width_m": 40,
        "depth_m": 30,
        "height_m": 12,
        "position_m": (250, 0, -320),  # adjacent to FBO
        "color": (0.55, 0.55, 0.60),
    },
    "fire_station": {
        # ARFF station — near runway intersection for rapid response
        "width_m": 25,
        "depth_m": 18,
        "height_m": 8,
        "position_m": (-50, 0, -20),  # near intersection of runways
        "color": (0.8, 0.2, 0.2),  # red
    },
    "skycommand_ops": {
        # SkyCommand ops — near GA runway 04L end, away from commercial ops
        "width_m": 15,
        "depth_m": 12,
        "height_m": 5,
        "position_m": (-110, 0, -100),  # near 04L threshold area
        "color": (0.2, 0.4, 0.8),  # blue for SkyCommand
    },
}

# Drone dock positions — near SkyCommand ops (GA runway area)
DRONE_DOCKS = [
    {"id": "DOCK-1", "position_m": (-100, 0, -110), "heading_deg": 39},
    {"id": "DOCK-2", "position_m": (-90, 0, -120), "heading_deg": 39},
    {"id": "DOCK-3", "position_m": (-80, 0, -130), "heading_deg": 39},
]

# Drone flight paths (waypoints in meters from airport center)
DRONE_PATHS = {
    "patrol_north": [
        (-100, 30, -110),   # takeoff from dock
        (-100, 60, -110),   # climb
        (200, 60, 500),     # north patrol
        (-500, 60, 800),    # pipeline corridor
        (-500, 60, 200),    # return leg
        (0, 60, -110),      # approach
        (-100, 30, -110),   # land
    ],
    "runway_inspection": [
        (-90, 30, -120),
        (-90, 45, -120),
        (-800, 45, 9),      # near Rwy 11 threshold
        (350, 45, 9),       # near Rwy 29 threshold
        (187, 45, -59),     # along 04R/22L
        (-68, 45, 108),     # along 04L/22R
        (-90, 30, -120),
    ],
    "emergency_response": [
        (-80, 30, -130),
        (-80, 100, -130),   # rapid climb
        (0, 100, 1000),     # emergency location 1km north
        (0, 60, 1000),      # descend for observation
        (0, 60, 500),       # orbit
        (-80, 30, -130),    # return
    ],
}

# Conflict zones (runway intersections + taxiway holds)
CONFLICT_ZONES = [
    {"center_m": (-50, 0, 0), "radius_m": 60, "label": "Runway 11/29 x 04R/22L Intersection"},
    {"center_m": (-150, 0, 50), "radius_m": 40, "label": "Runway 11/29 x 04L/22R Intersection"},
    {"center_m": (300, 0, -50), "radius_m": 30, "label": "Taxiway Alpha Hold — Terminal"},
    {"center_m": (-200, 0, -80), "radius_m": 30, "label": "Taxiway Bravo Hold — GA"},
]


def generate_usda_scene():
    """Generate a USDA (ASCII USD) scene file for the KLFT digital twin."""

    scene = []
    scene.append('#usda 1.0')
    scene.append('(')
    scene.append('    defaultPrim = "KLFT_Airport"')
    scene.append('    metersPerUnit = 1.0')
    scene.append('    upAxis = "Y"')
    scene.append(')')
    scene.append('')
    scene.append('def Xform "KLFT_Airport" (')
    scene.append('    kind = "assembly"')
    scene.append(')')
    scene.append('{')

    # Ground plane
    scene.append('    def Mesh "Ground"')
    scene.append('    {')
    scene.append('        float3[] extent = [(-3000, -0.1, -3000), (3000, 0, 3000)]')
    scene.append('        int[] faceVertexCounts = [4]')
    scene.append('        int[] faceVertexIndices = [0, 1, 2, 3]')
    scene.append('        point3f[] points = [(-3000, 0, -3000), (3000, 0, -3000), (3000, 0, 3000), (-3000, 0, 3000)]')
    scene.append('        color3f[] primvars:displayColor = [(0.15, 0.35, 0.12)]')  # grass green
    scene.append('    }')

    # Generate runways
    for rwy_name, rwy in RUNWAYS.items():
        length_m = rwy["length_ft"] * FT_TO_M
        width_m = rwy["width_ft"] * FT_TO_M
        heading_rad = math.radians(rwy["heading_deg"])
        cx, cz = rwy["center_offset_m"]

        # Runway as a rotated box
        safe_name = rwy_name.replace("/", "_")
        scene.append(f'    def Xform "Runway_{safe_name}"')
        scene.append('    {')
        scene.append(f'        double3 xformOp:translate = ({cx}, 0.05, {cz})')
        rot_y = -rwy["heading_deg"] + 90  # USD rotation
        scene.append(f'        float xformOp:rotateY = {rot_y}')
        scene.append('        uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:rotateY"]')
        scene.append(f'        def Cube "Surface"')
        scene.append('        {')
        scene.append(f'            float3 xformOp:scale = ({length_m/2}, 0.05, {width_m/2})')
        scene.append('            uniform token[] xformOpOrder = ["xformOp:scale"]')
        scene.append('            color3f[] primvars:displayColor = [(0.2, 0.2, 0.22)]')  # dark asphalt
        scene.append('        }')

        # Runway centerline
        scene.append(f'        def Cube "Centerline"')
        scene.append('        {')
        scene.append(f'            float3 xformOp:scale = ({length_m/2}, 0.06, 0.5)')
        scene.append('            uniform token[] xformOpOrder = ["xformOp:scale"]')
        scene.append('            color3f[] primvars:displayColor = [(0.9, 0.9, 0.9)]')  # white
        scene.append('        }')

        # Threshold markings
        for end in [-1, 1]:
            thr_label = "A" if end == -1 else "B"
            scene.append(f'        def Cube "Threshold_{thr_label}"')
            scene.append('        {')
            scene.append(f'            double3 xformOp:translate = ({end * (length_m/2 - 30)}, 0.01, 0)')
            scene.append(f'            float3 xformOp:scale = (15, 0.06, {width_m/2 - 5})')
            scene.append('            uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:scale"]')
            scene.append('            color3f[] primvars:displayColor = [(0.9, 0.9, 0.9)]')
            scene.append('        }')

        scene.append('    }')

    # Generate EMAS overrun areas at runway ends
    for emas in EMAS_ZONES:
        rwy = emas["runway"].replace("/", "_")
        end = emas["end"]
        ex, ez = emas["position_m"]
        heading_rad = math.radians(emas["heading_deg"])
        emas_len = emas["length_m"]
        emas_wid = emas["width_m"]
        rot_y = -emas["heading_deg"] + 90

        safe_end = end.replace("/", "_")
        scene.append(f'    def Xform "EMAS_{rwy}_{safe_end}"')
        scene.append('    {')
        # Push EMAS beyond the threshold (outward from runway)
        scene.append(f'        double3 xformOp:translate = ({ex}, 0.03, {ez})')
        scene.append(f'        float xformOp:rotateY = {rot_y}')
        scene.append('        uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:rotateY"]')
        scene.append(f'        def Cube "Bed"')
        scene.append('        {')
        scene.append(f'            float3 xformOp:scale = ({emas_len/2}, 0.15, {emas_wid/2})')
        scene.append('            uniform token[] xformOpOrder = ["xformOp:scale"]')
        scene.append('            color3f[] primvars:displayColor = [(0.6, 0.55, 0.3)]')  # tan/sand
        scene.append('        }')
        scene.append('    }')

    # Generate taxiways (simplified as strips connecting runways to terminal)
    taxiways = [
        {"name": "Alpha", "points": [(100, -59), (350, -59)], "width_m": 20},   # Rwy 04R/22L to terminal
        {"name": "Bravo", "points": [(-150, 0), (-100, -100)], "width_m": 15},  # intersection to GA area
        {"name": "Charlie", "points": [(350, -59), (250, -320)], "width_m": 15}, # terminal to FBO
        {"name": "Delta", "points": [(-68, 108), (-100, -20)], "width_m": 15},  # GA rwy to intersection
    ]

    for twy in taxiways:
        x1, z1 = twy["points"][0]
        x2, z2 = twy["points"][1]
        length = math.sqrt((x2-x1)**2 + (z2-z1)**2)
        angle = math.degrees(math.atan2(z2-z1, x2-x1))
        mx, mz = (x1+x2)/2, (z1+z2)/2

        scene.append(f'    def Xform "Taxiway_{twy["name"]}"')
        scene.append('    {')
        scene.append(f'        double3 xformOp:translate = ({mx}, 0.04, {mz})')
        scene.append(f'        float xformOp:rotateY = {-angle + 90}')
        scene.append('        uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:rotateY"]')
        scene.append(f'        def Cube "Surface"')
        scene.append('        {')
        scene.append(f'            float3 xformOp:scale = ({length/2}, 0.04, {twy["width_m"]/2})')
        scene.append('            uniform token[] xformOpOrder = ["xformOp:scale"]')
        scene.append('            color3f[] primvars:displayColor = [(0.25, 0.25, 0.27)]')
        scene.append('        }')
        scene.append('    }')

    # Generate buildings
    for bldg_name, bldg in BUILDINGS.items():
        x, y, z = bldg["position_m"]
        w, d, h = bldg["width_m"], bldg["depth_m"], bldg["height_m"]
        r, g, b = bldg["color"]

        scene.append(f'    def Xform "{bldg_name}"')
        scene.append('    {')

        if bldg.get("shape") == "L":
            # L-shaped terminal: main wing (E-W) + gate concourse (N-S)
            scene.append(f'        double3 xformOp:translate = ({x}, 0, {z})')
            scene.append('        uniform token[] xformOpOrder = ["xformOp:translate"]')
            # Main wing (east-west, full width)
            scene.append(f'        def Cube "MainWing"')
            scene.append('        {')
            scene.append(f'            double3 xformOp:translate = (0, {h/2}, 0)')
            scene.append(f'            float3 xformOp:scale = ({w/2}, {h/2}, 25)')
            scene.append('            uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:scale"]')
            scene.append(f'            color3f[] primvars:displayColor = [({r}, {g}, {b})]')
            scene.append('        }')
            # Gate concourse (north-south, perpendicular — west end)
            scene.append(f'        def Cube "GateConcourse"')
            scene.append('        {')
            scene.append(f'            double3 xformOp:translate = ({-w/2 + 15}, {h/2}, {-d/4})')
            scene.append(f'            float3 xformOp:scale = (15, {h/2}, {d/4})')
            scene.append('            uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:scale"]')
            scene.append(f'            color3f[] primvars:displayColor = [({r}, {g}, {b})]')
            scene.append('        }')
            # Jet bridges (5 gates along concourse)
            for gate_i in range(5):
                gz = -d/4 + gate_i * (d/2) / 5
                scene.append(f'        def Cube "Gate_{gate_i + 1}"')
                scene.append('        {')
                scene.append(f'            double3 xformOp:translate = ({-w/2 - 5}, {h * 0.6}, {gz})')
                scene.append(f'            float3 xformOp:scale = (8, 1.5, 2)')
                scene.append('            uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:scale"]')
                scene.append(f'            color3f[] primvars:displayColor = [(0.7, 0.7, 0.72)]')
                scene.append('        }')
        else:
            # Standard rectangular building
            scene.append(f'        double3 xformOp:translate = ({x}, {h/2}, {z})')
            scene.append('        uniform token[] xformOpOrder = ["xformOp:translate"]')
            scene.append(f'        def Cube "Body"')
            scene.append('        {')
            scene.append(f'            float3 xformOp:scale = ({w/2}, {h/2}, {d/2})')
            scene.append('            uniform token[] xformOpOrder = ["xformOp:scale"]')
            scene.append(f'            color3f[] primvars:displayColor = [({r}, {g}, {b})]')
            scene.append('        }')

        scene.append('    }')

    # Generate drone docks
    for dock in DRONE_DOCKS:
        x, y, z = dock["position_m"]
        scene.append(f'    def Xform "{dock["id"]}"')
        scene.append('    {')
        scene.append(f'        double3 xformOp:translate = ({x}, 0.5, {z})')
        scene.append('        uniform token[] xformOpOrder = ["xformOp:translate"]')
        scene.append(f'        def Cylinder "Pad"')
        scene.append('        {')
        scene.append('            double height = 0.3')
        scene.append('            double radius = 1.5')
        scene.append('            color3f[] primvars:displayColor = [(0.1, 0.6, 0.1)]')  # green pad
        scene.append('        }')
        scene.append(f'        def Cube "Dock"')
        scene.append('        {')
        scene.append(f'            double3 xformOp:translate = (0, 0.5, 0)')
        scene.append(f'            float3 xformOp:scale = (0.5, 0.5, 0.5)')
        scene.append('            uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:scale"]')
        scene.append('            color3f[] primvars:displayColor = [(0.3, 0.3, 0.35)]')
        scene.append('        }')
        scene.append('    }')

    # Generate conflict zones (red transparent spheres)
    for i, zone in enumerate(CONFLICT_ZONES):
        x, y, z = zone["center_m"]
        r = zone["radius_m"]
        scene.append(f'    def Xform "ConflictZone_{i}"')
        scene.append('    {')
        scene.append(f'        double3 xformOp:translate = ({x}, 5, {z})')
        scene.append('        uniform token[] xformOpOrder = ["xformOp:translate"]')
        scene.append(f'        def Sphere "Zone"')
        scene.append('        {')
        scene.append(f'            double radius = {r}')
        scene.append('            color3f[] primvars:displayColor = [(0.9, 0.1, 0.1)]')
        scene.append('        }')
        scene.append('    }')

    # Generate drone flight path visualizations (as tubes/lines)
    for path_name, waypoints in DRONE_PATHS.items():
        scene.append(f'    def Xform "FlightPath_{path_name}"')
        scene.append('    {')
        for j in range(len(waypoints) - 1):
            x1, y1, z1 = waypoints[j]
            x2, y2, z2 = waypoints[j+1]
            mx, my, mz = (x1+x2)/2, (y1+y2)/2, (z1+z2)/2
            length = math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)

            scene.append(f'        def Cube "Segment_{j}"')
            scene.append('        {')
            scene.append(f'            double3 xformOp:translate = ({mx}, {my}, {mz})')
            scene.append(f'            float3 xformOp:scale = ({length/2}, 0.3, 0.3)')
            scene.append('            uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:scale"]')
            if "emergency" in path_name:
                scene.append('            color3f[] primvars:displayColor = [(1.0, 0.2, 0.0)]')  # orange
            elif "patrol" in path_name:
                scene.append('            color3f[] primvars:displayColor = [(0.0, 0.8, 1.0)]')  # cyan
            else:
                scene.append('            color3f[] primvars:displayColor = [(0.0, 1.0, 0.5)]')  # green
            scene.append('        }')
        scene.append('    }')

    # Drone models (simple representations at dock positions)
    for i, dock in enumerate(DRONE_DOCKS):
        x, y, z = dock["position_m"]
        scene.append(f'    def Xform "Drone_{i}"')
        scene.append('    {')
        scene.append(f'        double3 xformOp:translate = ({x}, 1.5, {z})')
        scene.append('        uniform token[] xformOpOrder = ["xformOp:translate"]')
        # Body
        scene.append(f'        def Cube "Body"')
        scene.append('        {')
        scene.append(f'            float3 xformOp:scale = (0.2, 0.05, 0.2)')
        scene.append('            uniform token[] xformOpOrder = ["xformOp:scale"]')
        scene.append('            color3f[] primvars:displayColor = [(0.1, 0.1, 0.12)]')
        scene.append('        }')
        # Arms (4)
        for arm_i, (ax, az) in enumerate([(0.3, 0.3), (0.3, -0.3), (-0.3, 0.3), (-0.3, -0.3)]):
            scene.append(f'        def Cylinder "Arm_{arm_i}"')
            scene.append('        {')
            scene.append(f'            double3 xformOp:translate = ({ax}, 0, {az})')
            scene.append('            double height = 0.02')
            scene.append('            double radius = 0.12')
            scene.append('            uniform token[] xformOpOrder = ["xformOp:translate"]')
            scene.append('            color3f[] primvars:displayColor = [(0.15, 0.15, 0.18)]')
            scene.append('        }')
        scene.append('    }')

    # Camera presets
    cameras = {
        "tower_view": {"pos": (310, 38, -30), "target": (0, 0, 0)},
        "overhead": {"pos": (50, 1000, 0), "target": (50, 0, 0)},
        "approach_22L": {"pos": (-1500, 120, -800), "target": (187, 5, -59)},
        "approach_11": {"pos": (-1200, 100, 200), "target": (-224, 5, 9)},
        "new_terminal": {"pos": (500, 25, -59), "target": (350, 7, -59)},
        "skycommand_ops": {"pos": (-60, 12, -130), "target": (-110, 3, -100)},
        "drone_launch": {"pos": (-70, 8, -100), "target": (-100, 2, -110)},
    }

    for cam_name, cam in cameras.items():
        px, py, pz = cam["pos"]
        scene.append(f'    def Camera "{cam_name}"')
        scene.append('    {')
        scene.append(f'        double3 xformOp:translate = ({px}, {py}, {pz})')
        scene.append('        uniform token[] xformOpOrder = ["xformOp:translate"]')
        scene.append('        float focalLength = 35')
        scene.append('        float horizontalAperture = 36')
        scene.append('    }')

    # Close root
    scene.append('}')

    return '\n'.join(scene)


def generate_scene_config():
    """Generate a JSON config file with scene metadata for the render agent."""
    # Serialize runway data (convert tuples to lists for JSON)
    runways_serializable = {}
    for k, v in RUNWAYS.items():
        rv = dict(v)
        rv["center_offset_m"] = list(rv["center_offset_m"])
        runways_serializable[k] = rv

    config = {
        "scene_name": "KLFT_Digital_Twin",
        "airport": {
            "icao": "KLFT",
            "faa": "LFT",
            "name": "Lafayette Regional Airport",
            "elevation_ft": AIRPORT_ELEV_FT,
            "lat": AIRPORT_LAT,
            "lon": AIRPORT_LON,
            "airspace_class": "C",
            "reference_point": f"{AIRPORT_LAT}N, {abs(AIRPORT_LON)}W",
        },
        "runways": runways_serializable,
        "runway_thresholds": {k: {end: list(coords) for end, coords in v.items()} for k, v in RUNWAY_THRESHOLDS.items()},
        "emas_zones": len(EMAS_ZONES),
        "buildings": {k: {**{kk: (list(vv) if isinstance(vv, tuple) else vv) for kk, vv in v.items()}} for k, v in BUILDINGS.items()},
        "drone_docks": DRONE_DOCKS,
        "drone_paths": {k: [list(p) for p in v] for k, v in DRONE_PATHS.items()},
        "conflict_zones": CONFLICT_ZONES,
        "skycommand_integration": {
            "marlie_i_distance_mi": 0.8,
            "marlie_i_gps": "30.21975N, 92.00645W",
            "trappeys_distance_mi": 0.5,
            "trappeys_gps": "30.21356N, 92.00163W",
            "noc_primary": "Willow Glen Terminal (60 mi, fiber)",
            "noc_backup": "MARLIE I (0.8 mi, direct)",
        },
        "cameras": {
            "tower_view": "Control tower perspective — full airport surface",
            "overhead": "Satellite view — all 3 runways, buildings, drone paths",
            "approach_22L": "Aircraft approach to Runway 22L (ILS) — pilot perspective",
            "approach_11": "Aircraft approach to Runway 11 — pilot perspective",
            "new_terminal": "New $150M terminal building — curbside view",
            "skycommand_ops": "SkyCommand operations building close-up",
            "drone_launch": "Drone dock area — launch sequence view",
        },
    }
    return json.dumps(config, indent=2)


if __name__ == "__main__":
    # Generate USDA scene
    usda = generate_usda_scene()
    usda_path = os.path.join(os.path.dirname(__file__), "..", "adc3k-deploy", "klft-digital-twin.usda")
    with open(usda_path, "w") as f:
        f.write(usda)
    print(f"Generated USDA scene: {usda_path}")
    print(f"  Size: {len(usda):,} bytes")

    # Generate config
    config = generate_scene_config()
    config_path = os.path.join(os.path.dirname(__file__), "..", "adc3k-deploy", "klft-scene-config.json")
    with open(config_path, "w") as f:
        f.write(config)
    print(f"Generated scene config: {config_path}")

    # Summary
    print(f"\nScene contents:")
    print(f"  Runways: {len(RUNWAYS)}")
    print(f"  Buildings: {len(BUILDINGS)}")
    print(f"  Drone docks: {len(DRONE_DOCKS)}")
    print(f"  Flight paths: {len(DRONE_PATHS)}")
    print(f"  Conflict zones: {len(CONFLICT_ZONES)}")
    print(f"  EMAS zones: {len(EMAS_ZONES)}")
    print(f"  Camera presets: 7")
    print(f"\nUpload to RunPod pod and render with Kit SDK 109.")
