"""
AI Training Data Collector Example

This module demonstrates how to safely collect and validate training data
using Firecrawl's batch processing capabilities.
"""

import os
from datetime import datetime
from typing import List, Dict, Optional
from uuid import uuid4

from dotenv import load_dotenv
from firecrawl import FirecrawlApp
from pydantic import BaseModel, Field
from tqdm import tqdm

# Load environment variables
load_dotenv()

class SafetyConfig(BaseModel):
    """Configuration for content safety and quality checks"""
    min_quality_score: float = Field(default=0.7, ge=0, le=1)
    max_toxicity: float = Field(default=0.3, ge=0, le=1)
    required_attributes: List[str] = Field(default=["content"])
    
class QualityMetrics(BaseModel):
    """Quality metrics for collected content"""
    coherence: float = Field(ge=0, le=1)
    relevance: float = Field(ge=0, le=1)
    toxicity: float = Field(ge=0, le=1)

class CollectedItem(BaseModel):
    """Represents a single collected and validated item"""
    id: str
    content: str
    metadata: Dict
    quality_metrics: QualityMetrics

class CollectionStats(BaseModel):
    """Statistics about the collection process"""
    total_processed: int = 0
    passed_safety: int = 0
    failed_safety: int = 0
    average_quality: float = 0.0

class DataCollector:
    """Main collector class for gathering AI training data"""
    
    def __init__(
        self,
        safety_config: Optional[SafetyConfig] = None,
        api_key: Optional[str] = None
    ):
        self.safety_config = safety_config or SafetyConfig()
        self.app = FirecrawlApp(api_key=api_key or os.getenv("FIRECRAWL_API_KEY"))
        self.stats = CollectionStats()

    def _create_extraction_schema(self) -> dict:
        """Create schema for content extraction with safety checks"""
        return {
            "type": "object",
            "properties": {
                "content": {"type": "string"},
                "title": {"type": "string"},
                "author": {"type": "string"},
                "quality_metrics": {
                    "type": "object",
                    "properties": {
                        "coherence": {"type": "number"},
                        "relevance": {"type": "number"},
                        "toxicity": {"type": "number"}
                    }
                }
            },
            "required": self.safety_config.required_attributes
        }

    def _passes_safety_checks(self, item: dict) -> bool:
        """Check if an item passes safety and quality thresholds"""
        metrics = item.get("quality_metrics", {})
        
        if not metrics:
            return False
            
        # Check quality thresholds
        quality_score = (
            metrics.get("coherence", 0) +
            metrics.get("relevance", 0)
        ) / 2
        
        if quality_score < self.safety_config.min_quality_score:
            return False
            
        if metrics.get("toxicity", 1) > self.safety_config.max_toxicity:
            return False
            
        return True

    def collect_from_urls(
        self,
        urls: List[str],
        batch_size: int = 10
    ) -> Dict:
        """
        Collect and validate content from a list of URLs
        
        Args:
            urls: List of URLs to process
            batch_size: Number of URLs to process in each batch
            
        Returns:
            Dictionary containing collected items and stats
        """
        collected_items = []
        
        # Create extraction schema
        schema = self._create_extraction_schema()
        
        # Process URLs in batches
        for i in tqdm(range(0, len(urls), batch_size)):
            batch_urls = urls[i:i + batch_size]
            
            try:
                # Batch scrape with extraction
                batch_results = self.app.batch_scrape(
                    urls=batch_urls,
                    params={
                        "extract": {"schema": schema}
                    }
                )
                
                # Process results
                for result in batch_results.get("data", []):
                    self.stats.total_processed += 1
                    
                    if self._passes_safety_checks(result["extract"]):
                        self.stats.passed_safety += 1
                        
                        # Create collected item
                        item = CollectedItem(
                            id=str(uuid4()),
                            content=result["extract"]["content"],
                            metadata={
                                "source_url": result["metadata"]["sourceURL"],
                                "extraction_date": datetime.utcnow().isoformat(),
                                "title": result["extract"].get("title", ""),
                                "author": result["extract"].get("author", "")
                            },
                            quality_metrics=QualityMetrics(
                                **result["extract"]["quality_metrics"]
                            )
                        )
                        
                        collected_items.append(item.model_dump())
                    else:
                        self.stats.failed_safety += 1
                        
            except Exception as e:
                print(f"Error processing batch: {str(e)}")
                continue
                
        # Calculate final stats
        if self.stats.passed_safety > 0:
            self.stats.average_quality = sum(
                item["quality_metrics"]["coherence"] +
                item["quality_metrics"]["relevance"]
                for item in collected_items
            ) / (2 * self.stats.passed_safety)
            
        return {
            "items": collected_items,
            "stats": self.stats.model_dump()
        }

if __name__ == "__main__":
    # Example usage
    urls = [
        "https://example.com/article1",
        "https://example.com/article2"
    ]
    
    collector = DataCollector()
    results = collector.collect_from_urls(urls)
    
    print(f"Collection completed: {results['stats']}")