#!/usr/bin/env python3
"""
Script to check watsonx.ai and watsonx.data credentials
"""

import os
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from core.config import settings
    
    print("=" * 60)
    print("PolicyIQ Credentials Check")
    print("=" * 60)
    print()
    
    # Check watsonx.ai
    print("watsonx.ai Configuration:")
    print(f"  API Key: {'✓ SET' if settings.WATSONX_AI_API_KEY else '✗ NOT SET'}")
    if settings.WATSONX_AI_API_KEY:
        key_preview = settings.WATSONX_AI_API_KEY[:20] + "..." if len(settings.WATSONX_AI_API_KEY) > 20 else settings.WATSONX_AI_API_KEY
        print(f"    Preview: {key_preview}")
    
    print(f"  Project ID: {'✓ SET' if settings.WATSONX_AI_PROJECT_ID else '✗ NOT SET'}")
    if settings.WATSONX_AI_PROJECT_ID:
        print(f"    Value: {settings.WATSONX_AI_PROJECT_ID}")
    
    print(f"  URL: {settings.WATSONX_AI_URL}")
    print(f"  Model: {settings.WATSONX_AI_MODEL}")
    print()
    
    # Check watsonx.data
    print("watsonx.data Configuration:")
    print(f"  URL: {'✓ SET' if settings.WATSONX_DATA_URL else '✗ NOT SET'}")
    if settings.WATSONX_DATA_URL:
        print(f"    Value: {settings.WATSONX_DATA_URL}")
    
    print(f"  Username: {'✓ SET' if settings.WATSONX_DATA_USERNAME else '✗ NOT SET'}")
    print(f"  Password: {'✓ SET' if settings.WATSONX_DATA_PASSWORD else '✗ NOT SET'}")
    print(f"  Database: {settings.WATSONX_DATA_DATABASE}")
    print()
    
    # Summary
    print("=" * 60)
    ai_ready = settings.WATSONX_AI_API_KEY and settings.WATSONX_AI_PROJECT_ID
    data_ready = settings.WATSONX_DATA_URL and settings.WATSONX_DATA_USERNAME and settings.WATSONX_DATA_PASSWORD
    
    if ai_ready and data_ready:
        print("✓ All credentials are configured!")
    elif ai_ready:
        print("⚠ watsonx.ai is configured, but watsonx.data is missing")
    elif data_ready:
        print("⚠ watsonx.data is configured, but watsonx.ai is missing")
    else:
        print("✗ Missing credentials. Please configure .env file")
    print("=" * 60)
    
    # Test client initialization
    if ai_ready:
        print()
        print("Testing watsonx.ai client initialization...")
        try:
            from services.watsonx_ai.client import WatsonxAIClient
            client = WatsonxAIClient()
            if client.client:
                print("✓ watsonx.ai client initialized successfully")
            else:
                print("✗ watsonx.ai client failed to initialize")
        except Exception as e:
            print(f"✗ Error initializing client: {str(e)}")
    
except Exception as e:
    print(f"Error: {str(e)}")
    print("\nMake sure you're running this from the backend directory")
    print("and that the virtual environment is activated.")
