"""
import_opencity_wards.py

Script to import official Guwahati Municipal Corporation (GMC) 60 Wards dataset
from OpenCity / DataMeet / Bharatlas into MongoDB.

Usage:
    python scripts/import_opencity_wards.py <path-to-opencity-gmc.geojson>
"""

import sys
import json
from pathlib import Path
from scripts.parsers.geojson_parser import parse_geojson_features
from scripts.utils.mongo_client import save_locations


def main():
    print("=" * 60)
    print("  SurakshaNetZ — GMC Official Wards Importer (OpenCity)")
    print("=" * 60)
    print()

    if len(sys.argv) < 2:
        print("❌ Please provide the path to your OpenCity GeoJSON file.")
        print("\nUsage:")
        print("  python scripts/import_opencity_wards.py path/to/gmc_60_wards.geojson")
        print("\n📥 How to download OpenCity GMC Wards GeoJSON:")
        print("  1. Visit OpenCity (opencity.in) or Bharatlas (bharatlas.com)")
        print("  2. Search for 'Guwahati GMC 60 Ward Map'")
        print("  3. Download as GeoJSON and run this command!")
        sys.exit(1)

    file_path = Path(sys.argv[1]).resolve()
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        sys.exit(1)

    print(f"📂 Loading OpenCity GMC GeoJSON: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        geojson_data = json.load(f)

    if geojson_data.get("type") != "FeatureCollection" or not isinstance(geojson_data.get("features"), list):
        print("❌ Invalid GeoJSON format. Expected a FeatureCollection.")
        sys.exit(1)

    features = geojson_data["features"]
    print(f"✅ Found {len(features)} GMC ward features\n")

    locations = parse_geojson_features(features, source_name=f"OpenCity / GMC ({file_path.name})")

    if not locations:
        print("❌ No valid ward polygons extracted.")
        sys.exit(1)

    print(f"\n📋 Successfully transformed {len(locations)} official GMC Wards.\n")

    # Insert into MongoDB (clearing old unverified OSM locations if present)
    save_locations(locations, clear_existing=True)
    print("\n🎉 All 60 Official GMC Wards imported into MongoDB successfully!")


if __name__ == "__main__":
    main()
