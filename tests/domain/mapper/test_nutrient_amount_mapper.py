from decimal import Decimal

import pytest

from domain.mapper.nutrient_mapper import NutrientMapper


@pytest.fixture
def nutrient_mapper():
    nutrient_mapper = NutrientMapper()
    return nutrient_mapper


def test_should_return_nothing_when_value_cannot_be_converted_given_nutrient_to_convert(nutrient_mapper):
    nutrient_name = "sugar"
    nutrient_value = 45
    nutrient_unit = "other"

    result = nutrient_mapper.map_nutrient(nutrient_name, nutrient_value, nutrient_unit)

    assert result is None


def test_should_return_given_value_given_nutrient_not_to_convert(nutrient_mapper):
    nutrient_name = "other"
    nutrient_value = 45
    nutrient_unit = "g"

    result = nutrient_mapper.map_nutrient(nutrient_name, nutrient_value, nutrient_unit)

    assert result == nutrient_value


def test_should_return_given_value_given_nutrient_to_convert_and_correct_unit(nutrient_mapper):
    nutrient_name = "sugar"
    nutrient_value = 45
    nutrient_unit = "g"

    result = nutrient_mapper.map_nutrient(nutrient_name, nutrient_value, nutrient_unit)

    assert result == nutrient_value


def test_should_return_correctly_converted_value_given_nutrient_to_convert_in_g_and_incorrect_unit(nutrient_mapper):
    nutrient_name = "sugar"
    nutrient_value = 45
    nutrient_unit = "mg"

    result = nutrient_mapper.map_nutrient(nutrient_name, nutrient_value, nutrient_unit)

    assert result == nutrient_value / 1000


def test_should_return_correctly_converted_value_given_nutrient_to_convert_in_mcg_and_incorrect_unit(nutrient_mapper):
    nutrient_name = "sugar"
    nutrient_value = 45
    nutrient_unit = "iu"

    result = nutrient_mapper.map_nutrient(nutrient_name, nutrient_value, nutrient_unit)

    assert result == nutrient_value / Decimal("3.33")
