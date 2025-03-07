from unittest.mock import patch, MagicMock

import pytest

from domain.mapper.ecoscore_data_mapper import EcoscoreDataMapper
from domain.mapper.ingredients_mapper import IngredientsMapper
from domain.mapper.nova_data_mapper import NovaDataMapper
from domain.mapper.nutriscore_data_mapper import NutriscoreDataMapper
from domain.mapper.nutrition_facts_mapper import NutritionFactsMapper
from domain.mapper.product_mapper import ProductMapper
from domain.product.complexFields.ingredients import Ingredients
from domain.product.complexFields.nova_data import NovaData
from domain.product.complexFields.nutrient_facts import NutritionFacts
from domain.product.complexFields.score.ecoscore_data import EcoscoreData
from domain.product.complexFields.score.nutriscore_data import NutriscoreData
from domain.validator.nova_data_validator import NovaDataValidator
from domain.validator.product_validator import ProductValidator


@pytest.fixture
def ingredients_mapper():
    return MagicMock(spec=IngredientsMapper)


@pytest.fixture
def product_mapper(ingredients_mapper):
    return ProductMapper(ingredients_mapper)


@pytest.fixture
def fdc_dict():
    fdc_dict = {"gtinUpc": " 0445236", "description": " GRANOLA, CINNAMON, RAISIN, CINNAMON, RAISIN  ", "brandOwner": " MICHELE'S", "ingredients": None,
                "foodNutrients": None}

    return fdc_dict


@pytest.fixture
def off_rows():
    header = ["countries_en", "code", "product_name", "generic_name", "brands", "food_groups_en", "allergens_en", "nova_group", "pnns_groups_1",
              "categories_tags", "additives_n"]
    row = ["Canada, United Kingdom ", " 455612222", " GRANOLA, CINNAMON BAR", "granola and cinnamon bar ", " Michele's, Cliff", " cereals, snacks , ",
           " allergen 1, , allergen 2", "2", "cereals again", "en:cereals", "5"]

    return row, header


@pytest.fixture
def off_dict():
    off_dict = {"countries": ["Canada", "United Kingdom "], "code": " 455612222", "product_name": " GRANOLA, CINNAMON BAR", "generic_name": "granola and cinnamon bar ", "brands": " Michele's, Cliff", "food_groups": " cereals, snacks , ", "allergens": " allergen 1, , allergen 2", "nova_group": "2", "pnns_groups_1": ["cereals again"],
              "categories_tags": ["en:cereals", "en:snacks"], "additives_n": 5}

    return off_dict


# ----------------------------------------------------------------
# Tests map_fdc_dict_to_product
# ----------------------------------------------------------------

def test_should_return_correctly_formatted_strings_in_product_for_given_fdc_dict(product_mapper, fdc_dict):
    product_mapper.ingredients_mapper.map_fdc_dict_to_ingredients.return_value = Ingredients()
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()

    with patch.object(NutritionFactsMapper,
                      'map_fdc_dict_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_fdc_dict_to_nutriscore_data',
                          return_value=nutriscore_data):
            result = product_mapper.map_fdc_dict_to_product(fdc_dict)

    assert (
            result.product_name == fdc_dict["description"].strip().title()
    ), f"Expected product name field to be {fdc_dict["description"].strip().title()}, got {result.product_name}"
    assert (
            result.generic_name_en == fdc_dict["description"].strip().title()
    ), f"Expected generic name en field to be {fdc_dict["description"].strip().title()}, got {result.generic_name_en}"
    assert (
            result.brand_name == fdc_dict["brandOwner"].strip().title()
    ), f"Expected brand name field to be {fdc_dict["brandOwner"].strip().title()}, got {result.brand_name}"


def test_should_return_given_id_in_product_for_given_fdc_dict(product_mapper, fdc_dict):
    product_mapper.ingredients_mapper.map_fdc_dict_to_ingredients.return_value = Ingredients()
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()

    with patch.object(NutritionFactsMapper,
                      'map_fdc_dict_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_fdc_dict_to_nutriscore_data',
                          return_value=nutriscore_data):
            result = product_mapper.map_fdc_dict_to_product(fdc_dict)

    assert (
            result.id == fdc_dict["gtinUpc"].strip()
    ), f"Expected id field to be {fdc_dict["gtinUpc"].strip()}, got {result.id}"


def test_should_return_mapped_ingredients_in_product_for_given_fdc_dict(product_mapper, fdc_dict):
    ingredients = Ingredients(ingredients_text="given ingredients", ingredients_list=["given ingregients"])
    product_mapper.ingredients_mapper.map_fdc_dict_to_ingredients.return_value = ingredients
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()

    with patch.object(NutritionFactsMapper,
                      'map_fdc_dict_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_fdc_dict_to_nutriscore_data',
                          return_value=nutriscore_data):
            result = product_mapper.map_fdc_dict_to_product(fdc_dict)

    assert (
            result.ingredients == ingredients
    ), f"Expected ingredients field to be {ingredients}, got {result.ingredients}"


