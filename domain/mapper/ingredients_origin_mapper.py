from domain.product.complexFields.ingredients_origin import IngredientsOrigin


class IngredientsOriginMapper:
    @staticmethod
    def map_off_row_to_ingredients_origin(
        row: list[str], header: list[str]
    ) -> IngredientsOrigin:
        origin_index = header.index("origins")

        return IngredientsOrigin(
            origin=row[origin_index],
            percent=None,
            transportation_score=None,
        )

    @staticmethod
    def map_off_dict_to_ingredients_origin(product_dict: dict) -> IngredientsOrigin:
        origin_field = "origins"

        return IngredientsOrigin(
            origin=product_dict.get(origin_field),
            percent=None,
            transportation_score=None,
        )
