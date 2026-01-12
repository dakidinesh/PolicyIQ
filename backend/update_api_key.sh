#!/bin/bash

# Script to update API key in .env file

echo "=========================================="
echo "Update API Key"
echo "=========================================="
echo ""
echo "Current API key in .env:"
grep "^WATSONX_AI_API_KEY=" .env | head -1
echo ""
echo "Please paste your NEW API key below."
echo "It should start with 'ApiKey-' and be about 40-50 characters long."
echo ""
echo -n "Enter new API key: "
read NEW_KEY

# Remove any quotes or spaces
NEW_KEY=$(echo "$NEW_KEY" | tr -d '"' | tr -d "'" | xargs)

# Validate format
if [[ ! "$NEW_KEY" =~ ^ApiKey- ]]; then
    echo ""
    echo "✗ Error: API key must start with 'ApiKey-'"
    echo "  You entered: $NEW_KEY"
    exit 1
fi

# Update .env file
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' "s|^WATSONX_AI_API_KEY=.*|WATSONX_AI_API_KEY=$NEW_KEY|" .env
else
    # Linux
    sed -i "s|^WATSONX_AI_API_KEY=.*|WATSONX_AI_API_KEY=$NEW_KEY|" .env
fi

echo ""
echo "✓ API key updated!"
echo ""
echo "New API key in .env:"
grep "^WATSONX_AI_API_KEY=" .env | head -1
echo ""
echo "Verifying..."
echo ""

# Activate venv and verify
if [ -d "venv" ]; then
    source venv/bin/activate
    python verify_api_key.py
else
    echo "⚠ venv not found. Please verify manually:"
    echo "   python verify_api_key.py"
fi
