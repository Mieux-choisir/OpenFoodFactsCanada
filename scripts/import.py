import csv
import gzip
import zipfile

import ijson
import json
import os
import requests
import sys
import logging

from pymongo import MongoClient
from tenacity import retry, stop_after_attempt, wait_fixed

from product import Product
from scripts.mapper.off_csv_mapper import map_off_row_to_product
from scripts.mapper.off_jsonl_mapper import map_off_dict_to_product
from scripts.mapper.fdc_mapper import (
    map_fdc_dict_to_product,
    normalise_ingredients_list,
    Ingredients,
    NutriscoreData,
    EcoscoreData,
    NutritionFacts,
    NovaData,
)

########################################################################################################################
# VARIABLES GLOBALES ###################################################################################################
########################################################################################################################

# URL of the off csv file
off_csv_url = (
    "https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.csv.gz"
)

# URL of the off json file
off_jsonl_url = "https://static.openfoodfacts.org/data/openfoodfacts-products.jsonl.gz"

# URL of the fdc file
fdc_json_url = "https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_branded_food_json_2024-10-31.zip"


########################################################################################################################
# TELECHARGEMENT DES FICHIERS ##########################################################################################
########################################################################################################################


def download_and_decompress_data(
    source_url: str,
    compressed_file: str,
    compressed_file_extension: str,
    decompressed_file: str,
) -> None:
    if os.path.exists(decompressed_file):
        logging.info(f"File {decompressed_file} already exists. Skipping download.")
        return

    download_file(source_url, compressed_file)
    decompress_file(compressed_file, compressed_file_extension, decompressed_file)
    cleanup_file(compressed_file)


def download_file(
    url: str,
    download_path: str,
    chunk_size: int = 1024 * 1024,
    max_retries: int = 5,
    timeout: int = 60,
) -> None:
    """Downloads a file from a given url into a given download path"""
    logging.info(f"Downloading file from {url}...")

    @retry(stop=stop_after_attempt(max_retries), wait=wait_fixed(5))
    def download():
        try:
            with requests.get(url, stream=True, timeout=timeout) as response:
                response.raise_for_status()
                with open(download_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        f.write(chunk)
            logging.info(f"Download complete: {download_path}")
        except requests.exceptions.RequestException as exc:
            logging.error(f"Error downloading file {exc}")
            raise

    try:
        download()
    except Exception as e:
        logging.error(f"Download failed after {max_retries} attempts: {e}")
        raise


def decompress_file(
    compressed_file: str,
    compressed_file_extension: str,
    output_file: str,
    buffer_size: int = 1024 * 1024,
) -> None:
    logging.info(f"Decompressing {compressed_file} into {output_file}...")

    if compressed_file_extension == ".gz":
        decompress_gz_file(compressed_file, output_file, buffer_size)
    elif compressed_file_extension == ".zip":
        decompress_zip_file(compressed_file, output_file, buffer_size)
    else:
        logging.error(f"Unsupported file extension: {compressed_file_extension}")
        raise ValueError(
            f"Unsupported file extension: {compressed_file_extension}. Supported extensions are '.gz' and '.zip'."
        )
    logging.info("Decompression complete")


def decompress_gz_file(
    gz_file: str, output_file: str, buffer_size: int = 1024 * 1024
) -> None:
    """Decompresses a .gz file into a file named output_file"""
    with gzip.open(gz_file, "rb") as f_in:
        with open(output_file, "wb") as f_out:
            while chunk := f_in.read(buffer_size):
                f_out.write(chunk)


def decompress_zip_file(
    zip_file: str, output_file: str, buffer_size: int = 1024 * 1024
) -> None:
    """Decompresses a .zip file into a file named output_file"""
    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        with zip_ref.open(zip_ref.namelist()[0], "r") as f_in:
            with open(output_file, "wb") as f_out:
                while chunk := f_in.read(buffer_size):
                    f_out.write(chunk)


########################################################################################################################
# IMPORTS ##############################################################################################################
########################################################################################################################


def import_json_fdc_data(filename: str) -> list[Product]:
    """Imports the data of branded food in a json file into a list of strings for each branded food"""
    products = []
    with open(filename, "r", encoding="utf-8") as file:
        logging.info("Extracting Food Data Central products...")
        for obj in ijson.items(file, "BrandedFoods.item"):
            if (
                obj["marketCountry"] == "United States"
            ):  # there are also products from New Zealand
                prod = map_fdc_dict_to_product(obj)
                products.append(prod)
    logging.info("FDC data imported")
    return products


def import_jsonl_off_data(filename: str, limit: int = None) -> list[Product]:
    """Imports the data of canadian food in a json file into a list of products"""
    if limit is not None:
        logging.info(
            f"Extracting {limit} products from Open Food Facts jsonl dataset..."
        )
    else:
        logging.info("Extracting all products from Open Food Facts jsonl dataset...")

    products = []
    n = 0

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            try:
                obj = json.loads(line.strip())
                prod = map_off_dict_to_product(obj)
                if prod is not None:
                    products.append(prod)
                n += 1
                if limit is not None and n > limit:
                    break
            except json.JSONDecodeError as e:
                logging.info(f"Error parsing line: {line}. Error: {e}")

    logging.info("OFF data imported")
    return products


def import_csv_off_data(filename: str, limit: int = None) -> list[Product]:
    """Imports the data of canadian food in a csv file into a list of products

     Args:
        filename: The path to the imported Open Food Facts csv file
        limit (int, optional): The number of lines to read from the dataset. Defaults to None.
    Returns:
        list[Product]: A list of Product objects extracted from the dataset.
    """
    if limit is not None:
        logging.info(f"Extracting {limit} products from Open Food Facts csv dataset...")
    else:
        logging.info("Extracting all products from Open Food Facts csv dataset...")

    # Increase the CSV field size limit to avoid the error:
    # _csv.Error: field larger than field limit (131072)
    csv.field_size_limit(2**30)

    products: list[Product] = []
    n = 0
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)

        for row in reader:
            product = map_off_row_to_product(row, header)

            if product is None:
                continue

            products.append(product)
            n += 1

            if limit is not None and n >= limit:
                break

    logging.info("OFF data imported")
    return products


