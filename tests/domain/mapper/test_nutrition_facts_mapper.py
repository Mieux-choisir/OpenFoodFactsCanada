from unittest.mock import patch

import pytest
from decimal import Decimal

from domain.mapper.nutrient_amount_mapper import NutrientAmountMapper
from domain.mapper.nutrition_facts_mapper import NutritionFactsMapper

from domain.product.complexFields.nutrient_level import NutrientLevel
from domain.product.complexFields.nutrients import Nutrients

CONVERSION_ENERGY_KCAL_TO_KJ = Decimal(4.1868)


@pytest.fixture
def nutrition_facts_mapper():
    return NutritionFactsMapper()


@pytest.fixture
def fdc_dict():
    ids = {
        "fat": 1004,
        "sodium": 1093,
        "saturated_fats": 1258,
        "sugar": 2000,
        "carbohydrates": 1005,
        "energy_kcal": 1008,
        "vitamin_a": 1104,
    }

    fdc_dict = [
        {"nutrient": {"id": ids["fat"], "unitName": "g"}, "amount": 10},
        {"nutrient": {"id": ids["saturated_fats"], "unitName": "g"}, "amount": 20},
        {"nutrient": {"id": ids["sugar"], "unitName": "g"}, "amount": 30.5},
        {"nutrient": {"id": ids["carbohydrates"], "unitName": "g"}, "amount": 40},
        {"nutrient": {"id": ids["energy_kcal"], "unitName": "g"}, "amount": 50},
        {"nutrient": {"id": ids["sodium"], "unitName": "g"}, "amount": 62},
    ]

    return ids, fdc_dict


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


def test_should_return_mapped_nutrient_level_values_in_nutrition_facts_for_fdc_dict(
    nutrition_facts_mapper, fdc_dict
):
    _, fdc_dict = fdc_dict

    with patch.object(NutrientAmountMapper, "map_nutrient", return_value=25):
        result = nutrition_facts_mapper.map_fdc_dict_to_nutrition_facts(fdc_dict)

    assert result.nutrient_level.sugar == 25
    assert result.nutrient_level.saturated_fats == 25
    assert result.nutrient_level.fat == 25
    assert result.nutrient_level.salt == 25


def test_should_return_mapped_nutrients_in_nutrition_facts_for_fdc_dict(
    nutrition_facts_mapper, fdc_dict
):
    _, fdc_dict = fdc_dict

    with patch.object(NutrientAmountMapper, "map_nutrient", return_value=10.2):
        result = nutrition_facts_mapper.map_fdc_dict_to_nutrition_facts(fdc_dict)

    assert result.nutrients.carbohydrates_100g == 10.2
    assert result.nutrients.vitamin_a_100g == 10.2


def test_should_return_correct_energy_values_for_nutrients_in_nutrition_facts_for_fdc_dict(
    nutrition_facts_mapper, fdc_dict
):
    fdc_ids, fdc_dict = fdc_dict

    with patch.object(NutrientAmountMapper, "map_nutrient", return_value=10.2):
        result = nutrition_facts_mapper.map_fdc_dict_to_nutrition_facts(fdc_dict)

    expected_energy_kcal_100g = next(
        item["amount"]
        for item in fdc_dict
        if item["nutrient"]["id"] == fdc_ids["energy_kcal"]
    )
    assert result.nutrients.energy_100g == float(
        expected_energy_kcal_100g * CONVERSION_ENERGY_KCAL_TO_KJ
    )
    assert result.nutrients.energy_kcal_100g == expected_energy_kcal_100g


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
