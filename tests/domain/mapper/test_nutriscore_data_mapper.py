from decimal import Decimal
from unittest.mock import MagicMock, patch

import pytest

from domain.mapper.number_mapper import NumberMapper
from domain.mapper.nutriscore_data_mapper import NutriscoreDataMapper
from domain.utils.converter import Converter

CONVERSION_ENERGY_KCAL_TO_KJ = Decimal(4.1868)


@pytest.fixture
def number_mapper():
    return MagicMock(spec=NumberMapper)


@pytest.fixture
def nutriscore_data_mapper(number_mapper):
    return NutriscoreDataMapper(number_mapper)


@pytest.fixture
def fdc_dict():
    ids = {
        "sodium_100g": 1093,
        "saturated_fats_100g": 1258,
        "sugar_100g": 2000,
        "fibers_100g": 1079,
        "energy_kcal_100g": 1008,
        "proteins_100g": 1003,
    }

    nutrient_values = {
        "energy_kcal_100g": 45.2,
        "fibers_100g": 54,
        "proteins_100g": 20,
        "saturated_fats_100g": 63.78,
        "sodium_100g": 0.5,
        "sugar_100g": 45.14,
    }

    food_nutrients = [
        {
            "nutrient": {"id": ids["saturated_fats_100g"], "unitName": "g"},
            "amount": nutrient_values["saturated_fats_100g"],
        },
        {
            "nutrient": {"id": ids["sugar_100g"], "unitName": "g"},
            "amount": nutrient_values["sugar_100g"],
        },
        {
            "nutrient": {"id": ids["fibers_100g"], "unitName": "g"},
            "amount": nutrient_values["fibers_100g"],
        },
        {
            "nutrient": {"id": ids["energy_kcal_100g"], "unitName": "g"},
            "amount": nutrient_values["energy_kcal_100g"],
        },
        {
            "nutrient": {"id": ids["sodium_100g"], "unitName": "g"},
            "amount": nutrient_values["sodium_100g"],
        },
        {
            "nutrient": {"id": ids["proteins_100g"], "unitName": "g"},
            "amount": nutrient_values["proteins_100g"],
        },
    ]

    return food_nutrients, nutrient_values


@pytest.fixture
def off_valid_rows():
    header = [
        "nutriscore_grade",
        "energy_100g",
        "fiber_100g",
        "fruits-vegetables-nuts_100g",
        "proteins_100g",
        "saturated-fat_100g",
        "sodium_100g",
        "sugars_100g",
    ]
    row = ["a", "45.2", "54", "75", "20", "63.78", "0.5", "45.14"]

    return row, header


@pytest.fixture
def off_invalid_rows():
    header = [
        "nutriscore_grade",
        "energy_100g",
        "fiber_100g",
        "fruits-vegetables-nuts_100g",
        "proteins_100g",
        "saturated-fat_100g",
        "sodium_100g",
        "sugars_100g",
    ]
    row = ["", "", "", "seventy", "", "", "", ""]

    return row, header


@pytest.fixture
def off_valid_dict():
    off_dict = {
        "nutriscore_grade": "a",
        "nutriments": {
            "energy_100g": 45.2,
            "fiber_100g": 54,
            "fruits-vegetables-nuts_100g": 75,
            "proteins_100g": 20,
            "saturated-fat_100g": 63.78,
            "sodium_100g": 0.5,
            "sugars_100g": 45.14,
        },
    }

    return off_dict


@pytest.fixture
def off_invalid_dict():
    off_dict = {
        "nutriscore_grade": None,
        "nutriments": {
            "energy_100g": None,
            "fiber_100g": "other",
            "fruits-vegetables-nuts_100g": "75g",
            "proteins_100g": None,
            "saturated-fat_100g": None,
            "sodium_100g": None,
            "sugars_100g": None,
        },
    }

    return off_dict


