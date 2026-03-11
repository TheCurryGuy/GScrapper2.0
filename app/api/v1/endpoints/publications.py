from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.models.request import AuthorRequest
from app.models.response import AuthorResponse
from app.services.aggregator import AggregatorService
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("/search", response_model=AuthorResponse)
async def search_author_publications(
    request: AuthorRequest
):
    logger.info(f"Received search request for: {request.name}")
    
    try:
        aggregator = AggregatorService()
        response = await aggregator.search_all_sources(
            name=request.name,
            email=request.email,
            orcid_id=request.orcid_id
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Search failed for {request.name}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/search/advanced", response_model=AuthorResponse)
async def search_by_author_id(
    author_id: str = Query(..., description="Google Scholar author ID"),
    author_name: Optional[str] = Query(None, description="Optional author name")
):
    logger.info(f"Received advanced search request for author ID: {author_id}")
    
    try:
        aggregator = AggregatorService()
        response = await aggregator.search_by_author_id(
            author_id=author_id,
            author_name=author_name
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Advanced search failed for author ID {author_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Advanced search failed: {str(e)}")
