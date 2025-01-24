from transformers import AutoModelForCausalLM, AutoTokenizer
import json
import logging
from typing import Optional

class Synthesizer:
    def __init__(
        self, 
        model_name: str = 'minimind-v1', 
        max_length: int = 500, 
        temperature: float = 0.7,
        language: str = 'en'
    ):
        """
        Initializes the Synthesizer with the specified language model.
        
        Args:
            model_name (str): Name of the pre-trained language model.
            max_length (int): Maximum length of the generated summary.
            temperature (float): Sampling temperature for text generation.
            language (str): Target language for synthesis.
        """
        try:
            # Select appropriate tokenizer and model based on language
            self.language = language
            self.model_name = self._select_model_for_language(model_name, language)
            
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            
            self.max_length = max_length
            self.temperature = temperature
            
            self.logger = logging.getLogger(__name__)
        except Exception as init_error:
            logging.error(f"Error initializing synthesizer: {init_error}")
            raise

    def _select_model_for_language(
        self, 
        base_model: str, 
        language: str
    ) -> str:
        """
        Select an appropriate model based on the target language.
        
        Args:
            base_model (str): Base model name
            language (str): Target language code
        
        Returns:
            str: Selected model name
        """
        # Language-specific model mappings
        language_model_map = {
            'en': base_model,  # Default English model
            'es': 'spanish-gpt-model',  # Example Spanish model
            'fr': 'french-gpt-model',   # Example French model
            # Add more language models as needed
        }
        
        return language_model_map.get(language, base_model)

    def synthesize_research(
        self, 
        research_data: list, 
        research_topic: str
    ) -> str:
        """
        Synthesizes the research data into a coherent summary using a language model.
        
        Args:
            research_data (list): List of structured research data.
            research_topic (str): The topic of research for contextual synthesis.
        
        Returns:
            str: Synthesized summary of the research findings.
        """
        try:
            # Prepare the synthesis prompt with language-specific context
            synthesis_prompt = self._create_synthesis_prompt(
                research_data, 
                research_topic
            )
            
            # Tokenize the input
            inputs = self.tokenizer(
                synthesis_prompt, 
                return_tensors='pt', 
                max_length=1024, 
                truncation=True
            )
            
            # Generate summary
            outputs = self.model.generate(
                **inputs, 
                max_length=self.max_length,
                num_return_sequences=1,
                do_sample=True,
                temperature=self.temperature
            )
            
            # Decode the generated summary
            summary = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            return summary
        
        except Exception as synthesis_error:
            self.logger.error(f"Error during research synthesis: {synthesis_error}")
            return "Unable to synthesize research summary."

    def _create_synthesis_prompt(
        self, 
        research_data: list, 
        research_topic: str
    ) -> str:
        """
        Create a synthesis prompt with language-specific instructions.
        
        Args:
            research_data (list): Research data to synthesize
            research_topic (str): Research topic
        
        Returns:
            str: Synthesized prompt for language model
        """
        # Language-specific synthesis instructions
        language_instructions = {
            'en': "Synthesize a comprehensive research summary.",
            'es': "Sintetiza un resumen de investigación completo.",
            'fr': "Synthétisez un résumé de recherche complet."
        }
        
        # Default to English if language not found
        instruction = language_instructions.get(self.language, language_instructions['en'])
        
        # Prepare synthesis prompt
        synthesis_prompt = f"{instruction} Topic: {research_topic}\n\n"
        synthesis_prompt += "Research Sources:\n"
        
        for idx, result in enumerate(research_data, 1):
            synthesis_prompt += f"Source {idx}:\n"
            synthesis_prompt += json.dumps(result, indent=2) + "\n\n"
        
        synthesis_prompt += "Synthesize these findings into a coherent, well-structured summary."
        
        return synthesis_prompt