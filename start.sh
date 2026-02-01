#!/bin/bash

echo "🚀 Starting Expense Tracker"
echo "=========================="

# Check if we're in the right directory
if [ ! -f "README.md" ]; then
    echo "❌ Please run this script from the expense-tracker directory"
    exit 1
fi

echo "📦 Installing backend dependencies..."
cd backend
pip install -r requirements.txt

echo "🔧 Starting backend server..."
python main.py &
BACKEND_PID=$!

echo "Backend started with PID: $BACKEND_PID"
echo "Backend running at: http://localhost:8000"

# Wait a moment for backend to start
sleep 3

echo ""
echo "📦 Installing frontend dependencies..."
cd ../frontend
npm install

echo "🎨 Starting frontend server..."
echo "Frontend will be available at: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"

# Start frontend (this will block)
npm start

# Cleanup: kill backend when frontend stops
echo "🛑 Stopping backend server..."
kill $BACKEND_PID 2>/dev/null