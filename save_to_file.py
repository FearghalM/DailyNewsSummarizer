import os
import csv

def save_article_data(query, title, sentiment, authors, publish_date, combined_summary, response_url):
    # Create Articles directory if it doesn't exist
    if not os.path.exists('Articles'):
        os.makedirs('Articles')
    
    # Append articles data to the CSV file
    csv_filename = f"Articles/{query}_articles.csv"
    file_exists = os.path.isfile(csv_filename)
    
    with open(csv_filename, mode='a', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        # Check if the article is already in the file
        if file_exists:
            with open(csv_filename, 'r', encoding='utf-8') as check_file:
                reader = csv.reader(check_file)
                if any(query == row[0] for row in reader):
                    print(f"Article already in the file: {title}")
                    return
        
        # Replace commas in fields
        title = title.replace(',', ';')
        authors = authors.replace(',', ';')
        combined_summary = combined_summary.replace(',', ';')
        
        # Write data to the CSV file
        if not file_exists:
            writer.writerow(['Query', 'Title', 'Sentiment', 'Authors', 'Publish Date', 'Summary', 'URL'])
        
        writer.writerow([query, title, sentiment, authors, publish_date, combined_summary, response_url])
    
    print(f"Data successfully written to {csv_filename}")
