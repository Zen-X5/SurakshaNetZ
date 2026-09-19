from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.gis.pipelines.location_gis import get_location_gis_features

router = APIRouter(prefix="/api/v1/gis", tags=["GIS Analysis"])


class LocationRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    city: str = Field(default="Guwahati", min_length=2, max_length=120)
    state: str = Field(default="Assam", min_length=2, max_length=120)


@router.post("/locations")
def create_location_features(request: LocationRequest):
    return get_location_gis_features(request.name, request.city, request.state)
