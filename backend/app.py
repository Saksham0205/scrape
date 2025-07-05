from flask import Flask, jsonify, request
from flask_cors import CORS
import redis
import json
import time

app = Flask(__name__)
CORS(app)

def get_redis_connection():
    try:
        r = redis.Redis(host='localhost', port=6379, db=0, socket_connect_timeout=5)
        r.ping()  # Test connection
        return r
    except:
        return None

@app.route("/scraped-content", methods=["GET"])
def get_scraped_content():
    """
    API to retrieve scraped content from Redis.
    """
    try:
        r = get_redis_connection()
        if not r:
            return jsonify({"success": False, "message": "Redis connection failed"}), 500
            
        data = r.get("scraped_content")
        if data:
            # Decode bytes to string if necessary
            if isinstance(data, bytes):
                data_str = data.decode('utf-8')
            else:
                data_str = str(data)
            parsed_data = json.loads(data_str)
            return jsonify({
                "success": True, 
                "data": {
                    "head": parsed_data.get("head"),
                    "header": parsed_data.get("header"),
                    "url": parsed_data.get("url"),
                    "status": parsed_data.get("status"),
                    "scraped_at": parsed_data.get("scraped_at"),
                    "total_products_found": parsed_data.get("total_products_found", 0)
                }
            })
        else:
            return jsonify({"success": False, "message": "No scraped content found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": f"Error retrieving data: {str(e)}"}), 500

@app.route("/products", methods=["GET"])
def get_products():
    """
    This endpoint returns a list of real scraped products from Croma.
    """
    try:
        r = get_redis_connection()
        if not r:
            return jsonify({
                "success": False, 
                "message": "Redis connection failed. Please ensure Redis is running.",
                "data": []
            }), 500
            
        data = r.get("scraped_content")
        if not data:
            return jsonify({
                "success": False,
                "message": "No scraped data available. Please run the scraper first by clicking 'Scrape Products'.",
                "data": []
            }), 404
            
        # Decode bytes to string if necessary
        if isinstance(data, bytes):
            data_str = data.decode('utf-8')
        else:
            data_str = str(data)
        parsed_data = json.loads(data_str)
        scraped_products = parsed_data.get("products", [])
        
        if not scraped_products or len(scraped_products) == 0:
            return jsonify({
                "success": False,
                "message": "No products found in scraped data. Please run the scraper again.",
                "data": []
            }), 404
            
        return jsonify({
            "success": True, 
            "data": scraped_products, 
            "source": "scraped",
            "scraped_at": parsed_data.get("scraped_at"),
            "total_count": len(scraped_products),
            "url": parsed_data.get("url")
        })
    
    except Exception as e:
        return jsonify({
            "success": False, 
            "message": f"Error retrieving products: {str(e)}",
            "data": []
        }), 500

@app.route("/scrape", methods=["POST"])
def trigger_scrape():
    """
    Endpoint to trigger real scraping from Croma website
    """
    try:
        from scraper import scrape_page_elements, store_in_redis
        
        request_data = request.get_json() if request.is_json else {}
        url = request_data.get('url', 'https://www.croma.com/televisions-accessories/c/997')
        page_elements = scrape_page_elements(url)
        
        if page_elements["status"] == "success":
            store_in_redis(page_elements)
            return jsonify({
                "success": True, 
                "message": f"Scraping completed successfully! Found {len(page_elements['products'])} products", 
                "data": {
                    "url": page_elements["url"],
                    "products_found": len(page_elements["products"]),
                    "scraped_at": page_elements["scraped_at"],
                    "status": page_elements["status"]
                }
            })
        elif page_elements["status"] == "blocked":
            return jsonify({
                "success": False,
                "message": "Website blocked the scraping request (403 Forbidden)",
                "error": page_elements.get("error", "Scraping was blocked"),
                "suggestion": "This is common for e-commerce sites with anti-bot protection. For production use, consider implementing proxy rotation, browser automation (Selenium), or using official APIs."
            }), 403
        else:
            return jsonify({
                "success": False, 
                "message": "Scraping failed", 
                "error": page_elements.get("error", "Unknown error"),
                "data": page_elements
            }), 400
            
    except Exception as e:
        return jsonify({"success": False, "message": f"Scraping failed: {str(e)}"}), 500

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    redis_status = "connected" if get_redis_connection() else "disconnected"
    
    # Check if scraped data exists
    scraped_data_status = "no_data"
    try:
        r = get_redis_connection()
        if r:
            data = r.get("scraped_content")
            if data:
                parsed_data = json.loads(data.decode('utf-8') if isinstance(data, bytes) else str(data))
                products = parsed_data.get("products", [])
                scraped_data_status = f"{len(products)}_products" if products else "empty"
    except:
        scraped_data_status = "error"
    
    return jsonify({
        "status": "healthy",
        "redis": redis_status,
        "scraped_data": scraped_data_status,
        "timestamp": time.time(),
        "endpoints": {
            "products": "/products",
            "scraped_content": "/scraped-content", 
            "scrape": "/scrape"
        }
    })

if __name__ == "__main__":
    print("Server will run on: http://127.0.0.1:5001")
    app.run(debug=True, port=5001)