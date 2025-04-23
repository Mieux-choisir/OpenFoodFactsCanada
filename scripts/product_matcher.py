import logging
import dask.dataframe as dd
import pandas as pd
from pymongo import MongoClient
from pymongo.synchronous.database import Database


class ProductMatcher:
    """
    This is a class that matches products from different collections.

    Methods:
        match_products(): Matches products that have the same id between the off_products and the fdc_products collections, and then add the matched
        products to matched_products collections
    """

    def match_products(self, use_docker: bool = True) -> list[str]:
        """Matches products that have the same id between the off_products and the fdc_products collections.
        Then adds the matched OFF products to the matched_off_products collection and the matched FDC products to the matched_fdc_products collection.
        """
        connection_string = (
            "mongodb://mongo:27017/" if use_docker else "mongodb://localhost:37017"
        )
        client = MongoClient(connection_string)
        db = client["openfoodfacts"]

        off_collection = db["off_products"]
        fdc_collection = db["fdc_products"]

        df1, df2 = self.__extract_data(db)

        ddf1 = dd.from_pandas(df1, npartitions=1)
        ddf2 = dd.from_pandas(df2, npartitions=1)

        ddf1 = ddf1.set_index("id_match")
        ddf2 = ddf2.set_index("id_match")

        merged = ddf1.join(ddf2, how="inner")

        matched_ids = merged.compute().index.tolist()

        matched_off_collection = db["matched_off_products"]
        matched_fdc_collection = db["matched_fdc_products"]
        final_products_collection = db["final_products"]

        if matched_off_collection.count_documents({}) > 0:
            logging.info("Matched OFF products already exist. Skipping insert.")
        else:
            matched_off_products = off_collection.find(
                {"id_match": {"$in": list(matched_ids)}}
            )
            matched_off_collection.insert_many(matched_off_products)
            logging.info(f"Inserted {len(matched_ids)} matched OFF products.")

        if matched_fdc_collection.count_documents({}) > 0:
            logging.info("Matched FDC products already exist. Skipping insert.")
        else:
            matched_fdc_products = fdc_collection.find(
                {"id_match": {"$in": list(matched_ids)}}
            )
            matched_fdc_collection.insert_many(matched_fdc_products)

        logging.info(
            f"{len(matched_ids)} matched products between the two collections."
        )

        return matched_ids

    @staticmethod
    def __extract_data(db: Database) -> (pd.DataFrame, pd.DataFrame):
        """Extracts the data from the off_products and fdc_products collections as dataframes"""
        collection = db["off_products"]
        df1 = pd.DataFrame(list(collection.find({}, {"id_match": 1, "_id": 0})))

        # Check for duplicates
        off_duplicates = df1[df1.duplicated(subset="id_match", keep=False)]

        if off_duplicates.empty:
            logging.info("No duplicates in off_products.")
        else:
            logging.warning(
                f"There are {len(off_duplicates)} duplicates in off_products."
            )
            logging.warning(off_duplicates)

        collection = db["fdc_products"]
        df2 = pd.DataFrame(list(collection.find({}, {"id_match": 1, "_id": 0})))

        fdc_duplicates = df2[df2.duplicated(subset="id_match", keep=False)]

        if fdc_duplicates.empty:
            logging.info("No duplicates in fdc_products.")
        else:
            logging.warning(
                f"There are {len(fdc_duplicates)} duplicates in fdc_products."
            )
            logging.warning(fdc_duplicates)
        return df1, df2
