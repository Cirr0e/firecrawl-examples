import os
from typing import List, Dict, Optional
from firecrawl import FirecrawlApp
from pydantic import BaseModel
from dotenv import load_dotenv

from .validators import ContentValidator
from .processors import ContentProcessor
from .cache import CacheManager
from .metadata import MetadataExtractor
from .models import EducationalContent, ContentMetadata

load_dotenv()

class CrawlerConfig(BaseModel):
    """Configuration for the educational crawler"""
    max_pages_per_site: int = 100
    max_depth: int = 3
    content_types: List[str] = ["article", "lesson", "exercise", "video"]
    min_content_length: int = 100
    max_content_length: int = 50000

class EducationalCrawler:
    """Main crawler class for educational content"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        llm_api_key: Optional[str] = None,
        config: Optional[CrawlerConfig] = None
    ):
        self.api_key = api_key or os.getenv("FIRECRAWL_API_KEY")
        if not self.api_key:
            raise ValueError("Firecrawl API key is required")
            
        self.llm_api_key = llm_api_key or os.getenv("LLM_API_KEY")
        self.config = config or CrawlerConfig()
        
        # Initialize components
        self.app = FirecrawlApp(api_key=self.api_key)
        self.validator = ContentValidator(llm_api_key=self.llm_api_key)
        self.processor = ContentProcessor()
        self.cache = CacheManager()
        self.metadata = MetadataExtractor()

    def crawl_and_process(
        self, 
        urls: List[str],
        validate: bool = True,
        extract_metadata: bool = True
    ) -> List[EducationalContent]:
        """
        Crawl educational content from provided URLs and process it
        
        Args:
            urls: List of URLs to crawl
            validate: Whether to validate content quality
            extract_metadata: Whether to extract educational metadata
            
        Returns:
            List of processed educational content
        """
        results = []
        
        # Define extraction schema for educational content
        schema = {
            "title": "string",
            "content": "string",
            "type": "string",
            "grade_level": "string",
            "subject": "string",
            "learning_objectives": "array",
            "prerequisites": "array",
            "license": "string"
        }

        for url in urls:
            # Check cache first
            cached_content = self.cache.get(url)
            if cached_content:
                results.append(cached_content)
                continue
                
            # Crawl content using firecrawl
            crawled_data = self.app.scrape_url(
                url,
                params={
                    "extractionSchema": schema,
                    "maxPages": self.config.max_pages_per_site,
                    "maxDepth": self.config.max_depth
                }
            )
            
            # Process raw content into educational content format
            processed_content = self.processor.process(crawled_data)
            
            if validate:
                # Validate content quality and educational value
                processed_content = self.validator.validate(processed_content)
                
            if extract_metadata:
                # Extract educational metadata
                metadata = self.metadata.extract(processed_content)
                processed_content.metadata = metadata
                
            # Cache the processed content
            self.cache.set(url, processed_content)
            results.append(processed_content)
            
        return results

    def get_validated_content(self) -> List[EducationalContent]:
        """Get all validated educational content"""
        return self.cache.get_all_validated()
        
    def clear_cache(self):
        """Clear the content cache"""
        self.cache.clear()