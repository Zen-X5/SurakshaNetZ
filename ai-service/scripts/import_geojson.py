"""
import_geojson.py

CLI command to import a local GeoJSON file (exported from Overpass Turbo or QGIS)
into the MongoDB `locations` collection matching the Location schema.

Usage:
    python scripts/import_geojson.py <path-to-file.geojson>
"""

import json
import sys
from pathlib import Path

from scripts.parsers.geojson_parser import parse_geojson_features
from scripts.utils.mongo_client import save_locations


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

    if geojson.get("type") != "FeatureCollection" or not isinstance(geojson.get("features"), list):
        print("❌ Invalid GeoJSON format: Expected a FeatureCollection")
        sys.exit(1)

    features = geojson["features"]
    print(f"✅ Found {len(features)} features\n")

    locations = parse_geojson_features(features, source_name=file_path.name)
    if not locations:
        print("❌ No valid Polygon features found.")
        sys.exit(1)

    save_locations(locations, clear_existing=False)
    print("\n✅ GeoJSON Import Complete!")


if __name__ == "__main__":
    main()
