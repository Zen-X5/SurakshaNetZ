"""Calculate drainage density from mapped OpenStreetMap waterways."""

from __future__ import annotations

import math
from typing import Any

from shapely.geometry import LineString, shape
from shapely.ops import transform

from app.gis.http_client import get_json

OVERPASS_URL = "https://overpass-api.de/api/interpreter"


def _local_projection(longitude: float, latitude: float):
    x_scale = 111_320 * math.cos(math.radians(latitude))
    y_scale = 110_540
    return lambda x, y, z=None: (x * x_scale, y * y_scale)


def get_drainage_density(boundary: dict[str, Any], centroid: dict[str, Any]) -> float | None:
    longitude, latitude = centroid["coordinates"]
    query = f"""
    [out:json][timeout:60];
    way["waterway"~"river|stream|canal|drain|ditch"](around:5000,{latitude},{longitude});
    out geom;
    """
    payload = get_json(OVERPASS_URL, data={"data": query})
    project = _local_projection(longitude, latitude)
    target = transform(project, shape(boundary))
    total_length_m = 0.0

    for element in payload.get("elements", []) if isinstance(payload, dict) else []:
        points = [[point["lon"], point["lat"]] for point in element.get("geometry", [])]
        if len(points) < 2:
            continue
        total_length_m += transform(project, LineString(points)).intersection(target).length

    if target.area <= 0:
        return None
    return round((total_length_m / 1000) / (target.area / 1_000_000), 4)