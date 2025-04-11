# pylint: disable=missing-module-docstring, missing-function-docstring, missing-class-docstring
import datetime
from typing import Optional, List

from domain.product.complexFields.complex_field import ComplexField
from domain.product.complexFields.ingredients import Ingredients
from domain.product.complexFields.nova_data import NovaData
from domain.product.complexFields.nutrition_facts import NutritionFacts
from domain.product.complexFields.score.ecoscore_data import EcoscoreData
from domain.product.complexFields.score.nutriscore_data import NutriscoreData


class Product(ComplexField):
    """
    This is a class that stores data on the Nova data of a product.

    Attributes:
        id_match (Optional[int]): The formatted id used to match the products
        id_original (dict): The original id (not formatted) of the product
        product_name (Optional[str]): The name of the product
        data_source (Optional[str]): The source of the data obtained from the product
        modified_date (Optional[datetime.datetime]): The last date data of the product was modified
        available_date (Optional[datetime.datetime]): The date data of the product became first available
        publication_date (Optional[datetime.datetime]): The date data of the product was published
        quantity (Optional[str]): Quantity of the product
        categories_en (list[str]): List of the different categories of the product
        is_raw (Optional[bool]): Boolean indicating if the product is a raw product
        brands (list[str]): List of the brands of the product
        brand_owner (Optional[str]): Brand owner of the product
        food_groups_en (list[str]): List of the food groups of the product
        ingredients (Optional[Ingredients]): Data about the ingredients of the product
        serving_size (Optional[float]): The serving size of the product
        serving_size_unit (Optional[str]): The unit of the serving size of the product
        nutrition_facts (Optional[NutritionFacts]): Data about the nutrition facts of the product
        nutriscore_data (Optional[NutriscoreData]): Data about the NutriScore of the product
        ecoscore_data (Optional[EcoscoreData]): Data about the Eco-score of the product
        nova_data (Optional[NovaData]): Data about the Nova group of the product

    Methods:
        has_at_least_one_score(): Indicates whether the product has at least one score available (NutriScore, Eco-score or Nova group)
    """

    id_match: Optional[str] = None
    id_original: Optional[str] = None
    fdc_id: Optional[str] = None
    product_name: Optional[str] = None
    data_source: Optional[str] = None
    modified_date: Optional[datetime.datetime] = None
    available_date: Optional[datetime.datetime] = None
    publication_date: Optional[datetime.datetime] = None
    quantity: Optional[str] = None
    off_categories_en: list[str] = []
    fdc_category_en: str = None
    is_raw: Optional[bool] = None
    brands: List[str] = []
    brand_owner: Optional[str] = None
    food_groups_en: List[str] = []
    ingredients: Optional[Ingredients] = None
    serving_size: Optional[float] = None
    serving_size_unit: Optional[str] = None
    nutrition_facts: Optional[NutritionFacts] = None
    nutriscore_data: Optional[NutriscoreData] = NutriscoreData()
    ecoscore_data: Optional[EcoscoreData] = EcoscoreData()
    nova_data: Optional[NovaData] = NovaData()

    def has_at_least_one_score(self) -> bool:
        """Returns true if the product has at least one score available (ie not None)"""
        return self.product_name is not None and (
            self.nutriscore_data.score is not None
            or self.ecoscore_data.score is not None
            or self.nova_data.score is not None
        )