# ----------------------------------------------------------------
# Tests map_fdc_dict_to_nutriscore_data
# ----------------------------------------------------------------


def test_should_return_empty_score_in_nutriscore_data_for_given_fdc_dict(
    nutriscore_data_mapper,
):
    food_nutrients = []

    result = nutriscore_data_mapper.map_fdc_dict_to_nutriscore_data(food_nutrients)

    assert result.score is None, f"Expected nutriscore to be {None}, got {result.score}"


def test_should_assign_given_nutrient_values_in_nutriscore_data_for_given_fdc_dict(
    nutriscore_data_mapper, fdc_dict
):
    food_nutrients, nutrient_values = fdc_dict

    result = nutriscore_data_mapper.map_fdc_dict_to_nutriscore_data(food_nutrients)

    assert result.energy_100g == nutrient_values["energy_kcal_100g"] * float(
        CONVERSION_ENERGY_KCAL_TO_KJ
    ), f"Expected energy value to be {nutrient_values["energy_100g"]}, got {result.energy_100g}"
    assert (
        result.fibers_100g == nutrient_values["fibers_100g"]
    ), f"Expected fibers value to be {nutrient_values["fibers_100g"]}, got {result.fibers_100g}"
    assert (
        result.proteins_100g == nutrient_values["proteins_100g"]
    ), f"Expected proteins value to be {nutrient_values["proteins_100g"]}, got {result.proteins_100g}"
    assert (
        result.saturated_fats_100g == nutrient_values["saturated_fats_100g"]
    ), f"Expected saturated fats value to be {nutrient_values["saturated_fats_100g"]}, got {result.saturated_fats_100g}"
    assert (
        result.sodium_100g == nutrient_values["sodium_100g"]
    ), f"Expected sodium value to be {nutrient_values["sodium_100g"]}, got {result.sodium_100g}"
    assert (
        result.sugar_100g == nutrient_values["sugar_100g"]
    ), f"Expected sugar value to be {nutrient_values["sugar_100g"]}, got {result.sugar_100g}"


def test_should_return_empty_fruit_percentage_in_nutriscore_data_for_given_fdc_dict(
    nutriscore_data_mapper, fdc_dict
):
    food_nutrients, nutrient_values = fdc_dict

    result = nutriscore_data_mapper.map_fdc_dict_to_nutriscore_data(food_nutrients)

    assert (
        result.fruit_percentage is None
    ), f"Expected fruit percentage to be {None}, got {result.fruit_percentage}"


def test_should_return_empty_is_beverage_field_in_nutriscore_data_for_given_fdc_dict(
    nutriscore_data_mapper, fdc_dict
):
    food_nutrients, nutrient_values = fdc_dict

    result = nutriscore_data_mapper.map_fdc_dict_to_nutriscore_data(food_nutrients)

    assert (
        result.is_beverage is None
    ), f"Expected is beverage field to be {None}, got {result.is_beverage}"


# ----------------------------------------------------------------
# Tests map_off_row_to_nutriscore_data
# ----------------------------------------------------------------


def test_should_return_score_from_number_mapper_for_given_score_in_nutriscore_data_for_given_off_row(
    nutriscore_data_mapper, off_valid_rows
):
    row, header = off_valid_rows
    nutriscore_data_mapper.number_mapper.map_letter_to_number.return_value = 1
    result = nutriscore_data_mapper.map_off_row_to_nutriscore_data(row, header)

    assert result.score == 1, f"Expected nutriscore to be {1}, got {result.score}"


def test_should_return_empty_score_for_absent_score_in_nutriscore_data_for_given_off_row(
    nutriscore_data_mapper, off_invalid_rows
):
    row, header = off_invalid_rows
    nutriscore_data_mapper.number_mapper.map_letter_to_number.return_value = 1
    result = nutriscore_data_mapper.map_off_row_to_nutriscore_data(row, header)

    assert result.score is None, f"Expected nutriscore to be {None}, got {result.score}"


