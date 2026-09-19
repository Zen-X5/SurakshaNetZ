"""
Hydrological SCS Runoff Curve Number Solver.
Calculates potential maximum retention S (in mm) based on Curve Number (CN).
Formula: S = (25400 / CN) - 254
"""

def calculate_potential_retention(curve_number: float) -> float:
    """
    Calculate potential maximum retention S (in mm).
    :param curve_number: SCS Curve Number value between 30 and 100.
    :return: Potential retention in mm.
    """
    if curve_number < 30 or curve_number > 100:
        raise ValueError("Curve number must be between 30 and 100.")
    
    retention_s_mm = (25400.0 / curve_number) - 254.0
    return round(retention_s_mm, 2)


def estimate_curve_number(
    land_cover_type: str | None,
    hydrologic_group: str | None,
    impervious_pct: float | None,
) -> float | None:
    """Estimate CN from normalized land cover, soil group, and imperviousness."""
    if not land_cover_type or not hydrologic_group:
        return None

    group = hydrologic_group.upper()
    base_values = {
        "Vegetation": {"A": 39, "B": 61, "C": 74, "D": 80},
        "Built-up": {"A": 89, "B": 92, "C": 94, "D": 95},
        "Water/Wetland": {"A": 98, "B": 98, "C": 99, "D": 100},
        "Other": {"A": 55, "B": 70, "C": 80, "D": 85},
    }
    if land_cover_type not in base_values or group not in base_values[land_cover_type]:
        return None

    impervious = max(0.0, min(100.0, impervious_pct or 0.0))
    base = base_values[land_cover_type][group]
    curve_number = base * (1 - impervious / 100) + 98 * (impervious / 100)
    return round(max(30.0, min(100.0, curve_number)), 2)
