import pandas as pd
from pymongo import MongoClient

from scripts.product_matcher import ProductMatcher


def extract_data():
    client = MongoClient("mongodb://localhost:37017/")
    db = client["openfoodfacts"]

    collection = db["off_products"]
    df1 = pd.DataFrame(list(collection.find({}, {"id_match": 1, "_id": 0})))

    collection = db["fdc_products"]
    df2 = pd.DataFrame(list(collection.find({}, {"id_match": 1, "_id": 0})))

    return df1, df2


def main():
    product_matcher = ProductMatcher()

    product_matcher.match_products()


if __name__ == "__main__":
    main()
