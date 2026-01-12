# PolicyIQ Architecture

## System Overview

PolicyIQ is a full-stack application for regulatory compliance question-answering. It uses an agentic AI approach with RAG (Retrieval-Augmented Generation) to provide accurate, cited answers from regulatory documents.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (React)                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                 │
│  │   Chat   │  │  Upload  │  │  Audit   │                 │
│  │Interface │  │  Interface│  │  Logs    │                 │
│  └────┬─────┘  └────┬──────┘  └────┬─────┘                 │
└───────┼─────────────┼───────────────┼───────────────────────┘
        │             │               │
        └─────────────┴───────────────┘
                      │
        ┌─────────────▼───────────────┐
        │    FastAPI Backend          │
        │  ┌──────────────────────┐   │
        │  │   API Routes         │   │
        │  │  - /documents        │   │
        │  │  - /questions        │   │
        │  │  - /audit            │   │
        │  └──────────┬───────────┘   │
        │             │                │
        │  ┌──────────▼───────────┐   │
        │  │  Agentic Reasoning   │   │
        │  │  - Plan              │   │
        │  │  - Search           │   │
        │  │  - Reason           │   │
        │  │  - Verify           │   │
        │  │  - Respond          │   │
        │  └──────────┬───────────┘   │
        └─────────────┼───────────────┘
                      │
        ┌─────────────┼───────────────┐
        │             │               │
┌───────▼──────┐ ┌───▼──────┐ ┌──────▼──────┐
│  watsonx.ai  │ │ watsonx  │ │  Audit      │
│  (LLM)       │ │ .data    │ │  Logger      │
│              │ │ (Vector) │ │  (SQLite)   │
└──────────────┘ └──────────┘ └─────────────┘
```

## Component Details

### Frontend (React)

**Components:**
- `ChatInterface`: Main Q&A interface with message history
- `DocumentUpload`: PDF upload and document management
- `AuditLogs`: View and filter audit trail

**Features:**
- Real-time chat interface
- Document upload with progress tracking
- Citation display with relevance scores
- Confidence indicators
- Audit log browsing with filters

### Backend (FastAPI)

#### API Layer (`api/routes/`)
- **documents.py**: Document upload, list, delete
- **questions.py**: Question answering endpoint
- **audit.py**: Audit log retrieval

#### Core Components

**1. Ingestion Pipeline (`core/ingestion/`)**
- `pdf_processor.py`: PDF text extraction
- `chunker.py`: Text chunking with overlap
- `document_processor.py`: Complete processing pipeline

**2. RAG Pipeline (`core/rag/`)**
- `hybrid_search.py`: Combines vector and keyword search
- Weighted scoring: 70% vector, 30% keyword

**3. Agentic Reasoning (`core/agent/`)**
- `reasoning_loop.py`: 5-step reasoning process
  - **Plan**: Decompose complex questions
  - **Search**: Hybrid retrieval from watsonx.data
  - **Reason**: LLM generation with context
  - **Verify**: Self-check against sources
  - **Respond**: Format with citations
- `confidence_scorer.py`: Multi-factor confidence calculation

**4. Governance (`core/governance/`)**
- `audit_logger.py`: SQLite-based audit logging
- Tracks: questions, answers, citations, LLM prompts/responses, timestamps

#### Services

**watsonx.ai Client (`services/watsonx_ai/`)**
- LLM text generation
- Embedding generation (with sentence-transformers fallback)
- Context-aware prompting

**watsonx.data Client (`services/watsonx_data/`)**
- Vector storage for embeddings
- Vector similarity search
- Keyword search
- Document chunk management

## Data Flow

### Document Ingestion Flow

```
PDF Upload
    ↓
PDF Text Extraction (pdfplumber/PyPDF2)
    ↓
Text Chunking (with overlap)
    ↓
Embedding Generation (watsonx.ai)
    ↓
Storage in watsonx.data (chunks + embeddings)
    ↓
Document Ready for Querying
```

### Question Answering Flow

```
User Question
    ↓
Agent: Plan (decompose if needed)
    ↓
Agent: Search (hybrid: vector + keyword)
    ↓
Retrieve Top-K Chunks from watsonx.data
    ↓
Agent: Reason (LLM with context)
    ↓
Agent: Verify (self-check)
    ↓
Agent: Respond (format with citations)
    ↓
Confidence Scoring
    ↓
Audit Logging
    ↓
Return Answer to User
```

## Key Design Decisions

### 1. Hybrid Search
- **Why**: Combines semantic understanding (vector) with exact matching (keyword)
- **Benefit**: Better retrieval for both conceptual and specific queries
- **Weighting**: 70% vector, 30% keyword (configurable)

### 2. Agentic Reasoning Loop
- **Why**: Structured approach ensures quality and traceability
- **Benefit**: Each step is logged and can be reviewed
- **Verification**: Self-check step reduces hallucinations

### 3. Confidence Scoring
- **Factors**:
  - Retrieval quality (40%)
  - Answer completeness (30%)
  - Verification support (30%)
- **Threshold**: < 0.7 triggers manual review flag

### 4. Audit Logging
- **Why**: Compliance and governance requirements
- **Storage**: SQLite for development, scalable to PostgreSQL
- **Tracks**: Full interaction history with LLM prompts/responses

### 5. Chunking Strategy
- **Size**: 1000 characters (configurable)
- **Overlap**: 200 characters (configurable)
- **Method**: Paragraph-aware with sentence splitting for long paragraphs

## Configuration

All configuration is managed through environment variables (`.env`):

- **watsonx.ai**: API key, project ID, model selection
- **watsonx.data**: Connection details, database name
- **RAG**: Retrieval parameters, similarity thresholds
- **Confidence**: Scoring thresholds, review flags

## Scalability Considerations

### Current (Development)
- SQLite for audit logs
- In-memory document store
- Single server deployment

### Production Recommendations
- PostgreSQL for audit logs and document metadata
- Redis for caching
- Distributed vector database (watsonx.data)
- Load balancing for API
- CDN for frontend
- Horizontal scaling for ingestion

## Security

- Environment variables for credentials
- CORS configuration
- Input validation (Pydantic)
- SQL injection prevention (parameterized queries)
- File upload validation (PDF only)

## Monitoring & Observability

- Audit logs for all interactions
- Confidence scores for quality tracking
- Manual review flags for low-confidence answers
- API health endpoints
- Error logging

## Future Enhancements

1. **Multi-document Reasoning**: Cross-reference multiple documents
2. **Fine-tuning**: Domain-specific model fine-tuning
3. **Active Learning**: Learn from manual reviews
4. **Version Control**: Track document versions over time
5. **Collaborative Features**: Team annotations and reviews
6. **Advanced Analytics**: Usage patterns, common questions
7. **Multi-language Support**: Process documents in multiple languages
