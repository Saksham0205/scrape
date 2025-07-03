#!/bin/bash

echo "🚀 Setting up Full Stack Intern Challenge Project"
echo "=================================================="

# Check if Redis is running
check_redis() {
    if command -v redis-cli &> /dev/null; then
        if redis-cli ping &> /dev/null; then
            echo "✅ Redis is running"
            return 0
        else
            echo "❌ Redis is not running. Please start Redis server."
            echo "   On macOS: brew services start redis"
            echo "   On Ubuntu: sudo systemctl start redis-server"
            echo "   Using Docker: docker run -d -p 6379:6379 redis:latest"
            return 1
        fi
    else
        echo "❌ Redis is not installed. Please install Redis."
        echo "   On macOS: brew install redis"
        echo "   On Ubuntu: sudo apt-get install redis-server"
        echo "   Using Docker: docker run -d -p 6379:6379 redis:latest"
        return 1
    fi
}

# Setup backend
setup_backend() {
    echo "🐍 Setting up Python backend..."
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        echo "Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install backend dependencies
    echo "Installing Python dependencies..."
    cd backend
    pip install -r requirements.txt
    cd ..
    
    echo "✅ Backend setup complete"
}

# Setup frontend
setup_frontend() {
    echo "📦 Setting up Node.js frontend..."
    
    cd frontend
    echo "Installing Node.js dependencies..."
    npm install
    cd ..
    
    echo "✅ Frontend setup complete"
}

# Run the application
run_app() {
    echo "🎬 Starting the application..."
    
    # Start backend in background
    echo "Starting Flask backend..."
    source venv/bin/activate
    cd backend
    python app.py &
    BACKEND_PID=$!
    cd ..
    
    # Wait for backend to start
    sleep 3
    
    # Start frontend in background
    echo "Starting Vue frontend..."
    cd frontend
    npm run serve &
    FRONTEND_PID=$!
    cd ..
    
    echo "✅ Application started!"
    echo "🌐 Frontend: http://localhost:8080"
    echo "🔧 Backend API: http://localhost:5000"
    echo ""
    echo "Press Ctrl+C to stop the servers"
    
    # Function to handle cleanup
    cleanup() {
        echo ""
        echo "🛑 Stopping servers..."
        kill $BACKEND_PID 2>/dev/null
        kill $FRONTEND_PID 2>/dev/null
        exit 0
    }
    
    # Trap Ctrl+C
    trap cleanup INT
    
    # Wait for user to stop
    wait
}

# Main execution
main() {
    # Check Redis
    if ! check_redis; then
        exit 1
    fi
    
    # Setup backend
    setup_backend
    
    # Setup frontend
    setup_frontend
    
    # Ask user if they want to run the app
    echo ""
    read -p "Would you like to start the application now? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        run_app
    else
        echo "Setup complete! You can start the application manually:"
        echo "Backend: cd backend && source ../venv/bin/activate && python app.py"
        echo "Frontend: cd frontend && npm run serve"
    fi
}

# Run main function
main 