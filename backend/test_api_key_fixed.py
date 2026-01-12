#!/usr/bin/env python3
"""
Fixed API key test - uses correct IAM endpoint
"""

import requests
import sys
import os

# Try to get API key from .env
api_key = None
try:
    with open('.env', 'r') as f:
        for line in f:
            if line.startswith('WATSONX_AI_API_KEY='):
                api_key = line.split('=', 1)[1].strip().strip('"').strip("'")
                break
except:
    pass

# Or use command line argument
if len(sys.argv) > 1:
    api_key = sys.argv[1]

if not api_key:
    print("Usage: python test_api_key_fixed.py [API_KEY]")
    print("Or set WATSONX_AI_API_KEY in .env file")
    sys.exit(1)

print("=" * 60)
print("Testing watsonx.ai API Key")
print("=" * 60)
print(f"API Key: {api_key[:25]}...")
print()

# Use standard IBM Cloud IAM endpoint
token_url = "https://iam.cloud.ibm.com/identity/token"

print(f"Token Endpoint: {token_url}")
print()

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
            print("✓ API Key is VALID!")
            print(f"  Token expires in: {data.get('expires_in', 'unknown')} seconds")
            print(f"  Token type: {data.get('token_type', 'unknown')}")
            print()
            print("✓ Your API key is working correctly!")
            print("  The issue was the token endpoint URL.")
            print("  I've fixed it in the code.")
        else:
            print("✗ Unexpected response format")
            print(f"  Response: {data}")
    elif response.status_code == 401:
        print("✗ API Key is INVALID - Authentication failed (401)")
        print("  Please check your API key in IBM Cloud")
        print("  Make sure it starts with 'ApiKey-'")
    elif response.status_code == 403:
        print("✗ API Key is INVALID - Access forbidden (403)")
        print("  API key may not have required permissions")
    elif response.status_code == 404:
        print("✗ Endpoint not found (404)")
        print("  This shouldn't happen with the IAM endpoint")
        print(f"  URL: {token_url}")
    else:
        print(f"✗ Unexpected status code: {response.status_code}")
        print(f"  Response: {response.text[:200]}")
        
except requests.exceptions.Timeout:
    print("✗ Connection TIMEOUT")
    print("  Check your internet connection")
except requests.exceptions.ConnectionError:
    print("✗ Connection ERROR")
    print(f"  Cannot reach: {token_url}")
    print("  Check your internet connection")
except Exception as e:
    print(f"✗ Error: {str(e)}")

print()
print("=" * 60)
