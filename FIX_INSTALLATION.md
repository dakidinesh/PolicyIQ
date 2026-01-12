# Fixing Installation Issues

## Issue: Package Version Errors

You encountered an error because:
1. `ibm-watson-machine-learning==1.0.19` doesn't exist
2. Some packages may have Python 3.10+ requirements

## Solution

I've updated `requirements.txt` to use `ibm-watson-machine-learning>=1.0.333` (latest available version).

### Try Installing Again

```bash
cd /Users/dakidinesh/Documents/PolicyIQ/backend
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## If You Still Get Python Version Errors

You're using **Python 3.9.6**, but some packages prefer Python 3.10+. You have two options:

### Option 1: Upgrade Python (Recommended)

Install Python 3.10 or higher:

**macOS (using Homebrew):**
```bash
brew install python@3.11
# Then recreate venv
cd backend
rm -rf venv
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Or download from:** https://www.python.org/downloads/

### Option 2: Use Compatible Versions (Workaround)

If you must use Python 3.9, try installing with relaxed version constraints:

```bash
cd /Users/dakidinesh/Documents/PolicyIQ/backend
source venv/bin/activate

# Install core packages first
pip install fastapi uvicorn pydantic pydantic-settings python-dotenv
pip install PyPDF2 pdfplumber
pip install ibm-watson-machine-learning ibm-cloud-sdk-core
pip install requests numpy sentence-transformers
pip install python-multipart aiofiles sqlalchemy
pip install pytest pytest-asyncio black isort
```

## Common Errors and Fixes

### Error: "Requires-Python >=3.10"

**Fix:** Upgrade to Python 3.10+ or install packages individually with compatible versions.

### Error: "No matching distribution found"

**Fix:** 
```bash
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt
```

### Error: "ibm-watson-machine-learning version not found"

**Fix:** The version has been updated to `>=1.0.333`. If still failing:
```bash
pip install ibm-watson-machine-learning --upgrade
```

## Verify Installation

After installation, verify:

```bash
cd /Users/dakidinesh/Documents/PolicyIQ/backend
source venv/bin/activate
python -c "import fastapi; print('✓ FastAPI')"
python -c "import ibm_watson_machine_learning; print('✓ IBM WML')"
python -c "import pdfplumber; print('✓ pdfplumber')"
```

## Next Steps

Once installation succeeds:

1. **Start Backend:**
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn main:app --reload --port 8000
   ```

2. **Start Frontend** (in another terminal):
   ```bash
   cd frontend
   npm start
   ```
