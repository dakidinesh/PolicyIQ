#!/usr/bin/env python3
"""
Test API key provided by user
"""

import sys
import requests

if len(sys.argv) < 2:
    print("Usage: python test_key_from_user.py <API_KEY>")
    sys.exit(1)

api_key = sys.argv[1].strip().strip('"').strip("'")

print("=" * 70)
print("Testing API Key")
print("=" * 70)
print()
print(f"Key: {api_key[:30]}...")
print(f"Length: {len(api_key)} characters")
print(f"Starts with ApiKey-: {api_key.startswith('ApiKey-')}")
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
    
    print(f"Status Code: {response.status_code}")
    print()
    
    if response.status_code == 200:
        print("✓✓✓ KEY IS VALID! ✓✓✓")
        data = response.json()
        token = data.get("access_token")
        print(f"Access Token: {token[:50]}...")
        print(f"Token expires in: {data.get('expires_in', 'N/A')} seconds")
        print()
        print("Your API key is working! I'll update .env with this key.")
    else:
        print("✗✗✗ KEY IS INVALID ✗✗✗")
        error_data = response.json()
        error_msg = error_data.get("errorMessage", "Unknown")
        print(f"Error: {error_msg}")
        print()
        if response.status_code == 400:
            print("This means IBM Cloud cannot find this API key.")
            print("Possible reasons:")
            print("1. Key was copied incorrectly (missing characters)")
            print("2. Key is from a different account")
            print("3. Key was deleted/revoked")
        
except Exception as e:
    print(f"✗ Error: {str(e)}")

print()
print("=" * 70)
