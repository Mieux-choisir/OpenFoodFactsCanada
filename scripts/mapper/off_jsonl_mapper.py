# pylint: disable=missing-module-docstring, missing-function-docstring
from scripts.utils import *
from scripts.product import *

WANTED_COUNTRY = "Canada"


def map_off_dict_to_product(product_dict: dict) -> Product | None:
    country_field = "countries"
    if product_dict.get(country_field, "") != WANTED_COUNTRY:
        return None

    id_field = "code"
    product_name_field = "product_name"
    generic_name_field = "generic_name"
    brand_owner_field = "brands"
    food_groups_en_field = "food_groups"
    allergens_en_field = "allergens"

    return Product(
        id=product_dict[id_field],
        product_name=product_dict.get(product_name_field, ""),
        generic_name_en=product_dict.get(generic_name_field, ""),
        is_raw=off_json_is_raw_aliment(product_dict),
        brand_name=product_dict.get(brand_owner_field, ""),
        food_groups_en=product_dict.get(food_groups_en_field, "").split(",") if isinstance(product_dict.get(food_groups_en_field, ""), str) else product_dict.get(food_groups_en_field, []),
        #food_groups_en = product_dict.get(food_groups_en_field, []),
        ingredients=map_off_dict_to_ingredients(product_dict),
        nutrition_facts=map_off_dict_to_nutrition_facts(product_dict),
        allergens=product_dict.get(allergens_en_field, "").split(",") if isinstance(product_dict.get(allergens_en_field, ""), str) else product_dict.get(allergens_en_field, []),
        nutriscore_data=map_off_dict_to_nutriscore_data(product_dict),
        ecoscore_data=map_off_dict_to_ecoscore_data(product_dict),
        nova_data=map_off_dict_to_nova_data(product_dict)
    )


def off_json_is_raw_aliment(product_dict: dict) -> bool:
    """Checks if the aliment is raw based on its dict values"""
    # Check the NOVA group
    nova_field = "nova_group"
    nova_group = product_dict.get(nova_field, None)

    try:
        if check_nova_raw_group(nova_group):
            return True
        if check_nova_transformed_group(nova_group):
            return False
    except ValueError:
        pass

    # Check the PNNS groups
    pnns_field = "pnns_groups_1"
    if check_pnn_groups(product_dict.get(pnns_field, None)):
        return True

    # Check the categories
    cat_field = "categories_tags"
    if check_list_categories(product_dict.get(cat_field, [])):
        return True

    # Check the additives
    additives_field = "additives_n"
    try:
        if check_additives(product_dict.get(additives_field, None), nova_group):
            return True
    except ValueError:
        pass

    return False


def map_off_dict_to_ingredients(product_dict: dict) -> Ingredients:
    ingredients_text_field = "ingredients_text"

    return Ingredients(
        ingredients_list=[],
        ingredients_text=product_dict.get(ingredients_text_field, None)
    )


def map_off_dict_to_nutrition_facts(product_dict: dict) -> NutritionFacts:
    nutriments_field = "nutriments"
    fat_field = "fat_100g"
    salt_field = "salt_100g"
    saturated_fats_field = "saturated-fat_100g"
    sugar_field = "sugars_100g"

    nutrient_level = NutrientLevel(
        fat=product_dict.get(nutriments_field, {}).get(fat_field, None),
        salt=product_dict.get(nutriments_field, {}).get(salt_field, None),
        saturated_fats=product_dict.get(nutriments_field, {}).get(saturated_fats_field, None),
        sugar=product_dict.get(nutriments_field, {}).get(sugar_field, None)
    )

    carbohydrates_100g_field = "carbohydrates_100g"
    energy_100g_field = "energy_100g"
    energy_kcal_100g_field = "energy-kcal_100g"
    vitamin_a_100g_field = "vitamin-a_100g"

    nutrients = Nutrients(
        carbohydrates_100g=product_dict.get(nutriments_field, {}).get(carbohydrates_100g_field, None),
        energy_100g=product_dict.get(nutriments_field, {}).get(energy_100g_field, None),
        energy_kcal_100g=product_dict.get(nutriments_field, {}).get(energy_kcal_100g_field, None),
        vitamin_a_100g=product_dict.get(nutriments_field, {}).get(vitamin_a_100g_field, None)
    )


    return NutritionFacts(
        nutrient_level=nutrient_level,
        nutrients=nutrients,
    )


