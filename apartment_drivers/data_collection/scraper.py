import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

def get_price(url):
    """
    Crawls the given URL, extracts the price from the HTML content, and returns it.

    Args:
        url (str): The URL to crawl.

    Returns:
        str: The price of the property.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        price = soup.find('p', class_='text-blue-900 text-base font-bold text-right').text 
    except:
        price = 'N/A'
    return price

def get_meta(url):
    """
    Crawls the given URL, extracts the size of the property from the HTML content, and returns it.

    Args:
        url (str): The URL to crawl.

    Returns:
        str: The size of the property.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = soup.select('script')[-1].text
    
    meta_str = ''
    for metadata in json.loads(data)['props']['pageProps']['dataLayer'].keys():
        meta_str += json.loads(data)['props']['pageProps']['dataLayer'][metadata] + '|'

    meta = {}
    for m in meta_str.split('|'):
        if ':' in m:
            meta[m.split(':')[0]] = m.split(':')[1]
            
    df = pd.DataFrame(meta, index=[0])
    
    df['Address'] = url
    
    try:
        price = soup.find('p', class_='text-blue-900 text-base font-bold text-right').text 
    except:
        price = 'N/A'
        
    df['Price'] = price
    
    return df

def create_data_frame(filename):
    """
    Reads the addresses from the given file and creates a pandas DataFrame.

    Args:
        filename (str): The name of the file containing the addresses.

    Returns:
        pandas.DataFrame: A DataFrame containing the addresses and prices.
    """
    with open(filename, 'r') as file:
        addresses = file.readlines()
    
    df = (pd.DataFrame(addresses, columns=['Address'])
          .drop_duplicates()
          .reset_index(drop=True))

    # price_lst = [get_price(address) for address in df['Address']]
    # df['Price'] = price_lst
    
    meta_lst = [get_meta(address) for address in df['Address']]
    meta_df = pd.concat(meta_lst, ignore_index=True)
    
    final = pd.merge(df, meta_df, on='Address')
    return final
    

if __name__ == '__main__':
    url = 'https://www.boligsiden.dk/adresse/guldborgvej-20-9000-aalborg-08512731__20_______?udbud=1e3e17b2-7f65-4fbc-af1c-5fc3b3d72323'
    size = get_meta(url)
    size2 = get_meta(url)
    print(size)
    
    