import os
import sys
import logging
from datetime import datetime

from domain.mapper.ingredients_mapper import IngredientsMapper
from domain.mapper.number_mapper import NumberMapper
from domain.mapper.nutriscore_data_mapper import NutriscoreDataMapper
from domain.mapper.nutrition_facts_mapper import NutritionFactsMapper
from domain.mapper.product_mapper import ProductMapper
from domain.mapper.category_mapper import CategoryMapper
from domain.utils.category_creator import CategoryCreator
from domain.utils.ingredient_normalizer import IngredientNormalizer
from scripts.config import Config
from scripts.csv_creator import CsvCreator
from scripts.data_downloader import DataDownloader
from scripts.data_importer import DataImporter
from scripts.data_loader import DataLoader
from scripts.product_completer import ProductCompleter
from scripts.product_matcher import ProductMatcher

off_jsonl_url = "https://static.openfoodfacts.org/data/openfoodfacts-products.jsonl.gz"

# off_csv_url = (
#     "https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.csv.gz"
# )

fdc_json_url = "https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_branded_food_json_2025-04-24.zip"


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )

    config = Config()

    data_dir = "../data"
    os.makedirs(data_dir, exist_ok=True)

    data_downloader = DataDownloader()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)

    off_jsonl_gz_file = os.path.join(
        parent_dir, "data", config.off_compressed_jsonl_file_name
    )
    off_jsonl_file = os.path.join(parent_dir, "data", config.off_jsonl_file_name)

    data_downloader.download_and_decompress_data(
        off_jsonl_url, off_jsonl_gz_file, ".gz", off_jsonl_file
    )

    # off_csv_gz_file = os.path.join(
    #     parent_dir, "data", config.off_compressed_csv_file_name
    # )
    # off_csv_file = os.path.join(parent_dir, "data", config.off_csv_file_name)
    #
    # data_downloader.download_and_decompress_data(
    #     config.off_csv_url, off_csv_gz_file, ".gz", off_csv_file
    # )

    fdc_zip_file = os.path.join(
        parent_dir, "data", config.fdc_compressed_json_file_name
    )
    fdc_file = os.path.join(parent_dir, "data", config.fdc_json_file_name)

    data_downloader.download_and_decompress_data(
        config.fdc_json_url, fdc_zip_file, ".zip", fdc_file
    )

    categories_taxonomy_file = os.path.join(parent_dir, config.categories_taxonomy_file)
    category_mapping_file = os.path.join(parent_dir, config.category_mapping_file)

    data_importer = DataImporter(
        ProductMapper(
            IngredientsMapper(IngredientNormalizer()),
            NutriscoreDataMapper(NumberMapper()),
            NutritionFactsMapper(),
            CategoryMapper(
                CategoryCreator(), categories_taxonomy_file, category_mapping_file
            ),
        )
    )

    # off_products = data_importer.import_csv_off_data(off_csv_file)
    off_products = data_importer.import_jsonl_off_data(off_jsonl_file)
    fdc_products = data_importer.import_json_fdc_data(fdc_file)
    data_loader = DataLoader()

    data_loader.load_products_to_mongo(
        off_products, collection_name="off_products", use_docker=config.use_docker
    )
    data_loader.load_products_to_mongo(
        fdc_products, collection_name="fdc_products", use_docker=config.use_docker
    )

    product_matcher = ProductMatcher()

    fdc_products_from_db = data_loader.fetch_products_from_mongo(
        use_docker=config.use_docker
    )

    ids = product_matcher.match_products(use_docker=config.use_docker)
    csv_creator = CsvCreator(
        f"fdc_products_to_add_{datetime.now().strftime('%Y-%m-%d')}"
    )

    csv_creator.create_csv_files_for_products_not_existing_in_off(
        fdc_products_from_db, ids
    )

    product_completer = ProductCompleter()

    product_completer.complete_products()

    final_products_from_db = data_loader.fetch_products_from_mongo(
        collection_name="final_products", use_docker=config.use_docker
    )

    csv_creator_completed = CsvCreator(
        f"completed_off_products_to_add_{datetime.now().strftime('%Y-%m-%d')}"
    )

    csv_creator_completed.create_csv_files_for_products(final_products_from_db)


if __name__ == "__main__":
    main()
    sys.exit(1)