def map_off_dict_to_nutriscore_data(product_dict: dict) -> NutriscoreData:
    nutriments_field = "nutriments"
    nutriscore_score_field = "nutriscore_grade"
    energy_field = "energy_100g"
    fibers_field = "fiber_100g"
    fruit_percentage_field = "fruits-vegetables-nuts_100g"
    proteins_field = "proteins_100g"
    saturated_fats_field = "saturated-fat_100g"
    sodium_field = "sodium_100g"
    sugar_field = "sugars_100g"

    return NutriscoreData(
        score=map_letter_to_number(product_dict.get(nutriscore_score_field, None)) if product_dict.get(nutriscore_score_field, None) is not None else None,
        energy=product_dict.get(nutriments_field, {}).get(energy_field, None),
        fibers=product_dict.get(nutriments_field, {}).get(fibers_field, None),
        fruit_percentage=product_dict.get(nutriments_field, {}).get(fruit_percentage_field, None),
        proteins=product_dict.get(nutriments_field, {}).get(proteins_field, None),
        saturated_fats=product_dict.get(nutriments_field, {}).get(saturated_fats_field, None),
        sodium=product_dict.get(nutriments_field, {}).get(sodium_field, None),
        sugar=product_dict.get(nutriments_field, {}).get(sugar_field, None),
        is_beverage=None,
    )

def map_off_dict_to_ecoscore_data(product_dict: dict) -> EcoscoreData:
    score_field = "environmental_score_score"
    
    score = product_dict.get(score_field, None)
    
    origin_of_ingredients = list() 
    if "originOfIngredients" in product_dict:
        origin_of_ingredients = [map_dict_to_origin_of_ingredients(product_dict)]

    packaging = map_dict_to_packaging(product_dict) if "packaging" in product_dict else None
    production_system = map_dict_to_production_system(product_dict) if "production_system" in product_dict else None

    return EcoscoreData(
        score=score,
        origin_of_ingredients=origin_of_ingredients,
        packaging=packaging,
        production_system=production_system,
        threatened_species={} 
    )


def map_dict_to_origin_of_ingredients(product_dict: dict) -> OriginOfIngredients:
    origin_field = "origins"

    return OriginOfIngredients(
        origin=product_dict.get(origin_field, None),
        percent=None,
        transportation_score=None,
    )


def map_dict_to_packaging(product_dict: dict) -> Packaging:
    packaging_field = "packaging"
    #print(""packaging tags"", product_dict[""packaging_tags""])
    #print(""packaging_materials_tags"", product_dict[""packaging_materials_tags""])
    #print(""packaging_text"", product_dict[""packaging_text""])
    #print(""packagings_complete"", product_dict[""packagings_complete""])
    #print(""packagings_materials"", product_dict[""packagings_materials""])
    #print(""packagings_materials_main"", product_dict[""packagings_materials_main""])
    #print(""packagings"", product_dict[""packagings""])
    #print(""packagings_n"", product_dict[""packagings_n""])
    #print(""packaging"", product_dict[""packaging""])

    packaging_data = product_dict.get(packaging_field, None)

    return Packaging(
        non_recyclable_and_non_biodegradable_materials=None,
        #packaging=product_dict[packaging_field].split(",") if product_dict[packaging_field] is not None else []
        packaging=packaging_data.split(",") if packaging_data else [] 
    )


def map_dict_to_production_system(product_dict: dict) -> ProductionSystem:
    labels_field = "labels"

    labels_data = product_dict.get(labels_field, None)

    return ProductionSystem(
        #labels=product_dict[labels_field].split(",") if product_dict[labels_field] is not None else [], #TODO check other fields
        labels=labels_data.split(",") if labels_data else [],
        value=None,
        warning=None,
    )

def map_off_dict_to_nova_data(product_dict: dict) -> NovaData:
    score_field = "nova_group"
    
    score_value = product_dict.get(score_field, None)
    
    score = int(score_value) if score_value is not None else None

    return NovaData(
        score=score,
        group_markers={} 
    )
