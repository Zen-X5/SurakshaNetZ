"""
Geometry helper functions for spatial operations and coordinate transformations.
"""

def compute_centroid(ring: list[list[float]]) -> list[float]:
    """
    Compute centroid of a polygon ring (simple average, excluding closing duplicate point).
    Coordinates are expected in GeoJSON order: [longitude, latitude].
    """
    count = len(ring) - 1
    if count <= 0:
        return [0.0, 0.0]

    sum_lng = sum(pt[0] for pt in ring[:count])
    sum_lat = sum(pt[1] for pt in ring[:count])

    return [sum_lng / count, sum_lat / count]


def close_ring(ring: list[list[float]]) -> list[list[float]]:
    """Ensure that the first and last points of a linear ring are identical."""
    if not ring:
        return ring
    if ring[0] != ring[-1]:
        ring.append(list(ring[0]))
    return ring


def extract_polygon_from_relation(element: dict) -> list[list[list[float]]] | None:
    """
    Convert an Overpass relation's outer members into a GeoJSON Polygon
    coordinate ring: [[[lng, lat], [lng, lat], ...]]
    """
    members = element.get("members", [])
    if not members:
        return None

    outer_ring: list[list[float]] = []

    for member in members:
        if member.get("role") == "outer" and "geometry" in member:
            for node in member["geometry"]:
                outer_ring.append([node["lon"], node["lat"]])

    if len(outer_ring) < 4:
        return None

    outer_ring = close_ring(outer_ring)
    return [outer_ring]