def test_should_return_mapped_nutrition_facts_in_product_for_given_fdc_dict(product_mapper, fdc_dict):
    ingredients = Ingredients(ingredients_text="given ingredients", ingredients_list=["given ingredients"])
    product_mapper.ingredients_mapper.map_fdc_dict_to_ingredients.return_value = ingredients
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()

    with patch.object(NutritionFactsMapper,
                      'map_fdc_dict_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_fdc_dict_to_nutriscore_data',
                          return_value=nutriscore_data):
            result = product_mapper.map_fdc_dict_to_product(fdc_dict)

    assert (
            result.nutrition_facts == nutrition_facts
    ), f"Expected nutrition facts field to be {nutrition_facts}, got {result.nutrition_facts}"


def test_should_return_mapped_nutriscore_data_in_product_for_given_fdc_dict(product_mapper, fdc_dict):
    ingredients = Ingredients(ingredients_text="given ingredients", ingredients_list=["given ingregients"])
    product_mapper.ingredients_mapper.map_fdc_dict_to_ingredients.return_value = ingredients
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()

    with patch.object(NutritionFactsMapper,
                      'map_fdc_dict_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_fdc_dict_to_nutriscore_data',
                          return_value=nutriscore_data):
            result = product_mapper.map_fdc_dict_to_product(fdc_dict)

    assert (
            result.nutriscore_data == nutriscore_data
    ), f"Expected nutriscore data field to be {nutriscore_data}, got {result.nutriscore_data}"


def test_should_return_empty_list_for_food_groups_en_in_product_for_given_fdc_dict(product_mapper, fdc_dict):
    ingredients = Ingredients(ingredients_text="given ingredients", ingredients_list=["given ingregients"])
    product_mapper.ingredients_mapper.map_fdc_dict_to_ingredients.return_value = ingredients
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()

    with patch.object(NutritionFactsMapper,
                      'map_fdc_dict_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_fdc_dict_to_nutriscore_data',
                          return_value=nutriscore_data):
            result = product_mapper.map_fdc_dict_to_product(fdc_dict)

    assert (
            result.food_groups_en == []
    ), f"Expected food groups en field to be {[]}, got {result.food_groups_en}"


def test_should_return_empty_list_for_allergens_in_product_for_given_fdc_dict(product_mapper, fdc_dict):
    ingredients = Ingredients(ingredients_text="given ingredients", ingredients_list=["given ingregients"])
    product_mapper.ingredients_mapper.map_fdc_dict_to_ingredients.return_value = ingredients
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()

    with patch.object(NutritionFactsMapper,
                      'map_fdc_dict_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_fdc_dict_to_nutriscore_data',
                          return_value=nutriscore_data):
            result = product_mapper.map_fdc_dict_to_product(fdc_dict)

    assert (
            result.allergens == []
    ), f"Expected allergens field to be {[]}, got {result.allergens}"


def test_should_return_empty_is_raw_field_in_product_for_given_fdc_dict(product_mapper, fdc_dict):
    ingredients = Ingredients(ingredients_text="given ingredients", ingredients_list=["given ingregients"])
    product_mapper.ingredients_mapper.map_fdc_dict_to_ingredients.return_value = ingredients
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()

    with patch.object(NutritionFactsMapper,
                      'map_fdc_dict_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_fdc_dict_to_nutriscore_data',
                          return_value=nutriscore_data):
            result = product_mapper.map_fdc_dict_to_product(fdc_dict)

    assert (
            result.is_raw is None
    ), f"Expected is raw field to be {None}, got {result.is_raw}"


def test_should_return_empty_ecoscore_data_field_in_product_for_given_fdc_dict(product_mapper, fdc_dict):
    ingredients = Ingredients(ingredients_text="given ingredients", ingredients_list=["given ingregients"])
    product_mapper.ingredients_mapper.map_fdc_dict_to_ingredients.return_value = ingredients
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()

    with patch.object(NutritionFactsMapper,
                      'map_fdc_dict_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_fdc_dict_to_nutriscore_data',
                          return_value=nutriscore_data):
            result = product_mapper.map_fdc_dict_to_product(fdc_dict)

    assert (
            result.ecoscore_data is None
    ), f"Expected ecoscore data field to be {None}, got {result.ecoscore_data}"


