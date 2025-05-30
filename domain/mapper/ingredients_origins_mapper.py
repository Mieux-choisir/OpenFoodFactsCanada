from domain.product.complexFields.ingredients_origins import IngredientsOrigins


class IngredientsOriginMapper:
    """
    This is a class that maps products values to IngredientsOrigins objects.

    Methods:
        map_off_dict_to_ingredients_origin(product_dict): Maps the given dictionary to an IngredientsOrigins object
    """

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
