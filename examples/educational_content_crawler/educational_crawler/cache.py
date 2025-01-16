from typing import Optional, Dict, List
from .models import EducationalContent

class CacheManager:
    """Manages caching of processed educational content"""
    
    def __init__(self):
        self._cache: Dict[str, EducationalContent] = {}
        
    def get(self, url: str) -> Optional[EducationalContent]:
        """Get cached content for URL"""
        return self._cache.get(url)
        
    def set(self, url: str, content: EducationalContent):
        """Cache content for URL"""
        self._cache[url] = content
        
    def get_all_validated(self) -> List[EducationalContent]:
        """Get all validated content from cache"""
        return [
            content for content in self._cache.values()
            if content.validation_result and content.validation_result.is_valid
        ]
        
    def clear(self):
        """Clear the cache"""
        self._cache.clear()