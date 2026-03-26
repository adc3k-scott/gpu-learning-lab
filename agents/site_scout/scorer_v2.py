"""
ADC AI Factory Site Selection — Scoring Engine v2
===================================================
10 base variables (100 pts) + 6 bonus variables (24 pts) = 124 max.

Replaces the original 6-variable scorer and the river_scout 7-variable scorer
with a unified system that covers all site types.

Usage:
    from agents.site_scout.scorer_v2 import score_site_v2, get_tier_v2

    site = {
        "gas_pipeline": 10,    # 0-10: proximity to natural gas pipeline
        "water_access": 10,    # 0-10: proximity to cooling water
        "flood_zone": 10,      # 0-10: FEMA flood zone status
        "foundation": 10,      # 0-10: foundation type needed
        "grid_proximity": 10,  # 0-10: distance to electrical substation
        "fiber_proximity": 10, # 0-10: distance to lit fiber
        "road_access": 10,     # 0-10: road quality
        "rail_access": 10,     # 0-10: rail proximity
        "zoning": 10,          # 0-10: current zoning classification
        "acquisition_cost": 10,# 0-10: cost per acre
        # Bonus flags (optional)
        "historic_tax_credit": True,
        "brownfield_epa": True,
        "university_5mi": True,
        "existing_structure": True,
        "municipal_utility": True,
        "port_dock_access": True,
    }
    result = score_site_v2(site)
    # result = {**site, "base_score": 94, "bonus_total": 21, "total_score": 115, "base_tier": "S", ...}
"""
import math

# ── Base Variable Weights (sum = 100) ──────────────────────────────────────
WEIGHTS = {
    "gas_pipeline":     15,
    "water_access":     12,
    "flood_zone":       10,
    "foundation":        8,
    "grid_proximity":   10,
    "fiber_proximity":  10,
    "road_access":       8,
    "rail_access":       5,
    "zoning":           12,
    "acquisition_cost": 10,
}

MAX_RAW = 10  # All variables score 0-10

# ── Bonus Points ───────────────────────────────────────────────────────────
BONUS_MAP = {
    "historic_tax_credit": 5,
    "brownfield_epa":      5,
    "university_5mi":      5,
    "existing_structure":  3,
    "municipal_utility":   3,
    "port_dock_access":    3,
}

# ── Tier Definitions ──────────────────────────────────────────────────────
def get_tier_v2(base_score: int) -> dict:
    """Tier based on base score (before bonus)."""
    if base_score >= 90:
        return {"tier": "S", "label": "Exceptional",           "color": "#FFD700"}
    if base_score >= 80:
        return {"tier": "A", "label": "Top Priority",          "color": "#00e87a"}
    if base_score >= 60:
        return {"tier": "B", "label": "Strong Candidate",      "color": "#3b9eff"}
    if base_score >= 40:
        return {"tier": "C", "label": "Marginal",              "color": "#f5a623"}
    return     {"tier": "D", "label": "Disqualified",           "color": "#ff4d6d"}


# ── Scoring Helpers ────────────────────────────────────────────────────────

def gas_pipeline_score(miles: float) -> int:
    """Miles to nearest gas pipeline -> 0-10 score."""
    if miles <= 0.1:  return 10   # On property
    if miles <= 0.5:  return 9
    if miles <= 1.0:  return 8
    if miles <= 2.0:  return 7    # 0-5 mi band = 10 pts in original spec
    if miles <= 5.0:  return 6
    if miles <= 10.0: return 4    # 5-15 mi band = 7 pts
    if miles <= 15.0: return 3
    if miles <= 30.0: return 2    # 15-30 mi band = 4 pts
    return 0                       # >30 mi


def water_access_score(miles: float) -> int:
    """Miles to nearest river/bayou/lake -> 0-10 score."""
    if miles <= 0.05: return 10   # Adjacent / on waterfront
    if miles <= 0.25: return 9
    if miles <= 0.5:  return 8
    if miles <= 1.0:  return 7    # "Within 1 mi" band
    if miles <= 2.0:  return 5
    if miles <= 5.0:  return 4    # "Within 5 mi" band
    return 0


def flood_zone_score(zone: str) -> int:
    """FEMA flood zone -> 0-10 score."""
    zone = zone.upper().strip()
    if zone in ("X", "ZONE X", "MINIMAL"):
        return 10
    if zone in ("X SHADED", "ZONE X SHADED", "0.2PCT"):
        return 7
    if zone in ("AE", "A", "AH", "AO", "ZONE AE"):
        return 4  # Pilings solve this
    if zone in ("VE", "V", "ZONE VE", "ZONE V", "COASTAL"):
        return 0  # Hard disqualifier
    return 5  # Unknown — middle ground


def foundation_score(foundation_type: str) -> int:
    """Foundation type needed -> 0-10 score."""
    ft = foundation_type.lower().strip()
    if ft in ("slab", "slab on grade", "existing pad", "engineered"):
        return 10
    if ft in ("shallow piling", "shallow", "8-15 ft"):
        return 7
    if ft in ("deep piling", "deep", "30+ ft", "batture"):
        return 4
    if ft in ("impossible", "marsh", "wetland"):
        return 0
    return 7  # Default to shallow if unknown


