from unittest.mock import patch, mock_open

import pytest

from domain.utils.category_creator import CategoryCreator


@pytest.fixture
def category_creator():
    category_creator = CategoryCreator()
    return category_creator


@pytest.fixture
def categories_content():
    first_lines_for_terms = [
        "en: Shortbread cookie with apple\n",
        "en: Gingerbreads, gingerbread\n",
        "it: Grappa della Valle d'Aosta\n",
    ]
    first_tags_for_terms = [
        "en:shortbread-cookie-with-apple",
        "en:gingerbreads",
        "it:grappa-della-valle-d'aosta",
    ]

    following_lines_for_terms = [
        "fr: Sablés aux pommes\n",
        "ca: Pa de gingebre\n",
        "de: Lebkuchen\n",
        "fr: Grappa de la Vallée d'Aoste\n",
    ]
    following_tags_for_terms = [
        "fr:sablés-aux-pommes",
        "en:gingerbread",
        "ca:pa-de-gingebre",
        "de:lebkuchen",
        "fr:grappa-de-la-vallée-d'aoste",
    ]

    categories_content = (
        "synonyms:en: flavoured, flavored\n"
        "stopwords:fr: aux, au, de, le, du, la, a, et, avec, base\n"
        "stopwords:ca: als, a les, de, el, del, de la, la, té, i, amb, base\n"
        "### Properties for categories entries\n"
        "# add following tag for category having always same nutriscore grade\n"
        "< en:Shortbread cookies\n"
        + first_lines_for_terms[0]
        + following_lines_for_terms[0]
        + "agribalyse_food_code:en: 24072\n"
        "ciqual_food_code:en: 24072\n"
        "\n"
        "< en:Biscuits and cakes\n"
        + first_lines_for_terms[1]
        + following_lines_for_terms[1]
        + following_lines_for_terms[2]
        + "wikidata:en: Q178600\n"
        "\n"
        "< en:Italian grape marc spirit or grape marc\n"
        + first_lines_for_terms[2]
        + following_lines_for_terms[3]
        + "origins:en: en:italy\n"
    )

    return categories_content, first_tags_for_terms, following_tags_for_terms


def test_should_only_keep_first_appearing_tag_for_each_term_in_paragraphs_as_keys_in_categories(
    category_creator, categories_content
):
    content_to_read, first_tags_for_terms, following_tags_for_terms = categories_content

    with patch("builtins.open", mock_open(read_data=content_to_read)):
        result = category_creator.create_categories("mock_categories_content.txt")

    assert first_tags_for_terms[0] in result.keys()
    assert first_tags_for_terms[1] in result.keys()
    assert first_tags_for_terms[2] in result.keys()
    assert following_tags_for_terms[0] not in result.keys()
    assert following_tags_for_terms[1] not in result.keys()
    assert following_tags_for_terms[2] not in result.keys()
    assert following_tags_for_terms[3] not in result.keys()
    assert following_tags_for_terms[4] not in result.keys()


def test_should_keep_all_tags_for_each_term_as_values_with_corresponding_first_term_in_categories(
    category_creator, categories_content
):
    content_to_read, first_tags_for_terms, following_tags_for_terms = categories_content

    with patch("builtins.open", mock_open(read_data=content_to_read)):
        result = category_creator.create_categories("mock_categories_content.txt")

    assert first_tags_for_terms[0] in result[first_tags_for_terms[0]]
    assert following_tags_for_terms[0] in result[first_tags_for_terms[0]]
    assert first_tags_for_terms[1] in result[first_tags_for_terms[1]]
    assert following_tags_for_terms[1] in result[first_tags_for_terms[1]]
    assert following_tags_for_terms[2] in result[first_tags_for_terms[1]]
    assert following_tags_for_terms[3] in result[first_tags_for_terms[1]]
    assert first_tags_for_terms[2] in result[first_tags_for_terms[2]]
    assert following_tags_for_terms[4] in result[first_tags_for_terms[2]]
