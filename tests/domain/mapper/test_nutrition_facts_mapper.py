from unittest.mock import patch

import pytest

from domain.mapper.nutrient_amount_mapper import NutrientAmountMapper
from domain.mapper.nutrition_facts_mapper import NutritionFactsMapper
from domain.product.complexFields.nutrition_facts import NutritionFacts
from domain.product.complexFields.nutritionFactsPerHundredGrams import (
    NutritionFactsPerHundredGrams,
)
from domain.product.complexFields.nutritionFactsPerServing import (
    NutritionFactsPerServing,
)


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

    fdc_dict_100g = [
        {"nutrient": {"id": ids["fat"], "unitName": "g"}, "amount": 10},
        {"nutrient": {"id": ids["saturated_fats"], "unitName": "g"}, "amount": 20},
        {"nutrient": {"id": ids["sugar"], "unitName": "g"}, "amount": 30.5},
        {"nutrient": {"id": ids["carbohydrates"], "unitName": "g"}, "amount": 40},
        {"nutrient": {"id": ids["energy_kcal"], "unitName": "g"}, "amount": 50},
        {"nutrient": {"id": ids["sodium"], "unitName": "g"}, "amount": 62},
    ]

    fdc_dict_serving = {
        "fat": {"value": 14.0},
        "sodium": {"value": 50},
        "cholesterol": {"value": 6.7},
        "fiber": {"value": 0.04},
    }

    return ids, fdc_dict_100g, fdc_dict_serving


@pytest.fixture
def off_dict():
    off_dict = {
        "nutriments": {
            "fat_100g": 45.2,
            "salt_100g": 2.2,
            "saturated-fat_100g": 63.78,
            "sugars_100g": 45.14,
            "carbohydrates_100g": 423,
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
    _, fdc_dict_100g, fdc_dict_serving = fdc_dict
    product_preparation_state_code = "PREPARED"

    with patch.object(NutrientAmountMapper, "map_nutrient", return_value=25):
        result = nutrition_facts_mapper.map_fdc_dict_to_nutrition_facts(
            fdc_dict_100g, fdc_dict_serving, product_preparation_state_code
        )

    assert result.nutrition_facts_per_hundred_grams.sugar_100g == 25
    assert result.nutrition_facts_per_hundred_grams.saturated_fats_100g == 25
    assert result.nutrition_facts_per_hundred_grams.fat_100g == 25
    assert result.nutrition_facts_per_hundred_grams.salt_100g == 25
    assert result.nutrition_facts_per_hundred_grams.carbohydrates_100g == 25
    assert result.nutrition_facts_per_hundred_grams.vitamin_a_100g == 25

    assert result.nutrition_facts_per_serving.fat_serving == 25
    assert result.nutrition_facts_per_serving.sodium_serving == 25
    assert result.nutrition_facts_per_serving.cholesterol_serving == 25
    assert result.nutrition_facts_per_serving.fibers_serving == 25


def test_should_return_correct_energy_values_for_nutrients_in_nutrition_facts_for_fdc_dict(
    nutrition_facts_mapper, fdc_dict
):
    fdc_ids, fdc_dict_100g, fdc_dict_serving = fdc_dict
    product_preparation_state_code = "PREPARED"

    result = nutrition_facts_mapper.map_fdc_dict_to_nutrition_facts(
        fdc_dict_100g, fdc_dict_serving, product_preparation_state_code
    )

    expected_energy_kcal_100g = next(
        item["amount"]
        for item in fdc_dict_100g
        if item["nutrient"]["id"] == fdc_ids["energy_kcal"]
    )
    assert (
        result.nutrition_facts_per_hundred_grams.energy_kcal_100g
        == expected_energy_kcal_100g
    )


def test_should_return_true_is_for_prepared_food_field_for_prepared_state_code_in_nutrition_facts_per_serving_for_fdc_dict(
    nutrition_facts_mapper, fdc_dict
):
    fdc_ids, fdc_dict_100g, fdc_dict_serving = fdc_dict
    product_preparation_state_code = "PREPARED"

    result = nutrition_facts_mapper.map_fdc_dict_to_nutrition_facts(
        fdc_dict_100g, fdc_dict_serving, product_preparation_state_code
    )

    assert result.nutrition_facts_per_serving.is_for_prepared_food


def test_should_return_false_is_for_prepared_food_field_for_unprepared_state_code_in_nutrition_facts_per_serving_for_fdc_dict(
    nutrition_facts_mapper, fdc_dict
):
    fdc_ids, fdc_dict_100g, fdc_dict_serving = fdc_dict
    product_preparation_state_code = "UNPREPARED"

    result = nutrition_facts_mapper.map_fdc_dict_to_nutrition_facts(
        fdc_dict_100g, fdc_dict_serving, product_preparation_state_code
    )

    assert not result.nutrition_facts_per_serving.is_for_prepared_food


def test_should_return_empty_is_for_prepared_food_field_for_other_state_code_in_nutrition_facts_per_serving_for_fdc_dict(
    nutrition_facts_mapper, fdc_dict
):
    fdc_ids, fdc_dict_100g, fdc_dict_serving = fdc_dict
    product_preparation_state_code = "NO INFORMATION"

    result = nutrition_facts_mapper.map_fdc_dict_to_nutrition_facts(
        fdc_dict_100g, fdc_dict_serving, product_preparation_state_code
    )

    assert result.nutrition_facts_per_serving.is_for_prepared_food is None


# ----------------------------------------------------------------
# Tests map_off_dict_to_nutrition_facts
# ----------------------------------------------------------------


def test_should_return_correct_nutrition_facts_for_given_off_dict(
    nutrition_facts_mapper, off_dict
):
    result = nutrition_facts_mapper.map_off_dict_to_nutrition_facts(off_dict)

    expected_nutrition_facts = NutritionFacts(
        nutrition_facts_per_hundred_grams=NutritionFactsPerHundredGrams(
            fat_100g=float(off_dict["nutriments"].get("fat_100g")),
            salt_100g=float(off_dict["nutriments"].get("salt_100g")),
            saturated_fats_100g=float(off_dict["nutriments"].get("saturated-fat_100g")),
            sugar_100g=float(off_dict["nutriments"].get("sugars_100g")),
            carbohydrates_100g=float(off_dict["nutriments"].get("carbohydrates_100g")),
            energy_kcal_100g=float(off_dict["nutriments"].get("energy-kcal_100g")),
            vitamin_a_100g=float(off_dict["nutriments"].get("vitamin-a_100g")),
        ),
        nutrition_facts_per_serving=NutritionFactsPerServing(),
    )

    assert (
        result == expected_nutrition_facts
    ), f"Expected {expected_nutrition_facts}, got {result}"
