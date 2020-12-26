import numpy as np
import pandas as pd
import requests as rq
import re
import os
from credentials import GRAND_TYPE, CLIENT_ID, CLIENT_SECRET, BASE_URL

# Get credentials variables. TODO: check if this is safe
grant_type = GRAND_TYPE
cliend_id = CLIENT_ID
client_secret = CLIENT_SECRET
base_url = BASE_URL


# function to check urls
def getResponse(url):
    response = rq.get(url, allow_redirects=True)
    print("GET:", url, "Status Code:", response.status_code)
    if response:
        return response
    else:
        print('An error has occurred with the response:')
        return -1


def checkDir(dir):
    try:
        os.mkdir(dir)
    except FileExistsError:
        pass


# Check if csv files exist, if not then download
def checkFile(filename):
    filedir = './data/'
    filedir += str(filename)
    try:
        # check if file exists
        f = open(filedir)
        return
    except FileNotFoundError:
        checkDir("./data")
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
    string = re.sub('<[^>]+>',' ', string)
    string = string.replace('\\"', ' ').strip()
    return string


# Edit Category to lowercase and join to "|" and Subcategory column string
def editCategoryStr(row):
    result = str(row['CATEGORY']).lower()
    result += "|"
    result += str(row['SUB_CATEGORY'])
    return result


# Join Category and Subcategory
def joinCategories(df):
    df['CATEGORY'] = df.apply(editCategoryStr, axis=1)
    df = df.drop('SUB_CATEGORY', axis=1)
    return df


# clean Products csv removing tags & strings, and
# joining Categories & subcategoires
def filterProducts(df):
    df1 = df.select_dtypes(include='string')
    df1 = df1.applymap(lambda x: removeHtmlTags(str(x)))
    df.update(df1)
    df = joinCategories(df)
    return df


# remove elements with stock =< 0
def filterPrice(df):
    df = df[df['STOCK'] > 0]
    return df


# Output CSVs
def mergeDfsOut(df1, df2):
    checkDir("./out")
    df1.to_csv('./out/PRICES-STOCK_mod.csv', header=True)
    df2.to_csv('./out/PRODUCTS_mod.csv', header=True)
    joint_df = pd.merge(df1, df2,
                        left_index=True, right_index=True, how='outer')
    joint_df.to_csv('./out/JOINT.csv', header=True)
    return joint_df


# TODO: get the token
def getCredentials():
    url = f"{base_url}/oauth/token?client_id={cliend_id}" \
        f"&client_secret={client_secret}" \
        f"&grant_type={grant_type}"
    payload = {}
    headers = {}
    response = rq.request("POST", url, headers=headers, data=payload)
    r = response.json()
    access_token = r.get('access_token')
    return access_token


# Requests
def APIRequests():
    cred_response = getCredentials()
    print(cred_response)
    pass

# Main function to process csv files


def process_csv_files():
    # urls to obtain csv files
    products_dir = "./data/PRODUCTS.csv"
    prices_dir = "./data/PRICES-STOCK.csv"
    # Create dataframes & filter into PRODUCTS.csv, SKU as unique index
    products_df = pd.read_csv(products_dir, sep='|',
                              index_col='SKU').convert_dtypes()
    products_df = filterProducts(products_df)

    # Create dataframes from PRICES-STOCK.csv and filter to
    # only elements in stock
    prices_df = pd.read_csv(prices_dir, sep='|',
                            index_col='SKU').convert_dtypes()
    prices_df = filterPrice(prices_df)
    merged_df = mergeDfsOut(prices_df, products_df)
    APIRequests()
    pass


if __name__ == "__main__":
    checkFile("PRODUCTS.csv")
    checkFile("PRICES-STOCK.csv")
    process_csv_files()
