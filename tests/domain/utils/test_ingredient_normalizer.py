import pytest
from domain.utils.ingredient_normalizer import IngredientNormalizer

@pytest.fixture
def ingredient_normalizer():
    return IngredientNormalizer()

def test_should_normalize_ingredients_list(ingredient_normalizer):
    ingredients_text = "Salt, Sugar, Water"

    ingredients_list = ingredient_normalizer.normalise_ingredients_list(ingredients_text)

    assert ingredients_list == ["Salt", "Sugar", "Water"]

def test_should_remove_duplicates(ingredient_normalizer):
    ingredients_text = "Salt, Sugar, Sugar, Water"

    ingredients_list = ingredient_normalizer.normalise_ingredients_list(ingredients_text)

    assert ingredients_list == ["Salt", "Sugar", "Water"]

def test_should_normalize_case(ingredient_normalizer):
    ingredients_text = "salt, SUGAR, Water"

    ingredients_list = ingredient_normalizer.normalise_ingredients_list(ingredients_text)

    assert ingredients_list == ["Salt", "Sugar", "Water"]

def test_should_remove_punctuation(ingredient_normalizer):
    ingredients_text = "Salt, Sugar, Water."

    ingredients_list = ingredient_normalizer.normalise_ingredients_list(ingredients_text)

    assert ingredients_list == ["Salt", "Sugar", "Water"]

def test_should_remove_unnecessary_prefix(ingredient_normalizer):
    ingredients_text = "Contains: Salt, Sugar, Water"

    ingredients_list = ingredient_normalizer.normalise_ingredients_list(ingredients_text)

    assert ingredients_list == ["Salt", "Sugar", "Water"]

def test_should_keep_text_inside_parentheses(ingredient_normalizer):
    ingredients_text = "Salt (Iodized), Sugar, Water"

    ingredients_list = ingredient_normalizer.normalise_ingredients_list(ingredients_text)

    assert ingredients_list == ["Salt (Iodized)", "Sugar", "Water"]

def test_should_keep_text_inside_brackets(ingredient_normalizer):
    ingredients_text = "Salt [Iodized], Sugar, Water"

    ingredients_list = ingredient_normalizer.normalise_ingredients_list(ingredients_text)

    assert ingredients_list == ["Salt [Iodized]", "Sugar", "Water"]

def test_should_trim_spaces(ingredient_normalizer):
    ingredients_text = "  Salt  ,   Sugar , Water  "

    ingredients_list = ingredient_normalizer.normalise_ingredients_list(ingredients_text)

    assert ingredients_list == ["Salt", "Sugar", "Water"]

def test_should_return_empty_list_for_empty_string(ingredient_normalizer):
    ingredients_text = ""

    ingredients_list = ingredient_normalizer.normalise_ingredients_list(ingredients_text)

    assert ingredients_list == []
