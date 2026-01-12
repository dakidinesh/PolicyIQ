# Validate Your API Keys

## Quick Validation

Run this command to check if your API keys are valid:

```bash
cd /Users/dakidinesh/Documents/PolicyIQ/backend
source venv/bin/activate
python validate_api_keys.py
```

Or use the shell script:

```bash
cd /Users/dakidinesh/Documents/PolicyIQ/backend
./check_api_keys.sh
```

## Manual Validation

Based on your `env.example`, I can see you have credentials configured. Let me validate the format:

### watsonx.ai Credentials

From your `env.example`:
- **API Key**: `ApiKey-9df4beb1-dde2-4bbb-bae7-b51cb918f00d`
  - ✓ Format looks correct (starts with `ApiKey-`)
  - ✓ Length is appropriate
  
- **Project ID**: `a6d01a81-56bc-4d9d-8868-9c2d1b9980e3`
  - ✓ Format looks correct (UUID format)
  - ✓ Length is correct (36 characters)

- **URL**: `https://us-south.ml.cloud.ibm.com`
  - ✓ Format is correct

### watsonx.data Credentials

From your `env.example`:
- **URL**: `https://us-south.lakehouse.cloud.ibm.com`
  - ⚠ Note: This looks like a lakehouse URL, not the standard watsonx.data URL format
  - Standard format: `https://{instance-id}.dataplatform.cloud.ibm.com`
  
- **Username**: `apikey`
  - ✓ Set
  
- **Password**: `BLv5ih3INx5t60EXiKBkP9NHNNykHUiV8aChqcW3LJg_`
  - ✓ Set

## Test API Key Validity

To test if your watsonx.ai API key is actually valid, run:

```bash
# Test API key
curl -X POST "https://us-south.ml.cloud.ibm.com/v1/identity/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "apikey=ApiKey-9df4beb1-dde2-4bbb-bae7-b51cb918f00d&grant_type=urn:ibm:params:oauth:grant-type:apikey"
```

**Expected Result:**
- If valid: Returns JSON with `access_token`
- If invalid: Returns error (401 or 403)

## Common Issues

### Issue 1: .env file not being read

**Check:**
```bash
cd backend
ls -la .env
```

**Fix:**
```bash
# If .env doesn't exist, copy from example
cp env.example .env
```

### Issue 2: Backend server not reloading .env

**Fix:**
1. Stop backend server (Ctrl+C)
2. Restart: `uvicorn main:app --reload`

### Issue 3: API key format looks correct but still fails

**Possible causes:**
- API key expired or revoked
- API key doesn't have required permissions
- Project ID doesn't match the API key's project

**Solution:**
1. Generate new API key in IBM Cloud
2. Verify Project ID matches your watsonx.ai project
3. Update .env file
4. Restart backend

## Next Steps

1. **Run validation script:**
   ```bash
   cd backend
   source venv/bin/activate
   python validate_api_keys.py
   ```

2. **Check backend logs** when you start the server:
   ```bash
   uvicorn main:app --reload
   ```
   Look for warnings about client initialization

3. **Test in frontend:**
   - Ask a question
   - Should get real response (not error)

## What the Validation Checks

✅ **Format validation:**
- API key starts with `ApiKey-`
- Project ID is UUID format
- URLs are valid HTTPS URLs

✅ **Actual API test:**
- Attempts to get IAM token
- Validates authentication
- Checks token expiration

✅ **Configuration check:**
- Verifies all required fields are set
- Checks for placeholder values
- Validates format
