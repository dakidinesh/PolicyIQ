#!/usr/bin/env python3
"""
Interactive script to update API key in .env file
"""

from pathlib import Path
import re

env_path = Path(__file__).parent / ".env"

if not env_path.exists():
    print("✗ .env file not found!")
    exit(1)

print("=" * 70)
print("Update API Key in .env")
print("=" * 70)
print()

# Show current key
print("Current API key in .env:")
with open(env_path, 'r') as f:
    for line in f:
        if line.startswith('WATSONX_AI_API_KEY='):
            current = line.split('=', 1)[1].strip().strip('"').strip("'")
            print(f"  {current}")
            break

print()
print("Please paste your NEW API key below.")
print("It should start with 'ApiKey-' and be about 40-50 characters long.")
print()
new_key = input("Paste new API key: ").strip()

# Remove any quotes or spaces
new_key = new_key.strip('"').strip("'").strip()

# Validate
if not new_key.startswith('ApiKey-'):
    print()
    print("✗ Error: API key must start with 'ApiKey-'")
    print(f"  You entered: {new_key[:30]}...")
    exit(1)

# Read all lines
with open(env_path, 'r') as f:
    lines = f.readlines()

# Update the key
updated = False
new_lines = []
for line in lines:
    if line.startswith('WATSONX_AI_API_KEY='):
        new_lines.append(f"WATSONX_AI_API_KEY={new_key}\n")
        updated = True
    else:
        new_lines.append(line)

# Write back
if updated:
    with open(env_path, 'w') as f:
        f.writelines(new_lines)
    print()
    print("✓ API key updated in .env file!")
    print()
    print("New key:")
    print(f"  {new_key}")
    print()
    print("Now testing the key...")
    print()
else:
    print("✗ Could not find WATSONX_AI_API_KEY in .env")
    exit(1)

# Test the key
import requests
try:
    token_url = "https://iam.cloud.ibm.com/identity/token"
    response = requests.post(
        token_url,
        data={
            "apikey": new_key,
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=10
    )
    
    if response.status_code == 200:
        print("✓✓✓ API KEY IS VALID! ✓✓✓")
        print()
        print("Your API key is working correctly!")
        print("You can now use PolicyIQ.")
    else:
        print(f"✗ API key test failed (status: {response.status_code})")
        error = response.json().get("errorMessage", "Unknown error")
        print(f"  Error: {error}")
except Exception as e:
    print(f"✗ Error testing key: {str(e)}")

print()
print("=" * 70)