########################################################################################################################
# COMPLETION ###########################################################################################################
########################################################################################################################


def complete_products_data(
    off_products: list[Product], fdc_products: list[Product]
) -> list[Product]:
    """Completes the obtained OFF products with the data in the FDC products and returns a new completed list
    of products"""
    logging.info("Completing missing data for OFF products...")

    products = []
    for fdc_product in fdc_products:
        # try to find the same product in off products
        # if present : add the missing values
        off_product = find_product(fdc_product, off_products)
        if off_product is not None:
            new_product = complete_product(off_product, fdc_product)
            products.append(new_product)
        # else : add the whole product
        else:
            products.append(fdc_product)
        if len(products) > 100:
            continue
    logging.info("OFF products completed")
    return products


def find_product(searched_product: Product, products: list[Product]) -> Product | None:
    """Searches the product in the products list based on its id and returns it if it finds it"""
    for product in products:
        if product.id == searched_product.id:
            return product
    return None


def complete_product(off_product: Product, fdc_product: Product) -> Product:
    """Checks each field of the off_product and completes the ones that are missing values"""
    for field, fdc_value in fdc_product.__dict__.items():
        # if the off_product field is None, an empty list or a list of empty strings, complete it
        off_value = getattr(off_product, field, None)
        if off_value is None or (
            isinstance(off_value, list)
            and ((not off_value) or v == "" for v in off_value)
        ):
            setattr(off_product, field, fdc_value)
        elif isinstance(off_value, Ingredients):
            setattr(off_product, field, update_ingredients_values(off_value, fdc_value))
        elif isinstance(off_value, NutriscoreData):
            setattr(off_product, field, update_nutriscore_values(off_value, fdc_value))
        elif isinstance(off_value, NutritionFacts):
            setattr(
                off_product, field, update_nutrition_facts_values(off_value, fdc_value)
            )
        elif isinstance(off_value, EcoscoreData) or isinstance(off_value, NovaData):
            pass  # no useful information for these scores is present in fdc
    return off_product


