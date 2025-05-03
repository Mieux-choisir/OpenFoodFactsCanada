import csv
import logging
import os
from datetime import datetime
from decimal import Decimal

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
            "Trans fats for 100 g / 100 ml",
            "Cholesterol for 100 g / 100 ml",
            "Calcium for 100 g / 100 ml",
            "Iron for 100 g / 100 ml",
            "Potassium for 100 g / 100 ml",
            "Monounsaturated fats for 100 g / 100 ml",
            "Polyunsaturated fats for 100 g / 100 ml",
            "Vitamin a for 100 g / 100 ml",
            "Vitamin b1 for 100 g / 100 ml",
            "Vitamin b2 for 100 g / 100 ml",
            "Vitamin b6 for 100 g / 100 ml",
            "Vitamin b9 for 100 g / 100 ml",
            "Vitamin b12 for 100 g / 100 ml",
            "Vitamin c for 100 g / 100 ml",
            "Vitamin pp for 100 g / 100 ml",
            "Phosphorus for 100 g / 100 ml",
            "Magnesium for 100 g / 100 ml",
            "Zinc for 100 g / 100 ml",
            "Folates for 100 g / 100 ml",
            "Pantothenic acid for 100 g / 100 ml",
            "Soluble fiber for 100 g / 100 ml",
            "Insoluble fiber for 100 g / 100 ml",
            "Copper for 100 g / 100 ml",
            "Manganese for 100 g / 100 ml",
            "Polyols for 100 g / 100 ml",
            "Selenium for 100 g / 100 ml",
            "Phylloguinone for 100 g / 100 ml",
            "Iodine for 100 g / 100 ml",
            "Biotin for 100 g / 100 ml",
            "Caffeine for 100 g / 100 ml",
            "Molybdenum for 100 g / 100 ml",
            "Chromium for 100 g / 100 ml",
            "Alcohol for 100 g / 100 ml",
            "Energy (kJ) per serving",
            "Energy (kcal) per serving",
            "Fat per serving",
            "Saturated fat per serving",
            "Carbohydrates per serving",
            "Sugars per serving",
            "Fiber per serving",
            "Proteins per serving",
            "Salt per serving",
            "Sodium per serving",
            "Trans fats per serving",
            "Cholesterol per serving",
            "Calcium per serving",
            "Iron per serving",
            "Potassium per serving",
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
            "id_original": "Barcode",
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
            "nutrition_facts.nutrition_facts_per_hundred_grams.fat_100g": "Fat for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_hundred_grams.salt_100g": "Salt for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_hundred_grams.saturated_fats_100g": "Saturated fat for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_hundred_grams.sugar_100g": "Sugars for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_hundred_grams.carbohydrates_100g": "Carbohydrates for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_hundred_grams.energy_100g": None,
            "nutrition_facts.nutrition_facts_per_hundred_grams.energy_kcal_100g": "Energy (kcal) for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_hundred_grams.proteins_100g": "Proteins for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_hundred_grams.fibers_100g": "Fiber for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_hundred_grams.sodium_100g": "Sodium for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_hundred_grams.trans_fats_100g": "Trans fats for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_hundred_grams.cholesterol_100g": "Cholesterol for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_hundred_grams.calcium_100g": "Calcium for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_hundred_grams.iron_100g": "Iron for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_hundred_grams.potassium_100g": "Potassium for 100 g / 100 ml",
            "nutriscore_data.fruit_percentage": [
                "Fruits‚ vegetables‚ nuts and rapeseed‚ walnut and olive oils for 100 g / 100 ml",  # [
                "Fruits‚ vegetables and nuts - dried for 100 g / 100 ml",
            ],
            "nutrition_facts.nutrition_facts_per_hundred_grams.monounsaturated_fats_100g": "Monounsaturated fats for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_hundred_grams.polyunsaturated_fats_100g": "Polyunsaturated fats for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_hundred_grams.vitamin_a_100g": "Vitamin a for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_hundred_grams.vitamin_b1_100g": "Vitamin b1 for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_hundred_grams.vitamin_b2_100g": "Vitamin b2 for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_hundred_grams.vitamin_b6_100g": "Vitamin b6 for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_hundred_grams.vitamin_b9_100g": "Vitamin b9 for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_hundred_grams.vitamin_b12_100g": "Vitamin b12 for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_hundred_grams.vitamin_c_100g": "Vitamin c for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_hundred_grams.vitamin_pp_100g": "Vitamin pp for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_hundred_grams.phosphorus_100g": "Phosphorus for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_hundred_grams.magnesium_100g": "Magnesium for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_hundred_grams.zinc_100g": "Zinc for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_hundred_grams.folates_100g": "Folates for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_hundred_grams.pantothenic_acid_100g": "Pantothenic acid for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_hundred_grams.soluble_fiber_100g": "Soluble fiber for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_hundred_grams.insoluble_fiber_100g": "Insoluble fiber for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_hundred_grams.copper_100g": "Copper for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_hundred_grams.manganese_100g": "Manganese for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_hundred_grams.polyols_100g": "Polyols for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_hundred_grams.selenium_100g": "Selenium for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_hundred_grams.phylloguinone_100g": "Phylloguinone for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_hundred_grams.iodine_100g": "Iodine for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_hundred_grams.biotin_100g": "Biotin for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_hundred_grams.caffeine_100g": "Caffeine for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_hundred_grams.molybdenum_100g": "Molybdenum for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_hundred_grams.chromium_100g": "Chromium for 100 g / 100 ml",
            "nutrition_facts.nutrition_facts_per_serving.fat_serving": "Fat per serving",
            "nutrition_facts.nutrition_facts_per_serving.salt_serving": "Salt per serving",
            "nutrition_facts.nutrition_facts_per_serving.saturated_fats_serving": "Saturated fat per serving",
            "nutrition_facts.nutrition_facts_per_serving.sugar_serving": "Sugars per serving",
            "nutrition_facts.nutrition_facts_per_serving.carbohydrates_serving": "Carbohydrates per serving",
            "nutrition_facts.nutrition_facts_per_serving.energy_serving": None,
            "nutrition_facts.nutrition_facts_per_serving.energy_kcal_serving": "Energy (kcal) per serving",
            "nutrition_facts.nutrition_facts_per_serving.proteins_serving": "Proteins per serving",
            "nutrition_facts.nutrition_facts_per_serving.fibers_serving": "Fiber per serving",
            "nutrition_facts.nutrition_facts_per_serving.sodium_serving": "Sodium per serving",
            "nutrition_facts.nutrition_facts_per_serving.trans_fats_serving": "Trans fats per serving",
            "nutrition_facts.nutrition_facts_per_serving.cholesterol_serving": "Cholesterol per serving",
            "nutrition_facts.nutrition_facts_per_serving.calcium_serving": "Calcium per serving",
            "nutrition_facts.nutrition_facts_per_serving.iron_serving": "Iron per serving",
            "nutrition_facts.nutrition_facts_per_serving.potassium_serving": "Potassium per serving",
            "nutriscore_data.score": "Nutri-Score score",
            "ecoscore_data.ingredients_origins.origins": "Origins of ingredients",
            "ecoscore_data.packaging.packaging": "Packaging",
            "ecoscore_data.packaging.production_system.labels": "Labels",  # TODO removed => add back ?
            "ecoscore_data.packaging.production_system.warning": "Warning",  # TODO removed => add back ?
            "nova_data.score": "NOVA group",
        }

    def create_csv_files_for_products_not_existing_in_off(
        self, products: list[Product], existing_off_products_ids: list[str]
    ) -> None:
        logging.info("Creating csv files...")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)

        logging.info(f"Number of products in FDC : {len(products)}")
        logging.info(
            f"Number of products that matches : {len(existing_off_products_ids)}"
        )

        test_set = set(existing_off_products_ids)
        filtered_products = [
            product for product in products if product.id_match not in test_set
        ]
        logging.info(
            f"Number of products to create csv files for: {len(filtered_products)}"
        )
        batches = self.__create_batches(filtered_products, batch_size=10000)

        for i in range(len(batches)):
            csv_file = os.path.join(
                parent_dir, "data", self.csv_files_base_names + f"_{i + 1}.csv"
            )
            logging.info(f"Creating csv file: {csv_file}")
            self.__create_csv_file_for_products_not_existing_in_off(
                csv_file, batches[i], existing_off_products_ids
            )
            logging.info("Csv file created!")

        logging.info("Finished creating csv files.")

    def create_csv_files_for_products(self, products: list[Product]):
        logging.info("Creating csv files...")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)

        logging.info(f"Number of products to create csv files for: {len(products)}")
        batches = self.__create_batches(products, batch_size=10000)

        for i in range(len(batches)):
            csv_file = os.path.join(
                parent_dir, "data", self.csv_files_base_names + f"_{i + 1}.csv"
            )
            logging.info(f"Creating csv file: {csv_file}")
            self.__create_csv_file_for_products(csv_file, batches[i])
            logging.info("Csv file created!")

        logging.info("Finished creating csv files.")

    @staticmethod
    def __create_batches(
        products: list[Product], batch_size=10000
    ) -> list[list[Product]]:
        return [
            products[i : i + batch_size] for i in range(0, len(products), batch_size)
        ]

    def __create_csv_file_for_products_not_existing_in_off(
        self,
        csv_file: str,
        products: list[Product],
        existing_off_products_ids: list[str],
        warn_mandatory_columns: bool = False,
    ) -> None:
        with open(csv_file, "w", encoding="utf-8", newline="") as file:
            filewriter = csv.writer(
                file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )

            columns = (
                self.mandatory_columns
                + self.recommended_columns
                + self.optional_columns
            )

            filewriter.writerow(columns)

            for product in products:
                if product.id_match not in existing_off_products_ids:
                    list_to_write = self.__create_csv_line_for_product(product, columns)
                    filewriter.writerow(list_to_write)

                    empty_mandatory_columns = self.__check_fields_not_empty(
                        self.mandatory_columns, list_to_write
                    )
                    if warn_mandatory_columns and empty_mandatory_columns:
                        logging.warning(
                            f"WARNING: empty mandatory columns for product with code {product.id_match}:{empty_mandatory_columns}!"
                        )

    def __create_csv_file_for_products(
        self,
        csv_file: str,
        products: list[Product],
        warn_mandatory_columns: bool = False,
    ) -> None:
        with open(csv_file, "w", encoding="utf-8", newline="") as file:
            filewriter = csv.writer(
                file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )

            columns = (
                self.mandatory_columns
                + self.recommended_columns
                + self.optional_columns
            )

            filewriter.writerow(columns)

            for product in products:
                list_to_write = self.__create_csv_line_for_product(product, columns)
                filewriter.writerow(list_to_write)

                empty_mandatory_columns = self.__check_fields_not_empty(
                    self.mandatory_columns, list_to_write
                )
                if warn_mandatory_columns and empty_mandatory_columns:
                    logging.warning(
                        f"WARNING: empty mandatory columns for product with code {product.id_match}:{empty_mandatory_columns}!"
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

        final_serving_size_str = self.__format_serving_size(
            household_serving_fulltext, serving_size, serving_size_unit
        )
        line[serving_size_index] = final_serving_size_str

        line[serving_size_index] = final_serving_size_str

        for key, value in vars(product).items():
            if key in [
                "household_serving_fulltext",
                "serving_size",
                "serving_size_unit",
            ]:
                continue
            self.__add_values(
                columns,
                line,
                key,
                value,
                "",
                getattr(product, "nutrition_data_per", None),
            )

        line[columns.index("Main language")] = "English"
        line[columns.index("Countries")] = "United States"

        return line

    def __add_values(self, columns, line, key, value, old_key_name, nutrition_data_per):
        current_key_name = old_key_name + "." + key if old_key_name != "" else key

        if (
            (nutrition_data_per is None and "_100g" in current_key_name)
            or (nutrition_data_per == "100g" and "_serving" in current_key_name)
            or (nutrition_data_per == "serving" and "_100g" in current_key_name)
        ):
            return

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
                self.__add_values(
                    columns,
                    line,
                    new_key,
                    new_value,
                    current_key_name,
                    nutrition_data_per,
                )

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

    @staticmethod
    def __check_fields_not_empty(
        checked_columns: list[str], values_list: list[str]
    ) -> list[str]:
        empty_fields = []

        for i in range(len(checked_columns)):
            if values_list[i] == "":
                empty_fields.append(checked_columns[i])

        return empty_fields

    @staticmethod
    def __format_serving_size(household_text, size, unit):
        if isinstance(household_text, str) and household_text.strip().lower() == "none":
            household_text = ""

        if size is None:
            return household_text or ""

        formatted_size = CsvCreator.__format_decimal(size)

        if not formatted_size:
            return household_text or ""

        unit = (unit or "").strip()
        full_match = f"{formatted_size} {unit}".lower()

        if household_text and full_match in household_text.lower():
            return household_text.strip()

        if household_text:
            return f"{household_text.strip()} ({formatted_size} {unit})".strip()
        else:
            return f"{formatted_size} {unit}".strip()

    @staticmethod
    def __format_decimal(value: float | str | None, max_decimals: int = 5) -> str:
        try:
            number = float(value)
            rounded = round(number, max_decimals)

            return f"{rounded:.{max_decimals}f}".rstrip("0").rstrip(".")
        except (ValueError, TypeError):
            return ""
