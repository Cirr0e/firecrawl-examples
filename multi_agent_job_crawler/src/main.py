import os
from dotenv import load_dotenv

from .web_crawler import JobWebCrawler
from .job_matcher import JobMatcher
from .ai_agent import JobInsightAgent

def main():
    load_dotenv()
    
    # User Profile (configurable)
    user_profile = {
        'skills': 'Python, Machine Learning, AI, Data Science',
        'experience_level': 'Entry Level',
        'desired_roles': 'Software Engineer, AI Developer'
    }
    
    # Job Search Configuration
    job_title = os.getenv('TARGET_JOB_TITLE', 'Software Engineer')
    locations = os.getenv('TARGET_LOCATIONS', ['San Francisco', 'New York', 'Remote']).split(',')
    
    # Initialize Agents
    web_crawler = JobWebCrawler()
    job_matcher = JobMatcher(user_profile)
    insight_agent = JobInsightAgent()
    
    # Crawl Job Sites
    raw_jobs = web_crawler.crawl_job_sites(job_title, locations)
    preprocessed_jobs = web_crawler.preprocess_jobs(raw_jobs)
    
    # Match Jobs
    matched_jobs = job_matcher.match_jobs(preprocessed_jobs)
    
    # Generate Insights
    market_insights = insight_agent.generate_job_insights(matched_jobs)
    
    # Display Results
    print("Top Matched Jobs:")
    print(matched_jobs[['title', 'company', 'match_score']].to_string())
    
    print("\nMarket Insights:")
    print(market_insights)

if __name__ == "__main__":
    main()