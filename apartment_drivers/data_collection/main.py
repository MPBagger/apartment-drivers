from crawler import boliga_crawler
from scraper import create_data_frame
import pandas as pd

def main(url='https://www.boliga.dk/resultat?page=', pages=1):
    """
    This script collects data from a website using a crawler, creates a data frame, and saves it to a CSV file.

    Parameters:
    - url (str): The URL of the website to crawl.
    - pages (int): The number of pages to crawl.

    Returns:
    - None

    Example usage:
    ```
    url = 'https://www.boliga.dk/resultat?page='
    page_count = 1
    main(url, page_count)
    ```
    """
    dfs = []
    for page in range(pages):
        try:
            _filename = f'data/addresses_{page}.txt'
            boliga_crawler(url, _filename, 1)
            df = create_data_frame(_filename)
            df.to_csv(f'data/raw_{page}.csv', index=False)
            dfs.append(df)
        except Exception as e:
            print(f"An error occurred while processing page {page}: {e}")
    
    combined = pd.concat(dfs, ignore_index=True)
    combined.to_csv('data/raw.csv', index=False)

if __name__ == '__main__':
    main(url="https://www.boliga.dk/resultat?propertyType=3&page=",pages=5)
