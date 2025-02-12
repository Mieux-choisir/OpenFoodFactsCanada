# pylint: disable=missing-module-docstring, missing-function-docstring
from scripts.utils import *
from scripts.product import *

WANTED_COUNTRY = "Canada"


def map_off_row_to_product(row: list[str], header: list[str]) -> Product | None:
    country_index = header.index("countries_en")
    if row[country_index] != WANTED_COUNTRY:
        return None

    id_index = header.index("code")
    product_name_index = header.index("product_name")
    generic_name_index = header.index("generic_name")

    return Product(
        id=row[id_index],
        product_name=row[product_name_index].strip() if row[product_name_index] is not None else None,
        generic_name_en=row[generic_name_index].strip() if row[generic_name_index] is not None else None,
        is_raw=off_csv_is_raw_aliment(row, header),
        brands=map_off_row_to_brands(row, header),
        brand_owner=map_off_row_to_brand_owner(row, header),
        food_groups_en=map_off_row_to_food_groups(row, header),
        ingredients=map_off_row_to_ingredients(row, header),
        nutrition_facts=map_off_row_to_nutrition_facts(row, header),
        allergens=map_off_row_to_allergens(row, header),
        nutriscore_data=map_off_row_to_nutriscore_data(row, header),
        ecoscore_data=map_off_row_to_ecoscore_data(row, header),
        nova_data=map_off_row_to_nova_data(row, header),
    )


def off_csv_is_raw_aliment(row: list[str], header: list[str]) -> bool:
    """Checks if the aliment is raw based on its row values"""
    # Check the NOVA group
    nova_index = header.index("nova_group")
    nova_group = row[nova_index]
    try:
        if check_nova_raw_group(nova_group):
            return True
        if check_nova_transformed_group(nova_group):
            return False
    except ValueError:
        pass

    # Check the PNNS groups
    pnns_index = header.index("pnns_groups_1")
    if check_pnn_groups(row[pnns_index]):
        return True

    # Check the categories
    cat_index = header.index("categories_tags")
    if check_string_categories(row[cat_index]):
        return True

    # Check the additives
    additives_index = header.index("additives_n")
    try:
        if check_additives(row[additives_index], nova_group):
            return True
    except ValueError:
        pass

    return False


def map_off_row_to_brands(row: list[str], header: list[str]) -> list[str]:
    brands_index = header.index("brands")

    brands = []
    if row[brands_index] is not None and row[brands_index] != "":
        brands = row[brands_index].split(',')
    return brands


def map_off_row_to_brand_owner(row: list[str], header: list[str]) -> str | None:
    brands_index = header.index("brands")
    brand_owner_index = header.index("brand_owner")

    brand_owner = None
    if row[brand_owner_index] is not None and row[brand_owner_index] != "":
        brand_owner = row
    elif row[brands_index] is not None and row[brands_index] != "":
        brand_owner = row[brands_index]
    return brand_owner


def map_off_row_to_food_groups(row: str, header: list[str]) -> list[str]:
    food_groups_index = header.index("food_groups_en")

    food_groups = []
    if row[food_groups_index] is not None:
        food_groups = row[food_groups_index].split(',')
    return food_groups


def map_off_row_to_ingredients(row: list[str], header: list[str]) -> Ingredients:
    ingredients_text_index = header.index("ingredients_text")

    return Ingredients(
        ingredients_list=[],
        ingredients_text=row[ingredients_text_index],
    )


def map_off_row_to_nutrition_facts(row: list[str], header: list[str]) -> NutritionFacts:
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


def map_off_row_to_allergens(row: list[str], header: list[str]) -> list[str]:
    allergens_index = header.index("allergens")

    allergens = []
    if row[allergens_index] != "" and row[allergens_index] is not None:
        allergens = row[allergens_index].split(',')
    return allergens


def map_off_row_to_nutriscore_data(row: list[str], header: list[str]) -> NutriscoreData:
    nutriscore_score_index = header.index("nutriscore_grade")
    energy_index = header.index("energy_100g")
    fibers_index = header.index("fiber_100g")
    fruit_percentage_index = header.index("fruits-vegetables-nuts_100g")
    proteins_index = header.index("proteins_100g")
    saturated_fats_index = header.index("saturated-fat_100g")
    sodium_index = header.index("sodium_100g")
    sugar_index = header.index("sugars_100g")

    return NutriscoreData(
        score=map_letter_to_number(row[nutriscore_score_index]) if row[nutriscore_score_index] else None,
        energy=row[energy_index],
        fibers=row[fibers_index],
        fruit_percentage=row[fruit_percentage_index],
        proteins=row[proteins_index],
        saturated_fats=row[saturated_fats_index],
        sodium=row[sodium_index],
        sugar=row[sugar_index],
        is_beverage=None,
    )


def map_off_row_to_ecoscore_data(row: list[str], header: list[str]) -> EcoscoreData:
    score_index = header.index("environmental_score_score")

    origin_of_ingredients: list[OriginOfIngredients] = [
        map_row_to_origin_of_ingredients(row, header)
    ]
    packaging = map_row_to_packaging(row, header)
    production_system = map_row_to_production_system(row, header)

    return EcoscoreData(
        score=int(row[score_index]) if row[score_index] else None,
        origin_of_ingredients=origin_of_ingredients,
        packaging=packaging,
        production_system=production_system,
        threatened_species={},
    )


def map_row_to_origin_of_ingredients(row: list[str], header: list[str]) -> OriginOfIngredients:
    origin_index = header.index("origins")

    return OriginOfIngredients(
        origin=row[origin_index],
        percent=None,
        transportation_score=None,
    )


def map_row_to_packaging(row: list[str], header: list[str]) -> Packaging:
    packaging_index = header.index("packaging")

    return Packaging(
        non_recyclable_and_non_biodegradable_materials=None,
        packaging=row[packaging_index].split(",")
    )


def map_row_to_production_system(row: list[str], header: list[str]) -> ProductionSystem:
    labels_index = header.index("labels")

    return ProductionSystem(
        labels=row[labels_index].split(","),
        value=None,
        warning=None,
    )


def map_off_row_to_nova_data(row: list[str], header: list[str]) -> NovaData:
    score_index = header.index("nova_group")

    return NovaData(
        score=int(row[score_index]) if row[score_index] else None,
        group_markers={}
    )
