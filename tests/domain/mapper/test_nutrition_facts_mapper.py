import pytest
from decimal import Decimal

from domain.mapper.nutrition_facts_mapper import NutritionFactsMapper

from domain.product.complexFields.nutrient_level import NutrientLevel
from domain.product.complexFields.nutrients import Nutrients


@pytest.fixture
def nutrition_facts_mapper():
    return NutritionFactsMapper()


@pytest.fixture
def fdc_dict():
    fat_id = 1004
    saturated_fats_id = 1258
    sodium_id = 1093
    sugar_id = 2000
    carbohydrates_100g_id = 1005
    energy_kcal_100g_id = 1008
    vitamin_a_100g_id = 1104

    nutrient_values = {
        "fat": Decimal("45.2"),
        "saturated_fats": Decimal("63.78"),
        "sodium": Decimal("0.5"),
        "sugar": Decimal("45.14"),
        "carbohydrates": Decimal("423"),
        "energy_kcal": Decimal("10"),
        "vitamin_a": Decimal("120"),
    }

    food_nutrients = [
        {"nutrient": {"id": fat_id}, "amount": nutrient_values["fat"]},
        {
            "nutrient": {"id": saturated_fats_id},
            "amount": nutrient_values["saturated_fats"],
        },
        {"nutrient": {"id": sodium_id}, "amount": nutrient_values["sodium"]},
        {"nutrient": {"id": sugar_id}, "amount": nutrient_values["sugar"]},
        {
            "nutrient": {"id": carbohydrates_100g_id},
            "amount": nutrient_values["carbohydrates"],
        },
        {
            "nutrient": {"id": energy_kcal_100g_id},
            "amount": nutrient_values["energy_kcal"],
        },
        {"nutrient": {"id": vitamin_a_100g_id}, "amount": nutrient_values["vitamin_a"]},
    ]

    return food_nutrients, nutrient_values


@pytest.fixture
def off_rows():
    header = [
        "fat_100g",
        "salt_100g",
        "saturated-fat_100g",
        "sugars_100g",
        "carbohydrates_100g",
        "energy_100g",
        "energy-kcal_100g",
        "vitamin-a_100g",
    ]
    row = ["45.2", "2.2", "63.78", "45.14", "423", "15", "10", "120"]

    return row, header


@pytest.fixture
def off_dict():
    off_dict = {
        "nutriments": {
            "fat_100g": 45.2,
            "salt_100g": 2.2,
            "saturated-fat_100g": 63.78,
            "sugars_100g": 45.14,
            "carbohydrates_100g": 423,
            "energy_100g": 15,
            "energy-kcal_100g": 10,
            "vitamin-a_100g": 120,
        }
    }

    return off_dict


# ----------------------------------------------------------------
# Tests map_fdc_dict_to_nutrition_facts
# ----------------------------------------------------------------


def test_should_return_correct_nutrient_level_in_nutrition_facts_for_given_fdc_dict(
    nutrition_facts_mapper, fdc_dict
):
    food_nutrients, nutrient_values = fdc_dict

    result = nutrition_facts_mapper.map_fdc_dict_to_nutrition_facts(food_nutrients)

    expected_nutrient_level = NutrientLevel(
        fat=nutrient_values["fat"],
        salt=nutrient_values["sodium"] * Decimal("2.5"),
        saturated_fats=nutrient_values["saturated_fats"],
        sugar=nutrient_values["sugar"],
    )
    assert (
        result.nutrient_level == expected_nutrient_level
    ), f"Expected nutrient level to be {expected_nutrient_level}, got {result.nutrient_level}"


def test_should_return_correct_nutrients_in_nutrition_facts_for_given_fdc_dict(
    nutrition_facts_mapper, fdc_dict
):
    food_nutrients, nutrient_values = fdc_dict

    result = nutrition_facts_mapper.map_fdc_dict_to_nutrition_facts(food_nutrients)

    expected_nutrients = Nutrients(
        carbohydrates_100g=nutrient_values["carbohydrates"],
        energy_100g=nutrient_values["energy_kcal"] * Decimal(4.1868),
        energy_kcal_100g=nutrient_values["energy_kcal"],
        vitamin_a_100g=nutrient_values["vitamin_a"],
    )
    assert (
        result.nutrients == expected_nutrients
    ), f"Expected nutrient level to be {expected_nutrients}, got {result.nutrients}"


# ----------------------------------------------------------------
# Tests map_off_row_to_nutrition_facts
# ----------------------------------------------------------------


def test_should_return_correct_nutrient_level_in_nutrition_facts_for_given_off_row(
    nutrition_facts_mapper, off_rows
):
    row, header = off_rows

    result = nutrition_facts_mapper.map_off_row_to_nutrition_facts(row, header)

    expected_nutrient_level = NutrientLevel(
        fat=row[header.index("fat_100g")],
        salt=row[header.index("salt_100g")],
        saturated_fats=row[header.index("saturated-fat_100g")],
        sugar=row[header.index("sugars_100g")],
    )
    assert (
        result.nutrient_level == expected_nutrient_level
    ), f"Expected nutrient level to be {expected_nutrient_level}, got {result.nutrient_level}"


def test_should_return_correct_nutrients_in_nutrition_facts_for_given_off_row(
    nutrition_facts_mapper, off_rows
):
    row, header = off_rows

    result = nutrition_facts_mapper.map_off_row_to_nutrition_facts(row, header)

    expected_nutrients = Nutrients(
        carbohydrates_100g=row[header.index("carbohydrates_100g")],
        energy_100g=row[header.index("energy_100g")],
        energy_kcal_100g=row[header.index("energy-kcal_100g")],
        vitamin_a_100g=row[header.index("vitamin-a_100g")],
    )
    assert (
        result.nutrients == expected_nutrients
    ), f"Expected nutrient level to be {expected_nutrients}, got {result.nutrients}"


# ----------------------------------------------------------------
# Tests map_off_dict_to_nutrition_facts
# ----------------------------------------------------------------


def test_should_return_correct_nutrient_level_in_nutrition_facts_for_given_off_dict(
    nutrition_facts_mapper, off_dict
):
    result = nutrition_facts_mapper.map_off_dict_to_nutrition_facts(off_dict)

    expected_nutrient_level = NutrientLevel(
        fat=off_dict["nutriments"]["fat_100g"],
        salt=off_dict["nutriments"]["salt_100g"],
        saturated_fats=off_dict["nutriments"]["saturated-fat_100g"],
        sugar=off_dict["nutriments"]["sugars_100g"],
    )
    assert (
        result.nutrient_level == expected_nutrient_level
    ), f"Expected nutrient level to be {expected_nutrient_level}, got {result.nutrient_level}"


def test_should_return_correct_nutrients_in_nutrition_facts_for_given_off_dict(
    nutrition_facts_mapper, off_dict
):
    result = nutrition_facts_mapper.map_off_dict_to_nutrition_facts(off_dict)

    expected_nutrients = Nutrients(
        carbohydrates_100g=off_dict["nutriments"]["carbohydrates_100g"],
        energy_100g=off_dict["nutriments"]["energy_100g"],
        energy_kcal_100g=off_dict["nutriments"]["energy-kcal_100g"],
        vitamin_a_100g=off_dict["nutriments"]["vitamin-a_100g"],
    )
    assert (
        result.nutrients == expected_nutrients
    ), f"Expected nutrient level to be {expected_nutrients}, got {result.nutrients}"
