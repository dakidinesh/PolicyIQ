#!/usr/bin/env python3
"""
Quick test script to check watsonx.ai credentials
Run this from the backend directory with venv activated
"""

import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("PolicyIQ Credentials Diagnostic")
print("=" * 60)
print()

# Check .env file
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    print("✓ .env file found")
    print(f"  Location: {env_path}")
    
    # Read and check values
    with open(env_path, 'r') as f:
        content = f.read()
        
    api_key_set = "WATSONX_AI_API_KEY=" in content and "your_watsonx_ai_api_key_here" not in content
    project_id_set = "WATSONX_AI_PROJECT_ID=" in content and "your_project_id_here" not in content
    
    print(f"  API Key: {'✓ SET' if api_key_set else '✗ NOT SET or using placeholder'}")
    print(f"  Project ID: {'✓ SET' if project_id_set else '✗ NOT SET or using placeholder'}")
else:
    print("✗ .env file NOT FOUND")
    print(f"  Expected location: {env_path}")
    print("  Run: cp env.example .env")

print()

# Try to load settings
try:
    from core.config import settings
    
    print("Configuration loaded:")
    print(f"  API Key: {'✓ SET' if settings.WATSONX_AI_API_KEY else '✗ NOT SET'}")
    if settings.WATSONX_AI_API_KEY:
        preview = settings.WATSONX_AI_API_KEY[:25] + "..." if len(settings.WATSONX_AI_API_KEY) > 25 else settings.WATSONX_AI_API_KEY
        print(f"    Preview: {preview}")
    
    print(f"  Project ID: {'✓ SET' if settings.WATSONX_AI_PROJECT_ID else '✗ NOT SET'}")
    if settings.WATSONX_AI_PROJECT_ID:
        print(f"    Value: {settings.WATSONX_AI_PROJECT_ID}")
    
    print(f"  URL: {settings.WATSONX_AI_URL}")
    print(f"  Model: {settings.WATSONX_AI_MODEL}")
    print()
    
    # Try to initialize client
    if settings.WATSONX_AI_API_KEY and settings.WATSONX_AI_PROJECT_ID:
        print("Testing client initialization...")
        try:
            from services.watsonx_ai.client import WatsonxAIClient
            client = WatsonxAIClient()
            
            if client.client:
                print("✓ watsonx.ai client initialized successfully!")
            else:
                print("✗ watsonx.ai client failed to initialize")
                print("  Possible causes:")
                print("    - Invalid API key")
                print("    - Invalid Project ID")
                print("    - Network connectivity issues")
                print("    - Check backend server logs for detailed error")
        except Exception as e:
            print(f"✗ Error initializing client: {str(e)}")
    else:
        print("⚠ Cannot test client - credentials missing")
        
except Exception as e:
    print(f"✗ Error loading configuration: {str(e)}")
    print("  Make sure you're in the backend directory")
    print("  and virtual environment is activated")

print()
print("=" * 60)
