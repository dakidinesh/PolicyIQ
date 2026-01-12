# Check Your Project ID

If both API keys are failing, the issue might be the **Project ID**, not the API keys!

## How to Get Your watsonx.ai Project ID

### Step 1: Go to watsonx.ai
1. Go to: https://dataplatform.cloud.ibm.com
2. Or: https://cloud.ibm.com/watsonx
3. Sign in with your IBM Cloud account

### Step 2: Find Your Project
1. Look for "Projects" in the left sidebar
2. Click on your project (or create one if you don't have one)
3. The project name should be visible

### Step 3: Get Project ID
**Option A: From URL**
- When you're in your project, look at the browser URL
- It will look like: `https://dataplatform.cloud.ibm.com/projects/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
- The part after `/projects/` is your Project ID

**Option B: From Project Settings**
1. In your project, click on "Settings" or "Manage" tab
2. Look for "Project ID" or "Project GUID"
3. Copy the full ID (looks like: `a6d01a81-56bc-4d9d-8868-9c2d1b9980e3`)

### Step 4: Update .env
```bash
cd /Users/dakidinesh/Documents/PolicyIQ/backend
nano .env
```

Find:
```
WATSONX_AI_PROJECT_ID=a6d01a81-56bc-4d9d-8868-9c2d1b9980e3
```

Replace with your actual project ID.

## Alternative: Create API Key from watsonx.ai

Sometimes API keys created from IAM don't have watsonx.ai permissions.

### Create Key from watsonx.ai Service:
1. Go to: https://dataplatform.cloud.ibm.com
2. Go to your project
3. Look for "Access" or "API Keys" in project settings
4. Create a new API key from there
5. This key will automatically have watsonx.ai permissions

## Test Everything

Run the diagnostic:
```bash
cd backend
source venv/bin/activate
python diagnose_keys.py
```

This will test:
- IAM token generation (API key validity)
- watsonx.ai access (permissions)
- Project ID correctness
- Region settings
