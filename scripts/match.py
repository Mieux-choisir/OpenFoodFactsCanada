import logging
import pandas as pd
from pymongo import MongoClient

from product_matcher import ProductMatcher


def extract_data() -> (pd.DataFrame, pd.DataFrame):
    """Extracts products ids from the collections off_products and fdc_products into dataframes"""
    client = MongoClient("mongodb://localhost:37017/")
    db = client["openfoodfacts"]

    collection = db["off_products"]
    df1 = pd.DataFrame(list(collection.find({}, {"id_match": 1, "_id": 0})))

    collection = db["fdc_products"]
    df2 = pd.DataFrame(list(collection.find({}, {"id_match": 1, "_id": 0})))

    return df1, df2


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )

    product_matcher = ProductMatcher()

    product_matcher.match_products()


if __name__ == "__main__":
    main()
