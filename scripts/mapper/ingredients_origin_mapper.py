from scripts.product.complexFields.ingredients_origin import IngredientsOrigin


class IngredientsOriginMapper:
    @staticmethod
    def map_row_to_ingredients_origin(
            row: list[str], header: list[str]
    ) -> IngredientsOrigin:
        origin_field = header.index("origins")

        return IngredientsOrigin(
            origin=row[origin_field],
            percent=None,
            transportation_score=None,
        )

    @staticmethod
    def map_dict_to_ingredients_origin(product_dict: dict) -> IngredientsOrigin:
        origin_field = "origins"

        return IngredientsOrigin(
            origin=product_dict[origin_field],
            percent=None,
            transportation_score=None,
        )