import re
from typing import Dict, List
from .gemini_client import GeminiClient

class ItineraryGenerator:
    def __init__(self, gemini_client: GeminiClient):
        """Initialize itinerary generator with Gemini client."""
        self.gemini_client = gemini_client
    
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
            Create a detailed {duration}-day travel itinerary for Anand, Gujarat based on this request: "{user_request}"
            
            REQUIREMENTS:
            - Focus primarily on Anand and nearby attractions within 50km
            - Include practical details: timings, approximate costs, transportation
            - Mix of cultural, historical, spiritual, and local experience
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
            <h3>🗓️ Day 1: Arrival & Anand Exploration</h3>
            <div class="day-item">
            <strong>9:00 AM</strong> - Arrival and hotel check-in<br>
            <strong>10:30 AM</strong> - Visit Amul Dairy Museum 🥛<br>
            • Learn about the White Revolution<br>
            • Entry fee: ₹20 per person<br>
            <strong>12:30 PM</strong> - Lunch at local Gujarati restaurant<br>
            • Try: Dhokla, Thepla, Gujarati Thali<br>
            <strong>2:00 PM</strong> - ISKCON Temple visit 🏛️<br>
            <strong>Evening</strong> - Local market exploration<br>
            </div>
            
            Make it comprehensive, practical, and engaging for travelers!
            Language: {language}
            """
            
            response = self.gemini_client.generate_structured_response(itinerary_prompt)
            
            # If response doesn't contain HTML formatting, format it
            if not self._is_html_formatted(response):
                response = self._format_as_html(response)
            
            return f"""
            <h2>🗺️ Your Personalized Anand Travel Itinerary</h2>
            <p style="margin-bottom: 1rem;"><em>Crafted specially for your journey to the Milk Capital of India!</em></p>
            {response}
            <hr style="margin: 1rem 0;">
            <p><strong>💡 Pro Tips:</strong></p>
            <p>• Best time to visit: October to March<br>
            • Carry comfortable walking shoes<br>
            • Try local Gujarati thali at authentic restaurants<br>
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
