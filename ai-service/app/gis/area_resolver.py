from __future__ import annotations
from typing import Any
from shapely.geometry import shape
from app.gis.http_client import get_json
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"


def _largest_polygon(geometry: dict[str, Any]) -> dict[str, Any]:
    if geometry.get("type") == "Polygon":
        return geometry

    if geometry.get("type") != "MultiPolygon":
        raise ValueError("The geocoder returned a non-polygon area")

    polygons = [{"type": "Polygon", "coordinates": polygon} for polygon in geometry.get("coordinates", [])]
    if not polygons:
        raise ValueError("The geocoder returned an empty multipolygon")

    return max(polygons, key=lambda polygon: shape(polygon).area)


def resolve_area(name: str, city: str, state: str) -> dict[str, Any]:
    results = get_json(
        NOMINATIM_URL,
        params={
            "q": f"{name}, {city}, {state}, India",
            "format": "jsonv2",
            "polygon_geojson": 1,
            "addressdetails": 1,
            "limit": 1,
        },
    )
    if not isinstance(results, list) or not results:
        raise ValueError(f"No polygon area found for '{name}'")

    result = results[0]
    boundary = _largest_polygon(result.get("geojson", {}))
    centroid = shape(boundary).centroid
    address = result.get("address", {})

    return {
        "name": name,
        "city": address.get("city") or address.get("town") or address.get("municipality") or city,
        "state": address.get("state") or state,
        "boundary": boundary,
        "centroid": {"type": "Point", "coordinates": [centroid.x, centroid.y]},
    }