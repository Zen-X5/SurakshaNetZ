"""
MongoDB utility module for location collection management, indexing, and batch operations.
"""

from pymongo import MongoClient, GEOSPHERE, ASCENDING
from scripts.config import MONGO_URI, DB_NAME

def get_mongo_db(uri: str = MONGO_URI, db_name: str = DB_NAME):
    """Establish connection to MongoDB and return database instance."""
    client = MongoClient(uri)
    return client, client[db_name]


def save_locations(locations: list[dict], clear_existing: bool = False, uri: str = MONGO_URI, db_name: str = DB_NAME) -> int:
    """
    Inserts a list of location documents into the locations collection,
    optionally clearing existing records and building 2DSphere spatial indexes.
    """
    if not locations:
        print("⚠️ No locations provided to save.")
        return 0

    print(f"🔌 Connecting to MongoDB: {uri}")
    client, db = get_mongo_db(uri, db_name)
    collection = db["locations"]
    print("✅ Connected\n")

    if clear_existing:
        existing_count = collection.count_documents({})
        if existing_count > 0:
            print(f"🗑️ Clearing {existing_count} existing locations...")
            collection.delete_many({})

    result = collection.insert_many(locations)
    inserted_count = len(result.inserted_ids)
    print(f"🎉 Successfully inserted {inserted_count} locations into collection 'locations'.")

    # Ensure 2DSphere spatial & compound indexes
    print("📐 Creating geospatial 2dsphere indexes...")
    collection.create_index([("boundary", GEOSPHERE)])
    collection.create_index([("centroid", GEOSPHERE)])
    collection.create_index([("name", ASCENDING), ("city", ASCENDING)])
    print("✅ Indexes verified/created.\n")

    # Preview first 10 locations
    print("📍 Collection Preview:")
    for loc in collection.find({}, {"name": 1, "wardCode": 1}).limit(10):
        ward_info = f" (Ward {loc['wardCode']})" if loc.get("wardCode") else ""
        print(f"   • {loc['name']}{ward_info}")

    client.close()
    return inserted_count
