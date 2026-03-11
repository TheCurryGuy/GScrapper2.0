from fastapi import APIRouter
from app.api.v1.endpoints import publications, health

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(publications.router, prefix="/publications", tags=["publications"])
