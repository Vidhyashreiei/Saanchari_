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
        self.model = "gemini-1.5-pro"
    
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
            # Simple, focused prompt
            prompt = f"You are a tourism guide for Andhra Pradesh, India. User asks: {user_query}. Provide helpful tourism information about Andhra Pradesh including temples, beaches, food, and attractions. Respond in {language}."
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            if response and response.text:
                return response.text.strip()
            else:
                return self._get_fallback_response(user_query, language)
                
        except Exception as e:
            logging.error(f"Error in get_tourism_response: {str(e)}")
            return self._get_fallback_response(user_query, language)
    
    def _get_fallback_response(self, user_query: str, language: str) -> str:
        """Provide fallback responses when API fails"""
        query_lower = user_query.lower()
        
        # Temple responses
        if any(word in query_lower for word in ['temple', 'mandir', 'देवालय', 'దేవాలయం']):
            responses = {
                "English": """🏛️ **Famous Temples of Andhra Pradesh**

**Tirupati Balaji Temple** - The world's most visited religious site with millions of devotees annually. Located in Tirupati, it's dedicated to Lord Venkateswara.

**Kanaka Durga Temple** - Situated on Indrakeeladri Hill in Vijayawada, this temple offers stunning views of the Krishna River.

**Srisailam Temple** - One of the 12 Jyotirlingas, located in the Nallamala forest along the Krishna River.

*Tip: Book accommodation and darshan tickets in advance, especially for Tirupati.*""",
                "Hindi": """🏛️ **आंध्र प्रदेश के प्रसिद्ध मंदिर**

**तिरुपति बालाजी मंदिर** - दुनिया का सबसे ज्यादा देखा जाने वाला धार्मिक स्थल।

**कनक दुर्गा मंदिर** - विजयवाड़ा में कृष्णा नदी के किनारे स्थित।

**श्रीशैलम मंदिर** - 12 ज्योतिर्लिंगों में से एक, कृष्णा नदी के तट पर।""",
                "Telugu": """🏛️ **ఆంధ్ర ప్రదేశ్ ప్రసిద్ధ దేవాలయాలు**

**తిరుపతి బాలాజీ దేవాలయం** - ప్రపంచంలో అత్యధికంగా సందర్శకులు వచ్చే ఆధ్యాత్మిక కేంద్రం।

**కనక దుర్గా దేవాలయం** - విజయవాడలో కృష్ణా నది ఒడ్డున ఉన్న పవిత్ర క్షేత్రం।

**శ్రీశైలం దేవాలయం** - 12 జ్యోతిర్లింగాలలో ఒకటి, కృష్ణా నది తీరంలో."""
            }
            
        # Beach responses
        elif any(word in query_lower for word in ['beach', 'coast', 'sea', 'समुद्र', 'తీరం']):
            responses = {
                "English": """🏖️ **Beautiful Beaches of Andhra Pradesh**

**Visakhapatnam Beaches** - RK Beach is perfect for evening walks with beautiful sunsets and beach activities.

**Rushikonda Beach** - Known for its golden sand and water sports like surfing and jet skiing.

**Yarada Beach** - A hidden gem with pristine beauty, surrounded by hills and less crowded.

*Activities: Water sports, beach volleyball, local seafood, dolphin watching*""",
                "Hindi": """🏖️ **आंध्र प्रदेश के सुंदर समुद्री तट**

**विशाखापत्तनम बीच** - आरके बीच शाम की सैर और सूर्यास्त के लिए बेहतरीन।

**रुशिकोंडा बीच** - स्वर्णिम रेत और जल क्रीड़ाओं के लिए प्रसिद्ध।

**यारदा बीच** - पहाड़ियों से घिरा हुआ शांत और सुंदर समुद्री तट।""",
                "Telugu": """🏖️ **ఆంధ్ర ప్రదేశ్ అందమైన తీరాలు**

**విశాఖపట్నం తీరాలు** - ఆర్కే బీచ్ సాయంత్రం నడక మరియు సూర్యాస్తమయానికి అద్భుతం.

**రుషికొండ తీరం** - బంగారు ఇసుక మరియు వాటర్ స్పోర్ట్స్ కు ప్రసిద్ధి.

**యారద తీరం** - కొండలతో చుట్టుముట్టబడిన ప్రశాంత మరియు అందమైన ప్రదేశం."""
            }
            
        # Itinerary/Plan responses
        elif any(word in query_lower for word in ['plan', 'itinerary', 'trip', 'योजना', 'ప్రణాళిక']):
            responses = {
                "English": """📋 **3-Day Andhra Pradesh Itinerary**

**Day 1: Tirupati**
- Morning: Tirumala Balaji Temple darshan
- Afternoon: TTD Gardens and local markets
- Evening: Rest and local cuisine

**Day 2: Visakhapatnam**
- Morning: Travel to Vizag (4 hours)
- Afternoon: RK Beach and Submarine Museum
- Evening: Kailasagiri Hill Park

**Day 3: Araku Valley**
- Full day trip to Araku Valley (hill station)
- Coffee plantations and tribal museum
- Return to Vizag evening

*Budget: ₹8,000-12,000 per person including stay, food, and transport*""",
                "Hindi": """📋 **3-दिन आंध्र प्रदेश यात्रा योजना**

**दिन 1: तिरुपति**
- सुबह: तिरुमला बालाजी मंदिर दर्शन
- दोपहर: टीटीडी गार्डन
- शाम: आराम और स्थानीय भोजन

**दिन 2: विशाखापत्तनम**
- सुबह: विजाग की यात्रा
- दोपहर: आरके बीच
- शाम: कैलासगिरि पार्क

**दिन 3: अराकू घाटी**
- पूरा दिन अराकू घाटी
- कॉफी बागान और आदिवासी संग्रहालय""",
                "Telugu": """📋 **3-రోజుల ఆంధ్ర ప్రదేశ్ ప్రయాణ ప్రణాళిక**

**రోజు 1: తిరుపతి**
- ఉదయం: తిరుమల బాలాజీ దర్శనం
- మధ్యాహ్నం: TTD గార్డెన్స్
- సాయంత్రం: విశ్రాంతి మరియు స్థానిక వంటకాలు

**రోజు 2: విశాఖపట్నం**
- ఉదయం: విజాగ్ ప్రయాణం
- మధ్యాహ్నం: ఆర్కే బీచ్
- సాయంత్రం: కైలాసగిరి పార్క్

**రోజు 3: అరకు లోయ**
- పూర్తి రోజు అరకు లోయ సందర్శన
- కాఫీ తోటలు మరియు గిరిజన మ్యూజియం"""
            }
        else:
            responses = {
                "English": """🙏 **Welcome to Andhra Pradesh Tourism!**

Andhra Pradesh offers incredible diversity:

🏛️ **Spiritual Sites**: Tirupati (most visited temple), Srisailam, Vijayawada
🏖️ **Coastal Beauty**: Visakhapatnam beaches, coastal cuisine
🏔️ **Hill Stations**: Araku Valley, Horsley Hills
🍛 **Cuisine**: Spicy Andhra biryani, seafood, traditional thali
🎭 **Culture**: Kuchipudi dance, Kalamkari art, local festivals

Ask me about specific places, food, or say 'plan my trip' for detailed itineraries!""",
                "Hindi": """🙏 **आंध्र प्रदेश पर्यटन में आपका स्वागत है!**

आंध्र प्रदेश की अविश्वसनीय विविधता:

🏛️ **आध्यात्मिक स्थल**: तिरुपति, श्रीशैलम
🏖️ **तटीय सुंदरता**: विशाखापत्तनम के समुद्री तट
🏔️ **पहाड़ी स्टेशन**: अराकू घाटी
🍛 **व्यंजन**: तीखी आंध्र बिरयानी

विशिष्ट स्थानों के बारे में पूछें!""",
                "Telugu": """🙏 **ఆంధ్ర ప్రదేశ్ పర్యటనకు స్వాగతం!**

ఆంధ్ర ప్రదేశ్ యొక్క అద్భుతమైన వైవిధ్యం:

🏛️ **ఆధ్యాత్మిక కేంద్రాలు**: తిరుపతి, శ్రీశైలం
🏖️ **తీర అందాలు**: విశాఖపట్నం తీరాలు
🏔️ **కొండ ప్రాంతాలు**: అరకు లోయ
🍛 **వంటకాలు**: ఆంధ్ర బిర్యానీ, సీఫుడ్

నిర్దిష్ట ప్రదేశాల గురించి అడగండి!"""
            }
        
        return responses.get(language, responses["English"])
    
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
                contents=prompt,
                config=config
            )
            
            if response.text:
                return response.text.strip()
            else:
                return "Unable to generate structured response."
                
        except Exception as e:
            logging.error(f"Error in generate_structured_response: {str(e)}")
            return f"Error generating response: {str(e)}"
