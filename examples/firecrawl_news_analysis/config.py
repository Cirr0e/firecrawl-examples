import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_CONFIG = {
    'firecrawl': {
        'api_key': os.getenv('FIRECRAWL_API_KEY'),
        'base_url': 'https://api.firecrawl.dev/v0'
    },
    'newsapi': {
        'api_key': os.getenv('NEWSAPI_KEY'),
        'base_url': 'https://newsapi.org/v2'
    },
    'nyt': {
        'api_key': os.getenv('NYT_API_KEY'),
        'base_url': 'https://api.nytimes.com/svc/search/v2'
    }
}

# Default search parameters
DEFAULT_SEARCH_PARAMS = {
    'query': 'technology',
    'from_date': '2024-01-01',
    'to_date': '2024-02-01',
    'language': 'en',
    'sources': ['techcrunch', 'wired', 'the-verge']
}

# Logging configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(levelname)s: %(message)s'
}