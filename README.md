# Full Stack Intern Challenge

## Project Overview

Build a Python + Vue.js app that scrapes product card data from [Croma Televisions & Accessories](https://www.croma.com/televisions-accessories/c/997), stores it in Redis, and displays the data on a frontend page.

All sections to be completed by candidate are marked with TODO.

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 14+
- Redis server (local or Docker)
- The backend service expects a Redis server running on `localhost:6379`

### Backend

1. Set up a Python virtual environment and activate it:
```
python -m venv venv
source venv/bin/activate   # On Linux/macOS
venv\Scripts\activate     # On Windows
```
2. Navigate to the backend folder:
```
cd backend
```
3. Install dependencies:
```
pip install -r requirements.txt
```
4. Run the scraper (optional: provide your own logic or test with products.json):
```
python scraper.py
```
5. Start the Flask app:
```
python app.py
```

### Frontend

1. Open a new terminal session

2. Navigate to the frontend folder:
```
cd frontend
```
3. Install dependencies:
```
npm install
```
4. Run the app:
```
npm run serve
```

## Expected work
- Implement scraper logic in `scraper.py` to extract head and header html elements from a page.
- Complete `/scraped-content` endpoint function in `app.py`
- Complete the Vue app to dynamically render products.

## Notes
- Ensure you have installed all backend and frontend dependencies before running the app.

---

## 🚀 Quick Start Guide 

### Option 1: Automated Setup (Recommended)
```bash
# Clone and navigate to project directory
git clone https://github.com/Saksham0205/scrape.git
cd scrape

# Ensure Redis is running
redis-server  # Or: brew services start redis (macOS)

# Run automated setup script
chmod +x setup.sh
./setup.sh
```

The script will:
- Check all prerequisites
- Set up Python virtual environment
- Install backend dependencies
- Install frontend dependencies
- Optionally start both servers

### Option 2: Manual Setup
```bash
# 1. Start Redis server
redis-server

# 2. Backend setup (Terminal 1)
python3 -m venv venv
source venv/bin/activate
cd backend
pip install -r requirements.txt
python app.py

# 3. Frontend setup (Terminal 2)
cd frontend
npm install
npm run serve
```

## 🌐 Access the Application

Once both servers are running:

- **Frontend Application**: http://localhost:8080
- **Backend API**: http://localhost:5001
- **Health Check**: http://localhost:5001/health

## 🧪 Testing & Evaluation

### Key Features to Test:
1. **Main Interface**: Clean, responsive UI with Croma branding
2. **Product Scraping**: Click "Scrape Products" to fetch real data
3. **Product Display**: View scraped products in grid layout
4. **Error Handling**: Graceful handling of scraping failures
5. **Loading States**: Smooth UX during operations

### API Endpoints:
- `GET /health` - Server health and status
- `GET /products` - Retrieve scraped product data
- `GET /scraped-content` - Get head/header HTML elements
- `POST /scrape` - Trigger real-time scraping

### Test Commands:
```bash
# Test backend health
curl http://localhost:5001/health

# Test product endpoint
curl http://localhost:5001/products

# Trigger scraping
curl -X POST http://localhost:5001/scrape -H "Content-Type: application/json"
```

## 🛠️ Troubleshooting

### Common Issues:
1. **Redis Connection Failed**: Ensure Redis server is running
   ```bash
   redis-server
   # Or on macOS: brew services start redis
   ```

2. **Port Already in Use**: 
   - Backend (5001): `lsof -ti:5001 | xargs kill -9`
   - Frontend (8080): `lsof -ti:8080 | xargs kill -9`

3. **Selenium Issues**: Chrome/ChromeDriver may need updates
   ```bash
   # Update ChromeDriver if needed
   npm install -g chromedriver
   ```

4. **Scraping Blocked**: Normal behavior - website has anti-bot protection

### Dependencies:
- **Python**: 3.8+ (Tested with 3.13.5)
- **Node.js**: 14+ (Tested with 24.3.0)
- **Redis**: Latest version (Tested with 8.0.2)
- **Chrome**: Latest version (for Selenium)

## 🎯 Project Highlights

### Technical Stack:
- **Backend**: Flask, Redis, Selenium, BeautifulSoup
- **Frontend**: Vue.js 3, Modern CSS Grid
- **Database**: Redis for caching
- **Scraping**: Selenium WebDriver with anti-bot measures

### Key Features:
- ✅ Real-time web scraping with Selenium
- ✅ Anti-bot detection avoidance
- ✅ Responsive, mobile-first design
- ✅ Comprehensive error handling
- ✅ Production-ready setup automation
- ✅ RESTful API design
- ✅ Health monitoring endpoints

### Architecture:
- Clean separation of concerns
- Modular, maintainable code structure
- Professional error handling
- Scalable component architecture

---
