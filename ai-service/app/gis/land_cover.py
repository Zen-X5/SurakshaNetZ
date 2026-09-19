"""Estimate land cover and imperviousness from OpenStreetMap features."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from shapely.geometry import LineString, Point, Polygon, shape

from app.gis.http_client import get_json

OVERPASS_URL = "https://overpass-api.de/api/interpreter"


def _element_geometry(element: dict[str, Any]):
    geometry = element.get("geometry", [])
    if not geometry:
        return None
    coordinates = [[point["lon"], point["lat"]] for point in geometry]
    if len(coordinates) >= 4 and coordinates[0] == coordinates[-1]:
        return Polygon(coordinates)
    if len(coordinates) >= 2:
        return LineString(coordinates).buffer(0.00003)
    return Point(coordinates[0])


def get_land_cover(boundary: dict[str, Any], centroid: dict[str, Any]) -> dict[str, Any]:
    longitude, latitude = centroid["coordinates"]
    query = f"""
    [out:json][timeout:60];
    (
      nwr["landuse"](around:5000,{latitude},{longitude});
      nwr["natural"](around:5000,{latitude},{longitude});
      way["building"](around:5000,{latitude},{longitude});
      way["highway"](around:5000,{latitude},{longitude});
    );
    out geom;
    """
    payload = get_json(OVERPASS_URL, data={"data": query})
    target = shape(boundary)
    areas: dict[str, float] = defaultdict(float)

    for element in payload.get("elements", []) if isinstance(payload, dict) else []:
        geometry = _element_geometry(element)
        if geometry is None:
            continue
        clipped_area = geometry.intersection(target).area
        if clipped_area <= 0:
            continue

        tags = element.get("tags", {})
        landuse = tags.get("landuse")
        natural = tags.get("natural")
        if "building" in tags or "highway" in tags or landuse in {"residential", "commercial", "industrial", "retail"}:
            category = "Built-up"
        elif natural in {"water", "wetland"} or landuse in {"reservoir", "basin"}:
            category = "Water/Wetland"
        elif landuse in {"forest", "farmland", "grass", "meadow", "orchard", "greenfield"} or natural in {"wood", "scrub", "heath"}:
            category = "Vegetation"
        else:
            category = "Other"
        areas[category] += clipped_area

    if not areas:
        return {"type": None, "impervious_pct": None}

    dominant_type = max(areas, key=areas.get)
    mapped_area = sum(areas.values())
    impervious_pct = min(100.0, round((areas.get("Built-up", 0.0) / mapped_area) * 100, 2))
    return {"type": dominant_type, "impervious_pct": impervious_pct}