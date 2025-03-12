from decimal import Decimal
from unittest.mock import patch

import pytest

from domain.mapper.nutrient_amount_mapper import NutrientAmountMapper
from domain.mapper.nutrition_facts_mapper import NutritionFactsMapper


@pytest.fixture
def nutrition_facts_mapper():
    nutrition_facts_mapper = NutritionFactsMapper()
    return nutrition_facts_mapper


@pytest.fixture
def given_fdc_dict():
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


def test_should_return_mapped_nutrient_level_values_in_nutrition_facts_for_fdc_dict(
    nutrition_facts_mapper, given_fdc_dict
):
    _, fdc_dict = given_fdc_dict

    with patch.object(NutrientAmountMapper, "map_nutrient", return_value=25):
        result = nutrition_facts_mapper.map_fdc_dict_to_nutrition_facts(fdc_dict)

    assert result.nutrient_level.sugar == 25
    assert result.nutrient_level.saturated_fats == 25
    assert result.nutrient_level.fat == 25
    assert result.nutrient_level.salt == 25


def test_should_return_mapped_nutrients_in_nutrition_facts_for_fdc_dict(
    nutrition_facts_mapper, given_fdc_dict
):
    _, fdc_dict = given_fdc_dict

    with patch.object(NutrientAmountMapper, "map_nutrient", return_value=10.2):
        result = nutrition_facts_mapper.map_fdc_dict_to_nutrition_facts(fdc_dict)

    assert result.nutrients.carbohydrates_100g == 10.2
    assert result.nutrients.vitamin_a_100g == 10.2


def test_should_return_correct_energy_values_for_nutrients_in_nutrition_facts_for_fdc_dict(
    nutrition_facts_mapper, given_fdc_dict
):
    fdc_ids, fdc_dict = given_fdc_dict

    with patch.object(NutrientAmountMapper, "map_nutrient", return_value=10.2):
        result = nutrition_facts_mapper.map_fdc_dict_to_nutrition_facts(fdc_dict)

    expected_energy_kcal_100g = next(
        item["amount"]
        for item in fdc_dict
        if item["nutrient"]["id"] == fdc_ids["energy_kcal"]
    )
    assert result.nutrients.energy_100g == float(
        expected_energy_kcal_100g * Decimal(4.1868)
    )
    assert result.nutrients.energy_kcal_100g == expected_energy_kcal_100g
