from unittest.mock import patch, MagicMock

import pytest

from domain.mapper.brands_mapper import BrandsMapper
from domain.mapper.ecoscore_data_mapper import EcoscoreDataMapper
from domain.mapper.food_groups_mapper import FoodGroupsMapper
from domain.mapper.ingredients_mapper import IngredientsMapper
from domain.mapper.category_mapper import CategoryMapper
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
def nutriscore_data_mapper():
    return MagicMock(spec=NutriscoreDataMapper)


@pytest.fixture
def nutrition_facts_mapper():
    return MagicMock(spec=NutritionFactsMapper)


@pytest.fixture
def category_mapper():
    return MagicMock(spec=CategoryMapper)


@pytest.fixture
def product_mapper(
    ingredients_mapper, nutriscore_data_mapper, nutrition_facts_mapper, category_mapper
):
    return ProductMapper(
        ingredients_mapper,
        nutriscore_data_mapper,
        nutrition_facts_mapper,
        category_mapper,
    )


@pytest.fixture
def fdc_dict():
    fdc_dict = {
        "gtinUpc": " 00445236",
        "description": " GRANOLA, CINNAMON, RAISIN, CINNAMON, RAISIN  ",
        "brandName": "MichelE",
        "brandOwner": " MICHELE'S",
        "ingredients": None,
        "foodNutrients": None,
        "brandedFoodCategory": "cereals, ,bars ",
    }

    return fdc_dict


@pytest.fixture
def fdc_no_brand_name_dict():
    fdc_dict = {
        "gtinUpc": " 0445236",
        "description": " GRANOLA, CINNAMON, RAISIN, CINNAMON, RAISIN  ",
        "brandOwner": " MICHELE'S",
        "ingredients": None,
        "foodNutrients": None,
        "brandedFoodCategory": "cereals, ,bars ",
    }

    return fdc_dict


@pytest.fixture
def fdc_raw_dict():
    fdc_dict = {
        "gtinUpc": " 0445236",
        "description": " GRANOLA, CINNAMON, RAISIN, CINNAMON, RAISIN  ",
        "brandName": "MichelE",
        "brandOwner": " MICHELE'S",
        "ingredients": None,
        "foodNutrients": None,
        "brandedFoodCategory": "Vegetables  Unprepared/Unprocessed (Frozen)",
    }

    return fdc_dict


@pytest.fixture
def fdc_not_raw_dict():
    fdc_dict = {
        "gtinUpc": " 0445236",
        "description": " GRANOLA, CINNAMON, RAISIN, CINNAMON, RAISIN  ",
        "brandName": "MichelE",
        "brandOwner": " MICHELE'S",
        "ingredients": None,
        "foodNutrients": None,
        "brandedFoodCategory": "other",
    }

    return fdc_dict


@pytest.fixture
def fdc_not_enough_information_for_raw_dict():
    fdc_dict = {
        "gtinUpc": " 0445236",
        "description": " GRANOLA, CINNAMON, RAISIN, CINNAMON, RAISIN  ",
        "brandName": "MichelE",
        "brandOwner": " MICHELE'S",
        "ingredients": None,
        "foodNutrients": None,
        "brandedFoodCategory": "Pre-Packaged Fruit & Vegetables",
    }

    return fdc_dict


@pytest.fixture
def off_rows():
    header = [
        "countries_en",
        "code",
        "product_name",
        "generic_name",
        "brands",
        "food_groups_en",
        "nova_group",
        "pnns_groups_1",
        "categories_tags",
        "additives_n",
    ]
    row = [
        "Canada, United Kingdom ",
        " 00455612222",
        " GRANOLA, CINNAMON BAR",
        "granola and cinnamon bar ",
        " Michele's, Cliff",
        " cereals, snacks , ",
        "2",
        "cereals again",
        "en:cereals",
        "5",
    ]

    return row, header


@pytest.fixture
def off_emtpy_strings_rows():
    header = [
        "countries_en",
        "code",
        "product_name",
        "generic_name",
        "brands",
        "food_groups_en",
        "nova_group",
        "pnns_groups_1",
        "categories_tags",
        "additives_n",
    ]
    row = [
        "Canada, United Kingdom ",
        " 455612222",
        "",
        " ",
        " Michele's, Cliff",
        " cereals, snacks , ",
        "2",
        "cereals again",
        "en:cereals",
        "5",
    ]

    return row, header


