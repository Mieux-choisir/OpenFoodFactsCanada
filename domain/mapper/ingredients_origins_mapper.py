from domain.product.complexFields.ingredients_origins import IngredientsOrigins


class IngredientsOriginMapper:
    @staticmethod
    def map_off_row_to_ingredients_origin(
        row: list[str], header: list[str]
    ) -> IngredientsOrigins:
        origin_index = header.index("origins")

        return IngredientsOrigins(
            origins=row[origin_index].split(","),
            percent=None,
            transportation_score=None,
        )

    @staticmethod
    def map_off_dict_to_ingredients_origin(product_dict: dict) -> IngredientsOrigins:
        origin_field = "origins"

        return IngredientsOrigins(
            origins=product_dict.get(origin_field),
            percent=None,
            transportation_score=None,
        )
