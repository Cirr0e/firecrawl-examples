import os
from anthropic import Anthropic
from openai import OpenAI
import pandas as pd

class JobInsightAgent:
    def __init__(self):
        self.anthropic_client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    def generate_job_insights(self, job_df):
        """
        Generate insights about job market trends
        
        Args:
            job_df (pd.DataFrame): Ranked job listings
        
        Returns:
            dict: Job market insights
        """
        insights = {}
        
        # Company Trend Analysis
        top_companies = job_df['company'].value_counts()
        insights['top_hiring_companies'] = top_companies.to_dict()
        
        # Salary Range Analysis
        job_df['salary'] = job_df['salary_range'].apply(self._extract_salary)
        salary_stats = job_df['salary'].describe()
        insights['salary_statistics'] = salary_stats.to_dict()
        
        # AI-Generated Market Trend Report
        trend_report = self._generate_trend_analysis(job_df)
        insights['trend_report'] = trend_report
        
        return insights
    
    def _extract_salary(self, salary_str):
        """
        Extract numeric salary from string
        """
        try:
            # Basic salary extraction logic
            digits = ''.join(filter(str.isdigit, salary_str))
            return float(digits) if digits else np.nan
        except:
            return np.nan
    
    def _generate_trend_analysis(self, job_df):
        """
        Generate AI-powered trend analysis
        """
        prompt = f"""
        Analyze the following job market data and provide insights:
        
        Companies Hiring: {job_df['company'].value_counts().head()}
        Job Titles: {job_df['title'].value_counts().head()}
        
        Provide a concise report on:
        1. Current job market trends
        2. Skills in high demand
        3. Potential growth areas
        """
        
        response = self.anthropic_client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text