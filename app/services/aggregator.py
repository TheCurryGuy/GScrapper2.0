import asyncio
from datetime import datetime
from typing import List, Optional
from app.services.base import BaseAcademicService
from app.services.openalex import OpenAlexService
from app.services.crossref import CrossRefService
from app.services.google_scholar import GoogleScholarService
from app.models.response import Publication, AuthorMetrics, AuthorResponse
from app.utils.deduplication import deduplicate_publications
from app.core.logging import get_logger


class AggregatorService:
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.services = {
            'openalex': OpenAlexService(),
            'crossref': CrossRefService(),
        }
        self.google_scholar = GoogleScholarService()
    
    async def search_all_sources(
        self,
        name: str,
        email: str,
        orcid_id: Optional[str] = None
    ) -> AuthorResponse:
        self.logger.info(f"Starting comprehensive search for: {name}")
        
        tasks = []
        
        for service_name, service in self.services.items():
            task = asyncio.create_task(
                self._safe_search(service.search_by_name(name, email), service_name)
            )
            tasks.append(task)
        
        if orcid_id:
            for service_name, service in self.services.items():
                task = asyncio.create_task(
                    self._safe_search(service.search_by_orcid(orcid_id), f"{service_name}_orcid")
                )
                tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        all_publications = []
        sources_queried = set()
        
        for result in results:
            if isinstance(result, list):
                all_publications.extend(result)
                if result:
                    sources_queried.add(result[0].source)
        
        deduplicated = deduplicate_publications(all_publications)
        
        metrics = self._calculate_metrics(deduplicated)
        
        deduplicated.sort(key=lambda x: (x.year or 0, x.citations or 0), reverse=True)
        
        self.logger.info(
            f"Search complete: {len(deduplicated)} unique publications "
            f"from {len(sources_queried)} sources"
        )
        
        return AuthorResponse(
            author_name=name,
            email=email,
            orcid_id=orcid_id,
            metrics=metrics,
            publications=deduplicated,
            sources_queried=list(sources_queried),
            query_timestamp=datetime.utcnow(),
            cached=False
        )
    
    async def _safe_search(self, coro, service_name: str) -> List[Publication]:
        try:
            result = await coro
            self.logger.debug(f"{service_name}: {len(result)} results")
            return result
        except Exception as e:
            self.logger.error(f"Error in {service_name}: {e}")
            return []
    
    def _calculate_metrics(self, publications: List[Publication]) -> AuthorMetrics:
        total_pubs = len(publications)
        total_cites = sum(p.citations or 0 for p in publications)
        
        citation_counts = sorted([p.citations or 0 for p in publications], reverse=True)
        h_index = 0
        for i, citations in enumerate(citation_counts, 1):
            if citations >= i:
                h_index = i
            else:
                break
        
        i10_index = sum(1 for p in publications if (p.citations or 0) >= 10)
        
        years = [p.year for p in publications if p.year]
        years_active = max(years) - min(years) + 1 if years else None
        
        avg_citations = total_cites / total_pubs if total_pubs > 0 else 0.0
        
        return AuthorMetrics(
            total_publications=total_pubs,
            total_citations=total_cites,
            h_index=h_index,
            i10_index=i10_index,
            avg_citations_per_paper=round(avg_citations, 2),
            years_active=years_active
        )
    
    async def search_by_author_id(self, author_id: str, author_name: str = None) -> AuthorResponse:
        self.logger.info(f"Advanced search for author ID: {author_id}")
        
        publications, author_metadata = await self.google_scholar.search_by_author_id(author_id)
        
        metrics = self._calculate_metrics(publications)
        
        publications.sort(key=lambda x: (x.citations or 0), reverse=True)
        
        self.logger.info(f"Advanced search complete: {len(publications)} publications from Google Scholar")
        
        return AuthorResponse(
            author_name=author_metadata.get('name') or author_name or f"Author ID: {author_id}",
            email=None,
            orcid_id=None,
            metrics=metrics,
            publications=publications,
            sources_queried=["Google Scholar"],
            query_timestamp=datetime.utcnow(),
            cached=False,
            author_metadata=author_metadata
        )
    
    async def health_check(self) -> dict:
        health_tasks = {
            name: service.health_check()
            for name, service in self.services.items()
        }
        
        results = await asyncio.gather(*health_tasks.values(), return_exceptions=True)
        
        return {
            name: "healthy" if result is True else "unhealthy"
            for name, result in zip(health_tasks.keys(), results)
        }
