from firecrawl import FirecrawlApp
import logging
from .language_detector import LanguageDetector

class DataProcessor:
    def __init__(
        self, 
        firecrawl: FirecrawlApp, 
        max_sources: int = 10, 
        language: str = 'en'
    ):
        """
        Initializes the DataProcessor with a FirecrawlApp instance.
        
        Args:
            firecrawl (FirecrawlApp): Instance of FirecrawlApp for web crawling and extraction.
            max_sources (int): Maximum number of sources to process.
            language (str): Target language for research sources.
        """
        self.firecrawl = firecrawl
        self.max_sources = max_sources
        self.target_language = language
        self.logger = logging.getLogger(__name__)

    def process_search_results(
        self, 
        research_topic: str, 
        limit: int = None
    ) -> list:
        """
        Processes the research topic by searching and extracting structured data from URLs.
        
        Args:
            research_topic (str): The topic to research.
            limit (int, optional): Maximum number of sources to process.
        
        Returns:
            list: List of extracted and structured research data.
        """
        try:
            # Use limit or default to max_sources
            sources_limit = limit or self.max_sources
            
            # Perform web search
            search_results = self.firecrawl.search(
                query=research_topic,
                num_results=sources_limit,
                scrapeOptions={
                    'formats': ['markdown'],
                }
            )
            
            # Process and extract data from each search result
            processed_results = []
            for result in search_results:
                try:
                    # Extract structured information from each URL
                    extracted_info = self.firecrawl.extract(
                        urls=[result['url']],
                        schema={
                            'type': 'object',
                            'properties': {
                                'title': {'type': 'string'},
                                'key_points': {'type': 'array', 'items': {'type': 'string'}},
                                'summary': {'type': 'string'}
                            }
                        }
                    )
                    processed_results.append(extracted_info)
                except Exception as extract_error:
                    self.logger.warning(f"Could not extract data from {result['url']}: {extract_error}")
            
            # Filter sources by target language
            filtered_results = LanguageDetector.filter_sources_by_language(
                processed_results, 
                target_language=self.target_language
            )
            
            return filtered_results
        
        except Exception as search_error:
            self.logger.error(f"Error during web research: {search_error}")
            return []