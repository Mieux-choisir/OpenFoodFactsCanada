class BrandsMapper:
    """
    This is a class that maps products values to brands (list[str]) and brandOwner (str).

    Methods:
        map_off_row_to_brands(row, header): Maps the given csv row to its list of brands
        map_off_row_to_brand_owner(row, header): Maps the given csv row to its brand owner
        map_off_dict_to_brands(product_dict): Maps the given dictionary to its list of brands
        map_off_dict_to_brand_owner(product_dict): Maps the given dictionary to its brand owner
    """

    @staticmethod
    def map_off_row_to_brands(row: list[str], header: list[str]) -> list[str]:
        """Maps the values in a given OFF (csv) product to a list of brands (list[str])"""
        brands_index = header.index("brands")

        brands = []
        if row[brands_index] is not None and row[brands_index] != "":
            brands = list(
                filter(None, map(str.strip, row[brands_index].title().split(",")))
            )
        return brands

    @staticmethod
    def map_off_row_to_brand_owner(row: list[str], header: list[str]) -> str | None:
        """Maps the values in a given OFF (csv) product to its brand owner (str) if it exists"""
        brands_index = header.index("brands")
        brand_owner_index = header.index("brand_owner")

        brand_owner = None
        if row[brand_owner_index] is not None and row[brand_owner_index] != "":
            brand_owner = row[brand_owner_index].title().strip()
        elif row[brands_index] is not None and row[brands_index] != "":
            brand_owner = row[brands_index].split(",")[0].title().strip()
        return brand_owner

    @staticmethod
    def map_off_dict_to_brands(product_dict: dict, brands_field: str) -> list[str]:
        """Maps the values in a given OFF (jsonl) product to a list of brands (list[str])"""
        brands = []
        if product_dict.get(brands_field) is not None:
            brands = list(
                filter(
                    None,
                    map(str.strip, product_dict.get(brands_field).title().split(",")),
                )
            )
        return brands

    @staticmethod
    def map_off_dict_to_brand_owner(
        product_dict: dict, brand_owner_field: str, brands_field: str
    ) -> str | None:
        """Maps the values in a given OFF (jsonl) product to its brand owner (str) if it exists"""
        brand_owner_value = None
        if product_dict.get(brand_owner_field) is not None:
            brand_owner_value = product_dict.get(brand_owner_field).title().strip()
        elif product_dict.get(brands_field) is not None:
            brand_owner_value = product_dict.get(brands_field).title().strip()
        return brand_owner_value
