# Test Everything - PolicyIQ

## Quick Test Command

Run this in your terminal (with venv activated):

```bash
cd /Users/dakidinesh/Documents/PolicyIQ/backend
source venv/bin/activate
python test_everything.py
```

Or use the shell script:

```bash
cd /Users/dakidinesh/Documents/PolicyIQ/backend
./run_tests.sh
```

## Manual Test Checklist

### 1. Configuration Test

```bash
cd backend
source venv/bin/activate
python -c "from core.config import settings; print('API Key:', 'SET' if settings.WATSONX_AI_API_KEY else 'NOT SET'); print('Project ID:', 'SET' if settings.WATSONX_AI_PROJECT_ID else 'NOT SET')"
```

**Expected:** Both should show "SET"

### 2. API Key Format Test

Check your `.env` file:
```bash
cd backend
grep WATSONX_AI_API_KEY .env
```

**Should show:**
```
WATSONX_AI_API_KEY=ApiKey-9df4beb1-dde2-4bbb-bae7-b51cb918f00d
```

**Note:** Must start with `ApiKey-`

### 3. API Key Validity Test

```bash
cd backend
source venv/bin/activate
python test_api_key_fixed.py
```

**Expected:** Should show "✓ API Key is VALID!"

### 4. Client Initialization Test

```bash
cd backend
source venv/bin/activate
python -c "
from services.watsonx_ai.client import WatsonxAIClient
client = WatsonxAIClient()
if client.client:
    print('✓ Client initialized')
else:
    print('✗ Client failed to initialize')
"
```

**Expected:** "✓ Client initialized"

### 5. Test API Call

```bash
cd backend
source venv/bin/activate
python -c "
from services.watsonx_ai.client import WatsonxAIClient
client = WatsonxAIClient()
if client.client:
    result = client.generate_completion('Say hello in one word.')
    print('Response:', result['text'][:100])
else:
    print('Client not initialized')
"
```

**Expected:** Should return actual text (not placeholder)

### 6. Backend Server Test

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

**In another terminal:**
```bash
curl http://localhost:8000/health
```

**Expected:** `{"status":"healthy"}`

### 7. Frontend Test

```bash
cd frontend
npm start
```

**Expected:** Browser opens to http://localhost:3000

### 8. End-to-End Test

1. Start backend (Terminal 1)
2. Start frontend (Terminal 2)
3. Go to http://localhost:3000
4. Upload a PDF document
5. Ask a question
6. Should get real answer (not error)

## Current Status Based on Your Configuration

From your `.env` file (based on env.example):

### watsonx.ai
- ✅ **API Key Format**: Correct (starts with `ApiKey-`)
- ✅ **Project ID**: Correct (UUID format)
- ✅ **URL**: Correct
- ⚠️ **Need to verify**: Actual API key validity

### watsonx.data
- ✅ **URL**: Set
- ✅ **Username**: Set
- ✅ **Password**: Set

## Issues Found & Fixed

1. ✅ **API Key Prefix**: Fixed - now includes `ApiKey-`
2. ✅ **Token Endpoint**: Fixed - now uses `https://iam.cloud.ibm.com/identity/token`
3. ✅ **API Implementation**: Fixed - now makes actual API calls

## Next Steps

1. **Run the test script:**
   ```bash
   cd backend
   source venv/bin/activate
   python test_everything.py
   ```

2. **If API key test passes:**
   - Restart backend server
   - Test in frontend

3. **If API key test fails:**
   - Verify API key in IBM Cloud
   - Check Project ID matches your project
   - Generate new API key if needed

## Troubleshooting

### "No module named 'pydantic_settings'"
**Fix:** Activate venv and install dependencies
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "API Key is INVALID"
**Fix:** 
- Check API key in IBM Cloud console
- Verify it starts with `ApiKey-`
- Make sure it's not expired

### "Client not initialized"
**Fix:**
- Check .env file has correct values
- Restart backend after updating .env
- Check backend logs for errors
