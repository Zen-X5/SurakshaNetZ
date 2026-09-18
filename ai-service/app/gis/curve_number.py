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
    if curve_number <= 0 or curve_number > 100:
        raise ValueError("Curve number must be between 30 and 100.")
    
    retention_s_mm = (25400.0 / curve_number) - 254.0
    return round(retention_s_mm, 2)
