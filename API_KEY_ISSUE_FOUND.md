# ⚠️ API Key Issue Found!

## Problem

I found that your API key in `env.example` is **missing the `ApiKey-` prefix**!

**Current (WRONG):**
```
WATSONX_AI_API_KEY=9df4beb1-dde2-4bbb-bae7-b51cb918f00d
```

**Should be (CORRECT):**
```
WATSONX_AI_API_KEY=ApiKey-9df4beb1-dde2-4bbb-bae7-b51cb918f00d
```

## Fix

### Option 1: Update .env file directly

If you have a `.env` file, update it:

```bash
cd backend
# Edit .env and add "ApiKey-" prefix to your API key
```

Or use sed:
```bash
cd backend
sed -i '' 's/^WATSONX_AI_API_KEY=\(.*\)$/WATSONX_AI_API_KEY=ApiKey-\1/' .env
```

### Option 2: Copy from fixed env.example

I've fixed `env.example`. If you don't have `.env` yet:

```bash
cd backend
cp env.example .env
```

If you already have `.env`, manually add `ApiKey-` prefix to your API key.

## Verify the Fix

After updating, test your API key:

```bash
cd backend
source venv/bin/activate
python quick_test_api.py
```

Or test manually:
```bash
curl -X POST "https://us-south.ml.cloud.ibm.com/v1/identity/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "apikey=ApiKey-9df4beb1-dde2-4bbb-bae7-b51cb918f00d&grant_type=urn:ibm:params:oauth:grant-type:apikey"
```

**Expected:** Should return JSON with `access_token` (not an error)

## After Fixing

1. **Restart backend server:**
   ```bash
   # Stop current server (Ctrl+C)
   cd backend
   source venv/bin/activate
   uvicorn main:app --reload
   ```

2. **Test in frontend:**
   - Ask a question
   - Should now work!

## Why This Matters

IBM watsonx.ai API keys **must** start with `ApiKey-` prefix. Without it:
- Client initialization fails
- Authentication fails
- You get "client not initialized" errors

The prefix is part of the actual API key value, not just a label!
