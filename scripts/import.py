import os
import sys
import logging
from domain.mapper.product_mapper import ProductMapper
from scripts.data_downloader import DataDownloader
from scripts.data_importer import DataImporter
from scripts.data_loader import DataLoader
from scripts.product_completer import ProductCompleter

off_csv_url = "https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.csv.gz"

off_jsonl_url = "https://static.openfoodfacts.org/data/openfoodfacts-products.jsonl.gz"

fdc_json_url = "https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_branded_food_json_2024-10-31.zip"


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )

    data_dir = "/app/data"
    os.makedirs(data_dir, exist_ok=True)

    data_downloader = DataDownloader()

    off_csv_gz_file = os.path.join(data_dir, "off_csv.gz")
    off_csv_file = os.path.join(data_dir, "off_csv.csv")

    data_downloader.download_and_decompress_data(off_csv_url, off_csv_gz_file, ".gz", off_csv_file)

    fdc_zip_file = os.path.join(data_dir, "fdc_branded.zip")
    fdc_file = os.path.join(data_dir, "fdc_branded.json")

    data_downloader.download_and_decompress_data(fdc_json_url, fdc_zip_file, ".zip", fdc_file)

    data_importer = DataImporter(ProductMapper())

    off_products = data_importer.import_csv_off_data(off_csv_file, 10)
    fdc_products = data_importer.import_json_fdc_data(fdc_file)

    product_completer = ProductCompleter()

    off_products = product_completer.complete_products_data(off_products, fdc_products)

    data_loader = DataLoader()

    data_loader.load_products_to_mongo(off_products)


if __name__ == "__main__":
    main()
    sys.exit(1)
