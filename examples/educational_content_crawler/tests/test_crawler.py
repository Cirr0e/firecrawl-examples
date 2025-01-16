import pytest
from educational_crawler import EducationalCrawler
from educational_crawler.models import EducationalContent, ValidationResult

def test_crawler_initialization():
    """Test crawler initialization with API keys"""
    crawler = EducationalCrawler(api_key="test", llm_api_key="test")
    assert crawler.api_key == "test"
    assert crawler.llm_api_key == "test"

def test_crawler_initialization_no_api_key():
    """Test crawler initialization fails without API key"""
    with pytest.raises(ValueError):
        EducationalCrawler()

def test_crawl_and_process():
    """Test crawling and processing content"""
    crawler = EducationalCrawler(api_key="test", llm_api_key="test")
    
    # Mock test URLs
    urls = ["https://test.com/math"]
    
    # Process content
    results = crawler.crawl_and_process(urls)
    
    assert len(results) > 0
    assert isinstance(results[0], EducationalContent)
    assert results[0].validation_result is not None

def test_content_validation():
    """Test content validation"""
    crawler = EducationalCrawler(api_key="test", llm_api_key="test")
    
    # Mock content
    content = EducationalContent(
        title="Test Math Lesson",
        content="This is a test lesson about algebra",
        chunks=[],
        raw_data={}
    )
    
    # Validate content
    validation = crawler.validator.validate(content)
    
    assert isinstance(validation, ValidationResult)
    assert isinstance(validation.score, float)
    assert 0 <= validation.score <= 1