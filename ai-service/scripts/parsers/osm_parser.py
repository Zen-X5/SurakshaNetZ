"""
Parser for transforming OpenStreetMap Overpass elements into Location schema documents.
"""

from scripts.utils.geometry import extract_polygon_from_relation, compute_centroid
from scripts.utils.property_extractor import extract_name, extract_ward_codes

def parse_osm_elements(elements: list[dict]) -> list[dict]:
    """Transform Overpass relation elements into Location documents."""
    locations = []

    for element in elements:
        if element.get("type") != "relation":
            continue

        tags = element.get("tags", {})
        element_id = element.get("id")
        name = extract_name(tags, fallback_id=element_id)
        ward_codes = extract_ward_codes(tags)

        coordinates = extract_polygon_from_relation(element)
        if not coordinates:
            print(f'  ⚠️ Skipping "{name}" — could not extract outer polygon boundary')
            continue

        centroid = compute_centroid(coordinates[0])

        location = {
            "name": name,
            "city": "Guwahati",
            "state": "Assam",
            "wardCodes": ward_codes,
            "boundary": {
                "type": "Polygon",
                "coordinates": coordinates,
            },
            "centroid": {
                "type": "Point",
                "coordinates": centroid,
            },
            "staticFeatures": {
                "sourceNotes": f"OpenStreetMap relation/{element_id}",
            },
        }

        locations.append(location)
        pts = len(coordinates[0])
        ward_info = f" (Wards: {', '.join(ward_codes)})" if ward_codes else ""
        print(f"  ✔ {name}{ward_info} — {pts} boundary points")

    return locations

