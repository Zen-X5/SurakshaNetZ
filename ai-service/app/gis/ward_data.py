"""Fetch and normalize administrative ward geometries."""

from __future__ import annotations

from typing import Any

from app.gis.http_client import get_json
from scripts.utils.geometry import extract_polygon_from_relation

OVERPASS_URL = "https://overpass-api.de/api/interpreter"


def get_ward_features(centroid: dict[str, Any]) -> list[dict[str, Any]]:
    longitude, latitude = centroid["coordinates"]
    query = f"""
    [out:json][timeout:45];
    relation["boundary"="administrative"]["admin_level"~"9|10"](around:10000,{latitude},{longitude});
    out geom;
    """
    payload = get_json(OVERPASS_URL, data={"data": query})
    features = []

    for element in payload.get("elements", []) if isinstance(payload, dict) else []:
        geometry = extract_polygon_from_relation(element)
        if not geometry:
            continue

        tags = element.get("tags", {})
        ward_code = tags.get("ref") or tags.get("ward_no") or tags.get("gmc_ward")
        if not ward_code:
            continue

        features.append({
            "properties": {"wardCode": str(ward_code)},
            "geometry": {"type": "Polygon", "coordinates": geometry},
        })

    return features