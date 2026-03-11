from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime


class Publication(BaseModel):
    title: str
    authors: List[str]
    year: Optional[int] = None
    venue: Optional[str] = None
    publication_type: Optional[str] = None
    doi: Optional[str] = None
    url: Optional[str] = None
    citations: Optional[int] = None
    abstract: Optional[str] = None
    source: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Deep Learning for Natural Language Processing",
                "authors": ["Jane Doe", "John Smith"],
                "year": 2023,
                "venue": "Nature Machine Intelligence",
                "publication_type": "journal-article",
                "doi": "10.1038/s42256-023-00123-4",
                "url": "https://www.nature.com/articles/s42256-023-00123-4",
                "citations": 42,
                "abstract": "This paper explores...",
                "source": "Semantic Scholar"
            }
        }


class AuthorMetrics(BaseModel):
    total_publications: int
    total_citations: int
    h_index: Optional[int] = None
    i10_index: Optional[int] = None
    avg_citations_per_paper: float
    years_active: Optional[int] = None


class AuthorResponse(BaseModel):
    author_name: str
    email: Optional[str] = None
    orcid_id: Optional[str] = None
    metrics: AuthorMetrics
    publications: List[Publication]
    sources_queried: List[str]
    query_timestamp: datetime
    cached: bool = False
    author_metadata: Optional[dict] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "author_name": "Jane Doe",
                "email": "jane.doe@university.edu",
                "orcid_id": "0000-0001-2345-6789",
                "metrics": {
                    "total_publications": 25,
                    "total_citations": 450,
                    "h_index": 12,
                    "i10_index": 15,
                    "avg_citations_per_paper": 18.0,
                    "years_active": 8
                },
                "publications": [],
                "sources_queried": ["Google Scholar", "Semantic Scholar", "OpenAlex", "CrossRef", "ORCID"],
                "query_timestamp": "2025-10-27T22:51:00",
                "cached": False
            }
        }


class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: datetime
    services: dict
