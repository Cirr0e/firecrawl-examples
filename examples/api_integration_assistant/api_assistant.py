from firecrawl import FirecrawlApp
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, HttpUrl, validator
import json
import aiohttp
import asyncio
from datetime import datetime
from urllib.parse import urlparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIError(Exception):
    """Base exception for API-related errors."""
    pass

class APIEndpoint(BaseModel):
    path: str
    method: str
    auth_required: bool
    rate_limit: Optional[str] = None
    description: Optional[str] = None
    
    @validator('method')
    def validate_method(cls, v):
        valid_methods = {'GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'}
        if v.upper() not in valid_methods:
            raise ValueError(f"Invalid HTTP method. Must be one of {valid_methods}")
        return v.upper()

class APIInfo(BaseModel):
    endpoints: List[APIEndpoint]
    auth_method: Optional[str]
    base_url: HttpUrl
    documentation_url: Optional[HttpUrl] = None
    
    class Config:
        arbitrary_types_allowed = True

class MonitoringStats(BaseModel):
    last_check: Optional[datetime]
    average_response_time: float
    error_count: int
    recent_errors: List[Dict[str, Any]]

class APIIntegrationAssistant:
    def __init__(self, api_key: str):
        """Initialize the API Integration Assistant.

        Args:
            api_key (str): Your Firecrawl API key
        """
        if not api_key:
            raise ValueError("API key is required")
            
        self.app = FirecrawlApp(api_key=api_key)
        self.monitoring: Dict[str, Dict] = {}
        logger.info("API Integration Assistant initialized")

    async def discover_api(self, url: str) -> APIInfo:
        """Discover API endpoints and metadata from documentation.

        Args:
            url (str): URL of the API documentation

        Returns:
            APIInfo: Structured information about the API
            
        Raises:
            APIError: If there's an error discovering the API
        """
        try:
            logger.info(f"Discovering API at {url}")
            
            # Validate URL
            parsed_url = urlparse(url)
            if not all([parsed_url.scheme, parsed_url.netloc]):
                raise ValueError("Invalid URL provided")

            # Extract API information using Firecrawl
            result = await self.app.scrapeUrl(url, {
                'formats': ['extract'],
                'extract': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'endpoints': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'path': {'type': 'string'},
                                        'method': {'type': 'string'},
                                        'auth_required': {'type': 'boolean'},
                                        'rate_limit': {'type': 'string'},
                                        'description': {'type': 'string'}
                                    },
                                    'required': ['path', 'method', 'auth_required']
                                }
                            },
                            'auth_method': {'type': 'string'},
                            'base_url': {'type': 'string'},
                            'documentation_url': {'type': 'string'}
                        },
                        'required': ['endpoints', 'base_url']
                    }
                }
            })

            if not result.get('extract'):
                raise APIError("Failed to extract API information")

            api_info = APIInfo(**result['extract'])
            logger.info(f"Discovered {len(api_info.endpoints)} endpoints")
            return api_info

        except Exception as e:
            logger.error(f"Error discovering API: {str(e)}")
            raise APIError(f"Failed to discover API: {str(e)}") from e

    async def monitor_api(self, url: str):
        """Monitor API health and performance.

        Args:
            url (str): Base URL of the API
            
        Raises:
            ValueError: If URL is invalid
        """
        # Validate URL
        parsed_url = urlparse(url)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            raise ValueError("Invalid URL provided")

        if url in self.monitoring:
            logger.info(f"Already monitoring {url}")
            return

        logger.info(f"Starting monitoring for {url}")
        self.monitoring[url] = {
            'status': 'active',
            'last_check': None,
            'response_times': [],
            'errors': [],
            'start_time': datetime.now()
        }

        # Start monitoring task
        asyncio.create_task(self._monitor_loop(url))

    async def _monitor_loop(self, url: str):
        """Internal monitoring loop for API health checks.

        Args:
            url (str): URL to monitor
        """
        timeout = aiohttp.ClientTimeout(total=10)  # 10 second timeout
        
        async with aiohttp.ClientSession(timeout=timeout) as session:
            while self.monitoring.get(url, {}).get('status') == 'active':
                try:
                    start_time = datetime.now()
                    async with session.get(url) as response:
                        response_time = (datetime.now() - start_time).total_seconds()
                        
                        self.monitoring[url]['last_check'] = datetime.now()
                        self.monitoring[url]['response_times'].append(response_time)
                        
                        # Keep only last 100 response times
                        if len(self.monitoring[url]['response_times']) > 100:
                            self.monitoring[url]['response_times'].pop(0)
                        
                        if response.status >= 400:
                            error = {
                                'timestamp': datetime.now(),
                                'status': response.status,
                                'message': await response.text()
                            }
                            self.monitoring[url]['errors'].append(error)
                            logger.warning(f"API error: {error}")
                            
                except asyncio.TimeoutError:
                    error = {
                        'timestamp': datetime.now(),
                        'error': 'Request timed out'
                    }
                    self.monitoring[url]['errors'].append(error)
                    logger.error(f"Timeout error for {url}")
                    
                except Exception as e:
                    error = {
                        'timestamp': datetime.now(),
                        'error': str(e)
                    }
                    self.monitoring[url]['errors'].append(error)
                    logger.error(f"Error monitoring {url}: {str(e)}")
                
                # Keep only last 1000 errors
                if len(self.monitoring[url]['errors']) > 1000:
                    self.monitoring[url]['errors'] = self.monitoring[url]['errors'][-1000:]
                
                await asyncio.sleep(60)  # Check every minute

    def get_monitoring_stats(self, url: str) -> MonitoringStats:
        """Get monitoring statistics for an API.

        Args:
            url (str): URL of the monitored API

        Returns:
            MonitoringStats: Monitoring statistics
            
        Raises:
            ValueError: If URL is not being monitored
        """
        if url not in self.monitoring:
            raise ValueError(f"Not monitoring {url}")

        stats = self.monitoring[url]
        if stats['response_times']:
            avg_response_time = sum(stats['response_times']) / len(stats['response_times'])
        else:
            avg_response_time = 0

        return MonitoringStats(
            last_check=stats['last_check'],
            average_response_time=avg_response_time,
            error_count=len(stats['errors']),
            recent_errors=stats['errors'][-5:] if stats['errors'] else []
        )

    async def stop_monitoring(self, url: str):
        """Stop monitoring an API.

        Args:
            url (str): URL to stop monitoring
        """
        if url in self.monitoring:
            logger.info(f"Stopping monitoring for {url}")
            self.monitoring[url]['status'] = 'stopped'
            
            # Calculate final statistics
            stats = self.get_monitoring_stats(url)
            uptime = datetime.now() - self.monitoring[url]['start_time']
            
            logger.info(f"Monitoring stopped for {url}:")
            logger.info(f"Total uptime: {uptime}")
            logger.info(f"Average response time: {stats.average_response_time:.3f}s")
            logger.info(f"Total errors: {stats.error_count}")