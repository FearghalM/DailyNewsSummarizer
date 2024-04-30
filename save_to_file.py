import os

def save_article_data(query, title, sentiment, authors, publish_date, combined_summary, response_url):

    print(f"Saving data to file for {title}")
    
    # Append articles data to the text file
    txt_filename = f"Articles/{query}_articles.txt"
    
    # Check if the article already exists in the file or if title is "Title not found"
    if os.path.exists(txt_filename):
        with open(txt_filename, mode='r', encoding='utf-8') as txt_file:
            if title in txt_file.read() or "Title not found" in txt_file.read():
                print(f"Article already exists in {txt_filename}")
                return
        
    with open(txt_filename, mode='a', encoding='utf-8') as txt_file:
        txt_file.write(f"Title: {title}\n")
        txt_file.write(f"Sentiment: {sentiment}\n")
        txt_file.write(f"Authors: {authors}\n")
        txt_file.write(f"Publish_date: {publish_date}\n")
        txt_file.write(f"Summary: {combined_summary}\n")
        txt_file.write(f"URL: {response_url}\n\n")
    
    print(f"Data successfully written to {txt_filename}")
