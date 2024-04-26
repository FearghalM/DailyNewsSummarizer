from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from urllib.parse import quote

def scrapeWebsite(query):
    try:
        encoded_query = quote(query)
        url = f"https://news.google.com/search?q={encoded_query}&hl=en-IE&gl=IE&gl=IE&ceid=IE%3Aen"

        with urlopen(url) as data:
            wiki_html = data.read()
        page_soup = soup(wiki_html, 'html.parser')

        print(f"Title: {page_soup.title.string}")
        articles = page_soup.find_all('article')
        print(f"Total articles: {len(articles)}")
        for article in articles:
            time_element = article.find('time')
            if time_element:
                time_element = time_element['datetime'].replace('T', ' ').replace('Z', '')
            else:
                print("Datetime not found for this article")
            # sort by time_element to get the latest news
            tags = set(article.find_all('a'))
            for tag in tags:
                if len(tag.text) > 0:
                    print(f"Date Time: {time_element} \nTag Subject: {tag.text} \nTag URL: https://news.google.com/{tag['href'][2:]}")

    except Exception as e:
        print("An error occurred:", e)


if __name__ == '__main__':
    query = input("Enter a query: ")
    scrapeWebsite(query)
