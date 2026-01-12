#!/usr/bin/env python3
"""
Check if we can determine account information from the API key
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
print("Account & Key Verification")
print("=" * 70)
print()

if not api_key:
    print("✗ No API key found")
    exit(1)

print(f"Testing key: {api_key[:30]}...")
print()

# Test IAM
token_url = "https://iam.cloud.ibm.com/identity/token"

print("Attempting to get IAM token...")
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
    print()
    
    if response.status_code == 200:
        print("✓✓✓ KEY IS VALID! ✓✓✓")
        data = response.json()
        token = data.get("access_token")
        print(f"Got access token: {token[:50]}...")
        
        # Try to get account info
        print("\nAttempting to get account information...")
        try:
            account_url = "https://iam.cloud.ibm.com/v1/apikeys/details"
            headers = {"Authorization": f"Bearer {token}"}
            account_response = requests.get(account_url, headers=headers, timeout=10)
            
            if account_response.status_code == 200:
                account_data = account_response.json()
                print("Account Information:")
                print(f"  Account ID: {account_data.get('account_id', 'N/A')}")
                print(f"  IAM ID: {account_data.get('iam_id', 'N/A')}")
            else:
                print(f"Could not get account info (status: {account_response.status_code})")
        except Exception as e:
            print(f"Could not get account info: {str(e)}")
            
    elif response.status_code == 400:
        error_data = response.json()
        error_msg = error_data.get("errorMessage", "Unknown")
        error_code = error_data.get("errorCode", "N/A")
        
        print("✗✗✗ KEY IS INVALID ✗✗✗")
        print(f"Error Code: {error_code}")
        print(f"Error Message: {error_msg}")
        print()
        print("This means IBM Cloud cannot find this API key.")
        print()
        print("Most likely causes:")
        print("1. Key was created in a DIFFERENT IBM Cloud account")
        print("2. Key was deleted/revoked")
        print("3. You're logged into a different account than where key was created")
        print()
        print("To fix:")
        print("1. Go to: https://cloud.ibm.com/iam/apikeys")
        print("2. Check which account you're logged into (top right corner)")
        print("3. Verify the 'PolicyIQ' key exists in that account")
        print("4. If not, either:")
        print("   a) Log into the account where the key was created, OR")
        print("   b) Create a new key in your current account")
        
    else:
        print(f"✗ Unexpected status: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        
except Exception as e:
    print(f"✗ Error: {str(e)}")
    import traceback
    traceback.print_exc()

print()
print("=" * 70)
