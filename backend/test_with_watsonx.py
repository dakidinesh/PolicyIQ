#!/usr/bin/env python3
"""
Test API key with watsonx.ai directly (not just IAM)
"""

import sys
from pathlib import Path
import requests
from dotenv import load_dotenv
import os

env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

api_key = os.getenv("WATSONX_AI_API_KEY", "")
project_id = os.getenv("WATSONX_AI_PROJECT_ID", "")
url = os.getenv("WATSONX_AI_URL", "https://us-south.ml.cloud.ibm.com")

print("=" * 70)
print("Testing API Key with watsonx.ai")
print("=" * 70)
print()
print(f"API Key: {api_key[:30]}...")
print(f"Project ID: {project_id}")
print(f"URL: {url}")
print()

# Step 1: Get IAM token
print("Step 1: Getting IAM token...")
token_url = "https://iam.cloud.ibm.com/identity/token"

try:
    token_response = requests.post(
        token_url,
        data={
            "apikey": api_key,
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=10
    )
    
    print(f"  Status: {token_response.status_code}")
    
    if token_response.status_code != 200:
        error_data = token_response.json() if token_response.content else {}
        error_msg = error_data.get("errorMessage", token_response.text[:100])
        print(f"  ✗ Failed: {error_msg}")
        print()
        print("IAM token generation failed. Key is invalid.")
        sys.exit(1)
    
    token = token_response.json().get("access_token")
    if not token:
        print("  ✗ No access token in response")
        sys.exit(1)
    
    print(f"  ✓ Got access token: {token[:50]}...")
    print()
    
    # Step 2: Test with watsonx.ai
    print("Step 2: Testing with watsonx.ai API...")
    
    base_url = url.rstrip('/')
    if "/ml/v1" not in base_url:
        base_url += "/ml/v1"
    
    api_url = f"{base_url}/text/generation?version=2023-05-29"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model_id": "meta-llama/llama-3-70b-instruct",
        "input": "Hello, this is a test.",
        "parameters": {"max_new_tokens": 10},
        "project_id": project_id
    }
    
    print(f"  Testing endpoint: {api_url}")
    print(f"  Project ID: {project_id}")
    print()
    
    api_response = requests.post(api_url, json=payload, headers=headers, timeout=30)
    
    print(f"  Status: {api_response.status_code}")
    
    if api_response.status_code == 200:
        print()
        print("✓✓✓ SUCCESS! API KEY WORKS WITH WATSONX.AI! ✓✓✓")
        result = api_response.json()
        print(f"Response: {result}")
    elif api_response.status_code == 400:
        error_data = api_response.json() if api_response.content else {}
        error_msg = error_data.get("errorMessage", api_response.text[:200])
        print(f"  ✗ Bad request: {error_msg}")
        if "project" in error_msg.lower():
            print("  → Project ID might be incorrect")
    elif api_response.status_code == 401:
        print("  ✗ Unauthorized - Token might be invalid")
    elif api_response.status_code == 403:
        print("  ✗ Forbidden - API key might not have watsonx.ai permissions")
    else:
        print(f"  ✗ Error: {api_response.text[:200]}")
        
except requests.exceptions.Timeout:
    print("  ✗ Connection timeout")
except requests.exceptions.ConnectionError:
    print("  ✗ Connection error")
except Exception as e:
    print(f"  ✗ Exception: {str(e)}")
    import traceback
    traceback.print_exc()

print()
print("=" * 70)