def test_should_return_empty_nova_data_field_in_product_for_given_fdc_dict(product_mapper, fdc_dict):
    ingredients = Ingredients(ingredients_text="given ingredients", ingredients_list=["given ingregients"])
    product_mapper.ingredients_mapper.map_fdc_dict_to_ingredients.return_value = ingredients
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()

    with patch.object(NutritionFactsMapper,
                      'map_fdc_dict_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_fdc_dict_to_nutriscore_data',
                          return_value=nutriscore_data):
            result = product_mapper.map_fdc_dict_to_product(fdc_dict)

    assert (
            result.nova_data is None
    ), f"Expected nova data field to be {None}, got {result.nova_data}"


# ----------------------------------------------------------------
# Tests map_off_row_to_product
# ----------------------------------------------------------------

def test_should_return_correctly_formatted_strings_in_product_for_given_off_row(product_mapper, off_rows):
    product_mapper.ingredients_mapper.map_off_row_to_ingredients.return_value = Ingredients()
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()
    ecoscore_data = EcoscoreData()
    row, header = off_rows

    with patch.object(NutritionFactsMapper,
                      'map_off_row_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_off_row_to_nutriscore_data',
                          return_value=nutriscore_data):
            with patch.object(EcoscoreDataMapper,
                              'map_off_row_to_ecoscore_data',
                              return_value=ecoscore_data):
                result = product_mapper.map_off_row_to_product(row, header)

    assert (
            result.product_name == row[header.index("product_name")].strip().title()
    ), f"Expected product name field to be {row[header.index("product_name")].strip().title()}, got {result.product_name}"
    assert (
            result.generic_name_en == row[header.index("generic_name")].strip().title()
    ), f"Expected generic name en field to be {row[header.index("generic_name")].strip().title()}, got {result.generic_name_en}"
    assert (
            result.brand_name == row[header.index("brands")].strip().title()
    ), f"Expected brand name field to be {row[header.index("brands")].strip().title()}, got {result.brand_name}"


def test_should_return_given_id_in_product_for_given_off_row(product_mapper, off_rows):
    product_mapper.ingredients_mapper.map_off_row_to_ingredients.return_value = Ingredients()
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()
    ecoscore_data = EcoscoreData()
    row, header = off_rows

    with patch.object(NutritionFactsMapper,
                      'map_off_row_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_off_row_to_nutriscore_data',
                          return_value=nutriscore_data):
            with patch.object(EcoscoreDataMapper,
                              'map_off_row_to_ecoscore_data',
                              return_value=ecoscore_data):
                result = product_mapper.map_off_row_to_product(row, header)

    assert (
            result.id == row[header.index("code")].strip()
    ), f"Expected id field to be {row[header.index("code")].strip()}, got {result.id}"


def test_should_return_true_raw_field_for_raw_nova_group_in_product_for_given_off_row(product_mapper, off_rows):
    ingredients = Ingredients(ingredients_text="given ingredients", ingredients_list=["given ingredients"])
    product_mapper.ingredients_mapper.map_off_row_to_ingredients.return_value = ingredients
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()
    ecoscore_data = EcoscoreData()
    row, header = off_rows

    with patch.object(NutritionFactsMapper,
                      'map_off_row_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_off_row_to_nutriscore_data',
                          return_value=nutriscore_data):
            with patch.object(EcoscoreDataMapper,
                              'map_off_row_to_ecoscore_data',
                              return_value=ecoscore_data):
                with patch.object(NovaDataValidator,
                                  'check_nova_raw_group',
                                  return_value=True):
                    result = product_mapper.map_off_row_to_product(row, header)

    assert (
            result.is_raw
    ), f"Expected ingredients field to be {True}, got {result.is_raw}"


def test_should_return_false_raw_field_for_ultra_transformed_nova_group_in_product_for_given_off_row(product_mapper, off_rows):
    ingredients = Ingredients(ingredients_text="given ingredients", ingredients_list=["given ingredients"])
    product_mapper.ingredients_mapper.map_off_row_to_ingredients.return_value = ingredients
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()
    ecoscore_data = EcoscoreData()
    row, header = off_rows

    with patch.object(NutritionFactsMapper,
                      'map_off_row_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_off_row_to_nutriscore_data',
                          return_value=nutriscore_data):
            with patch.object(EcoscoreDataMapper,
                              'map_off_row_to_ecoscore_data',
                              return_value=ecoscore_data):
                with patch.object(NovaDataValidator,
                                  'check_nova_raw_group',
                                  return_value=False):
                    result = product_mapper.map_off_row_to_product(row, header)

    assert (
            not result.is_raw
    ), f"Expected ingredients field to be {False}, got {result.is_raw}"


