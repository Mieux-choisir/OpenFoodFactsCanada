import csv
import gzip
import ijson
import json
import os
import requests
import sys
import logging

from pymongo import MongoClient

from product import Product
from off_csv_mapper import *
from off_jsonl_mapper import *
from fdc_mapper import *

########################################################################################################################
##### VARIABLES GLOBALES ###############################################################################################
########################################################################################################################

# URL of the off csv file
off_csv_url = "https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.csv.gz"
off_csv_url = r"C:\Users\estre\Documents\stage\test2\pythonProject\scripts\en.openfoodfacts.org.products.csv"

# URL of the off json file
off_json_url = r"C:\Users\estre\Documents\stage\test2\pythonProject\scripts\filtered_canada_products.json"

# URL of the fdc file
fdc_json_url = r"C:\Users\estre\Documents\stage\bds\fdc\FoodData_Central_branded_food_json_2024-10-31\brandedDownload.json"


########################################################################################################################
##### TELECHARGEMENT DES FICHIERS ######################################################################################
########################################################################################################################

def download_file(url, download_path):
    """Downloads a file from a given url into a given download path"""
    logging.info(f"Downloading file from {url}...")
    response = requests.get(url, stream=True)
    with open(download_path, 'wb') as f:
        f.write(response.content)
    logging.info(f"Download complete: {download_path}")


def decompress_off_file(gz_file, output_file):
    """Decompresses a .gz file into a file named output_file"""
    logging.info(f"Decompressing {gz_file}...")
    with gzip.open(gz_file, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            f_out.write(f_in.read())
    logging.info(f"Decompression complete: {output_file}")  # TODO regarder pourquoi il crée un fichier vide


########################################################################################################################
##### IMPORTS ##########################################################################################################
########################################################################################################################

def import_json_fdc_data(filename: str) -> list[Product]:
    """Imports the data of branded food in a json file into a list of strings for each branded food"""
    products = []
    with open(filename, 'r', encoding='utf-8') as file:
        logging.info("Extracting Food Data Central products...")
        for obj in ijson.items(file, 'BrandedFoods.item'):
            if obj['marketCountry'] == 'United States':  # there are also products from New Zealand
                prod = map_fdc_dict_to_product(obj)
                products.append(prod)
    logging.info("FDC data imported")
    return products


def import_jsonl_off_data(filename: str, limit=None) -> list[Product]:
    """Imports the data of canadian food in a json file into a list of products"""
    if limit is not None:
        logging.info(f"Extracting {limit} products from Open Food Facts jsonl dataset...")
    else:
        logging.info("Extracting all products from Open Food Facts jsonl dataset...")

    products = []
    n = 0

    with open(filename, 'r', encoding='utf-8') as file:
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


def import_csv_off_data(filename: str, limit=None) -> list[Product]:
    """Imports the data of canadian food in a csv file into a list of products

     Args:
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
    csv.field_size_limit(2 ** 30)

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
##### COMPLETION #######################################################################################################
########################################################################################################################


def complete_products_data(off_products: list[Product], fdc_products: list[Product]) -> list[Product]:
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
                isinstance(off_value, list) and ((not off_value) or v == '' for v in off_value)):
            setattr(off_product, field, fdc_value)
        elif isinstance(off_value, Ingredients):
            setattr(off_product, field, update_ingredients_values(off_value, fdc_value))
        elif isinstance(off_value, NutriscoreData):
            setattr(off_product, field, update_nutriscore_values(off_value, fdc_value))
        elif isinstance(off_value, NutritionFacts):
            setattr(off_product, field, update_nutrition_facts_values(off_value, fdc_value))
        elif isinstance(off_value, EcoscoreData) or isinstance(off_value, NovaData):
            pass  # no useful information for these scores is present in fdc
    return off_product


def update_ingredients_values(off_value: Ingredients, fdc_value: Ingredients) -> Ingredients:
    if off_value.ingredients_text is None:
        off_value.ingredients_text = fdc_value.ingredients_text
    if not off_value.ingredients_list:
        off_value.ingredients_list = normalise_ingredients_list(off_value.ingredients_text)
    return off_value


def update_nutriscore_values(off_value: NutriscoreData, fdc_value: NutriscoreData) -> NutriscoreData:
    for field, value in off_value.__dict__.items():
        if value is None and getattr(fdc_value, field, None) is not None:
            setattr(off_value, field, getattr(fdc_value, field, None))
    return off_value


def update_nutrition_facts_values(off_value: NutritionFacts, fdc_value: NutritionFacts) -> NutritionFacts:
    for field, value in off_value.nutrient_level:
        if value is None:
            setattr(off_value.nutrient_level, field, getattr(fdc_value.nutrient_level, field, None))

    for field, value in off_value.nutrients:
        if value is None:
            setattr(off_value.nutrients, field, getattr(fdc_value.nutrients, field, None))

    return off_value


########################################################################################################################
##### AJOUT DANS MONGO #################################################################################################
########################################################################################################################

def load_products_to_mongo(products: list[Product], db_name="openfoodfacts", collection_name="products"):
    logging.info(f"Loading products to MongoDB...")

    # Connect to MongoDB (default localhost:27017)
    client = MongoClient("mongodb://localhost:27017/")
    db = client[db_name]
    collection = db[collection_name]
    logging.info("Connected to client")

    # Insert products into MongoDB
    collection.insert_many([product.model_dump() for product in products])
    logging.info(f"Data loading complete into {db_name}.{collection_name}")


########################################################################################################################
##### NETTOYAGE ########################################################################################################
########################################################################################################################

def cleanup_file(file_path):
    """Removes the file located in file_path"""
    logging.info(f"Cleaning up the file {file_path}...")
    os.remove(file_path)
    logging.info(f"File {file_path} removed.")


########################################################################################################################
##### MAIN #############################################################################################################
########################################################################################################################

def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )

    # Download and decompress
    # download_csv(csv_url, gz_file)
    # decompress_csv(gz_file, csv_file)

    # Load data and transform it
    off_products = import_jsonl_off_data(off_json_url, 10)
    fdc_products = import_json_fdc_data(fdc_json_url)
    off_products = complete_products_data(off_products, fdc_products)

    # Load transformed data into Mongo
    load_products_to_mongo(off_products)

    # Clean up
    # cleanup_file(gz_file)
    # cleanup_file(csv_file)


if __name__ == "__main__":
    main()
    sys.exit(1)
