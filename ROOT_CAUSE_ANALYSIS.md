# Root Cause Analysis: Why Both Keys Are Failing

## Current Status

Both API keys are returning:
```
Status Code: 400
Error: "Provided API key could not be found"
```

This means **the keys themselves don't exist in IBM Cloud**, not a permissions issue.

## Possible Causes

### 1. Keys Were Deleted/Revoked
- Someone deleted the keys in IBM Cloud
- Keys expired (if they had expiration set)
- Keys were disabled

**Check:** Go to https://cloud.ibm.com/iam/apikeys and verify:
- Is the "PolicyIQ" key still there?
- Is it enabled (green toggle)?
- Does it show as "Active"?

### 2. Wrong IBM Cloud Account
- Keys are from a different IBM Cloud account
- You're logged into a different account than where keys were created

**Check:** 
- Verify you're logged into the correct IBM Cloud account
- Check the account email matches where you created the keys

### 3. Keys Copied Incorrectly
- Missing characters at start/end
- Extra spaces or hidden characters
- Copied from wrong field

**Check:**
- Use the "Copy ID to clipboard" button (don't type manually)
- Verify key starts with `ApiKey-` and is ~40-50 characters
- No spaces before/after

### 4. Keys Never Actually Created
- Keys shown in UI but not actually saved
- Browser/UI glitch showing non-existent keys

**Solution:** Create a brand new key

## Solution: Create Fresh API Key

### Step 1: Verify Current Keys

1. Go to: https://cloud.ibm.com/iam/apikeys
2. Check if "PolicyIQ" key exists
3. If it exists:
   - Click on it
   - Check if "Enabled" toggle is ON
   - Try copying the ID again
4. If it doesn't exist or is disabled:
   - Delete it
   - Create a new one

### Step 2: Create New API Key (Recommended Method)

**Option A: From watsonx.ai (Best)**
1. Go to: https://dataplatform.cloud.ibm.com
2. Sign in and open your project
3. Go to **Project Settings** → **Access** → **API Keys**
4. Click **"Create API Key"**
5. Give it a name: "PolicyIQ"
6. Copy the key immediately (you won't see it again!)

**Option B: From IAM**
1. Go to: https://cloud.ibm.com/iam/apikeys
2. Click **"Create an IBM Cloud API key"**
3. Name: "PolicyIQ"
4. Description: "For PolicyIQ application"
5. Copy the key immediately

### Step 3: Verify Project ID

1. Go to: https://dataplatform.cloud.ibm.com
2. Open your project
3. Look at URL: `https://dataplatform.cloud.ibm.com/projects/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
4. Copy the UUID after `/projects/`
5. This is your Project ID

### Step 4: Update .env

```bash
cd /Users/dakidinesh/Documents/PolicyIQ/backend
nano .env
```

Update:
```
WATSONX_AI_API_KEY=ApiKey-YOUR-NEW-KEY-HERE
WATSONX_AI_PROJECT_ID=YOUR-PROJECT-ID-HERE
```

Save: `Ctrl+X`, `Y`, `Enter`

### Step 5: Test

```bash
cd backend
source venv/bin/activate
python simple_key_test.py
```

Should show: `✓✓✓ KEY IS VALID! ✓✓✓`

## Quick Verification Checklist

Before testing, verify:
- [ ] API key exists in IBM Cloud console
- [ ] API key is enabled (green toggle)
- [ ] API key starts with `ApiKey-`
- [ ] API key is ~40-50 characters long
- [ ] Project ID is correct UUID format
- [ ] Project exists in watsonx.ai
- [ ] Region matches (us-south, eu-de, etc.)
- [ ] You're logged into correct IBM Cloud account

## If Still Failing

If a brand new key still fails:

1. **Check IBM Cloud account status**
   - Account might be suspended
   - Payment issues
   - Account verification needed

2. **Try different region**
   - Maybe your account is in a different region
   - Update `WATSONX_AI_URL` accordingly

3. **Contact IBM Support**
   - There might be an account-level issue
   - Support can verify API key status

## Test Command

```bash
cd /Users/dakidinesh/Documents/PolicyIQ/backend
source venv/bin/activate
python simple_key_test.py
```

This will tell you exactly what's wrong.
