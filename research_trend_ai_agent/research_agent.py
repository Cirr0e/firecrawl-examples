import os
import yaml
import argparse
from dotenv import load_dotenv
from firecrawl import FirecrawlApp
from crewai import Agent, Task, Crew
import openai

# Load environment variables
load_dotenv()

# Load configuration
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

class ResearchTrendAgent:
    def __init__(self, topic):
        self.topic = topic
        self.firecrawl_app = FirecrawlApp(api_key=os.getenv('FIRECRAWL_API_KEY'))
        openai.api_key = os.getenv('OPENAI_API_KEY')

    def crawl_sources(self):
        """Crawl and extract content from configured sources"""
        results = []
        for source in config['research']['sources']:
            crawl_result = self.firecrawl_app.crawl_url(
                source, 
                params={
                    'max_depth': config['research']['max_depth'],
                    'format': 'markdown'
                }
            )
            results.extend(crawl_result.get('data', []))
        return results

    def create_research_agents(self, extracted_data):
        """Create AI agents for different research aspects"""
        researcher = Agent(
            role='Technology Trend Researcher',
            goal=f'Extract and synthesize insights about {self.topic}',
            backstory='An expert in technological research and trend analysis',
            verbose=True,
            allow_delegation=True
        )

        trend_analyzer = Agent(
            role='Trend Analyst',
            goal='Identify and interpret emerging technology patterns',
            backstory='A strategic analyst who understands technological shifts',
            verbose=True
        )

        report_generator = Agent(
            role='Report Writer',
            goal='Compile a comprehensive research report',
            backstory='A skilled technical writer who transforms complex insights into clear narratives',
            verbose=True
        )

        research_task = Task(
            description=f'Analyze {self.topic} trends from extracted web data',
            agent=researcher,
            context=extracted_data
        )

        analysis_task = Task(
            description='Generate strategic insights from research',
            agent=trend_analyzer
        )

        report_task = Task(
            description='Create a markdown research report',
            agent=report_generator
        )

        crew = Crew(
            agents=[researcher, trend_analyzer, report_generator],
            tasks=[research_task, analysis_task, report_task]
        )

        return crew

    def run_research(self):
        """Execute the full research workflow"""
        # Crawl sources
        extracted_data = self.crawl_sources()

        # Create and run research crew
        research_crew = self.create_research_agents(extracted_data)
        result = research_crew.kickoff()

        return result

def main():
    parser = argparse.ArgumentParser(description='AI Research Trend Assistant')
    parser.add_argument('--topic', required=True, help='Technology trend to research')
    args = parser.parse_args()

    research_agent = ResearchTrendAgent(args.topic)
    research_report = research_agent.run_research()

    # Save report
    with open(f'{args.topic.replace(" ", "_")}_research_report.md', 'w') as f:
        f.write(research_report)

    print(f"Research report generated for: {args.topic}")

if __name__ == "__main__":
    main()