import pytest

from domain.mapper.nutrient_amount_mapper import NutrientAmountMapper


@pytest.fixture
def nutrient_amount_mapper():
    nutrient_amount_mapper = NutrientAmountMapper()
    return nutrient_amount_mapper


def test_should_return_given_value_given_nutrient_not_to_convert(
    nutrient_amount_mapper,
):
    nutrient_value = 45
    nutrient_unit = "g"

    result = nutrient_amount_mapper.map_nutrient(nutrient_value, nutrient_unit)

    assert result == nutrient_value


def test_should_return_correctly_converted_value_given_nutrient_to_convert_and_possible_to_convert_unit(
    nutrient_amount_mapper,
):
    nutrient_value = 45
    nutrient_unit = "mg"

    result = nutrient_amount_mapper.map_nutrient(nutrient_value, nutrient_unit)

    assert result == nutrient_value / 1000


def test_should_return_nothing_given_nutrient_to_convert_and_impossible_to_convert_unit(
    nutrient_amount_mapper,
):
    nutrient_value = 45
    nutrient_unit = "other"

    result = nutrient_amount_mapper.map_nutrient(nutrient_value, nutrient_unit)

    assert result is None
