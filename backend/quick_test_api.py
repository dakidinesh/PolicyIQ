#!/usr/bin/env python3
"""
Quick test to validate watsonx.ai API key
Run: python quick_test_api.py
"""

import requests
import sys

# Get API key from command line or use default
if len(sys.argv) > 1:
    api_key = sys.argv[1]
else:
    # Try to read from .env
    try:
        with open('.env', 'r') as f:
            for line in f:
                if line.startswith('WATSONX_AI_API_KEY='):
                    api_key = line.split('=', 1)[1].strip().strip('"').strip("'")
                    break
    except:
        print("Usage: python quick_test_api.py [API_KEY]")
        print("Or set WATSONX_AI_API_KEY in .env file")
        sys.exit(1)

# Try different token endpoint URLs
urls_to_try = [
    "https://iam.cloud.ibm.com/identity/token",  # Standard IAM endpoint
    "https://us-south.ml.cloud.ibm.com/v1/identity/token",  # Regional endpoint
    "https://iam.cloud.ibm.com/oidc/token",  # Alternative endpoint
]

url = urls_to_try[0]  # Start with standard IAM endpoint

print("Testing watsonx.ai API key...")
print(f"API Key: {api_key[:25]}...")
print()

# Try standard IAM endpoint first
url = "https://iam.cloud.ibm.com/identity/token"

try:
    response = requests.post(
        url,
        data={
            "apikey": api_key,
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=10
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if "access_token" in data:
            print("✓ API Key is VALID!")
            print(f"  Token expires in: {data.get('expires_in', 'unknown')} seconds")
            print(f"  Token type: {data.get('token_type', 'unknown')}")
        else:
            print("✗ Unexpected response format")
            print(f"  Response: {data}")
    elif response.status_code == 401:
        print("✗ API Key is INVALID - Authentication failed")
        print("  Please check your API key in IBM Cloud")
    elif response.status_code == 403:
        print("✗ API Key is INVALID - Access forbidden")
        print("  API key may not have required permissions")
    else:
        print(f"✗ Unexpected status code: {response.status_code}")
        print(f"  Response: {response.text[:200]}")
        
except requests.exceptions.Timeout:
    print("✗ Connection TIMEOUT")
    print("  Check your internet connection")
except requests.exceptions.ConnectionError:
    print("✗ Connection ERROR")
    print(f"  Cannot reach: {url}")
except Exception as e:
    print(f"✗ Error: {str(e)}")
