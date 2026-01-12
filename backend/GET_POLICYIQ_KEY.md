# Get the Correct PolicyIQ API Key

## From Your Screenshot

I can see you have multiple API keys:
- ✅ **PolicyIQ** (created 1-12-2026 21:34 GMT) - **USE THIS ONE**
- PolicyIQ-test (created 1-12-2026 23:25 GMT)
- test (created 1-12-2026 23:30 GMT)

## Steps to Get the Correct Key

1. **Click on the "PolicyIQ" row** (the first one, created at 21:34)
   - NOT "PolicyIQ-test"
   - NOT "test"

2. **A popup will appear** showing key details

3. **Find the "ID" field** in the popup
   - It will show something like: `ApiKey-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

4. **Click "Copy ID to clipboard"** button
   - This copies the FULL key

5. **Paste it into your .env file**
   - Replace the current key with this one

## Important

Make sure you're copying from the **"PolicyIQ"** key (created at 21:34), not the test keys!

## After Updating

Once you've updated .env with the correct PolicyIQ key, I'll test it for you.
