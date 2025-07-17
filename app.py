import os
import streamlit as st
from dotenv import load_dotenv
from pathlib import Path
from PIL import Image
import google.generativeai as genai
from utils.gemini_client import GeminiClient
from utils.itinerary_generator import ItineraryGenerator

# Load environment variables from .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Verify API key is loaded
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("Error: GEMINI_API_KEY not found in environment variables. Please check your .env file.")
    st.stop()

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# UI Text Constants (in English, will be translated on the fly)
UI_TEXT = {
    "page_title": "Saanchari - Your Travel Companion",
    "language_label": "Language",
    "welcome_message": "🙏 Welcome to Saanchari! I'm your travel companion for exploring Andhra Pradesh. Ask me about places to visit, local culture, food recommendations, or say 'itinerary' or 'plan' to get a detailed travel plan!",
    "quick_actions": ["🏛️ Famous Temples", "🏖️ Beach Destinations", "📋 Plan My Trip"],
    "chat_placeholder": "Ask me anything about Andhra Pradesh tourism...",
    "thinking": "Thinking...",
    "error_message": "I apologize, but I'm having technical difficulties. Please try again.",
    "temple_query": "Tell me about famous temples in Andhra Pradesh",
    "beach_query": "Show me beautiful beach destinations in Andhra Pradesh",
    "plan_query": "Help me plan a 3-day trip to Andhra Pradesh"
}

# Available languages
LANGUAGES = ["English", "Hindi", "Telugu"]
LANGUAGE_CODES = {
    "English": "English",
    "Hindi": "Hindi",
    "Telugu": "Telugu"
}

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "language" not in st.session_state:
    st.session_state.language = "English"

# Initialize Gemini client
gemini_client = GeminiClient()

# Initialize Itinerary Generator
itinerary_generator = ItineraryGenerator(gemini_client)

# Function to translate text using Gemini API
def translate_text(text, target_lang):
    """Translate text using Gemini API"""
    if not text or target_lang == "English":
        return text
        
    try:
        # Initialize Gemini with API key
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            st.error("GEMINI_API_KEY not found in environment variables")
            return text
            
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        # Split long text into chunks to avoid token limits
        max_chunk_length = 1000
        if len(text) <= max_chunk_length:
            chunks = [text]
        else:
            chunks = [text[i:i+max_chunk_length] for i in range(0, len(text), max_chunk_length)]
            
        translated_chunks = []
        for chunk in chunks:
            try:
                prompt = f"Translate the following text to {target_lang}. Only return the translated text without any additional text or explanations. Here's the text to translate: \"{chunk}\""
                response = model.generate_content(prompt)
                if hasattr(response, 'text') and response.text:
                    translated_chunks.append(response.text.strip())
                else:
                    translated_chunks.append(chunk)  # Fallback to original text if translation fails
            except Exception as e:
                st.warning(f"Error translating chunk: {str(e)}")
                translated_chunks.append(chunk)  # Fallback to original text on error
                
        return " ".join(translated_chunks)
        
    except Exception as e:
        st.warning(f"Translation failed: {str(e)}")
        return text

# Function to get translated text
def get_text(key, target_lang=None):
    """Get translated text for the given key in the target language."""
    if not target_lang:
        target_lang = st.session_state.language
    
    if target_lang == "English":
        return UI_TEXT.get(key, key)
    
    text = UI_TEXT.get(key, key)
    return translate_text(text, target_lang)

# Page configuration
st.set_page_config(
    page_title=get_text("page_title"),
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

# Header with logo and language selector
col1, col2 = st.columns([3, 1])

with col1:
    # Display logo image
    try:
        logo_image = Image.open("attached_assets/logo_1752680671368.png")
        st.image(logo_image, width=200)
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
        get_text("language_label"),
        LANGUAGES,
        index=LANGUAGES.index(st.session_state.language) if st.session_state.language in LANGUAGES else 0,
        label_visibility="collapsed"
    )
    if selected_language != st.session_state.language:
        st.session_state.language = selected_language
        st.rerun()

# Welcome message
if not st.session_state.messages:
    st.session_state.messages.append({
        "role": "assistant",
        "content": get_text("welcome_message"),
        "original_content": UI_TEXT["welcome_message"]
    })

# Chat interface
#st.markdown("### Chat with Saanchari")

# Quick action buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button(get_text("quick_actions")[0], key="temples"):
        user_input = get_text("temple_query")
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.rerun()
        
with col2:
    if st.button(get_text("quick_actions")[1], key="beaches"):
        user_input = get_text("beach_query")
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.rerun()
        
with col3:
    if st.button(get_text("quick_actions")[2], key="plan"):
        user_input = get_text("plan_query")
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

# Check for unprocessed user messages (from buttons or chat input)
should_process_response = False
latest_user_message = None

# Check if last message is a user message without a corresponding AI response
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    should_process_response = True
    latest_user_message = st.session_state.messages[-1]["content"]

# Chat input container
with st.container():
    st.markdown("<div style='padding-bottom: 80px;'></div>", unsafe_allow_html=True)
    user_input = st.chat_input(get_text("chat_placeholder"))

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    should_process_response = True
    latest_user_message = user_input

if should_process_response and latest_user_message:
    with st.spinner(get_text("thinking")):
        try:
            # Check if user wants an itinerary
            keywords = ["itinerary", "plan", "trip", "schedule", "यात्रा कार्यक्रम", "योजना", "ప్రయాణ కార్యక్రమం", "ప్రణాళిక"]
            is_itinerary_request = any(keyword.lower() in latest_user_message.lower() for keyword in keywords)
            
            if is_itinerary_request:
                # Generate itinerary in English first
                itinerary = itinerary_generator.generate_itinerary(latest_user_message, "English")
                # Then translate if needed
                if st.session_state.language != "English":
                    itinerary = translation_service.translate_text(itinerary, st.session_state.language)
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": itinerary,
                    "type": "itinerary",
                    "original_content": itinerary
                })
            else:
                # Get response in the target language
                response = gemini_client.get_tourism_response(latest_user_message, st.session_state.language)
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "original_content": response
                })
                
        except Exception as e:
            error_msg = f"{get_text('error_message')} Error: {str(e)}"
            # Translate error message if needed
            if st.session_state.language != "English":
                error_msg = translate_text(error_msg, st.session_state.language)
            
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
    <small style='color: #07546B;'>Kshipani Tech Ventures Pvt Ltd.</small>
</div>
""", unsafe_allow_html=True)
