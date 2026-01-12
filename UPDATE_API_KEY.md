# How to Update Your API Key

## Current Status

Your API key is **INVALID**. The key `ApiKey-9df4beb1-dde2-4bbb-bae7-b51cb918f00d` does not exist in IBM Cloud.

## Step-by-Step: Get a Valid API Key

### Step 1: Go to IBM Cloud

Open your browser and go to:
**https://cloud.ibm.com/iam/apikeys**

### Step 2: Create or Find API Key

**Option A: Create New API Key**
1. Click **"Create an IBM Cloud API key"**
2. Give it a name: "PolicyIQ" or "watsonx.ai"
3. Click **"Create"**
4. **IMPORTANT**: Copy the key immediately (you won't see it again!)
5. The key will look like: `ApiKey-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

**Option B: Use Existing API Key**
1. Find an existing API key in the list
2. If you see one, click the **"Actions"** menu (three dots)
3. Click **"Copy"** or **"View"** to see the key
4. Copy the full key

### Step 3: Update .env File

1. **Open the file:**
   ```bash
   cd /Users/dakidinesh/Documents/PolicyIQ/backend
   nano .env
   # or use your preferred editor: code .env, vim .env, etc.
   ```

2. **Find this line:**
   ```
   WATSONX_AI_API_KEY=ApiKey-9df4beb1-dde2-4bbb-bae7-b51cb918f00d
   ```

3. **Replace with your new key:**
   ```
   WATSONX_AI_API_KEY=ApiKey-YOUR-NEW-KEY-HERE
   ```

4. **IMPORTANT**: 
   - Make sure there are **no spaces** around the `=`
   - Make sure there are **no quotes** around the key
   - Make sure the key starts with `ApiKey-`
   - Save the file

### Step 4: Verify the Update

Run this to check:
```bash
cd /Users/dakidinesh/Documents/PolicyIQ/backend
source venv/bin/activate
python verify_api_key.py
```

**Expected:** Should show `✓✓✓ API KEY IS VALID! ✓✓✓`

### Step 5: Restart Backend

**IMPORTANT**: You must restart the backend for changes to take effect!

```bash
# Stop current server (Ctrl+C in the terminal running it)
# Then restart:
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

### Step 6: Test in Frontend

1. Make sure backend is running
2. Start frontend (if not running):
   ```bash
   cd frontend
   npm start
   ```
3. Go to http://localhost:3000
4. Ask a question
5. Should get real answers!

## Quick Verification

After updating, verify:

```bash
cd backend
source venv/bin/activate
python verify_api_key.py
```

If it shows "API KEY IS VALID", you're good to go!

## Common Mistakes

❌ **Wrong**: `WATSONX_AI_API_KEY="ApiKey-xxx"` (quotes)
❌ **Wrong**: `WATSONX_AI_API_KEY = ApiKey-xxx` (spaces)
❌ **Wrong**: `WATSONX_AI_API_KEY=ApiKey-xxx ` (trailing space)
✅ **Correct**: `WATSONX_AI_API_KEY=ApiKey-xxx` (no quotes, no spaces)

## Still Having Issues?

1. **Double-check the key** - Make sure you copied the ENTIRE key
2. **Check for typos** - API keys are case-sensitive
3. **Verify in IBM Cloud** - Make sure the key exists and is active
4. **Restart backend** - Changes only take effect after restart

## Need Help?

If the key is still invalid after updating:
1. Generate a completely new API key
2. Make sure you're logged into the correct IBM Cloud account
3. Verify the key has watsonx.ai permissions
