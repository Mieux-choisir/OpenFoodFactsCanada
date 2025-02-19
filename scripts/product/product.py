# pylint: disable=missing-module-docstring, missing-function-docstring, missing-class-docstring
from typing import Optional, List, Dict
from pydantic import BaseModel, Field

from scripts.product.category_enum import CategoryEnum
from scripts.product.complexFields.complex_field import ComplexField
from scripts.product.complexFields.ingredients import Ingredients
from scripts.product.complexFields.nova_data import NovaData
from scripts.product.complexFields.nutrient_facts import NutritionFacts
from scripts.product.complexFields.score.ecoscore_data import EcoscoreData
from scripts.product.complexFields.score.nutriscore_data import NutriscoreData


class Product(ComplexField):
    id: Optional[str] = None
    generic_name_en: Optional[str] = None
    product_name: Optional[str] = None
    category_en: CategoryEnum = CategoryEnum.OTHER
    is_raw: Optional[bool] = None
    brand_name: Optional[str] = None
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
