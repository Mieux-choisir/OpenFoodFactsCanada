import pytest
from unittest.mock import MagicMock
from domain.mapper.ingredients_mapper import IngredientsMapper
from domain.utils.ingredient_normalizer import IngredientNormalizer


@pytest.fixture
def ingredient_normalizer():
    return MagicMock(spec=IngredientNormalizer)


@pytest.fixture
def ingredients_mapper(ingredient_normalizer):
    return IngredientsMapper(ingredient_normalizer)


# ----------------------------------------------------------------
# Tests map_fdc_dict_to_ingredients
# ----------------------------------------------------------------


def test_should_return_ingredients_text_in_title_format_in_ingredients_for_given_fdc_dict(
    ingredients_mapper,
):
    ingredients = "FLOUR, SUGAR, PEANUTS."

    result = ingredients_mapper.map_fdc_dict_to_ingredients(ingredients)

    assert (
        result.ingredients_text == ingredients.title()
    ), f"Expected ingredients text of {ingredients.title}, got {result.ingredients_text}"


def test_should_return_ingredients_list_from_ingredients_normalizer_in_ingredients_for_given_fdc_dict(
    ingredients_mapper,
):
    ingredients = "FLOUR, SUGAR, PEANUTS."
    ingredients_list = ["Flour", "sugar", "Peanuts"]
    ingredients_mapper.ingredient_normalizer.normalise_ingredients_list.return_value = (
        ingredients_list
    )

    result = ingredients_mapper.map_fdc_dict_to_ingredients(ingredients)

    assert (
        result.ingredients_list == ingredients_list
    ), f"Expected ingredients list of {ingredients_list}, got {result.ingredients_list}"


def test_should_correctly_call_ingredients_normalizer_for_given_fdc_dict(
    ingredients_mapper,
):
    ingredients = "FLOUR, SUGAR, PEANUTS."

    ingredients_mapper.map_fdc_dict_to_ingredients(ingredients)

    ingredients_mapper.ingredient_normalizer.normalise_ingredients_list.assert_called_with(
        ingredients
    )


# ----------------------------------------------------------------
# Tests map_off_row_to_ingredients
# ----------------------------------------------------------------


def test_should_return_ingredients_text_in_title_format_in_ingredients_for_given_off_row(
    ingredients_mapper,
):
    row = ["FLOUR, SUGAR, PEANUTS."]
    header = ["ingredients_text"]

    result = ingredients_mapper.map_off_row_to_ingredients(row, header)

    assert (
        result.ingredients_text == row[0].title()
    ), f"Expected ingredients text of {row[0].title()}, got {result.ingredients_text}"


def test_should_return_ingredients_list_from_ingredients_normalizer_in_ingredients_for_given_off_row(
    ingredients_mapper,
):
    row = ["FLOUR, SUGAR, PEANUTS."]
    header = ["ingredients_text"]
    ingredients_list = ["Flour", "sugar", "Peanuts"]
    ingredients_mapper.ingredient_normalizer.normalise_ingredients_list.return_value = (
        ingredients_list
    )

    result = ingredients_mapper.map_off_row_to_ingredients(row, header)

    assert (
        result.ingredients_list == ingredients_list
    ), f"Expected ingredients list of {ingredients_list}, got {result.ingredients_list}"


def test_should_correctly_call_ingredients_normalizer_for_given_off_row(
    ingredients_mapper,
):
    row = ["FLOUR, SUGAR, PEANUTS."]
    header = ["ingredients_text"]

    ingredients_mapper.map_off_row_to_ingredients(row, header)

    ingredients_mapper.ingredient_normalizer.normalise_ingredients_list.assert_called_with(
        row[0]
    )


# ----------------------------------------------------------------
# Tests map_off_dict_to_ingredients
# ----------------------------------------------------------------


def test_should_return_ingredients_text_in_title_format_in_ingredients_for_given_off_dict(
    ingredients_mapper,
):
    off_dict = {"ingredients_text": "FLOUR, SUGAR, PEANUTS."}

    result = ingredients_mapper.map_off_dict_to_ingredients(off_dict)

    assert (
        result.ingredients_text == off_dict["ingredients_text"].title()
    ), f"Expected ingredients text of {off_dict["ingredients_text"].title()}, got {result.ingredients_text}"


def test_should_return_ingredients_list_from_ingredients_normalizer_in_ingredients_for_given_off_dict(
    ingredients_mapper,
):
    off_dict = {"ingredients_text": "FLOUR, SUGAR, PEANUTS."}
    ingredients_list = ["Flour", "sugar", "Peanuts"]
    ingredients_mapper.ingredient_normalizer.normalise_ingredients_list.return_value = (
        ingredients_list
    )

    result = ingredients_mapper.map_off_dict_to_ingredients(off_dict)

    assert (
        result.ingredients_list == ingredients_list
    ), f"Expected ingredients list of {ingredients_list}, got {result.ingredients_list}"


def test_should_correctly_call_ingredients_normalizer_for_given_off_dict(
    ingredients_mapper,
):
    off_dict = {"ingredients_text": "FLOUR, SUGAR, PEANUTS."}

    ingredients_mapper.map_off_dict_to_ingredients(off_dict)

    ingredients_mapper.ingredient_normalizer.normalise_ingredients_list.assert_called_with(
        off_dict["ingredients_text"]
    )