def test_should_return_true_raw_field_for_other_nova_group_and_raw_pnns_group_1_in_product_for_given_off_row(product_mapper, off_rows):
    ingredients = Ingredients(ingredients_text="given ingredients", ingredients_list=["given ingredients"])
    product_mapper.ingredients_mapper.map_off_row_to_ingredients.return_value = ingredients
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()
    ecoscore_data = EcoscoreData()
    row, header = off_rows

    with patch.object(NutritionFactsMapper,
                      'map_off_row_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_off_row_to_nutriscore_data',
                          return_value=nutriscore_data):
            with patch.object(EcoscoreDataMapper,
                              'map_off_row_to_ecoscore_data',
                              return_value=ecoscore_data):
                with patch.object(ProductValidator,
                                  'check_pnn_groups',
                                  return_value=True):
                    result = product_mapper.map_off_row_to_product(row, header)

    assert (
            result.is_raw
    ), f"Expected ingredients field to be {True}, got {result.is_raw}"


def test_should_return_true_raw_field_for_other_nova_group_and_pnns_group_1_and_raw_categories_in_product_for_given_off_row(product_mapper, off_rows):
    ingredients = Ingredients(ingredients_text="given ingredients", ingredients_list=["given ingredients"])
    product_mapper.ingredients_mapper.map_off_row_to_ingredients.return_value = ingredients
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()
    ecoscore_data = EcoscoreData()
    row, header = off_rows

    with patch.object(NutritionFactsMapper,
                      'map_off_row_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_off_row_to_nutriscore_data',
                          return_value=nutriscore_data):
            with patch.object(EcoscoreDataMapper,
                              'map_off_row_to_ecoscore_data',
                              return_value=ecoscore_data):
                with patch.object(ProductValidator,
                                  'check_string_categories',
                                  return_value=True):
                    result = product_mapper.map_off_row_to_product(row, header)

    assert (
            result.is_raw
    ), f"Expected ingredients field to be {True}, got {result.is_raw}"


def test_should_return_true_raw_field_for_other_nova_group_pnns_group_1_and_categories_and_no_additives_in_product_for_given_off_row(product_mapper, off_rows):
    ingredients = Ingredients(ingredients_text="given ingredients", ingredients_list=["given ingredients"])
    product_mapper.ingredients_mapper.map_off_row_to_ingredients.return_value = ingredients
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()
    ecoscore_data = EcoscoreData()
    row, header = off_rows

    with patch.object(NutritionFactsMapper,
                      'map_off_row_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_off_row_to_nutriscore_data',
                          return_value=nutriscore_data):
            with patch.object(EcoscoreDataMapper,
                              'map_off_row_to_ecoscore_data',
                              return_value=ecoscore_data):
                with patch.object(ProductValidator,
                                  'check_additives',
                                  return_value=True):
                    result = product_mapper.map_off_row_to_product(row, header)

    assert (
            result.is_raw
    ), f"Expected ingredients field to be {True}, got {result.is_raw}"


def test_should_return_false_raw_field_for_other_nova_group_pnns_group_1_categories_and_additives_in_product_for_given_off_row(product_mapper, off_rows):
    ingredients = Ingredients(ingredients_text="given ingredients", ingredients_list=["given ingredients"])
    product_mapper.ingredients_mapper.map_off_row_to_ingredients.return_value = ingredients
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()
    ecoscore_data = EcoscoreData()
    row, header = off_rows

    with patch.object(NutritionFactsMapper,
                      'map_off_row_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_off_row_to_nutriscore_data',
                          return_value=nutriscore_data):
            with patch.object(EcoscoreDataMapper,
                              'map_off_row_to_ecoscore_data',
                              return_value=ecoscore_data):
                result = product_mapper.map_off_row_to_product(row, header)

    assert (
            not result.is_raw
    ), f"Expected ingredients field to be {False}, got {result.is_raw}"


def test_should_return_correctly_split_food_groups_en_in_product_for_given_off_row(product_mapper, off_rows):
    ingredients = Ingredients(ingredients_text="given ingredients", ingredients_list=["given ingredients"])
    product_mapper.ingredients_mapper.map_off_row_to_ingredients.return_value = ingredients
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()
    ecoscore_data = EcoscoreData()
    row, header = off_rows

    with patch.object(NutritionFactsMapper,
                      'map_off_row_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_off_row_to_nutriscore_data',
                          return_value=nutriscore_data):
            with patch.object(EcoscoreDataMapper,
                              'map_off_row_to_ecoscore_data',
                              return_value=ecoscore_data):
                result = product_mapper.map_off_row_to_product(row, header)

    expected_result = [x.strip() for x in row[header.index("food_groups_en")].split(',') if x.strip() != ""]
    assert (
            result.food_groups_en == expected_result
    ), f"Expected food groups en field to be {expected_result}, got {result.food_groups_en}"


