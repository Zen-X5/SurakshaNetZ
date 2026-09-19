"""
ward_solver.py

Spatial GIS module for dynamically resolving intersecting municipal ward codes
for any input location boundary using Shapely spatial geometries.
"""

from typing import List, Dict, Any
try:
    from shapely.geometry import shape
    HAS_SHAPELY = True
except ImportError:
    HAS_SHAPELY = False


def find_intersecting_wards(location_polygon: Dict[str, Any], ward_features: List[Dict[str, Any]]) -> List[str]:
    """
    Finds all municipal ward codes whose boundary polygons overlap with the given location polygon.

    :param location_polygon: GeoJSON Polygon dict: {"type": "Polygon", "coordinates": [...]}
    :param ward_features: List of ward features from OpenCity / GMC dataset.
    :return: List of unique matching ward codes e.g. ["WARD-01", "WARD-02", "WARD-06"]
    """
    if not location_polygon or "coordinates" not in location_polygon:
        return []

    matched_wards: List[str] = []

    if HAS_SHAPELY:
        try:
            target_geo = shape(location_polygon)

            for ward_feat in ward_features:
                geometry_dict = ward_feat.get("geometry") or ward_feat.get("boundary")
                properties = ward_feat.get("properties") or ward_feat

                if not geometry_dict:
                    continue

                ward_shape = shape(geometry_dict)

                # Check if target location intersects or overlaps with ward polygon
                if target_geo.intersects(ward_shape):
                    ward_code = (
                        properties.get("wardCode") or 
                        properties.get("WARD_NO") or 
                        properties.get("ward_no") or 
                        properties.get("ref")
                    )

                    if ward_code:
                        formatted_code = (
                            ward_code if str(ward_code).startswith("WARD-") 
                            else f"WARD-{str(ward_code).zfill(2)}"
                        )
                        if formatted_code not in matched_wards:
                            matched_wards.append(formatted_code)

            return sorted(matched_wards)
        except Exception as e:
            print(f"⚠️ Shapely spatial calculation fallback: {e}")

    # Fallback to simple bounding box overlap if Shapely is absent/fails
    return fallback_bbox_intersection(location_polygon, ward_features)


def fallback_bbox_intersection(location_polygon: Dict[str, Any], ward_features: List[Dict[str, Any]]) -> List[str]:
    """Fallback bounding box overlap solver when Shapely is not installed."""
    coords = location_polygon.get("coordinates", [[]])[0]
    if not coords:
        return []

    l_lngs = [pt[0] for pt in coords]
    l_lats = [pt[1] for pt in coords]
    l_min_lng, l_max_lng = min(l_lngs), max(l_lngs)
    l_min_lat, l_max_lat = min(l_lats), max(l_lats)

    matched_wards: List[str] = []

    for ward_feat in ward_features:
        properties = ward_feat.get("properties") or ward_feat
        geom = ward_feat.get("geometry") or ward_feat.get("boundary", {})
        w_coords = geom.get("coordinates", [[]])[0]

        if not w_coords:
            continue

        w_lngs = [pt[0] for pt in w_coords if isinstance(pt, list) and len(pt) >= 2]
        w_lats = [pt[1] for pt in w_coords if isinstance(pt, list) and len(pt) >= 2]

        if not w_lngs or not w_lats:
            continue

        w_min_lng, w_max_lng = min(w_lngs), max(w_lngs)
        w_min_lat, w_max_lat = min(w_lats), max(w_lats)

        # Bounding Box Overlap check
        overlap = not (l_max_lng < w_min_lng or l_min_lng > w_max_lng or l_max_lat < w_min_lat or l_min_lat > w_max_lat)

        if overlap:
            ward_code = (
                properties.get("wardCode") or 
                properties.get("WARD_NO") or 
                properties.get("ward_no") or 
                properties.get("ref")
            )
            if ward_code:
                formatted_code = (
                    ward_code if str(ward_code).startswith("WARD-") 
                    else f"WARD-{str(ward_code).zfill(2)}"
                )
                if formatted_code not in matched_wards:
                    matched_wards.append(formatted_code)

    return sorted(matched_wards)