@pytest.fixture
def off_rows_without_canada():
    header = [
        "countries_en",
        "code",
        "product_name",
        "generic_name",
        "brands",
        "food_groups_en",
        "nova_group",
        "pnns_groups_1",
        "categories_tags",
        "additives_n",
    ]
    row = [
        "Spain, United Kingdom ",
        " 455612222",
        " GRANOLA, CINNAMON BAR",
        "granola and cinnamon bar ",
        " Michele's, Cliff",
        " cereals, snacks , ",
        "2",
        "cereals again",
        "en:cereals",
        "5",
    ]

    return row, header


@pytest.fixture
def off_dict():
    off_dict = {
        "countries": ["Canada", "United Kingdom "],
        "code": " 00455612222",
        "product_name": " GRANOLA, CINNAMON BAR",
        "generic_name": "granola and cinnamon bar ",
        "brands": " Michele's, CLIFF",
        "brand_owner": " MICHELE'S",
        "food_groups": " cereals, snacks , ",
        "nova_group": "2",
        "pnns_groups_1": ["cereals again"],
        "categories_tags": ["en:cereals", "en:snacks"],
        "additives_n": 5,
        "categories": "en:breads, en:meals",
    }

    return off_dict


@pytest.fixture
def off_empty_strings_dict():
    off_dict = {
        "countries": ["Canada", "United Kingdom "],
        "code": " 455612222",
        "product_name": "",
        "generic_name": " ",
        "brands": " Michele's, CLIFF",
        "brand_owner": " MICHELE'S",
        "food_groups": " cereals, snacks , ",
        "nova_group": "2",
        "pnns_groups_1": ["cereals again"],
        "categories_tags": ["en:cereals", "en:snacks"],
        "additives_n": 5,
        "categories": "en:breads",
    }

    return off_dict


@pytest.fixture
def off_dict_without_canada():
    off_dict = {
        "countries": ["Spain", "United Kingdom "],
        "code": " 455612222",
        "product_name": " GRANOLA, CINNAMON BAR",
        "generic_name": "granola and cinnamon bar ",
        "brands": " Michele's, Cliff",
        "food_groups": " cereals, snacks , ",
        "nova_group": "2",
        "pnns_groups_1": ["cereals again"],
        "categories_tags": ["en:cereals", "en:snacks"],
        "additives_n": 5,
    }

    return off_dict


@pytest.fixture
def mock_fdc_functions(product_mapper):
    nutrition_facts = MagicMock(spec=NutritionFacts)
    ingredients = MagicMock(spec=Ingredients)
    nutriscore_data = MagicMock(spec=NutriscoreData)

    product_mapper.ingredients_mapper.map_fdc_dict_to_ingredients.return_value = (
        ingredients
    )
    product_mapper.nutriscore_data_mapper.map_fdc_dict_to_nutriscore_data.return_value = (
        nutriscore_data
    )
    product_mapper.nutrition_facts_mapper.map_fdc_dict_to_nutrition_facts.return_value = (
        nutrition_facts
    )

    with patch.object(
        NutritionFactsMapper,
        "map_fdc_dict_to_nutrition_facts",
        return_value=nutrition_facts,
    ):
        yield {
            "nutrition_facts": nutrition_facts,
            "ingredients": ingredients,
            "nutriscore_data": nutriscore_data,
        }


@pytest.fixture
def mock_off_row_functions(product_mapper):
    ingredients = MagicMock(spec=Ingredients)
    nutriscore_data = MagicMock(spec=NutriscoreData)
    nutrition_facts = MagicMock(spec=NutritionFacts)
    ecoscore_data = MagicMock(spec=EcoscoreData)
    nova_data = MagicMock(spec=NovaData)
    brands = ["brand 1", "brand 2", "brand 3"]
    brand_owner = "brand owner name"
    food_groups = ["food group1", "food group 2"]

    product_mapper.ingredients_mapper.map_off_row_to_ingredients.return_value = (
        ingredients
    )
    product_mapper.nutriscore_data_mapper.map_off_row_to_nutriscore_data.return_value = (
        nutriscore_data
    )
    product_mapper.nutrition_facts_mapper.map_off_row_to_nutrition_facts.return_value = (
        nutrition_facts
    )

    with patch.object(BrandsMapper, "map_off_row_to_brands", return_value=brands):
        with patch.object(
            BrandsMapper, "map_off_row_to_brand_owner", return_value=brand_owner
        ):
            with patch.object(
                FoodGroupsMapper,
                "map_off_row_to_food_groups",
                return_value=food_groups,
            ):
                with patch.object(
                    NutritionFactsMapper,
                    "map_off_row_to_nutrition_facts",
                    return_value=nutrition_facts,
                ):
                    with patch.object(
                        EcoscoreDataMapper,
                        "map_off_row_to_ecoscore_data",
                        return_value=ecoscore_data,
                    ):
                        with patch.object(
                            NovaDataMapper,
                            "map_off_row_to_nova_data",
                            return_value=nova_data,
                        ):
                            yield {
                                "ingredients": ingredients,
                                "nutriscore_data": nutriscore_data,
                                "nutrition_facts": nutrition_facts,
                                "ecoscore_data": ecoscore_data,
                                "brand_owner": brand_owner,
                                "brands": brands,
                                "food_groups": food_groups,
                                "nova_data": nova_data,
                            }


