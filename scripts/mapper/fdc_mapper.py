# pylint: disable=missing-module-docstring, missing-function-docstring
from scripts.utils import normalise_ingredients_list
from scripts.product import Product, Ingredients, NutritionFacts, NutrientLevel, Nutrients, NutriscoreData, EcoscoreData, NovaData

WANTED_COUNTRY = "Canada"


def map_fdc_dict_to_product(dict: dict) -> Product:
    """Maps a fdc dictionary to a product object"""
    id_field = "gtinUpc"
    product_name_field = "description"
    generic_name_field = "description"
    brand_owner_field = "brandOwner"

    return Product(
        id=dict[id_field],
        product_name=dict[product_name_field].title(),
        generic_name_en=dict[generic_name_field].title(),
        is_raw=None,  # TODO verifier si cest toujours cru ou pas
        brand_name=dict[brand_owner_field].title(),
        food_groups_en=[""],  # TODO compléter la liste si possible
        ingredients=map_fdc_dict_to_ingredients(dict["ingredients"]),
        nutrition_facts=map_fdc_dict_to_nutrition_facts(dict["foodNutrients"]),
        allergens=[""],  # TODO compléter la liste si possible
        nutriscore_data=map_fdc_dict_to_nutriscore_data(dict["foodNutrients"]),
        ecoscore_data=map_fdc_dict_to_ecoscore_data(),
        nova_data=map_fdc_dict_to_nova_data(),
    )


def map_fdc_dict_to_ingredients(ingredients: str) -> Ingredients:
    ingredients_list = normalise_ingredients_list(ingredients)

    return Ingredients(
        ingredients_list=ingredients_list, ingredients_text=ingredients.title()
    )


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


def map_fdc_dict_to_nutriscore_data(food_nutrients: list[dict]) -> NutriscoreData:
    energy_id = 1008
    fibers_id = 1079
    proteins_id = 1003
    saturated_fats_id = 1258
    sodium_id = 1093
    sugar_id = 2000

    return NutriscoreData(
        score=None,
        energy=next(
            (
                item["nutrient"]["number"]
                for item in food_nutrients
                if item["nutrient"]["id"] == energy_id
            ),
            None,
        ),
        fibers=next(
            (
                item["nutrient"]["number"]
                for item in food_nutrients
                if item["nutrient"]["id"] == fibers_id
            ),
            None,
        ),
        fruit_percentage=None,
        proteins=next(
            (
                item["nutrient"]["number"]
                for item in food_nutrients
                if item["nutrient"]["id"] == proteins_id
            ),
            None,
        ),
        saturated_fats=next(
            (
                item["nutrient"]["number"]
                for item in food_nutrients
                if item["nutrient"]["id"] == saturated_fats_id
            ),
            None,
        ),
        sodium=next(
            (
                item["nutrient"]["number"]
                for item in food_nutrients
                if item["nutrient"]["id"] == sodium_id
            ),
            None,
        ),
        sugar=next(
            (
                item["nutrient"]["number"]
                for item in food_nutrients
                if item["nutrient"]["id"] == sugar_id
            ),
            None,
        ),
        is_beverage=None,
    )


def map_fdc_dict_to_ecoscore_data() -> EcoscoreData:
    return EcoscoreData(
        score=None,
        origin_of_ingredients=[],
        packaging=None,
        production_system=None,
        threatened_species={},
    )


def map_fdc_dict_to_nova_data() -> NovaData:
    return NovaData(score=None, group_markers={})