def test_should_return_mapped_ingredients_in_product_for_given_off_row(product_mapper, off_rows):
    ingredients = Ingredients(ingredients_text="given ingredients", ingredients_list=["given ingredients"])
    product_mapper.ingredients_mapper.map_off_row_to_ingredients.return_value = ingredients
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()
    ecoscore_data = EcoscoreData()
    row, header = off_rows

    with patch.object(NutritionFactsMapper,
                      'map_off_row_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_off_row_to_nutriscore_data',
                          return_value=nutriscore_data):
            with patch.object(EcoscoreDataMapper,
                              'map_off_row_to_ecoscore_data',
                              return_value=ecoscore_data):
                result = product_mapper.map_off_row_to_product(row, header)

    assert (
            result.ingredients == ingredients
    ), f"Expected ingredients field to be {ingredients}, got {result.ingredients}"


def test_should_return_mapped_nutrition_facts_in_product_for_given_off_row(product_mapper, off_rows):
    ingredients = Ingredients(ingredients_text="given ingredients", ingredients_list=["given ingredients"])
    product_mapper.ingredients_mapper.map_off_row_to_ingredients.return_value = ingredients
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()
    ecoscore_data = EcoscoreData()
    row, header = off_rows

    with patch.object(NutritionFactsMapper,
                      'map_off_row_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_off_row_to_nutriscore_data',
                          return_value=nutriscore_data):
            with patch.object(EcoscoreDataMapper,
                              'map_off_row_to_ecoscore_data',
                              return_value=ecoscore_data):
                result = product_mapper.map_off_row_to_product(row, header)

    assert (
            result.nutrition_facts == nutrition_facts
    ), f"Expected nutrition facts field to be {nutrition_facts}, got {result.nutrition_facts}"


def test_should_return_correctly_split_allergens_in_product_for_given_off_row(product_mapper, off_rows):
    ingredients = Ingredients(ingredients_text="given ingredients", ingredients_list=["given ingredients"])
    product_mapper.ingredients_mapper.map_off_row_to_ingredients.return_value = ingredients
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()
    ecoscore_data = EcoscoreData()
    row, header = off_rows

    with patch.object(NutritionFactsMapper,
                      'map_off_row_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_off_row_to_nutriscore_data',
                          return_value=nutriscore_data):
            with patch.object(EcoscoreDataMapper,
                              'map_off_row_to_ecoscore_data',
                              return_value=ecoscore_data):
                result = product_mapper.map_off_row_to_product(row, header)

    expected_result = [x.strip() for x in row[header.index("allergens_en")].split(',') if x.strip() != ""]
    assert (
            result.allergens == expected_result
    ), f"Expected allergens field to be {expected_result}, got {result.allergens}"


def test_should_return_mapped_nutriscore_data_in_product_for_given_off_row(product_mapper, off_rows):
    ingredients = Ingredients(ingredients_text="given ingredients", ingredients_list=["given ingredients"])
    product_mapper.ingredients_mapper.map_off_row_to_ingredients.return_value = ingredients
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()
    ecoscore_data = EcoscoreData()
    row, header = off_rows

    with patch.object(NutritionFactsMapper,
                      'map_off_row_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_off_row_to_nutriscore_data',
                          return_value=nutriscore_data):
            with patch.object(EcoscoreDataMapper,
                              'map_off_row_to_ecoscore_data',
                              return_value=ecoscore_data):
                result = product_mapper.map_off_row_to_product(row, header)

    assert (
            result.nutriscore_data == nutriscore_data
    ), f"Expected nutriscore data field to be {nutriscore_data}, got {result.nutriscore_data}"


def test_should_return_mapped_ecoscore_data_field_in_product_for_given_off_row(product_mapper, off_rows):
    ingredients = Ingredients(ingredients_text="given ingredients", ingredients_list=["given ingredients"])
    product_mapper.ingredients_mapper.map_off_row_to_ingredients.return_value = ingredients
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()
    ecoscore_data = EcoscoreData()
    row, header = off_rows

    with patch.object(NutritionFactsMapper,
                      'map_off_row_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_off_row_to_nutriscore_data',
                          return_value=nutriscore_data):
            with patch.object(EcoscoreDataMapper,
                              'map_off_row_to_ecoscore_data',
                              return_value=ecoscore_data):
                result = product_mapper.map_off_row_to_product(row, header)

    assert (
            result.ecoscore_data == ecoscore_data
    ), f"Expected ecoscore data field to be {ecoscore_data}, got {result.ecoscore_data}"


