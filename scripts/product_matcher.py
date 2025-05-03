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

    def match_products(self, use_docker: bool = True):
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

        off_ids = self.__stream_ids(off_collection)
        fdc_ids = self.__stream_ids(fdc_collection)

        matched_ids = off_ids & fdc_ids
        unmatched_fdc_ids = fdc_ids - matched_ids

        matched_off_collection = db["matched_off_products"]
        matched_fdc_collection = db["matched_fdc_products"]
        unmatched_fdc_collection = db["unmatched_fdc_products"]

        if matched_off_collection.count_documents({}) > 0:
            logging.info("Matched OFF products already exist. Skipping insert.")
        else:
            cursor = off_collection.find({"id_match": {"$in": list(matched_ids)}})
            self.__batch_insert(cursor, matched_off_collection)
            logging.info(f"Inserted matched OFF products.")

        if matched_fdc_collection.count_documents({}) > 0:
            logging.info("Matched FDC products already exist. Skipping insert.")
        else:
            cursor = fdc_collection.find({"id_match": {"$in": list(matched_ids)}})
            self.__batch_insert(cursor, matched_fdc_collection)
            logging.info(f"Inserted matched FDC products.")

        if unmatched_fdc_collection.count_documents({}) > 0:
            logging.info("Unmatched FDC products already exist. Skipping insert.")
        else:
            cursor = fdc_collection.find({"id_match": {"$in": list(unmatched_fdc_ids)}})
            self.__batch_insert(cursor, unmatched_fdc_collection)
            logging.info(f"Inserted unmatched FDC products.")

        logging.info(
            f"{len(matched_ids)} matched products between the two collections."
        )


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

    @staticmethod
    def __stream_ids(collection) -> set:
        """Streams all 'id_match' values from a collection into a set."""
        ids = set()
        for doc in collection.find({}, {"id_match": 1, "_id": 0}):
            if "id_match" in doc:
                ids.add(doc["id_match"])
        return ids
    
    @staticmethod
    def __batch_insert(cursor, collection, batch_size=1000):
        """Inserts documents from a cursor into a collection in batches."""
        batch = []
        for doc in cursor:
            batch.append(doc)
            if len(batch) >= batch_size:
                collection.insert_many(batch)
                batch.clear()
        if batch:
            collection.insert_many(batch)