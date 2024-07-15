import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse, urljoin
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_internal_links(url, max_links=100):
    internal_links = set()
    domain = urlparse(url).netloc

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            full_url = urljoin(url, href)
            if domain in urlparse(full_url).netloc:
                internal_links.add(full_url)
                if len(internal_links) >= max_links:
                    break

        return list(internal_links)

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching {url}: {e}")
        return list(internal_links)

def parse_article(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.find('title').text if soup.find('title') else 'No title'

        categories = []
        for meta in soup.find_all('meta', {'name': ['news_keywords', 'keywords']}):
            if 'content' in meta.attrs:
                categories.extend(meta['content'].split(','))

        date = soup.find('meta', {'property': 'article:published_time'})
        date = date['content'] if date and 'content' in date.attrs else 'No date'

        article_section = soup.find('article')
        if article_section:
            for tag in article_section.find_all(True):
                if tag.name not in ['p', 'h1', 'h2', 'h3']:
                    tag.decompose()
            content = ' '.join(article_section.stripped_strings)
        else:
            content = 'No content found'

        return {
            'title': title,
            'categories': categories,
            'date': date,
            'content': content
        }

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching {url}: {e}")
    except Exception as e:
        logging.error(f"Error parsing {url}: {e}")
    return None

def add_to_response(data):
    try:
        with open("response.json", "r+", encoding="utf-8") as file:
            try:
                file_data = json.load(file)
            except json.decoder.JSONDecodeError:
                file_data = []
            
            file_data.append(data)
            
            file.seek(0)
            json.dump(file_data, file, indent=4, ensure_ascii=False)
            file.truncate()
    except IOError as e:
        logging.error(f"Error writing to response.json: {e}")

def process_url(url):
    data = parse_article(url)
    if data:
        add_to_response(data)
    return url, data is not None

def main(urls):
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(process_url, url): url for url in urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                _, success = future.result()
                if success:
                    logging.info(f"Successfully processed {url}")
                else:
                    logging.warning(f"Failed to process {url}")
            except Exception as e:
                logging.error(f"Exception occurred while processing {url}: {e}")

if __name__ == "__main__":
    urls = [
      # Sample urls
    ]
    main(urls)