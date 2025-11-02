#!/bin/bash

# Start Development Server Script for Flask E-Commerce with Bakong KHQR

echo "🚀 Starting Flask E-Commerce Development Server..."

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

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Please create one with the required environment variables."
    echo "📝 Required variables:"
    echo "   - SECRET_KEY"
    echo "   - MAIL_USERNAME"
    echo "   - MAIL_PASSWORD"
    echo "   - TELEGRAM_BOT_TOKEN"
    echo "   - TELEGRAM_CHAT_ID"
    echo "   - BAKONG_TOKEN"
    exit 1
fi

# Create static directory if it doesn't exist
mkdir -p static

# Run the Flask application
echo "🌐 Starting Flask development server..."
echo "📱 Access the app at: http://127.0.0.1:5000"
export FLASK_APP=app.py
export FLASK_ENV=development
flask run