@pytest.fixture
def mock_off_dict_functions(product_mapper):
    ingredients = MagicMock(spec=Ingredients)
    nutriscore_data = MagicMock(spec=NutriscoreData)
    nutrition_facts = MagicMock(spec=NutritionFacts)
    ecoscore_data = MagicMock(spec=EcoscoreData)
    nova_data = MagicMock(spec=NovaData)
    brands = ["brand 1", "brand 2", "brand 3"]
    brand_owner = "brand owner name"
    food_groups = ["food group1", "food group 2"]

    product_mapper.ingredients_mapper.map_off_dict_to_ingredients.return_value = (
        ingredients
    )
    product_mapper.nutriscore_data_mapper.map_off_dict_to_nutriscore_data.return_value = (
        nutriscore_data
    )
    product_mapper.nutrition_facts_mapper.map_off_dict_to_nutrition_facts.return_value = (
        nutrition_facts
    )

    with patch.object(BrandsMapper, "map_off_dict_to_brands", return_value=brands):
        with patch.object(
            BrandsMapper, "map_off_dict_to_brand_owner", return_value=brand_owner
        ):
            with patch.object(
                FoodGroupsMapper,
                "map_off_dict_to_food_groups",
                return_value=food_groups,
            ):
                with patch.object(
                    NutritionFactsMapper,
                    "map_off_dict_to_nutrition_facts",
                    return_value=nutrition_facts,
                ):
                    with patch.object(
                        EcoscoreDataMapper,
                        "map_off_dict_to_ecoscore_data",
                        return_value=ecoscore_data,
                    ):
                        with patch.object(
                            NovaDataMapper,
                            "map_off_dict_to_nova_data",
                            return_value=nova_data,
                        ):
                            yield {
                                "ingredients": ingredients,
                                "nutriscore_data": nutriscore_data,
                                "ecoscore_data": ecoscore_data,
                                "nova_data": nova_data,
                                "nutrition_facts": nutrition_facts,
                                "brand_owner": brand_owner,
                                "brands": brands,
                                "food_groups": food_groups,
                            }


# ----------------------------------------------------------------
# Tests map_fdc_dict_to_product
# ----------------------------------------------------------------


def test_should_return_correctly_formatted_strings_in_product_for_given_fdc_dict(
    product_mapper, fdc_dict, mock_fdc_functions
):
    result = product_mapper.map_fdc_dict_to_product(fdc_dict)

    assert (
        result.product_name == fdc_dict["description"].strip().title()
    ), f"Expected product name field to be {fdc_dict["description"].strip().title()}, got {result.product_name}"
    assert (
        result.generic_name_en == fdc_dict["description"].strip().title()
    ), f"Expected generic name en field to be {fdc_dict["description"].strip().title()}, got {result.generic_name_en}"
    assert (
        result.brand_owner == fdc_dict["brandOwner"].strip().title()
    ), f"Expected brand name field to be {fdc_dict["brandOwner"].strip().title()}, got {result.brand_name}"


def test_should_return_given_id_for_id_original_in_product_for_given_fdc_dict(
    product_mapper, fdc_dict, mock_fdc_functions
):
    result = product_mapper.map_fdc_dict_to_product(fdc_dict)

    assert (
        result.id_original == fdc_dict["gtinUpc"].strip()
    ), f"Expected original id field to be {fdc_dict["gtinUpc"].strip()}, got {result.id_original}"


def test_should_return_id_without_zeros_at_the_beginning_for_id_match_in_product_for_given_fdc_dict(
    product_mapper, fdc_dict, mock_fdc_functions
):
    result = product_mapper.map_fdc_dict_to_product(fdc_dict)

    assert result.id_match == fdc_dict["gtinUpc"].strip().lstrip(
        "0"
    ), f"Expected match id field to be {fdc_dict["gtinUpc"].strip().lstrip("0")}, got {result.id_match}"


