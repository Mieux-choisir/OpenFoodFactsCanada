from decimal import Decimal

from domain.mapper.nutrient_amount_mapper import NutrientAmountMapper
from domain.product.complexFields.nutrition_facts import NutritionFacts
from domain.product.complexFields.nutritionFactsPerHundredGrams import (
    NutritionFactsPerHundredGrams,
)
from domain.product.complexFields.nutritionFactsPerServing import (
    NutritionFactsPerServing,
)


class NutritionFactsMapper:
    """
    This is a class that maps products values to NutritionFacts objects.

    Attributes:
        sodium_to_salt (Decimal): The decimal value to convert sodium value to salt value

    Methods:
        map_fdc_dict_to_nutrition_facts(food_nutrients): Maps the given food nutrients list to a NutritionFacts object
        map_off_dict_to_nutrition_facts(product_dict): Maps the given dictionary to a NutritionFacts object
    """

    def __init__(self):
        self.sodium_to_salt = Decimal(2.5)
        self.units_in_nutrition_table = {
            "fat": "g",
            "saturatedFat": "g",
            "transFat": "g",
            "cholesterol": "mg",
            "sodium": "mg",
            "carbohydrates": "g",
            "fiber": "g",
            "sugars": "g",
            "protein": "g",
            "calcium": "mg",
            "iron": "mg",
            "potassium": "mg",
            "addedSugar": "g",
        }

    def map_fdc_dict_to_nutrition_facts(
        self,
        food_nutrients_per_100g: list[dict],
        food_nutrients_per_serving: dict,
        preparation_state_code: str,
    ) -> NutritionFacts:

        nutrition_facts_per_100g = self.__map_fdc_dict_to_nutrition_facts_per_100g(
            food_nutrients_per_100g
        )
        nutrition_facts_per_serving = (
            self.__map_fdc_dict_to_nutrition_facts_per_serving(
                food_nutrients_per_serving, preparation_state_code
            )
        )

        return NutritionFacts(
            nutrition_facts_per_hundred_grams=nutrition_facts_per_100g,
            nutrition_facts_per_serving=nutrition_facts_per_serving,
        )

    @staticmethod
    def map_off_dict_to_nutrition_facts(product_dict: dict) -> NutritionFacts:
        """Maps the values in a given OFF (jsonl) product to a NutritionFacts object"""
        nutriments = product_dict.get("nutriments", {})

        fields_100g = [
            "fat_100g",
            "salt_100g",
            "saturated-fat_100g",
            "sugars_100g",
            "carbohydrates_100g",
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

        nutrition_facts_100g = {
            field_mapping.get(field, field): (
                float(nutriments[field]) if field in nutriments else None
            )
            for field in fields_100g
        }

        fields_serving = [
            "fat_serving",
            "salt_serving",
            "saturated_fats_serving",
            "sugars_serving",
            "carbohydrates_serving",
            "energy_serving",
            "energy-kcal_serving",
            "proteins_serving",
            "fibers_serving",
            "sodium_serving",
            "trans_fats_serving",
            "cholesterol_serving",
            "calcium_serving",
            "iron_serving",
            "potassium_serving",
        ]

        serving_mapping = {
            "energy-kcal_serving": "energy_kcal_serving",
            "sugars_serving": "sugar_serving",
        }

        nutrition_facts_serving = {
            serving_mapping.get(field, field): (
                float(nutriments[field]) if field in nutriments else None
            )
            for field in fields_serving
        }

        return NutritionFacts(
            nutrition_facts_per_hundred_grams=NutritionFactsPerHundredGrams(
                **nutrition_facts_100g
            ),
            nutrition_facts_per_serving=NutritionFactsPerServing(
                **nutrition_facts_serving
            ),
        )

    def __map_fdc_dict_to_nutrition_facts_per_100g(
        self, food_nutrients: list[dict]
    ) -> NutritionFactsPerHundredGrams:
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
            value = self.__get_nutrient_level_per_100g(food_nutrients, nutrient_id)
            unit = self.__get_nutrient_unit(food_nutrients, nutrient_id)

            if field == "sodium_100g" and value is not None:
                nutrition_facts_data["salt_100g"] = NutrientAmountMapper().map_nutrient(
                    value * self.sodium_to_salt, unit
                )
            if field == "energy_kcal_100g" and value is not None:
                nutrition_facts_data["energy_kcal_100g"] = round(value)

            if field != "energy_kcal_100g":
                nutrition_facts_data[field] = NutrientAmountMapper().map_nutrient(
                    value, unit
                )

        return NutritionFactsPerHundredGrams(**nutrition_facts_data)

    def __map_fdc_dict_to_nutrition_facts_per_serving(
        self, food_nutrients_per_serving: dict, preparation_state_code: str
    ) -> NutritionFactsPerServing:
        is_for_prepared_food = None
        if (
            preparation_state_code is not None
            and preparation_state_code.strip().upper() == "PREPARED"
        ):
            is_for_prepared_food = True
        elif (
            preparation_state_code is not None
            and preparation_state_code == "UNPREPARED"
        ):
            is_for_prepared_food = False

        sodium_serving = self.__get_nutrient_level_per_serving(
            food_nutrients_per_serving, "sodium"
        )

        salt_serving = (
            float(sodium_serving) * float(self.sodium_to_salt)
            if sodium_serving is not None
            else None
        )

        return NutritionFactsPerServing(
            is_for_prepared_food=is_for_prepared_food,
            fat_serving=self.__get_nutrient_level_per_serving(
                food_nutrients_per_serving, "fat"
            ),
            saturated_fats_serving=self.__get_nutrient_level_per_serving(
                food_nutrients_per_serving, "saturatedFat"
            ),
            trans_fats_serving=self.__get_nutrient_level_per_serving(
                food_nutrients_per_serving, "transFat"
            ),
            cholesterol_serving=self.__get_nutrient_level_per_serving(
                food_nutrients_per_serving, "cholesterol"
            ),
            sodium_serving=sodium_serving,
            carbohydrates_serving=self.__get_nutrient_level_per_serving(
                food_nutrients_per_serving, "carbohydrates"
            ),
            fibers_serving=self.__get_nutrient_level_per_serving(
                food_nutrients_per_serving, "fiber"
            ),
            sugar_serving=self.__get_nutrient_level_per_serving(
                food_nutrients_per_serving, "sugars"
            ),
            proteins_serving=self.__get_nutrient_level_per_serving(
                food_nutrients_per_serving, "protein"
            ),
            calcium_serving=self.__get_nutrient_level_per_serving(
                food_nutrients_per_serving, "calcium"
            ),
            iron_serving=self.__get_nutrient_level_per_serving(
                food_nutrients_per_serving, "iron"
            ),
            energy_kcal_serving=self.__get_nutrient_level_per_serving(
                food_nutrients_per_serving, "calories"
            ),
            potassium_serving=self.__get_nutrient_level_per_serving(
                food_nutrients_per_serving, "potassium"
            ),
            added_sugar_serving=self.__get_nutrient_level_per_serving(
                food_nutrients_per_serving, "addedSugar"
            ),
            salt_serving=salt_serving,
        )

    def __get_nutrient_level_per_serving(
        self, food_nutrients_per_serving: dict, nutrient_name: str
    ) -> float:
        value = None
        if food_nutrients_per_serving.get(nutrient_name) is not None:
            value = food_nutrients_per_serving.get(nutrient_name).get("value")
            if nutrient_name != "calories":
                unit = self.units_in_nutrition_table.get(nutrient_name)
                value = NutrientAmountMapper().map_nutrient(value, unit)
        return value

    @staticmethod
    def __get_nutrient_level_per_100g(food_nutrients, searched_id):
        """Returns the nutrient level of a nutrient by its id in a given food nutrients dictionary.
        Returns None if the amount is greater than 100.

        Args:
            food_nutrients: the nutrients dictionary in which the specific nutrient level is searched
            searched_id: the id of the wanted nutrient
        """
        return next(
            (
                item["amount"]
                for item in food_nutrients
                if item["nutrient"]["id"] == searched_id and item["amount"] <= 100
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
