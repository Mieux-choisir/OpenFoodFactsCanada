import logging
import dask.dataframe as dd
import pandas as pd
from pymongo import MongoClient
from pymongo.synchronous.database import Database


class ProductMatcher:
    def match_products(self):
        client = MongoClient("mongodb://localhost:37017/")
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

        all_fdc_ids = df2["id_match"].tolist()
        unmatched_ids = list(set(all_fdc_ids) - set(matched_ids))

        if final_products_collection.count_documents({}) > 0:
            logging.info("Final products already exist. Skipping insert.")
        else:
            unmatched_fdc_products = list(fdc_collection.find(
                {"id_match": {"$in": unmatched_ids}}
            ))
            if unmatched_fdc_products:
                final_products_collection.insert_many(unmatched_fdc_products)
                logging.info(f"Inserted {len(unmatched_fdc_products)} unmatched FDC products into final_products.")
            else:
                logging.info("No unmatched FDC products to insert.")

        logging.info(f"{len(matched_ids)} produits matchés entre les deux collections.")

    def __extract_data(self, db: Database):

        collection = db["off_products"]
        df1 = pd.DataFrame(list(collection.find({}, {"id_match": 1, "_id": 0})))

        # Vérifier les doublons
        doublons_off = df1[df1.duplicated(subset="id_match", keep=False)]

        if doublons_off.empty:
            logging.info("Pas de doublons dans off_products.")
        else:
            logging.warning(f"Il y a {len(doublons_off)} doublons dans off_products.")
            logging.warning(doublons_off)

        collection = db["fdc_products"]
        df2 = pd.DataFrame(list(collection.find({}, {"id_match": 1, "_id": 0})))

        doublons_fdc = df2[df2.duplicated(subset="id_match", keep=False)]

        if doublons_fdc.empty:
            logging.info("Pas de doublons dans fdc_products.")
        else:
            logging.warning(f"Il y a {len(doublons_fdc)} doublons dans fdc_products.")
            logging.warning(doublons_fdc)
        return df1, df2
