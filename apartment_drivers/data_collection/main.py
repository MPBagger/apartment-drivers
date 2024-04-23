from crawler import boligsiden_crawler
from scraper import create_data_frame

def main():
    """
    This script collects data from a website using a crawler, creates a data frame, and saves it to a CSV file.

    Parameters:
    - url (str): The URL of the website to crawl.
    - filename (str): The name of the file to save the addresses to.
    - page_count (int): The number of pages to crawl.

    Returns:
    - None

    Example usage:
    ```
    url = 'https://www.boligsiden.dk/tilsalg?page='
    filename = 'data/addresses.txt'
    page_count = 1
    main(url, filename, page_count)
    ```
    """
    url = 'https://www.boligsiden.dk/tilsalg?page='
    filename = 'data/addresses.txt'
    boligsiden_crawler(url, filename, 1)
    df = create_data_frame(filename)
    df.to_csv('data/raw.csv', index=False)
    print(df)

if __name__ == '__main__':
    main()
