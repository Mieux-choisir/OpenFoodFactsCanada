import logging
from typing import List

from pymongo import MongoClient

from scripts.number_comparator import NumberComparator
from scripts.string_comparator import StringComparator


def merge_documents(off_product, fdc_product):
    if not isinstance(off_product, dict) or not isinstance(fdc_product, dict):
        return off_product if off_product is not None else fdc_product

    merged = {}
    for key in set(off_product.keys()).union(fdc_product.keys()):
        off_value = off_product.get(key)
        fdc_value = fdc_product.get(key)

        if isinstance(off_value, dict) and isinstance(fdc_value, dict):
            merged[key] = merge_documents(off_value, fdc_value)
        else:

            merged[key] = off_value if off_value is not None else fdc_value

    return merged


def compare_fields(off_product, fdc_product, merged_off_products_serving_size, matched_fdc_products_serving_size):
    string_comparator = StringComparator()
    number_comparator = NumberComparator()

    fields_to_skip = ["ecoscore_data", "modified_date", "available_date", "publication_date", "quantity", "data_source"]

    for key in set(off_product.keys()).union(fdc_product.keys()):
        off_value = off_product.get(key)
        fdc_value = fdc_product.get(key)

        if key in fields_to_skip:
            continue

        if isinstance(off_value, dict) and isinstance(fdc_value, dict):
            if not compare_fields(off_value, merged_off_products_serving_size, fdc_value,
                                  matched_fdc_products_serving_size):
                return False
        elif isinstance(off_value, str) and isinstance(fdc_value, str):
            if not string_comparator.compare_string(off_value, fdc_value):
                return False
        elif isinstance(off_value, List) and isinstance(fdc_value, List):
            if not string_comparator.compare_list(off_value, fdc_value):
                return False
        elif isinstance(off_value, float) and isinstance(fdc_value, float):
            if not number_comparator.check_value_per_100g(off_value, merged_off_products_serving_size, fdc_value,
                                                          matched_fdc_products_serving_size):
                return False
    return True


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )

    client = MongoClient("mongodb://localhost:37017/")
    db = client["openfoodfacts"]

    matched_off_products = db["matched_off_products"].find().sort("id_match", 1)
    matched_fdc_products = db["matched_fdc_products"].find().sort("id_match", 1)

    merged_off_products = db["merged_off_products"]

    unmergeable_off_products = db["unmergeable_off_products"]
    unmergeable_fdc_products = db["unmergeable_fdc_products"]

    final_products = db["final_products"]

    off_cursor = iter(matched_off_products)
    fdc_cursor = iter(matched_fdc_products)

    off_product = next(off_cursor, None)
    fdc_product = next(fdc_cursor, None)

    logging.info("Starting the product merge process")
    if db["merged_off_products"].count_documents({}) > 0:
        logging.info("Merged OFF products already exist. Skipping merging.")
    else:
        while off_product and fdc_product:
            if off_product["id_match"] == fdc_product["id_match"]:
                merged_off_product = merge_documents(off_product, fdc_product)

                merged_off_products.insert_one(merged_off_product)

                off_product = next(off_cursor, None)
                fdc_product = next(fdc_cursor, None)

        logging.info("Product merge completed. Now comparing merged products with FDC products.")

    merged_off_products = db["merged_off_products"].find().sort("id_match", 1)
    matched_fdc_products = db["matched_fdc_products"].find().sort("id_match", 1)

    off_cursor = iter(merged_off_products)
    fdc_cursor = iter(matched_fdc_products)

    off_product = next(off_cursor, None)
    fdc_product = next(fdc_cursor, None)

    while off_product and fdc_product:
        if off_product["id_match"] == fdc_product["id_match"]:
            if compare_fields(off_product, fdc_product, off_product["serving_size"], fdc_product["serving_size"]):
                final_products.insert_one(off_product)
            else:
                unmergeable_off_products.insert_one(off_product)
                unmergeable_fdc_products.insert_one(fdc_product)

        off_product = next(off_cursor, None)
        fdc_product = next(fdc_cursor, None)

    logging.info("Comparison completed.")


if __name__ == "__main__":
    main()
