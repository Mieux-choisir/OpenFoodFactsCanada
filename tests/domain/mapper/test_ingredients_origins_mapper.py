import pytest

from domain.mapper.ingredients_origins_mapper import IngredientsOriginMapper


@pytest.fixture
def ingredients_origin_mapper():
    return IngredientsOriginMapper()


# ----------------------------------------------------------------
# Tests map_off_row_to_ingredients_origin
# ----------------------------------------------------------------


def test_should_return_split_origins_in_ingredients_origins_for_given_off_row(
    ingredients_origin_mapper,
):
    row = ["Canada, United States"]
    header = ["origins"]

    result = ingredients_origin_mapper.map_off_row_to_ingredients_origin(row, header)

    assert result.origins == row[0].split(
        ","
    ), f"Expected origins of {row[0].split(',')}, got {result.origins}"


def test_should_return_empty_percent_in_ingredients_origins_for_given_off_row(
    ingredients_origin_mapper,
):
    row = ["Canada, United States"]
    header = ["origins"]

    result = ingredients_origin_mapper.map_off_row_to_ingredients_origin(row, header)

    assert result.percent is None, f"Expected percent of {None}, got {result.percent}"


def test_should_return_empty_transportation_score_in_ingredients_origins_for_given_off_row(
    ingredients_origin_mapper,
):
    row = ["Canada, United States"]
    header = ["origins"]

    result = ingredients_origin_mapper.map_off_row_to_ingredients_origin(row, header)

    assert (
        result.transportation_score is None
    ), f"Expected transportation score of {None}, got {result.transportation_score}"


# ----------------------------------------------------------------
# Tests map_off_dict_to_ingredients_origin
# ----------------------------------------------------------------


def test_should_return_given_origins_in_ingredients_origins_for_given_off_dict(
    ingredients_origin_mapper,
):
    off_dict = {"origins": ["Canada, United States"]}

    result = ingredients_origin_mapper.map_off_dict_to_ingredients_origin(off_dict)

    assert (
        result.origins == off_dict["origins"]
    ), f"Expected origins of {off_dict["origins"]}, got {result.origins}"


def test_should_return_empty_percent_in_ingredients_origins_for_given_off_dict(
    ingredients_origin_mapper,
):
    off_dict = {"origins": ["Canada, United States"]}

    result = ingredients_origin_mapper.map_off_dict_to_ingredients_origin(off_dict)

    assert result.percent is None, f"Expected percent of {None}, got {result.percent}"


def test_should_return_empty_transportation_score_in_ingredients_origins_for_given_off_dict(
    ingredients_origin_mapper,
):
    off_dict = {"origins": ["Canada, United States"]}

    result = ingredients_origin_mapper.map_off_dict_to_ingredients_origin(off_dict)

    assert (
        result.transportation_score is None
    ), f"Expected transportation score of {None}, got {result.transportation_score}"
