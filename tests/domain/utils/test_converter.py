import pytest
from domain.utils.converter import Converter


@pytest.fixture
def converter():
    return Converter()


def test_should_convert_to_int_for_int():
    assert Converter.safe_int("123") == 123


def test_should_return_none_for_non_int():
    assert Converter.safe_int("abc") is None


def test_should_convert_to_float_for_float():
    assert Converter.safe_float("123.45") == 123.45


def test_should_return_none_for_non_float():
    assert Converter.safe_float("abc") is None