def update_ingredients_values(
    off_value: Ingredients, fdc_value: Ingredients
) -> Ingredients:
    if off_value.ingredients_text is None:
        off_value.ingredients_text = fdc_value.ingredients_text
    if not off_value.ingredients_list:
        off_value.ingredients_list = normalise_ingredients_list(
            off_value.ingredients_text
        )
    return off_value


def update_nutriscore_values(
    off_value: NutriscoreData, fdc_value: NutriscoreData
) -> NutriscoreData:
    for field, value in off_value.__dict__.items():
        if value is None and getattr(fdc_value, field, None) is not None:
            setattr(off_value, field, getattr(fdc_value, field, None))
    return off_value


def update_nutrition_facts_values(
    off_value: NutritionFacts, fdc_value: NutritionFacts
) -> NutritionFacts:
    for field, value in off_value.nutrient_level:
        if value is None:
            setattr(
                off_value.nutrient_level,
                field,
                getattr(fdc_value.nutrient_level, field, None),
            )

    for field, value in off_value.nutrients:
        if value is None:
            setattr(
                off_value.nutrients, field, getattr(fdc_value.nutrients, field, None)
            )

    return off_value


########################################################################################################################
# AJOUT DANS MONGO #####################################################################################################
########################################################################################################################


def load_products_to_mongo(
    products: list[Product],
    db_name: str = "openfoodfacts",
    collection_name: str = "products",
) -> None:
    logging.info("Loading products to MongoDB...")

    # Connect to MongoDB (default localhost:27017)
    client = MongoClient("mongodb://mongo:27017/")
    db = client[db_name]
    collection = db[collection_name]
    logging.info("Connected to client")

    # Check if the collection already contains data
    if collection.estimated_document_count() > 0:
        logging.info(
            f"MongoDB collection {collection_name} already contains data. Skipping import."
        )
        return

    # Insert products into MongoDB
    logging.info("Inserting data into MongoDB...")
    collection.insert_many([product.model_dump() for product in products])
    logging.info(f"Data loading complete into {db_name}.{collection_name}")


########################################################################################################################
# NETTOYAGE ############################################################################################################
########################################################################################################################


def cleanup_file(file_path: str, force_delete: bool = False) -> None:
    """Removes the file located in file_path if force_delete is True"""
    if force_delete:
        logging.info(f"Cleaning up the file {file_path}...")
        os.remove(file_path)
        logging.info(f"File {file_path} removed.")
    else:
        logging.info(f"Skipping cleanup for {file_path}. File retained.")


########################################################################################################################
# MAIN #################################################################################################################
########################################################################################################################


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )

    data_dir = "/app/data"
    os.makedirs(data_dir, exist_ok=True)  # Create the folder if it does not exist

    # Download and decompress
    off_csv_gz_file = os.path.join(data_dir, "off_csv.gz")
    off_csv_file = os.path.join(data_dir, "off_csv.csv")

    download_and_decompress_data(off_csv_url, off_csv_gz_file, ".gz", off_csv_file)
    # off_jsonl_gz_file = "off_jsonl.gz"
    # off_jsonl_file = "off_jsonl.jsonl"
    # download_and_decompress_data(off_jsonl_url, off_jsonl_gz_file, '.gz', off_jsonl_file)

    fdc_zip_file = os.path.join(data_dir, "fdc_branded.zip")
    fdc_file = os.path.join(data_dir, "fdc_branded.json")
    download_and_decompress_data(fdc_json_url, fdc_zip_file, ".zip", fdc_file)

    # Load data and transform it
    off_products = import_csv_off_data(off_csv_file, 10)
    fdc_products = import_json_fdc_data(fdc_file)
    off_products = complete_products_data(off_products, fdc_products)

    # Load transformed data into Mongo
    load_products_to_mongo(off_products)

    # Clean up
    cleanup_file(off_csv_file, force_delete=False)
    cleanup_file(fdc_file, force_delete=False)


if __name__ == "__main__":
    main()
    sys.exit(1)