def test_should_return_given_brand_name_in_brands_list_in_product_for_given_fdc_dict(
    product_mapper, fdc_dict, mock_fdc_functions
):
    result = product_mapper.map_fdc_dict_to_product(fdc_dict)

    assert result.brands == [
        fdc_dict["brandName"].strip().title()
    ], f"Expected brands field to be {[fdc_dict["gtinUpc"].strip().title()]}, got {result.brands}"


def test_should_return_empty_brands_list_in_product_for_given_fdc_dict(
    product_mapper, fdc_no_brand_name_dict, mock_fdc_functions
):
    result = product_mapper.map_fdc_dict_to_product(fdc_no_brand_name_dict)

    assert result.brands == [], f"Expected brands field to be {[]}, got {result.brands}"


def test_should_return_mapped_ingredients_in_product_for_given_fdc_dict(
    product_mapper, fdc_dict, mock_fdc_functions
):
    result = product_mapper.map_fdc_dict_to_product(fdc_dict)

    assert (
        result.ingredients == mock_fdc_functions["ingredients"]
    ), f"Expected ingredients field to be {mock_fdc_functions["ingredients"]}, got {result.ingredients}"


def test_should_return_mapped_category_in_product_for_fdc_dict(
    product_mapper, fdc_dict, mock_fdc_functions
):
    product_mapper.category_mapper.get_off_categories_of_fdc_product.return_value = [
        "en:cereals",
        "en:snacks",
    ]

    result = product_mapper.map_fdc_dict_to_product(fdc_dict)

    assert result.categories_en == ["en:cereals", "en:snacks"]


def test_should_return_mapped_nutrition_facts_in_product_for_given_fdc_dict(
    product_mapper, fdc_dict, mock_fdc_functions
):
    result = product_mapper.map_fdc_dict_to_product(fdc_dict)

    assert (
        result.nutrition_facts == mock_fdc_functions["nutrition_facts"]
    ), f"Expected nutrition facts field to be {mock_fdc_functions["nutrition_facts"]}, got {result.nutrition_facts}"


def test_should_return_mapped_nutriscore_data_in_product_for_given_fdc_dict(
    product_mapper, fdc_dict, mock_fdc_functions
):
    result = product_mapper.map_fdc_dict_to_product(fdc_dict)

    assert (
        result.nutriscore_data == mock_fdc_functions["nutriscore_data"]
    ), f"Expected nutriscore data field to be {mock_fdc_functions["nutriscore_data"]}, got {result.nutriscore_data}"


def test_should_return_correctly_split_list_for_food_groups_en_in_product_for_given_fdc_dict(
    product_mapper, fdc_dict, mock_fdc_functions
):
    result = product_mapper.map_fdc_dict_to_product(fdc_dict)

    expected_result = [
        x.strip() for x in fdc_dict["brandedFoodCategory"].split(",") if x.strip() != ""
    ]
    assert (
        result.food_groups_en == expected_result
    ), f"Expected food groups en field to be {expected_result}, got {result.food_groups_en}"


def test_should_return_empty_is_raw_field_when_not_enough_information_in_product_for_given_fdc_dict(
    product_mapper, fdc_not_enough_information_for_raw_dict, mock_fdc_functions
):
    result = product_mapper.map_fdc_dict_to_product(
        fdc_not_enough_information_for_raw_dict
    )

    assert (
        result.is_raw is None
    ), f"Expected is raw field to be {None}, got {result.is_raw}"


def test_should_return_true_is_raw_field_for_raw_product_in_product_for_given_fdc_dict(
    product_mapper, fdc_raw_dict, mock_fdc_functions
):
    result = product_mapper.map_fdc_dict_to_product(fdc_raw_dict)

    assert result.is_raw, f"Expected is raw field to be {True}, got {result.is_raw}"


def test_should_return_false_is_raw_field_for_not_raw_product_in_product_for_given_fdc_dict(
    product_mapper, fdc_not_raw_dict, mock_fdc_functions
):
    result = product_mapper.map_fdc_dict_to_product(fdc_not_raw_dict)

    assert (
        not result.is_raw
    ), f"Expected is raw field to be {False}, got {result.is_raw}"


