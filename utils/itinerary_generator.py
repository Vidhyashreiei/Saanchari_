import re
from typing import Dict, List
from .gemini_client import GeminiClient

class ItineraryGenerator:
    def __init__(self, gemini_client=None):
        """
        Initialize itinerary generator.
        
        Args:
            gemini_client: Optional GeminiClient instance. If not provided, a new one will be created.
        """
        self.gemini_client = gemini_client if gemini_client is not None else GeminiClient()
    
    def generate_itinerary(self, user_request: str, language: str = "English") -> str:
        """
        Generate a detailed day-wise itinerary based on user request.
        
        Args:
            user_request (str): User's itinerary request
            language (str): Target language for the itinerary
            
        Returns:
            str: Formatted HTML itinerary
        """
        try:
            # Extract duration from user request
            duration = self._extract_duration(user_request)
            
            # Create detailed prompt for itinerary generation
            itinerary_prompt = f"""
            Create a detailed {duration}-day travel itinerary for Andhra Pradesh based on this request: "{user_request}"
            
            REQUIREMENTS:
            - Focus primarily on major cities and attractions in Andhra Pradesh
            - Include practical details: timings, approximate costs, transportation
            - Mix of cultural, historical, spiritual, and local experiences
            - Include local food recommendations for each day
            - Suggest authentic local experiences
            - Consider travel time between locations
            - Include rest periods and meal times
            
            FORMAT THE RESPONSE AS HTML WITH THESE ELEMENTS:
            - Use <h3> for day headers (Day 1, Day 2, etc.)
            - Use <div class="day-item"> for each day's content
            - Use <strong> for time slots and important places
            - Use <br> for line breaks
            - Include emojis for visual appeal
            - Use bullet points with • for activities
            
            SAMPLE STRUCTURE:
            <h3>🗓️ Day 1: Arrival & Visakhapatnam Exploration</h3>
            <div class="day-item">
            <strong>9:00 AM</strong> - Arrival and hotel check-in<br>
            <strong>10:30 AM</strong> - Visit Kailasagiri Hill Park 🏔️<br>
            • Enjoy panoramic views of the city<br>
            • Entry fee: ₹30 per person<br>
            <strong>12:30 PM</strong> - Lunch at local Andhra restaurant<br>
            • Try: Biryani, Pulihora, Andhra meals<br>
            <strong>2:00 PM</strong> - RK Beach visit 🏖️<br>
            <strong>Evening</strong> - Local market exploration<br>
            </div>
            
            Make it comprehensive, practical, and engaging for travelers!
            Language: {language}
            """
            
            # Generate itinerary using Gemini
            itinerary_html = self.gemini_client.get_tourism_response(itinerary_prompt, "English")
            
            # Translate to target language if needed
            if language != "English":
                itinerary_html = translation_service.translate_text(itinerary_html, language)
            
            return f"""
            <h2>🗺️ Your Personalized Andhra Pradesh Travel Itinerary</h2>
            <p style="margin-bottom: 1rem;"><em>Crafted specially for your journey to the land of rich heritage and culture!</em></p>
            {itinerary_html}
            <hr style="margin: 1rem 0;">
            <p><strong>💡 Pro Tips:</strong></p>
            <p>• Best time to visit: October to March<br>
            • Carry comfortable walking shoes<br>
            • Try local Andhra meals at authentic restaurants<br>
            • Book accommodations in advance during festival seasons<br>
            • Respect local customs and traditions</p>
            """
            
        except Exception as e:
            return f"""
            <div class="day-item">
            <h3>❌ Unable to Generate Itinerary</h3>
            <p>I apologize, but I couldn't create your itinerary at the moment.</p>
            <p><strong>Error:</strong> {str(e)}</p>
            <p>Please try again with a simpler request like "3 day plan for Anand" or "weekend trip to Anand".</p>
            </div>
            """
    
    def _extract_duration(self, user_request: str) -> int:
        """Extract duration in days from user request."""
        # Look for patterns like "3 days", "5-day", "one week", etc.
        patterns = [
            r'(\d+)\s*days?',
            r'(\d+)-day',
            r'(\d+)\s*nights?',
            r'one\s+day' 
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_request.lower())
            if match:
                if pattern == r'one\s+day':
                    return 1
                return int(match.group(1))
        
        # Default duration based on request context
        if any(word in user_request.lower() for word in ['weekend', 'short']):
            return 2
        elif any(word in user_request.lower() for word in ['week', 'long', 'extended']):
            return 7
        else:
            return 3  # Default 3-day itinerary
    
    def _is_html_formatted(self, text: str) -> bool:
        """Check if text contains HTML formatting."""
        html_tags = ['<h3>', '<div>', '<strong>', '<br>', '<p>']
        return any(tag in text for tag in html_tags)
    
    def _split_into_chunks(self, text: str, max_length: int = 3000) -> list:
        """Split text into chunks of maximum length, trying to split at sentence boundaries."""
        if len(text) <= max_length:
            return [text]
            
        # Try to split at sentence boundaries
        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) + 1 <= max_length:
                current_chunk += (sentence + " ")
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + " "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
            
        return chunks
    
    def _format_as_html(self, text: str) -> str:
        """Convert plain text itinerary to HTML format."""
        lines = text.split('\n')
        formatted_lines = []
        current_day = None
        in_day_content = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check for day headers
            if re.match(r'day\s+\d+', line.lower()) or re.match(r'\d+\.\s*day', line.lower()):
                if in_day_content:
                    formatted_lines.append('</div>')
                formatted_lines.append(f'<h3>🗓️ {line}</h3>')
                formatted_lines.append('<div class="day-item">')
                in_day_content = True
            
            # Check for time-based activities
            elif re.match(r'\d+:\d+\s*(am|pm)', line.lower()) or line.startswith('-'):
                if ':' in line and ('am' in line.lower() or 'pm' in line.lower()):
                    # Time-based activity
                    parts = line.split('-', 1)
                    if len(parts) == 2:
                        time_part = parts[0].strip()
                        activity_part = parts[1].strip()
                        formatted_lines.append(f'<strong>{time_part}</strong> - {activity_part}<br>')
                    else:
                        formatted_lines.append(f'<strong>{line}</strong><br>')
                else:
                    # Regular activity
                    formatted_lines.append(f'• {line.lstrip("- ")}<br>')
            
            else:
                # Regular content
                formatted_lines.append(f'{line}<br>')
        
        if in_day_content:
            formatted_lines.append('</div>')
        
        return '\n'.join(formatted_lines)
