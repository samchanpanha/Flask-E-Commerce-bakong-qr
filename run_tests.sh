#!/bin/bash

# Run Tests Script for Flask E-Commerce with Bakong KHQR

echo "🧪 Running Tests for Flask E-Commerce..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Install the local bakong_khqr package
echo "📦 Installing local bakong_khqr package..."
pip install -e .

# Run the tests
echo "🧪 Running pytest..."
pytest tests/ -v

# Run with coverage (optional)
echo "📊 Running tests with coverage..."
pytest tests/ --cov=bakong_khqr --cov-report=html

echo "✅ Tests completed!"
echo "📈 Coverage report available at: htmlcov/index.html"