def test_should_return_mapped_nova_data_field_in_product_for_given_off_row(product_mapper, off_rows):
    ingredients = Ingredients(ingredients_text="given ingredients", ingredients_list=["given ingredients"])
    product_mapper.ingredients_mapper.map_off_row_to_ingredients.return_value = ingredients
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()
    ecoscore_data = EcoscoreData()
    nova_data = NovaData()
    row, header = off_rows

    with patch.object(NutritionFactsMapper,
                      'map_off_row_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_off_row_to_nutriscore_data',
                          return_value=nutriscore_data):
            with patch.object(EcoscoreDataMapper,
                              'map_off_row_to_ecoscore_data',
                              return_value=ecoscore_data):
                with patch.object(NovaDataMapper,
                                  'map_off_row_to_nova_data',
                                  return_value=nova_data):
                    result = product_mapper.map_off_row_to_product(row, header)

    assert (
            result.nova_data == nova_data
    ), f"Expected nova data field to be {nova_data}, got {result.nova_data}"


# ----------------------------------------------------------------
# Tests map_off_dict_to_product
# ----------------------------------------------------------------

def test_should_return_correctly_formatted_strings_in_product_for_given_off_dict(product_mapper, off_dict):
    product_mapper.ingredients_mapper.map_off_dict_to_ingredients.return_value = Ingredients()
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()
    ecoscore_data = EcoscoreData()

    with patch.object(NutritionFactsMapper,
                      'map_off_dict_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_off_dict_to_nutriscore_data',
                          return_value=nutriscore_data):
            with patch.object(EcoscoreDataMapper,
                              'map_off_dict_to_ecoscore_data',
                              return_value=ecoscore_data):
                result = product_mapper.map_off_dict_to_product(off_dict)

    assert (
            result.product_name == off_dict["product_name"].strip().title()
    ), f"Expected product name field to be {off_dict["product_name"].strip().title()}, got {result.product_name}"
    assert (
            result.generic_name_en == off_dict["generic_name"].strip().title()
    ), f"Expected generic name en field to be {off_dict["generic_name"].strip().title()}, got {result.generic_name_en}"
    assert (
            result.brand_name == off_dict["brands"].strip().title()
    ), f"Expected brand name field to be {off_dict["brands"].strip().title()}, got {result.brand_name}"


def test_should_return_given_id_in_product_for_given_off_dict(product_mapper, off_dict):
    product_mapper.ingredients_mapper.map_off_dict_to_ingredients.return_value = Ingredients()
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()
    ecoscore_data = EcoscoreData()

    with patch.object(NutritionFactsMapper,
                      'map_off_dict_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_off_dict_to_nutriscore_data',
                          return_value=nutriscore_data):
            with patch.object(EcoscoreDataMapper,
                              'map_off_dict_to_ecoscore_data',
                              return_value=ecoscore_data):
                result = product_mapper.map_off_dict_to_product(off_dict)

    assert (
            result.id == off_dict["code"].strip()
    ), f"Expected id field to be {off_dict["code"].strip()}, got {result.id}"


def test_should_return_true_raw_field_for_raw_nova_group_in_product_for_given_off_dict(product_mapper, off_dict):
    product_mapper.ingredients_mapper.map_off_dict_to_ingredients.return_value = Ingredients()
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()
    ecoscore_data = EcoscoreData()

    with patch.object(NutritionFactsMapper,
                      'map_off_dict_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_off_dict_to_nutriscore_data',
                          return_value=nutriscore_data):
            with patch.object(EcoscoreDataMapper,
                              'map_off_dict_to_ecoscore_data',
                              return_value=ecoscore_data):
                with patch.object(NovaDataValidator,
                                  'check_nova_raw_group',
                                  return_value=True):
                    result = product_mapper.map_off_dict_to_product(off_dict)

    assert (
            result.is_raw
    ), f"Expected ingredients field to be {True}, got {result.is_raw}"


def test_should_return_false_raw_field_for_ultra_transformed_nova_group_in_product_for_given_off_dict(product_mapper, off_dict):
    product_mapper.ingredients_mapper.map_off_dict_to_ingredients.return_value = Ingredients()
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()
    ecoscore_data = EcoscoreData()

    with patch.object(NutritionFactsMapper,
                      'map_off_dict_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_off_dict_to_nutriscore_data',
                          return_value=nutriscore_data):
            with patch.object(EcoscoreDataMapper,
                              'map_off_dict_to_ecoscore_data',
                              return_value=ecoscore_data):
                with patch.object(NovaDataValidator,
                                  'check_nova_transformed_group',
                                  return_value=True):
                    result = product_mapper.map_off_dict_to_product(off_dict)

    assert (
            not result.is_raw
    ), f"Expected ingredients field to be {False}, got {result.is_raw}"


def test_should_return_true_raw_field_for_other_nova_group_and_raw_pnns_group_1_in_product_for_given_off_dict(product_mapper, off_dict):
    product_mapper.ingredients_mapper.map_off_dict_to_ingredients.return_value = Ingredients()
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()
    ecoscore_data = EcoscoreData()

    with patch.object(NutritionFactsMapper,
                      'map_off_dict_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_off_dict_to_nutriscore_data',
                          return_value=nutriscore_data):
            with patch.object(EcoscoreDataMapper,
                              'map_off_dict_to_ecoscore_data',
                              return_value=ecoscore_data):
                with patch.object(ProductValidator,
                                  'check_pnn_groups',
                                  return_value=True):
                    result = product_mapper.map_off_dict_to_product(off_dict)

    assert (
            result.is_raw
    ), f"Expected ingredients field to be {True}, got {result.is_raw}"


