import asyncio
from typing import List, Optional
from habanero import Crossref
from app.services.base import BaseAcademicService
from app.models.response import Publication
from app.core.config import settings


class CrossRefService(BaseAcademicService):
    
    def __init__(self):
        super().__init__()
        self.cr = Crossref(mailto=settings.CROSSREF_MAILTO)
    
    async def search_by_name(self, name: str, email: Optional[str] = None) -> List[Publication]:
        try:
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(
                None,
                lambda: self.cr.works(query_author=name, limit=1000)
            )
            
            items = results.get('message', {}).get('items', [])
            
            search_name_lower = name.lower().strip()
            search_parts = search_name_lower.split()
            
            publications = []
            for item in items:
                authors = []
                author_match_found = False
                
                for author in item.get('author', []):
                    given = author.get('given', '')
                    family = author.get('family', '')
                    full_name = f"{given} {family}".strip()
                    if full_name:
                        authors.append(full_name)
                        
                        author_lower = full_name.lower()
                        if all(part in author_lower for part in search_parts):
                            author_match_found = True
                
                if not author_match_found:
                    continue
                
                year = None
                if 'published-print' in item:
                    year = item['published-print'].get('date-parts', [[None]])[0][0]
                elif 'published-online' in item:
                    year = item['published-online'].get('date-parts', [[None]])[0][0]
                
                pub = Publication(
                    title=item.get('title', ['Unknown'])[0] if item.get('title') else 'Unknown',
                    authors=authors,
                    year=year,
                    venue=item.get('container-title', [None])[0] if item.get('container-title') else None,
                    publication_type=item.get('type'),
                    doi=item.get('DOI'),
                    url=item.get('URL'),
                    citations=item.get('is-referenced-by-count', 0),
                    abstract=item.get('abstract'),
                    source="CrossRef"
                )
                publications.append(pub)
            
            self.logger.info(f"Found {len(publications)} works from CrossRef for {name}")
            return publications
            
        except Exception as e:
            return self._handle_error(e, f"search_by_name({name})")
    
    async def search_by_orcid(self, orcid_id: str) -> List[Publication]:
        try:
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(
                None,
                lambda: self.cr.works(query_author=orcid_id, limit=200)
            )
            
            items = results.get('message', {}).get('items', [])
            
            publications = []
            for item in items:
                authors = []
                for author in item.get('author', []):
                    if author.get('ORCID') == f"http://orcid.org/{orcid_id}":
                        given = author.get('given', '')
                        family = author.get('family', '')
                        full_name = f"{given} {family}".strip()
                        if full_name:
                            authors.append(full_name)
                
                year = None
                if 'published-print' in item:
                    year = item['published-print'].get('date-parts', [[None]])[0][0]
                elif 'published-online' in item:
                    year = item['published-online'].get('date-parts', [[None]])[0][0]
                
                pub = Publication(
                    title=item.get('title', ['Unknown'])[0],
                    authors=authors or [a.get('family', 'Unknown') for a in item.get('author', [])],
                    year=year,
                    venue=item.get('container-title', [None])[0],
                    publication_type=item.get('type'),
                    doi=item.get('DOI'),
                    url=item.get('URL'),
                    citations=item.get('is-referenced-by-count', 0),
                    abstract=item.get('abstract'),
                    source="CrossRef"
                )
                publications.append(pub)
            
            self.logger.info(f"Found {len(publications)} works from CrossRef for ORCID {orcid_id}")
            return publications
            
        except Exception as e:
            return self._handle_error(e, f"search_by_orcid({orcid_id})")
