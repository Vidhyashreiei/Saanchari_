from deep_translator import GoogleTranslator
import logging

class Translator:
    def __init__(self):
        """Initialize Google Translator."""
        self.translator = GoogleTranslator()
        
        # Language code mapping
        self.language_codes = {
            "English": "en",
            "Hindi": "hi", 
            "Telugu": "te"
        }
    
    def translate_text(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Translate text from source language to target language.
        
        Args:
            text (str): Text to translate
            source_lang (str): Source language name
            target_lang (str): Target language name
            
        Returns:
            str: Translated text
        """
        try:
            # Return original text if same language
            if source_lang == target_lang:
                return text
            
            # Get language codes
            source_code = self.language_codes.get(source_lang, "en")
            target_code = self.language_codes.get(target_lang, "en")
            
            # Translate text using deep-translator
            translator = GoogleTranslator(source=source_code, target=target_code)
            result = translator.translate(text)
            
            return result if result else text
            
        except Exception as e:
            logging.error(f"Translation error: {str(e)}")
            # Return original text if translation fails
            return text
    
    def detect_language(self, text: str) -> str:
        """
        Detect the language of given text.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            str: Detected language name
        """
        try:
            # Simple language detection based on script/characters
            if any(ord(char) >= 0x0900 and ord(char) <= 0x097F for char in text):
                return "Hindi"
            elif any(ord(char) >= 0x0C00 and ord(char) <= 0x0C7F for char in text):
                return "Telugu"
            else:
                return "English"  # Default fallback
            
        except Exception as e:
            logging.error(f"Language detection error: {str(e)}")
            return "English"
    
    def get_supported_languages(self) -> list:
        """
        Get list of supported languages.
        
        Returns:
            list: List of supported language names
        """
        return list(self.language_codes.keys())
