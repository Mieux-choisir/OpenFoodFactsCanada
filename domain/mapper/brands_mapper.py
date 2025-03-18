class BrandsMapper:

    @staticmethod
    def map_off_row_to_brands(row: list[str], header: list[str]) -> list[str]:
        brands_index = header.index("brands")

        brands = []
        if row[brands_index] is not None and row[brands_index] != "":
            brands = list(
                filter(None, map(str.strip, row[brands_index].title().split(",")))
            )
        return brands

    @staticmethod
    def map_off_row_to_brand_owner(row: list[str], header: list[str]) -> str | None:
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
        brands = []
        if product_dict[brands_field] is not None:
            brands = list(
                filter(
                    None, map(str.strip, product_dict[brands_field].title().split(","))
                )
            )
        return brands

    @staticmethod
    def map_off_dict_to_brand_owner(
        product_dict: dict, brand_owner_field: str, brands_field: str
    ) -> str | None:
        brand_owner_value = None
        if product_dict[brand_owner_field] is not None:
            brand_owner_value = product_dict[brand_owner_field].title().strip()
        elif product_dict[brands_field] is not None:
            brand_owner_value = product_dict[brands_field].title().strip()
        return brand_owner_value