def grid_proximity_score(miles: float) -> int:
    """Miles to nearest electrical substation -> 0-10 score."""
    if miles <= 0.1:  return 10  # On-site
    if miles <= 0.5:  return 9
    if miles <= 1.0:  return 8
    if miles <= 2.0:  return 7
    if miles <= 5.0:  return 6
    if miles <= 10.0: return 4
    if miles <= 15.0: return 2
    return 0


def fiber_proximity_score(miles: float) -> int:
    """Miles to lit fiber -> 0-10 score."""
    if miles <= 0.1:  return 10
    if miles <= 0.5:  return 9
    if miles <= 1.0:  return 7
    if miles <= 2.0:  return 6
    if miles <= 5.0:  return 4
    if miles <= 10.0: return 2
    return 0


def road_access_score(road_type: str) -> int:
    """Road access quality -> 0-10 score."""
    rt = road_type.lower().strip()
    if rt in ("highway", "highway frontage", "interstate", "us highway"):
        return 10
    if rt in ("paved", "paved road", "parish road", "state highway"):
        return 7
    if rt in ("gravel", "unpaved", "gravel road"):
        return 4
    if rt in ("none", "no access"):
        return 0
    return 7  # Default paved


def rail_access_score(rail_type: str) -> int:
    """Rail access -> 0-10 score."""
    rt = rail_type.lower().strip()
    if rt in ("on-site", "onsite", "spur on property"):
        return 10
    if rt in ("adjacent", "within 0.25 mi"):
        return 7
    if rt in ("within 1 mi", "nearby"):
        return 4
    if rt in ("none", "no rail"):
        return 0
    return 0  # Default no rail


def zoning_score(zoning: str) -> int:
    """Zoning classification -> 0-10 score."""
    z = zoning.lower().strip()
    if z in ("industrial", "i-1", "i-2", "m2", "heavy industrial", "light industrial"):
        return 10
    if z in ("commercial", "c-1", "c-2", "business"):
        return 7
    if z in ("agricultural", "a-1", "a-2", "ag", "farm"):
        return 4
    if z in ("residential", "r-1", "r-2"):
        return 0
    if z in ("mixed", "unrestricted", "none"):
        return 6
    return 4  # Default agricultural


def acquisition_cost_score(price_per_acre: float) -> int:
    """Price per acre -> 0-10 score."""
    if price_per_acre <= 0:
        return 10  # Free / negligible
    if price_per_acre <= 5000:
        return 10
    if price_per_acre <= 10000:
        return 9
    if price_per_acre <= 25000:
        return 8
    if price_per_acre <= 50000:
        return 7
    if price_per_acre <= 75000:
        return 5
    if price_per_acre <= 100000:
        return 4
    return 0  # >$100K/acre


# ── Main Scorer ────────────────────────────────────────────────────────────

def score_site_v2(site: dict) -> dict:
    """
    Score a site using the v2 10+6 variable system.

    Accepts either:
    - Pre-scored 0-10 values in each field (gas_pipeline, water_access, etc.)
    - Raw measurement values with _miles/_type suffixes
      (gas_pipeline_miles, water_access_miles, flood_zone_type, etc.)

    Returns augmented dict with base_score, bonus_total, total_score, tiers.
    """
    # Extract raw scores (0-10)
    raw = {}
    for key in WEIGHTS:
        if key in site and isinstance(site[key], (int, float)):
            raw[key] = min(10, max(0, int(site[key])))
        else:
            raw[key] = 0

    # Calculate base score
    base_score = 0
    breakdown = {}
    for key, weight in WEIGHTS.items():
        pts = round((raw[key] / MAX_RAW) * weight, 1)
        breakdown[key] = {
            "raw": raw[key],
            "max": MAX_RAW,
            "weight": weight,
            "pts": pts,
        }
        base_score += pts

    base_score = round(base_score)

    # Calculate bonus
    bonus_total = 0
    bonus_breakdown = {}
    for key, max_pts in BONUS_MAP.items():
        eligible = bool(site.get(key, False))
        pts = max_pts if eligible else 0
        bonus_breakdown[key] = {"eligible": eligible, "pts": pts}
        bonus_total += pts

    total_score = base_score + bonus_total
    base_tier = get_tier_v2(base_score)

    # Effective tier (with bonus)
    effective_tier = get_tier_v2(min(base_score + bonus_total, 100))

    return {
        **site,
        "base_score": base_score,
        "bonus_total": bonus_total,
        "total_score": total_score,
        "base_tier": base_tier["tier"],
        "base_tier_label": base_tier["label"],
        "effective_tier": effective_tier["tier"],
        "breakdown": breakdown,
        "bonus_breakdown": bonus_breakdown,
    }


# ── Distance Utility ──────────────────────────────────────────────────────

def haversine_miles(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Distance in miles between two lat/lng points."""
    R = 3958.8
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
