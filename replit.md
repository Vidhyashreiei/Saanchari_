# Saanchari - Tourism Chatbot for Anand, Gujarat

## Overview

Saanchari is a sophisticated tourism chatbot built with Streamlit that serves as a digital travel companion for visitors to Anand, Gujarat, India. The application leverages Google Gemini AI to provide intelligent, contextual responses about local tourism, attractions, and cultural experiences. The system is designed with a focus on local expertise, multi-language support, and intelligent itinerary generation capabilities.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a modular, utility-based architecture with clear separation of concerns:

**Frontend**: Streamlit-based web interface with custom CSS styling for brand compliance
**Backend**: Python-based services utilizing Google Gemini AI for natural language processing
**Translation Layer**: Google Translate integration for multi-language support
**Specialized Modules**: Domain-specific utilities for tourism guidance and itinerary generation

The architecture prioritizes maintainability, scalability, and ease of deployment while keeping dependencies minimal.

## Key Components

### Core Application (`app.py`)
- **Main Streamlit Interface**: Handles user interactions, UI rendering, and session management
- **Custom Styling**: Brand-compliant CSS with specific color schemes (#07546B, #F75768, #FB6957)
- **Language Selection**: Multi-language interface with real-time switching capabilities
- **Chat Interface**: Conversational UI for tourism inquiries

### Gemini Client (`utils/gemini_client.py`)
- **AI Integration**: Manages communication with Google Gemini 2.5 Flash model
- **Tourism-Specific Prompting**: Specialized system prompt focused on Anand and Gujarat tourism
- **Knowledge Base**: Pre-configured with local attractions, cultural information, and practical details
- **Error Handling**: Robust exception management for API interactions

### Translation Service (`utils/translator.py`)
- **Multi-Language Support**: Handles English, Hindi, and Telugu translations
- **Google Translate Integration**: Real-time translation capabilities
- **Language Code Mapping**: Efficient language identification and conversion
- **Fallback Mechanisms**: Graceful degradation when translation fails

### Itinerary Generator (`utils/itinerary_generator.py`)
- **Smart Itinerary Creation**: Keyword-triggered, AI-powered travel planning
- **Duration Extraction**: Intelligent parsing of travel duration from user requests
- **Structured Output**: HTML-formatted itineraries with proper styling
- **Local Focus**: Emphasis on Anand and nearby attractions within practical travel distances

## Data Flow

1. **User Input**: Users interact through Streamlit chat interface
2. **Language Processing**: Input is processed and potentially translated to English
3. **AI Query**: Processed query sent to Gemini AI with tourism-specific context
4. **Response Generation**: AI generates contextual response about Anand/Gujarat tourism
5. **Itinerary Detection**: System checks for itinerary-related keywords
6. **Specialized Processing**: If itinerary requested, dedicated generator creates detailed plans
7. **Translation**: Response translated to user's preferred language
8. **UI Rendering**: Final response displayed in chat interface with proper formatting

## External Dependencies

### Required APIs
- **Google Gemini API**: Core AI functionality (requires GEMINI_API_KEY environment variable)
- **Google Translate API**: Multi-language support (via googletrans library)

### Python Libraries
- **streamlit**: Web application framework
- **google-genai**: Google Gemini AI client
- **googletrans**: Translation services
- **pillow**: Image processing capabilities

### Environment Configuration
- **GEMINI_API_KEY**: Required environment variable for API authentication
- **Python 3.8+**: Minimum runtime requirement

## Deployment Strategy

The application is designed for simple deployment with minimal configuration:

**Local Development**: Direct execution via `streamlit run app.py`
**Cloud Deployment**: Compatible with Streamlit Cloud, Replit, and other Python hosting platforms
**Environment Setup**: Single environment variable configuration
**Dependency Management**: Standard pip installation with requirements clearly documented

The architecture supports easy scaling and modification, with modular components that can be independently updated or replaced. The system prioritizes reliability and user experience while maintaining cost-effective operation through efficient API usage and caching strategies.