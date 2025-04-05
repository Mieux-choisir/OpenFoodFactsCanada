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
        "category1": {
            "values": ["category1", "other-category1"],
            "parents": ["parent1", "parent2"],
        },
        "category2": {"values": ["category2"], "parents": []},
        "category3": {"values": ["category3"], "parents": ["category2"]},
        "category4": {"values": ["category4"], "parents": ["category2"]},
    }
    category_creator.create_fdc_to_off_categories_mapping.return_value = {
        "fdc-category-1": ["other-category1"],
        "fdc-category-2": ["category2", "category3"],
    }

    category_mapper = CategoryMapper(
        category_creator, "taxonomy_file.txt", "mapping_file.txt"
    )

    return category_mapper


# ----------------------------------------------------------------
# Tests get_off_categories_of_off_product
# ----------------------------------------------------------------


def test_should_return_other_category_for_absent_category_in_off_categories(
    category_mapper,
):
    absent_category = "absent-category"

    result = category_mapper.get_off_categories_of_off_product(absent_category)

    assert result == ["en:other"]


def test_should_return_corresponding_category_in_for_found_category_in_off_categories(
    category_mapper,
):
    present_category = "other-category1"

    result = category_mapper.get_off_categories_of_off_product(present_category)

    assert result == ["category1"]


def test_should_return_only_most_precise_categories_for_found_categories_in_hierarchical_order_in_off_categories(
    category_mapper,
):
    present_categories = "other-category1, category2, category3, category4"

    result = category_mapper.get_off_categories_of_off_product(present_categories)

    assert result.sort() == ["category3", "category4"].sort()


# ----------------------------------------------------------------
# Tests get_off_categories_of_fdc_product
# ----------------------------------------------------------------


def test_should_return_fdc_category_with_fdc_at_the_end_for_absent_category_in_off(
    category_mapper,
):
    absent_category = "Ketchup - Mustard, BBQ & Cheese   Sauce (Shelf Stable)"

    result = category_mapper.get_off_categories_of_fdc_product(absent_category)

    expected_category = "en:ketchup-mustard-bbq-cheese-sauce-shelf-stable-fdc"
    assert result == [expected_category]


def test_should_return_matched_off_category_for_given_fdc_category(category_mapper):
    present_category = "fdc-category-1"

    result = category_mapper.get_off_categories_of_fdc_product(present_category)

    assert result == ["category1"]
