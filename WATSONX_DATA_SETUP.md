# How to Get watsonx.data Credentials

Step-by-step guide to get your watsonx.data connection credentials.

## Prerequisites

- IBM Cloud account (you already have this)
- watsonx.data service instance created

## Step-by-Step Instructions

### Step 1: Access Your watsonx.data Instance

1. **Log in to IBM Cloud**: https://cloud.ibm.com
2. **Go to Resource List**: Click "Resource List" in the top menu, or go to: https://cloud.ibm.com/resources
3. **Find your watsonx.data instance**: Look for a service named "watsonx.data" or similar
4. **Click on the service name** to open it

### Step 2: Get Service Credentials

**Method A: From Service Dashboard (Recommended)**

1. In your watsonx.data service page, look for **"Service credentials"** in the left sidebar
2. Click **"Service credentials"**
3. You'll see a list of credentials (or it might be empty)
4. Click **"New credential"** button (top right)
5. Fill in:
   - **Name**: Give it a name like "policyiq-credentials"
   - **Role**: Select "Writer" or "Manager" (needs write access for PolicyIQ)
6. Click **"Add"** or **"Create"**
7. **Copy the credentials** - you'll see a JSON object with:
   ```json
   {
     "host": "https://xxxxx.dataplatform.cloud.ibm.com",
     "username": "your_username",
     "password": "your_password",
     "database": "default"
   }
   ```

**Method B: From Connection Information**

1. In the watsonx.data service page, look for **"Connection information"** or **"Overview"**
2. You might see connection details displayed there
3. If you see a "View credentials" button, click it

### Step 3: Extract the Values

From the credentials JSON, extract:

- **`host`** or **`url`** → This is your `WATSONX_DATA_URL`
  - Should look like: `https://xxxxx.dataplatform.cloud.ibm.com`
  - Make sure it starts with `https://`

- **`username`** → This is your `WATSONX_DATA_USERNAME`
  - Usually your IBM Cloud username (email) or a service-specific username

- **`password`** → This is your `WATSONX_DATA_PASSWORD`
  - This is an API key or service password, NOT your IBM Cloud login password

- **`database`** (optional) → This is your `WATSONX_DATA_DATABASE`
  - Default is usually `"default"` or you can create one like `"policyiq_db"`

## Step 4: Update Your .env File

1. **Copy the example file** (if you haven't already):
   ```bash
   cd backend
   cp env.example .env
   ```

2. **Edit the `.env` file** and update these lines:

   ```env
   # IBM watsonx.data Configuration
   WATSONX_DATA_URL=https://your-instance-id.dataplatform.cloud.ibm.com
   WATSONX_DATA_USERNAME=your_username_from_credentials
   WATSONX_DATA_PASSWORD=your_password_from_credentials
   WATSONX_DATA_DATABASE=policyiq_db
   ```

3. **Replace the placeholder values** with your actual credentials

## Visual Guide: Where to Find Credentials

```
IBM Cloud Console
  └── Resource List
      └── watsonx.data Service
          └── Service Credentials (left sidebar)
              └── New credential / View credential
                  └── JSON with host, username, password
```

## Common Issues & Solutions

### Issue 1: "Service credentials" option not visible

**Solution:**
- Make sure you're the owner of the service or have Editor/Administrator role
- Try refreshing the page
- Check if the service is fully provisioned (not still creating)

### Issue 2: Can't create new credentials

**Solution:**
- You might need to wait a few minutes after creating the service
- Ensure you have proper IAM permissions
- Try using an existing credential if available

### Issue 3: URL format is wrong

**Solution:**
- The URL must start with `https://`
- Format should be: `https://{instance-id}.dataplatform.cloud.ibm.com`
- If you only have an instance ID, construct the full URL manually

### Issue 4: Authentication fails

**Solution:**
- Double-check username and password (no extra spaces)
- Username is usually your IBM Cloud email
- Password is the API key from credentials, not your login password
- Try creating a new credential with "Writer" role

## Alternative: Using IBM Cloud CLI

If you prefer command line:

```bash
# Install IBM Cloud CLI (if not installed)
# macOS: brew install ibmcloud-cli
# Or download from: https://cloud.ibm.com/docs/cli

# Login
ibmcloud login

# List your services
ibmcloud resource service-instances

# Get service credentials
ibmcloud resource service-keys <your-service-name>
```

## Testing Your Credentials

After updating `.env`, you can test:

```bash
cd backend
python -c "
from core.config import settings
print('URL:', settings.WATSONX_DATA_URL)
print('Username:', settings.WATSONX_DATA_USERNAME)
print('Database:', settings.WATSONX_DATA_DATABASE)
"
```

## Security Reminder

⚠️ **Important**: 
- Never commit your `.env` file to git (it's already in `.gitignore`)
- Keep your credentials secure
- Rotate credentials periodically
- Use different credentials for development and production

## Still Need Help?

1. **Check IBM Cloud Status**: https://cloud.ibm.com/status
2. **watsonx.data Documentation**: https://www.ibm.com/docs/en/watsonxdata
3. **IBM Cloud Support**: https://cloud.ibm.com/unifiedsupport/supportcenter

## Quick Checklist

- [ ] Found watsonx.data service in Resource List
- [ ] Opened Service Credentials
- [ ] Created or viewed credentials
- [ ] Copied `host` → `WATSONX_DATA_URL`
- [ ] Copied `username` → `WATSONX_DATA_USERNAME`
- [ ] Copied `password` → `WATSONX_DATA_PASSWORD`
- [ ] Set `WATSONX_DATA_DATABASE` (default or custom)
- [ ] Updated `.env` file
- [ ] Verified URL format (starts with `https://`)

Once you complete these steps, you're ready to use PolicyIQ with watsonx.data!
