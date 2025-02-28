import json
import pytest
from unittest.mock import MagicMock, mock_open, patch

from domain.mapper.product_mapper import ProductMapper
from domain.product.product import Product
from scripts.data_importer import DataImporter

VALID_FDC_PRODUCT_COUNT = 2
VALID_OFF_PRODUCT_COUNT = 2
LIMITED_OFF_PRODUCT_COUNT = 1

@pytest.fixture
def product_mapper():
    return MagicMock(spec=ProductMapper)

@pytest.fixture
def data_importer(product_mapper):
    return DataImporter(product_mapper)


# ----------------------------------------------------------------
# Tests import_json_fdc_data
# ----------------------------------------------------------------

def test_should_import_fdc_data_when_valid_json(data_importer):
    json_content = """
    {
        "BrandedFoods": [
            {"marketCountry": "United States", "gtinUpc": "12345"},
            {"marketCountry": "United States", "gtinUpc": "67890"}
        ]
    }
    """
    mock_product = MagicMock(spec=Product)
    data_importer.product_mapper.map_fdc_dict_to_product.return_value = mock_product

    with patch("builtins.open", mock_open(read_data=json_content)):
        result = data_importer.import_json_fdc_data("mock_file.json")

    assert len(result) == VALID_FDC_PRODUCT_COUNT, f"Expected {VALID_FDC_PRODUCT_COUNT} products, got {len(result)}"
    assert all(isinstance(p, Product) for p in result), "All returned elements should be instances of Product"

def test_should_ignore_non_us_products_in_fdc_data(data_importer):
    json_content = """
    {
        "BrandedFoods": [
            {"marketCountry": "Canada", "gtinUpc": "12345"},
            {"marketCountry": "United States", "gtinUpc": "67890"}
        ]
    }
    """
    mock_product = MagicMock(spec=Product)
    data_importer.product_mapper.map_fdc_dict_to_product.return_value = mock_product

    with patch("builtins.open", mock_open(read_data=json_content)):
        result = data_importer.import_json_fdc_data("mock_file.json")

    assert len(result) == 1, f"Expected 1 US product, but got {len(result)}"

def test_should_return_empty_list_when_fdc_file_is_empty(data_importer):
    json_content = "{}"

    with patch("builtins.open", mock_open(read_data=json_content)):
        result = data_importer.import_json_fdc_data("mock_file.json")

    assert result == [], "Expected an empty list when the FDC file is empty"


# ----------------------------------------------------------------
# Tests import_jsonl_off_data
# ----------------------------------------------------------------

def test_should_import_off_jsonl_data(data_importer):
    json_lines = '{"code": "123"}\n{"code": "456"}\n'
    mock_product = MagicMock(spec=Product)
    data_importer.product_mapper.map_off_dict_to_product.return_value = mock_product

    with patch("builtins.open", mock_open(read_data=json_lines)):
        result = data_importer.import_jsonl_off_data("mock_file.jsonl")

    assert len(result) == VALID_OFF_PRODUCT_COUNT, f"Expected {VALID_OFF_PRODUCT_COUNT} products, got {len(result)}"

def test_should_apply_limit_on_off_jsonl_data(data_importer):
    json_lines = '{"code": "123"}\n{"code": "456"}\n'
    mock_product = MagicMock(spec=Product)
    data_importer.product_mapper.map_off_dict_to_product.return_value = mock_product

    with patch("builtins.open", mock_open(read_data=json_lines)):
        result = data_importer.import_jsonl_off_data("mock_file.jsonl", limit=LIMITED_OFF_PRODUCT_COUNT)

    assert len(result) == LIMITED_OFF_PRODUCT_COUNT, f"Expected {LIMITED_OFF_PRODUCT_COUNT} products, got {len(result)}"


# ----------------------------------------------------------------
# Tests import_csv_off_data
# ----------------------------------------------------------------

def test_should_import_off_csv_data(data_importer):
    csv_content = "code\tproduct_name\n123\tMilk\n456\tCheese\n"
    mock_product = MagicMock(spec=Product)
    data_importer.product_mapper.map_off_row_to_product.return_value = mock_product

    with patch("builtins.open", mock_open(read_data=csv_content)), \
         patch("csv.reader", return_value=iter([["code", "product_name"], ["123", "Milk"], ["456", "Cheese"]])):
        result = data_importer.import_csv_off_data("mock_file.csv")

    assert len(result) == VALID_OFF_PRODUCT_COUNT, f"Expected {VALID_OFF_PRODUCT_COUNT} products, got {len(result)}"
