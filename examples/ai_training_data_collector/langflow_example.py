"""
LangFlow integration example for AI Training Data Collector
"""

import json
import os
from typing import List

from dotenv import load_dotenv
from langflow import LangFlowAPI
from pydantic import BaseModel

from collector import DataCollector, SafetyConfig

# Load environment variables
load_dotenv()

class WorkflowConfig(BaseModel):
    """Configuration for LangFlow workflow"""
    name: str
    description: str
    safety_config: SafetyConfig
    export_format: str = "jsonl"

def create_collection_workflow(config: WorkflowConfig) -> dict:
    """
    Create a LangFlow workflow for data collection
    
    Args:
        config: Workflow configuration
        
    Returns:
        Dictionary containing the workflow definition
    """
    # Define workflow nodes
    nodes = {
        "input": {
            "id": "input_node",
            "type": "input",
            "data": {
                "type": "text",
                "name": "urls",
                "description": "List of URLs to process"
            }
        },
        "collector": {
            "id": "collector_node",
            "type": "python",
            "data": {
                "code": """
                from collector import DataCollector, SafetyConfig
                
                safety_config = SafetyConfig(
                    min_quality_score=${min_quality_score},
                    max_toxicity=${max_toxicity},
                    required_attributes=${required_attributes}
                )
                
                collector = DataCollector(safety_config=safety_config)
                results = collector.collect_from_urls(urls.split('\\n'))
                
                return results
                """,
                "variables": {
                    "min_quality_score": config.safety_config.min_quality_score,
                    "max_toxicity": config.safety_config.max_toxicity,
                    "required_attributes": config.safety_config.required_attributes
                }
            }
        },
        "export": {
            "id": "export_node",
            "type": "python",
            "data": {
                "code": """
                import json
                
                def export_results(results, format='jsonl'):
                    if format == 'jsonl':
                        return '\\n'.join(
                            json.dumps(item) for item in results['items']
                        )
                    return json.dumps(results, indent=2)
                    
                return export_results(results, format='${format}')
                """,
                "variables": {
                    "format": config.export_format
                }
            }
        }
    }
    
    # Define edges connecting nodes
    edges = [
        {
            "source": "input_node",
            "target": "collector_node",
            "sourceHandle": "output",
            "targetHandle": "input"
        },
        {
            "source": "collector_node",
            "target": "export_node",
            "sourceHandle": "output",
            "targetHandle": "input"
        }
    ]
    
    return {
        "name": config.name,
        "description": config.description,
        "nodes": nodes,
        "edges": edges
    }

def run_collection_workflow(
    workflow: dict,
    urls: List[str]
) -> dict:
    """
    Run a LangFlow workflow for data collection
    
    Args:
        workflow: Workflow definition
        urls: List of URLs to process
        
    Returns:
        Results from the workflow execution
    """
    api = LangFlowAPI(
        api_key=os.getenv("LANGFLOW_API_KEY")
    )
    
    # Create workflow
    workflow_id = api.create_workflow(workflow)
    
    # Run workflow
    result = api.run_workflow(
        workflow_id,
        inputs={"urls": "\n".join(urls)}
    )
    
    return result

if __name__ == "__main__":
    # Example usage
    config = WorkflowConfig(
        name="Training Data Collection",
        description="Collect and validate AI training data",
        safety_config=SafetyConfig(
            min_quality_score=0.8,
            max_toxicity=0.2,
            required_attributes=["content", "title", "author"]
        ),
        export_format="jsonl"
    )
    
    # Create workflow
    workflow = create_collection_workflow(config)
    
    # Save workflow definition
    with open("langflow_workflow.json", "w") as f:
        json.dump(workflow, f, indent=2)
    
    # Example URLs
    urls = [
        "https://example.com/article1",
        "https://example.com/article2"
    ]
    
    # Run workflow
    results = run_collection_workflow(workflow, urls)
    print(f"Workflow completed: {results}")