from app.gis.curve_number import calculate_potential_retention

def get_jalukbari_gis_features():
    """
    Returns computed spatial features and hydrological indices for Jalukbari locality.
    """
    curve_num = 82
    retention_s = calculate_potential_retention(curve_num)

    return {
        "location_name": "Jalukbari",
        "city": "Guwahati",
        "centroid": {
            "type": "Point",
            "coordinates": [91.6628, 26.1445]
        },
        "boundary_type": "Polygon",
        "static_features": {
            "elevation_m": 51.2,
            "slope_degrees": 3.5,
            "land_cover_type": "Mixed Educational & Wetland Buffer",
            "soil_type": "Alluvial Clay Silt",
            "impervious_pct": 62,
            "distance_to_river_m": 1200,
            "drainage_density": 1.65,
            "curve_number": curve_num,
            "potential_retention_s_mm": retention_s,
            "source": "Python GIS Engine / Copernicus DEM"
        }
    }
