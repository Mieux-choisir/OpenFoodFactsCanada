import pytest

from domain.mapper.food_groups_mapper import FoodGroupsMapper


@pytest.fixture
def food_groups_mapper():
    food_groups_mapper = FoodGroupsMapper()

    return food_groups_mapper


@pytest.fixture
def off_rows():
    row = ["group1, groUP2,"]
    header = ["food_groups_en"]

    return row, header


@pytest.fixture
def off_empty_rows():
    row = [""]
    header = ["food_groups_en"]

    return row, header


@pytest.fixture
def off_dict():
    off_dict = {"food_groups_en": "group1, groUP2,"}

    return off_dict


@pytest.fixture
def off_empty_dict():
    off_dict = {"food_groups_en": None}

    return off_dict


# ----------------------------------------------------------------
# Tests map_off_row_to_food_groups
# ----------------------------------------------------------------

def test_should_return_correctly_split_food_groups_list_for_given_off_row(food_groups_mapper, off_rows):
    row, header = off_rows

    result = food_groups_mapper.map_off_row_to_food_groups(row, header)

    expected_result = [x.strip() for x in row[header.index("food_groups_en")].lower().split(",") if x.strip() != ""]
    assert (
            result == expected_result
    ), f"Expected result food groups list to be {expected_result}, got {result}"


def test_should_return_empty_food_groups_list_for_given_off_row(food_groups_mapper, off_empty_rows):
    row, header = off_empty_rows

    result = food_groups_mapper.map_off_row_to_food_groups(row, header)

    assert (
            result == []
    ), f"Expected result food groups list to be {[]}, got {result}"


# ----------------------------------------------------------------
# Tests map_off_row_to_food_groups
# ----------------------------------------------------------------

def test_should_return_correctly_split_food_groups_list_for_given_off_dict(food_groups_mapper, off_dict):
    result = food_groups_mapper.map_off_dict_to_food_groups(off_dict, "food_groups_en")

    expected_result = [x.strip() for x in off_dict["food_groups_en"].lower().split(",") if x.strip() != ""]
    assert (
            result == expected_result
    ), f"Expected result food groups list to be {expected_result}, got {result}"


def test_should_return_empty_food_groups_list_for_given_off_dict(food_groups_mapper, off_empty_dict):
    result = food_groups_mapper.map_off_dict_to_food_groups(off_empty_dict, "food_groups_en")

    assert (
            result == []
    ), f"Expected result food groups list to be {[]}, got {result}"