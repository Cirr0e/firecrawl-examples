# GPT Knowledge Crawler

## Overview

A flexible tool for generating knowledge bases for custom GPTs using Firecrawl, designed to intelligently extract and process web content.

## Features

- Web content crawling with Firecrawl
- Intelligent content filtering
- Knowledge file generation
- Configurable extraction parameters
- Support for multiple knowledge domains

## Prerequisites

- Python 3.9+
- Firecrawl API Key
- (Optional) OpenAI API Key

## Installation

1. Clone the repository
2. Create a virtual environment
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env` and fill in your API keys

## Usage

```bash
python main.py --url https://example.com/docs --config domains/tech_docs.yaml
```

### Configuration Options

Create a YAML configuration file to customize crawling:
- Specify allowed domains
- Define content filters
- Set extraction parameters
- Configure output formatting

## Example Configuration (domains/tech_docs.yaml)
```yaml
domain: 
  base_url: https://example.com/docs
  allowed_paths: 
    - /guide
    - /api
  exclude_paths:
    - /blog
    - /archived

extraction:
  max_tokens: 4000
  chunk_strategy: semantic
  
output:
  format: json
  filename: tech_knowledge_base.json
```