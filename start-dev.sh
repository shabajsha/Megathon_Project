#!/bin/bash

# MERN Stack Event Management System - Development Setup

echo "🚀 Starting MERN Stack Event Management System..."
echo ""

# Check if MongoDB is running (optional - can be skipped if using MongoDB Atlas)
echo "⚠️  Note: Make sure MongoDB is running on localhost:27017"
echo "   Or update MONGODB_URI in backend/.env to use MongoDB Atlas"
echo ""

# Start backend
echo "📦 Starting Backend Server..."
cd backend
npm run dev &
BACKEND_PID=$!
cd ..

# Wait a bit for backend to start
sleep 3

# Start frontend
echo "🎨 Starting Frontend Server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Services started!"
echo "   Backend:  http://localhost:5000"
echo "   Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for user interrupt
wait
