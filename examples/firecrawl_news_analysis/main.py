import argparse
import logging
from typing import List, Dict

from config import DEFAULT_SEARCH_PARAMS, LOGGING_CONFIG
from utils.helpers import validate_date
from api_clients.firecrawl_client import FirecrawlNewsClient
from data_processing.analyzer import NewsAnalyzer

def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=LOGGING_CONFIG['level'],
        format=LOGGING_CONFIG['format']
    )

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='Firecrawl News Analysis Tool')
    parser.add_argument('--query', default=DEFAULT_SEARCH_PARAMS['query'], 
                        help='Search query for news articles')
    parser.add_argument('--from-date', default=DEFAULT_SEARCH_PARAMS['from_date'], 
                        help='Start date for news search (YYYY-MM-DD)')
    parser.add_argument('--to-date', default=DEFAULT_SEARCH_PARAMS['to_date'], 
                        help='End date for news search (YYYY-MM-DD)')
    
    return parser.parse_args()

def main():
    """
    Main application workflow for news analysis.
    
    Steps:
    1. Parse arguments
    2. Validate dates
    3. Fetch news articles using Firecrawl
    4. Perform analysis
    5. Display results
    """
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Parse command-line arguments
        args = parse_arguments()
        
        # Validate and standardize dates
        from_date = validate_date(args.from_date)
        to_date = validate_date(args.to_date)
        
        # Initialize Firecrawl client
        firecrawl_client = FirecrawlNewsClient()
        
        # Fetch news articles
        logger.info(f"Searching news for query: {args.query}")
        news_articles = firecrawl_client.search_news(
            query=args.query, 
            from_date=from_date, 
            to_date=to_date
        )
        
        # Perform news analysis
        analyzer = NewsAnalyzer(news_articles)
        analysis_results = {
            'total_articles': len(news_articles),
            'sentiment_summary': analyzer.analyze_sentiment(),
            'top_keywords': analyzer.extract_top_keywords(),
            'source_distribution': analyzer.analyze_sources()
        }
        
        # Display results
        print("\n--- News Analysis Results ---")
        print(f"Total Articles: {analysis_results['total_articles']}")
        print("\nSentiment Summary:")
        for sentiment, count in analysis_results['sentiment_summary'].items():
            print(f"{sentiment.capitalize()}: {count}")
        
        print("\nTop Keywords:")
        for keyword, freq in analysis_results['top_keywords'].items():
            print(f"{keyword}: {freq}")
        
        print("\nNews Sources:")
        for source, count in analysis_results['source_distribution'].items():
            print(f"{source}: {count}")
    
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()