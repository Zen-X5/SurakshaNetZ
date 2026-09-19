"""Elevation and slope provider using sampled public DEM elevations."""

from __future__ import annotations

import math
from typing import Any

from app.gis.http_client import get_json

OPEN_ELEVATION_URL = "https://api.open-elevation.com/api/v1/lookup"


def get_elevation_and_slope(centroid: dict[str, Any]) -> tuple[float | None, float | None]:
    """Sample a 3x3 DEM grid and calculate a local slope in degrees."""
    longitude, latitude = centroid["coordinates"]
    step = 0.002
    points = [
        {"latitude": latitude + row * step, "longitude": longitude + column * step}
        for row in (-1, 0, 1)
        for column in (-1, 0, 1)
    ]
    payload = get_json(
        OPEN_ELEVATION_URL,
        params={"locations": "|".join(f"{point['latitude']},{point['longitude']}" for point in points)},
    )
    results = payload.get("results", []) if isinstance(payload, dict) else []
    if len(results) != 9:
        return None, None

    elevations = [float(result["elevation"]) for result in results]
    center_elevation = round(elevations[4], 2)
    horizontal_step_m = step * 111_320 * math.cos(math.radians(latitude))
    vertical_step_m = step * 110_540
    east_west_gradient = (elevations[5] - elevations[3]) / (2 * horizontal_step_m)
    north_south_gradient = (elevations[7] - elevations[1]) / (2 * vertical_step_m)
    slope_degrees = math.degrees(math.atan((east_west_gradient**2 + north_south_gradient**2) ** 0.5))
    return center_elevation, round(slope_degrees, 2)


def get_elevation(centroid: dict[str, Any]) -> float | None:
    elevation, _ = get_elevation_and_slope(centroid)
    return elevation