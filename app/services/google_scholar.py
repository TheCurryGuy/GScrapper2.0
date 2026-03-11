from typing import List, Optional, Tuple
import httpx
from app.services.base import BaseAcademicService
from app.models.response import Publication
from app.core.config import settings


class GoogleScholarService(BaseAcademicService):
    
    def __init__(self):
        super().__init__()
        self.api_url = "https://serpapi.com/search.json"
        self.api_keys = [
            (settings.SERPAPI_KEY, "primary"),
            (settings.SERPAPI_KEY_BACKUP, "backup"),
            (settings.SERPAPI_KEY_BACKUP2, "backup2"),
        ]
    
    async def search_by_author_id(self, author_id: str) -> Tuple[List[Publication], dict]:
        for api_key, key_type in self.api_keys:
            self.logger.info(f"Fetching Google Scholar data for author ID: {author_id} via SerpAPI ({key_type} key)")
            
            all_publications = []
            author_metadata = {}
            start = 0
            key_failed = False
            
            try:
                async with httpx.AsyncClient(timeout=60.0) as client:
                    while True:
                        params = {
                            "engine": "google_scholar_author",
                            "author_id": author_id,
                            "start": start,
                            "api_key": api_key
                        }
                        
                        response = await client.get(self.api_url, params=params)
                        
                        if response.status_code in (429, 403):
                            self.logger.warning(f"SerpAPI {key_type} key hit rate limit (status {response.status_code}), trying next key...")
                            key_failed = True
                            break
                        
                        response.raise_for_status()
                        data = response.json()
                        
                        if start == 0:
                            author_info = data.get("author", {})
                            cited_by = data.get("cited_by", {})
                            
                            h_index = 0
                            i10_index = 0
                            total_citations = 0
                            table = cited_by.get("table", [])
                            for row in table:
                                if "citations" in row:
                                    total_citations = row["citations"].get("all", 0)
                                if "h_index" in row:
                                    h_index = row["h_index"].get("all", 0)
                                if "i10_index" in row:
                                    i10_index = row["i10_index"].get("all", 0)
                            
                            author_metadata = {
                                "name": author_info.get("name", ""),
                                "affiliation": author_info.get("affiliations", ""),
                                "interests": [
                                    interest.get("title", "")
                                    for interest in author_info.get("interests", [])
                                ],
                                "h_index": h_index,
                                "i10_index": i10_index,
                                "total_citations": total_citations,
                                "thumbnail": author_info.get("thumbnail", ""),
                            }
                        
                        articles = data.get("articles", [])
                        if not articles:
                            break
                        
                        main_author = author_metadata.get("name", "")
                        
                        for article in articles:
                            title = article.get("title", "Unknown Title")
                            year_str = article.get("year", "")
                            year = int(year_str) if year_str and str(year_str).isdigit() else None
                            
                            authors_str = article.get("authors", "")
                            if authors_str:
                                authors = [a.strip() for a in authors_str.split(",")]
                            else:
                                authors = [main_author] if main_author else []
                            
                            cited_by_info = article.get("cited_by", {})
                            citations = cited_by_info.get("value", 0) if isinstance(cited_by_info, dict) else 0
                            
                            url = article.get("link", "")
                            
                            pub = Publication(
                                title=title,
                                authors=authors,
                                year=year,
                                venue=article.get("publication", None),
                                publication_type=None,
                                doi=None,
                                url=url,
                                citations=citations,
                                abstract=None,
                                source="Google Scholar"
                            )
                            all_publications.append(pub)
                        
                        start += 20
                
                if not key_failed:
                    self.logger.info(
                        f"Found {len(all_publications)} publications from Google Scholar "
                        f"for author ID: {author_id} ({key_type} key)"
                    )
                    return (all_publications, author_metadata)
                    
            except Exception as e:
                self.logger.error(f"SerpAPI {key_type} key failed for author ID {author_id}: {e}", exc_info=True)
                continue
        
        self.logger.error("All SerpAPI keys exhausted!")
        return ([], {})
    
    async def search_by_name(self, name: str, email: Optional[str] = None) -> List[Publication]:
        self.logger.info("Google Scholar name search not supported. Use search_by_author_id instead.")
        return []
    
    async def search_by_orcid(self, orcid_id: str) -> List[Publication]:
        self.logger.info("Google Scholar doesn't support ORCID search")
        return []
