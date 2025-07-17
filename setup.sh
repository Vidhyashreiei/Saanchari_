#!/bin/bash

# Install required packages
pip install -r requirements.txt

# Create necessary directories
mkdir -p ~/.streamlit/

# Create streamlit config
cat > ~/.streamlit/config.toml << EOL
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true

[browser]
serverAddress = "0.0.0.0"
serverPort = 8501
EOL

# Set execute permissions
chmod +x setup.sh
