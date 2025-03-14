class BrandsMapper:

    @staticmethod
    def map_off_row_to_brands(row: list[str], header: list[str]) -> list[str]:
        brands_index = header.index("brands")

        brands = []
        if row[brands_index] is not None and row[brands_index] != "":
            brands = row[brands_index].split(",")
        return brands

    @staticmethod
    def map_off_row_to_brand_owner(row: list[str], header: list[str]) -> str | None:
        brands_index = header.index("brands")
        brand_owner_index = header.index("brand_owner")

        brand_owner = None
        if row[brand_owner_index] is not None and row[brand_owner_index] != "":
            brand_owner = row[brand_owner_index]
        elif row[brands_index] is not None and row[brands_index] != "":
            brand_owner = row[brands_index]
        return brand_owner

    @staticmethod
    def map_off_dict_to_brands(product_dict: dict, brands_field: str) -> list[str]:
        brands_value = []
        if product_dict.get(brands_field) is not None:
            brands_value = product_dict.get(brands_field).title().split(",")
        return brands_value

    @staticmethod
    def map_off_dict_to_brand_owner(
        product_dict: dict, brand_owner_field: str, brands_field: str
    ) -> str | None:
        brand_owner_value = None
        if product_dict.get(brand_owner_field) is not None:
            brand_owner_value = product_dict.get(brand_owner_field).title()
        elif product_dict.get(brands_field) is not None:
            brand_owner_value = product_dict.get(brands_field).title()
        return brand_owner_value
