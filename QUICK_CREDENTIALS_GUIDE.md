# Quick Guide: Getting watsonx.data Credentials

You already have watsonx.ai credentials! Now you just need watsonx.data username and password.

## Quick Steps for watsonx.data

### Option 1: From IBM Cloud Console (Easiest)

1. **Go to IBM Cloud Resources**: https://cloud.ibm.com/resources
2. **Find your watsonx.data instance** (click on it)
3. **Click "Service credentials"** in the left sidebar
4. **Click "New credential"** (or view existing one)
5. **Copy the credentials** - you'll see:
   - `host` or `url` → This is your `WATSONX_DATA_URL` (should be full URL like `https://...`)
   - `username` → `WATSONX_DATA_USERNAME`
   - `password` → `WATSONX_DATA_PASSWORD`

### Option 2: From watsonx.data Dashboard

1. **Open watsonx.data**: Go to https://dataplatform.cloud.ibm.com
2. **Select your instance** (if prompted)
3. **Go to "Administration"** → **"Connection Information"**
4. **Copy connection details**:
   - Connection URL → `WATSONX_DATA_URL`
   - Username → `WATSONX_DATA_USERNAME`
   - Password → `WATSONX_DATA_PASSWORD`

### Option 3: Using IBM Cloud CLI

```bash
# Install IBM Cloud CLI if needed
ibmcloud login

# Get service credentials
ibmcloud resource service-keys <your-watsonx-data-instance-name>
```

## Important Notes

### URL Format
Your `WATSONX_DATA_URL` should be a **full URL**, not just the instance ID:
- ✅ **Correct**: `https://9eadb4b8-c18f-421d-8078-47aee37510c1.dataplatform.cloud.ibm.com`
- ❌ **Wrong**: `9eadb4b8-c18f-421d-8078-47aee37510c1`

If you only have the instance ID, add the prefix:
- Format: `https://{instance-id}.dataplatform.cloud.ibm.com`
- Or: `https://{instance-id}.{region}.watsonx.data.cloud.ibm.com`

### Username & Password
- **Username**: Usually your IBM Cloud username (email) or a service-specific username
- **Password**: This is typically an **API key** or service password, NOT your IBM Cloud login password

## Update Your .env File

Once you have the credentials:

```bash
cd backend
cp env.example .env
# Edit .env with your actual watsonx.data credentials
```

Your `.env` should look like:

```env
# watsonx.ai (you already have these ✅)
WATSONX_AI_API_KEY=ApiKey-9df4beb1-dde2-4bbb-bae7-b51cb918f00d
WATSONX_AI_PROJECT_ID=a6d01a81-56bc-4d9d-8868-9c2d1b9980e3

# watsonx.data (fill these in)
WATSONX_DATA_URL=https://9eadb4b8-c18f-421d-8078-47aee37510c1.dataplatform.cloud.ibm.com
WATSONX_DATA_USERNAME=your_actual_username
WATSONX_DATA_PASSWORD=your_actual_password_or_api_key
WATSONX_DATA_DATABASE=policyiq_db
```

## Testing Your Credentials

After updating `.env`, test the connection:

```bash
cd backend
python -c "from core.config import settings; print('Config loaded:', settings.WATSONX_DATA_URL)"
```

## Still Having Trouble?

1. **Check IBM Cloud Status**: https://cloud.ibm.com/status
2. **Verify Service is Running**: Ensure your watsonx.data instance is active
3. **Check Permissions**: Make sure you have access to the service
4. **See Full Guide**: Check `GETTING_CREDENTIALS.md` for detailed instructions

## Common Issues

**"Can't find Service Credentials"**
- Some instances require you to manually create credentials
- Look for "Service credentials" → "New credential" button
- Make sure you're the owner or have Editor role

**"URL format error"**
- Ensure URL starts with `https://`
- Include the full domain (`.dataplatform.cloud.ibm.com`)

**"Authentication failed"**
- Username might be your IBM Cloud email
- Password might be an API key (not your login password)
- Try creating a new service credential
