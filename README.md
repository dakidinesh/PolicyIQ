# PolicyIQ: Regulatory Compliance QA Agent

PolicyIQ is an enterprise-grade Regulatory Compliance QA Agent designed for banking and finance organizations. It ingests regulatory documents (GDPR, SOC2, PCI-DSS, internal policies) and provides natural-language question answering with cited sources, confidence estimates, and full audit traceability.

## Architecture Overview

PolicyIQ follows a modular architecture with clear separation of concerns:

```
PolicyIQ/
├── backend/              # FastAPI backend service
│   ├── api/             # API routes and endpoints
│   ├── core/            # Core business logic
│   │   ├── agent/       # Agentic reasoning loop
│   │   ├── ingestion/   # PDF processing and chunking
│   │   ├── rag/         # RAG pipeline (hybrid search)
│   │   └── governance/  # Audit logging and governance
│   ├── models/          # Data models and schemas
│   └── services/        # External service integrations
│       ├── watsonx_ai/  # IBM watsonx.ai LLM integration
│       └── watsonx_data/# IBM watsonx.data storage
├── frontend/            # React frontend application
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── services/    # API client services
│   │   └── utils/       # Utility functions
├── examples/            # Sample PDFs and questions
└── docs/                # Additional documentation
```

## Core Components

### 1. Document Ingestion Pipeline
- **PDF Processing**: Extracts text from PDF documents using PyPDF2/pdfplumber
- **Text Chunking**: Splits documents into semantically meaningful chunks with overlap
- **Embedding Generation**: Creates vector embeddings using watsonx.ai embedding models
- **Storage**: Stores chunks and embeddings in watsonx.data with metadata

### 2. RAG Pipeline (Hybrid Search)
- **Vector Similarity**: Semantic search using embeddings stored in watsonx.data
- **Keyword Search**: Traditional keyword matching for exact term retrieval
- **Hybrid Ranking**: Combines vector and keyword scores for optimal retrieval
- **Relevance Filtering**: Filters results by relevance threshold

### 3. Agentic Reasoning Loop
The agent follows a structured reasoning process:

1. **Plan**: Decomposes user question into sub-queries
2. **Search**: Queries watsonx.data using hybrid search
3. **Reason**: Uses watsonx.ai LLM to analyze retrieved context
4. **Verify**: Self-checks answer against source documents
5. **Respond**: Generates final answer with citations and confidence

### 4. Governance & Auditability
- **Audit Logging**: Records all interactions with timestamps
- **Prompt/Response Logging**: Stores LLM prompts and responses
- **Source Tracking**: Tracks document versions and sections used
- **Confidence Scoring**: Provides confidence estimates for answers
- **Manual Review Flags**: Flags low-confidence answers for review

## Technology Stack

### Backend
- **Python 3.10+**
- **FastAPI**: REST API framework
- **PyPDF2/pdfplumber**: PDF text extraction
- **IBM watsonx.ai**: LLM and embedding models
- **IBM watsonx.data**: Vector database and document storage
- **Pydantic**: Data validation and models

### Frontend
- **React 18+**: UI framework
- **TypeScript**: Type safety
- **Axios**: HTTP client
- **Tailwind CSS**: Styling (optional)

## Setup Instructions

### Prerequisites
1. Python 3.10 or higher
2. Node.js 18+ and npm
3. IBM Cloud account with watsonx.ai and watsonx.data access
4. API credentials for watsonx services

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your watsonx credentials
```

5. Run the FastAPI server:
```bash
uvicorn main:app --reload --port 8000
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Configure API endpoint (if different from default):
```bash
# Edit src/config.ts if needed
```

4. Start development server:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

### watsonx Configuration

1. **watsonx.ai Setup**:
   - Obtain API key from IBM Cloud
   - Set `WATSONX_AI_API_KEY` in `.env`
   - Set `WATSONX_AI_URL` (e.g., `https://us-south.ml.cloud.ibm.com`)

2. **watsonx.data Setup**:
   - Create a watsonx.data instance
   - Configure connection parameters
   - Set `WATSONX_DATA_URL`, `WATSONX_DATA_USERNAME`, `WATSONX_DATA_PASSWORD` in `.env`

## Usage

### Uploading Documents

1. Navigate to the upload section in the UI
2. Select PDF files (GDPR, SOC2, PCI-DSS, etc.)
3. Documents are automatically processed and indexed

### Asking Questions

1. Type your question in the chat interface
2. Examples:
   - "Does policy allow storing customer data outside the US?"
   - "What does PCI-DSS require for cardholder encryption?"
   - "What are the GDPR requirements for data breach notification?"
3. View the answer with:
   - Direct conclusion
   - Explanation
   - Cited regulation sections
   - Confidence score

### Viewing Audit Logs

1. Navigate to the audit log section
2. View all interactions with:
   - Timestamps
   - Questions asked
   - Sources retrieved
   - LLM prompts/responses
   - Confidence scores

## Example Questions

See `/examples/sample_questions.txt` for a comprehensive list of example questions covering:
- GDPR compliance
- PCI-DSS requirements
- SOC2 controls
- Data residency policies
- Encryption standards

## Security & Compliance

- All API communications use HTTPS
- Credentials stored in environment variables
- Audit logs provide full traceability
- Low-confidence answers flagged for manual review
- Document versioning for compliance tracking

## Development

### Running Tests
```bash
cd backend
pytest tests/
```

### Code Formatting
```bash
cd backend
black .
isort .
```

## License

Enterprise License - Internal Use Only

## Support

For issues or questions, contact the PolicyIQ development team.
