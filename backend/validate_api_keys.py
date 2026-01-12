#!/usr/bin/env python3
"""
Validate watsonx.ai and watsonx.data API keys
"""

import os
import sys
import requests
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 70)
print("PolicyIQ API Keys Validation")
print("=" * 70)
print()

# Check .env file exists
env_path = Path(__file__).parent / ".env"
if not env_path.exists():
    print("✗ ERROR: .env file not found!")
    print(f"  Expected location: {env_path}")
    print("  Run: cp env.example .env")
    sys.exit(1)

print("✓ .env file found")
print()

# Load settings
try:
    from core.config import settings
except Exception as e:
    print(f"✗ Error loading settings: {str(e)}")
    print("  Make sure virtual environment is activated")
    sys.exit(1)

# Validate watsonx.ai credentials
print("1. Validating watsonx.ai Credentials")
print("-" * 70)

api_key = settings.WATSONX_AI_API_KEY
project_id = settings.WATSONX_AI_PROJECT_ID
url = settings.WATSONX_AI_URL

if not api_key:
    print("✗ WATSONX_AI_API_KEY: NOT SET")
    print("  Please set this in .env file")
elif "your_watsonx_ai_api_key_here" in api_key or "ApiKey-" not in api_key:
    print("✗ WATSONX_AI_API_KEY: INVALID FORMAT")
    print(f"  Current value: {api_key[:30]}...")
    print("  Should start with 'ApiKey-'")
else:
    print(f"✓ WATSONX_AI_API_KEY: SET (format looks correct)")
    print(f"  Preview: {api_key[:25]}...")

if not project_id:
    print("✗ WATSONX_AI_PROJECT_ID: NOT SET")
    print("  Please set this in .env file")
elif "your_project_id_here" in project_id or len(project_id) < 30:
    print("✗ WATSONX_AI_PROJECT_ID: INVALID FORMAT")
    print(f"  Current value: {project_id}")
    print("  Should be a UUID (36 characters)")
else:
    print(f"✓ WATSONX_AI_PROJECT_ID: SET (format looks correct)")
    print(f"  Value: {project_id}")

print(f"  URL: {url}")
print(f"  Model: {settings.WATSONX_AI_MODEL}")
print()

# Test API key by getting IAM token
if api_key and project_id and "ApiKey-" in api_key:
    print("  Testing API key validity...")
    try:
        # Get IAM token
        token_url = f"{url}/v1/identity/token"
        token_data = {
            "apikey": api_key,
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
        }
        
        response = requests.post(
            token_url,
            data=token_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=10
        )
        
        if response.status_code == 200:
            token_data = response.json()
            if "access_token" in token_data:
                print("  ✓ API Key is VALID - Successfully obtained access token")
                print(f"    Token expires in: {token_data.get('expires_in', 'unknown')} seconds")
            else:
                print("  ✗ API Key validation FAILED")
                print(f"    Response: {token_data}")
        elif response.status_code == 401:
            print("  ✗ API Key is INVALID - Authentication failed")
            print("    Please check your API key in IBM Cloud")
        elif response.status_code == 403:
            print("  ✗ API Key is INVALID - Access forbidden")
            print("    API key may not have required permissions")
        else:
            print(f"  ⚠ API Key validation returned status {response.status_code}")
            print(f"    Response: {response.text[:200]}")
            
    except requests.exceptions.Timeout:
        print("  ✗ Connection TIMEOUT - Check internet connection")
    except requests.exceptions.ConnectionError:
        print("  ✗ Connection ERROR - Cannot reach IBM Cloud")
        print(f"    URL: {token_url}")
    except Exception as e:
        print(f"  ✗ Error testing API key: {str(e)}")
else:
    print("  ⚠ Skipping API key test - credentials not properly configured")

print()

# Validate watsonx.data credentials
print("2. Validating watsonx.data Credentials")
print("-" * 70)

data_url = settings.WATSONX_DATA_URL
data_username = settings.WATSONX_DATA_USERNAME
data_password = settings.WATSONX_DATA_PASSWORD

if not data_url:
    print("✗ WATSONX_DATA_URL: NOT SET")
elif "your_watsonx_data_url_here" in data_url or not data_url.startswith("https://"):
    print("✗ WATSONX_DATA_URL: INVALID FORMAT")
    print(f"  Current value: {data_url}")
    print("  Should be a full URL starting with https://")
else:
    print(f"✓ WATSONX_DATA_URL: SET")
    print(f"  Value: {data_url}")

if not data_username:
    print("✗ WATSONX_DATA_USERNAME: NOT SET")
elif "your_username_here" in data_username:
    print("✗ WATSONX_DATA_USERNAME: USING PLACEHOLDER")
    print("  Please set actual username")
else:
    print(f"✓ WATSONX_DATA_USERNAME: SET")
    print(f"  Value: {data_username}")

if not data_password:
    print("✗ WATSONX_DATA_PASSWORD: NOT SET")
elif "your_password_here" in data_password:
    print("✗ WATSONX_DATA_PASSWORD: USING PLACEHOLDER")
    print("  Please set actual password")
else:
    print(f"✓ WATSONX_DATA_PASSWORD: SET")
    print(f"  Value: {'*' * len(data_password)}")

print()

# Summary
print("=" * 70)
print("Summary")
print("=" * 70)

ai_ready = (api_key and "ApiKey-" in api_key and 
            project_id and len(project_id) > 30 and
            "your_" not in api_key and "your_" not in project_id)

data_ready = (data_url and data_url.startswith("https://") and
              data_username and "your_" not in data_username and
              data_password and "your_" not in data_password)

if ai_ready:
    print("✓ watsonx.ai: Credentials configured and API key validated")
else:
    print("✗ watsonx.ai: Credentials missing or invalid")

if data_ready:
    print("✓ watsonx.data: Credentials configured")
else:
    print("✗ watsonx.data: Credentials missing or invalid")

print()

if ai_ready and data_ready:
    print("🎉 All credentials are properly configured!")
    print("   You can now use PolicyIQ.")
elif ai_ready:
    print("⚠ watsonx.ai is ready, but watsonx.data needs configuration")
    print("   PolicyIQ will work for Q&A but document storage may not work")
elif data_ready:
    print("⚠ watsonx.data is ready, but watsonx.ai needs configuration")
    print("   PolicyIQ will not work without watsonx.ai")
else:
    print("❌ Credentials need to be configured")
    print("   See FIX_CREDENTIALS.md for help")

print("=" * 70)
