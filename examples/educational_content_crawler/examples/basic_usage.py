import os
from dotenv import load_dotenv
from educational_crawler import EducationalCrawler

# Load environment variables
load_dotenv()

def main():
    # Initialize crawler
    crawler = EducationalCrawler(
        api_key=os.getenv("FIRECRAWL_API_KEY"),
        llm_api_key=os.getenv("LLM_API_KEY")
    )
    
    # Define educational websites to crawl
    websites = [
        "https://www.khanacademy.org/math/algebra",
        "https://www.coursera.org/learn/python-programming"
    ]
    
    # Crawl and process content
    content = crawler.crawl_and_process(
        urls=websites,
        validate=True,
        extract_metadata=True
    )
    
    # Print results
    for item in content:
        print(f"\nTitle: {item.title}")
        print(f"Subject: {item.metadata.subject}")
        print(f"Grade Level: {item.metadata.grade_level}")
        print(f"Validation Score: {item.validation_result.score}")
        if item.validation_result.issues:
            print("Issues:", item.validation_result.issues)
        print("-" * 50)

if __name__ == "__main__":
    main()