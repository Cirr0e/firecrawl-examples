import os
import time
import yaml
import json
from datetime import datetime
from dotenv import load_dotenv
from firecrawl import FirecrawlApp
from kafka import KafkaProducer
from kafka.errors import KafkaError
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DocsCrawler:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Load configuration
        with open('config.yaml', 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Initialize Firecrawl
        self.firecrawl = FirecrawlApp(api_key=os.getenv('FIRECRAWL_API_KEY'))
        
        # Initialize Kafka producer
        self.producer = KafkaProducer(
            bootstrap_servers=self.config['kafka']['bootstrap_servers'],
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )

    def crawl_docs(self):
        """Crawl Kafka documentation using Firecrawl"""
        try:
            docs = self.firecrawl.crawl_url(
                url=self.config['crawler']['base_url'],
                params={
                    "includePaths": self.config['crawler']['include_paths'],
                    "excludePaths": self.config['crawler']['exclude_paths'],
                    "maxDepth": self.config['firecrawl']['max_depth'],
                    "allowExternalLinks": self.config['firecrawl']['allow_external_links'],
                    "timeout": self.config['firecrawl']['timeout'],
                    "scrapeOptions": {
                        "formats": self.config['firecrawl']['formats']
                    }
                }
            )
            return docs
        except Exception as e:
            logger.error(f"Error crawling documentation: {str(e)}")
            return None

    def process_docs(self, docs):
        """Process crawled documentation"""
        if not docs:
            return None
            
        processed_docs = []
        for doc in docs['data']:
            processed_doc = {
                'url': doc['url'],
                'title': doc.get('title', ''),
                'content': doc.get('markdown', doc.get('html', '')),
                'timestamp': datetime.now().isoformat(),
                'metadata': doc.get('metadata', {})
            }
            processed_docs.append(processed_doc)
        
        return processed_docs

    def send_to_kafka(self, docs):
        """Send processed documentation to Kafka"""
        if not docs:
            return
            
        topic = self.config['kafka']['topic']
        
        for doc in docs:
            try:
                future = self.producer.send(topic, value=doc)
                # Block until the message is sent
                record_metadata = future.get(timeout=10)
                logger.info(f"Sent doc update to Kafka: {doc['url']}")
                logger.debug(f"Partition: {record_metadata.partition}, Offset: {record_metadata.offset}")
            except KafkaError as e:
                logger.error(f"Error sending to Kafka: {str(e)}")

    def run(self):
        """Main crawler loop"""
        while True:
            try:
                logger.info("Starting documentation crawl...")
                
                # Crawl docs
                raw_docs = self.crawl_docs()
                
                # Process docs
                processed_docs = self.process_docs(raw_docs)
                
                # Send to Kafka
                self.send_to_kafka(processed_docs)
                
                logger.info("Documentation crawl completed successfully")
                
                # Wait for next update interval
                time.sleep(self.config['crawler']['update_interval'])
                
            except Exception as e:
                logger.error(f"Error in crawler loop: {str(e)}")
                # Wait before retrying
                time.sleep(60)

if __name__ == "__main__":
    crawler = DocsCrawler()
    crawler.run()