def test_should_return_empty_ecoscore_data_field_in_product_for_given_fdc_dict(
    product_mapper, fdc_dict, mock_fdc_functions
):
    result = product_mapper.map_fdc_dict_to_product(fdc_dict)

    assert (
        result.ecoscore_data is None
    ), f"Expected ecoscore data field to be {None}, got {result.ecoscore_data}"


def test_should_return_empty_nova_data_field_in_product_for_given_fdc_dict(
    product_mapper, fdc_dict, mock_fdc_functions
):
    result = product_mapper.map_fdc_dict_to_product(fdc_dict)

    assert (
        result.nova_data is None
    ), f"Expected nova data field to be {None}, got {result.nova_data}"


# ----------------------------------------------------------------
# Tests map_off_row_to_product
# ----------------------------------------------------------------


def test_should_return_no_product_if_canada_not_in_countries_for_given_off_row(
    product_mapper, off_rows_without_canada
):
    row, header = off_rows_without_canada

    result = product_mapper.map_off_row_to_product(row, header)

    assert result is None, f"Expected no product returned, got {result}"


def test_should_return_correctly_formatted_strings_in_product_for_given_off_row(
    product_mapper, off_rows, mock_off_row_functions
):
    row, header = off_rows

    result = product_mapper.map_off_row_to_product(row, header)

    assert (
        result.product_name == row[header.index("product_name")].strip().title()
    ), f"Expected product name field to be {row[header.index("product_name")].strip().title()}, got {result.product_name}"
    assert (
        result.generic_name_en == row[header.index("generic_name")].strip().title()
    ), f"Expected generic name en field to be {row[header.index("generic_name")].strip().title()}, got {result.generic_name_en}"


def test_should_return_empty_string_fields_for_given_empty_strings_in_product_for_given_off_row(
    product_mapper, off_emtpy_strings_rows, mock_off_row_functions
):
    row, header = off_emtpy_strings_rows

    result = product_mapper.map_off_row_to_product(row, header)

    assert (
        result.product_name is None
    ), f"Expected product name field to be {row[header.index("product_name")].strip().title()}, got {result.product_name}"
    assert (
        result.generic_name_en is None
    ), f"Expected generic name en field to be {row[header.index("generic_name")].strip().title()}, got {result.generic_name_en}"


def test_should_return_mapped_brand_owner_name_in_product_for_given_off_row(
    product_mapper, off_rows, mock_off_row_functions
):
    row, header = off_rows

    result = product_mapper.map_off_row_to_product(row, header)

    assert (
        result.brand_owner == mock_off_row_functions["brand_owner"]
    ), f"Expected brand name field to be {mock_off_row_functions["brand_owner"]}, got {result.brand_owner}"


def test_should_return_given_id_for_id_original_in_product_for_given_off_row(
    product_mapper, off_rows, mock_off_row_functions
):
    row, header = off_rows

    result = product_mapper.map_off_row_to_product(row, header)

    assert (
        result.id_original == row[header.index("code")].strip()
    ), f"Expected original id field to be {row[header.index("code")].strip()}, got {result.id_original}"


def test_should_return_id_without_zeros_at_the_beginning_for_id_match_in_product_for_given_off_row(
    product_mapper, off_rows, mock_off_row_functions
):
    row, header = off_rows

    result = product_mapper.map_off_row_to_product(row, header)

    assert result.id_match == row[header.index("code")].strip().lstrip(
        "0"
    ), f"Expected match id field to be {row[header.index("code")].strip()}, got {result.id_match}"


def test_should_return_true_is_raw_field_for_raw_nova_group_in_product_for_given_off_row(
    product_mapper, off_rows, mock_off_row_functions
):
    row, header = off_rows

    with patch.object(NovaDataValidator, "check_nova_raw_group", return_value=True):
        result = product_mapper.map_off_row_to_product(row, header)

    assert (
        result.is_raw
    ), f"Expected ingredients field to be {True}, got {result.is_raw}"


def test_should_return_false_is_raw_field_for_ultra_transformed_nova_group_in_product_for_given_off_row(
    product_mapper, off_rows, mock_off_row_functions
):
    row, header = off_rows

    with patch.object(
        NovaDataValidator,
        "check_nova_raw_group",
        return_value=False,
    ):
        result = product_mapper.map_off_row_to_product(row, header)

    assert (
        not result.is_raw
    ), f"Expected ingredients field to be {False}, got {result.is_raw}"


