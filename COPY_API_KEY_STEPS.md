# How to Copy Your API Key from IBM Cloud

Based on your screenshot, here's exactly what to do:

## Step-by-Step Instructions

### Step 1: Click on the PolicyIQ API Key

In your IBM Cloud API keys page:
1. Find the row with **Name: "PolicyIQ"**
2. Click anywhere on that row

### Step 2: Copy the API Key

In the popup window that appears:
1. Look for the **"ID"** field
2. You'll see something like: `ApiKey-a2f5ece1-29f0-4feb-...`
3. Click the **"Copy ID to clipboard"** button (or the copy icon)
4. The FULL key will be copied (even if it's partially shown in the popup)

### Step 3: Update .env File

**Option A: Using sed (Quick)**
```bash
cd /Users/dakidinesh/Documents/PolicyIQ/backend

# Replace YOUR-COPIED-KEY with the key you just copied
sed -i '' 's|^WATSONX_AI_API_KEY=.*|WATSONX_AI_API_KEY=YOUR-COPIED-KEY|' .env
```

**Option B: Manual Edit (Recommended)**
```bash
cd /Users/dakidinesh/Documents/PolicyIQ/backend
nano .env
```

Then:
1. Find the line: `WATSONX_AI_API_KEY=ApiKey-9df4beb1-dde2-4bbb-bae7-b51cb918f00d`
2. Replace the entire value after `=` with your copied key
3. Make sure it looks like: `WATSONX_AI_API_KEY=ApiKey-a2f5ece1-29f0-4feb-...` (your full key)
4. Save: Ctrl+X, then Y, then Enter

### Step 4: Verify

```bash
cd backend
source venv/bin/activate
python verify_api_key.py
```

**Expected:** Should show `✓✓✓ API KEY IS VALID! ✓✓✓`

### Step 5: Restart Backend

```bash
# Stop current server (Ctrl+C)
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

## Important Notes

⚠️ **Make sure you copy the ENTIRE key:**
- It should start with `ApiKey-`
- It should be about 40-50 characters long
- Don't copy just the visible part - use the "Copy ID" button

⚠️ **No spaces or quotes:**
- ✅ Correct: `WATSONX_AI_API_KEY=ApiKey-xxx`
- ❌ Wrong: `WATSONX_AI_API_KEY="ApiKey-xxx"`
- ❌ Wrong: `WATSONX_AI_API_KEY = ApiKey-xxx`

## Which Key to Use?

From your screenshot:
- **PolicyIQ** key - This is the one you created, use this one
- **CPD API key** - This is for Watson Studio, don't use this

Use the **PolicyIQ** API key!

## Quick Test After Update

After updating and restarting backend:

1. Go to http://localhost:3000
2. Ask a question
3. Should get real answers (not errors)!
