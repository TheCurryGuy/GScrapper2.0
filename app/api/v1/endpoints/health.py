from fastapi import APIRouter
from datetime import datetime
from app.models.response import HealthResponse
from app.services.aggregator import AggregatorService
from app.core.config import settings

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    aggregator = AggregatorService()
    services_status = await aggregator.health_check()
    
    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
        timestamp=datetime.utcnow(),
        services=services_status
    )
