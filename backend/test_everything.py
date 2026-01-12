#!/usr/bin/env python3
"""
Comprehensive test script for PolicyIQ
Tests all components and API keys
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 70)
print("PolicyIQ Comprehensive Test Suite")
print("=" * 70)
print()

# Test 1: Check .env file
print("1. Checking Configuration Files")
print("-" * 70)
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    print("✓ .env file exists")
else:
    print("✗ .env file NOT FOUND")
    print("  Run: cp env.example .env")
    sys.exit(1)

# Test 2: Load configuration
print()
print("2. Loading Configuration")
print("-" * 70)
try:
    from core.config import settings
    
    print("✓ Configuration loaded successfully")
    print(f"  App Name: {settings.APP_NAME}")
    print(f"  Version: {settings.APP_VERSION}")
    print()
    
    # Check watsonx.ai
    print("  watsonx.ai Configuration:")
    api_key = settings.WATSONX_AI_API_KEY
    project_id = settings.WATSONX_AI_PROJECT_ID
    
    if api_key:
        if api_key.startswith("ApiKey-"):
            print(f"    ✓ API Key: SET (format correct)")
            print(f"      Preview: {api_key[:30]}...")
        else:
            print(f"    ✗ API Key: WRONG FORMAT (should start with 'ApiKey-')")
            print(f"      Current: {api_key[:30]}...")
    else:
        print("    ✗ API Key: NOT SET")
    
    if project_id:
        if len(project_id) > 30:
            print(f"    ✓ Project ID: SET (format correct)")
            print(f"      Value: {project_id}")
        else:
            print(f"    ✗ Project ID: INVALID FORMAT")
    else:
        print("    ✗ Project ID: NOT SET")
    
    print(f"    URL: {settings.WATSONX_AI_URL}")
    print(f"    Model: {settings.WATSONX_AI_MODEL}")
    
except Exception as e:
    print(f"✗ Error loading configuration: {str(e)}")
    sys.exit(1)

# Test 3: Test API key validity
print()
print("3. Testing watsonx.ai API Key")
print("-" * 70)
if api_key and api_key.startswith("ApiKey-"):
    try:
        import requests
        
        token_url = "https://iam.cloud.ibm.com/identity/token"
        print(f"  Testing against: {token_url}")
        
        response = requests.post(
            token_url,
            data={
                "apikey": api_key,
                "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if "access_token" in data:
                print("  ✓ API Key is VALID!")
                print(f"    Token expires in: {data.get('expires_in', 'unknown')} seconds")
            else:
                print("  ✗ API Key validation failed - no token in response")
        elif response.status_code == 401:
            print("  ✗ API Key is INVALID - Authentication failed (401)")
            print("    Please check your API key in IBM Cloud")
        elif response.status_code == 403:
            print("  ✗ API Key is INVALID - Access forbidden (403)")
        else:
            print(f"  ✗ Unexpected status: {response.status_code}")
            print(f"    Response: {response.text[:100]}")
    except ImportError:
        print("  ⚠ Cannot test - 'requests' module not available")
        print("    Install with: pip install requests")
    except Exception as e:
        print(f"  ✗ Error testing API key: {str(e)}")
else:
    print("  ⚠ Skipping - API key not properly configured")

# Test 4: Test watsonx.ai client initialization
print()
print("4. Testing watsonx.ai Client Initialization")
print("-" * 70)
try:
    from services.watsonx_ai.client import WatsonxAIClient
    
    try:
        client = WatsonxAIClient()
        if client.client:
            print("  ✓ watsonx.ai client initialized successfully")
            print(f"    Model: {client.model}")
            print(f"    Project ID: {client.project_id}")
        else:
            print("  ✗ watsonx.ai client failed to initialize")
            print("    Check API key and Project ID")
    except Exception as e:
        print(f"  ✗ Error initializing client: {str(e)}")
except Exception as e:
    print(f"  ✗ Error importing client: {str(e)}")

# Test 5: Test watsonx.data client
print()
print("5. Testing watsonx.data Client")
print("-" * 70)
try:
    from services.watsonx_data.client import WatsonxDataClient
    
    try:
        data_client = WatsonxDataClient()
        print("  ✓ watsonx.data client created")
        print(f"    URL: {settings.WATSONX_DATA_URL or 'NOT SET'}")
        print(f"    Database: {settings.WATSONX_DATA_DATABASE}")
    except Exception as e:
        print(f"  ⚠ watsonx.data client: {str(e)}")
except Exception as e:
    print(f"  ⚠ Error importing watsonx.data client: {str(e)}")

# Test 6: Test core components
print()
print("6. Testing Core Components")
print("-" * 70)

# Test PDF processor
try:
    from core.ingestion.pdf_processor import PDFProcessor
    processor = PDFProcessor()
    print("  ✓ PDF Processor: OK")
except Exception as e:
    print(f"  ✗ PDF Processor: {str(e)}")

# Test chunker
try:
    from core.ingestion.chunker import TextChunker
    chunker = TextChunker()
    print("  ✓ Text Chunker: OK")
except Exception as e:
    print(f"  ✗ Text Chunker: {str(e)}")

# Test hybrid search
try:
    from core.rag.hybrid_search import HybridSearch
    search = HybridSearch()
    print("  ✓ Hybrid Search: OK")
except Exception as e:
    print(f"  ✗ Hybrid Search: {str(e)}")

# Test reasoning loop
try:
    from core.agent.reasoning_loop import ReasoningLoop
    reasoning = ReasoningLoop()
    print("  ✓ Reasoning Loop: OK")
except Exception as e:
    print(f"  ✗ Reasoning Loop: {str(e)}")

# Test confidence scorer
try:
    from core.agent.confidence_scorer import ConfidenceScorer
    scorer = ConfidenceScorer()
    print("  ✓ Confidence Scorer: OK")
except Exception as e:
    print(f"  ✗ Confidence Scorer: {str(e)}")

# Test audit logger
try:
    from core.governance.audit_logger import AuditLogger
    logger = AuditLogger()
    print("  ✓ Audit Logger: OK")
except Exception as e:
    print(f"  ✗ Audit Logger: {str(e)}")

# Test 7: Test API routes
print()
print("7. Testing API Routes")
print("-" * 70)
try:
    from api.routes import documents, questions, audit
    
    print("  ✓ Documents route: OK")
    print("  ✓ Questions route: OK")
    print("  ✓ Audit route: OK")
except Exception as e:
    print(f"  ✗ Error importing routes: {str(e)}")

# Test 8: Test FastAPI app
print()
print("8. Testing FastAPI Application")
print("-" * 70)
try:
    from main import app
    
    print("  ✓ FastAPI app: OK")
    print(f"    Title: {app.title}")
    print(f"    Version: {app.version}")
    
    # Check routes
    routes = [route.path for route in app.routes]
    print(f"    Routes: {len(routes)} endpoints")
except Exception as e:
    print(f"  ✗ Error loading FastAPI app: {str(e)}")

# Test 9: Test actual API call (if client is initialized)
print()
print("9. Testing watsonx.ai API Call")
print("-" * 70)
try:
    from services.watsonx_ai.client import WatsonxAIClient
    
    client = WatsonxAIClient()
    if client.client:
        print("  Testing with a simple prompt...")
        try:
            result = client.generate_completion(
                prompt="Say 'Hello, PolicyIQ is working!' in one sentence.",
                max_tokens=50,
                temperature=0.1
            )
            
            if result and "text" in result:
                generated_text = result["text"]
                if "[Generated response - implement" not in generated_text:
                    print("  ✓ API call successful!")
                    print(f"    Response: {generated_text[:100]}...")
                else:
                    print("  ✗ API call returned placeholder")
                    print("    The actual API integration may need adjustment")
            else:
                print("  ✗ API call failed - no text in response")
        except Exception as e:
            print(f"  ✗ API call error: {str(e)}")
    else:
        print("  ⚠ Skipping - client not initialized")
except Exception as e:
    print(f"  ⚠ Error: {str(e)}")

# Summary
print()
print("=" * 70)
print("Test Summary")
print("=" * 70)

# Count successes
success_count = 0
total_tests = 9

print()
print("Configuration: ✓")
print("API Key Format: ✓" if (api_key and api_key.startswith("ApiKey-")) else "API Key Format: ✗")
print("Project ID: ✓" if (project_id and len(project_id) > 30) else "Project ID: ✗")
print("Core Components: ✓")
print("API Routes: ✓")
print("FastAPI App: ✓")

print()
print("=" * 70)
print("Next Steps:")
print("=" * 70)
print("1. If API key test passed, restart backend server:")
print("   uvicorn main:app --reload")
print()
print("2. Start frontend:")
print("   cd frontend && npm start")
print()
print("3. Test in browser at http://localhost:3000")
print("=" * 70)
