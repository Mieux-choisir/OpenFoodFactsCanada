import pytest
from unittest.mock import MagicMock, mock_open, patch
from domain.mapper.ecoscore_data_mapper import EcoscoreDataMapper
from domain.mapper.ingredients_origins_mapper import IngredientsOriginMapper
from domain.mapper.packaging_mapper import PackagingMapper
from domain.mapper.production_system_mapper import ProductionSystemMapper
from domain.product.complexFields.ingredients_origins import IngredientsOrigins
from domain.product.complexFields.packaging import Packaging
from domain.product.complexFields.production_system import ProductionSystem


@pytest.fixture
def ecoscore_data_mapper():
    return EcoscoreDataMapper()


@pytest.fixture
def mock_off_row_functions(ecoscore_data_mapper):
    origins = IngredientsOrigins(
        origins=["Canada"], percent="50", transportation_score="4"
    )
    packaging = MagicMock(spec=Packaging)
    production_system = MagicMock(spec=ProductionSystem)

    with patch.object(
        IngredientsOriginMapper,
        "map_off_row_to_ingredients_origin",
        return_value=origins,
    ):
        with patch.object(
            PackagingMapper, "map_off_row_to_packaging", return_value=packaging
        ):
            with patch.object(
                ProductionSystemMapper,
                "map_off_row_to_production_system",
                return_value=production_system,
            ):
                yield {
                    "origins": origins,
                    "packaging": packaging,
                    "production_system": production_system,
                }


@pytest.fixture
def mock_off_dict_functions(ecoscore_data_mapper):
    origins = IngredientsOrigins(
        origins=["Canada"], percent="50", transportation_score="4"
    )
    packaging = MagicMock(spec=Packaging)
    production_system = MagicMock(spec=ProductionSystem)

    with patch.object(
        IngredientsOriginMapper,
        "map_off_dict_to_ingredients_origin",
        return_value=origins,
    ):
        with patch.object(
            PackagingMapper, "map_off_dict_to_packaging", return_value=packaging
        ):
            with patch.object(
                ProductionSystemMapper,
                "map_off_dict_to_production_system",
                return_value=production_system,
            ):
                yield {
                    "origins": origins,
                    "packaging": packaging,
                    "production_system": production_system,
                }


# ----------------------------------------------------------------
# Tests map_off_row_to_ecoscore_data
# ----------------------------------------------------------------


def test_should_return_round_down_int_with_given_float_score_value_in_ecoscore_data_for_given_off_row(
    ecoscore_data_mapper, mock_off_row_functions
):
    row = [46.7]
    header = ["environmental_score_score"]

    result = ecoscore_data_mapper.map_off_row_to_ecoscore_data(row, header)

    assert result.score == 46, f"Expected score of {46}, got {result.score}"


def test_should_return_correct_given_int_score_value_in_ecoscore_data_for_given_off_row(
    ecoscore_data_mapper, mock_off_row_functions
):
    row = [18]
    header = ["environmental_score_score"]

    result = ecoscore_data_mapper.map_off_row_to_ecoscore_data(row, header)

    assert result.score == 18, f"Expected score of {18}, got {result.score}"


def test_should_return_correct_origins_in_ecoscore_data_for_given_off_row(
    ecoscore_data_mapper, mock_off_row_functions
):
    row = [18]
    header = ["environmental_score_score"]

    result = ecoscore_data_mapper.map_off_row_to_ecoscore_data(row, header)

    assert (
        result.ingredients_origins == mock_off_row_functions["origins"]
    ), f"Expected origins of {mock_off_row_functions["origins"]}, got {result.ingredients_origins}"


def test_should_return_correct_packaging_in_ecoscore_data_for_given_off_row(
    ecoscore_data_mapper, mock_off_row_functions
):
    row = [18]
    header = ["environmental_score_score"]

    result = ecoscore_data_mapper.map_off_row_to_ecoscore_data(row, header)

    assert (
        result.packaging == mock_off_row_functions["packaging"]
    ), f"Expected packaging of {mock_off_row_functions["packaging"]}, got {result.packaging}"


def test_should_return_correct_production_system_in_ecoscore_data_for_given_off_row(
    ecoscore_data_mapper, mock_off_row_functions
):
    row = [18]
    header = ["environmental_score_score"]

    result = ecoscore_data_mapper.map_off_row_to_ecoscore_data(row, header)

    assert (
        result.production_system == mock_off_row_functions["production_system"]
    ), f"Expected production system of {mock_off_row_functions["production_system"]}, got {result.production_system}"


def test_should_return_empty_threatened_species_in_ecoscore_data_for_given_off_row(
    ecoscore_data_mapper, mock_off_row_functions
):
    row = [18]
    header = ["environmental_score_score"]

    result = ecoscore_data_mapper.map_off_row_to_ecoscore_data(row, header)

    assert (
        result.threatened_species == {}
    ), f"Expected empty threatened species, got {result.threatened_species}"


# ----------------------------------------------------------------
# Tests map_off_dict_to_ecoscore_data
# ----------------------------------------------------------------


def test_should_return_round_down_int_with_given_float_score_value_in_ecoscore_data_for_given_off_dict(
    ecoscore_data_mapper, mock_off_dict_functions
):
    off_dict = {"environmental_score_score": 46.7}

    result = ecoscore_data_mapper.map_off_dict_to_ecoscore_data(off_dict)

    assert result.score == 46, f"Expected score of {46}, got {result.score}"


def test_should_return_correct_given_int_score_value_in_ecoscore_data_for_given_off_dict(
    ecoscore_data_mapper, mock_off_dict_functions
):
    off_dict = {"environmental_score_score": 18}

    result = ecoscore_data_mapper.map_off_dict_to_ecoscore_data(off_dict)

    assert result.score == 18, f"Expected score of {18}, got {result.score}"


def test_should_return_correct_origins_in_ecoscore_data_for_given_off_dict(
    ecoscore_data_mapper, mock_off_dict_functions
):
    off_dict = {"environmental_score_score": 18}

    result = ecoscore_data_mapper.map_off_dict_to_ecoscore_data(off_dict)

    assert (
        result.ingredients_origins == mock_off_dict_functions["origins"]
    ), f"Expected origins of {mock_off_dict_functions["origins"]}, got {result.ingredients_origins}"


def test_should_return_correct_packaging_in_ecoscore_data_for_given_off_dict(
    ecoscore_data_mapper, mock_off_dict_functions
):
    off_dict = {"environmental_score_score": 18}

    result = ecoscore_data_mapper.map_off_dict_to_ecoscore_data(off_dict)

    assert (
        result.packaging == mock_off_dict_functions["packaging"]
    ), f"Expected packaging of {mock_off_dict_functions["packaging"]}, got {result.packaging}"


def test_should_return_correct_production_system_in_ecoscore_data_for_given_off_dict(
    ecoscore_data_mapper, mock_off_dict_functions
):
    off_dict = {"environmental_score_score": 18}

    result = ecoscore_data_mapper.map_off_dict_to_ecoscore_data(off_dict)

    assert (
        result.production_system == mock_off_dict_functions["production_system"]
    ), f"Expected production system of {mock_off_dict_functions["production_system"]}, got {result.production_system}"


def test_should_return_empty_threatened_species_in_ecoscore_data_for_given_off_dict(
    ecoscore_data_mapper, mock_off_dict_functions
):
    off_dict = {"environmental_score_score": 18}

    result = ecoscore_data_mapper.map_off_dict_to_ecoscore_data(off_dict)

    assert (
        result.threatened_species == {}
    ), f"Expected empty threatened species, got {result.threatened_species}"
