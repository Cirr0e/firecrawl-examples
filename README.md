
# Web Research Agent

## Overview

The Web Research Agent is an advanced, multilingual research tool that leverages AI technologies to perform comprehensive web research, extract structured information, and generate coherent research summaries across multiple languages.

## Key Features

- 🌐 **Multilingual Web Research**
  - Supports automatic language detection
  - Research in multiple languages (English, Spanish, French, with expandable support)
  - Language-specific model selection

- 🔍 **Intelligent Web Crawling**
  - Uses Firecrawl for efficient web searching
  - Structured data extraction
  - Configurable source limits and search parameters

- 📄 **Advanced Synthesis**
  - AI-powered summary generation
  - Customizable language models
  - Contextual research synthesis

- 🛡️ **Robust Configuration**
  - YAML-based configuration
  - Environment variable support
  - Flexible initialization options

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/web-research-agent.git
cd web-research-agent

# Install dependencies
pip install -r requirements.txt
```

### Configuration

1. Set your Firecrawl API key:
```bash
export FIRECRAWL_API_KEY='your_api_key_here'
```

2. (Optional) Customize `config.yaml` for advanced settings

### Usage Examples

#### Basic Usage
```python
from research_agent.agent import WebResearchAgent

# English research
research_agent = WebResearchAgent(
    research_topic="AI Market Research"
)
results = research_agent.perform_web_research()
print(results)

# Spanish research
spanish_agent = WebResearchAgent(
    research_topic="Inteligencia Artificial en Investigación de Mercado", 
    language='es'
)
spanish_results = spanish_agent.perform_web_research()
print(spanish_results)

# Automatic language detection
auto_agent = WebResearchAgent(
    research_topic="AI Market Research", 
    language='auto'
)
auto_results = auto_agent.perform_web_research()
print(auto_results)
```

## Configuration Options

The Web Research Agent supports extensive configuration via `config.yaml`:

- `general`: Debug mode and logging settings
- `search`: Web search configuration (max sources, domain restrictions)
- `synthesis`: Language model and summary generation settings
- `api`: API interaction parameters
- `topic_refinement`: Advanced research topic handling

## Components

- `WebResearchAgent`: Main orchestration class
- `DataProcessor`: Web crawling and data extraction
- `Synthesizer`: AI-powered research summary generation
- `LanguageDetector`: Multilingual support and language detection

## Dependencies

- Firecrawl
- Transformers
- PyTorch
- LangDetect

## Contributing

Contributions are welcome! Please read the contributing guidelines and submit pull requests.

## License

[Your License Here - e.g., MIT License]

## Roadmap

- [ ] Expand language model support
- [ ] Implement more sophisticated language detection
- [ ] Add translation capabilities
- [ ] Enhance error handling
- [ ] Create more comprehensive documentation

## Contact

[Your Contact Information]
