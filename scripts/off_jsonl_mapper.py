# pylint: disable=missing-module-docstring, missing-function-docstring
from utils import *
from product import *

WANTED_COUNTRY = "Canada"


def map_off_dict_to_product(product_dict: dict) -> Product | None:
    country_field = "countries"
    if product_dict[country_field] != WANTED_COUNTRY:
        return None

    id_field = "code"
    product_name_field = "product_name"
    generic_name_field = "generic_name"
    brand_owner_field = "brands"
    food_groups_en_field = "food_groups"
    allergens_en_field = "allergens"

    return Product(
        id=product_dict[id_field],
        product_name=product_dict[product_name_field],
        generic_name_en=product_dict[generic_name_field],
        is_raw=off_json_is_raw_aliment(product_dict),
        brand_name=product_dict[brand_owner_field],
        food_groups_en=[product_dict[food_groups_en_field] if product_dict[food_groups_en_field] is not None else ''],
        ingredients=map_off_dict_to_ingredients(product_dict),
        nutrition_facts=map_off_dict_to_nutrition_facts(product_dict),
        allergens=[product_dict[allergens_en_field]],
        nutriscore_data=map_off_dict_to_nutriscore_data(product_dict),
        ecoscore_data=map_off_dict_to_ecoscore_data(product_dict),
        nova_data=map_off_dict_to_nova_data(product_dict)
    )


def off_json_is_raw_aliment(product_dict: dict) -> bool:
    """Checks if the aliment is raw based on its dict values"""
    # Check the NOVA group
    nova_field = "nova_group"
    nova_group = product_dict[nova_field]

    try:
        if check_nova_raw_group(nova_group):
            return True
        if check_nova_transformed_group(nova_group):
            return False
    except ValueError:
        pass

    # Check the PNNS groups
    pnns_field = "pnns_groups_1"
    if check_pnn_groups(product_dict[pnns_field]):
        return True

    # Check the categories
    cat_field = "categories_tags"
    if check_list_categories(product_dict[cat_field]):
        return True

    # Check the additives
    additives_field = "additives_n"
    try:
        if check_additives(product_dict[additives_field], nova_group):
            return True
    except ValueError:
        pass

    return False


def map_off_dict_to_ingredients(product_dict: dict) -> Ingredients:
    ingredients_text_field = "ingredients_text"

    return Ingredients(
        ingredients_list=[],
        ingredients_text=product_dict[ingredients_text_field],
    )


def map_off_dict_to_nutrition_facts(product_dict: dict) -> NutritionFacts:
    nutriments_field = 'nutriments'
    fat_field = "fat_100g"
    salt_field = "salt_100g"
    saturated_fats_field = "saturated-fat_100g"
    sugar_field = "sugars_100g"

    nutrient_level = NutrientLevel(
        fat=product_dict[nutriments_field][fat_field],
        salt=product_dict[nutriments_field][salt_field],
        saturated_fats=product_dict[nutriments_field][saturated_fats_field],
        sugar=product_dict[nutriments_field][sugar_field]
    )

    carbohydrates_100g_field = "carbohydrates_100g"
    energy_100g_field = "energy_100g"
    energy_kcal_100g_field = "energy-kcal_100g"
    vitamin_a_100g_field = "vitamin-a_100g"

    nutrients = Nutrients(
        carbohydrates_100g=product_dict[nutriments_field][carbohydrates_100g_field],
        energy_100g=product_dict[nutriments_field][energy_100g_field],
        energy_kcal_100g=product_dict[nutriments_field][energy_kcal_100g_field],
        vitamin_a_100g=product_dict[nutriments_field][vitamin_a_100g_field]
    )

    return NutritionFacts(
        nutrient_level=nutrient_level,
        nutrients=nutrients,
    )


def map_off_dict_to_nutriscore_data(product_dict: dict) -> NutriscoreData:
    nutriments_field = 'nutriments'
    nutriscore_score_field = "nutriscore_grade"
    energy_field = "energy_100g"
    fibers_field = "fiber_100g"
    fruit_percentage_field = "fruits-vegetables-nuts_100g"
    proteins_field = "proteins_100g"
    saturated_fats_field = "saturated-fat_100g"
    sodium_field = "sodium_100g"
    sugar_field = "sugars_100g"

    return NutriscoreData(
        score=map_letter_to_number(product_dict[nutriscore_score_field]) if product_dict[nutriscore_score_field] else None,
        energy=product_dict[nutriments_field][energy_field],
        fibers=product_dict[nutriments_field][fibers_field],
        fruit_percentage=product_dict[nutriments_field][fruit_percentage_field],
        proteins=product_dict[nutriments_field][proteins_field],
        saturated_fats=product_dict[nutriments_field][saturated_fats_field],
        sodium=product_dict[nutriments_field][sodium_field],
        sugar=product_dict[nutriments_field][sugar_field],
        is_beverage=None,
    )


def map_off_dict_to_ecoscore_data(product_dict: dict) -> EcoscoreData:
    score_field = "environmental_score_score"

    origin_of_ingredients: list[OriginOfIngredients] = [
        map_dict_to_origin_of_ingredients(product_dict)
    ]
    packaging = map_dict_to_packaging(product_dict)
    production_system = map_dict_to_production_system(product_dict)

    return EcoscoreData(
        score=int(product_dict[score_field]) if product_dict[score_field] else None,
        origin_of_ingredients=origin_of_ingredients,
        packaging=packaging,
        production_system=production_system,
        threatened_species={}
    )


def map_dict_to_origin_of_ingredients(product_dict: dict) -> OriginOfIngredients:
    origin_field = "origins"

    return OriginOfIngredients(
        origin=product_dict[origin_field],
        percent=None,
        transportation_score=None,
    )


def map_dict_to_packaging(product_dict: dict) -> Packaging:
    packaging_field = "packaging"
    #print('packaging tags', product_dict['packaging_tags'])
    #print('packaging_materials_tags', product_dict['packaging_materials_tags'])
    #print('packaging_text', product_dict['packaging_text'])
    #print('packagings_complete', product_dict['packagings_complete'])
    #print('packagings_materials', product_dict['packagings_materials'])
    #print('packagings_materials_main', product_dict['packagings_materials_main'])
    #print('packagings', product_dict['packagings'])
    #print('packagings_n', product_dict['packagings_n'])
    #print('packaging', product_dict['packaging'])

    return Packaging(
        non_recyclable_and_non_biodegradable_materials=None,
        packaging=product_dict[packaging_field].split(",") if product_dict[packaging_field] is not None else []
    )


def map_dict_to_production_system(product_dict: dict) -> ProductionSystem:
    labels_field = "labels"

    return ProductionSystem(
        labels=product_dict[labels_field].split(",") if product_dict[labels_field] is not None else [], #TODO check other fields
        value=None,
        warning=None,
    )


def map_off_dict_to_nova_data(product_dict: dict) -> NovaData:
    score_field = "nova_group"

    return NovaData(
        score=int(product_dict[score_field]) if product_dict[score_field] else None,
        group_markers={}
    )
