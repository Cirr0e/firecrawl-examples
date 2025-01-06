from firecrawl import FirecrawlApp
from pydantic import BaseModel, Field
from typing import List, Optional
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImageContent(BaseModel):
    """Schema for image content extraction"""
    url: str = Field(..., description="URL of the image")
    alt_text: Optional[str] = Field(None, description="Alt text of the image")
    caption: Optional[str] = Field(None, description="Caption or text near the image")
    visual_content: Optional[str] = Field(None, description="Description of what's in the image")

class PageContentSchema(BaseModel):
    """Schema for full page content extraction"""
    title: str = Field(..., description="Title of the page")
    main_content: str = Field(..., description="Main textual content of the page")
    images: List[ImageContent] = Field(
        default_factory=list,
        description="List of images found on the page with their details"
    )
    metadata: dict = Field(
        default_factory=dict,
        description="Additional metadata about the page"
    )

class MultimodalCrawler:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the multimodal crawler with firecrawl"""
        self.api_key = api_key or os.getenv("FIRECRAWL_API_KEY")
        if not self.api_key:
            raise ValueError("Firecrawl API key is required")
        
        self.app = FirecrawlApp(api_key=self.api_key)
        
    async def crawl_page(self, url: str) -> PageContentSchema:
        """
        Crawl a webpage and extract both textual and image content
        """
        try:
            # Define extraction options with our schema
            extractor_options = {
                "mode": "llm-extraction",
                "extractionSchema": PageContentSchema.schema(),
                "extractionPrompt": """
                Extract the content from this page, including:
                1. The main textual content
                2. All images with their details
                3. Any relevant metadata
                
                For each image, try to understand and describe its visual content.
                """
            }

            # Crawl and extract data using firecrawl
            result = await self.app.scrape_url(
                url,
                {
                    "extractorOptions": extractor_options,
                    "pageOptions": {
                        "onlyMainContent": True,
                        "includeImages": True
                    }
                }
            )

            # Parse the result into our schema
            extracted_data = result.get("llm_extraction", {})
            return PageContentSchema(**extracted_data)

        except Exception as e:
            logger.error(f"Error crawling {url}: {e}")
            raise

async def main():
    # Example usage
    try:
        crawler = MultimodalCrawler()
        url = "https://example.com"
        
        print(f"Crawling {url}...")
        result = await crawler.crawl_page(url)
        
        # Print results
        print(f"\nTitle: {result.title}")
        print(f"Number of images found: {len(result.images)}")
        
        print("\nImage Analysis:")
        for img in result.images:
            print(f"\nImage URL: {img.url}")
            print(f"Visual Content: {img.visual_content}")
            print(f"Caption: {img.caption}")
            
    except Exception as e:
        logger.error(f"Error in main: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())