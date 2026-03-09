"""
Scoring engine for pipeline site candidates.
Mirrors the JavaScript scoring in site-intel.html exactly so scores match.
"""
import math

WEIGHTS = {
    "pipeline": 25,
    "flood":    20,
    "size":     15,
    "power":    15,
    "zoning":   15,
    "road":     10,
}

ZONING_SCORES = {
    "industrial":   5,
    "agricultural": 4,
    "commercial":   3,
    "mixed":        2,
    "residential":  1,
    "unknown":      1,
}

MAXES = {
    "pipeline": 5,
    "flood":    5,
    "size":     5,
    "power":    5,
    "zoning":   5,
    "road":     3,
}


def score_site(site: dict) -> dict:
    """
    Score a site dict. Returns augmented dict with score, tier, breakdown.
    site keys: pipeline, flood, size, power, zoning, road (all int or str int)
    """
    raw = {
        "pipeline": int(site.get("pipeline", 0)),
        "flood":    int(site.get("flood",    0)),
        "size":     int(site.get("size",     0)),
        "power":    int(site.get("power",    0)),
        "zoning":   ZONING_SCORES.get(str(site.get("zoning", "unknown")).lower(), 1),
        "road":     int(site.get("road",     0)),
    }

    total = 0
    breakdown = {}
    for k, w in WEIGHTS.items():
        pts = round((raw[k] / MAXES[k]) * w)
        breakdown[k] = {"raw": raw[k], "max": MAXES[k], "weight": w, "pts": pts}
        total += pts

    tier = get_tier(total)
    return {**site, "score": total, "tier": tier["tier"], "tier_label": tier["label"], "breakdown": breakdown}


def get_tier(score: int) -> dict:
    if score >= 80:
        return {"tier": "A", "label": "Top Priority",         "color": "#00e87a"}
    if score >= 60:
        return {"tier": "B", "label": "Strong Candidate",     "color": "#3b9eff"}
    if score >= 40:
        return {"tier": "C", "label": "Investigate Further",  "color": "#f5a623"}
    return     {"tier": "D", "label": "Low Priority",          "color": "#ff4d6d"}


def pipeline_distance_score(miles: float) -> int:
    """Convert miles to pipeline score tier."""
    if miles < 0.1:  return 5
    if miles < 0.5:  return 4
    if miles < 1.0:  return 3
    if miles < 2.0:  return 2
    if miles < 5.0:  return 1
    return 0


def haversine_miles(lat1, lng1, lat2, lng2) -> float:
    """Distance in miles between two lat/lng points."""
    R = 3958.8
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
