import pytest
from domain.validator.nova_data_validator import NovaDataValidator


@pytest.fixture
def nova_data_validator():
    return NovaDataValidator()


def test_should_return_true_for_raw_nova_group(nova_data_validator):
    nova_group = "1"

    result = nova_data_validator.check_nova_raw_group(nova_group)

    assert result is True


def test_should_return_false_for_not_raw_nova_group(nova_data_validator):
    nova_group = "2"

    result = nova_data_validator.check_nova_raw_group(nova_group)

    assert result is False


def test_should_throw_error_for_invalid_raw_nova_group(nova_data_validator):
    nova_group = "a"

    with pytest.raises(ValueError):
        nova_data_validator.check_nova_raw_group(nova_group)


def test_should_return_true_for_transformed_group(nova_data_validator):
    nova_group = "4"

    result = nova_data_validator.check_nova_transformed_group(nova_group)

    assert result is True


def test_should_return_false_for_not_transformed_nova_group(nova_data_validator):
    nova_group = "2"

    result = nova_data_validator.check_nova_transformed_group(nova_group)

    assert result is False


def test_should_throw_error_for_invalid_transformed_nova_group(nova_data_validator):
    nova_group = "a"

    with pytest.raises(ValueError):
        nova_data_validator.check_nova_transformed_group(nova_group)
