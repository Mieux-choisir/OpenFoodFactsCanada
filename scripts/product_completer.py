import logging
from collections import Counter

from pymongo import MongoClient

from scripts.statistics_creator import StatisticsCreator


class ProductCompleter:
    def complete_products(self, use_docker=True):

        connection_string = (
            "mongodb://mongo:27017/" if use_docker else "mongodb://localhost:37017"
        )

        client = MongoClient(connection_string)
        db = client["openfoodfacts"]

        matched_off_products = db["matched_off_products"].find().sort("id_match", 1)
        matched_fdc_products = db["matched_fdc_products"].find().sort("id_match", 1)

        nb_matched_off_products = db["matched_off_products"].count_documents({})
        nb_matched_fdc_products = db["matched_fdc_products"].count_documents({})

        final_products = db["final_products"]

        if final_products.count_documents({}) > 0:
            logging.info("Final products table already exist. Deleting old version.")
            final_products.drop()

        off_cursor = iter(matched_off_products)
        fdc_cursor = iter(matched_fdc_products)

        off_product = next(off_cursor, None)
        fdc_product = next(fdc_cursor, None)

        logging.info("Starting the product merge process")
        if db["merged_off_products"].count_documents({}) > 0:
            logging.info("Merged OFF products already exist. Skipping merging.")
        else:
            count_merged = 0
            count_skipped = 0

            overwrite_counter = Counter()
            complete_counter = Counter()

            while off_product and fdc_product:
                if off_product["id_match"] == fdc_product["id_match"]:
                    merged_off_product, overwritten, completed = self.__merge_documents(
                        off_product, fdc_product
                    )

                    overwrite_counter.update(overwritten)
                    complete_counter.update(completed)

                    if merged_off_product != off_product:
                        final_products.insert_one(merged_off_product)
                        count_merged += 1
                    else:
                        count_skipped += 1

                    off_product = next(off_cursor, None)
                    fdc_product = next(fdc_cursor, None)

            StatisticsCreator().make_merge_summary(
                overwrite_counter,
                complete_counter,
                count_skipped,
                nb_matched_off_products,
                nb_matched_fdc_products,
            )

    def __merge_documents(self, off_product, fdc_product, parent_key=""):
        if not isinstance(off_product, dict) or not isinstance(fdc_product, dict):
            return off_product if off_product is not None else fdc_product, [], []

        merged = {}
        overwritten_fields = []
        completed_fields = []

        for key in set(off_product.keys()).union(fdc_product.keys()):
            full_key = f"{parent_key}.{key}" if parent_key else key
            off_value = off_product.get(key)
            fdc_value = fdc_product.get(key)

            if key == "off_categories_en":
                if (
                    off_value is not None
                    and fdc_value is not None
                    and isinstance(off_value, list)
                    and isinstance(fdc_value, list)
                ):
                    new_items = [item for item in fdc_value if item not in off_value]
                    if new_items:
                        merged[key] = off_value + new_items
                        overwritten_fields.append(full_key)
                    else:
                        merged[key] = off_value
                elif isinstance(fdc_value, list) and off_value is None:
                    merged[key] = fdc_value
                    completed_fields.append(full_key)
                else:
                    merged[key] = off_value
            elif key in [
                "_id",
                "brands",
                "fdc_products",
                "food_groups_en",
                "product_name",
                "id_original",
                "brand_owner",
                "ingredients_text",
            ]:
                merged[key] = off_value
            elif isinstance(off_value, dict) and isinstance(fdc_value, dict):
                merged_value, sub_overwritten, sub_completed = self.__merge_documents(
                    off_value, fdc_value, full_key
                )
                merged[key] = merged_value
                overwritten_fields.extend(sub_overwritten)
                completed_fields.extend(sub_completed)
            else:
                if fdc_value is not None and fdc_value != off_value:
                    if off_value is None:
                        completed_fields.append(full_key)
                    else:
                        overwritten_fields.append(full_key)
                    merged[key] = fdc_value
                else:
                    merged[key] = off_value

        return merged, overwritten_fields, completed_fields
