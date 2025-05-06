import pytest

from domain.mapper.packaging_mapper import PackagingMapper


@pytest.fixture
def packaging_mapper():
    return PackagingMapper()


# ----------------------------------------------------------------
# Tests map_off_row_to_packaging
# ----------------------------------------------------------------


def test_should_return_empty_non_recyclable_field_in_packaging_for_given_off_row(
    packaging_mapper,
):
    row = ["plastic, bottle, glass"]
    header = ["packaging"]

    result = packaging_mapper.map_off_row_to_packaging(row, header)

    assert (
        result.non_recyclable_and_non_biodegradable_materials is None
    ), f"Expected non recyclable field to be {None}, got {result.non_recyclable_and_non_biodegradable_materials}"


def test_should_return_correctly_split_string_in_packaging_field_in_packaging_for_given_off_row(
    packaging_mapper,
):
    row = ["plastic, bottle, , glass,"]
    header = ["packaging"]

    result = packaging_mapper.map_off_row_to_packaging(row, header)

    wanted_result = ["plastic", "bottle", "glass"]
    assert (
        result.packaging == wanted_result
    ), f"Expected packaging field to be {wanted_result}, got {result.packaging}"


def test_should_return_empty_list_for_empty_string_in_packaging_field_in_packaging_for_given_off_row(
    packaging_mapper,
):
    row = [""]
    header = ["packaging"]

    result = packaging_mapper.map_off_row_to_packaging(row, header)

    assert (
        result.packaging == []
    ), f"Expected packaging field to be {[]}, got {result.packaging}"


# ----------------------------------------------------------------
# Tests map_off_dict_to_packaging
# ----------------------------------------------------------------


def test_should_return_empty_non_recyclable_field_in_packaging_for_given_off_dict(
    packaging_mapper,
):
    off_dict = {"packaging_tags": ["en:plastic", "en:bottle", "en:glass"]}

    result = packaging_mapper.map_off_dict_to_packaging(off_dict)

    assert (
        result.non_recyclable_and_non_biodegradable_materials is None
    ), f"Expected non recyclable field to be {None}, got {result.non_recyclable_and_non_biodegradable_materials}"


def test_should_return_given_list_in_packaging_field_in_packaging_for_given_off_dict(
    packaging_mapper,
):
    off_dict = {"packaging_tags": ["en:plastic", "en:bottle", "en:glass"]}

    result = packaging_mapper.map_off_dict_to_packaging(off_dict)

    assert (
        result.packaging == off_dict["packaging_tags"]
    ), f"Expected packaging field to be {off_dict['packaging_tags']}, got {result.packaging}"


def test_should_return_empty_list_for_absent_value_in_packaging_field_in_packaging_for_given_off_dict(
    packaging_mapper,
):
    off_dict = {"packaging_tags": None}

    result = packaging_mapper.map_off_dict_to_packaging(off_dict)

    assert (
        result.packaging == []
    ), f"Expected packaging field to be {[]}, got {result.packaging}"
