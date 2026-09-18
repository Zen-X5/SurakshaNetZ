"""
seed_locations_from_osm.py

Fetches Guwahati ward/locality boundaries from OpenStreetMap
via the Overpass API, transforms them to match the Location schema,
and inserts them into MongoDB.

Usage:
    pip install pymongo requests
    python scripts/seed_locations_from_osm.py

Set MONGO_URI env var to override the default connection string.
"""

import os
import sys
import requests
from pymongo import MongoClient, GEOSPHERE, ASCENDING

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/surakshanetz")
DB_NAME = os.getenv("DB_NAME", "surakshanetz")
OVERPASS_API = "https://overpass-api.de/api/interpreter"

# Overpass QL query — Guwahati bounding box (works with raw HTTP)
OVERPASS_QUERY = """
[out:json][timeout:60];
(
  rel["boundary"="administrative"]["admin_level"="10"](26.10,91.60,26.25,91.85);
  rel["boundary"="administrative"]["admin_level"="9"](26.10,91.60,26.25,91.85);
);
out geom;
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def fetch_from_overpass() -> list[dict]:
    """Fetch Guwahati boundaries from the Overpass API."""
    print("📡 Fetching Guwahati boundaries from Overpass API...")

    response = requests.post(
        OVERPASS_API,
        data={"data": OVERPASS_QUERY},
        timeout=90,
    )
    response.raise_for_status()

    data = response.json()
    elements = data.get("elements", [])
    print(f"✅ Received {len(elements)} elements from OSM\n")
    return elements


def extract_polygon_from_relation(element: dict) -> list[list[list[float]]] | None:
    """
    Convert an Overpass relation's outer members into a GeoJSON Polygon
    coordinate ring: [[lng, lat], [lng, lat], ...]
    """
    members = element.get("members", [])
    if not members:
        return None

    # Collect all "outer" way geometries
    outer_ring: list[list[float]] = []

    for member in members:
        if member.get("role") == "outer" and "geometry" in member:
            for node in member["geometry"]:
                outer_ring.append([node["lon"], node["lat"]])  # GeoJSON = [lng, lat]

    if len(outer_ring) < 4:
        return None

    # Ensure the ring is closed
    if outer_ring[0] != outer_ring[-1]:
        outer_ring.append(list(outer_ring[0]))

    return [outer_ring]  # GeoJSON Polygon: array of rings


def compute_centroid(ring: list[list[float]]) -> list[float]:
    """Compute centroid of a polygon ring (simple average, excluding closing point)."""
    count = len(ring) - 1  # exclude the closing duplicate point
    if count <= 0:
        return [0.0, 0.0]

    sum_lng = sum(pt[0] for pt in ring[:count])
    sum_lat = sum(pt[1] for pt in ring[:count])

    return [sum_lng / count, sum_lat / count]  # [lng, lat]


def transform_to_locations(elements: list[dict]) -> list[dict]:
    """Transform Overpass elements into Location documents."""
    locations = []

    for element in elements:
        if element.get("type") != "relation":
            continue

        tags = element.get("tags", {})
        name = tags.get("name") or tags.get("name:en") or f"Ward {element['id']}"
        ward_code = tags.get("ref") or tags.get("ref:ward") or None

        coordinates = extract_polygon_from_relation(element)
        if not coordinates:
            print(f"  ⚠️  Skipping \"{name}\" — could not extract polygon")
            continue

        centroid = compute_centroid(coordinates[0])

        location = {
            "name": name,
            "city": "Guwahati",
            "state": "Assam",
            "boundary": {
                "type": "Polygon",
                "coordinates": coordinates,
            },
            "centroid": {
                "type": "Point",
                "coordinates": centroid,
            },
            "staticFeatures": {
                "sourceNotes": f"OpenStreetMap relation/{element['id']}",
            },
        }

        if ward_code:
            location["wardCode"] = ward_code

        locations.append(location)
        pts = len(coordinates[0])
        ward_info = f" (Ward {ward_code})" if ward_code else ""
        print(f"  ✔ {name}{ward_info} — {pts} points")

    return locations


def print_manual_steps():
    """Print manual alternative instructions."""
    print("""
╔══════════════════════════════════════════════════════════╗
║  Manual Alternative: Overpass Turbo                      ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  1. Go to https://overpass-turbo.eu/                     ║
║                                                          ║
║  2. Paste this query:                                    ║
║                                                          ║
║     [out:json][timeout:60];                              ║
║     {{geocodeArea:Guwahati}}->.searchArea;               ║
║     (                                                    ║
║       rel["boundary"="administrative"]                   ║
║          ["admin_level"="10"](area.searchArea);          ║
║     );                                                   ║
║     out geom;                                            ║
║                                                          ║
║  3. Click "Run"                                          ║
║                                                          ║
║  4. Click "Export" → "Download as GeoJSON"               ║
║                                                          ║
║  5. Save the file, then run:                             ║
║     python scripts/import_geojson.py <file.geojson>      ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
""")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=" * 60)
    print("  SurakshaNetZ — OSM Location Seeder (Python)")
    print("=" * 60)
    print()

    # 1. Fetch from Overpass
    elements = fetch_from_overpass()

    if not elements:
        print("❌ No boundary data found. See manual steps below.")
        print_manual_steps()
        sys.exit(1)

    # 2. Transform to Location documents
    print("\n🔄 Transforming to Location schema format...\n")
    locations = transform_to_locations(elements)

    if not locations:
        print("❌ No valid polygons could be extracted.")
        print_manual_steps()
        sys.exit(1)

    print(f"\n📋 {len(locations)} locations ready to seed\n")

    # 3. Connect to MongoDB and insert
    print(f"🔌 Connecting to MongoDB: {MONGO_URI}")
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db["locations"]
    print("✅ Connected\n")

    # Clear existing data (comment out to append instead)
    existing = collection.count_documents({})
    if existing > 0:
        print(f"🗑️  Clearing {existing} existing locations...")
        collection.delete_many({})

    # Insert
    result = collection.insert_many(locations)
    print(f"\n🎉 Successfully seeded {len(result.inserted_ids)} locations!")

    # Create indexes
    print("📐 Creating geospatial indexes...")
    collection.create_index([("boundary", GEOSPHERE)])
    collection.create_index([("centroid", GEOSPHERE)])
    collection.create_index([("name", ASCENDING), ("city", ASCENDING)])
    print("✅ Indexes created\n")

    # Preview
    print("📍 Preview of seeded locations:")
    for loc in collection.find({}, {"name": 1, "wardCode": 1}).limit(10):
        ward_info = f" (Ward {loc['wardCode']})" if loc.get("wardCode") else ""
        print(f"   • {loc['name']}{ward_info}")

    client.close()
    print("\n✅ Done!")


if __name__ == "__main__":
    main()
