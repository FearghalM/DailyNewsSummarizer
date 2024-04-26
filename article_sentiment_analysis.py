from textblob import TextBlob
from newspaper import Article
import requests
import os

def analyze_article_sentiment(query, url,time_published,author_name):
    try:
        response = requests.head(url, allow_redirects=True, timeout=30)
        if response.history:  # Check if there's any redirect
            response_url = response.url
            print(f"Redirected URL: {response_url}")
        else:
            response_url = url
            print(f"URL: {response_url}")

        news_article = Article(response_url)
        news_article.download()
        news_article.parse()
        news_article.nlp()
        
        sentiment_analysis = TextBlob(news_article.text)
        sentiment = 'Positive' if sentiment_analysis.sentiment.polarity > 0 else 'Negative' if sentiment_analysis.sentiment.polarity < 0 else 'Neutral'
        
        print(f"news_article.authors: {news_article.authors} author_element: {author_name}")
        title = news_article.title
        authors = author_name if author_name else news_article.authors if news_article.authors else "Unknown"
        # check if authors is a list
        if isinstance(authors, list):
            authors = ', '.join(authors)
        publish_date = time_published
        summary = news_article.summary
        
        # Create Articles directory if it doesn't exist
        if not os.path.exists('Articles'):
            os.makedirs('Articles')
        # Append articles data to the text file
        txt_filename = f"Articles/{query}_articles.txt"
        with open(txt_filename, mode='a', encoding='utf-8') as txt_file:
            # Check if the article is already in the file
            with open(txt_filename, 'r', encoding='utf-8') as check_file:
                if title in check_file.read():
                    print(f"Article already in the file: {title}")
                    return
                
            # Write data to the text file
            txt_file.write(f"Title: {title}\n")
            txt_file.write(f"Sentiment: {sentiment}\n")
            txt_file.write(f"Authors: {authors}\n")
            txt_file.write(f"Publish Date: {publish_date}\n")
            txt_file.write(f"Summary: {summary}\n")
            txt_file.write(f"URL: {response_url}\n\n")

        print(f"Data successfully written to {txt_filename}")
    except Exception as e:
        print(f"Error scraping article: {e}")
        return

