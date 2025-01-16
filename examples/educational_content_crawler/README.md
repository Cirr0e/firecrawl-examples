# Educational Content Crawler with Firecrawl

A specialized web crawler that aggregates and validates educational content using Firecrawl and LLM-powered content analysis. This example demonstrates how to build an AI tutoring content aggregation system with robust content validation and retrieval capabilities.

## Features

- 🎓 Educational content crawling with automatic categorization
- 🧠 LLM-powered content validation and quality assessment
- 📚 Proposition-based content chunking for better retrieval
- ⚡ Efficient caching of frequently accessed content
- 🔍 Metadata extraction specific to educational materials
- 🛡️ Content license validation and age-appropriate filtering

## Requirements

- Python 3.10+
- firecrawl-py==1.9.0
- langchain>=0.1.0
- pydantic>=2.0.0

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from educational_crawler import EducationalCrawler

# Initialize the crawler
crawler = EducationalCrawler(
    api_key="your_firecrawl_api_key",
    llm_api_key="your_llm_api_key"
)

# Add educational websites to crawl
websites = [
    "https://www.khanacademy.org/math",
    "https://www.coursera.org/learn/python"
]

# Start crawling and processing
content = crawler.crawl_and_process(websites)

# Get validated educational content
validated_content = content.get_validated_content()
```

## Configuration

Set up your environment variables in a `.env` file:

```bash
FIRECRAWL_API_KEY=your_firecrawl_api_key
LLM_API_KEY=your_llm_api_key
```

## Usage Examples

See [examples.md](examples.md) for detailed usage examples including:
- Content validation workflows
- Custom filtering rules
- Content quality scoring
- License validation
- Age-appropriate content filtering

## Architecture

The system consists of several key components:

1. Content Crawler: Uses Firecrawl to efficiently crawl educational websites
2. Content Validator: Validates content quality and educational value using LLMs
3. Content Processor: Chunks content into propositions for optimal retrieval
4. Metadata Extractor: Extracts educational metadata (subject, grade level, etc.)
5. Cache Manager: Handles caching of frequently accessed content

## Documentation

- [API Reference](docs/api.md)
- [Content Validation Rules](docs/validation.md)
- [Caching Strategy](docs/caching.md)
- [Metadata Schema](docs/metadata.md)

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on how to submit pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.