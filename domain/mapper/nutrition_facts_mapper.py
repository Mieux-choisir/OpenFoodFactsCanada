from decimal import Decimal

from domain.mapper.nutrient_amount_mapper import NutrientAmountMapper
from domain.product.complexFields.nutrient_facts import NutritionFacts
from domain.product.complexFields.nutrient_level import NutrientLevel
from domain.product.complexFields.nutrients import Nutrients
from domain.utils.converter import Converter


class NutritionFactsMapper:

    def __init__(self):
        self.energy_kcal_to_kj = Decimal(4.1868)
        self.sodium_to_salt = Decimal(2.5)

    def map_fdc_dict_to_nutrition_facts(
        self, food_nutrients: list[dict]
    ) -> NutritionFacts:
        fat_id = 1004
        sodium_id = 1093
        saturated_fats_id = 1258
        sugar_id = 2000

        fat_level = self.__get_nutrient_level(food_nutrients, fat_id)
        fat_unit = self.__get_nutrient_unit(food_nutrients, fat_id)

        sodium_level = self.__get_nutrient_level(food_nutrients, sodium_id)
        sodium_unit = self.__get_nutrient_unit(food_nutrients, sodium_id)
        salt_level = sodium_level * self.sodium_to_salt if sodium_level is not None else None

        saturated_fats_level = self.__get_nutrient_level(
            food_nutrients, saturated_fats_id
        )
        saturated_fats_unit = self.__get_nutrient_unit(
            food_nutrients, saturated_fats_id
        )

        sugar_level = self.__get_nutrient_level(food_nutrients, sugar_id)
        sugar_unit = self.__get_nutrient_unit(food_nutrients, sugar_id)

        nutrient_level = NutrientLevel(
            fat=NutrientAmountMapper().map_nutrient("fat", fat_level, fat_unit),
            salt=NutrientAmountMapper().map_nutrient("salt", salt_level, sodium_unit),
            saturated_fats=NutrientAmountMapper().map_nutrient(
                "saturated_fats", saturated_fats_level, saturated_fats_unit
            ),
            sugar=NutrientAmountMapper().map_nutrient("sugar", sugar_level, sugar_unit),
        )

        carbohydrates_100g_id = 1005
        energy_kcal_100g_id = 1008
        vitamin_a_100g_id = 1104

        energy_kcal_100g_value = self.__get_nutrient_level(
            food_nutrients, energy_kcal_100g_id
        )
        energy_100g_value = (
            energy_kcal_100g_value * self.energy_kcal_to_kj
            if energy_kcal_100g_value is not None
            else None
        )

        carbohydrates_100g_value = self.__get_nutrient_level(
            food_nutrients, carbohydrates_100g_id
        )
        carbohydrates_100g_unit = self.__get_nutrient_unit(
            food_nutrients, carbohydrates_100g_id
        )

        vitamin_a_100g_value = self.__get_nutrient_level(
            food_nutrients, vitamin_a_100g_id
        )
        vitamin_a_100g_unit = self.__get_nutrient_unit(
            food_nutrients, vitamin_a_100g_id
        )

        nutrients = Nutrients(
            carbohydrates_100g=NutrientAmountMapper().map_nutrient(
                "carbohydrates", carbohydrates_100g_value, carbohydrates_100g_unit
            ),
            energy_100g=energy_100g_value,
            energy_kcal_100g=energy_kcal_100g_value,
            vitamin_a_100g=NutrientAmountMapper().map_nutrient(
                "vitamin_a", vitamin_a_100g_value, vitamin_a_100g_unit
            ),
        )

        return NutritionFacts(
            nutrient_level=nutrient_level,
            nutrients=nutrients,
        )

    @staticmethod
    def map_off_row_to_nutrition_facts(
        row: list[str], header: list[str]
    ) -> NutritionFacts:
        fat_index = header.index("fat_100g")
        salt_index = header.index("salt_100g")
        saturated_fats_index = header.index("saturated-fat_100g")
        sugar_index = header.index("sugars_100g")

        nutrient_level = NutrientLevel(
            fat=Converter.safe_float(row[fat_index]),
            salt=row[salt_index],
            saturated_fats=Converter.safe_float(row[saturated_fats_index]),
            sugar=row[sugar_index],
        )

        carbohydrates_100g_index = header.index("carbohydrates_100g")
        energy_100g_index = header.index("energy_100g")
        energy_kcal_100g_index = header.index("energy-kcal_100g")
        vitamin_a_100g_index = header.index("vitamin-a_100g")

        nutrients = Nutrients(
            carbohydrates_100g=row[carbohydrates_100g_index],
            energy_100g=Converter.safe_float(row[energy_100g_index]),
            energy_kcal_100g=Converter.safe_float(row[energy_kcal_100g_index]),
            vitamin_a_100g=row[vitamin_a_100g_index],
        )

        return NutritionFacts(
            nutrient_level=nutrient_level,
            nutrients=nutrients,
        )

    @staticmethod
    def map_off_dict_to_nutrition_facts(product_dict: dict) -> NutritionFacts:
        nutriments_field = "nutriments"
        fat_field = "fat_100g"
        salt_field = "salt_100g"
        saturated_fats_field = "saturated-fat_100g"
        sugar_field = "sugars_100g"

        nutrient_level = NutrientLevel(
            fat=product_dict[nutriments_field][fat_field],
            salt=product_dict[nutriments_field][salt_field],
            saturated_fats=product_dict[nutriments_field][saturated_fats_field],
            sugar=product_dict[nutriments_field][sugar_field],
        )

        carbohydrates_100g_field = "carbohydrates_100g"
        energy_100g_field = "energy_100g"
        energy_kcal_100g_field = "energy-kcal_100g"
        vitamin_a_100g_field = "vitamin-a_100g"

        nutrients = Nutrients(
            carbohydrates_100g=product_dict[nutriments_field][carbohydrates_100g_field],
            energy_100g=product_dict[nutriments_field][energy_100g_field],
            energy_kcal_100g=product_dict[nutriments_field][energy_kcal_100g_field],
            vitamin_a_100g=product_dict[nutriments_field][vitamin_a_100g_field],
        )

        return NutritionFacts(
            nutrient_level=nutrient_level,
            nutrients=nutrients,
        )

    @staticmethod
    def __get_nutrient_level(food_nutrients, searched_id):
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
        return next(
            (
                item["nutrient"]["unitName"].lower()
                for item in food_nutrients
                if item["nutrient"]["id"] == searched_id
            ),
            None,
        )
