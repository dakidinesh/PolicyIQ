# Complete Fix Guide - Both Keys Failing

If **both** API keys are showing as invalid, the issue is likely one of these:

## Issue 1: API Keys Don't Have watsonx.ai Permissions

**Problem:** API keys created from IAM might not have access to watsonx.ai service.

**Solution: Create API Key from watsonx.ai Service**

1. Go to: https://dataplatform.cloud.ibm.com
2. Sign in and select your project
3. Go to **Project Settings** → **Access** or **API Keys**
4. Create a new API key from there
5. This key will automatically have watsonx.ai permissions

**OR: Add Permissions to Existing Key**

1. Go to: https://cloud.ibm.com/iam/apikeys
2. Click on your PolicyIQ API key
3. Check if it has "watsonx.ai" service access
4. If not, you may need to:
   - Go to IAM → Access (IAM) → Service IDs
   - Create a service ID with watsonx.ai access
   - Use that service ID's API key

## Issue 2: Wrong Project ID

**Problem:** The Project ID in `.env` might be wrong or from a different region.

**Solution: Get Correct Project ID**

1. Go to: https://dataplatform.cloud.ibm.com
2. Click on your project
3. Look at the URL - it will be:
   ```
   https://dataplatform.cloud.ibm.com/projects/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   ```
4. The part after `/projects/` is your Project ID
5. Copy it and update `.env`:
   ```bash
   cd /Users/dakidinesh/Documents/PolicyIQ/backend
   nano .env
   # Update WATSONX_AI_PROJECT_ID=your-actual-project-id
   ```

## Issue 3: Region Mismatch

**Problem:** API key, project, and URL might be from different regions.

**Solution: Check Region Consistency**

Your `.env` has:
```
WATSONX_AI_URL=https://us-south.ml.cloud.ibm.com
```

Make sure:
- Your watsonx.ai instance is in **US South** region
- Your project is in the **same region**
- Your API key has access to that **region**

To check:
1. Go to: https://cloud.ibm.com/resources
2. Find your watsonx.ai service
3. Check the region (should be "US South" if URL says us-south)

If different, update URL:
- US South: `https://us-south.ml.cloud.ibm.com`
- EU Germany: `https://eu-de.ml.cloud.ibm.com`
- EU Great Britain: `https://eu-gb.ml.cloud.ibm.com`

## Issue 4: API Key Format/Copying Issue

**Problem:** Key might have hidden characters or be incomplete.

**Solution: Verify Key Format**

Run:
```bash
cd backend
source venv/bin/activate
python diagnose_keys.py
```

This will:
- Test IAM token generation
- Test watsonx.ai access
- Show detailed error messages
- Help identify the exact problem

## Quick Test: Create Fresh API Key

If nothing works, create a completely new key:

1. **From watsonx.ai (Recommended):**
   - Go to: https://dataplatform.cloud.ibm.com
   - Project Settings → Access → Create API Key
   - Copy the key immediately

2. **Update .env:**
   ```bash
   cd /Users/dakidinesh/Documents/PolicyIQ/backend
   nano .env
   ```
   Update:
   ```
   WATSONX_AI_API_KEY=ApiKey-YOUR-NEW-KEY
   WATSONX_AI_PROJECT_ID=YOUR-PROJECT-ID
   ```

3. **Test:**
   ```bash
   python verify_api_key.py
   ```

## Diagnostic Commands

Run these to get detailed info:

```bash
cd backend
source venv/bin/activate

# Test current key
python verify_api_key.py

# Comprehensive diagnostic
python diagnose_keys.py

# Check configuration
cat .env | grep WATSONX
```

## Still Not Working?

If both keys fail at IAM token level (400 error), they might be:
- Deleted/revoked
- From a different IBM Cloud account
- Expired (if they have expiration)

**Solution:** Create a brand new API key from scratch.
