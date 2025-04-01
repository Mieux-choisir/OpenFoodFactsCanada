from decimal import Decimal

from domain.mapper.nutrient_amount_mapper import NutrientAmountMapper
from domain.product.complexFields.nutrient_facts import NutritionFacts
from domain.utils.converter import Converter


class NutritionFactsMapper:

    def __init__(self):
        self.energy_kcal_to_kj = Decimal(4.1868)
        self.sodium_to_salt = Decimal(2.5)

    def map_fdc_dict_to_nutrition_facts(
        self, food_nutrients: list[dict]
    ) -> NutritionFacts:
        """Maps the given food nutrients of a FDC product to a NutritionFacts object"""
        nutrient_ids = {
            "fat_100g": 1004,
            "sodium_100g": 1093,
            "saturated_fats_100g": 1258,
            "sugar_100g": 2000,
            "carbohydrates_100g": 1005,
            "energy_kcal_100g": 1008,
            "vitamin_a_100g": 1104,
            "proteins_100g": 1003,
            "fiber_100g": 1079,
            "monounsaturated_fat_100g": 1292,
            "polyunsaturated_fat_100g": 1293,
            "trans_fat_100g": 1257,
            "cholesterol_100g": 1253,
            "calcium_100g": 1087,
            "iron_100g": 1089,
            "potassium_100g": 1092,
            "vitamin_b1_100g": 1165,
            "vitamin_b2_100g": 1166,
            "vitamin_b6_100g": 1175,
            "vitamin_b9_100g": 1186,
            "vitamin_b12_100g": 1178,
            "vitamin_c_100g": 1162,
            "vitamin_pp_100g": 1167,
            "phosphorus_100g": 1091,
            "magnesium_100g": 1090,
            "zinc_100g": 1095,
            "folates_100g": 1177,
            "pantothenic_acid_100g": 1170,
            "soluble_fiber_100g": 1082,
            "insoluble_fiber_100g": 1084,
            "copper_100g": 1098,
            "manganese_100g": 1101,
            "polyols_100g": 1086,
            "selenium_100g": 1103,
            "phylloguinone_100g": 1185,
            "iodine_100g": 1100,
            "biotin_100g": 1176,
            "caffeine_100g": 1057,
            "molybdenum_100g": 1102,
            "chromium_100g": 1096,
        }

        nutrition_facts_data = {}
        for field, nutrient_id in nutrient_ids.items():
            value = self.__get_nutrient_level(food_nutrients, nutrient_id)
            unit = self.__get_nutrient_unit(food_nutrients, nutrient_id)

            if field == "sodium_100g" and value is not None:
                nutrition_facts_data["salt_100g"] = NutrientAmountMapper().map_nutrient(
                    value * self.sodium_to_salt, unit
                )
            if field == "energy_kcal_100g" and value is not None:
                nutrition_facts_data["energy_100g"] = value * self.energy_kcal_to_kj

            nutrition_facts_data[field] = NutrientAmountMapper().map_nutrient(
                value, unit
            )

        return NutritionFacts(**nutrition_facts_data)

    @staticmethod
    def map_off_row_to_nutrition_facts(
        row: list[str], header: list[str]
    ) -> NutritionFacts:
        """Maps the values in a given OFF (csv) product to a NutritionFacts object"""
        field_mapping = {
            "saturated-fat_100g": "saturated_fats_100g",
            "sugars_100g": "sugar_100g",
            "trans-fat_100g": "trans_fats_100g",
            "fiber_100g": "fibers_100g",
            "monounsaturated-fat_100g": "monounsaturated_fats_100g",
            "polyunsaturated-fat_100g": "polyunsaturated_fats_100g",
            "energy-kcal_100g": "energy_kcal_100g",
            "vitamin-a_100g": "vitamin_a_100g",
            "vitamin-b1_100g": "vitamin_b1_100g",
            "vitamin-b2_100g": "vitamin_b2_100g",
            "vitamin-b6_100g": "vitamin_b6_100g",
            "vitamin-b9_100g": "vitamin_b9_100g",
            "vitamin-b12_100g": "vitamin_b12_100g",
            "vitamin-c_100g": "vitamin_c_100g",
            "vitamin-pp_100g": "vitamin_pp_100g",
            "pantothenic-acid_100g": "pantothenic_acid_100g",
            "soluble-fiber_100g": "soluble_fiber_100g",
            "insoluble-fiber_100g": "insoluble_fiber_100g",
        }

        fields = [
            "fat_100g",
            "salt_100g",
            "saturated-fat_100g",
            "sugars_100g",
            "carbohydrates_100g",
            "energy_100g",
            "energy-kcal_100g",
            "vitamin-a_100g",
            "proteins_100g",
            "fiber_100g",
            "sodium_100g",
            "monounsaturated-fat_100g",
            "polyunsaturated-fat_100g",
            "trans-fat_100g",
            "cholesterol_100g",
            "calcium_100g",
            "iron_100g",
            "potassium_100g",
            "vitamin-b1_100g",
            "vitamin-b2_100g",
            "vitamin-b6_100g",
            "vitamin-b9_100g",
            "vitamin-b12_100g",
            "vitamin-c_100g",
            "vitamin-pp_100g",
            "phosphorus_100g",
            "magnesium_100g",
            "zinc_100g",
            "folates_100g",
            "pantothenic-acid_100g",
            "soluble-fiber_100g",
            "insoluble-fiber_100g",
            "copper_100g",
            "manganese_100g",
            "polyols_100g",
            "selenium_100g",
            "phylloguinone_100g",
            "iodine_100g",
            "biotin_100g",
            "caffeine_100g",
            "molybdenum_100g",
            "chromium_100g",
        ]

        nutrition_facts_data = {
            field_mapping.get(field, field): (
                Converter.safe_float(row[header.index(field)])
                if field in header
                else None
            )
            for field in fields
        }

        return NutritionFacts(**nutrition_facts_data)

    @staticmethod
    def map_off_dict_to_nutrition_facts(product_dict: dict) -> NutritionFacts:
        """Maps the values in a given OFF (jsonl) product to a NutritionFacts object"""
        nutriments = product_dict.get("nutriments", {})

        field_mapping = {
            "saturated-fat_100g": "saturated_fats_100g",
            "sugars_100g": "sugar_100g",
            "trans-fat_100g": "trans_fats_100g",
            "fiber_100g": "fibers_100g",
            "monounsaturated-fat_100g": "monounsaturated_fats_100g",
            "polyunsaturated-fat_100g": "polyunsaturated_fats_100g",
            "energy-kcal_100g": "energy_kcal_100g",
            "vitamin-a_100g": "vitamin_a_100g",
            "vitamin-b1_100g": "vitamin_b1_100g",
            "vitamin-b2_100g": "vitamin_b2_100g",
            "vitamin-b6_100g": "vitamin_b6_100g",
            "vitamin-b9_100g": "vitamin_b9_100g",
            "vitamin-b12_100g": "vitamin_b12_100g",
            "vitamin-c_100g": "vitamin_c_100g",
            "vitamin-pp_100g": "vitamin_pp_100g",
            "pantothenic-acid_100g": "pantothenic_acid_100g",
            "soluble-fiber_100g": "soluble_fiber_100g",
            "insoluble-fiber_100g": "insoluble_fiber_100g",
        }

        fields = [
            "fat_100g",
            "salt_100g",
            "saturated-fat_100g",
            "sugars_100g",
            "carbohydrates_100g",
            "energy_100g",
            "energy-kcal_100g",
            "vitamin-a_100g",
            "proteins_100g",
            "fiber_100g",
            "sodium_100g",
            "monounsaturated-fat_100g",
            "polyunsaturated-fat_100g",
            "trans-fat_100g",
            "cholesterol_100g",
            "calcium_100g",
            "iron_100g",
            "potassium_100g",
            "vitamin-b1_100g",
            "vitamin-b2_100g",
            "vitamin-b6_100g",
            "vitamin-b9_100g",
            "vitamin-b12_100g",
            "vitamin-c_100g",
            "vitamin-pp_100g",
            "phosphorus_100g",
            "magnesium_100g",
            "zinc_100g",
            "folates_100g",
            "pantothenic-acid_100g",
            "soluble-fiber_100g",
            "insoluble-fiber_100g",
            "copper_100g",
            "manganese_100g",
            "polyols_100g",
            "selenium_100g",
            "phylloguinone_100g",
            "iodine_100g",
            "biotin_100g",
            "caffeine_100g",
            "molybdenum_100g",
            "chromium_100g",
        ]

        nutrition_facts_data = {
            field_mapping.get(field, field): (
                float(nutriments[field]) if field in nutriments else None
            )
            for field in fields
        }

        return NutritionFacts(**nutrition_facts_data)

    @staticmethod
    def __get_nutrient_level(food_nutrients, searched_id):
        """Returns the nutrient level of a nutrient by its id in a given food nutrients dictionary
        Args:
            food_nutrients: the nutrients dictionary in which the specific nutrient level is searched
            searched_id: the id of the wanted nutrient"""
        return next(
            (
                item["amount"]
                for item in food_nutrients
                if item["nutrient"]["id"] == searched_id
            ),
            None,
        )

    @staticmethod
    def __get_nutrient_unit(food_nutrients, searched_id):
        """Returns the nutrient unit of a nutrient by its id in a given food nutrients dictionary
        Args:
            food_nutrients: the nutrients dictionary in which the specific nutrient unit is searched
            searched_id: the id of the wanted nutrient"""
        return next(
            (
                item["nutrient"]["unitName"].lower()
                for item in food_nutrients
                if item["nutrient"]["id"] == searched_id
            ),
            None,
        )
