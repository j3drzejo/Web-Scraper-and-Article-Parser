import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from banned_domain_handler import is_domain_banned, add_to_banned_domains
from scraper import parse_article, add_to_response
from google_serp_api import ScrapeitCloudClient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
API_URL = 'https://api.hasdata.com/scrape/google/serp'
API_KEY = "YOUR-API-KEY"  # Consider using environment variables for sensitive data
MIN_CONTENT_LENGTH = 1500
MAX_ARTICLES = 3

def get_from_api(keyword):
    params = {
        'q': f"najlepsze gry planszowe 2024",
        'location': "Poland",
        'deviceType': "desktop",
        'gl': "pl",
        'hl': "pl",
        'num': 10,
    }
    try:
        client = ScrapeitCloudClient(api_key=API_KEY)
        response = client.scrape(params=params)
        data = json.loads(response.text)
        
        with open("sample.json", "w", encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        
        return data.get('organic_results', [])
    except Exception as e:
        logging.error(f"Error fetching data from API: {e}")
        return []

def check_if_long_enough(url):
    if is_domain_banned(url):
        return False
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        article = soup.find('article') or soup.find('body')
        
        if not article:
            add_to_banned_domains(url)
            return False
        
        content_length = len(''.join(article.stripped_strings))
        
        if content_length > MIN_CONTENT_LENGTH:
            return True
        else:
            add_to_banned_domains(url)
            return False
    except Exception as e:
        logging.warning(f"Error checking content length for {url}: {e}")
        add_to_banned_domains(url)
        return False

def scrape_top_articles(organic_results):
    articles_scraped = 0
    for result in organic_results:
        url = result.get("link")
        if not url:
            continue
        
        if check_if_long_enough(url):
            try:
                add_to_response(parse_article(url))
                articles_scraped += 1
                if articles_scraped == MAX_ARTICLES:
                    break
            except Exception as e:
                logging.error(f"Error parsing article from {url}: {e}")
    
    logging.info(f"Scraped {articles_scraped} articles")

def main():
    keyword = ""  # You can make this dynamic if needed
    organic_results = get_from_api(keyword)
    scrape_top_articles(organic_results)

if __name__ == "__main__":
    main()