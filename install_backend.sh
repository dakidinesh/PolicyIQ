#!/bin/bash
# Backend Installation Script

echo "Installing PolicyIQ Backend..."
cd backend

# Create venv
python3 -m venv venv || python -m venv venv

# Activate and install
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create directories
mkdir -p uploads

echo "✓ Backend installation complete!"
echo "To activate: source venv/bin/activate"
