"""
Parser for transforming GeoJSON files (from Overpass Turbo or QGIS) into Location schema documents.
"""

from pathlib import Path
from scripts.utils.geometry import compute_centroid
from scripts.utils.property_extractor import extract_name, extract_ward_codes

def parse_geojson_features(features: list[dict], source_name: str = "GeoJSON File") -> list[dict]:
    """Transform list of GeoJSON features into Location schema documents."""
    locations = []

    for i, feature in enumerate(features):
        geometry = feature.get("geometry", {})
        properties = feature.get("properties", {})
        geom_type = geometry.get("type")

        if geom_type not in ("Polygon", "MultiPolygon"):
            print(f'  ⚠️ Skipping feature {i} — geometry type is "{geom_type}"')
            continue

        coordinates = geometry["coordinates"]

        if geom_type == "MultiPolygon":
            polygon_coords = max(coordinates, key=lambda poly: len(poly[0]))
        else:
            polygon_coords = coordinates

        name = extract_name(properties, fallback_index=i)
        ward_codes = extract_ward_codes(properties)
        centroid = compute_centroid(polygon_coords[0])

        location = {
            "name": name,
            "city": "Guwahati",
            "state": "Assam",
            "wardCodes": ward_codes,
            "boundary": {
                "type": "Polygon",
                "coordinates": polygon_coords,
            },
            "centroid": {
                "type": "Point",
                "coordinates": centroid,
            },
            "staticFeatures": {
                "sourceNotes": f"Imported from {source_name}",
            },
        }

        locations.append(location)
        ward_info = f" (Wards: {', '.join(ward_codes)})" if ward_codes else ""
        print(f"  ✔ {name}{ward_info}")

    return locations

