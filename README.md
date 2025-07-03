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