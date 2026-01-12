#!/usr/bin/env python3
"""
Simple API key test - just test IAM token
"""

import sys
from pathlib import Path
import requests

env_path = Path(__file__).parent / ".env"

print("=" * 70)
print("Simple API Key Test")
print("=" * 70)
print()

# Read key from .env
api_key = None
if env_path.exists():
    with open(env_path, 'r') as f:
        for line in f:
            if line.startswith('WATSONX_AI_API_KEY='):
                api_key = line.split('=', 1)[1].strip().strip('"').strip("'")
                break

if not api_key:
    print("✗ No API key found in .env")
    sys.exit(1)

print(f"Testing key: {api_key[:30]}...")
print()

# Test IAM
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
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        print("✓✓✓ KEY IS VALID! ✓✓✓")
        token = response.json().get("access_token")
        print(f"Got access token: {token[:30]}...")
    elif response.status_code == 400:
        error = response.json().get("errorMessage", "Unknown")
        print(f"✗✗✗ KEY IS INVALID ✗✗✗")
        print(f"Error: {error}")
        print()
        print("This means the API key doesn't exist in IBM Cloud.")
        print()
        print("Possible reasons:")
        print("1. Key was deleted/revoked")
        print("2. Key is from a different IBM Cloud account")
        print("3. Key was copied incorrectly")
        print()
        print("Solution:")
        print("1. Go to: https://cloud.ibm.com/iam/apikeys")
        print("2. Check if 'PolicyIQ' key exists and is enabled")
        print("3. If not, create a NEW API key")
        print("4. Copy the ENTIRE key (starts with ApiKey-)")
        print("5. Update .env file")
    else:
        print(f"✗ Unexpected status: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        
except Exception as e:
    print(f"✗ Error: {str(e)}")

print()
print("=" * 70)
