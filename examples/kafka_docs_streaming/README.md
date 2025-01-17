# Kafka Documentation Streaming with Firecrawl

This example demonstrates how to use Firecrawl to crawl Kafka documentation and stream updates through Apache Kafka, deployed on Kubernetes using Strimzi operator.

## Features

- Automated documentation crawling with Firecrawl
- Real-time documentation updates via Kafka streaming
- Kubernetes deployment with Strimzi operator
- Structured data extraction and processing
- Documentation change detection and notifications

## Prerequisites

- Kubernetes cluster (local or cloud)
- [Strimzi Kafka Operator](https://strimzi.io/) installed
- Python 3.8+
- Firecrawl API key
- Docker for building containers

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a .env file with your Firecrawl API key:
```bash
FIRECRAWL_API_KEY=your_api_key_here
```

3. Deploy Kafka cluster using Strimzi:
```bash
kubectl apply -f kubernetes/kafka-cluster.yaml
```

4. Deploy the documentation crawler:
```bash
kubectl apply -f kubernetes/crawler-deployment.yaml
```

## Architecture

The system consists of three main components:

1. **Documentation Crawler**: Uses Firecrawl to fetch and process Kafka documentation
2. **Kafka Broker**: Handles message streaming and updates
3. **Change Detector**: Monitors for documentation changes and triggers notifications

## Usage

1. Start the documentation crawler:
```bash
python crawler.py
```

2. Monitor documentation updates:
```bash
python monitor.py
```

3. View processed documentation:
```bash
python viewer.py
```

## Configuration

Adjust the crawler settings in `config.yaml`:

```yaml
crawler:
  update_interval: 3600  # seconds
  base_url: "https://kafka.apache.org/documentation/"
  include_paths:
    - "/documentation/*"
    - "/apis/*"
  exclude_paths:
    - "/downloads/*"
    - "/community/*"

kafka:
  topic: "kafka_docs_updates"
  partitions: 3
  replicas: 3
```

## License

MIT License