import re
from unittest.mock import patch, mock_open, MagicMock

import pytest

from domain.product.complexFields.ingredients import Ingredients
from domain.product.complexFields.nova_data import NovaData
from domain.product.product import Product
from scripts.csv_creator import CsvCreator


@pytest.fixture
def csv_creator():
    csv_creator = CsvCreator("path")

    return csv_creator


@pytest.fixture
def products():
    product1 = Product(
        id_match="00145887",
        product_name="Product 1",
        ingredients=Ingredients(ingredients_text="ingredient1, ingredient2"),
        nova_data=NovaData(),
    )
    product2 = Product(
        id_match="55555555",
        product_name="Product 2",
        brands=["brand1", "brand2"],
        off_categories_en=["category1", "category2"],
        ingredients=Ingredients(),
        nova_data=NovaData(score="3"),
    )

    return [product1, product2]


@pytest.fixture
def products_mapped_lists(csv_creator, products):
    columns_list = (
        csv_creator.mandatory_columns
        + csv_creator.recommended_columns
        + csv_creator.optional_columns
    )

    id_match_id = columns_list.index(
        csv_creator.product_field_to_columns_mapping.get("id_match")
    )
    product_name_id = columns_list.index(
        csv_creator.product_field_to_columns_mapping.get("product_name")
    )
    ingredients_text_id = columns_list.index(
        csv_creator.product_field_to_columns_mapping.get("ingredients.ingredients_text")
    )
    brands_id = columns_list.index(
        csv_creator.product_field_to_columns_mapping.get("brands")
    )
    category_id = columns_list.index(
        csv_creator.product_field_to_columns_mapping.get("off_categories_en")
    )
    nova_data_score_id = columns_list.index(
        csv_creator.product_field_to_columns_mapping.get("nova_data.score")
    )
    language_id = columns_list.index("Main language")

    mapped_lists = []
    for product in products:
        expected_added_list = [""] * len(columns_list)
        expected_added_list[id_match_id] = (
            product.id_match if product.id_match is not None else ""
        )
        expected_added_list[product_name_id] = (
            product.product_name if product.product_name is not None else ""
        )
        expected_added_list[ingredients_text_id] = (
            product.ingredients.ingredients_text
            if product.ingredients.ingredients_text is not None
            else ""
        )
        expected_added_list[category_id] = (
            ", ".join(product.off_categories_en)
            if product.off_categories_en is not None
            else ""
        )
        expected_added_list[nova_data_score_id] = (
            str(product.nova_data.score) if product.nova_data.score is not None else ""
        )
        expected_added_list[language_id] = "English"

        expected_added_list[brands_id] = ""
        if product.brands:
            for brand in product.brands:
                expected_added_list[brands_id] += brand + ", "
        expected_added_list[brands_id] = expected_added_list[brands_id][:-2]

        mapped_lists.append(expected_added_list)

    return mapped_lists


def test_should_open_csv_file_with_correct_path(csv_creator):
    open_mock = mock_open()

    with patch("builtins.open", open_mock):
        csv_creator.create_csv_files_for_products_not_existing_in_off([Product()], [])

    assert re.match(
        r".*path_1\.csv", open_mock.call_args[0][0]
    ), f"Expected file path to match pattern, but got {open_mock.call_args[0][0]}"


def test_should_open_csv_file_with_correct_parameters(csv_creator):
    open_mock = mock_open()

    with patch("builtins.open", open_mock):
        csv_creator.create_csv_files_for_products_not_existing_in_off([Product()], [])

    open_mock.assert_called_with(
        open_mock.call_args[0][0], "w", encoding="utf-8", newline=""
    )


def test_should_write_correct_headers_line_in_csv_file(csv_creator):
    open_mock = mock_open()
    mock_filewriter = MagicMock()

    with patch("csv.writer", return_value=mock_filewriter):
        with patch("builtins.open", open_mock):
            csv_creator.create_csv_files_for_products_not_existing_in_off(
                [Product()], []
            )

    mock_filewriter.writerow.assert_any_call(
        csv_creator.mandatory_columns
        + csv_creator.recommended_columns
        + csv_creator.optional_columns
    )


def test_should_write_correctly_formatted_lines_only_for_products_with_ids_to_add_in_csv_file(
    csv_creator, products, products_mapped_lists
):
    open_mock = mock_open()
    mock_filewriter = MagicMock()

    with patch("csv.writer", return_value=mock_filewriter):
        with patch("builtins.open", open_mock):
            csv_creator.create_csv_files_for_products_not_existing_in_off(
                products, [products[0].id_match]
            )

    mock_filewriter.writerow.assert_called_with(products_mapped_lists[1])

    assert mock_filewriter.writerow.call_count == 2
