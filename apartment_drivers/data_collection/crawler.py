import requests
from bs4 import BeautifulSoup

def boliga_crawler(url, filename, num_pages=1):
    """
    Crawls through the given URL and extracts addresses from the web pages.
    
    Args:
        url (str): The base URL to crawl.
        filename (str): The name of the file to save the extracted addresses.
        num_pages (int): The number of pages to crawl. Default is 1.
    
    Returns:
        None
    """
    with open(filename, 'w') as file:
        for page in range(1, num_pages+1):
            response = requests.get(f'{url}{page}')
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a'):
                href = link.get('href')
                try:
                    if href.startswith('/adresse/'):
                        file.write('https://www.boliga.dk' + href + '\n')
                except:
                    pass

if __name__ == '__main__':
    boliga_crawler('https://www.boliga.dk/resultat?page=', 'adress.txt')
    