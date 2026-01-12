#!/usr/bin/env python3
"""
Comprehensive diagnostic for API keys
Tests both keys and checks all configuration
"""

import os
import sys
from pathlib import Path
import requests
from dotenv import load_dotenv

# Load .env
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

print("=" * 70)
print("COMPREHENSIVE API KEY DIAGNOSTIC")
print("=" * 70)
print()

# Get configuration
current_key = os.getenv("WATSONX_AI_API_KEY", "")
project_id = os.getenv("WATSONX_AI_PROJECT_ID", "")
url = os.getenv("WATSONX_AI_URL", "https://us-south.ml.cloud.ibm.com")

print("Current Configuration:")
print(f"  API Key: {current_key[:30]}... (length: {len(current_key)})")
print(f"  Project ID: {project_id}")
print(f"  URL: {url}")
print()

def test_iam_token(api_key):
    """Test if API key can get IAM token"""
    print("Testing IAM Token Generation...")
    try:
        token_url = "https://iam.cloud.ibm.com/identity/token"
        response = requests.post(
            token_url,
            data={
                "apikey": api_key,
                "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=10
        )
        
        if response.status_code == 200:
            token = response.json().get("access_token")
            print(f"  ✓ Got IAM token (status: {response.status_code})")
            return token, True
        else:
            error_data = response.json() if response.content else {}
            error_msg = error_data.get("errorMessage", response.text[:100])
            print(f"  ✗ Failed to get IAM token (status: {response.status_code})")
            print(f"    Error: {error_msg}")
            return None, False
    except Exception as e:
        print(f"  ✗ Exception: {str(e)}")
        return None, False

def test_watsonx_access(token, project_id, region="us-south"):
    """Test if token can access watsonx.ai"""
    print(f"\nTesting watsonx.ai Access (region: {region})...")
    
    base_urls = {
        "us-south": "https://us-south.ml.cloud.ibm.com",
        "eu-de": "https://eu-de.ml.cloud.ibm.com",
        "eu-gb": "https://eu-gb.ml.cloud.ibm.com"
    }
    
    base_url = base_urls.get(region, base_urls["us-south"])
    
    # Test 1: List models
    print("  Test 1: Listing available models...")
    try:
        models_url = f"{base_url}/ml/v1/foundation_model_predictions?version=2023-05-29"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Simple test - try to get model info
        test_url = f"{base_url}/ml/v1/text/generation?version=2023-05-29"
        payload = {
            "model_id": "meta-llama/llama-3-70b-instruct",
            "input": "test",
            "parameters": {"max_new_tokens": 5},
            "project_id": project_id
        }
        
        response = requests.post(test_url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f"    ✓✓✓ SUCCESS! API key works with watsonx.ai! ✓✓✓")
            return True
        elif response.status_code == 400:
            error_data = response.json() if response.content else {}
            error_msg = error_data.get("errorMessage", response.text[:200])
            print(f"    ✗ Bad request (400): {error_msg}")
            if "project" in error_msg.lower():
                print(f"      → Project ID might be wrong: {project_id}")
        elif response.status_code == 401:
            print(f"    ✗ Unauthorized (401) - Token might be invalid or expired")
        elif response.status_code == 403:
            print(f"    ✗ Forbidden (403) - API key might not have watsonx.ai permissions")
            print(f"      → Check if API key is associated with watsonx.ai service")
        elif response.status_code == 404:
            print(f"    ✗ Not found (404) - Project or endpoint not found")
            print(f"      → Check project ID: {project_id}")
        else:
            print(f"    ✗ Status {response.status_code}: {response.text[:200]}")
        
        return False
        
    except Exception as e:
        print(f"    ✗ Exception: {str(e)}")
        return False

# Test current key
print("\n" + "="*70)
print("TESTING CURRENT KEY FROM .ENV")
print("="*70)
print()

if not current_key:
    print("✗ No API key found in .env")
else:
    token, token_ok = test_iam_token(current_key)
    if token_ok and token:
        test_watsonx_access(token, project_id, "us-south")

# Interactive testing
print("\n" + "="*70)
print("INTERACTIVE KEY TESTING")
print("="*70)
print()
print("You can test additional keys here.")
print("From IBM Cloud, copy the API key ID and paste it below.")
print()

# Test PolicyIQ key
print("PolicyIQ API Key Test:")
print("1. Go to: https://cloud.ibm.com/iam/apikeys")
print("2. Click on 'PolicyIQ' row")
print("3. Copy the ID (starts with ApiKey-)")
print()
policyiq_key = input("Paste PolicyIQ key (or Enter to skip): ").strip()

if policyiq_key:
    print("\n" + "-"*70)
    print("Testing PolicyIQ Key")
    print("-"*70)
    token, token_ok = test_iam_token(policyiq_key)
    if token_ok and token:
        success = test_watsonx_access(token, project_id, "us-south")
        if success:
            print("\n" + "="*70)
            print("✓✓✓ USE THIS KEY! Update your .env file with:")
            print(f"WATSONX_AI_API_KEY={policyiq_key}")
            print("="*70)

# Test CPD key
print("\n" + "="*70)
print("CPD API Key Test (for comparison):")
cpd_key = input("Paste CPD key (or Enter to skip): ").strip()

if cpd_key:
    print("\n" + "-"*70)
    print("Testing CPD Key")
    print("-"*70)
    token, token_ok = test_iam_token(cpd_key)
    if token_ok and token:
        test_watsonx_access(token, project_id, "us-south")

# Summary
print("\n" + "="*70)
print("DIAGNOSTIC SUMMARY")
print("="*70)
print()
print("Common Issues:")
print("1. API key not associated with watsonx.ai service")
print("   → Solution: Create API key from watsonx.ai service page")
print()
print("2. Wrong project ID")
print("   → Solution: Get project ID from watsonx.ai project settings")
print()
print("3. API key doesn't have required permissions")
print("   → Solution: Check IAM policies for the API key")
print()
print("4. Wrong region")
print("   → Solution: Make sure URL matches your watsonx.ai region")
print()
print("Next Steps:")
print("1. If a key works, update .env: WATSONX_AI_API_KEY=<working-key>")
print("2. Verify project ID is correct")
print("3. Restart backend server")
print("="*70)
