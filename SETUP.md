# PolicyIQ Setup Guide

This guide will help you set up PolicyIQ on your local machine.

## Prerequisites

Before you begin, ensure you have:

1. **Python 3.10+** installed
   ```bash
   python --version
   ```

2. **Node.js 18+** and npm installed
   ```bash
   node --version
   npm --version
   ```

3. **IBM Cloud Account** with access to:
   - watsonx.ai (for LLM and embeddings)
   - watsonx.data (for vector storage)

4. **API Credentials** from IBM Cloud:
   - watsonx.ai API key
   - watsonx.ai Project ID
   - watsonx.data connection details

## Step 1: Clone and Navigate

```bash
cd PolicyIQ
```

## Step 2: Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
```

3. Activate virtual environment:
```bash
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

5. Configure environment variables:
```bash
# Copy the example env file
cp env.example .env

# Edit .env with your actual credentials
# Use your preferred text editor
nano .env  # or vim, code, etc.
```

6. Update `.env` with your credentials:
   - `WATSONX_AI_API_KEY`: Your watsonx.ai API key
   - `WATSONX_AI_PROJECT_ID`: Your watsonx.ai project ID
   - `WATSONX_DATA_URL`: Your watsonx.data URL
   - `WATSONX_DATA_USERNAME`: Your watsonx.data username
   - `WATSONX_DATA_PASSWORD`: Your watsonx.data password

7. Create necessary directories:
```bash
mkdir -p uploads
```

8. Start the backend server:
```bash
uvicorn main:app --reload --port 8000
```

The backend API will be available at `http://localhost:8000`

You can test it by visiting `http://localhost:8000/docs` for the API documentation.

## Step 3: Frontend Setup

1. Open a new terminal window (keep backend running)

2. Navigate to frontend directory:
```bash
cd frontend
```

3. Install Node dependencies:
```bash
npm install
```

4. (Optional) Configure API endpoint:
   - If your backend is not on `http://localhost:8000`, edit `src/services/api.js`
   - Update `API_BASE_URL` or set `REACT_APP_API_URL` environment variable

5. Start the frontend development server:
```bash
npm start
```

The frontend will open automatically at `http://localhost:3000`

## Step 4: Verify Installation

1. **Backend Health Check**:
   - Visit `http://localhost:8000/health`
   - Should return `{"status": "healthy"}`

2. **Frontend**:
   - Should load at `http://localhost:3000`
   - Navigation should show: Chat, Upload, Audit Logs

3. **Upload a Test Document**:
   - Go to Upload page
   - Upload a sample PDF (GDPR, PCI-DSS, etc.)
   - Wait for processing to complete

4. **Ask a Question**:
   - Go to Chat page
   - Ask: "What does PCI-DSS require for cardholder encryption?"
   - Verify answer with citations and confidence score

## Troubleshooting

### Backend Issues

**Import Errors**:
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

**Environment Variable Errors**:
- Check `.env` file exists in `backend/` directory
- Verify all required variables are set
- Restart the server after changing `.env`

**Port Already in Use**:
- Change port in `.env` or use: `uvicorn main:app --port 8001`

### Frontend Issues

**API Connection Errors**:
- Verify backend is running on port 8000
- Check CORS settings in `backend/main.py`
- Verify API URL in `frontend/src/services/api.js`

**Module Not Found**:
- Delete `node_modules` and `package-lock.json`
- Run `npm install` again

### watsonx Integration Issues

**Authentication Errors**:
- Verify API keys are correct
- Check project ID matches your watsonx.ai project
- Ensure credentials have proper permissions

**Embedding Generation**:
- If watsonx.ai embedding API is unavailable, the code falls back to sentence-transformers
- This may require additional model downloads on first use

**Vector Search**:
- Ensure watsonx.data is properly configured
- Verify database connection parameters
- Check that vector indexes are created

## Next Steps

1. **Upload Documents**: Add your regulatory documents (GDPR, SOC2, PCI-DSS)
2. **Test Questions**: Use sample questions from `examples/sample_questions.txt`
3. **Review Audit Logs**: Check the audit log page for full traceability
4. **Customize**: Adjust confidence thresholds and RAG parameters in `.env`

## Production Deployment

For production deployment:

1. Set `DEBUG=False` in `.env`
2. Use a production WSGI server (e.g., Gunicorn)
3. Configure proper database (PostgreSQL, etc.) instead of SQLite
4. Set up proper authentication and authorization
5. Use environment-specific configuration
6. Enable HTTPS
7. Set up monitoring and logging

## Support

For issues or questions:
- Check the main README.md
- Review API documentation at `/docs` endpoint
- Check example questions in `examples/` directory
