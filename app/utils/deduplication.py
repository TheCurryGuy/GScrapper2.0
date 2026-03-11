from typing import List
from difflib import SequenceMatcher
from app.models.response import Publication


def deduplicate_publications(publications: List[Publication]) -> List[Publication]:
    if not publications:
        return []
    
    doi_map = {}
    no_doi = []
    
    for pub in publications:
        if pub.doi:
            doi_key = pub.doi.lower().strip()
            if doi_key not in doi_map:
                doi_map[doi_key] = pub
            else:
                _merge_publications(doi_map[doi_key], pub)
        else:
            no_doi.append(pub)
    
    unique_pubs = list(doi_map.values())
    
    for pub in no_doi:
        is_duplicate = False
        
        for existing in unique_pubs:
            if _are_similar_titles(pub.title, existing.title):
                _merge_publications(existing, pub)
                is_duplicate = True
                break
        
        if not is_duplicate:
            unique_pubs.append(pub)
    
    return unique_pubs


def _are_similar_titles(title1: str, title2: str, threshold: float = 0.85) -> bool:
    if not title1 or not title2:
        return False
    
    t1 = title1.lower().strip()
    t2 = title2.lower().strip()
    
    if t1 == t2:
        return True
    
    ratio = SequenceMatcher(None, t1, t2).ratio()
    return ratio >= threshold


def _merge_publications(target: Publication, source: Publication) -> None:
    if not target.doi and source.doi:
        target.doi = source.doi
    
    if not target.url and source.url:
        target.url = source.url
    
    if not target.abstract and source.abstract:
        target.abstract = source.abstract
    
    if not target.venue and source.venue:
        target.venue = source.venue
    
    if not target.year and source.year:
        target.year = source.year
    
    if source.citations and (not target.citations or source.citations > target.citations):
        target.citations = source.citations
    
    if source.authors:
        target.authors = list(set(target.authors + source.authors))
