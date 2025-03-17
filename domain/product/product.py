# pylint: disable=missing-module-docstring, missing-function-docstring, missing-class-docstring
from typing import Optional, List

from domain.product.complexFields.complex_field import ComplexField
from domain.product.complexFields.ingredients import Ingredients
from domain.product.complexFields.nova_data import NovaData
from domain.product.complexFields.nutrient_facts import NutritionFacts
from domain.product.complexFields.score.ecoscore_data import EcoscoreData
from domain.product.complexFields.score.nutriscore_data import NutriscoreData


class Product(ComplexField):
    id: Optional[str] = None
    generic_name_en: Optional[str] = None
    product_name: Optional[str] = None
    categories_en: list[str] = None
    is_raw: Optional[bool] = None
    brands: List[str] = []
    brand_owner: Optional[str] = None
    food_groups_en: List[str] = []
    ingredients: Optional[Ingredients] = None
    nutrition_facts: Optional[NutritionFacts] = None
    allergens: List = []
    nutriscore_data: Optional[NutriscoreData] = NutriscoreData()
    ecoscore_data: Optional[EcoscoreData] = EcoscoreData()
    nova_data: Optional[NovaData] = NovaData()

    def has_atleast_one_score(self) -> bool:
        return self.product_name is not None and (
            self.nutriscore_data.score is not None
            or self.ecoscore_data.score is not None
            or self.nova_data.score is not None
        )
