# Quick API Key Update Guide

## The Problem

Your `.env` file still has the **old invalid key**: `ApiKey-9df4beb1-dde2-4bbb-bae7-b51cb918f00d`

You need to replace it with the **PolicyIQ API key** from your IBM Cloud account.

## Step 1: Get the Correct Key from IBM Cloud

1. Go to: https://cloud.ibm.com/iam/apikeys
2. Find the row named **"PolicyIQ"** (NOT the CPD one)
3. Click on the **PolicyIQ** row
4. In the popup, find the **"ID"** field
5. Click **"Copy ID to clipboard"** button
6. The full key will be copied (starts with `ApiKey-`)

## Step 2: Update .env File

**Option A: Use the interactive script (Easiest)**
```bash
cd /Users/dakidinesh/Documents/PolicyIQ/backend
./update_api_key.sh
# When prompted, paste your copied key and press Enter
```

**Option B: Manual update**
```bash
cd /Users/dakidinesh/Documents/PolicyIQ/backend
nano .env
```

Find this line:
```
WATSONX_AI_API_KEY=ApiKey-9df4beb1-dde2-4bbb-bae7-b51cb918f00d
```

Replace with your copied key:
```
WATSONX_AI_API_KEY=ApiKey-YOUR-ACTUAL-POLICYIQ-KEY-HERE
```

Save: `Ctrl+X`, then `Y`, then `Enter`

**Option C: One-line command**
```bash
cd /Users/dakidinesh/Documents/PolicyIQ/backend

# Replace YOUR-KEY with the actual key you copied
sed -i '' 's|^WATSONX_AI_API_KEY=.*|WATSONX_AI_API_KEY=YOUR-KEY-HERE|' .env
```

## Step 3: Verify

```bash
cd backend
source venv/bin/activate
python verify_api_key.py
```

**Expected output:**
```
✓✓✓ API KEY IS VALID! ✓✓✓
```

## Important Notes

⚠️ **Make sure you're using the PolicyIQ key, NOT the CPD key:**
- ✅ Use: The key from the "PolicyIQ" row
- ❌ Don't use: The key from "cpd-apikey-IBMid..." row

⚠️ **Copy the ENTIRE key:**
- It should be about 40-50 characters
- Starts with `ApiKey-`
- Use the "Copy ID" button, don't type it manually

⚠️ **No extra characters:**
- No quotes: `WATSONX_AI_API_KEY=ApiKey-xxx` ✅
- No spaces: `WATSONX_AI_API_KEY=ApiKey-xxx` ✅
- Wrong: `WATSONX_AI_API_KEY="ApiKey-xxx"` ❌

## Troubleshooting

If it still says invalid after updating:

1. **Double-check you copied the PolicyIQ key** (not CPD)
2. **Make sure no extra spaces** before/after the key
3. **Verify the key format**: Should start with `ApiKey-`
4. **Check the key is enabled** in IBM Cloud (green toggle should be ON)

## After Success

Once verified, restart your backend:
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

Then test at: http://localhost:3000
