from crawler import boligsiden_crawler
from scraper import create_data_frame

if __name__ == '__main__':
    url = 'https://www.boligsiden.dk/tilsalg?page='
    filename = 'data/addresses.txt'
    boligsiden_crawler(url, filename, 1)
    df = create_data_frame(filename)
    df.to_csv('data/raw.csv', index=False)
    print(df)