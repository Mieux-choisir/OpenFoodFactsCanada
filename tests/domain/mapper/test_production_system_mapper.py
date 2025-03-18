import pytest

from domain.mapper.production_system_mapper import ProductionSystemMapper


@pytest.fixture
def production_system_mapper():
    return ProductionSystemMapper()


# ----------------------------------------------------------------
# Tests map_off_dict_to_production_system
# ----------------------------------------------------------------


def test_should_return_given_labels_in_production_system_for_given_off_dict(
    production_system_mapper,
):
    off_dict = {"labels_tags": ["en:organic", "en:no-gmos", "en:non-gmo-project"]}

    result = production_system_mapper.map_off_dict_to_production_system(off_dict)

    assert (
        result.labels == off_dict["labels_tags"]
    ), f"Expected labels field to be {off_dict["labels_tags"]}, got {result.labels}"


def test_should_return_empty_labels_list_for_absent_labels_tags_in_production_system_for_given_off_dict(
    production_system_mapper,
):
    off_dict = {"labels_tags": None}

    result = production_system_mapper.map_off_dict_to_production_system(off_dict)

    assert result.labels == [], f"Expected labels field to be {[]}, got {result.labels}"


def test_should_return_empty_value_field_in_production_system_for_given_off_dict(
    production_system_mapper,
):
    off_dict = {"labels_tags": ["en:organic", "en:no-gmos", "en:non-gmo-project"]}

    result = production_system_mapper.map_off_dict_to_production_system(off_dict)

    assert (
        result.value is None
    ), f"Expected value field to be {None}, got {result.value}"


def test_should_return_empty_warning_field_in_production_system_for_given_off_dict(
    production_system_mapper,
):
    off_dict = {"labels_tags": ["en:organic", "en:no-gmos", "en:non-gmo-project"]}

    result = production_system_mapper.map_off_dict_to_production_system(off_dict)

    assert (
        result.warning is None
    ), f"Expected warning field to be {None}, got {result.warning}"


# ----------------------------------------------------------------
# Tests map_off_row_to_production_system
# ----------------------------------------------------------------


def test_should_return_given_labels_in_production_system_for_given_off_row(
    production_system_mapper,
):
    header = ["labels"]
    row = ["en:organic, en:no-gmos, en:non-gmo-project"]

    result = production_system_mapper.map_off_row_to_production_system(row, header)

    expected_result = [x.strip() for x in row[0].split(",") if x.strip() != ""]
    assert (
        result.labels == expected_result
    ), f"Expected labels field to be {expected_result}, got {result.labels}"


def test_should_return_empty_labels_list_for_absent_labels_tags_in_production_system_for_given_off_row(
    production_system_mapper,
):
    header = ["labels"]
    row = [""]

    result = production_system_mapper.map_off_row_to_production_system(row, header)

    assert result.labels == [], f"Expected labels field to be {[]}, got {result.labels}"


def test_should_return_empty_value_field_in_production_system_for_given_off_row(
    production_system_mapper,
):
    header = ["labels"]
    row = ["en:organic, en:no-gmos, en:non-gmo-project"]

    result = production_system_mapper.map_off_row_to_production_system(row, header)

    assert (
        result.value is None
    ), f"Expected value field to be {None}, got {result.value}"


def test_should_return_empty_warning_field_in_production_system_for_given_off_row(
    production_system_mapper,
):
    header = ["labels"]
    row = ["en:organic, en:no-gmos, en:non-gmo-project"]

    result = production_system_mapper.map_off_row_to_production_system(row, header)

    assert (
        result.warning is None
    ), f"Expected warning field to be {None}, got {result.warning}"
