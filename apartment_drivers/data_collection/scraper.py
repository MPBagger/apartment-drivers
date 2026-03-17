import requests
from bs4 import BeautifulSoup
import pandas as pd
import json


def _get_estate_data(url):
    """
    Fetches the page and extracts the estate data from the boliga-app-state script tag.

    Args:
        url (str): The URL to crawl.

    Returns:
        dict: The estate data dictionary, or None if not found.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    app_state_tag = soup.find('script', id='boliga-app-state')
    if not app_state_tag:
        return None

    raw = app_state_tag.text.replace('&q;', '"')
    app_state = json.loads(raw)

    # Find the oneurl key which contains property data
    for key in app_state:
        if 'oneurl' in key:
            estates = app_state[key].get('body', {}).get('estate', [])
            if estates:
                return estates[0]
    return None


def get_price(url):
    """
    Crawls the given URL, extracts the price from the HTML content, and returns it.

    Args:
        url (str): The URL to crawl.

    Returns:
        str: The price of the property.
    """
    estate = _get_estate_data(url)
    if estate and estate.get('price'):
        return str(estate['price'])
    return 'N/A'


def get_meta(url):
    """
    Crawls the given URL, extracts property metadata, and returns it as a DataFrame.

    Args:
        url (str): The URL to crawl.

    Returns:
        pandas.DataFrame: A single-row DataFrame with the property metadata.
    """
    estate = _get_estate_data(url)
    if estate is None:
        return pd.DataFrame({'Address': [url], 'Price': ['N/A']})

    meta = {
        'propertyType': estate.get('propertyType'),
        'energyClass': estate.get('energyClass'),
        'rooms': estate.get('rooms'),
        'size': estate.get('size'),
        'lotSize': estate.get('lotSize'),
        'buildYear': estate.get('buildYear'),
        'squaremeterPrice': estate.get('squaremeterPrice'),
        'daysForSale': estate.get('daysForSale'),
        'city': estate.get('city'),
        'zipCode': estate.get('zipCode'),
        'street': estate.get('street'),
        'latitude': estate.get('latitude'),
        'longitude': estate.get('longitude'),
        'basementSize': estate.get('basementSize'),
    }

    df = pd.DataFrame(meta, index=[0])
    df['Address'] = url
    df['Price'] = estate.get('price', 'N/A')

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
    url = 'https://www.boliga.dk/adresse/assensvej-39-5853-oerbaek-1817003112'
    price = get_price(url)
    print(price)
    meta = get_meta(url)
    print(meta)
    
    