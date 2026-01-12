#!/usr/bin/env python3
"""
Direct test of API key with detailed output
"""

import requests
from pathlib import Path

env_path = Path(__file__).parent / ".env"

# Read key
api_key = None
with open(env_path, 'r') as f:
    for line in f:
        if line.startswith('WATSONX_AI_API_KEY='):
            api_key = line.split('=', 1)[1].strip().strip('"').strip("'")
            break

print("=" * 70)
print("Direct API Key Test")
print("=" * 70)
print()
print(f"Key: {api_key}")
print(f"Length: {len(api_key)}")
print(f"Starts with ApiKey-: {api_key.startswith('ApiKey-')}")
print()

# Test IAM
print("Testing IAM token endpoint...")
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
    print(f"Response Headers: {dict(response.headers)}")
    print()
    
    if response.status_code == 200:
        data = response.json()
        print("✓✓✓ SUCCESS! Key is valid! ✓✓✓")
        print(f"Access Token: {data.get('access_token', '')[:50]}...")
        print(f"Token Type: {data.get('token_type', '')}")
        print(f"Expires In: {data.get('expires_in', '')} seconds")
    else:
        print("✗ Key validation failed")
        print(f"Response: {response.text}")
        
        # Try to parse error
        try:
            error_data = response.json()
            print(f"Error Message: {error_data.get('errorMessage', 'N/A')}")
            print(f"Error Code: {error_data.get('errorCode', 'N/A')}")
        except:
            print("Could not parse error response")
            
except Exception as e:
    print(f"✗ Exception: {str(e)}")
    import traceback
    traceback.print_exc()

print()
print("=" * 70)
print()
print("If the key is still invalid, check:")
print("1. Are you logged into the correct IBM Cloud account?")
print("2. Was the key created in the same account?")
print("3. Is the key enabled in IBM Cloud console?")
print("4. Try creating the key from IAM instead: https://cloud.ibm.com/iam/apikeys")
