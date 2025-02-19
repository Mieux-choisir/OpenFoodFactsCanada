from scripts.product.complexFields.ingredients import Ingredients
from scripts.utils import normalise_ingredients_list


class IngredientsMapper:
    @staticmethod
    def map_fdc_dict_to_ingredients(ingredients: str) -> Ingredients:
        ingredients_list = normalise_ingredients_list(ingredients)

        return Ingredients(
            ingredients_list=ingredients_list,
            ingredients_text=ingredients.title()
        )

    @staticmethod
    def map_off_row_to_ingredients(row: list[str], header: list[str]) -> Ingredients:
        ingredients_text_field = header.index("ingredients_text")

        return Ingredients(
            ingredients_list=[],
            ingredients_text=row[ingredients_text_field],
        )

    @staticmethod
    def map_off_dict_to_ingredients(product_dict: dict) -> Ingredients:
        ingredients_text_field = "ingredients_text"

        return Ingredients(
            ingredients_list=[],
            ingredients_text=product_dict[ingredients_text_field],
        )
