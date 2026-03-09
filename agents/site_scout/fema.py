"""
FEMA Flood Zone lookup via the National Flood Hazard Layer (NFHL) REST API.
Returns a score 0-5 based on flood zone class.
"""
import requests

FEMA_URL = (
    "https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer/28/query"
)

ZONE_SCORES = {
    # Minimal / outside mapped area
    "X":   5,
    "X500": 3,
    "D":   3,
    # 100-year floodplain
    "A":   1, "AE": 1, "AH": 1, "AO": 1, "AR": 1,
    "A99": 1, "A1": 1,
    # High risk coastal
    "V":   0, "VE": 0,
}

def get_flood_zone(lat: float, lng: float, timeout: int = 8) -> dict:
    """
    Query FEMA NFHL for the flood zone at a given lat/lng.
    Returns: { zone, zone_subtype, score, description }
    """
    try:
        params = {
            "geometry":     f"{lng},{lat}",
            "geometryType": "esriGeometryPoint",
            "spatialRel":   "esriSpatialRelIntersects",
            "outFields":    "FLD_ZONE,ZONE_SUBTY",
            "returnGeometry": "false",
            "f": "json",
        }
        r = requests.get(FEMA_URL, params=params, timeout=timeout)
        r.raise_for_status()
        data = r.json()

        features = data.get("features", [])
        if not features:
            return {"zone": "X", "score": 5, "description": "Outside mapped area — assume minimal risk"}

        attrs = features[0].get("attributes", {})
        zone = (attrs.get("FLD_ZONE") or "X").strip().upper()
        subtype = (attrs.get("ZONE_SUBTY") or "").strip()

        score = ZONE_SCORES.get(zone, 2)
        descriptions = {
            5: "Zone X — Minimal flood risk",
            3: "Zone X500 / D — Moderate risk",
            1: "Zone A/AE — 100-year floodplain",
            0: "Zone V/VE — High coastal risk",
        }
        return {
            "zone": zone,
            "zone_subtype": subtype,
            "score": score,
            "description": descriptions.get(score, f"Zone {zone}"),
        }

    except Exception as e:
        return {"zone": "unknown", "score": 3, "description": f"FEMA lookup failed: {e}"}
