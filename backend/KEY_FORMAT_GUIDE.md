# How to Get the Correct API Key

## Important Distinction

In IBM Cloud API keys page, there are **TWO different identifiers**:

1. **Table ID** (what you see in the list):
   - Short identifier like: `cpd-apikey-IBMid-693001D100-2026-01-12T21:35:12Z`
   - This is NOT the API key!

2. **API Key ID** (what you need):
   - Long string like: `ApiKey-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
   - This is the actual API key value
   - Usually 50+ characters long

## How to Get the Correct Key

### Step 1: Click on the PolicyIQ Row

1. In your API keys table, click on the **"PolicyIQ"** row
2. A popup window will appear on the right side

### Step 2: Find the ID Field in Popup

In the popup, look for a field labeled **"ID"** (not "Name" or "Description")

It will show something like:
```
ID: ApiKey-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

### Step 3: Copy the Full Key

1. Click the **"Copy ID to clipboard"** button next to the ID field
2. This copies the ENTIRE API key (starts with `ApiKey-`)

### Step 4: Verify the Key

The key should:
- Start with `ApiKey-`
- Be about 50-60 characters long
- NOT be the short table ID

## Common Mistakes

❌ **Wrong:** Using the table ID (short, like `cpd-apikey-...`)
✅ **Correct:** Using the API key ID from the popup (long, starts with `ApiKey-`)

❌ **Wrong:** `ApiKey-9df4beb1-dde2-4bbb-bae7-b51cb918f00d` (43 chars - too short)
✅ **Correct:** `ApiKey-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` (50+ chars)

## After Getting the Correct Key

1. Update `.env` file with the full key
2. Test with: `python simple_key_test.py`
3. Should show: `✓✓✓ KEY IS VALID! ✓✓✓`
