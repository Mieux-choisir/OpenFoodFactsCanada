class Config:
    """
    This is a class that stores config values used by the scripts.

    Attributes:
        use_docker(bool): A boolean indicating if the script is executed on Docker
        off_jsonl_url(str): The url for downloading the Open Food Facts jsonl export
        fdc_json_url(str): The url for downloading the Food Data Central json export
        off_compressed_jsonl_file_name(str): The name of the downloaded compressed Open Food Facts jsonl file
        fdc_compressed_json_file_name(str): The name of the downloaded compressed Food Data Central json file
        off_jsonl_file_name(str): The name of the decompressed Open Food Facts jsonl file
        fdc_json_file_name(str): The name of the decompressed Food Data Central json file
        categories_taxonomy_file(str): The path from the root of the project to the Open Food Facts categories taxonomy file
        category_mapping_file(str): The path from the root of the project to the mapping of Food Data Central categories to Open Food Facts categories
    """

    def __init__(self):

        self.use_docker: bool = True

        self.off_jsonl_url: str = (
            "https://static.openfoodfacts.org/data/openfoodfacts-products.jsonl.gz"
        )
        self.fdc_json_url: str = (
            "https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_branded_food_json_2025-04-24.zip"
        )

        self.off_compressed_jsonl_file_name: str = "off_jsonl.gz"
        self.fdc_compressed_json_file_name: str = "fdc_branded.zip"

        self.off_jsonl_file_name: str = "off_jsonl.jsonl"
        self.fdc_json_file_name: str = "fdc_branded.json"

        self.categories_taxonomy_file: str = "source_files/categories_taxonomy.txt"
        self.category_mapping_file: str = "source_files/categories_mapping_fdc_off.json"
