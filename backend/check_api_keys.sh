#!/bin/bash
# Quick script to check API keys format and validity

echo "============================================================"
echo "PolicyIQ API Keys Validation"
echo "============================================================"
echo ""

cd "$(dirname "$0")"

# Check if .env exists
if [ ! -f .env ]; then
    echo "✗ ERROR: .env file not found!"
    echo "  Run: cp env.example .env"
    exit 1
fi

echo "✓ .env file found"
echo ""

# Check watsonx.ai credentials
echo "1. Checking watsonx.ai Credentials"
echo "------------------------------------------------------------"

API_KEY=$(grep "^WATSONX_AI_API_KEY=" .env | cut -d'=' -f2- | tr -d '"' | tr -d "'")
PROJECT_ID=$(grep "^WATSONX_AI_PROJECT_ID=" .env | cut -d'=' -f2- | tr -d '"' | tr -d "'")
URL=$(grep "^WATSONX_AI_URL=" .env | cut -d'=' -f2- | tr -d '"' | tr -d "'")

if [ -z "$API_KEY" ]; then
    echo "✗ WATSONX_AI_API_KEY: NOT SET"
elif [[ "$API_KEY" == *"your_watsonx_ai_api_key_here"* ]] || [[ "$API_KEY" != "ApiKey-"* ]]; then
    echo "✗ WATSONX_AI_API_KEY: INVALID FORMAT"
    echo "  Current: ${API_KEY:0:30}..."
    echo "  Should start with 'ApiKey-'"
else
    echo "✓ WATSONX_AI_API_KEY: SET (format looks correct)"
    echo "  Preview: ${API_KEY:0:25}..."
    
    # Test API key
    echo "  Testing API key validity..."
    TOKEN_RESPONSE=$(curl -s -X POST "${URL}/v1/identity/token" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "apikey=${API_KEY}&grant_type=urn:ibm:params:oauth:grant-type:apikey" \
        -w "\n%{http_code}")
    
    HTTP_CODE=$(echo "$TOKEN_RESPONSE" | tail -n1)
    RESPONSE_BODY=$(echo "$TOKEN_RESPONSE" | head -n-1)
    
    if [ "$HTTP_CODE" = "200" ]; then
        if echo "$RESPONSE_BODY" | grep -q "access_token"; then
            echo "  ✓ API Key is VALID - Successfully obtained access token"
            EXPIRES=$(echo "$RESPONSE_BODY" | grep -o '"expires_in":[0-9]*' | cut -d':' -f2)
            if [ -n "$EXPIRES" ]; then
                echo "    Token expires in: $EXPIRES seconds"
            fi
        else
            echo "  ✗ API Key validation FAILED - No token in response"
        fi
    elif [ "$HTTP_CODE" = "401" ]; then
        echo "  ✗ API Key is INVALID - Authentication failed (401)"
        echo "    Please check your API key in IBM Cloud"
    elif [ "$HTTP_CODE" = "403" ]; then
        echo "  ✗ API Key is INVALID - Access forbidden (403)"
        echo "    API key may not have required permissions"
    else
        echo "  ⚠ API Key validation returned status $HTTP_CODE"
        echo "    Response: ${RESPONSE_BODY:0:100}..."
    fi
fi

if [ -z "$PROJECT_ID" ]; then
    echo "✗ WATSONX_AI_PROJECT_ID: NOT SET"
elif [[ "$PROJECT_ID" == *"your_project_id_here"* ]] || [ ${#PROJECT_ID} -lt 30 ]; then
    echo "✗ WATSONX_AI_PROJECT_ID: INVALID FORMAT"
    echo "  Current: $PROJECT_ID"
    echo "  Should be a UUID (36 characters)"
else
    echo "✓ WATSONX_AI_PROJECT_ID: SET (format looks correct)"
    echo "  Value: $PROJECT_ID"
fi

echo "  URL: ${URL:-'NOT SET'}"
echo ""

# Check watsonx.data credentials
echo "2. Checking watsonx.data Credentials"
echo "------------------------------------------------------------"

DATA_URL=$(grep "^WATSONX_DATA_URL=" .env | cut -d'=' -f2- | tr -d '"' | tr -d "'")
DATA_USERNAME=$(grep "^WATSONX_DATA_USERNAME=" .env | cut -d'=' -f2- | tr -d '"' | tr -d "'")
DATA_PASSWORD=$(grep "^WATSONX_DATA_PASSWORD=" .env | cut -d'=' -f2- | tr -d '"' | tr -d "'")

if [ -z "$DATA_URL" ]; then
    echo "✗ WATSONX_DATA_URL: NOT SET"
elif [[ "$DATA_URL" == *"your_watsonx_data_url_here"* ]] || [[ "$DATA_URL" != "https://"* ]]; then
    echo "✗ WATSONX_DATA_URL: INVALID FORMAT"
    echo "  Current: $DATA_URL"
    echo "  Should be a full URL starting with https://"
else
    echo "✓ WATSONX_DATA_URL: SET"
    echo "  Value: $DATA_URL"
fi

if [ -z "$DATA_USERNAME" ]; then
    echo "✗ WATSONX_DATA_USERNAME: NOT SET"
elif [[ "$DATA_USERNAME" == *"your_username_here"* ]]; then
    echo "✗ WATSONX_DATA_USERNAME: USING PLACEHOLDER"
else
    echo "✓ WATSONX_DATA_USERNAME: SET"
    echo "  Value: $DATA_USERNAME"
fi

if [ -z "$DATA_PASSWORD" ]; then
    echo "✗ WATSONX_DATA_PASSWORD: NOT SET"
elif [[ "$DATA_PASSWORD" == *"your_password_here"* ]]; then
    echo "✗ WATSONX_DATA_PASSWORD: USING PLACEHOLDER"
else
    echo "✓ WATSONX_DATA_PASSWORD: SET"
    PASSWORD_LEN=${#DATA_PASSWORD}
    echo "  Value: $(printf '*%.0s' {1..$PASSWORD_LEN})"
fi

echo ""

# Summary
echo "============================================================"
echo "Summary"
echo "============================================================"

AI_READY=false
DATA_READY=false

if [ -n "$API_KEY" ] && [[ "$API_KEY" == "ApiKey-"* ]] && \
   [ -n "$PROJECT_ID" ] && [ ${#PROJECT_ID} -gt 30 ] && \
   [[ "$API_KEY" != *"your_"* ]] && [[ "$PROJECT_ID" != *"your_"* ]]; then
    AI_READY=true
fi

if [ -n "$DATA_URL" ] && [[ "$DATA_URL" == "https://"* ]] && \
   [ -n "$DATA_USERNAME" ] && [[ "$DATA_USERNAME" != *"your_"* ]] && \
   [ -n "$DATA_PASSWORD" ] && [[ "$DATA_PASSWORD" != *"your_"* ]]; then
    DATA_READY=true
fi

if [ "$AI_READY" = true ]; then
    echo "✓ watsonx.ai: Credentials configured"
else
    echo "✗ watsonx.ai: Credentials missing or invalid"
fi

if [ "$DATA_READY" = true ]; then
    echo "✓ watsonx.data: Credentials configured"
else
    echo "✗ watsonx.data: Credentials missing or invalid"
fi

echo ""

if [ "$AI_READY" = true ] && [ "$DATA_READY" = true ]; then
    echo "🎉 All credentials are properly configured!"
elif [ "$AI_READY" = true ]; then
    echo "⚠ watsonx.ai is ready, but watsonx.data needs configuration"
else
    echo "❌ Credentials need to be configured"
    echo "   See FIX_CREDENTIALS.md for help"
fi

echo "============================================================"
