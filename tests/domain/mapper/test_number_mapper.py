import pytest
from domain.mapper.number_mapper import NumberMapper


@pytest.fixture
def number_mapper():
    return NumberMapper()


def test_should_convert_lowercase_letter_to_number(number_mapper):
    letter = "a"

    result = number_mapper.map_letter_to_number(letter)

    assert result == 1


def test_should_convert_uppercase_letter_to_number(number_mapper):
    letter = "A"

    result = number_mapper.map_letter_to_number(letter)

    assert result == 1


def test_should_return_none_for_non_alphabetic_character(number_mapper):
    letter = "1"

    result = number_mapper.map_letter_to_number(letter)

    assert result is None


def test_should_return_none_for_empty_string(number_mapper):
    letter = ""

    result = number_mapper.map_letter_to_number(letter)

    assert result is None


def test_should_return_none_for_none_input(number_mapper):
    letter = None

    result = number_mapper.map_letter_to_number(letter)

    assert result is None
