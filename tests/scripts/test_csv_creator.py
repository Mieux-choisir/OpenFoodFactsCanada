import unittest
from unittest.mock import MagicMock, patch
from domain.product.product import Product
from scripts.csv_creator import CsvCreator


class CsvCreatorTests(unittest.TestCase):
    def test_should_create_csv_line_with_correct_values(self):
        product = Product(
            id_original="123456",
            household_serving_fulltext="1 cup",
            serving_size=250,
            serving_size_unit="ml",
            nutrition_data_per="100g",
            nutrition_facts={
                "nutrition_facts_per_hundred_grams": {
                    "fat_100g": 10.5,
                    "sugar_100g": 5.2,
                }
            },
        )
        csv_creator = CsvCreator(csv_files_base_names="test")
        columns = (
            csv_creator.mandatory_columns
            + csv_creator.recommended_columns
            + csv_creator.optional_columns
        )
        line = csv_creator._CsvCreator__create_csv_line_for_product(product, columns)
        self.assertIn("1 cup (250 ml)", line)
        self.assertIn("10.5", line)
        self.assertIn("5.2", line)

    def test_should_handle_empty_serving_size_fields(self):
        product = Product(
            id_original="123456",
            household_serving_fulltext=None,
            serving_size=None,
            serving_size_unit=None,
        )
        csv_creator = CsvCreator(csv_files_base_names="test")
        columns = (
            csv_creator.mandatory_columns
            + csv_creator.recommended_columns
            + csv_creator.optional_columns
        )
        line = csv_creator._CsvCreator__create_csv_line_for_product(product, columns)
        self.assertEqual(line[columns.index("Serving size")], "")

    def test_should_format_decimal_values_correctly(self):
        formatted_value = CsvCreator._CsvCreator__format_decimal(
            123.456789, max_decimals=2
        )
        self.assertEqual(formatted_value, "123.46")

    def test_should_skip_fields_based_on_nutrition_data_per(self):
        product = Product(
            id_original="123456",
            nutrition_data_per="100g",
            nutrition_facts={
                "nutrition_facts_per_serving": {
                    "fat_serving": 5.0,
                }
            },
        )
        csv_creator = CsvCreator(csv_files_base_names="test")
        columns = (
            csv_creator.mandatory_columns
            + csv_creator.recommended_columns
            + csv_creator.optional_columns
        )
        line = csv_creator._CsvCreator__create_csv_line_for_product(product, columns)
        self.assertNotIn("5.0", line)

    @patch("scripts.csv_creator.MongoClient")
    def test_should_create_batches_from_cursor(self, mock_mongo_client):
        mock_cursor = MagicMock()
        mock_cursor.__iter__.return_value = [{"id_original": "123"}] * 15000
        csv_creator = CsvCreator(csv_files_base_names="test")
        batches = list(
            csv_creator._CsvCreator__batched_cursor(mock_cursor, batch_size=10000)
        )
        self.assertEqual(len(batches), 2)
        self.assertEqual(len(batches[0]), 10000)
        self.assertEqual(len(batches[1]), 5000)
