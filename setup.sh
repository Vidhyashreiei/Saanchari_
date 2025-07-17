#!/bin/bash

# Update pip
python -m pip install --upgrade pip

# Install specific version of setuptools
pip install setuptools==65.5.0

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

# Verify installations
echo "=== Verifying installations ==="
python --version
pip list | grep -E "streamlit|pillow|google-generativeai"

echo "=== Starting Streamlit server ==="
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
