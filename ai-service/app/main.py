from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import gis_router

app = FastAPI(
    title="SurakshaNetZ AI & GIS Microservice",
    description="Python engine for GIS data processing, hydrology calculations, and flood predictions.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(gis_router.router)

@app.get("/")
def read_root():
    return {
        "service": "SurakshaNetZ AI-Service",
        "status": "online",
        "documentation": "/docs"
    }
