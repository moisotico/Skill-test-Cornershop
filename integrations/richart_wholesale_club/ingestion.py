import numpy as np
import pandas as pd
import requests as rq


def process_csv_files():
    # urls to obtain dataframe
    products_url = "https://cornershop-scrapers-evaluation.s3.amazonaws.com/public/PRODUCTS.csv"
    prices_url = "https://cornershop-scrapers-evaluation.s3.amazonaws.com/public/PRICES-STOCK.csv"

    response = rq.get(prices_url)
    print("Status Code:", response.status_code)
    if response:
        print('Success!')
    else:
        print('An error has occurred.')
        return -1
    # put the dataframe into PRODUCTS.csv
    products_df = pd.read_csv(products_url, sep='|')
    '''
    products_df.to_csv('./PRODUCTS.csv', index=False, header=True)
    '''
    # put the dataframe into PRODUCTS.csv
    prices_df = pd.read_csv(prices_url, sep='|')
    print(prices_df.head())
    print(products_df.head())
    # prices_df.to_csv('./PRICES-STOCK.csv', index=False, header=True)


if __name__ == "__main__":
    process_csv_files()