def test_should_return_true_raw_field_for_other_nova_group_and_pnns_group_1_and_raw_categories_in_product_for_given_off_dict(product_mapper, off_dict):
    product_mapper.ingredients_mapper.map_off_dict_to_ingredients.return_value = Ingredients()
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()
    ecoscore_data = EcoscoreData()

    with patch.object(NutritionFactsMapper,
                      'map_off_dict_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_off_dict_to_nutriscore_data',
                          return_value=nutriscore_data):
            with patch.object(EcoscoreDataMapper,
                              'map_off_dict_to_ecoscore_data',
                              return_value=ecoscore_data):
                with patch.object(NovaDataValidator,
                                  'check_nova_raw_group',
                                  return_value=True):
                    result = product_mapper.map_off_dict_to_product(off_dict)

    assert (
            result.is_raw
    ), f"Expected ingredients field to be {True}, got {result.is_raw}"


def test_should_return_true_raw_field_for_other_nova_group_pnns_group_1_and_categories_and_no_additives_in_product_for_given_off_dict(product_mapper, off_dict):
    product_mapper.ingredients_mapper.map_off_dict_to_ingredients.return_value = Ingredients()
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()
    ecoscore_data = EcoscoreData()

    with patch.object(NutritionFactsMapper,
                      'map_off_dict_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_off_dict_to_nutriscore_data',
                          return_value=nutriscore_data):
            with patch.object(EcoscoreDataMapper,
                              'map_off_dict_to_ecoscore_data',
                              return_value=ecoscore_data):
                with patch.object(ProductValidator,
                                  'check_additives',
                                  return_value=True):
                    result = product_mapper.map_off_dict_to_product(off_dict)

    assert (
            result.is_raw
    ), f"Expected ingredients field to be {True}, got {result.is_raw}"


def test_should_return_false_raw_field_for_other_nova_group_pnns_group_1_categories_and_additives_in_product_for_given_off_dict(product_mapper, off_dict):
    product_mapper.ingredients_mapper.map_off_dict_to_ingredients.return_value = Ingredients()
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()
    ecoscore_data = EcoscoreData()

    with patch.object(NutritionFactsMapper,
                      'map_off_dict_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_off_dict_to_nutriscore_data',
                          return_value=nutriscore_data):
            with patch.object(EcoscoreDataMapper,
                              'map_off_dict_to_ecoscore_data',
                              return_value=ecoscore_data):
                result = product_mapper.map_off_dict_to_product(off_dict)

    assert (
            not result.is_raw
    ), f"Expected ingredients field to be {False}, got {result.is_raw}"


def test_should_return_correctly_split_food_groups_en_in_product_for_given_off_dict(product_mapper, off_dict):
    product_mapper.ingredients_mapper.map_off_dict_to_ingredients.return_value = Ingredients()
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()
    ecoscore_data = EcoscoreData()

    with patch.object(NutritionFactsMapper,
                      'map_off_dict_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_off_dict_to_nutriscore_data',
                          return_value=nutriscore_data):
            with patch.object(EcoscoreDataMapper,
                              'map_off_dict_to_ecoscore_data',
                              return_value=ecoscore_data):
                result = product_mapper.map_off_dict_to_product(off_dict)

    expected_result = [x.strip() for x in off_dict["food_groups"].split(',') if x.strip() != ""]
    assert (
            result.food_groups_en == expected_result
    ), f"Expected food groups en field to be {expected_result}, got {result.food_groups_en}"


def test_should_return_mapped_ingredients_in_product_for_given_off_dict(product_mapper, off_dict):
    ingredients = Ingredients(ingredients_text="given ingredients", ingredients_list=["given ingredients"])
    product_mapper.ingredients_mapper.map_off_dict_to_ingredients.return_value = ingredients
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()
    ecoscore_data = EcoscoreData()

    with patch.object(NutritionFactsMapper,
                      'map_off_dict_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_off_dict_to_nutriscore_data',
                          return_value=nutriscore_data):
            with patch.object(EcoscoreDataMapper,
                              'map_off_dict_to_ecoscore_data',
                              return_value=ecoscore_data):
                result = product_mapper.map_off_dict_to_product(off_dict)

    assert (
            result.ingredients == ingredients
    ), f"Expected ingredients field to be {ingredients}, got {result.ingredients}"


