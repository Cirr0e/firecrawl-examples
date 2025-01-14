import os
from firecrawl import FirecrawlApp
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

class JobWebCrawler:
    def __init__(self):
        self.firecrawl = FirecrawlApp(api_key=os.getenv('FIRECRAWL_API_KEY'))
        self.job_sites = [
            "https://www.linkedin.com/jobs",
            "https://www.indeed.com/jobs",
            "https://www.glassdoor.com/Jobs"
        ]

    def crawl_job_sites(self, job_title, locations):
        """
        Crawl multiple job sites and extract job listings
        
        Args:
            job_title (str): Job title to search
            locations (list): List of job locations
        
        Returns:
            pd.DataFrame: Extracted job listings
        """
        all_jobs = []
        
        for site in self.job_sites:
            try:
                search_query = f"{job_title} jobs in {', '.join(locations)}"
                crawl_result = self.firecrawl.search(
                    query=search_query,
                    max_pages=5,
                    params={
                        "extractorOptions": {
                            "extractionSchema": {
                                "title": "string",
                                "company": "string",
                                "location": "string",
                                "description": "string",
                                "salary_range": "string",
                                "job_link": "string"
                            }
                        }
                    }
                )
                
                # Process and append results
                for result in crawl_result['results']:
                    job = result.get('metadata', {})
                    all_jobs.append(job)
            
            except Exception as e:
                print(f"Error crawling {site}: {e}")
        
        return pd.DataFrame(all_jobs)

    def preprocess_jobs(self, jobs_df):
        """
        Clean and preprocess job data
        
        Args:
            jobs_df (pd.DataFrame): Raw job listings
        
        Returns:
            pd.DataFrame: Cleaned job listings
        """
        # Basic cleaning
        jobs_df['description'] = jobs_df['description'].fillna('')
        jobs_df['salary_range'] = jobs_df['salary_range'].fillna('Not disclosed')
        
        return jobs_df