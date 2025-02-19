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
from mapper.off_csv_mapper import *
from mapper.off_jsonl_mapper import *
from mapper.fdc_mapper import *

########################################################################################################################
##### VARIABLES GLOBALES ###############################################################################################
########################################################################################################################

# URL of the off csv file
off_csv_url = "https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.csv.gz"

# URL of the off json file
off_jsonl_url = "https://static.openfoodfacts.org/data/openfoodfacts-products.jsonl.gz"

# URL of the fdc file
fdc_json_url = "https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_branded_food_json_2024-10-31.zip"


########################################################################################################################
##### TELECHARGEMENT DES FICHIERS ######################################################################################
########################################################################################################################

def download_and_decompress_data(source_url, compressed_file, compressed_file_extension, decompressed_file):
    download_file(source_url, compressed_file)
    decompress_file(compressed_file, compressed_file_extension, decompressed_file)
    cleanup_file(compressed_file)


def download_file(url, download_path, chunk_size=1024*1024, max_retries=5, timeout=60):
    """Downloads a file from a given url into a given download path"""
    logging.info(f"Downloading file from {url}...")

    @retry(stop=stop_after_attempt(max_retries), wait=wait_fixed(5))
    def download():
        try:
            with requests.get(url, stream=True, timeout=timeout) as response:
                response.raise_for_status()
                with open(download_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        f.write(chunk)
            logging.info(f"Download complete: {download_path}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error downloading file {e}")
            raise

    try:
        download()
    except Exception as e:
        logging.error(f"Download failed after {max_retries} attemps: {e}")
        raise


def decompress_file(compressed_file, compressed_file_extension, output_file, buffer_size=1024*1024):
    logging.info(f"Decompressing {compressed_file} into {output_file}...")

    if compressed_file_extension == '.gz':
        decompress_gz_file(compressed_file, output_file, buffer_size)
    elif compressed_file_extension == '.zip':
        decompress_zip_file(compressed_file, output_file, buffer_size)
    else:
        logging.error(f"Unsupported file extension: {compressed_file_extension}")
        raise ValueError(f"Unsupported file extension: {compressed_file_extension}. Supported extensions are '.gz' and '.zip'.")
    logging.info(f"Decompression complete")


def decompress_gz_file(gz_file, output_file, buffer_size=1024*1024):
    """Decompresses a .gz file into a file named output_file"""
    with gzip.open(gz_file, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            while chunk := f_in.read(buffer_size):
                f_out.write(chunk)


def decompress_zip_file(zip_file, output_file, buffer_size=1024*1024):
    """Decompresses a .zip file into a file named output_file"""
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        with zip_ref.open(zip_ref.namelist()[0], 'r') as f_in:
            with open(output_file, 'wb') as f_out:
                while chunk := f_in.read(buffer_size):
                    f_out.write(chunk)



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

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                obj = json.loads(line.strip())
                prod = map_off_dict_to_product(obj)
                if prod is not None:
                    products.append(prod)
                if limit is not None and len(products) >= limit:
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
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)

        for i, row in enumerate(reader):
            if i in range(0, 5):
                print ("Produit", i)
                for h, r in zip(header, row):
                    print(f"{h}: {r}")
            product = map_off_row_to_product(row, header)

            if product is None:
                continue

            products.append(product)

            if limit is not None and len(products) >= limit:
                break

    logging.info("OFF data imported")
    return products

########################################################################################################################
##### AJOUT DANS MONGO #################################################################################################
########################################################################################################################

def load_products_to_mongo(products: list[Product], collection_name: str):
    logging.info(f"Loading products to MongoDB...")
    db_name = "openfoodfacts"

    # Connect to MongoDB (default localhost:27017)
    client = MongoClient("mongodb://localhost:37017/")
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
    off_csv_gz_file = "off_csv.gz"
    off_csv_file = "off_csv.csv"
    download_and_decompress_data(off_csv_url, off_csv_gz_file, '.gz', off_csv_file)

    fdc_zip_file = "fdc_branded.zip"
    fdc_file = "fdc_branded.json"
    download_and_decompress_data(fdc_json_url, fdc_zip_file, '.zip', fdc_file)

    # Load data and transform it
    #off_products = import_jsonl_off_data(off_json_url)
    off_products = import_csv_off_data(off_csv_file)
    fdc_products = import_json_fdc_data(fdc_file)

    # Load transformed data into Mongo
    load_products_to_mongo(off_products, "off_products")
    load_products_to_mongo(fdc_products, "fdc_products")

    # Clean up
    cleanup_file(off_csv_file)
    #cleanup_file(off_jsonl_file)
    cleanup_file(fdc_file)


if __name__ == "__main__":
    main()
    sys.exit(1)
