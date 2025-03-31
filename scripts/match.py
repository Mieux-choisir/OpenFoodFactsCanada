import logging
import pandas as pd
from pymongo import MongoClient

from product_matcher import ProductMatcher


def extract_data(use_docker: bool = True):
    connection_string = (
        "mongodb://mongo:27017/" if use_docker else "mongodb://localhost:37017"
    )
    client = MongoClient(connection_string)
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
