from domain.product.complexFields.ingredients import Ingredients
from domain.utils.ingredient_normalizer import IngredientNormalizer


class IngredientsMapper:
    def __init__(self, ingredient_normalizer: IngredientNormalizer):
        self.ingredient_normalizer = ingredient_normalizer

    def map_fdc_dict_to_ingredients(self, ingredients: str) -> Ingredients:
        """Maps the given ingredients string of a FDC product to an Ingredients object containing:
        - ingredients_list: a normalized list of ingredients
        - ingredients_text: the formatted ingredients string"""
        ingredients_list = self.ingredient_normalizer.normalise_ingredients_list(
            ingredients
        )

        return Ingredients(
            ingredients_list=ingredients_list, ingredients_text=ingredients.title()
        )

    def map_off_row_to_ingredients(
        self, row: list[str], header: list[str]
    ) -> Ingredients:
        """Maps the ingredients string of a given OFF (csv) product to an Ingredients object containing:
        - ingredients_list: a normalized list of ingredients
        - ingredients_text: the formatted ingredients string"""
        ingredients_text_index = header.index("ingredients_text")

        return Ingredients(
            ingredients_list=self.ingredient_normalizer.normalise_ingredients_list(
                row[ingredients_text_index]
            ),
            ingredients_text=row[ingredients_text_index].title(),
        )

    def map_off_dict_to_ingredients(self, product_dict: dict) -> Ingredients:
        """Maps the ingredients string of a given OFF (jsonl) product to an Ingredients object containing:
        - ingredients_list: a normalized list of ingredients
        - ingredients_text: the formatted ingredients string"""
        ingredients_text_field = "ingredients_text"

        return Ingredients(
            ingredients_list=self.ingredient_normalizer.normalise_ingredients_list(
                product_dict.get(ingredients_text_field)
            ),
            ingredients_text=product_dict.get(ingredients_text_field, "").title()
            or None,
        )
