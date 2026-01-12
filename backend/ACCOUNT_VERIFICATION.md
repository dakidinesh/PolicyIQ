# Account Verification & Troubleshooting

## Current Issue

Your API keys keep showing as invalid even though:
- ✅ Format is correct (starts with `ApiKey-`, 51 characters)
- ✅ No extra spaces or quotes
- ✅ Copied correctly

**Error:** "Provided API key could not be found" (BXNIM0415E)

## Root Cause: Account Mismatch

This error almost always means:
- The API key was created in a **different IBM Cloud account**
- You're testing with a different account than where the key was created

## How to Verify

### Step 1: Check Your Current Account

1. Go to: https://cloud.ibm.com
2. Look at the **top right corner** - you'll see your name/email
3. Note the **email address** shown

### Step 2: Verify Key Exists

1. Go to: https://cloud.ibm.com/iam/apikeys
2. Look for the "PolicyIQ" key in the list
3. **If it's NOT there:**
   - The key was created in a different account
   - You need to log into the correct account

### Step 3: Check All Accounts

If you have multiple IBM Cloud accounts:

1. Click on your name in top right
2. Look for "Switch account" or account switcher
3. Check each account for the PolicyIQ key
4. Find which account has the key

## Solution Options

### Option 1: Use the Correct Account

1. Log out of current IBM Cloud account
2. Log into the account where you created the key
3. Verify the key exists at: https://cloud.ibm.com/iam/apikeys
4. Copy the key again
5. Update .env

### Option 2: Create Key in Current Account

1. Stay logged into your current account
2. Go to: https://cloud.ibm.com/iam/apikeys
3. Create a NEW API key
4. Name it "PolicyIQ"
5. Copy it immediately
6. Update .env

### Option 3: Verify Account Access

1. Check if your account is active:
   - Go to: https://cloud.ibm.com/account/settings
   - Verify account status

2. Check if you have proper permissions:
   - Go to: https://cloud.ibm.com/iam/users
   - Verify your user has API key creation permissions

## Quick Test

After updating with a key from the correct account:

```bash
cd backend
source venv/bin/activate
python simple_key_test.py
```

## Still Not Working?

If keys from the correct account still fail:

1. **Check account status:**
   - Account might be suspended
   - Payment issues
   - Account verification needed

2. **Try a different region:**
   - Maybe there's a regional issue
   - Try creating key in different region

3. **Contact IBM Support:**
   - There might be an account-level issue
   - Support can verify API key status

## Important Notes

- API keys are **account-specific**
- Keys from Account A won't work with Account B
- Make sure you're using the key from the same account you're testing with
- The account email shown in IBM Cloud console must match where the key was created
