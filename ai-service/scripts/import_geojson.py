"""
import_geojson.py

Import a GeoJSON file (exported from Overpass Turbo or QGIS)
into the MongoDB `locations` collection matching the Location schema.

Usage:
    pip install pymongo
    python scripts/import_geojson.py <path-to-file.geojson>

The GeoJSON should have Features with Polygon or MultiPolygon geometries.
"""

import json
import os
import sys
from pathlib import Path

from pymongo import MongoClient, GEOSPHERE, ASCENDING

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/surakshanetz")
DB_NAME = os.getenv("DB_NAME", "surakshanetz")


def compute_centroid(ring: list[list[float]]) -> list[float]:
    """Compute centroid of a polygon ring (simple average, excluding closing point)."""
    count = len(ring) - 1
    if count <= 0:
        return [0.0, 0.0]

    sum_lng = sum(pt[0] for pt in ring[:count])
    sum_lat = sum(pt[1] for pt in ring[:count])

    return [sum_lng / count, sum_lat / count]


def extract_name(properties: dict, index: int) -> str:
    """Extract a location name from GeoJSON feature properties."""
    for key in ["name", "NAME", "name:en", "ward_name", "WARD_NAME", "label"]:
        if key in properties and properties[key]:
            return str(properties[key])
    return f"Location {index + 1}"


def extract_ward_code(properties: dict) -> str | None:
    """Extract ward code from GeoJSON feature properties."""
    for key in ["ref", "ref:ward", "ward_no", "WARD_NO", "ward_code"]:
        if key in properties and properties[key]:
            return str(properties[key])
    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/import_geojson.py <path-to-file.geojson>")
        sys.exit(1)

    file_path = Path(sys.argv[1]).resolve()

    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        sys.exit(1)

    print(f"📂 Reading GeoJSON from: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        geojson = json.load(f)

    if geojson.get("type") != "FeatureCollection" or not isinstance(
        geojson.get("features"), list
    ):
        print("❌ Invalid GeoJSON: expected a FeatureCollection")
        sys.exit(1)

    features = geojson["features"]
    print(f"✅ Found {len(features)} features\n")

    locations = []

    for i, feature in enumerate(features):
        geometry = feature.get("geometry", {})
        properties = feature.get("properties", {})
        geom_type = geometry.get("type")

        # We need Polygon or MultiPolygon
        if geom_type not in ("Polygon", "MultiPolygon"):
            print(f'  ⚠️  Skipping feature {i} — geometry type is "{geom_type}"')
            continue

        coordinates = geometry["coordinates"]

        # For MultiPolygon, take the polygon with the most points
        if geom_type == "MultiPolygon":
            polygon_coords = max(coordinates, key=lambda poly: len(poly[0]))
        else:
            polygon_coords = coordinates

        name = extract_name(properties, i)
        ward_code = extract_ward_code(properties)
        centroid = compute_centroid(polygon_coords[0])

        location = {
            "name": name,
            "city": "Guwahati",
            "state": "Assam",
            "boundary": {
                "type": "Polygon",
                "coordinates": polygon_coords,
            },
            "centroid": {
                "type": "Point",
                "coordinates": centroid,
            },
            "staticFeatures": {
                "sourceNotes": f"Imported from {file_path.name}",
            },
        }

        if ward_code:
            location["wardCode"] = ward_code

        locations.append(location)

        ward_info = f" (Ward {ward_code})" if ward_code else ""
        print(f"  ✔ {name}{ward_info}")

    if not locations:
        print("\n❌ No valid Polygon features found")
        sys.exit(1)

    print(f"\n📋 {len(locations)} locations ready to import\n")

    # Connect and insert
    print(f"🔌 Connecting to MongoDB: {MONGO_URI}")
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db["locations"]
    print("✅ Connected\n")

    result = collection.insert_many(locations)
    print(f"🎉 Inserted {len(result.inserted_ids)} locations!")

    # Ensure indexes
    print("📐 Creating geospatial indexes...")
    collection.create_index([("boundary", GEOSPHERE)])
    collection.create_index([("centroid", GEOSPHERE)])
    collection.create_index([("name", ASCENDING), ("city", ASCENDING)])
    print("✅ Indexes created\n")

    # Preview
    print("📍 Preview:")
    for loc in collection.find({}, {"name": 1, "wardCode": 1}).limit(10):
        ward_info = f" (Ward {loc['wardCode']})" if loc.get("wardCode") else ""
        print(f"   • {loc['name']}{ward_info}")

    client.close()
    print("\n✅ Done!")


if __name__ == "__main__":
    main()
