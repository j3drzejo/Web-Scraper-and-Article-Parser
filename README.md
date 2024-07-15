# Web Scraper and Article Parser

This project is a Python-based web scraper and article parser designed to extract content from specified URLs, focusing on internal links and article content.

## Features

- Scrape internal links from a given URL
- Parse article content, including title, categories, publication date, and main text
- Concurrent processing of multiple URLs
- JSON output for parsed articles
- Error handling and logging

## Requirements

- Python 3.6+
- Dependencies listed in `requirements.txt`

## Installation

1. Clone this repository
2. Install the required dependencies

## Usage

1. Update the `urls` list in the `main()` function with the URLs you want to scrape.
2. Run the script:
3. The parsed articles will be saved in `response.json` in the same directory.

## Main Components

- `get_internal_links(url)`: Extracts internal links from a given URL.
- `parse_article(url)`: Parses an article, extracting title, categories, date, and content.
- `add_to_response(data)`: Adds parsed article data to the JSON response file.
- `main(urls)`: Orchestrates the scraping and parsing process for multiple URLs concurrently.

## Output

The script generates a `response.json` file containing an array of parsed articles. Each article is represented as a JSON object with the following structure:

```json
{
"title": "Article Title",
"categories": ["Category1", "Category2"],
"date": "2024-07-15T12:00:00Z",
"content": "Article content..."
}# Web-Scraper-and-Article-Parser
