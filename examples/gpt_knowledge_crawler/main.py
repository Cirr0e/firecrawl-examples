import os
import sys
import argparse
import logging
from dotenv import load_dotenv
import yaml
import json
import tiktoken

from firecrawl import FirecrawlApp
import validators

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

class GPTKnowledgeCrawler:
    def __init__(self, config_path):
        load_dotenv()
        
        # Initialize Firecrawl
        self.firecrawl = FirecrawlApp(
            api_key=os.getenv('FIRECRAWL_API_KEY')
        )
        
        # Load configuration
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        
        # Validate base configuration
        self._validate_config()
    
    def _validate_config(self):
        """Validate configuration parameters"""
        if not validators.url(self.config['domain']['base_url']):
            raise ValueError("Invalid base URL in configuration")
        
        # Add more validation logic
        required_keys = ['base_url', 'allowed_paths']
        for key in required_keys:
            if key not in self.config['domain']:
                raise KeyError(f"Missing required configuration key: {key}")
    
    def crawl(self):
        """Crawl and extract content based on configuration"""
        base_url = self.config['domain']['base_url']
        allowed_paths = self.config['domain'].get('allowed_paths', [])
        exclude_paths = self.config['domain'].get('exclude_paths', [])
        
        try:
            crawl_result = self.firecrawl.crawl_url(
                base_url,
                {
                    "crawlerOptions": {
                        "includes": allowed_paths,
                        "excludes": exclude_paths,
                        "limit": self.config.get('extraction', {}).get('max_pages', 50)
                    }
                }
            )
            
            return self._process_crawl_results(crawl_result)
        
        except Exception as e:
            logger.error(f"Crawling error: {e}")
            return None
    
    def _process_crawl_results(self, results):
        """Process and filter crawl results"""
        max_tokens = self.config.get('extraction', {}).get('max_tokens', 4000)
        tokenizer = tiktoken.get_encoding("cl100k_base")
        
        processed_content = []
        for page in results.get('pages', []):
            tokens = tokenizer.encode(page['content'])
            
            if len(tokens) <= max_tokens:
                processed_content.append({
                    'url': page['url'],
                    'content': page['content']
                })
            else:
                logger.info(f"Truncating content from {page['url']}")
                truncated_content = tokenizer.decode(tokens[:max_tokens])
                processed_content.append({
                    'url': page['url'],
                    'content': truncated_content
                })
        
        return processed_content
    
    def save_knowledge_base(self, content):
        """Save processed content to knowledge base file"""
        output_format = self.config.get('output', {}).get('format', 'json')
        output_filename = self.config.get('output', {}).get(
            'filename', 
            f'knowledge_base_{int(time.time())}.{output_format}'
        )
        
        with open(output_filename, 'w') as f:
            if output_format == 'json':
                json.dump(content, f, indent=2)
            elif output_format == 'jsonl':
                for item in content:
                    f.write(json.dumps(item) + '\n')
        
        logger.info(f"Knowledge base saved to {output_filename}")

def main():
    parser = argparse.ArgumentParser(description="GPT Knowledge Crawler")
    parser.add_argument(
        '--config', 
        required=True, 
        help='Path to configuration YAML file'
    )
    
    args = parser.parse_args()
    
    try:
        crawler = GPTKnowledgeCrawler(args.config)
        results = crawler.crawl()
        
        if results:
            crawler.save_knowledge_base(results)
        else:
            logger.warning("No content extracted")
    
    except Exception as e:
        logger.error(f"Crawler failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()