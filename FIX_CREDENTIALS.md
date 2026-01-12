# Fix "watsonx.ai client not initialized" Error

## Quick Fix

The error "watsonx.ai client not initialized. Check API credentials" means your API keys aren't being loaded.

### Step 1: Check Credentials

Run this diagnostic script:

```bash
cd /Users/dakidinesh/Documents/PolicyIQ/backend
source venv/bin/activate
python test_credentials.py
```

This will tell you:
- If .env file exists
- If API keys are set
- If client can initialize

### Step 2: Verify .env File

Make sure `backend/.env` exists and has your credentials:

```bash
cd backend
cat .env | grep WATSONX_AI
```

You should see:
```
WATSONX_AI_API_KEY=ApiKey-your-actual-key-here
WATSONX_AI_PROJECT_ID=your-project-id-here
```

### Step 3: Common Issues

#### Issue 1: .env file doesn't exist

**Solution:**
```bash
cd backend
cp env.example .env
# Then edit .env with your actual credentials
```

#### Issue 2: Using placeholder values

**Problem:** .env has `your_watsonx_ai_api_key_here` instead of real key

**Solution:** Replace with your actual API key from IBM Cloud

#### Issue 3: Credentials not loading

**Problem:** Backend server started before .env was created/updated

**Solution:**
1. Stop the backend server (Ctrl+C)
2. Update .env file
3. Restart: `uvicorn main:app --reload`

#### Issue 4: Invalid credentials

**Problem:** API key or Project ID is incorrect

**Solution:**
1. Verify in IBM Cloud console
2. Generate new API key if needed
3. Update .env file
4. Restart server

### Step 4: Test After Fix

After updating credentials:

1. **Restart backend:**
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn main:app --reload
   ```

2. **Check for warnings:**
   - Look for "Failed to initialize watsonx.ai client" warnings
   - These indicate what's wrong

3. **Test in frontend:**
   - Ask a question
   - Should get real response (not error)

## Verification Checklist

- [ ] `.env` file exists in `backend/` directory
- [ ] `WATSONX_AI_API_KEY` is set (not placeholder)
- [ ] `WATSONX_AI_PROJECT_ID` is set (not placeholder)
- [ ] API key starts with `ApiKey-`
- [ ] Project ID is a valid UUID
- [ ] Backend server restarted after updating .env
- [ ] No errors in backend console

## Still Having Issues?

1. **Run diagnostic:**
   ```bash
   python test_credentials.py
   ```

2. **Check backend logs:**
   - Look for initialization errors
   - Check for network errors

3. **Verify in IBM Cloud:**
   - API key is active
   - Project ID matches your watsonx.ai project
   - Service is accessible

4. **Test API key manually:**
   ```bash
   # Get token
   curl -X POST "https://us-south.ml.cloud.ibm.com/v1/identity/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "apikey=YOUR_API_KEY&grant_type=urn:ibm:params:oauth:grant-type:apikey"
   ```
   
   Should return an access token (not an error)
