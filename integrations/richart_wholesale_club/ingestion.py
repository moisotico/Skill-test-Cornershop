import numpy as np
import pandas as pd
import requests as rq
import re

# using compile for a regular expression
TAG_RE = re.compile(r'<[^>]+>')

# function to check urls
def getResponse(url):
    response = rq.get(url)
    print("GET:", url, "Status Code:", response.status_code)
    if response:
        return 0
    else:
        print('An error has occurred with the response:')
        return -1


# TODO: refactor
def checkFiles():
    try:
        f = open('./data/PRODUCTS.csv')
        f = open('./data/PRICES-STOCK.csv')
        return
    except FileNotFoundError:
        print("File not accessible, starting download")
        products_url = "https://cornershop-scrapers-evaluation.s3.amazonaws.com/public/PRODUCTS.csv"
        prices_url = "https://cornershop-scrapers-evaluation.s3.amazonaws.com/public/PRICES-STOCK.csv"

        getResponse(products_url)
        print("Downloading PRODUCTS.csv")
        products_df = pd.read_csv(products_url)
        products_df.to_csv('./data/PRODUCTS.csv', header=True)

        getResponse(prices_url)
        print("Downloading PRICES-STOCK.csv")
        prices_df = pd.read_csv(prices_url)
        prices_df.to_csv('./data/PRICES-STOCK.csv', header=True)


# Function to remove HTML tags via a regex to match one or more characters
#  inside a tag "< >""
def removeHtmlTags(string):
    string = TAG_RE.sub(' ', string)
    string = string.replace('\\"', ' ').strip()
    return string


# remove html tags
def filterHtml(df):    
    df1 = df.select_dtypes(include='string')
    df1 = df1.applymap(lambda x: removeHtmlTags(str(x)))
    df.update(df1)
    return df


# Main function to process csv files
def process_csv_files():
    # urls to obtain csv files
    products_dir = "./data/PRODUCTS.csv"
    prices_dir = "./data/PRICES-STOCK.csv"

    # Create dataframes & filter into PRODUCTS.csv
    products_df = pd.read_csv(products_dir, sep='|', index_col='SKU').convert_dtypes()
    print(products_df['ITEM_DESCRIPTION'].head())
    products_df = filterHtml(products_df)
    print(products_df['ITEM_DESCRIPTION'].head())

    products_df.to_csv('./out/PRODUCTS_mod.csv', header=True)

    '''
    # Create dataframes from PRICES-STOCK.csv
    prices_df = pd.read_csv(prices_dir, sep='|', index_col='SKU').convert_dtypes()
    # include only elements in stock
    prices_df[prices_df["STOCK"] > 0]
    prices_df.to_csv('./out/PRICES-STOCK_mod.csv', header=True)
    '''


if __name__ == "__main__":
    checkFiles()
    process_csv_files()
