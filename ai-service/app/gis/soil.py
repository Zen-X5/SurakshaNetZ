"""Fetch shallow soil texture from the SoilGrids API."""

from __future__ import annotations

from typing import Any

from app.gis.http_client import get_json

SOILGRIDS_URL = "https://rest.isric.org/soilgrids/v2.0/properties/query"


def _mean_layer_value(payload: dict[str, Any], layer_name: str) -> float | None:
    for layer in payload.get("properties", {}).get("layers", []):
        if layer.get("name") != layer_name:
            continue
        for depth in layer.get("depths", []):
            if depth.get("label") == "0-5cm":
                value = depth.get("values", {}).get("mean")
                return float(value) if value is not None else None
    return None


def get_soil_profile(centroid: dict[str, Any]) -> dict[str, Any]:
    longitude, latitude = centroid["coordinates"]
    payload = get_json(
        SOILGRIDS_URL,
        params={
            "lon": longitude,
            "lat": latitude,
            "property": ["clay", "sand", "silt"],
            "depth": "0-5cm",
            "value": "mean",
        },
    )
    if not isinstance(payload, dict):
        return {"type": None, "hydrologic_group": None}

    clay = _mean_layer_value(payload, "clay")
    sand = _mean_layer_value(payload, "sand")
    silt = _mean_layer_value(payload, "silt")
    if clay is None or sand is None or silt is None:
        return {"type": None, "hydrologic_group": None}

    if clay >= 40:
        soil_type, hydrologic_group = "Clay-rich soil", "D"
    elif sand >= 70:
        soil_type, hydrologic_group = "Sandy soil", "A"
    elif clay >= 25:
        soil_type, hydrologic_group = "Loam/clay soil", "C"
    else:
        soil_type, hydrologic_group = "Loamy soil", "B"

    return {"type": soil_type, "hydrologic_group": hydrologic_group}