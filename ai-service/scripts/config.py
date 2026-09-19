import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/surakshanetz")
DB_NAME = os.getenv("DB_NAME", "surakshanetz")
OVERPASS_API = os.getenv("OVERPASS_API", "https://overpass-api.de/api/interpreter")

# Default Guwahati bounding box (South-West to North-East: lat_min, lng_min, lat_max, lng_max)
DEFAULT_GUWAHATI_BBOX = (26.10, 91.60, 26.25, 91.85)

# Default Overpass QL Query for Guwahati administrative ward boundaries
DEFAULT_OVERPASS_QUERY = """
[out:json][timeout:60];
(
  rel["boundary"="administrative"]["admin_level"="10"](26.10,91.60,26.25,91.85);
  rel["boundary"="administrative"]["admin_level"="9"](26.10,91.60,26.25,91.85);
);
out geom;
"""
