```python
import os
import json
import asyncio
from typing import List, Dict, Optional

from firecrawl import FirecrawlApp
from crewai import Agent, Task, Crew
from pydantic import BaseModel, Field

# Use sample data if no API key is available
SAMPLE_RESTAURANT_DATA = [
    {
        "name": "Sample Restaurant SF",
        "cuisine": "California Fusion",
        "price_range": "$$",
        "average_rating": 4.5,
        "top_dishes": ["Avocado Toast", "Seafood Risotto"],
        "contact_info": {"phone": "415-555-1234", "website": "https://sample-restaurant.com"}
    }
]

class RestaurantData(BaseModel):
    name: str = Field(..., description="Name of the restaurant")
    cuisine: str = Field(..., description="Type of cuisine")
    price_range: str = Field(..., description="Price category ($ to $$$$)")
    average_rating: float = Field(..., description="Average customer rating")
    top_dishes: List[str] = Field(default_factory=list, description="Signature or most popular dishes")
    contact_info: Dict[str, Optional[str]] = Field(
        default_factory=dict, 
        description="Contact information including phone and website"
    )

class RestaurantIntelligenceAgent:
    def __init__(self, target_city: str, firecrawl_api_key: Optional[str] = None):
        """
        Initialize the Restaurant Intelligence Agent
        
        Args:
            target_city (str): City to analyze restaurant landscape
            firecrawl_api_key (Optional[str]): API key for Firecrawl
        """
        self.target_city = target_city
        self.firecrawl = FirecrawlApp(api_key=firecrawl_api_key) if firecrawl_api_key else None
        self.restaurant_urls = []
    
    async def discover_restaurant_websites(self) -> List[str]:
        """
        Discover restaurant websites 
        
        Returns:
            List of restaurant website URLs
        """
        if not self.firecrawl:
            print("No Firecrawl API key. Using sample data.")
            return []
        
        try:
            search_query = f"best restaurants in {self.target_city}"
            map_results = self.firecrawl.map_url(
                url="https://www.google.com/search",
                params={
                    "query": search_query,
                    "search": "restaurant website",
                    "limit": 5
                }
            )
            self.restaurant_urls = map_results.get('links', [])
            return self.restaurant_urls
        except Exception as e:
            print(f"Error discovering websites: {e}")
            return []
    
    async def extract_restaurant_data(self, url: str = None) -> Optional[RestaurantData]:
        """
        Extract structured restaurant data
        
        Args:
            url (Optional[str]): Restaurant website URL
        
        Returns:
            Structured restaurant data or None
        """
        if not self.firecrawl:
            return RestaurantData(**SAMPLE_RESTAURANT_DATA[0])
        
        if not url:
            return None
        
        try:
            scrape_result = self.firecrawl.scrape_url(url, {
                "formats": ["extract"],
                "extract": {
                    "schema": RestaurantData.model_json_schema(),
                    "prompt": f"Extract detailed information about this restaurant in {self.target_city}"
                }
            })
            
            extracted_data = scrape_result.get('data', {}).get('llm_extraction')
            return RestaurantData(**extracted_data) if extracted_data else None
        
        except Exception as e:
            print(f"Error extracting data from {url}: {e}")
            return None
    
    async def analyze_restaurant_landscape(self) -> str:
        """
        Analyze restaurant landscape
        
        Returns:
            Comprehensive market analysis report
        """
        # Use sample data if no Firecrawl API
        if not self.firecrawl:
            restaurant_data = [RestaurantData(**data) for data in SAMPLE_RESTAURANT_DATA]
        else:
            # Discover websites first
            await self.discover_restaurant_websites()
            
            # Parallel extraction of restaurant data
            restaurant_data = await asyncio.gather(
                *[self.extract_restaurant_data(url) for url in self.restaurant_urls]
            )
        
        # Filter out None results
        valid_restaurant_data = [r for r in restaurant_data if r is not None]
        
        if not valid_restaurant_data:
            return "No restaurant data available."
        
        # Simple market report generation
        market_report = {
            "city": self.target_city,
            "total_restaurants": len(valid_restaurant_data),
            "cuisines": list(set(r.cuisine for r in valid_restaurant_data)),
            "restaurants": [
                {
                    "name": r.name,
                    "cuisine": r.cuisine,
                    "rating": r.average_rating
                } for r in valid_restaurant_data
            ]
        }
        
        return json.dumps(market_report, indent=2)

def main():
    firecrawl_api_key = os.getenv('FIRECRAWL_API_KEY')
    city_analyzer = RestaurantIntelligenceAgent('San Francisco', firecrawl_api_key)
    
    try:
        market_report = asyncio.run(city_analyzer.analyze_restaurant_landscape())
        
        # Save report to JSON
        with open('restaurant_market_report.json', 'w') as f:
            f.write(market_report)
        
        print("Market Analysis Complete. Report saved to restaurant_market_report.json")
        print(market_report)
    
    except Exception as e:
        print(f"Error in market analysis: {e}")

if __name__ == "__main__":
    main()
```