from domain.product.complexFields.ingredients import Ingredients
from domain.utils.ingredient_normalizer import IngredientNormalizer


class IngredientsMapper:
    def __init__(self, ingredient_normalizer: IngredientNormalizer):
        self.ingredient_normalizer = ingredient_normalizer

    def map_fdc_dict_to_ingredients(self, ingredients: str) -> Ingredients:
        ingredients_list = self.ingredient_normalizer.normalise_ingredients_list(
            ingredients
        )

        return Ingredients(
            ingredients_list=ingredients_list, ingredients_text=ingredients.title()
        )

    def map_off_row_to_ingredients(
        self, row: list[str], header: list[str]
    ) -> Ingredients:
        ingredients_text_index = header.index("ingredients_text")
        ingredients_list_index = header.index("ingredients_tags")

        return Ingredients(
            ingredients_text=row[ingredients_text_index],
            ingredients_list=(
                row[ingredients_list_index].split(",") if row[ingredients_list_index] else []
            ),
        )

    def map_off_dict_to_ingredients(self, product_dict: dict) -> Ingredients:
        ingredients_text_field = "ingredients_text"
        ingredients_list_field = "ingredients_tags"

        return Ingredients(
            ingredients_text=product_dict.get(ingredients_text_field),
            ingredients_list=product_dict.get(ingredients_list_field, []),
        )
