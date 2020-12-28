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


# check if directoriy exists, else create it
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
        print("Finished downloading to" + filedir)
        pass


# Function to remove HTML tags via a regex to match one or more characters
#  inside a tag "< >""
def removeHtmlTags(string):
    string = re.sub('<[^>]+>', ' ', string)
    string = string.replace('\\"', ' ').strip()
    return string


# Edit Category to lowercase and join to "|" and Subcategories column string
def editCategoryStr(row):
    result = str(row['CATEGORY'])
    result += "|"
    result += str(row['SUB_CATEGORY'])
    result += "|"
    result += str(row['SUB_SUB_CATEGORY'])
    return result.lower()


# Read dataframe's item description and  match a number(\d) and pattern
# (from a list of units) to get the package of the product
def extractPackage(df):
    units = ["UN", "KGS", "KG", "GR", "GRS", "G", "ML", "CJA"]
    for pattern in units:
        match = re.findall(r"\b\d\.?\+?\d*\s?"+pattern+r"\b",
                           df["ITEM_DESCRIPTION"])
        if match:
            last_match = match[-1].strip()
            print(df["ITEM_DESCRIPTION"])
            df["ITEM_DESCRIPTION"] = re.sub(
                last_match + r"\.?", '', df["ITEM_DESCRIPTION"])
            df["ITEM_DESCRIPTION"] = re.sub(' +', ' ', df["ITEM_DESCRIPTION"])

            df["PACKAGE"] = last_match
            print("description:", df["ITEM_DESCRIPTION"],
                  "Package: ", df["PACKAGE"])
            return df
    return df


# Extract the package and store it in its corresponding field in the df
def filterPackage(df):
    df = df.apply(extractPackage, axis=1)
    return df


# Join Category and Subcategory
def joinCategories(df):
    df['CATEGORY'] = df.apply(editCategoryStr, axis=1)
    df = df.drop('SUB_CATEGORY', axis=1)
    df = df.drop('SUB_SUB_CATEGORY', axis=1)
    return df


# clean Products csv removing tags & strings, and
# joining Categories & subcategoires
def filterProducts(df):
    df1 = df.select_dtypes(include='string')
    df1 = df1.applymap(lambda x: removeHtmlTags(str(x)))
    df.update(df1)
    df = joinCategories(df)
    df = filterPackage(df)
    return df


# remove elements with stock =< 0
def filterPrice(df):
    df = df[df['STOCK'] > 0]
    return df


# Output CSVs
def mergeDfsOut(df1, df2):
    checkDir("./out")
    joint_df = pd.merge(df1, df2,
                        left_index=True, right_index=True, how='outer')
    joint_df.to_csv('./out/JOINT.csv', header=True)
    return joint_df


# Search for a specific merchant in a JSON formatted response
def searchMerchant(merchant, items):
    for keyvalues in items['merchants']:
        if keyvalues['name'].lower() == merchant.lower():
            return keyvalues['id']
    return None


# get a valid access token
def getCredentials():
    url = f"{base_url}/oauth/token?client_id={cliend_id}" \
        f"&client_secret={client_secret}" \
        f"&grant_type={grant_type}"
    payload = {}
    headers = {}
    response = rq.request("POST", url, headers=headers, data=payload)
    print("getCredentials: ", response.status_code)
    r = response.json()
    return r.get('access_token')


# get Richart's Wholesale Club ID
def getMerchants(token, name):
    url = f"{base_url}/api/merchants"
    payload = {}
    headers = {
        'token': f'Bearer {token}'
    }
    response = rq.request("GET", url, headers=headers, data=payload)
    print("getMerchants: ", response.status_code)
    r = response.json()
    merchant_id = searchMerchant(name, r)
    return merchant_id, r


# update is_active field to true
def updateMerchant(token, merchant_id, merchant):

    url = f"{base_url}/api/merchants/{merchant_id}"

    payload = {
        "can_be_deleted": False,
        "can_be_updated": True,
        "id": f"{merchant_id}",
        "is_active": True,
        "name": f"{merchant}"
    }
    headers = {
        'token': f'Bearer {token}'
    }
    response = rq.request("PUT", url, headers=headers, json=payload)
    print("updateMerchant: ", response.status_code)
    pass


# delete a merchant if it finds the string
def deleteMerchant(token, merchant, response):
    merchant_id = searchMerchant(merchant, response)
    if merchant_id is not None:
        url = f"{base_url}/api/merchants/{merchant_id}"
        payload = {}
        headers = {
            'token': f'Bearer {token}'
        }
        response = rq.request("DELETE", url, headers=headers, data=payload)
        print("deleteMerchant: ", response.status_code)
        return 0
    print("Merchant not found!")
    return -1


'''
def sendProducts(token, merchant_id, merchant, df):
    url = "{{base_url}}/api/products"

    payload = {
        "merchant_id": f"{merchant_id}",
        "sku": f"{sku}",
        "barcodes": ["62773501448"],
        "brand": f"{brand_name}",
        "name": f"{item_name}",
        "description": f"{item_description}",
        "package": f"{package}",
        "image_url": f"{item_img}",
        "category": f"{category}",
        "url": "None",
        "branch_products": [{
            "branch": "Heartland Supercentre",
            "stock": stock,
            "price": price,
            "branch": "Heartland Supercentre",
            "stock": stock,
            "price": price
        }]
    }
    headers = {
        'token': f'Bearer {token}'
    }

    #response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.text.encode('utf8'))
    pass
'''

# get the 100 most expensive products of each branch and their package


def getMostExpensive(token, df, merchant_id, merchant):
    branches = df['BRANCH'].unique().dropna()
    for i in branches:
        me_df = df[df["BRANCH"] == i].nlargest(100, 'PRICE')
        #sendProducts(token, merchant_id, merchant, me_df)
    pass


# Requests for the heroku API:
def APIRequests(df):
    merchant = "Richard\'s"
    valid_token = getCredentials()
    merchant_id, r = getMerchants(valid_token, merchant)
    '''
    TODO: remove comment
    updateMerchant(valid_token, merchant_id, merchant)
    deleteMerchant(valid_token, "Beauty", r)
    '''
    getMostExpensive(valid_token, df, merchant, merchant_id)
    pass


# Main function to process csv files
def process_csv_files():
    # urls to obtain csv files
    products_dir = "./data/PRODUCTS.csv"
    prices_dir = "./data/PRICES-STOCK.csv"
    # Create dataframes & filter into PRODUCTS.csv, SKU as unique index
    print("reading " + products_dir)
    products_df = pd.read_csv(products_dir, sep='|',
                              index_col='SKU').convert_dtypes()
    products_df = filterProducts(products_df)

    # Create dataframes from PRICES-STOCK.csv and filter to
    # only elements in stock
    print("reading " + prices_dir)
    prices_df = pd.read_csv(prices_dir, sep='|',
                            index_col='SKU').convert_dtypes()
    prices_df = filterPrice(prices_df)
    products_df = mergeDfsOut(products_df, prices_df)
    out_dir = './out/JOINT.csv'
    print("reading " + out_dir)
    # TODO: erase
    '''
    products_df = pd.read_csv(out_dir, index_col='SKU').convert_dtypes()

    '''
    # TODO: finish testing
    print("Accesing API requests")
    APIRequests(products_df)
    pass


if __name__ == "__main__":
    checkFile("PRODUCTS.csv")
    checkFile("PRICES-STOCK.csv")
    process_csv_files()