def test_should_assign_given_valid_nutrient_values_in_nutriscore_data_for_given_off_row(
    nutriscore_data_mapper, off_valid_rows
):
    row, header = off_valid_rows
    return_float_converter_value = 10.3

    with patch.object(
        Converter, "safe_float", return_value=return_float_converter_value
    ):
        result = nutriscore_data_mapper.map_off_row_to_nutriscore_data(row, header)

    assert (
        result.energy_100g == return_float_converter_value
    ), f"Expected energy value to be {row[header.index("energy_100g")]}, got {result.energy_100g}"
    assert result.fibers_100g == float(
        row[header.index("fiber_100g")]
    ), f"Expected energy value to be {row[header.index("fiber_100g")]}, got {result.fibers_100g}"
    assert (
        result.fruit_percentage == return_float_converter_value
    ), f"Expected energy value to be {row[header.index("fruits-vegetables-nuts_100g")]}, got {result.fruit_percentage}"
    assert result.proteins_100g == float(
        row[header.index("proteins_100g")]
    ), f"Expected energy value to be {row[header.index("proteins_100g")]}, got {result.proteins_100g}"
    assert (
        result.saturated_fats_100g == return_float_converter_value
    ), f"Expected energy value to be {row[header.index("saturated-fat_100g")]}, got {result.saturated_fats_100g}"
    assert result.sodium_100g == float(
        row[header.index("sodium_100g")]
    ), f"Expected energy value to be {row[header.index("sodium_100g")]}, got {result.sodium_100g}"
    assert result.sugar_100g == float(
        row[header.index("sugars_100g")]
    ), f"Expected energy value to be {row[header.index("sugars_100g")]}, got {result.sugar_100g}"


def test_should_return_empty_nutrient_values_for_invalid_values_in_nutriscore_data_for_given_off_row(
    nutriscore_data_mapper, off_invalid_rows
):
    row, header = off_invalid_rows

    result = nutriscore_data_mapper.map_off_row_to_nutriscore_data(row, header)

    assert (
        result.energy_100g is None
    ), f"Expected energy value to be {None}, got {result.energy_100g}"
    assert (
        result.fibers_100g is None
    ), f"Expected energy value to be {None}, got {result.fibers_100g}"
    assert (
        result.fruit_percentage is None
    ), f"Expected energy value to be {None}, got {result.fruit_percentage}"
    assert (
        result.proteins_100g is None
    ), f"Expected energy value to be {None}, got {result.proteins_100g}"
    assert (
        result.saturated_fats_100g is None
    ), f"Expected energy value to be {None}, got {result.saturated_fats_100g}"
    assert (
        result.sodium_100g is None
    ), f"Expected energy value to be {None}, got {result.sodium_100g}"
    assert (
        result.sugar_100g is None
    ), f"Expected energy value to be {None}, got {result.suga_100gr}"


def test_should_return_empty_is_beverage_field_in_nutriscore_data_for_given_off_row(
    nutriscore_data_mapper, off_valid_rows
):
    row, header = off_valid_rows

    result = nutriscore_data_mapper.map_off_row_to_nutriscore_data(row, header)

    assert (
        result.is_beverage is None
    ), f"Expected is beverage field to be {None}, got {result.is_beverage}"


# ----------------------------------------------------------------
# Tests map_off_dict_to_nutriscore_data
# ----------------------------------------------------------------


def test_should_return_score_from_number_mapper_for_given_score_in_nutriscore_data_for_given_off_dict(
    nutriscore_data_mapper, off_valid_dict
):
    nutriscore_data_mapper.number_mapper.map_letter_to_number.return_value = 1

    result = nutriscore_data_mapper.map_off_dict_to_nutriscore_data(off_valid_dict)

    assert result.score == 1, f"Expected nutriscore to be {1}, got {result.score}"


