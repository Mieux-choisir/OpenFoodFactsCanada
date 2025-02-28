import pytest
from domain.validator.product_validator import ProductValidator


@pytest.fixture
def product_validator():
    return ProductValidator()


def test_should_return_true_for_valid_pnn_group(product_validator):
    pnn = "cereals"

    result = product_validator.check_pnn_groups(pnn)

    assert result is True


def test_should_return_false_for_invalid_pnn_group(product_validator):
    pnn = "meat"

    result = product_validator.check_pnn_groups(pnn)

    assert result is False


def test_should_return_true_for_raw_food_category(product_validator):
    category = "en:vegetables"

    result = product_validator.check_string_categories(category)

    assert result is True


def test_should_return_false_for_transformed_food_category(product_validator):
    category = "en:snacks"

    result = product_validator.check_string_categories(category)

    assert result is False


def test_should_return_false_for_mixed_food_category(product_validator):
    category = "en:vegetables,en:snacks"

    result = product_validator.check_string_categories(category)

    assert result is False


def test_should_return_true_for_raw_food_category_list(product_validator):
    category = ["en:vegetables"]

    result = product_validator.check_list_categories(category)

    assert result is True


def test_should_return_false_for_transformed_food_category_list(product_validator):
    category = ["en:snacks"]

    result = product_validator.check_list_categories(category)

    assert result is False


def test_should_return_false_for_mixed_food_category_list(product_validator):
    category = ["en:vegetables", "en:snacks"]

    result = product_validator.check_list_categories(category)

    assert result is False


def test_should_return_true_for_zero_additives_and_low_nova_group(product_validator):
    additives = "0"
    nova_group = "2"

    result = product_validator.check_additives(additives, nova_group)

    assert result is True


def test_should_return_false_for_zero_additives_and_high_nova_group(product_validator):
    additives = "0"
    nova_group = "3"

    result = product_validator.check_additives(additives, nova_group)

    assert result is False


def test_should_return_false_for_nonzero_additives(product_validator):
    additives = "1"
    nova_group = "2"

    result = product_validator.check_additives(additives, nova_group)

    assert result is False
