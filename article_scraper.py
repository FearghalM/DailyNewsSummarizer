from bs4 import BeautifulSoup as soup
from urllib.request import urlopen, Request
from urllib.parse import quote
from datetime import datetime, timedelta
import csv
import os

def scrape_article(url):
    # Scrapes the article content from the given URL
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = Request(url, headers=headers)

        with urlopen(req) as page_data:
            html_content = page_data.read()

        page_soup = soup(html_content, 'html.parser')

        article_content = page_soup.find('article')
        if article_content:
            return article_content.text.strip()
        else:
            return None
    except Exception as e:
        print(f"Error scraping article: {e}")
        return None

article_content = scrape_article("https://www.irishcentral.com/news/ireland-seabed-mapping-project-2026")
print(article_content)
