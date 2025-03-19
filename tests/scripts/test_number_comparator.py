import pytest

from scripts.number_comparator import NumberComparator

NUMBER = 2
SAME_NUMBER = 2
DIFFERENT_NUMBER = 1
RATIO_NUMERATOR = 10
RATIO_DENOMINATOR = 50
SAME_RATIO_NUMERATOR = 40
SAME_RATIO_DENOMINATOR = 200
OTHER_RATIO_NUMERATOR = 3
OTHER_RATIO_DENOMINATOR = 10

@pytest.fixture
def number_comparator():
    return NumberComparator()

def test_should_return_true_when_is_the_same_number(number_comparator):
    assert number_comparator.is_same_number(NUMBER, SAME_NUMBER) is True


def test_should_return_false_when_number_is_different(number_comparator):
    assert number_comparator.is_same_number(NUMBER, DIFFERENT_NUMBER) is False


def test_should_return_true_when_ratio_are_equal(number_comparator):
    assert number_comparator.check_value_per_100g(RATIO_NUMERATOR, RATIO_DENOMINATOR, SAME_RATIO_NUMERATOR, SAME_RATIO_DENOMINATOR) is True  


def test_should_return_false_when_ratio_are_not_equal(number_comparator):
    assert number_comparator.check_value_per_100g(RATIO_NUMERATOR, RATIO_DENOMINATOR, OTHER_RATIO_NUMERATOR, OTHER_RATIO_DENOMINATOR) is False

    
def test_should_raise_error_when_dividing_by_zero(number_comparator):
    with pytest.raises(ZeroDivisionError):
        number_comparator.check_value_per_100g(RATIO_NUMERATOR, 0, RATIO_NUMERATOR, RATIO_DENOMINATOR)
    
    with pytest.raises(ZeroDivisionError):
        number_comparator.check_value_per_100g(RATIO_NUMERATOR, RATIO_DENOMINATOR, RATIO_NUMERATOR, 0)

