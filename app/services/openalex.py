import httpx
from typing import List, Optional
from app.services.base import BaseAcademicService
from app.models.response import Publication
from app.core.config import settings


class OpenAlexService(BaseAcademicService):
    
    BASE_URL = "https://api.openalex.org"
    
    async def search_by_name(self, name: str, email: Optional[str] = None) -> List[Publication]:
        try:
            mailto = email or settings.OPENALEX_EMAIL
            async with httpx.AsyncClient(timeout=30.0) as client:
                author_url = f"{self.BASE_URL}/authors"
                params = {
                    "search": name,
                    "mailto": mailto
                }
                
                response = await client.get(author_url, params=params)
                response.raise_for_status()
                
                authors = response.json().get('results', [])
                if not authors:
                    self.logger.info(f"No author found for: {name}")
                    return []
                
                author_id = authors[0]['id']
                
                works_url = f"{self.BASE_URL}/works"
                params = {
                    "filter": f"author.id:{author_id}",
                    "mailto": mailto,
                    "per-page": 200
                }
                
                works_response = await client.get(works_url, params=params)
                works_response.raise_for_status()
                
                works = works_response.json().get('results', [])
                
                publications = []
                for work in works:
                    venue = None
                    primary_location = work.get('primary_location')
                    if primary_location and isinstance(primary_location, dict):
                        source = primary_location.get('source')
                        if source and isinstance(source, dict):
                            venue = source.get('display_name')
                    
                    pub = Publication(
                        title=work.get('display_name', 'Unknown Title'),
                        authors=[a['author']['display_name'] for a in work.get('authorships', []) if a.get('author')],
                        year=work.get('publication_year'),
                        venue=venue,
                        publication_type=work.get('type'),
                        doi=work.get('doi', '').replace('https://doi.org/', '') if work.get('doi') else None,
                        url=work.get('doi') or work.get('id'),
                        citations=work.get('cited_by_count', 0),
                        abstract=None,
                        source="OpenAlex"
                    )
                    publications.append(pub)
                
                self.logger.info(f"Found {len(publications)} works from OpenAlex for {name}")
                return publications
                
        except Exception as e:
            return self._handle_error(e, f"search_by_name({name})")
    
    async def search_by_orcid(self, orcid_id: str) -> List[Publication]:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                works_url = f"{self.BASE_URL}/works"
                params = {
                    "filter": f"author.orcid:{orcid_id}",
                    "mailto": settings.OPENALEX_EMAIL,
                    "per-page": 200
                }
                
                response = await client.get(works_url, params=params)
                response.raise_for_status()
                
                works = response.json().get('results', [])
                
                publications = []
                for work in works:
                    venue = None
                    primary_location = work.get('primary_location')
                    if primary_location and isinstance(primary_location, dict):
                        source = primary_location.get('source')
                        if source and isinstance(source, dict):
                            venue = source.get('display_name')
                    
                    pub = Publication(
                        title=work.get('display_name', 'Unknown Title'),
                        authors=[a['author']['display_name'] for a in work.get('authorships', []) if a.get('author')],
                        year=work.get('publication_year'),
                        venue=venue,
                        publication_type=work.get('type'),
                        doi=work.get('doi', '').replace('https://doi.org/', '') if work.get('doi') else None,
                        url=work.get('doi') or work.get('id'),
                        citations=work.get('cited_by_count', 0),
                        abstract=None,
                        source="OpenAlex"
                    )
                    publications.append(pub)
                
                self.logger.info(f"Found {len(publications)} works from OpenAlex for ORCID {orcid_id}")
                return publications
                
        except Exception as e:
            return self._handle_error(e, f"search_by_orcid({orcid_id})")
