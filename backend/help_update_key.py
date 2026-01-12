#!/usr/bin/env python3
"""
Interactive script to help update API key
"""

from pathlib import Path
import sys

env_path = Path(__file__).parent / ".env"

print("=" * 70)
print("Update API Key Helper")
print("=" * 70)
print()

if not env_path.exists():
    print("✗ .env file not found!")
    print("  Run: cp env.example .env")
    sys.exit(1)

# Show current key
print("Current API key in .env:")
with open(env_path, 'r') as f:
    for line in f:
        if line.startswith('WATSONX_AI_API_KEY='):
            current = line.split('=', 1)[1].strip().strip('"').strip("'")
            print(f"  {current[:40]}...")
            break

print()
print("From your IBM Cloud screenshot, I can see:")
print("  - You have a 'PolicyIQ' API key")
print("  - There's also a CPD API key (for Watson Studio)")
print()
print("To update your .env file:")
print()
print("1. In IBM Cloud, click on the 'PolicyIQ' API key row")
print("2. In the popup, find the 'ID' field")
print("3. Click 'Copy ID to clipboard' button")
print("4. The key will look like: ApiKey-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
print()
print("5. Then run this command (replace YOUR-KEY with the copied key):")
print()
print("   cd /Users/dakidinesh/Documents/PolicyIQ/backend")
print("   sed -i '' 's|^WATSONX_AI_API_KEY=.*|WATSONX_AI_API_KEY=YOUR-KEY-HERE|' .env")
print()
print("6. Or edit manually:")
print("   nano .env")
print("   # Find WATSONX_AI_API_KEY=... and replace with your new key")
print()
print("7. Verify with:")
print("   python verify_api_key.py")
print()
print("=" * 70)
