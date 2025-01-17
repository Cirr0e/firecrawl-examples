import os
import yaml
import json
from kafka import KafkaConsumer
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DocsMonitor:
    def __init__(self):
        # Load configuration
        with open('config.yaml', 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Initialize Kafka consumer
        self.consumer = KafkaConsumer(
            self.config['kafka']['topic'],
            bootstrap_servers=self.config['kafka']['bootstrap_servers'],
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            auto_offset_reset='latest',
            enable_auto_commit=True,
            group_id='docs_monitor_group'
        )
        
        # Store last update time for each URL
        self.last_updates = {}

    def detect_changes(self, message):
        """Detect changes in documentation"""
        url = message['url']
        timestamp = datetime.fromisoformat(message['timestamp'])
        
        if url in self.last_updates:
            last_update = self.last_updates[url]
            time_diff = timestamp - last_update
            
            if time_diff.total_seconds() > 0:
                logger.info(f"Documentation updated: {url}")
                logger.info(f"Time since last update: {time_diff}")
                self.last_updates[url] = timestamp
                return True
        else:
            logger.info(f"New documentation detected: {url}")
            self.last_updates[url] = timestamp
            return True
            
        return False

    def process_message(self, message):
        """Process Kafka message"""
        try:
            if self.detect_changes(message):
                # Here you could implement notifications
                # (e.g., send email, Slack message, etc.)
                logger.info(f"Title: {message.get('title', 'No title')}")
                logger.info(f"URL: {message['url']}")
                logger.info("-" * 50)
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")

    def run(self):
        """Main monitor loop"""
        logger.info("Starting documentation monitor...")
        
        try:
            for message in self.consumer:
                self.process_message(message.value)
        except Exception as e:
            logger.error(f"Error in monitor loop: {str(e)}")
        finally:
            self.consumer.close()

if __name__ == "__main__":
    monitor = DocsMonitor()
    monitor.run()