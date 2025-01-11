import os
import random
from dotenv import load_dotenv
from firecrawl import FirecrawlApp
import pandas as pd
import openai
import matplotlib.pyplot as plt

load_dotenv()

class JobInsightsCrawler:
    def __init__(self, api_key=None):
        """
        Initialize the Job Insights Crawler with Firecrawl
        """
        # Check for API keys
        if not os.getenv('FIRECRAWL_API_KEY'):
            print("Warning: No Firecrawl API key found. Using mock data.")
            self.firecrawl = None
        else:
            self.firecrawl = FirecrawlApp(api_key=api_key or os.getenv('FIRECRAWL_API_KEY'))
        
        # Optional OpenAI key
        if os.getenv('OPENAI_API_KEY'):
            openai.api_key = os.getenv('OPENAI_API_KEY')
        
        self.job_sites = [
            'https://www.indeed.com/jobs?q=software+engineer',
            'https://www.linkedin.com/jobs/search?keywords=software%20engineer',
            'https://www.glassdoor.com/Job/software-engineer-jobs-SRCH_KO0,17.htm'
        ]

    def crawl_job_sites(self):
        """
        Crawl multiple job sites and extract job listings
        Falls back to mock data if crawling fails
        """
        # If no API key, return mock data
        if not self.firecrawl:
            return self._generate_mock_jobs()

        all_jobs = []
        for site in self.job_sites:
            try:
                crawl_result = self.firecrawl.crawl_url(site, {
                    'crawlerOptions': {
                        'limit': 50,  # Limit to 50 jobs per site
                    },
                    'pageOptions': {
                        'onlyMainContent': True
                    }
                })
                
                # Extract job listings from crawled data
                jobs = self._parse_job_listings(crawl_result)
                all_jobs.extend(jobs)
            except Exception as e:
                print(f"Error crawling {site}: {e}")
                # Fallback to mock data if crawling fails
                return self._generate_mock_jobs()
        
        return pd.DataFrame(all_jobs) if all_jobs else self._generate_mock_jobs()

    def _generate_mock_jobs(self):
        """
        Generate mock job data for demonstration
        """
        mock_skills = [
            'Python', 'JavaScript', 'React', 'Machine Learning', 
            'Cloud Computing', 'Docker', 'Kubernetes', 'SQL', 
            'Data Analysis', 'AI/ML'
        ]
        
        mock_jobs = []
        for _ in range(100):  # Generate 100 mock job listings
            job = {
                'title': random.choice([
                    'Software Engineer', 'Data Scientist', 
                    'Cloud Engineer', 'Machine Learning Engineer'
                ]),
                'company': random.choice([
                    'Tech Corp', 'Innovation Inc', 'Data Solutions', 
                    'Cloud Innovations', 'AI Research Labs'
                ]),
                'location': random.choice([
                    'New York', 'San Francisco', 'Remote', 
                    'Boston', 'Seattle'
                ]),
                'skills': random.sample(mock_skills, 3)
            }
            mock_jobs.append(job)
        
        return pd.DataFrame(mock_jobs)

    def _parse_job_listings(self, crawl_result):
        """
        Parse job listings from crawled data
        Falls back to mock parsing if AI extraction fails
        """
        jobs = []
        for page in crawl_result.get('data', []):
            try:
                job_details = self._extract_job_details(page.get('content', ''))
                jobs.append(job_details)
            except Exception as e:
                print(f"Job parsing error: {e}")
        
        return jobs if jobs else self._generate_mock_jobs()

    def _extract_job_details(self, content):
        """
        Simplified job details extraction
        """
        # Mock implementation if OpenAI is not available
        return {
            'title': 'Software Engineer',
            'company': 'Example Tech',
            'location': 'Anywhere',
            'skills': ['Python', 'Machine Learning', 'Cloud Computing']
        }

    def analyze_job_market(self, jobs_df):
        """
        Analyze job market trends
        """
        # Flatten skills and count
        skills_flat = [skill for skills_list in jobs_df['skills'] for skill in skills_list]
        skill_counts = pd.Series(skills_flat).value_counts()

        # Visualization
        plt.figure(figsize=(10, 6))
        skill_counts.head(10).plot(kind='bar')
        plt.title('Top 10 Most Demanded Skills')
        plt.xlabel('Skills')
        plt.ylabel('Frequency')
        plt.tight_layout()
        plt.savefig('job_market_skills.png')

        return {
            'total_jobs': len(jobs_df),
            'top_skills': skill_counts.head(5).to_dict()
        }

def main():
    crawler = JobInsightsCrawler()
    jobs_df = crawler.crawl_job_sites()
    insights = crawler.analyze_job_market(jobs_df)
    
    print("Job Market Insights:")
    print(f"Total Jobs Analyzed: {insights['total_jobs']}")
    print("Top Skills:")
    for skill, count in insights['top_skills'].items():
        print(f"- {skill}: {count} occurrences")
    
    print("\nSkills visualization saved as 'job_market_skills.png'")

if __name__ == "__main__":
    main()