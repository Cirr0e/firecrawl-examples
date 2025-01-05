# RAG Documentation Crawler Example

This example demonstrates how to use firecrawl to build a RAG (Retrieval Augmented Generation) system for documentation sites. It shows how to:
1. Crawl documentation sites efficiently
2. Process the content for RAG applications
3. Create a question-answering system using the crawled content

## Installation

```bash
pip install -r requirements.txt
```

The python version at the time of this example being created is 3.12.1

## Usage

1. Set up your environment variables:
```bash
export FIRECRAWL_API_KEY=your_firecrawl_api_key
export OPENAI_API_KEY=your_openai_api_key
```

2. Run the example:
```bash
python main.py
```

## Features

- **Efficient Documentation Crawling**: Uses firecrawl to recursively gather documentation content while respecting site structure
- **RAG Pipeline Integration**: Converts crawled content into a format suitable for RAG applications
- **Vector Search**: Implements semantic search using OpenAI embeddings and Chroma vector store
- **Question Answering**: Creates a QA system that can answer questions based on the crawled documentation
- **Source Attribution**: Provides source URLs for answers to ensure verifiability

## Customization

You can customize the example by:
1. Modifying the crawling parameters in `crawl_documentation()`
2. Adjusting the chunk size and overlap for text splitting
3. Using different vector stores or embedding models
4. Customizing the QA chain parameters

## Example Output

```
Crawling documentation at https://docs.example.com

Question: How do I install the package?

Answer: To install the package, run `pip install your-package-name`. Make sure you have Python 3.7+ installed.

Sources: ['https://docs.example.com/installation', 'https://docs.example.com/getting-started']
```