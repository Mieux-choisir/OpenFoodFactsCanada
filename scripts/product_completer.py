import logging

from domain.product.complexFields.ingredients import Ingredients
from domain.product.complexFields.nova_data import NovaData
from domain.product.complexFields.nutrient_facts import NutritionFacts
from domain.product.complexFields.score.ecoscore_data import EcoscoreData
from domain.product.complexFields.score.nutriscore_data import NutriscoreData
from domain.product.product import Product
from domain.utils.ingredient_normalizer import IngredientNormalizer


class ProductCompleter:
    def complete_products_data(self,
                               off_products: list[Product], fdc_products: list[Product]
                               ) -> list[Product]:
        """Completes the obtained OFF products with the data in the FDC products and returns a new completed list
        of products"""
        logging.info("Completing missing data for OFF products...")

        products = []
        for fdc_product in fdc_products:
            # try to find the same product in off products
            # if present : add the missing values
            off_product = self.__find_product(fdc_product, off_products)
            if off_product is not None:
                new_product = self.__complete_product(off_product, fdc_product)
                products.append(new_product)
            # else : add the whole product
            else:
                products.append(fdc_product)
            if len(products) > 100:
                continue
        logging.info("OFF products completed")
        return products

    @staticmethod
    def __find_product(searched_product: Product, products: list[Product]) -> Product | None:
        """Searches the product in the products list based on its id and returns it if it finds it"""
        for product in products:
            if product.id == searched_product.id:
                return product
        return None

    def __complete_product(self, off_product: Product, fdc_product: Product) -> Product:
        """Checks each field of the off_product and completes the ones that are missing values"""
        for field, fdc_value in fdc_product.__dict__.items():
            # if the off_product field is None, an empty list or a list of empty strings, complete it
            off_value = getattr(off_product, field, None)
            if off_value is None or (
                    isinstance(off_value, list)
                    and ((not off_value) or v == "" for v in off_value)
            ):
                setattr(off_product, field, fdc_value)
            elif isinstance(off_value, Ingredients):
                setattr(off_product, field,
                        self.__update_ingredients_values(off_value, fdc_value, IngredientNormalizer()))
            elif isinstance(off_value, NutriscoreData):
                setattr(off_product, field, self.__update_nutriscore_values(off_value, fdc_value))
            elif isinstance(off_value, NutritionFacts):
                setattr(
                    off_product, field, self.__update_nutrition_facts_values(off_value, fdc_value)
                )
            elif isinstance(off_value, EcoscoreData) or isinstance(off_value, NovaData):
                pass  # no useful information for these scores is present in fdc
        return off_product

    @staticmethod
    def __update_ingredients_values(
            off_value: Ingredients, fdc_value: Ingredients, ingredient_normalizer: IngredientNormalizer
    ) -> Ingredients:
        if off_value.ingredients_text is None:
            off_value.ingredients_text = fdc_value.ingredients_text
        if not off_value.ingredients_list:
            off_value.ingredients_list = ingredient_normalizer.normalise_ingredients_list(
                off_value.ingredients_text
            )
        return off_value

    @staticmethod
    def __update_nutriscore_values(
            off_value: NutriscoreData, fdc_value: NutriscoreData
    ) -> NutriscoreData:
        for field, value in off_value.__dict__.items():
            if value is None and getattr(fdc_value, field, None) is not None:
                setattr(off_value, field, getattr(fdc_value, field, None))
        return off_value

    @staticmethod
    def __update_nutrition_facts_values(
            off_value: NutritionFacts, fdc_value: NutritionFacts
    ) -> NutritionFacts:
        for field, value in off_value.nutrient_level:
            if value is None:
                setattr(
                    off_value.nutrient_level,
                    field,
                    getattr(fdc_value.nutrient_level, field, None),
                )

        for field, value in off_value.nutrients:
            if value is None:
                setattr(
                    off_value.nutrients, field, getattr(fdc_value.nutrients, field, None)
                )

        return off_value