def test_should_return_true_is_raw_field_for_other_nova_group_and_raw_pnns_group_1_in_product_for_given_off_row(
    product_mapper, off_rows, mock_off_row_functions
):
    row, header = off_rows

    with patch.object(ProductValidator, "check_pnns_groups", return_value=True):
        result = product_mapper.map_off_row_to_product(row, header)

    assert (
        result.is_raw
    ), f"Expected ingredients field to be {True}, got {result.is_raw}"


def test_should_return_true_is_raw_field_for_other_nova_group_and_pnns_group_1_and_raw_categories_in_product_for_given_off_row(
    product_mapper, off_rows, mock_off_row_functions
):
    row, header = off_rows

    with patch.object(
        ProductValidator,
        "check_string_categories",
        return_value=True,
    ):
        result = product_mapper.map_off_row_to_product(row, header)

    assert (
        result.is_raw
    ), f"Expected ingredients field to be {True}, got {result.is_raw}"


def test_should_return_true_is_raw_field_for_other_nova_group_pnns_group_1_and_categories_and_no_additives_in_product_for_given_off_row(
    product_mapper, off_rows, mock_off_row_functions
):
    row, header = off_rows

    with patch.object(ProductValidator, "check_additives", return_value=True):
        result = product_mapper.map_off_row_to_product(row, header)

    assert (
        result.is_raw
    ), f"Expected ingredients field to be {True}, got {result.is_raw}"


def test_should_return_false_is_raw_field_for_other_nova_group_pnns_group_1_categories_and_additives_in_product_for_given_off_row(
    product_mapper, off_rows, mock_off_row_functions
):
    row, header = off_rows

    result = product_mapper.map_off_row_to_product(row, header)

    assert (
        not result.is_raw
    ), f"Expected ingredients field to be {False}, got {result.is_raw}"


def test_should_return_mapped_brands_in_product_for_given_off_row(
    product_mapper, off_rows, mock_off_row_functions
):
    row, header = off_rows

    result = product_mapper.map_off_row_to_product(row, header)

    assert (
        result.brands == mock_off_row_functions["brands"]
    ), f"Expected brands field to be {mock_off_row_functions["brands"]}, got {result.brands}"


def test_should_return_correctly_split_food_groups_en_in_product_for_given_off_row(
    product_mapper, off_rows, mock_off_row_functions
):
    row, header = off_rows

    result = product_mapper.map_off_row_to_product(row, header)

    assert (
        result.food_groups_en == mock_off_row_functions["food_groups"]
    ), f"Expected food groups en field to be {mock_off_row_functions["food_groups"]}, got {result.food_groups_en}"


def test_should_return_mapped_ingredients_in_product_for_given_off_row(
    product_mapper, off_rows, mock_off_row_functions
):
    row, header = off_rows

    result = product_mapper.map_off_row_to_product(row, header)

    assert (
        result.ingredients == mock_off_row_functions["ingredients"]
    ), f"Expected ingredients field to be {mock_off_row_functions["ingredients"]}, got {result.ingredients}"


def test_should_return_mapped_category_in_product_for_off_row(
    product_mapper, off_rows, mock_off_row_functions
):
    row, header = off_rows
    product_mapper.category_mapper.get_off_categories_of_off_product.return_value = [
        "en:cereals",
        "en:snacks",
    ]

    result = product_mapper.map_off_row_to_product(row, header)

    assert result.categories_en == ["en:cereals", "en:snacks"]


def test_should_return_mapped_nutrition_facts_in_product_for_given_off_row(
    product_mapper, off_rows, mock_off_row_functions
):
    row, header = off_rows

    result = product_mapper.map_off_row_to_product(row, header)

    assert (
        result.nutrition_facts == mock_off_row_functions["nutrition_facts"]
    ), f"Expected nutrition facts field to be {mock_off_row_functions["nutrition_facts"]}, got {result.nutrition_facts}"


def test_should_return_mapped_nutriscore_data_in_product_for_given_off_row(
    product_mapper, off_rows, mock_off_row_functions
):
    row, header = off_rows

    result = product_mapper.map_off_row_to_product(row, header)

    assert (
        result.nutriscore_data == mock_off_row_functions["nutriscore_data"]
    ), f"Expected nutriscore data field to be {mock_off_row_functions["nutriscore_data"]}, got {result.nutriscore_data}"


def test_should_return_mapped_ecoscore_data_field_in_product_for_given_off_row(
    product_mapper, off_rows, mock_off_row_functions
):
    row, header = off_rows

    result = product_mapper.map_off_row_to_product(row, header)

    assert (
        result.ecoscore_data == mock_off_row_functions["ecoscore_data"]
    ), f"Expected ecoscore data field to be {mock_off_row_functions["ecoscore_data"]}, got {result.ecoscore_data}"


