# AI Training Data Collector Example

This example demonstrates how to safely and efficiently collect training data for AI models using Firecrawl. It includes content safety checks, quality filters, and automated workflow orchestration through LangFlow.

## Features

- Batch processing of URLs with automatic rate limiting
- Content safety validation and scoring
- Quality metrics calculation
- Export to common LLM training formats
- LangFlow workflow integration
- Progress tracking and reporting

## Requirements

- Firecrawl v1.9.0+
- Python 3.8+
- LangFlow (optional, for workflow automation)

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Set up your environment:
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your API keys
FIRECRAWL_API_KEY=your_api_key_here
```

## Usage

### Basic Usage

```python
from ai_training_collector import DataCollector

collector = DataCollector()
results = collector.collect_from_urls([
    "https://example.com/article1",
    "https://example.com/article2"
])
```

### With Custom Safety Rules

```python
from ai_training_collector import DataCollector, SafetyConfig

safety_config = SafetyConfig(
    min_quality_score=0.7,
    max_toxicity=0.2,
    required_attributes=["title", "content", "author"]
)

collector = DataCollector(safety_config=safety_config)
results = collector.collect_from_urls(urls, batch_size=10)
```

### LangFlow Integration

See the included `langflow_example.json` for a complete workflow that includes:
- URL collection
- Content extraction
- Safety validation
- Quality filtering
- Export pipeline

## Output Format

The collector outputs data in a standardized format suitable for LLM training:

```json
{
    "items": [
        {
            "id": "unique_id",
            "content": "Clean, filtered content",
            "metadata": {
                "source_url": "https://example.com/article1",
                "quality_score": 0.85,
                "safety_score": 0.95,
                "extraction_date": "2025-01-14T12:00:00Z"
            },
            "quality_metrics": {
                "coherence": 0.9,
                "relevance": 0.85,
                "toxicity": 0.1
            }
        }
    ],
    "stats": {
        "total_processed": 100,
        "passed_safety": 95,
        "failed_safety": 5,
        "average_quality": 0.82
    }
}
```

## Safety Features

- Content moderation using custom extraction schemas
- Quality scoring based on multiple metrics
- Automatic filtering of unsafe or low-quality content
- Detailed safety reports for audit trails

## Best Practices

1. Always set appropriate safety thresholds for your use case
2. Use batch processing for efficient collection
3. Implement proper error handling and retry logic
4. Monitor and log collection statistics
5. Regularly validate output quality
6. Store source URLs and extraction dates for provenance

## License

MIT License - see LICENSE file for details.