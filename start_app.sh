#!/bin/bash

echo "Starting Video Summarizer Application..."
echo ""
ollama serve &
echo "Starting Python Backend..."
cd backend && python api.py &
BACKEND_PID=$!

echo "Waiting for backend to start..."
sleep 5

echo "Starting React Frontend..."
cd frontend && npm start &
FRONTEND_PID=$!

echo ""
echo "========================================"
echo "Video Summarizer is starting..."
echo ""
echo "Backend: http://localhost:5000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all services"
echo "========================================"

# Wait for user to press Ctrl+C
trap "echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
