import os
import sys
import logging

from domain.mapper.ingredients_mapper import IngredientsMapper
from domain.mapper.number_mapper import NumberMapper
from domain.mapper.nutriscore_data_mapper import NutriscoreDataMapper
from domain.mapper.nutrition_facts_mapper import NutritionFactsMapper
from domain.mapper.product_mapper import ProductMapper
from domain.mapper.category_mapper import CategoryMapper
from domain.utils.category_creator import CategoryCreator
from domain.utils.ingredient_normalizer import IngredientNormalizer
from scripts.data_downloader import DataDownloader
from scripts.data_importer import DataImporter
from scripts.data_loader import DataLoader

# off_jsonl_url = "https://static.openfoodfacts.org/data/openfoodfacts-products.jsonl.gz"

off_csv_url = (
    "https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.csv.gz"
)

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

    # off_jsonl_gz_file = "off_jsonl.gz"
    # off_jsonl_file = "off_jsonl.jsonl"

    # data_downloader.download_and_decompress_data(
    #     off_jsonl_url, off_jsonl_gz_file, ".gz", off_jsonl_file
    # )

    off_csv_gz_file = os.path.join(data_dir, "off_csv.gz")
    off_csv_file = os.path.join(data_dir, "off_csv.csv")

    data_downloader.download_and_decompress_data(
        off_csv_url, off_csv_gz_file, ".gz", off_csv_file
    )

    fdc_zip_file = os.path.join(data_dir, "fdc_branded.zip")
    fdc_file = os.path.join(data_dir, "fdc_branded.json")

    data_downloader.download_and_decompress_data(
        fdc_json_url, fdc_zip_file, ".zip", fdc_file
    )

    data_importer = DataImporter(
        ProductMapper(
            IngredientsMapper(IngredientNormalizer()),
            NutriscoreDataMapper(NumberMapper()),
            NutritionFactsMapper(),
            CategoryMapper(CategoryCreator()),
        )
    )

    off_products = data_importer.import_csv_off_data(off_csv_file, limit=100)
    # off_products = data_importer.import_jsonl_off_data(off_jsonl_file)
    fdc_products = data_importer.import_json_fdc_data(fdc_file)
    data_loader = DataLoader()

    data_loader.load_products_to_mongo(off_products, collection_name="off_products")
    data_loader.load_products_to_mongo(fdc_products, collection_name="fdc_products")


if __name__ == "__main__":
    main()
    sys.exit(1)
