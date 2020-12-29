import pytest
from ingestion import extractPackage, removeHtmlTags, editCategoryStr, filterPrice
import pandas as pd

mock_dir = './src/richart_wholesale_club/MOCK_PRODUCS.csv'
mock_dir2 = './src/richart_wholesale_club/MOCK_PRICE.csv'


# test to check remove tags function
def test_removeHtmlTags():
    df = pd.read_csv(mock_dir, sep='|').convert_dtypes()
    df = df.applymap(lambda x: removeHtmlTags(str(x)))
    # Basic test
    assert df.iloc[0]["ITEM_DESCRIPTION"] == \
        "CANASTO CONEJO F1 A 1UN", "test_removeHtmlTags failed"


# test to check the joining of the CATEGORY column
def test_editCategoryStr():
    df = pd.read_csv(mock_dir, sep='|').convert_dtypes()
    df['CATEGORY'] = df.apply(editCategoryStr, axis=1)
    # Basic test
    assert df.iloc[0]["CATEGORY"] == \
        "apparel|mens wear|men - t-shirts", "test_editCategoryStr() failed"


# test to check the extraction of packages
def test_extractPackage():
    df = pd.read_csv(mock_dir, sep='|').convert_dtypes()
    df = df.apply(extractPackage, axis=1)
    # case 0: Basic test
    assert df.iloc[0]["PACKAGE"] == "1UN", "test_extractPackage - case 0 failed"
    # case 1: whitespace and ignore/remove point
    assert df.iloc[1]["PACKAGE"] == "473 ML", "test_extractPackage - case 1 failed"


# check if we only get prices bigger than 0
def test_filterPrice():
    df = pd.read_csv(mock_dir2, sep='|').convert_dtypes()
    df = filterPrice(df)
    i = 0
    while i < len(df):
        assert df.iloc[i]["STOCK"] > 0, "test_filterPrice"
        i += 1
    pass
