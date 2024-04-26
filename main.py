from bs4 import BeautifulSoup as soup
from urllib.request import urlopen

try:
    wiki_url = 'https://en.wikipedia.org/wiki/Genome'
    with urlopen(wiki_url) as wiki_data:
        wiki_html = wiki_data.read()
    page_soup = soup(wiki_html, 'html.parser')

    genome_table = page_soup.find('table', {'class': 'wikitable sortable'})
    headers = genome_table.find_all('th')
    header_titles = [header.text.strip() for header in headers]

    all_rows = genome_table.find_all('tr')[1:]  # Skip the header row

    table_rows = []
    for row in all_rows:
        row_data = row.find_all('td')
        row_values = [data.text.strip() for data in row_data]
        table_rows.append(row_values)

    filename = 'genome_table.csv'
    with open(filename, 'w', encoding="utf-8") as f:
        f.write(','.join(header_titles) + '\n')
        for row in table_rows:
            f.write(','.join(row) + '\n')

    print("CSV file generated successfully!")

except Exception as e:
    print("An error occurred:", e)
