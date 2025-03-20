import csv
import logging
from decimal import Decimal

from pymongo import MongoClient

from domain.product.product import Product


class CsvCreator:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.mandatory_columns = [
            "Barcode",
            "Main language",
            "Product name",
            "Quantity",
            "Brands",
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
            "generic_name_en": "Common name",
            "product_name": "Product name",
            "category_en": "Categories",
            "is_raw": None,
            "brands": "Brands",
            "brand_owner": "Brand owner",
            "food_groups_en": None,
            "ingredients.ingredients_text": "Ingredients list",
            "ingredients.ingredients_list": None,
            "nutrition_facts.nutrient_level.fat": "Fat for 100 g / 100 ml",
            "nutrition_facts.nutrient_level.salt": "Salt for 100 g / 100 ml",
            "nutrition_facts.nutrient_level.saturated_fats": "Saturated fat for 100 g / 100 ml",
            "nutrition_facts.nutrient_level.sugar": "Sugars for 100 g / 100 ml",
            "nutrition_facts.nutrients.carbohydrates_100g": "Carbohydrates for 100 g / 100 ml",
            "nutrition_facts.nutrients.energy_100g": "Energy (kJ) for 100 g / 100 ml",
            "nutrition_facts.nutrients.energy_kcal_100g": "Energy (kcal) for 100 g / 100 ml",
            "nutrition_facts.nutrients.vitamin_a_100g": None,
            "nutriscore_data.energy": None,
            "nutriscore_data.fibers": "Fiber for 100 g / 100 ml",
            "nutriscore_data.proteins": "Proteins for 100 g / 100 ml",
            "nutriscore_data.saturated_fats": None,
            "nutriscore_data.sodium": "Sodium for 100 g / 100 ml",
            "nutriscore_data.sugar": None,
            "nutriscore_data.fruit_percentage": [
                "Fruits‚ vegetables‚ nuts and rapeseed‚ walnut and olive oils for 100 g / 100 ml",  # [
                "Fruits‚ vegetables and nuts - dried for 100 g / 100 ml",
            ],
            "nutriscore_data.is_beverage": None,
            "nutriscore_data.score": "Nutri-Score score",
            "ecoscore_data.score": None,
            "ecoscore_data.ingredients_origins.origins": "Origins of ingredients",
            "ecoscore_data.ingredients_origins.percent": None,
            "ecoscore_data.ingredients_origins.transportation_score": None,
            "ecoscore_data.packaging.non_recyclable_and_non_biodegradable_materials": None,
            "ecoscore_data.packaging.packaging": "Packaging",
            "ecoscore_data.packaging.production_system.labels": "Labels",
            "ecoscore_data.packaging.production_system.value": None,
            "ecoscore_data.packaging.production_system.warning": "Warning",
            "ecoscore_data.threatened_species": None,
            "nova_data.score": "NOVA group",
            "nova_data.group_markers": None,
        }

    def create_csv_file_for_products(
        self, products: list[Product], wanted_products_ids: list[str]
    ) -> None:
        with open(self.csv_path, "w", encoding="utf-8", newline="") as file:
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
                if product.id_match in wanted_products_ids:
                    list_to_write = self.__create_csv_line_for_product(product, columns)
                    filewriter.writerow(list_to_write)

                    empty_mandatory_columns = self.__check_fields_not_empty(
                        self.mandatory_columns, list_to_write
                    )
                    if empty_mandatory_columns:
                        logging.warning(
                            f"WARNING: empty mandatory columns:{empty_mandatory_columns}!"
                        )
                        logging.info(f"product: {product}")

    def __create_csv_line_for_product(
        self, product: Product, columns: list[str]
    ) -> list[str]:
        line = [""] * len(columns)

        for key, value in vars(product).items():
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
                    line[column_id] = (
                        str(value) if not isinstance(value, list) else value
                    )
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
        )
        return is_simple_field

    @staticmethod
    def __check_fields_not_empty(
        checked_columns: list[str], values_list: list[str]
    ) -> list[str]:
        empty_fields = []

        for i in range(len(checked_columns)):
            if values_list[i] == "":
                empty_fields.append(checked_columns[i])

        return empty_fields