def test_should_return_mapped_nutrition_facts_in_product_for_given_off_dict(product_mapper, off_dict):
    ingredients = Ingredients(ingredients_text="given ingredients", ingredients_list=["given ingredients"])
    product_mapper.ingredients_mapper.map_off_dict_to_ingredients.return_value = ingredients
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()
    ecoscore_data = EcoscoreData()

    with patch.object(NutritionFactsMapper,
                      'map_off_dict_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_off_dict_to_nutriscore_data',
                          return_value=nutriscore_data):
            with patch.object(EcoscoreDataMapper,
                              'map_off_dict_to_ecoscore_data',
                              return_value=ecoscore_data):
                result = product_mapper.map_off_dict_to_product(off_dict)

    assert (
            result.nutrition_facts == nutrition_facts
    ), f"Expected nutrition facts field to be {nutrition_facts}, got {result.nutrition_facts}"


def test_should_return_correctly_split_allergens_in_product_for_given_off_dict(product_mapper, off_dict):
    ingredients = Ingredients(ingredients_text="given ingredients", ingredients_list=["given ingredients"])
    product_mapper.ingredients_mapper.map_off_dict_to_ingredients.return_value = ingredients
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()
    ecoscore_data = EcoscoreData()

    with patch.object(NutritionFactsMapper,
                      'map_off_dict_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_off_dict_to_nutriscore_data',
                          return_value=nutriscore_data):
            with patch.object(EcoscoreDataMapper,
                              'map_off_dict_to_ecoscore_data',
                              return_value=ecoscore_data):
                result = product_mapper.map_off_dict_to_product(off_dict)

    expected_result = [x.strip() for x in off_dict["allergens"].split(',') if x.strip() != ""]
    assert (
            result.allergens == expected_result
    ), f"Expected allergens field to be {expected_result}, got {result.allergens}"


def test_should_return_mapped_nutriscore_data_in_product_for_given_off_dict(product_mapper, off_dict):
    ingredients = Ingredients(ingredients_text="given ingredients", ingredients_list=["given ingredients"])
    product_mapper.ingredients_mapper.map_off_dict_to_ingredients.return_value = ingredients
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()
    ecoscore_data = EcoscoreData()

    with patch.object(NutritionFactsMapper,
                      'map_off_dict_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_off_dict_to_nutriscore_data',
                          return_value=nutriscore_data):
            with patch.object(EcoscoreDataMapper,
                              'map_off_dict_to_ecoscore_data',
                              return_value=ecoscore_data):
                result = product_mapper.map_off_dict_to_product(off_dict)

    assert (
            result.nutriscore_data == nutriscore_data
    ), f"Expected nutrition facts field to be {nutriscore_data}, got {result.nutriscore_data}"


def test_should_return_mapped_ecoscore_data_field_in_product_for_given_off_dict(product_mapper, off_dict):
    ingredients = Ingredients(ingredients_text="given ingredients", ingredients_list=["given ingredients"])
    product_mapper.ingredients_mapper.map_off_dict_to_ingredients.return_value = ingredients
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()
    ecoscore_data = EcoscoreData()

    with patch.object(NutritionFactsMapper,
                      'map_off_dict_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_off_dict_to_nutriscore_data',
                          return_value=nutriscore_data):
            with patch.object(EcoscoreDataMapper,
                              'map_off_dict_to_ecoscore_data',
                              return_value=ecoscore_data):
                result = product_mapper.map_off_dict_to_product(off_dict)

    assert (
            result.ecoscore_data == ecoscore_data
    ), f"Expected ecoscore data field to be {ecoscore_data}, got {result.ecoscore_data}"


def test_should_return_mapped_nova_data_field_in_product_for_given_off_dict(product_mapper, off_dict):
    ingredients = Ingredients(ingredients_text="given ingredients", ingredients_list=["given ingredients"])
    product_mapper.ingredients_mapper.map_off_dict_to_ingredients.return_value = ingredients
    nutrition_facts = MagicMock(spec=NutritionFacts)
    nutriscore_data = NutriscoreData()
    ecoscore_data = EcoscoreData()
    nova_data = NovaData()

    with patch.object(NutritionFactsMapper,
                      'map_off_dict_to_nutrition_facts',
                      return_value=nutrition_facts):
        with patch.object(NutriscoreDataMapper,
                          'map_off_dict_to_nutriscore_data',
                          return_value=nutriscore_data):
            with patch.object(EcoscoreDataMapper,
                              'map_off_dict_to_ecoscore_data',
                              return_value=ecoscore_data):
                with patch.object(NovaDataMapper,
                                  'map_off_dict_to_nova_data',
                                  return_value=nova_data):
                    result = product_mapper.map_off_dict_to_product(off_dict)

    assert (
            result.nova_data == nova_data
    ), f"Expected nova data field to be {nova_data}, got {result.nova_data}"
