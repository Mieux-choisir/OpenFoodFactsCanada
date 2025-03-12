from unittest.mock import MagicMock, patch

import pytest

from domain.mapper.allergens_mapper import AllergensMapper
from domain.mapper.brands_mapper import BrandsMapper
from domain.mapper.ecoscore_data_mapper import EcoscoreDataMapper
from domain.mapper.food_groups_mapper import FoodGroupsMapper
from domain.mapper.ingredients_mapper import IngredientsMapper
from domain.mapper.nutriscore_data_mapper import NutriscoreDataMapper
from domain.mapper.nutrition_facts_mapper import NutritionFactsMapper
from domain.mapper.product_mapper import ProductMapper
from domain.product.food_category_model import FoodCategoryModel


@pytest.fixture
def ingredients_mapper():
    return MagicMock(spec=IngredientsMapper)


@pytest.fixture
def nutriscore_data_mapper():
    return MagicMock(spec=NutriscoreDataMapper)


@pytest.fixture
def food_category_model():
    return MagicMock(spec=FoodCategoryModel)


@pytest.fixture
def product_mapper(ingredients_mapper, nutriscore_data_mapper, food_category_model):
    product_mapper = ProductMapper(ingredients_mapper=ingredients_mapper, nutriscore_data_mapper=nutriscore_data_mapper,
                                   food_category_model=food_category_model)
    return product_mapper


def test_should_return_mapped_category_in_product_for_off_row(product_mapper):
    row = ["Canada", "195", "Super bars", "bars", "en:cereals", "4", "bars", "4"]
    header = ["countries_en", "code", "product_name", "generic_name", "categories_tags", "nova_group", "pnns_groups_1", "additives_n"]
    product_mapper.food_category_model.get_off_category.return_value = "en:cereals"
    product_mapper.ingredients_mapper.map_off_row_to_ingredients.return_value = None
    product_mapper.nutriscore_data_mapper.map_off_row_to_nutriscore_data.return_value = None

    with patch.object(BrandsMapper,
                      "map_off_row_to_brands",
                      return_value=[]):
        with patch.object(BrandsMapper,
                          "map_off_row_to_brand_owner",
                          return_value=""):
            with patch.object(FoodGroupsMapper,
                              "map_off_row_to_food_groups",
                              return_value=[]):
                with patch.object(NutritionFactsMapper,
                                  "map_off_row_to_nutrition_facts",
                                  return_value=None):
                    with patch.object(AllergensMapper,
                                      "map_off_row_to_allergens",
                                      return_value=[]):
                        with patch.object(EcoscoreDataMapper,
                                          "map_off_row_to_ecoscore_data",
                                          return_value=None):
                            result = product_mapper.map_off_row_to_product(row, header)

    assert result.category_en == "en:cereals"


def test_should_return_mapped_category_in_product_for_off_dict(product_mapper):
    off_dict = {"countries": "Canada", "code": "195", "product_name": "Super bars", "generic_name": "bars", "categories": ["en:cereals"], "nova_group": 4,
                "pnns_groups_1": "bars", "additives_n": 4}
    product_mapper.food_category_model.get_off_category.return_value = "en:cereals"
    product_mapper.ingredients_mapper.map_off_dict_to_ingredients.return_value = None
    product_mapper.nutriscore_data_mapper.map_off_dict_to_nutriscore_data.return_value = None

    with patch.object(BrandsMapper,
                      "map_off_dict_to_brands",
                      return_value=[]):
        with patch.object(BrandsMapper,
                          "map_off_dict_to_brand_owner",
                          return_value=""):
            with patch.object(FoodGroupsMapper,
                              "map_off_dict_to_food_groups",
                              return_value=[]):
                with patch.object(NutritionFactsMapper,
                                  "map_off_dict_to_nutrition_facts",
                                  return_value=None):
                    with patch.object(AllergensMapper,
                                      "map_off_dict_to_allergens",
                                      return_value=[]):
                        with patch.object(EcoscoreDataMapper,
                                          "map_off_dict_to_ecoscore_data",
                                          return_value=None):
                            result = product_mapper.map_off_dict_to_product(off_dict)

    assert result.category_en == "en:cereals"
