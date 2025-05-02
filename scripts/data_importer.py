import csv
import json
import logging

import ijson

from domain.mapper.product_mapper import ProductMapper
from domain.product.product import Product


class DataImporter:
    """
    This is a class that imports data on products.

    Attributes:
        product_mapper (ProductMapper)

    Methods:
        import_json_fdc_data(filename): Imports the data of branded food in a json file into a list of strings for each branded food
        import_jsonl_off_data(filename, limit): Imports the data of canadian food in a json file into a list of products
        import_csv_off_data(filename, limit): Imports the data of canadian food in a csv file into a list of products
    """

    def __init__(self, product_mapper: ProductMapper):
        self.product_mapper = product_mapper

    def import_json_fdc_data(self, filename: str) -> list[Product]:
        """Imports the data of branded food in a json file into a list of strings for each branded food

        Args:
            filename: The path to the imported Food Data Central json file
        Returns:
            list[Product]: A list of Product objects extracted from the dataset.
        """
        products = []
        count = 0
        with open(filename, "r", encoding="utf-8") as file:
            logging.info("Extracting Food Data Central products...")
            for obj in ijson.items(file, "BrandedFoods.item"):
                if obj.get("marketCountry") == "United States":
                    prod = self.product_mapper.map_fdc_dict_to_product(obj)
                    products.append(prod)
                    count += 1
                    if count % 10000 == 0:
                        logging.info(f"{count} products imported so far...")
        logging.info(f"FDC data imported, total: {count}")
        return products

    def import_jsonl_off_data(self, filename: str, limit: int = None) -> list[Product]:
        """Imports the data of canadian food in a json file into a list of products

        Args:
            filename: The path to the imported Open Food Facts jsonl file
            limit (int, optional): The number of objects to read from the dataset. Defaults to None.
        Returns:
            list[Product]: A list of Product objects extracted from the dataset.
        """
        if limit is not None:
            logging.info(
                f"Extracting {limit} products from Open Food Facts jsonl dataset..."
            )
        else:
            logging.info(
                "Extracting all products from Open Food Facts jsonl dataset..."
            )

        products = []
        count = 0

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
                except json.JSONDecodeError as e:
                    logging.info(f"Error parsing line: {line}. Error: {e}")

        logging.info("OFF data imported")
        return products

    def import_csv_off_data(self, filename: str, limit: int = None) -> list[Product]:
        """Imports the data of canadian food in a csv file into a list of products

         Args:
            filename: The path to the imported Open Food Facts csv file
            limit (int, optional): The number of lines to read from the dataset. Defaults to None.
        Returns:
            list[Product]: A list of Product objects extracted from the dataset.
        """
        if limit is not None:
            logging.info(
                f"Extracting {limit} products from Open Food Facts csv dataset..."
            )
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
                product = self.product_mapper.map_off_row_to_product(row, header)

                if product is None:
                    continue

                products.append(product)
                n += 1

                if limit is not None and n >= limit:
                    break

        logging.info("OFF data imported")
        return products
