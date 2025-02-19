from domain.product.complexFields.nutrient_facts import NutritionFacts
from domain.product.complexFields.nutrient_level import NutrientLevel
from domain.product.complexFields.nutrients import Nutrients


class NutritionFactsMapper:
    @staticmethod
    def map_fdc_dict_to_nutrition_facts(food_nutrients: list[dict]) -> NutritionFacts:
        fat_id = 1004
        sodium_id = 1093  # TODO convertir sodium en sel
        saturated_fats_id = 1258
        sugar_field = 2000

        nutrient_level = NutrientLevel(
            fat=next(
                (
                    item["nutrient"]["number"]
                    for item in food_nutrients
                    if item["nutrient"]["id"] == fat_id
                ),
                None,
            ),
            salt=next(
                (
                    item["nutrient"]["number"]
                    for item in food_nutrients
                    if item["nutrient"]["id"] == sodium_id
                ),
                None,
            ),
            # TODO convertir sodium en sel
            saturated_fats=next(
                (
                    item["nutrient"]["number"]
                    for item in food_nutrients
                    if item["nutrient"]["id"] == saturated_fats_id
                ),
                None,
            ),
            sugar=next(
                (
                    item["nutrient"]["number"]
                    for item in food_nutrients
                    if item["nutrient"]["id"] == sugar_field
                ),
                None,
            ),
        )

        carbohydrates_100g_field = 1005
        energy_100g_field = None  # TODO voir si on peut lui trouver quelque chose
        energy_kcal_100g_field = 1008
        vitamin_a_100g_field = 1104

        nutrients = Nutrients(
            carbohydrates_100g=next(
                (
                    item["nutrient"]["number"]
                    for item in food_nutrients
                    if item["nutrient"]["id"] == carbohydrates_100g_field
                ),
                None,
            ),
            energy_100g=next(
                (
                    item["nutrient"]["number"]
                    for item in food_nutrients
                    if item["nutrient"]["id"] == energy_100g_field
                ),
                None,
            ),
            energy_kcal_100g=next(
                (
                    item["nutrient"]["number"]
                    for item in food_nutrients
                    if item["nutrient"]["id"] == energy_kcal_100g_field
                ),
                None,
            ),
            vitamin_a_100g=next(
                (
                    item["nutrient"]["number"]
                    for item in food_nutrients
                    if item["nutrient"]["id"] == vitamin_a_100g_field
                ),
                None,
            ),
        )

        return NutritionFacts(
            nutrient_level=nutrient_level,
            nutrients=nutrients,
        )

    @staticmethod
    def map_off_row_to_nutrition_facts(row: list[str], header: list[str]) -> NutritionFacts:
        fat_field = header.index("fat_100g")
        salt_field = header.index("salt_100g")
        saturated_fats_field = header.index("saturated-fat_100g")
        sugar_field = header.index("sugars_100g")

        nutrient_level = NutrientLevel(
            fat=row[fat_field],
            salt=row[salt_field],
            saturated_fats=row[saturated_fats_field],
            sugar=row[sugar_field],
        )

        carbohydrates_100g_field = header.index("carbohydrates_100g")
        energy_100g_field = header.index("energy_100g")
        energy_kcal_100g_field = header.index("energy-kcal_100g")
        vitamin_a_100g_field = header.index("vitamin-a_100g")

        nutrients = Nutrients(
            carbohydrates_100g=row[carbohydrates_100g_field],
            energy_100g=row[energy_100g_field],
            energy_kcal_100g=row[energy_kcal_100g_field],
            vitamin_a_100g=row[vitamin_a_100g_field],
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
