import json
import logging

import ijson

from domain.mapper.product_mapper import ProductMapper
from scripts.data_loader import DataLoader
from scripts.config import Config


class DataImporter:
    """
    This is a class that imports data on products.

    Attributes:
        product_mapper (ProductMapper)

    Methods:
        import_json_fdc_data(filename): Imports the data of branded food in a json file into a list of strings for each branded food
        import_jsonl_off_data(filename, limit): Imports the data of canadian food in a json file into a list of products
    """

    def __init__(self, product_mapper: ProductMapper):
        self.product_mapper = product_mapper
        self.data_loader = DataLoader()
        self.config = Config()

    def import_json_fdc_data(self, filename: str, batch_size: int):
        """Imports the data of branded food in a json file into a list of strings for each branded food

        Args:
            filename: The path to the imported Food Data Central json file
            batch_size: The amount of rows treated by batch. Helps keeping RAM consumption in check.
        Returns:
            list[Product]: A list of Product objects extracted from the dataset.
        """
        products = []
        count = 0
        batch = batch_size

        with open(filename, "r", encoding="utf-8") as file:
            logging.info("Extracting Food Data Central products...")
            for obj in ijson.items(file, "BrandedFoods.item"):
                if obj.get("marketCountry") == "United States":
                    prod = self.product_mapper.map_fdc_dict_to_product(obj)
                    products.append(prod)
                    count += 1
                    if count % 10000 == 0:
                        logging.info(f"{count} products imported so far...")
                    if count >= batch:
                        self.data_loader.load_products_to_mongo(
                            products,
                            collection_name="fdc_products",
                            use_docker=self.config.use_docker,
                        )
                        batch = batch_size + batch
                        products = []
        logging.info(f"FDC data imported, total: {count}")
        self.data_loader.load_products_to_mongo(
            products, collection_name="fdc_products", use_docker=self.config.use_docker
        )

    def import_jsonl_off_data(self, filename: str, batch_size: int, limit: int = None):
        """Imports the data of canadian food in a json file into a list of products

        Args:
            filename: The path to the imported Open Food Facts jsonl file
            batch_size: The amount of rows treated by batch. Helps keeping RAM consumption in check.
            limit (int, optional): The number of objects to read from the dataset. Defaults to None.
        Returns:
            list[Product]: A list of Product objects extracted from the dataset.
        """
        if limit is not None:
            logging.info(
                f"Extracting {limit} products from Open Food Facts csv dataset..."
            )
        else:
            logging.info(
                "Extracting all products from Open Food Facts jsonl dataset..."
            )

        products = []
        count = 0
        batch = batch_size

        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                try:
                    obj = json.loads(line.strip())
                    prod = self.product_mapper.map_off_dict_to_product(obj)
                    if prod is not None:
                        products.append(prod)
                    count += 1
                    if count % 10000 == 0:
                        logging.info(f"{count} products imported so far...")
                    if limit is not None and count >= limit:
                        break
                    if count >= batch:
                        self.data_loader.load_products_to_mongo(
                            products,
                            collection_name="off_products",
                            use_docker=self.config.use_docker,
                        )
                        batch = batch_size + batch
                        products = []
                except json.JSONDecodeError as e:
                    logging.info(f"Error parsing line: {line}. Error: {e}")

        logging.info("OFF data imported")
        self.data_loader.load_products_to_mongo(
            products, collection_name="off_products", use_docker=self.config.use_docker
        )
