from bs4 import BeautifulSoup as soup
from urllib.request import urlopen, Request
from urllib.parse import quote
from datetime import datetime, timedelta
import article_sentiment_analysis as asa
import save_to_file as stf
import send_email as se

def scrape_website_search(query,max_articles,receiver_email):
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
        # print(f"Total articles: {len(articles)}")

        time_24_hours_ago = datetime.now() - timedelta(hours=24)  # Get date and time 24 hours ago

        article_count = 0  # Counter for the number of articles scraped

        for article in articles:
            if article_count >= max_articles:
                break  # Stop scraping if maximum articles limit is reached

            time_element = article.find('time')

            if time_element:
                time_published = time_element['datetime'].replace('T', ' ').replace('Z', '')
                time_published = datetime.strptime(time_published, "%Y-%m-%d %H:%M:%S")
            else:
                time_published = datetime.min  # Use minimum datetime if time is not found for the article

            tags = set(article.find_all('a'))
            for tag in tags:
                if tag.text.strip() and time_published > time_24_hours_ago:  # Skip empty tags and old articles
                    # Find the div element with the class 'bInasb'
                    author_element = article.find('div', class_='bInasb')

                    # Extract the text from the first span element within the div
                    author_name = author_element.find('span').text if author_element else None

                    print(f"Author: {author_name}")
                    article_url = f"https://news.google.com/{tag['href'][2:]}"
                    query, title, sentiment, authors, publish_date, combined_summary, response_url = asa.analyze_article_sentiment(query,article_url,time_published,author_name)
                    print(f"Title: {title}\nSentiment: {sentiment}\nAuthors: {authors}\nPublish Date: {publish_date}\nSummary: {combined_summary}\nURL: {response_url}")
                    #saves to file
                    stf.save_article_data(query, title, sentiment, authors, publish_date, combined_summary, response_url)
                    print("Data saved to file")

                    article_count += 1  # Increment the article count

        se.send_email(query,receiver_email)
        # clear the file after sending the email
        with open(f"Articles/{query}_articles.txt", 'w') as file:
            file.write("")
                    

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    query = input("Enter a query: ")
    max_articles = int(input("Enter how many articles to scrape: "))  # User input for maximum articles to scrape
    receiver_email = input("Enter your email: ")
    scrape_website_search(query,max_articles, receiver_email)

