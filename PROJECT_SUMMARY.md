# PolicyIQ Project Summary

## Project Overview

PolicyIQ is a full-stack Regulatory Compliance QA Agent designed for banking and finance organizations. It provides natural-language question answering with cited sources, confidence estimates, and full audit traceability.

## Project Structure

```
PolicyIQ/
├── backend/                    # FastAPI backend
│   ├── api/                   # API routes
│   │   └── routes/
│   │       ├── documents.py   # Document management
│   │       ├── questions.py   # Q&A endpoint
│   │       └── audit.py       # Audit logs
│   ├── core/                  # Core business logic
│   │   ├── agent/            # Agentic reasoning
│   │   │   ├── reasoning_loop.py
│   │   │   └── confidence_scorer.py
│   │   ├── ingestion/        # Document processing
│   │   │   ├── pdf_processor.py
│   │   │   ├── chunker.py
│   │   │   └── document_processor.py
│   │   ├── rag/              # RAG pipeline
│   │   │   └── hybrid_search.py
│   │   ├── governance/       # Audit logging
│   │   │   └── audit_logger.py
│   │   └── config.py         # Configuration
│   ├── models/               # Data models
│   │   └── schemas.py
│   ├── services/             # External services
│   │   ├── watsonx_ai/      # watsonx.ai client
│   │   └── watsonx_data/    # watsonx.data client
│   ├── main.py              # FastAPI app
│   ├── requirements.txt     # Python dependencies
│   └── env.example          # Environment template
│
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── ChatInterface.js
│   │   │   ├── DocumentUpload.js
│   │   │   └── AuditLogs.js
│   │   ├── services/        # API client
│   │   │   └── api.js
│   │   └── App.js           # Main app
│   └── package.json         # Node dependencies
│
├── examples/                 # Sample files
│   ├── sample_questions.txt
│   └── README.md
│
├── README.md                 # Main documentation
├── SETUP.md                  # Detailed setup guide
├── QUICKSTART.md            # Quick start guide
├── ARCHITECTURE.md          # Architecture documentation
└── .gitignore               # Git ignore rules
```

## Key Features Implemented

### ✅ Document Ingestion
- PDF text extraction (pdfplumber/PyPDF2)
- Intelligent text chunking with overlap
- Embedding generation (watsonx.ai with fallback)
- Storage in watsonx.data

### ✅ Question Answering
- Natural language question processing
- Hybrid search (vector + keyword)
- LLM-powered answer generation
- Citation extraction
- Confidence scoring

### ✅ Agentic Reasoning Loop
- **Plan**: Question decomposition
- **Search**: Hybrid retrieval
- **Reason**: LLM reasoning with context
- **Verify**: Self-check against sources
- **Respond**: Formatted answer with citations

### ✅ Governance & Auditability
- Complete audit logging (SQLite)
- LLM prompt/response tracking
- Source document tracking
- Confidence score logging
- Manual review flags

### ✅ Frontend UI
- Chat interface for Q&A
- Document upload interface
- Audit log viewer with filters
- Citation display
- Confidence indicators

## Technology Stack

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.10+
- **PDF Processing**: PyPDF2, pdfplumber
- **LLM**: IBM watsonx.ai
- **Vector DB**: IBM watsonx.data
- **Embeddings**: watsonx.ai (with sentence-transformers fallback)
- **Audit Logs**: SQLite (development)

### Frontend
- **Framework**: React 18
- **HTTP Client**: Axios
- **Routing**: React Router
- **Styling**: CSS (custom)

## Configuration

All configuration via environment variables (`.env`):
- watsonx.ai credentials
- watsonx.data connection
- RAG parameters
- Confidence thresholds
- Chunking parameters

## API Endpoints

### Documents
- `POST /api/v1/documents/upload` - Upload PDF
- `GET /api/v1/documents/` - List documents
- `GET /api/v1/documents/{id}` - Get document
- `DELETE /api/v1/documents/{id}` - Delete document

### Questions
- `POST /api/v1/questions/ask` - Ask question

### Audit
- `GET /api/v1/audit/logs` - Get audit logs (with filters)
- `GET /api/v1/audit/logs/{id}` - Get specific log

## Usage Workflow

1. **Setup**: Configure watsonx credentials in `.env`
2. **Upload**: Upload regulatory PDFs (GDPR, PCI-DSS, SOC2)
3. **Process**: Documents are automatically chunked and embedded
4. **Query**: Ask natural language questions
5. **Review**: Check answers with citations and confidence
6. **Audit**: Review full interaction history

## Example Questions

- "Does policy allow storing customer data outside the US?"
- "What does PCI-DSS require for cardholder encryption?"
- "What are the GDPR requirements for data breach notification?"

See `examples/sample_questions.txt` for more.

## Next Steps for Production

1. **Database**: Migrate from SQLite to PostgreSQL
2. **Authentication**: Add user authentication/authorization
3. **Deployment**: Containerize with Docker
4. **Monitoring**: Add logging and monitoring
5. **Testing**: Add unit and integration tests
6. **Documentation**: API documentation with examples
7. **CI/CD**: Set up continuous integration

## Development Status

✅ **Complete**: Core functionality implemented
✅ **Complete**: Frontend UI
✅ **Complete**: Backend API
✅ **Complete**: Document ingestion
✅ **Complete**: RAG pipeline
✅ **Complete**: Agentic reasoning
✅ **Complete**: Audit logging
✅ **Complete**: Documentation

⚠️ **Needs Configuration**: watsonx.ai and watsonx.data credentials
⚠️ **Needs Testing**: End-to-end testing with actual watsonx services
⚠️ **Placeholder**: Some watsonx API calls need actual implementation

## Notes

- watsonx.ai and watsonx.data clients include placeholder implementations
- Actual API calls need to be implemented based on current watsonx API documentation
- Embedding generation falls back to sentence-transformers if watsonx.ai unavailable
- SQLite used for audit logs (development); should migrate to PostgreSQL for production

## Support

- Main README: `README.md`
- Setup Guide: `SETUP.md`
- Quick Start: `QUICKSTART.md`
- Architecture: `ARCHITECTURE.md`
