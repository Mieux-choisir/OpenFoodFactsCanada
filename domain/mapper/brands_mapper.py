class BrandsMapper:
    """
    This is a class that maps products values to brands (list[str]) and brandOwner (str).

    Methods:
        map_off_dict_to_brands(product_dict): Maps the given dictionary to its list of brands
        map_off_dict_to_brand_owner(product_dict): Maps the given dictionary to its brand owner
    """

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
