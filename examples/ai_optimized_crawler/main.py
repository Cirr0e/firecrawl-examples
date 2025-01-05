```python
from firecrawl import WebCrawler, Pipeline
from firecrawl.processors import ContentCleaner, AIFormatter
from pydantic import BaseModel
from typing import List, Optional
import asyncio
import json

class AIReadyContent(BaseModel):
    """Schema for AI-optimized content structure"""
    title: str
    content: str
    metadata: dict
    source_url: str
    timestamp: str
    citations: List[dict]
    context: Optional[dict]

class AIOptimizedCrawler:
    def __init__(self, config=None):
        self.crawler = WebCrawler()
        self.pipeline = Pipeline([
            ContentCleaner(
                remove_ads=True,
                remove_navigation=True,
                min_content_length=100
            ),
            AIFormatter(
                format_type="markdown",
                include_citations=True,
                extract_context=True
            )
        ])
        
    async def crawl_and_process(self, urls: List[str]) -> List[AIReadyContent]:
        """Crawl URLs and process content for AI consumption"""
        results = []
        
        for url in urls:
            # Crawl the page
            raw_content = await self.crawler.crawl(url)
            
            # Process through the pipeline
            processed_content = await self.pipeline.process(raw_content)
            
            # Structure the content
            ai_ready_content = AIReadyContent(
                title=processed_content.title,
                content=processed_content.markdown_content,
                metadata=processed_content.metadata,
                source_url=url,
                timestamp=processed_content.timestamp,
                citations=processed_content.citations,
                context=processed_content.extracted_context
            )
            
            results.append(ai_ready_content)
            
        return results

    def save_results(self, results: List[AIReadyContent], output_file: str):
        """Save processed results to a file"""
        with open(output_file, 'w') as f:
            json.dump(
                [result.dict() for result in results],
                f,
                indent=2
            )

async def main():
    # Example usage
    urls = [
        "https://example.com/article1",
        "https://example.com/article2"
    ]
    
    crawler = AIOptimizedCrawler()
    results = await crawler.crawl_and_process(urls)
    
    # Save results
    crawler.save_results(results, "ai_ready_content.json")
    
    # Print sample output
    print(f"Processed {len(results)} URLs")
    print("\nSample processed content:")
    print(json.dumps(results[0].dict(), indent=2))

if __name__ == "__main__":
    asyncio.run(main())
```