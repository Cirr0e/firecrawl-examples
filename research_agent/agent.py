from firecrawl import FirecrawlApp
from .data_processor import DataProcessor
from .synthesizer import Synthesizer
from .config import config
from .language_detector import LanguageDetector
import logging
import os

class WebResearchAgent:
    def __init__(
        self, 
        research_topic: str, 
        firecrawl_api_key: str = None, 
        model_name: str = None,
        language: str = 'en'
    ):
        """
        Initializes the WebResearchAgent with enhanced configuration options.
        
        Args:
            research_topic (str): The topic to research.
            firecrawl_api_key (str, optional): API key for Firecrawl services.
            model_name (str, optional): Specific model name to override config.
            language (str, optional): Target language for research.
        """
        # Logging setup
        self.logger = logging.getLogger(__name__)
        
        # Detect language if not specified
        if language == 'auto':
            language = LanguageDetector.detect_language(research_topic)
        
        # API Key handling
        self.firecrawl_api_key = (
            firecrawl_api_key or 
            os.environ.get('FIRECRAWL_API_KEY') or 
            config.get('api.firecrawl.key')
        )
        
        if not self.firecrawl_api_key:
            raise ValueError("Firecrawl API key is required")
        
        # Model name selection
        self.model_name = (
            model_name or 
            config.get('synthesis.model_name')
        )
        
        # Firecrawl configuration
        firecrawl_config = {
            'retry_attempts': config.get('api.firecrawl.retry_attempts', 3),
            'timeout': config.get('api.firecrawl.timeout', 30)
        }
        
        # Initialize Firecrawl
        self.firecrawl = FirecrawlApp(
            api_key=self.firecrawl_api_key,
            **firecrawl_config
        )
        
        # Initialize components
        self.data_processor = DataProcessor(
            self.firecrawl, 
            max_sources=config.get('search.max_sources', 10),
            language=language
        )
        self.synthesizer = Synthesizer(
            model_name=self.model_name,
            max_length=config.get('synthesis.max_summary_length', 500),
            temperature=config.get('synthesis.temperature', 0.7),
            language=language
        )
        
        # Store research topic
        self.research_topic = self._refine_research_topic(research_topic)
        self.language = language

    # ... (rest of the implementation remains the same)