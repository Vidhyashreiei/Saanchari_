import streamlit as st
import os
from utils.gemini_client import GeminiClient
from utils.translator import Translator
from utils.itinerary_generator import ItineraryGenerator

# Page configuration
st.set_page_config(
    page_title="Saanchari - Your Travel Companion",
    page_icon="🗺️",
    layout="wide"
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
        max-height: 600px;
        overflow-y: auto;
        padding: 1.5rem;
        border: 2px solid #CFD1D1;
        border-radius: 15px;
        background: linear-gradient(135deg, #FAFAFA 0%, #F8F9FA 100%);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .user-message {
        background: linear-gradient(135deg, #F75768 0%, #FB6957 100%);
        color: white;
        padding: 1rem 1.2rem;
        border-radius: 20px 20px 5px 20px;
        margin: 1rem 0;
        margin-left: 25%;
        text-align: right;
        box-shadow: 0 2px 4px rgba(247, 87, 104, 0.3);
        font-size: 1rem;
        line-height: 1.6;
    }
    
    .bot-message {
        background: linear-gradient(135deg, #07546B 0%, #0A6B7D 100%);
        color: white;
        padding: 1.2rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 1rem 0;
        margin-right: 25%;
        box-shadow: 0 2px 4px rgba(7, 84, 107, 0.3);
        font-size: 1rem;
        line-height: 1.7;
    }
    
    .bot-message h3 {
        color: #FB6957;
        margin-top: 0;
        margin-bottom: 0.5rem;
    }
    
    .bot-message p {
        margin-bottom: 0.8rem;
    }
    
    .bot-message ul, .bot-message ol {
        margin: 0.5rem 0;
        padding-left: 1.5rem;
    }
    
    .bot-message li {
        margin: 0.3rem 0;
    }
    
    .itinerary-container {
        background: linear-gradient(135deg, #FB6957 0%, #F75768 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px 20px 20px 5px;
        margin: 1rem 0;
        margin-right: 25%;
        box-shadow: 0 4px 8px rgba(251, 105, 87, 0.3);
        font-size: 1rem;
        line-height: 1.7;
    }
    
    .day-item {
        background-color: rgba(255, 255, 255, 0.15);
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.8rem 0;
        border-left: 5px solid #F75768;
        backdrop-filter: blur(5px);
    }
    
    .quick-action-btn {
        background: linear-gradient(135deg, #07546B 0%, #0A6B7D 100%);
        color: white;
        border: none;
        padding: 0.8rem 1.2rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(7, 84, 107, 0.3);
        width: 100%;
        margin: 0.2rem 0;
    }
    
    .quick-action-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(7, 84, 107, 0.4);
        background: linear-gradient(135deg, #0A6B7D 0%, #07546B 100%);
    }
    
    .chat-input-container {
        background: white;
        border-radius: 25px;
        padding: 0.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        border: 2px solid #CFD1D1;
    }
    
    .stButton button {
        background: linear-gradient(135deg, #07546B 0%, #0A6B7D 100%);
        color: white;
        border: none;
        padding: 0.8rem 1.2rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(7, 84, 107, 0.3);
        width: 100%;
        margin: 0.2rem 0;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(7, 84, 107, 0.4);
        background: linear-gradient(135deg, #0A6B7D 0%, #07546B 100%);
    }
    
    .stButton button:focus {
        outline: none;
        box-shadow: 0 0 0 3px rgba(7, 84, 107, 0.3);
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
        "English": "🙏 Welcome to Saanchari! I'm your travel companion for exploring Andhra Pradesh. Ask me about places to visit, local culture, food recommendations, or say 'itinerary' or 'plan' to get a detailed travel plan!",
        "Hindi": "🙏 सांचारी में आपका स्वागत है! मैं आंध्र प्रदेश की खोज के लिए आपका यात्रा साथी हूं। घूमने की जगहों, स्थानीय संस्कृति, खाने की सिफारिशों के बारे में पूछें, या विस्तृत यात्रा योजना के लिए 'यात्रा कार्यक्रम' या 'योजना' कहें!",
        "Telugu": "🙏 సాంచారికి స్వాగతం! ఆంధ్ర ప్రదేశ్ అన్వేషణకు నేను మీ ప్రయాణ సహచరుడిని. సందర్శించవలసిన ప్రదేశాలు, స్థానిక సంస్కృతి, ఆహార సిఫార్సుల గురించి అడగండి, లేదా వివరణాత్మక ప్రయాణ ప్రణాళిక కోసం 'ప్రయాణ కార్యక్రమం' లేదా 'ప్రణాళిక' అని చెప్పండి!"
    }
    st.session_state.messages.append({
        "role": "assistant",
        "content": welcome_msg[st.session_state.language],
        "original_content": welcome_msg["English"]
    })

# Chat interface
st.markdown("### Chat with Saanchari")

# Quick action buttons
quick_actions = {
    "English": ["🏛️ Famous Temples", "🏖️ Beach Destinations", "📋 Plan My Trip"],
    "Hindi": ["🏛️ प्रसिद्ध मंदिर", "🏖️ समुद्री तट", "📋 मेरी यात्रा की योजना"],
    "Telugu": ["🏛️ ప్రసిద్ధ దేవాలయాలు", "🏖️ సముద్ర తీరాలు", "📋 నా ప్రయాణ ప్రణాళిక"]
}

col1, col2, col3 = st.columns(3)
with col1:
    if st.button(quick_actions[st.session_state.language][0], key="temples"):
        user_input = "Tell me about famous temples in Andhra Pradesh"
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.rerun()
        
with col2:
    if st.button(quick_actions[st.session_state.language][1], key="beaches"):
        user_input = "Show me beautiful beach destinations in Andhra Pradesh"
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.rerun()
        
with col3:
    if st.button(quick_actions[st.session_state.language][2], key="plan"):
        user_input = "Create a 3-day itinerary for Andhra Pradesh"
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.rerun()

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
user_input = st.chat_input("Ask me anything about Andhra Pradesh tourism...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner("Thinking..."):
        try:
            # Check if user wants an itinerary
            keywords = ["itinerary", "plan", "trip", "schedule", "यात्रा कार्यक्रम", "योजना", "ప్రయాణ కార్యక్రమం", "ప్రణాళిక"]
            is_itinerary_request = any(keyword.lower() in user_input.lower() for keyword in keywords)
            
            if is_itinerary_request:
                # Generate itinerary in English first
                itinerary = itinerary_generator.generate_itinerary(user_input, "English")
                # Then translate if needed
                if st.session_state.language != "English":
                    itinerary = translator.translate_text(itinerary, "English", st.session_state.language)
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": itinerary,
                    "type": "itinerary",
                    "original_content": itinerary
                })
            else:
                # Regular chat response in English first
                response = gemini_client.get_tourism_response(user_input, "English")
                # Then translate if needed
                if st.session_state.language != "English":
                    response = translator.translate_text(response, "English", st.session_state.language)
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "original_content": response
                })
                
        except Exception as e:
            error_msg = f"I apologize, but I'm having technical difficulties. Please try again. Error: {str(e)}"
            # Translate error message if needed
            if st.session_state.language != "English":
                error_msg = translator.translate_text(error_msg, "English", st.session_state.language)
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_msg,
                "original_content": error_msg
            })
    
    st.rerun()

# Add sticky footer at the bottom
st.markdown("""
<div style='position: fixed; bottom: 0; left: 0; right: 0; background-color: #FFFFFF; 
            border-top: 1px solid #CFD1D1; padding: 0.5rem; text-align: center; z-index: 999;'>
    <small style='color: #07546B;'>Rocket Growth Technologies</small>
</div>
""", unsafe_allow_html=True)
