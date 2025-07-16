import streamlit as st
import os
from utils.gemini_client import GeminiClient
from utils.translator import Translator
from utils.itinerary_generator import ItineraryGenerator

# Page configuration
st.set_page_config(
    page_title="Saanchari - Your Travel Companion",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for brand styling
st.markdown("""
<style>
    .main-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0;
        border-bottom: 2px solid #F75768;
        margin-bottom: 2rem;
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .logo-text {
        font-size: 2rem;
        font-weight: bold;
        color: #07546B;
        margin: 0;
    }
    
    .tagline {
        font-size: 0.9rem;
        color: #FB6957;
        margin: 0;
    }
    
    .language-selector {
        background-color: #F75768;
        color: white;
        border-radius: 8px;
        padding: 0.5rem;
    }
    
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        padding: 1rem;
        border: 1px solid #CFD1D1;
        border-radius: 10px;
        background-color: #FAFAFA;
    }
    
    .user-message {
        background-color: #F75768;
        color: white;
        padding: 0.8rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        margin-left: 20%;
        text-align: right;
    }
    
    .bot-message {
        background-color: #07546B;
        color: white;
        padding: 0.8rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        margin-right: 20%;
    }
    
    .itinerary-container {
        background-color: #FB6957;
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .day-item {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #F75768;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "language" not in st.session_state:
    st.session_state.language = "English"

# Initialize clients
@st.cache_resource
def initialize_clients():
    gemini_client = GeminiClient()
    translator = Translator()
    itinerary_generator = ItineraryGenerator(gemini_client)
    return gemini_client, translator, itinerary_generator

try:
    gemini_client, translator, itinerary_generator = initialize_clients()
except Exception as e:
    st.error(f"Failed to initialize services: {str(e)}")
    st.stop()

# Header with logo and language selector
col1, col2 = st.columns([3, 1])

with col1:
    # Display logo image
    try:
        from PIL import Image
        logo_image = Image.open("attached_assets/logo_1752680671368.png")
        st.image(logo_image, width=300)
    except:
        st.markdown("""
        <div class="logo-container">
            <div>
                <h1 class="logo-text">🗺️ SAANCHARI</h1>
                <p class="tagline">YOUR TRAVEL COMPANION</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col2:
    selected_language = st.selectbox(
        "Language",
        ["English", "Hindi", "Telugu"],
        index=["English", "Hindi", "Telugu"].index(st.session_state.language),
        key="language_selector"
    )
    if selected_language != st.session_state.language:
        st.session_state.language = selected_language
        st.rerun()

# Welcome message
if not st.session_state.messages:
    welcome_msg = {
        "English": "🙏 Welcome to Saanchari! I'm your travel companion for exploring Anand and Gujarat. Ask me about places to visit, local culture, food recommendations, or say 'itinerary' or 'plan' to get a detailed travel plan!",
        "Hindi": "🙏 सांचारी में आपका स्वागत है! मैं आनंद और गुजरात की खोज के लिए आपका यात्रा साथी हूं। घूमने की जगहों, स्थानीय संस्कृति, खाने की सिफारिशों के बारे में पूछें, या विस्तृत यात्रा योजना के लिए 'यात्रा कार्यक्रम' या 'योजना' कहें!",
        "Telugu": "🙏 సాంచారికి స్వాగతం! ఆనంద్ మరియు గుజరాత్ అన్వేషణకు నేను మీ ప్రయాణ సహచరుడిని. సందర్శించవలసిన ప్రదేశాలు, స్థానిక సంస్కృతి, ఆహార సిఫార్సుల గురించి అడగండి, లేదా వివరణాత్మక ప్రయాణ ప్రణాళిక కోసం 'ప్రయాణ కార్యక్రమం' లేదా 'ప్రణాళిక' అని చెప్పండి!"
    }
    st.session_state.messages.append({
        "role": "assistant",
        "content": welcome_msg[st.session_state.language],
        "original_content": welcome_msg["English"]
    })

# Chat interface
st.markdown("### Chat with Saanchari")

# Display chat messages
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            if "itinerary" in message.get("type", ""):
                st.markdown(f'<div class="itinerary-container">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-message">{message["content"]}</div>', unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Ask me anything about Anand tourism...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner("Thinking..."):
        try:
            # Check if user wants an itinerary
            keywords = ["itinerary", "plan", "trip", "schedule", "यात्रा कार्यक्रम", "योजना", "ప్రయాణ కార్యక్రమం", "ప్రణాళిక"]
            is_itinerary_request = any(keyword.lower() in user_input.lower() for keyword in keywords)
            
            if is_itinerary_request:
                # Generate itinerary
                itinerary = itinerary_generator.generate_itinerary(user_input, st.session_state.language)
                if st.session_state.language != "English":
                    itinerary = translator.translate_text(itinerary, "English", st.session_state.language)
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": itinerary,
                    "type": "itinerary",
                    "original_content": itinerary
                })
            else:
                # Regular chat response
                response = gemini_client.get_tourism_response(user_input, st.session_state.language)
                if st.session_state.language != "English":
                    response = translator.translate_text(response, "English", st.session_state.language)
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "original_content": response
                })
                
        except Exception as e:
            error_msg = {
                "English": f"I apologize, but I'm having technical difficulties. Please try again. Error: {str(e)}",
                "Hindi": f"मुझे खुशी है, लेकिन मुझे तकनीकी कठिनाइयों का सामना कर रहा हूं। कृपया पुनः प्रयास करें। त्रुटि: {str(e)}",
                "Telugu": f"క్షమించండి, నాకు సాంకేతిక ఇబ్బందులు ఉన్నాయి. దయచేసి మళ్లీ ప్రయత్నించండి. లోపం: {str(e)}"
            }
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_msg[st.session_state.language],
                "original_content": error_msg["English"]
            })
    
    st.rerun()

# Sidebar with additional information
with st.sidebar:
    st.markdown("### About Saanchari")
    st.markdown("""
    🗺️ **Saanchari** is your intelligent travel companion for exploring Anand, Gujarat.
    
    **Features:**
    - 💬 Tourism information and recommendations
    - 🗺️ Intelligent itinerary generation
    - 🌐 Multi-language support (English, Hindi, Telugu)
    - 🏛️ Local culture and heritage insights
    - 🍽️ Food and accommodation suggestions
    
    **How to use:**
    - Ask questions about places to visit
    - Request local recommendations
    - Say "itinerary" or "plan" for detailed travel plans
    - Switch languages anytime using the selector
    """)
    
    st.markdown("### Quick Tips")
    st.markdown("""
    - Try: "Show me famous temples in Anand"
    - Try: "Plan a 3-day itinerary for Anand"
    - Try: "Best local food in Anand"
    - Try: "Cultural festivals in Gujarat"
    """)
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #07546B; padding: 1rem;'>
    Made with ❤️ for travelers exploring Anand, Gujarat<br>
    <small>Powered by Google Gemini AI</small>
</div>
""", unsafe_allow_html=True)
