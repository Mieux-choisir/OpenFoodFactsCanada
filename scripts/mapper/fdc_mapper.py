# pylint: disable=missing-module-docstring, missing-function-docstring
from decimal import Decimal

from scripts.utils import *
from scripts.product import *

WANTED_COUNTRY = "Canada"


def map_fdc_dict_to_product(product_dict: dict, categories):
    """Maps a fdc dictionary to a product object"""
    country_field = 'marketCountry'
    id_field = 'gtinUpc'
    product_name_field = 'description'
    generic_name_field = 'description'
    brands_field = 'brandName'
    brand_owner_field = 'brandOwner'
    food_groups_en_field = 'brandedFoodCategory'  # TODO convert fdc categories to off food groups
    allergens_en_field = ''

    if product_dict['brandedFoodCategory'] in categories.keys():
        categories[product_dict['brandedFoodCategory']] += 1
    else:
        categories[product_dict['brandedFoodCategory']] = 1

    if product_dict['brandedFoodCategory'] == 'Berries/Small Fruit':
        print(product_dict['gtinUpc'], ":", product_dict['ingredients'], ":", product_dict)

    return Product(
        id=product_dict[id_field],
        product_name=product_dict[product_name_field].title(),
        generic_name_en=product_dict[generic_name_field].title(),
        is_raw=fdc_is_raw_aliment(product_dict['brandedFoodCategory']),
        brands=[product_dict[brand_owner_field].title(), product_dict[brands_field].title()] if brands_field in product_dict.keys() else [product_dict[brand_owner_field].title()],
        brand_owner=product_dict[brand_owner_field].title(),
        food_groups_en=product_dict[food_groups_en_field].split(','),
        ingredients=map_fdc_dict_to_ingredients(product_dict['ingredients']),
        nutrition_facts=map_fdc_dict_to_nutrition_facts(product_dict['foodNutrients']),
        allergens=[],
        nutriscore_data=map_fdc_dict_to_nutriscore_data(product_dict['foodNutrients']),
        ecoscore_data=map_fdc_dict_to_ecoscore_data(),
        nova_data=map_fdc_dict_to_nova_data()
    ), categories


def fdc_is_raw_aliment(category: str):
    is_raw = False

    if category in ['Vegetables  Unprepared/Unprocessed (Frozen)', 'Fruits, Vegetables & Produce', 'Vegetables - Unprepared/Unprocessed (Frozen)']:
        is_raw = True
    elif category == 'Pre-Packaged Fruit & Vegetables':
        is_raw = None #currently no way of knowing if the product is raw, there should be a more complex analysis
    return is_raw



def map_fdc_dict_to_ingredients(ingredients: str) -> Ingredients:
    ingredients_list = normalise_ingredients_list(ingredients)

    return Ingredients(
        ingredients_list=ingredients_list,
        ingredients_text=ingredients.title()
    )


def map_fdc_dict_to_nutrition_facts(food_nutrients: list[dict]) -> NutritionFacts:
    fat_id = 1004
    sodium_id = 1093
    saturated_fats_id = 1258
    sugar_field = 2000

    fat_level = next((item['amount'] for item in food_nutrients if item['nutrient']['id'] == fat_id), None)
    sodium_level = next((item['amount'] for item in food_nutrients if item['nutrient']['id'] == sodium_id), None)
    salt_level = sodium_level * Decimal('2.5') if sodium_level is not None else None
    saturated_fats_level = next((item['amount'] for item in food_nutrients if item['nutrient']['id'] == saturated_fats_id), None)
    sugar_level = next((item['amount'] for item in food_nutrients if item['nutrient']['id'] == sugar_field), None)
    nutrient_level = NutrientLevel(
        fat=fat_level,
        salt= salt_level,
        saturated_fats=saturated_fats_level,
        sugar=sugar_level,
    )

    carbohydrates_100g_field = 1005
    energy_100g_field = None  # TODO voir si on peut lui trouver quelque chose
    energy_kcal_100g_field = 1008
    vitamin_a_100g_field = 1104

    nutrients = Nutrients(
        carbohydrates_100g=next((item['nutrient']['number'] for item in food_nutrients if
                                 item['nutrient']['id'] == carbohydrates_100g_field), None),
        energy_100g=next(
            (item['nutrient']['number'] for item in food_nutrients if item['nutrient']['id'] == energy_100g_field),
            None),
        energy_kcal_100g=next(
            (item['nutrient']['number'] for item in food_nutrients if item['nutrient']['id'] == energy_kcal_100g_field),
            None),
        vitamin_a_100g=next(
            (item['nutrient']['number'] for item in food_nutrients if item['nutrient']['id'] == vitamin_a_100g_field),
            None),
    )

    return NutritionFacts(
        nutrient_level=nutrient_level,
        nutrients=nutrients,
    )


def map_fdc_dict_to_nutriscore_data(food_nutrients: list[dict]) -> NutriscoreData:
    nutriscore_score_id = None
    energy_id = 1008
    fibers_id = 1079
    fruit_percentage_id = None
    proteins_id = 1003
    saturated_fats_id = 1258
    sodium_id = 1093
    sugar_id = 2000

    return NutriscoreData(
        score=None,
        energy=next((item['nutrient']['number'] for item in food_nutrients if item['nutrient']['id'] == energy_id),
                    None),
        fibers=next((item['nutrient']['number'] for item in food_nutrients if item['nutrient']['id'] == fibers_id),
                    None),
        fruit_percentage=None,
        proteins=next((item['nutrient']['number'] for item in food_nutrients if item['nutrient']['id'] == proteins_id),
                      None),
        saturated_fats=next(
            (item['nutrient']['number'] for item in food_nutrients if item['nutrient']['id'] == saturated_fats_id),
            None),
        sodium=next((item['nutrient']['number'] for item in food_nutrients if item['nutrient']['id'] == sodium_id),
                    None),
        sugar=next((item['nutrient']['number'] for item in food_nutrients if item['nutrient']['id'] == sugar_id), None),
        is_beverage=None,
    )


def map_fdc_dict_to_ecoscore_data() -> EcoscoreData | None:
    return None


def map_fdc_dict_to_nova_data() -> NovaData | None:
    return None
