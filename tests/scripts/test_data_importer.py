import pytest
from unittest.mock import MagicMock, mock_open, patch

from domain.mapper.product_mapper import ProductMapper
from domain.product.product import Product
from scripts.data_importer import DataImporter

VALID_FDC_PRODUCT_COUNT = 2
VALID_OFF_PRODUCT_COUNT = 2
LIMITED_OFF_PRODUCT_COUNT = 1
BATCH_SIZE = 1000


@pytest.fixture
def product_mapper():
    return MagicMock(spec=ProductMapper)


@pytest.fixture
def data_importer(product_mapper):
    return DataImporter(product_mapper)


# ----------------------------------------------------------------
# Tests import_json_fdc_data
# ----------------------------------------------------------------


@patch("scripts.data_loader.DataLoader.load_products_to_mongo")
def test_should_import_fdc_data_when_valid_json(mock_loader, data_importer):
    json_content = """
    {
        "BrandedFoods": [
            {"marketCountry": "United States", "gtinUpc": "12345"},
            {"marketCountry": "United States", "gtinUpc": "67890"}
        ]
    }
    """
    mock_product = MagicMock(spec=Product)
    mock_mapper = MagicMock(spec=ProductMapper)
    mock_mapper.map_fdc_dict_to_product = MagicMock(return_value=mock_product)

    data_importer = DataImporter(mock_mapper)
    data_importer.config = MagicMock()
    data_importer.config.use_docker = False

    with patch("builtins.open", mock_open(read_data=json_content)):
        data_importer.import_json_fdc_data("mock_file.json", BATCH_SIZE)

    assert mock_mapper.map_fdc_dict_to_product.call_count == 2
    mock_loader.assert_called()


@patch("scripts.data_loader.DataLoader.load_products_to_mongo")
def test_should_ignore_non_us_products_in_fdc_data(mock_loader, data_importer):
    json_content = """
    {
        "BrandedFoods": [
            {"marketCountry": "Canada", "gtinUpc": "12345"},
            {"marketCountry": "United States", "gtinUpc": "67890"}
        ]
    }
    """
    mock_product = MagicMock(spec=Product)
    mock_mapper = MagicMock(spec=ProductMapper)
    mock_mapper.map_fdc_dict_to_product = MagicMock(return_value=mock_product)

    data_importer = DataImporter(mock_mapper)
    data_importer.config = MagicMock()
    data_importer.config.use_docker = False

    with patch("builtins.open", mock_open(read_data=json_content)):
        data_importer.import_json_fdc_data("mock_file.json", BATCH_SIZE)

    assert mock_mapper.map_fdc_dict_to_product.call_count == 1


@patch("scripts.data_loader.DataLoader.load_products_to_mongo")
def test_should_return_empty_list_when_fdc_file_is_empty(mock_loader, data_importer):
    json_content = "{}"

    mock_mapper = MagicMock(spec=ProductMapper)
    mock_mapper.map_fdc_dict_to_product = MagicMock()

    data_importer = DataImporter(mock_mapper)
    data_importer.config = MagicMock()
    data_importer.config.use_docker = False

    with patch("builtins.open", mock_open(read_data=json_content)):
        data_importer.import_json_fdc_data("mock_file.json", BATCH_SIZE)

    mock_mapper.map_fdc_dict_to_product.assert_not_called()
    mock_loader.assert_called_once_with(
        [], collection_name="fdc_products", use_docker=False
    )


# ----------------------------------------------------------------
# Tests import_jsonl_off_data
# ----------------------------------------------------------------


@patch("scripts.data_loader.DataLoader.load_products_to_mongo")
def test_should_import_off_jsonl_data(mock_loader, data_importer):
    json_lines = '{"code": "123"}\n{"code": "456"}\n'
    mock_product = MagicMock(spec=Product)
    data_importer.product_mapper.map_off_dict_to_product.return_value = mock_product
    data_importer.config = MagicMock()
    data_importer.config.use_docker = False

    with patch("builtins.open", mock_open(read_data=json_lines)):
        data_importer.import_jsonl_off_data("mock_file.jsonl", batch_size=100)

    mock_loader.assert_called_once_with(
        [mock_product, mock_product], collection_name="off_products", use_docker=False
    )


@patch("scripts.data_loader.DataLoader.load_products_to_mongo")
def test_should_apply_limit_on_off_jsonl_data(mock_loader, data_importer):
    json_lines = '{"code": "123"}\n{"code": "456"}\n'
    mock_product = MagicMock(spec=Product)
    data_importer.product_mapper.map_off_dict_to_product.return_value = mock_product
    data_importer.config = MagicMock()
    data_importer.config.use_docker = False

    with patch("builtins.open", mock_open(read_data=json_lines)):
        data_importer.import_jsonl_off_data("mock_file.jsonl", batch_size=100, limit=1)

    mock_loader.assert_called_once_with(
        [mock_product], collection_name="off_products", use_docker=False
    )


# ----------------------------------------------------------------
# Tests import_csv_off_data
# ----------------------------------------------------------------


def test_should_import_off_csv_data(data_importer):
    csv_content = "code\tproduct_name\n123\tMilk\n456\tCheese\n"
    mock_product = MagicMock(spec=Product)
    data_importer.product_mapper.map_off_row_to_product.return_value = mock_product

    with patch("builtins.open", mock_open(read_data=csv_content)), patch(
        "csv.reader",
        return_value=iter(
            [["code", "product_name"], ["123", "Milk"], ["456", "Cheese"]]
        ),
    ):
        result = data_importer.import_csv_off_data("mock_file.csv")

    assert (
        len(result) == VALID_OFF_PRODUCT_COUNT
    ), f"Expected {VALID_OFF_PRODUCT_COUNT} products, got {len(result)}"
