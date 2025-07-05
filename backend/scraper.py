from bs4 import BeautifulSoup, Tag
from bs4.element import NavigableString
import redis
import json
import time
import random
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def create_selenium_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')  
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36'
    ]
    chrome_options.add_argument(f'user-agent={random.choice(user_agents)}')
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)  
    return driver

def scrape_page_elements(url):
    try:
        driver = create_selenium_driver()
        
        try:
            
            time.sleep(random.uniform(2, 4))
            
            driver.get(url)
            
            # Wait for main content to load
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            total_height = driver.execute_script("return document.body.scrollHeight")
            for i in range(1, total_height, 100):
                driver.execute_script(f"window.scrollTo(0, {i});")
                time.sleep(random.uniform(0.1, 0.3))
            
            # Get the page source after JavaScript execution
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Initialize response structure
            response = {
                "status": "success",
                "url": url,
                "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "products": [],
                "head": str(soup.find('head')),
                "header": str(soup.find('header')),
                "total_products_found": 0
            }
            
            # Product container selectors (Croma specific)
            product_selectors = [
                'div[data-testid="product-item"]',
                '.product-item',
                '.product-card',
                '.plp-card-container',
                '[class*="ProductCard"]'
            ]
            
            # Try each selector until we find products
            products = []
            for selector in product_selectors:
                print(f"Trying selector: {selector}")
                product_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if product_elements:
                    print(f"Found {len(product_elements)} products")
                    
                    for i, product_elem in enumerate(product_elements):
                        try:
                            product_data = {
                                "product_id": str(i + 1),
                                "title": "",
                                "price": "",
                                "sale_price": "",
                                "discount_message": "",
                                "image_url": ""
                            }
                            
                            # Extract title
                            try:
                                title_elem = product_elem.find_element(By.CSS_SELECTOR, 
                                    'h3, h2, [class*="title"], [class*="name"]')
                                if title_elem and title_elem.text:
                                    product_data["title"] = title_elem.text.strip()
                            except NoSuchElementException:
                                continue
                            
                            # Extract prices
                            try:
                                price_elements = product_elem.find_elements(By.CSS_SELECTOR, 
                                    '[class*="price"], .amount, [class*="mrp"]')
                                prices = [price.text.strip() for price in price_elements if price.text and price.text.strip()]
                                if prices:
                                    # Usually first price is sale price, second is original
                                    product_data["sale_price"] = prices[0]
                                    if len(prices) > 1:
                                        product_data["price"] = prices[1]
                            except NoSuchElementException:
                                pass
                            
                            # Extract discount
                            try:
                                discount_elem = product_elem.find_element(By.CSS_SELECTOR, 
                                    '[class*="discount"], [class*="off"], [class*="save"]')
                                if discount_elem and discount_elem.text:
                                    product_data["discount_message"] = discount_elem.text.strip()
                            except NoSuchElementException:
                                pass
                            
                            # Extract image
                            try:
                                img_elem = product_elem.find_element(By.TAG_NAME, 'img')
                                if img_elem:
                                    src = img_elem.get_attribute('src')
                                    if src:
                                        product_data["image_url"] = src
                            except NoSuchElementException:
                                pass
                            
                            # Add product if we have minimum required data
                            if product_data["title"] and (product_data["price"] or product_data["sale_price"]):
                                products.append(product_data)
                            else:
                                print(f"Skipped product {i+1}: insufficient data")
                            
                        except Exception as e:
                            print(f"Error processing product {i+1}: {str(e)}")
                            continue
                    
                    break  # Exit loop if we found products
            
            response["products"] = products
            response["total_products_found"] = len(products)
            
            if not products:
                response["status"] = "error"
                response["error"] = "No products found with any selector"
            
            return response
            
        except TimeoutException:
            return {
                "status": "error",
                "error": "Page load timeout",
                "url": url,
                "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "url": url,
                "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
        finally:
            driver.quit()
            
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "url": url,
            "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }

def store_in_redis(data):
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.set("scraped_content", json.dumps(data))
        return True
    except Exception as e:
        return False

if __name__ == "__main__":
    url = "https://www.croma.com/televisions-accessories/c/997"
    result = scrape_page_elements(url)
    print(f"Found {len(result.get('products', []))} products")