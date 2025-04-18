import csv
import logging
import os
from datetime import datetime
from decimal import Decimal
from typing import Iterator

from domain.product.product import Product


class CsvCreator:
    def __init__(self, csv_files_base_names):
        self.csv_files_base_names = csv_files_base_names
        self.mandatory_columns = [
            "Barcode",
            "Main language",
            "sources_fields:org-database-usda:fdc_id",
            "Product name",
            "sources_fields:org-database-usda:fdc_data_source",
            "sources_fields:org-database-usda:modified_date",
            "sources_fields:org-database-usda:available_date",
            "sources_fields:org-database-usda:publication_date",
            "Quantity",
            "Brands",
            "sources_fields:org-database-usda:fdc_category",
            "Categories",
            "Labels",
            "Origins of ingredients",
            "Ingredients list",
            "Allergens",
            "Traces",
            "Energy (kJ) for 100 g / 100 ml",
            "Energy (kcal) for 100 g / 100 ml",
            "Fat for 100 g / 100 ml",
            "Saturated fat for 100 g / 100 ml",
            "Carbohydrates for 100 g / 100 ml",
            "Sugars for 100 g / 100 ml",
            "Fiber for 100 g / 100 ml",
            "Proteins for 100 g / 100 ml",
            "Salt for 100 g / 100 ml",
            "Fruits‚ vegetables‚ nuts and rapeseed‚ walnut and olive oils for 100 g / 100 ml",
            "Fruits‚ vegetables and nuts - dried for 100 g / 100 ml",
            "Recycling instructions and/or packaging information",
            "Link to front product photo",
            "Link to ingredients list photo",
            "Link to nutrition facts table photo",
            "Link to recycling instructions and/or packaging information photo",
            "Type of the product photo",
        ]
        self.recommended_columns = [
            "Abbreviated product name",
            "Common name",
            "Serving size",
            "Packaging",
            "Countries",
            "Stores",
            "Product taken off the market",
            "Withdrawal date",
            "Traceability codes",
            "Recycling instructions - To recycle",
            "Recycling instructions - To discard",
        ]
        self.optional_columns = [
            "Producer product identifier",
            "Producer version identifier",
            "Net weight",
            "Drained weight",
            "Volume",
            "Brand owner",
            "Periods after opening",
            "Origin of the product and/or its ingredients",
            "Manufacturing or processing places",
            "Producer",
            "Sodium for 100 g / 100 ml",
            "Alcohol for 100 g / 100 ml",
            "Packaging 1 - Number of units",
            "Packaging 1 - Shape",
            "Packaging 1 - Material",
            "Packaging 1 - Recycling",
            "Packaging 1 - Weight of one empty unit",
            "Packaging 1 - Quantity of product contained per unit",
            "Packaging 2 - Number of units",
            "Packaging 2 - Shape",
            "Packaging 2 - Material",
            "Packaging 2 - Recycling",
            "Packaging 2 - Weight of one empty unit",
            "Packaging 2 - Quantity of product contained per unit",
            "Packaging 3 - Number of units",
            "Packaging 3 - Shape",
            "Packaging 3 - Material",
            "Packaging 3 - Recycling",
            "Packaging 3 - Weight of one empty unit",
            "Packaging 3 - Quantity of product contained per unit",
            "Packaging 4 - Number of units",
            "Packaging 4 - Shape",
            "Packaging 4 - Material",
            "Packaging 4 - Recycling",
            "Packaging 4 - Weight of one empty unit",
            "Packaging 4 - Quantity of product contained per unit",
            "Packaging 5 - Number of units",
            "Packaging 5 - Shape",
            "Packaging 5 - Material",
            "Packaging 5 - Recycling",
            "Packaging 5 - Weight of one empty unit",
            "Packaging 5 - Quantity of product contained per unit",
            "Conservation conditions",
            "Warning",
            "Preparation",
            "Nutri-Score score",
            "Nutri-Score",
            "NOVA group",
            "Recipe idea",
            "Customer service",
            "Link to the product page on the official site of the producer",
            "Link to other product photo",
        ]
        self.product_field_to_columns_mapping = {
            "id_match": "Barcode",
            "fdc_id": "sources_fields:org-database-usda:fdc_id",
            "product_name": "Product name",
            "data_source": "sources_fields:org-database-usda:fdc_data_source",
            "modified_date": "sources_fields:org-database-usda:modified_date",
            "available_date": "sources_fields:org-database-usda:available_date",
            "publication_date": "sources_fields:org-database-usda:publication_date",
            "quantity": "Quantity",
            "off_categories_en": "Categories",
            "is_raw": None,
            "brands": "Brands",
            "fdc_category_en": "sources_fields:org-database-usda:fdc_category",
            "brand_owner": "Brand owner",
            "food_groups_en": None,
            "ingredients.ingredients_text": "Ingredients list",
            "ingredients.ingredients_list": None,
            "household_serving_fulltext": "Serving size",
            "serving_size": "Serving size",
            "serving_size_unit": "Serving size",
            "nutrition_facts.nutrition_facts_per_serving.fat_serving": "Fat for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_serving.salt_serving": "Salt for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_serving.saturated_fats_serving": "Saturated fat for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_serving.sugar_serving": "Sugars for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_serving.carbohydrates_serving": "Carbohydrates for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_serving.energy_serving": "Energy (kJ) for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_serving.energy_kcal_serving": "Energy (kcal) for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_serving.proteins_serving": "Proteins for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_serving.fibers_serving": "Fiber for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_serving.sodium_serving": "Sodium for 100 g / 100 ml",
            "nutriscore_data.fruit_percentage": [
                "Fruits‚ vegetables‚ nuts and rapeseed‚ walnut and olive oils for 100 g / 100 ml",  # [
                "Fruits‚ vegetables and nuts - dried for 100 g / 100 ml",
            ],
            "nutriscore_data.score": "Nutri-Score score",
            "ecoscore_data.ingredients_origins.origins": "Origins of ingredients",
            "ecoscore_data.packaging.packaging": "Packaging",
            "ecoscore_data.packaging.production_system.labels": "Labels",  # TODO removed => add back ?
            "ecoscore_data.packaging.production_system.warning": "Warning",  # TODO removed => add back ?
            "nova_data.score": "NOVA group",
        }

    def create_csv_files_for_products_not_existing_in_off(
        self,
        products_iter: Iterator[Product],
        existing_off_products_ids: list[str],
        batch_size: int = 10000,
    ) -> None:
        logging.info("Creating csv files...")

        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)
        os.makedirs(os.path.join(parent_dir, "data"), exist_ok=True)

        test_set = set(existing_off_products_ids)
        columns = (
            self.mandatory_columns + self.recommended_columns + self.optional_columns
        )

        file_idx = 1
        written = 0
        csv_file = None
        writer = None

        for prod in products_iter:
            if prod.id_match in test_set:
                continue

            if written % batch_size == 0:
                if csv_file:
                    csv_file.close()

                path = os.path.join(
                    parent_dir, "data", f"{self.csv_files_base_names}_{file_idx}.csv"
                )
                logging.info(f"Opening new CSV: {path}")
                csv_file = open(path, "w", encoding="utf-8", newline="")
                writer = csv.writer(
                    csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
                )
                writer.writerow(columns)

                file_idx += 1

            row = self.__create_csv_line_for_product(prod, columns)
            writer.writerow(row)
            written += 1

        if csv_file:
            csv_file.close()

        logging.info(
            f"Finished: {written} products written into {file_idx - 1} file(s)."
        )

    def __create_csv_line_for_product(
        self, product: Product, columns: list[str]
    ) -> list[str]:
        line = [""] * len(columns)
        serving_size_index = columns.index("Serving size")

        household_serving_fulltext = getattr(
            product, "household_serving_fulltext", None
        )
        serving_size = getattr(product, "serving_size", None)
        serving_size_unit = getattr(product, "serving_size_unit", None)

        if serving_size is not None:
            if household_serving_fulltext is not None and str(serving_size) in str(
                household_serving_fulltext
            ):
                final_serving_size_str = (
                    f"{serving_size} {serving_size_unit or ''}".strip()
                )
            else:
                final_serving_size_str = f"{household_serving_fulltext or ''} ({serving_size} {serving_size_unit or ''})".strip()
        else:
            final_serving_size_str = household_serving_fulltext or ""

        line[serving_size_index] = final_serving_size_str

        for key, value in vars(product).items():
            if key in [
                "household_serving_fulltext",
                "serving_size",
                "serving_size_unit",
            ]:
                continue
            self.__add_values(columns, line, key, value, "")

        line[columns.index("Main language")] = "English"

        return line

    def __add_values(self, columns, line, key, value, old_key_name):
        current_key_name = old_key_name + "." + key if old_key_name != "" else key

        if self.__is_simple_field(value):
            column_mapping = self.product_field_to_columns_mapping.get(current_key_name)
            if column_mapping is not None:
                if isinstance(column_mapping, str):
                    column_id = columns.index(column_mapping)
                    value = self.__format_value(value)
                    line[column_id] = value
                elif isinstance(column_mapping, list):
                    column_ids = [columns.index(cat) for cat in column_mapping]
                    for column_id in column_ids:
                        line[column_id] = (
                            str(value) if not isinstance(value, list) else value
                        )

        elif value is not None:
            value_dict = vars(value) if not isinstance(value, dict) else value
            for new_key, new_value in value_dict.items():
                self.__add_values(columns, line, new_key, new_value, current_key_name)

    @staticmethod
    def __is_simple_field(value) -> bool:
        is_simple_field = (
            isinstance(value, str)
            or isinstance(value, int)
            or isinstance(value, float)
            or isinstance(value, Decimal)
            or isinstance(value, list)
            or isinstance(value, datetime)
        )
        return is_simple_field

    @staticmethod
    def __format_value(value):
        formatted_value = ""
        if isinstance(value, list):
            if len(value) > 0:
                for element in value[:-1]:
                    formatted_value += str(element) + ", "
                formatted_value += str(value[-1])

        else:
            formatted_value = str(value) if not isinstance(value, list) else value
        return formatted_value
