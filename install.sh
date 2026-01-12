#!/bin/bash

# PolicyIQ Installation Script
# This script installs all dependencies for PolicyIQ

set -e

echo "🚀 PolicyIQ Installation Script"
echo "================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python
echo "📦 Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10+ first."
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo "✓ Found: $PYTHON_VERSION"
echo ""

# Check Node.js
echo "📦 Checking Node.js..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi
NODE_VERSION=$(node --version)
echo "✓ Found: $NODE_VERSION"
echo ""

# Backend Installation
echo "🔧 Installing Backend Dependencies..."
echo "--------------------------------------"
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment and install dependencies
echo "Installing Python packages..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✓ Backend dependencies installed${NC}"
deactivate

cd ..
echo ""

# Frontend Installation
echo "🔧 Installing Frontend Dependencies..."
echo "--------------------------------------"
cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installing Node.js packages..."
    npm install
    echo -e "${GREEN}✓ Frontend dependencies installed${NC}"
else
    echo "✓ Frontend dependencies already installed"
fi

cd ..
echo ""

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p backend/uploads
echo "✓ Created backend/uploads directory"
echo ""

# Verify .env file
echo "🔐 Checking configuration..."
if [ -f "backend/.env" ]; then
    echo -e "${GREEN}✓ .env file found${NC}"
else
    echo -e "${YELLOW}⚠ .env file not found. Please copy env.example to .env and fill in your credentials.${NC}"
fi
echo ""

echo "✅ Installation Complete!"
echo ""
echo "Next steps:"
echo "1. Make sure backend/.env is configured with your watsonx credentials"
echo "2. Start the backend: cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo "3. Start the frontend: cd frontend && npm start"
echo ""
