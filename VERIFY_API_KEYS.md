# Verify API Keys Configuration

## Quick Check

Run this script to verify your API keys are configured correctly:

```bash
cd /Users/dakidinesh/Documents/PolicyIQ/backend
source venv/bin/activate
python check_credentials.py
```

## Manual Check

### 1. Check .env File Exists

```bash
cd backend
ls -la .env
```

### 2. Verify API Keys in .env

```bash
cat .env | grep WATSONX
```

You should see:
- `WATSONX_AI_API_KEY=ApiKey-...`
- `WATSONX_AI_PROJECT_ID=...`
- `WATSONX_DATA_URL=...`
- `WATSONX_DATA_USERNAME=...`
- `WATSONX_DATA_PASSWORD=...`

### 3. Test Configuration Loading

```bash
cd backend
source venv/bin/activate
python -c "from core.config import settings; print('API Key:', 'SET' if settings.WATSONX_AI_API_KEY else 'NOT SET')"
```

## Common Issues

### Issue: Placeholder Response "[Generated response - implement actual API call]"

**Cause:** The watsonx.ai API call is not working properly.

**Solutions:**

1. **Verify API Keys:**
   ```bash
   python check_credentials.py
   ```

2. **Check API Key Format:**
   - Should start with `ApiKey-`
   - Should be the full key from IBM Cloud

3. **Verify Project ID:**
   - Should be a UUID format
   - Should match your watsonx.ai project

4. **Check URL:**
   - Should be: `https://us-south.ml.cloud.ibm.com` (or your region)
   - No trailing slash

5. **Test API Connection:**
   - Make sure you have internet connection
   - Check if watsonx.ai service is accessible

### Issue: "watsonx.ai client not initialized"

**Cause:** API key or Project ID is missing or invalid.

**Solution:**
1. Check `.env` file has correct values
2. Restart the backend server after updating `.env`
3. Verify credentials in IBM Cloud console

### Issue: "Failed to get access token"

**Cause:** API key is invalid or expired.

**Solution:**
1. Generate a new API key in IBM Cloud
2. Update `.env` file
3. Restart backend server

## Testing the API

After fixing credentials, test with:

```bash
cd backend
source venv/bin/activate
python -c "
from services.watsonx_ai.client import WatsonxAIClient
client = WatsonxAIClient()
if client.client:
    print('✓ Client initialized')
    result = client.generate_completion('Hello, test prompt')
    print('Response:', result['text'][:100])
else:
    print('✗ Client not initialized')
"
```

## Next Steps

1. Run `check_credentials.py` to verify configuration
2. If keys are missing, update `.env` file
3. Restart backend server: `uvicorn main:app --reload`
4. Try asking a question in the frontend
