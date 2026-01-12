# PolicyIQ Installation Guide

Since automated installation is restricted, please run these commands manually in your terminal.

## Quick Installation

### Option 1: Use the Installation Script

```bash
cd /Users/dakidinesh/Documents/PolicyIQ
chmod +x install.sh
./install.sh
```

### Option 2: Manual Installation

Follow the steps below.

## Step-by-Step Installation

### 1. Backend Installation

Open a terminal and run:

```bash
# Navigate to backend directory
cd /Users/dakidinesh/Documents/PolicyIQ/backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Create uploads directory
mkdir -p uploads

# Deactivate virtual environment (optional)
deactivate
```

**Note**: If `python3 -m venv` fails, try:
- `python3 -m virtualenv venv` (if virtualenv is installed)
- Or use `python` instead of `python3` if that's your Python command

### 2. Frontend Installation

Open a **new terminal** (keep backend terminal open if you want to run it later):

```bash
# Navigate to frontend directory
cd /Users/dakidinesh/Documents/PolicyIQ/frontend

# Install Node.js dependencies
npm install
```

### 3. Verify Installation

#### Check Backend:

```bash
cd /Users/dakidinesh/Documents/PolicyIQ/backend
source venv/bin/activate
python -c "import fastapi; print('✓ FastAPI installed')"
python -c "import uvicorn; print('✓ Uvicorn installed')"
deactivate
```

#### Check Frontend:

```bash
cd /Users/dakidinesh/Documents/PolicyIQ/frontend
ls node_modules | head -5
# Should show installed packages
```

### 4. Verify Configuration

Make sure your `.env` file exists and has all credentials:

```bash
cd /Users/dakidinesh/Documents/PolicyIQ/backend
cat .env | grep -E "WATSONX|DATABASE"
# Should show your API keys and configuration
```

## Starting the Application

### Terminal 1: Backend

```bash
cd /Users/dakidinesh/Documents/PolicyIQ/backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### Terminal 2: Frontend

```bash
cd /Users/dakidinesh/Documents/PolicyIQ/frontend
npm start
```

The browser should automatically open to `http://localhost:3000`

## Troubleshooting

### Python Virtual Environment Issues

**Problem**: `python3 -m venv` fails with permission error

**Solution**:
```bash
# Try using python instead
python -m venv venv

# Or install virtualenv first
pip3 install --user virtualenv
python3 -m virtualenv venv
```

### pip Installation Fails

**Problem**: Permission errors or SSL errors

**Solution**:
```bash
# Use user installation
pip3 install --user -r requirements.txt

# Or use sudo (not recommended but works)
sudo pip3 install -r requirements.txt
```

### Node.js Installation Issues

**Problem**: npm install fails

**Solution**:
```bash
# Clear npm cache
npm cache clean --force

# Try with verbose logging
npm install --verbose

# Or use yarn instead
yarn install
```

### Module Not Found Errors

**Problem**: Python can't find installed packages

**Solution**:
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall packages
pip install -r requirements.txt
```

### Port Already in Use

**Problem**: Port 8000 or 3000 already in use

**Solution**:
```bash
# Backend - use different port
uvicorn main:app --reload --port 8001

# Frontend - edit package.json or use:
PORT=3001 npm start
```

## Verification Checklist

After installation, verify:

- [ ] Backend virtual environment created (`backend/venv/` exists)
- [ ] Python packages installed (run `pip list` in venv)
- [ ] Frontend node_modules exists (`frontend/node_modules/` exists)
- [ ] `.env` file configured with API keys
- [ ] `uploads` directory created (`backend/uploads/` exists)
- [ ] Backend starts without errors
- [ ] Frontend starts without errors

## Next Steps

1. **Test Backend**: Visit http://localhost:8000/docs (API documentation)
2. **Test Frontend**: Visit http://localhost:3000
3. **Upload a Document**: Go to Upload page and upload a PDF
4. **Ask a Question**: Go to Chat page and try a sample question

## Need Help?

- Check the main README.md
- See SETUP.md for detailed setup
- Review GETTING_CREDENTIALS.md for API key setup
