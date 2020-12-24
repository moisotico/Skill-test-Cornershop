import numpy as np
import pandas as pd
import requests as rq
import re
import os

# using compile for a regular expression
TAG_RE = re.compile(r'<[^>]+>')

# function to check urls


def getResponse(url):
    response = rq.get(url, allow_redirects=True)
    print("GET:", url, "Status Code:", response.status_code)
    if response:
        return response
    else:
        print('An error has occurred with the response:')
        return -1


# TODO: refactor
def checkFiles(filename):
    filedir = './data/'
    filedir += str(filename)
    try:
        # check if file exists
        f = open(filedir)
        return
    except FileNotFoundError:
        try:
            os.mkdir("./data")
        except FileExistsError:
            pass
        # Get files from bucket
        print("File " + str(filedir) + " not accessible")
        print("Checking url...")
        url = "https://cornershop-scrapers-evaluation.s3.amazonaws.com/public/" + \
            str(filename)
        r = getResponse(url)
        print("Downloading " + filename)
        open(filedir, 'wb').write(r.content)
        print("Finished downloading " + filedir + "!")
        pass

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
    products_df = pd.read_csv(products_dir, sep='|',
                              index_col='SKU').convert_dtypes()
    products_df = filterHtml(products_df)
    os.mkdir("./out")

    products_df.to_csv('./out/PRODUCTS_mod.csv', header=True)

    # Create dataframes from PRICES-STOCK.csv
    prices_df = pd.read_csv(prices_dir, sep='|',
                            index_col='SKU').convert_dtypes()
    # include only elements in stock
    prices_df[prices_df["STOCK"] > 0]
    prices_df.to_csv('./out/PRICES-STOCK_mod.csv', header=True)


if __name__ == "__main__":
    checkFiles("PRODUCTS.csv")
    checkFiles("PRICES-STOCK.csv")
    process_csv_files()
