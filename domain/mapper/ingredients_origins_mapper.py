from domain.product.complexFields.ingredients_origins import IngredientsOrigins


class IngredientsOriginMapper:
    @staticmethod
    def map_off_row_to_ingredients_origin(
        row: list[str], header: list[str]
    ) -> IngredientsOrigins:
        """Maps the ingredients origins of a given OFF (csv) product to an IngredientsOrigins object containing:
        - origins: a list of the ingredients origins
        - percent: the percentage of the origins
        - transportation_score: the transportation score of the product"""
        origin_index = header.index("origins")

        return IngredientsOrigins(
            origins=row[origin_index].split(","),
            percent=None,
            transportation_score=None,
        )

    @staticmethod
    def map_off_dict_to_ingredients_origin(product_dict: dict) -> IngredientsOrigins:
        """Maps the ingredients origins of a given OFF (jsonl) product to an IngredientsOrigins object containing:
        - origins: a list of the ingredients origins
        - percent: the percentage of the origins
        - transportation_score: the transportation score of the product"""
        origin_field = "origins"
        origins_value = product_dict.get(origin_field, [])

        if isinstance(origins_value, str):
            origins_value = [origins_value.strip()] if origins_value.strip() else []

        return IngredientsOrigins(
            origins=origins_value,
            percent=None,
            transportation_score=None,
        )
