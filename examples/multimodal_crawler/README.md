# Multimodal Web Crawler Example

This example demonstrates how to use firecrawl to create a production-ready multimodal web crawler that can extract both text and image content from websites, leveraging firecrawl's built-in LLM extraction capabilities.

## Features

- Structured data extraction with Pydantic models
- Automatic image content analysis
- Built-in rate limiting and resilience
- Production-ready error handling
- Clean, maintainable code structure

## Prerequisites

- Python 3.10 or higher
- A Firecrawl API key

## Installation

```bash
pip install -r requirements.txt
```

## Environment Setup

Create a `.env` file with the following variables:

```
FIRECRAWL_API_KEY=your_firecrawl_api_key_here
```

## Usage

Basic usage:

```python
from multimodal_crawler import MultimodalCrawler
import asyncio

async def main():
    # Initialize the crawler
    crawler = MultimodalCrawler()
    
    # Crawl a webpage
    result = await crawler.crawl_page("https://example.com")
    
    # Access the results
    print(f"Title: {result.title}")
    print(f"Number of images: {len(result.images)}")
    for image in result.images:
        print(f"Image URL: {image.url}")
        print(f"Visual content: {image.visual_content}")

# Run the crawler
asyncio.run(main())
```

## Output Format

The crawler returns a `PageContentSchema` object with the following structure:

```python
{
    "title": "page_title",
    "main_content": "main_textual_content",
    "images": [
        {
            "url": "image_url",
            "alt_text": "image_alt_text",
            "caption": "image_caption",
            "visual_content": "description_of_image_content"
        }
    ],
    "metadata": {
        "key": "value"
    }
}
```

## Error Handling

The crawler includes robust error handling:
- Validates API key presence
- Handles network errors gracefully
- Provides detailed logging
- Returns structured error messages

The python version at the time of this example being created is 3.12.1