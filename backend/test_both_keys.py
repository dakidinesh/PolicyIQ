#!/usr/bin/env python3
"""
Test both API keys to see which one works
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
print("Testing API Keys")
print("=" * 70)
print()

# Get current key from .env
current_key = os.getenv("WATSONX_AI_API_KEY", "")
project_id = os.getenv("WATSONX_AI_PROJECT_ID", "")

print(f"Current key in .env: {current_key[:30]}...")
print(f"Project ID: {project_id}")
print()

# Test function
def test_key(api_key, key_name):
    print(f"\n{'='*70}")
    print(f"Testing: {key_name}")
    print(f"Key: {api_key[:30]}...")
    print(f"{'='*70}")
    
    try:
        # Get IAM token
        token_url = "https://iam.cloud.ibm.com/identity/token"
        token_data = {
            "apikey": api_key,
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
        }
        
        print("Step 1: Getting IAM token...")
        token_response = requests.post(
            token_url,
            data=token_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=10
        )
        
        print(f"  Status: {token_response.status_code}")
        
        if token_response.status_code != 200:
            error_text = token_response.text
            print(f"  ✗ Failed to get token")
            print(f"  Response: {error_text[:200]}")
            return False
        
        token = token_response.json().get("access_token")
        if not token:
            print("  ✗ No access token in response")
            return False
        
        print("  ✓ Got access token")
        
        # Test with watsonx.ai API
        print("\nStep 2: Testing with watsonx.ai API...")
        
        # Try different endpoints
        base_urls = [
            "https://us-south.ml.cloud.ibm.com",
            "https://eu-de.ml.cloud.ibm.com",
            "https://eu-gb.ml.cloud.ibm.com"
        ]
        
        for base_url in base_urls:
            api_url = f"{base_url}/ml/v1/text/generation?version=2023-05-29"
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model_id": "meta-llama/llama-3-70b-instruct",
                "input": "Hello",
                "parameters": {"max_new_tokens": 10},
                "project_id": project_id
            }
            
            try:
                print(f"  Trying: {base_url}")
                api_response = requests.post(
                    api_url,
                    json=payload,
                    headers=headers,
                    timeout=10
                )
                
                print(f"    Status: {api_response.status_code}")
                
                if api_response.status_code == 200:
                    print(f"    ✓✓✓ SUCCESS! This key works! ✓✓✓")
                    print(f"    Region: {base_url}")
                    return True
                elif api_response.status_code == 401:
                    print(f"    ✗ Unauthorized (wrong key or permissions)")
                elif api_response.status_code == 404:
                    print(f"    ✗ Not found (wrong endpoint or project)")
                else:
                    error_text = api_response.text[:200]
                    print(f"    ✗ Error: {error_text}")
                    
            except Exception as e:
                print(f"    ✗ Exception: {str(e)[:100]}")
        
        return False
        
    except Exception as e:
        print(f"  ✗ Exception: {str(e)}")
        return False

# Test current key
if current_key:
    test_key(current_key, "Current Key from .env")

# Ask for PolicyIQ key
print("\n" + "="*70)
print("Please provide the PolicyIQ API key to test")
print("="*70)
print("From IBM Cloud:")
print("1. Go to: https://cloud.ibm.com/iam/apikeys")
print("2. Click on the 'PolicyIQ' row")
print("3. Copy the ID (starts with ApiKey-)")
print()
policyiq_key = input("Paste PolicyIQ API key (or press Enter to skip): ").strip()

if policyiq_key:
    test_key(policyiq_key, "PolicyIQ Key")

# Ask for CPD key
print("\n" + "="*70)
print("Please provide the CPD API key to test")
print("="*70)
cpd_key = input("Paste CPD API key (or press Enter to skip): ").strip()

if cpd_key:
    test_key(cpd_key, "CPD Key")

print("\n" + "="*70)
print("Testing Complete")
print("="*70)
