import logging

from pymongo import MongoClient


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

    final_products = db["final_products"]

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
        while off_product and fdc_product:
            if off_product["id_match"] == fdc_product["id_match"]:
                merged_off_product = merge_documents(off_product, fdc_product)

                if merged_off_product != off_product:
                    final_products.insert_one(merged_off_product)
                    count_merged += 1
                else:
                    count_skipped += 1

                off_product = next(off_cursor, None)
                fdc_product = next(fdc_cursor, None)

        logging.info(
            f"Product merge completed. Inserted: {count_merged}, Skipped: {count_skipped}"
        )


if __name__ == "__main__":
    main()
