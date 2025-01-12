import os
from firecrawl import FirecrawlApp

def main():
    # Check if Firecrawl API key is available
    api_key = os.getenv('FIRECRAWL_API_KEY', 'dummy_key')
    
    try:
        # Initialize Firecrawl App
        app = FirecrawlApp(api_key=api_key)
        
        # Define a safe, public URL to crawl
        url = "https://www.python.org"
        
        # Attempt to crawl the website
        print(f"Attempting to crawl {url}...")
        
        crawl_result = app.crawl_url(
            url, 
            params={
                'limit': 3,
                'crawlerOptions': {
                    'excludes': ['blog/*', '*/comments'],
                },
                'pageOptions': {
                    'onlyMainContent': True
                }
            }
        )
        
        # Print basic crawl results
        print("\nCrawl Results:")
        for page in crawl_result.get('data', []):
            print(f"URL: {page.get('url', 'N/A')}")
            print(f"Content Length: {len(page.get('content', ''))}")
            print("---")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()