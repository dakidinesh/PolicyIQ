#!/bin/bash
# Run comprehensive tests for PolicyIQ

cd "$(dirname "$0")"

echo "============================================================"
echo "PolicyIQ Comprehensive Test Suite"
echo "============================================================"
echo ""

# Check if venv is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠ Virtual environment not activated"
    echo "  Activating venv..."
    if [ -d "venv" ]; then
        source venv/bin/activate
    else
        echo "✗ venv not found. Run: python3 -m venv venv"
        exit 1
    fi
fi

echo "✓ Virtual environment: $(which python)"
echo ""

# Run the test script
python test_everything.py

echo ""
echo "============================================================"
echo "Test Complete"
echo "============================================================"
