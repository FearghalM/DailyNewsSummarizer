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

    
        title = page_soup.title.string
        print(f"Title: {title}")

        articles = page_soup.find_all('div', class_='article-body')
        print(f"Total articles: {len(articles)}")
        # return text content of the article removing any extra spaces
        textwithoutspaces = ' '.join([article.text.strip() for article in articles])
        # add to the csv file
        with open(f'Articles/{title}.txt', 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Article Content']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'Article Content': textwithoutspaces})

        return textwithoutspaces
    except Exception as e:
        print(f"Error scraping article: {e}")
        return None

article_content = scrape_article("https://www.irishcentral.com/news/ireland-seabed-mapping-project-2026")
print(article_content)
