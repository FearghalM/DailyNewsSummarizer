from bs4 import BeautifulSoup as soup
from urllib.request import urlopen, Request
from urllib.parse import quote
from datetime import datetime, timedelta
import csv
import os
import article_sentiment_analysis as asa
import article_scraper as scraper

sentiments = ('Positive', 'Negative', 'Neutral')

def scrape_website_search(query):
    articles_data = []

    try:
        encoded_query = quote(query)
        url = f"https://news.google.com/search?q={encoded_query}&hl=en-IE&gl=IE&gl=IE&ceid=IE%3Aen"

        # Add user-agent header to mimic a web browser
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = Request(url, headers=headers)

        with urlopen(req) as page_data:
            html_content = page_data.read()

        page_soup = soup(html_content, 'html.parser')

        print(f"Title: {page_soup.title.string}")
        articles = page_soup.find_all('article')
        print(f"Total articles: {len(articles)}")

        time_24_hours_ago = datetime.now() - timedelta(hours=24)  # Get date and time 24 hours ago

        for article in articles:
            time_element = article.find('time')
            author_element = article.find('a', {'class': 'bInasb'})

            if time_element:
                time_published = time_element['datetime'].replace('T', ' ').replace('Z', '')
                time_published = datetime.strptime(time_published, "%Y-%m-%d %H:%M:%S")
            else:
                time_published = datetime.min  # Use minimum datetime if time is not found for the article

            tags = set(article.find_all('a'))
            for tag in tags:
                if tag.text.strip() and time_published > time_24_hours_ago:  # Skip empty tags and old articles
                    article_url = f"https://news.google.com/{tag['href'][2:]}"
                    asa.analyze_article_sentiment(query,article_url,time_published,author_element)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    query = input("Enter a query: ")
    scrape_website_search(query)
