from unittest.mock import patch, mock_open

import pytest

from domain.utils.category_creator import CategoryCreator


@pytest.fixture
def category_creator():
    category_creator = CategoryCreator()
    return category_creator


@pytest.fixture
def categories_content():
    lines_starting_by_english_language = ["en: Shortbread cookie with apple\n", "en: Gingerbreads, gingerbread\n"]
    lines_starting_by_english_language_as_tags = ["en:shortbread-cookie-with-apple", "en:gingerbreads", "en:gingerbread"]

    lines_starting_by_other_languages = ["fr: Sablés aux pommes\n", "ca: Pa de gingebre\n", "de: Lebkuchen\n"]
    lines_starting_by_other_languages_as_tags = ["fr:sables-aux-pommes", "ca:pa-de-gingebre", "de:lebkuchen"]

    categories_content = ("synonyms:en: flavoured, flavored\n"
                          "stopwords:fr: aux, au, de, le, du, la, a, et, avec, base\n"
                          "stopwords:ca: als, a les, de, el, del, de la, la, té, i, amb, base\n"
                          "### Properties for categories entries\n"
                          "# add following tag for category having always same nutriscore grade\n"
                          "< en:Shortbread cookies\n" +
                          lines_starting_by_english_language[0] +
                          lines_starting_by_other_languages[0] +
                          "agribalyse_food_code:en: 24072\n"
                          "ciqual_food_code:en: 24072\n"
                          "\n"
                          "< en:Biscuits and cakes\n" +
                          lines_starting_by_english_language[1] +
                          lines_starting_by_other_languages[1] +
                          lines_starting_by_other_languages[2] +
                          "wikidata:en: Q178600")

    return categories_content, lines_starting_by_english_language_as_tags, lines_starting_by_other_languages_as_tags


def test_should_only_keep_first_english_terms_as_keys_in_categories(category_creator, categories_content):
    content_to_read, english_tags, other_tags = categories_content

    with patch("builtins.open", mock_open(read_data=content_to_read)):
        result = category_creator.create_categories("mock_categories_content.txt")

    assert english_tags[0] in result.keys()
    assert english_tags[1] in result.keys()
    assert other_tags[0] not in result.keys()
    assert other_tags[1] not in result.keys()
    assert other_tags[2] not in result.keys()


def test_should_keep_all_english_terms_as_values_with_corresponding_first_term_in_categories(category_creator, categories_content):
    content_to_read, english_tags, _ = categories_content

    with patch("builtins.open", mock_open(read_data=content_to_read)):
        result = category_creator.create_categories("mock_categories_content.txt")

    assert english_tags[0] in result[english_tags[0]]
    assert english_tags[1] in result[english_tags[1]]
    assert english_tags[2] in result[english_tags[1]]


