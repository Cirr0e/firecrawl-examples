import os
import sys
from dotenv import load_dotenv
from firecrawl import FirecrawlApp
from swarms import Agent, SwarmRouter, SwarmType
from pydantic import BaseModel, Field
from typing import List, Dict

load_dotenv()

class ResearchTopic(BaseModel):
    query: str = Field(..., description="Research topic or question")
    domain: List[str] = Field(default=["wikipedia.org", "academic sites"], 
                               description="Preferred research domains")
    depth: int = Field(default=3, ge=1, le=5, 
                       description="Depth of web crawling")

class ResearchOutput(BaseModel):
    key_insights: List[str] = Field(..., description="Main research findings")
    sources: Dict[str, float] = Field(..., description="Source credibility map")
    summary: str = Field(..., description="Comprehensive research summary")

def create_research_agents(research_topic: str):
    firecrawl_app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

    # Web Crawler Agent
    web_crawler_agent = Agent(
        agent_name="Web Crawler Agent",
        system_prompt=f"""
        You are a specialized web crawler agent focused on extracting relevant information 
        for the research topic: {research_topic}. 
        
        Key Responsibilities:
        1. Use Firecrawl to systematically crawl and extract web content
        2. Prioritize high-quality, academic, and reputable sources
        3. Collect comprehensive information across multiple domains
        4. Ensure data relevance and minimize noise
        """,
        max_loops=3
    )

    # Research Analysis Agent
    research_analysis_agent = Agent(
        agent_name="Research Analysis Agent",
        system_prompt=f"""
        You are an expert research analysis agent focusing on the topic: {research_topic}. 
        
        Tasks:
        1. Analyze extracted web content critically
        2. Identify key themes, patterns, and insights
        3. Cross-reference multiple sources
        4. Evaluate source credibility
        5. Generate structured research insights
        """,
        max_loops=2
    )

    # Summary Generation Agent
    summary_agent = Agent(
        agent_name="Summary Generation Agent",
        system_prompt=f"""
        You are a professional research summarization agent for the topic: {research_topic}.
        
        Responsibilities:
        1. Create a concise, coherent research summary
        2. Highlight the most significant findings
        3. Maintain objectivity and clarity
        4. Provide a comprehensive yet accessible overview
        """,
        max_loops=1
    )

    return [web_crawler_agent, research_analysis_agent, summary_agent]

def conduct_web_research(research_topic: ResearchTopic) -> ResearchOutput:
    agents = create_research_agents(research_topic.query)
    
    swarm_router = SwarmRouter(
        name="Web Research Swarm",
        description="Multi-agent web research system",
        agents=agents,
        swarm_type=SwarmType.SequentialWorkflow
    )

    research_result = swarm_router.run(
        f"Conduct comprehensive web research on: {research_topic.query}. "
        f"Focus on domains: {', '.join(research_topic.domain)}. "
        f"Crawling depth: {research_topic.depth}"
    )

    # Here you would add more sophisticated output parsing and validation
    return ResearchOutput(
        key_insights=["Sample Insight 1", "Sample Insight 2"],
        sources={"Wikipedia": 0.9, "Academic Source": 0.85},
        summary="A comprehensive summary of the research findings."
    )

def main():
    if len(sys.argv) < 2:
        print("Please provide a research topic")
        sys.exit(1)

    research_topic = ResearchTopic(query=" ".join(sys.argv[1:]))
    result = conduct_web_research(research_topic)
    
    print("🔍 Research Insights:")
    for insight in result.key_insights:
        print(f"- {insight}")
    
    print("\n📊 Source Credibility:")
    for source, credibility in result.sources.items():
        print(f"{source}: {credibility * 100:.2f}%")
    
    print("\n📝 Summary:")
    print(result.summary)

if __name__ == "__main__":
    main()