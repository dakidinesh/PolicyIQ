# PolicyIQ Quick Start

Get PolicyIQ running in 5 minutes!

## Prerequisites Check

```bash
python --version  # Should be 3.10+
node --version    # Should be 18+
```

## Quick Setup

### 1. Backend (Terminal 1)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp env.example .env
# Edit .env with your watsonx credentials
uvicorn main:app --reload --port 8000
```

### 2. Frontend (Terminal 2)

```bash
cd frontend
npm install
npm start
```

### 3. Access

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## First Steps

1. **Upload a Document**
   - Go to Upload page
   - Select a PDF (GDPR, PCI-DSS, etc.)
   - Wait for "completed" status

2. **Ask a Question**
   - Go to Chat page
   - Try: "What does PCI-DSS require for cardholder encryption?"
   - View answer with citations and confidence

3. **Check Audit Logs**
   - Go to Audit Logs page
   - See full interaction history

## Sample Questions

See `examples/sample_questions.txt` for more questions to try!

## Troubleshooting

**Backend won't start?**
- Check `.env` file exists and has credentials
- Ensure port 8000 is available

**Frontend can't connect?**
- Verify backend is running
- Check browser console for errors

**No answers?**
- Ensure documents are uploaded and processed
- Check watsonx.ai credentials are correct

For detailed setup, see [SETUP.md](SETUP.md)