def test_should_return_mapped_nova_data_field_in_product_for_given_off_row(
    product_mapper, off_rows, mock_off_row_functions
):
    row, header = off_rows

    result = product_mapper.map_off_row_to_product(row, header)

    assert (
        result.nova_data == mock_off_row_functions["nova_data"]
    ), f"Expected nova data field to be {mock_off_row_functions["nova_data"]}, got {result.nova_data}"


# ----------------------------------------------------------------
# Tests map_off_dict_to_product
# ----------------------------------------------------------------


def test_should_return_no_product_if_canada_not_in_countries_for_given_off_dict(
    product_mapper, off_dict_without_canada
):
    result = product_mapper.map_off_dict_to_product(off_dict_without_canada)

    assert result is None, f"Expected no product returned, got {result}"


def test_should_return_correctly_formatted_strings_in_product_for_given_off_dict(
    product_mapper, off_dict, mock_off_dict_functions
):
    result = product_mapper.map_off_dict_to_product(off_dict)

    assert (
        result.product_name == off_dict["product_name"].strip().title()
    ), f"Expected product name field to be {off_dict["product_name"].strip().title()}, got {result.product_name}"
    assert (
        result.generic_name_en == off_dict["generic_name"].strip().title()
    ), f"Expected generic name en field to be {off_dict["generic_name"].strip().title()}, got {result.generic_name_en}"


def test_should_return_empty_string_fields_for_given_empty_strings_in_product_for_given_off_dict(
    product_mapper, off_empty_strings_dict, mock_off_dict_functions
):
    result = product_mapper.map_off_dict_to_product(off_empty_strings_dict)

    assert (
        result.product_name is None
    ), f"Expected product name field to be {None}, got {result.product_name}"
    assert (
        result.generic_name_en is None
    ), f"Expected generic name en field to be {None}, got {result.generic_name_en}"


def test_should_return_mapped_brand_owner_name_in_product_for_given_off_dict(
    product_mapper, off_dict, mock_off_dict_functions
):
    result = product_mapper.map_off_dict_to_product(off_dict)

    assert (
        result.brand_owner == mock_off_dict_functions["brand_owner"]
    ), f"Expected brand owner field to be {mock_off_dict_functions["brand_owner"]}, got {result.brand_name}"


def test_should_return_given_id_for_id_original_in_product_for_given_off_dict(
    product_mapper, off_dict, mock_off_dict_functions
):
    result = product_mapper.map_off_dict_to_product(off_dict)

    assert (
        result.id_original == off_dict["code"].strip()
    ), f"Expected original id field to be {off_dict["code"].strip()}, got {result.id_match}"


def test_should_return_id_without_zeros_at_the_beginning_for_id_match_in_product_for_given_off_dict(
    product_mapper, off_dict, mock_off_dict_functions
):
    result = product_mapper.map_off_dict_to_product(off_dict)

    assert result.id_match == off_dict["code"].strip().lstrip(
        "0"
    ), f"Expected match id field to be {off_dict["code"].strip().lstrip("0")}, got {result.id_match}"


def test_should_return_true_is_raw_field_for_raw_nova_group_in_product_for_given_off_dict(
    product_mapper, off_dict, mock_off_dict_functions
):
    with patch.object(NovaDataValidator, "check_nova_raw_group", return_value=True):
        result = product_mapper.map_off_dict_to_product(off_dict)

    assert result.is_raw, f"Expected is raw field to be {True}, got {result.is_raw}"


def test_should_return_false_is_raw_field_for_ultra_transformed_nova_group_in_product_for_given_off_dict(
    product_mapper, off_dict, mock_off_dict_functions
):
    with patch.object(
        NovaDataValidator, "check_nova_transformed_group", return_value=True
    ):
        result = product_mapper.map_off_dict_to_product(off_dict)

    assert (
        not result.is_raw
    ), f"Expected is raw field to be {False}, got {result.is_raw}"


def test_should_return_true_is_raw_field_for_other_nova_group_and_raw_pnns_group_1_in_product_for_given_off_dict(
    product_mapper, off_dict, mock_off_dict_functions
):
    with patch.object(ProductValidator, "check_pnns_groups", return_value=True):
        result = product_mapper.map_off_dict_to_product(off_dict)

    assert result.is_raw, f"Expected is raw field to be {True}, got {result.is_raw}"


