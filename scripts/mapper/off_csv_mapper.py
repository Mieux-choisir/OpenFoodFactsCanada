# pylint: disable=missing-module-docstring, missing-function-docstring
from scripts.utils import (
    check_nova_raw_group,
    check_nova_transformed_group,
    check_pnn_groups,
    check_string_categories,
    map_letter_to_number,
    check_additives,
)
from scripts.product import (
    Product,
    Ingredients,
    NutritionFacts,
    Nutrients,
    NutriscoreData,
    NutrientLevel,
    NovaData,
)
from scripts.product import (
    EcoscoreData,
    OriginOfIngredients,
    Packaging,
    ProductionSystem,
)

WANTED_COUNTRY = "Canada"


def map_off_row_to_product(row: list[str], header: list[str]) -> Product | None:
    country_field = header.index("countries_en")
    if row[country_field] != WANTED_COUNTRY:
        return None

    id_field = header.index("code")
    product_name_field = header.index("product_name")
    #generic_name_field = header.index("generic_name")
    brand_owner_field = header.index("brands")
    food_groups_en_field = header.index("food_groups_en")
    allergens_en_field = header.index("allergens_en")

    return Product(
        id=row[id_field],
        product_name=row[product_name_field],
        is_raw=off_csv_is_raw_aliment(row, header),
        brand_name=row[brand_owner_field],
        food_groups_en=[row[food_groups_en_field]],
        ingredients=map_off_row_to_ingredients(row, header),
        nutrition_facts=map_off_row_to_nutrition_facts(row, header),
        allergens=[row[allergens_en_field]],
        nutriscore_data=map_off_row_to_nutriscore_data(row, header),
        ecoscore_data=map_off_row_to_ecoscore_data(row, header),
        nova_data=map_off_row_to_nova_data(row, header),
    )


def off_csv_is_raw_aliment(row: list[str], header: list[str]):
    """Checks if the aliment is raw based on its row values"""
    # Check the NOVA group
    nova_idx = header.index("nova_group")
    nova_group = row[nova_idx]
    try:
        if check_nova_raw_group(nova_group):
            return True
        if check_nova_transformed_group(nova_group):
            return False
    except ValueError:
        pass

    # Check the PNNS groups
    pnns_idx = header.index("pnns_groups_1")
    if check_pnn_groups(row[pnns_idx]):
        return True

    # Check the categories
    cat_idx = header.index("categories_tags")
    if check_string_categories(row[cat_idx]):
        return True

    # Check the additives
    additives_idx = header.index("additives_n")
    try:
        if check_additives(row[additives_idx], nova_group):
            return True
    except ValueError:
        pass

    return False


def map_off_row_to_ingredients(row: list[str], header: list[str]) -> Ingredients:
    ingredients_text_field = header.index("ingredients_text")

    return Ingredients(
        ingredients_list=[],
        ingredients_text=row[ingredients_text_field],
    )


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


def map_off_row_to_nutriscore_data(row: list[str], header: list[str]) -> NutriscoreData:
    nutriscore_score_field = header.index("nutriscore_grade")
    energy_field = header.index("energy_100g")
    fibers_field = header.index("fiber_100g")
    fruit_percentage_field = header.index("fruits-vegetables-nuts_100g")
    proteins_field = header.index("proteins_100g")
    saturated_fats_field = header.index("saturated-fat_100g")
    sodium_field = header.index("sodium_100g")
    sugar_field = header.index("sugars_100g")

    return NutriscoreData(
        score=(
            map_letter_to_number(row[nutriscore_score_field])
            if row[nutriscore_score_field]
            else None
        ),
        energy=row[energy_field],
        fibers=row[fibers_field],
        fruit_percentage=row[fruit_percentage_field],
        proteins=row[proteins_field],
        saturated_fats=row[saturated_fats_field],
        sodium=row[sodium_field],
        sugar=row[sugar_field],
        is_beverage=None,
    )


def map_off_row_to_ecoscore_data(row: list[str], header: list[str]) -> EcoscoreData:
    score_field = header.index("environmental_score_score")

    origin_of_ingredients: list[OriginOfIngredients] = [
        map_row_to_origin_of_ingredients(row, header)
    ]
    packaging = map_row_to_packaging(row, header)
    production_system = map_row_to_production_system(row, header)

    return EcoscoreData(
        score=int(row[score_field]) if row[score_field] else None,
        origin_of_ingredients=origin_of_ingredients,
        packaging=packaging,
        production_system=production_system,
        threatened_species={},
    )


def map_row_to_origin_of_ingredients(
    row: list[str], header: list[str]
) -> OriginOfIngredients:
    origin_field = header.index("origins")

    return OriginOfIngredients(
        origin=row[origin_field],
        percent=None,
        transportation_score=None,
    )


def map_row_to_packaging(row: list[str], header: list[str]) -> Packaging:
    packaging_field = header.index("packaging")

    return Packaging(
        non_recyclable_and_non_biodegradable_materials=None,
        packaging=row[packaging_field].split(","),
    )


def map_row_to_production_system(row: list[str], header: list[str]) -> ProductionSystem:
    labels_field = header.index("labels")

    return ProductionSystem(
        labels=row[labels_field].split(","),
        value=None,
        warning=None,
    )


def map_off_row_to_nova_data(row: list[str], header: list[str]) -> NovaData:
    score_field = header.index("nova_group")

    return NovaData(
        score=int(row[score_field]) if row[score_field] else None, group_markers={}
    )
