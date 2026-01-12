# How to Get IBM watsonx API Keys and Credentials

This guide will help you obtain all the necessary credentials for PolicyIQ from IBM Cloud.

## Prerequisites

1. **IBM Cloud Account**: Sign up at https://cloud.ibm.com (free tier available)
2. **IBM Cloud CLI** (optional but recommended): https://cloud.ibm.com/docs/cli

## Part 1: watsonx.ai Credentials

### Step 1: Access watsonx.ai

1. Log in to IBM Cloud: https://cloud.ibm.com
2. Navigate to the **Catalog**: Click "Catalog" in the top navigation
3. Search for **"watsonx.ai"** or go directly to: https://cloud.ibm.com/catalog/services/watsonx-ai
4. Click on **"watsonx.ai"** service

### Step 2: Create a watsonx.ai Instance

1. Select a **pricing plan** (Lite plan is free for development)
2. Choose a **region** (e.g., US South, EU, etc.)
3. Select a **resource group**
4. Give it a **service name** (e.g., "policyiq-watsonx")
5. Click **"Create"**

### Step 3: Get API Key

1. After the service is created, go to your **Resource List**: https://cloud.ibm.com/resources
2. Click on your watsonx.ai service instance
3. In the service dashboard, look for **"Service credentials"** or **"API Key"**
4. Click **"New credential"** if none exists
5. Copy the **API Key** (starts with `ApiKey-...`)

**Alternative Method (IAM API Key):**
1. Go to **IAM** → **API Keys**: https://cloud.ibm.com/iam/apikeys
2. Click **"Create an IBM Cloud API key"**
3. Give it a name and description
4. Copy the API key (this is your `WATSONX_AI_API_KEY`)

### Step 4: Get Project ID

1. Go to **watsonx.ai Studio**: https://dataplatform.cloud.ibm.com
2. If prompted, select your watsonx.ai instance
3. In the watsonx.ai interface, look for **"Projects"** in the left sidebar
4. Click on a project (or create a new one)
5. The **Project ID** is displayed in the project settings or URL
   - It's a UUID like: `a6d01a81-56bc-4d9d-8868-9c2d1b9980e3`
6. Copy this Project ID

**Note**: If you don't have a project yet:
- Click **"Create project"** in watsonx.ai Studio
- Give it a name (e.g., "PolicyIQ")
- The Project ID will be shown after creation

## Part 2: watsonx.data Credentials

### Step 1: Access watsonx.data

1. In IBM Cloud Catalog, search for **"watsonx.data"**
2. Or go to: https://cloud.ibm.com/catalog/services/watsonx-data
3. Click on **"watsonx.data"** service

### Step 2: Create a watsonx.data Instance

1. Select a **pricing plan**
2. Choose a **region**
3. Select a **resource group**
4. Give it a **service name** (e.g., "policyiq-data")
5. Click **"Create"**

### Step 3: Get Connection Details

After the instance is created:

1. Go to your **Resource List**: https://cloud.ibm.com/resources
2. Click on your watsonx.data instance
3. Look for **"Connection information"** or **"Service credentials"**

You'll need:
- **URL/Endpoint**: The connection URL (e.g., `https://9eadb4b8-c18f-421d-8078-47aee37510c1.dataplatform.cloud.ibm.com`)
- **Username**: Usually your IBM Cloud username or a service-specific username
- **Password**: Service password or API key

**Alternative: Using Service Credentials**

1. In the watsonx.data service dashboard, go to **"Service credentials"**
2. Click **"New credential"**
3. Select credential type (usually "Reader" or "Writer")
4. Copy the credentials which will include:
   - `host` or `url` → `WATSONX_DATA_URL`
   - `username` → `WATSONX_DATA_USERNAME`
   - `password` → `WATSONX_DATA_PASSWORD`

### Step 4: Database Name

- The database name can be created in watsonx.data or use the default
- Common default: `default` or create one like `policyiq_db`
- This goes in `WATSONX_DATA_DATABASE`

## Part 3: Configure Your .env File

1. Copy the example file:
   ```bash
   cd backend
   cp env.example .env
   ```

2. Edit `.env` and fill in your credentials:

   ```env
   # watsonx.ai
   WATSONX_AI_API_KEY=ApiKey-your-actual-key-here
   WATSONX_AI_PROJECT_ID=your-project-id-here
   WATSONX_AI_URL=https://us-south.ml.cloud.ibm.com
   WATSONX_AI_MODEL=meta-llama/llama-2-70b-chat
   
   # watsonx.data
   WATSONX_DATA_URL=https://your-instance-id.dataplatform.cloud.ibm.com
   WATSONX_DATA_USERNAME=your-username
   WATSONX_DATA_PASSWORD=your-password
   WATSONX_DATA_DATABASE=policyiq_db
   ```

3. **Important**: Never commit `.env` to git! It's already in `.gitignore`

## Quick Reference: Where to Find Each Credential

| Credential | Where to Find |
|------------|---------------|
| `WATSONX_AI_API_KEY` | IAM → API Keys, or watsonx.ai Service Credentials |
| `WATSONX_AI_PROJECT_ID` | watsonx.ai Studio → Projects → Project Settings |
| `WATSONX_AI_URL` | Usually `https://us-south.ml.cloud.ibm.com` (based on region) |
| `WATSONX_DATA_URL` | watsonx.data Service → Connection Information |
| `WATSONX_DATA_USERNAME` | watsonx.data Service Credentials |
| `WATSONX_DATA_PASSWORD` | watsonx.data Service Credentials |
| `WATSONX_DATA_DATABASE` | Create in watsonx.data or use default |

## Troubleshooting

### "Invalid API Key" Error
- Verify the API key is copied correctly (no extra spaces)
- Check if the API key has expired
- Ensure you're using the correct region

### "Project Not Found" Error
- Verify the Project ID is correct (UUID format)
- Ensure the project exists in your watsonx.ai instance
- Check that you're using the correct watsonx.ai instance

### "Connection Failed" for watsonx.data
- Verify the URL is correct (should include `https://`)
- Check username and password are correct
- Ensure the watsonx.data instance is running
- Verify network/firewall settings

### Can't Find Service Credentials
- Some services require you to create credentials manually
- Look for "Service credentials" → "New credential" button
- Make sure you have proper permissions (Editor or Administrator role)

## Security Best Practices

1. **Never commit `.env` file** to version control
2. **Use environment variables** in production
3. **Rotate API keys** regularly
4. **Use least privilege** - only grant necessary permissions
5. **Store secrets securely** - use IBM Cloud Secrets Manager for production

## Additional Resources

- **IBM Cloud Documentation**: https://cloud.ibm.com/docs
- **watsonx.ai Documentation**: https://dataplatform.cloud.ibm.com/docs
- **watsonx.data Documentation**: https://www.ibm.com/docs/en/watsonxdata
- **IBM Cloud Support**: https://cloud.ibm.com/unifiedsupport/supportcenter

## Need Help?

If you're having trouble:
1. Check IBM Cloud status: https://cloud.ibm.com/status
2. Review service documentation
3. Contact IBM Cloud support
4. Check the PolicyIQ troubleshooting section in SETUP.md
