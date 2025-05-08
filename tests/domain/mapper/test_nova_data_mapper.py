import pytest

from domain.mapper.nova_data_mapper import NovaDataMapper


@pytest.fixture
def nova_data_mapper():
    return NovaDataMapper()


# ----------------------------------------------------------------
# Tests map_off_row_to_nova_data
# ----------------------------------------------------------------


def test_should_return_empty_score_for_absent_score_in_nova_data_for_given_off_row(
    nova_data_mapper,
):
    row = [""]
    header = ["nova_group"]

    result = nova_data_mapper.map_off_row_to_nova_data(row, header)

    assert result.score is None, f"Expected nova score to be {None}, got {result.score}"


def test_should_return_correct_score_for_present_score_in_nova_data_for_given_off_row(
    nova_data_mapper,
):
    row = ["4"]
    header = ["nova_group"]

    result = nova_data_mapper.map_off_row_to_nova_data(row, header)

    assert result.score == int(
        row[0]
    ), f"Expected nova score to be {row[0]}, got {result.score}"


def test_should_return_empty_score_for_invalid_score_in_nova_data_for_given_off_row(
    nova_data_mapper,
):
    row = ["4.5"]
    header = ["nova_group"]

    result = nova_data_mapper.map_off_row_to_nova_data(row, header)

    assert result.score is None, f"Expected nova score to be {None}, got {result.score}"


def test_should_return_empty_group_markers_in_nova_data_for_given_off_row(
    nova_data_mapper,
):
    row = ["4"]
    header = ["nova_group"]

    result = nova_data_mapper.map_off_row_to_nova_data(row, header)

    assert (
        result.group_markers == {}
    ), f"Expected group markers to be {{}}, got {result.group_markers}"


# ----------------------------------------------------------------
# Tests map_off_dict_to_nova_data
# ----------------------------------------------------------------


def test_should_return_empty_score_for_absent_score_in_nova_data_for_given_off_dict(
    nova_data_mapper,
):
    off_dict = {"nova_group": None}

    result = nova_data_mapper.map_off_dict_to_nova_data(off_dict)

    assert result.score is None, f"Expected nova score to be {None}, got {result.score}"


def test_should_return_correct_score_for_present_score_in_nova_data_for_given_off_dict(
    nova_data_mapper,
):
    off_dict = {"nova_group": 4}

    result = nova_data_mapper.map_off_dict_to_nova_data(off_dict)

    assert result.score == int(
        off_dict["nova_group"]
    ), f"Expected nova score to be {int(off_dict['nova_group'])}, got {result.score}"


def test_should_return_empty_score_for_invalid_score_in_nova_data_for_given_off_dict(
    nova_data_mapper,
):
    off_dict = {"nova_group": 3.8}

    result = nova_data_mapper.map_off_dict_to_nova_data(off_dict)

    assert result.score is None, f"Expected nova score to be {None}, got {result.score}"


def test_should_return_empty_group_markers_in_nova_data_for_given_off_dict(
    nova_data_mapper,
):
    off_dict = {"nova_group": 4}

    result = nova_data_mapper.map_off_dict_to_nova_data(off_dict)

    assert (
        result.group_markers == {}
    ), f"Expected group markers to be {{}}, got {result.group_markers}"
