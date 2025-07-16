import os
import logging
from google import genai
from google.genai import types

class GeminiClient:
    def __init__(self):
        """Initialize Gemini client with API key from environment variables."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.5-flash"
        
        # Tourism-focused system prompt for Andhra Pradesh
        self.system_prompt = """
        You are Saanchari, a knowledgeable and friendly tourism guide specializing in Andhra Pradesh, India. 
        You have deep knowledge about:
        
        ANDHRA PRADESH SPECIFIC INFORMATION:
        - Capital: Amaravati, largest city: Visakhapatnam
        - Famous temples: Tirupati Balaji, Srisailam, Vijayawada Kanaka Durga
        - Historical sites: Golconda Fort, Charminar, Warangal Fort
        - Natural attractions: Araku Valley, Horsley Hills, Belum Caves
        - Coastal areas: Visakhapatnam beaches, Rushikonda, Yarada
        - Cultural heritage: Kuchipudi dance, Kalamkari art, handloom textiles
        - Hill stations: Araku Valley, Lambasingi, Ananthagiri Hills
        
        ANDHRA PRADESH TOURISM:
        - Cuisine: Biryani, Pulihora, Pesarattu, Andhra meals, spicy curries
        - Festivals: Ugadi, Dussehra, Sankranti, Brahmotsavam
        - Wildlife: Nagarjunsagar-Srisailam Tiger Reserve, Kolleru Lake
        - Pilgrimage: Tirupati, Srisailam, Vijayawada, Mantralayam
        - Adventure: Trekking in Eastern Ghats, water sports at beaches
        
        GUIDELINES:
        - Always be helpful, informative, and enthusiastic about tourism
        - Provide practical information like timings, costs, transportation when relevant
        - Suggest local experiences and authentic cultural activities
        - Be respectful of local customs and traditions
        - Encourage sustainable and responsible tourism
        - If asked about places outside Andhra Pradesh, acknowledge but gently redirect to Andhra Pradesh
        - Keep responses concise but informative (2-3 paragraphs max for regular queries)
        
        Respond in a warm, friendly tone as if you're a local guide who loves sharing knowledge about the region.
        """
    
    def get_tourism_response(self, user_query: str, language: str = "English") -> str:
        """
        Get tourism-related response from Gemini API.
        
        Args:
            user_query (str): User's question or request
            language (str): Target language for response
            
        Returns:
            str: AI-generated response about tourism
        """
        try:
            # Enhance query with context
            enhanced_query = f"""
            User Query: {user_query}
            
            Please provide a helpful response about Andhra Pradesh tourism. 
            Focus on practical, accurate information that would help a traveler.
            Response language: {language}
            """
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=[
                    types.Content(
                        role="user", 
                        parts=[types.Part(text=enhanced_query)]
                    )
                ],
                config=types.GenerateContentConfig(
                    system_instruction=self.system_prompt,
                    temperature=0.7,
                    max_output_tokens=500
                )
            )
            
            if response.text:
                return response.text.strip()
            else:
                return "I apologize, but I couldn't generate a response. Please try rephrasing your question."
                
        except Exception as e:
            logging.error(f"Error in get_tourism_response: {str(e)}")
            return f"I'm experiencing technical difficulties. Please try again later. Error: {str(e)}"
    
    def generate_structured_response(self, prompt: str, response_schema=None) -> str:
        """
        Generate structured response for specific formats like itineraries.
        
        Args:
            prompt (str): Detailed prompt for structured content
            response_schema: Optional Pydantic model for structured output
            
        Returns:
            str: Structured response from Gemini
        """
        try:
            config = types.GenerateContentConfig(
                system_instruction=self.system_prompt,
                temperature=0.5,
                max_output_tokens=1000
            )
            
            if response_schema:
                config.response_mime_type = "application/json"
                config.response_schema = response_schema
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=[types.Content(role="user", parts=[types.Part(text=prompt)])],
                config=config
            )
            
            if response.text:
                return response.text.strip()
            else:
                return "Unable to generate structured response."
                
        except Exception as e:
            logging.error(f"Error in generate_structured_response: {str(e)}")
            return f"Error generating response: {str(e)}"
