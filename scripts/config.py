class Config:
    def __init__(self):
        self.off_csv_url: str = (
            "https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.csv.gz"
        )
        self.off_jsonl_url: str = (
            "https://static.openfoodfacts.org/data/openfoodfacts-products.jsonl.gz"
        )
        self.fdc_json_url: str = (
            "https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_branded_food_json_2024-10-31.zip"
        )

        self.off_compressed_csv_file_name: str = "off_csv.gz"
        self.off_compressed_jsonl_file_name: str = "off_jsonl.gz"
        self.fdc_compressed_json_file_name: str = "fdc_branded.zip"

        self.off_csv_file_name: str = "off_csv.csv"
        self.off_jsonl_file_name: str = "off_jsonl.jsonl"
        self.fdc_json_file_name: str = "fdc_branded.json"

        self.categories_taxonomy_file: str = "source_files/categories_taxonomy.txt"
        self.category_mapping_file: str = "source_files/categories_mapping_fdc_off.json"
