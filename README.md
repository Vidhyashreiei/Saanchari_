# Saanchari - Your Travel Companion

A sophisticated tourism chatbot for Andhra Pradesh, built with Streamlit and powered by Google Gemini AI.

## Features

- 🤖 **AI-Powered Chat**: Intelligent responses about Andhra Pradesh tourism using Google Gemini
- 🌐 **Multi-Language Support**: English, Hindi, and Telugu with real-time translation
- 🗺️ **Smart Itinerary Generation**: Day-wise travel plans triggered by keywords
- 🎨 **Brand-Compliant Design**: Professional UI with custom color scheme
- 📱 **Responsive Interface**: Clean, modern chat interface
- 🏛️ **Local Expertise**: Specialized knowledge about Andhra Pradesh tourism

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key

### Installation

1. **Clone or download the project files**

2. **Install required packages**:
   ```bash
   pip install streamlit google-genai deep-translator pillow
   ```

3. **Set up environment variables**:
   ```bash
   export GEMINI_API_KEY="your_gemini_api_key_here"
   
4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## Deployment on Streamlit Cloud

1. **Fork or upload this repository** to your GitHub account

2. **Visit [Streamlit Cloud](https://streamlit.io/cloud)** and sign in with your GitHub account

3. **Click "New app"** and select your repository

4. **Configure the app**:
   - Repository: `your-username/saanchari-chatbot`
   - Branch: `main`
   - Main file path: `app.py`

5. **Add secrets**:
   - In the Streamlit Cloud dashboard, go to "Settings" → "Secrets"
   - Add your environment variables:
     ```toml
     GEMINI_API_KEY = "your_gemini_api_key_here"
     ```

6. **Deploy**: Click "Deploy" and your app will be available at `https://your-app-name.streamlit.app`

## Key Features

- **Quick Action Buttons**: Pre-defined questions for temples, beaches, and trip planning
- **Multi-Language Support**: Seamless translation between English, Hindi, and Telugu
- **Smart Itinerary Generation**: Triggered by keywords like "plan", "itinerary", or "trip"
- **Brand Compliance**: Uses provided color scheme and logo
- **Responsive Design**: Works well on desktop and mobile devices

## Usage Tips

- Use the quick action buttons for common questions
- Try phrases like "Plan a 5-day trip to Andhra Pradesh" for detailed itineraries
- Switch languages anytime using the dropdown in the top right
- Clear chat history using the button below the chat interface
