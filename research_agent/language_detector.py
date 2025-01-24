import langdetect
from typing import Dict, List

class LanguageDetector:
    @staticmethod
    def detect_language(text: str) -> str:
        """
        Detect the language of the given text.
        
        Args:
            text (str): Input text to detect language.
        
        Returns:
            str: Detected language code (e.g., 'en', 'es', 'fr')
        """
        try:
            return langdetect.detect(text)
        except Exception:
            return 'en'  # Default to English if detection fails
    
    @staticmethod
    def filter_sources_by_language(
        sources: List[Dict], 
        target_language: str = 'en', 
        min_confidence: float = 0.7
    ) -> List[Dict]:
        """
        Filter sources based on target language.
        
        Args:
            sources (List[Dict]): List of source documents
            target_language (str): Target language code
            min_confidence (float): Minimum language detection confidence
        
        Returns:
            List[Dict]: Filtered sources in the target language
        """
        filtered_sources = []
        
        for source in sources:
            # Check language of title and summary
            text_to_check = f"{source.get('title', '')} {source.get('summary', '')}"
            
            try:
                detected_lang = langdetect.detect(text_to_check)
                
                if detected_lang == target_language:
                    filtered_sources.append(source)
            except Exception:
                # If language detection fails, keep the source
                filtered_sources.append(source)
        
        return filtered_sources