from textblob import TextBlob
from newspaper import Article
import requests
import text_summarization as ts


def analyze_article_sentiment(query, url,time_published,author_name):
    try:
        response = requests.head(url, allow_redirects=True, timeout=30)
        if response.history:  # Check if there's any redirect
            response_url = response.url
            # print(f"Redirected URL: {response_url}")
        else:
            response_url = url
            # print(f"URL: {response_url}")

        news_article = Article(response_url)
        news_article.download()
        news_article.parse()
        news_article.nlp()
        
        sentiment_analysis = TextBlob(news_article.text)
        sentiment = 'Positive' if sentiment_analysis.sentiment.polarity > 0 else 'Negative' if sentiment_analysis.sentiment.polarity < 0 else 'Neutral'
        
        # print(f"news_article.authors: {news_article.authors} author_element: {author_name}")
        title = news_article.title
        authors = author_name if author_name else news_article.authors if news_article.authors else "Unknown"
        # check if authors is a list
        if isinstance(authors, list):
            authors = ', '.join(authors)
        publish_date = time_published
        first_summary = news_article.summary

        combined_summary = ts.extractive_summarization(first_summary+news_article.text)

        # Assuming you have three summaries: first_summary, second_summary, and third_summary
        print(f"First Summary length: {len(first_summary)}, \nSecond Summary length: {len(combined_summary)} ")

        return(query, title, sentiment, authors, publish_date, combined_summary, response_url)

    
    except Exception as e:
        print(f"Error scraping article: {e}")
        return

