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

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/saanchari-tourism.git
   cd saanchari-tourism
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root and add:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

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

## Development Notes

### Translation Implementation

Initially, we experimented with using the `googletrans` and `deep-translator` packages for language translation. However, we encountered compatibility issues with other dependencies in the project. After several iterations, we decided to leverage the Gemini API for all translations, which provided better stability and simplified our dependency management. This approach ensures consistent behavior across different environments and eliminates potential conflicts with other packages.