def test_should_return_true_is_raw_field_for_other_nova_group_and_pnns_group_1_and_raw_categories_in_product_for_given_off_dict(
    product_mapper, off_dict, mock_off_dict_functions
):
    with patch.object(NovaDataValidator, "check_nova_raw_group", return_value=True):
        result = product_mapper.map_off_dict_to_product(off_dict)

    assert result.is_raw, f"Expected is raw field to be {True}, got {result.is_raw}"


def test_should_return_true_is_raw_field_for_other_nova_group_pnns_group_1_and_categories_and_no_additives_in_product_for_given_off_dict(
    product_mapper, off_dict, mock_off_dict_functions
):
    with patch.object(ProductValidator, "check_additives", return_value=True):
        result = product_mapper.map_off_dict_to_product(off_dict)

    assert result.is_raw, f"Expected is raw field to be {True}, got {result.is_raw}"


def test_should_return_false_is_raw_field_for_other_nova_group_pnns_group_1_categories_and_additives_in_product_for_given_off_dict(
    product_mapper, off_dict, mock_off_dict_functions
):
    result = product_mapper.map_off_dict_to_product(off_dict)

    assert (
        not result.is_raw
    ), f"Expected is raw field to be {False}, got {result.is_raw}"


def test_should_return_mapped_brands_in_product_for_given_off_dict(
    product_mapper, off_dict, mock_off_dict_functions
):
    result = product_mapper.map_off_dict_to_product(off_dict)

    assert (
        result.brands == mock_off_dict_functions["brands"]
    ), f"Expected brands field to be {mock_off_dict_functions["brands"]}, got {result.brands}"


def test_should_return_correctly_split_food_groups_en_in_product_for_given_off_dict(
    product_mapper, off_dict, mock_off_dict_functions
):
    result = product_mapper.map_off_dict_to_product(off_dict)

    assert (
        result.food_groups_en == mock_off_dict_functions["food_groups"]
    ), f"Expected food groups en field to be {mock_off_dict_functions["food_groups"]}, got {result.food_groups_en}"


def test_should_return_mapped_ingredients_in_product_for_given_off_dict(
    product_mapper, off_dict, mock_off_dict_functions
):
    result = product_mapper.map_off_dict_to_product(off_dict)

    assert (
        result.ingredients == mock_off_dict_functions["ingredients"]
    ), f"Expected ingredients field to be {mock_off_dict_functions["ingredients"]}, got {result.ingredients}"


def test_should_return_mapped_category_in_product_for_off_dict(
    product_mapper, off_dict, mock_off_dict_functions
):
    product_mapper.category_mapper.get_off_categories_of_off_product.return_value = [
        "en:cereals",
        "en:snacks",
    ]

    result = product_mapper.map_off_dict_to_product(off_dict)

    assert result.categories_en == ["en:cereals", "en:snacks"]


def test_should_return_mapped_nutrition_facts_in_product_for_given_off_dict(
    product_mapper, off_dict, mock_off_dict_functions
):
    result = product_mapper.map_off_dict_to_product(off_dict)

    assert (
        result.nutrition_facts == mock_off_dict_functions["nutrition_facts"]
    ), f"Expected nutrition facts field to be {mock_off_dict_functions["nutrition_facts"]}, got {result.nutrition_facts}"


def test_should_return_mapped_nutriscore_data_in_product_for_given_off_dict(
    product_mapper, off_dict, mock_off_dict_functions
):
    result = product_mapper.map_off_dict_to_product(off_dict)

    assert (
        result.nutriscore_data == mock_off_dict_functions["nutriscore_data"]
    ), f"Expected nutrition facts field to be {mock_off_dict_functions["nutriscore_data"]}, got {result.nutriscore_data}"


def test_should_return_mapped_ecoscore_data_field_in_product_for_given_off_dict(
    product_mapper, off_dict, mock_off_dict_functions
):
    result = product_mapper.map_off_dict_to_product(off_dict)

    assert (
        result.ecoscore_data == mock_off_dict_functions["ecoscore_data"]
    ), f"Expected ecoscore data field to be {mock_off_dict_functions["ecoscore_data"]}, got {result.ecoscore_data}"


def test_should_return_mapped_nova_data_field_in_product_for_given_off_dict(
    product_mapper, off_dict, mock_off_dict_functions
):
    result = product_mapper.map_off_dict_to_product(off_dict)

    assert (
        result.nova_data == mock_off_dict_functions["nova_data"]
    ), f"Expected nova data field to be {mock_off_dict_functions["nova_data"]}, got {result.nova_data}"
