#!/bin/bash
# Quick validation script - checks API key format and tests validity

cd "$(dirname "$0")"

echo "============================================================"
echo "PolicyIQ Quick Validation"
echo "============================================================"
echo ""

# Check .env exists
if [ ! -f .env ]; then
    echo "✗ .env file not found!"
    echo "  Run: cp env.example .env"
    exit 1
fi

echo "✓ .env file found"
echo ""

# Check API key format
API_KEY=$(grep "^WATSONX_AI_API_KEY=" .env | cut -d'=' -f2- | tr -d '"' | tr -d "'" | xargs)

if [ -z "$API_KEY" ]; then
    echo "✗ WATSONX_AI_API_KEY: NOT SET"
elif [[ "$API_KEY" != "ApiKey-"* ]]; then
    echo "✗ WATSONX_AI_API_KEY: WRONG FORMAT"
    echo "  Current: ${API_KEY:0:30}..."
    echo "  Should start with 'ApiKey-'"
    echo ""
    echo "  Fix: Update .env file to add 'ApiKey-' prefix"
else
    echo "✓ WATSONX_AI_API_KEY: Format correct"
    echo "  Preview: ${API_KEY:0:30}..."
    echo ""
    
    # Test API key
    echo "Testing API key validity..."
    TOKEN_URL="https://iam.cloud.ibm.com/identity/token"
    
    RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$TOKEN_URL" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "apikey=${API_KEY}&grant_type=urn:ibm:params:oauth:grant-type:apikey")
    
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    BODY=$(echo "$RESPONSE" | head -n-1)
    
    if [ "$HTTP_CODE" = "200" ]; then
        if echo "$BODY" | grep -q "access_token"; then
            echo "✓ API Key is VALID!"
            EXPIRES=$(echo "$BODY" | grep -o '"expires_in":[0-9]*' | cut -d':' -f2)
            echo "  Token expires in: ${EXPIRES:-unknown} seconds"
        else
            echo "✗ API Key validation failed"
        fi
    elif [ "$HTTP_CODE" = "401" ]; then
        echo "✗ API Key is INVALID (401 - Authentication failed)"
        echo "  Please check your API key in IBM Cloud"
    elif [ "$HTTP_CODE" = "403" ]; then
        echo "✗ API Key is INVALID (403 - Access forbidden)"
    else
        echo "✗ Unexpected response: HTTP $HTTP_CODE"
    fi
fi

echo ""
echo "============================================================"
echo "Summary"
echo "============================================================"

if [[ "$API_KEY" == "ApiKey-"* ]] && [ "$HTTP_CODE" = "200" ]; then
    echo "✓ API Key is configured correctly and valid!"
    echo ""
    echo "Next steps:"
    echo "1. Restart backend: uvicorn main:app --reload"
    echo "2. Test in frontend at http://localhost:3000"
else
    echo "⚠ API Key needs attention"
    echo "  See output above for details"
fi

echo "============================================================"
