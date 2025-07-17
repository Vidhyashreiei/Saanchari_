#!/bin/bash

# Update pip
python -m pip install --upgrade pip

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
echo "Verifying installations..."
python -c "import streamlit as st; print(f'Streamlit version: {st.__version__}')"
python -c "from PIL import Image; print(f'Pillow version: {Image.__version__}')"
