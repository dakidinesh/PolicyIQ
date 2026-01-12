#!/usr/bin/env python3
"""
Fix .env file formatting issues
"""

from pathlib import Path
import re

env_path = Path(__file__).parent / ".env"

if not env_path.exists():
    print("✗ .env file not found!")
    exit(1)

# Read current content
with open(env_path, 'r') as f:
    lines = f.readlines()

# Fix API key line
fixed = False
new_lines = []
for line in lines:
    if line.startswith('WATSONX_AI_API_KEY='):
        # Extract the key value
        parts = line.split('=', 1)
        if len(parts) == 2:
            key_value = parts[1].strip()
            # Remove quotes if present
            key_value = key_value.strip('"').strip("'").strip()
            # Remove any trailing whitespace
            key_value = key_value.rstrip()
            # Reconstruct line
            new_line = f"WATSONX_AI_API_KEY={key_value}\n"
            if new_line != line:
                print(f"Fixed line:")
                print(f"  Old: {line.rstrip()}")
                print(f"  New: {new_line.rstrip()}")
                fixed = True
            new_lines.append(new_line)
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

# Write back if fixed
if fixed:
    with open(env_path, 'w') as f:
        f.writelines(new_lines)
    print("\n✓ .env file fixed!")
else:
    print("✓ .env file format looks correct")

# Show current value
print("\nCurrent API key value:")
for line in new_lines:
    if 'WATSONX_AI_API_KEY' in line:
        key = line.split('=', 1)[1].strip().strip('"').strip("'")
        print(f"  {key}")
        print(f"  Length: {len(key)}")
        print(f"  Starts with ApiKey-: {key.startswith('ApiKey-')}")
        break
