```markdown
# AI-Optimized Web Crawler Example

This example demonstrates how to use firecrawl to build an AI-optimized web crawling pipeline that produces clean, structured data ready for LLM consumption.

## Features

- Clean content extraction with noise removal
- Markdown formatting optimized for LLMs
- Automatic citation tracking
- Context extraction
- Metadata preservation
- Structured output using Pydantic models

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Basic usage:

```python
from ai_optimized_crawler import AIOptimizedCrawler
import asyncio

async def main():
    urls = [
        "https://example.com/article1",
        "https://example.com/article2"
    ]
    
    crawler = AIOptimizedCrawler()
    results = await crawler.crawl_and_process(urls)
    crawler.save_results(results, "ai_ready_content.json")

asyncio.run(main())
```

## Configuration

You can customize the crawler behavior through the following settings:

```python
config = {
    "content_cleaning": {
        "remove_ads": True,
        "remove_navigation": True,
        "min_content_length": 100
    },
    "ai_formatting": {
        "format_type": "markdown",
        "include_citations": True,
        "extract_context": True
    }
}

crawler = AIOptimizedCrawler(config=config)
```

## Output Format

The crawler produces structured JSON output:

```json
{
  "title": "Article Title",
  "content": "Markdown formatted content...",
  "metadata": {
    "author": "John Doe",
    "publish_date": "2025-01-05",
    "tags": ["AI", "Web Crawling"]
  },
  "source_url": "https://example.com/article1",
  "timestamp": "2025-01-05T12:00:00Z",
  "citations": [
    {
      "text": "Quoted text",
      "source": "Original source",
      "context": "Surrounding context"
    }
  ],
  "context": {
    "section": "Technology",
    "category": "AI News",
    "related_topics": ["Machine Learning", "Data Science"]
  }
}
```

## Best Practices

1. **Content Cleaning**
   - Remove ads, navigation elements, and other noise
   - Preserve semantic structure of content
   - Maintain minimum content quality threshold

2. **AI Optimization**
   - Format content in Markdown for better LLM processing
   - Include relevant citations and sources
   - Extract and preserve context
   - Structure output consistently

3. **Performance**
   - Use async crawling for better throughput
   - Implement rate limiting to respect server limits
   - Cache processed results when appropriate

## Version Compatibility

This example is compatible with:
- Python 3.12.1
- firecrawl 0.0.1 (as of 2025-01-05)

## License

MIT License
```