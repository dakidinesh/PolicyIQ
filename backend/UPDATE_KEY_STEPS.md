# Steps to Update Your New API Key

## Step 1: Copy Your New API Key

You just created a new API key from watsonx.ai. Make sure you have it copied to your clipboard.

## Step 2: Update .env File

**In your .env file (which is currently open):**

Find this line:
```
WATSONX_AI_API_KEY=ApiKey-9df4beb1-dde2-4bbb-bae7-b51cb918f00d
```

**Replace it with:**
```
WATSONX_AI_API_KEY=ApiKey-YOUR-NEW-KEY-HERE
```

(Replace `ApiKey-YOUR-NEW-KEY-HERE` with the actual key you copied)

**Important:**
- ✅ No quotes: `WATSONX_AI_API_KEY=ApiKey-xxx`
- ❌ Wrong: `WATSONX_AI_API_KEY="ApiKey-xxx"`
- ❌ Wrong: `WATSONX_AI_API_KEY = ApiKey-xxx` (no spaces)

## Step 3: Save the File

Press `Ctrl+S` (or `Cmd+S` on Mac) to save.

## Step 4: Test the Key

After saving, run this command:

```bash
cd /Users/dakidinesh/Documents/PolicyIQ/backend
source venv/bin/activate
python simple_key_test.py
```

**Expected output:**
```
✓✓✓ KEY IS VALID! ✓✓✓
```

## Step 5: Restart Backend (if running)

If your backend server is running:
1. Stop it (Ctrl+C)
2. Restart it:
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn main:app --reload
   ```

## Step 6: Test PolicyIQ

1. Make sure backend is running: http://localhost:8000
2. Make sure frontend is running: http://localhost:3000
3. Try asking a question - it should work now!

## Quick Command Reference

```bash
# Test the key
cd backend
source venv/bin/activate
python simple_key_test.py

# Start backend
uvicorn main:app --reload

# Start frontend (in another terminal)
cd frontend
npm start
```

## Troubleshooting

If the key still shows as invalid:
1. Double-check you copied the ENTIRE key (no missing characters)
2. Make sure no extra spaces in .env file
3. Verify the key starts with `ApiKey-`
4. Try creating a new key if this one doesn't work
