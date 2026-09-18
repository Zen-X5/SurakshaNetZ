from fastapi import APIRouter
from app.gis.jalukbari_gis import get_jalukbari_gis_features

router = APIRouter(prefix="/api/v1/gis", tags=["GIS Analysis"])

@router.get("/jalukbari")
def read_jalukbari_features():
    """
    Returns spatial GIS features & hydrological retention index for Jalukbari.
    """
    return get_jalukbari_gis_features()
