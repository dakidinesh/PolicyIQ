#!/usr/bin/env python3
"""
Verify API key is valid and properly configured
"""

import sys
from pathlib import Path
import requests

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 70)
print("API Key Verification")
print("=" * 70)
print()

# Read from .env
env_path = Path(__file__).parent / ".env"
if not env_path.exists():
    print("✗ .env file not found!")
    sys.exit(1)

api_key = None
with open(env_path, 'r') as f:
    for line in f:
        if line.startswith('WATSONX_AI_API_KEY='):
            api_key = line.split('=', 1)[1].strip().strip('"').strip("'")
            break

if not api_key:
    print("✗ WATSONX_AI_API_KEY not found in .env")
    sys.exit(1)

print(f"API Key from .env:")
print(f"  Full key: {api_key}")
print(f"  Length: {len(api_key)} characters")
print(f"  Format: {'✓ Correct' if api_key.startswith('ApiKey-') else '✗ Wrong (should start with ApiKey-)'}")
print()

# Test the key
print("Testing API key validity...")
token_url = "https://iam.cloud.ibm.com/identity/token"

try:
    response = requests.post(
        token_url,
        data={
            "apikey": api_key,
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=10
    )
    
    print(f"Status Code: {response.status_code}")
    print()
    
    if response.status_code == 200:
        data = response.json()
        if "access_token" in data:
            print("✓✓✓ API KEY IS VALID! ✓✓✓")
            print(f"  Token expires in: {data.get('expires_in', 'unknown')} seconds")
            print()
            print("Your API key is working correctly!")
            print("You can now use PolicyIQ.")
        else:
            print("✗ Unexpected response format")
            print(f"  Response: {data}")
    elif response.status_code == 400:
        error_data = response.json()
        error_msg = error_data.get("errorMessage", "Unknown error")
        print("✗✗✗ API KEY IS INVALID ✗✗✗")
        print(f"  Error: {error_msg}")
        print()
        print("The API key in your .env file is not valid.")
        print()
        print("To fix this:")
        print("1. Go to: https://cloud.ibm.com/iam/apikeys")
        print("2. Create a new API key or find an existing valid one")
        print("3. Copy the ENTIRE key (it will start with 'ApiKey-')")
        print("4. Update backend/.env file:")
        print("   WATSONX_AI_API_KEY=ApiKey-YOUR-ACTUAL-KEY-HERE")
        print("5. Make sure there are no extra spaces or quotes")
        print("6. Restart the backend server")
    elif response.status_code == 401:
        print("✗ API Key authentication failed (401)")
    elif response.status_code == 403:
        print("✗ API Key access forbidden (403)")
    else:
        print(f"✗ Unexpected status: {response.status_code}")
        print(f"  Response: {response.text[:200]}")
        
except requests.exceptions.Timeout:
    print("✗ Connection timeout")
except requests.exceptions.ConnectionError:
    print("✗ Connection error - check internet")
except Exception as e:
    print(f"✗ Error: {str(e)}")

print()
print("=" * 70)
