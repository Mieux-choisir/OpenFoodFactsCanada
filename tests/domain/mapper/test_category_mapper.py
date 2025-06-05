from unittest.mock import MagicMock

import pytest

from domain.mapper.category_mapper import CategoryMapper
from domain.utils.category_creator import CategoryCreator


@pytest.fixture()
def category_creator():
    category_creator = MagicMock(spec=CategoryCreator)

    return category_creator


@pytest.fixture
def category_mapper(category_creator):
    category_creator.create_off_categories.return_value = {
        "en:category1": {
            "values": ["en:category1", "en:other-category1"],
            "parents": ["en:parent1", "en:parent2"],
        },
        "en:category2": {"values": ["en:category2"], "parents": []},
        "en:category3": {"values": ["en:category3"], "parents": ["en:category2"]},
        "en:category4": {"values": ["en:category4"], "parents": ["en:category2"]},
    }
    category_creator.create_fdc_to_off_categories_mapping.return_value = {
        "fdc-category-1": ["en:other-category1"],
        "fdc-category-2": ["en:category2", "en:category3"],
    }

    category_mapper = CategoryMapper(
        category_creator, "taxonomy_file.txt", "mapping_file.txt"
    )

    return category_mapper


# ----------------------------------------------------------------
# Tests get_off_categories_of_fdc_product
# ----------------------------------------------------------------


def test_should_not_return_any_category_for_no_existing_off_category_in_categories_list(
    category_mapper,
):
    absent_category = "Ketchup - Mustard, BBQ & Cheese   Sauce (Shelf Stable)"

    result = category_mapper.get_off_categories_of_fdc_product(absent_category)

    assert result == []


def test_should_return_matched_existing_off_categories_in_categories_list(
    category_mapper,
):
    present_category = "fdc-category-1"

    result = category_mapper.get_off_categories_of_fdc_product(present_category)

    assert result == ["en:category1"]
