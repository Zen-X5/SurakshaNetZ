"""
seed_locations_from_osm.py

Fetches Guwahati ward/locality boundaries from OpenStreetMap
via the Overpass API, transforms them to match the Location schema,
and inserts them into MongoDB.

Usage:
    python scripts/seed_locations_from_osm.py
"""

import sys
from scripts.services.overpass_service import fetch_overpass_elements
from scripts.parsers.osm_parser import parse_osm_elements
from scripts.utils.mongo_client import save_locations


def print_manual_instructions():
    print("""
╔══════════════════════════════════════════════════════════╗
║  Manual Alternative: Overpass Turbo                      ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  1. Go to https://overpass-turbo.eu/                     ║
║  2. Run query:                                           ║
║     rel["boundary"="administrative"]["admin_level"="10"] ║
║        (26.10,91.60,26.25,91.85); out geom;              ║
║  3. Export → Download as GeoJSON                         ║
║  4. Run: python scripts/import_geojson.py <file.geojson> ║
╚══════════════════════════════════════════════════════════╝
""")


def main():
    print("=" * 60)
    print("  SurakshaNetZ — OSM Location Seeder (Modular)")
    print("=" * 60)
    print()

    # 1. Fetch from Overpass
    elements = fetch_overpass_elements()
    if not elements:
        print("❌ No boundary data found.")
        print_manual_instructions()
        sys.exit(1)

    # 2. Transform to Location schema
    print("🔄 Transforming OSM elements to Location documents...\n")
    locations = parse_osm_elements(elements)
    if not locations:
        print("❌ Could not extract valid polygon geometries.")
        print_manual_instructions()
        sys.exit(1)

    print(f"\n📋 {len(locations)} locations ready to seed\n")

    # 3. Save to MongoDB & create indexes
    save_locations(locations, clear_existing=True)
    print("\n✅ Location Seeding Complete!")


if __name__ == "__main__":
    main()