def test_should_return_empty_score_for_absent_score_in_nutriscore_data_for_given_off_dict(
    nutriscore_data_mapper, off_invalid_dict
):
    nutriscore_data_mapper.number_mapper.map_letter_to_number.return_value = 1

    result = nutriscore_data_mapper.map_off_dict_to_nutriscore_data(off_invalid_dict)

    assert result.score is None, f"Expected nutriscore to be {None}, got {result.score}"


def test_should_assign_given_valid_nutrient_values_in_nutriscore_data_for_given_off_dict(
    nutriscore_data_mapper, off_valid_dict
):
    return_float_converter_value = 10.3

    with patch.object(
        Converter, "safe_float", return_value=return_float_converter_value
    ):
        result = nutriscore_data_mapper.map_off_dict_to_nutriscore_data(off_valid_dict)

    assert (
        result.energy_100g == off_valid_dict["nutriments"]["energy_100g"]
    ), f"Expected energy value to be {off_valid_dict["nutriments"]["energy_100g"]}, got {result.energy_100g}"
    assert (
        result.fibers_100g == return_float_converter_value
    ), f"Expected energy value to be {off_valid_dict["nutriments"]["fiber_100g"]}, got {result.fibers_100g}"
    assert (
        result.fruit_percentage == return_float_converter_value
    ), f"Expected energy value to be {off_valid_dict["nutriments"]["fruits-vegetables-nuts_100g"]}, got {result.fruit_percentage}"
    assert (
        result.proteins_100g == off_valid_dict["nutriments"]["proteins_100g"]
    ), f"Expected energy value to be {off_valid_dict["nutriments"]["proteins_100g"]}, got {result.proteins_100g}"
    assert (
        result.saturated_fats_100g == off_valid_dict["nutriments"]["saturated-fat_100g"]
    ), f"Expected energy value to be {off_valid_dict["nutriments"]["saturated-fat_100g"]}, got {result.saturated_fats_100g}"
    assert (
        result.sodium_100g == off_valid_dict["nutriments"]["sodium_100g"]
    ), f"Expected energy value to be {off_valid_dict["nutriments"]["sodium_100g"]}, got {result.sodium_100g}"
    assert (
        result.sugar_100g == off_valid_dict["nutriments"]["sugars_100g"]
    ), f"Expected energy value to be {off_valid_dict["nutriments"]["sugars_100g"]}, got {result.sugar_100g}"


def test_should_return_empty_nutrient_values_for_invalid_values_in_nutriscore_data_for_given_off_dict(
    nutriscore_data_mapper, off_invalid_dict
):
    result = nutriscore_data_mapper.map_off_dict_to_nutriscore_data(off_invalid_dict)

    assert (
        result.energy_100g is None
    ), f"Expected energy value to be {None}, got {result.energy_100g}"
    assert (
        result.fibers_100g is None
    ), f"Expected energy value to be {None}, got {result.fibers_100g}"
    assert (
        result.fruit_percentage is None
    ), f"Expected energy value to be {None}, got {result.fruit_percentage}"
    assert (
        result.proteins_100g is None
    ), f"Expected energy value to be {None}, got {result.proteins_100g}"
    assert (
        result.saturated_fats_100g is None
    ), f"Expected energy value to be {None}, got {result.saturated_fats_100g}"
    assert (
        result.sodium_100g is None
    ), f"Expected energy value to be {None}, got {result.sodium_100g}"
    assert (
        result.sugar_100g is None
    ), f"Expected energy value to be {None}, got {result.sugar_100g}"


def test_should_return_empty_is_beverage_field_in_nutriscore_data_for_given_off_dict(
    nutriscore_data_mapper, off_valid_dict
):
    result = nutriscore_data_mapper.map_off_dict_to_nutriscore_data(off_valid_dict)

    assert (
        result.is_beverage is None
    ), f"Expected is beverage field to be {None}, got {result.is_beverage}"
