from bs4 import BeautifulSoup as soup
from urllib.request import urlopen, Request
from urllib.parse import quote
from datetime import datetime, timedelta
import csv
import os

def scrape_website(query):
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
            if time_element:
                time_published = time_element['datetime'].replace('T', ' ').replace('Z', '')
                time_published = datetime.strptime(time_published, "%Y-%m-%d %H:%M:%S")
            else:
                time_published = datetime.min  # Use minimum datetime if time is not found for the article

            tags = set(article.find_all('a'))
            for tag in tags:
                if tag.text.strip() and time_published > time_24_hours_ago:  # Skip empty tags and old articles
                    article_title = tag.text.strip()
                    article_url = f"https://news.google.com/{tag['href'][2:]}"
                    articles_data.append({
                        'time_published': time_published,
                        'article_title': article_title,
                        'article_url': article_url
                    })

        # Sort articles by time_published
        articles_data.sort(key=lambda x: x['time_published'])

        # Print sorted articles
        for article in articles_data:
            print(f"Article Time: {article['time_published']} \nArticle Title: {article['article_title']} \nArticle URL: {article['article_url']}")

        # Create Articles directory if it doesn't exist
        if not os.path.exists('Articles'):
            os.makedirs('Articles')
        # Append articles data to the CSV file
        csv_filename = f"Articles/{query}_articles.csv"
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['time_published', 'article_title', 'article_url']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for article in articles_data:
                writer.writerow({
                    'time_published': article['time_published'].strftime("%Y-%m-%d %H:%M:%S"),
                    'article_title': article['article_title'],
                    'article_url': article['article_url']
                })
        print(f"Data successfully written to {csv_filename}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    query = input("Enter a query: ")
    scrape_website(query)
