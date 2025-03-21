import pytest

from scripts.string_comparator import StringComparator

STRING = "TEXT"
DIFFERENT_STRING = "DIFFERENT_TEXT"
SAME_STRING_CASE_INSENSITIVE = "tExT"
SAME_STRING_WHITESPACE_INSENSITIVE = "TE X\nT"
SAME_STRING_ACCENT_INSENSITIVE = "TÉXT"
LIST = ["a", "b", "c", "d"]
SHORT_LIST = ["a", "b", "c"]
DIFFERENT_LIST_SAME_LENGTH = ["a", "b", "c", "e"]
SAME_LIST_DIFFERENT_ORDER = ["a", "d", "c", "b"]


@pytest.fixture
def string_comparator():
    return StringComparator()


def test_should_return_true_when_is_identical(string_comparator):
    assert string_comparator.is_identical(STRING, STRING) is True


def test_should_return_false_when_is_not_identical(string_comparator):
    assert string_comparator.is_identical(STRING, DIFFERENT_STRING) is False


def test_should_return_true_when_is_identical_case_insensitive(string_comparator):
    assert (
        string_comparator.is_identical_case_insensitive(
            STRING, SAME_STRING_CASE_INSENSITIVE
        )
        is True
    )


def test_should_return_false_when_is_not_identical_case_insensitive(string_comparator):
    assert (
        string_comparator.is_identical_case_insensitive(STRING, DIFFERENT_STRING)
        is False
    )


def test_should_return_true_when_is_identical_whitespace_insensitive(string_comparator):
    assert (
        string_comparator.is_identical_case_white_space(
            STRING, SAME_STRING_WHITESPACE_INSENSITIVE
        )
        is True
    )


def test_should_return_false_when_is_not_identical_whitespace_insensitive(
    string_comparator,
):
    assert (
        string_comparator.is_identical_case_white_space(STRING, DIFFERENT_STRING)
        is False
    )


def test_should_return_true_when_is_identical_accent_insensitive(string_comparator):
    assert (
        string_comparator.compare_string(STRING, SAME_STRING_ACCENT_INSENSITIVE) is True
    )


def test_should_return_false_when_is_not_identical_accent_insensitive(
    string_comparator,
):
    assert string_comparator.compare_string(STRING, DIFFERENT_STRING) is False


def test_should_return_true_when_is_list_same_length(string_comparator):
    assert (
        string_comparator.is_list_same_length(LIST, DIFFERENT_LIST_SAME_LENGTH) is True
    )


def test_should_return_false_when_is_list_not_same_length(string_comparator):
    assert string_comparator.is_list_same_length(LIST, SHORT_LIST) is False


def test_should_return_true_when_is_lists_have_same_elements(string_comparator):
    assert string_comparator.is_lists_have_same_elements(LIST, LIST) is True


def test_should_return_false_when_lists_have_different_elements(string_comparator):
    assert (
        string_comparator.is_lists_have_same_elements(LIST, DIFFERENT_LIST_SAME_LENGTH)
        is False
    )


def test_should_return_false_when_lists_have_different_orders(string_comparator):
    assert (
        string_comparator.is_lists_have_same_elements(LIST, SAME_LIST_DIFFERENT_ORDER)
        is False
    )
