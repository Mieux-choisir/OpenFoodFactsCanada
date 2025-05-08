import pytest

from domain.mapper.brands_mapper import BrandsMapper


@pytest.fixture
def brands_mapper():
    return BrandsMapper()


@pytest.fixture
def off_dict():
    off_dict = {"brands": " brand1, BRAND2", "brand_owner": "brand1 "}

    return off_dict


@pytest.fixture
def off_empty_dict():
    off_dict = {"brands": None, "brand_owner": None}

    return off_dict


@pytest.fixture
def off_empty_brand_owner_field_dict():
    off_dict = {"brands": " brand1, BRAND2", "brand_owner": None}

    return off_dict


# ----------------------------------------------------------------
# Tests map_off_dict_to_brands
# ----------------------------------------------------------------


def test_should_return_empty_brands_list_for_empty_brands_field_in_row_for_given_off_dict(
    brands_mapper, off_empty_dict
):
    result = brands_mapper.map_off_dict_to_brands(off_empty_dict, "brands")

    assert result == [], f"Expected result brands to be {[]}, got {result}"


def test_should_return_correct_brands_list_for_given_brands_field_in_row_for_given_off_dict(
    brands_mapper, off_dict
):
    result = brands_mapper.map_off_dict_to_brands(off_dict, "brands")

    expected_result = [
        x.strip() for x in off_dict["brands"].title().split(",") if x.strip() != ""
    ]
    assert (
        result == expected_result
    ), f"Expected result brands to be {expected_result}, got {result}"


# ----------------------------------------------------------------
# Tests map_off_dict_to_brand_owner
# ----------------------------------------------------------------


def test_should_return_no_brand_owner_for_empty_brands_and_brand_owner_fields_in_row_for_given_off_dict(
    brands_mapper, off_empty_dict
):
    result = brands_mapper.map_off_dict_to_brand_owner(
        off_empty_dict, "brand_owner", "brands"
    )

    assert result is None, f"Expected result brand owner to be {None}, got {result}"


def test_should_return_brand_owner_field_for_not_empty_brand_owner_field_in_row_for_given_off_dict(
    brands_mapper, off_dict
):
    result = brands_mapper.map_off_dict_to_brand_owner(
        off_dict, "brand_owner", "brands"
    )

    assert (
        result == off_dict["brand_owner"].title().strip()
    ), f"Expected result brand owner to be {off_dict['brand_owner'].title().strip()}, got {result}"


def test_should_return_brands_field_for_empty_brand_owner_field_and_not_empty_brands_field_in_row_for_given_off_dict(
    brands_mapper, off_empty_brand_owner_field_dict
):
    result = brands_mapper.map_off_dict_to_brand_owner(
        off_empty_brand_owner_field_dict, "brand_owner", "brands"
    )

    assert (
        result == off_empty_brand_owner_field_dict["brands"].title().strip()
    ), f"Expected result brand owner to be {off_empty_brand_owner_field_dict['brands'].title().strip()}, got {result}"
