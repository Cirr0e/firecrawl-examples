import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

class JobMatcher:
    def __init__(self, user_profile):
        """
        Initialize job matcher with user profile
        
        Args:
            user_profile (dict): User's skills, experience, preferences
        """
        self.user_profile = user_profile
        self.vectorizer = TfidfVectorizer(stop_words='english')
    
    def match_jobs(self, jobs_df):
        """
        Match jobs based on user profile
        
        Args:
            jobs_df (pd.DataFrame): Job listings
        
        Returns:
            pd.DataFrame: Ranked and matched jobs
        """
        # Create a composite text feature for matching
        jobs_df['match_text'] = (
            jobs_df['title'] + ' ' + 
            jobs_df['description'] + ' ' + 
            jobs_df['company']
        )
        
        # Create user profile text
        user_text = ' '.join([
            self.user_profile.get('skills', ''),
            self.user_profile.get('experience_level', ''),
            self.user_profile.get('desired_roles', '')
        ])
        
        # Vectorize job descriptions and user profile
        job_vectors = self.vectorizer.fit_transform(jobs_df['match_text'])
        user_vector = self.vectorizer.transform([user_text])
        
        # Calculate cosine similarity
        similarity_scores = cosine_similarity(user_vector, job_vectors)[0]
        jobs_df['match_score'] = similarity_scores
        
        # Rank jobs by match score
        ranked_jobs = jobs_df.sort_values('match_score', ascending=False)
        
        return ranked_jobs.head(10)  # Top 10 matched jobs