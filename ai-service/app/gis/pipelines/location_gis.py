"""Orchestrate the providers that build a generic location GIS response."""

from __future__ import annotations

from typing import Any

import requests

from app.gis.area_resolver import resolve_area
from app.gis.curve_number import calculate_potential_retention, estimate_curve_number
from app.gis.drainage import get_drainage_density
from app.gis.elevation import get_elevation_and_slope
from app.gis.http_client import REQUEST_HEADERS
from app.gis.land_cover import get_land_cover
from app.gis.river_distance import get_nearest_waterway_distance_m
from app.gis.soil import get_soil_profile
from app.gis.ward_data import OVERPASS_URL, get_ward_features
from app.gis.ward_solver import find_intersecting_wards


def get_location_gis_features(name: str, city: str = "Guwahati", state: str = "Assam") -> dict[str, Any]:
    location = resolve_area(name, city, state)
    source_notes = ["Boundary and centroid: OpenStreetMap Nominatim"]

    try:
        ward_features = get_ward_features(location["centroid"])
        ward_codes = find_intersecting_wards(location["boundary"], ward_features)
        source_notes.append("Ward boundaries: OpenStreetMap Overpass")
    except requests.RequestException:
        ward_codes = []

    try:
        elevation_m, slope_degrees = get_elevation_and_slope(location["centroid"])
        source_notes.append("Elevation and slope: Open-Elevation DEM samples")
    except requests.RequestException:
        elevation_m, slope_degrees = None, None

    try:
        land_cover = get_land_cover(location["boundary"], location["centroid"])
        source_notes.append("Land cover and imperviousness: OpenStreetMap Overpass")
    except requests.RequestException:
        land_cover = {"type": None, "impervious_pct": None}

    try:
        soil = get_soil_profile(location["centroid"])
        source_notes.append("Soil texture: SoilGrids")
    except requests.RequestException:
        soil = {"type": None, "hydrologic_group": None}

    try:
        drainage_density = get_drainage_density(location["boundary"], location["centroid"])
        source_notes.append("Drainage density: OpenStreetMap Overpass")
    except requests.RequestException:
        drainage_density = None

    try:
        distance_to_river_m = get_nearest_waterway_distance_m(
            location["centroid"], OVERPASS_URL, REQUEST_HEADERS
        )
        source_notes.append("Waterway distance: OpenStreetMap Overpass")
    except requests.RequestException:
        distance_to_river_m = None

    curve_number = estimate_curve_number(
        land_cover["type"], soil["hydrologic_group"], land_cover["impervious_pct"]
    )
    retention_s = calculate_potential_retention(curve_number) if curve_number is not None else None

    return {
        "location_name": location["name"],
        "city": location["city"],
        "state": location["state"],
        "ward_codes": ward_codes,
        "boundary": location["boundary"],
        "centroid": location["centroid"],
        "static_features": {
            "elevation_m": elevation_m,
            "slope_degrees": slope_degrees,
            "land_cover_type": land_cover["type"],
            "soil_type": soil["type"],
            "impervious_pct": land_cover["impervious_pct"],
            "distance_to_river_m": distance_to_river_m,
            "drainage_density": drainage_density,
            "curve_number": curve_number,
            "potential_retention_s_mm": retention_s,
            "source": "; ".join(source_notes),
        },
    }