import re
from datetime import datetime, timedelta
from typing import Dict, Any

def validate_date(date_str: str) -> str:
    """
    Validate and standardize date input.
    
    Args:
        date_str (str): Input date string
    
    Returns:
        str: Validated date in YYYY-MM-DD format
    """
    try:
        # Try parsing the date in various formats
        for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%d-%m-%Y']:
            try:
                parsed_date = datetime.strptime(date_str, fmt)
                return parsed_date.strftime('%Y-%m-%d')
            except ValueError:
                continue
        
        # If no format matches, raise ValueError
        raise ValueError(f"Invalid date format: {date_str}")
    
    except Exception as e:
        print(f"Date validation error: {e}")
        # Default to current date if validation fails
        return datetime.now().strftime('%Y-%m-%d')

def clean_text(text: str) -> str:
    """
    Clean and normalize text.
    
    Args:
        text (str): Input text to clean
    
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # Remove special characters and extra whitespaces
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text.lower()

def extract_keywords(text: str, top_n: int = 10) -> Dict[str, Any]:
    """
    Extract top keywords from text.
    
    Args:
        text (str): Input text
        top_n (int): Number of top keywords to return
    
    Returns:
        Dict: Dictionary of top keywords with their frequencies
    """
    from collections import Counter
    import spacy

    try:
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(text)
        
        # Filter for nouns and proper nouns
        keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN']]
        
        return dict(Counter(keywords).most_common(top_n))
    except Exception as e:
        print(f"Keyword extraction error: {e}")
        return {}