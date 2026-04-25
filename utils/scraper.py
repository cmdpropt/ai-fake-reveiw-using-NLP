import requests
from bs4 import BeautifulSoup
import time
import re

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
}

def detect_platform(url):
    url_lower = url.lower()
    if "amazon" in url_lower:
        return "amazon"
    elif "flipkart" in url_lower:
        return "flipkart"
    return None

def scrape_amazon_reviews(url, max_pages=3):
    reviews = []
    
    # Try to convert product URL to review page URL
    dp_match = re.search(r'/dp/([A-Z0-9]+)', url)
    if dp_match:
        base_url = f"https://www.amazon.in/product-reviews/{dp_match.group(1)}/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber="
    else:
        # Fallback if not a standard DP url
        base_url = url + "&pageNumber=" if "?" in url else url + "?pageNumber="
        
    for page in range(1, max_pages + 1):
        try:
            page_url = base_url + str(page) if dp_match else base_url.replace("pageNumber=", f"pageNumber={page}")
            response = requests.get(page_url, headers=HEADERS, timeout=10)
            
            if response.status_code != 200:
                break
                
            soup = BeautifulSoup(response.content, 'html.parser')
            review_blocks = soup.find_all('div', {'data-hook': 'review'})
            
            if not review_blocks:
                break
                
            for block in review_blocks:
                text_elem = block.find('span', {'data-hook': 'review-body'})
                if text_elem:
                    text = text_elem.text.strip()
                    if text:
                        reviews.append(text)
            
            time.sleep(1) # Polite scraping
        except Exception as e:
            print(f"Error scraping Amazon page {page}: {e}")
            break
            
    return reviews[:100]

def scrape_flipkart_reviews(url, max_pages=3):
    reviews = []
    
    # Handle Flipkart pagination
    if "page=" in url:
        base_url = re.sub(r'page=\d+', 'page=', url)
    else:
        base_url = url + "&page=" if "?" in url else url + "?page="
        
    for page in range(1, max_pages + 1):
        try:
            page_url = base_url + str(page)
            response = requests.get(page_url, headers=HEADERS, timeout=10)
            
            if response.status_code != 200:
                break
                
            soup = BeautifulSoup(response.content, 'html.parser')
            # Flipkart uses this class for review text mostly
            review_blocks = soup.find_all('div', {'class': 't-ZTKy'})
            
            if not review_blocks:
                break
                
            for block in review_blocks:
                text_elem = block.find('div', {'class': ''})
                if text_elem:
                    text = text_elem.text.strip()
                    # Clean up READ MORE button text
                    text = text.replace("READ MORE", "").strip()
                    if text:
                        reviews.append(text)
                        
            time.sleep(1)
        except Exception as e:
            print(f"Error scraping Flipkart page {page}: {e}")
            break
            
    return reviews[:100]

def extract_reviews(url):
    platform = detect_platform(url)
    if platform == "amazon":
        return scrape_amazon_reviews(url)
    elif platform == "flipkart":
        return scrape_flipkart_reviews(url)
    else:
        return []
