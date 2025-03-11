from decimal import Decimal

from domain.product.complexFields.nutrient_facts import NutritionFacts
from domain.product.complexFields.nutrient_level import NutrientLevel
from domain.product.complexFields.nutrients import Nutrients


class NutritionFactsMapper:

    @staticmethod
    def map_fdc_dict_to_nutrition_facts(food_nutrients: list[dict]) -> NutritionFacts:
        fat_id = 1004
        sodium_id = 1093
        saturated_fats_id = 1258
        sugar_id = 2000

        fat_level = next(
            (
                item["amount"]
                for item in food_nutrients
                if item["nutrient"]["id"] == fat_id
            ),
            None,
        )
        sodium_level = next(
            (
                item["amount"]
                for item in food_nutrients
                if item["nutrient"]["id"] == sodium_id
            ),
            None,
        )
        salt_level = sodium_level * Decimal("2.5") if sodium_level is not None else None
        saturated_fats_level = next(
            (
                item["amount"]
                for item in food_nutrients
                if item["nutrient"]["id"] == saturated_fats_id
            ),
            None,
        )
        sugar_level = next(
            (
                item["amount"]
                for item in food_nutrients
                if item["nutrient"]["id"] == sugar_id
            ),
            None,
        )
        nutrient_level = NutrientLevel(
            fat=fat_level,
            salt=salt_level,
            saturated_fats=saturated_fats_level,
            sugar=sugar_level,
        )

        carbohydrates_100g_id = 1005
        energy_kcal_100g_id = 1008
        vitamin_a_100g_id = 1104

        energy_kcal_100g_value = next(
            (
                item["amount"]
                for item in food_nutrients
                if item["nutrient"]["id"] == energy_kcal_100g_id
            ),
            None,
        )
        energy_100g_value = (
            energy_kcal_100g_value * Decimal(4.1868)
            if energy_kcal_100g_value is not None
            else None
        )

        carbohydrates_100g_value = next(
            (
                item["amount"]
                for item in food_nutrients
                if item["nutrient"]["id"] == carbohydrates_100g_id
            ),
            None,
        )

        vitamin_a_100g_value = next(
            (
                item["amount"]
                for item in food_nutrients
                if item["nutrient"]["id"] == vitamin_a_100g_id
            ),
            None,
        )

        nutrients = Nutrients(
            carbohydrates_100g=carbohydrates_100g_value,
            energy_100g=energy_100g_value,
            energy_kcal_100g=energy_kcal_100g_value,
            vitamin_a_100g=vitamin_a_100g_value,
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
            fat=row[fat_index],
            salt=row[salt_index],
            saturated_fats=row[saturated_fats_index],
            sugar=row[sugar_index],
        )

        carbohydrates_100g_index = header.index("carbohydrates_100g")
        energy_100g_index = header.index("energy_100g")
        energy_kcal_100g_index = header.index("energy-kcal_100g")
        vitamin_a_100g_index = header.index("vitamin-a_100g")

        nutrients = Nutrients(
            carbohydrates_100g=row[carbohydrates_100g_index],
            energy_100g=row[energy_100g_index],
            energy_kcal_100g=row[energy_kcal_100g_index],
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
